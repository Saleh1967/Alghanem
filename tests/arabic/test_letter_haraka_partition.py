"""اختباراتُ جدول الحرف والحركة: العدّةُ، والخلوُّ، وسترلنج، وفجوةُ الجشع."""

from __future__ import annotations

import math

import pytest

from alghanem.arabic.letter_haraka_partition import (
    A_BELL_NUMBER_IS_A_COUNT_OF_THE_SPACE_NOT_A_SEARCH_OF_IT,
    A_GREEDY_MERGE_THAT_USUALLY_WINS_IS_NOT_AN_OPTIMISER,
    A_MODULE_THAT_MEASURES_THE_TREE_LEAVES_ITSELF_OUT,
    AN_EMPTY_CELL_UNDER_A_SPARSE_MARGIN_IS_NOT_A_PROHIBITION,
    LETTER_HARAKA_PARTITION_NAMED_RESIDUALS,
    NO_MEASUREMENT_HERE_LIFTS_A_BLOCK_OR_THAWS_A_FREEZE,
    THE_DECLARED_HARAKAT,
    THE_DECLARED_LETTERS,
    THE_DECLARED_PROBES,
    THE_HUNDRED_AND_TWELVE,
    THE_HUNDRED_AND_TWELVE_IS_A_DECLARATION_NOT_A_DISCOVERY,
    THE_PREREGISTERED_GREEDY_CONDITION,
    THE_SURPRISE_FLOOR,
    AbsenceStanding,
    CellAbsence,
    GreedyStanding,
    LetterHarakaPartitionError,
    PartitionProbe,
    ProbeReading,
    SourceRung,
    absent_cells,
    bell_number,
    cell_counts,
    greedy_partition,
    greedy_standing,
    letter_profiles,
    measure_greedy_gap,
    optimal_partition,
    partition_criterion,
    partitions_of,
    rung_text,
    stirling_second_kind,
    table_census,
    the_block_and_the_freeze_are_untouched,
    the_declared_probes,
    verify_stirling_matches_its_recurrence,
    verify_the_enumeration_counts_what_stirling_says,
)


class TestTheDeclaredUnits:
    """المُعلَنُ يُفحَص بوصفه قرارًا، لا يُؤخذ رقمًا."""

    def test_the_alphabet_is_twenty_eight_without_the_bare_hamza(self) -> None:
        assert len(THE_DECLARED_LETTERS) == 28
        assert "ء" not in THE_DECLARED_LETTERS
        assert len(set(THE_DECLARED_LETTERS)) == 28

    def test_the_harakat_are_four_and_exclude_tanwin_and_shadda(self) -> None:
        assert len(THE_DECLARED_HARAKAT) == 4
        assert "\u0651" not in THE_DECLARED_HARAKAT
        assert "\u064b" not in THE_DECLARED_HARAKAT
        assert "\u0670" not in THE_DECLARED_HARAKAT

    def test_the_hundred_and_twelve_is_computed_from_the_two_declarations(self) -> None:
        assert THE_HUNDRED_AND_TWELVE == 112
        assert THE_HUNDRED_AND_TWELVE == len(THE_DECLARED_LETTERS) * len(
            THE_DECLARED_HARAKAT
        )


class TestTheLadder:
    """الدرجاتُ تراكميّةٌ، والامتلاءُ يزيد ولا ينقص."""

    def test_each_rung_contains_the_text_of_the_rung_before_it(self) -> None:
        first = rung_text(SourceRung.FATIHA)
        second = rung_text(SourceRung.WITH_FATH)
        third = rung_text(SourceRung.WITH_PROSE)
        assert first in second
        assert second in third

    def test_realized_cells_never_decrease_along_the_ladder(self) -> None:
        readings = [table_census(rung).realized_cells for rung in SourceRung]
        assert readings == sorted(readings)

    def test_the_ladder_lands_on_the_recorded_census(self) -> None:
        assert table_census(SourceRung.FATIHA).realized_cells == 41
        assert table_census(SourceRung.WITH_FATH).realized_cells == 74
        assert table_census(SourceRung.WITH_PROSE).realized_cells == 109

    def test_every_declared_letter_appears_only_at_the_widest_rung(self) -> None:
        assert table_census(SourceRung.FATIHA).letters_present < 28
        assert table_census(SourceRung.WITH_FATH).letters_present == 27
        assert table_census(SourceRung.WITH_PROSE).letters_present == 28

    def test_the_table_does_not_fill_even_at_the_widest_rung(self) -> None:
        widest = table_census(SourceRung.WITH_PROSE)
        assert widest.empty_cells == 3
        assert widest.realized_cells < THE_HUNDRED_AND_TWELVE

    def test_no_cell_falls_outside_the_two_declarations(self) -> None:
        for letter, haraka in cell_counts(SourceRung.WITH_PROSE):
            assert letter in THE_DECLARED_LETTERS
            assert haraka in THE_DECLARED_HARAKAT

    def test_the_census_refuses_a_count_above_the_table(self) -> None:
        from alghanem.arabic.letter_haraka_partition import TableCensus

        with pytest.raises(LetterHarakaPartitionError):
            TableCensus(
                rung=SourceRung.FATIHA,
                realized_cells=113,
                occurrences=1,
                letters_present=1,
            )


