"""السوابقُ قبل الفعل المبنيّ — مرآةُ `A116.Sawabiq` (ADR ٤٦).

قائمةٌ مغلقة بترتيبٍ لا يُبدَّل: همزةُ الاستفهام «أَ» ← العاطفة «وَ» أو «فَ» ← اللام «لَ». والمرشَّحاتُ
(`candidates`) الكلمةُ أوّلًا ثمّ ما يبقى بعد كلّ سلسلةٍ مرتّبة، كلُّها لواحقُ للكلمة (`candidates_suffix`)،
واثنا عشر على الأكثر (`candidates_length_le`)، والجذعُ بعينه بينها (`peel_exact`).
"""

from __future__ import annotations

from typing import Final

FATHA: Final[str] = "َ"
SLOT1: Final[tuple[str, ...]] = ("", "أ" + FATHA)
SLOT2: Final[tuple[str, ...]] = ("", "و" + FATHA, "ف" + FATHA)
SLOT3: Final[tuple[str, ...]] = ("", "ل" + FATHA)


def _step(opts: tuple[str, ...], ws: list[str]) -> list[str]:
    return [w[len(p):] for w in ws for p in opts if w.startswith(p)]


def candidates(word: str) -> list[str]:
    """الكلمةُ أوّلًا، ثمّ ما يبقى بعد تقشير كلّ سلسلةٍ مرتّبةٍ من السوابق (بترتيب Lean)."""

    return _step(SLOT3, _step(SLOT2, _step(SLOT1, [word])))
