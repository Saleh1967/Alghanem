"""Tests for the observation and normalization foundation."""

from __future__ import annotations

from unicodedata import unidata_version

import pytest

from alghanem.arabic import (
    MeasurementProtocolSpec,
    MeasurementRunIdentity,
    MeasurementRunManifest,
    ObservationLedgerManifest,
    ObservationProvenance,
    RawSurfaceObservation,
    SurfaceNormalization,
)


def measurement_run(run_id: str = "run-1") -> MeasurementRunIdentity:
    return MeasurementRunIdentity(
        MeasurementProtocolSpec(
            protocol_id="surface-measurement",
            protocol_version="1",
            source_scope="test-source",
            normalization_policy="NFC",
            occurrence_scheme="caller-issued-sequence",
        ),
        run_id,
    )


def observation(
    source_id: str,
    occurrence_id: str,
    surface: str,
    run_identity: MeasurementRunIdentity | None = None,
) -> RawSurfaceObservation:
    return RawSurfaceObservation(
        ObservationProvenance(
            run_identity or measurement_run(), source_id, occurrence_id
        ),
        surface,
    )


def test_normalization_records_trace_residual_and_uninterpreted_atoms() -> None:
    source = observation("source", "first", "\u0627\u0654")

    audit = SurfaceNormalization.normalize(source)

    assert audit.trace.observation == source
    assert audit.trace.observation.provenance == source.provenance
    assert audit.trace.normalized_surface == "\u0623"
    assert audit.trace.normalization_form == "NFC"
    assert audit.trace.unicode_database_version == unidata_version
    assert audit.residuals[0].raw_surface == "\u0627\u0654"
    assert audit.residuals[0].normalized_surface == "\u0623"
    assert audit.candidate.atoms == ("\u0623",)


def test_ledger_preserves_duplicate_observation_occurrences() -> None:
    observations = [
        observation("source", "one", "\u0628\u064e"),
        observation("source", "two", "\u0627\u0654"),
        observation("source", "three", "\u0628\u064e"),
    ]

    ledger = SurfaceNormalization.audit_ledger(observations)

    assert len(ledger.audits) == 3
    assert [audit.trace.observation for audit in ledger.audits] == observations
    assert ledger.audits[0].trace.observation != ledger.audits[2].trace.observation
    assert (
        ledger.audits[0].trace.observation.surface
        == ledger.audits[2].trace.observation.surface
    )


def test_distinct_projection_collapses_duplicate_ledger_candidates() -> None:
    ledger = SurfaceNormalization.audit_ledger(
        [
            observation("source", "one", "\u0628\u064e"),
            observation("source", "two", "\u0628\u064e"),
        ]
    )

    projection = SurfaceNormalization.distinct_candidates(ledger)

    assert len(ledger.audits) == 2
    assert projection.candidates == (ledger.audits[0].candidate,)


def test_distinct_projection_is_independent_of_observation_order() -> None:
    observations = [
        observation("source", "one", "\u0628\u064e"),
        observation("source", "two", "\u0627\u0654"),
        observation("source", "three", "\u0628\u064e"),
    ]

    projection = SurfaceNormalization.distinct_candidates(
        SurfaceNormalization.audit_ledger(observations)
    )
    reversed_projection = SurfaceNormalization.distinct_candidates(
        SurfaceNormalization.audit_ledger(reversed(observations))
    )

    assert projection == reversed_projection
    assert {
        audit.trace.observation.provenance
        for audit in SurfaceNormalization.audit_ledger(observations).audits
    } == {
        audit.trace.observation.provenance
        for audit in SurfaceNormalization.audit_ledger(reversed(observations)).audits
    }


def test_unknown_combining_marks_remain_uninterpreted_surface_atoms() -> None:
    audit = SurfaceNormalization.normalize(observation("source", "one", "\u0628\u0657"))

    assert audit.candidate.atoms == ("\u0628", "\u0657")


def test_ledger_rejects_duplicate_occurrence_identity() -> None:
    repeated = [
        observation("source", "same", "\u0628\u064e"),
        observation("source", "same", "\u0627\u0654"),
    ]

    with pytest.raises(ValueError, match="duplicate occurrence identity"):
        SurfaceNormalization.audit_ledger(repeated)


