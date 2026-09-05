"""Canonical transition content identity.

``StructuralAdmissionGate`` issues each ``StructurallyAdmissibleTransition``
an opaque, run-specific ``admission_id``: a fresh ``uuid4().hex`` per
admission. That is deliberate -- it prevents accidental replay across
separate admissions -- but it also means two admissions of *the same
structural content*, today or a year from now, never share an identity:
``OccurrenceIdentity != ContentIdentity``.

This module closes that gap for one thing only: reconstructing a canonical
identity for a transition's own structural content, independent of *when* or
*how many times* it was admitted. It does **not** answer whether a verifier
is the verifier it claims to be (extractor/registry content identity is a
deliberately separate, later concern), and it does not certify anything:

    StructurallyAdmissibleTransition
        -> CanonicalTransitionManifest -> TransitionContentIdentity

``CanonicalTransitionEncoder.encode`` is a deterministic *representation*
step, not a certification boundary: ``Canonicalization != Certification``.
Two transitions that encode to the same ``TransitionContentIdentity`` are
known to share canonicalized structural content; nothing here says they were
verified, licensed, or hold the same epistemic authority in whatever run
produced them: ``SameContentID != SameEpistemicAuthority``.

Canonicalization contract (v1), deliberately conservative:

* Supported payload types are exactly: ``None``, ``bool``, ``int``, finite
  ``float`` (``NaN``/``Infinity``/``-Infinity`` are refused), ``str``,
  ``bytes``/``bytearray``, ``list``/``tuple`` (order-preserving sequences),
  and ``Mapping`` with ``str`` keys -- plus arbitrary compositions of these.
* Anything else raises ``CanonicalizationError``. There is no ``repr()``
  fallback: a stable-looking ``repr()`` of an arbitrary object is not a
  canonical identity (``StableRepr != CanonicalIdentity``), so canonicalizing
  an unsupported payload is refused outright, not approximated.
  ``Canonicalizable != True`` -- successfully serializing something is not a
  claim that the serialization is semantically meaningful.
* Sequences (``list``/``tuple``) preserve declared order: ``[e1, e2]`` and
  ``[e2, e1]`` canonicalize differently. Canonicalization must preserve
  declared structure, not erase it
  (``CanonicalizationMustPreserveDeclaredStructure``). Mapping key order does
  not affect the digest: mappings are canonicalized by sorting entries by
  key, since Python mapping equality does not depend on insertion order.
* ``preserved``/``changed`` component names are the one place this module
  deliberately *does* erase order: they are membership sets under the
  existing kernel contract (``_validate_components`` already requires them
  to be unique), so ``CanonicalTransitionEncoder`` canonicalizes each as a
  sorted, deduplicated sequence of names, not the declared tuple order. This
  is written here explicitly, not chosen silently inside a serializer.

Every canonical node is encoded as a self-describing, uniformly tagged
``[type, payload]`` pair (see ``_encode``), so scalar leaves of different
types can never collide at the canonical-JSON-bytes level -- for example, a
``str`` payload that happens to look like a ``bytes`` hex digest, or an
``int`` that happens to look like a ``bool``.

Snapshot-at-boundary: ``CanonicalStateManifest.from_payload`` (and therefore
``CanonicalTransitionEncoder.encode``) eagerly walks the payload into a new,
immutable tuple-only tree at construction time. Mutating the original
mutable payload afterward (for example appending to a list stored in
``State.value``) does not change an already-issued manifest or
``TransitionContentIdentity``: ``SnapshotIdentity is stable after issuance``.

No component here lets a transition issue its own identity
(``transition.content_id()`` is deliberately not a method): identity is
issued by ``CanonicalTransitionEncoder``, an external, stateless projector,
mirroring the kernel's existing gate-issuance philosophy without claiming
gate-level authority -- this is representation, not certification.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .anchor import Anchor
    from .evidence import Claim, Evidence
    from .operation import Operation
    from .residual import Residual
    from .trace import Trace
    from .transition import StructurallyAdmissibleTransition

_SCHEMA = "alghanem.transition-manifest.v1"
_CANONICALIZATION_VERSION = "transition-manifest-v1"
_ALGORITHM = "sha256"

#: A canonical value is a tagged tree, e.g. ``("str", "x")``,
#: ``("list", (("int", 1), ("int", 2)))``, or
#: ``("map", (("a", ("int", 1)), ("b", ("int", 2))))``. Every node is a
#: tuple, so the tree itself is immutable and hashable.
CanonicalValue = tuple[Any, ...]


class CanonicalizationError(ValueError):
    """A payload falls outside the v1 canonicalization contract.

    This is not an epistemic failure (not ``BLOCK``, not ``DEFER``): it is a
    refusal to issue a content identity for material the canonicalization
    contract does not cover, exactly mirroring
    ``Malformed/UnsupportedRepresentation != EpistemicFailure`` one layer up
    from invariant verification.
    """


def canonicalize(value: object) -> CanonicalValue:
    """Convert a supported Python payload into an immutable canonical tree.

    Raises ``CanonicalizationError`` for any payload outside the v1
    contract (see the module docstring); there is no ``repr()`` fallback.
    """

    if value is None:
        return ("null",)
    if isinstance(value, bool):
        return ("bool", value)
    if isinstance(value, int):
        return ("int", value)
    if isinstance(value, float):
        if value != value or value in (float("inf"), float("-inf")):
            raise CanonicalizationError(
                "canonicalization v1 refuses non-finite floats "
                "(NaN/Infinity/-Infinity)"
            )
        return ("float", repr(value))
    if isinstance(value, str):
        return ("str", value)
    if isinstance(value, (bytes, bytearray)):
        return ("bytes", bytes(value).hex())
    if isinstance(value, (list, tuple)):
        return ("list", tuple(canonicalize(item) for item in value))
    if isinstance(value, Mapping):
        entries: list[tuple[str, CanonicalValue]] = []
        for key, item in value.items():
            if not isinstance(key, str):
                raise CanonicalizationError(
                    "canonicalization v1 requires mapping keys to be str, "
                    f"got {type(key).__name__!r}"
                )
            entries.append((key, canonicalize(item)))
        entries.sort(key=lambda entry: entry[0])
        return ("map", tuple(entries))
    raise CanonicalizationError(
        f"canonicalization v1 has no contract for {type(value).__name__!r}; "
        "unsupported payloads are refused, never approximated via repr()"
    )


def _map(entries: dict[str, CanonicalValue]) -> CanonicalValue:
    """Wrap already-canonical values into a canonical ``map`` node."""

    return ("map", tuple(sorted(entries.items(), key=lambda entry: entry[0])))


def _encode(node: CanonicalValue) -> object:
    """Convert a canonical value tree into a JSON-serializable structure.

    Every node becomes a two-element ``[tag, payload]`` array, applied
    uniformly and recursively, so no scalar leaf of one type can ever be
    confused with a differently-typed leaf at the JSON text level.
    """

    tag = node[0]
    if tag in ("null", "bool", "int", "float", "str", "bytes"):
        payload = node[1] if len(node) > 1 else None
        return [tag, payload]
    if tag == "list":
        return [tag, [_encode(item) for item in node[1]]]
    if tag == "map":
        return [tag, [[key, _encode(item)] for key, item in node[1]]]
    raise AssertionError(f"unreachable canonical tag: {tag!r}")


def canonical_bytes(node: CanonicalValue) -> bytes:
    """Deterministic UTF-8 canonical JSON bytes for a canonical value tree."""

    return json.dumps(
        _encode(node),
        ensure_ascii=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


@dataclass(frozen=True, slots=True)
class CanonicalStateManifest:
    """A canonical, immutable snapshot of one opaque state-shaped payload.

    Used for ``State.value``, ``OperationResult.value``, and any other
    single opaque payload that needs a canonical identity. Construction
    eagerly canonicalizes the payload into an immutable tuple tree, so
    later mutation of the original payload object cannot change this
    manifest.
    """

    canonical_value: CanonicalValue

    @staticmethod
    def from_payload(value: object) -> CanonicalStateManifest:
        return CanonicalStateManifest(canonical_value=canonicalize(value))


@dataclass(frozen=True, slots=True)
class CanonicalOperationManifest:
    """A canonical snapshot of an ``Operation``'s declared fields."""

    name: str
    declared_change: str
    source_domain: str | None
    target_domain: str | None

    @staticmethod
    def from_operation(operation: Operation) -> CanonicalOperationManifest:
        return CanonicalOperationManifest(
            name=operation.name,
            declared_change=operation.declared_change,
            source_domain=operation.source_domain,
            target_domain=operation.target_domain,
        )

    def to_canonical(self) -> CanonicalValue:
        return canonicalize(dataclasses.asdict(self))


