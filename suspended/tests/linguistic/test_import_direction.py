"""اتّجاهُ التبعيّة أحاديّ: `metaalgebra → linguistic → arabic`، ولا ينعكس."""

from __future__ import annotations

import ast
from pathlib import Path

_SOURCE_ROOT = Path(__file__).resolve().parents[2] / "src" / "alghanem"


def _imported_modules(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            prefix = "." * node.level
            modules.append(prefix + (node.module or ""))
        elif isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
    return modules


def _linguistic_modules() -> list[Path]:
    return sorted((_SOURCE_ROOT / "linguistic").glob("*.py"))


def test_the_linguistic_nucleus_never_imports_the_arabic_layer() -> None:
    for path in _linguistic_modules():
        for module in _imported_modules(path):
            assert "arabic" not in module, (path.name, module)


def test_the_linguistic_nucleus_never_imports_the_kernel() -> None:
    for path in _linguistic_modules():
        for module in _imported_modules(path):
            assert "kernel" not in module, (path.name, module)


def test_the_linguistic_nucleus_never_imports_the_generated_tree() -> None:
    for path in _linguistic_modules():
        for module in _imported_modules(path):
            assert "generated" not in module, (path.name, module)


def test_the_metaalgebra_never_imports_the_linguistic_nucleus() -> None:
    for path in sorted((_SOURCE_ROOT / "metaalgebra").glob("*.py")):
        for module in _imported_modules(path):
            assert "linguistic" not in module, (path.name, module)


def test_the_arabic_layer_may_import_the_linguistic_nucleus() -> None:
    relativization = _SOURCE_ROOT / "arabic" / "nisbah_relativization.py"
    modules = _imported_modules(relativization)
    assert any("linguistic" in module for module in modules)


def test_no_kernel_module_reads_the_linguistic_nucleus() -> None:
    for path in sorted((_SOURCE_ROOT / "kernel").glob("*.py")):
        for module in _imported_modules(path):
            assert "linguistic" not in module, (path.name, module)
