"""الجزمُ والشرط: ثلاثُ علاماتٍ ثلاثُ عمليّات — مرآةُ `formal/Slge/Jazm.lean`.

العلاماتُ عمليّاتٌ على الخانة: السكونُ (`sukun`، مرخَّصٌ بعد متحرّك وغيرُ مرخَّصٍ بعد مدٍّ فيُلزِم حذفَ
عين الأجوف)، وحذفُ حرف العلّة (`drop_weak`، يترك حركةَ الأصل فلا يُقرأ الجزمُ بعده من الخانة)، وحذفُ
النون (`afal.form(..., "جزم")`، وهو صورةُ النصب بعينها). القارئُ `marker` يردّ الصورةَ إلى سكونٍ أو حذفِ
نونٍ أو لا يقرؤه. والأدواتُ تُعدّ في `JAZIM_ONE`/`SHART_JAZIM`/`SHART_GHAYR` مرخَّصة، ومنها ما خانتُه
خانةُ غيره (لا الناهية = لا النافية؛ لمّا الجازمة = الحينيّة؛ سبعةٌ = الاستفهام). الجزمُ بفعلين والفاءُ
الرابطةُ والامتناع: تيار. القياسُ على MASAQ في `tools/gen_jazm_index.py`.
"""

from __future__ import annotations

from typing import Final

from slge.afal import mood_of, pronoun_of
from slge.cells import STATES, Cell, licensed
from slge.khamsa import MADD
from slge.rawabit import PARTICLES, cells_of
from slge.zuruf import set_last

__all__ = ["JAZIM_ONE", "SHART_GHAYR", "SHART_JAZIM", "amr", "drop_weak", "marker", "sukun",
           "weak_final"]

_A, _I, _U, SUKUN = STATES
_SHORT: Final[dict[str, str]] = {"و": _U, "ا": _A, "ي": _I}


def sukun(word: tuple[Cell, ...]) -> tuple[Cell, ...]:
    return set_last(word, SUKUN)


def drop_weak(word: tuple[Cell, ...]) -> tuple[Cell, ...]:
    return word[:-1]


def weak_final(word: tuple[Cell, ...]) -> bool:
    """الآخرُ مدٌّ من جنس ما قبله؟"""

    if len(word) < 2:
        return False
    m, v = word[-1], word[-2]
    return m[1] == SUKUN and _SHORT.get(m[0]) == v[1]


def amr(word: tuple[Cell, ...]) -> tuple[Cell, ...]:
    """لامُ الأمر: حرفٌ متّصلٌ مكسور."""

    return (("ل", _I), *word)


def marker(word: tuple[Cell, ...]) -> str:
    """سكون | حذف النون | لا تقرؤه الخانة (المعتلُّ بعد الحذف يحمل حركةَ الأصل)."""

    if pronoun_of(word) is not None and mood_of(word) != "رفع":
        return "حذف النون"
    if word and word[-1][1] == SUKUN:
        return "سكون"
    return "لا تقرؤه الخانة"


JAZIM_ONE: Final[tuple[str, ...]] = ("لَمْ", "لَمَّا", "لِ", "لَا")
SHART_JAZIM: Final[tuple[str, ...]] = ("إِنْ", "إِذْمَا", "مَنْ", "مَا", "مَهْمَا", "مَتَى", "أَيَّانَ", "أَيْنَ",
                                       "أَنَّى", "حَيْثُمَا", "كَيْفَمَا", "أَيُّ")
SHART_GHAYR: Final[tuple[str, ...]] = ("إِذَا", "كُلَّمَا", "لَمَّا", "حِينَ", "لَوْ", "لَوْلَا", "لَوْمَا")
GATE: Final[frozenset[str]] = frozenset({
    "لَمْ", "لَمَّا", "لِ", "لَا", "إِنْ", "مَنْ", "مَا", "مَهْمَا", "مَتَى", "أَيَّانَ", "أَيْنَ", "أَنَّى", "أَيُّ",
    "إِذَا", "كُلَّمَا", "حِينَ", "لَوْ", "لَوْلَا",
})


def _check() -> None:
    for w in JAZIM_ONE + SHART_JAZIM + SHART_GHAYR:
        assert licensed(cells_of(w)), w
    yadu, yaqulu = cells_of("يَدْعُو"), cells_of("يَقُولُ")
    assert weak_final(yadu) and not weak_final(yaqulu)
    assert drop_weak(yadu) == cells_of("يَدْعُ") and marker(drop_weak(yadu)) == "لا تقرؤه الخانة"
    assert not licensed(sukun(yaqulu)) and licensed(cells_of("يَقُلْ"))
    assert marker(cells_of("يَلِدْ")) == "سكون" and marker(cells_of("تُبْطِلُوا")) == "حذف النون"
    assert amr(cells_of("يُنْفِقْ")) == cells_of("لِيُنْفِقْ")
    assert cells_of("لَا") == next(p.cells for p in PARTICLES if p.name == "لَا")
    assert MADD["رفع"] == "و"


_check()
