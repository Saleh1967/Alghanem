"""شهودٌ على الحدّ الأدنى المكتمل: مبرهنةٌ مشروطة، وقائمةُ تدقيقٍ صفرُها مُشتَقّ."""

from __future__ import annotations

from pathlib import Path

import pytest

from alghanem.arabic import minimal_complete_fiber as mcm_module
from alghanem.arabic.minimal_complete_fiber import (
    MINIMAL_COMPLETE_FIBER_NAMED_RESIDUALS,
    THE_CLOSURE_CHECKLIST,
    THE_DESIGNED_WITNESSES,
    AttributionCandidate,
    ChecklistCondition,
    ClosureChecklist,
    ClosureRequirement,
    DeletedComponent,
    FiberElement,
    MinimalCompleteFiberError,
    MinimalCompleteFiberVerdict,
    NecessityStanding,
    NecessityWitnessPair,
    RelationKind,
    StructuralFunction,
    SufficiencyStanding,
    a_separate_genus_field_is_required,
    assess_minimal_complete_fiber,
    assess_sufficiency,
    carried_functions,
    classification_information_is_required,
    delete,
    necessity_standing_of,
)
from alghanem.import_boundary import ImportBoundaryPolicy, audit_import_boundary

# --- الحدودُ البنيويّة --------------------------------------------------------


def test_the_minimal_complete_fiber_module_reaches_no_kernel_module() -> None:
    report = audit_import_boundary(
        (Path(str(mcm_module.__file__)),),
        ImportBoundaryPolicy(
            policy_id="minimal-complete-fiber",
            permitted_modules=(),
            forbidden_packages=("alghanem.kernel",),
        ),
    )
    assert not [
        name for name in report.reached_modules if name.startswith("alghanem.kernel")
    ]


def test_there_are_eight_named_residuals_all_distinct_and_non_blank() -> None:
    assert len(MINIMAL_COMPLETE_FIBER_NAMED_RESIDUALS) == 8
    assert len(set(MINIMAL_COMPLETE_FIBER_NAMED_RESIDUALS)) == 8
    assert all(note.strip() for note in MINIMAL_COMPLETE_FIBER_NAMED_RESIDUALS)


def test_no_refine_slot_operation_is_exported_by_this_deposit() -> None:
    exported = [
        name
        for name in mcm_module.__all__
        if callable(getattr(mcm_module, name))
        and ("refine" in name.lower() or "split" in name.lower())
    ]
    assert exported == []
    assert not hasattr(mcm_module, "RefineSlot")


# --- المعادلةُ التأسيسيّة ------------------------------------------------------


def test_four_representation_fields_carry_three_structural_functions() -> None:
    assert carried_functions() == (4, 3)
    assert len(StructuralFunction) == 3


def test_a_derivable_genus_needs_no_field_but_the_information_is_still_required() -> (
    None
):
    assert classification_information_is_required(True) is True
    assert classification_information_is_required(False) is True
    assert a_separate_genus_field_is_required(True) is False
    assert a_separate_genus_field_is_required(False) is True
    joined = "\n".join(MINIMAL_COMPLETE_FIBER_NAMED_RESIDUALS)
    assert "FourFieldsCarryThreeFunctions" in joined


def test_an_element_refuses_a_blank_anchor_genus_or_predicate() -> None:
    for anchor, genus, predicate in (("  ", "ج", "م"), ("ا", " ", "م"), ("ا", "ج", "")):
        with pytest.raises(MinimalCompleteFiberError):
            FiberElement(
                anchor=anchor,
                genus=genus,
                predicate=predicate,
                relation=RelationKind.PREDICATION,
            )


def test_the_relation_vocabulary_is_named_and_not_claimed_exhaustive() -> None:
    assert len(RelationKind) == 3
    joined = "\n".join(MINIMAL_COMPLETE_FIBER_NAMED_RESIDUALS)
    assert "TheRelationVocabularyIsNotClaimedExhaustive" in joined


# --- إسقاطاتُ الحذف وشواهدُ الضرورة -------------------------------------------


def test_each_deletion_erases_its_own_component_and_leaves_the_others() -> None:
    element = FiberElement(
        anchor="زيد",
        genus="شخصٌ مُعيَّن",
        predicate="طويل",
        relation=RelationKind.PREDICATION,
    )
    assert delete(element, DeletedComponent.CLASSIFICATION)[1] is None
    assert delete(element, DeletedComponent.PREDICATE)[2] is None
    assert delete(element, DeletedComponent.RELATION)[3] is None
    assert delete(element, DeletedComponent.RELATION)[0] == "زيد"


