"""`G0.METRIC-0` — خريطةُ القدرات العربية الكسريّة.

المقامُ `DeclaredArabicCapabilityUniverseV1` مُعلَنٌ من خارج التنفيذ، والقدرةُ
غيرُ المبنيّة تبقى فيه صفًّا ظاهرًا بحالة `S0_ABSENT` ومانِعِها وبوّابتها
التالية. والشواهدُ تدخل بمسارات سلطةٍ مُنمَّطة، والشهادةُ تُشتَقّ بالكامل ولا
يُملأ فيها حقلٌ يدويًّا.

ولا سلطةَ لهذه الحزمة: لا تقرؤها بوّابةٌ في `kernel/`، ولا تُولِد ولا تُجمِّد.
"""

from __future__ import annotations

from .aggregate import AggregationError, DerivedRatio, NodeAggregate, aggregate_universe
from .audit import (
    CAPABILITY_FORBIDDEN_PACKAGES,
    CAPABILITY_IMPORT_POLICY,
    CAPABILITY_PERMITTED_MODULES,
    capability_import_isolation_audit,
)
from .blockers import BlockerRow, rank_blockers
from .certificate import (
    COVERAGE_INDICATOR_NAMES,
    ArabicStateCertificate,
    CertificateNodeRow,
    derive_arabic_state_certificate,
)
from .declaration import (
    DECLARATION_PROTOCOL_ID,
    declaration_protocol_digest,
    derive_declaration_evidence,
)
from .evidence import (
    AuthorityPath,
    EvidenceError,
    EvidenceLedger,
    EvidencePolarity,
    EvidenceRefusal,
    EvidenceScope,
    RefusalCode,
    ResidualDisclosure,
    ScopedCapabilityEvidence,
    licensable_gates,
)
from .governance import GovernanceIndicators, derive_governance_indicators
from .laws import (
    A_DECLARED_DENOMINATOR_IS_NOT_THE_COMPLETE_ONTOLOGY_OF_ARABIC,
    A_DENOMINATOR_DERIVED_FROM_THE_IMPLEMENTATION_IS_NOT_A_MEASURE,
    A_RATIO_CARRIES_ITS_DENOMINATOR,
    BREADTH_IS_NOT_READINESS,
    CAPABILITY_LAWS,
    EVIDENCE_MUST_HAVE_AN_AUTHORITY_PATH,
    MISSING_IMPLEMENTATION_DOES_NOT_REMOVE_A_CAPABILITY,
    NO_KERNEL_MODULE_CONSUMES_THE_CAPABILITY_MAP,
    REPEATED_REFERENCE_IS_NOT_INDEPENDENT_EVIDENCE,
    STANDINGS_ARE_GATES_NOT_EPISTEMIC_MAGNITUDES,
    THE_DENOMINATOR_IS_CITED_NOT_INVENTED,
    THE_METRIC_MUST_BE_ALLOWED_TO_GO_DOWN,
    UNIMPLEMENTED_CAPABILITY_MUST_REMAIN_VISIBLE,
)
from .maturity import GATE_SEQUENCE, MaturityStage, blocking_reason_for_gate
from .measure import LeafMeasurement, measure_leaves
from .node import (
    DECLARED_SOURCES,
    CapabilityCitation,
    CapabilityNode,
    CapabilityNodeError,
    DeclaredSource,
    NodeKind,
    Requirement,
)
from .universe import CapabilityUniverse, CapabilityUniverseError, UniverseManifest
from .universe_v1 import (
    ARABIC_TOTAL_ID,
    DECLARED_ARABIC_CAPABILITY_UNIVERSE_V1,
    DECLARED_READINESS_GATE,
    UNIVERSE_V1_ID,
    build_declared_universe_v1,
)

__all__ = [
    "ARABIC_TOTAL_ID",
    "A_DECLARED_DENOMINATOR_IS_NOT_THE_COMPLETE_ONTOLOGY_OF_ARABIC",
    "A_DENOMINATOR_DERIVED_FROM_THE_IMPLEMENTATION_IS_NOT_A_MEASURE",
    "A_RATIO_CARRIES_ITS_DENOMINATOR",
    "BREADTH_IS_NOT_READINESS",
    "CAPABILITY_FORBIDDEN_PACKAGES",
    "CAPABILITY_IMPORT_POLICY",
    "CAPABILITY_LAWS",
    "CAPABILITY_PERMITTED_MODULES",
    "COVERAGE_INDICATOR_NAMES",
    "DECLARATION_PROTOCOL_ID",
    "DECLARED_ARABIC_CAPABILITY_UNIVERSE_V1",
    "DECLARED_READINESS_GATE",
    "DECLARED_SOURCES",
    "EVIDENCE_MUST_HAVE_AN_AUTHORITY_PATH",
    "GATE_SEQUENCE",
    "MISSING_IMPLEMENTATION_DOES_NOT_REMOVE_A_CAPABILITY",
    "NO_KERNEL_MODULE_CONSUMES_THE_CAPABILITY_MAP",
    "REPEATED_REFERENCE_IS_NOT_INDEPENDENT_EVIDENCE",
    "STANDINGS_ARE_GATES_NOT_EPISTEMIC_MAGNITUDES",
    "THE_DENOMINATOR_IS_CITED_NOT_INVENTED",
    "THE_METRIC_MUST_BE_ALLOWED_TO_GO_DOWN",
    "UNIMPLEMENTED_CAPABILITY_MUST_REMAIN_VISIBLE",
    "UNIVERSE_V1_ID",
    "AggregationError",
    "ArabicStateCertificate",
    "AuthorityPath",
    "BlockerRow",
    "CapabilityCitation",
    "CapabilityNode",
    "CapabilityNodeError",
    "CapabilityUniverse",
    "CapabilityUniverseError",
    "CertificateNodeRow",
    "DeclaredSource",
    "DerivedRatio",
    "EvidenceError",
    "EvidenceLedger",
    "EvidencePolarity",
    "EvidenceRefusal",
    "EvidenceScope",
    "GovernanceIndicators",
    "LeafMeasurement",
    "MaturityStage",
    "NodeAggregate",
    "NodeKind",
    "RefusalCode",
    "Requirement",
    "ResidualDisclosure",
    "ScopedCapabilityEvidence",
    "UniverseManifest",
    "aggregate_universe",
    "blocking_reason_for_gate",
    "build_declared_universe_v1",
    "capability_import_isolation_audit",
    "declaration_protocol_digest",
    "derive_arabic_state_certificate",
    "derive_declaration_evidence",
    "derive_governance_indicators",
    "licensable_gates",
    "measure_leaves",
    "rank_blockers",
]
