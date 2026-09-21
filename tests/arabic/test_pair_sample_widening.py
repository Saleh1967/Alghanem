"""اختباراتُ توسيع عيّنة المزدوجات: الصدارةُ تثبت والقاعُ يتبيّن أثرَ الوسيط."""

from __future__ import annotations

import re
import unicodedata

import pytest

from alghanem.arabic.mark_pair_census import pair_census_over, possible_pairs
from alghanem.arabic.pair_sample_widening import (
    DAGGER,
    DAMMA,
    FATHA,
    PROSE_SCOPE_AT_MEASUREMENT,
    SHADDA,
    SUKUN,
    THE_SCOPE_EXCLUSIONS,
    THE_TAIL_AUDITED,
    PairWideningError,
    ScopeFingerprint,
    TailOccurrence,
    prose_scope_files,
    prose_scope_fingerprint,
    prose_scope_has_drifted,
    prose_scope_text,
    shadda_bearing_pairs,
    tanwin_initial_pairs,
    the_floor_is_not_arabic,
    the_floor_moves_across_the_ladder,
    the_leader_is_stable_across_the_ladder,
    the_least_frequent_arabic_pair,
    the_widening_ladder,
)
from alghanem.arabic.pair_sample_widening import (
    PAIR_SAMPLE_WIDENING_NAMED_RESIDUALS as RESIDUALS,
)


def test_the_ladder_has_three_strictly_widening_rungs() -> None:
    ladder = the_widening_ladder()
    assert len(ladder) == 3
    totals = [census.total_pairs for census in ladder]
    assert totals == sorted(totals)
    assert len(set(totals)) == 3


def test_the_widening_is_by_more_than_five_hundred_fold() -> None:
    ladder = the_widening_ladder()
    assert ladder[-1].total_pairs // ladder[1].total_pairs >= 500


def test_the_leader_never_moves_and_is_never_contested() -> None:
    for census in the_widening_ladder():
        assert census.the_lead_is_uncontested
        assert census.leaders[0].pair == (FATHA, SHADDA)
    assert the_leader_is_stable_across_the_ladder()


def test_the_floor_claims_a_different_pair_at_every_rung() -> None:
    floors = [census.ranked[-1].pair for census in the_widening_ladder()]
    assert len(set(floors)) == len(floors)
    assert the_floor_moves_across_the_ladder()


def test_the_asymmetry_is_the_point_of_the_milestone() -> None:
    assert the_leader_is_stable_across_the_ladder()
    assert the_floor_moves_across_the_ladder()


def test_the_floor_of_the_widest_rung_stands_on_a_single_occurrence() -> None:
    widest = the_widening_ladder()[-1]
    assert widest.ranked[-1].occurrences == 1
    assert widest.ranked[-1].pair == (SUKUN, DAGGER)
    assert widest.the_floor_is_uncontested


def test_the_distribution_is_a_cliff_and_not_a_tail() -> None:
    widest = the_widening_ladder()[-1]
    body = shadda_bearing_pairs(widest)
    assert body / widest.total_pairs > 0.999
    ranked = widest.ranked
    lowest_body = [count for count in ranked if SHADDA in count.pair][-1]
    highest_tail = [count for count in ranked if SHADDA not in count.pair][0]
    assert lowest_body.occurrences > 100 * highest_tail.occurrences


def test_the_two_least_frequent_pairs_are_not_arabic_at_all() -> None:
    tail = sorted(THE_TAIL_AUDITED, key=lambda entry: entry.occurrences)
    assert [entry.is_arabic for entry in tail[:2]] == [False, False]
    assert the_floor_is_not_arabic()


def test_the_least_frequent_arabic_pair_is_far_above_the_floor() -> None:
    least_arabic = the_least_frequent_arabic_pair()
    assert least_arabic.pair == (FATHA, DAGGER)
    floor = min(THE_TAIL_AUDITED, key=lambda entry: entry.occurrences)
    assert least_arabic.occurrences == 9 * floor.occurrences


def test_the_audited_tail_accounts_for_every_non_shadda_occurrence() -> None:
    widest = the_widening_ladder()[-1]
    measured = {
        count.pair: count.occurrences
        for count in widest.ranked
        if SHADDA not in count.pair
    }
    audited = {entry.pair: entry.occurrences for entry in THE_TAIL_AUDITED}
    assert measured == audited


