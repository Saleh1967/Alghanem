"""الرتبُ والشهادة: لا رتبةَ يكتبها المستدعي، ولا شهادةَ تُصدَر في `GEN-0`.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import replace

import pytest
from generation_cases import generated_utterance, production_specification

from alghanem.generation.certificate import (
    GEN0_PRESERVED_INVARIANTS,
    CertifiedGeneratedUtterance,
    GenerationRankError,
    PreservedGenerationInvariant,
    RoundTripCertificate,
    RoundTripDecision,
    RoundTripGate,
    RoundTripStatus,
    StructuralLicensingGate,
    StructuralLicensingStatus,
    StructurallyLicensedSurface,
    SurfaceCandidate,
)
from alghanem.generation.specification import (
    CaseEffect,
    ProductionSpecification,
    SyntacticRealizationTarget,
)


def _candidate() -> tuple[SurfaceCandidate, ProductionSpecification]:
    specification = production_specification()
    utterance = generated_utterance(specification)
    candidate = SurfaceCandidate(
        utterance=utterance,
        specification_content_id=utterance.specification_content_id,
    )
    return candidate, specification


def test_the_first_rank_carries_no_licence_claim() -> None:
    candidate, _ = _candidate()
    assert isinstance(candidate, SurfaceCandidate)
    assert not isinstance(candidate, StructurallyLicensedSurface)


def test_the_second_rank_is_not_constructible_by_its_caller() -> None:
    candidate, specification = _candidate()
    with pytest.raises(GenerationRankError):
        StructurallyLicensedSurface(
            candidate=candidate,
            specification=specification,
            issuance=object(),  # type: ignore[arg-type]
        )


def test_the_gate_licenses_a_candidate_that_matches_its_specification() -> None:
    candidate, specification = _candidate()
    decision = StructuralLicensingGate.assess(
        candidate=candidate,
        specification=specification,
    )
    assert decision.status is StructuralLicensingStatus.LICENSED
    assert isinstance(decision.licensed, StructurallyLicensedSurface)
    assert decision.reason.strip()


def test_the_gate_refuses_a_case_effect_that_is_not_its_position_effect() -> None:
    candidate, specification = _candidate()
    tokens = candidate.utterance.tokens
    wrong = tuple(
        replace(token, case_effect=CaseEffect.NASB)
        if token.syntactic_target is SyntacticRealizationTarget.FAA_IL_POSITION
        else token
        for token in tokens
    )
    broken = replace(
        candidate,
        utterance=replace(candidate.utterance, tokens=wrong),
    )
    decision = StructuralLicensingGate.assess(
        candidate=broken,
        specification=specification,
    )
    assert decision.status is StructuralLicensingStatus.REFUSED
    assert decision.licensed is None


def test_the_gate_refuses_a_candidate_from_another_specification() -> None:
    candidate, specification = _candidate()
    other = replace(specification, production_id="production.synthetic.other")
    decision = StructuralLicensingGate.assess(candidate=candidate, specification=other)
    assert decision.status is StructuralLicensingStatus.REFUSED
    assert decision.licensed is None


def test_the_round_trip_gate_only_defers_today() -> None:
    candidate, specification = _candidate()
    decision = StructuralLicensingGate.assess(
        candidate=candidate,
        specification=specification,
    )
    licensed = decision.licensed
    assert licensed is not None
    verdict = RoundTripGate.assess(licensed=licensed)
    assert isinstance(verdict, RoundTripDecision)
    assert verdict.status is RoundTripStatus.DEFERRED_NO_FUNCTION_RECOVERING_ANALYSER
    assert verdict.certificate is None
    assert verdict.invariant_spec is GEN0_PRESERVED_INVARIANTS
    assert tuple(RoundTripStatus) == (
        RoundTripStatus.DEFERRED_NO_FUNCTION_RECOVERING_ANALYSER,
    )


def test_a_certificate_cannot_be_issued_by_a_caller() -> None:
    with pytest.raises(GenerationRankError):
        RoundTripCertificate(
            forward_trace_content_id="a" * 64,
            backward_structure_content_id="b" * 64,
            invariant_spec=GEN0_PRESERVED_INVARIANTS,
            invariant_match={
                component: True for component in GEN0_PRESERVED_INVARIANTS.components
            },
            residuals=(),
            issuance=object(),  # type: ignore[arg-type]
        )


def test_the_third_rank_is_not_constructible_without_a_certificate() -> None:
    candidate, specification = _candidate()
    decision = StructuralLicensingGate.assess(
        candidate=candidate,
        specification=specification,
    )
    licensed = decision.licensed
    assert licensed is not None
    with pytest.raises(GenerationRankError):
        CertifiedGeneratedUtterance(
            licensed=licensed,
            certificate=None,  # type: ignore[arg-type]
            issuance=object(),  # type: ignore[arg-type]
        )


def test_the_preserved_invariants_are_frozen_and_complete() -> None:
    assert GEN0_PRESERVED_INVARIANTS.components == tuple(PreservedGenerationInvariant)
    assert PreservedGenerationInvariant.CASE_RELATIONS in (
        GEN0_PRESERVED_INVARIANTS.components
    )
