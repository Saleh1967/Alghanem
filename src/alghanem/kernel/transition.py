"""Licensed transitions and explicit transition decisions."""

from dataclasses import dataclass
from enum import Enum, auto

from .anchor import Anchor, State
from .evidence import Evidence
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
class LicensedTransition:
    """A successful, licensed transition, validated at construction time."""

    anchor: Anchor
    before_state: State
    operation: Operation
    after_state: State
    evidence: tuple[Evidence, ...]
    preserved: tuple[str, ...]
    changed: tuple[str, ...]
    trace: Trace
    residuals: tuple[Residual, ...]
    outcome: Outcome
    result: OperationResult

    def __post_init__(self) -> None:
        if self.result is None:
            raise ValueError("successful transitions require a result")
        if self.outcome in {Outcome.BLOCK, Outcome.DEFER, Outcome.UNDEFINED}:
            raise ValueError("non-transition outcomes cannot be LicensedTransition")
        if not self.evidence:
            raise ValueError("successful transitions require evidence")
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
            raise ValueError("transition changes must include the operation's declared change")
        if not set(self.preserved).isdisjoint(self.changed):
            raise ValueError("preserved and changed components must be disjoint")
        if self.outcome is Outcome.CERTIFIED_BRANCH_BIRTH and not self.preserved:
            raise ValueError("certified branch births require a preserved origin")


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
        if self.transition is not None and self.outcome is not self.transition.outcome:
            raise ValueError("decision and transition outcomes must match")
        if self.outcome not in successful and self.transition is not None:
            raise ValueError("non-transition decisions cannot contain a transition")
