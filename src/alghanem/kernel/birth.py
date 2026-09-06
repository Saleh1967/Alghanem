"""G0.1 birth-experiment contracts, without a birth-assessment runtime."""

from dataclasses import dataclass
from enum import Enum, auto


class BirthExperimentSpecificationError(ValueError):
    """A malformed experiment specification cannot produce a verdict."""


class EvidenceMode(Enum):
    """The independent evidence mode declared before an assessment."""

    FORMAL = auto()
    EMPIRICAL = auto()
    MIXED = auto()


class BirthVerdictStatus(Enum):
    """Scoped epistemic outcomes for a structurally valid assessment."""

    BIRTH_IN_SCOPE = auto()
    NO_BIRTH_IN_SCOPE = auto()
    DEFER_IN_SCOPE = auto()


def _require_text(value: str, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise BirthExperimentSpecificationError(f"{field} must be non-blank")


def _require_unique(values: tuple[str, ...], field: str) -> None:
    if not values:
        raise BirthExperimentSpecificationError(f"{field} must not be empty")
    if any(not isinstance(value, str) or not value.strip() for value in values):
        raise BirthExperimentSpecificationError(
            f"{field} must contain non-blank values"
        )
    if len(set(values)) != len(values):
        raise BirthExperimentSpecificationError(f"{field} must not contain duplicates")


@dataclass(frozen=True, slots=True)
class BirthQuery:
    """A pre-evidence question about whether a projection is necessary."""

    query_id: str
    statement: str
    target_projection: str

    def __post_init__(self) -> None:
        _require_text(self.query_id, "query id")
        _require_text(self.statement, "query statement")
        _require_text(self.target_projection, "query target projection")


@dataclass(frozen=True, slots=True)
class ProjectionPoset:
    """A frozen partial order, with pairs ordered as ``(lower, richer)``."""

    projections: tuple[str, ...]
    strict_relations: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        _require_unique(self.projections, "projections")
        seen: set[tuple[str, str]] = set()
        for lower, richer in self.strict_relations:
            if lower not in self.projections or richer not in self.projections:
                raise BirthExperimentSpecificationError(
                    "projection relations must reference declared projections"
                )
            if lower == richer:
                raise BirthExperimentSpecificationError(
                    "projection relations must be strict"
                )
            if (lower, richer) in seen:
                raise BirthExperimentSpecificationError(
                    "projection relations must not contain duplicates"
                )
            seen.add((lower, richer))
        for projection in self.projections:
            if projection in self.strict_predecessors(projection):
                raise BirthExperimentSpecificationError(
                    "projection relations must not contain cycles"
                )

    def strict_predecessors(self, projection: str) -> tuple[str, ...]:
        """Derive the complete strict lower cone of ``projection``."""

        if projection not in self.projections:
            raise BirthExperimentSpecificationError("unknown target projection")
        predecessors: set[str] = set()
        frontier = [projection]
        while frontier:
            richer = frontier.pop()
            for lower, relation_richer in self.strict_relations:
                if relation_richer == richer and lower not in predecessors:
                    predecessors.add(lower)
                    frontier.append(lower)
        return tuple(item for item in self.projections if item in predecessors)

    def incomparable_with(self, projection: str) -> tuple[str, ...]:
        """Derive projections unrelated to ``projection`` in this poset."""

        if projection not in self.projections:
            raise BirthExperimentSpecificationError("unknown target projection")
        predecessors = set(self.strict_predecessors(projection))
        successors = self._strict_successors(projection)
        return tuple(
            candidate
            for candidate in self.projections
            if candidate not in predecessors | successors | {projection}
        )

    def _strict_successors(self, projection: str) -> set[str]:
        successors: set[str] = set()
        frontier = [projection]
        while frontier:
            lower = frontier.pop()
            for relation_lower, richer in self.strict_relations:
                if relation_lower == lower and richer not in successors:
                    successors.add(richer)
                    frontier.append(richer)
        return successors


@dataclass(frozen=True, slots=True)
class BirthExperimentSpecification:
    """The complete pre-evidence contract for one frozen birth experiment."""

    experiment_id: str
    revision_id: str
    evidence_mode: EvidenceMode
    domain: str
    projection_poset: ProjectionPoset
    birth_query: BirthQuery
    frozen_weaker_models: tuple[str, ...]
    residual_definition: str
    closure_criterion: str
    evidence_requirements: str

    def __post_init__(self) -> None:
        _require_text(self.experiment_id, "experiment id")
        _require_text(self.revision_id, "revision id")
        _require_text(self.domain, "domain")
        _require_text(self.residual_definition, "residual definition")
        _require_text(self.closure_criterion, "closure criterion")
        _require_text(self.evidence_requirements, "evidence requirements")
        if not isinstance(self.evidence_mode, EvidenceMode):
            raise BirthExperimentSpecificationError("evidence mode must be declared")
        if self.birth_query.target_projection not in self.projection_poset.projections:
            raise BirthExperimentSpecificationError(
                "birth query target must be declared by the projection poset"
            )
        expected = self.prerequisite_cone
        if set(self.frozen_weaker_models) != set(expected) or len(
            self.frozen_weaker_models
        ) != len(expected):
            raise BirthExperimentSpecificationError(
                "frozen weaker models must exactly equal the derived prerequisite cone"
            )

    @property
    def prerequisite_cone(self) -> tuple[str, ...]:
        """The derived ``Down_E(q)``; callers cannot select it independently."""

        return self.projection_poset.strict_predecessors(
            self.birth_query.target_projection
        )

    @property
    def competing_projections(self) -> tuple[str, ...]:
        """Potentially relevant incomparable explanations, not prerequisites."""

        return self.projection_poset.incomparable_with(
            self.birth_query.target_projection
        )


@dataclass(frozen=True, slots=True)
class EvidenceSnapshot:
    """Evidence bound only after the experiment specification is frozen."""

    snapshot_id: str
    description: str

    def __post_init__(self) -> None:
        _require_text(self.snapshot_id, "evidence snapshot id")
        _require_text(self.description, "evidence snapshot description")


@dataclass(frozen=True, slots=True)
class BirthAssessmentRequest:
    """A later assessment request binding frozen terms to actual evidence."""

    specification: BirthExperimentSpecification
    evidence_snapshot: EvidenceSnapshot


@dataclass(frozen=True, slots=True)
class CompetingExplanation:
    """An incomparable projection that may close the residual instead."""

    projection: str
    explanation: str

    def __post_init__(self) -> None:
        _require_text(self.projection, "competing projection")
        _require_text(self.explanation, "competing explanation")


@dataclass(frozen=True, slots=True)
class BirthVerdict:
    """A scoped result; issuing one is deferred to a future assessment gate."""

    request: BirthAssessmentRequest
    status: BirthVerdictStatus
    reason: str
    competing_explanations: tuple[CompetingExplanation, ...] = ()
    discriminating_evidence: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_text(self.reason, "verdict reason")
        if not isinstance(self.status, BirthVerdictStatus):
            raise ValueError("birth verdict requires a scoped verdict status")
        competing = set(self.request.specification.competing_projections)
        if any(
            item.projection not in competing for item in self.competing_explanations
        ):
            raise ValueError(
                "competing explanations must use projections incomparable "
                "with the query"
            )
        if self.status is BirthVerdictStatus.BIRTH_IN_SCOPE and (
            self.competing_explanations and not self.discriminating_evidence
        ):
            raise ValueError(
                "birth with competing explanations requires discriminating evidence"
            )


@dataclass(frozen=True, slots=True)
class BirthFreeze:
    """A frozen birth verdict, permitted only after ``BIRTH_IN_SCOPE``."""

    verdict: BirthVerdict
    e0_id: str

    def __post_init__(self) -> None:
        if self.verdict.status is not BirthVerdictStatus.BIRTH_IN_SCOPE:
            raise ValueError("only BIRTH_IN_SCOPE may be frozen")
        _require_text(self.e0_id, "E0 id")


@dataclass(frozen=True, slots=True)
class BirthRevisionHistory:
    """Preserves historical scoped verdicts while selecting the active one."""

    verdicts: tuple[BirthVerdict, ...]
    active_revision_id: str

    def __post_init__(self) -> None:
        if not self.verdicts:
            raise ValueError("revision history requires at least one verdict")
        _require_text(self.active_revision_id, "active revision id")
        first = self.verdicts[0].request.specification
        revisions: set[str] = set()
        for verdict in self.verdicts:
            specification = verdict.request.specification
            if (
                specification.experiment_id != first.experiment_id
                or specification.birth_query.query_id != first.birth_query.query_id
            ):
                raise ValueError(
                    "revision history must retain one experiment and birth query"
                )
            if specification.revision_id in revisions:
                raise ValueError("revision history must not duplicate revisions")
            revisions.add(specification.revision_id)
        latest_revision = self.verdicts[-1].request.specification.revision_id
        if self.active_revision_id != latest_revision:
            raise ValueError("only the latest recorded revision may be active")
