"""Tests for the classical-concept to kernel-structure map."""

from __future__ import annotations

import json
import pkgutil
from dataclasses import fields
from pathlib import Path

import pytest

import alghanem.kernel as kernel_package
from alghanem.arabic import (
    ClassicalKernelMapError,
    MapRow,
    MapRowReading,
    MapSanad,
    kernel_symbol_names,
    read_map,
)
from alghanem.arabic.external_audit import audit_card

_EXAMPLES = Path(__file__).resolve().parents[2] / "examples" / "external_audit"
_CARDS = (
    "man_2_255.yaml",
    "maa_2_197.yaml",
    "imran_3_33.yaml",
    "hadhan_20_63.yaml",
)


def test_the_map_holds_exactly_twelve_distinct_rows() -> None:
    rows = read_map()
    assert len(rows) == 12
    assert len({row.row.classical_concept for row in rows}) == 12
    assert len({row.row.kernel_symbol for row in rows}) == 12


def test_the_sanad_vocabulary_is_closed_at_three_members() -> None:
    assert len(MapSanad) == 3
    with pytest.raises(ClassicalKernelMapError, match="مفردته المغلقة"):
        MapRow(
            classical_concept="الوجود",
            kernel_symbol="StructuralDecisionStatus",
            sanad="مُشتقّ_من_الشيفرة",  # type: ignore[arg-type]
        )


def test_structure_presence_is_read_from_the_tree_not_written() -> None:
    present = kernel_symbol_names()
    assert "StructuralDecisionStatus" in present
    assert "TransitionContentIdentity" in present
    assert "Carrier" not in present
    for reading in read_map():
        assert reading.structure_present is (reading.row.kernel_symbol in present)


def test_the_carrier_row_is_declared_and_unverified_because_no_such_structure() -> None:
    carrier = next(
        reading for reading in read_map() if reading.row.kernel_symbol == "Carrier"
    )
    assert carrier.structure_present is False
    assert carrier.row.sanad is MapSanad.مُصرَّح_غير_مُتحقَّق
    assert carrier.is_verified_against_the_tree is False


def test_an_absent_structure_may_not_claim_derivation_from_the_code() -> None:
    with pytest.raises(ClassicalKernelMapError, match="ادّعاءُ قراءةٍ لم تجرِ"):
        MapRowReading(
            row=MapRow(
                classical_concept="الحامل",
                kernel_symbol="Carrier",
                sanad=MapSanad.مُشتقّ_من_الشيفرة,
            ),
            structure_present=False,
        )


def test_a_present_structure_may_not_be_recorded_as_unverified() -> None:
    with pytest.raises(ClassicalKernelMapError, match="جرى فعلاً"):
        MapRowReading(
            row=MapRow(
                classical_concept="الوجود",
                kernel_symbol="StructuralDecisionStatus",
                sanad=MapSanad.مُصرَّح_غير_مُتحقَّق,
            ),
            structure_present=True,
        )


def test_carrier_and_state_rows_are_translation_judgements_not_transmission() -> None:
    state = next(
        reading for reading in read_map() if reading.row.kernel_symbol == "State"
    )
    assert state.row.sanad is MapSanad.اجتهاد_ترجمة


def test_an_absent_kernel_tree_is_refused_not_read_as_no_structures(
    tmp_path: Path,
) -> None:
    with pytest.raises(ClassicalKernelMapError, match="لم تُقرأ الشجرة لأجله"):
        kernel_symbol_names(tmp_path)


def test_no_type_here_carries_a_count_or_verdict_field() -> None:
    for declaring_type in (MapRow, MapRowReading):
        declared = {item.name for item in fields(declaring_type)}
        for marker in ("count", "number", "total", "verdict", "birth"):
            assert not any(marker in name for name in declared), marker


def test_the_module_reads_no_kernel_authority() -> None:
    source = (
        Path(__file__).resolve().parents[2]
        / "src"
        / "alghanem"
        / "arabic"
        / "classical_kernel_map.py"
    ).read_text(encoding="utf-8")
    imports = tuple(
        line for line in source.splitlines() if line.startswith(("import ", "from "))
    )
    assert imports
    assert not any("kernel" in line for line in imports)


def test_no_kernel_module_reads_this_map() -> None:
    for module in pkgutil.walk_packages(
        kernel_package.__path__, prefix="alghanem.kernel."
    ):
        spec = module.module_finder.find_spec(module.name)  # type: ignore[union-attr]
        assert spec is not None and spec.origin is not None
        text = Path(spec.origin).read_text(encoding="utf-8")
        for name in ("classical_kernel_map", "MapRowReading", "read_map"):
            assert name not in text, (module.name, name)


@pytest.mark.parametrize("card", _CARDS)
def test_this_map_changes_no_external_audit_field(card: str) -> None:
    before = json.dumps(
        audit_card(_EXAMPLES / card).to_dict(), ensure_ascii=False, sort_keys=True
    )
    read_map()
    after = json.dumps(
        audit_card(_EXAMPLES / card).to_dict(), ensure_ascii=False, sort_keys=True
    )
    assert before == after
