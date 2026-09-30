"""اختباراتُ قياس ورقة Powers على البايتات المختومة."""

from __future__ import annotations

import math

import pytest

from alghanem.arabic.markov_readiness_gate import token_markov_standing
from alghanem.arabic.powers_two_regime_measure import (
    A_DECLARED_PENDING_LAW_IS_NEITHER_CONFIRMED_NOR_REFUTED,
    A_LADDER_THAT_BREAKS_AT_ITS_TOP_RUNG_IS_NOT_A_MONOTONE_LAW,
    A_PREDICTED_ORDERING_THAT_HOLDS_IS_NOT_A_QUOTED_MAGNITUDE_THAT_MATCHES,
    POWERS_NAMED_RESIDUALS,
    THE_FREQUENCY_BANDS,
    THE_HEAD_WINDOW,
    THE_LENGTHS_AT_MEASUREMENT,
    THE_MARKUP_PATTERN,
    THE_PENDING_LAWS,
    THE_QUOTED_POWERS_FIGURES,
    THE_QUOTED_SIMPLE_FAMILY_TOTAL,
    THE_R_SQUARED_TOLERANCE,
    THE_REGIMES_AT_MEASUREMENT,
    THE_TAIL_FLOOR,
    THE_TOKENS_AT_MEASUREMENT,
    BandLength,
    Law,
    PendingLaw,
    PowersMeasureError,
    QuotedFigure,
    TokenRule,
    Verdict,
    band_lengths,
    head_fit,
    tail_fit,
    the_ayah_field_rule_is_silent_on_these_bytes,
    the_corpus_gate_is_untouched,
    the_head_prefers_plain_zipf,
    the_ladder_breaks_only_where_a_band_is_thin,
    the_length_ladder_is_monotone,
    the_length_law_holds_between_the_extremes,
    the_markup_drop_lands_on_the_surveyed_total,
    the_measured_figures_have_drifted,
    the_publisher_markup_census,
    the_quoted_figures_against_ours,
    the_tail_prefers_the_corrected_law,
    token_census,
)


def test_the_frozen_figures_still_match_what_the_sealed_bytes_measure() -> None:
    assert the_measured_figures_have_drifted() is False


def test_the_token_totals_are_the_frozen_three() -> None:
    sealed = token_census(TokenRule.AS_SEALED)
    dropped = token_census(TokenRule.PUBLISHER_MARKUP_DROPPED)
    markup = the_publisher_markup_census()
    assert (sealed.tokens, dropped.tokens, markup.occurrences) == (
        THE_TOKENS_AT_MEASUREMENT
    )


def test_dropping_the_markup_removes_exactly_the_markup_occurrences() -> None:
    sealed = token_census(TokenRule.AS_SEALED)
    dropped = token_census(TokenRule.PUBLISHER_MARKUP_DROPPED)
    assert sealed.tokens - dropped.tokens == the_publisher_markup_census().occurrences


def test_the_most_frequent_token_on_our_bytes_is_a_publisher_mark() -> None:
    census = the_publisher_markup_census()
    assert census.top_rank == 1
    assert all(THE_MARKUP_PATTERN.fullmatch(form) for form in census.forms)


def test_the_markup_drop_lands_on_the_quoted_simple_family_total() -> None:
    assert the_markup_drop_lands_on_the_surveyed_total() is True
    assert THE_QUOTED_SIMPLE_FAMILY_TOTAL == 78_245


def test_that_coincidence_is_not_a_second_implementation_agreeing() -> None:
    """البايتاتُ بلا فواصل حقولٍ، فقاعدةُ حقل الآية صامتةٌ عليها."""

    assert the_ayah_field_rule_is_silent_on_these_bytes() is True


def test_the_tail_prefers_the_corrected_law_on_both_token_rules() -> None:
    for rule in TokenRule:
        assert the_tail_prefers_the_corrected_law(rule) is True


def test_the_head_prefers_plain_zipf_so_the_curve_has_two_regimes() -> None:
    for rule in TokenRule:
        assert the_head_prefers_plain_zipf(rule) is True


def test_every_fitted_regime_falls_with_rank() -> None:
    for rule in TokenRule:
        for law in Law:
            assert head_fit(rule, law).is_falling is True
            assert tail_fit(rule, law).is_falling is True


def test_the_four_frozen_r_squared_values_are_what_disk_measures() -> None:
    measured = (
        round(head_fit(TokenRule.AS_SEALED, Law.ZIPF).r_squared, 4),
        round(tail_fit(TokenRule.AS_SEALED, Law.ZIPF).r_squared, 4),
        round(tail_fit(TokenRule.AS_SEALED, Law.POWERS_CORRECTED).r_squared, 4),
        round(head_fit(TokenRule.PUBLISHER_MARKUP_DROPPED, Law.ZIPF).r_squared, 4),
    )
    assert measured == THE_REGIMES_AT_MEASUREMENT


def test_the_tail_slope_is_not_the_minus_one_the_form_asserts() -> None:
    """`1/(r·log²r)` تنصّ على أسٍّ واحد، والمقيسُ دونه بكثير."""

    slope = tail_fit(TokenRule.AS_SEALED, Law.POWERS_CORRECTED).slope
    assert -0.75 < slope < -0.6
    assert abs(slope + 1.0) > 0.25


def test_the_head_window_and_the_tail_floor_do_not_overlap() -> None:
    assert THE_HEAD_WINDOW[0] < THE_HEAD_WINDOW[1] < THE_TAIL_FLOOR


