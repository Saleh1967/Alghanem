"""`G0.METRIC-0.HARDEN`: `ArabicStateCertificate` — حالُ العربية مُشتَقّةً بالكامل.

ليس في هذه الشهادة حقلٌ يُملأ يدويًّا: كلُّ رقمٍ فيها له طريقٌ إلى شاهدٍ ذي
مسارِ سلطة، أو إلى غيابٍ مقيسٍ في المقام المُعلَن. وهي تحمل سقفَها معها: مقامٌ
مُعلَنٌ لا أنطولوجيا تامّة، وبوّاباتٌ لا مقاديرُ معرفيّة، وتغطيةٌ لا أهليّة.

ولم يعد فيها عنوانٌ مركّب: تسعُ بوّاباتٍ نوعيّةٍ لا تصير رقمًا واحدًا بلا
بروتوكول أوزانٍ مُعلَن، فيبقى `CompositeCoverage` **غيرَ معرَّفٍ بسببه** لا
مقدَّرًا (`NoOrdinalGateArithmeticWithoutDeclaredWeights`). وكذلك
`DomainBalancedCoverage` و`DependencyWeightedCoverage`؛ وتُعرَض المجالاتُ صفًّا
صفًّا في `DomainCoverageProfile` بدلًا من تسويتها في وسطٍ واحد.

وتحمل الشهادةُ إصدارَ مُخطَّطها: شهادتان على دلاليّتَي قياسٍ مختلفتين ليستا
مقارنةً رقميّة (`DifferentMeasurementSemanticsAreNotComparableCertificates`).
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from .aggregate import (
    DerivedRatio,
    DomainCoverageProfile,
    NodeAggregate,
    aggregate_universe,
    derive_domain_coverage_profile,
)
from .blockers import BlockerRow, rank_blockers
from .evidence import EvidenceLedger
from .governance import GovernanceIndicators, derive_governance_indicators
from .laws import CAPABILITY_LAWS, DECLARED_COVERAGE_IS_NOT_SYSTEM_CAPABILITY
from .maturity import GATE_SEQUENCE, MaturityStage
from .measure import LeafMeasurement, measure_leaves
from .provenance import (
    CitationProvenanceProfile,
    ReadinessGateOriginProfile,
    derive_citation_provenance_profile,
    derive_readiness_gate_origin_profile,
)
from .universe import CapabilityUniverse, UniverseManifest
from .weights import UndeclaredScalar, UndeclaredScalarReason

__all__ = [
    "CERTIFICATE_SCHEMA_VERSION",
    "COVERAGE_INDICATOR_NAMES",
    "ArabicStateCertificate",
    "CertificateNodeRow",
    "derive_arabic_state_certificate",
]

CERTIFICATE_SCHEMA_VERSION: Final[str] = "arabic-state-certificate.v2"
"""إصدارُ مُخطَّط الشهادة؛ تغيّرُ الدلاليّة يُعلَن هنا ولا يُقرأ تراجعًا في رقم."""

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
            self.measurement.attained_stage if self.measurement is not None else None
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
    gate_profile: Mapping[str, DerivedRatio]
    readiness: DerivedRatio
    certified_completion: DerivedRatio
    composite_coverage: UndeclaredScalar
    domain_coverage_profile: DomainCoverageProfile
    domain_balanced_coverage: UndeclaredScalar
    dependency_weighted_coverage: UndeclaredScalar
    citation_provenance: CitationProvenanceProfile
    readiness_gate_origins: ReadinessGateOriginProfile
    governance: GovernanceIndicators
    blockers: tuple[BlockerRow, ...]
    laws: tuple[str, ...]

    @property
    def schema_version(self) -> str:
        """إصدارُ مُخطَّط هذه الشهادة؛ يُقرأ قبل أن يُقارَن رقمٌ فيها بآخر."""

        return CERTIFICATE_SCHEMA_VERSION

    @property
    def coverage(self) -> Mapping[str, DerivedRatio]:
        """البوّاباتُ التسعُ منفصلةً؛ اسمٌ آخرُ لـ`gate_profile` لا رقمٌ ثانٍ."""

        return self.gate_profile

    @property
    def declared_coverage_law(self) -> str:
        """بلوغُ الإعلان تمامَه ليس تملّكًا لشيءٍ لغويّ؛ القانونُ محمولٌ معه."""

        return DECLARED_COVERAGE_IS_NOT_SYSTEM_CAPABILITY

    @property
    def headline_statement(self) -> str:
        """العنوانُ الصحيح: أسئلةٌ مُعلَنةٌ حاضرة، ولا نسبةَ عربيةٍ مركّبةٌ الآن."""

        declared = self.gate_profile["DeclaredCoverage"]
        return (
            f"{self.universe_manifest.universe_id}: "
            f"{declared.numerator}/{declared.denominator} declared questions are "
            "present. No composite Arabic capability percentage is currently "
            "defined."
        )

    @property
    def next_gate(self) -> str | None:
        """البوّابةُ التالية: أعلى مُعوِّقٍ بما يفتحه، لا بالحدس."""

        if not self.blockers:
            return None
        return self.blockers[0].blocking_reason

    def as_canonical_content(self) -> dict[str, object]:
        """المحتوى القانونيّ للشهادة كاملةً."""

        return {
            "certificate_schema_version": self.schema_version,
            "headline_statement": self.headline_statement,
            "universe_manifest": self.universe_manifest.as_canonical_content(),
            "gate_profile": {
                name: ratio.as_canonical_content()
                for name, ratio in self.gate_profile.items()
            },
            "readiness": self.readiness.as_canonical_content(),
            "certified_completion": self.certified_completion.as_canonical_content(),
            "composite_coverage": self.composite_coverage.as_canonical_content(),
            "domain_coverage_profile": (
                self.domain_coverage_profile.as_canonical_content()
            ),
            "domain_balanced_coverage": (
                self.domain_balanced_coverage.as_canonical_content()
            ),
            "dependency_weighted_coverage": (
                self.dependency_weighted_coverage.as_canonical_content()
            ),
            "citation_provenance": self.citation_provenance.as_canonical_content(),
            "readiness_gate_origins": (
                self.readiness_gate_origins.as_canonical_content()
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
    gate_profile = {
        COVERAGE_INDICATOR_NAMES[stage]: root.coverage[stage]
        for stage in GATE_SEQUENCE[1:]
    }
    return ArabicStateCertificate(
        universe_manifest=universe.manifest,
        rows=rows,
        gate_profile=gate_profile,
        readiness=root.readiness,
        certified_completion=root.certified_completion,
        composite_coverage=UndeclaredScalar(
            name="CompositeCoverage",
            reason=UndeclaredScalarReason.NO_DECLARED_WEIGHT_PROTOCOL,
        ),
        domain_coverage_profile=derive_domain_coverage_profile(universe, aggregates),
        domain_balanced_coverage=UndeclaredScalar(
            name="DomainBalancedCoverage",
            reason=UndeclaredScalarReason.NO_DECLARED_DOMAIN_WEIGHT_PROTOCOL,
        ),
        dependency_weighted_coverage=UndeclaredScalar(
            name="DependencyWeightedCoverage",
            reason=UndeclaredScalarReason.NO_DECLARED_DEPENDENCY_GRAPH,
        ),
        citation_provenance=derive_citation_provenance_profile(universe),
        readiness_gate_origins=derive_readiness_gate_origin_profile(universe),
        governance=derive_governance_indicators(universe, ledger, measurements),
        blockers=rank_blockers(universe, measurements),
        laws=CAPABILITY_LAWS,
    )
