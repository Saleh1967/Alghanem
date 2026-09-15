"""اختباراتُ جدول جذور «مقاييس اللغة»: البصمةُ من البايتات، والعدُّ بقاعدته."""

from __future__ import annotations

import hashlib

import pytest

from alghanem.arabic.maqayis_root_table_deposit import (
    DECLARED_COLUMNS,
    FROZEN_ROOT_TABLE,
    REDERIVED_DISTINCT_TRILATERAL_ROOTS,
    REDERIVED_RECORD_COUNT,
    REDERIVED_SPECIFICATION_FIGURES,
    ROOT_TABLE_RELATIVE_PATH,
    TRILATERAL_ROOT_TYPE,
    MaqayisRootTableError,
    RederivedSpecificationFigure,
    RootTableReference,
    read_root_table_bytes,
    rederive_distinct_trilateral_roots,
    rederive_record_count,
    root_table_digest,
    root_table_path,
    root_table_rows,
)


def test_the_digest_is_derived_from_the_bytes_not_copied() -> None:
    """البصمةُ تُشتَقّ من البايتات على القرص، ولا تُقرأ من حقلٍ مكتوب."""

    data = read_root_table_bytes()
    assert hashlib.sha256(data).hexdigest() == FROZEN_ROOT_TABLE.sha256_hex
    assert len(data) == FROZEN_ROOT_TABLE.byte_length
    assert root_table_digest() == FROZEN_ROOT_TABLE.sha256_hex


def test_the_file_is_in_the_tree_at_its_declared_path() -> None:
    """الملفُّ موجودٌ بمساره المُعلَن، والمسارُ مُشتقٌّ من جذر المستودع."""

    assert root_table_path().is_file()
    assert root_table_path().name == ROOT_TABLE_RELATIVE_PATH


def test_the_declared_header_is_matched_before_any_column_is_counted() -> None:
    """لا يُعَدّ عمودٌ باسمٍ متوهَّم: الترويسةُ تُطابَق قبل العدّ."""

    rows = root_table_rows()
    assert rows
    assert tuple(rows[0]) == DECLARED_COLUMNS


def test_the_record_count_is_rederived_from_the_frozen_bytes() -> None:
    """٤٬٥٧٦ سجلًّا مُعادُ الاشتقاق، لا منقولٌ من النصّ الوارد."""

    assert rederive_record_count() == REDERIVED_RECORD_COUNT == 4_576


def test_a_row_count_is_not_a_line_count() -> None:
    """أسطرُ الملفّ ليست سجلّاته: حقولٌ تحمل أسطرًا داخلها، والقاعدةُ تقول ذلك."""

    line_count = read_root_table_bytes().count(b"\n")
    assert line_count > rederive_record_count()


def test_the_trilateral_root_count_is_on_distinct_roots_not_rows() -> None:
    """٤٬٠٨٧ على الجذور المتمايزة؛ وصفوفُ «ثلاثي» ٤٬٠٨٩ لجذرين بصفّين."""

    rows = root_table_rows()
    trilateral_rows = [row for row in rows if row["root_type"] == TRILATERAL_ROOT_TYPE]
    assert len(trilateral_rows) == 4_089
    assert (
        rederive_distinct_trilateral_roots()
        == REDERIVED_DISTINCT_TRILATERAL_ROOTS
        == 4_087
    )


def test_the_rederived_figures_carry_their_counting_rule_and_their_limit() -> None:
    """رقمٌ بلا قاعدةِ عدٍّ أو بلا حدٍّ مكتوبٍ لما لا يُثبته لا يُسجَّل."""

    figures = {entry.figure: entry for entry in REDERIVED_SPECIFICATION_FIGURES}
    assert set(figures) == {"4,576", "4,087"}
    assert figures["4,576"].rederived_count == rederive_record_count()
    assert figures["4,087"].rederived_count == rederive_distinct_trilateral_roots()
    for entry in REDERIVED_SPECIFICATION_FIGURES:
        assert entry.counting_rule.strip()
        assert entry.what_it_still_does_not_establish.strip()


def test_a_figure_without_a_written_limit_is_refused() -> None:
    """المطابقةُ في القيمة ليست تصديقًا، فحقلُ الحدّ لازمٌ لا زينة."""

    with pytest.raises(MaqayisRootTableError):
        RederivedSpecificationFigure(
            figure="4,576",
            locus="§٢-ب",
            claim_text="«4,576 سجلًّا»",
            rederived_count=4_576,
            counting_rule="قاعدةٌ مُعلَنة",
            what_it_still_does_not_establish="   ",
        )


def test_a_non_positive_count_is_refused() -> None:
    with pytest.raises(MaqayisRootTableError):
        RederivedSpecificationFigure(
            figure="0",
            locus="§٢-ب",
            claim_text="«صفر»",
            rederived_count=0,
            counting_rule="قاعدةٌ مُعلَنة",
            what_it_still_does_not_establish="حدٌّ مكتوب",
        )


def test_a_truncated_or_malformed_digest_is_refused() -> None:
    """«2c60...ccb0» طرفان لا بصمة، ولا يُطابَق عليهما."""

    with pytest.raises(MaqayisRootTableError):
        RootTableReference(
            source_name=ROOT_TABLE_RELATIVE_PATH,
            byte_length=FROZEN_ROOT_TABLE.byte_length,
            sha256_hex="2c60...ccb0",
            encoding="utf-8-without-bom",
            normalization_policy="لا تطبيع",
        )


def test_bytes_that_do_not_match_the_frozen_reference_are_refused(tmp_path) -> None:
    """بايتاتٌ أخرى بالمسار نفسِه تُرفَض، فالمطابقةُ عند كلّ قراءةٍ لا مرّةً."""

    (tmp_path / ROOT_TABLE_RELATIVE_PATH).write_bytes(b"root_full\n")
    with pytest.raises(MaqayisRootTableError):
        read_root_table_bytes(tmp_path)


def test_a_missing_file_is_named_in_the_refusal(tmp_path) -> None:
    with pytest.raises(MaqayisRootTableError) as excinfo:
        read_root_table_bytes(tmp_path)
    assert ROOT_TABLE_RELATIVE_PATH in str(excinfo.value)
