"""Raw surface observations, before any interpretation."""

from __future__ import annotations

from dataclasses import dataclass

from .measurement import MeasurementRunIdentity


@dataclass(frozen=True)
class ObservationProvenance:
    """Run-scoped occurrence identity supplied by the measurement protocol."""

    run_identity: MeasurementRunIdentity
    source_id: str
    occurrence_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.run_identity, MeasurementRunIdentity):
            raise ValueError(
                "an observation provenance must include a measurement run identity"
            )
        if not isinstance(self.source_id, str) or not self.source_id:
            raise ValueError("an observation source id must be a non-empty string")
        if not isinstance(self.occurrence_id, str) or not self.occurrence_id:
            raise ValueError("an observation occurrence id must be a non-empty string")


@dataclass(frozen=True)
class RawSurfaceObservation:
    """An observed non-empty Unicode surface with no linguistic classification."""

    provenance: ObservationProvenance
    surface: str

    def __post_init__(self) -> None:
        if not isinstance(self.surface, str) or not self.surface:
            raise ValueError("an observed surface must be a non-empty string")
