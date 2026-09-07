"""Authority-issued authenticated historical transitions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .authenticated_snapshot import _AUTHORITY_TOKEN, AuthenticatedRepositorySnapshot

if TYPE_CHECKING:
    from .observation_run import RepositoryObservationRun
from .repository_snapshot import SelfObservationContractError


@dataclass(frozen=True, slots=True, init=False)
class AuthenticatedRepositoryTransition:
    from_snapshot: AuthenticatedRepositorySnapshot
    to_snapshot: AuthenticatedRepositorySnapshot
    observation_run: RepositoryObservationRun

    def __init__(
        self,
        from_snapshot: AuthenticatedRepositorySnapshot,
        to_snapshot: AuthenticatedRepositorySnapshot,
        observation_run: RepositoryObservationRun,
        *,
        _token: object | None = None,
    ) -> None:
        if _token is not _AUTHORITY_TOKEN:
            raise SelfObservationContractError(
                "authenticated transitions may only be issued by the "
                "observation authority"
            )
        if not isinstance(
            from_snapshot, AuthenticatedRepositorySnapshot
        ) or not isinstance(to_snapshot, AuthenticatedRepositorySnapshot):
            raise SelfObservationContractError(
                "transition requires authenticated snapshots"
            )
        if (
            from_snapshot.snapshot.repository_identity
            != to_snapshot.snapshot.repository_identity
        ):
            raise SelfObservationContractError(
                "transition snapshots must share a repository"
            )
        if from_snapshot.snapshot.commit_sha == to_snapshot.snapshot.commit_sha:
            raise SelfObservationContractError(
                "transition snapshots must have distinct commits"
            )
        if (
            from_snapshot.observation_run is not observation_run
            or to_snapshot.observation_run is not observation_run
        ):
            raise SelfObservationContractError(
                "transition snapshots must share the observation run"
            )
        object.__setattr__(self, "from_snapshot", from_snapshot)
        object.__setattr__(self, "to_snapshot", to_snapshot)
        object.__setattr__(self, "observation_run", observation_run)
