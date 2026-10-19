"""الميزان (ADR ٤٢): حكمُ الموصول آلةٌ منتهيةٌ جدولُها من البرهان، والبوّابةُ تحكم بها.

١. الجدولُ كاملٌ دالّةً: 116 خانةً بأرقامٍ متمايزة، و42 حالًا، والانتقالُ وصلًا ووقفًا
   على كلّ (حال، خانة) مرّةً واحدة — فهو الدالّةُ على مجالها كلِّه (`A116.Mizan.hal_nodup`،
   `khana_nodup`)؛ ومطابقتُه لما تطبعه النواةُ في CI (`lake exe a116-table mizan`
   و`git diff --exit-code`).
٢. المفسِّرُ على جدول Lean `hadd-join` كلِّه هو عمودا `strictJoinB`/`strictJoinPauseB`
   بعينهما — والتوقّعُ من النواة.
٣. ثلاثُ طفراتٍ في المفسِّر يلتقطها الجدول: بلا حدّ، والوقفُ بآلة الوصل، والبدءُ من غير `bad'`.
٤. (ADR ٤٤) الجدولُ هو ما فحصته النواة: `mizan.csv` صفًّا صفًّا هو `A116.MizanData` الذي تساويه
   النواةُ بتعريف الآلة (`A116.MizanKernel.cellT_eq`، `stateT_eq`، `waslT_eq`، `waqfT_eq`)؛
   وطفرةُ رقمٍ واحد تُلتقط.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Sequence

import pytest
from conftest import ROOT

from gate.mizan import BAD, CELL, HADD, QABIL_WAQF, QABIL_WASL, WAQF, WASL, machine_join, run

JOIN_TABLE = ROOT / "formal" / "a116" / "hadd-join.csv"
CSV = ROOT / "formal" / "a116" / "mizan.csv"
KERNEL_DATA = ROOT / "formal" / "a116" / "A116" / "MizanData.lean"
MARK = {"fatha": "\u064e", "damma": "\u064f", "kasra": "\u0650", "sukun": "\u0652"}
"""علامةُ الحالة كما يكتبها `HaddTable.mark` في جداول Lean الأخرى (`hadd-join.csv`): أربعٌ باليد."""


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


def _kernel_rows(text: str) -> list[str]:
    """صفوفُ `A116.MizanData` بصيغة `mizan.csv`: الخانةُ (حاملُها وعلامتُها) والحالُ والانتقال."""

    def block(name: str) -> str:
        i = text.index(f"def {name} ")
        return text[text.index(":= [", i) + 4:text.index("\n]", i)]

    rows = [f"cell,{chr(int(h, 16))}{MARK[m]},{k}"
            for h, m, k in re.findall(r"\('\\u([0-9a-f]{4})', \.(\w+), (\d+)\)", block("cellT"))]
    rows += [f"state,{i},{w},{q},{h}"
             for i, (w, q, h) in enumerate(re.findall(r"\((true|false), (true|false), (\d+)\)",
                                                      block("stateT")))]
    for name, tag in (("waslT", "wasl"), ("waqfT", "waqf")):
        for s, row in enumerate(re.findall(r"\[([\d, ]+)\]", block(name))):
            rows += [f"{tag},{s},{k},{t}" for k, t in enumerate(row.split(", "))]
    return rows


def test_csv_is_the_kernel_checked_table() -> None:
    kernel = _kernel_rows(KERNEL_DATA.read_text(encoding="utf-8"))
    assert len(kernel) == 116 + 42 + 2 * 42 * 116
    assert CSV.read_text(encoding="utf-8").splitlines() == kernel


def test_one_changed_number_breaks_the_match() -> None:
    """`MUTANT_TABLE_ENTRY`: رقمٌ واحدٌ في انتقال الوصل يتغيّر فيفترق الجدولان."""

    text = KERNEL_DATA.read_text(encoding="utf-8")
    i = text.index("[", text.index(":= [", text.index("def waslT ")) + 4)
    j = text.index(",", i)
    mutant = text[:i + 1] + str(int(text[i + 1:j]) + 1) + text[j:]
    assert CSV.read_text(encoding="utf-8").splitlines() != _kernel_rows(mutant)
