"""اختباراتُ تجميد أعمدة الإعراب وقياسِها، بأسطرٍ مُصطنَعةٍ مُصرَّحٍ بجنسها.

`SyntheticLinesAreDeclaredNotHidden`: الأسطرُ هنا **مُصطنَعة**، تُحاكي بنيةَ
الصفّ وحدَها؛ ولا يخرج منها رقمٌ عن MASAQ البتّة. والأرقامُ الثلاثةَ عشرَ
الواردةُ لا تُقاس إلّا من البايتات المُبصَّمة، واختبارُها الواحدُ يُفعَّل
حين تكون في `corpora/MASAQ.csv` أو في `ALGHANEM_MASAQ_PATH`.
"""

from __future__ import annotations

import os
import unicodedata

import pytest

from alghanem.arabic.irab_column_census import (
    IRAB_CENSUS_NAMED_RESIDUALS,
    CoverageReading,
    IrabCensusError,
    IrabValueStanding,
    census_from_bytes,
    column_census,
    distinct_value_count,
    non_empty_cells,
    read_coverage,
    read_coverages,
    read_figure,
    read_figures,
    segment_total_agrees,
    segments_with_value,
    value_counts,
    words_with_value,
)
from alghanem.arabic.irab_column_preregistration import (
    ARRIVING_COLUMN_COVERAGE,
    ARRIVING_IRAB_FIGURES,
    ARRIVING_SEGMENT_TOTAL,
    CASE_MOOD_COLUMN,
    CASE_MOOD_MARKER_COLUMN,
    FIRST_CONSIGNMENT_IRAB_FIGURES,
    INVARIABLE_DECLINABLE_COLUMN,
    IRAB_COLUMNS,
    IRAB_PREREGISTRATION_DIGEST,
    IRAB_PREREGISTRATION_NAMED_RESIDUALS,
    PHRASAL_FUNCTION_COLUMN,
    PRE_REGISTERED_EXPECTATION,
    SECOND_CONSIGNMENT_IRAB_FIGURES,
    SPELLING_CHECK_BESIDE_THE_EXPECTATION,
    STANDING,
    SYNTACTIC_ROLE_COLUMN,
    ArrivingColumnCoverage,
    ArrivingIrabFigure,
    IrabCountingRule,
    IrabPreregistrationError,
    RegistrationStanding,
    column_named,
    figures_for_column,
    preregistration_digest,
)
from alghanem.arabic.masaq_corpus_deposit import (
    MASAQ_PATH_VARIABLE,
    MASAQ_RELATIVE_PATH,
    masaq_records,
    read_masaq_bytes,
    vendored_masaq_path,
)

SYNTHETIC_RECORDS: tuple[dict[str, str], ...] = (
    {
        "Sura_No": "1",
        "Verse_No": "2",
        "Word_No": "1",
        "Column5": "1",
        SYNTACTIC_ROLE_COLUMN: "مبتدأ",
        CASE_MOOD_MARKER_COLUMN: "الضمة",
        PHRASAL_FUNCTION_COLUMN: "",
        CASE_MOOD_COLUMN: "مرفوع",
        INVARIABLE_DECLINABLE_COLUMN: "معرب",
    },
    {
        "Sura_No": "1",
        "Verse_No": "2",
        "Word_No": "2",
        "Column5": "1",
        SYNTACTIC_ROLE_COLUMN: "مبتدأ",
        CASE_MOOD_MARKER_COLUMN: "الضمة",
        PHRASAL_FUNCTION_COLUMN: "",
        CASE_MOOD_COLUMN: "مرفوع",
        INVARIABLE_DECLINABLE_COLUMN: "معرب",
    },
    {
        "Sura_No": "1",
        "Verse_No": "2",
        "Word_No": "1",
        "Column5": "2",
        SYNTACTIC_ROLE_COLUMN: "فاعل",
        CASE_MOOD_MARKER_COLUMN: "الواو",
        PHRASAL_FUNCTION_COLUMN: "نائب فاعل",
        CASE_MOOD_COLUMN: "مرفوع",
        INVARIABLE_DECLINABLE_COLUMN: "مبني",
    },
    {
        "Sura_No": "2",
        "Verse_No": "3",
        "Word_No": "1",
        "Column5": "1",
        SYNTACTIC_ROLE_COLUMN: "مفعول به",
        CASE_MOOD_MARKER_COLUMN: "فتحة مقدرة",
        PHRASAL_FUNCTION_COLUMN: "",
        CASE_MOOD_COLUMN: "مرفوع",
        INVARIABLE_DECLINABLE_COLUMN: "معرب",
    },
    {
        "Sura_No": "2",
        "Verse_No": "3",
        "Word_No": "1",
        "Column5": "2",
        SYNTACTIC_ROLE_COLUMN: "",
        CASE_MOOD_MARKER_COLUMN: "",
        PHRASAL_FUNCTION_COLUMN: "",
        CASE_MOOD_COLUMN: "",
        INVARIABLE_DECLINABLE_COLUMN: "",
    },
)
"""خمسةُ صفوفٍ مُصطنَعة: كلمةٌ بمقطعين، وقيمٌ فارغة، وقيمةٌ في عمود التركيب."""


