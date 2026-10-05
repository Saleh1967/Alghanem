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
    AuthorizedClosureOutcomeVocabulary,
    ClosureOutcomeVocabularyRegistry,
    DeclaredClosureOutcomeVocabulary,
    SealedClosureOutcomeVocabularyRegistry,
    WeakerModelClosureCertificate,
    WeakerModelClosureError,
    WeakerModelClosureGate,
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


def test_a_declared_vocabulary_maps_every_closed_status_exactly_once() -> None:
    vocabulary = declared_vocabulary()

    assert set(vocabulary.declared_outcomes.values()) == set(ClosureAssessmentStatus)
    assert vocabulary.declared_tokens == (CLOSE_TOKEN, FAIL_TOKEN, DEFER_TOKEN)


def test_the_declared_vocabulary_is_the_existing_closed_status_set() -> None:
    criterion = semantics_contract().closure_criterion

    assert set(criterion.supported_statuses) == set(
        declared_vocabulary().declared_outcomes.values()
    )


def test_a_vocabulary_missing_a_declared_status_is_refused() -> None:
    with pytest.raises(WeakerModelClosureError, match="every member"):
        declared_vocabulary(
            tokens=(
                (CLOSE_TOKEN, ClosureAssessmentStatus.CLOSE),
                (FAIL_TOKEN, ClosureAssessmentStatus.FAIL_TO_CLOSE),
            )
        )


def test_a_vocabulary_binding_two_tokens_to_one_status_is_refused() -> None:
    with pytest.raises(WeakerModelClosureError, match="exactly one token"):
        declared_vocabulary(
            tokens=(
                (CLOSE_TOKEN, ClosureAssessmentStatus.CLOSE),
                (FAIL_TOKEN, ClosureAssessmentStatus.FAIL_TO_CLOSE),
                (DEFER_TOKEN, ClosureAssessmentStatus.DEFER),
                ("another", ClosureAssessmentStatus.DEFER),
            )
        )


def test_a_vocabulary_binding_one_token_to_two_statuses_is_refused() -> None:
    with pytest.raises(WeakerModelClosureError, match="two outcomes"):
        declared_vocabulary(
            tokens=(
                (CLOSE_TOKEN, ClosureAssessmentStatus.CLOSE),
                (CLOSE_TOKEN, ClosureAssessmentStatus.FAIL_TO_CLOSE),
                (DEFER_TOKEN, ClosureAssessmentStatus.DEFER),
            )
        )


def test_a_padded_token_is_refused_because_matching_is_exact() -> None:
    with pytest.raises(WeakerModelClosureError, match="surrounding whitespace"):
        declared_vocabulary(
            tokens=(
                (f" {CLOSE_TOKEN} ", ClosureAssessmentStatus.CLOSE),
                (FAIL_TOKEN, ClosureAssessmentStatus.FAIL_TO_CLOSE),
                (DEFER_TOKEN, ClosureAssessmentStatus.DEFER),
            )
        )


def test_an_unissued_authorization_is_refused() -> None:
    with pytest.raises(WeakerModelClosureError, match="must be issued by"):
        AuthorizedClosureOutcomeVocabulary(
            vocabulary_id="forged",
            vocabulary=declared_vocabulary(),
            binding=content_binding(),
        )


def test_an_unissued_certificate_is_refused() -> None:
    with pytest.raises(WeakerModelClosureError, match="must be issued by"):
        WeakerModelClosureCertificate(
            authorization=sealed_vocabulary_registry().vocabularies[0],
            record=provenance_bound_record(),
            model_id="count",
            matched_token=FAIL_TOKEN,
            status=ClosureAssessmentStatus.FAIL_TO_CLOSE,
            reason="forged",
        )


def test_a_vocabulary_for_another_criterion_is_refused_at_registration() -> None:
    registry = ClosureOutcomeVocabularyRegistry()

    with pytest.raises(WeakerModelClosureError, match="frozen closure criterion"):
        registry.register(
            vocabulary_id="closure-vocabulary",
            vocabulary=declared_vocabulary(criterion_id="another-criterion"),
            binding=content_binding(),
        )


def test_a_vocabulary_for_another_domain_is_refused_at_registration() -> None:
    registry = ClosureOutcomeVocabularyRegistry()

    with pytest.raises(WeakerModelClosureError, match="domain must match"):
        registry.register(
            vocabulary_id="closure-vocabulary",
            vocabulary=declared_vocabulary(domain="another-domain"),
            binding=content_binding(),
        )


