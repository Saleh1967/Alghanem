"""أوّلُ تشغيلٍ فراكتاليٍّ فعليٍّ في المشروع؛ تخليقيٌّ محايدٌ داخل النواة وحدَها.

    Seed
      → ExpansionSet(A, B, C)
      → PatternConformance
      → BranchAdjudication(A ADMITTED, B ADMITTED, C DEFERRED)
      → IdentityPreservingTransformation(A)
      → BranchBirth(B)
      → transition traces
      → MRK Closure
      → سجلُّ A و B و C محفوظٌ كاملًا
      → LiftGate → DEFERRED_NO_SCALE_NECESSITY_AUTHORITY

ولا يُستدعى هنا `kernel/` ولا سلطةُ ولادةٍ ولا تجربةٌ مُجمَّدة؛ التشغيلُ محلّيٌّ
داخل `fractal_generation/` بعينها.
"""

from __future__ import annotations

from dataclasses import dataclass

import pytest
from fractal_cases import (
    ALPHA_CLOSURE_CONTRACT,
    ALPHA_IDENTITY,
    ALPHA_REF,
    BETA_REF,
    BRANCH_IDENTITY,
    CANDIDATE_A,
    CANDIDATE_B,
    CANDIDATE_C,
    EXPANSION_SET,
    PRESERVED,
    SCALE_SPACE,
    SEED,
    SEED_NODE,
    TRANSFORM_PATTERN,
)

from alghanem.fractal_generation import (
    NO_SCALE_NECESSITY_AUTHORITY,
    BranchAdjudicationDecision,
    BranchAdjudicationGate,
    BranchAssessment,
    BranchBirthCandidate,
    BranchRelation,
    BranchStanding,
    ClosedFractalNode,
    ClosureCandidate,
    ClosureDecision,
    ClosureGate,
    ClosureRequirement,
    ClosureStatus,
    ExpansionCandidate,
    FractalMovementKind,
    FractalResidual,
    FractalResidualKind,
    FractalTrace,
    FractalTransitionDecision,
    FractalTransitionGate,
    IdentityPreservingTransformationCandidate,
    InvariantAudit,
    LiftCandidate,
    LiftDecision,
    LiftGate,
    LiftStatus,
    PatternConformanceGate,
    PatternConformanceStatus,
    PatternConformantDifference,
    ScaleExhaustionCandidate,
    ScaleTransitionRequirement,
)


@dataclass(frozen=True)
class SyntheticRun:
    """ناتجُ التشغيل التخليقيِّ كاملًا؛ يُقرأ في الاختبارات ولا يُعاد تشغيله."""

    adjudication: BranchAdjudicationDecision
    decision_a: FractalTransitionDecision
    decision_b: FractalTransitionDecision
    closure: ClosureDecision
    closed: ClosedFractalNode
    lift: LiftDecision


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


