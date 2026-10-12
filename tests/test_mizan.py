"""الميزان (ADR ٤٢): حكمُ الموصول آلةٌ منتهيةٌ جدولُها من البرهان، والبوّابةُ تحكم بها.

١. الجدولُ كاملٌ دالّةً: 116 خانةً بأرقامٍ متمايزة، و42 حالًا، والانتقالُ وصلًا ووقفًا
   على كلّ (حال، خانة) مرّةً واحدة — فهو الدالّةُ على مجالها كلِّه (`A116.Mizan.hal_nodup`،
   `khana_nodup`)؛ ومطابقتُه لما تطبعه النواةُ في CI (`lake exe a116-table mizan`
   و`git diff --exit-code`).
٢. المفسِّرُ على جدول Lean `hadd-join` كلِّه هو عمودا `strictJoinB`/`strictJoinPauseB`
   بعينهما — والتوقّعُ من النواة.
٣. ثلاثُ طفراتٍ في المفسِّر يلتقطها الجدول: بلا حدّ، والوقفُ بآلة الوصل، والبدءُ من غير `bad'`.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

import pytest
from conftest import ROOT

from gate.mizan import BAD, CELL, HADD, QABIL_WAQF, QABIL_WASL, WAQF, WASL, machine_join, run

JOIN_TABLE = ROOT / "formal" / "a116" / "hadd-join.csv"


def _rows() -> list[tuple[tuple[str, ...], tuple[str, ...], bool, bool]]:
    out = []
    with JOIN_TABLE.open(encoding="utf-8") as fh:
        for line in fh:
            pair, _strict, joined, pause = line.rstrip("\n").split(",")
            left, right = pair.split("|")
            out.append((tuple(left.split(" ")), tuple(right.split(" ")), joined == "true",
                        pause == "true"))
    return out


ROWS = _rows()


def test_table_is_a_total_function() -> None:
    assert len(CELL) == 116 and sorted(CELL.values()) == list(range(116))
    n = len(QABIL_WASL)
    assert n == 42 == len(QABIL_WAQF) == len(HADD) and BAD == 0
    assert all(0 <= h < n for h in HADD)
    for step in (WASL, WAQF):
        assert set(step) == {(s, k) for s in range(n) for k in range(116)}
        assert all(0 <= t < n for t in step.values())


def test_machine_is_lean_strict_join_on_the_whole_table() -> None:
    assert len(ROWS) == 293904
    for left, right, joined, pause in ROWS:
        assert machine_join(left, right, False) == joined, (left, right)
        assert machine_join(left, right, True) == pause, (left, right)


def _mut_no_hadd(left: Sequence[str], right: Sequence[str], pause: bool) -> bool:
    """`MUTANT_NO_HADD_STEP`: الحدُّ لا يمسّ الحال."""

    step = WAQF if pause else WASL
    return (QABIL_WAQF if pause else QABIL_WASL)[run(step, run(step, BAD, left), right)]


def _mut_wasl_for_pause(left: Sequence[str], right: Sequence[str], pause: bool) -> bool:
    """`MUTANT_WASL_FOR_PAUSE`: الوقفُ بآلة الوصل."""

    return machine_join(left, right, False)


def _mut_wrong_start(left: Sequence[str], right: Sequence[str], pause: bool) -> bool:
    """`MUTANT_WRONG_START`: البدءُ من غير `bad'`."""

    step = WAQF if pause else WASL
    s = run(step, HADD[run(step, 3, left)], right)
    return (QABIL_WAQF if pause else QABIL_WASL)[s]


@pytest.mark.parametrize("mutant", [_mut_no_hadd, _mut_wasl_for_pause, _mut_wrong_start],
                         ids=["MUTANT_NO_HADD_STEP", "MUTANT_WASL_FOR_PAUSE", "MUTANT_WRONG_START"])
def test_table_catches_interpreter_mutants(
        mutant: Callable[[Sequence[str], Sequence[str], bool], bool]) -> None:
    assert any(mutant(left, right, False) != joined or mutant(left, right, True) != pause
               for left, right, joined, pause in ROWS)
