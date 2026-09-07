"""A reference to one observed transition between two repository snapshots.

`Change != Improvement`: this contract records only what moved between two
content-bound commits (`c_n -> c_{n+1}`), never that the later state is
better, safer, or more correct. A future `ImprovementClaim` would need its
own evidence; none is implied here.
"""

from __future__ import annotations

from dataclasses import dataclass

from .artifact_ref import RepositoryArtifactRef
from .repository_snapshot import RepositorySnapshotRef, SelfObservationContractError


def _require_artifact_tuple(
    values: tuple[RepositoryArtifactRef, ...], field_name: str
) -> None:
    if not isinstance(values, tuple) or any(
        not isinstance(value, RepositoryArtifactRef) for value in values
    ):
        raise SelfObservationContractError(
            f"{field_name} must be a tuple of RepositoryArtifactRef values"
        )
    paths = tuple(value.artifact_path for value in values)
    if len(set(paths)) != len(paths):
        raise SelfObservationContractError(
            f"{field_name} must not repeat an artifact path"
        )


@dataclass(frozen=True, slots=True)
class RepositoryTransitionRef:
    """An opaque reference to one observed `from_snapshot -> to_snapshot` move.

    Every listed artifact must be anchored to the snapshot side it belongs
    to: `added_artifacts` and `changed_artifacts` are bound to `to_snapshot`,
    `removed_artifacts` is bound to `from_snapshot`. `from_snapshot` and
    `to_snapshot` must name distinct commits: a transition without a genuine
    version change is not a transition.
    """

    from_snapshot: RepositorySnapshotRef
    to_snapshot: RepositorySnapshotRef
    changed_artifacts: tuple[RepositoryArtifactRef, ...]
    added_artifacts: tuple[RepositoryArtifactRef, ...]
    removed_artifacts: tuple[RepositoryArtifactRef, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.from_snapshot, RepositorySnapshotRef):
            raise SelfObservationContractError(
                "repository transition requires a from_snapshot RepositorySnapshotRef"
            )
        if not isinstance(self.to_snapshot, RepositorySnapshotRef):
            raise SelfObservationContractError(
                "repository transition requires a to_snapshot RepositorySnapshotRef"
            )
        if self.from_snapshot.commit_sha == self.to_snapshot.commit_sha:
            raise SelfObservationContractError(
                "repository transition requires distinct from/to commit shas"
            )
        _require_artifact_tuple(self.changed_artifacts, "changed artifacts")
        _require_artifact_tuple(self.added_artifacts, "added artifacts")
        _require_artifact_tuple(self.removed_artifacts, "removed artifacts")
        if any(
            artifact.snapshot != self.to_snapshot
            for artifact in self.changed_artifacts + self.added_artifacts
        ):
            raise SelfObservationContractError(
                "changed and added artifacts must be anchored to to_snapshot"
            )
        if any(
            artifact.snapshot != self.from_snapshot
            for artifact in self.removed_artifacts
        ):
            raise SelfObservationContractError(
                "removed artifacts must be anchored to from_snapshot"
            )
