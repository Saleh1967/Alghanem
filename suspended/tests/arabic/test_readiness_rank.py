"""Tests for the enforced four-rank phase-2 readiness ladder."""

from __future__ import annotations

import pkgutil
from dataclasses import fields, replace

import pytest

import alghanem.kernel as kernel_package
from alghanem.arabic import (
    PHASE2_OPEN_QUESTION,
    PHASE2_READINESS,
    MeasurementProgress,
    QuestionStatus,
    ReadinessRankError,
    ReadinessRankRecord,
    SpecificationFreeze,
    StructuralReadiness,
)


def record(**overrides: object) -> ReadinessRankRecord:
    base = dict(
        question_id="phase2-question",
        structural_readiness=StructuralReadiness.BUILT_AND_CHECKED,
        specification_freeze=SpecificationFreeze.NOT_YET_FROZEN,
        measurement=MeasurementProgress.NOT_STARTED,
        question=QuestionStatus.OPEN,
        structural_readiness_justification="البنية مبنيّة ومفحوصة باختباراتها",
        specification_freeze_justification="لا مواصفة قادمة مُجمَّدة بعد",
        measurement_justification="لا خطّ قياس في هذا المستودع",
        question_justification="السؤال مسجَّل مفتوحًا باحتمالاته الثلاثة",
    )
    base.update(overrides)
    return ReadinessRankRecord(**base)  # type: ignore[arg-type]


def test_the_four_ranks_are_four_independent_vocabularies() -> None:
    assert len(StructuralReadiness) == 2
    assert len(SpecificationFreeze) == 2
    assert len(MeasurementProgress) == 3
    assert len(QuestionStatus) == 2
    vocabularies = (
        StructuralReadiness,
        SpecificationFreeze,
        MeasurementProgress,
        QuestionStatus,
    )
    members = [member for vocabulary in vocabularies for member in vocabulary]
    assert len(set(members)) == len(members)


@pytest.mark.parametrize(
    "measurement",
    (MeasurementProgress.STARTED, MeasurementProgress.COMPLETED),
)
def test_measurement_requires_a_frozen_specification(
    measurement: MeasurementProgress,
) -> None:
    with pytest.raises(ReadinessRankError, match="غير مُجمَّدة"):
        record(
            measurement=measurement,
            specification_freeze=SpecificationFreeze.NOT_YET_FROZEN,
        )


def test_a_frozen_specification_requires_a_built_and_checked_structure() -> None:
    with pytest.raises(ReadinessRankError, match="لم يُبنَ"):
        record(
            specification_freeze=SpecificationFreeze.FROZEN,
            structural_readiness=StructuralReadiness.NOT_BUILT,
        )


def test_a_frozen_specification_without_measurement_is_admissible() -> None:
    admissible = record(
        specification_freeze=SpecificationFreeze.FROZEN,
        measurement=MeasurementProgress.NOT_STARTED,
    )

    assert admissible.measurement is MeasurementProgress.NOT_STARTED
    assert admissible.question_remains_open is True


def test_a_completed_measurement_with_an_open_question_is_admissible() -> None:
    admissible = record(
        specification_freeze=SpecificationFreeze.FROZEN,
        measurement=MeasurementProgress.COMPLETED,
        question=QuestionStatus.OPEN,
    )

    assert admissible.question_remains_open is True


def test_question_closure_is_declared_but_unconstructible_at_construction() -> None:
    assert QuestionStatus.CLOSED_BY_FROZEN_EXPERIMENT in set(QuestionStatus)

    with pytest.raises(ReadinessRankError, match="لا بوّابة ولادة"):
        record(
            question=QuestionStatus.CLOSED_BY_FROZEN_EXPERIMENT,
            specification_freeze=SpecificationFreeze.FROZEN,
            measurement=MeasurementProgress.COMPLETED,
        )


def test_closure_is_refused_by_its_own_reason_not_by_a_missing_measurement() -> None:
    with pytest.raises(ReadinessRankError, match="لا بوّابة ولادة"):
        record(
            question=QuestionStatus.CLOSED_BY_FROZEN_EXPERIMENT,
            measurement=MeasurementProgress.NOT_STARTED,
        )


@pytest.mark.parametrize(
    "field_name",
    (
        "structural_readiness_justification",
        "specification_freeze_justification",
        "measurement_justification",
        "question_justification",
    ),
)
@pytest.mark.parametrize("blank", ("", "   "))
def test_every_rank_carries_a_non_blank_justification(
    field_name: str, blank: str
) -> None:
    with pytest.raises(ReadinessRankError):
        record(**{field_name: blank})


def test_a_blank_question_reference_is_refused() -> None:
    with pytest.raises(ReadinessRankError, match="معرّف السؤال"):
        record(question_id="  ")


@pytest.mark.parametrize(
    ("field_name", "value"),
    (
        ("structural_readiness", "بُني_وفُحص"),
        ("specification_freeze", QuestionStatus.OPEN),
        ("measurement", "لم_يبدأ"),
        ("question", MeasurementProgress.NOT_STARTED),
    ),
)
def test_a_value_outside_its_vocabulary_is_refused_not_coerced(
    field_name: str, value: object
) -> None:
    with pytest.raises(ReadinessRankError, match="closed vocabulary"):
        record(**{field_name: value})


def test_the_recorded_readiness_states_todays_actual_ranks() -> None:
    assert PHASE2_READINESS.structural_readiness is (
        StructuralReadiness.BUILT_AND_CHECKED
    )
    assert PHASE2_READINESS.specification_freeze is SpecificationFreeze.NOT_YET_FROZEN
    assert PHASE2_READINESS.measurement is MeasurementProgress.NOT_STARTED
    assert PHASE2_READINESS.question is QuestionStatus.OPEN


def test_the_recorded_readiness_references_the_recorded_open_question() -> None:
    assert PHASE2_READINESS.question_id == PHASE2_OPEN_QUESTION.question_id
    assert PHASE2_READINESS.question_remains_open is PHASE2_OPEN_QUESTION.remains_open


def test_a_readiness_record_carries_no_answer_verdict_or_birth_field() -> None:
    declared = {item.name for item in fields(ReadinessRankRecord)}
    for marker in (
        "answer",
        "verdict",
        "conclusion",
        "resolution",
        "decision",
        "result",
        "outcome",
        "birth",
        "promotion",
    ):
        assert not any(marker in name for name in declared), marker


def test_a_readiness_record_is_frozen_and_replacement_is_revalidated() -> None:
    with pytest.raises(ReadinessRankError, match="غير مُجمَّدة"):
        replace(PHASE2_READINESS, measurement=MeasurementProgress.STARTED)


def test_no_kernel_module_reads_the_readiness_ladder() -> None:
    for module in pkgutil.walk_packages(
        kernel_package.__path__, prefix="alghanem.kernel."
    ):
        source = module.module_finder.find_spec(  # type: ignore[union-attr]
            module.name
        )
        assert source is not None and source.origin is not None
        with open(source.origin, encoding="utf-8") as handle:
            text = handle.read()
        assert "readiness_rank" not in text, module.name
        assert "ReadinessRankRecord" not in text, module.name
        assert "PHASE2_READINESS" not in text, module.name
