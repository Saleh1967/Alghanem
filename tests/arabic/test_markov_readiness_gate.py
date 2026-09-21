"""Witnesses for the Markov readiness gate: prerequisites, blocked, suspended."""

from __future__ import annotations

import pytest

from alghanem.arabic import markov_readiness_gate as module
from alghanem.arabic.fath_ayah_source_text import FATH_AYAH_SOURCE_ID
from alghanem.arabic.fatiha_source_text import FATIHA_SOURCE_ID
from alghanem.arabic.lexical_artifact_closure import dominance_of
from alghanem.arabic.markov_readiness_gate import (
    MARKOV_READINESS_NAMED_RESIDUALS,
    THE_PREREQUISITE_ORDER,
    ChainReading,
    ChainStanding,
    MarkovReadinessError,
    Prerequisite,
    PrerequisiteReading,
    TokenFigure,
    functional_markov_standing,
    projection_made_regularity_on,
    the_prerequisite_chain,
    token_markov_standing,
)
from alghanem.arabic.quran_corpus_word_total import (
    quran_corpus_bytes_are_resolvable,
)

# --- the prerequisites are ordered, not a set ------------------------------


def test_the_chain_reads_every_prerequisite_once_in_the_published_order() -> None:
    read = tuple(reading.prerequisite for reading in the_prerequisite_chain())
    assert read == THE_PREREQUISITE_ORDER
    assert set(read) == set(Prerequisite)


def test_the_first_two_prerequisites_are_met_by_the_deposits_in_this_tree() -> None:
    chain = {reading.prerequisite: reading for reading in the_prerequisite_chain()}
    assert chain[Prerequisite.LEXICAL_ARTIFACT_CLOSED].met
    assert chain[Prerequisite.SUKUN_COLUMN_SPLIT].met


def test_the_corpus_bytes_prerequisite_tracks_the_resolver_and_not_a_constant() -> None:
    chain = {reading.prerequisite: reading for reading in the_prerequisite_chain()}
    assert chain[Prerequisite.CORPUS_BYTES_PRESENT].met is (
        quran_corpus_bytes_are_resolvable()
    )


def test_a_prerequisite_reading_without_a_written_ground_is_refused() -> None:
    with pytest.raises(MarkovReadinessError):
        PrerequisiteReading(
            prerequisite=Prerequisite.CORPUS_BYTES_PRESENT, met=True, ground=" "
        )


# --- token Markov is blocked at the corpus bytes ---------------------------


def test_token_markov_is_blocked_and_names_the_corpus_bytes_as_its_door() -> None:
    reading = token_markov_standing()
    assert reading.standing is ChainStanding.BLOCKED
    assert reading.blocking_prerequisite is Prerequisite.CORPUS_BYTES_PRESENT


def test_the_blocking_ground_names_the_vendored_corpus_path() -> None:
    assert "quran-simple-enhanced.txt" in token_markov_standing().ground


# --- functional Markov is suspended, not blocked ---------------------------


def test_functional_markov_is_suspended_and_carries_no_blocking_prerequisite() -> None:
    reading = functional_markov_standing()
    assert reading.standing is ChainStanding.SUSPENDED
    assert reading.blocking_prerequisite is None


def test_the_suspension_is_grounded_in_the_negative_distributional_probe() -> None:
    assert "سالبة" in functional_markov_standing().ground


def test_a_suspended_chain_may_not_carry_a_blocking_prerequisite() -> None:
    with pytest.raises(MarkovReadinessError):
        ChainReading(
            chain_name="مختلق",
            standing=ChainStanding.SUSPENDED,
            ground="سند",
            blocking_prerequisite=Prerequisite.CORPUS_BYTES_PRESENT,
        )


def test_a_blocked_chain_must_name_its_blocking_prerequisite() -> None:
    with pytest.raises(MarkovReadinessError):
        ChainReading(chain_name="مختلق", standing=ChainStanding.BLOCKED, ground="سند")


def test_the_two_chains_do_not_share_a_standing() -> None:
    assert token_markov_standing().standing is not (
        functional_markov_standing().standing
    )


# --- no token figure without a dominance reading ---------------------------


def test_a_token_figure_without_a_dominance_reading_is_refused() -> None:
    with pytest.raises(MarkovReadinessError):
        TokenFigure(name="مقدار", value=3, dominance=None)  # type: ignore[arg-type]


def test_a_token_figure_publishes_the_leading_share_of_its_dominance() -> None:
    dominance = dominance_of(FATH_AYAH_SOURCE_ID, True)
    figure = TokenFigure(name="مقدار", value=54, dominance=dominance)
    assert figure.leading_share == pytest.approx(
        dominance.leading_occurrences / dominance.tokens
    )


# --- the statistical gate: what the projection itself made -----------------


def test_the_projection_makes_two_extra_repeated_types_on_the_fath_ayah() -> None:
    regularity = projection_made_regularity_on(FATH_AYAH_SOURCE_ID)
    assert (regularity.repeated_written, regularity.repeated_projected) == (3, 5)
    assert regularity.made_by_the_projection == 2


def test_the_projection_makes_nothing_extra_on_the_fatiha() -> None:
    regularity = projection_made_regularity_on(FATIHA_SOURCE_ID)
    assert regularity.made_by_the_projection == 0


def test_an_unmeasured_deposit_is_refused_rather_than_measured() -> None:
    with pytest.raises(MarkovReadinessError):
        projection_made_regularity_on("no-such-deposit")


# --- house guards ----------------------------------------------------------


def test_every_named_residual_begins_with_its_own_key() -> None:
    for key, text in MARKOV_READINESS_NAMED_RESIDUALS.items():
        assert text.startswith(f"{key}: ")


def test_the_gate_exports_no_probability_name_despite_its_subject() -> None:
    banned = ("entropy", "nll", "likelihood", "transition_matrix", "probability")
    for exported in module.__all__:
        assert not any(word in exported.lower() for word in banned)
