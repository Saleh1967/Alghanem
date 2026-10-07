"""إيداعُ الجهة الوجوديّة لكلّ قالبٍ من بابه المودَع: جدولُ Lean `formal/Slge/WujudTable.lean`
ومرآتُه `src/slge/wujud_table.py` مولَّدان من `slge.wazn.AWZAN` (بابُ كلّ وزنٍ كما أُودع من كتب
الصرف — معلَن).

الأصنافُ ستّة لا سابعَ لها: فعلٌ (ماضٍ ومضارعٌ وأمر)، مصدرٌ (المجرّدُ والمزيدُ والمرّةُ والهيئةُ
والصناعيّ)، وصفٌ مشتقّ (الفاعلُ والمفعولُ والمبالغةُ والصفةُ المشبّهة والتفضيلُ ومؤنّثاتُها)،
اسمٌ مشتقٌّ غيرُ وصفٍ (الزمانُ والمكانُ والآلة)، صيغةُ جمع (القلّةُ والكثرةُ ومنتهى الجموع: شكلٌ
لا نوع)، واسمٌ (أبنيةُ سيبويه والتصغير: مصدرٌ أو جامدٌ لا تفصله الخانة). بـ`--check` يقارن
الجدولين بما يولَّد الآن.
"""

from __future__ import annotations

import sys
from pathlib import Path

from slge.wazn import AWZAN

ROOT = Path(__file__).resolve().parent.parent
LEAN = ROOT / "formal" / "Slge" / "WujudTable.lean"
PY = ROOT / "src" / "slge" / "wujud_table.py"
FIL, MASDAR, WASF, ZARF, JAM, ISM = "فعل", "مصدر", "وصف", "ظرف وآلة", "جمع", "اسم"
LEAN_NAME = {FIL: "fil", MASDAR: "masdar", WASF: "wasf", ZARF: "zarfAla", JAM: "jam", ISM: "ism"}


def ont_of_bab(bab: str) -> str:
    if "ماضٍ" in bab or "مضارع" in bab or "أمر" in bab:
        return FIL
    if bab.startswith("مصدر") or bab in ("اسم مرّة", "اسم هيئة"):
        return MASDAR
    if bab.startswith(("اسم فاعل", "اسم مفعول", "مبالغة", "صفة مشبّهة", "تأنيث")):
        return WASF
    if bab in ("اسم مكان", "اسم آلة"):
        return ZARF
    if "جمع" in bab or bab == "منتهى الجموع":
        return JAM
    if bab in ("اسم (أبنية)", "تصغير"):
        return ISM
    raise SystemExit(f"BAB_WITHOUT_ONTOLOGY:{bab}")


def table() -> list[str]:
    out = []
    for w in AWZAN:
        if w.bab == "مصدر ميميّ / زمان ومكان":
            out.append(ZARF)  # مَفْعَل/مَفْعِل: زمانٌ ومكانٌ (ومصدرٌ ميميٌّ لا تفصله الخانة) — معلَن
        else:
            out.append(ont_of_bab(w.bab))
    return out


def render_lean(ont: list[str]) -> str:
    lines = [
        "import Slge.Bridge", "",
        "/-! الجهةُ الوجوديّة لكلّ قالبٍ من بابه المودَع: مولَّدٌ من `slge.wazn.AWZAN` "
        "بـ`tools/deposit_wujud.py`؛",
        "لا يُحرَّر باليد. الأصنافُ ستّة: فعل، مصدر، وصفٌ مشتقّ، اسمٌ مشتقٌّ غيرُ وصفٍ (زمانٌ ومكانٌ "
        "وآلة)، صيغةُ جمع،",
        "اسمٌ (مصدرٌ أو جامد لا تفصله الخانة). -/", "",
        "namespace Slge.Wujud", "",
        "inductive Ont where", "  | fil | masdar | wasf | zarfAla | jam | ism",
        "  deriving DecidableEq, Repr", "",
        f"/-- {len(ont)} قالبًا بترتيب `Wazn.awzan`. -/",
        "def table : List Ont := [",
    ]
    for i in range(0, len(ont), 10):
        chunk = ", ".join(f".{LEAN_NAME[x]}" for x in ont[i:i + 10])
        lines.append("  " + chunk + ("," if i + 10 < len(ont) else ""))
    lines += ["]", "", f"theorem table_length : table.length = {len(ont)} := by rfl", "",
              "end Slge.Wujud", ""]
    return "\n".join(lines)


def render_py(ont: list[str]) -> str:
    lines = [
        '"""الجهةُ الوجوديّة لكلّ قالبٍ — مولَّدٌ من `slge.wazn.AWZAN` '
        'بـ`tools/deposit_wujud.py`؛ لا يُحرَّر باليد."""',
        "", "from __future__ import annotations", "", "from typing import Final", "",
        "ONT: Final[tuple[str, ...]] = (",
    ]
    for i in range(0, len(ont), 8):
        lines.append("    " + ", ".join(f'"{x}"' for x in ont[i:i + 8]) + ",")
    lines += [")", ""]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    ont = table()
    lean, py = render_lean(ont), render_py(ont)
    if "--check" in argv:
        ok = LEAN.read_text(encoding="utf-8") == lean and PY.read_text(encoding="utf-8") == py
        sys.stdout.write("جدولا الوجود مطابقان للأبواب\n" if ok else "جدولا الوجود غيرُ مطابقين\n")
        return 0 if ok else 1
    LEAN.write_text(lean, encoding="utf-8")
    PY.write_text(py, encoding="utf-8")
    counts = {k: ont.count(k) for k in (FIL, MASDAR, WASF, ZARF, JAM, ISM)}
    sys.stdout.write(f"{len(ont)} قالبًا: {counts}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
