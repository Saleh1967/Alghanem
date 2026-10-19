import dataclasses

import pytest
from builders import transition

from alghanem.metaalgebra.transition import (
    CLOSURE_IS_NOT_A_RIGHT_OF_EXIT,
    NO_JUMP_CONSTRAINS_THE_PATH_NOT_THE_TARGET_MEMBERSHIP,
    NO_JUMP_LAW,
    REQUIRED_AUDIT_CERTIFICATE_FACTS,
    TRANSITION_COMPONENT_NAMES,
    HandoffCondition,
    LicenseGateSpecification,
    PreservationObligation,
    ResidualRankPolicy,
    TransitionOutcome,
    TransitionSignature,
    TransitionSignatureError,
    TransitionTraceObligation,
)


def test_transition_signature_has_six_components_plus_a_separate_handoff() -> None:
    assert TRANSITION_COMPONENT_NAMES == (
        "domain",
        "gate",
        "transformation",
        "preservation",
        "trace",
        "residual_policy",
    )
    assert "handoff" in TransitionSignature.__dataclass_fields__
    assert "handoff" not in TRANSITION_COMPONENT_NAMES


def test_no_outcome_is_named_proved() -> None:
    assert "PROVED" not in {member.value for member in TransitionOutcome}


def test_unlicensed_outcomes_are_block_or_defer_only() -> None:
    with pytest.raises(TransitionSignatureError) as excinfo:
        LicenseGateSpecification(
            gate_id="G",
            licensed_when="شرط",
            unlicensed_outcomes=(
                TransitionOutcome.CONDITIONALLY_LICENSED_RELATIVE_TO_SIGMA,
            ),
            unlicensed_reason="سبب",
        )

    assert NO_JUMP_LAW in str(excinfo.value)


def test_a_gate_without_a_refusal_outcome_is_refused() -> None:
    with pytest.raises(TransitionSignatureError):
        LicenseGateSpecification(
            gate_id="G",
            licensed_when="شرط",
            unlicensed_outcomes=(),
            unlicensed_reason="سبب",
        )


def test_no_jump_law_speaks_of_the_path_not_of_target_membership() -> None:
    assert "BLOCK/DEFER" in NO_JUMP_LAW
    assert "∉" not in NO_JUMP_LAW
    assert NO_JUMP_CONSTRAINS_THE_PATH_NOT_THE_TARGET_MEMBERSHIP.strip() != ""


def test_handoff_must_add_something_beyond_closure() -> None:
    shared = "عند تأهّل المغلَق"
    with pytest.raises(TransitionSignatureError) as excinfo:
        HandoffCondition(
            condition_id="handoff",
            holds_when=shared,
            beyond_closure=shared,
            failure_outcome=TransitionOutcome.DEFER,
        )

    assert CLOSURE_IS_NOT_A_RIGHT_OF_EXIT in str(excinfo.value)


def test_handoff_failure_cannot_be_a_successful_outcome() -> None:
    with pytest.raises(TransitionSignatureError):
        HandoffCondition(
            condition_id="handoff",
            holds_when="شرطُ التأهّل",
            beyond_closure="زيادةٌ على الإغلاق",
            failure_outcome=(
                TransitionOutcome.CONDITIONALLY_LICENSED_RELATIVE_TO_SIGMA
            ),
        )


def test_audit_certificate_requires_all_five_facts() -> None:
    assert len(REQUIRED_AUDIT_CERTIFICATE_FACTS) == 5
    for omitted in REQUIRED_AUDIT_CERTIFICATE_FACTS:
        remaining = tuple(
            fact for fact in REQUIRED_AUDIT_CERTIFICATE_FACTS if fact != omitted
        )
        with pytest.raises(TransitionSignatureError):
            TransitionTraceObligation(
                obligation_id="tau",
                certificate_facts=remaining,
                minimality_condition="شرط",
            )


def test_audit_certificate_does_not_demand_the_original_input() -> None:
    assert "source_object" not in REQUIRED_AUDIT_CERTIFICATE_FACTS
    assert "inverse" not in REQUIRED_AUDIT_CERTIFICATE_FACTS


def test_a_component_cannot_be_preserved_and_changed_at_once() -> None:
    with pytest.raises(TransitionSignatureError):
        PreservationObligation(
            preserved_components=("identity",),
            changed_components=("identity",),
            preservation_condition="شرط",
        )


def test_a_rank_violation_cannot_pass_as_success() -> None:
    with pytest.raises(TransitionSignatureError):
        ResidualRankPolicy(
            policy_id="rho",
            residual_condition="شرط",
            rank_relation="علاقة",
            violation_outcome=(
                TransitionOutcome.CONDITIONALLY_LICENSED_RELATIVE_TO_SIGMA
            ),
        )


def test_a_transition_from_a_layer_to_itself_is_refused() -> None:
    signature = transition()
    with pytest.raises(TransitionSignatureError):
        dataclasses.replace(signature, target_layer_id=signature.source_layer_id)


def test_transition_signature_carries_no_judgement_field() -> None:
    fields = set(TransitionSignature.__dataclass_fields__)
    assert not fields & {"outcome", "verdict", "decision", "status", "result"}


def test_transition_content_id_is_stable_and_content_sensitive() -> None:
    first = transition()
    assert first.content_id == transition().content_id
    assert first.content_id != transition(transition_id="beta").content_id
