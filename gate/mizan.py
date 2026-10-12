"""الميزان: حكمُ الموصول آلةً منتهيةً جدولُها مولَّدٌ من البرهان (ADR ٤٢).

`formal/a116/mizan.csv` يطبعه `lake exe a116-table mizan` من `A116.Harf`: كلُّ خانةٍ من الـ116
برقمها في الآلة، وكلُّ حالٍ من الـ42 بقبوله وصلًا ووقفًا وحالِه بعد الحدّ، والانتقالُ وصلًا ووقفًا
**على المجال كلِّه**. فالجدولُ هو الدالّةُ نفسُها لا عيّنةٌ منها؛ و`A116.Mizan.machineJoin_eq`/
`machineJoin_pause_eq` تبرهن أنّ هذه الآلة على كلّ طولٍ هي `strictJoinB`/`strictJoinPauseB` بعينهما.
وما هنا مفسِّرُ الجدول وحدَه: طيٌّ على الكلمة بين حدّين (`Harf.run`، `Harf.hadd`)، مطابقٌ لتعريف
`machineJoin` سطرًا بسطر.
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Final

TABLE: Final[Path] = Path(__file__).resolve().parents[1] / "formal" / "a116" / "mizan.csv"
BAD: Final[int] = 0
"""`Harf.Hal.all` أوّلُه `bad'` (`A116.Mizan.bad_first`)."""


def _load() -> tuple[dict[str, int], list[bool], list[bool], list[int], dict[tuple[int, int], int],
                     dict[tuple[int, int], int]]:
    cell: dict[str, int] = {}
    qw: dict[int, bool] = {}
    qq: dict[int, bool] = {}
    hadd: dict[int, int] = {}
    wasl: dict[tuple[int, int], int] = {}
    waqf: dict[tuple[int, int], int] = {}
    with TABLE.open(encoding="utf-8") as fh:
        for line in fh:
            row = line.rstrip("\n").split(",")
            if row[0] == "cell":
                cell[row[1]] = int(row[2])
            elif row[0] == "state":
                i = int(row[1])
                qw[i], qq[i], hadd[i] = row[2] == "true", row[3] == "true", int(row[4])
            else:
                (wasl if row[0] == "wasl" else waqf)[(int(row[1]), int(row[2]))] = int(row[3])
    n = len(qw)
    return (cell, [qw[i] for i in range(n)], [qq[i] for i in range(n)], [hadd[i] for i in range(n)],
            wasl, waqf)


CELL, QABIL_WASL, QABIL_WAQF, HADD, WASL, WAQF = _load()


def run(step: dict[tuple[int, int], int], s: int, word: Sequence[str]) -> int:
    """`Harf.run`: الطيُّ على الكلمة خانةً خانة."""

    for atom in word:
        s = step[(s, CELL[atom])]
    return s


def machine_join(left: Sequence[str], right: Sequence[str], pause: bool) -> bool:
    """`A116.Mizan.machineJoin`: اليسارُ من أوّله، ثمّ الحدّ، ثمّ اليمين — وصلًا أو وقفًا."""

    step = WAQF if pause else WASL
    s = run(step, HADD[run(step, BAD, left)], right)
    return (QABIL_WAQF if pause else QABIL_WASL)[s]
