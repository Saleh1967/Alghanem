"""تجميدُ قانون الوقف: انغلاقُ الوحدة الإسنادية، وثلاثةُ أنماطٍ وثلاثُ منازل.

**الوقفُ هنا نحويٌّ لا صوتيّ**: نقطةُ اكتمال الوحدة الإسنادية وانغلاقِها، لا
موضعُ سكوتٍ في التلاوة. والقانونُ الصوتيُّ المُسجَّل في
`ibtida_wasl_waqf_registration` بابٌ آخرُ بلفظٍ واحد، ولا يُقاس أحدُهما بالآخر
(`THE_PHONETIC_WAQF_IS_NOT_THIS_WAQF`).

**والقانونُ المُقترَح**: *تنغلق الوحدةُ الإسنادية حين يكتمل طرفاها، ولا تنغلق
شبهُ الجملة أبدًا بذاتها.* ولكلّ وحدةٍ ثلاثُ منازلَ لا يجمعها صفر: **مُغلَقة**
إن كان طرفاها موسومَين في آيتها، و**مفتوحة** إن وُسِم طرفٌ واحدٌ فقط،
و**تابعة** لشبه الجملة التي لا تُغلِق بذاتها.

**والمقامُ مُعلَنٌ لا مُفترَض**: `ADenominatorIsDeclaredNotAssumed` مستوردةً من
`irab_operator_preregistration`. ومقامُ هذه الأداة **المفاتيحُ** — الجذوعُ التي
تحمل قيمةَ طرفٍ فاتحٍ مُجمَّدة — لا الآياتُ ولا الجذوعُ كلُّها ولا «الجملُ في
القرآن». ومن قرأ عددَها حصرًا لجمل القرآن قرأ مقامًا غيرَ مقامه.

**وأخطرُ حدٍّ في هذه الأداة مكتوبٌ فيها لا خارجَها**
(`A_THIN_COLUMN_IS_NOT_A_THICK_ONE`): طرفا الجملة الاسمية يُقرآن من عمودين
مختلفَي التغطية — `Syntactic_Role` (٧٦٫٣٦٪ من المقاطع، ٩٩٫٦٨٪ من الجذوع) فيه
«مبتدأ»، و`Phrasal_Function` (١٫٧٩٪) فيه «خبر» بأنواعه. فعددُ «المفتوحة» في
الاسمية **يُقرأ أوّلًا خلوَّ عمودٍ لا انفتاحَ جملة**، ولا يُخرَج منه معدَّلُ
انغلاقٍ يُقرأ خبرًا عن العربية. وهذا بعينه الاعتراضُ الذي رُفِع به `Phrase`
(١٫٨٠٪)، فلا يُرفَع بأحدهما ويُبنى على الآخر صامتًا.

**والكواشفُ تُفرَّق بعمودها لا باسمها وحدَه**
(`A_VALUE_WITHOUT_ITS_COLUMN_IS_TWO_VALUES`): «فاعل» في `Syntactic_Role` عددُه
١٠٬٤٨٣، و«فاعل» في `Phrasal_Function` عددُه ١؛ وهما قيمتان لا قيمةٌ واحدةٌ
برقمين. ومثلُهما «نائب فاعل»: المُجمَّدُ في هذه الشجرة ٥٧ في `Phrasal_Function`
وحدَه، وكلُّ عددٍ آخرَ له عددٌ لعمودٍ آخرَ لم يُسَمَّ بعد.

**ولا كاشفَ بعددٍ لم يُجمَّد** (`AN_UNFROZEN_VALUE_IS_NOT_A_DETECTOR`): وصلت
أسماءُ «ظرف زمان» و«ظرف مكان» و«اسم ناسخ» بأعدادٍ بلا أعمدةٍ مُسمّاة، ولم
تُجمَّد صياغتُها الحرفيّةُ في `irab_column_preregistration`؛ فتُسجَّل هنا
**مُعلَّقةً باسمها** ولا تدخل عدًّا. وإدخالُها بصياغةٍ تُخمَّن يجعل الجوابَ
«ليست من قيم هذا العمود» صفرًا صامتًا، وذاك ما يمنعه
`AClaimedValueAbsentIsNotAZeroCount`.

**ولا عمودَ يقول «هنا انغلقت الجملة»**
(`A_CLOSURE_IS_INFERRED_FROM_NEIGHBOURHOOD_NOT_TAGGED`): الإغلاقُ استنتاجٌ من
حضور الطرفين داخل الآية، وحدُّ الآية **ليس حدَّ الجملة**
(`A_VERSE_BOUNDARY_IS_NOT_A_SENTENCE_BOUNDARY`) — فالجملةُ تمتدّ عبر آيتين،
والآيةُ تحوي جملًا؛ وكلُّ قياسٍ هنا يستعمل الآيةَ وحدةً، فهذا حدُّه لا حدُّ
العربية.

وهذه الوحدة تجميدٌ لا سلطة: لا ولادةَ فيها، ولا حكمَ ولادة، ولا تجميدَ `E0`،
ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه. ولا حقلَ نتيجةٍ ولا حقلَ
دقّةٍ فيها، وحارسٌ في آخرها يرفض إضافةَ أيّهما.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from .irab_column_census import SURA_COLUMN, VERSE_COLUMN
from .irab_column_preregistration import (
    A_THINLY_COVERED_COLUMN_IS_NOT_A_CENSUS_OF_ARABIC_NOTE,
    ANCHOR_COLUMN_NAME,
    ARRIVING_COLUMN_COVERAGE,
    PHRASAL_FUNCTION_COLUMN,
    SEGMENT_INDEX_COLUMN_NAME,
    STANDING,
    SYNTACTIC_ROLE_COLUMN,
    THE_FIGURES_ARRIVED_FROM_THE_HOLDER_OF_THE_BYTES_NOTE,
    THIS_REGISTRATION_IS_NOT_PRIOR_TO_THE_NUMBER_NOTE,
    WORD_KEY_COLUMN_NAME,
    ArrivingIrabFigure,
    RegistrationStanding,
    figures_for_column,
)
from .irab_operator_preregistration import (
    A_DENOMINATOR_IS_DECLARED_NOT_ASSUMED_NOTE,
    A_RELATION_NEEDS_TWO_PRESENT_TERMS_NOTE,
    COMPLETE_INDUCTION_IS_CORPUS_BOUNDED_NOTE,
    STEM_MORPH_TYPE,
    THE_PHRASE_COLUMN_IS_NOT_USED_NOTE,
    DeclaredDenominator,
)

__all__ = [
    "A_CLOSURE_IS_INFERRED_FROM_NEIGHBOURHOOD_NOT_TAGGED_NOTE",
    "A_PARTIAL_SCAN_FORBIDS_A_TOTAL_DENIAL_NOTE",
    "A_PHRASE_IS_NOT_A_CLAUSE_NOTE",
    "A_THIN_COLUMN_IS_NOT_A_THICK_ONE_NOTE",
    "A_VALUE_WITHOUT_ITS_COLUMN_IS_TWO_VALUES_NOTE",
    "AN_UNFROZEN_VALUE_IS_NOT_A_DETECTOR_NOTE",
    "A_VERSE_BOUNDARY_IS_NOT_A_SENTENCE_BOUNDARY_NOTE",
    "CLOSURE_CENSUS_COLUMNS",
    "CLOSURE_DETECTORS",
    "KEY_DENOMINATOR",
    "NOMINAL_TERM_COVERAGE_GAP",
    "PRE_MEASUREMENT_EXPECTATION",
    "SUSPENDED_ARRIVING_VALUES",
    "THE_PHONETIC_WAQF_IS_NOT_THIS_WAQF_NOTE",
    "WAQF_CLOSURE_PREREGISTRATION_DIGEST",
    "WAQF_CLOSURE_PREREGISTRATION_NAMED_RESIDUALS",
    "ClauseKind",
    "ClosureDetector",
    "ClosureStanding",
    "CoverageGap",
    "SuspendedArrivingValue",
    "TermSide",
    "WaqfClosurePreregistrationError",
    "closing_detectors_for",
    "detector_for",
    "opening_detectors_for",
    "waqf_closure_preregistration_digest",
]


class WaqfClosurePreregistrationError(ValueError):
    """رُوجِع التجميدُ بما لا يقوم به؛ ولا يُحمَل على أقرب حالةٍ مقبولة."""


# --- النصوصُ المُسمّاة: حدودٌ تُكتَب قبل أن تُخالَف -----------------------------


A_CLOSURE_IS_INFERRED_FROM_NEIGHBOURHOOD_NOT_TAGGED_NOTE: Final[str] = (
    "AClosureIsInferredFromNeighbourhoodNotTagged: لا عمودَ في المدوَّنة يقول "
    "«هنا انغلقت الجملة»؛ والإغلاقُ استنتاجٌ من حضور طرفَين موسومَين داخل "
    "الآية الواحدة، فهو قياسٌ لقاعدة الجوار المُجمَّدة هنا لا قراءةٌ لوسمٍ "
    "صريحٍ في البايتات"
)

A_VERSE_BOUNDARY_IS_NOT_A_SENTENCE_BOUNDARY_NOTE: Final[str] = (
    "AVerseBoundaryIsNotASentenceBoundary: حدُّ الآية ليس حدَّ الجملة — "
    "فالجملةُ تمتدّ عبر آيتين، والآيةُ تحوي جملًا؛ وكلُّ قياسٍ في هذه الأداة "
    "يستعمل الآيةَ وحدةً، فالمفتوحةُ قد تكون مُغلَقةً في الآية التالية، "
    "وهذا أخطرُ حدودها لأنّه يمسّ كلَّ رقمٍ تُخرِجه"
)

A_PHRASE_IS_NOT_A_CLAUSE_NOTE: Final[str] = (
    "APhraseIsNotAClause: شبهُ الجملة — جارٌّ ومجرور أو ظرف — لا تنغلق بذاتها "
    "لأنّها تحتاج متعلَّقًا؛ فمنزلتُها «تابعة» في كلّ حال، ولا تُعَدُّ "
    "مُغلَقةً ولو حضر متعلَّقٌ موسومٌ في آيتها. وحضورُ المتعلَّق يُعَدُّ في "
    "حقلٍ باسمه ولا يُرقّي المنزلة"
)

A_THIN_COLUMN_IS_NOT_A_THICK_ONE_NOTE: Final[str] = (
    "AThinColumnIsNotAThickOne: طرفا الجملة الاسمية يُقرآن من عمودَين "
    "مختلفَي التغطية — «مبتدأ» في `Syntactic_Role` و«خبر» بأنواعه في "
    "`Phrasal_Function` الذي تغطيتُه ١٫٧٩٪ — فعددُ «المفتوحة» في الاسمية "
    "يُقرأ أوّلًا خلوَّ عمودٍ لا انفتاحَ جملة، ولا يُخرَج منه معدَّلُ "
    "انغلاقٍ خبرًا عن العربية. " + A_THINLY_COVERED_COLUMN_IS_NOT_A_CENSUS_OF_ARABIC_NOTE
)

A_VALUE_WITHOUT_ITS_COLUMN_IS_TWO_VALUES_NOTE: Final[str] = (
    "AValueWithoutItsColumnIsTwoValues: «فاعل» في `Syntactic_Role` عددُه "
    "١٠٬٤٨٣ و«فاعل» في `Phrasal_Function` عددُه ١، فهما قيمتان بعمودين لا "
    "قيمةٌ واحدةٌ برقمين؛ وكلُّ كاشفٍ هنا يُعرَّف بزوج (العمود، القيمة) ولا "
    "يُعرَّف بالقيمة وحدَها"
)

AN_UNFROZEN_VALUE_IS_NOT_A_DETECTOR_NOTE: Final[str] = (
    "AnUnfrozenValueIsNotADetector: وصلت أسماءُ قيمٍ بأعدادٍ بلا أعمدةٍ "
    "مُسمّاة ولم تُجمَّد صياغتُها الحرفيّةُ في `irab_column_preregistration`، "
    "فتُسجَّل هنا مُعلَّقةً ولا تدخل عدًّا؛ وإدخالُها بصياغةٍ تُخمَّن يجعل "
    "جوابَ «ليست من قيم هذا العمود» صفرًا صامتًا"
)

A_PARTIAL_SCAN_FORBIDS_A_TOTAL_DENIAL_NOTE: Final[str] = (
    "APartialScanForbidsATotalDenial: لا يُنفى وجودُ قيمةٍ في عمودٍ إلّا بعد "
    "المرور على قيمه كلِّها؛ وفحصُ بعضِها ثمّ النفيُ عن كلِّها استدلالٌ "
    "بالجزء على الكلّ، فتُخرِج هذه الأداةُ مسحَ القيم تامًّا مع كلّ نفي"
)

THE_PHONETIC_WAQF_IS_NOT_THIS_WAQF_NOTE: Final[str] = (
    "ThePhoneticWaqfIsNotThisWaqf: الوقفُ المُسجَّل في "
    "`ibtida_wasl_waqf_registration` تسكينُ الحالة الأخيرة في التلاوة، "
    "والوقفُ هنا انغلاقُ وحدةٍ إسنادية؛ ولفظٌ واحدٌ لبابين لا يجعلهما بابًا "
    "واحدًا، ولا يُقاس أحدُهما بالآخر ولا يُصدَّق به"
)


WAQF_CLOSURE_PREREGISTRATION_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "AClosureIsInferredFromNeighbourhoodNotTagged": (
        A_CLOSURE_IS_INFERRED_FROM_NEIGHBOURHOOD_NOT_TAGGED_NOTE
    ),
    "AVerseBoundaryIsNotASentenceBoundary": (
        A_VERSE_BOUNDARY_IS_NOT_A_SENTENCE_BOUNDARY_NOTE
    ),
    "APhraseIsNotAClause": A_PHRASE_IS_NOT_A_CLAUSE_NOTE,
    "AThinColumnIsNotAThickOne": A_THIN_COLUMN_IS_NOT_A_THICK_ONE_NOTE,
    "AValueWithoutItsColumnIsTwoValues": A_VALUE_WITHOUT_ITS_COLUMN_IS_TWO_VALUES_NOTE,
    "AnUnfrozenValueIsNotADetector": AN_UNFROZEN_VALUE_IS_NOT_A_DETECTOR_NOTE,
    "APartialScanForbidsATotalDenial": A_PARTIAL_SCAN_FORBIDS_A_TOTAL_DENIAL_NOTE,
    "ThePhoneticWaqfIsNotThisWaqf": THE_PHONETIC_WAQF_IS_NOT_THIS_WAQF_NOTE,
    "ADenominatorIsDeclaredNotAssumed": A_DENOMINATOR_IS_DECLARED_NOT_ASSUMED_NOTE,
    "ARelationNeedsTwoPresentTerms": A_RELATION_NEEDS_TWO_PRESENT_TERMS_NOTE,
    "ThePhraseColumnIsNotUsed": THE_PHRASE_COLUMN_IS_NOT_USED_NOTE,
    "CompleteInductionIsCorpusBounded": COMPLETE_INDUCTION_IS_CORPUS_BOUNDED_NOTE,
    "ThisRegistrationIsNotPriorToTheNumber": (
        THIS_REGISTRATION_IS_NOT_PRIOR_TO_THE_NUMBER_NOTE
    ),
    "TheFiguresArrivedFromTheHolderOfTheBytes": (
        THE_FIGURES_ARRIVED_FROM_THE_HOLDER_OF_THE_BYTES_NOTE
    ),
}


# --- الأنماطُ والمنازلُ والأطراف ------------------------------------------------


class ClauseKind(Enum):
    """نمطُ الوحدة؛ ثلاثةٌ وبابٌ رابعٌ مُعلَنٌ لا يُبتلَع فيه فرق.

    والمانعيةُ الجامعة **على زوج (العمود، القيمة)** لا على الآية: الآيةُ
    الواحدة تحوي الأنماطَ الثلاثة معًا، فلا تُسنُّ المانعيةُ عليها.
    """

    NOMINAL = "جملة_اسمية"
    VERBAL = "جملة_فعلية"
    PHRASE = "شبه_جملة"
    OUTSIDE_THE_DETECTORS = "خارج_الكواشف"


class TermSide(Enum):
    """طرفُ القيمة من الوحدة: فاتحٌ يُفتَح به الإسناد، أو مُغلِقٌ يكتمل به."""

    OPENING = "طرف_فاتح"
    CLOSING = "طرف_مُغلِق"


class ClosureStanding(Enum):
    """منزلةُ الوحدة؛ ثلاثتُها لا يجمعها صفرٌ واحد."""

    CLOSED = "مُغلَقة"
    OPEN = "مفتوحة"
    DEPENDENT = "تابعة"


# --- المقامُ المُعلَن ------------------------------------------------------------


KEY_DENOMINATOR: Final[DeclaredDenominator] = DeclaredDenominator(
    name="المفاتيح",
    column=SYNTACTIC_ROLE_COLUMN,
    value="قيمُ الأطراف الفاتحة المُجمَّدة",
    counting_rule=(
        "المفتاحُ: جذعٌ — `Morph_type` فيه مطابقٌ حرفيًّا لـ«Stem» — تحمل "
        "خليّتُه قيمةَ طرفٍ فاتحٍ مُجمَّدةً في كاشفٍ من `CLOSURE_DETECTORS`؛ "
        "والمقامُ المفاتيحُ وحدَها لا الآياتُ ولا الجذوعُ كلُّها ولا الجملُ "
        "في القرآن، فلكلّ مفتاحٍ منزلةٌ واحدةٌ من الثلاث"
    ),
)
"""مقامُ هذه الأداة منطوقًا بقاعدة حصره؛ ولا نسبةَ تخرج منها بغيره."""


@dataclass(frozen=True, slots=True)
class CoverageGap:
    """فرقُ تغطيةٍ بين عمودَي طرفَين، مُشتقًّا من `ARRIVING_COLUMN_COVERAGE`.

    ولا تُكتَب نسبةٌ هنا بيدٍ: تُقرأ من موضع تجميدها، فرقمٌ مُجمَّدٌ مرّتين
    رقمان يفترقان بلا أن يفشل أحدُهما.
    """

    opening_column: str
    opening_percentage: str
    closing_column: str
    closing_percentage: str

    @property
    def opening_exceeds_closing(self) -> bool:
        """أعمودُ الطرف الفاتح أكثفُ من عمود الطرف المُغلِق؟"""

        return float(self.opening_percentage) > float(self.closing_percentage)


def _declared_coverage(column: str) -> str:
    """نسبةُ امتلاء عمودٍ كما جُمِّدت؛ وغيابُها يُوقِف البناء ولا يُقدَّر."""

    for coverage in ARRIVING_COLUMN_COVERAGE:
        if coverage.column == column:
            return coverage.declared_percentage
    raise WaqfClosurePreregistrationError(
        f"لا تغطيةَ مُجمَّدةً للعمود «{column}»؛ ولا تُقدَّر نسبةٌ لعمودٍ لم "
        "تصل تغطيتُه. " + A_THIN_COLUMN_IS_NOT_A_THICK_ONE_NOTE
    )


NOMINAL_TERM_COVERAGE_GAP: Final[CoverageGap] = CoverageGap(
    opening_column=SYNTACTIC_ROLE_COLUMN,
    opening_percentage=_declared_coverage(SYNTACTIC_ROLE_COLUMN),
    closing_column=PHRASAL_FUNCTION_COLUMN,
    closing_percentage=_declared_coverage(PHRASAL_FUNCTION_COLUMN),
)
"""٧٦٫٣٦٣١٪ مقابل ١٫٧٩٪: الفرقُ الذي يُقرأ به عددُ «المفتوحة» في الاسمية."""


# --- الكواشفُ: زوجُ (عمودٍ، قيمة) بعددٍ مستوردٍ لا مكتوبٍ ثانية -------------------


@dataclass(frozen=True, slots=True)
class ClosureDetector:
    """كاشفٌ مُجمَّد: عمودُه وقيمتُه ونمطُه وطرفُه وعددُه المُدَّعى.

    والعددُ **مستوردٌ** من `irab_column_preregistration`: لا يُكتَب رقمٌ ثانٍ
    لقيمةٍ مُجمَّدةٍ هناك.
    """

    column: str
    value: str
    kind: ClauseKind
    side: TermSide
    claimed_segment_count: int

    def __post_init__(self) -> None:
        for text, label in ((self.column, "اسمُ العمود"), (self.value, "قيمةُ الكاشف")):
            if not isinstance(text, str) or not text.strip():
                raise WaqfClosurePreregistrationError(f"{label} نصٌّ غير فارغ.")
        if not isinstance(self.kind, ClauseKind):
            raise WaqfClosurePreregistrationError("لكلّ كاشفٍ نمطٌ مُسمًّى.")
        if self.kind is ClauseKind.OUTSIDE_THE_DETECTORS:
            raise WaqfClosurePreregistrationError(
                "«خارج الكواشف» جوابُ قيمةٍ لم تُجمَّد، فلا يُجمَّد بها كاشف."
            )
        if not isinstance(self.side, TermSide):
            raise WaqfClosurePreregistrationError("لكلّ كاشفٍ طرفٌ مُسمًّى.")
        if self.kind is ClauseKind.PHRASE and self.side is TermSide.CLOSING:
            raise WaqfClosurePreregistrationError(
                "شبهُ الجملة لا طرفَ مُغلِقَ لها. " + A_PHRASE_IS_NOT_A_CLAUSE_NOTE
            )
        if (
            isinstance(self.claimed_segment_count, bool)
            or not isinstance(self.claimed_segment_count, int)
            or self.claimed_segment_count < 0
        ):
            raise WaqfClosurePreregistrationError("العددُ المُدَّعى عددٌ صحيحٌ غيرُ سالب.")

    @property
    def key(self) -> tuple[str, str]:
        """مفتاحُ الكاشف: زوجُ (العمود، القيمة). `AValueWithoutItsColumnIsTwoValues`."""

        return (self.column, self.value)


_DETECTOR_PLAN: Final[tuple[tuple[str, str, ClauseKind, TermSide], ...]] = (
    (SYNTACTIC_ROLE_COLUMN, "مبتدأ", ClauseKind.NOMINAL, TermSide.OPENING),
    (PHRASAL_FUNCTION_COLUMN, "خبر", ClauseKind.NOMINAL, TermSide.CLOSING),
    (PHRASAL_FUNCTION_COLUMN, "خبر حرف ناسخ", ClauseKind.NOMINAL, TermSide.CLOSING),
    (PHRASAL_FUNCTION_COLUMN, "خبر فعل ناسخ", ClauseKind.NOMINAL, TermSide.CLOSING),
    (
        PHRASAL_FUNCTION_COLUMN,
        "خبر لا النافية للجنس",
        ClauseKind.NOMINAL,
        TermSide.CLOSING,
    ),
    (SYNTACTIC_ROLE_COLUMN, "فعل ماضٍ", ClauseKind.VERBAL, TermSide.OPENING),
    (SYNTACTIC_ROLE_COLUMN, "فعل مضارع", ClauseKind.VERBAL, TermSide.OPENING),
    (SYNTACTIC_ROLE_COLUMN, "فاعل", ClauseKind.VERBAL, TermSide.CLOSING),
    (PHRASAL_FUNCTION_COLUMN, "نائب فاعل", ClauseKind.VERBAL, TermSide.CLOSING),
    (SYNTACTIC_ROLE_COLUMN, "حرف جر", ClauseKind.PHRASE, TermSide.OPENING),
)
"""عشرةُ كواشفَ بأزواجها؛ وكلُّها قيمٌ مُجمَّدةٌ صياغتُها في التسجيل الأوّل."""


def _frozen_figure(column: str, value: str) -> ArrivingIrabFigure:
    """الرقمُ المُجمَّد لزوج (عمودٍ، قيمة)؛ وغيابُه يُوقِف البناء."""

    for figure in figures_for_column(column):
        if figure.value == value:
            return figure
    raise WaqfClosurePreregistrationError(
        f"لا رقمَ مُجمَّدًا للقيمة «{value}» في العمود «{column}»؛ ولا يُكتَب "
        "هنا رقمٌ ثانٍ لها. " + AN_UNFROZEN_VALUE_IS_NOT_A_DETECTOR_NOTE
    )


def _build_detectors() -> tuple[ClosureDetector, ...]:
    detectors: list[ClosureDetector] = []
    seen: set[tuple[str, str]] = set()
    for column, value, kind, side in _DETECTOR_PLAN:
        figure = _frozen_figure(column, value)
        detector = ClosureDetector(
            column=column,
            value=value,
            kind=kind,
            side=side,
            claimed_segment_count=figure.claimed_count,
        )
        if detector.key in seen:
            raise WaqfClosurePreregistrationError(
                f"كاشفٌ مكرَّرٌ لزوج {detector.key}؛ والفئاتُ مانعةٌ جامعة."
            )
        seen.add(detector.key)
        detectors.append(detector)
    return tuple(detectors)


CLOSURE_DETECTORS: Final[tuple[ClosureDetector, ...]] = _build_detectors()
"""الكواشفُ العشرةُ بأعدادها المستوردة؛ ولكلّ زوجٍ نمطٌ واحدٌ وطرفٌ واحد."""


def detector_for(column: str, value: str) -> ClosureDetector | None:
    """الكاشفُ بزوجه؛ و`None` جوابُ زوجٍ لم يُجمَّد لا جوابُ غيابه من المدوَّنة."""

    for detector in CLOSURE_DETECTORS:
        if detector.column == column and detector.value == value.strip():
            return detector
    return None


def opening_detectors_for(kind: ClauseKind) -> tuple[ClosureDetector, ...]:
    """كواشفُ الطرف الفاتح لنمطٍ بعينه."""

    return tuple(
        detector
        for detector in CLOSURE_DETECTORS
        if detector.kind is kind and detector.side is TermSide.OPENING
    )


def closing_detectors_for(kind: ClauseKind) -> tuple[ClosureDetector, ...]:
    """كواشفُ الطرف المُغلِق لنمطٍ بعينه؛ وشبهُ الجملة بلا واحدٍ منها."""

    return tuple(
        detector
        for detector in CLOSURE_DETECTORS
        if detector.kind is kind and detector.side is TermSide.CLOSING
    )


# --- قيمٌ وصلت بلا عمودٍ مُسمًّى: تُسجَّل ولا تُعَدّ ------------------------------


@dataclass(frozen=True, slots=True)
class SuspendedArrivingValue:
    """اسمُ قيمةٍ وصل بعددٍ بلا عمودٍ مُسمًّى؛ مُسجَّلٌ مُعلَّقٌ لا كاشف."""

    name: str
    claimed_count: int
    kind: ClauseKind
    reason: str

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise WaqfClosurePreregistrationError("اسمُ القيمة نصٌّ غير فارغ.")
        if not isinstance(self.kind, ClauseKind):
            raise WaqfClosurePreregistrationError("لكلّ قيمةٍ مُعلَّقةٍ نمطٌ مُسمًّى.")
        if (
            isinstance(self.claimed_count, bool)
            or not isinstance(self.claimed_count, int)
            or self.claimed_count < 0
        ):
            raise WaqfClosurePreregistrationError("العددُ الواصلُ عددٌ صحيحٌ غيرُ سالب.")
        if not isinstance(self.reason, str) or not self.reason.strip():
            raise WaqfClosurePreregistrationError(
                "تعليقُ قيمةٍ بلا علّةٍ مكتوبةٍ إسقاطٌ صامت. "
                + AN_UNFROZEN_VALUE_IS_NOT_A_DETECTOR_NOTE
            )


SUSPENDED_ARRIVING_VALUES: Final[tuple[SuspendedArrivingValue, ...]] = (
    SuspendedArrivingValue(
        name="ظرف زمان",
        claimed_count=1_426,
        kind=ClauseKind.PHRASE,
        reason=(
            "وصل العددُ بلا عمودٍ مُسمًّى، ولم تُجمَّد صياغتُه الحرفيّةُ في "
            "التسجيل الأوّل؛ فلا يُبنى به كاشفٌ يُقرأ غيابُه صفرًا"
        ),
    ),
    SuspendedArrivingValue(
        name="ظرف مكان",
        claimed_count=758,
        kind=ClauseKind.PHRASE,
        reason=(
            "كسابقه: عددٌ بلا عمود، وصياغةٌ غيرُ مُجمَّدة؛ وشبهُ الجملة "
            "تُقاس هنا بالجارّ والمجرور وحدَه حتى يصل عمودُ الظرف"
        ),
    ),
    SuspendedArrivingValue(
        name="نائب فاعل",
        claimed_count=747,
        kind=ClauseKind.VERBAL,
        reason=(
            "المُجمَّدُ في هذه الشجرة «نائب فاعل» في `Phrasal_Function` "
            "عددُه ٥٧؛ و٧٤٧ عددٌ لعمودٍ آخرَ لم يُسَمَّ، فهما رقمان لقيمتين "
            "لا رقمان متنازعان لقيمةٍ واحدة. "
            + A_VALUE_WITHOUT_ITS_COLUMN_IS_TWO_VALUES_NOTE
        ),
    ),
    SuspendedArrivingValue(
        name="اسم ناسخ",
        claimed_count=0,
        kind=ClauseKind.NOMINAL,
        reason=(
            "وصل فارقُ «اسم الناسخ عن خبره» (١٬١٥٧) ولم يصل عددُ اسم الناسخ "
            "نفسِه ولا اسمُ عموده؛ وفارقٌ بلا طرفَيه لا يُشتَقُّ منه عدد، "
            "فيبقى المكانُ خاليًا مُسمًّى لا يُملأ بصفرٍ ولا بتقدير"
        ),
    ),
)
"""أربعُ قيمٍ واصلةٍ مُعلَّقةٍ بأسمائها؛ وعددُ «اسم ناسخ» صفرٌ بمعنى «لم يصل».

