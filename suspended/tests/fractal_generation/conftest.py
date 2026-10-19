"""عُدَّةُ شواهدِ الطبقة الفراكتاليّة: عقدةٌ مغلقةٌ صغرى تُبنى بالبوّابات وحدَها.

ولا يُبنى هنا التشغيلُ الفراكتاليُّ الكامل؛ ذاك موضعُه
`test_fractal_smoke_run.py` وحدَه.
"""

from __future__ import annotations

import pytest
from fractal_cases import (
    ALPHA_CLOSURE_CONTRACT,
    ALPHA_IDENTITY,
    CANDIDATE_A,
    EXPANSION_SET,
    PRESERVED,
    SCALE_SPACE,
    SEED_NODE,
    TRANSFORM_PATTERN,
)

from alghanem.fractal_generation import (
    BranchAdjudicationGate,
    BranchAssessment,
    BranchStanding,
    ClosedFractalNode,
    ClosureCandidate,
    ClosureGate,
    ClosureRequirement,
    FractalResidual,
    FractalResidualKind,
    FractalTrace,
    FractalTransitionGate,
    IdentityPreservingTransformationCandidate,
    InvariantAudit,
    PatternConformanceGate,
    PatternConformanceStatus,
)


@pytest.fixture(scope="session")
def closed_node() -> ClosedFractalNode:
    """عقدةٌ مغلقةٌ صغرى: فرعٌ واحدٌ مقبولٌ وفرعان مؤجَّلان بسجلٍّ محفوظ."""

    conformance = PatternConformanceGate.assess(
        candidate=CANDIDATE_A,
        pattern=TRANSFORM_PATTERN,
        node=SEED_NODE,
        space=SCALE_SPACE,
    )
    assert conformance.status is PatternConformanceStatus.CONFORMANT
    assert conformance.conformant is not None
    movement = IdentityPreservingTransformationCandidate(
        conformant=conformance.conformant,
        carrier_id="carrier.alpha",
        identity_before=ALPHA_IDENTITY,
        identity_after=ALPHA_IDENTITY,
        preserved_invariants=PRESERVED,
        output_content=(("mark", "m1"),),
    )
    deferrals = tuple(
        BranchAssessment(
            candidate_id=candidate_id,
            standing=BranchStanding.DEFERRED,
            reason="لا دليلَ عند المقياس الجاري",
            residuals=(
                FractalResidual(
                    kind=FractalResidualKind.DEFERRED_BRANCH,
                    subject_id=candidate_id,
                    reason="فرقٌ مؤجَّلٌ لغياب دليلٍ عند المقياس الجاري",
                ),
            ),
        )
        for candidate_id in ("branch.B", "branch.C")
    )
    adjudication = BranchAdjudicationGate.adjudicate(
        expansion_set=EXPANSION_SET,
        assessments=(
            BranchAssessment(
                candidate_id="branch.A",
                standing=BranchStanding.ADMITTED,
                reason="فرقٌ مُطابِقٌ مع حفظ عين الهويّة",
                residuals=(),
                movement=movement,
            ),
            *deferrals,
        ),
        gate_id="gate.adjudication.minimal",
    )
    decision = FractalTransitionGate.open_transition(
        adjudication=adjudication,
        candidate_id="branch.A",
        source_node=SEED_NODE,
        transition_id="transition.minimal",
        gate_id="gate.transition.minimal",
        evidence_ref="evidence.minimal",
        output_node_id="node.alpha.minimal",
    )
    trace = FractalTrace(steps=(decision.trace_step,))
    node = decision.output_node
    closure = ClosureGate.assess(
        candidate=ClosureCandidate(
            node=node,
            trace=trace,
            adjudication=adjudication,
            branch_transitions=(decision.trace_step,),
            contract=ALPHA_CLOSURE_CONTRACT,
            coverage=(
                ClosureRequirement(
                    requirement_id="MRK.alpha.identity",
                    satisfied_by_content_id=node.identity.content_id,
                    reason="هويّةُ العقدة مُحَلّةٌ بعقد مقياسها",
                ),
                ClosureRequirement(
                    requirement_id="MRK.alpha.trace",
                    satisfied_by_content_id=trace.output_content_id,
                    reason="الأثرُ ينتهي إلى هذه العقدة ببصمتها",
                ),
                ClosureRequirement(
                    requirement_id="MRK.alpha.branches",
                    satisfied_by_content_id=SEED_NODE.content_id,
                    reason="سجلُّ الفروع تامٌّ بأحكامه وبقاياه",
                ),
            ),
            invariant_audit=InvariantAudit(
                audited_invariants=PRESERVED,
                passed=True,
                reason="ثوابتُ النمط مُدقَّقةٌ على مخرج الحركة",
            ),
            residuals=(),
        ),
        gate_id="gate.closure.minimal",
    )
    assert closure.closed is not None
    return closure.closed
