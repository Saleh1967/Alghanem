"""G0.EX.1e: which frozen experiment is a run a run *of*?

Every assertion here is about one leak: a record produced under one frozen
experiment must not be offerable against another one that merely shares its
domain, or shares its name across a revision. `SameDomainIsNotSameExperiment`
and `SameExperimentNameIsNotSameFrozenContent` are read here from the binding
authority's side and from the gate's.
"""

from dataclasses import replace

import pytest
from test_experimental import (  # type: ignore[import-not-found]
    bound,
    case_set,
    experiment_binding,
    implementation_for,
    request,
)
from test_independent_closure_composition import (  # type: ignore[import-not-found]
    frozen_specification_binding,
    specification,
)

from alghanem.kernel.experimental import (
    ExperimentalAuthority,
    ExperimentalAuthorityError,
)
from alghanem.kernel.experimental_comparison import ExperimentalReplayAuthority
from alghanem.kernel.experimental_evidence_gate import ExperimentalEvidenceGate
from alghanem.kernel.experimental_request_content_identity import (
    request_content_digest,
)
from alghanem.kernel.experimental_run_binding import (
    EXPERIMENTAL_BINDING_NAMED_LAWS,
    BoundExperimentalRunRequest,
    ExperimentalRunBindingAuthority,
)
from alghanem.kernel.trace import Trace


def replayed(bound_request: object) -> tuple[object, object]:
    authority = ExperimentalAuthority(authority_id="lab")
    first = authority.run(
        run_id="run-1",
        bound_request=bound_request,  # type: ignore[arg-type]
        implementation=implementation_for(frozenset({"c2"})),  # type: ignore[arg-type]
    )
    second = authority.run(
        run_id="run-2",
        bound_request=bound_request,  # type: ignore[arg-type]
        implementation=implementation_for(frozenset({"c2"})),  # type: ignore[arg-type]
    )
    replay = ExperimentalReplayAuthority(authority_id="replay").observe(
        observation_id="replay-1", records=(first, second)
    )
    return first, replay


def test_binding_derives_the_request_identity_rather_than_accepting_one() -> None:
    run_request = request()

    bound_request = bound(run_request)

    assert type(bound_request) is BoundExperimentalRunRequest
    assert bound_request.request is run_request
    assert bound_request.request_content_digest == request_content_digest(run_request)
    assert bound_request.experiment_content_id == experiment_binding().content_id  # type: ignore[attr-defined]
    assert bound_request.domain == "finite-domain"
    assert f"request_content:{bound_request.request_content_digest}" in (
        bound_request.trace.events
    )


def test_a_bound_request_cannot_be_constructed_outside_the_authority() -> None:
    lawful = bound()

    with pytest.raises(ExperimentalAuthorityError):
        BoundExperimentalRunRequest(
            binding_id="fabricated",
            issuing_authority_id="whoever",
            bound_request=lawful.request,
            request_content_id=lawful.request_content_id,
            binding=lawful.binding,
            trace=Trace(("fabricated",)),
        )


def test_a_request_declared_for_another_scope_is_never_bound() -> None:
    other_domain = frozen_specification_binding(
        replace(specification(), domain="some-other-domain")
    )

    with pytest.raises(ExperimentalAuthorityError):
        ExperimentalRunBindingAuthority(authority_id="binding").bind(
            binding_id="binding-1", request=request(), binding=other_domain
        )


def test_a_record_bound_to_one_experiment_is_refused_against_another() -> None:
    """`SameDomainIsNotSameExperiment`, read as a provenance leak refusal."""

    experiment_a = experiment_binding("experiment-a")
    experiment_b = experiment_binding("experiment-b")
    assert experiment_a.specification.domain == experiment_b.specification.domain  # type: ignore[attr-defined]

    bound_to_a = bound(request(cases=case_set()), binding=experiment_a)
    record, replay = replayed(bound_to_a)

    with pytest.raises(ExperimentalAuthorityError):
        ExperimentalEvidenceGate(gate_id="gate").offer(
            offer_id="offer-1",
            record=record,  # type: ignore[arg-type]
            replay=replay,  # type: ignore[arg-type]
            bound_request=bound_to_a,
            binding=experiment_b,  # type: ignore[arg-type]
        )