def test_an_unnamed_component_may_not_be_deleted() -> None:
    element = FiberElement(
        anchor="زيد",
        genus="شخصٌ مُعيَّن",
        predicate="طويل",
        relation=RelationKind.PREDICATION,
    )
    with pytest.raises(MinimalCompleteFiberError):
        delete(element, "التصنيف")  # type: ignore[arg-type]


def test_the_three_designed_witnesses_cover_the_three_components() -> None:
    assert len(THE_DESIGNED_WITNESSES) == 3
    assert {item.component for item in THE_DESIGNED_WITNESSES} == set(DeletedComponent)


def test_every_designed_witness_really_collides_under_its_own_deletion() -> None:
    for item in THE_DESIGNED_WITNESSES:
        assert delete(item.first, item.component) == delete(item.second, item.component)
        assert item.collides_under_deletion is True
        assert item.the_deleted_information_is_copied_in_another_field is False


def test_a_pair_that_does_not_collide_under_deletion_is_refused() -> None:
    with pytest.raises(MinimalCompleteFiberError):
        NecessityWitnessPair(
            component=DeletedComponent.PREDICATE,
            first=FiberElement(
                anchor="زيد",
                genus="شخصٌ مُعيَّن",
                predicate="طويل",
                relation=RelationKind.PREDICATION,
            ),
            second=FiberElement(
                anchor="عمرو",
                genus="شخصٌ مُعيَّن",
                predicate="قصير",
                relation=RelationKind.PREDICATION,
            ),
            first_content="الأوّل",
            second_content="الثاني",
            scope_note="تصميم",
        )


def test_a_pair_whose_content_agrees_proves_no_deletion_wrong() -> None:
    with pytest.raises(MinimalCompleteFiberError):
        NecessityWitnessPair(
            component=DeletedComponent.PREDICATE,
            first=FiberElement(
                anchor="زيد",
                genus="شخصٌ مُعيَّن",
                predicate="طويل",
                relation=RelationKind.PREDICATION,
            ),
            second=FiberElement(
                anchor="زيد",
                genus="شخصٌ مُعيَّن",
                predicate="قصير",
                relation=RelationKind.PREDICATION,
            ),
            first_content="مضمونٌ واحد",
            second_content="مضمونٌ واحد",
            scope_note="تصميم",
        )


def test_a_witness_without_a_written_scope_is_refused() -> None:
    with pytest.raises(MinimalCompleteFiberError):
        NecessityWitnessPair(
            component=DeletedComponent.RELATION,
            first=FiberElement(
                anchor="الرجل",
                genus="شخصٌ مُعيَّن",
                predicate="طويل",
                relation=RelationKind.RESTRICTION,
            ),
            second=FiberElement(
                anchor="الرجل",
                genus="شخصٌ مُعيَّن",
                predicate="طويل",
                relation=RelationKind.PREDICATION,
            ),
            first_content="تقييد",
            second_content="إخبار",
            scope_note="   ",
        )


def test_the_designed_witnesses_are_not_an_executed_codec_test() -> None:
    assert all(item.scope_note.strip() for item in THE_DESIGNED_WITNESSES)
    joined = "\n".join(MINIMAL_COMPLETE_FIBER_NAMED_RESIDUALS)
    assert "ADesignedWitnessIsNotAnExecutedCodecTest" in joined
    assert "ACollisionInTheRepresentationIsNotACollisionInContext" in joined


def test_necessity_is_witnessed_for_each_component_on_the_designed_pairs() -> None:
    for component in DeletedComponent:
        assert (
            necessity_standing_of(component)
            is NecessityStanding.WITNESSED_ON_THE_DESIGNED_PAIRS
        )


def test_necessity_is_not_witnessed_when_no_pair_is_supplied() -> None:
    assert necessity_standing_of(DeletedComponent.RELATION, ()) is (
        NecessityStanding.NOT_WITNESSED
    )


# --- المعيارُ بشطريه ----------------------------------------------------------


def test_sufficiency_is_untested_because_no_independent_reader_exists_here() -> None:
    assert assess_sufficiency() is (
        SufficiencyStanding.NO_INDEPENDENT_READER_IN_THIS_TREE
    )
    joined = "\n".join(MINIMAL_COMPLETE_FIBER_NAMED_RESIDUALS)
    assert "WithoutAnIndependentReaderSufficiencyIsUntested" in joined


def test_the_criterion_is_not_established_although_every_necessity_is_witnessed() -> (
    None
):
    verdict = assess_minimal_complete_fiber()
    assert verdict.every_component_is_witnessed is True
    assert verdict.is_established is False
    assert verdict.minimality_is_relative_to_the_tested_alternatives is True
    joined = "\n".join(MINIMAL_COMPLETE_FIBER_NAMED_RESIDUALS)
    assert "TheMinimumIsRelativeToTheTestedAlternatives" in joined


