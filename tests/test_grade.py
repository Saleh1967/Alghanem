"""الدرجاتُ بعدد المقاطع (`A116.Grade`): مرآةٌ بالاستقصاء على `gate.licence` لا على تعريف Lean.

التوقّعاتُ مستقلّة: تُولَّد كلُّ متتاليات الأصناف (cv، v، c) التي تبدأ بمتحرّك وفيها k متحرّكًا (فكلُّ مقطعٍ
متحرّكٌ واحد)، ويُعدّ منها ما يرخّصه `continue_licensed` و`pause_licensed`: ‎4ᵏ‎ وصلًا و‎6·4ᵏ⁻¹‎ وقفًا
(`cont_length`، `pause_length`، `grade_table`). وقانونُ التدرّج (`cont_succ`، `pause_succ`): كلُّ مرخَّصٍ
بـk+1 مقطعًا هو مرخَّصٌ وصلًا بـk مقطعًا ومعه مقطعٌ واحد. والطفرة: لو جاز CVCC داخلَ الكلمة لزاد العدد.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator, Sequence
from itertools import product

from gate.licence import K, continue_licensed, pause_licensed

CODAS: tuple[tuple[K, ...], ...] = ((), ("v",), ("c",), ("v", "c"), ("c", "c"), ("v", "c", "c"))
"""ذيولُ المقاطع الستّة بعد متحرّكها، معدودةً باليد من `Stages.Syl.coda`."""


def seqs(k: int) -> Iterator[tuple[K, ...]]:
    """كلُّ متتاليةٍ تبدأ بمتحرّك وفيها k متحرّكًا وبين المتحرّكات ذيولٌ من ثلاثة أصنافٍ حتى ثلاثٍ —
    مجالٌ أوسعُ من المقاطع الستّة (كلُّ ذيلٍ ‎≤ 3‎ من v وc)، فما يرخّصه القانونُ يُعدّ لا يُفترض."""

    tails = [t for n in range(4) for t in product(("v", "c"), repeat=n)]
    for ts in product(tails, repeat=k):
        yield tuple(x for t in ts for x in ("cv", *t))


def count(k: int, pred: Callable[[Sequence[K]], bool]) -> int:
    return sum(1 for s in seqs(k) if pred(s))


def test_counts_per_grade() -> None:
    got = [(k, count(k, continue_licensed), count(k, pause_licensed)) for k in range(1, 5)]
    assert got == [(1, 4, 6), (2, 16, 24), (3, 64, 96), (4, 256, 384)]


def test_graded_law() -> None:
    # كلُّ مرخَّصٍ بـk+1 مقطعًا = مرخَّصٌ وصلًا بـk ثمّ مقطعٌ واحد (cv وذيله)
    for k in range(1, 4):
        cont_k = {s for s in seqs(k) if continue_licensed(s)}
        for s in seqs(k + 1):
            last = max(i for i, x in enumerate(s) if x == "cv")
            head, syl = s[:last], s[last:]
            if continue_licensed(s):
                assert head in cont_k and syl[1:] in CODAS[:4]
            if pause_licensed(s):
                assert head in cont_k and syl[1:] in CODAS


def test_mutant_medial_cvcc_is_refused() -> None:
    # الطفرة: لو رُخِّص الوصلُ بقانون الوقف (CVCC داخلًا) لما كان العددُ 4ᵏ
    assert count(2, pause_licensed) != 16 and count(2, continue_licensed) == 16
    assert not continue_licensed(("cv", "c", "c", "cv"))  # CVCC + CV
