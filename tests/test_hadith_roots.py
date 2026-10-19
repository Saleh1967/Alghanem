"""جذورُ الصحيحين من «مقاييس اللغة» (ADR ٤٧): القاعدةُ `RULE_B` على مدخلاتٍ باليد، ومعجمُ الهياكل
كما قرأتُه في النصّ.

التوقّعاتُ منقولةٌ باليد من نصّ ابن فارس في الجدول المختوم: تحت «قول» «قَالَ يَقُول قَولاً»
فـ«يقول» ← قول؛ وتحت «أجج» «أجيجاً» فـ«ءجيجا» ← ءجج. والتباسٌ مسمّى يُثبت ولا يُخفى
(`REFERENCE_HOMOGRAPH`): «قالوا» يقع تحت «قلو» لأنّ أصوله بترتيبها فيه. والطفرات:
`MUTANT_STRONG_ONLY` (الأصولُ الصحيحة وحدَها تُدخل «قال» تحت قول وتُكثر الالتباس)،
`MUTANT_NO_SEAT_FOLD`، `MUTANT_SEEN_INCLUDED`.
"""

from __future__ import annotations

import importlib.util
import sys
from typing import Any

from conftest import ROOT

SPEC = importlib.util.spec_from_file_location(
    "gen_hadith_roots", ROOT / "tools" / "gen_hadith_roots.py")
assert SPEC and SPEC.loader
MOD: Any = importlib.util.module_from_spec(SPEC)
sys.modules["gen_hadith_roots"] = MOD
SPEC.loader.exec_module(MOD)


def test_rule_on_hand_inputs() -> None:
    assert MOD.skeleton("يَقُولُ") == "يقول" and MOD.fold("أَمْر") == "ءَمْر"
    assert MOD.in_order("يقول", "قول") and not MOD.in_order("قال", "قول")
    assert MOD.in_order("قالوا", "قلو")  # REFERENCE_HOMOGRAPH: يُثبت ولا يُخفى


def test_dictionary_rows_read_by_hand() -> None:
    d = MOD.read_skeletons()
    assert d["يقول"] == ["قول"] and d["ءجيجا"] == ["ءجج"] and d["قالوا"] == ["قلو"]
    assert all(len(r) == 3 and set(r) <= MOD.RADICALS for rs in d.values() for r in rs)


def test_weak_class() -> None:
    assert MOD.wy("صلي") == MOD.wy("صلو") and MOD.wy("قول") != MOD.wy("قلع")


def test_mutants_are_caught() -> None:
    # MUTANT_STRONG_ONLY: لو كفت الأصولُ الصحيحة لوقع «قال» تحت قول — والقاعدةُ تمنعه
    strong = [c for c in "قول" if c not in "وي"]
    assert MOD.in_order("قال", "".join(strong)) and not MOD.in_order("قال", "قول")
    # MUTANT_NO_SEAT_FOLD: «أ» ليست من الأصول، فبلا طيٍّ يسقط جذرُ أجج
    assert "أ" not in MOD.RADICALS and MOD.fold("أجج") == "ءجج"
    # MUTANT_SEEN_INCLUDED: مواقعُ العيّنة التي ملأها الوكيلُ خارجَ القياس
    assert len(MOD.seen()) == 500
