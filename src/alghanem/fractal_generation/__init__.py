"""`G0.FGEN-0.SPEC`: نواةُ التوليد الفراكتاليِّ محايدةً عن اللغات.

    Seed
      → ExpansionSet
      → PatternConformance
      → BranchAdjudication
      → ActualTransition
      → MRKClosure
      → LiftGate(DEFER)

**والنواةُ مستقلّةٌ بنيويًّا**: لا تستورد من `alghanem` إلّا `canonical_content`؛
فلا `generation/` ولا `arabic/` ولا `linguistic/` ولا `realization/` ولا
`kernel/`. **والاتّجاهُ الوحيدُ المسموحُ مستقبلًا**:

    ArabicAdapter  →  FractalCore
    FractalCore    ↛  ArabicAdapter

**وقانونُ الاحتواء مُعلَنٌ لا مبرهن**: `LinearGeneration ⊂ FractalGeneration`
قانونٌ معماريٌّ في هذه المرحلة، وإثباتُه التشغيليُّ يأتي مع مُحوِّلٍ لم يُفتَح بعد.

**وسلطةُ الرفع لم تُفتَح**: `ClosedFractalNode ⇏ NextScaleSeed` حالُ هذه المرحلة
لا حكمُ أبد؛ وفجوةُ `RES.FGEN0.NoScaleNecessityAuthority` تحمل شرطَ رفعها.

تسجيلٌ لا سلطة: لا ولادةَ، ولا حكمَ ولادةٍ، ولا تجميدَ `E0`.
"""

from __future__ import annotations

from .authority_gaps import (
    FRACTAL_AUTHORITY_GAPS,
    NO_ARABIC_SPECIALIZATION_AUTHORITY,
    NO_PATTERN_PROOF_WITHOUT_READOUT,
    NO_SCALE_NECESSITY_AUTHORITY,
    NO_SEMANTIC_AUTHORITY_IN_FORMAL_GENERATION,
    FractalAuthorityGap,
    FractalAuthorityGapError,
)
from .branch import (
    A_PUSHOUT_IS_DOCUMENTED_NOT_COMPUTED,
    BranchAdjudicationDecision,
    BranchAdjudicationGate,
    BranchAssessment,
    BranchBirthCandidate,
    BranchError,
    BranchRelation,
    BranchStanding,
    IdentityPreservingTransformationCandidate,
    MovementCandidate,
)
from .closure import (
    ClosedFractalNode,
    ClosureCandidate,
    ClosureDecision,
    ClosureError,
    ClosureGate,
    ClosureRequirement,
    ClosureStatus,
    InvariantAudit,
    MinimumCompleteRequirement,
    ScaleClosureContract,
)
from .expansion import (
    CONFORMANCE_IS_NOT_LICENSING,
    DeclaredDifference,
    ExpansionCandidate,
    ExpansionError,
    ExpansionSet,
    PatternConformanceDecision,
    PatternConformanceGate,
    PatternConformanceStatus,
    PatternConformantDifference,
    ProposalProvenance,
)
from .laws import (
    CANDIDATE_IS_NOT_TRANSITION,
    CLOSED_WITH_AUTHORED_NECESSITY_CLAIM_DOES_NOT_ENTAIL_LIFT,
    CLOSURE_IS_NOT_EXHAUSTION,
    CLOSURE_IS_NOT_LIFT_NECESSITY,
    CLOSURE_IS_NOT_MEANING,
    CLOSURE_IS_NOT_TRUTH,
    DECLARED_DIFFERENCE_IS_NOT_LICENSED_DIFFERENCE,
    FRACTAL_GENERATION_LAW_SET_DIGEST,
    FRACTAL_GENERATION_LAW_SET_ID,
    FRACTAL_GENERATION_LAWS,
    LINEAR_GENERATION_IS_CONTAINED_IN_FRACTAL_GENERATION,
    NO_FORCED_CHOICE_AMONG_CO_ADMISSIBLE_BRANCHES,
    NO_FRACTAL_TRANSITION_WITHOUT_RECONSTRUCTIBLE_TRACE,
    NO_HIGHER_SCALE_WITHOUT_NECESSITY,
    NO_RESIDUAL_ERASURE,
    PATTERN_DECLARATION_IS_NOT_PATTERN_PROOF,
    RESIDUAL_IS_NOT_DISPOSITION,
    RUNTIME_RESIDUAL_IS_NOT_ARCHITECTURAL_AUTHORITY_GAP,
)
from .lift import (
    LiftCandidate,
    LiftDecision,
    LiftError,
    LiftGate,
    LiftStatus,
    NextScaleSeed,
    ScaleExhaustionCandidate,
    ScaleNecessityCertificate,
    ScaleTransitionRequirement,
)
from .node import (
    DO_NOT_STORE_DERIVABLE_IDENTITY_AS_A_SECOND_CLAIM,
    INSTANCE_IDENTITY_IS_NOT_IDENTITY_TYPE,
    FractalContent,
    FractalIdentity,
    FractalNode,
    FractalNodeError,
    FractalNodeRef,
    FractalResidual,
    FractalResidualKind,
    FractalSeed,
)
from .pattern import PatternContract, PatternContractError, PatternRef
from .scale import (
    A_SCALE_REF_IS_RESOLVED_NOT_ASSERTED,
    FractalScaleContract,
    FractalScaleError,
    FractalScaleRef,
    ScaleRelation,
    ScaleRelationEdge,
    ScaleSpace,
)
from .trace import (
    FractalMovementKind,
    FractalTrace,
    FractalTraceError,
    FractalTransition,
    FractalTransitionDecision,
    FractalTransitionGate,
    FractalTransitionTraceStep,
)

