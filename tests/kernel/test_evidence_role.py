"""Constitutional tests for G0.OB.1 and G0.EB.1."""

from dataclasses import fields
from typing import cast

import pytest

from alghanem.kernel import (
    Anchor,
    AuthenticatedObservationBinding,
    AuthenticatedObservationBridge,
    CanonicalClaimContentEncoder,
    Claim,
    ClaimCandidate,
    ClaimContentManifest,
    ClaimCore,
    ClaimEvidenceBinding,
    ClaimOccurrenceRef,
    ClaimPolarity,
    ClaimScopeRef,
    Evidence,
    EvidenceRoleCandidate,
    EvidenceRoleRef,
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


def binding(
    observation: str = "maqayis-naql-observation",
    authentication: str = "archive-attestation-1",
) -> AuthenticatedObservationBinding:
    return AuthenticatedObservationBridge._issue(observation, authentication)


def role(identifier: str = "source-attestation") -> EvidenceRoleRef:
    return EvidenceRoleRef(identifier)


def candidate(
    observed: AuthenticatedObservationBinding | None = None,
    asserted_claim: ClaimCandidate | None = None,
    proposed_role: EvidenceRoleRef | None = None,
) -> EvidenceRoleCandidate:
    return EvidenceRoleCandidate(
        observed or binding(), asserted_claim or claim(), proposed_role or role()
    )


def test_binding_rejects_direct_construction() -> None:
    with pytest.raises(
        ValueError, match="issued through AuthenticatedObservationBridge"
    ):
        AuthenticatedObservationBinding(
            "imaginary-observation", "imaginary-authentication"
        )


def test_same_observation_has_distinct_roles_for_distinct_claims() -> None:
    observed = binding()
    first = candidate(observed, claim(predicate="source-says-origin"))
    second = candidate(observed, claim(predicate="historical-origin"))

    assert (
        first.authenticated_observation_binding
        == second.authenticated_observation_binding
    )
    assert first.claim != second.claim
    assert first != second


def test_same_observation_and_claim_have_distinct_proposed_roles() -> None:
    observed, asserted_claim = binding(), claim()
    first = candidate(observed, asserted_claim, role("source-attestation"))
    second = candidate(observed, asserted_claim, role("historical-origin-support"))

    assert (
        first.authenticated_observation_binding
        == second.authenticated_observation_binding
    )
    assert first.claim == second.claim
    assert first.role != second.role
    assert first != second


def test_role_requires_binding_claim_and_role_reference() -> None:
    with pytest.raises(TypeError, match="authenticated observation binding"):
        EvidenceRoleCandidate(
            cast(AuthenticatedObservationBinding, "binding"), claim(), role()
        )
    with pytest.raises(TypeError, match="claim candidate"):
        EvidenceRoleCandidate(binding(), cast(ClaimCandidate, "claim"), role())
    with pytest.raises(TypeError, match="evidence role reference"):
        EvidenceRoleCandidate(binding(), claim(), cast(EvidenceRoleRef, "role"))


def test_role_reference_is_opaque_and_candidate_stops_before_later_judgments() -> None:
    assert {item.name for item in fields(EvidenceRoleRef)} == {"identifier"}
    assert {item.name for item in fields(EvidenceRoleCandidate)} == {
        "authenticated_observation_binding",
        "claim",
        "role",
    }
    assert {item.name for item in fields(EvidenceRoleCandidate)}.isdisjoint(
        {"applicable", "sufficient", "truth", "knowledge"}
    )


def projection(value: EvidenceRoleCandidate, deleted: str) -> tuple[object, ...]:
    return tuple(
        coordinate
        for name, coordinate in (
            ("observation", value.authenticated_observation_binding),
            ("claim", value.claim),
            ("role", value.role),
        )
        if name != deleted
    )


@pytest.mark.parametrize(
    ("deleted", "first", "second"),
    [
        (
            "observation",
            candidate(binding("first-observation"), claim(), role()),
            candidate(binding("second-observation"), claim(), role()),
        ),
        (
            "claim",
            candidate(binding(), claim(predicate="source-says-origin"), role()),
            candidate(binding(), claim(predicate="historical-origin"), role()),
        ),
        (
            "role",
            candidate(binding(), claim(), role("source-attestation")),
            candidate(binding(), claim(), role("counterevidence")),
        ),
    ],
    ids=["observation", "claim", "role"],
)
def test_deleting_each_core_coordinate_collapses_distinct_roles(
    deleted: str, first: EvidenceRoleCandidate, second: EvidenceRoleCandidate
) -> None:
    assert first != second
    assert projection(first, deleted) == projection(second, deleted)


def test_legacy_evidence_and_claim_binding_are_not_g0eb1_candidates() -> None:
    legacy = ClaimEvidenceBinding(
        Claim("legacy-claim", "statement"), (Evidence("legacy-claim", "basis"),)
    )

    assert type(legacy) is ClaimEvidenceBinding
    assert type(candidate()) is EvidenceRoleCandidate
    assert "role" not in {item.name for item in fields(ClaimEvidenceBinding)}
