"""المجالُ الخامس — جذورُ QAC مرجعًا محجوبًا (ADR ٤١): الختمُ، والمحاذاةُ، والصفوفُ كما قرأتُها باليد.

التوقّعاتُ منقولةٌ باليد من سطور `quranic-corpus-morphology-0.4.txt` ومن سطور المدوّنة المختومة، لا من
الأداة: (1:6:1) ‎{hodi‎ ‎IMPV‎ ‎ROOT:hdy‎ = «اهْدِنَا» السطر 6 الرمز 1؛ (1:7:3) ‎>anoEamo‎ ‎PERF‎ ‎ROOT:nEm‎ =
«أَنْعَمْتَ» 7/3؛ (2:21:3) ‎{Eobudu‎ ‎IMPV‎ ‎ROOT:Ebd‎ = «اعْبُدُوا» 28/4 بعد ضمّ «يَا» إلى «أَيُّهَا»؛ (6:1:1)
‎Hamodu‎ ‎ROOT:Hmd‎ = «الْحَمْدُ» 790/5 بعد ترك البسملة. ولا تُسأل البوّابةُ هنا: القياسُ في `measure` وحدَه.
والطفرات: `MUTANT_NO_BASMALA_RULE`، `MUTANT_NO_YA_RULE`، `MUTANT_HAMZA_AS_ALIF`.
"""

from __future__ import annotations

import hashlib
import importlib.util
import re
import sys
from typing import Any

from conftest import ROOT

SPEC = importlib.util.spec_from_file_location("gen_qac", ROOT / "tools" / "gen_qac.py")
assert SPEC and SPEC.loader
MOD: Any = importlib.util.module_from_spec(SPEC)
sys.modules["gen_qac"] = MOD
SPEC.loader.exec_module(MOD)

RADICALS = set("بتثجحخدذرزسشصضطظعغفقكلمنهويء")  # الحواملُ إلّا الألف — باليد
MARKS = re.compile(r"[ً-ْٰ]")


def _rows() -> dict[tuple[str, str], dict[str, str]]:
    return {(r["line"], r["pos"]): r for r in MOD.read_reference()}


def test_source_is_sealed() -> None:
    digest = "a1d12923815341face765083805d2148ed2d9f5cc3f7d6665219d887675d8c46"
    assert hashlib.sha256(MOD.source()).hexdigest() == digest


def test_hand_rows() -> None:
    rows = _rows()
    assert {k: rows[k]["root"] for k in [("6", "1"), ("7", "3"), ("28", "4"), ("790", "5")]} == {
        ("6", "1"): "هدي", ("7", "3"): "نعم", ("28", "4"): "عبد", ("790", "5"): "حمد"}
    assert (rows[("6", "1")]["aspect"], rows[("7", "3")]["aspect"]) == ("IMPV", "PERF")
    assert rows[("28", "4")]["loc"] == "2:21:3" and rows[("790", "5")]["loc"] == "6:1:1"
    assert all(set(r["root"]) <= RADICALS and len(r["root"]) in (3, 4) for r in rows.values())


def test_alignment_keeps_root_letters() -> None:
    # كلُّ صفٍّ كلمتُه من مدوّنتنا تحمل أصولَ جذره الصحيحةَ بترتيبها (والمضعَّفُ مرّة)، إلّا ما أبدلته أو حذفته
    # العربيّةُ نفسُها — بأسمائه باليد: ادَّخَرَ/ادَّكَرَ (ذ ← د)، يَكُ (حذفُ النون والواو)، المُصَيْطِر (س ← ص).
    allowed = {"ذخر", "ذكر", "كون", "سطر"}
    for r in _rows().values():
        word, root = MARKS.sub("", r["word"]), r["root"]
        root = root[:2] if root[1] == root[2] else root
        i, ok = 0, True
        for c in (c for c in root if c not in "ءويه"):
            k = word.find(c, i)
            if k < 0:
                ok = False
                break
            i = k + 1
        assert ok or r["root"] in allowed, r


def test_named_rules_and_residual() -> None:
    _, rules, residual = MOD.align(MOD.source(), MOD.CORPUS.read_text(encoding="utf-8"))
    assert rules["BASMALA"] == 112  # مئةٌ وأربعَ عشرةَ سورةً إلّا الفاتحةَ والتوبة
    assert residual == ["20:94", "37:130", "72:16"]  # يَبْنَؤُمَّ، إِلْيَاسِينَ، وَأَلَّوِ — كلمةٌ واحدةٌ عنده


def test_mutants_are_caught() -> None:
    raw = "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ الْحَمْدُ لِلَّهِ".split(" ")
    assert len(MOD.groups(6, 1, raw)[0]) == 2
    # MUTANT_NO_BASMALA_RULE: لو عُدّت البسملة لصارت الكلماتُ ستًّا لا اثنتين
    assert len([t for t in raw if MOD.LETTER.search(t)]) == 6
    # MUTANT_NO_YA_RULE: «يَا» موقعٌ وحدَه فتزيد الآيةُ كلمة
    ya = "يَا أَيُّهَا النَّاسُ".split(" ")
    assert len(MOD.groups(2, 21, ya)[0]) == 2 and len(ya) == 3
    # MUTANT_HAMZA_AS_ALIF: ‎A‎ ألفٌ لا همزة فيخرج الجذرُ من الأصول
    assert MOD.BW["A"] == "ء" and "ا" not in RADICALS
