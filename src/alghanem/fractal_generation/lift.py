"""الرفعُ إلى مقياسٍ أعلى: مُعرَّفٌ بالأنواع، ومؤجَّلٌ بالسلطة في هذه المرحلة.

    Closed ∧ AuthoredNecessityClaim  ⇏  Lift

**ودعوى الضرورة ليست شهادتَها**: `ScaleExhaustionCandidate` دعوى يكتبها
صاحبُها، و`ScaleNecessityCertificate` سلطةٌ لا مصنعَ لها في `G0.FGEN-0`: لا
بوّابةَ تُصدِرها، ولا تقبل `LiftGate.assess` دليلًا حرًّا من المستدعي.

**والحالُ الوحيدةُ المتاحةُ اليوم**:

    DEFERRED_NO_SCALE_NECESSITY_AUTHORITY

**وهذا حالُ مرحلةٍ لا حكمُ أبد** (`NotIssuedAtThisStage ≠ MustNeverExist`):
فجوةُ `RES.FGEN0.NoScaleNecessityAuthority` تحمل شرطَ رفعها، ومرحلةٌ مستقلّةٌ
لاحقةٌ تفتح السلطةَ فتصير الشهادةُ ممكنةً ويصير الرفعُ ممكنًا معها.

    ClosedFractalNode  ⇏  NextScaleSeed      (في هذه المرحلة)

تسجيلٌ لا سلطة: لا ولادةَ، ولا حكمَ ولادةٍ، ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .authority_gaps import NO_SCALE_NECESSITY_AUTHORITY, FractalAuthorityGap
from .closure import ClosedFractalNode
from .laws import (
    CLOSED_WITH_AUTHORED_NECESSITY_CLAIM_DOES_NOT_ENTAIL_LIFT,
    NO_HIGHER_SCALE_WITHOUT_NECESSITY,
)
from .node import FractalResidual, FractalSeed
from .scale import FractalScaleRef

__all__ = [
    "LiftCandidate",
    "LiftDecision",
    "LiftError",
    "LiftGate",
    "LiftStatus",
    "NextScaleSeed",
    "ScaleExhaustionCandidate",
    "ScaleNecessityCertificate",
    "ScaleTransitionRequirement",
]


class LiftError(ValueError):
    """رفضٌ عند تكوين متطلَّبِ رفعٍ أو دعوى استنفادٍ أو مرشَّحِ رفع."""


class _IssuanceToken:
    """رمزُ إصدارٍ داخليّ؛ ولا يملكه في هذه المرحلة مُصدِرٌ ألبتّة."""

    __slots__ = ()


def _named_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise LiftError(f"{label} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class ScaleTransitionRequirement:
    """شرطُ الانتقال إلى مقياسٍ أعلى: من أيِّ مقياسٍ إلى أيّ، وبأيِّ دعوى ضرورة."""

    from_scale_ref: FractalScaleRef
    to_scale_ref: FractalScaleRef
    necessity_claim: str

    def __post_init__(self) -> None:
        for ref, label in (
            (self.from_scale_ref, "المقياسُ الأدنى"),
            (self.to_scale_ref, "المقياسُ الأعلى"),
        ):
            if not isinstance(ref, FractalScaleRef):
                raise LiftError(f"{label} مرجعٌ من نوعه")
        if self.from_scale_ref == self.to_scale_ref:
            raise LiftError("لا رفعَ من مقياسٍ إلى نفسه")
        _named_text(self.necessity_claim, "دعوى الضرورة")


@dataclass(frozen=True, slots=True)
class ScaleExhaustionCandidate:
    """دعوى استنفادِ مقياس: يكتبها صاحبُها، ولا تُثبِت نفسَها."""

    closed_node: ClosedFractalNode
    claim: str
    irreducible_residuals: tuple[FractalResidual, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.closed_node, ClosedFractalNode):
            raise LiftError("دعوى الاستنفاد فوق عقدةٍ مغلقةٍ صادرةٍ عن بوّابتها")
        _named_text(self.claim, "نصُّ دعوى الاستنفاد")
        if not isinstance(self.irreducible_residuals, tuple):
            raise LiftError("البقايا غيرُ القابلة للردّ مجموعةٌ مُصرَّحٌ بها")
        for residual in self.irreducible_residuals:
            if not isinstance(residual, FractalResidual):
                raise LiftError("عضوٌ في بقايا الدعوى خارج نوعه")


@dataclass(frozen=True, slots=True)
class ScaleNecessityCertificate:
    """شهادةُ ضرورةِ مقياسٍ أعلى: سلطةٌ لا مُصدِرَ لها في هذه المرحلة."""

    requirement: ScaleTransitionRequirement
    exhaustion: ScaleExhaustionCandidate
    issuance: _IssuanceToken

    def __post_init__(self) -> None:
        raise LiftError(
            "لا سلطةَ في `G0.FGEN-0` تُصدِر شهادةَ ضرورةِ مقياس؛ و"
            + NO_HIGHER_SCALE_WITHOUT_NECESSITY
        )


@dataclass(frozen=True, slots=True)
class LiftCandidate:
    """مرشَّحُ رفع: عقدةٌ مغلقةٌ، ودعوى استنفاد، وشرطُ انتقالٍ مُسمًّى."""

    closed_node: ClosedFractalNode
    exhaustion: ScaleExhaustionCandidate
    requirement: ScaleTransitionRequirement

    def __post_init__(self) -> None:
        if not isinstance(self.closed_node, ClosedFractalNode):
            raise LiftError("مرشَّحُ الرفع فوق عقدةٍ مغلقةٍ من نوعها")
        if not isinstance(self.exhaustion, ScaleExhaustionCandidate):
            raise LiftError("مرشَّحُ الرفع يحمل دعوى استنفادٍ من نوعها")
        if self.exhaustion.closed_node is not self.closed_node:
            raise LiftError("دعوى الاستنفاد دعوى هذه العقدة بعينها")
        if not isinstance(self.requirement, ScaleTransitionRequirement):
            raise LiftError("مرشَّحُ الرفع يحمل شرطَ انتقالٍ من نوعه")
        if self.requirement.from_scale_ref != self.closed_node.scale_ref:
            raise LiftError("شرطُ الانتقال ينطلق من مقياس هذه العقدة بعينه")


@dataclass(frozen=True, slots=True)
class NextScaleSeed:
    """بذرةُ المقياس التالي: لا تُبنى إلّا بشهادةِ ضرورةٍ لا مُصدِرَ لها اليوم."""

    certificate: ScaleNecessityCertificate
    seed: FractalSeed

    def __post_init__(self) -> None:
        if not isinstance(self.certificate, ScaleNecessityCertificate):
            raise LiftError(
                "بذرةُ المقياس التالي تلزمها شهادةُ ضرورة؛ و"
                + NO_HIGHER_SCALE_WITHOUT_NECESSITY
            )
        if not isinstance(self.seed, FractalSeed):
            raise LiftError("بذرةُ المقياس التالي بذرةٌ من نوعها")


class LiftStatus(Enum):
    """حالُ بوّابة الرفع في هذه المرحلة؛ واحدةٌ لا غير."""

    DEFERRED_NO_SCALE_NECESSITY_AUTHORITY = "deferred_no_scale_necessity_authority"


@dataclass(frozen=True, slots=True)
class LiftDecision:
    """قرارُ بوّابة الرفع: حالُه، وسببُه، والفجوةُ المانعةُ مُسمّاة."""

    status: LiftStatus
    reason: str
    blocking_gap: FractalAuthorityGap
    next_scale_seed: None = None

    def __post_init__(self) -> None:
        if not isinstance(self.status, LiftStatus):
            raise LiftError("حالُ قرار الرفع عضوٌ في مفردته المغلقة")
        _named_text(self.reason, "سببُ قرار الرفع")
        if not isinstance(self.blocking_gap, FractalAuthorityGap):
            raise LiftError("قرارُ الرفع يُسمّي فجوتَه المانعة")
        if self.next_scale_seed is not None:
            raise LiftError(
                "لا بذرةَ مقياسٍ تاليةً في هذه المرحلة؛ و"
                + CLOSED_WITH_AUTHORED_NECESSITY_CLAIM_DOES_NOT_ENTAIL_LIFT
            )


class LiftGate:
    """بوّابةُ الرفع: تقرأ العقدةَ المغلقةَ وحدَها، ولا تقبل دليلًا حرًّا من المستدعي."""

    @staticmethod
    def assess(*, candidate: LiftCandidate) -> LiftDecision:
        """اقرأ مرشَّحَ الرفع؛ وحالُ هذه المرحلة تأجيلٌ لغياب سلطة الضرورة."""

        if not isinstance(candidate, LiftCandidate):
            raise LiftError("المقيسُ مرشَّحُ رفعٍ من نوعه")
        return LiftDecision(
            status=LiftStatus.DEFERRED_NO_SCALE_NECESSITY_AUTHORITY,
            reason=(
                "العقدةُ مغلقةٌ عند مقياسها، ودعوى الاستنفاد مكتوبةٌ بيد صاحبها، "
                "ولا شهادةَ ضرورةٍ تُصدَر في هذه المرحلة؛ و"
                + CLOSED_WITH_AUTHORED_NECESSITY_CLAIM_DOES_NOT_ENTAIL_LIFT
            ),
            blocking_gap=NO_SCALE_NECESSITY_AUTHORITY,
        )
