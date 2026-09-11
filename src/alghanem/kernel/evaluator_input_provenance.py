"""G0.BA.1b: evidence-derived evaluator input provenance.

This module closes exactly one of the three claims G0.BA.1a explicitly
refused to make: ``InputProvenance = DECLARED_DEFERRED``. G0.BA.1a invokes a
registry-bound implementation on *caller-supplied* ``input_content`` and
attaches the request's own ``AuthorizedEvidenceSnapshot`` for audit, but
nothing there relates the two (``EvidenceAttachedToRecord !=
EvaluatorExecutedOnEvidence``). A record therefore proves an implementation
ran on *some* content alongside *some* evidence, not that the one came from
the other.

The fix here is structural, not a comparison bolted onto the old gate:

* ``EvaluatorInputDerivation`` receives exactly one argument -- the
  ``canonical_bytes`` of the request's own authorized evidence manifest. It
  is never handed anything else, so it cannot return content sourced from
  outside that snapshot except by ignoring its input, which the recorded
  derivation identity then exposes.
* ``EvaluatorInputDerivationGate.derive`` takes **no** ``input_content``
  parameter at all (``CallerDoesNotOwnInputContent``). The caller chooses
  *which* authorized derivation runs; it never chooses what the evaluator
  sees.
* ``CanonicalEvaluatorInputDerivationEncoder`` digests the source evidence
  content identity, the derivation id, the implementation identity, and the
  produced content together, so the resulting
  ``EvaluatorInputContentIdentity`` binds *what was produced*, *from which
  exact evidence*, and *by which declared derivation* -- not merely the
  output bytes (``OutputDigest != DerivationIdentity``).

G0.BA.1a is left completely unchanged. Its gate still accepts unrelated
input content by design, and this stage layers above it rather than
weakening it: ``ProvenanceBoundEvaluatorExecutionGate.execute`` delegates to
``BirthEvaluatorExecutionGate.execute`` and then binds the resulting record
to the derivation that produced its input.

Claims this module still explicitly does **not** make:

* ``DerivationIdIsContentAuthenticated = DEFERRED``. ``derivation_id`` and
  ``implementation_identity`` are plain, caller-chosen strings, exactly as
  in G0.BA.1a. There is no canonical manifest or digest of the derivation
  *code*: ``DeclaredDerivationId != DerivationContentIdentity``. What is
  proven is that *this* record's input came from *this* evidence through
  *the* callable registered under that name -- not that the name describes
  the callable truthfully.
* ``ObservedDeterminism != ProvenPurity``. The gate invokes the derivation
  twice on identical bytes and rejects differing results. That rejects
  observed nondeterminism at derivation time; it does not prove the
  derivation is pure, side-effect free, or stable across processes.
* ``AuthorizedDefinition != DefinitionAuthorizedForThisFrozenExperiment``
  is inherited unchanged from G0.BA.1a: the execution boundary still
  matches only ``domain``.
* ``ProvenInputProvenance != AssessedEvidence``. A provenance-bound record
  carries no residual evaluation result, weaker-model exhaustion, closure,
  ``BirthCandidate``, ``IndependentClosure``, ``BirthVerdict``, or
  ``Freeze`` meaning. Knowing an evaluator truly ran on the authorized
  evidence says nothing about what its output means:
  ``Derivation != ExecutionRecord != Assessment``.
"""

from __future__ import annotations

import hashlib
import threading
from collections.abc import Callable
from dataclasses import dataclass, field

from .birth import (
    AuthorizedBirthAssessmentEvaluatorDefinition,
    BirthAssessmentRequest,
    BirthEvaluatorRole,
    BirthExperimentSpecificationError,
)
from .evaluator_execution import (
    BirthEvaluatorExecutionGate,
    BirthEvaluatorExecutionRecord,
    SealedBirthEvaluatorImplementationRegistry,
)
from .evidence_acquisition import AuthorizedEvidenceSnapshot, EvidenceContentIdentity
from .trace import Trace

