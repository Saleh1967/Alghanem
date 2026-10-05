"""شواهدُ البند المتوقَّع: المعيارُ يسبق الرقم، والمرآةُ لا تُقرأ فصلًا."""

from __future__ import annotations

import pytest

from alghanem.arabic.lexicon_bridge import (
    THE_TWENTY_MATERIALS,
    THE_WITHHELD_LEXICON,
    EntryStage,
    entry_leg_census,
    material_readings,
)
from alghanem.arabic.lexicon_dispersion_expectation import (
    SCALE,
    THE_LOCKED_SCALED_DISPERSIONS,
    THE_MATCHING_STAGE,
    THE_MIRRORED_LEXICON,
    DispersionExpectationError,
    DispersionMeasure,
    MirrorStanding,
    dispersion_of,
    dispersion_verdicts,
    leave_one_out_flips,
    locked_dispersions_have_drifted,
    mirror_rows,
)


def test_the_measure_is_required_and_never_chosen_for_the_reader() -> None:
    with pytest.raises(DispersionExpectationError):
        dispersion_of("معامِلُ الاختلاف", (1, 2, 3))  # type: ignore[arg-type]


def test_a_series_without_two_rows_or_with_a_zero_sum_yields_no_dispersion() -> None:
    for values in ((5,), (0, 0, 0)):
        with pytest.raises(DispersionExpectationError):
            dispersion_of(DispersionMeasure.GINI, values)


def test_every_named_measure_actually_computes_and_none_is_a_label_only() -> None:
    values = (1, 2, 3, 10)
    for measure in DispersionMeasure:
        assert dispersion_of(measure, values) > 0


def test_a_flat_series_disperses_at_zero_under_all_three_measures() -> None:
    flat = (7, 7, 7, 7)
    for measure in DispersionMeasure:
        assert dispersion_of(measure, flat) == 0


def test_the_mirror_measures_nineteen_materials_and_not_the_closed_twenty() -> None:
    rows = mirror_rows()
    assert len(rows) == 19
    assert len(rows) < len(THE_TWENTY_MATERIALS)


def test_the_material_absent_here_is_the_one_measured_absent_upstream() -> None:
    present = {row.material for row in mirror_rows()}
    absent = set(THE_TWENTY_MATERIALS) - present
    assert absent == set(entry_leg_census(THE_MATCHING_STAGE).absent)


def test_the_absence_follows_a_positive_witness_in_the_same_table() -> None:
    assert entry_leg_census(THE_MATCHING_STAGE).entries_in_the_lexicon == 19
    assert entry_leg_census(THE_MATCHING_STAGE).deposited_entries > 1_000


def test_the_textual_side_is_taken_from_the_bridge_and_not_recounted() -> None:
    occurrences = {r.material: r.occurrences for r in material_readings()}
    for row in mirror_rows():
        assert row.textual_occurrences == occurrences[row.material]


def test_the_lexical_side_is_a_small_tally_so_its_shares_move_on_one_segment() -> None:
    total = sum(row.lexical_segments for row in mirror_rows())
    assert total == 40
    assert total < sum(row.textual_occurrences for row in mirror_rows()) / 100


def test_the_three_measures_leave_together_and_none_can_be_picked_alone() -> None:
    verdicts = dispersion_verdicts()
    assert len(verdicts) == len(DispersionMeasure)
    assert {verdict.measure for verdict in verdicts} == set(DispersionMeasure)


def test_the_expectation_is_mirrored_under_all_three_measures_at_once() -> None:
    assert all(
        verdict.the_textual_side_disperses_more for verdict in dispersion_verdicts()
    )


def test_the_verdict_is_carried_by_one_material_not_by_the_table() -> None:
    for verdict in dispersion_verdicts():
        assert verdict.standing is MirrorStanding.MIRRORED_BUT_CARRIED_BY_ONE_ROW
        assert verdict.flipping_materials == ("علم",)


def test_dropping_the_carrying_material_flips_every_measure() -> None:
    rows = tuple(row for row in mirror_rows() if row.material != "علم")
    lexical = tuple(row.lexical_segments for row in rows)
    textual = tuple(row.textual_occurrences for row in rows)
    for measure in DispersionMeasure:
        assert dispersion_of(measure, textual) < dispersion_of(measure, lexical)


def test_the_leave_one_out_pass_visits_every_row_and_names_only_what_flips() -> None:
    for measure in DispersionMeasure:
        flipping = leave_one_out_flips(measure)
        assert set(flipping) <= {row.material for row in mirror_rows()}
        assert len(flipping) == 1


def test_equality_is_not_read_as_holding_since_the_rule_is_strict() -> None:
    verdict = dispersion_verdicts()[0]
    tied = type(verdict)(
        measure=verdict.measure,
        scaled_lexical=verdict.scaled_lexical,
        scaled_textual=verdict.scaled_lexical,
        rows=verdict.rows,
        flipping_materials=(),
    )
    assert not tied.the_textual_side_disperses_more
    assert tied.standing is MirrorStanding.NOT_MIRRORED


def test_every_locked_dispersion_is_regenerated_from_the_bytes_it_names() -> None:
    assert locked_dispersions_have_drifted() == ()
    for verdict in dispersion_verdicts():
        locked = THE_LOCKED_SCALED_DISPERSIONS[verdict.measure.name]
        assert (verdict.scaled_lexical, verdict.scaled_textual) == locked


def test_the_locked_figures_are_scaled_integers_and_never_compared_as_floats() -> None:
    assert SCALE == 1_000_000
    for lexical, textual in THE_LOCKED_SCALED_DISPERSIONS.values():
        assert isinstance(lexical, int) and isinstance(textual, int)
        assert 0 <= lexical < 4 * SCALE and 0 <= textual < 4 * SCALE


def test_the_mirror_is_never_named_with_the_withheld_lexicon() -> None:
    assert THE_MIRRORED_LEXICON != THE_WITHHELD_LEXICON
    assert "لسان" not in THE_MIRRORED_LEXICON


def test_the_matching_stage_is_the_entry_leg_stage_and_not_a_second_one() -> None:
    assert THE_MATCHING_STAGE is EntryStage.HAMZA_TO_BARE_ALIF


def test_a_row_never_carries_a_negative_count() -> None:
    row = mirror_rows()[0]
    with pytest.raises(DispersionExpectationError):
        type(row)(material="كتب", lexical_segments=-1, textual_occurrences=3)
