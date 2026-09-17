"""اختبارات بروتوكول اليقين المباشر: لا إتمامَ بتصريح، ولا تجميدَ بغير تشغيل."""

from __future__ import annotations

import pkgutil

import pytest

import alghanem.kernel as kernel_package
from alghanem.program.direct_certainty import (
    ABSENCE_OF_BYTES_IS_NOT_EVERY_GROUND_OF_REFUSAL,
    DIRECT_CERTAINTY_NAMED_RESIDUALS,
    REPORTED_UNVERIFIED_FIGURES,
    CertaintySourceGenus,
    DirectCertaintyError,
    DirectCertaintyStep,
    FigureConstraint,
    FreezeAssessment,
    FreezeStatus,
    ProtocolRun,
    StepRecord,
    UnverifiedFigureRecord,
    assess_freeze,
    figures_by_constraint,
    run_step,
)

_GATE_MODULE = "alghanem.arabic.encoding.contamination_gate"
_GATE_CALLABLE = "derive_negative_filter_blind_spots"


def _record(
    step: DirectCertaintyStep,
    genus: CertaintySourceGenus = CertaintySourceGenus.RERUN_NOW_IN_THIS_PROCESS,
) -> StepRecord:
    return StepRecord(
        step=step,
        reproducer_module=_GATE_MODULE,
        reproducer_callable=_GATE_CALLABLE,
        source_genus=genus,
    )


def _full_run(
    genus: CertaintySourceGenus = CertaintySourceGenus.RERUN_NOW_IN_THIS_PROCESS,
) -> ProtocolRun:
    return ProtocolRun(
        records=tuple(_record(step, genus) for step in DirectCertaintyStep)
    )


# --- جنسُ المصدر: واحدٌ فقط يصلح للتجميد ------------------------------------


def test_one_genus_alone_supports_a_freeze() -> None:
    supporting = [genus for genus in CertaintySourceGenus if genus.supports_freeze]
    assert supporting == [CertaintySourceGenus.RERUN_NOW_IN_THIS_PROCESS]


def test_an_earlier_message_of_mine_is_not_exempted_by_being_mine() -> None:
    genus = CertaintySourceGenus.EARLIER_MESSAGE_IN_THIS_CONVERSATION
    assert not genus.supports_freeze
    assert genus.requires_rerun_before_decisive_use


def test_an_obvious_axiom_is_not_exempted_by_being_obvious() -> None:
    genus = CertaintySourceGenus.DECLARED_MATHEMATICAL_INTUITION
    assert not genus.supports_freeze
    assert genus.requires_rerun_before_decisive_use


# --- الخطواتُ ستٌّ، مرتّبةٌ ولا تُتخطّى ---------------------------------------


def test_the_purity_check_is_step_zero() -> None:
    assert DirectCertaintyStep.DATA_PURITY_CHECK.position == 0
    assert DirectCertaintyStep.RAW_COUNT.position == 1


def test_the_steps_are_six_and_their_positions_are_contiguous() -> None:
    positions = [step.position for step in DirectCertaintyStep]
    assert positions == list(range(6))


def test_a_skipped_step_is_refused_at_construction() -> None:
    with pytest.raises(DirectCertaintyError, match="ولا تُتخطّى خطوةٌ"):
        ProtocolRun(
            records=(
                _record(DirectCertaintyStep.DATA_PURITY_CHECK),
                _record(DirectCertaintyStep.RAW_SAMPLE_INSPECTION),
            )
        )


def test_starting_after_the_purity_check_is_refused() -> None:
    with pytest.raises(DirectCertaintyError, match="المنتظَرُ الموضع 0"):
        ProtocolRun(records=(_record(DirectCertaintyStep.RAW_COUNT),))


def test_a_repeated_step_is_refused() -> None:
    with pytest.raises(DirectCertaintyError, match="خطوةٌ مكرّرة"):
        ProtocolRun(
            records=(
                _record(DirectCertaintyStep.DATA_PURITY_CHECK),
                _record(DirectCertaintyStep.DATA_PURITY_CHECK),
            )
        )


# --- الإتمامُ استدعاءٌ لا تصريح ----------------------------------------------


def test_a_step_without_a_named_reproducer_is_refused() -> None:
    with pytest.raises(DirectCertaintyError, match="بلا وحدةٍ تُعيد إنتاجَها"):
        StepRecord(
            step=DirectCertaintyStep.RAW_COUNT,
            reproducer_module="  ",
            reproducer_callable=_GATE_CALLABLE,
            source_genus=CertaintySourceGenus.RERUN_NOW_IN_THIS_PROCESS,
        )
    with pytest.raises(DirectCertaintyError, match="بلا دالةٍ تُستدعى"):
        StepRecord(
            step=DirectCertaintyStep.RAW_COUNT,
            reproducer_module=_GATE_MODULE,
            reproducer_callable="",
            source_genus=CertaintySourceGenus.RERUN_NOW_IN_THIS_PROCESS,
        )


