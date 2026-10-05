"""الحارس: لا قارئَ للنصّ في SLGE، والمعلَّق غيرُ قابلٍ للاستيراد، والسجلُّ مطابقٌ للشجرة."""

from __future__ import annotations

import importlib
import importlib.util
import json

from conftest import ROOT
from slge.guard import breaches


def test_no_breach_in_the_tree() -> None:
    assert breaches() == []


def test_a_planted_reader_is_caught() -> None:
    planted = ROOT / "src" / "slge" / "zz_planted.py"
    planted.write_text("def f(p):\n    return open(p).read()\n", encoding="utf-8")
    try:
        assert any(b.path.endswith("zz_planted.py") and b.what == "open" for b in breaches())
    finally:
        planted.unlink()


def test_suspended_is_not_importable() -> None:
    gone = ("slge.encoding", "slge.orthography", "slge.lexicon", "slge.morphology", "suspended.src")
    for name in gone:
        try:
            importlib.import_module(name)
        except ImportError:
            continue
        raise AssertionError(f"{name} ما زال قابلًا للاستيراد")


def test_registry_matches_suspended_tree() -> None:
    src = ROOT / "tools" / "gen_registry.py"
    spec = importlib.util.spec_from_file_location("gen_registry", src)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    registry = (ROOT / "SUSPENDED_REGISTRY.json").read_text(encoding="utf-8")
    assert mod.render() == registry
    units = json.loads(registry)["units"]
    assert units and all(u["reason"] and u["re_admit_requires"] for u in units)
