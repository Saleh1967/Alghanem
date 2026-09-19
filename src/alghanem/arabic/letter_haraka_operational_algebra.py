"""جبرٌ تشغيليٌّ للحرف والحركة: مُخرَجُه مدخلٌ مرخَّصٌ لاختبار CV، لا تعداد.

**ما هذه الوحدة**: عمليّةٌ تُجري، لا جدولٌ يُعَدّ. تأخذ وحداتِ (حامل، حالة) من
مِرماز الترميز، فتُخرِج عناصرَ مصنَّفةً في `X_C` و`X_V` بإسقاطَيها `π_I` و`π_Q`
مُشتَقَّين، ثمّ تعرضها أزواجًا على شروط التعريف المُجمَّدة في
`LICENSED_JOIN_SPECIFICATION`. فالمُخرَجُ **مدخلٌ مرخَّصٌ لـ`J`**، و`J` نفسُها
لا تُطبَّق ههنا (`THE_JOIN_IS_NOT_APPLIED_HERE`).

**ولا تعدادَ ٢٩×٤**: لا مفردةَ حروفٍ تُكتَب، ولا مجموعةَ علاماتٍ تُحصى. ما
يُبنى عنصرٌ عن وقوعٍ بعينه بموضعه وبرهانه؛ ومن لا يقع لا يُخترَع له عنصر
(`AN_ELEMENT_IS_AN_OCCURRENCE_NOT_AN_ALPHABET_CELL`).

**والبنيةُ الحاملةُ للوزن**: الحركةُ لا تقع بعد حاملها عنصرًا ثانيًا، بل تسكن
معه في وحدةٍ واحدة. فالجبرُ **يقسم** الوحدةَ الواحدة إلى موضعِ صامتٍ وموضعِ
صائتٍ **متزامنين**، ولا يرتّبهما في تسلسل. وهذا عينُ ما بُرهن في
`linearization_artifact`: الترتيبُ بين الحامل وحركته لا يحمل بتًّا.

**وثمنُ ذلك مُعلَنٌ لا مطويّ**: شرطُ التعريف الأوّل في المُجمَّد — «الصامتُ
يسبق الصائتَ بلا فاصل» — يصير **صادقًا بالبناء** تحت هذا القسم، إذ القاسمُ هو
الذي يضعهما متجاورين. فلا يجوز لاختبار CV أن يعدّ انعقادَه شاهدًا
(`THE_ADJACENCY_CONDITION_IS_TRUE_BY_CONSTRUCTION_NOT_BY_MEASUREMENT`).
والشرطان الآخران يبقيان قابلَين للفشل، وعليهما يقع العبء.

**وما لا يُعرَّف يُسمّى ولا يُرمَّم**: كمّيّةٌ لا تُشتَقّ، أو صائتٌ لا صامتَ
معه، أو شقٌّ ثانٍ من شدّةٍ سبق وصلُه — كلُّها تخرج `UNDEFINED` بعلّةٍ مكتوبة،
ولا يُصطنَع صامتٌ صفريّ ولا يُقرَّب الشكلُ إلى أقرب قالب.

**ولا ولادةَ ههنا**: لا حكمَ ولادةٍ كرنليًّا، ولا تجميدَ `E0`، ولا استيرادَ من
`kernel/`. وسقفُ ما تبلغه هذه الوحدةُ **ترخيصُ مدخل**، وسقفُ التجربة نفسِها
مُجمَّدٌ قبلُ في `vv_birth_preregistration` عند `CONDITIONAL_STRUCTURAL_BIRTH`
لا أكثر (`LICENSING_AN_INPUT_IS_NOT_A_BIRTH`).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from alghanem.canonical_content import canonical_bytes, canonical_digest

from .encoding.carrier_state_candidate import (
    CarrierState,
    CarrierStateCodec,
    CarrierStateUnit,
    GeminationRole,
)
from .fatiha_source_text import FATIHA_LINES, FATIHA_SOURCE_ID

__all__ = [
    "ALGEBRA_NAMED_RESIDUALS",
    "AN_ELEMENT_IS_AN_OCCURRENCE_NOT_AN_ALPHABET_CELL_NOTE",
    "BANNED_PROXY_FIELDS",
    "LICENSING_AN_INPUT_IS_NOT_A_BIRTH_NOTE",
    "THE_ADJACENCY_CONDITION_IS_TRUE_BY_CONSTRUCTION_NOTE",
    "THE_DEFERRED_MADD_AXIS_CAPS_THE_QUANTITY_PROJECTION_NOTE",
    "THE_JOIN_IS_NOT_APPLIED_HERE_NOTE",
    "ConsonantPosition",
    "JoinInputStatus",
    "LicensedJoinInput",
    "LicensedInputBundle",
    "OperationalAlgebraError",
    "VowelIdentity",
    "VowelPosition",
    "build_licensed_inputs",
    "decompose_word",
    "quantity_of",
]


class OperationalAlgebraError(ValueError):
    """رفضٌ صريح: عنصرٌ بلا برهانِ موضع، أو حالةٌ غيرُ معرَّفةٍ بلا علّةٍ مكتوبة."""


BANNED_PROXY_FIELDS: Final[tuple[str, ...]] = (
    "carrier_codepoint",
    "letter_index",
    "slot_position",
    "surface_offset",
)
"""حواملُ ممنوعةٌ بالاسم أن تكون هويّةً صوتيّة؛ مُعادةٌ هنا للفحص لا للتوسيع."""


class VowelIdentity(Enum):
    """`𝓘`: جودةُ الصائت وحدَها، مفردةٌ مغلقةٌ من ثلاث قيمٍ لا رابعَ لها."""

    FATHA = "fatha"
    DAMMA = "damma"
    KASRA = "kasra"


_VOWEL_STATES: Final[dict[CarrierState, VowelIdentity]] = {
    CarrierState.FATHA: VowelIdentity.FATHA,
    CarrierState.DAMMA: VowelIdentity.DAMMA,
    CarrierState.KASRA: VowelIdentity.KASRA,
}

_EXTENSION_CARRIER: Final[dict[VowelIdentity, str]] = {
    VowelIdentity.FATHA: "\u0627",
    VowelIdentity.DAMMA: "\u0648",
    VowelIdentity.KASRA: "\u064a",
}

_CONSONANT_STATES: Final[frozenset[CarrierState]] = frozenset(
    {CarrierState.SUKUN_EXPLICIT, CarrierState.SUKUN_IMPLICIT}
)


@dataclass(frozen=True)
class ConsonantPosition:
    """عنصرٌ في `X_C`: موضعُ صامتٍ ببرهان موضعه، لا خانةٌ في أبجديّة."""

    carrier: str
    word_index: int
    unit_index: int
    is_gemination_pair_start: bool
    admitted_because: str

    def __post_init__(self) -> None:
        if len(self.carrier) != 1:
            raise OperationalAlgebraError("حاملُ الموضع رمزٌ واحد")
        if self.word_index < 0 or self.unit_index < 0:
            raise OperationalAlgebraError("موضعُ العنصر عددٌ غيرُ سالب")
        if not self.admitted_because.strip():
            raise OperationalAlgebraError("عنصرٌ بلا علّةِ قبولٍ مكتوبة")


@dataclass(frozen=True)
class VowelPosition:
    """عنصرٌ في `X_V`: موضعُ صائتٍ بجودته وكمّيّته، كلتاهما مُشتقّةٌ لا مكتوبة."""

    carrier: str
    word_index: int
    unit_index: int
    identity: VowelIdentity
    quantity: int | None
    quantity_undefined_because: str | None

    def __post_init__(self) -> None:
        if len(self.carrier) != 1:
            raise OperationalAlgebraError("حاملُ الموضع رمزٌ واحد")
        if (self.quantity is None) != (self.quantity_undefined_because is not None):
            raise OperationalAlgebraError(
                "الكمّيّةُ إمّا مُشتقّةٌ وإمّا مُعلَّلةٌ بتعذّرها؛ ولا ثالثَ"
            )
        if self.quantity is not None and self.quantity not in (1, 2):
            raise OperationalAlgebraError(
                "كمّيّةٌ خارجَ {1, 2} لا تُقبَل عنصرًا؛ وتخرج غيرَ معرَّفة"
            )
        if self.quantity_undefined_because is not None:
            if not self.quantity_undefined_because.strip():
                raise OperationalAlgebraError("تعذّرٌ بلا علّةٍ مكتوبة")


def quantity_of(
    unit: CarrierStateUnit, following: CarrierStateUnit | None
) -> tuple[int | None, str | None]:
    """`π_Q`: عدُّ مواضع الصائت — واحدٌ للقصير، واثنان للممدود بموضع امتداد.

    ولا تُقرأ كمّيّةً زمنيّةً بالثواني: لا قطعةَ في هذه الشجرة صوتٌ مُسجَّل.
    وتُحسَب من موضعِ امتدادٍ تالٍ ساكنٍ موافقٍ للجودة، لا من نقطةِ ترميز الحامل
    ولا من موضعه في السطر.

    وإذا تلا الصائتَ حاملٌ في حالةِ ألفٍ خنجريّة، تعذّرت الكمّيّةُ ولم تُخمَّن:
    محورُ المدّ مؤجَّلٌ غيرُ مقروءٍ حالةً في الليف المقيس، فلا يُعلَم أموضعُ
    امتدادٍ هو أم لا. وتخرج `None` بعلّتها، لا واحدًا بالسكوت.
    """

    identity = _VOWEL_STATES.get(unit.state)
    if identity is None:
        raise OperationalAlgebraError("الكمّيّةُ لا تُشتَقّ إلّا عن موضعِ صائت")
    if following is None:
        return 1, None
    if following.state is CarrierState.DAGGER:
        return None, (
            "تلا الصائتَ حاملٌ في حالةِ ألفٍ خنجريّة، ومحورُ المدّ مؤجَّلٌ غيرُ "
            "مقروءٍ حالةً؛ فلا يُعلَم أموضعُ امتدادٍ هو أم لا، ولا تُخمَّن الكمّيّة"
        )
    extends = (
        following.carrier == _EXTENSION_CARRIER[identity]
        and following.state is CarrierState.SUKUN_IMPLICIT
        and following.gemination is None
    )
    return (2 if extends else 1), None


class JoinInputStatus(Enum):
    """حالُ الزوج أمام شروط التعريف المُجمَّدة؛ ولا حكمَ على `J` نفسِها."""

    ADMISSIBLE = "مقبولٌ_مدخلًا"
    UNDEFINED = "غيرُ_معرَّف"
    NOT_AN_ELEMENT = "ليس_عنصرًا"


@dataclass(frozen=True)
class LicensedJoinInput:
    """زوجٌ مصنَّفٌ معروضٌ على شروط التعريف، بحاله وعلّته وما صدق بالبناء."""

    word_index: int
    unit_index: int
    status: JoinInputStatus
    consonant: ConsonantPosition | None
    vowel: VowelPosition | None
    reason: str
    conditions_true_by_construction: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.reason.strip():
            raise OperationalAlgebraError("مدخلٌ بلا علّةٍ مكتوبة")
        if self.status is JoinInputStatus.ADMISSIBLE:
            if self.consonant is None or self.vowel is None:
                raise OperationalAlgebraError(
                    "مدخلٌ مقبولٌ بلا طرفَيه؛ ولا يُصطنَع له صامتٌ صفريّ"
                )
            if self.vowel.quantity is None:
                raise OperationalAlgebraError(
                    "مدخلٌ مقبولٌ بكمّيّةٍ غيرِ مُشتقّة؛ والقبولُ يلزمه اشتقاقُها"
                )
            if not self.conditions_true_by_construction:
                raise OperationalAlgebraError(
                    "مدخلٌ مقبولٌ لا يُسمّي ما صدق فيه بالبناء؛ والسكوتُ يُوهِم شاهدًا"
                )


def decompose_word(
    surface: str, word_index: int, *, codec: CarrierStateCodec | None = None
) -> tuple[LicensedJoinInput, ...]:
    """اقسِم كلَّ وحدةِ (حامل، حالة) إلى موضعَي صامتٍ وصائتٍ متزامنين.

    والقسمُ لا يرتّب: الموضعان يسكنان الوحدةَ نفسَها، ولا يُخترَع بينهما تتابع.
    """

    reader = CarrierStateCodec() if codec is None else codec
    units = reader.generate(surface)
    inputs: list[LicensedJoinInput] = []

    for index, unit in enumerate(units):
        following = units[index + 1] if index + 1 < len(units) else None
        identity = _VOWEL_STATES.get(unit.state)

        if identity is None:
            if unit.state in _CONSONANT_STATES:
                is_pair_start = unit.gemination is GeminationRole.PAIR_START
                consonant = ConsonantPosition(
                    carrier=unit.carrier,
                    word_index=word_index,
                    unit_index=index,
                    is_gemination_pair_start=is_pair_start,
                    admitted_because=(
                        "شقٌّ أوّلُ من شدّةٍ ساكن، وهو عنصرٌ في `X_C` بنصِّ " "المُجمَّد"
                        if is_pair_start
                        else "حاملٌ في حالةِ سكونٍ، وهو عنصرٌ في `X_C`"
                    ),
                )
                inputs.append(
                    LicensedJoinInput(
                        word_index=word_index,
                        unit_index=index,
                        status=JoinInputStatus.UNDEFINED,
                        consonant=consonant,
                        vowel=None,
                        reason=(
                            "عنصرُ `X_C` بلا صائتٍ معه؛ و`J` غيرُ معرَّفةٍ على "
                            "صامتٍ وحدَه، ولا يُصطنَع له صائتٌ صفريّ ولا يُقرَّب "
                            "الشكلُ إلى أقرب قالب"
                        ),
                        conditions_true_by_construction=(),
                    )
                )
                continue
            inputs.append(
                LicensedJoinInput(
                    word_index=word_index,
                    unit_index=index,
                    status=JoinInputStatus.NOT_AN_ELEMENT,
                    consonant=None,
                    vowel=None,
                    reason=(
                        f"حالةٌ بنيويّةٌ «{unit.state.value}» ليست عنصرًا في "
                        "`X_C` ولا في `X_V`؛ تخرج ولا تُقحَم صامتًا"
                    ),
                    conditions_true_by_construction=(),
                )
            )
            continue

        quantity, quantity_undefined_because = quantity_of(unit, following)
        consonant = ConsonantPosition(
            carrier=unit.carrier,
            word_index=word_index,
            unit_index=index,
            is_gemination_pair_start=unit.gemination is GeminationRole.PAIR_START,
            admitted_because=(
                "حاملُ الوحدة موضعُ صامتٍ، والحركةُ الساكنةُ معه موضعُ صائت؛ "
                "والقسمُ يفصل الموضعين ولا يرتّبهما"
            ),
        )
        vowel = VowelPosition(
            carrier=unit.carrier,
            word_index=word_index,
            unit_index=index,
            identity=identity,
            quantity=quantity,
            quantity_undefined_because=quantity_undefined_because,
        )
        if quantity is None:
            assert quantity_undefined_because is not None
            inputs.append(
                LicensedJoinInput(
                    word_index=word_index,
                    unit_index=index,
                    status=JoinInputStatus.UNDEFINED,
                    consonant=consonant,
                    vowel=vowel,
                    reason=quantity_undefined_because,
                    conditions_true_by_construction=(),
                )
            )
            continue
        inputs.append(
            LicensedJoinInput(
                word_index=word_index,
                unit_index=index,
                status=JoinInputStatus.ADMISSIBLE,
                consonant=consonant,
                vowel=vowel,
                reason=(
                    f"موضعُ صامتٍ وموضعُ صائتٍ «{identity.value}» بكمّيّة "
                    f"{quantity}، كلاهما مُشتقٌّ عن وحدةٍ واحدةٍ بموضعها"
                ),
                conditions_true_by_construction=(
                    "تجاورُ الصامت والصائت بلا فاصل: صادقٌ بالبناء لأنّ القاسمَ "
                    "هو الذي وضعهما في وحدةٍ واحدة، فلا يُعَدّ شاهدًا",
                ),
            )
        )

    return tuple(inputs)


@dataclass(frozen=True)
class LicensedInputBundle:
    """حزمةُ مداخلَ مرخَّصةٍ ببصمةِ محتوًى، ليُقيَّد بها اختبارُ CV المؤجَّل."""

    source_id: str
    inputs: tuple[LicensedJoinInput, ...]
    content_digest: str

    def __post_init__(self) -> None:
        if not self.inputs:
            raise OperationalAlgebraError("حزمةٌ بلا مدخلٍ واحد لا تُرخِّص شيئًا")
        if self.content_digest != _digest_of(self.inputs, self.source_id):
            raise OperationalAlgebraError(
                "بصمةُ الحزمة لا تُطابق محتواها؛ ولا يُقيَّد اختبارٌ ببصمةٍ مُعادة"
            )

    @property
    def admissible(self) -> tuple[LicensedJoinInput, ...]:
        """المداخلُ المقبولةُ وحدَها؛ مُشتقّةٌ لا مُخزَّنة."""

        return tuple(
            item for item in self.inputs if item.status is JoinInputStatus.ADMISSIBLE
        )

    @property
    def undefined(self) -> tuple[LicensedJoinInput, ...]:
        """ما خرج غيرَ معرَّفٍ بعلّته؛ محمولٌ في الحزمة لا مطروحٌ منها."""

        return tuple(
            item for item in self.inputs if item.status is JoinInputStatus.UNDEFINED
        )

    @property
    def quantity_undefined(self) -> tuple[LicensedJoinInput, ...]:
        """مواضعُ صائتٍ تعذّرت كمّيّتُها لمحورِ المدّ المؤجَّل؛ محمولةٌ بعلّتها."""

        return tuple(
            item
            for item in self.inputs
            if item.vowel is not None and item.vowel.quantity is None
        )

    @property
    def gemination_pair_starts(self) -> tuple[LicensedJoinInput, ...]:
        """أشقاءُ الشدّة الأُوَل؛ عناصرُ `X_C` لا يقع معها صائتٌ في وحدتها."""

        return tuple(
            item
            for item in self.inputs
            if item.consonant is not None and item.consonant.is_gemination_pair_start
        )

    @property
    def quantity_census(self) -> tuple[tuple[int, int], ...]:
        """توزيعُ الكمّيّة على المقبول؛ عدٌّ مُشتَقٌّ من المحتوى لا رقمٌ مكتوب."""

        counts: dict[int, int] = {}
        for item in self.admissible:
            assert item.vowel is not None
            quantity = item.vowel.quantity
            assert quantity is not None
            counts[quantity] = counts.get(quantity, 0) + 1
        return tuple(sorted(counts.items()))


def _encoded(
    inputs: tuple[LicensedJoinInput, ...], source_id: str
) -> dict[str, object]:
    return {
        "source_id": source_id,
        "inputs": [
            {
                "word_index": item.word_index,
                "unit_index": item.unit_index,
                "status": item.status.value,
                "carrier": item.vowel.carrier if item.vowel else None,
                "identity": item.vowel.identity.value if item.vowel else None,
                "quantity": item.vowel.quantity if item.vowel else None,
                "pair_start": (
                    item.consonant.is_gemination_pair_start if item.consonant else None
                ),
            }
            for item in inputs
        ],
    }


def _digest_of(inputs: tuple[LicensedJoinInput, ...], source_id: str) -> str:
    return canonical_digest(canonical_bytes(_encoded(inputs, source_id)))


def build_licensed_inputs(
    lines: tuple[str, ...] | None = None, *, source_id: str | None = None
) -> LicensedInputBundle:
    """أجرِ الجبرَ على نصٍّ مُودَع، وأخرِج حزمةَ مداخلَ مرخَّصةً مُبصَّمة."""

    text = FATIHA_LINES if lines is None else lines
    identifier = FATIHA_SOURCE_ID if source_id is None else source_id
    if not text:
        raise OperationalAlgebraError("نصٌّ بلا سطور؛ ولا يُجرى الجبرُ على خلاء")

    codec = CarrierStateCodec()
    collected: list[LicensedJoinInput] = []
    word_index = 0
    for line in text:
        for word in line.split():
            collected.extend(decompose_word(word, word_index, codec=codec))
            word_index += 1

    inputs = tuple(collected)
    return LicensedInputBundle(
        source_id=identifier,
        inputs=inputs,
        content_digest=_digest_of(inputs, identifier),
    )


# --- الحدودُ مُسمّاةً -------------------------------------------------------------


THE_JOIN_IS_NOT_APPLIED_HERE_NOTE: Final[str] = (
    "TheJoinIsNotAppliedHere: هذه الوحدةُ ترخّص مدخلًا لـ`J` ولا تُجري `J`؛ "
    "فلا مقطعَ يُولَد ههنا ولا `X_S` يُملأ، واختبارُ CV مؤجَّلٌ بسلطته"
)

THE_ADJACENCY_CONDITION_IS_TRUE_BY_CONSTRUCTION_NOTE: Final[str] = (
    "TheAdjacencyConditionIsTrueByConstructionNotByMeasurement: شرطُ «الصامتُ "
    "يسبق الصائتَ بلا فاصل» يصدق بالبناء لأنّ القاسمَ وضعهما في وحدةٍ واحدة؛ "
    "فلا يعدّه اختبارُ CV شاهدًا، والعبءُ على الشرطين الباقيين"
)

AN_ELEMENT_IS_AN_OCCURRENCE_NOT_AN_ALPHABET_CELL_NOTE: Final[str] = (
    "AnElementIsAnOccurrenceNotAnAlphabetCell: كلُّ عنصرٍ ههنا وقوعٌ بموضعه "
    "وعلّته، ولا تُكتَب مفردةُ تسعةٍ وعشرين حرفًا ولا أربعُ علامات؛ فما لم يقع "
    "لا يُخترَع له عنصر"
)

THE_DEFERRED_MADD_AXIS_CAPS_THE_QUANTITY_PROJECTION_NOTE: Final[str] = (
    "TheDeferredMaddAxisCapsTheQuantityProjection: `π_Q` تُشتَقّ من موضعِ "
    "امتدادٍ ساكنٍ موافقٍ للجودة، ومحورُ المدّ مؤجَّلٌ في الليف المقيس؛ فالكمّيّةُ "
    "عدُّ مواضعَ في الرسم لا مدّةٌ زمنيّةٌ منطوقة"
)

LICENSING_AN_INPUT_IS_NOT_A_BIRTH_NOTE: Final[str] = (
    "LicensingAnInputIsNotABirth: سقفُ هذه الوحدة ترخيصُ مدخل؛ ولا ولادةَ ولا "
    "حكمَ ولادةٍ كرنليًّا ولا تجميدَ `E0`، وسقفُ التجربة نفسِها مُجمَّدٌ قبلُ "
    "عند `CONDITIONAL_STRUCTURAL_BIRTH` لا أكثر"
)

ALGEBRA_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    THE_JOIN_IS_NOT_APPLIED_HERE_NOTE,
    THE_ADJACENCY_CONDITION_IS_TRUE_BY_CONSTRUCTION_NOTE,
    AN_ELEMENT_IS_AN_OCCURRENCE_NOT_AN_ALPHABET_CELL_NOTE,
    THE_DEFERRED_MADD_AXIS_CAPS_THE_QUANTITY_PROJECTION_NOTE,
    LICENSING_AN_INPUT_IS_NOT_A_BIRTH_NOTE,
)
