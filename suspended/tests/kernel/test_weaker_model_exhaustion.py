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
    WeakerModelExhaustionError,
    WeakerModelExhaustionGate,
    WeakerModelExhaustionStatus,
)

CLOSE_TOKEN = "CLOSE:residual-closed-by-this-model"
FAIL_TOKEN = "FAIL_TO_CLOSE:residual-survives-this-model"
DEFER_TOKEN = "DEFER:inputs-untestable-under-this-model"


def specification(
    *, experiment_id: str = "experiment", closure_criterion_id: str = "closure"
) -> BirthExperimentSpecification:
    return BirthExperimentSpecification(
        experiment_id=experiment_id,
        revision_id="r1",
        revision_sequence=1,
        evidence_mode=EvidenceMode.FORMAL,
        domain="finite-domain",
        projection_poset=ProjectionPoset(
            ("count", "set", "multiset", "sequence"),
            (
                ("count", "multiset"),
                ("set", "multiset"),
                ("multiset", "sequence"),
            ),
        ),
        birth_query=BirthQuery(
            "query",
            StructureHypothesis("structure", "a structure is necessary"),
            "sequence",
        ),
        residual_definition_id="residual",
        residual_definition="unexplained distinction",
        closure_criterion_id=closure_criterion_id,
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
    spec: BirthExperimentSpecification | None = None,
) -> BirthAssessmentSemanticsContract:
    resolved = spec if spec is not None else specification()
    return BirthAssessmentSemanticsContract(
        specification=resolved,
        residual_definition=ResidualDefinitionSpec(
            residual_id="residual",
            domain="finite-domain",
            input_projection="sequence",
            output_schema="residual-schema",
            evaluator_id="residual-evaluator",
            invariants=("total-domain-coverage",),
            failure_semantics="malformed residual inputs defer assessment",
        ),
        weaker_models=weaker_model_specs(),
        closure_criterion=ClosureCriterionSpec(
            criterion_id=resolved.closure_criterion_id,
            residual_id="residual",
            domain="finite-domain",
            residual_schema="residual-schema",
            model_result_schema="projection-result",
            evaluator_id="closure-evaluator",
            failure_semantics="untestable closure inputs defer assessment",
        ),
    )


def content_binding(
    contract: BirthAssessmentSemanticsContract | None = None,
) -> BirthAssessmentContentBinding:
    resolved = contract if contract is not None else semantics_contract()
    registry = BirthSemanticsContentRegistry()
    domain = resolved.specification.domain
    registry.freeze(
        domain=domain,
        role=BirthEvaluatorRole.RESIDUAL_DEFINITION,
        target_id=resolved.residual_definition.residual_id,
        manifest=CanonicalBirthSemanticsEncoder.encode_residual_definition(
            resolved.residual_definition
        ),
    )
    registry.freeze(
        domain=domain,
        role=BirthEvaluatorRole.CLOSURE_CRITERION,
        target_id=resolved.closure_criterion.criterion_id,
        manifest=CanonicalBirthSemanticsEncoder.encode_closure_criterion(
            resolved.closure_criterion
        ),
    )
    for model in resolved.weaker_models:
        registry.freeze(
            domain=domain,
            role=BirthEvaluatorRole.WEAKER_MODEL,
            target_id=model.model_id,
            manifest=CanonicalBirthSemanticsEncoder.encode_weaker_model(model),
        )
    frozen_experiment = PreEvidenceSpecificationRegistry().freeze(
        CanonicalBirthExperimentSpecificationEncoder.encode(resolved.specification)
    )
    return BirthAssessmentContentBinding(
        resolved, registry.seal("semantics-snapshot", frozen_experiment)
    )


def declared_vocabulary(
    *,
    criterion_id: str = "closure",
    domain: str = "finite-domain",
    tokens: tuple[tuple[str, ClosureAssessmentStatus], ...] | None = None,
) -> DeclaredClosureOutcomeVocabulary:
    return DeclaredClosureOutcomeVocabulary(
        criterion_id=criterion_id,
        domain=domain,
        tokens=tokens
        if tokens is not None
        else (
            (CLOSE_TOKEN, ClosureAssessmentStatus.CLOSE),
            (FAIL_TOKEN, ClosureAssessmentStatus.FAIL_TO_CLOSE),
            (DEFER_TOKEN, ClosureAssessmentStatus.DEFER),
        ),
    )


