"""G0.IC.1a: a gate-derived comparability closure assessment.

`IndependentClosure` is the step that G0.BV.1a openly declared missing: without
it, `BirthVerdictGate` can only defer. This module implements the part of that
step that is *decidable by copying an existing pattern*, and refuses to invent
the part that is not.

Structure copied, not invented. The register -> seal -> gate shape here is the
same one already enforced by `EvidenceAcquisitionAuthority`,
`InvariantExtractorRegistry` / `SealedInvariantExtractorRegistry` /
`InvariantVerificationGate`, `BirthEvaluatorImplementationRegistry` /
`SealedBirthEvaluatorImplementationRegistry` / `BirthEvaluatorExecutionGate`,
and `BirthVerdictScopeRegistry` / `SealedBirthVerdictScopeRegistry` /
`BirthVerdictGate`:

* `ClosureScopeRegistry.register` is the sole issuer of an
  `AuthorizedClosureScope`, and requires an already-verified
  `BirthExperimentSpecificationContentBinding`.
* `ClosureScopeRegistry.seal` alone produces a `SealedClosureScopeRegistry`.
* `IndependentClosureGate.assess` alone produces an
  `IndependentClosureAssessment`.

What this gate genuinely decides, and what it refuses to decide:

* `CallerDoesNotOwnClosureAuthority`. `assess` takes no status, no reason, and
  no comparability claim. It reads exactly one thing: the request's own frozen
  `ProjectionPoset`. Over a finite frozen projection set this is an
  exhaustively decidable question, so unlike G0.BV.1a's verdict this status is
  genuinely two-valued and both branches are reachable.
* `AbsentRelation != DeclaredIncomparability`, resolved conservatively. A
  frozen poset cannot distinguish "declared incomparable" from "relation never
  determined": both appear as the absence of a strict relation. The gate
  therefore treats both as unresolved competition. `COMPETITION_RESOLVED_IN_POSET`
  is reachable only when *every* other projection is strictly related to the
  test model, so ignorance is never read as resolution.
* `ComparabilityClosure != IndependentClosure`. This is the boundary this
  module refuses to cross. `NoRicherStructureBeforeLowerOpenResidualClosure`
  makes an empty competitor set only one conjunct of closure; the others are a
  residual that survived measurement or formal proof
  (`NoBirthWithoutResidualOrFormalNecessity`) and an exhausted licensed weaker
  model set (`NoBirthBeforeLicensedWeakerExhaustion`). Neither has any
  authority in this repository, and neither can be obtained by copying a
  pattern: both require *evaluating evidence content*, which
  `BirthEvaluatorExecutionGate` explicitly declares it does not do
  (`InputProvenance = DECLARED_DEFERRED`,
  `EvidenceAttachedToRecord != EvaluatorExecutedOnEvidence`). Accordingly
  `IndependentClosureAssessment.is_independent_closure` is `False`
  unconditionally, even on the resolved branch.
* `ComparabilityAssessment != Verdict`. `BirthVerdictGate` is deliberately not
  wired to consume this assessment. Consuming it would imply the missing
  conjuncts were satisfied, which would be exactly the fabricated closure
  G0.BV.1 exists to forbid. This stage issues no `BirthVerdict`, no `Freeze`,
  no `E0` mapping, and no `TraditionalName`.
* `AuthorizedScope != AssessedEvidence`. The assessment preserves the
  request's own authorized evidence snapshot for audit, but nothing here
  evaluates it.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from enum import Enum

from .birth import (
    BirthAssessmentRequest,
    BirthExperimentSpecification,
    BirthExperimentSpecificationError,
    EvidenceMode,
    _require_text,
)
from .evidence_acquisition import AuthorizedEvidenceSnapshot
from .experiment_spec_content_identity import (
    BirthExperimentSpecificationContentBinding,
    BirthExperimentSpecificationContentIdentity,
)

_CLOSURE_TOKEN = object()

_UNRESOLVED_REASON = (
    "MultipleIncomparableMinimalFactorizationsDefer: at least one projection "
    "is not strictly related to the test model in the frozen poset, and no "
    "authority here can supply discriminating evidence; an undetermined "
    "relation is counted as unresolved, never as resolution"
)
_RESOLVED_REASON = (
    "ComparabilityResolvedInFrozenPoset: every other projection is strictly "
    "related to the test model, so the incomparable-competitor clause of "
    "NoRicherStructureBeforeLowerOpenResidualClosure is vacuous in this scope. "
    "This is not IndependentClosure: no residual survival and no licensed "
    "weaker exhaustion has been certified by any authority"
)


class IndependentClosureAuthorityError(BirthExperimentSpecificationError):
    """A closure assessment was requested outside its authority boundary."""


class ComparabilityClosureStatus(Enum):
    """The gate's own two-valued comparability outcome, never a birth status."""

    COMPETITION_RESOLVED_IN_POSET = "COMPETITION_RESOLVED_IN_POSET"
    COMPETITION_UNRESOLVED_IN_POSET = "COMPETITION_UNRESOLVED_IN_POSET"


