"""موضعُ `fractal_experiment/` من البناء: طبقةٌ فوق النواة لا داخلَها.

    fractal_experiment  →  fractal_generation
    fractal_generation  ↛  fractal_experiment

وهي لا تستورد سوى `canonical_content` و`fractal_generation`؛ ولا تستوردها
النواةُ ولا الطبقاتُ الأدنى. **ولا مدخلَ خفيّ**: لا وقتٌ ولا عشوائيٌّ ولا بيئةٌ
ولا مسارُ ملفّ.

تسجيلٌ لا سلطة: لا ترخيصَ، ولا رتبةَ دائمة، ولا حكمَ كفاية.
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

_ALLOWED_PACKAGES = ("canonical_content", "fractal_generation")

_LICENSING_NAMES = (
    "LicensedPattern",
    "LicensedTransition",
    "LicensedScaleLift",
    "ArabicRuleLicense",
    "SufficiencyAssessment",
    "LicensingCandidate",
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


def _experiment_modules() -> list[Path]:
    return sorted((_SOURCE_ROOT / "fractal_experiment").glob("*.py"))


def test_the_experimental_layer_exists_as_its_own_package() -> None:
    names = {path.name for path in _experiment_modules()}
    assert {
        "__init__.py",
        "authority.py",
        "authority_gaps.py",
        "binding.py",
        "bundle.py",
        "laws.py",
        "lift.py",
        "transition.py",
        "witness.py",
    } <= names


def test_the_experimental_layer_reads_only_the_core_and_canonical_content() -> None:
    for path in _experiment_modules():
        for module in _imported_modules(path):
            if module.startswith(".."):
                head = module.lstrip(".").split(".")[0]
                assert head in _ALLOWED_PACKAGES, (path.name, module)
            elif not module.startswith("."):
                assert not module.startswith("alghanem"), (path.name, module)


def test_the_core_does_not_read_the_experimental_layer() -> None:
    for path in sorted((_SOURCE_ROOT / "fractal_generation").glob("*.py")):
        for module in _imported_modules(path):
            parts = module.lstrip(".").split(".")
            assert "fractal_experiment" not in parts, (path.name, module)


def test_the_experimental_layer_reads_no_ambient_input() -> None:
    for path in _experiment_modules():
        for module in _imported_modules(path):
            head = module.lstrip(".").split(".")[0]
            assert head not in _AMBIENT_MODULES, (path.name, module)


def test_the_experimental_layer_canonicalizes_at_one_named_place() -> None:
    for path in _experiment_modules():
        text = path.read_text(encoding="utf-8")
        if "sha256" in text:  # pragma: no cover - guard
            raise AssertionError(f"بصمةٌ ثانيةٌ تُحسَب في {path.name}")


def test_the_experimental_layer_declares_no_licensing_type() -> None:
    for path in _experiment_modules():
        text = path.read_text(encoding="utf-8")
        for name in _LICENSING_NAMES:
            assert f"class {name}" not in text, (path.name, name)


def test_the_experimental_layer_does_not_read_the_arabic_layer() -> None:
    for path in _experiment_modules():
        for module in _imported_modules(path):
            parts = module.lstrip(".").split(".")
            assert "arabic" not in parts, (path.name, module)
            assert "kernel" not in parts, (path.name, module)