def test_the_registration_is_declared_weaker_than_prior_to_the_number() -> None:
    assert STANDING is RegistrationStanding.FORMULATED_AFTER_THE_NUMBER
    assert "ThisRegistrationIsNotPriorToTheNumber" in (
        IRAB_PREREGISTRATION_NAMED_RESIDUALS
    )
    assert "TheFiguresArrivedFromTheHolderOfTheBytes" in (
        IRAB_PREREGISTRATION_NAMED_RESIDUALS
    )


def test_seven_columns_are_declared_each_with_a_written_limit() -> None:
    assert len(IRAB_COLUMNS) == 7
    for column in IRAB_COLUMNS:
        assert column.what_it_annotates.strip()
        assert column.what_it_does_not_annotate.strip()
    assert column_named(SYNTACTIC_ROLE_COLUMN).arabic_name == "الوظيفةُ النحوية"


def test_an_undeclared_column_is_refused_rather_than_guessed() -> None:
    with pytest.raises(IrabPreregistrationError):
        column_named("Root")


def test_the_two_consignments_carry_their_counting_rules() -> None:
    assert len(FIRST_CONSIGNMENT_IRAB_FIGURES) == 13
    assert len(ARRIVING_IRAB_FIGURES) == (
        len(FIRST_CONSIGNMENT_IRAB_FIGURES) + len(SECOND_CONSIGNMENT_IRAB_FIGURES)
    )
    assert len(figures_for_column(SYNTACTIC_ROLE_COLUMN)) == 11
    assert len(figures_for_column(CASE_MOOD_MARKER_COLUMN)) == 11
    assert len(figures_for_column(PHRASAL_FUNCTION_COLUMN)) == 10
    for figure in ARRIVING_IRAB_FIGURES:
        assert isinstance(figure.counting_rule, IrabCountingRule)
        assert figure.claimed_count >= 0


def test_a_distinct_value_figure_may_not_be_tied_to_one_value() -> None:
    with pytest.raises(IrabPreregistrationError):
        ArrivingIrabFigure(
            label="قيمٌ متمايزةٌ بقيمة",
            column=SYNTACTIC_ROLE_COLUMN,
            value="فاعل",
            claimed_count=66,
            counting_rule=IrabCountingRule.DISTINCT_COLUMN_VALUES,
        )


def test_a_value_figure_without_a_value_cannot_be_constructed() -> None:
    with pytest.raises(IrabPreregistrationError):
        ArrivingIrabFigure(
            label="رقمٌ بلا قيمة",
            column=SYNTACTIC_ROLE_COLUMN,
            value="   ",
            claimed_count=1,
            counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
        )


def test_the_preregistration_digest_is_derived_from_its_content() -> None:
    assert preregistration_digest() == IRAB_PREREGISTRATION_DIGEST
    assert len(IRAB_PREREGISTRATION_DIGEST) == 64


def test_an_empty_value_is_not_counted_as_a_value() -> None:
    counts = value_counts(SYNTHETIC_RECORDS, SYNTACTIC_ROLE_COLUMN)

    assert counts == {"مبتدأ": 2, "فاعل": 1, "مفعول به": 1}
    assert distinct_value_count(SYNTHETIC_RECORDS, SYNTACTIC_ROLE_COLUMN) == 3


def test_segments_and_words_are_two_counts_not_one() -> None:
    """مقطعان في كلمةٍ واحدة: العددان يختلفان، ولا يُقرأ أحدهما مكان الآخر."""

    assert segments_with_value(SYNTHETIC_RECORDS, SYNTACTIC_ROLE_COLUMN, "مبتدأ") == 2
    assert words_with_value(SYNTHETIC_RECORDS, SYNTACTIC_ROLE_COLUMN, "مبتدأ") == 1
    assert "SegmentsAndWordsAreTwoCounts" in IRAB_CENSUS_NAMED_RESIDUALS


