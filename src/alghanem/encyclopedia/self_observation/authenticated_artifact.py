"""Authority-issued authenticated repository artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .authenticated_snapshot import _AUTHORITY_TOKEN, AuthenticatedRepositorySnapshot

if TYPE_CHECKING:
    from .observation_run import RepositoryObservationRun
from .repository_snapshot import (
    SelfObservationContractError,
    _require_authority_token,
    _require_text,
)


@dataclass(frozen=True, slots=True, init=False)
class AuthenticatedRepositoryArtifact:
    snapshot: AuthenticatedRepositorySnapshot
    artifact_path: str
    blob_sha: str
    observation_run: RepositoryObservationRun

    def __init__(
        self,
        snapshot: AuthenticatedRepositorySnapshot,
        artifact_path: str,
        blob_sha: str,
        observation_run: RepositoryObservationRun,
        *,
        _token: object | None = None,
    ) -> None:
        _require_authority_token(_token, _AUTHORITY_TOKEN, "authenticated artifacts")
        if not isinstance(snapshot, AuthenticatedRepositorySnapshot):
            raise SelfObservationContractError(
                "authenticated artifact requires an authenticated snapshot"
            )
        _require_text(artifact_path, "authenticated artifact path")
        _require_text(blob_sha, "authenticated artifact blob sha")
        if observation_run is not snapshot.observation_run:
            raise SelfObservationContractError(
                "artifact and snapshot must share an observation run"
            )
        object.__setattr__(self, "snapshot", snapshot)
        object.__setattr__(self, "artifact_path", artifact_path)
        object.__setattr__(self, "blob_sha", blob_sha)
        object.__setattr__(self, "observation_run", observation_run)
