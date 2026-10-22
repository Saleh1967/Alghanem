"""شاهدُ المصحف على مرجع المالك (ADR ١١٨): الولاداتُ المشهودةُ في سياقها، والحروفُ ومثانيها.

المرجعُ قانونٌ مولَّدٌ من Lean: `formal/a116/marja.csv` (1044 ولادةً لكلّ خانةٍ في موضعها)
و`marja-azwaj.csv` (841 زوجًا بقسمها في قانون الإدغام). وهذه الأداةُ تعدّ ما يشهد له المصحفُ
المختوم **عبر البوّابة في سياق كلّ موقع** (`tools/gen_context_certificates.generate`: الآيةُ سطر،
أوّلُها ابتداءٌ وآخرُها وقف، والموصولُ بما قبله) — لا نصَّ خارج البوّابة.

الموضعُ من التيّار (`docs/marja/PREREG.md` §٢):
* **وجهُ الوصل على الحدّ يُطبَّق أوّلًا** (تعيينُ البنّاء، م٢٢): إن حملت شهادةُ الكلمة وجهًا
  (`FARQ_ALIF_DROPPED`، `MADD_DROPPED`، `SAKIN_KASRA`) فآخرُ الكلمة السابقة يُحذف أو يُكسَر
  كما تحكم البوّابة (`gate.licence.repair_junction`) قبل العدّ — فالمعدودُ السطرُ المصلَحُ
  الذي ترخّصه البوّابة لا صورةُ الكلمة قبل الإصلاح؛ وعددُ كلّ وجهٍ يُنشر.
* الخانةُ الأولى في الكلمة الأولى من الآية: **ابتداء**.
* الخانةُ الأولى في كلمةٍ موصولة: **وصلٌ** بعد حالة آخر خانةٍ في الكلمة السابقة بعد الإصلاح
  (إن كانت جاهزة).
* الخانةُ j > 0: **وصلٌ** بعد حالة الخانة ‎j−1‎، إلّا آخرَ خانةٍ في الكلمة الأخيرة من الآية فهي
  **وقفٌ** بعد حالة ما قبلها.
* **H2 داخلَ الكلمة وحدَها** (‎j > 0‎)؛ والساكنُ بعد ساكنٍ على الحدّ يُعدّ وصفًا
  (`hadd_sakin_ba3d_sakin`) لا فرضيّة.

المخرَج `docs/marja/shahid.json`: عددُ كلّ ولادةٍ مشهودة بعددها n في المرجع، والحروفُ كمًّا
(مبدأُ الكمّ عند الكندي، بعبارتي)، والأزواجُ المتجاورة داخلَ الكلمة وعلى الحدّ (مبدأُ الائتلاف عنده،
بعبارتي) بقسمها، والفرضيّتان المسجَّلتان مسبقًا بأعداد مخالفاتهما وأعيانها. **والغيابُ ليس امتناعًا**
(الدستور م١٣، م١٦): ما لم يُشهد يُسمّى «غيرَ مشهود».

`python tools/gen_marja.py` يكتب المخرَج؛ و`--check` يعيد الحسابَ ويقارنه بالمودَع قيمةً قيمة
(`SHAHID_DRIFTED`).
"""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from gen_context_certificates import generate  # noqa: E402

OUT = ROOT / "docs" / "marja" / "shahid.json"
PREREG = ROOT / "docs" / "marja" / "PREREG.md"
MARJA = ROOT / "formal" / "a116" / "marja.csv"
AZWAJ = ROOT / "formal" / "a116" / "marja-azwaj.csv"
HAL = {"فتح": "fatha", "ضم": "damma", "كسر": "kasra", "سكون": "sukun"}
FARQ = (("ء", "fatha"), ("ا", "sukun"))
MADD = {("ا", "fatha"), ("و", "damma"), ("ي", "kasra")}

Key = tuple[str, str, str]
Pair = tuple[str, str]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


DROP = ("FARQ_ALIF_DROPPED", "MADD_DROPPED")


def islah(form: list[tuple[str, str]], wajh: str) -> list[tuple[str, str]]:
    """وجهُ الوصل على آخر الكلمة اليسرى (`gate.licence.repair_junction`): الألفُ الفارقة
    وحرفُ المدّ يُحذفان، والساكنُ يُكسَر."""

    if wajh in DROP:
        return form[:-1]
    if wajh == "SAKIN_KASRA":
        return [*form[:-1], (form[-1][0], "kasra")]
    raise ValueError(wajh)


