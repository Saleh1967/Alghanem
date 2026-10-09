"""شهادةُ SLGE: الدالُّ خاناتٍ، ومسارُ القراءة أعدادًا، ونوعُ المدلول الخماسيّ (النبهانيّ) — ببصمةٍ مميِّزة؛
مرآةُ `Slge.Shahada` (ADR ٢٧).

البصمةُ عددٌ واحد: اقترانُ كانتور (`A116.Numbering.pair`) لعدد الذرّات (`atomNumber` بصورته المغلقة
`atomNumber_closed`: ‎geo(116, n) + digits(116, bridge)‎) مع ترميز المسار (`encList`) ونوعِ المدلول
(`encMadlul`). شهادتان ببصمةٍ واحدة هما واحدة (`fingerprint_injective`)؛ وإسنادُ نوع المدلول في طبقة
الحكم يغيّر البصمة (`withMadlul_changes_fingerprint`). `madlul=None` = لم يُحكم بعد: السُّلَّمُ يقرأ الدالَّ
من حيث هو، والمدلولُ يُسنَد فوقه بشاهد.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, replace
from typing import Any, Final

from slge.cells import A116_CARRIERS, A116_STATES, Cell
from slge.nabhani import MADLUL

__all__ = ["Shahada", "atom_number", "build", "enc_list", "fingerprint", "pair", "with_madlul"]

Word = tuple[Cell, ...]
_F: Final[int] = 116


@dataclass(frozen=True)
class Shahada:
    """الخاناتُ، والمسارُ (لكلّ بوّابةٍ قارئة عددُ قراءاتها)، ونوعُ المدلول (أو لا حكمَ بعد)."""

    cells: Word
    path: tuple[int, ...]
    madlul: str | None = None


def _bridge_index(c: Cell) -> int:
    """`bridgeIndex`: 4 × (الحاملُ بترتيب الجسر: الهمزةُ والألفُ يتبادلان) + الحالةُ بترتيب الجسر."""

    a = A116_CARRIERS.index(c[0])
    swapped = 28 if a == 0 else 0 if a == 28 else a
    return 4 * swapped + A116_STATES.index(c[1])


def atom_number(w: Word) -> int:
    """`atomNumber` بصورته المغلقة: ‎Σ_{j<n} 116^j + digits₁₁₆(bridge)‎ — مميِّزٌ لكلّ قائمة خانات."""

    geo: int = sum(_F**j for j in range(len(w)))
    digits: int = 0
    for c in w:
        digits = _F * digits + _bridge_index(c)
    return int(geo + digits)


def pair(u: int, r: int) -> int:
    """اقترانُ كانتور (`pair_closed`)."""

    return (u + r) * (u + r + 1) // 2 + r


def enc_list(xs: Sequence[int]) -> int:
    """`encList`: ‎[] ↦ 0؛ x::xs ↦ pair(x, encList xs) + 1‎ — مميِّز."""

    acc = 0
    for x in reversed(xs):
        acc = pair(x, acc) + 1
    return acc


def _enc_madlul(m: str | None) -> int:
    return 0 if m is None else MADLUL.index(m) + 1


def fingerprint(s: Shahada) -> int:
    """`fingerprint`: ‎pair(atomNumber, pair(encList path, encMadlul))‎."""

    return pair(atom_number(s.cells), pair(enc_list(s.path), _enc_madlul(s.madlul)))


def with_madlul(s: Shahada, m: str) -> Shahada:
    """إسنادُ نوع المدلول (من الخمسة) في طبقة الحكم."""

    assert m in MADLUL, m
    return replace(s, madlul=m)


def build(trace: Sequence[Any]) -> Shahada | None:
    """من أثر `gates.climb`: الخاناتُ من بوّابة الخانة، والمسارُ عددُ قراءات كلّ بوّابةٍ قارئة؛ ولا شهادةَ
    إن وقف السُّلَّم عند بوّابةٍ حاكمة."""

    from slge.gates import LADDER, Pass

    governing = {g.name for g in LADDER if g.governing}
    if len(trace) != len(LADDER) or not all(isinstance(t, Pass) for t in trace):
        return None
    cells: Word = tuple(trace[0].out)
    path: list[int] = []
    for t in trace:
        if t.gate in governing:
            continue
        out = t.out
        path.append(len(out) if isinstance(out, list | tuple) else 0 if out is None else 1)
    return Shahada(cells, tuple(path), None)


def _check() -> None:
    from slge.rawabit import cells_of

    w = cells_of("كَتَبَ")
    s = Shahada(w, (0, 0, 2, 1, 1, 1, 1), None)
    assert fingerprint(s) != fingerprint(with_madlul(s, MADLUL[0]))
    assert fingerprint(s) != fingerprint(replace(s, path=(0, 0, 1, 1, 1, 1, 1)))
    assert enc_list(()) == 0 and enc_list((0,)) == 1 and enc_list((0, 0)) == pair(0, 1) + 1
    assert pair(0, 0) == 0 and pair(1, 0) == 1 and pair(0, 1) == 2 and pair(1, 1) == 4
    assert atom_number(()) == 0 and atom_number(w) > atom_number(w[:2])
    assert _bridge_index(("ء", "فتح")) == 0 and _bridge_index(("ا", "سكون")) == 115


_check()
