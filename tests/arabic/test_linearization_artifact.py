"""شواهدُ دعوى الخطّيّة: ما صدق فراغًا، وما انعقد بعكسٍ تامّ، وما انتقض."""

from __future__ import annotations

import unicodedata
from dataclasses import replace
from pathlib import Path

import pytest

from alghanem.arabic import linearization_artifact as module
from alghanem.arabic.carrier_state_observed_fiber import (
    ObservedFiberTable,
    run_observed_fiber_on_the_deposited_fatiha,
)
from alghanem.arabic.linearization_artifact import (
    LINEARIZATION_NAMED_RESIDUALS,
    THE_CLAIM,
    LinearityReading,
    LinearityVerdict,
    LinearityVerdictReading,
    LinearizationError,
    MarkOrderFreedom,
    OrderingCensus,
    RoundTripAudit,
    every_mark_follows_its_carrier_by_definition,
    measure_mark_order_freedom,
    measure_ordering_census,
    read_the_linearity_claim,
    round_trip_from_unordered_sets,
)
from alghanem.import_boundary import ImportBoundaryPolicy, audit_import_boundary


@pytest.fixture(scope="module")
def table() -> ObservedFiberTable:
    return run_observed_fiber_on_the_deposited_fatiha()


@pytest.fixture(scope="module")
def readings(table: ObservedFiberTable) -> tuple[LinearityVerdictReading, ...]:
    return read_the_linearity_claim(table)


def _reading(
    readings: tuple[LinearityVerdictReading, ...], which: LinearityReading
) -> LinearityVerdictReading:
    return next(item for item in readings if item.reading is which)


def test_the_claim_is_stated_before_it_is_divided() -> None:
    assert "تسطيحِ بُعدَين" in THE_CLAIM


def test_every_reading_is_read_and_none_is_dropped(
    readings: tuple[LinearityVerdictReading, ...],
) -> None:
    assert {item.reading for item in readings} == set(LinearityReading)


def test_all_four_verdict_kinds_are_used(
    readings: tuple[LinearityVerdictReading, ...],
) -> None:
    assert {item.verdict for item in readings} == set(LinearityVerdict)


# --- المئةُ بالمئة مبرهنةٌ لا مرصودة -----------------------------------------------


def test_every_mark_has_a_nonzero_combining_class() -> None:
    assert every_mark_follows_its_carrier_by_definition() is True


def test_the_hundred_percent_needs_no_corpus_at_all() -> None:
    from inspect import signature

    assert signature(every_mark_follows_its_carrier_by_definition).parameters == {}
    assert every_mark_follows_its_carrier_by_definition() is True


def test_the_hundred_percent_reading_is_held_but_carries_no_information(
    readings: tuple[LinearityVerdictReading, ...],
) -> None:
    item = _reading(readings, LinearityReading.THE_MARK_ALWAYS_FOLLOWS_ITS_CARRIER)
    assert item.verdict is LinearityVerdict.HELD_BUT_CARRIES_NO_INFORMATION


def test_the_hundred_percent_reading_names_its_emptiness(
    readings: tuple[LinearityVerdictReading, ...],
) -> None:
    item = _reading(readings, LinearityReading.THE_MARK_ALWAYS_FOLLOWS_ITS_CARRIER)
    assert any("لا يُشتَقّ منه خبر" in note for note in item.residuals)


# --- الترتيبُ لم يكن حرًّا ---------------------------------------------------------


def test_the_combining_classes_are_pairwise_distinct() -> None:
    assert measure_mark_order_freedom().classes_are_pairwise_distinct is True


def test_no_mark_multiset_admits_two_canonical_forms() -> None:
    freedom = measure_mark_order_freedom()
    assert freedom.multisets_examined > 0
    assert not freedom.order_was_ever_free


def test_every_examined_multiset_has_a_single_canonical_form() -> None:
    freedom = measure_mark_order_freedom()
    assert freedom.multisets_with_a_single_canonical_form == freedom.multisets_examined


def test_a_shadda_haraka_pair_normalizes_to_one_form() -> None:
    forms = {
        unicodedata.normalize("NFC", "\u0628" + pair)
        for pair in ("\u0651\u064e", "\u064e\u0651")
    }
    assert len(forms) == 1


