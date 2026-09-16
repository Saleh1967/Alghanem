"""تجميدُ مقامِ الابتداء وفئاتِ الجملة الاسمية قبل قياس العلاقة.

**السؤالُ الذي وُضِعت له هذه الوحدة**: قياسُ الابتداء **ليس قياسًا على كل
الجذوع** — تلك سبعةٌ وسبعون ألفًا وسبعُمئةٍ وسبعةٌ وتسعون، وأكثرُها لا يقبل
الابتداءَ أصلًا — ولا على المقاطع. والمقامُ الصحيحُ **المواضعُ التي تقبل
الابتداء**: مجموعُ المبتدأ والخبر معًا بقيمهما الثماني، وهو ١١٬٣٤٩ موضعًا.

`A_DENOMINATOR_IS_DECLARED_NOT_ASSUMED`: القانونُ مسنونٌ في
`irab_operator_preregistration` ويُستورَد هنا لا يُعاد سنُّه. وهذا مقامٌ
**ثالث**: ١١٬٣٤٩ و٧٧٬٧٩٧ و١٥٧٬٦٧٧ ثلاثةُ مقاماتٍ لا ثلاثةُ أرقامٍ متنازعة،
وكلُّ نسبةٍ تخرج من هذه الوحدة مقرونةٌ بمقامها نصًّا.

`THE_TWO_COLUMNS_ARE_NOT_ONE_FIGURE`: القيمُ الثماني هنا قيمُ
`Syntactic_Role`، وفي `Phrasal_Function` قيمٌ بأسماءٍ تشبهها وأعدادٍ أخرى —
«خبر ١٬٣٩٨» و«خبر حرف ناسخ ٧٨٣» و«خبر فعل ناسخ ٥٥١» — مُجمَّدةٌ هناك ولا
تُمَسّ. وعمودان ليسا رقمين متنازعين: هما وَسْمان بشرطين، ولا يُطرَح أحدُهما
من الآخر ولا يُصحَّح به.

`A_ROLE_TAG_IS_NOT_A_LINK`: وَسْمُ «خبر» يقول إنّ هذا خبرٌ، **لا إنّه خبرُ هذا
المبتدأ بعينه**؛ فليس في المدوَّنة عمودٌ يربط الطرفين. والربطُ في وحدة القياس
استنتاجٌ بالجوار داخل الآية، والجوارُ ليس إسنادًا.

`AN_INCHOATIVE_GOVERNOR_IS_SEMANTIC_NOT_LEXICAL`: الابتداءُ عاملٌ معنويٌّ لا
لفظيّ، ولذلك **لا يُطلَب له كاشفٌ في العمود**؛ و٣٥٫٤٪ من المبتدأ علامتُه
السكون لا علامةَ رفعٍ، فالحكمُ يثبت والعلامةُ غائبة.

`A_PARTIAL_SCAN_FORBIDS_A_TOTAL_DENIAL`: قانونٌ يُسَنُّ هنا أوّلَ مرّة، وسببُ
سنِّه مكتوبٌ في `THE_RETRACTED_TOTAL_DENIAL`: أُعلِن سابقًا في هذا المسار أنّ
الخبر غير موسوم، وكان خطأً ناتجًا عن فحص أعلى عشر قيمٍ ثمّ النفي الشامل.
وفحصُ طرفٍ من قائمةٍ لا يُجيز نفيًا عن كلِّها.

`A_RELATION_NEEDS_TWO_PRESENT_TERMS`: مستوردًا كما هو — وحدةُ العلاقة الآيةُ
الواحدة، فلا يُربَط مبتدأ في آيةٍ بخبرٍ في أخرى ليكتمل عدد. ولكلّ مبتدأٍ ثلاثُ
منازلَ لا يجمعها صفر: له خبرٌ موسومٌ في آيته، أو **لا خبر موسوم** فيُسمّى
بموضعه، أو له أكثرُ من خبرٍ مرشَّح.

`THIS_REGISTRATION_IS_NOT_PRIOR_TO_THE_NUMBER`: الأرقامُ الثمانيةُ وتفصيلُ
المبتدأ وصلت قبل صوغ هذه القواعد، فمنزلةُ التسجيل `مُصاغ_بعد_الرقم` مستوردةً
لا مُعادةً بيد. و`PRE_MEASUREMENT_EXPECTATION` وحدَه سابقٌ لِما يقابله:
اقترانُ المبتدأ بخبره لم يُقَس بعدُ لا هنا ولا عند حائز البايتات.

وهذه الوحدة تجميدٌ لا سلطة: لا ولادةَ فيها، ولا حكمَ ولادة، ولا تجميدَ `E0`،
ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه. ولا حقلَ نتيجةٍ فيها،
وحارسٌ في آخرها يرفض إضافتَه.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from .irab_column_census import SURA_COLUMN, VERSE_COLUMN
from .irab_column_preregistration import (
    A_CLAIMED_VALUE_ABSENT_IS_NOT_A_ZERO_COUNT_NOTE,
    AN_ANNOTATED_IRAB_IS_A_HUMAN_JUDGEMENT_NOTE,
    ANCHOR_COLUMN_NAME,
    ARRIVING_SEGMENT_TOTAL,
    CASE_MOOD_COLUMN,
    CASE_MOOD_MARKER_COLUMN,
    SEGMENT_INDEX_COLUMN_NAME,
    STANDING,
    SYNTACTIC_ROLE_COLUMN,
    THE_FIGURES_ARRIVED_FROM_THE_HOLDER_OF_THE_BYTES_NOTE,
    THIS_REGISTRATION_IS_NOT_PRIOR_TO_THE_NUMBER_NOTE,
    WORD_KEY_COLUMN_NAME,
    IrabCountingRule,
    IrabPreregistrationError,
    RegistrationStanding,
    figures_for_column,
)
from .irab_operator_preregistration import (
    A_COVERAGE_IS_NOT_CORRECTNESS_NOTE,
    A_DENOMINATOR_IS_DECLARED_NOT_ASSUMED_NOTE,
    A_RELATION_NEEDS_TWO_PRESENT_TERMS_NOTE,
    AN_UNDECLARED_SPLIT_IS_NOT_A_ZERO_NOTE,
    ARRIVING_STEM_TOTAL,
    COMPLETE_INDUCTION_IS_CORPUS_BOUNDED_NOTE,
    STEM_MORPH_TYPE,
    DeclaredDenominator,
)

__all__ = [
    "ARRIVING_INCHOATIVE_POSITIONS",
    "ARRIVING_MUBTADA_BREAKDOWN",
    "A_PARTIAL_SCAN_FORBIDS_A_TOTAL_DENIAL_NOTE",
    "A_ROLE_TAG_IS_NOT_A_LINK_NOTE",
    "AN_INCHOATIVE_GOVERNOR_IS_SEMANTIC_NOT_LEXICAL_NOTE",
    "DECLARED_GOVERNOR_VALUES",
    "IBTIDA_CENSUS_COLUMNS",
    "IBTIDA_PREREGISTRATION_DIGEST",
    "IBTIDA_PREREGISTRATION_NAMED_RESIDUALS",
    "INCHOATIVE_POSITION_DENOMINATOR",
    "INCHOATIVE_POSITION_TOTAL",
    "INCHOATIVE_POSITION_VALUES",
    "NAMED_RESIDUES",
    "PRE_MEASUREMENT_EXPECTATION",
    "THE_RETRACTED_TOTAL_DENIAL",
    "THE_TWO_COLUMNS_ARE_NOT_ONE_FIGURE_NOTE",
    "ArrivingInchoativeFigure",
    "ArrivingMubtadaBreakdown",
    "NamedResidue",
    "PositionSide",
    "ResidueDerivation",
    "SentenceClass",
    "class_of_value",
    "figure_for_value",
    "figures_of_class",
    "ibtida_preregistration_digest",
    "side_of_value",
]


A_ROLE_TAG_IS_NOT_A_LINK_NOTE: Final[str] = (
    "ARoleTagIsNotALink: وَسْمُ «خبر» يقول إنّ هذا خبرٌ لا إنّه خبرُ هذا "
    "المبتدأ بعينه؛ فليس في المدوَّنة عمودٌ يربط الطرفين، والربطُ استنتاجٌ "
    "بالجوار داخل الآية، والجوارُ ليس إسنادًا"
)

AN_INCHOATIVE_GOVERNOR_IS_SEMANTIC_NOT_LEXICAL_NOTE: Final[str] = (
    "AnInchoativeGovernorIsSemanticNotLexical: الابتداءُ عاملٌ معنويٌّ لا "
    "لفظيّ، فلا يُطلَب له كاشفٌ في العمود كما يُطلَب لحرف الجرّ؛ و٣٥٫٤٪ من "
    "المبتدأ علامتُه السكون لا علامةَ رفع، فالحكمُ يثبت والعلامةُ غائبة"
)

A_PARTIAL_SCAN_FORBIDS_A_TOTAL_DENIAL_NOTE: Final[str] = (
    "APartialScanForbidsATotalDenial: فحصُ أعلى عشر قيمٍ من عمودٍ لا يُجيز "
    "نفيًا عن قيمه كلِّها؛ والنفيُ الشاملُ يحتاج مسحًا شاملًا، وإلّا فجوابُه "
    "«لم يُفحَص» لا «غير موجود»"
)

THE_RETRACTED_TOTAL_DENIAL: Final[str] = (
    "TheRetractedTotalDenial: أُعلِن سابقًا في هذا المسار أنّ الخبر غير "
    "موسوم، وكان خطأً ناتجًا عن فحص أعلى عشر قيمٍ ثمّ النفي الشامل. والخبرُ "
    "موسومٌ بأربع قيم — خبر، وخبر حرف ناسخ، وخبر فعل ناسخ، ومبتدأ مؤخر. "
    "وحسابُ الأربع كما وصل لا كما يُشتهى: الثلاثُ الأُوَل ٢٬٠٥٧ و٩٢٩ و٧٩٩ "
    "مجموعُها ٣٬٧٨٥ بعينه، وبضمّ «مبتدأ مؤخر ٥٧٠» تصير ٤٬٣٥٥؛ فوصل العددُ "
    "٣٬٧٨٥ منسوبًا إلى أربعٍ وهو مجموعُ ثلاثٍ، ويُسجَّل الفرقُ كما وقع ولا "
    "يُحذَف طرفٌ ليستقيم الجمع. " + A_PARTIAL_SCAN_FORBIDS_A_TOTAL_DENIAL_NOTE
)

THE_TWO_COLUMNS_ARE_NOT_ONE_FIGURE_NOTE: Final[str] = (
    "TheTwoColumnsAreNotOneFigure: «خبر» في `Syntactic_Role` و«خبر» في "
    "`Phrasal_Function` وَسْمان بشرطين لا رقمان متنازعان — ٢٬٠٥٧ هنا و١٬٣٩٨ "
    "هناك — فلا يُصحَّح أحدُهما بالآخر ولا يُطرَح منه ولا يُجمَع إليه، "
    "والمُجمَّدُ في عمود التركيب يبقى كما هو"
)


IBTIDA_PREREGISTRATION_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "ThisRegistrationIsNotPriorToTheNumber": (
        THIS_REGISTRATION_IS_NOT_PRIOR_TO_THE_NUMBER_NOTE
    ),
    "TheFiguresArrivedFromTheHolderOfTheBytes": (
        THE_FIGURES_ARRIVED_FROM_THE_HOLDER_OF_THE_BYTES_NOTE
    ),
    "ADenominatorIsDeclaredNotAssumed": A_DENOMINATOR_IS_DECLARED_NOT_ASSUMED_NOTE,
    "ARelationNeedsTwoPresentTerms": A_RELATION_NEEDS_TWO_PRESENT_TERMS_NOTE,
    "ARoleTagIsNotALink": A_ROLE_TAG_IS_NOT_A_LINK_NOTE,
    "AnInchoativeGovernorIsSemanticNotLexical": (
        AN_INCHOATIVE_GOVERNOR_IS_SEMANTIC_NOT_LEXICAL_NOTE
    ),
    "APartialScanForbidsATotalDenial": A_PARTIAL_SCAN_FORBIDS_A_TOTAL_DENIAL_NOTE,
    "TheRetractedTotalDenial": THE_RETRACTED_TOTAL_DENIAL,
    "TheTwoColumnsAreNotOneFigure": THE_TWO_COLUMNS_ARE_NOT_ONE_FIGURE_NOTE,
    "AnUndeclaredSplitIsNotAZero": AN_UNDECLARED_SPLIT_IS_NOT_A_ZERO_NOTE,
    "AClaimedValueAbsentIsNotAZeroCount": (
        A_CLAIMED_VALUE_ABSENT_IS_NOT_A_ZERO_COUNT_NOTE
    ),
    "AnAnnotatedIrabIsAHumanJudgement": AN_ANNOTATED_IRAB_IS_A_HUMAN_JUDGEMENT_NOTE,
    "CoverageIsNotCorrectness": A_COVERAGE_IS_NOT_CORRECTNESS_NOTE,
    "CompleteInductionIsCorpusBounded": COMPLETE_INDUCTION_IS_CORPUS_BOUNDED_NOTE,
}


IBTIDA_CENSUS_COLUMNS: Final[tuple[str, ...]] = (
    ANCHOR_COLUMN_NAME,
    SYNTACTIC_ROLE_COLUMN,
    CASE_MOOD_COLUMN,
    CASE_MOOD_MARKER_COLUMN,
    SURA_COLUMN,
    VERSE_COLUMN,
    WORD_KEY_COLUMN_NAME,
    SEGMENT_INDEX_COLUMN_NAME,
)
"""الأعمدةُ الثمانيةُ التي يقوم بها هذا القياس؛ وغيابُ واحدٍ منها يُوقِف العدّ.

