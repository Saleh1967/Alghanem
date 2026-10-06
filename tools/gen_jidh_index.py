"""فهرسُ الجذع على درجات الترخيص التدريجيّ (JIDH_INDEX.md): الرقمُ قبل التسوية والفصل وبعدهما على
المودَع نفسه.

القياسُ على `tests/data/corpus-certificates.json.gz` (18,179 صورةً مشهودةً من المصحف، بسوابقها
ولواحقها): (٠) القوالبُ على الصورة كما هي (`wad.senses`)؛ (١) بعد تسوية الآخر وحدَها
(`stem_senses`)؛ (٢) بعد فصل الزوائد (`jidh`). ثمّ على `masaq-shibh.json.gz` بقسمته المحجوبة
(سوابق/جذع/لواحق عند المرجع): هل قراءةُ الجذع توافق قسمةَ المرجع؟ وإن تعدّدت القراءات فهل القسمةُ
الذهبيّة بينها؟
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from slge.jidh import jidh, stem_senses
from slge.marifa import drop_tanwin
from slge.wad import senses

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "JIDH_INDEX.md"
DATA = ROOT / "tests" / "data"
Word = tuple[tuple[str, str], ...]
PRE_IN_STEM = ("IMPERF_PREF", "CV_PREF", "IV1S", "IV1P", "IV2MP", "IV3MS", "IV3MP", "IV3FS")
"""سوابقُ MASAQ التي تُعدّ من الجذع هنا (صدرُ المضارع والأمر جزءٌ من القالب)."""


def corpus_forms() -> list[Word]:
    with gzip.open(DATA / "corpus-certificates.json.gz", "rt", encoding="utf-8") as f:
        d: dict[str, Any] = json.load(f)
    return [tuple((a, b) for a, b in x["cells"]) for x in d["forms"]]


def masaq_rows() -> list[tuple[Word, Word, bool, Word, Word]]:
    """(الكلمة، سوابقُ المرجع بلا أل، أفيها أل؟، جذعُه، لواحقُه) — صدرُ المضارع مع الجذع."""

    with gzip.open(DATA / "masaq-shibh.json.gz", "rt", encoding="utf-8") as f:
        rows: list[dict[str, Any]] = json.load(f)["rows"]
    out = []
    for r in rows:
        allpre = tuple((a, b) for _, cs in r["pre"] for a, b in cs)
        pre = tuple((a, b) for t, cs in r["pre"] for a, b in cs
                    if t not in PRE_IN_STEM and t != "DET")
        det = any(t == "DET" for t, _ in r["pre"])
        stem = tuple((a, b) for t, cs in r["pre"] for a, b in cs if t in PRE_IN_STEM)
        stem += tuple((a, b) for a, b in r["stem"])
        suf = tuple((a, b) for _, cs in r["suf"] for a, b in cs)
        if stem:
            out.append((allpre + tuple((a, b) for a, b in r["stem"]) + suf, pre, det, stem, suf))
    return out


def measure() -> dict[str, Any]:
    forms = corpus_forms()
    before = sum(bool(senses(drop_tanwin(w))) for w in forms)
    step1 = sum(bool(stem_senses(w)) for w in forms)
    readings = Counter()
    for w in forms:
        n = len(jidh(w))
        readings["0" if n == 0 else "1" if n == 1 else "2" if n == 2 else "3+"] += 1
    step2 = len(forms) - readings["0"]
    gold_match = gold_among = none = only_wrong = 0
    rows = masaq_rows()
    for w, pre, det, _, suf in rows:
        rs = jidh(w)
        if not rs:
            none += 1
            continue
        hits = [r for r in rs if tuple(c for p in r.pre for c in p) == pre and (r.al != 0) == det
                and r.suf == suf]
        if hits and len(rs) == 1:
            gold_match += 1
        elif hits:
            gold_among += 1
        else:
            only_wrong += 1
    return {"forms": len(forms), "before": before, "step1": step1, "step2": step2,
            "readings": readings, "masaq": len(rows), "gold_match": gold_match,
            "gold_among": gold_among, "only_wrong": only_wrong, "none": none}


def render() -> str:
    m = measure()
    n, r = m["forms"], m["readings"]
    lines = [
        "# فهرسُ الجذع على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_jidh_index.py` من `src/slge/jidh.py`؛ لا يُحرَّر باليد. "
        "البرهانُ: "
        "`formal/Slge/Jidh.lean`.",
        "",
        "## د٤ الخانة — الإعرابُ حالةُ الخانة الأخيرة لا جزءٌ من القالب", "",
        "القوالبُ مودَعةٌ بآخرٍ واحد، فلا تُطابَق الكلمةُ إلّا بعد تسوية آخرها إلى حالة آخر القالب "
        "(`onTemplateMod`). مبرهَنٌ لكلّ قالبٍ وكلمةٍ وحالة: استخراجُ الجذر لا يرى الحالات "
        "(`rootOf_setLast`)، وملءُ قالبٍ سليم بأيّ حالةٍ في آخره يُقرأ على قالبه ويُستردّ "
        "جذرُه بعينه "
        "(`onTemplateMod_setLast`).",
        "",
        "## الفصلُ بردٍّ بعينه", "",
        "السوابقُ من الجداول الحاصرة (و ف ب ل ك س أ لَ، وأل بهمزتها أو موصولةً بلا همزةٍ بعد "
        "سابقة)، واللواحقُ "
        "من جداول الضمائر المتّصلة ولواحق الفاعل. كلُّ قطعٍ يُردّ بالإلصاق (`peelPrefix_sound`، "
        "`peelSuffix_sound`، `dropAl_sound`) والقارئُ لا يعيد قراءةً إلّا وردُّها الكلمةُ بعينها "
        "(`jidh_restores`: لكلّ كلمة). الشواهدُ `jidh_witnesses_*`.",
        "",
        "## الرقمُ قبلُ وبعدُ — على المودَع نفسه", "",
        f"{n:,} صورةً مشهودةً من المصحف بسوابقها ولواحقها:",
        "",
        "| المرحلة | صورٌ تقرؤها القوالب | % |", "|---|---|---|",
        f"| (٠) كما هي (`wad.senses`) | {m['before']:,} | {100 * m['before'] / n:.1f} |",
        f"| (١) بعد تسوية الآخر وحدَها | {m['step1']:,} | {100 * m['step1'] / n:.1f} |",
        f"| (٢) بعد فصل الزوائد (`jidh`) | {m['step2']:,} | {100 * m['step2'] / n:.1f} |",
        "",
        f"عددُ القراءات بعد الفصل: واحدة {r['1']:,}، اثنتان {r['2']:,}، ثلاثٌ فأكثر "
        f"{r['3+']:,}، لا قراءة "
        f"{r['0']:,} — التعدّدُ يُقرأ كما هو والقرينةُ تفصله.",
        "",
        "## القياس على قسمة MASAQ المحجوبة", "",
        f"على {m['masaq']:,} كلمةً قسمها المرجعُ سوابقَ وجذعًا ولواحقَ: قراءةٌ واحدةٌ توافق القسمة "
        f"{m['gold_match']:,} ({100 * m['gold_match'] / m['masaq']:.1f}%)، القسمةُ بين "
        f"قراءاتٍ متعدّدة "
        f"{m['gold_among']:,} ({100 * m['gold_among'] / m['masaq']:.1f}%)، قراءاتٌ كلُّها على "
        f"غير القسمة "
        f"{m['only_wrong']:,} ({100 * m['only_wrong'] / m['masaq']:.1f}%)، لا قراءة {m['none']:,} "
        f"({100 * m['none'] / m['masaq']:.1f}%).",
        "",
        "## ما لا يُقرأ بعدُ — باسمه", "",
        "- الإعلالُ (قَالَ، كَانَ، جَاءَ، يَكُنْ): مبرهَنٌ في الغانم `A116.Ilal` ولم يُنقل "
        "إلى هنا.",
        "- قالبا فِعْلٍ (عِلْم، ذِكْر، رِزْق) وفَعَالٍ (عَذَاب، سَمَاء) غيرُ مودَعين في الـ121.",
        "- تاءُ التأنيث واللواحقُ المركّبة (ونَ + هُ…) والمضعَّفُ المدغَم في المضارع (يَضِلُّ).",
        "- ما تقرؤه الجداول (الأدواتُ والضمائرُ والأعلامُ والأعداد) ليس للقوالب أصلًا.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("JIDH_INDEX.md غيرُ مطابق؛ شغّل tools/gen_jidh_index.py\n")
            return 1
        sys.stdout.write("JIDH_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب JIDH_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
