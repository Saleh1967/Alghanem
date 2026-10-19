"""الحركةُ الفعليّةُ وأثرُها: لا انتقالَ قبل فصلٍ تامّ، ولا أثرَ قبل انتقال.

    Adjudication  →  FractalTransition  →  FractalTransitionTraceStep

**والانتقالُ ناتجُ بوّابةٍ لا حقلٌ يكتبه المستدعي**: `FractalTransition` لا
تُنشَأ إلّا برمزِ إصدارٍ داخليٍّ بيد `FractalTransitionGate`، ولا تقع إلّا على
فرعٍ حُكِم فيه بالقَبول في قرار فصلٍ تامّ.

**والحركةُ الفعليّةُ واحدةٌ من اثنتين**:

    IDENTITY_PRESERVING_TRANSFORMATION  |  BRANCH_BIRTH

**والحركتان أفقيّتان في هذه المرحلة**: المقياسُ قبلُ هو المقياسُ بعدُ بعينه،
لأنّ الرفعَ سلطةٌ لم تُفتَح (`NoHigherScaleWithoutNecessity`).

**والأثرُ متّصلٌ ببصماته** (`NoFractalTransitionWithoutReconstructibleTrace`):

    previous.output_content_id  ==  next.input_content_id

فلا يُقرَأ الترتيبُ وحدَه دليلًا على الاتّصال، ولا يُبنى أثرٌ على مخرجٍ لم يُنتَج.

تسجيلٌ لا سلطة: لا ولادةَ، ولا حكمَ ولادةٍ، ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from ..canonical_content import is_canonical_digest
from .authority_gaps import FractalAuthorityGap
from .branch import (
    BranchAdjudicationDecision,
    BranchBirthCandidate,
    BranchStanding,
    IdentityPreservingTransformationCandidate,
    MovementCandidate,
)
from .expansion import DeclaredDifference
from .laws import (
    CANDIDATE_IS_NOT_TRANSITION,
    NO_FRACTAL_TRANSITION_WITHOUT_RECONSTRUCTIBLE_TRACE,
    NO_HIGHER_SCALE_WITHOUT_NECESSITY,
)
from .node import (
    FractalIdentity,
    FractalNode,
    FractalNodeRef,
    FractalResidual,
)
from .pattern import PatternRef
from .scale import FractalScaleRef

__all__ = [
    "FractalMovementKind",
    "FractalTransition",
    "FractalTransitionDecision",
    "FractalTransitionGate",
    "FractalTransitionTraceStep",
    "FractalTrace",
    "FractalTraceError",
]


class FractalTraceError(ValueError):
    """رفضٌ عند تكوين انتقالٍ أو خطوةِ أثرٍ أو أثرٍ متّصل."""


class _IssuanceToken:
    """رمزُ إصدارٍ داخليّ؛ وجودُه بيد البوّابة وحدَها لا بيد المستدعي."""

    __slots__ = ()


_TRANSITION_ISSUANCE: Final[_IssuanceToken] = _IssuanceToken()


def _named_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise FractalTraceError(f"{label} نصٌّ غير فارغ")
    return value


class FractalMovementKind(Enum):
    """جنسُ الحركة الفعليّة؛ اثنتان لا ثالثةَ لهما في هذه المرحلة."""

    IDENTITY_PRESERVING_TRANSFORMATION = "identity_preserving_transformation"
    BRANCH_BIRTH = "branch_birth"


@dataclass(frozen=True, slots=True)
class FractalTransition:
    """انتقالٌ وقع فعلًا بعد فصلٍ تامّ؛ ولا يُنشَأ إلّا ببوّابته."""

    transition_id: str
    movement_kind: FractalMovementKind
    movement: MovementCandidate
    source_ref: FractalNodeRef
    output_node: FractalNode
    gate_id: str
    adjudication_gate_id: str
    evidence_ref: str
    residuals: tuple[FractalResidual, ...]
    open_authority_gaps: tuple[FractalAuthorityGap, ...]
    issuance: _IssuanceToken

    def __post_init__(self) -> None:
        if self.issuance is not _TRANSITION_ISSUANCE:
            raise FractalTraceError(
                "الانتقالُ ناتجُ بوّابةٍ لا حقلٌ يكتبه المستدعي؛ و"
                + CANDIDATE_IS_NOT_TRANSITION
            )
        _named_text(self.transition_id, "مُعرِّفُ الانتقال")
        if not isinstance(self.movement_kind, FractalMovementKind):
            raise FractalTraceError("جنسُ الحركة عضوٌ في مفردته المغلقة")
        if not isinstance(self.output_node, FractalNode):
            raise FractalTraceError("مخرجُ الانتقال عقدةٌ من نوعها")

    @property
    def carrier_id(self) -> str:
        """حاملُ الحركة."""

        return self.output_node.carrier_id

    @property
    def identity_before(self) -> FractalIdentity:
        """هويّةُ النسخة قبل الحركة."""

        if isinstance(self.movement, IdentityPreservingTransformationCandidate):
            return self.movement.identity_before
        return self.movement.parent_identity

    @property
    def identity_after(self) -> FractalIdentity:
        """هويّةُ النسخة بعد الحركة."""

        if isinstance(self.movement, IdentityPreservingTransformationCandidate):
            return self.movement.identity_after
        return self.movement.child_identity

    @property
    def preserved_invariants(self) -> tuple[str, ...]:
        """الثوابتُ المحفوظةُ في الحركة كما وافقت عقدَ نمطها."""

        if isinstance(self.movement, IdentityPreservingTransformationCandidate):
            return self.movement.preserved_invariants
        return self.movement.shared_interface

    @property
    def accepted_difference(self) -> DeclaredDifference:
        """الفرقُ المقبولُ في الحركة؛ مُصرَّحٌ ومُطابِقٌ لا مرخَّص."""

        return self.movement.conformant.candidate.declared_difference

    @property
    def pattern_ref(self) -> PatternRef:
        """نمطُ الحركة بمرجع عقده."""

        return self.movement.conformant.pattern_ref

    @property
    def scale_before(self) -> FractalScaleRef:
        """مقياسُ ما قبل الحركة."""

        return self.identity_before.scale_ref

    @property
    def scale_after(self) -> FractalScaleRef:
        """مقياسُ ما بعد الحركة."""

        return self.identity_after.scale_ref

    @property
    def input_content_id(self) -> str:
        """بصمةُ مدخل الحركة."""

        return self.source_ref.content_id

    @property
    def output_content_id(self) -> str:
        """بصمةُ مخرج الحركة."""

        return self.output_node.content_id


@dataclass(frozen=True, slots=True)
class FractalTransitionTraceStep:
    """خطوةُ أثرٍ لانتقالٍ وقع؛ تُسمّي كلَّ ما يلزم لإعادة بنائه."""

    transition: FractalTransition
    issuance: _IssuanceToken

    def __post_init__(self) -> None:
        if self.issuance is not _TRANSITION_ISSUANCE:
            raise FractalTraceError(
                "خطوةُ الأثر تصدر عن بوّابة الانتقال وحدَها؛ و"
                + NO_FRACTAL_TRANSITION_WITHOUT_RECONSTRUCTIBLE_TRACE
            )
        if not isinstance(self.transition, FractalTransition):
            raise FractalTraceError("خطوةُ الأثر فوق انتقالٍ من نوعه")

    @property
    def carrier_id(self) -> str:
        """حاملُ الخطوة."""

        return self.transition.carrier_id

    @property
    def source_ref(self) -> FractalNodeRef:
        """مرجعُ العقدة المصدر."""

        return self.transition.source_ref

    @property
    def identity_before(self) -> FractalIdentity:
        """هويّةُ النسخة قبل."""

        return self.transition.identity_before

    @property
    def identity_after(self) -> FractalIdentity:
        """هويّةُ النسخة بعد."""

        return self.transition.identity_after

    @property
    def preserved_invariants(self) -> tuple[str, ...]:
        """الثوابتُ المحفوظة."""

        return self.transition.preserved_invariants

    @property
    def accepted_difference(self) -> DeclaredDifference:
        """الفرقُ المقبول."""

        return self.transition.accepted_difference

    @property
    def movement_kind(self) -> FractalMovementKind:
        """جنسُ الحركة."""

        return self.transition.movement_kind

    @property
    def pattern_ref(self) -> PatternRef:
        """نمطُ الحركة."""

        return self.transition.pattern_ref

    @property
    def evidence_ref(self) -> str:
        """مرجعُ السلطة أو الدليل الذي جرت عليه الحركة."""

        return self.transition.evidence_ref

    @property
    def gate_id(self) -> str:
        """بوّابةُ الانتقال التي أصدرت الحركة."""

        return self.transition.gate_id

    @property
    def scale_before(self) -> FractalScaleRef:
        """المقياسُ قبل."""

        return self.transition.scale_before

    @property
    def scale_after(self) -> FractalScaleRef:
        """المقياسُ بعد."""

        return self.transition.scale_after

    @property
    def residuals(self) -> tuple[FractalResidual, ...]:
        """بقايا الخطوة مرصودةً من حركتها."""

        return self.transition.residuals

    @property
    def open_authority_gaps(self) -> tuple[FractalAuthorityGap, ...]:
        """فجواتُ السلطة المُعلَنة في مدى هذه الخطوة."""

        return self.transition.open_authority_gaps

    @property
    def input_content_id(self) -> str:
        """بصمةُ المدخل."""

        return self.transition.input_content_id

    @property
    def output_content_id(self) -> str:
        """بصمةُ المخرج."""

        return self.transition.output_content_id


@dataclass(frozen=True, slots=True)
class FractalTransitionDecision:
    """ناتجُ بوّابة الانتقال: الحركةُ، وخطوةُ أثرها، وعقدتُها المخرجة."""

    transition: FractalTransition
    trace_step: FractalTransitionTraceStep

    def __post_init__(self) -> None:
        if self.trace_step.transition is not self.transition:
            raise FractalTraceError("خطوةُ الأثر أثرُ هذا الانتقال بعينه")

    @property
    def output_node(self) -> FractalNode:
        """العقدةُ الناتجةُ عن الحركة."""

        return self.transition.output_node


@dataclass(frozen=True, slots=True)
class FractalTrace:
    """أثرٌ متّصل: مخرجُ خطوةٍ هو مدخلُ التالية بعينه."""

    steps: tuple[FractalTransitionTraceStep, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.steps, tuple) or not self.steps:
            raise FractalTraceError("الأثرُ خطوةٌ واحدةٌ فأكثر")
        previous: FractalTransitionTraceStep | None = None
        for step in self.steps:
            if not isinstance(step, FractalTransitionTraceStep):
                raise FractalTraceError("عضوٌ في الأثر خارج نوع الخطوة")
            if not is_canonical_digest(step.input_content_id):
                raise FractalTraceError("مدخلُ الخطوة بصمةٌ قانونيّة")
            if previous is not None and previous.output_content_id != (
                step.input_content_id
            ):
                raise FractalTraceError(
                    "خطوةٌ تُبنى على مخرجٍ لم تُنتِجه سابقتُها؛ و"
                    + NO_FRACTAL_TRANSITION_WITHOUT_RECONSTRUCTIBLE_TRACE
                )
            previous = step

    @property
    def input_content_id(self) -> str:
        """بصمةُ مدخل أوّل خطوةٍ في الأثر."""

        return self.steps[0].input_content_id

    @property
    def output_content_id(self) -> str:
        """بصمةُ مخرج آخر خطوةٍ في الأثر."""

        return self.steps[-1].output_content_id

    @property
    def residuals(self) -> tuple[FractalResidual, ...]:
        """بقايا الأثر كلُّها مرصودةً من خطواته."""

        return tuple(residual for step in self.steps for residual in step.residuals)


class FractalTransitionGate:
    """البوّابةُ الوحيدةُ التي تُوقِع حركةً فعليّةً وتُصدِر أثرَها."""

    @staticmethod
    def open_transition(
        *,
        adjudication: BranchAdjudicationDecision,
        candidate_id: str,
        source_node: FractalNode,
        transition_id: str,
        gate_id: str,
        evidence_ref: str,
        output_node_id: str,
        output_identity_id: str | None = None,
        residuals: tuple[FractalResidual, ...] = (),
        open_authority_gaps: tuple[FractalAuthorityGap, ...] = (),
    ) -> FractalTransitionDecision:
        """أوقِع الحركةَ على فرعٍ قُبِل في فصلٍ تامّ، وأصدِر أثرَها المتّصل."""

        if not isinstance(adjudication, BranchAdjudicationDecision):
            raise FractalTraceError("الحركةُ لا تقع إلّا بعد قرارِ فصلٍ من نوعه")
        if not isinstance(source_node, FractalNode):
            raise FractalTraceError("مصدرُ الحركة عقدةٌ من نوعها")
        if adjudication.source != source_node.as_ref():
            raise FractalTraceError("قرارُ الفصل ليس فصلَ هذه العقدة ببصمتها")
        assessment = adjudication.assessment_for(
            _named_text(candidate_id, "مُعرِّفُ الفرع المتحرِّك")
        )
        if assessment.standing is not BranchStanding.ADMITTED:
            raise FractalTraceError(
                "لا حركةَ على فرعٍ لم يُقبَل؛ و" + CANDIDATE_IS_NOT_TRANSITION
            )
        movement = assessment.movement
        if movement is None:  # pragma: no cover - حرسٌ لنوعٍ مضمونٍ بحكمه
            raise FractalTraceError("الفرعُ المقبولُ يحمل مرشَّحَ حركته")
        if not isinstance(residuals, tuple) or not isinstance(
            open_authority_gaps, tuple
        ):
            raise FractalTraceError("البقايا والفجواتُ مجموعاتٌ مُصرَّحٌ بها")
        for residual in residuals:
            if not isinstance(residual, FractalResidual):
                raise FractalTraceError("عضوٌ في بقايا الحركة خارج نوعه")
        for gap in open_authority_gaps:
            if not isinstance(gap, FractalAuthorityGap):
                raise FractalTraceError("عضوٌ في فجوات الحركة خارج نوعه")
        if isinstance(movement, IdentityPreservingTransformationCandidate):
            kind = FractalMovementKind.IDENTITY_PRESERVING_TRANSFORMATION
            identity_after = movement.identity_after
        elif isinstance(movement, BranchBirthCandidate):
            kind = FractalMovementKind.BRANCH_BIRTH
            identity_after = movement.child_identity
        else:  # pragma: no cover - حرسٌ لمفردةٍ مغلقة
            raise FractalTraceError("جنسُ الحركة خارج المفردة المغلقة")
        if identity_after.scale_ref != source_node.identity.scale_ref:
            raise FractalTraceError(
                "الحركةُ الفعليّةُ أفقيّةٌ في هذه المرحلة؛ و"
                + NO_HIGHER_SCALE_WITHOUT_NECESSITY
            )
        if output_identity_id is not None:
            _named_text(output_identity_id, "مُعرِّفُ هويّة المخرج")
            if output_identity_id != identity_after.identity_id:
                raise FractalTraceError("هويّةُ المخرج هويّةُ الحركة بعدُ بعينها")
        output_node = FractalNode(
            node_id=_named_text(output_node_id, "مُعرِّفُ العقدة المخرجة"),
            identity=identity_after,
            carrier_id=source_node.carrier_id,
            content=movement.output_content,
            origin_id=source_node.content_id,
        )
        transition = FractalTransition(
            transition_id=_named_text(transition_id, "مُعرِّفُ الانتقال"),
            movement_kind=kind,
            movement=movement,
            source_ref=source_node.as_ref(),
            output_node=output_node,
            gate_id=_named_text(gate_id, "مُعرِّفُ بوّابة الانتقال"),
            adjudication_gate_id=adjudication.gate_id,
            evidence_ref=_named_text(evidence_ref, "مرجعُ السلطة أو الدليل"),
            residuals=residuals,
            open_authority_gaps=open_authority_gaps,
            issuance=_TRANSITION_ISSUANCE,
        )
        return FractalTransitionDecision(
            transition=transition,
            trace_step=FractalTransitionTraceStep(
                transition=transition, issuance=_TRANSITION_ISSUANCE
            ),
        )
