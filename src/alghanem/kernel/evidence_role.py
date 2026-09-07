"""G0.OB.1 and G0.EB.1's pre-applicability evidence-role boundary.

G0.OB.1 bridges a source-specific authenticated observation into an
authority-issued kernel binding without making the kernel depend on a source
layer. G0.EB.1 then records a proposed role relative to that binding, a
structured claim, and an opaque role reference. Neither milestone decides
applicability, sufficiency, truth, or knowledge.
"""

from __future__ import annotations

from dataclasses import dataclass

from ._authenticated_observation_bridge import AuthenticatedObservationBinding
from .claim_constitution import ClaimCandidate


def _require_text(value: str, name: str) -> None:
    if type(value) is not str or not value.strip():
        raise ValueError(f"{name} must be non-blank text")


@dataclass(frozen=True, slots=True)
class EvidenceRoleRef:
    """An opaque role reference, not a role semantics or applicability judgment."""

    identifier: str

    def __post_init__(self) -> None:
        _require_text(self.identifier, "evidence role reference")


@dataclass(frozen=True, slots=True)
class EvidenceRoleCandidate:
    """A proposed, claim-relative evidence role before applicability assessment."""

    authenticated_observation_binding: AuthenticatedObservationBinding
    claim: ClaimCandidate
    role: EvidenceRoleRef

    def __post_init__(self) -> None:
        if (
            type(self.authenticated_observation_binding)
            is not AuthenticatedObservationBinding
        ):
            raise TypeError(
                "evidence role candidate requires an authenticated observation binding"
            )
        if type(self.claim) is not ClaimCandidate:
            raise TypeError("evidence role candidate requires a claim candidate")
        if type(self.role) is not EvidenceRoleRef:
            raise TypeError(
                "evidence role candidate requires an evidence role reference"
            )
