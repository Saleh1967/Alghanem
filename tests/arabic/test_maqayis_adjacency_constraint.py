"""تجاربُ قيد التجاور: إسقاطُ المضاعف، واختبارُ الفرق، وقاعُ الترتيب."""

from __future__ import annotations

import pytest

from alghanem.arabic.maqayis_adjacency_constraint import (
    ADJACENCY_CONSTRAINT_NAMED_RESIDUALS,
    THE_DECLARED_NULL_PROFILE,
    THE_DECLARED_PLACE_CLASSES,
    THE_LETTER_FOLD,
    AdjacencyConstraintReading,
    AdjacentPosition,
    AsymmetryStanding,
    MaqayisAdjacencyConstraintError,
    NullProfile,
    QafStanding,
    expected_same_place_rate,
    fold_letter,
    folded_roots,
    holm_rejections,
    place_of,
    run_adjacency_constraint,
    same_place_rate,
)

_READING = run_adjacency_constraint()


def test_the_declared_places_cover_the_alphabet_once() -> None:
    """المخارجُ الأحدَ عشرَ تستغرق الثمانيةَ والعشرين حرفًا بلا تكرار."""

    letters = [
        letter for letters in THE_DECLARED_PLACE_CLASSES.values() for letter in letters
    ]
    assert len(letters) == 28
    assert len(set(letters)) == 28
    assert len(THE_DECLARED_PLACE_CLASSES) == 11
    assert place_of("ق") == place_of("ك") == "لهويّ"
    assert place_of("ض") == "ضاديّ"


def test_the_fold_is_applied_before_any_reading() -> None:
    """صورُ الهمزة تُطوى إلى أصلٍ واحد، وما لا يُصنَّف يُرفَع لا يُبتلَع."""

    assert {fold_letter(letter) for letter in "أإآؤئا"} == {"ء"}
    assert place_of("أ") == place_of("ء") == "حلقٌ أقصى"
    assert fold_letter("ب") == "ب"
    assert "ا" in THE_LETTER_FOLD
    with pytest.raises(MaqayisAdjacencyConstraintError):
        place_of("x")
    with pytest.raises(MaqayisAdjacencyConstraintError):
        fold_letter("به")


def test_the_deposit_stores_geminates_with_the_doubling_written() -> None:
    """المضاعفُ مكتوبٌ مُظهَرَ التضعيف، فحرفاه الثاني والثالثُ حرفٌ واحد."""

    roots = folded_roots()
    assert len(roots) == 4562
    assert _READING.dropped_roots == 3
    geminates = [root for root in roots if root[1] == root[2]]
    assert len(geminates) == 449
    assert _READING.geminate_roots == 449
    tripled = [root for root in roots if root[0] == root[1] == root[2]]
    assert tripled == [("د", "د", "د")]


def test_the_statistic_drops_the_pair_of_one_letter() -> None:
    """زوجُ الحرف الواحد ساقطٌ افتراضًا، ومقروءٌ عند الطلب ليُرى أثرُه."""

    left = ["ب", "ق", "ق", "ف"]
    right = ["م", "ق", "ك", "س"]
    assert same_place_rate(left, right) == (2, 3)
    assert same_place_rate(left, right, drop_identical=False) == (3, 4)
    with pytest.raises(MaqayisAdjacencyConstraintError):
        same_place_rate(left, right[:2])
    with pytest.raises(MaqayisAdjacencyConstraintError):
        same_place_rate([], [])


def test_the_expected_rate_is_computed_from_the_margins_exactly() -> None:
    """المتوقَّعُ محسوبٌ من الهوامش، فلا بذرَ يدخل في ترتيب الحروف."""

    left = ["ب", "ق"] * 50
    right = ["م", "ك"] * 50
    assert expected_same_place_rate(left, right) == pytest.approx(0.5)
    assert expected_same_place_rate(left, right) == expected_same_place_rate(
        left, right
    )
    with pytest.raises(MaqayisAdjacencyConstraintError):
        expected_same_place_rate(left, right[:3])


def test_the_constraint_holds_at_both_positions() -> None:
    """القيدُ قائمٌ في الموضعين معًا بعد التصحيح، ونسبتُه دونَ نصف المتوقَّع."""

    first = _READING.first_pair
    second = _READING.second_pair
    assert first.position is AdjacentPosition.FIRST_PAIR
    assert second.position is AdjacentPosition.SECOND_PAIR
    assert (first.observed_same, first.observed_pairs) == (117, 4560)
    assert (second.observed_same, second.observed_pairs) == (127, 4113)
    assert first.depression_ratio < 0.4
    assert second.depression_ratio < 0.4
    assert first.z_score < -10.0
    assert second.z_score < -10.0
    assert _READING.constraint_holds_at_both_positions
    assert _READING.rejections[:2] == (True, True)


def test_the_claimed_positional_asymmetry_is_an_artefact_of_the_spelling() -> None:
    """الأسيميّةُ تقوم في الخامّ وتسقط عند إسقاط أزواج الحرف الواحد."""

    first = _READING.first_pair
    second = _READING.second_pair
    assert second.raw_rate > first.raw_rate * 4
    assert _READING.raw_asymmetry_would_be_claimed
    assert second.rate < first.rate * 1.5
    assert second.raw_same - second.observed_same == 449


def test_the_asymmetry_is_tested_directly_and_is_not_distinguished() -> None:
    """الفرقُ نفسُه مقيسٌ في وجه صفريٍّ واحد، فلا يُفرَّق بين الموضعين."""

    assert _READING.asymmetry_p_value > _READING.corrected_threshold
    assert not _READING.rejections[2]
    assert (
        _READING.asymmetry_standing
        is AsymmetryStanding.THE_TWO_POSITIONS_ARE_NOT_DISTINGUISHED
    )
    assert abs(_READING.asymmetry_observed - _READING.asymmetry_null_mean) < (
        2.0 * _READING.asymmetry_null_sd
    )
    assert len(AsymmetryStanding) == 3


