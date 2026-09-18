"""`G0.SDAL-0.RESIDUAL`: تصنيفُ البقايا حاجبةً وغيرَ حاجبة، وأثرُه في الترقية.

البقيّةُ ليست مصرِفًا يبتلع كلَّ ما لم يُحسَم؛ ولو كانت كذلك لنجح كلُّ اختبار.
فمنذ `zero-one` تُصنَّف كلُّ بقيّةٍ، ويجري عليها:

    BlockingResidual  ->  NoPositivePromotion

فقد تُعيد البنيةُ بناءَ نفسها تمامًا ومع ذلك يُمنَع رفعُها إلى رتبةٍ أعلى.
والتصنيفُ مقروءٌ من `FractalResidual.blocking` القائم، لا حقلٌ مُوازٍ يُكتَب
ثانيةً فيناقضه.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum

from alghanem.fractal_generation import FractalResidual, FractalResidualKind

from .laws import BLOCKING_RESIDUAL_FORBIDS_POSITIVE_PROMOTION, StructuralDalError

__all__ = [
    "PromotionStanding",
    "ResidualClass",
    "ResidualReading",
    "promotion_standing_of",
    "read_residuals",
    "unassigned_role_basis_residual",
    "uncovered_core_residual",
]


class ResidualClass(Enum):
    """صنفا البقيّة؛ مفردةٌ مغلقةٌ لا صفةٌ حرّة."""

    NON_BLOCKING = "non_blocking"
    BLOCKING = "blocking"


class PromotionStanding(Enum):
    """موقفُ الترقية؛ مُشتَقٌّ من البقايا لا مُصرَّحٌ من خارجها."""

    PROMOTION_PERMITTED = "promotion_permitted"
    PROMOTION_BLOCKED = "promotion_blocked"


@dataclass(frozen=True, slots=True)
class ResidualReading:
    """قراءةُ بقيّةٍ مرصودة: عينُها، وصنفُها مُشتَقًّا من حجبها."""

    residual: FractalResidual

    def __post_init__(self) -> None:
        if not isinstance(self.residual, FractalResidual):
            raise StructuralDalError("قراءةُ البقيّة تقع على بقيّةٍ من نوعها")

    @property
    def residual_class(self) -> ResidualClass:
        """صنفُ البقيّة؛ مقروءٌ من حجبها لا مكتوبٌ بجانبها."""

        return (
            ResidualClass.BLOCKING
            if self.residual.blocking
            else ResidualClass.NON_BLOCKING
        )

    @property
    def subject_id(self) -> str:
        """حاملُ البقيّة."""

        return self.residual.subject_id

    @property
    def reason(self) -> str:
        """سببُ البقيّة مُسمًّى."""

        return self.residual.reason

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى القراءة للعرض والبصمة."""

        return {
            "kind": self.residual.kind.value,
            "subject_id": self.subject_id,
            "reason": self.reason,
            "residual_class": self.residual_class.value,
        }


def read_residuals(
    residuals: Iterable[FractalResidual],
) -> tuple[ResidualReading, ...]:
    """اقرأ بقايا بأعيانها مُصنَّفةً؛ ولا تُسقِط منها شيئًا."""

    return tuple(ResidualReading(residual=residual) for residual in residuals)


def promotion_standing_of(
    readings: Iterable[ResidualReading],
) -> PromotionStanding:
    """موقفُ الترقية: تُمنَع متى وُجدت بقيّةٌ حاجبةٌ واحدةٌ فأكثر."""

    for reading in readings:
        if reading.residual_class is ResidualClass.BLOCKING:
            return PromotionStanding.PROMOTION_BLOCKED
    return PromotionStanding.PROMOTION_PERMITTED


def uncovered_core_residual(subject_id: str) -> FractalResidual:
    """بقيّةٌ حاجبة: تقسيمٌ بلا خانةٍ أساسيّةٍ لا يُرقّى وإن أعاد بناءَ الكلّ."""

    return FractalResidual(
        kind=FractalResidualKind.UNCOVERED_MINIMUM_REQUIREMENT,
        subject_id=subject_id,
        reason=(
            "تقسيمٌ لا يُسنِد إلى أيّ خانةٍ دورَ الأساس؛ و"
            + BLOCKING_RESIDUAL_FORBIDS_POSITIVE_PROMOTION
        ),
        blocking=True,
    )


def unassigned_role_basis_residual(subject_id: str) -> FractalResidual:
    """بقيّةٌ غيرُ حاجبة: أساسُ إسناد الأدوار غيرُ مُبرهنٍ عند هذا المقياس."""

    return FractalResidual(
        kind=FractalResidualKind.UNRESOLVED_DIFFERENCE,
        subject_id=subject_id,
        reason=(
            "الدورُ مُصرَّحٌ لا مُستنبَط: لا مُرجِّحَ عند هذا المقياس يُبيِّن لماذا "
            "أخذت هذه الخانةُ دورَها دون غيره"
        ),
        blocking=False,
    )
