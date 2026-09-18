"""The single authority-free static import-boundary primitive.

Like `canonical_content`, this module is deliberately the *only* place in the
repository where declared imports are read from source, where a relative import
is resolved to its absolute position, and where a transitive reach is walked.
Two independent copies of that logic are two boundaries that can silently drift
apart: one layer would call a module unreachable while the other reaches it,
and neither would fail.

`StaticImportAudit != ProcessIsolation` is the ceiling this module keeps and
refuses to exceed. It reads source text. It proves nothing about what a running
process can open, spawn, or resolve at runtime, and it grants no confinement to
any caller. A layer that imports it inherits one thing — a measured reach over
declared source — and no isolation guarantee whatsoever.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Final

__all__ = [
    "DYNAMIC_ACCESS_NAMES",
    "STATIC_IMPORT_AUDIT_IS_NOT_PROCESS_ISOLATION",
    "ImportBoundaryError",
    "ImportBoundaryPolicy",
    "ImportBoundaryReport",
    "audit_import_boundary",
    "declared_imports",
    "displayed_path",
    "module_files",
    "resolve_relative_import",
]

STATIC_IMPORT_AUDIT_IS_NOT_PROCESS_ISOLATION: Final[str] = (
    "StaticImportAudit != ProcessIsolation: فحصُ الاستيرادات المُصرَّحة يقيس ما "
    "يبلغه المصدرُ نصًّا، ولا يُثبِت أنّ العمليّة الجارية عاجزةٌ عن بلوغ "
    "المستودع بطريقٍ آخر؛ فالحاجزُ هنا حاجزُ مصدرٍ مُصرَّح، ومن سمّاه حبسًا "
    "للعمليّة ادّعى ما لم يُثبِته"
)

DYNAMIC_ACCESS_NAMES: Final[tuple[str, ...]] = (
    "__import__",
    "eval",
    "exec",
    "exec_module",
    "import_module",
    "open",
)
"""أسماءٌ تفتح طريقًا خارج الاستيراد المُصرَّح؛ تُرصَد ولا تُعَدّ حبسًا للعمليّة."""

_PACKAGE_ROOT: Final = Path(__file__).resolve().parent
_ROOT_PACKAGE: Final = _PACKAGE_ROOT.name


class ImportBoundaryError(ValueError):
    """رفضٌ بنيويٌّ مُسمًّى في بدائيّة حاجز الاستيراد؛ لا حملَ على أقرب حالة."""


def _dotted_of(path: Path) -> str:
    relative = path.resolve().relative_to(_PACKAGE_ROOT)
    parts = relative.with_suffix("").parts
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join((_ROOT_PACKAGE, *parts))


def resolve_relative_import(module: str, level: int, path: Path) -> str:
    """Return the absolute dotted module a relative import names from `path`."""

    if level == 0:
        return module
    package = _dotted_of(path)
    if path.name != "__init__.py":
        package = package.rsplit(".", 1)[0]
    anchor = package.split(".")
    if level > 1:
        anchor = anchor[: -(level - 1)]
    if not anchor:
        raise ImportBoundaryError("استيرادٌ نسبيٌّ يتجاوز جذرَ الحزمة")
    return ".".join((*anchor, module)) if module else ".".join(anchor)


def declared_imports(path: Path) -> tuple[str, ...]:
    """Return every absolute dotted module the source at `path` declares."""

    tree = ast.parse(path.read_text(encoding="utf-8"))
    modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            modules.append(resolve_relative_import(node.module or "", node.level, path))
        elif isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
    return tuple(modules)


def _dynamic_accesses(path: Path) -> tuple[str, ...]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found: list[str] = []
    for node in ast.walk(tree):
        name: str | None = None
        if isinstance(node, ast.Call):
            target = node.func
            if isinstance(target, ast.Name):
                name = target.id
            elif isinstance(target, ast.Attribute):
                name = target.attr
        if name is not None and name in DYNAMIC_ACCESS_NAMES:
            found.append(name)
    return tuple(found)


def displayed_path(path: Path) -> str:
    """Return a machine-independent display of a source path where possible.

    A path inside this package is displayed relative to the package parent, so
    two machines agree on it. A path outside the package is displayed by its
    file name alone, because its absolute position is machine-dependent and a
    digest over it would differ where the source does not.
    """

    try:
        return str(path.relative_to(_PACKAGE_ROOT.parent))
    except ValueError:
        return path.name


def module_files(dotted: str) -> tuple[Path, ...]:
    """Return the source files of a dotted module inside this package."""

    parts = dotted.split(".")
    if not parts or parts[0] != _ROOT_PACKAGE:
        return ()
    relative = Path(*parts[1:]) if len(parts) > 1 else Path()
    module_path = _PACKAGE_ROOT / relative.with_suffix(".py")
    package_dir = _PACKAGE_ROOT / relative
    if module_path.is_file():
        return (module_path,)
    if package_dir.is_dir():
        return tuple(sorted(package_dir.rglob("*.py")))
    return ()


@dataclass(frozen=True, slots=True)
class ImportBoundaryPolicy:
    """A declared boundary: what may be reached, what may not, and how it is read.

    The policy decides nothing about processes. It names permitted first-level
    modules of the root package, forbidden first-level packages, forbidden exact
    dotted modules, and whether dynamic access names are recorded as violations.
    """

    policy_id: str
    permitted_modules: tuple[str, ...]
    forbidden_packages: tuple[str, ...]
    forbidden_modules: tuple[str, ...] = ()
    forbid_dynamic_access: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.policy_id, str) or not self.policy_id.strip():
            raise ImportBoundaryError("مُعرِّفُ السياسة نصٌّ غير فارغ")
        for label, value in (
            ("المسموحُ بلوغُه", self.permitted_modules),
            ("الممنوعُ من الحزم", self.forbidden_packages),
            ("الممنوعُ من الوحدات", self.forbidden_modules),
        ):
            if not isinstance(value, tuple):
                raise ImportBoundaryError(f"{label} صفٌّ مُجمَّد لا قائمة")
            if len(set(value)) != len(value):
                raise ImportBoundaryError(f"{label} لا يُكرِّر عضوًا؛ والمكرّرُ يُرفَض")
        overlap = set(self.permitted_modules) & set(self.forbidden_packages)
        if overlap:
            raise ImportBoundaryError(
                "حزمةٌ مسموحةٌ وممنوعةٌ معًا تُبطِل الحاجز: " + "، ".join(sorted(overlap))
            )

    def violation_of(self, dotted: str) -> str | None:
        """Return why a reached dotted module breaks this boundary, or `None`."""

        if dotted in self.forbidden_modules:
            return dotted
        for forbidden in self.forbidden_modules:
            if dotted.startswith(forbidden + "."):
                return dotted
        if not dotted.startswith(_ROOT_PACKAGE):
            return None
        head = dotted.split(".")[1] if "." in dotted else ""
        if head in self.forbidden_packages:
            return dotted
        if head and head not in self.permitted_modules:
            return dotted
        return None

    @property
    def isolation_ceiling(self) -> str:
        """The ceiling any report under this policy may claim."""

        return STATIC_IMPORT_AUDIT_IS_NOT_PROCESS_ISOLATION


@dataclass(frozen=True, slots=True)
class ImportBoundaryReport:
    """A measured reach: what was scanned, what was reached, and what violated."""

    policy_id: str
    scanned_files: tuple[str, ...]
    reached_modules: tuple[str, ...]
    violations: tuple[str, ...]
    dynamic_accesses: tuple[str, ...]

    @property
    def is_isolated(self) -> bool:
        """Whether the scanned source reached nothing the policy forbids."""

        return not self.violations and not self.dynamic_accesses

    @property
    def isolation_ceiling(self) -> str:
        """What this report may never be read as proving."""

        return STATIC_IMPORT_AUDIT_IS_NOT_PROCESS_ISOLATION

    def as_canonical_content(self) -> dict[str, object]:
        """The report content for a digest or a display."""

        return {
            "policy_id": self.policy_id,
            "scanned_files": list(self.scanned_files),
            "reached_modules": list(self.reached_modules),
            "violations": list(self.violations),
            "dynamic_accesses": list(self.dynamic_accesses),
            "is_isolated": self.is_isolated,
            "isolation_ceiling": self.isolation_ceiling,
        }


def audit_import_boundary(
    entry_files: tuple[Path, ...], policy: ImportBoundaryPolicy
) -> ImportBoundaryReport:
    """Walk the declared imports of `entry_files` and everything they reach."""

    if not isinstance(entry_files, tuple) or not entry_files:
        raise ImportBoundaryError("الفحصُ يقع على ملفّاتٍ مُسمّاةٍ غيرِ فارغة")
    scanned: list[str] = []
    reached: list[str] = []
    violations: list[str] = []
    dynamic: list[str] = []
    pending = [path.resolve() for path in entry_files]
    seen: set[Path] = set()
    while pending:
        path = pending.pop(0)
        if path in seen:
            continue
        if not path.is_file():
            raise ImportBoundaryError(f"ملفٌّ غيرُ موجودٍ في مدخل الفحص: {path}")
        seen.add(path)
        scanned.append(displayed_path(path))
        if policy.forbid_dynamic_access:
            dynamic.extend(
                f"{path.name} -> {name}()" for name in _dynamic_accesses(path)
            )
        for module in declared_imports(path):
            offending = policy.violation_of(module)
            if offending is not None:
                violations.append(f"{path.name} -> {offending}")
                continue
            if not module.startswith(_ROOT_PACKAGE):
                continue
            reached.append(module)
            pending.extend(module_files(module))
    return ImportBoundaryReport(
        policy_id=policy.policy_id,
        scanned_files=tuple(sorted(set(scanned))),
        reached_modules=tuple(sorted(set(reached))),
        violations=tuple(sorted(set(violations))),
        dynamic_accesses=tuple(sorted(set(dynamic))),
    )
