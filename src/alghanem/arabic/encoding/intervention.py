"""Controlled, non-linguistic interventions on surface-atom candidates."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Literal

from .normalization import ObservationLedgerManifest

InterventionType = Literal["delete", "substitute", "repeat", "swap", "insert"]


@dataclass(frozen=True)
class SurfaceAtomIntervention:
    """One position-indexed operation on an observed surface candidate.

    Coordinates are zero-based. Insert coordinates identify the position before
    which the payload is inserted; the atom count is therefore a valid append
    coordinate.
    """

    source_id: str
    occurrence_id: str
    intervention_type: InterventionType
    coordinates: tuple[int, ...]
    payload: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.source_id, str) or not self.source_id:
            raise ValueError("intervention source id must be a non-empty string")
        if not isinstance(self.occurrence_id, str) or not self.occurrence_id:
            raise ValueError("intervention occurrence id must be a non-empty string")
        if self.intervention_type not in {
            "delete",
            "substitute",
            "repeat",
            "swap",
            "insert",
        }:
            raise ValueError("intervention type is not supported")
        if not self.coordinates or any(
            isinstance(index, bool) or not isinstance(index, int)
            for index in self.coordinates
        ):
            raise ValueError("intervention coordinates must be non-empty integers")
        expected_coordinate_count = 2 if self.intervention_type == "swap" else 1
        if len(self.coordinates) != expected_coordinate_count:
            raise ValueError("intervention type has an invalid coordinate count")
        needs_payload = self.intervention_type in {"substitute", "insert"}
        if needs_payload != (self.payload is not None):
            raise ValueError("intervention payload does not match intervention type")
        if self.payload is not None and (
            not isinstance(self.payload, str) or not self.payload
        ):
            raise ValueError("intervention payload must be a non-empty atom")


@dataclass(frozen=True)
class SurfaceInterventionTrace:
    """The complete deterministic effect of one controlled intervention."""

    source_atoms: tuple[str, ...]
    intervention: SurfaceAtomIntervention
    result_atoms: tuple[str, ...]


@dataclass(frozen=True)
class SurfaceInterventionAuditRow:
    """Occurrence-bound, non-linguistic record of one atom intervention."""

    run_id: str
    source_id: str
    occurrence_id: str
    source_surface: str
    source_atoms: tuple[str, ...]
    intervention: SurfaceAtomIntervention
    result_surface: str
    result_atoms: tuple[str, ...]
    trace: SurfaceInterventionTrace

    def __post_init__(self) -> None:
        if not all(
            isinstance(value, str) and value
            for value in (
                self.run_id,
                self.source_id,
                self.occurrence_id,
                self.source_surface,
            )
        ):
            raise ValueError("audit row identity and source surface must be non-empty")
        if "".join(self.source_atoms) != self.source_surface:
            raise ValueError("source atoms must reproduce the source surface")
        if "".join(self.result_atoms) != self.result_surface:
            raise ValueError("result atoms must reproduce the result surface")
        if self.intervention.source_id != self.source_id:
            raise ValueError("intervention source id must match audit row")
        if self.intervention.occurrence_id != self.occurrence_id:
            raise ValueError("intervention occurrence id must match audit row")
        if self.trace != SurfaceInterventionTrace(
            self.source_atoms, self.intervention, self.result_atoms
        ):
            raise ValueError("intervention trace must reproduce the audit row")

    @property
    def source_atom_count(self) -> int:
        return len(self.source_atoms)

    @property
    def result_atom_count(self) -> int:
        return len(self.result_atoms)

    @property
    def preserved_positions(self) -> tuple[int, ...]:
        return tuple(
            index
            for index, (source, result) in enumerate(
                zip(self.source_atoms, self.result_atoms)
            )
            if source == result
        )

    @property
    def displaced_atoms(self) -> tuple[tuple[int, str], ...]:
        return tuple(
            (index, atom)
            for index, atom in enumerate(self.source_atoms)
            if index >= len(self.result_atoms) or atom != self.result_atoms[index]
        )

    @property
    def multiplicity_delta(self) -> tuple[tuple[str, int], ...]:
        source_counts = Counter(self.source_atoms)
        result_counts = Counter(self.result_atoms)
        return tuple(
            (atom, result_counts[atom] - source_counts[atom])
            for atom in sorted(source_counts.keys() | result_counts.keys())
            if result_counts[atom] != source_counts[atom]
        )

    @property
    def order_delta(self) -> bool:
        return _shared_atom_sequence(
            self.source_atoms, self.result_atoms
        ) != _shared_atom_sequence(self.result_atoms, self.source_atoms)

    @property
    def equality_signature(self) -> tuple[tuple[int, int], ...]:
        return _equality_signature(self.result_atoms)

    @property
    def boundary_delta(self) -> None:
        """No boundaries are modeled at this measurement stage."""
        return None

    @property
    def residual(self) -> tuple[str, ...]:
        """Nothing remains after the declared deterministic operation."""
        return ()


@dataclass(frozen=True)
class SurfaceInterventionAuditTable:
    """Derived rows for controlled interventions over manifested occurrences."""

    rows: tuple[SurfaceInterventionAuditRow, ...]


class SurfaceAtomInterventionAudit:
    """Apply neutral operations without inferring linguistic roles or identity."""

    @staticmethod
    def audit(
        manifest: ObservationLedgerManifest,
        interventions: tuple[SurfaceAtomIntervention, ...],
    ) -> SurfaceInterventionAuditTable:
        audits = {
            (
                audit.trace.observation.provenance.source_id,
                audit.trace.observation.provenance.occurrence_id,
            ): audit
            for audit in manifest.ledger.audits
        }
        rows = []
        for intervention in interventions:
            try:
                audit = audits[(intervention.source_id, intervention.occurrence_id)]
            except KeyError as error:
                raise ValueError(
                    "intervention must target a manifested occurrence"
                ) from error
            source_atoms = audit.candidate.atoms
            result_atoms = _apply(intervention, source_atoms)
            provenance = audit.trace.observation.provenance
            trace = SurfaceInterventionTrace(source_atoms, intervention, result_atoms)
            rows.append(
                SurfaceInterventionAuditRow(
                    provenance.run_identity.run_id,
                    provenance.source_id,
                    provenance.occurrence_id,
                    audit.candidate.normalized_surface,
                    source_atoms,
                    intervention,
                    "".join(result_atoms),
                    result_atoms,
                    trace,
                )
            )
        return SurfaceInterventionAuditTable(tuple(rows))


def _apply(
    intervention: SurfaceAtomIntervention, source_atoms: tuple[str, ...]
) -> tuple[str, ...]:
    coordinates = intervention.coordinates
    atom_count = len(source_atoms)
    if intervention.intervention_type == "insert":
        assert intervention.payload is not None
        _require_coordinate(coordinates[0], atom_count, allow_end=True)
        return (
            source_atoms[: coordinates[0]]
            + (intervention.payload,)
            + source_atoms[coordinates[0] :]
        )
    for coordinate in coordinates:
        _require_coordinate(coordinate, atom_count, allow_end=False)
    if intervention.intervention_type == "delete":
        return source_atoms[: coordinates[0]] + source_atoms[coordinates[0] + 1 :]
    if intervention.intervention_type == "substitute":
        assert intervention.payload is not None
        return (
            source_atoms[: coordinates[0]]
            + (intervention.payload,)
            + source_atoms[coordinates[0] + 1 :]
        )
    if intervention.intervention_type == "repeat":
        return (
            source_atoms[: coordinates[0] + 1]
            + (source_atoms[coordinates[0]],)
            + source_atoms[coordinates[0] + 1 :]
        )
    first, second = coordinates
    if first == second:
        raise ValueError("swap coordinates must be distinct")
    result = list(source_atoms)
    result[first], result[second] = result[second], result[first]
    return tuple(result)


def _require_coordinate(coordinate: int, atom_count: int, *, allow_end: bool) -> None:
    upper_bound = atom_count if allow_end else atom_count - 1
    if coordinate < 0 or coordinate > upper_bound:
        raise ValueError("intervention coordinate is outside the source atom sequence")


def _shared_atom_sequence(
    atoms: tuple[str, ...], other_atoms: tuple[str, ...]
) -> tuple[str, ...]:
    remaining = Counter(other_atoms)
    shared = []
    for atom in atoms:
        if remaining[atom]:
            shared.append(atom)
            remaining[atom] -= 1
    return tuple(shared)


def _equality_signature(atoms: tuple[str, ...]) -> tuple[tuple[int, int], ...]:
    return tuple(
        (left, right)
        for left, atom in enumerate(atoms)
        for right in range(left + 1, len(atoms))
        if atom == atoms[right]
    )
