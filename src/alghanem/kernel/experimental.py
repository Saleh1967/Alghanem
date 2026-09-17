"""G0.EX.1a: running what has not been born, without letting the run prove it.

This module closes exactly one question: may something that no authority has
certified be *run* at all, and if so, what does the run prove? The answer is
that it may be run, in a third path that is neither constitutional nor
executive, and that the run proves exactly one thing::

    this declared candidate, under these declared conditions, on these declared
    inputs, produced this output (or this failure)

`ExperimentalSuccess != Birth` and `ExperimentalFailure != NoBirth`. A run does
not prove that a genus was born, that the candidate's identity is independent,
that it differs from the origin it claims to branch from, that it is necessary,
that a weaker model would not have sufficed, or that anything holds outside the
experiment's own declared scope. Those are constitutional questions, decided
elsewhere, on inputs that must pass through G0.EX.1c's conversion gate first.

Three authorities, and this is the third. `ConstitutionalBirthAuthority`
(G0.BC.1a) certifies and runs nothing; `ExecutiveAdmissionGate` admits only what
was certified and certifies nothing; `ExperimentalAuthority` here runs what was
never certified and neither certifies nor admits anything.
`ExperimentalRunIsNotExecutionOfABornEntity`: an `ExperimentalRunRecord` is not
an `ExecutableEntity`, is reachable without any certificate
(`NoBornEntityIsRequiredToRunAnExperiment`), and confers no capability of its
own. This module imports nothing from `birth_verdict`, `birth_certificate`,
`independent_closure`, or `residual_survival`, so no reading here can travel
into a verdict path by import alone.

A run is reachable only through a bound request. `ExperimentalAuthority.run`
accepts no bare `ExperimentalRunRequest`: it takes a `BoundExperimentalRunRequest`
issued elsewhere against a frozen pre-evidence experiment, reads that binding's
canonical request content digest, and stamps it onto the record it issues. This
module defines only the abstract seam and never learns what the request was
bound *to*, so binding a run to a frozen experiment stays outside this
authority while running an unbound request stops being expressible.

`UnpermittedOperationCannotExecute`. An implementation reaches an operation only
through the `ExperimentalRunContext` this authority issues for its own case: the
context refuses an operation the request never permitted *before* invoking it,
the authority alone writes the `operation:` events of the run trace, and an
implementation that writes such an event into its own trace fails the run for
forging the authority's record. The earlier reading -- trusting whatever
operations an implementation chose to report -- was
`ReportedOperationMustBePermitted`, which is a weaker law and no longer the one
enforced here.

Four claims this module explicitly does **not** make:

* ``Isolation = ProcessLocalOnly``. `ExperimentalAuthority.run` invokes a
  caller-supplied implementation in this very process and captures the
  exceptions it raises instead of letting them propagate. That is authority
  isolation -- a failure cannot escape into the caller's control flow as if it
  were the caller's own -- and not a security sandbox: nothing here restricts
  filesystem, network, memory, or time, and an implementation that reaches for
  an ambient effect directly never passes through the capability at all.
  `CapturedFailure != SandboxedExecution`, and
  `MediatedOperation != AmbientEffect`.
* ``DeclaredOrigin != ProvedBranchRelation``. `declared_origin_ref` is a string
  the caller claims the candidate branched from. Nothing checks that such an
  origin exists, that the candidate differs from it, or that a
  `BranchOriginProvenance` could be derived for the pair.
* ``DeclaredCandidateId != ProvedIdentity``. A candidate id names the thing that
  was run inside this process. It is not an identity proof, and two declarations
  sharing an id are not thereby the same candidate.
* ``ObservedCaseReading != CertifiedResidual``. A case the declared model did not
  account for is recorded as an *observation* under a vocabulary frozen before
  the run. It is not a `ResidualCertificationCandidate`, not a certified
  residual, and it does not satisfy `NoBirthWithoutResidualOrFormalNecessity`.

Experimental output is synthetic unless its inputs were themselves measured, so
`CounterfactualResultIsNotObservation` and
`SyntheticInterventionMayGenerateHypothesisOnly` apply to it unchanged: at most
a hypothesis is licensed here, never a birth.

`NoGenusNameIsIntroducedHere`. Candidate and model references are opaque caller
strings. The kernel names no genus -- instruction, rule, general rule, law --
and a contrast between two such models is expressible here only as a contrast
between two opaque references, exactly as `TraditionalNamingOnlyAfterFreezeAndE0`
requires.
"""

from __future__ import annotations