def test_the_flattened_choice_reading_is_refuted(
    readings: tuple[LinearityVerdictReading, ...],
) -> None:
    item = _reading(readings, LinearityReading.THE_MARK_ORDER_IS_A_FLATTENED_CHOICE)
    assert item.verdict is LinearityVerdict.REFUTED


def test_the_verdict_is_hung_on_distinct_classes_not_on_mark_count(
    readings: tuple[LinearityVerdictReading, ...],
) -> None:
    item = _reading(readings, LinearityReading.THE_MARK_ORDER_IS_A_FLATTENED_CHOICE)
    assert any("لو تساوى صنفانِ" in note for note in item.residuals)


def test_a_freedom_proving_more_than_it_examined_is_refused() -> None:
    with pytest.raises(LinearizationError, match="مُحال"):
        MarkOrderFreedom(
            multisets_examined=3,
            multisets_with_a_single_canonical_form=4,
            distinct_combining_classes=6,
            marks_examined=6,
        )


# --- العكسُ التامّ ------------------------------------------------------------------


def test_every_word_is_rebuilt_from_unordered_mark_sets(
    table: ObservedFiberTable,
) -> None:
    audit = round_trip_from_unordered_sets(table)
    assert audit.words_examined > 0
    assert audit.is_lossless
    assert audit.mismatching_words == ()


def test_the_point_reading_is_held_by_exact_inversion(
    readings: tuple[LinearityVerdictReading, ...],
) -> None:
    item = _reading(readings, LinearityReading.CV_IS_A_POINT_NOT_AN_ORDERED_PAIR)
    assert item.verdict is LinearityVerdict.HELD_BY_EXACT_INVERSION


def test_the_inversion_needs_the_deferred_mark_to_stay_lossless(
    table: ObservedFiberTable,
) -> None:
    stripped = replace(
        table,
        rows=tuple(
            replace(row, deferred_axis_marks=(), unread_marks=()) for row in table.rows
        ),
    )
    audit = round_trip_from_unordered_sets(stripped)
    assert not audit.is_lossless
    assert audit.mismatching_words


def test_dropping_a_deferred_axis_is_a_loss_of_an_axis_not_of_order(
    readings: tuple[LinearityVerdictReading, ...],
) -> None:
    item = _reading(readings, LinearityReading.CV_IS_A_POINT_NOT_AN_ORDERED_PAIR)
    assert any("من طرحِ محورٍ لا من الترتيب" in note for note in item.residuals)


def test_the_carrier_sequence_itself_is_not_denied(
    readings: tuple[LinearityVerdictReading, ...],
) -> None:
    item = _reading(readings, LinearityReading.CV_IS_A_POINT_NOT_AN_ORDERED_PAIR)
    assert any("ترتيبُ الحوامل بينها" in note for note in item.residuals)


def test_an_audit_whose_mismatches_do_not_balance_is_refused() -> None:
    with pytest.raises(LinearizationError, match="لا يُطوى منه شيء"):
        RoundTripAudit(
            words_examined=5, words_reconstructed=3, mismatching_words=("كلمة",)
        )


def test_an_audit_rebuilding_more_than_examined_is_refused() -> None:
    with pytest.raises(LinearizationError, match="مُحال"):
        RoundTripAudit(words_examined=2, words_reconstructed=5, mismatching_words=())


def test_an_empty_table_cannot_be_inverted(table: ObservedFiberTable) -> None:
    with pytest.raises(LinearizationError, match="لا يُعكَس على خلاء"):
        round_trip_from_unordered_sets(replace(table, rows=()))


# --- الترتيباتُ المطويّة ------------------------------------------------------------


def test_the_collapsed_orderings_are_counted_in_bits(
    table: ObservedFiberTable,
) -> None:
    census = measure_ordering_census(table)
    assert census.carriers_bearing_more_than_one_mark > 0
    assert census.bits_of_apparent_freedom == pytest.approx(
        census.carriers_bearing_more_than_one_mark
    )


def test_single_mark_carriers_contribute_no_freedom(
    table: ObservedFiberTable,
) -> None:
    census = measure_ordering_census(table)
    assert census.carriers_bearing_marks > census.carriers_bearing_more_than_one_mark


def test_the_lost_dimension_reading_is_refuted(
    readings: tuple[LinearityVerdictReading, ...],
) -> None:
    item = _reading(readings, LinearityReading.THE_FLATTENING_LOSES_A_DIMENSION)
    assert item.verdict is LinearityVerdict.REFUTED


