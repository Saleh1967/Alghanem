"""الحارس: لا خرقَ في الشجرة، ويلتقط خرقًا مزروعًا."""

from __future__ import annotations

from conftest import ROOT

from gate.guard import breaches


def test_tree_has_no_breach() -> None:
    assert breaches() == []


def test_guard_catches_a_planted_breach(tmp_path, monkeypatch) -> None:
    planted = ROOT / "zz_planted.py"
    planted.write_text("open('x').read()\nimport suspended.src\n", encoding="utf-8")
    try:
        b = breaches()
    finally:
        planted.unlink()
    assert {x.what for x in b} >= {"open", "import suspended.src"}


def test_suspended_is_not_importable() -> None:
    import importlib

    for name in ("alghanem", "canonical116", "suspended.src.alghanem"):
        try:
            importlib.import_module(name)
        except ImportError:
            continue
        raise AssertionError(f"{name} ما زال قابلًا للاستيراد")


def test_registry_matches_suspended_tree() -> None:
    """السجلُّ مولَّدٌ لا محرَّر: كلُّ وحدةٍ في `suspended/` مسجَّلةٌ بسببها وشرطِ عودتها."""

    import importlib.util
    import json

    src = ROOT / "tools" / "gen_registry.py"
    spec = importlib.util.spec_from_file_location("gen_registry", src)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert mod.render() == (ROOT / "SUSPENDED_REGISTRY.json").read_text(encoding="utf-8")
    units = json.loads((ROOT / "SUSPENDED_REGISTRY.json").read_text(encoding="utf-8"))["units"]
    assert units and all(u["reason"] and u["re_admit_requires"] for u in units)