و`Phrasal_Function` ليس فيها: تغطيتُه ١٫٧٩٪، وقيمُه وَسْمٌ بشرطٍ آخرَ لا
تصحيحٌ لقيم `Syntactic_Role`. `TheTwoColumnsAreNotOneFigure`.
"""


class SentenceClass(Enum):
    """فئاتُ الجملة الاسمية الأربع، مانعةً جامعة؛ ولا موضعَ في اثنتين منها."""

    BARE = (
        "مجرَّدة: مبتدأٌ وخبرُه بلا ناسخ — ومعها «مبتدأ مؤخر» طرفًا للمبتدأ، "
        "لأنّ التقديمَ رتبةٌ لا فئةٌ خامسة"
    )
    NASIKH_PARTICLE = (
        "منسوخةٌ بحرف: اسمُ الحرف الناسخ وخبرُه؛ والوسمُ على الطرفين لا على "
        "الحرف نفسه في هذه القيم الثماني"
    )
    NASIKH_VERB = "منسوخةٌ بفعل: اسمُ الفعل الناسخ وخبرُه"
    LA_OF_ABSOLUTE_NEGATION = (
        "منفيّةٌ بلا النافية للجنس: اسمُها، وخبرُها **لم تصل له قيمةٌ في هذا "
        "العمود**؛ وذلك «لم يصل» لا «صفر»"
    )


class PositionSide(Enum):
    """طرفُ الموضع في الجملة الاسمية؛ وهما اثنان لا ثالثَ لهما في الثمانية."""

    INCHOATIVE = "مبتدأ_أو_اسمُ_ناسخ"
    PREDICATE = "خبر"


@dataclass(frozen=True, slots=True)
class ArrivingInchoativeFigure:
    """موضعٌ من مواضع الابتداء: قيمتُه، وفئتُه، وطرفُه، وعددُه المُدَّعى.

    `TheFiguresArrivedFromTheHolderOfTheBytes`: العددُ **دعوى** حتّى يُعاد
    اشتقاقُه من البايتات المُبصَّمة؛ وتجميدُه ليس تصديقًا له.
    """

    label: str
    column: str
    value: str
    sentence_class: SentenceClass
    side: PositionSide
    claimed_segment_count: int
    counting_rule: IrabCountingRule
    imported_from_the_first_freeze: bool

    def __post_init__(self) -> None:
        for text, label in (
            (self.label, "اسمُ الموضع"),
            (self.column, "اسمُ العمود"),
            (self.value, "قيمةُ العمود"),
        ):
            if not isinstance(text, str) or not text.strip():
                raise IrabPreregistrationError(f"{label} نصٌّ غير فارغ.")
        if self.column != SYNTACTIC_ROLE_COLUMN:
            raise IrabPreregistrationError(
                "مواضعُ الابتداء الثمانيةُ قيمُ `Syntactic_Role` وحدَه. "
                + THE_TWO_COLUMNS_ARE_NOT_ONE_FIGURE_NOTE
            )
        if not isinstance(self.sentence_class, SentenceClass):
            raise IrabPreregistrationError("لكلّ موضعٍ فئةٌ واحدةٌ من الأربع.")
        if not isinstance(self.side, PositionSide):
            raise IrabPreregistrationError("لكلّ موضعٍ طرفٌ مُسمًّى.")
        if self.counting_rule is not IrabCountingRule.SEGMENTS_WITH_VALUE:
            raise IrabPreregistrationError(
                "قاعدةُ العدّ هنا «المقطعُ ذو القيمة»؛ وعدُّ الكلمات عدٌّ آخر "
                "لا يُقرأ مكانَه."
            )
        if (
            isinstance(self.claimed_segment_count, bool)
            or not isinstance(self.claimed_segment_count, int)
            or self.claimed_segment_count <= 0
        ):
            raise IrabPreregistrationError(
                "عددُ الموضع عددٌ صحيحٌ موجب؛ وموضعٌ بصفرٍ ليس موضعًا يُعَدُّ "
                "في مقام. " + A_CLAIMED_VALUE_ABSENT_IS_NOT_A_ZERO_COUNT_NOTE
            )
        if not isinstance(self.imported_from_the_first_freeze, bool):
            raise IrabPreregistrationError("مصدرُ الرقم يُصرَّح به `True` أو `False`.")


def _mubtada_claimed_count() -> int:
    """عددُ «مبتدأ» مستوردًا من التجميد الأوّل؛ ولا يُكتَب هنا رقمٌ ثانٍ له.

    ورقمٌ مُجمَّدٌ مرّتين رقمان يفترقان بلا أن يفشل أحدُهما.
    """

    for figure in figures_for_column(SYNTACTIC_ROLE_COLUMN):
        if figure.value == "مبتدأ":
            return figure.claimed_count
    raise IrabPreregistrationError(
        "لا رقمَ مُجمَّدًا للقيمة «مبتدأ» في `Syntactic_Role`؛ ولا يُكتَب هنا " "رقمٌ ثانٍ لها."
    )


def _position(
    *,
    label: str,
    value: str,
    sentence_class: SentenceClass,
    side: PositionSide,
    claimed: int,
    imported: bool = False,
) -> ArrivingInchoativeFigure:
    return ArrivingInchoativeFigure(
        label=label,
        column=SYNTACTIC_ROLE_COLUMN,
        value=value,
        sentence_class=sentence_class,
        side=side,
        claimed_segment_count=claimed,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
        imported_from_the_first_freeze=imported,
    )


ARRIVING_INCHOATIVE_POSITIONS: Final[tuple[ArrivingInchoativeFigure, ...]] = (
    _position(
        label="مبتدأ",
        value="مبتدأ",
        sentence_class=SentenceClass.BARE,
        side=PositionSide.INCHOATIVE,
        claimed=_mubtada_claimed_count(),
        imported=True,
    ),
    _position(
        label="مبتدأ مؤخر",
        value="مبتدأ مؤخر",
        sentence_class=SentenceClass.BARE,
        side=PositionSide.INCHOATIVE,
        claimed=570,
    ),
    _position(
        label="خبر",
        value="خبر",
        sentence_class=SentenceClass.BARE,
        side=PositionSide.PREDICATE,
        claimed=2_057,
    ),
    _position(
        label="اسم حرف ناسخ",
        value="اسم حرف ناسخ",
        sentence_class=SentenceClass.NASIKH_PARTICLE,
        side=PositionSide.INCHOATIVE,
        claimed=2_086,
    ),
    _position(
        label="خبر حرف ناسخ",
        value="خبر حرف ناسخ",
        sentence_class=SentenceClass.NASIKH_PARTICLE,
        side=PositionSide.PREDICATE,
        claimed=929,
    ),
    _position(
        label="اسم فعل ناسخ",
        value="اسم فعل ناسخ",
        sentence_class=SentenceClass.NASIKH_VERB,
        side=PositionSide.INCHOATIVE,
        claimed=1_199,
    ),
    _position(
        label="خبر فعل ناسخ",
        value="خبر فعل ناسخ",
        sentence_class=SentenceClass.NASIKH_VERB,
        side=PositionSide.PREDICATE,
        claimed=799,
    ),
    _position(
        label="اسم لا النافية للجنس",
        value="اسم لا النافية للجنس",
        sentence_class=SentenceClass.LA_OF_ABSOLUTE_NEGATION,
        side=PositionSide.INCHOATIVE,
        claimed=111,
    ),
)
"""ثمانيةُ مواضعَ في أربع فئات؛ و«مبتدأ» وحدَه مستوردٌ من التجميد الأوّل.

