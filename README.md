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

The next quotient artifact is `NormalizationFiberCandidate`: a derived
equivalence class of ledger audits that share one normalized
`SurfaceAtomCandidate`. Fibers record occurrence counts and raw surface
variants without replacing the occurrence ledger and without introducing
Carrier, State, binding, or Arabic cardinality claims.

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
