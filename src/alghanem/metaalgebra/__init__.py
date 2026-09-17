"""الميتا-جبر: لغةُ التمثيل العامّة، قبل أيّ تطبيقٍ عربيّ وفوقَ أيّ لغة.

    Meta-Algebra  ≠  Authority Kernel  ≠  Arabic Instantiation

هذه الحزمةُ تُجمّد **ما يجعل الشيءَ طبقةً**، و**ما يجعل الشيءَ انتقالًا
مرخَّصًا**، و**شرطَ تركيبهما**، ومحورَي المنزلة؛ ولا تحمل طبقةً واحدةً مبنيّة،
ولا تُسمّي لغةً، ولا تُصدِر حكمًا، ولا تستورد من `kernel/` حرفًا ولا من
`arabic/`.

وحداتُها أربع:

* `standing` — محورا المنزلة (`G0.ST`)، ورتبةُ استقلال المواصفة.
* `layer` — `𝒜 = (C, S, Ω, Rel, Inv, Cl, Tr, R)`.
* `transition` — `𝒯 = (D, G, T, P, τ, ρ)` مع شرط التسليم، وقانونُ مَنعِ القفز.
* `composition` — شرطُ التجاور، وفصلُ صحّة المبرهنة عن تغطية تمثيلها.

والمعرّفاتُ لاتينيّةٌ والتوثيقُ عربيٌّ رياضيّ، لأنّ هذه الحزمةَ غيرُ مخصوصةٍ
بالعربيّة وإن كانت العربيّةُ أوّلَ ميادين تمثيلها.
"""

from __future__ import annotations

from .composition import (
    A_CHAIN_IS_NOT_A_PROOF,
    ADJACENCY_IS_A_HYPOTHESIS_NOT_A_CONCLUSION,
    BACKWARD_AUDITABILITY_OBLIGATION,
    COMPOSITION_LAW,
    THEOREM_VALIDITY_IS_NOT_INSTANTIATION_COVERAGE,
    CompositionChain,
    CompositionChainError,
    StepObligation,
)
from .layer import (
    A_LAYER_TYPE_IS_NOT_A_LAYER_ARCHITECTURE,
    A_PARTIAL_OPERATION_DECLARES_WHERE_IT_IS_UNDEFINED,
    CARRIER_IS_NOT_STATE,
    LAYER_COMPONENT_NAMES,
    NO_LAYER_IS_DECLARED_HERE,
    CarrierSpecification,
    ClosureLawSpecification,
    InvariantComponentSpecification,
    LayerSignature,
    LayerSignatureError,
    LicenseRelationSpecification,
    PartialOperationSpecification,
    ResidualSchemaSpecification,
    StateSpaceSpecification,
    TraceObligationSpecification,
)
from .standing import (
    A_CONTRACT_WRITTEN_AFTER_ITS_FUNCTION_IS_NOT_A_CONTRACT,
    EMPIRICAL_TARGET_INDEPENDENCE_IS_EMPIRICAL_ONLY,
    FORMAL_STRUCTURAL_PROOF_IS_NOT_EMPIRICAL_REALITY,
    MISSING_EMPIRICAL_EVIDENCE_IS_NOT_MISSING_STRUCTURAL_PROOF,
    NO_AXIS_COLLAPSE,
    NO_STRUCTURAL_STANDING_WITHOUT_ITS_FROZEN_SIGMA,
    SPECIFICATION_INDEPENDENCE_IS_NOT_EMPIRICAL_TARGET_INDEPENDENCE,
    DualStanding,
    EmpiricalStanding,
    ImplementationConformanceRecord,
    MetaAlgebraStandingError,
    SpecificationIndependenceGrade,
    SpecificationSetRef,
    StructuralStanding,
)
from .transition import (
    CLOSURE_IS_NOT_A_RIGHT_OF_EXIT,
    HANDOFF_LAW,
    NO_JUMP_CONSTRAINS_THE_PATH_NOT_THE_TARGET_MEMBERSHIP,
    NO_JUMP_LAW,
    REQUIRED_AUDIT_CERTIFICATE_FACTS,
    TRANSITION_COMPONENT_NAMES,
    DomainCondition,
    HandoffCondition,
    LicenseGateSpecification,
    PreservationObligation,
    ResidualRankPolicy,
    TransformationSpecification,
    TransitionOutcome,
    TransitionSignature,
    TransitionSignatureError,
    TransitionTraceObligation,
)

__all__ = [
    "ADJACENCY_IS_A_HYPOTHESIS_NOT_A_CONCLUSION",
    "A_CHAIN_IS_NOT_A_PROOF",
    "A_CONTRACT_WRITTEN_AFTER_ITS_FUNCTION_IS_NOT_A_CONTRACT",
    "A_LAYER_TYPE_IS_NOT_A_LAYER_ARCHITECTURE",
    "A_PARTIAL_OPERATION_DECLARES_WHERE_IT_IS_UNDEFINED",
    "BACKWARD_AUDITABILITY_OBLIGATION",
    "CARRIER_IS_NOT_STATE",
    "CLOSURE_IS_NOT_A_RIGHT_OF_EXIT",
    "COMPOSITION_LAW",
    "EMPIRICAL_TARGET_INDEPENDENCE_IS_EMPIRICAL_ONLY",
    "FORMAL_STRUCTURAL_PROOF_IS_NOT_EMPIRICAL_REALITY",
    "HANDOFF_LAW",
    "LAYER_COMPONENT_NAMES",
    "MISSING_EMPIRICAL_EVIDENCE_IS_NOT_MISSING_STRUCTURAL_PROOF",
    "NO_AXIS_COLLAPSE",
    "NO_JUMP_CONSTRAINS_THE_PATH_NOT_THE_TARGET_MEMBERSHIP",
    "NO_JUMP_LAW",
    "NO_LAYER_IS_DECLARED_HERE",
    "NO_STRUCTURAL_STANDING_WITHOUT_ITS_FROZEN_SIGMA",
    "REQUIRED_AUDIT_CERTIFICATE_FACTS",
    "SPECIFICATION_INDEPENDENCE_IS_NOT_EMPIRICAL_TARGET_INDEPENDENCE",
    "THEOREM_VALIDITY_IS_NOT_INSTANTIATION_COVERAGE",
    "TRANSITION_COMPONENT_NAMES",
    "CarrierSpecification",
    "ClosureLawSpecification",
    "CompositionChain",
    "CompositionChainError",
    "DomainCondition",
    "DualStanding",
    "EmpiricalStanding",
    "HandoffCondition",
    "ImplementationConformanceRecord",
    "InvariantComponentSpecification",
    "LayerSignature",
    "LayerSignatureError",
    "LicenseGateSpecification",
    "LicenseRelationSpecification",
    "MetaAlgebraStandingError",
    "PartialOperationSpecification",
    "PreservationObligation",
    "ResidualRankPolicy",
    "ResidualSchemaSpecification",
    "SpecificationIndependenceGrade",
    "SpecificationSetRef",
    "StateSpaceSpecification",
    "StepObligation",
    "StructuralStanding",
    "TraceObligationSpecification",
    "TransformationSpecification",
    "TransitionOutcome",
    "TransitionSignature",
    "TransitionSignatureError",
    "TransitionTraceObligation",
]