والسبعةُ الباقيةُ إرساليةٌ ثالثةٌ من حائز البايتات، منزلتُها منزلةُ سابقتيها:
`TheFiguresArrivedFromTheHolderOfTheBytes`، فهي دعاوى أرقامٍ لا أرقامٌ مقيسة.
وليس في الفئة الرابعة خبرٌ لأنّ قيمتَه لم تصل في هذا العمود، وذلك **«لم
يصل»** لا «صفر».
"""


INCHOATIVE_POSITION_VALUES: Final[tuple[str, ...]] = tuple(
    figure.value for figure in ARRIVING_INCHOATIVE_POSITIONS
)


INCHOATIVE_POSITION_DENOMINATOR: Final[DeclaredDenominator] = DeclaredDenominator(
    name="مواضعُ الابتداء",
    column=SYNTACTIC_ROLE_COLUMN,
    value="؛ ".join(INCHOATIVE_POSITION_VALUES),
    counting_rule=(
        "موضعُ الابتداء: سجلٌّ `Morph_type` فيه «Stem» وقيمةُ `Syntactic_Role` "
        "فيه مطابقةٌ حرفيًّا لواحدةٍ من القيم الثماني بعد تجريد الفراغ "
        "الطرفيّ؛ والمقامُ هذه المواضعُ وحدَها لا الجذوعُ كلُّها ولا المقاطعُ "
        "كلُّها، لأنّ ما لا يقبل الابتداءَ أصلًا لا يُعَدُّ في مقامه"
    ),
)
"""المقامُ الثالثُ المُعلَن في هذه الشجرة، بعد مقام المقاطع ومقام الجذوع."""


INCHOATIVE_POSITION_TOTAL: Final[int] = sum(
    figure.claimed_segment_count for figure in ARRIVING_INCHOATIVE_POSITIONS
)
"""١١٬٣٤٩ موضعًا، **مجموعًا** للقيم الثماني لا رقمًا تاسعًا يُكتَب بيد.

