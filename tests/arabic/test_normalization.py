"""Tests for the observation and normalization foundation."""

from __future__ import annotations

import pytest

from alghanem.arabic import RawSurfaceObservation, SurfaceNormalization


def test_normalization_records_trace_residual_and_uninterpreted_atoms() -> None:
    observation = RawSurfaceObservation("\u0627\u0654")

    audit = SurfaceNormalization.normalize(observation)

    assert audit.trace.observation == observation
    assert audit.trace.normalizer == "Unicode NFC"
    assert audit.trace.normalized_surface == "\u0623"
    assert audit.residuals[0].raw_surface == "\u0627\u0654"
    assert audit.residuals[0].normalized_surface == "\u0623"
    assert audit.candidate.atoms == ("\u0623",)


def test_candidate_collection_is_independent_of_observation_order() -> None:
    observations = [
        RawSurfaceObservation("\u0628\u064e"),
        RawSurfaceObservation("\u0627\u0654"),
        RawSurfaceObservation("\u0628\u064e"),
    ]

    candidates = SurfaceNormalization.candidates(observations)
    reversed_candidates = SurfaceNormalization.candidates(reversed(observations))

    assert candidates == reversed_candidates


def test_combining_marks_remain_uninterpreted_surface_atoms() -> None:
    audit = SurfaceNormalization.normalize(RawSurfaceObservation("\u0627\u0654"))

    assert audit.candidate.normalized_surface == "\u0623"
    assert not hasattr(audit.candidate, "state")
    assert not hasattr(audit.candidate, "carrier")


def test_unknown_combining_marks_do_not_create_a_state_identity() -> None:
    audit = SurfaceNormalization.normalize(RawSurfaceObservation("\u0628\u0657"))

    assert audit.candidate.atoms == ("\u0628", "\u0657")
    assert not hasattr(audit.candidate, "state")


@pytest.mark.parametrize("surface", ["", 1])
def test_observation_rejects_non_empty_non_string_surfaces(surface: object) -> None:
    with pytest.raises(ValueError, match="non-empty string"):
        RawSurfaceObservation(surface)  # type: ignore[arg-type]
