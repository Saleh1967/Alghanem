"""Tests for the third AIM.1 derivation reader over declared, unbuildable values."""

from __future__ import annotations

import ast
import pkgutil
from dataclasses import fields, replace
from enum import Enum
from pathlib import Path

import pytest

import alghanem.kernel as kernel_package
from alghanem.program import (
    CODOMAIN_DERIVED_FROM_LITERAL_WRITES_ONLY,
    DEFERRED_VALUE_NAMED_RESIDUALS,
    REFUSAL_SHAPE_IS_NOT_A_DECLARED_VOCABULARY,
    SECTION_4_DECLARED_VALUE_NAMES,
    SECTION_4_NAMES_THREE_VALUES_ONLY,
    SIBLING_ADMISSION_REFUSAL_DEPENDS_ON_VOCABULARY_SIZE,
    DeferredValueLedger,
    DeferredValueLedgerError,
    DeferredValueRow,
    DeferredValueShape,
    DeferredValueSite,
    GuardCensus,
    ReadGuard,
    read_deferred_value_ledger,
)
from alghanem.program import deferred_value_ledger as reader_module
from alghanem.program.aims import DESIGN_SOURCE_OPEN_QUESTION

_ANSWER_MARKERS = (
    "answer",
    "verdict",
    "conclusion",
    "resolution",
    "decision",
    "outcome",
    "birth",
    "promotion",
    "indicator",
    "score",
    "percent",
    "estimate",
    "priority",
)

_READER_TYPES = (
    ReadGuard,
    GuardCensus,
    DeferredValueRow,
    DeferredValueLedger,
)


def naming_row(**overrides: object) -> DeferredValueRow:
    base: dict[str, object] = dict(
        site=DeferredValueSite.CLOSED_BY_FROZEN_EXPERIMENT,
        declared_shape=DeferredValueShape.REFUSED_BY_NAMING_THE_VALUE,
        derived_shape=DeferredValueShape.REFUSED_BY_NAMING_THE_VALUE,
        evidence_line=191,
    )
    base.update(overrides)
    return DeferredValueRow(**base)  # type: ignore[arg-type]


def sibling_row(**overrides: object) -> DeferredValueRow:
    base: dict[str, object] = dict(
        site=DeferredValueSite.MORPHO_FUNCTIONAL,
        declared_shape=DeferredValueShape.REFUSED_BY_ADMITTING_ONLY_A_SIBLING,
        derived_shape=DeferredValueShape.REFUSED_BY_ADMITTING_ONLY_A_SIBLING,
        evidence_line=188,
        admitted_sibling="DISTRIBUTIONAL",
    )
    base.update(overrides)
    return DeferredValueRow(**base)  # type: ignore[arg-type]


def unreachable_row(**overrides: object) -> DeferredValueRow:
    base: dict[str, object] = dict(
        site=DeferredValueSite.BIRTH_IN_SCOPE,
        declared_shape=DeferredValueShape.UNREACHABLE_FROM_SOLE_AUTHORITY,
        derived_shape=DeferredValueShape.UNREACHABLE_FROM_SOLE_AUTHORITY,
        evidence_line=378,
        authority_codomain=("DEFER_IN_SCOPE",),
    )
    base.update(overrides)
    return DeferredValueRow(**base)  # type: ignore[arg-type]


def test_the_reader_covers_exactly_the_three_values_section_four_names() -> None:
    assert tuple(site.member_name for site in DeferredValueSite) == (
        SECTION_4_DECLARED_VALUE_NAMES
    )
    ledger = read_deferred_value_ledger()
    assert ledger.row_count == 3
    assert [row.site.member_name for row in ledger.rows] == list(
        SECTION_4_DECLARED_VALUE_NAMES
    )


def test_each_declared_shape_is_confirmed_by_the_shape_derived_from_the_code() -> None:
    ledger = read_deferred_value_ledger()
    derived = {row.site: row.derived_shape for row in ledger.rows}
    assert derived == {
        DeferredValueSite.CLOSED_BY_FROZEN_EXPERIMENT: (
            DeferredValueShape.REFUSED_BY_NAMING_THE_VALUE
        ),
        DeferredValueSite.MORPHO_FUNCTIONAL: (
            DeferredValueShape.REFUSED_BY_ADMITTING_ONLY_A_SIBLING
        ),
        DeferredValueSite.BIRTH_IN_SCOPE: (
            DeferredValueShape.UNREACHABLE_FROM_SOLE_AUTHORITY
        ),
    }
    for row in ledger.rows:
        assert row.declared_shape is row.derived_shape


def test_the_three_shapes_are_each_actually_occupied() -> None:
    counts = read_deferred_value_ledger().shape_counts
    assert set(counts) == set(DeferredValueShape)
    assert all(count == 1 for count in counts.values())


