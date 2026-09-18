"""الفصلُ الأفقيُّ بين الفروع: سجلٌّ تامٌّ، وبقايا غيرُ ممحوّة، ولا اختيارَ بين مقبولَين.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

import pytest
from fractal_cases import (
    ALPHA_IDENTITY,
    BRANCH_IDENTITY,
    CANDIDATE_A,
    CANDIDATE_B,
    EXPANSION_SET,
    PRESERVED,
    SCALE_SPACE,
    SEED_NODE,
    TRANSFORM_PATTERN,
)

from alghanem.fractal_generation import (
    BranchAdjudicationDecision,
    BranchAdjudicationGate,
    BranchAssessment,
    BranchBirthCandidate,
    BranchError,
    BranchRelation,
    BranchStanding,
    ExpansionCandidate,
    FractalResidual,
    FractalResidualKind,
    IdentityPreservingTransformationCandidate,
    PatternConformanceGate,
    PatternConformanceStatus,
    PatternConformantDifference,
)


def _conformant(candidate: ExpansionCandidate) -> PatternConformantDifference:
    decision = PatternConformanceGate.assess(
        candidate=candidate,
        pattern=TRANSFORM_PATTERN,
        node=SEED_NODE,
        space=SCALE_SPACE,
    )
    assert decision.status is PatternConformanceStatus.CONFORMANT
    assert decision.conformant is not None
    return decision.conformant


def _transformation() -> IdentityPreservingTransformationCandidate:
    return IdentityPreservingTransformationCandidate(
        conformant=_conformant(CANDIDATE_A),
        carrier_id="carrier.alpha",
        identity_before=ALPHA_IDENTITY,
        identity_after=ALPHA_IDENTITY,
        preserved_invariants=PRESERVED,
        output_content=(("mark", "m1"),),
    )


def _birth() -> BranchBirthCandidate:
    return BranchBirthCandidate(
        conformant=_conformant(CANDIDATE_B),
        parent_ref=SEED_NODE.as_ref(),
        parent_identity=ALPHA_IDENTITY,
        child_identity=BRANCH_IDENTITY,
        branch_relation=BranchRelation.SIBLING_DIFFERENTIATION,
        shared_interface=PRESERVED,
        declared_difference=CANDIDATE_B.declared_difference,
        output_content=(("mark", "m0"), ("mark_split", "m0b")),
    )


def _deferral(candidate_id: str) -> BranchAssessment:
    return BranchAssessment(
        candidate_id=candidate_id,
        standing=BranchStanding.DEFERRED,
        reason="لا دليلَ عند المقياس الجاري",
        residuals=(
            FractalResidual(
                kind=FractalResidualKind.DEFERRED_BRANCH,
                subject_id=candidate_id,
                reason="فرقٌ مؤجَّلٌ لغياب دليل",
            ),
        ),
    )


def test_the_standings_are_three_and_residual_is_not_one_of_them() -> None:
    assert [member.name for member in BranchStanding] == [
        "ADMITTED",
        "BLOCKED",
        "DEFERRED",
    ]
    assert "RESIDUAL" not in {member.name for member in BranchStanding}


def test_an_identity_preserving_candidate_refuses_another_instance() -> None:
    with pytest.raises(BranchError):
        IdentityPreservingTransformationCandidate(
            conformant=_conformant(CANDIDATE_A),
            carrier_id="carrier.alpha",
            identity_before=ALPHA_IDENTITY,
            identity_after=BRANCH_IDENTITY,
            preserved_invariants=PRESERVED,
            output_content=(("mark", "m1"),),
        )


def test_a_branch_birth_refuses_the_identity_of_its_parent() -> None:
    with pytest.raises(BranchError):
        BranchBirthCandidate(
            conformant=_conformant(CANDIDATE_B),
            parent_ref=SEED_NODE.as_ref(),
            parent_identity=ALPHA_IDENTITY,
            child_identity=ALPHA_IDENTITY,
            branch_relation=BranchRelation.SIBLING_DIFFERENTIATION,
            shared_interface=PRESERVED,
            declared_difference=CANDIDATE_B.declared_difference,
            output_content=(("mark", "m0b"),),
        )


def test_a_branch_birth_refuses_an_unnamed_shared_interface() -> None:
    with pytest.raises(BranchError):
        BranchBirthCandidate(
            conformant=_conformant(CANDIDATE_B),
            parent_ref=SEED_NODE.as_ref(),
            parent_identity=ALPHA_IDENTITY,
            child_identity=BRANCH_IDENTITY,
            branch_relation=BranchRelation.SIBLING_DIFFERENTIATION,
            shared_interface=(),
            declared_difference=CANDIDATE_B.declared_difference,
            output_content=(("mark", "m0b"),),
        )


def test_an_admitted_branch_carries_its_own_movement() -> None:
    with pytest.raises(BranchError):
        BranchAssessment(
            candidate_id="branch.B",
            standing=BranchStanding.ADMITTED,
            reason="قبولٌ بحركةِ فرعٍ آخر",
            residuals=(),
            movement=_transformation(),
        )


def test_a_non_admitted_branch_carries_no_movement_and_names_its_residual() -> None:
    with pytest.raises(BranchError):
        BranchAssessment(
            candidate_id="branch.A",
            standing=BranchStanding.DEFERRED,
            reason="تأجيلٌ بحركة",
            residuals=(),
            movement=_transformation(),
        )
    with pytest.raises(BranchError):
        BranchAssessment(
            candidate_id="branch.C",
            standing=BranchStanding.BLOCKED,
            reason="منعٌ بلا بقيّةٍ مُسمّاة",
            residuals=(),
        )


def test_an_adjudication_decision_is_issued_by_its_gate_alone() -> None:
    with pytest.raises(BranchError):
        BranchAdjudicationDecision(
            source=SEED_NODE.as_ref(),
            gate_id="gate.forged",
            assessments=(),
            issuance=object(),  # type: ignore[arg-type]
        )


def test_the_gate_refuses_an_incomplete_record_of_the_expansion_set() -> None:
    with pytest.raises(BranchError):
        BranchAdjudicationGate.adjudicate(
            expansion_set=EXPANSION_SET,
            assessments=(
                BranchAssessment(
                    candidate_id="branch.A",
                    standing=BranchStanding.ADMITTED,
                    reason="قبول",
                    residuals=(),
                    movement=_transformation(),
                ),
            ),
            gate_id="gate.partial",
        )


def test_the_gate_refuses_a_branch_outside_the_expansion_set() -> None:
    with pytest.raises(BranchError):
        BranchAdjudicationGate.adjudicate(
            expansion_set=EXPANSION_SET,
            assessments=(
                BranchAssessment(
                    candidate_id="branch.A",
                    standing=BranchStanding.ADMITTED,
                    reason="قبول",
                    residuals=(),
                    movement=_transformation(),
                ),
                _deferral("branch.B"),
                _deferral("branch.C"),
                _deferral("branch.Z"),
            ),
            gate_id="gate.stranger",
        )


def test_two_co_admissible_branches_are_neither_ranked_nor_chosen() -> None:
    decision = BranchAdjudicationGate.adjudicate(
        expansion_set=EXPANSION_SET,
        assessments=(
            BranchAssessment(
                candidate_id="branch.A",
                standing=BranchStanding.ADMITTED,
                reason="قبولٌ بحفظ عين الهويّة",
                residuals=(),
                movement=_transformation(),
            ),
            BranchAssessment(
                candidate_id="branch.B",
                standing=BranchStanding.ADMITTED,
                reason="قبولٌ بولادةِ فرعٍ أخ",
                residuals=(),
                movement=_birth(),
            ),
            _deferral("branch.C"),
        ),
        gate_id="gate.adjudication.pair",
    )
    assert decision.co_admissible_ids == {"branch.A", "branch.B"}
    for name in ("winner", "priority", "score", "ranking", "best"):
        assert not hasattr(decision, name)
    assert len(decision.assessments) == 3
    assert decision.residuals and decision.residuals[0].subject_id == "branch.C"
    assert decision.assessment_for("branch.C").standing is BranchStanding.DEFERRED
    with pytest.raises(BranchError):
        decision.assessment_for("branch.Z")
