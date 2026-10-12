"""قفلُ لين (ADR ٤٥): أدواتُ القفل على مدخلاتٍ مكتوبةٍ باليد، والختمُ والسطورُ المسمّاة.

الطفراتُ بأسمائها: `MUTANT_DAMMA_READ_AS_KASRA` (الضمُّ يُقرأ كسرًا)،
`MUTANT_ADMIT_WITHOUT_LANE` (تُقبل القاعدةُ المسمّاة بلا مثالٍ من لين)،
`MUTANT_PRECISION_COUNTS_BOTH_AS_HIT` (الوجهان إصابةٌ في الحدّ الأدنى)، `MUTANT_MARK_IGNORED`
(علامةُ لين «هُ» لا تعيّن التعدية في الإحصاء).
"""

from __future__ import annotations

import importlib.util
import sys
from typing import Any

from conftest import ROOT

SPEC = importlib.util.spec_from_file_location("gen_lane_khatm",
                                              ROOT / "tools" / "gen_lane_khatm.py")
assert SPEC and SPEC.loader
MOD: Any = importlib.util.module_from_spec(SPEC)
sys.modules["gen_lane_khatm"] = MOD
SPEC.loader.exec_module(MOD)
FA, KA, DA, SU = "َ", "ِ", "ُ", "ْ"
SENT = ("لأن جمع فعلة بكسر الفاء يكون على فعل بكسر الأول وفتح الثاني وجمع فعلة بضم الفاء يكون على "
        "فعل بضم الأول وفتح الثاني")
FI = (f"1{KA} 2{SU} 3{FA} ة", f"1{KA} 2{FA} 3")
FU = (f"1{DA} 2{SU} 3{FA} ة", f"1{DA} 2{FA} 3")


def test_named_rules_by_hand() -> None:
    assert MOD.named_rules(SENT) == [FI, FU]
    assert MOD.named_rules("جمع فعلة يكون على فعل") == []


def test_admit_by_hand() -> None:
    per = {"قربة/قرب": [list(FI)], "غرفة/غرف": [list(FU), list(FI)], "كسرة/كسر": [list(FI)]}
    assert MOD.admit([FI, FU], per) == [FI, FU]
    # لا يشكل لين وجهَ الضمّ في أمثلة البند: لا يُقبل
    assert MOD.admit([FI, FU], {"قربة/قرب": [list(FI)], "غرفة/غرف": [list(FI)]}) == [FI]
    # مثالُ البند الآخر لا يكفي
    assert MOD.admit([FU], {"كسرة/كسر": [list(FU)]}) == []


def test_precision_by_hand() -> None:
    rows = [["f", str(i), "r", "v", v, "past"] for i, v in enumerate(["1", "1", "01", "0"])]
    p = MOD.precision(rows)
    assert p and p["precision"] == [0.5, 0.75] and p["intransitive"] == 1 and p["both"] == 1
    assert MOD.precision(rows[:3] + [["f", "9", "r", "v", "", "past"]]) is None
    assert MOD.precision([]) is None


def _e(k: str, marked: bool, wit: bool, h0: tuple[bool, bool], h1: tuple[bool, bool]
       ) -> dict[str, Any]:
    both = (h0[0] and h1[0], h0[1] or h1[1])
    return {"file": "f", "entry": k, "rad": "r", "verb": "v", "marked": marked, "past": wit,
            "impf": False, "hit": {"0": h0, "1": h1, "01": both}}


YES, NO = (True, True), (False, False)


def test_census_by_hand() -> None:
    es = [_e("m", True, False, NO, YES),     # معلَّم: متعدٍّ ← إصابة
          _e("w", False, True, YES, NO),     # مشهود، مُلئ 0 ← إصابة
          _e("d", False, False, YES, YES),   # لا تتوقّف إصابتُه ← إصابة
          _e("u1", False, False, NO, YES), _e("u2", False, False, NO, YES)]   # U
    wframe = [["f", "w", "r", "v", "0", "past"]]
    c = MOD.census(es, [["f", "u1", "r", "v", "1"]], wframe)
    # 3 معيَّنة + |U| = 2 × q = 1 ← 5 من 5: المنقولُ صفر
    assert c and c["unresolved"] == 2 and c["transmitted"] == [0.0, 0.0]
    # q بين 0 و1 ← الإصابةُ بين 3 و5: المنقولُ بين 0 و0.4
    c = MOD.census(es, [["f", "u1", "r", "v", "01"]], wframe)
    assert c and c["transmitted"] == [0.0, 0.4]
    assert MOD.census(es, [["f", "u1", "r", "v", ""]], wframe) is None
    assert MOD.census(es, [["f", "d", "r", "v", "1"]], wframe) is None  # الإطارُ من U وحدَه


def test_seal_and_quotes() -> None:
    lines = MOD.sealed_lines()
    assert MOD.quotes_hold(lines) == []
    assert MOD.named_rules(MOD.span(lines, 8222, 8225)) == [FI, FU]
    # سطرٌ غيرُ مسمًّى لا يحمل الجملة
    assert MOD.named_rules(MOD.span(lines, 8407, 8409)) == []


def _mutant(old: str, new: str) -> Any:
    src = (ROOT / "tools" / "gen_lane_khatm.py").read_text(encoding="utf-8")
    assert old in src
    ns: dict[str, Any] = {"__name__": "khatm_mutant", "__file__": str(ROOT / "tools" / "x.py")}
    exec(compile(src.replace(old, new, 1), "khatm_mutant", "exec"), ns)  # noqa: S102
    return ns


def test_named_mutants_are_caught() -> None:
    m = _mutant('VOWEL_NAMES = {"ضم": DA,', 'VOWEL_NAMES = {"ضم": KA,')
    assert m["named_rules"](SENT) != [FI, FU]  # DAMMA_READ_AS_KASRA
    m = _mutant("return [r for r in named if r in seen]", "return list(named)")
    assert m["admit"]([FU], {}) == [FU]  # ADMIT_WITHOUT_LANE
    m = _mutant('if e["marked"]:\n            vals = "1"',
                'if e["marked"]:\n            vals = "01"')
    es = [_e("m", True, False, NO, YES), _e("u1", False, False, NO, YES)]
    got = m["census"](es, [["f", "u1", "r", "v", "1"]], [])
    assert got["transmitted"] != [0.0, 0.0]  # MARK_IGNORED
    m = _mutant('lo = sum(v == "1" for v in vals)', 'lo = sum(v in ("1", "01") for v in vals)')
    rows = [["f", str(i), "r", "v", v, "past"] for i, v in enumerate(["1", "01"])]
    assert m["precision"](rows)["precision"][0] == 1.0  # PRECISION_COUNTS_BOTH_AS_HIT
