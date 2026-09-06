from dataclasses import fields

import pytest

import alghanem.kernel.birth_content_identity as semantics_identity
from alghanem.kernel.birth import (
    BirthAssessmentSemanticsContract,
    BirthEvaluatorRole,
    BirthExperimentSpecification,
    BirthQuery,
    ClosureCriterionSpec,
    EvidenceMode,
    ProjectionPoset,
    ResidualDefinitionSpec,
    StructureHypothesis,
    WeakerModelSpec,
)
from alghanem.kernel.birth_content_identity import (
    CLOSURE_CRITERION_MANIFEST_COVERAGE,
    RESIDUAL_DEFINITION_MANIFEST_COVERAGE,
    WEAKER_MODEL_MANIFEST_COVERAGE,
    BirthAssessmentContentBinding,
    BirthSemanticsContentIdentity,
    BirthSemanticsContentIdentityError,
    BirthSemanticsContentRegistry,
    CanonicalBirthSemanticsEncoder,
    CanonicalResidualDefinitionManifest,
    FrozenBirthSemanticsContentScope,
)
from alghanem.kernel.experiment_spec_content_identity import (
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


def residual_definition(
    *,
    output_schema: str = "residual-schema",
    evaluator_id: str = "residual-evaluator",
    invariants: tuple[str, ...] = ("total-domain-coverage",),
    failure_semantics: str = "malformed residual inputs defer assessment",
) -> ResidualDefinitionSpec:
    return ResidualDefinitionSpec(
        residual_id="residual",
        domain="finite-domain",
        input_projection="sequence",
        output_schema=output_schema,
        evaluator_id=evaluator_id,
        invariants=invariants,
        failure_semantics=failure_semantics,
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


def closure_criterion(
    *, evaluator_id: str = "closure-evaluator"
) -> ClosureCriterionSpec:
    return ClosureCriterionSpec(
        criterion_id="closure",
        residual_id="residual",
        domain="finite-domain",
        residual_schema="residual-schema",
        model_result_schema="projection-result",
        evaluator_id=evaluator_id,
        failure_semantics="untestable closure inputs defer assessment",
    )


def assessment_semantics(
    *,
    residual: ResidualDefinitionSpec | None = None,
    closure: ClosureCriterionSpec | None = None,
) -> BirthAssessmentSemanticsContract:
    return BirthAssessmentSemanticsContract(
        specification=specification(),
        residual_definition=residual or residual_definition(),
        weaker_models=weaker_model_specs(),
        closure_criterion=closure or closure_criterion(),
    )


def sealed_registry_for(contract: BirthAssessmentSemanticsContract):
    registry = BirthSemanticsContentRegistry()
    domain = contract.specification.domain
    registry.freeze(
        domain=domain,
        role=BirthEvaluatorRole.RESIDUAL_DEFINITION,
        target_id=contract.residual_definition.residual_id,
        manifest=CanonicalBirthSemanticsEncoder.encode_residual_definition(
            contract.residual_definition
        ),
    )
    registry.freeze(
        domain=domain,
        role=BirthEvaluatorRole.CLOSURE_CRITERION,
        target_id=contract.closure_criterion.criterion_id,
        manifest=CanonicalBirthSemanticsEncoder.encode_closure_criterion(
            contract.closure_criterion
        ),
    )
    for model in contract.weaker_models:
        registry.freeze(
            domain=domain,
            role=BirthEvaluatorRole.WEAKER_MODEL,
            target_id=model.model_id,
            manifest=CanonicalBirthSemanticsEncoder.encode_weaker_model(model),
        )
    frozen_experiment = PreEvidenceSpecificationRegistry().freeze(
        CanonicalBirthExperimentSpecificationEncoder.encode(contract.specification)
    )
    return registry.seal("snapshot", frozen_experiment)


def test_canonical_encoding_is_deterministic_for_identical_content() -> None:
    first = CanonicalBirthSemanticsEncoder.encode_residual_definition(
        residual_definition()
    )
    second = CanonicalBirthSemanticsEncoder.encode_residual_definition(
        residual_definition()
    )

    assert first.content_id.digest == second.content_id.digest
    assert isinstance(first, CanonicalResidualDefinitionManifest)


def test_every_semantics_schema_field_is_covered_by_its_manifest() -> None:
    assert {item.name for item in fields(ResidualDefinitionSpec)} == set(
        RESIDUAL_DEFINITION_MANIFEST_COVERAGE
    )
    assert {item.name for item in fields(ClosureCriterionSpec)} == set(
        CLOSURE_CRITERION_MANIFEST_COVERAGE
    )
    assert {item.name for item in fields(WeakerModelSpec)} == set(
        WEAKER_MODEL_MANIFEST_COVERAGE
    )


def test_encoder_rejects_an_unaccounted_semantics_field(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(semantics_identity, "WEAKER_MODEL_MANIFEST_COVERAGE", ())

    with pytest.raises(RuntimeError, match="explicitly account"):
        CanonicalBirthSemanticsEncoder.encode_weaker_model(weaker_model_specs()[0])


@pytest.mark.parametrize(
    "drifted",
    [
        residual_definition(output_schema="schema-B"),
        residual_definition(evaluator_id="eval-Y"),
        residual_definition(invariants=("I9",)),
        residual_definition(failure_semantics="different semantics"),
    ],
)
def test_same_residual_id_with_different_content_has_different_content_id(
    drifted: ResidualDefinitionSpec,
) -> None:
    baseline = CanonicalBirthSemanticsEncoder.encode_residual_definition(
        residual_definition()
    )
    changed = CanonicalBirthSemanticsEncoder.encode_residual_definition(drifted)

    assert drifted.residual_id == "residual"
    assert baseline.content_id.digest != changed.content_id.digest


def test_content_identity_cannot_be_hand_constructed() -> None:
    with pytest.raises(BirthSemanticsContentIdentityError, match="issued by"):
        BirthSemanticsContentIdentity(
            algorithm="sha256",
            canonicalization_version="birth-semantics-manifest-v1",
            digest="0" * 64,
        )


def test_frozen_content_scope_cannot_be_hand_constructed() -> None:
    with pytest.raises(BirthSemanticsContentIdentityError, match="registry-issued"):
        FrozenBirthSemanticsContentScope(
            domain="finite-domain",
            role=BirthEvaluatorRole.RESIDUAL_DEFINITION,
            target_id="residual",
            canonical_bytes=b"{}",
            content_id=CanonicalBirthSemanticsEncoder.encode_residual_definition(
                residual_definition()
            ).content_id,
        )


def test_registry_freezes_first_content_and_accepts_matching_rebinds() -> None:
    registry = BirthSemanticsContentRegistry()
    manifest = CanonicalBirthSemanticsEncoder.encode_residual_definition(
        residual_definition()
    )

    first = registry.freeze(
        domain="finite-domain",
        role=BirthEvaluatorRole.RESIDUAL_DEFINITION,
        target_id="residual",
        manifest=manifest,
    )
    second = registry.freeze(
        domain="finite-domain",
        role=BirthEvaluatorRole.RESIDUAL_DEFINITION,
        target_id="residual",
        manifest=manifest,
    )

    assert first.canonical_bytes == second.canonical_bytes == manifest.canonical_bytes


def test_registry_rejects_drifted_content_for_the_same_scope() -> None:
    registry = BirthSemanticsContentRegistry()
    registry.freeze(
        domain="finite-domain",
        role=BirthEvaluatorRole.RESIDUAL_DEFINITION,
        target_id="residual",
        manifest=CanonicalBirthSemanticsEncoder.encode_residual_definition(
            residual_definition()
        ),
    )

    with pytest.raises(
        BirthSemanticsContentIdentityError, match="SameId != SameSemantics"
    ):
        registry.freeze(
            domain="finite-domain",
            role=BirthEvaluatorRole.RESIDUAL_DEFINITION,
            target_id="residual",
            manifest=CanonicalBirthSemanticsEncoder.encode_residual_definition(
                residual_definition(evaluator_id="eval-Y")
            ),
        )


def test_content_binding_passes_when_runtime_content_matches_frozen_content() -> None:
    contract = assessment_semantics()
    sealed = sealed_registry_for(contract)

    binding = BirthAssessmentContentBinding(contract=contract, registry_snapshot=sealed)

    assert binding.residual_definition_content_id.digest
    assert binding.closure_criterion_content_id.digest
    assert len(binding.weaker_model_content_ids) == 3


def test_content_binding_rejects_residual_content_drift_under_the_same_id() -> None:
    contract = assessment_semantics()
    sealed = sealed_registry_for(contract)

    drifted_contract = assessment_semantics(
        residual=residual_definition(evaluator_id="eval-Y")
    )

    with pytest.raises(
        BirthSemanticsContentIdentityError, match="SameId != SameSemantics"
    ):
        BirthAssessmentContentBinding(
            contract=drifted_contract, registry_snapshot=sealed
        )


def test_content_binding_rejects_closure_content_drift_under_the_same_id() -> None:
    contract = assessment_semantics()
    sealed = sealed_registry_for(contract)

    drifted_contract = assessment_semantics(
        closure=closure_criterion(evaluator_id="different-closure-evaluator")
    )

    with pytest.raises(
        BirthSemanticsContentIdentityError, match="SameId != SameSemantics"
    ):
        BirthAssessmentContentBinding(
            contract=drifted_contract, registry_snapshot=sealed
        )


def test_content_binding_requires_every_scope_to_be_frozen_in_the_registry() -> None:
    contract = assessment_semantics()
    registry = BirthSemanticsContentRegistry()
    registry.freeze(
        domain="finite-domain",
        role=BirthEvaluatorRole.RESIDUAL_DEFINITION,
        target_id="residual",
        manifest=CanonicalBirthSemanticsEncoder.encode_residual_definition(
            contract.residual_definition
        ),
    )
    frozen_experiment = PreEvidenceSpecificationRegistry().freeze(
        CanonicalBirthExperimentSpecificationEncoder.encode(contract.specification)
    )
    sealed = registry.seal("partial-snapshot", frozen_experiment)

    with pytest.raises(BirthSemanticsContentIdentityError, match="no frozen content"):
        BirthAssessmentContentBinding(contract=contract, registry_snapshot=sealed)


def test_content_binding_requires_a_real_contract_and_sealed_registry() -> None:
    contract = assessment_semantics()
    sealed = sealed_registry_for(contract)

    with pytest.raises(BirthSemanticsContentIdentityError, match="semantics contract"):
        BirthAssessmentContentBinding(
            contract="not-a-contract",  # type: ignore[arg-type]
            registry_snapshot=sealed,
        )

    with pytest.raises(BirthSemanticsContentIdentityError, match="sealed content"):
        BirthAssessmentContentBinding(
            contract=contract,
            registry_snapshot="not-a-registry",  # type: ignore[arg-type]
        )


def test_content_binding_rejects_a_snapshot_bound_to_another_experiment() -> None:
    contract = assessment_semantics()
    registry = BirthSemanticsContentRegistry()
    domain = contract.specification.domain
    registry.freeze(
        domain=domain,
        role=BirthEvaluatorRole.RESIDUAL_DEFINITION,
        target_id="residual",
        manifest=CanonicalBirthSemanticsEncoder.encode_residual_definition(
            contract.residual_definition
        ),
    )
    registry.freeze(
        domain=domain,
        role=BirthEvaluatorRole.CLOSURE_CRITERION,
        target_id="closure",
        manifest=CanonicalBirthSemanticsEncoder.encode_closure_criterion(
            contract.closure_criterion
        ),
    )
    for model in contract.weaker_models:
        registry.freeze(
            domain=domain,
            role=BirthEvaluatorRole.WEAKER_MODEL,
            target_id=model.model_id,
            manifest=CanonicalBirthSemanticsEncoder.encode_weaker_model(model),
        )
    other_specification = BirthExperimentSpecification(
        experiment_id="other-experiment",
        revision_id="r1",
        revision_sequence=1,
        evidence_mode=EvidenceMode.FORMAL,
        domain=domain,
        projection_poset=contract.specification.projection_poset,
        birth_query=contract.specification.birth_query,
        residual_definition_id="residual",
        residual_definition="unexplained distinction",
        closure_criterion_id="closure",
        closure_criterion="all prerequisite models fail to close the residual",
        evidence_requirements="exhaustive proof over the finite domain",
    )
    frozen_experiment = PreEvidenceSpecificationRegistry().freeze(
        CanonicalBirthExperimentSpecificationEncoder.encode(other_specification)
    )

    with pytest.raises(BirthSemanticsContentIdentityError, match="authorized frozen"):
        BirthAssessmentContentBinding(
            contract=contract,
            registry_snapshot=registry.seal("wrong-experiment", frozen_experiment),
        )
