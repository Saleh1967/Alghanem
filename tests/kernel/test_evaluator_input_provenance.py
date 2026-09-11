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
    BirthEvaluatorExecutionError,
    BirthEvaluatorExecutionGate,
    BirthEvaluatorExecutionRecord,
    BirthEvaluatorImplementationRegistry,
    SealedBirthEvaluatorImplementationRegistry,
)
from alghanem.kernel.evaluator_input_provenance import (
    AuthorizedEvaluatorInputDerivationBinding,
    CanonicalEvaluatorInputDerivationEncoder,
    CanonicalEvaluatorInputDerivationManifest,
    EvaluatorInputContentIdentity,
    EvaluatorInputDerivationGate,
    EvaluatorInputDerivationRegistry,
    EvaluatorInputProvenanceError,
    EvidenceDerivedEvaluatorInput,
    ProvenanceBoundEvaluatorExecutionGate,
    ProvenanceBoundEvaluatorExecutionRecord,
    SealedEvaluatorInputDerivationRegistry,
)
from alghanem.kernel.evidence_acquisition import EvidenceAcquisitionAuthority
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
            ("count", "multiset", "sequence"),
            (("count", "multiset"), ("multiset", "sequence")),
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


def assessment_request(payload: str = "enumeration") -> BirthAssessmentRequest:
    binding = frozen_specification_binding()
    authorization = EvidenceAcquisitionAuthority().authorize(
        authorization_id="authorization", binding=binding
    )
    snapshot = authorization.open_run("run").ingest(
        snapshot_id="snapshot", payload=payload, trace="acquisition-trace"
    )
    return BirthAssessmentRequest(
        experiment_binding=binding, evidence_snapshot=snapshot
    )


def uppercase_derivation(source_bytes: bytes) -> str:
    return source_bytes.decode("utf-8", "surrogatepass").upper()


def sealed_derivation_registry(
    *,
    domain: str = "finite-domain",
    derivation_id: str = "uppercase",
    implementation_identity: str = "uppercase-v1",
    derivation=uppercase_derivation,
) -> SealedEvaluatorInputDerivationRegistry:
    registry = EvaluatorInputDerivationRegistry()
    registry.register(
        domain=domain,
        derivation_id=derivation_id,
        implementation_identity=implementation_identity,
        declared_transformation="uppercase the authorized evidence bytes",
        derivation=derivation,
    )
    return registry.seal("derivation-snapshot")


def derived_input(
    request: BirthAssessmentRequest | None = None,
    **kwargs: object,
) -> EvidenceDerivedEvaluatorInput:
    return EvaluatorInputDerivationGate.derive(
        registry=sealed_derivation_registry(**kwargs),  # type: ignore[arg-type]
        request=request if request is not None else assessment_request(),
        derivation_id="uppercase",
        implementation_identity="uppercase-v1",
    )


def authorized_definition() -> AuthorizedBirthAssessmentEvaluatorDefinition:
    return BirthAssessmentEvaluatorRegistry().authorize(
        domain="finite-domain",
        role=BirthEvaluatorRole.RESIDUAL_DEFINITION,
        target_id="residual",
        evaluator_id="residual-evaluator",
    )


def passthrough_implementation(content: str) -> tuple[str, Trace]:
    return f"processed:{content}", Trace(("evaluated",))


def sealed_implementation_registry(
    definition: AuthorizedBirthAssessmentEvaluatorDefinition,
) -> SealedBirthEvaluatorImplementationRegistry:
    registry = BirthEvaluatorImplementationRegistry()
    registry.register(definition, "impl-v1", passthrough_implementation)
    return registry.seal("registry-snapshot")


# --- Positive path -----------------------------------------------------


def test_gate_derives_input_from_the_requests_own_evidence() -> None:
    request = assessment_request()

    result = derived_input(request)

    assert type(result) is EvidenceDerivedEvaluatorInput
    assert result.input_content == "ENUMERATION"
    assert result.request is request
    assert result.evidence_snapshot is request.evidence_snapshot
    assert result.source_content_id == request.evidence_snapshot.content_id
    assert result.domain == "finite-domain"
    assert result.derivation_id == "uppercase"
    assert result.implementation_identity == "uppercase-v1"
    assert type(result.content_id) is EvaluatorInputContentIdentity
    assert result.trace.events[1].endswith("snapshot")


def test_provenance_bound_execution_runs_on_derived_input_only() -> None:
    definition = authorized_definition()
    result = derived_input()

    record = ProvenanceBoundEvaluatorExecutionGate.execute(
        definition=definition,
        implementation_identity="impl-v1",
        registry=sealed_implementation_registry(definition),
        derived_input=result,
    )

    assert type(record) is ProvenanceBoundEvaluatorExecutionRecord
    assert type(record.execution_record) is BirthEvaluatorExecutionRecord
    assert record.definition == definition
    assert record.role is BirthEvaluatorRole.RESIDUAL_DEFINITION
    assert record.target_id == "residual"
    assert record.input_content == result.input_content
    assert record.output_content == "processed:ENUMERATION"
    assert record.trace.events == ("evaluated",)
    assert record.evidence_content_id == result.evidence_snapshot.content_id
    assert record.input_content_id == result.content_id