def sealed_vocabulary_registry(
    *,
    vocabulary: DeclaredClosureOutcomeVocabulary | None = None,
    binding: BirthAssessmentContentBinding | None = None,
) -> SealedClosureOutcomeVocabularyRegistry:
    registry = ClosureOutcomeVocabularyRegistry()
    registry.register(
        vocabulary_id="closure-vocabulary",
        vocabulary=vocabulary if vocabulary is not None else declared_vocabulary(),
        binding=binding if binding is not None else content_binding(),
    )
    return registry.seal("vocabulary-snapshot")


def frozen_specification_binding(
    spec: BirthExperimentSpecification | None = None,
) -> BirthExperimentSpecificationContentBinding:
    resolved = spec if spec is not None else specification()
    frozen = PreEvidenceSpecificationRegistry().freeze(
        CanonicalBirthExperimentSpecificationEncoder.encode(resolved)
    )
    return BirthExperimentSpecificationContentBinding(resolved, frozen)


def assessment_request(
    spec: BirthExperimentSpecification | None = None,
) -> BirthAssessmentRequest:
    binding = frozen_specification_binding(spec)
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


def derived_input(
    request: BirthAssessmentRequest | None = None,
) -> EvidenceDerivedEvaluatorInput:
    registry = EvaluatorInputDerivationRegistry()
    registry.register(
        domain="finite-domain",
        derivation_id="identity",
        implementation_identity="identity-v1",
        declared_transformation="decode the authorized evidence bytes",
        derivation=identity_derivation,
    )
    return EvaluatorInputDerivationGate.derive(
        registry=registry.seal("derivation-snapshot"),
        request=request if request is not None else assessment_request(),
        derivation_id="identity",
        implementation_identity="identity-v1",
    )


def authorized_definition(
    *,
    domain: str = "finite-domain",
    role: BirthEvaluatorRole = BirthEvaluatorRole.WEAKER_MODEL,
    target_id: str = "count",
) -> AuthorizedBirthAssessmentEvaluatorDefinition:
    return BirthAssessmentEvaluatorRegistry().authorize(
        domain=domain,
        role=role,
        target_id=target_id,
        evaluator_id=f"{target_id}-evaluator",
    )


def sealed_implementation_registry(
    definition: AuthorizedBirthAssessmentEvaluatorDefinition,
    *,
    output: str = FAIL_TOKEN,
) -> SealedBirthEvaluatorImplementationRegistry:
    def implementation(content: str) -> tuple[str, Trace]:
        return output, Trace(("evaluated",))

    registry = BirthEvaluatorImplementationRegistry()
    registry.register(definition, "impl-v1", implementation)
    return registry.seal("implementation-snapshot")


def provenance_bound_record(
    *,
    output: str = FAIL_TOKEN,
    domain: str = "finite-domain",
    role: BirthEvaluatorRole = BirthEvaluatorRole.WEAKER_MODEL,
    target_id: str = "count",
    request: BirthAssessmentRequest | None = None,
) -> ProvenanceBoundEvaluatorExecutionRecord:
    definition = authorized_definition(domain=domain, role=role, target_id=target_id)
    return ProvenanceBoundEvaluatorExecutionGate.execute(
        definition=definition,
        implementation_identity="impl-v1",
        registry=sealed_implementation_registry(definition, output=output),
        derived_input=derived_input(request),
    )


CONE = ("count", "multiset", "set")
_TOKENS = {
    ClosureAssessmentStatus.CLOSE: CLOSE_TOKEN,
    ClosureAssessmentStatus.FAIL_TO_CLOSE: FAIL_TOKEN,
    ClosureAssessmentStatus.DEFER: DEFER_TOKEN,
}


def certificate_for(
    request, model_id: str, status: ClosureAssessmentStatus
) -> WeakerModelClosureCertificate:
    return WeakerModelClosureGate.assess(
        registry=sealed_vocabulary_registry(),
        record=provenance_bound_record(
            output=_TOKENS[status], target_id=model_id, request=request
        ),
    )


def certificates_for(
    request, outcomes: dict[str, ClosureAssessmentStatus]
) -> tuple[WeakerModelClosureCertificate, ...]:
    return tuple(
        certificate_for(request, model_id, status)
        for model_id, status in outcomes.items()
    )


