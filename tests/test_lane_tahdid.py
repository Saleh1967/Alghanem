"""التعيين (ADR ٤٣): أدواتُ الحلّ على مدخلاتٍ مكتوبةٍ باليد.

الطفراتُ بأسمائها: `MUTANT_IMPERFECT_ACCEPTS_HAMZA` (أَفْعَلُهُ شاهدُ تعدية)، `MUTANT_COMPAT_U_ALLOWS_U`
(يَفْعُلُ يشهد لفَعُلَ)، `MUTANT_PIN_KEEPS_B` (التمايزُ لا يحذف البندَ الآخر)، `MUTANT_REFINE_IGNORES_LAST`
(التحقيقُ لا يقارن الحرفَ الأخير)، `MUTANT_ESTIMATE_PARTIAL` (تقديرٌ قبل ملء الإطار كلِّه).
"""

from __future__ import annotations

import importlib.util
import sys
from typing import Any

from conftest import ROOT

SPEC = importlib.util.spec_from_file_location("gen_lane_tahdid",
                                              ROOT / "tools" / "gen_lane_tahdid.py")
assert SPEC and SPEC.loader
MOD: Any = importlib.util.module_from_spec(SPEC)
sys.modules["gen_lane_tahdid"] = MOD
SPEC.loader.exec_module(MOD)
FA, KA, DA, SU = "َ", "ِ", "ُ", "ْ"


def test_imperfect_witness_by_hand() -> None:
    # يَضْرِبُهُ: مضارعٌ بمفعول، عينُه مكسورة
    assert MOD.imperfect_witness(("يَ", "ضْ", "رِ", "بُ", "هُ"), "ضرب") == {KA}
    # نَكْتُبُهُ وتَكْتُبُونَهُ ويَكْتُبُوهُ
    assert MOD.imperfect_witness(("نَ", "كْ", "تُ", "بُ", "هُ"), "كتب") == {DA}
    assert MOD.imperfect_witness(("تَ", "كْ", "تُ", "بُ", "وْ", "نَ", "هُ"), "كتب") == {DA}
    assert MOD.imperfect_witness(("يَ", "كْ", "تُ", "بُ", "وْ", "هُ"), "كتب") == {DA}
    # أَكْرَمُهُ: يلتبس بأفعل التفضيل — ليس شاهدًا
    assert MOD.imperfect_witness(("ءَ", "كْ", "رَ", "مُ", "هُ"), "كرم") == set()
    # يُكْرِمُهُ: مضارعُ أفعل (حرفُ المضارعة مضموم) — ليس من المجرّد
    assert MOD.imperfect_witness(("يُ", "كْ", "رِ", "مُ", "هُ"), "كرم") == set()
    # يَكْتُبُ بلا مفعول
    assert MOD.imperfect_witness(("يَ", "كْ", "تُ", "بُ"), "كتب") == set()


def test_compat_by_hand() -> None:
    assert MOD.compat_babs({DA}) == {FA}
    assert MOD.compat_babs({KA}) == {FA, KA}
    assert MOD.compat_babs({FA}) == {FA, KA}
    assert MOD.compat_babs(set()) == set()


def test_lane_label_by_hand() -> None:
    assert MOD.lane_label("aor. , inf. n. , It was, or became, broad; intrans.") == "neg_label"
    assert MOD.lane_label("He was, or became, glad") == "neg_stative"
    assert MOD.lane_label("He struck him; trans. ; also intrans.") is None
    assert MOD.lane_label("He wrote it") is None


def _cands(table: dict[str, set[str]]) -> Any:
    return lambda w, r: table.get(w)


def test_pin_by_hand() -> None:
    fi, fu = ("1ِ 2ْ 3َ ة", "1ِ 2َ 3"), ("1ُ 2ْ 3َ ة", "1ُ 2َ 3")
    table = {"قِرْبَةٌ": {fi[0]}, "قِرَبٌ": {fi[1]}, "قُرْبَةٌ": {fu[0]}, "قُرَبٌ": {fu[1]},
             "غِرْفَةٌ": {fi[0]}, "غِرَفٌ": {fi[1]}, "غُرْفَةٌ": {fu[0]}, "غُرَفٌ": {fu[1]},
             "كِسْرَةٌ": {fi[0]}, "كِسَرٌ": {fi[1]}}
    pc = {("قربة", "قرب"): [("قِرْبَةٌ", "قِرَبٌ"), ("قُرْبَةٌ", "قُرَبٌ")],
          ("غرفة", "غرف"): [("غِرْفَةٌ", "غِرَفٌ"), ("غُرْفَةٌ", "غُرَفٌ")],
          ("كسرة", "كسر"): [("كِسْرَةٌ", "كِسَرٌ")]}
    assert MOD.pin(pc, _cands(table))["pinned"] == list(fu)
    # إن احتمل البندُ الثاني الوجهين فلا تعيين
    pc2 = dict(pc)
    pc2[("كسرة", "كسر")] = [("كِسْرَةٌ", "كِسَرٌ"), ("قُرْبَةٌ", "قُرَبٌ")]
    assert MOD.pin(pc2, _cands(table))["pinned"] is None
    # وإن لم يشهد مثالُ البند الأوّل إلّا الوجهَ الواحد فلا يبقى شيءٌ بعد الحذف
    pc3 = dict(pc)
    pc3[("غرفة", "غرف")] = [("غِرْفَةٌ", "غِرَفٌ")]
    assert MOD.pin(pc3, _cands(table))["pinned"] is None


