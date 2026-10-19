"""G0.IC.1e: composing three derived conjunct readings, and refusing to overstate.

Comparability is two-valued and exhaustion and survival are three-valued, so the
composition has exactly `2 x 3 x 3 = 18` combinations. All eighteen are asserted
here by name, together with the binding rules that decide which readings may be
composed at all.
"""

import itertools

import pytest

from alghanem.kernel.birth import (
    AuthorizedBirthAssessmentEvaluatorDefinition,
    BirthAssessmentEvaluatorRegistry,
    BirthAssessmentRequest,
    BirthAssessmentSemanticsContract,
    BirthEvaluatorRole,
    BirthExperimentSpecification,
    BirthQuery,
    ClosureAssessmentStatus,
    ClosureCriterionSpec,
    EvidenceMode,
    ProjectionPoset,
    ResidualDefinitionSpec,
    ResidualSurvivalStatus,
    StructureHypothesis,
    WeakerModelSpec,
)
from alghanem.kernel.birth_content_identity import (
    BirthAssessmentContentBinding,
    BirthSemanticsContentRegistry,
    CanonicalBirthSemanticsEncoder,
)
from alghanem.kernel.evaluator_execution import (
    BirthEvaluatorImplementationRegistry,
    SealedBirthEvaluatorImplementationRegistry,
)
from alghanem.kernel.evaluator_input_provenance import (
    EvaluatorInputDerivationGate,
    EvaluatorInputDerivationRegistry,
    EvidenceDerivedEvaluatorInput,
    ProvenanceBoundEvaluatorExecutionGate,
    ProvenanceBoundEvaluatorExecutionRecord,
)
from alghanem.kernel.evidence_acquisition import EvidenceAcquisitionAuthority
from alghanem.kernel.experiment_spec_content_identity import (
    BirthExperimentSpecificationContentBinding,
    CanonicalBirthExperimentSpecificationEncoder,
    PreEvidenceSpecificationRegistry,
)
from alghanem.kernel.independent_closure import (
    ClosureScopeRegistry,
    ComparabilityClosureStatus,
    IndependentClosureAssessment,
    IndependentClosureGate,
)
from alghanem.kernel.independent_closure_composition import (
    IndependentClosureCompositionError,
    IndependentClosureCompositionGate,
    IndependentClosureCompositionStatus,
    IndependentClosureConjunct,
    IndependentClosureDecision,
)
from alghanem.kernel.residual_survival import (
    DeclaredResidualSurvivalVocabulary,
    ResidualSurvivalCertificate,
    ResidualSurvivalGate,
    ResidualSurvivalVocabularyRegistry,
    SealedResidualSurvivalVocabularyRegistry,
)
from alghanem.kernel.trace import Trace
from alghanem.kernel.weaker_model_closure import (
    ClosureOutcomeVocabularyRegistry,
    DeclaredClosureOutcomeVocabulary,
    SealedClosureOutcomeVocabularyRegistry,
    WeakerModelClosureCertificate,
    WeakerModelClosureGate,
)
from alghanem.kernel.weaker_model_exhaustion import (
    WeakerModelExhaustionAssessment,
    WeakerModelExhaustionGate,
    WeakerModelExhaustionStatus,
)

CLOSE_TOKEN = "CLOSE:residual-closed-by-this-model"
FAIL_TOKEN = "FAIL_TO_CLOSE:residual-survives-this-model"
CLOSURE_DEFER_TOKEN = "DEFER:inputs-untestable-under-this-model"
SURVIVES_TOKEN = "SURVIVES:residual-unexplained-after-every-licensed-projection"
DOES_NOT_SURVIVE_TOKEN = "DOES_NOT_SURVIVE:residual-explained-away"
SURVIVAL_DEFER_TOKEN = "DEFER:residual-inputs-untestable"

CLOSURE_TOKENS = {
    ClosureAssessmentStatus.CLOSE: CLOSE_TOKEN,
    ClosureAssessmentStatus.FAIL_TO_CLOSE: FAIL_TOKEN,
    ClosureAssessmentStatus.DEFER: CLOSURE_DEFER_TOKEN,
}
SURVIVAL_TOKENS = {
    ResidualSurvivalStatus.SURVIVES: SURVIVES_TOKEN,
    ResidualSurvivalStatus.DOES_NOT_SURVIVE: DOES_NOT_SURVIVE_TOKEN,
    ResidualSurvivalStatus.DEFER: SURVIVAL_DEFER_TOKEN,
}

