"""دستورُ الترتيب، ومنعُ القفز في الشيفرة نفسها."""

from __future__ import annotations

import ast

import pytest

from conftest import ROOT
from slge.order import LAYERS, META, MODULE_LAYER, ancestors, build, no_leap


def test_spine_is_acyclic() -> None:
    for layer in LAYERS:
        assert layer not in ancestors(layer)
        assert all(p in LAYERS for p in LAYERS[layer])


def test_no_leap() -> None:
    with pytest.raises(PermissionError):
        build("الإعراب", {"البتات"})
    assert no_leap("الإعراب", {"الموضع"}) and build("الإعراب", {"الموضع"})
    assert not no_leap("المبنيات", {"الإملاء"})  # والدلالة شرطٌ أيضًا


def _imports(path: str) -> set[str]:
    tree = ast.parse((ROOT / "src" / "slge" / f"{path}.py").read_text(encoding="utf-8"))
    out: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.level == 1:
            if node.module:
                out.add(node.module.split(".")[0])
            else:  # from . import x
                out |= {a.name for a in node.names}
        elif isinstance(node, ast.Import):
            out |= {a.name.split(".")[1] for a in node.names if a.name.startswith("slge.")}
        elif isinstance(node, ast.ImportFrom) and (node.module or "").startswith("slge."):
            out.add((node.module or "").split(".")[1])
    return out


def test_every_module_is_on_the_spine() -> None:
    modules = {p.stem for p in (ROOT / "src" / "slge").glob("*.py")} - {"__init__"}
    assert modules == set(MODULE_LAYER) | META
    assert set(MODULE_LAYER.values()) <= set(LAYERS)


def test_modules_import_only_their_prerequisites() -> None:
    for module, layer in MODULE_LAYER.items():
        allowed = ancestors(layer)
        for dep in _imports(module) - META:
            assert MODULE_LAYER[dep] in allowed, f"{module} ({layer}) يقفز إلى {dep}"
    for module in META:
        assert _imports(module) <= META