def test_a_declared_shape_that_contradicts_the_derived_one_is_refused() -> None:
    with pytest.raises(DeferredValueLedgerError, match="شكلٌ مُعلَن"):
        naming_row(declared_shape=DeferredValueShape.UNREACHABLE_FROM_SOLE_AUTHORITY)


def test_sibling_and_codomain_fields_are_required_exactly_where_they_apply() -> None:
    with pytest.raises(DeferredValueLedgerError, match="الأخ المقبول وحده"):
        sibling_row(admitted_sibling="")
    with pytest.raises(DeferredValueLedgerError, match="يبقى فارغًا"):
        naming_row(admitted_sibling="DISTRIBUTIONAL")
    with pytest.raises(DeferredValueLedgerError, match="مجالٍ فارغ"):
        unreachable_row(authority_codomain=())
    with pytest.raises(DeferredValueLedgerError, match="لا يُسجَّل إلا"):
        naming_row(authority_codomain=("DEFER_IN_SCOPE",))


def test_a_value_in_its_own_authority_codomain_is_not_recorded_as_held() -> None:
    with pytest.raises(DeferredValueLedgerError, match="حاضرٌ في مجال سلطته"):
        unreachable_row(authority_codomain=("DEFER_IN_SCOPE", "BIRTH_IN_SCOPE"))


def test_admitting_the_member_itself_is_a_release_not_a_hold() -> None:
    with pytest.raises(DeferredValueLedgerError, match="ليس العضو نفسه"):
        sibling_row(admitted_sibling="MORPHO_FUNCTIONAL")


def test_closed_vocabularies_reject_foreign_values() -> None:
    with pytest.raises(DeferredValueLedgerError, match="موضع القيمة"):
        naming_row(site="CLOSED_BY_FROZEN_EXPERIMENT")
    with pytest.raises(DeferredValueLedgerError, match="شكل الحجز المُشتَقّ"):
        naming_row(derived_shape="مرفوضة_بحارسٍ_يُسمّيها")
    with pytest.raises(DeferredValueLedgerError, match="شكل الحجز"):
        read_deferred_value_ledger().rows_with_shape("مرفوضة")  # type: ignore[arg-type]


def test_a_missing_site_is_refused_and_never_read_as_an_unheld_value() -> None:
    ledger = read_deferred_value_ledger()
    with pytest.raises(DeferredValueLedgerError, match="مواضع مُعلَنة لم تُقرَأ"):
        DeferredValueLedger(rows=ledger.rows[:2], guards=ledger.guards)


def test_a_duplicated_site_is_refused() -> None:
    ledger = read_deferred_value_ledger()
    with pytest.raises(DeferredValueLedgerError, match="موضعٌ مكرّر"):
        DeferredValueLedger(rows=(*ledger.rows, ledger.rows[0]), guards=ledger.guards)


def test_an_empty_ledger_is_refused() -> None:
    ledger = read_deferred_value_ledger()
    with pytest.raises(DeferredValueLedgerError, match="غير فارغة"):
        DeferredValueLedger(rows=(), guards=ledger.guards)
    with pytest.raises(DeferredValueLedgerError, match="إحصاء الحرّاس من نوعه"):
        DeferredValueLedger(rows=ledger.rows, guards=ledger.rows)  # type: ignore[arg-type]


