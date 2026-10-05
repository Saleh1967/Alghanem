"""G0.EX.1b: two models on one case set, and one candidate run twice.

The readings asserted here are deliberately weak: which cases each declared
model left unaccounted, whether one set is strictly contained in the other, and
whether repeated runs agreed. None of the four contrast statuses, including the
one where the richer model closes strictly more, confers necessity or birth.
"""

import pytest
from test_experimental import (  # type: ignore[import-not-found]
    ACCOUNTED,
    UNACCOUNTED,
    bound,
    candidate,
    case_set,
    implementation_for,
    request,
    vocabulary,
)

from alghanem.kernel.experimental import (
    ExperimentalAuthority,
    ExperimentalAuthorityError,
    ExperimentalOperationRef,
    ExperimentalOutcomeStatus,
    ExperimentalRunContext,
    ExperimentalRunRequest,
)
from alghanem.kernel.experimental_comparison import (
    EXPERIMENTAL_COMPARISON_NAMED_LAWS,
    ExperimentalContrastAuthority,
    ExperimentalReplayAuthority,
    ModelContrastStatus,
)
from alghanem.kernel.trace import Trace


def run_for(
    authority: ExperimentalAuthority,
    *,
    run_id: str,
    cases: object,
    model_ref: str,
    unaccounted: frozenset[str],
) -> object:
    return authority.run(
        run_id=run_id,
        bound_request=bound(
            request(cases=cases, model_ref=model_ref),  # type: ignore[arg-type]
            binding_id=f"binding-{run_id}",
        ),
        implementation=implementation_for(unaccounted),  # type: ignore[arg-type]
    )


def test_the_richer_model_closing_strictly_more_is_still_not_necessity() -> None:
    cases = case_set()
    authority = ExperimentalAuthority(authority_id="lab")
    instruction_only = run_for(
        authority,
        run_id="model-a",
        cases=cases,
        model_ref="instruction-only",
        unaccounted=frozenset({"c2", "c3"}),
    )
    rule_and_instructions = run_for(
        authority,
        run_id="model-b",
        cases=cases,
        model_ref="rule-plus-instructions",
        unaccounted=frozenset({"c3"}),
    )

    observation = ExperimentalContrastAuthority(authority_id="contrast").observe(
        observation_id="contrast-1",
        record_a=instruction_only,  # type: ignore[arg-type]
        record_b=rule_and_instructions,  # type: ignore[arg-type]
    )

    assert observation.status is ModelContrastStatus.B_CLOSES_STRICT_SUPERSET
    assert observation.cases_unexplained_by_a == ("c2", "c3")
    assert observation.cases_unexplained_by_b == ("c3",)
    assert observation.cases_closed_only_by_b == ("c2",)
    assert observation.cases_closed_only_by_a == ()
    assert observation.confers_necessity is False
    assert observation.confers_birth is False
    assert observation.confers_residual_certification is False


def test_a_weaker_model_that_accounts_for_everything_leaves_nothing_to_birth() -> None:
    cases = case_set()
    authority = ExperimentalAuthority(authority_id="lab")
    weaker = run_for(
        authority,
        run_id="model-a",
        cases=cases,
        model_ref="instruction-only",
        unaccounted=frozenset(),
    )
    richer = run_for(
        authority,
        run_id="model-b",
        cases=cases,
        model_ref="rule-plus-instructions",
        unaccounted=frozenset(),
    )

    observation = ExperimentalContrastAuthority(authority_id="contrast").observe(
        observation_id="contrast-1",
        record_a=weaker,  # type: ignore[arg-type]
        record_b=richer,  # type: ignore[arg-type]
    )

    assert observation.status is ModelContrastStatus.NO_DIFFERENCE_OBSERVED
    assert observation.cases_closed_only_by_b == ()


def test_each_model_closing_what_the_other_left_open_is_incomparable() -> None:
    cases = case_set()
    authority = ExperimentalAuthority(authority_id="lab")
    first = run_for(
        authority,
        run_id="model-a",
        cases=cases,
        model_ref="model-a",
        unaccounted=frozenset({"c1"}),
    )
    second = run_for(
        authority,
        run_id="model-b",
        cases=cases,
        model_ref="model-b",
        unaccounted=frozenset({"c2"}),
    )

    observation = ExperimentalContrastAuthority(authority_id="contrast").observe(
        observation_id="contrast-1",
        record_a=first,  # type: ignore[arg-type]
        record_b=second,  # type: ignore[arg-type]
    )

    assert observation.status is ModelContrastStatus.INCOMPARABLE_DIFFERENCE
    assert observation.cases_closed_only_by_b == ("c1",)
    assert observation.cases_closed_only_by_a == ("c2",)


