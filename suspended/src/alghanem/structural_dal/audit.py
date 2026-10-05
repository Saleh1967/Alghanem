"""`G0.SDAL-0.AUDIT`: فحصُ العزل الاستيراديّ وفحصُ المفردات.

العزلُ يُقاس على الاستيرادات المُصرَّحة في مصدر هذه الحزمة وما تبلغه عبرها من
وحدات `alghanem`، لا على `sys.modules` وقتَ التشغيل؛ فإنّ حزمةً أخرى قد
تُحمَّل في الجلسة عينِها لسببٍ لا يخصُّ هذه الطبقة.

والمفرداتُ تُفحَص على الأسماء: أسماءُ الأنواع، وحقولُها، وأعضاءُ مفرداتها
المغلقة؛ فلا يظهر فيها جذرٌ ولا وزنٌ ولا معنًى ولا معجمٌ ولا لسانٌ بعينه.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, fields, is_dataclass
from enum import Enum
from pathlib import Path
from types import ModuleType

from .laws import (
    NO_LINGUISTIC_VOCABULARY_IN_THE_ZERO_ONE_ALGEBRA,
    StructuralDalError,
)

__all__ = [
    "FORBIDDEN_ALGHANEM_PACKAGES",
    "FORBIDDEN_NAME_FRAGMENTS",
    "PERMITTED_ALGHANEM_MODULES",
    "ImportIsolationReport",
    "VocabularyAuditReport",
    "import_isolation_audit",
    "vocabulary_audit",
]

FORBIDDEN_ALGHANEM_PACKAGES: tuple[str, ...] = (
    "arabic",
    "kernel",
    "linguistic",
    "realization",
    "ontology",
    "prior",
    "metaalgebra",
    "generation",
    "program",
    "execution",
    "encyclopedia",
    "fractal_experiment",
)
"""حزمٌ لا تُستورد من هذه الطبقة: لسانٌ، ومعجمٌ، وسلطةُ نواةٍ، وطبقةُ دلالة."""

PERMITTED_ALGHANEM_MODULES: tuple[str, ...] = (
    "canonical_content",
    "fractal_generation",
    "structural_dal",
)
"""ما يجوز بلوغُه من `alghanem`: البصمةُ القانونيّة، والنواةُ الفراكتاليّة، والحزمةُ نفسُها."""

FORBIDDEN_NAME_FRAGMENTS: tuple[str, ...] = (
    "root",
    "weight",
    "wazn",
    "jidhr",
    "meaning",
    "madlul",
    "dalal",
    "signif",
    "ifada",
    "benefit",
    "isnad",
    "lexic",
    "maqayis",
    "morph",
    "affix",
    "augment",
    "arabic",
    "letter",
    "haraka",
    "syllable",
)
"""شظايا أسماءٍ لغويّةٍ ممنوعةٌ في مفردات هذا الطور."""

_SOURCE_ROOT = Path(__file__).resolve().parent
_ALGHANEM_ROOT = _SOURCE_ROOT.parent
_ALGEBRA_MODULES = (
    "__init__.py",
    "audit.py",
    "hypothesis.py",
    "induction.py",
    "laws.py",
    "residual.py",
    "slots.py",
    "space.py",
    "transition.py",
)


@dataclass(frozen=True, slots=True)
class ImportIsolationReport:
    """تقريرُ العزل: ما فُحص، وما استُورد، وما خالف."""

    scanned_files: tuple[str, ...]
    alghanem_imports: tuple[str, ...]
    violations: tuple[str, ...]

    @property
    def is_isolated(self) -> bool:
        """هل خلا المصدرُ وما بلغه من كلِّ حزمةٍ ممنوعة؟"""

        return not self.violations

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التقرير للعرض."""

        return {
            "scanned_files": list(self.scanned_files),
            "alghanem_imports": list(self.alghanem_imports),
            "violations": list(self.violations),
            "is_isolated": self.is_isolated,
        }


@dataclass(frozen=True, slots=True)
class VocabularyAuditReport:
    """تقريرُ المفردات: ما فُحص من أسماء، وما خالف منها."""

    inspected_names: tuple[str, ...]
    violations: tuple[str, ...]

    @property
    def is_clean(self) -> bool:
        """هل خلت الأسماءُ من كلِّ شظيّةٍ لغويّة؟"""

        return not self.violations

    @property
    def refusal(self) -> str:
        """قانونُ خلوِّ هذه الطبقة من المفردات اللغويّة."""

        return NO_LINGUISTIC_VOCABULARY_IN_THE_ZERO_ONE_ALGEBRA

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التقرير للعرض."""

        return {
            "inspected_name_count": len(self.inspected_names),
            "violations": list(self.violations),
            "is_clean": self.is_clean,
        }


def _declared_imports(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            modules.append("." * node.level + (node.module or ""))
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


def import_isolation_audit() -> ImportIsolationReport:
    """افحص العزلَ على مصدر الحزمة وما تبلغه من وحدات `alghanem`."""

    scanned: list[str] = []
    reached: list[str] = []
    violations: list[str] = []
    pending = [_SOURCE_ROOT / name for name in _ALGEBRA_MODULES]
    seen: set[Path] = set()
    while pending:
        path = pending.pop(0)
        if path in seen or not path.is_file():
            continue
        seen.add(path)
        scanned.append(str(path.relative_to(_ALGHANEM_ROOT)))
        for module in _declared_imports(path):
            if module.startswith("."):
                continue
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
    return ImportIsolationReport(
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


def vocabulary_audit() -> VocabularyAuditReport:
    """افحص أسماءَ الأنواع والحقول والأعضاء؛ ولا تفحص النصوصَ الشارحة."""

    from . import audit, hypothesis, induction, laws, residual, slots, transition

    inspected: list[str] = []
    for module in (laws, residual, slots, hypothesis, transition, induction, audit):
        inspected.extend(_inspected_names(module))
    violations = tuple(
        sorted(
            {
                name
                for name in inspected
                for fragment in FORBIDDEN_NAME_FRAGMENTS
                if fragment in name.lower()
            }
        )
    )
    return VocabularyAuditReport(
        inspected_names=tuple(sorted(set(inspected))), violations=violations
    )


def _refuse_an_unscannable_package() -> None:
    """ارفض عند الاستيراد فحصًا لا يبلغ كلَّ وحدةٍ في الحزمة."""

    present = {path.name for path in _SOURCE_ROOT.glob("*.py")}
    missing = present - set(_ALGEBRA_MODULES)
    if missing:
        raise StructuralDalError(
            "وحداتٌ في الحزمة خارج الفحص: " + ", ".join(sorted(missing))
        )


_refuse_an_unscannable_package()
