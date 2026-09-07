"""A reference to one file carried inside a bound repository snapshot.

`RepositoryFile = SourceFragmentCarrier`: an artifact is a carrier of
possible evidence, never evidence itself
(`RepositoryArtifactIsNotEvidenceByItself`). Naming a file, even one whose
content a future claim will cite, proves nothing about that claim; only an
explicit `EvidenceBinding` between a fragment and a claim can do that, and
no such binding exists in this module.

Like `RepositorySnapshotRef.tree_sha`, `blob_sha` is caller-supplied here:
this module proves only `RepositoryVersionIsExplicitlyAddressed`
(`artifact_path` and `blob_sha` are non-blank and anchored to a snapshot),
never `RepositoryVersionIsContentAuthenticated` -- that `blob_sha` is truly
the blob found at `artifact_path` in that snapshot's tree. That
authentication remains `DEFERRED` to a future `RepositoryObservationAuthority`.
"""

from __future__ import annotations

from dataclasses import dataclass

from .repository_snapshot import (
    RepositorySnapshotRef,
    SelfObservationContractError,
    _require_text,
)


@dataclass(frozen=True, slots=True)
class RepositoryArtifactRef:
    """An opaque reference to one file within one bound repository snapshot.

    The artifact is anchored to its exact `RepositorySnapshotRef`: the same
    `artifact_path` at a different commit names a different, unrelated
    occurrence of this contract, never the same one re-observed.
    """

    snapshot: RepositorySnapshotRef
    artifact_path: str
    blob_sha: str

    def __post_init__(self) -> None:
        if not isinstance(self.snapshot, RepositorySnapshotRef):
            raise SelfObservationContractError(
                "repository artifact ref requires a RepositorySnapshotRef"
            )
        _require_text(self.artifact_path, "repository artifact path")
        _require_text(self.blob_sha, "repository artifact blob sha")
