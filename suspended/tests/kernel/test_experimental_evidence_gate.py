"""G0.EX.1c: the single door out of the experimental path, and its locks.

An offer is refused unless the record was produced from a request bound to the
very frozen experiment it is offered to, the run's declared scope equals that
experiment's own domain, a replay covering that very record agreed, and the
payload is the gate's own canonical manifest rather than anything a caller
wrote. Even when all of that holds, the offer is not an
`AuthorizedEvidenceSnapshot`: the G0.2a.3 chain must still ingest it.
"""

import json

import pytest
from test_experimental import (  # type: ignore[import-not-found]
    ACCOUNTED,
    UNACCOUNTED,
    bound,
    candidate,
    case_set,
    experiment_binding,
    implementation_for,
    request,
    vocabulary,
)

from alghanem.kernel.evidence_acquisition import (
    AuthorizedEvidenceSnapshot,
    EvidenceAcquisitionAuthority,
)
from alghanem.kernel.experimental import (
    DeclaredCaseSet,
    ExperimentalAuthority,
    ExperimentalAuthorityError,
    ExperimentalCandidateDeclaration,
    ExperimentalOperationRef,
    ExperimentalOutcomeStatus,
    ExperimentalRunContext,
    ExperimentalRunRequest,
)
from alghanem.kernel.experimental_comparison import (
    ExperimentalContrastAuthority,
    ExperimentalReplayAuthority,
)
from alghanem.kernel.experimental_evidence_gate import (
    EXPERIMENTAL_EVIDENCE_NAMED_LAWS,
    CanonicalExperimentalEvidenceEncoder,
    ExperimentalEvidenceGate,
    ExperimentalEvidenceOffer,
)
from alghanem.kernel.trace import Trace


def replayed_run(
    *,
    scope: str = "finite-domain",
    unaccounted: frozenset[str] = frozenset({"c2"}),
    agreeing: bool = True,
    frozen_binding: object | None = None,
) -> tuple[object, object, object]:
    authority = ExperimentalAuthority(authority_id="lab")
    cases = case_set()
    declaration = ExperimentalCandidateDeclaration(
        candidate_id="candidate",
        declared_origin_ref="origin",
        declared_scope=scope,
        declared_conditions=("isolated run",),
        declared_model_ref="model-b",
    )
    run_request = ExperimentalRunRequest(
        candidate=declaration,
        case_set=cases,
        inputs=tuple((case_id, f"input:{case_id}") for case_id in cases.case_ids),
        permitted_operations=(ExperimentalOperationRef("apply"),),
        case_outcome_vocabulary=vocabulary(),
    )
    bound_request = bound(
        run_request,
        binding=frozen_binding if frozen_binding is not None else scope_binding(scope),
    )
    first = authority.run(
        run_id="run-1",
        bound_request=bound_request,
        implementation=implementation_for(unaccounted),  # type: ignore[arg-type]
    )
    second = authority.run(
        run_id="run-2",
        bound_request=bound_request,
        implementation=implementation_for(
            unaccounted if agreeing else frozenset({"c1"})
        ),  # type: ignore[arg-type]
    )
    replay = ExperimentalReplayAuthority(authority_id="replay").observe(
        observation_id="replay-1", records=(first, second)
    )
    return first, replay, bound_request


def scope_binding(scope: str) -> object:
    """A frozen experiment whose domain is the run's declared scope.

    A mismatched scope is refused by the binding authority itself, so a run
    declared for another scope has to be bound to that other scope's own frozen
    experiment before the gate can read it at all.
    """

    if scope == "finite-domain":
        return experiment_binding()
    return other_domain_binding(scope)


def other_domain_binding(domain: str) -> object:
    from dataclasses import replace

    from test_independent_closure_composition import (  # type: ignore[import-not-found]
        frozen_specification_binding,
        specification,
    )

    return frozen_specification_binding(replace(specification(), domain=domain))


def decoded(payload: str) -> dict[str, object]:
    parsed = json.loads(payload)
    assert isinstance(parsed, dict)
    return parsed


