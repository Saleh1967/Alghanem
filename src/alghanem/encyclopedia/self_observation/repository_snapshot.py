"""An explicitly-addressed reference to one state of the `Alghanem` repository.

`RepositorySnapshotRef` deliberately says only:

    We are talking about this exact state of the repository.

It does not say that state is architecturally sound, that any law it seems
to display holds universally, or that constructing this reference proves
anything about the repository beyond its own identity
(`RepositorySnapshotIsNotKnowledge`). It is the first, weakest link of:

    RepositorySnapshot -> Evidence -> Claim -> EpistemicLicensing
    -> SelfKnowledge

and carries no evidence, claim, or knowledge field of its own.

`RepositoryVersionMustBeContentBound` is the constitutional requirement
that grounds a claim only in an explicit version, never a bare branch name
(`Claim(C, Repository@commit_sha)`, never `Claim(C, Repository in
general)`). This module only makes a version *explicitly addressed*
(`RepositoryVersionIsExplicitlyAddressed`): every field is a caller-supplied
string, and no authority here checks that `tree_sha` is genuinely the tree
of `commit_sha`, or that `commit_sha` actually exists in
`repository_identity`. Content authentication
(`RepositoryVersionIsContentAuthenticated`) is deliberately `DEFERRED` to a
future `RepositoryObservationAuthority`, exactly as `FrozenFactorRef` in
`src/alghanem/kernel/fractal.py` is constructible by hand today without
proving a genuine freeze occurred: `Identifier != EvidenceOfIdentity`.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..inquiry import EncyclopediaContractError


class SelfObservationContractError(EncyclopediaContractError):
    """A malformed self-observation contract cannot enter a future runtime."""


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise SelfObservationContractError(f"{field_name} must be non-blank")


def _require_same_repository_distinct_commits(
    from_snapshot: RepositorySnapshotRef,
    to_snapshot: RepositorySnapshotRef,
    field_description: str,
) -> None:
    """Shared `SameRepositoryIdentity` + distinct-commit coherence check.

    Used by both `RepositoryArtifactChangeRef` and `RepositoryTransitionRef`
    so a before/after pair is coherent even outside a transition, without
    duplicating the same two checks in each module.
    """

    if from_snapshot.repository_identity != to_snapshot.repository_identity:
        raise SelfObservationContractError(
            f"{field_description} requires the same repository_identity "
            "on both sides"
        )
    if from_snapshot.commit_sha == to_snapshot.commit_sha:
        raise SelfObservationContractError(
            f"{field_description} requires distinct commit shas"
        )


@dataclass(frozen=True, slots=True)
class RepositorySnapshotRef:
    """An opaque reference to one exact, explicitly-addressed repository state.

    `KnowledgeAboutMain` (an unversioned branch name) never grounds a claim;
    only `Claim(C, Repository@commit_sha)` does, satisfying the
    constitutional requirement `RepositoryVersionMustBeContentBound`. Two
    refs with the same `repository_identity` but different `commit_sha`
    name two distinct, equally valid states: a later commit never erases
    what was true of an earlier one (`RevisionDoesNotEraseHistoricalFreeze`).

    Construction here only proves `RepositoryVersionIsExplicitlyAddressed`:
    the triple is well-formed and non-blank. It never proves
    `RepositoryVersionIsContentAuthenticated` -- that `tree_sha` is really
    the tree of `commit_sha` in `repository_identity` -- which remains
    `DEFERRED` until a future `RepositoryObservationAuthority` exists.
    """

    repository_identity: str
    commit_sha: str
    tree_sha: str

    def __post_init__(self) -> None:
        _require_text(self.repository_identity, "repository identity")
        _require_text(self.commit_sha, "repository commit sha")
        _require_text(self.tree_sha, "repository tree sha")
