"""`G0.SDAL-0.TRANSITION`: عقدُ الانتقال السباعيّ، وصعودُ خانةٍ واحدة، والترقية.

    StructuralTransition = <Input, Difference, Invariant, Gate, Output, Residual, Trace>

والانتقالُ لا يُكتَب بيدٍ: يمرُّ ببوّابات النواة الفراكتاليّة المحايدة، ثمّ تُقرَأ
حقولُه السبعةُ من نتيجتها. وأثرُ المخرج يمتدُّ على أثر المدخل بعينه، فلا يُعاد
بناؤه بعد وقوعه.

والفركتاليّةُ هنا ليست `1 → 2`، بل أن يدخل ناتجُ المستوى السابق في اللاحق مع
حفظ نسبه:

    PartAtScaleN  ->  WholeAtScaleNPlus1
    child.parent_anchor_id == parent.anchor_id
"""

from __future__ import annotations

from dataclasses import dataclass

from alghanem.fractal_generation import (
    BranchAdjudicationGate,
    BranchAssessment,
    BranchStanding,
    DeclaredDifference,
    ExpansionCandidate,
    ExpansionSet,
    FractalIdentity,
    FractalNode,
    FractalSeed,
    FractalTrace,
    FractalTransition,
    FractalTransitionGate,
    IdentityPreservingTransformationCandidate,
    PatternConformanceGate,
    PatternConformanceStatus,
    PatternConformantDifference,
)

from .hypothesis import SlotRole, StructuralDecomposition, StructuralPart
from .laws import (
    BLOCKING_RESIDUAL_FORBIDS_POSITIVE_PROMOTION,
    STRUCTURAL_TRANSITION_CONTRACT_FIELDS,
    THE_PART_KEEPS_ITS_PARENT_ANCHOR,
    THE_TRACE_IS_CUMULATIVE_NOT_RECONSTRUCTED,
    ZERO_ONE_BOUND,
    StructuralDalError,
)
from .residual import PromotionStanding, ResidualReading, read_residuals
from .slots import StructuralWhole
from .space import (
    ACCRETION_PATTERN,
    PATTERN_REF,
    PRESERVED_INVARIANTS,
    PROPOSAL_PROVENANCE,
    SCALE_SPACE,
    SLOT_SCALE_REF,
)

__all__ = [
    "PromotedWhole",
    "ScaleAscent",
    "StructuralTransition",
    "ascend_one_slot",
    "promote_part_to_whole",
]

_ADJUDICATION_GATE = "gate.adjudication.structural_dal.slot"
_TRANSITION_GATE = "gate.transition.structural_dal.slot"
_IDENTITY_CRITERION = "criterion.structural_dal.whole_instance"