def test_an_offer_records_a_derived_payload_and_confers_nothing() -> None:
    record, replay, bound_request = replayed_run()

    offer = ExperimentalEvidenceGate(gate_id="gate").offer(
        offer_id="offer-1",
        record=record,  # type: ignore[arg-type]
        replay=replay,  # type: ignore[arg-type]
        bound_request=bound_request,  # type: ignore[arg-type]
        binding=experiment_binding(),  # type: ignore[arg-type]
    )

    manifest = CanonicalExperimentalEvidenceEncoder.encode(
        record=record,  # type: ignore[arg-type]
        replay=replay,  # type: ignore[arg-type]
        bound_request=bound_request,  # type: ignore[arg-type]
    )
    content = decoded(offer.payload)
    assert offer.payload == manifest.payload
    assert offer.manifest_digest == manifest.digest
    assert content["record"]["observed_unexplained_cases"] == ["c2"]  # type: ignore[index]
    assert offer.domain == "finite-domain"
    assert offer.records_failure is False
    assert offer.confers_authorized_evidence is False
    assert offer.confers_sufficiency is False
    assert offer.confers_residual_certification is False
    assert offer.confers_birth is False
    assert not isinstance(offer, AuthorizedEvidenceSnapshot)


def test_an_offer_cannot_be_constructed_outside_the_gate() -> None:
    record, replay, bound_request = replayed_run()
    manifest = CanonicalExperimentalEvidenceEncoder.encode(
        record=record,  # type: ignore[arg-type]
        replay=replay,  # type: ignore[arg-type]
        bound_request=bound_request,  # type: ignore[arg-type]
    )

    with pytest.raises(ExperimentalAuthorityError):
        ExperimentalEvidenceOffer(
            offer_id="fabricated",
            record=record,  # type: ignore[arg-type]
            replay=replay,  # type: ignore[arg-type]
            contrast=None,
            bound_request=bound_request,  # type: ignore[arg-type]
            binding=experiment_binding(),  # type: ignore[arg-type]
            manifest=manifest,
            trace=Trace(("fabricated",)),
        )


def test_a_run_declared_for_another_scope_is_refused() -> None:
    record, replay, bound_request = replayed_run(scope="some-other-domain")

    with pytest.raises(ExperimentalAuthorityError):
        ExperimentalEvidenceGate(gate_id="gate").offer(
            offer_id="offer-1",
            record=record,  # type: ignore[arg-type]
            replay=replay,  # type: ignore[arg-type]
            bound_request=bound_request,  # type: ignore[arg-type]
            binding=experiment_binding(),  # type: ignore[arg-type]
        )


def test_a_replay_that_disagreed_is_refused() -> None:
    record, replay, bound_request = replayed_run(agreeing=False)

    with pytest.raises(ExperimentalAuthorityError):
        ExperimentalEvidenceGate(gate_id="gate").offer(
            offer_id="offer-1",
            record=record,  # type: ignore[arg-type]
            replay=replay,  # type: ignore[arg-type]
            bound_request=bound_request,  # type: ignore[arg-type]
            binding=experiment_binding(),  # type: ignore[arg-type]
        )


def test_a_replay_of_some_other_candidate_does_not_cover_this_record() -> None:
    record, _, bound_request = replayed_run()
    _, other_replay, _ = replayed_run()

    with pytest.raises(ExperimentalAuthorityError):
        ExperimentalEvidenceGate(gate_id="gate").offer(
            offer_id="offer-1",
            record=record,  # type: ignore[arg-type]
            replay=other_replay,  # type: ignore[arg-type]
            bound_request=bound_request,  # type: ignore[arg-type]
            binding=experiment_binding(),  # type: ignore[arg-type]
        )


def test_a_fabricated_record_is_refused() -> None:
    _, replay, bound_request = replayed_run()

    class LooksLikeARecord:
        run_id = "fabricated"

    with pytest.raises(ExperimentalAuthorityError):
        ExperimentalEvidenceGate(gate_id="gate").offer(
            offer_id="offer-1",
            record=LooksLikeARecord(),  # type: ignore[arg-type]
            replay=replay,  # type: ignore[arg-type]
            bound_request=bound_request,  # type: ignore[arg-type]
            binding=experiment_binding(),  # type: ignore[arg-type]
        )
    with pytest.raises(ExperimentalAuthorityError):
        CanonicalExperimentalEvidenceEncoder.encode(
            record=LooksLikeARecord(),  # type: ignore[arg-type]
            replay=replay,  # type: ignore[arg-type]
            bound_request=bound_request,  # type: ignore[arg-type]
        )


def test_a_fabricated_bound_request_is_refused() -> None:
    record, replay, bound_request = replayed_run()

    class LooksLikeABinding:
        request_content_digest = record.request_content_digest  # type: ignore[attr-defined]

    with pytest.raises(ExperimentalAuthorityError):
        ExperimentalEvidenceGate(gate_id="gate").offer(
            offer_id="offer-1",
            record=record,  # type: ignore[arg-type]
            replay=replay,  # type: ignore[arg-type]
            bound_request=LooksLikeABinding(),  # type: ignore[arg-type]
            binding=experiment_binding(),  # type: ignore[arg-type]
        )
    assert bound_request is not None


