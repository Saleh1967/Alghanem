"""الممنوعُ من الصرف: جرُّه نصبُه، وشرطا صرفه عمليّتان — مرآةُ `formal/Slge/Sarf.lean`.

**القانونُ الحاسم** على الخانات: الممنوعُ لا تنوينَ له وجرُّه بالفتحة، فصورةُ جرّه هي صورةُ نصبه بعينها
(`jarr_eq_nasb`)، بخلاف المنصرف (`sarf_jarr_ne_nasb`). و**شرطا الصرف** عمليّتان: أل (`marifa.al`)
والإضافةُ (`marifa.idafa`)، وبعدهما الكسرُ (`al_jarr_kasra`، `idafa_jarr_kasra`). **العللُ** على نوعين:
ما تقرؤه الخانة — منتهى الجموع (قوالبُ `wazn`)، ألفُ التأنيث المقصورة والممدودة، أوزانُ أَفْعَل/فَعْلَان/
فَعْلَاء/فُعْلَى (صفةٌ أو علمٌ على وزن الفعل) — وما لا تقرؤه: العلمُ بعجمته أو تأنيثه أو تركيبه أو عدله
(معجم). والهمزةُ الأصليّةُ في الممدود (أَبْنَاء) لا تفرّقها الخانة: دَينٌ مسمًّى.
"""

from __future__ import annotations

from typing import Final

from slge.cells import STATES, Cell, licensed
from slge.marifa import al, idafa
from slge.wazn import AWZAN, fill, root_of
from slge.zuruf import set_last

__all__ = ["MUNTAHA", "SIFA", "alif_nun", "illa", "mamduda", "mamnu_jarr", "maqsura", "on_template",
           "sarf_jarr", "sarf_nasb"]

_A, _I, _U, SUKUN = STATES
NUN: Final[Cell] = ("ن", SUKUN)
MUNTAHA: Final[tuple[int, ...]] = (101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112)
SIFA: Final[tuple[int, ...]] = (54, 55, 80, 81, 82)


def sarf_jarr(word: tuple[Cell, ...]) -> tuple[Cell, ...]:
    return (*set_last(word, _I), NUN)


def sarf_nasb(word: tuple[Cell, ...]) -> tuple[Cell, ...]:
    return (*set_last(word, _A), NUN)


def mamnu_jarr(word: tuple[Cell, ...]) -> tuple[Cell, ...]:
    """جرُّ الممنوع: فتحٌ بلا تنوين — وهو نصبُه بعينه."""

    return set_last(word, _A)


def al_jarr(word: tuple[Cell, ...]) -> tuple[Cell, ...]:
    return al(set_last(word, _I))


def idafa_jarr(word: tuple[Cell, ...], suffix: tuple[Cell, ...]) -> tuple[Cell, ...]:
    return idafa(set_last(word, _I), suffix)


def on_template(k: int, word: tuple[Cell, ...]) -> bool:
    t = AWZAN[k].template
    r = root_of(t, word)
    return r is not None and fill(t, r) == word


def maqsura(word: tuple[Cell, ...]) -> bool:
    return len(word) >= 4 and word[-1] == ("ا", SUKUN) and word[-2][1] == _A


def mamduda(word: tuple[Cell, ...]) -> bool:
    return len(word) >= 4 and word[-1][0] == "ء" and word[-2] == ("ا", SUKUN) and word[-3][1] == _A


def alif_nun(word: tuple[Cell, ...]) -> bool:
    """الألفُ والنونُ الزائدتان بعد ثلاثةٍ فأكثر."""

    return len(word) >= 5 and word[-1][0] == "ن" and word[-2] == ("ا", SUKUN)


def illa(word: tuple[Cell, ...]) -> str:
    """علّةُ الصيغة المقروءة من الخانة؛ «معجم» لما لا تقرؤه (علمٌ) أو للمنصرف."""

    w2 = set_last(word, _U)
    if any(on_template(k, w2) for k in MUNTAHA):
        return "صيغة منتهى الجموع"
    if mamduda(word):
        return "ألف التأنيث الممدودة"
    if maqsura(word):
        return "ألف التأنيث المقصورة"
    if any(on_template(k, w2) for k in SIFA):
        return "وزن أَفْعَل/فَعْلَان (صفةٌ أو علم)"
    if alif_nun(word):
        return "ألف ونون زائدتان"
    return "معجم"


def _check() -> None:
    masajid = (("م", _A), ("س", _A), ("ا", SUKUN), ("ج", _I), ("د", _A))
    assert illa(masajid) == "صيغة منتهى الجموع" and mamnu_jarr(masajid) == masajid
    assert sarf_jarr(masajid) != sarf_nasb(masajid) and licensed(sarf_jarr(masajid))
    assert al_jarr(masajid)[-1][1] == _I
    assert illa((("ء", _A), ("ا", SUKUN), ("د", _A), ("م", _A))) == "وزن أَفْعَل/فَعْلَان (صفةٌ أو علم)"


_check()
