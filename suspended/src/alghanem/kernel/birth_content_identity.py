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
contract naming that exact scope must reproduce identical canonical bytes.
It executes no residual, closure, or weaker-model evaluator, and it issues no
``BirthVerdict``, ``BirthCandidate``, or ``Freeze``.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass, field, fields

from .birth import (
    BirthAssessmentSemanticsContract,
    BirthEvaluatorRole,
    BirthExperimentSpecificationError,
    ClosureCriterionSpec,
    ResidualDefinitionSpec,
    WeakerModelSpec,
)
from .experiment_spec_content_identity import (
    BirthExperimentSpecificationContentBinding,
    FrozenPreEvidenceExperimentManifest,
)

_CONTENT_ID_TOKEN = object()
_ALGORITHM = "sha256"
_CANONICALIZATION_VERSION = "birth-semantics-manifest-v1"
RESIDUAL_DEFINITION_MANIFEST_COVERAGE = (
    "residual_id",
    "domain",
    "input_projection",
    "output_schema",
    "evaluator_id",
    "invariants",
    "failure_semantics",
)
WEAKER_MODEL_MANIFEST_COVERAGE = (
    "model_id",
    "domain",
    "projection_evaluator_id",
    "declared_information_loss",
    "result_schema",
    "strict_predecessors",
    "strict_successors",
)
CLOSURE_CRITERION_MANIFEST_COVERAGE = (
    "criterion_id",
    "residual_id",
    "domain",
    "residual_schema",
    "model_result_schema",
    "evaluator_id",
    "failure_semantics",
)


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
    identity cannot silently ignore a field that later drifts. Order-only
    collections (``invariants``, ``strict_predecessors``, ``strict_successors``)
    are sorted before encoding: for content-identity purposes their declared
    order carries no independent semantic meaning, only membership does.
    Encoding requires the exact declared spec type -- not a subclass -- so a
    caller cannot smuggle undeclared additional state past this encoder by
    subclassing one of these frozen dataclasses.
    """

    @classmethod
    def encode_residual_definition(
        cls, spec: ResidualDefinitionSpec
    ) -> CanonicalResidualDefinitionManifest:
        if type(spec) is not ResidualDefinitionSpec:
            raise BirthSemanticsContentIdentityError(
                "canonical encoding requires an executable residual definition"
            )
        cls._assert_schema_coverage(
            ResidualDefinitionSpec, RESIDUAL_DEFINITION_MANIFEST_COVERAGE
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
        cls._assert_schema_coverage(
            ClosureCriterionSpec, CLOSURE_CRITERION_MANIFEST_COVERAGE
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
        cls._assert_schema_coverage(WeakerModelSpec, WEAKER_MODEL_MANIFEST_COVERAGE)
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

    @staticmethod
    def _assert_schema_coverage(
        specification_type: (
            type[ResidualDefinitionSpec]
            | type[ClosureCriterionSpec]
            | type[WeakerModelSpec]
        ),
        manifest_coverage: tuple[str, ...],
    ) -> None:
        if {item.name for item in fields(specification_type)} != set(manifest_coverage):
            raise RuntimeError(
                "canonical birth semantics manifest coverage must explicitly account "
                f"for every {specification_type.__name__} field"
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
    """A registry-recorded canonical-content snapshot for one exact scope."""

    domain: str
    role: BirthEvaluatorRole
    target_id: str
    canonical_bytes: bytes
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
        if not isinstance(self.canonical_bytes, bytes):
            raise BirthSemanticsContentIdentityError(
                "frozen content scope requires canonical bytes"
            )
        _assert_digest_matches(self.canonical_bytes, self.content_id)


def _require_scope_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise BirthSemanticsContentIdentityError(f"{field_name} must be non-blank")


def _scope_label(domain: str, role: BirthEvaluatorRole, target_id: str) -> str:
    return f"domain={domain!r}, role={role!r}, target_id={target_id!r}"


def _manifest_matches_scope(
    manifest: (
        CanonicalResidualDefinitionManifest
        | CanonicalClosureCriterionManifest
        | CanonicalWeakerModelManifest
    ),
    domain: str,
    role: BirthEvaluatorRole,
    target_id: str,
) -> bool:
    manifest_type = {
        BirthEvaluatorRole.RESIDUAL_DEFINITION: CanonicalResidualDefinitionManifest,
        BirthEvaluatorRole.CLOSURE_CRITERION: CanonicalClosureCriterionManifest,
        BirthEvaluatorRole.WEAKER_MODEL: CanonicalWeakerModelManifest,
    }[role]
    if type(manifest) is not manifest_type:
        return False
    encoded = json.loads(manifest.canonical_bytes)
    id_field = {
        BirthEvaluatorRole.RESIDUAL_DEFINITION: "residual_id",
        BirthEvaluatorRole.CLOSURE_CRITERION: "criterion_id",
        BirthEvaluatorRole.WEAKER_MODEL: "model_id",
    }[role]
    return bool(encoded["domain"] == domain and encoded[id_field] == target_id)


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
        manifest: (
            CanonicalResidualDefinitionManifest
            | CanonicalClosureCriterionManifest
            | CanonicalWeakerModelManifest
        ),
    ) -> FrozenBirthSemanticsContentScope:
        """Bind canonical content to a scope, or verify a prior byte-exact binding."""

        _require_scope_text(domain, "content scope domain")
        if not isinstance(role, BirthEvaluatorRole):
            raise BirthSemanticsContentIdentityError(
                "content scope role must be declared"
            )
        _require_scope_text(target_id, "content scope target id")
        if not _manifest_matches_scope(manifest, domain, role, target_id):
            raise BirthSemanticsContentIdentityError(
                "registry freeze requires a canonical manifest for the exact scope"
            )
        key = (domain, role, target_id)
        existing = self._scopes.get(key)
        if (
            existing is not None
            and existing.canonical_bytes != manifest.canonical_bytes
        ):
            raise BirthSemanticsContentIdentityError(
                "runtime canonical content does not match the frozen canonical "
                "content for this scope: SameId != SameSemantics"
            )
        scope = existing or FrozenBirthSemanticsContentScope(
            domain=domain,
            role=role,
            target_id=target_id,
            canonical_bytes=manifest.canonical_bytes,
            content_id=manifest.content_id,
            _scope_token=_CONTENT_ID_TOKEN,
        )
        self._scopes[key] = scope
        return scope

    def seal(
        self,
        snapshot_id: str,
        frozen_experiment: FrozenPreEvidenceExperimentManifest,
    ) -> SealedBirthSemanticsContentRegistry:
        """Freeze the recorded content scopes without adding execution."""

        if not isinstance(snapshot_id, str) or not snapshot_id.strip():
            raise BirthSemanticsContentIdentityError(
                "content registry snapshot id must be non-blank"
            )
        if type(frozen_experiment) is not FrozenPreEvidenceExperimentManifest:
            raise BirthSemanticsContentIdentityError(
                "content registry seal requires a frozen pre-evidence "
                "experiment manifest"
            )
        return SealedBirthSemanticsContentRegistry(
            snapshot_id=snapshot_id,
            frozen_experiment=frozen_experiment,
            scopes=tuple(self._scopes.values()),
            _registry_token=_CONTENT_ID_TOKEN,
        )


@dataclass(frozen=True, slots=True)
class SealedBirthSemanticsContentRegistry:
    """Frozen registry snapshot; it resolves scopes but executes nothing."""

    snapshot_id: str
    frozen_experiment: FrozenPreEvidenceExperimentManifest
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
        if type(self.frozen_experiment) is not FrozenPreEvidenceExperimentManifest:
            raise BirthSemanticsContentIdentityError(
                "sealed content registry requires a frozen pre-evidence "
                "experiment manifest"
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
    ) -> FrozenBirthSemanticsContentScope:
        """Return the frozen canonical content for an exact declared scope."""

        scope = self._index.get((domain, role, target_id))
        if scope is None:
            raise BirthSemanticsContentIdentityError(
                "no frozen content (canonical bytes) is recorded for this scope "
                f"({_scope_label(domain, role, target_id)})"
            )
        return scope


@dataclass(frozen=True, slots=True)
class BirthAssessmentContentBinding:
    """Proves canonical-byte equality for one semantics contract.

    Binding this requires a sealed content registry that already recorded a
    frozen canonical content for every scope the contract declares. A caller
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
        try:
            BirthExperimentSpecificationContentBinding(
                specification=self.contract.specification,
                frozen_manifest=self.registry_snapshot.frozen_experiment,
            )
        except BirthExperimentSpecificationError as error:
            raise BirthSemanticsContentIdentityError(
                "content registry is not bound to this authorized frozen experiment"
            ) from error
        domain = self.contract.specification.domain

        residual_runtime = CanonicalBirthSemanticsEncoder.encode_residual_definition(
            self.contract.residual_definition
        )
        residual_frozen = self.registry_snapshot.resolve_frozen(
            domain=domain,
            role=BirthEvaluatorRole.RESIDUAL_DEFINITION,
            target_id=self.contract.residual_definition.residual_id,
        )
        if residual_runtime.canonical_bytes != residual_frozen.canonical_bytes:
            raise BirthSemanticsContentIdentityError(
                "residual definition content identity does not match its "
                "frozen content identity: SameId != SameSemantics"
            )
        object.__setattr__(
            self, "residual_definition_content_id", residual_frozen.content_id
        )

        closure_runtime = CanonicalBirthSemanticsEncoder.encode_closure_criterion(
            self.contract.closure_criterion
        )
        closure_frozen = self.registry_snapshot.resolve_frozen(
            domain=domain,
            role=BirthEvaluatorRole.CLOSURE_CRITERION,
            target_id=self.contract.closure_criterion.criterion_id,
        )
        if closure_runtime.canonical_bytes != closure_frozen.canonical_bytes:
            raise BirthSemanticsContentIdentityError(
                "closure criterion content identity does not match its "
                "frozen content identity: SameId != SameSemantics"
            )
        object.__setattr__(
            self, "closure_criterion_content_id", closure_frozen.content_id
        )

        weaker_model_content_ids = []
        for model in self.contract.weaker_models:
            runtime = CanonicalBirthSemanticsEncoder.encode_weaker_model(model)
            frozen = self.registry_snapshot.resolve_frozen(
                domain=domain,
                role=BirthEvaluatorRole.WEAKER_MODEL,
                target_id=model.model_id,
            )
            if runtime.canonical_bytes != frozen.canonical_bytes:
                raise BirthSemanticsContentIdentityError(
                    "weaker model content identity does not match its "
                    "frozen content identity: SameId != SameSemantics"
                )
            weaker_model_content_ids.append(frozen.content_id)
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
    "CLOSURE_CRITERION_MANIFEST_COVERAGE",
    "FrozenBirthSemanticsContentScope",
    "RESIDUAL_DEFINITION_MANIFEST_COVERAGE",
    "SealedBirthSemanticsContentRegistry",
    "WEAKER_MODEL_MANIFEST_COVERAGE",
]
