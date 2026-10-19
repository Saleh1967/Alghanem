"""اختبارُ تجميدِ نصّ الفرضية وتسجيلِ بنودها العشرة قبل أيّ قراءة."""

from __future__ import annotations

import pytest

from alghanem.arabic.fractal_transition_hypothesis import (
    COMPARED_FIELDS,
    EXCLUDED_FIELDS,
    FORBIDDEN_VERDICT_NAME,
    HYPOTHESIS_DIGEST,
    HYPOTHESIS_TEXT,
    REQUIRED_NOTATION_SITES,
    FractalTransitionHypothesisError,
    FractalVerdict,
    hypothesis_digest,
    require_compared_field,
)
from alghanem.arabic.fractal_transition_preregistration import (
    DECLARED_LAYERS,
    DECLARED_PAIRS,
    FROZEN_CASES,
    MATCH_CRITERION,
    PREREGISTRATION_DIGEST,
    FieldDeclaration,
    FractalTransitionPreregistrationError,
    LayerStanding,
    layer_named,
    pair_named,
    preregistration_digest,
)


def test_the_frozen_text_keeps_its_mathematical_notation() -> None:
    for site in REQUIRED_NOTATION_SITES:
        assert site in HYPOTHESIS_TEXT


def test_the_digest_is_rederived_not_declared() -> None:
    assert hypothesis_digest() == HYPOTHESIS_DIGEST
    assert len(HYPOTHESIS_DIGEST) == 64


def test_one_changed_character_changes_the_digest() -> None:
    assert (
        hypothesis_digest(HYPOTHESIS_TEXT.replace(r"\cong", "=")) != HYPOTHESIS_DIGEST
    )


def test_the_verdict_vocabulary_is_the_four_declared_ones() -> None:
    assert {member.value for member in FractalVerdict} == {
        "SUPPORTED",
        "REFUTED",
        "UNDERPOWERED",
        "WEAKER_MODEL_RECONSTRUCTS",
    }
    assert FORBIDDEN_VERDICT_NAME not in {member.name for member in FractalVerdict}


def test_an_excluded_field_may_not_enter_the_match_criterion() -> None:
    for field in EXCLUDED_FIELDS:
        with pytest.raises(FractalTransitionHypothesisError):
            require_compared_field(field)
    for field in COMPARED_FIELDS:
        assert require_compared_field(field) == field


def test_a_field_outside_the_six_is_refused() -> None:
    with pytest.raises(FractalTransitionHypothesisError):
        require_compared_field("Operation")


def test_the_preregistration_digest_is_rederived_not_declared() -> None:
    assert preregistration_digest() == PREREGISTRATION_DIGEST
    assert len(PREREGISTRATION_DIGEST) == 64


def test_every_layer_declares_the_six_fields_with_a_falsifier() -> None:
    for layer in DECLARED_LAYERS:
        assert tuple(item.field for item in layer.fields) == COMPARED_FIELDS
        for item in layer.fields:
            assert item.what_would_fail_it.strip()
            assert item.read_from.strip()


def test_a_field_without_a_falsifier_is_refused_at_construction() -> None:
    with pytest.raises(FractalTransitionPreregistrationError):
        FieldDeclaration(
            field="Gate",
            read_from="موضعٌ ما",
            statement="بيانٌ ما",
            what_would_fail_it="   ",
        )


def test_no_declared_pair_is_a_holdout_under_the_frozen_ladder() -> None:
    for layer in DECLARED_LAYERS:
        assert layer.is_named_in_the_frozen_ladder
    for pair in DECLARED_PAIRS:
        lower = layer_named(pair.lower_jurisdiction)
        upper = layer_named(pair.upper_jurisdiction)
        assert lower.is_named_in_the_frozen_ladder
        assert upper.is_named_in_the_frozen_ladder


def test_the_two_upper_layers_are_declared_unmeasurable_before_the_run() -> None:
    assert (
        layer_named("compound-layer").standing
        is LayerStanding.SOURCE_SUPPLIED_NO_CODED_CARRIER
    )
    assert (
        layer_named("sentence-card").standing
        is LayerStanding.SOURCE_SUPPLIED_NO_CODED_CARRIER
    )


def test_the_refuting_fields_are_the_four_named_in_the_hypothesis() -> None:
    assert set(MATCH_CRITERION.refuting_fields) == {
        "Gate",
        "Identity",
        "Residual",
        "Closure",
    }
    assert MATCH_CRITERION.compared_fields == COMPARED_FIELDS


def test_the_frozen_cases_were_written_with_their_reasons() -> None:
    assert len(FROZEN_CASES) == 5
    for case in FROZEN_CASES:
        assert case.why_chosen.strip()
    assert len({case.surface for case in FROZEN_CASES}) == len(FROZEN_CASES)


def test_an_undeclared_pair_is_refused_after_the_run() -> None:
    with pytest.raises(FractalTransitionPreregistrationError):
        pair_named("syllable-to-sentence")
