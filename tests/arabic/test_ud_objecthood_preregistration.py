"""Tests for the frozen pre-registration of the objecthood measurement."""

from __future__ import annotations

from dataclasses import fields, replace

import pytest

from alghanem.arabic.ud_objecthood_preregistration import (
    OBJECTHOOD_PREREGISTRATION,
    OBJECTHOOD_PREREGISTRATION_NAMED_RESIDUALS,
    FrozenObjecthoodPreregistration,
    ObjecthoodDecision,
    ObjecthoodPositionOutcome,
    ObjecthoodPreregistrationError,
)


def test_position_outcome_vocabulary_is_closed_at_three_values() -> None:
    assert len(ObjecthoodPositionOutcome) == 3
    assert ObjecthoodPositionOutcome.UNREADABLE_SURFACE not in (
        ObjecthoodPositionOutcome.PREDICTED_AND_IS_OBJECT,
        ObjecthoodPositionOutcome.PREDICTED_AND_IS_NOT_OBJECT,
    )


def test_decision_vocabulary_keeps_an_undecided_band() -> None:
    assert len(ObjecthoodDecision) == 3


def test_the_specification_carries_no_result_field() -> None:
    names = {field.name for field in fields(FrozenObjecthoodPreregistration)}
    for forbidden in ("precision", "accuracy", "outcome", "decision", "correct"):
        assert not any(forbidden in name for name in names)


def test_thresholds_were_declared_before_any_number() -> None:
    assert OBJECTHOOD_PREREGISTRATION.claim_falls_at_or_below < (
        OBJECTHOOD_PREREGISTRATION.claim_stands_at_or_above
    )
    assert OBJECTHOOD_PREREGISTRATION.decide(0.95) is ObjecthoodDecision.CLAIM_UPHELD
    assert OBJECTHOOD_PREREGISTRATION.decide(0.3) is ObjecthoodDecision.CLAIM_REFUTED
    assert OBJECTHOOD_PREREGISTRATION.decide(0.75) is (
        ObjecthoodDecision.CLAIM_UNDECIDED_IN_BAND
    )


def test_decision_boundaries_are_inclusive_as_written() -> None:
    assert (
        OBJECTHOOD_PREREGISTRATION.decide(
            OBJECTHOOD_PREREGISTRATION.claim_stands_at_or_above
        )
        is ObjecthoodDecision.CLAIM_UPHELD
    )
    assert (
        OBJECTHOOD_PREREGISTRATION.decide(
            OBJECTHOOD_PREREGISTRATION.claim_falls_at_or_below
        )
        is ObjecthoodDecision.CLAIM_REFUTED
    )


def test_a_ratio_outside_the_unit_interval_is_refused() -> None:
    with pytest.raises(ObjecthoodPreregistrationError):
        OBJECTHOOD_PREREGISTRATION.decide(1.5)


def test_development_and_held_out_files_do_not_overlap() -> None:
    assert not set(OBJECTHOOD_PREREGISTRATION.development_files) & set(
        OBJECTHOOD_PREREGISTRATION.held_out_files
    )
    with pytest.raises(ObjecthoodPreregistrationError):
        replace(
            OBJECTHOOD_PREREGISTRATION,
            held_out_files=OBJECTHOOD_PREREGISTRATION.development_files,
        )


def test_equal_thresholds_are_refused_because_they_erase_the_band() -> None:
    with pytest.raises(ObjecthoodPreregistrationError):
        replace(
            OBJECTHOOD_PREREGISTRATION,
            claim_falls_at_or_below=OBJECTHOOD_PREREGISTRATION.claim_stands_at_or_above,
        )


def test_the_column_fed_is_named_rather_than_assumed() -> None:
    assert OBJECTHOOD_PREREGISTRATION.surface_column == "MISC:Vform"


def test_the_gold_relation_is_the_schema_label_not_a_paraphrase() -> None:
    assert OBJECTHOOD_PREREGISTRATION.gold_relation == "obj"


def test_refused_readings_are_named_before_the_number_exists() -> None:
    assert len(OBJECTHOOD_PREREGISTRATION.refused_readings) >= 4


def test_content_digest_changes_with_any_edit_to_the_specification() -> None:
    original = OBJECTHOOD_PREREGISTRATION.content_digest
    assert len(original) == 64
    edited = replace(OBJECTHOOD_PREREGISTRATION, claim_stands_at_or_above=0.91)
    assert edited.content_digest != original


def test_named_residuals_include_what_was_already_seen() -> None:
    assert (
        "StepZeroCountsWereKnownBeforeThisPreregistration"
        in OBJECTHOOD_PREREGISTRATION_NAMED_RESIDUALS
    )
    assert (
        "ObjIsUdObjecthoodNotClassicalMaful"
        in OBJECTHOOD_PREREGISTRATION_NAMED_RESIDUALS
    )
    for note in OBJECTHOOD_PREREGISTRATION_NAMED_RESIDUALS.values():
        assert note.strip()


def test_a_blank_clause_is_refused() -> None:
    with pytest.raises(ObjecthoodPreregistrationError):
        replace(OBJECTHOOD_PREREGISTRATION, predictor_rule="   ")


def test_an_empty_split_is_refused() -> None:
    with pytest.raises(ObjecthoodPreregistrationError):
        replace(OBJECTHOOD_PREREGISTRATION, development_files=())


def test_this_module_reads_no_measurement() -> None:
    import alghanem.arabic.ud_objecthood_preregistration as module

    source = module.__doc__ or ""
    assert "A_PREREGISTRATION_IS_NOT_A_MEASUREMENT" in source
