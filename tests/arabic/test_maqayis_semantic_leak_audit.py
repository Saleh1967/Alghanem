"""اختباراتُ تدقيق تسرُّب أسماء الحروف على خريطة ابن فارس.

الأرقامُ مُعادةُ الاشتقاق من البايتات المُبصَّمة؛ والمِقبَضُ المخفَّض ههنا
(`_TEST_PROFILE`) مُصرَّحٌ به، ولا يُقرَأ منه رقمُ الجولة الكاملة بل اتّجاهُها.
"""

from __future__ import annotations

import random

import pytest

from alghanem.arabic.maqayis_semantic_leak_audit import (
    MAQAYIS_LEAK_AUDIT_NAMED_RESIDUALS,
    MINIMUM_BODY_LENGTH,
    THE_LETTER_NAME_STEMS,
    FamilyResult,
    LeakVocabulary,
    MaqayisLeakAuditError,
    MeasurementProfile,
    PairFamily,
    PredictionStanding,
    PreregistrationStanding,
    RegisteredPrediction,
    RootDocument,
    assess_prediction,
    assess_preregistration,
    build_domain,
    build_space,
    enumerate_family,
    leak_vocabulary,
    matched_excess,
    measure_family,
    tokenize,
)

_TEST_PROFILE = MeasurementProfile(sample_cap=900, replicates=8)


def _families(roots: tuple[str, ...]) -> dict[PairFamily, tuple[tuple[int, int], ...]]:
    return {
        family: enumerate_family(
            roots, family, random.Random(_TEST_PROFILE.seed), _TEST_PROFILE.sample_cap
        )
        for family in PairFamily
    }


def _results(kind: LeakVocabulary) -> dict[PairFamily, FamilyResult]:
    documents = build_domain()
    roots = tuple(document.root for document in documents)
    space = build_space(documents, leak_vocabulary(kind))
    return {
        family: measure_family(space, pairs, family, _TEST_PROFILE)
        for family, pairs in _families(roots).items()
    }


# --- البروتوكولُ والمجال ----------------------------------------------------------


def test_the_domain_obeys_its_declared_rule() -> None:
    """كلُّ مستندٍ ثلاثيٌّ متمايزُ الحروف، وشرحُه فوقَ الحدّ، والجذورُ لا تتكرّر."""

    documents = build_domain()
    assert len(documents) > 2000
    roots = [document.root for document in documents]
    assert len(roots) == len(set(roots))
    for document in documents:
        assert len(document.root) == 3
        assert len(set(document.root)) == 3
        assert document.tokens


def test_a_repeated_letter_root_is_refused() -> None:
    """جذرٌ فيه حرفان متماثلان لا يُعرَّف عليه اتّفاقُ المواضع، فيُرفَض."""

    with pytest.raises(MaqayisLeakAuditError):
        RootDocument(root="ددل", tokens=("شيء",))


def test_the_tokenizer_drops_diacritics_and_single_letters() -> None:
    """التقطيعُ يحذف الشكلَ ويُسقِط الأحاديَّ، بالقاعدة المُعلَنة لا بغيرها."""

    assert tokenize("أَبَتَ يومنا") == ("أبت", "يومنا")
    assert tokenize("و ا ب") == ()


def test_the_minimum_body_length_is_a_declared_knob() -> None:
    """الحدُّ مُعلَنٌ قبل الرقم، فيُقرَأ من المفردة لا من نصٍّ في وثيقة."""

    assert MINIMUM_BODY_LENGTH == 200


# --- التسرُّبُ نفسُه ----------------------------------------------------------------


def test_the_opening_formula_names_the_root_letters() -> None:
    """التسرُّبُ قائمٌ في البايتات: الشرحُ يفتتح بتسمية حروف جذره."""

    documents = {document.root: document for document in build_domain()}
    opening = documents["أبد"].tokens[:3]
    assert opening == ("الهمزة", "والباء", "والدال")


def test_the_mechanical_vocabulary_strictly_contains_the_conservative_one() -> None:
    """القائمةُ الموسَّعةُ تحوي المحافِظةَ، فالمقابلةُ بينهما تضييقٌ لا تبديل."""

    mechanical = leak_vocabulary(LeakVocabulary.MECHANICAL)
    conservative = leak_vocabulary(LeakVocabulary.CONSERVATIVE)
    assert conservative < mechanical
    assert leak_vocabulary(LeakVocabulary.NONE) == frozenset()
    assert len(THE_LETTER_NAME_STEMS) == 31


