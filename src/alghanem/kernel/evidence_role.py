"""G0.EB.1's pre-sufficiency constitution of claim-relative evidence roles.

An authenticated observation is not evidence by itself.  A
``EvidenceRoleCandidate`` records only that one authenticated observation is
being considered in relation to one structured claim.  It does not decide
applicability, sufficiency, truth, or knowledge.
"""

from __future__ import annotations

from dataclasses import dataclass

from .claim_constitution import ClaimCandidate


def _require_text(value: str, name: str) -> None:
    if type(value) is not str or not value.strip():
        raise ValueError(f"{name} must be non-blank text")


@dataclass(frozen=True, slots=True)
class AuthenticatedObservation:
    """An observation identified with the authentication that attests to it.

    The identifiers are opaque references.  They do not assert that the
    observation applies to any claim, nor do they decide its evidential force.
    """

    observation_id: str
    authentication_id: str

    def __post_init__(self) -> None:
        _require_text(self.observation_id, "observation id")
        _require_text(self.authentication_id, "observation authentication id")


@dataclass(frozen=True, slots=True)
class EvidenceRoleCandidate:
    """One proposed evidence role, relative to one observation and one claim.

    This is a structural pairing only.  ``EvidenceRoleCandidate`` is neither
    an applicability judgment nor an evidence-sufficiency, truth, or knowledge
    judgment.
    """

    observation: AuthenticatedObservation
    claim: ClaimCandidate

    def __post_init__(self) -> None:
        if type(self.observation) is not AuthenticatedObservation:
            raise TypeError(
                "evidence role candidate requires an authenticated observation"
            )
        if type(self.claim) is not ClaimCandidate:
            raise TypeError("evidence role candidate requires a claim candidate")
