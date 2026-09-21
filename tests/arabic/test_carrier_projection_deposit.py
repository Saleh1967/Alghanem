"""Witnesses for the deposited carrier projection: carriers, boundary, edge."""

from __future__ import annotations

import pytest

from alghanem.arabic import carrier_projection_deposit as module
from alghanem.arabic.carrier_projection_deposit import (
    CARRIER_PROJECTION_NAMED_RESIDUALS,
    THE_DEPOSITS_PROJECTED,
    THE_FOLDING,
    CarrierProjectionError,
    ProjectionCensus,
    WordBoundary,
    census_of,
    collisions_in,
    deposited_text,
    edges_of,
    project_letter,
    project_word,
    repeated_skeletons_in,
    repeated_words_in,
    the_edges_only_the_space_rule_makes,
    the_twenty_nine,
    words_of,
)
from alghanem.arabic.encoding.carrier_state_candidate import DECLARED_CARRIERS
from alghanem.arabic.fath_ayah_source_text import FATH_AYAH_SOURCE_ID
from alghanem.arabic.fatiha_source_text import FATIHA_SOURCE_ID

FATIHA = FATIHA_SOURCE_ID
FATH = FATH_AYAH_SOURCE_ID


# --- the projection is a folding, not a discovery ---------------------------


def test_the_carriers_are_twenty_nine() -> None:
    assert len(the_twenty_nine()) == 29


def test_the_twenty_nine_are_derived_from_the_deposited_set_not_rewritten() -> None:
    folded = {THE_FOLDING.get(letter, letter) for letter in DECLARED_CARRIERS}
    assert set(the_twenty_nine()) == folded


def test_the_folding_is_exactly_eight_written_forms() -> None:
    assert len(THE_FOLDING) == 8


def test_every_folded_form_is_itself_no_longer_a_carrier() -> None:
    for written in THE_FOLDING:
        assert written not in the_twenty_nine()


def test_every_fold_target_is_a_carrier() -> None:
    for base in THE_FOLDING.values():
        assert base in the_twenty_nine()


def test_the_five_hamza_forms_all_fold_to_one_carrier() -> None:
    assert {THE_FOLDING[form] for form in "أإؤئآ"} == {"ء"}


def test_the_wasla_alef_folds_to_the_alef() -> None:
    assert THE_FOLDING["\u0671"] == "\u0627"


def test_a_haraka_projects_to_nothing() -> None:
    for mark in "\u064b\u064c\u064d\u064e\u064f\u0650\u0651\u0652\u0670":
        assert project_letter(mark) is None


def test_a_carrier_projects_to_itself() -> None:
    for carrier in the_twenty_nine():
        assert project_letter(carrier) == carrier


def test_projecting_a_word_keeps_order_and_drops_the_rest() -> None:
    assert project_word("مُحَمَّدٌ") == "محمد"


def test_projecting_is_idempotent() -> None:
    for source_id in THE_DEPOSITS_PROJECTED:
        for word in words_of(deposited_text(source_id), WordBoundary.ANY_WHITESPACE):
            once = project_word(word)
            assert project_word(once) == once


# --- the word boundary is a decision ---------------------------------------


def test_the_space_rule_and_the_whitespace_rule_disagree_on_the_fatiha() -> None:
    assert census_of(FATIHA, WordBoundary.SPACE_ONLY).words == 23
    assert census_of(FATIHA, WordBoundary.ANY_WHITESPACE).words == 29


def test_the_two_rules_agree_exactly_on_the_fath_ayah() -> None:
    narrow = census_of(FATH, WordBoundary.SPACE_ONLY)
    wide = census_of(FATH, WordBoundary.ANY_WHITESPACE)
    assert narrow.words == wide.words == 54
    assert narrow.edges == wide.edges == 195


def test_a_rule_that_is_inert_on_one_text_is_not_thereby_right() -> None:
    assert the_edges_only_the_space_rule_makes(FATH) == ()
    assert the_edges_only_the_space_rule_makes(FATIHA) != ()


def test_the_space_rule_fabricates_exactly_six_edges_on_the_fatiha() -> None:
    assert len(the_edges_only_the_space_rule_makes(FATIHA)) == 6


def test_the_fabricated_edges_are_the_ayah_seams() -> None:
    assert the_edges_only_the_space_rule_makes(FATIHA) == (
        ("م", "ا"),
        ("م", "ص"),
        ("م", "م"),
        ("ن", "ء"),
        ("ن", "ا"),
        ("ن", "ا"),
    )


