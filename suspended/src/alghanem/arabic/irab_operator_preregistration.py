"""تجميدُ مقامِ الجذوع وكواشفِ العامل والمعمول قبل قياس العلاقة.

**السؤالُ الذي وُضِعت له هذه الوحدة**: عمودُ `Syntactic_Role` تغطيتُه ٧٦٫٣٦٪
من **المقاطع**، وهو رقمٌ يُقرأ نقصًا في الوسم؛ فإذا حُصِر المقامُ في
**الجذوع** وحدَها — `Morph_type == "Stem"` — انقلب الرقمُ إلى ٩٩٫٦٨٪. والفرقُ
ليس تحسينًا للنتيجة بل تصحيحٌ للمقام: المقاطعُ غيرُ الجذوع لواحقُ وسوابقُ لا
بابَ لها في الإعراب أصلًا، فعدُّها في المقام يُنقِص نسبةً لم تنقص.

`A_DENOMINATOR_IS_DECLARED_NOT_ASSUMED`: لا تخرج نسبةٌ من هذه الوحدة إلّا
مقرونةً بمقامها نصًّا. و٧٦٫٣٦٪ و٩٩٫٦٨٪ **ليستا رقمين متنازعين**: هما نسبتان
بمقامين، وقراءةُ إحداهما تصحيحًا للأخرى قراءةُ رقمٍ بلا مقامه.

`A_COVERAGE_IS_NOT_CORRECTNESS`: ٩٩٫٦٨٪ **تغطيةٌ لا صحّة**. وفي البقيّة نفسِها
شاهدٌ على ذلك: وصل أنّ «آمَنَ» في ٢:١٣ — وهو فعلٌ ماضٍ — موسومٌ `مجزوم`. فالوسمُ
الحاضرُ قد يكون خطأً، وحضورُه لا يُقاس صوابًا ولا يُعَدُّ كذلك هنا.

`AN_OPERATOR_TAG_IS_NOT_A_PROVEN_GOVERNMENT`: «حرف جر» وَسْمُ **بابِ الكلمة**
لا وَسْمُ رابطةٍ بين طرفين؛ فليس في المدوَّنة عمودٌ يربط عاملًا بمعموله بعينه.
وكلُّ زوجٍ يُخرِجه القياسُ زوجٌ **بقاعدة جوارٍ مُجمَّدةٍ هنا**، والجوارُ ليس
عملًا.

`A_RESIDUE_IS_NAMED_BEFORE_IT_IS_EXCUSED`: البقيّةُ ٢٤٦ جذعًا بلا دور، وهي
**ليست عشوائيةً ولا موحَّدةَ السبب**: ١٩٠ آيةً بمعدّل ١٫٢٩ جذعٍ للآية، ونمطان
متمايزان — سهوٌ موضعيٌّ في آيةٍ بقيّتُها مُغطّاة، وآياتٌ أُغفِلت بأكملها
أبرزُها ٢:١٣ بثلاثةَ عشرَ جذعًا. فتُسمَّى البقيّةُ بنمطيها لا تُذكَر عددًا
مجملًا يُقرأ ضوضاء.

`AN_UNDECLARED_SPLIT_IS_NOT_A_ZERO`: وصل عددُ الآيات في الأنماط الثلاثة
(١٦٤ و٤ و٢٢) وعددُ الجذوع في النمط الأوّل وحدَه (١٦٤، جذعٌ لكلّ آية)؛ ولم يصل
انقسامُ الاثنين والثمانين الباقيةِ على النمطين الآخرَين. فيُترَك المكانُ خاليًا
مُسمًّى، ولا يُملأ بصفرٍ ولا بقسمةٍ تُقدَّر.

`THIS_REGISTRATION_IS_NOT_PRIOR_TO_THE_NUMBER`: وصلت التغطيةُ ٩٩٫٦٨٣٨٪ وعددُ
البقيّة قبل صوغ هذه القواعد، فمنزلةُ التسجيل `مُصاغ_بعد_الرقم` مستوردةً من
`irab_column_preregistration` لا مُعادةً بيدٍ. وحدَه `PRE_MEASUREMENT_EXPECTATION`
سابقٌ لِما يُقابِله: العاملُ والمعمولُ لم يُقَس اقترانُهما بعدُ، لا هنا ولا عند
حائز البايتات.

وهذه الوحدة تجميدٌ لا سلطة: لا ولادةَ فيها، ولا حكمَ ولادة، ولا تجميدَ `E0`،
ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه. ولا حقلَ نتيجةٍ فيها،
وحارسٌ في آخرها يرفض إضافتَه.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest

# اسمُ عمودٍ يُستورَد ولا يُكتَب ثانيةً؛ وهو اسمُ ترويسةٍ لا رقمٌ مُجمَّد، فلا
# يُقرأ استيرادُه من وحدة القياس حملَ سلطةٍ منها.
from .irab_column_census import SURA_COLUMN, VERSE_COLUMN
from .irab_column_preregistration import (
    A_THINLY_COVERED_COLUMN_IS_NOT_A_CENSUS_OF_ARABIC_NOTE,
    AN_ANNOTATED_IRAB_IS_A_HUMAN_JUDGEMENT_NOTE,
    AN_ESTIMATED_MARKER_HAS_NO_WRITTEN_TRACE_NOTE,
    ANCHOR_COLUMN_NAME,
    SEGMENT_INDEX_COLUMN_NAME,
    STANDING,
    SYNTACTIC_ROLE_COLUMN,
    THE_FIGURES_ARRIVED_FROM_THE_HOLDER_OF_THE_BYTES_NOTE,
    THIS_REGISTRATION_IS_NOT_PRIOR_TO_THE_NUMBER_NOTE,
    WORD_KEY_COLUMN_NAME,
    IrabPreregistrationError,
    RegistrationStanding,
    figures_for_column,
)

__all__ = [
    "AN_OPERATOR_TAG_IS_NOT_A_PROVEN_GOVERNMENT_NOTE",
    "AN_UNDECLARED_SPLIT_IS_NOT_A_ZERO_NOTE",
    "ARRIVING_RESIDUE_ACCOUNT",
    "ARRIVING_ROLE_COVERAGE_ON_STEMS",
    "ARRIVING_STEM_TOTAL",
    "A_COVERAGE_IS_NOT_CORRECTNESS_NOTE",
    "A_DENOMINATOR_IS_DECLARED_NOT_ASSUMED_NOTE",
    "A_RELATION_NEEDS_TWO_PRESENT_TERMS_NOTE",
    "A_RESIDUE_IS_NAMED_BEFORE_IT_IS_EXCUSED_NOTE",
    "ACCEPTANCE_THRESHOLD_PERCENTAGE",
    "COMPLETE_INDUCTION_IS_CORPUS_BOUNDED_NOTE",
    "IRAB_OPERATOR_PREREGISTRATION_DIGEST",
    "IRAB_OPERATOR_PREREGISTRATION_NAMED_RESIDUALS",
    "NEUTRAL_ROLE_VALUES",
    "OPERATOR_CENSUS_COLUMNS",
    "OPERATOR_ROLE_VALUES",
    "DEPENDENT_ROLE_VALUES",
    "PRE_MEASUREMENT_EXPECTATION",
    "STEM_MORPH_TYPE",
    "THE_MARKER_IS_NOT_INFERRED_FROM_THE_CASE_NOTE",
    "THE_PHRASE_COLUMN_IS_NOT_USED_NOTE",
    "ArrivingResidueAccount",
    "ArrivingStemCoverage",
    "DeclaredDenominator",
    "ResiduePattern",
    "RoleDetector",
    "RoleSide",
    "STEM_DENOMINATOR",
    "detector_for_value",
    "operator_preregistration_digest",
    "role_side_of",
]


STEM_MORPH_TYPE: Final[str] = "Stem"
"""قيمةُ المرساة التي تُعرَّف بها الجذوع؛ مطابقةً حرفيّةً لا احتواءً."""


A_DENOMINATOR_IS_DECLARED_NOT_ASSUMED_NOTE: Final[str] = (
    "ADenominatorIsDeclaredNotAssumed: لا نسبةَ بلا مقامها منطوقًا معها؛ "
    "فـ٧٦٫٣٦٪ على المقاطع و٩٩٫٦٨٪ على الجذوع نسبتان بمقامين لا رقمان "
    "متنازعان، وقراءةُ إحداهما تصحيحًا للأخرى قراءةُ رقمٍ بلا مقامه"
)

A_COVERAGE_IS_NOT_CORRECTNESS_NOTE: Final[str] = (
    "CoverageIsNotCorrectness: ٩٩٫٦٨٪ عددُ الجذوع التي **وُسِمت** منسوبًا إلى "
    "الجذوع كلِّها، لا عددُ ما وُسِم **صوابًا**؛ وفي البقيّة شاهدٌ عليه: "
    "«آمَنَ» في ٢:١٣ فعلٌ ماضٍ موسومٌ `مجزوم`، فالحاضرُ قد يكون خطأً ولا "
    "يُقاس حضورُه صوابًا"
)

AN_OPERATOR_TAG_IS_NOT_A_PROVEN_GOVERNMENT_NOTE: Final[str] = (
    "AnOperatorTagIsNotAProvenGovernment: الوسمُ يقول «حرف جر» ولا يقول إنّه "
    "عَمِل في هذا المعمول بعينه؛ فلا عمودَ في المدوَّنة يربط عاملًا بمعموله، "
    "وكلُّ زوجٍ يخرج من قاعدة الجوار المُجمَّدةِ هنا قياسٌ للقاعدة، والجوارُ "
    "ليس عملًا"
)

A_RELATION_NEEDS_TWO_PRESENT_TERMS_NOTE: Final[str] = (
    "ARelationNeedsTwoPresentTerms: طرفا العلاقة يُطلَبان داخل الآية الواحدة "
    "ولا يُجاوَز بها حدُّها؛ ومعمولٌ لا عاملَ في آيته يُسمّى «لا عامل مرصود» "
    "ولا يُوصَل بعاملٍ من آيةٍ أخرى ليكتمل عددٌ"
)

A_RESIDUE_IS_NAMED_BEFORE_IT_IS_EXCUSED_NOTE: Final[str] = (
    "AResidueIsNamedBeforeItIsExcused: البقيّةُ ٢٤٦ جذعًا في ١٩٠ آية بمعدّل "
    "١٫٢٩، فهي ليست عشوائيةً ولا موحَّدةَ السبب: سهوٌ موضعيٌّ في آيةٍ بقيّتُها "
    "مُغطّاة، وآياتٌ أُغفِلت بأكملها أبرزُها ٢:١٣ بثلاثةَ عشرَ جذعًا؛ "
    "وذكرُها عددًا مجملًا يُقرأ ضوضاءً لا نمطًا"
)

AN_UNDECLARED_SPLIT_IS_NOT_A_ZERO_NOTE: Final[str] = (
    "AnUndeclaredSplitIsNotAZero: وصل عددُ الآيات في الأنماط الثلاثة وعددُ "
    "الجذوع في النمط الأوّل وحدَه؛ وانقسامُ الاثنين والثمانين الباقيةِ على "
    "النمطين الآخرَين لم يصل، فيبقى مكانُه خاليًا مُسمًّى لا يُملأ بصفرٍ ولا "
    "بقسمةٍ تُقدَّر"
)

THE_PHRASE_COLUMN_IS_NOT_USED_NOTE: Final[str] = (
    "ThePhraseColumnIsNotUsed: عمودُ `Phrase` تغطيتُه ١٫٨٠٪ ووسمُه معلَّقٌ "
    "بالموقع الإعرابيّ، فيَسِم الجملةَ المُضمَّنةَ دون الرئيسية؛ فلا يُقاس به "
    "شيءٌ هنا، وتفاوتُ أعداده بين أنواع الجمل فرقٌ في شرط الوسم لا في العربية"
)

THE_MARKER_IS_NOT_INFERRED_FROM_THE_CASE_NOTE: Final[str] = (
    "TheMarkerIsNotInferredFromTheCase: لا تُستنتَج العلامةُ من الحالة ولا من "
    "الحالة والموقع معًا، لأنّ اختيارَها يستلزم صنفَ اللفظ — سالمًا أو مثنًّى "
    "أو جمعًا أو من الأسماء الخمسة — فلا يُشتَقُّ في هذه الوحدة عمودٌ من عمود. "
    + AN_ESTIMATED_MARKER_HAS_NO_WRITTEN_TRACE_NOTE
)

COMPLETE_INDUCTION_IS_CORPUS_BOUNDED_NOTE: Final[str] = (
    "CompleteInductionIsCorpusBounded: كلُّ رقمٍ هنا وصفٌ لهذه البايتات تحت "
    "قاعدة عدِّه، لا قانونٌ عن العربية؛ فـ٩٩٫٦٨٪ تغطيةُ وَسْمٍ في مدوَّنةٍ "
    "واحدة، ولا يُقرأ منها استقراءٌ تامٌّ لبابِ العامل والمعمول"
)


IRAB_OPERATOR_PREREGISTRATION_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "ADenominatorIsDeclaredNotAssumed": A_DENOMINATOR_IS_DECLARED_NOT_ASSUMED_NOTE,
    "CoverageIsNotCorrectness": A_COVERAGE_IS_NOT_CORRECTNESS_NOTE,
    "AnOperatorTagIsNotAProvenGovernment": (
        AN_OPERATOR_TAG_IS_NOT_A_PROVEN_GOVERNMENT_NOTE
    ),
    "ARelationNeedsTwoPresentTerms": A_RELATION_NEEDS_TWO_PRESENT_TERMS_NOTE,
    "AResidueIsNamedBeforeItIsExcused": A_RESIDUE_IS_NAMED_BEFORE_IT_IS_EXCUSED_NOTE,
    "AnUndeclaredSplitIsNotAZero": AN_UNDECLARED_SPLIT_IS_NOT_A_ZERO_NOTE,
    "ThePhraseColumnIsNotUsed": THE_PHRASE_COLUMN_IS_NOT_USED_NOTE,
    "TheMarkerIsNotInferredFromTheCase": THE_MARKER_IS_NOT_INFERRED_FROM_THE_CASE_NOTE,
    "CompleteInductionIsCorpusBounded": COMPLETE_INDUCTION_IS_CORPUS_BOUNDED_NOTE,
    "AnAnnotatedIrabIsAHumanJudgement": AN_ANNOTATED_IRAB_IS_A_HUMAN_JUDGEMENT_NOTE,
    "AThinlyCoveredColumnIsNotACensusOfArabic": (
        A_THINLY_COVERED_COLUMN_IS_NOT_A_CENSUS_OF_ARABIC_NOTE
    ),
    "ThisRegistrationIsNotPriorToTheNumber": (
        THIS_REGISTRATION_IS_NOT_PRIOR_TO_THE_NUMBER_NOTE
    ),
    "TheFiguresArrivedFromTheHolderOfTheBytes": (
        THE_FIGURES_ARRIVED_FROM_THE_HOLDER_OF_THE_BYTES_NOTE
    ),
}


OPERATOR_CENSUS_COLUMNS: Final[tuple[str, ...]] = (
    ANCHOR_COLUMN_NAME,
    SYNTACTIC_ROLE_COLUMN,
    SURA_COLUMN,
    VERSE_COLUMN,
    WORD_KEY_COLUMN_NAME,
    SEGMENT_INDEX_COLUMN_NAME,
)
"""الأعمدةُ الستّةُ التي يقوم بها هذا القياس؛ وغيابُ واحدٍ منها يُوقِف العدّ.

