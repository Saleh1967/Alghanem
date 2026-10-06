"""المدود: المدُّ خانةٌ ساكنةٌ بعد حركتها، وأحكامُه من الخانة التالية والحدّ — مرآةُ `Madd`.

`kinds` تُسقط الخانات على الأصناف الثلاثة `cv/v/c` (مرآةُ `gate.licence.kind_of` على الخانات)؛ ومنها
الترخيصُ الثلاثيّ وصلًا ووقفًا (`continue_licensed`/`pause_licensed`) والثنائيُّ `binary_ok`
(= `licensed`: `licensed_eq_binOK`). المدُّ اللازم (مدٌّ ثمّ ساكن) هو فاصلُ الثلاثيّ عن الثنائيّ
(`lazim_iff_not_binary`).
القارئُ `madd(w, next, pause)` يقرأ أحكامَ المدود من الخانة التالية والحدّ، واللينَ والصلةَ، ويحجب
الواوَ الساقطةَ بالجدول. القياسُ على مودَع المصحف في `tools/gen_madd_index.py`.
"""

from __future__ import annotations

from collections.abc import Sequence
from itertools import pairwise
from typing import Final, Literal

from slge.cells import SUKUN, Cell, licensed
from slge.marifa import drop_tanwin

__all__ = ["binary_ok", "continue_licensed", "has_vc", "kinds", "madd", "pause_licensed"]

Word = tuple[Cell, ...]
K = Literal["cv", "v", "c"]
Syl = Literal["CV", "CVV", "CVC", "CVVC", "CVCC", "CVVCC"]
_MADD: Final[dict[str, str]] = {"ا": "فتح", "و": "ضم", "ي": "كسر"}
_SYL: Final[dict[tuple[str, ...], Syl]] = {
    (): "CV", ("v",): "CVV", ("c",): "CVC", ("v", "c"): "CVVC", ("c", "c"): "CVCC",
    ("v", "c", "c"): "CVVCC"}
PAUSE_ONLY: Final[frozenset[str]] = frozenset({"CVCC", "CVVCC"})
SILENT_WAW: Final[tuple[Word, ...]] = (
    (("ء", "ضم"), ("و", SUKUN), ("ل", "فتح"), ("ء", "كسر"), ("ك", "فتح")),   # أُولَئِكَ
    (("ء", "ضم"), ("و", SUKUN), ("ل", "ضم"), ("و", SUKUN)),                   # أُولُو
    (("ء", "ضم"), ("و", SUKUN), ("ل", "كسر"), ("ي", SUKUN)),                  # أُولِي
    (("ء", "ضم"), ("و", SUKUN), ("ل", "فتح"), ("ا", SUKUN), ("ء", "كسر")),    # أُولَاءِ
    (("ء", "ضم"), ("و", SUKUN), ("ل", "فتح"), ("ا", SUKUN), ("ت", "ضم")),     # أُولَاتُ
)


def kinds(w: Sequence[Cell]) -> list[K]:
    """متحرّكٌ `cv`؛ مدٌّ `v` (ألفٌ بعد فتح، واوٌ بعد ضمّ، ياءٌ بعد كسر — ساكنةً)؛ وإلّا ساكنٌ `c`."""

    out: list[K] = []
    for i, (carrier, state) in enumerate(w):
        if state != SUKUN:
            out.append("cv")
        elif i > 0 and _MADD.get(carrier) == w[i - 1][1]:
            out.append("v")
        else:
            out.append("c")
    return out


def _parse(k: Sequence[K]) -> list[Syl] | None:
    """`Stages.parse` بلا قطعةٍ صادرة: المقاطعُ أو `None`."""

    if not k or k[0] != "cv":
        return None if k else []
    out: list[Syl] = []
    i = 0
    while i < len(k):
        if k[i] != "cv":
            return None
        j = i + 1
        while j < len(k) and k[j] != "cv":
            j += 1
        s = _SYL.get(tuple(k[i + 1:j]))
        if s is None:
            return None
        out.append(s)
        i = j
    return out


def continue_licensed(w: Sequence[Cell]) -> bool:
    """`Ternary.continueB` على الأصناف: بلا قطعةٍ صادرة ولا مقطعٍ وقفيّ."""

    ss = _parse(kinds(w))
    return ss is not None and all(s not in PAUSE_ONLY for s in ss)


def pause_licensed(w: Sequence[Cell]) -> bool:
    """`Ternary.pauseB`: كذلك إلّا المقطعَ الأخير."""

    ss = _parse(kinds(w))
    return ss is not None and all(s not in PAUSE_ONLY for s in ss[:-1])


def binary_ok(w: Sequence[Cell]) -> bool:
    """`Ternary.binOK` على الأصناف = `cells.licensed` (`licensed_eq_binOK`)."""

    k = kinds(w)
    return not k or (k[0] == "cv" and all(a == "cv" or b == "cv" for a, b in pairwise(k)))


