"""اختباراتُ التسجيل القبْليّ للقاموس الموحَّد: المنازلُ مفصولةٌ والتعذّرُ مُسمًّى."""

from __future__ import annotations

import pytest

from alghanem.arabic.encoding.carrier_state_candidate import CarrierState
from alghanem.arabic.word_structure_dictionary_preregistration import (
    DICTIONARY_LAYER_REGISTRATIONS,
    GLOSSARY_CATEGORIES_NOT_YET_SUPPLIED,
    GLOSSARY_CONCORDANCE,
    ROLE_READINGS_OVER_THE_EXISTING_UNIT,
    ConcordanceReading,
    DictionaryLayer,
    GlossaryConcordanceRow,
    LayerEpistemicStanding,
    LayerRegistration,
    RoleReading,
    UnsuppliedGlossaryCategory,
    WordStructureDictionaryPreregistrationError,
    existing_carrier_state_names,
    layer_registration,
)


def test_every_layer_is_registered_exactly_once() -> None:
    registered = tuple(
        registration.layer for registration in DICTIONARY_LAYER_REGISTRATIONS
    )
    assert set(registered) == set(DictionaryLayer)
    assert len(registered) == len(set(registered)) == 7


def test_the_seven_layers_do_not_share_one_standing() -> None:
    """التجميعُ لا يُسوّي المنازل: الأربعُ كلُّها مستعمَلةٌ فعلًا."""

    standings = {
        registration.standing for registration in DICTIONARY_LAYER_REGISTRATIONS
    }
    assert standings == set(LayerEpistemicStanding)


def test_the_two_blocked_layers_are_not_measured() -> None:
    assert (
        layer_registration(DictionaryLayer.PHONETIC_FEATURES).standing
        is LayerEpistemicStanding.IMPORTED_BEHIND_AN_OPEN_BARRIER
    )
    assert (
        layer_registration(DictionaryLayer.AL_ANALYSIS).standing
        is LayerEpistemicStanding.UNDECIDABLE_FROM_THE_WRITTEN_MARKS
    )
    assert (
        layer_registration(DictionaryLayer.JARAD_ANALYSIS).standing
        is LayerEpistemicStanding.HYPOTHESIS_WITH_A_DECLARED_DEFECT
    )


def test_every_layer_names_a_refusal_field_instead_of_a_null() -> None:
    for registration in DICTIONARY_LAYER_REGISTRATIONS:
        assert registration.refusal_field_name.strip()
        assert registration.what_the_refusal_field_says.strip()


def test_a_null_named_refusal_field_is_refused_at_construction() -> None:
    for forbidden in ("None", "null", "   "):
        with pytest.raises(WordStructureDictionaryPreregistrationError):
            LayerRegistration(
                layer=DictionaryLayer.SYLLABLES_AND_WAZN,
                standing=LayerEpistemicStanding.HYPOTHESIS_WITH_A_DECLARED_DEFECT,
                source_in_this_tree="مصدرٌ",
                entry_condition="شرطٌ",
                refusal_field_name=forbidden,
                what_the_refusal_field_says="قولٌ",
            )


def test_a_layer_without_an_entry_condition_is_refused() -> None:
    with pytest.raises(WordStructureDictionaryPreregistrationError):
        LayerRegistration(
            layer=DictionaryLayer.LETTERS,
            standing=LayerEpistemicStanding.MEASURED_BY_AN_EXISTING_CODEC,
            source_in_this_tree="مصدرٌ",
            entry_condition="  ",
            refusal_field_name="letters_unread",
            what_the_refusal_field_says="قولٌ",
        )


def test_the_sukun_collision_is_settled_as_one_concept() -> None:
    rows = {row.glossary_category: row for row in GLOSSARY_CONCORDANCE}
    assert rows["SUKUN"].reading is ConcordanceReading.SAME_CONCEPT_ONE_ENTRY
    assert (
        rows["IMPLICIT_SUKUN"].reading
        is ConcordanceReading.CONFLATES_TWO_EPISTEMIC_RANKS
    )
    names = existing_carrier_state_names()
    assert "SUKUN_EXPLICIT" in names
    assert "SUKUN_IMPLICIT" in names


def test_the_wasl_row_keeps_the_positional_inference_separate() -> None:
    rows = {row.glossary_category: row for row in GLOSSARY_CONCORDANCE}
    assert rows["ALIF_WASL"].reading is ConcordanceReading.CONFLATES_TWO_EPISTEMIC_RANKS
    assert "ibtida_wasl_waqf_registration" in rows["ALIF_WASL"].tree_reference


def test_the_two_proposed_states_are_read_as_roles_not_members() -> None:
    rows = {row.glossary_category: row for row in GLOSSARY_CONCORDANCE}
    for name in ("TANWEEN_ALIF_CARRIER", "SHADDA_*"):
        assert rows[name].reading is ConcordanceReading.ROLE_OVER_AN_EXISTING_UNIT
    proposed = {
        reading.proposed_name for reading in ROLE_READINGS_OVER_THE_EXISTING_UNIT
    }
    assert proposed == {"TANWEEN_ALIF_CARRIER", "SHADDA_*"}
    assert not proposed & set(existing_carrier_state_names())


def test_the_carrier_state_vocabulary_is_unchanged_by_this_registration() -> None:
    assert len(CarrierState) == 7


def test_a_role_without_existing_fields_is_refused() -> None:
    with pytest.raises(WordStructureDictionaryPreregistrationError):
        RoleReading(
            proposed_name="SHADDA_FATHA",
            existing_unit_fields=(),
            grounds="مُبرِّرٌ",
        )


def test_unsupplied_categories_are_recorded_not_guessed() -> None:
    assert GLOSSARY_CATEGORIES_NOT_YET_SUPPLIED
    for category in GLOSSARY_CATEGORIES_NOT_YET_SUPPLIED:
        assert category.why_it_is_not_compared.strip()
    supplied = {row.glossary_category for row in GLOSSARY_CONCORDANCE}
    unsupplied = {
        category.category_name for category in GLOSSARY_CATEGORIES_NOT_YET_SUPPLIED
    }
    assert not supplied & unsupplied


def test_an_unsupplied_category_without_a_reason_is_refused() -> None:
    with pytest.raises(WordStructureDictionaryPreregistrationError):
        UnsuppliedGlossaryCategory(category_name="فئةٌ", why_it_is_not_compared=" ")


def test_a_concordance_row_without_a_tree_reference_is_refused() -> None:
    with pytest.raises(WordStructureDictionaryPreregistrationError):
        GlossaryConcordanceRow(
            glossary_category="SUKUN",
            glossary_says="سكونٌ",
            this_tree_says="سكونٌ",
            tree_reference="",
            reading=ConcordanceReading.SAME_CONCEPT_ONE_ENTRY,
            what_was_settled="حُسِم",
        )


def test_an_unregistered_layer_lookup_is_refused_not_defaulted() -> None:
    with pytest.raises(WordStructureDictionaryPreregistrationError):
        layer_registration("الحرف_والحركة")  # type: ignore[arg-type]
