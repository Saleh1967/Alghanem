"""ولّد `JAZM_INDEX.md`: فهرسُ أدوات الجزم والشرط على درجات الترخيص التدريجيّ من `slge.jazm`، وقياسُ
العلامات الثلاث على شريحة MASAQ المجمَّدة (المضارعُ المجزوم بشهادات البوّابة)؛ ‎--check‎."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from slge.cells import index
from slge.jazm import GATE, JAZIM_ONE, SHART_GHAYR, SHART_JAZIM, marker
from slge.rawabit import cells_of

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "JAZM_INDEX.md"
SLICE = ROOT / "tests" / "data" / "masaq-jazm.json"

EXPECT = {"السكون": "سكون", "حذف النون": "حذف النون", "حذف حرف العلة": "لا تقرؤه الخانة"}


def measure() -> tuple[Counter[tuple[str, str]], Counter[str], Counter[tuple[str, str]], int]:
    """علامةُ MASAQ مقابلَ قارئ الخانة؛ والأداةُ السابقة؛ والمعتلُّ المحذوفُ الآخر: حركتُه الباقية."""

    rows = json.loads(SLICE.read_text(encoding="utf-8"))
    table: Counter[tuple[str, str]] = Counter()
    tools: Counter[str] = Counter()
    weak: Counter[tuple[str, str]] = Counter()
    for row in rows:
        stem = tuple((c[0], c[1]) for c in row["stem"])
        read = marker(stem)
        table[(row["marker"], read)] += 1
        tools[row["tool"][0] if row["tool"] else "—"] += 1
        if row["marker"] in ("حذف حرف العلة", "السكون") and read == "لا تقرؤه الخانة" and stem:
            weak[(row["marker"], stem[-1][1])] += 1
    return table, tools, weak, len(rows)


def _cells(w: str) -> str:
    return "-".join(str(index(c)) for c in cells_of(w))


def _deposit(name: str, words: tuple[str, ...]) -> str:
    return f"- **{name}** ({len(words)}): " + ", ".join(
        f"{w}{'' if w in GATE else '°'} `{_cells(w)}`" for w in words)


def render() -> str:
    table, tools, weak, total = measure()
    lines = [
        "# فهرسُ أدوات الجزم والشرط على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_jazm_index.py` من `src/slge/jazm.py`؛ لا يُحرَّر باليد. "
        "البرهانُ: `formal/Slge/Jazm.lean`. الشاهدُ بلا علامةٍ بشهادة البوّابة (في المصحف)؛ و° مودَعٌ "
        "على طريقتها.",
        "",
        "## د٤ الخانة — العلاماتُ الثلاث عمليّاتٌ ثلاث", "",
        "| العلامة | العمليّة | المبرهَن |", "|---|---|---|",
        "| السكون الظاهر | `sukun`: سكونُ الآخر | مرخَّصٌ بعد متحرّك (`sukun_licensed`)؛ **غيرُ مرخَّصٍ "
        "بعد مدّ** (`hollow_forced`): حذفُ عين الأجوف يَقُولُ ← يَقُلْ ملزَمٌ (`yaqulu_sukun_unlicensed`، "
        "`yaqul_licensed`) |",
        "| حذف حرف العلّة | `dropWeak`: إسقاطُ المدّ الأخير | يحفظ الترخيص (`dropWeak_licensed`)؛ "
        "يترك حركةَ الأصل في الآخر (`dropWeak_last`) — فلا يُقرأ الجزمُ من الخانة بعده |",
        "| حذف النون | `Afal.form _ _ _ .jazm` | صورةُ الجزم = صورةُ النصب (`afal_jazm_eq_nasb`): "
        "الأداةُ تفصل |",
        "",
        "واوُ الجماعة المجزومة وواوُ المعتلّ المرفوع خانةٌ واحدة (يَدْعُوا = يَدْعُو: `waw_shared`) — "
        "الألفُ الفارقةُ بقيّةُ رسمٍ في شهادة البوّابة تفصلهما.",
        "",
        "## د٨ الحدّ — الأداةُ تُعدّ ولا تُقرأ", "",
        "الأدواتُ مرخَّصةٌ كلُّها (`tools_licensed`؛ `counts` 4 + 12 + 7):", "",
        _deposit("تجزم فعلًا واحدًا", JAZIM_ONE),
        _deposit("أدواتُ الشرط الجازمة", SHART_JAZIM),
        _deposit("أدواتُ الشرط غيرُ الجازمة", SHART_GHAYR),
        "",
        "- لامُ الأمر حرفٌ متّصلٌ مكسورٌ لا يُفسد ما بعده (`amr_licensed`؛ لِيُنْفِقْ `yunfiq_witness`).",
        "- **الخانةُ الواحدةُ باسمها**: لَا الناهيةُ = لَا النافية، ولَمَّا الجازمةُ = لَمَّا الحينيّة "
        "(`shared_la_lamma`)؛ وسبعةٌ من أسماء الشرط = الاستفهام: مَنْ مَا مَتَى أَيَّانَ أَيْنَ أَنَّى أَيّ "
        "(`shared_istifham`) — الحكمُ من الفعل بعدها لا من الأداة.",
        "- أَيّ وحدَها معربة: ثلاثُ صورٍ بثلاث حركات (`ayy_declines`).",
        "- جدولُ أدوات الربط يسجّل الجوازمَ كلَّها بعملها (لَمْ لَمَّا والاثنتي عشرة) وغيرَ الجازمة السبعَ "
        "بلا عمل (`rawabit_jazm`) — دَينٌ سُدِّد.",
        "",
        "## د١٦ الإعراب من الخانة — القارئ `marker`", "",
        "النونُ أوّلًا (الصورةُ الخمسيّة: `marker_afal_jazm`)، ثمّ السكون؛ وما سواهما لا يُقرأ "
        "(`marker_witnesses`: يَلِدْ ويَعْمَلْ سكون، تُبْطِلُوا وتَكُونُوا حذفُ نون، يَدْعُ ويَسْعَ ويُجْزَ لا "
        "تقرؤه الخانة). والجزمُ بفعلين حكمُ كلٍّ منهما حكمُ الواحد (`two_verbs`).",
        "",
        "## القياس على MASAQ — المضارعُ المجزوم", "",
        f"على {total} مضارعًا مجزومًا بشهادات البوّابة (الجذعُ بعد السابقة وقبل ضمير النصب؛ "
        "المؤكَّدُ بالنون مستبعَد):", "",
        "| علامةُ MASAQ | قراءةُ الخانة | العدد |", "|---|---|---|",
        *[f"| {m} | {r} | {v} |" for (m, r), v in sorted(table.items(), key=lambda kv: -kv[1])],
        "",
        "حذفُ حرف العلّة **لا تقرؤه الخانة** بعد الحذف — كما برهن `dropWeak_last`: الآخرُ يحمل حركةَ "
        "الأصل: " + "، ".join(f"{st} {v}" for (m, st), v in weak.most_common() if m != "السكون")
        + ". والسكونُ الذي لا تقرؤه الخانة: "
        + "، ".join(f"{st} {v}" for (m, st), v in weak.most_common() if m == "السكون")
        + " — الكسرُ كسرةُ التقاء الساكنين في الوصل (يُضْلِلِ اللَّهُ): سكونٌ حرّكه الحدُّ، قانونُ "
        "`Context` في الغانم لا تخمينٌ هنا؛ والضمُّ يَكُ/تَكُ بحذف نون يَكُنْ تخفيفًا: معجم.",
        "",
        "### الأداةُ السابقةُ للمجزوم (أقربُ أداةٍ في الآية)", "",
        "| الأداة | العدد |", "|---|---|",
        *[f"| {t} | {v} |" for t, v in tools.most_common(12)],
        "",
        "## ما لا تقرؤه الخانة — باسمه", "",
        "- المعتلُّ المحذوفُ الآخر: يُقرأ بالمقارنة بالأصل لا من الصورة.",
        "- لَا الناهيةُ من النافية، ولَمَّا الجازمةُ من الحينيّة، وأسماءُ الشرط من الاستفهام: التيار.",
        "- الجزمُ بفعلين (شرطٌ وجواب)، والفاءُ الرابطةُ بحالاتها السبع، والامتناعُ (لَوْ، لَوْلَا): تيار.",
        "- نونُ التوكيد بعد المجزوم (الفتحة): خارج هذا القياس باسمها.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("JAZM_INDEX.md غيرُ مطابق؛ شغّل python tools/gen_jazm_index.py\n")
            return 1
        sys.stdout.write("JAZM_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب JAZM_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
