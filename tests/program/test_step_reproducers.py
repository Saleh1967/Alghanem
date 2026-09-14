"""اختبارات ربطِ الخطوة بكودها: أن يُستدعى شيءٌ ليس أن يُستدعى كودُ الخطوة."""

from __future__ import annotations

import pkgutil

import pytest

import alghanem.kernel as kernel_package
from alghanem.program.binary_outcome import GapClosureOutcome, MidFigureClassification
from alghanem.program.direct_certainty import (
    CertaintySourceGenus,
    DirectCertaintyStep,
    FreezeStatus,
    ProtocolRun,
    StepRecord,
    assess_freeze,
    run_step,
)
from alghanem.program.step_reproducers import (
    STEP_BINDING_DISCOVERY,
    STEP_REPRODUCERS,
    STEP_REPRODUCERS_NAMED_RESIDUALS,
    BindingStanding,
    ReproducerRef,
    StepImplementationStanding,
    StepReproducerError,
    assess_record_binding,
    assess_run_bindings,
    derive_implemented_steps,
    derive_raw_count_record,
    derive_reproducers_run_step_cannot_call,
    derive_unimplemented_steps,
    step_implementation_standing,
)

_GATE_MODULE = "alghanem.arabic.encoding.contamination_gate"
_GATE_CALLABLE = "derive_negative_filter_blind_spots"


def _record(
    step: DirectCertaintyStep,
    module: str = _GATE_MODULE,
    callable_name: str = _GATE_CALLABLE,
) -> StepRecord:
    return StepRecord(
        step=step,
        reproducer_module=module,
        reproducer_callable=callable_name,
        source_genus=CertaintySourceGenus.RERUN_NOW_IN_THIS_PROCESS,
    )


# --- السجلّ: صفٌّ لكلّ خطوة، والخالي مقروءٌ لا مطويّ ---------------------------


def test_every_protocol_step_has_a_row_in_the_registry() -> None:
    assert set(STEP_REPRODUCERS) == set(DirectCertaintyStep)


def test_three_of_the_six_steps_have_code_in_this_tree_today() -> None:
    assert derive_implemented_steps() == (
        DirectCertaintyStep.DATA_PURITY_CHECK,
        DirectCertaintyStep.RAW_COUNT,
        DirectCertaintyStep.RAW_SAMPLE_INSPECTION,
    )
    assert len(derive_unimplemented_steps()) == 3


def test_an_empty_row_reads_as_no_implementation_rather_than_silence() -> None:
    assert (
        step_implementation_standing(DirectCertaintyStep.ONE_CONDITION_AT_A_TIME)
        is StepImplementationStanding.NO_IMPLEMENTATION_IN_THIS_TREE
    )
    assert (
        step_implementation_standing(DirectCertaintyStep.DATA_PURITY_CHECK)
        is StepImplementationStanding.IMPLEMENTED_IN_THIS_TREE
    )


def test_a_step_outside_the_vocabulary_is_refused() -> None:
    with pytest.raises(StepReproducerError, match="عضوٌ في `DirectCertaintyStep`"):
        step_implementation_standing("raw_count")  # type: ignore[arg-type]


def test_a_reference_without_a_named_module_or_callable_is_refused() -> None:
    with pytest.raises(StepReproducerError, match="يُسمّي وحدتَه"):
        ReproducerRef(module="  ", callable_name=_GATE_CALLABLE)
    with pytest.raises(StepReproducerError, match="يُسمّي دالتَه"):
        ReproducerRef(module=_GATE_MODULE, callable_name="")


def test_a_reference_that_does_not_resolve_is_refused_at_resolution() -> None:
    with pytest.raises(StepReproducerError, match="لا تُستورَد"):
        ReproducerRef("alghanem.program.no_such_module", _GATE_CALLABLE).resolve()
    with pytest.raises(StepReproducerError, match="لا دالةَ باسم"):
        ReproducerRef(_GATE_MODULE, "no_such_callable").resolve()


