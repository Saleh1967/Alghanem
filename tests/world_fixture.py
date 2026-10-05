"""عالمٌ صغيرٌ للاختبار، منقولٌ من `alghanem/src/alghanem/arabic/world_knowledge_gap.py`.

الشواهدُ بنصوصها ومواضعها هناك (القرآنُ المودَع، والبخاريّ، ولسانُ العرب، ومعيارُ العلم)؛
وهنا تُستعمل أسماؤها لاختبار الآلة لا لإثبات القواعد.
"""

from __future__ import annotations

from slge.knowledge import (
    Admission,
    Degree,
    Evidence,
    Genus,
    Licence,
    LicenceGround,
    Literal,
    Naql,
    Standing,
    WorldRule,
)
from slge.learning import GoldQuestion

GENERATOR = "مولِّد (رأي سابق)"


def ev(eid: str, genus: Genus, source: str, naql: Naql | None = None) -> Evidence:
    return Evidence(eid, genus, eid, source, naql=naql)


def rule(rid: str, a: str, b: str, st: Standing, e: Evidence | None,
         blockers: tuple[str, ...] = (), degree: Degree = Degree.اخص) -> WorldRule:
    return WorldRule(rid, a, b, degree, st, Admission.مقبول if e else Admission.مرشح,
                     "دليل مستقل" if e else GENERATOR, e, blockers)


QURAN = "corpora/quran-simple-enhanced.txt"
ADMITTED = (
    rule("أف-محرم", "أف", "محرم", Standing.شرعي,
         ev("قرآن-2052", Genus.خبر_مقبول, QURAN, Naql.متواتر)),
    rule("حمل-نفقة", "حامل", "نفقة", Standing.شرعي,
         ev("قرآن-5223", Genus.خبر_مقبول, QURAN, Naql.متواتر)),
    rule("سائمة-زكاة", "سائمة", "زكاة", Standing.شرعي,
         ev("بخاري", Genus.خبر_مقبول, "bukhari", Naql.آحاد)),
    rule("أف-أذى", "أف", "أذى", Standing.وضعي, ev("لسان", Genus.شاهد_معجمي, "lisan")),
    rule("إنسان-حيوان", "إنسان", "حيوان", Standing.تعريفي,
         ev("حد", Genus.تعريف_مشترط, "micyar")),
)
PROPOSED_RULES = (
    rule("أذى-محرم", "أذى", "محرم", Standing.شرعي, None),
    rule("ضرب-أذى", "ضرب", "أذى", Standing.عادي, None, ("ضرب لا يؤلم",)),
)


def hypothesis(rid: str, ground: LicenceGround) -> Licence:
    return Licence(rid, ground, ev(f"اقتراح-{rid}", Genus.فرضية, GENERATOR))


PROPOSED_LICENCES = (
    hypothesis("سائمة-زكاة", LicenceGround.وصف_مفهم),
    hypothesis("حمل-نفقة", LicenceGround.أداة_شرط),
)

GOLD = (
    GoldQuestion("موافقة", "هل يحرم ضرب الوالدين؟", Literal("ضرب", True), "محرم",
                 Literal("محرم", True), "ج٣:519"),
    GoldQuestion("مخالفة-صفة", "هل تجب الزكاة في المعلوفة؟", Literal("سائمة", False), "زكاة",
                 Literal("زكاة", False), "ج٣:529"),
    GoldQuestion("مخالفة-شرط", "هل تجب النفقة لغير الحامل؟", Literal("حامل", False), "نفقة",
                 Literal("نفقة", False), "ج٣:534"),
    GoldQuestion("ضابط", "إذا لم يكن إنسانًا، أليس حيوانًا؟", Literal("إنسان", False), "حيوان",
                 None, "معيار العلم"),
)