@dataclass(frozen=True, slots=True)
class TransitionContentIdentity:
    """A canonical, algorithm- and version-explicit transition content id.

    Deliberately not a bare ``str``: a hash value without its
    canonicalization algorithm/version is not a reconstructible identity
    over time. ``algorithm`` and ``canonicalization_version`` pin down
    exactly what ``digest`` was computed over, so a future v2
    canonicalization contract cannot be silently confused with v1 digests
    that happen to look the same.
    """

    algorithm: str
    canonicalization_version: str
    digest: str

    def __post_init__(self) -> None:
        if not self.algorithm.strip():
            raise ValueError("a transition content identity requires an algorithm")
        if not self.canonicalization_version.strip():
            raise ValueError(
                "a transition content identity requires a canonicalization version"
            )
        if not self.digest.strip():
            raise ValueError("a transition content identity requires a digest")


@dataclass(frozen=True, slots=True)
class CanonicalTransitionManifest:
    """The canonical structural content of an admitted transition.

    Deliberately excludes occurrence-only identifiers: ``admission_id`` is
    not part of this manifest, so two admissions of the same declared
    content produce the same manifest and the same
    ``TransitionContentIdentity`` even though each admission still gets its
    own distinct ``admission_id``
    (``OccurrenceIdentity != ContentIdentity``). Covers exactly the fields
    that are structurally part of the transition's own content: source and
    target anchor, before/after state, operation, claim, evidence,
    preserved/changed components, trace, residuals, claimed kind, and
    result. It intentionally excludes ``branch_origin_provenance`` (already
    structurally redundant with the validated anchor/preserved fields for
    every transition that reaches structural admission) to keep this PR's
    scope to the transition's own content identity; extractor/registry
    content identity is a separate, later concern.

    Construction is a deterministic representation step, not certification:
    ``Canonicalization != Certification``. Use
    ``CanonicalTransitionEncoder.encode``, not a method on the transition
    itself.
    """

    schema: str
    anchor: CanonicalValue
    target_anchor: CanonicalValue
    before_state: CanonicalStateManifest
    after_state: CanonicalStateManifest
    operation: CanonicalOperationManifest
    claim: CanonicalValue
    evidence: CanonicalValue
    preserved: CanonicalValue
    changed: CanonicalValue
    trace: CanonicalValue
    residuals: CanonicalValue
    kind: str
    result: CanonicalStateManifest
    #: The exact bytes ``content_id.digest`` was computed over. Retained
    #: (not recomputed from the fields above) so the manifest is
    #: independently auditable/testable without re-deriving and re-hashing
    #: the document; for very large payloads, callers that only need
    #: ``content_id`` may discard the manifest after issuance.
    canonical_bytes: bytes
    content_id: TransitionContentIdentity


