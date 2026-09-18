"""`G0.EXEC-0.AUDIT`: عزلُ طبقة التنفيذ نفسِها، بوصولاتها التشغيليّة مُعلَنةً.

طبقةُ التنفيذ تُشغِّل عمليّةً وتكتب مساحةَ عملٍ مؤقّتة، فوصولاتُها الديناميكيّة
موجودةٌ بالضرورة. والأمانةُ هنا ألّا تُخفى: تُقاس بالبدائيّة المشتركة نفسِها ثمّ
تُطابَق على قائمةٍ مُعلَنةٍ باسمها وموضعها، فما خرج عنها مخالفة.

ولا تبلغ هذه الطبقةُ مادّةَ مجالٍ ولا سلطةَ نواة: تدخلها المادّةُ عقدًا مُجمَّدًا
ورِبطًا مُجمَّدًا من خارجها. وسقفُ الفحص مُعلَنٌ لا مُدَّعًى:
`StaticImportAudit != ProcessIsolation`، ومعه `SeparateProcess != Sandbox`.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..import_boundary import (
    STATIC_IMPORT_AUDIT_IS_NOT_PROCESS_ISOLATION,
    ImportBoundaryPolicy,
    ImportBoundaryReport,
    audit_import_boundary,
)
from .laws import SEPARATE_PROCESS_IS_NOT_A_SANDBOX

__all__ = [
    "EXECUTION_DECLARED_ACCESSES",
    "EXECUTION_FORBIDDEN_PACKAGES",
    "EXECUTION_IMPORT_POLICY",
    "EXECUTION_PERMITTED_MODULES",
    "ExecutionIsolationReport",
    "execution_import_isolation_audit",
]

EXECUTION_FORBIDDEN_PACKAGES: tuple[str, ...] = (
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
"""حزمٌ لا تُستورد من طبقة التنفيذ: مادّةُ مجالٍ، وسلطةُ نواة، وحزمةُ تنفيذٍ أخرى."""

EXECUTION_PERMITTED_MODULES: tuple[str, ...] = (
    "canonical_content",
    "import_boundary",
    "prior",
    "prior_fiber",
    "evaluation",
    "evaluation_execution",
)
"""ما يجوز بلوغُه: البدائيّتان المشتركتان، والعقدُ المحايد، وحدُّ التقييم، ونفسُها."""

EXECUTION_DECLARED_ACCESSES: tuple[str, ...] = ("runner.py -> import_module()",)
"""الوصولاتُ التشغيليّةُ المُعلَنة، باسمها وموضعها؛ وما خرج عنها مخالفة."""

EXECUTION_IMPORT_POLICY: ImportBoundaryPolicy = ImportBoundaryPolicy(
    policy_id="policy.evaluation_execution.g0_exec_0",
    permitted_modules=EXECUTION_PERMITTED_MODULES,
    forbidden_packages=EXECUTION_FORBIDDEN_PACKAGES,
    forbid_dynamic_access=True,
)
"""تخصيصُ السياسة لهذه الطبقة فوق البدائيّة المشتركة، لا منطقٌ ثانٍ بجانبها."""

_SOURCE_ROOT = Path(__file__).resolve().parent
_EXECUTION_MODULES = (
    "__init__.py",
    "audit.py",
    "authority.py",
    "laws.py",
    "runner.py",
    "workspace.py",
)


@dataclass(frozen=True, slots=True)
class ExecutionIsolationReport:
    """تقريرُ عزلٍ يفصل المخالفةَ عن الوصول التشغيليِّ المُعلَن."""

    measured: ImportBoundaryReport
    declared_accesses: tuple[str, ...]

    @property
    def undeclared_accesses(self) -> tuple[str, ...]:
        """وصولاتٌ ديناميكيّةٌ مقيسةٌ خارج المُعلَن؛ تُسمّى جميعًا ولا تُطوى."""

        return tuple(
            sorted(set(self.measured.dynamic_accesses) - set(self.declared_accesses))
        )

    @property
    def unused_declarations(self) -> tuple[str, ...]:
        """وصولاتٌ أُعلِنت ولم تُقَس؛ إعلانٌ زائدٌ يُسمّى ولا يُطوى."""

        return tuple(
            sorted(set(self.declared_accesses) - set(self.measured.dynamic_accesses))
        )

    @property
    def is_isolated_within_declared_accesses(self) -> bool:
        """أخلت الطبقةُ من كلِّ حزمةٍ ممنوعةٍ ومن كلِّ وصولٍ غيرِ مُعلَن؟"""

        return not self.measured.violations and not self.undeclared_accesses

    @property
    def isolation_ceiling(self) -> str:
        """ما لا يجوز أن يُقرَأ هذا التقريرُ إثباتًا له."""

        return STATIC_IMPORT_AUDIT_IS_NOT_PROCESS_ISOLATION

    @property
    def mechanism_ceiling(self) -> str:
        """سقفُ آليّة التشغيل المُعلَنة."""

        return SEPARATE_PROCESS_IS_NOT_A_SANDBOX

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التقرير للعرض."""

        return {
            "policy_id": self.measured.policy_id,
            "scanned_files": list(self.measured.scanned_files),
            "reached_modules": list(self.measured.reached_modules),
            "violations": list(self.measured.violations),
            "declared_accesses": list(self.declared_accesses),
            "undeclared_accesses": list(self.undeclared_accesses),
            "unused_declarations": list(self.unused_declarations),
            "is_isolated_within_declared_accesses": (
                self.is_isolated_within_declared_accesses
            ),
            "isolation_ceiling": self.isolation_ceiling,
            "mechanism_ceiling": self.mechanism_ceiling,
        }


def execution_import_isolation_audit() -> ExecutionIsolationReport:
    """افحص عزلَ طبقة التنفيذ على مصدرها وما تبلغه، ووصولاتِها المُعلَنة."""

    return ExecutionIsolationReport(
        measured=audit_import_boundary(
            tuple(_SOURCE_ROOT / name for name in _EXECUTION_MODULES),
            EXECUTION_IMPORT_POLICY,
        ),
        declared_accesses=EXECUTION_DECLARED_ACCESSES,
    )
