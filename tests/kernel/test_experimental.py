"""G0.EX.1a: what a run of a not-yet-born candidate proves, and what it cannot.

Every assertion here is about one boundary: an `ExperimentalRunRecord` records
observed facts under an authority that certifies nothing, and no branch of it --
completed, failed, or aborted -- confers birth, validity, identity, difference
from origin, necessity, or constitutional evidence.
"""

from dataclasses import fields

import pytest
from test_independent_closure_composition import (  # type: ignore[import-not-found]
    frozen_specification_binding,
    specification,
)

from alghanem.kernel.birth import BirthExperimentSpecificationError
from alghanem.kernel.experimental import (
    EXPERIMENTAL_NAMED_LAWS,
    DeclaredCaseSet,
    ExperimentalAuthority,
    ExperimentalAuthorityError,
    ExperimentalCandidateDeclaration,
    ExperimentalCaseOutcomeVocabulary,
    ExperimentalFailureKind,
    ExperimentalFailureRecord,
    ExperimentalOperationRef,
    ExperimentalOutcomeStatus,
    ExperimentalRunContext,
    ExperimentalRunRecord,
    ExperimentalRunRequest,
    sweep_forbidden_fields,
)
from alghanem.kernel.experimental_request_content_identity import (
    request_content_digest,
)
from alghanem.kernel.experimental_run_binding import (
    BoundExperimentalRunRequest,
    ExperimentalRunBindingAuthority,
)
from alghanem.kernel.trace import Trace

ACCOUNTED = "ACCOUNTED:the declared model accounts for this case"
UNACCOUNTED = "UNACCOUNTED:the declared model does not account for this case"


def vocabulary() -> ExperimentalCaseOutcomeVocabulary:
    return ExperimentalCaseOutcomeVocabulary(
        accounted_token=ACCOUNTED, unaccounted_token=UNACCOUNTED
    )


def case_set(case_ids: tuple[str, ...] = ("c1", "c2", "c3")) -> DeclaredCaseSet:
    return DeclaredCaseSet(case_set_id="case-set", case_ids=case_ids)


def candidate(
    *, candidate_id: str = "candidate", model_ref: str = "model-a"
) -> ExperimentalCandidateDeclaration:
    return ExperimentalCandidateDeclaration(
        candidate_id=candidate_id,
        declared_origin_ref="origin",
        declared_scope="finite-domain",
        declared_conditions=("isolated run", "no measured input"),
        declared_model_ref=model_ref,
    )


def request(
    *,
    cases: DeclaredCaseSet | None = None,
    model_ref: str = "model-a",
    permitted: tuple[str, ...] = ("apply", "compare"),
) -> ExperimentalRunRequest:
    declared_cases = cases if cases is not None else case_set()
    return ExperimentalRunRequest(
        candidate=candidate(model_ref=model_ref),
        case_set=declared_cases,
        inputs=tuple(
            (case_id, f"input:{case_id}") for case_id in declared_cases.case_ids
        ),
        permitted_operations=tuple(
            ExperimentalOperationRef(identifier) for identifier in permitted
        ),
        case_outcome_vocabulary=vocabulary(),
    )


def experiment_binding(experiment_id: str = "experiment") -> object:
    return frozen_specification_binding(specification(experiment_id=experiment_id))


def bound(
    run_request: ExperimentalRunRequest | None = None,
    *,
    binding: object | None = None,
    binding_id: str = "binding-1",
    authority: ExperimentalRunBindingAuthority | None = None,
) -> BoundExperimentalRunRequest:
    """Bind one request to a frozen experiment, as every run now requires."""

    binding_authority = authority or ExperimentalRunBindingAuthority(
        authority_id="binding"
    )
    return binding_authority.bind(
        binding_id=binding_id,
        request=run_request if run_request is not None else request(),
        binding=binding if binding is not None else experiment_binding(),  # type: ignore[arg-type]
    )


def implementation_for(
    unaccounted: frozenset[str], *, operation: str = "apply"
) -> object:
    def implementation(
        context: ExperimentalRunContext, input_content: str
    ) -> tuple[str, Trace]:
        case_id = input_content.removeprefix("input:")
        token = UNACCOUNTED if case_id in unaccounted else ACCOUNTED
        context.invoke(operation, lambda: None)
        return token, Trace((f"read:{case_id}",))

    return implementation


