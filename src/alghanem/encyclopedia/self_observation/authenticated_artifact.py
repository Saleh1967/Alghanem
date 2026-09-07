"""Authority-issued authenticated repository artifacts."""

from __future__ import annotations

from dataclasses import dataclass

from .authenticated_snapshot import _AUTHORITY_TOKEN, AuthenticatedRepositorySnapshot
from .observation_run import RepositoryObservationRun
from .repository_snapshot import SelfObservationContractError, _require_text


@dataclass(frozen=True, slots=True, init=False)
class AuthenticatedRepositoryArtifact:
    snapshot: AuthenticatedRepositorySnapshot
    artifact_path: str
    blob_sha: str
    observation_run: RepositoryObservationRun

    def __init__(
        self, snapshot, artifact_path, blob_sha, observation_run, *, _token=None
    ):
        if _token is not _AUTHORITY_TOKEN:
            raise SelfObservationContractError(
                "authenticated artifacts may only be issued by the observation "
                "authority"
            )
        if not isinstance(snapshot, AuthenticatedRepositorySnapshot):
            raise SelfObservationContractError(
                "authenticated artifact requires an authenticated snapshot"
            )
        _require_text(artifact_path, "authenticated artifact path")
        _require_text(blob_sha, "authenticated artifact blob sha")
        if observation_run != snapshot.observation_run:
            raise SelfObservationContractError(
                "artifact and snapshot must share an observation run"
            )
        object.__setattr__(self, "snapshot", snapshot)
        object.__setattr__(self, "artifact_path", artifact_path)
        object.__setattr__(self, "blob_sha", blob_sha)
        object.__setattr__(self, "observation_run", observation_run)

    @classmethod
    def _issue(cls, snapshot, artifact_path, blob_sha, run):
        return cls(snapshot, artifact_path, blob_sha, run, _token=_AUTHORITY_TOKEN)
