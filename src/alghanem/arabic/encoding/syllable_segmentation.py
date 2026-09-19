"""تقطيعٌ مقطعيٌّ عكوسٌ فوق وحدات الحامل/الحالة: تجزئةٌ لا تفسير.

هذه الوحدةُ تأخذ مخرجَ `CarrierStateCodec.generate` بعينه — لا نصًّا ولا
مفردةً جديدة — وتقسمه إلى مقاطعَ متجاورةٍ تستوعب كلَّ وحدةٍ مرّةً واحدة، ثمّ
تردّها كما أخذتها. فالطبقةُ تدخل الشجرةَ لأنّها **تأخذ مخرجَ ما تحتها وتسمح
بإعادة بنائه**، لا لأنّها مطلوبةٌ نظريًّا.

`SEGMENTATION_IS_NOT_A_WAZN`: لا وزنَ يخرج من هنا، ولا `CV`/`CVC` يُقرأ صرفًا،
ولا اسمَ مقطعٍ يُنسَب إلى عروضٍ أو إلى تصنيفٍ مستورَد. والمقطعُ هنا **مدًى على
الوحدات** بموضعِ بدايته وعدده، فطبقةُ «المقطع والوزن» في
`word_structure_dictionary_preregistration` تبقى محجوبةً بحالها: شرطُ دخولها
وحدةُ سيلبنةٍ **وأرضيّةُ قبولٍ مكتوبةٌ قبل قياسها**، وهذه الوحدةُ تُوفّي الشقَّ
الأوّلَ ولا تدّعي الثاني.

`A_REFUSAL_IS_NOT_A_SEGMENTATION`: ما لا تنطبق عليه قاعدةُ البدء — ساكنٌ في
أوّل الكلمة، أو ساكنان متجاوران، أو رمزٌ مُمرَّرٌ خارج الحوامل — يُرفَع رفضًا
باسمه ولا يُلصَق بمقطعٍ قبله ليخرج الجدولُ نظيفًا.

`THE_INVERSE_IS_RUN_NOT_ASSERTED`: `desegment` تُنفَّذ فعلًا ويُقارَن ناتجُها
بالوحدات الداخلة؛ ولا تُكتب هنا نسبةُ استرجاعٍ واحدة.

`THE_ALEF_IS_A_NEUTRAL_ELEMENT`: الألفُ العاري في أوّل الكلمة — ألفُ الوصل —
حركتُه متعذّرةٌ من العلامات المكتوبة، وهذا التعذّرُ باقٍ. فلا يُخمَّن له فتحٌ
ولا ضمٌّ ولا كسر، وإنّما يُعامَل **عنصرًا محايدًا**: صدرٌ يفتح مقطعًا ولا يدّعي
نواةً. ومقطعُه يُقرأ `onset=NEUTRAL_ALEF` و`claims_a_nucleus=False`، فمن عدَّه
مقطعًا موصوفًا فقد قرأ ما لم يُكتَب. والحيادُ **لا يُصلح** شيئًا تحته: الوحدةُ
تُحفَظ بعينها ويردّها `desegment` كما دخلت، والساكنُ الثاني بعد صدرٍ محايدٍ
يبقى رفضًا باسمه.

ومدى الحياد مُعلَن: **أوّلُ الكلمة وحدَه**. فالألفُ العاري في وسطها أو آخرها
يبقى على قراءته الحالية ساكنًا يُغلِق مقطعًا، لأنّ تلك القراءةَ تُشغَّل وترجع
بالبايتات، فلا موجبَ لتغييرها.

`THE_OPENING_BEFORE_THE_FIRST_VOWEL_IS_NOT_WRITTEN`: قوانينُ الابتداء والوصل
والوقف — المُسجَّلةُ في `ibtida_wasl_waqf_registration` بلا قراءة — تتّفق على
أنّ ما يجري في **مفتتح الكلمة قبل أوّل حركةٍ مكتوبة** لا تُقرّره العلاماتُ
وحدَها: الابتداءُ يُحرِّك همزةَ الوصل بحركةٍ غيرِ مكتوبة، والوصلُ يُسقطها
ويستمدّ الحركةَ من آخر ما قبلها، والوقفُ لا يمسّ المفتتحَ أصلًا. فالوحدةُ
تُعمِّم الحيادَ على هذا المفتتح كلِّه لا على الألف وحدَه: **مدًى متّصلٌ من
وحداتٍ لم تُكتَب عليها علامةٌ ألبتّة** — لا حركةً ولا سكونًا ولا شدّة — يفتتحه
الألفُ العاري، ويُغلَق بساكنٍ واحدٍ على الأكثر.

وهذا **توسيعُ امتناعٍ لا استيرادُ قراءة**: لا يُقال إنّ اللام لامُ تعريفٍ، ولا
إنّها مُدغَمة، ولا يُخمَّن لها لفظ؛ إنّما يُقال إنّ حالتَها غيرُ مكتوبة فلا
تُحاسَب حسابَ الساكن المكتوب. والوحداتُ تُحفَظ بأعيانها ويردّها `desegment` كما
دخلت. وما بعد أوّلِ حركةٍ مكتوبةٍ خارجٌ عن هذا المدى بتمامه، فالتقاءُ ساكنَين
في وسط الكلمة — كالمدّ قبل مُشدَّدٍ — يبقى رفضًا باسمه.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Final

from .carrier_state_candidate import CarrierState, CarrierStateUnit

__all__ = [
    "A_REFUSAL_IS_NOT_A_SEGMENTATION_NOTE",
    "NEUTRAL_ALEF_CARRIER",
    "NEUTRAL_ONSET_STATES",
    "NUCLEUS_STATES",
    "SEGMENTATION_IS_NOT_A_WAZN_NOTE",
    "THE_ALEF_IS_A_NEUTRAL_ELEMENT_NOTE",
    "THE_INVERSE_IS_RUN_NOT_ASSERTED_NOTE",
    "THE_OPENING_BEFORE_THE_FIRST_VOWEL_IS_NOT_WRITTEN_NOTE",
    "Syllable",
    "SyllableOnset",
    "SyllableParse",
    "SyllableRefusal",
    "SyllableSegmentationError",
    "desegment",
    "segment",
]


class SyllableSegmentationError(ValueError):
    """رفضٌ بنيويٌّ عند التقطيع، مُسمًّى برمزه لا محمولٌ على أقرب حالة."""

    def __init__(self, refusal: SyllableRefusal, message: str) -> None:
        super().__init__(message)
        self.refusal = refusal


class SyllableRefusal(Enum):
    """أسبابُ امتناع التقطيع؛ مفردةٌ مغلقةٌ لا نصٌّ حُرّ."""

    NO_UNIT_AT_ALL = "NO_UNIT_AT_ALL"
    ONSETLESS_INITIAL_SAKIN = "ONSETLESS_INITIAL_SAKIN"
    TWO_ADJACENT_SAKINS = "TWO_ADJACENT_SAKINS"
    PASSTHROUGH_IS_NOT_SYLLABIFIED = "PASSTHROUGH_IS_NOT_SYLLABIFIED"


NUCLEUS_STATES: Final[frozenset[CarrierState]] = frozenset(
    {
        CarrierState.FATHA,
        CarrierState.DAMMA,
        CarrierState.KASRA,
        CarrierState.DAGGER,
    }
)
"""الحالاتُ التي تفتح مقطعًا؛ مقروءةٌ من المفردة القائمة لا مُبتكَرةٌ هنا."""

_SAKIN_STATES: Final[frozenset[CarrierState]] = frozenset(
    {CarrierState.SUKUN_EXPLICIT, CarrierState.SUKUN_IMPLICIT}
)

NEUTRAL_ALEF_CARRIER: Final[str] = "\u0627"
"""الحاملُ الذي يُعامَل محايدًا في أوّل الكلمة: الألفُ العاري لا سواه."""

NEUTRAL_ONSET_STATES: Final[frozenset[CarrierState]] = frozenset(
    {CarrierState.SUKUN_IMPLICIT}
)
"""الحالةُ الوحيدةُ التي يُقبَل معها الحياد: ألفٌ لم تُكتَب عليه علامةٌ أصلًا."""


class SyllableOnset(Enum):
    """صدرُ المقطع: حاملٌ متحرّكٌ موصوف، أو ألفٌ محايدٌ لا نواةَ يدّعيها."""

    MOVING_CARRIER = "moving_carrier"
    NEUTRAL_ALEF = "neutral_alef"


def _is_neutral_alef(unit: CarrierStateUnit) -> bool:
    """أهذه الوحدةُ ألفٌ عارٍ؟ مقروءٌ من الحامل والحالة لا من موضعٍ وحدَه."""

    return unit.carrier == NEUTRAL_ALEF_CARRIER and unit.state in NEUTRAL_ONSET_STATES


def _is_unwritten(unit: CarrierStateUnit) -> bool:
    """أخلت هذه الوحدةُ من كلّ علامةٍ مكتوبة؟ لا حركةَ ولا سكونَ ولا شدّة.

    هذا هو الشرطُ الوحيدُ لامتداد المفتتح المحايد؛ فوحدةٌ عليها سكونٌ مكتوبٌ أو
    شدّةٌ حالتُها **مقروءةٌ من الخطّ**، فلا تدخل فيما لم يُكتَب.
    """

    return unit.state is CarrierState.SUKUN_IMPLICIT and unit.gemination is None


@dataclass(frozen=True, slots=True)
class Syllable:
    """مقطعٌ واحد: مدًى متّصلٌ على الوحدات، بموضعِ بدايته ووحداته بأعيانها."""

    start: int
    units: tuple[CarrierStateUnit, ...]
    onset: SyllableOnset = SyllableOnset.MOVING_CARRIER

    def __post_init__(self) -> None:
        if not isinstance(self.start, int) or self.start < 0:
            raise SyllableSegmentationError(
                SyllableRefusal.NO_UNIT_AT_ALL,
                "موضعُ بدء المقطع عددٌ غيرُ سالب",
            )
        if not self.units:
            raise SyllableSegmentationError(
                SyllableRefusal.NO_UNIT_AT_ALL,
                "مقطعٌ بلا وحدةٍ واحدةٍ ليس مقطعًا قصيرًا بل لا مقطعَ أصلًا",
            )
        if not isinstance(self.onset, SyllableOnset):
            raise SyllableSegmentationError(
                SyllableRefusal.NO_UNIT_AT_ALL,
                "صدرُ المقطع مفردةٌ مغلقةٌ لا نصٌّ حُرّ",
            )
        if self.onset is SyllableOnset.NEUTRAL_ALEF:
            if not _is_neutral_alef(self.units[0]):
                raise SyllableSegmentationError(
                    SyllableRefusal.ONSETLESS_INITIAL_SAKIN,
                    "الحيادُ للألف العاري وحدَه؛ ولا يُوسَّع إلى حاملٍ آخر",
                )
            if self.start != 0:
                raise SyllableSegmentationError(
                    SyllableRefusal.ONSETLESS_INITIAL_SAKIN,
                    "الحيادُ مدًى مُعلَنٌ: أوّلُ الكلمة وحدَه لا وسطُها",
                )
            self._refuse_a_written_state_inside_the_opening()
        elif self.units[0].state not in NUCLEUS_STATES:
            raise SyllableSegmentationError(
                SyllableRefusal.ONSETLESS_INITIAL_SAKIN,
                "المقطعُ يبدأ بحاملٍ متحرّك؛ والساكنُ لا يفتح مقطعًا",
            )
        elif len(self.units) > 2:
            raise SyllableSegmentationError(
                SyllableRefusal.TWO_ADJACENT_SAKINS,
                "المقطعُ حاملٌ متحرّكٌ ومعه ساكنٌ واحدٌ على الأكثر",
            )

    def _refuse_a_written_state_inside_the_opening(self) -> None:
        """المفتتحُ المحايد: وحداتٌ بلا علامةٍ مكتوبة، وساكنٌ واحدٌ يُغلِقه."""

        for unit in self.units[:-1]:
            if not _is_unwritten(unit):
                raise SyllableSegmentationError(
                    SyllableRefusal.TWO_ADJACENT_SAKINS,
                    "المفتتحُ المحايدُ لا يبتلع وحدةً حالتُها مكتوبة",
                )
        last = self.units[-1]
        if not _is_unwritten(last) and last.state not in _SAKIN_STATES:
            raise SyllableSegmentationError(
                SyllableRefusal.TWO_ADJACENT_SAKINS,
                "المفتتحُ المحايدُ يُغلَق بساكنٍ واحدٍ على الأكثر؛ "
                "والمتحرّكُ يفتح مقطعًا موصوفًا لا يدخل فيه",
            )

    @property
    def length(self) -> int:
        """عددُ الوحدات في هذا المقطع؛ مشتقٌّ لا مكتوب."""

        return len(self.units)

    @property
    def undecided_opening(self) -> tuple[CarrierStateUnit, ...]:
        """وحداتُ المفتتح التي لم تُكتَب عليها علامة؛ فارغةٌ في المقطع الموصوف."""

        if self.onset is not SyllableOnset.NEUTRAL_ALEF:
            return ()
        opening: list[CarrierStateUnit] = []
        for unit in self.units:
            if not _is_unwritten(unit):
                break
            opening.append(unit)
        return tuple(opening)

    @property
    def has_coda(self) -> bool:
        """أفي المقطع ساكنٌ بعد صدره؟ مقروءٌ من الوحدات لا من اسمٍ."""

        if self.onset is SyllableOnset.NEUTRAL_ALEF:
            return len(self.units) > len(self.undecided_opening)
        return len(self.units) == 2

    @property
    def claims_a_nucleus(self) -> bool:
        """أيدّعي هذا المقطعُ نواةً موصوفة؟ المحايدُ لا يدّعيها ولا يُخمّنها."""

        return self.onset is not SyllableOnset.NEUTRAL_ALEF


@dataclass(frozen=True, slots=True)
class SyllableParse:
    """تقطيعُ كلمةٍ واحدة: مقاطعُها، وعددُ الوحدات الداخلة، لا نسبةَ فيه."""

    syllables: tuple[Syllable, ...]
    unit_total: int

    def __post_init__(self) -> None:
        if not self.syllables:
            raise SyllableSegmentationError(
                SyllableRefusal.NO_UNIT_AT_ALL,
                "تقطيعٌ بلا مقطعٍ واحدٍ ليس قراءةً لكلمةٍ بلا مقاطع",
            )
        covered = sum(syllable.length for syllable in self.syllables)
        if covered != self.unit_total:
            raise SyllableSegmentationError(
                SyllableRefusal.NO_UNIT_AT_ALL,
                "المقاطعُ تستوعب كلَّ وحدةٍ مرّةً واحدة؛ وتقطيعٌ يُسقِط وحدةً "
                "أو يُكرّرها ليس تجزئةً",
            )
        expected = 0
        for syllable in self.syllables:
            if syllable.start != expected:
                raise SyllableSegmentationError(
                    SyllableRefusal.NO_UNIT_AT_ALL,
                    "المقاطعُ متجاورةٌ بمواضعها؛ وفجوةٌ بينها تقطيعٌ لغير ما قُرِئ",
                )
            expected += syllable.length
        for syllable in self.syllables[1:]:
            if syllable.onset is SyllableOnset.NEUTRAL_ALEF:
                raise SyllableSegmentationError(
                    SyllableRefusal.ONSETLESS_INITIAL_SAKIN,
                    "الصدرُ المحايدُ واحدٌ في أوّل الكلمة؛ ولا يتكرّر في وسطها",
                )

    @property
    def neutral_onset_count(self) -> int:
        """كم مقطعًا افتُتح بصدرٍ محايدٍ لا نواةَ يدّعيها؟ مشتقٌّ لا مكتوب."""

        return sum(
            1
            for syllable in self.syllables
            if syllable.onset is SyllableOnset.NEUTRAL_ALEF
        )

    @property
    def undecided_opening_length(self) -> int:
        """كم وحدةً في مفتتح الكلمة لم تُكتَب عليها علامة؟ مشتقٌّ لا مكتوب."""

        return sum(len(syllable.undecided_opening) for syllable in self.syllables)


def segment(units: Sequence[CarrierStateUnit]) -> SyllableParse:
    """قطِّع وحداتِ الحامل/الحالة إلى مقاطعَ متجاورة، أو ارفع رفضًا مُسمًّى.

    لا تُصلَح هنا عاهةُ ما تحت: وحدةٌ مُمرَّرةٌ أو ساكنٌ لا متحرّكَ قبله يُرفَع
    رفضًا برمزه ولا يُلحَق بمقطعٍ مجاورٍ تجميلًا للجدول.
    """

    if not units:
        raise SyllableSegmentationError(
            SyllableRefusal.NO_UNIT_AT_ALL,
            "تقطيعُ لا وحدةَ فيه ليس تقطيعَ كلمةٍ خالية",
        )

    syllables: list[Syllable] = []
    index = 0
    total = len(units)
    while index < total:
        unit = units[index]
        if unit.state is CarrierState.PASSTHROUGH:
            raise SyllableSegmentationError(
                SyllableRefusal.PASSTHROUGH_IS_NOT_SYLLABIFIED,
                "رمزٌ خارج الحوامل المُعلَنة لا يُقطَّع مقطعًا ولا يُحذَف",
            )
        onset = SyllableOnset.MOVING_CARRIER
        if index == 0 and _is_neutral_alef(unit):
            onset = SyllableOnset.NEUTRAL_ALEF
        elif unit.state in _SAKIN_STATES:
            raise SyllableSegmentationError(
                SyllableRefusal.ONSETLESS_INITIAL_SAKIN
                if index == 0
                else SyllableRefusal.TWO_ADJACENT_SAKINS,
                "ساكنٌ لا متحرّكَ يفتح له مقطعًا",
            )
        span = [unit]
        following = index + 1
        if onset is SyllableOnset.NEUTRAL_ALEF:
            while following < total and _is_unwritten(units[following]):
                span.append(units[following])
                following += 1
        if following < total:
            candidate = units[following]
            if candidate.state in _SAKIN_STATES:
                span.append(candidate)
                following += 1
        syllables.append(Syllable(start=index, units=tuple(span), onset=onset))
        index = following

    return SyllableParse(syllables=tuple(syllables), unit_total=total)


def desegment(syllables: Iterable[Syllable]) -> tuple[CarrierStateUnit, ...]:
    """أعِد الوحداتِ من المقاطع بترتيبها؛ هذه هي الدالّةُ العكسيّةُ نفسُها."""

    units: list[CarrierStateUnit] = []
    for syllable in syllables:
        units.extend(syllable.units)
    if not units:
        raise SyllableSegmentationError(
            SyllableRefusal.NO_UNIT_AT_ALL,
            "إعادةٌ بلا وحدةٍ واحدةٍ ليست إعادةَ كلمةٍ خالية",
        )
    return tuple(units)


SEGMENTATION_IS_NOT_A_WAZN_NOTE: Final[str] = (
    "SegmentationIsNotAWazn: ما يخرج من هنا مدًى على وحداتٍ قائمة، لا وزنٌ ولا "
    "كائنٌ صرفيٌّ مولود؛ وطبقةُ «المقطع والوزن» في القاموس البنيويّ تبقى محجوبةً "
    "حتّى تُكتَب أرضيّةُ قبولها قبل قياسها"
)

A_REFUSAL_IS_NOT_A_SEGMENTATION_NOTE: Final[str] = (
    "ARefusalIsNotASegmentation: الساكنُ في أوّل الكلمة، والساكنان المتجاوران، "
    "والرمزُ المُمرَّر تُرفَع بأسمائها ولا تُلحَق بمقاطعَ مجاورةٍ لتخرج نسبةُ "
    "تقطيعٍ نظيفة"
)

THE_INVERSE_IS_RUN_NOT_ASSERTED_NOTE: Final[str] = (
    "TheInverseIsRunNotAsserted: `desegment` تُنفَّذ ويُقارَن ناتجُها بالوحدات "
    "الداخلة في كلّ قياس؛ ولا تُكتَب في هذه الوحدة نسبةُ استرجاعٍ واحدة"
)

THE_ALEF_IS_A_NEUTRAL_ELEMENT_NOTE: Final[str] = (
    "TheAlefIsANeutralElement: الألفُ العاري في أوّل الكلمة صدرٌ محايدٌ يفتح "
    "مقطعًا ولا يدّعي نواةً؛ فلا حركةَ تُخمَّن له، ولا يُعَدُّ مقطعًا موصوفًا "
    "(`claims_a_nucleus=False`)، ومداهُ أوّلُ الكلمة وحدَه، والوحدةُ تُردّ "
    "بعينها في العكس"
)

THE_OPENING_BEFORE_THE_FIRST_VOWEL_IS_NOT_WRITTEN_NOTE: Final[str] = (
    "TheOpeningBeforeTheFirstVowelIsNotWritten: قوانينُ الابتداء والوصل والوقف "
    "لا تُكتَب في الخطّ، فما في مفتتح الكلمة من وحداتٍ بلا علامةٍ ألبتّة — "
    "يفتتحها الألفُ العاري — يُعامَل مدًى محايدًا واحدًا يُغلَق بساكنٍ واحدٍ "
    "على الأكثر؛ وهذا توسيعُ امتناعٍ لا قراءةُ إدغامٍ ولا تسميةُ لامِ تعريف، "
    "والوحداتُ تُردّ بأعيانها، وما بعد أوّلِ حركةٍ مكتوبةٍ خارجٌ عنه بتمامه"
)