def test_one_experiment_name_across_two_revisions_is_two_experiments() -> None:
    """`SameExperimentNameIsNotSameFrozenContent`."""

    first_revision = specification(experiment_id="experiment")
    second_revision = replace(first_revision, revision_id="r2", revision_sequence=2)
    binding_r1 = frozen_specification_binding(first_revision)
    binding_r2 = frozen_specification_binding(second_revision)
    assert binding_r1.specification.experiment_id == (
        binding_r2.specification.experiment_id
    )
    assert binding_r1.content_id != binding_r2.content_id

    bound_to_r1 = bound(request(cases=case_set()), binding=binding_r1)
    record, replay = replayed(bound_to_r1)

    with pytest.raises(ExperimentalAuthorityError):
        ExperimentalEvidenceGate(gate_id="gate").offer(
            offer_id="offer-1",
            record=record,  # type: ignore[arg-type]
            replay=replay,  # type: ignore[arg-type]
            bound_request=bound_to_r1,
            binding=binding_r2,
        )


def test_a_record_of_another_run_is_refused_against_this_binding() -> None:
    authority = ExperimentalRunBindingAuthority(authority_id="binding")
    first = bound(
        request(cases=case_set()), binding_id="binding-1", authority=authority
    )
    other = bound(
        request(cases=case_set(("c1", "c2"))),
        binding_id="binding-2",
        authority=authority,
    )
    record, replay = replayed(first)

    with pytest.raises(ExperimentalAuthorityError):
        ExperimentalEvidenceGate(gate_id="gate").offer(
            offer_id="offer-1",
            record=record,  # type: ignore[arg-type]
            replay=replay,  # type: ignore[arg-type]
            bound_request=other,
            binding=experiment_binding(),  # type: ignore[arg-type]
        )


def test_one_request_is_not_bound_to_two_experiments_in_one_authority() -> None:
    authority = ExperimentalRunBindingAuthority(authority_id="binding")
    run_request = request()
    authority.bind(
        binding_id="binding-1",
        request=run_request,
        binding=experiment_binding("experiment-a"),  # type: ignore[arg-type]
    )

    with pytest.raises(ExperimentalAuthorityError):
        authority.bind(
            binding_id="binding-2",
            request=run_request,
            binding=experiment_binding("experiment-b"),  # type: ignore[arg-type]
        )


def test_binding_ids_are_injective_within_one_authority() -> None:
    authority = ExperimentalRunBindingAuthority(authority_id="binding")
    authority.bind(
        binding_id="binding-1",
        request=request(),
        binding=experiment_binding(),  # type: ignore[arg-type]
    )

    with pytest.raises(ExperimentalAuthorityError):
        authority.bind(
            binding_id="binding-1",
            request=request(cases=case_set(("c1",))),
            binding=experiment_binding(),  # type: ignore[arg-type]
        )


def test_a_bound_request_confers_nothing() -> None:
    bound_request = bound()

    assert bound_request.confers_authorized_evidence is False
    assert bound_request.confers_birth is False
    assert bound_request.confers_necessity is False


def test_the_binding_authority_exposes_no_running_or_offering_surface() -> None:
    surface = {
        name
        for name in vars(ExperimentalRunBindingAuthority)
        if not name.startswith("_")
    }

    assert surface == {"authority_id", "bind"}


def test_every_named_law_opens_with_its_own_name() -> None:
    assert EXPERIMENTAL_BINDING_NAMED_LAWS
    for name, text in EXPERIMENTAL_BINDING_NAMED_LAWS.items():
        assert text.startswith(f"{name}:")