def test_a_missing_column_stops_the_count_instead_of_returning_zero() -> None:
    with pytest.raises(IrabCensusError):
        value_counts(SYNTHETIC_RECORDS, "Syntactic_Function")
    with pytest.raises(IrabCensusError):
        value_counts((), SYNTACTIC_ROLE_COLUMN)


def test_an_absent_value_is_not_reported_as_a_zero_count() -> None:
    """الفرقُ بين «ليست من قيم هذا العمود» و«صفر» مُنفَّذٌ لا مُعلَن فقط."""

    absent = ArrivingIrabFigure(
        label="قيمةٌ بصياغةٍ أخرى",
        column=SYNTACTIC_ROLE_COLUMN,
        value="فاعِلٌ",
        claimed_count=0,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    )

    reading = read_figure(SYNTHETIC_RECORDS, absent)

    assert reading.standing is IrabValueStanding.NOT_A_VALUE_OF_THIS_COLUMN
    assert reading.derived_count == 0
    assert not reading.agrees, "غيابُ القيمة ليس موافقةً ولو تساوى العددان"
    assert "AnAbsentValueIsNotAZero" in IRAB_CENSUS_NAMED_RESIDUALS


def test_a_present_value_that_matches_is_marked_as_agreeing() -> None:
    figure = ArrivingIrabFigure(
        label="مبتدأٌ مُصطنَع",
        column=SYNTACTIC_ROLE_COLUMN,
        value="مبتدأ",
        claimed_count=2,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    )

    reading = read_figure(SYNTHETIC_RECORDS, figure)

    assert reading.standing is IrabValueStanding.PRESENT_AND_AGREES
    assert reading.agrees
    assert reading.word_count == 1
    assert reading.preregistration_digest == IRAB_PREREGISTRATION_DIGEST


def test_a_present_value_that_differs_is_shown_not_silently_refreshed() -> None:
    figure = ArrivingIrabFigure(
        label="مبتدأٌ بعددٍ آخر",
        column=SYNTACTIC_ROLE_COLUMN,
        value="مبتدأ",
        claimed_count=99,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    )

    reading = read_figure(SYNTHETIC_RECORDS, figure)

    assert reading.standing is IrabValueStanding.PRESENT_AND_DIFFERS
    assert reading.derived_count == 2
    assert reading.figure.claimed_count == 99


def test_the_column_census_separates_annotated_from_unannotated() -> None:
    census = column_census(SYNTHETIC_RECORDS, CASE_MOOD_MARKER_COLUMN)

    assert census.distinct_values == 3
    assert census.annotated_segments == 4
    assert census.unannotated_segments == 1


def test_the_arriving_figures_do_not_rederive_from_synthetic_rows() -> None:
    """ما خرج من هذه الأسطر رقمٌ عن MASAQ؛ وهو نصُّ `SyntheticLinesAreDeclared`."""

    readings = read_figures(SYNTHETIC_RECORDS)

    assert len(readings) == len(ARRIVING_IRAB_FIGURES)
    assert not any(reading.agrees for reading in readings)


SYNTHETIC_CSV = (
    "Sura_No,Verse_No,Word_No,Column5,"
    f"{SYNTACTIC_ROLE_COLUMN},{CASE_MOOD_MARKER_COLUMN},{PHRASAL_FUNCTION_COLUMN},"
    f"{CASE_MOOD_COLUMN},{INVARIABLE_DECLINABLE_COLUMN}\n"
    "1,2,1,1,مبتدأ,الضمة,,مرفوع,معرب\n"
    "1,2,2,1,مبتدأ,الضمة,,مرفوع,معرب\n"
    "1,2,1,2,فاعل,الواو,نائب فاعل,مرفوع,مبني\n"
)
"""ملفٌّ مُصطنَعٌ بترويسةٍ كاملة؛ يُحاكي بنيةَ الصفّ ولا يحمل رقمًا عن المدوَّنة."""


def test_the_census_reads_a_csv_end_to_end_without_adopting_its_numbers() -> None:
    """أنبوبُ القراءة يعمل على بايتاتٍ تامّةِ الترويسة، والأرقامُ لا تُطابِق."""

    readings = census_from_bytes(SYNTHETIC_CSV.encode("utf-8"))

    assert len(readings) == len(ARRIVING_IRAB_FIGURES)
    assert not any(reading.agrees for reading in readings)


def test_a_csv_without_the_declared_columns_stops_the_census() -> None:
    data = b"Sura_No,Verse_No,Word_No\n1,2,1\n"

    with pytest.raises(IrabCensusError):
        census_from_bytes(data)


