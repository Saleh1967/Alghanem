# Alghanem Kernel Constitution

These are the initial laws of the language-agnostic kernel:

| Law | Status | Kernel v0.1 scope |
| --- | --- | --- |
| Explicit domain | ENFORCED | Anchors require a non-blank domain. When an operation declares a source domain, it must match the source anchor's domain. When an operation declares a target domain, it must match the target anchor's domain. |
| Explicit target anchor | ENFORCED | No successful transition without an explicitly declared target anchor; a default derived from the source anchor never satisfies admission. Identity-preserving transformations require source anchor = target anchor. Branch-birth claims require source anchor != target anchor, and branch provenance must bind the actual source and target anchors. |
| Evidence present | ENFORCED | Successful transitions require at least one evidence record. |
| Evidence-to-claim binding | ENFORCED | Successful-transition evidence is structurally bound by claim id to the transition's own claim. This is not proof sufficiency. |
| Structural admission boundary | ENFORCED | Candidates become `StructurallyAdmissibleTransition`s only through `StructuralAdmissionGate`. The gate is a controlled construction boundary inside the Python API, not a cryptographic or security-grade mechanism, and it certifies structural completeness only — not evidential sufficiency, domain-transition authority, or layer authority. Structural admission must not be conflated with a future `LicensedTransition`: `Representability != Licensability` and `StructuralValidity != EvidentialSufficiency`. |
| Claimed kind vs. certified outcome | ENFORCED | Every candidate declares what it represents via `TransitionKind` (`IDENTITY_PRESERVATION_CLAIM` or `BRANCH_BIRTH_CLAIM`). Candidates do not carry certified outcomes or decision statuses (`Candidate != Decision`); a candidate cannot decide or certify its own outcome. `StructuralAdmissionGate` evaluates the candidate and yields a `StructuralAdmissionDecision` with a status (`ADMITTED`, `BLOCK`, `DEFER`, `UNDEFINED`). `CertifiedOutcome` (`IDENTITY_PRESERVING_TRANSFORMATION`, `CERTIFIED_BRANCH_BIRTH`) is strictly reserved for the final certification stage (`CertifiedTransition`), not asserted by structural admission alone. In particular, `target_anchor == anchor` is a structural check, not proof: `AnchorEquality != ProvenIdentityPreservation`. Declaring a name in `preserved`/`changed` is not proof it was extracted from `before_state`/`after_state`: `DeclaredInvariant != VerifiedInvariant`. |
| Declared invariant presence | ENFORCED | Identity-preserving transformations require a declared invariant. |
| Verified invariant preservation | PARTIALLY_ENFORCED | `InvariantVerificationGate.verify` independently checks a single named invariant against an already-admitted `StructurallyAdmissibleTransition`, producing a gate-issued `InvariantVerification` (`preserved: bool`) from an `InvariantObservation` of the actual before/after values. Construction is enforced, not just documented: `InvariantVerification` requires a private sentinel token only `InvariantVerificationGate.verify` holds, so it cannot be fabricated by direct construction. Registration authority is separated from resolution authority: extractors are registered on a mutable `InvariantExtractorRegistry`, but the gate only ever accepts a read-only `SealedInvariantExtractorRegistry` produced by `.seal()` — the gate itself never registers or manufactures extractor authority. Every verification carries an `InvariantVerificationProvenance` (source claim id, source anchor, resolved target anchor, source trace) binding it to the transition it checked; `InvariantVerificationGate.require_bound_to` rejects a verification replayed against a different transition, even under the same `invariant_id`. The comparison `before_value == after_value` is required to yield an actual `bool`; a non-`bool` result raises `InvariantComparisonError` instead of being coerced. `ClaimedInvariant != VerifiedInvariant`: declaring a spec, or a name in `preserved`, is still not proof, and none of this is a cryptographic identity guarantee — it raises the bar against accidental misuse and casual replay, not a determined, dishonest caller fabricating matching field values by hand. Verification is not yet wired into `StructuralAdmissionGate` or required for admission, it checks one declared invariant at a time (not the full `preserved` set), and it is not evidential sufficiency. |
| Preserved/changed separation | ENFORCED | Preserved and changed components are non-blank, unique, and disjoint. |
| Declared change | ENFORCED | Every successful transition has a result and a changed component matching the operation's declared change. |
| Branch birth separation | ENFORCED | A branch-birth claim is distinct from identity preservation and requires origin provenance whose preserved components exactly equal its declared preserved components, plus a distinct branch anchor equal to the target anchor. |
| Non-admitted decisions | ENFORCED | `BLOCK`, `DEFER`, and `UNDEFINED` are external decision statuses (`StructuralDecisionStatus`), never properties of a candidate or `StructurallyAdmissibleTransition`s. |
| Non-success audit | ENFORCED | No non-success decision without reviewable audit information. Every non-success decision preserves its trace, its residuals, and a non-blank structural reason; the assessed candidate is preserved when one exists, and the audit's trace and residuals are then bound to that candidate's own history — no history without provenance from the assessed attempt. Without a candidate, the audit owns its trace and residuals directly. Non-success decision histories must not be erased: `require_admitted` raises `StructuralAdmissionError`, which carries the complete non-admitted decision. An optional `DecisionReasonCode` provides a coarse-grained, machine-auditable classification alongside the human-readable `reason`; it does not replace `reason` or carry additional structural authority. |
| Residual presence | PARTIALLY_ENFORCED | Residual records cannot be blank when present and are preserved in non-success audits, but residual provenance is not defined and residuals are not interpreted or ranked. |
| No epistemic promotion | DECLARED_DEFERRED | Claim/evidence binding is structural only; evidential sufficiency is not implemented. |
| No higher-layer repair | DECLARED_DEFERRED | Higher layers may not repair invalid lower-layer transitions, but layer authority is not defined. |

