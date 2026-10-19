"""اختباراتُ تسجيل حياد الألف والتاء المربوطة: نطاقان منفصلان ودعوى غيرُ مقيسة."""

from __future__ import annotations

from dataclasses import fields

import pytest

from alghanem.arabic.alif_neutrality_registration import (
    ALIF_FUNCTIONAL_ROLES,
    ALIF_NEUTRALITY_REGISTRATION_NAMED_RESIDUALS,
    ALIF_SCOPE_READINGS,
    FEATURE_AXES,
    TAA_MARBUTA_EXCLUSION,
    AlifNeutralityRegistrationError,
    AlifRoleRecord,
    AlifScopeReading,
    ConventionalExclusion,
    NeutralityScope,
    RoleSeparability,
    separable_roles,
    unseparable_roles,
)
from alghanem.arabic.gflk_feature_table_import_barrier import (
    FEATURE_TABLE_IMPORT_BARRIERS,
    ImportBarrierStanding,
)
from alghanem.arabic.p_extractor import PhoneticRole


def test_the_four_roles_are_named_once_each() -> None:
    names = [role.name for role in ALIF_FUNCTIONAL_ROLES]
    assert len(names) == 4
    assert len(set(names)) == 4


def test_exactly_one_role_is_informationally_non_neutral() -> None:
    non_neutral = [
        role
        for role in ALIF_FUNCTIONAL_ROLES
        if not role.specification_calls_it_informationally_neutral
    ]
    assert [role.name for role in non_neutral] == ["TANWEEN_CARRIER"]


def test_the_wasl_role_is_the_only_unseparable_one() -> None:
    assert [role.name for role in unseparable_roles()] == ["HAMZAT_WASL"]
    assert len(separable_roles()) == 3


def test_every_separable_role_names_a_role_the_reader_can_hang() -> None:
    readable = {role.name for role in PhoneticRole}
    assert "MADD_EXTENSION" in readable
    assert "SILENT_DIFFERENTIATING_ALIF" in readable
    assert "TANWEEN_ALIF_CARRIER" in readable
    for role in separable_roles():
        assert any(name in role.separability_grounds for name in readable)


def test_the_two_scopes_are_registered_separately_and_both_blocked() -> None:
    assert len(ALIF_SCOPE_READINGS) == len(NeutralityScope) == 2
    assert {reading.scope for reading in ALIF_SCOPE_READINGS} == set(NeutralityScope)
    for reading in ALIF_SCOPE_READINGS:
        assert reading.what_blocks_the_test is not None
        assert reading.what_blocks_the_test.strip()


def test_the_registration_lifts_no_import_barrier() -> None:
    assert FEATURE_TABLE_IMPORT_BARRIERS
    assert all(
        barrier.standing is ImportBarrierStanding.OPEN
        for barrier in FEATURE_TABLE_IMPORT_BARRIERS
    )


def test_the_four_axes_are_quoted_not_scored() -> None:
    assert len(FEATURE_AXES) == 4
    role_fields = {field.name for field in fields(AlifRoleRecord)}
    assert not role_fields & set(FEATURE_AXES)
    assert not role_fields & {"jahr", "itbaq", "istila", "asli"}


def test_no_record_carries_a_resolution_field() -> None:
    for record in (AlifRoleRecord, AlifScopeReading, ConventionalExclusion):
        names = {field.name for field in fields(record)}
        assert not names & {"resolution", "resolved", "verdict", "outcome", "decision"}


def test_taa_marbuta_is_excluded_by_convention_and_read_nowhere() -> None:
    assert TAA_MARBUTA_EXCLUSION.letter == "\u0629"
    assert TAA_MARBUTA_EXCLUSION.why_it_is_not_neutrality.strip()
    assert TAA_MARBUTA_EXCLUSION.what_this_tree_does_not_read.strip()


def test_the_named_residuals_are_sorted_and_unique() -> None:
    residuals = ALIF_NEUTRALITY_REGISTRATION_NAMED_RESIDUALS
    assert list(residuals) == sorted(residuals)
    assert len(set(residuals)) == len(residuals)


def test_a_blank_blocking_reason_is_refused_rather_than_read_as_none() -> None:
    with pytest.raises(AlifNeutralityRegistrationError):
        AlifScopeReading(
            scope=NeutralityScope.FEATURAL,
            what_the_specification_says="نصّ",
            what_this_tree_can_test="نصّ",
            what_blocks_the_test="   ",
        )


def test_a_role_refuses_a_free_text_separability() -> None:
    with pytest.raises(AlifNeutralityRegistrationError):
        AlifRoleRecord(
            name="X",
            description="وصف",
            separability="يُفرَز",  # type: ignore[arg-type]
            separability_grounds="مُبرِّر",
            specification_calls_it_informationally_neutral=True,
        )


def test_the_separability_vocabulary_is_closed_at_two() -> None:
    assert len(RoleSeparability) == 2
