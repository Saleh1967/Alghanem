"""اختباراتُ علاج السكون المُضمَر: يُفصَل بمصدره ولا يُجمَع في رقمٍ واحد."""

from __future__ import annotations

import pytest

from alghanem.arabic.encoding.carrier_state_candidate import (
    CarrierState,
    CarrierStateCodec,
    CarrierStateUnit,
)
from alghanem.arabic.fatiha_source_text import FATIHA_LINES
from alghanem.arabic.implicit_sukun_treatment import (
    IMPLICIT_SUKUN_NAMED_RESIDUALS,
    THE_ALIF,
    ImplicitSukunError,
    SukunCensus,
    SukunSource,
    VisibilityStanding,
    census_over,
    measured_onset_census,
    measured_text_census,
    onset_census_over,
    source_of,
    words_of,
)

_CODEC = CarrierStateCodec()


def test_most_of_the_sukun_is_written_nowhere() -> None:
    census = measured_text_census()
    assert census.total == 75
    assert census.written == 21
    assert census.unwritten == 54
    assert census.written_share == pytest.approx(28.0, abs=1e-9)
    assert census.standing is VisibilityStanding.MOSTLY_UNWRITTEN


def test_the_implicit_sukun_splits_into_three_named_causes() -> None:
    census = measured_text_census()
    assert census.count_of(SukunSource.ALIF_WITHOUT_A_MARK) == 23
    assert census.count_of(SukunSource.GEMINATION_PAIR_START) == 14
    assert census.count_of(SukunSource.BARE_CARRIER) == 17
    assert (
        census.count_of(SukunSource.ALIF_WITHOUT_A_MARK)
        + census.count_of(SukunSource.GEMINATION_PAIR_START)
        + census.count_of(SukunSource.BARE_CARRIER)
        == census.unwritten
    )


def test_a_quarter_of_the_implicit_sukun_is_half_a_geminate() -> None:
    census = measured_text_census()
    assert census.share_of_unwritten(
        SukunSource.GEMINATION_PAIR_START
    ) == pytest.approx(25.925926, abs=1e-6)


def test_every_alif_in_the_fatiha_holds_an_unmarked_sukun() -> None:
    held = {
        unit.state
        for word in words_of()
        for unit in _CODEC.generate(word)
        if unit.carrier == THE_ALIF and unit.seat is None
    }
    assert held == {CarrierState.SUKUN_IMPLICIT, CarrierState.DAGGER}
    assert CarrierState.SUKUN_EXPLICIT not in held
    assert CarrierState.FATHA not in held


def test_the_onset_sukun_is_two_thirds_unwritten() -> None:
    onset = measured_onset_census()
    assert onset.total == 14
    assert onset.written == 5
    assert onset.written_share == pytest.approx(35.714286, abs=1e-6)
    assert onset.standing is VisibilityStanding.MOSTLY_UNWRITTEN


def test_no_alif_survives_the_onset_neutralisation() -> None:
    onset = measured_onset_census()
    assert onset.count_of(SukunSource.ALIF_WITHOUT_A_MARK) == 0
    assert onset.count_of(SukunSource.BARE_CARRIER) == 8
    assert onset.count_of(SukunSource.GEMINATION_PAIR_START) == 1


def test_the_split_is_the_output_and_names_every_source() -> None:
    split = measured_text_census().split()
    assert len(split) == len(SukunSource)
    assert [name for name, _ in split] == [source.value for source in SukunSource]
    assert sum(count for _, count in split) == measured_text_census().total


def test_a_fully_written_source_is_named_as_such() -> None:
    census = census_over(["بِسْمِ"], scope="كلمةٌ واحدة")
    assert census.standing is VisibilityStanding.FULLY_WRITTEN
    assert census.unwritten == 0
    assert census.written_share == pytest.approx(100.0)


def test_the_unwritten_share_of_a_written_source_is_refused() -> None:
    with pytest.raises(ImplicitSukunError):
        measured_text_census().share_of_unwritten(SukunSource.EXPLICIT_MARK)


def test_the_unwritten_share_over_nothing_unwritten_is_refused() -> None:
    census = census_over(["بِسْمِ"], scope="كلمةٌ واحدة")
    with pytest.raises(ImplicitSukunError):
        census.share_of_unwritten(SukunSource.BARE_CARRIER)


def test_only_the_explicit_mark_is_read_from_bytes() -> None:
    written = [source for source in SukunSource if source.is_written]
    assert written == [SukunSource.EXPLICIT_MARK]


def test_a_vowelled_unit_has_no_sukun_source_to_name() -> None:
    unit = CarrierStateUnit("\u0628", CarrierState.FATHA)
    with pytest.raises(ImplicitSukunError):
        source_of(unit)


def test_a_gemination_half_is_sourced_before_its_carrier() -> None:
    units = _CODEC.generate("\u0627\u0644\u0644\u0651\u064e\u0647\u0650")
    halves = [unit for unit in units if unit.gemination is not None]
    assert halves
    assert source_of(halves[0]) is SukunSource.GEMINATION_PAIR_START


def test_an_empty_text_is_refused_not_counted_as_zero() -> None:
    with pytest.raises(ImplicitSukunError):
        census_over([])
    with pytest.raises(ImplicitSukunError):
        onset_census_over(["   "])


def test_a_census_with_a_repeated_source_is_refused() -> None:
    with pytest.raises(ImplicitSukunError):
        SukunCensus(
            scope="مكرَّر",
            words=1,
            by_source=(
                (SukunSource.BARE_CARRIER, 1),
                (SukunSource.BARE_CARRIER, 2),
            ),
        )


def test_a_census_over_no_words_is_refused() -> None:
    with pytest.raises(ImplicitSukunError):
        SukunCensus(scope="لا كلمات", words=0, by_source=())


def test_a_negative_count_is_refused() -> None:
    with pytest.raises(ImplicitSukunError):
        SukunCensus(
            scope="سالب",
            words=1,
            by_source=((SukunSource.BARE_CARRIER, -1),),
        )


def test_the_words_are_read_from_the_deposited_lines() -> None:
    assert words_of() == words_of(FATIHA_LINES)
    assert len(words_of()) == 29


def test_every_named_residual_begins_with_its_own_key() -> None:
    assert IMPLICIT_SUKUN_NAMED_RESIDUALS
    for key, text in IMPLICIT_SUKUN_NAMED_RESIDUALS.items():
        assert text.startswith(f"{key}: ")


def test_the_residuals_bind_the_split_to_the_deposited_onset_column() -> None:
    joined = " ".join(IMPLICIT_SUKUN_NAMED_RESIDUALS.values())
    assert "position_haraka_bit_account" in joined
    assert "10,182" in joined
    assert "alif_neutrality" in joined
