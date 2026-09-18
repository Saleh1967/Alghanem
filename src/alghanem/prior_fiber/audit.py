"""`G0.FIBER-0.AUDIT`: فحصُ العزل الاستيراديّ وفحصُ حياد المفردات.

العزلُ يُقاس على الاستيرادات المُصرَّحة في مصدر هذه الحزمة وما تبلغه عبرها من
وحدات `alghanem`، لا على `sys.modules` وقتَ التشغيل. والاستيرادُ النسبيُّ يُحَلُّ
إلى موضعه المطلق قبل الحكم، وإلّا صار العزلُ دعوى تُخرَق بنقطةٍ واحدة.

والحيادُ يُفحَص على الأسماء: لا يظهر في هذه الطبقة لسانٌ بعينه ولا مادّةُ مجالٍ
ولا اسمُ نظامٍ من الأنظمة التي ستقرأ عقدَها.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, fields, is_dataclass
from enum import Enum
from pathlib import Path
from types import ModuleType

from .laws import (
    AN_ADAPTER_FLOWS_INTO_THE_FIBER_NOT_THE_REVERSE,
    NO_SYSTEM_DEFINES_THE_CONTRACT_IT_IS_READ_BY,
    PriorFiberError,
)

__all__ = [
    "FORBIDDEN_ALGHANEM_PACKAGES",
    "FORBIDDEN_NAME_FRAGMENTS",
    "PERMITTED_ALGHANEM_MODULES",
    "FiberImportIsolationReport",
    "FiberVocabularyReport",
    "fiber_import_isolation_audit",
    "fiber_vocabulary_audit",
]

FORBIDDEN_ALGHANEM_PACKAGES: tuple[str, ...] = (
    "arabic",
    "kernel",
    "linguistic",
    "realization",
    "ontology",
    "metaalgebra",
    "structural_dal",
    "fractal_generation",
    "fractal_experiment",
    "generation",
    "program",
    "execution",
    "encyclopedia",
)
"""حزمٌ لا تُستورد من هذه الطبقة: مادّةُ مجالٍ، وسلطةُ نواةٍ، وأيُّ نظامٍ سيقرأ العقد."""

PERMITTED_ALGHANEM_MODULES: tuple[str, ...] = (
    "canonical_content",
    "prior",
    "prior_fiber",
)
"""ما يجوز بلوغُه: البصمةُ القانونيّة، وقاعدةُ المعلومات السابقة، والحزمةُ نفسُها."""

FORBIDDEN_NAME_FRAGMENTS: tuple[str, ...] = (
    "arabic",
    "madlul",
    "dalal",
    "lafz",
    "root",
    "wazn",
    "letter",
    "haraka",
    "lexic",
    "morph",
    "nahw",
)
"""شظايا أسماءٍ لمجالٍ بعينه؛ ممنوعةٌ في طبقةٍ محايدةٍ عن المجالات."""

_SOURCE_ROOT = Path(__file__).resolve().parent
_ALGHANEM_ROOT = _SOURCE_ROOT.parent
_FIBER_MODULES = (
    "__init__.py",
    "audit.py",
    "contract.py",
    "fibers.py",
    "laws.py",
    "node.py",
)


@dataclass(frozen=True, slots=True)
class FiberImportIsolationReport:
    """تقريرُ العزل: ما فُحص، وما بُلِغ، وما خالف."""

    scanned_files: tuple[str, ...]
    alghanem_imports: tuple[str, ...]
    violations: tuple[str, ...]

    @property
    def is_isolated(self) -> bool:
        """هل خلا المصدرُ وما بلغه من كلِّ حزمةٍ ممنوعة؟"""

        return not self.violations

    @property
    def refusal(self) -> str:
        """قانونُ اتّجاه المُحوِّل: المجالُ يدخل إلى الليف ولا يُستورَد منه."""

        return AN_ADAPTER_FLOWS_INTO_THE_FIBER_NOT_THE_REVERSE

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التقرير للعرض."""

        return {
            "scanned_files": list(self.scanned_files),
            "alghanem_imports": list(self.alghanem_imports),
            "violations": list(self.violations),
            "is_isolated": self.is_isolated,
        }


