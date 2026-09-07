# Alghanem Kernel Constitution

These are the initial laws of the language-agnostic kernel:

| Law | Status | Kernel v0.1 scope |
| --- | --- | --- |
| Explicit domain | ENFORCED | Anchors require a non-blank domain. When an operation declares a source domain, it must match the source anchor's domain. When an operation declares a target domain, it must match the target anchor's domain. |
| Explicit target anchor | ENFORCED | No successful transition without an explicitly declared target anchor; a default derived from the source anchor never satisfies admission. Identity-preserving transformations require source anchor = target anchor. Branch-birth claims require source anchor != target anchor, and branch provenance must bind the actual source and target anchors. |
| Evidence present | ENFORCED | Successful transitions require at least one evidence record. |
| Evidence-to-claim binding | ENFORCED | Successful-transition evidence is structurally bound by claim id to the transition's own claim. This is not proof sufficiency. |
| G0.C.1 minimal claim constitution | ENFORCED_AT_CONTENT_ENCODER | `ClaimCandidate` is a reviewable occurrence of `ClaimContentManifest(ClaimCore, qualifications)`, not truth, evidence, knowledge, or a license. For the declared target of distinguishing structured claims, no-weaker projection collisions prove `anchor`, opaque typed `PredicateRef`, `polarity`, and `scope` are each necessary in `ClaimCore`; broader semantic minimality remains `DECLARED_DEFERRED`. Predicate rendering and semantics are deferred, so text is not claim input or primary identity. `CanonicalClaimContentEncoder` alone issues a `ClaimContentIdentity`; coverage guards fail closed for every field of `ClaimContentManifest`, `ClaimCore`, `PredicateRef`, `ClaimScopeRef`, and `ClaimQualification`. Qualification tuple order is content-significant (`NoUnlicensedQualificationCommutation`). Scope and polarity are encoded content. `ClaimOccurrenceRef != ClaimOccurrenceIdentity`: it is a reusable local reference only; portable occurrence identity is `DECLARED_DEFERRED`. The legacy `Claim(claim_id, statement)`/`ClaimEvidenceBinding` runtime remains separate and its claim-id equality is not G0.EB.1 evidence binding. No evidence or evidence-binding field exists in `ClaimCandidate`; claim-specific evidence binding is deferred to G0.EB.1. |
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
| G0.2a.1 birth semantics content identity | ENFORCED_AT_CONTENT_ENCODER | `NoResidualIdDriftAfterFreeze`/`NoClosureCriterionIdDriftAfterFreeze` (G0.2a's id-equality checks) are label identity, not content identity: `ResidualDefinitionId != ResidualDefinitionContentIdentity`, and the same distinction holds for `ClosureCriterionSpec` and `WeakerModelSpec`. `CanonicalBirthSemanticsEncoder` is the sole issuer of `CanonicalResidualDefinitionManifest`, `CanonicalClosureCriterionManifest`, `CanonicalWeakerModelManifest`, and their `BirthSemanticsContentIdentity` SHA-256 digest references, covering every declared field of each spec. `BirthSemanticsContentRegistry` freezes the *first* canonical content bound to an exact `(domain, role, target_id)` scope; a later attempt to bind different content to that same scope is content drift and is rejected, not silently accepted because the id string still matches. `BirthAssessmentContentBinding` resolves every scope a `BirthAssessmentSemanticsContract` declares against a `SealedBirthSemanticsContentRegistry` and requires `CID(runtime) == CID(frozen)` for the residual definition, the closure criterion, and every weaker model; an unresolvable scope raises rather than passing silently. This closes `NoSemanticDriftAfterFreeze` for content, distinct from and in addition to `NoResidualDefinitionDriftAfterFreeze`/`NoClosureCriterionDriftAfterFreeze` for ids. It performs no evaluation and issues no `BirthVerdict`, `BirthCandidate`, or `Freeze`; `EvaluatorId != EvaluatorImplementationIdentity` and evaluator execution authority remain out of scope. |
| G0.2a.3 evidence acquisition authority | ENFORCED_AT_ACQUISITION_AUTHORITY | Binding evidence to a frozen experiment (G0.2a.2) proves only `FreezePrecedesRequestConstruction`, not that the freeze authorized the evidence's own acquisition; a caller could still select evidence first and attach a freeze afterward. This stage closes the narrower, code-provable `FrozenExperimentPrecedesAuthorizedEvidenceIngestion` instead of an unprovable external-world chronology claim (`AuthorizedCapture != ProofOfExternalAcquisitionChronology`). `EvidenceAcquisitionAuthority.authorize` is the sole issuer of an `EvidenceAcquisitionAuthorization`, requiring a genuine, verified `BirthExperimentSpecificationContentBinding` (`NoEvidenceAcquisitionAuthorizationWithoutFrozenExperiment`); its `experiment_content_id`, `domain`, `evidence_mode`, `evidence_requirements`, `revision_id`, and `revision_sequence` are derived properties of that binding, never independent caller-supplied facts. Only that authorization can issue an `EvidenceAcquisitionRun` (`open_run`), and only that run can issue an `AuthorizedEvidenceSnapshot` (`ingest`), closing `NoAssessableEvidenceSnapshotWithoutAcquisitionAuthorization`; none of the three is caller-constructible. `CanonicalEvidenceContentEncoder` alone issues the ingested payload's `EvidenceContentIdentity`, keeping `EvidenceOccurrenceIdentity != EvidenceContentIdentity` (`snapshot_id`/`run_id`/`authorization_id` name one occurrence; `content_id` is a digest over ingested bytes). `BirthAssessmentRequest` now requires an `AuthorizedEvidenceSnapshot` (rejecting the deprecated, unauthorized `EvidenceSnapshot`) and rejects a snapshot whose `experiment_content_id` does not equal its own experiment binding's `content_id`. `AuthorizedEvidence != SufficientEvidence`: this stage does not imply `ResidualSurvival` or `Birth`, and issues no `ResidualAssessment` or `BirthVerdict`. |
| G0.2a.3.1 issuer-scoped occurrence issuance integrity | ENFORCED_AT_ACQUISITION_AUTHORITY | Before this stage, `authorization_id`/`run_id`/`snapshot_id` were caller-chosen strings with no uniqueness authority: an issuer accepted a repeat of the same id, so `same(id) => same(occurrence)` did not hold and these were `EvidenceOccurrenceCoordinates`, not a proven identity. Each issuer now keeps its own registry of ids it has already issued -- `EvidenceAcquisitionAuthority` for `authorization_id`, one `EvidenceAcquisitionAuthorization` for its own `run_id`s, one `EvidenceAcquisitionRun` for its own `snapshot_id`s -- and `EvidenceAcquisitionAuthorityError` rejects a repeat within that scope, even for a snapshot repeat carrying different content. Each registry's check-and-insert is synchronized with an internal lock so concurrent calls on one instance cannot race past the uniqueness check. This makes issuance injective *within its declared scope* (`IssuerScopedOccurrenceUniqueness = PROVED`): two ids from the same issuer that are equal name the same occurrence, and two ids from the same issuer that differ name different occurrences. `LocalInjectivity != PortableIdentity`: `AuthorizedEvidenceSnapshot` carries no `issuer_scope_id`, so two distinct `EvidenceAcquisitionAuthority` instances are separate, uncoordinated issuance scopes whose ids are not thereby proven to differ from each other, and two snapshots from different authorities can share identical comparable representations despite being genuinely independent occurrences. `PortableEvidenceOccurrenceIdentity` remains `DEFERRED` pending a self-issuing `EvidenceIssuerScopeIdentity` propagated through the chain. `EvidenceAcquisitionRun`/`EvidenceAcquisitionAuthorization` are `ExternallyFrozen, InternallyStatefulAuthority` objects: `frozen=True` fixes their own declared identity fields, but each also holds a private, mutable `_issued_*` registry and lock (excluded from equality, `repr`, and content identity) as operational bookkeeping only. |

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

## G0 — Birth Protocol (declared law, no runtime gate yet)

The kernel and Arabic layer never introduce a new named object, cardinality,
or ontology term because it is convenient, expected, or traditional. A
candidate object is only permitted to be *born* — closed independently and
eventually handed a traditional name — through the following declared chain.
At Kernel v0.1 this chain is **law only**: no `BirthGate`, rank/complexity
class, or Arabic-specific carrier/state/relation ontology type exists yet. A
non-linguistic intervention-operation runtime does already exist (see
`InterventionOperationIsNotOntology` below); it is a declared experimental
tool, not one of these ontology types, and does not itself satisfy this
chain. Those ontology types are separate, later milestones that must
themselves be structurally admitted like any other change, and must not be
named in advance of the residual that would force them (`G0.F` below); this
section only freezes the constraints they will have to satisfy if and when
they are born.

```
BirthQuery -> Evidence -> Residual -> LicensedWeakerExhaustion
-> NecessaryInvariantCandidate -> BirthCandidate -> IndependentClosure
-> BirthVerdict -> Freeze -> E0 -> TraditionalName
```

`BirthCandidate != BirthVerdict`: a candidate remains only a proposal until
`IndependentClosure` produces `BIRTH_IN_SCOPE` through a future gate. `Freeze`
is the separate, later act of fixing only that successful scoped verdict;
`E0` consumes that frozen result in a subsequent stage. `NO_BIRTH_IN_SCOPE`
and `DEFER_IN_SCOPE` cannot be frozen. Naming never occurs before birth
verdict, freeze, and `E0` have happened.

| Law | Status | Scope |
| --- | --- | --- |
| `NoBirthWithoutResidualOrFormalNecessity` | DECLARED_DEFERRED | No candidate object, factor, or axis may be born without one of two independent evidence modes. In `EMPIRICAL` mode, a *measured* residual (from real observations, not synthetic interventions alone) must remain unexplained after every licensed weaker projection has been applied. In `FORMAL` mode, over a declared `FrozenFormalDomain` with `card(Ω) < ∞` (or another exhaustively decidable closed domain), an exhaustive proof over every element of that domain, with no weaker formal model sufficing, may license birth without any measurement run. A `MIXED` mode combines both and must satisfy each mode's own condition on its own part of the claim. `FormalProof ⇏ EmpiricalReality` and `EmpiricalPattern ⇏ MathematicalNecessity`: neither mode substitutes for the other, and every birth must declare which mode(s) it relies on. |
| `NoBirthBeforeLicensedWeakerExhaustion` | DECLARED_DEFERRED | Before any `BirthCandidate` may be proposed, every weaker projection or formal model *licensed and frozen for that experiment* (`W_E = {W_1, ..., W_n}`), not an unbounded or open-ended "every weaker model conceivable," must first be tried and shown insufficient. A birth proposal that skips a licensed weaker model is malformed, not merely unproven. Discovering a new weaker model `W_{n+1}` afterward opens a new, separately recorded revision; it does not erase the historical closure in its original scope. |
| `NoRicherStructureBeforeLowerOpenResidualClosure` | DECLARED_DEFERRED | For a queried structure `q`, its prerequisite cone is exactly `Down_E(q) = {p ∈ P_E : p ≺_E q}`, derived from the experiment's frozen projection poset, never selected independently by the caller. If any `p ∈ Down_E(q)` has an open residual, examination of `q` is blocked. This is a partial-order constraint, not a linear "rank `r+1`" constraint. An incomparable projection (`p ∥ q`) does not block examination; however, if it offers a complete competing explanation of the residual, `BIRTH_IN_SCOPE(q)` is blocked until discriminating evidence resolves the competition. |
| `ScopedBirthIsNotGlobalOntologyClaim` | DECLARED_DEFERRED | Every verdict is scoped to the exact `(experiment, revision, domain, licensed weaker-model set, evidence mode, measurement run or formal domain, evidence snapshot)` tuple that produced it: `BIRTH_IN_SCOPE(...)`, `NO_BIRTH_IN_SCOPE(...)`, or `DEFER_IN_SCOPE(...)`. A malformed specification produces no verdict; `DEFER_IN_SCOPE` is reserved for a structurally valid but epistemically unresolved assessment. A later revision may become the active epistemic assessment, but cannot erase a prior verdict's historical scoped record. No scoped verdict generalizes into a global ontology claim. |
| `ProjectionIsNotOntology` | DECLARED_DEFERRED | Weaker-model projections (for example count, set, multiset, ordered-tuple) are analysis tools for deciding whether a residual survives, not born objects and not linguistic claims. Projections form a partial order, not a total order: `P_count` and `P_set` are incomparable (`P_count ∥ P_set`), while both are recoverable from `P_multiset`, and `P_multiset` is recoverable from `P_seq` (`P_count ⪯ P_multi`, `P_set ⪯ P_multi`, `P_multi ⪯ P_seq`). No total-order complexity vector may be assumed across projections or coordinates that have not themselves been born. |
| `InterventionOperationIsNotOntology` | DECLARED_DEFERRED | A declared basis of experimental interventions (for example an "ExperimentalInterventionBasisV0" of delete/insert/substitute/repeat/swap) is an explicit, named, non-exhaustive experimental tool. It must never be asserted to be the complete set of primitive operations, and its members are not linguistic or structural objects. |
| `CounterfactualResultIsNotObservation` | DECLARED_DEFERRED | The output of a synthetic/counterfactual intervention applied to a previously observed occurrence is not itself a `RawSurfaceObservation` or any other measured observation. This is a type/authority separation, not an implementation detail: a counterfactual result must belong to a distinct type that cannot be admitted into the observation or normalization ledgers, regardless of how any particular field on it is named or valued. |
| `SyntheticInterventionMayGenerateHypothesisOnly` | DECLARED_DEFERRED | A residual discovered only through synthetic/counterfactual interventions (`R_synthetic`) may license nothing beyond a hypothesis (recorded as a `HypothesisResidual`, not a `FactorCandidate`). It cannot by itself satisfy `NoBirthWithoutResidualOrFormalNecessity`. A hypothesis becomes birth-eligible only after an independently measured contrast (`R_measured`), drawn from real observations under a measurement run, is found to match the hypothesis and itself survives every licensed weaker projection, with replication in a second, independent measurement run. For example, a `swap` intervention showing `(a, b) != (b, a)` at the codepoint-sequence level proves only `CodepointSequenceIsOrderSensitive` within the synthetic domain; it does not by itself birth any order-related linguistic or structural candidate. |
| `TraditionalNamingOnlyAfterFreezeAndE0` | DECLARED_DEFERRED | A traditional name (linguistic, grammatical, or morphological) may only be attached after the full chain `BirthCandidate -> IndependentClosure -> BIRTH_IN_SCOPE -> Freeze -> E0` has completed. The name is never part of the birth proof, never influences whether birth, closure, or freeze occurs, and the kernel itself must never define or reference `TraditionalName`; any such naming step belongs strictly to a downstream, kernel-independent evaluation/oracle layer. |

These laws are declared now, ahead of any experiment, precisely so that the
question being asked cannot be quietly reshaped by the answer an experiment
later produces. Implementing `BirthGate`, a rank/complexity representation,
or any Arabic-specific carrier/state/relation ontology type is out of scope
for this section and must occur in later, separately reviewed milestones
that are held to these same laws. No such type -- including any general
linguistic "binding" relation -- is to be named or scaffolded before a
residual is shown to force it: see `G0.F`'s `DerivedRelationDoesNotBirth` and
`NoTraditionalSchemaBeforeFactorization` below. (`kernel/binding.py`'s
`ClaimEvidenceBinding` is an unrelated kernel-level evidence/claim binding,
not an Arabic linguistic relation, and is out of scope of this paragraph.)

### G0.1 — Birth experiment contract

`BirthExperimentSpecification` is a language-agnostic, frozen pre-evidence
contract. It contains an experiment identity, revision identity and monotonic
revision sequence, evidence mode, domain, frozen projection poset,
`BirthQuery`, stable residual-definition identity, residual-definition text,
stable closure-criterion identity, closure-criterion text, and evidence
requirements. The stable identities are the freeze boundary; descriptive text
alone cannot identify a later executable contract. It does not contain an
evidence snapshot, a candidate, a verdict, or caller-selected weaker models.
Its frozen weaker-model set and `PrerequisiteCone` are both derived as
`Down_E(q)` from the poset and query: they share values in G0.1, but name the
distinct frozen-model-set and query-relative order roles. Its incomparable
projections are recorded as possible competing explanations.

`BirthAssessmentRequest = AuthorizedFrozenExperimentBinding +
AuthorizedEvidenceSnapshot`; the request refuses a raw
`BirthExperimentSpecification` and refuses the legacy, unauthorized
`EvidenceSnapshot` (deprecated: it carries no acquisition provenance). This
ordering enforces `NoAssessmentRequestWithoutAuthorizedPreEvidenceFreeze` and
`EvidenceMayBeAttachedOnlyToAnAuthorizedFrozenExperiment`, preventing evidence
from redesigning the question or its closure criterion. The contract validates
malformed bindings before any request can enter a future runtime. G0.1 stops at
`BirthAssessmentRequest`: it has no
executable verdict, revision-history, competing-explanation assessment, or
freeze authority. `BirthVerdictStatus` is future vocabulary only.

### G0.2a.3 — Evidence acquisition authority

Binding evidence to a frozen experiment is not enough: a caller could still
select or construct evidence before designing an experiment, then attach it
to a `BirthExperimentSpecificationContentBinding` produced afterward. This
proves only `FreezePrecedesRequestConstruction`, not that the freeze
authorized the evidence's own acquisition. G0.2a.3 closes the narrower,
code-provable claim `FrozenExperimentPrecedesAuthorizedEvidenceIngestion`
instead of an unprovable external-world chronology claim.

The chain is
`BirthExperimentSpecification -> FrozenPreEvidenceExperimentManifest ->
BirthExperimentSpecificationContentBinding -> EvidenceAcquisitionAuthorization
-> EvidenceAcquisitionRun -> AuthorizedEvidenceSnapshot`.
`EvidenceAcquisitionAuthority.authorize` is the sole issuer of an
`EvidenceAcquisitionAuthorization`, and requires a genuine, already-verified
`BirthExperimentSpecificationContentBinding`
(`NoEvidenceAcquisitionAuthorizationWithoutFrozenExperiment`). The
authorization does not accept caller-supplied `experiment_content_id`,
`domain`, `evidence_mode`, `evidence_requirements`, `revision_id`, or
`revision_sequence`: every one of these is a derived property read from the
verified binding, so an authorization can never assert a condition the frozen
experiment did not itself freeze.

An `EvidenceAcquisitionAuthorization` is also the sole issuer of an
`EvidenceAcquisitionRun` (`authorization.open_run(...)`), and an
`EvidenceAcquisitionRun` is the sole issuer of an `AuthorizedEvidenceSnapshot`
(`run.ingest(...)`), closing
`NoAssessableEvidenceSnapshotWithoutAcquisitionAuthorization`: no caller can
construct any of the three objects directly, each raising
`EvidenceAcquisitionAuthorityError` when its authority token is missing.
`CanonicalEvidenceContentEncoder` is the sole issuer of the ingested payload's
`EvidenceContentIdentity`; a snapshot never accepts a caller-supplied content
identity. This keeps `EvidenceOccurrenceIdentity != EvidenceContentIdentity`:
`snapshot_id`, `run_id`, and `authorization_id` name one acquisition
occurrence, while `content_id` is a digest over the ingested bytes, shared by
any two occurrences that ingest byte-identical content.
`BirthAssessmentRequest` further checks that its evidence snapshot's
`experiment_content_id` equals its own experiment binding's `content_id`,
rejecting a snapshot authorized under a different frozen experiment.

`AuthorizedCapture != ProofOfExternalAcquisitionChronology`: this stage does
not prove when or how evidence was first observed or produced outside this
process, and pre-existing evidence could still be ingested through an
authorized run. It also does not claim anything about evidence quality:
`AuthorizedEvidence != SufficientEvidence`, and authorized evidence does not
imply `ResidualSurvival` or `Birth`. G0.2a.3 issues no `ResidualAssessment`
and no `BirthVerdict`.

### G0.2a.3.1 — Issuer-scoped occurrence issuance integrity

G0.2a.3 alone let `authorization_id`, `run_id`, and `snapshot_id` be any
non-empty, caller-chosen string: nothing stopped
`EvidenceAcquisitionAuthority.authorize` from issuing two authorizations for
the same `authorization_id`, an authorization from opening the same `run_id`
twice, or a run from ingesting two different payloads under the same
`snapshot_id`. These strings were therefore `EvidenceOccurrenceCoordinates`
with real provenance, but not yet a proven `EvidenceOccurrenceIdentity`:
`same(id)` did not imply `same(occurrence)`, since an issuer would accept the
id again.

Each issuer now keeps its own registry of the ids it has already issued and
rejects a repeat with `EvidenceAcquisitionAuthorityError`: an
`EvidenceAcquisitionAuthority` instance tracks its issued `authorization_id`s,
one `EvidenceAcquisitionAuthorization` tracks its own issued `run_id`s, and
one `EvidenceAcquisitionRun` tracks its own issued `snapshot_id`s (rejecting a
repeat even when the later `ingest` call carries different content). Each
registry's check-and-insert is synchronized with an internal lock, so
concurrent calls on the same authority, authorization, or run instance cannot
race past the uniqueness check. This makes issuance injective within its
declared scope: two ids issued by the same issuer are equal only if they name
the same occurrence, and distinct ids issued by the same issuer always name
distinct occurrences. This is `IssuerScopedOccurrenceUniqueness`, precisely:

```
forall issuer, id:
    Issued_issuer(o1) = id and Issued_issuer(o2) = id => o1 = o2
```

This is deliberately **not** named `EvidenceOccurrenceIdentity`, because
`LocalInjectivity != PortableIdentity`: proving an id is never repeated
*within one issuer's own registry* does not prove it is never repeated
*across issuers*. Nothing in `AuthorizedEvidenceSnapshot` carries an
`issuer_scope_id`, so two distinct `EvidenceAcquisitionAuthority` instances
remain two distinct, uncoordinated issuance scopes: each is free to issue
`authorization_id="a1"`, whose `open_run("r1")` issues `run_id="r1"`, whose
`ingest(snapshot_id="s1", ...)` issues `snapshot_id="s1"`, and nothing in the
resulting snapshot's comparable fields (`snapshot_id`, `run_id`,
`authorization_id`, `experiment_content_id`, `domain`, `evidence_mode`,
`trace`) distinguishes which authority issued it. If both authorities also
share the same frozen experiment binding, payload, and trace, the two
snapshots' comparable representations coincide even though the two
acquisition occurrences are genuinely independent
(`Occurrence_A != Occurrence_B` yet
`Representation(Occurrence_A) == Representation(Occurrence_B)`). A portable
identity would require an issuer-scope identity of its own -- one that
carries its own issuance authority rather than being another caller-chosen
string -- propagated through `Authorization -> Run -> Snapshot`; that is not
built here. So the accurate judgment is:

