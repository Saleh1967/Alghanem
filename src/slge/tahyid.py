"""التحييد (ADR ٥٩): الصورةُ القانونيّة للنصّ المستخرَج من حاويته — مرآةُ `formal/Slge/Tahyid.lean`.

السطرُ يحمل علامةَ الاستثناء البنيويّ من الباب (جدولٌ أو صندوقُ نصّ)؛ والصورةُ القانونيّة: يُحذف
المستثنى، ثمّ الجدولة، ثمّ تُقصّ المسافاتُ من الطرفين، ثمّ يُحذف الفارغ. لا تمسّ حرفًا غيرَ المسافة
والجدولة (`marks_preserved`).
"""

from __future__ import annotations

from collections.abc import Iterable

__all__ = ["canon", "clean", "del_tab", "order_matters", "strip_sp"]


def del_tab(line: str) -> str:
    return line.replace("\t", "")


def strip_sp(line: str) -> str:
    return line.strip(" ")


def clean(line: str) -> str:
    return strip_sp(del_tab(line))


def canon(rows: Iterable[tuple[bool, str]]) -> list[str]:
    """(مستثنًى بالبنية، السطر) ← أسطرُ الصورة القانونيّة."""

    return [c for excluded, line in rows if not excluded and (c := clean(line))]


def order_matters(line: str) -> bool:
    """زوجُ التقاء: سطرٌ يختلف ناتجُه بترتيب القاعدتين."""

    return strip_sp(del_tab(line)) != del_tab(strip_sp(line))
