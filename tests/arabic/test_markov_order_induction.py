"""اختباراتُ مربّع الاستقراء في رتبة ماركوف."""

from __future__ import annotations

import math

import pytest

from alghanem.arabic.markov_order_induction import (
    A_CONDITION_FIXED_AFTER_A_PROBE_IS_NOT_A_PREDICTION,
    MARKOV_ORDER_INDUCTION_NAMED_RESIDUALS,
    MEASURING_MARKOV_ON_THE_ROOT_TABLE_DOES_NOT_OPEN_THE_CORPUS_GATE,
    THE_DECLARED_SMOOTHINGS,
    THE_LADDER_ORDER,
    THE_PREREGISTERED_COMMUTATION_CONDITION,
    THE_REQUIRED_AGREEMENT_SHARE,
    THE_REQUIRED_DRAW_FLOOR,
    CommutationReading,
    CommutationStanding,
    CrossoverRow,
    InductionDirection,
    LadderRung,
    MarkovOrderInductionError,
    SplitReading,
    degrees_of_freedom,
    fit_rung,
    held_out_winner,
    information_criterion,
    log_likelihood,
    measure_commutation,
    place_alphabet,
    place_sequences,
    rung_crossover_scan,
    rung_index,
    select_rung,
    the_corpus_gate_is_untouched,
    verify_the_ladder_is_strictly_nested,
    verify_the_triangle_fit_reproduces_every_margin,
)

# --- المادّة ---------------------------------------------------------------


def test_the_material_is_the_algebra_substrate_read_as_places() -> None:
    sequences = place_sequences()
    assert len(sequences) == 4559
    assert all(len(row) == 3 for row in sequences)
    assert set(place_alphabet()) == {place for row in sequences for place in row}
    assert len(place_alphabet()) == 11


def test_the_alphabet_is_sorted_and_stable_across_calls() -> None:
    first = place_alphabet()
    assert list(first) == sorted(first)
    assert first is place_alphabet()


# --- السلّمُ ودرجاتُ الحرّيّة ------------------------------------------------


def test_the_ladder_is_declared_in_one_order_and_nowhere_else() -> None:
    assert THE_LADDER_ORDER == (
        LadderRung.INDEPENDENT,
        LadderRung.CHAIN,
        LadderRung.TRIANGLE,
        LadderRung.SATURATED,
    )
    assert set(THE_LADDER_ORDER) == set(LadderRung)
    assert [rung_index(rung) for rung in THE_LADDER_ORDER] == [0, 1, 2, 3]


def test_the_degrees_of_freedom_are_computed_not_transcribed() -> None:
    assert [degrees_of_freedom(rung, 11) for rung in THE_LADDER_ORDER] == [
        30,
        230,
        330,
        1330,
    ]
    for width in (2, 3, 5, 11):
        freedoms = [degrees_of_freedom(rung, width) for rung in THE_LADDER_ORDER]
        assert freedoms == sorted(freedoms)
        assert len(set(freedoms)) == len(freedoms)


def test_an_alphabet_below_two_letters_is_refused() -> None:
    with pytest.raises(MarkovOrderInductionError):
        degrees_of_freedom(LadderRung.CHAIN, 1)


def test_the_ladder_nesting_theorem_is_checked_and_not_described() -> None:
    assert verify_the_ladder_is_strictly_nested() is True


def test_the_triangle_fit_reproduces_all_three_margins() -> None:
    assert verify_the_triangle_fit_reproduces_every_margin() is True


def test_every_rung_conserves_the_total_mass_of_the_table() -> None:
    sample = place_sequences()
    for rung in THE_LADDER_ORDER:
        assert math.isclose(
            math.fsum(fit_rung(rung, sample)), float(len(sample)), rel_tol=1e-9
        )


def test_the_likelihood_does_not_fall_as_the_ladder_widens() -> None:
    sample = place_sequences()
    readings = [
        log_likelihood(sample, fit_rung(rung, sample)) for rung in THE_LADDER_ORDER
    ]
    assert readings == sorted(readings)


def test_the_saturated_rung_reproduces_the_table_exactly() -> None:
    sample = place_sequences()
    fitted = fit_rung(LadderRung.SATURATED, sample)
    assert sum(1 for cell in fitted if cell > 0.0) == 776


def test_an_empty_sample_is_refused_rather_than_fitted() -> None:
    with pytest.raises(MarkovOrderInductionError):
        fit_rung(LadderRung.CHAIN, [])


def test_a_place_outside_the_alphabet_is_refused_not_counted_silently() -> None:
    with pytest.raises(MarkovOrderInductionError):
        fit_rung(LadderRung.CHAIN, [("شفويّ", "شفويّ", "مخرجٌ موهوم")])


