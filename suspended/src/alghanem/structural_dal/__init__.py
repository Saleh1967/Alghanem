"""`G0.SDAL-0`: جبرُ `StructuralDal` عند `zero-one`، على خاناتٍ مُصطنَعةٍ وحدَها.

    StructuralOperatorProof  →  EligibleForFiberIntegration  →  (مؤجَّل)

هذه الطبقةُ أسبقُ من `DalAsIndicator`: لا مِرساةَ دلالةٍ أُولى، ولا مطابقةَ،
ولا تضمُّنَ، ولا التزامَ، ولا `signified_ref`، ولا `license_ref`. والحدودُ
مفحوصةٌ لا مُصرَّحةٌ فقط:

    zero-one  ↛  signifier_algebra
    zero-one  ↛  maqayis
    zero-one  ↛  madlul
    zero-one  ↛  kernel authority

والترتيبُ المقصود: يُبرهَن الجبرُ أوّلًا، ثمّ يُسقَط على وحداتِ لسانٍ بعينه في
طورٍ لاحقٍ لم يُفتَح بعد. ولا تُعرِّف الأمثلةُ اللغويّةُ الجبرَ.

تسجيلٌ لا سلطة: لا ولادةَ، ولا حكمَ ولادةٍ، ولا دعوى معنًى.
"""

from __future__ import annotations

from .audit import (
    FORBIDDEN_ALGHANEM_PACKAGES,
    FORBIDDEN_NAME_FRAGMENTS,
    PERMITTED_ALGHANEM_MODULES,
    ImportIsolationReport,
    VocabularyAuditReport,
    import_isolation_audit,
    vocabulary_audit,
)
from .hypothesis import (
    PartWholeRelation,
    ShapePartitionHypothesis,
    ShapePartitionHypothesisSet,
    SlotRole,
    StructuralDecomposition,
    StructuralPart,
    ZeroStructuralState,
    decompose,
    enumerate_shape_partitions,
    zero_structural_state,
)
from .induction import (
    ContractOutcome,
    PromotionAttempt,
    SelfDefinedContractReading,
    WeakerModelObservation,
    ZeroOneAlgebraReport,
    prove_zero_one_algebra,
    run_weaker_model,
)
from .laws import (
    BLOCKING_RESIDUAL_FORBIDS_POSITIVE_PROMOTION,
    NO_BRANCH_BIRTH_WITHOUT_EXTERNAL_CERTIFICATE,
    NO_FORCED_WINNER_AMONG_SHAPE_PARTITIONS,
    NO_IMPLICIT_IDENTITY_MODE,
    NO_POSITIVE_STRUCTURE_FROM_NEUTRAL_INPUT,
    NO_SILENT_DROPPED_SLOT,
    PREREGISTRATION_DIGEST,
    SELF_DEFINED_CONTRACT_DOES_NOT_ESTABLISH_COMPARATIVE_STRENGTH,
    SHAPE_PARTITION_HYPOTHESIS_IS_NOT_A_ROOT_CANDIDATE,
    SHAPE_PARTITION_HYPOTHESIS_IS_NOT_A_WEIGHT_CANDIDATE,
    STRUCTURAL_ACCEPTANCE_CONDITIONS,
    STRUCTURAL_BASE_CASE_IS_NOT_A_LINGUISTIC_ROOT_PROOF,
    STRUCTURAL_DAL_LAWS,
    STRUCTURAL_OPERATOR_PROOF_IS_ONLY_ELIGIBLE_FOR_FIBER_INTEGRATION,
    STRUCTURAL_TRANSITION_CONTRACT_FIELDS,
    THE_PART_HAS_ITS_OWN_IDENTITY,
    THE_PART_KEEPS_ITS_PARENT_ANCHOR,
    THE_TRACE_IS_CUMULATIVE_NOT_RECONSTRUCTED,
    UNPROVED_ROLE_BASIS_IS_BLOCKING,
    ZERO_ONE_BOUND,
    AcceptanceItem,
    OutputContractComponent,
    Scale,
    StructuralAcceptanceCondition,
    StructuralDalError,
    condition_named,
)
from .residual import (
    PromotionStanding,
    ResidualClass,
    ResidualReading,
    promotion_standing_of,
    read_residuals,
)
from .slots import StructuralSlot, StructuralWhole, origin_whole
from .transition import (
    DeferredBranchBirth,
    IdentityTransitionAvailability,
    IdentityTransitionMode,
    ScaleAscent,
    StructuralTransition,
    ascend_one_slot,
    availability_of,
    request_part_branch_birth,
)

