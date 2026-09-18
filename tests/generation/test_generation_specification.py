"""مواصفةُ الإنتاج: مصدرُها نجاحٌ سابق، ولا تُعيد كتابةَ النسبة ولا تحمل رتبة.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import fields, replace

import pytest
from generation_cases import (
    FIRST_ANCHOR_ID,
    PREDICATE_ID,
    SECOND_ANCHOR_ID,
    lexical_choice,
    passing_envelope,
    production_specification,
    two_anchor_document,
)

from alghanem.execution.engine import execute_document
from alghanem.execution.outcome import ExecutionOutcome
from alghanem.generation.specification import (
    _SOURCE_REF_ISSUANCE,
    PAST_ACTIVE_TRANSITIVE_VSO,
    FormSelectionMode,
    GenerationSpecificationError,
    LexicalChoiceRef,
    PassedNisbahSourceRef,
    ProductionSpecification,
    RealizationConstraint,
    RealizationConstraintKind,
    RealizationConstraintValue,
    RealizationTargetAssignment,
    RequestedSentenceForm,
    RequestedTense,
    RequestedVoice,
    SourceElementKind,
    SourceInventorySnapshot,
    SyntacticRealizationTarget,
)


def test_source_ref_is_read_from_a_passing_envelope() -> None:
    envelope = passing_envelope()
    assert envelope.core.outcome is ExecutionOutcome.PASS
    ref = PassedNisbahSourceRef.from_envelope(envelope)
    assert ref.nisbah_id == envelope.declaration.nisbah.nisbah_id
    assert ref.execution_digest == envelope.execution_digest
    assert ref.law_set_digest == envelope.core.law_set_digest


def test_a_blocked_execution_is_not_a_generation_source() -> None:
    document = two_anchor_document()
    nisbah = document["nisbah"]
    assert isinstance(nisbah, dict)
    predicate = nisbah["predicate"]
    assert isinstance(predicate, dict)
    predicate["arity"] = 1
    report = execute_document(document)
    envelope = report.envelope
    assert envelope is not None
    assert envelope.core.outcome is not ExecutionOutcome.PASS
    with pytest.raises(GenerationSpecificationError):
        PassedNisbahSourceRef.from_envelope(envelope)


def test_the_specification_carries_neither_rank_nor_residuals() -> None:
    names = {field.name for field in fields(ProductionSpecification)}
    assert "rank" not in names
    assert "residuals" not in names
    assert "evidence" not in names


def test_the_specification_does_not_restate_the_source_structure() -> None:
    names = {field.name for field in fields(ProductionSpecification)}
    assert "relation_kind" not in names
    assert "predicate_anchor" not in names
    assert "argument_anchors" not in names


def test_a_specification_holds_no_surface_form() -> None:
    with pytest.raises(GenerationSpecificationError):
        LexicalChoiceRef(
            choice_id="choice.verb",
            element_id=PREDICATE_ID,
            entry_id="كتب",
            entry_content_id="content.entry.verb",
            lexical_source_id="lexicon.gen0.synthetic",
            lexical_source_digest="digest.lexicon.gen0.synthetic",
            form_selection_mode=(FormSelectionMode.LEXICALLY_ATTESTED_FORM_SELECTION),
        )


def test_root_derivation_is_refused_until_gen_morph_1() -> None:
    with pytest.raises(GenerationSpecificationError):
        LexicalChoiceRef(
            choice_id="choice.verb",
            element_id=PREDICATE_ID,
            entry_id="entry.verb",
            entry_content_id="content.entry.verb",
            lexical_source_id="lexicon.gen0.synthetic",
            lexical_source_digest="digest.lexicon.gen0.synthetic",
            form_selection_mode=FormSelectionMode.DERIVED_FROM_ROOT,
        )


def test_a_position_is_not_claimed_of_the_predicate_and_the_anchor_alike() -> None:
    with pytest.raises(GenerationSpecificationError):
        RealizationTargetAssignment(
            element_kind=SourceElementKind.ANCHOR,
            element_id=FIRST_ANCHOR_ID,
            target=SyntacticRealizationTarget.PREDICATE_POSITION,
        )
    with pytest.raises(GenerationSpecificationError):
        RealizationTargetAssignment(
            element_kind=SourceElementKind.PREDICATE,
            element_id=PREDICATE_ID,
            target=SyntacticRealizationTarget.FAA_IL_POSITION,
        )


def test_an_element_absent_from_the_source_has_no_position() -> None:
    envelope = passing_envelope()
    with pytest.raises(GenerationSpecificationError):
        ProductionSpecification.for_passed_execution(
            envelope=envelope,
            production_id="production.synthetic.absent",
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
                    element_id="anchor.never.declared",
                    target=SyntacticRealizationTarget.MAF_UL_BIH_POSITION,
                ),
            ),
            lexical_choice_refs=(
                lexical_choice(PREDICATE_ID, "entry.verb"),
                lexical_choice(FIRST_ANCHOR_ID, "entry.agentive.noun"),
                lexical_choice("anchor.never.declared", "entry.object.noun"),
            ),
            realization_constraints=(),
        )


def test_the_family_positions_are_complete_and_ordered() -> None:
    specification = production_specification()
    assert (
        tuple(item.target for item in specification.realization_targets)
        == PAST_ACTIVE_TRANSITIVE_VSO.surface_order
    )
    with pytest.raises(GenerationSpecificationError):
        replace(
            specification,
            realization_targets=specification.realization_targets[:2],
            lexical_choice_refs=specification.lexical_choice_refs[:2],
        )


def test_an_undetermined_request_does_not_enter_the_open_family() -> None:
    specification = production_specification()
    with pytest.raises(GenerationSpecificationError):
        replace(specification, requested_tense=RequestedTense.UNDETERMINED)
    with pytest.raises(GenerationSpecificationError):
        replace(specification, requested_voice=RequestedVoice.UNDETERMINED)
    with pytest.raises(GenerationSpecificationError):
        replace(
            specification,
            requested_sentence_form=RequestedSentenceForm.UNDETERMINED,
        )


def test_every_realized_element_has_exactly_one_lexical_choice() -> None:
    specification = production_specification()
    with pytest.raises(GenerationSpecificationError):
        replace(
            specification,
            lexical_choice_refs=specification.lexical_choice_refs[:2],
        )


def test_a_constraint_value_falls_under_its_own_kind() -> None:
    with pytest.raises(GenerationSpecificationError):
        RealizationConstraint(
            element_id=SECOND_ANCHOR_ID,
            kind=RealizationConstraintKind.NUMBER,
            value=RealizationConstraintValue.DEFINITE,
        )


def test_the_family_names_what_it_excludes_with_a_reason() -> None:
    excluded = PAST_ACTIVE_TRANSITIVE_VSO.excluded_features
    assert "passive_voice" in excluded
    assert "root_derivation" in excluded
    assert "phonological_realization" in excluded
    assert all(reason.strip() for reason in excluded.values())


def test_the_specification_content_is_stable_under_repetition() -> None:
    envelope = passing_envelope()
    first = production_specification(envelope)
    second = production_specification(envelope)
    assert first.as_canonical_content() == second.as_canonical_content()


def test_a_source_ref_is_not_constructible_by_its_caller() -> None:
    envelope = passing_envelope()
    ref = PassedNisbahSourceRef.from_envelope(envelope)
    with pytest.raises(GenerationSpecificationError):
        PassedNisbahSourceRef(
            nisbah_id=ref.nisbah_id,
            materialized_content_id=ref.materialized_content_id,
            input_digest=ref.input_digest,
            execution_digest=ref.execution_digest,
            law_set_digest=ref.law_set_digest,
            source_inventory=ref.source_inventory,
            issuance=object(),  # type: ignore[arg-type]
        )


def test_a_source_ref_carries_the_inventory_of_its_source_elements() -> None:
    ref = PassedNisbahSourceRef.from_envelope(passing_envelope())
    assert ref.kind_of(PREDICATE_ID) is SourceElementKind.PREDICATE
    assert ref.kind_of(FIRST_ANCHOR_ID) is SourceElementKind.ANCHOR
    assert ref.kind_of(SECOND_ANCHOR_ID) is SourceElementKind.ANCHOR
    assert ref.kind_of("anchor.never.declared") is None
    content = ref.as_canonical_content()
    assert content["source_inventory"] == ref.source_inventory.as_canonical_content()
    assert content["source_inventory_content_id"] == ref.source_inventory.content_id
    assert "issuance" not in content
    assert "issuance" not in ref.source_inventory.as_canonical_content()


def test_a_source_inventory_is_not_constructible_by_its_caller() -> None:
    ref = PassedNisbahSourceRef.from_envelope(passing_envelope())
    with pytest.raises(GenerationSpecificationError):
        SourceInventorySnapshot(
            elements=ref.source_inventory.elements,
            issuance=object(),  # type: ignore[arg-type]
        )


def test_a_source_inventory_carries_its_elements_not_only_their_digest() -> None:
    ref = PassedNisbahSourceRef.from_envelope(passing_envelope())
    inventory = ref.source_inventory
    assert {element.element_id for element in inventory.elements} == {
        PREDICATE_ID,
        FIRST_ANCHOR_ID,
        SECOND_ANCHOR_ID,
    }
    assert (
        inventory.content_id
        == SourceInventorySnapshot(
            elements=tuple(reversed(inventory.elements)),
            issuance=_SOURCE_REF_ISSUANCE,
        ).content_id
    )


def test_a_specification_is_not_constructible_beside_its_factory() -> None:
    specification = production_specification()
    with pytest.raises(GenerationSpecificationError):
        ProductionSpecification(
            production_id=specification.production_id,
            source_ref=specification.source_ref,
            production_family=specification.production_family,
            requested_tense=specification.requested_tense,
            requested_voice=specification.requested_voice,
            requested_sentence_form=specification.requested_sentence_form,
            realization_targets=specification.realization_targets,
            lexical_choice_refs=specification.lexical_choice_refs,
            realization_constraints=specification.realization_constraints,
            issuance=object(),  # type: ignore[arg-type]
        )


def test_the_source_check_binds_the_class_not_the_factory() -> None:
    specification = production_specification()
    forged = RealizationTargetAssignment(
        element_kind=SourceElementKind.ANCHOR,
        element_id="anchor.never.declared",
        target=SyntacticRealizationTarget.MAF_UL_BIH_POSITION,
    )
    with pytest.raises(GenerationSpecificationError):
        replace(
            specification,
            realization_targets=specification.realization_targets[:2] + (forged,),
            lexical_choice_refs=(
                specification.lexical_choice_refs[:2]
                + (lexical_choice("anchor.never.declared", "entry.object.noun"),)
            ),
            realization_constraints=(),
        )


def test_a_declared_kind_that_contradicts_the_source_is_refused() -> None:
    envelope = passing_envelope()
    with pytest.raises(GenerationSpecificationError):
        ProductionSpecification.for_passed_execution(
            envelope=envelope,
            production_id="production.synthetic.miskind",
            production_family=PAST_ACTIVE_TRANSITIVE_VSO,
            requested_tense=RequestedTense.PAST,
            requested_voice=RequestedVoice.ACTIVE,
            requested_sentence_form=RequestedSentenceForm.VERBAL_VSO,
            realization_targets=(
                RealizationTargetAssignment(
                    element_kind=SourceElementKind.PREDICATE,
                    element_id=FIRST_ANCHOR_ID,
                    target=SyntacticRealizationTarget.PREDICATE_POSITION,
                ),
                RealizationTargetAssignment(
                    element_kind=SourceElementKind.ANCHOR,
                    element_id=PREDICATE_ID,
                    target=SyntacticRealizationTarget.FAA_IL_POSITION,
                ),
                RealizationTargetAssignment(
                    element_kind=SourceElementKind.ANCHOR,
                    element_id=SECOND_ANCHOR_ID,
                    target=SyntacticRealizationTarget.MAF_UL_BIH_POSITION,
                ),
            ),
            lexical_choice_refs=(
                lexical_choice(FIRST_ANCHOR_ID, "entry.verb"),
                lexical_choice(PREDICATE_ID, "entry.agentive.noun"),
                lexical_choice(SECOND_ANCHOR_ID, "entry.object.noun"),
            ),
            realization_constraints=(),
        )


def test_a_constraint_on_an_element_outside_the_source_is_refused() -> None:
    specification = production_specification()
    with pytest.raises(GenerationSpecificationError):
        replace(
            specification,
            realization_constraints=(
                RealizationConstraint(
                    element_id="anchor.never.declared",
                    kind=RealizationConstraintKind.NUMBER,
                    value=RealizationConstraintValue.SINGULAR,
                ),
            ),
        )


def test_a_lexical_choice_ref_says_of_itself_that_it_is_a_claim() -> None:
    specification = production_specification()
    for choice in specification.lexical_choice_refs:
        assert choice.is_a_claim_until_the_readout.strip()
