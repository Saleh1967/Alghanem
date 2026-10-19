"""Language-agnostic research kernel for structurally admissible transformations."""

from .kernel.transition import (
    StructuralAdmissionDecision,
    StructuralAdmissionError,
    StructuralDecisionStatus,
    StructurallyAdmissibleTransition,
)

__all__ = [
    "StructuralAdmissionDecision",
    "StructuralAdmissionError",
    "StructuralDecisionStatus",
    "StructurallyAdmissibleTransition",
]
