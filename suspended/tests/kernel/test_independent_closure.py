import pytest

from alghanem.kernel.birth import (
    BirthAssessmentRequest,
    BirthExperimentSpecification,
    BirthQuery,
    EvidenceMode,
    ProjectionPoset,
    StructureHypothesis,
)
from alghanem.kernel.evidence_acquisition import EvidenceAcquisitionAuthority
from alghanem.kernel.experiment_spec_content_identity import (
    BirthExperimentSpecificationContentBinding,
    CanonicalBirthExperimentSpecificationEncoder,
    PreEvidenceSpecificationRegistry,
)
from alghanem.kernel.independent_closure import (
    AuthorizedClosureScope,
    ClosureScopeRegistry,
    ComparabilityClosureStatus,
    IndependentClosureAssessment,
    IndependentClosureAuthorityError,
    IndependentClosureGate,
    SealedClosureScopeRegistry,
)

CHAIN_PROJECTIONS = ("count", "set", "multiset", "sequence")
CHAIN_RELATIONS = (
    ("count", "multiset"),
    ("set", "multiset"),
    ("multiset", "sequence"),
)


def specification(
    *,
    experiment_id: str = "experiment",
    projections: tuple[str, ...] = CHAIN_PROJECTIONS,
    strict_relations: tuple[tuple[str, str], ...] = CHAIN_RELATIONS,
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
) -> SealedClosureScopeRegistry:
    registry = ClosureScopeRegistry()
    registry.register(scope_id="scope", binding=binding)
    return registry.seal("registry-snapshot")


def test_scope_is_not_caller_constructible() -> None:
    binding = frozen_binding(specification())

    with pytest.raises(IndependentClosureAuthorityError, match="must be issued by"):
        AuthorizedClosureScope(scope_id="scope", binding=binding)


def test_sealed_registry_is_not_caller_constructible() -> None:
    binding = frozen_binding(specification())
    scope = ClosureScopeRegistry().register(scope_id="scope", binding=binding)

    with pytest.raises(IndependentClosureAuthorityError, match="must be issued by"):
        SealedClosureScopeRegistry(snapshot_id="snapshot", scopes=(scope,))


def test_assessment_is_not_caller_constructible() -> None:
    binding = frozen_binding(specification())
    scope = ClosureScopeRegistry().register(scope_id="scope", binding=binding)
    request = assessment_request(binding)

    with pytest.raises(IndependentClosureAuthorityError, match="must be issued by"):
        IndependentClosureAssessment(
            scope=scope,
            request=request,
            evidence_snapshot=request.evidence_snapshot,
            status=ComparabilityClosureStatus.COMPETITION_RESOLVED_IN_POSET,
            reason="a caller-declared closure",
            incomparable_competitors=(),
            open_prerequisite_models=(),
        )


def test_unsealed_registry_is_rejected_by_the_gate() -> None:
    binding = frozen_binding(specification())
    registry = ClosureScopeRegistry()
    registry.register(scope_id="scope", binding=binding)

    with pytest.raises(IndependentClosureAuthorityError, match="sealed closure scope"):
        IndependentClosureGate.assess(
            registry=registry,  # type: ignore[arg-type]
            request=assessment_request(binding),
        )


def test_unregistered_experiment_is_rejected_by_the_gate() -> None:
    registered = frozen_binding(specification(experiment_id="registered"))
    other = frozen_binding(specification(experiment_id="other"))

    with pytest.raises(
        IndependentClosureAuthorityError, match="no authorized closure scope"
    ):
        IndependentClosureGate.assess(
            registry=sealed_registry_for(registered),
            request=assessment_request(other),
        )


def test_duplicate_scope_id_is_rejected() -> None:
    registry = ClosureScopeRegistry()
    registry.register(scope_id="scope", binding=frozen_binding(specification()))

    with pytest.raises(IndependentClosureAuthorityError, match="already issued"):
        registry.register(
            scope_id="scope",
            binding=frozen_binding(specification(experiment_id="other")),
        )


def test_duplicate_frozen_experiment_is_rejected() -> None:
    registry = ClosureScopeRegistry()
    registry.register(scope_id="first", binding=frozen_binding(specification()))

    with pytest.raises(IndependentClosureAuthorityError, match="already authorized"):
        registry.register(scope_id="second", binding=frozen_binding(specification()))


def test_scope_conditions_are_derived_from_the_frozen_binding() -> None:
    binding = frozen_binding(specification())
    scope = ClosureScopeRegistry().register(scope_id="scope", binding=binding)

    assert scope.experiment_content_id == binding.content_id
    assert scope.domain == "finite-domain"
    assert scope.experiment_id == "experiment"
    assert scope.revision_id == "r1"
    assert scope.revision_sequence == 1
    assert scope.evidence_mode is EvidenceMode.FORMAL
    assert scope.test_model == "sequence"


def test_a_chain_poset_resolves_competition() -> None:
    binding = frozen_binding(specification())

    assessment = IndependentClosureGate.assess(
        registry=sealed_registry_for(binding), request=assessment_request(binding)
    )

    assert assessment.status is ComparabilityClosureStatus.COMPETITION_RESOLVED_IN_POSET
    assert assessment.incomparable_competitors == ()
    assert assessment.open_prerequisite_models == ("count", "set", "multiset")
    assert "ComparabilityResolvedInFrozenPoset" in assessment.reason


def test_an_incomparable_projection_leaves_competition_unresolved() -> None:
    binding = frozen_binding(specification(test_model="count"))

    assessment = IndependentClosureGate.assess(
        registry=sealed_registry_for(binding), request=assessment_request(binding)
    )

    assert (
        assessment.status is ComparabilityClosureStatus.COMPETITION_UNRESOLVED_IN_POSET
    )
    assert assessment.incomparable_competitors == ("set",)
    assert "MultipleIncomparableMinimalFactorizationsDefer" in assessment.reason


def test_an_undetermined_relation_is_never_read_as_resolution() -> None:
    """A poset cannot tell `incomparable` from `relation never determined`.

    Both appear as the absence of a strict relation, so the gate must treat
    both as unresolved competition rather than as a resolved comparison.
    """

    binding = frozen_binding(
        specification(projections=CHAIN_PROJECTIONS, strict_relations=())
    )

    assessment = IndependentClosureGate.assess(
        registry=sealed_registry_for(binding), request=assessment_request(binding)
    )

    assert (
        assessment.status is ComparabilityClosureStatus.COMPETITION_UNRESOLVED_IN_POSET
    )
    assert assessment.incomparable_competitors == ("count", "set", "multiset")
    assert assessment.open_prerequisite_models == ()


def test_no_reachable_input_yields_an_independent_closure() -> None:
    """Both statuses are reachable, but neither is `IndependentClosure`.

    Comparability is one conjunct of closure; residual survival and licensed
    weaker exhaustion have no authority in this repository, so no assessment
    may be read as a closure.
    """

    reached = set()
    for test_model in ("sequence", "count"):
        binding = frozen_binding(specification(test_model=test_model))
        assessment = IndependentClosureGate.assess(
            registry=sealed_registry_for(binding), request=assessment_request(binding)
        )
        reached.add(assessment.status)
        assert assessment.is_independent_closure is False

    assert reached == set(ComparabilityClosureStatus)


def test_the_assessment_preserves_its_own_request_and_evidence() -> None:
    binding = frozen_binding(specification())
    request = assessment_request(binding)

    assessment = IndependentClosureGate.assess(
        registry=sealed_registry_for(binding), request=request
    )

    assert assessment.request is request
    assert assessment.evidence_snapshot is request.evidence_snapshot
    assert assessment.scope.specification == request.specification
