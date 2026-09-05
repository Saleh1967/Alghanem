# Alghanem

Alghanem is a research codebase for a general algebra of licensed
transformations. The current release is the language-agnostic **Kernel v0.1**:
small, shallowly immutable data structures for anchors, operations, evidence,
traces, residuals, and certified transition outcomes.

Arabic linguistic layers are intentionally deferred. Concepts such as carriers,
morphology, syntax, and identity certificates will be added only after the
foundational kernel has been independently tested.

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
