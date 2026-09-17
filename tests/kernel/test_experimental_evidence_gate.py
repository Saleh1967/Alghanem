"""G0.EX.1c: the single door out of the experimental path, and its four locks.

An offer is refused unless the run's declared scope equals the frozen
experiment's own domain, a replay covering that very record agreed, and the
payload is derived rather than written. Even when all of that holds, the offer
is not an `AuthorizedEvidenceSnapshot`: the G0.2a.3 chain must still ingest it.
"""

import pytest
from test_experimental import (  # type: ignore[import-not-found]
    ACCOUNTED,
    UNACCOUNTED,
    candidate,
    case_set,
    implementation_for,
    request,
    vocabulary,
)
from test_independent_closure_composition import (  # type: ignore[import-not-found]
    frozen_specification_binding,
    specification,
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
    ExperimentalRunRequest,
)
from alghanem.kernel.experimental_comparison import (
    ExperimentalContrastAuthority,
    ExperimentalReplayAuthority,
)
from alghanem.kernel.experimental_evidence_gate import (
    EXPERIMENTAL_EVIDENCE_NAMED_LAWS,
    ExperimentalEvidenceGate,
    ExperimentalEvidenceOffer,
    encode_offer_payload,
)
from alghanem.kernel.trace import Trace


def binding() -> object:
    return frozen_specification_binding(specification())


def replayed_run(
    *,
    scope: str = "finite-domain",
    unaccounted: frozenset[str] = frozenset({"c2"}),
    agreeing: bool = True,
) -> tuple[object, object]:
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
    first = authority.run(
        run_id="run-1",
        request=run_request,
        implementation=implementation_for(unaccounted),  # type: ignore[arg-type]
    )
    second = authority.run(
        run_id="run-2",
        request=run_request,
        implementation=implementation_for(
            unaccounted if agreeing else frozenset({"c1"})
        ),  # type: ignore[arg-type]
    )
    replay = ExperimentalReplayAuthority(authority_id="replay").observe(
        observation_id="replay-1", records=(first, second)
    )
    return first, replay


def test_an_offer_records_a_derived_payload_and_confers_nothing() -> None:
    record, replay = replayed_run()

    offer = ExperimentalEvidenceGate(gate_id="gate").offer(
        offer_id="offer-1",
        record=record,  # type: ignore[arg-type]
        replay=replay,  # type: ignore[arg-type]
        binding=binding(),  # type: ignore[arg-type]
    )

    assert offer.payload == encode_offer_payload(record)  # type: ignore[arg-type]
    assert "observed_unexplained_cases=c2" in offer.payload
    assert offer.domain == "finite-domain"
    assert offer.records_failure is False
    assert offer.confers_authorized_evidence is False
    assert offer.confers_sufficiency is False
    assert offer.confers_residual_certification is False
    assert offer.confers_birth is False
    assert not isinstance(offer, AuthorizedEvidenceSnapshot)


def test_an_offer_cannot_be_constructed_outside_the_gate() -> None:
    record, replay = replayed_run()

    with pytest.raises(ExperimentalAuthorityError):
        ExperimentalEvidenceOffer(
            offer_id="fabricated",
            record=record,  # type: ignore[arg-type]
            replay=replay,  # type: ignore[arg-type]
            contrast=None,
            binding=binding(),  # type: ignore[arg-type]
            payload="whatever the caller wants assessed",
            trace=Trace(("fabricated",)),
        )


def test_a_run_declared_for_another_scope_is_refused() -> None:
    record, replay = replayed_run(scope="some-other-domain")

    with pytest.raises(ExperimentalAuthorityError):
        ExperimentalEvidenceGate(gate_id="gate").offer(
            offer_id="offer-1",
            record=record,  # type: ignore[arg-type]
            replay=replay,  # type: ignore[arg-type]
            binding=binding(),  # type: ignore[arg-type]
        )


def test_a_replay_that_disagreed_is_refused() -> None:
    record, replay = replayed_run(agreeing=False)

    with pytest.raises(ExperimentalAuthorityError):
        ExperimentalEvidenceGate(gate_id="gate").offer(
            offer_id="offer-1",
            record=record,  # type: ignore[arg-type]
            replay=replay,  # type: ignore[arg-type]
            binding=binding(),  # type: ignore[arg-type]
        )


