"""Witnesses for the lexical artifact closure: standing, mechanism, extent, dominance."""

from __future__ import annotations

import pytest

from alghanem.arabic import lexical_artifact_closure as module
from alghanem.arabic.carrier_projection_deposit import (
    THE_DEPOSITS_PROJECTED,
    WordBoundary,
    deposited_text,
    words_of,
)
from alghanem.arabic.distributional_probe_report import RECORDED_PROBE_REPORT
from alghanem.arabic.fath_ayah_source_text import FATH_AYAH_SOURCE_ID
from alghanem.arabic.fatiha_source_text import FATIHA_SOURCE_ID
from alghanem.arabic.lexical_artifact_closure import (
    LEXICAL_ARTIFACT_NAMED_RESIDUALS,
    THE_CLOSED_CLAIMS,
    ClosedClaim,
    ClosureExtent,
    CorruptionMechanism,
    ExclusionStanding,
    LexicalArtifactError,
    closed_claim,
    dominance_of,
    refuse_to_freeze,
    the_probe_witness,
)

# --- the standing is not a threshold ---------------------------------------


def test_a_closed_artifact_carries_a_standing_of_its_own_not_below_threshold() -> None:
    for claim in THE_CLOSED_CLAIMS:
        assert claim.standing is ExclusionStanding.CLOSED_AS_LEXICAL_ARTIFACT
        assert claim.standing is not ExclusionStanding.BELOW_THRESHOLD


def test_the_three_standings_are_distinct_values_and_not_aliases() -> None:
    values = {member.value for member in ExclusionStanding}
    assert len(values) == len(ExclusionStanding) == 3


def test_a_closed_claim_may_not_be_written_with_a_weaker_standing() -> None:
    with pytest.raises(LexicalArtifactError):
        ClosedClaim(
            claim_key="مختلق",
            claim_text="دعوى",
            standing=ExclusionStanding.BELOW_THRESHOLD,
            extent=ClosureExtent.WHOLE_CLAIM,
            mechanism=CorruptionMechanism.TOKEN_REPETITION_INFLATION,
            ground="سند",
        )


# --- the mechanism has a deposited witness ---------------------------------


def test_the_probe_witness_is_read_from_the_deposited_report_not_written_here() -> None:
    witness = the_probe_witness()
    assert witness.surface_forms == (
        RECORDED_PROBE_REPORT.specification.surface_form_count
    )
    assert witness.selected_k == RECORDED_PROBE_REPORT.selected_k


def test_the_probe_selected_two_clusters_and_not_three() -> None:
    assert the_probe_witness().selected_k == 2


def test_the_smaller_cluster_mixes_function_words_with_frequent_content_words() -> None:
    members = the_probe_witness().mixed_members
    assert "في" in members
    assert "الله" in members


def test_the_cluster_split_is_lopsided_as_the_closure_prose_reports() -> None:
    witness = the_probe_witness()
    assert witness.smallest_cluster < min(witness.cluster_sizes) * 2
    assert witness.smallest_cluster == min(witness.cluster_sizes)


# --- dominance is derived, not transcribed ---------------------------------


@pytest.mark.parametrize("source_id", sorted(THE_DEPOSITS_PROJECTED))
@pytest.mark.parametrize("projected", [False, True])
def test_the_dominance_token_count_equals_what_the_deposit_holds(
    source_id: str, projected: bool
) -> None:
    reading = dominance_of(source_id, projected)
    expected = len(words_of(deposited_text(source_id), WordBoundary.ANY_WHITESPACE))
    assert reading.tokens == expected


def test_projection_lowers_the_type_count_on_the_fath_ayah_and_not_on_the_fatiha(
) -> None:
    fath_written = dominance_of(FATH_AYAH_SOURCE_ID, False)
    fath_projected = dominance_of(FATH_AYAH_SOURCE_ID, True)
    fatiha_written = dominance_of(FATIHA_SOURCE_ID, False)
    fatiha_projected = dominance_of(FATIHA_SOURCE_ID, True)
    assert fath_projected.types < fath_written.types
    assert fatiha_projected.types == fatiha_written.types


def test_the_exposed_share_is_the_repeated_mass_and_not_the_leading_share() -> None:
    reading = dominance_of(FATH_AYAH_SOURCE_ID, True)
    assert reading.exposed_share == pytest.approx(
        (reading.tokens - reading.types) / reading.tokens
    )
    assert reading.exposed_share != pytest.approx(reading.leading_share)


def test_dominance_refuses_a_deposit_outside_the_measured_scope() -> None:
    with pytest.raises(LexicalArtifactError):
        dominance_of("no-such-deposit", True)


# --- extent: whole versus measured share -----------------------------------


def test_the_sukun_overlap_claim_is_closed_whole_and_the_fatha_only_is_not() -> None:
    assert closed_claim("sukun-overlap").extent is ClosureExtent.WHOLE_CLAIM
    assert closed_claim("fatha-only").extent is ClosureExtent.MEASURED_SHARE_ONLY


def test_every_closed_claim_names_the_same_named_mechanism() -> None:
    for claim in THE_CLOSED_CLAIMS:
        assert claim.mechanism is CorruptionMechanism.TOKEN_REPETITION_INFLATION


def test_an_unknown_claim_key_is_refused_and_not_silently_admitted() -> None:
    with pytest.raises(LexicalArtifactError):
        closed_claim("لا-شيء")


# --- the closed does not return --------------------------------------------


@pytest.mark.parametrize("claim_key", ["sukun-overlap", "fatha-only"])
def test_a_closed_claim_is_always_refused_a_freeze(claim_key: str) -> None:
    with pytest.raises(LexicalArtifactError):
        refuse_to_freeze(claim_key)


# --- house guards ----------------------------------------------------------


def test_every_named_residual_begins_with_its_own_key() -> None:
    for key, text in LEXICAL_ARTIFACT_NAMED_RESIDUALS.items():
        assert text.startswith(f"{key}: ")


def test_the_module_exports_no_kernel_authority_name() -> None:
    assert not any(
        name in module.__all__ for name in ("Verdict", "freeze", "birth", "license")
    )
