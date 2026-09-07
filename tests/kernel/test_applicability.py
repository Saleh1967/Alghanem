"""Constitutional tests for G0.EA.1."""

import pytest

from alghanem.kernel import (
    Anchor,
    ApplicabilityAssessmentGate,
    ApplicabilityAssessmentSpecification,
    ApplicabilityAssessmentStatus,
    ApplicabilityModelResult,
    AuthenticatedObservationBinding,
    CanonicalClaimContentEncoder,
    ClaimCandidate,
    ClaimContentManifest,
    ClaimCore,
    ClaimOccurrenceRef,
    ClaimPolarity,
    ClaimScopeRef,
    EvidenceApplicabilityAssessment,
    EvidenceRoleCandidate,
    EvidenceRoleRef,
    FrozenApplicabilityModel,
    PredicateRef,
    Residual,
    Trace,
)


def candidate() -> EvidenceRoleCandidate:
    content = ClaimContentManifest(
        core=ClaimCore(
            anchor=Anchor("maqayis-naql", "lexicon"),
            predicate=PredicateRef("source-says"),
            polarity=ClaimPolarity.AFFIRM,
            scope=ClaimScopeRef("work-entry", "naqala"),
        )
    )
    claim = ClaimCandidate(
        occurrence=ClaimOccurrenceRef("occurrence"),
        content=content,
        content_manifest=CanonicalClaimContentEncoder.encode(content),
    )
    return EvidenceRoleCandidate(
        AuthenticatedObservationBinding.__new__(AuthenticatedObservationBinding),
        claim,
        EvidenceRoleRef("source-attestation"),
    )


def result(status: ApplicabilityAssessmentStatus) -> ApplicabilityModelResult:
    return ApplicabilityModelResult(
        status=status,
        reason=status.value,
        trace=Trace(("model checked",)),
        residuals=(
            (Residual("unresolved historical scope"),)
            if status is ApplicabilityAssessmentStatus.DEFER
            else ()
        ),
    )


def test_assessment_aggregates_models_without_claiming_sufficiency() -> None:
    observed = candidate()
    specification = ApplicabilityAssessmentSpecification(
        (
            FrozenApplicabilityModel("source-attestation", lambda _: result(ApplicabilityAssessmentStatus.PASS)),
            FrozenApplicabilityModel(
                "historical-proof",
                lambda _: result(ApplicabilityAssessmentStatus.DEFER),
                weaker_model_ids=("source-attestation",),
            ),
        )
    )

    assessment = ApplicabilityAssessmentGate.assess(observed, specification)

    assert assessment.status is ApplicabilityAssessmentStatus.DEFER
    assert assessment.scope == observed.claim.content.core.scope
    assert assessment.residuals
    assert not hasattr(assessment, "sufficient")
    assert not hasattr(assessment, "truth")


def test_block_precedes_defer_and_assessments_cannot_be_fabricated() -> None:
    specification = ApplicabilityAssessmentSpecification(
        (
            FrozenApplicabilityModel("source", lambda _: result(ApplicabilityAssessmentStatus.BLOCK)),
            FrozenApplicabilityModel("history", lambda _: result(ApplicabilityAssessmentStatus.DEFER)),
        )
    )
    assessment = ApplicabilityAssessmentGate.assess(candidate(), specification)
    assert assessment.status is ApplicabilityAssessmentStatus.BLOCK
    with pytest.raises(ValueError, match="issued by"):
        EvidenceApplicabilityAssessment(
            candidate(),
            ApplicabilityAssessmentStatus.PASS,
            "fabricated",
            candidate().claim.content.core.scope,
            Trace(("fabricated",)),
            (),
        )


def test_weaker_model_graph_must_be_frozen_and_acyclic() -> None:
    with pytest.raises(ValueError, match="acyclic"):
        ApplicabilityAssessmentSpecification(
            (
                FrozenApplicabilityModel("a", lambda _: result(ApplicabilityAssessmentStatus.PASS), ("b",)),
                FrozenApplicabilityModel("b", lambda _: result(ApplicabilityAssessmentStatus.PASS), ("a",)),
            )
        )
