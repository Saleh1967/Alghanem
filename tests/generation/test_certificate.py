"""الرتبُ والشهادة: لا رتبةَ يكتبها المستدعي، ولا شهادةَ تُصدَر في `GEN-0`.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import replace

import pytest
from generation_cases import (
    FIRST_ANCHOR_ID,
    PREDICATE_ID,
    SECOND_ANCHOR_ID,
    generated_utterance,
    inverted_production_specification,
    production_specification,
    token_trace,
)

from alghanem.generation.certificate import (
    CONFORMANCE_RESIDUALS,
    GEN0_PRESERVED_INVARIANTS,
    CertifiedGeneratedUtterance,
    GenerationRankError,
    PreservedGenerationInvariant,
    RoundTripCertificate,
    RoundTripDecision,
    RoundTripGate,
    RoundTripStatus,
    SpecificationConformanceGate,
    SpecificationConformanceStatus,
    SpecificationConformantSurface,
    SurfaceCandidate,
)
from alghanem.generation.laws import (
    NO_INDEPENDENT_ANCHOR_TO_SYNTACTIC_FUNCTION_AUTHORITY_ID,
)
from alghanem.generation.specification import (
    CaseEffect,
    ProductionSpecification,
    SyntacticRealizationTarget,
)
from alghanem.generation.trace import GenerationResidualKind, GenerationStage


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
    assert not isinstance(candidate, SpecificationConformantSurface)


def test_the_second_rank_is_not_constructible_by_its_caller() -> None:
    candidate, specification = _candidate()
    with pytest.raises(GenerationRankError):
        SpecificationConformantSurface(
            candidate=candidate,
            specification=specification,
            issuance=object(),  # type: ignore[arg-type]
        )


def test_the_gate_finds_a_candidate_conformant_to_its_specification() -> None:
    candidate, specification = _candidate()
    decision = SpecificationConformanceGate.assess(
        candidate=candidate,
        specification=specification,
    )
    assert decision.status is SpecificationConformanceStatus.CONFORMANT
    assert isinstance(decision.conformant, SpecificationConformantSurface)
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
    decision = SpecificationConformanceGate.assess(
        candidate=broken,
        specification=specification,
    )
    assert decision.status is SpecificationConformanceStatus.REFUSED
    assert decision.conformant is None


def test_the_gate_refuses_a_candidate_from_another_specification() -> None:
    candidate, specification = _candidate()
    other = replace(specification, production_id="production.synthetic.other")
    decision = SpecificationConformanceGate.assess(
        candidate=candidate,
        specification=other,
    )
    assert decision.status is SpecificationConformanceStatus.REFUSED
    assert decision.conformant is None


def test_the_round_trip_gate_only_defers_today() -> None:
    candidate, specification = _candidate()
    decision = SpecificationConformanceGate.assess(
        candidate=candidate,
        specification=specification,
    )
    conformant = decision.conformant
    assert conformant is not None
    verdict = RoundTripGate.assess(conformant=conformant)
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
    decision = SpecificationConformanceGate.assess(
        candidate=candidate,
        specification=specification,
    )
    conformant = decision.conformant
    assert conformant is not None
    with pytest.raises(GenerationRankError):
        CertifiedGeneratedUtterance(
            conformant=conformant,
            certificate=None,  # type: ignore[arg-type]
            issuance=object(),  # type: ignore[arg-type]
        )


def test_the_preserved_invariants_are_frozen_and_complete() -> None:
    assert GEN0_PRESERVED_INVARIANTS.components == tuple(PreservedGenerationInvariant)
    assert PreservedGenerationInvariant.CASE_RELATIONS in (
        GEN0_PRESERVED_INVARIANTS.components
    )


def test_a_conformance_decision_names_what_it_did_not_prove() -> None:
    candidate, specification = _candidate()
    decision = SpecificationConformanceGate.assess(
        candidate=candidate,
        specification=specification,
    )
    assert decision.residuals == CONFORMANCE_RESIDUALS
    kinds = {residual.kind for residual in decision.residuals}
    assert kinds == {
        GenerationResidualKind.UNLICENSED_SYNTACTIC_FUNCTION_ASSIGNMENT,
        GenerationResidualKind.UNATTESTED_LEXICAL_REFERENCE,
    }
    assert all(
        residual.stage is GenerationStage.SPECIFICATION_CONFORMANCE
        for residual in decision.residuals
    )
    assert any(
        residual.subject_id == NO_INDEPENDENT_ANCHOR_TO_SYNTACTIC_FUNCTION_AUTHORITY_ID
        for residual in decision.residuals
    )


def test_a_conformant_rank_cannot_be_issued_without_its_residuals() -> None:
    candidate, specification = _candidate()
    decision = SpecificationConformanceGate.assess(
        candidate=candidate,
        specification=specification,
    )
    with pytest.raises(GenerationRankError):
        replace(decision, residuals=())


def test_the_gate_conforms_an_inverted_function_assignment() -> None:
    """شاهدُ `RES.GEN0.NoIndependentAnchorToSyntacticFunctionAuthority`.

    تعيينُ الفاعليّة والمفعوليّة دعوى صاحب المواصفة؛ فلو قُلِبت بين المرساتين
    لمنحت البوّابةُ المطابقةَ نفسَها، لأنّها تقيس حفظَ الدعوى لا ترخيصَها.
    """

    specification = inverted_production_specification()
    utterance = generated_utterance(specification)
    candidate = SurfaceCandidate(
        utterance=utterance,
        specification_content_id=utterance.specification_content_id,
    )
    decision = SpecificationConformanceGate.assess(
        candidate=candidate,
        specification=specification,
    )
    assert decision.status is SpecificationConformanceStatus.CONFORMANT
    assert specification.target_of(FIRST_ANCHOR_ID) is (
        SyntacticRealizationTarget.MAF_UL_BIH_POSITION
    )
    assert specification.target_of(SECOND_ANCHOR_ID) is (
        SyntacticRealizationTarget.FAA_IL_POSITION
    )


def test_the_gate_refuses_an_utterance_whose_tokens_are_not_its_projection() -> None:
    candidate, specification = _candidate()
    tokens = candidate.utterance.tokens
    forged = (replace(tokens[0], surface="زعمٌ"),) + tokens[1:]
    broken = replace(
        candidate,
        utterance=replace(candidate.utterance, tokens=forged),
    )
    decision = SpecificationConformanceGate.assess(
        candidate=broken,
        specification=specification,
    )
    assert decision.status is SpecificationConformanceStatus.REFUSED
    assert decision.conformant is None
    assert decision.residuals == ()


def test_the_gate_refuses_an_utterance_that_claims_a_foreign_projection() -> None:
    candidate, specification = _candidate()
    broken = replace(
        candidate,
        utterance=replace(candidate.utterance, orthographic_content_id="c" * 64),
    )
    decision = SpecificationConformanceGate.assess(
        candidate=broken,
        specification=specification,
    )
    assert decision.status is SpecificationConformanceStatus.REFUSED
    assert decision.conformant is None


def test_the_gate_refuses_a_token_trace_that_is_merely_adjacent() -> None:
    candidate, specification = _candidate()
    tokens = candidate.utterance.tokens
    stranger = inverted_production_specification()
    stray_trace, _, _ = token_trace(stranger, PREDICATE_ID)
    forged = (replace(tokens[0], generation_trace=stray_trace),) + tokens[1:]
    broken = replace(
        candidate,
        utterance=replace(candidate.utterance, tokens=forged),
    )
    decision = SpecificationConformanceGate.assess(
        candidate=broken,
        specification=specification,
    )
    assert decision.status is SpecificationConformanceStatus.REFUSED
    assert decision.conformant is None
