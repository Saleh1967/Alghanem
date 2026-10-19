"""«المخصَّص» مرجعًا للجنس والقابليّة (ADR ٤٨): العُقَدُ والعضويّةُ كما قرأتُهما في النصّ
المختوم.

التوقّعاتُ منقولةٌ باليد من سطور الطبعة: السطر 31007 `### | (كتاب الدهور والأزمنة والأهوية
والرياح)` يليه `### $ 3 - (أسماء الدهر والأوقات)` وفي نصّه «دهر كلّ قوم زمانهم»؛ والسطر
25165 `### $ 1 - الكتاب الغنم` عنوانُ كتابٍ مرقومٌ عقدةً. والطفرات: `MUTANT_KEEP_PARENS`
(القوسان يُبقيان فلا يُعرف الكتاب)، `MUTANT_AMBIGUOUS_COUNTS` (الهيكلُ الملتبس لا يُدخل
جذرًا)، `MUTANT_PAGE_LINES` (علاماتُ الصفحة ليست نصًّا).
"""

from __future__ import annotations

import importlib.util
import sys
from typing import Any

from conftest import ROOT

SPEC = importlib.util.spec_from_file_location(
    "gen_mukhassas", ROOT / "tools" / "gen_mukhassas.py")
assert SPEC and SPEC.loader
MOD: Any = importlib.util.module_from_spec(SPEC)
sys.modules["gen_mukhassas"] = MOD
SPEC.loader.exec_module(MOD)


def _nodes() -> dict[str, dict[str, str]]:
    rows = MOD.NODES.read_text(encoding="utf-8").splitlines()
    head = rows[0].split("\t")
    return {r.split("\t")[0]: dict(zip(head, r.split("\t"), strict=True)) for r in rows[1:]}


def _membership() -> dict[str, list[str]]:
    return {ln.split("\t")[0]: ln.split("\t")[1].split(" ")
            for ln in MOD.MEMBERSHIP.read_text(encoding="utf-8").splitlines()}


def test_hand_nodes() -> None:
    by_line = {n["line"]: n for n in _nodes().values()}
    assert by_line["31007"]["title"] == "كتاب الدهور والأزمنة والأهوية والرياح"
    dahr = by_line["31008"]
    dahur = "كتاب الدهور والأزمنة والأهوية والرياح"
    assert (dahr["title"], dahr["book"]) == ("أسماء الدهر والأوقات", dahur)
    assert by_line["25165"]["book"] == "الكتاب الغنم"  # BOOK_HEADING_MISTYPED


def test_hand_membership() -> None:
    by_line = {n["line"]: n for n in _nodes().values()}
    assert by_line["31008"]["id"] in _membership()["دهر"]


def test_mutants_are_caught() -> None:
    # MUTANT_KEEP_PARENS: «(كتاب الدهور…)» لا يبدأ بـ«كتاب »
    assert not MOD.is_book("(كتاب الدهور)") and MOD.is_book(MOD.title("(كتاب الدهور)"))
    # MUTANT_AMBIGUOUS_COUNTS: هيكلٌ بجذرين لا يُدخل أحدَهما
    ns = [{"id": 1, "body": ["قلت"]}]
    assert MOD.membership(ns, {"قلت": ["قلت", "قول"]}) == {}
    assert MOD.membership(ns, {"قلت": ["قول"]}) == {"قول": [1]}
    # MUTANT_PAGE_LINES: علامةُ الصفحة لا تدخل نصَّ العقدة
    got = MOD.nodes("### | (كتاب س)\n# PageV01P001\nنص")
    assert got[0]["body"] == ["نص"]
