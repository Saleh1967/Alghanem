import pytest

from alghanem.kernel.birth import (
    AuthorizedBirthAssessmentEvaluatorDefinition,
    BirthAssessmentEvaluatorRegistry,
    BirthAssessmentRequest,
    BirthEvaluatorRole,
    BirthExperimentSpecification,
    BirthQuery,
    EvidenceMode,
    ProjectionPoset,
    StructureHypothesis,
)
from alghanem.kernel.evaluator_execution import (
    AuthorizedBirthEvaluatorImplementationBinding,
    BirthEvaluatorExecutionError,
    BirthEvaluatorExecutionGate,
    BirthEvaluatorExecutionRecord,
    BirthEvaluatorImplementationRegistry,
    SealedBirthEvaluatorImplementationRegistry,
)
from alghanem.kernel.evidence_acquisition import (
    AuthorizedEvidenceSnapshot,
    EvidenceAcquisitionAuthority,
)
from alghanem.kernel.experiment_spec_content_identity import (
    BirthExperimentSpecificationContentBinding,
    CanonicalBirthExperimentSpecificationEncoder,
    PreEvidenceSpecificationRegistry,
)
from alghanem.kernel.trace import Trace


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


def authorized_evidence_snapshot() -> AuthorizedEvidenceSnapshot:
    binding = frozen_specification_binding()
    authorization = EvidenceAcquisitionAuthority().authorize(
        authorization_id="authorization",
        binding=binding,
    )
    run = authorization.open_run("run")
    return run.ingest(
        snapshot_id="snapshot", payload="enumeration", trace="acquisition-trace"
    )


def assessment_request() -> BirthAssessmentRequest:
    return BirthAssessmentRequest(
        experiment_binding=frozen_specification_binding(),
        evidence_snapshot=authorized_evidence_snapshot(),
    )


def authorized_definition(
    *,
    domain: str = "finite-domain",
    role: BirthEvaluatorRole = BirthEvaluatorRole.RESIDUAL_DEFINITION,
    target_id: str = "residual",
    evaluator_id: str = "residual-evaluator",
) -> AuthorizedBirthAssessmentEvaluatorDefinition:
    registry = BirthAssessmentEvaluatorRegistry()
    return registry.authorize(
        domain=domain,
        role=role,
        target_id=target_id,
        evaluator_id=evaluator_id,
    )


def passthrough_implementation(content: str) -> tuple[str, Trace]:
    return f"processed:{content}", Trace(("evaluated",))


def sealed_registry_with(
    definition: AuthorizedBirthAssessmentEvaluatorDefinition,
    *,
    implementation_identity: str = "impl-v1",
    implementation=passthrough_implementation,
) -> SealedBirthEvaluatorImplementationRegistry:
    registry = BirthEvaluatorImplementationRegistry()
    registry.register(definition, implementation_identity, implementation)
    return registry.seal("registry-snapshot")


# --- Positive path -----------------------------------------------------


def test_execution_gate_issues_a_record_for_a_bound_implementation() -> None:
    definition = authorized_definition()
    registry = sealed_registry_with(definition)
    request = assessment_request()

    record = BirthEvaluatorExecutionGate.execute(
        definition=definition,
        implementation_identity="impl-v1",
        registry=registry,
        request=request,
        input_content="raw-evidence",
    )

    assert type(record) is BirthEvaluatorExecutionRecord
    assert record.definition == definition
    assert record.implementation_identity == "impl-v1"
    assert record.role is BirthEvaluatorRole.RESIDUAL_DEFINITION
    assert record.target_id == "residual"
    assert record.request is request
    assert record.evidence_snapshot is request.evidence_snapshot
    assert record.input_content == "raw-evidence"
    assert record.output_content == "processed:raw-evidence"
    assert record.trace.events == ("evaluated",)


def test_execution_record_carries_no_assessment_or_verdict_authority() -> None:
    field_names = set(BirthEvaluatorExecutionRecord.__dataclass_fields__)
    forbidden = {
        "birth",
        "verdict",
        "freeze",
        "assessment",
        "residual_survived",
        "weaker_exhausted",
        "closure",
        "status",
    }
    assert not (field_names & forbidden)


# --- Definition/implementation separation -------------------------------


def test_evaluator_id_alone_cannot_execute() -> None:
    """A bare evaluator id string, without a registry-issued definition,
    cannot resolve or execute anything."""

    with pytest.raises(BirthEvaluatorExecutionError, match="authorized evaluator"):
        BirthEvaluatorExecutionGate.execute(
            definition="residual-evaluator",  # type: ignore[arg-type]
            implementation_identity="impl-v1",
            registry=sealed_registry_with(authorized_definition()),
            request=assessment_request(),
            input_content="raw-evidence",
        )