# --- Identity binds source, derivation, and output ---------------------


def test_identity_changes_when_the_evidence_payload_changes() -> None:
    first = derived_input(assessment_request("enumeration"))
    second = derived_input(assessment_request("other-enumeration"))

    assert first.content_id != second.content_id


def test_identity_changes_when_the_declared_derivation_changes() -> None:
    request = assessment_request()
    first = derived_input(request)
    second = EvaluatorInputDerivationGate.derive(
        registry=sealed_derivation_registry(
            derivation_id="shout", implementation_identity="shout-v1"
        ),
        request=request,
        derivation_id="shout",
        implementation_identity="shout-v1",
    )

    assert first.input_content == second.input_content
    assert first.content_id != second.content_id


def test_identical_evidence_and_derivation_share_one_identity() -> None:
    first = derived_input(assessment_request("enumeration"))
    second = derived_input(assessment_request("enumeration"))

    assert first.request is not second.request
    assert first.content_id == second.content_id


def test_encoder_rejects_a_fabricated_source_identity() -> None:
    with pytest.raises(EvaluatorInputProvenanceError):
        CanonicalEvaluatorInputDerivationEncoder.encode(
            source_content_id="not-an-identity",  # type: ignore[arg-type]
            derivation_id="uppercase",
            implementation_identity="uppercase-v1",
            input_content="ENUMERATION",
        )


# --- Authority boundaries ----------------------------------------------


def test_derived_inputs_are_not_caller_constructible() -> None:
    result = derived_input()

    with pytest.raises(EvaluatorInputProvenanceError):
        EvidenceDerivedEvaluatorInput(
            binding=result.binding,
            request=result.request,
            evidence_snapshot=result.evidence_snapshot,
            source_content_id=result.source_content_id,
            input_content=result.input_content,
            derivation_manifest=result.derivation_manifest,
            trace=result.trace,
        )


def test_provenance_bound_records_are_not_caller_constructible() -> None:
    definition = authorized_definition()
    result = derived_input()
    record = ProvenanceBoundEvaluatorExecutionGate.execute(
        definition=definition,
        implementation_identity="impl-v1",
        registry=sealed_implementation_registry(definition),
        derived_input=result,
    )

    with pytest.raises(EvaluatorInputProvenanceError):
        ProvenanceBoundEvaluatorExecutionRecord(
            execution_record=record.execution_record,
            derived_input=result,
        )


def test_derivation_bindings_are_not_caller_constructible() -> None:
    with pytest.raises(EvaluatorInputProvenanceError):
        AuthorizedEvaluatorInputDerivationBinding(
            domain="finite-domain",
            derivation_id="uppercase",
            implementation_identity="uppercase-v1",
            declared_transformation="uppercase",
            derivation=uppercase_derivation,
        )


def test_manifests_and_identities_are_not_caller_constructible() -> None:
    with pytest.raises(EvaluatorInputProvenanceError):
        EvaluatorInputContentIdentity(
            algorithm="sha256",
            canonicalization_version="evaluator-input-derivation-manifest-v1",
            digest="0" * 64,
        )
    with pytest.raises(EvaluatorInputProvenanceError):
        CanonicalEvaluatorInputDerivationManifest(
            canonical_bytes=b"", content_id=derived_input().content_id
        )


def test_sealed_registries_are_not_caller_constructible() -> None:
    with pytest.raises(EvaluatorInputProvenanceError):
        SealedEvaluatorInputDerivationRegistry(snapshot_id="snapshot", bindings=())


def test_registry_rejects_a_duplicate_derivation_scope() -> None:
    registry = EvaluatorInputDerivationRegistry()
    registry.register(
        domain="finite-domain",
        derivation_id="uppercase",
        implementation_identity="uppercase-v1",
        declared_transformation="uppercase",
        derivation=uppercase_derivation,
    )

    with pytest.raises(EvaluatorInputProvenanceError):
        registry.register(
            domain="finite-domain",
            derivation_id="uppercase",
            implementation_identity="uppercase-v1",
            declared_transformation="uppercase again",
            derivation=uppercase_derivation,
        )


def test_unregistered_derivation_scope_cannot_derive() -> None:
    with pytest.raises(EvaluatorInputProvenanceError):
        EvaluatorInputDerivationGate.derive(
            registry=sealed_derivation_registry(),
            request=assessment_request(),
            derivation_id="uppercase",
            implementation_identity="an-identity-nobody-registered",
        )


