"""اختباراتُ السيلبنة: قوالبُ ستّةٌ مغلقة، ووزنٌ مشتقٌّ، وتعذّرٌ مُسمًّى لا خالٍ."""

from __future__ import annotations

from dataclasses import fields

import pytest

from alghanem.arabic.p_extractor import read_surface
from alghanem.arabic.syllabifier import (
    SYLLABIFIER_NAMED_RESIDUALS,
    Slot,
    SlotKind,
    StatedWaqfTransform,
    SyllabifiedWord,
    SyllabifierError,
    UnresolvedWazn,
    apply_stated_waqf,
    expand_slots,
    syllabify_surface,
)
from alghanem.arabic.syllable_preregistration import (
    PREREGISTRATION_DIGEST,
    STRUCTURAL_ACCEPTANCE_CONDITIONS,
    WAQF_TRANSFORM_RULES,
    SyllablePreregistrationError,
    SyllableTemplate,
    layer_registration,
    preregistration_digest,
    template_of,
)
from alghanem.arabic.word_structure_dictionary import WITHHELD_LAYERS
from alghanem.arabic.word_structure_dictionary_preregistration import (
    DictionaryLayer,
    LayerEpistemicStanding,
)

_BISMI = "\u0628\u0650\u0633\u0652\u0645\u0650"
_INNA = "\u0625\u0650\u0646\u064e\u0651\u0627"
_KITABAN = "\u0643\u0650\u062a\u064e\u0627\u0628\u064b\u0627"
_QALU = "\u0642\u064e\u0627\u0644\u064f\u0648\u0627"
_ALLAHI = "\u0627\u0644\u0644\u064e\u0651\u0647\u0650"
_RAHMATUN = "\u0631\u064e\u062d\u0652\u0645\u0629\u064c"


def test_the_templates_are_six_and_closed() -> None:
    assert len(SyllableTemplate) == 6
    assert {template.value for template in SyllableTemplate} == {
        "CV",
        "CVC",
        "CVV",
        "CVVC",
        "CVCC",
        "CVVCC",
    }


def test_the_preregistration_digest_did_not_drift() -> None:
    assert preregistration_digest() == PREREGISTRATION_DIGEST


def test_a_shape_outside_the_six_is_refused_not_rounded() -> None:
    with pytest.raises(SyllablePreregistrationError):
        template_of(0, 1, 0)
    with pytest.raises(SyllablePreregistrationError):
        template_of(1, 3, 0)
    with pytest.raises(SyllablePreregistrationError):
        template_of(1, 1, 3)


def test_the_wazn_is_a_projection_computed_on_demand() -> None:
    word = syllabify_surface(_BISMI)
    assert word.is_resolved
    assert word.wazn == "CVC-CV"
    stored = {field.name for field in fields(SyllabifiedWord)}
    assert "wazn" not in stored
    assert "wazn_unresolved" in stored


def test_the_shadda_is_expanded_into_a_closing_and_an_opening_slot() -> None:
    word = syllabify_surface(_INNA)
    assert [syllable.template.value for syllable in word.syllables] == ["CVC", "CVV"]


def test_the_tanween_is_read_as_a_vowel_plus_a_closing_consonant() -> None:
    word = syllabify_surface(_KITABAN)
    assert [syllable.template.value for syllable in word.syllables] == [
        "CV",
        "CVV",
        "CVC",
    ]
    slots, failure = expand_slots(read_surface(_KITABAN))
    assert failure is None
    assert any(slot.is_tanween_nun for slot in slots)


def test_the_differentiating_alif_takes_no_slot() -> None:
    word = syllabify_surface(_QALU)
    assert [syllable.template.value for syllable in word.syllables] == ["CVV", "CVV"]


def test_an_unsegmentable_word_names_its_standing_refusal() -> None:
    word = syllabify_surface(_ALLAHI)
    assert not word.is_resolved
    assert word.syllables == ()
    assert len(word.wazn_unresolved) == 1
    reason = word.wazn_unresolved[0].reason
    assert "\u0645\u062a\u0639\u0630\u0651\u0631" in reason


