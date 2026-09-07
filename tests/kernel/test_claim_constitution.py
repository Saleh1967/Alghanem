"""Constitutional tests for G0.C.1's evidence-free claim candidates."""

from dataclasses import fields

import pytest

from alghanem.kernel import (
    Anchor,
    CanonicalClaimContentEncoder,
    Claim,
    ClaimCandidate,
    ClaimContentIdentity,
    ClaimContentManifest,
    ClaimCore,
    ClaimEvidenceBinding,
    ClaimOccurrenceRef,
    ClaimPolarity,
    ClaimQualification,
    ClaimScopeRef,
    Evidence,
    PredicateRef,
    claim_constitution,
)


def core(
    *,
    anchor: Anchor | None = None,
    predicate: PredicateRef | None = None,
    polarity: ClaimPolarity = ClaimPolarity.AFFIRM,
    scope: ClaimScopeRef | None = None,
) -> ClaimCore:
    return ClaimCore(
        anchor=anchor
        or Anchor(
            identifier="Saleh1967/Alghanem@62755d7",
            domain="repository",
        ),
        predicate=predicate or PredicateRef("repository-observation-authority"),
        polarity=polarity,
        scope=scope or ClaimScopeRef("repository-revision", "62755d7"),
    )


def content(
    *,
    claim_core: ClaimCore | None = None,
    qualifications: tuple[ClaimQualification, ...] = (),
) -> ClaimContentManifest:
    return ClaimContentManifest(
        core=claim_core or core(), qualifications=qualifications
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


@pytest.mark.parametrize("deleted", ["anchor", "predicate", "polarity", "scope"])
def test_every_claim_core_field_is_necessary_for_representability(deleted: str) -> None:
    core_fields = {
        "anchor": core().anchor,
        "predicate": core().predicate,
        "polarity": core().polarity,
        "scope": core().scope,
    }
    del core_fields[deleted]

    with pytest.raises(
        TypeError, match=f"missing 1 required positional argument: '{deleted}'"
    ):
        ClaimCore(**core_fields)  # type: ignore[call-arg]


def test_core_fields_and_ordered_qualifications_are_claim_content() -> None:
    baseline = CanonicalClaimContentEncoder.encode(content())
    changed_anchor = CanonicalClaimContentEncoder.encode(
        content(
            claim_core=core(
                anchor=Anchor(
                    identifier="Saleh1967/Alghanem@62755d8",
                    domain="repository",
                )
            )
        )
    )
    changed_predicate = CanonicalClaimContentEncoder.encode(
        content(claim_core=core(predicate=PredicateRef("other-predicate")))
    )
    changed_scope = CanonicalClaimContentEncoder.encode(
        content(
            claim_core=core(scope=ClaimScopeRef("repository", "Saleh1967/Alghanem"))
        )
    )
    negated = CanonicalClaimContentEncoder.encode(
        content(claim_core=core(polarity=ClaimPolarity.NEGATE))
    )
    first_qualification = ClaimQualification("modality", "possible")
    second_qualification = ClaimQualification("context", "review")
    ordered = CanonicalClaimContentEncoder.encode(
        content(qualifications=(first_qualification, second_qualification))
    )
    reversed_order = CanonicalClaimContentEncoder.encode(
        content(qualifications=(second_qualification, first_qualification))
    )

    assert baseline.content_id != changed_anchor.content_id
    assert baseline.content_id != changed_predicate.content_id
    assert baseline.content_id != changed_scope.content_id
    assert baseline.content_id != negated.content_id
    assert ordered.content_id != reversed_order.content_id


def test_predicate_reference_has_no_rendered_text_field() -> None:
    assert {item.name for item in fields(PredicateRef)} == {"identifier"}


def test_schema_coverage_rejects_an_unaccounted_manifest_field(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(claim_constitution, "MANIFEST_COVERAGE", ("core",))

    with pytest.raises(RuntimeError, match="coverage"):
        CanonicalClaimContentEncoder.encode(content())


def test_candidate_rejects_a_manifest_for_other_content() -> None:
    with pytest.raises(ValueError, match="does not match"):
        ClaimCandidate(
            occurrence=ClaimOccurrenceRef("claim-1"),
            content=content(),
            content_manifest=CanonicalClaimContentEncoder.encode(
                content(claim_core=core(polarity=ClaimPolarity.NEGATE))
            ),
        )


def test_occurrence_reference_reuse_does_not_prove_occurrence_identity() -> None:
    occurrence = ClaimOccurrenceRef("reusable-local-reference")
    first_content = content()
    second_content = content(claim_core=core(polarity=ClaimPolarity.NEGATE))

    first = ClaimCandidate(
        occurrence=occurrence,
        content=first_content,
        content_manifest=CanonicalClaimContentEncoder.encode(first_content),
    )
    second = ClaimCandidate(
        occurrence=occurrence,
        content=second_content,
        content_manifest=CanonicalClaimContentEncoder.encode(second_content),
    )

    assert first.occurrence == second.occurrence
    assert first.content_id != second.content_id


def test_legacy_claim_id_binding_is_not_g0c1_evidence_binding() -> None:
    legacy = ClaimEvidenceBinding(
        Claim("legacy-claim", "statement"), (Evidence("legacy-claim", "basis"),)
    )

    assert type(legacy.claim) is Claim
    assert type(candidate()) is ClaimCandidate
    assert "content_id" not in {item.name for item in fields(ClaimEvidenceBinding)}


def test_claim_candidate_has_no_evidence_truth_or_knowledge_fields() -> None:
    assert {field.name for field in fields(ClaimCandidate)} == {
        "occurrence",
        "content",
        "content_manifest",
        "content_id",
    }
