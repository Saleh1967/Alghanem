"""Licensed transitions and explicit transition decisions."""

from dataclasses import dataclass
from enum import Enum, auto

from .anchor import Anchor, State
from .evidence import Claim, Evidence
from .operation import Operation, OperationResult
from .residual import Residual
from .trace import Trace


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

    origin: Anchor
    preserved_components: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.preserved_components:
            raise ValueError("branch origin provenance requires preserved components")


@dataclass(frozen=True, slots=True)
class LicensedTransition:
    """A successful, licensed transition, validated at construction time."""

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

    def __post_init__(self) -> None:
        if self.result is None:
            raise ValueError("successful transitions require a result")
        if (
            self.operation.source_domain is not None
            and self.operation.source_domain != self.anchor.domain
        ):
            raise ValueError(
                "operation source domain must match the transition anchor domain"
            )
        if self.outcome in {Outcome.BLOCK, Outcome.DEFER, Outcome.UNDEFINED}:
            raise ValueError("non-transition outcomes cannot be LicensedTransition")
        if not self.evidence:
            raise ValueError("successful transitions require evidence")
        if any(evidence.claim != self.claim for evidence in self.evidence):
            raise ValueError("transition evidence must be bound to its claim")
        if self.outcome is Outcome.IDENTITY_PRESERVING_TRANSFORMATION:
            if not self.preserved:
                raise ValueError(
                    "identity-preserving transformations require an invariant"
                )
            if not self.changed:
                raise ValueError(
                    "identity-preserving transformations require a declared change"
                )
        if not self.changed:
            raise ValueError("successful transitions require a declared change")
        if self.operation.declared_change not in self.changed:
            raise ValueError(
                "transition changes must include the operation's declared change"
            )
        if not set(self.preserved).isdisjoint(self.changed):
            raise ValueError("preserved and changed components must be disjoint")
        if self.outcome is Outcome.CERTIFIED_BRANCH_BIRTH:
            if not self.preserved:
                raise ValueError(
                    "certified branch births require preserved information"
                )
            if self.branch_origin_provenance is None:
                raise ValueError(
                    "certified branch births require explicit origin provenance"
                )
            if self.branch_origin_provenance.origin != self.anchor:
                raise ValueError(
                    "branch origin provenance must match the transition anchor"
                )
            provenance_components = set(
                self.branch_origin_provenance.preserved_components
            )
            if not provenance_components.issubset(set(self.preserved)):
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
