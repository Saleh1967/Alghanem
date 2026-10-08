"""سجلُّ الأرقام (`tools/gen_claims.py`): كلُّ مولِّدٍ مسمًّى موجودٌ في الشجرة، والاختزالُ إلى أرقامٍ
بمساراتها ثابت، وعددٌ في `CLAUDE.md` بلا مولِّد يُرفض باسمه (`NUMBER_WITHOUT_GENERATOR`).
لا يستدعي المولِّدات (نحو أربع دقائق)؛ ذلك عملُ `--check` في CI."""

from __future__ import annotations

import importlib
import importlib.util
import sys
from pathlib import Path

from conftest import ROOT

SPEC = importlib.util.spec_from_file_location("gen_claims", ROOT / "tools" / "gen_claims.py")
assert SPEC and SPEC.loader
MOD = importlib.util.module_from_spec(SPEC)
sys.modules["gen_claims"] = MOD
SPEC.loader.exec_module(MOD)


def test_every_generator_is_a_named_function_in_the_gate() -> None:
    gens = MOD.generators()
    assert [g[0] for g in gens][:2] == ["gate.audit.main", "gate.hamza.seat_census"]
    for name, reads, _ in gens:
        module, attr = name.rsplit(".", 1)
        assert hasattr(importlib.import_module(module), attr), name
        assert all((ROOT / r).exists() for r in reads), name


def test_root_is_expanded_and_large_maps_are_summarised() -> None:
    out: list[tuple[str, int | float]] = []
    MOD._numbers({f"k{i}": i for i in range(20)}, "", out)
    assert len(out) == 20  # الجذرُ يُفرد كلُّه
    out = []
    MOD._numbers({"big": {f"k{i}": i for i in range(20)}, "s": {3, 1}}, "", out)
    assert out == [("big.len", 20), ("big.sum", 190), ("s.len", 2)]


def test_a_number_without_generator_is_refused_by_name(monkeypatch, tmp_path: Path) -> None:  # type: ignore[no-untyped-def]
    rows = [{"generator": "g", "reads": [], "fingerprint": "f", "numbers": [("n", 18179)]}]
    claude = tmp_path / "CLAUDE.md"
    claude.write_text("READY 18,179\nADR ٧: 1,743\n", encoding="utf-8")
    monkeypatch.setattr(MOD, "ROOT", tmp_path)
    assert MOD.unbacked(rows) == []
    claude.write_text("READY 18,179 و167 مبرهنة و3,706 مرفوضة\n", encoding="utf-8")
    assert MOD.unbacked(rows) == ["CLAUDE.md:1: 3,706 — NUMBER_WITHOUT_GENERATOR"]


def test_ledger_file_names_every_generator_and_table() -> None:
    text = (ROOT / "CLAIMS.md").read_text(encoding="utf-8")
    for name, _, _ in MOD.generators():
        assert f"### `{name}`" in text, name
    for csv in (ROOT / "formal" / "a116").glob("*.csv"):
        assert f"`{csv.name}.rows`" in text, csv.name
    from gate.api import CORPUS_SHA256

    assert CORPUS_SHA256 in text
