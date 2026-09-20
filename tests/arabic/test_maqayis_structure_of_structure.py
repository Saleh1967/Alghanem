"""تجاربُ معادلة بنيةِ البنية: تعييرُها، وصفريُّها، وإرجاؤها المُدقَّق."""

from __future__ import annotations

import math

import pytest

from alghanem.arabic.dal_alone_gloss import THE_PROFILE_AXES, ProfileAxis
from alghanem.arabic.maqayis_structure_of_structure import (
    MAQAYIS_STRUCTURE_OF_STRUCTURE_NAMED_RESIDUALS,
    THE_DECLARED_NULL_PROFILE,
    THE_DECLARED_PARENTHOOD_RULE,
    CoverLevel,
    FractalStanding,
    MaqayisStructureOfStructureError,
    NullProfile,
    ParenthoodStanding,
    assess_parenthood_recovery,
    binary_entropy,
    classify_cover_level,
    compare_excess_fields,
    exact_null_distribution,
    exact_null_reading,
    holm_rejections,
    miller_madow_mutual_information,
    normalised_structure,
    run_structure_of_structure,
    smallest_attainable_p,
    structure_from_counts,
)

_READING = run_structure_of_structure()

THE_DAL_CELL = "كتاب الدّال"


def test_the_structure_function_is_normalised_into_the_unit_interval() -> None:
    """دالّةُ البنية لا تجاوز الواحدَ، وتبلغه عند التطابق التامّ."""

    membership = [True, True, False, False]
    assert normalised_structure(membership, membership) == pytest.approx(1.0, abs=0.35)
    perfect = structure_from_counts(100, 50, 50, 50)
    assert perfect is not None
    assert perfect <= 1.0
    for reading in _READING.readings:
        assert reading.structure is not None
        assert reading.structure <= 1.0


def test_the_two_forms_of_the_structure_function_agree() -> None:
    """صورةُ المتتاليتين وصورةُ العدّ تُخرِجان القيمةَ نفسَها."""

    membership = [True] * 7 + [False] * 13
    indicator = [True, False] * 10
    hits = sum(1 for a, b in zip(membership, indicator, strict=True) if a and b)
    by_counts = structure_from_counts(20, 7, 10, hits)
    by_sequence = normalised_structure(membership, indicator)
    assert by_counts == pytest.approx(by_sequence)


def test_a_zero_ceiling_is_read_as_powerless_and_not_as_agreement() -> None:
    """سقفٌ صفرٌ يُخرِج لا شيءَ، ولا يُقرَأ انطباقًا تامًّا."""

    assert normalised_structure([True, True], [True, False]) is None
    assert normalised_structure([True, False], [True, True]) is None
    assert structure_from_counts(10, 10, 4, 4) is None
    assert binary_entropy(0.0) == 0.0
    assert binary_entropy(1.0) == 0.0
    assert binary_entropy(0.5) == pytest.approx(1.0)
    with pytest.raises(MaqayisStructureOfStructureError):
        binary_entropy(1.5)


def test_the_bias_correction_is_subtracted_and_may_go_negative() -> None:
    """تصحيحُ ميلر–مادو مطروحٌ فعلًا، فيخرج سالبًا حيث لا ارتباط."""

    independent = miller_madow_mutual_information(
        [True, False] * 20, [True, True, False, False] * 10
    )
    assert independent < 0.0
    assert independent == pytest.approx(-1 / (2 * 40 * math.log(2)), abs=1e-9)
    with pytest.raises(MaqayisStructureOfStructureError):
        miller_madow_mutual_information([True], [True, False])
    with pytest.raises(MaqayisStructureOfStructureError):
        miller_madow_mutual_information([], [])


def test_the_null_is_enumerated_exactly_and_sums_to_one() -> None:
    """التوزيعُ الصفريُّ تامٌّ: أوزانُه تجمع واحدًا، فليس عيّنةً منه."""

    distribution = exact_null_distribution(200, 40, 60)
    assert sum(weight for _, weight in distribution) == pytest.approx(1.0)
    assert len(distribution) == min(40, 60) - max(0, 40 + 60 - 200) + 1


def test_the_exact_null_reproduces_a_permutation_null() -> None:
    """الصفريُّ المُحصى يُطابِق صفريَّ التبديل، فالإحصاءُ ليس مقياسًا آخر."""

    import random

    total, size, positives = 60, 18, 25
    rows = [True] * size + [False] * (total - size)
    values = [True] * positives + [False] * (total - positives)
    rng = random.Random(7)
    drawn: list[float] = []
    for _ in range(4000):
        rng.shuffle(values)
        hits = sum(1 for a, b in zip(rows, values, strict=True) if a and b)
        sampled = structure_from_counts(total, size, positives, hits)
        assert sampled is not None
        drawn.append(sampled)
    observed = structure_from_counts(total, size, positives, 14)
    assert observed is not None
    _, exact = exact_null_reading(total, size, positives, observed)
    empirical = sum(1 for value in drawn if value >= observed) / len(drawn)
    assert exact == pytest.approx(empirical, abs=0.02)


