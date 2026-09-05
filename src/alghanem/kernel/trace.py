"""Immutable traces of declared events."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Trace:
    """An ordered, immutable record without interpretive meaning."""

    events: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.events or any(not event.strip() for event in self.events):
            raise ValueError("a trace requires at least one non-empty event")
