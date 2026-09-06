import pytest

from alghanem.kernel.birth import (
    BirthExperimentSpecification,
    BirthQuery,
    EvidenceMode,
    ProjectionPoset,
    StructureHypothesis,
)
from alghanem.kernel.experiment_spec_content_identity import (
    BirthExperimentContentIdentityError,
    BirthExperimentSpecificationContentBinding,
    BirthExperimentSpecificationContentIdentity,
    CanonicalBirthExperimentSpecificationEncoder,
    FrozenPreEvidenceExperimentManifest,
    PreEvidenceSpecificationRegistry,
)


def specification(*, hypothesis: str = "a structure is necessary"):
    return BirthExperimentSpecification(
        experiment_id="experiment",
        revision_id="r1",
        revision_sequence=1,
        evidence_mode=EvidenceMode.FORMAL,
        domain="finite-domain",
        projection_poset=ProjectionPoset(
            ("count", "multiset", "sequence"), (("count", "multiset"),)
        ),
        birth_query=BirthQuery(
            "query", StructureHypothesis("structure", hypothesis), "sequence"
        ),
        residual_definition_id="residual",
        residual_definition="unexplained distinction",
        closure_criterion_id="closure",
        closure_criterion="all prerequisite models fail",
        evidence_requirements="exhaustive proof",
    )


def test_canonical_experiment_manifest_covers_nested_declared_content() -> None:
    baseline = CanonicalBirthExperimentSpecificationEncoder.encode(specification())
    drifted = CanonicalBirthExperimentSpecificationEncoder.encode(
        specification(hypothesis="a different structure is necessary")
    )

    assert baseline.canonical_bytes != drifted.canonical_bytes
    assert baseline.content_id.digest != drifted.content_id.digest


def test_pre_evidence_registry_rejects_content_drift_for_same_scope() -> None:
    registry = PreEvidenceSpecificationRegistry()
    frozen = registry.freeze(
        CanonicalBirthExperimentSpecificationEncoder.encode(specification())
    )

    with pytest.raises(BirthExperimentContentIdentityError, match="pre-evidence"):
        registry.freeze(
            CanonicalBirthExperimentSpecificationEncoder.encode(
                specification(hypothesis="different hypothesis")
            )
        )

    assert frozen.content_id.digest


def test_experiment_content_binding_requires_exact_frozen_bytes() -> None:
    frozen = PreEvidenceSpecificationRegistry().freeze(
        CanonicalBirthExperimentSpecificationEncoder.encode(specification())
    )

    binding = BirthExperimentSpecificationContentBinding(specification(), frozen)
    assert binding.content_id == frozen.content_id

    with pytest.raises(BirthExperimentContentIdentityError, match="does not match"):
        BirthExperimentSpecificationContentBinding(
            specification(hypothesis="different hypothesis"), frozen
        )


def test_experiment_identity_and_frozen_manifest_cannot_be_hand_constructed() -> None:
    with pytest.raises(BirthExperimentContentIdentityError, match="issued by"):
        BirthExperimentSpecificationContentIdentity(
            "sha256", "birth-experiment-specification-manifest-v1", "0" * 64
        )
    with pytest.raises(BirthExperimentContentIdentityError, match="registry-issued"):
        FrozenPreEvidenceExperimentManifest(
            CanonicalBirthExperimentSpecificationEncoder.encode(specification())
        )
