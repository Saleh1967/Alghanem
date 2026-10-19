"""اختباراتُ حساب همزة الوصل بأثرها وحيادِ الألف محدودًا."""

from __future__ import annotations

import pytest

from alghanem.arabic.position_haraka_bit_account import (
    THE_FIRST_POSITION_TABLE,
    THE_LAST_POSITION_TABLE,
    DepositedTable,
    TableStanding,
)
from alghanem.arabic.wasl_alif_neutrality import (
    THE_ALIF,
    WASL_ALIF_NEUTRALITY_NAMED_RESIDUALS,
    AlifNeutralityBound,
    NeutralityStanding,
    SignatureStanding,
    SukunOnsetReading,
    WaslAlifNeutralityError,
    alif_neutrality_bound,
    assess_shortfall_signature,
    carrier_sukun_share,
    sukun_onset_reading,
)


def test_the_alif_onset_row_is_four_zeros() -> None:
    bound = alif_neutrality_bound()
    assert bound.printed_cells == (0, 0, 0, 0)
    assert bound.printed_occurrences == 0
    assert bound.observed_share == pytest.approx(0.0)


def test_the_zero_is_bounded_and_not_established() -> None:
    bound = alif_neutrality_bound()
    assert bound.standing is NeutralityStanding.ZERO_OBSERVED_AND_BOUNDED
    assert bound.zero_is_established() is False
    assert bound.unaccounted_occurrences == 12139
    assert bound.maximum_share == pytest.approx(15.520041, abs=1e-6)


def test_the_bound_closes_when_the_shortfall_closes() -> None:
    closed = DepositedTable(
        table_name="جدولٌ مُغلَقٌ للاختبار",
        position="موضعٌ للاختبار",
        standing=TableStanding.QUOTED_NOT_REDERIVED,
        rows=((THE_ALIF, (0, 0, 0, 0)), ("ب", (3, 2, 1, 4))),
        stated_grand_total=10,
        stated_column_totals=(3, 2, 1, 4),
    )
    bound = alif_neutrality_bound(closed)
    assert bound.standing is NeutralityStanding.ZERO_OBSERVED_AND_CLOSED
    assert bound.zero_is_established() is True


def test_the_final_position_alif_row_is_seventeen_fathas_only() -> None:
    bound = alif_neutrality_bound(THE_LAST_POSITION_TABLE)
    assert bound.printed_cells == (17, 0, 0, 0)
    assert bound.standing is NeutralityStanding.NOT_ZERO
    assert bound.observed_share == pytest.approx(100.0 * 17 / 78076, abs=1e-9)


def test_a_missing_carrier_is_refused_not_read_as_zero() -> None:
    with pytest.raises(WaslAlifNeutralityError):
        alif_neutrality_bound(THE_FIRST_POSITION_TABLE, "ء")


def test_the_onset_sukun_is_counted_as_the_trace() -> None:
    reading = sukun_onset_reading()
    assert reading.derived_sukun == 10182
    assert reading.stated_sukun == 10339
    assert reading.carriers_with_a_sukun_onset == 27
    assert reading.share_of_printed == pytest.approx(15.409528, abs=1e-6)


def test_the_heaviest_two_onsets_are_lam_and_mim() -> None:
    reading = sukun_onset_reading()
    assert reading.heaviest_carriers == (("ل", 3150), ("م", 2268))
    assert reading.heaviest_total == 5418


def test_the_lam_mim_share_moves_with_its_denominator() -> None:
    reading = sukun_onset_reading()
    assert reading.heaviest_share_on_derived() == pytest.approx(53.211550, abs=1e-6)
    assert reading.heaviest_share_on_stated() == pytest.approx(52.403521, abs=1e-6)
    assert reading.heaviest_share_on_derived() > reading.heaviest_share_on_stated()


def test_the_document_quoted_the_stated_denominator() -> None:
    reading = sukun_onset_reading()
    assert round(reading.heaviest_share_on_stated(), 1) == 52.4
    assert round(reading.heaviest_share_on_derived(), 1) != 52.4


def test_a_non_positive_heaviest_count_is_refused() -> None:
    with pytest.raises(WaslAlifNeutralityError):
        sukun_onset_reading(heaviest=0)


def test_the_shortfall_matches_the_hamza_on_sukun_only() -> None:
    standing, shortfall_share, reference_share = assess_shortfall_signature()
    assert standing is SignatureStanding.CONSISTENT_ON_SUKUN_APART_ELSEWHERE
    assert shortfall_share == pytest.approx(1.293352, abs=1e-6)
    assert reference_share == pytest.approx(1.311806, abs=1e-6)
    assert abs(shortfall_share - reference_share) < 0.02


def test_the_shortfall_sukun_share_is_far_below_the_printed_table() -> None:
    _, shortfall_share, _ = assess_shortfall_signature()
    assert sukun_onset_reading().share_of_printed > 10 * shortfall_share


def test_a_signature_is_refused_when_the_sukun_shares_part() -> None:
    standing, _, _ = assess_shortfall_signature(sukun_tolerance=0.001)
    assert standing is SignatureStanding.APART


def test_a_table_without_a_shortfall_has_no_signature_to_read() -> None:
    with pytest.raises(WaslAlifNeutralityError):
        assess_shortfall_signature(THE_LAST_POSITION_TABLE)


def test_a_share_on_an_empty_row_is_refused() -> None:
    with pytest.raises(WaslAlifNeutralityError):
        carrier_sukun_share((0, 0, 0, 0))


def test_a_bound_on_no_occurrences_is_refused() -> None:
    with pytest.raises(WaslAlifNeutralityError):
        AlifNeutralityBound(
            table_name="لا شيء",
            carrier=THE_ALIF,
            printed_occurrences=0,
            printed_cells=(0, 0, 0, 0),
            counted_occurrences=0,
            unaccounted_occurrences=0,
            standing=NeutralityStanding.ZERO_OBSERVED_AND_CLOSED,
        )


def test_a_reading_with_no_sukun_trace_is_refused() -> None:
    with pytest.raises(WaslAlifNeutralityError):
        SukunOnsetReading(
            table_name="لا أثر",
            derived_sukun=0,
            stated_sukun=10,
            printed_occurrences=10,
            carriers_with_a_sukun_onset=0,
            heaviest_carriers=(),
        )


def test_a_stated_denominator_of_zero_is_refused_not_divided_by() -> None:
    reading = SukunOnsetReading(
        table_name="بلا مقامٍ مُعلَن",
        derived_sukun=4,
        stated_sukun=0,
        printed_occurrences=8,
        carriers_with_a_sukun_onset=1,
        heaviest_carriers=(("ل", 4),),
    )
    with pytest.raises(WaslAlifNeutralityError):
        reading.heaviest_share_on_stated()


def test_every_named_residual_begins_with_its_own_key() -> None:
    assert WASL_ALIF_NEUTRALITY_NAMED_RESIDUALS
    for key, text in WASL_ALIF_NEUTRALITY_NAMED_RESIDUALS.items():
        assert text.startswith(f"{key}: ")


def test_the_named_residuals_keep_the_two_scopes_apart() -> None:
    joined = " ".join(WASL_ALIF_NEUTRALITY_NAMED_RESIDUALS.values())
    assert "alif_neutrality" in joined
    assert "66,076" in joined
    assert "imperative_wasla_census" in joined
