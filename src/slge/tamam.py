"""قانونُ التمام (ADR ٥٧): الحاجةُ مرفوعةً إلى الكلم — صدارةٌ وإغلاقٌ ووصل — مرآةُ
`formal/Slge/Tamam.lean`.

الحالةُ (مكدَّسُ مجموعاتِ حاجاتٍ مفتوحة، وأقسامُ ما رُئي منذ أوّل الوحدة)؛ والكلمةُ تقضي حتمًا ما تقدر عليه من
المجموعة العليا، ثمّ تُقضى حاجاتُها «قبل» بما رُئي، وتُفتح حاجاتُها «بعد» مجموعةً. ذو الصدارة لا يقضي ما
قبله ولا يقع
وما قبله مفتوح، ولا يرى ما قبله. والوحدةُ تامّةٌ إذا بلغ طريقٌ مكدَّسًا فارغًا.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Final

from slge.haja import HARF_BABS, NEEDS, SADR

__all__ = ["START", "St", "Tok", "fill", "pick", "run_all", "step_all", "step_set", "tamm"]

Tok = tuple[str, str]
"""(القسم: harf/mudmar/fil/ism، الباب)."""

St = tuple[tuple[tuple[str, ...], ...], tuple[str, ...]]
"""(المكدَّس: مجموعاتُ ما يقضي الحاجات، أعلاها أوّلًا؛ أقسامُ ما رُئي بترتيب `ORDER`)."""

START: Final[St] = ((), ())


def fills(t: Tok, m: str) -> bool:
    if m == "ism":
        return t[0] in ("ism", "mudmar")
    if m == "fil":
        return t[0] == "fil"
    return True


def qabl_ok(seen: tuple[str, ...], m: str) -> bool:
    if m == "ism":
        return "ism" in seen or "mudmar" in seen
    if m == "fil":
        return "fil" in seen
    return bool(seen)


def pick(g: tuple[str, ...], t: Tok) -> int | None:
    """الجنسُ بعينه (اسمٌ أو فعل) أوّلًا، ثمّ «جزءُ الكلام»."""

    for i, m in enumerate(g):
        if m != "juz" and fills(t, m):
            return i
    for i, m in enumerate(g):
        if fills(t, m):
            return i
    return None


def fill(stack: tuple[tuple[str, ...], ...], t: Tok) -> tuple[tuple[str, ...], ...]:
    if not stack:
        return ()
    g, rest = stack[0], stack[1:]
    i = pick(g, t)
    if i is None:
        return stack
    g2 = g[:i] + g[i + 1:]
    return rest if not g2 else (g2, *rest)


ORDER: Final[tuple[str, ...]] = ("harf", "mudmar", "fil", "ism")


def add_seen(leaf: str, seen: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(x for x in ORDER if x == leaf or x in seen)


def opens(t: Tok) -> tuple[str, ...]:
    return tuple(m for j, m, _, _ in NEEDS[t[1]] if j == "bad")


def finish(seen0: tuple[str, ...], stack1: tuple[tuple[str, ...], ...], t: Tok) -> St | None:
    sadr = t[1] in SADR
    if sadr and stack1:
        return None
    seen = () if sadr else seen0
    if not all(j != "qabl" or qabl_ok(seen, m) for j, m, _, _ in NEEDS[t[1]]):
        return None
    o = opens(t)
    stack = stack1 if not o else (o, *stack1)
    return (stack, add_seen(t[0], seen))


def step_all(s: St, t: Tok) -> list[St]:
    r = finish(s[1], s[0] if t[1] in SADR else fill(s[0], t), t)
    return [] if r is None else [r]


def _dedup(xs: Iterable[St]) -> list[St]:
    """بلا تكرار، وأوّلُ ظهورٍ أوّلًا (`List.eraseDups`)."""

    return list(dict.fromkeys(xs))


def step_set(states: list[St], ts: Iterable[Tok]) -> list[St]:
    tl = list(ts)
    return _dedup(r for s in states for t in tl for r in step_all(s, t))


def run_all(states: list[St], words: Iterable[Iterable[Tok]]) -> list[St]:
    for w in words:
        states = step_set(states, w)
    return states


def tamm(states: list[St]) -> bool:
    return any(not s[0] for s in states)


def _check() -> None:
    assert all(any(j != "ayy" for j, _, _, _ in NEEDS[b]) for b in HARF_BABS)


_check()
