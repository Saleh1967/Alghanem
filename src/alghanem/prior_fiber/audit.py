"""`G0.FIBER-0.AUDIT`: فحصُ العزل الاستيراديّ وفحصُ حياد المفردات.

العزلُ يُقاس على الاستيرادات المُصرَّحة في مصدر هذه الحزمة وما تبلغه عبرها من
وحدات `alghanem`، لا على `sys.modules` وقتَ التشغيل. ومنطقُ المشي والحلِّ النسبيِّ
واحدٌ في المشروع: `alghanem.import_boundary`، ولا يُنسَخ هنا؛ فنسختان من قاعدةٍ
واحدةٍ حاجزان ينحرفان بصمت. وهذه الطبقةُ تُخصِّص السياسةَ فحسب.

وسقفُ هذا الفحص مُعلَنٌ لا مُدَّعًى: `StaticImportAudit != ProcessIsolation`.

والحيادُ يُفحَص على الأسماء: لا يظهر في هذه الطبقة لسانٌ بعينه ولا مادّةُ مجالٍ
ولا اسمُ نظامٍ من الأنظمة التي ستقرأ عقدَها.
"""

from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
from enum import Enum
from pathlib import Path
from types import ModuleType

from ..import_boundary import (
    STATIC_IMPORT_AUDIT_IS_NOT_PROCESS_ISOLATION,
    ImportBoundaryPolicy,
    audit_import_boundary,
)
from .laws import (
    AN_ADAPTER_FLOWS_INTO_THE_FIBER_NOT_THE_REVERSE,
    NO_SYSTEM_DEFINES_THE_CONTRACT_IT_IS_READ_BY,
)

__all__ = [
    "FORBIDDEN_ALGHANEM_PACKAGES",
    "FORBIDDEN_NAME_FRAGMENTS",
    "PERMITTED_ALGHANEM_MODULES",
    "PRIOR_FIBER_IMPORT_POLICY",
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
    "evaluation",
)
"""حزمٌ لا تُستورد من هذه الطبقة: مادّةُ مجالٍ، وسلطةُ نواةٍ، وطبقةُ التقييم فوقها."""

PERMITTED_ALGHANEM_MODULES: tuple[str, ...] = (
    "canonical_content",
    "import_boundary",
    "prior",
    "prior_fiber",
)
"""ما يجوز بلوغُه: البصمةُ القانونيّة، وحاجزُ الاستيراد، والقاعدةُ السابقة، والحزمةُ نفسُها."""

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

PRIOR_FIBER_IMPORT_POLICY: ImportBoundaryPolicy = ImportBoundaryPolicy(
    policy_id="policy.prior_fiber.g0_fiber_0",
    permitted_modules=PERMITTED_ALGHANEM_MODULES,
    forbidden_packages=FORBIDDEN_ALGHANEM_PACKAGES,
)
"""تخصيصُ السياسة لهذه الطبقة فوق البدائيّة المشتركة، لا منطقٌ ثانٍ بجانبها."""

_SOURCE_ROOT = Path(__file__).resolve().parent
_FIBER_MODULES = (
    "__init__.py",
    "audit.py",
    "commitment.py",
    "contract.py",
    "fibers.py",
    "laws.py",
    "node.py",
)


@dataclass(frozen=True, slots=True)
class FiberImportIsolationReport:
    """تقريرُ العزل: ما فُحص، وما بُلِغ، وما خالف، وسقفُ ما يُدَّعى به."""

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

    @property
    def isolation_ceiling(self) -> str:
        """ما لا يجوز أن يُقرَأ هذا التقريرُ إثباتًا له."""

        return STATIC_IMPORT_AUDIT_IS_NOT_PROCESS_ISOLATION

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التقرير للعرض."""

        return {
            "scanned_files": list(self.scanned_files),
            "alghanem_imports": list(self.alghanem_imports),
            "violations": list(self.violations),
            "is_isolated": self.is_isolated,
            "isolation_ceiling": self.isolation_ceiling,
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


def fiber_import_isolation_audit() -> FiberImportIsolationReport:
    """افحص العزلَ على مصدر الحزمة وما تبلغه من وحدات `alghanem`."""

    report = audit_import_boundary(
        tuple(_SOURCE_ROOT / name for name in _FIBER_MODULES),
        PRIOR_FIBER_IMPORT_POLICY,
    )
    return FiberImportIsolationReport(
        scanned_files=report.scanned_files,
        alghanem_imports=report.reached_modules,
        violations=report.violations,
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
