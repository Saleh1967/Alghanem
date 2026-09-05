"""Structural bindings between claims and evidence records."""

from dataclasses import dataclass

from .evidence import Claim, Evidence


@dataclass(frozen=True, slots=True)
class ClaimEvidenceBinding:
    """A claim together with evidence records bound to it.

    This structural binding is not proof sufficiency.
    """

    claim: Claim
    evidence: tuple[Evidence, ...]

    def __post_init__(self) -> None:
        if not self.evidence:
            raise ValueError("a certificate requires evidence")
        if any(evidence.claim != self.claim for evidence in self.evidence):
            raise ValueError("evidence records must be bound to the binding claim")


Certificate = ClaimEvidenceBinding
