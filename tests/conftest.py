"""أدواتٌ مشتركة: تعدادُ المرخَّصات، وجذرُ المستودع."""

from __future__ import annotations

from collections.abc import Iterator
from itertools import product
from pathlib import Path

from slge.cells import CELLS, Cell, licensed

ROOT = Path(__file__).resolve().parent.parent


def licensed_words(n: int) -> Iterator[tuple[Cell, ...]]:
    """كلُّ مرخَّصةٍ بطول n، بترتيب `product` على `CELLS`."""

    for w in product(CELLS, repeat=n):
        if licensed(w):
            yield w
