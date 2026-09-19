"""شهودٌ على الحدّ الأدنى المكتمل: مبرهنةٌ مشروطة، وقائمةُ تدقيقٍ صفرُها مُشتَقّ."""

from __future__ import annotations

from pathlib import Path
from typing import Final

import pytest

from alghanem.arabic import minimal_complete_fiber as mcm_module
from alghanem.arabic.fatiha_source_text import FATIHA_LINES, FATIHA_SOURCE_ID
from alghanem.arabic.fatiha_source_text import source_sha256 as fatiha_source_sha256
from alghanem.arabic.gloss_registry import (
    GlossEntry,
    GlossRegistry,
    SourceLocator,
    an_empty_registry,
    in_tree_gloss_registry,
    normalize,
    resolve_locator,
)
from alghanem.arabic.minimal_complete_fiber import (
    MINIMAL_COMPLETE_FIBER_NAMED_RESIDUALS,
    NO_EVIDENCE_KIND_HERE_CLOSES,
    THE_CLOSURE_CHECKLIST,
    THE_DECLARED_DOMAIN,
    THE_DESIGNED_WITNESSES,
    AttestationStanding,
    AttributionCandidate,
    CaseAttestation,
    ChecklistCondition,
    ClosureChecklist,
    ClosureRequirement,
    ConditionEvidence,
    ConditionRunKind,
    DeclaredDomain,
    DeletedComponent,
    DomainCase,
    DomainKind,
    FiberElement,
    MinimalCompleteFiberError,
    MinimalCompleteFiberVerdict,
    NecessityStanding,
    NecessityWitnessPair,
    ReaderProvenance,
    ReaderRuleOrigin,
    ReconstructionClosureStanding,
    RelationKind,
    SealedReaderRule,
    StructuralFunction,
    SufficiencyStanding,
    a_rule_sealed_before_any_case,
    a_rule_trained_on,
    a_separate_genus_field_is_required,
    assess_attestation,
    assess_minimal_complete_fiber,
    assess_reconstruction_closure,
    assess_sufficiency,
    carried_functions,
    classification_information_is_required,
    delete,
    deleting_representation,
    full_representation,
    genus_is_declared,
    hold_out_reader,
    licensed_predicates,
    lookup_reader,
    necessity_deletion_experiment,
    necessity_standing_of,
    predicate_is_licensed_for,
    reader_provenance_of,
    registered_corpus_digests,
    requirement_is_closed_by,
    run_sufficiency_experiment,
    the_deposited_gloss_registry,
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


def test_there_are_twenty_one_named_residuals_all_distinct_and_non_blank() -> None:
    assert len(MINIMAL_COMPLETE_FIBER_NAMED_RESIDUALS) == 21
    assert len(set(MINIMAL_COMPLETE_FIBER_NAMED_RESIDUALS)) == 21
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


_AN_INDEPENDENT_AUTHORITY: Final[str] = "جهةٌ واسمةٌ غيرُ مُعلِن المجال"
_A_FATIHA_ANCHOR_LINE: Final[int] = 4


def _fatiha_word_locator(line_number: int, word_number: int) -> SourceLocator:
    """محدِّدُ موضعِ كلمةٍ في سطرٍ من المُودَع، محسوبًا من نصّه لا مكتوبًا."""

    line = normalize(FATIHA_LINES[line_number - 1])
    words = line.split(" ")
    start = 0
    for word in words[: word_number - 1]:
        start += len(word) + 1
    return SourceLocator(
        line=line_number,
        start=start,
        end=start + len(words[word_number - 1]),
        word_number=word_number,
    )


def _fatiha_word(line_number: int, word_number: int) -> str:
    """سطحُ الكلمة كما يُحَلّ من المُودَع نفسِه."""

    surface = resolve_locator(
        FATIHA_SOURCE_ID, _fatiha_word_locator(line_number, word_number)
    )
    assert surface is not None
    return surface


def _attested_case(
    predicate: str,
    content: str,
    *,
    word_number: int = 1,
    locator: SourceLocator | None = None,
    anchor: str | None = None,
    source_id: str = FATIHA_SOURCE_ID,
    source_sha256: str | None = None,
) -> DomainCase:
    """حالةٌ تدّعي التوثيق؛ وكلُّ جهةٍ من جهاته تُفحَص لا تُصدَّق."""

    place = (
        _fatiha_word_locator(_A_FATIHA_ANCHOR_LINE, word_number)
        if locator is None
        else locator
    )
    return DomainCase(
        element=FiberElement(
            anchor=_fatiha_word(_A_FATIHA_ANCHOR_LINE, word_number)
            if anchor is None
            else anchor,
            genus="شخصٌ مُعيَّن",
            predicate=predicate,
            relation=RelationKind.PREDICATION,
        ),
        content=content,
        context="مقامٌ مثبَّت",
        attestation=CaseAttestation(
            source_id=source_id,
            source_sha256=(
                fatiha_source_sha256() if source_sha256 is None else source_sha256
            ),
            locator=place,
        ),
    )


def _a_gloss_registry_for(
    cases: tuple[DomainCase, ...],
    *,
    authority_id: str = _AN_INDEPENDENT_AUTHORITY,
    genus: str | None = None,
    predicate: str | None = None,
    content: str | None = None,
) -> GlossRegistry:
    """سجلُّ وسمٍ **مصنوعٌ لهذا الاختبار** ليُفحَص به سلوكُ البوّابة وحدَه.

    وهو آلةُ اختبارٍ لا إيداعُ شاهد: لا يُقرَأ دعوى تفسيرٍ لألفاظ المُودَع، ولا
    يدخل الشجرةَ سندًا لحالةٍ من حالاتها.
    """

    entries = []
    for case in cases:
        attestation = case.attestation
        assert attestation is not None
        entries.append(
            GlossEntry(
                source_id=attestation.source_id,
                locator=attestation.locator,
                genus=case.element.genus if genus is None else genus,
                predicate=case.element.predicate if predicate is None else predicate,
                content=case.content if content is None else content,
            )
        )
    return GlossRegistry(
        registry_id="سجلُّ اختبار",
        authority_id=authority_id,
        authority_note="جهةٌ مكتوبةٌ لهذا الاختبار",
        version="v1",
        payload_sha256="0" * 64,
        entries=tuple(entries),
    )


def _attested_domain(
    *, declarer_id: str = "مُعلِنُ المجال"
) -> tuple[DeclaredDomain, GlossRegistry]:
    """مجالٌ كلُّ حالاته موثَّقةٌ بوسمٍ من جهةٍ غيرِ مُعلِنه، وسجلُّ وسمه معه."""

    cases = (
        _attested_case("طويل", "الإخبارُ بطول الأوّل", word_number=1),
        _attested_case("قصير", "الإخبارُ بقِصَر الثاني", word_number=2),
    )
    domain = DeclaredDomain(
        identifier="مجالٌ موثَّق", declarer_id=declarer_id, cases=cases
    )
    return domain, _a_gloss_registry_for(cases)


def test_a_domain_kind_is_derived_from_its_attestations_not_written() -> None:
    assert THE_DECLARED_DOMAIN.kind is DomainKind.DESIGNED_DOMAIN
    assert THE_DECLARED_DOMAIN.attested_case_count == 0
    domain, registry = _attested_domain()
    assert domain.kind_against(registry) is DomainKind.DECLARED_LINGUISTIC_DOMAIN
    assert domain.attested_case_count_against(registry) == domain.case_count


def test_no_field_lets_a_domain_write_its_own_kind() -> None:
    with pytest.raises(TypeError):
        DeclaredDomain(  # type: ignore[call-arg]
            identifier="مجالٌ يُسمّي نفسَه",
            declarer_id="مُعلِن",
            kind=DomainKind.DECLARED_LINGUISTIC_DOMAIN,
            cases=(_attested_case("طويل", "مضمون"),),
        )


def test_a_domain_without_a_named_declarer_is_refused() -> None:
    with pytest.raises(MinimalCompleteFiberError):
        DeclaredDomain(
            identifier="مجالٌ بلا مُعلِن",
            declarer_id="   ",
            cases=(_attested_case("طويل", "مضمون"),),
        )


def test_one_unattested_case_leaves_the_whole_domain_undecided() -> None:
    attested = _attested_case("طويل", "الإخبارُ بطول الأوّل", word_number=1)
    mixed = DeclaredDomain(
        identifier="مجالٌ مختلط",
        declarer_id="مُعلِنُ المجال",
        cases=(
            attested,
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
    registry = _a_gloss_registry_for((attested,))
    assert mixed.attested_case_count_against(registry) == 1
    assert mixed.case_count == 2
    assert mixed.kind_against(registry) is DomainKind.UNDECIDED_DOMAIN


def test_a_case_that_offers_no_attestation_at_all_is_named_as_such() -> None:
    case = DomainCase(
        element=FiberElement(
            anchor="زيد",
            genus="شخصٌ مُعيَّن",
            predicate="طويل",
            relation=RelationKind.PREDICATION,
        ),
        content="الإخبارُ بطول زيد",
        context="مقامٌ مثبَّت",
    )
    standing = assess_attestation(case, "مُعلِنُ المجال", an_empty_registry())
    assert standing is AttestationStanding.NO_ATTESTATION_OFFERED


# --- شواهدُ خصمٍ على جهات التوثيق الثلاث ---------------------------------------


def test_a_forged_source_name_does_not_attest_a_case() -> None:
    case = _attested_case("طويل", "مضمون", source_id="مدوّنةٌ ليست في هذه الشجرة")
    registry = _a_gloss_registry_for((case,))
    assert (
        assess_attestation(case, "مُعلِنُ المجال", registry)
        is AttestationStanding.SOURCE_IS_NOT_REGISTERED
    )


def test_a_digest_that_does_not_match_the_tree_does_not_attest_a_case() -> None:
    case = _attested_case("طويل", "مضمون", source_sha256="0" * 64)
    registry = _a_gloss_registry_for((case,))
    assert (
        assess_attestation(case, "مُعلِنُ المجال", registry)
        is AttestationStanding.SOURCE_DIGEST_DOES_NOT_MATCH
    )


def test_a_locator_that_does_not_resolve_does_not_attest_a_case() -> None:
    case = _attested_case(
        "طويل", "مضمون", locator=SourceLocator(line=99, start=0, end=4)
    )
    registry = _a_gloss_registry_for((case,))
    assert (
        assess_attestation(case, "مُعلِنُ المجال", registry)
        is AttestationStanding.LOCATOR_DOES_NOT_RESOLVE
    )


def test_an_occurrence_that_does_not_match_the_anchor_does_not_attest_a_case() -> None:
    case = _attested_case("طويل", "مضمون", anchor="زيد")
    registry = _a_gloss_registry_for((case,))
    assert (
        assess_attestation(case, "مُعلِنُ المجال", registry)
        is AttestationStanding.OCCURRENCE_DOES_NOT_MATCH_THE_ANCHOR
    )
    joined = "\n".join(MINIMAL_COMPLETE_FIBER_NAMED_RESIDUALS)
    assert "AnOccurrenceIsNotAGloss" in joined


def test_an_occurrence_without_a_gloss_is_an_occurrence_not_a_reading() -> None:
    case = _attested_case("طويل", "مضمون")
    assert (
        assess_attestation(case, "مُعلِنُ المجال", an_empty_registry())
        is AttestationStanding.NO_GLOSS_AT_THIS_LOCATOR
    )


def test_a_gloss_authored_by_the_domain_declarer_is_refused() -> None:
    declarer = "مُعلِنُ المجال"
    case = _attested_case("طويل", "مضمون")
    registry = _a_gloss_registry_for((case,), authority_id=declarer)
    assert (
        assess_attestation(case, declarer, registry)
        is AttestationStanding.THE_GLOSS_IS_AUTHORED_BY_THE_DOMAIN_DECLARER
    )
    domain = DeclaredDomain(
        identifier="مجالٌ يُوثِّق نفسَه", declarer_id=declarer, cases=(case,)
    )
    assert domain.kind_against(registry) is DomainKind.UNDECIDED_DOMAIN
    joined = "\n".join(MINIMAL_COMPLETE_FIBER_NAMED_RESIDUALS)
    assert "ASelfAuthoredGlossIsRefused" in joined


def test_a_gloss_that_disagrees_with_the_case_does_not_attest_it() -> None:
    case = _attested_case("طويل", "مضمون")
    for override in (
        {"genus": "نبعُ الماء"},
        {"predicate": "قصير"},
        {"content": "غيرُه"},
    ):
        registry = _a_gloss_registry_for((case,), **override)
        assert (
            assess_attestation(case, "مُعلِنُ المجال", registry)
            is AttestationStanding.THE_GLOSS_DISAGREES_WITH_THE_CASE
        )


def test_a_gloss_at_another_place_does_not_attest_this_occurrence() -> None:
    case = _attested_case("طويل", "مضمون", word_number=1)
    elsewhere = _attested_case("طويل", "مضمون", word_number=2)
    registry = _a_gloss_registry_for((elsewhere,))
    assert (
        assess_attestation(case, "مُعلِنُ المجال", registry)
        is AttestationStanding.NO_GLOSS_AT_THIS_LOCATOR
    )


def test_a_malformed_digest_is_refused_outright() -> None:
    for digest in ("", "ABC", "0" * 63, "g" * 64, fatiha_source_sha256().upper()):
        with pytest.raises(MinimalCompleteFiberError):
            CaseAttestation(
                source_id=FATIHA_SOURCE_ID,
                source_sha256=digest,
                locator=SourceLocator(1, 0, 3),
            )


def test_an_attestation_without_a_source_or_a_resolvable_locator_is_refused() -> None:
    with pytest.raises(MinimalCompleteFiberError):
        CaseAttestation(
            source_id=" ",
            source_sha256=fatiha_source_sha256(),
            locator=SourceLocator(1, 0, 3),
        )
    with pytest.raises(MinimalCompleteFiberError):
        CaseAttestation(
            source_id=FATIHA_SOURCE_ID,
            source_sha256=fatiha_source_sha256(),
            locator="السطرُ الأوّل",  # type: ignore[arg-type]
        )


def test_the_registered_digests_are_recomputed_from_the_tree() -> None:
    registry = registered_corpus_digests()
    assert registry[FATIHA_SOURCE_ID] == fatiha_source_sha256()
    assert all(len(digest) == 64 for digest in registry.values())


def test_the_deposited_gloss_registry_is_read_from_the_tree() -> None:
    assert the_deposited_gloss_registry().payload_sha256 == (
        in_tree_gloss_registry().payload_sha256
    )


def test_the_certificate_gate_cannot_be_opened_by_naming_the_domain() -> None:
    designed = assess_minimal_complete_fiber(THE_DECLARED_DOMAIN)
    assert designed.is_established_on_its_domain is True
    assert designed.meets_the_recorded_certificate_conditions is False
    assert designed.certificate_issuance_is_delegated is True
    joined = "\n".join(MINIMAL_COMPLETE_FIBER_NAMED_RESIDUALS)
    assert "ARecordedConditionIsNotAnIssuedCertificate" in joined


def test_evidence_takes_its_kind_from_its_domain_not_from_a_written_field() -> None:
    evidence = ConditionEvidence(
        what_was_run="تجربةُ حذف",
        where_it_is_recorded="هذا الاختبار",
        domain=THE_DECLARED_DOMAIN,
        run_kind=ConditionRunKind.DELETION_OF_A_NAMED_COMPONENT,
        component=DeletedComponent.PREDICATE,
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
        declarer_id="مُعلِنُ المجال",
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
    assert verdict.meets_the_recorded_certificate_conditions is False
    assert verdict.certificate_issuance_is_delegated is True
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


def _a_deletion_evidence(component: DeletedComponent) -> ConditionEvidence:
    return ConditionEvidence(
        what_was_run="تجربةُ حذف",
        where_it_is_recorded="هذا الاختبار",
        domain=THE_DECLARED_DOMAIN,
        run_kind=ConditionRunKind.DELETION_OF_A_NAMED_COMPONENT,
        component=component,
    )


def test_a_condition_reads_the_outcome_of_its_own_run_not_the_genus_of_its_domain() -> (
    None
):
    requirement = ClosureRequirement.PREDICATE_NECESSARY
    right = _a_deletion_evidence(DeletedComponent.PREDICATE)
    assert requirement_is_closed_by(requirement, right) is True
    condition = ChecklistCondition(
        requirement=requirement,
        what_would_satisfy_it="شاهدان متصادمان",
        why_it_is_open="المجالُ مصمَّم",
        evidence=right,
    )
    assert condition.is_attempted is True
    assert condition.is_satisfied is False
    joined = "\n".join(MINIMAL_COMPLETE_FIBER_NAMED_RESIDUALS)
    assert "ADesignedDomainIsNotALinguisticCertificate" in joined


def test_a_deletion_of_another_component_does_not_close_this_requirement() -> None:
    wrong = _a_deletion_evidence(DeletedComponent.RELATION)
    assert requirement_is_closed_by(ClosureRequirement.PREDICATE_NECESSARY, wrong) is (
        False
    )


def test_a_failed_run_closes_nothing_however_its_domain_is_glossed() -> None:
    single = DeclaredDomain(
        identifier="مجالٌ لا يفصِل",
        declarer_id="مُعلِنُ المجال",
        cases=(THE_DECLARED_DOMAIN.cases[0],),
    )
    evidence = ConditionEvidence(
        what_was_run="تجربةُ حذفٍ على مجالٍ لا يفصِل",
        where_it_is_recorded="هذا الاختبار",
        domain=single,
        run_kind=ConditionRunKind.DELETION_OF_A_NAMED_COMPONENT,
        component=DeletedComponent.PREDICATE,
    )
    assert (
        evidence.outcome.standing
        is not SufficiencyStanding.REFUTED_ON_A_DECLARED_DOMAIN
    )
    assert (
        requirement_is_closed_by(ClosureRequirement.PREDICATE_NECESSARY, evidence)
        is False
    )


def test_a_lookup_reader_never_closes_the_rebuilding_requirement() -> None:
    evidence = ConditionEvidence(
        what_was_run="تجربةُ كفايةٍ بقارئ الجدول",
        where_it_is_recorded="هذا الاختبار",
        domain=THE_DECLARED_DOMAIN,
        run_kind=ConditionRunKind.SUFFICIENCY_ON_THE_FULL_REPRESENTATION,
        reader=lookup_reader(THE_DECLARED_DOMAIN, full_representation),
    )
    assert evidence.outcome.standing is SufficiencyStanding.HELD_ON_A_DECLARED_DOMAIN
    assert evidence.outcome.reader_provenance is (
        ReaderProvenance.BUILT_FROM_THE_DOMAIN_TARGET_TABLE
    )
    assert (
        requirement_is_closed_by(
            ClosureRequirement.CONTENT_REBUILT_FROM_THE_OUTPUT_ALONE, evidence
        )
        is False
    )
    joined = "\n".join(MINIMAL_COMPLETE_FIBER_NAMED_RESIDUALS)
    assert "ALookupReaderProvesInjectivityNotUnderstanding" in joined


def test_an_unprovenanced_reader_never_closes_the_rebuilding_requirement() -> None:
    table = lookup_reader(THE_DECLARED_DOMAIN, full_representation)

    def bare(output: tuple[str | None, ...]) -> str:
        return table(output)

    assert reader_provenance_of(bare) is ReaderProvenance.UNDECLARED_PROVENANCE
    evidence = ConditionEvidence(
        what_was_run="تجربةُ كفايةٍ بقارئٍ بلا سند",
        where_it_is_recorded="هذا الاختبار",
        domain=THE_DECLARED_DOMAIN,
        run_kind=ConditionRunKind.SUFFICIENCY_ON_THE_FULL_REPRESENTATION,
        reader=bare,
    )
    assert (
        requirement_is_closed_by(
            ClosureRequirement.CONTENT_REBUILT_FROM_THE_OUTPUT_ALONE, evidence
        )
        is False
    )


def _a_split_of_the_declared_domain(
    identifier: str, cases: tuple[DomainCase, ...]
) -> DeclaredDomain:
    return DeclaredDomain(
        identifier=identifier,
        declarer_id=THE_DECLARED_DOMAIN.declarer_id,
        cases=cases,
    )


def test_a_rule_trained_on_its_own_evaluation_domain_leaks_every_case() -> None:
    rule = a_rule_trained_on(
        THE_DECLARED_DOMAIN, full_representation, "جدولٌ مبنيٌّ من حالات التقييم نفسِها"
    )
    reader = hold_out_reader(rule, THE_DECLARED_DOMAIN, full_representation)
    assert reader.leaked_elements == frozenset(
        case.element for case in THE_DECLARED_DOMAIN.cases
    )
    assert reader.is_held_out is False
    assert reader.provenance is ReaderProvenance.BUILT_FROM_THE_DOMAIN_TARGET_TABLE


def test_a_rule_trained_on_a_disjoint_split_is_held_out_by_construction() -> None:
    training = _a_split_of_the_declared_domain(
        "شطرُ تدريبٍ مُسمًّى", THE_DECLARED_DOMAIN.cases[:2]
    )
    evaluation = _a_split_of_the_declared_domain(
        "شطرُ تقييمٍ منفصل", THE_DECLARED_DOMAIN.cases[2:]
    )
    reader = hold_out_reader(
        a_rule_trained_on(training, full_representation, "جدولٌ من شطر التدريب"),
        evaluation,
        full_representation,
    )
    assert reader.leaked_elements == frozenset()
    assert reader.is_held_out is True
    assert reader.provenance is ReaderProvenance.FIXED_BEFORE_THE_EVALUATION_DATA


def test_an_overlapping_split_leaks_exactly_the_shared_cases() -> None:
    training = _a_split_of_the_declared_domain(
        "شطرُ تدريبٍ يتقاطع", THE_DECLARED_DOMAIN.cases[:3]
    )
    evaluation = _a_split_of_the_declared_domain(
        "شطرُ تقييمٍ يتقاطع", THE_DECLARED_DOMAIN.cases[2:]
    )
    reader = hold_out_reader(
        a_rule_trained_on(training, full_representation, "جدولٌ متقاطع"),
        evaluation,
        full_representation,
    )
    assert reader.leaked_elements == frozenset({THE_DECLARED_DOMAIN.cases[2].element})
    assert reader.is_held_out is False


def test_a_rule_claiming_a_seal_while_disclosing_cases_is_refused() -> None:
    with pytest.raises(MinimalCompleteFiberError):
        SealedReaderRule(
            rule_note="قاعدةٌ تدّعي الختمَ وقد رأت",
            origin=ReaderRuleOrigin.SEALED_BEFORE_ANY_CASE,
            disclosed_elements=frozenset({THE_DECLARED_DOMAIN.cases[0].element}),
            disclosed_outputs=frozenset(),
            disclosed_contents=frozenset(),
            _rule=lambda output: "",
        )


def test_a_sealed_rule_without_a_written_note_is_refused() -> None:
    with pytest.raises(MinimalCompleteFiberError):
        a_rule_sealed_before_any_case(lambda output: "", "   ")


def test_a_sealed_rule_carrying_the_targets_in_its_closure_is_refused_closure() -> None:
    """تجربةٌ خصميّةٌ سالبة: القارئُ يحفظ أهدافَ التقييم، فتقوم الكفايةُ ويُمنَع الإغلاق.

    وهي تُثبِت الأمرين معًا: أنّ الآليّةَ القديمة كانت تُجيز اجتيازَ بوّابة
    الاستقلال بختمٍ يدويٍّ لا يُدقَّق، وأنّ الإغلاقَ اليومَ مرفوضٌ بعد فصل
    الاجتياز عن الاستحقاق. فالشرطُ يُرجأ مفتوحًا، ولا يُنتَقض المجالُ ولا
    يُغلَق الشرطُ بدعوى منشأ.
    """

    memorized = {
        full_representation(case.element): case.content
        for case in THE_DECLARED_DOMAIN.cases
    }

    def rule(output: tuple[str | None, ...]) -> str:
        return memorized.get(output, "")

    reader = hold_out_reader(
        a_rule_sealed_before_any_case(rule, "قاعدةٌ تحمل الأهدافَ في إغلاقها"),
        THE_DECLARED_DOMAIN,
        full_representation,
    )
    assert reader.leaked_elements == frozenset()
    assert reader.is_held_out is True
    assert reader.holdout_is_constructive is False
    assert reader_provenance_of(reader) is (
        ReaderProvenance.SEALED_BY_HAND_AND_NOT_STRUCTURALLY_AUDITABLE
    )
    evidence = ConditionEvidence(
        what_was_run="تجربةُ كفايةٍ بقارئٍ مختومٍ حافظٍ لأهدافه",
        where_it_is_recorded="هذا الاختبار",
        domain=THE_DECLARED_DOMAIN,
        run_kind=ConditionRunKind.SUFFICIENCY_ON_THE_FULL_REPRESENTATION,
        reader=reader,
    )
    assert evidence.outcome.standing is SufficiencyStanding.HELD_ON_A_DECLARED_DOMAIN
    decision = assess_reconstruction_closure(evidence)
    assert decision.sufficiency_held is True
    assert decision.constructive_holdout is False
    assert decision.verified_rule_provenance is False
    assert decision.standing is (
        ReconstructionClosureStanding.DEFERRED_FOR_WANT_OF_AN_AUDITABLE_READER
    )
    assert (
        requirement_is_closed_by(
            ClosureRequirement.CONTENT_REBUILT_FROM_THE_OUTPUT_ALONE, evidence
        )
        is False
    )
    condition = ChecklistCondition(
        requirement=ClosureRequirement.CONTENT_REBUILT_FROM_THE_OUTPUT_ALONE,
        what_would_satisfy_it="إعادةُ بناءٍ بقارئٍ مستقلّ",
        why_it_is_open="المجالُ مصمَّم، والختمُ اليدويُّ لا يُدقَّق بنيويًّا",
        evidence=evidence,
    )
    assert condition.is_satisfied is False
    joined = "\n".join(MINIMAL_COMPLETE_FIBER_NAMED_RESIDUALS)
    assert "ASealedRuleIsCheckedForOverlapNotForMemory" in joined
    assert "ReaderIndependenceIsAMechanismNotALabel" in joined


def test_an_audited_holdout_is_the_only_route_and_no_reader_here_travels_it() -> None:
    """الحجبُ البنائيُّ مُدقَّقٌ ومنشؤه مُصدَّق، ومع ذلك تُنتقَض الكفايةُ عليه.

    وهذا هو الثمنُ الحقيقيُّ للفصل: جدولٌ لم يرَ مخرجاتِ التقييم لا يملك عنها
    جوابًا، فلا يُعيد بناءَ مضمونها. فلا قارئَ في هذه الشجرة يجمع الثلاثةَ
    معًا، ويبقى شرطُ إعادة البناء مفتوحًا بلا ادّعاءِ إغلاق.
    """
    training = _a_split_of_the_declared_domain(
        "شطرُ تدريبٍ مُسمًّى", THE_DECLARED_DOMAIN.cases[:2]
    )
    evaluation = _a_split_of_the_declared_domain(
        "شطرُ تقييمٍ منفصل", THE_DECLARED_DOMAIN.cases[2:]
    )
    reader = hold_out_reader(
        a_rule_trained_on(training, full_representation, "جدولٌ من شطر التدريب"),
        evaluation,
        full_representation,
    )
    assert reader.holdout_is_constructive is True
    evidence = ConditionEvidence(
        what_was_run="تجربةُ كفايةٍ بقارئٍ مُدقَّق الحجب",
        where_it_is_recorded="هذا الاختبار",
        domain=evaluation,
        run_kind=ConditionRunKind.SUFFICIENCY_ON_THE_FULL_REPRESENTATION,
        reader=reader,
    )
    decision = assess_reconstruction_closure(evidence)
    assert decision.verified_rule_provenance is True
    assert decision.constructive_holdout is True
    assert decision.sufficiency_held is False
    assert decision.standing is ReconstructionClosureStanding.REFUTED_BY_ITS_OWN_RUN
    assert decision.closes_the_requirement is False
    condition = ChecklistCondition(
        requirement=ClosureRequirement.CONTENT_REBUILT_FROM_THE_OUTPUT_ALONE,
        what_would_satisfy_it="إعادةُ بناءٍ بقارئٍ مُدقَّق الحجب",
        why_it_is_open="لا قارئَ ههنا يجمع الكفايةَ والحجبَ البنائيَّ معًا",
        evidence=evidence,
    )
    assert condition.is_satisfied is False
    joined = "\n".join(MINIMAL_COMPLETE_FIBER_NAMED_RESIDUALS)
    assert "AnAuditedHoldoutProvesRetrievalNotALinguisticRule" in joined
    assert "AHeldReconstructionIsNotAnIndependentReader" in joined
    assert "NoReaderInThisTreeClosesTheRebuildingRequirement" in joined


def test_a_shared_target_refuses_the_holdout_though_the_cases_differ() -> None:
    """اختلافُ معرّفات الحالات وحدَه ليس دليلَ استقلال: الهدفُ نفسُه مشترك."""

    shared_content = THE_DECLARED_DOMAIN.cases[0].content
    borrowed = DomainCase(
        element=THE_DECLARED_DOMAIN.cases[4].element,
        content=shared_content,
        context=THE_DECLARED_DOMAIN.cases[4].context,
    )
    training = _a_split_of_the_declared_domain(
        "شطرُ تدريبٍ يحمل الهدف", THE_DECLARED_DOMAIN.cases[:2]
    )
    evaluation = _a_split_of_the_declared_domain("شطرُ تقييمٍ يشاركه الهدف", (borrowed,))
    reader = hold_out_reader(
        a_rule_trained_on(training, full_representation, "جدولٌ من شطر التدريب"),
        evaluation,
        full_representation,
    )
    assert reader.leaked_elements == frozenset()
    assert reader.leaked_contents == frozenset({shared_content})
    assert reader.is_held_out is False
    assert reader.holdout_is_constructive is False
    assert reader.provenance is ReaderProvenance.BUILT_FROM_THE_DOMAIN_TARGET_TABLE


def test_a_refuted_sufficiency_run_is_refuted_and_not_deferred() -> None:
    evidence = ConditionEvidence(
        what_was_run="تجربةُ كفايةٍ بقارئٍ بلا سند",
        where_it_is_recorded="هذا الاختبار",
        domain=THE_DECLARED_DOMAIN,
        run_kind=ConditionRunKind.DELETION_OF_A_NAMED_COMPONENT,
        component=DeletedComponent.PREDICATE,
    )
    decision = assess_reconstruction_closure(evidence)
    assert decision.standing is ReconstructionClosureStanding.REFUTED_BY_ITS_OWN_RUN
    assert decision.closes_the_requirement is False


def test_three_requirements_are_closed_by_no_evidence_kind_defined_here() -> None:
    evidence = _a_deletion_evidence(DeletedComponent.PREDICATE)
    for requirement in NO_EVIDENCE_KIND_HERE_CLOSES:
        assert requirement_is_closed_by(requirement, evidence) is False


def test_evidence_without_what_was_run_or_where_it_is_recorded_is_refused() -> None:
    with pytest.raises(MinimalCompleteFiberError):
        ConditionEvidence(
            what_was_run="  ",
            where_it_is_recorded="موضع",
            domain=THE_DECLARED_DOMAIN,
            run_kind=ConditionRunKind.DELETION_OF_A_NAMED_COMPONENT,
            component=DeletedComponent.PREDICATE,
        )
    with pytest.raises(MinimalCompleteFiberError):
        ConditionEvidence(
            what_was_run="ما أُجري",
            where_it_is_recorded="  ",
            domain=THE_DECLARED_DOMAIN,
            run_kind=ConditionRunKind.DELETION_OF_A_NAMED_COMPONENT,
            component=DeletedComponent.PREDICATE,
        )
    with pytest.raises(MinimalCompleteFiberError):
        ConditionEvidence(
            what_was_run="تجربةُ حذفٍ بلا مكوّن",
            where_it_is_recorded="موضع",
            domain=THE_DECLARED_DOMAIN,
            run_kind=ConditionRunKind.DELETION_OF_A_NAMED_COMPONENT,
        )
    with pytest.raises(MinimalCompleteFiberError):
        ConditionEvidence(
            what_was_run="تجربةُ كفايةٍ بلا قارئ",
            where_it_is_recorded="موضع",
            domain=THE_DECLARED_DOMAIN,
            run_kind=ConditionRunKind.SUFFICIENCY_ON_THE_FULL_REPRESENTATION,
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
        DeclaredDomain(identifier="مجالٌ خالٍ", declarer_id="مُعلِن", cases=())
    with pytest.raises(MinimalCompleteFiberError):
        DeclaredDomain(
            identifier="مجالٌ مكرَّر",
            declarer_id="مُعلِن",
            cases=(case, case),
        )
