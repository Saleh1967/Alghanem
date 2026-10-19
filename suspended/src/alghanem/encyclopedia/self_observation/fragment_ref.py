"""A reference to one candidate evidence fragment inside a repository artifact.

`CodeFragment = EvidenceCandidate`, but `CodeFragment !=> Evidence`: a
fragment only becomes evidence *for a specific claim* once a future
`EvidenceBinding(fragment, claim)` exists. This module deliberately has no
claim or binding field; it names a fragment, and nothing else.
"""

from __future__ import annotations

from dataclasses import dataclass

from .artifact_ref import RepositoryArtifactRef
from .repository_snapshot import SelfObservationContractError, _require_text


@dataclass(frozen=True, slots=True)
class RepositoryFragmentRef:
    """An opaque reference to one located fragment within a bound artifact.

    `fragment_locator` names *where* within the artifact the fragment sits
    (for example a line range or a qualified symbol name); it is an opaque
    key, not semantic evidence about the fragment's content
    (`NoSemanticLabelLeakThroughIdentifiers`, mirrored here from the
    encyclopedia nucleus).
    """

    artifact: RepositoryArtifactRef
    fragment_locator: str
    fragment_content_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.artifact, RepositoryArtifactRef):
            raise SelfObservationContractError(
                "repository fragment ref requires a RepositoryArtifactRef"
            )
        _require_text(self.fragment_locator, "repository fragment locator")
        _require_text(self.fragment_content_id, "repository fragment content id")
