"""Transition candidates, licensed transitions, and explicit decisions."""

from dataclasses import InitVar, dataclass
from enum import Enum, auto

from .anchor import Anchor, State
from .evidence import Claim, Evidence
from .operation import Operation, OperationResult
from .residual import Residual
from .trace import Trace

_LICENSE_TOKEN = object()


class Outcome(Enum):
    """The complete initial vocabulary of transition outcomes."""

    IDENTITY_PRESERVING_TRANSFORMATION = auto()
    CERTIFIED_BRANCH_BIRTH = auto()
    BLOCK = auto()
    DEFER = auto()
    UNDEFINED = auto()


@dataclass(frozen=True, slots=True)
class BranchOriginProvenance:
    """Structural origin provenance for preserved branch components."""

    origin_anchor: Anchor
    branch_anchor: Anchor
    preserved_components: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.preserved_components:
            raise ValueError("branch origin provenance requires preserved components")
        _validate_components(
            "branch origin provenance preserved components",
            self.preserved_components,
        )
        if self.branch_anchor == self.origin_anchor:
            raise ValueError(
                "branch origin provenance requires a distinct branch anchor"
            )


@dataclass(frozen=True, slots=True)
class TransitionCandidate:
    """A transition-shaped candidate that has not crossed the licensing boundary.

    ``anchor`` is the source anchor; ``target_anchor`` is the explicitly
    declared anchor the transition targets. A candidate may omit
    ``target_anchor`` before licensing, but a successful transition must
    declare it explicitly; ``resolved_target_anchor`` never substitutes for
    the explicitness requirement.
    """

    anchor: Anchor
    before_state: State
    operation: Operation
    after_state: State
    claim: Claim
    evidence: tuple[Evidence, ...]
    preserved: tuple[str, ...]
    changed: tuple[str, ...]
    trace: Trace
    residuals: tuple[Residual, ...]
    outcome: Outcome
    result: OperationResult | None
    branch_origin_provenance: BranchOriginProvenance | None = None
    target_anchor: Anchor | None = None

    @property
    def resolved_target_anchor(self) -> Anchor:
        """The declared target anchor, defaulting to the source anchor.

        A convenience view for incomplete candidates only; it never satisfies
        the explicit-target-anchor requirement for a successful transition.
        """
        return self.target_anchor if self.target_anchor is not None else self.anchor

    def __post_init__(self) -> None:
        _validate_candidate_components(self)

    def validate_success(self) -> None:
        """Validate the structural laws required for licensing success."""

        _validate_successful_transition_fields(self)


@dataclass(frozen=True, slots=True)
class LicensedTransition(TransitionCandidate):
    """A successful transition issued only by the licensing boundary.

    Use ``LicensingGate.license`` on a candidate to create this type. Dataclass
    replacement paths that rerun ``__init__`` are not licensing paths.
    """

    _license_token: InitVar[object | None] = None

    def __post_init__(self, _license_token: object | None) -> None:
        if _license_token is not _LICENSE_TOKEN:
            raise ValueError("licensed transitions must be issued by LicensingGate")
        _validate_candidate_components(self)
        self.validate_success()


class LicensingGate:
    """Minimal structural licensing boundary for successful transitions.

    Already licensed transitions are rejected rather than re-licensed.
    """

    @staticmethod
    def license(candidate: TransitionCandidate) -> LicensedTransition:
        """Issue a licensed transition after structural validation."""

        if isinstance(candidate, LicensedTransition):
            raise ValueError("licensed transitions cannot be re-licensed")
        return LicensedTransition(
            anchor=candidate.anchor,
            before_state=candidate.before_state,
            operation=candidate.operation,
            after_state=candidate.after_state,
            claim=candidate.claim,
            evidence=candidate.evidence,
            preserved=candidate.preserved,
            changed=candidate.changed,
            trace=candidate.trace,
            residuals=candidate.residuals,
            outcome=candidate.outcome,
            result=candidate.result,
            branch_origin_provenance=candidate.branch_origin_provenance,
            target_anchor=candidate.target_anchor,
            _license_token=_LICENSE_TOKEN,
        )


def _validate_components(label: str, components: tuple[str, ...]) -> None:
    if any(not component.strip() for component in components):
        raise ValueError(f"{label} cannot be blank")
    if len(set(components)) != len(components):
        raise ValueError(f"{label} must be unique")


def _validate_candidate_components(candidate: TransitionCandidate) -> None:
    _validate_components("preserved components", candidate.preserved)
    _validate_components("changed components", candidate.changed)


