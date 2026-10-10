"""عددُ المرخَّص وقفًا بالوزن فيبوناتشي (ADR ١٠): مرآةُ `A116.Ternary.pause_count_fib`.

الوزنُ: `cv` = 2، `v` = 1، `c` = 1 (`kw`). عددُ متتاليات الأصناف التي وزنُها n (n ≥ 2) ويرخّصها الوقفُ
(`pause_licensed`، مرآةُ `Ternary.pauseB`) هو fib n؛ ومجموعُها من 2 إلى 12 هو 375 (`pause_count_375`).
التوقّعاتُ مكتوبةٌ باليد لا من الشيفرة؛ والطفرتان: الوصلُ ليس فيبوناتشي، والوقفُ بقطعةٍ صادرة ليس كذلك.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator, Sequence

from gate.licence import K, continue_licensed, parse, pause_licensed

# fib 2 … fib 14 مكتوبةً باليد (fib 0 = 0، fib 1 = 1)
FIB = {2: 1, 3: 2, 4: 3, 5: 5, 6: 8, 7: 13, 8: 21, 9: 34, 10: 55, 11: 89, 12: 144, 13: 233, 14: 377}


def _kseqs(n: int) -> Iterator[tuple[K, ...]]:
    """`kseqs n`: كلُّ متتاليات الأصناف بالوزن n، بلا تكرار."""

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


def test_kseqs_are_the_weighted_sequences() -> None:
    # عددُ المتتاليات بالوزن n: a(n) = a(n-2) + 2·a(n-1) — Pell: 1, 2, 5, 12, 29
    assert [len(set(_kseqs(n))) for n in range(5)] == [1, 2, 5, 12, 29]
    assert [len(list(_kseqs(n))) for n in range(5)] == [1, 2, 5, 12, 29]


def test_pause_count_is_fib() -> None:
    assert _count(1, pause_licensed) == 0  # الوزنُ 1: لا مرخَّص (`cnt_start_one`)
    for n, f in FIB.items():
        assert _count(n, pause_licensed) == f, n
    assert sum(_count(n, pause_licensed) for n in range(2, 13)) == 375


def test_mutations_are_not_fib() -> None:
    """الوصلُ يرفض المقطعَ الوقفيّ الأخير فيقلّ عن fib؛ والوقفُ بقطعةٍ صادرة يزيد عليه."""

    def lead_allowed(k: Sequence[K]) -> bool:
        p = parse(k)
        return p is not None and all(s not in ("CVCC", "CVVCC") for s in p[1][:-1])

    cont = [_count(n, continue_licensed) for n in FIB]
    lead = [_count(n, lead_allowed) for n in FIB]
    assert cont != list(FIB.values()) and lead != list(FIB.values())
    assert all(c <= f for c, f in zip(cont, FIB.values(), strict=True))
    assert all(x >= f for x, f in zip(lead, FIB.values(), strict=True))
