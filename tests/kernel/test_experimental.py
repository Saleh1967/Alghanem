"""G0.EX.1a: what a run of a not-yet-born candidate proves, and what it cannot.

Every assertion here is about one boundary: an `ExperimentalRunRecord` records
observed facts under an authority that certifies nothing, and no branch of it --
completed, failed, or aborted -- confers birth, validity, identity, difference
from origin, necessity, or constitutional evidence.
"""

from dataclasses import fields

import pytest

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
    ExperimentalRunRecord,
    ExperimentalRunRequest,
    sweep_forbidden_fields,
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


def implementation_for(
    unaccounted: frozenset[str], *, operation: str = "apply"
) -> object:
    def implementation(input_content: str) -> tuple[str, Trace]:
        case_id = input_content.removeprefix("input:")
        token = UNACCOUNTED if case_id in unaccounted else ACCOUNTED
        return token, Trace((f"operation:{operation}", f"read:{case_id}"))

    return implementation


def test_a_completed_run_records_only_the_cases_its_model_left_unaccounted() -> None:
    authority = ExperimentalAuthority(authority_id="lab")

    record = authority.run(
        run_id="run-1",
        request=request(),
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

    def raising(_: str) -> tuple[str, Trace]:
        raise RuntimeError("the implementation gave up")

    completed = authority.run(
        run_id="completed",
        request=request(),
        implementation=implementation_for(frozenset()),
    )
    failed = authority.run(run_id="failed", request=request(), implementation=raising)

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
        request=request(),
        implementation=implementation_for(frozenset()),
    )

    with pytest.raises(ExperimentalAuthorityError):
        ExperimentalRunRecord(
            run_id="fabricated",
            issuing_authority_id="lab",
            request=issued.request,
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

    def raising(_: str) -> tuple[str, Trace]:
        raise ValueError("no")

    record = authority.run(run_id="run-1", request=request(), implementation=raising)

    assert record.outcome_status is ExperimentalOutcomeStatus.FAILED
    assert record.failure is not None
    assert record.failure.failure_kind is ExperimentalFailureKind.IMPLEMENTATION_RAISED
    assert record.failure.case_id == "c1"
    assert record.output_content is None
    assert record.records_failure is True


def test_an_unreadable_implementation_result_is_refused_as_a_failure() -> None:
    authority = ExperimentalAuthority(authority_id="lab")

    def wrong_shape(_: str) -> tuple[str, Trace]:
        return "just a string"  # type: ignore[return-value]

    record = authority.run(
        run_id="run-1", request=request(), implementation=wrong_shape
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

    def off_vocabulary(_: str) -> tuple[str, Trace]:
        return "PROBABLY_FINE", Trace(("operation:apply",))

    record = authority.run(
        run_id="run-1", request=request(), implementation=off_vocabulary
    )

    assert record.outcome_status is ExperimentalOutcomeStatus.FAILED
    assert record.failure is not None
    assert (
        record.failure.failure_kind is ExperimentalFailureKind.UNREADABLE_CASE_OUTCOME
    )


def test_an_operation_the_request_never_permitted_aborts_the_run() -> None:
    authority = ExperimentalAuthority(authority_id="lab")

    record = authority.run(
        run_id="run-1",
        request=request(permitted=("apply",)),
        implementation=implementation_for(frozenset(), operation="rewrite"),
    )

    assert record.outcome_status is ExperimentalOutcomeStatus.ABORTED
    assert record.failure is not None
    assert (
        record.failure.failure_kind is ExperimentalFailureKind.OPERATION_NOT_PERMITTED
    )
    assert record.output_content is None


def test_run_ids_are_injective_within_one_authority_only() -> None:
    first = ExperimentalAuthority(authority_id="lab-1")
    second = ExperimentalAuthority(authority_id="lab-2")
    implementation = implementation_for(frozenset())

    first.run(run_id="run", request=request(), implementation=implementation)
    with pytest.raises(ExperimentalAuthorityError):
        first.run(run_id="run", request=request(), implementation=implementation)

    # LocalInjectivity != PortableIdentity: a second issuer is uncoordinated.
    second.run(run_id="run", request=request(), implementation=implementation)


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