def test_the_mechanical_vocabulary_catches_words_that_are_not_letter_names() -> None:
    """إفراطُ الإزالة الآليّة مقيسٌ لا مستور: «كلام» و«وراء» فيها."""

    mechanical = leak_vocabulary(LeakVocabulary.MECHANICAL)
    assert {"كلام", "وراء", "لحاء"} <= mechanical
    assert not {"كلام", "وراء", "لحاء"} & leak_vocabulary(LeakVocabulary.CONSERVATIVE)


def test_cleaning_halves_the_measured_effect() -> None:
    """الأثرُ قبل التنظيف ضِعفُ ما بعده تقريبًا؛ فنصفُه كان اسمَ حرف."""

    dirty = _results(LeakVocabulary.NONE)
    clean = _results(LeakVocabulary.MECHANICAL)
    for family in (
        PairFamily.SHARED_C2C3,
        PairFamily.SHARED_C1_ONLY,
        PairFamily.PERMUTATION_AGREE_ZERO,
        PairFamily.PERMUTATION_AGREE_ONE,
    ):
        assert dirty[family].ratio > clean[family].ratio
    dirty_excess = dirty[PairFamily.SHARED_C2C3].ratio - 1.0
    clean_excess = clean[PairFamily.SHARED_C2C3].ratio - 1.0
    assert clean_excess < dirty_excess * 0.6


def test_the_verdicts_do_not_flip_when_the_removal_list_narrows() -> None:
    """ثباتُ الحكم تحت تضييق الأداة نتيجة؛ ولو انقلب لَبطَل الاستنتاج."""

    mechanical = _results(LeakVocabulary.MECHANICAL)
    conservative = _results(LeakVocabulary.CONSERVATIVE)
    for prediction in RegisteredPrediction:
        assert assess_prediction(prediction, mechanical) is assess_prediction(
            prediction, conservative
        )


# --- الأفواج ---------------------------------------------------------------------


def test_every_family_is_non_empty_and_obeys_its_definition() -> None:
    """كلُّ فوجٍ قائمٌ، وأزواجُه تستوفي تعريفَه؛ ولا فوجَ يُقاس بلا فحصِ حدّه."""

    roots = tuple(document.root for document in build_domain())
    families = _families(roots)
    for family, pairs in families.items():
        assert pairs, family
        for left, right in pairs:
            first, second = roots[left], roots[right]
            agreement = sum(a == b for a, b in zip(first, second))
            if family is PairFamily.SHARED_C2C3:
                assert first[1:] == second[1:] and first[0] != second[0]
            elif family is PairFamily.SHARED_C1C2:
                assert first[:2] == second[:2] and first[2] != second[2]
            elif family is PairFamily.SHARED_C1_ONLY:
                assert first[0] == second[0] and agreement == 1
            elif family is PairFamily.PERMUTATION_AGREE_ZERO:
                assert sorted(first) == sorted(second) and agreement == 0
            elif family is PairFamily.NON_PERMUTATION_AGREE_ONE:
                assert sorted(first) != sorted(second) and agreement == 1


def test_the_permutation_families_are_small_and_the_controls_are_capped() -> None:
    """أفواجُ التقليب صغيرةٌ بطبيعتها، وضوابطُها مُعايَنةٌ عند السقف."""

    roots = tuple(document.root for document in build_domain())
    families = _families(roots)
    assert len(families[PairFamily.PERMUTATION_AGREE_ZERO]) < 2000
    assert (
        len(families[PairFamily.NON_PERMUTATION_AGREE_ZERO]) == _TEST_PROFILE.sample_cap
    )


def test_a_zero_cap_is_refused() -> None:
    """سقفُ معاينةٍ دون الواحد لا يُنتج فوجًا، فيُرفَض ولا يُقرَأ خاليًا."""

    roots = tuple(document.root for document in build_domain())
    with pytest.raises(MaqayisLeakAuditError):
        enumerate_family(roots, PairFamily.SHARED_C2C3, random.Random(1), 0)


# --- النتائجُ والأحكام -------------------------------------------------------------


def test_a_single_replicate_null_is_refused() -> None:
    """عدمٌ بإعادةٍ واحدةٍ لا انحرافَ له، فلا يُشتَقّ منه `Z`."""

    with pytest.raises(MaqayisLeakAuditError):
        MeasurementProfile(replicates=1)
    with pytest.raises(MaqayisLeakAuditError):
        FamilyResult(
            family=PairFamily.SHARED_C2C3,
            pair_count=10,
            observed_mean=0.02,
            null_means=(0.01,),
        )


def test_a_zero_spread_null_refuses_a_z_score() -> None:
    """انحرافُ عدمٍ صفرٌ يُرفَع به خطأٌ، ولا يُقرَأ `Z` لانهاية."""

    result = FamilyResult(
        family=PairFamily.SHARED_C2C3,
        pair_count=10,
        observed_mean=0.02,
        null_means=(0.01, 0.01, 0.01),
    )
    assert result.ratio == pytest.approx(2.0)
    with pytest.raises(MaqayisLeakAuditError):
        _ = result.z_score


