"""بُناةُ موادّ اختبارٍ للإنتاج: غلافُ نجاحٍ مُصطنَع، ومواصفةٌ من عائلة `GEN-0`.

هذه الوحدةُ **مادّةُ اختبارٍ لا جزءٌ من الطبقة**: لا معجمَ ذهبيًّا هنا ولا
وثيقةً مُراجَعة، فتلك مرحلةُ `G0.GEN-0.DATA`. وما يُبنى هنا مُصطنَعٌ بالكامل،
ويُصرَّح بذلك حتى لا تُقرأ صورةٌ عربيّةٌ في اختبارٍ شاهدًا لغويًّا.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from alghanem.execution.engine import execute_document
from alghanem.execution.result import ExecutionResultEnvelope
from alghanem.generation.candidate import (
    CaseEffectCandidate,
    CompositionCandidate,
    GeneratedArabicUtterance,
    LexicalSelectionCandidate,
    MorphologicalOperation,
    OrthographicProjection,
    RelationSlotAssignment,
    SurfaceToken,
    WordFormCandidate,
    specification_content_id,
)
from alghanem.generation.specification import (
    PAST_ACTIVE_TRANSITIVE_VSO,
    FormSelectionMode,
    LexicalChoiceRef,
    ProductionSpecification,
    RealizationConstraint,
    RealizationConstraintKind,
    RealizationConstraintValue,
    RealizationTargetAssignment,
    RequestedSentenceForm,
    RequestedTense,
    RequestedVoice,
    SourceElementKind,
    SyntacticRealizationTarget,
)
from alghanem.generation.trace import (
    GenerationStage,
    GenerationStep,
    GenerationTrace,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "execution"))

from execution_cases import mutate, valid_document  # noqa: E402

PREDICATE_ID = "predicate.A"
FIRST_ANCHOR_ID = "anchor.first"
SECOND_ANCHOR_ID = "anchor.second"


def two_anchor_document() -> dict[str, Any]:
    """وثيقةٌ ناجحةٌ بمرساتين؛ فالعائلةُ الأولى تحتاج فاعلًا ومفعولًا ظاهرين."""

    document = mutate(valid_document())
    nisbah: Any = document["nisbah"]
    first: Any = nisbah["anchors"][0]
    second = mutate(first)
    second["anchor_id"] = SECOND_ANCHOR_ID
    nisbah["anchors"] = [first, second]
    return document


def passing_envelope() -> ExecutionResultEnvelope:
    """غلافُ نتيجةٍ حكمُه نجاح؛ ولا يُبنى الإنتاجُ على غيره."""

    report = execute_document(two_anchor_document())
    envelope = report.envelope
    assert envelope is not None
    return envelope


def lexical_choice(element_id: str, entry_id: str) -> LexicalChoiceRef:
    """اختيارٌ معجميٌّ مُصطنَع: مرجعٌ مُبصَّمٌ لا صورةٌ سطحيّة."""

    return LexicalChoiceRef(
        choice_id=f"choice.{element_id}",
        element_id=element_id,
        entry_id=entry_id,
        entry_content_id=f"content.{entry_id}",
        lexical_source_id="lexicon.gen0.synthetic",
        lexical_source_digest="digest.lexicon.gen0.synthetic",
        form_selection_mode=FormSelectionMode.LEXICALLY_ATTESTED_FORM_SELECTION,
    )


def production_specification(
    envelope: ExecutionResultEnvelope | None = None,
) -> ProductionSpecification:
    """مواصفةُ إنتاجٍ كاملةٌ من العائلة الأولى، مبنيّةٌ على غلافٍ ناجح."""

    source = passing_envelope() if envelope is None else envelope
    return ProductionSpecification.for_passed_execution(
        envelope=source,
        production_id="production.synthetic.0",
        production_family=PAST_ACTIVE_TRANSITIVE_VSO,
        requested_tense=RequestedTense.PAST,
        requested_voice=RequestedVoice.ACTIVE,
        requested_sentence_form=RequestedSentenceForm.VERBAL_VSO,
        realization_targets=(
            RealizationTargetAssignment(
                element_kind=SourceElementKind.PREDICATE,
                element_id=PREDICATE_ID,
                target=SyntacticRealizationTarget.PREDICATE_POSITION,
            ),
            RealizationTargetAssignment(
                element_kind=SourceElementKind.ANCHOR,
                element_id=FIRST_ANCHOR_ID,
                target=SyntacticRealizationTarget.FAA_IL_POSITION,
            ),
            RealizationTargetAssignment(
                element_kind=SourceElementKind.ANCHOR,
                element_id=SECOND_ANCHOR_ID,
                target=SyntacticRealizationTarget.MAF_UL_BIH_POSITION,
            ),
        ),
        lexical_choice_refs=(
            lexical_choice(PREDICATE_ID, "entry.verb"),
            lexical_choice(FIRST_ANCHOR_ID, "entry.agentive.noun"),
            lexical_choice(SECOND_ANCHOR_ID, "entry.object.noun"),
        ),
        realization_constraints=(
            RealizationConstraint(
                element_id=FIRST_ANCHOR_ID,
                kind=RealizationConstraintKind.NUMBER,
                value=RealizationConstraintValue.SINGULAR,
            ),
            RealizationConstraint(
                element_id=SECOND_ANCHOR_ID,
                kind=RealizationConstraintKind.DEFINITENESS,
                value=RealizationConstraintValue.DEFINITE,
            ),
        ),
    )


def inverted_production_specification(
    envelope: ExecutionResultEnvelope | None = None,
) -> ProductionSpecification:
    """المواصفةُ نفسُها بتعيينٍ مقلوب: المرساةُ الأولى مفعولًا والثانيةُ فاعلًا.

    ولا شيءَ في المصدر يمنع هذا القلب، لأنّه لا يحمل رابطةَ
    `Anchor → SyntacticFunction`؛ وهذه مادّةُ شاهدٍ على بقيّةٍ مُسمّاة لا حلٌّ لها.
    """

    source = passing_envelope() if envelope is None else envelope
    return ProductionSpecification.for_passed_execution(
        envelope=source,
        production_id="production.synthetic.inverted",
        production_family=PAST_ACTIVE_TRANSITIVE_VSO,
        requested_tense=RequestedTense.PAST,
        requested_voice=RequestedVoice.ACTIVE,
        requested_sentence_form=RequestedSentenceForm.VERBAL_VSO,
        realization_targets=(
            RealizationTargetAssignment(
                element_kind=SourceElementKind.PREDICATE,
                element_id=PREDICATE_ID,
                target=SyntacticRealizationTarget.PREDICATE_POSITION,
            ),
            RealizationTargetAssignment(
                element_kind=SourceElementKind.ANCHOR,
                element_id=SECOND_ANCHOR_ID,
                target=SyntacticRealizationTarget.FAA_IL_POSITION,
            ),
            RealizationTargetAssignment(
                element_kind=SourceElementKind.ANCHOR,
                element_id=FIRST_ANCHOR_ID,
                target=SyntacticRealizationTarget.MAF_UL_BIH_POSITION,
            ),
        ),
        lexical_choice_refs=(
            lexical_choice(PREDICATE_ID, "entry.verb"),
            lexical_choice(SECOND_ANCHOR_ID, "entry.agentive.noun"),
            lexical_choice(FIRST_ANCHOR_ID, "entry.object.noun"),
        ),
        realization_constraints=(),
    )


SYNTHETIC_SURFACES: dict[str, str] = {
    PREDICATE_ID: "فعلَ",
    FIRST_ANCHOR_ID: "اسمٌ",
    SECOND_ANCHOR_ID: "اسمًا",
}


def token_trace(
    specification: ProductionSpecification, element_id: str
) -> tuple[GenerationTrace, WordFormCandidate, RelationSlotAssignment]:
    """أثرُ رمزٍ واحد: اختيارٌ، فصورةٌ، فإسنادٌ إلى موقعٍ في نسبة المصدر."""

    spec_content_id = specification_content_id(specification)
    target = specification.target_of(element_id)
    choice = next(
        item
        for item in specification.lexical_choice_refs
        if item.element_id == element_id
    )
    selection = LexicalSelectionCandidate(
        production_id=specification.production_id,
        specification_content_id=spec_content_id,
        element_id=element_id,
        target=target,
        choice=choice,
    )
    word_form = WordFormCandidate(
        selection_content_id=selection.content_id,
        element_id=element_id,
        target=target,
        lexical_form_ref=f"{choice.entry_id}.form",
        morphological_operation_trace=(
            MorphologicalOperation.LEXICALLY_ATTESTED_FORM_SELECTION,
        ),
    )
    assignment = RelationSlotAssignment(
        word_form_content_id=word_form.content_id,
        element_id=element_id,
        target=target,
        source_nisbah_id=specification.source_ref.nisbah_id,
        source_execution_digest=specification.source_ref.execution_digest,
    )
    trace = GenerationTrace(
        steps=(
            GenerationStep(
                stage=GenerationStage.LEXICAL_SELECTION,
                rule_id="rule.select.lexical.choice",
                input_content_id=spec_content_id,
                output_content_id=selection.content_id,
                residuals=(),
            ),
            GenerationStep(
                stage=GenerationStage.WORD_FORM,
                rule_id="rule.attested.form.selection",
                input_content_id=selection.content_id,
                output_content_id=word_form.content_id,
                residuals=(),
            ),
            GenerationStep(
                stage=GenerationStage.RELATION_SLOT_ASSIGNMENT,
                rule_id="rule.assign.relation.slot",
                input_content_id=word_form.content_id,
                output_content_id=assignment.content_id,
                residuals=(),
            ),
        )
    )
    return trace, word_form, assignment


def generated_utterance(
    specification: ProductionSpecification,
) -> GeneratedArabicUtterance:
    """عبارةٌ مُصطنَعةٌ كاملةُ الأثر؛ صورُها موادُّ اختبارٍ لا شواهدُ لغويّة."""

    spec_content_id = specification_content_id(specification)
    family = specification.production_family
    tokens: list[SurfaceToken] = []
    assignments: list[RelationSlotAssignment] = []
    for item in specification.realization_targets:
        trace, _, assignment = token_trace(specification, item.element_id)
        assignments.append(assignment)
        choice = next(
            choice
            for choice in specification.lexical_choice_refs
            if choice.element_id == item.element_id
        )
        tokens.append(
            SurfaceToken(
                token_id=f"token.{item.element_id}",
                surface=SYNTHETIC_SURFACES[item.element_id],
                source_element_id=item.element_id,
                lexical_choice_id=choice.choice_id,
                morphological_operation_trace=(
                    MorphologicalOperation.LEXICALLY_ATTESTED_FORM_SELECTION,
                ),
                syntactic_target=item.target,
                case_effect=family.case_effect_for(item.target),
                generation_trace=trace,
            )
        )
    composition = CompositionCandidate(
        specification_content_id=spec_content_id,
        source_nisbah_id=specification.source_ref.nisbah_id,
        assignments=tuple(assignments),
        surface_order=family.surface_order,
    )
    case_effect = CaseEffectCandidate(
        composition_content_id=composition.content_id,
        effects={
            target: family.case_effect_for(target) for target in family.surface_order
        },
    )
    orthographic = OrthographicProjection(
        case_effect_content_id=case_effect.content_id,
        tokens=tuple(tokens),
        orthographic_source=FormSelectionMode.LEXICALLY_ATTESTED_FORM_SELECTION,
    )
    steps = (
        GenerationStep(
            stage=GenerationStage.COMPOSITION,
            rule_id="rule.compose.by.relation",
            input_content_id=spec_content_id,
            output_content_id=composition.content_id,
            residuals=(),
        ),
        GenerationStep(
            stage=GenerationStage.CASE_EFFECT,
            rule_id="rule.case.effect.of.position",
            input_content_id=composition.content_id,
            output_content_id=case_effect.content_id,
            residuals=(),
        ),
        GenerationStep(
            stage=GenerationStage.ORTHOGRAPHIC_PROJECTION,
            rule_id="rule.project.attested.orthography",
            input_content_id=case_effect.content_id,
            output_content_id=orthographic.content_id,
            residuals=(),
        ),
    )
    return GeneratedArabicUtterance(
        production_id=specification.production_id,
        specification_content_id=spec_content_id,
        orthographic_content_id=orthographic.content_id,
        tokens=tuple(tokens),
        trace=GenerationTrace(steps=steps),
    )
