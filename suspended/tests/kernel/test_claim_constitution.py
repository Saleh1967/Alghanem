"""Constitutional tests for G0.C.1's evidence-free claim candidates."""

from dataclasses import fields
from typing import cast

import pytest

from alghanem.kernel import (
    Anchor,
    CanonicalClaimContentEncoder,
    CanonicalClaimContentManifest,
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


def projection(claim_core: ClaimCore, deleted: str) -> tuple[object, ...]:
    return tuple(
        value
        for name, value in (
            ("anchor", claim_core.anchor),
            ("predicate", claim_core.predicate),
            ("polarity", claim_core.polarity),
            ("scope", claim_core.scope),
        )
        if name != deleted
    )


@pytest.mark.parametrize(
    ("algorithm", "version", "digest"),
    [
        ("sha1", "claim-content-manifest-v1", "0" * 64),
        ("sha256", "other-version", "0" * 64),
        ("sha256", "claim-content-manifest-v1", "0" * 63),
        ("sha256", "claim-content-manifest-v1", "g" * 64),
    ],
)
def test_content_identity_rejects_invalid_encoder_issued_values(
    algorithm: str, version: str, digest: str
) -> None:
    with pytest.raises(ValueError, match="invalid claim content identity"):
        ClaimContentIdentity(
            algorithm,
            version,
            digest,
            _token=claim_constitution._CLAIM_CONTENT_TOKEN,
        )


@pytest.mark.parametrize(
    ("field", "invalid"),
    [
        ("anchor", cast(Anchor, "not-an-anchor")),
        ("predicate", cast(PredicateRef, "not-a-predicate-reference")),
        ("polarity", cast(ClaimPolarity, "not-a-polarity")),
        ("scope", cast(ClaimScopeRef, "not-a-scope-reference")),
    ],
)
def test_claim_core_rejects_wrong_typed_fields(field: str, invalid: object) -> None:
    baseline = core()
    values: dict[str, object] = {
        "anchor": baseline.anchor,
        "predicate": baseline.predicate,
        "polarity": baseline.polarity,
        "scope": baseline.scope,
    }
    values[field] = invalid

    with pytest.raises(TypeError, match="claim core requires"):
        ClaimCore(**values)  # type: ignore[arg-type]


def test_content_manifest_and_candidate_reject_wrong_typed_fields() -> None:
    valid_content = content()
    valid_manifest = CanonicalClaimContentEncoder.encode(valid_content)

    with pytest.raises(TypeError, match="claim content requires"):
        ClaimContentManifest(core=cast(ClaimCore, "not-a-core"))
    with pytest.raises(TypeError, match="claim qualifications must"):
        ClaimContentManifest(
            core=core(),
            qualifications=cast(
                tuple[ClaimQualification, ...], ("not-a-qualification",)
            ),
        )
    with pytest.raises(TypeError, match="claim candidate requires"):
        ClaimCandidate(
            occurrence=cast(ClaimOccurrenceRef, "not-an-occurrence"),
            content=valid_content,
            content_manifest=valid_manifest,
        )
    with pytest.raises(TypeError, match="claim candidate requires"):
        ClaimCandidate(
            occurrence=ClaimOccurrenceRef("claim-1"),
            content=cast(ClaimContentManifest, "not-content"),
            content_manifest=valid_manifest,
        )
    with pytest.raises(TypeError, match="claim candidate requires"):
        ClaimCandidate(
            occurrence=ClaimOccurrenceRef("claim-1"),
            content=valid_content,
            content_manifest=cast(CanonicalClaimContentManifest, "not-a-manifest"),
        )


@pytest.mark.parametrize(
    ("deleted", "distinct"),
    [
        (
            "anchor",
            core(
                anchor=Anchor(
                    identifier="Saleh1967/Alghanem@62755d8",
                    domain="repository",
                )
            ),
        ),
        ("predicate", core(predicate=PredicateRef("other-predicate"))),
        ("polarity", core(polarity=ClaimPolarity.NEGATE)),
        ("scope", core(scope=ClaimScopeRef("repository", "Saleh1967/Alghanem"))),
    ],
    ids=["anchor", "predicate", "polarity", "scope"],
)
def test_deleting_each_core_field_collapses_distinct_claims(
    deleted: str, distinct: ClaimCore
) -> None:
    baseline = core()

    assert baseline != distinct
    assert projection(baseline, deleted) == projection(distinct, deleted)


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


@pytest.mark.parametrize(
    "coverage_name",
    [
        "CLAIM_CONTENT_MANIFEST_COVERAGE",
        "CLAIM_CORE_COVERAGE",
        "ANCHOR_COVERAGE",
        "PREDICATE_REF_COVERAGE",
        "CLAIM_SCOPE_REF_COVERAGE",
        "CLAIM_QUALIFICATION_COVERAGE",
    ],
)
def test_schema_coverage_rejects_unaccounted_identity_bearing_fields(
    monkeypatch: pytest.MonkeyPatch,
    coverage_name: str,
) -> None:
    coverage = getattr(claim_constitution, coverage_name)
    monkeypatch.setattr(claim_constitution, coverage_name, coverage[:-1])

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
