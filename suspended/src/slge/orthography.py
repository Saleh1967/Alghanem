"""طبقة الإملاء وقوانينها الثلاثة: الذرّات ⇄ الرسم، والابتداء، والوصل، والوقف.

العقدُ المفحوص (`tests/test_orthography.py`): ‎to_atoms(to_rasm(w)) = w‎ لكلّ
مرخَّصةٍ بطول ‎≤ 2‎ (‎10,180‎ كلمة) استقصاءً، ولطول ‎3‎ كلِّه في الفحص البطيء
(‎1,097,505‎ كلمة). والرسمُ قد يتعدّد للذرّات الواحدة (التنوين و«نْ» الخاتمة)،
فالعقدُ من الذرّات إلى الذرّات لا من الرسم إلى الرسم.
"""

from __future__ import annotations

from typing import Final

from .cells import ALPHABET, SUKUN, Cell, Word
from .encoding import normalize

__all__ = ["SUN", "begin", "join", "pause", "to_atoms", "to_rasm"]

SUN: Final[frozenset[str]] = frozenset("تثدذرزسشصضطظلن")
"""الحروفُ الشمسيّة."""

_MARK: Final[dict[str, str]] = {"فتح": "َ", "كسر": "ِ", "ضم": "ُ", SUKUN: "ْ"}
_TANWIN: Final[dict[str, str]] = {"فتح": "ً", "ضم": "ٌ", "كسر": "ٍ"}
_HAMZA: Final[dict[str, str]] = {"فتح": "أَ", "كسر": "إِ", "ضم": "أُ", SUKUN: "ءْ"}
_VOWEL: Final[dict[str, str]] = {"َ": "فتح", "ِ": "كسر", "ُ": "ضم", "ْ": SUKUN}
_TW: Final[dict[str, str]] = {"ً": "فتح", "ٌ": "ضم", "ٍ": "كسر"}
_SEAT: Final[dict[str, str]] = {"أ": "ء", "إ": "ء", "ؤ": "ء", "ئ": "ء", "ة": "ت", "ى": "ا",
                                "ٱ": "ا"}


def to_rasm(cells: Word) -> str:
    """الذرّات ← الرسم المشكول."""

    out: list[str] = []
    i, n = 0, len(cells)
    while i < n:
        c, s = cells[i]
        prev = cells[i - 1][1] if i > 0 else None
        if (c, s) == ("ن", SUKUN) and i == n - 1 and prev is not None and prev != SUKUN:
            out[-1] = out[-1][:-1] + _TANWIN[prev]  # تنوينُ الخاتمة يحلّ محلّ حركة سابقه
        elif c == "ء" and s == "فتح" and i + 1 < n and cells[i + 1] == ("ا", SUKUN):
            out.append("آ")
            i += 1
        elif c == "ء":
            out.append(_HAMZA[s])
        elif (c, s, prev) in (("و", SUKUN, "ضم"), ("ي", SUKUN, "كسر")):
            out.append(c)  # حرفُ المدّ بلا علامة
        else:
            out.append(c + _MARK[s])
        i += 1
    return "".join(out)


def to_atoms(word: str) -> list[Cell]:
    """الرسم ← الذرّات (القواعد الثمان المعلنة)."""

    word = normalize(word)
    cells: list[Cell] = []
    i, n = 0, len(word)
    while i < n:
        ch = word[i]
        if ch in _VOWEL or ch in _TW or ch == "ّ":
            i += 1
            continue
        if ch == "آ":
            cells += [("ء", "فتح"), ("ا", SUKUN)]
            i += 1
            continue
        base = _SEAT.get(ch, ch)
        if base not in ALPHABET:
            i += 1
            continue
        j, shadda, vowel, tw = i + 1, False, None, None
        while j < n and word[j] in "ًٌٍَُِّْ":
            if word[j] == "ّ":
                shadda = True
            elif word[j] in _TW:
                tw = _TW[word[j]]
            elif vowel is None:
                vowel = _VOWEL[word[j]]
            j += 1
        if shadda:
            cells.append((base, SUKUN))
        if base == "و" and vowel is None and j < n and word[j] == "ا" and j + 1 >= n:
            cells.append(("و", "فتح"))  # واو الجماعة وألفُها الفارقة
            i = j + 1
            continue
        cells.append((base, vowel or tw or SUKUN))
        if tw:
            if tw == "فتح" and j < n and word[j] == "ا":
                j += 1
            cells.append(("ن", SUKUN))
        i = j
    return cells


def begin(cells: Word) -> list[Cell]:
    """قانون الابتداء: همزةُ الوصل تُنطق همزةً متحرّكة، والمطلعُ متحرّك.

    الأصلُ (`slge_laws.begin`) جعلها ‎(ا، فتح)‎ فنقض ρ (الألفُ لا تتحرّك)؛ وهنا
    ‎(ء، فتح)‎: الحركةُ التي اختارها الأصلُ نفسُها على الحامل الذي يحملها. وكسرُها
    وضمُّها في غير «ال» سؤالٌ مفتوحٌ في `status.LEDGER` (Q12-wasl).
    """

    c = list(cells)
    if c and c[0] == ("ا", SUKUN):
        c[0] = ("ء", "فتح")
    if len(c) > 2 and c[0][1] != SUKUN and c[1] == ("ل", SUKUN) and c[2][0] in SUN \
            and c[2][1] == SUKUN:
        c = [c[0], *c[2:]]
    return c


def join(prev: Word, nxt: Word) -> tuple[list[Cell], bool]:
    """قانون الوصل: همزةُ الوصل تسقط، والشمسيُّ يُدغم، والوصلةُ ليست ساكنين."""

    c = list(nxt)
    if len(c) >= 2 and c[0] == ("ا", SUKUN) and c[1][1] == SUKUN:
        c = c[1:]
    if len(c) >= 2 and c[0] == ("ل", SUKUN) and c[1][0] in SUN and c[1][1] == SUKUN:
        c = c[1:]
    out: list[Cell] = []
    i = 0
    while i < len(c):
        if i + 2 < len(c) and c[i][1] == SUKUN and c[i + 1] == (c[i][0], SUKUN) \
                and c[i + 2][0] == c[i][0] and c[i + 2][1] != SUKUN:
            i += 1
        out.append(c[i])
        i += 1
    ok = not (prev and out and prev[-1][1] == SUKUN and out[0][1] == SUKUN)
    return out, ok


def pause(cells: Word) -> list[Cell]:
    """قانون الوقف: الختامُ سكون، ونونُ التنوين تُحذف، ونونُ الإعراب بعد واوٍ أو ألفٍ تُحذف معها."""

    w = list(cells)
    if not w:
        return w
    if w[-1] == ("ن", SUKUN) and len(w) > 1 and w[-2][1] != SUKUN:
        return [*w[:-2], (w[-2][0], SUKUN)]
    if w[-1][0] == "ن" and len(w) >= 2 and w[-2][0] in "وا":
        return w[:-2]
    return w if w[-1][1] == SUKUN else [*w[:-1], (w[-1][0], SUKUN)]
