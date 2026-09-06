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
cone, and a later `BirthAssessmentRequest` that binds the evidence snapshot.
`BirthCandidate` is distinct from a scoped birth verdict and from `Freeze`;
only `BIRTH_IN_SCOPE` may proceed through freeze and an `E0` step. See the
"G0 — Birth Protocol" section of
`docs/CONSTITUTION.md` for the full declared laws; no `BirthGate`,
rank/complexity runtime, or intervention runtime exists yet.

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