def test_the_fatiha_separates_its_ayahs_by_a_newline_not_a_space() -> None:
    assert "\n" in deposited_text(FATIHA)
    assert "\n" not in deposited_text(FATH)


def test_the_carrier_count_does_not_move_between_the_two_rules() -> None:
    for source_id in THE_DEPOSITS_PROJECTED:
        narrow = census_of(source_id, WordBoundary.SPACE_ONLY)
        wide = census_of(source_id, WordBoundary.ANY_WHITESPACE)
        assert narrow.carrier_occurrences == wide.carrier_occurrences


def test_only_the_edge_count_moves() -> None:
    narrow = census_of(FATIHA, WordBoundary.SPACE_ONLY)
    wide = census_of(FATIHA, WordBoundary.ANY_WHITESPACE)
    assert narrow.edges - wide.edges == 6


def test_the_space_rule_makes_a_fourteen_carrier_word_that_is_two_words() -> None:
    assert census_of(FATIHA, WordBoundary.SPACE_ONLY).longest_word == 14
    assert census_of(FATIHA, WordBoundary.ANY_WHITESPACE).longest_word == 8


def test_words_of_never_yields_an_empty_word() -> None:
    for source_id in THE_DEPOSITS_PROJECTED:
        for boundary in WordBoundary:
            assert all(words_of(deposited_text(source_id), boundary))


# --- the edge definition ----------------------------------------------------


def test_the_edge_count_is_the_carriers_minus_the_words() -> None:
    for source_id in THE_DEPOSITS_PROJECTED:
        for boundary in WordBoundary:
            census = census_of(source_id, boundary)
            assert census.edges == census.carrier_occurrences - census.words


def test_the_refused_boundary_edges_are_published_not_silent() -> None:
    assert census_of(FATIHA, WordBoundary.ANY_WHITESPACE).boundary_edges_refused == 28
    assert census_of(FATH, WordBoundary.ANY_WHITESPACE).boundary_edges_refused == 53


def test_the_edge_list_has_exactly_the_counted_length() -> None:
    for source_id in THE_DEPOSITS_PROJECTED:
        for boundary in WordBoundary:
            listed = edges_of(source_id, boundary)
            assert len(listed) == census_of(source_id, boundary).edges


def test_every_edge_joins_two_carriers() -> None:
    for source_id in THE_DEPOSITS_PROJECTED:
        for left, right in edges_of(source_id, WordBoundary.ANY_WHITESPACE):
            assert left in the_twenty_nine()
            assert right in the_twenty_nine()


def test_a_census_refuses_an_edge_count_that_breaks_the_definition() -> None:
    with pytest.raises(CarrierProjectionError):
        ProjectionCensus(
            source_id=FATH,
            boundary=WordBoundary.ANY_WHITESPACE,
            words=54,
            carrier_occurrences=249,
            edges=249,
            boundary_edges_refused=53,
            residue_occurrences=204,
            residue_kinds=8,
            longest_word=8,
            distinct_words=50,
            distinct_skeletons=47,
        )


def test_a_census_refuses_a_refusal_count_that_is_not_the_words_minus_one() -> None:
    with pytest.raises(CarrierProjectionError):
        ProjectionCensus(
            source_id=FATH,
            boundary=WordBoundary.ANY_WHITESPACE,
            words=54,
            carrier_occurrences=249,
            edges=195,
            boundary_edges_refused=0,
            residue_occurrences=204,
            residue_kinds=8,
            longest_word=8,
            distinct_words=50,
            distinct_skeletons=47,
        )


# --- what the projection costs ---------------------------------------------


def test_the_residue_is_counted_not_discarded_silently() -> None:
    assert census_of(FATIHA, WordBoundary.ANY_WHITESPACE).residue_occurrences == 119
    assert census_of(FATH, WordBoundary.ANY_WHITESPACE).residue_occurrences == 204


def test_the_residue_kinds_differ_between_the_two_deposits() -> None:
    assert census_of(FATIHA, WordBoundary.ANY_WHITESPACE).residue_kinds == 6
    assert census_of(FATH, WordBoundary.ANY_WHITESPACE).residue_kinds == 8


