"""اختباراتُ المطلقِ والمقيّد: الحملُ مشروطٌ بشرطين معًا، وشاهدُه شاهدُ عدمِ حمل."""

from __future__ import annotations

import pkgutil
from pathlib import Path

import pytest

import alghanem.kernel as kernel_package
from alghanem.arabic import (
    BOTH_UNITIES_ARE_REQUIRED_NOTE,
    ITLAQ_IS_NOT_UMUM_NOTE,
    MUTLAQ_IS_NOT_A_GATE_NOTE,
    MUTLAQ_WORDING_NOT_TRANSCRIBED,
    NON_CARRYING_WITNESS_IS_THE_SHARPER_ONE_NOTE,
    ZIHAR_QATL_PAIR,
    CarryingOutcome,
    DalilScope,
    ItlaqStanding,
    MutlaqMuqayyadError,
    MutlaqMuqayyadPair,
    NassRegistration,
    derive_carrying,
)

_MODULE = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "alghanem"
    / "arabic"
    / "mutlaq_muqayyad.py"
)


def mutlaq(**overrides: object) -> NassRegistration:
    base: dict[str, object] = {
        "reference": "النصُّ المطلق",
        "wording": "لفظٌ شائعٌ في جنسه بلا قيد",
        "ruling": "عتقُ رقبة",
        "ruling_cause": "سببُ الحكم",
        "standing": ItlaqStanding.مطلق,
    }
    base.update(overrides)
    return NassRegistration(**base)  # type: ignore[arg-type]


def muqayyad(**overrides: object) -> NassRegistration:
    base: dict[str, object] = {
        "reference": "النصُّ المقيَّد",
        "wording": "لفظٌ في جنسه مع قيد",
        "ruling": "عتقُ رقبة",
        "ruling_cause": "سببُ الحكم",
        "standing": ItlaqStanding.مقيد,
        "qayd": "الإيمان",
    }
    base.update(overrides)
    return NassRegistration(**base)  # type: ignore[arg-type]


def test_carrying_requires_both_unities_together() -> None:
    assert derive_carrying(True, True) is CarryingOutcome.يحمل
    assert derive_carrying(True, False) is CarryingOutcome.لا_يحمل
    assert derive_carrying(False, True) is CarryingOutcome.لا_يحمل
    assert derive_carrying(False, False) is CarryingOutcome.لا_يحمل
    assert "معًا" in BOTH_UNITIES_ARE_REQUIRED_NOTE


def test_a_qayd_is_required_of_the_muqayyad_and_forbidden_of_the_mutlaq() -> None:
    with pytest.raises(MutlaqMuqayyadError):
        muqayyad(qayd="")
    with pytest.raises(MutlaqMuqayyadError):
        mutlaq(qayd="الإيمان")


def test_the_standings_are_not_the_scopes_of_umum_khusus() -> None:
    assert ItlaqStanding is not DalilScope
    assert "مستقلّةٌ عن `DalilScope`" in ITLAQ_IS_NOT_UMUM_NOTE


def test_a_pair_must_be_one_mutlaq_and_one_muqayyad() -> None:
    with pytest.raises(MutlaqMuqayyadError):
        MutlaqMuqayyadPair(
            mutlaq=mutlaq(),
            muqayyad=mutlaq(reference="نصٌّ آخر"),
            declared_outcome=CarryingOutcome.يحمل,
        )


def test_the_declared_outcome_is_checked_against_the_derived_one() -> None:
    with pytest.raises(MutlaqMuqayyadError):
        MutlaqMuqayyadPair(
            mutlaq=mutlaq(),
            muqayyad=muqayyad(ruling_cause="سببٌ آخر"),
            declared_outcome=CarryingOutcome.يحمل,
        )


def test_carrying_is_derived_when_both_unities_hold() -> None:
    pair = MutlaqMuqayyadPair(
        mutlaq=mutlaq(),
        muqayyad=muqayyad(),
        declared_outcome=CarryingOutcome.يحمل,
    )
    assert pair.same_ruling is True
    assert pair.same_cause is True
    assert pair.outcome is CarryingOutcome.يحمل
    assert pair.blocked_by_cause_alone is False


def test_the_zihar_witness_blocks_by_the_cause_alone() -> None:
    assert ZIHAR_QATL_PAIR.same_ruling is True
    assert ZIHAR_QATL_PAIR.same_cause is False
    assert ZIHAR_QATL_PAIR.outcome is CarryingOutcome.لا_يحمل
    assert ZIHAR_QATL_PAIR.blocked_by_cause_alone is True
    assert "عدمِ حمل" in NON_CARRYING_WITNESS_IS_THE_SHARPER_ONE_NOTE


def test_both_texts_are_retained_and_neither_is_dropped() -> None:
    assert ZIHAR_QATL_PAIR.retained == (
        ZIHAR_QATL_PAIR.mutlaq,
        ZIHAR_QATL_PAIR.muqayyad,
    )


def test_the_source_gap_is_named_not_folded() -> None:
    assert "MUTLAQ_WORDING_NOT_TRANSCRIBED" in MUTLAQ_WORDING_NOT_TRANSCRIBED


def test_the_module_declares_its_own_limits_by_name() -> None:
    assert "لا سلطة" in MUTLAQ_IS_NOT_A_GATE_NOTE


def test_the_module_imports_no_kernel_authority() -> None:
    source = _MODULE.read_text(encoding="utf-8")
    imports = tuple(
        line for line in source.splitlines() if line.startswith(("import ", "from "))
    )
    assert imports
    assert not any("kernel" in line for line in imports)


def test_no_kernel_module_reads_this_registration() -> None:
    for module in pkgutil.walk_packages(
        kernel_package.__path__, prefix="alghanem.kernel."
    ):
        spec = module.module_finder.find_spec(module.name)  # type: ignore[union-attr]
        assert spec is not None and spec.origin is not None
        text = Path(spec.origin).read_text(encoding="utf-8")
        for name in ("mutlaq_muqayyad", "MutlaqMuqayyadPair", "NassRegistration"):
            assert name not in text, (module.name, name)
