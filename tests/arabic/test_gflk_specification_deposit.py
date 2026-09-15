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
    GFLK_SPECIFICATION_AMENDMENTS,
    GFLK_SPECIFICATION_CONFLICTS,
    GFLK_SPECIFICATION_DEPOSIT,
    GFLK_SPECIFICATION_NUMERIC_CLAIMS,
    NOT_ISSUED_BY_THIS_TREE,
    SPECIFICATION_RELATIVE_PATH,
    SUBMITTED_FREEZE_IDENTIFIERS,
    ConflictStanding,
    GflkSpecificationConflict,
    GflkSpecificationDeposit,
    GflkSpecificationDepositError,
    ProvenanceGenus,
    SpecificationAmendment,
    SpecificationNumericClaim,
    SubmittedFreezeIdentifier,
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
from alghanem.arabic.word_structure_dictionary import MEASURED_LAYERS, WITHHELD_LAYERS
from alghanem.arabic.word_structure_dictionary_preregistration import DictionaryLayer


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


def test_both_versions_are_deposited_verbatim_in_the_document() -> None:
    """§٢ و§٢-أ تحملان النصّين كما وصلا، فلا يُحرَّر المُودَع صامتًا."""

    text = read_specification_bytes().decode("utf-8")
    assert "## ٢ — النصّ المُودَع حرفيًّا (النسخة الأولى)" in text
    assert "## ٢-أ — النصّ المُودَع حرفيًّا (النسخة الثانية الواردة)" in text
    assert "العنصر السابع عشر المحايد" in text
    assert "FI'L-AMR-SYLLABLE-SIGNATURE-AR-1" in text
    assert "shرط حتمية" in text
    assert GFLK_SPECIFICATION_DEPOSIT.deposited_versions == 2


def test_depositing_the_expanded_version_alone_is_refused() -> None:
    """إيداعُ المُوسَّعة وحدها يمحو أنّ دعوًى أُطلِقت ثمّ قُيِّدت."""

    with pytest.raises(GflkSpecificationDepositError):
        GflkSpecificationDeposit(
            genus=ProvenanceGenus.PROSE_FROM_ANOTHER_CONVERSATION,
            arrival_date="2026-09-15",
            relative_path=SPECIFICATION_RELATIVE_PATH,
            deposited_versions=1,
        )


def test_every_amendment_names_both_versions_and_the_tree_reading() -> None:
    assert GFLK_SPECIFICATION_AMENDMENTS
    for amendment in GFLK_SPECIFICATION_AMENDMENTS:
        assert amendment.first_version_said.strip()
        assert amendment.second_version_says.strip()
        assert amendment.what_this_tree_reads_in_the_change.strip()
    loci = " | ".join(item.locus for item in GFLK_SPECIFICATION_AMENDMENTS)
    assert "فعل الأمر" in loci
    assert "متعدٍّ/لازم" in loci
    with pytest.raises(GflkSpecificationDepositError):
        SpecificationAmendment(
            locus="§٣",
            first_version_said="قول",
            second_version_says="قول آخر",
            what_this_tree_reads_in_the_change="  ",
        )


def test_the_compression_figures_are_recorded_as_unchanged() -> None:
    """رقمٌ تكرّر في نسختين من المصدر نفسِه ليس شاهدين."""

    by_locus = {item.locus: item for item in GFLK_SPECIFICATION_AMENDMENTS}
    entry = by_locus["§٦ — أرقام الضغط"]
    assert "بلا تغيير" in entry.second_version_says
    assert "compression_model_revision_audit" in (
        entry.what_this_tree_reads_in_the_change
    )


def test_every_figure_is_registered_as_not_rederivable_with_its_condition() -> None:
    assert GFLK_SPECIFICATION_NUMERIC_CLAIMS
    for claim in GFLK_SPECIFICATION_NUMERIC_CLAIMS:
        assert claim.not_rederivable_because.strip()
        assert claim.what_would_make_it_rederivable.strip()
    figures = {claim.figure for claim in GFLK_SPECIFICATION_NUMERIC_CLAIMS}
    assert {"4,087", "10,599", "11,467", "37,682", "18,333", "6/6", "4/4"} == figures


