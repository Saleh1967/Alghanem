"""G0.1 question, specification, and evidence-binding contracts only."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .evidence_acquisition import AuthorizedEvidenceSnapshot
    from .experiment_spec_content_identity import (
        BirthExperimentSpecificationContentBinding,
    )

_BIRTH_EVALUATOR_DEFINITION_TOKEN = object()


class BirthExperimentSpecificationError(ValueError):
    """A malformed G0.1 contract cannot enter a future assessment runtime."""


class BirthAssessmentEvaluatorAuthorityError(BirthExperimentSpecificationError):
    """Caller-declared evaluator ids are not trusted evaluator authority."""


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


class ClosureAssessmentStatus(Enum):
    """Local closure outcome vocabulary for weaker-model evaluators, not verdicts."""

    CLOSE = auto()
    FAIL_TO_CLOSE = auto()
    DEFER = auto()


class BirthEvaluatorRole(Enum):
    """Evaluator-declaration roles that a future registry may authorize."""

    RESIDUAL_DEFINITION = auto()
    WEAKER_MODEL = auto()
    CLOSURE_CRITERION = auto()


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


def _require_text_tuple(
    values: tuple[str, ...], field_name: str, *, allow_empty: bool = False
) -> None:
    if not allow_empty and not values:
        raise BirthExperimentSpecificationError(f"{field_name} must not be empty")
    if not isinstance(values, tuple) or any(
        not isinstance(value, str) or not value.strip() for value in values
    ):
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

    def strict_successors(self, projection: str) -> tuple[str, ...]:
        """Derive the complete strict upper cone of a model."""

        if projection not in self.projections:
            raise BirthExperimentSpecificationError("unknown test model")
        successors = self._traverse(projection, reverse=False)
        return tuple(item for item in self.projections if item in successors)

    def incomparable_with(self, projection: str) -> tuple[str, ...]:
        """Derive models unrelated to a test model; they are not prerequisites."""

        if projection not in self.projections:
            raise BirthExperimentSpecificationError("unknown test model")
        predecessors = set(self.strict_predecessors(projection))
        successors = set(self.strict_successors(projection))
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
    residual_definition_id: str
    residual_definition: str
    closure_criterion_id: str
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
        _require_text(self.residual_definition_id, "residual definition id")
        _require_text(self.residual_definition, "residual definition")
        _require_text(self.closure_criterion_id, "closure criterion id")
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
class ResidualDefinitionSpec:
    """G0.2a contract for a residual definition; evaluator id is declarative."""

    residual_id: str
    domain: str
    input_projection: str
    output_schema: str
    evaluator_id: str
    invariants: tuple[str, ...]
    failure_semantics: str

    def __post_init__(self) -> None:
        _require_text(self.residual_id, "residual id")
        _require_text(self.domain, "residual domain")
        _require_text(self.input_projection, "residual input projection")
        _require_text(self.output_schema, "residual output schema")
        _require_text(self.evaluator_id, "residual evaluator id")
        _require_text_tuple(self.invariants, "residual invariants")
        _require_text(self.failure_semantics, "residual failure semantics")


@dataclass(frozen=True, slots=True)
class WeakerModelSpec:
    """G0.2a contract for one weaker model; evaluator id is declarative."""

    model_id: str
    domain: str
    projection_evaluator_id: str
    declared_information_loss: str
    result_schema: str
    strict_predecessors: tuple[str, ...]
    strict_successors: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_text(self.model_id, "weaker model id")
        _require_text(self.domain, "weaker model domain")
        _require_text(self.projection_evaluator_id, "weaker model evaluator id")
        _require_text(
            self.declared_information_loss, "weaker model declared information loss"
        )
        _require_text(self.result_schema, "weaker model result schema")
        _require_text_tuple(
            self.strict_predecessors,
            "weaker model strict predecessors",
            allow_empty=True,
        )
        _require_text_tuple(
            self.strict_successors,
            "weaker model strict successors",
            allow_empty=True,
        )


@dataclass(frozen=True, slots=True)
class ClosureCriterionSpec:
    """G0.2a contract for closure semantics; evaluator id is declarative."""

    criterion_id: str
    residual_id: str
    domain: str
    residual_schema: str
    model_result_schema: str
    evaluator_id: str
    failure_semantics: str

    def __post_init__(self) -> None:
        _require_text(self.criterion_id, "closure criterion id")
        _require_text(self.residual_id, "closure residual id")
        _require_text(self.domain, "closure domain")
        _require_text(self.residual_schema, "closure residual schema")
        _require_text(self.model_result_schema, "closure model result schema")
        _require_text(self.evaluator_id, "closure evaluator id")
        _require_text(self.failure_semantics, "closure failure semantics")

    @property
    def supported_statuses(self) -> tuple[ClosureAssessmentStatus, ...]:
        """The only local outcomes of ``Close(W_i, R)``."""

        return (
            ClosureAssessmentStatus.CLOSE,
            ClosureAssessmentStatus.FAIL_TO_CLOSE,
            ClosureAssessmentStatus.DEFER,
        )


@dataclass(frozen=True, slots=True)
class BirthAssessmentSemanticsContract:
    """G0.2a executable assessment contract; it issues no birth verdict."""

    specification: BirthExperimentSpecification
    residual_definition: ResidualDefinitionSpec
    weaker_models: tuple[WeakerModelSpec, ...]
    closure_criterion: ClosureCriterionSpec

    def __post_init__(self) -> None:
        if not isinstance(self.specification, BirthExperimentSpecification):
            raise BirthExperimentSpecificationError(
                "assessment semantics require a frozen experiment specification"
            )
        if not isinstance(self.residual_definition, ResidualDefinitionSpec):
            raise BirthExperimentSpecificationError(
                "assessment semantics require an executable residual definition"
            )
        if not isinstance(self.closure_criterion, ClosureCriterionSpec):
            raise BirthExperimentSpecificationError(
                "assessment semantics require an executable closure criterion"
            )
        if (
            self.residual_definition.residual_id
            != self.specification.residual_definition_id
        ):
            raise BirthExperimentSpecificationError(
                "residual definition id must match the frozen specification"
            )
        if self.residual_definition.domain != self.specification.domain:
            raise BirthExperimentSpecificationError(
                "residual definition domain must match the experiment domain"
            )
        if (
            self.residual_definition.input_projection
            != self.specification.birth_query.test_model
        ):
            raise BirthExperimentSpecificationError(
                "residual input projection must match the queried test model"
            )
        if self.closure_criterion.domain != self.specification.domain:
            raise BirthExperimentSpecificationError(
                "closure criterion domain must match the experiment domain"
            )
        if (
            self.closure_criterion.criterion_id
            != self.specification.closure_criterion_id
        ):
            raise BirthExperimentSpecificationError(
                "closure criterion id must match the frozen specification"
            )
        if self.closure_criterion.residual_id != self.residual_definition.residual_id:
            raise BirthExperimentSpecificationError(
                "closure criterion must target the declared residual"
            )
        if (
            self.closure_criterion.residual_schema
            != self.residual_definition.output_schema
        ):
            raise BirthExperimentSpecificationError(
                "closure criterion residual schema must match the residual output"
            )
        self._validate_weaker_models()

    def _validate_weaker_models(self) -> None:
        if not isinstance(self.weaker_models, tuple):
            raise BirthExperimentSpecificationError("weaker model specs must be frozen")
        if any(not isinstance(model, WeakerModelSpec) for model in self.weaker_models):
            raise BirthExperimentSpecificationError(
                "assessment semantics require executable weaker model specs"
            )
        model_ids = tuple(model.model_id for model in self.weaker_models)
        if model_ids != self.specification.frozen_weaker_models:
            raise BirthExperimentSpecificationError(
                "weaker model specs must exactly cover the frozen prerequisite cone"
            )
        schemas = {model.result_schema for model in self.weaker_models}
        if schemas != {self.closure_criterion.model_result_schema}:
            raise BirthExperimentSpecificationError(
                "weaker model result schemas must match the closure criterion"
            )
        for model in self.weaker_models:
            if model.domain != self.specification.domain:
                raise BirthExperimentSpecificationError(
                    "weaker model domains must match the experiment domain"
                )
            if (
                model.strict_predecessors
                != self.specification.projection_poset.strict_predecessors(
                    model.model_id
                )
            ):
                raise BirthExperimentSpecificationError(
                    "weaker model predecessor relation must match the projection poset"
                )
            if model.strict_successors != (
                self.specification.projection_poset.strict_successors(model.model_id)
            ):
                raise BirthExperimentSpecificationError(
                    "weaker model successor relation must match the projection poset"
                )


@dataclass(frozen=True, slots=True)
class AuthorizedBirthAssessmentEvaluatorDefinition:
    """Registry-issued evaluator authorization for an exact role and target."""

    domain: str
    role: BirthEvaluatorRole
    target_id: str
    evaluator_id: str
    version: str = "1"
    _authority_token: object = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._authority_token is not _BIRTH_EVALUATOR_DEFINITION_TOKEN:
            raise BirthAssessmentEvaluatorAuthorityError(
                "authorized evaluator definitions must be registry-issued"
            )
        _require_text(self.domain, "authorized evaluator domain")
        if not isinstance(self.role, BirthEvaluatorRole):
            raise BirthAssessmentEvaluatorAuthorityError(
                "authorized evaluator role must be declared"
            )
        _require_text(self.target_id, "authorized evaluator target id")
        _require_text(self.evaluator_id, "authorized evaluator id")
        _require_text(self.version, "authorized evaluator version")


@dataclass(frozen=True, slots=True)
class SealedBirthAssessmentEvaluatorRegistry:
    """Frozen registry snapshot; it authorizes declarations but executes nothing."""

    snapshot_id: str
    definitions: tuple[AuthorizedBirthAssessmentEvaluatorDefinition, ...]
    _registry_token: object = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._registry_token is not _BIRTH_EVALUATOR_DEFINITION_TOKEN:
            raise BirthAssessmentEvaluatorAuthorityError(
                "sealed evaluator registries must be registry-issued"
            )
        _require_text(self.snapshot_id, "evaluator registry snapshot id")
        if not isinstance(self.definitions, tuple):
            raise BirthAssessmentEvaluatorAuthorityError(
                "evaluator registry definitions must be frozen"
            )
        seen: set[tuple[str, BirthEvaluatorRole, str, str]] = set()
        for definition in self.definitions:
            if not isinstance(definition, AuthorizedBirthAssessmentEvaluatorDefinition):
                raise BirthAssessmentEvaluatorAuthorityError(
                    "sealed registry requires authorized evaluator definitions"
                )
            key = (
                definition.domain,
                definition.role,
                definition.target_id,
                definition.evaluator_id,
            )
            if key in seen:
                raise BirthAssessmentEvaluatorAuthorityError(
                    "sealed registry must not contain duplicate definitions"
                )
            seen.add(key)

    def resolve_authorized(
        self,
        *,
        domain: str,
        role: BirthEvaluatorRole,
        target_id: str,
        evaluator_id: str,
    ) -> AuthorizedBirthAssessmentEvaluatorDefinition:
        """Return a registry-issued authorization for an exact declaration."""

        for definition in self.definitions:
            if (
                definition.domain == domain
                and definition.role is role
                and definition.target_id == target_id
                and definition.evaluator_id == evaluator_id
            ):
                return definition
        raise BirthAssessmentEvaluatorAuthorityError(
            "declared evaluator id is not authorized for this scope"
        )


class BirthAssessmentEvaluatorRegistry:
    """Authority boundary for evaluator definitions; it performs no assessment."""

    def __init__(self) -> None:
        self._definitions: dict[
            tuple[str, BirthEvaluatorRole, str, str],
            AuthorizedBirthAssessmentEvaluatorDefinition,
        ] = {}

    def authorize(
        self,
        *,
        domain: str,
        role: BirthEvaluatorRole,
        target_id: str,
        evaluator_id: str,
        version: str = "1",
    ) -> AuthorizedBirthAssessmentEvaluatorDefinition:
        """Authorize a declared evaluator id for one exact role and target."""

        definition = AuthorizedBirthAssessmentEvaluatorDefinition(
            domain=domain,
            role=role,
            target_id=target_id,
            evaluator_id=evaluator_id,
            version=version,
            _authority_token=_BIRTH_EVALUATOR_DEFINITION_TOKEN,
        )
        key = (domain, role, target_id, evaluator_id)
        self._definitions[key] = definition
        return definition

    def seal(self, snapshot_id: str) -> SealedBirthAssessmentEvaluatorRegistry:
        """Freeze the authorized evaluator definitions without adding execution."""

        return SealedBirthAssessmentEvaluatorRegistry(
            snapshot_id=snapshot_id,
            definitions=tuple(self._definitions.values()),
            _registry_token=_BIRTH_EVALUATOR_DEFINITION_TOKEN,
        )


@dataclass(frozen=True, slots=True)
class BirthAssessmentEvaluatorDefinitions:
    """Registry-authorized evaluator definitions for a semantics contract."""

    contract: BirthAssessmentSemanticsContract
    registry_snapshot: SealedBirthAssessmentEvaluatorRegistry
    residual_definition: AuthorizedBirthAssessmentEvaluatorDefinition = field(
        init=False
    )
    weaker_models: tuple[AuthorizedBirthAssessmentEvaluatorDefinition, ...] = field(
        init=False
    )
    closure_criterion: AuthorizedBirthAssessmentEvaluatorDefinition = field(init=False)

    def __post_init__(self) -> None:
        if not isinstance(self.contract, BirthAssessmentSemanticsContract):
            raise BirthAssessmentEvaluatorAuthorityError(
                "evaluator definitions require a birth assessment semantics contract"
            )
        if not isinstance(
            self.registry_snapshot, SealedBirthAssessmentEvaluatorRegistry
        ):
            raise BirthAssessmentEvaluatorAuthorityError(
                "evaluator definitions require a sealed evaluator registry"
            )
        object.__setattr__(
            self,
            "residual_definition",
            self.registry_snapshot.resolve_authorized(
                domain=self.contract.specification.domain,
                role=BirthEvaluatorRole.RESIDUAL_DEFINITION,
                target_id=self.contract.residual_definition.residual_id,
                evaluator_id=self.contract.residual_definition.evaluator_id,
            ),
        )
        object.__setattr__(
            self,
            "weaker_models",
            tuple(
                self.registry_snapshot.resolve_authorized(
                    domain=self.contract.specification.domain,
                    role=BirthEvaluatorRole.WEAKER_MODEL,
                    target_id=model.model_id,
                    evaluator_id=model.projection_evaluator_id,
                )
                for model in self.contract.weaker_models
            ),
        )
        object.__setattr__(
            self,
            "closure_criterion",
            self.registry_snapshot.resolve_authorized(
                domain=self.contract.specification.domain,
                role=BirthEvaluatorRole.CLOSURE_CRITERION,
                target_id=self.contract.closure_criterion.criterion_id,
                evaluator_id=self.contract.closure_criterion.evaluator_id,
            ),
        )


@dataclass(frozen=True, slots=True)
class EvidenceSnapshot:
    """Deprecated: a bare, unauthorized evidence description.

    This type carries no acquisition provenance and cannot prove that its
    content was ingested under any frozen experiment. It is retained only for
    historical reference and is no longer accepted by `BirthAssessmentRequest`;
    use `evidence_acquisition.AuthorizedEvidenceSnapshot` instead, which is
    issuer-only and bound to an `EvidenceAcquisitionAuthorization`.
    """

    snapshot_id: str
    description: str

    def __post_init__(self) -> None:
        _require_text(self.snapshot_id, "evidence snapshot id")
        _require_text(self.description, "evidence snapshot description")


@dataclass(frozen=True, slots=True)
class BirthAssessmentRequest:
    """A valid request for G0.2; it is not an assessment or a verdict."""

    experiment_binding: BirthExperimentSpecificationContentBinding
    evidence_snapshot: AuthorizedEvidenceSnapshot

    def __post_init__(self) -> None:
        from .evidence_acquisition import AuthorizedEvidenceSnapshot
        from .experiment_spec_content_identity import (
            BirthExperimentSpecificationContentBinding,
        )

        if (
            type(self.experiment_binding)
            is not BirthExperimentSpecificationContentBinding
        ):
            raise BirthExperimentSpecificationError(
                "assessment request requires an authorized frozen experiment binding"
            )
        if type(self.evidence_snapshot) is not AuthorizedEvidenceSnapshot:
            raise BirthExperimentSpecificationError(
                "assessment request requires an authorized evidence snapshot issued "
                "by an evidence acquisition run"
            )
        if (
            self.evidence_snapshot.experiment_content_id
            != self.experiment_binding.content_id
        ):
            raise BirthExperimentSpecificationError(
                "evidence snapshot was not acquired under this frozen experiment"
            )

    @property
    def specification(self) -> BirthExperimentSpecification:
        """The specification proven equal to the authorized frozen manifest."""

        return self.experiment_binding.specification
