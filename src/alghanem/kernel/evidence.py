"""Claims and the evidence that supports them."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Claim:
    """A proposition kept separate from the evidence for it."""

    statement: str

    def __post_init__(self) -> None:
        if not self.statement:
            raise ValueError("a claim requires a statement")


@dataclass(frozen=True, slots=True)
class Evidence:
    """A record supporting a claim; it is not itself the claim."""

    claim: Claim
    basis: str

    def __post_init__(self) -> None:
        if not self.basis:
            raise ValueError("evidence requires a basis")
