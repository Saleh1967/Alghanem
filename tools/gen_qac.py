"""المجالُ المعلَنُ الخامس — جذورُ Quranic Arabic Corpus 0.4 مرجعًا محجوبًا للاسترجاع (ADR ٤١،
قرارُ المالك 2026-10-12).

**الواقع.** وسمُ Kais Dukes الصرفيّ للمصحف (الإصدار 0.4، 2011؛ GPL، النسخُ بلا تغيير)، منسوخًا
بعينه من `q-ran/quran@bb97fe4` إلى `corpora/qac/quranic-corpus-morphology-0.4.txt.gz` (ضغطٌ بلا
طابع زمن)، وبصمتُه بعد فكّ الضغط `QAC_SHA256` — الختم. لكلّ كلمةٍ (سورة:آية:كلمة) قطعٌ، وعلى
قطعة الجذع `ROOT:` بحروف Buckwalter. البوّابةُ لم تقرأه قطّ؛ فهو حكمٌ بشريٌّ محجوبٌ عن شيفرتها.

**المحاذاة** (`align`) على المدوّنة المختومة `corpora/quran-simple-enhanced.txt` — الآيةُ سطرٌ
بالترتيب نفسه، والموقعُ رمزٌ فيه حرف (الرموزُ الأخرى علاماتُ وقف). قاعدتان مسمّاتان معلَنتان
قبل القياس:

* `BASMALA`: أوّلُ آيةٍ من كلّ سورةٍ غير الفاتحة والتوبة تبدأ في طبعتنا بالبسملة ولا يعدّها QAC
  — تُترك مواقعُها الأربعة.
* `YA_JOINED`: «يَا» «وَيَا» «هَا» منفصلةٌ عندنا متّصلةٌ بما بعدها عنده — تُضمّ إلى الموقع
  التالي، والجذرُ على الموقع التالي (الأخير في الضمّة).

وما لم يتساوَ عددُه بعدهما يُترك آيةً كاملةً باسمه `ALIGN_RESIDUAL` (يُعدّ ولا يُخمَّن).

**المرجع** (`reference` → `corpora/qac/qac-roots.tsv`): لكلّ كلمةٍ في QAC لها `ROOT` موقعُها
(السطر، الرمز، عدّاهما من 1 كترقيم إطار عيّنة الأحكام)، والكلمةُ من مدوّنتنا، والجذرُ بالأصول
الثمانية والعشرين (`BW`)، وقسمُها (`POS`)، وجهتُها للفعل (`PERF`/`IMPF`/`IMPV`)، وهل له سابقة
(`PREFIX`).

**القياس** (`measure` → `docs/qac/result.json`) كما سُجّل في `docs/qac/PREREG.md`: كلُّ كلمةٍ
تدخل `Gate().enter` أوّلًا (والمرفوضُ يُعدّ باسمه)، ثمّ `gate.recover` على الموقع بعينه؛ لا
تقشيرَ ولا تطبيعَ هنا.

`--check` يُسقط البناءَ بأسمائها: `QAC_SOURCE_DRIFTED`، `QAC_REFERENCE_DRIFTED`،
`QAC_RESULT_DRIFTED`. الأداةُ معفاةٌ في الحارس لأنّها أداةُ إيداع.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import io
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

QAC = ROOT / "corpora" / "qac" / "quranic-corpus-morphology-0.4.txt.gz"
QAC_SHA256 = "a1d12923815341face765083805d2148ed2d9f5cc3f7d6665219d887675d8c46"
CORPUS = ROOT / "corpora" / "quran-simple-enhanced.txt"
REFERENCE = ROOT / "corpora" / "qac" / "qac-roots.tsv"
RESULT = ROOT / "docs" / "qac" / "result.json"
SEEN_FRAME = ROOT / "corpora" / "hukm-sample-frame.tsv"
"""مواقعُ عيّنة الأحكام رآها الوكيلُ وجذّرها بيده (ADR ٣٩)، فهي خارجَ القياس (PREREG §٤)."""

BW: dict[str, str] = {
    "A": "ء", "b": "ب", "t": "ت", "v": "ث", "j": "ج", "H": "ح", "x": "خ", "d": "د", "*": "ذ",
    "r": "ر", "z": "ز", "s": "س", "$": "ش", "S": "ص", "D": "ض", "T": "ط", "Z": "ظ", "E": "ع",
    "g": "غ", "f": "ف", "q": "ق", "k": "ك", "l": "ل", "m": "م", "n": "ن", "h": "ه", "w": "و",
    "y": "ي",
}
"""حروفُ جذور QAC (‎28‎ حرفًا كما وُجدت في الملفّ) ← الأصولُ الثمانية والعشرون؛ و`A` في الجذر همزة."""

LETTER = re.compile(r"[ء-يٱ]")
MARKS = re.compile(r"[ً-ْٰ]")
BASMALA = ("بسم", "الله", "الرحمن", "الرحيم")
YA_JOINED = frozenset({"يا", "ويا", "ها"})
MABNI = frozenset({"PERF", "IMPV"})
FIELDS = ("line", "pos", "loc", "word", "root", "tag", "aspect", "prefix")


def source() -> bytes:
    return gzip.decompress(QAC.read_bytes())


def qac_words(data: bytes) -> dict[tuple[int, int], list[tuple[int, list[str]]]]:
    """‎(سورة، آية) ← [(رقمُ الكلمة، خصائصُ قطعها)]‎ بالترتيب."""

    out: dict[tuple[int, int], dict[int, list[str]]] = {}
    for ln in data.decode("utf-8").splitlines():
        if not ln.startswith("("):
            continue
        loc, _form, _tag, feats = ln.split("\t")
        s, v, w, _seg = (int(x) for x in loc.strip("()").split(":"))
        out.setdefault((s, v), {}).setdefault(w, []).append(feats)
    return {k: sorted(ws.items()) for k, ws in out.items()}


def bare(token: str) -> str:
    return MARKS.sub("", token)


def groups(s: int, v: int, raw: list[str]) -> tuple[list[list[int]], bool]:
    """مواقعُ الكلمات (فهارسُ الرموز) مضمومةً بـ`YA_JOINED` بعد ترك `BASMALA`، وهل تُركت."""

    idx = [j for j, t in enumerate(raw) if LETTER.search(t)]
    dropped = False
    if v == 1 and s not in (1, 9) and tuple(bare(raw[j]) for j in idx[:4]) == BASMALA:
        idx, dropped = idx[4:], True
    out: list[list[int]] = []
    pending: list[int] = []
    for j in idx:
        pending.append(j)
        if bare(raw[j]) not in YA_JOINED:
            out.append(pending)
            pending = []
    if pending:
        out.append(pending)
    return out, dropped


def field(feats: list[str], key: str) -> str:
    for f in feats:
        m = re.search(rf"(?:^|\|){key}:([^|]+)", f)
        if m:
            return m.group(1)
    return ""


def align(data: bytes, corpus: str) -> tuple[list[dict[str, str]], Counter[str], list[str]]:
    """صفوفُ المرجع، وعدّادُ القاعدتين، والآياتُ المتروكة بـ`ALIGN_RESIDUAL`."""

    words = qac_words(data)
    lines = corpus.splitlines()
    keys = sorted(words)
    assert len(keys) == len(lines), "QAC_VERSE_COUNT"
    rows: list[dict[str, str]] = []
    rules: Counter[str] = Counter()
    residual: list[str] = []
    for i, (s, v) in enumerate(keys):
        raw = lines[i].split(" ")
        gs, dropped = groups(s, v, raw)
        rules["BASMALA"] += dropped
        rules["YA_JOINED"] += sum(len(g) - 1 for g in gs)
        if len(gs) != len(words[(s, v)]):
            residual.append(f"{s}:{v}")
            continue
        for g, (w, feats) in zip(gs, words[(s, v)], strict=True):
            root = field(feats, "ROOT")
            if not root:
                continue
            stem = [f for f in feats if f.startswith("STEM")]
            aspect = next(
                (a for a in ("PERF", "IMPF", "IMPV") if any(f"|{a}" in f for f in stem)), "-")
            rows.append({
                "line": str(i + 1), "pos": str(g[-1] + 1), "loc": f"{s}:{v}:{w}",
                "word": raw[g[-1]],
                "root": "".join(BW[c] for c in root), "tag": field(stem, "POS"), "aspect": aspect,
                "prefix": "1" if any(f.startswith("PREFIX") for f in feats) else "0",
            })
    return rows, rules, residual


def render(rows: list[dict[str, str]]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def reference_text() -> str:
    data = source()
    rows, _, _ = align(data, CORPUS.read_text(encoding="utf-8"))
    return render(rows)


def read_reference() -> list[dict[str, str]]:
    with REFERENCE.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def seen() -> set[tuple[str, str]]:
    with SEEN_FRAME.open(encoding="utf-8", newline="") as f:
        return {(r["line"], r["pos"]) for r in csv.DictReader(f, delimiter="\t")}


def wilson(k: int, n: int, z: float = 1.959964) -> list[float]:
    if n == 0:
        return [0.0, 0.0]
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(c - h, 6), round(c + h, 6)]


def wy(root: str) -> str:
    """لامُ الناقص بلا تمييزٍ بين واوٍ وياء (الثانويّ `NAQIS_LAM_WAW_YA`)."""

    return root[:-1] + "ي" if root.endswith("و") else root


def judge(word: str, root: str, gate_obj: object) -> str:
    from gate import Refusal, recover

    if isinstance(gate_obj.enter(word.encode("utf-8")), Refusal):  # type: ignore[attr-defined]
        return "refused"
    roots = {r[0] for r in recover(word)[1]}
    if not roots:
        return "no_reading"
    if roots == {root}:
        return "agree_unique"
    if root in roots:
        return "agree_among"
    if wy(root) in {wy(r) for r in roots}:
        return "disagree_waw_ya"
    return "disagree"


def tally(rows: list[dict[str, str]], gate_obj: object) -> dict[str, object]:
    c: Counter[str] = Counter(judge(r["word"], r["root"], gate_obj) for r in rows)
    n = len(rows)
    hit = c["agree_unique"] + c["agree_among"]
    covered = n - c["refused"] - c["no_reading"]
    return {
        "n": n, "outcomes": dict(sorted(c.items())),
        "agree_any": hit, "agree_any_rate": round(hit / n, 6) if n else 0.0,
        "agree_any_wilson95": wilson(hit, n),
        "agree_unique_rate": round(c["agree_unique"] / n, 6) if n else 0.0,
        "agree_mod_waw_ya_rate": round((hit + c["disagree_waw_ya"]) / n, 6) if n else 0.0,
        "covered": covered, "agree_among_covered_rate": round(hit / covered, 6) if covered else 0.0,
    }


def measure() -> dict[str, object]:
    from gate.api import Gate

    g = Gate()
    rows = read_reference()
    skip = seen()
    pool = [r for r in rows if (r["line"], r["pos"]) not in skip]
    verbs = [r for r in pool if r["tag"] == "V" and r["aspect"] in MABNI]
    _, rules, residual = align(source(), CORPUS.read_text(encoding="utf-8"))
    return {
        "prereg": "docs/qac/PREREG.md",
        "reference_sha256": QAC_SHA256,
        "alignment": {"rules": dict(sorted(rules.items())), "residual_verses": residual,
                      "rooted_rows": len(rows), "excluded_seen": len(rows) - len(pool)},
        "primary_mabni_verbs": tally(verbs, g),
        "primary_by_prefix": {
            p: tally([r for r in verbs if r["prefix"] == p], g) for p in ("0", "1")},
        "secondary_all_rooted": tally(pool, g),
    }


def dump(obj: object) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + "\n"


def check() -> list[str]:
    bad: list[str] = []
    if hashlib.sha256(source()).hexdigest() != QAC_SHA256:
        return ["QAC_SOURCE_DRIFTED"]
    if not REFERENCE.exists() or REFERENCE.read_text(encoding="utf-8") != reference_text():
        bad.append("QAC_REFERENCE_DRIFTED")
    if RESULT.exists() and RESULT.read_text(encoding="utf-8") != dump(measure()):
        bad.append("QAC_RESULT_DRIFTED")
    return bad


def main(argv: list[str]) -> int:
    if "--check" in argv:
        bad = check()
        rows = read_reference()
        state = "مطابقة" if RESULT.exists() else "لم تُقس بعد"
        ok = f"مرجعُ QAC مطابق: {len(rows):,} كلمةً مجذورة؛ النتيجة {state}"
        print(", ".join(bad) if bad else ok)
        return 1 if bad else 0
    if argv[:1] == ["measure"]:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(dump(measure()), encoding="utf-8")
        print(f"كُتب {RESULT.relative_to(ROOT)}")
        return 0
    REFERENCE.write_text(reference_text(), encoding="utf-8")
    print(f"كُتب {REFERENCE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