def test_a_failed_run_is_still_offered_and_marked_rather_than_dropped() -> None:
    authority = ExperimentalAuthority(authority_id="lab")
    cases = DeclaredCaseSet(case_set_id="case-set", case_ids=("c1",))
    declaration = ExperimentalCandidateDeclaration(
        candidate_id="candidate",
        declared_origin_ref="origin",
        declared_scope="finite-domain",
        declared_conditions=("isolated run",),
        declared_model_ref="model-b",
    )
    run_request = ExperimentalRunRequest(
        candidate=declaration,
        case_set=cases,
        inputs=(("c1", "input:c1"),),
        permitted_operations=(ExperimentalOperationRef("apply"),),
        case_outcome_vocabulary=vocabulary(),
    )

    def raising(
        context: ExperimentalRunContext, input_content: str
    ) -> tuple[str, Trace]:
        raise RuntimeError("the implementation gave up")

    bound_request = bound(run_request)
    first = authority.run(
        run_id="run-1", bound_request=bound_request, implementation=raising
    )
    second = authority.run(
        run_id="run-2", bound_request=bound_request, implementation=raising
    )
    replay = ExperimentalReplayAuthority(authority_id="replay").observe(
        observation_id="replay-1", records=(first, second)
    )

    offer = ExperimentalEvidenceGate(gate_id="gate").offer(
        offer_id="offer-1",
        record=first,
        replay=replay,
        bound_request=bound_request,
        binding=experiment_binding(),  # type: ignore[arg-type]
    )

    assert first.outcome_status is ExperimentalOutcomeStatus.FAILED
    assert offer.records_failure is True
    failure = decoded(offer.payload)["record"]["failure"]  # type: ignore[index]
    assert failure["failure_kind"] == "IMPLEMENTATION_RAISED"  # type: ignore[index]


def test_an_offered_contrast_must_contrast_this_very_record() -> None:
    cases = case_set()
    authority = ExperimentalAuthority(authority_id="lab")
    shared = bound(request(cases=cases, model_ref="model-a"), binding_id="binding-a")
    first = authority.run(
        run_id="a-1",
        bound_request=shared,
        implementation=implementation_for(frozenset({"c2"})),
    )
    second = authority.run(
        run_id="a-2",
        bound_request=shared,
        implementation=implementation_for(frozenset({"c2"})),
    )
    other = authority.run(
        run_id="b-1",
        bound_request=bound(
            request(cases=cases, model_ref="model-b"), binding_id="binding-b"
        ),
        implementation=implementation_for(frozenset()),
    )
    replay = ExperimentalReplayAuthority(authority_id="replay").observe(
        observation_id="replay-1", records=(first, second)
    )
    contrast = ExperimentalContrastAuthority(authority_id="contrast").observe(
        observation_id="contrast-1", record_a=first, record_b=other
    )
    unrelated_contrast = ExperimentalContrastAuthority(
        authority_id="contrast-2"
    ).observe(observation_id="contrast-2", record_a=second, record_b=other)
    gate = ExperimentalEvidenceGate(gate_id="gate")

    accepted = gate.offer(
        offer_id="offer-1",
        record=first,
        replay=replay,
        bound_request=shared,
        binding=experiment_binding(),  # type: ignore[arg-type]
        contrast=contrast,
    )
    assert accepted.contrast is contrast

    with pytest.raises(ExperimentalAuthorityError):
        gate.offer(
            offer_id="offer-2",
            record=first,
            replay=replay,
            bound_request=shared,
            binding=experiment_binding(),  # type: ignore[arg-type]
            contrast=unrelated_contrast,
        )


