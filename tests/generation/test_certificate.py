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

from alghanem.generation.authority_gaps import (
    NO_INDEPENDENT_ANCHOR_TO_SYNTACTIC_FUNCTION_AUTHORITY,
    NO_VERIFIED_LEXICAL_ATTESTATION,
)
from alghanem.generation.candidate import (
    GeneratedArabicUtterance,
    GenerationCandidateError,
    OrthographicProjection,
    SurfaceToken,
)
from alghanem.generation.certificate import (
    CONFORMANCE_AUTHORITY_GAPS,
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
from alghanem.generation.specification import (
    CaseEffect,
    FormSelectionMode,
    ProductionSpecification,
    SyntacticRealizationTarget,
)
from alghanem.generation.trace import GenerationStep, GenerationTrace


def _candidate() -> tuple[SurfaceCandidate, ProductionSpecification]:
    specification = production_specification()
    utterance = generated_utterance(specification)
    candidate = SurfaceCandidate(
        utterance=utterance,
        specification_content_id=utterance.specification_content_id,
    )
    return candidate, specification


def _projection_of(
    utterance: GeneratedArabicUtterance, tokens: tuple[SurfaceToken, ...]
) -> OrthographicProjection:
    projection = utterance.orthographic_projection
    return OrthographicProjection(
        case_effect_content_id=projection.case_effect_content_id,
        tokens=tokens,
        orthographic_source=FormSelectionMode.LEXICALLY_ATTESTED_FORM_SELECTION,
    )


def _with_tokens(
    candidate: SurfaceCandidate, tokens: tuple[SurfaceToken, ...]
) -> SurfaceCandidate:
    """أعِد بناءَ مرشَّحٍ برموزٍ أخرى مع سلسلةٍ متّصلةٍ بها؛ فالاتّصالُ شرطُ بناء."""

    projection = _projection_of(candidate.utterance, tokens)
    steps = candidate.utterance.trace.steps
    last = steps[-1]
    rebuilt = GenerationTrace(
        steps=steps[:-1]
        + (
            GenerationStep(
                stage=last.stage,
                rule_id=last.rule_id,
                input_content_id=last.input_content_id,
                output_content_id=projection.content_id,
                residuals=(),
            ),
        )
    )
    return replace(
        candidate,
        utterance=replace(
            candidate.utterance,
            orthographic_projection=projection,
            trace=rebuilt,
        ),
    )


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
    broken = _with_tokens(candidate, wrong)
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
    assert decision.open_authority_gaps == CONFORMANCE_AUTHORITY_GAPS
    assert set(decision.open_authority_gaps) == {
        NO_INDEPENDENT_ANCHOR_TO_SYNTACTIC_FUNCTION_AUTHORITY,
        NO_VERIFIED_LEXICAL_ATTESTATION,
    }
    assert all(gap.discharge_condition.strip() for gap in decision.open_authority_gaps)


def test_an_authority_gap_is_not_an_observed_residual() -> None:
    candidate, specification = _candidate()
    decision = SpecificationConformanceGate.assess(
        candidate=candidate,
        specification=specification,
    )
    observed = {residual.subject_id for residual in candidate.residuals}
    for gap in decision.open_authority_gaps:
        assert gap.gap_id not in observed
        assert not hasattr(gap, "stage")


def test_a_conformant_rank_cannot_be_issued_without_its_gaps() -> None:
    candidate, specification = _candidate()
    decision = SpecificationConformanceGate.assess(
        candidate=candidate,
        specification=specification,
    )
    with pytest.raises(GenerationRankError):
        replace(decision, open_authority_gaps=())


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


def test_an_utterance_cannot_carry_tokens_its_chain_did_not_project() -> None:
    candidate, _ = _candidate()
    tokens = candidate.utterance.tokens
    forged = (replace(tokens[0], surface="زعمٌ"),) + tokens[1:]
    with pytest.raises(GenerationCandidateError):
        replace(
            candidate.utterance,
            orthographic_projection=_projection_of(candidate.utterance, forged),
        )


def test_the_gate_refuses_a_token_trace_that_is_merely_adjacent() -> None:
    candidate, specification = _candidate()
    tokens = candidate.utterance.tokens
    stray_trace, _, _ = token_trace(inverted_production_specification(), PREDICATE_ID)
    forged = (replace(tokens[0], generation_trace=stray_trace),) + tokens[1:]
    decision = SpecificationConformanceGate.assess(
        candidate=_with_tokens(candidate, forged),
        specification=specification,
    )
    assert decision.status is SpecificationConformanceStatus.REFUSED
    assert decision.conformant is None
    assert decision.open_authority_gaps == ()