@pytest.fixture(scope="module")
def run() -> SyntheticRun:
    """المسارُ الفراكتاليُّ كاملًا، مُشغَّلًا مرّةً واحدةً ومقروءًا في الاختبارات."""

    movement_a = IdentityPreservingTransformationCandidate(
        conformant=_conformant(CANDIDATE_A),
        carrier_id="carrier.alpha",
        identity_before=ALPHA_IDENTITY,
        identity_after=ALPHA_IDENTITY,
        preserved_invariants=PRESERVED,
        output_content=(("mark", "m1"),),
    )
    movement_b = BranchBirthCandidate(
        conformant=_conformant(CANDIDATE_B),
        parent_ref=SEED_NODE.as_ref(),
        parent_identity=ALPHA_IDENTITY,
        child_identity=BRANCH_IDENTITY,
        branch_relation=BranchRelation.SIBLING_DIFFERENTIATION,
        shared_interface=PRESERVED,
        declared_difference=CANDIDATE_B.declared_difference,
        output_content=(("mark", "m0"), ("mark_split", "m0b")),
    )
    _conformant(CANDIDATE_C)

    adjudication = BranchAdjudicationGate.adjudicate(
        expansion_set=EXPANSION_SET,
        assessments=(
            BranchAssessment(
                candidate_id="branch.A",
                standing=BranchStanding.ADMITTED,
                reason="فرقٌ مُطابِقٌ في بُعدٍ غيرِ مانعٍ مع حفظ عين الهويّة",
                residuals=(),
                movement=movement_a,
            ),
            BranchAssessment(
                candidate_id="branch.B",
                standing=BranchStanding.ADMITTED,
                reason="فرقٌ مُطابِقٌ يقتضي هويّةً أخرى بواجهةٍ مشتركةٍ مُصرَّحة",
                residuals=(),
                movement=movement_b,
            ),
            BranchAssessment(
                candidate_id="branch.C",
                standing=BranchStanding.DEFERRED,
                reason="لا دليلَ على فرق الترتيب عند هذا المقياس",
                residuals=(
                    FractalResidual(
                        kind=FractalResidualKind.DEFERRED_BRANCH,
                        subject_id="branch.C",
                        reason="فرقُ الترتيب مؤجَّلٌ لغياب دليلٍ عند المقياس الجاري",
                    ),
                ),
            ),
        ),
        gate_id="gate.adjudication.alpha",
    )

    decision_a = FractalTransitionGate.open_transition(
        adjudication=adjudication,
        candidate_id="branch.A",
        source_node=SEED_NODE,
        transition_id="transition.A",
        gate_id="gate.transition.alpha",
        evidence_ref="evidence.synthetic.alpha",
        output_node_id="node.alpha.1",
    )
    decision_b = FractalTransitionGate.open_transition(
        adjudication=adjudication,
        candidate_id="branch.B",
        source_node=SEED_NODE,
        transition_id="transition.B",
        gate_id="gate.transition.alpha",
        evidence_ref="evidence.synthetic.alpha",
        output_node_id="node.alpha.1b",
    )

    trace = FractalTrace(steps=(decision_a.trace_step,))
    node = decision_a.output_node
    closure = ClosureGate.assess(
        candidate=ClosureCandidate(
            node=node,
            trace=trace,
            adjudication=adjudication,
            branch_transitions=(decision_a.trace_step, decision_b.trace_step),
            contract=ALPHA_CLOSURE_CONTRACT,
            coverage=(
                ClosureRequirement(
                    requirement_id="MRK.alpha.identity",
                    satisfied_by_content_id=node.identity.content_id,
                    reason="هويّةُ العقدة مُحَلّةٌ في فضاء المقاييس بعقدها",
                ),
                ClosureRequirement(
                    requirement_id="MRK.alpha.trace",
                    satisfied_by_content_id=trace.output_content_id,
                    reason="الأثرُ ينتهي إلى هذه العقدة ببصمتها",
                ),
                ClosureRequirement(
                    requirement_id="MRK.alpha.branches",
                    satisfied_by_content_id=SEED_NODE.content_id,
                    reason="سجلُّ الفروع الثلاثة تامٌّ بأحكامه وبقاياه",
                ),
            ),
            invariant_audit=InvariantAudit(
                audited_invariants=PRESERVED,
                passed=True,
                reason="ثوابتُ النمط مُدقَّقةٌ على مخرج الحركة",
            ),
            residuals=(),
        ),
        gate_id="gate.closure.alpha",
    )
    assert closure.closed is not None
    lift = LiftGate.assess(
        candidate=LiftCandidate(
            closed_node=closure.closed,
            exhaustion=ScaleExhaustionCandidate(
                closed_node=closure.closed,
                claim="يُدَّعى أنّ المقياسَ الأدنى استُنفِد وأنّ بنيةً أعلى لازمة",
                irreducible_residuals=(
                    FractalResidual(
                        kind=FractalResidualKind.IRREDUCIBLE_AT_CURRENT_SCALE,
                        subject_id="branch.C",
                        reason="فرقُ الترتيب لا يُردّ عند هذا المقياس",
                    ),
                ),
            ),
            requirement=ScaleTransitionRequirement(
                from_scale_ref=ALPHA_REF,
                to_scale_ref=BETA_REF,
                necessity_claim="التجميعُ عند `scale.beta` لازمٌ لردّ البقيّة",
            ),
        )
    )
    return SyntheticRun(
        adjudication=adjudication,
        decision_a=decision_a,
        decision_b=decision_b,
        closure=closure,
        closed=closure.closed,
        lift=lift,
    )