class TestTheAbsences:
    """الخلوُّ يُقاس بهوامشه، ولا يُقرأ منعًا بمجرّده."""

    def test_the_three_absences_are_named_exactly(self) -> None:
        absences = absent_cells()
        assert len(absences) == 3
        assert {(item.letter, item.haraka) for item in absences} == {
            ("ا", "\u064e"),
            ("ا", "\u0652"),
            ("ز", "\u0652"),
        }

    def test_every_absence_carries_one_of_the_two_standings_and_no_third(self) -> None:
        absences = absent_cells()
        standings = [item.standing for item in absences]
        assert len(standings) == len(absences)
        assert set(standings) <= {
            AbsenceStanding.CONSISTENT_WITH_SCARCITY,
            AbsenceStanding.SURPRISING_UNDER_THE_MARGIN,
        }

    def test_the_alef_fatha_is_surprising_at_every_measurement(self) -> None:
        alef = next(
            item
            for item in absent_cells()
            if (item.letter, item.haraka) == ("ا", "\u064e")
        )
        assert alef.standing is AbsenceStanding.SURPRISING_UNDER_THE_MARGIN

    def test_the_zay_standing_is_read_off_the_floor_and_not_frozen_here(self) -> None:
        zay = next(item for item in absent_cells() if item.letter == "ز")
        floor = -math.log(THE_SURPRISE_FLOOR)
        expected_standing = (
            AbsenceStanding.SURPRISING_UNDER_THE_MARGIN
            if zay.expected > floor
            else AbsenceStanding.CONSISTENT_WITH_SCARCITY
        )
        assert zay.standing is expected_standing

    def test_the_zay_cell_sits_just_past_the_margin_and_drifts_with_the_tree(
        self,
    ) -> None:
        floor = -math.log(THE_SURPRISE_FLOOR)
        zay = next(item for item in absent_cells() if item.letter == "ز")
        assert floor < zay.expected < 2 * floor, (
            "منزلةُ هذه الخليّة مؤرَّخةٌ بهامشها: عبرت العتبةَ بنموّ النثر "
            "وحدَه، وما زالت دون ضعفها؛ فلا يُجمَّد لها مقدارٌ بعينه."
        )

    def test_the_alef_row_is_itself_almost_empty(self) -> None:
        alef = next(item for item in absent_cells() if item.letter == "ا")
        assert alef.row_total < 20

    def test_the_standing_is_a_function_of_the_floor_and_nothing_else(self) -> None:
        just_under = CellAbsence(
            letter="ب",
            haraka="\u0652",
            row_total=10,
            expected=-math.log(THE_SURPRISE_FLOOR) + 1.0,
        )
        just_over = CellAbsence(
            letter="ب",
            haraka="\u0652",
            row_total=10,
            expected=-math.log(THE_SURPRISE_FLOOR) - 1.0,
        )
        assert just_under.standing is AbsenceStanding.SURPRISING_UNDER_THE_MARGIN
        assert just_over.standing is AbsenceStanding.CONSISTENT_WITH_SCARCITY

    def test_a_negative_expectation_is_refused(self) -> None:
        with pytest.raises(LetterHarakaPartitionError):
            CellAbsence(letter="ب", haraka="\u0652", row_total=1, expected=-0.5)

    def test_a_narrow_rung_has_far_more_absences_than_the_wide_one(self) -> None:
        assert len(absent_cells(SourceRung.FATIHA)) == 112 - 41