def test_a_renamed_or_removed_member_is_a_named_refusal(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import alghanem.arabic.readiness_rank as readiness

    monkeypatch.delattr(readiness, "QuestionStatus")
    with pytest.raises(DeferredValueLedgerError, match="غير مرئيّة"):
        read_deferred_value_ledger()


def test_a_site_without_any_hold_in_its_module_is_refused(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original = reader_module._scan_guards

    def no_guards(*args: object, **kwargs: object) -> list[ReadGuard]:
        return []

    monkeypatch.setattr(reader_module, "_scan_guards", no_guards)
    with pytest.raises(DeferredValueLedgerError, match="لا حارسَ يُسمّيه"):
        read_deferred_value_ledger()
    monkeypatch.setattr(reader_module, "_scan_guards", original)


def test_every_guard_over_a_tracked_vocabulary_is_counted_not_skipped() -> None:
    census = read_deferred_value_ledger().guards
    assert census.guard_count == len(census.guards)
    assert census.guard_count >= 2
    for site in DeferredValueSite:
        found = census.guards_over(site.vocabulary_name)
        assert all(guard.vocabulary_name == site.vocabulary_name for guard in found)
    negated = [guard for guard in census.guards if guard.admits_only_this_member]
    assert all(guard.negated for guard in negated)


def test_the_guard_census_refuses_foreign_members() -> None:
    with pytest.raises(DeferredValueLedgerError, match="كل عنصرٍ حارسٌ مرصود"):
        GuardCensus(guards=("not a guard",))  # type: ignore[arg-type]
    with pytest.raises(DeferredValueLedgerError, match="موضع الحارس"):
        ReadGuard(
            module_name="m",
            vocabulary_name="V",
            member_name="M",
            negated=False,
            document_line=0,
        )
    with pytest.raises(DeferredValueLedgerError, match="نفيُ الحارس"):
        ReadGuard(
            module_name="m",
            vocabulary_name="V",
            member_name="M",
            negated="yes",  # type: ignore[arg-type]
            document_line=1,
        )


def test_counts_are_derived_properties_and_never_written_fields() -> None:
    for declaring_type in _READER_TYPES:
        declared = {item.name for item in fields(declaring_type)}
        assert not any("count" in name for name in declared), declaring_type
    ledger = read_deferred_value_ledger()
    assert ledger.row_count == sum(ledger.shape_counts.values())
    with pytest.raises(TypeError):
        ledger.shape_counts[DeferredValueShape.REFUSED_BY_NAMING_THE_VALUE] = 9  # type: ignore[index]


def test_a_read_row_is_frozen_and_replacement_is_revalidated() -> None:
    row = naming_row()
    with pytest.raises(DeferredValueLedgerError, match="شكلٌ مُعلَن"):
        replace(row, declared_shape=DeferredValueShape.UNREACHABLE_FROM_SOLE_AUTHORITY)


@pytest.mark.parametrize("marker", _ANSWER_MARKERS)
def test_no_reader_type_carries_an_answer_bearing_field(marker: str) -> None:
    for declaring_type in _READER_TYPES:
        declared = {item.name for item in fields(declaring_type)}
        assert not any(marker in name for name in declared), declaring_type


def test_the_reader_is_not_bound_to_any_aim() -> None:
    bound = set(vars(reader_module)) & {
        "AimId",
        "AIM_RECORDS",
        "AimRecord",
        "AttainmentStanding",
        "ForeignDeclaredAim",
    }
    assert bound == set()
    for declaring_type in _READER_TYPES:
        declared = {item.name for item in fields(declaring_type)}
        assert not any("aim" in name for name in declared), declaring_type


def test_the_module_cites_its_direct_design_source() -> None:
    assert reader_module.__doc__ is not None
    assert DESIGN_SOURCE_OPEN_QUESTION in reader_module.__doc__
    assert DESIGN_SOURCE_OPEN_QUESTION in reader_module.DESIGN_SOURCE_CITATION_NOTE


def test_the_residuals_left_by_this_reader_are_named_not_hidden() -> None:
    assert set(DEFERRED_VALUE_NAMED_RESIDUALS) == {
        REFUSAL_SHAPE_IS_NOT_A_DECLARED_VOCABULARY,
        SIBLING_ADMISSION_REFUSAL_DEPENDS_ON_VOCABULARY_SIZE,
        CODOMAIN_DERIVED_FROM_LITERAL_WRITES_ONLY,
        SECTION_4_NAMES_THREE_VALUES_ONLY,
    }
    assert all(text.strip() for text in DEFERRED_VALUE_NAMED_RESIDUALS.values())
    with pytest.raises(TypeError):
        DEFERRED_VALUE_NAMED_RESIDUALS["X"] = "y"  # type: ignore[index]


def test_the_sibling_hold_is_refused_when_its_vocabulary_stops_being_two_valued(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import alghanem.arabic.probe_preregistration as preregistration

    three_valued = Enum(  # type: ignore[misc]
        "EvidenceGenus",
        {
            "DISTRIBUTIONAL": "توزيعي",
            "MORPHO_FUNCTIONAL": "صرفي_وظيفي",
            "A_THIRD_GENUS": "ثالث",
        },
    )
    monkeypatch.setattr(preregistration, "EvidenceGenus", three_valued)
    with pytest.raises(DeferredValueLedgerError, match="ثنائية"):
        read_deferred_value_ledger()


def test_the_derived_evidence_line_points_at_the_real_hold() -> None:
    ledger = read_deferred_value_ledger()
    for row in ledger.rows:
        source = Path(
            reader_module.importlib.import_module(row.site.module_name).__file__ or ""
        ).read_text(encoding="utf-8")
        line = source.splitlines()[row.evidence_line - 1]
        assert row.site.vocabulary_name in line, row.site


def test_the_reader_parses_the_modules_it_names() -> None:
    for site in DeferredValueSite:
        source = reader_module._module_source(site.module_name)
        assert isinstance(ast.parse(source), ast.Module)


def test_no_kernel_module_reads_the_deferred_value_reader() -> None:
    for module in pkgutil.walk_packages(
        kernel_package.__path__, prefix="alghanem.kernel."
    ):
        source = module.module_finder.find_spec(  # type: ignore[union-attr]
            module.name
        )
        assert source is not None and source.origin is not None
        text = Path(source.origin).read_text(encoding="utf-8")
        assert "alghanem.program" not in text, module.name
        assert "DeferredValueLedger" not in text, module.name
        assert "DeferredValueSite" not in text, module.name