_PROVENANCE_TOKEN = object()
_ALGORITHM = "sha256"
_CANONICALIZATION_VERSION = "evaluator-input-derivation-manifest-v1"


class EvaluatorInputProvenanceError(BirthExperimentSpecificationError):
    """Evaluator input was produced outside its derivation authority boundary."""


def _require_text(value: object, field_name: str) -> None:
    if type(value) is not str or not value.strip():
        raise EvaluatorInputProvenanceError(f"{field_name} must be non-blank text")


# A derivation receives the authorized evidence snapshot's own canonical
# bytes -- and nothing else -- and returns the exact content an evaluator
# will be executed on. It carries no role-specific meaning: this module does
# not know, and must not encode, what any particular derivation computes.
EvaluatorInputDerivation = Callable[[bytes], str]


@dataclass(frozen=True, slots=True)
class EvaluatorInputContentIdentity:
    """A digest reference binding derived input to its exact evidence source.

    This is not an ``EvidenceContentIdentity``: it identifies the triple
    (source evidence content identity, declared derivation, produced
    content), so two derivations that happen to produce byte-identical
    output from different evidence remain distinguishable
    (``OutputDigest != DerivationIdentity``).
    """

    algorithm: str
    canonicalization_version: str
    digest: str
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _PROVENANCE_TOKEN:
            raise EvaluatorInputProvenanceError(
                "evaluator input content identities must be issued by "
                "CanonicalEvaluatorInputDerivationEncoder"
            )
        if (
            self.algorithm != _ALGORITHM
            or self.canonicalization_version != _CANONICALIZATION_VERSION
            or len(self.digest) != 64
            or any(character not in "0123456789abcdef" for character in self.digest)
        ):
            raise EvaluatorInputProvenanceError(
                "invalid evaluator input content identity"
            )


@dataclass(frozen=True, slots=True)
class CanonicalEvaluatorInputDerivationManifest:
    """The complete canonical content of one evidence-derived evaluator input."""

    canonical_bytes: bytes
    content_id: EvaluatorInputContentIdentity
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _PROVENANCE_TOKEN:
            raise EvaluatorInputProvenanceError(
                "canonical evaluator input manifests must be issued by "
                "CanonicalEvaluatorInputDerivationEncoder"
            )
        if hashlib.sha256(self.canonical_bytes).hexdigest() != self.content_id.digest:
            raise EvaluatorInputProvenanceError(
                "manifest bytes do not match its content digest"
            )


class CanonicalEvaluatorInputDerivationEncoder:
    """The sole issuer of evaluator input manifests and content identities."""

    @classmethod
    def encode(
        cls,
        *,
        source_content_id: EvidenceContentIdentity,
        derivation_id: str,
        implementation_identity: str,
        input_content: str,
    ) -> CanonicalEvaluatorInputDerivationManifest:
        """Encode the derived input together with the source it came from."""

        if type(source_content_id) is not EvidenceContentIdentity:
            raise EvaluatorInputProvenanceError(
                "evaluator input encoding requires an authorized evidence "
                "content identity"
            )
        _require_text(derivation_id, "evaluator input derivation id")
        _require_text(implementation_identity, "evaluator input derivation identity")
        if type(input_content) is not str:
            raise EvaluatorInputProvenanceError(
                "canonical evaluator input encoding requires a text payload"
            )
        _require_text(input_content, "derived evaluator input content")

        # Every part is length-prefixed so no two distinct tuples can share a
        # canonical encoding by concatenation.
        parts = (
            _CANONICALIZATION_VERSION,
            source_content_id.algorithm,
            source_content_id.canonicalization_version,
            source_content_id.digest,
            derivation_id,
            implementation_identity,
            input_content,
        )
        canonical_bytes = b"".join(
            f"{len(encoded)}:".encode("ascii") + encoded
            for encoded in (part.encode("utf-8", "surrogatepass") for part in parts)
        )
        content_id = EvaluatorInputContentIdentity(
            algorithm=_ALGORITHM,
            canonicalization_version=_CANONICALIZATION_VERSION,
            digest=hashlib.sha256(canonical_bytes).hexdigest(),
            _token=_PROVENANCE_TOKEN,
        )
        return CanonicalEvaluatorInputDerivationManifest(
            canonical_bytes=canonical_bytes,
            content_id=content_id,
            _token=_PROVENANCE_TOKEN,
        )


