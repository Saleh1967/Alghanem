"""Tests for the amendment that corrects the two named defects."""

from __future__ import annotations

from dataclasses import fields, replace

import pytest

from alghanem.arabic.ud_objecthood_amendment import (
    AMENDED_DEVELOPMENT_SPLIT_MEASUREMENT,
    AMENDED_HELD_OUT_SPLIT_MEASUREMENT,
    AMENDED_OBJECTHOOD_SPECIFICATION,
    AMENDMENT_NAMED_RESIDUALS,
    AmendedObjecthoodMeasurement,
    AmendedPositionOutcome,
    AmendmentStanding,
    classify_amended_position,
    is_function_word,
)
from alghanem.arabic.ud_objecthood_measurement import (
    FUNCTION_WORD_UPOS_TAGS,
    HELD_OUT_SPLIT_OBJECTHOOD_MEASUREMENT,
    ObjecthoodMeasurementError,
)
from alghanem.arabic.ud_objecthood_preregistration import (
    OBJECTHOOD_PREREGISTRATION,
    ObjecthoodDecision,
    ObjecthoodPositionOutcome,
)

_FATHA = "\u064e"
_DAMMA = "\u064f"

_AMENDED = (
    AMENDED_DEVELOPMENT_SPLIT_MEASUREMENT,
    AMENDED_HELD_OUT_SPLIT_MEASUREMENT,
)


def test_the_first_specification_is_untouched_by_the_amendment() -> None:
    assert len(ObjecthoodPositionOutcome) == 3
    assert AMENDED_OBJECTHOOD_SPECIFICATION.amends_digest == (
        OBJECTHOOD_PREREGISTRATION.content_digest
    )
    assert AMENDED_OBJECTHOOD_SPECIFICATION.content_digest != (
        OBJECTHOOD_PREREGISTRATION.content_digest
    )


def test_the_as_stated_measurement_still_stands_at_its_own_number() -> None:
    assert round(HELD_OUT_SPLIT_OBJECTHOOD_MEASUREMENT.precision_on_decided, 4) == 0.358
    assert HELD_OUT_SPLIT_OBJECTHOOD_MEASUREMENT.decision is (
        ObjecthoodDecision.CLAIM_REFUTED
    )


def test_the_amendment_cannot_claim_the_stronger_standing() -> None:
    assert AMENDED_OBJECTHOOD_SPECIFICATION.standing is (
        AmendmentStanding.AMENDED_AFTER_THE_NUMBER
    )
    with pytest.raises(ObjecthoodMeasurementError):
        replace(
            AMENDED_OBJECTHOOD_SPECIFICATION,
            standing=AmendmentStanding.PRIOR_TO_EVIDENCE,
        )


def test_an_amendment_that_does_not_name_its_original_is_refused() -> None:
    with pytest.raises(ObjecthoodMeasurementError):
        replace(AMENDED_OBJECTHOOD_SPECIFICATION, amends_digest="0" * 64)


def test_both_named_defects_are_declared_as_corrected() -> None:
    assert set(AMENDED_OBJECTHOOD_SPECIFICATION.corrected_defects) == {
        "FunctionWordsAreInThePopulationAsStated",
        "PreregisteredVocabularyCoversPredictedPositionsOnly",
    }


def test_the_vocabulary_defect_is_corrected_by_a_fourth_value() -> None:
    assert len(AmendedPositionOutcome) == 4
    assert classify_amended_position(f"كِتَاب{_DAMMA}", "obj") is (
        AmendedPositionOutcome.READABLE_BUT_NOT_PREDICTED
    )


def test_the_corrected_vocabulary_no_longer_raises_on_that_position() -> None:
    from alghanem.arabic.ud_objecthood_measurement import classify_position

    with pytest.raises(ObjecthoodMeasurementError):
        classify_position(f"كِتَاب{_DAMMA}", "obj")
    assert classify_amended_position(f"كِتَاب{_DAMMA}", "obj") is (
        AmendedPositionOutcome.READABLE_BUT_NOT_PREDICTED
    )


def test_the_population_defect_is_corrected_by_the_same_declared_list() -> None:
    assert is_function_word("ADP")
    assert is_function_word("SCONJ")
    assert not is_function_word("NOUN")
    assert AMENDED_OBJECTHOOD_SPECIFICATION.excluded_upos == FUNCTION_WORD_UPOS_TAGS


def test_a_second_hand_picked_exclusion_list_is_refused() -> None:
    with pytest.raises(ObjecthoodMeasurementError):
        replace(AMENDED_OBJECTHOOD_SPECIFICATION, excluded_upos=frozenset({"ADP"}))


def test_the_thresholds_were_not_moved_to_fit_the_new_number() -> None:
    assert AMENDED_OBJECTHOOD_SPECIFICATION.claim_stands_at_or_above == (
        OBJECTHOOD_PREREGISTRATION.claim_stands_at_or_above
    )
    assert AMENDED_OBJECTHOOD_SPECIFICATION.claim_falls_at_or_below == (
        OBJECTHOOD_PREREGISTRATION.claim_falls_at_or_below
    )


