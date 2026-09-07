"""Residual records and the G0.RC.1 certified-residual boundary."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import TYPE_CHECKING

from ._internal.authenticated_observation_bridge import AuthenticatedObservationBinding
from .trace import Trace

if TYPE_CHECKING:
    from .fractal import BornBridgeRef, FrozenFactorRef


class ResidualCertificationError(ValueError):
    """A residual certification contract crossed its evidence boundary."""


_CERTIFICATION_TOKEN = object()
_FROZEN_PARENT_TYPES: tuple[type[object], ...] | None = None


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ResidualCertificationError(f"{field_name} must be non-blank")


def _content_id(*values: object) -> str:
    payload = json.dumps(
        [repr(value) for value in values],
        ensure_ascii=False,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8", "surrogatepass")).hexdigest()


@dataclass(frozen=True, slots=True, init=False)
class ReconstructionSpec:
    """A pre-registered reconstruction contract, not an execution result."""

    spec_id: str
    content_id: str

    @classmethod
    def register(cls, spec_id: str, semantics: str) -> ReconstructionSpec:
        _require_text(spec_id, "reconstruction specification id")
        _require_text(semantics, "reconstruction semantics")
        return cls(
            spec_id,
            _content_id("reconstruction-spec-v1", spec_id, semantics),
            _token=_CERTIFICATION_TOKEN,
        )

    def __init__(
        self, spec_id: str, content_id: str, *, _token: object | None = None
    ) -> None:
        if _token is not _CERTIFICATION_TOKEN:
            raise ResidualCertificationError(
                "reconstruction specifications must be pre-registered"
            )
        object.__setattr__(self, "spec_id", spec_id)
        object.__setattr__(self, "content_id", content_id)
        _require_text(self.spec_id, "reconstruction specification id")
        _require_text(self.content_id, "reconstruction specification content id")


@dataclass(frozen=True, slots=True, init=False)
class ResidualComparatorSpec:
    """A pre-registered comparator whose content is bound before observation."""

    spec_id: str
    content_id: str

    @classmethod
    def register(cls, spec_id: str, semantics: str) -> ResidualComparatorSpec:
        _require_text(spec_id, "comparator specification id")
        _require_text(semantics, "comparator semantics")
        return cls(
            spec_id,
            _content_id("residual-comparator-v1", spec_id, semantics),
            _token=_CERTIFICATION_TOKEN,
        )

    def __init__(
        self, spec_id: str, content_id: str, *, _token: object | None = None
    ) -> None:
        if _token is not _CERTIFICATION_TOKEN:
            raise ResidualCertificationError(
                "comparator specifications must be pre-registered"
            )
        object.__setattr__(self, "spec_id", spec_id)
        object.__setattr__(self, "content_id", content_id)
        _require_text(self.spec_id, "comparator specification id")
        _require_text(self.content_id, "comparator specification content id")


@dataclass(frozen=True, slots=True)
class ObservedDifference:
    """The comparator's result; an empty witness means that nothing differed."""

    comparator_spec_id: str
    comparator_content_id: str
    observed_projection_id: str
    reconstructed_projection_id: str
    difference_witness_id: str

    def __post_init__(self) -> None:
        for value, name in (
            (self.comparator_spec_id, "comparator specification id"),
            (self.comparator_content_id, "comparator content id"),
            (self.observed_projection_id, "observed projection id"),
            (self.reconstructed_projection_id, "reconstructed projection id"),
        ):
            _require_text(value, name)
        if self.difference_witness_id and not isinstance(
            self.difference_witness_id, str
        ):
            raise ResidualCertificationError(
                "difference witness id must be text when present"
            )

    @property
    def differs(self) -> bool:
        return bool(self.difference_witness_id) and (
            self.observed_projection_id != self.reconstructed_projection_id
        )