```
IssuerScopedOccurrenceUniqueness = PROVED
PortableEvidenceOccurrenceIdentity = DEFERRED
```

`BirthAssessmentRequest` does not hold an authority or issuer-scope object
either: it only checks `snapshot.experiment_content_id ==
binding.content_id`, so it cannot and does not distinguish which authority
scope produced an otherwise-matching snapshot. This is an accepted, narrower
surface than a caller might assume from the name "occurrence identity" alone,
and is the reason this stage's claim is `IssuerScopedOccurrenceUniqueness`,
not `EvidenceOccurrenceIdentity`.

This closes `IssuerScopedOccurrenceUniqueness` only within each issuer's own
scope, not globally: two different `EvidenceAcquisitionAuthority` instances
are two different issuance scopes, and nothing proves their respective
`authorization_id`s differ from one another. `EvidenceAcquisitionAuthority()`
remains a construction boundary, not a permission or security authority --
identical to how `StructuralAdmissionGate` construction is not itself a claim
of external authorization.

`EvidenceAcquisitionRun` and `EvidenceAcquisitionAuthorization` are
`ExternallyFrozen, InternallyStatefulAuthority` objects, not plain immutable
value objects: their dataclass is `frozen=True` so their *own* declared
identity fields (`run_id`, `authorization_id`, `binding`, etc.) can never be
reassigned after construction, but each also holds a private, mutable
`_issued_*` registry `set` and a `threading.Lock` (both `compare=False`,
`repr=False`, `init=False`) as internal operational bookkeeping state. This
bookkeeping is deliberately excluded from equality, `repr`, and from any
content-identity computation (it is never hashed or serialized into
`EvidenceContentIdentity` or any experiment content identity): it exists only
to enforce this stage's issuance uniqueness, not to describe the object's own
identity or content.


