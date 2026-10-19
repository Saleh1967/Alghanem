"""المربّعُ التبادليّ لكلّ انتقال؛ وميدانان تغطيةٌ لا استقلالُ تمثيل."""

from __future__ import annotations

import pytest
from builders import realization, specification

from alghanem.metaalgebra.commutation import (
    CommutationObligation,
    CommutationObligationError,
    RepresentationIndependenceObligation,
)
from alghanem.metaalgebra.transition import TransitionOutcome


def _obligation(
    obligation_id: str = "sq.alpha.D0",
    *,
    domain_id: str = "D0",
    source: str = "D0::L0.C",
    target: str = "D0::L1.C",
) -> CommutationObligation:
    return CommutationObligation(
        obligation_id=obligation_id,
        transition_id="alpha",
        domain_id=domain_id,
        source_carrier_realization_id=source,
        target_carrier_realization_id=target,
        realized_transition_id="D0::alpha",
        witness_of_commutation="تطابقُ الطريقين على كلّ مُدخَلٍ يجتاز البوّابة",
        witness_of_break="مُدخَلٌ يختلف فيه الطريقان",
        break_outcome=TransitionOutcome.BLOCK,
    )


def test_the_square_names_two_distinct_carrier_realizations() -> None:
    obligation = _obligation()
    assert obligation.source_carrier_realization_id != (
        obligation.target_carrier_realization_id
    )
    assert "D0::L1.C ∘ alpha" in obligation.law_statement


def test_one_carrier_realization_written_twice_is_refused() -> None:
    with pytest.raises(CommutationObligationError):
        _obligation(source="D0::L0.C", target="D0::L0.C")


def test_a_break_never_passes_as_a_silent_success() -> None:
    with pytest.raises(CommutationObligationError):
        CommutationObligation(
            obligation_id="sq",
            transition_id="alpha",
            domain_id="D0",
            source_carrier_realization_id="a",
            target_carrier_realization_id="b",
            realized_transition_id="t",
            witness_of_commutation="شاهدُ تبادل",
            witness_of_break="شاهدُ كسر",
            break_outcome=(TransitionOutcome.CONDITIONALLY_LICENSED_RELATIVE_TO_SIGMA),
        )


def test_identical_witnesses_cancel_the_falsifier() -> None:
    with pytest.raises(CommutationObligationError):
        CommutationObligation(
            obligation_id="sq",
            transition_id="alpha",
            domain_id="D0",
            source_carrier_realization_id="a",
            target_carrier_realization_id="b",
            realized_transition_id="t",
            witness_of_commutation="الشاهدُ نفسُه",
            witness_of_break="الشاهدُ نفسُه",
            break_outcome=TransitionOutcome.DEFER,
        )


def test_two_domains_prove_coverage_not_independence() -> None:
    spec = specification()
    obligation = RepresentationIndependenceObligation(
        obligation_id="RI.0",
        specification=spec,
        realizations=(
            realization("R.a", domain_id="D0", spec=spec),
            realization("R.b", domain_id="D1", spec=spec),
        ),
        commutation_obligations=(_obligation(),),
    )
    assert obligation.instantiation_coverage == 2
    assert obligation.discharged_square_count == 0
    assert obligation.outstanding_obligation_ids == ("sq.alpha.D0",)
    assert "استقلالَ التمثيل" in obligation.why_this_is_not_yet_independence


def test_the_counts_are_derived_not_written() -> None:
    field_names = {
        field.name
        for field in RepresentationIndependenceObligation.__dataclass_fields__.values()
    }
    assert "instantiation_coverage" not in field_names
    assert "discharged_square_count" not in field_names


def test_a_realization_of_another_theory_is_not_a_parallel_representation() -> None:
    with pytest.raises(CommutationObligationError):
        RepresentationIndependenceObligation(
            obligation_id="RI.0",
            specification=specification(),
            realizations=(
                realization("R.other", domain_id="D0", spec=specification("OTHER")),
            ),
            commutation_obligations=(),
        )


def test_a_repeated_domain_adds_no_coverage() -> None:
    spec = specification()
    with pytest.raises(CommutationObligationError):
        RepresentationIndependenceObligation(
            obligation_id="RI.0",
            specification=spec,
            realizations=(
                realization("R.a", domain_id="D0", spec=spec),
                realization("R.b", domain_id="D0", spec=spec),
            ),
            commutation_obligations=(),
        )


def test_a_square_for_a_transition_outside_the_theory_is_refused() -> None:
    spec = specification()
    with pytest.raises(CommutationObligationError):
        RepresentationIndependenceObligation(
            obligation_id="RI.0",
            specification=spec,
            realizations=(realization("R.a", domain_id="D0", spec=spec),),
            commutation_obligations=(
                CommutationObligation(
                    obligation_id="sq.omega",
                    transition_id="omega",
                    domain_id="D0",
                    source_carrier_realization_id="a",
                    target_carrier_realization_id="b",
                    realized_transition_id="t",
                    witness_of_commutation="شاهدُ تبادل",
                    witness_of_break="شاهدُ كسر",
                    break_outcome=TransitionOutcome.BLOCK,
                ),
            ),
        )


def test_discharging_an_unregistered_obligation_is_a_claim_without_a_subject() -> None:
    spec = specification()
    with pytest.raises(CommutationObligationError):
        RepresentationIndependenceObligation(
            obligation_id="RI.0",
            specification=spec,
            realizations=(realization("R.a", domain_id="D0", spec=spec),),
            commutation_obligations=(_obligation(),),
            discharged_obligation_ids=("sq.unknown",),
        )
