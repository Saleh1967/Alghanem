"""`G0.SDAL-0.TRANSITION`: عقدُ الانتقال السباعيّ، وصعودُ خانةٍ واحدة، والترقية.

    StructuralTransition = <Input, Difference, Invariant, Gate, Output, Residual, Trace>

والانتقالُ لا يُكتَب بيدٍ: يمرُّ ببوّابات النواة الفراكتاليّة المحايدة، ثمّ تُقرَأ
حقولُه السبعةُ من نتيجتها. وأثرُ المخرج يمتدُّ على أثر المدخل بعينه، فلا يُعاد
بناؤه بعد وقوعه.

ونمطُ انتقال الهويّة مُصرَّحٌ لا مفترَض:

    SameEntityRescaling      → مفتوحٌ في هذا الطور، وعينُ الهويّة محفوظة
    CertifiedBranchBirth     → مُسمًّى مؤجَّلٌ حتّى تُصدِر سلطةٌ خارجيّةٌ شهادتَه

فلا تمنح هذه الطبقةُ نفسَها رخصةَ فرعٍ ولا شهادةَ ولادة، وعدمُ التصريح رفضٌ لا
حملٌ على أقرب نمط.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from alghanem.fractal_generation import (
    BranchAdjudicationGate,
    BranchAssessment,
    BranchStanding,
    DeclaredDifference,
    ExpansionCandidate,
    ExpansionSet,
    FractalNode,
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
    NO_BRANCH_BIRTH_WITHOUT_EXTERNAL_CERTIFICATE,
    NO_IMPLICIT_IDENTITY_MODE,
    STRUCTURAL_TRANSITION_CONTRACT_FIELDS,
    THE_TRACE_IS_CUMULATIVE_NOT_RECONSTRUCTED,
    ZERO_ONE_BOUND,
    StructuralDalError,
)
from .residual import ResidualReading, read_residuals
from .slots import StructuralWhole
from .space import (
    ACCRETION_PATTERN,
    PATTERN_REF,
    PRESERVED_INVARIANTS,
    PROPOSAL_PROVENANCE,
    SCALE_SPACE,
)

__all__ = [
    "DeferredBranchBirth",
    "IdentityTransitionAvailability",
    "IdentityTransitionMode",
    "ScaleAscent",
    "StructuralTransition",
    "ascend_one_slot",
    "availability_of",
    "request_part_branch_birth",
]


class IdentityTransitionMode(Enum):
    """نمطا انتقال الهويّة؛ مفردةٌ مغلقةٌ يُصرَّح بأحدها ولا يُفترَض."""

    SAME_ENTITY_RESCALING = "same_entity_rescaling"
    CERTIFIED_BRANCH_BIRTH = "certified_branch_birth"


class IdentityTransitionAvailability(Enum):
    """إتاحةُ النمط في هذا الطور؛ مفتوحٌ أو مؤجَّلٌ لانعدام سلطته."""

    OPEN = "open"
    DEFERRED = "deferred"


def availability_of(mode: IdentityTransitionMode) -> IdentityTransitionAvailability:
    """إتاحةُ نمطٍ بعينه؛ والولادةُ المشهودةُ مؤجَّلةٌ بلا سلطةٍ خارجيّة."""

    if not isinstance(mode, IdentityTransitionMode):
        raise StructuralDalError("نمطُ انتقال الهويّة عضوٌ في مفردته المغلقة")
    if mode is IdentityTransitionMode.SAME_ENTITY_RESCALING:
        return IdentityTransitionAvailability.OPEN
    return IdentityTransitionAvailability.DEFERRED


_ADJUDICATION_GATE = "gate.adjudication.structural_dal.slot"
_TRANSITION_GATE = "gate.transition.structural_dal.slot"


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
    """صعودُ خانةٍ واحدة: كلٌّ قبل، وكلٌّ بعد، ونمطُ هويّةٍ مُصرَّح، وعقدٌ يربطهما."""

    before: StructuralWhole
    after: StructuralWhole
    transition: StructuralTransition
    mode: IdentityTransitionMode

    def __post_init__(self) -> None:
        if not isinstance(self.mode, IdentityTransitionMode):
            raise StructuralDalError(
                "نمطُ انتقال الهويّة مُصرَّح؛ و" + NO_IMPLICIT_IDENTITY_MODE
            )
        if self.mode is not IdentityTransitionMode.SAME_ENTITY_RESCALING:
            raise StructuralDalError(
                "الصعودُ إعادةُ مقياسٍ لعين الكيان؛ و"
                + NO_BRANCH_BIRTH_WITHOUT_EXTERNAL_CERTIFICATE
            )
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
    def preserves_instance_identity(self) -> bool:
        """هل بقيت عينُ الهويّة عبر إعادة المقياس؟"""

        return (
            self.after.anchor_id == self.before.anchor_id
            and self.transition.preserves_instance_identity
        )

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
    mode: IdentityTransitionMode,
    evidence_ref: str = "evidence.structural_dal.zero_one",
) -> ScaleAscent:
    """اصعد خانةً واحدةً بنمطٍ مُصرَّح؛ والمِرساةُ والأثرُ يُحفظان.

    ولا افتراضَ للنمط: من لم يُصرِّح رُفض، ومن طلب ولادةَ فرعٍ رُفض لانعدام
    السلطة التي تُصدِر شهادتَه.
    """

    if not isinstance(mode, IdentityTransitionMode):
        raise StructuralDalError(
            "نمطُ انتقال الهويّة مُصرَّح؛ و" + NO_IMPLICIT_IDENTITY_MODE
        )
    if availability_of(mode) is IdentityTransitionAvailability.DEFERRED:
        raise StructuralDalError(
            f"نمطٌ مؤجَّلٌ في هذا الطور: {mode.value}؛ و"
            + NO_BRANCH_BIRTH_WITHOUT_EXTERNAL_CERTIFICATE
        )
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
        mode=mode,
        transition=StructuralTransition(
            fractal_transition=decision.transition,
            cumulative_trace=cumulative,
            added_slot_index=index,
            parent_anchor_id=before.parent_anchor_id,
        ),
    )


@dataclass(frozen=True, slots=True)
class DeferredBranchBirth:
    """طلبُ ولادةِ فرعٍ مرفوعٌ ومؤجَّل: جزؤُه، ومِرساتُه المطلوبة، وسببُ تأجيله.

    فالجزءُ لا يصير كلًّا مستقلًّا في هذا الطور: مِرساتُه غيرُ مِرساة أبيه،
    وإصدارُ شهادةِ الولادة سلطةٌ خارج هذه الطبقة لم تَقُم بعد.
    """

    source_part: StructuralPart
    requested_mode: IdentityTransitionMode
    refusal: str

    def __post_init__(self) -> None:
        if not isinstance(self.source_part, StructuralPart):
            raise StructuralDalError("الطلبُ يقع على جزءٍ من نوعه")
        if self.requested_mode is not IdentityTransitionMode.CERTIFIED_BRANCH_BIRTH:
            raise StructuralDalError(
                "طلبُ صيرورة الجزء كلًّا ولادةُ فرعٍ لا إعادةُ مقياس؛ و"
                + NO_BRANCH_BIRTH_WITHOUT_EXTERNAL_CERTIFICATE
            )
        if not isinstance(self.refusal, str) or not self.refusal.strip():
            raise StructuralDalError("سببُ التأجيل نصٌّ غيرُ فارغ")

    @property
    def availability(self) -> IdentityTransitionAvailability:
        """إتاحةُ النمط المطلوب؛ مؤجَّلةٌ بحكم انعدام سلطته."""

        return availability_of(self.requested_mode)

    @property
    def requested_anchor_id(self) -> str:
        """المِرساةُ التي كانت ستُطلَب للفرع؛ مُعلَنةٌ ولا تُصدَر."""

        return self.source_part.part_anchor_id

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الطلب المؤجَّل للعرض."""

        return {
            "part_id": self.source_part.part_id,
            "requested_mode": self.requested_mode.value,
            "availability": self.availability.value,
            "requested_anchor_id": self.requested_anchor_id,
            "refusal": self.refusal,
        }