G0.2 is split into smaller authority-preserving stages. G0.2a defines only
executable assessment contracts: `ResidualDefinitionSpec` identifies the
residual domain, input projection, output schema, evaluator-id declaration,
invariants, and failure semantics; each `WeakerModelSpec` binds a frozen weaker
model to its evaluator, information loss, result schema, and exact poset
relations; and `ClosureCriterionSpec` defines the local
`Close(W_i, R) ∈ {CLOSE, FAIL_TO_CLOSE, DEFER}` vocabulary for weaker-model
closure. `BirthAssessmentSemanticsContract` validates that these executable
contracts match the frozen residual-definition and closure-criterion
identities, experiment, domain, queried projection, prerequisite cone, schemas,
and poset relations. Matching only domain or schema is insufficient:
`NoResidualDefinitionDriftAfterFreeze` and
`NoClosureCriterionDriftAfterFreeze` require exact identity equality.

Evaluator ids in these contracts are declarations only:
`DeclaredEvaluatorId != AuthorizedEvaluator`. `CallerDoesNotOwnEvaluatorAuthority`
requires registry-issued definitions before those ids can become authorized for
an exact `(domain, role, target_id, evaluator_id)` scope.
`BirthAssessmentEvaluatorRegistry` and
`SealedBirthAssessmentEvaluatorRegistry` provide that sealed definition
boundary while executing no assessment. G0.2a obeys `NoVerdictYet`: it issues
no `ResidualAssessment`, `BirthCandidate`, `BirthVerdict`, `Freeze`, or E0
result.

