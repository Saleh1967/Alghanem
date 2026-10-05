"""الخانة والترخيص والعدّ والطيّ — النواة التي يبرهنها `formal/Slge/Bridge.lean`.

الخانةُ زوجٌ (حامل، حالة): تسعةٌ وعشرون حاملًا في أربع حالات، فهي ‎116‎ خانة.
والكلمةُ **مرخَّصة** إذا لم تبدأ بساكنٍ ولم يتجاور فيها ساكنان.

ترتيبُ SLGE (الهمزةُ أوّلًا؛ «فتح، كسر، ضم، سكون») غيرُ ترتيب الـ116 في الغانم
(الهمزةُ آخرًا؛ «فتحة، ضمّة، كسرة، سكون»). والجسرُ بينهما `a116_code` مبرهَنٌ في
Lean (`Slge.licensed_iff`، `Slge.slgeFold_injective`، `Slge.slgeFold_surjective`،
`Slge.count_eq_U`)، وتطابقُ هذه الشيفرةِ تعريفاتِ Lean يفحصه
`tests/test_conformance.py` على كلّ خانةٍ وكلّ مرخَّصةٍ بطول ‎≤ 2‎ وكلّ ‎U(n)‎ لـ‎n ≤ 12‎.
"""

from __future__ import annotations

from collections.abc import Sequence
from functools import cache
from typing import Final, TypeAlias

__all__ = [
    "A116_CARRIERS",
    "A116_STATES",
    "ALPHABET",
    "CELLS",
    "FORBIDDEN",
    "MOVING",
    "STATES",
    "SUKUN",
    "Cell",
    "Word",
    "a116_code",
    "count",
    "fold",
    "from_a116_code",
    "index",
    "is_cell",
    "licensed",
    "rho_admits",
    "shadow",
    "unfold",
]

Cell: TypeAlias = tuple[str, str]
Word: TypeAlias = Sequence[Cell]

ALPHABET: Final[tuple[str, ...]] = tuple("ءابتثجحخدذرزسشصضطظعغفقكلمنهوي")
STATES: Final[tuple[str, ...]] = ("فتح", "كسر", "ضم", "سكون")
SUKUN: Final[str] = "سكون"
MOVING: Final[tuple[str, ...]] = STATES[:3]
CELLS: Final[tuple[Cell, ...]] = tuple((c, s) for c in ALPHABET for s in STATES)

A116_CARRIERS: Final[tuple[str, ...]] = (*ALPHABET[1:], ALPHABET[0])
"""ترتيبُ الغانم (`letter_fingerprint.LETTER_VOCABULARY`): الهمزةُ في الموضع ‎28‎."""
A116_STATES: Final[tuple[str, ...]] = ("فتح", "ضم", "كسر", "سكون")
"""ترتيبُ الغانم (`THE_DECLARED_HARAKAT`) بأسماء SLGE."""

_FREE: Final[int] = 87
_BLOCKED: Final[int] = 29

FORBIDDEN: Final[frozenset[Cell]] = frozenset(("ا", s) for s in MOVING)
"""قاعدة ρ: الألفُ لا تتحرّك. والهمزةُ حاملٌ مستقلّ (ء). وهذا قيدٌ معجميّ فوق الـ116،
لا جزءٌ من الترخيص: العدُّ ‎U(n)‎ يعدّ الخاناتِ كلَّها."""


def is_cell(x: object) -> bool:
    """أهي خانةٌ من الـ116؟"""

    return isinstance(x, tuple) and len(x) == 2 and x[0] in ALPHABET and x[1] in STATES


def index(cell: Cell) -> int:
    """رمزُ SLGE الأصليّ ‎4·حامل + حالة‎ (فيه فجوات؛ للطيّ الكثيف انظر `fold`)."""

    return 4 * ALPHABET.index(cell[0]) + STATES.index(cell[1])


def licensed(word: Word) -> bool:
    """لا تبدأ بساكن، ولا يتجاور ساكنان. والخاليةُ مرخَّصة (‎U(0) = 1‎).

    مطابقٌ لـ`Slge.licensed` في Lean، والمبرهَنُ أنه `A116.Admissible` بعد الجسر.
    """

    if not word:
        return True
    if word[0][1] == SUKUN:
        return False
    return all(
        not (word[i][1] == SUKUN and word[i + 1][1] == SUKUN) for i in range(len(word) - 1)
    )


def rho_admits(cell: Cell) -> bool:
    """قاعدة ρ: هل الخانةُ خارجَ المثالي المحظور؟"""

    return cell not in FORBIDDEN


def shadow(word: Word) -> str:
    """الظلّ M/S: ما يراه النموذجُ المقطعيّ وحده (متحرّك/ساكن)."""

    return "".join("S" if s == SUKUN else "M" for _, s in word)


def a116_code(cell: Cell) -> int:
    """الجسر: المتحرّكاتُ ‎3ℓ + h‎ (أحرار ‎0…86‎)، والسواكنُ ‎87 + ℓ‎ (محجورون)."""

    carrier, state = cell
    ell = A116_CARRIERS.index(carrier)
    if state == SUKUN:
        return _FREE + ell
    return 3 * ell + A116_STATES.index(state)


def from_a116_code(code: int) -> Cell:
    """معكوسُ `a116_code` على ‎{0, …, 115}‎."""

    if not 0 <= code < _FREE + _BLOCKED:
        raise ValueError(f"رمزٌ خارج الـ116: {code}")
    if code < _FREE:
        return (A116_CARRIERS[code // 3], A116_STATES[code % 3])
    return (A116_CARRIERS[code - _FREE], SUKUN)


def count(n: int) -> int:
    """‎U(n)‎: عددُ المرخَّصات بطول n. ‎U(n+2) = 87·U(n+1) + 87·29·U(n)‎ (`Slge.count_eq_U`)."""

    if n < 0:
        raise ValueError("الطولُ عددٌ طبيعيّ")
    a, b = 1, 87
    for _ in range(n):
        a, b = b, 87 * b + 2523 * a
    return a


@cache
def _s(m: int, open_: bool) -> int:
    """‎S(m, open)‎ في `A116/Fold.lean`."""

    if m == 0:
        return 1
    if open_:
        return _FREE * _s(m - 1, True) + _BLOCKED * _s(m - 1, False)
    return _FREE * _s(m - 1, True)


def fold(word: Word) -> int:
    """طيُّ مرخَّصةٍ إلى ‎{0, …, U(n) − 1}‎: `A116.Fold.fold 87 29 false` بعد الجسر."""

    if not licensed(word):
        raise ValueError("لا يُطوى إلّا المرخَّص")
    codes = [a116_code(c) for c in word]
    total, open_ = 0, False
    for i, x in enumerate(codes):
        rest = len(codes) - 1 - i
        total += min(x, _FREE) * _s(rest, True)
        if open_:
            total += max(x - _FREE, 0) * _s(rest, False)
        open_ = x < _FREE
    return total


def unfold(n: int, k: int) -> list[Cell]:
    """فكُّ ‎k < U(n)‎ إلى المرخَّصة الوحيدة بطول n التي طيُّها k."""

    if not 0 <= k < count(n):
        raise ValueError(f"‎{k}‎ خارج ‎[0, U({n}))‎")
    out: list[int] = []
    for i in range(n):
        m = n - 1 - i
        lo = _FREE * _s(m, True)
        if k < lo:
            out.append(k // _s(m, True))
            k %= _s(m, True)
        else:
            k -= lo
            out.append(_FREE + k // _s(m, False))
            k %= _s(m, False)
    return [from_a116_code(x) for x in out]