def test_two_vocabularies_for_one_criterion_are_refused() -> None:
    registry = ClosureOutcomeVocabularyRegistry()
    registry.register(
        vocabulary_id="first",
        vocabulary=declared_vocabulary(),
        binding=content_binding(),
    )

    with pytest.raises(WeakerModelClosureError, match="already authorized"):
        registry.register(
            vocabulary_id="second",
            vocabulary=declared_vocabulary(),
            binding=content_binding(),
        )


def test_a_reused_vocabulary_id_is_refused() -> None:
    registry = ClosureOutcomeVocabularyRegistry()
    registry.register(
        vocabulary_id="closure-vocabulary",
        vocabulary=declared_vocabulary(),
        binding=content_binding(),
    )

    other = specification(closure_criterion_id="second-closure")

    with pytest.raises(WeakerModelClosureError, match="already issued"):
        registry.register(
            vocabulary_id="closure-vocabulary",
            vocabulary=declared_vocabulary(criterion_id="second-closure"),
            binding=content_binding(semantics_contract(other)),
        )


def test_an_unsealed_registry_is_refused_by_the_gate() -> None:
    with pytest.raises(WeakerModelClosureError, match="sealed vocabulary registry"):
        WeakerModelClosureGate.assess(
            registry=ClosureOutcomeVocabularyRegistry(),  # type: ignore[arg-type]
            record=provenance_bound_record(),
        )


def test_an_unrelated_object_is_not_a_provenance_bound_record() -> None:
    with pytest.raises(WeakerModelClosureError, match="provenance-bound"):
        WeakerModelClosureGate.assess(
            registry=sealed_vocabulary_registry(),
            record=object(),  # type: ignore[arg-type]
        )


def test_a_declared_fail_to_close_token_is_read_as_fail_to_close() -> None:
    certificate = WeakerModelClosureGate.assess(
        registry=sealed_vocabulary_registry(),
        record=provenance_bound_record(output=FAIL_TOKEN),
    )

    assert certificate.status is ClosureAssessmentStatus.FAIL_TO_CLOSE
    assert certificate.matched_token == FAIL_TOKEN
    assert certificate.model_id == "count"


def test_a_declared_close_token_is_read_as_close() -> None:
    certificate = WeakerModelClosureGate.assess(
        registry=sealed_vocabulary_registry(),
        record=provenance_bound_record(output=CLOSE_TOKEN),
    )

    assert certificate.status is ClosureAssessmentStatus.CLOSE


def test_a_declared_defer_token_is_read_as_defer() -> None:
    certificate = WeakerModelClosureGate.assess(
        registry=sealed_vocabulary_registry(),
        record=provenance_bound_record(output=DEFER_TOKEN),
    )

    assert certificate.status is ClosureAssessmentStatus.DEFER


def test_every_declared_outcome_is_reachable_through_the_gate() -> None:
    reached = {
        WeakerModelClosureGate.assess(
            registry=sealed_vocabulary_registry(),
            record=provenance_bound_record(output=token),
        ).status
        for token in (CLOSE_TOKEN, FAIL_TOKEN, DEFER_TOKEN)
    }

    assert reached == set(ClosureAssessmentStatus)


def test_an_undeclared_output_is_refused_and_never_read_as_a_deferral() -> None:
    with pytest.raises(WeakerModelClosureError, match="never read as a"):
        WeakerModelClosureGate.assess(
            registry=sealed_vocabulary_registry(),
            record=provenance_bound_record(output="the model did not close it"),
        )


def test_a_padded_output_is_refused_rather_than_trimmed() -> None:
    with pytest.raises(WeakerModelClosureError, match="not a token"):
        WeakerModelClosureGate.assess(
            registry=sealed_vocabulary_registry(),
            record=provenance_bound_record(output=f" {FAIL_TOKEN}"),
        )


def test_a_case_folded_output_is_refused_rather_than_matched() -> None:
    with pytest.raises(WeakerModelClosureError, match="not a token"):
        WeakerModelClosureGate.assess(
            registry=sealed_vocabulary_registry(),
            record=provenance_bound_record(output=FAIL_TOKEN.lower()),
        )


def test_an_output_extending_a_declared_token_is_refused() -> None:
    with pytest.raises(WeakerModelClosureError, match="not a token"):
        WeakerModelClosureGate.assess(
            registry=sealed_vocabulary_registry(),
            record=provenance_bound_record(output=f"{FAIL_TOKEN}-and-more"),
        )


def test_a_record_under_another_role_is_refused() -> None:
    with pytest.raises(WeakerModelClosureError, match="WEAKER_MODEL role"):
        WeakerModelClosureGate.assess(
            registry=sealed_vocabulary_registry(),
            record=provenance_bound_record(
                role=BirthEvaluatorRole.RESIDUAL_DEFINITION,
                target_id="residual",
            ),
        )


