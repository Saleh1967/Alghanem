"""`G0.EVAL-0`: حدُّ تقييمٍ محجوبٌ عن جوابه، مقيَّدُ المصدر، قابلٌ لإعادة التدقيق.

    Frozen Domain Contract
            │
            ├── contract_body_digest
            └── GoldCommitment  =  H(gold ‖ nonce ‖ body_digest ‖ scheme)
                    │
    FrozenSystemIdentity(F₁)   FrozenSystemIdentity(F₂)
                    │
            FrozenEvaluationProtocol
                    │
            BoundEvaluationRequest
                    │
            Serialized Blind Payload
                 F₁       F₂
                  ↓        ↓
            FrozenRunReport₁  FrozenRunReport₂
                    │
            GoldRevealAuthority
                    │
            GoldRevealRecord

ولا مقارنةَ هنا، ولا سيطرة، ولا حكم. والسقفُ سجلُّ فتحٍ مشروط.
"""

from __future__ import annotations

from .audit import (
    EVALUATION_FORBIDDEN_PACKAGES,
    EVALUATION_IMPORT_POLICY,
    EVALUATION_PERMITTED_MODULES,
    evaluation_import_isolation_audit,
)
from .binding import BoundEvaluationRequest, EvaluationBinding
from .boundary import (
    BLIND_PAYLOAD_SCHEME,
    READER_FORBIDDEN_MODULES,
    READER_FORBIDDEN_PACKAGES,
    READER_IMPORT_POLICY,
    READER_PERMITTED_MODULES,
    BlindPayload,
    ProcessConfinementDeclaration,
    issue_blind_payload,
    reader_import_audit,
)
from .identity import (
    SYSTEM_IDENTITY_COMPONENTS,
    FrozenSystemIdentity,
    compose_system_content_id,
    freeze_system_identity,
    measure_configuration_digest,
    measure_dependency_boundary_digest,
    measure_implementation_digest,
)
from .laws import (
    A_FIRST_RUN_HAPPENS_ONCE,
    A_HARNESS_IS_NOT_AN_EXECUTION_AUTHORITY,
    A_RESIDUAL_IS_NAMED_NOT_STRINGLY,
    A_REVEAL_RECORD_IS_NOT_A_VERDICT,
    A_SERIALIZED_CONTRACT_IS_WHAT_THE_READER_RECEIVES,
    A_SYSTEM_NAME_IS_NOT_A_SYSTEM_IDENTITY,
    AN_IN_PROCESS_SEAL_IS_NOT_UNFORGEABLE_PROVENANCE,
    DIGEST_ONLY_IS_NOT_CRYPTOGRAPHICALLY_HIDDEN_GOLD,
    EVALUATION_LAWS,
    FAILURE_IS_RECEIPTED_BUT_NOT_PROMOTED_TO_REFERENCE_RUN,
    FROZEN_CONTRACT_BEFORE_READERS,
    NO_EVALUATION_VERDICT_BEFORE,
    NO_RUN_REPORT_WITHOUT_BOUND_EXECUTION,
    NO_SYSTEM_DEFINES_THE_CONTRACT_IT_IS_READ_BY,
    OBSERVED_DOMINANCE_IS_BOUNDED_BY_ITS_FROZEN_DOMAIN,
    ONLY_EXECUTION_AUTHORITY_ISSUES_EXECUTION_RECEIPTS,
    RECEIPT_ISSUANCE_IS_KEYED_NOT_MERELY_SEALED,
    STATIC_IMPORT_AUDIT_IS_NOT_PROCESS_ISOLATION,
    EvaluationError,
    ProcessConfinementStanding,
)
from .protocol import EvaluationProtocolKind, FrozenEvaluationProtocol
from .provenance import (
    ISSUANCE_SIGNATURE_ALGORITHM,
    IssuanceProvenanceStanding,
    ReceiptIssuanceKey,
)
from .receipt import (
    BoundExecutionReceipt,
    ExecutionExitStatus,
    ExecutionMode,
    verify_receipt_issuance,
)
from .report import FrozenRunReport, RunLedger, report_from_receipt
from .residual import ResidualCode, RunResidual
from .reveal import GoldRevealAuthority, GoldRevealRecord

__all__ = [
    "AN_IN_PROCESS_SEAL_IS_NOT_UNFORGEABLE_PROVENANCE",
    "A_FIRST_RUN_HAPPENS_ONCE",
    "A_HARNESS_IS_NOT_AN_EXECUTION_AUTHORITY",
    "A_RESIDUAL_IS_NAMED_NOT_STRINGLY",
    "A_REVEAL_RECORD_IS_NOT_A_VERDICT",
    "A_SERIALIZED_CONTRACT_IS_WHAT_THE_READER_RECEIVES",
    "A_SYSTEM_NAME_IS_NOT_A_SYSTEM_IDENTITY",
    "BLIND_PAYLOAD_SCHEME",
    "DIGEST_ONLY_IS_NOT_CRYPTOGRAPHICALLY_HIDDEN_GOLD",
    "EVALUATION_FORBIDDEN_PACKAGES",
    "EVALUATION_IMPORT_POLICY",
    "EVALUATION_LAWS",
    "EVALUATION_PERMITTED_MODULES",
    "FAILURE_IS_RECEIPTED_BUT_NOT_PROMOTED_TO_REFERENCE_RUN",
    "FROZEN_CONTRACT_BEFORE_READERS",
    "ISSUANCE_SIGNATURE_ALGORITHM",
    "NO_EVALUATION_VERDICT_BEFORE",
    "NO_RUN_REPORT_WITHOUT_BOUND_EXECUTION",
    "NO_SYSTEM_DEFINES_THE_CONTRACT_IT_IS_READ_BY",
    "OBSERVED_DOMINANCE_IS_BOUNDED_BY_ITS_FROZEN_DOMAIN",
    "ONLY_EXECUTION_AUTHORITY_ISSUES_EXECUTION_RECEIPTS",
    "RECEIPT_ISSUANCE_IS_KEYED_NOT_MERELY_SEALED",
    "READER_FORBIDDEN_MODULES",
    "READER_FORBIDDEN_PACKAGES",
    "READER_IMPORT_POLICY",
    "READER_PERMITTED_MODULES",
    "STATIC_IMPORT_AUDIT_IS_NOT_PROCESS_ISOLATION",
    "SYSTEM_IDENTITY_COMPONENTS",
    "BlindPayload",
    "BoundEvaluationRequest",
    "BoundExecutionReceipt",
    "EvaluationBinding",
    "EvaluationError",
    "EvaluationProtocolKind",
    "ExecutionExitStatus",
    "ExecutionMode",
    "FrozenEvaluationProtocol",
    "FrozenRunReport",
    "FrozenSystemIdentity",
    "GoldRevealAuthority",
    "GoldRevealRecord",
    "IssuanceProvenanceStanding",
    "ProcessConfinementDeclaration",
    "ProcessConfinementStanding",
    "ReceiptIssuanceKey",
    "ResidualCode",
    "RunLedger",
    "RunResidual",
    "compose_system_content_id",
    "evaluation_import_isolation_audit",
    "freeze_system_identity",
    "issue_blind_payload",
    "measure_configuration_digest",
    "measure_dependency_boundary_digest",
    "measure_implementation_digest",
    "reader_import_audit",
    "report_from_receipt",
    "verify_receipt_issuance",
]
