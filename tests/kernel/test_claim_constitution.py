"""Constitutional tests for G0.C.1's evidence-free claim candidates."""

from dataclasses import fields

import pytest

from alghanem.kernel import (
    Anchor,
    CanonicalClaimContentEncoder,
    ClaimCandidate,
    ClaimContentIdentity,
    ClaimContentManifest,
    ClaimOccurrenceRef,
    ClaimPolarity,
    ClaimQualification,
    ClaimScopeRef,
)


def content(
    *,
    polarity: ClaimPolarity = ClaimPolarity.AFFIRM,
    scope: ClaimScopeRef | None = None,
    qualifications: tuple[ClaimQualification, ...] = (),
) -> ClaimContentManifest:
    return ClaimContentManifest(
        anchor=Anchor("repository", "Saleh1967/Alghanem@62755d7"),
        predicate="has authenticated observations",
        polarity=polarity,
        scope=scope or ClaimScopeRef("repository-revision", "62755d7"),
        qualifications=qualifications,
    )


def candidate(occurrence: str = "claim-1") -> ClaimCandidate:
    manifest_content = content()
    return ClaimCandidate(
        occurrence=ClaimOccurrenceRef(occurrence),
        content=manifest_content,
        content_manifest=CanonicalClaimContentEncoder.encode(manifest_content),
    )


def test_content_identity_is_encoder_issued_and_independent_of_occurrence() -> None:
    with pytest.raises(ValueError, match="issued by CanonicalClaimContentEncoder"):
        ClaimContentIdentity("sha256", "claim-content-manifest-v1", "0" * 64)

    first = candidate("claim-1")
    second = candidate("claim-2")

    assert first.occurrence != second.occurrence
    assert first.content_id == second.content_id


def test_scope_polarity_and_qualifications_are_claim_content() -> None:
    baseline = CanonicalClaimContentEncoder.encode(content())
    changed_scope = CanonicalClaimContentEncoder.encode(
        content(scope=ClaimScopeRef("repository", "Saleh1967/Alghanem"))
    )
    negated = CanonicalClaimContentEncoder.encode(
        content(polarity=ClaimPolarity.NEGATE)
    )
    qualified = CanonicalClaimContentEncoder.encode(
        content(qualifications=(ClaimQualification("modality", "possible"),))
    )

    assert baseline.content_id != changed_scope.content_id
    assert baseline.content_id != negated.content_id
    assert baseline.content_id != qualified.content_id


def test_candidate_rejects_a_manifest_for_other_content() -> None:
    with pytest.raises(ValueError, match="does not match"):
        ClaimCandidate(
            occurrence=ClaimOccurrenceRef("claim-1"),
            content=content(),
            content_manifest=CanonicalClaimContentEncoder.encode(
                content(polarity=ClaimPolarity.NEGATE)
            ),
        )


def test_claim_candidate_has_no_evidence_truth_or_knowledge_fields() -> None:
    assert {field.name for field in fields(ClaimCandidate)} == {
        "occurrence",
        "content",
        "content_manifest",
        "content_id",
    }
