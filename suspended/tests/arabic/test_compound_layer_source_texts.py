"""اختبارات النصوص المُزوَّدة لمراحل طبقة المركّب وأثرها المحدود على تسجيلها."""

from __future__ import annotations

from dataclasses import replace

import pytest

from alghanem.arabic.compound_layer_preregistration import (
    COMPOUND_LAYER_PREREGISTRATION,
    AttestationStanding,
    CompoundLayerPreregistrationError,
    CompoundStage,
)
from alghanem.arabic.compound_layer_source_texts import (
    AMIL_MAMUL_IBN_AQIL_ISHTIGHAL,
    AMIL_MAMUL_MUGHNI_FASL,
    COMPOUND_SUPPLIED_SOURCE_TEXTS,
    CompoundSourceReference,
    CompoundSuppliedSourceText,
    compound_texts_for_stage,
    require_attested_compound_excerpt,
    supplied_compound_text_for,
)
from alghanem.arabic.sentence_card_source_texts import (
    LocusVerification,
    SourceTextError,
)


def test_both_texts_are_registered_for_the_first_stage_only() -> None:
    assert compound_texts_for_stage(CompoundStage.AMIL_MAMUL) == (
        AMIL_MAMUL_IBN_AQIL_ISHTIGHAL,
        AMIL_MAMUL_MUGHNI_FASL,
    )
    for stage in CompoundStage:
        if stage is not CompoundStage.AMIL_MAMUL:
            assert compound_texts_for_stage(stage) == ()


def test_the_two_texts_come_from_two_distinct_references() -> None:
    references = {
        supplied.reference for supplied in COMPOUND_SUPPLIED_SOURCE_TEXTS.values()
    }
    assert references == set(CompoundSourceReference)


def test_locus_is_the_middle_rank_not_the_collated_one() -> None:
    for supplied in COMPOUND_SUPPLIED_SOURCE_TEXTS.values():
        assert (
            supplied.locus_verification
            is LocusVerification.ترقيم_طبعة_مرمز_رقميا_غير_مقابل
        )
        assert supplied.locus_is_collated_by_hand is False


def test_no_supplied_text_claims_a_witness_for_every_branch() -> None:
    for supplied in COMPOUND_SUPPLIED_SOURCE_TEXTS.values():
        assert supplied.attests_every_branch is False


def test_every_text_records_that_its_term_is_used_not_defined() -> None:
    for supplied in COMPOUND_SUPPLIED_SOURCE_TEXTS.values():
        assert (
            "TERM_IS_USED_NOT_DEFINED_IN_THE_SUPPLIED_TEXT" in supplied.named_residuals
        )


def test_every_text_records_the_reversed_vocabulary_order() -> None:
    for supplied in COMPOUND_SUPPLIED_SOURCE_TEXTS.values():
        assert (
            "REFERENCE_VOCABULARY_OPENED_AFTER_ITS_TEXT_WAS_SEEN"
            in supplied.named_residuals
        )


def test_a_text_without_that_residual_is_refused() -> None:
    with pytest.raises(SourceTextError, match="فتحِ المفردة"):
        replace(
            AMIL_MAMUL_MUGHNI_FASL,
            named_residuals=("DIGITALLY_ENCODED_PRINT_PAGINATION_UNCOLLATED",),
        )


def test_a_text_without_any_residual_is_refused() -> None:
    with pytest.raises(SourceTextError, match="بلا بقيّةٍ"):
        replace(AMIL_MAMUL_MUGHNI_FASL, named_residuals=())


def test_an_authority_absent_from_the_text_is_refused() -> None:
    with pytest.raises(SourceTextError, match="غيرُ واقعةٍ في النصّ"):
        replace(AMIL_MAMUL_MUGHNI_FASL, internal_authorities=("سيبويه",))


def test_the_digital_witnesses_name_two_different_editorial_teams() -> None:
    ibn_aqil = AMIL_MAMUL_IBN_AQIL_ISHTIGHAL.digital_witness
    mughni = AMIL_MAMUL_MUGHNI_FASL.digital_witness
    assert ibn_aqil is not None and mughni is not None
    assert "محمد محيي الدين عبد الحميد" in ibn_aqil.print_edition
    assert "محمد محيي الدين عبد الحميد" not in mughni.print_edition
    assert "مازن المبارك" in mughni.print_edition