import threading
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field, fields
from enum import Enum
from typing import TypeVar

from alghanem.canonical_content import is_canonical_digest

from .trace import Trace

_EXPERIMENTAL_TOKEN = object()
_CAPABILITY_TOKEN = object()

_OPERATION_EVENT_PREFIX = "operation:"

_T = TypeVar("_T")

_FORBIDDEN_FIELD_NAMES = frozenset(
    {
        "birth",
        "born",
        "certificate",
        "certified",
        "is_born",
        "is_certified",
        "is_correct",
        "is_valid",
        "proved",
        "rank",
        "valid",
        "validity",
        "verdict",
    }
)


class ExperimentalAuthorityError(ValueError):
    """An experimental declaration, run, or record broke its own boundary.

    Deliberately not a subclass of `BirthExperimentSpecificationError`: the
    experimental path is not a stage of the birth path, and an error raised
    here must not be catchable as a birth-protocol error.
    """


EXPERIMENTAL_NAMED_LAWS: dict[str, str] = {
    "ExperimentalSuccessIsNotBirth": (
        "ExperimentalSuccessIsNotBirth: a completed run proves that this "
        "declared candidate, under these declared conditions, produced this "
        "output. It does not prove that a genus was born, that the candidate "
        "is necessary, or that anything holds outside the run's declared scope"
    ),
    "ExperimentalFailureIsNotNoBirth": (
        "ExperimentalFailureIsNotNoBirth: a failed or aborted run proves that "
        "this implementation did not complete under these declared conditions. "
        "It is not a NO_BIRTH_IN_SCOPE verdict, and a failure is kept as a "
        "recorded fact rather than discarded"
    ),
    "ExperimentalCandidateIsNotBirthCandidate": (
        "ExperimentalCandidateIsNotBirthCandidate: no type declared here is, "
        "subclasses, or is accepted anywhere a birth candidate, verdict, "
        "closure reading, or certificate is required. The two paths share no "
        "type and no error class"
    ),
    "NoValidityFieldOnAnExperimentalArtifact": (
        "NoValidityFieldOnAnExperimentalArtifact: no experimental type may "
        "declare a field named for birth, validity, correctness, certification, "
        "rank, or verdict. The prohibition is swept at import time over every "
        "dataclass in this module, so a field added later fails the import "
        "rather than quietly conferring a status"
    ),
    "ObservedUnexplainedCasesIsNotCertifiedResidual": (
        "ObservedUnexplainedCasesIsNotCertifiedResidual: a run records the "
        "cases its declared model did not account for, read through a "
        "vocabulary frozen before the run. That reading is an observation, "
        "never a certified residual, and it satisfies no birth condition"
    ),
    "ExperimentalAuthorityCannotCertifyOrExecute": (
        "ExperimentalAuthorityCannotCertifyOrExecute: this authority exposes "
        "`run` and its own id, and no method that certifies a birth or admits "
        "an entity for use. Successful experimentation is never a route to the "
        "authority that would legitimise it"
    ),
    "NoBornEntityIsRequiredToRunAnExperiment": (
        "NoBornEntityIsRequiredToRunAnExperiment: a run requires no "
        "certificate and no executable entity, which is the whole point of the "
        "third path: the laboratory may try what the constitution has not "
        "admitted"
    ),
    "ExperimentalRunIsNotExecutionOfABornEntity": (
        "ExperimentalRunIsNotExecutionOfABornEntity: a run record is not an "
        "executable entity, cannot be produced from one, and cannot produce "
        "one. Running in the laboratory and using what was born are two acts "
        "under two authorities"
    ),
    "UnpermittedOperationCannotExecute": (
        "UnpermittedOperationCannotExecute: an operation is reachable only "
        "through the authority-issued capability of the case being run, which "
        "refuses an unpermitted operation before invoking it and aborts the "
        "run. The authority alone writes the run's operation events, and an "
        "implementation that writes one into its own trace fails the run "
        "rather than being believed"
    ),
    "NoRunWithoutABoundRequest": (
        "NoRunWithoutABoundRequest: this authority runs a bound request or "
        "nothing. The bare request is not an admissible argument, and the "
        "canonical content digest the binding carries is stamped onto the "
        "record rather than recomputed or accepted here"
    ),
    "DeclaredOriginIsNotProvedBranchRelation": (
        "DeclaredOriginIsNotProvedBranchRelation: the origin a candidate "
        "claims to branch from is a caller's declaration. Nothing here checks "
        "that it exists or that the candidate differs from it"
    ),
    "NoGenusNameIsIntroducedHere": (
        "NoGenusNameIsIntroducedHere: candidate and model references are "
        "opaque caller strings, and the kernel names no genus of its own, so "
        "an experiment cannot smuggle a vocabulary past "
        "TraditionalNamingOnlyAfterFreezeAndE0"
    ),
}
"""The named limits this module freezes; each text opens with its own law name."""