def test_a_closure_criterion_record_is_refused_too() -> None:
    with pytest.raises(WeakerModelClosureError, match="WEAKER_MODEL role"):
        WeakerModelClosureGate.assess(
            registry=sealed_vocabulary_registry(),
            record=provenance_bound_record(
                role=BirthEvaluatorRole.CLOSURE_CRITERION,
                target_id="closure",
            ),
        )


def test_a_target_outside_the_frozen_prerequisite_cone_is_refused() -> None:
    with pytest.raises(WeakerModelClosureError, match="prerequisite cone"):
        WeakerModelClosureGate.assess(
            registry=sealed_vocabulary_registry(),
            record=provenance_bound_record(target_id="sequence"),
        )


def test_the_test_model_itself_is_not_a_weaker_model() -> None:
    request = assessment_request()

    assert request.specification.birth_query.test_model == "sequence"
    assert "sequence" not in request.specification.frozen_weaker_models


def test_no_vocabulary_for_this_criterion_is_refused() -> None:
    registry = ClosureOutcomeVocabularyRegistry()

    with pytest.raises(WeakerModelClosureError, match="no closure outcome"):
        WeakerModelClosureGate.assess(
            registry=registry.seal("empty-snapshot"),
            record=provenance_bound_record(),
        )


def test_a_vocabulary_bound_to_another_experiment_is_refused() -> None:
    other = specification(experiment_id="another-experiment")

    with pytest.raises(WeakerModelClosureError, match="not this request's own"):
        WeakerModelClosureGate.assess(
            registry=sealed_vocabulary_registry(
                binding=content_binding(semantics_contract(other))
            ),
            record=provenance_bound_record(request=assessment_request()),
        )


def test_the_certificate_reads_the_records_own_output_and_target() -> None:
    record = provenance_bound_record(output=CLOSE_TOKEN, target_id="multiset")
    certificate = WeakerModelClosureGate.assess(
        registry=sealed_vocabulary_registry(), record=record
    )

    assert certificate.matched_token == record.output_content
    assert certificate.model_id == record.target_id
    assert certificate.record is record


def test_the_certified_output_came_from_the_requests_own_evidence() -> None:
    record = provenance_bound_record()
    certificate = WeakerModelClosureGate.assess(
        registry=sealed_vocabulary_registry(), record=record
    )

    assert (
        certificate.record.evidence_content_id
        == certificate.request.evidence_snapshot.content_id
    )


def test_a_certificate_is_not_weaker_model_exhaustion() -> None:
    certificate = WeakerModelClosureGate.assess(
        registry=sealed_vocabulary_registry(),
        record=provenance_bound_record(output=FAIL_TOKEN),
    )

    assert certificate.is_weaker_model_exhaustion is False
    assert len(certificate.frozen_weaker_models) > 1


def test_a_certificate_is_not_independent_closure() -> None:
    certificate = WeakerModelClosureGate.assess(
        registry=sealed_vocabulary_registry(),
        record=provenance_bound_record(output=FAIL_TOKEN),
    )

    assert certificate.is_independent_closure is False


def test_every_reachable_outcome_leaves_closure_and_exhaustion_false() -> None:
    for token in (CLOSE_TOKEN, FAIL_TOKEN, DEFER_TOKEN):
        certificate = WeakerModelClosureGate.assess(
            registry=sealed_vocabulary_registry(),
            record=provenance_bound_record(output=token),
        )

        assert certificate.is_independent_closure is False
        assert certificate.is_weaker_model_exhaustion is False


def test_the_reason_is_derived_and_not_caller_supplied() -> None:
    first = WeakerModelClosureGate.assess(
        registry=sealed_vocabulary_registry(),
        record=provenance_bound_record(output=FAIL_TOKEN),
    )
    second = WeakerModelClosureGate.assess(
        registry=sealed_vocabulary_registry(),
        record=provenance_bound_record(output=CLOSE_TOKEN),
    )

    assert first.reason != second.reason
    assert first.reason.startswith("DeclaredFailToCloseTokenRead")
    assert second.reason.startswith("DeclaredCloseTokenRead")


def test_this_gate_issues_no_verdict_candidate_or_freeze() -> None:
    certificate = WeakerModelClosureGate.assess(
        registry=sealed_vocabulary_registry(), record=provenance_bound_record()
    )

    for forbidden in (
        "verdict",
        "birth_candidate",
        "freeze",
        "traditional_name",
        "e0",
    ):
        assert not hasattr(certificate, forbidden)


def test_the_gate_accepts_no_status_or_reason_from_its_caller() -> None:
    import inspect

    parameters = inspect.signature(WeakerModelClosureGate.assess).parameters

    assert set(parameters) == {"registry", "record"}
