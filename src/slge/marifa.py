"""المعارف: التعريفُ عمليّاتٌ على الخانات، والنكرةُ ما بقي — مرآةُ `formal/Slge/Marifa.lean`.

السبعةُ ثلاثةُ أصناف: **بالذات** (الضمير، الإشارة، الموصول: جداولُ صورٍ؛ والعلمُ معجمٌ لا خانة)؛
**بالأداة**: `al` همزةٌ مفتوحةٌ فلامٌ ساكنة ثمّ الإدغامُ الشمسيُّ في أربعةَ عشرَ حرفًا (`shamsi`؛ يحفظ
الترخيص لأنّه لا يغيّر نمطَ السكون)، والأداةُ تُقرأ من الصدر (`has_al`)؛ **بالتبعية**: الإضافةُ تُسقط
التنوينَ ثمّ تُلحق (`idafa`)، فالمضافُ لا تنوينَ له (`idafa_no_tanwin`). والقانونُ المقيس على MASAQ:
التنوينُ والأداةُ لا يجتمعان، والمضافُ لا يُنوَّن إلّا تنوينَ العوض (يَوْمَئِذٍ، كُلٍّ)؛ والعلمُ يُنوَّن إن
انصرف فالتنوينُ ليس علامةَ تنكير. والقوّةُ ترتيبٌ معلَن؛ والمستترُ بلا خانة؛ ومَنْ نونُها أصلٌ تقرؤها
الخانةُ كتنوين (تشابهٌ مسمًّى).
"""

from __future__ import annotations

from typing import Final

from slge.cells import ALPHABET, STATES, Cell, licensed
from slge.damair import ATTACHED_NASB
from slge.ishara import FORMS as ISHARA_FORMS
from slge.istifham import MA, MAN, ayy
from slge.nida import has_tanwin

__all__ = ["MAWSUL", "SUN", "al", "drop_tanwin", "has_al", "idafa", "kind_of", "shamsi"]

_A, _I, _U, SUKUN = STATES
SUN: Final[frozenset[str]] = frozenset("تثدذرزسشصضطظلن")
assert all(s in ALPHABET for s in SUN)


def shamsi(word: tuple[Cell, ...]) -> tuple[Cell, ...]:
    """لامٌ ساكنةٌ بعد الهمزة قبل شمسيٍّ تصير ذلك الحرفَ ساكنًا."""

    if len(word) >= 3 and word[1] == ("ل", SUKUN) and word[2][0] in SUN:
        return (word[0], (word[2][0], SUKUN), *word[2:])
    return word


def al(word: tuple[Cell, ...]) -> tuple[Cell, ...]:
    """التعريفُ بأل (ألفُ الوصل بقيّةُ رسم في الشهادة)."""

    return shamsi((("ء", _A), ("ل", SUKUN), *word))


def has_al(word: tuple[Cell, ...]) -> bool:
    if len(word) < 2 or word[0] != ("ء", _A) or word[1][1] != SUKUN:
        return False
    if word[1][0] == "ل":
        return True
    return len(word) >= 3 and word[1][0] in SUN and word[2][0] == word[1][0]


def drop_tanwin(word: tuple[Cell, ...]) -> tuple[Cell, ...]:
    return word[:-1] if has_tanwin(word) else word


def idafa(word: tuple[Cell, ...], suffix: tuple[Cell, ...]) -> tuple[Cell, ...]:
    """الإضافة: إسقاطُ التنوين ثمّ الإلحاق."""

    return (*drop_tanwin(word), *suffix)


MAWSUL: Final[dict[str, tuple[Cell, ...]]] = {
    "الَّذِي": al((("ل", _A), ("ذ", _I), ("ي", SUKUN))),
    "الَّتِي": al((("ل", _A), ("ت", _I), ("ي", SUKUN))),
    "اللَّذَانِ": al((("ل", _A), ("ذ", _A), ("ا", SUKUN), ("ن", _I))),
    "اللَّتَانِ": al((("ل", _A), ("ت", _A), ("ا", SUKUN), ("ن", _I))),
    "اللَّذَيْنِ": al((("ل", _A), ("ذ", _A), ("ي", SUKUN), ("ن", _I))),
    "اللَّتَيْنِ": al((("ل", _A), ("ت", _A), ("ي", SUKUN), ("ن", _I))),
    "الَّذِينَ": al((("ل", _A), ("ذ", _I), ("ي", SUKUN), ("ن", _A))),
    "اللَّاتِي": al((("ل", _A), ("ا", SUKUN), ("ت", _I), ("ي", SUKUN))),
    "اللَّائِي": al((("ل", _A), ("ا", SUKUN), ("ء", _I), ("ي", SUKUN))),
    "اللَّوَاتِي": al((("ل", _A), ("و", _A), ("ا", SUKUN), ("ت", _I), ("ي", SUKUN))),
    "مَنْ": MAN, "مَا": MA, "أَيُّ": ayy(_U), "ذُو": (("ذ", _U), ("و", SUKUN)),
}
"""الموصولةُ الأربعَ عشرةَ؛ الشدّةُ في الَّذِي خانتان بعد اللام الساكنة كما تُخرجها البوّابة."""

_ISHARA = frozenset(f.cells for f in ISHARA_FORMS)
_SUFFIXES = frozenset(p.cells for p in ATTACHED_NASB)


def kind_of(word: tuple[Cell, ...]) -> str:
    """الصنفُ المقروء من الخانة: إشارةٌ، موصولٌ، معرَّفٌ بأل، مضافٌ إلى ضمير، أو «لا تقرؤه الخانة»
    (علمٌ أو نكرةٌ أو منادًى مقصود: من المعجم والتيار)."""

    if word in _ISHARA:
        return "اسم إشارة"
    if word in MAWSUL.values():
        return "اسم موصول"
    if has_al(word):
        return "معرَّف بأل"
    if any(len(word) > len(s) and word[-len(s):] == s for s in _SUFFIXES):
        return "مضاف إلى ضمير"
    return "لا تقرؤه الخانة"


def _check() -> None:
    kitab = (("ك", _I), ("ت", _A), ("ا", SUKUN), ("ب", _U))
    assert has_al(al(kitab)) and licensed(al(kitab))
    rahman = (("ر", _A), ("ح", SUKUN), ("م", _A), ("ن", _I))
    assert al(rahman)[:3] == (("ء", _A), ("ر", SUKUN), ("ر", _A))
    assert not has_tanwin(idafa((*kitab, ("ن", SUKUN)), (("ك", _A),)))
    assert all(licensed(w) for w in MAWSUL.values())


_check()