def test_same_occurrence_id_in_distinct_runs_remains_distinct() -> None:
    repeated = [
        observation("source", "same", "\u0628\u064e", measurement_run("run-1")),
        observation("source", "same", "\u0627\u0654", measurement_run("run-2")),
    ]

    ledger = SurfaceNormalization.audit_ledger(repeated)

    assert len(ledger.audits) == 2


def test_manifest_binds_ledger_to_one_measurement_run() -> None:
    run_identity = measurement_run()
    observations = [
        observation("source", "one", "\u0628\u064e", run_identity),
        observation("source", "two", "\u0627\u0654", run_identity),
    ]

    manifest = SurfaceNormalization.ledger_manifest(run_identity, observations)

    assert manifest.run_identity == run_identity
    assert manifest.run_manifest.normalization_form == "NFC"
    assert manifest.run_manifest.unicode_database_version == (unidata_version)
    assert manifest.ledger.audits[0].trace.observation.provenance.run_identity == (
        run_identity
    )


def test_manifest_rejects_observations_from_another_measurement_run() -> None:
    ledger = SurfaceNormalization.audit_ledger(
        [observation("source", "one", "\u0628\u064e", measurement_run("run-2"))]
    )

    with pytest.raises(ValueError, match="measurement run identities"):
        ObservationLedgerManifest(
            MeasurementRunManifest.current(measurement_run("run-1")), ledger
        )


def test_manifest_rejects_normalization_policy_mismatch() -> None:
    run_identity = MeasurementRunIdentity(
        MeasurementProtocolSpec(
            protocol_id="surface-measurement",
            protocol_version="1",
            source_scope="test-source",
            normalization_policy="NFD",
            occurrence_scheme="caller-issued-sequence",
        ),
        "run-1",
    )

    with pytest.raises(ValueError, match="normalization"):
        ObservationLedgerManifest(
            MeasurementRunManifest(
                run_identity,
                normalization_form="NFD",
                unicode_database_version=unidata_version,
            ),
            SurfaceNormalization.audit_ledger(
                [observation("source", "one", "\u0628\u064e", run_identity)]
            ),
        )


def test_measurement_run_manifest_rejects_policy_mismatch() -> None:
    run_identity = measurement_run()

    with pytest.raises(ValueError, match="protocol policy"):
        MeasurementRunManifest(
            run_identity,
            normalization_form="NFD",
            unicode_database_version=unidata_version,
        )


def test_normalization_equivalence_projection_groups_by_candidate() -> None:
    run_identity = measurement_run()
    observations = [
        observation("source", "one", "\u0627\u0654", run_identity),
        observation("source", "two", "\u0623", run_identity),
        observation("source", "three", "\u0628\u064e", run_identity),
    ]
    manifest = SurfaceNormalization.ledger_manifest(run_identity, observations)

    projection = SurfaceNormalization.normalization_equivalence_projection(manifest)

    assert len(projection.classes) == 2
    alef_class = projection.classes[0]
    assert alef_class.candidate.normalized_surface == "\u0623"
    assert alef_class.occurrence_count == 2
    assert alef_class.raw_variant_count == 2
    assert alef_class.raw_variants == ("\u0623", "\u0627\u0654")
    assert {
        member.trace.observation.provenance.occurrence_id
        for member in alef_class.members
    } == {"one", "two"}


def test_normalization_equivalence_projection_is_order_independent() -> None:
    run_identity = measurement_run()
    observations = [
        observation("source", "one", "\u0628\u064e", run_identity),
        observation("source", "two", "\u0627\u0654", run_identity),
        observation("source", "three", "\u0623", run_identity),
    ]

    projection = SurfaceNormalization.normalization_equivalence_projection(
        SurfaceNormalization.ledger_manifest(run_identity, observations)
    )
    reversed_projection = SurfaceNormalization.normalization_equivalence_projection(
        SurfaceNormalization.ledger_manifest(run_identity, reversed(observations))
    )

    assert projection == reversed_projection


