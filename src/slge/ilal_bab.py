"""أبوابُ الإعلال عند سيبويه — مرآةُ `Slge.IlalBab` (الحدُّ الأدنى المكتمل).

لكلّ قاعدةٍ من قواعد `Slge.Ilal` الثلاثَ عشرةَ بابُها في الكتاب المختوم بسطره وشاهدُه رسمًا من نصّ
الباب بعينه (`every_rule_once`)؛ وثمانٍ منها لها صورةٌ من مودَع المصحف تقرؤها القاعدةُ نفسُها —
`undo` غيرُ فارغ في موضعها (`witnesses_read`)؛ والخمسُ الباقيةُ شاهدُها رسمٌ بلا خانات لم يُشكَّل من
الذاكرة (`unwitnessed`). وأبوابٌ عند سيبويه لا قاعدةَ لها عندنا ديونٌ مسمّاةٌ بأسطرها (`debts_named`).
الجدولُ `ilal_bab_table` مولَّدٌ بـ`tools/deposit_ilal_bab.py`؛ هذه الطبقةُ تقرؤه ولا تزيد عليه.
"""

from __future__ import annotations

from typing import Final

from slge.ilal import RULES, undo
from slge.ilal_bab_table import DEBTS, TABLE, Row

__all__ = ["DEBTS", "TABLE", "Row", "anchor_of", "reads", "unwitnessed", "witnessed"]


def anchor_of(rule: str) -> Row:
    """صفُّ القاعدة: بابُها وسطرُه وشاهدُه وصورةُ المصحف إن وُجدت."""

    return next(r for r in TABLE if r[0] == rule)


def reads(row: Row) -> bool:
    """هل تقرأ القاعدةُ صورةَ المصحف المودَعة في موضعها؟ (`IlalBab.reads`)"""

    rule, _, _, _, cells, at, _ = row
    return cells is not None and at is not None and bool(undo(rule, cells, at))


def witnessed() -> tuple[Row, ...]:
    """الصفوفُ التي لها صورةٌ من المصحف."""

    return tuple(r for r in TABLE if r[4] is not None)


def unwitnessed() -> tuple[str, ...]:
    """القواعدُ التي شاهدُها رسمُ الباب بلا خانات — غائبةٌ باسمها."""

    return tuple(r[0] for r in TABLE if r[4] is None)


_WITNESSED: Final[tuple[str, ...]] = ("QALB_AYN", "HADHF_AYN_U", "HADHF_AYN_I", "NAQL", "QALB_LAM",
                                      "HADHF_WAW", "HAMZA_MADD", "WAW_YA")
_UNWITNESSED: Final[tuple[str, ...]] = ("HADHF_LAM", "TA_TTA", "TA_DAL", "FA_TA", "YA_WAW")


def _check() -> None:
    assert tuple(r[0] for r in TABLE) == RULES, "لكلّ قاعدةٍ صفٌّ واحدٌ بترتيب Rule.all"
    assert all(r[3] and r[2] > 0 for r in TABLE)
    assert tuple(r[0] for r in witnessed()) == _WITNESSED and all(reads(r) for r in witnessed())
    assert unwitnessed() == _UNWITNESSED
    assert all(r[6] == ("chapter" if r[4] is not None else "none") for r in TABLE)
    lines = {r[2] for r in TABLE}
    assert len(DEBTS) == 7 == len({n for _, n in DEBTS}) and not lines & {n for _, n in DEBTS}


_check()