def _require_text(value: object, field_name: str) -> None:
    if type(value) is not str or not value.strip():
        raise ExperimentalAuthorityError(f"{field_name} must be non-blank text")


def _require_text_tuple(value: object, field_name: str) -> None:
    if type(value) is not tuple or not value:
        raise ExperimentalAuthorityError(f"{field_name} must be a non-empty tuple")
    for entry in value:
        _require_text(entry, f"each {field_name} entry")
    if len(set(value)) != len(value):
        raise ExperimentalAuthorityError(f"{field_name} must not contain duplicates")


@dataclass(frozen=True, slots=True)
class DeclaredCaseSet:
    """The cases an experiment will be read against, frozen before any run.

    Freezing the case set before the run is what stops a result from reshaping
    the question it answered: a model cannot be judged over the cases it
    happened to handle.
    """

    case_set_id: str
    case_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_text(self.case_set_id, "declared case set id")
        _require_text_tuple(self.case_ids, "declared case ids")


@dataclass(frozen=True, slots=True)
class ExperimentalOperationRef:
    """One operation a run is permitted to use; an opaque, non-exhaustive ref.

    `InterventionOperationIsNotOntology` applies unchanged: a permitted set of
    operations is an explicit experimental tool, never a claim to be the
    complete set of primitives, and its members are not born objects.
    """

    identifier: str

    def __post_init__(self) -> None:
        _require_text(self.identifier, "experimental operation reference")


@dataclass(frozen=True, slots=True)
class ExperimentalCaseOutcomeVocabulary:
    """The two tokens through which a run's per-case output is read.

    Declared before the run, exactly as `DeclaredClosureOutcomeVocabulary` is
    declared before a closure execution, so that what counts as "the declared
    model did not account for this case" cannot be chosen after seeing the
    output.
    """

    accounted_token: str
    unaccounted_token: str

    def __post_init__(self) -> None:
        _require_text(self.accounted_token, "accounted token")
        _require_text(self.unaccounted_token, "unaccounted token")
        if self.accounted_token == self.unaccounted_token:
            raise ExperimentalAuthorityError(
                "the accounted and unaccounted tokens must differ"
            )


@dataclass(frozen=True, slots=True)
class ExperimentalCandidateDeclaration:
    """A candidate declared for experimentation; nothing about it is proved.

    Every field is a caller's declaration. The declaration is not a
    `BirthCandidate`, is accepted by no birth authority, and carries no
    identity, difference, or necessity claim.
    """

    candidate_id: str
    declared_origin_ref: str
    declared_scope: str
    declared_conditions: tuple[str, ...]
    declared_model_ref: str

    def __post_init__(self) -> None:
        _require_text(self.candidate_id, "experimental candidate id")
        _require_text(self.declared_origin_ref, "declared origin reference")
        _require_text(self.declared_scope, "declared experimental scope")
        _require_text_tuple(self.declared_conditions, "declared conditions")
        _require_text(self.declared_model_ref, "declared model reference")

    @property
    def proves_origin_branch_relation(self) -> bool:
        """`DeclaredOrigin != ProvedBranchRelation`; structurally false."""

        return False

    @property
    def proves_candidate_identity(self) -> bool:
        """`DeclaredCandidateId != ProvedIdentity`; structurally false."""

        return False


