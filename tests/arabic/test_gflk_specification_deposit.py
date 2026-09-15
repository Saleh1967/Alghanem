"""اختباراتُ إيداع مواصفة GFLK: البصمةُ من الملفّ، والتعارضاتُ بلا حسم."""

from __future__ import annotations

import hashlib
from dataclasses import fields

import pytest

from alghanem.arabic.gflk_feature_table_import_barrier import (
    ANALYTIC_REGISTRATIONS,
    FEATURE_TABLE_IMPORT_BARRIERS,
    OCP_PREREGISTERED_EXPECTATION,
    AnalyticRegistration,
    FeatureTableImportBarrier,
    FeatureTableImportError,
    ImportBarrierStanding,
    frozen_makhraj_count,
)
from alghanem.arabic.gflk_specification_deposit import (
    GFLK_SPECIFICATION_CONFLICTS,
    GFLK_SPECIFICATION_DEPOSIT,
    ConflictStanding,
    GflkSpecificationConflict,
    GflkSpecificationDepositError,
    ProvenanceGenus,
    read_specification_bytes,
    specification_digest,
    specification_path,
)
from alghanem.arabic.gflk_state_machine_registration import (
    P_EXTRACTOR_ACCEPTANCE_CONDITION,
    PROPOSED_STATE_READINGS,
    UNRESOLVABLE_PROPOSALS,
    ProposedStateReading,
    ProposedStateVerdict,
    StateMachineRegistrationError,
    existing_carrier_state_names,
)


def test_the_deposited_document_exists_in_the_tree() -> None:
    assert specification_path().is_file()
    assert read_specification_bytes()


def test_the_digest_is_rederived_from_the_file_not_stored() -> None:
    """البصمةُ تُشتَقّ من بايتات الملفّ في كلّ نداء، فلا تُصادق على غيره."""

    expected = hashlib.sha256(read_specification_bytes()).hexdigest()
    assert specification_digest() == expected
    assert GFLK_SPECIFICATION_DEPOSIT.digest() == expected


def test_the_deposit_declares_a_foreign_genus() -> None:
    assert (
        GFLK_SPECIFICATION_DEPOSIT.genus
        is ProvenanceGenus.PROSE_FROM_ANOTHER_CONVERSATION
    )
    assert GFLK_SPECIFICATION_DEPOSIT.arrival_date == "2026-09-15"


def test_no_conflict_carries_a_resolution_field() -> None:
    """التعارضُ يحمل شرطَ حسمه ولا يحمل حسمًا؛ ولا عضوَ «محسوم» في المنزلة."""

    names = {field.name for field in fields(GflkSpecificationConflict)}
    assert "resolution" not in names
    assert "resolved" not in names
    assert "verdict" not in names
    assert {member.name for member in ConflictStanding} == {
        "RECORDED_UNRESOLVED",
        "BLOCKS_IMPORT_UNTIL_RESOLVED",
    }


def test_every_conflict_names_its_locus_reference_and_resolution_condition() -> None:
    assert GFLK_SPECIFICATION_CONFLICTS
    for conflict in GFLK_SPECIFICATION_CONFLICTS:
        assert conflict.locus_in_specification.strip()
        assert conflict.tree_reference.strip()
        assert conflict.what_would_resolve_it.strip()


def test_the_three_named_conflicts_are_recorded() -> None:
    loci = " | ".join(
        conflict.locus_in_specification for conflict in GFLK_SPECIFICATION_CONFLICTS
    )
    assert "المخرج" in loci
    assert "الزيادة" in loci
    assert "DEFER" in loci


def test_a_conflict_without_a_resolution_condition_is_refused() -> None:
    with pytest.raises(GflkSpecificationDepositError):
        GflkSpecificationConflict(
            locus_in_specification="§١",
            specification_says="شيء",
            this_tree_says="شيء آخر",
            tree_reference="مرجع",
            what_would_resolve_it="   ",
            standing=ConflictStanding.RECORDED_UNRESOLVED,
        )


