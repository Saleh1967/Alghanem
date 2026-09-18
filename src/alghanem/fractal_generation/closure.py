"""الإغلاقُ عند المقياس: أقلُّ تمامٍ لازمٍ، لا استنفادٌ ولا ضرورةُ رفع.

    Closure  =  MinimalCompleteAtCurrentScale

    Closure  ≠  Exhaustion   ∧   Closure ≠ LiftNecessity
    Closure  ≠  Meaning      ∧   Closure ≠ Truth

**ولا يُنشِئ المستدعي عقدةً مغلقة**: `ClosedFractalNode` لا تُنشَأ إلّا برمزِ
إصدارٍ داخليٍّ بيد `ClosureGate`، ولا تُصدَر إلّا باجتماع خمسةٍ:

1. تغطيةُ كلِّ متطلّبات `MinimumCompleteRequirement` عند المقياس،
2. تدقيقُ ثوابتَ ناجحٌ مُسمًّى،
3. غيابُ بقايا مانعة،
4. أثرٌ قابلٌ لإعادة البناء ينتهي إلى العقدة بعينها،
5. فصلٌ أفقيٌّ تامٌّ كلُّ مقبولٍ فيه تحرَّك فعلًا.

**والسجلُّ لا يُمحى** (`NoResidualErasure`): العقدةُ المغلقةُ تحمل أحكامَ الفروع
كلَّها — المقبولَ والممنوعَ والمؤجَّل — وبقاياها مُسمّاة.

تسجيلٌ لا سلطة: لا ولادةَ، ولا حكمَ ولادةٍ، ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from ..canonical_content import is_canonical_digest
from .branch import BranchAdjudicationDecision, BranchAssessment
from .laws import (
    CLOSURE_IS_NOT_EXHAUSTION,
    CLOSURE_IS_NOT_LIFT_NECESSITY,
    NO_FRACTAL_TRANSITION_WITHOUT_RECONSTRUCTIBLE_TRACE,
    NO_RESIDUAL_ERASURE,
)
from .node import FractalNode, FractalResidual
from .scale import FractalScaleRef
from .trace import FractalTrace, FractalTransitionTraceStep

__all__ = [
    "ClosedFractalNode",
    "ClosureCandidate",
    "ClosureDecision",
    "ClosureError",
    "ClosureGate",
    "ClosureRequirement",
    "ClosureStatus",
    "InvariantAudit",
    "MinimumCompleteRequirement",
    "ScaleClosureContract",
]


class ClosureError(ValueError):
    """رفضٌ عند تكوين متطلّبٍ أو عقدِ إغلاقٍ أو مرشَّحٍ أو قرارٍ."""


class _IssuanceToken:
    """رمزُ إصدارٍ داخليّ؛ وجودُه بيد البوّابة وحدَها لا بيد المستدعي."""

    __slots__ = ()


_CLOSURE_ISSUANCE: Final[_IssuanceToken] = _IssuanceToken()


def _named_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ClosureError(f"{label} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class MinimumCompleteRequirement:
    """متطلَّبُ أقلِّ التمام عند مقياس: ما لا تكون العقدةُ تامّةً بدونه."""

    requirement_id: str
    statement: str
    evidence_kind: str

    def __post_init__(self) -> None:
        _named_text(self.requirement_id, "مُعرِّفُ المتطلَّب")
        _named_text(self.statement, "نصُّ المتطلَّب")
        _named_text(self.evidence_kind, "جنسُ الدليل الذي يُغطّيه")


@dataclass(frozen=True, slots=True)
class ScaleClosureContract:
    """عقدُ إغلاقِ مقياس: متطلّباتُ أقلِّ التمام فيه، لا استيفاءُ ما فوقه."""

    scale_ref: FractalScaleRef
    requirements: tuple[MinimumCompleteRequirement, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.scale_ref, FractalScaleRef):
            raise ClosureError("عقدُ الإغلاق يقع عند مقياسٍ بمرجعه")
        if not isinstance(self.requirements, tuple) or not self.requirements:
            raise ClosureError("عقدُ الإغلاق متطلَّبٌ واحدٌ فأكثر")
        seen: set[str] = set()
        for requirement in self.requirements:
            if not isinstance(requirement, MinimumCompleteRequirement):
                raise ClosureError("عضوٌ في متطلّبات الإغلاق خارج نوعه")
            if requirement.requirement_id in seen:
                raise ClosureError("متطلَّبٌ مُكرَّرٌ في عقدٍ واحد")
            seen.add(requirement.requirement_id)

    @property
    def requirement_ids(self) -> frozenset[str]:
        """مُعرِّفاتُ المتطلّبات مجموعةً."""

        return frozenset(
            requirement.requirement_id for requirement in self.requirements
        )


@dataclass(frozen=True, slots=True)
class ClosureRequirement:
    """تغطيةُ متطلَّبٍ بعينه: بأيِّ محتوًى غُطِّي، وبأيِّ سببٍ مُسمًّى."""

    requirement_id: str
    satisfied_by_content_id: str
    reason: str

    def __post_init__(self) -> None:
        _named_text(self.requirement_id, "مُعرِّفُ المتطلَّب المُغطّى")
        if not is_canonical_digest(self.satisfied_by_content_id):
            raise ClosureError("التغطيةُ تُشير إلى محتوًى ببصمةٍ قانونيّة")
        _named_text(self.reason, "سببُ التغطية")


@dataclass(frozen=True, slots=True)
class InvariantAudit:
    """تدقيقُ ثوابت: ما دُقِّق، وهل نجح، وبأيِّ سبب."""

    audited_invariants: tuple[str, ...]
    passed: bool
    reason: str

    def __post_init__(self) -> None:
        if not isinstance(self.audited_invariants, tuple):
            raise ClosureError("الثوابتُ المُدقَّقة مجموعةٌ مُصرَّحٌ بها")
        for invariant in self.audited_invariants:
            _named_text(invariant, "عضوٌ في الثوابت المُدقَّقة")
        if type(self.passed) is not bool:
            raise ClosureError("نتيجةُ التدقيق حكمٌ ثنائيٌّ صريح")
        _named_text(self.reason, "سببُ نتيجة التدقيق")


@dataclass(frozen=True, slots=True)
class ClosureCandidate:
    """مرشَّحُ إغلاق: عقدةٌ وأثرُها وفصلُها وعقدُ مقياسها وتغطيتُها وتدقيقُها."""

    node: FractalNode
    trace: FractalTrace
    adjudication: BranchAdjudicationDecision
    branch_transitions: tuple[FractalTransitionTraceStep, ...]
    contract: ScaleClosureContract
    coverage: tuple[ClosureRequirement, ...]
    invariant_audit: InvariantAudit
    residuals: tuple[FractalResidual, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.node, FractalNode):
            raise ClosureError("مرشَّحُ الإغلاق عقدةٌ من نوعها")
        if not isinstance(self.trace, FractalTrace):
            raise ClosureError("مرشَّحُ الإغلاق يحمل أثرًا متّصلًا من نوعه")
        if not isinstance(self.adjudication, BranchAdjudicationDecision):
            raise ClosureError("مرشَّحُ الإغلاق يحمل قرارَ فصلٍ من نوعه")
        if not isinstance(self.branch_transitions, tuple):
            raise ClosureError("حركاتُ الفروع الأفقيّةُ مجموعةٌ مُصرَّحٌ بها")
        for step in self.branch_transitions:
            if not isinstance(step, FractalTransitionTraceStep):
                raise ClosureError("عضوٌ في حركات الفروع خارج نوع خطوة الأثر")
        if not isinstance(self.contract, ScaleClosureContract):
            raise ClosureError("مرشَّحُ الإغلاق يُقاس على عقد إغلاقٍ من نوعه")
        if not isinstance(self.coverage, tuple):
            raise ClosureError("تغطيةُ المتطلّبات مجموعةٌ مُصرَّحٌ بها")
        for entry in self.coverage:
            if not isinstance(entry, ClosureRequirement):
                raise ClosureError("عضوٌ في التغطية خارج نوعه")
        if not isinstance(self.invariant_audit, InvariantAudit):
            raise ClosureError("تدقيقُ الثوابت من نوعه")
        if not isinstance(self.residuals, tuple):
            raise ClosureError("بقايا المرشَّح مجموعةٌ مُصرَّحٌ بها")
        for residual in self.residuals:
            if not isinstance(residual, FractalResidual):
                raise ClosureError("عضوٌ في بقايا المرشَّح خارج نوعه")

    @property
    def horizontal_steps(self) -> tuple[FractalTransitionTraceStep, ...]:
        """خطواتُ الأثر الرأسيّ وحركاتُ الإخوة الأفقيّة بلا تكرار."""

        steps = list(self.trace.steps)
        for step in self.branch_transitions:
            if step not in steps:
                steps.append(step)
        return tuple(steps)

    @property
    def all_residuals(self) -> tuple[FractalResidual, ...]:
        """بقايا المرشَّح وحركاتِه وفصلِه مجموعةً واحدةً بلا محو."""

        return (
            self.residuals
            + tuple(
                residual
                for step in self.horizontal_steps
                for residual in step.residuals
            )
            + self.adjudication.residuals
        )


@dataclass(frozen=True, slots=True)
class ClosedFractalNode:
    """عقدةٌ بلغت أقلَّ التمام عند مقياسها؛ ولا تُنشَأ إلّا ببوّابة الإغلاق."""

    candidate: ClosureCandidate
    gate_id: str
    issuance: _IssuanceToken

    def __post_init__(self) -> None:
        if self.issuance is not _CLOSURE_ISSUANCE:
            raise ClosureError(
                "العقدةُ المغلقةُ ناتجُ بوّابةٍ لا حقلٌ يكتبه المستدعي؛ و"
                + CLOSURE_IS_NOT_LIFT_NECESSITY
            )
        if not isinstance(self.candidate, ClosureCandidate):
            raise ClosureError("العقدةُ المغلقةُ فوق مرشَّحٍ من نوعه")
        _named_text(self.gate_id, "مُعرِّفُ بوّابة الإغلاق")

    @property
    def node(self) -> FractalNode:
        """العقدةُ نفسُها."""

        return self.candidate.node

    @property
    def scale_ref(self) -> FractalScaleRef:
        """المقياسُ الذي تمّت عنده، لا المقياسُ الذي فوقه."""

        return self.candidate.contract.scale_ref

    @property
    def trace(self) -> FractalTrace:
        """أثرُها المتّصل."""

        return self.candidate.trace

    @property
    def branch_record(self) -> tuple[BranchAssessment, ...]:
        """سجلُّ فروعها كلِّها: المقبولُ والممنوعُ والمؤجَّل."""

        return self.candidate.adjudication.assessments

    @property
    def residuals(self) -> tuple[FractalResidual, ...]:
        """بقاياها كلُّها مُسمّاةً بلا محو."""

        return self.candidate.all_residuals


class ClosureStatus(Enum):
    """حالُ بوّابة الإغلاق؛ مفردةٌ مغلقة."""

    CLOSED = "closed"
    BLOCKED = "blocked"
    DEFERRED = "deferred"


@dataclass(frozen=True, slots=True)
class ClosureDecision:
    """قرارُ الإغلاق: حالُه، وسببُه، وعقدتُه إن صدرت، وبقاياه."""

    status: ClosureStatus
    reason: str
    closed: ClosedFractalNode | None
    residuals: tuple[FractalResidual, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.status, ClosureStatus):
            raise ClosureError("حالُ القرار عضوٌ في مفردته المغلقة")
        _named_text(self.reason, "سببُ القرار")
        if not isinstance(self.residuals, tuple):
            raise ClosureError("بقايا القرار مجموعةٌ مُصرَّحٌ بها")
        if self.status is ClosureStatus.CLOSED:
            if not isinstance(self.closed, ClosedFractalNode):
                raise ClosureError("قرارُ الإغلاق يحمل عقدتَه الصادرة")
        elif self.closed is not None:
            raise ClosureError("قرارٌ غيرُ مُغلِقٍ لا يحمل عقدةً مغلقة")


class ClosureGate:
    """البوّابةُ الوحيدةُ التي تُصدِر `ClosedFractalNode`؛ تمامًا عند المقياس لا فوقه."""

    @staticmethod
    def assess(*, candidate: ClosureCandidate, gate_id: str) -> ClosureDecision:
        """اقرأ أقلَّ التمام عند المقياس الجاري؛ ولا تقرأ استنفادًا ولا ضرورةَ رفع."""

        if not isinstance(candidate, ClosureCandidate):
            raise ClosureError("المقيسُ مرشَّحُ إغلاقٍ من نوعه")
        _named_text(gate_id, "مُعرِّفُ بوّابة الإغلاق")
        residuals = candidate.all_residuals
        if candidate.node.identity.scale_ref != candidate.contract.scale_ref:
            return ClosureDecision(
                status=ClosureStatus.BLOCKED,
                reason="عقدُ الإغلاق ليس عقدَ مقياس هذه العقدة بمرجعه",
                closed=None,
                residuals=residuals,
            )
        if candidate.trace.output_content_id != candidate.node.content_id:
            return ClosureDecision(
                status=ClosureStatus.BLOCKED,
                reason=(
                    "الأثرُ لا ينتهي إلى هذه العقدة ببصمتها؛ و"
                    + NO_FRACTAL_TRANSITION_WITHOUT_RECONSTRUCTIBLE_TRACE
                ),
                closed=None,
                residuals=residuals,
            )
        covered = {entry.requirement_id for entry in candidate.coverage}
        required = set(candidate.contract.requirement_ids)
        if covered - required:
            return ClosureDecision(
                status=ClosureStatus.BLOCKED,
                reason="تغطيةٌ تُشير إلى متطلَّبٍ خارج عقد هذا المقياس",
                closed=None,
                residuals=residuals,
            )
        if required - covered:
            return ClosureDecision(
                status=ClosureStatus.DEFERRED,
                reason=(
                    "متطلَّبٌ من أقلِّ التمام لم يُغطَّ بعد؛ و" + CLOSURE_IS_NOT_EXHAUSTION
                ),
                closed=None,
                residuals=residuals,
            )
        if not candidate.invariant_audit.passed:
            return ClosureDecision(
                status=ClosureStatus.BLOCKED,
                reason="تدقيقُ الثوابت لم ينجح: " + candidate.invariant_audit.reason,
                closed=None,
                residuals=residuals,
            )
        blocking = tuple(residual for residual in residuals if residual.blocking)
        if blocking:
            return ClosureDecision(
                status=ClosureStatus.BLOCKED,
                reason=("بقيّةٌ مانعةٌ قائمةٌ لم تُرفَع؛ و" + NO_RESIDUAL_ERASURE),
                closed=None,
                residuals=residuals,
            )
        moved = {
            step.transition.movement.candidate_id for step in candidate.horizontal_steps
        }
        admitted = set(candidate.adjudication.co_admissible_ids)
        if admitted - moved:
            return ClosureDecision(
                status=ClosureStatus.DEFERRED,
                reason=(
                    "فرعٌ مقبولٌ لم تقع حركتُه بعد، فالفصلُ الأفقيُّ غيرُ تامّ؛ و"
                    + NO_RESIDUAL_ERASURE
                ),
                closed=None,
                residuals=residuals,
            )
        return ClosureDecision(
            status=ClosureStatus.CLOSED,
            reason=(
                "أقلُّ التمام عند هذا المقياس مُغطًّى بأثرٍ متّصلٍ وفصلٍ تامّ؛ و"
                + CLOSURE_IS_NOT_EXHAUSTION
            ),
            closed=ClosedFractalNode(
                candidate=candidate, gate_id=gate_id, issuance=_CLOSURE_ISSUANCE
            ),
            residuals=residuals,
        )