def test_the_minor_derivation_holds_on_the_cleaned_space() -> None:
    """`S1` صمد بعد التنظيف: نسبةُ `C2C3` فوقَ العتبة و`Z` فوقَ ثلاثة."""

    results = _results(LeakVocabulary.MECHANICAL)
    c2c3 = results[PairFamily.SHARED_C2C3]
    assert c2c3.ratio >= 1.20
    assert c2c3.z_score > 3.0
    assert (
        assess_prediction(RegisteredPrediction.S1_MINOR_DERIVATION, results)
        is PredictionStanding.HELD
    )


def test_the_positional_order_is_refuted_in_the_observed_direction() -> None:
    """`S2` مُكذَّب، والمرصودُ `C1C2 > C1C3 > C2C3` لا ما تنبّأ به."""

    results = _results(LeakVocabulary.MECHANICAL)
    first = results[PairFamily.SHARED_C1C2].ratio
    middle = results[PairFamily.SHARED_C1C3].ratio
    last = results[PairFamily.SHARED_C2C3].ratio
    assert first > middle > last
    assert (
        assess_prediction(RegisteredPrediction.S2_POSITIONAL_ORDER, results)
        is PredictionStanding.REFUTED
    )


def test_the_major_derivation_splits_between_its_two_halves() -> None:
    """`S3` انقسم: يجتاز عند اتّفاق موضعٍ، ويسقط عند اتّفاق صفر."""

    results = _results(LeakVocabulary.MECHANICAL)
    assert results[PairFamily.PERMUTATION_AGREE_ONE].ratio >= 1.20
    assert results[PairFamily.PERMUTATION_AGREE_ZERO].ratio < 1.20
    assert (
        assess_prediction(RegisteredPrediction.S3_MAJOR_DERIVATION, results)
        is PredictionStanding.SPLIT
    )


def test_the_fourth_prediction_is_ill_posed_not_merely_false() -> None:
    """`S4` قابل فئتين غيرَ متكافئتين، فهو غيرُ قابلٍ للاختبار لا مُكذَّبٌ فحسب."""

    results = _results(LeakVocabulary.MECHANICAL)
    assert (
        assess_prediction(
            RegisteredPrediction.S4_PERMUTATION_EXCEEDS_POSITIONAL, results
        )
        is PredictionStanding.ILL_POSED_SO_NOT_TESTABLE
    )


def test_the_matched_excess_is_positive_and_consistent_across_both_cases() -> None:
    """الاختبارُ العادل: فائضُ التقليب موجبٌ ومتقاربٌ عند صفرِ موضعٍ وعند واحد."""

    results = _results(LeakVocabulary.MECHANICAL)
    zero = matched_excess(
        results[PairFamily.PERMUTATION_AGREE_ZERO],
        results[PairFamily.NON_PERMUTATION_AGREE_ZERO],
    )
    one = matched_excess(
        results[PairFamily.PERMUTATION_AGREE_ONE],
        results[PairFamily.NON_PERMUTATION_AGREE_ONE],
    )
    assert zero > 0.0
    assert one > 0.0
    assert abs(zero - one) < 0.15


def test_the_unmatched_control_falls_below_its_null() -> None:
    """ضابطُ غيرِ التقليب باتّفاق صفرٍ دون عدمه؛ فالمقياسُ يُنتج سالبًا أيضًا."""

    results = _results(LeakVocabulary.MECHANICAL)
    assert results[PairFamily.NON_PERMUTATION_AGREE_ZERO].ratio < 1.0


# --- التسجيلُ القبليُّ والبقايا -----------------------------------------------------


def test_the_named_preregistration_is_not_deposited_so_every_verdict_is_posterior() -> (
    None
):
    """`PREREG-6.md` مُسمًّى لا مُودَع، فالأحكامُ بَعديّةٌ ولو طابقت أرقامُها."""

    assert (
        assess_preregistration()
        is PreregistrationStanding.POSTERIOR_FOR_WANT_OF_A_DEPOSITED_DOCUMENT
    )


def test_every_named_residual_carries_its_own_key() -> None:
    """كلُّ بقيّةٍ تبدأ باسمها، فلا يُنقَل نصٌّ عن مفتاحٍ آخر."""

    assert len(MAQAYIS_LEAK_AUDIT_NAMED_RESIDUALS) == 10
    for key, text in MAQAYIS_LEAK_AUDIT_NAMED_RESIDUALS.items():
        assert text.startswith(f"{key}: ")
