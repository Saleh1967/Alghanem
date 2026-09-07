"""A reference to one artifact's before/after pair across a transition.

Recording only an `after` artifact for a "changed" file discards the
information needed to reconstruct a delta: it says only that the file
exists in the new snapshot and was labeled changed by some external
process. `RepositoryArtifactChangeRef` instead keeps both ends bound to
their own snapshot, so a future claim about *what* changed always has both
sides available.
"""

from __future__ import annotations

from dataclasses import dataclass

from .artifact_ref import RepositoryArtifactRef
from .repository_snapshot import SelfObservationContractError


@dataclass(frozen=True, slots=True)
class RepositoryArtifactChangeRef:
    """An opaque before/after pair naming one ordinary in-place modification.

    `before` and `after` must name the same `artifact_path`: a change in
    path is a distinct identity question (`SameContent+DifferentPath`,
    a candidate rename/move) and is deliberately out of scope here as a
    future `RepositoryArtifactMoveCandidate`. `before.blob_sha` and
    `after.blob_sha` must differ: a pair with no content difference is not
    a change.
    """

    before: RepositoryArtifactRef
    after: RepositoryArtifactRef

    def __post_init__(self) -> None:
        if not isinstance(self.before, RepositoryArtifactRef):
            raise SelfObservationContractError(
                "repository artifact change requires a before RepositoryArtifactRef"
            )
        if not isinstance(self.after, RepositoryArtifactRef):
            raise SelfObservationContractError(
                "repository artifact change requires an after RepositoryArtifactRef"
            )
        if self.before.artifact_path != self.after.artifact_path:
            raise SelfObservationContractError(
                "repository artifact change requires the same artifact_path "
                "on both sides"
            )
        if self.before.blob_sha == self.after.blob_sha:
            raise SelfObservationContractError(
                "repository artifact change requires distinct before/after "
                "blob shas"
            )

    @property
    def artifact_path(self) -> str:
        """Return the shared artifact path of both sides of the change."""

        return self.after.artifact_path