class TestStirlingAndBell:
    """العدُّ يُفحَص بتكراره، وبمطابقة المولِّد له."""

    def test_the_recurrence_holds_where_it_is_checked(self) -> None:
        assert verify_stirling_matches_its_recurrence() is True

    def test_the_enumeration_produces_exactly_what_stirling_counts(self) -> None:
        assert verify_the_enumeration_counts_what_stirling_says() is True

    def test_the_known_small_values(self) -> None:
        assert stirling_second_kind(10, 2) == 511
        assert stirling_second_kind(10, 3) == 9330
        assert stirling_second_kind(10, 4) == 34105
        assert stirling_second_kind(0, 0) == 1
        assert stirling_second_kind(5, 0) == 0
        assert stirling_second_kind(3, 5) == 0

    def test_bell_is_the_sum_of_its_stirling_row(self) -> None:
        for count in range(9):
            assert bell_number(count) == sum(
                stirling_second_kind(count, classes) for classes in range(count + 1)
            )
        assert bell_number(28) > 10**21

    def test_a_negative_count_is_refused(self) -> None:
        with pytest.raises(LetterHarakaPartitionError):
            stirling_second_kind(-1, 2)

    def test_the_enumeration_partitions_are_exhaustive_and_disjoint(self) -> None:
        items = ("أ", "ب", "ج", "د")
        for classes in range(1, 5):
            for partition in partitions_of(items, classes):
                flat = [letter for block in partition for letter in block]
                assert sorted(flat) == sorted(items)
                assert len(partition) == classes

    def test_an_impossible_class_count_yields_nothing(self) -> None:
        assert list(partitions_of(("أ", "ب"), 3)) == []
        assert list(partitions_of(("أ", "ب"), 0)) == []


class TestTheCriterion:
    """المعيارُ يُفحَص في اتّجاهه وفي رفضه، لا في قيمته وحدها."""

    def test_more_classes_cost_more_freedom_on_identical_rows(self) -> None:
        profiles = {"أ": (10, 10, 10, 10), "ب": (10, 10, 10, 10)}
        joined = partition_criterion((("أ", "ب"),), profiles)
        split = partition_criterion((("أ",), ("ب",)), profiles)
        assert joined < split

    def test_rows_that_differ_pay_for_being_merged(self) -> None:
        profiles = {"أ": (100, 0, 0, 0), "ب": (0, 100, 0, 0)}
        joined = partition_criterion((("أ", "ب"),), profiles)
        split = partition_criterion((("أ",), ("ب",)), profiles)
        assert split < joined

    def test_a_repeated_letter_is_refused(self) -> None:
        profiles = {"أ": (1, 1, 1, 1)}
        with pytest.raises(LetterHarakaPartitionError):
            partition_criterion((("أ",), ("أ",)), profiles)

    def test_an_empty_mass_is_refused(self) -> None:
        profiles = {"أ": (0, 0, 0, 0)}
        with pytest.raises(LetterHarakaPartitionError):
            partition_criterion((("أ",),), profiles)


