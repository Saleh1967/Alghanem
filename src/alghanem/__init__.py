"""Language-agnostic research kernel for structurally admissible transformations."""

from .kernel.transition import StructurallyAdmissibleTransition, TransitionDecision

__all__ = ["StructurallyAdmissibleTransition", "TransitionDecision"]
