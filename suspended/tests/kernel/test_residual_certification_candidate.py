import pytest

from alghanem.kernel import (
    AuthenticatedObservationBinding,
    Residual,
    ResidualCertificationCandidate,
    ResidualCertificationError,
    Trace,
)
from alghanem.kernel._internal.authenticated_observation_bridge import (
    issue_from_source_authority,
)
from alghanem.kernel.birth import (
    BirthAssessmentSemanticsContract,
    BirthEvaluatorRole,
    BirthExperimentSpecification,
    BirthQuery,
    ClosureCriterionSpec,
    EvidenceMode,
    ProjectionPoset,
    ResidualDefinitionSpec,
    StructureHypothesis,
    WeakerModelSpec,
)
from alghanem.kernel.birth_content_identity import (
    BirthAssessmentContentBinding,
    BirthSemanticsContentRegistry,
    CanonicalBirthSemanticsEncoder,
)
from alghanem.kernel.experiment_spec_content_identity import (
    CanonicalBirthExperimentSpecificationEncoder,
    PreEvidenceSpecificationRegistry,
)
from alghanem.kernel.fractal import FrozenFactorRef


def specification() -> BirthExperimentSpecification:
    return BirthExperimentSpecification(
        "experiment",
        "r1",
        1,
        EvidenceMode.FORMAL,
        "domain",
        ProjectionPoset(("base", "input"), (("base", "input"),)),
        BirthQuery("query", StructureHypothesis("hypothesis", "statement"), "input"),
        "residual",
        "residual definition",
        "closure",
        "closure criterion",
        "formal evidence",
    )


def residual_definition(*, output_schema: str = "schema") -> ResidualDefinitionSpec:
    return ResidualDefinitionSpec(
        "residual",
        "domain",
        "input",
        output_schema,
        "evaluator",
        ("coverage",),
        "defer malformed inputs",
    )


def binding(
    definition: ResidualDefinitionSpec | None = None,
) -> BirthAssessmentContentBinding:
    definition = definition or residual_definition()
    contract = BirthAssessmentSemanticsContract(
        specification=specification(),
        residual_definition=definition,
        weaker_models=(
            WeakerModelSpec(
                "base",
                "domain",
                "projection-evaluator",
                "declared loss",
                "result",
                (),
                ("input",),
            ),
        ),
        closure_criterion=ClosureCriterionSpec(
            "closure",
            "residual",
            "domain",
            definition.output_schema,
            "result",
            "closure-evaluator",
            "defer malformed inputs",
        ),
    )
    registry = BirthSemanticsContentRegistry()
    registry.freeze(
        domain="domain",
        role=BirthEvaluatorRole.RESIDUAL_DEFINITION,
        target_id="residual",
        manifest=CanonicalBirthSemanticsEncoder.encode_residual_definition(definition),
    )
    registry.freeze(
        domain="domain",
        role=BirthEvaluatorRole.WEAKER_MODEL,
        target_id="base",
        manifest=CanonicalBirthSemanticsEncoder.encode_weaker_model(
            contract.weaker_models[0]
        ),
    )
    registry.freeze(
        domain="domain",
        role=BirthEvaluatorRole.CLOSURE_CRITERION,
        target_id="closure",
        manifest=CanonicalBirthSemanticsEncoder.encode_closure_criterion(
            contract.closure_criterion
        ),
    )
    experiment = PreEvidenceSpecificationRegistry().freeze(
        CanonicalBirthExperimentSpecificationEncoder.encode(specification())
    )
    return BirthAssessmentContentBinding(
        contract, registry.seal("snapshot", experiment)
    )


def parent() -> FrozenFactorRef:
    return FrozenFactorRef("factor", "content", "certificate", "domain", "birth", "r1")


def observation() -> AuthenticatedObservationBinding:
    return issue_from_source_authority("observation", "authentication")


def candidate(
    content_binding: BirthAssessmentContentBinding | None = None,
) -> ResidualCertificationCandidate:
    return ResidualCertificationCandidate(
        "occurrence",
        parent(),
        observation(),
        "scope",
        content_binding or binding(),
        "attempt",
        "comparison",
        Trace(("observe", "reconstruct", "compare")),
    )


def test_candidate_derives_definition_and_identity_from_sealed_binding() -> None:
    result = candidate()

    assert (
        result.residual_definition
        is result.birth_content_binding.contract.residual_definition
    )
    assert (
        result.residual_definition_content_id
        is result.birth_content_binding.residual_definition_content_id
    )


def test_definition_cannot_be_paired_with_another_frozen_identity() -> None:
    definition_a = residual_definition()
    definition_b = residual_definition(output_schema="different-schema")
    binding_a = binding(definition_a)
    binding_b = binding(definition_b)

    with pytest.raises(AssertionError):
        assert (
            binding_a.residual_definition_content_id
            == binding_b.residual_definition_content_id
        )
    assert (
        candidate(binding_a).residual_definition
        != candidate(binding_b).residual_definition
    )


def test_legacy_residual_has_no_certification_authority() -> None:
    assert isinstance(Residual("legacy remainder"), Residual)
    assert not isinstance(Residual("legacy remainder"), ResidualCertificationCandidate)


def test_candidate_requires_a_sealed_binding() -> None:
    with pytest.raises(ResidualCertificationError):
        ResidualCertificationCandidate(
            "occurrence",
            parent(),
            observation(),
            "scope",
            "not-a-binding",  # type: ignore[arg-type]
            "attempt",
            "comparison",
            Trace(("compare",)),
        )