def _validate_successful_transition_fields(candidate: TransitionCandidate) -> None:
    if candidate.result is None:
        raise ValueError("successful transitions require a result")
    if (
        candidate.operation.source_domain is not None
        and candidate.operation.source_domain != candidate.anchor.domain
    ):
        raise ValueError(
            "operation source domain must match the transition anchor domain"
        )
    if candidate.target_anchor is None:
        raise ValueError("successful transitions require an explicit target anchor")
    target_anchor = candidate.target_anchor
    if (
        candidate.operation.target_domain is not None
        and candidate.operation.target_domain != target_anchor.domain
    ):
        raise ValueError("operation target domain must match the target anchor domain")
    if candidate.outcome in {Outcome.BLOCK, Outcome.DEFER, Outcome.UNDEFINED}:
        raise ValueError("non-transition outcomes cannot be LicensedTransition")
    if not candidate.evidence:
        raise ValueError("successful transitions require evidence")
    if any(
        evidence.claim_id != candidate.claim.claim_id for evidence in candidate.evidence
    ):
        raise ValueError("transition evidence must be bound to its claim")
    if candidate.outcome is Outcome.IDENTITY_PRESERVING_TRANSFORMATION:
        if not candidate.preserved:
            raise ValueError("identity-preserving transformations require an invariant")
        if not candidate.changed:
            raise ValueError(
                "identity-preserving transformations require a declared change"
            )
        if target_anchor != candidate.anchor:
            raise ValueError(
                "identity-preserving transformations require an unchanged anchor"
            )
    if not candidate.changed:
        raise ValueError("successful transitions require a declared change")
    if candidate.operation.declared_change not in candidate.changed:
        raise ValueError(
            "transition changes must include the operation's declared change"
        )
    if not set(candidate.preserved).isdisjoint(candidate.changed):
        raise ValueError("preserved and changed components must be disjoint")
    if candidate.outcome is Outcome.CERTIFIED_BRANCH_BIRTH:
        _validate_branch_birth(candidate)


def _validate_branch_birth(candidate: TransitionCandidate) -> None:
    if not candidate.preserved:
        raise ValueError("certified branch births require preserved information")
    if candidate.branch_origin_provenance is None:
        raise ValueError("certified branch births require explicit origin provenance")
    if candidate.branch_origin_provenance.origin_anchor != candidate.anchor:
        raise ValueError("branch origin provenance must match the transition anchor")
    if candidate.target_anchor is None:
        raise ValueError("certified branch births require an explicit target anchor")
    target_anchor = candidate.target_anchor
    if target_anchor == candidate.anchor:
        raise ValueError("certified branch births require a distinct target anchor")
    if candidate.branch_origin_provenance.branch_anchor != target_anchor:
        raise ValueError(
            "branch origin provenance branch anchor must be the target anchor"
        )
    provenance_components = set(candidate.branch_origin_provenance.preserved_components)
    if not provenance_components.issubset(set(candidate.preserved)):
        raise ValueError(
            "branch origin provenance components must be declared preserved"
        )


@dataclass(frozen=True, slots=True)
class NonSuccessDecisionAudit:
    """Reviewable record of a decision that did not license a transition.

    A non-success decision is not an erased history: it preserves the trace,
    the residuals, and a structural reason so the decision can be reviewed.
    When an assessed candidate exists, the audit trace and residuals are bound
    to that candidate's own history, so no history is fabricated or attached
    without provenance. Without a candidate, the audit owns its trace and
    residuals directly. Residuals are preserved, not interpreted.
    """

    trace: Trace
    residuals: tuple[Residual, ...]
    reason: str
    candidate: TransitionCandidate | None = None

    def __post_init__(self) -> None:
        if not self.reason.strip():
            raise ValueError("non-success decisions require a structural reason")
        if self.candidate is not None and isinstance(
            self.candidate, LicensedTransition
        ):
            raise ValueError(
                "non-success decision audits cannot reference a licensed transition"
            )
        if self.candidate is not None and self.trace != self.candidate.trace:
            raise ValueError(
                "non-success decision audit trace must match the candidate trace"
            )
        if self.candidate is not None and self.residuals != self.candidate.residuals:
            raise ValueError(
                "non-success decision audit residuals must match the candidate"
            )


@dataclass(frozen=True, slots=True)
class TransitionDecision:
    """The assessment of an attempted transition, successful or not."""

    outcome: Outcome
    transition: LicensedTransition | None = None
    audit: NonSuccessDecisionAudit | None = None

    def __post_init__(self) -> None:
        successful = {
            Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
            Outcome.CERTIFIED_BRANCH_BIRTH,
        }
        if self.outcome in successful:
            if self.transition is None:
                raise ValueError("successful decisions require a licensed transition")
            if self.audit is not None:
                raise ValueError(
                    "successful decisions cannot carry a non-success audit"
                )
        else:
            if self.transition is not None:
                raise ValueError("non-transition decisions cannot contain a transition")
            if self.audit is None:
                raise ValueError("non-transition decisions require an audit record")
        if self.transition is not None and self.outcome is not self.transition.outcome:
            raise ValueError("decision and transition outcomes must match")
