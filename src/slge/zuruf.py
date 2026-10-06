"""ظروفُ المكان: الإضافةُ والقطعُ والجرُّ في الخانة الأخيرة — مرآةُ `formal/Slge/Zuruf.lean`.

الظرفُ المعربُ جذعٌ وخانةُ إعرابٍ في آخره تقرأ ثلاثةَ أحوال (`hukm`): فتحٌ ⇒ منصوبٌ مضافًا؛ كسرٌ ⇒
مجرورٌ بالجارّ (أو مضافٌ إلى ياء المتكلّم)؛ ضمٌّ ⇒ **مقطوعٌ عن الإضافة** مبنيًّا على الضمّ. والقطعُ
والجرُّ والإضافةُ عمليّاتٌ على الخانة الأخيرة (`set_last`) تحفظ الترخيصَ (`setLast_licensed`)
ويقرؤها الحكم (`hukm_qat`…). والثوابتُ المبنيّة صورةٌ واحدة: حَيْثُ (ضمٌّ لازم)، لَدُنْ، لَدَى، ثَمَّ، هُنَا.
والمختصُّ (المسجد، البيت) ليس ظرفًا: قيدٌ معجميّ لا خانة. والمقاديرُ (مِيل، فَرْسَخ) أسماءٌ تُعرب
كالمعرب نفسِه: لم تُودَع لغياب شاهدها.

القياسُ على شريحة MASAQ المجمَّدة (1,493 ظرفًا بشهادات البوّابة) في `tools/gen_zuruf_index.py`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from slge.cells import STATES, Cell, licensed

__all__ = ["CONSTANTS", "STEMS", "Zarf", "hukm", "jarr", "mudaf", "qat", "set_last"]

_A, _I, _U, SUKUN = STATES
HUKM: Final[dict[str, str]] = {_A: "منصوب مضاف", _I: "مجرور",
                               _U: "مقطوع عن الإضافة (مبني على الضم)"}


def hukm(word: tuple[Cell, ...]) -> str:
    if not word:
        return "لا تقرؤه الخانة"
    return HUKM.get(word[-1][1], "لا تقرؤه الخانة")


def set_last(word: tuple[Cell, ...], state: str) -> tuple[Cell, ...]:
    if not word:
        return word
    return (*word[:-1], (word[-1][0], state))


def mudaf(stem: tuple[Cell, ...]) -> tuple[Cell, ...]:
    return set_last(stem, _A)


def jarr(stem: tuple[Cell, ...]) -> tuple[Cell, ...]:
    return set_last(stem, _I)


def qat(stem: tuple[Cell, ...]) -> tuple[Cell, ...]:
    """القطعُ عن الإضافة."""

    return set_last(stem, _U)


@dataclass(frozen=True, slots=True)
class Zarf:
    name: str
    stem: tuple[Cell, ...]
    bab: str  # الجهات الست | مقادير | مصدر | معرب آخر | ثابت
    witnessed: tuple[str, ...]  # الصورُ التي عادت من البوّابة: فتح/كسر/ضم


def _s(*cells: Cell) -> tuple[Cell, ...]:
    return cells


STEMS: Final[tuple[Zarf, ...]] = (
    Zarf("فَوْق", _s(("ف", _A), ("و", SUKUN), ("ق", _A)), "الجهات الست", ("فتح", "كسر")),
    Zarf("تَحْت", _s(("ت", _A), ("ح", SUKUN), ("ت", _A)), "الجهات الست", ("فتح", "كسر")),
    Zarf("خَلْف", _s(("خ", _A), ("ل", SUKUN), ("ف", _A)), "الجهات الست", ()),
    Zarf("وَرَاء", _s(("و", _A), ("ر", _A), ("ا", SUKUN), ("ء", _A)), "الجهات الست", ("فتح", "كسر")),
    Zarf("أَمَام", _s(("ء", _A), ("م", _A), ("ا", SUKUN), ("م", _A)), "الجهات الست", ()),
    Zarf("يَمِين", _s(("ي", _A), ("م", _I), ("ي", SUKUN), ("ن", _A)), "الجهات الست", ()),
    Zarf("شِمَال", _s(("ش", _I), ("م", _A), ("ا", SUKUN), ("ل", _A)), "الجهات الست", ()),
    Zarf("يَسَار", _s(("ي", _A), ("س", _A), ("ا", SUKUN), ("ر", _A)), "الجهات الست", ()),
    Zarf("بَيْن", _s(("ب", _A), ("ي", SUKUN), ("ن", _A)), "معرب آخر", ("فتح", "كسر")),
    Zarf("حَوْل", _s(("ح", _A), ("و", SUKUN), ("ل", _A)), "معرب آخر", ("فتح", "كسر")),
    Zarf("تِلْقَاء", _s(("ت", _I), ("ل", SUKUN), ("ق", _A), ("ا", SUKUN), ("ء", _A)), "معرب آخر",
         ("فتح", "كسر")),
    Zarf("تِجَاه", _s(("ت", _I), ("ج", _A), ("ا", SUKUN), ("ه", _A)), "معرب آخر", ()),
    Zarf("نَحْو", _s(("ن", _A), ("ح", SUKUN), ("و", _A)), "معرب آخر", ()),
    Zarf("قَبْل", _s(("ق", _A), ("ب", SUKUN), ("ل", _A)), "مقطوع", ("فتح", "كسر", "ضم")),
    Zarf("بَعْد", _s(("ب", _A), ("ع", SUKUN), ("د", _A)), "مقطوع", ("فتح", "كسر", "ضم")),
    Zarf("عِنْد", _s(("ع", _I), ("ن", SUKUN), ("د", _A)), "معرب آخر", ("فتح", "كسر")),
    Zarf("دُون", _s(("د", _U), ("و", SUKUN), ("ن", _A)), "معرب آخر", ("فتح", "كسر")),
)

CONSTANTS: Final[dict[str, tuple[Cell, ...]]] = {
    "حَيْثُ": _s(("ح", _A), ("ي", SUKUN), ("ث", _U)),
    "لَدُنْ": _s(("ل", _A), ("د", _U), ("ن", SUKUN)),
    "لَدَى": _s(("ل", _A), ("د", _A), ("ا", SUKUN)),
    "ثَمَّ": _s(("ث", _A), ("م", SUKUN), ("م", _A)),  # = ishara.THAMMA؛ تطابقُه conformance
    "هُنَا": _s(("ه", _U), ("ن", _A), ("ا", SUKUN)),   # = ishara.HUNA
}


def _check() -> None:
    for z in STEMS:
        for op in (mudaf, jarr, qat):
            if not licensed(op(z.stem)):
                raise ValueError(f"UNLICENSED:{z.name}")
    assert hukm(qat(STEMS[13].stem)).startswith("مقطوع")
    assert hukm(CONSTANTS["حَيْثُ"]).startswith("مقطوع")


_check()
