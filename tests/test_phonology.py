"""الصفات والمخارج."""

from __future__ import annotations

from slge.cells import ALPHABET
from slge.phonology import LETTERS, MAHRAJ, PAIRS, PLACES, features


def test_letters_are_the_29() -> None:
    assert LETTERS == ALPHABET and set(MAHRAJ) == set(LETTERS)


def test_every_letter_has_a_full_vector() -> None:
    for c in LETTERS:
        f = features(c)
        assert set(f) == {p[0] for p in PAIRS} and set(f.values()) <= {"+", "-", "بيني"}


def test_pairs_partition() -> None:
    for name, _opp, pos, bet in PAIRS:
        neg = {c for c in LETTERS if features(c)[name] == "-"}
        assert set(pos) | set(bet) | neg == set(LETTERS)


def test_jawf_is_madd() -> None:
    assert {c for c, (place, _) in MAHRAJ.items() if place == "الجوف"} == {"ا", "و", "ي"}
    assert all(place in PLACES for place, _ in MAHRAJ.values())