def all_failing(request) -> tuple[WeakerModelClosureCertificate, ...]:
    return certificates_for(
        request, dict.fromkeys(CONE, ClosureAssessmentStatus.FAIL_TO_CLOSE)
    )


def test_the_frozen_cone_is_derived_not_written() -> None:
    assert set(assessment_request().specification.frozen_weaker_models) == set(CONE)


def test_every_model_failing_to_close_is_exhaustion() -> None:
    request = assessment_request()

    assessment = WeakerModelExhaustionGate.assess(
        request=request, certificates=all_failing(request)
    )

    assert (
        assessment.status
        is WeakerModelExhaustionStatus.LICENSED_WEAKER_MODELS_EXHAUSTED
    )
    assert assessment.is_weaker_model_exhaustion is True


def test_one_closing_model_outranks_every_deferral() -> None:
    request = assessment_request()
    certificates = certificates_for(
        request,
        {
            "count": ClosureAssessmentStatus.DEFER,
            "multiset": ClosureAssessmentStatus.DEFER,
            "set": ClosureAssessmentStatus.CLOSE,
        },
    )

    assessment = WeakerModelExhaustionGate.assess(
        request=request, certificates=certificates
    )

    assert assessment.status is WeakerModelExhaustionStatus.WEAKER_MODEL_CLOSES_RESIDUAL
    assert assessment.closing_models == ("set",)
    assert assessment.is_weaker_model_exhaustion is False


def test_a_single_deferral_blocks_exhaustion() -> None:
    request = assessment_request()
    certificates = certificates_for(
        request,
        {
            "count": ClosureAssessmentStatus.FAIL_TO_CLOSE,
            "multiset": ClosureAssessmentStatus.FAIL_TO_CLOSE,
            "set": ClosureAssessmentStatus.DEFER,
        },
    )

    assessment = WeakerModelExhaustionGate.assess(
        request=request, certificates=certificates
    )

    assert assessment.status is WeakerModelExhaustionStatus.EXHAUSTION_UNDETERMINED
    assert assessment.deferred_models == ("set",)
    assert assessment.is_weaker_model_exhaustion is False


def test_the_aggregate_does_not_depend_on_certificate_order() -> None:
    request = assessment_request()
    certificates = certificates_for(
        request,
        {
            "count": ClosureAssessmentStatus.DEFER,
            "multiset": ClosureAssessmentStatus.CLOSE,
            "set": ClosureAssessmentStatus.FAIL_TO_CLOSE,
        },
    )

    forward = WeakerModelExhaustionGate.assess(
        request=request, certificates=certificates
    )
    reversed_order = WeakerModelExhaustionGate.assess(
        request=request, certificates=tuple(reversed(certificates))
    )

    assert forward.status is reversed_order.status
    assert forward.closing_models == reversed_order.closing_models
    assert forward.deferred_models == reversed_order.deferred_models


def test_every_exhaustion_status_is_reachable() -> None:
    request = assessment_request()
    reached = {
        WeakerModelExhaustionGate.assess(
            request=request, certificates=certificates_for(request, outcomes)
        ).status
        for outcomes in (
            dict.fromkeys(CONE, ClosureAssessmentStatus.FAIL_TO_CLOSE),
            {
                "count": ClosureAssessmentStatus.CLOSE,
                "multiset": ClosureAssessmentStatus.FAIL_TO_CLOSE,
                "set": ClosureAssessmentStatus.FAIL_TO_CLOSE,
            },
            {
                "count": ClosureAssessmentStatus.DEFER,
                "multiset": ClosureAssessmentStatus.FAIL_TO_CLOSE,
                "set": ClosureAssessmentStatus.FAIL_TO_CLOSE,
            },
        )
    }

    assert reached == set(WeakerModelExhaustionStatus)


def test_a_missing_model_is_refused_and_never_read_as_failure_to_close() -> None:
    request = assessment_request()
    certificates = certificates_for(
        request,
        {
            "count": ClosureAssessmentStatus.FAIL_TO_CLOSE,
            "multiset": ClosureAssessmentStatus.FAIL_TO_CLOSE,
        },
    )

    with pytest.raises(WeakerModelExhaustionError, match="never a failure to close"):
        WeakerModelExhaustionGate.assess(request=request, certificates=certificates)


