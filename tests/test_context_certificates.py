"""شهاداتُ المصحف **بسياقها** مودَعًا لـSLGE (`tools/gen_context_certificates.py`): كلُّ موقعٍ يدخل
البوّابةَ في سياقه (ابتداءٌ/وصلٌ، استمرارٌ/وقف) على قاموسٍ مسمًّى، والتوقّعاتُ من قانون الحدّ في Lean
(`Boundary.join_iff`، `Hadd.strictB`، `Hadd.strictJoinB`) لا من الشيفرة؛ والانحرافُ عن المودَع يُرفض
باسمه."""

from __future__ import annotations

import copy
import importlib.util
import sys

import pytest
from conftest import ROOT

from gate import Refusal
from gate.api import Context, Gate, sealed_forms
from gate.residue import repair

SPEC = importlib.util.spec_from_file_location("gen_context_certificates",
                                              ROOT / "tools" / "gen_context_certificates.py")
assert SPEC and SPEC.loader
MOD = importlib.util.module_from_spec(SPEC)
sys.modules["gen_context_certificates"] = MOD
SPEC.loader.exec_module(MOD)
FATIHA = MOD.lines_of(MOD.CORPUS.read_bytes())[:7]


def _joined(left: str, word: str, exit_: str) -> object:
    return Gate(Context(entry="joined", exit=exit_, left=left),
                domain=[repair(word)[0]]).enter(word.encode("utf-8"))


def test_declared_domain_is_inside_the_sealed_corpus_and_left_is_canonical() -> None:
    with pytest.raises(ValueError, match="DOMAIN_OUTSIDE_SEALED_CORPUS"):
        Gate(domain=["حَاسُوبٌ"])  # رسمٌ ليس من المدوّنة
    with pytest.raises(ValueError, match="DOMAIN_OUTSIDE_SEALED_CORPUS"):
        Gate(domain=[FATIHA[0][1]])  # رسمٌ لا صورةٌ قانونيّة (الشدّةُ قبل الحركة)
    g = Gate(Context(entry="joined", left=FATIHA[0][0]), domain=[repair(FATIHA[0][1])[0]])
    assert g.context.left == repair(FATIHA[0][0])[0] and g.context.left in sealed_forms()
    assert len(sealed_forms()) == 17572 and Gate().context == Context()


def test_wasl_drops_after_a_word_and_pause_silences_the_last() -> None:
    """`Boundary.join_iff`: همزةُ الوصل تسقط في الوصل فتبدأ الذرّاتُ بالساكن؛ والوقفُ يُسكِّن الآخر."""

    bismi, allahi, rahman = FATIHA[0][:3]
    start = Gate().enter(allahi.encode("utf-8"))
    joined = _joined(bismi, allahi, "continue")
    assert not isinstance(start, Refusal) and not isinstance(joined, Refusal)
    assert start.atoms[0] == "ءَ" and joined.atoms == start.atoms[1:]
    nabudu = FATIHA[4][1]
    cont, pause = _joined(FATIHA[4][0], nabudu, "continue"), _joined(FATIHA[4][0], nabudu, "pause")
    assert cont.atoms[-1] == "دُ" and pause.atoms[-1] == "دْ" and cont.atoms[:-1] == pause.atoms[:-1]
    assert _joined(allahi, rahman, "continue").atoms[0] == "رْ"


def test_pausal_madd_is_licensed_and_the_cross_word_straddle_is_refused_by_name() -> None:
    """`Hadd.strictPauseB`: قافيةُ مدٍّ يُغلقها ساكنُ الوقف (الرَّحِيمْ) مرخَّصةٌ وقفًا (المدُّ العارض
    للسكون؛ `rahim_pause_debt_closed`) — الدَّينُ `CVVC_PAUSE` مسدود؛ ووصلًا كما كانت."""

    r = _joined(FATIHA[0][2], FATIHA[0][3], "pause")
    assert not isinstance(r, Refusal) and r.atoms[-2:] == ("يْ", "مْ")
    assert not isinstance(_joined(FATIHA[0][2], FATIHA[0][3], "continue"), Refusal)
    # `Hadd.strictJoinB`: المدُّ في كلمةٍ والمدغمُ في التالية (اهْدِنَا + الصِّرَاطَ) — عبر الحدّ لا يُستثنى
    r = _joined(FATIHA[5][0], FATIHA[5][1], "continue")
    assert r == Refusal("REJECT", ("JUNCTION_NOT_LICENSED", "CVVC_ACROSS_WORD_BOUNDARY"))


def test_gates_follow_the_declared_boundary_policy() -> None:
    gates = MOD.gates_for(FATIHA[:2])
    keys = sorted(gates)
    assert keys == sorted({(repair(t[i - 1])[0], MOD.EXITS[i == len(t) - 1])
                           for t in FATIHA[:2] for i in range(1, len(t))})
    assert all(g.context.entry == "joined" and g.context.exit == e for (_, e), g in gates.items())
    left, word = FATIHA[0][0], FATIHA[0][1]
    assert repair(word)[0] in gates[(repair(left)[0], "continue")].book.domain
    assert MOD.POLICY["exit"].startswith("الموقعُ الأخير pause")


def test_drift_is_named_at_its_first_position() -> None:
    fresh = {"version": 1, "tokens": 3, "line_lengths": [3], "forms": [{"cells": []}],
             "stream": [[0, 0, -1], [0, 0, -1], [-1, 1, 0]], "refusals": ["REJECT:X"]}
    assert MOD.drift(fresh, fresh) is None
    mutant = copy.deepcopy(fresh)
    mutant["stream"][2] = [0, 1, -1]
    assert MOD.drift(fresh, mutant).startswith("stream[2]:")
    mutant = copy.deepcopy(fresh)
    mutant["line_lengths"] = [2]
    assert MOD.drift(fresh, mutant).startswith("line_lengths[0]:")
    mutant = copy.deepcopy(fresh)
    del mutant["forms"][-1]
    assert "الطولُ" in MOD.drift(fresh, mutant)
    mutant = copy.deepcopy(fresh)
    del mutant["refusals"]
    assert "في أحدهما فقط" in MOD.drift(fresh, mutant)


def test_the_whole_mushaf_in_context() -> None:
    """المودَعُ كاملًا: المواقعُ هي مواقعُ `corpus-certificates` نفسُها، وكلُّ رفضٍ باسمه."""

    fresh = MOD.generate()
    assert fresh["tokens"] == 78245 and fresh["lines"] == 6236
    assert sum(fresh["line_lengths"]) == fresh["tokens"]
    assert sum(fresh["status"].values()) == fresh["tokens"]
    assert sum(fresh["refusal_counts"].values()) == fresh["tokens"] - fresh["status"]["READY"]
    assert all(s[0] == -1 or s[2] == -1 for s in fresh["stream"])
    assert all(":" in r for r in fresh["refusals"])