# --- رتبةُ الربط الثلاثية -----------------------------------------------------


def test_a_step_bound_to_its_own_registered_code_reads_as_agreeing() -> None:
    row = assess_record_binding(_record(DirectCertaintyStep.DATA_PURITY_CHECK))
    assert row.standing is BindingStanding.BOUND_TO_ITS_OWN_STEP
    assert not row.standing.is_a_named_mismatch


def test_a_step_bound_to_another_steps_code_is_a_named_mismatch() -> None:
    row = assess_record_binding(_record(DirectCertaintyStep.RAW_COUNT))
    assert row.standing is BindingStanding.BOUND_TO_ANOTHER_STEPS_CODE
    assert row.standing.is_a_named_mismatch
    assert row.registered_for == (DirectCertaintyStep.DATA_PURITY_CHECK,)


def test_code_outside_the_registry_is_unjudged_rather_than_refused() -> None:
    row = assess_record_binding(
        _record(DirectCertaintyStep.RAW_COUNT, callable_name="tokenize")
    )
    assert row.standing is BindingStanding.UNJUDGED_NOT_IN_THE_REGISTRY
    assert row.registered_for == ()
    assert not row.standing.is_a_named_mismatch


def test_every_row_carries_its_steps_implementation_standing() -> None:
    row = assess_record_binding(_record(DirectCertaintyStep.ONE_CONDITION_AT_A_TIME))
    assert (
        row.step_standing is StepImplementationStanding.NO_IMPLEMENTATION_IN_THIS_TREE
    )
    filled = assess_record_binding(_record(DirectCertaintyStep.RAW_COUNT))
    assert filled.step_standing is StepImplementationStanding.IMPLEMENTED_IN_THIS_TREE


# --- المسار: صفٌّ لكلّ تصريحٍ بلا طرحٍ ولا اختصار ------------------------------


def test_a_run_yields_one_row_per_record_in_order() -> None:
    run = ProtocolRun(records=tuple(_record(step) for step in DirectCertaintyStep))
    rows = assess_run_bindings(run)
    assert tuple(row.step for row in rows) == tuple(DirectCertaintyStep)
    assert len(rows) == 6


def test_the_gap_this_stage_found_is_reproduced_here_not_asserted() -> None:
    """المسارُ الذي تُسمّيه القراءةُ مخالفًا يبقى مقبولًا عند حكم التجميد."""
    run = ProtocolRun(records=tuple(_record(step) for step in DirectCertaintyStep))
    assert assess_freeze(run).status is FreezeStatus.FROZEN_ADMISSIBLE
    mismatched = [
        row for row in assess_run_bindings(run) if row.standing.is_a_named_mismatch
    ]
    assert len(mismatched) == 5


def test_reading_something_that_is_not_a_run_or_a_record_is_refused() -> None:
    with pytest.raises(StepReproducerError, match="`ProtocolRun`"):
        assess_run_bindings("مسارٌ مذكورٌ في رسالة")  # type: ignore[arg-type]
    with pytest.raises(StepReproducerError, match="`StepRecord`"):
        assess_record_binding("تصريحٌ منقول")  # type: ignore[arg-type]


# --- حدُّ الاختبار العمليّ، مُشتَقًّا من التواقيع -------------------------------


def test_the_gate_functions_run_step_cannot_call_are_derived() -> None:
    unreachable = derive_reproducers_run_step_cannot_call()
    names = {ref.callable_name for ref in unreachable}
    assert names == {"scan_tokens", "scan_lines"}


def test_a_reproducer_needing_an_argument_is_named_though_it_is_the_gate() -> None:
    unreachable = derive_reproducers_run_step_cannot_call()
    assert all(
        ref in STEP_REPRODUCERS[DirectCertaintyStep.DATA_PURITY_CHECK]
        for ref in unreachable
    )