@dataclass(frozen=True, slots=True)
class AuthorizedEvaluatorInputDerivationBinding:
    """Authority-issued binding of one declared derivation to one callable.

    Constructible only by ``EvaluatorInputDerivationRegistry.register``. The
    ``declared_transformation`` text is carried for audit and is never
    verified against the callable: ``DeclaredTransformation !=
    VerifiedTransformation``.
    """

    domain: str
    derivation_id: str
    implementation_identity: str
    declared_transformation: str
    derivation: EvaluatorInputDerivation = field(repr=False, compare=False)
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _PROVENANCE_TOKEN:
            raise EvaluatorInputProvenanceError(
                "evaluator input derivation bindings must be issued by "
                "EvaluatorInputDerivationRegistry"
            )
        _require_text(self.domain, "evaluator input derivation domain")
        _require_text(self.derivation_id, "evaluator input derivation id")
        _require_text(
            self.implementation_identity, "evaluator input derivation identity"
        )
        _require_text(
            self.declared_transformation, "evaluator input declared transformation"
        )
        if not callable(self.derivation):
            raise EvaluatorInputProvenanceError(
                "an evaluator input derivation binding requires an executable "
                "callable"
            )


class EvaluatorInputDerivationRegistry:
    """Authority that issues and seals evaluator input derivation bindings."""

    def __init__(self) -> None:
        self._bindings: dict[
            tuple[str, str, str], AuthorizedEvaluatorInputDerivationBinding
        ] = {}
        self._lock = threading.Lock()

    def register(
        self,
        *,
        domain: str,
        derivation_id: str,
        implementation_identity: str,
        declared_transformation: str,
        derivation: EvaluatorInputDerivation,
    ) -> AuthorizedEvaluatorInputDerivationBinding:
        """Authorize exactly one derivation callable for one exact scope."""

        binding = AuthorizedEvaluatorInputDerivationBinding(
            domain=domain,
            derivation_id=derivation_id,
            implementation_identity=implementation_identity,
            declared_transformation=declared_transformation,
            derivation=derivation,
            _token=_PROVENANCE_TOKEN,
        )
        key = (binding.domain, binding.derivation_id, binding.implementation_identity)
        with self._lock:
            if key in self._bindings:
                raise EvaluatorInputProvenanceError(
                    "a derivation is already bound to this exact domain, "
                    "derivation id, and implementation identity"
                )
            self._bindings[key] = binding
        return binding

    def seal(self, snapshot_id: str) -> SealedEvaluatorInputDerivationRegistry:
        """Freeze the registered derivation bindings."""

        _require_text(snapshot_id, "derivation registry snapshot id")
        with self._lock:
            bindings = tuple(self._bindings.values())
        return SealedEvaluatorInputDerivationRegistry(
            snapshot_id=snapshot_id,
            bindings=bindings,
            _token=_PROVENANCE_TOKEN,
        )


