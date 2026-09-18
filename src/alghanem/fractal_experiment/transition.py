"""الانتقالُ التجريبيُّ: تسجيلٌ موازٍ فوق انتقالٍ فراكتاليٍّ وقع، بلا أيّ رتبة.

    ExperimentalRunPermit  +  FractalTransition  →  ExperimentalFractalTransition

**ولا تُعدَّل النواة**: `FractalTransition` تبقى كما هي، وهذا غلافٌ مستقلٌّ
يربطها بإذنها وبمدخلها المُجمَّد وبأثرها وبقاياها وفجوات سلطتها.

**ولا رتبةَ هنا** (`ExperimentalTransition ≠ LicensedTransition`): لا حقلَ
ترخيصٍ ولا رتبةَ ولا حكم؛ وواقعةُ التشغيل لا تصير إذنًا لما بعدها.

تسجيلٌ لا سلطة: لا ترخيصَ، ولا رتبةَ دائمة، ولا حكمَ كفاية.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from ..fractal_generation import (
    FractalIdentity,
    FractalMovementKind,
    FractalResidual,
    FractalScaleRef,
    FractalTrace,
    FractalTransition,
    PatternRef,
)
from .authority import (
    ExperimentalFractalAuthority,
    ExperimentalRunPermit,
)
from .authority_gaps import ExperimentalAuthorityGap
from .binding import FrozenExperimentBinding, FrozenInputEntry
from .laws import (
    EXPERIMENTAL_PERMISSION_IS_NOT_LICENSE,
    EXPERIMENTAL_TRANSITION_IS_NOT_LICENSED_TRANSITION,
)

__all__ = [
    "ExperimentalFractalTransition",
    "ExperimentalTransitionError",
    "ExperimentalTransitionGate",
]


class ExperimentalTransitionError(ValueError):
    """رفضٌ عند تسجيل انتقالٍ تجريبيٍّ خارج مدى إذنه أو بلا أثرٍ متّصل."""


class _IssuanceToken:
    """رمزُ إصدارٍ داخليّ؛ وجودُه بيد البوّابة وحدَها لا بيد المستدعي."""

    __slots__ = ()


_EXPERIMENTAL_TRANSITION_ISSUANCE: Final[_IssuanceToken] = _IssuanceToken()


def _named_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ExperimentalTransitionError(f"{label} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class ExperimentalFractalTransition:
    """انتقالٌ فراكتاليٌّ جرى تجريبًا: إذنُه، ومدخلُه المُجمَّد، وأثرُه، وبقاياه."""

    experiment_id: str
    run_id: str
    permit_content_id: str
    frozen_input_id: str
    frozen_input_content_id: str
    operation: str
    transition: FractalTransition
    trace: FractalTrace
    residuals: tuple[FractalResidual, ...]
    open_authority_gaps: tuple[ExperimentalAuthorityGap, ...]
    issuance: _IssuanceToken

    def __post_init__(self) -> None:
        if self.issuance is not _EXPERIMENTAL_TRANSITION_ISSUANCE:
            raise ExperimentalTransitionError(
                "الانتقالُ التجريبيُّ ناتجُ بوّابةٍ لا حقلٌ يكتبه المستدعي؛ و"
                + EXPERIMENTAL_TRANSITION_IS_NOT_LICENSED_TRANSITION
            )
        if not isinstance(self.transition, FractalTransition):
            raise ExperimentalTransitionError("الملفوفُ انتقالٌ فراكتاليٌّ من نوعه")
        if not isinstance(self.trace, FractalTrace):
            raise ExperimentalTransitionError("الانتقالُ التجريبيُّ يحمل أثرًا متّصلًا")

    @property
    def movement_kind(self) -> FractalMovementKind:
        """جنسُ الحركة كما وقعت في النواة."""

        return self.transition.movement_kind

    @property
    def identity_before(self) -> FractalIdentity:
        """هويّةُ النسخة قبل الحركة."""

        return self.transition.identity_before

    @property
    def identity_after(self) -> FractalIdentity:
        """هويّةُ النسخة بعد الحركة."""

        return self.transition.identity_after

    @property
    def pattern_ref(self) -> PatternRef:
        """نمطُ الحركة بمرجع عقده."""

        return self.transition.pattern_ref

    @property
    def scale_before(self) -> FractalScaleRef:
        """مقياسُ ما قبل الحركة."""

        return self.transition.scale_before

    @property
    def scale_after(self) -> FractalScaleRef:
        """مقياسُ ما بعد الحركة."""

        return self.transition.scale_after

    @property
    def observed_output_content_id(self) -> str:
        """بصمةُ المخرج المرصود."""

        return self.transition.output_content_id

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الانتقال التجريبيِّ للبصمة."""

        return {
            "experiment_id": self.experiment_id,
            "run_id": self.run_id,
            "permit_content_id": self.permit_content_id,
            "frozen_input_id": self.frozen_input_id,
            "frozen_input_content_id": self.frozen_input_content_id,
            "operation": self.operation,
            "transition_id": self.transition.transition_id,
            "input_content_id": self.transition.input_content_id,
            "output_content_id": self.transition.output_content_id,
            "movement_kind": self.transition.movement_kind.value,
            "residuals": [
                residual.as_canonical_content() for residual in self.residuals
            ],
            "open_authority_gaps": [
                gap.as_canonical_content() for gap in self.open_authority_gaps
            ],
        }

    @property
    def content_id(self) -> str:
        """بصمةُ الانتقال التجريبيّ؛ مُشتَقّةٌ لا مكتوبة."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


class ExperimentalTransitionGate:
    """البوّابةُ الوحيدةُ التي تُسجِّل انتقالًا تجريبيًّا داخلَ مدى إذنٍ نشط."""

    @staticmethod
    def record(
        *,
        authority: ExperimentalFractalAuthority,
        permit: ExperimentalRunPermit,
        run_id: str,
        binding: FrozenExperimentBinding,
        frozen_input: FrozenInputEntry,
        operation: str,
        transition: FractalTransition,
        trace: FractalTrace,
        residuals: tuple[FractalResidual, ...] = (),
        open_authority_gaps: tuple[ExperimentalAuthorityGap, ...] = (),
    ) -> ExperimentalFractalTransition:
        """سجِّل انتقالًا وقع في النواة شاهدًا تجريبيًّا داخلَ مدى إذنه."""

        if not isinstance(authority, ExperimentalFractalAuthority):
            raise ExperimentalTransitionError("السلطةُ التجريبيّةُ من نوعها")
        active = authority.require_active_for_run(permit, run_id=run_id)
        if not isinstance(binding, FrozenExperimentBinding):
            raise ExperimentalTransitionError("رباطُ التجميد من نوعه")
        if binding.content_id != active.binding_content_id:
            raise ExperimentalTransitionError(
                "رباطُ تجميدٍ غيرُ الذي صدر عليه الإذن؛ و"
                + EXPERIMENTAL_PERMISSION_IS_NOT_LICENSE
            )
        if not isinstance(frozen_input, FrozenInputEntry):
            raise ExperimentalTransitionError("المدخلُ المُجمَّدُ مدخلةٌ من نوعها")
        if binding.entry_for(frozen_input.input_id) != frozen_input:
            raise ExperimentalTransitionError("مدخلةٌ مُجمَّدةٌ ليست مدخلةَ هذا الرباط")
        if not isinstance(transition, FractalTransition):
            raise ExperimentalTransitionError("المُسجَّلُ انتقالٌ فراكتاليٌّ من نوعه")
        if not isinstance(trace, FractalTrace):
            raise ExperimentalTransitionError("الأثرُ متّصلٌ من نوعه")
        if trace.output_content_id != transition.output_content_id:
            raise ExperimentalTransitionError("الأثرُ لا ينتهي إلى مخرج هذا الانتقال")
        checked_operation = _named_text(operation, "اسمُ العمليّة")
        if not active.permits_operation(checked_operation):
            raise ExperimentalTransitionError("عمليّةٌ خارج مدى الإذن التجريبيّ")
        if not active.permits_pattern(transition.pattern_ref):
            raise ExperimentalTransitionError("نمطٌ خارج مدى الإذن التجريبيّ")
        if not active.permits_source_scale(transition.scale_before):
            raise ExperimentalTransitionError("مقياسُ مصدرٍ خارج مدى الإذن التجريبيّ")
        if not active.permits_target_scale(transition.scale_after):
            raise ExperimentalTransitionError("مقياسُ هدفٍ خارج مدى الإذن التجريبيّ")
        if (
            transition.movement_kind is FractalMovementKind.BRANCH_BIRTH
            and not active.permitted_branch_birth
        ):
            raise ExperimentalTransitionError("ولادةُ فرعٍ غيرُ مأذونٍ فيها في هذا الإذن")
        if not isinstance(residuals, tuple):
            raise ExperimentalTransitionError("البقايا مجموعةٌ مُصرَّحٌ بها")
        for residual in residuals:
            if not isinstance(residual, FractalResidual):
                raise ExperimentalTransitionError("عضوٌ في البقايا خارج نوعه")
        if not isinstance(open_authority_gaps, tuple):
            raise ExperimentalTransitionError("فجواتُ السلطة مجموعةٌ مُصرَّحٌ بها")
        for gap in open_authority_gaps:
            if not isinstance(gap, ExperimentalAuthorityGap):
                raise ExperimentalTransitionError("عضوٌ في فجوات السلطة خارج نوعه")
        return ExperimentalFractalTransition(
            experiment_id=active.experiment_id,
            run_id=active.run_id,
            permit_content_id=active.content_id,
            frozen_input_id=frozen_input.input_id,
            frozen_input_content_id=frozen_input.content_id,
            operation=checked_operation,
            transition=transition,
            trace=trace,
            residuals=residuals + transition.residuals,
            open_authority_gaps=open_authority_gaps,
            issuance=_EXPERIMENTAL_TRANSITION_ISSUANCE,
        )