@dataclass(frozen=True, slots=True)
class ExperimentalRunRequest:
    """One candidate, one frozen case set, one input per case, one vocabulary.

    The inputs must cover the declared case set exactly: neither a case without
    an input nor an input for a case the set never declared is admitted, so the
    run cannot silently narrow or widen the question.
    """

    candidate: ExperimentalCandidateDeclaration
    case_set: DeclaredCaseSet
    inputs: tuple[tuple[str, str], ...]
    permitted_operations: tuple[ExperimentalOperationRef, ...]
    case_outcome_vocabulary: ExperimentalCaseOutcomeVocabulary

    def __post_init__(self) -> None:
        if type(self.candidate) is not ExperimentalCandidateDeclaration:
            raise ExperimentalAuthorityError(
                "an experimental run request requires a candidate declaration"
            )
        if type(self.case_set) is not DeclaredCaseSet:
            raise ExperimentalAuthorityError(
                "an experimental run request requires a declared case set"
            )
        if type(self.case_outcome_vocabulary) is not ExperimentalCaseOutcomeVocabulary:
            raise ExperimentalAuthorityError(
                "an experimental run request requires a case outcome vocabulary"
            )
        operations = self.permitted_operations
        if type(operations) is not tuple or not operations:
            raise ExperimentalAuthorityError(
                "an experimental run request requires at least one permitted operation"
            )
        for operation in self.permitted_operations:
            if type(operation) is not ExperimentalOperationRef:
                raise ExperimentalAuthorityError(
                    "each permitted operation must be an experimental operation "
                    "reference"
                )
        identifiers = tuple(
            operation.identifier for operation in self.permitted_operations
        )
        if len(set(identifiers)) != len(identifiers):
            raise ExperimentalAuthorityError(
                "permitted operations must not contain duplicates"
            )
        if type(self.inputs) is not tuple or not self.inputs:
            raise ExperimentalAuthorityError(
                "an experimental run request requires at least one case input"
            )
        for entry in self.inputs:
            if type(entry) is not tuple or len(entry) != 2:
                raise ExperimentalAuthorityError(
                    "each case input must be a (case id, input content) pair"
                )
            _require_text(entry[0], "case input case id")
            _require_text(entry[1], "case input content")
        declared_cases = tuple(case_id for case_id, _ in self.inputs)
        if declared_cases != self.case_set.case_ids:
            raise ExperimentalAuthorityError(
                "case inputs must cover the declared case set exactly, in order"
            )

    @property
    def declared_scope(self) -> str:
        """The candidate's own declared scope; never independently chosen."""

        return self.candidate.declared_scope

    @property
    def permitted_operation_ids(self) -> frozenset[str]:
        return frozenset(
            operation.identifier for operation in self.permitted_operations
        )


class BoundExperimentalRunRequest(ABC):
    """The abstract seam through which a bound request reaches this authority.

    A run is admissible only as a bound request, and binding a request to a
    frozen pre-evidence experiment is not this module's authority to exercise.
    So the concrete bound request is declared elsewhere and reaches `run` only
    through this seam, which exposes exactly two readings: the request that was
    bound, and the canonical content digest the binding derived for it. Nothing
    here can read, or even name, the experiment a request was bound to.
    """

    __slots__ = ()

    @property
    @abstractmethod
    def request(self) -> ExperimentalRunRequest:
        """The frozen request this binding closed over."""

    @property
    @abstractmethod
    def request_content_digest(self) -> str:
        """The canonical content digest the binding derived for that request."""


class ExperimentalOutcomeStatus(Enum):
    """How the run itself ended. Never whether its result was valid.

    `COMPLETED` says the implementation returned a readable output for every
    declared case, `FAILED` that it raised or returned something unreadable,
    and `ABORTED` that it reached for an operation the request never permitted.
    None of the three is a judgement about the candidate.
    """

    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    ABORTED = "ABORTED"


class ExperimentalFailureKind(Enum):
    """Named grounds on which a run did not complete; never a bare `False`."""

    IMPLEMENTATION_RAISED = "IMPLEMENTATION_RAISED"
    UNREADABLE_IMPLEMENTATION_RESULT = "UNREADABLE_IMPLEMENTATION_RESULT"
    UNREADABLE_CASE_OUTCOME = "UNREADABLE_CASE_OUTCOME"
    OPERATION_NOT_PERMITTED = "OPERATION_NOT_PERMITTED"
    OPERATION_EVENT_NOT_AUTHORITY_ISSUED = "OPERATION_EVENT_NOT_AUTHORITY_ISSUED"


@dataclass(frozen=True, slots=True)
class ExperimentalFailureRecord:
    """What went wrong, on which case, and with which trace up to that point.

    A failure is kept, not swallowed: it is one of the observed facts the run
    produced, and `ExperimentalFailureIsNotNoBirth` is what stops it from
    becoming a verdict.
    """

    failure_kind: ExperimentalFailureKind
    case_id: str
    message: str
    trace: Trace

    def __post_init__(self) -> None:
        if not isinstance(self.failure_kind, ExperimentalFailureKind):
            raise ExperimentalAuthorityError(
                "a failure record requires a member of ExperimentalFailureKind"
            )
        _require_text(self.case_id, "failure case id")
        _require_text(self.message, "failure message")
        if type(self.trace) is not Trace:
            raise ExperimentalAuthorityError("a failure record requires a trace")


