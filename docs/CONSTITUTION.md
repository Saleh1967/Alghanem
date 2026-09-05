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
| Verified invariant preservation | ENFORCED_AT_INVARIANT_GATE | Structural admission issues an opaque `admission_id`; verification provenance binds that exact transition identity and the sealed registry's `registry_snapshot_id`, in addition to claim, anchors, and trace. `InvariantVerificationGate.assess_all_preserved` and `InvariantVerificationBundle` require exactly one successful verification for every declared preserved component; both `InvariantVerificationDecision` and `InvariantVerificationBundle` are gate-issued only, mirroring each other (`VerificationDecision must be gate-issued`, and `InvariantVerificationBundle` now enforces this with its own private token), so a caller cannot hand-build a `VERIFIED` decision or a bundle, and a later layer that trusts either cannot be fooled by a self-declared result. An `InvariantSpec`'s `extractor_id` is only a claim, never a grant of authority: `InvariantExtractorRegistry.authorize` binds a trusted, registry-owned `RegisteredInvariantDefinition` (`domain`, `component`, `invariant_id` -> exactly one `extractor_id`), and `InvariantVerificationGate.verify` resolves only through `SealedInvariantExtractorRegistry.resolve_authorized`, which raises `UnauthorizedExtractorError` unless that exact extractor id is authorized for that exact scope (`Candidate/Caller does not own verifier selection authority`). `DEFER` is a real, distinct status: epistemic non-answers (unregistered or unauthorized extractor, failing extractor, ambiguous non-`bool` comparison) are `DEFER`, a disproved invariant is `BLOCK`, and internal/programming errors are caught into neither -- they propagate. `assess_all_preserved` evaluates every declared component independently rather than stopping at the first untestable one, and aggregates with strict precedence `BLOCK` (any disproved component) > `DEFER` (else, any untestable component) > `VERIFIED`, recording disproved (`failed_components`) and untestable (`deferred_components`) components as separate, sorted sets so the aggregate judgment never depends on the order components were declared in (`Known falsification dominates epistemic deferral`). Failures remain in an auditable `InvariantVerificationDecision`, and the convenience API raises a typed error carrying that decision. Registration authority, authorization authority, and snapshot resolution authority are three distinct concerns, but none of them is an evidential authority license. `StructurallyAdmissibleTransition.transition_projection_fingerprint` and `SealedInvariantExtractorRegistry.registry_projection_hash` are corroborating, deterministic *projections* of part of the transition/registry content, recorded alongside the opaque `admission_id`/`registry_snapshot_id` (`OccurrenceIdentity != ContentIdentity` for both transitions and registries) -- they are explicitly **not** canonical content identity or reproducibility proofs (each omits significant structurally-relevant content; see their docstrings), and must not be used to promote epistemic status. A full `CanonicalTransitionManifest`/`ExtractorRegistration` content-identity and reproducibility design is deferred to a dedicated follow-up. Verification is not yet wired into `StructuralAdmissionGate` or evidential sufficiency; `No epistemic promotion` remains `DECLARED_DEFERRED`. |
| Preserved/changed separation | ENFORCED | Preserved and changed components are non-blank, unique, and disjoint. |
| Declared change | ENFORCED | Every successful transition has a result and a changed component matching the operation's declared change. |
| Branch birth separation | ENFORCED | A branch-birth claim is distinct from identity preservation and requires origin provenance whose preserved components exactly equal its declared preserved components, plus a distinct branch anchor equal to the target anchor. |
| Non-admitted decisions | ENFORCED | `BLOCK`, `DEFER`, and `UNDEFINED` are external decision statuses (`StructuralDecisionStatus`), never properties of a candidate or `StructurallyAdmissibleTransition`s. |
| Non-success audit | ENFORCED | No non-success decision without reviewable audit information. Every non-success decision preserves its trace, its residuals, and a non-blank structural reason; the assessed candidate is preserved when one exists, and the audit's trace and residuals are then bound to that candidate's own history — no history without provenance from the assessed attempt. Without a candidate, the audit owns its trace and residuals directly. Non-success decision histories must not be erased: `require_admitted` raises `StructuralAdmissionError`, which carries the complete non-admitted decision. An optional `DecisionReasonCode` provides a coarse-grained, machine-auditable classification alongside the human-readable `reason`; it does not replace `reason` or carry additional structural authority. |
| Residual presence | PARTIALLY_ENFORCED | Residual records cannot be blank when present and are preserved in non-success audits, but residual provenance is not defined and residuals are not interpreted or ranked. |
| No epistemic promotion | DECLARED_DEFERRED | Claim/evidence binding is structural only; evidential sufficiency is not implemented. |
| No partial invariant coverage | DECLARED_DEFERRED | No transition may be promoted as preserved from partial invariant coverage; complete invariant verification is available as a separate gate before evidential sufficiency. |
| No higher-layer repair | DECLARED_DEFERRED | Higher layers may not repair invalid lower-layer transitions, but layer authority is not defined. |
| Canonical transition content snapshot | ENFORCED_AT_CONTENT_ENCODER | `CanonicalTransitionEncoder` is the sole issuer of `CanonicalTransitionManifest` and `TransitionContentIdentity`. The manifest preserves immutable canonical bytes for every structural transition field, including branch-origin provenance; occurrence-only `admission_id` and projection fingerprint are explicit exclusions. Its SHA-256 value is a digest reference, not proof of canonical-byte equality. Canonical values accept only exact built-in types, distinguish list from tuple and bytes from bytearray, preserve raw Unicode code points without normalization, encode finite floats as IEEE-754 binary64, and reject unsupported values and cycles. `preserved`, `changed`, and branch provenance components are sets; trace, evidence, and residuals are ordered sequences. Schema coverage rejects unaccounted structural fields. |

Invariant assessment request semantics are closed at the gate: `BLOCK` means an
authorized verifier observed at least one invariant as false; `DEFER` means no
invariant was false but at least one could not be checked; and `VERIFIED` means
every declared component was checked and preserved. Missing, extra, or duplicate
specifications are malformed requests and raise
`InvariantAssessmentSpecificationError`; they produce no epistemic decision and
must not be recorded as failed components.

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

Canonical manifests are independent snapshots: mutation of a shallow payload
after encoding cannot alter existing canonical bytes, but a later encoding may
produce a different content digest for the same admission occurrence.

The kernel does not assume reversibility, global composition, path
independence, a group, or a groupoid. Those questions are intentionally
deferred until later milestones.
