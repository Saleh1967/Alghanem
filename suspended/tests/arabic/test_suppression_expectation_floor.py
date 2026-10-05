"""Witnesses for the suppression expectation floor: null, floor, contributors."""

from __future__ import annotations

import pytest

from alghanem.arabic import suppression_expectation_floor as module
from alghanem.arabic.suppression_expectation_floor import (
    SUPPRESSION_FLOOR_NAMED_RESIDUALS,
    THE_CONTRACT_REGISTER,
    THE_NAMED_UNDEPOSITED_TESTS,
    NullHypothesis,
    SuppressionContract,
    SuppressionFloorError,
    SuppressionStanding,
    TypeContributor,
    contract_for,
    read_zero_cell,
)


def _a_complete_contract(**overrides: object) -> SuppressionContract:
    fields: dict[str, object] = {
        "test_identity": "عقدٌ-للشهادة",
        "null_hypothesis": NullHypothesis.INDEPENDENT_MARGINALS,
        "minimum_expectation": 5.0,
        "type_contributors": (
            TypeContributor(type_key="نمط-أ", occurrences=4),
            TypeContributor(type_key="نمط-ب", occurrences=6),
        ),
    }
    fields.update(overrides)
    return SuppressionContract(**fields)  # type: ignore[arg-type]


# --- nothing is read without all three deposits ----------------------------


def test_a_contract_without_a_contributor_distribution_is_refused() -> None:
    with pytest.raises(SuppressionFloorError):
        _a_complete_contract(type_contributors=())


def test_a_contract_without_a_positive_expectation_floor_is_refused() -> None:
    with pytest.raises(SuppressionFloorError):
        _a_complete_contract(minimum_expectation=0.0)


def test_a_contract_repeating_a_contributor_key_is_refused() -> None:
    with pytest.raises(SuppressionFloorError):
        _a_complete_contract(
            type_contributors=(
                TypeContributor(type_key="نمط-أ", occurrences=1),
                TypeContributor(type_key="نمط-أ", occurrences=2),
            )
        )


def test_the_null_hypothesis_is_a_declared_choice_of_two() -> None:
    assert len(NullHypothesis) == 2


# --- a zero under the floor is an empty cell, not a suppression ------------


def test_a_zero_beneath_the_expectation_floor_reads_as_an_empty_cell() -> None:
    reading = read_zero_cell(_a_complete_contract(), observed=0, expected=0.4)
    assert reading.standing is SuppressionStanding.EMPTY_CELL


def test_a_zero_above_the_expectation_floor_reads_as_a_suppression() -> None:
    reading = read_zero_cell(_a_complete_contract(), observed=0, expected=12.0)
    assert reading.standing is SuppressionStanding.SUPPRESSION


def test_a_nonzero_outside_the_declared_band_is_withheld_not_called_near_zero() -> None:
    reading = read_zero_cell(_a_complete_contract(), observed=3, expected=12.0)
    assert reading.standing is (SuppressionStanding.WITHHELD_FOR_AN_INCOMPLETE_CONTRACT)


def test_a_declared_near_zero_band_admits_what_it_declares_and_no_more() -> None:
    contract = _a_complete_contract(near_zero_band=2)
    assert (
        read_zero_cell(contract, observed=2, expected=12.0).standing
        is SuppressionStanding.SUPPRESSION
    )
    assert (
        read_zero_cell(contract, observed=3, expected=12.0).standing
        is SuppressionStanding.WITHHELD_FOR_AN_INCOMPLETE_CONTRACT
    )


def test_the_expectation_is_examined_before_the_observation() -> None:
    contract = _a_complete_contract(near_zero_band=0)
    reading = read_zero_cell(contract, observed=9, expected=0.1)
    assert reading.standing is SuppressionStanding.EMPTY_CELL


# --- every reading publishes its largest contributor share -----------------


def test_every_reading_carries_the_largest_contributor_share() -> None:
    reading = read_zero_cell(_a_complete_contract(), observed=0, expected=12.0)
    assert reading.largest_contributor_share == pytest.approx(6 / 10)


# --- the register is empty and the named test is refused by name -----------


def test_the_contract_register_is_empty_on_this_evidence() -> None:
    assert THE_CONTRACT_REGISTER == ()


def test_the_filtered_cvc_test_is_named_and_refused_rather_than_unknown() -> None:
    assert "filtered-cvc-4747" in THE_NAMED_UNDEPOSITED_TESTS
    with pytest.raises(SuppressionFloorError, match="مسمًّى"):
        contract_for("filtered-cvc-4747")


def test_an_unnamed_test_is_refused_too_but_not_as_a_named_one() -> None:
    with pytest.raises(SuppressionFloorError) as raised:
        contract_for("لا-اختبار")
    assert "مسمًّى" not in str(raised.value)


# --- house guards ----------------------------------------------------------


def test_every_named_residual_begins_with_its_own_key() -> None:
    for key, text in SUPPRESSION_FLOOR_NAMED_RESIDUALS.items():
        assert text.startswith(f"{key}: ")


def test_no_probability_name_is_exported_from_this_module() -> None:
    banned = ("entropy", "markov", "likelihood", "transition_matrix")
    for exported in module.__all__:
        assert not any(word in exported.lower() for word in banned)