@dataclass(frozen=True, slots=True)
class ExperimentalRunRecord:
    """Authority-issued record of one experimental run; observed facts only.

    Constructible only by `ExperimentalAuthority.run`. Exactly one of
    `output_content` and `failure` is present: a completed run has an output
    and no failure, and a failed or aborted run has a failure and no output.
    """

    run_id: str
    issuing_authority_id: str
    request: ExperimentalRunRequest
    request_content_digest: str
    outcome_status: ExperimentalOutcomeStatus
    output_content: str | None
    failure: ExperimentalFailureRecord | None
    observed_unexplained_cases: tuple[str, ...]
    operations_used: tuple[str, ...]
    trace: Trace
    _token: object | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._token is not _EXPERIMENTAL_TOKEN:
            raise ExperimentalAuthorityError(
                "experimental run records must be issued by ExperimentalAuthority"
            )
        _require_text(self.run_id, "experimental run id")
        _require_text(self.issuing_authority_id, "experimental authority id")
        if type(self.request) is not ExperimentalRunRequest:
            raise ExperimentalAuthorityError(
                "an experimental run record requires its own run request"
            )
        if not is_canonical_digest(self.request_content_digest):
            raise ExperimentalAuthorityError(
                "an experimental run record requires the canonical content "
                "digest of the bound request it ran"
            )
        if not isinstance(self.outcome_status, ExperimentalOutcomeStatus):
            raise ExperimentalAuthorityError(
                "an experimental run record requires an outcome status"
            )
        if type(self.trace) is not Trace:
            raise ExperimentalAuthorityError(
                "an experimental run record requires a trace"
            )
        completed = self.outcome_status is ExperimentalOutcomeStatus.COMPLETED
        if completed:
            _require_text(self.output_content, "completed run output content")
            if self.failure is not None:
                raise ExperimentalAuthorityError("a completed run records no failure")
        else:
            if self.output_content is not None:
                raise ExperimentalAuthorityError(
                    "a run that did not complete records no output content"
                )
            if type(self.failure) is not ExperimentalFailureRecord:
                raise ExperimentalAuthorityError(
                    "a run that did not complete requires a failure record"
                )
        for observed in (self.observed_unexplained_cases, self.operations_used):
            if type(observed) is not tuple or any(
                type(entry) is not str for entry in observed
            ):
                raise ExperimentalAuthorityError(
                    "observed case and operation readings must be text tuples"
                )
        unknown = set(self.observed_unexplained_cases) - set(
            self.request.case_set.case_ids
        )
        if unknown:
            raise ExperimentalAuthorityError(
                "observed unexplained cases must belong to the declared case set"
            )

    @property
    def candidate(self) -> ExperimentalCandidateDeclaration:
        return self.request.candidate

    @property
    def case_set(self) -> DeclaredCaseSet:
        return self.request.case_set

    @property
    def declared_model_ref(self) -> str:
        return self.request.candidate.declared_model_ref

    @property
    def records_failure(self) -> bool:
        """Whether a failure was observed; a kept fact, not a verdict."""

        return self.failure is not None

    @property
    def confers_birth(self) -> bool:
        """`ExperimentalSuccess != Birth`; structurally false."""

        return False

    @property
    def confers_validity(self) -> bool:
        """A run observes an output; it never pronounces it valid."""

        return False

    @property
    def confers_constitutional_evidence(self) -> bool:
        """`ExperimentalResult != ConstitutionalEvidence`; structurally false."""

        return False

    @property
    def confers_identity_proof(self) -> bool:
        """Running a candidate does not prove its identity is independent."""

        return False

    @property
    def confers_difference_from_origin(self) -> bool:
        """Running a candidate does not prove it differs from its origin."""

        return False

    @property
    def confers_necessity(self) -> bool:
        """A result does not oblige the birth of what produced it."""

        return False


class _UnpermittedOperation(BaseException):
    """Raised through an implementation when it reaches for a refused operation.

    Deliberately a `BaseException`: an implementation that wraps its work in
    `except Exception` must not be able to swallow the authority's refusal and
    carry on as though the operation had been available. Even if it does catch
    this, the capability has already recorded the refusal, and the run is
    aborted on return.
    """

    def __init__(self, operation_id: str) -> None:
        super().__init__(operation_id)
        self.operation_id = operation_id


