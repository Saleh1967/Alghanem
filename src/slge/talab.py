"""الطلب: صورُ الأمر الأربع من الخانة، والأمرُ ليس نهيًا على الخانة، والإلزامُ ليس في الخانة — `Talab`.

صورُ الأمر: الصيغةُ (قالبُ الأمر)، ولامُ الأمر على المضارع المجزوم (لِيَكْتُبْ؛ وبعد الواو والفاء ساكنةً:
وَلْيَكْتُبْ)، والمصدرُ النائب (ضَرْبًا في الصدر)، واسمُ الفعل من جدوله (`ISM_FIL`) — يقرؤها `talab`. الصيغةُ
للمخاطب واللامُ لكلّ شخص. لَا قبل صيغة الأمر لا تقلبها نهيًا (`uslub`)، والنهيُ لا يُقرأ إلّا بلَا قبل
مضارع. الإلزامُ (وجوبٌ/ندب) ليس في الخانة: معلَن. القياسُ على MASAQ في `tools/gen_talab_index.py`.
"""

from __future__ import annotations

from typing import Final

from slge.cells import STATES, Cell, licensed
from slge.filiyya import is_masdar
from slge.jazm import amr as lam_of
from slge.jazm import sukun
from slge.jiha import sigha
from slge.nawasikh import nasb, tanwin
from slge.nida import has_tanwin
from slge.rawabit import cells_of
from slge.tawabi import case_class
from slge.uslub import present_any_mood

__all__ = ["ISM_FIL", "lam_amr", "lam_amr_after_waw", "masdar_amr", "talab"]

_A, _I, _U, SUKUN = STATES
Word = tuple[Cell, ...]

ISM_FIL: Final[tuple[tuple[str, Word], ...]] = (
    *((w, cells_of(w)) for w in ("صَهْ", "مَهْ", "هَلُمَّ", "حَيَّ")),
    ("آمِينَ", cells_of("ءَامِينَ")),
    *((w, cells_of(w)) for w in ("إِيهِ", "هَيَّا", "هَاتِ")),
)
WAW: Final[Word] = cells_of("وَ")
FA: Final[Word] = cells_of("فَ")
_LAM_I: Final[Word] = (("ل", _I),)
_LAM_S: Final[Word] = (("ل", SUKUN),)


def lam_amr(v: Word) -> Word:
    """لامُ الأمر على المضارع المجزوم."""

    return lam_of(sukun(v))


def lam_amr_after_waw(v: Word) -> Word:
    """بعد الواو والفاء تسكن اللام: وَلْيَكْتُبْ."""

    return (*_LAM_S, *sukun(v))


def masdar_amr(w: Word) -> Word:
    return tanwin(nasb(w))


def talab(prev: Word, w: Word) -> str | None:
    """صورةُ الطلب من الخانة: صيغةٌ، لام، اسمُ فعل، أو مصدرٌ منصوبٌ منوَّنٌ في الصدر؛ وإلّا لا طلب."""

    if sigha(w) == "أمر":
        return "صيغة"
    lam = w[:1] == _LAM_I or (w[:1] == _LAM_S and prev in (WAW, FA))
    if lam and present_any_mood(w[1:]) and w[-1][1] == SUKUN:
        return "لام"
    if any(cs == w for _, cs in ISM_FIL):
        return "اسم فعل"
    if prev == () and is_masdar(w) and case_class(w) == "نصب" and has_tanwin(w):
        return "مصدر"
    return None


def _check() -> None:
    from slge.maqam import shakhs
    from slge.uslub import LA, uslub

    assert len(ISM_FIL) == 8 and all(licensed(cs) for _, cs in ISM_FIL)
    yaktubu, kataba, uktub, darb = (cells_of(w) for w in ("يَكْتُبُ", "كَتَبَ", "اُكْتُبْ", "ضَرْبُ"))
    assert talab((), uktub) == "صيغة" and talab((), lam_amr(yaktubu)) == "لام"
    assert lam_amr(yaktubu) == cells_of("لِيَكْتُبْ")
    assert lam_amr_after_waw(yaktubu)[1:] == sukun(yaktubu)
    assert talab(WAW, lam_amr_after_waw(yaktubu)) == "لام"
    assert talab(FA, lam_amr_after_waw(yaktubu)) == "لام"
    assert talab((), lam_amr_after_waw(yaktubu)) is None
    assert talab((), masdar_amr(darb)) == "مصدر" and talab(kataba, masdar_amr(darb)) is None
    assert talab((), cells_of("صَهْ")) == "اسم فعل" and talab((), yaktubu) is None
    assert talab((), kataba) is None
    assert shakhs(uktub) == "مخاطب" and shakhs(yaktubu) == "غائب"
    assert shakhs(cells_of("أَكْتُبُ")) == "متكلم"
    assert uslub(LA, uktub) == "أمر" and uslub(LA, sukun(yaktubu)) == "نهي"
    assert lam_amr(yaktubu)[-1][1] == SUKUN and licensed(lam_amr(yaktubu))


_check()