def test_the_correction_does_not_rescue_the_claim() -> None:
    held_out = AMENDED_HELD_OUT_SPLIT_MEASUREMENT
    assert round(held_out.precision_on_decided, 4) == 0.6447
    assert held_out.decision is ObjecthoodDecision.CLAIM_UNDECIDED_IN_BAND
    assert held_out.precision_on_decided < (
        AMENDED_OBJECTHOOD_SPECIFICATION.claim_stands_at_or_above
    )


def test_the_two_splits_disagree_under_the_amendment() -> None:
    assert AMENDED_DEVELOPMENT_SPLIT_MEASUREMENT.decision is (
        ObjecthoodDecision.CLAIM_REFUTED
    )
    assert AMENDED_HELD_OUT_SPLIT_MEASUREMENT.decision is (
        ObjecthoodDecision.CLAIM_UNDECIDED_IN_BAND
    )
    assert "TheTwoSplitsDisagreeUnderTheAmendment" in AMENDMENT_NAMED_RESIDUALS


def test_the_correction_raises_precision_on_both_splits() -> None:
    from alghanem.arabic.ud_objecthood_measurement import (
        DEVELOPMENT_SPLIT_OBJECTHOOD_MEASUREMENT,
    )

    assert (
        AMENDED_DEVELOPMENT_SPLIT_MEASUREMENT.precision_on_decided
        > DEVELOPMENT_SPLIT_OBJECTHOOD_MEASUREMENT.precision_on_decided
    )
    assert (
        AMENDED_HELD_OUT_SPLIT_MEASUREMENT.precision_on_decided
        > HELD_OUT_SPLIT_OBJECTHOOD_MEASUREMENT.precision_on_decided
    )


def test_the_exclusion_also_removes_objects_and_says_so() -> None:
    from alghanem.arabic.ud_objecthood_measurement import (
        DEVELOPMENT_SPLIT_OBJECTHOOD_MEASUREMENT,
    )

    assert AMENDED_HELD_OUT_SPLIT_MEASUREMENT.objects_lost_to_the_exclusion == 4
    assert (
        AMENDED_HELD_OUT_SPLIT_MEASUREMENT.objects_in_population
        + AMENDED_HELD_OUT_SPLIT_MEASUREMENT.objects_lost_to_the_exclusion
        == HELD_OUT_SPLIT_OBJECTHOOD_MEASUREMENT.objects_in_population
    )
    assert (
        AMENDED_DEVELOPMENT_SPLIT_MEASUREMENT.objects_in_population
        + AMENDED_DEVELOPMENT_SPLIT_MEASUREMENT.objects_lost_to_the_exclusion
        == DEVELOPMENT_SPLIT_OBJECTHOOD_MEASUREMENT.objects_in_population
    )


def test_reach_did_not_improve_with_the_correction() -> None:
    assert (
        AMENDED_HELD_OUT_SPLIT_MEASUREMENT.recall_over_objects
        < HELD_OUT_SPLIT_OBJECTHOOD_MEASUREMENT.recall_over_objects
    )


def test_the_four_positional_counts_exhaust_the_amended_population() -> None:
    for measurement in _AMENDED:
        assert (
            measurement.predicted_and_is_object
            + measurement.predicted_and_is_not_object
            + measurement.unreadable_positions
            + measurement.readable_but_not_predicted
            == measurement.population
        )
    with pytest.raises(ObjecthoodMeasurementError):
        replace(AMENDED_HELD_OUT_SPLIT_MEASUREMENT, unreadable_positions=0)


def test_every_amended_measurement_is_bound_to_the_amended_digest() -> None:
    for measurement in _AMENDED:
        assert measurement.amended_specification_digest == (
            AMENDED_OBJECTHOOD_SPECIFICATION.content_digest
        )
    with pytest.raises(ObjecthoodMeasurementError):
        replace(
            AMENDED_HELD_OUT_SPLIT_MEASUREMENT, amended_specification_digest="0" * 64
        )


def test_the_amended_measurement_carries_no_stored_verdict_or_ratio() -> None:
    names = {field.name for field in fields(AmendedObjecthoodMeasurement)}
    for forbidden in ("decision", "precision", "recall", "verdict"):
        assert not any(forbidden in name for name in names)


def test_the_cost_of_the_correction_is_named() -> None:
    assert "TheAmendedPopulationIsDefinedByTheAnnotation" in AMENDMENT_NAMED_RESIDUALS
    assert "TheFrozenSpecificationIsNotEdited" in AMENDMENT_NAMED_RESIDUALS
    assert (
        "AnAmendmentAfterTheNumberIsWeakerThanAPreregistration"
        in AMENDMENT_NAMED_RESIDUALS
    )
    for note in AMENDMENT_NAMED_RESIDUALS.values():
        assert note.strip()


def test_a_fatha_still_predicts_under_the_amendment() -> None:
    assert classify_amended_position(f"كِتَاب{_FATHA}", "obj") is (
        AmendedPositionOutcome.PREDICTED_AND_IS_OBJECT
    )
    assert classify_amended_position(f"كِتَاب{_FATHA}", "obl:arg") is (
        AmendedPositionOutcome.PREDICTED_AND_IS_NOT_OBJECT
    )
