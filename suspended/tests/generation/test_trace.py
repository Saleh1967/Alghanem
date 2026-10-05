"""أثرُ الإنتاج: اتّصالُ البصمات، وبقايا مرصودةٌ في خطواتها لا مكتوبةٌ بجانبها.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import replace

import pytest
from generation_cases import PREDICATE_ID, production_specification, token_trace

from alghanem.generation.trace import (
    GenerationResidual,
    GenerationResidualKind,
    GenerationStage,
    GenerationStep,
    GenerationTrace,
    GenerationTraceError,
)

_DIGEST_A = "a" * 64
_DIGEST_B = "b" * 64
_DIGEST_C = "c" * 64


def _residual(stage: GenerationStage) -> GenerationResidual:
    return GenerationResidual(
        kind=GenerationResidualKind.UNMEASURED_PROSODIC_LAYER,
        stage=stage,
        subject_id="subject.synthetic",
        reason="سببٌ مُسمًّى للاختبار",
    )


def test_a_step_input_is_a_canonical_digest_not_free_text() -> None:
    with pytest.raises(GenerationTraceError):
        GenerationStep(
            stage=GenerationStage.WORD_FORM,
            rule_id="rule.synthetic",
            input_content_id="not-a-digest",
            output_content_id=_DIGEST_A,
            residuals=(),
        )


def test_a_step_without_an_output_names_its_residual() -> None:
    with pytest.raises(GenerationTraceError):
        GenerationStep(
            stage=GenerationStage.PHONOLOGICAL_PROJECTION,
            rule_id="rule.synthetic",
            input_content_id=_DIGEST_A,
            output_content_id=None,
            residuals=(),
        )


def test_a_residual_is_not_attributed_to_another_stage() -> None:
    with pytest.raises(GenerationTraceError):
        GenerationStep(
            stage=GenerationStage.CASE_EFFECT,
            rule_id="rule.synthetic",
            input_content_id=_DIGEST_A,
            output_content_id=_DIGEST_B,
            residuals=(_residual(GenerationStage.WORD_FORM),),
        )


def test_a_chain_is_read_from_its_digests_not_its_order() -> None:
    first = GenerationStep(
        stage=GenerationStage.LEXICAL_SELECTION,
        rule_id="rule.first",
        input_content_id=_DIGEST_A,
        output_content_id=_DIGEST_B,
        residuals=(),
    )
    disconnected = GenerationStep(
        stage=GenerationStage.WORD_FORM,
        rule_id="rule.second",
        input_content_id=_DIGEST_C,
        output_content_id=_DIGEST_A,
        residuals=(),
    )
    with pytest.raises(GenerationTraceError):
        GenerationTrace(steps=(first, disconnected))


def test_no_step_follows_a_step_that_produced_nothing() -> None:
    withheld = GenerationStep(
        stage=GenerationStage.PHONOLOGICAL_PROJECTION,
        rule_id="rule.withheld",
        input_content_id=_DIGEST_A,
        output_content_id=None,
        residuals=(_residual(GenerationStage.PHONOLOGICAL_PROJECTION),),
    )
    following = GenerationStep(
        stage=GenerationStage.ORTHOGRAPHIC_PROJECTION,
        rule_id="rule.after",
        input_content_id=_DIGEST_A,
        output_content_id=_DIGEST_B,
        residuals=(),
    )
    with pytest.raises(GenerationTraceError):
        GenerationTrace(steps=(withheld, following))


def test_the_trace_residuals_are_observed_from_its_steps() -> None:
    residual = _residual(GenerationStage.PHONOLOGICAL_PROJECTION)
    step = GenerationStep(
        stage=GenerationStage.PHONOLOGICAL_PROJECTION,
        rule_id="rule.withheld",
        input_content_id=_DIGEST_A,
        output_content_id=None,
        residuals=(residual,),
    )
    trace = GenerationTrace(steps=(step,))
    assert trace.residuals == (residual,)
    assert trace.output_content_id is None


def test_an_empty_trace_is_not_a_generation() -> None:
    with pytest.raises(GenerationTraceError):
        GenerationTrace(steps=())


def test_the_same_specification_gives_the_same_trace_digest() -> None:
    specification = production_specification()
    first, _, _ = token_trace(specification, PREDICATE_ID)
    second, _, _ = token_trace(specification, PREDICATE_ID)
    assert first.content_id == second.content_id


def test_a_changed_rule_changes_the_trace_digest() -> None:
    specification = production_specification()
    trace, _, _ = token_trace(specification, PREDICATE_ID)
    altered = GenerationTrace(
        steps=(replace(trace.steps[0], rule_id="rule.other"),) + trace.steps[1:]
    )
    assert altered.content_id != trace.content_id
