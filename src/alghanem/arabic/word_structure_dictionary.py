"""القاموسُ البنيويُّ للكلمة: نقطةُ دخولٍ واحدةٌ تُخرِج المقيسَ وتُسمّي المتعذّر.

هذه الوحدةُ تبني ما أجازه التسجيلُ القبْليّ في
`word_structure_dictionary_preregistration` ولا تتجاوزه بحرف. والطبقاتُ سبعٌ
متفاوتةُ المنزلة، فالمخرجُ ليس قاموسًا متجانسَ الشكل بل بنيةٌ **تفصل الأجناس
بالنوع لا بالتعليق**:

* **ثلاثُ طبقاتٍ مقيسةٌ على مرمازٍ قائم** تُخرَج قيمًا فعليّة، وكلُّها مقروءةٌ
  من `CarrierStateCodec` لا من مفردةٍ مُبتكَرة: الحرفُ وحالتُه (`letters`)،
  ودورُ الشدّة (`shadda_roles`)، ودورُ التنوين (`tanween_roles`).
* **أربعُ طبقاتٍ لم تُقَس** تُخرَج `WithheldLayer` بحقلِ تعذّرٍ مُسمًّى: المقطعُ
  والوزن، والمخرجُ والصفة، وأل، ومجرّد/مزيد.

`AGGREGATION_DOES_NOT_LEVEL_EPISTEMIC_RANK`: كلُّ مخرجٍ هنا يحمل منزلتَه من
`LayerEpistemicStanding`، والتجميعُ في بنيةٍ واحدةٍ لا يُسوّي بين المقيس
والمحجوز. والطبقاتُ المحجوزةُ **تُشتَقّ من التسجيل نفسِه** لا تُكتَب هنا، فلا
تُصبح طبقةٌ مقيسةً بحذفِ سطرٍ من هذه الوحدة.

`AN_UNMEASURED_LAYER_IS_A_SEPARATE_REFUSAL_FIELD_NOT_A_NULL`: ما لم يُقَس لا
يُخرَج `None`. فالأداةُ الواردةُ من المحادثة الأخرى كانت تكتب `wazn=None`
و`syllables=None` عند تعذّر الحلّ، فيستوي «لم يُقَس» و«قِيس فكان لا شيء»؛ وهنا
لا حقلَ أصلًا يقبل قيمةً خاليةً لطبقةٍ محجوزة، بل `WithheldLayer` باسمِ حقلِ
تعذّرها وشرطِ دخولها.

`A_ROLE_IS_NOT_A_STATE`: الشدّةُ والتنوينُ يُقرآن **دورين** على
`CarrierStateUnit` من حقولها القائمة (`gemination`، `tanwin`،
`tanwin_alif_seat`، `seat`)، ولا يُدخَلان عضوين في `CarrierState` المغلقة
بسبعة.

`THE_SHADDA_SOURCE_IS_NOT_READ_FROM_THE_MARKS`: الأداةُ الواردةُ كانت تنسب كلَّ
شدّةٍ إلى «إدغامٍ شمسيّ» أو «تضعيفٍ جذريّ» بالنظر إلى لامٍ قبلها. ولامُ «أل»
غيرُ مُميَّزةٍ من العلامات أصلًا (`HAMZAT_WASL_IS_NOT_DECIDABLE_FROM_THE_WRITTEN_MARKS`)،
ولامُ «الرَّحْمَنِ» تخرج من المرماز `SUKUN_IMPLICIT` كأيِّ حرفٍ بلا علامة. فدورُ
الشدّة يُخرَج مرصودًا، ومصدرُه يبقى في حقلِ تعذّرٍ لا يُنسَب إلى أحدهما.

`A_PASSTHROUGH_IS_NOT_A_LETTER_THAT_WAS_READ`: ما وقع خارج `DECLARED_CARRIERS`
يخرج من المرماز `PASSTHROUGH`، فيُسمّى في `unread` بأعيانه ولا يُعَدّ حرفًا
قُرِئت حالتُه.

`THIS_IS_A_READING_NOT_A_BIRTH`: لا ولادةَ هنا، ولا حكمَ ولادة، ولا تجميدَ
`E0`، ولا استيرادَ من `kernel/`. والمخرجُ قراءةٌ لمرمازٍ **مرشَّحٍ** لم يُلحَق
به وزنُ نموذجٍ أضعفَ مُجمَّد (`NO_WEAKER_MODEL_WAS_LICENSED_OR_FROZEN`)، فليس
`letters` عدَّ حروفٍ ذاتِ هويّةٍ ولا دعوى ذرّيّة.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from .encoding.carrier_state_candidate import (
    CarrierSeat,
    CarrierState,
    CarrierStateCodec,
    CarrierStateUnit,
    GeminationRole,
    round_trip_holds,
)
from .word_structure_dictionary_preregistration import (
    DICTIONARY_LAYER_REGISTRATIONS,
    DictionaryLayer,
    LayerEpistemicStanding,
    layer_registration,
)

__all__ = [
    "A_PASSTHROUGH_IS_NOT_A_LETTER_THAT_WAS_READ_NOTE",
    "MEASURED_LAYERS",
    "THE_SHADDA_SOURCE_IS_NOT_READ_FROM_THE_MARKS_NOTE",
    "THIS_IS_A_READING_NOT_A_BIRTH_NOTE",
    "WITHHELD_LAYERS",
    "LetterReading",
    "ShaddaRoleReading",
    "TanweenRoleReading",
    "UnreadSegment",
    "WithheldLayer",
    "WordStructureDictionary",
    "WordStructureDictionaryError",
    "analyze_word",
]


class WordStructureDictionaryError(ValueError):
    """رفضٌ عند القراءة: سطحٌ ليس نصًّا، أو سطحٌ خالٍ، أو طبقةٌ خارج التسجيل."""


@dataclass(frozen=True, slots=True, order=True)
class LetterReading:
    """حرفٌ واحدٌ كما قرأه المرمازُ القائم، بحقوله التي كُتبت وتُقرأ."""

    position: int
    carrier: str
    written_form: str
    state: CarrierState
    gemination: GeminationRole | None
    tanwin: bool
    tanwin_alif_seat: bool
    seat: CarrierSeat | None
    silent: bool
    waw_madda: bool

    @property
    def state_name(self) -> str:
        """اسمُ الحالة من المفردة القائمة، لا من تسميةِ جلسةٍ أخرى."""

        return self.state.name


@dataclass(frozen=True, slots=True, order=True)
class ShaddaRoleReading:
    """دورُ تضعيفٍ مرصودٌ على وحدةٍ قائمة، بلا نسبةٍ إلى مصدرٍ لم يُقرأ."""

    position: int
    carrier: str
    source_undecided: str


@dataclass(frozen=True, slots=True, order=True)
class TanweenRoleReading:
    """دورُ تنوينٍ مرصودٌ على وحدةٍ قائمة، ومَقعدُه إن كان على ألف."""

    position: int
    carrier: str
    state: CarrierState
    seated_on_alif: bool


@dataclass(frozen=True, slots=True, order=True)
class UnreadSegment:
    """رمزٌ خارج الحوامل المُعلَنة: مُمرَّرٌ لا حرفٌ قُرِئت حالتُه."""

    position: int
    codepoint: str


@dataclass(frozen=True, slots=True)
class WithheldLayer:
    """طبقةٌ لم تُقَس: منزلتُها، واسمُ حقلِ تعذّرها، وشرطُ دخولها — لا قيمة."""

    layer: DictionaryLayer
    standing: LayerEpistemicStanding
    refusal_field_name: str
    what_the_refusal_field_says: str
    entry_condition: str

    def __post_init__(self) -> None:
        if self.standing is LayerEpistemicStanding.MEASURED_BY_AN_EXISTING_CODEC:
            raise WordStructureDictionaryError(
                "طبقةٌ منزلتُها «مقيسٌ على مرمازٍ قائم» لا تُحجَب؛ والحجبُ مع "
                "القدرة على القياس امتناعٌ لا تعذّر"
            )


@dataclass(frozen=True, slots=True)
class WordStructureDictionary:
    """قاموسُ كلمةٍ واحدة: المقيسُ قيمًا، والمحجوبُ حقولَ تعذّرٍ مُسمّاة."""

    surface: str
    surface_round_trips: bool
    letters: tuple[LetterReading, ...]
    unread: tuple[UnreadSegment, ...]
    shadda_roles: tuple[ShaddaRoleReading, ...]
    tanween_roles: tuple[TanweenRoleReading, ...]
    withheld: tuple[WithheldLayer, ...]

    def __post_init__(self) -> None:
        withheld_layers = tuple(entry.layer for entry in self.withheld)
        if len(set(withheld_layers)) != len(withheld_layers):
            raise WordStructureDictionaryError("لا تُحجَب طبقةٌ مرّتين")
        if set(withheld_layers) != set(_WITHHELD_LAYER_NAMES):
            raise WordStructureDictionaryError(
                "الطبقاتُ المحجوبةُ تُشتَقّ من التسجيل القبْليّ بعينها؛ وحجبُ "
                "غيرِها أو إطلاقُ إحداها هنا تجاوزٌ للتسجيل لا قراءةٌ له"
            )

    @property
    def measured_layers(self) -> tuple[DictionaryLayer, ...]:
        """الطبقاتُ التي خرجت قيمًا فعليّة، مُشتقّةً من التسجيل لا مكتوبة."""

        return MEASURED_LAYERS

    def standing_of(self, layer: DictionaryLayer) -> LayerEpistemicStanding:
        """منزلةُ طبقةٍ بعينها؛ فالتجميعُ لا يُسقِط المنزلةَ عن المخرج."""

        return layer_registration(layer).standing

    def refusal_field_for(self, layer: DictionaryLayer) -> WithheldLayer:
        """حقلُ تعذّرِ طبقةٍ محجوبة؛ والمقيسةُ تُرَدّ ولا تُعطى حقلَ تعذّر."""

        for entry in self.withheld:
            if entry.layer is layer:
                return entry
        raise WordStructureDictionaryError(
            f"الطبقة {layer.value} ليست محجوبةً، فلا حقلَ تعذّرٍ لها"
        )


MEASURED_LAYERS: Final[tuple[DictionaryLayer, ...]] = tuple(
    registration.layer
    for registration in DICTIONARY_LAYER_REGISTRATIONS
    if registration.standing is LayerEpistemicStanding.MEASURED_BY_AN_EXISTING_CODEC
)

WITHHELD_LAYERS: Final[tuple[WithheldLayer, ...]] = tuple(
    WithheldLayer(
        layer=registration.layer,
        standing=registration.standing,
        refusal_field_name=registration.refusal_field_name,
        what_the_refusal_field_says=registration.what_the_refusal_field_says,
        entry_condition=registration.entry_condition,
    )
    for registration in DICTIONARY_LAYER_REGISTRATIONS
    if registration.standing is not LayerEpistemicStanding.MEASURED_BY_AN_EXISTING_CODEC
)

_WITHHELD_LAYER_NAMES: Final[frozenset[DictionaryLayer]] = frozenset(
    entry.layer for entry in WITHHELD_LAYERS
)

_SHADDA_SOURCE_UNDECIDED: Final[str] = (
    "مصدرُ التضعيف — إدغامٌ شمسيٌّ أم تضعيفٌ جذريّ — لا يُقرأ من العلامات: لامُ "
    "«أل» غيرُ مُميَّزةٍ فيها، وتخرج من المرماز `SUKUN_IMPLICIT` كأيِّ حرفٍ بلا "
    "علامة"
)

_CODEC: Final[CarrierStateCodec] = CarrierStateCodec()


def _letter_of(position: int, unit: CarrierStateUnit) -> LetterReading:
    return LetterReading(
        position=position,
        carrier=unit.carrier,
        written_form=unit.written_form,
        state=unit.state,
        gemination=unit.gemination,
        tanwin=unit.tanwin,
        tanwin_alif_seat=unit.tanwin_alif_seat,
        seat=unit.seat,
        silent=unit.silent,
        waw_madda=unit.waw_madda,
    )


def analyze_word(surface: str) -> WordStructureDictionary:
    """اقرأ كلمةً واحدةً: المقيسُ يخرج قيمًا، والمحجوبُ يخرج حقلَ تعذّرٍ مُسمًّى.

    القراءةُ كلُّها من `CarrierStateCodec`؛ وما رفضه المرمازُ يُرفَع رفضًا كما
    هو ولا يُصلَح هنا، فإصلاحُ رفضٍ في طبقةٍ فوقه يُخفي عطبَ ما تحته.
    """

    if not isinstance(surface, str):
        raise WordStructureDictionaryError("السطحُ نصّ")
    if not surface.strip():
        raise WordStructureDictionaryError(
            "سطحٌ خالٍ ليس كلمةً بلا بنية، بل لا كلمةَ أصلًا؛ فيُرَدّ ولا يُقرأ " "قاموسًا فارغًا"
        )

    units = _CODEC.generate(surface)

    letters: list[LetterReading] = []
    unread: list[UnreadSegment] = []
    shadda_roles: list[ShaddaRoleReading] = []
    tanween_roles: list[TanweenRoleReading] = []

    for position, unit in enumerate(units):
        if unit.state is CarrierState.PASSTHROUGH:
            unread.append(UnreadSegment(position=position, codepoint=unit.carrier))
            continue
        letters.append(_letter_of(position, unit))
        if unit.gemination is GeminationRole.PAIR_START:
            shadda_roles.append(
                ShaddaRoleReading(
                    position=position,
                    carrier=unit.carrier,
                    source_undecided=_SHADDA_SOURCE_UNDECIDED,
                )
            )
        if unit.tanwin:
            tanween_roles.append(
                TanweenRoleReading(
                    position=position,
                    carrier=unit.carrier,
                    state=unit.state,
                    seated_on_alif=unit.tanwin_alif_seat,
                )
            )

    return WordStructureDictionary(
        surface=surface,
        surface_round_trips=round_trip_holds(surface),
        letters=tuple(letters),
        unread=tuple(unread),
        shadda_roles=tuple(shadda_roles),
        tanween_roles=tuple(tanween_roles),
        withheld=WITHHELD_LAYERS,
    )


A_PASSTHROUGH_IS_NOT_A_LETTER_THAT_WAS_READ_NOTE: Final[str] = (
    "APassthroughIsNotALetterThatWasRead: ما خرج من المرماز `PASSTHROUGH` وقع "
    "خارج الحوامل المُعلَنة، فيُسمّى في `unread` بعينه ولا يُعَدّ حرفًا قُرِئت "
    "حالتُه"
)

THE_SHADDA_SOURCE_IS_NOT_READ_FROM_THE_MARKS_NOTE: Final[str] = (
    "TheShaddaSourceIsNotReadFromTheMarks: دورُ التضعيف مرصودٌ، ونسبتُه إلى "
    "إدغامٍ شمسيٍّ أو تضعيفٍ جذريٍّ متوقّفةٌ على تمييزِ لامِ «أل» وهو متعذّرٌ من "
    "العلامات؛ فيبقى المصدرُ في حقلِ تعذّرٍ لا يُنسَب"
)

THIS_IS_A_READING_NOT_A_BIRTH_NOTE: Final[str] = (
    "ThisIsAReadingNotABirth: القاموسُ قراءةٌ لمرمازٍ مرشَّحٍ لم يُلحَق به نموذجٌ "
    "أضعفُ مُجمَّد؛ فليس `letters` عدَّ حروفٍ ذاتِ هويّةٍ ولا دعوى ذرّيّة"
)


if len(MEASURED_LAYERS) + len(WITHHELD_LAYERS) != len(DictionaryLayer):
    raise RuntimeError("كلُّ طبقةٍ إمّا مقيسةٌ تُخرِج قيمةً وإمّا محجوبةٌ تُخرِج تعذّرًا.")
if set(MEASURED_LAYERS) & _WITHHELD_LAYER_NAMES:
    raise RuntimeError("لا تكون الطبقةُ مقيسةً ومحجوبةً معًا.")
if len(MEASURED_LAYERS) != 3 or len(WITHHELD_LAYERS) != 4:
    raise RuntimeError("المقيسُ ثلاثُ طبقاتٍ والمحجوبُ أربع، كما جُمِّد في التسجيل.")
