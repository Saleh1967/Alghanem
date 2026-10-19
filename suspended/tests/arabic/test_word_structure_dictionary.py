"""اختباراتُ القاموس البنيويّ: المقيسُ يخرج قيمًا، والمحجوبُ حقلَ تعذّرٍ لا `None`."""

from __future__ import annotations

from dataclasses import fields

import pytest

from alghanem.arabic.encoding.carrier_state_candidate import (
    CarrierState,
    GeminationRole,
)
from alghanem.arabic.word_structure_dictionary import (
    MEASURED_LAYERS,
    WITHHELD_LAYERS,
    WithheldLayer,
    WordStructureDictionary,
    WordStructureDictionaryError,
    analyze_word,
)
from alghanem.arabic.word_structure_dictionary_preregistration import (
    DictionaryLayer,
    LayerEpistemicStanding,
)


def test_the_three_measured_layers_are_derived_from_the_preregistration() -> None:
    assert set(MEASURED_LAYERS) == {
        DictionaryLayer.LETTERS,
        DictionaryLayer.SHADDA_ANALYSIS,
        DictionaryLayer.TANWEEN_ANALYSIS,
    }
    assert {entry.layer for entry in WITHHELD_LAYERS} == {
        DictionaryLayer.SYLLABLES_AND_WAZN,
        DictionaryLayer.PHONETIC_FEATURES,
        DictionaryLayer.AL_ANALYSIS,
        DictionaryLayer.JARAD_ANALYSIS,
    }


def test_no_field_exists_for_a_withheld_layer_value() -> None:
    """الحجبُ بنيويّ: لا حقلَ أصلًا يقبل قيمةً خاليةً لطبقةٍ محجوبة."""

    names = {declared.name for declared in fields(WordStructureDictionary)}
    for forbidden in ("wazn", "syllables", "makhraj", "manner", "al_", "jarad"):
        assert not any(forbidden in name for name in names)


def test_every_withheld_layer_names_its_refusal_field() -> None:
    dictionary = analyze_word("كَتَبَ")
    for layer in (
        DictionaryLayer.SYLLABLES_AND_WAZN,
        DictionaryLayer.PHONETIC_FEATURES,
        DictionaryLayer.AL_ANALYSIS,
        DictionaryLayer.JARAD_ANALYSIS,
    ):
        entry = dictionary.refusal_field_for(layer)
        assert entry.refusal_field_name.strip()
        assert entry.entry_condition.strip()
        assert (
            entry.standing is not LayerEpistemicStanding.MEASURED_BY_AN_EXISTING_CODEC
        )


def test_a_measured_layer_has_no_refusal_field() -> None:
    dictionary = analyze_word("كَتَبَ")
    with pytest.raises(WordStructureDictionaryError):
        dictionary.refusal_field_for(DictionaryLayer.LETTERS)


def test_a_measured_layer_may_not_be_declared_withheld() -> None:
    with pytest.raises(WordStructureDictionaryError):
        WithheldLayer(
            layer=DictionaryLayer.LETTERS,
            standing=LayerEpistemicStanding.MEASURED_BY_AN_EXISTING_CODEC,
            refusal_field_name="letters_unread",
            what_the_refusal_field_says="قولٌ",
            entry_condition="شرطٌ",
        )


def test_the_aggregate_keeps_each_layer_standing() -> None:
    dictionary = analyze_word("كَتَبَ")
    assert (
        dictionary.standing_of(DictionaryLayer.LETTERS)
        is LayerEpistemicStanding.MEASURED_BY_AN_EXISTING_CODEC
    )
    assert (
        dictionary.standing_of(DictionaryLayer.PHONETIC_FEATURES)
        is LayerEpistemicStanding.IMPORTED_BEHIND_AN_OPEN_BARRIER
    )
    assert (
        dictionary.standing_of(DictionaryLayer.AL_ANALYSIS)
        is LayerEpistemicStanding.UNDECIDABLE_FROM_THE_WRITTEN_MARKS
    )


def test_letters_carry_the_existing_vocabulary_names_only() -> None:
    dictionary = analyze_word("الْحَمْدُ")
    names = [reading.state_name for reading in dictionary.letters]
    assert names == [
        "SUKUN_IMPLICIT",
        "SUKUN_EXPLICIT",
        "FATHA",
        "SUKUN_EXPLICIT",
        "DAMMA",
    ]
    assert all(reading.state in CarrierState for reading in dictionary.letters)


def test_the_surface_round_trip_is_reported_for_every_reading() -> None:
    for word in ("الْحَمْدُ", "الرَّحْمَنِ", "كَتَبَ", "مَرَضاً", "كِتَابٌ"):
        assert analyze_word(word).surface_round_trips is True


def test_a_shadda_is_a_role_and_its_source_stays_undecided() -> None:
    doubled = analyze_word("سَبَّحَ")
    assert [(role.position, role.carrier) for role in doubled.shadda_roles] == [
        (1, "ب")
    ]
    assert doubled.shadda_roles[0].source_undecided.strip()
    assert not hasattr(doubled.shadda_roles[0], "source")
    assert doubled.letters[1].gemination is GeminationRole.PAIR_START
    assert doubled.letters[1].state is CarrierState.SUKUN_IMPLICIT


def test_the_sun_lam_is_not_distinguished_from_any_unmarked_letter() -> None:
    """لامُ «الرَّحْمَنِ» تخرج `SUKUN_IMPLICIT` كأيِّ حرفٍ بلا علامة، فلا تُنسَب الشدّة."""

    reading = analyze_word("الرَّحْمَنِ")
    assert reading.letters[1].carrier == "ل"
    assert reading.letters[1].state is CarrierState.SUKUN_IMPLICIT
    assert len(reading.shadda_roles) == 1
    role_fields = {declared.name for declared in fields(type(reading.shadda_roles[0]))}
    assert "source" not in role_fields
    assert "source_undecided" in role_fields


def test_a_tanween_is_a_role_read_from_the_existing_fields() -> None:
    seated = analyze_word("مَرَضاً")
    assert len(seated.tanween_roles) == 1
    assert seated.tanween_roles[0].seated_on_alif is True
    assert seated.tanween_roles[0].state is CarrierState.FATHA

    unseated = analyze_word("كِتَابٌ")
    assert len(unseated.tanween_roles) == 1
    assert unseated.tanween_roles[0].seated_on_alif is False
    assert unseated.tanween_roles[0].state is CarrierState.DAMMA


def test_a_passthrough_is_recorded_unread_not_counted_as_a_letter() -> None:
    reading = analyze_word("كَتَبَ!")
    assert [segment.codepoint for segment in reading.unread] == ["!"]
    assert all(
        letter.state is not CarrierState.PASSTHROUGH for letter in reading.letters
    )
    assert len(reading.letters) == 3


def test_an_empty_or_non_string_surface_is_refused_not_read_as_empty() -> None:
    for blank in ("", "   "):
        with pytest.raises(WordStructureDictionaryError):
            analyze_word(blank)
    with pytest.raises(WordStructureDictionaryError):
        analyze_word(None)  # type: ignore[arg-type]


def test_a_dictionary_that_releases_a_withheld_layer_is_refused() -> None:
    reading = analyze_word("كَتَبَ")
    with pytest.raises(WordStructureDictionaryError):
        WordStructureDictionary(
            surface=reading.surface,
            surface_round_trips=reading.surface_round_trips,
            letters=reading.letters,
            unread=reading.unread,
            shadda_roles=reading.shadda_roles,
            tanween_roles=reading.tanween_roles,
            withheld=reading.withheld[1:],
        )
