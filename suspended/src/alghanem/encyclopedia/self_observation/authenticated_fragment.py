"""Authority-issued authenticated repository fragments."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .authenticated_artifact import AuthenticatedRepositoryArtifact

if TYPE_CHECKING:
    from .observation_run import RepositoryObservationRun
from .repository_snapshot import (
    SelfObservationContractError,
    _require_text,
)


@dataclass(frozen=True, slots=True, init=False)
class AuthenticatedRepositoryFragment:
    artifact: AuthenticatedRepositoryArtifact
    fragment_locator: str
    fragment_content_id: str
    observation_run: RepositoryObservationRun

    def __init__(
        self,
        artifact: AuthenticatedRepositoryArtifact,
        fragment_locator: str,
        fragment_content_id: str,
        observation_run: RepositoryObservationRun,
        *,
        _token: object | None = None,
    ) -> None:
        if not isinstance(artifact, AuthenticatedRepositoryArtifact):
            raise SelfObservationContractError(
                "authenticated fragment requires an authenticated artifact"
            )
        _require_text(fragment_locator, "authenticated fragment locator")
        _require_text(fragment_content_id, "authenticated fragment content id")
        if observation_run is not artifact.observation_run:
            raise SelfObservationContractError(
                "fragment and artifact must share an observation run"
            )
        if not observation_run._accepts_capability(_token):
            raise SelfObservationContractError(
                "authenticated fragments may only be issued by their observation run"
            )
        object.__setattr__(self, "artifact", artifact)
        object.__setattr__(self, "fragment_locator", fragment_locator)
        object.__setattr__(self, "fragment_content_id", fragment_content_id)
        object.__setattr__(self, "observation_run", observation_run)

    def source_observation_coordinate(self) -> dict[str, str]:
        """Return all source-observation fields for G0.OB.1 provenance encoding."""

        snapshot = self.artifact.snapshot.snapshot
        return {
            "repository_identity": snapshot.repository_identity,
            "commit_sha": snapshot.commit_sha,
            "artifact_path": self.artifact.artifact_path,
            "fragment_locator": self.fragment_locator,
            "fragment_content_id": self.fragment_content_id,
        }
