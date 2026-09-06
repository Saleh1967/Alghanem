"""Auditable, non-linguistic Unicode surface normalization."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Final, Literal
from unicodedata import normalize, unidata_version

from .candidates import SurfaceAtomCandidate
from .observation import RawSurfaceObservation

_NORMALIZATION_FORM: Final[Literal["NFC"]] = "NFC"


@dataclass(frozen=True)
class NormalizationTrace:
    """The deterministic normalization operation applied to one observation."""

    observation: RawSurfaceObservation
    normalized_surface: str
    normalization_form: str
    unicode_database_version: str


@dataclass(frozen=True)
class NormalizationResidual:
    """A raw-to-normalized difference retained without semantic interpretation."""

    raw_surface: str
    normalized_surface: str


@dataclass(frozen=True)
class NormalizationAudit:
    """The trace, residuals, and uninterpreted candidate of normalization."""

    trace: NormalizationTrace
    residuals: tuple[NormalizationResidual, ...]
    candidate: SurfaceAtomCandidate


@dataclass(frozen=True)
class ObservationAuditLedger:
    """The occurrence-preserving record from which projections are derived."""

    audits: tuple[NormalizationAudit, ...]


@dataclass(frozen=True)
class DistinctSurfaceAtomCandidateProjection:
    """A derived, canonical-order projection of the ledger's candidates."""

    candidates: tuple[SurfaceAtomCandidate, ...]


class SurfaceNormalization:
    """Produce canonical surface candidates without inferring linguistic roles."""

    @staticmethod
    def normalize(observation: RawSurfaceObservation) -> NormalizationAudit:
        normalized_surface = normalize(_NORMALIZATION_FORM, observation.surface)
        trace = NormalizationTrace(
            observation,
            normalized_surface,
            normalization_form=_NORMALIZATION_FORM,
            unicode_database_version=unidata_version,
        )
        residuals = (
            ()
            if normalized_surface == observation.surface
            else (NormalizationResidual(observation.surface, normalized_surface),)
        )
        return NormalizationAudit(
            trace,
            residuals,
            SurfaceAtomCandidate(normalized_surface, tuple(normalized_surface)),
        )

    @classmethod
    def audit_ledger(
        cls, observations: Iterable[RawSurfaceObservation]
    ) -> ObservationAuditLedger:
        """Normalize every observation without removing occurrence provenance."""
        return ObservationAuditLedger(
            tuple(cls.normalize(observation) for observation in observations)
        )

    @staticmethod
    def distinct_candidates(
        ledger: ObservationAuditLedger,
    ) -> DistinctSurfaceAtomCandidateProjection:
        """Derive distinct candidates in canonical order without altering the ledger."""
        return DistinctSurfaceAtomCandidateProjection(
            tuple(sorted({audit.candidate for audit in ledger.audits}))
        )
