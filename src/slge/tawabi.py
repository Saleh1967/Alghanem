"""التوابع: الحالةُ لا العلامة — مرآةُ `formal/Slge/Tawabi.lean`.

قانونُ الفرز: التابعُ يتبع المتبوعَ في **الحالة** لا في **العلامة**. فالقارئُ `case_class` يردّ العلاماتِ
كلَّها إلى الحالة: الضمّةُ والواوُ (ُونَ، ُو) والألفُ (َانِ) رفعٌ؛ الفتحةُ والياءُ (ِينَ، َيْنِ) نصبٌ أو جرّ؛
الكسرةُ جرّ (وبعد ألفٍ وتاءٍ نصبٌ أو جرّ: جمعُ المؤنّث السالم)؛ والألفُ بعد فتحٍ والياءُ بعد كسرٍ
لا تقرؤهما الخانة (الخمسةُ أم مقصورٌ ومنقوص: المعجم).
و`follows` توافقٌ مع التباسِ الياء (`compatible`). عطفُ النسق تسعةُ حروف كلُّها في
`rawabit`؛ والتوكيدُ المعنويّ ستّةُ ألفاظٍ تُضاف إلى ضميرٍ (وعَامَّة خارج الثنائيّ كحَاجَّ). النعتُ والبدلُ
وعطفُ البيان لا تفرّقها الخانة: كلُّها تابعٌ يوافق في الحالة؛ والمطابقةُ في التعريف والجنس والعدد قوانينُ
تيارٍ تُقاس (`tools/gen_tawabi_index.py`).
"""

from __future__ import annotations

from typing import Final

from slge.cells import STATES, Cell, licensed
from slge.marifa import idafa

__all__ = ["NASAQ", "TAWKID", "case_class", "compatible", "follows", "tawkid"]

_A, _I, _U, SUKUN = STATES
NASAQ: Final[tuple[str, ...]] = ("وَ", "فَ", "ثُمَّ", "حَتَّى", "أَوْ", "أَمْ", "لَا", "بَلْ", "لَكِنْ")


def _s(*cells: Cell) -> tuple[Cell, ...]:
    return cells


TAWKID: Final[dict[str, tuple[Cell, ...]]] = {
    "نَفْس": _s(("ن", _A), ("ف", SUKUN), ("س", _U)),
    "عَيْن": _s(("ع", _A), ("ي", SUKUN), ("ن", _U)),
    "كُلّ": _s(("ك", _U), ("ل", SUKUN), ("ل", _U)),
    "جَمِيع": _s(("ج", _A), ("م", _I), ("ي", SUKUN), ("ع", _U)),
    "كِلَا": _s(("ك", _I), ("ل", _A), ("ا", SUKUN)),
    "كِلْتَا": _s(("ك", _I), ("ل", SUKUN), ("ت", _A), ("ا", SUKUN)),
}


def case_class(word: tuple[Cell, ...]) -> str:
    """الحالةُ من العلامة أيًّا كانت: رفع | نصب | جرّ | نصب/جرّ | لا تقرؤه الخانة."""

    if not word:
        return "لا تقرؤه الخانة"
    n = word[-1]
    g = word[-2] if len(word) >= 2 else None
    p = word[-3] if len(word) >= 3 else None
    if g and p and n[0] == "ن" and g[1] == SUKUN:
        if n[1] == _A and g[0] == "و" and p[1] == _U:
            return "رفع"
        if n[1] == _A and g[0] == "ي" and p[1] == _I:
            return "نصب/جرّ"
        if n[1] == _I and g[0] == "ا" and p[1] == _A:
            return "رفع"
        if n[1] == _I and g[0] == "ي" and p[1] == _A:
            return "نصب/جرّ"
    if p and n == ("ن", SUKUN) and g == ("ت", _I) and p == ("ا", SUKUN):
        return "نصب/جرّ"  # جمعُ المؤنّث السالم منوَّنًا
    if g and n == ("ت", _I) and g == ("ا", SUKUN):
        return "نصب/جرّ"  # جمعُ المؤنّث السالم
    if g and n == ("ن", SUKUN) and g[1] != SUKUN:
        return {_U: "رفع", _A: "نصب", _I: "جرّ"}.get(g[1], "لا تقرؤه الخانة")
    if g and n[1] == SUKUN:
        if n[0] == "و" and g[1] == _U:
            return "رفع"
        # الألفُ بعد فتحٍ والياءُ بعد كسر: إمّا من الخمسة وإمّا مقصورٌ ومنقوصٌ مقدَّر — المعجمُ يفصل
        return "لا تقرؤه الخانة"
    return {_U: "رفع", _A: "نصب", _I: "جرّ"}.get(n[1], "لا تقرؤه الخانة")


def compatible(a: str, b: str) -> bool:
    if a.startswith("لا تقرؤه") or b.startswith("لا تقرؤه"):
        return False
    return a == b or {a, b} <= {"نصب/جرّ", "نصب"} or {a, b} <= {"نصب/جرّ", "جرّ"}


def follows(tabi: tuple[Cell, ...], matbu: tuple[Cell, ...]) -> bool:
    return compatible(case_class(tabi), case_class(matbu))


def tawkid(word: str, suffix: tuple[Cell, ...]) -> tuple[Cell, ...]:
    """التوكيدُ المعنويّ: اللفظُ مضافًا إلى الضمير."""

    return idafa(TAWKID[word], suffix)


def _check() -> None:
    assert all(licensed(w) for w in TAWKID.values())
    assert case_class(_s(("ء", _A), ("خ", _U), ("و", SUKUN))) == "رفع"
    muslimuna = _s(("م", _U), ("س", SUKUN), ("ل", _I), ("م", _U), ("و", SUKUN), ("ن", _A))
    assert case_class(muslimuna) == "رفع"
    assert follows(_s(("ر", _A), ("ج", _U), ("ل", _U)), _s(("ء", _A), ("خ", _U), ("و", SUKUN)))


_check()