class ExperimentalRunContext:
    """The authority-issued capability through which one case reaches operations.

    `UnpermittedOperationCannotExecute`: an operation the request never
    permitted is refused *before* the action is invoked, so an implementation
    cannot perform it and then decline to mention it. A permitted operation is
    recorded by the authority itself, in the authority's own trace, at the
    moment it is invoked.

    A capability is issued per case and revoked when that case ends, so it
    cannot be stored and used to reach an operation outside the run that
    granted it. This is a mediation boundary and not a sandbox: an
    implementation that reaches an ambient effect without asking never passes
    through here, which `ExperimentalIsolationIsProcessLocal` already declares.
    """

    def __init__(
        self,
        *,
        run_id: str,
        case_id: str,
        permitted_operation_ids: frozenset[str],
        events: list[str],
        operations_used: list[str],
        token: object,
    ) -> None:
        if token is not _CAPABILITY_TOKEN:
            raise ExperimentalAuthorityError(
                "experimental run capabilities must be issued by "
                "ExperimentalAuthority"
            )
        self._run_id = run_id
        self._case_id = case_id
        self._permitted_operation_ids = permitted_operation_ids
        self._events = events
        self._operations_used = operations_used
        self._revoked = False
        self._refused_operation: str | None = None

    @property
    def run_id(self) -> str:
        return self._run_id

    @property
    def case_id(self) -> str:
        return self._case_id

    @property
    def permitted_operation_ids(self) -> frozenset[str]:
        return self._permitted_operation_ids

    def invoke(self, operation_id: str, action: Callable[[], _T]) -> _T:
        """Perform one declared operation, or refuse it before it happens."""

        _require_text(operation_id, "experimental operation id")
        if self._revoked:
            raise ExperimentalAuthorityError(
                "an experimental run capability cannot be used outside the case "
                "it was issued for"
            )
        if operation_id not in self._permitted_operation_ids:
            self._refused_operation = operation_id
            self._revoked = True
            raise _UnpermittedOperation(operation_id)
        self._events.append(f"{_OPERATION_EVENT_PREFIX}{operation_id}")
        if operation_id not in self._operations_used:
            self._operations_used.append(operation_id)
        return action()

    def _revoke(self) -> None:
        self._revoked = True


# An implementation receives the capability issued for one case together with
# that case's input content, and returns its output content with a trace of
# what it did. It carries no role-specific meaning: this module does not know
# what any output means, only how the request's own frozen vocabulary reads it.
ExperimentalImplementation = Callable[[ExperimentalRunContext, str], tuple[str, Trace]]