def test_realize_and_refine_by_hand() -> None:
    # قَالَ من قول: فَعَلَ يصير قَ اْ لَ، وفَعِلَ لا
    q = ("قَ", "اْ", "لَ")
    got, st = MOD.refine({f"1{FA} 2{FA} 3", f"1{FA} 2{KA} 3", f"1{FA} اْ 3"}, "قول", q, "")
    assert st == "REFINED" and f"1{FA} 2{FA} 3" in got and f"1{FA} 2{KA} 3" not in got
    # الصحيح: الوزنُ نفسُه يعيد الخانات (هويّة)، والتاءُ المربوطةُ زائدةٌ بعد الأصل
    assert MOD.refine({f"1{KA} 2{FA} اْ 3"}, "كتب", ("كِ", "تَ", "اْ", "بُ", "نْ"),
                      "كِتَابٌ")[1] == "REFINED"
    assert MOD.refine({f"1{FA} 2{FA} اْ 3{FA} ة"}, "فصح",
                      ("فَ", "صَ", "اْ", "حَ", "تُ", "نْ"), "فَصَاحَةٌ")[1] == "REFINED"
    # لا مرشَّحَ يعيدها: تبقى القائمةُ كما هي
    assert MOD.refine({f"1{KA} 2{KA} 3"}, "كتب", ("كِ", "تَ", "اْ", "بُ"), "") == (
        {f"1{KA} 2{KA} 3"}, "NO_REALIZATION")
    assert MOD.refine(None, "كتب", (), "") == (None, "UNBOUNDED")


def test_frame_size_and_estimate_by_hand() -> None:
    # |U| = 500 من n = 1000: ‎(1.96·0.5·0.5/0.03)² = 266.8…‎ ← 267
    assert MOD.frame_size(500, 1000) == 267
    assert MOD.frame_size(10, 1000) == 1  # ‎(1.96·0.5·0.01/0.03)² = 0.107…‎
    assert MOD.frame_size(900, 1000) == 865  # ‎864.36‎
    assert MOD.frame_size(950, 1000) == 950  # ‎963.07‎ يجاوز |U| فالحدُّ |U|
    assert MOD.frame_size(0, 1000) == 0
    hit = {("f", "a"): {"0": False, "1": True}, ("f", "b"): {"0": True, "1": False}}
    rows = [["f", "a", "r", "v", "1"], ["f", "b", "r", "v", "01"]]
    est = MOD.estimate(rows, hit, lo=100, u=200, n=1000)
    # q بين 1/2 و2/2: المنقولُ بين 1 − (100+200)/1000 و1 − (100+100)/1000
    assert est and est["transmitted"] == [0.7, 0.8]
    assert MOD.estimate([["f", "a", "r", "v", "1"], ["f", "b", "r", "v", ""]],
                        hit, 100, 200, 1000) is None


def _mutant(old: str, new: str) -> Any:
    src = (ROOT / "tools" / "gen_lane_tahdid.py").read_text(encoding="utf-8")
    assert old in src
    ns: dict[str, Any] = {"__name__": "tahdid_mutant", "__file__": str(ROOT / "tools" / "x.py")}
    exec(compile(src.replace(old, new, 1), "tahdid_mutant", "exec"), ns)  # noqa: S102
    return ns


def test_named_mutants_are_caught() -> None:
    m = _mutant('PREFIX = frozenset("يتن")', 'PREFIX = frozenset("يتنء")')
    assert m["imperfect_witness"](("ءَ", "كْ", "رَ", "مُ", "هُ"), "كرم")  # ACCEPTS_HAMZA
    m = _mutant("DA: frozenset(FA), KA", "DA: frozenset(FA + DA), KA")
    assert DA in m["compat_babs"]({DA})  # COMPAT_U_ALLOWS_U
    m = _mutant("rest = sorted(ca - cb)", "rest = sorted(ca)")
    fi, fu = ("1ِ 2ْ 3َ ة", "1ِ 2َ 3"), ("1ُ 2ْ 3َ ة", "1ُ 2َ 3")
    table = {"a": {fi[0]}, "b": {fi[1]}, "c": {fu[0]}, "d": {fu[1]}}
    pc = {("قربة", "قرب"): [("a", "b"), ("c", "d")], ("غرفة", "غرف"): [("a", "b"), ("c", "d")],
          ("كسرة", "كسر"): [("a", "b")]}
    assert m["pin"](pc, _cands(table))["pinned"] is None  # PIN_KEEPS_B
    m = _mutant("and bool(real) and real[-1][0] == surf[-1][0])", "and bool(real))")
    assert m["same"](["كِ", "تَ", "اْ", "بْ"], ("كِ", "تَ", "اْ", "مُ"))  # REFINE_IGNORES_LAST
    m = _mutant('any(v not in ("1", "0", "01") for v in vals)', "False")
    hit = {("f", "a"): {"0": False, "1": True}}
    try:
        got = m["estimate"]([["f", "a", "r", "v", ""]], hit, 1, 2, 10)
    except (KeyError, ValueError):
        got = "crash"
    assert got is not None  # ESTIMATE_PARTIAL
