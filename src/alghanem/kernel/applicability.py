"""G0.EA.1 applicability assessment over an evidence-role candidate."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from dataclasses import InitVar, dataclass, field
from enum import Enum
from threading import Lock

from .claim_constitution import ClaimScopeRef
from .evidence_role import EvidenceRoleCandidate
from .residual import Residual
from .trace import Trace

_ASSESSMENT_TOKEN = object()
_BINDING_TOKEN = object()
_REGISTRY_TOKEN = object()


class ApplicabilityAssessmentStatus(Enum):
    PASS = "pass"
    BLOCK = "block"
    DEFER = "defer"


@dataclass(frozen=True, slots=True)
class ApplicabilityModelResult:
    """One authorized model's auditable closure result."""

    status: ApplicabilityAssessmentStatus
    reason: str
    trace: Trace
    residuals: tuple[Residual, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.status, ApplicabilityAssessmentStatus):
            raise TypeError("applicability model result requires a status")
        if type(self.reason) is not str or not self.reason.strip():
            raise ValueError("applicability model results require a reason")
        if type(self.trace) is not Trace:
            raise TypeError("applicability model results require a trace")
        if type(self.residuals) is not tuple or any(
            type(item) is not Residual for item in self.residuals
        ):
            raise TypeError("applicability residuals must be a tuple of residuals")
        if self.status is ApplicabilityAssessmentStatus.PASS and self.residuals:
            raise ValueError("PASS applicability results cannot retain residuals")
        if self.status is ApplicabilityAssessmentStatus.DEFER and not self.residuals:
            raise ValueError("DEFER applicability results require residuals")


ApplicabilityEvaluator = Callable[
    [EvidenceRoleCandidate], ApplicabilityModelResult
]


@dataclass(frozen=True, slots=True, init=False)
class AuthorizedApplicabilityEvaluatorBinding:
    """Authority-issued evaluator bound to one role and claim scope."""

    evaluator_id: str
    implementation_identity: str
    role_identifier: str
    scope: ClaimScopeRef
    evaluator: ApplicabilityEvaluator = field(repr=False, compare=False)

    def __init__(
        self,
        evaluator_id: str,
        implementation_identity: str,
        role_identifier: str,
        scope: ClaimScopeRef,
        evaluator: ApplicabilityEvaluator,
        *,
        _token: object | None = None,
    ) -> None:
        if _token is not _BINDING_TOKEN:
            raise ValueError(
                "applicability evaluator bindings must be issued by the registry"
            )
        for value, name in (
            (evaluator_id, "evaluator id"),
            (implementation_identity, "evaluator implementation identity"),
            (role_identifier, "role identifier"),
        ):
            if type(value) is not str or not value.strip():
                raise ValueError(f"{name} must be non-blank text")
        if type(scope) is not ClaimScopeRef or not callable(evaluator):
            raise TypeError("applicability evaluator binding has invalid coordinates")
        object.__setattr__(self, "evaluator_id", evaluator_id)
        object.__setattr__(self, "implementation_identity", implementation_identity)
        object.__setattr__(self, "role_identifier", role_identifier)
        object.__setattr__(self, "scope", scope)
        object.__setattr__(self, "evaluator", evaluator)


class ApplicabilityEvaluatorRegistry:
    """Authority that issues and seals content-bound evaluator bindings."""

    def __init__(self) -> None:
        self._definitions: dict[str, AuthorizedApplicabilityEvaluatorBinding] = {}
        self._lock = Lock()

    def register(
        self,
        evaluator_id: str,
        implementation_identity: str,
        role_identifier: str,
        scope: ClaimScopeRef,
        evaluator: ApplicabilityEvaluator,
    ) -> None:
        binding = AuthorizedApplicabilityEvaluatorBinding(
            evaluator_id,
            implementation_identity,
            role_identifier,
            scope,
            evaluator,
            _token=_BINDING_TOKEN,
        )
        with self._lock:
            if evaluator_id in self._definitions:
                raise ValueError("applicability evaluator ids must be unique")
            self._definitions[evaluator_id] = binding

    def seal(self, snapshot_id: str) -> SealedApplicabilityEvaluatorRegistry:
        if type(snapshot_id) is not str or not snapshot_id.strip():
            raise ValueError("applicability registry snapshot id must be text")
        with self._lock:
            bindings = tuple(self._definitions.values())
        return SealedApplicabilityEvaluatorRegistry(
            snapshot_id,
            bindings,
            _registry_token=_REGISTRY_TOKEN,
        )


