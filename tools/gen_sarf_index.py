"""ولّد `SARF_INDEX.md`: فهرسُ الممنوع من الصرف على درجات الترخيص التدريجيّ من `slge.sarf`، وقياسُ
القانون الحاسم وشرطي الصرف على شريحة MASAQ المجمَّدة (أسماءٌ بعد جارٍّ بشهادات البوّابة)؛ ‎--check‎."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from slge.cells import STATES
from slge.sarf import illa

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "SARF_INDEX.md"
SLICE = ROOT / "tests" / "data" / "masaq-sarf.json"
_A, _I, _U, SUKUN = STATES


def measure() -> tuple[Counter[tuple[str, str]], Counter[str], list[str], int]:
    """(الصنفُ، الحالةُ الأخيرة) → العدد؛ وعللُ المفتوحِ المجرّد؛ وأمثلتُه."""

    rows = json.loads(SLICE.read_text(encoding="utf-8"))
    out: Counter[tuple[str, str]] = Counter()
    ilal: Counter[str] = Counter()
    examples: list[str] = []
    for row in rows:
        cells = tuple((c[0], c[1]) for c in row["cells"])
        if not cells:
            continue
        st = ("تنوين " if row["tanwin"] else "") + (cells[-2][1] if row["tanwin"] else cells[-1][1])
        cat = "بأل" if row["det"] else ("مضاف" if row["mudaf"] else "مجرّد")
        out[(cat, st)] += 1
        if cat == "مجرّد" and st == "فتح":
            ilal[illa(cells)] += 1
            if len(examples) < 12:
                examples.append(row["word"])
    return out, ilal, examples, len(rows)


def render() -> str:
    table, ilal, examples, total = measure()
    mamnu = table[("مجرّد", "فتح")]
    lines = [
        "# فهرسُ الممنوع من الصرف على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_sarf_index.py` من `src/slge/sarf.py`؛ لا يُحرَّر باليد. "
        "البرهانُ: `formal/Slge/Sarf.lean`.",
        "",
        "## د١٦ الإعراب من الخانة — القانونُ الحاسم", "",
        "الممنوعُ لا تنوينَ له وجرُّه بالفتحة: فصورةُ جرّه **هي صورةُ نصبه بعينها** (`jarr_eq_nasb`)، "
        "بخلاف المنصرف الذي يفرّق الكسرُ والتنوينُ جرَّه من نصبه (`sarf_jarr_ne_nasb`). وشرطا الصرف "
        "عمليّتان على الخانات: أل (`al_jarr_kasra`) والإضافةُ (`idafa_jarr_kasra`) تردّان الكسرة.", "",
        "## د٨ الحدّ — عللُ الصيغة (تقرؤها الخانة)", "",
        "| العلّة | القارئ | المبرهَن |", "|---|---|---|",
        "| صيغة منتهى الجموع | على قالبٍ من 12 قالبًا في `wazn` | `onTemplate_fill` (سليمٌ لكلّ أصل)، "
        "`muntaha_wf` |",
        "| ألف التأنيث المقصورة | ألفٌ ساكنةٌ بعد فتحٍ رابعةً فأكثر | `maqsura` |",
        "| ألف التأنيث الممدودة | همزةٌ بعد ألفٍ ساكنةٍ بعد فتح | `mamduda` |",
        "| وزن أَفْعَل / فَعْلَان / فَعْلَاء / فُعْلَى | قوالبُ `wazn` | `illa` |",
        "",
        "الشواهد (`witnesses_illa`): مَسَاجِدَ، مَصَابِيحَ ← منتهى الجموع؛ شُفَعَاءَ ← ممدودة؛ كُبْرَى ← مقصورة؛ "
        "أَحْمَرَ، عَطْشَانَ، **آدَمَ** ← وزن أَفْعَل (العلميّةُ ووزنُ الفعل تقرؤها الخانة)؛ إِبْرَاهِيمَ ← معجم.", "",
        "## د٤ — عللُ المعجم (لا تقرؤها الخانة)", "",
        "العلميّةُ مع التأنيث أو العجمة أو التركيب أو الألف والنون أو العدل (عُمَر): معجمٌ، معلَن. "
        "والهمزةُ الأصليّةُ في الممدود (أَبْنَاء، أَسْمَاء) لا تفرّقها الخانة عن الزائدة: دَينٌ مسمًّى.", "",
        "## القياس على MASAQ — بعد الجارّ", "",
        f"على {total} اسمًا بعد جارٍّ (بشهادات البوّابة، بلا ضميرٍ لاحق):", "",
        "| الصنف | الحالةُ الأخيرة | العدد |", "|---|---|---|",
        *[f"| {a} | {b} | {v} |" for (a, b), v in table.most_common()],
        "",
        f"- **بأل ⇒ كسر** {table[('بأل', 'كسر')]} (والسكونُ مقصورٌ: الدُّنْيَا؛ والفتحُ الواحد "
        "بِالْبَنِينَ جمعٌ بالياء).",
        f"- **مضاف ⇒ كسر** {table[('مضاف', 'كسر')]} (والسكونُ مقصورٌ أو جمعٌ بالياء).",
        f"- **المجرّد**: منوَّنُ كسرٍ {table[('مجرّد', 'تنوين كسر')]} (منصرف) أو مفتوحٌ بلا تنوين "
        f"**{mamnu}** (الممنوع)؛ وتنوينُ الضمّ {table[('مجرّد', 'تنوين ضم')]} لامُ ابتداءٍ موسومةٌ جارًّا.",
        "",
        f"عللُ المفتوحِ المجرّد ({mamnu}) كما تقرؤها الخانة:", "",
        "| العلّة | العدد |", "|---|---|",
        *[f"| {k} | {v} |" for k, v in ilal.most_common()],
        "",
        f"أمثلة: {'، '.join(examples)}.", "",
        "## خارج الخانة — باسمه", "",
        "- المقصورُ (مُوسَى، الدُّنْيَا): جرُّه مقدَّرٌ، لا تقرأ الخانةُ حالتَه.",
        "- صُنْ شَمْلَهُ (نوح، لوط، هود…): منصرفةٌ بثلاثيّتها — معجم.", "",
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    text = render()
    if "--check" in argv:
        if not TARGET.exists() or TARGET.read_text(encoding="utf-8") != text:
            print("SARF_INDEX.md قديم: شغّل python tools/gen_sarf_index.py", file=sys.stderr)
            return 1
        print("SARF_INDEX.md مطابق")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    print(f"كُتب {TARGET.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
