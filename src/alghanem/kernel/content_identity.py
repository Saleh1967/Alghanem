"""Canonical, snapshot-based content representations for admitted transitions."""

from __future__ import annotations

import base64
import hashlib
import json
import math
import struct
from dataclasses import dataclass, fields
from typing import cast

from .anchor import Anchor, State
from .evidence import Claim, Evidence
from .operation import Operation, OperationResult
from .residual import Residual
from .trace import Trace
from .transition import BranchOriginProvenance, StructurallyAdmissibleTransition

_CONTENT_ID_TOKEN = object()
_ALGORITHM = "sha256"
_CANONICALIZATION_VERSION = "transition-manifest-v1"

# These fields belong to one admitted transition's content. Occurrence-specific
# admission metadata is intentionally excluded because a fresh admission must
# not alter a content snapshot.
MANIFEST_COVERAGE = (
    "anchor",
    "before_state",
    "operation",
    "after_state",
    "claim",
    "evidence",
    "preserved",
    "changed",
    "trace",
    "residuals",
    "kind",
    "result",
    "branch_origin_provenance",
    "target_anchor",
)
OCCURRENCE_ONLY_EXCLUSIONS = (
    "admission_id",
    "transition_projection_fingerprint",
)


@dataclass(frozen=True, slots=True)
class TransitionContentIdentity:
    """A SHA-256 reference to canonical bytes, issued only by the encoder.

    Equality of these values is digest equality, not proof that the canonical
    bytes are equal. The manifest retains those bytes as the canonical content
    snapshot.
    """

    algorithm: str
    canonicalization_version: str
    digest: str
    _content_id_token: object | None = None

    def __post_init__(self) -> None:
        if self._content_id_token is not _CONTENT_ID_TOKEN:
            raise ValueError(
                "transition content identities must be issued by "
                "CanonicalTransitionEncoder"
            )
        if (
            self.algorithm != _ALGORITHM
            or self.canonicalization_version != _CANONICALIZATION_VERSION
            or len(self.digest) != 64
            or any(character not in "0123456789abcdef" for character in self.digest)
        ):
            raise ValueError("invalid transition content identity")


@dataclass(frozen=True, slots=True)
class CanonicalTransitionManifest:
    """An immutable canonical-content snapshot with a digest reference."""

    canonical_bytes: bytes
    content_id: TransitionContentIdentity
    _manifest_token: object | None = None

    def __post_init__(self) -> None:
        if self._manifest_token is not _CONTENT_ID_TOKEN:
            raise ValueError(
                "canonical transition manifests must be issued by "
                "CanonicalTransitionEncoder"
            )
        digest = hashlib.sha256(self.canonical_bytes).hexdigest()
        if digest != self.content_id.digest:
            raise ValueError("manifest bytes do not match its content digest")


