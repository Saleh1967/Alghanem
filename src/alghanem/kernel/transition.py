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
        if any(not component.strip() for component in self.preserved_components):
            raise ValueError("branch origin provenance components cannot be blank")
        if len(set(self.preserved_components)) != len(self.preserved_components):
            raise ValueError("branch origin provenance components must be unique")
        if self.branch_anchor == self.origin_anchor:
            raise ValueError(
                "branch origin provenance requires a distinct branch anchor"
            )


@dataclass(frozen=True, slots=True)
class TransitionCandidate:
    """A transition-shaped candidate that has not crossed the licensing boundary."""

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
    result: OperationResult
    branch_origin_provenance: BranchOriginProvenance | None = None

    def validate_success(self) -> None:
        """Validate the structural laws required for licensing success."""

        _validate_successful_transition_fields(self)


@dataclass(frozen=True, slots=True)
class LicensedTransition(TransitionCandidate):
    """A successful transition issued only by the licensing boundary."""

    license_token: InitVar[object | None] = None

    def __post_init__(self, license_token: object | None) -> None:
        if license_token is not _LICENSE_TOKEN:
            raise ValueError("licensed transitions must be issued by LicensingGate")
        self.validate_success()


class LicensingGate:
    """Minimal structural licensing boundary for successful transitions."""

    @staticmethod
    def license(candidate: TransitionCandidate) -> LicensedTransition:
        """Issue a licensed transition after structural validation."""

        candidate.validate_success()
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
            license_token=_LICENSE_TOKEN,
        )


def _validate_components(name: str, components: tuple[str, ...]) -> None:
    if any(not component.strip() for component in components):
        raise ValueError(f"{name} components cannot be blank")
    if len(set(components)) != len(components):
        raise ValueError(f"{name} components must be unique")


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
    if candidate.outcome in {Outcome.BLOCK, Outcome.DEFER, Outcome.UNDEFINED}:
        raise ValueError("non-transition outcomes cannot be LicensedTransition")
    if not candidate.evidence:
        raise ValueError("successful transitions require evidence")
    if any(
        evidence.claim_id != candidate.claim.claim_id for evidence in candidate.evidence
    ):
        raise ValueError("transition evidence must be bound to its claim")
    _validate_components("preserved", candidate.preserved)
    _validate_components("changed", candidate.changed)
    if candidate.outcome is Outcome.IDENTITY_PRESERVING_TRANSFORMATION:
        if not candidate.preserved:
            raise ValueError("identity-preserving transformations require an invariant")
        if not candidate.changed:
            raise ValueError(
                "identity-preserving transformations require a declared change"
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
    provenance_components = set(candidate.branch_origin_provenance.preserved_components)
    if not provenance_components.issubset(set(candidate.preserved)):
        raise ValueError(
            "branch origin provenance components must be declared preserved"
        )


@dataclass(frozen=True, slots=True)
class TransitionDecision:
    """The assessment of an attempted transition, successful or not."""

    outcome: Outcome
    transition: LicensedTransition | None = None

    def __post_init__(self) -> None:
        successful = {
            Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
            Outcome.CERTIFIED_BRANCH_BIRTH,
        }
        if self.outcome in successful and self.transition is None:
            raise ValueError("successful decisions require a licensed transition")
        if self.outcome not in successful and self.transition is not None:
            raise ValueError("non-transition decisions cannot contain a transition")
        if self.transition is not None and self.outcome is not self.transition.outcome:
            raise ValueError("decision and transition outcomes must match")