@dataclass(frozen=True, slots=True)
class AuthorizedClosureScope:
    """Issuer-only closure scope; conditions are derived, never caller-supplied.

    Every condition is read from the verified `binding`, so a scope cannot
    assert conditions the frozen experiment never froze. Holding a scope
    decides nothing: only `IndependentClosureGate` may act on one.
    """

    scope_id: str
    binding: BirthExperimentSpecificationContentBinding
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _CLOSURE_TOKEN:
            raise IndependentClosureAuthorityError(
                "authorized closure scopes must be issued by ClosureScopeRegistry"
            )
        _require_text(self.scope_id, "closure scope id")
        if type(self.binding) is not BirthExperimentSpecificationContentBinding:
            raise IndependentClosureAuthorityError(
                "a closure scope requires a verified frozen experiment binding"
            )

    @property
    def specification(self) -> BirthExperimentSpecification:
        """The specification proven equal to the authorized frozen manifest."""

        return self.binding.specification

    @property
    def experiment_content_id(self) -> BirthExperimentSpecificationContentIdentity:
        return self.binding.content_id

    @property
    def domain(self) -> str:
        return self.specification.domain

    @property
    def experiment_id(self) -> str:
        return self.specification.experiment_id

    @property
    def revision_id(self) -> str:
        return self.specification.revision_id

    @property
    def revision_sequence(self) -> int:
        return self.specification.revision_sequence

    @property
    def evidence_mode(self) -> EvidenceMode:
        return self.specification.evidence_mode

    @property
    def test_model(self) -> str:
        return self.specification.birth_query.test_model


class ClosureScopeRegistry:
    """Authority that issues and seals closure scopes; it assesses nothing."""

    def __init__(self) -> None:
        self._scopes: dict[
            tuple[str, BirthExperimentSpecificationContentIdentity],
            AuthorizedClosureScope,
        ] = {}
        self._issued_scope_ids: set[str] = set()
        self._lock = threading.Lock()

    def register(
        self,
        *,
        scope_id: str,
        binding: BirthExperimentSpecificationContentBinding,
    ) -> AuthorizedClosureScope:
        """Authorize exactly one frozen experiment for later closure assessment."""

        scope = AuthorizedClosureScope(
            scope_id=scope_id,
            binding=binding,
            _token=_CLOSURE_TOKEN,
        )
        key = (scope.domain, scope.experiment_content_id)
        with self._lock:
            if scope_id in self._issued_scope_ids:
                raise IndependentClosureAuthorityError(
                    "closure scope id already issued by this registry"
                )
            if key in self._scopes:
                raise IndependentClosureAuthorityError(
                    "a closure scope is already authorized for this exact domain "
                    "and frozen experiment content identity"
                )
            self._scopes[key] = scope
            self._issued_scope_ids.add(scope_id)
        return scope

    def seal(self, snapshot_id: str) -> SealedClosureScopeRegistry:
        """Freeze the authorized closure scopes."""

        _require_text(snapshot_id, "closure registry snapshot id")
        with self._lock:
            scopes = tuple(self._scopes.values())
        return SealedClosureScopeRegistry(
            snapshot_id=snapshot_id,
            scopes=scopes,
            _token=_CLOSURE_TOKEN,
        )


@dataclass(frozen=True, slots=True)
class SealedClosureScopeRegistry:
    """Frozen scope snapshot; it authorizes scopes but assesses nothing."""

    snapshot_id: str
    scopes: tuple[AuthorizedClosureScope, ...]
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _CLOSURE_TOKEN:
            raise IndependentClosureAuthorityError(
                "sealed closure registries must be issued by ClosureScopeRegistry"
            )
        _require_text(self.snapshot_id, "closure registry snapshot id")
        if type(self.scopes) is not tuple or any(
            type(item) is not AuthorizedClosureScope for item in self.scopes
        ):
            raise IndependentClosureAuthorityError(
                "sealed closure registries require frozen authorized scopes"
            )
        seen: set[tuple[str, BirthExperimentSpecificationContentIdentity]] = set()
        for scope in self.scopes:
            key = (scope.domain, scope.experiment_content_id)
            if key in seen:
                raise IndependentClosureAuthorityError(
                    "sealed closure registry must not contain duplicate scopes"
                )
            seen.add(key)

    def resolve(
        self,
        *,
        domain: str,
        experiment_content_id: BirthExperimentSpecificationContentIdentity,
    ) -> AuthorizedClosureScope:
        """Return the exact registry-issued scope for this frozen experiment."""

        for scope in self.scopes:
            if (
                scope.domain == domain
                and scope.experiment_content_id == experiment_content_id
            ):
                return scope
        raise IndependentClosureAuthorityError(
            "no authorized closure scope is registered for this exact domain "
            "and frozen experiment content identity"
        )


