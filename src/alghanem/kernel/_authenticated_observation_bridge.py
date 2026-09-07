"""Internal G0.OB.1 bridge for source observation authorities.

This module is intentionally excluded from the public kernel API. Source
adapters invoke it only after their own authority has authenticated an
observation; ordinary callers consume the resulting binding but cannot issue
one through ``alghanem.kernel``.
"""

from .evidence_role import (
    AuthenticatedObservationBinding,
    _issue_authenticated_observation_binding,
)


def issue_from_source_authority(
    source_observation_ref: str, source_authentication_ref: str
) -> AuthenticatedObservationBinding:
    """Issue a kernel binding from a source authority's authenticated observation."""

    return _issue_authenticated_observation_binding(
        source_observation_ref, source_authentication_ref
    )
