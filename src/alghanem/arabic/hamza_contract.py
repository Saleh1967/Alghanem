"""عقدُ الهمزة: أربعةُ حقولٍ مفصولةٍ في عقدٍ واحدٍ قابلٍ للفحص، ثمّ اختبارُها.

**الحكمُ المُودَع أوّلًا**: ليفُ الهمزة الحاليُّ — أي ما يحفظه `CarrierStateCodec`
عن الهمزة — صالحٌ لحفظ **بعض فروق الرسم**، ولا يُعتمَد ليفًا صوتيًّا مكتملًا،
ولا يُغلَق بحياد الألف ولادةُ المقطع. وليس هذا الحكمُ دعوًى ههنا: يُشتَقّ
بتشغيل المِرماز على وقوعاتٍ مُعلَنةٍ ثمّ عدِّ ما دمجه
(`THE_CODEC_KEEPS_SEATS_AND_MERGES_FUNCTIONS`).

**والعقدُ يفصل أربعةَ حقولٍ يجيب كلٌّ منها عن سؤالٍ غيرِ سؤال أخيه**:

====================  ===================================================
الحقل                 السؤال الذي يجيب عنه
====================  ===================================================
`identity`            أهذا الموضعُ همزةٌ أصلًا، أم ألفُ مدٍّ لا همزَ فيها؟
`seat`                على أيّ كرسيٍّ رُسمت في الخطّ؟
`function`            ما وظيفتُها في البنية: قطعٌ أم وصلٌ أم لا همز؟
`realization`         كيف تحقّقت في هذا المقام بعينه؟
====================  ===================================================

**والكرسيُّ وحدَه هو المفحوصُ من الخطّ**: `HamzaOccurrence` تُشغِّل المِرماز على
سطحها وتقابل ما قرأه بالكرسيّ المُسجَّل، فترفض وقوعًا سُجِّل كرسيُّه بخلاف ما
يقرؤه المِرماز. أمّا الوظيفةُ والتحقّقُ فـ**مُعلَنان بمصدرٍ مكتوبٍ لكلّ وقوع**،
لأنّ همزةَ الوصل لا تُعرَف من العلامات المكتوبة أصلًا، كما سبق تسميتُه في
`ibtida_wasl_waqf_registration.HAMZAT_WASL_IS_NOT_DECIDABLE_FROM_THE_WRITTEN_MARKS`
— فمن اشتقَّ الوظيفةَ من الرسم أدخل في القياس ما ليس فيه
(`FUNCTION_AND_REALIZATION_ARE_DECLARED_NOT_READ_FROM_THE_RASM`).

**والعقدُ يمنع التوليفات المتناقضة بنيويًّا لا بالتعليق**: فالوصلُ لا يُرسَم على
واوٍ ولا ياء، والسقوطُ في الدرج لا يكون إلّا لوصل، والمدُّ لا يكون إلّا على
كرسيّ المدّ، وانتفاءُ الهمز يلزمه انتفاءُ وظيفتها وتحقُّقِها معًا.

**ثمّ يُختبَر كلُّ حقلٍ اختبارين لا اختبارًا واحدًا**:

1. **الضرورة**: أيدمج حذفُه وقوعين يختلف مضمونُهما؟ فإن دمج، استحال قارئٌ يردُّ
   المضمونين من قيمةٍ واحدة، فالمعلومةُ لازمة.
2. **الاشتقاق**: أتُعيِّن الحقولُ الباقيةُ قيمتَه تعيينًا دالّيًّا على المجال؟
   فإن عيَّنته لم يلزم **تخزينُه**، وإن لزمت معلومتُه. والفرقُ بين لزوم
   المعلومة ولزوم الحقل هو موضعُ الخلط الأكبر.

وكلا الاختبارين مُقيَّدٌ بمجالٍ **مُعلَنٍ مصمَّمٍ** مكتوبٍ ههنا؛ فالتعيينُ
الدالّيُّ على مجالٍ منتهٍ ليس قاعدةَ اشتقاقٍ في العربية
(`FUNCTIONAL_DETERMINATION_ON_A_FINITE_DOMAIN_IS_NOT_A_DERIVATION_RULE`)، وقيامُ
العقد على هذا المجال ليس شهادةً لغويّة
(`THIS_CONTRACT_IS_NOT_A_COMPLETE_PHONETIC_FIBER`).

**ولا يُغلَق بحياد الألف شيء**: حيادُ الألف مقيسٌ في `alif_neutrality` على محورٍ
جُمِّد فيه المدُّ مؤجَّلًا، والألفُ أَولى الحوامل بحمله؛ فلا يُستعمَل ذلك
الحيادُ لإغلاق ولادة المقطع
(`ALIF_NEUTRALITY_MAY_NOT_CLOSE_SYLLABLE_BIRTH`).

ولا سلطةَ لهذه الوحدة: لا ولادةَ، ولا حكمَ ولادة، ولا تجميدَ، ولا استيرادَ من
`kernel/`.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from enum import Enum
from typing import Final

from .encoding.carrier_state_candidate import (
    CarrierSeat,
    CarrierStateCodec,
    CarrierStateUnit,
)

__all__ = [
    "ALIF_NEUTRALITY_MAY_NOT_CLOSE_SYLLABLE_BIRTH_NOTE",
    "A_MERGED_PAIR_IS_A_ROW_NOT_A_RATE_NOTE",
    "DETERMINATION_MAY_BE_AN_ARTIFACT_OF_THE_CONTRACTS_OWN_GUARDS_NOTE",
    "FUNCTIONAL_DETERMINATION_ON_A_FINITE_DOMAIN_IS_NOT_A_DERIVATION_RULE_NOTE",
    "FUNCTION_AND_REALIZATION_ARE_DECLARED_NOT_READ_FROM_THE_RASM_NOTE",
    "HAMZA_CONTRACT_NAMED_RESIDUALS",
    "THE_CODEC_KEEPS_SEATS_AND_MERGES_FUNCTIONS_NOTE",
    "THE_DECLARED_OCCURRENCES",
    "THE_SEAT_IS_RASM_NOT_SOUND_NOTE",
    "THIS_CONTRACT_IS_NOT_A_COMPLETE_PHONETIC_FIBER_NOTE",
    "WASL_IS_NOT_DECIDABLE_FROM_THE_WRITTEN_MARKS_NOTE",
    "CodecSeparationReport",
    "ComponentAssessment",
    "ContractField",
    "DerivabilityStanding",
    "HamzaContractError",
    "HamzaFunction",
    "HamzaIdentity",
    "HamzaOccurrence",
    "HamzaRealization",
    "HamzaSeat",
    "NecessityStanding",
    "alif_neutrality_may_close_syllable_birth",
    "assess_contract_fields",
    "assess_field",
    "codec_projection",
    "contract_projection",
    "delete_field",
    "measure_codec_separation",
    "seat_read_by_the_codec",
]


class HamzaContractError(ValueError):
    """رفضٌ صريح: كرسيٌّ يخالف المِرماز، أو توليفةٌ يمنعها العقدُ بنيويًّا."""


# --- الحقولُ الأربعة ----------------------------------------------------------


class ContractField(Enum):
    """حقولُ العقد الأربعة؛ وكلُّ واحدٍ يُختبَر حذفُه وحدَه."""

    IDENTITY = "الهويّة"
    SEAT = "الكرسيّ"
    FUNCTION = "الوظيفة"
    REALIZATION = "التحقّقُ_السياقيّ"


class HamzaIdentity(Enum):
    """أهمزةٌ هي أم لا؟ والألفُ الممدودةُ حرفٌ آخرُ لا همزَ فيه."""

    HAMZA = "همزة"
    NOT_A_HAMZA = "ليست_همزة"


class HamzaSeat(Enum):
    """الكرسيُّ المرسومُ في الخطّ؛ وهو **رسمٌ لا صوت**."""

    BARE = "مفردةٌ_على_السطر"
    ON_ALEF = "على_الألف"
    ON_ALEF_KASRA = "على_الألف_مكسورًا_ما_قبلها"
    ON_WAW = "على_الواو"
    ON_YEH = "على_الياء"
    ON_ALEF_MADDA = "على_ألف_المدّ"
    NO_HAMZA_SEAT = "لا_كرسيَّ_همزةٍ_في_الخطّ"


class HamzaFunction(Enum):
    """الوظيفةُ في البنية؛ مُعلَنةٌ بمصدرها لا مقروءةٌ من العلامات."""

    QAT = "قطع"
    WASL = "وصل"
    NO_HAMZA_FUNCTION = "لا_وظيفةَ_همزةٍ"


class HamzaRealization(Enum):
    """التحقّقُ في هذا المقام بعينه؛ وهو غيرُ الوظيفة."""

    REALIZED = "مُحقَّقةٌ_نطقًا"
    ELIDED_IN_WASL = "ساقطةٌ_في_الدرج"
    REALIZED_AT_IBTIDA_ONLY = "مُحقَّقةٌ_في_الابتداء_وحدَه"
    LENGTHENED = "مُحقَّقةٌ_ممدودة"
    NOT_A_HAMZA_REALIZATION = "لا_تحقّقَ_همزةٍ"


_SEAT_CODEPOINTS: Final[dict[HamzaSeat, CarrierSeat | None]] = {
    HamzaSeat.BARE: None,
    HamzaSeat.ON_ALEF: CarrierSeat.ON_ALEF,
    HamzaSeat.ON_ALEF_KASRA: CarrierSeat.ON_ALEF_KASRA,
    HamzaSeat.ON_WAW: CarrierSeat.ON_WAW,
    HamzaSeat.ON_YEH: CarrierSeat.ON_YEH,
    HamzaSeat.ON_ALEF_MADDA: CarrierSeat.MADD,
}
"""مقابلةُ كرسيّ العقد بما يقرؤه المِرماز؛ و`BARE` همزةٌ بلا كرسيٍّ مرسوم."""

_HAMZA_CARRIER: Final[str] = "\u0621"

_WASL_SEATS: Final[frozenset[HamzaSeat]] = frozenset({HamzaSeat.NO_HAMZA_SEAT})
_WASL_REALIZATIONS: Final[frozenset[HamzaRealization]] = frozenset(
    {HamzaRealization.ELIDED_IN_WASL, HamzaRealization.REALIZED_AT_IBTIDA_ONLY}
)
_QAT_REALIZATIONS: Final[frozenset[HamzaRealization]] = frozenset(
    {HamzaRealization.REALIZED, HamzaRealization.LENGTHENED}
)

_CODEC: Final[CarrierStateCodec] = CarrierStateCodec()


def seat_read_by_the_codec(surface: str, index: int) -> HamzaSeat:
    """اقرأ كرسيَّ الوحدة رقمَ `index` من سطحٍ بتشغيل المِرماز عليه.

    فالكرسيُّ **يُفحَص** ولا يُصدَّق: ما لم يقرأ المِرمازُ في ذلك الموضع حاملَ
    همزةٍ رُدَّ `NO_HAMZA_SEAT`، وهي حالُ ألفِ الوصل وألفِ المدّ في الخطّ.
    """

    units: tuple[CarrierStateUnit, ...] = _CODEC.generate(
        unicodedata.normalize("NFC", surface)
    )
    if not 0 <= index < len(units):
        raise HamzaContractError("موضعٌ خارجَ وحدات السطح؛ ولا يُفحَص ما لا يُقرأ")
    unit = units[index]
    if unit.carrier != _HAMZA_CARRIER:
        return HamzaSeat.NO_HAMZA_SEAT
    for seat, carrier_seat in _SEAT_CODEPOINTS.items():
        if unit.seat is carrier_seat:
            return seat
    raise HamzaContractError(  # pragma: no cover - كرسيٌّ لم يُقابَل بعدُ
        "كرسيٌّ قرأه المِرمازُ ولا مقابلَ له في العقد؛ ولا يُسكَت عنه"
    )


@dataclass(frozen=True, slots=True)
class HamzaOccurrence:
    """وقوعٌ واحد: أربعةُ حقولٍ، ومقامُه، ومصدرُ ما أُعلِن منه.

    الكرسيُّ مفحوصٌ بتشغيل المِرماز على السطح؛ والوظيفةُ والتحقّقُ مُعلَنان
    بمصدرٍ مكتوب، لأنّهما لا يُقرآن من العلامات.
    """

    surface: str
    index: int
    identity: HamzaIdentity
    seat: HamzaSeat
    function: HamzaFunction
    realization: HamzaRealization
    context: str
    declared_source: str
    content: str

    def __post_init__(self) -> None:
        for name, value in (
            ("مقام", self.context),
            ("مصدر", self.declared_source),
            ("مضمون", self.content),
        ):
            if not value.strip():
                raise HamzaContractError(f"وقوعٌ بلا {name} مكتوبٍ لا يُفحَص")
        if self.seat is not seat_read_by_the_codec(self.surface, self.index):
            raise HamzaContractError(
                "الكرسيُّ المُسجَّل يخالف ما يقرؤه المِرماز من السطح؛ "
                "والكرسيُّ يُفحَص ولا يُصدَّق"
            )
        self._refuse_contradictory_combinations()

    def _refuse_contradictory_combinations(self) -> None:
        if self.identity is HamzaIdentity.NOT_A_HAMZA:
            if self.function is not HamzaFunction.NO_HAMZA_FUNCTION:
                raise HamzaContractError("ما ليس همزةً لا تكون له وظيفةُ همزة")
            if self.realization is not HamzaRealization.NOT_A_HAMZA_REALIZATION:
                raise HamzaContractError("ما ليس همزةً لا يكون له تحقّقُ همزة")
            return
        if self.function is HamzaFunction.NO_HAMZA_FUNCTION:
            raise HamzaContractError("همزةٌ بلا وظيفةٍ مُعلَنةٍ لا تُفحَص وظيفتُها")
        if self.realization is HamzaRealization.NOT_A_HAMZA_REALIZATION:
            raise HamzaContractError("همزةٌ بلا تحقّقٍ مُعلَنٍ لا يُفحَص تحقّقُها")
        if self.function is HamzaFunction.WASL:
            if self.seat not in _WASL_SEATS:
                raise HamzaContractError(
                    "همزةُ الوصل لا تُرسَم على كرسيّ همزةٍ في الخطّ؛ "
                    "ولا يُسجَّل لها كرسيٌّ لم يُرسَم"
                )
            if self.realization not in _WASL_REALIZATIONS:
                raise HamzaContractError(
                    "تحقّقُ همزة الوصل سقوطٌ في الدرج أو نطقٌ في الابتداء، لا غير"
                )
            return
        if self.realization not in _QAT_REALIZATIONS:
            raise HamzaContractError(
                "السقوطُ في الدرج والاختصاصُ بالابتداء من شأن الوصل لا القطع"
            )
        if (self.realization is HamzaRealization.LENGTHENED) != (
            self.seat is HamzaSeat.ON_ALEF_MADDA
        ):
            raise HamzaContractError(
                "المدُّ في التحقّق يلازم كرسيَّ المدّ في الخطّ؛ ولا ينفكّ أحدُهما"
            )

    @property
    def is_a_complete_phonetic_description(self) -> bool:
        """أهو وصفٌ صوتيٌّ مكتمل؟ لا — والجوابُ ثابتٌ بالبناء لا بالحال."""

        return False


def contract_projection(
    occurrence: HamzaOccurrence,
) -> tuple[str | None, str | None, str | None, str | None]:
    """مخرجُ العقد كاملًا: أربعةُ حقولٍ لا يُطوى منها شيء."""

    return (
        occurrence.identity.value,
        occurrence.seat.value,
        occurrence.function.value,
        occurrence.realization.value,
    )


def codec_projection(occurrence: HamzaOccurrence) -> tuple[str, str | None]:
    """ما يحفظه المِرمازُ وحدَه عن هذا الموضع: الحاملُ وكرسيُّه، لا أكثر."""

    units = _CODEC.generate(unicodedata.normalize("NFC", occurrence.surface))
    unit = units[occurrence.index]
    return (unit.carrier, None if unit.seat is None else unit.seat.value)


def delete_field(
    occurrence: HamzaOccurrence, field: ContractField
) -> tuple[str | None, ...]:
    """`T_{-i}`: مخرجُ العقد بعد إسقاط معلومات الحقل المُسمّى وحدَه."""

    if not isinstance(field, ContractField):
        raise HamzaContractError("حقلٌ غيرُ مُسمًّى؛ ولا يُسقَط ما لا يُسمّى")
    projected = list(contract_projection(occurrence))
    order = (
        ContractField.IDENTITY,
        ContractField.SEAT,
        ContractField.FUNCTION,
        ContractField.REALIZATION,
    )
    projected[order.index(field)] = None
    return tuple(projected)


# --- الاختباران: الضرورةُ والاشتقاق -------------------------------------------


class NecessityStanding(Enum):
    """أيدمج حذفُ الحقل وقوعين يختلف مضمونُهما على هذا المجال؟"""

    NECESSARY_ON_THIS_DOMAIN = "لازمةٌ_على_هذا_المجال"
    NOT_SHOWN_NECESSARY_ON_THIS_DOMAIN = "لم_تلزم_على_هذا_المجال"


class DerivabilityStanding(Enum):
    """أتُعيِّن الحقولُ الباقيةُ قيمةَ هذا الحقل تعيينًا دالّيًّا على المجال؟"""

    DETERMINED_BY_THE_OTHER_FIELDS = "مُعيَّنةٌ_بالحقول_الباقية"
    NOT_DETERMINED_BY_THE_OTHER_FIELDS = "غيرُ_مُعيَّنةٍ_بالحقول_الباقية"


@dataclass(frozen=True, slots=True)
class ComponentAssessment:
    """حكمُ حقلٍ واحد بالاختبارين معًا، مع صفوف الشواهد لا رقمٍ مُلخَّص."""

    field: ContractField
    necessity: NecessityStanding
    derivability: DerivabilityStanding
    merged_contents: tuple[tuple[str, ...], ...]
    undetermined_values: tuple[tuple[str, ...], ...]

    @property
    def the_information_is_required(self) -> bool:
        """أتلزم **معلومةُ** هذا الحقل؟ يُقرَأ من اختبار الضرورة وحدَه."""

        return self.necessity is NecessityStanding.NECESSARY_ON_THIS_DOMAIN

    @property
    def a_separate_field_is_required(self) -> bool:
        """أيلزم **حقلٌ** مستقلٌّ له؟ لا متى عيَّنته الحقولُ الباقية.

        ولزومُ المعلومة غيرُ لزوم الحقل؛ والخلطُ بينهما هو الذي يُقرَأ إسقاطًا.
        """

        return self.the_information_is_required and (
            self.derivability is DerivabilityStanding.NOT_DETERMINED_BY_THE_OTHER_FIELDS
        )


def _require_domain(occurrences: tuple[HamzaOccurrence, ...]) -> None:
    if not occurrences:
        raise HamzaContractError("مجالٌ خالٍ تُثبَت عليه كلُّ دعوى")


def assess_field(
    field: ContractField, occurrences: tuple[HamzaOccurrence, ...]
) -> ComponentAssessment:
    """اختبر حقلًا اختبارين: أيدمج حذفُه مضمونين، وأتُعيِّنه الحقولُ الباقية."""

    _require_domain(occurrences)
    if not isinstance(field, ContractField):
        raise HamzaContractError("حقلٌ غيرُ مُسمًّى؛ ولا يُختبَر ما لا يُسمّى")

    by_deletion: dict[tuple[str | None, ...], set[str]] = {}
    by_remainder: dict[tuple[str | None, ...], set[str | None]] = {}
    order = (
        ContractField.IDENTITY,
        ContractField.SEAT,
        ContractField.FUNCTION,
        ContractField.REALIZATION,
    )
    position = order.index(field)
    for occurrence in occurrences:
        deleted = delete_field(occurrence, field)
        by_deletion.setdefault(deleted, set()).add(occurrence.content)
        by_remainder.setdefault(deleted, set()).add(
            contract_projection(occurrence)[position]
        )

    merged = tuple(
        tuple(sorted(contents))
        for contents in by_deletion.values()
        if len(contents) > 1
    )
    undetermined = tuple(
        tuple(sorted(value for value in values if value is not None))
        for values in by_remainder.values()
        if len(values) > 1
    )

    return ComponentAssessment(
        field=field,
        necessity=(
            NecessityStanding.NECESSARY_ON_THIS_DOMAIN
            if merged
            else NecessityStanding.NOT_SHOWN_NECESSARY_ON_THIS_DOMAIN
        ),
        derivability=(
            DerivabilityStanding.NOT_DETERMINED_BY_THE_OTHER_FIELDS
            if undetermined
            else DerivabilityStanding.DETERMINED_BY_THE_OTHER_FIELDS
        ),
        merged_contents=merged,
        undetermined_values=undetermined,
    )


def assess_contract_fields(
    occurrences: tuple[HamzaOccurrence, ...],
) -> tuple[ComponentAssessment, ...]:
    """اختبر الحقولَ الأربعةَ كلَّها؛ وتُذكَر كلُّها أو لا تُذكَر."""

    return tuple(assess_field(field, occurrences) for field in ContractField)


# --- ما يحفظه المِرمازُ وما يدمجه ----------------------------------------------


@dataclass(frozen=True, slots=True)
class CodecSeparationReport:
    """ما فرَّقه المِرمازُ وما دمجه على المجال، صفوفًا لا نسبةً مئويّة."""

    distinct_codec_outputs: int
    distinct_contract_outputs: int
    merged_by_the_codec: tuple[tuple[str, ...], ...]
    seat_differences_kept: tuple[tuple[str, ...], ...]

    @property
    def the_codec_keeps_some_rasm_differences(self) -> bool:
        """أيحفظ المِرمازُ بعضَ فروق الرسم؟ يُقرَأ من صفوف الكراسيّ المحفوظة."""

        return bool(self.seat_differences_kept)

    @property
    def the_codec_is_a_complete_phonetic_fiber(self) -> bool:
        """أهو ليفٌ صوتيٌّ مكتمل؟ لا ما دام يدمج مضمونين مختلفين."""

        return not self.merged_by_the_codec


def measure_codec_separation(
    occurrences: tuple[HamzaOccurrence, ...],
) -> CodecSeparationReport:
    """شغِّل المِرمازَ على المجال، وأحصِ ما دمجه بمضمونه لا بوصفه."""

    _require_domain(occurrences)
    by_codec: dict[tuple[str, str | None], set[str]] = {}
    seats_by_codec: dict[tuple[str, str | None], set[str]] = {}
    for occurrence in occurrences:
        key = codec_projection(occurrence)
        by_codec.setdefault(key, set()).add(occurrence.content)
        seats_by_codec.setdefault(key, set()).add(occurrence.seat.value)

    kept = tuple(
        sorted(
            tuple(sorted(seats))
            for key, seats in seats_by_codec.items()
            if key[0] == _HAMZA_CARRIER
        )
    )
    return CodecSeparationReport(
        distinct_codec_outputs=len(by_codec),
        distinct_contract_outputs=len(
            {contract_projection(item) for item in occurrences}
        ),
        merged_by_the_codec=tuple(
            tuple(sorted(contents))
            for contents in by_codec.values()
            if len(contents) > 1
        ),
        seat_differences_kept=kept,
    )


def alif_neutrality_may_close_syllable_birth() -> bool:
    """أيُغلَق بحياد الألف ولادةُ المقطع؟ لا — والمانعُ مُسمًّى لا مُقدَّر.

    فحيادُ الألف مقيسٌ على محاورَ جُمِّد فيها المدُّ مؤجَّلًا، والألفُ أَولى
    الحوامل بحمله؛ فقد يكون الحيادُ أثرَ التأجيل لا خاصّيّةً فيها.
    """

    return False


# --- المجالُ المُعلَن ----------------------------------------------------------


THE_DECLARED_OCCURRENCES: Final[tuple[HamzaOccurrence, ...]] = (
    HamzaOccurrence(
        surface="\u0623",
        index=0,
        identity=HamzaIdentity.HAMZA,
        seat=HamzaSeat.ON_ALEF,
        function=HamzaFunction.QAT,
        realization=HamzaRealization.REALIZED,
        context="فاءُ الكلمة في «أَكَلَ»، مبتدأً به ومدرَجًا سواء",
        declared_source="إعلانُ هذه الوحدة، لا قراءةٌ من العلامات",
        content="همزةُ قطعٍ محقَّقةٌ على كرسيّ الألف",
    ),
    HamzaOccurrence(
        surface="\u0623",
        index=0,
        identity=HamzaIdentity.HAMZA,
        seat=HamzaSeat.ON_ALEF,
        function=HamzaFunction.QAT,
        realization=HamzaRealization.REALIZED,
        context="همزةُ الاستفهام الداخلةُ على الجملة، لا فاءَ كلمة",
        declared_source="إعلانُ هذه الوحدة، لا قراءةٌ من العلامات",
        content="همزةُ قطعٍ محقَّقةٌ على كرسيّ الألف",
    ),
    HamzaOccurrence(
        surface="\u0625",
        index=0,
        identity=HamzaIdentity.HAMZA,
        seat=HamzaSeat.ON_ALEF_KASRA,
        function=HamzaFunction.QAT,
        realization=HamzaRealization.REALIZED,
        context="مفتتحُ «إِذَا»، والكسرُ مكتوبٌ تحت الألف",
        declared_source="إعلانُ هذه الوحدة، لا قراءةٌ من العلامات",
        content="همزةُ قطعٍ محقَّقةٌ على كرسيّ الألف مكسورًا",
    ),
    HamzaOccurrence(
        surface="\u0624",
        index=0,
        identity=HamzaIdentity.HAMZA,
        seat=HamzaSeat.ON_WAW,
        function=HamzaFunction.QAT,
        realization=HamzaRealization.REALIZED,
        context="عينُ الكلمة في «سُؤَال»، والكرسيُّ واوٌ",
        declared_source="إعلانُ هذه الوحدة، لا قراءةٌ من العلامات",
        content="همزةُ قطعٍ محقَّقةٌ على كرسيّ الواو",
    ),
    HamzaOccurrence(
        surface="\u0626",
        index=0,
        identity=HamzaIdentity.HAMZA,
        seat=HamzaSeat.ON_YEH,
        function=HamzaFunction.QAT,
        realization=HamzaRealization.REALIZED,
        context="عينُ الكلمة في «سَائِل»، والكرسيُّ ياءٌ",
        declared_source="إعلانُ هذه الوحدة، لا قراءةٌ من العلامات",
        content="همزةُ قطعٍ محقَّقةٌ على كرسيّ الياء",
    ),
    HamzaOccurrence(
        surface="\u0621",
        index=0,
        identity=HamzaIdentity.HAMZA,
        seat=HamzaSeat.BARE,
        function=HamzaFunction.QAT,
        realization=HamzaRealization.REALIZED,
        context="لامُ الكلمة في «شَيْء»، والهمزةُ مفردةٌ على السطر",
        declared_source="إعلانُ هذه الوحدة، لا قراءةٌ من العلامات",
        content="همزةُ قطعٍ محقَّقةٌ بلا كرسيّ",
    ),
    HamzaOccurrence(
        surface="\u0622",
        index=0,
        identity=HamzaIdentity.HAMZA,
        seat=HamzaSeat.ON_ALEF_MADDA,
        function=HamzaFunction.QAT,
        realization=HamzaRealization.LENGTHENED,
        context="مفتتحُ «آمَنَ»، والمدُّ مرسومٌ على الألف",
        declared_source="إعلانُ هذه الوحدة، لا قراءةٌ من العلامات",
        content="همزةُ قطعٍ ممدودةٌ على ألف المدّ",
    ),
    HamzaOccurrence(
        surface="\u0627",
        index=0,
        identity=HamzaIdentity.HAMZA,
        seat=HamzaSeat.NO_HAMZA_SEAT,
        function=HamzaFunction.WASL,
        realization=HamzaRealization.ELIDED_IN_WASL,
        context="مفتتحُ «الْحَمْدُ» مدرَجًا بعد كلامٍ قبله",
        declared_source="إعلانٌ معجميٌّ صرفيّ؛ والعلاماتُ لا تقوله",
        content="همزةُ وصلٍ ساقطةٌ في الدرج",
    ),
    HamzaOccurrence(
        surface="\u0627",
        index=0,
        identity=HamzaIdentity.HAMZA,
        seat=HamzaSeat.NO_HAMZA_SEAT,
        function=HamzaFunction.WASL,
        realization=HamzaRealization.REALIZED_AT_IBTIDA_ONLY,
        context="مفتتحُ «الْحَمْدُ» مبتدأً به",
        declared_source="إعلانٌ معجميٌّ صرفيّ؛ والعلاماتُ لا تقوله",
        content="همزةُ وصلٍ منطوقةٌ في الابتداء",
    ),
    HamzaOccurrence(
        surface="\u0627",
        index=0,
        identity=HamzaIdentity.NOT_A_HAMZA,
        seat=HamzaSeat.NO_HAMZA_SEAT,
        function=HamzaFunction.NO_HAMZA_FUNCTION,
        realization=HamzaRealization.NOT_A_HAMZA_REALIZATION,
        context="ألفُ المدّ في «قَالَ» بعد فتحةٍ مكتوبة",
        declared_source="إعلانُ هذه الوحدة، لا قراءةٌ من العلامات",
        content="ألفُ مدٍّ لا همزَ فيها",
    ),
)
"""مجالٌ مُعلَنٌ مصمَّمٌ لاختبار العقد؛ وليس مدوّنةً عربيّةً مُبصَّمة."""


# --- البواقي المُسمّاة --------------------------------------------------------


ALIF_NEUTRALITY_MAY_NOT_CLOSE_SYLLABLE_BIRTH_NOTE: Final[str] = (
    "AlifNeutralityMayNotCloseSyllableBirth: حيادُ الألف مقيسٌ على محاورَ "
    "جُمِّد فيها المدُّ مؤجَّلًا، والألفُ أَولى الحوامل بحمله؛ فقد يكون الحيادُ "
    "أثرَ التأجيل لا خاصّيّةً فيها، ولا يُغلَق به بابُ ولادة المقطع"
)

A_MERGED_PAIR_IS_A_ROW_NOT_A_RATE_NOTE: Final[str] = (
    "AMergedPairIsARowNotARate: ما دمجه المِرمازُ يُحفَظ صفوفًا بمضمونها في "
    "`merged_by_the_codec`، ولا يُلخَّص نسبةً مئويّة؛ فالنسبةُ تُخفي أيَّ "
    "فرقٍ ضاع، والصفُّ يُبقيه قابلًا للمراجعة"
)

FUNCTIONAL_DETERMINATION_ON_A_FINITE_DOMAIN_IS_NOT_A_DERIVATION_RULE_NOTE: Final[
    str
] = (
    "FunctionalDeterminationOnAFiniteDomainIsNotADerivationRule: تعيينُ الحقول "
    "الباقيةِ قيمةَ حقلٍ على مجالٍ منتهٍ مُعلَنٍ يمنع **تخزينَه** على ذلك "
    "المجال وحدَه؛ وليس قاعدةَ اشتقاقٍ في العربية، وقد ينقضه وقوعٌ واحدٌ خارجَه"
)

FUNCTION_AND_REALIZATION_ARE_DECLARED_NOT_READ_FROM_THE_RASM_NOTE: Final[str] = (
    "FunctionAndRealizationAreDeclaredNotReadFromTheRasm: وظيفةُ الهمزة "
    "وتحقّقُها مُعلَنان لكلّ وقوعٍ بمصدرٍ مكتوب، ولا يُشتقّان من العلامات؛ "
    "والكرسيُّ وحدَه هو المفحوصُ بتشغيل المِرماز على السطح"
)

DETERMINATION_MAY_BE_AN_ARTIFACT_OF_THE_CONTRACTS_OWN_GUARDS_NOTE: Final[str] = (
    "DeterminationMayBeAnArtifactOfTheContractsOwnGuards: العقدُ يمنع بنيويًّا "
    "توليفاتٍ (كأن يكون لما ليس همزةً وظيفةُ همزة)، فقد يُعيَّن حقلٌ بالحقول "
    "الباقية لأنّ العقدَ منع ما سواه، لا لأنّ العربيةَ تُعيِّنه؛ فتعيينُ "
    "الهويّة والوظيفة ههنا يُقرَأ خبرًا عن العقد قبل أن يُقرَأ خبرًا عن اللغة"
)

THE_CODEC_KEEPS_SEATS_AND_MERGES_FUNCTIONS_NOTE: Final[str] = (
    "TheCodecKeepsSeatsAndMergesFunctions: المِرمازُ يفرّق كراسيَّ الهمزة "
    "فيحفظ بعضَ فروق الرسم، ويدمج وقوعاتٍ تختلف وظيفةً أو تحقّقًا؛ والحكمان "
    "مُشتقّان بتشغيله على المجال لا بقراءة نثره"
)

THE_SEAT_IS_RASM_NOT_SOUND_NOTE: Final[str] = (
    "TheSeatIsRasmNotSound: الكرسيُّ مقروءٌ من الخطّ، وليس وصفًا لمخرجٍ ولا "
    "صفةً صوتيّة؛ وحفظُ فروقه حفظُ رسمٍ لا قياسُ صوت"
)

THIS_CONTRACT_IS_NOT_A_COMPLETE_PHONETIC_FIBER_NOTE: Final[str] = (
    "ThisContractIsNotACompletePhoneticFiber: العقدُ يفصل أربعةَ حقولٍ ويمنع "
    "توليفاتٍ متناقضة، ويُختبَر على مجالٍ مصمَّمٍ مكتوبٍ ههنا؛ فلا يُعتمَد "
    "ليفًا صوتيًّا مكتملًا، ولا تُقرَأ نتائجُه شهادةً لغويّة"
)

WASL_IS_NOT_DECIDABLE_FROM_THE_WRITTEN_MARKS_NOTE: Final[str] = (
    "WaslIsNotDecidableFromTheWrittenMarks: ألفُ «الْحَمْدُ» لا تحمل علامةً، "
    "فلا يُعرَف كونُها همزةَ وصلٍ إلّا بمعرفةٍ معجميّةٍ أو صرفيّةٍ ليست في "
    "العلامات، كما سُمّي في `ibtida_wasl_waqf_registration`؛ فوظيفتُها في هذا "
    "العقد مُعلَنةٌ بمصدرها لا مقيسة"
)

HAMZA_CONTRACT_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    THE_SEAT_IS_RASM_NOT_SOUND_NOTE,
    FUNCTION_AND_REALIZATION_ARE_DECLARED_NOT_READ_FROM_THE_RASM_NOTE,
    WASL_IS_NOT_DECIDABLE_FROM_THE_WRITTEN_MARKS_NOTE,
    THE_CODEC_KEEPS_SEATS_AND_MERGES_FUNCTIONS_NOTE,
    A_MERGED_PAIR_IS_A_ROW_NOT_A_RATE_NOTE,
    FUNCTIONAL_DETERMINATION_ON_A_FINITE_DOMAIN_IS_NOT_A_DERIVATION_RULE_NOTE,
    DETERMINATION_MAY_BE_AN_ARTIFACT_OF_THE_CONTRACTS_OWN_GUARDS_NOTE,
    THIS_CONTRACT_IS_NOT_A_COMPLETE_PHONETIC_FIBER_NOTE,
    ALIF_NEUTRALITY_MAY_NOT_CLOSE_SYLLABLE_BIRTH_NOTE,
)
"""البواقي المُسمّاة؛ تُعَدّ في الاختبار ولا يُكتَب عددُها بجانبها."""