def test_the_ambiguous_state_is_kept_out_of_the_state_vocabulary() -> None:
    """حفظًا للبند الأوّل: الغموضُ في حقلٍ منفصلٍ لا عضوًا في المفردة."""

    proposed = {reading.proposed_name for reading in PROPOSED_STATE_READINGS}
    assert "AMBIGUOUS_MADD_OR_TANWEEN_ROOT" not in proposed
    assert "AMBIGUOUS_MADD_OR_TANWEEN_ROOT" not in existing_carrier_state_names()
    assert {item.proposed_name for item in UNRESOLVABLE_PROPOSALS} == {
        "AMBIGUOUS_MADD_OR_TANWEEN_ROOT"
    }


def test_the_existing_state_vocabulary_is_read_not_copied() -> None:
    names = existing_carrier_state_names()
    assert len(names) == 7
    assert "SUKUN_IMPLICIT" in names


def test_role_readings_must_name_the_existing_unit_they_hang_on() -> None:
    for reading in PROPOSED_STATE_READINGS:
        if reading.verdict is ProposedStateVerdict.ROLE_OVER_AN_EXISTING_UNIT:
            assert (reading.existing_unit or "").strip()
    with pytest.raises(StateMachineRegistrationError):
        ProposedStateReading(
            proposed_name="X",
            verdict=ProposedStateVerdict.ROLE_OVER_AN_EXISTING_UNIT,
            grounds="مبرّر",
            existing_unit=None,
        )


def test_tanween_alif_and_madd_are_read_as_roles_not_states() -> None:
    by_name = {reading.proposed_name: reading for reading in PROPOSED_STATE_READINGS}
    for name in ("TANWEEN_ALIF_CARRIER", "MADD_EXTENSION"):
        assert by_name[name].verdict is ProposedStateVerdict.ROLE_OVER_AN_EXISTING_UNIT


def test_the_acceptance_floor_is_stated_with_its_rederivation_path() -> None:
    condition = P_EXTRACTOR_ACCEPTANCE_CONDITION
    assert "٩٩٫٩٩٢٢٥١" in condition.floor_description
    assert "measure_carrier_state_invertibility" in condition.floor_reference
    assert condition.what_counts_as_regression.strip()
    assert condition.explicit_test_cases.strip()


def test_the_makhraj_barrier_is_open_and_reads_the_frozen_count() -> None:
    assert frozen_makhraj_count() == 16
    barrier = FEATURE_TABLE_IMPORT_BARRIERS[0]
    assert barrier.standing is ImportBarrierStanding.OPEN
    assert "ثلاثَ عشرةَ" in barrier.barrier


def test_no_import_barrier_is_lifted_yet() -> None:
    assert all(
        barrier.standing is ImportBarrierStanding.OPEN
        for barrier in FEATURE_TABLE_IMPORT_BARRIERS
    )


def test_a_barrier_without_a_lifting_condition_is_refused() -> None:
    with pytest.raises(FeatureTableImportError):
        FeatureTableImportBarrier(
            table="جدول",
            barrier="مانع",
            what_lifts_it="",
            standing=ImportBarrierStanding.OPEN,
        )


def test_the_inclusion_relation_is_registered_as_analytic_with_its_definition() -> None:
    registration = ANALYTIC_REGISTRATIONS[0]
    assert registration.proposition == "إطباق ⊆ استعلاء"
    assert registration.definition_text.strip()
    assert registration.what_would_make_it_empirical.strip()
    with pytest.raises(FeatureTableImportError):
        AnalyticRegistration(
            proposition="ص",
            definition_text=" ",
            what_follows_from_the_definition="ش",
            what_would_make_it_empirical="ش",
        )


def test_the_ocp_expectation_is_defer_and_written_with_its_prior_grounds() -> None:
    expectation = OCP_PREREGISTERED_EXPECTATION
    assert expectation.expected_outcome == "DEFER لا PASS"
    assert "phonetic_economy_candidate" in expectation.grounds_known_before_measuring
    assert expectation.what_would_overturn_the_expectation.strip()