def request_part_branch_birth(
    decomposition: StructuralDecomposition,
    role: SlotRole,
) -> DeferredBranchBirth:
    """اطلب صيرورةَ جزءٍ كلًّا؛ والجوابُ تأجيلٌ مُسمًّى لا ترقيةٌ تقع.

    ولا يُقاس التأجيلُ ببقايا التفكيك وحدَها: حتّى لو ارتفع كلُّ حاجب، تبقى
    ولادةُ الفرع موقوفةً على شهادةٍ من خارج هذه الطبقة.
    """

    if not isinstance(decomposition, StructuralDecomposition):
        raise StructuralDalError("الطلبُ يقع على تفكيكٍ من نوعه")
    part = decomposition.part_of(role)
    if part.is_empty:
        raise StructuralDalError("جزءٌ خالٍ لا يُطلَب له ولادةٌ أصلًا")
    return DeferredBranchBirth(
        source_part=part,
        requested_mode=IdentityTransitionMode.CERTIFIED_BRANCH_BIRTH,
        refusal=(
            f"ولادةُ فرعٍ عن الجزء {part.part_id} مؤجَّلة؛ و"
            + NO_BRANCH_BIRTH_WITHOUT_EXTERNAL_CERTIFICATE
        ),
    )


def _refuse_a_contract_with_missing_fields() -> None:
    """ارفض عند الاستيراد عقدَ انتقالٍ ينقصه حقلٌ من حقوله السبعة."""

    for field_name in STRUCTURAL_TRANSITION_CONTRACT_FIELDS:
        if not hasattr(StructuralTransition, field_name):
            raise StructuralDalError(f"عقدُ الانتقال ينقصه حقلُ {field_name}")


_refuse_a_contract_with_missing_fields()
