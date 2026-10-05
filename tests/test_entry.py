"""المدخل: ذرّاتُ شهادةِ الغانم ⇄ خانات SLGE، والطيُّ على المرخَّص، والرفضُ بالاسم."""

from __future__ import annotations

import pytest

from conftest import licensed_words
from slge.cells import CELLS, count
from slge.entry import from_atoms, from_integer, to_atoms, to_integer

KITABUN = ("كِ", "تَ", "اْ", "بُ", "نْ")  # ذرّاتُ «كِتَابٌ» كما تُصدرها gate.enter في الغانم
HAJJA = ("حَ", "اْ", "جْ", "جَ")  # «حَاجَّ»: مرخَّصةٌ ثلاثيًّا لا ثنائيًّا


def test_kitabun_enters_as_five_cells_and_exits_byte_for_byte() -> None:
    cells = from_atoms(KITABUN)
    assert cells == (("ك", "كسر"), ("ت", "فتح"), ("ا", "سكون"), ("ب", "ضم"), ("ن", "سكون"))
    assert to_atoms(cells) == KITABUN
    assert from_integer(to_integer(cells), 5) == cells


def test_every_cell_round_trips() -> None:
    for cell in CELLS:
        assert from_atoms(to_atoms((cell,))) == (cell,)


def test_fold_is_a_bijection_on_every_licensed_word_up_to_3() -> None:
    for n in range(4):
        seen = set()
        for w in licensed_words(n):
            k = to_integer(w)
            assert 0 <= k < count(n) and from_integer(k, n) == w
            seen.add(k)
        assert len(seen) == count(n)


def test_ternary_only_word_enters_but_is_not_folded_here() -> None:
    cells = from_atoms(HAJJA)
    assert to_atoms(cells) == HAJJA
    with pytest.raises(ValueError, match="NOT_BINARY_LICENSED"):
        to_integer(cells)


@pytest.mark.parametrize("atom", ["ك", "كِِ", "xَ", "كa", "ة", "كّ", "آ"])
def test_non_atoms_are_refused_by_name(atom: str) -> None:
    with pytest.raises(ValueError, match="NOT_A_116_ATOM"):
        from_atoms((atom,))