def has_vc(w: Sequence[Cell]) -> bool:
    """مدٌّ ثمّ ساكن: المدُّ اللازم على الأصناف."""

    k = kinds(w)
    return any(a == "v" and b == "c" for a, b in pairwise(k))


def _next_hamza(nxt: Sequence[Cell]) -> bool:
    return bool(nxt) and nxt[0][0] == "ء"


def _madd_at(w: Sequence[Cell], i: int, nxt: Sequence[Cell], pause: bool) -> str | None:
    if kinds(w)[i] != "v":
        return None
    if i + 1 == len(w):
        return "منفصل" if _next_hamza(nxt) and not pause else "طبيعيّ"
    x = w[i + 1]
    if x[0] == "ء":
        return "متّصل"
    if x[1] == SUKUN:
        return "لازم مثقَّل" if i + 2 < len(w) and w[i + 2][0] == x[0] else "لازم مخفَّف"
    if pause and i + 2 == len(w):
        return "عارض"
    return "طبيعيّ"


def _lin_at(w: Sequence[Cell], i: int, pause: bool) -> bool:
    if not pause or i + 2 != len(w) or i == 0:
        return False
    x, p = w[i], w[i - 1]
    return x[0] in "وي" and x[1] == SUKUN and p[1] == "فتح"


def _sila(w: Sequence[Cell], nxt: Sequence[Cell]) -> str | None:
    if len(w) < 2 or not nxt:
        return None
    h, p = w[-1], w[-2]
    if h[0] == "ه" and h[1] in ("ضم", "كسر") and p[1] != SUKUN:
        return "صلة كبرى" if _next_hamza(nxt) else "صلة صغرى"
    return None


def madd(w: Sequence[Cell], nxt: Sequence[Cell] = (), pause: bool = False) -> list[tuple[int, str]]:
    """مدودُ الكلمة (الموضع، الحكم): `next` التاليةُ وصلًا، و`pause` وقفٌ على الكلمة (يُردّ التنوين)."""

    if pause:
        w = drop_tanwin(tuple(w))
    out: list[tuple[int, str]] = []
    silent = tuple(w) in SILENT_WAW
    for i in range(len(w)):
        if silent and i == 1:
            out.append((i, "محجوب"))
            continue
        k = _madd_at(w, i, nxt, pause)
        if k is not None:
            out.append((i, k))
        elif _lin_at(w, i, pause):
            out.append((i, "لين"))
    s = _sila(w, nxt)
    if s is not None:
        out.append((len(w) - 1, s))
    return out


def _check() -> None:
    from slge.rawabit import cells_of

    qalu, kana = cells_of("قَالُو"), cells_of("كَانَ")  # الفارقةُ بقيّةُ رسمٍ تُردّ في الغانم
    assert kinds(qalu) == ["cv", "v", "cv", "v"] and madd(qalu) == [(1, "طبيعيّ"), (3, "طبيعيّ")]
    assert madd(cells_of("اَسَّمَاءِ")) == [(4, "متّصل")]
    dallin = cells_of("اَضَّالِّينَ")
    assert madd(dallin) == [(3, "لازم مثقَّل"), (6, "طبيعيّ")]
    assert continue_licensed(dallin) and not licensed(dallin) and has_vc(dallin)  # ثلاثيٌّ فقط = لازم
    assert madd(cells_of("ءَالْءَانَ")) == [(1, "لازم مخفَّف"), (4, "طبيعيّ")]
    alamin = cells_of("اَلْعَالَمِينَ")
    assert madd(alamin, pause=True) == [(3, "طبيعيّ"), (6, "عارض")]
    assert madd(alamin)[1] == (6, "طبيعيّ")
    assert madd(cells_of("خَوْفٌ"), pause=True) == [(1, "لين")] and madd(cells_of("خَوْفٌ")) == []
    assert madd(cells_of("إِنَّهُ"), kana) == [(3, "صلة صغرى")]
    assert madd(cells_of("إِنَّهُ"), cells_of("إِلَّا")) == [(3, "صلة كبرى")]
    assert madd(cells_of("بِمَا"), cells_of("أُنْزِلَ")) == [(2, "منفصل")]
    assert madd(cells_of("بِمَا"), kana) == [(2, "طبيعيّ")]
    assert madd(cells_of("ءَامَنُو")) == [(1, "طبيعيّ"), (4, "طبيعيّ")]
    assert madd(cells_of("أُولَئِكَ")) == [(1, "محجوب")]
    for w in (qalu, kana, dallin, alamin):
        assert binary_ok(w) == licensed(w)
        k = kinds(w)
        assert k[0] != "v" and all(not (a == "v" and b == "v") for a, b in pairwise(k))


_check()