G0.2a's id-equality checks close *label* identity, not *content* identity:
`SameId` does not imply `SameSemantics`. G0.2a.1 closes that separately.
`ResidualDefinitionId != ResidualDefinitionContentIdentity`, and the same
distinction holds for `ClosureCriterionSpec` and `WeakerModelSpec`.
`CanonicalBirthSemanticsEncoder` issues immutable canonical manifests and
`BirthSemanticsContentIdentity` digests for each; `BirthSemanticsContentRegistry`
freezes the canonical bytes of the first canonical content bound to an exact
`(domain, role, target_id)` scope, rejecting later content drift under the
same id; and `BirthAssessmentContentBinding` proves
exact canonical-byte equality for the residual definition, the closure
criterion, and every weaker model bound to a `BirthAssessmentSemanticsContract`.
This closes `NoDeclaredSemanticDigestDriftAfterFreeze`; the registry retains
the canonical bytes and binding compares those bytes directly, so it also
enforces `ExactCanonicalContentFreeze` rather than treating digest equality as
content equality. G0.2a.2 separately gives every complete
`BirthExperimentSpecification` an encoder-issued canonical manifest and
content identity, covering its revision, evidence mode, domain, poset, query
and hypothesis, residual/closure declarations, and evidence requirements.
`PreEvidenceSpecificationRegistry` alone issues a
`FrozenPreEvidenceExperimentManifest`; semantic-registry sealing requires that
manifest, so a semantic snapshot cannot float independently of its frozen
experiment specification. All canonical encoders enforce schema coverage:
every declared field is either encoded or listed as an explicit derived
exclusion, including `ProjectionPoset`, `BirthQuery`, and
`StructureHypothesis`; adding an unaccounted field rejects encoding. It still
performs no evaluation and
issues no birth authority. `EvaluatorId != EvaluatorImplementationIdentity`
remains open: this stage authorizes evaluator *declarations*, not evaluator
*implementations*, and any future runtime must resolve evaluator execution
through a registry-owned implementation bound to an approved content
identity, never a caller-supplied callable.

Later G0.2 stages alone may implement the complete authority chain:
`BirthAssessmentRequest -> ResidualAssessment ->
LicensedWeakerExhaustion -> NecessaryInvariantCandidate -> BirthCandidate ->
IndependentClosureDecision -> gate-issued BirthVerdict -> Freeze -> E0`.
That gate must assess every relevant incomparable model itself; callers cannot
omit a competitor or promote string placeholders as discriminating evidence.
It must keep `Freeze` distinct from the subsequent `E0` assessment. No
Arabic-specific type is part of G0.1 or this deferred G0.2 design.