ورقمٌ تاسعٌ مكتوبٌ بجانبها رقمان يفترقان بلا أن يفشل أحدُهما، كما في
`ARRIVING_RESIDUE_STEMS`.
"""


if INCHOATIVE_POSITION_TOTAL in (ARRIVING_STEM_TOTAL, ARRIVING_SEGMENT_TOTAL):
    raise IrabPreregistrationError(
        "مقامُ الابتداء غيرُ مقام الجذوع وغيرُ مقام المقاطع. "
        + A_DENOMINATOR_IS_DECLARED_NOT_ASSUMED_NOTE
    )


def figure_for_value(value: str) -> ArrivingInchoativeFigure | None:
    """الموضعُ بقيمته؛ و`None` جوابُ قيمةٍ لم تُجمَّد لا جوابُ غيابها."""

    stripped = value.strip()
    for figure in ARRIVING_INCHOATIVE_POSITIONS:
        if figure.value == stripped:
            return figure
    return None


def class_of_value(value: str) -> SentenceClass | None:
    """فئةُ القيمة من الأربع؛ و`None` لِما ليس من مواضع الابتداء الثمانية."""

    figure = figure_for_value(value)
    return figure.sentence_class if figure is not None else None


def side_of_value(value: str) -> PositionSide | None:
    """طرفُ القيمة؛ و`None` لِما ليس من الثمانية، لا دفعًا إلى طرف."""

    figure = figure_for_value(value)
    return figure.side if figure is not None else None


def figures_of_class(
    sentence_class: SentenceClass,
) -> tuple[ArrivingInchoativeFigure, ...]:
    """مواضعُ فئةٍ بعينها؛ والفئاتُ مانعةٌ جامعة، فلا موضعَ في اثنتين."""

    if not isinstance(sentence_class, SentenceClass):
        raise IrabPreregistrationError("الفئةُ واحدةٌ من الأربع المسنونة.")
    return tuple(
        figure
        for figure in ARRIVING_INCHOATIVE_POSITIONS
        if figure.sentence_class is sentence_class
    )


def _assert_the_four_classes_partition_the_eight() -> None:
    """احرسْ كونَ الفئات الأربع مانعةً جامعةً على القيم الثماني."""

    seen: set[str] = set()
    total = 0
    for sentence_class in SentenceClass:
        for figure in figures_of_class(sentence_class):
            if figure.value in seen:
                raise IrabPreregistrationError(
                    f"الموضعُ «{figure.value}» في أكثرَ من فئة؛ والفئاتُ مانعة."
                )
            seen.add(figure.value)
            total += figure.claimed_segment_count
    if seen != set(INCHOATIVE_POSITION_VALUES):
        raise IrabPreregistrationError(
            "موضعٌ خارجَ الفئات الأربع؛ والفئاتُ جامعةٌ على القيم الثماني."
        )
    if total != INCHOATIVE_POSITION_TOTAL:
        raise IrabPreregistrationError(
            "مجموعُ الفئات الأربع هو المقامُ بعينه؛ ولا يُقبَل فرقٌ بينهما."
        )


_assert_the_four_classes_partition_the_eight()


@dataclass(frozen=True, slots=True)
class ArrivingMubtadaBreakdown:
    """تفصيلُ المبتدأ كما وصل، ومقامُه المبتدأُ نفسُه منطوقًا في البنية.

    `ADenominatorIsDeclaredNotAssumed`: كلُّ جزءٍ هنا منسوبٌ إلى `positions`،
    ولا يُقرأ منسوبًا إلى الجذوع ولا إلى المقاطع ولا إلى مقام الابتداء.
    """

    positions: int
    declared_nominative_percentage: str
    accusative_positions: int
    invariable_positions: int
    declinable_positions: int
    top_marker_label: str
    top_marker_positions: int

    def __post_init__(self) -> None:
        if isinstance(self.positions, bool) or not isinstance(self.positions, int):
            raise IrabPreregistrationError("مقامُ التفصيل عددٌ صحيح.")
        if self.positions <= 0:
            raise IrabPreregistrationError(
                "تفصيلٌ بلا مقامٍ موجب. " + A_DENOMINATOR_IS_DECLARED_NOT_ASSUMED_NOTE
            )
        if "." not in self.declared_nominative_percentage:
            raise IrabPreregistrationError(
                "تُكتَب النسبةُ بمنازلها العشرية كما وصلت؛ فبها تُعرَف دقّةُ "
                "المقارنة، ونسبةٌ بلا منازلَ تُقارَن بدقّةٍ لم تُصرَّح."
            )
        if not isinstance(self.top_marker_label, str) or not (
            self.top_marker_label.strip()
        ):
            raise IrabPreregistrationError("لأعلى علامةٍ اسمُها المُصرَّحُ به.")
        for count, label in (
            (self.accusative_positions, "المنصوب"),
            (self.invariable_positions, "المبنيّ"),
            (self.declinable_positions, "المعرَب"),
            (self.top_marker_positions, "أعلى علامة"),
        ):
            if isinstance(count, bool) or not isinstance(count, int) or count < 0:
                raise IrabPreregistrationError(f"عددُ {label} صحيحٌ غيرُ سالب.")
            if count > self.positions:
                raise IrabPreregistrationError(
                    f"عددُ {label} لا يتجاوز مقامَه. "
                    + A_DENOMINATOR_IS_DECLARED_NOT_ASSUMED_NOTE
                )

    @property
    def build_total(self) -> int:
        """المبنيُّ والمعرَبُ مجموعين؛ عدًّا لا اشتقاقًا من نسبة."""

        return self.invariable_positions + self.declinable_positions

    @property
    def unaccounted_by_build(self) -> int:
        """ما لم يقع في المبنيّ ولا في المعرَب: فرقٌ يُعرَض ولا يُبتلَع.

        `AnUndeclaredSplitIsNotAZero`: هذا الفرقُ مكانٌ مُسمًّى لم يصل ما
        يملؤه، ولا يُقسَم تقديرًا على البابين.
        """

        return self.positions - self.build_total

    @property
    def top_marker_share(self) -> float:
        """حصّةُ أعلى علامةٍ من المبتدأ وحدَه، لا من الجذوع ولا من المقاطع."""

        return self.top_marker_positions / self.positions

    @property
    def nominative_positions_if_only_the_accusative_are_excepted(self) -> int:
        """المبتدأُ ناقصَ المنصوب؛ حسابٌ يُعرَض بجانب النسبة المُدَّعاة."""

        return self.positions - self.accusative_positions


ARRIVING_MUBTADA_BREAKDOWN: Final[ArrivingMubtadaBreakdown] = ArrivingMubtadaBreakdown(
    positions=_mubtada_claimed_count(),
    declared_nominative_percentage="99.5",
    accusative_positions=3,
    invariable_positions=2_354,
    declinable_positions=1_219,
    top_marker_label="السكون",
    top_marker_positions=1_274,
)
"""تفصيلُ المبتدأ الثلاثيُّ كما وصل، ومقامُه ٣٬٥٩٨ مستوردًا لا مكتوبًا ثانية.

