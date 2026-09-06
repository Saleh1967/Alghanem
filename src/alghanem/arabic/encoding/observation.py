"""Raw surface observations, before any interpretation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RawSurfaceObservation:
    """An observed non-empty Unicode surface with no linguistic classification."""

    surface: str

    def __post_init__(self) -> None:
        if not isinstance(self.surface, str) or not self.surface:
            raise ValueError("an observed surface must be a non-empty string")