@dataclass(frozen=True, slots=True)
class IndependentClosureAssessment:
    """The gate-issued record of one scoped comparability assessment.

    `status` is never caller-supplied: it is computed by
    `IndependentClosureGate.assess` from the frozen projection poset alone.

    `COMPETITION_RESOLVED_IN_POSET` states exactly one thing: within this
    frozen experiment, no projection is left incomparable with the test model.
    It is not a birth, not a verdict, and not `IndependentClosure` — see
    `is_independent_closure`.
    """

    scope: AuthorizedClosureScope
    request: BirthAssessmentRequest
    evidence_snapshot: AuthorizedEvidenceSnapshot
    status: ComparabilityClosureStatus
    reason: str
    incomparable_competitors: tuple[str, ...]
    open_prerequisite_models: tuple[str, ...]
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _CLOSURE_TOKEN:
            raise IndependentClosureAuthorityError(
                "closure assessments must be issued by IndependentClosureGate"
            )
        if type(self.scope) is not AuthorizedClosureScope:
            raise IndependentClosureAuthorityError(
                "a closure assessment requires an authorized closure scope"
            )
        if type(self.request) is not BirthAssessmentRequest:
            raise IndependentClosureAuthorityError(
                "a closure assessment requires an authorized assessment request"
            )
        if type(self.evidence_snapshot) is not AuthorizedEvidenceSnapshot:
            raise IndependentClosureAuthorityError(
                "a closure assessment requires an authorized evidence snapshot"
            )
        if self.evidence_snapshot is not self.request.evidence_snapshot:
            raise IndependentClosureAuthorityError(
                "closure evidence must be the request's own bound evidence snapshot"
            )
        if not isinstance(self.status, ComparabilityClosureStatus):
            raise IndependentClosureAuthorityError(
                "a closure assessment requires a derived closure status"
            )
        _require_text(self.reason, "closure assessment reason")
        for models, field_name in (
            (self.incomparable_competitors, "incomparable competitors"),
            (self.open_prerequisite_models, "open prerequisite models"),
        ):
            if type(models) is not tuple or any(
                type(item) is not str for item in models
            ):
                raise IndependentClosureAuthorityError(
                    f"{field_name} must be frozen text"
                )
        resolved = (
            self.status is ComparabilityClosureStatus.COMPETITION_RESOLVED_IN_POSET
        )
        if resolved is bool(self.incomparable_competitors):
            raise IndependentClosureAuthorityError(
                "closure status must agree with the derived competitor set"
            )

    @property
    def is_independent_closure(self) -> bool:
        """Always `False`: comparability is only one conjunct of closure.

        `IndependentClosure` additionally requires a residual that survived
        measurement or formal proof, and an exhausted licensed weaker model
        set, each certified by an authority that does not exist here. This
        property is therefore `False` even on the resolved branch, so no
        caller can read a comparability result as a closure.
        """

        return False


class IndependentClosureGate:
    """The sole authority that may issue an `IndependentClosureAssessment`.

    The gate accepts no status, reason, or comparability claim from its
    caller. It resolves the request's own frozen experiment against a sealed
    scope registry and derives the status from that experiment's frozen
    projection poset alone.

    Unlike `BirthVerdictGate`, both branches of this status are reachable:
    comparability over a finite frozen projection set is exhaustively
    decidable. What remains unreachable is `IndependentClosure` itself.
    """

    @staticmethod
    def assess(
        *,
        registry: SealedClosureScopeRegistry,
        request: BirthAssessmentRequest,
    ) -> IndependentClosureAssessment:
        """Derive one scoped comparability assessment for a frozen experiment."""

        if type(registry) is not SealedClosureScopeRegistry:
            raise IndependentClosureAuthorityError(
                "closure assessment requires a sealed closure scope registry"
            )
        if type(request) is not BirthAssessmentRequest:
            raise IndependentClosureAuthorityError(
                "closure assessment requires an authorized assessment request"
            )

        specification = request.specification
        scope = registry.resolve(
            domain=specification.domain,
            experiment_content_id=request.experiment_binding.content_id,
        )
        if scope.specification != specification:
            raise IndependentClosureAuthorityError(
                "resolved closure scope does not match the request's own "
                "frozen experiment specification"
            )

        competitors = specification.competing_projections
        if competitors:
            status = ComparabilityClosureStatus.COMPETITION_UNRESOLVED_IN_POSET
            reason = _UNRESOLVED_REASON
        else:
            status = ComparabilityClosureStatus.COMPETITION_RESOLVED_IN_POSET
            reason = _RESOLVED_REASON

        return IndependentClosureAssessment(
            scope=scope,
            request=request,
            evidence_snapshot=request.evidence_snapshot,
            status=status,
            reason=reason,
            incomparable_competitors=competitors,
            open_prerequisite_models=specification.frozen_weaker_models,
            _token=_CLOSURE_TOKEN,
        )