# --- المعيارُ والاختيار ----------------------------------------------------


def test_the_criterion_penalises_freedom_and_ranks_the_saturated_last() -> None:
    sample = place_sequences()
    readings = {rung: information_criterion(rung, sample) for rung in THE_LADDER_ORDER}
    assert readings[LadderRung.SATURATED] == max(readings.values())
    assert readings[LadderRung.CHAIN] == min(readings.values())


def test_the_rung_on_the_whole_is_the_chain() -> None:
    assert select_rung(place_sequences()) is LadderRung.CHAIN


def test_the_held_out_winner_is_the_triangle_at_both_declared_smoothings() -> None:
    sample = place_sequences()
    seen = sample[::2]
    hidden = sample[1::2]
    winners = {
        smoothing: held_out_winner(seen, hidden, smoothing)
        for smoothing in THE_DECLARED_SMOOTHINGS
    }
    assert set(winners.values()) == {LadderRung.TRIANGLE}


def test_a_non_positive_smoothing_is_refused() -> None:
    sample = place_sequences()
    with pytest.raises(MarkovOrderInductionError):
        held_out_winner(sample[::2], sample[1::2], 0.0)


# --- المربّع ---------------------------------------------------------------


def test_the_square_does_not_commute_on_this_source() -> None:
    reading = measure_commutation(draws=THE_REQUIRED_DRAW_FLOOR)
    assert reading.standing is CommutationStanding.DOES_NOT_COMMUTE
    ends = reading.rung_by_direction()
    assert ends[InductionDirection.ON_THEN_FOR] is LadderRung.CHAIN
    assert ends[InductionDirection.FOR_THEN_ON] is LadderRung.INDEPENDENT
    assert reading.agreement_share == 0.0
    assert reading.held_out_rung is LadderRung.TRIANGLE


def test_the_three_routes_land_on_three_different_rungs() -> None:
    reading = measure_commutation(draws=THE_REQUIRED_DRAW_FLOOR)
    landed = {
        reading.rung_on_the_whole,
        reading.modal_rung_inside_the_seen,
        reading.held_out_rung,
    }
    assert len(landed) == 3


def test_a_reading_below_the_draw_floor_is_unreadable_not_a_verdict() -> None:
    reading = measure_commutation(draws=THE_REQUIRED_DRAW_FLOOR - 1)
    assert len(reading.splits) < THE_REQUIRED_DRAW_FLOOR
    assert reading.standing is CommutationStanding.UNREADABLE


def test_disagreeing_smoothings_make_the_reading_unreadable() -> None:
    split = SplitReading(
        seen_count=10,
        hidden_count=10,
        rung_inside_the_seen=LadderRung.CHAIN,
        winners_by_smoothing=(
            (THE_DECLARED_SMOOTHINGS[0], LadderRung.CHAIN),
            (THE_DECLARED_SMOOTHINGS[1], LadderRung.TRIANGLE),
        ),
    )
    assert split.smoothings_agree is False
    assert split.held_out_winner is None
    reading = CommutationReading(
        rung_on_the_whole=LadderRung.CHAIN,
        splits=(split,) * THE_REQUIRED_DRAW_FLOOR,
    )
    assert reading.standing is CommutationStanding.UNREADABLE


def test_a_square_that_agrees_everywhere_closes() -> None:
    agreeing = SplitReading(
        seen_count=10,
        hidden_count=10,
        rung_inside_the_seen=LadderRung.CHAIN,
        winners_by_smoothing=tuple(
            (smoothing, LadderRung.CHAIN) for smoothing in THE_DECLARED_SMOOTHINGS
        ),
    )
    reading = CommutationReading(
        rung_on_the_whole=LadderRung.CHAIN,
        splits=(agreeing,) * THE_REQUIRED_DRAW_FLOOR,
    )
    assert reading.agreement_share == 1.0
    assert reading.standing is CommutationStanding.COMMUTES_ON_THIS_SOURCE


def test_agreement_just_below_the_declared_share_does_not_close() -> None:
    agreeing = SplitReading(
        seen_count=10,
        hidden_count=10,
        rung_inside_the_seen=LadderRung.CHAIN,
        winners_by_smoothing=tuple(
            (smoothing, LadderRung.CHAIN) for smoothing in THE_DECLARED_SMOOTHINGS
        ),
    )
    straying = SplitReading(
        seen_count=10,
        hidden_count=10,
        rung_inside_the_seen=LadderRung.INDEPENDENT,
        winners_by_smoothing=tuple(
            (smoothing, LadderRung.CHAIN) for smoothing in THE_DECLARED_SMOOTHINGS
        ),
    )
    splits = (agreeing,) * 37 + (straying,) * 3
    reading = CommutationReading(rung_on_the_whole=LadderRung.CHAIN, splits=splits)
    assert reading.agreement_share < THE_REQUIRED_AGREEMENT_SHARE
    assert reading.modal_rung_inside_the_seen is LadderRung.CHAIN
    assert reading.standing is CommutationStanding.DOES_NOT_COMMUTE


