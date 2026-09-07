"""Authority-issued execution scope for repository observations."""

from __future__ import annotations

from dataclasses import dataclass, field

from .artifact_ref import RepositoryArtifactRef
from .authenticated_artifact import AuthenticatedRepositoryArtifact
from .authenticated_fragment import AuthenticatedRepositoryFragment
from .authenticated_snapshot import AuthenticatedRepositorySnapshot
from .authenticated_transition import AuthenticatedRepositoryTransition
from .observation_provider import RepositoryObservationProvider
from .repository_snapshot import (
    RepositorySnapshotRef,
    SelfObservationContractError,
    _require_text,
)

_RUN_TOKEN = object()


@dataclass(frozen=True, slots=True, init=False)
class RepositoryObservationRun:
    """One authority-owned scope that can authenticate many related refs."""

    run_id: str
    provider_identity: str
    implementation_identity: str
    protocol_version: str
    _provider: RepositoryObservationProvider = field(
        init=False, repr=False, compare=False
    )
    _issuance_capability: object = field(init=False, repr=False, compare=False)

    def __init__(
        self,
        run_id: str,
        provider_identity: str,
        implementation_identity: str,
        protocol_version: str,
        provider: RepositoryObservationProvider,
        *,
        _token: object | None = None,
    ) -> None:
        if _token is not _RUN_TOKEN:
            raise SelfObservationContractError(
                "observation runs may only be issued by the observation authority"
            )
        for value, name in (
            (run_id, "run id"),
            (provider_identity, "provider identity"),
            (implementation_identity, "implementation identity"),
            (protocol_version, "protocol version"),
        ):
            _require_text(value, name)
        object.__setattr__(self, "run_id", run_id)
        object.__setattr__(self, "provider_identity", provider_identity)
        object.__setattr__(self, "implementation_identity", implementation_identity)
        object.__setattr__(self, "protocol_version", protocol_version)
        object.__setattr__(self, "_provider", provider)
        object.__setattr__(self, "_issuance_capability", object())

    def _accepts_capability(self, capability: object | None) -> bool:
        return capability is self._issuance_capability

    def observe_snapshot(
        self, ref: RepositorySnapshotRef
    ) -> AuthenticatedRepositorySnapshot:
        repository = self._provider.resolve_repository(ref.repository_identity)
        commit = (
            None
            if repository is None
            else self._provider.resolve_commit(repository, ref.commit_sha)
        )
        if commit is None or self._provider.tree_for_commit(commit) != ref.tree_sha:
            raise SelfObservationContractError(
                "repository snapshot could not be authenticated"
            )
        return AuthenticatedRepositorySnapshot(
            ref, self, _token=self._issuance_capability
        )

    def observe_artifact(
        self, snapshot: AuthenticatedRepositorySnapshot, ref: RepositoryArtifactRef
    ) -> AuthenticatedRepositoryArtifact:
        if ref.snapshot != snapshot.snapshot or snapshot.observation_run is not self:
            raise SelfObservationContractError(
                "artifact is not anchored to this authenticated snapshot"
            )
        blob = self._provider.blob_at_path(ref.snapshot.tree_sha, ref.artifact_path)
        if blob != ref.blob_sha:
            raise SelfObservationContractError(
                "repository artifact could not be authenticated"
            )
        return AuthenticatedRepositoryArtifact(
            snapshot,
            ref.artifact_path,
            ref.blob_sha,
            self,
            _token=self._issuance_capability,
        )

    def observe_fragment(
        self, artifact: AuthenticatedRepositoryArtifact, locator: str
    ) -> AuthenticatedRepositoryFragment:
        if artifact.observation_run is not self:
            raise SelfObservationContractError(
                "fragment artifact is not owned by this observation run"
            )
        content_id = self._provider.fragment_from_blob(artifact.blob_sha, locator)
        if content_id is None:
            raise SelfObservationContractError(
                "repository fragment could not be authenticated"
            )
        return AuthenticatedRepositoryFragment(
            artifact,
            locator,
            content_id,
            self,
            _token=self._issuance_capability,
        )

    def observe_transition(
        self,
        from_snapshot: AuthenticatedRepositorySnapshot,
        to_snapshot: AuthenticatedRepositorySnapshot,
    ) -> AuthenticatedRepositoryTransition:
        if (
            from_snapshot.observation_run is not self
            or to_snapshot.observation_run is not self
        ):
            raise SelfObservationContractError(
                "transition snapshots must share this observation run"
            )
        from_ref, to_ref = from_snapshot.snapshot, to_snapshot.snapshot
        repository = self._provider.resolve_repository(from_ref.repository_identity)
        if (
            repository is None
            or from_ref.repository_identity != to_ref.repository_identity
            or not self._provider.is_ancestor(
                repository, from_ref.commit_sha, to_ref.commit_sha
            )
        ):
            raise SelfObservationContractError(
                "repository transition ancestry could not be authenticated"
            )
        return AuthenticatedRepositoryTransition(
            from_snapshot,
            to_snapshot,
            self,
            _token=self._issuance_capability,
        )
