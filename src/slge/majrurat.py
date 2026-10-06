"""المجرورات: الجرُّ عمليّةٌ واحدة على الخانة، وسببُه في الحدّ — مرآةُ `formal/Slge/Majrurat.lean`.

`jarr` كسرٌ في الآخر (وللنكرة `tanwin`)؛ الياءُ في الجمع السالم (`adad.uqud`) والمثنّى (`dual`) نصبٌ أو
جرّ لا تفصلهما الخانة؛ والأسماءُ الخمسة بالياء لا يقرؤها القارئُ العامّ؛ والفتحةُ في الممنوع تُقرأ نصبًا
والجرُّ من جدول العلل. حروفُ الجرّ مودَعة (`HARFS`، المتّصلةُ الخمسةُ أوّلًا)؛ والإضافةُ تُسقط التنوينَ ونونَ
الجمع والمثنّى (`mudaf_uqud`، `mudaf_dual`)؛ واللفظيّةُ يقرؤها القالب (`mansubat.derived`)؛ والتبعيّةُ
توافقٌ (`tawabi.follows`). القياسُ على MASAQ في `tools/gen_majrurat_index.py`.
"""

from __future__ import annotations

from typing import Final

from slge.adad import uqud
from slge.cells import STATES, Cell, licensed
from slge.marifa import drop_tanwin, idafa
from slge.rawabit import PARTICLES, cells_of
from slge.zuruf import set_last

__all__ = ["HARFS", "PROCLITIC", "dual", "jarr", "jarr_nakira", "mudaf", "mudaf_dual",
           "mudaf_uqud"]

_A, _I, _U, SUKUN = STATES


def jarr(word: tuple[Cell, ...]) -> tuple[Cell, ...]:
    return set_last(word, _I)


def jarr_nakira(word: tuple[Cell, ...]) -> tuple[Cell, ...]:
    return (*jarr(word), ("ن", SUKUN))


def dual(stem: tuple[Cell, ...]) -> tuple[Cell, ...]:
    """المثنّى مجرورًا/منصوبًا: فتحٌ فياءٌ ساكنةٌ فنونٌ مكسورة."""

    return (*set_last(stem, _A), ("ي", SUKUN), ("ن", _I))


def mudaf(word: tuple[Cell, ...], suffix: tuple[Cell, ...]) -> tuple[Cell, ...]:
    """قانونُ حسم المضاف: إسقاطُ التنوين ثمّ الإلحاق."""

    return idafa(word, suffix)


def mudaf_uqud(stem: tuple[Cell, ...], raf: bool) -> tuple[Cell, ...]:
    """مضافٌ من الجمع السالم: تسقط النون."""

    return uqud(stem, raf)[:-1]


def mudaf_dual(stem: tuple[Cell, ...]) -> tuple[Cell, ...]:
    return dual(stem)[:-1]


PROCLITIC: Final[tuple[str, ...]] = ("بِ", "لِ", "كَ", "وَ", "تَ")
HARFS: Final[tuple[str, ...]] = (*PROCLITIC, "مِنْ", "إِلَى", "عَنْ", "عَلَى", "فِي", "حَتَّى", "مُذْ", "مُنْذُ",
                                 "خَلَا", "عَدَا", "حَاشَا", "رُبَّ")
GATE: Final[frozenset[str]] = frozenset({"مِنْ", "إِلَى", "عَنْ", "عَلَى", "فِي", "حَتَّى", "خَلَا"})


def _check() -> None:
    for w in HARFS:
        assert licensed(cells_of(w)), w
    rajul = cells_of("رَجُلُ")
    assert jarr_nakira(rajul) == cells_of("رَجُلٍ") and licensed(jarr(rajul))
    assert dual(rajul) == cells_of("رَجُلَيْنِ")
    assert mudaf_uqud(cells_of("مُهَنْدِسُ"), True) == cells_of("مُهَنْدِسُو")
    kitab = mudaf(cells_of("كِتَابٌ"), jarr_nakira(cells_of("مُحَمَّدُ")))
    assert kitab == cells_of("كِتَابُ") + cells_of("مُحَمَّدٍ")
    assert drop_tanwin(cells_of("كِتَابٌ")) == cells_of("كِتَابُ")
    amal = {p.name: p.amal for p in PARTICLES}
    assert all(amal[h] == "جرّ" for h in ("بِ", "لِ", "كَ", "مِنْ", "إِلَى", "عَنْ", "عَلَى", "حَتَّى"))


_check()