و`Phrase` ليس فيها عمدًا: `ThePhraseColumnIsNotUsed`.
"""


@dataclass(frozen=True, slots=True)
class DeclaredDenominator:
    """مقامٌ منطوقٌ باسمه وقاعدةِ حصرِه؛ ولا نسبةَ في هذه الوحدة بغيره."""

    name: str
    column: str
    value: str
    counting_rule: str

    def __post_init__(self) -> None:
        for field in fields(self):
            text = getattr(self, field.name)
            if not isinstance(text, str) or not text.strip():
                raise IrabPreregistrationError(
                    f"{field.name} نصٌّ غير فارغ؛ ومقامٌ بلا قاعدةِ حصرٍ مكتوبةٍ "
                    "يُقرأ نسبةً بلا مقام. " + A_DENOMINATOR_IS_DECLARED_NOT_ASSUMED_NOTE
                )


STEM_DENOMINATOR: Final[DeclaredDenominator] = DeclaredDenominator(
    name="الجذوع",
    column=ANCHOR_COLUMN_NAME,
    value=STEM_MORPH_TYPE,
    counting_rule=(
        "الجذعُ: سجلٌّ قيمةُ `Morph_type` فيه مطابقةٌ حرفيًّا لـ«Stem» بعد "
        "تجريد الفراغ الطرفيّ؛ والمقامُ الجذوعُ وحدَها لا المقاطعُ كلُّها، "
        "لأنّ اللواحقَ والسوابقَ لا بابَ لها في الإعراب فعدُّها يُنقِص نسبةً "
        "لم تنقص"
    ),
)


ARRIVING_STEM_TOTAL: Final[int] = 77_797
"""جملةُ الجذوع كما وصلت؛ مقامُ التغطية أدناه، ودعوًى حتّى يُعادَ اشتقاقُها."""


@dataclass(frozen=True, slots=True)
class ArrivingStemCoverage:
    """تغطيةُ `Syntactic_Role` على مقام الجذوع كما وصلت، بمقامها لا بدونه."""

    column: str
    denominator: DeclaredDenominator
    denominator_count: int
    covered_count: int
    declared_percentage: str

    def __post_init__(self) -> None:
        if not isinstance(self.denominator, DeclaredDenominator):
            raise IrabPreregistrationError(
                "نسبةٌ بلا مقامٍ مُعلَن. " + A_DENOMINATOR_IS_DECLARED_NOT_ASSUMED_NOTE
            )
        for count, label in (
            (self.denominator_count, "عددُ المقام"),
            (self.covered_count, "عددُ المُغطّى"),
        ):
            if isinstance(count, bool) or not isinstance(count, int) or count < 0:
                raise IrabPreregistrationError(f"{label} عددٌ صحيحٌ غيرُ سالب.")
        if self.covered_count > self.denominator_count:
            raise IrabPreregistrationError("المُغطّى لا يتجاوز مقامَه.")
        if "." not in self.declared_percentage:
            raise IrabPreregistrationError(
                "تُكتَب النسبةُ بمنازلها العشرية كما وصلت؛ فبها تُعرَف دقّةُ "
                "المقارنة، ونسبةٌ بلا منازلَ تُقارَن بدقّةٍ لم تُصرَّح."
            )

    @property
    def residue_count(self) -> int:
        """الجذوعُ بلا دورٍ: المقامُ ناقصَ المُغطّى، عدًّا لا اشتقاقًا من نسبة."""

        return self.denominator_count - self.covered_count

    @property
    def decimal_places(self) -> int:
        """منازلُ النسبة المُصرَّح بها؛ وعندها تقف المقارنةُ ولا تتجاوزها."""

        return len(self.declared_percentage.split(".")[1])


ARRIVING_ROLE_COVERAGE_ON_STEMS: Final[ArrivingStemCoverage] = ArrivingStemCoverage(
    column=SYNTACTIC_ROLE_COLUMN,
    denominator=STEM_DENOMINATOR,
    denominator_count=ARRIVING_STEM_TOTAL,
    covered_count=77_551,
    declared_percentage="99.6838",
)
"""التغطيةُ على مقام الجذوع كما وصلت؛ و٢٤٦ بقيّتُها معدودةً لا مشتقّةً منها."""


ACCEPTANCE_THRESHOLD_PERCENTAGE: Final[str] = "99.00"
"""عتبةُ القبول على مقام الجذوع وحدَه؛ ولا تُقرأ عتبةً على مقام المقاطع.

