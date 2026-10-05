"""سلطةُ التشغيل التجريبيّة: إذنٌ مربوطٌ بتشغيلٍ بعينه، ينتهي بانتهائه.

    ISSUED → ACTIVE → REVOKED

ولا ترخيصَ فيها ولا شهادةَ كفاية.

تسجيلٌ لا سلطة: لا ترخيصَ، ولا رتبةَ دائمة، ولا حكمَ كفاية.
"""

from __future__ import annotations

import pytest
from experiment_cases import (
    BINDING,
    FROZEN_ENTRY,
    LOWER_REF,
    OPERATION,
    PATTERN_REF,
    UPPER_REF,
    build_run,
    issue_permit,
)

from alghanem.fractal_experiment import (
    ExperimentalAuthorityError,
    ExperimentalFractalAuthority,
    ExperimentalPermitState,
    ExperimentalRunPermit,
    FrozenExperimentBindingError,
)


def test_a_permit_is_issued_by_its_authority_not_written_by_a_caller() -> None:
    authority = ExperimentalFractalAuthority(authority_id="authority.synthetic")
    permit = issue_permit(authority, run_id="run.a")
    assert authority.state_of(permit) is ExperimentalPermitState.ISSUED
    with pytest.raises(ExperimentalAuthorityError):
        ExperimentalRunPermit(
            authority_id="authority.synthetic",
            experiment_id="experiment.synthetic",
            run_id="run.forged",
            frozen_specification_ref=BINDING.frozen_specification_ref,
            frozen_input_set_ref=BINDING.frozen_input_set_ref,
            binding_content_id=BINDING.content_id,
            permitted_patterns=(PATTERN_REF,),
            permitted_operations=(OPERATION,),
            permitted_source_scales=(LOWER_REF,),
            permitted_target_scales=(UPPER_REF,),
            permitted_branch_birth=False,
            permitted_experimental_lift=True,
            authority_scope="إذنٌ مكتوبٌ بلا بوّابة",
            issuance=object(),  # type: ignore[arg-type]
        )


def test_a_permit_does_not_serve_another_run() -> None:
    authority = ExperimentalFractalAuthority(authority_id="authority.synthetic")
    permit = authority.activate(issue_permit(authority, run_id="run.a"))
    assert authority.is_active_for_run(permit, run_id="run.a")
    assert not authority.is_active_for_run(permit, run_id="run.b")
    with pytest.raises(ExperimentalAuthorityError):
        authority.require_active_for_run(permit, run_id="run.b")


def test_a_permit_of_another_authority_is_refused() -> None:
    first = ExperimentalFractalAuthority(authority_id="authority.first")
    second = ExperimentalFractalAuthority(authority_id="authority.second")
    permit = first.activate(issue_permit(first, run_id="run.a"))
    with pytest.raises(ExperimentalAuthorityError):
        second.require_active_for_run(permit, run_id="run.a")


def test_a_revoked_permit_does_not_work_again() -> None:
    authority = ExperimentalFractalAuthority(authority_id="authority.synthetic")
    permit = authority.activate(issue_permit(authority, run_id="run.a"))
    revoked = authority.revoke(permit)
    assert authority.state_of(revoked) is ExperimentalPermitState.REVOKED
    with pytest.raises(ExperimentalAuthorityError):
        authority.require_active_for_run(revoked, run_id="run.a")
    with pytest.raises(ExperimentalAuthorityError):
        authority.activate(revoked)


def test_the_authority_expires_with_its_run() -> None:
    run = build_run("run.expiry")
    assert run.final_state is ExperimentalPermitState.REVOKED
    with pytest.raises(ExperimentalAuthorityError):
        run.authority.require_active_for_run(run.permit, run_id="run.expiry")


def test_the_experimental_authority_has_no_licensing_member() -> None:
    authority = ExperimentalFractalAuthority(authority_id="authority.synthetic")
    permit = issue_permit(authority, run_id="run.a")
    for name in dir(authority) + dir(permit):
        lowered = name.lower()
        assert "license" not in lowered
        assert "licence" not in lowered
        assert "certify" not in lowered
        assert "certificate" not in lowered
        assert "sufficiency" not in lowered


def test_a_permit_names_the_frozen_binding_it_was_issued_upon() -> None:
    authority = ExperimentalFractalAuthority(authority_id="authority.synthetic")
    permit = issue_permit(authority, run_id="run.a")
    assert permit.binding_content_id == BINDING.content_id
    assert permit.frozen_input_set_ref == BINDING.frozen_input_set_ref
    assert permit.belongs_to_run("run.a")
    assert not permit.belongs_to_run("run.b")


def test_the_frozen_binding_refuses_a_held_out_field_in_the_generator_input() -> None:
    BINDING.refuse_held_out_fields({"mark": "m0"})
    with pytest.raises(FrozenExperimentBindingError):
        BINDING.refuse_held_out_fields({"mark": "m0", "expected_mark": "m1"})
    with pytest.raises(FrozenExperimentBindingError):
        BINDING.refuse_held_out_fields({"mark": "m0", "undeclared": "x"})


def test_the_frozen_entry_is_the_one_named_in_the_binding() -> None:
    assert BINDING.entry_for(FROZEN_ENTRY.input_id) == FROZEN_ENTRY
    with pytest.raises(FrozenExperimentBindingError):
        BINDING.entry_for("input.absent")
