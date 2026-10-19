"""اختباراتُ تجميدِ سبرِ اللزوم والتعدّي قبل قياسه.

وهي تفحص ما تفحصه وحدةُ تجميدٍ لا وحدةُ قياس: خلوَّها من حقل نتيجة، وثباتَ
بصمة محتواها، وحملَ كلّ رقمٍ وارِدٍ قاعدةَ عدّه، وأنّ حدَّ `p` ليس صفرًا.
"""

from __future__ import annotations

import pytest

from alghanem.arabic.transitivity_probe_preregistration import (
    ARRIVING_FIGURES,
    PERMUTATION_PROTOCOL,
    PRE_REGISTERED_EXPECTATION,
    PROBE_PREREGISTRATION_DIGEST,
    TRANSITIVITY_PROBE_NAMED_RESIDUALS,
    UNTAGGED_CATEGORIES,
    ArrivingFigure,
    PermutationProtocol,
    TransitivityClass,
    TransitivityCountingRule,
    TransitivityPreregistrationError,
    preregistration_digest,
)


def test_the_digest_rederives_from_the_registration_content() -> None:
    assert preregistration_digest() == PROBE_PREREGISTRATION_DIGEST


def test_the_permutation_p_value_has_a_floor_above_zero() -> None:
    assert PERMUTATION_PROTOCOL.p_value_floor == 1 / 5001
    assert PERMUTATION_PROTOCOL.p_value_floor > 0


def test_a_protocol_without_permutations_is_refused() -> None:
    with pytest.raises(TransitivityPreregistrationError):
        PermutationProtocol(
            statistic="فارقُ النسبتين",
            permutations=0,
            seed=1,
            generator="random.Random",
            p_value_formula="(1 + المتجاوزات) / (1 + التباديل)",
            p_value_floor_numerator=1,
        )


def test_every_arriving_figure_carries_its_counting_rule() -> None:
    assert ARRIVING_FIGURES
    for figure in ARRIVING_FIGURES:
        assert isinstance(figure.counting_rule, TransitivityCountingRule)
        assert figure.claimed_value.strip()


def test_a_figure_without_a_counting_rule_is_refused() -> None:
    with pytest.raises(TransitivityPreregistrationError):
        ArrivingFigure(
            label="رقمٌ بلا قاعدة",
            claimed_value="1",
            counting_rule="TAGGED_ROOTS",  # type: ignore[arg-type]
        )


def test_the_untagged_categories_name_why_their_nearest_tag_is_not_them() -> None:
    names = {category.arabic_name for category in UNTAGGED_CATEGORIES}
    assert {"المصدر", "اسمُ المكان الصرفيّ", "اسمُ الزمان الصرفيّ"} <= names
    for category in UNTAGGED_CATEGORIES:
        assert category.why_the_nearest_tag_is_not_it.strip()


def test_the_two_classes_are_named_by_corpus_evidence_not_by_grammar() -> None:
    assert "مرشَّح" in TransitivityClass.INTRANSITIVE_CANDIDATE.value
    assert "هذه المدوَّنة" in TransitivityClass.CONFIRMED_TRANSITIVE.value


def test_the_expectation_and_the_residuals_are_present_before_any_number() -> None:
    assert "PreRegisteredExpectation" in PRE_REGISTERED_EXPECTATION
    assert "TheIndicatorAndItsTestShareAParent" in TRANSITIVITY_PROBE_NAMED_RESIDUALS
    assert "APermutationPHasAFloor" in TRANSITIVITY_PROBE_NAMED_RESIDUALS
