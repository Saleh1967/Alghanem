"""G0.BA.1a: authorized evaluator implementation binding and execution.

This module closes exactly one question: can an already registry-authorized
birth evaluator definition (`AuthorizedBirthAssessmentEvaluatorDefinition`,
issued under G0.2a) be bound to an exact implementation identity and executed
through an authority boundary that produces a non-caller-constructible
execution record?

It does not answer, and must not be read as answering, any question about
residual survival, weaker-model exhaustion, closure, birth candidacy,
independent closure, birth verdicts, or freeze. ``Definition !=
ImplementationBinding != ExecutionRecord != Assessment``:

* ``AuthorizedBirthAssessmentEvaluatorDefinition`` (G0.2a) authorizes a
  *declaration* only; it is preserved unchanged here and gains no execution
  semantics.
* ``AuthorizedBirthEvaluatorImplementationBinding`` binds that exact
  declaration to one implementation identity and one executable callable.
  It is issued only by ``BirthEvaluatorImplementationRegistry``; callers
  cannot construct it directly.
* ``BirthEvaluatorExecutionRecord`` is the auditable record of one execution
  of a bound implementation. It is issued only by
  ``BirthEvaluatorExecutionGate.execute`` and carries no assessment,
  survival, exhaustion, closure, verdict, or freeze meaning.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import InitVar, dataclass, field
from threading import Lock

from .birth import (
    AuthorizedBirthAssessmentEvaluatorDefinition,
    BirthAssessmentRequest,
    BirthEvaluatorRole,
    BirthExperimentSpecificationError,
)
from .evidence_acquisition import AuthorizedEvidenceSnapshot
from .trace import Trace

_BINDING_TOKEN = object()
_REGISTRY_TOKEN = object()
_EXECUTION_TOKEN = object()


class BirthEvaluatorExecutionError(BirthExperimentSpecificationError):
    """An evaluator id or declaration alone cannot execute an assessment."""


def _require_text(value: object, field_name: str) -> None:
    if type(value) is not str or not value.strip():
        raise BirthEvaluatorExecutionError(f"{field_name} must be non-blank text")


# An implementation receives arbitrary input content and returns its output
# content together with an auditable trace of what it did. It carries no
# role-specific meaning: this module does not know, and must not encode,
# what "residual", "weaker model", or "closure" mean for any given content.
BirthEvaluatorImplementation = Callable[[str], tuple[str, Trace]]


@dataclass(frozen=True, slots=True, init=False)
class AuthorizedBirthEvaluatorImplementationBinding:
    """Authority-issued binding of one authorized definition to one implementation.

    Constructible only by ``BirthEvaluatorImplementationRegistry.register``,
    which requires an actual, already registry-issued
    ``AuthorizedBirthAssessmentEvaluatorDefinition`` -- never a
    caller-fabricated stand-in.
    """

    definition: AuthorizedBirthAssessmentEvaluatorDefinition
    implementation_identity: str
    implementation: BirthEvaluatorImplementation = field(repr=False, compare=False)

    def __init__(
        self,
        definition: AuthorizedBirthAssessmentEvaluatorDefinition,
        implementation_identity: str,
        implementation: BirthEvaluatorImplementation,
        *,
        _token: object | None = None,
    ) -> None:
        if _token is not _BINDING_TOKEN:
            raise BirthEvaluatorExecutionError(
                "evaluator implementation bindings must be issued by "
                "BirthEvaluatorImplementationRegistry"
            )
        if type(definition) is not AuthorizedBirthAssessmentEvaluatorDefinition:
            raise BirthEvaluatorExecutionError(
                "an implementation binding requires an authorized evaluator definition"
            )
        _require_text(implementation_identity, "evaluator implementation identity")
        if not callable(implementation):
            raise BirthEvaluatorExecutionError(
                "an implementation binding requires an executable callable"
            )
        object.__setattr__(self, "definition", definition)
        object.__setattr__(self, "implementation_identity", implementation_identity)
        object.__setattr__(self, "implementation", implementation)


class BirthEvaluatorImplementationRegistry:
    """Authority that issues and seals evaluator implementation bindings."""

    def __init__(self) -> None:
        self._bindings: dict[
            tuple[str, BirthEvaluatorRole, str, str, str],
            AuthorizedBirthEvaluatorImplementationBinding,
        ] = {}
        self._lock = Lock()

    def register(
        self,
        definition: AuthorizedBirthAssessmentEvaluatorDefinition,
        implementation_identity: str,
        implementation: BirthEvaluatorImplementation,
    ) -> AuthorizedBirthEvaluatorImplementationBinding:
        """Bind one already authorized definition to one implementation."""

        binding = AuthorizedBirthEvaluatorImplementationBinding(
            definition,
            implementation_identity,
            implementation,
            _token=_BINDING_TOKEN,
        )
        key = (
            definition.domain,
            definition.role,
            definition.target_id,
            definition.evaluator_id,
            implementation_identity,
        )
        with self._lock:
            if key in self._bindings:
                raise BirthEvaluatorExecutionError(
                    "an implementation is already bound to this exact "
                    "definition and implementation identity"
                )
            self._bindings[key] = binding
        return binding

    def seal(self, snapshot_id: str) -> SealedBirthEvaluatorImplementationRegistry:
        """Freeze the registered implementation bindings."""

        _require_text(snapshot_id, "implementation registry snapshot id")
        with self._lock:
            bindings = tuple(self._bindings.values())
        return SealedBirthEvaluatorImplementationRegistry(
            snapshot_id,
            bindings,
            _registry_token=_REGISTRY_TOKEN,
        )


@dataclass(frozen=True, slots=True)
class SealedBirthEvaluatorImplementationRegistry:
    """Frozen registry snapshot; it authorizes bindings but executes nothing."""

    snapshot_id: str
    bindings: tuple[AuthorizedBirthEvaluatorImplementationBinding, ...]
    _registry_token: InitVar[object | None] = field(default=None, repr=False)

    def __post_init__(self, _registry_token: object | None) -> None:
        if _registry_token is not _REGISTRY_TOKEN:
            raise BirthEvaluatorExecutionError(
                "sealed implementation registries must be issued by "
                "BirthEvaluatorImplementationRegistry"
            )
        _require_text(self.snapshot_id, "implementation registry snapshot id")
        if type(self.bindings) is not tuple or any(
            type(item) is not AuthorizedBirthEvaluatorImplementationBinding
            for item in self.bindings
        ):
            raise BirthEvaluatorExecutionError(
                "sealed implementation registries require frozen bindings"
            )
        seen: set[tuple[str, BirthEvaluatorRole, str, str, str]] = set()
        for binding in self.bindings:
            key = (
                binding.definition.domain,
                binding.definition.role,
                binding.definition.target_id,
                binding.definition.evaluator_id,
                binding.implementation_identity,
            )
            if key in seen:
                raise BirthEvaluatorExecutionError(
                    "sealed implementation registry must not contain duplicate bindings"
                )
            seen.add(key)

    def resolve(
        self,
        *,
        domain: str,
        role: BirthEvaluatorRole,
        target_id: str,
        evaluator_id: str,
        implementation_identity: str,
    ) -> AuthorizedBirthEvaluatorImplementationBinding:
        """Return the exact registry-issued binding for this scope."""

        for binding in self.bindings:
            definition = binding.definition
            if (
                definition.domain == domain
                and definition.role is role
                and definition.target_id == target_id
                and definition.evaluator_id == evaluator_id
                and binding.implementation_identity == implementation_identity
            ):
                return binding
        raise BirthEvaluatorExecutionError(
            "no authorized implementation is bound to this exact "
            "definition and implementation identity"
        )


@dataclass(frozen=True, slots=True)
class BirthEvaluatorExecutionRecord:
    """The gate-issued record of one execution of a bound implementation.

    This record proves that a specific, registry-bound implementation ran
    against a specific, authorized request's evidence. It carries no
    assessment, survival, exhaustion, closure, verdict, or freeze meaning:
    those remain separate, later, and still-deferred authorities.
    """

    definition: AuthorizedBirthAssessmentEvaluatorDefinition
    implementation_identity: str
    role: BirthEvaluatorRole
    target_id: str
    request: BirthAssessmentRequest
    evidence_snapshot: AuthorizedEvidenceSnapshot
    input_content: str
    output_content: str
    trace: Trace
    _execution_token: InitVar[object | None] = field(default=None, repr=False)

    def __post_init__(self, _execution_token: object | None) -> None:
        if _execution_token is not _EXECUTION_TOKEN:
            raise BirthEvaluatorExecutionError(
                "evaluator execution records must be issued by "
                "BirthEvaluatorExecutionGate"
            )
        if type(self.definition) is not AuthorizedBirthAssessmentEvaluatorDefinition:
            raise BirthEvaluatorExecutionError(
                "an execution record requires an authorized evaluator definition"
            )
        _require_text(self.implementation_identity, "evaluator implementation identity")
        if self.role is not self.definition.role:
            raise BirthEvaluatorExecutionError(
                "execution record role must match the authorized definition"
            )
        if self.target_id != self.definition.target_id:
            raise BirthEvaluatorExecutionError(
                "execution record target must match the authorized definition"
            )
        if type(self.request) is not BirthAssessmentRequest:
            raise BirthEvaluatorExecutionError(
                "an execution record requires an authorized assessment request"
            )
        if self.request.specification.domain != self.definition.domain:
            raise BirthEvaluatorExecutionError(
                "execution record request domain must match the authorized "
                "definition domain"
            )
        if type(self.evidence_snapshot) is not AuthorizedEvidenceSnapshot:
            raise BirthEvaluatorExecutionError(
                "an execution record requires an authorized evidence snapshot"
            )
        if self.evidence_snapshot is not self.request.evidence_snapshot:
            raise BirthEvaluatorExecutionError(
                "execution record evidence must be the request's own bound "
                "evidence snapshot"
            )
        _require_text(self.input_content, "execution input content")
        if type(self.output_content) is not str:
            raise BirthEvaluatorExecutionError("execution output content must be text")
        if type(self.trace) is not Trace:
            raise BirthEvaluatorExecutionError("an execution record requires a trace")


class BirthEvaluatorExecutionGate:
    """The sole authority that may invoke a bound implementation."""

    @staticmethod
    def execute(
        *,
        definition: AuthorizedBirthAssessmentEvaluatorDefinition,
        implementation_identity: str,
        registry: SealedBirthEvaluatorImplementationRegistry,
        request: BirthAssessmentRequest,
        input_content: str,
    ) -> BirthEvaluatorExecutionRecord:
        """Execute the exact bound implementation and record the result."""

        if type(definition) is not AuthorizedBirthAssessmentEvaluatorDefinition:
            raise BirthEvaluatorExecutionError(
                "execution requires an authorized evaluator definition"
            )
        _require_text(implementation_identity, "evaluator implementation identity")
        if type(registry) is not SealedBirthEvaluatorImplementationRegistry:
            raise BirthEvaluatorExecutionError(
                "execution requires a sealed implementation registry"
            )
        if type(request) is not BirthAssessmentRequest:
            raise BirthEvaluatorExecutionError(
                "execution requires an authorized assessment request"
            )
        _require_text(input_content, "execution input content")

        binding = registry.resolve(
            domain=definition.domain,
            role=definition.role,
            target_id=definition.target_id,
            evaluator_id=definition.evaluator_id,
            implementation_identity=implementation_identity,
        )
        if binding.definition != definition:
            raise BirthEvaluatorExecutionError(
                "resolved implementation binding does not match the "
                "authorized definition"
            )

        outcome = binding.implementation(input_content)
        if (
            type(outcome) is not tuple
            or len(outcome) != 2
            or type(outcome[0]) is not str
            or type(outcome[1]) is not Trace
        ):
            raise BirthEvaluatorExecutionError(
                "a bound implementation must return (output_content, trace)"
            )
        output_content, trace = outcome

        return BirthEvaluatorExecutionRecord(
            definition,
            implementation_identity,
            definition.role,
            definition.target_id,
            request,
            request.evidence_snapshot,
            input_content,
            output_content,
            trace,
            _execution_token=_EXECUTION_TOKEN,
        )