def test_every_character_is_carrier_or_residue_or_whitespace() -> None:
    for source_id in THE_DEPOSITS_PROJECTED:
        text = deposited_text(source_id)
        census = census_of(source_id, WordBoundary.ANY_WHITESPACE)
        whitespace = sum(1 for character in text if character.isspace())
        assert (
            census.carrier_occurrences + census.residue_occurrences + whitespace
        ) == len(text)


def test_the_fath_ayah_collides_three_pairs() -> None:
    assert len(collisions_in(FATH)) == 3


def test_the_fatiha_collides_nothing() -> None:
    assert collisions_in(FATIHA) == {}


def test_every_collision_on_this_evidence_is_an_ending() -> None:
    for written in collisions_in(FATH).values():
        heads = {word[:-1] for word in written}
        assert len(heads) == 1


def test_the_collisions_are_the_three_named_in_the_docstring() -> None:
    assert set(collisions_in(FATH)) == {"الله", "الكفار", "من"}


def test_the_distinct_counts_record_the_collision() -> None:
    census = census_of(FATH, WordBoundary.ANY_WHITESPACE)
    assert census.distinct_words - census.distinct_skeletons == 3


def test_the_fatiha_records_no_collision_in_its_counts() -> None:
    census = census_of(FATIHA, WordBoundary.ANY_WHITESPACE)
    assert census.distinct_words == census.distinct_skeletons == 26


# --- repetition is made by the projection, not found by it ------------------


def test_the_projection_creates_repetition_on_the_fath_ayah() -> None:
    assert len(repeated_words_in(FATH)) == 3
    assert len(repeated_skeletons_in(FATH)) == 5


def test_the_name_of_god_repeats_twice_written_and_three_times_projected() -> None:
    assert repeated_words_in(FATH)["اللَّهِ"] == 2
    assert repeated_skeletons_in(FATH)["الله"] == 3


def test_the_fatiha_repeats_the_same_three_either_way() -> None:
    assert len(repeated_words_in(FATIHA)) == len(repeated_skeletons_in(FATIHA)) == 3


def test_a_repeated_skeleton_is_never_rarer_than_its_written_word() -> None:
    for source_id in THE_DEPOSITS_PROJECTED:
        written = repeated_words_in(source_id)
        projected = repeated_skeletons_in(source_id)
        for word, total in written.items():
            assert projected[project_word(word)] >= total


# --- the deposits and the refusals -----------------------------------------


def test_exactly_two_deposits_are_projected() -> None:
    assert len(THE_DEPOSITS_PROJECTED) == 2


def test_the_two_deposits_hold_eighty_three_words_between_them() -> None:
    total = sum(
        census_of(source_id, WordBoundary.ANY_WHITESPACE).words
        for source_id in THE_DEPOSITS_PROJECTED
    )
    assert total == 83


def test_a_text_outside_the_tree_is_refused_not_fetched() -> None:
    with pytest.raises(CarrierProjectionError):
        deposited_text("masaq-not-in-this-tree")


def test_no_probability_name_is_exported() -> None:
    banned = ("entropy", "probab", "nll", "likelihood", "markov")
    for name in module.__all__:
        if name in CARRIER_PROJECTION_NAMED_RESIDUALS:
            continue
        assert not any(word in name.lower() for word in banned)


def test_the_no_probability_residual_is_present() -> None:
    assert (
        "NO_PROBABILITY_IS_COMPUTED_HERE_AND_NONE_MAY_BE_READ_IN"
        in CARRIER_PROJECTION_NAMED_RESIDUALS
    )


def test_masaq_is_named_and_refused_in_the_same_breath() -> None:
    residual = CARRIER_PROJECTION_NAMED_RESIDUALS[
        "MASAQ_IS_NAMED_AND_NOT_DEPOSITED_SO_ITS_CHAIN_STAYS_UNREAD"
    ]
    assert "MASAQ" in residual


def test_every_residual_is_named_by_its_key() -> None:
    for key, text in CARRIER_PROJECTION_NAMED_RESIDUALS.items():
        assert text.startswith(f"{key}: ")


def test_five_residuals_are_named() -> None:
    assert len(CARRIER_PROJECTION_NAMED_RESIDUALS) == 5


def test_the_census_is_frozen() -> None:
    census = census_of(FATH, WordBoundary.ANY_WHITESPACE)
    with pytest.raises(AttributeError):
        census.words = 0  # type: ignore[misc]