CONE = ("count", "set", "multiset")
CHAIN_PROJECTIONS = ("count", "set", "multiset", "sequence")
CHAIN_RELATIONS = (
    ("count", "multiset"),
    ("set", "multiset"),
    ("multiset", "sequence"),
)

REFUTED = IndependentClosureCompositionStatus.CLOSURE_REFUTED_IN_SCOPE
UNDETERMINED = IndependentClosureCompositionStatus.CLOSURE_UNDETERMINED_IN_SCOPE
SATISFIED = (
    IndependentClosureCompositionStatus.CONJUNCTS_SATISFIED_PENDING_RESIDUAL_CERTIFICATION  # noqa: E501
)


def specification(
    *, comparable: bool = True, experiment_id: str = "experiment"
) -> BirthExperimentSpecification:
    """A frozen experiment whose poset alone decides the comparability branch.

    The extra `graph` projection is strictly related to nothing, so it is left
    incomparable with the test model without disturbing the derived cone.
    """

    projections = CHAIN_PROJECTIONS if comparable else CHAIN_PROJECTIONS + ("graph",)
    return BirthExperimentSpecification(
        experiment_id=experiment_id,
        revision_id="r1",
        revision_sequence=1,
        evidence_mode=EvidenceMode.FORMAL,
        domain="finite-domain",
        projection_poset=ProjectionPoset(projections, CHAIN_RELATIONS),
        birth_query=BirthQuery(
            "query",
            StructureHypothesis("structure", "a structure is necessary"),
            "sequence",
        ),
        residual_definition_id="residual",
        residual_definition="unexplained distinction",
        closure_criterion_id="closure",
        closure_criterion="all prerequisite models fail to close the residual",
        evidence_requirements="exhaustive proof over the finite domain",
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


def semantics_contract(
    spec: BirthExperimentSpecification,
) -> BirthAssessmentSemanticsContract:
    return BirthAssessmentSemanticsContract(
        specification=spec,
        residual_definition=ResidualDefinitionSpec(
            residual_id=spec.residual_definition_id,
            domain=spec.domain,
            input_projection=spec.birth_query.test_model,
            output_schema="residual-schema",
            evaluator_id="residual-evaluator",
            invariants=("total-domain-coverage",),
            failure_semantics="malformed residual inputs defer assessment",
        ),
        weaker_models=weaker_model_specs(),
        closure_criterion=ClosureCriterionSpec(
            criterion_id=spec.closure_criterion_id,
            residual_id=spec.residual_definition_id,
            domain=spec.domain,
            residual_schema="residual-schema",
            model_result_schema="projection-result",
            evaluator_id="closure-evaluator",
            failure_semantics="untestable closure inputs defer assessment",
        ),
    )


def content_binding(
    spec: BirthExperimentSpecification,
) -> BirthAssessmentContentBinding:
    contract = semantics_contract(spec)
    registry = BirthSemanticsContentRegistry()
    registry.freeze(
        domain=spec.domain,
        role=BirthEvaluatorRole.RESIDUAL_DEFINITION,
        target_id=contract.residual_definition.residual_id,
        manifest=CanonicalBirthSemanticsEncoder.encode_residual_definition(
            contract.residual_definition
        ),
    )
    registry.freeze(
        domain=spec.domain,
        role=BirthEvaluatorRole.CLOSURE_CRITERION,
        target_id=contract.closure_criterion.criterion_id,
        manifest=CanonicalBirthSemanticsEncoder.encode_closure_criterion(
            contract.closure_criterion
        ),
    )
    for model in contract.weaker_models:
        registry.freeze(
            domain=spec.domain,
            role=BirthEvaluatorRole.WEAKER_MODEL,
            target_id=model.model_id,
            manifest=CanonicalBirthSemanticsEncoder.encode_weaker_model(model),
        )
    frozen_experiment = PreEvidenceSpecificationRegistry().freeze(
        CanonicalBirthExperimentSpecificationEncoder.encode(spec)
    )
    return BirthAssessmentContentBinding(
        contract, registry.seal("semantics-snapshot", frozen_experiment)
    )


def sealed_closure_vocabulary(
    spec: BirthExperimentSpecification,
) -> SealedClosureOutcomeVocabularyRegistry:
    registry = ClosureOutcomeVocabularyRegistry()
    registry.register(
        vocabulary_id="closure-vocabulary",
        vocabulary=DeclaredClosureOutcomeVocabulary(
            criterion_id=spec.closure_criterion_id,
            domain=spec.domain,
            tokens=(
                (CLOSE_TOKEN, ClosureAssessmentStatus.CLOSE),
                (FAIL_TOKEN, ClosureAssessmentStatus.FAIL_TO_CLOSE),
                (CLOSURE_DEFER_TOKEN, ClosureAssessmentStatus.DEFER),
            ),
        ),
        binding=content_binding(spec),
    )
    return registry.seal("closure-vocabulary-snapshot")


def sealed_survival_vocabulary(
    spec: BirthExperimentSpecification,
) -> SealedResidualSurvivalVocabularyRegistry:
    registry = ResidualSurvivalVocabularyRegistry()
    registry.register(
        vocabulary_id="residual-vocabulary",
        vocabulary=DeclaredResidualSurvivalVocabulary(
            residual_id=spec.residual_definition_id,
            domain=spec.domain,
            tokens=(
                (SURVIVES_TOKEN, ResidualSurvivalStatus.SURVIVES),
                (DOES_NOT_SURVIVE_TOKEN, ResidualSurvivalStatus.DOES_NOT_SURVIVE),
                (SURVIVAL_DEFER_TOKEN, ResidualSurvivalStatus.DEFER),
            ),
        ),
        binding=content_binding(spec),
    )
    return registry.seal("residual-vocabulary-snapshot")


def frozen_specification_binding(
    spec: BirthExperimentSpecification,
) -> BirthExperimentSpecificationContentBinding:
    frozen = PreEvidenceSpecificationRegistry().freeze(
        CanonicalBirthExperimentSpecificationEncoder.encode(spec)
    )
    return BirthExperimentSpecificationContentBinding(spec, frozen)


def assessment_request(
    binding: BirthExperimentSpecificationContentBinding,
) -> BirthAssessmentRequest:
    authorization = EvidenceAcquisitionAuthority().authorize(
        authorization_id="authorization", binding=binding
    )
    snapshot = authorization.open_run("run").ingest(
        snapshot_id="snapshot", payload="enumeration", trace="acquisition-trace"
    )
    return BirthAssessmentRequest(
        experiment_binding=binding, evidence_snapshot=snapshot
    )


def identity_derivation(source_bytes: bytes) -> str:
    return source_bytes.decode("utf-8", "surrogatepass")


def derived_input(request: BirthAssessmentRequest) -> EvidenceDerivedEvaluatorInput:
    registry = EvaluatorInputDerivationRegistry()
    registry.register(
        domain=request.specification.domain,
        derivation_id="identity",
        implementation_identity="identity-v1",
        declared_transformation="decode the authorized evidence bytes",
        derivation=identity_derivation,
    )
    return EvaluatorInputDerivationGate.derive(
        registry=registry.seal("derivation-snapshot"),
        request=request,
        derivation_id="identity",
        implementation_identity="identity-v1",
    )


def authorized_definition(
    *, role: BirthEvaluatorRole, target_id: str
) -> AuthorizedBirthAssessmentEvaluatorDefinition:
    return BirthAssessmentEvaluatorRegistry().authorize(
        domain="finite-domain",
        role=role,
        target_id=target_id,
        evaluator_id=f"{target_id}-evaluator",
    )


def sealed_implementation_registry(
    definition: AuthorizedBirthAssessmentEvaluatorDefinition, *, output: str
) -> SealedBirthEvaluatorImplementationRegistry:
    def implementation(content: str) -> tuple[str, Trace]:
        return output, Trace(("evaluated",))

    registry = BirthEvaluatorImplementationRegistry()
    registry.register(definition, "impl-v1", implementation)
    return registry.seal("implementation-snapshot")


def provenance_bound_record(
    *,
    request: BirthAssessmentRequest,
    role: BirthEvaluatorRole,
    target_id: str,
    output: str,
) -> ProvenanceBoundEvaluatorExecutionRecord:
    definition = authorized_definition(role=role, target_id=target_id)
    return ProvenanceBoundEvaluatorExecutionGate.execute(
        definition=definition,
        implementation_identity="impl-v1",
        registry=sealed_implementation_registry(definition, output=output),
        derived_input=derived_input(request),
    )


def comparability_for(
    request: BirthAssessmentRequest,
) -> IndependentClosureAssessment:
    registry = ClosureScopeRegistry()
    registry.register(scope_id="scope", binding=request.experiment_binding)
    return IndependentClosureGate.assess(
        registry=registry.seal("scope-snapshot"), request=request
    )


def closure_certificates(
    request: BirthAssessmentRequest, outcomes: dict[str, ClosureAssessmentStatus]
) -> tuple[WeakerModelClosureCertificate, ...]:
    vocabulary = sealed_closure_vocabulary(request.specification)
    return tuple(
        WeakerModelClosureGate.assess(
            registry=vocabulary,
            record=provenance_bound_record(
                request=request,
                role=BirthEvaluatorRole.WEAKER_MODEL,
                target_id=model_id,
                output=CLOSURE_TOKENS[status],
            ),
        )
        for model_id, status in outcomes.items()
    )


def exhaustion_for(
    request: BirthAssessmentRequest, status: WeakerModelExhaustionStatus
) -> WeakerModelExhaustionAssessment:
    outcomes = dict.fromkeys(CONE, ClosureAssessmentStatus.FAIL_TO_CLOSE)
    if status is WeakerModelExhaustionStatus.WEAKER_MODEL_CLOSES_RESIDUAL:
        outcomes["set"] = ClosureAssessmentStatus.CLOSE
    elif status is WeakerModelExhaustionStatus.EXHAUSTION_UNDETERMINED:
        outcomes["set"] = ClosureAssessmentStatus.DEFER
    assessment = WeakerModelExhaustionGate.assess(
        request=request, certificates=closure_certificates(request, outcomes)
    )
    assert assessment.status is status
    return assessment


def survival_for(
    request: BirthAssessmentRequest, status: ResidualSurvivalStatus
) -> ResidualSurvivalCertificate:
    certificate = ResidualSurvivalGate.assess(
        registry=sealed_survival_vocabulary(request.specification),
        record=provenance_bound_record(
            request=request,
            role=BirthEvaluatorRole.RESIDUAL_DEFINITION,
            target_id=request.specification.residual_definition_id,
            output=SURVIVAL_TOKENS[status],
        ),
    )
    assert certificate.status is status
    return certificate


def decision_for(
    comparability: ComparabilityClosureStatus,
    exhaustion: WeakerModelExhaustionStatus,
    survival: ResidualSurvivalStatus,
) -> IndependentClosureDecision:
    resolved = comparability is ComparabilityClosureStatus.COMPETITION_RESOLVED_IN_POSET
    request = assessment_request(
        frozen_specification_binding(specification(comparable=resolved))
    )
    comparability_assessment = comparability_for(request)
    assert comparability_assessment.status is comparability
    return IndependentClosureCompositionGate.assess(
        comparability=comparability_assessment,
        exhaustion=exhaustion_for(request, exhaustion),
        survival=survival_for(request, survival),
    )


def expected_status(
    comparability: ComparabilityClosureStatus,
    exhaustion: WeakerModelExhaustionStatus,
    survival: ResidualSurvivalStatus,
) -> IndependentClosureCompositionStatus:
    """The enumeration, written independently of the gate's own branching."""

    refuting = (
        exhaustion is WeakerModelExhaustionStatus.WEAKER_MODEL_CLOSES_RESIDUAL
    ) or (survival is ResidualSurvivalStatus.DOES_NOT_SURVIVE)
    if refuting:
        return REFUTED
    undetermined = (
        comparability is ComparabilityClosureStatus.COMPETITION_UNRESOLVED_IN_POSET
        or exhaustion is WeakerModelExhaustionStatus.EXHAUSTION_UNDETERMINED
        or survival is ResidualSurvivalStatus.DEFER
    )
    return UNDETERMINED if undetermined else SATISFIED


ALL_COMBINATIONS = tuple(
    itertools.product(
        tuple(ComparabilityClosureStatus),
        tuple(WeakerModelExhaustionStatus),
        tuple(ResidualSurvivalStatus),
    )
)


def test_the_enumeration_is_exactly_eighteen_combinations() -> None:
    assert len(ALL_COMBINATIONS) == 18
    counts = {REFUTED: 0, UNDETERMINED: 0, SATISFIED: 0}
    for combination in ALL_COMBINATIONS:
        counts[expected_status(*combination)] += 1
    assert counts == {REFUTED: 10, UNDETERMINED: 7, SATISFIED: 1}


@pytest.mark.parametrize("combination", ALL_COMBINATIONS)
def test_every_combination_composes_to_its_named_status(
    combination: tuple[
        ComparabilityClosureStatus,
        WeakerModelExhaustionStatus,
        ResidualSurvivalStatus,
    ],
) -> None:
    decision = decision_for(*combination)

    assert decision.status is expected_status(*combination)
    assert decision.reason.strip()
    assert decision.is_independent_closure is False


def test_the_only_satisfied_combination_is_still_not_independent_closure() -> None:
    decision = decision_for(
        ComparabilityClosureStatus.COMPETITION_RESOLVED_IN_POSET,
        WeakerModelExhaustionStatus.LICENSED_WEAKER_MODELS_EXHAUSTED,
        ResidualSurvivalStatus.SURVIVES,
    )

    assert decision.status is SATISFIED
    assert decision.is_independent_closure is False
    assert decision.refuting_conjuncts == ()
    assert decision.undetermined_conjuncts == ()
    assert set(decision.satisfied_conjuncts) == set(IndependentClosureConjunct)
    assert "OneWitnessIsNotResidualCertification" in decision.reason


def test_a_refuting_conjunct_outranks_every_deferral() -> None:
    decision = decision_for(
        ComparabilityClosureStatus.COMPETITION_UNRESOLVED_IN_POSET,
        WeakerModelExhaustionStatus.EXHAUSTION_UNDETERMINED,
        ResidualSurvivalStatus.DOES_NOT_SURVIVE,
    )

    assert decision.status is REFUTED
    assert decision.refuting_conjuncts == (
        IndependentClosureConjunct.RESIDUAL_SURVIVAL,
    )
    assert decision.undetermined_conjuncts == (
        IndependentClosureConjunct.COMPARABILITY,
        IndependentClosureConjunct.WEAKER_MODEL_EXHAUSTION,
    )


def test_unresolved_comparability_is_ignorance_never_refutation() -> None:
    decision = decision_for(
        ComparabilityClosureStatus.COMPETITION_UNRESOLVED_IN_POSET,
        WeakerModelExhaustionStatus.LICENSED_WEAKER_MODELS_EXHAUSTED,
        ResidualSurvivalStatus.SURVIVES,
    )

    assert decision.status is UNDETERMINED
    assert decision.refuting_conjuncts == ()
    assert decision.undetermined_conjuncts == (
        IndependentClosureConjunct.COMPARABILITY,
    )


def test_both_refuting_conjuncts_are_reported_in_a_fixed_order() -> None:
    decision = decision_for(
        ComparabilityClosureStatus.COMPETITION_RESOLVED_IN_POSET,
        WeakerModelExhaustionStatus.WEAKER_MODEL_CLOSES_RESIDUAL,
        ResidualSurvivalStatus.DOES_NOT_SURVIVE,
    )

    assert decision.refuting_conjuncts == (
        IndependentClosureConjunct.WEAKER_MODEL_EXHAUSTION,
        IndependentClosureConjunct.RESIDUAL_SURVIVAL,
    )
    assert decision.satisfied_conjuncts == (IndependentClosureConjunct.COMPARABILITY,)


def test_the_decision_reads_its_request_and_mode_from_the_frozen_experiment() -> None:
    request = assessment_request(frozen_specification_binding(specification()))
    decision = IndependentClosureCompositionGate.assess(
        comparability=comparability_for(request),
        exhaustion=exhaustion_for(
            request, WeakerModelExhaustionStatus.LICENSED_WEAKER_MODELS_EXHAUSTED
        ),
        survival=survival_for(request, ResidualSurvivalStatus.SURVIVES),
    )

    assert decision.request is request
    assert decision.specification is request.specification
    assert decision.evidence_mode is EvidenceMode.FORMAL
    assert decision.conjunct_statuses[IndependentClosureConjunct.COMPARABILITY] == (
        ComparabilityClosureStatus.COMPETITION_RESOLVED_IN_POSET.name
    )


def test_readings_of_different_requests_are_refused() -> None:
    spec = specification()
    first = assessment_request(frozen_specification_binding(spec))
    second = assessment_request(frozen_specification_binding(spec))

    with pytest.raises(IndependentClosureCompositionError, match="this exact"):
        IndependentClosureCompositionGate.assess(
            comparability=comparability_for(first),
            exhaustion=exhaustion_for(
                second, WeakerModelExhaustionStatus.LICENSED_WEAKER_MODELS_EXHAUSTED
            ),
            survival=survival_for(second, ResidualSurvivalStatus.SURVIVES),
        )


def test_a_survival_reading_of_another_request_is_refused() -> None:
    spec = specification()
    request = assessment_request(frozen_specification_binding(spec))
    other = assessment_request(frozen_specification_binding(spec))

    with pytest.raises(IndependentClosureCompositionError, match="this exact"):
        IndependentClosureCompositionGate.assess(
            comparability=comparability_for(request),
            exhaustion=exhaustion_for(
                request, WeakerModelExhaustionStatus.LICENSED_WEAKER_MODELS_EXHAUSTED
            ),
            survival=survival_for(other, ResidualSurvivalStatus.SURVIVES),
        )


@pytest.mark.parametrize("substituted", ["comparability", "exhaustion", "survival"])
def test_a_reading_that_no_gate_issued_is_refused(substituted: str) -> None:
    request = assessment_request(frozen_specification_binding(specification()))
    readings = {
        "comparability": comparability_for(request),
        "exhaustion": exhaustion_for(
            request, WeakerModelExhaustionStatus.LICENSED_WEAKER_MODELS_EXHAUSTED
        ),
        "survival": survival_for(request, ResidualSurvivalStatus.SURVIVES),
    }
    readings[substituted] = object()  # type: ignore[assignment]

    with pytest.raises(IndependentClosureCompositionError, match="gate-issued"):
        IndependentClosureCompositionGate.assess(**readings)  # type: ignore[arg-type]


def test_a_decision_cannot_be_constructed_outside_the_gate() -> None:
    request = assessment_request(frozen_specification_binding(specification()))

    with pytest.raises(IndependentClosureCompositionError, match="must be issued"):
        IndependentClosureDecision(
            comparability=comparability_for(request),
            exhaustion=exhaustion_for(
                request, WeakerModelExhaustionStatus.LICENSED_WEAKER_MODELS_EXHAUSTED
            ),
            survival=survival_for(request, ResidualSurvivalStatus.SURVIVES),
            status=SATISFIED,
            reason="fabricated closure",
            refuting_conjuncts=(),
            undetermined_conjuncts=(),
        )


def test_the_composed_conjunct_readings_keep_their_own_false_property() -> None:
    request = assessment_request(frozen_specification_binding(specification()))
    comparability = comparability_for(request)
    exhaustion = exhaustion_for(
        request, WeakerModelExhaustionStatus.LICENSED_WEAKER_MODELS_EXHAUSTED
    )
    survival = survival_for(request, ResidualSurvivalStatus.SURVIVES)

    IndependentClosureCompositionGate.assess(
        comparability=comparability, exhaustion=exhaustion, survival=survival
    )

    assert comparability.is_independent_closure is False
    assert exhaustion.is_independent_closure is False
    assert exhaustion.is_weaker_model_exhaustion is True
    assert survival.is_independent_closure is False


def test_the_gate_takes_exactly_the_three_conjunct_readings() -> None:
    import inspect

    signature = inspect.signature(IndependentClosureCompositionGate.assess)

    assert tuple(signature.parameters) == ("comparability", "exhaustion", "survival")
    assert all(
        parameter.kind is inspect.Parameter.KEYWORD_ONLY
        for parameter in signature.parameters.values()
    )
