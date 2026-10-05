"""The sole authority for opening repository observation runs."""

from __future__ import annotations

from uuid import uuid4

from .authenticated_artifact import AuthenticatedRepositoryArtifact
from .authenticated_snapshot import AuthenticatedRepositorySnapshot
from .observation_provider import RepositoryObservationProvider
from .observation_request import RepositoryObservationRequest
from .observation_run import _RUN_TOKEN, RepositoryObservationRun


class RepositoryObservationAuthority:
    def __init__(self, provider: RepositoryObservationProvider) -> None:
        self._provider = provider

    def open_run(self) -> RepositoryObservationRun:
        """Open one execution scope for one or more related observations."""

        return RepositoryObservationRun(
            run_id=str(uuid4()),
            provider_identity=self._provider.provider_identity,
            implementation_identity=self._provider.implementation_identity,
            protocol_version=self._provider.protocol_version,
            provider=self._provider,
            _token=_RUN_TOKEN,
        )

    def observe(
        self, request: RepositoryObservationRequest
    ) -> tuple[
        AuthenticatedRepositorySnapshot, tuple[AuthenticatedRepositoryArtifact, ...]
    ]:
        """Observe one request in a single-shot run and return its artifacts.

        Use :meth:`open_run` when authenticated artifacts, fragments, or
        transitions must remain available in the same execution scope.
        """

        run = self.open_run()
        snapshot = run.observe_snapshot(request.requested_snapshot)
        artifacts = tuple(
            run.observe_artifact(snapshot, artifact)
            for artifact in request.requested_artifacts
        )
        return snapshot, artifacts