def test_running_a_step_actually_imports_and_calls_it_now() -> None:
    blind = run_step(_record(DirectCertaintyStep.DATA_PURITY_CHECK))
    assert blind != ()


def test_a_reproducer_that_does_not_import_is_refused_at_run_time() -> None:
    record = StepRecord(
        step=DirectCertaintyStep.RAW_COUNT,
        reproducer_module="alghanem.program.no_such_module_here",
        reproducer_callable=_GATE_CALLABLE,
        source_genus=CertaintySourceGenus.RERUN_NOW_IN_THIS_PROCESS,
    )
    with pytest.raises(DirectCertaintyError, match="لا تُستورَد"):
        run_step(record)


def test_a_reproducer_name_that_is_not_there_is_refused_at_run_time() -> None:
    record = StepRecord(
        step=DirectCertaintyStep.RAW_COUNT,
        reproducer_module=_GATE_MODULE,
        reproducer_callable="no_such_callable_here",
        source_genus=CertaintySourceGenus.RERUN_NOW_IN_THIS_PROCESS,
    )
    with pytest.raises(DirectCertaintyError, match="لا دالةَ باسم"):
        run_step(record)


def test_a_reproducer_that_is_not_callable_is_refused_at_run_time() -> None:
    record = StepRecord(
        step=DirectCertaintyStep.RAW_COUNT,
        reproducer_module=_GATE_MODULE,
        reproducer_callable="CONTAMINATION_SAMPLE_LINES",
        source_genus=CertaintySourceGenus.RERUN_NOW_IN_THIS_PROCESS,
    )
    with pytest.raises(DirectCertaintyError, match="ليس قابلًا للاستدعاء"):
        run_step(record)


# --- حكمُ التجميد -------------------------------------------------------------


def test_a_complete_rerun_alone_is_admitted() -> None:
    assessment = assess_freeze(_full_run())
    assert assessment.status is FreezeStatus.FROZEN_ADMISSIBLE
    assert assessment.missing_steps == ()
    assert assessment.unverified_steps == ()


def test_an_incomplete_run_is_refused_and_names_what_is_missing() -> None:
    run = ProtocolRun(records=(_record(DirectCertaintyStep.DATA_PURITY_CHECK),))
    assessment = assess_freeze(run)
    assert assessment.status is FreezeStatus.REFUSED_INCOMPLETE_STEPS
    assert DirectCertaintyStep.RAW_COUNT in assessment.missing_steps
    assert len(assessment.missing_steps) == 5


def test_a_complete_run_quoted_from_prose_is_refused() -> None:
    run = _full_run(CertaintySourceGenus.PROSE_FROM_ANOTHER_CONVERSATION)
    assessment = assess_freeze(run)
    assert assessment.status is FreezeStatus.REFUSED_UNVERIFIED_SOURCE
    assert assessment.missing_steps == ()
    assert len(assessment.unverified_steps) == 6


def test_incompleteness_is_named_before_source_genus_and_neither_hides_the_other() -> (
    None
):
    run = ProtocolRun(
        records=(
            _record(
                DirectCertaintyStep.DATA_PURITY_CHECK,
                CertaintySourceGenus.PROSE_FROM_ANOTHER_CONVERSATION,
            ),
        )
    )
    assessment = assess_freeze(run)
    assert assessment.status is FreezeStatus.REFUSED_INCOMPLETE_STEPS
    assert assessment.unverified_steps == (DirectCertaintyStep.DATA_PURITY_CHECK,)


def test_an_admitted_verdict_may_not_carry_a_missing_step() -> None:
    with pytest.raises(DirectCertaintyError, match="لا يجتمع تجميدٌ مقبول"):
        FreezeAssessment(
            status=FreezeStatus.FROZEN_ADMISSIBLE,
            reason="دعوى",
            missing_steps=(DirectCertaintyStep.RAW_COUNT,),
            unverified_steps=(),
        )


def test_a_verdict_without_a_written_reason_is_refused() -> None:
    with pytest.raises(DirectCertaintyError, match="بلا علّةٍ مكتوبة"):
        FreezeAssessment(
            status=FreezeStatus.REFUSED_INCOMPLETE_STEPS,
            reason="   ",
            missing_steps=(DirectCertaintyStep.RAW_COUNT,),
            unverified_steps=(),
        )


