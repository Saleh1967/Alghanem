"""العدد: المخالفةُ تاءٌ، والتركيبُ فتحٌ، والعقودُ واوٌ وياء — مرآةُ `formal/Slge/Adad.lean`.

**المخالفة (3–10)**: المذكّرُ = الجذعُ مفتوحًا + تاءٌ بحركة الإعراب؛ المؤنّثُ = الجذعُ بحركة الإعراب:
الفرقُ خانةُ تاءٍ واحدة (`fem_is_masc_without_ta`)، وجنسُ المعدود يُقرأ منها (`gender_of`). **التركيب
(11–19)**: الجزءان مفتوحان، وعَشَر تطابق: عَشَرَ/عَشْرَةَ وشينُها مفتوحةٌ/ساكنة (`shin_law`). **اثنا عشر**:
إعرابُ الجزء الأوّل من مدّه. **العقود**: ُونَ رفعٌ، ِينَ نصبٌ/جرّ (`uqud_case`). **الحياد**: مِائَة وأَلْف
صورةٌ واحدة. **التمييز**: حالةُ المعدود دالّةٌ في مدى العدد (`tamyiz_state`)، تُقاس على MASAQ.
"""

from __future__ import annotations

from typing import Final

from slge.cells import STATES, Cell, licensed
from slge.zuruf import set_last

__all__ = ["STEMS", "TEN_FEM", "TEN_MASC", "UQUD", "compound", "fem", "gender_of", "masc",
           "tamyiz_state", "twelve", "twelve_case", "uqud", "uqud_case"]

_A, _I, _U, SUKUN = STATES


def _s(*cells: Cell) -> tuple[Cell, ...]:
    return cells


STEMS: Final[dict[int, tuple[Cell, ...]]] = {
    3: _s(("ث", _A), ("ل", _A), ("ا", SUKUN), ("ث", _A)),
    4: _s(("ء", _A), ("ر", SUKUN), ("ب", _A), ("ع", _A)),
    5: _s(("خ", _A), ("م", SUKUN), ("س", _A)), 6: _s(("س", _I), ("ت", SUKUN), ("ت", _A)),
    7: _s(("س", _A), ("ب", SUKUN), ("ع", _A)),
    8: _s(("ث", _A), ("م", _A), ("ا", SUKUN), ("ن", _I), ("ي", _A)),
    9: _s(("ت", _I), ("س", SUKUN), ("ع", _A)), 10: _s(("ع", _A), ("ش", SUKUN), ("ر", _A)),
}
TEN_MASC: Final[tuple[Cell, ...]] = _s(("ع", _A), ("ش", _A), ("ر", _A))
TEN_FEM: Final[tuple[Cell, ...]] = _s(("ع", _A), ("ش", SUKUN), ("ر", _A), ("ت", _A))
UQUD: Final[dict[int, tuple[Cell, ...]]] = {
    20: _s(("ع", _I), ("ش", SUKUN), ("ر", _A)), 30: STEMS[3], 40: STEMS[4], 50: STEMS[5],
    60: STEMS[6],
    70: STEMS[7], 80: _s(("ث", _A), ("م", _A), ("ا", SUKUN), ("ن", _A)), 90: STEMS[9],
}


def masc(stem: tuple[Cell, ...], case: str) -> tuple[Cell, ...]:
    """صورةُ المذكّر: الجذعُ مفتوحًا + تاءٌ بحركة الإعراب."""

    return (*set_last(stem, _A), ("ت", case))


def fem(stem: tuple[Cell, ...], case: str) -> tuple[Cell, ...]:
    return set_last(stem, case)


def gender_of(word: tuple[Cell, ...]) -> str | None:
    """جنسُ المعدود من التاء: تاءٌ بعد فتحةِ الجذع ⇒ مذكّر، وإلّا مؤنّث (سِتُّ: تاؤها أصلٌ بعد ساكن)."""

    if not word:
        return None
    return "مذكّر" if word[-1][0] == "ت" and len(word) >= 2 and word[-2][1] == _A else "مؤنّث"


def compound(unit: tuple[Cell, ...], masculine: bool) -> tuple[Cell, ...]:
    """التركيب: الجزءُ الأوّل مفتوحًا + عَشَر مطابِقة."""

    return (*set_last(unit, _A), *(TEN_MASC if masculine else TEN_FEM))


def twelve(raf: bool, masculine: bool) -> tuple[Cell, ...]:
    head = (("ء", _I), ("ث", SUKUN), ("ن", _A)) + (() if masculine else (("ت", _A),))
    return (*head, ("ا" if raf else "ي", SUKUN), *(TEN_MASC if masculine else TEN_FEM))


def twelve_case(word: tuple[Cell, ...]) -> str | None:
    # آخرُ الكلمة: تاءٌ ⇒ عَشْرَةَ (مؤنّث) ⇒ أربعُ خانات؛ وإلّا عَشَرَ ⇒ ثلاث
    n = 4 if word and word[-1][0] == "ت" else 3
    head = word[: len(word) - n]
    if not head:
        return None
    return {"ا": "رفع", "ي": "نصب/جرّ"}.get(head[-1][0]) if head[-1][1] == SUKUN else None


def uqud(stem: tuple[Cell, ...], raf: bool) -> tuple[Cell, ...]:
    return (*set_last(stem, _U if raf else _I), ("و" if raf else "ي", SUKUN), ("ن", _A))


def uqud_case(word: tuple[Cell, ...]) -> str | None:
    if len(word) < 2 or word[-1] != ("ن", _A) or word[-2][1] != SUKUN:
        return None
    return {"و": "رفع", "ي": "نصب/جرّ"}.get(word[-2][0])


def tamyiz_state(n: int) -> tuple[str, bool, bool]:
    """(حالةُ المعدود، منوَّن؟، جمع؟) دالّةً في مدى العدد."""

    if 3 <= n <= 10:
        return (_I, False, True)
    if 11 <= n <= 99:
        return (_A, True, False)
    if n in (100, 1000):
        return (_I, False, False)
    return (_A, False, False)


def _check() -> None:
    for stem in STEMS.values():
        for case in (_U, _A, _I):
            assert gender_of(masc(stem, case)) == "مذكّر" and gender_of(fem(stem, case)) == "مؤنّث"
            assert licensed(masc(stem, case)) and licensed(fem(stem, case))
    for stem in UQUD.values():
        assert uqud_case(uqud(stem, True)) == "رفع" and uqud_case(uqud(stem, False)) == "نصب/جرّ"
    for raf in (True, False):
        for m in (True, False):
            assert twelve_case(twelve(raf, m)) == ("رفع" if raf else "نصب/جرّ")


_check()
