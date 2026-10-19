"""اختبارُ قياسِ ضرورةِ البنية الصرفية: تطبيقٌ فعليّ، وتمييزُ التعذّر عن النفي."""

from __future__ import annotations

import pytest

from alghanem.arabic.morphological_necessity_measurement import (
    NAMED_RESIDUALS,
    DomainApplication,
    DomainApplicationRow,
    MorphologicalNecessityMeasurementError,
    NecessityProbeReport,
    PairMeasurement,
    PairStanding,
    ReaderAttempt,
    apply_domain_to_pair,
    run_necessity_probe,
)
from alghanem.arabic.morphological_necessity_probe import (
    FROZEN_DISCRIMINATION_TARGET,
    read_weaker_domain_cone,
)


def test_every_domain_is_actually_called_on_both_surfaces() -> None:
    report = run_necessity_probe()
    for measurement in report.measurements:
        assert len(measurement.rows) == 4
        for row in measurement.rows:
            surfaces = {attempt.surface for attempt in row.attempts}
            assert surfaces == {measurement.pair.surface_a, measurement.pair.surface_b}


def test_each_refusal_carries_the_domains_own_message_verbatim() -> None:
    report = run_necessity_probe()
    for measurement in report.measurements:
        for row in measurement.rows:
            for attempt in row.attempts:
                if not attempt.accepted:
                    assert attempt.refusal_message
                    assert "must be one of" in (attempt.refusal_message or "")


def test_refusal_is_recorded_as_no_entry_never_as_equating() -> None:
    report = run_necessity_probe()
    for measurement in report.measurements:
        for row in measurement.rows:
            if not row.accepting_readers:
                assert row.application is DomainApplication.NO_ENTRY_FOR_SURFACE_FORM
                assert row.application is not DomainApplication.EQUATES


def test_one_blocked_domain_forbids_the_measured_negative() -> None:
    cone = read_weaker_domain_cone()
    pair = FROZEN_DISCRIMINATION_TARGET[0]
    rows = tuple(apply_domain_to_pair(pair, reference) for reference in cone)
    measurement = PairMeasurement(
        pair=pair,
        rows=rows,
        covered_cone=tuple(reference.module_relative_path for reference in cone),
    )
    assert measurement.blocking_domains
    assert (
        measurement.standing
        is not PairStanding.UNDISTINGUISHED_AFTER_EXHAUSTIVE_MEASUREMENT
    )
    assert measurement.standing is PairStanding.UNRESOLVED_MEASUREMENT_IMPOSSIBLE


def test_the_negative_requires_every_domain_to_have_equated_the_two() -> None:
    pair = FROZEN_DISCRIMINATION_TARGET[0]
    cone = read_weaker_domain_cone()
    equating_rows = tuple(
        DomainApplicationRow(
            pair=pair,
            module_relative_path=reference.module_relative_path,
            attempts=(
                ReaderAttempt(
                    reader_name=_first_reader_name(reference.module_relative_path),
                    surface=pair.surface_a,
                    accepted=True,
                    accepted_member="نعم",
                    refusal_message=None,
                ),
                ReaderAttempt(
                    reader_name=_first_reader_name(reference.module_relative_path),
                    surface=pair.surface_b,
                    accepted=True,
                    accepted_member="نعم",
                    refusal_message=None,
                ),
            ),
        )
        for reference in cone
    )
    measurement = PairMeasurement(
        pair=pair,
        rows=equating_rows,
        covered_cone=tuple(reference.module_relative_path for reference in cone),
    )
    assert (
        measurement.standing
        is PairStanding.UNDISTINGUISHED_AFTER_EXHAUSTIVE_MEASUREMENT
    )


def test_one_distinguishing_domain_outranks_every_other_reading() -> None:
    pair = FROZEN_DISCRIMINATION_TARGET[0]
    cone = read_weaker_domain_cone()
    rows = list(apply_domain_to_pair(pair, reference) for reference in cone)
    reader_name = _first_reader_name(cone[0].module_relative_path)
    rows[0] = DomainApplicationRow(
        pair=pair,
        module_relative_path=cone[0].module_relative_path,
        attempts=(
            ReaderAttempt(
                reader_name=reader_name,
                surface=pair.surface_a,
                accepted=True,
                accepted_member="نعم",
                refusal_message=None,
            ),
            ReaderAttempt(
                reader_name=reader_name,
                surface=pair.surface_b,
                accepted=True,
                accepted_member="لا",
                refusal_message=None,
            ),
        ),
    )
    measurement = PairMeasurement(
        pair=pair,
        rows=tuple(rows),
        covered_cone=tuple(reference.module_relative_path for reference in cone),
    )
    assert measurement.standing is PairStanding.DISTINGUISHED_BY_STANDING_DOMAIN


def test_partial_cone_coverage_is_refused_before_any_standing() -> None:
    cone = read_weaker_domain_cone()
    pair = FROZEN_DISCRIMINATION_TARGET[0]
    rows = tuple(apply_domain_to_pair(pair, reference) for reference in cone[:3])
    with pytest.raises(MorphologicalNecessityMeasurementError):
        PairMeasurement(
            pair=pair,
            rows=rows,
            covered_cone=tuple(reference.module_relative_path for reference in cone),
        )


def test_a_duplicated_domain_cannot_double_one_witness() -> None:
    cone = read_weaker_domain_cone()
    pair = FROZEN_DISCRIMINATION_TARGET[0]
    row = apply_domain_to_pair(pair, cone[0])
    with pytest.raises(MorphologicalNecessityMeasurementError):
        PairMeasurement(
            pair=pair,
            rows=(row, row),
            covered_cone=(cone[0].module_relative_path,),
        )


def test_a_report_bound_to_another_target_is_refused() -> None:
    report = run_necessity_probe()
    with pytest.raises(MorphologicalNecessityMeasurementError):
        NecessityProbeReport(
            measurements=report.measurements,
            target_digest="0" * 64,
            pre_registered_expectation=report.pre_registered_expectation,
        )


def test_an_accepted_attempt_without_a_named_member_is_refused() -> None:
    with pytest.raises(MorphologicalNecessityMeasurementError):
        ReaderAttempt(
            reader_name="canonical_answer",
            surface="مِن",
            accepted=True,
            accepted_member=None,
            refusal_message=None,
        )


def test_a_refusal_without_the_domains_message_is_refused() -> None:
    with pytest.raises(MorphologicalNecessityMeasurementError):
        ReaderAttempt(
            reader_name="canonical_answer",
            surface="مِن",
            accepted=False,
            accepted_member=None,
            refusal_message="   ",
        )


def test_the_actual_result_is_recorded_as_it_fell() -> None:
    report = run_necessity_probe()
    assert [standing for _, standing in report.standing_by_pair] == [
        PairStanding.UNRESOLVED_MEASUREMENT_IMPOSSIBLE
    ] * 3
    assert report.matches_pre_registered_expectation is True


def test_the_module_declares_no_necessity_verdict() -> None:
    import alghanem.arabic.morphological_necessity_measurement as module

    assert not hasattr(module, "NEW_FORMAL_DOMAIN_IS_NECESSARY")
    assert "MEASURED_NEGATIVE_IS_NOT_A_CONSTITUTIONAL_NECESSITY" in NAMED_RESIDUALS
    assert "REFUSAL_IS_NOT_FAILURE_TO_DISCRIMINATE" in NAMED_RESIDUALS


def _first_reader_name(module_relative_path: str) -> str:
    from alghanem.arabic.morphological_necessity_measurement import _READERS_BY_MODULE

    return _READERS_BY_MODULE[module_relative_path][0][0]
