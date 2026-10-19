"""موضعُ `fractal_generation/` من البناء: نواةٌ مستقلّةٌ لا تستورد سواها.

الحارسُ الصحيحُ هنا واحد:

    FractalCore  imports only  canonical_content

وهو حارسٌ على النواة نفسِها لا على مستهلكيها: `ArabicAdapter → FractalCore`
مسموحٌ ومقصودٌ لاحقًا، و`FractalCore → ArabicAdapter` ممنوعٌ أبدًا.

ويُمنَع كذلك أن تستوردها الطبقاتُ الأدنى **القائمةُ اليوم**، لأنّ استيرادَها
منها يقلب اتّجاه البناء؛ وليس في ذلك حظرٌ على مستهلكٍ مستقبليٍّ لم يُكتَب بعد.

**ولا مدخلَ خفيّ**: لا وقتٌ ولا عشوائيٌّ ولا بيئةٌ ولا مسارُ ملفّ.

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

_CURRENT_LOWER_PACKAGES = (
    "kernel",
    "prior",
    "ontology",
    "metaalgebra",
    "execution",
    "program",
)

_FORBIDDEN_SIBLINGS = (
    "generation",
    "arabic",
    "linguistic",
    "realization",
    "kernel",
    "encyclopedia",
    "program",
    "execution",
    "ontology",
    "prior",
    "metaalgebra",
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


def _fractal_modules() -> list[Path]:
    return sorted((_SOURCE_ROOT / "fractal_generation").glob("*.py"))


def test_the_fractal_level_exists_as_its_own_package() -> None:
    names = {path.name for path in _fractal_modules()}
    assert {
        "__init__.py",
        "authority_gaps.py",
        "branch.py",
        "closure.py",
        "expansion.py",
        "laws.py",
        "lift.py",
        "node.py",
        "pattern.py",
        "scale.py",
        "trace.py",
    } <= names


def test_the_fractal_core_reads_only_canonical_content_from_alghanem() -> None:
    for path in _fractal_modules():
        for module in _imported_modules(path):
            if module.startswith(".."):
                head = module.lstrip(".").split(".")[0]
                assert head == "canonical_content", (path.name, module)
            elif not module.startswith("."):
                assert not module.startswith("alghanem"), (path.name, module)


def test_the_fractal_core_reads_no_sibling_layer() -> None:
    for path in _fractal_modules():
        for module in _imported_modules(path):
            parts = module.lstrip(".").split(".")
            for sibling in _FORBIDDEN_SIBLINGS:
                assert sibling not in parts, (path.name, module)


def test_no_currently_lower_layer_reads_the_fractal_core() -> None:
    for package in _CURRENT_LOWER_PACKAGES:
        directory = _SOURCE_ROOT / package
        if not directory.is_dir():
            continue
        for path in sorted(directory.rglob("*.py")):
            for module in _imported_modules(path):
                parts = module.lstrip(".").split(".")
                assert "fractal_generation" not in parts, (path.name, module)


def test_the_fractal_core_reads_no_ambient_input() -> None:
    for path in _fractal_modules():
        for module in _imported_modules(path):
            head = module.lstrip(".").split(".")[0]
            assert head not in _AMBIENT_MODULES, (path.name, module)


def test_the_fractal_core_canonicalizes_at_one_named_place() -> None:
    for path in _fractal_modules():
        text = path.read_text(encoding="utf-8")
        if "sha256" in text:  # pragma: no cover - guard
            raise AssertionError(f"بصمةٌ ثانيةٌ تُحسَب في {path.name}")


def test_a_future_consumer_of_the_core_is_not_forbidden_here() -> None:
    source = Path(__file__).read_text(encoding="utf-8")
    assert "ArabicAdapter → FractalCore" in source
    assert "FractalCore → ArabicAdapter" in source
