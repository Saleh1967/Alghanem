"""الحركةُ الفعليّةُ وأثرُها: لا انتقالَ قبل فصلٍ تامّ، ولا أثرَ قبل انتقال.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

import pytest
from fractal_cases import (
    ALPHA_IDENTITY,
    ALPHA_REF,
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
    BranchRelation,
    BranchStanding,
    ExpansionCandidate,
    FractalMovementKind,
    FractalNode,
    FractalResidual,
    FractalResidualKind,
    FractalTrace,
    FractalTraceError,
    FractalTransition,
    FractalTransitionGate,
    FractalTransitionTraceStep,
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
    assert decision.conformant is not None
    assert decision.status is PatternConformanceStatus.CONFORMANT
    return decision.conformant


def _adjudication() -> BranchAdjudicationDecision:
    return BranchAdjudicationGate.adjudicate(
        expansion_set=EXPANSION_SET,
        assessments=(
            BranchAssessment(
                candidate_id="branch.A",
                standing=BranchStanding.ADMITTED,
                reason="قبولٌ بحفظ عين الهويّة",
                residuals=(),
                movement=IdentityPreservingTransformationCandidate(
                    conformant=_conformant(CANDIDATE_A),
                    carrier_id="carrier.alpha",
                    identity_before=ALPHA_IDENTITY,
                    identity_after=ALPHA_IDENTITY,
                    preserved_invariants=PRESERVED,
                    output_content=(("mark", "m1"),),
                ),
            ),
            BranchAssessment(
                candidate_id="branch.B",
                standing=BranchStanding.ADMITTED,
                reason="قبولٌ بولادةِ فرعٍ أخ",
                residuals=(),
                movement=BranchBirthCandidate(
                    conformant=_conformant(CANDIDATE_B),
                    parent_ref=SEED_NODE.as_ref(),
                    parent_identity=ALPHA_IDENTITY,
                    child_identity=BRANCH_IDENTITY,
                    branch_relation=BranchRelation.SIBLING_DIFFERENTIATION,
                    shared_interface=PRESERVED,
                    declared_difference=CANDIDATE_B.declared_difference,
                    output_content=(("mark", "m0"), ("mark_split", "m0b")),
                ),
            ),
            BranchAssessment(
                candidate_id="branch.C",
                standing=BranchStanding.DEFERRED,
                reason="لا دليلَ عند المقياس الجاري",
                residuals=(
                    FractalResidual(
                        kind=FractalResidualKind.DEFERRED_BRANCH,
                        subject_id="branch.C",
                        reason="فرقٌ مؤجَّل",
                    ),
                ),
            ),
        ),
        gate_id="gate.adjudication.trace",
    )


def _open(candidate_id: str, node_id: str) -> FractalTransitionTraceStep:
    return FractalTransitionGate.open_transition(
        adjudication=_adjudication(),
        candidate_id=candidate_id,
        source_node=SEED_NODE,
        transition_id=f"transition.{candidate_id}",
        gate_id="gate.transition.trace",
        evidence_ref="evidence.trace",
        output_node_id=node_id,
    ).trace_step


def test_the_movement_kinds_are_two_and_no_more() -> None:
    assert [member.name for member in FractalMovementKind] == [
        "IDENTITY_PRESERVING_TRANSFORMATION",
        "BRANCH_BIRTH",
    ]


def test_a_transition_is_issued_by_its_gate_alone() -> None:
    step = _open("branch.A", "node.alpha.1")
    with pytest.raises(FractalTraceError):
        FractalTransition(
            transition_id="transition.forged",
            movement_kind=FractalMovementKind.BRANCH_BIRTH,
            movement=step.transition.movement,
            source_ref=SEED_NODE.as_ref(),
            output_node=step.transition.output_node,
            gate_id="gate.forged",
            adjudication_gate_id="gate.forged",
            evidence_ref="evidence.forged",
            residuals=(),
            open_authority_gaps=(),
            issuance=object(),  # type: ignore[arg-type]
        )


def test_a_trace_step_is_issued_by_the_transition_gate_alone() -> None:
    step = _open("branch.A", "node.alpha.1")
    with pytest.raises(FractalTraceError):
        FractalTransitionTraceStep(
            transition=step.transition,
            issuance=object(),  # type: ignore[arg-type]
        )


def test_no_movement_is_opened_on_a_branch_that_was_not_admitted() -> None:
    with pytest.raises(FractalTraceError):
        FractalTransitionGate.open_transition(
            adjudication=_adjudication(),
            candidate_id="branch.C",
            source_node=SEED_NODE,
            transition_id="transition.C",
            gate_id="gate.transition.trace",
            evidence_ref="evidence.trace",
            output_node_id="node.alpha.1c",
        )


def test_no_movement_is_opened_over_a_node_that_was_not_adjudicated() -> None:
    other_node = FractalNode(
        node_id="node.other",
        identity=ALPHA_IDENTITY,
        carrier_id="carrier.alpha",
        content=(("mark", "m7"),),
        origin_id=SEED_NODE.content_id,
    )
    with pytest.raises(FractalTraceError):
        FractalTransitionGate.open_transition(
            adjudication=_adjudication(),
            candidate_id="branch.A",
            source_node=other_node,
            transition_id="transition.A",
            gate_id="gate.transition.trace",
            evidence_ref="evidence.trace",
            output_node_id="node.other.1",
        )


def test_a_trace_step_names_everything_needed_to_rebuild_it() -> None:
    step = _open("branch.B", "node.alpha.1b")
    assert step.carrier_id == "carrier.alpha"
    assert step.source_ref == SEED_NODE.as_ref()
    assert step.identity_before == ALPHA_IDENTITY
    assert step.identity_after == BRANCH_IDENTITY
    assert step.preserved_invariants == PRESERVED
    assert step.movement_kind is FractalMovementKind.BRANCH_BIRTH
    assert step.pattern_ref == TRANSFORM_PATTERN.as_ref()
    assert step.gate_id == "gate.transition.trace"
    assert step.evidence_ref == "evidence.trace"
    assert step.scale_before == ALPHA_REF
    assert step.scale_after == ALPHA_REF
    assert step.residuals == ()
    assert step.open_authority_gaps == ()
    assert step.output_content_id == step.transition.output_node.content_id


def test_a_trace_refuses_a_break_in_its_digest_chain() -> None:
    first = _open("branch.A", "node.alpha.1")
    second = _open("branch.B", "node.alpha.1b")
    with pytest.raises(FractalTraceError):
        FractalTrace(steps=(first, second))


def test_a_trace_of_one_step_reads_its_two_ends() -> None:
    step = _open("branch.A", "node.alpha.1")
    trace = FractalTrace(steps=(step,))
    assert trace.input_content_id == SEED_NODE.content_id
    assert trace.output_content_id == step.transition.output_node.content_id
    assert trace.steps == (step,)


def test_a_trace_refuses_to_be_empty() -> None:
    with pytest.raises(FractalTraceError):
        FractalTrace(steps=())