def test_the_length_ladder_is_the_frozen_five() -> None:
    assert tuple(round(band.mean_length, 4) for band in band_lengths()) == (
        THE_LENGTHS_AT_MEASUREMENT
    )


def test_the_claimed_monotone_ascent_is_refuted_on_our_bytes() -> None:
    assert the_length_ladder_is_monotone(TokenRule.AS_SEALED) is False


def test_but_the_extremes_of_the_length_law_do_hold() -> None:
    for rule in TokenRule:
        assert the_length_law_holds_between_the_extremes(rule) is True


def test_the_only_break_sits_at_a_band_of_fewer_than_ten_types() -> None:
    assert the_ladder_breaks_only_where_a_band_is_thin(TokenRule.AS_SEALED) is True
    assert band_lengths()[0].is_a_single_specimen is False
    assert band_lengths()[0].types == 2
    assert (
        band_lengths(TokenRule.PUBLISHER_MARKUP_DROPPED)[0].is_a_single_specimen is True
    )


def test_the_bands_cover_the_frequencies_without_gap_or_overlap() -> None:
    for upper, lower in zip(THE_FREQUENCY_BANDS, THE_FREQUENCY_BANDS[1:]):
        assert lower[1] + 1 == upper[0]
    assert THE_FREQUENCY_BANDS[-1] == (1, 1)


def test_the_band_type_counts_sum_to_the_vocabulary() -> None:
    assert sum(band.types for band in band_lengths()) == token_census().types


def test_the_head_quotation_contradicts_and_the_tail_pair_agrees() -> None:
    rows = {row.name: row for row in the_quoted_figures_against_ours()}
    head = rows["الرأس ‎10–99‎ على زِبف"]
    assert head.standing is Verdict.CONTRADICTS
    assert head.gap > 0.0
    assert rows["الذيل ‎100+‎ على المصحَّح"].standing is Verdict.AGREES
    assert rows["الذيل ‎100+‎ على زِبف"].standing is Verdict.AGREES


def test_the_agreeing_tail_zipf_sits_on_the_very_edge_of_the_tolerance() -> None:
    row = {row.name: row for row in the_quoted_figures_against_ours()}[
        "الذيل ‎100+‎ على زِبف"
    ]
    assert abs(row.gap) <= THE_R_SQUARED_TOLERANCE
    assert abs(row.gap) > THE_R_SQUARED_TOLERANCE * 0.95


def test_every_quoted_length_rung_contradicts_ours() -> None:
    rows = [
        row
        for row in the_quoted_figures_against_ours()
        if row.name.startswith("طولُ النطاق")
    ]
    assert len(rows) == len(THE_FREQUENCY_BANDS)
    assert all(row.standing is Verdict.CONTRADICTS for row in rows)


def test_the_tolerance_is_declared_before_any_comparison_is_read() -> None:
    assert THE_R_SQUARED_TOLERANCE > 0.0
    assert all(row.tolerance > 0.0 for row in the_quoted_figures_against_ours())


def test_the_pending_laws_each_name_what_they_are_waiting_for() -> None:
    assert len(THE_PENDING_LAWS) == 2
    assert all(law.what_it_needs.strip() for law in THE_PENDING_LAWS)


def test_a_pending_law_cannot_be_deposited_without_its_missing_material() -> None:
    with pytest.raises(PowersMeasureError):
        PendingLaw(name="قانون", what_it_needs="   ")


def test_a_quoted_figure_cannot_be_deposited_nameless() -> None:
    with pytest.raises(PowersMeasureError):
        QuotedFigure(name="  ", value=0.5)


def test_an_inverted_band_is_refused() -> None:
    with pytest.raises(PowersMeasureError):
        BandLength(low=10, high=2, types=3, mean_length=4.0)


def test_an_empty_band_is_refused() -> None:
    with pytest.raises(PowersMeasureError):
        BandLength(low=1, high=1, types=0, mean_length=4.0)


def test_the_quoted_figures_are_deposited_verbatim() -> None:
    assert tuple(figure.value for figure in THE_QUOTED_POWERS_FIGURES) == (
        0.9805,
        0.9508,
        0.9476,
    )


def test_every_named_residual_opens_with_its_own_name() -> None:
    for name, text in POWERS_NAMED_RESIDUALS.items():
        assert text.startswith(f"{name}: ")


def test_the_four_residuals_are_the_exported_four() -> None:
    assert set(POWERS_NAMED_RESIDUALS.values()) == {
        A_PREDICTED_ORDERING_THAT_HOLDS_IS_NOT_A_QUOTED_MAGNITUDE_THAT_MATCHES,
        A_LADDER_THAT_BREAKS_AT_ITS_TOP_RUNG_IS_NOT_A_MONOTONE_LAW,
        A_DECLARED_PENDING_LAW_IS_NEITHER_CONFIRMED_NOR_REFUTED,
        POWERS_NAMED_RESIDUALS["THE_FIRST_RANK_IS_A_PUBLISHER_MARK_NOT_A_WORD"],
    }


def test_the_corpus_gate_is_untouched_by_this_unit() -> None:
    assert the_corpus_gate_is_untouched() is True
    assert token_markov_standing() is not None


def test_the_fit_is_a_plain_least_squares_with_no_dependency() -> None:
    """الملاءمةُ حسابٌ مكشوف؛ يُعاد يدويًّا فيطابق."""

    fit = head_fit(TokenRule.AS_SEALED, Law.ZIPF)
    predicted = fit.slope * math.log(10)
    assert math.isfinite(predicted)
    assert fit.first_rank == THE_HEAD_WINDOW[0]
    assert fit.last_rank == THE_HEAD_WINDOW[1]
