"""اختباراتُ فحص العيّنة الخامّ: تُشغِّل الفحصَ على المُودَع لا على مصنوعٍ بديل."""

from __future__ import annotations

import pytest

from alghanem.arabic.alif_carrier_inspection import (
    ALIF_CARRIER_INSPECTION_NAMED_RESIDUALS,
    ONE_ROW_PER_VERSE_LINE_IS_THE_SLICE_PRINCIPLE,
    WASL_ALIF,
    AlifCarrierInspection,
    AlifCarrierInspectionError,
    RasmForm,
    inspect_alif_carrier_rows,
    inspect_carrier_rows,
    inspect_the_deposited_fatiha_alif_carriers,
    sample_other_carrier_rows,
)
from alghanem.arabic.alif_state_raw_count import (
    ALIF,
    SHORT_VOWELS,
    count_alif_states,
    run_raw_count_on_the_deposited_fatiha,
)
from alghanem.arabic.fatiha_source_text import (
    FATIHA_LINES,
    FATIHA_SOURCE_ID,
    FATIHA_SOURCE_TEXT,
)

_FATHA, _DAMMA, _KASRA = SHORT_VOWELS


# --- صفوفُ الألف كلُّها، لا عيّنةٌ منها --------------------------------------


def test_every_alif_row_in_the_deposit_comes_back_none_dropped() -> None:
    table = run_raw_count_on_the_deposited_fatiha()
    samples = inspect_alif_carrier_rows(table)
    assert len(samples) == len(table.alif_rows) == 23
    assert tuple(sample.row for sample in samples) == table.alif_rows


def test_the_inspection_reads_the_count_rather_than_recounting_the_text() -> None:
    table = run_raw_count_on_the_deposited_fatiha()
    inspection = inspect_carrier_rows(table)
    assert inspection.source_id == FATIHA_SOURCE_ID
    assert all(sample.row in table.rows for sample in inspection.alif_samples)


# --- السياق: مقروءٌ من المُودَع لا قيمةٌ موضوعةٌ مكانَه ----------------------


def test_each_sample_carries_the_verse_line_it_came_from() -> None:
    inspection = inspect_the_deposited_fatiha_alif_carriers()
    for sample in inspection.alif_samples:
        assert sample.verse_line in FATIHA_LINES
        assert sample.verse_line == FATIHA_LINES[sample.line_index]
        assert sample.row.word in sample.verse_line


def test_the_position_in_line_indexes_back_to_the_same_row() -> None:
    table = run_raw_count_on_the_deposited_fatiha()
    for sample in inspect_alif_carrier_rows(table):
        line_rows = tuple(
            row for row in table.rows if row.line_index == sample.line_index
        )
        assert line_rows[sample.position_in_line] is sample.row


def test_the_neighbours_are_real_adjacent_atoms_and_none_only_at_the_edges() -> None:
    table = run_raw_count_on_the_deposited_fatiha()
    for sample in inspect_alif_carrier_rows(table):
        line_rows = tuple(
            row for row in table.rows if row.line_index == sample.line_index
        )
        position = sample.position_in_line
        if position == 0:
            assert sample.preceding_carrier is None
        else:
            assert sample.preceding_carrier is line_rows[position - 1]
        if position + 1 == len(line_rows):
            assert sample.following_carrier is None
        else:
            assert sample.following_carrier is line_rows[position + 1]


def test_at_least_one_sample_has_a_neighbour_on_each_side() -> None:
    """لا يُقرأ الجارُ الخالي عادةً؛ فالجيرانُ قيمٌ مقروءةٌ لا حشوٌ ثابت."""
    samples = inspect_the_deposited_fatiha_alif_carriers().alif_samples
    assert any(
        sample.preceding_carrier is not None and sample.following_carrier is not None
        for sample in samples
    )
    assert {sample.line_index for sample in samples} == set(range(7))


def test_a_sample_whose_context_line_contradicts_its_row_is_refused() -> None:
    sample = inspect_the_deposited_fatiha_alif_carriers().alif_samples[0]
    with pytest.raises(AlifCarrierInspectionError, match="غيرُ سطر الصفّ"):
        type(sample)(
            row=sample.row,
            line_index=sample.line_index + 1,
            verse_line=sample.verse_line,
            position_in_line=sample.position_in_line,
            preceding_carrier=None,
            following_carrier=None,
            rasm_form=sample.rasm_form,
        )


# --- صورةُ الرسم: حقلٌ على الصفّ، مقروءٌ من حروف كلمته ------------------------


def test_the_rasm_form_is_populated_on_every_one_of_the_alif_rows() -> None:
    samples = inspect_the_deposited_fatiha_alif_carriers().alif_samples
    assert len(samples) == 23
    for sample in samples:
        assert isinstance(sample.rasm_form, RasmForm)
        assert sample.rasm_form is RasmForm.PLAIN_ALIF
        assert sample.row.carrier == ALIF


def test_the_deposit_holds_no_explicit_wasla_at_all() -> None:
    assert FATIHA_SOURCE_TEXT.count(WASL_ALIF) == 0


def test_the_absent_wasla_form_is_filed_as_a_named_row_not_left_a_zero() -> None:
    inspection = inspect_the_deposited_fatiha_alif_carriers()
    assert "WASLA_FORM_ABSENT_FROM_THIS_DEPOSIT" in inspection.filed_findings
    assert inspection.samples_carrying_the_wasl_form == ()
    assert "RASM_IS_IMLAI_NOT_UTHMANI" in inspection.finding_text(
        "WASLA_FORM_ABSENT_FROM_THIS_DEPOSIT"
    )


