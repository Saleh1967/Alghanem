"""Internal G0.OB.1 binding and bridge for source observation authorities.

This module is intentionally excluded from the public kernel API. Its direct
use by source adapters is the explicit, narrow cross-package exception that
permits those adapters to issue bindings only after their own authority has
authenticated an observation. Ordinary callers consume the resulting binding
but cannot issue one through ``alghanem.kernel``.
"""

from dataclasses import dataclass

_AUTHENTICATED_OBSERVATION_BINDING_TOKEN = object()


def _require_text(value: str, name: str) -> None:
    if type(value) is not str or not value.strip():
        raise ValueError(f"{name} must be non-blank text")


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
        _require_text(source_observation_ref, "source observation reference")
        _require_text(source_authentication_ref, "source authentication reference")
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
