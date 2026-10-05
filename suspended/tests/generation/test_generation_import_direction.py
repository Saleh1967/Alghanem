"""موضعُ `generation/` من البناء: فوق محور التنفيذ، لا يستوردها منه شيء.

    prior/ → ontology/ → linguistic/ → execution/ → generation/

فإن استوردتها طبقةٌ سابقةٌ صارت صحّةُ التحليل متوقّفةً على آلة الإنتاج،
وذلك عينُ ما يمنعه `AnalysisIsNotInvertedGeneration`.

**ولا مدخلَ خفيًّا في الإنتاج**: لا وقتٌ ولا عشوائيٌّ ولا بيئةٌ ولا مسارُ ملفّ.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

import ast
from pathlib import Path

_SOURCE_ROOT = Path(__file__).resolve().parents[2] / "src" / "alghanem"

_AMBIENT_MODULES = (
    "datetime",
    "time",
    "random",
    "secrets",
    "os",
    "pathlib",
    "socket",
    "uuid",
    "json",
)

_LOWER_PACKAGES = (
    "prior",
    "ontology",
    "linguistic",
    "kernel",
    "arabic",
    "metaalgebra",
    "execution",
    "realization",
    "program",
    "encyclopedia",
)


def _imported_modules(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            modules.append("." * node.level + (node.module or ""))
        elif isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
    return modules


def _generation_modules() -> list[Path]:
    return sorted((_SOURCE_ROOT / "generation").glob("*.py"))


def test_the_generation_level_exists_as_its_own_package() -> None:
    assert _generation_modules()


def test_the_generation_level_is_read_by_no_earlier_level() -> None:
    for package in _LOWER_PACKAGES:
        directory = _SOURCE_ROOT / package
        if not directory.is_dir():
            continue
        for path in sorted(directory.rglob("*.py")):
            for module in _imported_modules(path):
                parts = module.lstrip(".").split(".")
                assert "generation" not in parts, (path.name, module)
                assert not module.startswith("alghanem.generation"), (
                    path.name,
                    module,
                )


def test_the_generation_level_reads_execution_at_one_named_place() -> None:
    permitted = {"..execution.result", "..execution.outcome"}
    for path in _generation_modules():
        for module in _imported_modules(path):
            if "execution" not in module:
                continue
            assert module in permitted, (path.name, module)


def test_the_generation_level_reads_no_analyser_and_no_kernel() -> None:
    for path in _generation_modules():
        for module in _imported_modules(path):
            assert "kernel" not in module, (path.name, module)
            assert "arabic" not in module, (path.name, module)
            assert "generated" not in module, (path.name, module)


def test_the_generation_level_reads_no_ambient_input() -> None:
    for path in _generation_modules():
        for module in _imported_modules(path):
            head = module.lstrip(".").split(".")[0]
            assert head not in _AMBIENT_MODULES, (path.name, module)


def test_the_generation_level_canonicalizes_at_one_named_place() -> None:
    for path in _generation_modules():
        text = path.read_text(encoding="utf-8")
        if "sha256" in text:  # pragma: no cover - guard
            raise AssertionError(f"بصمةٌ ثانيةٌ تُحسَب في {path.name}")
