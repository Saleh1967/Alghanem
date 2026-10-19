"""Tests for the derived signification-channel indicator (eighth milestone)."""

from __future__ import annotations

import ast
import pkgutil
from dataclasses import fields, replace
from pathlib import Path
from types import MappingProxyType

import pytest

import alghanem.kernel as kernel_package
import alghanem.program.dalala_indicator as dalala_module
from alghanem.arabic import DalalaChannel, IfadaStanding, MafhumKind
from alghanem.program import (
    AIM_RECORDS,
    CHANNEL_IS_DERIVED_BY_A_SECOND_INDEPENDENT_READING_NOTE,
    CHANNEL_READS_THE_CITATION_NOT_THE_MEASURED_ARABIC_SURFACE,
    DALALA_INDICATOR_AUTHORITY_NOTE,
    DALALA_INDICATOR_DESIGN_SOURCE_CITATION_NOTE,
    DALALA_INDICATOR_NAMED_RESIDUALS,
    DESIGN_SOURCE_OPEN_QUESTION,
    IFADA_HERE_IS_READ_STATUS_NOT_LINGUISTIC_BENEFIT,
    MANTUQ_COUNT_IS_NOT_PERFORMANCE,
    MUKHALAFA_IS_UNREAD_IN_TODAYS_TRACE,
    PERFORMANCE_INDICATOR_IS_REFUSED_BY_SECTION_ONE_NOTE,
    UNRESOLVED_REFERENCE_HAS_NO_CHANNEL,
    AimId,
    DalalaIndicatorError,
    DalalaIndicatorLedger,
    DalalaIndicatorRow,
    DalalaReferenceCensus,
    ReadDalalaReference,
    SupportNameIndex,
    load_dalala_indicator_ledger,
)


@pytest.fixture(scope="module")
def ledger() -> DalalaIndicatorLedger:
    return load_dalala_indicator_ledger()


def reference(**overrides: object) -> ReadDalalaReference:
    base: dict[str, object] = {
        "aim_id": AimId.K1,
        "reference_name": "Structural admission boundary",
        "citation_offset": 0,
        "ifada": IfadaStanding.مُفيد,
        "channel": DalalaChannel.منطوق,
        "mafhum_kind": MafhumKind.لا_ينطبق,
    }
    base.update(overrides)
    return ReadDalalaReference(**base)  # type: ignore[arg-type]


# --- the ledger carries one row per aim, in the order §2 declares them ---


def test_every_aim_has_exactly_one_row_in_section_two_order(
    ledger: DalalaIndicatorLedger,
) -> None:
    assert tuple(row.aim_id for row in ledger.rows) == tuple(AIM_RECORDS)
    assert ledger.row_count == len(AIM_RECORDS)
    assert set(ledger.rows_by_aim) == set(AIM_RECORDS)


def test_a_reordered_or_missing_row_is_refused(ledger: DalalaIndicatorLedger) -> None:
    with pytest.raises(DalalaIndicatorError, match="بترتيب ورودها"):
        DalalaIndicatorLedger(rows=tuple(reversed(ledger.rows)))
    with pytest.raises(DalalaIndicatorError, match="بترتيب ورودها"):
        DalalaIndicatorLedger(rows=ledger.rows[1:])


def test_a_reference_from_another_aim_is_not_counted_for_this_one(
    ledger: DalalaIndicatorLedger,
) -> None:
    row = ledger.rows[0]
    foreign = replace(row.references[0], aim_id=ledger.rows[1].aim_id)
    with pytest.raises(DalalaIndicatorError, match="غايةٍ أخرى"):
        DalalaIndicatorRow(aim_id=row.aim_id, references=(foreign,))


def test_references_keep_the_order_of_the_citation_text(
    ledger: DalalaIndicatorLedger,
) -> None:
    for row in ledger.rows:
        offsets = [item.citation_offset for item in row.references]
        assert offsets == sorted(offsets)
        assert len(set(offsets)) == len(offsets)


# --- the channel is derived, and the two channels are kept apart ---


def test_both_channels_are_read_in_the_standing_trace(
    ledger: DalalaIndicatorLedger,
) -> None:
    counts = ledger.census.channel_counts
    assert set(counts) == set(DalalaChannel)
    assert counts[DalalaChannel.منطوق] > 0
    assert counts[DalalaChannel.مفهوم] > 0


