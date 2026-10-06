"""ولّد `MARIFA_INDEX.md`: فهرسُ المعارف على درجات الترخيص التدريجيّ من `slge.marifa`، وقياسُ قانون
التنوين (لا يجامع الأداةَ ولا الإضافة) على شريحة MASAQ المجمَّدة؛ ‎--check‎ يفشل إن كان قديمًا."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from slge.cells import Cell, index
from slge.marifa import MAWSUL

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "MARIFA_INDEX.md"
SLICE = ROOT / "tests" / "data" / "masaq-marifa.json"
IWAD = ("يَوْمَئِذٍ", "يَوْمِئِذٍ", "فَيَوْمَئِذٍ", "كُلٍّ")


def measure() -> tuple[Counter[tuple[str, bool]], int]:
    rows = json.loads(SLICE.read_text(encoding="utf-8"))
    out: Counter[tuple[str, bool]] = Counter()
    for row in rows:
        if row["det"]:
            cat = "معرَّف بأل"
        elif row["pron_suffix"]:
            cat = "مضاف إلى ضمير"
        elif row["mudaf"] == "مضاف":
            cat = "مضاف"
        elif row["tag"].startswith("NOUN_PROP"):
            cat = "علم"
        else:
            cat = "غير ذلك (نكرةٌ غالبًا)"
        out[(cat, row["tanwin"])] += 1
    return out, len(rows)


def k(w: tuple[Cell, ...]) -> str:
    return "-".join(str(index(c)) for c in w)


def render() -> str:
    table, total = measure()

    def n(cat: str, tanwin: bool) -> int:
        return table[(cat, tanwin)]

    lines = [
        "# فهرسُ المعارف على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_marifa_index.py` من `src/slge/marifa.py`؛ لا يُحرَّر باليد. "
        "البرهانُ: `formal/Slge/Marifa.lean`.",
        "",
        "السبعةُ في الحصر ثلاثةُ أصنافٍ على الخانات: **بالذات** (جداولُ صور)، **بالأداة** (عمليّةُ أل "
        "والإدغامُ الشمسيّ)، **بالتبعية** (إسقاطُ التنوين والإلحاق). والقوّةُ (الضمير فالعلم…) ترتيبٌ "
        "**معلن**؛ والعلمُ معجمٌ لا خانة؛ والمستترُ بلا خانة.",
        "",
        "## د٤ الخانة — بالذات: جداولُ صور", "",
        "| الصنف | المصدر | المبرهَن |", "|---|---|---|",
        "| الضمائر | `damair` (24 منفصلًا، 9 متّصلة) | `Damair.*` |",
        "| أسماء الإشارة | `ishara` (25 صورة) | `Ishara.*` |",
        f"| الأسماء الموصولة | `marifa.MAWSUL` ({len(MAWSUL)} صورة) | `mawsul_licensed`، "
        "`mawsul_nodup`، `mawsul_al`، `mawsul_dual_case` |",
        "| العلم | معجمٌ — لا خانةَ تقرؤه | — |",
        "",
        "| الموصول | الخانات |", "|---|---|",
        *[f"| {name} | `{k(w)}` |" for name, w in MAWSUL.items()],
        "",
        "## د٨ الحدّ — بالأداة: أل والإدغامُ الشمسيّ", "",
        "`al`: همزةٌ مفتوحة (ألفُ الوصل بقيّةُ رسم) فلامٌ ساكنة؛ ثمّ `shamsi`: اللامُ قبل الشمسيّ تصير "
        "الحرفَ نفسَه ساكنًا (الرَّحْمَنِ = ءَ رْ رَ…). المبرهَن: الإدغامُ لا يغيّر نمطَ السكون فيحفظ الترخيص "
        "(`shamsi_licensed`)، والتعريفُ يحفظ الترخيص (`al_licensed`)، والأداةُ تُقرأ من الصدر "
        "(`hasAl_al`).",
        "",
        "## د٨ الحدّ — بالتبعية: الإضافة", "",
        "`idafa`: إسقاطُ التنوين (يحفظ الترخيص: `dropTanwin_licensed`) ثمّ الإلحاقُ بالمضاف إليه؛ "
        "المضافُ إلى ضميرٍ لا تنوينَ له (`idafa_no_tanwin`). والمنادى المقصودُ: ضمٌّ بلا تنوين "
        "(`Nida.damm_is_bina`).",
        "",
        "## القانون المقيس — التنوينُ لا يجامع الأداةَ ولا الإضافة", "",
        f"على {total} صورةً اسميّة متباينة من MASAQ بشهادات البوّابة:", "",
        "| الصنف (وسم MASAQ) | بلا تنوين | بتنوين |", "|---|---|---|",
        *[f"| {cat} | {n(cat, False)} | {n(cat, True)} |"
          for cat in ("معرَّف بأل", "مضاف", "مضاف إلى ضمير", "علم", "غير ذلك (نكرةٌ غالبًا)")],
        "",
        f"- أل مع تنوين: **{n('معرَّف بأل', True)}** (هَاوِيَةٌ: وسمُ DET خاطئ — لا أل فيها).",
        f"- مضافٌ مع تنوين: **{n('مضاف', True) + n('مضاف إلى ضمير', True)}** — منها **تنوينُ العوض** "
        f"({'، '.join(IWAD)}) وهو الاستثناءُ المسمّى في النحو، والباقي (غَفُورٌ رَحِيمٌ…) خلافُ وسم.",
        f"- العلم: **{n('علم', True)}/{n('علم', True) + n('علم', False)}** منوَّن (المنصرف) — "
        "فالتنوينُ ليس علامةَ تنكير، والعلمُ لا يُقرأ من الخانة.",
        "",
        "## ما لا تقرؤه الخانة — باسمه", "",
        "- العلمُ والنكرة: المعجم.",
        "- النكرةُ المقصودة بالنداء: ضمٌّ بلا تنوين كالعلم المنادى؛ الفصلُ من المعجم.",
        "- مَنْ: نونُها أصلٌ ساكنٌ بعد فتحٍ فتقرؤها الخانةُ كتنوين (`man_looks_like_tanwin`).",
        "- المضافُ إلى اسمٍ تالٍ: تيارُ شهادتين؛ يُقاس في النظم.", "",
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    text = render()
    if "--check" in argv:
        if not TARGET.exists() or TARGET.read_text(encoding="utf-8") != text:
            print("MARIFA_INDEX.md قديم: شغّل python tools/gen_marifa_index.py", file=sys.stderr)
            return 1
        print("MARIFA_INDEX.md مطابق")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    print(f"كُتب {TARGET.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
