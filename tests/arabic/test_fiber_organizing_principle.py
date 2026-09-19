"""شهودٌ على الترشيح: أربعُ قراءاتٍ للشاهد، وأربعةُ التزاماتٍ لا واحدٌ مُبرَأ."""

from __future__ import annotations

from pathlib import Path

import pytest

from alghanem.arabic import fiber_organizing_principle as principle_module
from alghanem.arabic.alif_neutrality import AlifClaimReading, AlifVerdict
from alghanem.arabic.carrier_state_observed_fiber import (
    run_observed_fiber_on_the_deposited_fatiha,
)
from alghanem.arabic.fiber_organizing_principle import (
    ORGANIZING_PRINCIPLE_NAMED_RESIDUALS,
    THE_CANDIDATE_RECORD,
    THE_HYPOTHESIS,
    THE_OBLIGATIONS,
    DischargeStanding,
    HypothesisStanding,
    IdentityParticipation,
    ObligationRecord,
    OrganizingPrincipleCandidate,
    OrganizingPrincipleError,
    ProofObligation,
    measure_identity_participation,
    read_the_alif_witness,
)
from alghanem.import_boundary import ImportBoundaryPolicy, audit_import_boundary

# --- الحدودُ البنيويّة ------------------------------------------------------------


def test_the_principle_module_reaches_no_kernel_module() -> None:
    report = audit_import_boundary(
        (Path(str(principle_module.__file__)),),
        ImportBoundaryPolicy(
            policy_id="fiber-organizing-principle",
            permitted_modules=(),
            forbidden_packages=("alghanem.kernel",),
        ),
    )
    assert not [
        name for name in report.reached_modules if name.startswith("alghanem.kernel")
    ]


def test_there_are_five_named_residuals_all_distinct_and_non_blank() -> None:
    assert len(ORGANIZING_PRINCIPLE_NAMED_RESIDUALS) == 5
    assert len(set(ORGANIZING_PRINCIPLE_NAMED_RESIDUALS)) == 5
    assert all(note.strip() for note in ORGANIZING_PRINCIPLE_NAMED_RESIDUALS)


def test_no_birth_or_refinement_operation_is_exported_here() -> None:
    exported = [
        name
        for name in principle_module.__all__
        if callable(getattr(principle_module, name))
        and any(
            marker in name.lower() for marker in ("refine", "split", "birth", "born")
        )
    ]
    assert exported == []
    assert not hasattr(principle_module, "RefineSlot")


# --- الترشيحُ لا يُرفَع -------------------------------------------------------


def test_the_hypothesis_is_deposited_as_a_candidate_and_is_not_born() -> None:
    assert THE_CANDIDATE_RECORD.hypothesis == THE_HYPOTHESIS
    assert THE_CANDIDATE_RECORD.standing is HypothesisStanding.A_CANDIDATE
    assert THE_CANDIDATE_RECORD.is_born is False


def test_candidacy_is_the_only_standing_the_vocabulary_offers() -> None:
    assert len(HypothesisStanding) == 1


def test_a_hypothesis_may_not_be_deposited_above_candidacy() -> None:
    class _Forged:
        pass

    with pytest.raises(OrganizingPrincipleError):
        OrganizingPrincipleCandidate(
            hypothesis=THE_HYPOTHESIS,
            standing=_Forged(),  # type: ignore[arg-type]
            obligations=THE_OBLIGATIONS,
        )


def test_a_measurement_is_recorded_as_not_being_a_birth_certificate() -> None:
    joined = "\n".join(ORGANIZING_PRINCIPLE_NAMED_RESIDUALS)
    assert "AMeasurementIsNotABirthCertificate" in joined


# --- الالتزاماتُ الأربعة -----------------------------------------------------


def test_the_four_obligations_are_all_recorded_and_none_is_discharged() -> None:
    assert len(THE_OBLIGATIONS) == len(ProofObligation) == 4
    assert all(item.is_discharged is False for item in THE_OBLIGATIONS)
    assert len(THE_CANDIDATE_RECORD.undischarged_obligations) == 4


def test_the_four_obligations_are_distinct_and_cover_the_vocabulary() -> None:
    assert {item.obligation for item in THE_OBLIGATIONS} == set(ProofObligation)


def test_dropping_an_obligation_is_refused_as_a_silent_discharge() -> None:
    with pytest.raises(OrganizingPrincipleError):
        OrganizingPrincipleCandidate(
            hypothesis=THE_HYPOTHESIS,
            standing=HypothesisStanding.A_CANDIDATE,
            obligations=THE_OBLIGATIONS[:3],
        )


def test_repeating_an_obligation_is_refused_because_it_hides_a_missing_one() -> None:
    with pytest.raises(OrganizingPrincipleError):
        OrganizingPrincipleCandidate(
            hypothesis=THE_HYPOTHESIS,
            standing=HypothesisStanding.A_CANDIDATE,
            obligations=THE_OBLIGATIONS[:3] + (THE_OBLIGATIONS[0],),
        )


def test_every_obligation_carries_a_discharge_condition_and_a_reason() -> None:
    for item in THE_OBLIGATIONS:
        assert item.what_would_discharge_it.strip()
        assert item.why_it_stands_there.strip()


def test_an_obligation_without_a_discharge_condition_is_refused() -> None:
    with pytest.raises(OrganizingPrincipleError):
        ObligationRecord(
            obligation=ProofObligation.CV_BIRTH,
            standing=DischargeStanding.NOT_ATTEMPTED,
            what_would_discharge_it="   ",
            why_it_stands_there="سببٌ مكتوب",
        )


