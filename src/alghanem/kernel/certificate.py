"""Small certificates for declared transition properties."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Certificate:
    """A certificate records a claim supported by supplied evidence."""

    statement: str

    def __post_init__(self) -> None:
        if not self.statement:
            raise ValueError("a certificate requires a statement")
