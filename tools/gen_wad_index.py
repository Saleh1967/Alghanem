"""فهرسُ الوضع والمشترك والترادف على درجات الترخيص التدريجيّ (WAD_INDEX.md) من `slge.wad` وشريحة
MASAQ.

القياسُ على `masaq-shibh.json.gz` بشهادات البوّابة: لكلّ كلمةٍ موسومةٍ بلا لواحق (السوابقُ والجذع) عددُ
القوالب التي تقرؤها بجذرٍ لا ألفَ فيه؛ ووسمُ MASAQ للصنف (GERUND مصدرٌ، NOUN جامدٌ أو جمعٌ، ADJ/PART
مشتقٌّ، IV/PV/CV فعل، NOUN_PROP علَم) مرجعٌ محجوبٌ يقوم مقامَ القرينة فيفصل المشترك.
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from slge.marifa import drop_tanwin
from slge.wad import classes, collision_pairs, duplicates, senses, wad
from slge.wazn import AWZAN

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "WAD_INDEX.md"
DATA = ROOT / "tests" / "data"
Word = tuple[tuple[str, str], ...]
PRE_TAGS = ("DET", "IMPERF_PREF", "CV_PREF", "IV1S", "IV1P", "IV2MP", "IV3MS", "IV3MP", "IV3FS")
SUBJ_TAGS = ("SUBJ_PRON", "PVSUFF_SUBJ", "IVSUFF_SUBJ", "CVSUFF_SUBJ", "OBJ_PRON", "PVSUFF_DO",
             "IVSUFF_DO", "POSS_PRON", "NSUFF", "EMPHATIC_NUN", "PROTECT_NUN")
TAG_KIND: dict[str, str] = {
    "PRON": "جزئيّ", "DEM_PRON": "جزئيّ", "REL_PRON": "جزئيّ",
    "NOUN_ACTIVE_PART": "مشتقّ", "NOUN_PASSIVE_PART": "مشتقّ", "ADJ_QUALIT": "مشتقّ",
    "ADJ_COMP": "مشتقّ",
    "GERUND": "مصدر", "IV": "فعل", "PV": "فعل", "CV": "فعل", "IV_PASS": "فعل", "PV_PASS": "فعل",
    "NOUN_CONCRETE": "جامد/جمع", "NOUN_ABSTRACT": "جامد/جمع", "NOUN_PROP": "علَم",
}
KINDS = ("مجدوَل", "مفرد الوضع", "مشترك الوضع", "مشترك الصورة", "—")


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
    dist: Counter[str] = Counter()
    sura: Counter[tuple[tuple[int, ...], str]] = Counter()
    wadc: Counter[tuple[tuple[int, ...], str]] = Counter()
    ws = words()
    for kind, w in ws:
        dist[wad(w)] += 1
        v = drop_tanwin(w)
        s, c = senses(v), classes(v)
        if len(c) >= 2:
            sura[(c, kind)] += 1
        elif len(s) >= 2:
            wadc[(s, kind)] += 1
    return {"dist": dist, "sura": sura, "wad": wadc, "n": len(ws)}


def _names(ks: tuple[int, ...]) -> str:
    return "/".join(AWZAN[k].name for k in ks)


def render() -> str:
    m = measure()
    dist: Counter[str] = m["dist"]  # type: ignore[assignment]
    sura: Counter[tuple[tuple[int, ...], str]] = m["sura"]  # type: ignore[assignment]
    wadc: Counter[tuple[tuple[int, ...], str]] = m["wad"]  # type: ignore[assignment]
    readable = dist["مفرد الوضع"] + dist["مشترك الوضع"] + dist["مشترك الصورة"]
    pairs = collision_pairs()
    dups = duplicates()
    sura_pairs = [(k, q) for k, q in pairs if (k, q) not in dups]
    lines = [
        "# فهرسُ الوضع والمشترك والترادف على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_wad_index.py` من `src/slge/wad.py`؛ لا يُحرَّر باليد. "
        "البرهانُ: "
        "`formal/Slge/Wad.lean`.",
        "",
        "## د٤ الخانة — الوضعُ ملءُ قالبٍ بجذر", "",
        "الوضعُ على الخانات `fill t r`: القالبُ (الصورة) والجذرُ (المادّة) يُقرَنان في الكلمة. "
        "متباينٌ في "
        "الجذر لكلّ قالبٍ سليم (`wad_injective`)، والقالبُ يُستردّ من ملئه لكلّ جذرٍ لا ألفَ فيه "
        "(`sense_of_fill`). الميزانُ (ف‑ع‑ل) لا يُشترَك: كلُّ ميزانٍ من الـ121 يُقرأ على صورةٍ "
        "واحدة "
        "ومعانيه بابُ قالبه بعينه (`mizan_unaided`، `mizan_senses`).",
        "",
        "## المشتركُ اللفظيّ على الخانات", "",
        f"**اشتراكُ الوضع** — صورةٌ واحدةٌ مودَعةٌ لأكثر من باب: {len(dups)} أزواجٍ متطابقة "
        "(`duplicate_templates`): "
        + "، ".join(f"{AWZAN[k].name} ({k}: {AWZAN[k].bab}، {q}: {AWZAN[q].bab})" for k, q in dups)
        + ".",
        "",
        "**اشتراكُ الصورة** — قالبان مختلفان يلتقيان في كلمة. لا يلتقيان على كلمةٍ لجذرين لا "
        "ألفَ فيهما إلّا "
        "إذا تساوى طولُهما وحالاتُهما وزوائدُهما المتقابلة ولم يقابل ألفًا زائدةً موضعُ أصل "
        "(`mayCollide_sound`: لكلّ قالبين ولكلّ جذرين)؛ وأزواجُ الـ121 التي تستوفي ذلك "
        f"{len(pairs)} بعينها (`collision_pairs_eq`)، منها {len(sura_pairs)} مختلفةُ القالب "
        "(`collision_pairs_split`) — فكلُّ اشتراكِ صورةٍ في المعجم المودَع مجدوَلٌ "
        "(`homonymy_is_tabled`):",
        "",
        "| الزوج | القالبان |", "|---|---|",
        *[f"| ({k}, {q}) | {AWZAN[k].name} / {AWZAN[q].name} |" for k, q in sura_pairs],
        "",
        "الشاهد: اِنْتِشَارٌ ملءُ اِنْفِعَالٍ بـ(ت، ش، ر) وملءُ افْتِعَالٍ بـ(ن، ش، ر) صورةٌ واحدة "
        "(`intishar_two_roots`)؛ ومَنْحَةٌ مَفْعَلٌ من ن‑ح‑ت وفَعْلَةٌ من م‑ن‑ح.",
        "",
        "## الترادف على الخانات", "",
        "المترادفان الصرفيّان صورتان مختلفتان لجذرٍ واحد في بابٍ واحد (مصادرُ الجذر): يشتركان في "
        "الجذر لكلّ "
        "قالبين سليمين ولكلّ جذر (`taraduf_same_root`) ويختلفان في الصورة إلّا ما تطابق قالبُه "
        "(`masdar_forms_distinct`).",
        "",
        "## القارئ", "",
        "`wad` يقرأ الوضعَ من الخانة بعد ردّ التنوين: مجدوَلٌ (الجزئيُّ من جدول)، مفردُ الوضع "
        "(قالبٌ واحد — "
        "الفهمُ بلا قرينة `unaided`)، مشتركُ الوضع، مشتركُ الصورة، أو لا يُقرأ — `wad_witnesses`.",
        "",
        "## القياس على MASAQ", "",
        f"على {m['n']:,} كلمةً موسومةً بلا لواحق من شريحة شبه الجملة بشهادات البوّابة: "
        + "، ".join(f"{'لا تقرؤه الخانة' if k == '—' else k} {dist[k]:,}" for k in KINDS)
        + f". ممّا تقرؤه القوالب ({readable:,}) يُفهم بلا قرينة {dist['مفرد الوضع']:,} "
        f"({100 * dist['مفرد الوضع'] / readable:.1f}%).",
        "",
        "وسمُ MASAQ قرينةً تفصل مشتركَ الوضع (الصورةُ الواحدةُ لأكثر من باب):",
        "",
        "| القوالب | قرينةُ المرجع | العدد |", "|---|---|---|",
        *[f"| {_names(s)} | {kind} | {v:,} |" for (s, kind), v in wadc.most_common()],
        "",
        "ومشتركَ الصورة (قالبان مختلفان):",
        "",
        "| القوالب | قرينةُ المرجع | العدد |", "|---|---|---|",
        *[f"| {_names(c)} | {kind} | {v:,} |" for (c, kind), v in sura.most_common()],
        "",
        "## ما لا تقرؤه الخانة — باسمه", "",
        "- المعنى اللغويّ: عَيْنٌ (ماءٌ أو بصر) مفردةُ الوضع بالخانة (فَعْلٌ) واشتراكُها معنًى؛ "
        "وقَمَرٌ/هِلَالٌ "
        "مترادفا جذرين لا تقرؤهما الخانة ترادفًا — معلَن.",
        "- الوضعُ الخاصّ (العلَم) بالمعجم: اللَّهُ بسابقة أل يُقرأ أَفْعَلَ/فَعَّلَ بالخانة "
        "(أكبرُ المشترك المقيس).",
        "- «الوضعُ موضوعُه الذهن» رأيٌ لا خانةَ له؛ وعلى الخانات الموضوعُ له زوجٌ (قالب، جذر) "
        "يُستردّ من الكلمة.",
        "- الإبدالُ: آمَنَ (أَأْمَنَ) تُقرأ فَاعَلَ من ء‑م‑ن بالخانة، وأَفْعَلَ تقتضي ألفًا في "
        "الجذر فتُردّ — "
        "مفردةُ الوضع على غير قالبها الأصليّ.",
        "- ما على غير قالبٍ من الـ121 (المعتلّ، الرباعيّ، الحروف، ما مع لواحق) لا يُقرأ وضعُه.",
        "- الحصرُ المُرسَل: أنواعُه ثلاثُ كلماتٍ مكتوبةٍ باليد وبرهاناه `rfl` و`cases h` على "
        "محمولٍ لا بانيَ "
        "له إلّا الذهن، وفحصُه عدٌّ عشوائيّ — لم يُدخَل منه شيء؛ ودخل معناه على الخانات.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("WAD_INDEX.md غيرُ مطابق؛ شغّل tools/gen_wad_index.py\n")
            return 1
        sys.stdout.write("WAD_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب WAD_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