## G0.F — Factorization-First Ontology (declared law, no runtime yet)

G0's chain as written above reads as *one* candidate object, closed
independently and frozen. That phrasing is a special case, not the general
law: a domain `L`'s residual over everything frozen prior to experiment
(`K_L`) does not name in advance how many candidate objects, or which ones,
would close it. Requiring `Residual(O_L | K_L) = 0` may force a single
factor, several jointly-necessary factors, or none at all
(`NO_BIRTH_IN_SCOPE`). This section restates G0's chain, for any domain `L`,
as closing a **minimal sufficient irreducible factorization** rather than a
single named object, and it is held to the same discipline as G0: **law
only**, ahead of any runtime, ahead of any Arabic-specific folder structure,
and ahead of any decision about how many factors traditional grammar expects.

```
K_L -> Residual(O_L | K_L) -> candidate factorizations F (poset-ordered)
    -> Sufficiency(F) & FamilyMinimality(F) & ComponentIrreducibility(F)
    -> IndependentClosure -> BirthVerdict -> Freeze(F*) -> Bridge stage -> E0
```

`Bridge stage`: once (and only once) two factors are each independently
frozen, a *separate* birth protocol -- not automatic adjacency -- decides
whether any relation between them is itself born or merely derived. `E0`
here names a mapping graph from the frozen factor/bridge network to external
(traditional) terminology, not a single rename step. Neither the
factorization runtime nor the bridge runtime nor the E0-mapping runtime is
implemented by this section; as with G0, only the constraints they must
satisfy are frozen now.

| Law | Status | Scope |
| --- | --- | --- |
| `NoTraditionalSchemaBeforeFactorization` | DECLARED_DEFERRED | A domain `L`'s factorization is discovered from `Residual(O_L \| K_L)`, never assumed from a traditional grammatical schema (for example, a presumed phonology/morphology/syntax/semantics split) before that residual is examined. A traditional category name may describe a result after `E0`; it must never seed or constrain the search for one. |
| `NoPredeterminedFactorCount` | DECLARED_DEFERRED | No experiment, spec, or runtime may fix in advance how many factors a domain's minimal factorization contains. `Residual(O_L \| K_L) = 0` licenses `NO_BIRTH_IN_SCOPE` for the whole domain; a nonzero residual licenses exactly the factor family the closure proof produces, whether that is one factor, several, or (pending further evidence) none yet decidable. |
| `FactorizationMinimalityIsPartialOrderRelative` | DECLARED_DEFERRED | The set of admissible minimal factorizations for `L` is `M_L = Min_{≺_L}{F : Sufficient_L(F) and Closed_L(F)}`, where `≺_L` is the domain's frozen partial order over candidate factor families and `Min` selects its minimal elements. `M_L` is never computed as `argmin` of a linear/scalar complexity measure: `ProjectionIsNotOntology`'s ban on assuming a total-order complexity vector across projections applies equally here to factor families. |
| `MultipleIncomparableMinimalFactorizationsDefer` | DECLARED_DEFERRED | If `\|M_L\| > 1` and two members of `M_L` are pairwise incomparable under `≺_L` (neither is derivable from, nor a refinement of, the other under currently licensed weaker models), no verdict may pick one: the assessment is `DEFER_IN_SCOPE`, mirroring `NoRicherStructureBeforeLowerOpenResidualClosure`'s treatment of an incomparable competing explanation, until discriminating evidence resolves the competition. |
| `DerivedRelationDoesNotBirth` | DECLARED_DEFERRED | A relation between two already-frozen factors `F_i`, `F_j` is not itself a candidate for birth merely because both endpoints exist. If the relation's value is fully reconstructible from `F_i`, `F_j`, and shared already-frozen context (`ReconstructibleRelation => Derived, not Born`), it is recorded as a derived relationship (`D*`), not promoted to an ontology object, regardless of how useful or traditionally named that relationship is. |
| `NoBridgeBeforeIndependentEndpointFreeze` | DECLARED_DEFERRED | A `BridgeResidualExperiment(F_i, F_j)` may only be opened after both `F_i` and `F_j` have each already completed their own independent `Freeze`. Endpoint existence as an in-progress candidate, hypothesis, or unclosed factor never licenses opening a bridge experiment between them. |
| `NoBridgeBirthIfReconstructible` | DECLARED_DEFERRED | Given frozen `F_i`, `F_j`, and shared context, if every licensed weaker reconstruction model accounts for the coupling between them (residual `R_ij = 0`), the relation is `DERIVED`, not a `BridgeCandidate`. Only a coupling residual that survives every licensed weaker reconstruction model (`R_ij != 0` after exhaustion) may proceed to `BridgeCandidate -> IndependentClosure -> Freeze`, mirroring `NoBirthBeforeLicensedWeakerExhaustion` for bridges. |
| `FrozenFactorReopeningRequiresNewRevision` | DECLARED_DEFERRED | A frozen factor's content is fixed at freeze time and is never silently mutated by later evidence. New evidence bearing on an already-frozen factor opens a new, separately recorded revision (mirroring `NoBirthBeforeLicensedWeakerExhaustion`'s treatment of a newly discovered weaker model); it does not erase, edit in place, or retroactively rewrite the original frozen verdict's historical scoped record. |
| `LayerIsDiscoveryJurisdictionNotOntology` | DECLARED_DEFERRED | A domain `L` (however named -- "encoding," "phonology," "morphology," or otherwise) denotes only the scope of experiment, evidence, and residual under examination: a `DiscoveryJurisdiction`, not a promise that factorization will reproduce any traditional layer boundary. A single born factor may cut across what tradition calls two layers, or one traditional layer may fracture into several independently born factors; neither outcome is a failure of this law. |
| `E0IsExternalAuditOnly` | DECLARED_DEFERRED | `E0` maps the frozen factor/bridge network to external (traditional or reference) terminology for audit and communication only. `E0` certifies no birth, closure, or freeze decision, and a factor's or bridge's epistemic status never depends on whether, or how, `E0` maps it to an external name. |
| `E0MappingMayBePartialAndManyToMany` | DECLARED_DEFERRED | The `E0` mapping `Π^E0 : FrozenDiscoveryGraph ⇀ ExternalConceptGraph` is a partial relation, not a total function: an entry may be one-to-one, one-to-many, many-to-one, or absent entirely (a frozen factor with no traditional counterpart, or a traditional term matching no single frozen factor). An unmapped frozen factor, or a traditional term left unmatched, is not itself evidence against either side. |
| `RuleTableIsDerivedArtifact` | DECLARED_DEFERRED | Any future "Arabic rule table" is a compiled, read-only projection of the frozen factor set, frozen bridge set, derived-relation set, and `E0` mapping (`ArabicRuleTable = Compile(F*, B*, D*, Π^E0)`), produced strictly after those inputs are frozen. It is never hand-authored ahead of, or independently of, that frozen network. |
| `NoRuleTableFeedbackIntoDiscovery` | DECLARED_DEFERRED | A compiled rule table, or any traditional inventory or category count it reflects, may never feed back into an open experiment, residual criterion, weaker-model set, or factorization search (`ArabicRuleTable ↛ Discovery`, `TraditionalInventory ↛ FactorCount`, `TraditionalCategory ↛ ResidualCriterion`). Discovery in progress must not be steered toward reproducing a table that has not yet been compiled from it. |
| `NoOracleLabelCriterionOrFunctionLeakBeforeFreeze` | DECLARED_DEFERRED | No caller-supplied oracle label, closure criterion, or evaluator function/callable may be substituted for, or silently override, the frozen residual definition, closure criterion, or weaker-model specifications bound at G0.1/G0.2a, for any stage of factorization, bridge, or `E0` assessment. This extends `EvaluatorId != EvaluatorImplementationIdentity` and `CallerDoesNotOwnEvaluatorAuthority` (G0.2a) to the factorization and bridge stages: a caller may declare which evaluator it expects, but never supply, swap, or leak the executing implementation itself ahead of a sealed registry's authorization. |