@dataclass(frozen=True, slots=True, init=False)
class CertifiedResidual:
    """A content-bound, comparator-certified reconstruction failure.

    This is deliberately separate from :class:`Residual`: a description,
    residual id, or caller-created definition cannot issue this record.
    """

    residual_id: str
    residual_content_id: str
    parent_freeze_ref: FrozenFactorRef | BornBridgeRef
    observation_ref: AuthenticatedObservationBinding
    scope_ref: str
    reconstruction_spec_id: str
    reconstruction_content_id: str
    comparator_spec_id: str
    comparator_content_id: str
    observed_projection_id: str
    reconstructed_projection_id: str
    difference_witness_id: str
    trace: Trace

    def __init__(
        self,
        residual_id: str,
        parent_freeze_ref: FrozenFactorRef | BornBridgeRef,
        observation_ref: AuthenticatedObservationBinding,
        scope_ref: str,
        reconstruction: ReconstructionSpec,
        comparator: ResidualComparatorSpec,
        difference: ObservedDifference,
        trace: Trace,
        *,
        _token: object | None = None,
    ) -> None:
        if _token is not _CERTIFICATION_TOKEN:
            raise ResidualCertificationError(
                "certified residuals must be issued by certify"
            )
        if not _is_frozen_parent(parent_freeze_ref):
            raise ResidualCertificationError(
                "certified residuals require an exact frozen parent reference"
            )
        if not isinstance(observation_ref, AuthenticatedObservationBinding):
            raise ResidualCertificationError(
                "certified residuals require an authenticated observation"
            )
        if not isinstance(reconstruction, ReconstructionSpec):
            raise ResidualCertificationError(
                "certified residuals require a pre-registered reconstruction"
            )
        if not isinstance(comparator, ResidualComparatorSpec):
            raise ResidualCertificationError(
                "certified residuals require a pre-registered comparator"
            )
        if not isinstance(difference, ObservedDifference) or not difference.differs:
            raise ResidualCertificationError(
                "a certified residual requires a reconstructible observed difference"
            )
        if (
            difference.comparator_spec_id != comparator.spec_id
            or difference.comparator_content_id != comparator.content_id
        ):
            raise ResidualCertificationError(
                "difference was not produced by the pre-registered comparator"
            )
        if not isinstance(trace, Trace):
            raise ResidualCertificationError("certified residuals require a trace")
        _require_text(residual_id, "residual id")
        _require_text(scope_ref, "residual scope")
        values = (
            residual_id,
            parent_freeze_ref,
            observation_ref,
            scope_ref,
            reconstruction.spec_id,
            reconstruction.content_id,
            comparator.spec_id,
            comparator.content_id,
            difference.observed_projection_id,
            difference.reconstructed_projection_id,
            difference.difference_witness_id,
            trace,
        )
        object.__setattr__(self, "residual_id", residual_id)
        object.__setattr__(self, "residual_content_id", _content_id(*values))
        object.__setattr__(self, "parent_freeze_ref", parent_freeze_ref)
        object.__setattr__(self, "observation_ref", observation_ref)
        object.__setattr__(self, "scope_ref", scope_ref)
        object.__setattr__(self, "reconstruction_spec_id", reconstruction.spec_id)
        object.__setattr__(self, "reconstruction_content_id", reconstruction.content_id)
        object.__setattr__(self, "comparator_spec_id", comparator.spec_id)
        object.__setattr__(self, "comparator_content_id", comparator.content_id)
        object.__setattr__(
            self, "observed_projection_id", difference.observed_projection_id
        )
        object.__setattr__(
            self, "reconstructed_projection_id", difference.reconstructed_projection_id
        )
        object.__setattr__(
            self, "difference_witness_id", difference.difference_witness_id
        )
        object.__setattr__(self, "trace", trace)

    @classmethod
    def certify(
        cls,
        residual_id: str,
        parent_freeze_ref: FrozenFactorRef | BornBridgeRef,
        observation_ref: AuthenticatedObservationBinding,
        scope_ref: str,
        reconstruction: ReconstructionSpec,
        comparator: ResidualComparatorSpec,
        difference: ObservedDifference,
        trace: Trace,
    ) -> CertifiedResidual:
        return cls(
            residual_id,
            parent_freeze_ref,
            observation_ref,
            scope_ref,
            reconstruction,
            comparator,
            difference,
            trace,
            _token=_CERTIFICATION_TOKEN,
        )


def _is_frozen_parent(value: object) -> bool:
    global _FROZEN_PARENT_TYPES
    if _FROZEN_PARENT_TYPES is None:
        from .fractal import BornBridgeRef, FrozenFactorRef

        _FROZEN_PARENT_TYPES = (FrozenFactorRef, BornBridgeRef)
    return isinstance(value, _FROZEN_PARENT_TYPES)


@dataclass(frozen=True, slots=True)
class Residual:
    """An explicit remainder; residuals are not silently discarded."""

    description: str

    def __post_init__(self) -> None:
        if not self.description.strip():
            raise ValueError("a residual requires a description")
