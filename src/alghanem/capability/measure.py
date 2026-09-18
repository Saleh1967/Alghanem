"""`G0.METRIC-0`: قياسُ الورقة من شواهدها، والغيابُ رقمٌ لا فراغ.

ورقةٌ بلا شاهدٍ ليست خطأَ بناء: هي `S0_ABSENT` بمانعها وبوّابتها التالية
(`UnimplementedCapabilityMustRemainVisible`). والقفزُ فوق بوّابةٍ مفتوحة يُرصَد
ولا يُصرَف: شاهدٌ عند `S6` وبوّابةُ `S3` مفتوحةٌ ادّعاءٌ بلا طريق، فيُسجَّل
`jumped_gates` ولا يرفع الدرجةَ المُشتَقّة.

والشاهدُ الناقضُ يُبطِل بوّابتَه ولا يُحذَف: `TheMetricMustBeAllowedToGoDown`.
"""

from __future__ import annotations

from dataclasses import dataclass

from .evidence import EvidenceLedger, EvidencePolarity, ScopedCapabilityEvidence
from .maturity import GATE_SEQUENCE, MaturityStage, blocking_reason_for_gate
from .node import CapabilityNode
from .universe import CapabilityUniverse

__all__ = [
    "LeafMeasurement",
    "measure_leaves",
]


@dataclass(frozen=True)
class LeafMeasurement:
    """قياسُ ورقةٍ واحدة: درجتُها، ومانعُها، وبوّابتُها التالية، وبواقيها."""

    capability_id: str
    attained_stage: MaturityStage
    attested_gates: tuple[MaturityStage, ...]
    contested_gates: tuple[MaturityStage, ...]
    jumped_gates: tuple[MaturityStage, ...]
    blocking_reason: str
    next_gate: MaturityStage | None
    readiness_gate: MaturityStage
    evidence_count: int
    residuals: tuple[str, ...]
    scopes: tuple[str, ...]

    @property
    def is_ready(self) -> bool:
        """هل بلغت الورقةُ بوّابةَ الأهليّة المُعلَنة لها؟"""

        return self.attained_stage.gate_index >= self.readiness_gate.gate_index

    @property
    def has_no_jump(self) -> bool:
        """هل خلا سِجِلُّها من ادّعاءٍ فوق بوّابةٍ مفتوحة؟"""

        return not self.jumped_gates

    def as_canonical_content(self) -> dict[str, object]:
        """المحتوى القانونيّ للقياس."""

        return {
            "capability_id": self.capability_id,
            "attained_stage": self.attained_stage.value,
            "attested_gates": [gate.value for gate in self.attested_gates],
            "contested_gates": [gate.value for gate in self.contested_gates],
            "jumped_gates": [gate.value for gate in self.jumped_gates],
            "blocking_reason": self.blocking_reason,
            "next_gate": None if self.next_gate is None else self.next_gate.value,
            "readiness_gate": self.readiness_gate.value,
            "evidence_count": self.evidence_count,
            "residuals": list(self.residuals),
            "scopes": list(self.scopes),
        }


def _attained_stage(effective: frozenset[MaturityStage]) -> MaturityStage:
    attained = MaturityStage.S0_ABSENT
    for gate in GATE_SEQUENCE[1:]:
        if gate not in effective:
            break
        attained = gate
    return attained


def _measure_leaf(
    node: CapabilityNode, items: tuple[ScopedCapabilityEvidence, ...]
) -> LeafMeasurement:
    positive = {
        item.attested_gate
        for item in items
        if item.polarity is EvidencePolarity.POSITIVE
    }
    contested = {
        item.attested_gate
        for item in items
        if item.polarity is EvidencePolarity.NEGATIVE
    }
    effective = frozenset(positive - contested)
    attained = _attained_stage(effective)
    jumped = tuple(
        gate
        for gate in GATE_SEQUENCE
        if gate in effective and gate.gate_index > attained.gate_index
    )
    next_index = attained.gate_index + 1
    next_gate = GATE_SEQUENCE[next_index] if next_index < len(GATE_SEQUENCE) else None
    blocking_reason = (
        "NOTHING_IS_BLOCKED_ABOVE_THE_LAST_GATE"
        if next_gate is None
        else blocking_reason_for_gate(next_gate)
    )
    residuals = tuple(sorted({code for item in items for code in item.residuals}))
    scopes = tuple(sorted({item.scope.scope_digest for item in items}))
    return LeafMeasurement(
        capability_id=node.node_id,
        attained_stage=attained,
        attested_gates=tuple(gate for gate in GATE_SEQUENCE if gate in positive),
        contested_gates=tuple(gate for gate in GATE_SEQUENCE if gate in contested),
        jumped_gates=jumped,
        blocking_reason=blocking_reason,
        next_gate=next_gate,
        readiness_gate=node.readiness_gate,
        evidence_count=len(items),
        residuals=residuals,
        scopes=scopes,
    )


def measure_leaves(
    universe: CapabilityUniverse, ledger: EvidenceLedger
) -> dict[str, LeafMeasurement]:
    """قِس كلَّ ورقةٍ في المقام، بما فيها ما لا شاهدَ له البتّة."""

    return {
        leaf_id: _measure_leaf(universe.node(leaf_id), ledger.for_capability(leaf_id))
        for leaf_id in universe.leaf_ids()
    }