و«صفرٌ بمعنى لم يصل» إنّما جاز هنا لأنّ هذه البنيةَ **لا تدخل عدًّا** أصلًا:
علّتُها مكتوبةٌ في `reason`، وحقلُها لا يُجمَع مع رقمٍ مقيس.
"""


# --- التوقّعُ، والأعمدة، والبصمة -------------------------------------------------


CLOSURE_CENSUS_COLUMNS: Final[tuple[str, ...]] = (
    ANCHOR_COLUMN_NAME,
    SYNTACTIC_ROLE_COLUMN,
    PHRASAL_FUNCTION_COLUMN,
    SURA_COLUMN,
    VERSE_COLUMN,
    WORD_KEY_COLUMN_NAME,
    SEGMENT_INDEX_COLUMN_NAME,
)
"""الأعمدةُ السبعةُ التي يقوم بها القياس؛ وغيابُ واحدٍ منها يُوقِف العدّ.

و`Phrase` ليس فيها عمدًا: `ThePhraseColumnIsNotUsed`.
"""


PRE_MEASUREMENT_EXPECTATION: Final[str] = (
    "PreMeasurementExpectation: انغلاقُ الوحدات لم يُقَس بعدُ — لا هنا ولا عند "
    "حائز البايتات — وهو ثلاثةُ أمورٍ قابلةٍ للتكذيب. **أوّلًا**: يُتوقَّع أن "
    "تكون مفاتيحُ الجملة الفعلية أكثرَ من مفاتيح الاسمية على مقام المفاتيح؛ "
    "وهو الادّعاءُ التراثيُّ الشائع، ويُختبَر بمقامه لا بعمود `Phrase`. "
    "**ثانيًا**: يُتوقَّع أن تكون حصّةُ «المفتوحة» في الاسمية أكبرَ منها في "
    "الفعلية بفارقٍ يقارب فارقَ تغطية العمودين لا فارقًا في العربية؛ فإن "
    "تساوت الحصّتان كُذِّب التوقّع، وإن تفاوتتا فالتفاوتُ **لا يُقرأ بنيةً** "
    "حتى يأتي عمودٌ أكثفُ لطرف الخبر. **ثالثًا**: يُتوقَّع ألّا تُغلَق شبهُ "
    "جملةٍ واحدةٌ البتّة، لأنّ المنزلةَ مسنونةٌ لا مقيسة — وهذا التوقّعُ "
    "الثالثُ **ليس اكتشافًا** بل قراءةٌ للتعريف، ويُكتَب ليُرى أنّه كذلك. "
    + A_THIN_COLUMN_IS_NOT_A_THICK_ONE_NOTE
)


def waqf_closure_preregistration_digest() -> str:
    """بصمةُ محتوى التجميد؛ فتبديلُ كاشفٍ أو مقامٍ أو نصٍّ تُغيّرها."""

    return canonical_digest(
        canonical_bytes(
            {
                "standing": STANDING.value,
                "anchor_value": STEM_MORPH_TYPE,
                "denominator": [
                    KEY_DENOMINATOR.name,
                    KEY_DENOMINATOR.column,
                    KEY_DENOMINATOR.value,
                    KEY_DENOMINATOR.counting_rule,
                ],
                "kinds": {kind.name: kind.value for kind in ClauseKind},
                "standings": {
                    standing.name: standing.value for standing in ClosureStanding
                },
                "detectors": [
                    [
                        detector.column,
                        detector.value,
                        detector.kind.value,
                        detector.side.value,
                        detector.claimed_segment_count,
                    ]
                    for detector in CLOSURE_DETECTORS
                ],
                "suspended": [
                    [value.name, value.claimed_count, value.kind.value, value.reason]
                    for value in SUSPENDED_ARRIVING_VALUES
                ],
                "coverage_gap": [
                    NOMINAL_TERM_COVERAGE_GAP.opening_column,
                    NOMINAL_TERM_COVERAGE_GAP.opening_percentage,
                    NOMINAL_TERM_COVERAGE_GAP.closing_column,
                    NOMINAL_TERM_COVERAGE_GAP.closing_percentage,
                ],
                "columns": list(CLOSURE_CENSUS_COLUMNS),
                "expectation": PRE_MEASUREMENT_EXPECTATION,
                "residuals": sorted(WAQF_CLOSURE_PREREGISTRATION_NAMED_RESIDUALS),
            }
        )
    )


WAQF_CLOSURE_PREREGISTRATION_DIGEST: Final[str] = waqf_closure_preregistration_digest()
"""بصمةُ التجميد مُشتقّةً من محتواه؛ ولا تُكتَب بيدٍ فتُصادِق على ما لم يُبصَّم."""


# --- حارسا الوحدة: لا حقلَ نتيجةٍ ولا حقلَ دقّة ---------------------------------


_FORBIDDEN_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "outcome",
    "result",
    "observed",
    "measured",
    "rederived",
    "verdict",
    "birth",
    "accuracy",
    "precision",
    "confidence",
)
"""«دقّة» و«ثقة» زِيدتا على المنوال الأوّل: لا تُرقَّم دقّةُ علاقةٍ بلا وسمٍ رابط."""


def _assert_no_outcome_or_accuracy_field() -> None:
    """احرسْ خلوَّ التجميد من حقلِ نتيجةٍ أو دقّةٍ؛ والقياسُ موضعُه وحدةُ القياس."""

    for dataclass_type in (
        CoverageGap,
        ClosureDetector,
        SuspendedArrivingValue,
    ):
        for field in fields(dataclass_type):
            lowered = field.name.lower()
            for marker in _FORBIDDEN_FIELD_MARKERS:
                if marker in lowered:
                    raise WaqfClosurePreregistrationError(
                        f"حقلٌ ممنوعٌ في وحدة تجميد: {dataclass_type.__name__}."
                        f"{field.name}؛ ولا تُرقَّم دقّةُ علاقةٍ بلا وسمٍ رابط."
                    )


_assert_no_outcome_or_accuracy_field()


if STANDING is not RegistrationStanding.FORMULATED_AFTER_THE_NUMBER:  # pragma: no cover
    raise WaqfClosurePreregistrationError(
        "منزلةُ هذا التجميد `مُصاغ_بعد_الرقم`: وصلت أعدادُ القيم قبل صوغ "
        "قواعده. " + THIS_REGISTRATION_IS_NOT_PRIOR_TO_THE_NUMBER_NOTE
    )
