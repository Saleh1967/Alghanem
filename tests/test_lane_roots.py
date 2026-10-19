"""جذورُ لين مرجعًا بالحركات (ADR ٤٩): المفتاحُ والحارسُ وصفوفُ المعجم والتفكيكُ على مدخلاتٍ باليد.

الطفراتُ بأسمائها: `MUTANT_KEY_KEEPS_CASE` (حركةُ الإعراب في المفتاح)،
`MUTANT_WEAK_NOT_OPTIONAL` (المعتلُّ لا يسقط في الحارس)،
`MUTANT_AMBIGUOUS_REFERENCE` (مفتاحٌ بجذرين يُعدّ مرجعًا).
"""

from __future__ import annotations

import importlib.util
import sys
from typing import Any

from conftest import ROOT

SPEC = importlib.util.spec_from_file_location("gen_lane_roots",
                                              ROOT / "tools" / "gen_lane_roots.py")
assert SPEC and SPEC.loader
MOD: Any = importlib.util.module_from_spec(SPEC)
sys.modules["gen_lane_roots"] = MOD
SPEC.loader.exec_module(MOD)


def test_key_by_hand() -> None:
    # كِتَابٌ وكِتَابٍ وكِتَابُ مفتاحٌ واحد: التنوينُ وحركةُ الإعراب خارجه
    k = ("كِ", "تَ", "اْ", "ب")
    assert MOD.key(("كِ", "تَ", "اْ", "بُ", "نْ"), "كِتَابٌ") == k
    assert MOD.key(("كِ", "تَ", "اْ", "بِ", "نْ"), "كِتَابٍ") == k
    assert MOD.key(("كِ", "تَ", "اْ", "بُ"), "كِتَابُ") == k
    # نونٌ أصليّة ساكنة لا تُحذف إذ لا تنوين في الرسم
    assert MOD.key(("مِ", "نْ"), "مِنْ") == ("مِ", "ن")
    # والحركاتُ الداخلة تفرّق: كَتَبَ غيرُ كُتُب
    assert MOD.key(("كَ", "تَ", "بَ"), "كَتَبَ") != MOD.key(("كُ", "تُ", "بُ", "نْ"), "كُتُبٌ")


def test_radicals_in_by_hand() -> None:
    assert MOD.radicals_in("كتب", "كتب")
    assert MOD.radicals_in("مكتوب", "كتب")
    assert not MOD.radicals_in("قلم", "كتب")
    # الأجوف: الواوُ ألفًا (قال)، أو ياءً (قيل)، أو ساقطة (قل)
    assert MOD.radicals_in("قال", "قول")
    assert MOD.radicals_in("قيل", "قول")
    assert MOD.radicals_in("قل", "قول")
    # الصحيحُ لا يسقط
    assert not MOD.radicals_in("كب", "كتب")


def test_lexicon_rows_by_hand() -> None:
    d = MOD.read_keys()
    # كَتَبَ ← كتب بلا التباس، وقَالَ ← قول وقيل معًا (الخاناتُ واحدة: `Dal.qala_same_cells`)
    assert d[("كَ", "تَ", "ب")] == ["كتب"]
    assert d[("قَ", "اْ", "ل")] == ["قول", "قيل"]
    assert MOD.ref_of(d, ("قَ", "اْ", "لَ"), "قَالَ") is None
    assert MOD.ref_of(d, ("كَ", "تَ", "بَ"), "كَتَبَ") == "كتب"


def test_same_is_weak_class() -> None:
    assert MOD.same("رمي", "رمو") and MOD.same("كتب", "كتب") and not MOD.same("كتب", "كبت")


def _mutant(old: str, new: str) -> Any:
    src = (ROOT / "tools" / "gen_lane_roots.py").read_text(encoding="utf-8")
    assert old in src
    ns: dict[str, Any] = {"__name__": "roots_mutant", "__file__": str(ROOT / "tools" / "x.py")}
    exec(compile(src.replace(old, new, 1), "roots_mutant", "exec"), ns)  # noqa: S102
    return ns


def test_named_mutants_are_caught() -> None:
    m = _mutant("return a[:-1] + (a[-1][0],)", "return a")
    assert m["key"](("كِ", "تَ", "اْ", "بُ", "نْ"), "كِتَابٌ") != m["key"](
        ("كِ", "تَ", "اْ", "بِ", "نْ"), "كِتَابٍ")  # KEY_KEEPS_CASE
    m = _mutant("if r in WEAK and go(i, k + 1):", "if False:")
    assert not m["radicals_in"]("قل", "قول")  # WEAK_NOT_OPTIONAL
    m = _mutant("return roots[0] if roots and len(roots) == 1 else None",
                "return roots[0] if roots else None")
    assert m["ref_of"]({("قَ", "اْ", "ل"): ["قول", "قيل"]}, ("قَ", "اْ", "لَ"), "قَالَ") == "قول"
