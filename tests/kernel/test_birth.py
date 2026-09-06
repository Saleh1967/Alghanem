import pytest

import alghanem.kernel.birth as birth
from alghanem.kernel.birth import (
    BirthAssessmentRequest,
    BirthAssessmentSemantics,
    BirthExperimentSpecification,
    BirthExperimentSpecificationError,
    BirthQuery,
    ClosureAssessmentStatus,
    ClosureCriterionSpec,
    EvidenceMode,
    EvidenceSnapshot,
    ProjectionPoset,
    ResidualDefinitionSpec,
    StructureHypothesis,
    WeakerModelSpec,
)


def specification() -> BirthExperimentSpecification:
    return BirthExperimentSpecification(
        experiment_id="experiment",
        revision_id="r1",
        revision_sequence=1,
        evidence_mode=EvidenceMode.FORMAL,
        domain="finite-domain",
        projection_poset=ProjectionPoset(
            ("count", "set", "multiset", "sequence", "unicode"),
            (("count", "multiset"), ("set", "multiset"), ("multiset", "sequence")),
        ),
        birth_query=BirthQuery(
            "query",
            StructureHypothesis("structure", "a structure is necessary"),
            "sequence",
        ),
        residual_definition="unexplained distinction",
        closure_criterion="all prerequisite models fail to close the residual",
        evidence_requirements="exhaustive proof over the finite domain",
    )


def residual_definition() -> ResidualDefinitionSpec:
    return ResidualDefinitionSpec(
        residual_id="residual",
        domain="finite-domain",
        input_projection="sequence",
        output_schema="residual-schema",
        evaluator_id="residual-evaluator",
        invariants=("total-domain-coverage",),
        failure_semantics="malformed residual inputs defer assessment",
    )


def weaker_model_specs() -> tuple[WeakerModelSpec, ...]:
    return (
        WeakerModelSpec(
            model_id="count",
            domain="finite-domain",
            projection_evaluator_id="count-evaluator",
            declared_information_loss="forgets identity and order",
            result_schema="projection-result",
            strict_predecessors=(),
            strict_successors=("multiset", "sequence"),
        ),
        WeakerModelSpec(
            model_id="set",
            domain="finite-domain",
            projection_evaluator_id="set-evaluator",
            declared_information_loss="forgets multiplicity and order",
            result_schema="projection-result",
            strict_predecessors=(),
            strict_successors=("multiset", "sequence"),
        ),
        WeakerModelSpec(
            model_id="multiset",
            domain="finite-domain",
            projection_evaluator_id="multiset-evaluator",
            declared_information_loss="forgets order",
            result_schema="projection-result",
            strict_predecessors=("count", "set"),
            strict_successors=("sequence",),
        ),
    )


def closure_criterion() -> ClosureCriterionSpec:
    return ClosureCriterionSpec(
        criterion_id="closure",
        residual_id="residual",
        domain="finite-domain",
        residual_schema="residual-schema",
        model_result_schema="projection-result",
        evaluator_id="closure-evaluator",
        failure_semantics="untestable closure inputs defer assessment",
    )


def assessment_semantics() -> BirthAssessmentSemantics:
    return BirthAssessmentSemantics(
        specification=specification(),
        residual_definition=residual_definition(),
        weaker_models=weaker_model_specs(),
        closure_criterion=closure_criterion(),
    )


def test_specification_derives_models_without_treating_them_as_ontology() -> None:
    spec = specification()

    assert spec.birth_query.hypothesis.hypothesis_id == "structure"
    assert spec.birth_query.test_model == "sequence"
    assert spec.prerequisite_cone == ("count", "set", "multiset")
    assert spec.frozen_weaker_models == spec.prerequisite_cone
    assert spec.competing_projections == ("unicode",)


@pytest.mark.parametrize(
    ("projections", "relations", "message"),
    [
        (("one", "two"), (("one", "missing"),), "declared projections"),
        (("one", "two"), (("one", "two"), ("one", "two")), "duplicates"),
        (("one", "two"), (("one", "two"), ("two", "one")), "cycles"),
    ],
)
def test_projection_poset_rejects_malformed_relations(
    projections: tuple[str, ...],
    relations: tuple[tuple[str, str], ...],
    message: str,
) -> None:
    with pytest.raises(BirthExperimentSpecificationError, match=message):
        ProjectionPoset(projections, relations)