class CanonicalTransitionEncoder:
    """The sole issuer of canonical snapshots and their digest references."""

    @classmethod
    def encode(
        cls, transition: StructurallyAdmissibleTransition
    ) -> CanonicalTransitionManifest:
        if type(transition) is not StructurallyAdmissibleTransition:
            raise TypeError("canonical encoding requires an admitted transition")
        cls._assert_schema_coverage()
        encoded = cls._encode_transition(transition)
        canonical_bytes = json.dumps(
            encoded, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        ).encode("utf-8", "surrogatepass")
        content_id = TransitionContentIdentity(
            algorithm=_ALGORITHM,
            canonicalization_version=_CANONICALIZATION_VERSION,
            digest=hashlib.sha256(canonical_bytes).hexdigest(),
            _content_id_token=_CONTENT_ID_TOKEN,
        )
        return CanonicalTransitionManifest(
            canonical_bytes=canonical_bytes,
            content_id=content_id,
            _manifest_token=_CONTENT_ID_TOKEN,
        )

    @staticmethod
    def _assert_schema_coverage() -> None:
        transition_fields = {
            field.name for field in fields(StructurallyAdmissibleTransition)
        }
        accounted_for = set(MANIFEST_COVERAGE) | set(OCCURRENCE_ONLY_EXCLUSIONS)
        if transition_fields != accounted_for:
            raise RuntimeError(
                "canonical transition manifest coverage must explicitly account "
                "for every structurally admissible transition field"
            )

    @classmethod
    def _encode_transition(cls, transition: StructurallyAdmissibleTransition) -> object:
        return {
            "anchor": cls._anchor(transition.anchor),
            "after_state": cls._state(transition.after_state),
            "before_state": cls._state(transition.before_state),
            "branch_origin_provenance": (
                None
                if transition.branch_origin_provenance is None
                else cls._branch_origin_provenance(transition.branch_origin_provenance)
            ),
            "changed": cls._set_of_strings(transition.changed),
            "claim": cls._claim(transition.claim),
            "evidence": [cls._evidence(item) for item in transition.evidence],
            "kind": transition.kind.name,
            "operation": cls._operation(transition.operation),
            "preserved": cls._set_of_strings(transition.preserved),
            "residuals": [cls._residual(item) for item in transition.residuals],
            "result": None
            if transition.result is None
            else cls._result(transition.result),
            "target_anchor": (
                None
                if transition.target_anchor is None
                else cls._anchor(transition.target_anchor)
            ),
            "trace": cls._trace(transition.trace),
            "version": _CANONICALIZATION_VERSION,
        }

    @staticmethod
    def _anchor(value: Anchor) -> object:
        return {"domain": value.domain, "identifier": value.identifier}

    @classmethod
    def _state(cls, value: State) -> object:
        return {"value": cls._value(value.value, set())}

    @staticmethod
    def _operation(value: Operation) -> object:
        return {
            "declared_change": value.declared_change,
            "name": value.name,
            "source_domain": value.source_domain,
            "target_domain": value.target_domain,
        }

    @staticmethod
    def _claim(value: Claim) -> object:
        return {"claim_id": value.claim_id, "statement": value.statement}

    @staticmethod
    def _evidence(value: Evidence) -> object:
        return {"basis": value.basis, "claim_id": value.claim_id}

    @classmethod
    def _result(cls, value: OperationResult) -> object:
        return {"value": cls._value(value.value, set())}

    @staticmethod
    def _trace(value: Trace) -> object:
        return {"events": list(value.events)}

    @staticmethod
    def _residual(value: Residual) -> object:
        return {"description": value.description}

    @classmethod
    def _branch_origin_provenance(cls, value: BranchOriginProvenance) -> object:
        return {
            "branch_anchor": cls._anchor(value.branch_anchor),
            "origin_anchor": cls._anchor(value.origin_anchor),
            "preserved_components": cls._set_of_strings(value.preserved_components),
        }

    @staticmethod
    def _set_of_strings(values: tuple[str, ...]) -> list[str]:
        return sorted(values)

    @classmethod
    def _value(cls, value: object, active_containers: set[int]) -> object:
        value_type = type(value)
        if value is None:
            return ["none"]
        if value_type is bool:
            return ["bool", value]
        if value_type is int:
            return ["int", str(value)]
        if value_type is float:
            float_value = cast(float, value)
            if not math.isfinite(float_value):
                raise TypeError("canonical values cannot contain non-finite floats")
            return ["float64", struct.pack(">d", float_value).hex()]
        if value_type is str:
            return ["str", value]
        if value_type is bytes:
            return ["bytes", base64.b64encode(cast(bytes, value)).decode("ascii")]
        if value_type in (list, tuple, dict, set, frozenset):
            identifier = id(value)
            if identifier in active_containers:
                raise TypeError("canonical values cannot contain cycles")
            active_containers.add(identifier)
            try:
                if value_type is list:
                    list_value = cast(list[object], value)
                    return [
                        "list",
                        [cls._value(item, active_containers) for item in list_value],
                    ]
                if value_type is tuple:
                    tuple_value = cast(tuple[object, ...], value)
                    return [
                        "tuple",
                        [cls._value(item, active_containers) for item in tuple_value],
                    ]
                if value_type is dict:
                    dict_value = cast(dict[object, object], value)
                    entries = [
                        [
                            cls._value(key, active_containers),
                            cls._value(item, active_containers),
                        ]
                        for key, item in dict_value.items()
                    ]
                    return ["dict", sorted(entries, key=cls._sort_key)]
                set_value = cast(set[object] | frozenset[object], value)
                items = [cls._value(item, active_containers) for item in set_value]
                return [
                    "set" if value_type is set else "frozenset",
                    sorted(items, key=cls._sort_key),
                ]
            finally:
                active_containers.remove(identifier)
        raise TypeError(f"unsupported canonical value type: {value_type.__qualname__}")

    @staticmethod
    def _sort_key(value: object) -> str:
        return json.dumps(
            value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        )
