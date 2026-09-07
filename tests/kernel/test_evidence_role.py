"""Constitutional tests for G0.EB.1's claim-relative evidence role boundary."""

from dataclasses import fields
from typing import cast

import pytest

from alghanem.kernel import (
    Anchor,
    AuthenticatedObservation,
    CanonicalClaimContentEncoder,
    ClaimCandidate,
    ClaimContentManifest,
    ClaimCore,
    ClaimOccurrenceRef,
    ClaimPolarity,
    ClaimScopeRef,
    EvidenceRoleCandidate,
    PredicateRef,
)


def claim(
    occurrence: str = "claim-1",
    *,
    predicate: str = "source-says",
    polarity: ClaimPolarity = ClaimPolarity.AFFIRM,
    scope: ClaimScopeRef | None = None,
) -> ClaimCandidate:
    content = ClaimContentManifest(
        core=ClaimCore(
            anchor=Anchor(identifier="ibn-faris:maqayis-naql", domain="lexicon"),
            predicate=PredicateRef(predicate),
            polarity=polarity,
            scope=scope or ClaimScopeRef("work-entry", "naqala"),
        )
    )
    return ClaimCandidate(
        occurrence=ClaimOccurrenceRef(occurrence),
        content=content,
        content_manifest=CanonicalClaimContentEncoder.encode(content),
    )


def observation(
    observation_id: str = "maqayis-naql-observation",
    authentication_id: str = "archive-attestation-1",
) -> AuthenticatedObservation:
    return AuthenticatedObservation(observation_id, authentication_id)


def test_same_observation_has_distinct_roles_for_distinct_claims() -> None:
    source_statement = claim(predicate="ibn-faris-says-origin-is-transfer")
    historical_truth = claim(predicate="historical-origin-is-transfer")
    observed = observation()

    first = EvidenceRoleCandidate(observed, source_statement)
    second = EvidenceRoleCandidate(observed, historical_truth)

    assert first.observation == second.observation
    assert first.claim != second.claim
    assert first != second


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("observation_id", ""),
        ("authentication_id", "   "),
    ],
)
def test_authenticated_observation_rejects_blank_coordinates(
    field_name: str, value: str
) -> None:
    values = {
        "observation_id": "maqayis-naql-observation",
        "authentication_id": "archive-attestation-1",
    }
    values[field_name] = value

    with pytest.raises(ValueError, match="must be non-blank text"):
        AuthenticatedObservation(**values)


def test_role_requires_authenticated_observation_and_structured_claim() -> None:
    with pytest.raises(TypeError, match="authenticated observation"):
        EvidenceRoleCandidate(cast(AuthenticatedObservation, "observation"), claim())
    with pytest.raises(TypeError, match="claim candidate"):
        EvidenceRoleCandidate(observation(), cast(ClaimCandidate, "claim"))


def test_observation_authentication_is_not_evidence_applicability() -> None:
    assert {item.name for item in fields(AuthenticatedObservation)} == {
        "observation_id",
        "authentication_id",
    }
    assert {item.name for item in fields(EvidenceRoleCandidate)} == {
        "observation",
        "claim",
    }


def test_role_candidate_stops_before_sufficiency_truth_and_knowledge() -> None:
    field_names = {item.name for item in fields(EvidenceRoleCandidate)}

    assert field_names.isdisjoint({"applicable", "sufficient", "truth", "knowledge"})


def test_weaker_id_only_model_collapses_distinct_roles() -> None:
    observed = observation()
    first = EvidenceRoleCandidate(observed, claim(predicate="source-says-origin"))
    second = EvidenceRoleCandidate(observed, claim(predicate="historical-origin"))

    assert first.observation.observation_id == second.observation.observation_id
    assert first != second


def test_weaker_anchor_only_model_collapses_distinct_roles() -> None:
    observed = observation()
    first = EvidenceRoleCandidate(observed, claim(predicate="source-says-origin"))
    second = EvidenceRoleCandidate(observed, claim(predicate="historical-origin"))

    assert first.claim.content.core.anchor == second.claim.content.core.anchor
    assert first != second


def test_weaker_scope_only_model_collapses_distinct_roles() -> None:
    observed = observation()
    first = EvidenceRoleCandidate(observed, claim(predicate="source-says-origin"))
    second = EvidenceRoleCandidate(observed, claim(predicate="historical-origin"))

    assert first.claim.content.core.scope == second.claim.content.core.scope
    assert first != second


def test_weaker_shared_provenance_model_collapses_distinct_roles() -> None:
    shared_authentication = "archive-attestation-1"
    first = EvidenceRoleCandidate(
        observation("maqayis-naql-observation", shared_authentication),
        claim(predicate="source-says-origin"),
    )
    second = EvidenceRoleCandidate(
        observation("maqayis-naql-copy", shared_authentication),
        claim(predicate="historical-origin"),
    )

    assert first.observation.authentication_id == second.observation.authentication_id
    assert first != second
