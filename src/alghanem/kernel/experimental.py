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

Four claims this module explicitly does **not** make:

* ``Isolation = ProcessLocalOnly``. `ExperimentalAuthority.run` invokes a
  caller-supplied implementation in this very process and captures the
  exceptions it raises instead of letting them propagate. That is authority
  isolation -- a failure cannot escape into the caller's control flow as if it
  were the caller's own -- and not a security sandbox: nothing here restricts
  filesystem, network, memory, or time. `CapturedFailure != SandboxedExecution`.
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
from collections.abc import Callable
from dataclasses import dataclass, field, fields
from enum import Enum

from .trace import Trace

_EXPERIMENTAL_TOKEN = object()

_OPERATION_EVENT_PREFIX = "operation:"

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


class ExperimentalOutcomeStatus(Enum):
    """How the run itself ended. Never whether its result was valid.

    `COMPLETED` says the implementation returned a readable output for every
    declared case, `FAILED` that it raised or returned something unreadable,
    and `ABORTED` that it declared an operation the request never permitted.
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


# An implementation receives one case's input content and returns its output
# content together with a trace of what it did. It carries no role-specific
# meaning: this module does not know what any output means, only how the
# request's own frozen vocabulary reads it.
ExperimentalImplementation = Callable[[str], tuple[str, Trace]]


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
        request: ExperimentalRunRequest,
        implementation: ExperimentalImplementation,
    ) -> ExperimentalRunRecord:
        """Run one declared candidate over its case set, recording only facts."""

        _require_text(run_id, "experimental run id")
        if type(request) is not ExperimentalRunRequest:
            raise ExperimentalAuthorityError(
                "an experimental run requires an experimental run request"
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
            try:
                result = implementation(input_content)
            except Exception as error:  # captured, never propagated
                events.append(f"case_failed:{case_id}:{type(error).__name__}")
                return self._failed_record(
                    run_id=run_id,
                    request=request,
                    status=ExperimentalOutcomeStatus.FAILED,
                    failure=ExperimentalFailureRecord(
                        failure_kind=ExperimentalFailureKind.IMPLEMENTATION_RAISED,
                        case_id=case_id,
                        message=f"{type(error).__name__}: {error}",
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
            events.extend(
                f"implementation:{case_id}:{event}" for event in case_trace.events
            )

            for event in case_trace.events:
                if not event.startswith(_OPERATION_EVENT_PREFIX):
                    continue
                operation_id = event[len(_OPERATION_EVENT_PREFIX) :]
                if operation_id not in request.permitted_operation_ids:
                    events.append(f"operation_not_permitted:{case_id}:{operation_id}")
                    return self._failed_record(
                        run_id=run_id,
                        request=request,
                        status=ExperimentalOutcomeStatus.ABORTED,
                        failure=ExperimentalFailureRecord(
                            failure_kind=(
                                ExperimentalFailureKind.OPERATION_NOT_PERMITTED
                            ),
                            case_id=case_id,
                            message=(
                                f"operation {operation_id!r} was not permitted by "
                                "this run request"
                            ),
                            trace=Trace(tuple(events)),
                        ),
                        operations_used=operations_used,
                        events=events,
                    )
                if operation_id not in operations_used:
                    operations_used.append(operation_id)

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
            outcome_status=status,
            output_content=None,
            failure=failure,
            observed_unexplained_cases=(),
            operations_used=tuple(operations_used),
            trace=Trace(tuple(events)),
            _token=_EXPERIMENTAL_TOKEN,
        )


_EXPERIMENTAL_AUTHORITY_SURFACE = frozenset({"authority_id", "run"})


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
for _law_name, _law_text in EXPERIMENTAL_NAMED_LAWS.items():
    if not _law_text.startswith(f"{_law_name}:"):
        raise RuntimeError("each named law text must open with its own law name")


__all__ = [
    "EXPERIMENTAL_NAMED_LAWS",
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
    "ExperimentalRunRecord",
    "ExperimentalRunRequest",
    "sweep_forbidden_fields",
]