class ExperimentalAuthority:
    """The sole issuer of an `ExperimentalRunRecord`; it certifies nothing.

    `ExperimentalAuthorityCannotCertifyOrExecute`: this class exposes `run` and
    its own id, and no method that certifies a birth or admits an entity for
    use.

    Run ids are unique within this authority's own registry, guarded by a lock
    so concurrent calls on the same instance cannot race past the check. As in
    G0.2a.3.1, `LocalInjectivity != PortableIdentity`: two authorities are two
    uncoordinated issuance scopes and may each issue the same run id.
    """

    def __init__(self, *, authority_id: str) -> None:
        _require_text(authority_id, "experimental authority id")
        self._authority_id = authority_id
        self._issued_run_ids: set[str] = set()
        self._lock = threading.Lock()

    @property
    def authority_id(self) -> str:
        return self._authority_id

    def run(
        self,
        *,
        run_id: str,
        bound_request: BoundExperimentalRunRequest,
        implementation: ExperimentalImplementation,
    ) -> ExperimentalRunRecord:
        """Run one bound request over its case set, recording only facts."""

        _require_text(run_id, "experimental run id")
        if not isinstance(bound_request, BoundExperimentalRunRequest):
            raise ExperimentalAuthorityError(
                "an experimental run requires a bound experimental run request"
            )
        request = bound_request.request
        request_content_digest = bound_request.request_content_digest
        if type(request) is not ExperimentalRunRequest:
            raise ExperimentalAuthorityError(
                "a bound experimental run request must carry its own run request"
            )
        if not is_canonical_digest(request_content_digest):
            raise ExperimentalAuthorityError(
                "a bound experimental run request must carry the canonical "
                "content digest of the request it bound"
            )
        if not callable(implementation):
            raise ExperimentalAuthorityError(
                "an experimental run requires a callable implementation"
            )
        with self._lock:
            if run_id in self._issued_run_ids:
                raise ExperimentalAuthorityError(
                    "experimental run id already issued by this authority"
                )
            self._issued_run_ids.add(run_id)

        events: list[str] = [
            f"run:{run_id}",
            f"authority:{self._authority_id}",
            f"candidate:{request.candidate.candidate_id}",
            f"declared_origin:{request.candidate.declared_origin_ref}",
            f"declared_model:{request.candidate.declared_model_ref}",
            f"scope:{request.declared_scope}",
            f"case_set:{request.case_set.case_set_id}",
            f"request_content:{request_content_digest}",
        ]
        events.extend(
            f"condition:{condition}"
            for condition in request.candidate.declared_conditions
        )

        vocabulary = request.case_outcome_vocabulary
        unexplained: list[str] = []
        operations_used: list[str] = []
        readings: list[str] = []

        for case_id, input_content in request.inputs:
            events.append(f"case:{case_id}")
            capability = ExperimentalRunContext(
                run_id=run_id,
                case_id=case_id,
                permitted_operation_ids=request.permitted_operation_ids,
                events=events,
                operations_used=operations_used,
                token=_CAPABILITY_TOKEN,
            )
            refused: str | None = None
            raised: BaseException | None = None
            try:
                result = implementation(capability, input_content)
            except _UnpermittedOperation as refusal:
                refused = refusal.operation_id
                result = None
            except Exception as error:  # captured, never propagated
                raised = error
                result = None
            finally:
                capability._revoke()
            if refused is None:
                refused = capability._refused_operation
            if refused is not None:
                events.append(f"operation_not_permitted:{case_id}:{refused}")
                return self._failed_record(
                    run_id=run_id,
                    request=request,
                    request_content_digest=request_content_digest,
                    status=ExperimentalOutcomeStatus.ABORTED,
                    failure=ExperimentalFailureRecord(
                        failure_kind=ExperimentalFailureKind.OPERATION_NOT_PERMITTED,
                        case_id=case_id,
                        message=(
                            f"operation {refused!r} was not permitted by this "
                            "run request and was refused before it could run"
                        ),
                        trace=Trace(tuple(events)),
                    ),
                    operations_used=operations_used,
                    events=events,
                )
            if raised is not None:
                events.append(f"case_failed:{case_id}:{type(raised).__name__}")
                return self._failed_record(
                    run_id=run_id,
                    request=request,
                    request_content_digest=request_content_digest,
                    status=ExperimentalOutcomeStatus.FAILED,
                    failure=ExperimentalFailureRecord(
                        failure_kind=ExperimentalFailureKind.IMPLEMENTATION_RAISED,
                        case_id=case_id,
                        message=f"{type(raised).__name__}: {raised}",
                        trace=Trace(tuple(events)),
                    ),
                    operations_used=operations_used,
                    events=events,
                )
            if (
                type(result) is not tuple
                or len(result) != 2
                or type(result[0]) is not str
                or type(result[1]) is not Trace
            ):
                events.append(f"case_unreadable_result:{case_id}")
                return self._failed_record(
                    run_id=run_id,
                    request=request,
                    request_content_digest=request_content_digest,
                    status=ExperimentalOutcomeStatus.FAILED,
                    failure=ExperimentalFailureRecord(
                        failure_kind=(
                            ExperimentalFailureKind.UNREADABLE_IMPLEMENTATION_RESULT
                        ),
                        case_id=case_id,
                        message=(
                            "an implementation must return exactly an output "
                            "string and a trace"
                        ),
                        trace=Trace(tuple(events)),
                    ),
                    operations_used=operations_used,
                    events=events,
                )
            output, case_trace = result
            forged = tuple(
                event
                for event in case_trace.events
                if event.startswith(_OPERATION_EVENT_PREFIX)
            )
            if forged:
                events.append(f"forged_operation_event:{case_id}:{forged[0]}")
                return self._failed_record(
                    run_id=run_id,
                    request=request,
                    request_content_digest=request_content_digest,
                    status=ExperimentalOutcomeStatus.FAILED,
                    failure=ExperimentalFailureRecord(
                        failure_kind=(
                            ExperimentalFailureKind.OPERATION_EVENT_NOT_AUTHORITY_ISSUED
                        ),
                        case_id=case_id,
                        message=(
                            "operation events are written by this authority "
                            "when a capability is used, and an implementation "
                            f"that writes {forged[0]!r} into its own trace is "
                            "forging the authority's record"
                        ),
                        trace=Trace(tuple(events)),
                    ),
                    operations_used=operations_used,
                    events=events,
                )
            events.extend(
                f"implementation:{case_id}:{event}" for event in case_trace.events
            )

            if output == vocabulary.accounted_token:
                events.append(f"case_accounted:{case_id}")
            elif output == vocabulary.unaccounted_token:
                events.append(f"case_unaccounted:{case_id}")
                unexplained.append(case_id)
            else:
                events.append(f"case_unreadable_outcome:{case_id}")
                return self._failed_record(
                    run_id=run_id,
                    request=request,
                    request_content_digest=request_content_digest,
                    status=ExperimentalOutcomeStatus.FAILED,
                    failure=ExperimentalFailureRecord(
                        failure_kind=ExperimentalFailureKind.UNREADABLE_CASE_OUTCOME,
                        case_id=case_id,
                        message=(
                            "the output is neither the accounted nor the "
                            "unaccounted token of this request's frozen vocabulary"
                        ),
                        trace=Trace(tuple(events)),
                    ),
                    operations_used=operations_used,
                    events=events,
                )
            readings.append(f"{case_id}={output}")

        events.append("outcome:COMPLETED")
        return ExperimentalRunRecord(
            run_id=run_id,
            issuing_authority_id=self._authority_id,
            request=request,
            request_content_digest=request_content_digest,
            outcome_status=ExperimentalOutcomeStatus.COMPLETED,
            output_content="\n".join(readings),
            failure=None,
            observed_unexplained_cases=tuple(unexplained),
            operations_used=tuple(operations_used),
            trace=Trace(tuple(events)),
            _token=_EXPERIMENTAL_TOKEN,
        )

    def _failed_record(
        self,
        *,
        run_id: str,
        request: ExperimentalRunRequest,
        request_content_digest: str,
        status: ExperimentalOutcomeStatus,
        failure: ExperimentalFailureRecord,
        operations_used: list[str],
        events: list[str],
    ) -> ExperimentalRunRecord:
        events.append(f"outcome:{status.name}")
        return ExperimentalRunRecord(
            run_id=run_id,
            issuing_authority_id=self._authority_id,
            request=request,
            request_content_digest=request_content_digest,
            outcome_status=status,
            output_content=None,
            failure=failure,
            observed_unexplained_cases=(),
            operations_used=tuple(operations_used),
            trace=Trace(tuple(events)),
            _token=_EXPERIMENTAL_TOKEN,
        )


