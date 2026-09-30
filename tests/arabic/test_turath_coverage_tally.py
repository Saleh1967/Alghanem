"""اختباراتُ قياس جدول تغطية عقد الدال بالتراث."""

from __future__ import annotations

import pytest

from alghanem.arabic.markov_readiness_gate import token_markov_standing
from alghanem.arabic.turath_coverage_tally import (
    A_COVERAGE_CLAIM_WITHOUT_A_CRITERION_IS_NOT_FALSIFIABLE,
    A_FIGURE_MEASURED_ELSEWHERE_DOES_NOT_BECOME_OURS_BY_BEING_TABULATED,
    A_HEDGED_VERDICT_IS_NOT_THE_PLAIN_ONE_IT_IS_TALLIED_WITH,
    AN_ABSENCE_IN_AN_UNDEPOSITED_CORPUS_IS_NOT_A_MEASURED_ABSENCE,
    THE_BREACHES_AT_MEASUREMENT,
    THE_COVERAGE_CRITERION_IS_ABSENT,
    THE_GROUND_CENSUS_AT_MEASUREMENT,
    THE_QUOTED_HEADER,
    THE_QUOTED_NETWORK_WORDS,
    THE_QUOTED_NODE_COUNT,
    THE_ROWS,
    THE_TALLY_AT_MEASUREMENT,
    THE_TALLY_IS_AN_IDENTITY_INSIDE_THE_QUOTATION,
    THE_TURATH_TEXTS_NAMED_IN_THE_TABLE,
    TURATH_COVERAGE_NAMED_RESIDUALS,
    CoverageRow,
    Ground,
    Mark,
    QuotedHeader,
    Tally,
    TurathCoverageError,
    deposited_ayah_lines,
    deposited_corpora,
    falsifiable_rows,
    ground_census,
    hedged_rows,
    mark_census,
    no_turath_bytes_are_deposited,
    our_totals_are_not_the_quoted_denominator,
    rows_by_ground,
    tally,
    the_atom_figure_is_rederivable_here,
    the_ayah_figure_is_rederivable_here,
    the_corpus_gate_is_untouched,
    the_header_overstates_the_covered_rows_by,
    the_measured_figures_have_drifted,
    the_title_is_unreached_even_by_the_header,
    unnamed_nodes,
)


def test_the_frozen_figures_still_match_what_the_rows_and_disk_give() -> None:
    assert the_measured_figures_have_drifted() is False


def test_the_tally_is_the_frozen_four() -> None:
    current = tally()
    assert (current.rows, current.covered, current.absent, current.hedged) == (
        THE_TALLY_AT_MEASUREMENT
    )


def test_the_table_holds_twenty_five_rows_not_the_thirty_three_of_its_title() -> None:
    assert len(THE_ROWS) == 25
    assert THE_QUOTED_NODE_COUNT == 33
    assert unnamed_nodes() == 8


def test_the_header_overstates_the_covered_rows_by_seven() -> None:
    assert THE_QUOTED_HEADER.covered == 28
    assert tally().covered == 21
    assert the_header_overstates_the_covered_rows_by() == 7


def test_the_header_does_not_even_reach_its_own_title() -> None:
    assert THE_QUOTED_HEADER.total == 32
    assert the_title_is_unreached_even_by_the_header() == 1


def test_the_three_breaches_are_the_frozen_three() -> None:
    assert (
        the_header_overstates_the_covered_rows_by(),
        unnamed_nodes(),
        the_title_is_unreached_even_by_the_header(),
    ) == THE_BREACHES_AT_MEASUREMENT


def test_no_two_of_the_three_totals_agree() -> None:
    totals = {len(THE_ROWS), THE_QUOTED_HEADER.total, THE_QUOTED_NODE_COUNT}
    assert len(totals) == 3


def test_the_absent_rows_are_the_four_that_were_declared() -> None:
    absent = [row for row in THE_ROWS if not row.mark.is_counted_covered_by_the_header]
    assert len(absent) == 4
    assert THE_QUOTED_HEADER.absent == 4


def test_the_verdict_vocabulary_is_four_valued_not_two() -> None:
    census = mark_census()
    assert len(census) == 4
    assert census[Mark.COVERED] == 20
    assert census[Mark.COVERED_STRUCTURALLY] == 1
    assert census[Mark.ABSENT] == 3
    assert census[Mark.ABSENT_NO_EXPLICIT_NODE] == 1


def test_two_rows_carry_a_hedge_that_the_two_way_tally_erases() -> None:
    hedged = hedged_rows()
    assert len(hedged) == 2
    assert {row.mark for row in hedged} == {
        Mark.COVERED_STRUCTURALLY,
        Mark.ABSENT_NO_EXPLICIT_NODE,
    }


