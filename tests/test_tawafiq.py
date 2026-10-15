"""توافيقُ الخانات (`A116.Tawafiq`، ADR ٦٣): عددُ المرخَّص من كلّ سلاسل الشبكة (113) بطولٍ معلوم.

١. `tawafiq.csv` (يطبعه Lean المترجَم، ويطابقه CI): أعدادُ الطولين الأوّل والثاني مكتوبةٌ هنا باليد
   من البنية — 84 = 28 × 3، و9,492 = 84 × 84 + 84 × 29، و56 = 28 × 2 — وأعدادُ الطول الثالث تُعاد
   بمرآة البوّابة المستقلّة (`gate.licence`) لا بـLean (`-m slow`: ‎1.44 مليون سلسلة‎).
٢. الثغرةُ المسمّاة `ALIF_CLOSER_NOT_REFUSED`: كُاْ مرخَّصٌ وصلًا في المرآة أيضًا، والألفُ فيه مُغلِق.
الطفرات: `MUTANT_ALIF_ONSET` (29 × 3 = 87)، `MUTANT_BINARY_COUNT` (‎U(2) = 10,092‎)، `MUTANT_3364`.
"""

from __future__ import annotations

import itertools
from pathlib import Path

import pytest

from gate.licence import kind_of, licensable_atom, strict_licensed, strict_pause_licensed

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "formal" / "a116" / "tawafiq.csv"
LICENSABLE = ROOT / "formal" / "a116" / "licensable.csv"


def _rows() -> dict[int, tuple[int, int, int, int]]:
    out: dict[int, tuple[int, int, int, int]] = {}
    for ln in TABLE.read_text(encoding="utf-8").splitlines()[1:]:
        n, *rest = ln.split(",")
        out[int(n)] = tuple(int(x) for x in rest)  # type: ignore[assignment]
    return out


def _cells() -> list[str]:
    cells = [ln.split(",")[0] for ln in LICENSABLE.read_text(encoding="utf-8").splitlines()
             if ln.strip()]
    assert len(cells) == 113 and all(licensable_atom(c) for c in cells)
    return cells


def _count(n: int) -> tuple[int, int, int, int]:
    total = wasl = waqf = closers = 0
    for seq in itertools.product(_cells(), repeat=n):
        a = list(seq)
        total += 1
        if strict_licensed(a):
            wasl += 1
            if a[-1] == "اْ" and kind_of(a)[-1] == "c":
                closers += 1
        if strict_pause_licensed(a):
            waqf += 1
    return total, wasl, waqf, closers


def test_lengths_one_and_two_by_hand() -> None:
    rows = _rows()
    assert rows[1] == (113, 28 * 3, 28 * 3, 0)
    assert rows[2] == (113 ** 2, 84 * 84 + 84 * 29, 84 * 84 + 84 * 29, 28 * 2)
    assert _count(1) == rows[1] and _count(2) == rows[2]


@pytest.mark.slow
def test_length_three_by_independent_mirror() -> None:
    rows = _rows()
    assert rows[3][0] == 113 ** 3 and rows[3][2] == 84 * 113 ** 2 and rows[3][3] == 56 * 84
    assert _count(3) == rows[3]


def test_alif_closer_not_refused() -> None:
    """`ALIF_CLOSER_NOT_REFUSED`: الألفُ الساكنة بعد ضمّةٍ مُغلِقٌ مرخَّص، وبعد فتحةٍ مدّ."""

    assert strict_licensed(["كُ", "اْ"]) and kind_of(["كُ", "اْ"]) == ["cv", "c"]
    assert kind_of(["كَ", "اْ"]) == ["cv", "v"]
    assert strict_pause_licensed(["كَ", "اْ", "اْ"]) and not strict_licensed(["كَ", "اْ", "اْ"])


def test_mutants_rejected() -> None:
    rows = _rows()
    assert 29 * 3 != rows[1][1]                    # MUTANT_ALIF_ONSET: الألفُ حاملَ ابتداء
    assert 87 * 87 + 87 * 29 != rows[2][1]         # MUTANT_BINARY_COUNT: U(2) الثنائيّ على الـ116
    assert 29 * 4 * 29 not in rows[1] + rows[2]    # MUTANT_3364