class TestGreedyAgainstOptimal:
    """الجشعُ يُحاكَم بالشرط المُودَع، لا بمعدّل إصابته."""

    def test_the_condition_is_written_before_the_reading_is_named(self) -> None:
        assert "صفرًا" in THE_PREREGISTERED_GREEDY_CONDITION
        assert "كلّ" in THE_PREREGISTERED_GREEDY_CONDITION
        assert "بِل" in THE_PREREGISTERED_GREEDY_CONDITION

    def test_the_probes_are_four_and_each_is_within_the_alphabet(self) -> None:
        probes = the_declared_probes()
        assert len(probes) == 4
        for probe in probes:
            assert set(probe.letters) <= set(THE_DECLARED_LETTERS)
            assert probe.class_counts == (2, 3, 4, 5)
        assert "أربعةُ مساباتٍ" in THE_DECLARED_PROBES

    def test_a_probe_with_a_foreign_letter_is_refused(self) -> None:
        with pytest.raises(LetterHarakaPartitionError):
            PartitionProbe("مسبارٌ فاسد", ("ب", "ء"), (2,))

    def test_a_probe_that_repeats_a_letter_is_refused(self) -> None:
        with pytest.raises(LetterHarakaPartitionError):
            PartitionProbe("مسبارٌ مكرَّر", ("ب", "ب"), (2,))

    def test_a_class_count_that_cannot_be_probed_is_refused(self) -> None:
        with pytest.raises(LetterHarakaPartitionError):
            PartitionProbe("مسبارٌ مستحيل", ("ب", "ت", "ث"), (3,))

    def test_greedy_covers_its_letters_and_hits_the_asked_class_count(self) -> None:
        letters = the_declared_probes()[0].letters
        blocks = greedy_partition(letters, 3)
        assert len(blocks) == 3
        assert sorted(letter for block in blocks for letter in block) == sorted(letters)

    def test_greedy_refuses_a_class_count_outside_its_letters(self) -> None:
        with pytest.raises(LetterHarakaPartitionError):
            greedy_partition(("ب", "ت"), 5)

    def test_the_optimum_is_never_beaten_by_any_enumerated_partition(self) -> None:
        profiles = letter_profiles()
        letters = the_declared_probes()[1].letters[:6]
        best, reading = optimal_partition(letters, 3, profiles)
        assert len(best) == 3
        for partition in partitions_of(letters, 3):
            assert partition_criterion(partition, profiles) >= reading - 1e-9

    def test_the_gap_is_measured_on_every_declared_cell(self) -> None:
        readings = measure_greedy_gap()
        assert len(readings) == 16
        assert all(reading.gap >= 0.0 for reading in readings)

    def test_greedy_falls_short_and_the_standing_says_so(self) -> None:
        readings = measure_greedy_gap()
        missed = [reading for reading in readings if not reading.reached]
        assert missed, "لو بلغ الجشعُ في كلّ خليّةٍ لوجب تغييرُ النصّ لا الشرط."
        assert greedy_standing(readings) is GreedyStanding.FALLS_SHORT

    def test_a_single_miss_is_enough_to_fell_the_claim(self) -> None:
        reached = ProbeReading(
            probe="مصنوع", classes=2, greedy_criterion=10.0, optimal_criterion=10.0
        )
        missed = ProbeReading(
            probe="مصنوع", classes=3, greedy_criterion=11.0, optimal_criterion=10.0
        )
        assert greedy_standing((reached,)) is GreedyStanding.REACHES_THE_OPTIMUM
        assert greedy_standing((reached, missed)) is GreedyStanding.FALLS_SHORT

    def test_a_greedy_below_the_optimum_is_refused_as_impossible(self) -> None:
        with pytest.raises(LetterHarakaPartitionError):
            ProbeReading(
                probe="مصنوع", classes=2, greedy_criterion=1.0, optimal_criterion=5.0
            )

    def test_an_empty_reading_set_yields_no_standing(self) -> None:
        with pytest.raises(LetterHarakaPartitionError):
            greedy_standing(())

    def test_the_gap_can_be_zero_so_the_statistic_is_not_always_positive(self) -> None:
        readings = measure_greedy_gap()
        assert any(reading.reached for reading in readings)


class TestTheInertness:
    """الوحدةُ لا تحرّك البوّابةَ، وتُقارَن بعد القياس بقراءتها عند الاستيراد."""

    def test_the_corpus_gate_does_not_move_after_every_measurement(self) -> None:
        measure_greedy_gap()
        table_census(SourceRung.WITH_PROSE)
        assert the_block_and_the_freeze_are_untouched() is True

    def test_the_named_residuals_are_six_and_each_carries_its_own_name(self) -> None:
        assert len(LETTER_HARAKA_PARTITION_NAMED_RESIDUALS) == 6
        for name, text in LETTER_HARAKA_PARTITION_NAMED_RESIDUALS.items():
            assert text.startswith(f"{name}: ")

    def test_every_residual_constant_is_registered(self) -> None:
        registered = set(LETTER_HARAKA_PARTITION_NAMED_RESIDUALS.values())
        assert THE_HUNDRED_AND_TWELVE_IS_A_DECLARATION_NOT_A_DISCOVERY in registered
        assert AN_EMPTY_CELL_UNDER_A_SPARSE_MARGIN_IS_NOT_A_PROHIBITION in registered
        assert A_BELL_NUMBER_IS_A_COUNT_OF_THE_SPACE_NOT_A_SEARCH_OF_IT in registered
        assert A_GREEDY_MERGE_THAT_USUALLY_WINS_IS_NOT_AN_OPTIMISER in registered
        assert A_MODULE_THAT_MEASURES_THE_TREE_LEAVES_ITSELF_OUT in registered
        assert NO_MEASUREMENT_HERE_LIFTS_A_BLOCK_OR_THAWS_A_FREEZE in registered

    def test_the_module_is_not_part_of_the_material_it_measures(self) -> None:
        assert "A_MODULE_THAT_MEASURES_THE_TREE_LEAVES_ITSELF_OUT" not in rung_text(
            SourceRung.WITH_PROSE
        )
