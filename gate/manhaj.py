"""سلسلةُ القرار — مرآةُ `A116.Qarar.judge1` و`A116.Manhaj.judgeT` (ADR ٥٨).

الدعوى: رقمٌ، ووجودٌ (لا حقيقة/صفة)، ووقوعُ الحسّ على واقعها، ومعارضٌ مودَعٌ بعد الاستقراء،
وأصولُها. الحكمُ لكلّ دعوى بترتيب السلسلة: أصلٌ لم يسبق ← دور؛ أصلٌ ساقط ← ساقط؛ أصلٌ بلا حكم، أو
لا حسَّ — وفي `judge_t`: لا حسَّ ولا أصل (ج1 س45) — ← لا حكم؛ معارض ← خاطئ؛ وجودٌ على أصولٍ قطعيّة
← قطعيّ؛ وإلّا ظنّيّ.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Final, NamedTuple

QATI: Final = "qati"
ZANNI: Final = "zanni"
KHATA: Final = "khata"
SAQIT: Final = "saqit"
DAWR: Final = "dawr"
LA_HUKM: Final = "laHukm"
FALLEN: Final = frozenset({KHATA, SAQIT, DAWR})
SAWAB: Final = frozenset({QATI, ZANNI})


class Daawa(NamedTuple):
    id: int
    wujud: bool
    mahsus: bool
    muarid: bool
    usul: tuple[int, ...] = ()


Judge = Callable[[dict[int, str], Daawa], str]


def _judge(prior: dict[int, str], c: Daawa, taslim: bool) -> str:
    prem = [prior.get(u) for u in c.usul]
    if any(p is None for p in prem):
        return DAWR
    if any(p in FALLEN for p in prem):
        return SAQIT
    ungrounded = not c.mahsus and (not taslim or not c.usul)
    if any(p == LA_HUKM for p in prem) or ungrounded:
        return LA_HUKM
    if c.muarid:
        return KHATA
    if c.wujud and all(p == QATI for p in prem):
        return QATI
    return ZANNI


def judge1(prior: dict[int, str], c: Daawa) -> str:
    return _judge(prior, c, taslim=False)


def judge_t(prior: dict[int, str], c: Daawa) -> str:
    return _judge(prior, c, taslim=True)


def run(cs: Sequence[Daawa], judge: Judge = judge_t) -> list[tuple[int, str]]:
    """الأحكامُ بالترتيب؛ والبحثُ عن الأصل أوّلُ مطابقٍ كما في `List.lookup`."""

    out: list[tuple[int, str]] = []
    prior: dict[int, str] = {}
    for c in cs:
        h = judge(prior, c)
        out.append((c.id, h))
        prior.setdefault(c.id, h)
    return out