@dataclass(frozen=True, slots=True)
class SealedApplicabilityEvaluatorRegistry:
    snapshot_id: str
    bindings: tuple[AuthorizedApplicabilityEvaluatorBinding, ...]
    registry_projection_hash: str = field(init=False)
    _registry_token: InitVar[object | None] = field(default=None, repr=False)

    def __post_init__(self, _registry_token: object | None) -> None:
        if _registry_token is not _REGISTRY_TOKEN:
            raise ValueError(
                "sealed applicability registries must be issued by the registry"
            )
        if not self.snapshot_id.strip() or any(
            type(item) is not AuthorizedApplicabilityEvaluatorBinding
            for item in self.bindings
        ):
            raise ValueError("invalid sealed applicability registry")
        projection = json.dumps(
            [
                {
                    "evaluator_id": item.evaluator_id,
                    "implementation_identity": item.implementation_identity,
                    "role_identifier": item.role_identifier,
                    "scope": {
                        "reference": item.scope.reference,
                        "scope_type": item.scope.scope_type,
                    },
                }
                for item in sorted(self.bindings, key=lambda item: item.evaluator_id)
            ],
            separators=(",", ":"),
            sort_keys=True,
        ).encode()
        object.__setattr__(
            self, "registry_projection_hash", hashlib.sha256(projection).hexdigest()
        )

    def resolve(self, evaluator_id: str) -> AuthorizedApplicabilityEvaluatorBinding:
        for binding in self.bindings:
            if binding.evaluator_id == evaluator_id:
                return binding
        raise KeyError(f"unknown applicability evaluator: {evaluator_id}")


@dataclass(frozen=True, slots=True)
class FrozenApplicabilityModel:
    """A content-bound model and its explicitly weaker models."""

    model_id: str
    evaluator_id: str
    weaker_model_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for value, name in (
            (self.model_id, "model id"),
            (self.evaluator_id, "evaluator id"),
        ):
            if type(value) is not str or not value.strip():
                raise ValueError(f"applicability {name} must be non-blank text")
        if type(self.weaker_model_ids) is not tuple or any(
            type(item) is not str or not item.strip()
            for item in self.weaker_model_ids
        ):
            raise TypeError("weaker applicability model ids must be text")
        if self.model_id in self.weaker_model_ids:
            raise ValueError("an applicability model cannot be weaker than itself")


@dataclass(frozen=True, slots=True)
class ApplicabilityAssessmentSpecification:
    """A frozen model family with a canonical content identity."""

    models: tuple[FrozenApplicabilityModel, ...]
    specification_id: str = field(init=False)

    def __post_init__(self) -> None:
        if type(self.models) is not tuple or not self.models:
            raise ValueError("applicability specifications require frozen models")
        if any(type(item) is not FrozenApplicabilityModel for item in self.models):
            raise TypeError("applicability specifications require frozen models")
        ids = tuple(item.model_id for item in self.models)
        if len(set(ids)) != len(ids):
            raise ValueError("applicability models cannot duplicate identifiers")
        known = set(ids)
        if any(not set(item.weaker_model_ids) <= known for item in self.models):
            raise ValueError("applicability models reference an unknown weaker model")
        if _has_cycle(self.models):
            raise ValueError("applicability model weakening must be acyclic")
        encoded = json.dumps(
            [
                {
                    "evaluator_id": item.evaluator_id,
                    "model_id": item.model_id,
                    "weaker_model_ids": item.weaker_model_ids,
                }
                for item in self.models
            ],
            separators=(",", ":"),
            sort_keys=True,
        ).encode()
        object.__setattr__(
            self, "specification_id", hashlib.sha256(encoded).hexdigest()
        )


@dataclass(frozen=True, slots=True)
class EvidenceApplicabilityAssessment:
    """The gate-issued, claim-relative applicability result."""

    candidate: EvidenceRoleCandidate
    status: ApplicabilityAssessmentStatus
    reason: str
    scope: ClaimScopeRef
    trace: Trace
    residuals: tuple[Residual, ...]
    specification_id: str
    registry_snapshot_id: str
    registry_projection_hash: str
    model_results: tuple[tuple[str, ApplicabilityModelResult], ...] = ()
    _assessment_token: InitVar[object | None] = field(
        default=None, repr=False, compare=False
    )

    def __post_init__(self, _assessment_token: object | None) -> None:
        if _assessment_token is not _ASSESSMENT_TOKEN:
            raise ValueError(
                "evidence applicability assessments must be issued by "
                "ApplicabilityAssessmentGate"
            )
        if type(self.candidate) is not EvidenceRoleCandidate:
            raise TypeError(
                "applicability assessments require an evidence-role candidate"
            )
        if self.scope != self.candidate.claim.content.core.scope:
            raise ValueError("applicability assessment scope must be claim scope")
        if not self.reason.strip() or type(self.trace) is not Trace:
            raise ValueError("applicability assessments require reason and trace")
        if self.status is ApplicabilityAssessmentStatus.PASS and self.residuals:
            raise ValueError("PASS applicability assessments cannot retain residuals")
        if self.status is ApplicabilityAssessmentStatus.DEFER and not self.residuals:
            raise ValueError("DEFER applicability assessments require residuals")


