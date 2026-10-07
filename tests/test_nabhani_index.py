"""فهرسُ المطابقة (النبهانيّ ↔ الوحدات): لا سطرَ يشير إلى ما لا وجودَ له — وحدةٌ غيرُ مسجَّلة، أو
مبرهنةٌ غيرُ مدقَّقة، أو اختبارٌ غيرُ موجود، كلٌّ يُرفض باسمه."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from conftest import ROOT

SPEC = importlib.util.spec_from_file_location("gen_nabhani_index",
                                              ROOT / "tools" / "gen_nabhani_index.py")
assert SPEC and SPEC.loader
MOD = importlib.util.module_from_spec(SPEC)
sys.modules["gen_nabhani_index"] = MOD
SPEC.loader.exec_module(MOD)


def test_index_is_generated_and_every_reference_exists() -> None:
    assert MOD.problems() == []
    assert (ROOT / "NABHANI_INDEX.md").read_text(encoding="utf-8") == MOD.render()
    tags = [row[5] for row in MOD.ROWS]
    assert len(MOD.ROWS) == 19 and sum(t.startswith("لا وحدة") for t in tags) == 4


def test_mutations_are_refused_by_name(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    row = MOD.ROWS[0]
    monkeypatch.setattr(MOD, "ROWS",
                        (*MOD.ROWS, (row[0], row[1], row[2], ("ontology_hierarchy",), (), "x")))
    assert MOD.problems() == ["UNKNOWN_UNIT:" + row[0] + ":ontology_hierarchy"]
    monkeypatch.setattr(MOD, "ROWS", (*MOD.ROWS[:19], (row[0], row[1], row[2], (),
                                                       ("lean:Slge.Maani.no_such_theorem",), "x")))
    assert MOD.problems() == ["UNAUDITED_THEOREM:" + row[0] + ":Slge.Maani.no_such_theorem"]
    monkeypatch.setattr(MOD, "ROWS", (*MOD.ROWS[:19],
                                      (row[0], row[1], row[2], (),
                                       ("test:tests/test_maani.py::test_invented",), "x")))
    assert MOD.problems() == ["MISSING_TEST:" + row[0] + ":tests/test_maani.py::test_invented"]
    assert isinstance(Path(MOD.AXIOMS).read_text(encoding="utf-8"), str)
