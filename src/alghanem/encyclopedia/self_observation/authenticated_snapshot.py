"""Authority-issued authenticated repository snapshots."""

from __future__ import annotations

from dataclasses import dataclass

from .observation_run import RepositoryObservationRun
from .repository_snapshot import RepositorySnapshotRef, SelfObservationContractError

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
        if _token is not _AUTHORITY_TOKEN:
            raise SelfObservationContractError(
                "authenticated snapshots may only be issued by the observation authority"
            )
        if not isinstance(snapshot, RepositorySnapshotRef):
            raise SelfObservationContractError("authenticated snapshot requires a snapshot ref")
        if not isinstance(observation_run, RepositoryObservationRun):
            raise SelfObservationContractError("authenticated snapshot requires an observation run")
        object.__setattr__(self, "snapshot", snapshot)
        object.__setattr__(self, "observation_run", observation_run)

    @classmethod
    def _issue(cls, snapshot: RepositorySnapshotRef, run: RepositoryObservationRun) -> "AuthenticatedRepositorySnapshot":
        return cls(snapshot, run, _token=_AUTHORITY_TOKEN)
