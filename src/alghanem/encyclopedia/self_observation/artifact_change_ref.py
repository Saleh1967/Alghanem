"""A reference to one artifact's before/after pair across a transition.

Recording only an `after` artifact for a "changed" file discards the
information needed to reconstruct a delta: it says only that the file
exists in the new snapshot and was labeled changed by some external
process. `RepositoryArtifactChangeRef` instead keeps both ends bound to
their own snapshot, so a future claim about *what* changed always has both
sides available.

`ArtifactChangeRefIsContextDependent` does not hold here: this contract
enforces its own minimal snapshot coherence directly, rather than relying
on a later `RepositoryTransitionRef` to reject a mismatched pair. It does
not attempt to prove `Ancestor(before, after)`; it only refuses to pair two
artifacts that plainly cannot belong to the same before/after move, namely
one from a different repository or the same commit on both sides.
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
    a change. `before.snapshot` and `after.snapshot` must share the same
    `repository_identity` and name distinct `commit_sha`s: pairing artifacts
    from two different repositories, or from the same commit, is rejected
    here directly rather than left to a later `RepositoryTransitionRef`.
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
        if (
            self.before.snapshot.repository_identity
            != self.after.snapshot.repository_identity
        ):
            raise SelfObservationContractError(
                "repository artifact change requires the same "
                "repository_identity on both sides"
            )
        if self.before.snapshot.commit_sha == self.after.snapshot.commit_sha:
            raise SelfObservationContractError(
                "repository artifact change requires distinct before/after "
                "snapshot commit shas"
            )

    @property
    def artifact_path(self) -> str:
        """Return the shared artifact path of both sides of the change."""

        return self.after.artifact_path
