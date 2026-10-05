"""إغلاقُ أقلِّ التمام: إغلاقٌ عند المقياس الجاري لا استنفادٌ ولا ضرورةُ رفع.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import replace

import pytest
from fractal_cases import (
    ALPHA_CLOSURE_CONTRACT,
    ALPHA_IDENTITY,
    ALPHA_REF,
    BETA_REF,
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
    ClosedFractalNode,
    ClosureCandidate,
    ClosureError,
    ClosureGate,
    ClosureRequirement,
    ClosureStatus,
    FractalResidual,
    FractalResidualKind,
    FractalTrace,
    FractalTransitionGate,
    FractalTransitionTraceStep,
    IdentityPreservingTransformationCandidate,
    InvariantAudit,
    MinimumCompleteRequirement,
    PatternConformanceGate,
    ScaleClosureContract,
)


def _admission_of_a() -> BranchAssessment:
    conformance = PatternConformanceGate.assess(
        candidate=CANDIDATE_A,
        pattern=TRANSFORM_PATTERN,
        node=SEED_NODE,
        space=SCALE_SPACE,
    )
    assert conformance.conformant is not None
    return BranchAssessment(
        candidate_id="branch.A",
        standing=BranchStanding.ADMITTED,
        reason="قبولٌ بحفظ عين الهويّة",
        residuals=(),
        movement=IdentityPreservingTransformationCandidate(
            conformant=conformance.conformant,
            carrier_id="carrier.alpha",
            identity_before=ALPHA_IDENTITY,
            identity_after=ALPHA_IDENTITY,
            preserved_invariants=PRESERVED,
            output_content=(("mark", "m1"),),
        ),
    )


def _adjudication() -> BranchAdjudicationDecision:
    deferrals = tuple(
        BranchAssessment(
            candidate_id=candidate_id,
            standing=BranchStanding.DEFERRED,
            reason="لا دليلَ عند المقياس الجاري",
            residuals=(
                FractalResidual(
                    kind=FractalResidualKind.DEFERRED_BRANCH,
                    subject_id=candidate_id,
                    reason="فرقٌ مؤجَّل",
                ),
            ),
        )
        for candidate_id in ("branch.B", "branch.C")
    )
    return BranchAdjudicationGate.adjudicate(
        expansion_set=EXPANSION_SET,
        assessments=(
            _admission_of_a(),
            *deferrals,
        ),
        gate_id="gate.adjudication.closure",
    )


def _coverage(
    *, node_content_id: str, trace_content_id: str
) -> tuple[ClosureRequirement, ...]:
    return (
        ClosureRequirement(
            requirement_id="MRK.alpha.identity",
            satisfied_by_content_id=node_content_id,
            reason="هويّةُ العقدة مُحَلّةٌ بعقد مقياسها",
        ),
        ClosureRequirement(
            requirement_id="MRK.alpha.trace",
            satisfied_by_content_id=trace_content_id,
            reason="الأثرُ ينتهي إلى هذه العقدة",
        ),
        ClosureRequirement(
            requirement_id="MRK.alpha.branches",
            satisfied_by_content_id=SEED_NODE.content_id,
            reason="سجلُّ الفروع تامٌّ بأحكامه وبقاياه",
        ),
    )


def _candidate(**overrides: object) -> ClosureCandidate:
    adjudication = _adjudication()
    step: FractalTransitionTraceStep = FractalTransitionGate.open_transition(
        adjudication=adjudication,
        candidate_id="branch.A",
        source_node=SEED_NODE,
        transition_id="transition.A",
        gate_id="gate.transition.closure",
        evidence_ref="evidence.closure",
        output_node_id="node.alpha.1",
    ).trace_step
    trace = FractalTrace(steps=(step,))
    base = ClosureCandidate(
        node=step.transition.output_node,
        trace=trace,
        adjudication=adjudication,
        branch_transitions=(step,),
        contract=ALPHA_CLOSURE_CONTRACT,
        coverage=_coverage(
            node_content_id=step.transition.output_node.identity.content_id,
            trace_content_id=trace.output_content_id,
        ),
        invariant_audit=InvariantAudit(
            audited_invariants=PRESERVED,
            passed=True,
            reason="ثوابتُ النمط مُدقَّقة",
        ),
        residuals=(),
    )
    return replace(base, **overrides) if overrides else base


def test_a_closed_node_cannot_be_built_by_a_caller() -> None:
    candidate = _candidate()
    with pytest.raises(ClosureError):
        ClosedFractalNode(
            candidate=candidate,
            gate_id="gate.forged",
            issuance=object(),  # type: ignore[arg-type]
        )


def test_closure_is_the_minimum_complete_at_the_current_scale() -> None:
    decision = ClosureGate.assess(candidate=_candidate(), gate_id="gate.closure")
    assert decision.status is ClosureStatus.CLOSED
    assert decision.closed is not None
    assert decision.closed.scale_ref == ALPHA_REF
    assert "استنفاد" in decision.reason or "الاستنفاد" in decision.reason


def test_an_uncovered_requirement_defers_the_closure() -> None:
    candidate = _candidate()
    decision = ClosureGate.assess(
        candidate=replace(candidate, coverage=candidate.coverage[:2]),
        gate_id="gate.closure",
    )
    assert decision.status is ClosureStatus.DEFERRED
    assert decision.closed is None


def test_a_coverage_outside_the_contract_blocks_the_closure() -> None:
    candidate = _candidate()
    decision = ClosureGate.assess(
        candidate=replace(
            candidate,
            coverage=(
                *candidate.coverage,
                ClosureRequirement(
                    requirement_id="MRK.alpha.stranger",
                    satisfied_by_content_id=SEED_NODE.content_id,
                    reason="متطلَّبٌ خارج العقد",
                ),
            ),
        ),
        gate_id="gate.closure",
    )
    assert decision.status is ClosureStatus.BLOCKED


def test_a_failed_invariant_audit_blocks_the_closure() -> None:
    decision = ClosureGate.assess(
        candidate=_candidate(
            invariant_audit=InvariantAudit(
                audited_invariants=PRESERVED,
                passed=False,
                reason="ثابتٌ لم يُحفَظ في مخرج الحركة",
            )
        ),
        gate_id="gate.closure",
    )
    assert decision.status is ClosureStatus.BLOCKED
    assert decision.closed is None


def test_a_blocking_residual_blocks_the_closure() -> None:
    decision = ClosureGate.assess(
        candidate=_candidate(
            residuals=(
                FractalResidual(
                    kind=FractalResidualKind.UNRESOLVED_DIFFERENCE,
                    subject_id="node.alpha.1",
                    reason="فرقٌ مانعٌ لم يُحسَم",
                    blocking=True,
                ),
            )
        ),
        gate_id="gate.closure",
    )
    assert decision.status is ClosureStatus.BLOCKED


def test_an_admitted_branch_that_has_not_moved_defers_the_closure() -> None:
    conformance_b = PatternConformanceGate.assess(
        candidate=CANDIDATE_B,
        pattern=TRANSFORM_PATTERN,
        node=SEED_NODE,
        space=SCALE_SPACE,
    )
    assert conformance_b.conformant is not None
    adjudication = BranchAdjudicationGate.adjudicate(
        expansion_set=EXPANSION_SET,
        assessments=(
            _admission_of_a(),
            BranchAssessment(
                candidate_id="branch.B",
                standing=BranchStanding.ADMITTED,
                reason="قبولٌ بولادةِ فرعٍ أخ",
                residuals=(),
                movement=BranchBirthCandidate(
                    conformant=conformance_b.conformant,
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
        gate_id="gate.adjudication.pair",
    )
    step = FractalTransitionGate.open_transition(
        adjudication=adjudication,
        candidate_id="branch.A",
        source_node=SEED_NODE,
        transition_id="transition.A",
        gate_id="gate.transition.closure",
        evidence_ref="evidence.closure",
        output_node_id="node.alpha.1",
    ).trace_step
    trace = FractalTrace(steps=(step,))
    decision = ClosureGate.assess(
        candidate=ClosureCandidate(
            node=step.transition.output_node,
            trace=trace,
            adjudication=adjudication,
            branch_transitions=(step,),
            contract=ALPHA_CLOSURE_CONTRACT,
            coverage=_coverage(
                node_content_id=step.transition.output_node.identity.content_id,
                trace_content_id=trace.output_content_id,
            ),
            invariant_audit=InvariantAudit(
                audited_invariants=PRESERVED,
                passed=True,
                reason="ثوابتُ النمط مُدقَّقة",
            ),
            residuals=(),
        ),
        gate_id="gate.closure",
    )
    assert decision.status is ClosureStatus.DEFERRED
    assert decision.closed is None


def test_a_contract_of_another_scale_blocks_the_closure() -> None:
    decision = ClosureGate.assess(
        candidate=_candidate(
            contract=ScaleClosureContract(
                scale_ref=BETA_REF,
                requirements=(
                    MinimumCompleteRequirement(
                        requirement_id="MRK.alpha.identity",
                        statement="بيان",
                        evidence_kind="resolved_scale_ref",
                    ),
                ),
            )
        ),
        gate_id="gate.closure",
    )
    assert decision.status is ClosureStatus.BLOCKED


def test_the_closed_node_keeps_every_branch_including_the_deferred() -> None:
    decision = ClosureGate.assess(candidate=_candidate(), gate_id="gate.closure")
    assert decision.closed is not None
    record = {
        assessment.candidate_id: assessment.standing
        for assessment in decision.closed.branch_record
    }
    assert record == {
        "branch.A": BranchStanding.ADMITTED,
        "branch.B": BranchStanding.DEFERRED,
        "branch.C": BranchStanding.DEFERRED,
    }
    assert {residual.subject_id for residual in decision.closed.residuals} == {
        "branch.B",
        "branch.C",
    }


def test_a_closed_node_claims_no_exhaustion_and_no_lift() -> None:
    decision = ClosureGate.assess(candidate=_candidate(), gate_id="gate.closure")
    assert decision.closed is not None
    for name in ("exhausted", "lift", "next_scale_seed", "necessity", "meaning"):
        assert not hasattr(decision.closed, name)
