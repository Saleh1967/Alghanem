"""حروفُ `Field112.lean` الثمانيةُ والعشرون هي `LETTER_VOCABULARY` بعينها."""

import re
from pathlib import Path

from alghanem.arabic.letter_fingerprint import LETTER_VOCABULARY

LEAN = Path(__file__).resolve().parents[2] / "formal/a116/A116/Field112.lean"
PATTERN = r'def letters28 : List Char := "([^"]+)"\.toList'


def _lean_letters() -> str:
    match = re.search(PATTERN, LEAN.read_text("utf-8"))
    assert match, "letters28 غائبةٌ عن ملفّ Lean"
    return match.group(1)


def test_lean_letters_are_the_first_28_carriers() -> None:
    assert _lean_letters() == "".join(LETTER_VOCABULARY[:28])


def test_the_29th_carrier_is_the_lone_hamza() -> None:
    assert LETTER_VOCABULARY[28:] == ("ء",)
    assert "carriers29 : List Char := letters28 ++ ['ء']" in LEAN.read_text("utf-8")
