"""Uninterpreted candidates produced by surface normalization."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class SurfaceAtomCandidate:
    """A normalized surface represented as uninterpreted Unicode atoms."""

    normalized_surface: str
    atoms: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.normalized_surface or not self.atoms:
            raise ValueError("a surface candidate must contain normalized atoms")
        if "".join(self.atoms) != self.normalized_surface:
            raise ValueError("candidate atoms must reproduce the normalized surface")
