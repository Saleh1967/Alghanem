"""Authority-issued authenticated repository snapshots."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .observation_run import RepositoryObservationRun
from .repository_snapshot import (
    RepositorySnapshotRef,
    SelfObservationContractError,
    _require_authority_token,
)

_AUTHORITY_TOKEN = object()


@dataclass(frozen=True, slots=True, init=False)
class AuthenticatedRepositorySnapshot:
    snapshot: RepositorySnapshotRef
    observation_run: RepositoryObservationRun

    def __init__(
        self,
        snapshot: RepositorySnapshotRef,
        observation_run: RepositoryObservationRun,
        *,
        _token: object | None = None,
    ) -> None:
        from .observation_run import RepositoryObservationRun

        _require_authority_token(_token, _AUTHORITY_TOKEN, "authenticated snapshots")
        if not isinstance(snapshot, RepositorySnapshotRef):
            raise SelfObservationContractError(
                "authenticated snapshot requires a snapshot ref"
            )
        if not isinstance(observation_run, RepositoryObservationRun):
            raise SelfObservationContractError(
                "authenticated snapshot requires an observation run"
            )
        object.__setattr__(self, "snapshot", snapshot)
        object.__setattr__(self, "observation_run", observation_run)
