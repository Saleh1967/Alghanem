"""اختباراتُ توسيع المجتمع: علامةٌ صارت حرفًا فاختفت عن تعداد العلامات."""

from __future__ import annotations

import glob
import unicodedata

import pytest

from alghanem.arabic.fath_ayah_source_text import FATH_AYAH_SOURCE_TEXT
from alghanem.arabic.fatiha_source_text import FATIHA_LINES
from alghanem.arabic.hidden_mark_population import (
    HAMZA_ABOVE,
    HAMZA_BELOW,
    MADDAH_ABOVE,
    THE_POPULATION_MEASURED_BY_UNICODE_VERSION,
    HiddenMarkError,
    InvisibilityReading,
    arabic_letters,
    classes_are_pairwise_distinct,
    combining_classes_of,
    foreign_decomposables,
    fused_bases,
    fused_letters,
    fusion_is_order_indifferent,
    fusion_passes_through,
    hidden_marks,
    hidden_marks_are_all_combining,
    hidden_marks_are_disjoint_from_the_nine,
    letter_named_marks,
    normalization_delta,
    order_bearing_pairs,
    read_invisibility,
    the_identity_holds_on,
    the_population_recorded_for,
)
from alghanem.arabic.hidden_mark_population import (
    HIDDEN_MARK_NAMED_RESIDUALS as RESIDUALS,
)
from alghanem.arabic.mark_pair_census import THE_NINE_MARKS
from alghanem.arabic.written_haraka_mark import (
    arabic_combining_marks,
    the_superset_recorded_for,
)

FATIHA = "\n".join(FATIHA_LINES)


def test_the_widened_population_is_the_whole_arabic_letter_universe() -> None:
    letters = the_population_recorded_for(unicodedata.unidata_version)
    marks = the_superset_recorded_for(unicodedata.unidata_version)
    if letters is None or marks is None:
        pytest.skip(f"لم يُقَس على يونيكود {unicodedata.unidata_version} بعد.")
    assert len(arabic_letters()) == letters
    assert len(arabic_combining_marks()) == marks


def test_the_population_is_a_fact_about_a_unicode_version_not_about_arabic() -> None:
    assert THE_POPULATION_MEASURED_BY_UNICODE_VERSION["13.0.0"] == 968
    assert THE_POPULATION_MEASURED_BY_UNICODE_VERSION["15.0.0"] == 970


def test_an_unmeasured_unicode_version_is_refused_not_guessed() -> None:
    assert the_population_recorded_for("1.0.0") is None


def test_only_eight_letters_of_the_population_are_not_simple() -> None:
    fused = fused_letters()
    assert len(fused) == 8
    assert len(fused) / len(arabic_letters()) < 0.01


def test_the_five_arabic_fused_letters_are_the_ones_expected() -> None:
    assert set("\u0622\u0623\u0624\u0625\u0626") <= set(fused_letters())


def test_every_fused_letter_really_decomposes_into_carrier_and_mark() -> None:
    for letter in fused_letters():
        decomposed = unicodedata.normalize("NFD", letter)
        assert len(decomposed) == 2
        assert unicodedata.combining(decomposed[0]) == 0
        assert unicodedata.combining(decomposed[1]) != 0


def test_exactly_three_marks_are_hidden_inside_the_eight() -> None:
    assert hidden_marks() == (MADDAH_ABOVE, HAMZA_ABOVE, HAMZA_BELOW)


def test_the_hidden_are_marks_by_the_table_not_by_assertion() -> None:
    assert hidden_marks_are_all_combining()


def test_none_of_the_hidden_is_among_the_nine_we_have_been_counting() -> None:
    assert hidden_marks_are_disjoint_from_the_nine()
    assert not (set(hidden_marks()) & set(THE_NINE_MARKS))


def test_the_two_families_share_no_combining_class_either() -> None:
    assert not (
        set(combining_classes_of(hidden_marks()))
        & set(combining_classes_of(THE_NINE_MARKS))
    )


def test_the_nine_are_pairwise_distinct_but_the_three_are_not() -> None:
    assert classes_are_pairwise_distinct(THE_NINE_MARKS)
    assert not classes_are_pairwise_distinct(hidden_marks())


def test_the_order_rule_proved_for_the_nine_fails_here() -> None:
    assert order_bearing_pairs(THE_NINE_MARKS) == ()
    assert order_bearing_pairs(hidden_marks()) == ((MADDAH_ABOVE, HAMZA_ABOVE),)


def test_the_order_bearing_pair_really_survives_normalization() -> None:
    first = unicodedata.normalize("NFC", f"\u0628{MADDAH_ABOVE}{HAMZA_ABOVE}")
    second = unicodedata.normalize("NFC", f"\u0628{HAMZA_ABOVE}{MADDAH_ABOVE}")
    assert first != second


def test_a_haraka_does_not_shield_the_alef_from_fusion() -> None:
    for haraka in THE_NINE_MARKS:
        assert fusion_passes_through(haraka)
        assert fusion_is_order_indifferent(haraka)


def test_fusion_through_a_haraka_yields_the_fused_letter_and_keeps_the_haraka() -> None:
    composed = unicodedata.normalize("NFC", f"\u0627\u064e{HAMZA_ABOVE}")
    assert composed == "\u0623\u064e"


