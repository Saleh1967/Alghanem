"""G0.EA.1 applicability assessment over an evidence-role candidate.

This module deliberately supplies no semantic role taxonomy.  Applicability
models are frozen by the caller, and their evaluators return only auditable
model checks.  The resulting assessment is not a sufficiency, truth, or
knowledge judgment.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, InitVar

from .evidence_role import EvidenceRoleCandidate
from .residual import Residual
from .trace import Trace

_ASSESSMENT_TOKEN = object()


class ApplicabilityAssessmentStatus(Enum):
    PASS = "pass"
    BLOCK = "block"
    DEFER = "defer"


@dataclass(frozen=True, slots=True)
class ApplicabilityModelResult:
    """One model's auditable check, not an evidence judgment."""

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


ApplicabilityEvaluator = Callable[
    [EvidenceRoleCandidate], ApplicabilityModelResult
]


@dataclass(frozen=True, slots=True)
class FrozenApplicabilityModel:
    """A caller-frozen applicability model and its explicitly weaker models."""

    identifier: str
    evaluator: ApplicabilityEvaluator
    weaker_model_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if type(self.identifier) is not str or not self.identifier.strip():
            raise ValueError("applicability models require an identifier")
        if not callable(self.evaluator):
            raise TypeError("applicability models require an evaluator")
        if type(self.weaker_model_ids) is not tuple or any(
            type(item) is not str or not item.strip()
            for item in self.weaker_model_ids
        ):
            raise TypeError("weaker applicability model ids must be text")
        if self.identifier in self.weaker_model_ids:
            raise ValueError("an applicability model cannot be weaker than itself")


@dataclass(frozen=True, slots=True)
class ApplicabilityAssessmentSpecification:
    """A frozen, explicit model family for one applicability assessment."""

    models: tuple[FrozenApplicabilityModel, ...]

    def __post_init__(self) -> None:
        if type(self.models) is not tuple or not self.models:
            raise ValueError("applicability specifications require frozen models")
        if any(type(item) is not FrozenApplicabilityModel for item in self.models):
            raise TypeError("applicability specifications require frozen models")
        identifiers = tuple(item.identifier for item in self.models)
        if len(set(identifiers)) != len(identifiers):
            raise ValueError("applicability models cannot duplicate identifiers")
        known = set(identifiers)
        for model in self.models:
            if not set(model.weaker_model_ids) <= known:
                raise ValueError("applicability models reference an unknown weaker model")
        if _has_cycle(self.models):
            raise ValueError("applicability model weakening must be acyclic")


@dataclass(frozen=True, slots=True)
class EvidenceApplicabilityAssessment:
    """The gate-issued, claim-relative applicability result."""

    candidate: EvidenceRoleCandidate
    status: ApplicabilityAssessmentStatus
    reason: str
    scope: object
    trace: Trace
    residuals: tuple[Residual, ...]
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
            raise TypeError("applicability assessments require an evidence-role candidate")
        if not isinstance(self.status, ApplicabilityAssessmentStatus):
            raise TypeError("applicability assessments require a status")
        if type(self.reason) is not str or not self.reason.strip():
            raise ValueError("applicability assessments require a reason")
        if self.scope != self.candidate.claim.content.core.scope:
            raise ValueError("applicability assessment scope must be claim scope")
        if type(self.trace) is not Trace:
            raise TypeError("applicability assessments require a trace")
        if type(self.residuals) is not tuple or any(
            type(item) is not Residual for item in self.residuals
        ):
            raise TypeError("applicability residuals must be a tuple of residuals")


class ApplicabilityAssessmentGate:
    """Runs only the caller-frozen applicability models."""

    @staticmethod
    def assess(
        candidate: EvidenceRoleCandidate,
        specification: ApplicabilityAssessmentSpecification,
    ) -> EvidenceApplicabilityAssessment:
        if type(candidate) is not EvidenceRoleCandidate:
            raise TypeError("applicability assessment requires an evidence-role candidate")
        if type(specification) is not ApplicabilityAssessmentSpecification:
            raise TypeError("applicability assessment requires a specification")

        results: list[tuple[str, ApplicabilityModelResult]] = []
        for model in specification.models:
            result = model.evaluator(candidate)
            if type(result) is not ApplicabilityModelResult:
                raise TypeError(
                    f"applicability model {model.identifier} returned an invalid result"
                )
            results.append((model.identifier, result))

        statuses = [result.status for _, result in results]
        if ApplicabilityAssessmentStatus.BLOCK in statuses:
            status = ApplicabilityAssessmentStatus.BLOCK
        elif ApplicabilityAssessmentStatus.DEFER in statuses:
            status = ApplicabilityAssessmentStatus.DEFER
        else:
            status = ApplicabilityAssessmentStatus.PASS
        residuals = tuple(
            residual for _, result in results for residual in result.residuals
        )
        events = tuple(
            f"applicability model {identifier}: {result.status.value}"
            for identifier, result in results
        )
        reason = "; ".join(
            f"{identifier}: {result.reason}" for identifier, result in results
        )
        return EvidenceApplicabilityAssessment(
            candidate=candidate,
            status=status,
            reason=reason,
            scope=candidate.claim.content.core.scope,
            trace=Trace(events),
            residuals=residuals,
            model_results=tuple(results),
            _assessment_token=_ASSESSMENT_TOKEN,
        )


def _has_cycle(models: tuple[FrozenApplicabilityModel, ...]) -> bool:
    graph = {model.identifier: model.weaker_model_ids for model in models}
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