def test_the_weaker_model_may_also_close_the_strict_superset() -> None:
    cases = case_set()
    authority = ExperimentalAuthority(authority_id="lab")
    first = run_for(
        authority,
        run_id="model-a",
        cases=cases,
        model_ref="model-a",
        unaccounted=frozenset(),
    )
    second = run_for(
        authority,
        run_id="model-b",
        cases=cases,
        model_ref="model-b",
        unaccounted=frozenset({"c1"}),
    )

    observation = ExperimentalContrastAuthority(authority_id="contrast").observe(
        observation_id="contrast-1",
        record_a=first,  # type: ignore[arg-type]
        record_b=second,  # type: ignore[arg-type]
    )

    assert observation.status is ModelContrastStatus.A_CLOSES_STRICT_SUPERSET


def test_runs_over_two_different_case_sets_are_refused_rather_than_reconciled() -> None:
    authority = ExperimentalAuthority(authority_id="lab")
    first = run_for(
        authority,
        run_id="model-a",
        cases=case_set(),
        model_ref="model-a",
        unaccounted=frozenset({"c1"}),
    )
    second = run_for(
        authority,
        run_id="model-b",
        cases=case_set(("c1", "c2")),
        model_ref="model-b",
        unaccounted=frozenset({"c1"}),
    )

    with pytest.raises(ExperimentalAuthorityError):
        ExperimentalContrastAuthority(authority_id="contrast").observe(
            observation_id="contrast-1",
            record_a=first,  # type: ignore[arg-type]
            record_b=second,  # type: ignore[arg-type]
        )


def test_two_separately_declared_but_content_equal_case_sets_are_one_case_set() -> None:
    """`OneContentIdentityLawForSameness`: sameness is content, not object id."""

    authority = ExperimentalAuthority(authority_id="lab")
    first = run_for(
        authority,
        run_id="model-a",
        cases=case_set(),
        model_ref="model-a",
        unaccounted=frozenset({"c1"}),
    )
    second = run_for(
        authority,
        run_id="model-b",
        cases=case_set(),
        model_ref="model-b",
        unaccounted=frozenset({"c1", "c2"}),
    )
    assert first.case_set is not second.case_set  # type: ignore[attr-defined]

    observation = ExperimentalContrastAuthority(authority_id="contrast").observe(
        observation_id="contrast-1",
        record_a=first,  # type: ignore[arg-type]
        record_b=second,  # type: ignore[arg-type]
    )

    assert observation.status is ModelContrastStatus.A_CLOSES_STRICT_SUPERSET


def test_two_content_equal_requests_are_one_request_for_a_replay() -> None:
    """`OneContentIdentityLawForSameness`, read from the replay's own side."""

    authority = ExperimentalAuthority(authority_id="lab")
    cases = case_set()
    first = authority.run(
        run_id="run-1",
        bound_request=bound(request(cases=cases), binding_id="binding-1"),
        implementation=implementation_for(frozenset({"c2"})),
    )
    # A separately constructed, content-equal request and a second binding.
    second = authority.run(
        run_id="run-2",
        bound_request=bound(request(cases=case_set()), binding_id="binding-2"),
        implementation=implementation_for(frozenset({"c2"})),
    )
    assert first.request is not second.request

    replay = ExperimentalReplayAuthority(authority_id="replay").observe(
        observation_id="replay-1", records=(first, second)
    )

    assert replay.outputs_identical is True
    assert replay.traces_identical is True


def test_two_runs_of_one_request_identity_are_a_replay_and_not_a_contrast() -> None:
    authority = ExperimentalAuthority(authority_id="lab")
    shared = bound(request(cases=case_set()))
    first = authority.run(
        run_id="run-1",
        bound_request=shared,
        implementation=implementation_for(frozenset()),
    )
    second = authority.run(
        run_id="run-2",
        bound_request=shared,
        implementation=implementation_for(frozenset()),
    )

    with pytest.raises(ExperimentalAuthorityError):
        ExperimentalContrastAuthority(authority_id="contrast").observe(
            observation_id="contrast-1", record_a=first, record_b=second
        )


def test_a_model_contrasted_with_itself_observes_nothing() -> None:
    cases = case_set()
    authority = ExperimentalAuthority(authority_id="lab")
    first = run_for(
        authority,
        run_id="model-a",
        cases=cases,
        model_ref="one-model",
        unaccounted=frozenset(),
    )
    same_model_again = run_for(
        authority,
        run_id="model-a-again",
        cases=cases,
        model_ref="one-model",
        unaccounted=frozenset(),
    )
    contrast = ExperimentalContrastAuthority(authority_id="contrast")

    with pytest.raises(ExperimentalAuthorityError):
        contrast.observe(
            observation_id="contrast-1",
            record_a=first,  # type: ignore[arg-type]
            record_b=first,  # type: ignore[arg-type]
        )
    with pytest.raises(ExperimentalAuthorityError):
        contrast.observe(
            observation_id="contrast-2",
            record_a=first,  # type: ignore[arg-type]
            record_b=same_model_again,  # type: ignore[arg-type]
        )