def test_the_null_quantile_widens_for_the_smaller_cell() -> None:
    """السماحيّةُ مُشتَقّةٌ من العدّة: أوسعُ للخليّة الصغيرة وأضيقُ للكبيرة."""

    small, _ = exact_null_reading(4000, 20, 1800, 0.0)
    large, _ = exact_null_reading(4000, 700, 1800, 0.0)
    assert small is not None and large is not None
    assert small > large


def test_a_reading_that_cannot_reach_the_corrected_threshold_is_counted() -> None:
    """العجزُ البنيويُّ عن بلوغ العتبة معدودٌ، ولا يُطوى في اجتياز."""

    assert smallest_attainable_p(4576, 700, 1900) < _READING.corrected_threshold
    tiny = [r for r in _READING.readings if r.size <= 8]
    assert tiny
    assert any(r.is_unresolvable_at(_READING.corrected_threshold) for r in tiny)
    assert not any(
        r.is_unresolvable_at(_READING.corrected_threshold)
        for r in _READING.readings
        if r.size >= 100
    )
    assert _READING.unresolvable_readings == 17
    assert _READING.cells_with_no_resolvable_axis == ()


def test_holm_stops_at_the_first_failure() -> None:
    """هولم يقف عند أوّل إخفاق، فلا يُرفَض ما بعده ولو صغُرت قيمتُه."""

    assert holm_rejections([0.0001, 0.03, 0.04], alpha=0.05) == (True, False, False)
    assert holm_rejections([0.001, 0.04, 0.0001], alpha=0.05) == (True, True, True)
    assert holm_rejections([0.2, 0.0001], alpha=0.05) == (False, True)
    assert holm_rejections(()) == ()


def test_the_declared_null_profile_is_not_retuned() -> None:
    """صفةُ الصفريّ مُعلَنةٌ بقيمها، ولا تُقبَل صفةٌ لا تُخرِج حكمًا."""

    assert THE_DECLARED_NULL_PROFILE.alpha == 0.05
    assert THE_DECLARED_NULL_PROFILE.seed == 20260920
    with pytest.raises(MaqayisStructureOfStructureError):
        NullProfile(replicates=10, alpha=0.05, seed=1)
    with pytest.raises(MaqayisStructureOfStructureError):
        NullProfile(replicates=400, alpha=0.9, seed=1)


def test_the_cover_level_is_read_from_the_header_form_alone() -> None:
    """صورةُ الترويسة تُصنَّف بشكلها، ولا تنظر القاعدةُ إلى عمودٍ مقيس."""

    assert classify_cover_level("كتاب الدّال") is CoverLevel.BOOK_FORM
    assert classify_cover_level("باب الواو والثاءِ") is CoverLevel.SECTION_FORM
    assert classify_cover_level("   ") is CoverLevel.UNNAMED
    assert classify_cover_level("فصل") is CoverLevel.UNNAMED


def test_the_flat_cover_carries_both_levels_in_one_row() -> None:
    """التغطيةُ مسطّحةٌ فعلًا: صفٌّ يحمل صورةً واحدةً لا صورتين."""

    levels = {classify_cover_level(cell) for cell in _READING.cells}
    assert levels == {CoverLevel.BOOK_FORM, CoverLevel.SECTION_FORM}
    books = [
        c for c in _READING.cells if classify_cover_level(c) is CoverLevel.BOOK_FORM
    ]
    assert len(books) == 14
    assert len(_READING.cells) == 40


def test_the_parenthood_rule_is_refuted_by_counting_its_violations() -> None:
    """قاعدةُ استرداد الأبوّة مُعلَنةٌ ثمّ منقوضةٌ بعدّ مخالفاتها لا بالترجيح."""

    probe = assess_parenthood_recovery()
    assert probe.resets == 28
    assert probe.book_starts == 14
    assert probe.resets_off_a_header_boundary == 28
    assert probe.book_starts_without_a_reset == 14
    assert probe.violations == 54
    assert probe.standing is ParenthoodStanding.REFUTED
    assert not probe.recovers_a_second_depth
    assert "entry_num" in THE_DECLARED_PARENTHOOD_RULE


def test_the_equation_is_deferred_and_not_refuted() -> None:
    """بغير عمقٍ ثانٍ مُدقَّقٍ لا تُقرَأ المعادلةُ قائمةً ولا منقوضة."""

    assert _READING.standing is FractalStanding.DEFERRED_FOR_WANT_OF_A_SECOND_DEPTH
    assert (
        _READING.standing is not FractalStanding.THE_LAW_DIFFERS_ACROSS_THE_TWO_DEPTHS
    )
    assert len(FractalStanding) == 3