def test_a_residue_defined_figure_without_a_dependency_tag_is_refused() -> None:
    """فئةٌ عُرِّفت بعدم المطابقة تتحرّك بحركة القاعدة، فليست شاهدًا مستقلًّا."""

    unconfirmed = next(
        claim for claim in GFLK_SPECIFICATION_NUMERIC_CLAIMS if claim.figure == "11,467"
    )
    assert unconfirmed.is_residue_defined
    assert unconfirmed.depends_on_figure == "4,087"
    with pytest.raises(GflkSpecificationDepositError):
        SpecificationNumericClaim(
            figure="ر",
            locus="§٢-أ",
            claim_text="نصّ",
            not_rederivable_because="سبب",
            what_would_make_it_rederivable="شرط",
            is_residue_defined=True,
        )


def test_the_four_submitted_freezes_are_kept_verbatim_and_disowned() -> None:
    identifiers = {entry.identifier for entry in SUBMITTED_FREEZE_IDENTIFIERS}
    assert identifiers == {
        "JARAD-MAZID-CORRECTED-AR-1",
        "FI'L-AMR-SYLLABLE-SIGNATURE-AR-1",
        "MUDARI-WEAK-RADICAL-IDENTITY-AR-1",
        "LUZUM-TA'ADDI-STRUCTURAL-TOOL-AR-1",
    }
    for entry in SUBMITTED_FREEZE_IDENTIFIERS:
        assert entry.not_issued_by_this_tree == NOT_ISSUED_BY_THIS_TREE
        assert entry.what_it_declares.strip()
    with pytest.raises(GflkSpecificationDepositError):
        SubmittedFreezeIdentifier(
            identifier="X-AR-1",
            what_it_declares="إعلان",
            not_issued_by_this_tree="",
        )


def test_no_submitted_freeze_identifier_exists_in_this_tree() -> None:
    """صفرُ تطابقٍ في `src/` و`docs/` و`tests/` عدا مواضعَ التسجيل نفسِها."""

    root = specification_path().parent.parent.parent
    registration_files = {
        root / "src" / "alghanem" / "arabic" / "gflk_specification_deposit.py",
        root / "docs" / "reference" / "gflk_arabic_letter_specification.md",
        root / "tests" / "arabic" / "test_gflk_specification_deposit.py",
        root / "README.md",
    }
    for entry in SUBMITTED_FREEZE_IDENTIFIERS:
        for folder in ("src", "docs", "tests"):
            for path in (root / folder).rglob("*"):
                if not path.is_file() or path in registration_files:
                    continue
                if path.suffix not in {".py", ".md"}:
                    continue
                assert entry.identifier not in path.read_text(encoding="utf-8")


def test_the_new_conflicts_are_recorded_and_still_unresolved() -> None:
    loci = " | ".join(
        conflict.locus_in_specification for conflict in GFLK_SPECIFICATION_CONFLICTS
    )
    assert "فعل الأمر" in loci
    assert "مبنيٍّ للمجهول" in loci
    assert "مُعرِّفات تجميدٍ واردة" in loci
    assert all(
        conflict.standing
        in {
            ConflictStanding.RECORDED_UNRESOLVED,
            ConflictStanding.BLOCKS_IMPORT_UNTIL_RESOLVED,
        }
        for conflict in GFLK_SPECIFICATION_CONFLICTS
    )


def test_no_register_carries_a_result_or_resolution_field() -> None:
    forbidden = {"result", "verdict", "resolved", "resolution", "proof"}
    for dataclass_type in (
        SpecificationAmendment,
        SpecificationNumericClaim,
        SubmittedFreezeIdentifier,
        GflkSpecificationDeposit,
    ):
        names = {field.name.lower() for field in fields(dataclass_type)}
        assert not (names & forbidden)


def test_the_withheld_layers_are_still_withheld_after_this_deposit() -> None:
    """الإيداعُ لا يرفع حجبًا: طبقةُ مجرد/مزيد وطبقةُ المقطع محجوبتان كما كانتا."""

    withheld = {entry.layer for entry in WITHHELD_LAYERS}
    assert DictionaryLayer.JARAD_ANALYSIS in withheld
    assert DictionaryLayer.SYLLABLES_AND_WAZN in withheld
    assert DictionaryLayer.JARAD_ANALYSIS not in MEASURED_LAYERS
