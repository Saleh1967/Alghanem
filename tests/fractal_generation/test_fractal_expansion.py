"""النمطُ والاقتراحُ والمطابقة: إعلانٌ لا برهان، واقتراحٌ لا حركة، ومطابقةٌ لا ترخيص.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

import pytest
from fractal_cases import (
    BETA_REF,
    CANDIDATE_A,
    EXPANSION_SET,
    PATTERN_REF,
    PROVENANCE,
    SCALE_SPACE,
    SEED_NODE,
    TRANSFORM_PATTERN,
)

from alghanem.fractal_generation import (
    DeclaredDifference,
    ExpansionCandidate,
    ExpansionError,
    ExpansionSet,
    PatternConformanceGate,
    PatternConformanceStatus,
    PatternConformantDifference,
    PatternContract,
    PatternContractError,
)


def _difference(*, dimension: str, preserved: tuple[str, ...]) -> DeclaredDifference:
    return DeclaredDifference(
        difference_id="difference.X",
        dimension=dimension,
        description="فرقٌ مُصرَّحٌ للقياس",
        preserved_invariants=preserved,
    )


def _candidate(difference: DeclaredDifference) -> ExpansionCandidate:
    return ExpansionCandidate(
        candidate_id="branch.X",
        source=SEED_NODE.as_ref(),
        pattern_ref=PATTERN_REF,
        declared_difference=difference,
        proposal_provenance=PROVENANCE,
    )


def test_a_pattern_contract_names_no_licensed_variation_class() -> None:
    assert not hasattr(TRANSFORM_PATTERN, "licensed_variation_class")
    assert "licensed" not in " ".join(TRANSFORM_PATTERN.__slots__).lower()
    assert "proven" not in " ".join(TRANSFORM_PATTERN.__slots__).lower()


def test_a_pattern_contract_carries_all_its_declared_clauses() -> None:
    for field in (
        "admissible_seed_contract",
        "operation_contract",
        "declared_variation_contract",
        "reapplication_condition",
        "residual_policy",
        "authority_scope",
    ):
        assert getattr(TRANSFORM_PATTERN, field).strip()
    assert TRANSFORM_PATTERN.blockers == ("semantic_role",)
    assert TRANSFORM_PATTERN.scales_resolved_in(SCALE_SPACE)


def test_a_pattern_refuses_an_empty_scale_range() -> None:
    with pytest.raises(PatternContractError):
        PatternContract(
            pattern_id="pattern.void",
            domain_id="domain.synthetic",
            applicable_scales=(),
            admissible_seed_contract="عقد",
            operation_contract="عقد",
            preserved_invariants=("a",),
            declared_variation_contract="عقد",
            reapplication_condition="شرط",
            closure_requirements=(),
            branch_conditions=(),
            blockers=(),
            residual_policy="سياسة",
            authority_scope="مدى",
        )


def test_a_proposal_carries_no_movement_of_any_kind() -> None:
    for name in (
        "movement_kind",
        "identity_after",
        "trace",
        "trace_step",
        "transition",
        "output_content",
    ):
        assert not hasattr(CANDIDATE_A, name)
    assert CANDIDATE_A.proposal_provenance is PROVENANCE


def test_an_expansion_set_refuses_a_proposal_of_another_node() -> None:
    stranger = ExpansionCandidate(
        candidate_id="branch.Z",
        source=SEED_NODE.as_ref(),
        pattern_ref=PATTERN_REF,
        declared_difference=_difference(dimension="mark_shape", preserved=()),
        proposal_provenance=PROVENANCE,
    )
    with pytest.raises(ExpansionError):
        ExpansionSet(source=CANDIDATE_A.source, candidates=(stranger, stranger))


def test_an_expansion_set_ranks_nothing() -> None:
    for name in ("winner", "priority", "score", "ranking", "best", "ordered"):
        assert not hasattr(EXPANSION_SET, name)
    assert EXPANSION_SET.candidate_for("branch.A") is CANDIDATE_A
    with pytest.raises(ExpansionError):
        EXPANSION_SET.candidate_for("branch.Z")


def test_a_conformant_difference_is_issued_by_the_gate_alone() -> None:
    with pytest.raises(ExpansionError):
        PatternConformantDifference(
            candidate=CANDIDATE_A,
            pattern_ref=PATTERN_REF,
            checked_invariants=TRANSFORM_PATTERN.preserved_invariants,
            issuance=object(),  # type: ignore[arg-type]
        )


def test_the_gate_refuses_a_difference_in_a_blocked_dimension() -> None:
    decision = PatternConformanceGate.assess(
        candidate=_candidate(
            _difference(
                dimension="semantic_role",
                preserved=TRANSFORM_PATTERN.preserved_invariants,
            )
        ),
        pattern=TRANSFORM_PATTERN,
        node=SEED_NODE,
        space=SCALE_SPACE,
    )
    assert decision.status is PatternConformanceStatus.NONCONFORMANT
    assert decision.conformant is None


def test_the_gate_refuses_a_difference_that_drops_a_pattern_invariant() -> None:
    decision = PatternConformanceGate.assess(
        candidate=_candidate(
            _difference(dimension="mark_shape", preserved=("carrier_continuity",))
        ),
        pattern=TRANSFORM_PATTERN,
        node=SEED_NODE,
        space=SCALE_SPACE,
    )
    assert decision.status is PatternConformanceStatus.NONCONFORMANT


def test_the_gate_refuses_a_pattern_outside_the_scale_of_the_node() -> None:
    elsewhere = PatternContract(
        pattern_id="pattern.transform",
        domain_id="domain.synthetic",
        applicable_scales=(BETA_REF,),
        admissible_seed_contract="عقد",
        operation_contract="عقد",
        preserved_invariants=TRANSFORM_PATTERN.preserved_invariants,
        declared_variation_contract="عقد",
        reapplication_condition="شرط",
        closure_requirements=(),
        branch_conditions=(),
        blockers=(),
        residual_policy="سياسة",
        authority_scope="مدى",
    )
    candidate = ExpansionCandidate(
        candidate_id="branch.Y",
        source=SEED_NODE.as_ref(),
        pattern_ref=elsewhere.as_ref(),
        declared_difference=_difference(
            dimension="mark_shape",
            preserved=TRANSFORM_PATTERN.preserved_invariants,
        ),
        proposal_provenance=PROVENANCE,
    )
    decision = PatternConformanceGate.assess(
        candidate=candidate,
        pattern=elsewhere,
        node=SEED_NODE,
        space=SCALE_SPACE,
    )
    assert decision.status is PatternConformanceStatus.NONCONFORMANT


def test_conformance_declares_no_licence_and_no_proof() -> None:
    decision = PatternConformanceGate.assess(
        candidate=CANDIDATE_A,
        pattern=TRANSFORM_PATTERN,
        node=SEED_NODE,
        space=SCALE_SPACE,
    )
    assert decision.status is PatternConformanceStatus.CONFORMANT
    conformant = decision.conformant
    assert conformant is not None
    for name in ("licensed", "proof", "proven", "authorized"):
        assert not hasattr(conformant, name)
    assert "ليست ترخيصًا" in decision.reason or "برهان" in decision.reason
