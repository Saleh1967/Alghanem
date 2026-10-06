"""فهرسُ المتباين على درجات الترخيص التدريجيّ (TABAYUN_INDEX.md) من `slge.tabayun` وشريحة MASAQ.

القياسُ على `masaq-shibh.json.gz` بشهادات البوّابة: الصورُ المقروءةُ (التي تقرؤها القوالب بجذرٍ لا ألفَ
فيه) من الكلمات الموسومة بلا لواحق، ثمّ العلاقةُ بين كلّ صورتين منها (متباينان/متّحدا المادّة/متداخلان)
وعائلاتُ المادّة الواحدة.
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path
from typing import Any

from slge.marifa import drop_tanwin
from slge.tabayun import isolated, mawadd
from slge.wazn import AWZAN

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "TABAYUN_INDEX.md"
DATA = ROOT / "tests" / "data"
Word = tuple[tuple[str, str], ...]
PRE_TAGS = ("DET", "IMPERF_PREF", "CV_PREF", "IV1S", "IV1P", "IV2MP", "IV3MS", "IV3MP", "IV3FS")
SUBJ_TAGS = ("SUBJ_PRON", "PVSUFF_SUBJ", "IVSUFF_SUBJ", "CVSUFF_SUBJ", "OBJ_PRON", "PVSUFF_DO",
             "IVSUFF_DO", "POSS_PRON", "NSUFF", "EMPHATIC_NUN", "PROTECT_NUN")
TAGS = ("PRON", "DEM_PRON", "REL_PRON", "NOUN_ACTIVE_PART", "NOUN_PASSIVE_PART", "ADJ_QUALIT",
        "ADJ_COMP", "GERUND", "IV", "PV", "CV", "IV_PASS", "PV_PASS", "NOUN_CONCRETE",
        "NOUN_ABSTRACT", "NOUN_PROP")


def _cells(r: dict[str, Any]) -> Word:
    pre = [(a, b) for t, cs in r["pre"] for a, b in cs if t in PRE_TAGS]
    return (*pre, *((a, b) for a, b in r["stem"]))


def forms() -> dict[Word, frozenset[tuple[str, str, str] | None]]:
    """الصورُ المقروءة (بعد ردّ التنوين) ← موادُّها."""

    with gzip.open(DATA / "masaq-shibh.json.gz", "rt", encoding="utf-8") as f:
        rows: list[dict[str, Any]] = json.load(f)["rows"]
    out: dict[Word, frozenset[tuple[str, str, str] | None]] = {}
    for r in rows:
        if str(r["tag"]) not in TAGS or any(t.startswith(SUBJ_TAGS) for t, _ in r["suf"]):
            continue
        if r["stem"]:
            v = drop_tanwin(_cells(r))
            m = frozenset(mawadd(v))
            if m:
                out.setdefault(v, m)
    return out


def measure() -> dict[str, object]:
    fs = forms()
    pairs: Counter[str] = Counter()
    for a, b in combinations(fs, 2):
        ma, mb = fs[a], fs[b]
        pairs["متباينان" if not ma & mb else "متّحدا المادّة" if ma == mb else "متداخلان"] += 1
    families: Counter[tuple[str, str, str] | None] = Counter()
    for m in fs.values():
        if len(m) == 1:
            families[next(iter(m))] += 1
    sizes: Counter[int] = Counter(families.values())
    return {"forms": len(fs), "pairs": pairs, "families": families, "sizes": sizes,
            "isolated": sum(isolated(k) for k in range(len(AWZAN)))}


def render() -> str:
    m = measure()
    pairs: Counter[str] = m["pairs"]  # type: ignore[assignment]
    families: Counter[tuple[str, str, str] | None] = m["families"]  # type: ignore[assignment]
    sizes: Counter[int] = m["sizes"]  # type: ignore[assignment]
    total = sum(pairs.values())
    top = ["".join(k) if k else "—" for k, _ in families.most_common(5)]
    lines = [
        "# فهرسُ المتباين على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_tabayun_index.py` من `src/slge/tabayun.py`؛ لا يُحرَّر باليد. "
        "البرهانُ: `formal/Slge/Tabayun.lean`.",
        "",
        "## د٤ الخانة — المادّةُ والحصرُ السباعيّ", "",
        "المادّةُ على الخانات جذرُ الكلمة بقالبٍ يقرؤها، وموادُّها جذورُها بكلّ قالبٍ قارئ. الحصرُ "
        "السباعيُّ باعتبار الدالّ والمدلول يُقرأ بعدد الكلمات وعدد الموادّ: منفردٌ (كلمةٌ بمادّة)، "
        "مشتركٌ (كلمةٌ بمادّتين)، متّحدا المادّة (كلمتان مادّتُهما واحدة — ترادفُ صورة)، متباينان "
        "(كلمتان لا مادّةَ بينهما)؛ والمتداخلان (مادّةٌ مشتركةٌ وأخرى منفردة) قسمٌ ثامن تقرؤه الخانة "
        "ولا يذكره الحصر (`seven_not_exhaustive`: اِنْتِشَارٌ/نَشْرٌ).",
        "",
        "التباينُ متماثلٌ لكلّ كلمتين (`tabayun_symm`) وكلُّ ذي مادّةٍ يشارك نفسَه (`shareMadda_self`) "
        "فلا كلمةَ تباين نفسَها (`tabayun_irrefl`). والترادفُ التامُّ مستحيلٌ على الخانات: الملءُ دالّة "
        "(`fill_functional` — بديهيّ).",
        "",
        "## الأصلُ في الوضع التباين", "",
        f"على القالب المعزول (لا يلتقي بقالبٍ غيرِ مطابق — {m['isolated']} من الـ{len(AWZAN)} "
        "`isolated_count`)، جذران مختلفان لا ألفَ فيهما يعطيان كلمتين متباينتين على قالبٍ واحد: "
        "التباينُ في المادّة لا يلغي الجنسَ الجامع (الصورة) — `tabayun_of_isolated` لكلّ قالبٍ معزول "
        "ولكلّ جذرين. وعلى غير المعزول يقع التداخل.",
        "",
        "## القارئ", "",
        "`rel` يقرأ علاقةَ كلمتين بعد ردّ التنوين — `rel_witnesses`: ضَرْبٌ/قَتْلٌ متباينان على فَعْلٍ، "
        "ضَرْبٌ/ضِرَابٌ متّحدا المادّة، اِنْتِشَارٌ/نَشْرٌ متداخلان، كِتَابٌ منفردٌ بمادّته وإن اشترك وضعُه، "
        "اِنْتِشَارٌ مشترك.",
        "",
        "## القياس على MASAQ", "",
        f"{m['forms']:,} صورةً مقروءةً من كلمات الشريحة الموسومة بلا لواحق بشهادات البوّابة؛ "
        f"بين كلّ صورتين ({total:,} زوجًا): متباينان {pairs['متباينان']:,} "
        f"({100 * pairs['متباينان'] / total:.2f}%)، متّحدا المادّة {pairs['متّحدا المادّة']:,}، "
        f"متداخلان {pairs['متداخلان']:,}. عائلاتُ المادّة الواحدة {len(families):,}: "
        + "، ".join(f"{n} صورة ×{sizes[n]}" for n in sorted(sizes)) + f"؛ أكبرُها {'، '.join(top)}.",
        "",
        "## ما لا تقرؤه الخانة — باسمه", "",
        "- المنقولُ والحقيقةُ والمجاز: نقلٌ بالاشتهار لا خانةَ له — معلَن.",
        "- التضادّ: السوادُ والبياضُ متباينان بالخانة كأيّ جذرين، والضدّيّةُ معنًى؛ وفَعَالٌ "
        "(سَوَادٌ/بَيَاضٌ) ليست في المعجم المودَع فلا تُقرأ.",
        "- متّحدا المادّة ترادفُ صورةٍ لا معنًى: كَتَبَ وكِتَابٌ وكَاتِبٌ مادّتُها واحدة.",
        "- الحصرُ المُرسَل: أنواعُه مكتوبةٌ باليد وبرهاناه `cases r <;> simp` على عدٍّ مكتوبٍ باليد — "
        "لم يُدخَل منه شيء؛ ودخل معناه على الخانات.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("TABAYUN_INDEX.md غيرُ مطابق؛ شغّل tools/gen_tabayun_index.py\n")
            return 1
        sys.stdout.write("TABAYUN_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب TABAYUN_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
