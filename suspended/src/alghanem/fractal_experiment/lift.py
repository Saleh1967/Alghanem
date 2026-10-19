"""الرفعُ التجريبيُّ: مسارٌ موازٍ يختبر ضرورةَ المقياس ولا يشهد بها.

    ClosedFractalNode  +  ExperimentalLiftPermit
        →  ExperimentalLiftCandidate
        →  ExperimentalLiftGate
        →  ExperimentalNextScaleSeed

**والناتجُ ليس بذرةَ المقياس الدائمة** (`ExperimentalNextScaleSeed ≠
NextScaleSeed`): لا وراثةَ بينهما، ولا تحويلَ من الأولى إلى الثانية، ولا مدخلَ
لها إلى النواة؛ وسلطتُها تنتهي بانتهاء تشغيلها.

**وضرورةُ المقياس ليست شرطَ الدخول** (`ExperimentalLiftTestsNecessity;
ItDoesNotCertifyNecessity`): إثباتُها موضوعُ التجربة، و
`ScaleNecessityCertificate` في النواة تبقى مغلقةً كما هي.

تسجيلٌ لا سلطة: لا ترخيصَ، ولا رتبةَ دائمة، ولا حكمَ كفاية.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest, is_canonical_digest
from ..fractal_generation import (
    ClosedFractalNode,
    FractalResidual,
    FractalScaleRef,
)
from .authority import (
    ExperimentalFractalAuthority,
    ExperimentalRunPermit,
)
from .authority_gaps import (
    NO_SCALE_NECESSITY_CERTIFICATION_IN_EXPERIMENT,
    ExperimentalAuthorityGap,
)
from .laws import (
    EXPERIMENTAL_LIFT_TESTS_NECESSITY_IT_DOES_NOT_CERTIFY_NECESSITY,
    EXPERIMENTAL_NEXT_SCALE_SEED_IS_NOT_NEXT_SCALE_SEED,
)

__all__ = [
    "ExperimentalLiftCandidate",
    "ExperimentalLiftDecision",
    "ExperimentalLiftError",
    "ExperimentalLiftGate",
    "ExperimentalLiftPermit",
    "ExperimentalLiftStatus",
    "ExperimentalNextScaleSeed",
    "issue_experimental_lift_permit",
]


class ExperimentalLiftError(ValueError):
    """رفضٌ عند إصدار إذن رفعٍ تجريبيٍّ أو بناء مرشَّحه أو بذرته."""


class _IssuanceToken:
    """رمزُ إصدارٍ داخليّ؛ وجودُه بيد بوّابته وحدَها لا بيد المستدعي."""

    __slots__ = ()


_LIFT_PERMIT_ISSUANCE: Final[_IssuanceToken] = _IssuanceToken()
_EXPERIMENTAL_SEED_ISSUANCE: Final[_IssuanceToken] = _IssuanceToken()


def _named_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ExperimentalLiftError(f"{label} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class ExperimentalLiftPermit:
    """إذنُ رفعٍ تجريبيٍّ: من مقياسٍ إلى مقياسٍ، بدعوى ضرورةٍ **تحت الاختبار**."""

    run_permit_content_id: str
    run_id: str
    experiment_id: str
    source_scale_ref: FractalScaleRef
    target_scale_ref: FractalScaleRef
    necessity_claim_under_test: str
    issuance: _IssuanceToken

    def __post_init__(self) -> None:
        if self.issuance is not _LIFT_PERMIT_ISSUANCE:
            raise ExperimentalLiftError(
                "إذنُ الرفع التجريبيِّ ناتجُ سلطةٍ لا حقلٌ يكتبه المستدعي؛ و"
                + EXPERIMENTAL_LIFT_TESTS_NECESSITY_IT_DOES_NOT_CERTIFY_NECESSITY
            )
        if not is_canonical_digest(self.run_permit_content_id):
            raise ExperimentalLiftError("بصمةُ إذن التشغيل قانونيّة")
        _named_text(self.run_id, "مُعرِّفُ التشغيل")
        _named_text(self.experiment_id, "مُعرِّفُ التجربة")
        for ref, label in (
            (self.source_scale_ref, "مقياسُ المصدر"),
            (self.target_scale_ref, "مقياسُ الهدف"),
        ):
            if not isinstance(ref, FractalScaleRef):
                raise ExperimentalLiftError(f"{label} مرجعٌ من نوعه")
        if self.source_scale_ref == self.target_scale_ref:
            raise ExperimentalLiftError("لا رفعَ من مقياسٍ إلى نفسه")
        _named_text(self.necessity_claim_under_test, "دعوى الضرورة تحت الاختبار")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى إذن الرفع للبصمة."""

        return {
            "run_permit_content_id": self.run_permit_content_id,
            "run_id": self.run_id,
            "experiment_id": self.experiment_id,
            "source_scale_id": self.source_scale_ref.scale_id,
            "target_scale_id": self.target_scale_ref.scale_id,
            "necessity_claim_under_test": self.necessity_claim_under_test,
        }

    @property
    def content_id(self) -> str:
        """بصمةُ إذن الرفع؛ مُشتَقّةٌ لا مكتوبة."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


def issue_experimental_lift_permit(
    *,
    authority: ExperimentalFractalAuthority,
    permit: ExperimentalRunPermit,
    run_id: str,
    source_scale_ref: FractalScaleRef,
    target_scale_ref: FractalScaleRef,
    necessity_claim_under_test: str,
) -> ExperimentalLiftPermit:
    """أصدِر إذنَ رفعٍ تجريبيًّا داخلَ مدى إذنِ تشغيلٍ نشطٍ يسمح بالرفع."""

    if not isinstance(authority, ExperimentalFractalAuthority):
        raise ExperimentalLiftError("السلطةُ التجريبيّةُ من نوعها")
    active = authority.require_active_for_run(permit, run_id=run_id)
    if not active.permitted_experimental_lift:
        raise ExperimentalLiftError("الرفعُ التجريبيُّ غيرُ مأذونٍ فيه في هذا الإذن")
    if not active.permits_source_scale(source_scale_ref):
        raise ExperimentalLiftError("مقياسُ المصدر خارج مدى الإذن التجريبيّ")
    if not active.permits_target_scale(target_scale_ref):
        raise ExperimentalLiftError("مقياسُ الهدف خارج مدى الإذن التجريبيّ")
    return ExperimentalLiftPermit(
        run_permit_content_id=active.content_id,
        run_id=active.run_id,
        experiment_id=active.experiment_id,
        source_scale_ref=source_scale_ref,
        target_scale_ref=target_scale_ref,
        necessity_claim_under_test=_named_text(
            necessity_claim_under_test, "دعوى الضرورة تحت الاختبار"
        ),
        issuance=_LIFT_PERMIT_ISSUANCE,
    )


@dataclass(frozen=True, slots=True)
class ExperimentalLiftCandidate:
    """مرشَّحُ رفعٍ تجريبيّ: عقدةٌ مغلقةٌ، وإذنُ رفعٍ، وبقايا محفوظةٌ بلا محو."""

    closed_node: ClosedFractalNode
    lift_permit: ExperimentalLiftPermit
    carried_residuals: tuple[FractalResidual, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.closed_node, ClosedFractalNode):
            raise ExperimentalLiftError(
                "الرفعُ التجريبيُّ فوق عقدةٍ مغلقةٍ صادرةٍ عن بوّابة النواة"
            )
        if not isinstance(self.lift_permit, ExperimentalLiftPermit):
            raise ExperimentalLiftError("مرشَّحُ الرفع يحمل إذنَ رفعٍ من نوعه")
        if not isinstance(self.carried_residuals, tuple):
            raise ExperimentalLiftError("البقايا المحمولةُ مجموعةٌ مُصرَّحٌ بها")
        for residual in self.carried_residuals:
            if not isinstance(residual, FractalResidual):
                raise ExperimentalLiftError("عضوٌ في البقايا المحمولة خارج نوعه")


@dataclass(frozen=True, slots=True)
class ExperimentalNextScaleSeed:
    """بذرةُ مقياسٍ **تجريبيّة**: أثرُ سلطتها ينتهي بتشغيلها، ولا تُحوَّل إلى الدائمة."""

    seed_id: str
    experiment_id: str
    run_id: str
    lift_permit_content_id: str
    source_scale_ref: FractalScaleRef
    target_scale_ref: FractalScaleRef
    closed_node_content_id: str
    necessity_claim_under_test: str
    carried_residuals: tuple[FractalResidual, ...]
    issuance: _IssuanceToken

    def __post_init__(self) -> None:
        if self.issuance is not _EXPERIMENTAL_SEED_ISSUANCE:
            raise ExperimentalLiftError(
                "البذرةُ التجريبيّةُ ناتجُ بوّابةٍ لا حقلٌ يكتبه المستدعي؛ و"
                + EXPERIMENTAL_NEXT_SCALE_SEED_IS_NOT_NEXT_SCALE_SEED
            )
        _named_text(self.seed_id, "مُعرِّفُ البذرة التجريبيّة")
        _named_text(self.experiment_id, "مُعرِّفُ التجربة")
        _named_text(self.run_id, "مُعرِّفُ التشغيل")
        if not is_canonical_digest(self.lift_permit_content_id):
            raise ExperimentalLiftError("بصمةُ إذن الرفع قانونيّة")
        if not is_canonical_digest(self.closed_node_content_id):
            raise ExperimentalLiftError("بصمةُ العقدة المغلقة قانونيّة")
        _named_text(self.necessity_claim_under_test, "دعوى الضرورة تحت الاختبار")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى البذرة التجريبيّة للبصمة."""

        return {
            "seed_id": self.seed_id,
            "experiment_id": self.experiment_id,
            "run_id": self.run_id,
            "lift_permit_content_id": self.lift_permit_content_id,
            "source_scale_id": self.source_scale_ref.scale_id,
            "target_scale_id": self.target_scale_ref.scale_id,
            "closed_node_content_id": self.closed_node_content_id,
            "necessity_claim_under_test": self.necessity_claim_under_test,
            "carried_residuals": [
                residual.as_canonical_content() for residual in self.carried_residuals
            ],
        }

    @property
    def content_id(self) -> str:
        """بصمةُ البذرة التجريبيّة؛ مُشتَقّةٌ لا مكتوبة."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


class ExperimentalLiftStatus(Enum):
    """حالُ بوّابة الرفع التجريبيّ؛ مفردةٌ مغلقة."""

    EXPERIMENTAL_SEED_ISSUED = "experimental_seed_issued"
    REFUSED_OUT_OF_SCOPE = "refused_out_of_scope"


@dataclass(frozen=True, slots=True)
class ExperimentalLiftDecision:
    """قرارُ الرفع التجريبيّ: حالُه، وسببُه، وبذرتُه إن صدرت، وفجوتُه المُسمّاة."""

    status: ExperimentalLiftStatus
    reason: str
    experimental_seed: ExperimentalNextScaleSeed | None
    open_authority_gap: ExperimentalAuthorityGap

    def __post_init__(self) -> None:
        if not isinstance(self.status, ExperimentalLiftStatus):
            raise ExperimentalLiftError("حالُ القرار عضوٌ في مفردته المغلقة")
        _named_text(self.reason, "سببُ قرار الرفع التجريبيّ")
        if not isinstance(self.open_authority_gap, ExperimentalAuthorityGap):
            raise ExperimentalLiftError("قرارُ الرفع يُسمّي فجوتَه القائمة")
        if self.status is ExperimentalLiftStatus.EXPERIMENTAL_SEED_ISSUED:
            if not isinstance(self.experimental_seed, ExperimentalNextScaleSeed):
                raise ExperimentalLiftError("قرارُ الإصدار يحمل بذرتَه التجريبيّة")
        elif self.experimental_seed is not None:
            raise ExperimentalLiftError("قرارُ الرفض لا يحمل بذرةً")


class ExperimentalLiftGate:
    """البوّابةُ الوحيدةُ التي تُصدِر بذرةً تجريبيّة؛ ولا تشهد بضرورةِ مقياس."""

    @staticmethod
    def assess(
        *,
        authority: ExperimentalFractalAuthority,
        permit: ExperimentalRunPermit,
        run_id: str,
        candidate: ExperimentalLiftCandidate,
        seed_id: str,
    ) -> ExperimentalLiftDecision:
        """اقرأ مرشَّحَ الرفع التجريبيّ؛ ولا تقرأ منه ضرورةً مُثبَتة."""

        if not isinstance(authority, ExperimentalFractalAuthority):
            raise ExperimentalLiftError("السلطةُ التجريبيّةُ من نوعها")
        active = authority.require_active_for_run(permit, run_id=run_id)
        if not isinstance(candidate, ExperimentalLiftCandidate):
            raise ExperimentalLiftError("المقيسُ مرشَّحُ رفعٍ تجريبيٍّ من نوعه")
        lift_permit = candidate.lift_permit
        if lift_permit.run_permit_content_id != active.content_id:
            raise ExperimentalLiftError("إذنُ رفعٍ صادرٌ عن إذن تشغيلٍ آخر")
        if not active.permitted_experimental_lift:
            return ExperimentalLiftDecision(
                status=ExperimentalLiftStatus.REFUSED_OUT_OF_SCOPE,
                reason="الرفعُ التجريبيُّ غيرُ مأذونٍ فيه في هذا الإذن",
                experimental_seed=None,
                open_authority_gap=NO_SCALE_NECESSITY_CERTIFICATION_IN_EXPERIMENT,
            )
        if candidate.closed_node.scale_ref != lift_permit.source_scale_ref:
            return ExperimentalLiftDecision(
                status=ExperimentalLiftStatus.REFUSED_OUT_OF_SCOPE,
                reason="العقدةُ المغلقةُ ليست عند مقياس المصدر المأذون فيه",
                experimental_seed=None,
                open_authority_gap=NO_SCALE_NECESSITY_CERTIFICATION_IN_EXPERIMENT,
            )
        if not active.permits_target_scale(lift_permit.target_scale_ref):
            return ExperimentalLiftDecision(
                status=ExperimentalLiftStatus.REFUSED_OUT_OF_SCOPE,
                reason="مقياسُ الهدف خارج مدى الإذن التجريبيّ",
                experimental_seed=None,
                open_authority_gap=NO_SCALE_NECESSITY_CERTIFICATION_IN_EXPERIMENT,
            )
        return ExperimentalLiftDecision(
            status=ExperimentalLiftStatus.EXPERIMENTAL_SEED_ISSUED,
            reason=(
                "عقدةٌ مغلقةٌ وإذنُ رفعٍ تجريبيٌّ داخلَ المدى، فصدرت بذرةٌ "
                "تجريبيّةٌ تُختبَر بها دعوى الضرورة؛ و"
                + EXPERIMENTAL_LIFT_TESTS_NECESSITY_IT_DOES_NOT_CERTIFY_NECESSITY
            ),
            experimental_seed=ExperimentalNextScaleSeed(
                seed_id=_named_text(seed_id, "مُعرِّفُ البذرة التجريبيّة"),
                experiment_id=active.experiment_id,
                run_id=active.run_id,
                lift_permit_content_id=lift_permit.content_id,
                source_scale_ref=lift_permit.source_scale_ref,
                target_scale_ref=lift_permit.target_scale_ref,
                closed_node_content_id=candidate.closed_node.node.content_id,
                necessity_claim_under_test=lift_permit.necessity_claim_under_test,
                carried_residuals=candidate.carried_residuals
                + candidate.closed_node.residuals,
                issuance=_EXPERIMENTAL_SEED_ISSUANCE,
            ),
            open_authority_gap=NO_SCALE_NECESSITY_CERTIFICATION_IN_EXPERIMENT,
        )
