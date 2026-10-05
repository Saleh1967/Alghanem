"""النواة: الخانات، والترخيص، والعدّ، والطيّ."""

from __future__ import annotations

import random

import pytest

from conftest import licensed_words
from slge.cells import (
    ALPHABET,
    CELLS,
    STATES,
    SUKUN,
    a116_code,
    count,
    fold,
    from_a116_code,
    licensed,
    shadow,
    unfold,
)


def test_cells_are_116() -> None:
    assert len(CELLS) == len(set(CELLS)) == 116 == len(ALPHABET) * len(STATES)


def test_a116_code_is_a_bijection_onto_116() -> None:
    codes = [a116_code(c) for c in CELLS]
    assert sorted(codes) == list(range(116))
    assert all(from_a116_code(a116_code(c)) == c for c in CELLS)
    assert all((a116_code(c) >= 87) == (c[1] == SUKUN) for c in CELLS)


def test_empty_word_is_licensed_and_counted() -> None:
    assert licensed(()) and count(0) == 1 and fold(()) == 0 and unfold(0, 0) == []


@pytest.mark.parametrize("n", [1, 2, 3])
def test_count_equals_enumeration(n: int) -> None:
    assert sum(1 for _ in licensed_words(n)) == count(n)


def test_fold_is_a_bijection_exhaustively_upto_2() -> None:
    for n in (0, 1, 2):
        images = [fold(w) for w in licensed_words(n)]
        assert sorted(images) == list(range(count(n)))
        assert all(tuple(unfold(n, fold(w))) == w for w in licensed_words(n))


def test_fold_roundtrip_on_long_random_words() -> None:
    rng = random.Random(116)
    for _ in range(2000):
        n = rng.randint(3, 40)
        k = rng.randrange(count(n))
        w = unfold(n, k)
        assert len(w) == n and licensed(w) and fold(w) == k


def test_fold_rejects_unlicensed() -> None:
    with pytest.raises(ValueError):
        fold([("ب", SUKUN)])
    with pytest.raises(ValueError):
        unfold(2, count(2))


def test_inventory_is_derived_from_U1() -> None:
    u1, carriers = count(1), len(ALPHABET)
    moving = u1 // carriers
    assert u1 % carriers == 0 and moving == 3 and carriers * (moving + 1) == 116


def test_shadow_fails_fold_separates() -> None:
    dhayn = [("ذ", "فتح"), ("ي", SUKUN), ("ن", "كسر")]
    dheen = [("ذ", "كسر"), ("ي", SUKUN), ("ن", "فتح")]
    assert shadow(dhayn) == shadow(dheen)
    assert fold(dhayn) != fold(dheen)


def test_stream_refuses_unlicensed_and_is_prefix_free() -> None:
    """لا يُرمَّز غيرُ المرخَّص؛ وترميزُ كلمةٍ لا يبدأ به ترميزُ أخرى (مرآةُ `encodeWord_prefix_free`)."""

    import pytest

    from slge.stream import decode_word, encode_word

    with pytest.raises(ValueError, match="NOT_LICENSED"):
        encode_word((("ب", "سكون"),))
    a, b = (("م", "فتح"), ("ا", "سكون")), (("م", "كسر"), ("ن", "سكون"))
    ea, eb = encode_word(a), encode_word(b)
    assert ea != eb and ea[: len(eb)] != eb and eb[: len(ea)] != ea
    assert decode_word(ea + eb) == (a, eb)
    assert decode_word(eb) == (b, [])
