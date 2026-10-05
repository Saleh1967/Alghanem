"""طبقة يونيكود: لا خانةَ إلّا بنقطةٍ قانونيّةٍ واحدة (NFC)، ولا حرفَ خارج الجدول المعلن."""

from __future__ import annotations

import unicodedata
from typing import Final

__all__ = ["CANON", "MARKS", "OUTSIDE", "SEATS", "SUBSTITUTIONS", "audit_text", "conflicts",
           "normalize"]

CANON: Final[dict[str, str]] = {c: f"U+{ord(c):04X}" for c in "ءابتثجحخدذرزسشصضطظعغفقكلمنهوي"}
"""الحواملُ الـ29 بنقاطها القانونيّة."""

MARKS: Final[dict[str, str]] = {c: f"U+{ord(c):04X}" for c in "ًٌٍَُِّْ"}
"""الحركاتُ والتنوينُ والشدّةُ والسكون."""

SEATS: Final[frozenset[str]] = frozenset("أإآؤئةىٱ")
"""مقاعدُ وصورٌ إملائيّةٌ مشروعة؛ يقرؤها `orthography.to_atoms` ولا تُبدَّل."""

SUBSTITUTIONS: Final[dict[str, str]] = {"ک": "ك", "ی": "ي", "ﻻ": "لا", "ـ": "", "ٰ": ""}
"""المخالفةُ ← القانونيّ: كافٌ وياءٌ فارسيّتان، ولامُ ألفٍ مركّبة، والتطويل، والألفُ
الخنجريّة. (ملاحظة معلنة: حذفُ الخنجريّة يُسقط مدًّا في الرسم العثمانيّ.)"""

OUTSIDE: Final[frozenset[str]] = frozenset("ﷺﷻ")
"""محارفُ مركّبةٌ محظورة."""


def normalize(text: str) -> str:
    """التطبيعُ المعلن ثمّ NFC. متساوي الأثر: ‎normalize(normalize(t)) = normalize(t)‎."""

    for bad, good in SUBSTITUTIONS.items():
        text = text.replace(bad, good)
    return unicodedata.normalize("NFC", text)


def conflicts(text: str) -> list[tuple[str, int]]:
    """ما خالف القانونَ في النصّ: (وصفُه، عددُ مرّاته)، مرتّبًا."""

    found: list[tuple[str, int]] = []
    for ch in sorted(set(text)):
        if ch in SUBSTITUTIONS:
            found.append((f"U+{ord(ch):04X} → {SUBSTITUTIONS[ch]!r}", text.count(ch)))
        elif ch in OUTSIDE:
            found.append((f"U+{ord(ch):04X} محظور", text.count(ch)))
    return found


def audit_text(text: str) -> list[str]:
    """محارفُ من الفضاء العربيّ ‎U+0600…U+06FF‎ خارجَ الجدول المعلن."""

    allowed = set(CANON) | set(MARKS) | SEATS | set(SUBSTITUTIONS) | set("،؛؟٠١٢٣٤٥٦٧٨٩")
    return sorted(
        {f"U+{ord(c):04X} {c!r}" for c in text if "\u0600" <= c <= "\u06ff" and c not in allowed}
    )
