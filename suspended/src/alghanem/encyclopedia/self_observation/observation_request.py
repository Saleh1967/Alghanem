"""Requests for repository observations."""

from __future__ import annotations

from dataclasses import dataclass

from .artifact_ref import RepositoryArtifactRef
from .repository_snapshot import RepositorySnapshotRef, SelfObservationContractError


@dataclass(frozen=True, slots=True)
class RepositoryObservationRequest:
    """Addresses to resolve; construction itself authenticates nothing."""

    requested_snapshot: RepositorySnapshotRef
    requested_artifacts: tuple[RepositoryArtifactRef, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.requested_snapshot, RepositorySnapshotRef):
            raise SelfObservationContractError(
                "observation request requires a RepositorySnapshotRef"
            )
        if not isinstance(self.requested_artifacts, tuple) or any(
            not isinstance(artifact, RepositoryArtifactRef)
            for artifact in self.requested_artifacts
        ):
            raise SelfObservationContractError(
                "requested_artifacts must be a tuple of RepositoryArtifactRef values"
            )
        if any(
            artifact.snapshot != self.requested_snapshot
            for artifact in self.requested_artifacts
        ):
            raise SelfObservationContractError(
                "requested artifacts must be anchored to requested_snapshot"
            )
