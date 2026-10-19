"""Provider boundary for repository observations."""

from __future__ import annotations

from typing import Protocol


class RepositoryObservationProvider(Protocol):
    """Resolve repository addresses without giving the provider authority."""

    provider_identity: str
    implementation_identity: str
    protocol_version: str

    def resolve_repository(self, repository_identity: str) -> object | None: ...

    def resolve_commit(self, repository: object, commit_sha: str) -> object | None: ...

    def tree_for_commit(self, commit: object) -> str | None: ...

    def blob_at_path(self, tree_sha: str, artifact_path: str) -> str | None: ...

    def fragment_from_blob(
        self, blob_sha: str, fragment_locator: str
    ) -> str | None: ...

    def is_ancestor(
        self, repository: object, from_commit_sha: str, to_commit_sha: str
    ) -> bool: ...
