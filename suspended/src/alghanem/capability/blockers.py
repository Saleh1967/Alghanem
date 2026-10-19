"""`G0.METRIC-0`: ترتيبُ البوّابات بما تفتحه، لا بالحدس.

أعلى مُعوِّقٍ ليس أكثرَها ذكرًا ولا أحدثَها، بل البوّابةُ التي يفتح إغلاقُها
أكبرَ عددٍ من الأوراق المحجوبة عند الدرجة نفسِها. والترتيبُ مُشتَقٌّ ومستقرّ:
عند تساوي العدد يُرتَّب بالمعرّف، فلا يتغيّر جوابُ «ما التالي؟» بتغيّر ترتيب
القراءة.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from .maturity import MaturityStage
from .measure import LeafMeasurement
from .universe import CapabilityUniverse

__all__ = [
    "BlockerRow",
    "rank_blockers",
]


@dataclass(frozen=True)
class BlockerRow:
    """مُعوِّقٌ مُجمَّع: بوّابةٌ ومانعُها، وكم ورقةً وأيَّ مجالاتٍ يحجب."""

    gate: MaturityStage
    blocking_reason: str
    blocked_leaf_count: int
    blocked_domains: tuple[str, ...]
    example_leaf_ids: tuple[str, ...]

    def as_canonical_content(self) -> dict[str, object]:
        """المحتوى القانونيّ للمُعوِّق."""

        return {
            "gate": self.gate.value,
            "blocking_reason": self.blocking_reason,
            "blocked_leaf_count": self.blocked_leaf_count,
            "blocked_domains": list(self.blocked_domains),
            "example_leaf_ids": list(self.example_leaf_ids),
        }


def _domain_of(universe: CapabilityUniverse, leaf_id: str) -> str:
    current = universe.node(leaf_id)
    while current.parent_id is not None and current.parent_id != universe.root_id:
        current = universe.node(current.parent_id)
    return current.node_id


def rank_blockers(
    universe: CapabilityUniverse,
    measurements: Mapping[str, LeafMeasurement],
    *,
    example_limit: int = 5,
) -> tuple[BlockerRow, ...]:
    """رتّب المُعوِّقات بما تحجبه من أوراق، ثمّ بالمعرّف عند التساوي."""

    if type(example_limit) is not int or example_limit < 0:
        raise ValueError("an example limit is a non-negative count")
    grouped: dict[tuple[MaturityStage, str], list[str]] = {}
    for leaf_id in universe.leaf_ids():
        row = measurements[leaf_id]
        if row.next_gate is None:
            continue
        grouped.setdefault((row.next_gate, row.blocking_reason), []).append(leaf_id)
    rows = [
        BlockerRow(
            gate=gate,
            blocking_reason=reason,
            blocked_leaf_count=len(leaf_ids),
            blocked_domains=tuple(
                sorted({_domain_of(universe, leaf_id) for leaf_id in leaf_ids})
            ),
            example_leaf_ids=tuple(sorted(leaf_ids)[:example_limit]),
        )
        for (gate, reason), leaf_ids in grouped.items()
    ]
    return tuple(
        sorted(
            rows,
            key=lambda row: (-row.blocked_leaf_count, row.gate.gate_index),
        )
    )
