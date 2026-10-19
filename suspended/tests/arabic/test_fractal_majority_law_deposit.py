"""اختباراتُ إيداع القانون الغالب: كلُّ رقمٍ يُعاد من القرص، ولا حكمَ مكتوب."""

from __future__ import annotations

import pytest

from alghanem.arabic.fractal_majority_law_deposit import (
    FRACTAL_MAJORITY_LAW_NAMED_RESIDUALS as RESIDUALS,
)
from alghanem.arabic.fractal_majority_law_deposit import (
    THE_ENDING_SHAPE_AS_TRANSCRIBED,
    THE_ENTROPY_TOLERANCE,
    THE_FIRST_CONDITION,
    THE_FOUR_BREAKS,
    THE_LEVELS,
    THE_QUOTED_ENDING_SHAPE,
    THE_QUOTED_FIRST_POSITION_DENOMINATOR,
    THE_SECOND_CONDITION,
    THE_SHARE_TOLERANCE,
    THE_THREE_SIGNATURES,
    BreakGenus,
    Comparison,
    ConditionStanding,
    EndingKey,
    FractalMajorityLawError,
    LevelStanding,
    NamedBreak,
    PositionCensus,
    QuotedRow,
    SlotClass,
    Verdict,
    measured_rows,
    measured_share_of_the_table,
    reading_for,
    the_corpus_gate_is_untouched,
    the_direction_holds_on_every_key,
    the_marked_word_count,
    the_measured_ladder,
    the_transcription_verdicts,
    transcribed_rows_from_disk,
)

# ---------------------------------------------------------------------------
# الشرطُ الثاني: مقيسٌ من القرص، لا منقولٌ ولا مكتوب
# ---------------------------------------------------------------------------


def test_the_ladder_carries_both_declared_keys_once_each() -> None:
    keys = [reading.key for reading in the_measured_ladder()]
    assert keys == list(EndingKey)


def test_every_census_counts_every_slot_class_and_conserves_the_slots() -> None:
    for reading in the_measured_ladder():
        for census in (reading.interior, reading.ending):
            assert set(census.as_mapping) == set(SlotClass)
        assert reading.interior.total_slots > reading.ending.total_slots > 0


def test_the_two_keys_move_the_ending_denominator_by_the_unmarked_words() -> None:
    by_base = reading_for(EndingKey.LAST_BASE_SLOT).ending
    by_mark = reading_for(EndingKey.LAST_MARKED_SLOT).ending
    assert by_base.total_slots != by_mark.total_slots
    assert by_mark.as_mapping[SlotClass.UNMARKED] == 0
    assert by_base.as_mapping[SlotClass.UNMARKED] > 0


def test_the_tanwin_of_the_ending_moves_with_the_key() -> None:
    by_base = reading_for(EndingKey.LAST_BASE_SLOT).ending
    by_mark = reading_for(EndingKey.LAST_MARKED_SLOT).ending
    assert by_mark.as_mapping[SlotClass.TANWIN] > by_base.as_mapping[SlotClass.TANWIN]


def test_the_direction_holds_on_every_key_and_is_not_a_vacuous_claim() -> None:
    assert the_direction_holds_on_every_key() is True
    for reading in the_measured_ladder():
        assert reading.fatha_collapse > 0.05
        assert reading.entropy_rise > 0.05


def test_the_ending_is_not_the_resting_place_on_either_key() -> None:
    for reading in the_measured_ladder():
        assert reading.ending.three_vowel_entropy > reading.interior.three_vowel_entropy


def test_the_transcribed_table_matches_what_the_disk_measures() -> None:
    assert transcribed_rows_from_disk() == THE_ENDING_SHAPE_AS_TRANSCRIBED


# ---------------------------------------------------------------------------
# المقابلةُ: الحكمُ مشتقٌّ، والاتّجاهُ غيرُ المقدار
# ---------------------------------------------------------------------------


