"""الشاهدُ التجريبيّ: رصدٌ مُسجَّلٌ بأثره وبقاياه، لا حكمٌ ولا رتبة.

    ExperimentalRun  →  FractalExperimentalWitness

**والنجاحُ شاهدٌ لا ترخيص** (`ExperimentalSuccessIsAWitnessNotALicense`):
`OBSERVED_SUPPORT` و`OBSERVED_REFUTATION` و`UNDERPOWERED` و`RUN_FAILURE`
أربعتُها شواهد؛ فالفشلُ يُسجَّل كما يُسجَّل التأييد، ولا يُحذَف.

**ولا لغةَ رتبةٍ في الشاهد**: كلماتُ `LICENSED` و`PROVED` و`NECESSARY` و
`CERTIFIED_LANGUAGE_RULE` و`TRUE` مرفوضةٌ في نصوص الرصد، لأنّها تُقرَأ حكمًا
وليست في الشاهد سلطةٌ تحكم.

تسجيلٌ لا سلطة: لا ترخيصَ، ولا رتبةَ دائمة، ولا حكمَ كفاية.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest, is_canonical_digest
from ..fractal_generation import (
    FractalResidual,
    FractalScaleRef,
    FractalTrace,
    PatternRef,
)
from .authority_gaps import ExperimentalAuthorityGap
from .laws import (
    EXPERIMENTAL_SUCCESS_IS_A_WITNESS_NOT_A_LICENSE,
    WITNESS_IS_NOT_JUDGMENT,
)

__all__ = [
    "FORBIDDEN_RANK_VOCABULARY",
    "ExperimentalStanding",
    "FractalExperimentalWitness",
    "WitnessError",
]


class WitnessError(ValueError):
    """رفضٌ عند تكوين شاهدٍ تجريبيٍّ أو حمله لغةَ رتبة."""


FORBIDDEN_RANK_VOCABULARY: Final[tuple[str, ...]] = (
    "LICENSED",
    "TRUE",
    "NECESSARY",
    "PROVED",
    "CERTIFIED_LANGUAGE_RULE",
)
"""ألفاظُ الرتبة الممنوعةُ في نصوص الرصد؛ فالشاهدُ يرصد ولا يحكم."""


def _named_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise WitnessError(f"{label} نصٌّ غير فارغ")
    _refuse_rank_vocabulary(value, label)
    return value


def _refuse_rank_vocabulary(value: str, label: str) -> None:
    for word in FORBIDDEN_RANK_VOCABULARY:
        if word in value:
            raise WitnessError(
                f"{label} يحمل لفظَ رتبةٍ `{word}`؛ و" + WITNESS_IS_NOT_JUDGMENT
            )


def _observations(values: object, label: str) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        raise WitnessError(f"{label} مجموعةٌ مُصرَّحٌ بها")
    for value in values:
        _named_text(value, f"عضوٌ في {label}")
    return values


class ExperimentalStanding(Enum):
    """وقوفُ التشغيل التجريبيّ؛ أربعةٌ كلُّها شواهد، وليس فيها ترخيص."""

    OBSERVED_SUPPORT = "observed_support"
    OBSERVED_REFUTATION = "observed_refutation"
    UNDERPOWERED = "underpowered"
    RUN_FAILURE = "run_failure"


@dataclass(frozen=True, slots=True)
class FractalExperimentalWitness:
    """شاهدُ تشغيلٍ تجريبيٍّ واحد: ما رُصِد، وبأيِّ إذنٍ، وعلى أيِّ مدخلٍ مُجمَّد."""

    witness_id: str
    experiment_id: str
    run_id: str
    permit_content_id: str
    frozen_input_content_id: str
    preregistration_content_id: str
    standing: ExperimentalStanding
    source_scale: FractalScaleRef
    identity_before: str
    identity_after: str
    movement_kind: str
    observed_difference: str
    reconstruction_observation: str
    closure_observation: str
    pattern_ref: PatternRef | None = None
    target_scale: FractalScaleRef | None = None
    preserved_invariants_observed: tuple[str, ...] = ()
    weaker_model_observations: tuple[str, ...] = ()
    negative_control_observations: tuple[str, ...] = ()
    counterexample_observations: tuple[str, ...] = ()
    residuals: tuple[FractalResidual, ...] = ()
    authority_gaps: tuple[ExperimentalAuthorityGap, ...] = ()
    trace: FractalTrace | None = None

    def __post_init__(self) -> None:
        for value, label in (
            (self.witness_id, "مُعرِّفُ الشاهد"),
            (self.experiment_id, "مُعرِّفُ التجربة"),
            (self.run_id, "مُعرِّفُ التشغيل"),
            (self.identity_before, "هويّةُ ما قبل"),
            (self.identity_after, "هويّةُ ما بعد"),
            (self.movement_kind, "جنسُ الحركة المرصود"),
            (self.observed_difference, "الفرقُ المرصود"),
            (self.reconstruction_observation, "رصدُ إعادة البناء"),
            (self.closure_observation, "رصدُ الإغلاق"),
        ):
            _named_text(value, label)
        for digest, label in (
            (self.permit_content_id, "بصمةُ الإذن"),
            (self.frozen_input_content_id, "بصمةُ المدخل المُجمَّد"),
            (self.preregistration_content_id, "بصمةُ التسجيل المُسبَق"),
        ):
            if not is_canonical_digest(digest):
                raise WitnessError(f"{label} بصمةٌ قانونيّة")
        if not isinstance(self.standing, ExperimentalStanding):
            raise WitnessError(
                "وقوفُ الشاهد عضوٌ في مفردته المغلقة؛ و"
                + EXPERIMENTAL_SUCCESS_IS_A_WITNESS_NOT_A_LICENSE
            )
        if not isinstance(self.source_scale, FractalScaleRef):
            raise WitnessError("مقياسُ المصدر مرجعٌ من نوعه")
        if self.target_scale is not None and not isinstance(
            self.target_scale, FractalScaleRef
        ):
            raise WitnessError("مقياسُ الهدف مرجعٌ من نوعه إن ذُكِر")
        if self.pattern_ref is not None and not isinstance(
            self.pattern_ref, PatternRef
        ):
            raise WitnessError("مرجعُ النمط من نوعه إن ذُكِر")
        _observations(self.preserved_invariants_observed, "الثوابتُ المرصودة")
        _observations(self.weaker_model_observations, "رصدُ النموذج الأضعف")
        _observations(self.negative_control_observations, "رصدُ الضابط السالب")
        _observations(self.counterexample_observations, "رصدُ النقوض")
        if not isinstance(self.residuals, tuple):
            raise WitnessError("بقايا الشاهد مجموعةٌ مُصرَّحٌ بها")
        for residual in self.residuals:
            if not isinstance(residual, FractalResidual):
                raise WitnessError("عضوٌ في بقايا الشاهد خارج نوعه")
        if not isinstance(self.authority_gaps, tuple):
            raise WitnessError("فجواتُ سلطة الشاهد مجموعةٌ مُصرَّحٌ بها")
        for gap in self.authority_gaps:
            if not isinstance(gap, ExperimentalAuthorityGap):
                raise WitnessError("عضوٌ في فجوات سلطة الشاهد خارج نوعه")
        if self.trace is not None and not isinstance(self.trace, FractalTrace):
            raise WitnessError("أثرُ الشاهد متّصلٌ من نوعه إن ذُكِر")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الشاهد للبصمة."""

        return {
            "witness_id": self.witness_id,
            "experiment_id": self.experiment_id,
            "run_id": self.run_id,
            "permit_content_id": self.permit_content_id,
            "frozen_input_content_id": self.frozen_input_content_id,
            "preregistration_content_id": self.preregistration_content_id,
            "standing": self.standing.value,
            "source_scale_id": self.source_scale.scale_id,
            "target_scale_id": (
                None if self.target_scale is None else self.target_scale.scale_id
            ),
            "pattern_id": (
                None if self.pattern_ref is None else self.pattern_ref.pattern_id
            ),
            "identity_before": self.identity_before,
            "identity_after": self.identity_after,
            "movement_kind": self.movement_kind,
            "observed_difference": self.observed_difference,
            "preserved_invariants_observed": list(self.preserved_invariants_observed),
            "reconstruction_observation": self.reconstruction_observation,
            "closure_observation": self.closure_observation,
            "weaker_model_observations": list(self.weaker_model_observations),
            "negative_control_observations": list(self.negative_control_observations),
            "counterexample_observations": list(self.counterexample_observations),
            "residuals": [
                residual.as_canonical_content() for residual in self.residuals
            ],
            "authority_gaps": [
                gap.as_canonical_content() for gap in self.authority_gaps
            ],
            "trace_output_content_id": (
                None if self.trace is None else self.trace.output_content_id
            ),
        }

    @property
    def content_id(self) -> str:
        """بصمةُ الشاهد؛ مُشتَقّةٌ لا مكتوبة."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))
