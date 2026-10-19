"""Witnesses for the sukun state contract: two states, one eviction, no merged total."""

from __future__ import annotations

import pytest

from alghanem.arabic import sukun_state_contract as module
from alghanem.arabic.implicit_sukun_treatment import (
    SukunSource,
    measured_text_census,
)
from alghanem.arabic.sukun_second_scope import second_text_census
from alghanem.arabic.sukun_state_contract import (
    SUKUN_STATE_NAMED_RESIDUALS,
    NonSukunCategory,
    SukunState,
    SukunStateContractError,
    SukunStateSplit,
    refuse_a_merged_total,
    split_of,
    the_state_space_of,
    the_sukun_splits,
)

# --- the split is the measured census redistributed ------------------------


def test_the_two_splits_are_derived_from_the_two_deposited_censuses() -> None:
    scopes = {split.scope for split in the_sukun_splits()}
    assert scopes == {measured_text_census().scope, second_text_census().scope}


def test_the_written_state_is_exactly_the_explicit_mark_count() -> None:
    for split, census in zip(
        the_sukun_splits(),
        (measured_text_census(), second_text_census()),
        strict=True,
    ):
        assert split.written == dict(census.by_source)[SukunSource.EXPLICIT_MARK]


def test_the_inferred_state_is_the_alif_and_the_bare_carrier_together() -> None:
    for split, census in zip(
        the_sukun_splits(),
        (measured_text_census(), second_text_census()),
        strict=True,
    ):
        counted = dict(census.by_source)
        assert split.inferred == (
            counted[SukunSource.ALIF_WITHOUT_A_MARK] + counted[SukunSource.BARE_CARRIER]
        )


def test_the_measured_split_matches_what_the_prose_publishes() -> None:
    published = {
        measured_text_census().scope: (21, 40, 14, 75),
        second_text_census().scope: (27, 61, 16, 104),
    }
    for split in the_sukun_splits():
        assert (
            split.written,
            split.inferred,
            split.evicted,
            split.raw_column,
        ) == published[split.scope]


# --- two states, not one ---------------------------------------------------


def test_the_state_space_holds_exactly_the_two_sukun_states() -> None:
    for split in the_sukun_splits():
        assert set(the_state_space_of(split.scope)) == set(SukunState)
        assert len(the_state_space_of(split.scope)) == 2


def test_the_written_and_the_inferred_are_never_summed_into_one_state() -> None:
    for split in the_sukun_splits():
        states = the_state_space_of(split.scope)
        assert states[SukunState.WRITTEN_SUKUN] != split.in_state_space
        assert states[SukunState.INFERRED_SUKUN] != split.in_state_space


# --- the gemination first half is evicted, not subclassed ------------------


def test_the_gemination_first_half_is_outside_the_sukun_state_space() -> None:
    assert {member.name for member in NonSukunCategory}.isdisjoint(
        {member.name for member in SukunState}
    )
    assert NonSukunCategory.GEMINATION_FIRST_HALF not in set(SukunState)


def test_the_eviction_lowers_the_state_space_below_the_raw_column() -> None:
    for split in the_sukun_splits():
        assert split.in_state_space == split.raw_column - split.evicted
        assert split.in_state_space < split.raw_column


# --- no single total is issued ---------------------------------------------


def test_a_merged_column_total_is_always_refused_and_names_its_three_parts() -> None:
    for split in the_sukun_splits():
        with pytest.raises(SukunStateContractError) as raised:
            refuse_a_merged_total(split.scope)
        message = str(raised.value)
        assert str(split.written) in message
        assert str(split.inferred) in message
        assert str(split.evicted) in message


def test_an_unmeasured_scope_is_refused_rather_than_answered() -> None:
    with pytest.raises(SukunStateContractError):
        split_of("نطاقٌ لم يُقَس")


def test_a_split_that_does_not_exhaust_its_column_is_refused() -> None:
    with pytest.raises(SukunStateContractError):
        SukunStateSplit(scope="مختلق", written=1, inferred=1, evicted=1, raw_column=9)


# --- house guards ----------------------------------------------------------


def test_every_named_residual_begins_with_its_own_key() -> None:
    for key, text in SUKUN_STATE_NAMED_RESIDUALS.items():
        assert text.startswith(f"{key}: ")


def test_the_module_exports_no_probability_name() -> None:
    banned = ("entropy", "markov", "likelihood", "transition_matrix")
    for exported in module.__all__:
        assert not any(word in exported.lower() for word in banned)