def test_a_completed_run_records_only_the_cases_its_model_left_unaccounted() -> None:
    authority = ExperimentalAuthority(authority_id="lab")

    record = authority.run(
        run_id="run-1",
        bound_request=bound(),
        implementation=implementation_for(frozenset({"c2"})),
    )

    assert record.outcome_status is ExperimentalOutcomeStatus.COMPLETED
    assert record.observed_unexplained_cases == ("c2",)
    assert record.operations_used == ("apply",)
    assert record.failure is None
    assert record.records_failure is False
    assert "outcome:COMPLETED" in record.trace.events


def test_no_branch_of_a_record_confers_birth_validity_or_evidence() -> None:
    authority = ExperimentalAuthority(authority_id="lab")

    def raising(
        context: ExperimentalRunContext, input_content: str
    ) -> tuple[str, Trace]:
        raise RuntimeError("the implementation gave up")

    completed = authority.run(
        run_id="completed",
        bound_request=bound(),
        implementation=implementation_for(frozenset()),
    )
    failed = authority.run(
        run_id="failed", bound_request=bound(), implementation=raising
    )

    for record in (completed, failed):
        assert record.confers_birth is False
        assert record.confers_validity is False
        assert record.confers_constitutional_evidence is False
        assert record.confers_identity_proof is False
        assert record.confers_difference_from_origin is False
        assert record.confers_necessity is False
    assert completed.candidate.proves_candidate_identity is False
    assert completed.candidate.proves_origin_branch_relation is False


def test_a_run_record_cannot_be_constructed_outside_its_authority() -> None:
    authority = ExperimentalAuthority(authority_id="lab")
    issued = authority.run(
        run_id="run-1",
        bound_request=bound(),
        implementation=implementation_for(frozenset()),
    )

    with pytest.raises(ExperimentalAuthorityError):
        ExperimentalRunRecord(
            run_id="fabricated",
            issuing_authority_id="lab",
            request=issued.request,
            request_content_digest=issued.request_content_digest,
            outcome_status=ExperimentalOutcomeStatus.COMPLETED,
            output_content="anything at all",
            failure=None,
            observed_unexplained_cases=(),
            operations_used=(),
            trace=Trace(("fabricated",)),
        )


def test_an_implementation_that_raises_becomes_a_failure_rather_than_an_exception() -> (
    None
):
    authority = ExperimentalAuthority(authority_id="lab")

    def raising(
        context: ExperimentalRunContext, input_content: str
    ) -> tuple[str, Trace]:
        raise ValueError("no")

    record = authority.run(
        run_id="run-1", bound_request=bound(), implementation=raising
    )

    assert record.outcome_status is ExperimentalOutcomeStatus.FAILED
    assert record.failure is not None
    assert record.failure.failure_kind is ExperimentalFailureKind.IMPLEMENTATION_RAISED
    assert record.failure.case_id == "c1"
    assert record.output_content is None
    assert record.records_failure is True


def test_an_unreadable_implementation_result_is_refused_as_a_failure() -> None:
    authority = ExperimentalAuthority(authority_id="lab")

    def wrong_shape(
        context: ExperimentalRunContext, input_content: str
    ) -> tuple[str, Trace]:
        return "just a string"  # type: ignore[return-value]

    record = authority.run(
        run_id="run-1", bound_request=bound(), implementation=wrong_shape
    )

    assert record.outcome_status is ExperimentalOutcomeStatus.FAILED
    assert record.failure is not None
    assert (
        record.failure.failure_kind
        is ExperimentalFailureKind.UNREADABLE_IMPLEMENTATION_RESULT
    )


