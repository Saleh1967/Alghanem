"""`G0.EVAL-0.AUDIT`: عزلُ طبقة التقييم نفسِها، مقيسًا لا مُدَّعًى.

طبقةُ التقييم تبني آلةَ الامتحان، فلا يجوز أن تستورد مادّةَ مجالٍ بعينه ولا
سلطةَ نواة: تدخلها المادّةُ عقدًا مُجمَّدًا من خارجها، ولا تُنسَخ إليها. وهي
تبلغ العقدَ المحايد (`prior_fiber`) وحدَه فوق البدائيّتين المشتركتين.

والمنطقُ واحدٌ لا يُنسَخ: السياسةُ هنا تخصيصٌ فوق `alghanem.import_boundary`،
وسقفُها مُعلَنٌ لا مُدَّعًى: `StaticImportAudit != ProcessIsolation`.
"""

from __future__ import annotations

from pathlib import Path

from ..import_boundary import (
    ImportBoundaryPolicy,
    ImportBoundaryReport,
    audit_import_boundary,
)

__all__ = [
    "EVALUATION_FORBIDDEN_PACKAGES",
    "EVALUATION_IMPORT_POLICY",
    "EVALUATION_PERMITTED_MODULES",
    "evaluation_import_isolation_audit",
]

EVALUATION_FORBIDDEN_PACKAGES: tuple[str, ...] = (
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
"""حزمٌ لا تُستورد من طبقة التقييم: مادّةُ مجالٍ، وسلطةُ نواة، وأنظمةٌ ستُقرَأ."""

EVALUATION_PERMITTED_MODULES: tuple[str, ...] = (
    "canonical_content",
    "import_boundary",
    "prior",
    "prior_fiber",
    "evaluation",
)
"""ما يجوز بلوغُه: البدائيّتان المشتركتان، والعقدُ المحايد، والحزمةُ نفسُها."""

EVALUATION_IMPORT_POLICY: ImportBoundaryPolicy = ImportBoundaryPolicy(
    policy_id="policy.evaluation.g0_eval_0",
    permitted_modules=EVALUATION_PERMITTED_MODULES,
    forbidden_packages=EVALUATION_FORBIDDEN_PACKAGES,
)
"""تخصيصُ السياسة لهذه الطبقة فوق البدائيّة المشتركة، لا منطقٌ ثانٍ بجانبها."""

_SOURCE_ROOT = Path(__file__).resolve().parent
_EVALUATION_MODULES = (
    "__init__.py",
    "audit.py",
    "binding.py",
    "boundary.py",
    "identity.py",
    "laws.py",
    "protocol.py",
    "report.py",
    "reveal.py",
)


def evaluation_import_isolation_audit() -> ImportBoundaryReport:
    """افحص عزلَ طبقة التقييم على مصدرها وما تبلغه من وحدات المشروع."""

    return audit_import_boundary(
        tuple(_SOURCE_ROOT / name for name in _EVALUATION_MODULES),
        EVALUATION_IMPORT_POLICY,
    )
