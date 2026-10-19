"""السكونُ المُضمَر: عمودٌ ليس حرفًا، وعلاجُه أن يُفصَل لا أن يُجمَع.

بين الحركات الأربع **السكونُ وحدَه ليس علامةً بالضرورة**. الفتحةُ والكسرةُ
والضمّةُ لكلٍّ منها نقطةُ ترميزٍ مكتوبةٌ لا تُقرأ إلّا بها؛ أمّا السكونُ
فيُقرأ مرّةً من علامةٍ مكتوبة (U+0652) ومرّةً **من لا شيء**: من خلوّ الحامل.
فكلُّ جدولٍ يضع للسكون عمودًا واحدًا قد **جمع مصدرين مختلفَي المنزلة** في
خانةٍ واحدة: مرصودًا ومستنتَجًا.

وهذا ليس تنظيرًا. قِيس على بايتات الفاتحة المُودَعة في هذه الشجرة
(`fatiha_source_text`) بمولّد الحالات المُدوَّر (`carrier_state_candidate`):

    خمسةٌ وسبعون حاملًا ساكنًا، منها **واحدٌ وعشرون مكتوبًا (28.000%)**
    و**أربعةٌ وخمسون لا أثرَ لها في النصّ (72.000%)**.

فأقلُّ من ثلث السكون مرئيّ. والباقي **استنتاجٌ من الغياب**، والغيابُ لا
بصمةَ له (`WHAT_IS_READ_FROM_ABSENCE_IS_NOT_READ_FROM_BYTES`).

**والعلاجُ فصلٌ لا جَبر.** لا يُصلَح هذا بأن تُكتَب السكونُ في النصّ — فذاك
تحريرُ مصدرٍ لا قياسُه — ولا بأن يُقال «السكونُ كذا» رقمًا واحدًا. يُصلَح
بأن **يُمنَع الرقمُ الواحد**: كلُّ عدٍّ للسكون ههنا يخرج مفصولًا بمصدره، ولا
تُخرِج هذه الوحدةُ مجموعًا عاريًا إلّا مقرونًا بنصيبه المرئيّ
(`A_MERGED_SUKUN_COLUMN_IS_TWO_COLUMNS_COLLAPSED`).

**والمُضمَرُ نفسُه ليس بابًا واحدًا.** الأربعةُ والخمسون تنقسم بأسبابٍ ثلاثةٍ
متمايزة:

| المصدر | العدّة | النصيب |
|---|---|---|
| ألفٌ لا تحمل علامةً قطّ | 23 | 42.593% |
| أوّلُ زوج الشدّة، ولا يُكتَب له شيء | 14 | 25.926% |
| حاملٌ عارٍ سوى ذلك | 17 | 31.481% |

وأوّلُ الزوج **ليس سكونًا أصلًا**: هو نصفُ حرفٍ مشدَّد، سُجِّل سكونًا لأنّ
الرسمَ لا يكتب له شيئًا. فربعُ المُضمَر تقريبًا مقولةٌ أخرى دخلت العمود
(`A_GEMINATION_HALF_IS_NOT_A_SUKUN_AND_STILL_COUNTS_AS_ONE`).

**والألفُ أشدُّها**: من ثلاثٍ وعشرين ألفًا في الفاتحة، **كلُّها** بسكونٍ
مُضمَر، ولا واحدةَ بعلامةٍ مكتوبة ولا بحركة. فحيادُ الألف المقيسُ في
`alif_neutrality` وفي `wasl_alif_neutrality` **مبنيٌّ بتمامه على غيابٍ**: لا
بايتَ واحدًا يقول إنّ الألفَ ساكنة (`THE_ALIFS_NEUTRALITY_RESTS_ENTIRELY_ON_AN_ABSENCE`).

**وأثرُه في جدول الابتداء.** بعد رفع ألف الوصل، افتتح أربعةَ عشرَ من كلمات
الفاتحة بساكن: **خمسةٌ بعلامةٍ مكتوبة (35.714%)** وتسعةٌ بلا شيء. فالعمودُ
«سكون» في الموضع الأوّل — الذي عُدَّ فيه 10,182 موضعًا في
`position_haraka_bit_account` — **عمودان مجموعان**، وثلثاه على هذا القياس
غيرُ مكتوبٍ أصلًا. ولا سبيلَ إلى فصلهما هناك: الجدولُ منقولٌ ولا بايتاتِ له
(`THE_DEPOSITED_ONSET_SUKUN_CANNOT_BE_SPLIT_WHERE_IT_LIVES`).

**وسَعةُ القياس تسعٌ وعشرون كلمة.** هذه الأعدادُ كلُّها من الفاتحة وحدَها،
وهي جزءٌ من ألفٍ من المصحف. فالنسبُ ههنا **مقيسةٌ صادقةٌ على ما قِيست عليه**،
ولا تُعمَّم على 78,215 ولا يُضرَب بها فيها
(`A_RATE_MEASURED_ON_ONE_SURA_IS_NOT_A_CORPUS_RATE`).

**خمولٌ سلطويّ**: لا ولادةَ ولا حكمَ ولا تجميد، ولا استيرادَ من `kernel/`.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from .encoding.carrier_state_candidate import (
    CarrierState,
    CarrierStateCodec,
    CarrierStateUnit,
)
from .fatiha_source_text import FATIHA_LINES

__all__ = [
    "A_GEMINATION_HALF_IS_NOT_A_SUKUN_AND_STILL_COUNTS_AS_ONE",
    "A_MERGED_SUKUN_COLUMN_IS_TWO_COLUMNS_COLLAPSED",
    "A_RATE_MEASURED_ON_ONE_SURA_IS_NOT_A_CORPUS_RATE",
    "IMPLICIT_SUKUN_NAMED_RESIDUALS",
    "THE_ALIFS_NEUTRALITY_RESTS_ENTIRELY_ON_AN_ABSENCE",
    "THE_DEPOSITED_ONSET_SUKUN_CANNOT_BE_SPLIT_WHERE_IT_LIVES",
    "THE_TREATMENT_IS_A_SPLIT_NOT_AN_EDIT_OF_THE_SOURCE",
    "WHAT_IS_READ_FROM_ABSENCE_IS_NOT_READ_FROM_BYTES",
    "ImplicitSukunError",
    "SukunCensus",
    "SukunSource",
    "VisibilityStanding",
    "census_over",
    "measured_onset_census",
    "measured_text_census",
    "onset_census_over",
    "source_of",
    "words_of",
]

THE_ALIF: Final[str] = "ا"
"""الحاملُ الذي لا يحمل علامةً قطّ في هذا القياس."""

_SUKUN_STATES: Final[frozenset[CarrierState]] = frozenset(
    {CarrierState.SUKUN_EXPLICIT, CarrierState.SUKUN_IMPLICIT}
)

_CODEC: Final[CarrierStateCodec] = CarrierStateCodec()


class ImplicitSukunError(ValueError):
    """رفضٌ عند القياس: نصٌّ خالٍ، أو وحدةٌ ليست ساكنةً تُسأل عن مصدر سكونها."""


class SukunSource(Enum):
    """مصدرُ السكون الواحد، أربعةٌ مغلقةٌ لا خامسَ لها."""

    EXPLICIT_MARK = "علامةٌ مكتوبة"
    ALIF_WITHOUT_A_MARK = "ألفٌ بلا علامة"
    GEMINATION_PAIR_START = "أوّلُ زوج الشدّة"
    BARE_CARRIER = "حاملٌ عارٍ"

    @property
    def is_written(self) -> bool:
        """أيُقرأ هذا المصدرُ من بايتٍ مكتوب، أم من غيابه؟"""

        return self is SukunSource.EXPLICIT_MARK


class VisibilityStanding(Enum):
    """حالُ العمود من الرؤية، ثلاثةٌ مغلقةٌ لا رابعَ يُفتَح."""

    MOSTLY_UNWRITTEN = "أكثرُه غيرُ مكتوب"
    MOSTLY_WRITTEN = "أكثرُه مكتوب"
    FULLY_WRITTEN = "كلُّه مكتوب"


@dataclass(frozen=True)
class SukunCensus:
    """إحصاءُ سكونٍ مفصولٌ بمصدره؛ ولا يُخرِج مجموعًا بلا نصيبه المرئيّ."""

    scope: str
    words: int
    by_source: tuple[tuple[SukunSource, int], ...]

    def __post_init__(self) -> None:
        if self.words <= 0:
            raise ImplicitSukunError("إحصاءٌ على صفرِ كلماتٍ ليس إحصاءً.")
        seen = [source for source, _ in self.by_source]
        if len(seen) != len(set(seen)):
            raise ImplicitSukunError("مصدرٌ مكرَّرٌ في الإحصاء، فالعدُّ مزدوج.")
        if any(count < 0 for _, count in self.by_source):
            raise ImplicitSukunError("عدّةٌ سالبةٌ لا تكون.")

    def count_of(self, source: SukunSource) -> int:
        """عدّةُ مصدرٍ بعينه، وصفرًا إن لم يُرصَد."""

        for held, count in self.by_source:
            if held is source:
                return count
        return 0

    @property
    def total(self) -> int:
        """مجموعُ الحوامل الساكنة على اختلاف مصادرها."""

        return sum(count for _, count in self.by_source)

    @property
    def written(self) -> int:
        """ما يُقرأ من بايتٍ مكتوب."""

        return sum(count for source, count in self.by_source if source.is_written)

    @property
    def unwritten(self) -> int:
        """ما يُستنتَج من غياب، ولا بايتَ له."""

        return self.total - self.written

    @property
    def written_share(self) -> float:
        """نصيبُ المكتوب من المجموع، نسبةً مئويّة."""

        if not self.total:
            raise ImplicitSukunError("نصيبٌ على مجموعٍ خالٍ لا يُحسَب.")
        return 100.0 * self.written / self.total

    @property
    def standing(self) -> VisibilityStanding:
        """حكمُ الرؤية، مشتقًّا من النصيب لا مكتوبًا في حقل."""

        if not self.unwritten:
            return VisibilityStanding.FULLY_WRITTEN
        if self.written_share > 50.0:
            return VisibilityStanding.MOSTLY_WRITTEN
        return VisibilityStanding.MOSTLY_UNWRITTEN

    def share_of_unwritten(self, source: SukunSource) -> float:
        """نصيبُ مصدرٍ مُضمَرٍ من المُضمَر كلِّه، نسبةً مئويّة."""

        if source.is_written:
            raise ImplicitSukunError("المكتوبُ لا يُقسَم على المُضمَر.")
        if not self.unwritten:
            raise ImplicitSukunError("لا مُضمَرَ ههنا، فلا نصيبَ منه.")
        return 100.0 * self.count_of(source) / self.unwritten

    def split(self) -> tuple[tuple[str, int], ...]:
        """العلاجُ نفسُه: العمودُ مفصولًا بأسمائه، لا رقمًا واحدًا."""

        return tuple((source.value, count) for source, count in self.by_source)


def source_of(unit: CarrierStateUnit) -> SukunSource:
    """يسمّي مصدرَ سكونِ وحدةٍ ساكنة، ويرفض أن يُسأل عن غيرِ ساكنة."""

    if unit.state not in _SUKUN_STATES:
        raise ImplicitSukunError(
            f"الوحدةُ تحمل {unit.state.value} لا سكونًا، فلا مصدرَ سكونٍ لها."
        )
    if unit.state is CarrierState.SUKUN_EXPLICIT:
        return SukunSource.EXPLICIT_MARK
    if unit.gemination is not None:
        return SukunSource.GEMINATION_PAIR_START
    if unit.carrier == THE_ALIF:
        return SukunSource.ALIF_WITHOUT_A_MARK
    return SukunSource.BARE_CARRIER


def words_of(lines: Iterable[str] = FATIHA_LINES) -> tuple[str, ...]:
    """كلماتُ نصٍّ مُودَعٍ كما يفصلها البياض، ولا تفسيرَ فوق ذلك."""

    return tuple(word for line in lines for word in line.split())


def _tally(
    units_per_word: Sequence[Sequence[CarrierStateUnit]],
) -> tuple[tuple[SukunSource, int], ...]:
    counts: dict[SukunSource, int] = {source: 0 for source in SukunSource}
    for units in units_per_word:
        for unit in units:
            if unit.state in _SUKUN_STATES:
                counts[source_of(unit)] += 1
    return tuple((source, counts[source]) for source in SukunSource)


def census_over(
    lines: Iterable[str] = FATIHA_LINES,
    scope: str = "الفاتحة — كلُّ المواضع",
) -> SukunCensus:
    """يقيس السكونَ كلَّه في نصٍّ مُودَعٍ، مفصولًا بمصادره الأربعة."""

    words = words_of(lines)
    if not words:
        raise ImplicitSukunError("نصٌّ بلا كلماتٍ لا يُقاس.")
    return SukunCensus(
        scope=scope,
        words=len(words),
        by_source=_tally([_CODEC.generate(word) for word in words]),
    )


def onset_census_over(
    lines: Iterable[str] = FATIHA_LINES,
    scope: str = "الفاتحة — الموضع الأوّل بعد رفع ألف الوصل",
) -> SukunCensus:
    """يقيس سكونَ الابتداء وحدَه، بعد رفع الألف التي لا تحمل علامة."""

    words = words_of(lines)
    if not words:
        raise ImplicitSukunError("نصٌّ بلا كلماتٍ لا يُقاس.")
    onsets: list[list[CarrierStateUnit]] = []
    for word in words:
        remaining = [
            unit
            for unit in _CODEC.generate(word)
            if not (
                unit.carrier == THE_ALIF and unit.state is CarrierState.SUKUN_IMPLICIT
            )
        ]
        if remaining:
            onsets.append([remaining[0]])
    return SukunCensus(scope=scope, words=len(words), by_source=_tally(onsets))


def measured_text_census() -> SukunCensus:
    """إحصاءُ الفاتحة كاملًا، مقيسًا عند القراءة لا مكتوبًا في ثابت."""

    return census_over()


def measured_onset_census() -> SukunCensus:
    """إحصاءُ سكون الابتداء في الفاتحة، مقيسًا عند القراءة لا منقولًا."""

    return onset_census_over()


WHAT_IS_READ_FROM_ABSENCE_IS_NOT_READ_FROM_BYTES: Final[str] = (
    "WHAT_IS_READ_FROM_ABSENCE_IS_NOT_READ_FROM_BYTES: الفتحةُ والكسرةُ "
    "والضمّةُ لها نقاطُ ترميزٍ تُقرأ منها، والسكونُ يُقرأ مرّةً من U+0652 "
    "ومرّةً من خلوّ الحامل. وقِيس على الفاتحة: 21 من 75 مكتوبٌ (28.000%) و54 "
    "مُضمَر (72.000%). فأكثرُ العمود **استنتاجٌ من غياب**، والغيابُ لا بصمةَ "
    "له ولا يُبصَّم."
)

A_MERGED_SUKUN_COLUMN_IS_TWO_COLUMNS_COLLAPSED: Final[str] = (
    "A_MERGED_SUKUN_COLUMN_IS_TWO_COLUMNS_COLLAPSED: كلُّ جدولٍ يضع للسكون "
    "عمودًا واحدًا يجمع مرصودًا بمستنتَجٍ في خانة. وعلاجُه ههنا أنّ "
    "`SukunCensus` لا يُخرِج مجموعًا إلّا ومعه نصيبُه المرئيّ وتفصيلُه "
    "بمصادره، و`split()` هي المخرَجُ المقصود لا `total`."
)

A_GEMINATION_HALF_IS_NOT_A_SUKUN_AND_STILL_COUNTS_AS_ONE: Final[str] = (
    "A_GEMINATION_HALF_IS_NOT_A_SUKUN_AND_STILL_COUNTS_AS_ONE: من 54 مُضمَرًا "
    "في الفاتحة 14 (25.926%) أوّلُ زوج شدّة — نصفُ حرفٍ مشدَّد لا حرفٌ ساكن، "
    "دخل العمودَ لأنّ الرسمَ لا يكتب له شيئًا. فرُبعُ المُضمَر تقريبًا مقولةٌ "
    "أخرى، ولا يُميَّز منها شيءٌ في جدولٍ لا عمودَ فيه للشدّة."
)

THE_ALIFS_NEUTRALITY_RESTS_ENTIRELY_ON_AN_ABSENCE: Final[str] = (
    "THE_ALIFS_NEUTRALITY_RESTS_ENTIRELY_ON_AN_ABSENCE: من 23 ألفًا في "
    "الفاتحة، كلُّها بسكونٍ مُضمَر ولا واحدةَ بعلامةٍ مكتوبةٍ ولا بحركة. "
    "فحيادُ الألف في `alif_neutrality` و`wasl_alif_neutrality` مبنيٌّ بتمامه "
    "على غياب: لا بايتَ واحدًا يقول إنّ الألفَ ساكنة، وإنّما يقول إنّها "
    "**غيرُ موسومة**. والفرقُ بينهما هو مدارُ هذه الوحدة."
)

THE_DEPOSITED_ONSET_SUKUN_CANNOT_BE_SPLIT_WHERE_IT_LIVES: Final[str] = (
    "THE_DEPOSITED_ONSET_SUKUN_CANNOT_BE_SPLIT_WHERE_IT_LIVES: بعد رفع ألف "
    "الوصل، افتتح 14 من كلمات الفاتحة بساكن: 5 بعلامةٍ (35.714%) و9 بلا شيء. "
    "فعمودُ سكون الابتداء المُودَع (10,182 في "
    "`position_haraka_bit_account`) عمودان مجموعان. ولا يُفصَلان هناك: "
    "الجدولُ منقولٌ ولا بايتاتِ له في الشجرة، فالفصلُ يبقى مطلوبًا لا مُنجَزًا."
)

A_RATE_MEASURED_ON_ONE_SURA_IS_NOT_A_CORPUS_RATE: Final[str] = (
    "A_RATE_MEASURED_ON_ONE_SURA_IS_NOT_A_CORPUS_RATE: كلُّ نسبةٍ ههنا مقيسةٌ "
    "على 29 كلمةً من الفاتحة، وهي جزءٌ من ألفٍ من المصحف. فهي صادقةٌ على ما "
    "قِيست عليه، ولا تُضرَب في 78,215 ولا تُقرأ نصيبًا للمصحف. والفاتحةُ "
    "أكثفُ تعريفًا (أل) من سواها، فميلُها نحو المُضمَر متوقَّعٌ لا مُقدَّر."
)

THE_TREATMENT_IS_A_SPLIT_NOT_AN_EDIT_OF_THE_SOURCE: Final[str] = (
    "THE_TREATMENT_IS_A_SPLIT_NOT_AN_EDIT_OF_THE_SOURCE: لم يُكتَب سكونٌ في "
    "نصٍّ، ولم يُعدَّل حرفٌ، ولم يُضَف إلى المصدر ما ليس فيه. العلاجُ أن "
    "يُسمَّى المصدرُ عند كلّ عدّة، فيبقى النصُّ كما وُدِع ويبقى الفرقُ بين "
    "المرصود والمستنتَج ظاهرًا. وكتابةُ السكون في النصّ كانت ستكون تحريرَ "
    "مصدرٍ لا قياسًا له."
)

IMPLICIT_SUKUN_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "WHAT_IS_READ_FROM_ABSENCE_IS_NOT_READ_FROM_BYTES": (
        WHAT_IS_READ_FROM_ABSENCE_IS_NOT_READ_FROM_BYTES
    ),
    "A_MERGED_SUKUN_COLUMN_IS_TWO_COLUMNS_COLLAPSED": (
        A_MERGED_SUKUN_COLUMN_IS_TWO_COLUMNS_COLLAPSED
    ),
    "A_GEMINATION_HALF_IS_NOT_A_SUKUN_AND_STILL_COUNTS_AS_ONE": (
        A_GEMINATION_HALF_IS_NOT_A_SUKUN_AND_STILL_COUNTS_AS_ONE
    ),
    "THE_ALIFS_NEUTRALITY_RESTS_ENTIRELY_ON_AN_ABSENCE": (
        THE_ALIFS_NEUTRALITY_RESTS_ENTIRELY_ON_AN_ABSENCE
    ),
    "THE_DEPOSITED_ONSET_SUKUN_CANNOT_BE_SPLIT_WHERE_IT_LIVES": (
        THE_DEPOSITED_ONSET_SUKUN_CANNOT_BE_SPLIT_WHERE_IT_LIVES
    ),
    "A_RATE_MEASURED_ON_ONE_SURA_IS_NOT_A_CORPUS_RATE": (
        A_RATE_MEASURED_ON_ONE_SURA_IS_NOT_A_CORPUS_RATE
    ),
    "THE_TREATMENT_IS_A_SPLIT_NOT_AN_EDIT_OF_THE_SOURCE": (
        THE_TREATMENT_IS_A_SPLIT_NOT_AN_EDIT_OF_THE_SOURCE
    ),
}
"""ما لا يُثبِته هذا العلاجُ مُسمًّى باسمه، لا مطويًّا في رقمٍ واحد."""

_FORBIDDEN_FIELD_TOKENS: Final[tuple[str, ...]] = (
    "authority",
    "born",
    "birth",
    "gate",
    "rank",
    "verdict",
)


def _assert_no_authority_field() -> None:
    """حارسُ استيراد: لا حقلَ سلطةٍ ولا رتبةٍ في إحصاءٍ لا سلطةَ فيه."""

    for declared in fields(SukunCensus):
        lowered = declared.name.lower()
        for token in _FORBIDDEN_FIELD_TOKENS:
            if token in lowered:
                raise ImplicitSukunError(
                    f"حقلٌ يحمل سلطةً أو رتبةً تسلّل إلى SukunCensus: "
                    f"{declared.name}؛ وهذا إحصاءٌ لا سلطةَ فيه."
                )


def _assert_the_sukun_is_still_mostly_unwritten() -> None:
    """حارسُ استيراد: لو صار السكونُ كلُّه مكتوبًا فقد حُرِّر المصدرُ لا قِيس."""

    census = measured_text_census()
    if census.standing is VisibilityStanding.FULLY_WRITTEN:
        raise ImplicitSukunError(
            "صار السكونُ كلُّه مكتوبًا في النصّ المُودَع؛ وهذا تحريرُ مصدرٍ "
            "لا قياسٌ له، وهو عينُ ما تمنعه هذه الوحدة."
        )
    if census.count_of(SukunSource.ALIF_WITHOUT_A_MARK) != sum(
        1
        for word in words_of()
        for unit in _CODEC.generate(word)
        if unit.carrier == THE_ALIF and unit.state in _SUKUN_STATES
    ):
        raise ImplicitSukunError(
            "ألفٌ ساكنةٌ خرجت عن باب «ألفٌ بلا علامة»؛ فإمّا حملت علامةً "
            "وإمّا صُنِّفت خطأً، وكلاهما ينقض ما تقوم عليه هذه الوحدة."
        )


_assert_no_authority_field()
_assert_the_sukun_is_still_mostly_unwritten()
