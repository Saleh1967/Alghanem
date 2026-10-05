"""الأقانيم: الصنفُ مجموعةُ خاناتٍ بعضويّةٍ قابلةٍ للفصل — مرآةُ `formal/Slge/Categories.lean`.

الأقنومُ دالّةٌ على الخانات. والمودَعُ الأوّل **الضمائرُ المنفصلة** الاثنا عشر، خاناتُها من شهادات
بوّابة الغانم (2026-10-06) لا من اليد، ومطابقتُها لجدول Lean في `tests/test_conformance.py`.
المبرهَن هناك: `pronoun_sound` (كلُّها مرخَّصة)، `pronoun_numbers_nodup` (لكلٍّ عددُه)،
`pronoun_shape_not_fingerprint` (الشكلُ ليس بصمة). والاكتمالُ على MASAQ قياسٌ يُطبع لا يُدَّعى.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Final

from slge.cells import ALPHABET, STATES, Cell, fold, licensed

__all__ = ["PRONOUNS", "Aqnum", "exclusive", "pronoun", "sound", "sub"]

Aqnum = Callable[[Sequence[Cell]], bool]


def _c(k: int, s: int) -> Cell:
    return (ALPHABET[k], STATES[s])


PRONOUNS: Final[tuple[tuple[Cell, ...], ...]] = (
    (_c(0, 0), _c(25, 0), _c(1, 3)),                            # أَنَا
    (_c(25, 0), _c(6, 3), _c(25, 2)),                           # نَحْنُ
    (_c(0, 0), _c(25, 3), _c(3, 0)),                            # أَنْتَ
    (_c(0, 0), _c(25, 3), _c(3, 1)),                            # أَنْتِ
    (_c(0, 0), _c(25, 3), _c(3, 2), _c(24, 0), _c(1, 3)),       # أَنْتُمَا
    (_c(0, 0), _c(25, 3), _c(3, 2), _c(24, 3)),                 # أَنْتُمْ
    (_c(0, 0), _c(25, 3), _c(3, 2), _c(25, 3), _c(25, 0)),      # أَنْتُنَّ
    (_c(26, 2), _c(27, 0)),                                     # هُوَ
    (_c(26, 1), _c(28, 0)),                                     # هِيَ
    (_c(26, 2), _c(24, 0), _c(1, 3)),                           # هُمَا
    (_c(26, 2), _c(24, 3)),                                     # هُمْ
    (_c(26, 2), _c(25, 3), _c(25, 0)),                          # هُنَّ
)


def pronoun(w: Sequence[Cell]) -> bool:
    """`Categories.pronoun`: عضويّةُ الضمائر المنفصلة."""

    return tuple(w) in PRONOUNS


def sound(chi: Aqnum, sample: Sequence[Sequence[Cell]]) -> bool:
    """`Sound` على عيّنة: لا يقبل غيرَ مرخَّص."""

    return all(licensed(w) for w in sample if chi(w))


def sub(chi: Aqnum, psi: Aqnum, sample: Sequence[Sequence[Cell]]) -> bool:
    return all(psi(w) for w in sample if chi(w))


def exclusive(chi: Aqnum, psi: Aqnum, sample: Sequence[Sequence[Cell]]) -> bool:
    return not any(psi(w) for w in sample if chi(w))


def fingerprints() -> tuple[int, ...]:
    """أعدادُ الضمائر بطيّها (متباينة، `pronoun_numbers_nodup`)."""

    return tuple(fold(w) for w in PRONOUNS)
