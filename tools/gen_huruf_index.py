"""ولّد `HURUF_INDEX.md`: فهرسُ الحروف والأدوات على درجات الترخيص التدريجيّ من `slge.huruf`، وقياسُ
أدوارها وأثرِها على ما بعدها في MASAQ (عدُّ أوصافٍ مجمَّد؛ صورُ الحروف بشهادات البوّابة)؛ ‎--check‎."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from slge.cells import index
from slge.huruf import FIL, ISM, MUSHTARAK, TABLE, shared

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "HURUF_INDEX.md"
SLICE = ROOT / "tests" / "data" / "masaq-huruf.json"


def measure() -> dict[str, object]:
    data = json.loads(SLICE.read_text(encoding="utf-8"))
    roles: dict[str, Counter[str]] = {}
    for seg, role, v in data["roles"]:
        roles.setdefault(seg, Counter())[role] += v
    after: dict[str, Counter[str]] = {}
    for seg, a, v in data["after"]:
        after.setdefault(seg, Counter())[a] += v
    return {"roles": roles, "after": after}


def _cells(w: tuple[tuple[str, str], ...]) -> str:
    return "-".join(str(index(c)) for c in w)


def _group(name: str, items: tuple[object, ...]) -> list[str]:
    lines = [f"### {name} ({len(items)})", "", "| الحرف | الخانات | العمل |", "|---|---|---|"]
    for x in items:
        lines.append(f"| {x.name} | `{_cells(x.cells)}` | {x.amal or '—'} |")  # type: ignore[attr-defined]
    return [*lines, ""]


def render() -> str:
    m = measure()
    roles: dict[str, Counter[str]] = m["roles"]  # type: ignore[assignment]
    after: dict[str, Counter[str]] = m["after"]  # type: ignore[assignment]
    sh = shared()
    lines = [
        "# فهرسُ الحروف والأدوات على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_huruf_index.py` من `src/slge/huruf.py`؛ لا يُحرَّر باليد. البرهانُ: "
        "`formal/Slge/Huruf.lean`، والعملُ مبرهَنٌ في أبوابه (`Majrurat`، `Nawasikh`، `Nida`، "
        "`Rawabit`، `Jazm`، `Tawabi`).",
        "",
        "## د٤ الخانة — الحرفُ صورةٌ مودَعة", "",
        f"{len(TABLE)} مدخلًا على {len({x.cells for x in TABLE})} صورةً مختلفة، كلُّها مرخَّصة "
        "(`table_licensed`)، ولا تنوينَ فيها (`no_tanwin`؛ وما نونُه أصلٌ ساكنٌ بعد حركةٍ تقرؤه الخانةُ "
        "كالتنوين: مِنْ عَنْ أَنْ لَنْ إِذَنْ إِنْ لَكِنْ — تشابهٌ مسمًّى). المتّصلةُ (خانةٌ واحدةٌ متحرّكة: بِ لِ كَ "
        "وَ تَ فَ سَ أَ) لا تُفسد ما بعدها (`proclitics_keep_licence`).",
        "",
        *_group("المختصّةُ بالأسماء", ISM),
        *_group("المختصّةُ بالأفعال", FIL),
        *_group("المشتركة", MUSHTARAK),
        "## د٨ الحدّ — الخانةُ الواحدةُ في أكثرَ من باب", "",
        "الحصرُ يرتّب الحروفَ بعملها؛ والخانةُ ترتّبها بصورتها — والصورةُ الواحدةُ تقع في أبوابٍ عدّة "
        "(`shared_cells`): العملُ من التيار لا من الخانة.", "",
        "| الخانات | المداخل |", "|---|---|",
        *[f"| `{_cells(k)}` | {'، '.join(v)} |"
          for k, v in sorted(sh.items(), key=lambda kv: -len(kv[1]))],
        "",
        "## د١٦ — العملُ عمليّةٌ على ما بعده", "",
        "`amal_is_operation`: الجرُّ `Majrurat.jarr` يحكم عليه الجدول (`govern_jarr`)؛ نصبُ الاسم "
        "ورفعُ الخبر = `Nawasikh.inna`؛ نصبُ المضارع (`govern_nasb_afal`) وجزمُه "
        "(`govern_jazm_afal`)؛ والعطفُ تبعيّةٌ (`Tawabi.follows`). وجدولُ أدوات الربط يشهد لما فيه "
        "(`rawabit_agrees`). التنفيسُ بلا أثرٍ على الآخر: سَيَقُولُ بشهادة البوّابة (`sawfa_witness`).",
        "",
        "## القياس على MASAQ", "",
        "### الصورةُ الواحدةُ وأدوارُها (عدُّ MASAQ)", "",
        "| الحرف | الأدوار |", "|---|---|",
        *[f"| {seg} | " + "، ".join(f"{r} {v}" for r, v in roles[seg].most_common(5)) + " |"
          for seg in ("لا", "ما", "إن", "أن", "لم", "ل", "و", "ف", "أما", "قد", "هل")
          if seg in roles],
        "",
        "### ما بعد النواصب والجوازم", "",
        "| الحرف | ما بعده |", "|---|---|",
        *[f"| {seg} | " + "، ".join(f"{a} {v}" for a, v in after[seg].most_common(4)) + " |"
          for seg in ("لن", "كي", "أن", "حتى", "لم", "لا", "إذن") if seg in after],
        "",
        "لَنْ وكَيْ تنصب المضارعَ بعدها كلَّه؛ وأَنْ تنصبه حين تدخل على الفعل وتنصب الاسمَ حين تكون أَنَّ "
        "(الشدّةُ بقيّةُ رسم: الخانةُ تقرؤها نونين)؛ وحَتَّى على الفعل ناصبةٌ وعلى الاسم جارّة — الخانةُ "
        "الواحدةُ وعملان، كما في الحصر.",
        "",
        "## ما لا تقرؤه الخانة — باسمه", "",
        "- قانونُ الفرز (حرفٌ محض/أداة) والمعاني (الردع، التحقيق، الاستفتاح): معلَن.",
        "- أَنْ المضمرةُ بعد لام كي وحتّى وفاء السببيّة وواو المعيّة: تيار.",
        "- إِذَنْ في المصحف اسمٌ مجرور (إِذْنٍ) لا الناصبة: الخانةُ واحدة — المعجم.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("HURUF_INDEX.md غيرُ مطابق؛ شغّل tools/gen_huruf_index.py\n")
            return 1
        sys.stdout.write("HURUF_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب HURUF_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