def test_a_non_combining_blocker_is_refused_rather_than_answered() -> None:
    with pytest.raises(HiddenMarkError):
        fusion_passes_through("\u0627")
    with pytest.raises(HiddenMarkError):
        fusion_is_order_indifferent("\u0627")


def test_the_deposits_write_eleven_of_these_marks_and_show_none() -> None:
    fatiha = read_invisibility(FATIHA, "الفاتحة")
    fath = read_invisibility(FATH_AYAH_SOURCE_TEXT, "الفتح")
    assert (fatiha.written, fath.written) == (3, 8)
    assert (fatiha.standalone, fath.standalone) == (0, 0)
    assert fatiha.seen_by_a_mark_census == 0
    assert fath.seen_by_a_mark_census == 0


def test_the_invisible_share_on_both_deposits_is_total() -> None:
    for text in (FATIHA, FATH_AYAH_SOURCE_TEXT):
        assert read_invisibility(text, "نطاق").invisible_share == 100.0


def test_a_fused_carrier_may_also_bear_one_of_the_nine() -> None:
    fatiha = read_invisibility(FATIHA, "الفاتحة")
    fath = read_invisibility(FATH_AYAH_SOURCE_TEXT, "الفتح")
    assert fatiha.fused_carriers_also_marked == 3
    assert fath.fused_carriers_also_marked == 6


def test_the_standalone_count_is_zero_before_normalization_too() -> None:
    three = set(hidden_marks())
    for text in (FATIHA, FATH_AYAH_SOURCE_TEXT):
        assert not [character for character in text if character in three]


def test_the_fused_carriers_account_for_the_whole_normalization_delta() -> None:
    for text in (FATIHA, FATH_AYAH_SOURCE_TEXT):
        assert the_identity_holds_on(text)
        assert normalization_delta(text) == read_invisibility(text, "نطاق").hidden


def test_the_deposits_carry_no_foreign_decomposable_at_all() -> None:
    for text in (FATIHA, FATH_AYAH_SOURCE_TEXT):
        assert foreign_decomposables(text) == 0


def test_the_identity_breaks_exactly_by_the_foreign_decomposables() -> None:
    mixed = f"{FATIHA}\n≠ ā ∉"
    reading = read_invisibility(mixed, "مخلوط")
    assert not the_identity_holds_on(mixed)
    assert normalization_delta(mixed) - reading.hidden == foreign_decomposables(mixed)


def test_the_break_is_accounted_on_the_whole_tree_prose() -> None:
    prose = "\n".join(
        open(path, encoding="utf-8").read()
        for path in sorted(glob.glob("src/alghanem/**/*.py", recursive=True))
    )
    reading = read_invisibility(prose, "النثر")
    assert normalization_delta(prose) - reading.hidden == foreign_decomposables(prose)


def test_exactly_one_combining_mark_is_named_a_letter() -> None:
    named = letter_named_marks()
    assert named == ("\u0670",)
    assert "LETTER" in unicodedata.name(named[0])


def test_the_alef_is_the_commonest_base_of_the_fused_letters() -> None:
    bases = fused_bases()
    assert bases[0] == ("\u0627", 3)
    assert sum(count for _, count in bases) == len(fused_letters())


def test_a_reading_without_a_scope_is_refused() -> None:
    with pytest.raises(HiddenMarkError):
        InvisibilityReading(
            scope="  ", standalone=0, hidden=1, fused_carriers_also_marked=0
        )


def test_more_marked_carriers_than_carriers_is_refused() -> None:
    with pytest.raises(HiddenMarkError):
        InvisibilityReading(
            scope="نطاق", standalone=0, hidden=1, fused_carriers_also_marked=2
        )


def test_a_negative_occurrence_is_refused() -> None:
    with pytest.raises(HiddenMarkError):
        InvisibilityReading(
            scope="نطاق", standalone=-1, hidden=1, fused_carriers_also_marked=0
        )


def test_a_share_of_nothing_is_refused_rather_than_returned_as_zero() -> None:
    empty = read_invisibility("بسم", "بلا مخفيّ")
    assert empty.written == 0
    with pytest.raises(HiddenMarkError):
        empty.invisible_share


def test_the_gap_is_left_open_and_the_nine_are_untouched() -> None:
    assert len(THE_NINE_MARKS) == 9
    assert not (set(THE_NINE_MARKS) & set(hidden_marks()))
    assert "THE_GAP_IS_NAMED_AND_MEASURED_HERE_BUT_NOT_CLOSED" in RESIDUALS


def test_every_residual_is_named_by_its_own_key() -> None:
    assert RESIDUALS
    for key, text in RESIDUALS.items():
        assert text.startswith(f"{key}: ")


def test_the_residuals_name_the_blindness_and_the_broken_order_rule() -> None:
    assert "A_MARK_THAT_BECAME_A_LETTER_IS_INVISIBLE_TO_A_MARK_CENSUS" in RESIDUALS
    assert (
        "THE_ORDER_RULE_PROVED_FOR_THE_NINE_FAILS_IN_THE_WIDER_POPULATION" in RESIDUALS
    )