_EXPERIMENTAL_AUTHORITY_SURFACE = frozenset({"authority_id", "run"})
_EXPERIMENTAL_CAPABILITY_SURFACE = frozenset(
    {"case_id", "invoke", "permitted_operation_ids", "run_id"}
)


def _public_surface(owner: type) -> frozenset[str]:
    return frozenset(name for name in vars(owner) if not name.startswith("_"))


def sweep_forbidden_fields(*owners: type) -> None:
    """Raise if any dataclass declares a field naming a status it cannot confer."""

    for owner in owners:
        for declared in fields(owner):
            if declared.name.lstrip("_") in _FORBIDDEN_FIELD_NAMES:
                raise RuntimeError(
                    f"{owner.__name__} declares the forbidden field "
                    f"{declared.name!r}: an experimental artifact records "
                    "observed facts only"
                )


sweep_forbidden_fields(
    DeclaredCaseSet,
    ExperimentalCandidateDeclaration,
    ExperimentalCaseOutcomeVocabulary,
    ExperimentalFailureRecord,
    ExperimentalOperationRef,
    ExperimentalRunRecord,
    ExperimentalRunRequest,
)

if _public_surface(ExperimentalAuthority) != _EXPERIMENTAL_AUTHORITY_SURFACE:
    raise RuntimeError(
        "ExperimentalAuthority must expose no method beyond running an experiment"
    )
if _public_surface(ExperimentalRunContext) != _EXPERIMENTAL_CAPABILITY_SURFACE:
    raise RuntimeError(
        "ExperimentalRunContext must expose no surface beyond invoking one "
        "permitted operation and naming the run and case it belongs to"
    )
for _law_name, _law_text in EXPERIMENTAL_NAMED_LAWS.items():
    if not _law_text.startswith(f"{_law_name}:"):
        raise RuntimeError("each named law text must open with its own law name")


__all__ = [
    "EXPERIMENTAL_NAMED_LAWS",
    "BoundExperimentalRunRequest",
    "DeclaredCaseSet",
    "ExperimentalAuthority",
    "ExperimentalAuthorityError",
    "ExperimentalCandidateDeclaration",
    "ExperimentalCaseOutcomeVocabulary",
    "ExperimentalFailureKind",
    "ExperimentalFailureRecord",
    "ExperimentalImplementation",
    "ExperimentalOperationRef",
    "ExperimentalOutcomeStatus",
    "ExperimentalRunContext",
    "ExperimentalRunRecord",
    "ExperimentalRunRequest",
    "sweep_forbidden_fields",
]