def test_a_text_that_does_hold_a_wasla_files_no_absence_and_reads_the_form() -> None:
    """الحقلُ مقروءٌ لا ثابت: نصٌّ فيه «ٱ» يُخرِج صورتَها ولا يُقيَّد غيابُها."""
    table = count_alif_states((WASL_ALIF + "لْحَمْدُ لِلَّهِ",), source_id="نصٌّ مصنوعٌ للاختبار")
    inspection = inspect_carrier_rows(table)
    forms = tuple(sample.rasm_form for sample in inspection.alif_samples)
    assert RasmForm.WASL_ALIF in forms
    assert "WASLA_FORM_ABSENT_FROM_THIS_DEPOSIT" not in inspection.filed_findings
    assert len(inspection.samples_carrying_the_wasl_form) == 1


def test_a_finding_that_was_not_filed_is_not_read_from_the_record() -> None:
    inspection = inspect_the_deposited_fatiha_alif_carriers()
    with pytest.raises(AlifCarrierInspectionError, match="غيرُ مُقيَّد"):
        inspection.finding_text("WASLA_FORM_ABSENT_FROM_THIS_DEPOSIT" * 2)


# --- الشريحة: عيّنةٌ بمبدأٍ مكتوب، لا سحبٌ صامت ------------------------------


def test_the_other_carrier_slice_is_one_row_per_verse_line() -> None:
    table = run_raw_count_on_the_deposited_fatiha()
    sampled = sample_other_carrier_rows(table)
    assert len(sampled) == 7
    assert tuple(row.line_index for row in sampled) == tuple(range(7))
    for sampled_row in sampled:
        assert sampled_row.row.carrier != ALIF
        assert sampled_row.row in table.other_rows_carrying_a_short_vowel
        assert sampled_row.short_vowels
        assert set(sampled_row.short_vowels) <= set(SHORT_VOWELS)


def test_the_slice_principle_is_carried_on_the_record_not_only_in_a_comment() -> None:
    inspection = inspect_the_deposited_fatiha_alif_carriers()
    assert inspection.slice_principle == ONE_ROW_PER_VERSE_LINE_IS_THE_SLICE_PRINCIPLE
    assert "ONE_ROW_PER_VERSE_LINE_IS_THE_SLICE_PRINCIPLE" in inspection.slice_principle


def test_the_slice_is_the_same_on_every_run() -> None:
    first = sample_other_carrier_rows(run_raw_count_on_the_deposited_fatiha())
    second = sample_other_carrier_rows(run_raw_count_on_the_deposited_fatiha())
    assert first == second


def test_a_line_without_a_qualifying_row_gets_no_substitute() -> None:
    table = count_alif_states((ALIF + "ب" + _FATHA,), source_id="نصٌّ مصنوعٌ للاختبار")
    assert sample_other_carrier_rows(table)[0].short_vowels == (_FATHA,)
    empty = count_alif_states((ALIF,), source_id="نصٌّ مصنوعٌ آخر")
    assert sample_other_carrier_rows(empty) == ()


# --- ما لا يقوله هذا الفحص، مُسمًّى -------------------------------------------


def test_no_record_in_this_module_carries_a_verdict_field() -> None:
    inspection = inspect_the_deposited_fatiha_alif_carriers()
    for record in (
        inspection,
        inspection.alif_samples[0],
        inspection.sampled_other_rows[0],
    ):
        names = set(vars(record))
        assert "verdict" not in names
        assert "status" not in names
        assert "established" not in names
        assert "passed" not in names


def test_a_record_outside_its_shape_is_refused() -> None:
    with pytest.raises(AlifCarrierInspectionError, match="اسمِ مصدرٍ"):
        AlifCarrierInspection(
            source_id="  ",
            alif_samples=(),
            sampled_other_rows=(),
            slice_principle=ONE_ROW_PER_VERSE_LINE_IS_THE_SLICE_PRINCIPLE,
            filed_findings=(),
        )
    with pytest.raises(AlifCarrierInspectionError, match="لا نصَّ له"):
        AlifCarrierInspection(
            source_id="نصٌّ مصنوعٌ للاختبار",
            alif_samples=(),
            sampled_other_rows=(),
            slice_principle=ONE_ROW_PER_VERSE_LINE_IS_THE_SLICE_PRINCIPLE,
            filed_findings=("NO_SUCH_RESIDUAL",),
        )
    with pytest.raises(AlifCarrierInspectionError, match="`AlifStateRawCountTable`"):
        inspect_alif_carrier_rows("جدولٌ ليس جدولًا")  # type: ignore[arg-type]
    with pytest.raises(AlifCarrierInspectionError, match="`AlifStateRawCountTable`"):
        sample_other_carrier_rows(None)  # type: ignore[arg-type]


def test_every_named_residual_is_reachable_and_says_something() -> None:
    assert len(ALIF_CARRIER_INSPECTION_NAMED_RESIDUALS) == 6
    for name, text in ALIF_CARRIER_INSPECTION_NAMED_RESIDUALS.items():
        assert name.isupper()
        assert name in text


def test_the_inspection_files_the_standing_narrowings_of_this_step() -> None:
    filed = inspect_the_deposited_fatiha_alif_carriers().filed_findings
    assert "FULL_SET_NOT_A_SAMPLE" in filed
    assert "THE_SLICE_IS_CHOSEN_NOT_REPRESENTATIVE" in filed
    assert "INSPECTION_WRITES_NO_CONDITION" in filed
    assert "RASM_RESIDUAL_STAYS_OPEN" in filed
