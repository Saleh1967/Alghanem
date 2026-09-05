# Alghanem Kernel Constitution

These are the initial laws of the language-agnostic kernel:

- No transition without an explicit domain.
  Domain names alone are insufficient: when an operation declares a source
  domain, that binding must be compatible with the transition anchor's domain.
- No successful transition without evidence.
- Evidence-to-claim binding is structural only; it is not proof sufficiency.
- No identity-preserving transformation without a declared invariant.
- No hidden change: preserved and changed components must be distinguishable.
- No erased residuals.
- No epistemic promotion beyond the available evidence.
- `BLOCK`, `DEFER`, and `UNDEFINED` are not transformations.
- A `LicensedTransition` represents only a successful transformation; non-transition
  outcomes are represented by a `TransitionDecision` without a transition.
- Every successful transition has evidence, a result, and a declared change.
- A branch birth is distinct from an identity-preserving transformation.
  Certified branch birth requires preserved origin provenance, not merely a
  non-empty preserved set.
- Higher layers may not retroactively repair an invalid lower-layer transition.
- The foundational kernel is language-agnostic.

The kernel does not assume reversibility, global composition, path
independence, a group, or a groupoid. Those questions are intentionally
deferred until later milestones.
