"""تجميدُ قواعدِ سبرِ اللزوم والتعدّي قبل قياسها، وإيداعُ الأرقام الواردة كما وردت.

**السؤالُ الذي وُضِعت له هذه الوحدة**: وصلت من محادثةٍ خارجيةٍ أربعُ نتائجَ
معدودةٍ على مدوَّنة `QURANIC_ARABIC_CORPUS_WITNESS`، مؤدّاها أنّ فعلًا مجرَّدًا
لا يُوسَم له مجهولٌ مجرَّدٌ «مرشَّحٌ لازم»، وأنّ الفرق بينه وبين المتعدّي ظاهرٌ
في اسم المفعول، وأنّ فرضية «اللازم يصير متعدّيًا بالتزيّد» تُفنَّد كقاعدة.
والأرقامُ لا تُقرأ قياسًا ما لم تحمل **قاعدةَ عدِّها** و**بروتوكولَ اختبارها**؛
فيُجمَّدان هنا، ويقع القياسُ في `transitivity_corpus_census` لا هنا.

`FREEZE_BEFORE_MEASUREMENT`: ليس في هذه الوحدة دالّةُ قياسٍ ولا حقلُ نتيجة،
وحارسٌ عند الاستيراد يمنع تسلُّلَهما لاحقًا — على منوال
`hollow_root_levels_preregistration`.

`THE_SCHEMA_WAS_READ_BEFORE_THE_RULE_THE_RESULT_WAS_NOT`: قاعدتا التصنيف
أدناه مبنيّتان على واقعتين في **مخطَّط** المدوَّنة قُرِئتا من البايتات قبل
صياغتهما: (أ) الفعلُ المبنيُّ للمعلوم **لا يحمل وسمَ `ACT`** أصلًا في خانة
الأفعال، فالمعلومُ هو غيابُ `PASS` لا حضورُ `ACT`؛ (ب) الوزنُ الأوّل **لا
يُوسَم** `(I)`، فالمجرَّدُ هو غيابُ وسمِ الوزن. وهذا اطّلاعٌ على المخطَّط لا
على النتيجة، والفرقُ بينهما مُسجَّلٌ ولا يُطوى: من قرأ هذه الوحدة تسجيلًا
قبْليًّا تامًّا بمعنى `THE_NUMBERS_ARRIVED_BEFORE_THE_RUN` قرأ أكثرَ ممّا فيها.

`ABSENCE_OF_A_TAG_IS_NOT_ABSENCE_OF_A_FORM`: «لا مجهولَ مجرَّدًا لهذا الجذر»
حكمٌ على **هذه المدوَّنة**، لا على العربية ولا على المعجم. فالمجموعتان
`CONFIRMED_TRANSITIVE` و`INTRANSITIVE_CANDIDATE` اسمان مدوَّنيّان، والثانيةُ
مُسمّاةٌ «مرشَّحًا» لهذا السبب بعينه.

`THE_INDICATOR_AND_ITS_TEST_SHARE_A_PARENT`: اسمُ المفعول صيغةٌ مجهولة،
والمجموعتان عُرِّفتا أصلًا بحضور المجهول وغيابه؛ فاختبارُ فرقِ اسم المفعول بين
المجموعتين **ليس شاهدًا مستقلًّا** عن تعريفهما، بل تقاربُ مؤشّرَي تعدٍّ
مختلفَي الاشتقاق. ويُكتَب هذا التحفّظ قبل الرقم لا بعده.

`A_PERMUTATION_P_HAS_A_FLOOR`: اختبارُ التبديل بعددٍ منتهٍ من التباديل لا
يُخرِج صفرًا: أصغرُ ما يُخرِجه `(1 + عدد المتجاوزات) / (1 + عدد التباديل)`،
وهو هنا `1/5001`. فكتابةُ `p = 0.0000` تُسنِد إلى الاختبار دقّةً لا يملكها،
والمكتوبُ هنا الكسرُ بحدّه.

`THE_MAXIMUM_NULL_GAP_IS_NOT_THE_P_VALUE`: «تجاوزَ الفارقُ أقصى فارقٍ عدميّ»
عبارةٌ عن إحصاءةٍ طرفيةٍ شديدةِ التقلّب بعدد التباديل، وقد يقع فارقٌ دالٌّ
بـ`p` صغيرةٍ **دون** أقصى الفوارق العدمية. فالحكمُ على `p` المُصرَّح
ببروتوكولها، وأقصى الفارق العدميّ يُودَع وصفًا لا معيارًا.

`UNTAGGED_IS_LEFT_WITHOUT_A_NUMBER_NOT_WITH_A_ZERO`: المصدرُ واسمُ المكان
واسمُ الزمان الصرفيّان واسمُ الآلة والتمييز **غيرُ موسومةٍ في هذه المدوَّنة**؛
و`POS:LOC` و`POS:T` وَسْما ظرفٍ نحويَّين لا صيغتين صرفيّتين. فتُترَك بلا رقم،
ولا تُكتَب لها أصفارٌ تُقرأ غيابًا في العربية.

`THIS_IS_REGISTRATION_NOT_AUTHORITY`: لا ولادةَ هنا، ولا حكمَ ولادة، ولا
تجميدَ `E0`، ولا استيرادَ من `kernel/`، ولا تُبدَّل بهذه الوحدة مرتبةُ تعارضٍ
مُسجَّلٍ في وحدةٍ أخرى.

المصدر: مدوَّنة القرآن الصرفية، http://corpus.quran.com — مبنيّةٌ على نصّ
تنزيل، http://tanzil.info. والإسنادُ إليهما شرطُ رخصةٍ لا لطفَ عبارة.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest

__all__ = [
    "ABSENCE_OF_A_TAG_IS_NOT_ABSENCE_OF_A_FORM_NOTE",
    "ARRIVING_FIGURES",
    "A_PERMUTATION_P_HAS_A_FLOOR_NOTE",
    "FREEZE_BEFORE_MEASUREMENT_NOTE",
    "PERMUTATION_PROTOCOL",
    "PRE_REGISTERED_EXPECTATION",
    "PROBE_PREREGISTRATION_DIGEST",
    "TRANSITIVITY_PROBE_NAMED_RESIDUALS",
    "THE_INDICATOR_AND_ITS_TEST_SHARE_A_PARENT_NOTE",
    "THE_MAXIMUM_NULL_GAP_IS_NOT_THE_P_VALUE_NOTE",
    "THE_SCHEMA_WAS_READ_BEFORE_THE_RULE_THE_RESULT_WAS_NOT_NOTE",
    "THIS_IS_REGISTRATION_NOT_AUTHORITY_NOTE",
    "UNTAGGED_CATEGORIES",
    "UNTAGGED_IS_LEFT_WITHOUT_A_NUMBER_NOT_WITH_A_ZERO_NOTE",
    "ArrivingFigure",
    "PermutationProtocol",
    "TransitivityClass",
    "TransitivityCountingRule",
    "TransitivityPreregistrationError",
    "UntaggedCategory",
    "preregistration_digest",
]


class TransitivityPreregistrationError(ValueError):
    """رفضٌ عند الإنشاء: قاعدةٌ بلا نصّ، أو بروتوكولٌ بلا عددِ تباديلَ موجب."""


FREEZE_BEFORE_MEASUREMENT_NOTE: Final[str] = (
    "FreezeBeforeMeasurement: ليس في هذه الوحدة دالّةُ قياسٍ ولا حقلُ نتيجة؛ "
    "واختبارٌ يُصاغ هدفُه بعد رؤية أوّل نتيجةٍ اختبارٌ بُني لينجح"
)

THE_SCHEMA_WAS_READ_BEFORE_THE_RULE_THE_RESULT_WAS_NOT_NOTE: Final[str] = (
    "TheSchemaWasReadBeforeTheRuleTheResultWasNot: المعلومُ في هذه المدوَّنة "
    "غيابُ PASS لا حضورُ ACT، والمجرَّدُ غيابُ وسمِ الوزن لا حضورُ (I)؛ "
    "وهاتان واقعتا مخطَّطٍ قُرِئتا قبل صياغة القاعدة، لا نتيجتا قياس"
)

ABSENCE_OF_A_TAG_IS_NOT_ABSENCE_OF_A_FORM_NOTE: Final[str] = (
    "AbsenceOfATagIsNotAbsenceOfAForm: «لا مجهولَ مجرَّدًا لهذا الجذر» حكمٌ "
    "على هذه المدوَّنة وحدها؛ ولذلك سُمّيت المجموعةُ مرشَّحًا لازمًا لا لازمًا"
)

THE_INDICATOR_AND_ITS_TEST_SHARE_A_PARENT_NOTE: Final[str] = (
    "TheIndicatorAndItsTestShareAParent: المجموعتان عُرِّفتا بحضور المجهول "
    "وغيابه، واسمُ المفعول صيغةٌ مجهولة؛ فالفرقُ بينهما تقاربُ مؤشّرَي تعدٍّ "
    "لا شاهدٌ مستقلٌّ عن التعريف"
)

A_PERMUTATION_P_HAS_A_FLOOR_NOTE: Final[str] = (
    "APermutationPHasAFloor: أصغرُ ما يُخرِجه اختبارُ التبديل "
    "(1 + المتجاوزات) / (1 + التباديل)، وهو هنا 1/5001؛ فـ p = 0.0000 تُسنِد "
    "إلى الاختبار دقّةً لا يملكها"
)

THE_MAXIMUM_NULL_GAP_IS_NOT_THE_P_VALUE_NOTE: Final[str] = (
    "TheMaximumNullGapIsNotThePValue: أقصى الفارق العدميّ إحصاءةٌ طرفيةٌ "
    "تتقلّب بعدد التباديل، وقد يقع فارقٌ دالٌّ دونها؛ فيُودَع وصفًا لا معيارًا"
)

UNTAGGED_IS_LEFT_WITHOUT_A_NUMBER_NOT_WITH_A_ZERO_NOTE: Final[str] = (
    "UntaggedIsLeftWithoutANumberNotWithAZero: ما لا تَسِمه المدوَّنةُ أصلًا "
    "يُترَك بلا رقم؛ وصفرٌ يُكتَب له يُقرأ غيابًا في العربية وهو غيابُ وَسْم"
)

THIS_IS_REGISTRATION_NOT_AUTHORITY_NOTE: Final[str] = (
    "ThisIsRegistrationNotAuthority: لا ولادةَ هنا ولا حكمَ ولادة ولا تجميدَ "
    "E0 ولا استيرادَ من kernel؛ ولا تُبدَّل بهذه الوحدة مرتبةُ تعارضٍ مُسجَّل"
)

TRANSITIVITY_PROBE_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "FreezeBeforeMeasurement": FREEZE_BEFORE_MEASUREMENT_NOTE,
    "TheSchemaWasReadBeforeTheRuleTheResultWasNot": (
        THE_SCHEMA_WAS_READ_BEFORE_THE_RULE_THE_RESULT_WAS_NOT_NOTE
    ),
    "AbsenceOfATagIsNotAbsenceOfAForm": ABSENCE_OF_A_TAG_IS_NOT_ABSENCE_OF_A_FORM_NOTE,
    "TheIndicatorAndItsTestShareAParent": (
        THE_INDICATOR_AND_ITS_TEST_SHARE_A_PARENT_NOTE
    ),
    "APermutationPHasAFloor": A_PERMUTATION_P_HAS_A_FLOOR_NOTE,
    "TheMaximumNullGapIsNotThePValue": THE_MAXIMUM_NULL_GAP_IS_NOT_THE_P_VALUE_NOTE,
    "UntaggedIsLeftWithoutANumberNotWithAZero": (
        UNTAGGED_IS_LEFT_WITHOUT_A_NUMBER_NOT_WITH_A_ZERO_NOTE
    ),
    "ThisIsRegistrationNotAuthority": THIS_IS_REGISTRATION_NOT_AUTHORITY_NOTE,
}


class TransitivityCountingRule(Enum):
    """قواعدُ العدّ بنصّها؛ ورقمٌ بلا واحدةٍ منها ليس عددًا.

    وهي قواعدُ عدِّ **جذورٍ** لا مقاطع: سؤالُ اللزوم والتعدّي يقع على الجذر،
    فتردُّدُ المقاطع لا يدخل في أيّ رقمٍ من أرقام هذا السبر.
    """

    TAGGED_ROOTS = (
        "الجذرُ الموسوم: قيمةُ ROOT متمايزةً في سمات أيّ مقطعٍ في الملفّ، "
        "أيًّا كان وَسْمُه؛ فجذرٌ لم يَرِد إلا في اسمٍ يُعَدّ هنا"
    )
    VERB_TAGGED_ROOTS = (
        "الجذرُ ذو الفعل: جذرٌ ورد في مقطعٍ وَسْمُه POS:V وفيه زمنٌ "
        "(PERF أو IMPF أو IMPV)؛ والأسماءُ وحدَها لا تُدخِل جذرًا هنا"
    )
    BARE_PERFECT_ACTIVE_ROOTS = (
        "الجذرُ ذو الماضي المجرَّد المعلوم: جذرٌ له مقطعٌ POS:V فيه PERF "
        "بلا وسمِ وزنٍ (II)…(XII) وبلا PASS؛ وهو مجالُ التقسيم كلِّه"
    )


class TransitivityClass(Enum):
    """قسمَا المجال، بتعريفهما المدوَّنيّ لا بتعريفٍ نحويٍّ مُستعار."""

    CONFIRMED_TRANSITIVE = (
        "متعدٍّ مؤكَّد: للجذر ماضٍ مجرَّدٌ معلومٌ **و** ماضٍ مجرَّدٌ مجهول "
        "في هذه المدوَّنة؛ والمجهولُ المجرَّدُ قرينةُ مفعولٍ به نائبٍ عن فاعل"
    )
    INTRANSITIVE_CANDIDATE = (
        "مرشَّحٌ لازم: للجذر ماضٍ مجرَّدٌ معلومٌ ولا مجهولَ مجرَّدَ له البتّة "
        "في هذه المدوَّنة؛ و«مرشَّح» لأنّ غيابَ الوَسْم ليس غيابَ الصيغة"
    )


@dataclass(frozen=True, slots=True)
class PermutationProtocol:
    """بروتوكولُ اختبار التبديل بأرقامه كاملةً قبل تشغيله.

    والبذرةُ والمولِّدُ يُصرَّح بهما لأنّ اختبارًا عشوائيًّا بلا بذرةٍ مُعلَنةٍ
    يُعاد اشتقاقُه تقريبًا لا حرفًا بحرف؛ وهذا نقضٌ لشرط إعادة الاشتقاق.
    """

    statistic: str
    permutations: int
    seed: int
    generator: str
    p_value_formula: str
    p_value_floor_numerator: int

    def __post_init__(self) -> None:
        for text, label in (
            (self.statistic, "نصُّ الإحصاءة"),
            (self.generator, "المولِّدُ العشوائيّ"),
            (self.p_value_formula, "صيغةُ p"),
        ):
            if not text.strip():
                raise TransitivityPreregistrationError(f"{label} نصٌّ غير فارغ.")
        if self.permutations < 1:
            raise TransitivityPreregistrationError(
                "عددُ التباديل عددٌ صحيحٌ موجب؛ واختبارٌ بلا تبديلٍ ليس اختبارًا."
            )
        if self.p_value_floor_numerator != 1:
            raise TransitivityPreregistrationError(
                "بسطُ حدِّ p واحدٌ بحكم صيغته (1 + المتجاوزات) عند صفر متجاوز."
            )

    @property
    def p_value_floor(self) -> float:
        """أصغرُ `p` يُخرِجها هذا البروتوكول؛ ولا يُخرِج صفرًا البتّة."""

        return self.p_value_floor_numerator / (1 + self.permutations)


PERMUTATION_PROTOCOL: Final[PermutationProtocol] = PermutationProtocol(
    statistic=(
        "القيمةُ المطلقةُ لفارق النسبتين بالنقاط المئوية بين المجموعتين، "
        "على متجهِ صفرٍ وواحدٍ لكلّ جذرٍ يحمل الخاصّيّة المسؤولَ عنها"
    ),
    permutations=5_000,
    seed=20_260_916,
    generator="random.Random(seed).shuffle — مولِّدُ مرسين تويستر في المكتبة القياسية",
    p_value_formula="(1 + عددُ التباديل التي فارقُها ≥ الفارق المرصود) / (1 + التباديل)",
    p_value_floor_numerator=1,
)
"""البروتوكولُ بأرقامه؛ وتبديلُ البذرة بعد رؤية `p` يجعل الاختيارَ نتيجةً."""


@dataclass(frozen=True, slots=True)
class UntaggedCategory:
    """بابٌ صرفيٌّ لا تَسِمه المدوَّنةُ أصلًا، ولمَ لا يصلح بديلُه المتاح."""

    arabic_name: str
    why_it_is_not_measurable_here: str
    nearest_available_tag: str
    why_the_nearest_tag_is_not_it: str

    def __post_init__(self) -> None:
        for text, label in (
            (self.arabic_name, "اسمُ الباب"),
            (self.why_it_is_not_measurable_here, "سببُ تعذُّر القياس"),
            (self.nearest_available_tag, "أقربُ وَسْمٍ متاح"),
            (self.why_the_nearest_tag_is_not_it, "سببُ عدم إجزاء الوَسْم"),
        ):
            if not text.strip():
                raise TransitivityPreregistrationError(f"{label} نصٌّ غير فارغ.")


UNTAGGED_CATEGORIES: Final[tuple[UntaggedCategory, ...]] = (
    UntaggedCategory(
        arabic_name="المصدر",
        why_it_is_not_measurable_here="ليس في سمات المدوَّنة وَسْمٌ للمصدر البتّة",
        nearest_available_tag="POS:N",
        why_the_nearest_tag_is_not_it=(
            "وَسْمُ الاسم يجمع المصدرَ وغيرَه، ففرزُ المصادر منه يحتاج حكمًا "
            "من عندنا لا وَسْمًا من عند المُوسِّمين"
        ),
    ),
    UntaggedCategory(
        arabic_name="اسمُ المكان الصرفيّ",
        why_it_is_not_measurable_here="لا وَسْمَ لصيغة مَفْعَل ولا لما في معناها",
        nearest_available_tag="POS:LOC",
        why_the_nearest_tag_is_not_it=(
            "LOC ظرفُ مكانٍ **نحويّ** يقع على كلماتٍ ليست اسمَ مكانٍ صرفيًّا، "
            "ويفوته اسمُ المكان حين لا يقع ظرفًا"
        ),
    ),
    UntaggedCategory(
        arabic_name="اسمُ الزمان الصرفيّ",
        why_it_is_not_measurable_here="لا وَسْمَ لصيغته، ولا تمييزَ لها عن اسم المكان",
        nearest_available_tag="POS:T",
        why_the_nearest_tag_is_not_it=(
            "T ظرفُ زمانٍ **نحويّ** لا صيغةٌ صرفية، فيقع على الجامد والمشتقّ معًا"
        ),
    ),
    UntaggedCategory(
        arabic_name="اسمُ الآلة",
        why_it_is_not_measurable_here="لا وَسْمَ لصيغة مِفْعَل ومِفْعال ومِفْعَلة",
        nearest_available_tag="POS:N",
        why_the_nearest_tag_is_not_it="الاسمُ يجمعها بغيرها، ولا فارزَ في السمات",
    ),
    UntaggedCategory(
        arabic_name="التمييز",
        why_it_is_not_measurable_here=(
            "وظيفةٌ نحويةٌ في شجرة الإعراب، وملفُّ الصرف لا يحمل وظائفَ نحوية"
        ),
        nearest_available_tag="ACC",
        why_the_nearest_tag_is_not_it=(
            "النصبُ حالةٌ إعرابيةٌ يشترك فيها التمييزُ والمفعولُ والحالُ وغيرُها"
        ),
    ),
)
"""خمسةُ أبوابٍ تُترَك بلا رقم؛ وكلُّ رقمٍ عنها من هذه البايتات اختلاق."""


@dataclass(frozen=True, slots=True)
class ArrivingFigure:
    """رقمٌ وصل مُصرَّحًا به في النصّ الوارد، مُجمَّدًا بنصّه قبل إعادة الاشتقاق.

    وإيداعُه هنا ليس تصديقًا له: هو تثبيتُ المُدَّعى كي يكون الفرقُ — إن وقع —
    **قابلًا للعرض** بدل أن تُعدَّل القاعدةُ حتى تُطابق.
    """

    label: str
    claimed_value: str
    counting_rule: TransitivityCountingRule

    def __post_init__(self) -> None:
        for text, field_label in (
            (self.label, "اسمُ الرقم"),
            (self.claimed_value, "قيمةُ الرقم كما وصلت"),
        ):
            if not text.strip():
                raise TransitivityPreregistrationError(f"{field_label} نصٌّ غير فارغ.")
        if not isinstance(self.counting_rule, TransitivityCountingRule):
            raise TransitivityPreregistrationError("لكلّ رقمٍ قاعدةُ عدٍّ مُسمّاة.")


ARRIVING_FIGURES: Final[tuple[ArrivingFigure, ...]] = (
    ArrivingFigure(
        label="الجذورُ الموسومة",
        claimed_value="1532",
        counting_rule=TransitivityCountingRule.TAGGED_ROOTS,
    ),
    ArrivingFigure(
        label="جذورٌ لها ماضٍ مجرَّدٌ معلوم",
        claimed_value="379",
        counting_rule=TransitivityCountingRule.BARE_PERFECT_ACTIVE_ROOTS,
    ),
    ArrivingFigure(
        label="متعدٍّ مؤكَّد",
        claimed_value="67",
        counting_rule=TransitivityCountingRule.BARE_PERFECT_ACTIVE_ROOTS,
    ),
    ArrivingFigure(
        label="مرشَّحٌ لازم",
        claimed_value="312",
        counting_rule=TransitivityCountingRule.BARE_PERFECT_ACTIVE_ROOTS,
    ),
    ArrivingFigure(
        label="مضارعٌ مجهولٌ مجرَّدٌ بلا ماضٍ مجهولٍ مجرَّد",
        claimed_value="46",
        counting_rule=TransitivityCountingRule.VERB_TAGGED_ROOTS,
    ),
    ArrivingFigure(
        label="الزمنان المجهولان المجرَّدان معًا",
        claimed_value="35",
        counting_rule=TransitivityCountingRule.VERB_TAGGED_ROOTS,
    ),
    ArrivingFigure(
        label="نسبةُ اسم الفاعل في المتعدّي المؤكَّد",
        claimed_value="65.7",
        counting_rule=TransitivityCountingRule.BARE_PERFECT_ACTIVE_ROOTS,
    ),
    ArrivingFigure(
        label="نسبةُ اسم المفعول في المتعدّي المؤكَّد",
        claimed_value="44.8",
        counting_rule=TransitivityCountingRule.BARE_PERFECT_ACTIVE_ROOTS,
    ),
    ArrivingFigure(
        label="نسبةُ اسم الفاعل في المرشَّح اللازم",
        claimed_value="44.2",
        counting_rule=TransitivityCountingRule.BARE_PERFECT_ACTIVE_ROOTS,
    ),
    ArrivingFigure(
        label="نسبةُ اسم المفعول في المرشَّح اللازم",
        claimed_value="17.3",
        counting_rule=TransitivityCountingRule.BARE_PERFECT_ACTIVE_ROOTS,
    ),
    ArrivingFigure(
        label="فارقُ اسم المفعول بالنقاط",
        claimed_value="27.47",
        counting_rule=TransitivityCountingRule.BARE_PERFECT_ACTIVE_ROOTS,
    ),
    ArrivingFigure(
        label="أقصى فارقٍ عدميٍّ في اسم المفعول",
        claimed_value="18.40",
        counting_rule=TransitivityCountingRule.BARE_PERFECT_ACTIVE_ROOTS,
    ),
    ArrivingFigure(
        label="لوازمُ لها مجهولٌ في وزنٍ مزيد",
        claimed_value="41",
        counting_rule=TransitivityCountingRule.BARE_PERFECT_ACTIVE_ROOTS,
    ),
    ArrivingFigure(
        label="نسبةُ المجهول المزيد في المرشَّح اللازم",
        claimed_value="13.1",
        counting_rule=TransitivityCountingRule.BARE_PERFECT_ACTIVE_ROOTS,
    ),
    ArrivingFigure(
        label="نسبةُ المجهول المزيد في المتعدّي المؤكَّد",
        claimed_value="16.4",
        counting_rule=TransitivityCountingRule.BARE_PERFECT_ACTIVE_ROOTS,
    ),
)
"""الأرقامُ الواردةُ بنصّها؛ ومطابقتُها أو مخالفتُها تُعرَض في وحدة القياس."""


PRE_REGISTERED_EXPECTATION: Final[str] = (
    "PreRegisteredExpectation: المُتوقَّعُ قبل تشغيل القياس ثلاثةُ أمور. "
    "**أوّلًا**: يفوق اسمُ المفعول في المتعدّي المؤكَّد نظيرَه في المرشَّح "
    "اللازم فوقًا لا يُفسَّر بالصدفة تحت بروتوكول التبديل المُجمَّد. **ثانيًا**: "
    "لا يستلزم وجودُ المجهول في أحد الزمنين وجودَه في الآخر داخل هذه "
    "المدوَّنة، فأداةُ اللزوم والتعدّي تفحص الزمنين معًا. **ثالثًا**: فرضيةُ "
    "«اللازمُ يصير متعدّيًا بالتزيّد» تُفنَّد كقاعدةٍ عامّة إن لم تتجاوز نسبةُ "
    "اللوازم ذاتِ المجهول المزيد النصفَ، وتُفنَّد كفارقٍ بين المجموعتين إن لم "
    "يكن فارقُهما دالًّا تحت البروتوكول نفسِه. ومطابقةُ التوقّع تأكيدٌ "
    "ومخالفتُه مفاجأةٌ تُوثَّق، ولا يُصاغ أحدُهما بعد وقوعه"
)


def preregistration_digest() -> str:
    """بصمةُ محتوى التسجيل القبْليّ؛ فزيادةُ بابٍ أو تبديلُ بذرةٍ تُغيّرها."""

    return canonical_digest(
        canonical_bytes(
            {
                "counting_rules": {
                    rule.name: rule.value for rule in TransitivityCountingRule
                },
                "classes": {item.name: item.value for item in TransitivityClass},
                "permutation_protocol": {
                    "statistic": PERMUTATION_PROTOCOL.statistic,
                    "permutations": PERMUTATION_PROTOCOL.permutations,
                    "seed": PERMUTATION_PROTOCOL.seed,
                    "generator": PERMUTATION_PROTOCOL.generator,
                    "p_value_formula": PERMUTATION_PROTOCOL.p_value_formula,
                },
                "untagged": [item.arabic_name for item in UNTAGGED_CATEGORIES],
                "arriving_figures": [
                    [item.label, item.claimed_value, item.counting_rule.name]
                    for item in ARRIVING_FIGURES
                ],
                "expectation": PRE_REGISTERED_EXPECTATION,
            }
        )
    )


PROBE_PREREGISTRATION_DIGEST: Final[str] = (
    "35f4635f80877089e8649c1f1d950c86318756b0fb0fcc3d1b355614729579ba"
)
"""البصمةُ المُجمَّدة؛ وحارسُ الاستيراد يرفض أيّ تبديلٍ صامتٍ بعد التجميد."""


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

    for dataclass_type in (PermutationProtocol, UntaggedCategory, ArrivingFigure):
        for field in fields(dataclass_type):
            lowered = field.name.lower()
            for marker in _FORBIDDEN_FIELD_MARKERS:
                if marker in lowered:
                    raise RuntimeError(
                        f"{dataclass_type.__name__}.{field.name} حقلٌ ممنوع: "
                        "هذه وحدةُ تجميدٍ قبل القياس. " + FREEZE_BEFORE_MEASUREMENT_NOTE
                    )


def _assert_the_registration_is_frozen() -> None:
    """احرسْ ثباتَ المُجمَّد ببصمةٍ مُعادةِ الاشتقاق من محتواه."""

    recomputed = preregistration_digest()
    if recomputed != PROBE_PREREGISTRATION_DIGEST:
        raise RuntimeError(
            "محتوى التسجيل القبْليّ تغيّر بعد تجميده: البصمةُ المُعادُ "
            f"اشتقاقُها {recomputed} تخالف المُجمَّدة "
            f"{PROBE_PREREGISTRATION_DIGEST}. " + FREEZE_BEFORE_MEASUREMENT_NOTE
        )


_assert_no_outcome_field()
_assert_the_registration_is_frozen()
