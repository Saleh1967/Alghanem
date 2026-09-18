"""`G0.SDAL-0.INDUCTION`: برهانُ `zero-one` على جبر `StructuralDal`.

    ZeroStructuralState  --Δ-->  ShapePartitionHypothesisSet

والبرهانُ هنا ليس أنّ `1 → 2`، بل أنّ ناتجَ المستوى السابق يدخل اللاحقَ مع حفظ
هويّته وأثره ونسبه، وأنّ التقسيمَ يُعرَض بلا فائزٍ مفروض، وأنّ بقيّةً حاجبةً
تمنع الترقيةَ ولو صحّت إعادةُ البناء.

والمقارنةُ مع النموذج الأضعف تقع على **عقد المخرج** لا على نصِّ المخرج؛ فإنّ
الوصلَ البسيط يبلغ الرموزَ عينَها ولا يبلغ تقسيمًا مُصنَّفًا ولا بقيّةً مُسمّاةً
ولا أثرًا متّصلًا.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .audit import (
    ImportIsolationReport,
    VocabularyAuditReport,
    import_isolation_audit,
    vocabulary_audit,
)
from .hypothesis import (
    ShapePartitionHypothesisSet,
    SlotRole,
    StructuralDecomposition,
    ZeroStructuralState,
    decompose,
    enumerate_shape_partitions,
    zero_structural_state,
)
from .laws import (
    PREREGISTRATION_DIGEST,
    AcceptanceItem,
    OutputContractComponent,
    StructuralDalError,
)
from .residual import PromotionStanding
from .slots import StructuralWhole, origin_whole
from .transition import PromotedWhole, ScaleAscent, ascend_one_slot, promote_part_to_whole

__all__ = [
    "ComparativeStanding",
    "ContractOutcome",
    "PromotionAttempt",
    "WeakerModelObservation",
    "ZeroOneAlgebraReport",
    "prove_zero_one_algebra",
    "run_weaker_model",
]


class ContractOutcome(Enum):
    """حالُ نموذجٍ من عقد المخرج؛ مفردةٌ مغلقة."""

    CONTRACT_MET = "contract_met"
    CONTRACT_PARTIAL = "contract_partial"
    CONTRACT_UNMET = "contract_unmet"


class ComparativeStanding(Enum):
    """موقفُ المقارنة بين البنية والنموذج الأضعف."""

    STRUCTURAL_ONLY = "structural_only"
    BOTH_MEET = "both_meet"
    WEAKER_ONLY = "weaker_only"
    NEITHER_MEETS = "neither_meets"


@dataclass(frozen=True, slots=True)
class WeakerModelObservation:
    """تشغيلُ نموذجٍ أضعفَ على المدخل عينِه، ومقارنتُه على عقد المخرج."""

    model_id: str
    description: str
    output: tuple[str, ...]
    satisfied: tuple[OutputContractComponent, ...]

    @property
    def outcome(self) -> ContractOutcome:
        """حالُ النموذج الأضعف من عقد المخرج؛ مُشتَقٌّ لا مُصرَّح."""

        return _outcome_of(self.satisfied)


@dataclass(frozen=True, slots=True)
class PromotionAttempt:
    """محاولةُ ترقيةِ جزءٍ إلى كلّ: موقفُها، وناتجُها أو سببُ رفضها."""

    decomposition_id: str
    standing: PromotionStanding
    promoted: PromotedWhole | None
    refusal: str | None

    def __post_init__(self) -> None:
        if (self.promoted is None) == (self.refusal is None):
            raise StructuralDalError("المحاولةُ إمّا ناتجٌ وإمّا سببُ رفضٍ مُسمًّى")
        if self.standing is PromotionStanding.PROMOTION_BLOCKED and (
            self.promoted is not None
        ):
            raise StructuralDalError("ترقيةٌ وقعت مع بقيّةٍ حاجبة")


def _outcome_of(
    satisfied: tuple[OutputContractComponent, ...],
) -> ContractOutcome:
    if not satisfied:
        return ContractOutcome.CONTRACT_UNMET
    if set(satisfied) == set(OutputContractComponent):
        return ContractOutcome.CONTRACT_MET
    return ContractOutcome.CONTRACT_PARTIAL


def run_weaker_model(whole: StructuralWhole) -> WeakerModelObservation:
    """النموذجُ الأضعف: وصلُ الرموز بلا تقسيمٍ ولا بقيّةٍ ولا أثر."""

    return WeakerModelObservation(
        model_id="weaker.concatenation",
        description="وصلُ رموز الخانات بترتيبها بلا أدوارٍ ولا بقايا ولا أثر",
        output=whole.tokens,
        satisfied=(OutputContractComponent.WHOLE_RECONSTRUCTION,),
    )


@dataclass(frozen=True, slots=True)
class ZeroOneAlgebraReport:
    """تقريرُ برهان `zero-one`: كلُّ بندٍ من بنود القبول بدليله التشغيليّ."""

    zero: ZeroStructuralState
    zero_hypotheses: ShapePartitionHypothesisSet
    ascent: ScaleAscent
    one_hypotheses: ShapePartitionHypothesisSet
    one_decompositions: tuple[StructuralDecomposition, ...]
    promotion_attempts: tuple[PromotionAttempt, ...]
    weaker: WeakerModelObservation
    isolation: ImportIsolationReport
    vocabulary: VocabularyAuditReport

    @property
    def preregistration_digest(self) -> str:
        """بصمةُ التسجيل المسبق التي جرى عليها القياس."""

        return PREREGISTRATION_DIGEST

    @property
    def structural_satisfied(self) -> tuple[OutputContractComponent, ...]:
        """مُركّباتُ عقد المخرج التي وفّاها الجبرُ البنيويُّ عند الواحد."""

        if not self.one_decompositions:
            return ()
        common = set(self.one_decompositions[0].satisfied_contract_components)
        for decomposition in self.one_decompositions[1:]:
            common &= set(decomposition.satisfied_contract_components)
        return tuple(
            component for component in OutputContractComponent if component in common
        )

    @property
    def structural_outcome(self) -> ContractOutcome:
        """حالُ الجبر البنيويّ من عقد المخرج."""

        return _outcome_of(self.structural_satisfied)

    @property
    def standing(self) -> ComparativeStanding:
        """موقفُ المقارنة؛ مُشتَقٌّ من الحالين لا مكتوبٌ بينهما."""

        structural = self.structural_outcome is ContractOutcome.CONTRACT_MET
        weaker = self.weaker.outcome is ContractOutcome.CONTRACT_MET
        if structural and weaker:
            return ComparativeStanding.BOTH_MEET
        if structural:
            return ComparativeStanding.STRUCTURAL_ONLY
        if weaker:
            return ComparativeStanding.WEAKER_ONLY
        return ComparativeStanding.NEITHER_MEETS

    @property
    def blocked_attempts(self) -> tuple[PromotionAttempt, ...]:
        """محاولاتُ ترقيةٍ مُنِعت لبقيّةٍ حاجبة."""

        return tuple(
            attempt
            for attempt in self.promotion_attempts
            if attempt.standing is PromotionStanding.PROMOTION_BLOCKED
        )

    @property
    def permitted_attempts(self) -> tuple[PromotionAttempt, ...]:
        """محاولاتُ ترقيةٍ وقعت بلا حاجب."""

        return tuple(
            attempt
            for attempt in self.promotion_attempts
            if attempt.standing is PromotionStanding.PROMOTION_PERMITTED
        )

    @property
    def findings(self) -> dict[AcceptanceItem, bool]:
        """بنودُ القبول الثمانية بأحكامها المُشتقّة من هذا التشغيل."""

        zero_holds = (
            self.zero.reconstructs_exactly
            and self.zero.covers_every_slot_once
            and self.zero.preserves_identity
            and self.zero.preserves_trace
        )
        multiple = (
            self.one_hypotheses.count > 1 and self.one_hypotheses.forced_winner is None
        )
        no_dropped = bool(self.one_decompositions) and all(
            decomposition.covers_every_slot_once and decomposition.reconstructs_whole
            for decomposition in self.one_decompositions
        )
        parent_survives = (
            self.ascent.after.anchor_id == self.ascent.before.anchor_id
            and bool(self.permitted_attempts)
            and all(
                attempt.promoted is not None and attempt.promoted.keeps_parent_anchor
                for attempt in self.permitted_attempts
            )
        )
        blocking_works = bool(self.blocked_attempts) and all(
            attempt.promoted is None for attempt in self.blocked_attempts
        )
        return {
            AcceptanceItem.ZERO_RECONSTRUCTS_EXACTLY: zero_holds,
            AcceptanceItem.ONE_PRODUCES_MULTIPLE_HYPOTHESES: multiple,
            AcceptanceItem.NO_SLOT_SILENTLY_DROPPED: no_dropped,
            AcceptanceItem.PARENT_IDENTITY_SURVIVES_SCALE_TRANSITION: parent_survives,
            AcceptanceItem.BLOCKING_RESIDUAL_PREVENTS_PROMOTION: blocking_works,
            AcceptanceItem.TRACE_IS_CUMULATIVE: self.ascent.trace_is_cumulative,
            AcceptanceItem.LAYER_IS_STRUCTURALLY_ISOLATED: self.isolation.is_isolated,
            AcceptanceItem.NO_LINGUISTIC_CLAIM_IN_OUTPUT: self.vocabulary.is_clean,
        }

    @property
    def unmet_items(self) -> tuple[AcceptanceItem, ...]:
        """بنودُ القبول التي لم يُثبِتها هذا التشغيل."""

        return tuple(item for item, held in self.findings.items() if not held)

    @property
    def algebra_holds(self) -> bool:
        """هل ثبتت بنودُ القبول الثمانيةُ جميعًا؟"""

        return not self.unmet_items

    @property
    def what_is_not_established(self) -> tuple[str, ...]:
        """ما لا يُثبِته هذا البرهانُ مهما تمّ."""

        return (
            self.zero.does_not_establish,
            *self.one_hypotheses.what_it_is_not,
        )


def prove_zero_one_algebra(
    *,
    base_token: str = "SlotA",
    added_token: str = "SlotB",
    subject_id: str = "zero_one",
) -> ZeroOneAlgebraReport:
    """أقِم برهانَ `zero-one` على رموزٍ مُصطنَعة؛ ولا لسانَ في المدخل."""

    whole = origin_whole(
        whole_id=f"whole.{subject_id}",
        anchor_id=f"anchor.{subject_id}",
        carrier_id=f"carrier.{subject_id}",
        tokens=(base_token,),
    )
    zero = zero_structural_state(whole)
    zero_hypotheses = enumerate_shape_partitions(whole)
    ascent = ascend_one_slot(whole, added_token)
    one_hypotheses = enumerate_shape_partitions(ascent.after)
    decompositions = tuple(
        decompose(ascent.after, hypothesis)
        for hypothesis in one_hypotheses.hypotheses
    )
    attempts: list[PromotionAttempt] = []
    for decomposition in decompositions:
        standing = decomposition.promotion_standing
        if standing is PromotionStanding.PROMOTION_BLOCKED:
            attempts.append(
                PromotionAttempt(
                    decomposition_id=decomposition.decomposition_id,
                    standing=standing,
                    promoted=None,
                    refusal="بقيّةٌ حاجبةٌ تمنع الترقية",
                )
            )
            continue
        attempts.append(
            PromotionAttempt(
                decomposition_id=decomposition.decomposition_id,
                standing=standing,
                promoted=promote_part_to_whole(decomposition, SlotRole.CORE),
                refusal=None,
            )
        )
    return ZeroOneAlgebraReport(
        zero=zero,
        zero_hypotheses=zero_hypotheses,
        ascent=ascent,
        one_hypotheses=one_hypotheses,
        one_decompositions=decompositions,
        promotion_attempts=tuple(attempts),
        weaker=run_weaker_model(ascent.after),
        isolation=import_isolation_audit(),
        vocabulary=vocabulary_audit(),
    )
