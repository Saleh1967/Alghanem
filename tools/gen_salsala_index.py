"""فهرسُ السلسلة (SALSALA_INDEX.md): أركانُ المدلول الكونيّ على سلالم النبهانيّ الثلاثة، ركنًا ركنًا
بسطره وعبارته من المختومَين — أو معلَنًا باسمه بقرار المالك — ومرتبتِه وسوالفِه (منصوصةً أو رأيًا). كلُّ
صفٍّ هنا بندٌ من ADR ٣١. مولَّدٌ من `salsala_table` (المولَّدِ من المودَع بـ`--check`)؛ بـ`--check` يقارن
الفهرسَ بما يولَّد الآن.
"""

from __future__ import annotations

import sys
from pathlib import Path

from slge.salsala import DECLARED, GRADES, LADDERS, ROWS, salaf

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "SALSALA_INDEX.md"


def render() -> str:
    out = [
        "# فهرسُ السلسلة — أركانُ المدلول الكونيّ على سلالم النبهانيّ الثلاثة (ADR ٣١)", "",
        "مولَّدٌ بـ`python tools/gen_salsala_index.py` من `salsala_table` (المولَّدِ من ج3 و«التفكير» "
        "المختومَين بـ`tools/deposit_salsala.py --check`)؛ لا يُحرَّر باليد. المرتبةُ: **يقين** للوجود "
        "وحقائقه، **ظنّ** للكنه والصفات (التفكير 65، 123)، **—** لما ليس حكمًا على واقع. السالفُ "
        "**منصوص** إن كان له سطر، وإلّا **رأي** من جدول المالك. الركنُ بلا مرساةٍ **معلَنٌ بقرار "
        "المالك** (2026-10-10) لا من الذاكرة.", "",
        f"الأركانُ {len(ROWS)}: {sum(1 for r in ROWS if r[1] == 0)} في المعلومات السابقة، "
        f"{sum(1 for r in ROWS if r[1] == 1)} في الوضع والنسب، "
        f"{sum(1 for r in ROWS if r[1] == 2)} في الحكم؛ "
        f"المرسى {sum(1 for r in ROWS if r[4])}، المعلَن {len(DECLARED)}.", "",
    ]
    for li, lname in enumerate(LADDERS):
        out += [f"## {'أبج'[li]}. {lname}", "",
                "| # | الركن | المرتبة | السطر والعبارة من المودَع | السوالف | ملاحظة |",
                "|---|---|---|---|---|---|"]
        for rid, lad, name, gr, anchors, _, note in ROWS:
            if lad != li:
                continue
            an = "؛ ".join(f"{src} {line}: «{ph}»" for src, line, ph in anchors) or "— (معلَن)"
            sa = "، ".join(f"{s}{'' if ok else '؟'}" for s, ok in salaf(rid)) or "—"
            out.append(f"| {rid} | {name} | {GRADES[gr]} | {an} | {sa} | {note} |")
        out.append("")
    out += ["**العلامة «؟» بعد السالف:** رأيٌ من جدول المالك لا سطرَ له. **ما بقي باسمه:** الأركانُ "
            "المعلَنة الثلاثة (القابليّات، المكان، العدد) تحتاج سطرًا من مودَعٍ مختوم أو تبقى معلَنة؛ "
            "ومرجعُ الأحكام المحجوب (المادّة ١٢) لم يُؤذن به بعد فلا «مقيس» هنا.", ""]
    return "\n".join(out)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("SALSALA_INDEX.md غيرُ مطابق؛ شغّل tools/gen_salsala_index.py\n")
            return 1
        sys.stdout.write("SALSALA_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب SALSALA_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
