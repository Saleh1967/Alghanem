"""فهرسُ بوّابات المعنى (BAWWABAT_INDEX.md) من `slge.bawwabat` وجدولِه المرسى في ج3، ثمّ على مودَع
المصحف.

١. البوّاباتُ بأسطرها؛ ٢. جدولُ الأدوات على الهيئات كاملًا (تخليصٌ أو قلب) والأزمنةُ المبلوغة؛ ٣. جدولُ صدق
العطف؛
٤. العمومُ بالدور؛ ٥. على مودَع المصحف (`corpus-certificates.json.gz`، تيّارُ المواقع): كلُّ أداةٍ مستقلّةٍ
بخاناتها
بعينها، وصيغةُ الكلمة التالية بقارئ الصيغة (`jiha.sigha`، والمضارعُ بأيّ حالةٍ للآخر) — فحصٌ لمجال الأداة
على المودَع،
لا قياسٌ على مرجعٍ محجوب.
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from slge import bawwabat as B
from slge.bawwabat_table import GATES
from slge.huruf import TABLE as HURUF
from slge.jiha import sigha
from slge.zuruf import set_last

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "BAWWABAT_INDEX.md"
DATA = ROOT / "tests" / "data"
Word = tuple[tuple[str, str], ...]

STANDALONE: tuple[str, ...] = ("sawfa", "an", "inShart", "inNafy", "la", "lan", "lam", "lamma",
                               "ma",
                               "qad")
"""الأدواتُ المستقلّة كلماتٍ (السينُ سابقةٌ تقرؤها `jiha`)؛ وإِنْ الشرطيّةُ والنافيةُ خاناتٌ واحدة، ولا ولا."""

AR: dict[str, str] = {"sin": "سَ", "sawfa": "سَوْفَ", "an": "أَنْ", "inShart": "إِنْ (الشرط)",
                      "la": "لَا", "lan": "لَنْ", "lam": "لَمْ", "lamma": "لَمَّا", "ma": "مَا",
                      "inNafy": "إِنْ (النفي)", "qad": "قَدْ"}
HAY: dict[str, str] = {"madi": "الماضي", "mudari": "المضارع", "amr": "الأمر"}
TIMES = ("ماضٍ", "قريب", "حال", "مستقبل")


def _az(z: B.Azmina | None) -> str:
    if z is None:
        return "—"
    return "{" + "، ".join(t for t, on in zip(TIMES, z, strict=True) if on) + "}"


def _stream() -> list[Word]:
    with gzip.open(DATA / "corpus-certificates.json.gz", "rt", encoding="utf-8") as f:
        d: dict[str, Any] = json.load(f)
    forms = [tuple((a, b) for a, b in x["cells"]) for x in d["forms"]]
    return [forms[i] for i in d["stream"]]


def _sigha_any(w: Word) -> str | None:
    s = sigha(w)
    if s is not None:
        return s
    return "مضارع" if w and sigha(set_last(w, "ضم")) == "مضارع" else None


def measure() -> dict[str, Any]:
    toks = _stream()
    cells: dict[str, Word] = {a: tuple(HURUF[B.ADAT_HARF[a]].cells) for a in STANDALONE}
    after: dict[str, Counter[str]] = {}
    seen: dict[Word, str] = {}
    for a in STANDALONE:
        w = cells[a]
        if w in seen:  # إِنْ الشرطيّةُ والنافية، ولا: خاناتٌ واحدة — تُعدّ مرّةً باسم الأولى
            continue
        seen[w] = a
        after[a] = Counter()
    for i, t in enumerate(toks[:-1]):
        hit = seen.get(t)
        if hit is None:
            continue
        after[hit][_sigha_any(toks[i + 1]) or "غيرُ فعلٍ مقروء"] += 1
    return {"tokens": len(toks),
            "after": {a: dict(sorted(c.items())) for a, c in after.items()},
            "shared": {AR[a]: AR[seen[cells[a]]] for a in STANDALONE if seen[cells[a]] != a}}


def render(m: dict[str, Any]) -> str:
    out = ["# فهرسُ بوّابات المعنى — الزمنُ والعطفُ والتخصيصُ والعموم", "",
           "مولَّدٌ بـ`python tools/gen_bawwabat_index.py` من `src/slge/bawwabat.py` وجدولِه المرسى "
           "(`tools/deposit_bawwabat.py`)؛ لا يُحرَّر باليد. البرهانُ `formal/Slge/Bawwabat.lean` (ADR"
           " ٥٥): "
           "تخليصٌ أو قلبٌ لا ثالث (`takhlis_xor_qalb`)، والأزمنةُ المبلوغة خمسٌ (`reach_exhausted`)، "
           "والترتيبُ تعقيبٌ أو تراخٍ (`tartib_split`)، والتخصيصُ لا يُدخل (`istithna_sub`…)، "
           "والشرطُ ومفهومُه قسمة (`shart_mafhum_partition`). المبرهَنُ خواصُّ هذا الجبر المنقول لا"
           " اللغة.", "",
           "## ١. البوّاباتُ بأسطرها في ج3 المختوم", "",
           "| المفتاح | البوّابة | السطر |", "|---|---|---|"]
    out += [f"| `{k}` | {n} | {ln} |" for k, n, ln, _ in GATES]
    out += ["", "## ٢. الزمن: الهيئةُ والأداة", "",
            "الأوقاتُ أربعة لأنّ النصَّ يسمّي «الماضي القريب من الحال». الأمرُ لا يسمّي النصُّ زمنَه "
            "(`AMR_TIME_UNSOURCED`).", "",
            "| الهيئة | زمنُها |", "|---|---|"]
    out += [f"| {HAY[h]} | {_az(B.zaman_of(h))} |" for h in B.HAYAA]
    out += ["", "| الأداة | على | الناتج | العمليّة | نفي |", "|---|---|---|---|---|"]
    for a in B.ADAT:
        for h in B.HAYAA:
            z = B.apply(a, h)
            if z is None:
                continue
            kind = "تخليص" if B.takhlis(a, h) else "قلب"
            nafy = "نعم" if a in B.NAFY else ""
            out.append(f"| {AR[a]} | {HAY[h]} | {_az(z)} | {kind} | {nafy} |")
    out += ["", "الأزمنةُ المبلوغة (الاستنفاد): " + "، ".join(_az(z) for z in B.reach()) + ".", "",
            "## ٣. العطف", "",
            "| الحرف | الصدق |", "|---|---|",
            "| وَ | الأوّلُ والثاني (تبادليّ) |", "| فَ | الأوّلُ والثاني، والثاني عقبَ الأوّل |",
            "| ثُمَّ | الأوّلُ والثاني، وبينهما فاصل |",
            "| حَتَّى | الأوّلُ والثاني، والثاني بعد الأوّل (الجزئيّةُ: `HATTA_JUZ_NOT_MODELED`) |",
            "| أَوْ، أَمْ | أحدُهما على الأقلّ؛ وأَمْ في الاستفهام وحده |",
            "| لَا، بَلْ، لَكِنْ | أحدُهما بعينه دون الآخر |", "",
            "## ٤. العموم بالدور", "",
            "| الصيغة | " + " | ".join(B.DAWR) + " |", "|---|" + "---|" * len(B.DAWR)]
    for s in B.SIYAGH:
        out.append(f"| {s} | " + " | ".join(B.umum(s, d) or "—" for d in B.DAWR) + " |")
    out += ["", "## ٥. على مودَع المصحف — ما يلي الأداةَ المستقلّة (مفحوصٌ لا مقيس)", "",
            f"تيّارُ المواقع: {m['tokens']:,} موقعًا. الكلمةُ التالية بقارئ الصيغة `jiha.sigha` "
            "(والمضارعُ بأيّ حالةٍ للآخر)؛ «غيرُ فعلٍ مقروء» = اسمٌ أو فعلٌ بسابقةٍ أو ما لا يقرؤه"
            " القالب.", "",
            "| الأداة | ماضٍ | مضارع | أمر | غيرُ فعلٍ مقروء |", "|---|---|---|---|---|"]
    for a, c in m["after"].items():
        out.append(f"| {AR[a]} | {c.get('ماضٍ', 0):,} | {c.get('مضارع', 0):,} | "
                   f"{c.get('أمر', 0):,} | "
                   f"{c.get('غيرُ فعلٍ مقروء', 0):,} |")
    out += ["", "خاناتٌ واحدة تُعدّ مرّةً باسم الأولى: "
            + "، ".join(f"{k} = {v}" for k, v in m["shared"].items()) + " — لا تفصلها الخانات.", "",
            "## ما ليس هنا — باسمه", "",
            "- `AMR_TIME_UNSOURCED`: زمنُ الأمر لا يسمّيه مبحثُ الفعل في ج3.",
            "- `HATTA_JUZ_NOT_MODELED`: «المعطوفُ جزءٌ من المعطوف عليه» علاقةُ مجموعتين لا صدقُ"
            " قضيّتين.",
            "- `IN_NAFY_SHART_SAME_CELLS`: إِنْ النافيةُ والشرطيّة خاناتٌ واحدة، فالعمليّةُ تختارها"
            " القرينة لا الخانة.",
            "- `QAD_MUDARI_UNSOURCED`: «قَدْ» على المضارع واقعٌ في المودَع (الجدول أعلاه) ولا يذكره"
            " مبحثُ الحرف"
            " إلّا على الماضي؛ فلا عمليّةَ له هنا.",
            "- `LAMMA_AN_MA_MADI_SAME_CELLS`: ما يلي «لَمَّا» و«أَنْ» و«مَا» ماضيًا كلماتٌ بخانات الأداة"
            " نفسِها"
            " وبابٍ آخر (الحينيّة، المصدريّة، الموصولة) — الخانةُ لا تفصلها.",
            "- `SIGHA_READS_FEW`: «غيرُ فعلٍ مقروء» يجمع الاسمَ والفعلَ الذي لا يقرؤه قالبٌ بعد تسوية"
            " الآخر"
            " (المعتلُّ المجزوم، والفعلُ بلاحقة)؛ فالأعمدةُ حدٌّ أدنى لا توزيع.",
            "- الوقتُ القريب من الحال لا يُقاس على مرجعٍ هنا؛ والمجالُ الواقعيُّ للحكم (العامّ) من طبقة"
            " الحكم.", ""]
    return "\n".join(out)


def main(argv: list[str]) -> int:
    text = render(measure())
    if "--check" in argv:
        ok = TARGET.read_text(encoding="utf-8") == text
        sys.stdout.write("BAWWABAT_INDEX.md مطابق\n" if ok else "BAWWABAT_INDEX.md غيرُ مطابق\n")
        return 0 if ok else 1
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب BAWWABAT_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
