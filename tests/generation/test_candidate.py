"""سلسلةُ الإنتاج: مراحلُ مفصولةٌ بالنوع، وإسقاطٌ صوتيٌّ محجوزٌ لا فراغ.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import replace

import pytest
from generation_cases import (
    FIRST_ANCHOR_ID,
    PREDICATE_ID,
    generated_utterance,
    production_specification,
    token_trace,
)

from alghanem.generation.candidate import (
    CaseEffectCandidate,
    CompositionCandidate,
    GeneratedStage,
    GenerationCandidateError,
    MorphologicalOperation,
    OrthographicProjection,
    SurfaceToken,
    WithheldStage,
    specification_content_id,
    withheld_phonological_projection,
)
from alghanem.generation.specification import (
    PAST_ACTIVE_TRANSITIVE_VSO,
    CaseEffect,
    FormSelectionMode,
    SyntacticRealizationTarget,
)
from alghanem.generation.trace import (
    GenerationResidualKind,
    GenerationStage,
    GenerationStep,
)


def test_no_surface_token_without_its_source_anchor() -> None:
    utterance = generated_utterance(production_specification())
    token = utterance.tokens[0]
    with pytest.raises(GenerationCandidateError):
        replace(token, source_element_id="   ")


def test_a_surface_token_is_a_form_not_an_identifier() -> None:
    utterance = generated_utterance(production_specification())
    with pytest.raises(GenerationCandidateError):
        replace(utterance.tokens[0], surface="token.without.a.form")


def test_no_word_form_without_a_morphological_trace() -> None:
    utterance = generated_utterance(production_specification())
    with pytest.raises(GenerationCandidateError):
        replace(utterance.tokens[0], morphological_operation_trace=())


def test_the_only_licensed_morphological_operation_is_attested_selection() -> None:
    assert tuple(MorphologicalOperation) == (
        MorphologicalOperation.LEXICALLY_ATTESTED_FORM_SELECTION,
    )


def test_no_composition_without_one_relation_behind_it() -> None:
    specification = production_specification()
    utterance = generated_utterance(specification)
    _, _, first = token_trace(specification, PREDICATE_ID)
    _, _, second = token_trace(specification, FIRST_ANCHOR_ID)
    with pytest.raises(GenerationCandidateError):
        CompositionCandidate(
            specification_content_id=utterance.specification_content_id,
            source_nisbah_id=specification.source_ref.nisbah_id,
            assignments=(first, replace(second, source_nisbah_id="nisbah.other")),
            surface_order=PAST_ACTIVE_TRANSITIVE_VSO.surface_order[:2],
        )


def test_case_effect_follows_the_licensed_position() -> None:
    family = PAST_ACTIVE_TRANSITIVE_VSO
    assert (
        family.case_effect_for(SyntacticRealizationTarget.FAA_IL_POSITION)
        is CaseEffect.RAF
    )
    assert (
        family.case_effect_for(SyntacticRealizationTarget.MAF_UL_BIH_POSITION)
        is CaseEffect.NASB
    )
    assert (
        family.case_effect_for(SyntacticRealizationTarget.PREDICATE_POSITION)
        is CaseEffect.NO_EFFECT_IN_THIS_FAMILY
    )


def test_an_unregistered_position_has_no_inferred_case_effect() -> None:
    candidate = CaseEffectCandidate(
        composition_content_id="a" * 64,
        effects={SyntacticRealizationTarget.FAA_IL_POSITION: CaseEffect.RAF},
    )
    with pytest.raises(GenerationCandidateError):
        candidate.effect_for(SyntacticRealizationTarget.MAF_UL_BIH_POSITION)


def test_the_phonological_projection_is_withheld_not_empty() -> None:
    utterance = generated_utterance(production_specification())
    withheld = withheld_phonological_projection(
        case_effect_content_id=utterance.trace.steps[1].output_content_id or "",
        rule_id="rule.phonology.withheld",
        subject_id=utterance.production_id,
    )
    assert isinstance(withheld, WithheldStage)
    assert not isinstance(withheld, GeneratedStage)
    assert withheld.step.output_content_id is None
    assert withheld.residual.kind is GenerationResidualKind.UNMEASURED_PROSODIC_LAYER


def test_the_orthographic_projection_is_not_a_child_of_the_withheld_phonology() -> None:
    specification = production_specification()
    utterance = generated_utterance(specification)
    orthographic_step = utterance.trace.steps[-1]
    assert orthographic_step.stage is GenerationStage.ORTHOGRAPHIC_PROJECTION
    case_effect_step = utterance.trace.steps[-2]
    assert case_effect_step.stage is GenerationStage.CASE_EFFECT
    assert orthographic_step.input_content_id == case_effect_step.output_content_id


def test_an_orthography_that_claims_derivation_is_refused() -> None:
    utterance = generated_utterance(production_specification())
    with pytest.raises(GenerationCandidateError):
        OrthographicProjection(
            case_effect_content_id="b" * 64,
            tokens=utterance.tokens,
            orthographic_source=FormSelectionMode.DERIVED_FROM_ROOT,
        )


def test_a_generated_stage_is_bound_to_the_step_that_produced_it() -> None:
    specification = production_specification()
    utterance = generated_utterance(specification)
    composition_step = utterance.trace.steps[0]
    payload = CaseEffectCandidate(
        composition_content_id=composition_step.output_content_id or "",
        effects={
            target: PAST_ACTIVE_TRANSITIVE_VSO.case_effect_for(target)
            for target in PAST_ACTIVE_TRANSITIVE_VSO.surface_order
        },
    )
    stage = GeneratedStage(
        stage=GenerationStage.CASE_EFFECT,
        payload=payload,
        step=utterance.trace.steps[1],
    )
    assert stage.content_id == payload.content_id
    with pytest.raises(GenerationCandidateError):
        GeneratedStage(
            stage=GenerationStage.CASE_EFFECT,
            payload=payload,
            step=utterance.trace.steps[0],
        )


def test_a_withheld_stage_holds_no_payload_and_names_its_residual() -> None:
    step = GenerationStep(
        stage=GenerationStage.PHONOLOGICAL_PROJECTION,
        rule_id="rule.phonology.withheld",
        input_content_id="c" * 64,
        output_content_id="d" * 64,
        residuals=(),
    )
    withheld = withheld_phonological_projection(
        case_effect_content_id="c" * 64,
        rule_id="rule.phonology.withheld",
        subject_id="production.synthetic.0",
    )
    with pytest.raises(GenerationCandidateError):
        WithheldStage(
            stage=GenerationStage.PHONOLOGICAL_PROJECTION,
            step=step,
            residual=withheld.residual,
        )


def test_one_source_element_does_not_emit_two_tokens() -> None:
    specification = production_specification()
    utterance = generated_utterance(specification)
    duplicated = utterance.tokens + (utterance.tokens[0],)
    with pytest.raises(GenerationCandidateError):
        replace(utterance, tokens=duplicated)


def test_the_token_residuals_are_read_from_its_own_trace() -> None:
    utterance = generated_utterance(production_specification())
    token: SurfaceToken = utterance.tokens[0]
    assert token.residuals == token.generation_trace.residuals


def test_the_utterance_is_bound_to_its_specification_content() -> None:
    specification = production_specification()
    utterance = generated_utterance(specification)
    assert utterance.specification_content_id == specification_content_id(specification)
