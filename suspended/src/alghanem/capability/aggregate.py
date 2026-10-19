"""`G0.METRIC-0`: التجميعُ الفركتاليّ، والنسبةُ محمولةً بمقامها.

`DerivedRatio` لا تُعرَض قيمةً مجرّدة: تحمل بسطَها ومقامَها ومصدرَ تجميد مقامها
(`ARatioCarriesItsDenominator`)، ومقامُ الصفر يُخرِج **غيرَ معرَّفة** لا صفرًا
ولا تمامًا.

والتغطيةُ غيرُ الأهليّة (`Breadth != Readiness`): الأولى مقدارُ ما بُني عبر
المجال المُعلَن، والثانية مدى صلاحيّة المبنيّ لأن تُبنى عليه الطبقةُ التالية،
والأبُ فيها لا يتجاوز أضعفَ أبنائه المُلزِمين.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Final

from .laws import (
    A_RATIO_CARRIES_ITS_DENOMINATOR,
    BREADTH_IS_NOT_READINESS,
    TAXONOMY_GRANULARITY_IS_NOT_CAPABILITY_IMPORTANCE,
)
from .maturity import GATE_SEQUENCE, MaturityStage
from .measure import LeafMeasurement
from .universe import CapabilityUniverse

__all__ = [
    "COVERAGE_GEOMETRY",
    "AggregationError",
    "DerivedRatio",
    "DomainCoverageProfile",
    "DomainCoverageRow",
    "NodeAggregate",
    "aggregate_universe",
    "derive_domain_coverage_profile",
]

COVERAGE_GEOMETRY: Final[str] = "LeafCoverage"
"""هندسةُ التغطية المُشتَقّة هنا: عدُّ الأوراق، مُسمًّى لا مضمرًا."""


class AggregationError(ValueError):
    """رفضٌ بنيويٌّ مُسمًّى في التجميع؛ لا نسبةَ تُخرَج من مقامٍ مجهول."""


@dataclass(frozen=True)
class DerivedRatio:
    """نسبةٌ مُشتَقّةٌ محمولةٌ ببسطها ومقامها ومصدرِ تجميد مقامها."""

    numerator: int
    denominator: int
    denominator_source: str

    def __post_init__(self) -> None:
        if type(self.numerator) is not int or type(self.denominator) is not int:
            raise AggregationError("a derived ratio counts, it does not estimate")
        if self.numerator < 0 or self.denominator < 0:
            raise AggregationError("a derived ratio has no negative side")
        if self.numerator > self.denominator:
            raise AggregationError("a numerator cannot exceed its own denominator")
        if (
            type(self.denominator_source) is not str
            or not self.denominator_source.strip()
        ):
            raise AggregationError(
                "a derived ratio names the source of its denominator"
            )

    @property
    def value(self) -> float | None:
        """القيمةُ العشريّة، أو `None` حين يكون المقامُ صفرًا؛ لا صفرَ مُوهِم."""

        if self.denominator == 0:
            return None
        return self.numerator / self.denominator

    @property
    def reading_law(self) -> str:
        """سقفُ قراءة النسبة، محمولًا معها لا مفصولًا عنها."""

        return A_RATIO_CARRIES_ITS_DENOMINATOR

    def as_canonical_content(self) -> dict[str, object]:
        """المحتوى القانونيّ للنسبة."""

        return {
            "numerator": self.numerator,
            "denominator": self.denominator,
            "denominator_source": self.denominator_source,
            "value": self.value,
        }


@dataclass(frozen=True)
class NodeAggregate:
    """تجميعُ عقدةٍ على أوراقها: تغطيةٌ عند كلّ بوّابة، وأهليّةٌ مسقوفةٌ بأبنائها."""

    node_id: str
    leaf_total: int
    stage_counts: Mapping[MaturityStage, int]
    coverage: Mapping[MaturityStage, DerivedRatio]
    own_readiness: DerivedRatio
    readiness: DerivedRatio
    certified_completion: DerivedRatio
    blocking_leaf_ids: tuple[str, ...]

    @property
    def breadth_law(self) -> str:
        """التغطيةُ ليست أهليّةً؛ القانونُ محمولٌ مع التجميع."""

        return BREADTH_IS_NOT_READINESS

    @property
    def coverage_geometry(self) -> str:
        """هندسةُ هذه التغطية: عدُّ الأوراق، مُسمّاةً كي لا تُقرأ مقدارَ العربية."""

        return COVERAGE_GEOMETRY

    @property
    def granularity_law(self) -> str:
        """سقفُ قراءة عدّ الأوراق، محمولًا مع التجميع لا مفصولًا عنه."""

        return TAXONOMY_GRANULARITY_IS_NOT_CAPABILITY_IMPORTANCE

    def as_canonical_content(self) -> dict[str, object]:
        """المحتوى القانونيّ للتجميع."""

        return {
            "node_id": self.node_id,
            "leaf_total": self.leaf_total,
            "coverage_geometry": self.coverage_geometry,
            "stage_counts": {
                stage.value: self.stage_counts[stage] for stage in GATE_SEQUENCE
            },
            "coverage": {
                stage.value: self.coverage[stage].as_canonical_content()
                for stage in GATE_SEQUENCE[1:]
            },
            "own_readiness": self.own_readiness.as_canonical_content(),
            "readiness": self.readiness.as_canonical_content(),
            "certified_completion": self.certified_completion.as_canonical_content(),
            "blocking_leaf_ids": list(self.blocking_leaf_ids),
        }


def _ratio(numerator: int, denominator: int, source: str) -> DerivedRatio:
    return DerivedRatio(
        numerator=numerator, denominator=denominator, denominator_source=source
    )


def aggregate_universe(
    universe: CapabilityUniverse, measurements: Mapping[str, LeafMeasurement]
) -> dict[str, NodeAggregate]:
    """جمِّع المقامَ كلَّه صاعدًا من الأوراق، بالأب مسقوفًا بأبنائه المُلزِمين."""

    missing = set(universe.leaf_ids()) - set(measurements)
    if missing:
        raise AggregationError(
            f"every declared leaf is measured, including absent ones: {sorted(missing)}"
        )
    source = universe.manifest.universe_id
    own: dict[str, DerivedRatio] = {}
    aggregates: dict[str, NodeAggregate] = {}
    for node_id in universe.node_ids():
        leaves = universe.leaf_ids(node_id)
        rows = [measurements[leaf_id] for leaf_id in leaves]
        total = len(rows)
        stage_counts = {
            stage: sum(1 for row in rows if row.attained_stage is stage)
            for stage in GATE_SEQUENCE
        }
        coverage = {
            stage: _ratio(
                sum(
                    1
                    for row in rows
                    if row.attained_stage.gate_index >= stage.gate_index
                ),
                total,
                source,
            )
            for stage in GATE_SEQUENCE[1:]
        }
        own[node_id] = _ratio(sum(1 for row in rows if row.is_ready), total, source)
        certified = _ratio(
            sum(
                1
                for row in rows
                if row.attained_stage.gate_index
                >= MaturityStage.S7_BLIND_VERIFIED.gate_index
                and not row.residuals
            ),
            total,
            source,
        )
        aggregates[node_id] = NodeAggregate(
            node_id=node_id,
            leaf_total=total,
            stage_counts=stage_counts,
            coverage=coverage,
            own_readiness=own[node_id],
            readiness=own[node_id],
            certified_completion=certified,
            blocking_leaf_ids=tuple(
                row.capability_id for row in rows if not row.is_ready
            ),
        )
    return _cap_readiness_by_required_children(universe, aggregates)


def _cap_readiness_by_required_children(
    universe: CapabilityUniverse, aggregates: dict[str, NodeAggregate]
) -> dict[str, NodeAggregate]:
    """اسقُف أهليّةَ كلّ أبٍ بأضعف أبنائه المُلزِمين، صاعدًا من الأوراق."""

    order = sorted(
        universe.node_ids(),
        key=lambda node_id: len(universe.descendants(node_id)),
    )
    capped = dict(aggregates)
    for node_id in order:
        required = universe.required_children(node_id)
        if not required:
            continue
        current = capped[node_id]
        child_values = [
            capped[child].readiness
            for child in required
            if capped[child].readiness.value is not None
        ]
        if not child_values:
            continue
        weakest = min(child_values, key=lambda ratio: ratio.value or 0.0)
        own_value = current.own_readiness.value
        weakest_value = weakest.value or 0.0
        if own_value is not None and own_value <= weakest_value:
            continue
        capped[node_id] = NodeAggregate(
            node_id=current.node_id,
            leaf_total=current.leaf_total,
            stage_counts=current.stage_counts,
            coverage=current.coverage,
            own_readiness=current.own_readiness,
            readiness=weakest,
            certified_completion=current.certified_completion,
            blocking_leaf_ids=current.blocking_leaf_ids,
        )
    return capped


@dataclass(frozen=True)
class DomainCoverageRow:
    """صفُّ مجالٍ واحدٍ في اتّجاه المجالات: أوراقُه، وتغطيتُه، وأهليّتُه."""

    domain_id: str
    title: str
    leaf_total: int
    coverage: Mapping[MaturityStage, DerivedRatio]
    readiness: DerivedRatio

    def as_canonical_content(self) -> dict[str, object]:
        """المحتوى القانونيّ لصفّ المجال."""

        return {
            "domain_id": self.domain_id,
            "title": self.title,
            "leaf_total": self.leaf_total,
            "coverage": {
                stage.value: self.coverage[stage].as_canonical_content()
                for stage in GATE_SEQUENCE[1:]
            },
            "readiness": self.readiness.as_canonical_content(),
        }


@dataclass(frozen=True)
class DomainCoverageProfile:
    """اتّجاهُ المجالات السبعةَ عشرَ منفصلةً؛ لا رقمَ واحدٌ يُغني عن قراءتها.

    عرضُ المجالات صفًّا صفًّا هو البديلُ الأمين عن تسويتها في وسطٍ واحد: تسويةُ
    الأوزان هندسةُ قياسٍ أخرى لا حقيقةٌ مُشتَقّة، وعدُّ الأوراق وحدَه يجعل بابًا
    فصّلناه أكثرَ أثقلَ من بابٍ لم نفصّله
    (`TaxonomyGranularity != CapabilityImportance`).
    """

    rows: tuple[DomainCoverageRow, ...]

    def row(self, domain_id: str) -> DomainCoverageRow:
        """صفُّ مجالٍ بعينه؛ ومعرّفٌ غيرُ معلومٍ رفضٌ لا `None` صامت."""

        for row in self.rows:
            if row.domain_id == domain_id:
                return row
        raise AggregationError(f"«{domain_id}» is not a declared domain")

    @property
    def granularity_law(self) -> str:
        """سقفُ قراءة الاتّجاه، محمولًا معه لا مفصولًا عنه."""

        return TAXONOMY_GRANULARITY_IS_NOT_CAPABILITY_IMPORTANCE

    def as_canonical_content(self) -> dict[str, object]:
        """المحتوى القانونيّ لاتّجاه المجالات."""

        return {
            "coverage_geometry": COVERAGE_GEOMETRY,
            "rows": [row.as_canonical_content() for row in self.rows],
        }


def _natural_key(node_id: str) -> tuple[int, str]:
    """ترتيبُ عرضٍ طبيعيٌّ للمعرّفات المرقّمة؛ ترتيبُ قراءةٍ لا ترتيبُ أهمّيّة."""

    return (len(node_id), node_id)


def derive_domain_coverage_profile(
    universe: CapabilityUniverse, aggregates: Mapping[str, NodeAggregate]
) -> DomainCoverageProfile:
    """اعرض المجالات السبعةَ عشرَ منفصلةً بدل أن تُسوَّى في رقمٍ واحد."""

    rows = tuple(
        DomainCoverageRow(
            domain_id=domain_id,
            title=universe.node(domain_id).title,
            leaf_total=aggregates[domain_id].leaf_total,
            coverage=aggregates[domain_id].coverage,
            readiness=aggregates[domain_id].readiness,
        )
        for domain_id in sorted(universe.domain_ids(), key=_natural_key)
    )
    return DomainCoverageProfile(rows=rows)
