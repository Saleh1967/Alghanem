"""فهرسُ الجهة الوجوديّة (WUJUD_INDEX.md): تقسيمُ القوالب المغلق، ومطابقتُه مع القارئ، ومع وسوم
MASAQ المحجوبة.

(١) على `tests/data/corpus-certificates.json.gz` (18,179 صورة): جهةُ القراءة الأولى لكلّ صورةٍ
يقرؤها الجذع. (٢) على `masaq-shibh.json.gz`: وسمُ المرجع (فعلٌ: PV/IV/CV ومبنيّهما للمجهول؛
مصدرٌ: GERUND؛ وصفٌ: اسما الفاعل والمفعول والصفةُ والتفضيل؛ اسمٌ: سائرُ الأسماء) مقابل جهة
القراءة الأولى (الظرفُ والآلةُ والجمعُ والاسمُ اسمٌ عند المقابلة) — قبل ترتيب الأداة المجاورة
وبعده.
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from slge.adawat import of_cells
from slge.adawat import rank as rank_adawat
from slge.jidh import jidh
from slge.maqayis import rank as rank_maqayis
from slge.wujud import FIL, ISM, JAM, MASDAR, WASF, ZARF, of_class, ont_of_reading

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "WUJUD_INDEX.md"
DATA = ROOT / "tests" / "data"
Word = tuple[tuple[str, str], ...]
GOLD: dict[str, str] = {
    "PV": FIL, "IV": FIL, "CV": FIL, "PV_PASS": FIL, "IV_PASS": FIL, "GERUND": MASDAR,
    "NOUN_ACTIVE_PART": WASF, "NOUN_PASSIVE_PART": WASF, "ADJ_QUALIT": WASF, "ADJ_COMP": WASF,
    "NOUN_CONCRETE": ISM, "NOUN_ABSTRACT": ISM, "NOUN_PROP": ISM, "NOUN_PROP_FOREIGN": ISM,
    "ADV": ISM,
}
COARSE: dict[str, str] = {FIL: FIL, MASDAR: MASDAR, WASF: WASF, ZARF: ISM, JAM: ISM, ISM: ISM}
CLASSES = (FIL, MASDAR, WASF, ISM)


def corpus_forms() -> list[Word]:
    with gzip.open(DATA / "corpus-certificates.json.gz", "rt", encoding="utf-8") as f:
        d: dict[str, Any] = json.load(f)
    return [tuple((a, b) for a, b in x["cells"]) for x in d["forms"]]


def masaq_rows() -> list[dict[str, Any]]:
    with gzip.open(DATA / "masaq-shibh.json.gz", "rt", encoding="utf-8") as f:
        rows: list[dict[str, Any]] = json.load(f)["rows"]
    return rows


def whole(r: dict[str, Any]) -> Word:
    return (*((a, b) for _, cs in r["pre"] for a, b in cs), *((a, b) for a, b in r["stem"]),
            *((a, b) for _, cs in r["suf"] for a, b in cs))


def measure() -> dict[str, Any]:
    forms = corpus_forms()
    dist: Counter[str] = Counter()
    for w in forms:
        rs = rank_maqayis(jidh(w))
        dist[ont_of_reading(rs[0]) if rs else "—"] += 1
    rows = masaq_rows()
    idx = {(r["ref"], r["pos"]): r for r in rows}
    conf_b: Counter[tuple[str, str]] = Counter()
    conf_a: Counter[tuple[str, str]] = Counter()
    none = 0
    for r in rows:
        gold = GOLD.get(r["tag"])
        if gold is None:
            continue
        rs = rank_maqayis(jidh(whole(r)))
        if not rs:
            none += 1
            continue
        conf_b[(gold, COARSE[ont_of_reading(rs[0])])] += 1
        prev = idx.get((r["ref"], r["pos"] - 1))
        a = of_cells(whole(prev)) if prev else None
        top = rank_adawat(a, rs)[0] if a else rs[0]
        conf_a[(gold, COARSE[ont_of_reading(top)])] += 1
    return {"forms": len(forms), "dist": dist, "classes": {o: len(of_class(o)) for o in
            (FIL, MASDAR, WASF, ZARF, JAM, ISM)}, "masaq": sum(conf_b.values()) + none,
            "none": none, "before": conf_b, "after": conf_a}


def _table(conf: Counter[tuple[str, str]]) -> list[str]:
    lines = ["| المرجع ↓ / القراءة → | " + " | ".join(CLASSES) + " | موافق |",
             "|---|" + "---|" * (len(CLASSES) + 1)]
    for g in CLASSES:
        tot = sum(conf[(g, p)] for p in CLASSES)
        cells = " | ".join(f"{conf[(g, p)]:,}" for p in CLASSES)
        pct = f"{100 * conf[(g, g)] / tot:.1f}%" if tot else "—"
        lines.append(f"| {g} ({tot:,}) | {cells} | {pct} |")
    tot = sum(conf.values())
    hit = sum(conf[(g, g)] for g in CLASSES)
    lines.append(f"| **الكلّ** ({tot:,}) | | | | | **{100 * hit / tot:.1f}%** |")
    return lines


def render() -> str:
    m = measure()
    d, c = m["dist"], m["classes"]
    lines = [
        "# فهرسُ الجهة الوجوديّة — المصدرُ والمشتقُّ والجامد",
        "",
        "مولَّدٌ بـ`python tools/gen_wujud_index.py` من `src/slge/wujud.py`؛ لا يُحرَّر باليد. البرهانُ: "
        "`formal/Slge/Wujud.lean`؛ الجدولُ `formal/Slge/WujudTable.lean` مولَّدٌ من أبواب الأوزان "
        "(`tools/deposit_wujud.py --check`).",
        "",
        "## التقسيمُ المغلق", "",
        f"125 قالبًا على ستّة أصناف لا سابعَ لها: فعلٌ {c[FIL]}، مصدرٌ {c[MASDAR]}، وصفٌ مشتقّ {c[WASF]}، "
        f"ظرفٌ وآلة {c[ZARF]}، صيغةُ جمع {c[JAM]}، اسمٌ {c[ISM]} (مصدرٌ أو جامدٌ: الجمودُ قيدٌ معجميٌّ لا "
        "تفصله الخانة). مبرهَن: الفعلُ هو قوائمُ الماضي والمضارع والأمر (`fil_eq`)، والمصدرُ قوالبُ "
        "المصدر "
        "بعينها (`masdar_eq`)، والوصفُ داخل قوالب الوصف إلّا فُعَلَاءُ جمعًا (`wasf_derived`)؛ كلُّ فعلٍ له "
        "صيغةٌ على ميزانه ولا صيغةَ لمصدر (`fil_sigha_mizan`، `masdar_no_sigha_mizan`)؛ أصلُ الشبكة "
        "مصدرٌ "
        "(`root_masdar`)، ولا شيءَ ينحدر من اسمٍ أو صيغة جمع (`ism_jam_leaves`)، والمشتقُّ أبوه فعلٌ أو "
        "مشتقّ (`mushtaqq_from_fil_or_mushtaqq`) — هذا معنى «الجامدُ لا يُشتقّ منه» على الجدول.",
        "",
        "## المطابقةُ مع القارئ", "",
        "`kulli` يقرأ الجهةَ المودَعة على الميزان في 111 من 125 (`kulli_agreement`)؛ والمخالفُ 14 "
        "بأرقامها "
        "وسببُه اشتراكُ الصورة (أَفْعَلُ/أَفْعُلُ مضارعُ المتكلّم، فِعْلَة جمعًا وهيئة، فِعَال وفُعُول جمعًا "
        "ومصدرًا، مُفَاعَلَة ومِفْعَال وفَعَّالَة بصورة المشتقّ، فُعَلَاء) أو ما لا يقرؤه (المقصور).",
        "",
        "## على مودَع المصحف", "",
        f"جهةُ القراءة الأولى لـ{m['forms']:,} صورة: فعلٌ {d[FIL]:,}، مصدرٌ {d[MASDAR]:,}، "
        f"وصفٌ {d[WASF]:,}، "
        f"ظرفٌ وآلة {d[ZARF]:,}، جمعٌ {d[JAM]:,}، اسمٌ {d[ISM]:,}، لا قراءة {d['—']:,}.",
        "",
        "## المطابقةُ مع وسوم MASAQ المحجوبة", "",
        f"على {m['masaq']:,} كلمةً وسمُها من الأصناف الأربعة (الظرفُ والآلةُ والجمعُ والاسمُ اسمٌ عند "
        "المقابلة)؛ "
        f"لا قراءةَ لها {m['none']:,}. قبل ترتيب الأداة المجاورة:",
        "",
        *_table(m["before"]),
        "",
        "وبعد ترتيب الأداة المجاورة (`Adawat.rank`):",
        "",
        *_table(m["after"]),
        "",
        "## ما ليس هنا — باسمه", "",
        "- الجمودُ قيدٌ معجميّ: فِعْلٌ عِلْمٌ مصدرٌ ورِجْلٌ جامد — الخانةُ لا تفصلهما، والقرينةُ المعجميّةُ تشهد "
        "للجذر لا للجمود.",
        "- الزمانُ والمكانُ والآلةُ لا صنفَ لها عند القارئ الكليّ (تُقرأ «كليًّا ماهويًّا»).",
        "- المصدرُ الميميّ (مَفْعَل) زمانٌ ومكانٌ في الجدول؛ تعدّدُه مصدرًا لا تفصله الخانة.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("WUJUD_INDEX.md غيرُ مطابق؛ شغّل tools/gen_wujud_index.py\n")
            return 1
        sys.stdout.write("WUJUD_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب WUJUD_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
