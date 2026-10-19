"""تسجيلٌ قبْليٌّ لقراءة P-EXTRACTOR: ترتيبُ قواعدها، ومتعذّرُها، وأرضيّتُها.

المواصفةُ المُودَعة في `docs/reference/gflk_arabic_letter_specification.md`
تصف «آلةَ حالةٍ» بمرورين: مرورٌ أوّلُ يُصنّف كلَّ حرفٍ أساسيّ، ومرورٌ ثانٍ
يحلّ المعلَّق **بترتيبٍ مذكور**. والترتيبُ ههنا ليس زينةً: قاعدةٌ تُطبَّق قبل
أختها تُغيّر ما تراه الأخت، فمن لم يُجمّد الترتيبَ قبل القراءة جاز له أن
يُبدّله بعدها حتّى يوافق الناتجُ ما أراد.

`THE_RULE_ORDER_IS_FROZEN_BEFORE_THE_READING`: القواعدُ الثمانِ مُجمَّدةٌ هنا
بترتيبها وبما تقرؤه من حقول `CarrierStateUnit`، وبصمةُ المُجمَّد في
`PREREGISTRATION_DIGEST`. ووحدةُ القراءة `p_extractor` تُطابق أسماءَها
وترتيبَها عند الاستيراد، فلا تُطبَّق قاعدةٌ لم تُسجَّل ولا تُهمَل قاعدةٌ
سُجِّلت.

`AN_UNDECIDABLE_RULE_IS_REGISTERED_NOT_GUESSED`: من القواعد الواردة ما لا
تحسمه العلاماتُ المكتوبة أصلًا — همزةُ الوصل وفرعُها الشمسيُّ/القمريّ —
وقرارُ هذه الشجرة سابقٌ لوصول المواصفة
(`ibtida_wasl_waqf_registration.HAMZAT_WASL_IS_NOT_DECIDABLE_FROM_THE_WRITTEN_MARKS`).
فتُسجَّل القاعدةُ متعذّرةً بحقلٍ مُسمًّى، ولا تُنفَّذ استدلالًا موضعيًّا
يُقرأ بعد جلساتٍ قراءةً للعلامات.

`A_ROLE_IS_NOT_A_STATE`: ما تسمّيه المواصفةُ «حالاتٍ» جديدةً يُقرأ **دورًا**
على `CarrierStateUnit` القائمة، ومفردةُ `CarrierState` تبقى مغلقةً بسبعة
أعضاء كما في `gflk_state_machine_registration.PROPOSED_STATE_READINGS`.

`REFUSAL_IS_NOT_A_MEMBER_OF_THE_VOCABULARY`: قاعدةُ الغموض الأخيرة لا تُخرِج
دورًا البتّة، بل سجلَّ تعذّرٍ في حقلٍ منفصل. والمواصفةُ نفسُها تُعلن في بندها
الأوّل أنّ DEFER ليست قيمةً ثالثة، فإدخالُها عضوًا ينقض بندَها الأوّل ببندها
الثاني.

`THE_FLOOR_IS_READ_NOT_RESTATED`: أرضيّةُ القبول مكتوبةٌ قبل هذه الجلسة في
`gflk_state_machine_registration.P_EXTRACTOR_ACCEPTANCE_CONDITION`، وتُقرأ من
موضعها ولا تُنسَخ هنا؛ ونسخُ شرطٍ في موضعين يُنتج شرطين يفترقان عند أوّل
تحرير. والمواضعُ الستّةُ المُسمّاةُ تُقرأ من
`gflk_codec_revision_audit.SILENT_OVERWRITE_LOCATIONS` كذلك.

`THIS_IS_REGISTRATION_NOT_AUTHORITY`: لا ولادةَ هنا، ولا حكمَ ولادة، ولا
تجميدَ `E0`، ولا استيرادَ من `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from alghanem.canonical_content import canonical_bytes, canonical_digest

from .encoding.carrier_state_candidate import CarrierStateUnit
from .gflk_codec_revision_audit import SILENT_OVERWRITE_LOCATIONS
from .gflk_state_machine_registration import (
    P_EXTRACTOR_ACCEPTANCE_CONDITION,
    AcceptanceCondition,
)

__all__ = [
    "AN_UNDECIDABLE_RULE_IS_REGISTERED_NOT_GUESSED_NOTE",
    "A_ROLE_IS_NOT_A_STATE_NOTE",
    "HARAKA_BEARING_DEFINITION",
    "PASS_TWO_RULES",
    "PREREGISTRATION_DIGEST",
    "P_EXTRACTOR_NAMED_RESIDUALS",
    "REFUSAL_IS_NOT_A_MEMBER_OF_THE_VOCABULARY_NOTE",
    "THE_FLOOR_IS_READ_NOT_RESTATED_NOTE",
    "THE_RULE_ORDER_IS_FROZEN_BEFORE_THE_READING_NOTE",
    "THIS_IS_REGISTRATION_NOT_AUTHORITY_NOTE",
    "UNREPRESENTED_SPECIFICATION_CATEGORIES",
    "PassTwoRule",
    "PExtractorPreregistrationError",
    "RuleDecidability",
    "RuleEmission",
    "UnrepresentedCategory",
    "acceptance_condition",
    "floor_named_cases",
    "preregistration_digest",
    "rule_named",
]


class PExtractorPreregistrationError(ValueError):
    """رفضٌ عند الإنشاء: قاعدةٌ بلا حقلٍ تقرؤه، أو متعذّرٌ يُخرِج دورًا."""


class RuleDecidability(Enum):
    """أتحسم العلاماتُ المكتوبةُ هذه القاعدةَ أم لا؟ مفردةٌ ثنائيّةٌ مغلقة."""

    DECIDABLE_FROM_THE_WRITTEN_MARKS = "تحسمها العلاماتُ المكتوبة"
    UNDECIDABLE_FROM_THE_WRITTEN_MARKS = "لا تحسمها العلاماتُ المكتوبة"


class RuleEmission(Enum):
    """ما تُخرِجه القاعدةُ عند انطباقها. ليس فيها `حالةٌ جديدة`."""

    ROLE_OVER_AN_EXISTING_UNIT = "دورٌ يُعلَّق على وحدةٍ قائمة"
    AMBIGUITY_RECORD = "سجلُّ غموضٍ في حقلٍ منفصل"
    UNDECIDED_SITE = "موضعُ تعذّرٍ يُسمّى ولا يُخمَّن"


_UNIT_FIELD_NAMES: Final[frozenset[str]] = frozenset(
    field.name for field in fields(CarrierStateUnit)
)


@dataclass(frozen=True, slots=True)
class PassTwoRule:
    """قاعدةٌ واحدةٌ من المرور الثاني: رتبتُها، وشرطُها، وما تقرؤه، وما تُخرِج."""

    order: int
    name: str
    trigger: str
    unit_fields_read: tuple[str, ...]
    decidability: RuleDecidability
    emission: RuleEmission
    emitted_role_name: str | None
    grounds: str

    def __post_init__(self) -> None:
        if isinstance(self.order, bool) or not isinstance(self.order, int):
            raise PExtractorPreregistrationError("رتبةُ القاعدة عددٌ صحيح")
        if self.order < 1:
            raise PExtractorPreregistrationError("رتبةُ القاعدة عددٌ موجب")
        for value, label in (
            (self.name, "اسمُ القاعدة"),
            (self.trigger, "شرطُ القاعدة"),
            (self.grounds, "مُبرِّرُ القاعدة"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise PExtractorPreregistrationError(f"{label} نصٌّ غير فارغ")
        if not isinstance(self.decidability, RuleDecidability):
            raise PExtractorPreregistrationError("حسمُ القاعدة عضوٌ في مفردته المغلقة")
        if not isinstance(self.emission, RuleEmission):
            raise PExtractorPreregistrationError("مُخرَجُ القاعدة عضوٌ في مفردته المغلقة")
        if not self.unit_fields_read:
            raise PExtractorPreregistrationError(
                "قاعدةٌ لا تقرأ حقلًا واحدًا من الوحدة القائمة قاعدةٌ تقرأ من "
                "مفردةٍ مُبتكَرةٍ لا من المرماز"
            )
        unknown = tuple(
            name for name in self.unit_fields_read if name not in _UNIT_FIELD_NAMES
        )
        if unknown:
            raise PExtractorPreregistrationError(
                f"حقولٌ لا وجودَ لها في `CarrierStateUnit`: {unknown!r}"
            )
        if self.emission is RuleEmission.ROLE_OVER_AN_EXISTING_UNIT:
            if not (self.emitted_role_name or "").strip():
                raise PExtractorPreregistrationError("قاعدةٌ تُخرِج دورًا بلا اسمِ دورٍ مُسمًّى")
        elif self.emitted_role_name is not None:
            raise PExtractorPreregistrationError(
                REFUSAL_IS_NOT_A_MEMBER_OF_THE_VOCABULARY_NOTE
            )
        if (
            self.decidability is RuleDecidability.UNDECIDABLE_FROM_THE_WRITTEN_MARKS
            and self.emission is RuleEmission.ROLE_OVER_AN_EXISTING_UNIT
        ):
            raise PExtractorPreregistrationError(
                AN_UNDECIDABLE_RULE_IS_REGISTERED_NOT_GUESSED_NOTE
            )

    def as_canonical_content(self) -> dict[str, object]:
        """صورةٌ قانونيّةٌ للبصمة؛ يتغيّر بندٌ فيها فتتغيّر البصمةُ كلُّها."""

        return {
            "order": self.order,
            "name": self.name,
            "trigger": self.trigger,
            "unit_fields_read": list(self.unit_fields_read),
            "decidability": self.decidability.name,
            "emission": self.emission.name,
            "emitted_role_name": self.emitted_role_name,
            "grounds": self.grounds,
        }


@dataclass(frozen=True, slots=True)
class UnrepresentedCategory:
    """فئةٌ في المواصفة لا تُخرِجها هذه القراءةُ، وسببُ تركها مُسمًّى."""

    category_name: str
    why_it_is_not_emitted: str
    what_would_admit_it: str

    def __post_init__(self) -> None:
        for value, label in (
            (self.category_name, "اسمُ الفئة"),
            (self.why_it_is_not_emitted, "سببُ تركها"),
            (self.what_would_admit_it, "شرطُ دخولها"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise PExtractorPreregistrationError(f"{label} نصٌّ غير فارغ")


PASS_TWO_RULES: Final[tuple[PassTwoRule, ...]] = (
    PassTwoRule(
        order=1,
        name="IDGHAM",
        trigger=(
            "وحدةٌ ساكنةٌ ضمنًا يليها نصفٌ أوّلُ من زوج تضعيفٍ مغايرُ الهويّة، "
            "فالأولى مُدغَمةٌ ساكتة"
        ),
        unit_fields_read=("carrier", "state", "gemination"),
        decidability=RuleDecidability.DECIDABLE_FROM_THE_WRITTEN_MARKS,
        emission=RuleEmission.ROLE_OVER_AN_EXISTING_UNIT,
        emitted_role_name="ASSIMILATED_SILENT",
        grounds=(
            "الشدّةُ مرصودةٌ في `GeminationRole.PAIR_START`، والمغايرةُ تُقرأ من "
            "حقل `carrier` وحدَه؛ فلا يُحتاج إلى معرفةٍ معجميّةٍ خارج العلامات"
        ),
    ),
    PassTwoRule(
        order=2,
        name="DOUBLED_WEAK_IDGHAM",
        trigger=("الشرطُ نفسُه بهويّةٍ مطابقةٍ والحرفُ من {و، ي}، فالأولى مُدغَمةٌ " "ساكتة"),
        unit_fields_read=("carrier", "state", "gemination"),
        decidability=RuleDecidability.DECIDABLE_FROM_THE_WRITTEN_MARKS,
        emission=RuleEmission.ROLE_OVER_AN_EXISTING_UNIT,
        emitted_role_name="ASSIMILATED_SILENT",
        grounds=(
            "تُفصَل عن سابقتها بالهويّة لا بالمُخرَج، فتبقى القاعدتان مُميَّزتين "
            "في السجلّ وإن اتّفق دورُهما"
        ),
    ),
    PassTwoRule(
        order=3,
        name="TANWEEN_ALIF_CARRIER",
        trigger=(
            "وحدةٌ حاملةٌ تنوينَ فتحٍ استهلكت ألفَ مَقعدٍ مكتوبةً بعدها "
            "(`tanwin_alif_seat`)، أو ألفٌ ساكنةٌ ضمنًا تلي مباشرةً وحدةً "
            "حاملةً تنوينَ فتحٍ؛ والصورتان اختلافُ ترتيبِ كتابةِ العلامةِ "
            "والألفِ لا اختلافُ ظاهرةٍ"
        ),
        unit_fields_read=("carrier", "seat", "tanwin", "tanwin_alif_seat", "state"),
        decidability=RuleDecidability.DECIDABLE_FROM_THE_WRITTEN_MARKS,
        emission=RuleEmission.ROLE_OVER_AN_EXISTING_UNIT,
        emitted_role_name="TANWEEN_ALIF_CARRIER",
        grounds=(
            "المرمازُ القائم لا يُنشئ للألف وحدةً مستقلّةً حين تُكتَب العلامةُ "
            "بعد الألف، بل يرصد استهلاكَها في `tanwin_alif_seat` على الوحدة "
            "السابقة؛ فالدورُ يُعلَّق حيث يُرصَد المَقعد، وفرقُ الموضع هذا "
            "مُسجَّلٌ تعارضًا لا مطويًّا"
        ),
    ),
    PassTwoRule(
        order=4,
        name="MADD_EXTENSION",
        trigger=(
            "مَقعدُ مدٍّ مكتوبٌ (آ)، أو حرفٌ من {ا، و، ي} ساكنٌ ضمنًا بعد حركةٍ "
            "مجانسةٍ له: فتحةٌ قبل الألف، ضمّةٌ قبل الواو، كسرةٌ قبل الياء"
        ),
        unit_fields_read=("carrier", "state", "seat", "tanwin", "gemination"),
        decidability=RuleDecidability.DECIDABLE_FROM_THE_WRITTEN_MARKS,
        emission=RuleEmission.ROLE_OVER_AN_EXISTING_UNIT,
        emitted_role_name="MADD_EXTENSION",
        grounds=(
            "المجانسةُ تُقرأ من حالة الوحدة السابقة وحرفِ هذه، وكلاهما مكتوب؛ "
            "و`CarrierSeat.MADD` قائمةٌ في المفردة فلا يُزاد لها عضو"
        ),
    ),
    PassTwoRule(
        order=5,
        name="WASL_LAM",
        trigger="ألفٌ عاريةٌ في أوّل الصورة يليها لام، بلا علامةٍ على أيّتهما",
        unit_fields_read=("carrier", "state", "seat"),
        decidability=RuleDecidability.UNDECIDABLE_FROM_THE_WRITTEN_MARKS,
        emission=RuleEmission.UNDECIDED_SITE,
        emitted_role_name=None,
        grounds=(
            "`HAMZAT_WASL_IS_NOT_DECIDABLE_FROM_THE_WRITTEN_MARKS` مكتوبٌ في "
            "`ibtida_wasl_waqf_registration` قبل وصول المواصفة: ألفُ «الْحَمْدُ» "
            "لا تحمل علامةً، فقراءتُها ألفَ وصلٍ معرفةٌ معجميّةٌ لا قراءةُ "
            "علامات. وفرعُ الشمسيّة/القمريّة تحتها فمتعذّرٌ تبعًا لها"
        ),
    ),
    PassTwoRule(
        order=6,
        name="SILENT_DIFFERENTIATING_ALIF",
        trigger=(
            "ألفٌ عاريةٌ بلا حركةٍ في آخر الصورة، قبلها واوٌ قُرِئت في القاعدة " "الرابعة مدًّا"
        ),
        unit_fields_read=("carrier", "state", "seat", "tanwin"),
        decidability=RuleDecidability.DECIDABLE_FROM_THE_WRITTEN_MARKS,
        emission=RuleEmission.ROLE_OVER_AN_EXISTING_UNIT,
        emitted_role_name="SILENT_DIFFERENTIATING_ALIF",
        grounds=(
            "الشرطُ كلُّه مكتوب: موضعُ الآخِر، وخلوُّ الألف من علامة، ودورُ "
            "الواو قبلها مُشتَقٌّ من قاعدةٍ سابقةٍ في الترتيب المُجمَّد"
        ),
    ),
    PassTwoRule(
        order=7,
        name="SHADDA_PAIR_START",
        trigger="وحدةٌ تحمل `GeminationRole.PAIR_START`",
        unit_fields_read=("gemination", "state"),
        decidability=RuleDecidability.DECIDABLE_FROM_THE_WRITTEN_MARKS,
        emission=RuleEmission.ROLE_OVER_AN_EXISTING_UNIT,
        emitted_role_name="SHADDA_PAIR_START",
        grounds=(
            "التضعيفُ مرصودٌ أصلًا، فالدورُ تسميةٌ لما في الوحدة لا محمولٌ " "يُضاف إليها"
        ),
    ),
    PassTwoRule(
        order=8,
        name="MADD_TANWEEN_AMBIGUITY",
        trigger=(
            "وحدةٌ قُرِئت مدًّا يليها مباشرةً ما قُرِئ حاملَ ألفِ تنوين، فلا "
            "يُفصَل أصلُ الجذر من المدّ"
        ),
        unit_fields_read=("carrier", "state", "tanwin_alif_seat"),
        decidability=RuleDecidability.DECIDABLE_FROM_THE_WRITTEN_MARKS,
        emission=RuleEmission.AMBIGUITY_RECORD,
        emitted_role_name=None,
        grounds=(
            "المواصفةُ تسمّيها «حالةَ DEFER صريحة» وتُدخلها مفردةَ الحالات، "
            "وبندُها الأوّل يمنع القيمةَ الثالثة؛ فتُخرَج سجلَّ تعذّرٍ في حقلٍ "
            "منفصلٍ حفظًا للبندين معًا"
        ),
    ),
)
"""القواعدُ الثمانِ بترتيب المواصفة، مُجمَّدةً قبل أن تُقرأ صورةٌ واحدة."""


UNREPRESENTED_SPECIFICATION_CATEGORIES: Final[tuple[UnrepresentedCategory, ...]] = (
    UnrepresentedCategory(
        category_name="ALIF_WASL",
        why_it_is_not_emitted=(
            "تمييزُ همزة الوصل من غيرها متعذّرٌ من العلامات المكتوبة، فإخراجُها "
            "دورًا يجعل استدلالًا موضعيًّا يُقرأ بعد جلساتٍ قراءةً للعلامات"
        ),
        what_would_admit_it=(
            "علامةٌ مكتوبةٌ تخصّها — كألف الوصل المرسومة `\u0671` — أو طبقةٌ "
            "معجميّةٌ مُبصَّمةٌ تُستشار صراحةً وتُنسَب إلى مصدرها"
        ),
    ),
    UnrepresentedCategory(
        category_name="MUQATTAAT_EXCLUDED",
        why_it_is_not_emitted=(
            "استبعادُ فواتح السور فئةٌ سياقيّةٌ تُعرَف من موضع الآية لا من "
            "صورة الكلمة، ولا تقرأ هذه الوحدةُ موضعًا من مدوَّنة"
        ),
        what_would_admit_it=(
            "مدخلٌ يُصرَّح فيه بموضع الكلمة من مدوَّنةٍ مُبصَّمة، وقاعدةُ "
            "استبعادٍ مكتوبةٌ قبل القياس"
        ),
    ),
    UnrepresentedCategory(
        category_name="IMPLICIT_SUKUN",
        why_it_is_not_emitted=(
            "قائمةٌ في المفردة سلفًا باسم `CarrierState.SUKUN_IMPLICIT`، "
            "فإعادتُها دورًا تُنتج اسمين لشيءٍ واحد"
        ),
        what_would_admit_it=(
            "لا شيء: `THE_SAME_CONCEPT_UNDER_TWO_NAMES_IS_ONE_ENTRY_NOT_TWO` "
            "يمنعه بنيويًّا"
        ),
    ),
)
"""فئاتٌ وردت في المواصفة ولا تُخرِجها هذه القراءةُ، بأسبابها وشروط دخولها."""


HARAKA_BEARING_DEFINITION: Final[str] = (
    "HarakaBearingIsADerivedPredicateNotAStoredFlag: الوحدةُ حاملةُ حركةٍ "
    "حقيقيّةٍ إن حملت فتحةً أو ضمّةً أو كسرةً — منوَّنةً أو غيرَ منوَّنة — ولم "
    "يُعلَّق عليها دورٌ من أدوار الإسكات (`ASSIMILATED_SILENT`، "
    "`MADD_EXTENSION`، `SILENT_DIFFERENTIATING_ALIF`). والحكمُ يُشتَقّ عند "
    "السؤال من الحالة والأدوار، ولا يُخزَّن حقلًا يُحرَّر على حدة"
)


THE_RULE_ORDER_IS_FROZEN_BEFORE_THE_READING_NOTE: Final[str] = (
    "TheRuleOrderIsFrozenBeforeTheReading: ترتيبُ القواعد مُجمَّدٌ ومُبصَّمٌ قبل "
    "قراءة صورةٍ واحدة؛ ومن قرأ أوّلًا ثمّ رتّب رتّب على مقاسِ ما قرأ"
)

AN_UNDECIDABLE_RULE_IS_REGISTERED_NOT_GUESSED_NOTE: Final[str] = (
    "AnUndecidableRuleIsRegisteredNotGuessed: ما لا تحسمه العلاماتُ المكتوبة "
    "يُسجَّل موضعَ تعذّرٍ ولا يُخرِج دورًا؛ فالدورُ المُخرَجُ عن استدلالٍ موضعيٍّ "
    "يُقرأ بعد جلساتٍ قراءةً للعلامات"
)

A_ROLE_IS_NOT_A_STATE_NOTE: Final[str] = (
    "ARoleIsNotAState: مفردةُ `CarrierState` تبقى مغلقةً بسبعة أعضاء، وما "
    "سمّته المواصفةُ حالةً يُعلَّق دورًا على الوحدة القائمة"
)

REFUSAL_IS_NOT_A_MEMBER_OF_THE_VOCABULARY_NOTE: Final[str] = (
    "RefusalIsNotAMemberOfTheVocabulary: الغموضُ يُخرَج في حقلٍ منفصلٍ لا "
    "عضوًا في مفردة الأدوار؛ وإلّا استوى «لم يُميَّز» و«تميَّز غموضًا»"
)

THE_FLOOR_IS_READ_NOT_RESTATED_NOTE: Final[str] = (
    "TheFloorIsReadNotRestated: أرضيّةُ القبول والمواضعُ الستّةُ تُقرآن من "
    "موضعيهما المكتوبين قبل هذه الجلسة، ولا يُنسَخ نصُّهما هنا"
)

THIS_IS_REGISTRATION_NOT_AUTHORITY_NOTE: Final[str] = (
    "تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`، ولا استيرادَ من "
    "`kernel/`، ولا تقرأ هذه الوحدةَ وحدةٌ فيه"
)

P_EXTRACTOR_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "THE_RULE_ORDER_IS_FROZEN_BEFORE_THE_READING": (
        THE_RULE_ORDER_IS_FROZEN_BEFORE_THE_READING_NOTE
    ),
    "AN_UNDECIDABLE_RULE_IS_REGISTERED_NOT_GUESSED": (
        AN_UNDECIDABLE_RULE_IS_REGISTERED_NOT_GUESSED_NOTE
    ),
    "A_ROLE_IS_NOT_A_STATE": A_ROLE_IS_NOT_A_STATE_NOTE,
    "REFUSAL_IS_NOT_A_MEMBER_OF_THE_VOCABULARY": (
        REFUSAL_IS_NOT_A_MEMBER_OF_THE_VOCABULARY_NOTE
    ),
    "HARAKA_BEARING_IS_A_DERIVED_PREDICATE": HARAKA_BEARING_DEFINITION,
    "THE_FLOOR_IS_READ_NOT_RESTATED": THE_FLOOR_IS_READ_NOT_RESTATED_NOTE,
    "THE_READING_IS_BOUNDED_BY_ONE_SURFACE": (
        "TheReadingIsBoundedByOneSurface: تُقرأ الصورةُ الواحدةُ وحدَها، فما "
        "احتاج إلى ما قبلها أو ما بعدها من الكلام — كالوقف والوصل — لا يُقرأ "
        "هنا ولا يُفتَرض"
    ),
    "THIS_IS_REGISTRATION_NOT_AUTHORITY": THIS_IS_REGISTRATION_NOT_AUTHORITY_NOTE,
}


def rule_named(name: str) -> PassTwoRule:
    """قاعدةٌ بعينها، مقروءةً من الجدول المُجمَّد لا مُنشأةً عند النداء."""

    for rule in PASS_TWO_RULES:
        if rule.name == name:
            return rule
    raise PExtractorPreregistrationError(
        f"لا قاعدةَ باسم {name!r}؛ والقواعدُ مُجمَّدةٌ بترتيبها"
    )


def acceptance_condition() -> AcceptanceCondition:
    """أرضيّةُ القبول، مقروءةً من موضعها السابق لهذه الجلسة لا منسوخةً هنا."""

    return P_EXTRACTOR_ACCEPTANCE_CONDITION


def floor_named_cases() -> tuple[tuple[int, int, int], ...]:
    """المواضعُ الستّةُ بأعيانها، مقروءةً من سجلّ التدقيق لا مكتوبةً هنا."""

    return tuple(token.location for token in SILENT_OVERWRITE_LOCATIONS)


_FLOOR: Final[AcceptanceCondition] = P_EXTRACTOR_ACCEPTANCE_CONDITION


def preregistration_digest() -> str:
    """بصمةُ المُجمَّد: يتغيّر بندٌ فيه فتتغيّر، فيسقط تحقّقُ وحدة القراءة."""

    return canonical_digest(
        canonical_bytes(
            {
                "pass_two_rules": [
                    rule.as_canonical_content() for rule in PASS_TWO_RULES
                ],
                "unrepresented_categories": [
                    {
                        "category_name": entry.category_name,
                        "why_it_is_not_emitted": entry.why_it_is_not_emitted,
                        "what_would_admit_it": entry.what_would_admit_it,
                    }
                    for entry in UNREPRESENTED_SPECIFICATION_CATEGORIES
                ],
                "haraka_bearing_definition": HARAKA_BEARING_DEFINITION,
                "acceptance_floor": {
                    "floor_description": _FLOOR.floor_description,
                    "floor_reference": _FLOOR.floor_reference,
                    "what_counts_as_regression": _FLOOR.what_counts_as_regression,
                    "explicit_test_cases": _FLOOR.explicit_test_cases,
                },
                "floor_named_cases": [
                    list(location) for location in floor_named_cases()
                ],
                "residuals": P_EXTRACTOR_NAMED_RESIDUALS,
            }
        )
    )


PREREGISTRATION_DIGEST: Final[str] = preregistration_digest()
"""بصمةُ التسجيل القبْليّ، تُشتَقّ عند الاستيراد ولا تُكتَب رقمًا يُنسَخ."""


if len(PASS_TWO_RULES) != len({rule.name for rule in PASS_TWO_RULES}):
    raise PExtractorPreregistrationError("اسمُ قاعدةٍ تكرّر، فالترتيبُ غيرُ مُميَّز")

if tuple(rule.order for rule in PASS_TWO_RULES) != tuple(
    range(1, len(PASS_TWO_RULES) + 1)
):
    raise PExtractorPreregistrationError("رتبُ القواعد متّصلةٌ من واحدٍ بلا فجوةٍ ولا تكرار")