def test_normalization_equivalence_projection_does_not_replace_ledger() -> None:
    run_identity = measurement_run()
    observations = [
        observation("source", "one", "\u0628\u064e", run_identity),
        observation("source", "two", "\u0628\u064e", run_identity),
    ]
    manifest = SurfaceNormalization.ledger_manifest(run_identity, observations)

    projection = SurfaceNormalization.normalization_equivalence_projection(manifest)

    assert len(manifest.ledger.audits) == 2
    assert len(projection.classes) == 1
    assert projection.classes[0].occurrence_count == 2
    assert tuple(
        member.trace.observation for member in projection.classes[0].members
    ) == (
        observations[0],
        observations[1],
    )


def test_residual_table_has_one_row_per_occurrence_in_canonical_order() -> None:
    run_identity = measurement_run()
    observations = [
        observation("source", "two", "\u0628\u064e", run_identity),
        observation("source", "one", "\u0627\u0654", run_identity),
    ]
    manifest = SurfaceNormalization.ledger_manifest(run_identity, observations)

    table = SurfaceNormalization.residual_table(manifest)

    assert len(table.rows) == len(manifest.ledger.audits)
    assert [row.occurrence_id for row in table.rows] == ["one", "two"]


def test_residual_table_records_atom_level_changed_delta() -> None:
    run_identity = measurement_run()
    manifest = SurfaceNormalization.ledger_manifest(
        run_identity,
        [observation("source", "one", "\u0627\u0654", run_identity)],
    )

    row = SurfaceNormalization.residual_table(manifest).rows[0]

    assert row.run_id == run_identity.run_id
    assert row.source_id == "source"
    assert row.occurrence_id == "one"
    assert row.raw_surface == "\u0627\u0654"
    assert row.raw_codepoints == ("\u0627", "\u0654")
    assert row.normalized_surface == "\u0623"
    assert row.normalized_codepoints == ("\u0623",)
    assert row.raw_atom_count == 2
    assert row.normalized_atom_count == 1
    assert row.changed is True
    assert row.length_delta == 1
    assert row.common_prefix_len == 0
    assert row.common_suffix_len == 0
    assert row.removed_segment == "\u0627\u0654"
    assert row.inserted_segment == "\u0623"
    assert row.order_changed is False
    assert row.residual_count == 2
    assert row.candidate_surface == "\u0623"


def test_residual_table_preserves_zero_residual_rows() -> None:
    run_identity = measurement_run()
    manifest = SurfaceNormalization.ledger_manifest(
        run_identity,
        [observation("source", "one", "\u0628\u064e", run_identity)],
    )

    row = SurfaceNormalization.residual_table(manifest).rows[0]

    assert row.changed is False
    assert row.length_delta == 0
    assert row.common_prefix_len == 2
    assert row.common_suffix_len == 0
    assert row.removed_segment == ""
    assert row.inserted_segment == ""
    assert row.residual_count == 0
    assert row.candidate_surface == "\u0628\u064e"


def test_residual_table_detects_order_change_within_delta_segment() -> None:
    run_identity = measurement_run()
    manifest = SurfaceNormalization.ledger_manifest(
        run_identity,
        [observation("source", "one", "\u0628\u0655\u064e", run_identity)],
    )

    row = SurfaceNormalization.residual_table(manifest).rows[0]

    assert row.raw_codepoints == ("\u0628", "\u0655", "\u064e")
    assert row.normalized_codepoints == ("\u0628", "\u064e", "\u0655")
    assert row.common_prefix_len == 1
    assert row.common_suffix_len == 0
    assert row.removed_segment == "\u0655\u064e"
    assert row.inserted_segment == "\u064e\u0655"
    assert row.order_changed is True


def test_observation_provenance_requires_measurement_run() -> None:
    with pytest.raises(ValueError, match="measurement run identity"):
        ObservationProvenance("source", "one", "extra")  # type: ignore[arg-type]


@pytest.mark.parametrize("surface", ["", 1])
def test_observation_rejects_empty_or_non_string_surfaces(surface: object) -> None:
    with pytest.raises(ValueError, match="non-empty string"):
        RawSurfaceObservation(
            ObservationProvenance(measurement_run(), "source", "one"),
            surface,  # type: ignore[arg-type]
        )
