"""`G0.METRIC-0`: `ArabicStateCertificate` — حالُ العربية مُشتَقّةً بالكامل.

ليس في هذه الشهادة حقلٌ يُملأ يدويًّا: كلُّ رقمٍ فيها له طريقٌ إلى شاهدٍ ذي
مسارِ سلطة، أو إلى غيابٍ مقيسٍ في المقام المُعلَن. وهي تحمل سقفَها معها: مقامٌ
مُعلَنٌ لا أنطولوجيا تامّة، وبوّاباتٌ لا مقاديرُ معرفيّة، وتغطيةٌ لا أهليّة.

و`ArabicTotalCoverage` عنوانٌ رئيسٌ **لا يُقرأ وحدَه**: هو وسطُ درجاتِ الأوراق
منسوبًا إلى آخر بوّابة، ويُعرَض دائمًا ومعه مكوّناتُه التسعةُ مستقلّةً، لأنّ
دمجَ `Blind` و`Transfer` في رقمٍ واحدٍ يُخفي الفرقَ الذي أُنشئت الشهادةُ لإظهاره.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from ..canonical_content import canonical_bytes, canonical_digest
from .aggregate import DerivedRatio, NodeAggregate, aggregate_universe
from .blockers import BlockerRow, rank_blockers
from .evidence import EvidenceLedger
from .governance import GovernanceIndicators, derive_governance_indicators
from .laws import CAPABILITY_LAWS
from .maturity import GATE_SEQUENCE, MaturityStage
from .measure import LeafMeasurement, measure_leaves
from .universe import CapabilityUniverse, UniverseManifest

__all__ = [
    "COVERAGE_INDICATOR_NAMES",
    "ArabicStateCertificate",
    "CertificateNodeRow",
    "derive_arabic_state_certificate",
]

COVERAGE_INDICATOR_NAMES: Mapping[MaturityStage, str] = {
    MaturityStage.S1_DECLARED: "DeclaredCoverage",
    MaturityStage.S2_MODELED: "ModeledCoverage",
    MaturityStage.S3_EXECUTABLE: "ExecutableCoverage",
    MaturityStage.S4_TESTED: "TestedCoverage",
    MaturityStage.S5_FROZEN_DOMAIN: "FrozenDomainCoverage",
    MaturityStage.S6_GOLD_EVALUATED: "GoldCoverage",
    MaturityStage.S7_BLIND_VERIFIED: "BlindVerifiedCoverage",
    MaturityStage.S8_TRANSFER_VERIFIED: "TransferVerifiedCoverage",
    MaturityStage.S9_REPRODUCED: "ReproducedCoverage",
}
"""أسماءُ المكوّنات التسعة؛ تبقى مستقلّةً ولا تُدمَج في رقمٍ واحد."""


@dataclass(frozen=True)
class CertificateNodeRow:
    """صفُّ عقدةٍ في الشهادة: بوّاباتُها، وتغطيتُها، وأهليّتُها، ومانعُها."""

    node_id: str
    title: str
    kind: str
    aggregate: NodeAggregate
    measurement: LeafMeasurement | None

    @property
    def gate_answers(self) -> dict[str, bool]:
        """جوابُ كلّ بوّابةٍ بنعم أو لا، للورقة وللأب على سواء."""

        floor = (
            self.measurement.attained_stage
            if self.measurement is not None
            else None
        )
        answers: dict[str, bool] = {}
        for stage in GATE_SEQUENCE[1:]:
            if floor is not None:
                answers[stage.value] = floor.gate_index >= stage.gate_index
            else:
                ratio = self.aggregate.coverage[stage]
                answers[stage.value] = (
                    ratio.denominator > 0 and ratio.numerator == ratio.denominator
                )
        return answers

    def as_canonical_content(self) -> dict[str, object]:
        """المحتوى القانونيّ لصفّ العقدة."""

        return {
            "node_id": self.node_id,
            "title": self.title,
            "kind": self.kind,
            "gate_answers": self.gate_answers,
            "aggregate": self.aggregate.as_canonical_content(),
            "measurement": (
                None
                if self.measurement is None
                else self.measurement.as_canonical_content()
            ),
        }


@dataclass(frozen=True)
class ArabicStateCertificate:
    """شهادةُ حالِ العربية: مُشتَقّةٌ بالكامل، ومحمولةٌ بسقفها ومقامها."""

    universe_manifest: UniverseManifest
    rows: Mapping[str, CertificateNodeRow]
    coverage: Mapping[str, DerivedRatio]
    readiness: DerivedRatio
    certified_completion: DerivedRatio
    arabic_total_coverage: DerivedRatio
    governance: GovernanceIndicators
    blockers: tuple[BlockerRow, ...]
    laws: tuple[str, ...]

    @property
    def next_gate(self) -> str | None:
        """البوّابةُ التالية: أعلى مُعوِّقٍ بما يفتحه، لا بالحدس."""

        if not self.blockers:
            return None
        return self.blockers[0].blocking_reason

    def as_canonical_content(self) -> dict[str, object]:
        """المحتوى القانونيّ للشهادة كاملةً."""

        return {
            "universe_manifest": self.universe_manifest.as_canonical_content(),
            "coverage": {
                name: ratio.as_canonical_content()
                for name, ratio in self.coverage.items()
            },
            "readiness": self.readiness.as_canonical_content(),
            "certified_completion": self.certified_completion.as_canonical_content(),
            "arabic_total_coverage": (
                self.arabic_total_coverage.as_canonical_content()
            ),
            "governance": self.governance.as_canonical_content(),
            "blockers": [row.as_canonical_content() for row in self.blockers],
            "next_gate": self.next_gate,
            "rows": [
                self.rows[node_id].as_canonical_content()
                for node_id in sorted(self.rows)
            ],
            "laws": list(self.laws),
        }

    @property
    def certificate_digest(self) -> str:
        """مُلخَّصُ محتوى الشهادة؛ شهادتان على مقامين ليستا مقارنة."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


