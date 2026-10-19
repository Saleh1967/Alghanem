"""تكرارُ تجربةِ «الجزءُ بنيةُ الكلّ» على أبواب المعجم كلِّها، لا على بابٍ واحد.

سُئل قبلُ: أشذوذٌ في باب الدال خروجُ نصيب الشاهد الشعريّ عن السماحيّة، أم
انحرافٌ موزَّعٌ على الأبواب جميعًا؟ والسؤالُ يُحسَم بالعدّ لا بالنظر، فهذه
الوحدة تُجري القياسَ نفسَه على كلّ بابٍ في البايتات المُودَعة، وتفصل::

    OneChapterRefuted      != ThatChapterIsAnomalous
    PartVersusWhole        != PartVersusComplement
    AVerdictAtOneTolerance != AMeasuredClaim
    PassingTheBand         != PowerToFailIt

**النتيجةُ تنقض الفرضَ الذي بُني عليه السؤال.** بابُ الدال ليس شاذًّا: فرقُه
في الشاهد الشعريّ يقع في **المرتبة الخامسةَ عشرةَ من أربعين**، وخمسةَ عشرَ بابًا
تتجاوزه. بل هو من أقرب الأبواب إلى الكلّ إجمالًا، إذ يجتاز أربعةً من خمسة
والأبوابُ المجتازةُ للخمسة كلِّها **بابان من أربعين**. فالانحرافُ موزَّعٌ لا
مُتمركِز، وقراءةُ نقضٍ في بابٍ واحدٍ شذوذًا لذلك الباب تعميمٌ من عيّنةِ واحد
(`A_REFUTATION_IN_ONE_CHAPTER_IS_NOT_A_PROPERTY_OF_THAT_CHAPTER`).

**والتحيّزُ الاحتوائيُّ يُقاس ههنا ولا يُسمّى فحسب.** البابُ داخلٌ في الكلّ
الذي يُقابَل به، فمقابلتُه به تجذب النصيبين أحدَهما إلى الآخر. وعلاجُه مقابلةُ
البابِ بمُتمِّمه — بالجدول منقوصًا منه — وهي مقابلةُ مجموعتين منفصلتين. وأثرُ
ذلك **مقيسٌ لا مفترَض**: المقابلةُ بالمتمّم توسّع الفرقَ في المائتَي قياسٍ
كلِّها ولا تضيّقه في واحد. فالتحيّزُ باتّجاهٍ واحدٍ مُثبَتٍ بالعدّ، ولا يُنقِذ
بابًا سقط ولا يُسقِط بابًا قام (`THE_COMPLEMENT_COMPARISON_NEVER_RESCUES_A_CHAPTER`).

**والسماحيّةُ مِقبَضٌ، فتُقرَأ منحنًى لا حكمًا عند نقطة.** الحكمُ الواحدُ عند
`0.05` دالّةٌ في عتبةٍ اختيرت؛ فتُخرِج هذه الوحدةُ عددَ الأبواب المجتازة عند
كلّ سماحيّةٍ مُعلَنة، ويُشتَقّ لكلّ بابٍ **أصغرُ سماحيّةٍ يجتاز بها**. فمن
أراد حكمًا عند عتبةٍ أعلنها فليعلنها، ويقرأ معها ثمنَها في سائر الأبواب
(`A_VERDICT_AT_ONE_TOLERANCE_IS_A_FUNCTION_OF_THAT_TOLERANCE`).

**واجتيازُ السماحيّة ليس دائمًا شهادةَ تشابه.** في سبعةٍ وعشرين بابًا من أربعين
لا جذرَ واحدٌ من نوع «ثلاثي معتل»؛ فنصيبُه صفرٌ وفرقُه نصيبُ الكلّ نفسُه، وهو
دون السماحيّة بالبناء. فذلك اجتيازٌ **بلا قدرةٍ على السقوط**، ويُعَدّ على حدةٍ
ولا يُجمَع مع اجتيازٍ ذي قدرة (`PowerlessPass`). وكذلك أربعةَ عشرَ بابًا دون
ثلاثين مدخلًا، يزحزح فيها المدخلُ الواحدُ النصيبَ أكثرَ من السماحيّة كلِّها.

**والتقسيمُ الذي يعطيه المصدرُ ليس نقيًّا، ولا يُنظَّف ههنا.** في عمود الترويسة
سطورٌ ليست ترويسةَ بابٍ أصلًا — «كتاب رسول اللّه ﵌» ومطلعُ شرحٍ سقط في موضع
الترويسة. وتنقيتُها باليد بعد رؤية النتائج تفصيلٌ على المقاس، فتُعَدّ وتُسمّى
وتبقى في القياس، ويخرج عددُها مع كلّ قراءة
(`THE_SOURCE_PARTITION_IS_POLLUTED_AND_IS_NOT_CLEANED_HERE`).

**خمولٌ سلطويّ**: لا ولادةَ هنا ولا حكمَ ولادةٍ ولا تجميدَ `E0`، ولا استيرادَ
من `kernel/`، ولا يُرفَع بهذه الوحدة شرطٌ من شروط الإغلاق.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from .dal_alone_gloss import (
    DECLARED_TOLERANCE,
    THE_DAL_CHAPTER_HEADER,
    THE_PROFILE_AXES,
    DalGlossEntry,
    ProfileAxis,
    profile_of,
    whole_table_entries,
)

__all__ = [
    "AN_UNEQUAL_CHAPTER_SIZE_IS_NOT_AN_UNEQUAL_SUBJECT",
    "A_REFUTATION_IN_ONE_CHAPTER_IS_NOT_A_PROPERTY_OF_THAT_CHAPTER",
    "A_VERDICT_AT_ONE_TOLERANCE_IS_A_FUNCTION_OF_THAT_TOLERANCE",
    "MAQAYIS_CHAPTER_CENSUS_NAMED_RESIDUALS",
    "THE_COMPLEMENT_COMPARISON_NEVER_RESCUES_A_CHAPTER",
    "THE_DECLARED_SIZE_STRATUM",
    "THE_DECLARED_TOLERANCE_LADDER",
    "THE_SHARES_ARE_OF_ENTRIES_NOT_OF_THE_LANGUAGE",
    "THE_SOURCE_PARTITION_IS_POLLUTED_AND_IS_NOT_CLEANED_HERE",
    "A_DISTRIBUTED_DEVIATION_IS_NOT_AN_EXPLAINED_ONE",
    "ChapterCensus",
    "ChapterReading",
    "DivergenceLocality",
    "LocalityVerdict",
    "MaqayisChapterCensusError",
    "PowerlessPass",
    "ToleranceRung",
    "assess_divergence_locality",
    "chapter_entries",
    "chapter_headers",
    "read_chapter",
    "run_chapter_census",
]


class MaqayisChapterCensusError(ValueError):
    """خطأٌ في إحصاء الأبواب أو في مقابلة بابٍ بالكلّ أو بمتمّمه."""


THE_DECLARED_TOLERANCE_LADDER: Final[tuple[float, ...]] = (
    0.05,
    0.10,
    0.15,
    0.20,
    0.25,
    0.50,
)
"""سُلَّمُ السماحيّات المُعلَنُ قبل القراءة؛ ولا تُزاد درجةٌ بعد رؤية النتيجة."""

THE_DECLARED_SIZE_STRATUM: Final[int] = 30
"""حدُّ العدّة المُعلَن؛ طبقةٌ تُعلَن مع الرقم لا مصفاةٌ تُسقِط أبوابًا من القياس."""


# --- تقسيمُ المصدر ---------------------------------------------------------------


def chapter_headers() -> tuple[str, ...]:
    """ترويساتُ الأبواب كما وردت، مرتَّبةً على أوّل ورودٍ لا على هجاء.

    والترويسةُ الخاليةُ ليست بابًا فلا تدخل؛ وصفوفُها تُعَدّ في
    `ChapterCensus.entries_outside_any_chapter` ولا تُطوى.
    """

    seen: list[str] = []
    for entry in whole_table_entries():
        header = entry.chapter_header
        if header and header not in seen:
            seen.append(header)
    if not seen:
        raise MaqayisChapterCensusError("جدولٌ بلا ترويسةِ بابٍ واحدةٍ لا يُقسَّم")
    return tuple(seen)


def chapter_entries(header: str) -> tuple[DalGlossEntry, ...]:
    """مداخلُ بابٍ واحدٍ بترويسته، مقروءةً من البايتات عند كلّ نداء."""

    entries = tuple(
        entry for entry in whole_table_entries() if entry.chapter_header == header
    )
    if not entries:
        raise MaqayisChapterCensusError(
            f"لا صفَّ تحت ترويسة «{header}»؛ وبابٌ خالٍ يُوقِف القراءة ولا يُقرَأ صفرًا"
        )
    return entries


# --- قراءةُ بابٍ واحد -------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class PowerlessPass:
    """اجتيازٌ بلا قدرةٍ على السقوط: محورٌ نصيبُه صفرٌ في الباب.

    فالفرقُ حينئذٍ نصيبُ الكلّ نفسُه، فإن كان دون السماحيّة فالاجتيازُ مُعطًى
    بالبناء لا مقيسًا؛ وعدُّه مع سائر الاجتيازات يضخّم عددَ الموافقات.
    """

    axis: ProfileAxis
    whole_share: float

    def __post_init__(self) -> None:
        if not 0.0 <= self.whole_share <= 1.0:
            raise MaqayisChapterCensusError("نصيبٌ خارجَ المجال ليس نصيبًا")


@dataclass(frozen=True, slots=True)
class ChapterReading:
    """قراءةُ بابٍ واحد: نصيبُه، ونصيبُ الكلّ، ونصيبُ متمّمه، على المحاور كلِّها.

    ولا حكمَ مكتوبٌ ههنا: الفروقُ والاجتيازاتُ والسماحيّةُ اللازمة كلُّها
    خاصّيّاتٌ تُشتقّ عند السؤال.
    """

    header: str
    size: int
    part_shares: tuple[float, ...]
    whole_shares: tuple[float, ...]
    complement_shares: tuple[float, ...]

    def __post_init__(self) -> None:
        widths = {
            len(self.part_shares),
            len(self.whole_shares),
            len(self.complement_shares),
        }
        if widths != {len(THE_PROFILE_AXES)}:
            raise MaqayisChapterCensusError(
                "المحاورُ تُقرأ كلُّها أو لا تُقرأ؛ وإسقاطُ محورٍ تشابهٌ صامت"
            )
        if self.size <= 0:
            raise MaqayisChapterCensusError("بابٌ بعدّةٍ غيرِ موجبةٍ لا تُقسَم نِسَبُه")

    @property
    def gaps_against_the_whole(self) -> tuple[float, ...]:
        """فروقُ المحاور مقابلَ الجدول كلِّه، مُشتقّةً بالطرح."""

        return tuple(
            abs(part - whole)
            for part, whole in zip(self.part_shares, self.whole_shares, strict=True)
        )

    @property
    def gaps_against_the_complement(self) -> tuple[float, ...]:
        """فروقُ المحاور مقابلَ الجدول منقوصًا منه؛ مقابلةُ منفصلَين لا محتويَين."""

        return tuple(
            abs(part - rest)
            for part, rest in zip(self.part_shares, self.complement_shares, strict=True)
        )

    @property
    def powerless_passes(self) -> tuple[PowerlessPass, ...]:
        """المحاورُ التي نصيبُ الباب فيها صفر؛ اجتيازُها مُعطًى لا مقيس."""

        return tuple(
            PowerlessPass(axis=axis, whole_share=whole)
            for axis, part, whole in zip(
                THE_PROFILE_AXES, self.part_shares, self.whole_shares, strict=True
            )
            if part == 0.0
        )

    @property
    def is_below_the_size_stratum(self) -> bool:
        """أعدّةُ الباب دون الحدّ المُعلَن؟ تُعلَن مع رقمه ولا تُسقِطه."""

        return self.size < THE_DECLARED_SIZE_STRATUM

    def diverging_axes(
        self, tolerance: float = DECLARED_TOLERANCE, *, against_complement: bool = False
    ) -> tuple[ProfileAxis, ...]:
        """المحاورُ الخارجةُ عن سماحيّةٍ مُمرَّرة، مُسمّاةً لا معدودةً فحسب."""

        if tolerance < 0.0:
            raise MaqayisChapterCensusError("سماحيّةٌ سالبةٌ ليست سماحيّة")
        gaps = (
            self.gaps_against_the_complement
            if against_complement
            else self.gaps_against_the_whole
        )
        return tuple(
            axis
            for axis, gap in zip(THE_PROFILE_AXES, gaps, strict=True)
            if gap > tolerance
        )

    def mirrors_the_whole(self, tolerance: float = DECLARED_TOLERANCE) -> bool:
        """أيجتاز البابُ المحاورَ الخمسةَ عند سماحيّةٍ مُمرَّرة؟"""

        return not self.diverging_axes(tolerance)

    def gap_on(self, axis: ProfileAxis) -> float:
        """فرقُ محورٍ بعينه مقابلَ الكلّ؛ يُسأل بالمحور لا بموضعه في الصفّ."""

        return self.gaps_against_the_whole[THE_PROFILE_AXES.index(axis)]

    @property
    def smallest_tolerance_that_passes(self) -> float:
        """أصغرُ سماحيّةٍ يجتاز بها البابُ المحاورَ كلَّها: أكبرُ فروقه.

        وهي قراءةُ الحكمِ منحنًى بدل نقطة؛ فبها يُقارَن بابٌ ببابٍ بلا عتبةٍ
        مفروضةٍ سلفًا على المقارنة.
        """

        return max(self.gaps_against_the_whole)


def read_chapter(header: str) -> ChapterReading:
    """اقرأ بابًا واحدًا: نصيبُه ونصيبُ الكلّ ونصيبُ متمّمه، مُشتقّةً بالعدّ."""

    everything = whole_table_entries()
    inside = tuple(entry for entry in everything if entry.chapter_header == header)
    outside = tuple(entry for entry in everything if entry.chapter_header != header)
    if not inside:
        raise MaqayisChapterCensusError(
            f"لا صفَّ تحت ترويسة «{header}»؛ وبابٌ خالٍ يُوقِف القراءة"
        )
    if not outside:
        raise MaqayisChapterCensusError(
            "بابٌ يستغرق الجدولَ كلَّه لا متمّمَ له، فلا تقوم المقابلةُ المنفصلة"
        )
    part = profile_of(header, inside)
    whole = profile_of("الجدولُ كلُّه", everything)
    complement = profile_of("الجدولُ منقوصًا منه", outside)
    return ChapterReading(
        header=header,
        size=part.size,
        part_shares=tuple(part.share(axis) for axis in THE_PROFILE_AXES),
        whole_shares=tuple(whole.share(axis) for axis in THE_PROFILE_AXES),
        complement_shares=tuple(complement.share(axis) for axis in THE_PROFILE_AXES),
    )


# --- إحصاءُ الأبواب جميعًا ---------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ToleranceRung:
    """درجةٌ من سُلَّم السماحيّة: كم بابًا يجتاز عندها."""

    tolerance: float
    mirroring_chapters: int
    chapter_count: int

    def __post_init__(self) -> None:
        if not 0 <= self.mirroring_chapters <= self.chapter_count:
            raise MaqayisChapterCensusError("مجتازون أكثرُ من الأبواب كلِّها؛ عدٌّ فاسد")


@dataclass(frozen=True, slots=True)
class ChapterCensus:
    """إحصاءُ الأبواب كلِّها؛ ولا رقمَ مكتوبٌ فيه، كلُّه خاصّيّاتٌ تُحسَب."""

    readings: tuple[ChapterReading, ...]
    entries_outside_any_chapter: int

    def __post_init__(self) -> None:
        if not self.readings:
            raise MaqayisChapterCensusError("إحصاءٌ بلا بابٍ واحدٍ لا يُقرَأ")
        if len({item.header for item in self.readings}) != len(self.readings):
            raise MaqayisChapterCensusError("بابٌ تكرّر في الإحصاء؛ والتكرارُ يُضخّم")
        if self.entries_outside_any_chapter < 0:
            raise MaqayisChapterCensusError("صفوفٌ خارجَ الأبواب عددٌ غيرُ سالبٍ بالبناء")

    @property
    def chapter_count(self) -> int:
        """عددُ الأبواب، مُشتقًّا بالعدّ."""

        return len(self.readings)

    @property
    def partition_covers_the_table(self) -> bool:
        """أيستغرق تقسيمُ الترويسات الجدولَ كلَّه؟ يُقرَأ ولا يُفترَض."""

        return self.entries_outside_any_chapter == 0

    @property
    def chapters_below_the_size_stratum(self) -> int:
        """كم بابًا عدّتُه دون الحدّ المُعلَن؟ يُعلَن مع كلّ حكمٍ إجماليّ."""

        return sum(1 for item in self.readings if item.is_below_the_size_stratum)

    def mirroring_chapters(
        self, tolerance: float = DECLARED_TOLERANCE
    ) -> tuple[ChapterReading, ...]:
        """الأبوابُ المجتازةُ للمحاور كلِّها عند سماحيّةٍ مُمرَّرة."""

        return tuple(
            item for item in self.readings if item.mirrors_the_whole(tolerance)
        )

    def diverging_chapters_on(
        self, axis: ProfileAxis, tolerance: float = DECLARED_TOLERANCE
    ) -> tuple[ChapterReading, ...]:
        """الأبوابُ الخارجةُ عن السماحيّة في محورٍ بعينه."""

        return tuple(
            item for item in self.readings if axis in item.diverging_axes(tolerance)
        )

    def tolerance_ladder(self) -> tuple[ToleranceRung, ...]:
        """منحنى الحكم: كم بابًا يجتاز عند كلّ درجةٍ من السُّلَّم المُعلَن."""

        return tuple(
            ToleranceRung(
                tolerance=tolerance,
                mirroring_chapters=len(self.mirroring_chapters(tolerance)),
                chapter_count=self.chapter_count,
            )
            for tolerance in THE_DECLARED_TOLERANCE_LADDER
        )

    def ranked_by_gap_on(self, axis: ProfileAxis) -> tuple[ChapterReading, ...]:
        """الأبوابُ مرتَّبةً تنازليًّا بفرقها في محورٍ بعينه، ثمّ بترويستها."""

        return tuple(
            sorted(self.readings, key=lambda item: (-item.gap_on(axis), item.header))
        )

    def rank_of(self, header: str, axis: ProfileAxis) -> int:
        """مرتبةُ بابٍ في فرقه على محور، بدءًا من الواحد؛ تُشتَقّ لا تُكتَب."""

        ordered = [item.header for item in self.ranked_by_gap_on(axis)]
        if header not in ordered:
            raise MaqayisChapterCensusError(f"بابٌ غيرُ محصًى لا مرتبةَ له: «{header}»")
        return ordered.index(header) + 1

    @property
    def the_complement_comparison_only_widens(self) -> bool:
        """أتوسّع مقابلةُ المتمّم كلَّ فرقٍ ولا تضيّق واحدًا؟ يُقاس ولا يُفترَض.

        وهذا اتّجاهُ التحيّز الاحتوائيّ مُثبَتًا بالعدّ: البابُ داخلٌ في الكلّ
        فيجذبه إليه، ونزعُه من الكلّ يُظهِر فرقًا أوسع. فإن صدق هذا لم تكن
        مقابلةُ المتمّم مُنقِذةً لبابٍ سقط في مقابلة الكلّ.
        """

        return all(
            wide >= narrow
            for item in self.readings
            for narrow, wide in zip(
                item.gaps_against_the_whole,
                item.gaps_against_the_complement,
                strict=True,
            )
        )


def run_chapter_census() -> ChapterCensus:
    """أجرِ القياسَ على الأبواب كلِّها من البايتات المُودَعة، في قراءةٍ واحدة."""

    everything = whole_table_entries()
    headers = chapter_headers()
    readings = tuple(read_chapter(header) for header in headers)
    outside = sum(1 for entry in everything if not entry.chapter_header)
    return ChapterCensus(readings=readings, entries_outside_any_chapter=outside)


# --- حكمُ موضع الانحراف ------------------------------------------------------------


class DivergenceLocality(Enum):
    """أين يقع الانحرافُ: في بابٍ بعينه أم في الأبواب جميعًا؟ ثلاثٌ لا اثنتان."""

    ANOMALOUS_TO_THE_NAMED_CHAPTER = "شاذٌّ_بالبابِ_المُسمّى"
    SHARED_ACROSS_THE_CHAPTERS = "موزَّعٌ_على_الأبواب"
    UNDECIDED_FOR_WANT_OF_A_SEPARATING_MARGIN = "غيرُ_مفصولٍ_لضيق_الفارق"


@dataclass(frozen=True, slots=True)
class LocalityVerdict:
    """حكمُ موضع الانحراف، مُشتقًّا من الإحصاء لا مكتوبًا بجانبه."""

    header: str
    axis: ProfileAxis
    rank: int
    chapter_count: int
    chapters_exceeding: int
    tolerance: float

    def __post_init__(self) -> None:
        if not 1 <= self.rank <= self.chapter_count:
            raise MaqayisChapterCensusError("مرتبةٌ خارجَ عدد الأبواب ليست مرتبة")
        if self.chapters_exceeding < 0:
            raise MaqayisChapterCensusError("متجاوزون بعددٍ سالبٍ عدٌّ فاسد")

    @property
    def standing(self) -> DivergenceLocality:
        """المنزلةُ خاصّيّةٌ تُشتَقّ؛ ولا حقلَ منزلةٍ ههنا.

        والشذوذُ يُدَّعى بالانفراد: بابٌ لا يتجاوزه أحدٌ في فرقه شاذٌّ بحقّ.
        فإن تجاوزه بابٌ واحدٌ فأكثر فالانحرافُ مشترَكٌ لا خاصٌّ به. وبقيت
        حالةٌ ثالثةٌ لا تُطوى: أن يكون منفردًا وفرقُه دون السماحيّة أصلًا،
        فلا انحرافَ يُنسَب إليه ولا شذوذَ يُقال.
        """

        if self.chapters_exceeding > 0:
            return DivergenceLocality.SHARED_ACROSS_THE_CHAPTERS
        if self.rank == 1 and self.chapters_exceeding == 0:
            return DivergenceLocality.ANOMALOUS_TO_THE_NAMED_CHAPTER
        return DivergenceLocality.UNDECIDED_FOR_WANT_OF_A_SEPARATING_MARGIN


def assess_divergence_locality(
    census: ChapterCensus | None = None,
    header: str = THE_DAL_CHAPTER_HEADER,
    axis: ProfileAxis = ProfileAxis.SHARE_WITH_POETRY,
    tolerance: float = DECLARED_TOLERANCE,
) -> LocalityVerdict:
    """أشذوذٌ بالباب المُسمّى فرقُه في محورٍ مُسمًّى، أم انحرافٌ موزَّع؟"""

    taken = run_chapter_census() if census is None else census
    matches = [item for item in taken.readings if item.header == header]
    if not matches:
        raise MaqayisChapterCensusError(f"بابٌ غيرُ محصًى لا يُحكَم عليه: «{header}»")
    own_gap = matches[0].gap_on(axis)
    return LocalityVerdict(
        header=header,
        axis=axis,
        rank=taken.rank_of(header, axis),
        chapter_count=taken.chapter_count,
        chapters_exceeding=sum(
            1 for item in taken.readings if item.gap_on(axis) > own_gap
        ),
        tolerance=tolerance,
    )


# --- البقايا المُسمّاة --------------------------------------------------------------


A_REFUTATION_IN_ONE_CHAPTER_IS_NOT_A_PROPERTY_OF_THAT_CHAPTER: Final[str] = (
    "A_REFUTATION_IN_ONE_CHAPTER_IS_NOT_A_PROPERTY_OF_THAT_CHAPTER: نقضُ دعوى "
    "«الجزءُ بنيةُ الكلّ» في باب الدال كان حكمًا على الدعوى لا وصفًا للباب. "
    "وقد تبيّن بالعدّ أنّ بابَ الدال من أقرب الأبواب إلى الكلّ لا من أبعدها، "
    "فمن قرأ النقضَ شذوذًا في المادّة قرأ في عيّنةِ واحدٍ ما لا تحمله."
)

THE_COMPLEMENT_COMPARISON_NEVER_RESCUES_A_CHAPTER: Final[str] = (
    "THE_COMPLEMENT_COMPARISON_NEVER_RESCUES_A_CHAPTER: مقابلةُ البابِ بمتمّمه "
    "تُزيل التحيّزَ الاحتوائيّ، وقد قيس أثرُها فوجِد توسيعًا في كلّ قياسٍ ولا "
    "تضييقَ في واحد. فهي تشديدٌ لا ترخيص، ولا يُقرَأ سقوطُ بابٍ فيها نتيجةً "
    "جديدةً بل تأكيدًا لسقوطه في المقابلة المتحيّزة لصالحه."
)

A_VERDICT_AT_ONE_TOLERANCE_IS_A_FUNCTION_OF_THAT_TOLERANCE: Final[str] = (
    "A_VERDICT_AT_ONE_TOLERANCE_IS_A_FUNCTION_OF_THAT_TOLERANCE: عددُ الأبواب "
    "المجتازة يتغيّر بالسماحيّة تغيّرًا واسعًا، فلا يُنقَل حكمٌ عند عتبةٍ بلا "
    "ذكرها. وهذه الوحدةُ تُخرِج السُّلَّمَ كلَّه وأصغرَ سماحيّةٍ يجتاز بها كلُّ "
    "باب، فلا تُغلِق على عتبةٍ واحدةٍ ولا تُرخي لتمرّ نتيجة."
)

AN_UNEQUAL_CHAPTER_SIZE_IS_NOT_AN_UNEQUAL_SUBJECT: Final[str] = (
    "AN_UNEQUAL_CHAPTER_SIZE_IS_NOT_AN_UNEQUAL_SUBJECT: عدّةُ الأبواب تتفاوت "
    "من مدخلَين إلى مئاتٍ، فالفرقُ في البابِ الصغير يزحزحه مدخلٌ واحد. وحدُّ "
    "العدّة يُعلَن طبقةً تُقرَأ مع الرقم، ولا يُتّخذ مصفاةً تُسقِط أبوابًا بعد "
    "رؤية نتائجها؛ فإسقاطُها بعدَها انتقاءٌ على المقاس."
)

THE_SOURCE_PARTITION_IS_POLLUTED_AND_IS_NOT_CLEANED_HERE: Final[str] = (
    "THE_SOURCE_PARTITION_IS_POLLUTED_AND_IS_NOT_CLEANED_HERE: في عمود الترويسة "
    "سطورٌ ليست ترويسةَ بابٍ بل نصٌّ سقط في موضعها. وتنقيتُها باليد بعد رؤية "
    "النتائج تفصيلٌ على المقاس، فتبقى في القياس معدودةً مُسمّاة؛ وعددُ الأبواب "
    "ههنا عددُ ترويساتٍ متمايزة، لا عددُ أبوابٍ في المعجم بالضرورة."
)

THE_SHARES_ARE_OF_ENTRIES_NOT_OF_THE_LANGUAGE: Final[str] = (
    "THE_SHARES_ARE_OF_ENTRIES_NOT_OF_THE_LANGUAGE: كلُّ نصيبٍ ههنا نصيبٌ من "
    "مداخلِ هذا الاستخراج، لا من كلام العرب ولا من المطبوع. فنصيبُ الشاهد "
    "الشعريّ نصيبُ الصفوفِ التي حُمِل فيها الشاهدُ إلى عمودٍ في هذا الملفّ، "
    "وخلوُّ العمود قد يكون خلوَّ الاستخراج لا خلوَّ الأصل."
)

A_DISTRIBUTED_DEVIATION_IS_NOT_AN_EXPLAINED_ONE: Final[str] = (
    "A_DISTRIBUTED_DEVIATION_IS_NOT_AN_EXPLAINED_ONE: إثباتُ أنّ الانحراف موزَّعٌ "
    "على الأبواب ينفي تفسيرًا واحدًا — أنّه خاصّةُ بابٍ بعينه — ولا يُثبِت "
    "بديلًا. وسببُ التوزّع غيرُ مقيسٍ ههنا: أهو تفاوتُ تأليف ابن فارس بين "
    "الأبواب، أم تفاوتُ الاستخراج، أم صِغَرُ أبوابٍ كثيرةٍ يُضخّم فروقَها؟ "
    "ثلاثةٌ لم يُفصَل بينها، ولا تُرجَّح واحدةٌ بهذه القراءة."
)

MAQAYIS_CHAPTER_CENSUS_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "A_REFUTATION_IN_ONE_CHAPTER_IS_NOT_A_PROPERTY_OF_THAT_CHAPTER": (
        A_REFUTATION_IN_ONE_CHAPTER_IS_NOT_A_PROPERTY_OF_THAT_CHAPTER
    ),
    "THE_COMPLEMENT_COMPARISON_NEVER_RESCUES_A_CHAPTER": (
        THE_COMPLEMENT_COMPARISON_NEVER_RESCUES_A_CHAPTER
    ),
    "A_VERDICT_AT_ONE_TOLERANCE_IS_A_FUNCTION_OF_THAT_TOLERANCE": (
        A_VERDICT_AT_ONE_TOLERANCE_IS_A_FUNCTION_OF_THAT_TOLERANCE
    ),
    "AN_UNEQUAL_CHAPTER_SIZE_IS_NOT_AN_UNEQUAL_SUBJECT": (
        AN_UNEQUAL_CHAPTER_SIZE_IS_NOT_AN_UNEQUAL_SUBJECT
    ),
    "THE_SOURCE_PARTITION_IS_POLLUTED_AND_IS_NOT_CLEANED_HERE": (
        THE_SOURCE_PARTITION_IS_POLLUTED_AND_IS_NOT_CLEANED_HERE
    ),
    "THE_SHARES_ARE_OF_ENTRIES_NOT_OF_THE_LANGUAGE": (
        THE_SHARES_ARE_OF_ENTRIES_NOT_OF_THE_LANGUAGE
    ),
    "A_DISTRIBUTED_DEVIATION_IS_NOT_AN_EXPLAINED_ONE": (
        A_DISTRIBUTED_DEVIATION_IS_NOT_AN_EXPLAINED_ONE
    ),
}
"""ما لا تُثبِته هذه القراءةُ مُسمًّى باسمه، لا مطويًّا في حكمٍ عامّ."""
