"""G0.C.1's minimal, evidence-free constitution for claim candidates.

`ClaimCandidate` records structured content someone puts forward; it neither
asserts truth nor knowledge, and it carries no evidence or evidence binding.
Its occurrence reference is deliberately distinct from its content identity:
independent occurrences may manifest canonically identical claim content.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, fields
from enum import Enum

from .anchor import Anchor

_CLAIM_CONTENT_TOKEN = object()
_ALGORITHM = "sha256"
_CANONICALIZATION_VERSION = "claim-content-manifest-v1"
CLAIM_CONTENT_MANIFEST_COVERAGE = ("core", "qualifications")
CLAIM_CORE_COVERAGE = ("anchor", "predicate", "polarity", "scope")
ANCHOR_COVERAGE = ("identifier", "domain")
PREDICATE_REF_COVERAGE = ("identifier",)
CLAIM_SCOPE_REF_COVERAGE = ("scope_type", "reference")
CLAIM_QUALIFICATION_COVERAGE = ("kind", "value")


def _require_text(value: str, name: str) -> None:
    if type(value) is not str or not value.strip():
        raise ValueError(f"{name} must be non-blank text")


class ClaimPolarity(Enum):
    """Whether the structured predication is affirmed or negated."""

    AFFIRM = "affirm"
    NEGATE = "negate"


@dataclass(frozen=True, slots=True)
class ClaimScopeRef:
    """An explicit scope that is part of claim content, not occurrence metadata."""

    scope_type: str
    reference: str

    def __post_init__(self) -> None:
        _require_text(self.scope_type, "claim scope type")
        _require_text(self.reference, "claim scope reference")


@dataclass(frozen=True, slots=True)
class ClaimQualification:
    """A typed optional qualification that narrows a claim's content."""

    kind: str
    value: str

    def __post_init__(self) -> None:
        _require_text(self.kind, "claim qualification kind")
        _require_text(self.value, "claim qualification value")


@dataclass(frozen=True, slots=True)
class PredicateRef:
    """An opaque predicate reference; its rendering and semantics are deferred."""

    identifier: str

    def __post_init__(self) -> None:
        _require_text(self.identifier, "predicate reference")


@dataclass(frozen=True, slots=True)
class ClaimCore:
    """The irreducible structured content required to represent a claim."""

    anchor: Anchor
    predicate: PredicateRef
    polarity: ClaimPolarity
    scope: ClaimScopeRef

    def __post_init__(self) -> None:
        if type(self.anchor) is not Anchor:
            raise TypeError("claim core requires an anchor")
        if type(self.predicate) is not PredicateRef:
            raise TypeError("claim core requires a predicate reference")
        if not isinstance(self.polarity, ClaimPolarity):
            raise TypeError("claim core requires a claim polarity")
        if type(self.scope) is not ClaimScopeRef:
            raise TypeError("claim core requires a claim scope")


@dataclass(frozen=True, slots=True)
class ClaimContentManifest:
    """A claim core plus optional, ordered qualifications."""

    core: ClaimCore
    qualifications: tuple[ClaimQualification, ...] = ()

    def __post_init__(self) -> None:
        if type(self.core) is not ClaimCore:
            raise TypeError("claim content requires a claim core")
        if type(self.qualifications) is not tuple or any(
            type(item) is not ClaimQualification for item in self.qualifications
        ):
            raise TypeError("claim qualifications must be a tuple of qualifications")


_CLAIM_CONTENT_MANIFEST_FIELDS = frozenset(
    item.name for item in fields(ClaimContentManifest)
)
_CLAIM_CORE_FIELDS = frozenset(item.name for item in fields(ClaimCore))
_ANCHOR_FIELDS = frozenset(item.name for item in fields(Anchor))
_PREDICATE_REF_FIELDS = frozenset(item.name for item in fields(PredicateRef))
_CLAIM_SCOPE_REF_FIELDS = frozenset(item.name for item in fields(ClaimScopeRef))
_CLAIM_QUALIFICATION_FIELDS = frozenset(
    item.name for item in fields(ClaimQualification)
)


@dataclass(frozen=True, slots=True)
class ClaimContentIdentity:
    """A digest reference to canonical structured claim content."""

    algorithm: str
    canonicalization_version: str
    digest: str
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _CLAIM_CONTENT_TOKEN:
            raise ValueError(
                "claim content identities must be issued by "
                "CanonicalClaimContentEncoder"
            )
        if (
            self.algorithm != _ALGORITHM
            or self.canonicalization_version != _CANONICALIZATION_VERSION
            or len(self.digest) != 64
            or any(character not in "0123456789abcdef" for character in self.digest)
        ):
            raise ValueError("invalid claim content identity")


