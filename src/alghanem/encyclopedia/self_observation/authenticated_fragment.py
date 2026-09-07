"""Authority-issued authenticated repository fragments."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .authenticated_artifact import AuthenticatedRepositoryArtifact
from .authenticated_snapshot import _AUTHORITY_TOKEN

if TYPE_CHECKING:
    from .authenticated_artifact import AuthenticatedRepositoryArtifact
    from .observation_run import RepositoryObservationRun
from .repository_snapshot import SelfObservationContractError, _require_text


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
        if _token is not _AUTHORITY_TOKEN:
            raise SelfObservationContractError(
                "authenticated fragments may only be issued by the observation "
                "authority"
            )
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
        object.__setattr__(self, "artifact", artifact)
        object.__setattr__(self, "fragment_locator", fragment_locator)
        object.__setattr__(self, "fragment_content_id", fragment_content_id)
        object.__setattr__(self, "observation_run", observation_run)