These fourteen laws are declared now, before any factorization runtime,
`EvaluatorImplementationIdentity`/execution-authority stage (itself still
open per `EvaluatorId != EvaluatorImplementationIdentity` above), typed
residual/provenance stage, bridge-assessment stage, or `E0`-mapping-audit
stage exists. As with G0, no Arabic-specific `phonology`/`morphology`/
`syntax`/`semantics` (or similarly pre-committed) module or folder is created
by this section, and none should be created merely to anticipate a
factorization that has not yet been discovered
(`LayerIsDiscoveryJurisdictionNotOntology`). This section governs, but does
not implement, the milestones that must be built to close it.

### G0.F.1 — Fractal reopen protocol (declared law, contracts only)

G0.F above closes one experiment's factorization question. Fractality is not
a folder layout; it is the same execution law applied recursively: a frozen
result from one experiment must be capable of being read, unmodified, inside
a *later, higher* experiment, without being reborn, copied, or having its
identity re-decided:

```
Birth -> Freeze -> Reopen -> Residual -> MinimalFactorization
-> Freeze -> Reopen -> ...
```

Formally, for a jurisdiction (domain) `L` at level `n`, given the already
frozen set `F_n = {F_1, ..., F_m}` opened in a new jurisdiction `J_{n+1}`:

```
W_0 = Reopen(F_n) + KnownDerivedRelations
R_{n+1} = Residual(O_{n+1} | W_0)
```

`R_{n+1} = 0` licenses `NoBirthAtReopen`: reopening never forces a new layer
to appear. Otherwise the next frozen layer is exactly:

```
F_{n+1} = Freeze(MinimalFactorization(Residual(O_{n+1} | Reopen(F_{<=n}))))
```

which is itself immediately reopenable, making the recurrence indefinite.
Every higher-layer result is exactly one of three kinds, and the three are
never conflated: a `BornFactor` (irreducible under every licensed weaker
reconstruction), a `DerivedRelation` (reconstructible from already-frozen
factors and shared context; `DERIVED_NO_BIRTH`, per `DerivedRelationDoesNotBirth`
above), or a `BornBridge` (a coupling between two independently frozen
factors that survives every licensed weaker reconstruction model). So:

```
FractalGraph = FrozenFactors + DerivedRelations + BornBridges
```

| Law | Status | Scope |
| --- | --- | --- |
| `BirthOnceFreezeOnceReopenMany` | DECLARED_DEFERRED | A factor is born and frozen exactly once; after that, every later experiment that needs it must `Reopen` that one frozen result rather than re-run its birth. Nothing licenses a second, independent birth of what is content-identically the same factor inside the same scope. |
| `ReopenDoesNotRebirth` | DECLARED_DEFERRED | `Reopen(FrozenFactorRef, E_{n+1})` opens a read-only, licensed window onto an already-frozen factor for use in a new experiment; it is not a second construction of that factor and issues no new `BirthVerdict` for it. Formally `Reopen(F) != Rebirth(F)` and `Id_after(F) == Id_before(F)`: reopening a factor can never change the factor's own declared identity, only license a new question about it. |
| `NoBridgeForSequentialInquiry` | PROVED (at contract level) | A later question about a frozen factor is represented only by `ReopenExperimentSpecification` and, once its result is frozen, `ProofLineageEdge`. A proof-lineage edge records discovery history and is not accepted as a `BornBridgeRef` or `DerivedRelationSpec`. |
| `ParentageIsNotOntologicalRelation` | PROVED (at contract level) | `FractalSnapshot` keeps `proof_lineage_edges` separate from `born_bridges` and `derived_relations`: parentage belongs exclusively to the provenance graph and cannot populate the born ontology or derived-relation graphs. |
| `ProofLineageGraphIsAcyclic` | PROVED (at contract level) | `FractalSnapshot` rejects any cycle in `proof_lineage_edges`, including indirect cycles; reopening an ancestor remains valid because it does not add a reverse ancestor edge. |
| `LineageEdgeBindsExactReopenSpecification` | PROVED (at contract level) | Every `ProofLineageEdge` carries one exact `ReopenExperimentSpecification`; the child birth experiment and declared parent are checked against that specification, with no duplicated lineage identity strings. |
| `FrozenOntologyRefIncludesBornBridge` | PROVED (at contract level) | Reopen and proof-lineage parent references may be either `FrozenFactorRef` or `BornBridgeRef`; `DerivedRelationRef` is not an ontology reference and cannot become a lineage parent. |
| `DistinctBridgeExperimentFromEndpointExperiments` | PROVED (at contract level) | `BornBridgeRef` requires a bridge birth experiment identifier distinct from every endpoint birth experiment identifier. This is identifier-level contract evidence only; independent endpoint birth remains deferred until freeze authority exists. |
| `BridgeRequiresIndependentEndpointBirth` | DECLARED_DEFERRED | Independent endpoint birth requires authority to prove the ordering `Freeze(F_i) < BridgeExperiment`; caller-constructible references and distinct identifiers cannot establish that authority claim. |
| `BridgeRequiresResidualBeyondEndpointReconstruction` | DECLARED_DEFERRED | A future bridge gate may freeze a `BornBridgeRef` only after its own G0 experiment shows a coupling residual beyond both endpoints and shared frozen context; a zero residual produces `DerivedRelationSpec`, never a bridge. |
| `NoUpstreamIdentityMutation` | DECLARED_DEFERRED | If `F_i` is frozen, no later result `G` computed from a `Reopen` of `F_i` may modify `F_i`, rename it, reinterpret its identity, merge it with another frozen factor, or change its rank. `G` may only carry `ParentRef(G, F_i)`; new evidence that bears on `F_i` opens a new revision on `F_i` itself (`NewEvidence => NewRevision != HistoricalOverwrite`, consistent with `BirthExperimentSpecification.revision_id`/`revision_sequence`), never a retroactive edit performed by `G`. |
| `HigherExperimentHoldsRefsNotCopies` | DECLARED_DEFERRED | A higher-level experiment or result holds a `FrozenFactorRef` (`factor_id`, `factor_content_id`, `freeze_certificate_id`, `domain`, `birth_experiment_id`, `birth_revision_id`) to a parent factor, never a reconstructed or mutable copy of the parent's own content. `HigherLayerOwnsReference != HigherLayerOwnsIdentity`: owning the reference grants no authority over the referenced factor's identity. |
| `NoTraditionalLayerEnum` | DECLARED_DEFERRED | No fixed enumeration of traditional layers (for example `ORTHOGRAPHY`/`PHONOLOGY`/`MORPHOLOGY`/`SYNTAX`/`SEMANTICS`) may be declared as a closed type in the kernel or Arabic runtime. A domain `L` is identified only by its own frozen experiment/jurisdiction scope (`Layer = FrozenExperimentJurisdiction`); two jurisdictions may later be shown to share a factor without that implying either was ever a case of the other. |
| `FractalParentageDoesNotDefineIdentity` | DECLARED_DEFERRED | A `FractalProvenancePath` records which frozen factors, bridges, derived relations, and reopen experiments produced a later result, strictly for audit and reconstruction of the proof path. `Parentage != Identity`: this path is never part of the later result's own declared identity or content identity, and two results with identical content but different provenance paths remain distinct occurrences, exactly as `EvidenceOccurrenceIdentity != EvidenceContentIdentity` already separates occurrence from content elsewhere in this kernel. |
| `RevisionDoesNotEraseHistoricalFreeze` | DECLARED_DEFERRED | Restates `FrozenFactorReopeningRequiresNewRevision` (G0.F above) at the fractal-reopen level: new evidence discovered through a `Reopen` never edits, deletes, or silently supersedes a parent's historical frozen record. `ContentIdentity_new(F) == ContentIdentity_old(F)` is required for any claim that a later step merely *reopened* `F`; a change in `F`'s own content identity is not a reopen at all -- it is a new revision or a new birth, recorded separately. |
| `ExactFrozenReferencePreservation` | PROVED (at contract level) | `FractalSnapshot` checks a derived relation's or bridge's referenced factor against the *exact* `FrozenFactorRef` recorded in the snapshot -- every declared field (`factor_id`, `factor_content_id`, `freeze_certificate_id`, `domain`, `birth_experiment_id`, `birth_revision_id`), never against a bare `factor_id` string. A reference sharing a `factor_id` but differing in content id, domain, birth experiment/revision, or freeze certificate names a different, unrecognized occurrence and is rejected. `factor_id` equality alone is never sufficient membership proof. |
| `ReopenComposesG0DoesNotForkG0` | PROVED (at contract level) | `ReopenExperimentSpecification` embeds one ordinary, complete `BirthExperimentSpecification` (`experiment`) rather than redeclaring its own `new_question`/`residual_definition`/`closure_criterion` fields. This preserves G0's own revision identity, `EvidenceMode`, `ProjectionPoset`, `BirthQuery`, residual/closure identities, and derived prerequisite cone verbatim, so reopen semantics cannot drift from G0 semantics over time (`G0SemanticsDriftBetweenBirthAndReopen` is closed, not merely avoided by convention). Reopen uses G0; Reopen does not fork G0. |
| `DerivedRelationProvenanceIsContentBound` | PROVED (at contract level) | `FractalProvenancePath.derived_relation_refs` holds `DerivedRelationRef` values (`relation_id` plus `derivation_content_id`), never bare `relation_id` strings. `SameRelationId != SameDerivationSemantics`: two derivations that happen to reuse the same `relation_id` but disagree on `derivation_content_id` are distinguishable, so drift in a derived relation's own recorded content is detectable from its provenance rather than silently trusted by id alone. |

