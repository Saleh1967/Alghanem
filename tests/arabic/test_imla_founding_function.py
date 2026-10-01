"""اختباراتُ دالّة التأسيس: الجمعُ مقيسٌ، والمنعُ بنيويٌّ، والنصفُ الصوتيُّ موقوف."""

from __future__ import annotations

import pytest

from alghanem.arabic.imla_founding_function import (
    IMLA_FOUNDING_NAMED_RESIDUALS,
    THE_IMLA_TABLE,
    THE_PHONETIC_HALF,
    THE_PHONETIC_HALF_COMPLETION_CONDITIONS,
    HalfStanding,
    ImlaClass,
    ImlaFamily,
    ImlaFoundingError,
    Position,
    class_of,
    classify,
    deposit_coverage,
    exclusivity_reading,
    families_of,
    matching_rules,
    possibility_condition,
    seating_classes,
    the_block_and_the_freeze_are_untouched,
)


def test_the_table_is_exclusive_by_construction_not_by_sampling() -> None:
    reading = exclusivity_reading()
    assert reading.is_exclusive
    assert reading.overlapping_codepoints == ()
    assert reading.codepoints_split_by_position == 1


def test_every_position_of_the_sealed_deposit_finds_exactly_one_door() -> None:
    coverage = deposit_coverage()
    assert coverage.is_total
    assert coverage.unclassified == 0
    assert coverage.classified == coverage.positions


def test_the_mandated_topics_each_have_a_declared_door() -> None:
    required = {
        ImlaFamily.ALIF,
        ImlaFamily.HAMZA,
        ImlaFamily.TA,
        ImlaFamily.HA,
        ImlaFamily.TANWIN,
        ImlaFamily.SHADDA,
        ImlaFamily.HARAKA,
        ImlaFamily.SUKUN,
    }
    declared = {family for rule in THE_IMLA_TABLE for family in rule.families}
    assert required <= declared


def test_the_five_hamza_seats_are_each_their_own_door() -> None:
    seats = {class_of(char) for char in "ءأإؤئ"}
    assert seats == {
        ImlaClass.HAMZA_ALONE,
        ImlaClass.HAMZA_ON_ALIF,
        ImlaClass.HAMZA_UNDER_ALIF,
        ImlaClass.HAMZA_ON_WAW,
        ImlaClass.HAMZA_ON_YA,
    }
    assert len(seats) == 5


def test_the_two_taas_are_separated_and_the_marbuta_is_also_a_ha() -> None:
    assert class_of("ت") is ImlaClass.TA_MAFTUHA
    assert class_of("ة", word_final=True) is ImlaClass.TA_MARBUTA
    assert ImlaFamily.HA in families_of(ImlaClass.TA_MARBUTA)


def test_the_ha_is_read_by_its_position_so_waqf_has_its_own_door() -> None:
    assert class_of("ه", word_final=True) is ImlaClass.HA_AT_WORD_END
    assert class_of("ه") is ImlaClass.HA_WITHIN_THE_WORD
    assert classify("لَهُ وَ", 2) is ImlaClass.HA_AT_WORD_END
    assert classify("أَهْلِ", 2) is ImlaClass.HA_WITHIN_THE_WORD


def test_a_family_overlap_is_not_a_class_overlap() -> None:
    families = families_of(ImlaClass.ALIF_MADDA)
    assert {ImlaFamily.ALIF, ImlaFamily.HAMZA} <= families
    assert len(matching_rules("آ", 0)) == 1


def test_an_undeclared_codepoint_is_named_a_residue_and_never_silently_folded() -> None:
    assert classify("۞", 0) is ImlaClass.OUTSIDE_THE_DECLARED_TABLE
    assert families_of(ImlaClass.OUTSIDE_THE_DECLARED_TABLE) == frozenset(
        {ImlaFamily.UNCLASSIFIED}
    )


def test_the_seating_doors_are_read_from_the_fingerprint_fold() -> None:
    seats = set(seating_classes())
    assert ImlaClass.ALIF_MAMDUDA in seats
    assert ImlaClass.HAMZA_ON_WAW in seats
    assert ImlaClass.TA_MARBUTA not in seats
    assert ImlaClass.DAGGER_ALIF not in seats
    assert ImlaClass.SHADDA not in seats


def test_the_phonetic_half_is_suspended_and_names_its_completion_conditions() -> None:
    condition = possibility_condition()
    assert condition.phonetic_half is HalfStanding.SUSPENDED
    assert condition.suspension_reason.strip()
    assert condition.completion_conditions == (THE_PHONETIC_HALF_COMPLETION_CONDITIONS)
    assert len(THE_PHONETIC_HALF) == 2


def test_a_complete_orthographic_half_does_not_meet_the_possibility_condition() -> None:
    condition = possibility_condition()
    assert condition.orthographic_half is HalfStanding.MET
    assert not condition.is_met
    assert condition.unmet_halves == ("النصفُ الصوتيّ: موقوف",)


def test_a_position_outside_the_text_is_refused_not_defaulted() -> None:
    with pytest.raises(ImlaFoundingError):
        classify("ا", 5)
    with pytest.raises(ImlaFoundingError):
        class_of("اب")


def test_the_declared_table_never_declares_the_residue_door() -> None:
    assert all(
        rule.cls is not ImlaClass.OUTSIDE_THE_DECLARED_TABLE for rule in THE_IMLA_TABLE
    )
    assert all(rule.codepoints for rule in THE_IMLA_TABLE)
    assert sum(1 for rule in THE_IMLA_TABLE if rule.position is not Position.ANY) == 2


def test_the_named_residuals_and_the_absence_of_authority_are_present() -> None:
    assert len(IMLA_FOUNDING_NAMED_RESIDUALS) == 5
    assert all(text.strip() for text in IMLA_FOUNDING_NAMED_RESIDUALS)
    assert the_block_and_the_freeze_are_untouched()