وفيه فرقان معروضان لا مُبتلَعان: ٢٬٣٥٤ + ١٬٢١٩ = ٣٬٥٧٣، فبقي خمسةٌ وعشرون
موضعًا لا بابَ لها في `Invariable_Declinable` كما وصل؛ و٩٩٫٥٪ لا تخرج من
استثناء الثلاثة المنصوبة وحدَها — فتلك تُخرِج ٩٩٫٩٢٪ — فالفرقُ بينهما مكانٌ
مُسمًّى لم يصل ما يملؤه.
"""


class ResidueDerivation(Enum):
    """منشأُ عددِ البقيّة؛ و«وصل عددًا» غيرُ «اشتُقَّ طرحًا» غيرُ «بلا عدد»."""

    DERIVED_BY_SUBTRACTION = (
        "مُشتَقٌّ طرحًا من رقمين مُجمَّدين هنا؛ فلا يُكتَب رقمًا ثالثًا يفترق " "عنهما"
    )
    ARRIVED_AS_A_COUNT = (
        "وصل عددًا من حائز البايتات ولم يُشتَقَّ من المُجمَّد؛ فطرفاه غيرُ "
        "معلومَين هنا ويبقى مكانُهما مُسمًّى خاليًا"
    )
    NAMED_WITHOUT_A_COUNT = (
        "بقيّةٌ بنيويّةٌ لا عددَ لها: لا وَسْمَ في العمود يقابلها أصلًا، "
        "فعددُها `None` بمعنى «لا مقيسَ له» لا «صفر»"
    )


@dataclass(frozen=True, slots=True)
class NamedResidue:
    """بقيّةٌ مُسمّاةٌ قبل أن تُعذَر: اسمُها، وحجمُها، ومنشؤه، وفحصُها الواجب."""

    name: str
    description: str
    claimed_size: int | None
    derivation: ResidueDerivation
    minuend_value: str | None
    subtrahend_value: str | None
    requires_individual_inspection: bool

    def __post_init__(self) -> None:
        for text, label in ((self.name, "اسمُ البقيّة"), (self.description, "وصفُها")):
            if not isinstance(text, str) or not text.strip():
                raise IrabPreregistrationError(f"{label} نصٌّ غير فارغ.")
        if not isinstance(self.derivation, ResidueDerivation):
            raise IrabPreregistrationError("لكلّ بقيّةٍ منشأُ عددٍ مُسمًّى.")
        if not isinstance(self.requires_individual_inspection, bool):
            raise IrabPreregistrationError("الفحصُ الفرديُّ يُصرَّح به لا يُستنتَج.")
        if self.derivation is ResidueDerivation.NAMED_WITHOUT_A_COUNT:
            if self.claimed_size is not None:
                raise IrabPreregistrationError(
                    "بقيّةٌ بلا عددٍ حجمُها `None`؛ وصفرٌ مكانَه دعوى قياس. "
                    + AN_UNDECLARED_SPLIT_IS_NOT_A_ZERO_NOTE
                )
        elif (
            isinstance(self.claimed_size, bool)
            or not isinstance(self.claimed_size, int)
            or self.claimed_size < 0
        ):
            raise IrabPreregistrationError("حجمُ البقيّة عددٌ صحيحٌ غيرُ سالب.")
        if self.derivation is ResidueDerivation.DERIVED_BY_SUBTRACTION:
            if self.minuend_value is None or self.subtrahend_value is None:
                raise IrabPreregistrationError(
                    "الاشتقاقُ طرحًا يحتاج طرفيه مُسمَّيين من القيم الثماني."
                )
            minuend = figure_for_value(self.minuend_value)
            subtrahend = figure_for_value(self.subtrahend_value)
            if minuend is None or subtrahend is None:
                raise IrabPreregistrationError(
                    "طرفا الطرحِ من مواضع الابتداء الثمانية لا من غيرها."
                )
            difference = (
                minuend.claimed_segment_count - subtrahend.claimed_segment_count
            )
            if difference != self.claimed_size:
                raise IrabPreregistrationError(
                    f"الفرقُ المُشتَقُّ {difference} لا {self.claimed_size}؛ "
                    "ولا يُكتَب رقمٌ ثالثٌ يفترق عن طرفيه."
                )
        elif self.minuend_value is not None or self.subtrahend_value is not None:
            raise IrabPreregistrationError(
                "طرفا الطرحِ لا يُكتَبان لبقيّةٍ لم تُشتَقَّ طرحًا؛ فكتابتُهما "
                "تُوهِم اشتقاقًا لم يقع."
            )


NAMED_RESIDUES: Final[tuple[NamedResidue, ...]] = (
    NamedResidue(
        name="مبتدأ منصوب",
        description=(
            "ثلاثةُ مواضعَ وُسِمت «مبتدأ» و`Case_Mood` فيها «منصوب»؛ والقاعدةُ "
            "أنّ المبتدأ مرفوعٌ أو مبنيٌّ في محلّ رفع. **فحصٌ فرديٌّ إلزاميٌّ "
            "قبل الاعتماد**: ثلاثةٌ عددٌ يُفحَص واحدًا واحدًا لا يُلخَّص نسبةً، "
            "ومواضعُها لم تصل فتُخرَج من البايتات نفسِها"
        ),
        claimed_size=3,
        derivation=ResidueDerivation.ARRIVED_AS_A_COUNT,
        minuend_value=None,
        subtrahend_value=None,
        requires_individual_inspection=True,
    ),
    NamedResidue(
        name="فارق مبتدأ/خبر",
        description=(
            "وصل الفارقُ ١٨٧ ولم يصل طرفاه؛ وهو **لا يُشتَقُّ طرحًا** من القيم "
            "الثماني: ٣٬٥٩٨ + ٥٧٠ − ٢٬٠٥٧ = ٢٬١١١، لا ١٨٧. فيُسجَّل كما وصل "
            "ويبقى طرفاه مكانًا مُسمًّى خاليًا، والتفسيرُ المطلوبُ اثنان: "
            "خبران معطوفان لمبتدأٍ واحد؟ أم خبرٌ بلا مبتدأٍ موسوم؟"
        ),
        claimed_size=187,
        derivation=ResidueDerivation.ARRIVED_AS_A_COUNT,
        minuend_value=None,
        subtrahend_value=None,
        requires_individual_inspection=False,
    ),
    NamedResidue(
        name="فارق اسم الحرف الناسخ وخبره",
        description=(
            "اسمُ الحرف الناسخ موسومٌ أكثرَ من خبره؛ والفارقُ مُشتَقٌّ طرحًا من "
            "الرقمين لا مكتوبٌ ثالثًا. **أكبرُ بقيّةٍ في هذه الوحدة**، وسببُها "
            "غيرُ مفحوص: تُسمّى ولا تُبتلَع"
        ),
        claimed_size=2_086 - 929,
        derivation=ResidueDerivation.DERIVED_BY_SUBTRACTION,
        minuend_value="اسم حرف ناسخ",
        subtrahend_value="خبر حرف ناسخ",
        requires_individual_inspection=False,
    ),
    NamedResidue(
        name="فارق اسم الفعل الناسخ وخبره",
        description=(
            "اسمُ الفعل الناسخ موسومٌ أكثرَ من خبره؛ والفارقُ مُشتَقٌّ طرحًا "
            "كسابقه. وهو والذي قبله بقيّةٌ واحدةٌ في الحساب واثنتان في السطر، "
            "كي لا يختفي أحدُهما داخلَ مجموع"
        ),
        claimed_size=1_199 - 799,
        derivation=ResidueDerivation.DERIVED_BY_SUBTRACTION,
        minuend_value="اسم فعل ناسخ",
        subtrahend_value="خبر فعل ناسخ",
        requires_individual_inspection=False,
    ),
    NamedResidue(
        name="لا وسمَ لخبرٍ مقدَّم",
        description=(
            "«مبتدأ مؤخر» موسومٌ و«خبر مقدَّم» غيرُ موسوم؛ فطرفُ التقديم الآخرُ "
            "غيرُ موسومٍ بنيويًّا، ولا يُقاس تقديمٌ من طرفٍ واحد. ولا عددَ لهذه "
            "البقيّة لأنّ العمودَ لا يحمل قيمتَها أصلًا"
        ),
        claimed_size=None,
        derivation=ResidueDerivation.NAMED_WITHOUT_A_COUNT,
        minuend_value=None,
        subtrahend_value=None,
        requires_individual_inspection=False,
    ),
)
"""البقايا الأربعُ مُسمّاةً قبل القياس، مكتوبةً في خمسة أسطر.

