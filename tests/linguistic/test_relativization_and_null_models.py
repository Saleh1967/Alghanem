"""ترتيبُ المنزلة ليس منافسةً، والنماذجُ الأضعفُ مُسجَّلةٌ لا مُشغَّلة."""

from __future__ import annotations

import dataclasses

import pytest

from alghanem.arabic.flt1_qiyas_law import FLT1_QIYAS_TEXT_DIGEST
from alghanem.arabic.nisbah_relativization import (
    FLT1_QIYAS_RELATIVIZATION,
    FLT1_QIYAS_STATEMENT_REF,
)
from alghanem.linguistic.null_model import (
    CORPUS_INDEPENDENCE_CONDITIONS,
    NISBAH_NULL_MODELS,
    NullModelRegistration,
    NullModelRegistrationError,
    RunStanding,
)
from alghanem.linguistic.relativization import (
    ContradictionStanding,
    RelativizationError,
)


def test_the_relativization_record_does_not_supersede_the_qiyas_text() -> None:
    assert FLT1_QIYAS_RELATIVIZATION.supersedes is False
    assert (
        FLT1_QIYAS_RELATIVIZATION.contradiction_standing
        is ContradictionStanding.NO_CONTRADICTION_DEMONSTRATED
    )


def test_the_relativized_digest_is_derived_not_transcribed() -> None:
    assert FLT1_QIYAS_STATEMENT_REF.text_digest == FLT1_QIYAS_TEXT_DIGEST


def test_a_record_declaring_a_contradiction_is_refused_at_construction() -> None:
    with pytest.raises(RelativizationError):
        dataclasses.replace(
            FLT1_QIYAS_RELATIVIZATION,
            contradiction_standing=ContradictionStanding.CONTRADICTION_DEMONSTRATED,
        )


def test_two_identical_questions_are_not_two_levels() -> None:
    with pytest.raises(RelativizationError):
        dataclasses.replace(
            FLT1_QIYAS_RELATIVIZATION,
            representation_question="سؤالٌ واحد",
            relational_question="سؤالٌ واحد",
        )


def test_every_registered_null_model_awaits_a_held_out_corpus() -> None:
    assert NISBAH_NULL_MODELS
    for model in NISBAH_NULL_MODELS:
        assert (
            model.run_standing
            is RunStanding.DEFERRED_UNTIL_A_HELD_OUT_CORPUS_IS_NAMED
        )


def test_a_runnable_registration_before_a_named_corpus_is_refused() -> None:
    with pytest.raises(NullModelRegistrationError):
        NullModelRegistration(
            model_id="carrier-only",
            what_it_represents="الحاملُ وحده",
            what_its_tie_defeats="دعوى أنّ النسبةَ مستوًى زائد",
            run_standing=RunStanding.RUNNABLE,
        )


def test_the_corpus_independence_conditions_are_frozen_and_named() -> None:
    assert CORPUS_INDEPENDENCE_CONDITIONS
    ids = tuple(
        condition.condition_id for condition in CORPUS_INDEPENDENCE_CONDITIONS
    )
    assert len(set(ids)) == len(ids)