def test_a_run_that_did_not_complete_has_no_per_case_reading_to_contrast() -> None:
    cases = case_set()
    authority = ExperimentalAuthority(authority_id="lab")
    completed = run_for(
        authority,
        run_id="model-a",
        cases=cases,
        model_ref="model-a",
        unaccounted=frozenset(),
    )

    def raising(
        context: ExperimentalRunContext, input_content: str
    ) -> tuple[str, Trace]:
        raise RuntimeError("stopped")

    failed = authority.run(
        run_id="model-b",
        bound_request=bound(request(cases=cases, model_ref="model-b")),
        implementation=raising,
    )
    assert failed.outcome_status is ExperimentalOutcomeStatus.FAILED

    with pytest.raises(ExperimentalAuthorityError):
        ExperimentalContrastAuthority(authority_id="contrast").observe(
            observation_id="contrast-1",
            record_a=completed,  # type: ignore[arg-type]
            record_b=failed,
        )


def test_a_replay_reads_agreement_without_claiming_reproducibility() -> None:
    cases = case_set()
    authority = ExperimentalAuthority(authority_id="lab")
    shared_request = bound(request(cases=cases))
    first = authority.run(
        run_id="run-1",
        bound_request=shared_request,
        implementation=implementation_for(frozenset({"c2"})),
    )
    second = authority.run(
        run_id="run-2",
        bound_request=shared_request,
        implementation=implementation_for(frozenset({"c2"})),
    )

    replay = ExperimentalReplayAuthority(authority_id="replay").observe(
        observation_id="replay-1", records=(first, second)
    )

    assert replay.outputs_identical is True
    assert replay.traces_identical is True
    assert replay.statuses_identical is True
    assert replay.run_ids == ("run-1", "run-2")
    assert replay.proves_reproducibility is False
    assert replay.proves_independent_replication is False


def test_a_replay_detects_a_second_run_that_disagreed() -> None:
    cases = case_set()
    authority = ExperimentalAuthority(authority_id="lab")
    shared_request = bound(request(cases=cases))
    first = authority.run(
        run_id="run-1",
        bound_request=shared_request,
        implementation=implementation_for(frozenset({"c2"})),
    )
    second = authority.run(
        run_id="run-2",
        bound_request=shared_request,
        implementation=implementation_for(frozenset({"c3"})),
    )

    replay = ExperimentalReplayAuthority(authority_id="replay").observe(
        observation_id="replay-1", records=(first, second)
    )

    assert replay.outputs_identical is False
    assert replay.traces_identical is False


def test_one_record_read_twice_is_not_a_replay() -> None:
    authority = ExperimentalAuthority(authority_id="lab")
    record = authority.run(
        run_id="run-1",
        bound_request=bound(),
        implementation=implementation_for(frozenset()),
    )

    with pytest.raises(ExperimentalAuthorityError):
        ExperimentalReplayAuthority(authority_id="replay").observe(
            observation_id="replay-1", records=(record, record)
        )


def test_replayed_runs_must_share_one_request() -> None:
    authority = ExperimentalAuthority(authority_id="lab")
    first = authority.run(
        run_id="run-1",
        bound_request=bound(),
        implementation=implementation_for(frozenset()),
    )
    other_request = ExperimentalRunRequest(
        candidate=candidate(),
        case_set=case_set(("c1",)),
        inputs=(("c1", "input:c1"),),
        permitted_operations=(ExperimentalOperationRef("apply"),),
        case_outcome_vocabulary=vocabulary(),
    )
    second = authority.run(
        run_id="run-2",
        bound_request=bound(other_request),
        implementation=implementation_for(frozenset()),
    )

    with pytest.raises(ExperimentalAuthorityError):
        ExperimentalReplayAuthority(authority_id="replay").observe(
            observation_id="replay-1", records=(first, second)
        )


def test_observation_ids_are_injective_within_each_authority() -> None:
    cases = case_set()
    authority = ExperimentalAuthority(authority_id="lab")
    shared_request = bound(request(cases=cases))
    first = authority.run(
        run_id="run-1",
        bound_request=shared_request,
        implementation=implementation_for(frozenset()),
    )
    second = authority.run(
        run_id="run-2",
        bound_request=shared_request,
        implementation=implementation_for(frozenset()),
    )
    replay_authority = ExperimentalReplayAuthority(authority_id="replay")
    replay_authority.observe(observation_id="replay-1", records=(first, second))

    with pytest.raises(ExperimentalAuthorityError):
        replay_authority.observe(observation_id="replay-1", records=(first, second))


def test_the_two_vocabulary_tokens_are_the_only_readable_outputs() -> None:
    assert ACCOUNTED != UNACCOUNTED


def test_every_named_law_opens_with_its_own_name() -> None:
    assert EXPERIMENTAL_COMPARISON_NAMED_LAWS
    for name, text in EXPERIMENTAL_COMPARISON_NAMED_LAWS.items():
        assert text.startswith(f"{name}:")