# --- الكشفُ مُسجَّلٌ بآلة قاعدة النتيجتين --------------------------------------


def test_the_discovery_is_filed_as_a_second_outcome_not_as_an_apology() -> None:
    assert STEP_BINDING_DISCOVERY.outcome is GapClosureOutcome.DEEPER_LAYER_REVEALED
    assert STEP_BINDING_DISCOVERY.narrowed_unknown.strip()


def test_the_discovery_opens_on_no_middle_figure() -> None:
    assert STEP_BINDING_DISCOVERY.opening_mid_figure == ""
    assert STEP_BINDING_DISCOVERY.mid_figure_classification is None


# --- السلطة: هذه الوحدة خاملة ------------------------------------------------


def test_no_kernel_module_reads_this_registry() -> None:
    for module in pkgutil.iter_modules(kernel_package.__path__):
        path = f"{kernel_package.__path__[0]}/{module.name}.py"
        try:
            with open(path, encoding="utf-8") as handle:
                source = handle.read()
        except OSError:  # pragma: no cover - a package, not a module file
            continue
        assert "step_reproducers" not in source


def test_the_protocol_module_does_not_import_this_reader() -> None:
    """اتّجاهُ الاعتماد واحدٌ: هذه الوحدة تقرأ البروتوكول ولا يقرؤها."""
    import alghanem.program.direct_certainty as protocol

    with open(protocol.__file__, encoding="utf-8") as handle:
        source = handle.read()
    assert "step_reproducers" not in source


def test_every_named_residual_is_reachable_and_says_something() -> None:
    assert len(STEP_REPRODUCERS_NAMED_RESIDUALS) == 5
    for name, text in STEP_REPRODUCERS_NAMED_RESIDUALS.items():
        assert name.isupper()
        assert name in text


# --- الخطوةُ الأولى: كودٌ يُشغَّل فعلًا لا اسمٌ في السجلّ ----------------------


def test_the_raw_count_row_names_a_zero_argument_entry_point() -> None:
    refs = STEP_REPRODUCERS[DirectCertaintyStep.RAW_COUNT]
    assert len(refs) == 1
    assert refs[0].module == "alghanem.arabic.alif_state_raw_count"
    assert refs[0] not in derive_reproducers_run_step_cannot_call()


def test_run_step_actually_runs_the_raw_count_on_arabic_text() -> None:
    """الاختبارُ العمليّ مُشغَّلًا: ناتجٌ مقيسٌ من نصٍّ عربيّ، لا `None`."""
    ref = STEP_REPRODUCERS[DirectCertaintyStep.RAW_COUNT][0]
    table = run_step(
        StepRecord(
            step=DirectCertaintyStep.RAW_COUNT,
            reproducer_module=ref.module,
            reproducer_callable=ref.callable_name,
            source_genus=CertaintySourceGenus.RERUN_NOW_IN_THIS_PROCESS,
        )
    )
    assert table.rows
    assert table.alif_rows
    assert len(table.rows) == len(table.alif_rows) + len(table.other_carrier_rows)


def test_the_raw_count_declaration_binds_to_its_own_step() -> None:
    ref = STEP_REPRODUCERS[DirectCertaintyStep.RAW_COUNT][0]
    row = assess_record_binding(
        _record(
            DirectCertaintyStep.RAW_COUNT,
            module=ref.module,
            callable_name=ref.callable_name,
        )
    )
    assert row.standing is BindingStanding.BOUND_TO_ITS_OWN_STEP
    assert row.registered_for == (DirectCertaintyStep.RAW_COUNT,)


def test_pointing_the_raw_count_code_at_another_step_is_a_named_mismatch() -> None:
    ref = STEP_REPRODUCERS[DirectCertaintyStep.RAW_COUNT][0]
    row = assess_record_binding(
        _record(
            DirectCertaintyStep.RAW_SAMPLE_INSPECTION,
            module=ref.module,
            callable_name=ref.callable_name,
        )
    )
    assert row.standing is BindingStanding.BOUND_TO_ANOTHER_STEPS_CODE
    assert row.registered_for == (DirectCertaintyStep.RAW_COUNT,)


