import pytest

import alghanem.kernel.birth as birth
from alghanem.kernel.birth import (
    AuthorizedBirthAssessmentEvaluatorDefinition,
    BirthAssessmentEvaluatorAuthorityError,
    BirthAssessmentEvaluatorDefinitions,
    BirthAssessmentEvaluatorRegistry,
    BirthAssessmentRequest,
    BirthAssessmentSemanticsContract,
    BirthEvaluatorRole,
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
from alghanem.kernel.evidence_acquisition import (
    AuthorizedEvidenceSnapshot,
    EvidenceAcquisitionAuthority,
    EvidenceAcquisitionAuthorityError,
    EvidenceAcquisitionAuthorization,
    EvidenceAcquisitionRun,
)
from alghanem.kernel.experiment_spec_content_identity import (
    BirthExperimentSpecificationContentBinding,
    CanonicalBirthExperimentSpecificationEncoder,
    PreEvidenceSpecificationRegistry,
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
        residual_definition_id="residual",
        residual_definition="unexplained distinction",
        closure_criterion_id="closure",
        closure_criterion="all prerequisite models fail to close the residual",
        evidence_requirements="exhaustive proof over the finite domain",
    )


def frozen_specification_binding() -> BirthExperimentSpecificationContentBinding:
    spec = specification()
    frozen = PreEvidenceSpecificationRegistry().freeze(
        CanonicalBirthExperimentSpecificationEncoder.encode(spec)
    )
    return BirthExperimentSpecificationContentBinding(spec, frozen)


def authorized_evidence_snapshot(
    binding: BirthExperimentSpecificationContentBinding | None = None,
) -> AuthorizedEvidenceSnapshot:
    authorization = EvidenceAcquisitionAuthority().authorize(
        authorization_id="authorization",
        binding=binding if binding is not None else frozen_specification_binding(),
    )
    run = authorization.open_run("run")
    return run.ingest(
        snapshot_id="snapshot", payload="enumeration", trace="acquisition-trace"
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


def assessment_semantics() -> BirthAssessmentSemanticsContract:
    return BirthAssessmentSemanticsContract(
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
        frozen_specification_binding(), authorized_evidence_snapshot()
    )

    assert request.evidence_snapshot.snapshot_id == "snapshot"
    assert request.specification == specification()


@pytest.mark.parametrize("binding_value", (None, specification(), "not-a-binding"))
def test_malformed_assessment_request_cannot_enter_future_runtime(
    binding_value: object,
) -> None:
    with pytest.raises(BirthExperimentSpecificationError, match="frozen experiment"):
        BirthAssessmentRequest(
            binding_value,  # type: ignore[arg-type]
            authorized_evidence_snapshot(),
        )


@pytest.mark.parametrize(
    "evidence_value", (None, "not-an-evidence-snapshot", EvidenceSnapshot("s", "d"))
)
def test_request_requires_a_real_evidence_snapshot(evidence_value: object) -> None:
    with pytest.raises(BirthExperimentSpecificationError, match="authorized evidence"):
        BirthAssessmentRequest(
            frozen_specification_binding(),
            evidence_value,  # type: ignore[arg-type]
        )


def test_request_rejects_snapshot_acquired_under_a_different_experiment() -> None:
    other_spec = BirthExperimentSpecification(
        experiment_id="other-experiment",
        revision_id="r1",
        revision_sequence=1,
        evidence_mode=EvidenceMode.FORMAL,
        domain="finite-domain",
        projection_poset=ProjectionPoset(("sequence",), ()),
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
    other_frozen = PreEvidenceSpecificationRegistry().freeze(
        CanonicalBirthExperimentSpecificationEncoder.encode(other_spec)
    )
    other_binding = BirthExperimentSpecificationContentBinding(other_spec, other_frozen)
    foreign_snapshot = authorized_evidence_snapshot(other_binding)

    with pytest.raises(BirthExperimentSpecificationError, match="not acquired under"):
        BirthAssessmentRequest(frozen_specification_binding(), foreign_snapshot)


def test_evidence_acquisition_authorization_requires_a_genuine_frozen_binding() -> None:
    for bad_binding in (None, specification(), "not-a-binding"):
        with pytest.raises(EvidenceAcquisitionAuthorityError, match="genuine frozen"):
            EvidenceAcquisitionAuthority().authorize(
                authorization_id="authorization",
                binding=bad_binding,  # type: ignore[arg-type]
            )


def test_evidence_acquisition_authorization_derives_conditions_from_binding() -> None:
    binding = frozen_specification_binding()
    authorization = EvidenceAcquisitionAuthority().authorize(
        authorization_id="authorization", binding=binding
    )

    assert authorization.experiment_content_id == binding.content_id
    assert authorization.domain == binding.specification.domain
    assert authorization.evidence_mode == binding.specification.evidence_mode
    assert (
        authorization.evidence_requirements
        == binding.specification.evidence_requirements
    )
    assert authorization.revision_id == binding.specification.revision_id
    assert authorization.revision_sequence == binding.specification.revision_sequence


def test_evidence_acquisition_authorization_cannot_be_constructed_directly() -> None:
    binding = frozen_specification_binding()
    with pytest.raises(EvidenceAcquisitionAuthorityError, match="issued by"):
        EvidenceAcquisitionAuthorization(
            authorization_id="authorization", binding=binding
        )


def test_evidence_acquisition_run_cannot_be_constructed_directly() -> None:
    binding = frozen_specification_binding()
    with pytest.raises(EvidenceAcquisitionAuthorityError, match="issued by"):
        EvidenceAcquisitionRun(
            run_id="run",
            authorization_id="authorization",
            experiment_content_id=binding.content_id,
            domain=binding.specification.domain,
            evidence_mode=binding.specification.evidence_mode,
        )


def test_authorized_evidence_snapshot_cannot_be_constructed_directly() -> None:
    binding = frozen_specification_binding()
    authorization = EvidenceAcquisitionAuthority().authorize(
        authorization_id="authorization", binding=binding
    )
    run = authorization.open_run("run")
    snapshot = run.ingest(snapshot_id="s", payload="content", trace="trace")

    with pytest.raises(EvidenceAcquisitionAuthorityError, match="issued by"):
        AuthorizedEvidenceSnapshot(
            snapshot_id="s",
            run_id="run",
            authorization_id="authorization",
            experiment_content_id=binding.content_id,
            domain=binding.specification.domain,
            evidence_mode=binding.specification.evidence_mode,
            evidence_manifest=snapshot.evidence_manifest,
            trace="trace",
        )


def test_authorized_evidence_ingestion_derives_content_identity() -> None:
    binding = frozen_specification_binding()
    authorization = EvidenceAcquisitionAuthority().authorize(
        authorization_id="authorization", binding=binding
    )
    run = authorization.open_run("run")

    first = run.ingest(snapshot_id="s1", payload="same content", trace="trace")
    second = run.ingest(snapshot_id="s2", payload="same content", trace="trace")
    different = run.ingest(snapshot_id="s3", payload="other content", trace="trace")

    assert first.content_id == second.content_id
    assert first.content_id != different.content_id
    assert first.experiment_content_id == binding.content_id


def test_evidence_acquisition_authority_rejects_repeated_authorization_id() -> None:
    binding = frozen_specification_binding()
    authority = EvidenceAcquisitionAuthority()
    authority.authorize(authorization_id="authorization", binding=binding)

    with pytest.raises(EvidenceAcquisitionAuthorityError, match="already issued"):
        authority.authorize(authorization_id="authorization", binding=binding)


def test_evidence_acquisition_authorization_rejects_repeated_run_id() -> None:
    binding = frozen_specification_binding()
    authorization = EvidenceAcquisitionAuthority().authorize(
        authorization_id="authorization", binding=binding
    )
    authorization.open_run("run")

    with pytest.raises(EvidenceAcquisitionAuthorityError, match="already issued"):
        authorization.open_run("run")


def test_evidence_acquisition_run_rejects_repeated_snapshot_id() -> None:
    binding = frozen_specification_binding()
    authorization = EvidenceAcquisitionAuthority().authorize(
        authorization_id="authorization", binding=binding
    )
    run = authorization.open_run("run")
    run.ingest(snapshot_id="s1", payload="content", trace="trace")

    with pytest.raises(EvidenceAcquisitionAuthorityError, match="already issued"):
        run.ingest(snapshot_id="s1", payload="other content", trace="trace")


def test_evidence_occurrence_ids_are_scoped_and_independent() -> None:
    binding = frozen_specification_binding()
    authority = EvidenceAcquisitionAuthority()
    first_authorization = authority.authorize(authorization_id="a1", binding=binding)
    second_authorization = EvidenceAcquisitionAuthority().authorize(
        authorization_id="a1", binding=binding
    )

    first_run = first_authorization.open_run("run-1")
    second_run = second_authorization.open_run("run-1")
    other_run = first_authorization.open_run("run-2")

    assert first_run.run_id == second_run.run_id == "run-1"
    assert other_run.run_id != first_run.run_id

    first_run.ingest(snapshot_id="s1", payload="content", trace="trace")
    other_run.ingest(snapshot_id="s1", payload="content", trace="trace")


def test_issuer_scoped_uniqueness_is_not_yet_a_portable_occurrence_identity() -> None:
    """`LocalInjectivity != PortableIdentity` (G0.2a.3.1 is scope-relative).

    Two distinct `EvidenceAcquisitionAuthority` instances are two distinct,
    uncoordinated issuance scopes: nothing stops both from independently
    issuing the same `authorization_id`/`run_id`/`snapshot_id` triple. If they
    also share the same frozen experiment binding, payload, and trace, the
    resulting snapshots' comparable representations coincide even though the
    two acquisition occurrences are genuinely independent objects. Proving
    `PortableEvidenceOccurrenceIdentity` would require a self-issuing
    issuer-scope identity propagated through the chain, which does not exist
    yet.
    """

    binding = frozen_specification_binding()
    first_snapshot = (
        EvidenceAcquisitionAuthority()
        .authorize(authorization_id="a1", binding=binding)
        .open_run("r1")
        .ingest(snapshot_id="s1", payload="same content", trace="same-trace")
    )
    second_snapshot = (
        EvidenceAcquisitionAuthority()
        .authorize(authorization_id="a1", binding=binding)
        .open_run("r1")
        .ingest(snapshot_id="s1", payload="same content", trace="same-trace")
    )

    assert first_snapshot is not second_snapshot
    assert first_snapshot == second_snapshot
    assert first_snapshot.content_id == second_snapshot.content_id


def test_g0_2a_binds_executable_semantics_without_birth_verdict() -> None:
    semantics = assessment_semantics()

    assert semantics.residual_definition.residual_id == (
        semantics.specification.residual_definition_id
    )
    assert semantics.closure_criterion.criterion_id == (
        semantics.specification.closure_criterion_id
    )
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
        BirthAssessmentSemanticsContract(
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


def test_executable_semantics_reject_residual_definition_drift() -> None:
    with pytest.raises(
        BirthExperimentSpecificationError, match="residual definition id"
    ):
        BirthAssessmentSemanticsContract(
            specification=specification(),
            residual_definition=ResidualDefinitionSpec(
                residual_id="changed-residual",
                domain="finite-domain",
                input_projection="sequence",
                output_schema="residual-schema",
                evaluator_id="residual-evaluator",
                invariants=("total-domain-coverage",),
                failure_semantics="malformed residual inputs defer assessment",
            ),
            weaker_models=weaker_model_specs(),
            closure_criterion=ClosureCriterionSpec(
                criterion_id="closure",
                residual_id="changed-residual",
                domain="finite-domain",
                residual_schema="residual-schema",
                model_result_schema="projection-result",
                evaluator_id="closure-evaluator",
                failure_semantics="untestable closure inputs defer assessment",
            ),
        )


def test_executable_semantics_reject_closure_criterion_drift() -> None:
    with pytest.raises(BirthExperimentSpecificationError, match="closure criterion id"):
        BirthAssessmentSemanticsContract(
            specification=specification(),
            residual_definition=residual_definition(),
            weaker_models=weaker_model_specs(),
            closure_criterion=ClosureCriterionSpec(
                criterion_id="changed-closure",
                residual_id="residual",
                domain="finite-domain",
                residual_schema="residual-schema",
                model_result_schema="projection-result",
                evaluator_id="closure-evaluator",
                failure_semantics="untestable closure inputs defer assessment",
            ),
        )


def test_executable_semantics_require_exact_weaker_cone_coverage() -> None:
    with pytest.raises(BirthExperimentSpecificationError, match="prerequisite cone"):
        BirthAssessmentSemanticsContract(
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
        BirthAssessmentSemanticsContract(
            specification=specification(),
            residual_definition=residual_definition(),
            weaker_models=(*weaker_models[:2], malformed),
            closure_criterion=closure_criterion(),
        )


def test_executable_semantics_bind_closure_to_residual_schema() -> None:
    with pytest.raises(BirthExperimentSpecificationError, match="residual schema"):
        BirthAssessmentSemanticsContract(
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


def authorized_registry() -> BirthAssessmentEvaluatorRegistry:
    registry = BirthAssessmentEvaluatorRegistry()
    registry.authorize(
        domain="finite-domain",
        role=BirthEvaluatorRole.RESIDUAL_DEFINITION,
        target_id="residual",
        evaluator_id="residual-evaluator",
    )
    registry.authorize(
        domain="finite-domain",
        role=BirthEvaluatorRole.CLOSURE_CRITERION,
        target_id="closure",
        evaluator_id="closure-evaluator",
    )
    for model in weaker_model_specs():
        registry.authorize(
            domain="finite-domain",
            role=BirthEvaluatorRole.WEAKER_MODEL,
            target_id=model.model_id,
            evaluator_id=model.projection_evaluator_id,
        )
    return registry


def test_declared_evaluator_id_is_not_an_authorized_evaluator() -> None:
    with pytest.raises(BirthAssessmentEvaluatorAuthorityError, match="registry-issued"):
        AuthorizedBirthAssessmentEvaluatorDefinition(
            domain="finite-domain",
            role=BirthEvaluatorRole.RESIDUAL_DEFINITION,
            target_id="residual",
            evaluator_id=residual_definition().evaluator_id,
        )


def test_sealed_registry_authorizes_declared_evaluator_scopes() -> None:
    definitions = BirthAssessmentEvaluatorDefinitions(
        contract=assessment_semantics(),
        registry_snapshot=authorized_registry().seal("registry-snapshot"),
    )

    assert definitions.residual_definition.evaluator_id == "residual-evaluator"
    assert tuple(definition.target_id for definition in definitions.weaker_models) == (
        "count",
        "set",
        "multiset",
    )
    assert definitions.closure_criterion.evaluator_id == "closure-evaluator"


def test_evaluator_authorization_requires_exact_declared_scope() -> None:
    registry = authorized_registry()
    registry.authorize(
        domain="other-domain",
        role=BirthEvaluatorRole.RESIDUAL_DEFINITION,
        target_id="residual",
        evaluator_id="untrusted-residual-evaluator",
    )

    with pytest.raises(BirthAssessmentEvaluatorAuthorityError, match="not authorized"):
        BirthAssessmentEvaluatorDefinitions(
            contract=BirthAssessmentSemanticsContract(
                specification=specification(),
                residual_definition=ResidualDefinitionSpec(
                    residual_id="residual",
                    domain="finite-domain",
                    input_projection="sequence",
                    output_schema="residual-schema",
                    evaluator_id="untrusted-residual-evaluator",
                    invariants=("total-domain-coverage",),
                    failure_semantics="malformed residual inputs defer assessment",
                ),
                weaker_models=weaker_model_specs(),
                closure_criterion=closure_criterion(),
            ),
            registry_snapshot=registry.seal("registry-snapshot"),
        )
