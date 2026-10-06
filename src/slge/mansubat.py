"""بقيّةُ المنصوبات: الحالُ والتمييزُ عمليّةٌ واحدة، والاستثناءُ ثلاثُ عمليّات — مرآةُ `Mansubat.lean`.

الحالُ المفردةُ والتمييزُ على الخانة نكرةٌ منصوبة = فتحٌ فتنوين (`nakira_mansuba`)؛ والفرزُ بينهما
(مشتقٌّ/جامد) يقرؤه القالبُ (`derived`: فَاعِل في `wazn.AWZAN[48]`)، والمعنى معلَن. الاستثناءُ ثلاثُ
حالات = ثلاثُ عمليّات على المستثنى (`mustathna`): نصبٌ في التامّ المثبت، نصبٌ أو بدلٌ في التامّ
المنفيّ، وعمليّةُ الموقع في المفرَّغ (إِلَّا بلا أثرٍ على الخانة). غَيْر مضافةٌ تأخذ حكمَ ما بعد إِلَّا
وما بعدها مجرور (`ghayr_of`)؛ خَلَا/عَدَا/حَاشَا جرٌّ أو نصب وبـ«مَا» نصب (`after_khala`). النفيُ
والتمامُ والرابطُ في الحال الجملة: تيار. القياسُ على MASAQ في `tools/gen_mansubat_index.py`.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Final

from slge.cells import STATES, Cell, licensed
from slge.marifa import al, idafa
from slge.rawabit import PARTICLES, cells_of
from slge.wazn import AWZAN, fill, root_of
from slge.zuruf import jarr, set_last

__all__ = ["DERIVED", "FAAIL", "FAL", "TOOLS", "after_khala", "derived", "ghayr_of", "hal",
           "mustathna", "nakira_mansuba", "tahwil", "tamyiz"]

_A, _I, _U, SUKUN = STATES
FAAIL: Final[int] = 48
FAL: Final[int] = 29
DERIVED: Final[tuple[int, ...]] = (48, 49, 50, 51, 52, 53, 54, 55, 66, 67, 68, 69, 70, 71, 72, 73,
                                   74, 75, 76, 77, 78, 79)
Op = Callable[[tuple[Cell, ...]], tuple[Cell, ...]]


def raf(word: tuple[Cell, ...]) -> tuple[Cell, ...]:
    return set_last(word, _U)


def nasb(word: tuple[Cell, ...]) -> tuple[Cell, ...]:
    return set_last(word, _A)


def nakira_mansuba(word: tuple[Cell, ...]) -> tuple[Cell, ...]:
    """فتحٌ فتنوين (العمليّتان عمليّتا `nawasikh`: الطبقةُ تمنع الاستيراد لا التطابق)."""

    return (*nasb(word), ("ن", SUKUN))


def _on_template(k: int, word: tuple[Cell, ...]) -> bool:
    t = AWZAN[k].template
    r = root_of(t, word)
    return r is not None and fill(t, r) == word


hal: Final[Op] = nakira_mansuba
tamyiz: Final[Op] = nakira_mansuba


def derived(stem: tuple[Cell, ...]) -> bool:
    """قانونُ الفرز: على قالبٍ من قوالب الوصف ⇒ مشتقٌّ (حال)؛ وإلّا فجامدٌ أو قالبٌ لا يقرؤه."""

    return any(_on_template(k, set_last(stem, _U)) for k in DERIVED)


def tahwil(s: tuple[Cell, ...], r: tuple[Cell, ...]) -> tuple[tuple[Cell, ...], tuple[Cell, ...]]:
    """المحوَّلُ عن فاعل: (شَيْبُ الرَّأْسِ) ← (الرَّأْسُ، شَيْبًا)."""

    return al(raf(r)), nakira_mansuba(s)


def mustathna(kind: str, role: Op, badal: bool, word: tuple[Cell, ...]) -> tuple[Cell, ...]:
    """تامّ مثبت ⇒ نصب؛ تامّ منفي ⇒ نصب أو بدل (عمليّةُ المستثنى منه)؛ ناقص منفي ⇒ عمليّةُ الموقع."""

    if kind == "تامّ مثبت":
        return nakira_mansuba(word)
    if kind == "تامّ منفي":
        return role(word) if badal else nakira_mansuba(word)
    return role(word)


def ghayr_of(hukm: Op, word: tuple[Cell, ...]) -> tuple[Cell, ...]:
    return idafa(hukm(cells_of("غَيْرُ")), jarr(word))


def after_khala(ma: bool, word: tuple[Cell, ...]) -> tuple[Cell, ...]:
    return nasb(word) if ma else jarr(word)


TOOLS: Final[tuple[str, ...]] = ("إِلَّا", "غَيْرُ", "سِوَى", "خَلَا", "عَدَا", "حَاشَا")
GATE: Final[frozenset[str]] = frozenset({"إِلَّا", "غَيْرُ", "خَلَا"})


def _check() -> None:
    for w in TOOLS:
        assert licensed(cells_of(w)), w
    shayb, ras = cells_of("شَيْبُ"), cells_of("رَأْسُ")
    assert nakira_mansuba(shayb) == cells_of("شَيْبًا") and tahwil(shayb, ras)[0] == cells_of("اَرَّأْسُ")
    assert derived(cells_of("ضَاحِكُ")) and not derived(cells_of("نَفْسُ"))
    assert mustathna("ناقص منفي", raf, False, shayb) == raf(shayb)
    assert ghayr_of(raf, cells_of("رَجُلُ"))[-1] == ("ل", _I)
    assert after_khala(True, shayb)[-1] == ("ب", _A)
    amal = {p.name: p.amal for p in PARTICLES}
    assert amal["إِلَّا"] == "" and amal["غَيْرُ"] == "جرّ"
    assert FAL == 29


_check()