# --- أرقامُ نصّ البروتوكول تخضع لقاعدته ---------------------------------------


def test_every_reported_figure_arrived_as_prose_and_none_is_a_measurement() -> None:
    assert len(REPORTED_UNVERIFIED_FIGURES) == 17
    for record in REPORTED_UNVERIFIED_FIGURES:
        assert not record.source_genus.supports_freeze
        assert record.subject.strip()
        assert record.figure_text.strip()


def test_the_pre_purification_figures_carry_their_constraint() -> None:
    constraints = {record.constraint for record in REPORTED_UNVERIFIED_FIGURES}
    assert FigureConstraint.COMPUTED_ON_UNPURIFIED_DATA in constraints
    assert FigureConstraint.CLASSIFICATION_INCOMPLETE in constraints
    assert FigureConstraint.NOT_RE_DERIVABLE_IN_THIS_TREE in constraints


def test_the_constraint_split_is_derived_and_covers_every_record() -> None:
    split = figures_by_constraint()
    assert set(split) == set(FigureConstraint)
    counted = sum(len(records) for records in split.values())
    assert counted == len(REPORTED_UNVERIFIED_FIGURES)
    for constraint, records in split.items():
        for record in records:
            assert record.constraint is constraint


def test_no_single_constraint_accounts_for_every_reported_figure() -> None:
    split = figures_by_constraint()
    for constraint, records in split.items():
        assert records, f"جنسٌ بلا سجلٍّ واحد: {constraint}"
        assert len(records) < len(REPORTED_UNVERIFIED_FIGURES)


def test_the_two_constraints_bytes_cannot_lift_are_populated() -> None:
    split = figures_by_constraint()
    assert split[FigureConstraint.COMPUTED_ON_UNPURIFIED_DATA]
    assert split[FigureConstraint.CLASSIFICATION_INCOMPLETE]
    assert "ABSENCE_OF_BYTES_IS_NOT_EVERY_GROUND_OF_REFUSAL" in (
        ABSENCE_OF_BYTES_IS_NOT_EVERY_GROUND_OF_REFUSAL
    )
    assert (
        DIRECT_CERTAINTY_NAMED_RESIDUALS[
            "ABSENCE_OF_BYTES_IS_NOT_EVERY_GROUND_OF_REFUSAL"
        ]
        == ABSENCE_OF_BYTES_IS_NOT_EVERY_GROUND_OF_REFUSAL
    )


def test_a_rerun_figure_may_not_be_filed_as_unverified() -> None:
    with pytest.raises(DirectCertaintyError, match="لا يُسجَّل غيرَ مُتحقَّقٍ منه"):
        UnverifiedFigureRecord(
            subject="رقمٌ أُعيد تشغيله",
            figure_text="٣",
            source_genus=CertaintySourceGenus.RERUN_NOW_IN_THIS_PROCESS,
            constraint=FigureConstraint.NOT_RE_DERIVABLE_IN_THIS_TREE,
        )


def test_a_figure_record_without_a_subject_or_a_figure_is_refused() -> None:
    with pytest.raises(DirectCertaintyError, match="بلا موضوعٍ مُسمًّى"):
        UnverifiedFigureRecord(
            subject=" ",
            figure_text="٣",
            source_genus=CertaintySourceGenus.PROSE_FROM_ANOTHER_CONVERSATION,
            constraint=FigureConstraint.NOT_RE_DERIVABLE_IN_THIS_TREE,
        )
    with pytest.raises(DirectCertaintyError, match="بلا رقمٍ مكتوبٍ"):
        UnverifiedFigureRecord(
            subject="موضوع",
            figure_text=" ",
            source_genus=CertaintySourceGenus.PROSE_FROM_ANOTHER_CONVERSATION,
            constraint=FigureConstraint.NOT_RE_DERIVABLE_IN_THIS_TREE,
        )


# --- السلطة: هذه الوحدة خاملة ------------------------------------------------


def test_no_kernel_module_reads_this_protocol() -> None:
    for module in pkgutil.iter_modules(kernel_package.__path__):
        path = f"{kernel_package.__path__[0]}/{module.name}.py"
        try:
            with open(path, encoding="utf-8") as handle:
                source = handle.read()
        except OSError:  # pragma: no cover - a package, not a module file
            continue
        assert "direct_certainty" not in source


def test_every_named_residual_is_reachable_and_says_something() -> None:
    assert len(DIRECT_CERTAINTY_NAMED_RESIDUALS) == 6
    for name, text in DIRECT_CERTAINTY_NAMED_RESIDUALS.items():
        assert name.isupper()
        assert name in text
