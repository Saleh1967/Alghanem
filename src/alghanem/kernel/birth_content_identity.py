"""G0.2a.1 semantic content identity: ``SameId != SameSemantics``.

``BirthAssessmentSemanticsContract`` already enforces
``NoResidualDefinitionDriftAfterFreeze`` and ``NoClosureCriterionDriftAfterFreeze``
by comparing ``residual_id``/``criterion_id`` text against the frozen
specification. That closes *label* identity, not *content* identity: two
``ResidualDefinitionSpec`` instances can share ``residual_id`` while carrying a
different ``output_schema``, ``evaluator_id``, ``invariants``, or
``failure_semantics``. The same drift is possible for ``ClosureCriterionSpec``
and ``WeakerModelSpec``. This module names that distinct hazard explicitly:
``ResidualDefinitionId != ResidualDefinitionContentIdentity`` and the same for
closure criteria and weaker models, mirroring the already-established
``OccurrenceIdentity != ContentIdentity`` law used for transition manifests
(see ``content_identity.py``).

This module only issues canonical, immutable content snapshots and their
digest references, and a registry that freezes the *first* canonical content
bound to a given ``(domain, role, target_id)`` scope so that any later
contract naming that exact scope must reproduce identical canonical content.
It executes no residual, closure, or weaker-model evaluator, and it issues no
``BirthVerdict``, ``BirthCandidate``, or ``Freeze``.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass, field

from .birth import (
    BirthAssessmentSemanticsContract,
    BirthEvaluatorRole,
    BirthExperimentSpecificationError,
    ClosureCriterionSpec,
    ResidualDefinitionSpec,
    WeakerModelSpec,
)

_CONTENT_ID_TOKEN = object()
_ALGORITHM = "sha256"
_CANONICALIZATION_VERSION = "birth-semantics-manifest-v1"


class BirthSemanticsContentIdentityError(BirthExperimentSpecificationError):
    """Runtime executable content does not match its frozen content identity."""


@dataclass(frozen=True, slots=True)
class BirthSemanticsContentIdentity:
    """A SHA-256 reference to canonical bytes, issued only by the encoder.

    Equality of these values is digest equality, not proof that the canonical
    bytes are equal. The manifest that produced this identity retains those
    bytes as the canonical content snapshot.
    """

    algorithm: str
    canonicalization_version: str
    digest: str
    _content_id_token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._content_id_token is not _CONTENT_ID_TOKEN:
            raise BirthSemanticsContentIdentityError(
                "birth semantics content identities must be issued by "
                "CanonicalBirthSemanticsEncoder"
            )
        if (
            self.algorithm != _ALGORITHM
            or self.canonicalization_version != _CANONICALIZATION_VERSION
            or len(self.digest) != 64
            or any(character not in "0123456789abcdef" for character in self.digest)
        ):
            raise BirthSemanticsContentIdentityError(
                "invalid birth semantics content identity"
            )


def _canonical_manifest_class_error(role_label: str) -> str:
    return (
        f"canonical {role_label} manifests must be issued by "
        "CanonicalBirthSemanticsEncoder"
    )


@dataclass(frozen=True, slots=True)
class CanonicalResidualDefinitionManifest:
    """An immutable canonical-content snapshot of one ``ResidualDefinitionSpec``."""

    canonical_bytes: bytes
    content_id: BirthSemanticsContentIdentity
    _manifest_token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._manifest_token is not _CONTENT_ID_TOKEN:
            raise BirthSemanticsContentIdentityError(
                _canonical_manifest_class_error("residual definition")
            )
        _assert_digest_matches(self.canonical_bytes, self.content_id)


@dataclass(frozen=True, slots=True)
class CanonicalClosureCriterionManifest:
    """An immutable canonical-content snapshot of one ``ClosureCriterionSpec``."""

    canonical_bytes: bytes
    content_id: BirthSemanticsContentIdentity
    _manifest_token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._manifest_token is not _CONTENT_ID_TOKEN:
            raise BirthSemanticsContentIdentityError(
                _canonical_manifest_class_error("closure criterion")
            )
        _assert_digest_matches(self.canonical_bytes, self.content_id)


@dataclass(frozen=True, slots=True)
class CanonicalWeakerModelManifest:
    """An immutable canonical-content snapshot of one ``WeakerModelSpec``."""

    canonical_bytes: bytes
    content_id: BirthSemanticsContentIdentity
    _manifest_token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._manifest_token is not _CONTENT_ID_TOKEN:
            raise BirthSemanticsContentIdentityError(
                _canonical_manifest_class_error("weaker model")
            )
        _assert_digest_matches(self.canonical_bytes, self.content_id)


def _assert_digest_matches(
    canonical_bytes: bytes, content_id: BirthSemanticsContentIdentity
) -> None:
    digest = hashlib.sha256(canonical_bytes).hexdigest()
    if digest != content_id.digest:
        raise BirthSemanticsContentIdentityError(
            "manifest bytes do not match its content digest"
        )


class CanonicalBirthSemanticsEncoder:
    """The sole issuer of canonical birth-semantics snapshots and digests.

    Every declared field of ``ResidualDefinitionSpec``, ``ClosureCriterionSpec``,
    and ``WeakerModelSpec`` is included in its canonical encoding: content
    identity cannot silently ignore a field that later drifts.
    """

    @classmethod
    def encode_residual_definition(
        cls, spec: ResidualDefinitionSpec
    ) -> CanonicalResidualDefinitionManifest:
        if type(spec) is not ResidualDefinitionSpec:
            raise BirthSemanticsContentIdentityError(
                "canonical encoding requires an executable residual definition"
            )
        encoded = {
            "domain": spec.domain,
            "evaluator_id": spec.evaluator_id,
            "failure_semantics": spec.failure_semantics,
            "input_projection": spec.input_projection,
            "invariants": sorted(spec.invariants),
            "output_schema": spec.output_schema,
            "residual_id": spec.residual_id,
            "version": _CANONICALIZATION_VERSION,
        }
        canonical_bytes = _canonical_bytes(encoded)
        content_id = _issue_content_id(canonical_bytes)
        return CanonicalResidualDefinitionManifest(
            canonical_bytes=canonical_bytes,
            content_id=content_id,
            _manifest_token=_CONTENT_ID_TOKEN,
        )

    @classmethod
    def encode_closure_criterion(
        cls, spec: ClosureCriterionSpec
    ) -> CanonicalClosureCriterionManifest:
        if type(spec) is not ClosureCriterionSpec:
            raise BirthSemanticsContentIdentityError(
                "canonical encoding requires an executable closure criterion"
            )
        encoded = {
            "criterion_id": spec.criterion_id,
            "domain": spec.domain,
            "evaluator_id": spec.evaluator_id,
            "failure_semantics": spec.failure_semantics,
            "model_result_schema": spec.model_result_schema,
            "residual_id": spec.residual_id,
            "residual_schema": spec.residual_schema,
            "version": _CANONICALIZATION_VERSION,
        }
        canonical_bytes = _canonical_bytes(encoded)
        content_id = _issue_content_id(canonical_bytes)
        return CanonicalClosureCriterionManifest(
            canonical_bytes=canonical_bytes,
            content_id=content_id,
            _manifest_token=_CONTENT_ID_TOKEN,
        )

    @classmethod
    def encode_weaker_model(cls, spec: WeakerModelSpec) -> CanonicalWeakerModelManifest:
        if type(spec) is not WeakerModelSpec:
            raise BirthSemanticsContentIdentityError(
                "canonical encoding requires an executable weaker model"
            )
        encoded = {
            "declared_information_loss": spec.declared_information_loss,
            "domain": spec.domain,
            "model_id": spec.model_id,
            "projection_evaluator_id": spec.projection_evaluator_id,
            "result_schema": spec.result_schema,
            "strict_predecessors": sorted(spec.strict_predecessors),
            "strict_successors": sorted(spec.strict_successors),
            "version": _CANONICALIZATION_VERSION,
        }
        canonical_bytes = _canonical_bytes(encoded)
        content_id = _issue_content_id(canonical_bytes)
        return CanonicalWeakerModelManifest(
            canonical_bytes=canonical_bytes,
            content_id=content_id,
            _manifest_token=_CONTENT_ID_TOKEN,
        )


def _canonical_bytes(encoded: Mapping[str, object]) -> bytes:
    return json.dumps(
        encoded, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8", "surrogatepass")


def _issue_content_id(canonical_bytes: bytes) -> BirthSemanticsContentIdentity:
    return BirthSemanticsContentIdentity(
        algorithm=_ALGORITHM,
        canonicalization_version=_CANONICALIZATION_VERSION,
        digest=hashlib.sha256(canonical_bytes).hexdigest(),
        _content_id_token=_CONTENT_ID_TOKEN,
    )


@dataclass(frozen=True, slots=True)
class FrozenBirthSemanticsContentScope:
    """A registry-recorded, first-binding content identity for one exact scope."""

    domain: str
    role: BirthEvaluatorRole
    target_id: str
    content_id: BirthSemanticsContentIdentity
    _scope_token: object = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._scope_token is not _CONTENT_ID_TOKEN:
            raise BirthSemanticsContentIdentityError(
                "frozen content scopes must be registry-issued"
            )
        if not isinstance(self.content_id, BirthSemanticsContentIdentity):
            raise BirthSemanticsContentIdentityError(
                "frozen content scope requires an issued content identity"
            )


class BirthSemanticsContentRegistry:
    """Freezes the first canonical content bound to a ``(domain, role, target_id)``.

    ``SameId => SameSemantics`` is not free: this registry is where that law is
    enforced. The first content identity recorded for an exact scope becomes
    that scope's frozen content; any later attempt to record a *different*
    content identity for the same scope is content drift and is rejected. It
    performs no evaluation and grants no evaluator execution authority.
    """

    def __init__(self) -> None:
        self._scopes: dict[
            tuple[str, BirthEvaluatorRole, str], FrozenBirthSemanticsContentScope
        ] = {}

    def freeze(
        self,
        *,
        domain: str,
        role: BirthEvaluatorRole,
        target_id: str,
        content_id: BirthSemanticsContentIdentity,
    ) -> FrozenBirthSemanticsContentScope:
        """Bind ``content_id`` to a scope, or verify it matches a prior binding."""

        if not isinstance(content_id, BirthSemanticsContentIdentity):
            raise BirthSemanticsContentIdentityError(
                "registry freeze requires an issued content identity"
            )
        key = (domain, role, target_id)
        existing = self._scopes.get(key)
        if existing is not None and existing.content_id.digest != content_id.digest:
            raise BirthSemanticsContentIdentityError(
                "runtime content identity does not match the frozen content "
                "identity for this scope: SameId != SameSemantics"
            )
        scope = existing or FrozenBirthSemanticsContentScope(
            domain=domain,
            role=role,
            target_id=target_id,
            content_id=content_id,
            _scope_token=_CONTENT_ID_TOKEN,
        )
        self._scopes[key] = scope
        return scope

    def seal(self, snapshot_id: str) -> SealedBirthSemanticsContentRegistry:
        """Freeze the recorded content scopes without adding execution."""

        if not isinstance(snapshot_id, str) or not snapshot_id.strip():
            raise BirthSemanticsContentIdentityError(
                "content registry snapshot id must be non-blank"
            )
        return SealedBirthSemanticsContentRegistry(
            snapshot_id=snapshot_id,
            scopes=tuple(self._scopes.values()),
            _registry_token=_CONTENT_ID_TOKEN,
        )


@dataclass(frozen=True, slots=True)
class SealedBirthSemanticsContentRegistry:
    """Frozen registry snapshot; it resolves scopes but executes nothing."""

    snapshot_id: str
    scopes: tuple[FrozenBirthSemanticsContentScope, ...]
    _registry_token: object = field(default=None, repr=False, compare=False)
    _index: dict[
        tuple[str, BirthEvaluatorRole, str], FrozenBirthSemanticsContentScope
    ] = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._registry_token is not _CONTENT_ID_TOKEN:
            raise BirthSemanticsContentIdentityError(
                "sealed content registries must be registry-issued"
            )
        if not isinstance(self.snapshot_id, str) or not self.snapshot_id.strip():
            raise BirthSemanticsContentIdentityError(
                "content registry snapshot id must be non-blank"
            )
        if not isinstance(self.scopes, tuple):
            raise BirthSemanticsContentIdentityError(
                "content registry scopes must be frozen"
            )
        index: dict[
            tuple[str, BirthEvaluatorRole, str], FrozenBirthSemanticsContentScope
        ] = {}
        for scope in self.scopes:
            if not isinstance(scope, FrozenBirthSemanticsContentScope):
                raise BirthSemanticsContentIdentityError(
                    "sealed content registry requires frozen content scopes"
                )
            key = (scope.domain, scope.role, scope.target_id)
            if key in index:
                raise BirthSemanticsContentIdentityError(
                    "sealed content registry must not contain duplicate scopes"
                )
            index[key] = scope
        object.__setattr__(self, "_index", index)

    def resolve_frozen(
        self, *, domain: str, role: BirthEvaluatorRole, target_id: str
    ) -> BirthSemanticsContentIdentity:
        """Return the frozen content identity for an exact declared scope."""

        scope = self._index.get((domain, role, target_id))
        if scope is None:
            raise BirthSemanticsContentIdentityError(
                "no frozen content identity is recorded for this scope"
            )
        return scope.content_id


@dataclass(frozen=True, slots=True)
class BirthAssessmentContentBinding:
    """Proves ``CID(runtime) == CID(frozen)`` for one semantics contract.

    Binding this requires a sealed content registry that already recorded a
    frozen content identity for every scope the contract declares. A caller
    cannot manufacture a passing binding by omitting a scope from the
    registry: ``resolve_frozen`` raises for any scope it does not recognize.
    """

    contract: BirthAssessmentSemanticsContract
    registry_snapshot: SealedBirthSemanticsContentRegistry
    residual_definition_content_id: BirthSemanticsContentIdentity = field(init=False)
    closure_criterion_content_id: BirthSemanticsContentIdentity = field(init=False)
    weaker_model_content_ids: tuple[BirthSemanticsContentIdentity, ...] = field(
        init=False
    )

    def __post_init__(self) -> None:
        if not isinstance(self.contract, BirthAssessmentSemanticsContract):
            raise BirthSemanticsContentIdentityError(
                "content binding requires a birth assessment semantics contract"
            )
        if not isinstance(self.registry_snapshot, SealedBirthSemanticsContentRegistry):
            raise BirthSemanticsContentIdentityError(
                "content binding requires a sealed content registry"
            )
        domain = self.contract.specification.domain

        residual_runtime_id = CanonicalBirthSemanticsEncoder.encode_residual_definition(
            self.contract.residual_definition
        ).content_id
        residual_frozen_id = self.registry_snapshot.resolve_frozen(
            domain=domain,
            role=BirthEvaluatorRole.RESIDUAL_DEFINITION,
            target_id=self.contract.residual_definition.residual_id,
        )
        if residual_runtime_id.digest != residual_frozen_id.digest:
            raise BirthSemanticsContentIdentityError(
                "residual definition content identity does not match its "
                "frozen content identity: SameId != SameSemantics"
            )
        object.__setattr__(self, "residual_definition_content_id", residual_frozen_id)

        closure_runtime_id = CanonicalBirthSemanticsEncoder.encode_closure_criterion(
            self.contract.closure_criterion
        ).content_id
        closure_frozen_id = self.registry_snapshot.resolve_frozen(
            domain=domain,
            role=BirthEvaluatorRole.CLOSURE_CRITERION,
            target_id=self.contract.closure_criterion.criterion_id,
        )
        if closure_runtime_id.digest != closure_frozen_id.digest:
            raise BirthSemanticsContentIdentityError(
                "closure criterion content identity does not match its "
                "frozen content identity: SameId != SameSemantics"
            )
        object.__setattr__(self, "closure_criterion_content_id", closure_frozen_id)

        weaker_model_content_ids = []
        for model in self.contract.weaker_models:
            runtime_id = CanonicalBirthSemanticsEncoder.encode_weaker_model(
                model
            ).content_id
            frozen_id = self.registry_snapshot.resolve_frozen(
                domain=domain,
                role=BirthEvaluatorRole.WEAKER_MODEL,
                target_id=model.model_id,
            )
            if runtime_id.digest != frozen_id.digest:
                raise BirthSemanticsContentIdentityError(
                    "weaker model content identity does not match its "
                    "frozen content identity: SameId != SameSemantics"
                )
            weaker_model_content_ids.append(frozen_id)
        object.__setattr__(
            self, "weaker_model_content_ids", tuple(weaker_model_content_ids)
        )


__all__ = [
    "BirthAssessmentContentBinding",
    "BirthSemanticsContentIdentity",
    "BirthSemanticsContentIdentityError",
    "BirthSemanticsContentRegistry",
    "CanonicalBirthSemanticsEncoder",
    "CanonicalClosureCriterionManifest",
    "CanonicalResidualDefinitionManifest",
    "CanonicalWeakerModelManifest",
    "FrozenBirthSemanticsContentScope",
    "SealedBirthSemanticsContentRegistry",
]
