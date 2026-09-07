"""The sole authority for opening repository observation runs."""

from __future__ import annotations

from uuid import uuid4

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
    ) -> AuthenticatedRepositorySnapshot:
        """Compatibility helper that observes a single requested snapshot."""

        run = self.open_run()
        snapshot = run.observe_snapshot(request.requested_snapshot)
        for artifact in request.requested_artifacts:
            run.observe_artifact(snapshot, artifact)
        return snapshot
