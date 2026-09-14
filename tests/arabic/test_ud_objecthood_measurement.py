"""Tests for the pre-registered objecthood measurement over the UD relation layer."""

from __future__ import annotations

from dataclasses import fields, replace

import pytest

from alghanem.arabic.ud_objecthood_measurement import (
    DEVELOPMENT_SPLIT_OBJECTHOOD_MEASUREMENT,
    FUNCTION_WORD_UPOS_TAGS,
    HELD_OUT_SPLIT_OBJECTHOOD_MEASUREMENT,
    OBJECTHOOD_MEASUREMENT_NAMED_RESIDUALS,
    ObjecthoodMeasurement,
    ObjecthoodMeasurementError,
    classify_position,
    predicts_object,
    read_final_short_vowel,
)
from alghanem.arabic.ud_objecthood_preregistration import (
    OBJECTHOOD_PREREGISTRATION,
    ObjecthoodDecision,
    ObjecthoodPositionOutcome,
)

_FATHA = "\u064e"
_DAMMA = "\u064f"
_KASRA = "\u0650"
_FATHATAN = "\u064b"
_SUKUN = "\u0652"

_MEASUREMENTS = (
    DEVELOPMENT_SPLIT_OBJECTHOOD_MEASUREMENT,
    HELD_OUT_SPLIT_OBJECTHOOD_MEASUREMENT,
)


def test_final_short_vowel_is_read_from_the_end() -> None:
    assert read_final_short_vowel(f"كَتَب{_FATHA}") == _FATHA
    assert read_final_short_vowel(f"كِتَاب{_KASRA}") == _KASRA
    assert read_final_short_vowel(f"قَادِر{_FATHATAN}ا") == _FATHATAN


def test_a_sukun_ending_stops_the_scan_rather_than_borrowing_an_earlier_vowel() -> None:
    assert read_final_short_vowel(f"كَتَب{_SUKUN}") is None
    assert predicts_object(f"كَتَب{_SUKUN}") is None


def test_an_unvocalized_form_is_unreadable_not_wrong() -> None:
    assert predicts_object("كتاب") is None
    assert classify_position("كتاب", "obj") is (
        ObjecthoodPositionOutcome.UNREADABLE_SURFACE
    )


def test_fatha_predicts_and_damma_does_not() -> None:
    assert predicts_object(f"كِتَاب{_FATHA}") is True
    assert predicts_object(f"كِتَاب{_DAMMA}") is False


def test_classification_uses_the_gold_relation_of_the_frozen_specification() -> None:
    assert classify_position(f"كِتَاب{_FATHA}", "obj") is (
        ObjecthoodPositionOutcome.PREDICTED_AND_IS_OBJECT
    )
    assert classify_position(f"كِتَاب{_FATHA}", "obl:arg") is (
        ObjecthoodPositionOutcome.PREDICTED_AND_IS_NOT_OBJECT
    )


def test_a_readable_unpredicted_position_is_refused_a_place_in_the_three_values() -> (
    None
):
    with pytest.raises(ObjecthoodMeasurementError):
        classify_position(f"كِتَاب{_DAMMA}", "obj")


def test_every_measurement_is_bound_to_the_live_specification_digest() -> None:
    for measurement in _MEASUREMENTS:
        assert measurement.preregistration_digest == (
            OBJECTHOOD_PREREGISTRATION.content_digest
        )


def test_a_measurement_bound_to_another_specification_cannot_be_built() -> None:
    with pytest.raises(ObjecthoodMeasurementError):
        replace(HELD_OUT_SPLIT_OBJECTHOOD_MEASUREMENT, preregistration_digest="0" * 64)


def test_the_four_positional_counts_exhaust_the_population() -> None:
    for measurement in _MEASUREMENTS:
        assert (
            measurement.predicted_and_is_object
            + measurement.predicted_and_is_not_object
            + measurement.unreadable_positions
            + measurement.readable_but_not_predicted
            == measurement.population
        )


def test_a_position_dropped_from_the_count_is_refused() -> None:
    with pytest.raises(ObjecthoodMeasurementError):
        replace(HELD_OUT_SPLIT_OBJECTHOOD_MEASUREMENT, unreadable_positions=0)


