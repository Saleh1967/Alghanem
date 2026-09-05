# Alghanem Kernel Constitution

These are the initial laws of the language-agnostic kernel:

| Law | Status | Kernel v0.1 scope |
| --- | --- | --- |
| Explicit domain | ENFORCED | Anchors require a non-blank domain. When an operation declares a source domain, it must match the transition anchor's domain. |
| Evidence present | ENFORCED | Successful transitions require at least one evidence record. |
| Evidence-to-claim binding | ENFORCED | Successful-transition evidence is structurally bound by claim id to the transition's own claim. This is not proof sufficiency. |
| Licensing boundary | ENFORCED | Candidates become licensed transitions only through the licensing gate. |
| Identity invariant | ENFORCED | Identity-preserving transformations require a declared invariant. |
| Preserved/changed separation | ENFORCED | Preserved and changed components are non-blank, unique, and disjoint. |
| Declared change | ENFORCED | Every successful transition has a result and a changed component matching the operation's declared change. |
| Branch birth separation | ENFORCED | Certified branch birth is distinct from identity preservation and requires preserved origin provenance tied to declared preserved components and a distinct branch anchor. |
| Non-transition outcomes | ENFORCED | `BLOCK`, `DEFER`, and `UNDEFINED` are decisions, not licensed transitions. |
| Residual presence | PARTIALLY_ENFORCED | Residual records cannot be blank when present, but residual provenance is not defined. |
| No epistemic promotion | DECLARED_DEFERRED | Claim/evidence binding is structural only; evidential sufficiency is not implemented. |
| No higher-layer repair | DECLARED_DEFERRED | Higher layers may not repair invalid lower-layer transitions, but layer authority is not defined. |

At Kernel v0.1, an operation's target domain is declared metadata only; it does
not grant transition authority.

Kernel dataclasses are shallowly immutable: field reassignment is blocked, but
payload objects stored in `State.value` and `OperationResult.value` are not
deep-frozen by the kernel.

The kernel does not assume reversibility, global composition, path
independence, a group, or a groupoid. Those questions are intentionally
deferred until later milestones.
