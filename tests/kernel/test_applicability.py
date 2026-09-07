"""Constitutional tests for G0.EA.1."""

import pytest

from alghanem.encyclopedia.self_observation import (
    RepositoryArtifactRef,
    RepositoryObservationAuthority,
    RepositorySnapshotRef,
)
from alghanem.kernel import (
    Anchor,
    ApplicabilityAssessmentGate,
    ApplicabilityAssessmentSpecification,
    ApplicabilityAssessmentStatus,
    ApplicabilityEvaluatorRegistry,
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


class SourceProvider:
    provider_identity = "test-provider"
    implementation_identity = "test-implementation"
    protocol_version = "1"

    def resolve_repository(self, repository_identity: str) -> object | None:
        return repository_identity

    def resolve_commit(self, repository: object, commit_sha: str) -> object | None:
        return commit_sha

    def tree_for_commit(self, commit: object) -> str | None:
        return "tree-1"

    def blob_at_path(self, tree_sha: str, artifact_path: str) -> str | None:
        return "blob-1"

    def fragment_from_blob(self, blob_sha: str, fragment_locator: str) -> str | None:
        return f"{blob_sha}/{fragment_locator}"

    def is_ancestor(
        self, repository: object, from_commit_sha: str, to_commit_sha: str
    ) -> bool:
        return False


def observation() -> AuthenticatedObservationBinding:
    run = RepositoryObservationAuthority(SourceProvider()).open_run()
    snapshot = run.observe_snapshot(
        RepositorySnapshotRef("lexicon-source", "commit-1", "tree-1")
    )
    artifact = run.observe_artifact(
        snapshot, RepositoryArtifactRef(snapshot.snapshot, "maqayis-naql", "blob-1")
    )
    return run.bridge_authenticated_fragment(run.observe_fragment(artifact, "entry"))


def claim(
    predicate: str,
    role: str,
    binding: AuthenticatedObservationBinding | None = None,
) -> EvidenceRoleCandidate:
    content = ClaimContentManifest(
        core=ClaimCore(
            anchor=Anchor("ibn-faris:maqayis-naql", "lexicon"),
            predicate=PredicateRef(predicate),
            polarity=ClaimPolarity.AFFIRM,
            scope=ClaimScopeRef("work-entry", "naqala"),
        )
    )
    asserted_claim = ClaimCandidate(
        ClaimOccurrenceRef(f"{predicate}-occurrence"),
        content,
        CanonicalClaimContentEncoder.encode(content),
    )
    return EvidenceRoleCandidate(
        binding or observation(), asserted_claim, EvidenceRoleRef(role)
    )


def result(
    status: ApplicabilityAssessmentStatus,
    residuals: tuple[Residual, ...] = (),
) -> ApplicabilityModelResult:
    return ApplicabilityModelResult(
        status, status.value, Trace(("model checked",)), residuals
    )


def assess(candidate: EvidenceRoleCandidate, status: ApplicabilityAssessmentStatus):
    registry = ApplicabilityEvaluatorRegistry()
    registry.register(
        "maqayis-evaluator",
        "implementation-v1",
        candidate.role.identifier,
        candidate.claim.content.core.scope,
        lambda _: result(
            status,
            (Residual("historical proof remains unresolved"),)
            if status is ApplicabilityAssessmentStatus.DEFER
            else (),
        ),
    )
    sealed = registry.seal("registry-1")
    specification = ApplicabilityAssessmentSpecification(
        (FrozenApplicabilityModel("model", "maqayis-evaluator"),)
    )
    return ApplicabilityAssessmentGate.assess(candidate, specification, sealed)


def test_maqayis_source_attestation_and_historical_proof_are_independent() -> None:
    observed = observation()
    source = claim("source-says-origin", "source-attestation", observed)
    historical = claim("historical-origin", "historical-origin-proof", observed)

    source_assessment = assess(source, ApplicabilityAssessmentStatus.PASS)
    historical_assessment = assess(historical, ApplicabilityAssessmentStatus.DEFER)

    assert source_assessment.status is ApplicabilityAssessmentStatus.PASS
    assert historical_assessment.status is ApplicabilityAssessmentStatus.DEFER
    assert source_assessment.candidate.authenticated_observation_binding == (
        historical_assessment.candidate.authenticated_observation_binding
    )
    assert historical_assessment.residuals


def test_weakest_closing_model_is_not_worst_status_aggregation() -> None:
    candidate = claim("source-says-origin", "source-attestation")
    registry = ApplicabilityEvaluatorRegistry()
    scope = candidate.claim.content.core.scope
    registry.register(
        "weak",
        "implementation-v1",
        candidate.role.identifier,
        scope,
        lambda _: result(ApplicabilityAssessmentStatus.PASS),
    )
    registry.register(
        "strong",
        "implementation-v2",
        candidate.role.identifier,
        scope,
        lambda _: result(
            ApplicabilityAssessmentStatus.DEFER,
            (Residual("stronger unresolved boundary"),),
        ),
    )
    registry.register(
        "strongest",
        "implementation-v3",
        candidate.role.identifier,
        scope,
        lambda _: result(
            ApplicabilityAssessmentStatus.DEFER,
            (Residual("strongest unresolved boundary"),),
        ),
    )
    sealed = registry.seal("registry-1")
    specification = ApplicabilityAssessmentSpecification(
        (
            FrozenApplicabilityModel("weak-model", "weak"),
            FrozenApplicabilityModel("strong-model", "strong", ("weak-model",)),
            FrozenApplicabilityModel(
                "strongest-model", "strongest", ("strong-model",)
            ),
        )
    )

    assessment = ApplicabilityAssessmentGate.assess(candidate, specification, sealed)

    assert assessment.status is ApplicabilityAssessmentStatus.PASS
    assert not assessment.residuals
    assert [model_id for model_id, _ in assessment.model_results] == [
        "weak-model",
        "strong-model",
        "strongest-model",
    ]
    assert assessment.specification_id
    assert assessment.registry_snapshot_id == "registry-1"


def test_status_residual_consistency_and_authorized_scope() -> None:
    with pytest.raises(ValueError, match="cannot retain residuals"):
        result(ApplicabilityAssessmentStatus.PASS, (Residual("unresolved"),))
    with pytest.raises(ValueError, match="require residuals"):
        result(ApplicabilityAssessmentStatus.DEFER)

    candidate = claim("source-says-origin", "source-attestation")
    registry = ApplicabilityEvaluatorRegistry()
    registry.register(
        "wrong-role",
        "implementation-v1",
        "historical-origin-proof",
        candidate.claim.content.core.scope,
        lambda _: result(ApplicabilityAssessmentStatus.PASS),
    )
    with pytest.raises(ValueError, match="not authorized"):
        ApplicabilityAssessmentGate.assess(
            candidate,
            ApplicabilityAssessmentSpecification(
                (FrozenApplicabilityModel("model", "wrong-role"),)
            ),
            registry.seal("registry-1"),
        )


def test_block_is_preserved_when_no_model_closes() -> None:
    candidate = claim("historical-origin", "historical-origin-proof")
    registry = ApplicabilityEvaluatorRegistry()
    scope = candidate.claim.content.core.scope
    registry.register(
        "blocked",
        "implementation-v1",
        candidate.role.identifier,
        scope,
        lambda _: result(ApplicabilityAssessmentStatus.BLOCK),
    )
    registry.register(
        "deferred",
        "implementation-v2",
        candidate.role.identifier,
        scope,
        lambda _: result(
            ApplicabilityAssessmentStatus.DEFER,
            (Residual("unresolved historical scope"),),
        ),
    )
    assessment = ApplicabilityAssessmentGate.assess(
        candidate,
        ApplicabilityAssessmentSpecification(
            (
                FrozenApplicabilityModel("blocked-model", "blocked"),
                FrozenApplicabilityModel(
                    "deferred-model", "deferred", ("blocked-model",)
                ),
            )
        ),
        registry.seal("registry-1"),
    )

    assert assessment.status is ApplicabilityAssessmentStatus.BLOCK


def test_assessment_cannot_be_fabricated_and_models_are_content_bound() -> None:
    candidate = claim("source-says-origin", "source-attestation")
    with pytest.raises(ValueError, match="issued by"):
        EvidenceApplicabilityAssessment(
            candidate,
            ApplicabilityAssessmentStatus.PASS,
            "fabricated",
            candidate.claim.content.core.scope,
            Trace(("fabricated",)),
            (),
            "specification",
            "registry",
            "registry-hash",
        )

    first = ApplicabilityAssessmentSpecification(
        (FrozenApplicabilityModel("model", "evaluator-1"),)
    )
    second = ApplicabilityAssessmentSpecification(
        (FrozenApplicabilityModel("model", "evaluator-2"),)
    )
    assert first.specification_id != second.specification_id