@dataclass(frozen=True, slots=True)
class SealedEvaluatorInputDerivationRegistry:
    """Frozen derivation snapshot; it authorizes callables but derives nothing."""

    snapshot_id: str
    bindings: tuple[AuthorizedEvaluatorInputDerivationBinding, ...]
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _PROVENANCE_TOKEN:
            raise EvaluatorInputProvenanceError(
                "sealed derivation registries must be issued by "
                "EvaluatorInputDerivationRegistry"
            )
        _require_text(self.snapshot_id, "derivation registry snapshot id")
        if type(self.bindings) is not tuple or any(
            type(item) is not AuthorizedEvaluatorInputDerivationBinding
            for item in self.bindings
        ):
            raise EvaluatorInputProvenanceError(
                "sealed derivation registries require authorized derivation " "bindings"
            )
        seen: set[tuple[str, str, str]] = set()
        for binding in self.bindings:
            key = (
                binding.domain,
                binding.derivation_id,
                binding.implementation_identity,
            )
            if key in seen:
                raise EvaluatorInputProvenanceError(
                    "sealed derivation registry must not contain duplicate scopes"
                )
            seen.add(key)

    def resolve(
        self,
        *,
        domain: str,
        derivation_id: str,
        implementation_identity: str,
    ) -> AuthorizedEvaluatorInputDerivationBinding:
        """Return the exact registry-issued binding for this three-part scope."""

        for binding in self.bindings:
            if (
                binding.domain == domain
                and binding.derivation_id == derivation_id
                and binding.implementation_identity == implementation_identity
            ):
                return binding
        raise EvaluatorInputProvenanceError(
            "no authorized derivation is bound to this exact domain, derivation "
            "id, and implementation identity"
        )


@dataclass(frozen=True, slots=True)
class EvidenceDerivedEvaluatorInput:
    """Gate-issued proof that this content came from this exact evidence.

    ``input_content`` is not caller-supplied at any point: it is whatever the
    registry-owned derivation returned when handed the request's own
    authorized evidence bytes. ``content_id`` binds that content to the
    source evidence identity and to the declared derivation, so substituting
    either changes the identity.

    ``ProvenInputProvenance != AssessedEvidence``: holding one of these
    proves where evaluator input came from and nothing about what it means.
    """

    binding: AuthorizedEvaluatorInputDerivationBinding
    request: BirthAssessmentRequest
    evidence_snapshot: AuthorizedEvidenceSnapshot
    source_content_id: EvidenceContentIdentity
    input_content: str
    derivation_manifest: CanonicalEvaluatorInputDerivationManifest
    trace: Trace
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _PROVENANCE_TOKEN:
            raise EvaluatorInputProvenanceError(
                "evidence-derived evaluator inputs must be issued by "
                "EvaluatorInputDerivationGate"
            )
        if type(self.binding) is not AuthorizedEvaluatorInputDerivationBinding:
            raise EvaluatorInputProvenanceError(
                "a derived evaluator input requires an authorized derivation " "binding"
            )
        if type(self.request) is not BirthAssessmentRequest:
            raise EvaluatorInputProvenanceError(
                "a derived evaluator input requires an authorized assessment " "request"
            )
        if type(self.evidence_snapshot) is not AuthorizedEvidenceSnapshot:
            raise EvaluatorInputProvenanceError(
                "a derived evaluator input requires an authorized evidence " "snapshot"
            )
        if self.evidence_snapshot is not self.request.evidence_snapshot:
            raise EvaluatorInputProvenanceError(
                "derived evaluator input evidence must be the request's own "
                "bound evidence snapshot"
            )
        if self.source_content_id != self.evidence_snapshot.content_id:
            raise EvaluatorInputProvenanceError(
                "derived evaluator input source must be the evidence snapshot's "
                "own content identity"
            )
        _require_text(self.input_content, "derived evaluator input content")
        if (
            type(self.derivation_manifest)
            is not CanonicalEvaluatorInputDerivationManifest
        ):
            raise EvaluatorInputProvenanceError(
                "a derived evaluator input requires a canonical derivation " "manifest"
            )
        expected = CanonicalEvaluatorInputDerivationEncoder.encode(
            source_content_id=self.source_content_id,
            derivation_id=self.binding.derivation_id,
            implementation_identity=self.binding.implementation_identity,
            input_content=self.input_content,
        )
        if expected.content_id != self.derivation_manifest.content_id:
            raise EvaluatorInputProvenanceError(
                "derivation manifest does not match this input, its source "
                "evidence, and its declared derivation"
            )
        if type(self.trace) is not Trace:
            raise EvaluatorInputProvenanceError(
                "a derived evaluator input requires a trace"
            )

    @property
    def content_id(self) -> EvaluatorInputContentIdentity:
        """The identity binding this input to its evidence and derivation."""

        return self.derivation_manifest.content_id

    @property
    def domain(self) -> str:
        return self.binding.domain

    @property
    def derivation_id(self) -> str:
        return self.binding.derivation_id

    @property
    def implementation_identity(self) -> str:
        return self.binding.implementation_identity


