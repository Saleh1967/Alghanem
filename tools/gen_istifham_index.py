"""ولّد `ISTIFHAM_INDEX.md`: فهرسُ أسماء الاستفهام على درجات الترخيص التدريجيّ من `slge.istifham`،
وقياسُ الصدارة على شريحة MASAQ المجمَّدة؛ ‎--check‎ يفشل إن كان قديمًا."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from slge.cells import index
from slge.istifham import FORMS, case_of, tier

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "ISTIFHAM_INDEX.md"
SLICE = ROOT / "tests" / "data" / "masaq-interrog.json"
TIERS = ("د١٦ الإعراب من الخانة (أَيّ)", "د٨ الحدّ (تركيبٌ على الخانات)", "د٤ الخانة (مبنيٌّ أو حرف)")
WHAT = {
    TIERS[0]: "الحالةُ تُقرأ من الخانة الأخيرة؛ صورُه الثلاث تختلف فيها لا غير (`caseOf_ayy`، "
              "`ayy_differs_only_in_state`، `ayy_three_forms`).",
    TIERS[1]: "تركيبٌ بعمليّةٍ على الخانات: مَا ++ ذَا، وصلُ مَنْ ذَا، أَمْ ++ مَنْ، والجارُّ ++ مَ بحذف الألف "
              "ثمّ الإدغام (`madha_is_ma_dha`، `man_dha_junction`، `ma_after_jarr`، "
              "`amma_is_an_ma_idgham`، `idghamNM_length`).",
    TIERS[2]: "صورةٌ واحدةٌ مرخَّصة لا تظهر عليها حالة (`mabni_single_form`)؛ والهمزةُ حرفٌ متّصل "
              "(`hamza_prefix_licensed`).",
}
FRONT = {"CONJ", "CONJ_PART", "PREP", "INTERROG", "INTERROG_PART", "RSLT"}


def precedence() -> tuple[int, int, int, Counter[str]]:
    """(صدرُ الآية أو بعد عاطف/جارّ/همزة، بعد فعلِ قولٍ ونظرٍ وسؤال ونحوه، الكلّ، تفصيلُ الباقي)."""

    rows = json.loads(SLICE.read_text(encoding="utf-8"))
    front = other = 0
    rest: Counter[str] = Counter()
    for row in rows:
        prev = row["prev"]
        if prev is None or prev[1] in FRONT:
            front += 1
        else:
            other += 1
            rest[prev[1]] += 1
    return front, other, len(rows), rest


def render() -> str:
    front, other, total, rest = precedence()
    lines = [
        "# فهرسُ أسماء الاستفهام على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_istifham_index.py` من `src/slge/istifham.py`؛ لا يُحرَّر باليد. "
        "البرهانُ: `formal/Slge/Istifham.lean`.",
        "",
        f"**{len(FORMS)} صورةً** — {sum(f.witnessed for f in FORMS)} منها من شهادات البوّابة بعينها. "
        "الدلالةُ (عاقل، غير عاقل، زمان، مكان، حال، عدد) من الحصر المُرسَل **معلن**؛ "
        "ما تقرؤه الخانةُ مبرهَن.",
        "",
    ]
    for t in TIERS:
        fs = [f for f in FORMS if tier(f) == t]
        lines += [f"## {t} — {len(fs)}", "", WHAT[t], "",
                  "| الاسم | النوع | الخانات | ما تقرؤه الخانة | الدلالة (معلن) | الشاهد |",
                  "|---|---|---|---|---|---|"]
        for f in fs:
            key = "-".join(str(index(c)) for c in f.cells)
            lines.append(f"| {f.name} | {f.kind} | `{key}` | {case_of(f.cells) or 'مبنيّ'} | "
                         f"{f.dalala} | {'شهادة' if f.witnessed else 'بالقانون'} |")
        lines.append("")
    lines += [
        "## الصدارة — مقيسةٌ لا مبرهَنة", "",
        f"على شريحة MASAQ المجمَّدة ({total} اسمَ استفهامٍ موسومًا `INTERROG_PRON`): "
        f"**{front}** في صدر الآية أو بعد عاطفٍ أو جارٍّ أو همزة ({100 * front // total}%)، "
        f"و**{other}** بعد غير ذلك — أكثرُه أفعالُ القول والنظر والسؤال (قَالَ، انْظُرْ، يَسْأَلُ) فالاسمُ في "
        "صدر **جملته** لا الآية. فالصدارةُ صدارةُ جملةٍ، ولا تُقاس بلا حدٍّ للجملة: دَينٌ مسمًّى "
        "على النظم.", "",
        "| ما قبله (وسم MASAQ) | العدد |", "|---|---|",
        *[f"| {k} | {v} |" for k, v in rest.most_common(8)], "",
        "## ما لا تفصله الخانة — باسمه", "",
        "- مَنْ ومَا: استفهامٌ أم شرطٌ أم موصول — الخانةُ واحدة؛ الفصلُ من التيار.",
        "- محلُّ المبنيّ: من موقعه في النظم.",
        "- كَأَيِّنْ: ليست في المدوّنة بهذا الرسم: خارج الجدول.", "",
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    text = render()
    if "--check" in argv:
        if not TARGET.exists() or TARGET.read_text(encoding="utf-8") != text:
            print("ISTIFHAM_INDEX.md قديم: شغّل python tools/gen_istifham_index.py", file=sys.stderr)
            return 1
        print("ISTIFHAM_INDEX.md مطابق")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    print(f"كُتب {TARGET.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