def test_a_derivation_registered_for_another_domain_cannot_derive() -> None:
    with pytest.raises(EvaluatorInputProvenanceError):
        EvaluatorInputDerivationGate.derive(
            registry=sealed_derivation_registry(domain="another-domain"),
            request=assessment_request(),
            derivation_id="uppercase",
            implementation_identity="uppercase-v1",
        )


def test_gate_requires_a_sealed_registry_and_an_authorized_request() -> None:
    with pytest.raises(EvaluatorInputProvenanceError):
        EvaluatorInputDerivationGate.derive(
            registry=EvaluatorInputDerivationRegistry(),  # type: ignore[arg-type]
            request=assessment_request(),
            derivation_id="uppercase",
            implementation_identity="uppercase-v1",
        )
    with pytest.raises(EvaluatorInputProvenanceError):
        EvaluatorInputDerivationGate.derive(
            registry=sealed_derivation_registry(),
            request="not-a-request",  # type: ignore[arg-type]
            derivation_id="uppercase",
            implementation_identity="uppercase-v1",
        )


def test_execution_gate_refuses_caller_supplied_input_content() -> None:
    definition = authorized_definition()

    with pytest.raises(EvaluatorInputProvenanceError):
        ProvenanceBoundEvaluatorExecutionGate.execute(
            definition=definition,
            implementation_identity="impl-v1",
            registry=sealed_implementation_registry(definition),
            derived_input="raw-evidence",  # type: ignore[arg-type]
        )


def test_execution_gate_still_requires_a_bound_implementation() -> None:
    definition = authorized_definition()

    with pytest.raises(BirthEvaluatorExecutionError):
        ProvenanceBoundEvaluatorExecutionGate.execute(
            definition=definition,
            implementation_identity="an-implementation-nobody-registered",
            registry=sealed_implementation_registry(definition),
            derived_input=derived_input(),
        )


# --- Derivation discipline ---------------------------------------------


def test_a_derivation_returning_non_text_is_rejected() -> None:
    with pytest.raises(EvaluatorInputProvenanceError):
        EvaluatorInputDerivationGate.derive(
            registry=sealed_derivation_registry(
                derivation=lambda source: len(source)  # type: ignore[arg-type,return-value]
            ),
            request=assessment_request(),
            derivation_id="uppercase",
            implementation_identity="uppercase-v1",
        )


def test_a_derivation_returning_blank_content_is_rejected() -> None:
    with pytest.raises(EvaluatorInputProvenanceError):
        EvaluatorInputDerivationGate.derive(
            registry=sealed_derivation_registry(derivation=lambda source: "   "),
            request=assessment_request(),
            derivation_id="uppercase",
            implementation_identity="uppercase-v1",
        )


def test_an_observably_nondeterministic_derivation_is_rejected() -> None:
    counter = {"calls": 0}

    def unstable(source_bytes: bytes) -> str:
        counter["calls"] += 1
        return f"{source_bytes.decode()}-{counter['calls']}"

    with pytest.raises(EvaluatorInputProvenanceError):
        EvaluatorInputDerivationGate.derive(
            registry=sealed_derivation_registry(derivation=unstable),
            request=assessment_request(),
            derivation_id="uppercase",
            implementation_identity="uppercase-v1",
        )


# --- Preserved non-claims ----------------------------------------------


def test_g0_ba_1a_still_accepts_unrelated_input_content() -> None:
    """This stage layers above G0.BA.1a; it does not weaken it.

    ``BirthEvaluatorExecutionGate`` keeps ``InputProvenance =
    DECLARED_DEFERRED`` exactly as before. Provenance is proven only for
    records issued by ``ProvenanceBoundEvaluatorExecutionGate``.
    """

    definition = authorized_definition()
    request = assessment_request()

    record = BirthEvaluatorExecutionGate.execute(
        definition=definition,
        implementation_identity="impl-v1",
        registry=sealed_implementation_registry(definition),
        request=request,
        input_content="unrelated-to-evidence-payload",
    )

    assert type(record) is BirthEvaluatorExecutionRecord
    assert (
        record.input_content.encode()
        != request.evidence_snapshot.evidence_manifest.canonical_bytes
    )


def test_proven_provenance_is_not_an_assessment() -> None:
    definition = authorized_definition()
    record = ProvenanceBoundEvaluatorExecutionGate.execute(
        definition=definition,
        implementation_identity="impl-v1",
        registry=sealed_implementation_registry(definition),
        derived_input=derived_input(),
    )

    assert record.is_assessment is False
    field_names = set(ProvenanceBoundEvaluatorExecutionRecord.__dataclass_fields__)
    for forbidden in (
        "status",
        "verdict",
        "residual_survived",
        "weaker_models_exhausted",
        "closure",
        "birth_candidate",
        "freeze",
    ):
        assert forbidden not in field_names
        assert not hasattr(record, forbidden)
