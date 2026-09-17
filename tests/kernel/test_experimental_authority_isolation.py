"""G0.EX: the third path's isolation, asserted by sweep rather than by prose.

Two directions are swept. Nothing in the kernel reads the experimental path
except its own evidence gate, and the experimental path reads nothing of the
verdict, certificate, or closure modules. The authority surfaces on both sides
of the constitutional/executive split are asserted to have gained nothing.
"""

import ast
from pathlib import Path

import alghanem
from alghanem.kernel import (
    experimental,
    experimental_comparison,
    experimental_evidence_gate,
)
from alghanem.kernel.birth_certificate import (
    ConstitutionalBirthAuthority,
    ExecutableEntity,
    ExecutiveAdmissionGate,
)
from alghanem.kernel.birth_verdict import BirthVerdictGate
from alghanem.kernel.experimental import ExperimentalAuthority, ExperimentalRunRecord

KERNEL_ROOT = Path(alghanem.__file__).parent / "kernel"
EXPERIMENTAL_MODULE_NAMES = frozenset(
    {"experimental", "experimental_comparison", "experimental_evidence_gate"}
)
FORBIDDEN_UPSTREAM_IMPORTS = frozenset(
    {
        "birth",
        "birth_certificate",
        "birth_content_identity",
        "birth_verdict",
        "evidence_acquisition",
        "independent_closure",
        "independent_closure_composition",
        "residual",
        "residual_survival",
        "weaker_model_closure",
        "weaker_model_exhaustion",
    }
)


def imported_kernel_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.level == 1 and node.module:
            imported.add(node.module.split(".")[0])
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("alghanem.kernel."):
                    imported.add(alias.name.split(".")[2])
    return imported


def test_no_kernel_module_outside_the_gate_reads_the_experimental_path() -> None:
    readers = {
        path.stem: sorted(imported_kernel_modules(path) & EXPERIMENTAL_MODULE_NAMES)
        for path in KERNEL_ROOT.rglob("*.py")
        if path.stem not in EXPERIMENTAL_MODULE_NAMES and path.stem != "__init__"
    }

    assert {name: reads for name, reads in readers.items() if reads} == {}


def test_the_experimental_core_reads_nothing_of_the_birth_path() -> None:
    for module_name in ("experimental", "experimental_comparison"):
        imported = imported_kernel_modules(KERNEL_ROOT / f"{module_name}.py")

        assert not imported & FORBIDDEN_UPSTREAM_IMPORTS


def test_the_gate_reads_only_the_frozen_binding_and_never_the_acquisition_chain() -> (
    None
):
    imported = imported_kernel_modules(KERNEL_ROOT / "experimental_evidence_gate.py")

    assert "experiment_spec_content_identity" in imported
    assert not imported & FORBIDDEN_UPSTREAM_IMPORTS


def test_the_three_authority_surfaces_gained_nothing_from_this_milestone() -> None:
    def surface(owner: type) -> set[str]:
        return {name for name in vars(owner) if not name.startswith("_")}

    assert surface(ConstitutionalBirthAuthority) == {"assess", "authority_id"}
    assert surface(ExecutiveAdmissionGate) == {"admit"}
    assert surface(BirthVerdictGate) == {"assess"}
    assert surface(ExperimentalAuthority) == {"authority_id", "run"}


def test_an_experimental_record_is_not_an_executable_entity() -> None:
    assert not issubclass(ExperimentalRunRecord, ExecutableEntity)
    assert not issubclass(ExecutableEntity, ExperimentalRunRecord)


def test_the_experimental_modules_declare_their_own_named_laws() -> None:
    assert experimental.EXPERIMENTAL_NAMED_LAWS
    assert experimental_comparison.EXPERIMENTAL_COMPARISON_NAMED_LAWS
    assert experimental_evidence_gate.EXPERIMENTAL_EVIDENCE_NAMED_LAWS
