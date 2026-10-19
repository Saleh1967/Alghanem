"""علاقةُ الوضع مودَعةً (ADR ٥٦): صفوفٌ باليد من الراويين، وتطابقُ المودَع ومصدرَيه،
و`WadData.lean` مع المودَع.

الطفراتُ بأسمائها:

* `MUTANT_NO_HAMZA_FOLD`: ألفُ لين في الجذر لا تُطوى همزةً، فيسقط شاهدُ ابن فارس عن «أَلَفَت».
* `MUTANT_VOWELLED_SKELETON`: الهيكلُ بالحركات، فلا يشهد ابنُ فارس على شيء.
* `MUTANT_DROPPED_ROOT`: صفُّ «قَ اْ ل» بجذرٍ واحد، فلا يطابق `WadData` المودَعَ.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from typing import Any

from conftest import ROOT

SPEC = importlib.util.spec_from_file_location("gen_wad", ROOT / "tools" / "gen_wad.py")
assert SPEC and SPEC.loader
MOD: Any = importlib.util.module_from_spec(SPEC)
sys.modules["gen_wad"] = MOD
SPEC.loader.exec_module(MOD)

WAD = ROOT / "corpora" / "wad" / "wad.tsv"
LEAN = ROOT / "formal" / "a116" / "A116" / "WadData.lean"


def _rows() -> list[tuple[str, str, str]]:
    out = []
    for ln in WAD.read_text(encoding="utf-8").splitlines():
        k, r, w = ln.split("\t")
        out.append((k, r, w))
    return out


def test_rows_by_hand() -> None:
    rows = {(k, r): w for k, r, w in _rows()}
    # المشتركُ الذي برهن عليه Dal: قَالَ تحت قول وقيل عند لين، ولا هيكلَ «قال» عند ابن فارس
    assert rows[("قَ اْ ل", "قول")] == "lane" and rows[("قَ اْ ل", "قيل")] == "lane"
    # خَطْف: لين بالحركات، وابنُ فارس بالهيكل «خطف» تحت خطف
    assert rows[("خُ طْ ف", "خطف")] == "lane,ibn-faris"
    # أَلَفَت: جذرُ لين «الف» = «ءلف» عند ابن فارس، وهيكلُها «ءلفت» عنده تحت ءلف
    assert rows[("ءَ اْ لَ فَ ت", "الف")] == "lane,ibn-faris"


def test_deposit_is_exactly_lane_pairs_with_their_witnesses() -> None:
    lane: set[tuple[str, str]] = set()
    lane_keys = ROOT / "corpora" / "lane" / "lane-root-keys.tsv"
    for ln in lane_keys.read_text(encoding="utf-8").splitlines():
        k, roots = ln.split("\t")
        lane |= {(k, r) for r in roots.split(" ")}
    faris: dict[str, set[str]] = {}
    for ln in (ROOT / "corpora" / "hadith" / "maqayis-skeletons.tsv").read_text(
            encoding="utf-8").splitlines():
        sk, roots = ln.split("\t")
        faris[sk] = set(roots.split(" "))
    rows = _rows()
    assert {(k, r) for k, r, _ in rows} == lane and len(rows) == len(lane)
    for k, r, w in rows:
        sk = "".join(a[0] for a in k.split(" ")).replace("ى", "ي")
        expect = "lane,ibn-faris" if r.replace("ا", "ء") in faris.get(sk, set()) else "lane"
        assert w == expect, (k, r, w)


def test_mutants_are_caught() -> None:
    ps = MOD.pairs()
    good = {(k, r): ws for k, r, ws in ps}
    assert good[("ءَ اْ لَ فَ ت", "الف")] == ("lane", "ibn-faris")
    # MUTANT_NO_HAMZA_FOLD
    old = MOD.lane_root_as_ibn_faris
    MOD.lane_root_as_ibn_faris = lambda root: MOD.fold(root)
    try:
        bad = {(k, r): ws for k, r, ws in MOD.pairs()}
        assert bad[("ءَ اْ لَ فَ ت", "الف")] == ("lane",)
    finally:
        MOD.lane_root_as_ibn_faris = old
    # MUTANT_VOWELLED_SKELETON
    old_sk = MOD.skeleton_of_key
    MOD.skeleton_of_key = lambda key: key.replace(" ", "")
    try:
        assert not any(len(ws) == 2 for _, _, ws in MOD.pairs())
    finally:
        MOD.skeleton_of_key = old_sk
    # MUTANT_DROPPED_ROOT
    cut = [p for p in ps if p[:2] != ("قَ اْ ل", "قيل")]
    assert MOD.render_lean(cut) != LEAN.read_text(encoding="utf-8")


def test_lean_data_matches_the_deposit() -> None:
    text = LEAN.read_text(encoding="utf-8")
    rows = _rows()
    assert f"def pairCount : Nat := {len(rows)}" in text
    assert f"def keyCount : Nat := {len({k for k, _, _ in rows})}" in text
    assert f"def twoNarrators : Nat := {sum(1 for *_, w in rows if w == 'lane,ibn-faris')}" in text
    by: dict[str, list[str]] = {}
    for k, r, _ in rows:
        by.setdefault(k, []).append(r)
    mush = {k for k, v in by.items() if len(v) >= 2}
    lean_keys = set(re.findall(r'^  \("([^"]+)", \[', text, flags=re.M))
    assert lean_keys == mush and len(mush) == 382


def test_check_passes() -> None:
    assert MOD.main(["--check"]) == 0
