"""اختباراتُ تجميد أعمدة الإعراب وقياسِها، بأسطرٍ مُصطنَعةٍ مُصرَّحٍ بجنسها.

`SyntheticLinesAreDeclaredNotHidden`: الأسطرُ هنا **مُصطنَعة**، تُحاكي بنيةَ
الصفّ وحدَها؛ ولا يخرج منها رقمٌ عن MASAQ البتّة. والأرقامُ الثلاثةَ عشرَ
الواردةُ لا تُقاس إلّا من البايتات المُبصَّمة، واختبارُها الواحدُ يُفعَّل
حين تكون في `corpora/MASAQ.csv` أو في `ALGHANEM_MASAQ_PATH`.
"""

from __future__ import annotations

import os

import pytest

from alghanem.arabic.irab_column_census import (
    IRAB_CENSUS_NAMED_RESIDUALS,
    IrabCensusError,
    IrabValueStanding,
    census_from_bytes,
    column_census,
    distinct_value_count,
    read_figure,
    read_figures,
    segments_with_value,
    value_counts,
    words_with_value,
)
from alghanem.arabic.irab_column_preregistration import (
    ARRIVING_IRAB_FIGURES,
    CASE_MOOD_MARKER_COLUMN,
    IRAB_COLUMNS,
    IRAB_PREREGISTRATION_DIGEST,
    IRAB_PREREGISTRATION_NAMED_RESIDUALS,
    PHRASAL_FUNCTION_COLUMN,
    STANDING,
    SYNTACTIC_ROLE_COLUMN,
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
    },
    {
        "Sura_No": "1",
        "Verse_No": "2",
        "Word_No": "2",
        "Column5": "1",
        SYNTACTIC_ROLE_COLUMN: "مبتدأ",
        CASE_MOOD_MARKER_COLUMN: "الضمة",
        PHRASAL_FUNCTION_COLUMN: "",
    },
    {
        "Sura_No": "1",
        "Verse_No": "2",
        "Word_No": "1",
        "Column5": "2",
        SYNTACTIC_ROLE_COLUMN: "فاعل",
        CASE_MOOD_MARKER_COLUMN: "الواو",
        PHRASAL_FUNCTION_COLUMN: "نائب فاعل",
    },
    {
        "Sura_No": "2",
        "Verse_No": "3",
        "Word_No": "1",
        "Column5": "1",
        SYNTACTIC_ROLE_COLUMN: "مفعول به",
        CASE_MOOD_MARKER_COLUMN: "فتحة مقدرة",
        PHRASAL_FUNCTION_COLUMN: "",
    },
    {
        "Sura_No": "2",
        "Verse_No": "3",
        "Word_No": "1",
        "Column5": "2",
        SYNTACTIC_ROLE_COLUMN: "",
        CASE_MOOD_MARKER_COLUMN: "",
        PHRASAL_FUNCTION_COLUMN: "",
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


def test_five_columns_are_declared_each_with_a_written_limit() -> None:
    assert len(IRAB_COLUMNS) == 5
    for column in IRAB_COLUMNS:
        assert column.what_it_annotates.strip()
        assert column.what_it_does_not_annotate.strip()
    assert column_named(SYNTACTIC_ROLE_COLUMN).arabic_name == "الوظيفةُ النحوية"


def test_an_undeclared_column_is_refused_rather_than_guessed() -> None:
    with pytest.raises(IrabPreregistrationError):
        column_named("Root")


def test_the_thirteen_arriving_figures_carry_their_counting_rules() -> None:
    assert len(ARRIVING_IRAB_FIGURES) == 13
    assert len(figures_for_column(SYNTACTIC_ROLE_COLUMN)) == 5
    assert len(figures_for_column(CASE_MOOD_MARKER_COLUMN)) == 7
    assert len(figures_for_column(PHRASAL_FUNCTION_COLUMN)) == 1
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

    assert len(readings) == 13
    assert not any(reading.agrees for reading in readings)


SYNTHETIC_CSV = (
    "Sura_No,Verse_No,Word_No,Column5,"
    f"{SYNTACTIC_ROLE_COLUMN},{CASE_MOOD_MARKER_COLUMN},{PHRASAL_FUNCTION_COLUMN}\n"
    "1,2,1,1,مبتدأ,الضمة,\n"
    "1,2,2,1,مبتدأ,الضمة,\n"
    "1,2,1,2,فاعل,الواو,نائب فاعل\n"
)
"""ملفٌّ مُصطنَعٌ بترويسةٍ كاملة؛ يُحاكي بنيةَ الصفّ ولا يحمل رقمًا عن المدوَّنة."""


def test_the_census_reads_a_csv_end_to_end_without_adopting_its_numbers() -> None:
    """أنبوبُ القراءة يعمل على بايتاتٍ تامّةِ الترويسة، والأرقامُ لا تُطابِق."""

    readings = census_from_bytes(SYNTHETIC_CSV.encode("utf-8"))

    assert len(readings) == 13
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