def test_the_hedged_covered_row_is_still_counted_covered_by_the_header() -> None:
    """التحفُّظُ يُعَدّ تغطيةً في جمع الترويسة؛ يُسجَّل ذلك ولا يُصحَّح."""

    assert Mark.COVERED_STRUCTURALLY.is_counted_covered_by_the_header is True
    assert Mark.COVERED_STRUCTURALLY.is_hedged is True


def test_no_row_of_the_table_is_falsifiable_while_the_criterion_is_absent() -> None:
    assert falsifiable_rows() == ()
    assert all(row.is_falsifiable_here is False for row in THE_ROWS)
    assert THE_COVERAGE_CRITERION_IS_ABSENT.strip()


def test_the_ground_census_is_the_frozen_five() -> None:
    assert tuple(ground_census()[ground] for ground in Ground) == (
        THE_GROUND_CENSUS_AT_MEASUREMENT
    )


def test_exactly_one_row_is_rederivable_from_this_tree() -> None:
    rederivable = rows_by_ground(Ground.REDERIVABLE_HERE)
    assert len(rederivable) == 1
    assert rederivable[0].measured_node == "الذرّات 112"
    assert the_atom_figure_is_rederivable_here() is True


def test_no_row_is_purely_audit_material_because_the_network_row_is_mixed() -> None:
    assert rows_by_ground(Ground.AUDIT_MATERIAL_ONLY) == ()
    mixed = rows_by_ground(Ground.MIXED_GROUNDS)
    assert len(mixed) == 1
    assert mixed[0].measured_node.startswith("الشبكة")


def test_one_figure_of_the_mixed_row_is_ours_and_another_is_not() -> None:
    assert deposited_ayah_lines() == 6_236
    assert the_ayah_figure_is_rederivable_here() is True
    assert our_totals_are_not_the_quoted_denominator() is True
    assert THE_QUOTED_NETWORK_WORDS == 77_801


def test_most_rows_carry_no_figure_at_all() -> None:
    assert len(rows_by_ground(Ground.NO_FIGURE)) == 16
    assert len(rows_by_ground(Ground.NOT_DEPOSITED)) == 7


def test_the_ground_counts_sum_to_the_rows() -> None:
    assert sum(ground_census().values()) == len(THE_ROWS)


def test_no_turath_bytes_are_deposited_so_the_absences_are_unmeasurable() -> None:
    assert no_turath_bytes_are_deposited() is True
    assert deposited_corpora() == (
        "globalquran-simple-enhanced.txt",
        "quran-simple-enhanced.txt",
    )
    assert len(THE_TURATH_TEXTS_NAMED_IN_THE_TABLE) == 5


def test_a_row_with_an_empty_column_is_refused() -> None:
    with pytest.raises(TurathCoverageError):
        CoverageRow(
            measured_node="  ",
            turath_node="باب",
            mark=Mark.COVERED,
            ground=Ground.NO_FIGURE,
        )


def test_a_negative_header_is_refused() -> None:
    with pytest.raises(TurathCoverageError):
        QuotedHeader(covered=-1, absent=4)


def test_a_tally_that_does_not_sum_to_its_rows_is_refused() -> None:
    with pytest.raises(TurathCoverageError):
        Tally(rows=25, covered=21, absent=3, hedged=2)


def test_every_row_names_both_of_its_columns() -> None:
    for row in THE_ROWS:
        assert row.measured_node.strip()
        assert row.turath_node.strip()


def test_every_named_residual_opens_with_its_own_name() -> None:
    for name, text in TURATH_COVERAGE_NAMED_RESIDUALS.items():
        assert text.startswith(f"{name}: ")


def test_the_five_residuals_are_the_exported_five() -> None:
    assert set(TURATH_COVERAGE_NAMED_RESIDUALS.values()) == {
        THE_TALLY_IS_AN_IDENTITY_INSIDE_THE_QUOTATION,
        A_COVERAGE_CLAIM_WITHOUT_A_CRITERION_IS_NOT_FALSIFIABLE,
        A_HEDGED_VERDICT_IS_NOT_THE_PLAIN_ONE_IT_IS_TALLIED_WITH,
        A_FIGURE_MEASURED_ELSEWHERE_DOES_NOT_BECOME_OURS_BY_BEING_TABULATED,
        AN_ABSENCE_IN_AN_UNDEPOSITED_CORPUS_IS_NOT_A_MEASURED_ABSENCE,
    }


def test_the_corpus_gate_is_untouched_by_this_unit() -> None:
    assert the_corpus_gate_is_untouched() is True
    assert token_markov_standing() is not None