def derive_arabic_state_certificate(
    universe: CapabilityUniverse, ledger: EvidenceLedger
) -> ArabicStateCertificate:
    """اشتقّ الشهادةَ من المقام والدفتر وحدَهما؛ لا حقلَ فيها يُملأ يدويًّا."""

    measurements = measure_leaves(universe, ledger)
    aggregates = aggregate_universe(universe, measurements)
    root = aggregates[universe.root_id]
    rows = {
        node_id: CertificateNodeRow(
            node_id=node_id,
            title=universe.node(node_id).title,
            kind=universe.node(node_id).kind.value,
            aggregate=aggregates[node_id],
            measurement=measurements.get(node_id),
        )
        for node_id in universe.node_ids()
    }
    coverage = {
        COVERAGE_INDICATOR_NAMES[stage]: root.coverage[stage]
        for stage in GATE_SEQUENCE[1:]
    }
    leaves = universe.leaf_ids()
    last_gate_index = GATE_SEQUENCE[-1].gate_index
    total_coverage = DerivedRatio(
        numerator=sum(
            measurements[leaf_id].attained_stage.gate_index for leaf_id in leaves
        ),
        denominator=len(leaves) * last_gate_index,
        denominator_source=(
            f"{universe.manifest.universe_id}.leaves × {GATE_SEQUENCE[-1].value}"
        ),
    )
    return ArabicStateCertificate(
        universe_manifest=universe.manifest,
        rows=rows,
        coverage=coverage,
        readiness=root.readiness,
        certified_completion=root.certified_completion,
        arabic_total_coverage=total_coverage,
        governance=derive_governance_indicators(universe, ledger, measurements),
        blockers=rank_blockers(universe, measurements),
        laws=CAPABILITY_LAWS,
    )
