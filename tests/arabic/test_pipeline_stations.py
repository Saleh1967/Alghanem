"""Tests for the eleven pipeline stations read off the tree."""

from __future__ import annotations

import json
import pkgutil
from dataclasses import fields
from pathlib import Path

import pytest

import alghanem.kernel as kernel_package
from alghanem.arabic import (
    ARABIC_PACKAGE_RELATIVE_PATH,
    PipelineStationsError,
    StationCoding,
    StationDeclaration,
    StationEpistemicState,
    StationReading,
    read_stations,
    repository_root_path,
)
from alghanem.arabic.external_audit import audit_card

_EXAMPLES = Path(__file__).resolve().parents[2] / "examples" / "external_audit"
_CARDS = (
    "man_2_255.yaml",
    "maa_2_197.yaml",
    "imran_3_33.yaml",
    "hadhan_20_63.yaml",
)


def declaration(**overrides: object) -> StationDeclaration:
    base: dict[str, object] = {
        "ordinal": 1,
        "title": "الرصدُ السطحيّ الخام",
        "module_relative_path": "encoding/observation.py",
        "epistemic_state": StationEpistemicState.معلومة,
    }
    base.update(overrides)
    return StationDeclaration(**base)  # type: ignore[arg-type]


def test_the_table_holds_exactly_eleven_successive_stations() -> None:
    readings = read_stations()
    assert len(readings) == 11
    assert [reading.declaration.ordinal for reading in readings] == list(range(1, 12))


def test_every_declared_station_names_a_module_that_exists_in_the_tree() -> None:
    root = repository_root_path()
    for reading in read_stations():
        assert reading.is_coded is True
        assert (root / reading.declaration.module_path).is_file()


def test_a_station_whose_module_is_absent_reads_as_uncoded_not_skipped(
    tmp_path: Path,
) -> None:
    package = tmp_path / ARABIC_PACKAGE_RELATIVE_PATH
    (package / "encoding").mkdir(parents=True)
    (package / "encoding" / "observation.py").write_text("", encoding="utf-8")
    readings = read_stations(tmp_path)
    assert len(readings) == 11
    assert readings[0].coding is StationCoding.مُرمَّزة
    assert all(
        reading.coding is StationCoding.محطة_غير_مُرمَّزة for reading in readings[1:]
    )


def test_an_absent_arabic_package_is_refused_not_read_as_no_modules(
    tmp_path: Path,
) -> None:
    with pytest.raises(PipelineStationsError, match="لم تُقرأ الشجرة لأجله"):
        read_stations(tmp_path)


def test_station_zero_is_refused_inside_the_table_by_its_own_message() -> None:
    with pytest.raises(PipelineStationsError, match="خارج الأنبوب"):
        declaration(ordinal=0)


def test_a_station_beyond_the_eleventh_is_refused() -> None:
    with pytest.raises(PipelineStationsError, match="المحطّةُ"):
        declaration(ordinal=12)


def test_a_station_may_not_name_a_package_assembly_file() -> None:
    with pytest.raises(PipelineStationsError, match="ملفَّ تجميعِ حزمة"):
        declaration(module_relative_path="encoding/__init__.py")


def test_the_epistemic_state_comes_from_its_closed_five_member_vocabulary() -> None:
    assert len(StationEpistemicState) == 5
    with pytest.raises(PipelineStationsError, match="مفردتها المغلقة"):
        declaration(epistemic_state="ظنّي")


def test_every_closed_epistemic_state_is_used_by_at_least_one_station() -> None:
    used = {reading.declaration.epistemic_state for reading in read_stations()}
    assert used == set(StationEpistemicState)


def test_no_type_here_carries_a_count_or_verdict_field() -> None:
    for declaring_type in (StationDeclaration, StationReading):
        declared = {item.name for item in fields(declaring_type)}
        for marker in ("count", "number", "total", "verdict", "birth"):
            assert not any(marker in name for name in declared), marker


def test_the_module_reads_no_kernel_authority() -> None:
    source = (
        Path(__file__).resolve().parents[2]
        / "src"
        / "alghanem"
        / "arabic"
        / "pipeline_stations.py"
    ).read_text(encoding="utf-8")
    imports = tuple(
        line for line in source.splitlines() if line.startswith(("import ", "from "))
    )
    assert imports
    assert not any("kernel" in line for line in imports)


def test_no_kernel_module_reads_this_station_table() -> None:
    for module in pkgutil.walk_packages(
        kernel_package.__path__, prefix="alghanem.kernel."
    ):
        spec = module.module_finder.find_spec(module.name)  # type: ignore[union-attr]
        assert spec is not None and spec.origin is not None
        text = Path(spec.origin).read_text(encoding="utf-8")
        for name in ("pipeline_stations", "StationReading", "read_stations"):
            assert name not in text, (module.name, name)


@pytest.mark.parametrize("card", _CARDS)
def test_this_table_changes_no_external_audit_field(card: str) -> None:
    before = json.dumps(
        audit_card(_EXAMPLES / card).to_dict(), ensure_ascii=False, sort_keys=True
    )
    read_stations()
    after = json.dumps(
        audit_card(_EXAMPLES / card).to_dict(), ensure_ascii=False, sort_keys=True
    )
    assert before == after
