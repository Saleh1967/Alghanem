"""قياسُ القابليّة على «المخصَّص» مرجعًا آليًّا (ADR ٥٠؛ التسجيل `docs/hukm/PREREG-mukhassas.md`).

توقّعاتٌ باليد على قواعد التسجيل: التطبيعُ N، ومقابلةُ الجذر بالموضع المعتلّ، واحتمالُ الصدفة،
وفاصلُ Wilson؛ وزوجٌ صادقٌ قُرئ باليد من الملفّين (ولد ← «باب الحمل والولادة»: العقدةُ 2 في SLGE،
والعقدةُ 4 في المرجع)؛ وطفرتان بأسمائهما؛ والنتيجةُ المودَعة هي ما تحسبه الأداةُ الآن.
"""

from __future__ import annotations

import importlib.util
import json
import sys

from conftest import ROOT

SPEC = importlib.util.spec_from_file_location("gen_hukm_mukhassas",
                                              ROOT / "tools" / "gen_hukm_mukhassas.py")
assert SPEC and SPEC.loader
MOD = importlib.util.module_from_spec(SPEC)
sys.modules["gen_hukm_mukhassas"] = MOD
SPEC.loader.exec_module(MOD)


def test_norm_by_hand() -> None:
    assert MOD.norm("بَابُ  الحَمْلِ (والوِلادة).") == "باب الحمل والولادة"
    assert MOD.norm("أسماء ما يخرج مع الولد ١٢") == "اسماء ما يخرج مع الولد"
    assert MOD.norm("الأُنثى") == "الانثي"


def test_root_match_by_hand() -> None:
    walad = 27 * 900 + 23 * 30 + 8  # و ل د
    assert MOD.root_matches(walad, "ولد") and not MOD.root_matches(walad, "يلد")
    weak = 1 * 900 + 23 * 30 + 29  # ا ل [معتلّ]: الموضعُ الثالث 29
    assert MOD.root_matches(weak, "الو") and MOD.root_matches(weak, "الي")
    assert not MOD.root_matches(weak, "الد") and not MOD.root_matches(walad, "ولدت")


def test_chance_and_wilson_by_hand() -> None:
    assert abs(MOD.chance(10, 2, 3) - (1 - 56 / 120)) < 1e-12
    assert MOD.chance(10, 0, 3) == 0.0 and MOD.chance(10, 8, 3) == 1.0
    lo, hi = MOD.wilson(50, 100)
    assert abs(lo - 0.4038) < 1e-4 and abs(hi - 0.5962) < 1e-4


def test_one_true_pair_by_hand() -> None:
    by_title, members, n = MOD.reference()
    assert n == 2314 and by_title["باب الحمل والولادة"] == [4]
    assert 4 in MOD.nodes_of(27 * 900 + 23 * 30 + 8, members)


def test_mutants_are_caught() -> None:
    """`MUTANT_NO_HAMZA_FOLD`، `MUTANT_WEAK_MATCHES_ANY`."""

    def no_fold(t: str) -> str:
        return " ".join(MOD.DROP.sub("", t).split())

    assert no_fold("الأُنثى") != MOD.norm("الأُنثى")
    def weak_any(code: int, rho: str) -> bool:
        return len(rho) == 3 and all(i == MOD.WEAK or MOD.ALPHABET[i] == rho[k]
                                     for k, i in enumerate(MOD.decode(code)))

    weak = 1 * 900 + 23 * 30 + 29
    assert weak_any(weak, "الد") != MOD.root_matches(weak, "الد")


def test_result_is_what_the_tool_computes() -> None:
    path = ROOT / "docs" / "hukm" / "mukhassas-result.json"
    saved = json.loads(path.read_text(encoding="utf-8"))
    assert saved == json.loads(MOD.render(MOD.measure()))
    assert saved["pairs"]["matched"] + saved["pairs"]["node_unmatched"] == saved["pairs"]["all"]