def test_an_understood_reference_names_the_fuller_support_it_reached(
    ledger: DalalaIndicatorLedger,
) -> None:
    understood = [item for item in ledger.census.references if item.is_understood]
    assert understood
    for item in understood:
        assert item.understood_through.strip()
        assert item.understood_through != item.reference_name
        assert item.mafhum_kind is not MafhumKind.لا_ينطبق


def test_the_opposition_part_is_zero_today_and_derived_not_dropped(
    ledger: DalalaIndicatorLedger,
) -> None:
    counts = ledger.census.mafhum_kind_counts
    assert set(counts) == set(MafhumKind)
    assert counts[MafhumKind.مخالفة] == 0
    assert MUKHALAFA_IS_UNREAD_IN_TODAYS_TRACE in DALALA_INDICATOR_NAMED_RESIDUALS


def test_a_name_in_both_indexes_at_once_is_refused() -> None:
    with pytest.raises(DalalaIndicatorError, match="في الفهرسين معًا"):
        SupportNameIndex(
            uttered_names=frozenset({"G0.BV.1"}),
            understood_names=MappingProxyType({"G0.BV.1": "G0.BV.1 full name"}),
        )


def test_a_reference_resolved_by_the_sixth_milestone_but_unreachable_here_is_refused(
    ledger: DalalaIndicatorLedger,
) -> None:
    indicator_ledger = dalala_module.read_aim_indicator_ledger(
        ledger=dalala_module.load_constitution_ledger(
            dalala_module.constitution_document_path()
        ),
        document_text=dalala_module.constitution_document_path().read_text(
            encoding="utf-8"
        ),
        repository_root=dalala_module.repository_root_path(),
    )
    empty = SupportNameIndex(
        uttered_names=frozenset(), understood_names=MappingProxyType({})
    )
    with pytest.raises(DalalaIndicatorError, match="ولم يبلغها"):
        dalala_module.read_dalala_indicator_ledger(
            indicator=indicator_ledger,
            index=empty,
            repository_root=dalala_module.repository_root_path(),
        )
    assert CHANNEL_IS_DERIVED_BY_A_SECOND_INDEPENDENT_READING_NOTE


# --- an excluded reference is uttered in the prose yet carries no channel ---


def test_a_reference_without_a_channel_carries_no_part_and_no_benefit(
    ledger: DalalaIndicatorLedger,
) -> None:
    channel_less = ledger.census.references_without_channel
    assert channel_less
    for item in channel_less:
        assert item.channel is None
        assert item.mafhum_kind is None
        assert item.understood_through == ""
        assert item.ifada is IfadaStanding.غير_مُفيد
    assert UNRESOLVED_REFERENCE_HAS_NO_CHANNEL in DALALA_INDICATOR_NAMED_RESIDUALS


def test_writing_a_part_or_a_road_on_a_channel_less_reference_is_refused() -> None:
    with pytest.raises(DalalaIndicatorError, match=UNRESOLVED_REFERENCE_HAS_NO_CHANNEL):
        reference(
            ifada=IfadaStanding.غير_مُفيد,
            channel=None,
            mafhum_kind=MafhumKind.لا_ينطبق,
        )


def test_a_channel_less_reference_must_be_read_as_not_benefiting() -> None:
    with pytest.raises(DalalaIndicatorError, match="غير_مُفيد"):
        reference(ifada=IfadaStanding.مُفيد, channel=None, mafhum_kind=None)


def test_the_part_is_refused_on_the_uttered_and_required_on_the_understood() -> None:
    with pytest.raises(DalalaIndicatorError, match="قسيمه"):
        reference(mafhum_kind=MafhumKind.موافقة)
    with pytest.raises(DalalaIndicatorError, match="يلزمه قسمُه"):
        reference(channel=DalalaChannel.مفهوم, mafhum_kind=MafhumKind.لا_ينطبق)
    with pytest.raises(DalalaIndicatorError, match="تسميةُ تمام ما فُهِم"):
        reference(channel=DalalaChannel.مفهوم, mafhum_kind=MafhumKind.موافقة)


# --- benefit is reaching a declared status, and the unread is a member ---


def test_every_ifada_member_is_counted_even_at_zero(
    ledger: DalalaIndicatorLedger,
) -> None:
    counts = ledger.census.ifada_counts
    assert set(counts) == set(IfadaStanding)
    assert sum(counts.values()) == ledger.census.reference_count
    assert set(ledger.ifada_standing_counts) == set(IfadaStanding)
    assert sum(ledger.ifada_standing_counts.values()) == ledger.row_count


