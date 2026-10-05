"""Witnesses for the composition ordering law: commutes, order required, unresolved."""

from __future__ import annotations

import pytest

from alghanem.arabic import projection_composition_order as module
from alghanem.arabic.carrier_projection_deposit import (
    THE_DEPOSITS_PROJECTED,
    WordBoundary,
)
from alghanem.arabic.fath_ayah_source_text import FATH_AYAH_SOURCE_ID
from alghanem.arabic.fatiha_source_text import FATIHA_SOURCE_ID
from alghanem.arabic.projection_composition_order import (
    COMPOSITION_ORDER_NAMED_RESIDUALS,
    THE_ORDER_REGISTER,
    CompositionOrderError,
    CompositionStanding,
    DepositedOrder,
    LegalSide,
    OrderFinding,
    classify_composition,
    the_composition_table,
    usable_for_composition,
)
from alghanem.arabic.projection_identity_certificate import (
    the_fold_and_the_boundary_commute_on,
)

# --- the classification is measured, not asserted --------------------------


@pytest.mark.parametrize("source_id", sorted(THE_DEPOSITS_PROJECTED))
@pytest.mark.parametrize("boundary", list(WordBoundary))
def test_a_cell_is_commuting_exactly_when_the_certificate_measures_it_so(
    source_id: str, boundary: WordBoundary
) -> None:
    commutes = the_fold_and_the_boundary_commute_on(source_id, boundary)
    finding = classify_composition(source_id, boundary)
    assert (finding.standing is CompositionStanding.COMMUTES) is commutes


def test_the_table_covers_every_deposit_and_every_boundary_once() -> None:
    cells = {
        (finding.source_identity, finding.boundary_rule)
        for finding in the_composition_table()
    }
    assert len(cells) == len(the_composition_table())
    assert len(cells) == len(THE_DEPOSITS_PROJECTED) * len(WordBoundary)


# --- a failure to commute does not itself deposit an order -----------------


def test_the_one_broken_cell_is_the_fatiha_under_the_space_only_rule() -> None:
    broken = [
        finding
        for finding in the_composition_table()
        if finding.standing is not CompositionStanding.COMMUTES
    ]
    assert len(broken) == 1
    assert broken[0].source_identity == FATIHA_SOURCE_ID
    assert broken[0].boundary_rule is WordBoundary.SPACE_ONLY


def test_the_broken_cell_is_unresolved_and_not_promoted_to_order_required() -> None:
    finding = classify_composition(FATIHA_SOURCE_ID, WordBoundary.SPACE_ONLY)
    assert finding.standing is CompositionStanding.UNRESOLVED
    assert finding.legal_side is None


def test_the_order_register_is_empty_on_this_evidence() -> None:
    assert THE_ORDER_REGISTER == ()


def test_the_one_line_deposit_commutes_under_both_boundary_rules() -> None:
    for boundary in WordBoundary:
        finding = classify_composition(FATH_AYAH_SOURCE_ID, boundary)
        assert finding.standing is CompositionStanding.COMMUTES


# --- a known order, not a commuting one ------------------------------------


def test_what_is_unusable_is_exactly_what_is_unresolved() -> None:
    for finding in the_composition_table():
        unusable = not usable_for_composition(
            finding.source_identity, finding.boundary_rule
        )
        assert unusable is (finding.standing is CompositionStanding.UNRESOLVED)


def test_an_order_required_finding_without_a_legal_side_is_refused() -> None:
    with pytest.raises(CompositionOrderError):
        OrderFinding(
            source_identity=FATIHA_SOURCE_ID,
            boundary_rule=WordBoundary.SPACE_ONLY,
            standing=CompositionStanding.ORDER_REQUIRED,
            ground="سند",
        )


def test_a_commuting_finding_may_not_carry_a_legal_side() -> None:
    with pytest.raises(CompositionOrderError):
        OrderFinding(
            source_identity=FATIHA_SOURCE_ID,
            boundary_rule=WordBoundary.ANY_WHITESPACE,
            standing=CompositionStanding.COMMUTES,
            ground="سند",
            legal_side=LegalSide.BOUNDARY_THEN_FOLD,
        )


def test_a_deposited_order_without_a_written_ground_is_refused() -> None:
    with pytest.raises(CompositionOrderError):
        DepositedOrder(
            source_identity=FATIHA_SOURCE_ID,
            boundary_rule=WordBoundary.SPACE_ONLY,
            legal_side=LegalSide.BOUNDARY_THEN_FOLD,
            ground="   ",
        )


def test_a_deposited_order_for_an_unmeasured_source_is_refused() -> None:
    with pytest.raises(CompositionOrderError):
        DepositedOrder(
            source_identity="no-such-deposit",
            boundary_rule=WordBoundary.SPACE_ONLY,
            legal_side=LegalSide.FOLD_THEN_BOUNDARY,
            ground="سند",
        )


# --- the table is measured and not generalized -----------------------------


def test_an_unmeasured_source_is_refused_rather_than_classified() -> None:
    with pytest.raises(CompositionOrderError):
        classify_composition("no-such-deposit", WordBoundary.ANY_WHITESPACE)


# --- house guards ----------------------------------------------------------


def test_the_three_standings_are_distinct_values() -> None:
    assert len({member.value for member in CompositionStanding}) == 3


def test_every_named_residual_begins_with_its_own_key() -> None:
    for key, text in COMPOSITION_ORDER_NAMED_RESIDUALS.items():
        assert text.startswith(f"{key}: ")


def test_the_module_exports_no_probability_name() -> None:
    banned = ("entropy", "markov", "likelihood", "transition_matrix")
    for exported in module.__all__:
        assert not any(word in exported.lower() for word in banned)
