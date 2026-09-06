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

    run_manifest: MeasurementRunManifest
    ledger: ObservationAuditLedger

    def __post_init__(self) -> None:
        if not isinstance(self.run_manifest, MeasurementRunManifest):
            raise ValueError("ledger manifest must declare a measurement run manifest")
        if not isinstance(self.ledger, ObservationAuditLedger):
            raise ValueError("ledger manifest must contain an observation audit ledger")
        expected_run = self.run_manifest.run_identity
        expected_policy = self.run_manifest.normalization_form
        expected_unicode = self.run_manifest.unicode_database_version
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
        return self.run_manifest.run_identity


@dataclass(frozen=True)
class NormalizationEquivalenceClass:
    """A derived quotient class over occurrence-preserving audits."""

    candidate: SurfaceAtomCandidate
    members: tuple[NormalizationAudit, ...]
    raw_variants: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.candidate, SurfaceAtomCandidate):
            raise ValueError(
                "normalization equivalence class must declare a surface candidate"
            )
        if not self.members:
            raise ValueError(
                "normalization equivalence class must contain at least one member"
            )
        if any(member.candidate != self.candidate for member in self.members):
            raise ValueError(
                "normalization equivalence class members must share one candidate"
            )
        if self.raw_variants != tuple(
            sorted({member.trace.observation.surface for member in self.members})
        ):
            raise ValueError(
                "normalization equivalence class raw variants must be canonical"
            )

    @property
    def occurrence_count(self) -> int:
        """Number of observation occurrences in this quotient class."""
        return len(self.members)

    @property
    def raw_variant_count(self) -> int:
        """Number of distinct raw surfaces collapsed into this quotient class."""
        return len(self.raw_variants)


@dataclass(frozen=True)
class NormalizationEquivalenceProjection:
    """A derived projection grouping observations by normalized candidate."""

    classes: tuple[NormalizationEquivalenceClass, ...]


@dataclass(frozen=True)
class NormalizationResidualRow:
    """Occurrence-complete, non-linguistic row of raw-to-NFC residual data.

    Count and segment attributes are derived from the stored raw/normalized
    codepoints and common boundaries, so consumers do not need to keep duplicate
    constructor fields in sync. ``candidate_surface`` is the current normalized
    projection surface; it is projection metadata, not a new identity claim.
    """

    run_id: str
    source_id: str
    occurrence_id: str
    raw_surface: str
    raw_codepoints: tuple[str, ...]
    normalized_surface: str
    normalized_codepoints: tuple[str, ...]
    common_prefix_len: int
    common_suffix_len: int

    def __post_init__(self) -> None:
        for field_name, string_value in (
            ("run id", self.run_id),
            ("source id", self.source_id),
            ("occurrence id", self.occurrence_id),
            ("raw surface", self.raw_surface),
            ("normalized surface", self.normalized_surface),
        ):
            if not isinstance(string_value, str) or not string_value:
                raise ValueError(f"{field_name} must be a non-empty string")
        if self.raw_codepoints != tuple(self.raw_surface):
            raise ValueError("raw codepoints must reproduce the raw surface")
        if self.normalized_codepoints != tuple(self.normalized_surface):
            raise ValueError(
                "normalized codepoints must reproduce the normalized surface"
            )
        for field_name, integer_value in (
            ("common prefix length", self.common_prefix_len),
            ("common suffix length", self.common_suffix_len),
        ):
            if isinstance(integer_value, bool) or not isinstance(integer_value, int):
                raise ValueError(f"{field_name} must be an integer")
        if self.common_prefix_len < 0 or self.common_suffix_len < 0:
            raise ValueError("common boundary lengths must be non-negative")
        if self.common_prefix_len + self.common_suffix_len > min(
            len(self.raw_codepoints), len(self.normalized_codepoints)
        ):
            raise ValueError("common boundary lengths must not overlap")

    @property
    def raw_atom_count(self) -> int:
        """Number of raw codepoints observed before normalization."""
        return len(self.raw_codepoints)

    @property
    def normalized_atom_count(self) -> int:
        """Number of codepoints produced after normalization."""
        return len(self.normalized_codepoints)

    @property
    def changed(self) -> bool:
        """Whether raw and normalized surfaces differ."""
        return self.raw_surface != self.normalized_surface

    @property
    def length_delta(self) -> int:
        """Raw atom count minus normalized atom count."""
        return self.raw_atom_count - self.normalized_atom_count

    @property
    def removed_segment(self) -> str:
        """Raw residual segment outside the shared prefix/suffix."""
        return "".join(self._removed_codepoints)

    @property
    def inserted_segment(self) -> str:
        """Normalized residual segment outside the shared prefix/suffix."""
        return "".join(self._inserted_codepoints)

    @property
    def order_changed(self) -> bool:
        """Whether the local residual segment is a pure atom permutation."""
        return (
            self.changed
            and sorted(self._removed_codepoints) == sorted(self._inserted_codepoints)
            and self._removed_codepoints != self._inserted_codepoints
        )

    @property
    def residual_count(self) -> int:
        """Width of the local atom-delta segment."""
        return max(len(self._removed_codepoints), len(self._inserted_codepoints))

    @property
    def candidate_surface(self) -> str:
        """Current normalized projection surface for this residual row."""
        return self.normalized_surface

    @property
    def _removed_codepoints(self) -> tuple[str, ...]:
        raw_end = len(self.raw_codepoints) - self.common_suffix_len
        return self.raw_codepoints[self.common_prefix_len : raw_end]

    @property
    def _inserted_codepoints(self) -> tuple[str, ...]:
        normalized_end = len(self.normalized_codepoints) - self.common_suffix_len
        return self.normalized_codepoints[self.common_prefix_len : normalized_end]


