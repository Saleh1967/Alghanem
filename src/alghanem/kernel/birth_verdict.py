"""G0.BV.1a: an authority-issued, gate-derived scoped birth verdict.

This module implements the first executable authority boundary for a
`BirthVerdictStatus`. It copies, rather than invents, the register -> seal ->
gate shape already enforced three times in this repository
(`EvidenceAcquisitionAuthority`, `InvariantExtractorRegistry` /
`SealedInvariantExtractorRegistry` / `InvariantVerificationGate`, and
`BirthEvaluatorImplementationRegistry` /
`SealedBirthEvaluatorImplementationRegistry` /
`BirthEvaluatorExecutionGate`):

* `BirthVerdictScopeRegistry.register` is the sole issuer of an
  `AuthorizedBirthVerdictScope`, and requires an already-verified
  `BirthExperimentSpecificationContentBinding`. Every scope condition
  (`experiment_content_id`, `domain`, `experiment_id`, `revision_id`,
  `revision_sequence`, `test_model`) is *derived* from that binding, never
  accepted as an independent caller-supplied fact.
* `BirthVerdictScopeRegistry.seal` alone produces a
  `SealedBirthVerdictScopeRegistry`.
* `BirthVerdictGate.assess` alone produces a `BirthVerdictDecision`, and only
  for a request whose own frozen experiment resolves to an authorized scope in
  that sealed registry.

Two boundaries this module holds, and one narrowness it declares openly:

* `CallerDoesNotOwnVerdictAuthority`. `BirthVerdictGate.assess` takes no
  status, no reason, and no closure claim from its caller. It derives the
  status itself from the request's own frozen projection poset, so
  G0.BV.1's `No runtime authority may convert caller-declared assessment
  status into a verdict` is enforced by the signature, not only by prose.
* `DeferredVerdict != Birth`. This gate's codomain is currently the single
  value `BirthVerdictStatus.DEFER_IN_SCOPE`. `BIRTH_IN_SCOPE` and
  `NO_BIRTH_IN_SCOPE` are unreachable here *by construction*, not by
  accident: both require a gate-issued `IndependentClosureDecision`, and no
  authority in this repository can issue one. A verdict authority that can
  only defer still refuses every unlicensed birth, which is the boundary
  G0.BV.1 exists to protect; supplying the missing assessment authority
  (`ResidualAssessment -> LicensedWeakerExhaustion ->
  NecessaryInvariantCandidate -> BirthCandidate -> IndependentClosureDecision`)
  remains a separate, later stage. `NoDeferredVerdictMayBeFrozen`: this
  module issues no `Freeze` and no `E0` mapping, and
  `ScopedBirthIsNotGlobalOntologyClaim` still forbids reading any decision
  here as a global claim.
* `AuthorizedScope != AssessedEvidence`. The decision preserves the request's
  own authorized evidence snapshot for audit, but nothing here evaluates that
  evidence: no evaluator is executed, no residual is measured, and no weaker
  model is exhausted.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field

from .birth import (
    BirthAssessmentRequest,
    BirthExperimentSpecification,
    BirthExperimentSpecificationError,
    BirthVerdictStatus,
    EvidenceMode,
    _require_text,
)
from .evidence_acquisition import AuthorizedEvidenceSnapshot
from .experiment_spec_content_identity import (
    BirthExperimentSpecificationContentBinding,
    BirthExperimentSpecificationContentIdentity,
)

_BIRTH_VERDICT_TOKEN = object()

_UNRESOLVED_COMPETITION_REASON = (
    "MultipleIncomparableMinimalFactorizationsDefer: the frozen projection "
    "poset leaves incomparable competing models unresolved, and no "
    "discriminating evidence authority exists to resolve them"
)
_OPEN_PREREQUISITE_REASON = (
    "NoRicherStructureBeforeLowerOpenResidualClosure: the derived prerequisite "
    "cone is non-empty and no authority can certify any of its residuals closed"
)
_NO_CLOSURE_AUTHORITY_REASON = (
    "NoBirthWithoutIndependentClosure: no authority in this repository can "
    "issue the IndependentClosureDecision that BIRTH_IN_SCOPE or "
    "NO_BIRTH_IN_SCOPE would require"
)


class BirthVerdictAuthorityError(BirthExperimentSpecificationError):
    """A scoped verdict was requested outside its authority boundary."""


@dataclass(frozen=True, slots=True)
class AuthorizedBirthVerdictScope:
    """Issuer-only verdict scope; conditions are derived, never caller-supplied.

    `experiment_content_id`, `domain`, `experiment_id`, `revision_id`,
    `revision_sequence`, and `test_model` are read from the verified
    `binding`, so a scope cannot assert conditions the frozen experiment never
    froze. Holding a scope grants no verdict: only `BirthVerdictGate` may act
    on one (`AuthorizedScope != Verdict`).
    """

    scope_id: str
    binding: BirthExperimentSpecificationContentBinding
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _BIRTH_VERDICT_TOKEN:
            raise BirthVerdictAuthorityError(
                "authorized birth verdict scopes must be issued by "
                "BirthVerdictScopeRegistry"
            )
        _require_text(self.scope_id, "birth verdict scope id")
        if (
            type(self.binding) is not BirthExperimentSpecificationContentBinding  # noqa: E721
        ):
            raise BirthVerdictAuthorityError(
                "a birth verdict scope requires a verified frozen experiment binding"
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


class BirthVerdictScopeRegistry:
    """Authority that issues and seals verdict scopes; it issues no verdict."""

    def __init__(self) -> None:
        self._scopes: dict[
            tuple[str, BirthExperimentSpecificationContentIdentity],
            AuthorizedBirthVerdictScope,
        ] = {}
        self._issued_scope_ids: set[str] = set()
        self._lock = threading.Lock()

    def register(
        self,
        *,
        scope_id: str,
        binding: BirthExperimentSpecificationContentBinding,
    ) -> AuthorizedBirthVerdictScope:
        """Authorize exactly one frozen experiment for later verdict assessment."""

        scope = AuthorizedBirthVerdictScope(
            scope_id=scope_id,
            binding=binding,
            _token=_BIRTH_VERDICT_TOKEN,
        )
        key = (scope.domain, scope.experiment_content_id)
        with self._lock:
            if scope_id in self._issued_scope_ids:
                raise BirthVerdictAuthorityError(
                    "birth verdict scope id already issued by this registry"
                )
            if key in self._scopes:
                raise BirthVerdictAuthorityError(
                    "a verdict scope is already authorized for this exact "
                    "domain and frozen experiment content identity"
                )
            self._scopes[key] = scope
            self._issued_scope_ids.add(scope_id)
        return scope

    def seal(self, snapshot_id: str) -> SealedBirthVerdictScopeRegistry:
        """Freeze the authorized verdict scopes."""

        _require_text(snapshot_id, "birth verdict registry snapshot id")
        with self._lock:
            scopes = tuple(self._scopes.values())
        return SealedBirthVerdictScopeRegistry(
            snapshot_id=snapshot_id,
            scopes=scopes,
            _token=_BIRTH_VERDICT_TOKEN,
        )


@dataclass(frozen=True, slots=True)
class SealedBirthVerdictScopeRegistry:
    """Frozen scope snapshot; it authorizes scopes but assesses nothing."""

    snapshot_id: str
    scopes: tuple[AuthorizedBirthVerdictScope, ...]
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _BIRTH_VERDICT_TOKEN:
            raise BirthVerdictAuthorityError(
                "sealed birth verdict registries must be issued by "
                "BirthVerdictScopeRegistry"
            )
        _require_text(self.snapshot_id, "birth verdict registry snapshot id")
        if type(self.scopes) is not tuple or any(
            type(item) is not AuthorizedBirthVerdictScope for item in self.scopes
        ):
            raise BirthVerdictAuthorityError(
                "sealed birth verdict registries require frozen authorized scopes"
            )
        seen: set[tuple[str, BirthExperimentSpecificationContentIdentity]] = set()
        for scope in self.scopes:
            key = (scope.domain, scope.experiment_content_id)
            if key in seen:
                raise BirthVerdictAuthorityError(
                    "sealed birth verdict registry must not contain duplicate scopes"
                )
            seen.add(key)

    def resolve(
        self,
        *,
        domain: str,
        experiment_content_id: BirthExperimentSpecificationContentIdentity,
    ) -> AuthorizedBirthVerdictScope:
        """Return the exact registry-issued scope for this frozen experiment."""

        for scope in self.scopes:
            if (
                scope.domain == domain
                and scope.experiment_content_id == experiment_content_id
            ):
                return scope
        raise BirthVerdictAuthorityError(
            "no authorized verdict scope is registered for this exact domain "
            "and frozen experiment content identity"
        )


@dataclass(frozen=True, slots=True)
class BirthVerdictDecision:
    """The gate-issued record of one scoped verdict assessment.

    The decision preserves the exact scope, request, and evidence snapshot it
    was derived from, together with the derived competing models and
    prerequisite cone that produced its status. `status` is never a
    caller-supplied value: it is computed by `BirthVerdictGate.assess`.

    A `DEFER_IN_SCOPE` decision is a real, structurally valid, epistemically
    unresolved outcome — not a failure and not a birth. It may not be frozen,
    and it grants no naming, no `E0` mapping, and no ontology claim.
    """

    scope: AuthorizedBirthVerdictScope
    request: BirthAssessmentRequest
    evidence_snapshot: AuthorizedEvidenceSnapshot
    status: BirthVerdictStatus
    reason: str
    unresolved_competing_models: tuple[str, ...]
    open_prerequisite_models: tuple[str, ...]
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _BIRTH_VERDICT_TOKEN:
            raise BirthVerdictAuthorityError(
                "birth verdict decisions must be issued by BirthVerdictGate"
            )
        if type(self.scope) is not AuthorizedBirthVerdictScope:
            raise BirthVerdictAuthorityError(
                "a verdict decision requires an authorized verdict scope"
            )
        if type(self.request) is not BirthAssessmentRequest:
            raise BirthVerdictAuthorityError(
                "a verdict decision requires an authorized assessment request"
            )
        if type(self.evidence_snapshot) is not AuthorizedEvidenceSnapshot:
            raise BirthVerdictAuthorityError(
                "a verdict decision requires an authorized evidence snapshot"
            )
        if self.evidence_snapshot is not self.request.evidence_snapshot:
            raise BirthVerdictAuthorityError(
                "verdict evidence must be the request's own bound evidence snapshot"
            )
        if not isinstance(self.status, BirthVerdictStatus):
            raise BirthVerdictAuthorityError(
                "a verdict decision requires a declared verdict status"
            )
        _require_text(self.reason, "birth verdict reason")
        for models, field_name in (
            (self.unresolved_competing_models, "unresolved competing models"),
            (self.open_prerequisite_models, "open prerequisite models"),
        ):
            if type(models) is not tuple or any(
                type(item) is not str for item in models
            ):
                raise BirthVerdictAuthorityError(f"{field_name} must be frozen text")

    @property
    def is_birth(self) -> bool:
        """Whether this decision births anything; a deferral never does."""

        return self.status is BirthVerdictStatus.BIRTH_IN_SCOPE


class BirthVerdictGate:
    """The sole authority that may issue a scoped `BirthVerdictDecision`.

    The gate accepts no status, reason, or closure claim from its caller. It
    resolves the request's own frozen experiment against a sealed scope
    registry and then derives the status from that experiment's frozen
    projection poset alone.

    Its codomain is currently the single value `DEFER_IN_SCOPE`: reaching
    `BIRTH_IN_SCOPE` or `NO_BIRTH_IN_SCOPE` requires a gate-issued
    `IndependentClosureDecision`, which no authority here can produce. The
    derivation records *which* obstacle applied so the reason is auditable
    rather than uniform.
    """

    @staticmethod
    def assess(
        *,
        registry: SealedBirthVerdictScopeRegistry,
        request: BirthAssessmentRequest,
    ) -> BirthVerdictDecision:
        """Derive one scoped verdict for an authorized frozen experiment."""

        if type(registry) is not SealedBirthVerdictScopeRegistry:
            raise BirthVerdictAuthorityError(
                "verdict assessment requires a sealed birth verdict scope registry"
            )
        if type(request) is not BirthAssessmentRequest:
            raise BirthVerdictAuthorityError(
                "verdict assessment requires an authorized assessment request"
            )

        specification = request.specification
        scope = registry.resolve(
            domain=specification.domain,
            experiment_content_id=request.experiment_binding.content_id,
        )
        if scope.specification != specification:
            raise BirthVerdictAuthorityError(
                "resolved verdict scope does not match the request's own "
                "frozen experiment specification"
            )

        competing = specification.competing_projections
        prerequisites = specification.frozen_weaker_models
        if competing:
            reason = _UNRESOLVED_COMPETITION_REASON
        elif prerequisites:
            reason = _OPEN_PREREQUISITE_REASON
        else:
            reason = _NO_CLOSURE_AUTHORITY_REASON

        return BirthVerdictDecision(
            scope=scope,
            request=request,
            evidence_snapshot=request.evidence_snapshot,
            status=BirthVerdictStatus.DEFER_IN_SCOPE,
            reason=reason,
            unresolved_competing_models=competing,
            open_prerequisite_models=prerequisites,
            _token=_BIRTH_VERDICT_TOKEN,
        )