def test_an_output_outside_the_frozen_vocabulary_is_unreadable_not_reinterpreted() -> (
    None
):
    authority = ExperimentalAuthority(authority_id="lab")

    def off_vocabulary(
        context: ExperimentalRunContext, input_content: str
    ) -> tuple[str, Trace]:
        return "PROBABLY_FINE", Trace(("read:anything",))

    record = authority.run(
        run_id="run-1", bound_request=bound(), implementation=off_vocabulary
    )

    assert record.outcome_status is ExperimentalOutcomeStatus.FAILED
    assert record.failure is not None
    assert (
        record.failure.failure_kind is ExperimentalFailureKind.UNREADABLE_CASE_OUTCOME
    )


def test_a_run_record_carries_the_bound_requests_canonical_content_digest() -> None:
    authority = ExperimentalAuthority(authority_id="lab")
    bound_request = bound()

    record = authority.run(
        run_id="run-1",
        bound_request=bound_request,
        implementation=implementation_for(frozenset()),
    )

    assert record.request_content_digest == request_content_digest(record.request)
    assert record.request_content_digest == bound_request.request_content_digest
    assert f"request_content:{record.request_content_digest}" in record.trace.events


def test_an_unbound_request_is_not_an_admissible_argument_to_a_run() -> None:
    authority = ExperimentalAuthority(authority_id="lab")

    with pytest.raises(ExperimentalAuthorityError):
        authority.run(
            run_id="run-1",
            bound_request=request(),  # type: ignore[arg-type]
            implementation=implementation_for(frozenset()),
        )


def test_an_operation_the_request_never_permitted_aborts_the_run() -> None:
    authority = ExperimentalAuthority(authority_id="lab")

    record = authority.run(
        run_id="run-1",
        bound_request=bound(request(permitted=("apply",))),
        implementation=implementation_for(frozenset(), operation="rewrite"),
    )

    assert record.outcome_status is ExperimentalOutcomeStatus.ABORTED
    assert record.failure is not None
    assert (
        record.failure.failure_kind is ExperimentalFailureKind.OPERATION_NOT_PERMITTED
    )
    assert record.output_content is None


def test_an_unpermitted_operation_never_runs_even_if_it_is_never_reported() -> None:
    authority = ExperimentalAuthority(authority_id="lab")
    performed: list[str] = []

    def reaches_for_a_refused_operation(
        context: ExperimentalRunContext, input_content: str
    ) -> tuple[str, Trace]:
        try:
            context.invoke("rewrite", lambda: performed.append("rewrite"))
        except Exception:  # a refusal an implementation must not be able to swallow
            performed.append("swallowed")
        return ACCOUNTED, Trace(("read:quietly",))

    record = authority.run(
        run_id="run-1",
        bound_request=bound(request(permitted=("apply",))),
        implementation=reaches_for_a_refused_operation,
    )

    assert performed == []
    assert record.outcome_status is ExperimentalOutcomeStatus.ABORTED
    assert record.failure is not None
    assert (
        record.failure.failure_kind is ExperimentalFailureKind.OPERATION_NOT_PERMITTED
    )
    assert record.operations_used == ()


def test_the_authority_writes_the_operation_events_of_its_own_trace() -> None:
    authority = ExperimentalAuthority(authority_id="lab")

    record = authority.run(
        run_id="run-1",
        bound_request=bound(),
        implementation=implementation_for(frozenset()),
    )

    assert "operation:apply" in record.trace.events
    assert record.operations_used == ("apply",)


def test_an_implementation_that_forges_an_operation_event_fails_the_run() -> None:
    authority = ExperimentalAuthority(authority_id="lab")

    def forging(
        context: ExperimentalRunContext, input_content: str
    ) -> tuple[str, Trace]:
        return ACCOUNTED, Trace(("operation:rewrite",))

    record = authority.run(
        run_id="run-1", bound_request=bound(), implementation=forging
    )

    assert record.outcome_status is ExperimentalOutcomeStatus.FAILED
    assert record.failure is not None
    assert (
        record.failure.failure_kind
        is ExperimentalFailureKind.OPERATION_EVENT_NOT_AUTHORITY_ISSUED
    )
    assert record.operations_used == ()