At Kernel v0.1, an operation's target domain is declared structural metadata
only; it does not grant transition or domain-transition authority. Source and
target domains may differ; whether they must coincide is a licensing question
deferred beyond Kernel v0.1.

Structural admission is not full licensing. `StructuralAdmissionGate` proves
only that a transition is well-formed under the laws above; it does not prove
evidential sufficiency, cross-domain authority, or inter-layer authority.
Those remain declared-deferred laws, and a future `LicensedTransition` — issued
only once those gates exist — must not be assumed to already exist because a
transition is structurally admissible.

Kernel v0.1's epistemic ladder, current rung marked with `*`:

```
Representable (TransitionCandidate) -> *StructurallyAdmissible* (StructurallyAdmissibleTransition) -> EvidentiallySupported -> AuthorityLicensed -> Certified (CertifiedTransition)
```

`TransitionKind` names the claim a candidate makes (what it is *representing*);
`StructurallyAdmissibleTransition` certifies only that the claim is
well-formed under structural laws. `StructuralAdmissionGate` evaluates candidates
to produce `StructuralAdmissionDecision`s (`ADMITTED`, `BLOCK`, `DEFER`, `UNDEFINED`).
Evidential sufficiency (`EvidentiallySupportedTransition`), authority to license a
transition (`AuthorityLicensedTransition`), and final certification
(`CertifiedTransition` carrying `CertifiedOutcome`) are later rungs, deferred
beyond Kernel v0.1. A linguistic layer (for example, a future Carrier/J
adapter) must be built as a client that produces evidence and invariant
claims for this kernel to structurally admit; it must not be granted
certification the kernel itself does not yet issue.

Kernel dataclasses are shallowly immutable: field reassignment is blocked, but
payload objects stored in `State.value` and `OperationResult.value` are not
deep-frozen by the kernel.

The kernel does not assume reversibility, global composition, path
independence, a group, or a groupoid. Those questions are intentionally
deferred until later milestones.
