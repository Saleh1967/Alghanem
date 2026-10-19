"""`G0.FIBER-0.LAWS`: قوانينُ العقدة الليفيّة، مُجمَّدةً قبل أيّ تشغيلٍ ونتيجة.

المعلوماتُ السابقة المنظَّمة ليست خانةً تُعطى دورًا، ولا نصًّا يُقرَأ، بل هندسةٌ
مُرخَّصة: مجالٌ، ومواضعُ ممكنة، وفروقٌ مقبولة، وعلاقاتٌ، وقدراتٌ، وشروطُ دليلٍ،
وبوّاباتٌ، وسقفُ رتبةٍ مُحالٌ إلى سلطته، وسياسةُ بقايا، وأثر.

    PriorOrganizedInformation  =  LicensedFiberGeometry

ومنها تخرج ثلاثةُ ألياف **معًا لا على التعاقب**:

    P  →  CarrierAlone  ‖  ContentAlone  ‖  CarrierAndContentTogether

وهذه الطبقةُ لا تملك نظامًا، ولا تُجري مقارنةً، ولا تفتح gold. إنّما تُجمِّد
العقدَ الذي يُقرَأ لاحقًا من نظامين متوازيين، على أن يكون العقدُ محايدًا عنهما.
"""

from __future__ import annotations

from typing import Final

__all__ = [
    "AN_ADAPTER_FLOWS_INTO_THE_FIBER_NOT_THE_REVERSE",
    "A_COMMITTED_GOLD_IS_BOUND_NOT_SHIPPED",
    "DIGEST_ONLY_IS_NOT_CRYPTOGRAPHICALLY_HIDDEN_GOLD",
    "FROZEN_CONTRACT_BEFORE_READERS",
    "NO_POSITIVE_ROLE_FROM_A_NEUTRAL_FIBER_INPUT",
    "NO_SYSTEM_DEFINES_THE_CONTRACT_IT_IS_READ_BY",
    "OBSERVED_DOMINANCE_IS_BOUNDED_BY_ITS_FROZEN_DOMAIN",
    "PRIOR_FIBER_LAWS",
    "PriorFiberError",
    "THE_FIBER_DEFERS_ITS_RANK_TO_AN_EXTERNAL_AUTHORITY",
    "THE_THREE_FIBERS_ARE_PARALLEL_NOT_SEQUENTIAL",
]


class PriorFiberError(ValueError):
    """رفضٌ بنيويٌّ مُسمًّى في طبقة العقد الليفيّة؛ لا حملَ على أقرب حالة."""


NO_POSITIVE_ROLE_FROM_A_NEUTRAL_FIBER_INPUT: Final[str] = (
    "NeutralFiberInput ↛ PositiveStructuralRole: الدورُ الإيجابيُّ يُولَد أو "
    "يُرخَّص داخل الليف بدليلٍ مُسمًّى؛ فلا تُقلَب حالةُ مدخلٍ محايدةٍ دورًا "
    "بمجرّد وقوعها، ومن فعل ذلك أودع الجوابَ في موضع البرهان"
)

THE_THREE_FIBERS_ARE_PARALLEL_NOT_SEQUENTIAL: Final[str] = (
    "ThreeFibersAreParallelNotSequential: الأليافُ الثلاثةُ تُشتَقُّ من العقدة "
    "الواحدة معًا، ولا يُبنى ليفٌ على مخرج ليفٍ آخر؛ فترتيبُ التشغيل ليس ترتيبَ "
    "اشتقاق، ومن اشتقّ الثانيَ من الأوّل جعل محورًا شرطًا لمحور"
)

NO_SYSTEM_DEFINES_THE_CONTRACT_IT_IS_READ_BY: Final[str] = (
    "NoSystemDefinesTheContractItIsReadBy: عقدُ المجال محايدٌ عن كلِّ نظامٍ "
    "سيُقرَأ به؛ فمن عرّف الامتحانَ فاز به، والمقارنةُ حينئذٍ صورةٌ لا حجّة"
)

A_COMMITTED_GOLD_IS_BOUND_NOT_SHIPPED: Final[str] = (
    "CommittedGoldIsBoundNotShipped: العقدُ يحمل التزامَ الجواب المحجوب ولا يحمل "
    "الجوابَ؛ ولا يكفي أن يُسمّى محجوبًا وهو مقروءٌ من محتواه"
)