def test_a_capability_cannot_be_kept_and_used_after_its_case_ended() -> None:
    authority = ExperimentalAuthority(authority_id="lab")
    kept: list[ExperimentalRunContext] = []

    def keeping(
        context: ExperimentalRunContext, input_content: str
    ) -> tuple[str, Trace]:
        kept.append(context)
        return ACCOUNTED, Trace(("read:kept",))

    authority.run(run_id="run-1", bound_request=bound(), implementation=keeping)

    assert kept
    for context in kept:
        with pytest.raises(ExperimentalAuthorityError):
            context.invoke("apply", lambda: None)


def test_a_capability_cannot_be_constructed_outside_its_authority() -> None:
    with pytest.raises(ExperimentalAuthorityError):
        ExperimentalRunContext(
            run_id="fabricated",
            case_id="c1",
            permitted_operation_ids=frozenset({"anything"}),
            events=[],
            operations_used=[],
            token=object(),
        )


def test_the_capability_exposes_no_surface_beyond_one_permitted_operation() -> None:
    surface = {
        name for name in vars(ExperimentalRunContext) if not name.startswith("_")
    }

    assert surface == {"case_id", "invoke", "permitted_operation_ids", "run_id"}


def test_run_ids_are_injective_within_one_authority_only() -> None:
    first = ExperimentalAuthority(authority_id="lab-1")
    second = ExperimentalAuthority(authority_id="lab-2")
    implementation = implementation_for(frozenset())

    first.run(run_id="run", bound_request=bound(), implementation=implementation)
    with pytest.raises(ExperimentalAuthorityError):
        first.run(run_id="run", bound_request=bound(), implementation=implementation)

    # LocalInjectivity != PortableIdentity: a second issuer is uncoordinated.
    second.run(run_id="run", bound_request=bound(), implementation=implementation)


def test_inputs_must_cover_the_frozen_case_set_exactly_and_in_order() -> None:
    cases = case_set()

    with pytest.raises(ExperimentalAuthorityError):
        ExperimentalRunRequest(
            candidate=candidate(),
            case_set=cases,
            inputs=(("c1", "input:c1"), ("c2", "input:c2")),
            permitted_operations=(ExperimentalOperationRef("apply"),),
            case_outcome_vocabulary=vocabulary(),
        )
    with pytest.raises(ExperimentalAuthorityError):
        ExperimentalRunRequest(
            candidate=candidate(),
            case_set=cases,
            inputs=(
                ("c3", "input:c3"),
                ("c2", "input:c2"),
                ("c1", "input:c1"),
            ),
            permitted_operations=(ExperimentalOperationRef("apply"),),
            case_outcome_vocabulary=vocabulary(),
        )


def test_a_vocabulary_with_one_token_for_both_readings_is_refused() -> None:
    with pytest.raises(ExperimentalAuthorityError):
        ExperimentalCaseOutcomeVocabulary(
            accounted_token=ACCOUNTED, unaccounted_token=ACCOUNTED
        )


def test_no_experimental_type_declares_a_field_naming_a_status_it_cannot_confer() -> (
    None
):
    from dataclasses import dataclass

    @dataclass(frozen=True)
    class Overreaching:
        is_born: bool

    with pytest.raises(RuntimeError):
        sweep_forbidden_fields(Overreaching)

    for owner in (
        DeclaredCaseSet,
        ExperimentalCandidateDeclaration,
        ExperimentalFailureRecord,
        ExperimentalRunRecord,
        ExperimentalRunRequest,
    ):
        names = {declared.name.lstrip("_") for declared in fields(owner)}
        assert not names & {"is_born", "is_valid", "verdict", "certified", "rank"}


def test_the_experimental_error_is_not_catchable_as_a_birth_protocol_error() -> None:
    assert not issubclass(ExperimentalAuthorityError, BirthExperimentSpecificationError)
    assert not issubclass(BirthExperimentSpecificationError, ExperimentalAuthorityError)


def test_the_authority_exposes_no_certifying_or_admitting_surface() -> None:
    surface = {name for name in vars(ExperimentalAuthority) if not name.startswith("_")}

    assert surface == {"authority_id", "run"}


def test_every_named_law_opens_with_its_own_name() -> None:
    assert EXPERIMENTAL_NAMED_LAWS
    for name, text in EXPERIMENTAL_NAMED_LAWS.items():
        assert text.startswith(f"{name}:")