class EvaluatorInputDerivationGate:
    """The sole authority that may produce evaluator input from evidence.

    ``CallerDoesNotOwnInputContent``: ``derive`` accepts no input content and
    no domain. The domain is read from the request's own frozen experiment,
    and the content is produced by the resolved, registry-owned derivation
    from the request's own authorized evidence bytes.
    """

    @staticmethod
    def derive(
        *,
        registry: SealedEvaluatorInputDerivationRegistry,
        request: BirthAssessmentRequest,
        derivation_id: str,
        implementation_identity: str,
    ) -> EvidenceDerivedEvaluatorInput:
        """Derive one evaluator input from this request's own evidence."""

        if type(registry) is not SealedEvaluatorInputDerivationRegistry:
            raise EvaluatorInputProvenanceError(
                "input derivation requires a sealed derivation registry"
            )
        if type(request) is not BirthAssessmentRequest:
            raise EvaluatorInputProvenanceError(
                "input derivation requires an authorized assessment request"
            )
        _require_text(derivation_id, "evaluator input derivation id")
        _require_text(implementation_identity, "evaluator input derivation identity")

        snapshot = request.evidence_snapshot
        binding = registry.resolve(
            domain=request.specification.domain,
            derivation_id=derivation_id,
            implementation_identity=implementation_identity,
        )

        source_bytes = snapshot.evidence_manifest.canonical_bytes
        if hashlib.sha256(source_bytes).hexdigest() != snapshot.content_id.digest:
            raise EvaluatorInputProvenanceError(
                "authorized evidence bytes do not match the snapshot's own "
                "content identity"
            )

        produced = binding.derivation(source_bytes)
        if type(produced) is not str:
            raise EvaluatorInputProvenanceError(
                "a bound derivation must return evaluator input as text"
            )
        _require_text(produced, "derived evaluator input content")
        # ObservedDeterminism != ProvenPurity: this rejects observed
        # nondeterminism, it does not prove the derivation is pure.
        if binding.derivation(source_bytes) != produced:
            raise EvaluatorInputProvenanceError(
                "a bound derivation must return the same content for the same "
                "authorized evidence bytes"
            )

        manifest = CanonicalEvaluatorInputDerivationEncoder.encode(
            source_content_id=snapshot.content_id,
            derivation_id=binding.derivation_id,
            implementation_identity=binding.implementation_identity,
            input_content=produced,
        )
        return EvidenceDerivedEvaluatorInput(
            binding=binding,
            request=request,
            evidence_snapshot=snapshot,
            source_content_id=snapshot.content_id,
            input_content=produced,
            derivation_manifest=manifest,
            trace=Trace(
                (
                    f"resolved derivation {binding.derivation_id} "
                    f"({binding.implementation_identity}) for domain "
                    f"{binding.domain}",
                    f"derived evaluator input from evidence snapshot "
                    f"{snapshot.snapshot_id}",
                )
            ),
            _token=_PROVENANCE_TOKEN,
        )


