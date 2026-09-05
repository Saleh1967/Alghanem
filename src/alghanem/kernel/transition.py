"""Licensed transitions and their explicit outcomes."""

from dataclasses import dataclass
from enum import Enum, auto

from .anchor import Anchor
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
    """A minimally specified transition, validated at construction time."""

    anchor: Anchor
    operation: Operation
    evidence: tuple[Evidence, ...]
    preserved: tuple[str, ...]
    changed: tuple[str, ...]
    trace: Trace
    residuals: tuple[Residual, ...]
    outcome: Outcome
    result: OperationResult | None = None

    def __post_init__(self) -> None:
        if not self.anchor.domain:
            raise ValueError("a transition requires an explicit domain")
        if not self.preserved and self.outcome is Outcome.IDENTITY_PRESERVING_TRANSFORMATION:
            raise ValueError("identity-preserving transformations require an invariant")
        if self.outcome in {
            Outcome.IDENTITY_PRESERVING_TRANSFORMATION,
            Outcome.CERTIFIED_BRANCH_BIRTH,
        } and not self.evidence:
            raise ValueError("successful transitions require evidence")
        if self.outcome in {
            Outcome.BLOCK,
            Outcome.DEFER,
            Outcome.UNDEFINED,
        } and self.result is not None:
            raise ValueError("non-success outcomes cannot contain a result")