def test_the_illegal_specimens_are_still_where_the_provenance_says() -> None:
    specimen = re.compile(f"[{FATHA}{DAMMA}]{{2}}")
    carrying = {
        path.name
        for path in prose_scope_files()
        if specimen.search(path.read_text(encoding="utf-8"))
    }
    assert carrying == {"carrier_state_candidate.py", "state_evidence.py"}


def test_widening_changed_the_population_and_not_only_its_size() -> None:
    ladder = the_widening_ladder()
    assert tanwin_initial_pairs(ladder[1]) == 0
    assert tanwin_initial_pairs(ladder[-1]) > 4000


def test_the_quranic_rungs_realize_no_tanwin_pair_whatever() -> None:
    for census in the_widening_ladder()[:2]:
        assert tanwin_initial_pairs(census) == 0


def test_the_widest_rung_realizes_nine_of_the_thirty_six() -> None:
    widest = the_widening_ladder()[-1]
    assert widest.realized == 9
    assert len(possible_pairs()) == 36


def test_realization_grows_but_never_reaches_the_permitted_thirty_six() -> None:
    realized = [census.realized for census in the_widening_ladder()]
    assert realized == sorted(realized)
    assert max(realized) < 36


def test_the_prose_scope_excludes_the_deposits_and_the_instrument() -> None:
    names = {path.name for path in prose_scope_files()}
    assert not (names & THE_SCOPE_EXCLUSIONS)
    assert "pair_sample_widening.py" in THE_SCOPE_EXCLUSIONS


def test_excluding_the_deposits_keeps_the_ladder_free_of_double_counting() -> None:
    ladder = the_widening_ladder()
    prose_only = pair_census_over(prose_scope_text(), "نثرٌ وحدَه")
    assert ladder[-1].total_pairs == ladder[1].total_pairs + prose_only.total_pairs


def test_the_scope_fingerprint_is_read_from_disk_and_matches_the_frozen_one() -> None:
    assert prose_scope_fingerprint() == PROSE_SCOPE_AT_MEASUREMENT
    assert not prose_scope_has_drifted()


def test_drift_is_detected_rather_than_smoothed_over() -> None:
    assert ScopeFingerprint(files=1, text_bytes=1) != PROSE_SCOPE_AT_MEASUREMENT


def test_an_empty_scope_is_refused_a_fingerprint() -> None:
    with pytest.raises(PairWideningError):
        ScopeFingerprint(files=0, text_bytes=1)


def test_a_floor_entry_without_provenance_is_refused() -> None:
    with pytest.raises(PairWideningError):
        TailOccurrence(
            pair=(SUKUN, DAGGER), occurrences=1, is_arabic=False, provenance="  "
        )


def test_a_pair_does_not_pair_a_mark_with_itself() -> None:
    with pytest.raises(PairWideningError):
        TailOccurrence(
            pair=(SUKUN, SUKUN), occurrences=1, is_arabic=False, provenance="x"
        )


def test_the_unoccurring_is_not_admitted_to_the_floor() -> None:
    with pytest.raises(PairWideningError):
        TailOccurrence(
            pair=(SUKUN, DAGGER), occurrences=0, is_arabic=False, provenance="x"
        )


def test_every_audited_pair_is_made_of_combining_marks() -> None:
    for entry in THE_TAIL_AUDITED:
        for mark in entry.pair:
            assert unicodedata.combining(mark) != 0


def test_the_trailers_report_a_tie_and_do_not_break_it() -> None:
    census = pair_census_over("بَّ بِّ", "تساوٍ مصنوع")
    assert len(census.trailers) == 2
    assert not census.the_floor_is_uncontested


def test_an_unrealized_pair_is_absent_from_the_trailers_not_at_their_head() -> None:
    census = the_widening_ladder()[-1]
    realized = {count.pair for count in census.ranked}
    for trailer in census.trailers:
        assert trailer.pair in realized
        assert trailer.occurrences > 0


def test_every_residual_is_named_by_its_own_key() -> None:
    assert RESIDUALS
    for key, text in RESIDUALS.items():
        assert text.startswith(f"{key}: ")


def test_the_residuals_name_the_register_and_the_dating() -> None:
    assert "THE_TREE_PROSE_IS_A_CONTRASTING_REGISTER_NOT_A_SECOND_WITNESS" in RESIDUALS
    assert "THE_PROSE_SCOPE_GROWS_WITH_THE_TREE_SO_ITS_FIGURES_ARE_DATED" in RESIDUALS
