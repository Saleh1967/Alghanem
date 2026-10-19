"""تسجيلُ حياد الألف والتاء المربوطة: نطاقان لا يُخلَطان، ودعوى لا تُختبَر هنا.

هذه الوحدةُ **تسجيلٌ** لا قياس: لا تعدّ حرفًا، ولا ترفع حاجزًا، ولا تُدخِل
الألفَ في جدول صفةٍ ولا مخرج — فالجدولان محجوبان أصلًا في
`gflk_feature_table_import_barrier` ولا تمسّهما هذه الوحدة.

`TWO_SCOPES_ARE_NOT_ONE_CLAIM`: ما وردَ في §٣ من المواصفة دعويان في نطاقين
مختلفين، وجمعُهما في عبارةٍ واحدةٍ («الألفُ محايدة») يُخفي أنّ إحداهما حيادٌ
تامٌّ والأخرى حيادٌ في ثلاثةٍ من أربعة:

* صفاتيًّا: N/A على المحاور الأربعة **معًا**، لا سلبًا افتراضيًّا في بعضها؛
* معلوماتيًّا: π(بها) = π(بدونها) في ثلاثة أدوارٍ وظيفيّة، وتخلّفُ المساواة
  في الرابع (حاملةُ ألف التنوين) حيث يُحذَف بحذفها خبرٌ صوتيٌّ فعليّ.

`THE_INFORMATIONAL_CLAIM_IS_NOT_TESTABLE_IN_THIS_TREE`: الدعوى المعلوماتيّةُ
تُقاس على الأدوار الأربعة مفروزةً. وقراءةُ `p_extractor` تفرز ثلاثةً منها
بالعلامات المكتوبة — حاملةَ التنوين، وحرفَ المدّ، والألفَ الفارقة — وتبقى
همزةُ الوصل متعذّرةً بنصّ
`ibtida_wasl_waqf_registration.HAMZAT_WASL_IS_NOT_DECIDABLE_FROM_THE_WRITTEN_MARKS`.
ودعوى «حيادٌ في ثلاثةٍ من أربعة» لا تُختبَر بفرزِ ثلاثةٍ: نصفُ الشرط ليس
الشرطَ، ونقصُ الدور الرابع ليس نقصَ دقّةٍ بل انعدامُ الطرف المُقابَل.

`WHAT_IS_COUNTABLE_IS_COUNTED_ELSEWHERE`: ما تعدّه الشجرةُ فعلًا في الألف
مكتوبٌ في `alif_state_raw_count` و`alif_carrier_inspection`، ولا يُعاد هنا ولا
يُلخَّص رقمًا ثانيًا.

`TAA_MARBUTA_IS_EXCLUDED_BY_CONVENTION_NOT_BY_NEUTRALITY`: التاءُ المربوطةُ
خارجَ الشبكة لسببٍ آخرَ جنسًا: لها مخرجٌ وصفةٌ عند النطق وصلًا. ونطقُها وصلًا
غيرُ مقروءٍ في هذه الشجرة في أيّ موضع، فاستبعادُها هنا استبعادٌ اصطلاحيٌّ
مُسجَّلٌ لا حيادٌ مُثبَت.

`THIS_IS_A_REGISTRATION_NOT_A_BIRTH`: لا حكمَ، ولا ولادة، ولا تجميدَ `E0`، ولا
استيرادَ من `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

__all__ = [
    "ALIF_FUNCTIONAL_ROLES",
    "ALIF_NEUTRALITY_REGISTRATION_NAMED_RESIDUALS",
    "ALIF_SCOPE_READINGS",
    "FEATURE_AXES",
    "TAA_MARBUTA_EXCLUSION",
    "TAA_MARBUTA_IS_EXCLUDED_BY_CONVENTION_NOT_BY_NEUTRALITY",
    "THE_INFORMATIONAL_CLAIM_IS_NOT_TESTABLE_IN_THIS_TREE",
    "THIS_IS_A_REGISTRATION_NOT_A_BIRTH",
    "TWO_SCOPES_ARE_NOT_ONE_CLAIM",
    "WHAT_IS_COUNTABLE_IS_COUNTED_ELSEWHERE",
    "AlifNeutralityRegistrationError",
    "AlifRoleRecord",
    "AlifScopeReading",
    "ConventionalExclusion",
    "NeutralityScope",
    "RoleSeparability",
    "separable_roles",
    "unseparable_roles",
]


class AlifNeutralityRegistrationError(ValueError):
    """رفضٌ عند الإنشاء: تسجيلٌ بلا مُبرِّر، أو حسمٌ أُقحِم في موضع التعذّر."""


class NeutralityScope(Enum):
    """نطاقا الدعوى. مفردةٌ ثنائيّةٌ مغلقة، وجمعُهما في نطاقٍ واحدٍ خلطٌ لا اختصار."""

    FEATURAL = "صفاتيًّا: محاورُ الجهر والإطباق والاستعلاء والأصالة"
    INFORMATIONAL = "معلوماتيًّا: إسقاطُ π لحركة الكلام مع الحرف وبدونه"


class RoleSeparability(Enum):
    """أيُفرَز هذا الدورُ من العلامات المكتوبة في هذه الشجرة؟ لا ثالثَ بينهما."""

    SEPARABLE_BY_THE_WRITTEN_MARKS = "يُفرَز بالعلامات المكتوبة"
    NOT_SEPARABLE_IN_THIS_TREE = "لا يُفرَز في هذه الشجرة"


FEATURE_AXES: Final[tuple[str, ...]] = (
    "جهر/همس",
    "إطباق/انفتاح",
    "استعلاء/استفال",
    "أصلي/زائد",
)
"""المحاورُ الأربعةُ كما وردت في المواصفة، مذكورةً لتُنفى عن الألف جميعًا معًا."""


@dataclass(frozen=True, slots=True)
class AlifRoleRecord:
    """دورٌ وظيفيٌّ واحدٌ للألف: أيُفرَز هنا، وأمحايدٌ معلوماتيًّا بنصّ المواصفة."""

    name: str
    description: str
    separability: RoleSeparability
    separability_grounds: str
    specification_calls_it_informationally_neutral: bool

    def __post_init__(self) -> None:
        for value, label in (
            (self.name, "اسمُ الدور"),
            (self.description, "وصفُ الدور"),
            (self.separability_grounds, "مُبرِّرُ الفرز أو تعذّره"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise AlifNeutralityRegistrationError(f"{label} نصٌّ غير فارغ")
        if not isinstance(self.separability, RoleSeparability):
            raise AlifNeutralityRegistrationError("الفرزُ عضوٌ في مفردته المغلقة")
        if not isinstance(self.specification_calls_it_informationally_neutral, bool):
            raise AlifNeutralityRegistrationError("الحيادُ المعلوماتيُّ قولٌ ثنائيّ")


ALIF_FUNCTIONAL_ROLES: Final[tuple[AlifRoleRecord, ...]] = (
    AlifRoleRecord(
        name="HAMZAT_WASL",
        description="همزةُ الوصل: ألفٌ ابتدائيّةٌ تسقط وصلًا وتُنطَق ابتداءً",
        separability=RoleSeparability.NOT_SEPARABLE_IN_THIS_TREE,
        separability_grounds=(
            "`HAMZAT_WASL_IS_NOT_DECIDABLE_FROM_THE_WRITTEN_MARKS` في "
            "`ibtida_wasl_waqf_registration`؛ وقاعدةُ «أل» في "
            "`p_extractor_preregistration` مُسجَّلةٌ متعذّرةً لا مُخمَّنة، "
            "فتخرج موضعًا في `PExtractorReading.undecided`"
        ),
        specification_calls_it_informationally_neutral=True,
    ),
    AlifRoleRecord(
        name="MADD_LETTER",
        description="حرفُ المدّ: ألفٌ تمتدّ بها فتحةٌ قبلها",
        separability=RoleSeparability.SEPARABLE_BY_THE_WRITTEN_MARKS,
        separability_grounds=(
            "`p_extractor.PhoneticRole.MADD_EXTENSION` تُعلَّق على الوحدة "
            "بقاعدةٍ مُسجَّلةٍ محسومةٍ بالعلامات المكتوبة"
        ),
        specification_calls_it_informationally_neutral=True,
    ),
    AlifRoleRecord(
        name="DIFFERENTIATING_ALIF",
        description="الألفُ الفارقة: بعد واو الجماعة آخرَ الصورة، لا تُنطَق",
        separability=RoleSeparability.SEPARABLE_BY_THE_WRITTEN_MARKS,
        separability_grounds=(
            "`p_extractor.PhoneticRole.SILENT_DIFFERENTIATING_ALIF`، وحدُّها "
            "مكتوبٌ: «آخرُ الصورة» لا «آخرُ نطقٍ في سياق» "
            "(`THE_READING_IS_BOUNDED_BY_ONE_SURFACE`)"
        ),
        specification_calls_it_informationally_neutral=True,
    ),
    AlifRoleRecord(
        name="TANWEEN_CARRIER",
        description="حاملةُ ألف التنوين: تحمل علامةَ تنوين الفتح ذاتها",
        separability=RoleSeparability.SEPARABLE_BY_THE_WRITTEN_MARKS,
        separability_grounds=(
            "`p_extractor.PhoneticRole.TANWEEN_ALIF_CARRIER` على صورتَي "
            "الكتابة معًا: `tanwin_alif_seat` على الوحدة السابقة، أو ألفٌ "
            "ساكنةٌ ضمنًا تلي وحدةً حاملةَ تنوينِ فتح"
        ),
        specification_calls_it_informationally_neutral=False,
    ),
)
"""الأدوارُ الأربعةُ كما وردت في المواصفة، وفرزُها في هذه الشجرة لا حكمُها."""


def separable_roles() -> tuple[AlifRoleRecord, ...]:
    """الأدوارُ المفروزةُ بالعلامات المكتوبة، مُشتقّةً لا مكتوبةً عددًا."""

    return tuple(
        role
        for role in ALIF_FUNCTIONAL_ROLES
        if role.separability is RoleSeparability.SEPARABLE_BY_THE_WRITTEN_MARKS
    )


def unseparable_roles() -> tuple[AlifRoleRecord, ...]:
    """الأدوارُ المتعذّرةُ في هذه الشجرة، مُشتقّةً لا مكتوبةً عددًا."""

    return tuple(
        role
        for role in ALIF_FUNCTIONAL_ROLES
        if role.separability is RoleSeparability.NOT_SEPARABLE_IN_THIS_TREE
    )


@dataclass(frozen=True, slots=True)
class AlifScopeReading:
    """قراءةُ دعوى الحياد في نطاقٍ واحدٍ بعينه، ومانعُ اختبارها إن وُجد."""

    scope: NeutralityScope
    what_the_specification_says: str
    what_this_tree_can_test: str
    what_blocks_the_test: str | None

    def __post_init__(self) -> None:
        if not isinstance(self.scope, NeutralityScope):
            raise AlifNeutralityRegistrationError("النطاقُ عضوٌ في مفردته المغلقة")
        for value, label in (
            (self.what_the_specification_says, "نصُّ المواصفة"),
            (self.what_this_tree_can_test, "ما تختبره الشجرة"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise AlifNeutralityRegistrationError(f"{label} نصٌّ غير فارغ")
        if self.what_blocks_the_test is not None and not (
            isinstance(self.what_blocks_the_test, str)
            and self.what_blocks_the_test.strip()
        ):
            raise AlifNeutralityRegistrationError(
                "المانعُ إمّا نصٌّ مُسمًّى وإمّا لا مانعَ؛ ولا يكون فراغًا يُقرأ " "انتفاءً"
            )


ALIF_SCOPE_READINGS: Final[tuple[AlifScopeReading, ...]] = (
    AlifScopeReading(
        scope=NeutralityScope.FEATURAL,
        what_the_specification_says=(
            "الألفُ N/A على المحاور الأربعة معًا، لا بقيمةٍ سلبيّةٍ افتراضيّةٍ "
            "في بعضها؛ فهي خارجَ الخانات الستّ عشرةَ كلِّها"
        ),
        what_this_tree_can_test=(
            "لا شيءَ: جدولُ الصفة لم يدخل الشجرةَ أصلًا، ولا بايتاتٍ له ولا "
            "بصمةَ ولا نسبة؛ والمحاورُ الأربعةُ مذكورةٌ هنا نقلًا لا إقرارًا"
        ),
        what_blocks_the_test=(
            "حاجزُ الاستيراد القائم في `gflk_feature_table_import_barrier`، "
            "وهو مفتوحٌ (`ImportBarrierStanding.OPEN`) ولا ترفعه هذه الوحدة"
        ),
    ),
    AlifScopeReading(
        scope=NeutralityScope.INFORMATIONAL,
        what_the_specification_says=(
            "π(بها) = π(بدونها) في ثلاثةٍ من الأدوار الأربعة، وتتخلّف "
            "المساواةُ في الرابع (حاملةُ التنوين) لأنّها تحمل العلامةَ ذاتها"
        ),
        what_this_tree_can_test=(
            "ثلاثةُ أدوارٍ من أربعةٍ تُفرَز بالعلامات المكتوبة بعد "
            "`p_extractor`؛ وهذا فرزُ الأدوار لا قياسُ π، فلا إسقاطَ للكلام "
            "مقيسًا في الشجرة أصلًا"
        ),
        what_blocks_the_test=(
            "همزةُ الوصل غيرُ مفروزة، والدعوى على الأربعة معًا؛ ونسبةُ «ثلاثةٍ "
            "من أربعة» لا تُختبَر بثلاثةٍ وحدَها"
        ),
    ),
)
"""قراءتا النطاقين، منفصلتين؛ وجمعُهما في سطرٍ واحدٍ هو الخلطُ المُحذَّرُ منه."""


@dataclass(frozen=True, slots=True)
class ConventionalExclusion:
    """استبعادٌ اصطلاحيٌّ مُسجَّل: سببُه، وما يُميِّزه عن الحياد، وما لا يُقرأ."""

    letter: str
    excluded_from: str
    why_it_is_not_neutrality: str
    what_this_tree_does_not_read: str

    def __post_init__(self) -> None:
        for value, label in (
            (self.letter, "الحرف"),
            (self.excluded_from, "موضعُ الاستبعاد"),
            (self.why_it_is_not_neutrality, "فرقُه عن الحياد"),
            (self.what_this_tree_does_not_read, "ما لا تقرؤه الشجرة"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise AlifNeutralityRegistrationError(f"{label} نصٌّ غير فارغ")


TAA_MARBUTA_EXCLUSION: Final[ConventionalExclusion] = ConventionalExclusion(
    letter="\u0629",
    excluded_from="شبكةُ المخرج والصفة في §٣ من المواصفة المُودَعة",
    why_it_is_not_neutrality=(
        "لها مخرجٌ وصفةٌ حقيقيّان عند النطق وصلًا — تُنطَق تاءً — فاستبعادُها "
        "اصطلاحيٌّ سياقيٌّ لا حيادٌ تامٌّ كالألف؛ والفرقُ جنسٌ لا درجة"
    ),
    what_this_tree_does_not_read=(
        "نطقُها وصلًا غيرُ مقروءٍ في أيّ موضعٍ من الشجرة: المرمازُ يقرأ الصورةَ "
        "الواحدةَ وحدَها، والوصلُ يحتاج ما بعدَها من الكلام"
    ),
)
"""التاءُ المربوطة: استبعادٌ مُسجَّلٌ بسببه، لا حيادٌ مُثبَتٌ ولا قياسٌ مُجرًى."""


TWO_SCOPES_ARE_NOT_ONE_CLAIM: Final[str] = (
    "TwoScopesAreNotOneClaim: حيادٌ صفاتيٌّ تامٌّ وحيادٌ معلوماتيٌّ في ثلاثةٍ "
    "من أربعةٍ دعويان في نطاقين؛ وجمعُهما في عبارةٍ واحدةٍ يُقرَأ تعميمًا "
    "لأوسعهما على أضيقهما"
)

THE_INFORMATIONAL_CLAIM_IS_NOT_TESTABLE_IN_THIS_TREE: Final[str] = (
    "TheInformationalClaimIsNotTestableInThisTree: الدعوى على أربعة أدوارٍ "
    "مفروزة، والمفروزُ هنا ثلاثةٌ؛ والرابعُ متعذّرٌ بحاجزٍ قائمٍ قبل وصول "
    "المواصفة، فالدعوى تُسجَّل ولا تُقاس"
)

WHAT_IS_COUNTABLE_IS_COUNTED_ELSEWHERE: Final[str] = (
    "WhatIsCountableIsCountedElsewhere: عدُّ حالات الألف قائمٌ في "
    "`alif_state_raw_count` وفحصُ صفوفه في `alif_carrier_inspection`؛ ولا "
    "تُعيد هذه الوحدةُ عدًّا ولا تُلخِّصه رقمًا ثانيًا"
)

TAA_MARBUTA_IS_EXCLUDED_BY_CONVENTION_NOT_BY_NEUTRALITY: Final[str] = (
    "TaaMarbutaIsExcludedByConventionNotByNeutrality: استبعادُ ة اصطلاحيٌّ "
    "وسببُه مكتوب؛ ومن ساواه بحياد الألف جعل غيابَ القياس حيادًا"
)

THIS_IS_A_REGISTRATION_NOT_A_BIRTH: Final[str] = (
    "ThisIsARegistrationNotABirth: تسجيلٌ بلا حكمٍ ولا ولادةٍ ولا تجميدٍ ولا "
    "رفعِ حاجز؛ ولا تقرؤه بوّابةٌ في `kernel/`"
)

ALIF_NEUTRALITY_REGISTRATION_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    TAA_MARBUTA_IS_EXCLUDED_BY_CONVENTION_NOT_BY_NEUTRALITY,
    THE_INFORMATIONAL_CLAIM_IS_NOT_TESTABLE_IN_THIS_TREE,
    THIS_IS_A_REGISTRATION_NOT_A_BIRTH,
    TWO_SCOPES_ARE_NOT_ONE_CLAIM,
    WHAT_IS_COUNTABLE_IS_COUNTED_ELSEWHERE,
)
"""البواقي المُسمّاةُ لهذه الوحدة، مرتّبةً كما تُرتَّب في بقيّة الطبقة."""


def _refuse_a_silently_dropped_role() -> None:
    """حارسٌ عند الاستيراد: الأدوارُ أربعةٌ بأسماءٍ متمايزة، ونطاقان لا أكثر."""

    names = [role.name for role in ALIF_FUNCTIONAL_ROLES]
    if len(set(names)) != len(names) or len(names) != 4:
        raise AlifNeutralityRegistrationError(
            "أدوارُ الألف أربعةٌ متمايزةٌ بنصّ المواصفة؛ ونقصُ دورٍ يُحوّل "
            "«ثلاثةٌ من أربعة» إلى نسبةٍ أخرى بصمت"
        )
    scopes = [reading.scope for reading in ALIF_SCOPE_READINGS]
    if len(set(scopes)) != len(scopes) or len(scopes) != len(NeutralityScope):
        raise AlifNeutralityRegistrationError("لكلّ نطاقٍ قراءةٌ واحدةٌ لا أكثر")


_refuse_a_silently_dropped_role()
