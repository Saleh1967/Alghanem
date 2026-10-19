import inspect

import pytest

from alghanem.kernel.birth import (
    AuthorizedBirthAssessmentEvaluatorDefinition,
    BirthAssessmentEvaluatorRegistry,
    BirthAssessmentRequest,
    BirthAssessmentSemanticsContract,
    BirthEvaluatorRole,
    BirthExperimentSpecification,
    BirthQuery,
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
from alghanem.kernel.residual_survival import (
    AuthorizedResidualSurvivalVocabulary,
    DeclaredResidualSurvivalVocabulary,
    ResidualSurvivalCertificate,
    ResidualSurvivalError,
    ResidualSurvivalGate,
    ResidualSurvivalVocabularyRegistry,
    SealedResidualSurvivalVocabularyRegistry,
)
from alghanem.kernel.trace import Trace

SURVIVES_TOKEN = "SURVIVES:residual-unexplained-after-every-licensed-projection"
DOES_NOT_SURVIVE_TOKEN = "DOES_NOT_SURVIVE:residual-explained-away"
DEFER_TOKEN = "DEFER:residual-inputs-untestable"

_TOKENS = {
    ResidualSurvivalStatus.SURVIVES: SURVIVES_TOKEN,
    ResidualSurvivalStatus.DOES_NOT_SURVIVE: DOES_NOT_SURVIVE_TOKEN,
    ResidualSurvivalStatus.DEFER: DEFER_TOKEN,
}


def specification(
    *,
    experiment_id: str = "experiment",
    residual_definition_id: str = "residual",
    evidence_mode: EvidenceMode = EvidenceMode.FORMAL,
) -> BirthExperimentSpecification:
    return BirthExperimentSpecification(
        experiment_id=experiment_id,
        revision_id="r1",
        revision_sequence=1,
        evidence_mode=evidence_mode,
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
        residual_definition_id=residual_definition_id,
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
    spec: BirthExperimentSpecification | None = None,
) -> BirthAssessmentSemanticsContract:
    resolved = spec if spec is not None else specification()
    return BirthAssessmentSemanticsContract(
        specification=resolved,
        residual_definition=ResidualDefinitionSpec(
            residual_id=resolved.residual_definition_id,
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
            residual_id=resolved.residual_definition_id,
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
    residual_id: str = "residual",
    domain: str = "finite-domain",
    tokens: tuple[tuple[str, ResidualSurvivalStatus], ...] | None = None,
) -> DeclaredResidualSurvivalVocabulary:
    return DeclaredResidualSurvivalVocabulary(
        residual_id=residual_id,
        domain=domain,
        tokens=tokens
        if tokens is not None
        else (
            (SURVIVES_TOKEN, ResidualSurvivalStatus.SURVIVES),
            (DOES_NOT_SURVIVE_TOKEN, ResidualSurvivalStatus.DOES_NOT_SURVIVE),
            (DEFER_TOKEN, ResidualSurvivalStatus.DEFER),
        ),
    )


def sealed_vocabulary_registry(
    *,
    vocabulary: DeclaredResidualSurvivalVocabulary | None = None,
    binding: BirthAssessmentContentBinding | None = None,
) -> SealedResidualSurvivalVocabularyRegistry:
    registry = ResidualSurvivalVocabularyRegistry()
    registry.register(
        vocabulary_id="residual-vocabulary",
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
    role: BirthEvaluatorRole = BirthEvaluatorRole.RESIDUAL_DEFINITION,
    target_id: str = "residual",
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
    output: str = SURVIVES_TOKEN,
) -> SealedBirthEvaluatorImplementationRegistry:
    def implementation(content: str) -> tuple[str, Trace]:
        return output, Trace(("evaluated",))

    registry = BirthEvaluatorImplementationRegistry()
    registry.register(definition, "impl-v1", implementation)
    return registry.seal("implementation-snapshot")


def provenance_bound_record(
    *,
    output: str = SURVIVES_TOKEN,
    domain: str = "finite-domain",
    role: BirthEvaluatorRole = BirthEvaluatorRole.RESIDUAL_DEFINITION,
    target_id: str = "residual",
    request: BirthAssessmentRequest | None = None,
) -> ProvenanceBoundEvaluatorExecutionRecord:
    definition = authorized_definition(domain=domain, role=role, target_id=target_id)
    return ProvenanceBoundEvaluatorExecutionGate.execute(
        definition=definition,
        implementation_identity="impl-v1",
        registry=sealed_implementation_registry(definition, output=output),
        derived_input=derived_input(request),
    )


def certificate_for(status: ResidualSurvivalStatus) -> ResidualSurvivalCertificate:
    return ResidualSurvivalGate.assess(
        registry=sealed_vocabulary_registry(),
        record=provenance_bound_record(output=_TOKENS[status]),
    )


def test_every_declared_survival_outcome_is_reachable() -> None:
    for status in ResidualSurvivalStatus:
        certificate = certificate_for(status)
        assert certificate.status is status
        assert certificate.matched_token == _TOKENS[status]
        assert certificate.reason.strip()


def test_the_status_is_the_outcome_the_frozen_vocabulary_declares() -> None:
    certificate = certificate_for(ResidualSurvivalStatus.DOES_NOT_SURVIVE)
    declared = certificate.authorization.vocabulary.declared_outcomes
    assert declared[certificate.matched_token] is certificate.status


def test_the_certificate_reads_the_residual_from_the_frozen_experiment() -> None:
    certificate = certificate_for(ResidualSurvivalStatus.SURVIVES)
    assert certificate.residual_id == certificate.specification.residual_definition_id
    assert certificate.residual_definition.residual_id == certificate.residual_id
    assert certificate.evidence_mode is EvidenceMode.FORMAL
    assert certificate.request is certificate.record.execution_record.request


@pytest.mark.parametrize(
    "output",
    [
        f" {SURVIVES_TOKEN}",
        f"{SURVIVES_TOKEN} ",
        SURVIVES_TOKEN.lower(),
        SURVIVES_TOKEN[:12],
        f"{SURVIVES_TOKEN}-extra",
        "definitely-not-a-declared-token",
    ],
)
def test_an_inexactly_matching_output_is_refused_and_never_read_as_defer(
    output: str,
) -> None:
    with pytest.raises(ResidualSurvivalError, match="not a token"):
        ResidualSurvivalGate.assess(
            registry=sealed_vocabulary_registry(),
            record=provenance_bound_record(output=output),
        )


@pytest.mark.parametrize(
    "role",
    [BirthEvaluatorRole.WEAKER_MODEL, BirthEvaluatorRole.CLOSURE_CRITERION],
)
def test_a_record_under_another_role_is_refused(role: BirthEvaluatorRole) -> None:
    with pytest.raises(ResidualSurvivalError, match="RESIDUAL_DEFINITION role"):
        ResidualSurvivalGate.assess(
            registry=sealed_vocabulary_registry(),
            record=provenance_bound_record(role=role, target_id="count"),
        )


def test_a_target_that_is_not_the_frozen_residual_is_refused() -> None:
    with pytest.raises(ResidualSurvivalError, match="own frozen"):
        ResidualSurvivalGate.assess(
            registry=sealed_vocabulary_registry(),
            record=provenance_bound_record(target_id="some-other-residual"),
        )


def test_an_unbound_execution_record_is_refused() -> None:
    record = provenance_bound_record()
    with pytest.raises(ResidualSurvivalError, match="provenance-bound"):
        ResidualSurvivalGate.assess(
            registry=sealed_vocabulary_registry(),
            record=record.execution_record,  # type: ignore[arg-type]
        )


def test_an_unsealed_registry_is_refused() -> None:
    registry = ResidualSurvivalVocabularyRegistry()
    registry.register(
        vocabulary_id="residual-vocabulary",
        vocabulary=declared_vocabulary(),
        binding=content_binding(),
    )
    with pytest.raises(ResidualSurvivalError, match="sealed vocabulary registry"):
        ResidualSurvivalGate.assess(
            registry=registry,  # type: ignore[arg-type]
            record=provenance_bound_record(),
        )


def test_a_vocabulary_bound_to_another_frozen_experiment_is_refused() -> None:
    other = semantics_contract(specification(experiment_id="other-experiment"))
    registry = sealed_vocabulary_registry(binding=content_binding(other))
    with pytest.raises(ResidualSurvivalError, match="not this request's own"):
        ResidualSurvivalGate.assess(registry=registry, record=provenance_bound_record())


def test_resolving_an_unauthorized_scope_is_refused() -> None:
    registry = ResidualSurvivalVocabularyRegistry().seal("empty-snapshot")
    with pytest.raises(ResidualSurvivalError, match="no residual survival vocabulary"):
        registry.resolve(domain="finite-domain", residual_id="residual")


def test_a_mixed_mode_experiment_is_refused_by_name() -> None:
    mixed = specification(evidence_mode=EvidenceMode.MIXED)
    registry = sealed_vocabulary_registry(
        binding=content_binding(semantics_contract(mixed))
    )
    with pytest.raises(ResidualSurvivalError, match="MixedModeNeedsTwoScopedWitnesses"):
        ResidualSurvivalGate.assess(
            registry=registry,
            record=provenance_bound_record(request=assessment_request(mixed)),
        )


def test_an_empirical_mode_experiment_is_read_without_claiming_replication() -> None:
    empirical = specification(evidence_mode=EvidenceMode.EMPIRICAL)
    registry = sealed_vocabulary_registry(
        binding=content_binding(semantics_contract(empirical))
    )
    certificate = ResidualSurvivalGate.assess(
        registry=registry,
        record=provenance_bound_record(request=assessment_request(empirical)),
    )
    assert certificate.evidence_mode is EvidenceMode.EMPIRICAL
    assert certificate.status is ResidualSurvivalStatus.SURVIVES
    assert certificate.is_independent_closure is False


def test_the_vocabulary_must_cover_every_declared_outcome_exactly_once() -> None:
    with pytest.raises(ResidualSurvivalError, match="cover every member"):
        declared_vocabulary(
            tokens=(
                (SURVIVES_TOKEN, ResidualSurvivalStatus.SURVIVES),
                (DEFER_TOKEN, ResidualSurvivalStatus.DEFER),
            )
        )


def test_one_token_may_not_name_two_outcomes() -> None:
    with pytest.raises(ResidualSurvivalError, match="two outcomes"):
        declared_vocabulary(
            tokens=(
                (SURVIVES_TOKEN, ResidualSurvivalStatus.SURVIVES),
                (SURVIVES_TOKEN, ResidualSurvivalStatus.DOES_NOT_SURVIVE),
                (DEFER_TOKEN, ResidualSurvivalStatus.DEFER),
            )
        )


def test_one_outcome_may_not_be_named_by_two_tokens() -> None:
    with pytest.raises(ResidualSurvivalError, match="exactly one token"):
        declared_vocabulary(
            tokens=(
                (SURVIVES_TOKEN, ResidualSurvivalStatus.SURVIVES),
                (DOES_NOT_SURVIVE_TOKEN, ResidualSurvivalStatus.SURVIVES),
                (DEFER_TOKEN, ResidualSurvivalStatus.DEFER),
            )
        )


def test_a_token_with_surrounding_whitespace_is_refused() -> None:
    with pytest.raises(ResidualSurvivalError, match="surrounding whitespace"):
        declared_vocabulary(
            tokens=(
                (f" {SURVIVES_TOKEN} ", ResidualSurvivalStatus.SURVIVES),
                (DOES_NOT_SURVIVE_TOKEN, ResidualSurvivalStatus.DOES_NOT_SURVIVE),
                (DEFER_TOKEN, ResidualSurvivalStatus.DEFER),
            )
        )


def test_an_empty_vocabulary_is_refused() -> None:
    with pytest.raises(ResidualSurvivalError, match="frozen declared tokens"):
        declared_vocabulary(tokens=())


def test_a_vocabulary_must_name_the_bound_contracts_own_residual() -> None:
    registry = ResidualSurvivalVocabularyRegistry()
    with pytest.raises(ResidualSurvivalError, match="own frozen residual definition"):
        registry.register(
            vocabulary_id="residual-vocabulary",
            vocabulary=declared_vocabulary(residual_id="another-residual"),
            binding=content_binding(),
        )


def test_a_vocabulary_domain_must_match_the_frozen_experiment_domain() -> None:
    registry = ResidualSurvivalVocabularyRegistry()
    with pytest.raises(ResidualSurvivalError, match="frozen experiment domain"):
        registry.register(
            vocabulary_id="residual-vocabulary",
            vocabulary=declared_vocabulary(domain="another-domain"),
            binding=content_binding(),
        )


def test_a_caller_cannot_construct_an_authorization() -> None:
    with pytest.raises(ResidualSurvivalError, match="must be issued by"):
        AuthorizedResidualSurvivalVocabulary(
            vocabulary_id="forged",
            vocabulary=declared_vocabulary(),
            binding=content_binding(),
        )


def test_a_caller_cannot_construct_a_sealed_registry() -> None:
    with pytest.raises(ResidualSurvivalError, match="must be issued by"):
        SealedResidualSurvivalVocabularyRegistry(snapshot_id="forged", vocabularies=())


def test_a_caller_cannot_construct_a_certificate() -> None:
    certificate = certificate_for(ResidualSurvivalStatus.SURVIVES)
    with pytest.raises(ResidualSurvivalError, match="must be issued by"):
        ResidualSurvivalCertificate(
            authorization=certificate.authorization,
            record=certificate.record,
            residual_id=certificate.residual_id,
            matched_token=certificate.matched_token,
            status=ResidualSurvivalStatus.SURVIVES,
            reason="forged",
        )


def test_a_vocabulary_id_cannot_be_issued_twice() -> None:
    registry = ResidualSurvivalVocabularyRegistry()
    registry.register(
        vocabulary_id="residual-vocabulary",
        vocabulary=declared_vocabulary(),
        binding=content_binding(),
    )
    with pytest.raises(ResidualSurvivalError, match="already issued"):
        registry.register(
            vocabulary_id="residual-vocabulary",
            vocabulary=declared_vocabulary(),
            binding=content_binding(),
        )


def test_one_domain_and_residual_may_hold_only_one_vocabulary() -> None:
    registry = ResidualSurvivalVocabularyRegistry()
    registry.register(
        vocabulary_id="residual-vocabulary",
        vocabulary=declared_vocabulary(),
        binding=content_binding(),
    )
    with pytest.raises(ResidualSurvivalError, match="already authorized"):
        registry.register(
            vocabulary_id="second-vocabulary",
            vocabulary=declared_vocabulary(),
            binding=content_binding(),
        )


def test_the_gate_accepts_no_status_or_reason_from_its_caller() -> None:
    parameters = inspect.signature(ResidualSurvivalGate.assess).parameters
    assert tuple(parameters) == ("registry", "record")


def test_this_gate_issues_no_verdict_candidate_or_freeze() -> None:
    certificate = certificate_for(ResidualSurvivalStatus.SURVIVES)
    forbidden = ("verdict", "candidate", "birth", "freeze", "rank", "name")
    for attribute in dir(certificate):
        if attribute.startswith("_"):
            continue
        assert not any(word in attribute.lower() for word in forbidden)


def test_a_survival_reading_is_still_not_independent_closure() -> None:
    for status in ResidualSurvivalStatus:
        assert certificate_for(status).is_independent_closure is False
