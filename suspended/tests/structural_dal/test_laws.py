"""قوانينُ `G0.SDAL-0` وشروطُ قبولها: مُجمَّدةٌ قبل القياس، وبلا عددٍ متوقَّع."""

from __future__ import annotations

import pytest

from alghanem.structural_dal import (
    NO_BRANCH_BIRTH_WITHOUT_EXTERNAL_CERTIFICATE,
    NO_IMPLICIT_IDENTITY_MODE,
    NO_POSITIVE_STRUCTURE_FROM_NEUTRAL_INPUT,
    PREREGISTRATION_DIGEST,
    SELF_DEFINED_CONTRACT_DOES_NOT_ESTABLISH_COMPARATIVE_STRENGTH,
    STRUCTURAL_ACCEPTANCE_CONDITIONS,
    STRUCTURAL_DAL_LAWS,
    STRUCTURAL_OPERATOR_PROOF_IS_ONLY_ELIGIBLE_FOR_FIBER_INTEGRATION,
    STRUCTURAL_TRANSITION_CONTRACT_FIELDS,
    THE_PART_HAS_ITS_OWN_IDENTITY,
    UNPROVED_ROLE_BASIS_IS_BLOCKING,
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


def test_the_acceptance_items_are_distinct_without_a_frozen_count() -> None:
    values = [item.value for item in AcceptanceItem]
    assert len(set(values)) == len(values)
    assert values


def test_the_output_contract_has_five_named_components() -> None:
    values = [component.value for component in OutputContractComponent]
    assert len(set(values)) == len(values) == 5


def test_no_expected_count_is_frozen_in_the_registration() -> None:
    from alghanem.structural_dal import laws

    for name in vars(laws):
        assert not name.startswith("EXPECTED")
        assert not name.endswith("_EXPECTED_COUNT")


def test_the_hardening_laws_are_registered_in_the_frozen_set() -> None:
    for law in (
        NO_POSITIVE_STRUCTURE_FROM_NEUTRAL_INPUT,
        UNPROVED_ROLE_BASIS_IS_BLOCKING,
        THE_PART_HAS_ITS_OWN_IDENTITY,
        NO_IMPLICIT_IDENTITY_MODE,
        NO_BRANCH_BIRTH_WITHOUT_EXTERNAL_CERTIFICATE,
        SELF_DEFINED_CONTRACT_DOES_NOT_ESTABLISH_COMPARATIVE_STRENGTH,
        STRUCTURAL_OPERATOR_PROOF_IS_ONLY_ELIGIBLE_FOR_FIBER_INTEGRATION,
    ):
        assert law in STRUCTURAL_DAL_LAWS


def test_the_layer_claims_only_eligibility_for_fiber_integration() -> None:
    from alghanem.structural_dal import laws

    assert "ArabicProjection" not in laws.__doc__
    assert "RootCandidate" not in laws.__doc__
    assert "EligibleForFiberIntegration" in laws.__doc__
