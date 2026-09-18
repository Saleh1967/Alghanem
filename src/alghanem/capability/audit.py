"""`G0.METRIC-0.AUDIT`: عزلُ طبقة القياس، مقيسًا لا مُدَّعًى.

المقامُ مُعلَنٌ من خارج التنفيذ، فلا يجوز أن تستورد هذه الحزمةُ مادّةَ مجالٍ
مبنيّةً ولا سلطةَ نواة: لو بلغت `arabic/` لصار المقامُ مُشتقًّا من الشجرة
المبنيّة، وهو عينُ ما يمنعه
`ADenominatorDerivedFromTheImplementationIsNotAMeasure`.

والمنطقُ واحدٌ لا يُنسَخ: السياسةُ تخصيصٌ فوق `alghanem.import_boundary`،
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
    "CAPABILITY_FORBIDDEN_PACKAGES",
    "CAPABILITY_IMPORT_POLICY",
    "CAPABILITY_PERMITTED_MODULES",
    "capability_import_isolation_audit",
]

CAPABILITY_FORBIDDEN_PACKAGES: tuple[str, ...] = (
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
    "evaluation_execution",
    "encyclopedia",
    "prior",
    "prior_fiber",
    "evaluation",
)
"""ما لا تبلغه طبقةُ القياس: مادّةُ مجالٍ مبنيّة، وسلطةُ نواة، وآلةُ تنفيذ."""

CAPABILITY_PERMITTED_MODULES: tuple[str, ...] = (
    "canonical_content",
    "import_boundary",
    "capability",
)
"""ما يجوز بلوغُه: البدائيّتان المشتركتان، والحزمةُ نفسُها، ولا رابعَ لها."""

CAPABILITY_IMPORT_POLICY: ImportBoundaryPolicy = ImportBoundaryPolicy(
    policy_id="policy.capability.g0_metric_0",
    permitted_modules=CAPABILITY_PERMITTED_MODULES,
    forbidden_packages=CAPABILITY_FORBIDDEN_PACKAGES,
)
"""تخصيصُ السياسة لهذه الطبقة فوق البدائيّة المشتركة، لا منطقٌ ثانٍ بجانبها."""

_SOURCE_ROOT = Path(__file__).resolve().parent
_CAPABILITY_MODULES = (
    "__init__.py",
    "aggregate.py",
    "audit.py",
    "blockers.py",
    "certificate.py",
    "declaration.py",
    "evidence.py",
    "governance.py",
    "laws.py",
    "maturity.py",
    "measure.py",
    "node.py",
    "universe.py",
    "universe_v1.py",
)


def capability_import_isolation_audit() -> ImportBoundaryReport:
    """افحص عزلَ طبقة القياس على مصدرها وما تبلغه من وحدات المشروع."""

    return audit_import_boundary(
        tuple(_SOURCE_ROOT / name for name in _CAPABILITY_MODULES),
        CAPABILITY_IMPORT_POLICY,
    )
