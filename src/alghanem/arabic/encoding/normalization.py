"""Auditable, non-linguistic Unicode surface normalization."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Final, Literal
from unicodedata import normalize, unidata_version

from .candidates import SurfaceAtomCandidate
from .measurement import MeasurementRunIdentity, MeasurementRunManifest
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

    def __post_init__(self) -> None:
        identities = {
            (
                audit.trace.observation.provenance.run_identity,
                audit.trace.observation.provenance.source_id,
                audit.trace.observation.provenance.occurrence_id,
            )
            for audit in self.audits
        }
        if len(identities) != len(self.audits):
            raise ValueError(
                "an audit ledger cannot contain duplicate occurrence identity"
            )


@dataclass(frozen=True)
class DistinctSurfaceAtomCandidateProjection:
    """A derived, canonical-order projection of the ledger's candidates."""

    candidates: tuple[SurfaceAtomCandidate, ...]


@dataclass(frozen=True)
class ObservationLedgerManifest:
    """A ledger bound to one measurement run and normalization policy."""

    measurement_run_manifest: MeasurementRunManifest
    ledger: ObservationAuditLedger

    def __post_init__(self) -> None:
        if not isinstance(self.measurement_run_manifest, MeasurementRunManifest):
            raise ValueError("ledger manifest must declare a measurement run manifest")
        if not isinstance(self.ledger, ObservationAuditLedger):
            raise ValueError("ledger manifest must contain an observation audit ledger")
        expected_run = self.measurement_run_manifest.run_identity
        expected_policy = self.measurement_run_manifest.normalization_form
        expected_unicode = self.measurement_run_manifest.unicode_database_version
        for audit in self.ledger.audits:
            provenance = audit.trace.observation.provenance
            if provenance.run_identity != expected_run:
                raise ValueError(
                    "ledger manifest cannot mix measurement run identities"
                )
            if audit.trace.normalization_form != expected_policy:
                raise ValueError(
                    "ledger manifest normalization must match measurement policy"
                )
            if audit.trace.unicode_database_version != expected_unicode:
                raise ValueError(
                    "ledger manifest Unicode version must match measurement manifest"
                )

    @property
    def run_identity(self) -> MeasurementRunIdentity:
        """The measurement run whose observations are preserved in the ledger."""
        return self.measurement_run_manifest.run_identity


@dataclass(frozen=True)
class NormalizationFiberCandidate:
    """One normalization equivalence class over occurrence-preserving audits."""

    candidate: SurfaceAtomCandidate
    members: tuple[NormalizationAudit, ...]
    raw_variants: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.candidate, SurfaceAtomCandidate):
            raise ValueError("normalization fiber must declare a surface candidate")
        if not self.members:
            raise ValueError("normalization fiber must contain at least one member")
        if any(member.candidate != self.candidate for member in self.members):
            raise ValueError("normalization fiber members must share one candidate")
        if self.raw_variants != tuple(
            sorted({member.trace.observation.surface for member in self.members})
        ):
            raise ValueError("normalization fiber raw variants must be canonical")

    @property
    def occurrence_count(self) -> int:
        """Number of observation occurrences in this normalization fiber."""
        return len(self.members)

    @property
    def raw_variant_count(self) -> int:
        """Number of distinct raw surfaces collapsed into this fiber."""
        return len(self.raw_variants)


@dataclass(frozen=True)
class NormalizationFiberCandidateProjection:
    """A quotient projection that groups observations by normalized candidate."""

    fibers: tuple[NormalizationFiberCandidate, ...]


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

    @classmethod
    def ledger_manifest(
        cls,
        run_identity: MeasurementRunIdentity,
        observations: Iterable[RawSurfaceObservation],
    ) -> ObservationLedgerManifest:
        """Normalize observations into a ledger authorized by one measurement run."""
        return ObservationLedgerManifest(
            MeasurementRunManifest.current(run_identity),
            cls.audit_ledger(observations),
        )

    @staticmethod
    def distinct_candidates(
        ledger: ObservationAuditLedger,
    ) -> DistinctSurfaceAtomCandidateProjection:
        """Derive distinct candidates in canonical order without altering the ledger."""
        return DistinctSurfaceAtomCandidateProjection(
            tuple(sorted({audit.candidate for audit in ledger.audits}))
        )

    @staticmethod
    def normalization_fibers(
        manifest: ObservationLedgerManifest,
    ) -> NormalizationFiberCandidateProjection:
        """Derive normalization fibers without replacing the occurrence ledger."""
        grouped: dict[SurfaceAtomCandidate, list[NormalizationAudit]] = {}
        for audit in manifest.ledger.audits:
            grouped.setdefault(audit.candidate, []).append(audit)

        fibers = []
        for candidate, members in sorted(grouped.items()):
            canonical_members = tuple(
                sorted(
                    members,
                    key=lambda audit: (
                        audit.trace.observation.provenance.source_id,
                        audit.trace.observation.provenance.occurrence_id,
                        audit.trace.observation.surface,
                    ),
                )
            )
            fibers.append(
                NormalizationFiberCandidate(
                    candidate,
                    canonical_members,
                    tuple(
                        sorted(
                            {
                                member.trace.observation.surface
                                for member in canonical_members
                            }
                        )
                    ),
                )
            )
        return NormalizationFiberCandidateProjection(tuple(fibers))
