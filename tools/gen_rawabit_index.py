"""ولّد `RAWABIT_INDEX.md`: فهرسةُ أدوات الربط على درجات الترخيص الجبريّ التدريجيّ، من
`slge.rawabit` لا من اليد؛ و‎--check‎ يفشل إن كان الملفُّ قديمًا."""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

from slge.cells import index
from slge.rawabit import BABS, COMPOUND, PARTICLES, tier

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "RAWABIT_INDEX.md"
TIERS = ("د١٦ العمل", "د٨ الحدّ", "د٤ الخانة")
WHAT = {
    "د١٦ العمل": "خاناتُها مرخَّصة، وأثرُها في آخر ما بعدها دالّةٌ مفحوصة (`govern`)؛ "
                "على الأفعال الخمسة مبرهَن (`govern_jazm_afal`).",
    "د٨ الحدّ": "حرفٌ واحدٌ متحرّك يتّصل بما بعده ولا يُفسد ترخيصَه (`proclitic_keeps_licence`).",
    "د٤ الخانة": "خاناتُها مرخَّصة (`particles_licensed`)؛ ما فوق ذلك معنًى معلَن.",
}


def render() -> str:
    wit = Counter(p.witness for p in PARTICLES)
    lines = [
        "# فهرسةُ أدوات الربط على درجات الترخيص الجبريّ التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_rawabit_index.py` من `src/slge/rawabit.py`؛ لا يُحرَّر باليد. "
        "البرهانُ: `formal/Slge/Rawabit.lean`.",
        "",
        f"**{len(PARTICLES)} أداةً مفردة** — {wit['شهادة']} خاناتُها من شهادات البوّابة، "
        f"{wit['بالقانون']} بالقانون نفسِه (خارج مجال المدوّنة). والمعنى (البابُ من الجدول المُرسَل) "
        "**معلَن** في كلّ درجة: البرهانُ لا يبلغه.",
        "",
    ]
    for t in TIERS:
        ps = [p for p in PARTICLES if tier(p) == t]
        lines += [f"## {t} — {len(ps)} أداة", "", WHAT[t], "",
                  "| الأداة | الخانات (رموز SLGE) | العمل | الباب (معلن) | الشاهد |",
                  "|---|---|---|---|---|"]
        for p in sorted(ps, key=lambda p: (p.bab, p.name)):
            key = "-".join(str(index(c)) for c in p.cells)
            lines.append(f"| {p.name} | `{key}` | {p.amal or '—'} | {p.bab} {BABS[p.bab]} | "
                         f"{p.witness} |")
        lines.append("")
    lines += ["## خارج الفهرسة — تراكيبُ لا أدوات", "",
              "تياراتُ شهاداتٍ (كلمتان فأكثر، أو لفظٌ غيرُ مشكولٍ في الجدول): لا تُودَع خانات، "
              "ولا تُرخَّص أداةً؛ تدخل كلمةً كلمةً من البوّابة ويُقاس تركيبُها في النظم.", "",
              "| الباب | التراكيب |", "|---|---|"]
    for b in sorted(COMPOUND):
        lines.append(f"| {b} {BABS[b]} | {'، '.join(COMPOUND[b])} |")
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    text = render()
    if "--check" in argv:
        if not TARGET.exists() or TARGET.read_text(encoding="utf-8") != text:
            print("RAWABIT_INDEX.md قديم: شغّل python tools/gen_rawabit_index.py", file=sys.stderr)
            return 1
        print("RAWABIT_INDEX.md مطابق")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    print(f"كُتب {TARGET.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
