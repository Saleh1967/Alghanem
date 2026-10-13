"""أداةُ القياس المسجَّل (ADR ٥٨): الحكمُ على الموقع وقاعدةُ القرار بتوقّعاتٍ باليد من التسجيل المسبق، وطفرتان."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("gen_haja_qac", ROOT / "tools" / "gen_haja_qac.py")
assert SPEC is not None and SPEC.loader is not None
MOD = importlib.util.module_from_spec(SPEC)
sys.modules["gen_haja_qac"] = MOD
SPEC.loader.exec_module(MOD)


# (الوسم، الأبواب، المتوقَّع: ذهبيّ، له أبواب، يحمل، واحدٌ صحيح) — من جدول PREREG §٢ باليد
ROWS = (
    ("NEG", ("nafy",), (True, True, True, True)),
    ("NEG", ("amilFil",), (True, True, True, True)),          # لَمْ ولَنْ داخلان على الفعل
    ("NEG", ("mushabbaha", "amilFil", "atf", "nafy"), (True, True, True, False)),  # لَا
    ("RES", ("istithna",), (True, True, True, True)),          # إلّا بعد نفي
    ("ACC", ("nafy",), (True, True, False, False)),
    ("N", ("jarr",), (False, True, False, False)),
    ("PRON", (), (True, False, False, False)),
    ("V", (), (False, False, False, False)),
)


def test_judge_by_hand() -> None:
    for gold, babs, want in ROWS:
        assert MOD.judge(gold, babs) == want, (gold, babs)


def test_verdict_by_hand() -> None:
    assert MOD.verdict(0.96, 0.91) == "HAJA_JAMI_MANI"
    assert MOD.verdict(0.96, 0.80) == "HAJA_JAMI"
    assert MOD.verdict(0.90, 0.95) == "HAJA_MANI"
    assert MOD.verdict(0.90, 0.80) == "HAJA_GAPS"


def test_mapping_is_the_registered_one() -> None:
    assert MOD.TAGS["istithna"] == frozenset({"EXP", "RES"})
    assert MOD.TAGS["amilFil"] == frozenset({"NEG", "FUT", "CERT", "PRO", "SUB"})
    assert "ghayrMusnad" not in MOD.TAGS and "mustaqill" not in MOD.TAGS
    assert len(MOD.GOLD) == 18


def test_mutant_threshold_swapped_rejected() -> None:
    """THRESHOLD_SWAPPED: عتبتا الجامع والمانع مبدَّلتان — يحكم على (0.92، 0.96) بغير ما سجّل."""

    def mutant(m1: float, m2: float) -> str:
        return MOD.verdict(m2, m1)

    assert mutant(0.92, 0.96) != MOD.verdict(0.92, 0.96)


def test_mutant_single_ignores_correctness_rejected() -> None:
    """SINGLE_WITHOUT_HIT: «الحسم» يعدّ البابَ الواحد ولو خطأً — يخالف صفَّ ACC/nafy."""

    def mutant(gold: str, babs: tuple[str, ...]) -> tuple[bool, bool, bool, bool]:
        g, h, hit, _ = MOD.judge(gold, babs)
        return (g, h, hit, len(babs) == 1)

    assert any(mutant(g, b) != w for g, b, w in ROWS)