@dataclass(frozen=True, slots=True)
class FiberVocabularyReport:
    """تقريرُ الحياد: ما فُحص من أسماء، وما خالف منها."""

    inspected_names: tuple[str, ...]
    violations: tuple[str, ...]

    @property
    def is_neutral(self) -> bool:
        """هل خلت الأسماءُ من كلِّ شظيّة مجالٍ بعينه؟"""

        return not self.violations

    @property
    def refusal(self) -> str:
        """قانونُ حياد العقد عن الأنظمة والمجالات."""

        return NO_SYSTEM_DEFINES_THE_CONTRACT_IT_IS_READ_BY

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التقرير للعرض."""

        return {
            "inspected_name_count": len(self.inspected_names),
            "violations": list(self.violations),
            "is_neutral": self.is_neutral,
        }


def _dotted_of(path: Path) -> str:
    relative = path.relative_to(_ALGHANEM_ROOT)
    parts = relative.with_suffix("").parts
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(("alghanem", *parts))


def _resolve(module: str, level: int, path: Path) -> str:
    if level == 0:
        return module
    package = _dotted_of(path)
    if path.name != "__init__.py":
        package = package.rsplit(".", 1)[0]
    anchor = package.split(".")
    if level > 1:
        anchor = anchor[: -(level - 1)]
    if not anchor:
        raise PriorFiberError("استيرادٌ نسبيٌّ يتجاوز جذرَ الحزمة")
    return ".".join((*anchor, module)) if module else ".".join(anchor)


def _declared_imports(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            modules.append(_resolve(node.module or "", node.level, path))
        elif isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
    return modules


def _module_files(dotted: str) -> list[Path]:
    relative = Path(*dotted.split(".")[1:])
    module_path = _ALGHANEM_ROOT / relative.with_suffix(".py")
    package_dir = _ALGHANEM_ROOT / relative
    if module_path.is_file():
        return [module_path]
    if package_dir.is_dir():
        return sorted(package_dir.rglob("*.py"))
    return []


def fiber_import_isolation_audit() -> FiberImportIsolationReport:
    """افحص العزلَ على مصدر الحزمة وما تبلغه من وحدات `alghanem`."""

    scanned: list[str] = []
    reached: list[str] = []
    violations: list[str] = []
    pending = [_SOURCE_ROOT / name for name in _FIBER_MODULES]
    seen: set[Path] = set()
    while pending:
        path = pending.pop(0)
        if path in seen or not path.is_file():
            continue
        seen.add(path)
        scanned.append(str(path.relative_to(_ALGHANEM_ROOT)))
        for module in _declared_imports(path):
            if not module.startswith("alghanem"):
                continue
            head = module.split(".")[1] if "." in module else ""
            if head in FORBIDDEN_ALGHANEM_PACKAGES:
                violations.append(f"{path.name} -> {module}")
                continue
            if head and head not in PERMITTED_ALGHANEM_MODULES:
                violations.append(f"{path.name} -> {module}")
                continue
            reached.append(module)
            pending.extend(_module_files(module))
    return FiberImportIsolationReport(
        scanned_files=tuple(sorted(set(scanned))),
        alghanem_imports=tuple(sorted(set(reached))),
        violations=tuple(sorted(set(violations))),
    )


def _inspected_names(module: ModuleType) -> list[str]:
    names: list[str] = []
    for attribute_name in getattr(module, "__all__", ()):
        attribute = getattr(module, attribute_name, None)
        if attribute is None:
            continue
        if isinstance(attribute, type) and issubclass(attribute, Enum):
            names.append(attribute.__name__)
            names.extend(member.name for member in attribute)
            continue
        if isinstance(attribute, type) and is_dataclass(attribute):
            names.append(attribute.__name__)
            names.extend(field.name for field in fields(attribute))
            continue
        if isinstance(attribute, type) or callable(attribute):
            names.append(attribute_name)
    return names


def fiber_vocabulary_audit(*modules: ModuleType) -> FiberVocabularyReport:
    """افحص حيادَ الأسماء المُصدَّرة من وحدات هذه الطبقة."""

    inspected: list[str] = []
    violations: list[str] = []
    for module in modules:
        for name in _inspected_names(module):
            inspected.append(name)
            lowered = name.lower()
            for fragment in FORBIDDEN_NAME_FRAGMENTS:
                if fragment in lowered:
                    violations.append(f"{module.__name__}:{name} -> {fragment}")
    return FiberVocabularyReport(
        inspected_names=tuple(sorted(set(inspected))),
        violations=tuple(sorted(set(violations))),
    )