def test_every_quoted_figure_is_compared_on_both_keys() -> None:
    comparisons = the_transcription_verdicts()
    assert len(comparisons) == len(EndingKey) * 9
    assert {comparison.key for comparison in comparisons} == set(EndingKey)


def test_the_interior_rows_agree_and_the_ending_rows_mostly_contradict() -> None:
    interior = [
        comparison
        for comparison in the_transcription_verdicts()
        if comparison.name.startswith("داخل اللفظ")
    ]
    ending = [
        comparison
        for comparison in the_transcription_verdicts()
        if comparison.name.startswith("خاتمة اللفظ")
    ]
    assert interior and ending
    assert all(comparison.verdict is Verdict.AGREES for comparison in interior)
    contradicting = [
        comparison for comparison in ending if comparison.verdict is Verdict.CONTRADICTS
    ]
    assert len(contradicting) == len(ending) - 1


def test_the_quoted_sukun_and_tanwin_share_contradicts_on_both_keys() -> None:
    rows = [
        comparison
        for comparison in the_transcription_verdicts()
        if comparison.name.endswith("سكون+تنوين")
    ]
    assert len(rows) == len(EndingKey)
    assert all(row.verdict is Verdict.CONTRADICTS for row in rows)


def test_a_verdict_is_recomputed_and_flips_with_the_figure() -> None:
    agreeing = Comparison(
        name="مصنوعٌ للاختبار",
        key=EndingKey.LAST_BASE_SLOT,
        quoted=0.500,
        measured=0.505,
        tolerance=THE_SHARE_TOLERANCE,
    )
    assert agreeing.verdict is Verdict.AGREES
    contradicting = Comparison(
        name="مصنوعٌ للاختبار",
        key=EndingKey.LAST_BASE_SLOT,
        quoted=0.500,
        measured=0.560,
        tolerance=THE_SHARE_TOLERANCE,
    )
    assert contradicting.verdict is Verdict.CONTRADICTS


def test_a_non_positive_tolerance_is_refused() -> None:
    with pytest.raises(FractalMajorityLawError):
        Comparison(
            name="حدٌّ فاسد",
            key=EndingKey.LAST_BASE_SLOT,
            quoted=0.5,
            measured=0.9,
            tolerance=0.0,
        )


def test_the_declared_tolerances_are_small_enough_to_refuse_something() -> None:
    assert 0.0 < THE_SHARE_TOLERANCE <= 0.02
    assert 0.0 < THE_ENTROPY_TOLERANCE <= 0.02


def test_a_quoted_row_that_does_not_sum_to_one_is_refused() -> None:
    with pytest.raises(FractalMajorityLawError):
        QuotedRow("مصنوع", 0.6, 0.2, 0.05, 1.3)


def test_the_quoted_shape_is_two_rows_and_the_ending_is_the_wider_one() -> None:
    interior, ending = THE_QUOTED_ENDING_SHAPE
    assert interior.fatha > ending.fatha
    assert ending.entropy > interior.entropy


# ---------------------------------------------------------------------------
# التقاطعُ مع مقامٍ منقولٍ في وحدةٍ أخرى
# ---------------------------------------------------------------------------


def test_the_marked_word_count_reproduces_the_quoted_denominator() -> None:
    assert the_marked_word_count() == THE_QUOTED_FIRST_POSITION_DENOMINATOR


def test_the_marked_word_count_is_below_the_whole_word_count() -> None:
    ending = reading_for(EndingKey.LAST_BASE_SLOT).ending
    assert the_marked_word_count() < ending.total_slots


# ---------------------------------------------------------------------------
# الجدولُ قانونًا غالبًا، وكسورُه الأربعة
# ---------------------------------------------------------------------------


def test_every_level_row_names_its_standing_and_its_place() -> None:
    for row in THE_LEVELS:
        assert isinstance(row.standing, LevelStanding)
        assert row.where.strip()


