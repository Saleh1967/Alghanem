"""فهرسُ الكليّ والجزئيّ على درجات الترخيص التدريجيّ (KULLI_INDEX.md) من `slge.kulli` وشريحة MASAQ.

القياسُ على `masaq-shibh.json.gz` بشهادات البوّابة: وسمُ MASAQ للصنف مرجعٌ محجوب —
PRON/DEM_PRON/REL_PRON جزئيّ؛ NOUN_ACTIVE_PART/NOUN_PASSIVE_PART/ADJ_QUALIT/ADJ_COMP كليٌّ عرضيّ؛
GERUND حدثٌ مجرّد؛ IV/PV/CV (ومبنيُّها للمجهول) حدثٌ مهيّأ؛ NOUN_CONCRETE/NOUN_ABSTRACT كليٌّ ماهويّ؛
NOUN_PROP جزئيٌّ بالمعجم (لا يُقرأ من الخانة — يُعدّ على حدة). الكلمةُ: السوابقُ (أل، صدرُ المضارع)
والجذعُ بلا لواحق.
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from slge.kulli import kulli
from slge.wazn import AWZAN, mizan

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "KULLI_INDEX.md"
DATA = ROOT / "tests" / "data"
Word = tuple[tuple[str, str], ...]
PRE_TAGS = ("DET", "IMPERF_PREF", "CV_PREF", "IV1S", "IV1P", "IV2MP", "IV3MS", "IV3MP", "IV3FS")
SUBJ_TAGS = ("SUBJ_PRON", "PVSUFF_SUBJ", "IVSUFF_SUBJ", "CVSUFF_SUBJ", "OBJ_PRON", "PVSUFF_DO",
             "IVSUFF_DO", "POSS_PRON", "NSUFF", "EMPHATIC_NUN", "PROTECT_NUN")
TAG_KIND: dict[str, str] = {
    "PRON": "جزئيّ", "DEM_PRON": "جزئيّ", "REL_PRON": "جزئيّ",
    "NOUN_ACTIVE_PART": "كليّ عرضيّ", "NOUN_PASSIVE_PART": "كليّ عرضيّ", "ADJ_QUALIT": "كليّ عرضيّ",
    "ADJ_COMP": "كليّ عرضيّ", "GERUND": "حدث مجرّد",
    "IV": "حدث مهيّأ", "PV": "حدث مهيّأ", "CV": "حدث مهيّأ", "IV_PASS": "حدث مهيّأ",
    "PV_PASS": "حدث مهيّأ",
    "NOUN_CONCRETE": "كليّ ماهويّ", "NOUN_ABSTRACT": "كليّ ماهويّ", "NOUN_PROP": "علم (جزئيٌّ بالمعجم)",
}


def _cells(r: dict[str, Any]) -> Word:
    pre = [(a, b) for t, cs in r["pre"] for a, b in cs if t in PRE_TAGS]
    return (*pre, *((a, b) for a, b in r["stem"]))


def words() -> list[tuple[str, Word]]:
    """(صنفُ MASAQ، الخانات) للكلمات الموسومة بلا لواحق."""

    with gzip.open(DATA / "masaq-shibh.json.gz", "rt", encoding="utf-8") as f:
        rows: list[dict[str, Any]] = json.load(f)["rows"]
    out: list[tuple[str, Word]] = []
    for r in rows:
        kind = TAG_KIND.get(str(r["tag"]))
        if kind is None or any(t.startswith(SUBJ_TAGS) for t, _ in r["suf"]):
            continue
        if r["stem"]:
            out.append((kind, _cells(r)))
    return out


def measure() -> dict[str, object]:
    read: Counter[tuple[str, str]] = Counter()
    for kind, w in words():
        read[(kind, kulli(w))] += 1
    on_mizan: Counter[str] = Counter(kulli(mizan(AWZAN[k].template)) for k in range(len(AWZAN)))
    return {"read": read, "mizan": on_mizan, "n": sum(read.values())}


def render() -> str:
    m = measure()
    read: Counter[tuple[str, str]] = m["read"]  # type: ignore[assignment]
    on_mizan: Counter[str] = m["mizan"]  # type: ignore[assignment]
    kinds = ("جزئيّ", "كليّ عرضيّ", "حدث مجرّد", "حدث مهيّأ", "كليّ ماهويّ")
    agree = sum(v for (t, k), v in read.items() if t == k)
    total = sum(v for (t, _), v in read.items() if t in kinds)
    lines = [
        "# فهرسُ الكليّ والجزئيّ على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_kulli_index.py` من `src/slge/kulli.py`؛ لا يُحرَّر باليد. "
        "البرهانُ: "
        "`formal/Slge/Kulli.lean`.",
        "",
        "## د٤ الخانة — الكليُّ في الخارج وجودُه في أفراده", "",
        "القالبُ (الماهيةُ) لا يوجد في الخانات إلّا مملوءًا بجذر: ما على قالبٍ فهو `fill t r` "
        "لجذرٍ ما، وكلُّ "
        "ملءٍ على قالبه — لكلّ قالبٍ حسنِ التكوين ولكلّ كلمة (`universal_in_particulars`). "
        "المعجمُ المودَع "
        f"({len(AWZAN)} قالبًا) قوالبُ لا أفراد. والجزئيُّ (الضمائرُ والإشارةُ والموصول) من جدولٍ لا من "
        "قالب: ليس على قالبٍ من الـ121 إلّا أربعٌ تشابه قالبًا بالخانة (نَحْنُ وأَيُّ على فَعْلٌ، "
        "ذَلِكَ على "
        "فَعِلَ، ثَمَّتَ على فَعَّلَ — `particulars_off_templates`)، والقارئُ يقدّم الجدولَ على "
        "القالب فيقرأها "
        "كلَّها جزئيًّا (`juzi_by_table`). الكليُّ العرضيُّ (قوالبُ الوصف) والحدثُ (قوالبُ "
        "المصدر) لا يشتركان "
        "في قالب (`aradi_hadath_disjoint`).",
        "",
        "## د٨ الحدّ — المصدرُ مجرّدٌ من الزمن والفعلُ مهيّأٌ به", "",
        "لكلّ قالبِ مصدرٍ ولكلّ جذرٍ لا ألفَ فيه لا يُقرأ المصدرُ ماضيًا ولا مضارعًا ولا أمرًا "
        "(`masdar_no_sigha`؛ حالاتُه غيرُ حالات قوالب الفعل `masdar_states_disjoint`، والمصدرُ "
        "الميميّ "
        "صدرُه ميم، وفَعْلَةُ بشرط ألّا تكون فاؤها صدرَ مضارع — باسمها)، فلا تدخله أدواتُ الإزاحة "
        "(`masdar_not_shifted`)؛ والفعلُ مهيّأٌ بالزمن لكلّ قالبٍ (`Jiha.sigha_of_fill`).",
        "",
        "## القارئ", "",
        "`kulli` يقرأ الجهةَ الوجوديّة من الخانة: جزئيٌّ مجدوَل، كليٌّ عرضيّ (مشتقّ)، حدثٌ مهيّأ "
        "(فعل)، حدثٌ "
        "مجرّد (مصدر)، كليٌّ ماهويّ (اسمٌ مقروءُ الإعراب على غير ذلك) — `kulli_witnesses`. على "
        "الميزان: "
        + "، ".join(f"{k} {v}" for k, v in on_mizan.most_common()) + ".",
        "",
        "## القياس على MASAQ", "",
        f"على {m['n']:,} كلمةً موسومةً بلا لواحق من شريحة شبه الجملة بشهادات البوّابة: القارئُ يوافق "
        "صنفَ "
        f"MASAQ في {agree:,} من {total:,} (الأعلامُ تُعدّ على حدة: جزئيّةٌ بالمعجم لا بالخانة).",
        "",
        "| صنفُ MASAQ | القارئ | العدد |", "|---|---|---|",
        *[f"| {t} | {k} | {v:,} |" for (t, k), v in read.most_common()],
        "",
        "## ما لا تقرؤه الخانة — باسمه", "",
        "- العلمُ (NOUN_PROP) جزئيٌّ بالمعجم: الخانةُ تقرؤه ماهويًّا أو عرضيًّا بقالبه (اللَّهُ "
        "على فَعَّال "
        "بالخانة).",
        "- مُفَاعَلَةٌ (مصدرُ فَاعَلَ) هي مُفَاعَلٌ + تاءُ التأنيث بالخانة (مُكَاتَبَةٌ: مصدرٌ أو اسمُ مفعولٍ مؤنّث): "
        "تُقرأ عرضيّةً — الخانةُ لا تفصل.",
        "- الجامدُ والمصدرُ على قالبٍ واحد (بَحْرٌ وضَرْبٌ على فَعْلٌ، كِتَابٌ وقِتَالٌ على "
        "فِعَالٌ): «حدثٌ "
        "مجرّد» عند القارئ يعني «على قالب المصدر»، والفرقُ معنًى — أكبرُ البقايا (كليٌّ ماهويّ "
        "يُقرأ حدثًا).",
        "- الجامدُ على قالب الوصف (كَاتِب علمًا) والمصدرُ على قالب الجامد: القالبُ لا المعنى.",
        "- الفعلُ المعتلُّ والمبنيُّ للمجهول من المزيد على غير قالب؛ والفعلُ الماضي يشابه مصدرًا "
        "بالخانة بعد "
        "ردّ آخره (كَتَبَ/فَعَلٌ) فقُدِّمت الصيغة.",
        "- الحصرُ المُرسَل: أنواعُه مكتوبةٌ باليد وبرهاناه `use t` وفحصُه `assert x in [True, "
        "False]` — لم "
        "يُدخَل منه شيء؛ ودخل معناه على الخانات.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("KULLI_INDEX.md غيرُ مطابق؛ شغّل tools/gen_kulli_index.py\n")
            return 1
        sys.stdout.write("KULLI_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب KULLI_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