DIGEST_ONLY_IS_NOT_CRYPTOGRAPHICALLY_HIDDEN_GOLD: Final[str] = (
    "DigestOnly != CryptographicallyHiddenGold: بصمةُ الجواب وحدَها التزامٌ "
    "يُجرَّب في مجالٍ صغير؛ فالالتزامُ يُربَط بعشوائيّةٍ عاليةٍ وبجسم العقد، "
    "ويبقى سقفُ الدعوى ربطًا يمنع التبديل، لا إخفاءً تشفيريًّا لمادّةٍ مقروءةٍ "
    "من موضعٍ آخر"
)

FROZEN_CONTRACT_BEFORE_READERS: Final[str] = (
    "FrozenContractBeforeReaders: العقدُ يصف المجالَ والامتحانَ ويُجمَّد قبل أن "
    "يوجد خصمٌ أصلًا؛ فلا يحمل هويّةَ قارئٍ ولا ينتظره، وربطُ القرّاء يقع في "
    "طبقة التقييم بعده لا فيه"
)

THE_FIBER_DEFERS_ITS_RANK_TO_AN_EXTERNAL_AUTHORITY: Final[str] = (
    "TheFiberDefersItsRankToAnExternalAuthority: الليفُ يحمل مرجعَ دليله وسقفَ "
    "رتبته إحالةً، ولا يُنشئ سلّمَ رتبٍ ثانيًا بجانب سلطة الرتب في المشروع؛ "
    "فنظاما رتبٍ متوازيان ينحرفان"
)

AN_ADAPTER_FLOWS_INTO_THE_FIBER_NOT_THE_REVERSE: Final[str] = (
    "AnAdapterFlowsIntoTheFiberNotTheReverse: مادّةُ مجالٍ بعينه تدخل عبر "
    "مُحوِّلٍ خارج هذه الطبقة، ولا تستورد الطبقةُ مجالًا ولا تُنسَخ مادّتُه "
    "إليها؛ فالنسخُ يُنشئ مصدرَ حقيقةٍ ثانيًا ينحرف عن أصله"
)

OBSERVED_DOMINANCE_IS_BOUNDED_BY_ITS_FROZEN_DOMAIN: Final[str] = (
    "ObservedDominanceWithinFrozenDomain: أقصى ما تُنتِجه مقارنةٌ لاحقةٌ سيطرةٌ "
    "مرصودةٌ داخل مجالٍ مُجمَّدٍ بعينه؛ ولا يصير ذلك حكمًا بأنّ نظامًا أقوى "
    "مطلقًا، ولا يُعمَّم على مجالٍ لم يُستقرَأ"
)

PRIOR_FIBER_LAWS: Final[tuple[str, ...]] = (
    NO_POSITIVE_ROLE_FROM_A_NEUTRAL_FIBER_INPUT,
    THE_THREE_FIBERS_ARE_PARALLEL_NOT_SEQUENTIAL,
    NO_SYSTEM_DEFINES_THE_CONTRACT_IT_IS_READ_BY,
    A_COMMITTED_GOLD_IS_BOUND_NOT_SHIPPED,
    DIGEST_ONLY_IS_NOT_CRYPTOGRAPHICALLY_HIDDEN_GOLD,
    FROZEN_CONTRACT_BEFORE_READERS,
    THE_FIBER_DEFERS_ITS_RANK_TO_AN_EXTERNAL_AUTHORITY,
    AN_ADAPTER_FLOWS_INTO_THE_FIBER_NOT_THE_REVERSE,
    OBSERVED_DOMINANCE_IS_BOUNDED_BY_ITS_FROZEN_DOMAIN,
)


def _refuse_a_duplicated_law() -> None:
    """ارفض عند الاستيراد قانونًا مُكرَّرًا أو فارغًا."""

    if len(set(PRIOR_FIBER_LAWS)) != len(PRIOR_FIBER_LAWS):
        raise PriorFiberError("قانونٌ مُكرَّرٌ في مجموعة قوانين الليف")
    for law in PRIOR_FIBER_LAWS:
        if not law.strip():
            raise PriorFiberError("قانونٌ بلا نصّ")


_refuse_a_duplicated_law()