def test_the_law_is_a_majority_and_not_a_total_one() -> None:
    assert 0.0 < measured_share_of_the_table() < 1.0
    assert measured_rows()


def test_the_breaks_are_four_named_and_each_sits_on_a_declared_level() -> None:
    assert len(THE_FOUR_BREAKS) == 4
    levels = {row.level for row in THE_LEVELS}
    for a_break in THE_FOUR_BREAKS:
        assert a_break.level in levels
        assert a_break.where_it_breaks.strip()
        assert isinstance(a_break.genus, BreakGenus)


def test_each_break_genus_is_used_and_no_break_is_unsourced() -> None:
    assert {a_break.genus for a_break in THE_FOUR_BREAKS} == set(BreakGenus)
    assert all(a_break.source.strip() for a_break in THE_FOUR_BREAKS)


def test_a_break_without_a_place_is_refused() -> None:
    with pytest.raises(FractalMajorityLawError):
        NamedBreak(
            name="كسرٌ بلا موضع",
            level="الكلمة",
            where_it_breaks="   ",
            genus=BreakGenus.MEASURED_ON_OUR_SEALED_BYTES,
            source="لا شيء",
        )


def test_the_signatures_are_the_three_that_were_signed() -> None:
    names = [signature.name for signature in THE_THREE_SIGNATURES]
    assert names == ["الحنجرةُ ثلاثُ حالات", "الصوائتُ مجهورة", "غالبٌ لا تام"]
    assert all(signature.what_it_changes.strip() for signature in THE_THREE_SIGNATURES)


def test_the_laryngeal_row_is_asserted_and_never_read_as_measured() -> None:
    laryngeal = next(row for row in THE_LEVELS if row.level == "الحنجرة")
    assert laryngeal.standing is LevelStanding.ASSERTED_AND_NOT_MEASURED
    assert laryngeal not in measured_rows()


# ---------------------------------------------------------------------------
# الشرطان مُقيَّدان بمصدريهما
# ---------------------------------------------------------------------------


def test_the_first_condition_is_blocked_and_has_no_agreement_verdict() -> None:
    assert (
        THE_FIRST_CONDITION.standing
        is ConditionStanding.BLOCKED_ON_BYTES_NOT_DEPOSITED_HERE
    )
    assert THE_FIRST_CONDITION.verdict_genus is Verdict.NOT_CHECKABLE_HERE
    assert "Algebra" in THE_FIRST_CONDITION.bound_to


def test_the_second_condition_is_bound_to_our_sealed_corpus() -> None:
    assert THE_SECOND_CONDITION.standing is ConditionStanding.RUN_ON_OUR_SEALED_BYTES
    assert "quran-simple-enhanced" in THE_SECOND_CONDITION.bound_to
    assert THE_SECOND_CONDITION.verdict_genus is None


def test_a_condition_without_a_source_is_refused() -> None:
    with pytest.raises(FractalMajorityLawError):
        THE_SECOND_CONDITION.__class__(
            question="سؤالٌ بلا مصدر",
            standing=ConditionStanding.RUN_ON_OUR_SEALED_BYTES,
            bound_to="  ",
            reading="قراءة",
        )


# ---------------------------------------------------------------------------
# الخمولُ والبقايا
# ---------------------------------------------------------------------------


def test_the_markov_gate_is_not_moved_by_this_deposit() -> None:
    assert the_corpus_gate_is_untouched() is True


def test_every_named_residual_is_keyed_by_its_own_token() -> None:
    assert RESIDUALS
    for token, text in RESIDUALS.items():
        assert text.startswith(f"{token}:")


def test_a_census_on_an_empty_denominator_refuses_a_share() -> None:
    empty = PositionCensus("مصنوع", tuple((member, 0) for member in SlotClass))
    with pytest.raises(FractalMajorityLawError):
        _ = empty.three_vowel_shares
