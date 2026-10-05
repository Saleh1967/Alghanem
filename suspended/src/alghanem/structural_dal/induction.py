"""`G0.SDAL-0.INDUCTION`: برهانُ `zero-one` على جبر `StructuralDal`.

    ZeroStructuralState  --Δ-->  ShapePartitionHypothesisSet

والبرهانُ هنا ليس أنّ `1 → 2`، بل أنّ ناتجَ المستوى السابق يدخل اللاحقَ مع حفظ
هويّته وأثره ونسبه، وأنّ التقسيمَ يُعرَض بلا فائزٍ مفروض، وأنّ بقيّةً حاجبةً
تمنع الترقيةَ ولو صحّت إعادةُ البناء.

والقراءةُ مع النموذج الأضعف تقع على **عقد المخرج** لا على نصِّ المخرج؛ فإنّ
الوصلَ البسيط يبلغ الرموزَ عينَها ولا يبلغ تقسيمًا مُصنَّفًا ولا بقيّةً مُسمّاةً
ولا أثرًا متّصلًا.

ولا تُقرَأ هذه القراءةُ حكمَ قوّة: عقدُ المخرج مُعرَّفٌ من هذه الطبقة نفسِها،
و`SelfDefinedContract ⇏ ComparativeStrength`؛ فالمقارنةُ الحقيقيّةُ موقوفةٌ على
عقدٍ محايدٍ لا يملك أيُّ نظامٍ تعريفَه، ولا يُفتَح في هذا الطور.
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
    SELF_DEFINED_CONTRACT_DOES_NOT_ESTABLISH_COMPARATIVE_STRENGTH,
    STRUCTURAL_OPERATOR_PROOF_IS_ONLY_ELIGIBLE_FOR_FIBER_INTEGRATION,
    AcceptanceItem,
    OutputContractComponent,
    StructuralDalError,
)
from .residual import PromotionStanding, ResidualClass
from .slots import StructuralWhole, origin_whole
from .transition import (
    DeferredBranchBirth,
    IdentityTransitionAvailability,
    IdentityTransitionMode,
    ScaleAscent,
    ascend_one_slot,
    request_part_branch_birth,
)

__all__ = [
    "ContractOutcome",
    "PromotionAttempt",
    "SelfDefinedContractReading",
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


class SelfDefinedContractReading(Enum):
    """قراءةُ عقدِ مخرجٍ عرّفته هذه الطبقةُ لنفسها؛ وصفٌ داخلَه لا حكمُ قوّة."""

    THIS_LAYER_MEETS_ITS_OWN_CONTRACT_ALONE = "this_layer_meets_its_own_contract_alone"
    BOTH_MEET_THIS_LAYERS_CONTRACT = "both_meet_this_layers_contract"
    ONLY_THE_WEAKER_MEETS_THIS_LAYERS_CONTRACT = (
        "only_the_weaker_meets_this_layers_contract"
    )
    NEITHER_MEETS_THIS_LAYERS_CONTRACT = "neither_meets_this_layers_contract"

    @property
    def does_not_establish(self) -> str:
        """ما لا تُثبِته هذه القراءةُ مهما مالت."""

        return SELF_DEFINED_CONTRACT_DOES_NOT_ESTABLISH_COMPARATIVE_STRENGTH


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
    """محاولةُ ترقيةِ جزءٍ إلى كلّ: موقفُها، وسببُ رفضها مُسمًّى.

    ولا حقلَ فيها لناتجٍ مُرقًّى: لا ترقيةَ مع بقيّةٍ حاجبة، ولا ولادةَ فرعٍ
    بشهادةٍ تُصدِرها هذه الطبقةُ لنفسها.
    """

    decomposition_id: str
    standing: PromotionStanding
    refusal: str
    deferred_birth: DeferredBranchBirth | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.refusal, str) or not self.refusal.strip():
            raise StructuralDalError("سببُ رفض المحاولة نصٌّ غيرُ فارغ")
        if self.deferred_birth is not None and not isinstance(
            self.deferred_birth, DeferredBranchBirth
        ):
            raise StructuralDalError("الطلبُ المؤجَّلُ من نوعه أو لا طلبَ")


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
    def self_defined_contract_reading(self) -> SelfDefinedContractReading:
        """قراءةُ العقد الذاتيِّ؛ مُشتَقّةٌ من الحالين ولا تُثبِت قوّةً مقارنة."""

        structural = self.structural_outcome is ContractOutcome.CONTRACT_MET
        weaker = self.weaker.outcome is ContractOutcome.CONTRACT_MET
        if structural and weaker:
            return SelfDefinedContractReading.BOTH_MEET_THIS_LAYERS_CONTRACT
        if structural:
            return SelfDefinedContractReading.THIS_LAYER_MEETS_ITS_OWN_CONTRACT_ALONE
        if weaker:
            return SelfDefinedContractReading.ONLY_THE_WEAKER_MEETS_THIS_LAYERS_CONTRACT
        return SelfDefinedContractReading.NEITHER_MEETS_THIS_LAYERS_CONTRACT

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
        """محاولاتُ ترقيةٍ ارتفع عنها الحاجب؛ وهي في هذا الطور خاليةٌ بحكم قانونها."""

        return tuple(
            attempt
            for attempt in self.promotion_attempts
            if attempt.standing is PromotionStanding.PROMOTION_PERMITTED
        )

    @property
    def deferred_births(self) -> tuple[DeferredBranchBirth, ...]:
        """طلباتُ ولادةِ فرعٍ المؤجَّلةُ لانعدام سلطةِ شهادتها."""

        return tuple(
            attempt.deferred_birth
            for attempt in self.promotion_attempts
            if attempt.deferred_birth is not None
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
        zero_is_neutral = (
            self.zero.assigns_no_positive_role
            and self.zero.promotion_standing is PromotionStanding.PROMOTION_BLOCKED
        )
        distinct_identity = bool(self.one_decompositions) and all(
            decomposition.parts_carry_distinct_identity
            for decomposition in self.one_decompositions
        )
        rescaling_preserves = (
            self.ascent.mode is IdentityTransitionMode.SAME_ENTITY_RESCALING
            and self.ascent.preserves_instance_identity
        )
        births_deferred = bool(self.deferred_births) and all(
            birth.availability is IdentityTransitionAvailability.DEFERRED
            for birth in self.deferred_births
        )
        role_basis_blocks = bool(self.one_decompositions) and all(
            any(
                reading.residual_class is ResidualClass.BLOCKING
                for reading in decomposition.residuals
            )
            and decomposition.promotion_standing is PromotionStanding.PROMOTION_BLOCKED
            for decomposition in self.one_decompositions
        )
        multiple = (
            self.one_hypotheses.count > 1 and self.one_hypotheses.forced_winner is None
        )
        no_dropped = bool(self.one_decompositions) and all(
            decomposition.covers_every_slot_once and decomposition.reconstructs_whole
            for decomposition in self.one_decompositions
        )
        blocking_works = bool(self.blocked_attempts) and not self.permitted_attempts
        return {
            AcceptanceItem.ZERO_RECONSTRUCTS_EXACTLY: zero_holds,
            AcceptanceItem.ZERO_ASSIGNS_NO_POSITIVE_ROLE: zero_is_neutral,
            AcceptanceItem.ONE_PRODUCES_MULTIPLE_HYPOTHESES: multiple,
            AcceptanceItem.NO_SLOT_SILENTLY_DROPPED: no_dropped,
            AcceptanceItem.PART_IDENTITY_IS_DISTINCT_FROM_LINEAGE: distinct_identity,
            AcceptanceItem.SAME_ENTITY_RESCALING_PRESERVES_IDENTITY: (
                rescaling_preserves
            ),
            AcceptanceItem.BRANCH_BIRTH_IS_UNAVAILABLE_HERE: births_deferred,
            AcceptanceItem.UNPROVED_ROLE_BASIS_BLOCKS_PROMOTION: role_basis_blocks,
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
            self.self_defined_contract_reading.does_not_establish,
            STRUCTURAL_OPERATOR_PROOF_IS_ONLY_ELIGIBLE_FOR_FIBER_INTEGRATION,
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
    ascent = ascend_one_slot(
        whole,
        added_token,
        mode=IdentityTransitionMode.SAME_ENTITY_RESCALING,
    )
    one_hypotheses = enumerate_shape_partitions(ascent.after)
    decompositions = tuple(
        decompose(ascent.after, hypothesis) for hypothesis in one_hypotheses.hypotheses
    )
    attempts: list[PromotionAttempt] = []
    for decomposition in decompositions:
        core = decomposition.part_of(SlotRole.CORE)
        deferred = (
            None
            if core.is_empty
            else request_part_branch_birth(decomposition, SlotRole.CORE)
        )
        attempts.append(
            PromotionAttempt(
                decomposition_id=decomposition.decomposition_id,
                standing=decomposition.promotion_standing,
                refusal=(
                    "بقيّةٌ حاجبةٌ تمنع الترقية"
                    if decomposition.promotion_standing
                    is PromotionStanding.PROMOTION_BLOCKED
                    else "لا ترقيةَ في هذا الطور بلا شهادةٍ خارجيّة"
                ),
                deferred_birth=deferred,
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
