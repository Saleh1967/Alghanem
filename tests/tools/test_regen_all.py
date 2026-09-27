"""اختبارُ البوّابة نفسِها: أتصادِم فعلًا، وتُسمّي، ولا تحمل نسخةً ثانية؟"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
GATE_PATH = REPO_ROOT / "tools" / "regen_all.py"


def _load_gate() -> ModuleType:
    spec = importlib.util.spec_from_file_location("regen_all", GATE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("لا تُحمَّل البوّابةُ من مسارها.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


gate = _load_gate()


def test_no_guarded_figure_has_drifted_from_its_generator() -> None:
    drifted = [
        (report.figure, reading.field, reading.transcribed, reading.measured)
        for report in gate.the_registry()
        for reading in report.discrepancies
    ]
    assert drifted == []


def test_the_gate_returns_zero_only_when_nothing_drifted() -> None:
    assert gate.main(["--check"]) == 0


def test_every_figure_is_named_by_one_of_the_three_genera() -> None:
    genera = {report.genus for report in gate.the_registry()}
    assert genera <= {gate.GATE, gate.PROSE, gate.WITNESS}
    assert gate.GATE in genera
    assert gate.PROSE in genera
    assert gate.WITNESS in genera


def test_a_witness_is_listed_and_never_collided() -> None:
    witnesses = [
        report for report in gate.the_registry() if report.genus == gate.WITNESS
    ]
    assert witnesses
    for report in witnesses:
        assert report.readings
        assert report.discrepancies == ()


def test_a_gate_without_a_field_it_guards_is_refused() -> None:
    with pytest.raises(gate.RegenerationError):
        gate.FigureReport(
            figure="بوّابةٌ خاوية",
            genus=gate.GATE,
            source="لا شيء",
            readings=(),
        )


def test_an_undeclared_genus_is_refused() -> None:
    with pytest.raises(gate.RegenerationError):
        gate.FigureReport(
            figure="جنسٌ مُختلَق",
            genus="[عرض]",
            source="لا شيء",
            readings=(gate.FieldReading("حقل", "1", "1"),),
        )


def test_a_collision_refuses_two_sides_that_do_not_name_the_same_fields() -> None:
    with pytest.raises(gate.RegenerationError):
        gate._collide(
            figure="جانبان لا يلتقيان",
            source="اختبار",
            transcribed={"a": 1},
            measured={"b": 1},
        )


def test_a_named_difference_is_rendered_and_not_swallowed() -> None:
    report = gate.FigureReport(
        figure="فارقٌ مُصطنَع",
        genus=gate.GATE,
        source="اختبار",
        readings=(gate.FieldReading("حقل", "1", "2"),),
    )
    rendered = "\n".join(gate.render((report,)))
    assert "حقل" in rendered
    assert "1" in rendered and "2" in rendered
    assert report.discrepancies
