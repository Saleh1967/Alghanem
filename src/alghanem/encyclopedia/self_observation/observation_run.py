"""Immutable provenance for one authority execution."""

from __future__ import annotations

from dataclasses import dataclass

from .repository_snapshot import SelfObservationContractError, _require_text


@dataclass(frozen=True, slots=True)
class RepositoryObservationRun:
    run_id: str
    provider_identity: str
    implementation_identity: str
    protocol_version: str
    requested_refs: object

    def __post_init__(self) -> None:
        for value, name in (
            (self.run_id, "run id"),
            (self.provider_identity, "provider identity"),
            (self.implementation_identity, "implementation identity"),
            (self.protocol_version, "protocol version"),
        ):
            _require_text(value, name)

