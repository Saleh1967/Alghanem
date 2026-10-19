"""تجميعُ الشواهد وعقدُ الكفاية: جمعٌ بلا حكم، وإعلانٌ بلا مقياس.

    Witness*  →  WitnessBundle        (تجميعٌ لا حكم)
    WitnessBundle  ≠  EvidenceSufficiencyAssessment

**والحزمةُ لا تحمل حكمًا**: لا `verdict` ولا `license` ولا `rank` ولا درجة؛
تحفظ الشواهدَ بأعيانها وتفرزها برصدها لا برتبتها.

**وعقدُ الكفاية إعلانٌ مُجمَّدٌ فقط في هذه المرحلة**
(`SufficiencyCriterionMustPrecedeItsMeasurement`): يُكتَب قبل أن تُعَدَّ
الشواهد، ولا مُقيِّمَ له هنا؛ فقياسُه سلطةُ طبقةٍ مستقلّةٍ لم تُفتَح.

تسجيلٌ لا سلطة: لا ترخيصَ، ولا رتبةَ دائمة، ولا حكمَ كفاية.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..canonical_content import canonical_bytes, canonical_digest, is_canonical_digest
from ..fractal_generation import FractalResidual
from .authority_gaps import (
    NO_SUFFICIENCY_ASSESSMENT_AUTHORITY,
    ExperimentalAuthorityGap,
)
from .laws import (
    SUFFICIENCY_CRITERION_MUST_PRECEDE_ITS_MEASUREMENT,
    WITNESS_ACCUMULATION_PRECEDES_LICENSING,
)
from .witness import ExperimentalStanding, FractalExperimentalWitness

__all__ = [
    "WitnessBundle",
    "WitnessBundleError",
    "WitnessSufficiencyContract",
]


class WitnessBundleError(ValueError):
    """رفضٌ عند تكوين حزمةِ شواهدَ أو عقدِ كفاية."""


def _named_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise WitnessBundleError(f"{label} نصٌّ غير فارغ")
    return value


def _named_texts(values: object, label: str) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        raise WitnessBundleError(f"{label} مجموعةٌ مُصرَّحٌ بها")
    for value in values:
        _named_text(value, f"عضوٌ في {label}")
    return values


@dataclass(frozen=True, slots=True)
class WitnessBundle:
    """حزمةُ شواهد: تجميعٌ مُفهرَسٌ بلا حكمٍ ولا ترخيصٍ ولا درجة."""

    bundle_id: str
    target_claim_ref: str
    preregistration_ref: str
    witnesses: tuple[FractalExperimentalWitness, ...]
    input_coverage: tuple[str, ...]
    open_authority_gaps: tuple[ExperimentalAuthorityGap, ...] = (
        NO_SUFFICIENCY_ASSESSMENT_AUTHORITY,
    )

    def __post_init__(self) -> None:
        _named_text(self.bundle_id, "مُعرِّفُ الحزمة")
        _named_text(self.target_claim_ref, "مرجعُ الدعوى المقصودة")
        if not is_canonical_digest(self.preregistration_ref):
            raise WitnessBundleError("مرجعُ التسجيل المُسبَق بصمةٌ قانونيّة")
        if not isinstance(self.witnesses, tuple) or not self.witnesses:
            raise WitnessBundleError(
                "الحزمةُ شاهدٌ واحدٌ فأكثر؛ و" + WITNESS_ACCUMULATION_PRECEDES_LICENSING
            )
        seen: set[str] = set()
        for witness in self.witnesses:
            if not isinstance(witness, FractalExperimentalWitness):
                raise WitnessBundleError("عضوٌ في الحزمة خارج نوع الشاهد")
            if witness.witness_id in seen:
                raise WitnessBundleError("مُعرِّفُ شاهدٍ مُكرَّرٌ في حزمةٍ واحدة")
            seen.add(witness.witness_id)
        _named_texts(self.input_coverage, "تغطيةُ المدخلات")
        if not isinstance(self.open_authority_gaps, tuple):
            raise WitnessBundleError("فجواتُ سلطة الحزمة مجموعةٌ مُصرَّحٌ بها")
        for gap in self.open_authority_gaps:
            if not isinstance(gap, ExperimentalAuthorityGap):
                raise WitnessBundleError("عضوٌ في فجوات سلطة الحزمة خارج نوعه")

    def _of(
        self, standing: ExperimentalStanding
    ) -> tuple[FractalExperimentalWitness, ...]:
        return tuple(
            witness for witness in self.witnesses if witness.standing is standing
        )

    @property
    def witness_ids(self) -> tuple[str, ...]:
        """مُعرِّفاتُ الشواهد بترتيب إيداعها؛ والترتيبُ عرضٌ لا ترجيح."""

        return tuple(witness.witness_id for witness in self.witnesses)

    @property
    def independent_run_ids(self) -> frozenset[str]:
        """تشغيلاتُ الشواهد بأعيانها؛ استقلالُها مرصودٌ لا محكومٌ به."""

        return frozenset(witness.run_id for witness in self.witnesses)

    @property
    def positive_observations(self) -> tuple[FractalExperimentalWitness, ...]:
        """الشواهدُ التي رُصِد فيها تأييد؛ رصدًا لا حكمًا."""

        return self._of(ExperimentalStanding.OBSERVED_SUPPORT)

    @property
    def refuting_observations(self) -> tuple[FractalExperimentalWitness, ...]:
        """الشواهدُ التي رُصِد فيها تكذيب؛ وتبقى في الحزمة بلا محو."""

        return self._of(ExperimentalStanding.OBSERVED_REFUTATION)

    @property
    def underpowered_observations(self) -> tuple[FractalExperimentalWitness, ...]:
        """الشواهدُ الضعيفةُ القوّة؛ شواهدُ كذلك لا فراغ."""

        return self._of(ExperimentalStanding.UNDERPOWERED)

    @property
    def run_failure_observations(self) -> tuple[FractalExperimentalWitness, ...]:
        """الشواهدُ التي أخفق تشغيلُها؛ محفوظةٌ بأسبابها."""

        return self._of(ExperimentalStanding.RUN_FAILURE)

    @property
    def residual_union(self) -> tuple[FractalResidual, ...]:
        """بقايا الحزمة كلُّها مجموعةً بلا محو."""

        return tuple(
            residual for witness in self.witnesses for residual in witness.residuals
        )

    @property
    def authority_gaps(self) -> tuple[ExperimentalAuthorityGap, ...]:
        """فجواتُ السلطة القائمةُ على الحزمة وشواهدِها."""

        gaps: list[ExperimentalAuthorityGap] = list(self.open_authority_gaps)
        for witness in self.witnesses:
            for gap in witness.authority_gaps:
                if gap not in gaps:
                    gaps.append(gap)
        return tuple(gaps)

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الحزمة للبصمة."""

        return {
            "bundle_id": self.bundle_id,
            "target_claim_ref": self.target_claim_ref,
            "preregistration_ref": self.preregistration_ref,
            "witness_content_ids": [witness.content_id for witness in self.witnesses],
            "independent_run_ids": sorted(self.independent_run_ids),
            "input_coverage": list(self.input_coverage),
            "authority_gaps": [
                gap.as_canonical_content() for gap in self.authority_gaps
            ],
        }

    @property
    def content_id(self) -> str:
        """بصمةُ الحزمة؛ مُشتَقّةٌ لا مكتوبة."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


@dataclass(frozen=True, slots=True)
class WitnessSufficiencyContract:
    """عقدُ كفايةٍ **معلَنٌ فقط**: يُجمَّد قبل العدّ، ولا مُقيِّمَ له في هذه المرحلة."""

    contract_id: str
    target_claim: str
    required_scope: str
    independence_criterion: str
    positive_witness_requirement: str
    negative_controls: tuple[str, ...]
    weaker_model_requirement: str
    counterexample_policy: str
    replication_requirement: str
    reconstruction_requirement: str
    residual_tolerance: str
    blocking_residuals: tuple[str, ...]

    def __post_init__(self) -> None:
        for value, label in (
            (self.contract_id, "مُعرِّفُ عقد الكفاية"),
            (self.target_claim, "الدعوى المقصودة"),
            (self.required_scope, "المدى المطلوب"),
            (self.independence_criterion, "معيارُ الاستقلال"),
            (self.positive_witness_requirement, "شرطُ الشواهد المؤيِّدة"),
            (self.weaker_model_requirement, "شرطُ النموذج الأضعف"),
            (self.counterexample_policy, "سياسةُ النقوض"),
            (self.replication_requirement, "شرطُ التكرار"),
            (self.reconstruction_requirement, "شرطُ إعادة البناء"),
            (self.residual_tolerance, "حدُّ احتمال البقايا"),
        ):
            _named_text(value, label)
        _named_texts(self.negative_controls, "الضوابطُ السالبة")
        _named_texts(self.blocking_residuals, "البقايا المانعة")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى عقد الكفاية للبصمة."""

        return {
            "contract_id": self.contract_id,
            "target_claim": self.target_claim,
            "required_scope": self.required_scope,
            "independence_criterion": self.independence_criterion,
            "positive_witness_requirement": self.positive_witness_requirement,
            "negative_controls": list(self.negative_controls),
            "weaker_model_requirement": self.weaker_model_requirement,
            "counterexample_policy": self.counterexample_policy,
            "replication_requirement": self.replication_requirement,
            "reconstruction_requirement": self.reconstruction_requirement,
            "residual_tolerance": self.residual_tolerance,
            "blocking_residuals": list(self.blocking_residuals),
            "note": SUFFICIENCY_CRITERION_MUST_PRECEDE_ITS_MEASUREMENT,
        }

    @property
    def content_id(self) -> str:
        """بصمةُ عقد الكفاية؛ مُشتَقّةٌ لا مكتوبة."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))
