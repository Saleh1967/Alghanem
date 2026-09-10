# Alghanem

Alghanem is a research codebase for a general algebra of licensed
transformations. The current release is the language-agnostic **Kernel v0.1**:
small, shallowly immutable data structures for anchors, operations, evidence,
traces, residuals, and certified transition outcomes.

Kernel v0.1 only proves `StructurallyAdmissibleTransition`: a transition that
is well-formed under the kernel's structural laws. It deliberately does not
yet prove evidential sufficiency, domain-transition authority, or
inter-layer authority; a `LicensedTransition` — carrying those additional
guarantees — is a future gate, not a synonym for structural admission. What a
candidate claims to be (its `TransitionKind`) is likewise kept distinct from
any certified outcome. See `docs/CONSTITUTION.md` for the full law-by-law
status.

G0.OB.1 bridges a source-specific, authority-issued authenticated observation
to a kernel `AuthenticatedObservationBinding`; identifiers alone never
constitute authentication. G0.EB.1 then adds a claim-relative
`EvidenceRoleCandidate` over that binding, a `ClaimCandidate`, and an opaque
`EvidenceRoleRef`. It does not judge applicability, sufficiency, truth, or
knowledge: authentication or a proposed role does not by itself make an
observation evidence for a claim.

Bindings are source-bound authenticated coordinates, not portable observation
identities; portable identity remains deferred.

G0.EA.1 assesses an existing `EvidenceRoleCandidate` only for applicability in
the claim's scope. Its gate-issued `EvidenceApplicabilityAssessment` is
`PASS`, `BLOCK`, or `DEFER`, with reason, trace, residuals, and the identities
of its frozen specification and sealed evaluator registry. Evaluators are
authority-issued and bound to the candidate's role and claim scope. The gate
selects the weakest declared model that closes applicability rather than
aggregating every model's worst status. This stage does not assess sufficiency,
truth, licensed-claim status, or knowledge.

The initial Arabic layer is limited to `RawSurfaceObservation` and
`SurfaceNormalization`. It emits versioned normalization traces, residuals,
and uninterpreted surface-atom candidates. `ObservationAuditLedger` preserves
every occurrence under measurement-protocol-supplied source and occurrence
identities; distinct candidates are only a derived projection. It does not
infer identities, bindings, Arabic cardinalities, or grammatical concepts;
those require separate future birth gates and a later E0 audit.

P0.1 freezes measurement authority with `MeasurementProtocolSpec`,
`MeasurementRunIdentity`, `MeasurementRunManifest`, and
`ObservationLedgerManifest`. An observation provenance must name its measurement
run, and manifests bind an audit ledger to one run plus the run's declared
normalization policy and Unicode database version before later factorization or
identity-birth gates may consume it.

The next audit artifact is `NormalizationResidualTable`: an occurrence-complete
derived table with one row per audit, including unchanged rows, raw and
normalized codepoint sequences, atom counts, prefix/suffix delta boundaries,
removed/inserted segments, and the current candidate surface. The weaker
`NormalizationEquivalenceProjection` remains only a quotient projection over
equal normalized `SurfaceAtomCandidate`s; it is not a born object and does not
introduce Carrier, State, binding, or Arabic cardinality claims.

G0 freezes the birth protocol itself, ahead of any experiment: before any new
Arabic candidate, factor, or structural coordinate may be born, either a
measured residual (empirical mode) or an exhaustive proof over a declared
finite formal domain (formal mode) — never a synthetic-intervention artifact
alone — must survive exhaustion of every weaker model licensed and frozen for
that experiment. G0.1 supplies a language-agnostic pre-evidence
`BirthExperimentSpecification` with a `BirthQuery`, a derived prerequisite
cone, stable residual/closure identities, and a later
`BirthAssessmentRequest` that binds the evidence snapshot. G0.1 stops at that
request: it has no birth-verdict or freeze authority. G0.2a adds executable
residual, weaker-model, and closure contracts that must match the frozen
residual/closure identities. Evaluator ids in those contracts are declarations
only unless a sealed evaluator registry authorizes the exact scope, and
G0.BV.1 remains deferred: no runtime birth-verdict authority exists until an
assessment authority, `BirthCandidate`, and `IndependentClosure` exist.
`BirthCandidate` is distinct from a scoped birth verdict and from `Freeze`;
the future G0.BV.1 authority may issue `BIRTH_IN_SCOPE`, then a later freeze
authority may freeze it before a separate `E0` step. See the
"G0 — Birth Protocol" section of
`docs/CONSTITUTION.md` for the full declared laws; no `BirthGate` or
rank/complexity runtime exists yet. A non-linguistic
`SurfaceAtomIntervention`/`SurfaceInterventionTrace` runtime does exist
(`src/alghanem/arabic/encoding/intervention.py`), but per
`InterventionOperationIsNotOntology` and
`SyntheticInterventionMayGenerateHypothesisOnly` it is an explicit,
non-exhaustive experimental tool that can license at most a hypothesis, never
a `BirthGate` verdict on its own.

For bounded card-level review, the repository also includes
`src/alghanem/arabic/external_audit.py` with a golden example at
`examples/external_audit/man_2_255.yaml`. This auditor is explicitly
non-authoritative (`ExternalAuditor != KernelAuthority`): it emits only
external audit status (`نتيجة_التدقيق_الخارجي`), derives
`مخروط_الأضعف_المشتق` from the frozen projection poset (rejecting
caller-declared weaker cones), reports all competing readings, and exposes
explicit `حالة_إغلاق_Down_E`/`سبب_حالة_إغلاق_Down_E` fields.
`علاقة_بالنموذج_المختبر` is a closed vocabulary — `غير_متعينة`,
`أضعف_صوريًّا`, `مكافئ_صوريًّا`, `غير_قابل_للمقارنة` — and any other text
(a misspelling or an invented term) is rejected instead of silently counting
as a resolved relation. Following
`NoRicherStructureBeforeLowerOpenResidualClosure`, an incomparable competing
reading defers unless the card declares `تفسير_منافس_كامل: false`; when the
flag is absent or true the reading still blocks, because an incomparable
projection that offers a complete competing explanation is unresolved until
discriminating evidence exists. Card text is
compared through `comparison_key`, an orthography-insensitive key (NFC plus
removal of combining marks, invisible formatting characters, and `TATWEEL`,
plus `ALEF`/`ALEF MAQSURA`/`TEH MARBUTA` folding), so an optional diacritic or
an invisible character can no longer turn a deferred relation into a passing
one; the key is used only for comparison and never replaces the card's own
reported text.

G0.F declares, ahead of any runtime, that factorization is the general case
of birth (a domain may close with one factor, several jointly-necessary
factors, or none) and that fractality is a law, not a folder layout: a
frozen factor must be reopenable inside a later, higher experiment without
being reborn, copied, or renamed. G0.F.1 adds contract skeletons for that
reopen protocol —`FrozenFactorRef`, `BornBridgeRef`, `DerivedRelationSpec`,
`ReopenExperimentSpecification`, `FractalProvenancePath`, `ProofLineageEdge`, and
`FractalSnapshot` (`src/alghanem/kernel/fractal.py`) — but issues none of
them from any authority yet: constructing one only proves it is
well-formed, never that a factor was actually born and frozen. See the
"G0.F" section of `docs/CONSTITUTION.md` for the full declared laws.

## Development

```bash
python -m pip install -e '.[dev]'
pytest
ruff check .
ruff format --check .
mypy src
```

See [`docs/CONSTITUTION.md`](docs/CONSTITUTION.md) for the initial
constitutional laws governing the kernel.
