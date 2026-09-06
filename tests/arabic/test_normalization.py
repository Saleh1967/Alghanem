"""Tests for the observation and normalization foundation."""

from __future__ import annotations

from unicodedata import unidata_version

import pytest

from alghanem.arabic import RawSurfaceObservation, SurfaceNormalization


def test_normalization_records_trace_residual_and_uninterpreted_atoms() -> None:
    observation = RawSurfaceObservation("\u0627\u0654")

    audit = SurfaceNormalization.normalize(observation)

    assert audit.trace.observation == observation
    assert audit.trace.normalized_surface == "\u0623"
    assert audit.trace.normalization_form == "NFC"
    assert audit.trace.unicode_database_version == unidata_version
    assert audit.residuals[0].raw_surface == "\u0627\u0654"
    assert audit.residuals[0].normalized_surface == "\u0623"
    assert audit.candidate.atoms == ("\u0623",)


def test_ledger_preserves_duplicate_observation_occurrences() -> None:
    observations = [
        RawSurfaceObservation("\u0628\u064e"),
        RawSurfaceObservation("\u0627\u0654"),
        RawSurfaceObservation("\u0628\u064e"),
    ]

    ledger = SurfaceNormalization.audit_ledger(observations)

    assert len(ledger.audits) == 3
    assert [audit.trace.observation for audit in ledger.audits] == observations


def test_distinct_projection_collapses_duplicate_ledger_candidates() -> None:
    ledger = SurfaceNormalization.audit_ledger(
        [RawSurfaceObservation("\u0628\u064e"), RawSurfaceObservation("\u0628\u064e")]
    )

    projection = SurfaceNormalization.distinct_candidates(ledger)

    assert len(ledger.audits) == 2
    assert projection.candidates == (ledger.audits[0].candidate,)


def test_distinct_projection_is_independent_of_observation_order() -> None:
    observations = [
        RawSurfaceObservation("\u0628\u064e"),
        RawSurfaceObservation("\u0627\u0654"),
        RawSurfaceObservation("\u0628\u064e"),
    ]

    projection = SurfaceNormalization.distinct_candidates(
        SurfaceNormalization.audit_ledger(observations)
    )
    reversed_projection = SurfaceNormalization.distinct_candidates(
        SurfaceNormalization.audit_ledger(reversed(observations))
    )

    assert projection == reversed_projection


def test_unknown_combining_marks_remain_uninterpreted_surface_atoms() -> None:
    audit = SurfaceNormalization.normalize(RawSurfaceObservation("\u0628\u0657"))

    assert audit.candidate.atoms == ("\u0628", "\u0657")


@pytest.mark.parametrize("surface", ["", 1])
def test_observation_rejects_non_empty_non_string_surfaces(surface: object) -> None:
    with pytest.raises(ValueError, match="non-empty string"):
        RawSurfaceObservation(surface)  # type: ignore[arg-type]
