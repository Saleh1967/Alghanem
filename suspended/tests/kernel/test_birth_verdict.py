import pytest

from alghanem.kernel.birth import (
    BirthAssessmentRequest,
    BirthExperimentSpecification,
    BirthQuery,
    BirthVerdictStatus,
    EvidenceMode,
    ProjectionPoset,
    StructureHypothesis,
)
from alghanem.kernel.birth_verdict import (
    AuthorizedBirthVerdictScope,
    BirthVerdictAuthorityError,
    BirthVerdictDecision,
    BirthVerdictGate,
    BirthVerdictScopeRegistry,
    SealedBirthVerdictScopeRegistry,
)
from alghanem.kernel.evidence_acquisition import EvidenceAcquisitionAuthority
from alghanem.kernel.experiment_spec_content_identity import (
    BirthExperimentSpecificationContentBinding,
    CanonicalBirthExperimentSpecificationEncoder,
    PreEvidenceSpecificationRegistry,
)


def specification(
    *,
    experiment_id: str = "experiment",
    projections: tuple[str, ...] = ("count", "set", "multiset", "sequence"),
    strict_relations: tuple[tuple[str, str], ...] = (
        ("count", "multiset"),
        ("set", "multiset"),
        ("multiset", "sequence"),
    ),
    test_model: str = "sequence",
) -> BirthExperimentSpecification:
    return BirthExperimentSpecification(
        experiment_id=experiment_id,
        revision_id="r1",
        revision_sequence=1,
        evidence_mode=EvidenceMode.FORMAL,
        domain="finite-domain",
        projection_poset=ProjectionPoset(projections, strict_relations),
        birth_query=BirthQuery(
            "query",
            StructureHypothesis("structure", "a structure is necessary"),
            test_model,
        ),
        residual_definition_id="residual",
        residual_definition="unexplained distinction",
        closure_criterion_id="closure",
        closure_criterion="all prerequisite models fail to close the residual",
        evidence_requirements="exhaustive proof over the finite domain",
    )