def test_an_obligation_without_a_written_reason_is_refused() -> None:
    with pytest.raises(OrganizingPrincipleError):
        ObligationRecord(
            obligation=ProofObligation.CV_BIRTH,
            standing=DischargeStanding.NOT_ATTEMPTED,
            what_would_discharge_it="شرطٌ مكتوب",
            why_it_stands_there="",
        )


def test_the_four_obligations_do_not_all_stand_in_the_same_way() -> None:
    standings = {item.standing for item in THE_OBLIGATIONS}
    assert len(standings) == 4


def test_cv_birth_is_barred_by_a_standing_guard_not_merely_deferred() -> None:
    (record,) = (
        item for item in THE_OBLIGATIONS if item.obligation is ProofObligation.CV_BIRTH
    )
    assert record.standing is DischargeStanding.BARRED_BY_A_STANDING_GUARD
    joined = "\n".join(ORGANIZING_PRINCIPLE_NAMED_RESIDUALS)
    assert "OneObligationIsBarredNotMerelyDeferred" in joined


def test_refine_slot_necessity_stands_refuted_as_stated() -> None:
    (record,) = (
        item
        for item in THE_OBLIGATIONS
        if item.obligation is ProofObligation.REFINE_SLOT_NECESSITY
    )
    assert record.standing is DischargeStanding.REFUTED_AS_STATED


def test_end_to_end_utility_was_not_even_attempted() -> None:
    (record,) = (
        item
        for item in THE_OBLIGATIONS
        if item.obligation is ProofObligation.END_TO_END_UTILITY
    )
    assert record.standing is DischargeStanding.NOT_ATTEMPTED


# --- شاهدُ الألف --------------------------------------------------------------


def test_the_alif_witness_is_read_live_as_four_separate_readings() -> None:
    readings = read_the_alif_witness()
    assert len(readings) == 4
    assert dict(readings) == {
        AlifClaimReading.ALIF_ACCEPTS_ONE_COMBINATION: AlifVerdict.HELD_BY_MEASUREMENT,
        AlifClaimReading.THAT_COMBINATION_IS_THE_IDENTITY: (
            AlifVerdict.HELD_BY_MEASUREMENT
        ),
        AlifClaimReading.ALIF_IS_NOT_AN_ELEMENT_OF_C: AlifVerdict.ADMISSIBLE_BUT_CHOSEN,
        AlifClaimReading.REMOVING_ALIF_RESTORES_THE_PRODUCT: AlifVerdict.REFUTED,
    }


def test_the_witness_contains_a_refuted_reading_so_it_is_not_cited_whole() -> None:
    verdicts = [verdict for _, verdict in read_the_alif_witness()]
    assert AlifVerdict.REFUTED in verdicts
    assert AlifVerdict.ADMISSIBLE_BUT_CHOSEN in verdicts
    joined = "\n".join(ORGANIZING_PRINCIPLE_NAMED_RESIDUALS)
    assert "TheAlifWitnessIsFourReadingsNotOne" in joined


def test_the_witness_carries_the_standing_madd_blocker_with_it() -> None:
    joined = "\n".join(ORGANIZING_PRINCIPLE_NAMED_RESIDUALS)
    assert "TheWitnessCarriesItsOwnBlocker" in joined


# --- العموم: مشاركةُ المحايد --------------------------------------------------


def test_the_identity_state_is_shared_by_exactly_four_carriers() -> None:
    participation = measure_identity_participation()
    assert participation.carrier_count == 23
    assert participation.carriers_containing_identity == ("ا", "ل", "و", "ي")


def test_only_the_alif_has_the_identity_as_its_whole_fiber() -> None:
    participation = measure_identity_participation()
    assert participation.carriers_whose_fiber_is_only_identity == ("ا",)
    assert participation.the_alif_property_is_unique is True


def test_the_participation_is_neither_singular_nor_general() -> None:
    participation = measure_identity_participation()
    assert participation.participation_is_neither_singular_nor_general is True
    joined = "\n".join(ORGANIZING_PRINCIPLE_NAMED_RESIDUALS)
    assert "FourCarriersIsNeitherOneNorGeneral" in joined


def test_the_identity_state_is_absent_on_every_named_axis() -> None:
    participation = measure_identity_participation()
    assert all(value == "ABSENT" for _, value in participation.identity_state)
    assert len(participation.identity_state) == 4


def test_a_participation_whose_counts_contradict_each_other_is_refused() -> None:
    with pytest.raises(OrganizingPrincipleError):
        IdentityParticipation(
            identity_state=(("vowel", "ABSENT"),),
            carrier_count=23,
            carriers_containing_identity=("ل", "و", "ي"),
            carriers_whose_fiber_is_only_identity=("ا",),
        )


def test_a_participation_exceeding_the_carrier_count_is_refused() -> None:
    with pytest.raises(OrganizingPrincipleError):
        IdentityParticipation(
            identity_state=(("vowel", "ABSENT"),),
            carrier_count=2,
            carriers_containing_identity=("ا", "ل", "و"),
            carriers_whose_fiber_is_only_identity=(),
        )


def test_the_numbers_are_derived_from_the_deposited_table_not_written_beside_it() -> (
    None
):
    table = run_observed_fiber_on_the_deposited_fatiha()
    participation = measure_identity_participation(table)
    assert len(participation.carriers_containing_identity) == 4
    assert participation.carrier_count == 23