def test_an_offer_becomes_assessable_only_through_the_acquisition_chain() -> None:
    frozen_binding = experiment_binding()
    record, replay, bound_request = replayed_run(frozen_binding=frozen_binding)
    offer = ExperimentalEvidenceGate(gate_id="gate").offer(
        offer_id="offer-1",
        record=record,  # type: ignore[arg-type]
        replay=replay,  # type: ignore[arg-type]
        bound_request=bound_request,  # type: ignore[arg-type]
        binding=frozen_binding,  # type: ignore[arg-type]
    )

    authorization = EvidenceAcquisitionAuthority().authorize(
        authorization_id="authorization",
        binding=frozen_binding,  # type: ignore[arg-type]
    )
    snapshot = authorization.open_run("acquisition-run").ingest(
        snapshot_id="snapshot",
        payload=offer.payload,
        trace="ingested one experimental evidence offer",
    )

    assert type(snapshot) is AuthorizedEvidenceSnapshot
    assert snapshot.domain == offer.domain
    # The snapshot exists because the acquisition chain ran, not because the
    # offer was held: the gate itself issues no snapshot at all.
    assert not hasattr(ExperimentalEvidenceGate, "ingest")


def test_the_gate_exposes_no_certifying_admitting_or_ingesting_surface() -> None:
    surface = {
        name for name in vars(ExperimentalEvidenceGate) if not name.startswith("_")
    }

    assert surface == {"gate_id", "offer"}


def test_offer_ids_are_injective_within_one_gate() -> None:
    record, replay, bound_request = replayed_run()
    gate = ExperimentalEvidenceGate(gate_id="gate")
    gate.offer(
        offer_id="offer-1",
        record=record,  # type: ignore[arg-type]
        replay=replay,  # type: ignore[arg-type]
        bound_request=bound_request,  # type: ignore[arg-type]
        binding=experiment_binding(),  # type: ignore[arg-type]
    )

    with pytest.raises(ExperimentalAuthorityError):
        gate.offer(
            offer_id="offer-1",
            record=record,  # type: ignore[arg-type]
            replay=replay,  # type: ignore[arg-type]
            bound_request=bound_request,  # type: ignore[arg-type]
            binding=experiment_binding(),  # type: ignore[arg-type]
        )


def test_the_payload_records_both_vocabulary_readings_verbatim() -> None:
    record, replay, bound_request = replayed_run()
    manifest = CanonicalExperimentalEvidenceEncoder.encode(
        record=record,  # type: ignore[arg-type]
        replay=replay,  # type: ignore[arg-type]
        bound_request=bound_request,  # type: ignore[arg-type]
    )
    payload = manifest.payload

    assert ACCOUNTED in payload
    assert UNACCOUNTED in payload
    assert candidate().candidate_id in payload
    request_content = decoded(payload)["record"]["request"]  # type: ignore[index]
    assert request_content["inputs"] == [  # type: ignore[index]
        ["c1", "input:c1"],
        ["c2", "input:c2"],
        ["c3", "input:c3"],
    ]
    assert request_content["permitted_operations"] == ["apply"]  # type: ignore[index]


def test_two_readings_of_one_flat_encoding_do_not_share_a_manifest() -> None:
    """`CallerDoesNotWriteTheOfferedPayload`, read as a collision refusal.

    A flat `'|'.join` encoding cannot tell `("a|b",)` from `("a", "b")`; a
    structured canonical encoding must, or the provenance of what was tried is
    lost before acquisition ever sees it.
    """

    digests = set()
    for conditions in (("a|b",), ("a", "b")):
        authority = ExperimentalAuthority(authority_id="lab")
        cases = case_set(("c1",))
        declaration = ExperimentalCandidateDeclaration(
            candidate_id="candidate",
            declared_origin_ref="origin",
            declared_scope="finite-domain",
            declared_conditions=conditions,
            declared_model_ref="model-b",
        )
        run_request = ExperimentalRunRequest(
            candidate=declaration,
            case_set=cases,
            inputs=(("c1", "input:c1"),),
            permitted_operations=(ExperimentalOperationRef("apply"),),
            case_outcome_vocabulary=vocabulary(),
        )
        bound_request = bound(run_request)
        first = authority.run(
            run_id="run-1",
            bound_request=bound_request,
            implementation=implementation_for(frozenset()),
        )
        second = authority.run(
            run_id="run-2",
            bound_request=bound_request,
            implementation=implementation_for(frozenset()),
        )
        replay = ExperimentalReplayAuthority(authority_id="replay").observe(
            observation_id="replay-1", records=(first, second)
        )
        digests.add(
            CanonicalExperimentalEvidenceEncoder.encode(
                record=first, replay=replay, bound_request=bound_request
            ).digest
        )

    assert len(digests) == 2


def test_every_named_law_opens_with_its_own_name() -> None:
    assert EXPERIMENTAL_EVIDENCE_NAMED_LAWS
    for name, text in EXPERIMENTAL_EVIDENCE_NAMED_LAWS.items():
        assert text.startswith(f"{name}:")
