"""G0.OB.1 and G0.EB.1's pre-applicability evidence-role boundary.

G0.OB.1 bridges a source-specific authenticated observation into an
authority-issued kernel binding without making the kernel depend on a source
layer. G0.EB.1 then records a proposed role relative to that binding, a
structured claim, and an opaque role reference. Neither milestone decides
applicability, sufficiency, truth, or knowledge.
"""

from __future__ import annotations

from dataclasses import dataclass

from .claim_constitution import ClaimCandidate

_AUTHENTICATED_OBSERVATION_BINDING_TOKEN = object()


def _require_text(value: str, name: str) -> None:
    if type(value) is not str or not value.strip():
        raise ValueError(f"{name} must be non-blank text")


@dataclass(frozen=True, slots=True, init=False)
class AuthenticatedObservationBinding:
    """A kernel binding issued from one source-authenticated observation.

    The source-specific authority owns issuance. Source references identify
    what that authority authenticated; they are not caller assertions of
    authentication and do not decide evidence applicability.
    """

    source_observation_ref: str
    source_authentication_ref: str

    def __init__(
        self,
        source_observation_ref: str,
        source_authentication_ref: str,
        *,
        _token: object | None = None,
    ) -> None:
        if _token is not _AUTHENTICATED_OBSERVATION_BINDING_TOKEN:
            raise ValueError(
                "authenticated observation bindings must be issued through "
                "a source authority"
            )
        _require_text(source_observation_ref, "source observation reference")
        _require_text(source_authentication_ref, "source authentication reference")
        object.__setattr__(self, "source_observation_ref", source_observation_ref)
        object.__setattr__(self, "source_authentication_ref", source_authentication_ref)


def _issue_authenticated_observation_binding(
    source_observation_ref: str, source_authentication_ref: str
) -> AuthenticatedObservationBinding:
    """Issue a binding for use exclusively by a source authority.

    This private module function is intentionally absent from the kernel public
    API. A source-specific authority calls it only after authenticating its own
    observation. This preserves the source-agnostic kernel dependency direction.
    """

    return AuthenticatedObservationBinding(
        source_observation_ref,
        source_authentication_ref,
        _token=_AUTHENTICATED_OBSERVATION_BINDING_TOKEN,
    )


@dataclass(frozen=True, slots=True)
class EvidenceRoleRef:
    """An opaque role reference, not a role semantics or applicability judgment."""

    identifier: str

    def __post_init__(self) -> None:
        _require_text(self.identifier, "evidence role reference")


@dataclass(frozen=True, slots=True)
class EvidenceRoleCandidate:
    """A proposed, claim-relative evidence role before applicability assessment."""

    authenticated_observation_binding: AuthenticatedObservationBinding
    claim: ClaimCandidate
    role: EvidenceRoleRef

    def __post_init__(self) -> None:
        if (
            type(self.authenticated_observation_binding)
            is not AuthenticatedObservationBinding
        ):
            raise TypeError(
                "evidence role candidate requires an authenticated observation binding"
            )
        if type(self.claim) is not ClaimCandidate:
            raise TypeError("evidence role candidate requires a claim candidate")
        if type(self.role) is not EvidenceRoleRef:
            raise TypeError(
                "evidence role candidate requires an evidence role reference"
            )
