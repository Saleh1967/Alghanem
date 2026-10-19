"""Internal G0.OB.1 binding and bridge for source observation authorities.

This module belongs to the explicit internal adapter namespace, excluded from
the public kernel API. Source adapters invoke it only after their own
authority has authenticated an observation. Ordinary callers consume the
resulting binding but cannot issue one through ``alghanem.kernel``.
Python's internal-module and private-token conventions are a controlled API
boundary, not cryptographic protection against deliberate private access.
"""

from dataclasses import dataclass

from .text import require_text

_AUTHENTICATED_OBSERVATION_BINDING_TOKEN = object()


@dataclass(frozen=True, slots=True, init=False)
class AuthenticatedObservationBinding:
    """A source-bound authenticated coordinate issued by a source authority."""

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
        require_text(source_observation_ref, "source observation reference")
        require_text(source_authentication_ref, "source authentication reference")
        object.__setattr__(self, "source_observation_ref", source_observation_ref)
        object.__setattr__(self, "source_authentication_ref", source_authentication_ref)


def issue_from_source_authority(
    source_observation_ref: str, source_authentication_ref: str
) -> AuthenticatedObservationBinding:
    """Issue a kernel binding from a source authority's authenticated observation."""

    return AuthenticatedObservationBinding(
        source_observation_ref,
        source_authentication_ref,
        _token=_AUTHENTICATED_OBSERVATION_BINDING_TOKEN,
    )
