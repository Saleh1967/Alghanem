"""دستورُ الترتيب: عمودُ الطبقات، ومنعُ القفز، والتمييزُ بالبصمة لا بالظلّ.

العمودُ هو عمودُ `slge_order.py` (اثنتا عشرة طبقة من البتّات إلى الإعراب)، وأُدخلت فيه
الدلالةُ حيث أعلنها `dal-madlul-constitution` («بعد الإملاء وقبل المبنيّات»)، والصفاتُ
حيث أعلنها `slge_phon` («قبل الـ116»)، وفوقه المعرفةُ ثمّ الترجيحُ (رتبةُ الجواب) والتعلّمُ ثمّ الجواب.

والقاعدةُ نفسُها تحكم الشيفرة: `MODULE_LAYER` يُسند كلَّ وحدةٍ إلى طبقة، ويفحص
`tests/test_order.py` أنّ الوحدةَ لا تستورد إلّا وحداتِ طبقاتٍ من شروطها (منعُ القفز في
البناء، لا في الوصف وحده).
"""

from __future__ import annotations

import hashlib
from collections.abc import Iterable
from typing import Final

__all__ = ["LAYERS", "META", "MODULE_LAYER", "ancestors", "build", "no_leap", "stamp"]

LAYERS: Final[dict[str, tuple[str, ...]]] = {
    "الصفات": (),
    "البتات": (),
    "المدخل": ("البتات",),
    "التسلسل": ("البتات",),
    "الأقانيم": ("البتات",),
    "اليونيكود": ("البتات",),
    "الترميز العثماني": ("اليونيكود",),
    "الإملاء": ("الترميز العثماني",),
    "الدلالة": ("الإملاء",),
    "المبنيات": ("الإملاء", "الدلالة"),
    "الفعل": ("المبنيات",),
    "الوزن": ("الفعل",),
    "المعتل": ("الوزن",),
    "الجذع": ("المعتل",),
    "المشتق": ("الجذع",),
    "الموضع": ("المشتق",),
    "الإعراب": ("الموضع",),
    "النظم": ("الإعراب", "الدلالة"),
    "المعرفة": ("الدلالة", "الإعراب"),
    "الترجيح": ("المعرفة",),
    "التعلم": ("المعرفة",),
    "الجواب": ("المعرفة", "الترجيح"),
}
"""الطبقة ← شروطُها المباشرة."""

MODULE_LAYER: Final[dict[str, str]] = {
    "phonology": "الصفات",
    "cells": "البتات",
    "entry": "المدخل",
    "stream": "التسلسل",
    "categories": "الأقانيم",
    "semantics": "الدلالة",
    "nazm": "النظم",
    "grant": "النظم",
    "wazn": "الوزن",
    "shabaka": "المشتق",
    "khamsa": "الإعراب",
    "knowledge": "المعرفة",
    "rank": "الترجيح",
    "learning": "التعلم",
    "answer": "الجواب",
}
"""الوحدة ← طبقتُها. والصرفُ كلُّه (الفعل … الإعراب) في وحدةٍ واحدة طبقتُها أعلاها."""

SUSPENDED_MODULES: Final[dict[str, str]] = {
    "encoding": "اليونيكود",
    "orthography": "الإملاء",
    "lexicon": "المبنيات",
    "morphology": "الإعراب",
}
"""وحداتٌ معلَّقةٌ في `suspended/src/slge/` بطبقاتها: كانت تقرأ النصّ وتكتبه خارج البوّابة.
لا يدخل نصٌّ إلى العمود إلّا شهادةً من بوّابة الغانم (`gate.enter`)، فلا تعود إلّا من هناك."""

META: Final[frozenset[str]] = frozenset({"order", "status", "guard"})
"""وحداتٌ خارج العمود: تصفه ولا تبني فيه؛ يستوردها أيُّ أحد، ولا تستورد هي شيئًا منه."""


def ancestors(layer: str) -> frozenset[str]:
    """كلُّ ما تشترطه الطبقةُ مباشرةً أو بواسطة."""

    seen: set[str] = set()
    todo = list(LAYERS[layer])
    while todo:
        x = todo.pop()
        if x not in seen:
            seen.add(x)
            todo.extend(LAYERS[x])
    return frozenset(seen)


def stamp(cells: Iterable[tuple[str, str]]) -> str:
    """بصمةُ البناء: الخليةُ كاملةً لا ظلّها."""

    return hashlib.sha256(str(tuple(cells)).encode("utf-8")).hexdigest()[:12]


def no_leap(layer: str, verified: Iterable[str]) -> bool:
    """بوّابةُ منع القفز: لا تُبنى طبقةٌ قبل أن تخضرّ بصماتُ شروطها كلِّها."""

    return set(LAYERS[layer]) <= set(verified)


def build(layer: str, verified: Iterable[str]) -> str:
    """ابنِ الطبقةَ إن جاز، وإلّا فارفع."""

    done = set(verified)
    if not no_leap(layer, done):
        missing = sorted(set(LAYERS[layer]) - done)
        raise PermissionError(f"قفزٌ ممنوع: {layer} قبل {'، '.join(missing)}")
    return stamp([(layer, "بُني")])