@dataclass(frozen=True, slots=True)
class CanonicalClaimContentManifest:
    """Immutable canonical bytes and identity for one claim's content."""

    canonical_bytes: bytes
    content_id: ClaimContentIdentity
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _CLAIM_CONTENT_TOKEN:
            raise ValueError(
                "canonical claim content manifests must be issued by "
                "CanonicalClaimContentEncoder"
            )
        if hashlib.sha256(self.canonical_bytes).hexdigest() != self.content_id.digest:
            raise ValueError("manifest bytes do not match its content digest")


class CanonicalClaimContentEncoder:
    """The sole issuer of canonical claim-content manifests and identities."""

    @classmethod
    def encode(cls, content: ClaimContentManifest) -> CanonicalClaimContentManifest:
        if type(content) is not ClaimContentManifest:
            raise TypeError("canonical claim encoding requires claim content")
        cls._assert_schema_coverage()
        cls._assert_nested_schema_coverage()
        encoded = {
            "anchor": {
                "domain": content.core.anchor.domain,
                "identifier": content.core.anchor.identifier,
            },
            "polarity": content.core.polarity.value,
            "predicate_ref": content.core.predicate.identifier,
            "qualifications": [
                {"kind": item.kind, "value": item.value}
                for item in content.qualifications
            ],
            "scope": {
                "reference": content.core.scope.reference,
                "scope_type": content.core.scope.scope_type,
            },
            "version": _CANONICALIZATION_VERSION,
        }
        canonical_bytes = json.dumps(
            encoded, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        ).encode("utf-8", "surrogatepass")
        content_id = ClaimContentIdentity(
            algorithm=_ALGORITHM,
            canonicalization_version=_CANONICALIZATION_VERSION,
            digest=hashlib.sha256(canonical_bytes).hexdigest(),
            _token=_CLAIM_CONTENT_TOKEN,
        )
        return CanonicalClaimContentManifest(
            canonical_bytes=canonical_bytes,
            content_id=content_id,
            _token=_CLAIM_CONTENT_TOKEN,
        )

    @staticmethod
    def _assert_schema_coverage() -> None:
        CanonicalClaimContentEncoder._assert_type_coverage(
            "ClaimContentManifest",
            _CLAIM_CONTENT_MANIFEST_FIELDS,
            CLAIM_CONTENT_MANIFEST_COVERAGE,
        )

    @staticmethod
    def _assert_nested_schema_coverage() -> None:
        CanonicalClaimContentEncoder._assert_type_coverage(
            "ClaimCore", _CLAIM_CORE_FIELDS, CLAIM_CORE_COVERAGE
        )
        CanonicalClaimContentEncoder._assert_type_coverage(
            "Anchor", _ANCHOR_FIELDS, ANCHOR_COVERAGE
        )
        CanonicalClaimContentEncoder._assert_type_coverage(
            "PredicateRef", _PREDICATE_REF_FIELDS, PREDICATE_REF_COVERAGE
        )
        CanonicalClaimContentEncoder._assert_type_coverage(
            "ClaimScopeRef", _CLAIM_SCOPE_REF_FIELDS, CLAIM_SCOPE_REF_COVERAGE
        )
        CanonicalClaimContentEncoder._assert_type_coverage(
            "ClaimQualification",
            _CLAIM_QUALIFICATION_FIELDS,
            CLAIM_QUALIFICATION_COVERAGE,
        )

    @staticmethod
    def _assert_type_coverage(
        content_type_name: str,
        actual_fields: frozenset[str],
        covered_fields: tuple[str, ...],
    ) -> None:
        if actual_fields != set(covered_fields):
            raise RuntimeError(
                f"{content_type_name} coverage must explicitly account for "
                "every identity-bearing field"
            )


@dataclass(frozen=True, slots=True)
class ClaimOccurrenceRef:
    """A local reference, not a portable identity, for one claim occurrence."""

    value: str

    def __post_init__(self) -> None:
        _require_text(self.value, "claim occurrence reference")


@dataclass(frozen=True, slots=True)
class ClaimCandidate:
    """One reviewable occurrence of structured claim content, without evidence."""

    occurrence: ClaimOccurrenceRef
    content: ClaimContentManifest
    content_manifest: CanonicalClaimContentManifest
    content_id: ClaimContentIdentity = field(init=False)

    def __post_init__(self) -> None:
        if type(self.occurrence) is not ClaimOccurrenceRef:
            raise TypeError("claim candidate requires an occurrence reference")
        if type(self.content) is not ClaimContentManifest:
            raise TypeError("claim candidate requires claim content")
        if type(self.content_manifest) is not CanonicalClaimContentManifest:
            raise TypeError("claim candidate requires a canonical content manifest")
        expected = CanonicalClaimContentEncoder.encode(self.content)
        if self.content_manifest != expected:
            raise ValueError("claim candidate manifest does not match its content")
        object.__setattr__(self, "content_id", self.content_manifest.content_id)