وهي مكتوبةٌ بنصِّها لا بعائمٍ، ومنزلتُها منزلةُ التسجيل كلِّه: وصلت التغطيةُ
قبل صوغها، فليست عتبةً سابقةً للرقم. وتُترَك مع ذلك مكتوبةً لأنّ عتبةً معلنةً
تُقاس بها القراءاتُ القادمةُ خيرٌ من حكمٍ يُصاغ عند كلّ رقمٍ على مقاسه.
"""


class ResiduePattern(Enum):
    """أنماطُ البقيّة مُسمّاةً؛ و«لم يُصنَّف» بابٌ مُعلَنٌ لا يُبتلَع فيه فرق."""

    SINGLE_UNROLED_STEM_IN_VERSE = (
        "سهوٌ موضعيّ: جذعٌ واحدٌ في الآية بلا دور، وبقيّةُ جذوعها مُغطّاة؛ "
        "فهو سهوُ خليّةٍ لا فجوةٌ منهجية"
    )
    WHOLLY_UNANNOTATED_VERSE = (
        "آيةٌ مُهمَلةٌ بأكملها: لا جذعَ فيها حمل دورًا نحويًّا البتّة؛ فهو "
        "إغفالُ آيةٍ لا سهوُ كلمة"
    )
    NEITHER_PATTERN = (
        "لا هذا ولا ذاك: في الآية أكثرُ من جذعٍ بلا دورٍ وفيها جذعٌ مُغطًّى؛ "
        "فلا تُدفَع إلى أحد النمطين لتختفي"
    )


@dataclass(frozen=True, slots=True)
class ArrivingResidueAccount:
    """حسابُ البقيّة كما وصل: آياتٍ بأنماطها، وجذوعًا حيث صُرِّح بها.

    `AnUndeclaredSplitIsNotAZero`: `stems` قد تكون `None`، ومعناها «لم يصل»
    لا «صفر»؛ فلا تُجمَع ولا تُقسَم تقديرًا.
    """

    pattern: ResiduePattern
    verses: int
    stems: int | None

    def __post_init__(self) -> None:
        if not isinstance(self.pattern, ResiduePattern):
            raise IrabPreregistrationError("لكلّ حسابٍ نمطٌ مُسمًّى من الثلاثة.")
        if isinstance(self.verses, bool) or not isinstance(self.verses, int):
            raise IrabPreregistrationError("عددُ الآيات عددٌ صحيح.")
        if self.verses < 0:
            raise IrabPreregistrationError("عددُ آياتٍ لا يكون سالبًا.")
        if self.stems is None:
            return
        if isinstance(self.stems, bool) or not isinstance(self.stems, int):
            raise IrabPreregistrationError(
                "عددُ الجذوع عددٌ صحيحٌ أو `None` بمعنى «لم يصل». "
                + AN_UNDECLARED_SPLIT_IS_NOT_A_ZERO_NOTE
            )
        if self.stems < self.verses:
            raise IrabPreregistrationError(
                "لا تقلُّ جذوعُ البقيّة عن آياتها: لكلّ آيةٍ في البقيّة جذعٌ "
                "واحدٌ فأكثرُ بلا دور."
            )


ARRIVING_RESIDUE_ACCOUNT: Final[tuple[ArrivingResidueAccount, ...]] = (
    ArrivingResidueAccount(
        pattern=ResiduePattern.SINGLE_UNROLED_STEM_IN_VERSE,
        verses=164,
        stems=164,
    ),
    ArrivingResidueAccount(
        pattern=ResiduePattern.WHOLLY_UNANNOTATED_VERSE,
        verses=4,
        stems=None,
    ),
    ArrivingResidueAccount(
        pattern=ResiduePattern.NEITHER_PATTERN,
        verses=22,
        stems=None,
    ),
)
"""١٩٠ آيةً في ثلاثة أنماط، و٢٤٦ جذعًا مجموعًا؛ والمُصرَّحُ به جذوعُ الأوّل.

