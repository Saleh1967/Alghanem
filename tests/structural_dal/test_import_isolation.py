"""موضعُ `structural_dal/` من البناء: طبقةٌ أسبقُ من كلِّ دعوى لغويّة.

الحارسُ هنا مزدوج:

    zero-one  ↛  signifier_algebra / maqayis / madlul / kernel authority
    zero-one  vocabulary  ↛  root / weight / meaning / lexicon

والعزلُ يُقاس على الاستيرادات المُصرَّحة في المصدر وما تبلغه، لا على
`sys.modules` وقتَ التشغيل؛ فإنّ `alghanem/__init__.py` نفسَه يستورد النواةَ
ولا سلطةَ لهذه الطبقة عليه.
"""

from __future__ import annotations

import ast
from pathlib import Path

from alghanem.structural_dal import (
    FORBIDDEN_ALGHANEM_PACKAGES,
    PERMITTED_ALGHANEM_MODULES,
    import_isolation_audit,
    vocabulary_audit,
)

_SOURCE_ROOT = Path(__file__).resolve().parents[2] / "src" / "alghanem"
_PACKAGE = _SOURCE_ROOT / "structural_dal"

_FORBIDDEN_NAMES = (
    "maqayis",
    "madlul",
    "signifier_algebra",
    "signified_kind",
    "signifier_signified_relation",
    "jarad_mazid",
    "lexical_evidence_layer",
    "maqayis_lexical_evidence",
)


def _declared_imports(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            modules.append("." * node.level + (node.module or ""))
        elif isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
    return modules


def _package_modules() -> list[Path]:
    return sorted(_PACKAGE.glob("*.py"))


def test_the_layer_exists_as_its_own_package() -> None:
    names = {path.name for path in _package_modules()}
    assert {
        "__init__.py",
        "audit.py",
        "hypothesis.py",
        "induction.py",
        "laws.py",
        "residual.py",
        "slots.py",
        "space.py",
        "transition.py",
    } == names


def test_the_layer_reads_only_permitted_alghanem_modules() -> None:
    for path in _package_modules():
        for module in _declared_imports(path):
            if module.startswith(".") or not module.startswith("alghanem"):
                continue
            head = module.split(".")[1]
            assert head in PERMITTED_ALGHANEM_MODULES, (path.name, module)


def test_the_layer_reads_no_forbidden_package() -> None:
    for path in _package_modules():
        for module in _declared_imports(path):
            parts = module.lstrip(".").split(".")
            for forbidden in FORBIDDEN_ALGHANEM_PACKAGES:
                assert forbidden not in parts, (path.name, module)


def test_no_lexical_or_semantic_module_is_named_in_the_source() -> None:
    for path in _package_modules():
        text = path.read_text(encoding="utf-8")
        for module in _declared_imports(path):
            for name in _FORBIDDEN_NAMES:
                assert name not in module, (path.name, module)
        assert "PrimarySignificationAnchor" not in text, path.name


def test_the_audit_reports_the_layer_as_isolated() -> None:
    report = import_isolation_audit()
    assert report.is_isolated
    assert report.violations == ()
    assert set(report.alghanem_imports) <= {
        "alghanem.canonical_content",
        "alghanem.fractal_generation",
    }


def test_the_audit_reaches_beyond_the_package_itself() -> None:
    report = import_isolation_audit()
    assert any(path.startswith("fractal_generation/") for path in report.scanned_files)
    assert any(path.startswith("structural_dal/") for path in report.scanned_files)


def test_the_vocabulary_carries_no_linguistic_claim() -> None:
    report = vocabulary_audit()
    assert report.is_clean
    assert report.violations == ()
    assert report.inspected_names


def test_no_lower_layer_reads_this_layer() -> None:
    for package in ("kernel", "prior", "ontology", "metaalgebra", "fractal_generation"):
        directory = _SOURCE_ROOT / package
        if not directory.is_dir():
            continue
        for path in sorted(directory.rglob("*.py")):
            for module in _declared_imports(path):
                parts = module.lstrip(".").split(".")
                assert "structural_dal" not in parts, (path.name, module)