والثالثةُ منها فارقان — ١٬١٥٧ و٤٠٠ — فُصِلا كي لا يُقرأ مجموعُهما بقيّةً
واحدةً يختفي فيها أحدُهما.
"""


DECLARED_GOVERNOR_VALUES: Final[tuple[str, ...]] = ("حرف ناسخ", "فعل ناسخ")
"""صياغتا الناسخ نفسِه كما يُتوقَّع ورودُهما؛ **ولا عددَ مُجمَّدٌ لهما هنا**.

`AClaimedValueAbsentIsNotAZeroCount`: إن لم تَرِد إحداهما في العمود فالجوابُ
«ليست من قيم هذا العمود» لا «صفر»، وذلك خبرٌ عن اسم القيمة لا عن العربية.
ووَسْمُ الناسخ نفسِه ليس من مواضع الابتداء الثمانية، فلا يدخل في المقام.
"""


PRE_MEASUREMENT_EXPECTATION: Final[str] = (
    "PreMeasurementExpectation: هذا وحدَه سابقٌ لِما يُقابِله — فاقترانُ "
    "المبتدأ بخبره لم يُقَس بعدُ لا هنا ولا عند حائز البايتات — وهو ثلاثةُ "
    "أمورٍ قابلةٍ للتكذيب. **أوّلًا**: كلُّ مبتدأٍ مرفوعٌ أو مبنيٌّ في محلّ "
    "رفع، والاستثناءاتُ الثلاثُ المنصوبةُ تبقى ثلاثًا بعد إعادة الاشتقاق؛ "
    "فإن صارت أربعًا أو اثنتين فالتوقّعُ كُذِّب ولا يُعدَّل الرقمُ ليُطابِق. "
    "**ثانيًا**: الخبرُ المنسوخُ موسومٌ أقلَّ من اسمه، بنسبةٍ تقارب ٢٫٢٥:١ "
    "في الحرف الناسخ و١٫٥:١ في الفعل الناسخ؛ **فإن تساوى الطرفان فالفرضيةُ "
    "تفشل**، ولا تُقرأ نسبةٌ أخرى تصحيحًا لها. **ثالثًا**: لكلّ ناسخٍ موسومٍ "
    "اسمٌ موسومٌ في الآية نفسِها؛ فإن وُجِد ناسخٌ بلا اسمٍ فهو بقيّةٌ تُسمّى "
    "بموضعها ولا تُدفَع إلى صفر. وحدُّ الثلاثة واحدٌ: كلُّها عن **الوسم في "
    "هذه المدوَّنة** تحت قاعدة الجوار المُجمَّدة، لا عن إسنادٍ مُثبَتٍ في "
    "العربية. " + A_ROLE_TAG_IS_NOT_A_LINK_NOTE
)


def ibtida_preregistration_digest() -> str:
    """بصمةُ محتوى التسجيل؛ فتبديلُ موضعٍ أو فئةٍ أو بقيّةٍ تُغيّرها."""

    return canonical_digest(
        canonical_bytes(
            {
                "standing": STANDING.value,
                "denominator": [
                    INCHOATIVE_POSITION_DENOMINATOR.name,
                    INCHOATIVE_POSITION_DENOMINATOR.column,
                    INCHOATIVE_POSITION_DENOMINATOR.value,
                    INCHOATIVE_POSITION_DENOMINATOR.counting_rule,
                ],
                "position_total": INCHOATIVE_POSITION_TOTAL,
                "positions": [
                    [
                        figure.value,
                        figure.sentence_class.name,
                        figure.side.value,
                        figure.claimed_segment_count,
                        figure.imported_from_the_first_freeze,
                    ]
                    for figure in ARRIVING_INCHOATIVE_POSITIONS
                ],
                "classes": {
                    sentence_class.name: sentence_class.value
                    for sentence_class in SentenceClass
                },
                "mubtada_breakdown": [
                    ARRIVING_MUBTADA_BREAKDOWN.positions,
                    ARRIVING_MUBTADA_BREAKDOWN.declared_nominative_percentage,
                    ARRIVING_MUBTADA_BREAKDOWN.accusative_positions,
                    ARRIVING_MUBTADA_BREAKDOWN.invariable_positions,
                    ARRIVING_MUBTADA_BREAKDOWN.declinable_positions,
                    ARRIVING_MUBTADA_BREAKDOWN.top_marker_label,
                    ARRIVING_MUBTADA_BREAKDOWN.top_marker_positions,
                ],
                "residues": [
                    [
                        residue.name,
                        residue.description,
                        (
                            residue.claimed_size
                            if residue.claimed_size is not None
                            else ""
                        ),
                        residue.derivation.name,
                        residue.requires_individual_inspection,
                    ]
                    for residue in NAMED_RESIDUES
                ],
                "governors": list(DECLARED_GOVERNOR_VALUES),
                "columns": list(IBTIDA_CENSUS_COLUMNS),
                "expectation": PRE_MEASUREMENT_EXPECTATION,
                "retraction": THE_RETRACTED_TOTAL_DENIAL,
                "residuals": sorted(IBTIDA_PREREGISTRATION_NAMED_RESIDUALS),
            }
        )
    )


IBTIDA_PREREGISTRATION_DIGEST: Final[str] = ibtida_preregistration_digest()
"""بصمةُ التسجيل مُشتقّةً من محتواه؛ ولا تُكتَب بيدٍ فتُصادِق على ما لم يُبصَّم."""


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
    "recall",
)


def _assert_no_outcome_field() -> None:
    """احرسْ خلوَّ وحدة التجميد من حقلِ نتيجةٍ أو دقّةٍ أو مُخرَجٍ مقيس."""

    for dataclass_type in (
        ArrivingInchoativeFigure,
        ArrivingMubtadaBreakdown,
        NamedResidue,
    ):
        for field in fields(dataclass_type):
            lowered = field.name.lower()
            for marker in _FORBIDDEN_FIELD_MARKERS:
                if marker in lowered:
                    raise IrabPreregistrationError(
                        f"حقلٌ ممنوعٌ في وحدة تجميد: {dataclass_type.__name__}."
                        f"{field.name}؛ والقياسُ موضعُه وحدةُ القياس."
                    )


_assert_no_outcome_field()

if STANDING is not RegistrationStanding.FORMULATED_AFTER_THE_NUMBER:
    raise IrabPreregistrationError(
        "منزلةُ هذا التسجيل `مُصاغ_بعد_الرقم`؛ وصلت الأرقامُ الثمانيةُ "
        "وتفصيلُ المبتدأ قبل صوغ قواعدِه. "
        + THIS_REGISTRATION_IS_NOT_PRIOR_TO_THE_NUMBER_NOTE
    )

if STEM_MORPH_TYPE != "Stem":  # pragma: no cover - حارسُ استيرادٍ لا فرعُ منطق
    raise IrabPreregistrationError("قيمةُ المرساة مستوردةٌ كما هي ولا تُبدَّل هنا.")