ووصل مع النمط الثاني أنّ أكبرَ آياته ٢:١٣ بثلاثةَ عشرَ جذعًا، وأنّ مواضعَها
متتاليةٌ من ٢:١٣:٥ إلى ٢:١٣:١٥؛ وذلك وصفُ آيةٍ بعينها لا قاعدةُ عدٍّ، فلا يدخل
في حسابٍ ولا يُشتَقُّ منه انقسامُ الاثنين والثمانين.
"""


class RoleSide(Enum):
    """طرفُ القيمة في العلاقة، مسنونًا قبل قياسٍ؛ و«خارج الكواشف» منها."""

    OPERATOR = "عامل"
    DEPENDENT = "معمول"
    NEUTRAL = "محايد"
    OUTSIDE_THE_DETECTORS = "خارج_الكواشف"


@dataclass(frozen=True, slots=True)
class RoleDetector:
    """كاشفٌ مُجمَّد: قيمةٌ من `Syntactic_Role`، وطرفُها، وعددُها المُدَّعى.

    والعددُ **مستوردٌ** من `irab_column_preregistration` لا مُعادٌ كتابةً:
    رقمٌ مُجمَّدٌ مرّتين رقمان يفترقان بلا أن يفشل أحدُهما.
    """

    value: str
    side: RoleSide
    claimed_segment_count: int

    def __post_init__(self) -> None:
        if not isinstance(self.value, str) or not self.value.strip():
            raise IrabPreregistrationError("قيمةُ الكاشف نصٌّ غير فارغ.")
        if not isinstance(self.side, RoleSide):
            raise IrabPreregistrationError("لكلّ كاشفٍ طرفٌ مُسمًّى.")
        if self.side is RoleSide.OUTSIDE_THE_DETECTORS:
            raise IrabPreregistrationError(
                "«خارج الكواشف» جوابُ قيمةٍ لم تُجمَّد، فلا يُجمَّد بها كاشف."
            )
        if (
            isinstance(self.claimed_segment_count, bool)
            or not isinstance(self.claimed_segment_count, int)
            or self.claimed_segment_count < 0
        ):
            raise IrabPreregistrationError("العددُ المُدَّعى عددٌ صحيحٌ غيرُ سالب.")


_DETECTOR_SIDES: Final[tuple[tuple[str, RoleSide], ...]] = (
    ("حرف جر", RoleSide.OPERATOR),
    ("فعل ماضٍ", RoleSide.OPERATOR),
    ("فعل مضارع", RoleSide.OPERATOR),
    ("اسم مجرور", RoleSide.DEPENDENT),
    ("فاعل", RoleSide.DEPENDENT),
    ("مفعول به", RoleSide.DEPENDENT),
    ("حرف غير عامل", RoleSide.NEUTRAL),
    ("حرف عطف", RoleSide.NEUTRAL),
)
"""ثمانيةُ كواشفَ بأطرافها؛ وصياغتُها الحرفيّةُ هي المُجمَّدةُ في التسجيل الأوّل."""


def _claimed_counts() -> dict[str, int]:
    """أعدادُ الأدوار المُدَّعاةُ كما جُمِّدت هناك؛ استيرادًا لا نسخًا."""

    counts: dict[str, int] = {}
    for figure in figures_for_column(SYNTACTIC_ROLE_COLUMN):
        if figure.value is not None:
            counts[figure.value] = figure.claimed_count
    return counts


def _build_detectors() -> tuple[RoleDetector, ...]:
    counts = _claimed_counts()
    detectors: list[RoleDetector] = []
    for value, side in _DETECTOR_SIDES:
        if value not in counts:
            raise IrabPreregistrationError(
                f"لا رقمَ مُجمَّدًا للقيمة «{value}» في `Syntactic_Role`؛ "
                "ولا يُكتَب هنا رقمٌ ثانٍ لها."
            )
        detectors.append(
            RoleDetector(value=value, side=side, claimed_segment_count=counts[value])
        )
    return tuple(detectors)


_DETECTORS: Final[tuple[RoleDetector, ...]] = _build_detectors()


OPERATOR_ROLE_VALUES: Final[tuple[str, ...]] = tuple(
    detector.value for detector in _DETECTORS if detector.side is RoleSide.OPERATOR
)

DEPENDENT_ROLE_VALUES: Final[tuple[str, ...]] = tuple(
    detector.value for detector in _DETECTORS if detector.side is RoleSide.DEPENDENT
)

NEUTRAL_ROLE_VALUES: Final[tuple[str, ...]] = tuple(
    detector.value for detector in _DETECTORS if detector.side is RoleSide.NEUTRAL
)


def detector_for_value(value: str) -> RoleDetector | None:
    """الكاشفُ بقيمته؛ و`None` جوابُ قيمةٍ لم تُجمَّد لا جوابُ غيابها."""

    for detector in _DETECTORS:
        if detector.value == value:
            return detector
    return None


def role_side_of(value: str) -> RoleSide:
    """طرفُ القيمة؛ وما لم يُجمَّد يخرج `خارج_الكواشف` لا يُدفَع إلى طرف.

    والكواشفُ ثمانيةٌ من ستٍّ وستّين قيمة، فأكثرُ القيم خارجَها بالتصميم؛
    وقراءةُ «خارج الكواشف» نفيًا لعملٍ قراءةُ حدِّ الأداة خبرًا عن العربية.
    """

    detector = detector_for_value(value.strip())
    return detector.side if detector is not None else RoleSide.OUTSIDE_THE_DETECTORS


PRE_MEASUREMENT_EXPECTATION: Final[str] = (
    "PreMeasurementExpectation: هذا وحدَه سابقٌ لِما يُقابِله — فاقترانُ "
    "العامل بالمعمول لم يُقَس بعدُ لا هنا ولا عند حائز البايتات — وهو أمران. "
    "**أوّلًا**: يُتوقَّع أن يسبق العاملُ معمولَه في الغالبية العظمى من "
    "الأزواج المرصودة، فإن خرجت «له عاملٌ لاحقٌ» كثرةً غالبةً فالتوقّعُ "
    "كُذِّب ولا تُعدَّل القاعدةُ لتُطابِق. **ثانيًا**: يُتوقَّع أن تكون "
    "المسافةُ الأشيعُ بين العامل ومعموله كلمةً واحدةً — أي الجوارَ المباشر — "
    "فإن كانت غيرَها فالتوقّعُ كُذِّب. وحدُّ التوقّعين واحدٌ: كلاهما عن "
    "**الوسم في هذه المدوَّنة** تحت قاعدة الجوار المُجمَّدة، لا عن عملٍ "
    "مُثبَتٍ في العربية. " + AN_OPERATOR_TAG_IS_NOT_A_PROVEN_GOVERNMENT_NOTE
)


def operator_preregistration_digest() -> str:
    """بصمةُ محتوى التسجيل؛ فتبديلُ كاشفٍ أو مقامٍ أو عتبةٍ تُغيّرها."""

    return canonical_digest(
        canonical_bytes(
            {
                "standing": STANDING.value,
                "denominator": [
                    STEM_DENOMINATOR.name,
                    STEM_DENOMINATOR.column,
                    STEM_DENOMINATOR.value,
                    STEM_DENOMINATOR.counting_rule,
                ],
                "stem_total": ARRIVING_STEM_TOTAL,
                "coverage": [
                    ARRIVING_ROLE_COVERAGE_ON_STEMS.column,
                    ARRIVING_ROLE_COVERAGE_ON_STEMS.covered_count,
                    ARRIVING_ROLE_COVERAGE_ON_STEMS.declared_percentage,
                ],
                "threshold": ACCEPTANCE_THRESHOLD_PERCENTAGE,
                "residue_patterns": {
                    pattern.name: pattern.value for pattern in ResiduePattern
                },
                "residue_account": [
                    [
                        account.pattern.name,
                        account.verses,
                        account.stems if account.stems is not None else "",
                    ]
                    for account in ARRIVING_RESIDUE_ACCOUNT
                ],
                "detectors": [
                    [
                        detector.value,
                        detector.side.value,
                        detector.claimed_segment_count,
                    ]
                    for detector in _DETECTORS
                ],
                "columns": list(OPERATOR_CENSUS_COLUMNS),
                "expectation": PRE_MEASUREMENT_EXPECTATION,
                "residuals": sorted(IRAB_OPERATOR_PREREGISTRATION_NAMED_RESIDUALS),
            }
        )
    )


IRAB_OPERATOR_PREREGISTRATION_DIGEST: Final[str] = operator_preregistration_digest()
"""بصمةُ التسجيل مُشتقّةً من محتواه؛ ولا تُكتَب بيدٍ فتُصادِق على ما لم يُبصَّم."""


_FORBIDDEN_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "outcome",
    "result",
    "observed",
    "measured",
    "rederived",
    "verdict",
    "birth",
)


def _assert_no_outcome_field() -> None:
    """احرسْ خلوَّ وحدة التجميد من حقلِ نتيجةٍ أو مُخرَجٍ مقيس."""

    for dataclass_type in (
        DeclaredDenominator,
        ArrivingStemCoverage,
        ArrivingResidueAccount,
        RoleDetector,
    ):
        for field in fields(dataclass_type):
            lowered = field.name.lower()
            for marker in _FORBIDDEN_FIELD_MARKERS:
                if marker in lowered:
                    raise IrabPreregistrationError(
                        f"حقلُ نتيجةٍ في وحدة تجميد: {dataclass_type.__name__}."
                        f"{field.name}؛ والقياسُ موضعُه وحدةُ القياس."
                    )


_assert_no_outcome_field()

if STANDING is not RegistrationStanding.FORMULATED_AFTER_THE_NUMBER:
    raise IrabPreregistrationError(
        "منزلةُ هذا التسجيل `مُصاغ_بعد_الرقم`؛ وصلت التغطيةُ وعددُ البقيّة "
        "قبل صوغ قواعدِه. " + THIS_REGISTRATION_IS_NOT_PRIOR_TO_THE_NUMBER_NOTE
    )
