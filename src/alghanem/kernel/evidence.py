"""Claims and evidence records bound to them."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Claim:
    """A proposition kept separate from the evidence for it."""

    claim_id: str
    statement: str

    def __post_init__(self) -> None:
        if not self.claim_id.strip() or not self.statement.strip():
            raise ValueError("a claim requires a claim id and statement")


@dataclass(frozen=True, slots=True)
class Evidence:
    """A record bound to a claim; binding is not proof sufficiency."""

    claim_id: str
    basis: str

    def __post_init__(self) -> None:
        if not self.claim_id.strip() or not self.basis.strip():
            raise ValueError("evidence requires a claim id and basis")
