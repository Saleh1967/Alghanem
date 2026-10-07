"""معاني الحروف: تعدّدُ معاني الحرف الواحد مرتَّبًا بالقرينة لا مختارًا — مرآةُ `Slge.Maani`.

الجدولُ `maani_table.TABLE` منقولٌ من مبحث «الحرف» في الشخصيّة ج3 بترتيب المصدر
(`tools/deposit_maani.py`).
القرينتان معلَنتان: ظرفُ مكانٍ أو زمانٍ بعد الحرف يقدّم معاني الغاية والظرفيّة (`is_zarf` من جدولَي
`zuruf`/`zaman`)، ونفيٌ قبله يقدّم «زائدة» (يحسبه القارئُ من `adawat` خارج هذه الوحدة)؛ وبلا قرينةٍ
ترتيبُ المصدر. الترتيبُ لا يُسقط معنًى (`mem_rank`، `length_rank`).
"""

from __future__ import annotations

from typing import Final

from slge.cells import Cell
from slge.huruf import TABLE as HURUF
from slge.maani_table import SENSES, TABLE
from slge.zaman import STEMS as ZAMAN_STEMS
from slge.zaman import forms_of
from slge.zuruf import STEMS as ZURUF_STEMS
from slge.zuruf import jarr, mudaf, qat

__all__ = ["GHAYA", "MULTI", "SENSES", "is_zarf", "jarr_uncovered", "rank", "senses_of"]

Word = tuple[Cell, ...]

GHAYA: Final[frozenset[str]] = frozenset(
    {"ابتداء الغاية", "انتهاء الغاية", "الظرفية", "ابتداء الغاية في الزمان"})
"""معاني الغاية والظرفيّة (`Maani.ghaya`)."""

ZAIDA: Final[str] = "زائدة"


def senses_of(h: int) -> tuple[str, ...]:
    """معاني الحرف `h` (فهرسُه في `huruf.TABLE`) بترتيب المصدر؛ فارغةٌ لما لا معنى له فيه
    (`sensesOf`)."""

    return tuple(SENSES[i] for i in TABLE.get(h, ()))


MULTI: Final[tuple[int, ...]] = tuple(h for h, ss in sorted(TABLE.items()) if len(ss) >= 2)
"""الحروفُ ذاتُ المعنيين فأكثر (`multi`)."""


def jarr_uncovered() -> tuple[int, ...]:
    """حروفُ الجرّ بلا معنًى في المصدر (`jarr_uncovered`)."""

    return tuple(i for i, h in enumerate(HURUF) if h.amal == "جرّ" and not senses_of(i))


_ZARF_FORMS: Final[frozenset[Word]] = frozenset(
    {*(f for z in ZURUF_STEMS for f in (mudaf(z.stem), jarr(z.stem), qat(z.stem))),
     *(f for s in ZAMAN_STEMS.values() for f in forms_of(s))})


def is_zarf(w: Word) -> bool:
    """ظرفُ مكانٍ أو زمانٍ من الجدولَين بصوره (`isZarf`)."""

    return w in _ZARF_FORMS


def _split(pred: frozenset[str], ss: tuple[str, ...]) -> tuple[str, ...]:
    return (*(s for s in ss if s in pred), *(s for s in ss if s not in pred))


def rank(senses: tuple[str, ...], *, nafy_before: bool = False,
         zarf_after: bool = False) -> tuple[str, ...]:
    """ظرفٌ بعده يقدّم الغاية؛ وإلّا نفيٌ قبله يقدّم «زائدة»؛ وإلّا ترتيبُ المصدر (`rank`)."""

    if zarf_after:
        return _split(GHAYA, senses)
    if nafy_before:
        return _split(frozenset({ZAIDA}), senses)
    return senses


def _check() -> None:
    assert senses_of(5) == ("ابتداء الغاية", "التبعيض", "بيان الجنس", "زائدة")
    assert rank(senses_of(5), nafy_before=True) == (
        "زائدة", "ابتداء الغاية", "التبعيض", "بيان الجنس")
    assert rank(senses_of(9), zarf_after=True) == ("الظرفية", "بمعنى على", "التجوّز")
    assert rank(senses_of(5), nafy_before=True, zarf_after=True) == senses_of(5)
    assert senses_of(13) == () and jarr_uncovered() == (13, 14, 15)
    assert MULTI == (0, 1, 5, 6, 9, 10, 52, 53, 61)


_check()
