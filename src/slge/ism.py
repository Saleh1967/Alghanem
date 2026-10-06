"""الاسم: بنيتُه حالاتٌ على خانات، وتحويلاتُه عمليّات، وبناؤه العارضُ حالةٌ ثابتة — مرآةُ `Ism.lean`.

المجرّدُ الثلاثيّ عشرةٌ = 3 × 4 − 2 (`TEN`: حركةُ الفاء في حالة العين، يسقط فُعُل وفِعُل)، تُقرأ من
الخانتين الأُوليين (`read_thulathi`)؛ الرباعيُّ والخماسيُّ أشكالُ حالات (`shape`؛ الحصرُ يعدّ الرباعيَّ ستّةً
ويسمّي فَعْلَل مرّتين: خمسةُ أشكال)؛ التصغيرُ ثلاثُ عمليّات (`saghir3/4/5`) يقرؤها `is_tasghir`؛ والنسبُ
عمليّةٌ واحدة (`nisba`) بعد تهيئةٍ مسمّاة (`prepare`) يقرؤها `is_nisba`. البناءُ العارضُ في أبوابه
(`nida`، `nawasikh`، `zuruf`، `adad`). الماهيةُ ومسألةُ الكحل: معلَن/تيار. القياسُ في
`tools/gen_ism_index.py`.
"""

from __future__ import annotations

from typing import Final

from slge.cells import STATES, Cell, licensed
from slge.rawabit import cells_of
from slge.zuruf import set_last

__all__ = ["DROPPED", "KHUMASI", "RUBAI", "TEN", "TWELVE", "is_nisba", "is_tasghir", "nisba",
           "prepare", "read_thulathi", "saghir3", "saghir4", "saghir5", "shape"]

_A, _I, _U, SUKUN = STATES
TWELVE: Final[tuple[tuple[str, str], ...]] = tuple((f, a) for f in (_A, _U, _I)
                                                   for a in (_A, _U, _I, SUKUN))
DROPPED: Final[tuple[tuple[str, str], ...]] = ((_U, _U), (_I, _U))
TEN: Final[tuple[tuple[str, str], ...]] = tuple(p for p in TWELVE if p not in DROPPED)
NAMES: Final[dict[tuple[str, str], str]] = {
    (_A, SUKUN): "فَعْل", (_A, _A): "فَعَل", (_A, _I): "فَعِل", (_A, _U): "فَعُل", (_U, SUKUN): "فُعْل",
    (_U, _A): "فُعَل", (_U, _I): "فُعِل", (_U, _U): "فُعُل", (_I, SUKUN): "فِعْل", (_I, _A): "فِعَل",
    (_I, _I): "فِعِل", (_I, _U): "فِعُل",
}
RUBAI: Final[tuple[str, ...]] = ("جَعْفَرُ", "زِبْرِجُ", "بُرْقُعُ", "دِرْهَمُ", "قِمَطْرُ", "طَحْلَبُ")
KHUMASI: Final[tuple[str, ...]] = ("سَفَرْجَلُ", "جَحْمَرِشُ", "قِرْطَعْبُ", "خُذَاعِرُ")


def read_thulathi(word: tuple[Cell, ...]) -> tuple[str, str] | None:
    return (word[0][1], word[1][1]) if len(word) == 3 else None


def shape(word: tuple[Cell, ...]) -> tuple[str, ...]:
    """حالاتُ الخانات قبل الأخيرة."""

    return tuple(s for _, s in word[:-1])


def saghir3(a: str, b: str, d: str, st: str) -> tuple[Cell, ...]:
    return ((a, _U), (b, _A), ("ي", SUKUN), (d, st))


def saghir4(a: str, b: str, d: str, e: str, st: str) -> tuple[Cell, ...]:
    return ((a, _U), (b, _A), ("ي", SUKUN), (d, _I), (e, st))


def saghir5(a: str, b: str, d: str, e: str, st: str) -> tuple[Cell, ...]:
    return ((a, _U), (b, _A), ("ي", SUKUN), (d, _I), ("ي", SUKUN), (e, st))


def is_tasghir(word: tuple[Cell, ...]) -> bool:
    return len(word) >= 3 and word[0][1] == _U and word[1][1] == _A and word[2] == ("ي", SUKUN)


def nisba(word: tuple[Cell, ...], st: str) -> tuple[Cell, ...]:
    """ياءٌ مشدّدةٌ مكسورٌ ما قبلها."""

    return (*set_last(word, _I), ("ي", SUKUN), ("ي", st))


def prepare(kind: str, word: tuple[Cell, ...]) -> tuple[Cell, ...]:
    """التهيئة: بلا | حذف التاء | مقصور ثالث | مقصور رابع | منقوص ثالث | منقوص رابع."""

    if kind == "بلا":
        return word
    if kind in ("حذف التاء", "مقصور رابع", "منقوص رابع"):
        return word[:-1]
    if kind == "مقصور ثالث":
        return (*word[:-1], ("و", _A))
    if kind == "منقوص ثالث":
        return (*set_last(word[:-1], _A), ("و", _A))
    raise ValueError(kind)


def is_nisba(word: tuple[Cell, ...]) -> bool:
    return len(word) >= 3 and word[-1][0] == "ي" and word[-2] == ("ي", SUKUN) and word[-3][1] == _I


def _check() -> None:
    assert len(TWELVE) == 12 and len(TEN) == 10
    for f, a in TEN:
        assert licensed((("ش", f), ("م", a), ("س", _U)))
    assert read_thulathi(cells_of("رَجُلُ")) == (_A, _U) and (_A, _U) in TEN
    assert len({shape(cells_of(w)) for w in RUBAI}) == 5
    assert len({shape(cells_of(w)) for w in KHUMASI}) == 4
    assert saghir3("ر", "ج", "ل", _U) == cells_of("رُجَيْلُ") and is_tasghir(cells_of("بُنَيَّ"))
    assert saghir4("د", "ر", "ه", "م", _U) == cells_of("دُرَيْهِمُ")
    assert saghir5("ع", "ص", "ف", "ر", _U) == cells_of("عُصَيْفِيرُ")
    assert nisba(cells_of("مِصْرُ"), _U) == cells_of("مِصْرِيُّ")
    assert nisba(prepare("حذف التاء", cells_of("مَكَّةُ")), _U) == cells_of("مَكِّيُّ")
    assert nisba(prepare("مقصور ثالث", cells_of("عَصَا")), _U) == cells_of("عَصَوِيُّ")
    assert nisba(prepare("مقصور رابع", cells_of("مُصْطَفَى")), _U) == cells_of("مُصْطَفِيُّ")
    assert nisba(prepare("منقوص ثالث", cells_of("عَمِي")), _U) == cells_of("عَمَوِيُّ")
    assert nisba(prepare("منقوص رابع", cells_of("قَاضِي")), _U) == cells_of("قَاضِيُّ")
    assert is_nisba(cells_of("عَرَبِيٌّ")[:-1])  # قبل نون التنوين
    assert all(licensed(cells_of(w)) for w in RUBAI + KHUMASI)


_check()
