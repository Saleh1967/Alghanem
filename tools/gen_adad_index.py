"""ولّد `ADAD_INDEX.md`: فهرسُ العدد على درجات الترخيص التدريجيّ من `slge.adad`، وقياسُ حكم المعدود
على شريحة MASAQ المجمَّدة (أعدادٌ بشهادات البوّابة ومعدودُها)؛ ‎--check‎ يفشل إن كان قديمًا."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from slge.adad import (
    STEMS,
    TEN_FEM,
    TEN_MASC,
    UQUD,
    compound,
    fem,
    masc,
    tamyiz_state,
    twelve,
    uqud,
)
from slge.cells import STATES, Cell, index

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "ADAD_INDEX.md"
SLICE = ROOT / "tests" / "data" / "masaq-adad.json"
_A, _I, _U, SUKUN = STATES
COUNTED_ROLES = {"مضاف إليه", "تمييز"}
RANGE_N = {"3-10": 7, "11-19": 15, "20-90": 40, "100": 100, "1000": 1000}


def measure() -> tuple[Counter[tuple[str, str, bool]], int, int]:
    """(المدى، حالةُ المعدود، مطابقٌ للقانون؟) على المواضع التي يلي فيها المعدودُ العددَ."""

    rows = json.loads(SLICE.read_text(encoding="utf-8"))
    out: Counter[tuple[str, str, bool]] = Counter()
    counted = 0
    for row in rows:
        if row["counted_role"] not in COUNTED_ROLES:
            continue
        counted += 1
        cells = [(c[0], c[1]) for c in row["counted_cells"]]
        st = cells[-2][1] if row["tanwin"] else cells[-1][1]
        want_state, _, _ = tamyiz_state(RANGE_N[row["cat"]])
        # الحالةُ هي القانون؛ التنوينُ تبعٌ للتعريف والإضافة. والممنوعُ من الصرف يُجرّ بالفتحة بلا
        # تنوين (سَنَابِلَ، مَسَاكِينَ) فهو مطابق
        ok = st == want_state or (want_state == _I and st == _A and not row["tanwin"])
        label = ("تنوين " if row["tanwin"] else "") + st
        out[(row["cat"], label, ok)] += 1
    return out, counted, len(rows)


def k(w: tuple[Cell, ...]) -> str:
    return "-".join(str(index(c)) for c in w)


def render() -> str:
    table, counted, total = measure()
    ok = sum(v for (_, _, o), v in table.items() if o)
    lines = [
        "# فهرسُ العدد على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_adad_index.py` من `src/slge/adad.py`؛ لا يُحرَّر باليد. "
        "البرهانُ: `formal/Slge/Adad.lean`.",
        "",
        "## د١٦ الإعراب من الخانة — المخالفة تاءٌ واحدة (3–10)", "",
        "المذكّرُ = الجذعُ مفتوحًا + تاءٌ بحركة الإعراب؛ المؤنّثُ = الجذعُ بحركة الإعراب "
        "(`fem_is_masc_without_ta`). جنسُ المعدود يُقرأ من التاء بعد فتحة الجذع (`genderOf_masc`، "
        "`genderOf_fem_forms`)؛ وسِتُّ تاؤها أصلٌ بعد ساكن (`six_ta_is_radical`).", "",
        "| العدد | مذكّر (رفع) | مؤنّث (رفع) |", "|---|---|---|",
        *[f"| {n} | `{k(masc(s, _U))}` | `{k(fem(s, _U))}` |" for n, s in STEMS.items()],
        "",
        "## د٨ الحدّ — التركيب (11–19) واثنا عشر", "",
        "الجزءان مفتوحان (`compound_both_fatha`)؛ عَشَرَ للمذكّر وعَشْرَةَ للمؤنّث، الشينُ مفتوحةٌ أو "
        "ساكنة (`shin_law`). اثنا عشر: إعرابُ الجزء الأوّل من مدّه (`twelve_case`).", "",
        f"- عَشَرَ: `{k(TEN_MASC)}`؛ عَشْرَةَ: `{k(TEN_FEM)}`.",
        f"- ثَلَاثَةَ عَشَرَ: `{k(compound(STEMS[3], True))}`؛ "
        f"ثَلَاثَ عَشْرَةَ: `{k(compound(STEMS[3], False))}`.",
        f"- اثْنَا عَشَرَ: `{k(twelve(True, True))}`؛ اثْنَيْ عَشَرَ: `{k(twelve(False, True))}`؛ "
        f"اثْنَتَا عَشْرَةَ: `{k(twelve(True, False))}`.", "",
        "## د١٦ الإعراب من الخانة — العقود (20–90)", "",
        "ملحقةٌ بجمع المذكّر السالم: ُونَ رفعٌ، ِينَ نصبٌ/جرّ، والحركةُ قبل المدّ من جنسه (`uqud_case`).", "",
        "| العقد | رفع | نصب/جرّ |", "|---|---|---|",
        *[f"| {n} | `{k(uqud(s, True))}` | `{k(uqud(s, False))}` |" for n, s in UQUD.items()],
        "",
        "## التمييز — دالّةٌ في مدى العدد، مقيسةٌ على MASAQ", "",
        "| مدى العدد | حالةُ المعدود (القانون) |", "|---|---|",
        "| 3–10 | جمعٌ مجرور (كسرٌ أو تنوينُ كسر؛ والممنوعُ من الصرف بالفتحة) |",
        "| 11–99 | مفردٌ منصوبٌ منوَّن |", "| 100، 1000 | مفردٌ مجرور |", "",
        f"على {total} عددًا بشهادات البوّابة، يلي المعدودُ العددَ في {counted} موضعًا (مضافًا إليه أو "
        f"تمييزًا): **المطابقُ للقانون {ok}/{counted}** (والواحدُ: عَشْرُ أَمْثَالِهَا — معدودٌ مضافٌ إلى "
        "ضميرٍ لم يُقطَع في هذا القياس).", "",
        "| المدى | حالةُ المعدود | مطابق | العدد |", "|---|---|---|---|",
        *[f"| {a} | {b} | {'نعم' if o else 'لا'} | {v} |" for (a, b, o), v in table.most_common()],
        "",
        "## خارج الخانة — باسمه", "",
        "- مِائَة وأَلْف: صورةٌ واحدة للجنسين (الحياد) — لا تاءَ تُقرأ: معلن.",
        "- المعطوفُ (21–99): كلمتان بواو العطف؛ كلٌّ بقانونها: المفردُ ثمّ العقد.",
        "- واحد واثنان: نعتٌ يطابق؛ إعرابُ اثنين بالمدّ كالمثنّى (`twelve_case` للمركّب).",
        "- تذكيرُ المعدود بمفرده لا بجمعه: من المعجم لا من الخانة.", "",
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    text = render()
    if "--check" in argv:
        if not TARGET.exists() or TARGET.read_text(encoding="utf-8") != text:
            print("ADAD_INDEX.md قديم: شغّل python tools/gen_adad_index.py", file=sys.stderr)
            return 1
        print("ADAD_INDEX.md مطابق")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    print(f"كُتب {TARGET.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
