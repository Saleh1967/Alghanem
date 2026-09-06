"""G0.1 question, specification, and evidence-binding contracts only."""

from dataclasses import dataclass, field
from enum import Enum, auto


class BirthExperimentSpecificationError(ValueError):
    """A malformed G0.1 contract cannot enter a future assessment runtime."""


class EvidenceMode(Enum):
    """The independent evidence mode declared before an assessment."""

    FORMAL = auto()
    EMPIRICAL = auto()
    MIXED = auto()


class BirthVerdictStatus(Enum):
    """Future scoped verdict vocabulary; values confer no decision authority."""

    BIRTH_IN_SCOPE = auto()
    NO_BIRTH_IN_SCOPE = auto()
    DEFER_IN_SCOPE = auto()


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise BirthExperimentSpecificationError(f"{field_name} must be non-blank")


def _require_unique(values: tuple[str, ...], field_name: str) -> None:
    if not values:
        raise BirthExperimentSpecificationError(f"{field_name} must not be empty")
    if any(not isinstance(value, str) or not value.strip() for value in values):
        raise BirthExperimentSpecificationError(
            f"{field_name} must contain non-blank values"
        )
    if len(set(values)) != len(values):
        raise BirthExperimentSpecificationError(
            f"{field_name} must not contain duplicates"
        )


@dataclass(frozen=True, slots=True)
class StructureHypothesis:
    """A proposed structure, distinct from the analytical models used to test it."""

    hypothesis_id: str
    statement: str

    def __post_init__(self) -> None:
        _require_text(self.hypothesis_id, "hypothesis id")
        _require_text(self.statement, "hypothesis statement")


@dataclass(frozen=True, slots=True)
class BirthQuery:
    """A pre-evidence question testing one model against a structure hypothesis."""

    query_id: str
    hypothesis: StructureHypothesis
    test_model: str

    def __post_init__(self) -> None:
        _require_text(self.query_id, "query id")
        if not isinstance(self.hypothesis, StructureHypothesis):
            raise BirthExperimentSpecificationError(
                "birth query requires a structure hypothesis"
            )
        _require_text(self.test_model, "query test model")


@dataclass(frozen=True, slots=True)
class ProjectionPoset:
    """A frozen partial order of analytical models, ordered ``(lower, richer)``."""

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
        """Derive the complete strict lower cone of a test model."""

        if projection not in self.projections:
            raise BirthExperimentSpecificationError("unknown test model")
        predecessors = self._traverse(projection, reverse=True)
        return tuple(item for item in self.projections if item in predecessors)

    def incomparable_with(self, projection: str) -> tuple[str, ...]:
        """Derive models unrelated to a test model; they are not prerequisites."""

        if projection not in self.projections:
            raise BirthExperimentSpecificationError("unknown test model")
        predecessors = set(self.strict_predecessors(projection))
        successors = self._traverse(projection, reverse=False)
        return tuple(
            candidate
            for candidate in self.projections
            if candidate not in predecessors | successors | {projection}
        )

    def _traverse(self, projection: str, *, reverse: bool) -> set[str]:
        related: set[str] = set()
        frontier = [projection]
        while frontier:
            current = frontier.pop()
            for lower, richer in self.strict_relations:
                source, target = (richer, lower) if reverse else (lower, richer)
                if source == current and target not in related:
                    related.add(target)
                    frontier.append(target)
        return related


@dataclass(frozen=True, slots=True)
class BirthExperimentSpecification:
    """The frozen, pre-evidence G0.1 contract for one experiment revision."""

    experiment_id: str
    revision_id: str
    revision_sequence: int
    evidence_mode: EvidenceMode
    domain: str
    projection_poset: ProjectionPoset
    birth_query: BirthQuery
    residual_definition: str
    closure_criterion: str
    evidence_requirements: str
    _prerequisite_cone: tuple[str, ...] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        _require_text(self.experiment_id, "experiment id")
        _require_text(self.revision_id, "revision id")
        if (
            not isinstance(self.revision_sequence, int)
            or isinstance(self.revision_sequence, bool)
            or self.revision_sequence < 1
        ):
            raise BirthExperimentSpecificationError(
                "revision sequence must be a positive integer"
            )
        _require_text(self.domain, "domain")
        _require_text(self.residual_definition, "residual definition")
        _require_text(self.closure_criterion, "closure criterion")
        _require_text(self.evidence_requirements, "evidence requirements")
        if not isinstance(self.evidence_mode, EvidenceMode):
            raise BirthExperimentSpecificationError("evidence mode must be declared")
        if not isinstance(self.projection_poset, ProjectionPoset):
            raise BirthExperimentSpecificationError("projection poset must be declared")
        if not isinstance(self.birth_query, BirthQuery):
            raise BirthExperimentSpecificationError("birth query must be declared")
        if self.birth_query.test_model not in self.projection_poset.projections:
            raise BirthExperimentSpecificationError(
                "birth query test model must be declared by the projection poset"
            )
        object.__setattr__(
            self,
            "_prerequisite_cone",
            self.projection_poset.strict_predecessors(self.birth_query.test_model),
        )

    @property
    def prerequisite_cone(self) -> tuple[str, ...]:
        """The derived ``Down_E(q)``; callers cannot select it independently."""

        return self._prerequisite_cone

    @property
    def frozen_weaker_models(self) -> tuple[str, ...]:
        """The frozen model-set role of the derived query-relative cone."""

        return self.prerequisite_cone

    @property
    def competing_projections(self) -> tuple[str, ...]:
        """Potential competing models for G0.2 to assess, not caller selections."""

        return self.projection_poset.incomparable_with(self.birth_query.test_model)


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
    """A valid request for G0.2; it is not an assessment or a verdict."""

    specification: BirthExperimentSpecification
    evidence_snapshot: EvidenceSnapshot

    def __post_init__(self) -> None:
        if not isinstance(self.specification, BirthExperimentSpecification):
            raise BirthExperimentSpecificationError(
                "assessment request requires a frozen experiment specification"
            )
        if not isinstance(self.evidence_snapshot, EvidenceSnapshot):
            raise BirthExperimentSpecificationError(
                "assessment request requires an evidence snapshot"
            )