def frozen_binding(
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
    run = authorization.open_run("run")
    snapshot = run.ingest(
        snapshot_id="snapshot", payload="enumeration", trace="acquisition-trace"
    )
    return BirthAssessmentRequest(
        experiment_binding=binding, evidence_snapshot=snapshot
    )


def sealed_registry_for(
    binding: BirthExperimentSpecificationContentBinding,
) -> SealedBirthVerdictScopeRegistry:
    registry = BirthVerdictScopeRegistry()
    registry.register(scope_id="scope", binding=binding)
    return registry.seal("registry-snapshot")


def test_scope_is_not_caller_constructible() -> None:
    binding = frozen_binding(specification())

    with pytest.raises(BirthVerdictAuthorityError, match="must be issued by"):
        AuthorizedBirthVerdictScope(scope_id="scope", binding=binding)


def test_sealed_registry_is_not_caller_constructible() -> None:
    binding = frozen_binding(specification())
    scope = BirthVerdictScopeRegistry().register(scope_id="scope", binding=binding)

    with pytest.raises(BirthVerdictAuthorityError, match="must be issued by"):
        SealedBirthVerdictScopeRegistry(snapshot_id="snapshot", scopes=(scope,))


def test_decision_is_not_caller_constructible() -> None:
    binding = frozen_binding(specification())
    registry = BirthVerdictScopeRegistry()
    scope = registry.register(scope_id="scope", binding=binding)
    request = assessment_request(binding)

    with pytest.raises(BirthVerdictAuthorityError, match="must be issued by"):
        BirthVerdictDecision(
            scope=scope,
            request=request,
            evidence_snapshot=request.evidence_snapshot,
            status=BirthVerdictStatus.BIRTH_IN_SCOPE,
            reason="a caller-declared birth",
            unresolved_competing_models=(),
            open_prerequisite_models=(),
        )


def test_scope_conditions_are_derived_from_the_frozen_binding() -> None:
    spec = specification()
    binding = frozen_binding(spec)

    scope = BirthVerdictScopeRegistry().register(scope_id="scope", binding=binding)

    assert scope.specification == spec
    assert scope.experiment_content_id == binding.content_id
    assert scope.domain == spec.domain
    assert scope.experiment_id == spec.experiment_id
    assert scope.revision_id == spec.revision_id
    assert scope.revision_sequence == spec.revision_sequence
    assert scope.evidence_mode is spec.evidence_mode
    assert scope.test_model == spec.birth_query.test_model


def test_registry_rejects_a_repeated_scope_id() -> None:
    registry = BirthVerdictScopeRegistry()
    registry.register(scope_id="scope", binding=frozen_binding(specification()))

    with pytest.raises(BirthVerdictAuthorityError, match="scope id already issued"):
        registry.register(
            scope_id="scope",
            binding=frozen_binding(specification(experiment_id="other")),
        )


def test_registry_rejects_a_repeated_frozen_experiment() -> None:
    registry = BirthVerdictScopeRegistry()
    registry.register(scope_id="scope", binding=frozen_binding(specification()))

    with pytest.raises(BirthVerdictAuthorityError, match="already authorized"):
        registry.register(
            scope_id="second-scope", binding=frozen_binding(specification())
        )


def test_assessment_requires_a_sealed_registry() -> None:
    binding = frozen_binding(specification())
    registry = BirthVerdictScopeRegistry()
    registry.register(scope_id="scope", binding=binding)

    with pytest.raises(BirthVerdictAuthorityError, match="sealed"):
        BirthVerdictGate.assess(
            registry=registry,  # type: ignore[arg-type]
            request=assessment_request(binding),
        )


def test_assessment_rejects_an_unregistered_frozen_experiment() -> None:
    registered = frozen_binding(specification())
    unregistered = frozen_binding(specification(experiment_id="unregistered"))

    with pytest.raises(BirthVerdictAuthorityError, match="no authorized verdict scope"):
        BirthVerdictGate.assess(
            registry=sealed_registry_for(registered),
            request=assessment_request(unregistered),
        )


def test_assessment_requires_an_authorized_request() -> None:
    binding = frozen_binding(specification())

    with pytest.raises(BirthVerdictAuthorityError, match="assessment request"):
        BirthVerdictGate.assess(
            registry=sealed_registry_for(binding),
            request=binding,  # type: ignore[arg-type]
        )


def test_gate_defers_on_an_open_prerequisite_cone() -> None:
    binding = frozen_binding(specification())
    request = assessment_request(binding)

    decision = BirthVerdictGate.assess(
        registry=sealed_registry_for(binding), request=request
    )

    assert decision.status is BirthVerdictStatus.DEFER_IN_SCOPE
    assert decision.is_birth is False
    assert decision.unresolved_competing_models == ()
    assert decision.open_prerequisite_models == ("count", "set", "multiset")
    assert "NoRicherStructureBeforeLowerOpenResidualClosure" in decision.reason
    assert decision.request is request
    assert decision.evidence_snapshot is request.evidence_snapshot


def test_gate_defers_on_unresolved_incomparable_competitors() -> None:
    spec = specification(
        projections=("count", "set", "multiset", "sequence"),
        strict_relations=(("count", "multiset"),),
        test_model="sequence",
    )
    binding = frozen_binding(spec)

    decision = BirthVerdictGate.assess(
        registry=sealed_registry_for(binding), request=assessment_request(binding)
    )

    assert decision.status is BirthVerdictStatus.DEFER_IN_SCOPE
    assert decision.unresolved_competing_models == ("count", "set", "multiset")
    assert "MultipleIncomparableMinimalFactorizationsDefer" in decision.reason


def test_gate_defers_even_with_no_competitor_and_no_prerequisite() -> None:
    spec = specification(
        projections=("sequence",), strict_relations=(), test_model="sequence"
    )
    binding = frozen_binding(spec)

    decision = BirthVerdictGate.assess(
        registry=sealed_registry_for(binding), request=assessment_request(binding)
    )

    assert decision.status is BirthVerdictStatus.DEFER_IN_SCOPE
    assert decision.unresolved_competing_models == ()
    assert decision.open_prerequisite_models == ()
    assert "NoBirthWithoutIndependentClosure" in decision.reason


def test_no_reachable_input_yields_a_birth_or_a_non_birth() -> None:
    for spec in (
        specification(),
        specification(strict_relations=(("count", "multiset"),)),
        specification(projections=("sequence",), strict_relations=()),
    ):
        binding = frozen_binding(spec)

        decision = BirthVerdictGate.assess(
            registry=sealed_registry_for(binding), request=assessment_request(binding)
        )

        assert decision.status is BirthVerdictStatus.DEFER_IN_SCOPE
        assert decision.is_birth is False