@dataclass(frozen=True, slots=True)
class StructuralTransition:
    """قراءةُ الانتقال بحقوله السبعة؛ كلُّها مُشتَقّةٌ من نتيجة بوّابته."""

    fractal_transition: FractalTransition
    cumulative_trace: FractalTrace
    added_slot_index: int
    parent_anchor_id: str | None

    def __post_init__(self) -> None:
        if not isinstance(self.fractal_transition, FractalTransition):
            raise StructuralDalError("قراءةُ الانتقال فوق انتقالٍ صادرٍ عن بوّابته")
        if not isinstance(self.cumulative_trace, FractalTrace):
            raise StructuralDalError("أثرُ الانتقال أثرٌ من نوعه")
        if self.cumulative_trace.steps[-1].transition is not self.fractal_transition:
            raise StructuralDalError(
                "آخرُ خطوةٍ في الأثر ليست هذا الانتقال بعينه؛ و"
                + THE_TRACE_IS_CUMULATIVE_NOT_RECONSTRUCTED
            )
        if not isinstance(self.added_slot_index, int) or isinstance(
            self.added_slot_index, bool
        ):
            raise StructuralDalError("موضعُ الخانة المُضافة عددٌ صحيح")
        if self.added_slot_index < 1:
            raise StructuralDalError("الخانةُ المُضافةُ تأتي بعد خانةٍ قائمة")

    @property
    def input_identity(self) -> str:
        """هويّةُ الكلّ قبل الانتقال."""

        return self.fractal_transition.identity_before.identity_id

    @property
    def difference(self) -> DeclaredDifference:
        """الفرقُ المُصرَّحُ الذي وقع الانتقالُ عليه."""

        movement = self.fractal_transition.movement
        if not isinstance(movement, IdentityPreservingTransformationCandidate):
            raise StructuralDalError("حركةُ هذا الطور حافظةٌ للهويّة لا غير")
        return movement.conformant.candidate.declared_difference

    @property
    def invariant(self) -> tuple[str, ...]:
        """الثوابتُ التي قيست مطابقتُها لعقد النمط."""

        movement = self.fractal_transition.movement
        if not isinstance(movement, IdentityPreservingTransformationCandidate):
            raise StructuralDalError("حركةُ هذا الطور حافظةٌ للهويّة لا غير")
        return movement.conformant.checked_invariants

    @property
    def gate(self) -> tuple[str, ...]:
        """بوّابتا الفصل والانتقال بأعيانهما."""

        return (
            self.fractal_transition.adjudication_gate_id,
            self.fractal_transition.gate_id,
        )

    @property
    def output_identity(self) -> str:
        """هويّةُ الكلّ بعد الانتقال؛ وهي عينُ ما قبلَه في هذا الطور."""

        return self.fractal_transition.identity_after.identity_id

    @property
    def residual(self) -> tuple[ResidualReading, ...]:
        """بقايا الانتقال مُصنَّفة."""

        return read_residuals(self.fractal_transition.residuals)

    @property
    def trace(self) -> FractalTrace:
        """الأثرُ التراكميُّ حتّى هذا الانتقال."""

        return self.cumulative_trace

    @property
    def preserves_instance_identity(self) -> bool:
        """هل بقيت عينُ الهويّة عبر الانتقال؟"""

        return self.input_identity == self.output_identity

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى العقد السباعيّ للعرض."""

        return {
            "input_identity": self.input_identity,
            "difference": self.difference.as_canonical_content(),
            "invariant": list(self.invariant),
            "gate": list(self.gate),
            "output_identity": self.output_identity,
            "residual": [reading.as_canonical_content() for reading in self.residual],
            "trace": len(self.trace.steps),
            "added_slot_index": self.added_slot_index,
            "parent_anchor_id": self.parent_anchor_id,
        }


@dataclass(frozen=True, slots=True)
class ScaleAscent:
    """صعودُ خانةٍ واحدة: كلٌّ قبل، وكلٌّ بعد، وعقدُ انتقالٍ يربطهما."""

    before: StructuralWhole
    after: StructuralWhole
    transition: StructuralTransition

    def __post_init__(self) -> None:
        if self.after.slot_count != self.before.slot_count + 1:
            raise StructuralDalError("الصعودُ خانةٌ واحدةٌ لا أكثر")
        if self.after.anchor_id != self.before.anchor_id:
            raise StructuralDalError("الصعودُ يحفظ عينَ المِرساة")
        if self.after.tokens[: self.before.slot_count] != self.before.tokens:
            raise StructuralDalError("الصعودُ يحفظ ترتيبَ الخانات السابقة")
        before_steps = () if self.before.trace is None else self.before.trace.steps
        after_steps = () if self.after.trace is None else self.after.trace.steps
        if after_steps[:-1] != before_steps:
            raise StructuralDalError(
                "أثرُ المخرج لا يمتدُّ على أثر المدخل؛ و"
                + THE_TRACE_IS_CUMULATIVE_NOT_RECONSTRUCTED
            )

    @property
    def added_token(self) -> str:
        """رمزُ الخانة المُضافة."""

        return self.after.tokens[-1]

    @property
    def trace_is_cumulative(self) -> bool:
        """هل زاد الأثرُ خطوةً واحدةً فوق سابقه بلا إعادة بناء؟"""

        return self.after.trace_steps == self.before.trace_steps + 1


def _conformant(
    candidate: ExpansionCandidate, node: FractalNode
) -> PatternConformantDifference:
    decision = PatternConformanceGate.assess(
        candidate=candidate,
        pattern=ACCRETION_PATTERN,
        node=node,
        space=SCALE_SPACE,
    )
    if decision.status is not PatternConformanceStatus.CONFORMANT or (
        decision.conformant is None
    ):
        raise StructuralDalError("اقتراحُ الضمّ لم يُطابِق عقدَ نمطه")
    return decision.conformant


def ascend_one_slot(
    before: StructuralWhole,
    added_token: str,
    *,
    evidence_ref: str = "evidence.structural_dal.zero_one",
) -> ScaleAscent:
    """اصعد خانةً واحدةً عبر بوّاباتها؛ والمِرساةُ والأثرُ يُحفظان."""

    if not isinstance(before, StructuralWhole):
        raise StructuralDalError("الصعودُ يقع على كلٍّ من نوعه")
    if not isinstance(added_token, str) or not added_token.strip():
        raise StructuralDalError("رمزُ الخانة المُضافة نصٌّ غيرُ فارغ")
    index = before.slot_count
    if index + 1 > ZERO_ONE_BOUND:
        raise StructuralDalError(
            f"صعودٌ فوق حدِّ هذا الطور {ZERO_ONE_BOUND}؛ وسلطتُه لم تُفتَح"
        )
    candidate_id = f"accretion.{before.whole_id}.{index}"
    candidate = ExpansionCandidate(
        candidate_id=candidate_id,
        source=before.node.as_ref(),
        pattern_ref=PATTERN_REF,
        declared_difference=DeclaredDifference(
            difference_id=f"difference.{candidate_id}",
            dimension="slot_accretion",
            description=f"ضمُّ الخانة رقم {index} إلى محتوى الكلّ",
            preserved_invariants=PRESERVED_INVARIANTS,
        ),
        proposal_provenance=PROPOSAL_PROVENANCE,
    )
    movement = IdentityPreservingTransformationCandidate(
        conformant=_conformant(candidate, before.node),
        carrier_id=before.node.carrier_id,
        identity_before=before.node.identity,
        identity_after=before.node.identity,
        preserved_invariants=PRESERVED_INVARIANTS,
        output_content=before.node.content + ((f"slot.{index}", added_token),),
    )
    adjudication = BranchAdjudicationGate.adjudicate(
        expansion_set=ExpansionSet(
            source=before.node.as_ref(), candidates=(candidate,)
        ),
        assessments=(
            BranchAssessment(
                candidate_id=candidate_id,
                standing=BranchStanding.ADMITTED,
                reason="ضمُّ الخانة التالية مُطابِقٌ لعقد النمط مع حفظ عين المِرساة",
                residuals=(),
                movement=movement,
            ),
        ),
        gate_id=_ADJUDICATION_GATE,
    )
    decision = FractalTransitionGate.open_transition(
        adjudication=adjudication,
        candidate_id=candidate_id,
        source_node=before.node,
        transition_id=f"transition.{candidate_id}",
        gate_id=_TRANSITION_GATE,
        evidence_ref=evidence_ref,
        output_node_id=f"node.{before.whole_id}.{index}",
    )
    previous = () if before.trace is None else before.trace.steps
    cumulative = FractalTrace(steps=previous + (decision.trace_step,))
    after = StructuralWhole(
        whole_id=f"{before.whole_id}.slot{index}",
        node=decision.output_node,
        provenance=before.provenance,
        parent_anchor_id=before.parent_anchor_id,
        descent_depth=before.descent_depth,
        trace=cumulative,
    )
    return ScaleAscent(
        before=before,
        after=after,
        transition=StructuralTransition(
            fractal_transition=decision.transition,
            cumulative_trace=cumulative,
            added_slot_index=index,
            parent_anchor_id=before.parent_anchor_id,
        ),
    )


@dataclass(frozen=True, slots=True)
class PromotedWhole:
    """جزءٌ صار كلًّا في المقياس التالي، ونسبُه محفوظٌ بمِرساة أبيه."""

    source_part: StructuralPart
    whole: StructuralWhole

    def __post_init__(self) -> None:
        if self.whole.parent_anchor_id != self.source_part.parent_anchor_id:
            raise StructuralDalError(
                "الكلُّ المُرقّى فقد نسبَه؛ و" + THE_PART_KEEPS_ITS_PARENT_ANCHOR
            )
        if self.whole.tokens != self.source_part.tokens:
            raise StructuralDalError("الكلُّ المُرقّى يحمل رموزَ جزئه بعينها")

    @property
    def keeps_parent_anchor(self) -> bool:
        """هل بقيت مِرساةُ الأب في الابن؟"""

        return self.whole.parent_anchor_id == self.source_part.parent_anchor_id


def promote_part_to_whole(
    decomposition: StructuralDecomposition,
    role: SlotRole,
) -> PromotedWhole:
    """رقِّ جزءًا إلى كلٍّ في المقياس التالي، ما لم تحجب بقيّةٌ حاجبة."""

    if not isinstance(decomposition, StructuralDecomposition):
        raise StructuralDalError("الترقيةُ تقع على تفكيكٍ من نوعه")
    standing = decomposition.promotion_standing
    if standing is PromotionStanding.PROMOTION_BLOCKED:
        raise StructuralDalError(
            "ترقيةٌ مرفوضةٌ لبقيّةٍ حاجبة؛ و"
            + BLOCKING_RESIDUAL_FORBIDS_POSITIVE_PROMOTION
        )
    part = decomposition.part_of(role)
    if part.is_empty:
        raise StructuralDalError("جزءٌ خالٍ لا يصير كلًّا مكتملًا")
    parent = decomposition.whole
    child_anchor = f"{parent.anchor_id}.{role.value}"
    content = tuple(
        (f"slot.{position}", slot.token)
        for position, slot in enumerate(part.slot_map)
    )
    node = FractalNode.from_seed(
        FractalSeed(
            seed_id=f"seed.{part.part_id}",
            identity=FractalIdentity(
                identity_id=child_anchor,
                scale_ref=SLOT_SCALE_REF,
                identity_criterion_id=_IDENTITY_CRITERION,
            ),
            carrier_id=parent.node.carrier_id,
            content=content,
        ),
        node_id=f"node.{part.part_id}",
    )
    child = StructuralWhole(
        whole_id=f"{part.part_id}.whole",
        node=node,
        provenance=(
            f"مُرقًّى عن الجزء {part.part_id} في التفكيك "
            f"{decomposition.decomposition_id}"
        ),
        parent_anchor_id=parent.anchor_id,
        descent_depth=parent.descent_depth + 1,
        trace=parent.trace,
    )
    return PromotedWhole(source_part=part, whole=child)


def _refuse_a_contract_with_missing_fields() -> None:
    """ارفض عند الاستيراد عقدَ انتقالٍ ينقصه حقلٌ من حقوله السبعة."""

    for field_name in STRUCTURAL_TRANSITION_CONTRACT_FIELDS:
        if not hasattr(StructuralTransition, field_name):
            raise StructuralDalError(f"عقدُ الانتقال ينقصه حقلُ {field_name}")


_refuse_a_contract_with_missing_fields()
