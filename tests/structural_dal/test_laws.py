"""قوانينُ `G0.SDAL-0` وشروطُ قبولها: مُجمَّدةٌ قبل القياس، وبلا عددٍ متوقَّع."""

from __future__ import annotations

import pytest

from alghanem.structural_dal import (
    PREREGISTRATION_DIGEST,
    STRUCTURAL_ACCEPTANCE_CONDITIONS,
    STRUCTURAL_DAL_LAWS,
    STRUCTURAL_TRANSITION_CONTRACT_FIELDS,
    ZERO_ONE_BOUND,
    AcceptanceItem,
    OutputContractComponent,
    Scale,
    StructuralDalError,
    condition_named,
)
from alghanem.structural_dal.laws import preregistration_digest


def test_the_digest_is_derived_not_written() -> None:
    assert PREREGISTRATION_DIGEST == preregistration_digest()
    assert len(PREREGISTRATION_DIGEST) == 64


def test_the_two_scales_carry_their_own_slot_counts() -> None:
    assert Scale.ZERO.slot_count == 1
    assert Scale.ONE.slot_count == 2
    assert ZERO_ONE_BOUND == max(scale.slot_count for scale in Scale)


def test_the_transition_contract_is_the_declared_seven() -> None:
    assert STRUCTURAL_TRANSITION_CONTRACT_FIELDS == (
        "input_identity",
        "difference",
        "invariant",
        "gate",
        "output_identity",
        "residual",
        "trace",
    )


def test_every_acceptance_condition_names_its_disqualifier() -> None:
    for condition in STRUCTURAL_ACCEPTANCE_CONDITIONS:
        assert condition.disqualifier.strip()
        assert condition_named(condition.condition_id) is condition


def test_an_unregistered_condition_is_refused_by_name() -> None:
    with pytest.raises(StructuralDalError):
        condition_named("SDAL0.NOT_REGISTERED")


def test_the_laws_are_distinct_and_non_empty() -> None:
    assert len(set(STRUCTURAL_DAL_LAWS)) == len(STRUCTURAL_DAL_LAWS)
    assert all(law.strip() for law in STRUCTURAL_DAL_LAWS)


def test_the_eight_acceptance_items_are_distinct() -> None:
    values = [item.value for item in AcceptanceItem]
    assert len(set(values)) == len(values) == 8


def test_the_output_contract_has_five_named_components() -> None:
    values = [component.value for component in OutputContractComponent]
    assert len(set(values)) == len(values) == 5


def test_no_expected_count_is_frozen_in_the_registration() -> None:
    from alghanem.structural_dal import laws

    for name in vars(laws):
        assert not name.startswith("EXPECTED")
        assert not name.endswith("_EXPECTED_COUNT")