@dataclass(frozen=True)
class NormalizationResidualTable:
    """A derived residual table with exactly one row per ledger occurrence."""

    rows: tuple[NormalizationResidualRow, ...]


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
    def normalization_equivalence_projection(
        manifest: ObservationLedgerManifest,
    ) -> NormalizationEquivalenceProjection:
        """Derive NFC equivalence classes without replacing the occurrence ledger."""
        grouped: dict[SurfaceAtomCandidate, list[NormalizationAudit]] = {}
        for audit in manifest.ledger.audits:
            grouped.setdefault(audit.candidate, []).append(audit)

        classes = []
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
            classes.append(
                NormalizationEquivalenceClass(
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
        return NormalizationEquivalenceProjection(tuple(classes))

    @staticmethod
    def residual_table(
        manifest: ObservationLedgerManifest,
    ) -> NormalizationResidualTable:
        """Derive an occurrence-complete residual table from a manifested ledger."""
        return NormalizationResidualTable(
            tuple(
                _residual_row(audit)
                for audit in sorted(
                    manifest.ledger.audits,
                    key=lambda item: (
                        item.trace.observation.provenance.run_identity.run_id,
                        item.trace.observation.provenance.source_id,
                        item.trace.observation.provenance.occurrence_id,
                    ),
                )
            )
        )


def _common_prefix_len(raw: tuple[str, ...], normalized: tuple[str, ...]) -> int:
    """Count unchanged leading atoms shared by raw and normalized codepoints."""
    count = 0
    for raw_atom, normalized_atom in zip(raw, normalized):
        if raw_atom != normalized_atom:
            break
        count += 1
    return count


def _common_suffix_len(
    raw: tuple[str, ...], normalized: tuple[str, ...], prefix_len: int
) -> int:
    """Count unchanged trailing atoms after excluding the shared prefix."""
    count = 0
    max_count = min(len(raw), len(normalized)) - prefix_len
    while count < max_count and raw[-(count + 1)] == normalized[-(count + 1)]:
        count += 1
    return count


def _residual_row(audit: NormalizationAudit) -> NormalizationResidualRow:
    observation = audit.trace.observation
    provenance = observation.provenance
    raw_codepoints = tuple(observation.surface)
    normalized_codepoints = tuple(audit.trace.normalized_surface)
    prefix_len = _common_prefix_len(raw_codepoints, normalized_codepoints)
    suffix_len = _common_suffix_len(raw_codepoints, normalized_codepoints, prefix_len)

    return NormalizationResidualRow(
        run_id=provenance.run_identity.run_id,
        source_id=provenance.source_id,
        occurrence_id=provenance.occurrence_id,
        raw_surface=observation.surface,
        raw_codepoints=raw_codepoints,
        normalized_surface=audit.trace.normalized_surface,
        normalized_codepoints=normalized_codepoints,
        common_prefix_len=prefix_len,
        common_suffix_len=suffix_len,
    )