def test_callers_cannot_construct_an_implementation_binding_directly() -> None:
    definition = authorized_definition()
    with pytest.raises(BirthEvaluatorExecutionError, match="Registry"):
        AuthorizedBirthEvaluatorImplementationBinding(
            definition, "impl-v1", passthrough_implementation
        )


def test_callers_cannot_construct_an_execution_record_directly() -> None:
    definition = authorized_definition()
    request = assessment_request()
    with pytest.raises(BirthEvaluatorExecutionError, match="ExecutionGate"):
        BirthEvaluatorExecutionRecord(
            definition,
            "impl-v1",
            definition.role,
            definition.target_id,
            request,
            request.evidence_snapshot,
            "raw-evidence",
            "processed:raw-evidence",
            Trace(("evaluated",)),
        )


def test_implementation_binding_requires_a_genuine_authorized_definition() -> None:
    registry = BirthEvaluatorImplementationRegistry()
    with pytest.raises(BirthEvaluatorExecutionError, match="authorized evaluator"):
        registry.register(
            "residual-evaluator",  # type: ignore[arg-type]
            "impl-v1",
            passthrough_implementation,
        )


# --- Adversarial scope mismatches ----------------------------------------


def test_wrong_domain_definition_is_rejected() -> None:
    bound_definition = authorized_definition(domain="finite-domain")
    registry = sealed_registry_with(bound_definition)
    mismatched_definition = authorized_definition(domain="other-domain")

    with pytest.raises(BirthEvaluatorExecutionError, match="no authorized"):
        BirthEvaluatorExecutionGate.execute(
            definition=mismatched_definition,
            implementation_identity="impl-v1",
            registry=registry,
            request=assessment_request(),
            input_content="raw-evidence",
        )


def test_wrong_role_definition_is_rejected() -> None:
    bound_definition = authorized_definition(
        role=BirthEvaluatorRole.RESIDUAL_DEFINITION
    )
    registry = sealed_registry_with(bound_definition)
    mismatched_definition = authorized_definition(
        role=BirthEvaluatorRole.CLOSURE_CRITERION
    )

    with pytest.raises(BirthEvaluatorExecutionError, match="no authorized"):
        BirthEvaluatorExecutionGate.execute(
            definition=mismatched_definition,
            implementation_identity="impl-v1",
            registry=registry,
            request=assessment_request(),
            input_content="raw-evidence",
        )


def test_wrong_target_definition_is_rejected() -> None:
    bound_definition = authorized_definition(target_id="residual")
    registry = sealed_registry_with(bound_definition)
    mismatched_definition = authorized_definition(target_id="other-target")

    with pytest.raises(BirthEvaluatorExecutionError, match="no authorized"):
        BirthEvaluatorExecutionGate.execute(
            definition=mismatched_definition,
            implementation_identity="impl-v1",
            registry=registry,
            request=assessment_request(),
            input_content="raw-evidence",
        )


def test_wrong_evaluator_id_definition_is_rejected() -> None:
    bound_definition = authorized_definition(evaluator_id="residual-evaluator")
    registry = sealed_registry_with(bound_definition)
    mismatched_definition = authorized_definition(evaluator_id="other-evaluator")

    with pytest.raises(BirthEvaluatorExecutionError, match="no authorized"):
        BirthEvaluatorExecutionGate.execute(
            definition=mismatched_definition,
            implementation_identity="impl-v1",
            registry=registry,
            request=assessment_request(),
            input_content="raw-evidence",
        )


def test_implementation_identity_mismatch_is_rejected() -> None:
    definition = authorized_definition()
    registry = sealed_registry_with(definition, implementation_identity="impl-v1")

    with pytest.raises(BirthEvaluatorExecutionError, match="no authorized"):
        BirthEvaluatorExecutionGate.execute(
            definition=definition,
            implementation_identity="impl-v2-unregistered",
            registry=registry,
            request=assessment_request(),
            input_content="raw-evidence",
        )


def test_unsealed_registry_cannot_execute() -> None:
    definition = authorized_definition()
    unsealed_registry = BirthEvaluatorImplementationRegistry()
    unsealed_registry.register(definition, "impl-v1", passthrough_implementation)

    with pytest.raises(BirthEvaluatorExecutionError, match="sealed"):
        BirthEvaluatorExecutionGate.execute(
            definition=definition,
            implementation_identity="impl-v1",
            registry=unsealed_registry,  # type: ignore[arg-type]
            request=assessment_request(),
            input_content="raw-evidence",
        )


