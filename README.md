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

The first Arabic layer, `ArabicSymbolEncodingV1`, is independent of grammar.
It discovers carrier identities, combining-state identities, their separately
born bindings, and normalized canonical surface encodings before freezing an
exactly 29-by-4 symbolic foundation. Linguistic names and grammatical concepts
remain outside this layer.

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
