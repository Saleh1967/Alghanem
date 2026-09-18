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
    freeze_system_identity,
)
from .laws import (
    A_FIRST_RUN_HAPPENS_ONCE,
    A_REVEAL_RECORD_IS_NOT_A_VERDICT,
    A_SERIALIZED_CONTRACT_IS_WHAT_THE_READER_RECEIVES,
    A_SYSTEM_NAME_IS_NOT_A_SYSTEM_IDENTITY,
    DIGEST_ONLY_IS_NOT_CRYPTOGRAPHICALLY_HIDDEN_GOLD,
    EVALUATION_LAWS,
    FROZEN_CONTRACT_BEFORE_READERS,
    NO_EVALUATION_VERDICT_BEFORE,
    NO_SYSTEM_DEFINES_THE_CONTRACT_IT_IS_READ_BY,
    OBSERVED_DOMINANCE_IS_BOUNDED_BY_ITS_FROZEN_DOMAIN,
    STATIC_IMPORT_AUDIT_IS_NOT_PROCESS_ISOLATION,
    EvaluationError,
    ProcessConfinementStanding,
)
from .protocol import EvaluationProtocolKind, FrozenEvaluationProtocol
from .report import FrozenRunReport, RunLedger
from .reveal import GoldRevealAuthority, GoldRevealRecord

__all__ = [
    "A_FIRST_RUN_HAPPENS_ONCE",
    "A_REVEAL_RECORD_IS_NOT_A_VERDICT",
    "A_SERIALIZED_CONTRACT_IS_WHAT_THE_READER_RECEIVES",
    "A_SYSTEM_NAME_IS_NOT_A_SYSTEM_IDENTITY",
    "BLIND_PAYLOAD_SCHEME",
    "DIGEST_ONLY_IS_NOT_CRYPTOGRAPHICALLY_HIDDEN_GOLD",
    "EVALUATION_FORBIDDEN_PACKAGES",
    "EVALUATION_IMPORT_POLICY",
    "EVALUATION_LAWS",
    "EVALUATION_PERMITTED_MODULES",
    "FROZEN_CONTRACT_BEFORE_READERS",
    "NO_EVALUATION_VERDICT_BEFORE",
    "NO_SYSTEM_DEFINES_THE_CONTRACT_IT_IS_READ_BY",
    "OBSERVED_DOMINANCE_IS_BOUNDED_BY_ITS_FROZEN_DOMAIN",
    "READER_FORBIDDEN_MODULES",
    "READER_FORBIDDEN_PACKAGES",
    "READER_IMPORT_POLICY",
    "READER_PERMITTED_MODULES",
    "STATIC_IMPORT_AUDIT_IS_NOT_PROCESS_ISOLATION",
    "SYSTEM_IDENTITY_COMPONENTS",
    "BlindPayload",
    "BoundEvaluationRequest",
    "EvaluationBinding",
    "EvaluationError",
    "EvaluationProtocolKind",
    "FrozenEvaluationProtocol",
    "FrozenRunReport",
    "FrozenSystemIdentity",
    "GoldRevealAuthority",
    "GoldRevealRecord",
    "ProcessConfinementDeclaration",
    "ProcessConfinementStanding",
    "RunLedger",
    "evaluation_import_isolation_audit",
    "freeze_system_identity",
    "issue_blind_payload",
    "reader_import_audit",
]