@pytest.mark.skipif(
    not os.environ.get(MASAQ_PATH_VARIABLE) and not vendored_masaq_path().is_file(),
    reason=(
        f"the MASAQ bytes are not in {MASAQ_RELATIVE_PATH} and no path is "
        "declared; the thirteen arriving i'rab figures are re-derived only "
        "from the fingerprinted bytes"
    ),
)
def test_the_arriving_figures_are_rederived_from_the_deposited_bytes() -> None:
    """يُعرَض المُدَّعى والمُشتَقّ معًا؛ ولا يُعدَّل رقمٌ ليُطابِق ما قِيس."""

    records = masaq_records(read_masaq_bytes())
    readings = read_figures(records)

    disagreeing = [
        (
            reading.figure.label,
            reading.figure.claimed_count,
            reading.derived_count,
            reading.standing.value,
        )
        for reading in readings
        if not reading.agrees
    ]

    assert disagreeing == [], (
        "أرقامٌ واردةٌ لم تُطابِق ما اشتُقَّ من البايتات المُبصَّمة؛ "
        "والفرقُ يُعرَض ولا يُطوى: " + repr(disagreeing)
    )


TRANSMITTED_LITERAL_SPELLINGS: tuple[tuple[str, str], ...] = (
    (SYNTACTIC_ROLE_COLUMN, "فاعل"),
    (SYNTACTIC_ROLE_COLUMN, "مفعول به"),
    (SYNTACTIC_ROLE_COLUMN, "مضاف إليه"),
    (SYNTACTIC_ROLE_COLUMN, "مبتدأ"),
    (CASE_MOOD_MARKER_COLUMN, "ثبوت النون"),
    (CASE_MOOD_MARKER_COLUMN, "حذف النون"),
    (CASE_MOOD_MARKER_COLUMN, "الياء"),
    (CASE_MOOD_MARKER_COLUMN, "الواو"),
    (CASE_MOOD_MARKER_COLUMN, "ضمة مقدرة"),
    (CASE_MOOD_MARKER_COLUMN, "فتحة مقدرة"),
    (PHRASAL_FUNCTION_COLUMN, "نائب فاعل"),
)
"""الصياغةُ الحرفيّةُ للقيم كما نقلها حائزُ البايتات، منقولةً هنا بلا تطبيع.

وهي **منقولٌ عن ناقل** لا ترويسةٌ قُرِئت؛ فمطابقتُها تُثبِت ما ينصُّ عليه
`ATransmittedSpellingIsNotTheHeader` وحدَه.
"""


def test_the_frozen_value_strings_equal_the_transmitted_spellings() -> None:
    """فحصُ ما يُفحَص قبل وصول البايتات: صورةُ القيمة مقابلَ صورتها المنقولة."""

    frozen = {
        (figure.column, figure.value)
        for figure in FIRST_CONSIGNMENT_IRAB_FIGURES
        if figure.value is not None
    }

    assert set(TRANSMITTED_LITERAL_SPELLINGS) == frozen, (
        "قيمةٌ مُجمَّدةٌ خالفت صياغتَها المنقولة؛ والخلافُ هنا خطأُ نقلٍ "
        "يُصحَّح قبل القياس لا بعده"
    )
    for _, value in TRANSMITTED_LITERAL_SPELLINGS:
        assert value == value.strip()
        assert unicodedata.normalize("NFC", value) == value


def test_the_expectation_is_not_edited_after_the_spelling_arrived() -> None:
    """الفحصُ يُكتَب إلى جانب التوقّع لا مكانَه؛ وتعديلُه يمحو ما كان يُقاس به."""

    assert "SpellingCheckBesideTheExpectation" in SPELLING_CHECK_BESIDE_THE_EXPECTATION
    assert "ATransmittedSpellingIsNotTheHeader" in (
        SPELLING_CHECK_BESIDE_THE_EXPECTATION
    )
    assert "PreRegisteredExpectation" in PRE_REGISTERED_EXPECTATION
    assert "ليست من قيم هذا العمود" in PRE_REGISTERED_EXPECTATION


def test_the_second_consignment_repeats_nothing_from_the_first() -> None:
    """رقمٌ في الدُّفعتين يُوهِم شاهدين؛ والحارسُ يرفضه عند الاستيراد."""

    first = {
        (figure.column, figure.value, figure.counting_rule)
        for figure in FIRST_CONSIGNMENT_IRAB_FIGURES
    }
    second = {
        (figure.column, figure.value, figure.counting_rule)
        for figure in SECOND_CONSIGNMENT_IRAB_FIGURES
    }

    assert first.isdisjoint(second)
    assert len(SECOND_CONSIGNMENT_IRAB_FIGURES) == 36