`FrozenFactorRef`, `BornBridgeRef`, `DerivedRelationSpec`,
`DerivedRelationRef`, `ReopenExperimentSpecification`,
`FractalProvenancePath`, `ProofLineageEdge`, and `FractalSnapshot`
(`src/alghanem/kernel/fractal.py`) are contract *skeletons* only: their
constructors validate internal well-formedness (non-blank identities,
non-empty/non-duplicate parent or endpoint sets, exact-reference membership,
and so on), exactly as `BirthExperimentSpecification` and its G0.2a siblings
do ahead of any executable assessment runtime. None of them is issued by a
freeze or reopen authority yet, because no such authority exists: a caller
can construct a syntactically valid `FrozenFactorRef` by hand today, which
proves only that the contract is well-formed, never that a factor was
actually born, closed, and frozen (`ConstructibleContract != IssuedByAuthority`,
equivalently `WellFormedFrozenFactorRef != AuthorityIssuedFrozenFactorRef`).
No code anywhere in the kernel may treat successful construction, or a
passing `isinstance(x, FrozenFactorRef)` check, as proof that a genuine
freeze occurred. A future `FreezeAuthority`/`ReopenAuthority` -- analogous to
`EvidenceAcquisitionAuthority`'s sole-issuer pattern -- is a separate, later
milestone; only that authority may make an issued `FrozenFactorRef`
trustworthy. `FractalSnapshot` contains no `ArabicRuleTable` and no other
compiled artifact; per `RuleTableIsDerivedArtifact` above, any such table
remains a strictly later, derived projection of a frozen snapshot like this
one.

## Encyclopedia Nucleus — Constitution

The encyclopedia is an application consumer of the kernel, never a replacement
for it. Its minimal state is:

```
EncyclopediaNucleusSnapshot = FractalSnapshot + GrowthFrontier
GrowthFrontier = RootInquiries + ReopenInquiries
```

`FractalSnapshot` remains a discovery graph, not a knowledge graph. It holds
only frozen discovery contracts, whose construction remains non-authoritative
until the future birth and freeze authorities exist. The frontier holds open
questions. Frontier immutability is a contract property; preserving an inquiry
after a `DEFER` verdict is deferred until a growth transition mechanism exists.

| Law | Status | Scope |
| --- | --- | --- |
| `NoDedicatedTraditionalSchemaFields` | PROVED (at contract level) | The encyclopedia namespace has no dedicated domain, ontology, or human-science label fields. |
| `NoSemanticLabelLeakThroughIdentifiers` | DECLARED_DEFERRED | Identifiers are opaque keys, not semantic evidence; a future registry and evaluator authority must ensure their values cannot influence discovery. |
| `QuestionGenerationIsNotAuthorization` | PROVED (at contract level) | `QuestionProposal` has no experiment or execution field. `RootInquiry` requires a `BirthExperimentSpecificationContentBinding`, which proves its complete G0 specification exactly matches registry-frozen pre-evidence content. |
| `QuestionGrowthUsesReopen` | PROVED (at contract level) | Later questions around frozen results are represented by kernel `ReopenExperimentSpecification`; sequential inquiry is not an ontological bridge. |
| `FrontierReopenParentMustExistInSnapshot` | PROVED (at contract level) | Every reopen parent in the frontier must exactly equal a frozen factor or born bridge reference present in the paired `FractalSnapshot`; identifier equality alone is insufficient. |
| `FrontierImmutability` | PROVED (at contract level) | The frozen frontier contract cannot be mutated after construction. |
| `DeferPreservesOpenQuestion` | DECLARED_DEFERRED | A future `EncyclopediaGrowthTransition` must retain an inquiry after a `DEFER` result; no verdict-to-frontier transition exists yet. |
| `NoKnowledgeBeforeLicensedClaim` | PROVED (at contract level) | The nucleus contains no claim or knowledge fields. Frozen factors are not knowledge states. |
| `NoTextBeforeKnowledgeProjection` | PROVED (at contract level) | The nucleus contains no article or text fields; rendering is a later projection and cannot create knowledge. |
| `NoIndexFeedbackIntoDiscovery` | DECLARED_DEFERRED | A future index or renderer may project licensed knowledge but may not authorize or alter discovery. |