def test_a_split_with_an_empty_side_is_refused() -> None:
    with pytest.raises(MarkovOrderInductionError):
        SplitReading(
            seen_count=0,
            hidden_count=10,
            rung_inside_the_seen=LadderRung.CHAIN,
            winners_by_smoothing=tuple(
                (smoothing, LadderRung.CHAIN) for smoothing in THE_DECLARED_SMOOTHINGS
            ),
        )


def test_a_winner_count_that_misses_a_smoothing_is_refused() -> None:
    with pytest.raises(MarkovOrderInductionError):
        SplitReading(
            seen_count=10,
            hidden_count=10,
            rung_inside_the_seen=LadderRung.CHAIN,
            winners_by_smoothing=((THE_DECLARED_SMOOTHINGS[0], LadderRung.CHAIN),),
        )


def test_a_reading_without_a_written_condition_is_refused() -> None:
    with pytest.raises(MarkovOrderInductionError):
        CommutationReading(
            rung_on_the_whole=LadderRung.CHAIN, splits=(), condition="   "
        )


def test_a_degenerate_split_share_is_refused() -> None:
    with pytest.raises(MarkovOrderInductionError):
        measure_commutation(draws=2, seen_share=1.0)
    with pytest.raises(MarkovOrderInductionError):
        measure_commutation(draws=0)


def test_the_measurement_is_reproducible_under_its_declared_seed() -> None:
    first = measure_commutation(draws=THE_REQUIRED_DRAW_FLOOR, seed=11)
    second = measure_commutation(draws=THE_REQUIRED_DRAW_FLOOR, seed=11)
    assert [split.rung_inside_the_seen for split in first.splits] == [
        split.rung_inside_the_seen for split in second.splits
    ]


# --- مسحُ العتبة -----------------------------------------------------------


def test_the_crossover_scan_shows_the_rung_moving_with_the_sample_size() -> None:
    rows = rung_crossover_scan()
    assert rows[0].rungs[0] is LadderRung.INDEPENDENT
    assert rows[-1].rungs[0] is LadderRung.CHAIN
    assert [row.seen_count for row in rows] == sorted(row.seen_count for row in rows)
    assert any(not row.is_unanimous for row in rows)


def test_the_scan_refuses_a_share_that_leaves_nothing_to_fit() -> None:
    with pytest.raises(MarkovOrderInductionError):
        rung_crossover_scan(shares=(0.0,))
    with pytest.raises(MarkovOrderInductionError):
        rung_crossover_scan(shares=(1e-6,))


def test_a_scan_row_without_a_single_choice_is_refused() -> None:
    with pytest.raises(MarkovOrderInductionError):
        CrossoverRow(seen_count=10, rungs=())


# --- البقايا والبوّابة ------------------------------------------------------


def test_every_named_residual_is_registered_under_its_own_name() -> None:
    assert len(MARKOV_ORDER_INDUCTION_NAMED_RESIDUALS) == 6
    for name, text in MARKOV_ORDER_INDUCTION_NAMED_RESIDUALS.items():
        assert text.startswith(f"{name}: ")


def test_the_condition_confesses_that_a_probe_came_first() -> None:
    assert "قبل جولتها المسجَّلة" in THE_PREREGISTERED_COMMUTATION_CONDITION
    assert "تنبّؤٌ مُودَع" in A_CONDITION_FIXED_AFTER_A_PROBE_IS_NOT_A_PREDICTION


def test_the_condition_names_its_three_clauses_and_its_guard() -> None:
    assert f"{THE_REQUIRED_AGREEMENT_SHARE:.2f}" in (
        THE_PREREGISTERED_COMMUTATION_CONDITION
    )
    assert str(THE_REQUIRED_DRAW_FLOOR) in THE_PREREGISTERED_COMMUTATION_CONDITION
    assert "UNREADABLE" in THE_PREREGISTERED_COMMUTATION_CONDITION


def test_measuring_here_leaves_the_corpus_gate_blocked() -> None:
    assert the_corpus_gate_is_untouched() is True
    measure_commutation(draws=THE_REQUIRED_DRAW_FLOOR)
    assert the_corpus_gate_is_untouched() is True
    assert "المدوّنة" in MEASURING_MARKOV_ON_THE_ROOT_TABLE_DOES_NOT_OPEN_THE_CORPUS_GATE
