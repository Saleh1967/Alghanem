"""اتّجاهُ محور الموجودات أحاديّ: `prior → ontology`، ولا ينعكس ولا يتجاوز.

    prior/     →  ontology/      (محورُ الموجودات)
    metaalgebra/ → linguistic/ → arabic/   (محورُ الجبر)

والمستوى السابقُ لا يستورد اللاحقَ ولا يستورد شيئًا من محور الجبر؛ فطبقةٌ
أنطولوجيّةٌ تقرأ جبرًا طبقةٌ وُلِدت من جبرٍ، وذلك عينُ ما قام هذا المستوى
لمنعه (`TheAlgebraDoesNotCreateItsObjects`).
"""

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


def _modules_of(package: str) -> list[Path]:
    return sorted((_SOURCE_ROOT / package).glob("*.py"))


_FORBIDDEN_FOR_PRIOR = ("ontology", "linguistic", "metaalgebra", "arabic", "kernel")
_FORBIDDEN_FOR_ONTOLOGY = ("linguistic.", "metaalgebra", "arabic", "kernel")


def test_the_prior_level_reads_no_later_level() -> None:
    for path in _modules_of("prior"):
        for module in _imported_modules(path):
            for forbidden in _FORBIDDEN_FOR_PRIOR:
                assert forbidden not in module, (path.name, module)


def test_the_ontology_level_reads_no_algebra() -> None:
    for path in _modules_of("ontology"):
        for module in _imported_modules(path):
            for forbidden in _FORBIDDEN_FOR_ONTOLOGY:
                assert forbidden not in module, (path.name, module)


def test_the_ontology_level_may_read_the_prior_level() -> None:
    general = _SOURCE_ROOT / "ontology" / "general.py"
    assert any("prior" in module for module in _imported_modules(general))


def test_no_generated_tree_is_read_by_either_level() -> None:
    for package in ("prior", "ontology"):
        for path in _modules_of(package):
            for module in _imported_modules(path):
                assert "generated" not in module, (path.name, module)


def test_no_kernel_module_reads_the_new_levels() -> None:
    for path in _modules_of("kernel"):
        for module in _imported_modules(path):
            assert "prior" not in module, (path.name, module)
            assert "ontology" not in module, (path.name, module)


def test_the_linguistic_nucleus_is_not_touched_by_this_deposit() -> None:
    for path in _modules_of("linguistic"):
        for module in _imported_modules(path):
            assert "prior" not in module, (path.name, module)
            assert "ontology" not in module, (path.name, module)


def test_the_metaalgebra_reads_neither_new_level() -> None:
    for path in _modules_of("metaalgebra"):
        for module in _imported_modules(path):
            assert "prior" not in module, (path.name, module)
            assert "ontology" not in module, (path.name, module)