def test_the_two_error_genera_exhaust_the_errors() -> None:
    for measurement in _MEASUREMENTS:
        assert (
            measurement.function_word_errors + measurement.content_word_errors
            == measurement.predicted_and_is_not_object
        )
    with pytest.raises(ObjecthoodMeasurementError):
        replace(HELD_OUT_SPLIT_OBJECTHOOD_MEASUREMENT, function_word_errors=0)


def test_the_measurement_carries_no_stored_verdict_or_ratio() -> None:
    names = {field.name for field in fields(ObjecthoodMeasurement)}
    for forbidden in ("decision", "precision", "recall", "verdict"):
        assert not any(forbidden in name for name in names)


def test_the_claim_falls_on_both_splits_by_the_declared_threshold() -> None:
    for measurement in _MEASUREMENTS:
        assert measurement.precision_on_decided <= (
            OBJECTHOOD_PREREGISTRATION.claim_falls_at_or_below
        )
        assert measurement.decision is ObjecthoodDecision.CLAIM_REFUTED


def test_the_held_out_number_is_the_one_that_is_reported() -> None:
    held_out = HELD_OUT_SPLIT_OBJECTHOOD_MEASUREMENT
    assert held_out.witness.measured_path in OBJECTHOOD_PREREGISTRATION.held_out_files
    assert round(held_out.precision_on_decided, 4) == 0.358
    assert (
        DEVELOPMENT_SPLIT_OBJECTHOOD_MEASUREMENT.witness.measured_path
        in OBJECTHOOD_PREREGISTRATION.development_files
    )


def test_reach_is_reported_beside_precision_rather_than_hidden() -> None:
    for measurement in _MEASUREMENTS:
        assert 0.5 < measurement.recall_over_objects < 0.8
        assert 0.0 < measurement.unreadable_share < 0.2


def test_most_errors_are_function_words_on_the_held_out_split() -> None:
    held_out = HELD_OUT_SPLIT_OBJECTHOOD_MEASUREMENT
    assert held_out.function_word_error_share > 0.5
    assert "ADP" in FUNCTION_WORD_UPOS_TAGS
    assert "NOUN" not in FUNCTION_WORD_UPOS_TAGS


def test_a_hit_count_above_the_objects_present_is_refused() -> None:
    with pytest.raises(ObjecthoodMeasurementError):
        replace(HELD_OUT_SPLIT_OBJECTHOOD_MEASUREMENT, objects_in_population=10)


def test_the_specification_gap_is_named_rather_than_silently_amended() -> None:
    assert (
        "PreregisteredVocabularyCoversPredictedPositionsOnly"
        in OBJECTHOOD_MEASUREMENT_NAMED_RESIDUALS
    )
    assert (
        "FunctionWordsAreInThePopulationAsStated"
        in OBJECTHOOD_MEASUREMENT_NAMED_RESIDUALS
    )
    assert "AdjacencyIsNotGovernment" in OBJECTHOOD_MEASUREMENT_NAMED_RESIDUALS
    for note in OBJECTHOOD_MEASUREMENT_NAMED_RESIDUALS.values():
        assert note.strip()


def test_the_witnesses_are_the_step_zero_deposits_not_new_ones() -> None:
    from alghanem.arabic.ud_relation_layer_step0 import (
        UD_ARABIC_PADT_DEV_CENSUS,
        UD_ARABIC_PADT_TEST_CENSUS,
    )

    assert DEVELOPMENT_SPLIT_OBJECTHOOD_MEASUREMENT.witness == (
        UD_ARABIC_PADT_DEV_CENSUS.witness
    )
    assert HELD_OUT_SPLIT_OBJECTHOOD_MEASUREMENT.witness == (
        UD_ARABIC_PADT_TEST_CENSUS.witness
    )


def test_the_population_is_smaller_than_the_accusatives_already_counted() -> None:
    from alghanem.arabic.ud_relation_layer_step0 import UD_ARABIC_PADT_TEST_CENSUS

    assert (
        HELD_OUT_SPLIT_OBJECTHOOD_MEASUREMENT.population
        < UD_ARABIC_PADT_TEST_CENSUS.accusative_tokens
    )