def test_a_verdict_that_drops_or_repeats_a_component_is_refused() -> None:
    standing = NecessityStanding.WITNESSED_ON_THE_DESIGNED_PAIRS
    with pytest.raises(MinimalCompleteFiberError):
        MinimalCompleteFiberVerdict(
            sufficiency=SufficiencyStanding.NO_INDEPENDENT_READER_IN_THIS_TREE,
            necessity=((DeletedComponent.PREDICATE, standing),),
        )
    with pytest.raises(MinimalCompleteFiberError):
        MinimalCompleteFiberVerdict(
            sufficiency=SufficiencyStanding.NO_INDEPENDENT_READER_IN_THIS_TREE,
            necessity=(
                (DeletedComponent.PREDICATE, standing),
                (DeletedComponent.PREDICATE, standing),
                (DeletedComponent.RELATION, standing),
            ),
        )


# --- `zero` و`one` ------------------------------------------------------------


def test_zero_is_an_unnamed_relation_and_not_an_empty_fiber() -> None:
    zero = FiberElement(anchor="زيد", genus="شخصٌ مُعيَّن", predicate="طويل", relation=None)
    assert zero.is_zero is True
    assert zero.is_an_empty_fiber is False
    joined = "\n".join(MINIMAL_COMPLETE_FIBER_NAMED_RESIDUALS)
    assert "ZeroIsAnUnnamedRelationNotAnEmptyFiber" in joined


def test_one_names_an_attribution_without_asserting_its_truth() -> None:
    one = AttributionCandidate(
        element=FiberElement(
            anchor="زيد",
            genus="شخصٌ مُعيَّن",
            predicate="طويل",
            relation=RelationKind.PREDICATION,
        ),
        evidence="شاهدٌ مُسمًّى في الإيداع",
        residues=("نطاقُ الإسناد لم يُحدَّد",),
    )
    assert one.asserts_the_proposition_is_true is False
    assert one.element.is_zero is False
    joined = "\n".join(MINIMAL_COMPLETE_FIBER_NAMED_RESIDUALS)
    assert "OneIsANamedAttributionNotATrueProposition" in joined


def test_an_attribution_without_a_named_relation_or_without_evidence_is_refused() -> (
    None
):
    with pytest.raises(MinimalCompleteFiberError):
        AttributionCandidate(
            element=FiberElement(
                anchor="زيد", genus="شخصٌ مُعيَّن", predicate="طويل", relation=None
            ),
            evidence="دليل",
            residues=(),
        )
    with pytest.raises(MinimalCompleteFiberError):
        AttributionCandidate(
            element=FiberElement(
                anchor="زيد",
                genus="شخصٌ مُعيَّن",
                predicate="طويل",
                relation=RelationKind.PREDICATION,
            ),
            evidence="   ",
            residues=(),
        )


# --- قائمةُ التدقيق -----------------------------------------------------------


def test_the_checklist_has_seven_conditions_and_zero_are_satisfied() -> None:
    assert THE_CLOSURE_CHECKLIST.total_count == 7
    assert THE_CLOSURE_CHECKLIST.satisfied_count == 0
    assert THE_CLOSURE_CHECKLIST.is_complete is False
    assert len(ClosureRequirement) == 7


def test_every_condition_writes_what_would_satisfy_it_and_why_it_is_open() -> None:
    for item in THE_CLOSURE_CHECKLIST.conditions:
        assert item.what_would_satisfy_it.strip()
        assert item.why_it_is_open.strip()
        assert item.is_satisfied is False


def test_a_condition_without_a_written_satisfier_or_reason_is_refused() -> None:
    with pytest.raises(MinimalCompleteFiberError):
        ChecklistCondition(
            requirement=ClosureRequirement.PREDICATE_NECESSARY,
            what_would_satisfy_it="  ",
            why_it_is_open="مفتوح",
        )
    with pytest.raises(MinimalCompleteFiberError):
        ChecklistCondition(
            requirement=ClosureRequirement.PREDICATE_NECESSARY,
            what_would_satisfy_it="شاهدان",
            why_it_is_open="  ",
        )


def test_a_checklist_that_drops_or_repeats_a_condition_is_refused() -> None:
    condition = THE_CLOSURE_CHECKLIST.conditions[0]
    with pytest.raises(MinimalCompleteFiberError):
        ClosureChecklist(conditions=(condition,))
    with pytest.raises(MinimalCompleteFiberError):
        ClosureChecklist(conditions=(condition,) * 7)
