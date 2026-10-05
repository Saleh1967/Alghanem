"""المدخلُ الوحيد إلى العمود: شهادةُ بوّابة الغانم ← خاناتُ SLGE، وبالعكس.

لا نصَّ هنا. ما يدخل هو ذرّاتُ الشهادة التي أصدرتها `gate.enter(bytes)` في مستودع الغانم
(بروتوكول A116-CANONICAL-TXT-1.1): كلُّ ذرّةٍ حاملٌ وعلامةٌ من أربع. وهذه الوحدةُ تُسقطها
على خانات SLGE `(حامل، حالة)` بالجسر المبرهَن في `formal/Slge/Bridge.lean`
(`Slge.ofCell_toCell`، `Slge.toCell_ofCell`)، وتُعيدها ذرّاتٍ بعينها للمخرج.

* `from_atoms(atoms)` — ذرّاتُ الشهادة ← خانات. ترفض (`ValueError`) ذرّةً ليست من الـ116.
* `to_atoms(cells)` — خانات ← ذرّاتُ الشهادة، للعودة إلى `gate.exit`.
* `from_integer(code, length)` / `to_integer(cells)` — الطيُّ المبرهَن (`Slge.slgeFold_*`) على
  مرخَّصةٍ ثنائيًّا؛ أمّا ما رخّصه الثلاثيُّ وحدَه (مدٌّ ثمّ مشدَّد، كـ«حَاجَّ») فيدخل خاناتٍ ولا يُطوى هنا، وعددُه
  في شهادته (`Certificate.integer`) لا هنا.

وهذا المدخلُ لا يستورد بوّابةَ الغانم: الشهادةُ تصل بتّاتٍ (ذرّاتٍ وعددًا) من مستودعها، ويبقى
هذا المستودع خاليًا من أيّ قارئٍ للنصّ (`tests/test_guard.py`).
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Final

from slge.cells import ALPHABET, SUKUN, Cell, fold, licensed, unfold

__all__ = ["MARKS", "from_atoms", "from_integer", "to_atoms", "to_integer"]

MARKS: Final[dict[str, str]] = {"َ": "فتح", "ِ": "كسر", "ُ": "ضم", "ْ": SUKUN}
"""علامةُ الذرّة في الشهادة ← حالةُ الخانة في SLGE."""

_MARK_OF: Final[dict[str, str]] = {v: k for k, v in MARKS.items()}
_CARRIERS: Final[frozenset[str]] = frozenset(ALPHABET)


def from_atoms(atoms: Iterable[str]) -> tuple[Cell, ...]:
    """ذرّاتُ شهادةٍ ← خانات. كلُّ ذرّةٍ حرفان: حاملٌ من التسعة والعشرين وعلامةٌ من الأربع."""

    out: list[Cell] = []
    for a in atoms:
        if len(a) != 2 or a[0] not in _CARRIERS or a[1] not in MARKS:
            raise ValueError(f"NOT_A_116_ATOM:{a!r}")
        out.append((a[0], MARKS[a[1]]))
    return tuple(out)


def to_atoms(cells: Sequence[Cell]) -> tuple[str, ...]:
    """خانات ← ذرّاتُ الشهادة بعينها (`from_atoms` معكوسةً)."""

    return tuple(c + _MARK_OF[s] for c, s in cells)


def to_integer(cells: Sequence[Cell]) -> int:
    """الطيُّ المبرهَن على مرخَّصةٍ ثنائيًّا؛ وإلّا `ValueError` باسمه."""

    if not licensed(cells):
        raise ValueError("NOT_BINARY_LICENSED: يُؤخذ العددُ من الشهادة لا من هنا")
    return fold(cells)


def from_integer(code: int, length: int) -> tuple[Cell, ...]:
    """الفكُّ المبرهَن: العددُ ‎< U(length)‎ وطولُه ← الخانات."""

    return tuple(unfold(length, code))
