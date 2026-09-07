"""The sole issuer of authenticated repository observations."""

from __future__ import annotations

from uuid import uuid4

from .artifact_ref import RepositoryArtifactRef
from .authenticated_artifact import AuthenticatedRepositoryArtifact
from .authenticated_fragment import AuthenticatedRepositoryFragment
from .authenticated_snapshot import AuthenticatedRepositorySnapshot
from .authenticated_transition import AuthenticatedRepositoryTransition
from .observation_provider import RepositoryObservationProvider
from .observation_request import RepositoryObservationRequest
from .observation_run import RepositoryObservationRun
from .repository_snapshot import SelfObservationContractError


class RepositoryObservationAuthority:
    def __init__(self, provider: RepositoryObservationProvider) -> None:
        self._provider = provider

    def _run(self, request: RepositoryObservationRequest) -> RepositoryObservationRun:
        return RepositoryObservationRun(
            run_id=str(uuid4()),
            provider_identity=self._provider.provider_identity,
            implementation_identity=self._provider.implementation_identity,
            protocol_version=self._provider.protocol_version,
            requested_refs=(
                request.requested_snapshot,
                *request.requested_artifacts,
            ),
        )

    def observe(
        self, request: RepositoryObservationRequest
    ) -> AuthenticatedRepositorySnapshot:
        run = self._run(request)
        ref = request.requested_snapshot
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
        snapshot = AuthenticatedRepositorySnapshot._issue(ref, run)
        for artifact in request.requested_artifacts:
            self.observe_artifact(snapshot, artifact)
        return snapshot

    def observe_artifact(
        self,
        snapshot: AuthenticatedRepositorySnapshot,
        ref: RepositoryArtifactRef,
    ) -> AuthenticatedRepositoryArtifact:
        if ref.snapshot != snapshot.snapshot:
            raise SelfObservationContractError(
                "artifact is not anchored to the authenticated snapshot"
            )
        blob = self._provider.blob_at_path(
            ref.snapshot.tree_sha, ref.artifact_path
        )
        if blob != ref.blob_sha:
            raise SelfObservationContractError(
                "repository artifact could not be authenticated"
            )
        return AuthenticatedRepositoryArtifact._issue(
            snapshot,
            ref.artifact_path,
            ref.blob_sha,
            snapshot.observation_run,
        )

    def observe_fragment(
        self, artifact: AuthenticatedRepositoryArtifact, locator: str
    ) -> AuthenticatedRepositoryFragment:
        content_id = self._provider.fragment_from_blob(artifact.blob_sha, locator)
        if content_id is None:
            raise SelfObservationContractError(
                "repository fragment could not be authenticated"
            )
        return AuthenticatedRepositoryFragment._issue(
            artifact, locator, content_id, artifact.observation_run
        )

    def observe_transition(
        self,
        from_snapshot: AuthenticatedRepositorySnapshot,
        to_snapshot: AuthenticatedRepositorySnapshot,
    ) -> AuthenticatedRepositoryTransition:
        if from_snapshot.observation_run != to_snapshot.observation_run:
            raise SelfObservationContractError(
                "transition snapshots must share an observation run"
            )
        ref = from_snapshot.snapshot
        to_ref = to_snapshot.snapshot
        repository = self._provider.resolve_repository(ref.repository_identity)
        if (
            repository is None
            or ref.repository_identity != to_ref.repository_identity
            or not self._provider.is_ancestor(
                repository, ref.commit_sha, to_ref.commit_sha
            )
        ):
            raise SelfObservationContractError(
                "repository transition ancestry could not be authenticated"
            )
        return AuthenticatedRepositoryTransition._issue(
            from_snapshot, to_snapshot, from_snapshot.observation_run
        )