def test_registry_rejects_duplicate_implementation_binding() -> None:
    definition = authorized_definition()
    registry = BirthEvaluatorImplementationRegistry()
    registry.register(definition, "impl-v1", passthrough_implementation)

    with pytest.raises(BirthEvaluatorExecutionError, match="already bound"):
        registry.register(definition, "impl-v1", passthrough_implementation)


def test_malformed_implementation_output_is_rejected() -> None:
    def broken_implementation(content: str) -> tuple[str, Trace]:
        return content  # type: ignore[return-value]

    definition = authorized_definition()
    registry = sealed_registry_with(definition, implementation=broken_implementation)

    with pytest.raises(BirthEvaluatorExecutionError, match="output_content, trace"):
        BirthEvaluatorExecutionGate.execute(
            definition=definition,
            implementation_identity="impl-v1",
            registry=registry,
            request=assessment_request(),
            input_content="raw-evidence",
        )


# --- Request/evidence provenance preservation ---------------------------


def test_request_domain_must_match_the_authorized_definition_domain() -> None:
    definition = authorized_definition(domain="other-domain")
    registry = BirthEvaluatorImplementationRegistry()
    registry.register(definition, "impl-v1", passthrough_implementation)
    sealed = registry.seal("registry-snapshot")

    with pytest.raises(BirthEvaluatorExecutionError, match="domain"):
        BirthEvaluatorExecutionGate.execute(
            definition=definition,
            implementation_identity="impl-v1",
            registry=sealed,
            request=assessment_request(),
            input_content="raw-evidence",
        )


def test_execution_record_preserves_the_exact_request_and_evidence() -> None:
    definition = authorized_definition()
    registry = sealed_registry_with(definition)
    request = assessment_request()

    record = BirthEvaluatorExecutionGate.execute(
        definition=definition,
        implementation_identity="impl-v1",
        registry=registry,
        request=request,
        input_content="raw-evidence",
    )

    assert record.request is request
    assert record.evidence_snapshot is request.evidence_snapshot


# --- Acknowledged residuals: EvidenceAttachedToRecord != -----------------
# --- EvaluatorExecutedOnEvidence, and AuthorizedDefinition != ------------
# --- DefinitionAuthorizedForThisFrozenExperiment. These tests document ---
# --- the current, deliberately narrow scope of G0.BA.1a; they are not ---
# --- regression guards for a stronger guarantee that does not exist yet.-


def test_input_content_need_not_originate_from_the_evidence_payload() -> None:
    """InputProvenance = DECLARED_DEFERRED.

    The gate never compares ``input_content`` against the request's own
    evidence snapshot payload. This test makes that narrow scope explicit:
    a record is issued even though ``input_content`` shares nothing with the
    evidence snapshot's own canonical bytes, proving the gate performs an
    ``AuthorizedCallableInvocation``, not an
    ``AuthorizedAssessmentEvidenceExecution``.
    """

    definition = authorized_definition()
    registry = sealed_registry_with(definition)
    request = assessment_request()
    evidence_bytes = request.evidence_snapshot.evidence_manifest.canonical_bytes

    record = BirthEvaluatorExecutionGate.execute(
        definition=definition,
        implementation_identity="impl-v1",
        registry=registry,
        request=request,
        input_content="unrelated-to-evidence-payload",
    )

    assert record.input_content.encode() != evidence_bytes
    assert record.evidence_snapshot is request.evidence_snapshot


def test_definition_authorized_for_domain_need_not_be_bound_to_this_experiment() -> (
    None
):
    """AuthorizedDefinition != DefinitionAuthorizedForThisFrozenExperiment.

    The gate checks only that the resolved definition's ``domain`` matches
    the request's frozen experiment domain; it never checks the request's
    own ``BirthAssessmentContentBinding``/``BirthAssessmentEvaluatorDefinitions``.
    This test documents that a definition authorized in a registry that has
    no relationship whatsoever to this request's experiment can still
    execute against it, as long as the domain string matches.
    """

    unrelated_registry = BirthAssessmentEvaluatorRegistry()
    definition = unrelated_registry.authorize(
        domain="finite-domain",
        role=BirthEvaluatorRole.RESIDUAL_DEFINITION,
        target_id="an-unrelated-target",
        evaluator_id="an-unrelated-evaluator",
    )
    registry = sealed_registry_with(definition)
    request = assessment_request()

    record = BirthEvaluatorExecutionGate.execute(
        definition=definition,
        implementation_identity="impl-v1",
        registry=registry,
        request=request,
        input_content="raw-evidence",
    )

    assert record.definition == definition
    assert record.definition.target_id == "an-unrelated-target"
