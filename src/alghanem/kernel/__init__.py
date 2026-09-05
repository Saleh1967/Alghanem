"""Foundational, language-agnostic kernel types."""

from .anchor import Anchor, State
from .binding import ClaimEvidenceBinding
from .evidence import Claim, Evidence
from .invariant import (
    InvariantExtractionError,
    InvariantExtractorRegistry,
    InvariantObservation,
    InvariantSpec,
    InvariantVerification,
    InvariantVerificationGate,
    UnregisteredExtractorError,
)
from .operation import Operation, OperationResult
from .residual import Residual
from .trace import Trace
from .transition import (
    BranchOriginProvenance,
    CertifiedOutcome,
    DecisionReasonCode,
    NonSuccessDecisionAudit,
    StructuralAdmissionDecision,
    StructuralAdmissionError,
    StructuralAdmissionGate,
    StructuralDecisionStatus,
    StructurallyAdmissibleTransition,
    TransitionCandidate,
    TransitionKind,
)

__all__ = [
    "Anchor",
    "BranchOriginProvenance",
    "CertifiedOutcome",
    "Claim",
    "ClaimEvidenceBinding",
    "DecisionReasonCode",
    "Evidence",
    "InvariantExtractionError",
    "InvariantExtractorRegistry",
    "InvariantObservation",
    "InvariantSpec",
    "InvariantVerification",
    "InvariantVerificationGate",
    "NonSuccessDecisionAudit",
    "StructuralAdmissionError",
    "Operation",
    "OperationResult",
    "Residual",
    "State",
    "StructuralAdmissionDecision",
    "StructuralAdmissionGate",
    "StructuralDecisionStatus",
    "StructurallyAdmissibleTransition",
    "Trace",
    "TransitionCandidate",
    "TransitionKind",
    "UnregisteredExtractorError",
]
