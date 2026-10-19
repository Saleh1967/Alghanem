"""الشاهدُ يضيّق الحصر (ADR ٤٠): أدواتُ الحلّ على مدخلاتٍ مكتوبةٍ باليد.

الطفراتُ بأسمائها: `MUTANT_WITNESS_ACCEPTS_3MS` (فَعَلَهُ شاهدُ تعدية)، `MUTANT_OVER_NO_DELETION` (العكسُ
لا يحذف المعتلّ)، `MUTANT_LOWER_IS_ANY` (الأدنى «أحدُهم» لا «كلُّهم»).
"""

from __future__ import annotations

import importlib.util
import sys
from typing import Any

from conftest import ROOT

SPEC = importlib.util.spec_from_file_location("gen_lane_shahid",
                                              ROOT / "tools" / "gen_lane_shahid.py")
assert SPEC and SPEC.loader
MOD: Any = importlib.util.module_from_spec(SPEC)
sys.modules["gen_lane_shahid"] = MOD
SPEC.loader.exec_module(MOD)
FA, KA, DA, SU = "َ", "ِ", "ُ", "ْ"


def test_transitivity_witness_by_hand() -> None:
    # كَتَبْتُهُ: فاعلٌ ثمّ مفعول ← متعدٍّ بابُه الفتح
    assert MOD.witness_forms(("كَ", "تَ", "بْ", "تُ", "هُ"), "كتب") == ({FA}, set())
    # فَهِمُوهُ: بابُ الكسر
    assert MOD.witness_forms(("فَ", "هِ", "مُ", "وْ", "هُ"), "فهم") == ({KA}, set())
    # كَتَبَهُ: يلتبس باسمٍ منصوبٍ مضاف — ليس شاهدًا
    assert MOD.witness_forms(("كَ", "تَ", "بَ", "هُ"), "كتب") == (set(), set())
    # كَتَبْتُ بلا مفعول: ليس شاهدَ تعدية
    assert MOD.witness_forms(("كَ", "تَ", "بْ", "تُ"), "كتب") == (set(), set())


def test_doubled_bab_witness_by_hand() -> None:
    # فَرِرْتُ: الفكُّ يُظهر الكسر
    assert MOD.witness_forms(("فَ", "رِ", "رْ", "تُ"), "فرر") == (set(), {KA})
    # رَدَدْنَاهُ: فكٌّ ومفعول
    assert MOD.witness_forms(("رَ", "دَ", "دْ", "نَ", "اْ", "هُ"), "ردد") == ({FA}, {FA})


def test_over_by_hand() -> None:
    # الصحيحُ: قائمةٌ من واحد هي وزنُ gen_lane.pattern
    assert MOD.over(("كِ", "تَ", "اْ", "بُ", "نْ"), "كتب", "كِتَابٌ") == {f"1{KA} 2{FA} ا{SU} 3"}
    # قَالَ من قول: العينُ ألفٌ وحركتُها مجهولة — فَعَلَ بأبوابه فيها
    q = MOD.over(("قَ", "اْ", "لَ"), "قول", "")
    assert {f"1{FA} 2{FA} 3", f"1{FA} 2{KA} 3", f"1{FA} 2{DA} 3"} <= q
    # قِيَامٌ من قوم: الواوُ ياءً تبقى حركتُها
    assert f"1{KA} 2{FA} ا{SU} 3" in MOD.over(("قِ", "يَ", "اْ", "مُ", "نْ"), "قوم", "قِيَامٌ")
    # عِدَةٌ من وعد: الفاءُ محذوفة
    assert any(p.startswith("1") and p.split()[1] == f"2{KA}"
               for p in MOD.over(("عِ", "دَ", "تُ", "نْ"), "وعد", "عِدَةٌ"))


def test_hit_bounds_by_hand() -> None:
    rules = {"a": {"x"}, "b": {"y"}}
    assert MOD.hit_bounds({"a"}, [{"x"}], rules) == (True, True)
    assert MOD.hit_bounds({"a", "b"}, [{"x"}], rules) == (False, True)
    assert MOD.hit_bounds({"a"}, [{"x", "z"}], rules) == (False, True)
    assert MOD.hit_bounds({"a"}, [{"z"}, None], rules) == (False, True)
    assert MOD.hit_bounds({"a"}, [{"z"}], rules) == (False, False)


def test_spans_after_all_by_hand() -> None:
    toks = [("t", " inf. n. "), ("ar", "ضَرْبٌ"), ("t", " A man struck "), ("ar", "ضَرَبٌ"),
            ("t", "; and inf. n. "), ("ar", "ضِرَابٌ")]
    assert MOD.spans_after_all(toks, MOD.L.INF) == ["ضَرْبٌ", "ضِرَابٌ"]


def _mutant(old: str, new: str) -> Any:
    src = (ROOT / "tools" / "gen_lane_shahid.py").read_text(encoding="utf-8")
    assert old in src
    ns: dict[str, Any] = {"__name__": "shahid_mutant", "__file__": str(ROOT / "tools" / "x.py")}
    exec(compile(src.replace(old, new, 1), "shahid_mutant", "exec"), ns)  # noqa: S102
    return ns


def test_named_mutants_are_caught() -> None:
    m = _mutant('(DA, ("وْ",)), (FA, ("تْ",))', '(DA, ("وْ",)), (FA, ()), (FA, ("تْ",))')
    assert m["witness_forms"](("كَ", "تَ", "بَ", "هُ"), "كتب") != (set(), set())  # 3MS
    m = _mutant("                        go(i, k + 1, prev + (f\"{k + 1}{m}\",))  # حذف\n", "")
    assert not any(p.split()[1] == f"2{KA}" for p in
                   m["over"](("عِ", "دَ", "تُ", "نْ"), "وعد", "عِدَةٌ") or set())  # NO_DELETION
    m = _mutant("return all(certain(c) for c in cls)", "return any(certain(c) for c in cls)")
    assert m["hit_bounds"]({"a", "b"}, [{"x"}], {"a": {"x"}, "b": {"y"}})[0]  # LOWER_IS_ANY
