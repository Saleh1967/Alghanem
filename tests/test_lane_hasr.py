"""الحصرُ على معجم لين (ADR ٣٧): أدواتُ الحلّ الرياضيّ على مدخلاتٍ مكتوبةٍ باليد.

التوقّعاتُ محسوبةٌ هنا باليد لا بالأداة؛ والطفراتُ بأسمائها:
`MUTANT_LOO_INCLUDES_SELF` (جدولُ الأغلبيّة يرى الصفَّ نفسَه)، `MUTANT_HAMZA_NOT_NORMALIZED` (صورُ
الهمزة لا تُوحَّد)، `MUTANT_BOUNDS_SWAPPED` (طرفا المنقول مقلوبان).
"""

from __future__ import annotations

import importlib.util
import math
import sys
from typing import Any

from conftest import ROOT

SPEC = importlib.util.spec_from_file_location("gen_lane_hasr", ROOT / "tools" / "gen_lane_hasr.py")
assert SPEC and SPEC.loader
MOD: Any = importlib.util.module_from_spec(SPEC)
sys.modules["gen_lane_hasr"] = MOD
SPEC.loader.exec_module(MOD)

ROWS = [("a", "x"), ("a", "x"), ("a", "y"), ("b", "y"), ("b", "y"), ("c", "z")]


def test_strata() -> None:
    assert MOD.stratum("كتب") == ("sound", "كتب")
    assert MOD.stratum("أكل") == ("hamzated", "ءكل")
    assert MOD.stratum("سأل") == ("hamzated", "سءل")
    assert MOD.stratum("رد") == ("doubled", "ردد")
    assert MOD.stratum("قول") == ("weak", "قول")
    assert MOD.stratum("كأ") == ("doubled", "كءء")  # المضعّفُ يُقدَّم: الرأسُ حرفان
    assert MOD.stratum("كتبر") is None


def test_loo_majority_by_hand() -> None:
    # a: x,x,y → ترك x يبقى (x,y) تعادلٌ يُكسر بالأصغر x: يصيب؛ ترك y يبقى (x,x): لا يصيب
    # b: y,y → كلٌّ يصيب؛ c: وحيدٌ لا يصيب
    assert MOD.loo_majority(ROWS) == (4, 6)


def test_conditional_entropy_by_hand() -> None:
    # H(Y|F) = (3/6)·H(2/3,1/3) + 0 + 0
    h = 0.5 * (-(2 / 3) * math.log2(2 / 3) - (1 / 3) * math.log2(1 / 3))
    assert abs(MOD.cond_entropy(ROWS) - h) < 1e-12
    assert MOD.cond_entropy([(0, "x"), (0, "x")]) == 0.0


def test_skeleton_and_bounds() -> None:
    assert MOD.skeleton("1ِ 2َ اْ 3") == "1 2 ا 3"
    b = MOD.bounds(30, 70, 100)
    assert b["transmitted_low"] == 0.3 and b["transmitted_high"] == 0.7


def _mutant(old: str, new: str) -> Any:
    src = (ROOT / "tools" / "gen_lane_hasr.py").read_text(encoding="utf-8")
    assert old in src
    ns: dict[str, Any] = {"__name__": "hasr_mutant", "__file__": str(ROOT / "tools" / "x.py")}
    exec(compile(src.replace(old, new, 1), "hasr_mutant", "exec"), ns)  # noqa: S102
    return ns


def test_named_mutants_are_caught() -> None:
    m = _mutant("        c[y] -= 1\n", "")  # MUTANT_LOO_INCLUDES_SELF
    assert m["loo_majority"](ROWS) != (4, 6)
    m = _mutant('"ء" if c in HAMZA else c', "c")  # MUTANT_HAMZA_NOT_NORMALIZED
    assert m["stratum"]("أكل") != ("hamzated", "ءكل")
    m = _mutant('"transmitted_low": round(1 - hi / n, 4)',
                '"transmitted_low": round(1 - lo / n, 4)')  # MUTANT_BOUNDS_SWAPPED
    assert m["bounds"](30, 70, 100)["transmitted_low"] != 0.3
