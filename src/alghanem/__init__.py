"""Language-agnostic research kernel for structurally admissible transformations."""

from .kernel.transition import (
    StructuralAdmissionDecision,
    StructuralDecisionStatus,
    StructurallyAdmissibleTransition,
    TransitionDecision,
)

__all__ = [
    "StructuralAdmissionDecision",
    "StructuralDecisionStatus",
    "StructurallyAdmissibleTransition",
    "TransitionDecision",
]