class ApplicabilityAssessmentGate:
    """Evaluates authorized models and selects the weakest model that closes."""

    @staticmethod
    def assess(
        candidate: EvidenceRoleCandidate,
        specification: ApplicabilityAssessmentSpecification,
        registry: SealedApplicabilityEvaluatorRegistry,
    ) -> EvidenceApplicabilityAssessment:
        if type(candidate) is not EvidenceRoleCandidate:
            raise TypeError(
                "applicability assessment requires an evidence-role candidate"
            )
        if type(specification) is not ApplicabilityAssessmentSpecification:
            raise TypeError("applicability assessment requires a specification")
        if type(registry) is not SealedApplicabilityEvaluatorRegistry:
            raise TypeError("applicability assessment requires a sealed registry")
        results: list[tuple[str, ApplicabilityModelResult]] = []
        for model in specification.models:
            binding = registry.resolve(model.evaluator_id)
            if (
                binding.role_identifier != candidate.role.identifier
                or binding.scope != candidate.claim.content.core.scope
            ):
                raise ValueError(
                    f"evaluator {model.evaluator_id} is not authorized for candidate"
                )
            result = binding.evaluator(candidate)
            if type(result) is not ApplicabilityModelResult:
                raise TypeError(
                    f"evaluator {model.evaluator_id} returned an invalid result"
                )
            results.append((model.model_id, result))
        by_id = dict(results)
        weaker_closure = _weaker_closure(specification.models)
        passing = [
            model for model in specification.models
            if by_id[model.model_id].status is ApplicabilityAssessmentStatus.PASS
        ]
        weakest_passing = [
            model
            for model in passing
            if not any(
                by_id[weaker].status is ApplicabilityAssessmentStatus.PASS
                for weaker in weaker_closure[model.model_id]
            )
        ]
        status = (
            ApplicabilityAssessmentStatus.PASS
            if passing
            else (
                ApplicabilityAssessmentStatus.BLOCK
                if any(
                    result.status is ApplicabilityAssessmentStatus.BLOCK
                    for _, result in results
                )
                else ApplicabilityAssessmentStatus.DEFER
            )
        )
        selected_models = weakest_passing
        if not selected_models:
            selected_models = [
                model
                for model in specification.models
                if by_id[model.model_id].status is status
                and not any(
                    by_id[weaker].status is status
                    for weaker in weaker_closure[model.model_id]
                )
            ]
        selected_ids = {model.model_id for model in selected_models}
        residuals = tuple(
            residual
            for model_id, result in results
            if status is not ApplicabilityAssessmentStatus.PASS
            and result.status is status
            and model_id in selected_ids
            for residual in result.residuals
        )
        events = tuple(
            event
            for model_id, result in results
            for event in (
                f"applicability model {model_id}: {result.status.value}",
                *result.trace.events,
            )
        )
        return EvidenceApplicabilityAssessment(
            candidate,
            status,
            "; ".join(
                f"{model_id}: {result.reason}"
                for model_id, result in results
            ),
            candidate.claim.content.core.scope, Trace(events), residuals,
            specification.specification_id,
            registry.snapshot_id,
            registry.registry_projection_hash,
            tuple(results),
            _assessment_token=_ASSESSMENT_TOKEN,
        )


def _weaker_closure(
    models: tuple[FrozenApplicabilityModel, ...],
) -> dict[str, frozenset[str]]:
    graph = {model.model_id: model.weaker_model_ids for model in models}
    closure: dict[str, frozenset[str]] = {}

    def descendants(model_id: str) -> frozenset[str]:
        if model_id in closure:
            return closure[model_id]
        values = set(graph[model_id])
        for weaker in graph[model_id]:
            values.update(descendants(weaker))
        closure[model_id] = frozenset(values)
        return closure[model_id]

    for model in models:
        descendants(model.model_id)
    return closure


def _has_cycle(models: tuple[FrozenApplicabilityModel, ...]) -> bool:
    graph = {model.model_id: model.weaker_model_ids for model in models}
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(identifier: str) -> bool:
        if identifier in visiting:
            return True
        if identifier in visited:
            return False
        visiting.add(identifier)
        if any(visit(weaker) for weaker in graph[identifier]):
            return True
        visiting.remove(identifier)
        visited.add(identifier)
        return False

    return any(visit(identifier) for identifier in graph)