`src/alghanem/encyclopedia/inquiry.py`,
`src/alghanem/encyclopedia/frontier.py`, and
`src/alghanem/encyclopedia/snapshot.py` intentionally define no growth engine,
domain taxonomy, knowledge graph, article store, or evaluator authority.
`EncyclopediaGrowthTransition` is the deferred future boundary for applying
authorized kernel outcomes to a nucleus snapshot.

## Encyclopedia Self-Observation — Constitution

`Alghanem` is not exempt from its own encyclopedia's discipline: the
repository the encyclopedia is implemented in is itself a legitimate future
`ObjectOfInquiry`. But a four-way separation must hold before any claim
about the repository can be licensed as knowledge:

```
System != RepositoryRepresentation != SelfModel != KnowledgeAboutSystem
```

A GitHub repository is a `SourceArtifact` carrying traces of the system; a
commit is one exact `SourceVersion`; a file is a `SourceFragmentCarrier`;
a line, node, or function is an `EvidenceCandidate`
(`CodeFragment != Evidence` until a future claim-specific
`EvidenceBinding` exists). This module intentionally goes no further than
naming these carriers:

```
RepositorySnapshot -> Evidence -> Claim -> EpistemicLicensing -> SelfKnowledge
```

`src/alghanem/encyclopedia/self_observation/` defines only the first link,
`RepositorySnapshotRef` plus the artifact/fragment/transition refs anchored
to it. It defines no `Claim`, `EvidenceBinding`, or `SelfEpistemicState`
runtime; those remain a later, separate `SelfKnowledgeBridgeExperiment`
milestone, built only once a claim/evidence constitution exists.

| Law | Status | Scope |
| --- | --- | --- |
| `RepositorySnapshotIsNotKnowledge` | PROVED (at contract level) | `RepositorySnapshotRef` has no claim, evidence, or knowledge field; it names one explicitly-addressed repository state and nothing else. |
| `RepositoryArtifactIsNotEvidenceByItself` | PROVED (at contract level) | `RepositoryArtifactRef` and `RepositoryFragmentRef` name a file or fragment carrier only; naming a fragment proves nothing about any claim until a future `EvidenceBinding` exists. |
| `DocumentationIsNotImplementation` | DECLARED_DEFERRED | A future claim constitution must keep `DeclaredSelfModel` (from `docs/CONSTITUTION.md` and other prose) distinct from `ImplementedSelfModel` (from source); this module records neither yet. |
| `TestPassIsNotUniversalTruth` | DECLARED_DEFERRED | A future evidence constitution must keep `TestedSelfModel` (from passing tests/CI at one commit) distinct from `FormalProofEvidence` and from universal correctness; no test-evidence field exists yet. |
| `SelfModelIsNotSystem` | PROVED (at contract level) | `RepositorySnapshotRef`, `RepositoryArtifactRef`, `RepositoryFragmentRef`, and `RepositoryTransitionRef` are all references anchored to a commit; none of them is, contains, or executes the repository itself. |
| `SelfDescriptionDoesNotGrantAuthority` | PROVED (at contract level) | This module defines no freeze, reopen, or mutation authority; constructing or observing any of its refs grants no permission to alter the kernel or encyclopedia they describe. |
| `RepositoryVersionMustBeContentBound` | CONSTITUTIONAL REQUIREMENT | Every ref in this module is anchored to an explicit `commit_sha` (never a branch name); `RepositoryArtifactRef` and `RepositoryFragmentRef` are anchored to their exact snapshot, and `RepositoryTransitionRef` requires distinct `from_snapshot`/`to_snapshot` commit shas. This requirement is only *proved* at the weaker `RepositoryVersionIsExplicitlyAddressed` level below; full content authentication remains `RepositoryVersionIsContentAuthenticated` (DECLARED_DEFERRED). |
| `RepositoryVersionIsExplicitlyAddressed` | PROVED (at contract level) | `RepositorySnapshotRef` and `RepositoryArtifactRef` require non-blank `commit_sha`/`tree_sha`/`blob_sha` fields, each anchored to an explicit version, never a bare identifier without context. |
| `RepositoryVersionIsContentAuthenticated` | PROVED (within provider scope) | `RepositoryObservationAuthority` opens an authority-issued `RepositoryObservationRun`; the run verifies repository→commit→tree and tree/path→blob, and issues authenticated snapshots/artifacts only after those checks. This remains scoped to the provider's returned observations, not universal repository truth. |
| `SameRepositoryIdentity` | PROVED (at contract level) | `RepositoryTransitionRef` requires `from_snapshot.repository_identity == to_snapshot.repository_identity`; a pair naming two different repositories is rejected, not silently accepted as a transition. |
| `DifferentCommitsIsNotHistoricalTransition` | PROVED (within provider scope) | `RepositoryTransitionRef` remains address-only; an `AuthenticatedRepositoryTransition` requires two authenticated snapshots from the same observation run and a provider ancestry witness. Distinct commit shas alone remain insufficient. |
| `AuthenticatedObservationIsNotEvidence` | PROVED (at contract level) | Authenticated snapshots, artifacts, fragments, and transitions contain no claim or evidence binding; authentication of repository structure does not make an observation evidence or knowledge. |
| `ProviderDeclaredImplementationIdIsNotExecutionIdentity` | DECLARED_DEFERRED | `implementation_identity` is provider-declared provenance metadata. This milestone does not independently bind that string to the implementation that executed the run. |
| `ArtifactChangeRecordsBothSides` | PROVED (at contract level) | `RepositoryArtifactChangeRef` requires both a `before` (anchored to `from_snapshot`) and an `after` (anchored to `to_snapshot`) `RepositoryArtifactRef`, sharing the same `artifact_path` with distinct `blob_sha`s, so a delta can be reconstructed instead of only naming the post-change file. It also independently requires `before.snapshot.repository_identity == after.snapshot.repository_identity` and distinct `commit_sha`s, so a well-formed change pair is coherent even when constructed outside a `RepositoryTransitionRef`. |

`RepositoryTransitionRef` records `changed_artifacts` (as
`RepositoryArtifactChangeRef` before/after pairs), `added_artifacts`, and
`removed_artifacts` between two explicitly-addressed snapshots of the *same*
repository, but `Change != Improvement`: it makes no claim that a later
commit is better, safer, or more correct than an earlier one.
`RevisionDoesNotEraseHistoricalFreeze` follows directly from
`RepositoryVersionMustBeContentBound`: a later snapshot never invalidates
what a licensed claim once said about an earlier one, because the two are
distinct, equally addressable versions. A path renamed or moved between
`from_snapshot` and `to_snapshot` (`SameContent+DifferentPath`) is
deliberately out of scope for `RepositoryArtifactChangeRef`, which requires
an identical `artifact_path` on both sides; a future
`RepositoryArtifactMoveCandidate` would carry that separate identity
question.
