"""Anchors and states."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Anchor:
    """A named reference in an explicitly declared domain."""

    identifier: str
    domain: str

    def __post_init__(self) -> None:
        if not self.identifier or not self.domain:
            raise ValueError("an anchor requires an identifier and domain")


@dataclass(frozen=True, slots=True)
class State:
    """Opaque state associated with a transition, without assumed semantics."""

    value: object