def _canonicalize_anchor(anchor: Anchor) -> CanonicalValue:
    return canonicalize({"id": anchor.identifier, "domain": anchor.domain})


def _canonicalize_claim(claim: Claim) -> CanonicalValue:
    return canonicalize({"claim_id": claim.claim_id, "statement": claim.statement})


def _canonicalize_evidence(evidence: tuple[Evidence, ...]) -> CanonicalValue:
    return canonicalize(
        tuple({"claim_id": item.claim_id, "basis": item.basis} for item in evidence)
    )


def _canonicalize_component_set(components: tuple[str, ...]) -> CanonicalValue:
    """Sorted, deduplicated membership set -- see the module docstring's
    explicit ``preserved``/``changed`` canonicalization rule."""

    return canonicalize(tuple(sorted(set(components))))


def _canonicalize_trace(trace: Trace) -> CanonicalValue:
    return canonicalize(tuple(trace.events))


def _canonicalize_residuals(residuals: tuple[Residual, ...]) -> CanonicalValue:
    return canonicalize(tuple(residual.description for residual in residuals))


class CanonicalTransitionEncoder:
    """Deterministic ``StructurallyAdmissibleTransition`` -> manifest encoder.

    A stateless projector, not a gate: it does not certify anything about
    the transition it encodes, and it is not itself a source of epistemic
    authority. It only reconstructs a canonical identity for structural
    content that already exists on an admitted transition.
    """

    @staticmethod
    def encode(
        transition: StructurallyAdmissibleTransition,
    ) -> CanonicalTransitionManifest:
        """Encode an admitted transition's canonical structural content.

        Raises ``CanonicalizationError`` if any covered field's payload
        falls outside the v1 canonicalization contract (see the module
        docstring); this is a refusal, not a best-effort approximation.
        """

        if transition.result is None:
            raise CanonicalizationError(
                "a structurally admissible transition requires a result to "
                "encode a canonical transition manifest"
            )

        anchor_canonical = _canonicalize_anchor(transition.anchor)
        target_anchor_canonical = _canonicalize_anchor(
            transition.resolved_target_anchor
        )
        before_state = CanonicalStateManifest.from_payload(
            transition.before_state.value
        )
        after_state = CanonicalStateManifest.from_payload(transition.after_state.value)
        operation = CanonicalOperationManifest.from_operation(transition.operation)
        claim_canonical = _canonicalize_claim(transition.claim)
        evidence_canonical = _canonicalize_evidence(transition.evidence)
        preserved_canonical = _canonicalize_component_set(transition.preserved)
        changed_canonical = _canonicalize_component_set(transition.changed)
        trace_canonical = _canonicalize_trace(transition.trace)
        residuals_canonical = _canonicalize_residuals(transition.residuals)
        result_state = CanonicalStateManifest.from_payload(transition.result.value)

        document = _map(
            {
                "schema": canonicalize(_SCHEMA),
                "anchor": anchor_canonical,
                "target_anchor": target_anchor_canonical,
                "before_state": before_state.canonical_value,
                "after_state": after_state.canonical_value,
                "operation": operation.to_canonical(),
                "claim": claim_canonical,
                "evidence": evidence_canonical,
                "preserved": preserved_canonical,
                "changed": changed_canonical,
                "trace": trace_canonical,
                "residuals": residuals_canonical,
                "kind": canonicalize(transition.kind.name),
                "result": result_state.canonical_value,
            }
        )
        document_bytes = canonical_bytes(document)
        digest = hashlib.sha256(document_bytes).hexdigest()
        content_id = TransitionContentIdentity(
            algorithm=_ALGORITHM,
            canonicalization_version=_CANONICALIZATION_VERSION,
            digest=digest,
        )

        return CanonicalTransitionManifest(
            schema=_SCHEMA,
            anchor=anchor_canonical,
            target_anchor=target_anchor_canonical,
            before_state=before_state,
            after_state=after_state,
            operation=operation,
            claim=claim_canonical,
            evidence=evidence_canonical,
            preserved=preserved_canonical,
            changed=changed_canonical,
            trace=trace_canonical,
            residuals=residuals_canonical,
            kind=transition.kind.name,
            result=result_state,
            canonical_bytes=document_bytes,
            content_id=content_id,
        )
