"""Authority-issued authenticated repository snapshots."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .observation_run import RepositoryObservationRun
from .repository_snapshot import RepositorySnapshotRef, SelfObservationContractError


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

        if not isinstance(snapshot, RepositorySnapshotRef):
            raise SelfObservationContractError(
                "authenticated snapshot requires a snapshot ref"
            )
        if not isinstance(observation_run, RepositoryObservationRun):
            raise SelfObservationContractError(
                "authenticated snapshot requires an observation run"
            )
        if not observation_run._accepts_capability(_token):
            raise SelfObservationContractError(
                "authenticated snapshots may only be issued by their observation run"
            )
        object.__setattr__(self, "snapshot", snapshot)
        object.__setattr__(self, "observation_run", observation_run)
