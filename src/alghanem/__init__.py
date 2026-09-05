"""Language-agnostic research kernel for licensed transformations."""

from .kernel.transition import LicensedTransition, TransitionDecision

__all__ = ["LicensedTransition", "TransitionDecision"]