def test_the_removed_freedom_is_named_false_not_lost(
    readings: tuple[LinearityVerdictReading, ...],
) -> None:
    item = _reading(readings, LinearityReading.THE_FLATTENING_LOSES_A_DIMENSION)
    assert any("كاذبةٌ لا مفقودة" in note for note in item.residuals)


def test_a_census_with_fewer_than_one_ordering_is_refused() -> None:
    with pytest.raises(LinearizationError, match="لا ينزل عن واحد"):
        OrderingCensus(
            carriers_bearing_marks=2,
            carriers_bearing_more_than_one_mark=1,
            orderings_denoting_the_same_reading=0,
        )


def test_a_census_with_impossible_proportions_is_refused() -> None:
    with pytest.raises(LinearizationError, match="مقامٌ مُحال"):
        OrderingCensus(
            carriers_bearing_marks=1,
            carriers_bearing_more_than_one_mark=2,
            orderings_denoting_the_same_reading=2,
        )


# --- الاستقلالُ مُقيَّدًا ------------------------------------------------------------


def test_the_independence_claim_holds_only_in_a_narrower_sense(
    readings: tuple[LinearityVerdictReading, ...],
) -> None:
    item = _reading(readings, LinearityReading.THE_SECOND_AXIS_IS_INDEPENDENT)
    assert item.verdict is LinearityVerdict.HELD_ONLY_IN_A_NARROWER_SENSE


def test_the_shared_dependence_on_unicode_is_named(
    readings: tuple[LinearityVerdictReading, ...],
) -> None:
    item = _reading(readings, LinearityReading.THE_SECOND_AXIS_IS_INDEPENDENT)
    assert any("ليس استقلالَ النظام" in note for note in item.residuals)


def test_what_would_lift_the_shared_dependence_is_named(
    readings: tuple[LinearityVerdictReading, ...],
) -> None:
    item = _reading(readings, LinearityReading.THE_SECOND_AXIS_IS_INDEPENDENT)
    assert any("لا يمرّ بيونيكود" in note for note in item.residuals)


# --- الأحكامُ والبقايا -------------------------------------------------------------


def test_a_reading_without_a_written_reason_is_refused() -> None:
    with pytest.raises(LinearizationError, match="سببٍ مكتوب"):
        LinearityVerdictReading(
            reading=LinearityReading.THE_FLATTENING_LOSES_A_DIMENSION,
            verdict=LinearityVerdict.REFUTED,
            what_decided_it="  ",
            residuals=("بقيّة",),
        )


def test_a_reading_without_a_named_residual_is_refused() -> None:
    with pytest.raises(LinearizationError, match="بلا بقيّةٍ مُسمّاة"):
        LinearityVerdictReading(
            reading=LinearityReading.THE_FLATTENING_LOSES_A_DIMENSION,
            verdict=LinearityVerdict.REFUTED,
            what_decided_it="سبب",
            residuals=(),
        )


def test_a_zero_combining_class_would_halt_the_reading(
    table: ObservedFiberTable, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        module, "every_mark_follows_its_carrier_by_definition", lambda: False
    )
    with pytest.raises(LinearizationError, match="صنفُها التركيبيُّ صفر"):
        read_the_linearity_claim(table)


def test_the_named_residuals_are_all_present() -> None:
    assert len(LINEARIZATION_NAMED_RESIDUALS) == 5
    assert all(note.strip() for note in LINEARIZATION_NAMED_RESIDUALS)


def test_the_no_bits_residual_is_named() -> None:
    assert any(
        "AHundredPercentForcedByTheEncodingCarriesNoBits" in note
        for note in LINEARIZATION_NAMED_RESIDUALS
    )


def test_the_writing_only_ceiling_is_named() -> None:
    assert any(
        "AReadingHereIsAReadingOfWriting" in note
        for note in LINEARIZATION_NAMED_RESIDUALS
    )


def test_this_reading_reaches_no_kernel_module() -> None:
    source = Path(str(module.__file__))
    report = audit_import_boundary(
        (source,),
        ImportBoundaryPolicy(
            policy_id="linearization-artifact-reaches-no-kernel",
            permitted_modules=("alghanem.arabic",),
            forbidden_packages=("alghanem.kernel",),
        ),
    )
    assert not [
        name for name in report.reached_modules if name.startswith("alghanem.kernel")
    ]
