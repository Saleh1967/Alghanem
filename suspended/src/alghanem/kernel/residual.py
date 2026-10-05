"""Residual records and the deferred G0.RC.1 contract boundary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ._internal.authenticated_observation_bridge import AuthenticatedObservationBinding
from .birth import ResidualDefinitionSpec
from .birth_content_identity import (
    BirthAssessmentContentBinding,
    BirthSemanticsContentIdentity,
)
from .trace import Trace

if TYPE_CHECKING:
    from .fractal import FrozenOntologyRef


class ResidualCertificationError(ValueError):
    """A malformed residual contract."""


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ResidualCertificationError(f"{field_name} must be non-blank")


@dataclass(frozen=True, slots=True)
class ResidualCertificationCandidate:
    """A contract-shaped proposal, not an authority-issued certification.

    G0.RC.1 remains deferred until freeze, reconstruction, and comparison
    authorities exist. In particular, a ``FrozenOntologyRef`` is only a
    caller-supplied reference at this stage; its type does not prove that a
    freeze occurred.
    """

    residual_id: str
    parent_freeze_ref: FrozenOntologyRef
    observation_ref: AuthenticatedObservationBinding
    scope_ref: str
    birth_content_binding: BirthAssessmentContentBinding
    reconstruction_attempt_ref: str
    comparison_result_ref: str
    trace: Trace

    def __post_init__(self) -> None:
        _require_text(self.residual_id, "residual id")
        if not _is_frozen_reference(self.parent_freeze_ref):
            raise ResidualCertificationError(
                "residual candidates require a frozen-reference-shaped parent"
            )
        if not isinstance(self.observation_ref, AuthenticatedObservationBinding):
            raise ResidualCertificationError(
                "residual candidates require an authenticated observation"
            )
        _require_text(self.scope_ref, "residual scope")
        if not isinstance(self.birth_content_binding, BirthAssessmentContentBinding):
            raise ResidualCertificationError(
                "residual candidates require a sealed birth content binding"
            )
        _require_text(self.reconstruction_attempt_ref, "reconstruction attempt ref")
        _require_text(self.comparison_result_ref, "comparison result ref")
        if not isinstance(self.trace, Trace):
            raise ResidualCertificationError("residual candidates require a trace")

    @property
    def residual_definition(self) -> ResidualDefinitionSpec:
        """The definition proven by the sealed birth content binding."""

        return self.birth_content_binding.contract.residual_definition

    @property
    def residual_definition_content_id(self) -> BirthSemanticsContentIdentity:
        """The registry-issued identity for ``residual_definition``."""

        return self.birth_content_binding.residual_definition_content_id


def _is_frozen_reference(value: object) -> bool:
    from .fractal import BornBridgeRef, FrozenFactorRef

    return isinstance(value, FrozenFactorRef | BornBridgeRef)


@dataclass(frozen=True, slots=True)
class Residual:
    """An explicit remainder; residuals are not silently discarded."""

    description: str

    def __post_init__(self) -> None:
        if not self.description.strip():
            raise ValueError("a residual requires a description")
