"""الزوائد: حروفُ سيبويه العشرة، ونونُ التوكيد، وتاءُ التأنيث الساكنة، وحروفُ المضارعة — مرآةُ
`Slge.Zawaid`.

المصدرُ «باب علم حروف الزوائد» و«باب النون الثقيلة والخفيفة» من الكتاب المختوم (`zawaid_table` مولَّدٌ
منه). الزائدةُ عمليّةٌ جبريّةٌ على الخانات مغلقةٌ على الترخيص: الإلصاقُ يحفظه (`tawkid_licensed`،
`anith_licensed`) والقطعُ عكسُه بعينه عبر لواحق `jidh` (`in_enclitics`). الخفيفةُ خانتُها خانةُ التنوين
(`khafifa_is_tanwin`) فتمييزُهما بالجهة لا بالخانة. لا بطاقاتٍ نثريّة: خاناتٌ وعمليّات.
"""

from __future__ import annotations

from typing import Final

from slge.cells import ALPHABET, STATES, Cell, licensed
from slge.zawaid_table import TABLE, WITNESSES
from slge.zuruf import set_last

__all__ = ["CELLS", "KHAFIFA", "LETTERS", "MUDARAA", "TABLE", "TA_TANITH", "THAQILA", "WITNESSES",
           "anith", "has_tanwin_shape", "tawkid"]

Word = tuple[Cell, ...]

LETTERS: Final[tuple[str, ...]] = tuple(row[1] for row in TABLE)
"""حواملُ الزوائد العشرة بترتيب الباب: ء ا ه ي ن ت س م و ل."""

CELLS: Final[tuple[Cell, ...]] = tuple((k, s) for k in LETTERS for s in STATES)
"""خاناتُ الزوائد: كلُّ حرفٍ زائد في حالاته الأربع — أربعون من الـ116."""

THAQILA: Final[Word] = (("ن", "سكون"), ("ن", "فتح"))
KHAFIFA: Final[Word] = (("ن", "سكون"),)
TA_TANITH: Final[Word] = (("ت", "سكون"),)
MUDARAA: Final[tuple[str, ...]] = ("ء", "ن", "ي", "ت")
"""حروفُ المضارعة الأربعة — من العشرة، «أوّلًا في الفعل» عند سيبويه."""


def tawkid(w: Word, heavy: bool) -> Word:
    """إلصاقُ نون التوكيد بالفعل: فتحُ آخره ثمّ النون الثقيلة أو الخفيفة (`tawkid`)."""

    return set_last(w, "فتح") + (THAQILA if heavy else KHAFIFA)


def anith(w: Word) -> Word:
    """إلصاقُ تاء التأنيث الساكنة بالماضي: فتحُ آخره ثمّ التاء (`anith`)."""

    return set_last(w, "فتح") + TA_TANITH


def has_tanwin_shape(w: Word) -> bool:
    """خانةُ التنوين: نونٌ ساكنةٌ بعد متحرّك في الآخر (`Nida.hasTanwin`) — وهي خانةُ الخفيفة بعينها."""

    return len(w) >= 2 and w[-1] == ("ن", "سكون") and w[-2][1] != "سكون"


def _check() -> None:
    assert LETTERS == ("ء", "ا", "ه", "ي", "ن", "ت", "س", "م", "و", "ل") and len(set(LETTERS)) == 10
    assert all(k in ALPHABET for k in LETTERS) and len(CELLS) == 40 and len(set(CELLS)) == 40
    assert set(MUDARAA) <= set(LETTERS)
    taqul = (("ت", "فتح"), ("ق", "ضم"), ("و", "سكون"), ("ل", "ضم"))
    assert tawkid(taqul, True) == (("ت", "فتح"), ("ق", "ضم"), ("و", "سكون"), ("ل", "فتح"), *THAQILA)
    assert licensed(tawkid(taqul, True)) and licensed(tawkid(taqul, False))
    assert has_tanwin_shape(tawkid(taqul, False))
    qala = (("ق", "فتح"), ("ا", "سكون"), ("ل", "فتح"))
    assert anith(qala) == (*qala, ("ت", "سكون")) and licensed(anith(qala))
    assert sum(len(ws) for _, ws in WITNESSES) == 48


_check()
