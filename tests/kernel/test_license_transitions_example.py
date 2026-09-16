"""شاهدُ المثال المُشغَّل: كلُّ حالةٍ من الخمس تُثبَّت بقرارها لا بوصفها.

المثالُ في `examples/kernel/license_transitions.py` يُحمَّل من مساره لا
يُستورَد حزمةً — فشجرةُ `examples/` ليست حزمةً، ونسخُ منطقه هنا يُنتِج نسختين
تفترقان عند أوّل تحرير.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

from alghanem.kernel import (
    InvariantAssessmentSpecificationError,
    InvariantSpec,
    InvariantVerificationGate,
    StructuralAdmissionGate,
)

_EXAMPLE = (
    Path(__file__).resolve().parents[2]
    / "examples"
    / "kernel"
    / "license_transitions.py"
)


def _load() -> ModuleType:
    spec = importlib.util.spec_from_file_location("license_transitions", _EXAMPLE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def example() -> ModuleType:
    return _load()


@pytest.fixture(scope="module")
def statuses(example: ModuleType) -> dict[str, str]:
    result = example.run()
    assert isinstance(result, dict)
    return result


def test_a_faithful_transition_is_admitted_and_then_verified(
    statuses: dict[str, str],
) -> None:
    assert statuses["case_1_admission"] == "ADMITTED"
    assert statuses["case_1_invariant"] == "VERIFIED"


def test_a_declared_invariant_survives_admission_and_falls_at_verification(
    statuses: dict[str, str],
) -> None:
    """`DeclaredInvariant != VerifiedInvariant`: القبولُ لا يحسم المضمون."""

    assert statuses["case_2_admission"] == statuses["case_1_admission"]
    assert statuses["case_2_invariant"] == "BLOCK"


def test_a_structural_refusal_is_recorded_with_its_own_audit(
    example: ModuleType, statuses: dict[str, str]
) -> None:
    assert statuses["case_3_admission"] == "BLOCK"
    candidate = example.strip_marks_candidate(
        before_letters="كتب",
        after_letters="كتب",
        evidence_claim_id="CLAIM-SOMETHING-ELSE",
    )
    decision = StructuralAdmissionGate.assess(candidate)
    assert decision.transition is None
    audit = decision.audit
    assert audit is not None
    assert audit.candidate is candidate
    assert audit.trace is candidate.trace
    assert audit.reason.strip()


def test_a_branch_birth_claim_is_admitted_and_its_origin_is_bound(
    example: ModuleType, statuses: dict[str, str]
) -> None:
    """القبولُ البنيويُّ ليس `CertifiedOutcome`: لا حكمَ يصدر من هذا المستوى."""

    assert statuses["case_4_admission"] == "ADMITTED"
    assert statuses["case_4_invariant"] == "VERIFIED"
    transition = StructuralAdmissionGate.require_admitted(
        example.syllable_birth_candidate()
    )
    provenance = transition.branch_origin_provenance
    assert provenance is not None
    assert provenance.origin_anchor == transition.anchor
    assert provenance.branch_anchor == transition.target_anchor
    assert not hasattr(transition, "outcome")


def test_an_unauthorized_extractor_defers_and_a_disproof_outranks_it(
    statuses: dict[str, str],
) -> None:
    """`Unauthorized != Disproved`، و`False ∧ Unknown == False`."""

    assert statuses["case_5_unauthorized"] == "DEFER"
    assert statuses["case_5_mixed"] == "BLOCK"


def test_specs_that_do_not_cover_the_preserved_components_are_refused(
    example: ModuleType,
) -> None:
    """طلبٌ مُعطَلُ الصياغة ليس حكمًا: لا يُقرأ تفنيدًا ولا تعذّرًا."""

    transition = StructuralAdmissionGate.require_admitted(
        example.strip_marks_candidate(before_letters="كتب", after_letters="كتب")
    )
    with pytest.raises(InvariantAssessmentSpecificationError):
        InvariantVerificationGate.assess_all_preserved(
            transition, (), example.sealed_registry()
        )
    with pytest.raises(InvariantAssessmentSpecificationError):
        InvariantVerificationGate.assess_all_preserved(
            transition,
            (
                InvariantSpec(
                    invariant_id=example.SKELETON_INVARIANT,
                    component=example.SKELETON,
                    extractor_id=example.SKELETON_EXTRACTOR,
                ),
                InvariantSpec(
                    invariant_id=example.COUNT_INVARIANT,
                    component=example.LETTER_COUNT,
                    extractor_id=example.COUNT_EXTRACTOR,
                ),
            ),
            example.sealed_registry(),
        )