def births(ctx: dict[str, Any]) -> tuple[Counter[Key], Counter[str], list[dict[str, Any]],
                                        Counter[Pair], Counter[Pair], Counter[str]]:
    """الولاداتُ المشهودة على السطر المصلَح، والمتروكُ بسببه، ومواضعُ H2 داخلَ الكلمة بسياقها،
    وأزواجُ الحروف داخلَ الكلمة وعلى الحدّ، وأوجهُ الوصل وما على الحدّ من ساكنٍ بعد ساكن."""

    forms = [[(c, HAL[s]) for c, s in f["cells"]] for f in ctx["forms"]]
    wujuh = ctx["junctions"]
    seen: Counter[Key] = Counter()
    skipped: Counter[str] = Counter()
    mashrut: list[dict[str, Any]] = []
    inside: Counter[Pair] = Counter()
    seam: Counter[Pair] = Counter()
    extra: Counter[str] = Counter()
    pos = 0
    for satr, length in enumerate(ctx["line_lengths"]):
        entries = ctx["stream"][pos:pos + length]
        pos += length
        line: list[list[tuple[str, str]] | None] = [
            forms[e[0]] if e[0] >= 0 else None for e in entries]
        for i in range(1, length):
            jw = entries[i][3]
            if entries[i][0] >= 0 and jw >= 0:
                extra[f"wajh:{wujuh[jw]}"] += 1
                left = line[i - 1]
                if left is not None:
                    line[i - 1] = islah(left, wujuh[jw])
        prev_form: list[tuple[str, str]] | None = None
        tark = "LEFT_REFUSED"
        for i, w in enumerate(line):
            exit_ = entries[i][1]
            if w is None:
                skipped["REFUSED_TOKEN"] += 1
                prev_form, tark = None, "LEFT_REFUSED"
                continue
            if not w:
                skipped["EMPTY_AFTER_REPAIR"] += 1
                prev_form, tark = None, "LEFT_EMPTY"
                continue
            last_word = i == length - 1
            for j, (c, h) in enumerate(w):
                if j == 0 and i == 0:
                    mawdi, before = "ibtida", None
                elif j == 0:
                    if prev_form is None:
                        skipped[tark] += 1
                        continue
                    before = prev_form[-1]
                    mawdi = "waqf" if (last_word and exit_ == 1 and len(w) == 1) else "wasl"
                    seam[(before[0], c)] += 1
                else:
                    before = w[j - 1]
                    final = last_word and exit_ == 1 and j == len(w) - 1
                    mawdi = "waqf" if final else "wasl"
                    inside[(before[0], c)] += 1
                key = (c, h, mawdi if before is None else f"{mawdi}:{before[1]}")
                seen[key] += 1
                sakin2 = (mawdi == "wasl" and before is not None and before[1] == "sukun"
                          and h == "sukun")
                if sakin2 and j == 0:
                    extra["hadd_sakin_ba3d_sakin"] += 1
                elif sakin2 and before is not None:
                    nxt = w[j + 1] if j + 1 < len(w) else None
                    geminate = nxt is not None and nxt[0] == c and nxt[1] != "sukun"
                    farq = j == 2 and tuple(w[:2]) == FARQ and c == "ل"
                    ante = w[j - 2] if j >= 2 else None
                    madd = ante is not None and (before[0], ante[1]) in MADD
                    mashrut.append({"satr": satr, "kalima": i, "j": j, "harf": c,
                                    "geminate": geminate, "farq": farq, "madd_before": madd})
            prev_form = w
    return seen, skipped, mashrut, inside, seam, extra


def h2_mukhalif(m: dict[str, Any]) -> bool:
    """مخالفةُ H2: ساكنٌ بعد ساكنٍ داخلَ الكلمة ليس قبله مدٌّ، أو ليس أوّلَ مثلين
    ولا لامَ «ءَ اْ لْ»."""

    return not (m["madd_before"] and (m["geminate"] or m["farq"]))


def by_qism(pairs: Counter[Pair], qism: dict[Pair, str]) -> dict[str, dict[str, int]]:
    """لكلّ قسمٍ من قانون الإدغام: عددُ أزواجه، والمشهودُ منها، ومواقعُها."""

    out: dict[str, dict[str, int]] = {}
    for q in sorted(set(qism.values())):
        keys = [p for p, qq in qism.items() if qq == q]
        out[q] = {"azwaj": len(keys), "mashhud": sum(1 for p in keys if pairs[p] > 0),
                  "mawaqi": sum(pairs[p] for p in keys)}
    return out


