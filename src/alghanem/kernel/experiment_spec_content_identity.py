"""G0.2a.2 canonical, pre-evidence identity for birth experiment specifications."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field

from .birth import BirthExperimentSpecification, BirthExperimentSpecificationError

_EXPERIMENT_CONTENT_TOKEN = object()
_ALGORITHM = "sha256"
_CANONICALIZATION_VERSION = "birth-experiment-specification-manifest-v1"


class BirthExperimentContentIdentityError(BirthExperimentSpecificationError):
    """An experiment specification is not its authorized frozen content."""


@dataclass(frozen=True, slots=True)
class BirthExperimentSpecificationContentIdentity:
    """A digest reference to an encoder-issued canonical experiment manifest."""

    algorithm: str
    canonicalization_version: str
    digest: str
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _EXPERIMENT_CONTENT_TOKEN:
            raise BirthExperimentContentIdentityError(
                "experiment content identities must be issued by "
                "CanonicalBirthExperimentSpecificationEncoder"
            )
        if (
            self.algorithm != _ALGORITHM
            or self.canonicalization_version != _CANONICALIZATION_VERSION
            or len(self.digest) != 64
            or any(character not in "0123456789abcdef" for character in self.digest)
        ):
            raise BirthExperimentContentIdentityError(
                "invalid experiment specification content identity"
            )


@dataclass(frozen=True, slots=True)
class CanonicalBirthExperimentSpecificationManifest:
    """The complete canonical content of one experiment specification."""

    canonical_bytes: bytes
    content_id: BirthExperimentSpecificationContentIdentity
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _EXPERIMENT_CONTENT_TOKEN:
            raise BirthExperimentContentIdentityError(
                "canonical experiment manifests must be issued by "
                "CanonicalBirthExperimentSpecificationEncoder"
            )
        if hashlib.sha256(self.canonical_bytes).hexdigest() != self.content_id.digest:
            raise BirthExperimentContentIdentityError(
                "manifest bytes do not match its content digest"
            )


class CanonicalBirthExperimentSpecificationEncoder:
    """The sole issuer of complete, canonical experiment-specification manifests."""

    @classmethod
    def encode(
        cls, specification: BirthExperimentSpecification
    ) -> CanonicalBirthExperimentSpecificationManifest:
        if type(specification) is not BirthExperimentSpecification:
            raise BirthExperimentContentIdentityError(
                "canonical encoding requires a birth experiment specification"
            )
        poset = specification.projection_poset
        query = specification.birth_query
        encoded = {
            "birth_query": {
                "hypothesis": {
                    "hypothesis_id": query.hypothesis.hypothesis_id,
                    "statement": query.hypothesis.statement,
                },
                "query_id": query.query_id,
                "test_model": query.test_model,
            },
            "closure_criterion": specification.closure_criterion,
            "closure_criterion_id": specification.closure_criterion_id,
            "domain": specification.domain,
            "evidence_mode": specification.evidence_mode.name,
            "evidence_requirements": specification.evidence_requirements,
            "experiment_id": specification.experiment_id,
            "projection_poset": {
                "projections": sorted(poset.projections),
                "strict_relations": sorted(poset.strict_relations),
            },
            "residual_definition": specification.residual_definition,
            "residual_definition_id": specification.residual_definition_id,
            "revision_id": specification.revision_id,
            "revision_sequence": specification.revision_sequence,
            "version": _CANONICALIZATION_VERSION,
        }
        canonical_bytes = json.dumps(
            encoded, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        ).encode("utf-8", "surrogatepass")
        content_id = BirthExperimentSpecificationContentIdentity(
            algorithm=_ALGORITHM,
            canonicalization_version=_CANONICALIZATION_VERSION,
            digest=hashlib.sha256(canonical_bytes).hexdigest(),
            _token=_EXPERIMENT_CONTENT_TOKEN,
        )
        return CanonicalBirthExperimentSpecificationManifest(
            canonical_bytes=canonical_bytes,
            content_id=content_id,
            _token=_EXPERIMENT_CONTENT_TOKEN,
        )


@dataclass(frozen=True, slots=True)
class FrozenPreEvidenceExperimentManifest:
    """Authority-issued immutable experiment content, frozen before evidence."""

    canonical_manifest: CanonicalBirthExperimentSpecificationManifest
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _EXPERIMENT_CONTENT_TOKEN:
            raise BirthExperimentContentIdentityError(
                "frozen pre-evidence experiment manifests must be registry-issued"
            )

    @property
    def content_id(self) -> BirthExperimentSpecificationContentIdentity:
        return self.canonical_manifest.content_id


class PreEvidenceSpecificationRegistry:
    """Separate authority boundary for canonical experiment pre-evidence freezes."""

    def __init__(self) -> None:
        self._frozen: dict[
            tuple[str, str, int], FrozenPreEvidenceExperimentManifest
        ] = {}

    def freeze(
        self, manifest: CanonicalBirthExperimentSpecificationManifest
    ) -> FrozenPreEvidenceExperimentManifest:
        if type(manifest) is not CanonicalBirthExperimentSpecificationManifest:
            raise BirthExperimentContentIdentityError(
                "pre-evidence freeze requires a canonical experiment manifest"
            )
        encoded = json.loads(manifest.canonical_bytes)
        key = (
            encoded["domain"],
            encoded["experiment_id"],
            encoded["revision_sequence"],
        )
        existing = self._frozen.get(key)
        if existing is not None:
            if existing.canonical_manifest.canonical_bytes != manifest.canonical_bytes:
                raise BirthExperimentContentIdentityError(
                    "experiment canonical content does not match the authorized "
                    "pre-evidence freeze"
                )
            return existing
        frozen = FrozenPreEvidenceExperimentManifest(
            canonical_manifest=manifest, _token=_EXPERIMENT_CONTENT_TOKEN
        )
        self._frozen[key] = frozen
        return frozen


@dataclass(frozen=True, slots=True)
class BirthExperimentSpecificationContentBinding:
    """Proves a runtime specification reproduces an authorized frozen manifest."""

    specification: BirthExperimentSpecification
    frozen_manifest: FrozenPreEvidenceExperimentManifest
    content_id: BirthExperimentSpecificationContentIdentity = field(init=False)

    def __post_init__(self) -> None:
        if type(self.specification) is not BirthExperimentSpecification:
            raise BirthExperimentContentIdentityError(
                "experiment content binding requires a birth experiment specification"
            )
        if type(self.frozen_manifest) is not FrozenPreEvidenceExperimentManifest:
            raise BirthExperimentContentIdentityError(
                "experiment content binding requires a frozen pre-evidence manifest"
            )
        runtime_manifest = CanonicalBirthExperimentSpecificationEncoder.encode(
            self.specification
        )
        if (
            runtime_manifest.canonical_bytes
            != self.frozen_manifest.canonical_manifest.canonical_bytes
        ):
            raise BirthExperimentContentIdentityError(
                "runtime experiment canonical content does not match the authorized "
                "pre-evidence freeze"
            )
        object.__setattr__(self, "content_id", self.frozen_manifest.content_id)


__all__ = [
    "BirthExperimentContentIdentityError",
    "BirthExperimentSpecificationContentBinding",
    "BirthExperimentSpecificationContentIdentity",
    "CanonicalBirthExperimentSpecificationEncoder",
    "CanonicalBirthExperimentSpecificationManifest",
    "FrozenPreEvidenceExperimentManifest",
    "PreEvidenceSpecificationRegistry",
]
