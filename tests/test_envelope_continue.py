"""الوصلُ بالوزن والغلافُ الثنائيّ (ADR ١١): مرآةُ `A116.Ternary.continue_count_closed` و`envelope_*`.

التوقّعاتُ مكتوبةٌ باليد: أعدادُ الوصل للأوزان 0..14 (`CONT`؛ منها 2..12 مجموعُها 304)، وتساوي
‎(fib(n+1) + χ(n))/2‎ بـ ‎χ = 1، −1، 0‎ دوريًّا؛ والغلافُ 375 منها 75 وقفًا و59 وصلًا.
والطفرات: الوصلُ ليس فيبوناتشي؛ وقراءةُ كلّ ‎C‎ وحدَها ساكنًا (لا مدًّا) تُسقط الأعيانَ إلى 35.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator, Sequence
from itertools import product

from gate.licence import K, continue_licensed, pause_licensed

CONT = [1, 0, 1, 2, 2, 4, 7, 10, 17, 28, 44, 72, 117, 188, 305]
FIB = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]
CHI = (1, -1, 0)


def _kseqs(n: int) -> Iterator[tuple[K, ...]]:
    if n == 0:
        yield ()
        return
    if n >= 2:
        for t in _kseqs(n - 2):
            yield ("cv", *t)
    for t in _kseqs(n - 1):
        yield ("v", *t)
    for t in _kseqs(n - 1):
        yield ("c", *t)


def _count(n: int, pred: Callable[[Sequence[K]], bool]) -> int:
    return sum(1 for k in _kseqs(n) if pred(k))


def test_continue_count_closed_form() -> None:
    got = [_count(n, continue_licensed) for n in range(15)]
    assert got == CONT
    assert all(2 * a == FIB[n + 1] + CHI[n % 3] for n, a in enumerate(CONT))
    assert sum(CONT[2:13]) == 304
    # الوقفُ = الوصلُ + مقطعٌ طرفيٌّ CVCC (4) أو CVVCC (5)
    for n in range(5, 15):
        assert _count(n, pause_licensed) == CONT[n] + CONT[n - 4] + CONT[n - 5] == FIB[n]


def _envelope(n: int) -> Iterator[str]:
    for t in product("CV", repeat=n):
        s = "".join(t)
        if s[0] == "C" and s[-1] == "C" and "VV" not in s:
            yield s


def _readings(s: str, lone: tuple[K, ...] = ("v", "c")) -> list[tuple[K, ...]]:
    opts: list[tuple[K, ...]] = []
    i = 0
    while i < len(s):
        if s[i] == "C" and s[i + 1: i + 2] == "V":
            opts.append(("cv",))
            i += 2
        else:
            opts.append(lone)
            i += 1
    return list(product(*opts))


def _env_total(pred: Callable[[str], bool]) -> int:
    return sum(1 for n in range(2, 13) for s in _envelope(n) if pred(s))


def test_envelope_count_equals_but_members_differ() -> None:
    assert _env_total(lambda s: True) == 375
    assert _env_total(lambda s: any(pause_licensed(r) for r in _readings(s))) == 75
    assert _env_total(lambda s: any(continue_licensed(r) for r in _readings(s))) == 59


def test_mutations_are_rejected() -> None:
    assert [_count(n, continue_licensed) for n in range(2, 15)] != FIB[2:15]
    # الغلافُ أعمى عن المدّ: لو قُرئت ‎C‎ وحدَها ساكنًا أبدًا لنقص المرخَّصُ إلى 35
    only_c = _env_total(lambda s: any(pause_licensed(r) for r in _readings(s, ("c",))))
    assert only_c == 35 != 75


def test_envelope_per_length_and_recurrences() -> None:
    """لكلّ طولٍ 2..12 (ADR ١٢): الأعدادُ مكتوبةٌ باليد، والتكراران عليها — الوصلُ أبقارُ نارايانا
    ‎C(n) = C(n−1) + C(n−3)‎ والوقفُ ‎P(n) = P(n−2) + P(n−3) + P(n−4)‎
    و‎3P(n) = C(n+1)+C(n)+2C(n−1)−(−1)ⁿ‎.
    الطفرة: تكرارُ فيبوناتشي (عددُ الغلاف نفسِه) لا يصدق على المرخَّص."""

    p = [0, 1, 1, 2, 2, 4, 5, 8, 11, 17, 24]
    c = [0, 1, 1, 1, 2, 3, 4, 6, 9, 13, 19]
    for n in range(2, 13):
        env = list(_envelope(n))
        assert sum(any(pause_licensed(r) for r in _readings(s)) for s in env) == p[n - 2]
        assert sum(any(continue_licensed(r) for r in _readings(s)) for s in env) == c[n - 2]
    assert all(c[i] == c[i - 1] + c[i - 3] for i in range(3, 11))
    assert all(p[i] == p[i - 2] + p[i - 3] + p[i - 4] for i in range(4, 11))
    assert all(3 * p[i] == c[i + 1] + c[i] + 2 * c[i - 1] - (-1) ** (i + 2) for i in range(3, 10))
    assert not all(p[i] == p[i - 1] + p[i - 2] for i in range(2, 11))
    for n, a in enumerate(CONT):  # الشكلُ المغلق بالصحاح (`continue_count_closed_form`)
        assert 2 * a == FIB[n + 1] + (n % 3 == 0) - (n % 3 == 1)
