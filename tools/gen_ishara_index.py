"""ولّد `ISHARA_INDEX.md`: فهرسُ أسماء الإشارة على درجات الترخيص التدريجيّ من `slge.ishara`؛
‎--check‎ يفشل إن كان قديمًا."""

from __future__ import annotations

import sys
from pathlib import Path

from slge.cells import index
from slge.ishara import FORMS, WITNESSED, case_of, tier

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "ISHARA_INDEX.md"
TIERS = ("د١٦ الإعراب من الخانة (المثنّى)", "د٨ الحدّ (تنبيهٌ أو بُعد)", "د٤ الخانة (مبنيٌّ على نواته)")
WHAT = {
    TIERS[0]: "الحالةُ تُقرأ من المدّ قبل النون: ا رفعٌ، ي نصبٌ/جرّ (`caseOf_dual`، `caseOf_dual_bud`)؛ "
              "ولا تفرّق الياءُ بين النصب والجرّ (`nasb_eq_jarr_dual`).",
    TIERS[1]: "النواةُ بعمليّةٍ على حدّها: هَ التنبيه في الصدر (`tanbih_licensed`) أو لامُ البعد وكافُ "
              "الخطاب في العجز (`bud_licensed`)؛ مبنيّةٌ: لا حالةَ تُقرأ (`mabni_no_case`).",
    TIERS[2]: "النواةُ وحدَها أو ظرفُ المكان: خاناتٌ مرخَّصة (`forms_licensed`)، لا حالةَ تُقرأ.",
}


def render() -> str:
    lines = [
        "# فهرسُ أسماء الإشارة على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_ishara_index.py` من `src/slge/ishara.py`؛ لا يُحرَّر باليد. "
        "البرهانُ: `formal/Slge/Ishara.lean`.",
        "",
        f"**{len(FORMS)} صورةً** — {len(WITNESSED)} منها من شهادات البوّابة بعينها، "
        "والباقي بالقانون. "
        "الدلالةُ (قريب/بعيد، مفرد/مثنّى/جمع، مذكّر/مؤنّث) من الحصر المُرسَل **معلن**؛ ما تقرؤه الخانةُ "
        "مبرهَن: التنبيهُ والبعدُ والتثنيةُ ثلاثُ عمليّاتٍ على نواة.",
        "",
    ]
    for t in TIERS:
        fs = [f for f in FORMS if tier(f) == t]
        lines += [f"## {t} — {len(fs)}", "", WHAT[t], "",
                  "| الاسم | الباب | الخانات | ما تقرؤه الخانة | الدلالة (معلن) | الشاهد |",
                  "|---|---|---|---|---|---|"]
        for f in fs:
            key = "-".join(str(index(c)) for c in f.cells)
            lines.append(f"| {f.name} | {f.bab} | `{key}` | {case_of(f.cells) or 'مبنيّ'} | "
                         f"{f.dalala} | {'شهادة' if f.witnessed else 'بالقانون'} |")
        lines.append("")
    lines += ["## ما لا تفصله الخانة — باسمه", "",
              "- محلُّ المبنيّ (رفعٌ أو نصبٌ أو جرّ): من موقعه في النظم لا من خانته.",
              "- ظرفيّةُ المكان (في محلّ نصب): من الموقع كذلك.",
              "- ثَمَّ الإشاريّةُ وثُمَّ العاطفة: تفصلهما خانةُ الثاء (فتحٌ/ضمّ) — وهذا مقروءٌ من الخانة.", ""]
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    text = render()
    if "--check" in argv:
        if not TARGET.exists() or TARGET.read_text(encoding="utf-8") != text:
            print("ISHARA_INDEX.md قديم: شغّل python tools/gen_ishara_index.py", file=sys.stderr)
            return 1
        print("ISHARA_INDEX.md مطابق")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    print(f"كُتب {TARGET.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
