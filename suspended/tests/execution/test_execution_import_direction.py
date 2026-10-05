"""موضعُ `execution/` من البناء: فوق محور الوجود، لا يستوردها منه شيء.

    prior/ → ontology/ → linguistic/anchored_v3.py → execution/

فإن استوردتها طبقةٌ سابقةٌ صار بقاءُ معناها متوقّفًا على وجود محرّك التنفيذ،
وذلك عينُ ما قام الفصلُ لمنعه. وتقرأ هذه الطبقةُ من الجبر موضعًا واحدًا
مُسمًّى: `linguistic/anchored_v3.py` و`linguistic/nisbah.py`، لا الحزمةَ كلَّها.

**ولا مدخلَ خفيًّا في المحرّك** (`SameInputSameLawsSameResult`): لا وقتٌ ولا
عشوائيٌّ ولا بيئةٌ ولا مسارُ ملفّ؛ فما لم يُصرَّح به لا يدخل في الحكم.

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

_LOWER_PACKAGES = ("prior", "ontology", "linguistic", "kernel", "arabic", "metaalgebra")


def _imported_modules(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            modules.append("." * node.level + (node.module or ""))
        elif isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
    return modules


def _execution_modules() -> list[Path]:
    return sorted((_SOURCE_ROOT / "execution").glob("*.py"))


def test_the_execution_level_is_read_by_no_earlier_level() -> None:
    for package in _LOWER_PACKAGES:
        for path in sorted((_SOURCE_ROOT / package).rglob("*.py")):
            for module in _imported_modules(path):
                parts = module.lstrip(".").split(".")
                assert "execution" not in parts, (path.name, module)
                assert not module.startswith("alghanem.execution"), (
                    path.name,
                    module,
                )


def test_the_execution_level_reads_the_algebra_at_one_named_place() -> None:
    permitted = {"..linguistic.anchored_v3", "..linguistic.nisbah"}
    for path in _execution_modules():
        for module in _imported_modules(path):
            if "linguistic" not in module:
                continue
            if "ontology.linguistic" in module:
                continue
            assert module in permitted, (path.name, module)


def test_the_execution_level_reads_no_generated_tree_and_no_kernel() -> None:
    for path in _execution_modules():
        for module in _imported_modules(path):
            assert "generated" not in module, (path.name, module)
            assert "kernel" not in module, (path.name, module)
            assert "arabic" not in module, (path.name, module)


def test_the_execution_level_reads_no_ambient_input() -> None:
    for path in _execution_modules():
        for module in _imported_modules(path):
            head = module.lstrip(".").split(".")[0]
            assert head not in _AMBIENT_MODULES, (path.name, module)


def test_the_execution_level_canonicalizes_at_one_named_place() -> None:
    for path in _execution_modules():
        text = path.read_text(encoding="utf-8")
        if "sha256" in text:  # pragma: no cover - guard
            raise AssertionError(f"بصمةٌ ثانيةٌ تُحسَب في {path.name}")
