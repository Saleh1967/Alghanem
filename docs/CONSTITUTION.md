# Alghanem Kernel Constitution

These are the initial laws of the language-agnostic kernel:

- No transition without an explicit domain.
- No successful transition without evidence.
- No identity-preserving transformation without a declared invariant.
- No hidden change: preserved and changed components must be distinguishable.
- No erased residuals.
- No epistemic promotion beyond the available evidence.
- `BLOCK`, `DEFER`, and `UNDEFINED` are not transformations.
- A `LicensedTransition` represents only a successful transformation; non-transition
  outcomes are represented by a `TransitionDecision` without a transition.
- Every successful transition has evidence, a result, and a declared change.
- A branch birth is distinct from an identity-preserving transformation.
- Higher layers may not retroactively repair an invalid lower-layer transition.
- The foundational kernel is language-agnostic.

The kernel does not assume reversibility, global composition, path
independence, a group, or a groupoid. Those questions are intentionally
deferred until later milestones.
