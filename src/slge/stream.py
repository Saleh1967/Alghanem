"""التسلسل: النصُّ تيارُ شهاداتٍ ذاتيُّ الحدّ — مرآةُ `formal/Slge/Sequence.lean`.

لا فاصلَ بين الكلمات ولا حاملَ زائد: طولُ الكلمة أُحاديًّا (‎k‎ آحادٍ ثمّ صفر)، ثمّ عددُها
‎n = fold(w) < U(k)‎ بعرضٍ ثابت ‎width(k) = ⌊log₂ U(k)⌋ + 1‎ (الخانةُ الدنيا أوّلًا).
المبرهَن هناك: `decodeWord_encodeWord` (ذاتيّةُ الحدّ)، `encodeWord_prefix_free` (التفكيكُ وحيد)،
`decode_encode` (التيارُ يعود كلُّه). وهذه الدوالّ تُطابَق بجدول Lean في `tests/test_conformance.py`.
الكلفةُ معلنة: ‎cost(k) = (k + 1) + width(k)‎ بتًّا.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence

from slge.cells import Cell, count, fold, licensed, unfold

__all__ = ["cost", "decode", "decode_word", "encode", "encode_word", "width"]


def width(k: int) -> int:
    """‎log₂ U(k) + 1‎ (`Sequence.width`)."""

    return count(k).bit_length()


def cost(k: int) -> int:
    return (k + 1) + width(k)


def _nat_to_bits(w: int, n: int) -> list[bool]:
    return [bool((n >> i) & 1) for i in range(w)]


def _bits_to_nat(bits: Sequence[bool]) -> int:
    return sum(1 << i for i, b in enumerate(bits) if b)


def encode_word(w: Sequence[Cell]) -> list[bool]:
    """`Sequence.encodeWord`: الطولُ أُحاديًّا ثمّ العددُ بعرضه؛ لا يرمَّز إلّا المرخَّص."""

    if not licensed(w):
        raise ValueError("NOT_LICENSED: لا يُرمَّز إلّا المرخَّص")
    k = len(w)
    return [True] * k + [False] + _nat_to_bits(width(k), fold(w))


def decode_word(bits: Sequence[bool]) -> tuple[tuple[Cell, ...], list[bool]] | None:
    """`Sequence.decodeWord`: كلمةٌ من رأس التيار وما بعدها، أو `None`."""

    k = 0
    while k < len(bits) and bits[k]:
        k += 1
    if k >= len(bits):
        return None
    rest = list(bits[k + 1 :])
    w = width(k)
    if w > len(rest):
        return None
    return tuple(unfold(k, _bits_to_nat(rest[:w]))), rest[w:]


def encode(words: Iterable[Sequence[Cell]]) -> list[bool]:
    out: list[bool] = []
    for w in words:
        out.extend(encode_word(w))
    return out


def decode(bits: Sequence[bool]) -> list[tuple[Cell, ...]]:
    """`Sequence.decodeN` بوقودٍ كافٍ: يفكّ حتى أوّل تعذّر."""

    out: list[tuple[Cell, ...]] = []
    rest = list(bits)
    while rest:
        got = decode_word(rest)
        if got is None:
            break
        w, rest = got
        out.append(w)
    return out