def test_a_coverage_is_compared_at_its_declared_precision_only() -> None:
    """٨٤٫٤٥٪ منزلتان: تُقارَن بهما، ولا تُقرأ توكيدًا للمنزلة الثالثة."""

    two_places = CoverageReading(
        column=INVARIABLE_DECLINABLE_COLUMN,
        declared_percentage="84.45",
        non_empty_cells=8_445,
        total_records=10_000,
    )
    finer = CoverageReading(
        column=INVARIABLE_DECLINABLE_COLUMN,
        declared_percentage="84.45",
        non_empty_cells=84_452,
        total_records=100_000,
    )

    assert two_places.agrees
    assert finer.agrees, "المنزلةُ الثالثةُ لم تُصرَّح، فلا تُقارَن ولا تُكذِّب"
    assert "ACoverageIsComparedAtItsDeclaredPrecision" in IRAB_CENSUS_NAMED_RESIDUALS
    assert "ACoverageIsNotACount" in IRAB_PREREGISTRATION_NAMED_RESIDUALS


def test_a_coverage_whose_percentage_carries_no_places_is_refused() -> None:
    """نسبةٌ بلا منازلَ تُقارَن بدقّةٍ لم يُصرَّح بها؛ فتُرفَض عند التجميد."""

    with pytest.raises(IrabPreregistrationError):
        ArrivingColumnCoverage(column="Phrase", declared_percentage="2")
    with pytest.raises(IrabPreregistrationError):
        ArrivingColumnCoverage(column="Phrase", declared_percentage="101.00")


def test_coverage_is_read_from_rows_and_a_missing_column_stops_it() -> None:
    """التغطيةُ تُعَدُّ خلايا، والعمودُ الغائبُ يُوقِف العدَّ لا يُصفِّره."""

    coverage = ArrivingColumnCoverage(
        column=CASE_MOOD_COLUMN, declared_percentage="79.13"
    )

    reading = read_coverage(SYNTHETIC_RECORDS, coverage)

    assert reading.non_empty_cells == 4
    assert reading.total_records == 5
    assert non_empty_cells(SYNTHETIC_RECORDS, CASE_MOOD_COLUMN) == 4
    assert not reading.agrees, "٨٠٪ من خمسة صفوفٍ مُصطنَعةٍ ليست تغطيةَ المدوَّنة"
    with pytest.raises(IrabCensusError):
        read_coverage(
            SYNTHETIC_RECORDS,
            ArrivingColumnCoverage(column="Morph_type", declared_percentage="100.0000"),
        )


def test_the_declared_coverages_do_not_rederive_from_synthetic_rows() -> None:
    """أربعةٌ من الأعمدة العشرةِ ليست من الخمسة، فلا تُقرأ من هذه الصفوف أصلًا."""

    assert len(ARRIVING_COLUMN_COVERAGE) == 10
    with pytest.raises(IrabCensusError):
        read_coverages(SYNTHETIC_RECORDS)


def test_the_segment_total_is_counted_not_derived_from_a_percentage() -> None:
    """جملةُ المقاطع تُعَدُّ سجلًّا سجلًّا؛ ولا تُشتَقُّ من نسبةٍ مئويّة."""

    assert ARRIVING_SEGMENT_TOTAL == 157_677
    assert not segment_total_agrees(SYNTHETIC_RECORDS)


@pytest.mark.skipif(
    not os.environ.get(MASAQ_PATH_VARIABLE) and not vendored_masaq_path().is_file(),
    reason=(
        f"the MASAQ bytes are not in {MASAQ_RELATIVE_PATH} and no path is "
        "declared; the ten arriving coverages and the segment total are "
        "re-derived only from the fingerprinted bytes"
    ),
)
def test_the_arriving_coverages_are_rederived_from_the_deposited_bytes() -> None:
    """التغطياتُ العشرُ وجملةُ المقاطع، مقيسةً لا مُدَّعاة."""

    records = masaq_records(read_masaq_bytes())

    assert segment_total_agrees(records), (
        "جملةُ المقاطع خالفت المُدَّعى: " + f"{len(records)} لا {ARRIVING_SEGMENT_TOTAL}"
    )
    disagreeing = [
        (reading.column, reading.declared_percentage, reading.measured_percentage)
        for reading in read_coverages(records)
        if not reading.agrees
    ]

    assert disagreeing == [], "تغطياتٌ واردةٌ لم تُطابِق ما اشتُقَّ من البايتات: " + repr(
        disagreeing
    )