def test_g0_1_exports_no_birth_authority_or_freeze() -> None:
    assert not hasattr(birth, "BirthVerdict")
    assert not hasattr(birth, "BirthFreeze")
    assert not hasattr(birth, "BirthRevisionHistory")
    assert not hasattr(birth, "CompetingExplanation")
    assert not hasattr(birth, "BirthGate")
    assert not hasattr(birth, "NecessaryInvariantCandidate")


def test_assessment_request_binds_evidence_after_frozen_specification() -> None:
    request = BirthAssessmentRequest(
        specification(), EvidenceSnapshot("snapshot", "enumeration")
    )

    assert request.evidence_snapshot.snapshot_id == "snapshot"


@pytest.mark.parametrize("specification_value", (None, "not-a-specification"))
def test_malformed_assessment_request_cannot_enter_future_runtime(
    specification_value: object,
) -> None:
    with pytest.raises(BirthExperimentSpecificationError, match="specification"):
        BirthAssessmentRequest(
            specification_value,  # type: ignore[arg-type]
            EvidenceSnapshot("snapshot", "enumeration"),
        )


@pytest.mark.parametrize("evidence_value", (None, "not-an-evidence-snapshot"))
def test_request_requires_a_real_evidence_snapshot(evidence_value: object) -> None:
    with pytest.raises(BirthExperimentSpecificationError, match="evidence snapshot"):
        BirthAssessmentRequest(
            specification(),
            evidence_value,  # type: ignore[arg-type]
        )


def test_g0_2a_binds_executable_semantics_without_birth_verdict() -> None:
    semantics = assessment_semantics()

    assert semantics.residual_definition.input_projection == "sequence"
    assert tuple(model.model_id for model in semantics.weaker_models) == (
        "count",
        "set",
        "multiset",
    )
    assert semantics.closure_criterion.supported_statuses == (
        ClosureAssessmentStatus.CLOSE,
        ClosureAssessmentStatus.FAIL_TO_CLOSE,
        ClosureAssessmentStatus.DEFER,
    )
    assert not hasattr(semantics, "verdict")


def test_executable_semantics_require_residual_domain_to_match_spec() -> None:
    with pytest.raises(BirthExperimentSpecificationError, match="domain"):
        BirthAssessmentSemantics(
            specification=specification(),
            residual_definition=ResidualDefinitionSpec(
                residual_id="residual",
                domain="other-domain",
                input_projection="sequence",
                output_schema="residual-schema",
                evaluator_id="residual-evaluator",
                invariants=("total-domain-coverage",),
                failure_semantics="malformed residual inputs defer assessment",
            ),
            weaker_models=weaker_model_specs(),
            closure_criterion=closure_criterion(),
        )


def test_executable_semantics_require_exact_weaker_cone_coverage() -> None:
    with pytest.raises(BirthExperimentSpecificationError, match="prerequisite cone"):
        BirthAssessmentSemantics(
            specification=specification(),
            residual_definition=residual_definition(),
            weaker_models=weaker_model_specs()[:-1],
            closure_criterion=closure_criterion(),
        )


def test_executable_semantics_reject_weaker_model_relation_mismatch() -> None:
    weaker_models = weaker_model_specs()
    malformed = WeakerModelSpec(
        model_id="multiset",
        domain="finite-domain",
        projection_evaluator_id="multiset-evaluator",
        declared_information_loss="forgets order",
        result_schema="projection-result",
        strict_predecessors=("count",),
        strict_successors=("sequence",),
    )

    with pytest.raises(BirthExperimentSpecificationError, match="predecessor"):
        BirthAssessmentSemantics(
            specification=specification(),
            residual_definition=residual_definition(),
            weaker_models=(*weaker_models[:2], malformed),
            closure_criterion=closure_criterion(),
        )


def test_executable_semantics_bind_closure_to_residual_schema() -> None:
    with pytest.raises(BirthExperimentSpecificationError, match="residual schema"):
        BirthAssessmentSemantics(
            specification=specification(),
            residual_definition=residual_definition(),
            weaker_models=weaker_model_specs(),
            closure_criterion=ClosureCriterionSpec(
                criterion_id="closure",
                residual_id="residual",
                domain="finite-domain",
                residual_schema="other-schema",
                model_result_schema="projection-result",
                evaluator_id="closure-evaluator",
                failure_semantics="untestable closure inputs defer assessment",
            ),
        )
