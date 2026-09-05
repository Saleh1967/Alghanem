"""Residuals that remain after an operation."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Residual:
    """An explicit remainder; residuals are not silently discarded."""

    description: str

    def __post_init__(self) -> None:
        if not self.description.strip():
            raise ValueError("a residual requires a description")
