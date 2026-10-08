"""حسمُ الجذع: قسمةٌ واحدة بقرينتين — مرآةُ `Slge.Hasm`.

ما يسأله المرجعُ عن الكلمة هو **قسمتُها** (سوابق، أل، جذع، لواحق) لا قالبُها؛ فالقراءاتُ التي تتّفق في
القسمة وتختلف في القالب قسمةٌ واحدة (`segments`). فإن بقيت قسمتان فأكثر حُسم بينها بالقرائن لا
بالحذف: (١) التركيبيّة — الأداةُ المجاورة توافق القراءة (`adawat.fits`)؛ (٢) المعجميّة — جذرُ القراءة في
المقاييس (`maqayis.attested`)؛ (٣) تكرارُ الجذر في المودَع — كم صورةً وحيدةَ القسمة في المصحف لها هذا
الجذر (`hasm_table.ROOT_FREQ`، مولَّدٌ). الدرجةُ عددٌ واحد مرتَّبٌ ترتيبًا معجميًّا (`score`)، والحسمُ
**الأعلى الوحيد** (`best`)؛ وإن تساوت قسمتان فالاسمُ `TIE` ولا يُختار. القراءاتُ لا تُحذف: الحسمُ اختيارُ
قسمةٍ منها (`hasm_mem`) والقائمةُ كما هي.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from slge.adawat import Adat, fits
from slge.cells import Cell
from slge.hasm_table import BOUND, ROOT_FREQ
from slge.jidh import Reading
from slge.maqayis import _code, attested, roots_of

__all__ = ["BOUND", "Hasm", "Seg", "best", "freq", "hasm", "score", "seg_of", "segments"]

Word = tuple[Cell, ...]
Seg = tuple[tuple[Word, ...], int, Word, Word]
"""القسمة: (السوابق، أل، الجذع، اللاحقة)."""

NAMES: Final[tuple[str, ...]] = ("NO_READING", "UNIQUE", "DECIDED", "TIE")


def seg_of(rd: Reading) -> Seg:
    return (rd.pre, rd.al, rd.stem, rd.suf)


def segments(rs: tuple[Reading, ...]) -> tuple[tuple[Seg, tuple[Reading, ...]], ...]:
    """القسماتُ المتمايزة بترتيب أوّل ظهورها، وقراءاتُ كلٍّ منها."""

    out: dict[Seg, list[Reading]] = {}
    for rd in rs:
        out.setdefault(seg_of(rd), []).append(rd)
    return tuple((s, tuple(v)) for s, v in out.items())


def freq(rd: Reading) -> int:
    """أكبرُ تكرارٍ في المودَع لجذرٍ من جذور القراءة (0 إن لم يُشهد)."""

    return max((ROOT_FREQ.get(_key(r), 0) for r in roots_of(rd)), default=0)


def _key(r: tuple[str, str, str]) -> int:
    a, b, d = _code(r)
    return a * 900 + b * 30 + d


def score(a: Adat | None, group: tuple[Reading, ...]) -> int:
    """درجةُ القسمة: الجوارُ ثمّ المعجمُ ثمّ التكرار، ترتيبًا معجميًّا في عددٍ واحد (`score`)."""

    n = 1 if a is not None and any(fits(a, rd) for rd in group) else 0
    lex = 1 if any(attested(rd) for rd in group) else 0
    f = max(freq(rd) for rd in group)
    assert f < BOUND
    return (n * 2 + lex) * BOUND + f


def best(scores: tuple[int, ...]) -> int | None:
    """موضعُ الأعلى إن كان وحيدًا، وإلّا `None` (`best`)."""

    if not scores:
        return None
    top = max(scores)
    return scores.index(top) if scores.count(top) == 1 else None


@dataclass(frozen=True)
class Hasm:
    name: str
    seg: Seg | None
    readings: tuple[Reading, ...]
    """القراءاتُ المختارةُ قسمتُها (كلُّها إن كانت القسمةُ واحدة)؛ فارغةٌ عند `TIE`/`NO_READING`."""


def hasm(a: Adat | None, rs: tuple[Reading, ...]) -> Hasm:
    """حسمُ القسمة: واحدةٌ بلا قرينة، أو الأعلى الوحيدةُ بالقرائن، أو تعادلٌ باسمه (`hasm`)."""

    gs = segments(rs)
    if not gs:
        return Hasm("NO_READING", None, ())
    if len(gs) == 1:
        return Hasm("UNIQUE", gs[0][0], gs[0][1])
    i = best(tuple(score(a, g) for _, g in gs))
    if i is None:
        return Hasm("TIE", None, ())
    return Hasm("DECIDED", gs[i][0], gs[i][1])


def _check() -> None:
    assert best(()) is None and best((3,)) == 0 and best((1, 3, 2)) == 1 and best((3, 3)) is None
    assert max(ROOT_FREQ.values(), default=0) < BOUND and all(v > 0 for v in ROOT_FREQ.values())
    assert NAMES == ("NO_READING", "UNIQUE", "DECIDED", "TIE")
    assert hasm(None, ()).name == "NO_READING"


_check()