@dataclass(frozen=True, slots=True)
class ProvenanceBoundEvaluatorExecutionRecord:
    """One G0.BA.1a execution record bound to the derivation that fed it.

    Unlike a bare ``BirthEvaluatorExecutionRecord``, this record does prove
    ``EvaluatorExecutedOnEvidence`` for its own input: the executed content
    is exactly what the registry-owned derivation produced from this
    request's own authorized evidence snapshot. It proves nothing further --
    no residual survival, weaker-model exhaustion, closure, candidacy,
    verdict, or freeze.
    """

    execution_record: BirthEvaluatorExecutionRecord
    derived_input: EvidenceDerivedEvaluatorInput
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _PROVENANCE_TOKEN:
            raise EvaluatorInputProvenanceError(
                "provenance-bound execution records must be issued by "
                "ProvenanceBoundEvaluatorExecutionGate"
            )
        if type(self.execution_record) is not BirthEvaluatorExecutionRecord:
            raise EvaluatorInputProvenanceError(
                "a provenance-bound record requires a gate-issued execution " "record"
            )
        if type(self.derived_input) is not EvidenceDerivedEvaluatorInput:
            raise EvaluatorInputProvenanceError(
                "a provenance-bound record requires a gate-issued derived "
                "evaluator input"
            )
        if self.execution_record.request is not self.derived_input.request:
            raise EvaluatorInputProvenanceError(
                "execution and derivation must share the same authorized "
                "assessment request"
            )
        if (
            self.execution_record.evidence_snapshot
            is not self.derived_input.evidence_snapshot
        ):
            raise EvaluatorInputProvenanceError(
                "execution and derivation must share the same authorized "
                "evidence snapshot"
            )
        if self.execution_record.input_content != self.derived_input.input_content:
            raise EvaluatorInputProvenanceError(
                "executed input content must be the derived evaluator input"
            )

    @property
    def definition(self) -> AuthorizedBirthAssessmentEvaluatorDefinition:
        return self.execution_record.definition

    @property
    def role(self) -> BirthEvaluatorRole:
        return self.execution_record.role

    @property
    def target_id(self) -> str:
        return self.execution_record.target_id

    @property
    def input_content(self) -> str:
        return self.derived_input.input_content

    @property
    def output_content(self) -> str:
        return self.execution_record.output_content

    @property
    def trace(self) -> Trace:
        return self.execution_record.trace

    @property
    def evidence_content_id(self) -> EvidenceContentIdentity:
        """The authorized evidence the executed input was derived from."""

        return self.derived_input.source_content_id

    @property
    def input_content_id(self) -> EvaluatorInputContentIdentity:
        """The identity binding executed input to evidence and derivation."""

        return self.derived_input.content_id

    @property
    def is_assessment(self) -> bool:
        """Always ``False``: proven provenance is not an assessment.

        Knowing that an evaluator truly ran on the authorized evidence says
        nothing about residual survival, weaker-model exhaustion, closure,
        candidacy, or birth. Those remain separate, later, and still
        unauthorized questions.
        """

        return False


class ProvenanceBoundEvaluatorExecutionGate:
    """The sole authority issuing provenance-bound execution records.

    It delegates the invocation itself to ``BirthEvaluatorExecutionGate``,
    which is preserved unchanged, and then binds the issued record to the
    derivation that produced its input. Callers cannot supply input content
    here either: it comes only from an already gate-issued
    ``EvidenceDerivedEvaluatorInput``.
    """

    @staticmethod
    def execute(
        *,
        definition: AuthorizedBirthAssessmentEvaluatorDefinition,
        implementation_identity: str,
        registry: SealedBirthEvaluatorImplementationRegistry,
        derived_input: EvidenceDerivedEvaluatorInput,
    ) -> ProvenanceBoundEvaluatorExecutionRecord:
        """Execute a bound implementation on evidence-derived input only."""

        if type(derived_input) is not EvidenceDerivedEvaluatorInput:
            raise EvaluatorInputProvenanceError(
                "provenance-bound execution requires a gate-issued derived "
                "evaluator input"
            )
        record = BirthEvaluatorExecutionGate.execute(
            definition=definition,
            implementation_identity=implementation_identity,
            registry=registry,
            request=derived_input.request,
            input_content=derived_input.input_content,
        )
        return ProvenanceBoundEvaluatorExecutionRecord(
            execution_record=record,
            derived_input=derived_input,
            _token=_PROVENANCE_TOKEN,
        )