def test_a_recovered_depth_without_a_comparison_still_yields_no_verdict() -> None:
    """لو استُردَّ عمقٌ ثانٍ ولم تُقابَل حقولُه لَوقفت القراءةُ ولم تحكم."""

    recovered = assess_parenthood_recovery().__class__(
        resets=14,
        book_starts=14,
        resets_off_a_header_boundary=0,
        resets_not_on_a_book_header=0,
        book_starts_without_a_reset=0,
    )
    assert recovered.standing is ParenthoodStanding.RECOVERED
    reading = _READING.__class__(
        readings=_READING.readings,
        parenthood=recovered,
        profile=_READING.profile,
    )
    with pytest.raises(MaqayisStructureOfStructureError):
        _ = reading.standing


def test_the_field_comparison_separates_two_unlike_laws() -> None:
    """مقابلةُ الحقلين تُفرِّق بين قانونين مختلفين ولا تُفرِّق بين متشابهين."""

    alike_first = [0.01 * index for index in range(40)]
    alike_second = [0.01 * index + 0.0005 for index in range(40)]
    assert compare_excess_fields(alike_first, alike_second) > 0.05
    unlike = [value + 5.0 for value in alike_first]
    assert compare_excess_fields(alike_first, unlike) < 0.05
    with pytest.raises(MaqayisStructureOfStructureError):
        compare_excess_fields([0.1], [0.2, 0.3])


def test_every_cell_and_axis_is_read_and_none_is_dropped() -> None:
    """كلُّ خليّةٍ تُقرَأ على المحاور الخمسة، فلا عتبةَ عدّةٍ تُسقِط خليّة."""

    assert len(_READING.readings) == len(_READING.cells) * len(THE_PROFILE_AXES)
    assert len(_READING.readings) == 200
    assert _READING.powerless_readings == 0
    assert min(reading.size for reading in _READING.readings) < 30
    assert _READING.corrected_threshold == pytest.approx(0.05 / 200)


def test_the_dal_cell_is_read_and_holds_on_every_declared_axis() -> None:
    """بابُ الدال يُقرَأ على الخمسة، ولا يتمايز بعد التصحيح، ولا عجزَ فيه."""

    readings = [r for r in _READING.readings if r.cell_label == THE_DAL_CELL]
    assert len(readings) == 5
    assert all(not r.is_unresolvable_at(_READING.corrected_threshold) for r in readings)
    assert THE_DAL_CELL in _READING.self_similar_cells
    assert THE_DAL_CELL not in _READING.distinguished_cells
    poetry = next(r for r in readings if r.axis is ProfileAxis.SHARE_WITH_POETRY)
    assert poetry.excess is not None and poetry.excess > 0.0
    assert all(
        r.excess is not None and r.excess < 0.0
        for r in readings
        if r.axis is not ProfileAxis.SHARE_WITH_POETRY
    )


def test_the_uncorrected_reading_is_shown_beside_the_corrected_one() -> None:
    """يُعرَض العددان معًا، فلا يُكتَم أنّ حكمَ خلايا دالّةٌ في التصحيح."""

    assert len(_READING.cells_distinguished_before_correction) == 27
    assert len(_READING.distinguished_cells) == 12
    assert THE_DAL_CELL in _READING.cells_distinguished_before_correction
    assert set(_READING.distinguished_cells) <= set(
        _READING.cells_distinguished_before_correction
    )


def test_the_cells_split_into_two_named_halves_with_no_remainder() -> None:
    """المتمايزُ والمنطبقُ يستغرقان التغطيةَ، فلا خليّةَ بلا حكم."""

    assert set(_READING.distinguished_cells) | set(_READING.self_similar_cells) == set(
        _READING.cells
    )
    assert not set(_READING.distinguished_cells) & set(_READING.self_similar_cells)
    assert len(_READING.self_similar_cells) == 28
    assert len(_READING.excess_field) == 200


def test_an_unknown_axis_is_refused_rather_than_silently_missed() -> None:
    """محورٌ غيرُ مُعلَنٍ يُوقِف القياسَ ولا يمرّ صفرًا."""

    entry = next(iter(_READING.cells))
    assert isinstance(entry, str)
    with pytest.raises(MaqayisStructureOfStructureError):
        _READING.structure_of("بابٌ لا وجودَ له", ProfileAxis.SHARE_MUDAAF)
    assert (
        _READING.structure_of(THE_DAL_CELL, ProfileAxis.SHARE_WITH_POETRY) is not None
    )


def test_the_named_residuals_carry_their_own_keys() -> None:
    """كلُّ بقيّةٍ مُسمّاةٌ تبدأ باسمها، فلا تُقرَأ منزوعةً عن مفتاحها."""

    assert len(MAQAYIS_STRUCTURE_OF_STRUCTURE_NAMED_RESIDUALS) == 6
    for key, text in MAQAYIS_STRUCTURE_OF_STRUCTURE_NAMED_RESIDUALS.items():
        assert text.startswith(f"{key}: ")
