"""A reference to one observed transition between two repository snapshots.

`Change != Improvement`: this contract records only what moved between two
content-bound commits (`c_n -> c_{n+1}`), never that the later state is
better, safer, or more correct. A future `ImprovementClaim` would need its
own evidence; none is implied here.

`DifferentCommits !=> HistoricalTransition`: two distinct commit shas alone
never prove that `to_snapshot` is a genuine, later revision reachable from
`from_snapshot` in the repository's real history (`Ancestor(from, to)`).
This module only proves that both snapshots name the *same repository*
(`SameRepositoryIdentity`) and distinct commits within it; proving true
ancestry is deliberately `DEFERRED` to a future
`RepositoryObservationAuthority`, exactly like content authentication in
`repository_snapshot.py`.
"""

from __future__ import annotations

from dataclasses import dataclass

from .artifact_change_ref import RepositoryArtifactChangeRef
from .artifact_ref import RepositoryArtifactRef
from .repository_snapshot import RepositorySnapshotRef, SelfObservationContractError


def _require_artifact_tuple(
    values: tuple[RepositoryArtifactRef, ...], field_name: str
) -> tuple[str, ...]:
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
    return paths


def _require_artifact_change_tuple(
    values: tuple[RepositoryArtifactChangeRef, ...], field_name: str
) -> tuple[str, ...]:
    if not isinstance(values, tuple) or any(
        not isinstance(value, RepositoryArtifactChangeRef) for value in values
    ):
        raise SelfObservationContractError(
            f"{field_name} must be a tuple of RepositoryArtifactChangeRef values"
        )
    paths = tuple(value.artifact_path for value in values)
    if len(set(paths)) != len(paths):
        raise SelfObservationContractError(
            f"{field_name} must not repeat an artifact path"
        )
    return paths


@dataclass(frozen=True, slots=True)
class RepositoryTransitionRef:
    """An opaque reference to one observed `from_snapshot -> to_snapshot` move.

    `from_snapshot` and `to_snapshot` must share the same
    `repository_identity` (`SameRepositoryIdentity`) and name distinct
    commits: a transition across two different repositories, or with no
    genuine version change, is not a transition. Every `changed_artifacts`
    entry keeps both its `before` (anchored to `from_snapshot`) and `after`
    (anchored to `to_snapshot`) sides; `added_artifacts` is anchored to
    `to_snapshot`; `removed_artifacts` is anchored to `from_snapshot`.
    """

    from_snapshot: RepositorySnapshotRef
    to_snapshot: RepositorySnapshotRef
    changed_artifacts: tuple[RepositoryArtifactChangeRef, ...]
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
        if (
            self.from_snapshot.repository_identity
            != self.to_snapshot.repository_identity
        ):
            raise SelfObservationContractError(
                "repository transition requires the same repository_identity "
                "on both snapshots"
            )
        if self.from_snapshot.commit_sha == self.to_snapshot.commit_sha:
            raise SelfObservationContractError(
                "repository transition requires distinct from/to commit shas"
            )
        changed_paths = _require_artifact_change_tuple(
            self.changed_artifacts, "changed artifacts"
        )
        added_paths = _require_artifact_tuple(self.added_artifacts, "added artifacts")
        removed_paths = _require_artifact_tuple(
            self.removed_artifacts, "removed artifacts"
        )
        if any(
            change.before.snapshot != self.from_snapshot
            for change in self.changed_artifacts
        ):
            raise SelfObservationContractError(
                "changed artifacts' before side must be anchored to from_snapshot"
            )
        if any(
            change.after.snapshot != self.to_snapshot
            for change in self.changed_artifacts
        ):
            raise SelfObservationContractError(
                "changed artifacts' after side must be anchored to to_snapshot"
            )
        if any(
            artifact.snapshot != self.to_snapshot for artifact in self.added_artifacts
        ):
            raise SelfObservationContractError(
                "added artifacts must be anchored to to_snapshot"
            )
        if any(
            artifact.snapshot != self.from_snapshot
            for artifact in self.removed_artifacts
        ):
            raise SelfObservationContractError(
                "removed artifacts must be anchored to from_snapshot"
            )
        all_paths = changed_paths + added_paths + removed_paths
        if len(set(all_paths)) != len(all_paths):
            raise SelfObservationContractError(
                "an artifact path must not appear in more than one of "
                "changed/added/removed artifacts"
            )