def generate_shahid() -> dict[str, Any]:
    ctx = generate("quran")
    law = {(r["harf"], r["haraka"], r["mawdi"]): r for r in table(MARJA)}
    seen, skipped, mashrut, inside, seam, extra = births(ctx)

    def n_of(k: Key) -> int:
        return int(law[k]["n"])

    unknown = sorted(k for k in seen if k not in law)
    by_hukm: Counter[str] = Counter()
    by_hukm_tokens: Counter[str] = Counter()
    h1: list[dict[str, Any]] = []
    for k, v in seen.items():
        if k in law:
            hk = law[k]["hukm"]
            by_hukm[hk] += 1
            by_hukm_tokens[hk] += v
            if hk not in ("murakhkhas", "mashrut"):
                h1.append({"n": n_of(k), "harf": k[0], "haraka": k[1], "mawdi": k[2],
                           "count": v, "hukm": hk, "ism": law[k]["shart"]})
    licensed = {k for k, r in law.items() if r["hukm"] in ("murakhkhas", "mashrut")}
    unattested = sorted((n_of(k), *k) for k in licensed if k not in seen)
    h2 = [m for m in mashrut if h2_mukhalif(m)]
    harf: Counter[str] = Counter()
    for (c, _, _), v in seen.items():
        harf[c] += v
    qism = {(r["a"], r["b"]): r["qism"] for r in table(AZWAJ)}
    attested = sorted(((n_of(k), k, v) for k, v in seen.items() if k in law))
    return {
        "version": 1,
        "source": "gate.enter في سياق كلّ موقع (gen_context_certificates.generate)"
                  " على المصحف المختوم",
        "corpus_sha256": ctx["corpus_sha256"],
        "prereg_sha256": sha(PREREG),
        "marja_sha256": sha(MARJA),
        "azwaj_sha256": sha(AZWAJ),
        "tool_sha256": sha(Path(__file__).resolve()),
        "tokens": ctx["tokens"],
        "status": ctx["status"],
        "skipped": dict(sorted(skipped.items())),
        "wujuh_wa_hadd": dict(sorted(extra.items())),
        "cells_counted": sum(seen.values()),
        "births_attested": len(seen),
        "births_licensed": len(licensed),
        "births_licensed_unattested": len(unattested),
        "attested_by_hukm": dict(sorted(by_hukm.items())),
        "attested_tokens_by_hukm": dict(sorted(by_hukm_tokens.items())),
        "unknown_keys": [list(k) for k in unknown],
        "H1": {"statement": "كلُّ ولادةٍ مشهودةٍ حكمُها في المرجع مرخَّصٌ أو مشروط",
               "violations": len(h1), "list": sorted(h1, key=lambda d: d["n"])},
        "H2": {"statement": "كلُّ ساكنٍ بعد ساكنٍ وصلًا داخلَ كلمةٍ قبله مدٌّ ويليه مثلُه متحرّكًا"
                            " أو هو لامُ «ءَ اْ لْ»",
               "sites": len(mashrut), "violations": len(h2),
               "geminate": sum(1 for m in mashrut if m["geminate"]),
               "farq": sum(1 for m in mashrut if m["farq"]),
               "list": h2},
        "births": [{"n": n, "harf": k[0], "haraka": k[1], "mawdi": k[2], "count": v}
                   for n, k, v in attested],
        "unattested": [{"n": n, "harf": a, "haraka": b, "mawdi": m} for n, a, b, m in unattested],
        "huruf": {"total": sum(harf.values()),
                  "rank": [[c, v] for c, v in sorted(harf.items(),
                                                     key=lambda kv: (-kv[1], kv[0]))]},
        "azwaj_dakhil": by_qism(inside, qism),
        "azwaj_hadd": by_qism(seam, qism),
        "azwaj_dakhil_mashhud": sum(1 for p in inside if inside[p] > 0),
        "azwaj_hadd_mashhud": sum(1 for p in seam if seam[p] > 0),
    }


def canonical(d: dict[str, Any]) -> str:
    return json.dumps(d, ensure_ascii=False, sort_keys=True, indent=1) + "\n"


def main(argv: list[str]) -> int:
    if len(argv) == 2 and argv[1] == "--check":
        if not OUT.exists():
            sys.stderr.write("SHAHID_DRIFTED: docs/marja/shahid.json غيرُ مودَع\n")
            return 1
        fresh = canonical(generate_shahid())
        if OUT.read_text(encoding="utf-8") != fresh:
            sys.stderr.write("SHAHID_DRIFTED: docs/marja/shahid.json ليس ما تحسبه الأداةُ الآن\n")
            return 1
        digest = hashlib.sha256(fresh.encode()).hexdigest()
        sys.stdout.write(f"شاهدُ المرجع هو ما تحسبه البوّابة الآن: {digest}\n")
        return 0
    if len(argv) != 1:
        sys.stderr.write("gen_marja.py | --check\n")
        return 2
    fresh = canonical(generate_shahid())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(fresh, encoding="utf-8")
    sys.stdout.write(f"كُتب {OUT.relative_to(ROOT)}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
