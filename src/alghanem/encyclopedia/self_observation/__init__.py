"""Repository self-observation contracts: rendered as observable source only.

`Repository != KnowledgeAboutRepository`: every contract in this package is
a pure observation of the `Alghanem` repository as a `SourceArtifact` --
never a claim, evidence binding, or knowledge state about it. No module here
defines a `Claim`, `EvidenceRoleCandidate`, or `SelfKnowledge` runtime; those
remain a later, separate milestone (`SelfKnowledgeBridgeExperiment`) built on
top of these references, once a claim/evidence constitution exists.

Governing laws (see `docs/CONSTITUTION.md`, Encyclopedia Self-Observation):

- `RepositorySnapshotIsNotKnowledge`
- `RepositoryArtifactIsNotEvidenceByItself`
- `DocumentationIsNotImplementation`
- `TestPassIsNotUniversalTruth`
- `SelfModelIsNotSystem`
- `SelfDescriptionDoesNotGrantAuthority`
- `RepositoryVersionMustBeContentBound`
- `RepositoryVersionIsExplicitlyAddressed`
- `RepositoryVersionIsContentAuthenticated` (DECLARED_DEFERRED)
- `SameRepositoryIdentity`
- `DifferentCommitsIsNotHistoricalTransition` (DECLARED_DEFERRED)
- `ArtifactChangeRecordsBothSides`
"""

from .artifact_change_ref import RepositoryArtifactChangeRef
from .artifact_ref import RepositoryArtifactRef
from .authenticated_artifact import AuthenticatedRepositoryArtifact
from .authenticated_fragment import AuthenticatedRepositoryFragment
from .authenticated_snapshot import AuthenticatedRepositorySnapshot
from .authenticated_transition import AuthenticatedRepositoryTransition
from .fragment_ref import RepositoryFragmentRef
from .observation_authority import RepositoryObservationAuthority
from .observation_provider import RepositoryObservationProvider
from .observation_request import RepositoryObservationRequest
from .observation_run import RepositoryObservationRun
from .repository_snapshot import (
    RepositorySnapshotRef,
    SelfObservationContractError,
)
from .repository_transition import RepositoryTransitionRef

__all__ = [
    "RepositoryArtifactChangeRef",
    "RepositoryArtifactRef",
    "AuthenticatedRepositoryArtifact",
    "AuthenticatedRepositoryFragment",
    "AuthenticatedRepositorySnapshot",
    "AuthenticatedRepositoryTransition",
    "RepositoryFragmentRef",
    "RepositoryObservationAuthority",
    "RepositoryObservationProvider",
    "RepositoryObservationRequest",
    "RepositoryObservationRun",
    "RepositorySnapshotRef",
    "RepositoryTransitionRef",
    "SelfObservationContractError",
]
