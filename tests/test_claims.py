"""سجلُّ الأرقام (`tools/gen_claims.py`): الاختزالُ إلى أرقامٍ بمساراتها، وثباتُ البصمة على ترتيب
المجموعات، ورفضُ عددٍ في `CLAUDE.md` لا مولِّدَ له باسمه (`NUMBER_WITHOUT_GENERATOR`).
لا يستدعي `measure()` (سبعُ دقائق)؛ ذلك عملُ `--check` في CI."""

from __future__ import annotations

import importlib.util
import sys
from collections import Counter
from pathlib import Path

from conftest import ROOT

SPEC = importlib.util.spec_from_file_location("gen_claims", ROOT / "tools" / "gen_claims.py")
assert SPEC and SPEC.loader
MOD = importlib.util.module_from_spec(SPEC)
sys.modules["gen_claims"] = MOD
SPEC.loader.exec_module(MOD)


def test_numbers_are_reduced_with_their_paths() -> None:
    out: list[tuple[str, int | float]] = []
    big = Counter({f"k{i}": i for i in range(20)})
    MOD._numbers({"a": 3, "b": [1, 2], "c": {"d": 0.5}, "big": big, "s": {1, 2, 3}, "t": "x"},
                 "", out)
    assert out == [("a", 3), ("b[0]", 1), ("b[1]", 2), ("c.d", 0.5), ("big.len", 20),
                   ("big.sum", 190), ("s.len", 3)]


def test_fingerprint_ignores_set_order_and_counter_type() -> None:
    a = MOD._canon({"x": {3, 1, 2}, "y": Counter({"b": 1, "a": 2})})
    b = MOD._canon({"y": {"a": 2, "b": 1}, "x": frozenset({2, 3, 1})})
    assert a == b == {"x": [1, 2, 3], "y": {"a": 2, "b": 1}}


def test_every_generator_reads_registered_deposits_only() -> None:
    tools = sorted((ROOT / "tools").glob("gen_*_index.py"))
    with_measure = [t for t in tools if "\ndef measure(" in t.read_text(encoding="utf-8")]
    assert len(with_measure) == 45
    registered = {d.path for d in MOD.DEPOSITS}
    for t in with_measure:
        assert set(MOD._reads(t)) <= registered


def test_a_number_without_generator_is_refused_by_name(monkeypatch, tmp_path: Path) -> None:  # type: ignore[no-untyped-def]
    rows = [{"generator": "g", "reads": [], "fingerprint": "f", "numbers": [("n", 4561)]}]
    claude = tmp_path / "CLAUDE.md"
    claude.write_text("فيه 4,561 جذرًا\nوفي ADR ٧: 1,743 صورةً\n", encoding="utf-8")
    monkeypatch.setattr(MOD, "ROOT", tmp_path)
    assert MOD.unbacked(rows) == []
    claude.write_text("فيه 4,561 جذرًا و19,216 ملفًا\n", encoding="utf-8")
    assert MOD.unbacked(rows) == ["CLAUDE.md:1: 19,216 — NUMBER_WITHOUT_GENERATOR"]


def test_ledger_file_exists_and_names_every_generator() -> None:
    text = (ROOT / "CLAIMS.md").read_text(encoding="utf-8")
    for t in (ROOT / "tools").glob("gen_*_index.py"):
        if "\ndef measure(" in t.read_text(encoding="utf-8"):
            assert f"### `tools/{t.name}::measure`" in text, t.name
    assert MOD.a116_rev() in text
    for d in MOD.DEPOSITS:
        assert f"`{d.path}`" in text