def test_excerpt_must_fall_inside_the_supplied_text() -> None:
    assert require_attested_compound_excerpt(
        "AMIL_MAMUL_MUGHNI_FASL", "بين العامل والمعمول"
    )
    with pytest.raises(SourceTextError, match="لا يقع حرفُه"):
        require_attested_compound_excerpt(
            "AMIL_MAMUL_MUGHNI_FASL", "العامل ما أوجب كون آخر الكلمة"
        )


def test_an_unregistered_key_is_refused() -> None:
    with pytest.raises(SourceTextError, match="لا نصَّ مُزوَّدًا"):
        supplied_compound_text_for("AMIL_MAMUL_NAHW_WADIH")


def test_no_supplied_text_carries_a_result_field() -> None:
    forbidden = ("result", "outcome", "verdict", "birth", "certificate")
    for name in CompoundSuppliedSourceText.__dataclass_fields__:
        assert not any(token in name.lower() for token in forbidden)


def test_the_first_stage_alone_moved_to_the_middle_standing() -> None:
    for registration in COMPOUND_LAYER_PREREGISTRATION.registrations:
        if registration.stage is CompoundStage.AMIL_MAMUL:
            assert (
                registration.attestation
                is AttestationStanding.SOURCE_SUPPLIED_NOT_VERIFIED
            )
            assert registration.supplied_text_keys == (
                "AMIL_MAMUL_IBN_AQIL_ISHTIGHAL",
                "AMIL_MAMUL_MUGHNI_FASL",
            )
        else:
            assert registration.attestation is AttestationStanding.SOURCE_NOT_SUPPLIED
            assert registration.supplied_text_keys == ()


def test_the_refusal_statement_changes_genus_with_the_standing() -> None:
    supplied_stage = COMPOUND_LAYER_PREREGISTRATION.registration_for(
        CompoundStage.AMIL_MAMUL
    )
    bare_stage = COMPOUND_LAYER_PREREGISTRATION.registration_for(
        CompoundStage.NISBA_ROLE
    )
    assert "لا سلطة" in supplied_stage.standing_refusal_statement
    assert "لم يُقدَّم" in bare_stage.standing_refusal_statement
    assert supplied_stage.standing_refusal_statement != (
        bare_stage.standing_refusal_statement
    )


def test_declaring_supply_without_keys_is_refused() -> None:
    registration = COMPOUND_LAYER_PREREGISTRATION.registration_for(
        CompoundStage.AMIL_MAMUL
    )
    with pytest.raises(CompoundLayerPreregistrationError, match="بلا مُزوَّد"):
        replace(registration, supplied_text_keys=())


def test_declaring_keys_without_supply_is_refused() -> None:
    registration = COMPOUND_LAYER_PREREGISTRATION.registration_for(
        CompoundStage.NISBA_ROLE
    )
    with pytest.raises(CompoundLayerPreregistrationError, match="متناقضان"):
        replace(registration, supplied_text_keys=("AMIL_MAMUL_MUGHNI_FASL",))


def test_supplying_a_text_does_not_make_a_certificate_constructible() -> None:
    assert COMPOUND_LAYER_PREREGISTRATION.certificate_is_constructible is False


def test_the_first_stage_vocabulary_was_not_widened_after_its_text() -> None:
    registration = COMPOUND_LAYER_PREREGISTRATION.registration_for(
        CompoundStage.AMIL_MAMUL
    )
    assert registration.declared_outcomes == ("عامل", "معمول", "لا_ينطبق")
    assert {refusal.name for refusal in registration.refusals} >= {
        "GovernanceRelationIsNotBornOntology",
        "SurfaceEffectIsNotSemanticRole",
    }


def test_attested_per_branch_is_still_unconstructible_after_supply() -> None:
    registration = COMPOUND_LAYER_PREREGISTRATION.registration_for(
        CompoundStage.AMIL_MAMUL
    )
    with pytest.raises(CompoundLayerPreregistrationError, match="لا سلطة"):
        replace(registration, attestation=AttestationStanding.ATTESTED_PER_BRANCH)