def test_a_replay_of_some_other_candidate_does_not_cover_this_record() -> None:
    record, _ = replayed_run()
    _, other_replay = replayed_run()

    with pytest.raises(ExperimentalAuthorityError):
        ExperimentalEvidenceGate(gate_id="gate").offer(
            offer_id="offer-1",
            record=record,  # type: ignore[arg-type]
            replay=other_replay,  # type: ignore[arg-type]
            binding=binding(),  # type: ignore[arg-type]
        )


def test_a_fabricated_record_is_refused() -> None:
    _, replay = replayed_run()

    class LooksLikeARecord:
        run_id = "fabricated"

    with pytest.raises(ExperimentalAuthorityError):
        ExperimentalEvidenceGate(gate_id="gate").offer(
            offer_id="offer-1",
            record=LooksLikeARecord(),  # type: ignore[arg-type]
            replay=replay,  # type: ignore[arg-type]
            binding=binding(),  # type: ignore[arg-type]
        )
    with pytest.raises(ExperimentalAuthorityError):
        encode_offer_payload(LooksLikeARecord())  # type: ignore[arg-type]


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

    def raising(_: str) -> tuple[str, Trace]:
        raise RuntimeError("the implementation gave up")

    first = authority.run(run_id="run-1", request=run_request, implementation=raising)
    second = authority.run(run_id="run-2", request=run_request, implementation=raising)
    replay = ExperimentalReplayAuthority(authority_id="replay").observe(
        observation_id="replay-1", records=(first, second)
    )

    offer = ExperimentalEvidenceGate(gate_id="gate").offer(
        offer_id="offer-1",
        record=first,
        replay=replay,
        binding=binding(),  # type: ignore[arg-type]
    )

    assert first.outcome_status is ExperimentalOutcomeStatus.FAILED
    assert offer.records_failure is True
    assert "failure_kind=IMPLEMENTATION_RAISED" in offer.payload


def test_an_offered_contrast_must_contrast_this_very_record() -> None:
    cases = case_set()
    authority = ExperimentalAuthority(authority_id="lab")
    shared = request(cases=cases, model_ref="model-a")
    first = authority.run(
        run_id="a-1",
        request=shared,
        implementation=implementation_for(frozenset({"c2"})),
    )
    second = authority.run(
        run_id="a-2",
        request=shared,
        implementation=implementation_for(frozenset({"c2"})),
    )
    other = authority.run(
        run_id="b-1",
        request=request(cases=cases, model_ref="model-b"),
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
        binding=binding(),  # type: ignore[arg-type]
        contrast=contrast,
    )
    assert accepted.contrast is contrast

    with pytest.raises(ExperimentalAuthorityError):
        gate.offer(
            offer_id="offer-2",
            record=first,
            replay=replay,
            binding=binding(),  # type: ignore[arg-type]
            contrast=unrelated_contrast,
        )


def test_an_offer_becomes_assessable_only_through_the_acquisition_chain() -> None:
    record, replay = replayed_run()
    frozen_binding = binding()
    offer = ExperimentalEvidenceGate(gate_id="gate").offer(
        offer_id="offer-1",
        record=record,  # type: ignore[arg-type]
        replay=replay,  # type: ignore[arg-type]
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
    record, replay = replayed_run()
    gate = ExperimentalEvidenceGate(gate_id="gate")
    gate.offer(
        offer_id="offer-1",
        record=record,  # type: ignore[arg-type]
        replay=replay,  # type: ignore[arg-type]
        binding=binding(),  # type: ignore[arg-type]
    )

    with pytest.raises(ExperimentalAuthorityError):
        gate.offer(
            offer_id="offer-1",
            record=record,  # type: ignore[arg-type]
            replay=replay,  # type: ignore[arg-type]
            binding=binding(),  # type: ignore[arg-type]
        )


def test_the_payload_records_both_vocabulary_readings_verbatim() -> None:
    record, _ = replayed_run()
    payload = encode_offer_payload(record)  # type: ignore[arg-type]

    assert ACCOUNTED in payload
    assert UNACCOUNTED in payload
    assert f"candidate_id={candidate().candidate_id}" in payload


def test_every_named_law_opens_with_its_own_name() -> None:
    assert EXPERIMENTAL_EVIDENCE_NAMED_LAWS
    for name, text in EXPERIMENTAL_EVIDENCE_NAMED_LAWS.items():
        assert text.startswith(f"{name}:")