def test_asking_an_unresolved_word_for_a_wazn_raises_rather_than_invents() -> None:
    word = syllabify_surface(_ALLAHI)
    with pytest.raises(SyllabifierError):
        _ = word.wazn


def test_segmentation_is_deterministic() -> None:
    first = syllabify_surface(_KITABAN)
    second = syllabify_surface(_KITABAN)
    assert first == second


def test_every_emitted_syllable_reconstructs_its_slots() -> None:
    word = syllabify_surface(_KITABAN)
    slots, failure = expand_slots(read_surface(_KITABAN))
    assert failure is None
    rebuilt = tuple(slot for syllable in word.syllables for slot in syllable.slots)
    assert rebuilt == slots


def test_a_word_is_never_partly_segmented_and_partly_refused() -> None:
    with pytest.raises(SyllabifierError):
        SyllabifiedWord(
            surface=_BISMI,
            syllables=syllabify_surface(_BISMI).syllables,
            wazn_unresolved=(
                UnresolvedWazn(surface=_BISMI, letter_index=0, reason="سبب"),
            ),
        )


def test_a_word_refuses_a_foreign_preregistration_digest() -> None:
    with pytest.raises(SyllabifierError):
        SyllabifiedWord(surface=_BISMI, syllables=(), preregistration_digest="0" * 64)


def test_no_record_carries_a_null_wazn_field() -> None:
    for record in (SyllabifiedWord, UnresolvedWazn, Slot, StatedWaqfTransform):
        names = {field.name for field in fields(record)}
        assert "wazn" not in names
        assert not names & {"resolution", "verdict", "outcome", "decision"}


def test_a_consonant_slot_may_not_be_lengthened() -> None:
    with pytest.raises(SyllabifierError):
        Slot(kind=SlotKind.CONSONANT, letter_index=0, length=2)


def test_the_waqf_transform_is_offered_on_a_stated_input_with_its_limit() -> None:
    transform = apply_stated_waqf(read_surface(_RAHMATUN))
    assert transform.applied_rule is not None
    assert transform.applied_rule.name == "TAA_MARBUTA"
    assert transform.declared_limit.strip()
    assert {rule.name for rule in WAQF_TRANSFORM_RULES} == {
        "TANWEEN_DAMM_OR_KASR",
        "TANWEEN_FATH",
        "BARE_HARAKA",
        "TAA_MARBUTA",
    }


def test_the_waqf_transform_returns_no_rewritten_surface() -> None:
    names = {field.name for field in fields(StatedWaqfTransform)}
    assert "transformed_surface" not in names
    assert "transformed_units" not in names


def test_the_structural_floor_was_written_and_is_not_a_percentage() -> None:
    assert len(STRUCTURAL_ACCEPTANCE_CONDITIONS) == 4
    assert {condition.name for condition in STRUCTURAL_ACCEPTANCE_CONDITIONS} == {
        "CLOSURE",
        "RECONSTRUCTION",
        "TOTALITY",
        "DETERMINISM",
    }
    for condition in STRUCTURAL_ACCEPTANCE_CONDITIONS:
        assert condition.what_would_fail_it.strip()
        assert "%" not in condition.statement


def test_the_layer_is_still_withheld_with_its_declared_defect() -> None:
    withheld = {entry.layer: entry for entry in WITHHELD_LAYERS}
    assert DictionaryLayer.SYLLABLES_AND_WAZN in withheld
    entry = withheld[DictionaryLayer.SYLLABLES_AND_WAZN]
    assert entry.standing is LayerEpistemicStanding.HYPOTHESIS_WITH_A_DECLARED_DEFECT
    assert entry.refusal_field_name == "wazn_unresolved"
    assert layer_registration().refusal_field_name == "wazn_unresolved"


def test_the_named_residuals_are_sorted_and_unique() -> None:
    assert list(SYLLABIFIER_NAMED_RESIDUALS) == sorted(SYLLABIFIER_NAMED_RESIDUALS)
    assert len(set(SYLLABIFIER_NAMED_RESIDUALS)) == len(SYLLABIFIER_NAMED_RESIDUALS)