def test_an_empty_certificate_set_is_refused() -> None:
    with pytest.raises(WeakerModelExhaustionError, match="exactly cover"):
        WeakerModelExhaustionGate.assess(request=assessment_request(), certificates=())


def test_a_duplicated_model_is_refused() -> None:
    request = assessment_request()
    certificates = all_failing(request) + (
        certificate_for(request, "count", ClosureAssessmentStatus.CLOSE),
    )

    with pytest.raises(WeakerModelExhaustionError, match="twice"):
        WeakerModelExhaustionGate.assess(request=request, certificates=certificates)


def test_a_certificate_from_another_request_is_refused() -> None:
    request = assessment_request()
    other = assessment_request()
    certificates = all_failing(request)[:-1] + (
        certificate_for(other, "set", ClosureAssessmentStatus.FAIL_TO_CLOSE),
    )

    with pytest.raises(WeakerModelExhaustionError, match="this exact"):
        WeakerModelExhaustionGate.assess(request=request, certificates=certificates)


def test_a_non_certificate_is_refused() -> None:
    with pytest.raises(WeakerModelExhaustionError, match="gate-issued"):
        WeakerModelExhaustionGate.assess(
            request=assessment_request(),
            certificates=(object(),),  # type: ignore[arg-type]
        )


def test_an_unauthorized_request_is_refused() -> None:
    with pytest.raises(WeakerModelExhaustionError, match="authorized assessment"):
        WeakerModelExhaustionGate.assess(
            request=object(),  # type: ignore[arg-type]
            certificates=(),
        )


def test_an_unissued_assessment_is_refused() -> None:
    request = assessment_request()

    with pytest.raises(WeakerModelExhaustionError, match="must be issued by"):
        WeakerModelExhaustionAssessment(
            request=request,
            certificates=all_failing(request),
            status=WeakerModelExhaustionStatus.LICENSED_WEAKER_MODELS_EXHAUSTED,
            reason="forged",
            closing_models=(),
            deferred_models=(),
        )


def test_outcome_counts_include_every_declared_outcome_at_zero() -> None:
    request = assessment_request()

    assessment = WeakerModelExhaustionGate.assess(
        request=request, certificates=all_failing(request)
    )

    assert set(assessment.outcome_counts) == set(ClosureAssessmentStatus)
    assert assessment.outcome_counts[ClosureAssessmentStatus.CLOSE] == 0
    assert assessment.outcome_counts[ClosureAssessmentStatus.FAIL_TO_CLOSE] == len(CONE)
    assert sum(assessment.outcome_counts.values()) == len(assessment.certificates)


def test_the_counts_are_properties_not_written_fields() -> None:
    assert isinstance(WeakerModelExhaustionAssessment.outcome_counts, property)
    assert isinstance(
        WeakerModelExhaustionAssessment.is_weaker_model_exhaustion, property
    )


def test_exhaustion_is_still_not_independent_closure() -> None:
    request = assessment_request()

    assessment = WeakerModelExhaustionGate.assess(
        request=request, certificates=all_failing(request)
    )

    assert assessment.is_independent_closure is False


def test_the_gate_accepts_no_status_or_reason_from_its_caller() -> None:
    import inspect

    parameters = inspect.signature(WeakerModelExhaustionGate.assess).parameters

    assert set(parameters) == {"request", "certificates"}


def test_this_gate_issues_no_verdict_candidate_or_freeze() -> None:
    request = assessment_request()
    assessment = WeakerModelExhaustionGate.assess(
        request=request, certificates=all_failing(request)
    )

    for forbidden in ("verdict", "birth_candidate", "freeze", "traditional_name", "e0"):
        assert not hasattr(assessment, forbidden)


def test_the_test_model_is_not_part_of_the_cone_to_be_exhausted() -> None:
    spec = specification()

    assert spec.birth_query.test_model not in spec.frozen_weaker_models


def test_a_record_under_the_weaker_model_role_is_what_feeds_this_gate() -> None:
    request = assessment_request()
    certificate = certificate_for(
        request, "count", ClosureAssessmentStatus.FAIL_TO_CLOSE
    )

    assert certificate.record.role is BirthEvaluatorRole.WEAKER_MODEL
