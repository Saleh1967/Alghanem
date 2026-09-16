"""قياسُ أعمدة الإعراب في MASAQ من بايتاتٍ مُبصَّمة، أو الوقوفُ دون رقم.

هذا تشغيلُ `irab_column_preregistration` لا تعديلٌ له: لا عمودَ أُضيف بعد
الرقم، ولا قيمةَ بُدِّلت حتّى تُطابق، ولا رقمٌ يخرج من هنا إلّا وقاعدةُ عدِّه
مُجمَّدةٌ هناك وبصمتُها مربوطةٌ به.

`NO_FIGURE_WITHOUT_THE_FINGERPRINTED_BYTES`: كلُّ عددٍ هنا مُشتَقٌّ من
`read_masaq_bytes`، وهي تُطابِق الطولَ والبصمةَ قبل أن تُعيد بايتةً واحدة.
فإن لم تكن البايتاتُ في الشجرة ولا في مسارٍ مُصرَّحٍ به **لم يخرج رقم**، ولم
يُوضَع مكانَه تقديرٌ ولا قيمةٌ محفوظة.

`AN_ABSENT_VALUE_IS_NOT_A_ZERO`: `IrabValueStanding` تفصل ثلاثةَ أحوالٍ كان
خلطُها يُنتِج صفرًا كاذبًا: قيمةٌ وردت وطابق عددُها، وقيمةٌ وردت وخالف، وقيمةٌ
**لم تَرِد في العمود البتّة**. والثالثةُ خبرٌ عن اسم القيمة لا عن المدوَّنة،
فلا تُقرأ نفيًا لشيءٍ في العربية.

`A_MISSING_COLUMN_STOPS_THE_COUNT`: عمودٌ غائبٌ عن الترويسة يُرفَع به خطأٌ ولا
يُحمَل على أقرب اسمٍ إليه ولا يُعَدُّ صفرًا. والفرقُ أنّ الصفرَ يمرّ في تقريرٍ
كأنّه قياس، والخطأَ يقف.

`SEGMENTS_AND_WORDS_ARE_TWO_COUNTS`: الوحدةُ الافتراضيّةُ **مقطع**، وعدُّ
الكلمات يُجمَع بثلاثيّة `(سورة، آية، Column5)`. ويُخرِج هذا الأنبوبُ العددين
معًا لكلّ قيمة، لأنّ قراءةَ أحدهما مكان الآخر هي بعينها العلّةُ التي أهبطت
قياسَ محاذاةٍ من ٢٣٫٣٪ إلى ٠٫٣٪.

`COUNTING_A_JUDGEMENT_IS_NOT_SETTLING_IT`: عدُّ «ضمّةٍ مقدَّرة» إحصاءُ أحكامِ
مُوسِّمٍ على ما لا أثرَ له في الرسم؛ فلا يُحسَم به بابُ المقدَّر، ولا يُقرأ
عددُ «نائب فاعل» مجهولًا مقيسًا في مدوَّنةٍ أخرى.

وهذه الوحدة تسجيلٌ لا سلطة: لا ولادةَ فيها، ولا حكمَ ولادة، ولا تجميدَ `E0`،
ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Final

from .irab_column_preregistration import (
    ARRIVING_COLUMN_COVERAGE,
    ARRIVING_IRAB_FIGURES,
    ARRIVING_SEGMENT_TOTAL,
    IRAB_PREREGISTRATION_DIGEST,
    ArrivingColumnCoverage,
    ArrivingIrabFigure,
    IrabCountingRule,
    column_named,
)
from .masaq_corpus_deposit import (
    MASAQ_SHA256,
    MasaqDepositError,
    masaq_records,
)

__all__ = [
    "A_COVERAGE_IS_COMPARED_AT_ITS_DECLARED_PRECISION_NOTE",
    "CoverageReading",
    "non_empty_cells",
    "read_coverage",
    "read_coverages",
    "segment_total_agrees",
    "A_MISSING_COLUMN_STOPS_THE_COUNT_NOTE",
    "AN_ABSENT_VALUE_IS_NOT_A_ZERO_NOTE",
    "COUNTING_A_JUDGEMENT_IS_NOT_SETTLING_IT_NOTE",
    "IRAB_CENSUS_NAMED_RESIDUALS",
    "NO_FIGURE_WITHOUT_THE_FINGERPRINTED_BYTES_NOTE",
    "SEGMENTS_AND_WORDS_ARE_TWO_COUNTS_NOTE",
    "VERSE_COLUMN",
    "SURA_COLUMN",
    "IrabCensusError",
    "IrabColumnCensus",
    "IrabFigureReading",
    "IrabValueStanding",
    "census_from_bytes",
    "column_census",
    "distinct_value_count",
    "read_figure",
    "read_figures",
    "segments_with_value",
    "value_counts",
    "words_with_value",
]


class IrabCensusError(ValueError):
    """تُرفَع حين يُطلَب عددٌ من عمودٍ غائبٍ أو من بايتاتٍ لم تُطابَق."""


NO_FIGURE_WITHOUT_THE_FINGERPRINTED_BYTES_NOTE: Final[str] = (
    "NoFigureWithoutTheFingerprintedBytes: كلُّ عددٍ هنا مُشتَقٌّ من بايتاتٍ "
    "طُوبِق طولُها وبصمتُها قبل قراءتها؛ فإن غابت لم يخرج رقمٌ ولم يُوضَع "
    "مكانَه تقديرٌ ولا قيمةٌ محفوظة"
)

AN_ABSENT_VALUE_IS_NOT_A_ZERO_NOTE: Final[str] = (
    "AnAbsentValueIsNotAZero: «لم تَرِد هذه القيمةُ في العمود» خبرٌ عن اسم "
    "القيمة، و«صفرٌ» خبرٌ عن المدوَّنة؛ وخلطُهما يُنتِج نفيًا لم يُقَس"
)

A_MISSING_COLUMN_STOPS_THE_COUNT_NOTE: Final[str] = (
    "AMissingColumnStopsTheCount: عمودٌ غائبٌ عن الترويسة يُوقِف العدَّ ولا "
    "يُحمَل على أقرب اسمٍ إليه ولا يُعَدُّ صفرًا؛ فالصفرُ يمرّ كأنّه قياس، "
    "والخطأُ يقف"
)

SEGMENTS_AND_WORDS_ARE_TWO_COUNTS_NOTE: Final[str] = (
    "SegmentsAndWordsAreTwoCounts: الوحدةُ الافتراضيّةُ مقطعٌ لا كلمة، "
    "وعدُّ الكلمات يُجمَع بثلاثيّة (سورة، آية، Column5)؛ فيُخرَج العددان معًا "
    "لأنّ قراءةَ أحدهما مكان الآخر أهبطت قياسًا من ٢٣٫٣٪ إلى ٠٫٣٪"
)

COUNTING_A_JUDGEMENT_IS_NOT_SETTLING_IT_NOTE: Final[str] = (
    "CountingAJudgementIsNotSettlingIt: عدُّ «ضمّةٍ مقدَّرة» إحصاءُ أحكامٍ "
    "على ما لا أثرَ له في الرسم فلا يحسم بابَ المقدَّر، وعددُ «نائب فاعل» "
    "شاهدٌ في هذه المدوَّنة لا مجهولٌ مقيسٌ في غيرها"
)

A_COVERAGE_IS_COMPARED_AT_ITS_DECLARED_PRECISION_NOTE: Final[str] = (
    "ACoverageIsComparedAtItsDeclaredPrecision: النسبةُ المقيسةُ تُقرَّب إلى "
    "منازل النسبة المُصرَّح بها ثمّ تُقارَن؛ فـ٨٤٫٤٥٪ تُقارَن بمنزلتين، "
    "ومطابقتُها لا تُثبِت المنزلةَ الثالثة، وعددُ الخلايا المملوءةِ يُعاد "
    "معها كي يُقرأ العددُ ولا تُقرأ النسبةُ عددًا"
)


IRAB_CENSUS_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "ACoverageIsComparedAtItsDeclaredPrecision": (
        A_COVERAGE_IS_COMPARED_AT_ITS_DECLARED_PRECISION_NOTE
    ),
    "NoFigureWithoutTheFingerprintedBytes": (
        NO_FIGURE_WITHOUT_THE_FINGERPRINTED_BYTES_NOTE
    ),
    "AnAbsentValueIsNotAZero": AN_ABSENT_VALUE_IS_NOT_A_ZERO_NOTE,
    "AMissingColumnStopsTheCount": A_MISSING_COLUMN_STOPS_THE_COUNT_NOTE,
    "SegmentsAndWordsAreTwoCounts": SEGMENTS_AND_WORDS_ARE_TWO_COUNTS_NOTE,
    "CountingAJudgementIsNotSettlingIt": COUNTING_A_JUDGEMENT_IS_NOT_SETTLING_IT_NOTE,
}


SURA_COLUMN: Final[str] = "Sura_No"
VERSE_COLUMN: Final[str] = "Verse_No"

_WORD_KEY_COLUMN: Final[str] = "Column5"


def _require_column(records: Sequence[Mapping[str, str]], column: str) -> None:
    """احرسْ حضورَ العمود في الترويسة؛ وغيابُه يُوقِف العدَّ لا يُصفِّره."""

    if not records:
        raise IrabCensusError(
            "لا سجلَّ يُقرأ؛ ولا يُخرَج عددٌ من ملفٍّ بلا سجلّات. "
            + NO_FIGURE_WITHOUT_THE_FINGERPRINTED_BYTES_NOTE
        )
    if column not in records[0]:
        raise IrabCensusError(
            f"العمودُ «{column}» غائبٌ عن الترويسة. "
            + A_MISSING_COLUMN_STOPS_THE_COUNT_NOTE
        )


def value_counts(records: Sequence[Mapping[str, str]], column: str) -> dict[str, int]:
    """توزيعُ قيم العمود بالمطابقة الحرفيّة؛ والقيمةُ الفارغةُ ليست قيمة."""

    _require_column(records, column)
    counts: dict[str, int] = {}
    for record in records:
        value = record.get(column, "").strip()
        if not value:
            continue
        counts[value] = counts.get(value, 0) + 1
    return counts


def distinct_value_count(records: Sequence[Mapping[str, str]], column: str) -> int:
    """عددُ القيم المتمايزة تحت `DISTINCT_COLUMN_VALUES`."""

    return len(value_counts(records, column))


def segments_with_value(
    records: Sequence[Mapping[str, str]], column: str, value: str
) -> int:
    """عددُ المقاطع التي قيمةُ عمودها مطابقةٌ حرفيًّا للقيمة المطلوبة."""

    _require_column(records, column)
    return sum(1 for record in records if record.get(column, "").strip() == value)


def words_with_value(
    records: Sequence[Mapping[str, str]], column: str, value: str
) -> int:
    """عددُ الكلمات لا المقاطع: ثلاثيّةُ `(سورة، آية، مفتاح الكلمة)` متمايزةً.

    `SegmentsAndWordsAreTwoCounts`: هذا عددٌ آخرُ بقاعدةٍ أخرى، ولا يُقرأ
    أحدُهما مكان الآخر ولو تقاربا.
    """

    _require_column(records, column)
    for key in (SURA_COLUMN, VERSE_COLUMN, _WORD_KEY_COLUMN):
        _require_column(records, key)
    words = {
        (record[SURA_COLUMN], record[VERSE_COLUMN], record[_WORD_KEY_COLUMN])
        for record in records
        if record.get(column, "").strip() == value
    }
    return len(words)


class IrabValueStanding(Enum):
    """منزلةُ القيمة المُدَّعاة؛ وثلاثتُها كانت تُخلَط في صفرٍ واحدٍ كاذب."""

    PRESENT_AND_AGREES = "واردةٌ_وطابق_عددُها"
    PRESENT_AND_DIFFERS = "واردةٌ_وخالف_عددُها"
    NOT_A_VALUE_OF_THIS_COLUMN = "ليست_من_قيم_هذا_العمود"


@dataclass(frozen=True, slots=True)
class IrabFigureReading:
    """قراءةُ رقمٍ واردٍ من البايتات: المُدَّعى، والمُشتَقّ، ومنزلةُ قيمته."""

    figure: ArrivingIrabFigure
    derived_count: int
    word_count: int | None
    standing: IrabValueStanding
    preregistration_digest: str
    corpus_digest: str

    @property
    def agrees(self) -> bool:
        """أطابق المُدَّعى المُشتَقَّ؟ والغيابُ ليس موافقةً ولو تساوى العددان."""

        return self.standing is IrabValueStanding.PRESENT_AND_AGREES


def read_figure(
    records: Sequence[Mapping[str, str]],
    figure: ArrivingIrabFigure,
    *,
    corpus_digest: str = MASAQ_SHA256,
) -> IrabFigureReading:
    """أعِد اشتقاقَ رقمٍ واردٍ واحد، وسمِّ منزلةَ قيمته بلا طيٍّ ولا تقريب."""

    column_named(figure.column)
    if figure.counting_rule is IrabCountingRule.DISTINCT_COLUMN_VALUES:
        derived = distinct_value_count(records, figure.column)
        standing = (
            IrabValueStanding.PRESENT_AND_AGREES
            if derived == figure.claimed_count
            else IrabValueStanding.PRESENT_AND_DIFFERS
        )
        return IrabFigureReading(
            figure=figure,
            derived_count=derived,
            word_count=None,
            standing=standing,
            preregistration_digest=IRAB_PREREGISTRATION_DIGEST,
            corpus_digest=corpus_digest,
        )

    value = figure.value
    if value is None:
        raise IrabCensusError("رقمٌ بقاعدةِ قيمةٍ بلا قيمة؛ والتسجيلُ يمنعه.")
    counts = value_counts(records, figure.column)
    if value not in counts:
        return IrabFigureReading(
            figure=figure,
            derived_count=0,
            word_count=None,
            standing=IrabValueStanding.NOT_A_VALUE_OF_THIS_COLUMN,
            preregistration_digest=IRAB_PREREGISTRATION_DIGEST,
            corpus_digest=corpus_digest,
        )
    derived = counts[value]
    standing = (
        IrabValueStanding.PRESENT_AND_AGREES
        if derived == figure.claimed_count
        else IrabValueStanding.PRESENT_AND_DIFFERS
    )
    return IrabFigureReading(
        figure=figure,
        derived_count=derived,
        word_count=words_with_value(records, figure.column, value),
        standing=standing,
        preregistration_digest=IRAB_PREREGISTRATION_DIGEST,
        corpus_digest=corpus_digest,
    )


def read_figures(
    records: Sequence[Mapping[str, str]],
    figures: Sequence[ArrivingIrabFigure] = ARRIVING_IRAB_FIGURES,
    *,
    corpus_digest: str = MASAQ_SHA256,
) -> tuple[IrabFigureReading, ...]:
    """قراءةُ الأرقام الواردة كلِّها؛ ولا يُتخطّى رقمٌ خالف صامتًا."""

    return tuple(
        read_figure(records, figure, corpus_digest=corpus_digest) for figure in figures
    )


@dataclass(frozen=True, slots=True)
class IrabColumnCensus:
    """جردُ عمودٍ واحد: قيمُه بتوزيعها، وعددُ المتمايز، وعددُ ما لم يُوسَم."""

    column: str
    distinct_values: int
    counts: dict[str, int]
    unannotated_segments: int

    @property
    def annotated_segments(self) -> int:
        """المقاطعُ التي حملت قيمةً غيرَ فارغةٍ في هذا العمود."""

        return sum(self.counts.values())


def column_census(
    records: Sequence[Mapping[str, str]], column: str
) -> IrabColumnCensus:
    """جردُ العمود كلِّه؛ والفراغُ يُعَدُّ «لم يُوسَم» لا يُحمَل على قيمة."""

    counts = value_counts(records, column)
    annotated = sum(counts.values())
    return IrabColumnCensus(
        column=column,
        distinct_values=len(counts),
        counts=counts,
        unannotated_segments=len(records) - annotated,
    )


@dataclass(frozen=True, slots=True)
class CoverageReading:
    """قراءةُ تغطيةِ عمودٍ: عددُها ومقامُها ونسبتُها، والمُدَّعى إلى جانبها."""

    column: str
    declared_percentage: str
    non_empty_cells: int
    total_records: int

    @property
    def measured_percentage(self) -> float:
        """النسبةُ المقيسةُ كاملةً؛ ولا تُقارَن بها بل بمُقرَّبِها."""

        if self.total_records == 0:
            raise IrabCensusError(
                "لا سجلَّ يُقسَم عليه. " + NO_FIGURE_WITHOUT_THE_FINGERPRINTED_BYTES_NOTE
            )
        return 100.0 * self.non_empty_cells / self.total_records

    @property
    def agrees(self) -> bool:
        """أطابقت عند المنازل المُصرَّح بها وحدَها؟ `ACoverageIsNotACount`."""

        places = len(self.declared_percentage.split(".")[1])
        return f"{self.measured_percentage:.{places}f}" == self.declared_percentage


def non_empty_cells(records: Sequence[Mapping[str, str]], column: str) -> int:
    """عددُ الخلايا المملوءة تحت `NON_EMPTY_COLUMN_CELLS`؛ والغيابُ يُوقِف العدّ."""

    _require_column(records, column)
    return sum(1 for record in records if record.get(column, "").strip())


def read_coverage(
    records: Sequence[Mapping[str, str]], coverage: ArrivingColumnCoverage
) -> CoverageReading:
    """أعِد اشتقاقَ تغطيةِ عمودٍ مُدَّعاةٍ؛ وعمودٌ غائبٌ يُرفَع به خطأ."""

    return CoverageReading(
        column=coverage.column,
        declared_percentage=coverage.declared_percentage,
        non_empty_cells=non_empty_cells(records, coverage.column),
        total_records=len(records),
    )


def read_coverages(
    records: Sequence[Mapping[str, str]],
    coverages: Sequence[ArrivingColumnCoverage] = ARRIVING_COLUMN_COVERAGE,
) -> tuple[CoverageReading, ...]:
    """قراءةُ التغطيات كلِّها؛ ولا تُسقَط واحدةٌ لأنّ عمودَها ليس من الخمسة."""

    return tuple(read_coverage(records, coverage) for coverage in coverages)


def segment_total_agrees(records: Sequence[Mapping[str, str]]) -> bool:
    """أطابق عددُ السجلّات جملةَ المقاطع المُدَّعاة؟ عدًّا لا اشتقاقًا من نسبة."""

    return len(records) == ARRIVING_SEGMENT_TOTAL


def census_from_bytes(data: bytes) -> tuple[IrabFigureReading, ...]:
    """اقرأ السجلّات من بايتاتٍ مُطابَقةٍ سلفًا، ثمّ أعِد اشتقاقَ الأرقام كلِّها.

    والبايتاتُ تأتي من `read_masaq_bytes` وحدَها: هي التي تُطابِق الطولَ
    والبصمةَ قبل القراءة. `NoFigureWithoutTheFingerprintedBytes`.
    """

    try:
        records = masaq_records(data)
    except MasaqDepositError as error:
        raise IrabCensusError(
            f"لم تُقرأ سجلّاتُ المدوَّنة: {error}. "
            + NO_FIGURE_WITHOUT_THE_FINGERPRINTED_BYTES_NOTE
        ) from error
    return read_figures(records)
