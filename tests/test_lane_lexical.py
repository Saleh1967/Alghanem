"""الكلمةُ بعينها أوّلًا (ADR ٥٠): تركيبُ القرّاء والعدُّ والحكمُ على مدخلاتٍ باليد.
 الطفراتُ بأسمائها: `MUTANT_PEEL_BEFORE_LEXICON` (المقشِّرُ قبل المعجم في `S3`)،
`MUTANT_WEAK_COUNTS_AS_EXACT` (الصنفُ الضعيف اتّفاقٌ حرفًا)، `MUTANT_VERDICT_IGNORES_PRECISION`
(الحكمُ لا يرى هبوطَ الاتّفاق على المغطّى).
"""

from __future__ import annotations

import importlib.util
import sys
from typing import Any

from conftest import ROOT

SPEC = importlib.util.spec_from_file_location("gen_lane_lexical",
                                              ROOT / "tools" / "gen_lane_lexical.py")
assert SPEC and SPEC.loader
MOD: Any = importlib.util.module_from_spec(SPEC)
sys.modules["gen_lane_lexical"] = MOD
SPEC.loader.exec_module(MOD)

# ثلاثةُ قرّاء باليد: المباشرُ يقرأ «كُنْتُ»، والمعجمُ يقرأ «كُنْتُ» (خطأُ صيغة الاستشهاد)
# و«وَجْه»، والمقشِّرُ يأخذ الواوَ أصلًا
DIRECT = {"كُنْتُ": {"كون"}}
LEXICAL = {"كُنْتُ": {"كنت"}, "وَجْهَ": {"وجه"}, "بَطْنَ": {"بطن"}}
PEELED = {"كُنْتُ": {"كون"}, "وَجْهَ": {"جهو"}}


def systems() -> dict[str, Any]:
    return MOD.compose(lambda w: DIRECT.get(w, set()), lambda w: LEXICAL.get(w, set()),
                       lambda w: PEELED.get(w, set()))


def test_compose_by_hand() -> None:
    s = systems()
    assert s["S0"]("وَجْهَ") == {"جهو"} and s["S0"]("بَطْنَ") == set()
    assert s["S1"]("وَجْهَ") == {"جهو"} and s["S1"]("بَطْنَ") == {"بطن"}
    assert s["S2"]("كُنْتُ") == {"كنت"}          # المعجمُ أوّلًا يخطئ في الفعل المتصرّف
    assert s["S3"]("كُنْتُ") == {"كون"}          # الكلمةُ بعينها: الفعلُ المباشر أوّلًا
    assert s["S3"]("وَجْهَ") == {"وجه"}          # ثمّ المعجمُ قبل التقشير
    assert s["S3"]("بَطْنَ") == {"بطن"}


def test_tally_by_hand() -> None:
    rows = [("كُنْتُ", "كون"), ("وَجْهَ", "وجه"), ("بَطْنَ", "بطن"), ("زَيْدٌ", "زيد")]
    t = MOD.tally(rows, systems()["S3"])
    assert t["outcomes"] == {"agree": 3, "no_reading": 1}
    assert t["agree_over_all"]["k"] == 3 and t["coverage"] == 0.75
    t0 = MOD.tally(rows, systems()["S0"])
    assert t0["outcomes"] == {"agree": 1, "disagree": 1, "no_reading": 2}
    # الصنفُ الضعيف يُعدّ وحدَه
    w = MOD.tally([("رَمَى", "رمي")], lambda _w: {"رمو"})
    assert w["outcomes"] == {"agree_weak_class": 1}


def _r(k: int, n: int) -> dict[str, Any]:
    return MOD.R.rate(k, n)


def test_verdict_by_hand() -> None:
    s0 = {"agree_over_all": _r(400, 1000), "agree_among_covered": _r(400, 500)}
    better = {"agree_over_all": _r(600, 1000), "agree_among_covered": _r(600, 760)}
    same = {"agree_over_all": _r(405, 1000), "agree_among_covered": _r(405, 505)}
    sloppy = {"agree_over_all": _r(600, 1000), "agree_among_covered": _r(600, 1000)}
    assert MOD.verdict(s0, better) == "S3_BETTER"
    assert MOD.verdict(s0, same) == "S3_NOT_BETTER"
    assert MOD.verdict(s0, sloppy) == "S3_LOSES_PRECISION"


def _mutant(old: str, new: str) -> Any:
    src = (ROOT / "tools" / "gen_lane_lexical.py").read_text(encoding="utf-8")
    assert old in src
    ns: dict[str, Any] = {"__name__": "lexical_mutant", "__file__": str(ROOT / "tools" / "x.py")}
    exec(compile(src.replace(old, new, 1), "lexical_mutant", "exec"), ns)  # noqa: S102
    return ns


def test_named_mutants_are_caught() -> None:
    m = _mutant('"S3": first(direct, lexical, peeled)', '"S3": first(direct, peeled, lexical)')
    s = m["compose"](lambda w: DIRECT.get(w, set()), lambda w: LEXICAL.get(w, set()),
                     lambda w: PEELED.get(w, set()))
    assert s["S3"]("وَجْهَ") == {"جهو"}  # PEEL_BEFORE_LEXICON
    m = _mutant("elif gold in rs:", "elif gold in rs or any(R.same(gold, r) for r in rs):")
    assert m["tally"]([("رَمَى", "رمي")], lambda _w: {"رمو"})["outcomes"] == {"agree": 1}
    m = _mutant("return \"S3_BETTER\" if up and keep", "return \"S3_BETTER\" if up")
    s0 = {"agree_over_all": _r(400, 1000), "agree_among_covered": _r(400, 500)}
    sloppy = {"agree_over_all": _r(600, 1000), "agree_among_covered": _r(600, 1000)}
    assert m["verdict"](s0, sloppy) == "S3_BETTER"  # VERDICT_IGNORES_PRECISION