__all__ = [
    "BLOCKING_RESIDUAL_FORBIDS_POSITIVE_PROMOTION",
    "NO_BRANCH_BIRTH_WITHOUT_EXTERNAL_CERTIFICATE",
    "NO_IMPLICIT_IDENTITY_MODE",
    "NO_POSITIVE_STRUCTURE_FROM_NEUTRAL_INPUT",
    "SELF_DEFINED_CONTRACT_DOES_NOT_ESTABLISH_COMPARATIVE_STRENGTH",
    "STRUCTURAL_OPERATOR_PROOF_IS_ONLY_ELIGIBLE_FOR_FIBER_INTEGRATION",
    "THE_PART_HAS_ITS_OWN_IDENTITY",
    "UNPROVED_ROLE_BASIS_IS_BLOCKING",
    "FORBIDDEN_ALGHANEM_PACKAGES",
    "FORBIDDEN_NAME_FRAGMENTS",
    "NO_FORCED_WINNER_AMONG_SHAPE_PARTITIONS",
    "NO_SILENT_DROPPED_SLOT",
    "PERMITTED_ALGHANEM_MODULES",
    "PREREGISTRATION_DIGEST",
    "SHAPE_PARTITION_HYPOTHESIS_IS_NOT_A_ROOT_CANDIDATE",
    "SHAPE_PARTITION_HYPOTHESIS_IS_NOT_A_WEIGHT_CANDIDATE",
    "STRUCTURAL_ACCEPTANCE_CONDITIONS",
    "STRUCTURAL_BASE_CASE_IS_NOT_A_LINGUISTIC_ROOT_PROOF",
    "STRUCTURAL_DAL_LAWS",
    "STRUCTURAL_TRANSITION_CONTRACT_FIELDS",
    "THE_PART_KEEPS_ITS_PARENT_ANCHOR",
    "THE_TRACE_IS_CUMULATIVE_NOT_RECONSTRUCTED",
    "ZERO_ONE_BOUND",
    "AcceptanceItem",
    "ContractOutcome",
    "DeferredBranchBirth",
    "IdentityTransitionAvailability",
    "IdentityTransitionMode",
    "ImportIsolationReport",
    "OutputContractComponent",
    "PartWholeRelation",
    "PromotionAttempt",
    "PromotionStanding",
    "ResidualClass",
    "ResidualReading",
    "Scale",
    "ScaleAscent",
    "SelfDefinedContractReading",
    "ShapePartitionHypothesis",
    "ShapePartitionHypothesisSet",
    "SlotRole",
    "StructuralAcceptanceCondition",
    "StructuralDalError",
    "StructuralDecomposition",
    "StructuralPart",
    "StructuralSlot",
    "StructuralTransition",
    "StructuralWhole",
    "VocabularyAuditReport",
    "WeakerModelObservation",
    "ZeroOneAlgebraReport",
    "ZeroStructuralState",
    "ascend_one_slot",
    "availability_of",
    "condition_named",
    "decompose",
    "enumerate_shape_partitions",
    "import_isolation_audit",
    "origin_whole",
    "promotion_standing_of",
    "prove_zero_one_algebra",
    "read_residuals",
    "request_part_branch_birth",
    "run_weaker_model",
    "vocabulary_audit",
    "zero_structural_state",
]