def test_the_seed_opens_three_proposals_and_none_of_them_is_a_movement() -> None:
    assert EXPANSION_SET.candidate_ids == {"branch.A", "branch.B", "branch.C"}
    for candidate in EXPANSION_SET.candidates:
        assert not hasattr(candidate, "trace")
        assert not hasattr(candidate, "movement_kind")
        assert not hasattr(candidate, "identity_after")
    assert SEED_NODE.origin_id == SEED.content_id


def test_all_three_proposals_conform_to_their_pattern() -> None:
    for candidate in (CANDIDATE_A, CANDIDATE_B, CANDIDATE_C):
        decision = PatternConformanceGate.assess(
            candidate=candidate,
            pattern=TRANSFORM_PATTERN,
            node=SEED_NODE,
            space=SCALE_SPACE,
        )
        assert decision.status is PatternConformanceStatus.CONFORMANT


def test_two_branches_are_admitted_and_one_is_deferred(run: SyntheticRun) -> None:
    assert run.adjudication.co_admissible_ids == {"branch.A", "branch.B"}
    assert tuple(
        assessment.candidate_id for assessment in run.adjudication.deferred
    ) == ("branch.C",)
    assert run.adjudication.blocked == ()


def test_no_winner_is_chosen_among_the_co_admissible(run: SyntheticRun) -> None:
    for name in ("winner", "priority", "score", "ranking", "best"):
        assert not hasattr(run.adjudication, name)
        assert not hasattr(EXPANSION_SET, name)
    assert isinstance(run.adjudication.co_admissible_ids, frozenset)
    assert len(run.adjudication.co_admissible_ids) == 2


def test_the_two_movements_are_of_the_two_named_kinds(run: SyntheticRun) -> None:
    transition_a = run.decision_a.transition
    transition_b = run.decision_b.transition
    assert (
        transition_a.movement_kind
        is FractalMovementKind.IDENTITY_PRESERVING_TRANSFORMATION
    )
    assert transition_b.movement_kind is FractalMovementKind.BRANCH_BIRTH
    assert transition_a.identity_before.is_same_instance_as(transition_a.identity_after)
    assert not transition_b.identity_before.is_same_instance_as(
        transition_b.identity_after
    )


def test_each_transition_carries_a_reconstructible_trace_step(
    run: SyntheticRun,
) -> None:
    for decision in (run.decision_a, run.decision_b):
        step = decision.trace_step
        assert step.carrier_id == "carrier.alpha"
        assert step.source_ref == SEED_NODE.as_ref()
        assert step.input_content_id == SEED_NODE.content_id
        assert step.output_content_id == decision.output_node.content_id
        assert step.gate_id == "gate.transition.alpha"
        assert step.evidence_ref == "evidence.synthetic.alpha"
        assert step.scale_before == ALPHA_REF
        assert step.scale_after == ALPHA_REF
        assert step.pattern_ref == TRANSFORM_PATTERN.as_ref()
        assert step.accepted_difference.dimension in ("mark_shape", "mark_split")


def test_one_node_closes_its_minimum_complete_requirement(run: SyntheticRun) -> None:
    assert run.closure.status is ClosureStatus.CLOSED
    assert run.closed.node.node_id == "node.alpha.1"
    assert run.closed.scale_ref == ALPHA_REF
    assert run.closed.trace.output_content_id == run.closed.node.content_id


def test_the_closed_node_keeps_the_record_of_all_three_branches(
    run: SyntheticRun,
) -> None:
    record = {
        assessment.candidate_id: assessment.standing
        for assessment in run.closed.branch_record
    }
    assert record == {
        "branch.A": BranchStanding.ADMITTED,
        "branch.B": BranchStanding.ADMITTED,
        "branch.C": BranchStanding.DEFERRED,
    }
    assert any(residual.subject_id == "branch.C" for residual in run.closed.residuals)


def test_the_lift_gate_defers_for_want_of_scale_necessity_authority(
    run: SyntheticRun,
) -> None:
    assert run.lift.status is LiftStatus.DEFERRED_NO_SCALE_NECESSITY_AUTHORITY
    assert run.lift.blocking_gap is NO_SCALE_NECESSITY_AUTHORITY


def test_no_next_scale_seed_is_produced_by_this_run(run: SyntheticRun) -> None:
    assert run.lift.next_scale_seed is None
