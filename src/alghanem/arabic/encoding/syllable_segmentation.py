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
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Final

from .carrier_state_candidate import CarrierState, CarrierStateUnit

__all__ = [
    "A_REFUSAL_IS_NOT_A_SEGMENTATION_NOTE",
    "NUCLEUS_STATES",
    "SEGMENTATION_IS_NOT_A_WAZN_NOTE",
    "THE_INVERSE_IS_RUN_NOT_ASSERTED_NOTE",
    "Syllable",
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


@dataclass(frozen=True, slots=True)
class Syllable:
    """مقطعٌ واحد: مدًى متّصلٌ على الوحدات، بموضعِ بدايته ووحداته بأعيانها."""

    start: int
    units: tuple[CarrierStateUnit, ...]

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
        if self.units[0].state not in NUCLEUS_STATES:
            raise SyllableSegmentationError(
                SyllableRefusal.ONSETLESS_INITIAL_SAKIN,
                "المقطعُ يبدأ بحاملٍ متحرّك؛ والساكنُ لا يفتح مقطعًا",
            )
        if len(self.units) > 2:
            raise SyllableSegmentationError(
                SyllableRefusal.TWO_ADJACENT_SAKINS,
                "المقطعُ حاملٌ متحرّكٌ ومعه ساكنٌ واحدٌ على الأكثر",
            )

    @property
    def length(self) -> int:
        """عددُ الوحدات في هذا المقطع؛ مشتقٌّ لا مكتوب."""

        return len(self.units)

    @property
    def has_coda(self) -> bool:
        """أفي المقطع ساكنٌ بعد متحرّكه؟ مقروءٌ من الوحدات لا من اسمٍ."""

        return len(self.units) == 2


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
        if unit.state in _SAKIN_STATES:
            raise SyllableSegmentationError(
                SyllableRefusal.ONSETLESS_INITIAL_SAKIN
                if index == 0
                else SyllableRefusal.TWO_ADJACENT_SAKINS,
                "ساكنٌ لا متحرّكَ يفتح له مقطعًا",
            )
        span = [unit]
        following = index + 1
        if following < total:
            candidate = units[following]
            if candidate.state in _SAKIN_STATES:
                span.append(candidate)
                following += 1
        syllables.append(Syllable(start=index, units=tuple(span)))
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
