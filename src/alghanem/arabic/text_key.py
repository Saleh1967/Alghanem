"""The orthography-insensitive comparison key shared by Arabic card layers.

This lives on its own so that more than one Arabic-layer module can compare
card text by the same rule without importing each other. It is a text utility
only: it asserts no linguistic identity and never replaces a card's own text.
"""

from __future__ import annotations

from typing import Final
from unicodedata import category, normalize

_TATWEEL: Final = "\u0640"
_LETTER_FOLDING: Final = {
    "\u0622": "\u0627",
    "\u0623": "\u0627",
    "\u0625": "\u0627",
    "\u0671": "\u0627",
    "\u0649": "\u064a",
    "\u0629": "\u0647",
}


def comparison_key(value: str) -> str:
    """Return the orthography-insensitive key used to compare card text.

    The key applies the repository's `NFC` normalization form, drops every
    combining mark, invisible formatting character, and `TATWEEL`, and folds
    equivalent `ALEF`, `ALEF MAQSURA`, and `TEH MARBUTA` surface forms. It
    exists only so that comparisons do not silently depend on optional
    diacritics or invisible characters; it asserts no linguistic identity and
    never replaces the card's own text in any reported field.
    """
    unmarked = "".join(
        character
        for character in normalize("NFC", value)
        if category(character) not in {"Mn", "Cf"} and character != _TATWEEL
    )
    return "".join(_LETTER_FOLDING.get(character, character) for character in unmarked)
