"""النواسخ: أربعةُ أبوابٍ عمليّتان — مرآةُ `formal/Slge/Nawasikh.lean`.

على الخانات عمليّتان لا غير: `raf` (ضمٌّ في الآخر) و`nasb` (فتحٌ في الآخر). فكان = (رفع، نصب)، وإنّ
عكسُها، وكاد عملُ كان، وظنّ نصبان، ولا النافيةُ للجنس عملُ إنّ. والتنوينُ عمليّةٌ ثالثةٌ منفصلة (`tanwin`):
الحركةُ وحدَها لا تنوينَ معها — ومنه اسمُ لا: فتحٌ بلا تنوينٍ ولا أداة. والكفُّ `kaffa` يُلحق «مَا»، وجدولُ
أدوات الربط يسجّل إِنَّ ناصبةً للاسم وإِنَّمَا بلا عمل. وخبرُ كاد مضارعٌ مرفوع (`afal.form`).

الجامدُ والمتصرّف، والتمامُ، وشرطُ النفي قبل زال، والتعليقُ والإلغاء: تيارٌ ومعجمٌ لا خانة. القياسُ على
MASAQ (بقارئ الحالة `tawabi.case_class`) في `tools/gen_nawasikh_index.py`.
"""

from __future__ import annotations

from typing import Final

from slge.cells import STATES, Cell, licensed
from slge.marifa import has_al
from slge.nida import has_tanwin
from slge.rawabit import PARTICLES, cells_of
from slge.zuruf import set_last

__all__ = ["AMAL", "INNA", "KADA", "KANA", "LA", "ZANNA", "kaffa", "nasb", "raf", "tanwin"]

_A, _I, _U, SUKUN = STATES


def raf(word: tuple[Cell, ...]) -> tuple[Cell, ...]:
    return set_last(word, _U)


def nasb(word: tuple[Cell, ...]) -> tuple[Cell, ...]:
    return set_last(word, _A)


def tanwin(word: tuple[Cell, ...]) -> tuple[Cell, ...]:
    """التنوين: نونٌ ساكنةٌ بعد الحركة — عمليّةٌ منفصلة."""

    return (*word, ("ن", SUKUN))


def kaffa(word: tuple[Cell, ...]) -> tuple[Cell, ...]:
    """«مَا» الزائدةُ تُلحق بالحرف فتكفّه."""

    return (*word, ("م", _A), ("ا", SUKUN))


# عملُ كلّ باب: (ما يصنعه بالاسم، ما يصنعه بالخبر)
AMAL: Final[dict[str, tuple[str, str]]] = {
    "كان": ("رفع", "نصب"), "كاد": ("رفع", "نصب"), "إنّ": ("نصب", "رفع"),
    "لا النافية للجنس": ("نصب", "رفع"), "ظنّ": ("نصب", "نصب"),
}

KANA: Final[tuple[str, ...]] = ("كَانَ", "أَصْبَحَ", "أَضْحَى", "ظَلَّ", "أَمْسَى", "بَاتَ", "صَارَ",
                                "لَيْسَ", "زَالَ", "بَرِحَ", "فَتِئَ", "اِنْفَكَّ", "دَامَ")
KADA: Final[tuple[str, ...]] = ("كَادَ", "كَرَبَ", "أَوْشَكَ", "عَسَى", "حَرَى", "اِخْلَوْلَقَ", "أَنْشَأَ",
                                "طَفِقَ", "جَعَلَ", "هَبَّ", "أَخَذَ", "بَدَأَ")
INNA: Final[tuple[str, ...]] = ("إِنَّ", "أَنَّ", "كَأَنَّ", "لَكِنَّ", "لَيْتَ", "لَعَلَّ")
LA: Final[str] = "لَا"
ZANNA: Final[tuple[str, ...]] = ("ظَنَّ", "حَسِبَ", "خَالَ", "زَعَمَ", "جَعَلَ", "رَأَى", "عَلِمَ", "وَجَدَ",
                                 "دَرَى", "أَلْفَى", "صَيَّرَ", "اِتَّخَذَ", "تَرَكَ", "رَدَّ", "وَهَبَ")

# شواهدُ البوّابة (في المصحف)؛ والباقي مودَعٌ على طريقتها
GATE: Final[frozenset[str]] = frozenset({
    "كَانَ", "أَصْبَحَ", "ظَلَّ", "لَيْسَ", "كَادَ", "عَسَى", "أَنْشَأَ", "جَعَلَ", "أَخَذَ", "بَدَأَ", "إِنَّ",
    "أَنَّ", "كَأَنَّ", "لَيْتَ", "لَعَلَّ", "لَا", "ظَنَّ", "حَسِبَ", "زَعَمَ", "رَأَى", "عَلِمَ", "وَجَدَ",
    "تَرَكَ", "وَهَبَ", "اِتَّخَذَ", "إِنَّمَا", "أَنَّمَا", "كَأَنَّمَا", "مَا", "أَنْ",
})


def _check() -> None:
    for w in KANA + KADA + INNA + ZANNA + (LA,):
        assert licensed(cells_of(w)), w
    ghafur = cells_of("غَفُورُ")
    assert tanwin(nasb(ghafur)) == cells_of("غَفُورًا") and tanwin(raf(ghafur)) == cells_of("غَفُورٌ")
    rayb = cells_of("رَيْبُ")
    assert not has_tanwin(nasb(rayb)) and not has_al(nasb(rayb)) and nasb(rayb) == cells_of("رَيْبَ")
    assert all(licensed(kaffa(cells_of(w))) for w in INNA)
    by_name = {p.name: p.amal for p in PARTICLES}
    assert by_name["إِنَّ"] == "نصب الاسم ورفع الخبر" and by_name["إِنَّمَا"] == ""
    assert cells_of("جَعَلَ") == (("ج", _A), ("ع", _A), ("ل", _A))


_check()