def test_a_support_without_a_declared_status_is_unread_not_unbeneficial(
    ledger: DalalaIndicatorLedger,
) -> None:
    unread = [
        item
        for item in ledger.census.references
        if item.ifada is IfadaStanding.غير_مقروء
    ]
    assert unread
    for item in unread:
        assert item.channel is not None
    assert IFADA_HERE_IS_READ_STATUS_NOT_LINGUISTIC_BENEFIT in (
        DALALA_INDICATOR_NAMED_RESIDUALS
    )


def test_the_row_standing_is_derived_from_its_references(
    ledger: DalalaIndicatorLedger,
) -> None:
    for row in ledger.rows:
        standings = {item.ifada for item in row.references}
        if IfadaStanding.مُفيد in standings:
            assert row.ifada_standing is IfadaStanding.مُفيد
        elif IfadaStanding.غير_مقروء in standings:
            assert row.ifada_standing is IfadaStanding.غير_مقروء
        else:
            assert row.ifada_standing is IfadaStanding.غير_مُفيد


# --- counts are derived properties, never written fields ---


def test_no_type_here_carries_a_count_rank_progress_or_performance_field() -> None:
    for declaring_type in (
        SupportNameIndex,
        ReadDalalaReference,
        DalalaReferenceCensus,
        DalalaIndicatorRow,
        DalalaIndicatorLedger,
    ):
        declared = {item.name for item in fields(declaring_type)}
        for marker in (
            "count",
            "score",
            "rank",
            "progress",
            "percent",
            "ratio",
            "performance",
            "attainment",
            "verdict",
        ):
            assert not any(marker in name for name in declared), marker


def test_every_count_is_a_derived_property() -> None:
    assert isinstance(DalalaIndicatorLedger.row_count, property)
    assert isinstance(DalalaReferenceCensus.reference_count, property)
    assert isinstance(DalalaIndicatorRow.uttered_support_count, property)
    assert isinstance(DalalaIndicatorRow.understood_support_count, property)


def test_the_uttered_and_understood_counts_add_up_to_the_channelled_references(
    ledger: DalalaIndicatorLedger,
) -> None:
    for row in ledger.rows:
        channelled = [item for item in row.references if item.channel is not None]
        assert row.uttered_support_count + row.understood_support_count == len(
            channelled
        )


# --- authority inertness, and the cited design source ---


def test_the_ledger_issues_no_verdict_freeze_or_birth() -> None:
    source = Path(dalala_module.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    assert not any(module.startswith("alghanem.kernel") for module in imported)
    written = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    } & {"Freeze", "BirthVerdict", "AttainmentStanding"}
    assert written == set()


def test_no_kernel_or_arabic_module_reads_this_ledger() -> None:
    import alghanem.arabic as arabic_package

    for package in (kernel_package, arabic_package):
        for module_info in pkgutil.walk_packages(
            package.__path__, prefix=f"{package.__name__}."
        ):
            spec = module_info.module_finder.find_spec(  # type: ignore[union-attr]
                module_info.name
            )
            if spec is None or spec.origin is None:
                continue
            text = Path(spec.origin).read_text(encoding="utf-8")
            assert "dalala_indicator" not in text, module_info.name


def test_the_design_source_is_cited_by_name_not_re_derived_silently() -> None:
    assert DESIGN_SOURCE_OPEN_QUESTION in DALALA_INDICATOR_DESIGN_SOURCE_CITATION_NOTE
    source = Path(dalala_module.__file__).read_text(encoding="utf-8")
    assert DESIGN_SOURCE_OPEN_QUESTION in source


def test_the_performance_name_is_refused_and_its_residual_is_named() -> None:
    assert "§١" in PERFORMANCE_INDICATOR_IS_REFUSED_BY_SECTION_ONE_NOTE
    assert MANTUQ_COUNT_IS_NOT_PERFORMANCE in DALALA_INDICATOR_NAMED_RESIDUALS
    assert CHANNEL_READS_THE_CITATION_NOT_THE_MEASURED_ARABIC_SURFACE in (
        DALALA_INDICATOR_NAMED_RESIDUALS
    )
    assert "لا يكتب بلوغَ غايةٍ" in DALALA_INDICATOR_AUTHORITY_NOTE


def test_every_named_residual_carries_a_non_blank_reason() -> None:
    assert DALALA_INDICATOR_NAMED_RESIDUALS
    for name, reason in DALALA_INDICATOR_NAMED_RESIDUALS.items():
        assert name.isupper()
        assert reason.strip()
