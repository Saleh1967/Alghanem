"""Small certificates for declared transition properties."""

from dataclasses import dataclass

from .evidence import Claim, Evidence


@dataclass(frozen=True, slots=True)
class Certificate:
    """A claim together with the evidence supplied to support it."""

    claim: Claim
    evidence: tuple[Evidence, ...]

    def __post_init__(self) -> None:
        if not self.evidence:
            raise ValueError("a certificate requires evidence")
