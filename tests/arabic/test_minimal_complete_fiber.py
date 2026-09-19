"""شهودٌ على الحدّ الأدنى المكتمل: مبرهنةٌ مشروطة، وقائمةُ تدقيقٍ صفرُها مُشتَقّ."""

from __future__ import annotations

from pathlib import Path

import pytest

from alghanem.arabic import minimal_complete_fiber as mcm_module
from alghanem.arabic.fatiha_source_text import FATIHA_SOURCE_ID
from alghanem.arabic.fatiha_source_text import source_sha256 as fatiha_source_sha256
from alghanem.arabic.minimal_complete_fiber import (
    MINIMAL_COMPLETE_FIBER_NAMED_RESIDUALS,
    THE_CLOSURE_CHECKLIST,
    THE_DECLARED_DOMAIN,
    THE_DESIGNED_WITNESSES,
    AttributionCandidate,
    CaseAttestation,
    ChecklistCondition,
    ClosureChecklist,
    ClosureRequirement,
    ConditionEvidence,
    DeclaredDomain,
    DeletedComponent,
    DomainCase,
    DomainKind,
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
    deleting_representation,
    full_representation,
    genus_is_declared,
    licensed_predicates,
    lookup_reader,
    necessity_deletion_experiment,
    necessity_standing_of,
    predicate_is_licensed_for,
    registered_corpus_digests,
    run_sufficiency_experiment,
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


def test_there_are_twelve_named_residuals_all_distinct_and_non_blank() -> None:
    assert len(MINIMAL_COMPLETE_FIBER_NAMED_RESIDUALS) == 12
    assert len(set(MINIMAL_COMPLETE_FIBER_NAMED_RESIDUALS)) == 12
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
            context="مقامٌ مثبَّت",
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
            context="مقامٌ مثبَّت",
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
            context="مقامٌ مثبَّت",
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


def test_every_deletion_is_actually_run_and_merges_two_contents() -> None:
    for component in DeletedComponent:
        result = necessity_deletion_experiment(component)
        assert result.standing is SufficiencyStanding.REFUTED_ON_A_DECLARED_DOMAIN
        assert result.no_reader_can_exist is True
        assert len(result.merged_contents) == 1
        assert len(result.merged_contents[0]) == 2


def _attested_case(predicate: str, content: str) -> DomainCase:
    """حالةٌ موثَّقةٌ بمدوّنةٍ مُسجَّلةٍ في الشجرة، ببصمةٍ محسوبةٍ الآن."""

    return DomainCase(
        element=FiberElement(
            anchor="زيد",
            genus="شخصٌ مُعيَّن",
            predicate=predicate,
            relation=RelationKind.PREDICATION,
        ),
        content=content,
        context="مقامٌ مثبَّت",
        attestation=CaseAttestation(
            source_id=FATIHA_SOURCE_ID,
            source_sha256=fatiha_source_sha256(),
            locator="السطرُ الأوّل",
        ),
    )


def _attested_domain() -> DeclaredDomain:
    """مجالٌ كلُّ حالاته موثَّقة؛ فجنسُه يُشتَقّ لغويًّا مُعلَنًا لا يُكتَب."""

    return DeclaredDomain(
        identifier="مجالٌ موثَّق",
        cases=(_attested_case("طويل", "الإخبارُ بطول زيد"),),
    )


def test_a_domain_kind_is_derived_from_its_attestations_not_written() -> None:
    assert THE_DECLARED_DOMAIN.kind is DomainKind.DESIGNED_DOMAIN
    assert THE_DECLARED_DOMAIN.attested_case_count == 0
    assert _attested_domain().kind is DomainKind.DECLARED_LINGUISTIC_DOMAIN


def test_no_field_lets_a_domain_write_its_own_kind() -> None:
    with pytest.raises(TypeError):
        DeclaredDomain(  # type: ignore[call-arg]
            identifier="مجالٌ يُسمّي نفسَه",
            kind=DomainKind.DECLARED_LINGUISTIC_DOMAIN,
            cases=(_attested_case("طويل", "مضمون"),),
        )


def test_one_unattested_case_keeps_the_whole_domain_designed() -> None:
    mixed = DeclaredDomain(
        identifier="مجالٌ مختلط",
        cases=(
            _attested_case("طويل", "الإخبارُ بطول زيد"),
            DomainCase(
                element=FiberElement(
                    anchor="زيد",
                    genus="شخصٌ مُعيَّن",
                    predicate="قصير",
                    relation=RelationKind.PREDICATION,
                ),
                content="الإخبارُ بقِصَر زيد",
                context="مقامٌ مثبَّت",
            ),
        ),
    )
    assert mixed.attested_case_count == 1
    assert mixed.case_count == 2
    assert mixed.kind is DomainKind.DESIGNED_DOMAIN


def test_an_attestation_to_an_unregistered_source_is_not_verified() -> None:
    attestation = CaseAttestation(
        source_id="مدوّنةٌ ليست في هذه الشجرة",
        source_sha256=fatiha_source_sha256(),
        locator="موضع",
    )
    assert not attestation.is_verified_against_the_tree


def test_an_attestation_whose_digest_does_not_match_is_not_verified() -> None:
    attestation = CaseAttestation(
        source_id=FATIHA_SOURCE_ID,
        source_sha256="0" * 64,
        locator="موضع",
    )
    assert not attestation.is_verified_against_the_tree


def test_a_malformed_digest_is_refused_outright() -> None:
    for digest in ("", "ABC", "0" * 63, "g" * 64, fatiha_source_sha256().upper()):
        with pytest.raises(MinimalCompleteFiberError):
            CaseAttestation(
                source_id=FATIHA_SOURCE_ID, source_sha256=digest, locator="موضع"
            )


def test_an_attestation_without_a_source_or_a_locator_is_refused() -> None:
    with pytest.raises(MinimalCompleteFiberError):
        CaseAttestation(
            source_id=" ", source_sha256=fatiha_source_sha256(), locator="موضع"
        )
    with pytest.raises(MinimalCompleteFiberError):
        CaseAttestation(
            source_id=FATIHA_SOURCE_ID, source_sha256=fatiha_source_sha256(), locator=""
        )


def test_the_registered_digests_are_recomputed_from_the_tree() -> None:
    registry = registered_corpus_digests()
    assert registry[FATIHA_SOURCE_ID] == fatiha_source_sha256()
    assert all(len(digest) == 64 for digest in registry.values())


def test_the_certificate_gate_cannot_be_opened_by_naming_the_domain() -> None:
    designed = assess_minimal_complete_fiber(THE_DECLARED_DOMAIN)
    assert designed.is_established_on_its_domain is True
    assert designed.is_a_linguistic_certificate is False


def test_evidence_takes_its_kind_from_its_domain_not_from_a_written_field() -> None:
    evidence = ConditionEvidence(
        what_was_run="تجربةُ حذف",
        where_it_is_recorded="هذا الاختبار",
        domain=THE_DECLARED_DOMAIN,
    )
    assert evidence.domain_kind is THE_DECLARED_DOMAIN.kind
    with pytest.raises(TypeError):
        ConditionEvidence(  # type: ignore[call-arg]
            what_was_run="تجربةُ حذف",
            where_it_is_recorded="هذا الاختبار",
            domain_kind=DomainKind.DECLARED_LINGUISTIC_DOMAIN,
        )


def test_necessity_is_not_witnessed_on_a_domain_that_does_not_separate() -> None:
    domain = DeclaredDomain(
        identifier="مجالٌ بحالةٍ واحدة",
        cases=(
            DomainCase(
                element=FiberElement(
                    anchor="زيد",
                    genus="شخصٌ مُعيَّن",
                    predicate="طويل",
                    relation=RelationKind.PREDICATION,
                ),
                content="الإخبارُ بطول زيد",
                context="مقامٌ مثبَّت",
            ),
        ),
    )
    assert necessity_standing_of(DeletedComponent.PREDICATE, domain) is (
        NecessityStanding.NOT_WITNESSED
    )


# --- المعيارُ بشطريه ----------------------------------------------------------


def test_sufficiency_is_run_not_inferred_from_the_interface_names() -> None:
    assert assess_sufficiency() is SufficiencyStanding.HELD_ON_A_DECLARED_DOMAIN
    result = run_sufficiency_experiment(
        THE_DECLARED_DOMAIN,
        full_representation,
        lookup_reader(THE_DECLARED_DOMAIN, full_representation),
    )
    assert result.merged_contents == ()
    assert result.mismatched_contents == ()
    assert result.distinct_output_count == THE_DECLARED_DOMAIN.case_count
    joined = "\n".join(MINIMAL_COMPLETE_FIBER_NAMED_RESIDUALS)
    assert "ALookupReaderProvesInjectivityNotUnderstanding" in joined


def test_the_reader_never_receives_the_original_element() -> None:
    seen: list[object] = []

    def recording_reader(output: tuple[str | None, ...]) -> str:
        seen.append(output)
        return ""

    run_sufficiency_experiment(
        THE_DECLARED_DOMAIN, full_representation, recording_reader
    )
    assert seen
    assert all(isinstance(item, tuple) for item in seen)
    assert all(
        isinstance(part, str) or part is None
        for item in seen
        if isinstance(item, tuple)
        for part in item
    )


def test_a_merging_representation_refutes_sufficiency_before_any_reader_is_asked() -> (
    None
):
    asked = 0

    def counting_reader(output: tuple[str | None, ...]) -> str:
        nonlocal asked
        asked += 1
        return ""

    result = run_sufficiency_experiment(
        THE_DECLARED_DOMAIN,
        deleting_representation(DeletedComponent.PREDICATE),
        counting_reader,
    )
    assert result.no_reader_can_exist is True
    assert result.standing is SufficiencyStanding.REFUTED_ON_A_DECLARED_DOMAIN
    assert asked < THE_DECLARED_DOMAIN.case_count


def test_the_criterion_holds_on_its_designed_domain_and_is_no_certificate() -> None:
    verdict = assess_minimal_complete_fiber()
    assert verdict.every_component_is_witnessed is True
    assert verdict.is_established_on_its_domain is True
    assert verdict.is_a_linguistic_certificate is False
    assert verdict.domain_kind is DomainKind.DESIGNED_DOMAIN
    assert verdict.minimality_is_relative_to_the_tested_alternatives is True
    joined = "\n".join(MINIMAL_COMPLETE_FIBER_NAMED_RESIDUALS)
    assert "TheMinimumIsRelativeToTheTestedAlternatives" in joined
    assert "ADesignedDomainIsNotALinguisticCertificate" in joined


def test_a_verdict_names_its_domain_by_carrying_it_not_by_writing_it() -> None:
    standing = NecessityStanding.WITNESSED_ON_THE_DESIGNED_PAIRS
    verdict = MinimalCompleteFiberVerdict(
        domain=THE_DECLARED_DOMAIN,
        sufficiency=SufficiencyStanding.HELD_ON_A_DECLARED_DOMAIN,
        necessity=tuple((item, standing) for item in DeletedComponent),
    )
    assert verdict.domain_identifier == THE_DECLARED_DOMAIN.identifier
    assert verdict.domain_kind is THE_DECLARED_DOMAIN.kind
    with pytest.raises(TypeError):
        MinimalCompleteFiberVerdict(  # type: ignore[call-arg]
            domain_identifier="مجالٌ يُسمّي نفسَه",
            domain_kind=DomainKind.DECLARED_LINGUISTIC_DOMAIN,
            sufficiency=SufficiencyStanding.HELD_ON_A_DECLARED_DOMAIN,
            necessity=tuple((item, standing) for item in DeletedComponent),
        )


def test_a_verdict_that_drops_or_repeats_a_component_is_refused() -> None:
    standing = NecessityStanding.WITNESSED_ON_THE_DESIGNED_PAIRS
    with pytest.raises(MinimalCompleteFiberError):
        MinimalCompleteFiberVerdict(
            domain=THE_DECLARED_DOMAIN,
            sufficiency=SufficiencyStanding.HELD_ON_A_DECLARED_DOMAIN,
            necessity=((DeletedComponent.PREDICATE, standing),),
        )
    with pytest.raises(MinimalCompleteFiberError):
        MinimalCompleteFiberVerdict(
            domain=THE_DECLARED_DOMAIN,
            sufficiency=SufficiencyStanding.HELD_ON_A_DECLARED_DOMAIN,
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


def test_the_checklist_is_a_live_audit_that_counts_attempted_runs() -> None:
    assert THE_CLOSURE_CHECKLIST.is_a_live_audit is True
    assert THE_CLOSURE_CHECKLIST.attempted_count == 5
    attempted = [item for item in THE_CLOSURE_CHECKLIST.conditions if item.is_attempted]
    assert all(item.is_satisfied is False for item in attempted)
    assert all(
        item.evidence is not None
        and item.evidence.domain_kind is DomainKind.DESIGNED_DOMAIN
        for item in attempted
    )


def test_a_condition_reads_its_standing_from_the_evidence_it_carries() -> None:
    requirement = ClosureRequirement.PREDICATE_NECESSARY
    designed = ChecklistCondition(
        requirement=requirement,
        what_would_satisfy_it="شاهدان متصادمان",
        why_it_is_open="المجالُ مصمَّم",
        evidence=ConditionEvidence(
            what_was_run="تجربةُ حذف",
            where_it_is_recorded="هذا الاختبار",
            domain=THE_DECLARED_DOMAIN,
        ),
    )
    linguistic = ChecklistCondition(
        requirement=requirement,
        what_would_satisfy_it="شاهدان متصادمان",
        why_it_is_open="يبقى مكتوبًا حتّى بعد الاستيفاء",
        evidence=ConditionEvidence(
            what_was_run="تجربةُ حذف",
            where_it_is_recorded="هذا الاختبار",
            domain=_attested_domain(),
        ),
    )
    assert designed.is_attempted is True
    assert designed.is_satisfied is False
    assert linguistic.is_satisfied is True


def test_evidence_without_what_was_run_or_where_it_is_recorded_is_refused() -> None:
    with pytest.raises(MinimalCompleteFiberError):
        ConditionEvidence(
            what_was_run="  ",
            where_it_is_recorded="موضع",
            domain=THE_DECLARED_DOMAIN,
        )
    with pytest.raises(MinimalCompleteFiberError):
        ConditionEvidence(
            what_was_run="ما أُجري",
            where_it_is_recorded="  ",
            domain=THE_DECLARED_DOMAIN,
        )


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


# --- فاحصُ التوافق النوعيّ والمجالُ المُعلَن -----------------------------------


def test_the_predicate_space_licenses_a_shared_predicate_across_two_genera() -> None:
    assert predicate_is_licensed_for("عضوُ الإبصار", "غائرة") is True
    assert predicate_is_licensed_for("نبعُ الماء", "غائرة") is True
    assert predicate_is_licensed_for("نبعُ الماء", "مُبصِرة") is False
    assert "غائرة" in licensed_predicates("عضوُ الإبصار")


def test_an_undeclared_genus_is_refused_and_not_read_as_an_empty_space() -> None:
    assert genus_is_declared("جنسٌ لم يُعلَن") is False
    with pytest.raises(MinimalCompleteFiberError):
        licensed_predicates("جنسٌ لم يُعلَن")
    with pytest.raises(MinimalCompleteFiberError):
        predicate_is_licensed_for("جنسٌ لم يُعلَن", "طويل")
    joined = "\n".join(MINIMAL_COMPLETE_FIBER_NAMED_RESIDUALS)
    assert "ThePredicateSpaceIsDeclaredNotMeasured" in joined


def test_a_case_outside_the_predicate_space_or_without_a_context_is_refused() -> None:
    with pytest.raises(MinimalCompleteFiberError):
        DomainCase(
            element=FiberElement(
                anchor="عين",
                genus="نبعُ الماء",
                predicate="مُبصِرة",
                relation=RelationKind.PREDICATION,
            ),
            content="مضمون",
            context="مقامٌ مثبَّت",
        )
    with pytest.raises(MinimalCompleteFiberError):
        DomainCase(
            element=FiberElement(
                anchor="زيد",
                genus="شخصٌ مُعيَّن",
                predicate="طويل",
                relation=RelationKind.PREDICATION,
            ),
            content="مضمون",
            context="   ",
        )


def test_a_witness_whose_predicate_is_outside_its_genus_space_is_refused() -> None:
    with pytest.raises(MinimalCompleteFiberError):
        NecessityWitnessPair(
            component=DeletedComponent.CLASSIFICATION,
            first=FiberElement(
                anchor="عين",
                genus="عضوُ الإبصار",
                predicate="مُبصِرة",
                relation=RelationKind.PREDICATION,
            ),
            second=FiberElement(
                anchor="عين",
                genus="نبعُ الماء",
                predicate="مُبصِرة",
                relation=RelationKind.PREDICATION,
            ),
            first_content="الأوّل",
            second_content="الثاني",
            context="مقامٌ مثبَّت",
            scope_note="تصميم",
        )


def test_every_domain_case_carries_a_written_context() -> None:
    assert THE_DECLARED_DOMAIN.case_count == 6
    assert THE_DECLARED_DOMAIN.kind is DomainKind.DESIGNED_DOMAIN
    assert all(case.context.strip() for case in THE_DECLARED_DOMAIN.cases)


def test_an_empty_or_repeating_domain_is_refused() -> None:
    case = THE_DECLARED_DOMAIN.cases[0]
    with pytest.raises(MinimalCompleteFiberError):
        DeclaredDomain(identifier="مجالٌ خالٍ", cases=())
    with pytest.raises(MinimalCompleteFiberError):
        DeclaredDomain(
            identifier="مجالٌ مكرَّر",
            cases=(case, case),
        )