__all__ = [
    "A_PUSHOUT_IS_DOCUMENTED_NOT_COMPUTED",
    "A_SCALE_REF_IS_RESOLVED_NOT_ASSERTED",
    "BranchAdjudicationDecision",
    "BranchAdjudicationGate",
    "BranchAssessment",
    "BranchBirthCandidate",
    "BranchError",
    "BranchRelation",
    "BranchStanding",
    "CANDIDATE_IS_NOT_TRANSITION",
    "CLOSED_WITH_AUTHORED_NECESSITY_CLAIM_DOES_NOT_ENTAIL_LIFT",
    "CLOSURE_IS_NOT_EXHAUSTION",
    "CLOSURE_IS_NOT_LIFT_NECESSITY",
    "CLOSURE_IS_NOT_MEANING",
    "CLOSURE_IS_NOT_TRUTH",
    "CONFORMANCE_IS_NOT_LICENSING",
    "ClosedFractalNode",
    "ClosureCandidate",
    "ClosureDecision",
    "ClosureError",
    "ClosureGate",
    "ClosureRequirement",
    "ClosureStatus",
    "DECLARED_DIFFERENCE_IS_NOT_LICENSED_DIFFERENCE",
    "DO_NOT_STORE_DERIVABLE_IDENTITY_AS_A_SECOND_CLAIM",
    "DeclaredDifference",
    "ExpansionCandidate",
    "ExpansionError",
    "ExpansionSet",
    "FRACTAL_AUTHORITY_GAPS",
    "FRACTAL_GENERATION_LAWS",
    "FRACTAL_GENERATION_LAW_SET_DIGEST",
    "FRACTAL_GENERATION_LAW_SET_ID",
    "FractalAuthorityGap",
    "FractalAuthorityGapError",
    "FractalContent",
    "FractalIdentity",
    "FractalMovementKind",
    "FractalNode",
    "FractalNodeError",
    "FractalNodeRef",
    "FractalResidual",
    "FractalResidualKind",
    "FractalScaleContract",
    "FractalScaleError",
    "FractalScaleRef",
    "FractalSeed",
    "FractalTrace",
    "FractalTraceError",
    "FractalTransition",
    "FractalTransitionDecision",
    "FractalTransitionGate",
    "FractalTransitionTraceStep",
    "INSTANCE_IDENTITY_IS_NOT_IDENTITY_TYPE",
    "IdentityPreservingTransformationCandidate",
    "InvariantAudit",
    "LINEAR_GENERATION_IS_CONTAINED_IN_FRACTAL_GENERATION",
    "LiftCandidate",
    "LiftDecision",
    "LiftError",
    "LiftGate",
    "LiftStatus",
    "MinimumCompleteRequirement",
    "MovementCandidate",
    "NO_ARABIC_SPECIALIZATION_AUTHORITY",
    "NO_FORCED_CHOICE_AMONG_CO_ADMISSIBLE_BRANCHES",
    "NO_FRACTAL_TRANSITION_WITHOUT_RECONSTRUCTIBLE_TRACE",
    "NO_HIGHER_SCALE_WITHOUT_NECESSITY",
    "NO_PATTERN_PROOF_WITHOUT_READOUT",
    "NO_RESIDUAL_ERASURE",
    "NO_SCALE_NECESSITY_AUTHORITY",
    "NO_SEMANTIC_AUTHORITY_IN_FORMAL_GENERATION",
    "NextScaleSeed",
    "PATTERN_DECLARATION_IS_NOT_PATTERN_PROOF",
    "PatternConformanceDecision",
    "PatternConformanceGate",
    "PatternConformanceStatus",
    "PatternConformantDifference",
    "PatternContract",
    "PatternContractError",
    "PatternRef",
    "ProposalProvenance",
    "RESIDUAL_IS_NOT_DISPOSITION",
    "RUNTIME_RESIDUAL_IS_NOT_ARCHITECTURAL_AUTHORITY_GAP",
    "ScaleClosureContract",
    "ScaleExhaustionCandidate",
    "ScaleNecessityCertificate",
    "ScaleRelation",
    "ScaleRelationEdge",
    "ScaleSpace",
    "ScaleTransitionRequirement",
]