def test_a_separated_field_would_still_be_read_as_an_asymmetry() -> None:
    """مسارُ الأسيميّة قائمٌ في الشفرة: فرقٌ مرفوضٌ يُخرِج حكمًا لا إرجاءً."""

    separated = AdjacencyConstraintReading(
        roots=_READING.roots,
        dropped_roots=_READING.dropped_roots,
        pairs=_READING.pairs,
        asymmetry_p_value=1e-6,
        asymmetry_observed=_READING.asymmetry_observed,
        asymmetry_null_mean=_READING.asymmetry_null_mean,
        asymmetry_null_sd=_READING.asymmetry_null_sd,
        depressions=_READING.depressions,
        profile=_READING.profile,
    )
    assert (
        separated.asymmetry_standing
        is AsymmetryStanding.THE_FIRST_PAIR_IS_MORE_CONSTRAINED
    )


def test_the_null_can_reach_the_corrected_threshold() -> None:
    """أرضيّةُ دقّة الصفريّ دونَ العتبة المُصحَّحة، فليس الاختبارُ ميّتًا."""

    assert THE_DECLARED_NULL_PROFILE.replicates == 2000
    assert THE_DECLARED_NULL_PROFILE.smallest_attainable_p == pytest.approx(1 / 2001)
    assert _READING.corrected_threshold == pytest.approx(0.05 / 3)
    assert _READING.the_null_can_reach_the_threshold
    assert THE_DECLARED_NULL_PROFILE.smallest_attainable_p < 0.0167
    with pytest.raises(MaqayisAdjacencyConstraintError):
        NullProfile(replicates=100, alpha=0.05, seed=1)
    with pytest.raises(MaqayisAdjacencyConstraintError):
        NullProfile(replicates=2000, alpha=0.8, seed=1)


def test_holm_stops_at_the_first_failure() -> None:
    """هولم يقف عند أوّل إخفاق، فلا يُرفَض ما بعده مهما صغُرت قيمتُه."""

    assert holm_rejections([0.0001, 0.03, 0.04], alpha=0.05) == (True, False, False)
    assert holm_rejections([0.0005, 0.0005, 0.71], alpha=0.05) == (True, True, False)
    assert holm_rejections(()) == ()


def test_qaf_is_tied_at_the_floor_and_not_singled_out() -> None:
    """القافُ في القاع مع أربعةَ عشرَ غيرَها، فلا خصوصيّةَ لها ههنا."""

    assert _READING.qaf_standing is QafStanding.TIED_AT_THE_FLOOR
    floor = _READING.letters_at_the_floor
    assert "ق" in floor
    assert len(floor) == 15
    qaf = _READING.depression_of("ق")
    assert qaf.observed == 0
    assert qaf.neighbours == 360
    assert qaf.expected > 5.0
    assert qaf.ratio == 0.0
    assert len(QafStanding) == 3


def test_the_letter_table_is_ordered_and_complete() -> None:
    """الترتيبُ من القاع صاعدًا، والحروفُ كلُّها مقروءةٌ بلا إسقاطٍ صامت."""

    ratios = [row.ratio for row in _READING.depressions]
    assert ratios == sorted(ratios)
    assert len(_READING.depressions) == 27
    assert _READING.depressions[-1].letter in {"ش", "ج"}
    assert _READING.depressions[-1].ratio > 1.0
    with pytest.raises(MaqayisAdjacencyConstraintError):
        _READING.depression_of("x")


def test_the_glides_carry_the_surviving_violations() -> None:
    """ما ينجو من القيد جُلُّه أزواجٌ طرفُها واوٌ أو ياء، وذلك مُسمًّى."""

    surviving = [
        root
        for root in _READING.roots
        if root[0] != root[1] and place_of(root[0]) == place_of(root[1])
    ]
    assert len(surviving) == 117
    with_glides = [root for root in surviving if "و" in root[:2] or "ي" in root[:2]]
    assert len(with_glides) * 2 > len(surviving)
    assert _READING.depression_of("و").ratio > 0.5
    assert _READING.depression_of("ي").ratio > 0.5


def test_a_different_seed_does_not_move_any_standing() -> None:
    """تبديلُ البذر يُزحزح الأرقامَ ولا يُزحزح حكمًا، فليست الأحكامُ دالّةً فيه."""

    other = run_adjacency_constraint(
        NullProfile(replicates=1000, alpha=0.05, seed=7654321)
    )
    assert other.constraint_holds_at_both_positions
    assert other.asymmetry_standing is _READING.asymmetry_standing
    assert other.qaf_standing is _READING.qaf_standing
    assert other.letters_at_the_floor == _READING.letters_at_the_floor
    assert other.first_pair.rate == _READING.first_pair.rate
    assert other.first_pair.null_mean == pytest.approx(
        _READING.first_pair.null_mean, abs=0.005
    )


def test_the_named_residuals_carry_their_own_keys() -> None:
    """كلُّ بقيّةٍ مُسمّاةٌ تبدأ باسمها، فلا تُقرَأ منزوعةً عن مفتاحها."""

    assert len(ADJACENCY_CONSTRAINT_NAMED_RESIDUALS) == 6
    for key, text in ADJACENCY_CONSTRAINT_NAMED_RESIDUALS.items():
        assert text.startswith(f"{key}: ")