def test_filling_the_second_row_did_not_fill_the_other_three() -> None:
    """خطوتان مُلئتا، والثلاثُ الباقيةُ تبقى خاليةً مقروءةً لا مُزيَّفة."""
    assert derive_unimplemented_steps() == (
        DirectCertaintyStep.ONE_CONDITION_AT_A_TIME,
        DirectCertaintyStep.ITERATE_UNTIL_FULL_CLASSIFICATION,
        DirectCertaintyStep.FREEZE_ASSESSMENT,
    )
    for step in derive_unimplemented_steps():
        assert STEP_REPRODUCERS[step] == ()


def test_the_raw_count_is_filed_as_a_second_outcome_with_its_figure_classified() -> (
    None
):
    record = derive_raw_count_record()
    assert record.outcome is GapClosureOutcome.DEEPER_LAYER_REVEALED
    assert record.opening_mid_figure.strip()
    assert (
        record.mid_figure_classification
        is MidFigureClassification.INCOMPLETE_MEASUREMENT_ON_A_RIGHT_QUESTION
    )


def test_the_freeze_gate_was_not_touched_by_filling_a_row() -> None:
    """هذه القراءةُ ما زالت قارئًا لا بوّابة: المسارُ المخالفُ يُقبَل كما كان."""
    run = ProtocolRun(records=tuple(_record(step) for step in DirectCertaintyStep))
    assert assess_freeze(run).status is FreezeStatus.FROZEN_ADMISSIBLE


# --- الخطوةُ الثانية: فحصُ العيّنة مربوطًا بخطوته ومُشغَّلًا --------------------


def test_the_sample_inspection_row_names_a_zero_argument_entry_point() -> None:
    refs = STEP_REPRODUCERS[DirectCertaintyStep.RAW_SAMPLE_INSPECTION]
    assert len(refs) == 1
    assert refs[0].module == "alghanem.arabic.alif_carrier_inspection"
    assert refs[0] not in derive_reproducers_run_step_cannot_call()


def test_the_sample_inspection_declaration_binds_to_its_own_step() -> None:
    ref = STEP_REPRODUCERS[DirectCertaintyStep.RAW_SAMPLE_INSPECTION][0]
    row = assess_record_binding(
        _record(
            DirectCertaintyStep.RAW_SAMPLE_INSPECTION,
            module=ref.module,
            callable_name=ref.callable_name,
        )
    )
    assert row.standing is BindingStanding.BOUND_TO_ITS_OWN_STEP
    assert row.registered_for == (DirectCertaintyStep.RAW_SAMPLE_INSPECTION,)
    assert row.step_standing is StepImplementationStanding.IMPLEMENTED_IN_THIS_TREE


def test_run_step_actually_runs_the_sample_inspection_on_the_counted_rows() -> None:
    """الاختبارُ العمليّ مُشغَّلًا: صفوفٌ بسياقها من المُودَع، لا `None`."""
    ref = STEP_REPRODUCERS[DirectCertaintyStep.RAW_SAMPLE_INSPECTION][0]
    inspection = run_step(
        StepRecord(
            step=DirectCertaintyStep.RAW_SAMPLE_INSPECTION,
            reproducer_module=ref.module,
            reproducer_callable=ref.callable_name,
            source_genus=CertaintySourceGenus.RERUN_NOW_IN_THIS_PROCESS,
        )
    )
    assert len(inspection.alif_samples) == 23
    assert all(sample.verse_line.strip() for sample in inspection.alif_samples)
    assert "WASLA_FORM_ABSENT_FROM_THIS_DEPOSIT" in inspection.filed_findings
