"""السيلبنة: تقطيعٌ حتميٌّ فوق قراءة P-EXTRACTOR، ووزنٌ إسقاطٌ يُشتَقّ عند السؤال.

القواعدُ والقوالبُ مُجمَّدةٌ قبلَ هذه الوحدة في `syllable_preregistration`،
وتُطابَق بصمتُها عند الاستيراد؛ فتغيّرُ بندٍ هناك يُسقط قراءةَ هذه الوحدة ولا
يمرّ بصمت.

`AN_UNSEGMENTABLE_WORD_IS_A_NAMED_REFUSAL_NOT_A_NULL`: الكلمةُ التي لا تقع
مقاطعُها في القوالب الستّة تخرج بـ`syllables=()` وبسببٍ مُسمًّى في
`wazn_unresolved`؛ ولا `wazn=None` ولا مقطعٌ مُقرَّبٌ إلى أقرب قالب.

`WAZN_IS_A_DERIVED_PROJECTION_NOT_A_BORN_OBJECT`: `SyllabifiedWord.wazn`
خاصّيّةٌ تُحسَب من سلسلة المقاطع عند النداء، ولا تُخزَّن حقلًا؛ ومن سأل وزنَ
كلمةٍ متعذّرةٍ رُفِع له استثناءٌ ولم تُخترَع له قيمة.

`THE_LAYER_STAYS_WITHHELD_UNTIL_THE_FLOOR_IS_MEASURED`: وجودُ هذه الوحدة لا
يرفع حجبَ `DictionaryLayer.SYLLABLES_AND_WAZN` في `word_structure_dictionary`.
الشروطُ البنيويّةُ الأربعةُ في `syllable_preregistration
.STRUCTURAL_ACCEPTANCE_CONDITIONS` تُفحَص على المدوّنة المُبصَّمة بالسكربت
المرافق، وحتّى يُسجَّل ذلك الفحصُ تبقى الطبقةُ محجوبةً بمنزلتها.

`THE_FREE_MADDA_MARK_IS_NOT_READ_AS_LENGTH`: علامةُ المدّ الحرّة (`waw_madda`
في الوحدة) تُنقَل ولا تُقرأ طولًا في التقطيع. وهذا نقصُ قراءةٍ مُصرَّحٌ به لا
قراءةٌ بالسالب: من عدَّها طولًا أدخل في العدّ ما لم يُقَس.

`THIS_IS_A_READING_NOT_A_BIRTH`: لا ولادةَ هنا، ولا حكم، ولا تجميدَ `E0`، ولا
استيرادَ من `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from .encoding.carrier_state_candidate import CarrierSeat, CarrierState
from .p_extractor import LetterReading, PExtractorReading, PhoneticRole, read_surface
from .syllable_preregistration import (
    PREREGISTRATION_DIGEST,
    WAQF_TRANSFORM_RULES,
    SyllableTemplate,
    WaqfRule,
    template_of,
)

__all__ = [
    "AN_UNSEGMENTABLE_WORD_IS_A_NAMED_REFUSAL_NOT_A_NULL_NOTE",
    "SYLLABIFIER_NAMED_RESIDUALS",
    "THE_ALEF_MAQSURA_TANWEEN_SEAT_IS_NOT_READ_NOTE",
    "THE_FREE_MADDA_MARK_IS_NOT_READ_AS_LENGTH_NOTE",
    "THE_LAYER_STAYS_WITHHELD_UNTIL_THE_FLOOR_IS_MEASURED_NOTE",
    "THE_WAQF_TRANSFORM_READS_NO_CORPUS_NOTE",
    "WAZN_IS_A_DERIVED_PROJECTION_NOT_A_BORN_OBJECT_NOTE",
    "Slot",
    "SlotKind",
    "StatedWaqfTransform",
    "Syllable",
    "SyllabifiedWord",
    "SyllabifierError",
    "UnresolvedWazn",
    "apply_stated_waqf",
    "expand_slots",
    "syllabify_reading",
    "syllabify_surface",
]


class SyllabifierError(ValueError):
    """رفضٌ عند القراءة: وزنٌ سُئل عنه وهو متعذّر، أو قراءةٌ ببصمةٍ أخرى."""


class SlotKind(Enum):
    """جنسُ الشريحة بعد التوسيع. صامتٌ أو صائت، ولا ثالثَ بينهما."""

    CONSONANT = "صامت"
    VOWEL = "صائت"


@dataclass(frozen=True, slots=True)
class Slot:
    """شريحةٌ واحدةٌ بعد التوسيع، ومعها موضعُ الوحدة التي أخرجتها."""

    kind: SlotKind
    letter_index: int
    length: int = 1
    is_tanween_nun: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.kind, SlotKind):
            raise SyllabifierError("جنسُ الشريحة عضوٌ في مفردته المغلقة")
        if isinstance(self.letter_index, bool) or not isinstance(
            self.letter_index, int
        ):
            raise SyllabifierError("موضعُ الوحدة عددٌ صحيح")
        if self.letter_index < 0:
            raise SyllabifierError("موضعُ الوحدة عددٌ غيرُ سالب")
        if self.kind is SlotKind.CONSONANT and self.length != 1:
            raise SyllabifierError("الصامتُ شريحةٌ واحدةٌ لا تُطوَّل")
        if self.kind is SlotKind.VOWEL and self.length not in (1, 2):
            raise SyllabifierError("الصائتُ قصيرٌ أو طويلٌ، ولا ثالثَ له")
        if self.is_tanween_nun and self.kind is not SlotKind.CONSONANT:
            raise SyllabifierError("نونُ التنوين صامتٌ مُغلِق")


@dataclass(frozen=True, slots=True)
class Syllable:
    """مقطعٌ واحدٌ بقالبه وشرائحه؛ والقالبُ مُشتَقٌّ من الشكل لا مكتوبٌ معه."""

    template: SyllableTemplate
    slots: tuple[Slot, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.template, SyllableTemplate):
            raise SyllabifierError("القالبُ عضوٌ في القوالب الستّة المغلقة")
        if not self.slots:
            raise SyllabifierError("مقطعٌ بلا شرائح ليس مقطعًا")
        vowels = [slot for slot in self.slots if slot.kind is SlotKind.VOWEL]
        if len(vowels) != 1:
            raise SyllabifierError("للمقطع نواةٌ واحدةٌ لا أكثر ولا أقلّ")
        consonants = len(self.slots) - 1
        derived = template_of(1, vowels[0].length, consonants - 1)
        if derived is not self.template:
            raise SyllabifierError("القالبُ المكتوبُ يخالف شكلَ الشرائح")


@dataclass(frozen=True, slots=True)
class UnresolvedWazn:
    """تعذّرُ تقطيعٍ مُسمًّى: أينَ وقف، ولِمَ وقف. حقلٌ مستقلٌّ لا قيمةٌ خالية."""

    surface: str
    letter_index: int | None
    reason: str

    def __post_init__(self) -> None:
        if not isinstance(self.surface, str):
            raise SyllabifierError("الصورةُ نصّ")
        if self.letter_index is not None:
            if isinstance(self.letter_index, bool) or not isinstance(
                self.letter_index, int
            ):
                raise SyllabifierError("موضعُ التعذّر عددٌ صحيحٌ أو لا موضعَ له")
            if self.letter_index < 0:
                raise SyllabifierError("موضعُ التعذّر عددٌ غيرُ سالب")
        if not isinstance(self.reason, str) or not self.reason.strip():
            raise SyllabifierError("سببُ التعذّر نصٌّ غير فارغ")


@dataclass(frozen=True, slots=True)
class SyllabifiedWord:
    """كلمةٌ مُقطَّعةٌ أو متعذّرة؛ ولا تجتمع المقاطعُ والتعذّرُ في مُخرَجٍ واحد."""

    surface: str
    syllables: tuple[Syllable, ...]
    wazn_unresolved: tuple[UnresolvedWazn, ...] = ()
    preregistration_digest: str = PREREGISTRATION_DIGEST

    def __post_init__(self) -> None:
        if self.syllables and self.wazn_unresolved:
            raise SyllabifierError(
                "كلمةٌ مُقطَّعةٌ ومتعذّرةٌ معًا تُقرأ مُقطَّعةً بجزءٍ وتُخفي "
                "الباقي؛ والتعذّرُ يردّ الكلمةَ كلَّها"
            )
        if self.preregistration_digest != PREREGISTRATION_DIGEST:
            raise SyllabifierError(
                "قراءةٌ ببصمةِ تجميدٍ غيرِ القائمة قراءةٌ بقوالبَ أو بقواعدَ أخرى"
            )

    @property
    def is_resolved(self) -> bool:
        """أقُطِّعت الكلمةُ كلُّها؟ مُشتَقٌّ لا مُخزَّن."""

        return not self.wazn_unresolved

    @property
    def wazn(self) -> str:
        """الوزنُ إسقاطًا مشتقًّا من سلسلة المقاطع، لا كائنًا مولودًا."""

        if not self.is_resolved:
            raise SyllabifierError(
                "لا وزنَ لكلمةٍ متعذّرة؛ وسببُ تعذّرها في `wazn_unresolved` "
                "ولا تُخترَع له قيمة"
            )
        return "-".join(syllable.template.value for syllable in self.syllables)


_ALEF: Final[str] = "\u0627"
_TAA: Final[str] = "\u062a"
_HAA: Final[str] = "\u0647"
_SHORT_VOWELS: Final[frozenset[CarrierState]] = frozenset(
    {CarrierState.FATHA, CarrierState.DAMMA, CarrierState.KASRA}
)
_SILENT_ROLES: Final[frozenset[PhoneticRole]] = frozenset(
    {PhoneticRole.ASSIMILATED_SILENT, PhoneticRole.SILENT_DIFFERENTIATING_ALIF}
)


def _is_lengthener(letter: LetterReading) -> bool:
    """أهذه وحدةُ مدٍّ تُطيل صائتًا قبلها بدل أن تُخرِج شريحةً لنفسها؟"""

    if letter.unit.state is CarrierState.DAGGER:
        return True
    return (
        letter.has_role(PhoneticRole.MADD_EXTENSION)
        and letter.unit.seat is not CarrierSeat.MADD
    )


def _is_dropped_tanween_seat(letter: LetterReading) -> bool:
    """أهذه ألفُ مَقعدٍ للتنوين لا صامتَ لها ولا صائت؟"""

    return (
        letter.has_role(PhoneticRole.TANWEEN_ALIF_CARRIER)
        and letter.unit.carrier == _ALEF
        and letter.unit.state is CarrierState.SUKUN_IMPLICIT
    )


def expand_slots(reading: PExtractorReading) -> tuple[tuple[Slot, ...], str | None]:
    """وسِّع القراءةَ إلى شرائحَ، أو أعِد سببَ تعذّرٍ مُسمًّى.

    والشدّةُ موسَّعةٌ أصلًا في المرماز: شقُّها الأوّلُ وحدةٌ مستقلّةٌ ساكنة،
    فتخرج صامتًا مُغلِقًا، والثاني يخرج صامتًا متحرّكًا.
    """

    slots: list[Slot] = []
    for letter in reading.letters:
        unit = letter.unit
        if unit.state is CarrierState.PASSTHROUGH:
            return (), "حرفٌ مُمرَّرٌ لا حاملَ له ولا حالة"
        if unit.silent:
            continue
        if any(role in _SILENT_ROLES for role in letter.roles):
            continue
        if _is_dropped_tanween_seat(letter):
            continue
        if _is_lengthener(letter):
            if not slots or slots[-1].kind is not SlotKind.VOWEL:
                return (), "مدٌّ بلا صائتٍ قبله يمتدّ به"
            previous = slots[-1]
            if previous.length != 1:
                return (), "مدٌّ على صائتٍ طويلٍ أصلًا"
            slots[-1] = Slot(
                kind=SlotKind.VOWEL,
                letter_index=previous.letter_index,
                length=2,
            )
            continue
        slots.append(Slot(kind=SlotKind.CONSONANT, letter_index=letter.index))
        if unit.seat is CarrierSeat.MADD:
            slots.append(Slot(kind=SlotKind.VOWEL, letter_index=letter.index, length=2))
            continue
        if unit.state in _SHORT_VOWELS:
            slots.append(Slot(kind=SlotKind.VOWEL, letter_index=letter.index))
            if unit.tanwin:
                slots.append(
                    Slot(
                        kind=SlotKind.CONSONANT,
                        letter_index=letter.index,
                        is_tanween_nun=True,
                    )
                )
    if not slots:
        return (), "لا شريحةَ واحدةً بعد التوسيع"
    return tuple(slots), None


def _segment(
    slots: tuple[Slot, ...],
) -> tuple[tuple[Syllable, ...], int | None, str | None]:
    """قطِّع الشرائحَ حتميًّا، أو قِف عند أوّل موضعٍ لا يقع في القوالب الستّة."""

    syllables: list[Syllable] = []
    index = 0
    total = len(slots)
    while index < total:
        onset = slots[index]
        if onset.kind is not SlotKind.CONSONANT:
            return (), onset.letter_index, "صائتٌ يفتتح مقطعًا بلا صامتٍ قبله"
        if index + 1 >= total or slots[index + 1].kind is not SlotKind.VOWEL:
            return (), onset.letter_index, "صامتٌ ساكنٌ لا يقع إغلاقًا لمقطعٍ قبله"
        nucleus = slots[index + 1]
        index += 2
        coda: list[Slot] = []
        while len(coda) < 2 and index < total:
            candidate = slots[index]
            if candidate.kind is not SlotKind.CONSONANT:
                break
            if index + 1 < total and slots[index + 1].kind is SlotKind.VOWEL:
                break
            if coda and index + 1 != total:
                break
            coda.append(candidate)
            index += 1
        try:
            template = template_of(1, nucleus.length, len(coda))
        except ValueError:
            return (), onset.letter_index, "شكلٌ خارجَ القوالب الستّة"
        syllables.append(Syllable(template=template, slots=(onset, nucleus, *coda)))
    return tuple(syllables), None, None


def _name_the_standing_refusal(
    reading: PExtractorReading, letter_index: int | None, reason: str
) -> str:
    """إن وقف التقطيعُ عند موضعٍ مُسجَّلٍ متعذّرًا، سُمِّي تعذّرُه القائمُ معه."""

    if letter_index is None:
        return reason
    for site in reading.undecided:
        if site.index == letter_index:
            return f"{reason} — وموضعُه مُسجَّلٌ متعذّرًا: {site.why_it_is_undecided}"
    return reason


def syllabify_reading(reading: PExtractorReading) -> SyllabifiedWord:
    """قطِّع قراءةً واحدة؛ والمتعذّرُ يخرج باسم سببه لا قيمةً خالية."""

    slots, failure = expand_slots(reading)
    if failure is not None:
        return SyllabifiedWord(
            surface=reading.surface,
            syllables=(),
            wazn_unresolved=(
                UnresolvedWazn(
                    surface=reading.surface, letter_index=None, reason=failure
                ),
            ),
        )
    syllables, letter_index, reason = _segment(slots)
    if reason is not None:
        return SyllabifiedWord(
            surface=reading.surface,
            syllables=(),
            wazn_unresolved=(
                UnresolvedWazn(
                    surface=reading.surface,
                    letter_index=letter_index,
                    reason=_name_the_standing_refusal(reading, letter_index, reason),
                ),
            ),
        )
    return SyllabifiedWord(surface=reading.surface, syllables=syllables)


def syllabify_surface(surface: str) -> SyllabifiedWord:
    """اقرأ صورةً ثمّ قطِّعها، بالطريق الواحد: المرمازُ فالأدوارُ فالمقاطع."""

    return syllabify_reading(read_surface(surface))


@dataclass(frozen=True, slots=True)
class StatedWaqfTransform:
    """تحويلُ وقفٍ على مُدخَلٍ **مُصرَّحٍ** بوقفه، لا قراءةٌ لوقفٍ في مدوّنة."""

    surface: str
    applied_rule: WaqfRule | None
    letter_index: int | None
    declared_limit: str

    def __post_init__(self) -> None:
        if self.applied_rule is not None and not isinstance(
            self.applied_rule, WaqfRule
        ):
            raise SyllabifierError("القاعدةُ المُطبَّقةُ من الجدول المُجمَّد")
        if not isinstance(self.declared_limit, str) or not self.declared_limit.strip():
            raise SyllabifierError("الحدُّ المُعلَن نصٌّ غير فارغ")


_WAQF_LIMIT: Final[str] = (
    "المُدخَلُ مُصرَّحٌ بوقفه من خارج الشجرة؛ فالسكونُ الوقفيُّ غيرُ مُميَّزٍ "
    "من الوصليّ هنا، وهذا التحويلُ عمليّةٌ على مقولٍ لا قراءةٌ لمقروء"
)


def _waqf_rule_named(name: str) -> WaqfRule:
    for rule in WAQF_TRANSFORM_RULES:
        if rule.name == name:
            return rule
    raise SyllabifierError(f"لا قاعدةَ وقفٍ باسم {name!r}")


def apply_stated_waqf(reading: PExtractorReading) -> StatedWaqfTransform:
    """أيُّ قاعدةِ وقفٍ تنطبق على آخِر هذه الصورة، لو صُرِّح بأنّها موقوفٌ عليها.

    ولا تُعيد هذه الدالّةُ صورةً محوَّلةً ولا وحداتٍ مُعادةَ البناء: تُسمّي
    القاعدةَ وموضعَها، وتُصرِّح بحدِّها؛ فالتحويلُ نفسُه إعرابٌ للمقول لا
    اكتشافٌ في المقروء.
    """

    for letter in reversed(reading.letters):
        unit = letter.unit
        if (
            unit.seat is CarrierSeat.TA_MARBUTA
            and letter.index == len(reading.letters) - 1
        ):
            return StatedWaqfTransform(
                surface=reading.surface,
                applied_rule=_waqf_rule_named("TAA_MARBUTA"),
                letter_index=letter.index,
                declared_limit=_WAQF_LIMIT,
            )
        if unit.state not in _SHORT_VOWELS or not letter.is_haraka_bearing:
            continue
        if unit.tanwin:
            name = (
                "TANWEEN_FATH"
                if unit.state is CarrierState.FATHA
                else "TANWEEN_DAMM_OR_KASR"
            )
        else:
            name = "BARE_HARAKA"
        return StatedWaqfTransform(
            surface=reading.surface,
            applied_rule=_waqf_rule_named(name),
            letter_index=letter.index,
            declared_limit=_WAQF_LIMIT,
        )
    return StatedWaqfTransform(
        surface=reading.surface,
        applied_rule=None,
        letter_index=None,
        declared_limit=_WAQF_LIMIT,
    )


AN_UNSEGMENTABLE_WORD_IS_A_NAMED_REFUSAL_NOT_A_NULL_NOTE: Final[str] = (
    "AnUnsegmentableWordIsANamedRefusalNotANull: المتعذّرُ يخرج باسم سببه في "
    "`wazn_unresolved`، ولا يجتمع مع مقاطعَ جزئيّةٍ في مُخرَجٍ واحد"
)

THE_ALEF_MAQSURA_TANWEEN_SEAT_IS_NOT_READ_NOTE: Final[str] = (
    "TheAlefMaqsuraTanweenSeatIsNotRead: المواصفةُ تقصر مَقعدَ تنوين الفتح "
    "على الألف وحدَها، فالألفُ المقصورةُ في نحو «مُصَلًّى» تخرج من التقطيع "
    "صامتًا مُغلِقًا لا مَقعدًا مُهمَلًا؛ وهذا أثرُ حدٍّ في المواصفة المُودَعة "
    "يُسجَّل ولا يُلتَفّ عليه بقاعدةٍ غيرِ مُسجَّلة"
)

THE_FREE_MADDA_MARK_IS_NOT_READ_AS_LENGTH_NOTE: Final[str] = (
    "TheFreeMaddaMarkIsNotReadAsLength: علامةُ المدّ الحرّةُ تُنقَل ولا تُقرأ "
    "طولًا؛ نقصُ قراءةٍ مُصرَّحٌ به لا قراءةٌ بالسالب"
)

THE_LAYER_STAYS_WITHHELD_UNTIL_THE_FLOOR_IS_MEASURED_NOTE: Final[str] = (
    "TheLayerStaysWithheldUntilTheFloorIsMeasured: وجودُ أداةٍ ليس بلوغَ "
    "أرضيّة؛ وطبقةُ المقطع والوزن تبقى محجوبةً حتّى تُفحَص الشروطُ الأربعةُ "
    "على المدوّنة المُبصَّمة"
)

THE_WAQF_TRANSFORM_READS_NO_CORPUS_NOTE: Final[str] = (
    "TheWaqfTransformReadsNoCorpus: قواعدُ الوقف تُطبَّق على مُدخَلٍ مُصرَّحٍ "
    "بوقفه؛ ولا يُستدَلّ بها على أنّ موضعًا في مدوّنةٍ موقوفٌ عليه"
)

WAZN_IS_A_DERIVED_PROJECTION_NOT_A_BORN_OBJECT_NOTE: Final[str] = (
    "WaznIsADerivedProjectionNotABornObject: `wazn` خاصّيّةٌ تُحسَب عند "
    "السؤال؛ ولا حقلَ لها يُخزَّن فيُحتَجّ به على ما أُسقِط عنه"
)

SYLLABIFIER_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    AN_UNSEGMENTABLE_WORD_IS_A_NAMED_REFUSAL_NOT_A_NULL_NOTE,
    THE_ALEF_MAQSURA_TANWEEN_SEAT_IS_NOT_READ_NOTE,
    THE_FREE_MADDA_MARK_IS_NOT_READ_AS_LENGTH_NOTE,
    THE_LAYER_STAYS_WITHHELD_UNTIL_THE_FLOOR_IS_MEASURED_NOTE,
    THE_WAQF_TRANSFORM_READS_NO_CORPUS_NOTE,
    WAZN_IS_A_DERIVED_PROJECTION_NOT_A_BORN_OBJECT_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة، مرتّبةً كما تُرتَّب في بقيّة الطبقة."""
