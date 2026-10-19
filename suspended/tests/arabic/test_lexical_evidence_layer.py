"""اختباراتُ `G0.LEX-0`: القوانينُ المُسمّاة، والسقف، والفصلُ بين المحاور."""

from __future__ import annotations

import pkgutil
from dataclasses import fields
from pathlib import Path

import pytest

import alghanem.kernel as kernel_package
from alghanem.arabic import (
    ADAPTER_ORDER,
    AXES_ARE_INDEPENDENT_IN_AUTHORITY_NOT_IN_DATA_NOTE,
    CONDITION_IS_NOT_MUJIB_NOTE,
    CORE_OUTPUT_IS_NOT_AUDIT_RECORD_NOTE,
    GENERAL_TRANSITION_LAW_SCOPE,
    LAZIM_IS_CONDITION_NOT_MUJIB_NOTE,
    NECESSARY_RELATION_IS_NOT_GENERATIVE_AUTHORITY_NOTE,
    NO_RETROACTIVE_PREREGISTRATION_OF_MAQAYIS_NOTE,
    NORMALIZATION_BRANCH_RULE_NAMES,
    PART_OF_MEANING_IS_CONDITION_NOT_GENERATIVE_AUTHORITY_NOTE,
    PROVEN_VOCABULARY_IS_NOT_PROVEN_ASSIGNMENT_NOTE,
    REFERENCE_IS_NOT_ISSUANCE_NOTE,
    RELATION_STATE_IS_NOT_GENERATION_HISTORY_NOTE,
    CandidateCore,
    CandidateGateState,
    DalalaKind,
    DerivedMorphologicalCandidate,
    HaqiqaGenus,
    IltizamCandidate,
    LafzMadlulRelation,
    LexicalAmbiguityRecord,
    LexicalAuditArtifact,
    LexicalComparativeStanding,
    LexicalCoreOutput,
    LexicalEvidenceCandidate,
    LexicalEvidenceLayerError,
    LexicalEvidenceSpecificationError,
    LexicalGenerationPath,
    LexicalMatchCandidate,
    LexicalNormalizationTrace,
    LexicalPathCandidate,
    LexicalPathError,
    LexicalTaskOutcome,
    MadlulSection,
    MorphologicalAgreement,
    MorphologicalAgreementRecord,
    MutabaqaCandidate,
    NormalizationBranch,
    ParticleRelationalEvidence,
    PrimarySignificationAnchor,
    RefusedPathEvidenceKind,
    ReportedMorphologicalEvidence,
    SignifiedKindCandidate,
    SignifiedKindError,
    SignifierAlgebraError,
    SignifierCandidate,
    SignifierSignifiedRelationCandidate,
    SignifierSignifiedRelationError,
    SurfaceOccurrence,
    TadammunCandidate,
    WordClass,
    derive_comparative_standing,
    derive_task_outcome,
    refuse_numeric_or_verdict_fields,
    refuse_path_evidence_kind,
    refuse_reported_morphology_as_generative_input,
    synthetic_occurrences,
)

_ARABIC = Path(__file__).resolve().parents[2] / "src" / "alghanem" / "arabic"

_LEX0_MODULES = (
    "lexical_evidence_specification",
    "lexical_evidence_layer",
    "signifier_algebra",
    "signified_kind",
    "signifier_signified_relation",
    "lexical_path_candidate",
    "synthetic_lexical_adapter",
)

_AXIS_MODULES = (
    "signifier_algebra",
    "signified_kind",
    "signifier_signified_relation",
)


def _source(name: str) -> str:
    return (_ARABIC / f"{name}.py").read_text(encoding="utf-8")


def _occurrence() -> SurfaceOccurrence:
    return SurfaceOccurrence(
        source_id="synthetic:test",
        occurrence_id="1",
        raw_form="كتب",
        source_position="1:1",
        local_position=0,
    )


def _exact_trace(raw_form: str = "كتب") -> LexicalNormalizationTrace:
    return LexicalNormalizationTrace(
        branch=NormalizationBranch.EXACT,
        raw_form=raw_form,
        normalized_form=raw_form,
        what_it_destroys="",
    )


def _signifier() -> SignifierCandidate:
    return SignifierCandidate(occurrence=_occurrence(), trace=_exact_trace())


def _anchor() -> PrimarySignificationAnchor:
    return PrimarySignificationAnchor(
        signifier=_signifier(),
        signified_ref="madlul:1",
        license_ref="license:1",
        evidence_refs=("evidence:1",),
    )


# ------------------------------- التخصيص ---------------------------------


def test_the_general_law_declares_three_separate_scopes() -> None:
    assert GENERAL_TRANSITION_LAW_SCOPE.constitutional_scope == "GENERAL"
    assert GENERAL_TRANSITION_LAW_SCOPE.runtime_enforcement_scope == "G0.LEX-0"
    assert GENERAL_TRANSITION_LAW_SCOPE.global_runtime_status == "NOT_YET_ESTABLISHED"
    assert "NecessaryRelationIsNotGenerativeAuthority" in (
        GENERAL_TRANSITION_LAW_SCOPE.law_names
    )


def test_the_general_law_is_declared_in_the_constitution() -> None:
    document = (
        Path(__file__).resolve().parents[2] / "docs" / "CONSTITUTION.md"
    ).read_text(encoding="utf-8")
    assert "NecessaryRelationIsNotGenerativeAuthority" in document
    assert "G0.LEX-0 necessary relation is not generative authority" in document
    assert "DECLARED_LAW_ONLY" in document


def test_the_two_condition_laws_are_literal_not_paraphrased() -> None:
    assert "LazimIsConditionNotMujib" in LAZIM_IS_CONDITION_NOT_MUJIB_NOTE
    assert "PartOfMeaningIsConditionNotGenerativeAuthority" in (
        PART_OF_MEANING_IS_CONDITION_NOT_GENERATIVE_AUTHORITY_NOTE
    )
    assert "ConditionIsNotMujib" in CONDITION_IS_NOT_MUJIB_NOTE
    assert "NecessaryRelationIsNotGenerativeAuthority" in (
        NECESSARY_RELATION_IS_NOT_GENERATIVE_AUTHORITY_NOTE
    )


def test_the_core_output_ceiling_is_fifteen_and_the_audit_record_is_outside_it() -> (
    None
):
    assert len(LexicalCoreOutput) == 15
    assert LexicalCoreOutput.PRIMARY_SIGNIFICATION_ANCHOR in LexicalCoreOutput
    assert "MorphologicalAgreementRecord" not in {
        member.value for member in LexicalCoreOutput
    }
    assert LexicalAuditArtifact.MORPHOLOGICAL_AGREEMENT_RECORD.value == (
        "MorphologicalAgreementRecord"
    )
    assert "CoreOutputIsNotAuditRecord" in CORE_OUTPUT_IS_NOT_AUDIT_RECORD_NOTE


def test_maqayis_is_never_retroactively_preregistered() -> None:
    assert "NoRetroactivePreregistrationOfMaqayis" in (
        NO_RETROACTIVE_PREREGISTRATION_OF_MAQAYIS_NOTE
    )
    for name in _LEX0_MODULES:
        assert "preregistration" not in _source(name)


def test_the_exact_branch_is_a_named_branch_with_no_rule() -> None:
    assert len(NormalizationBranch) == 3
    assert NORMALIZATION_BRANCH_RULE_NAMES[NormalizationBranch.EXACT] is None
    for branch in NormalizationBranch:
        if branch is not NormalizationBranch.EXACT:
            assert NORMALIZATION_BRANCH_RULE_NAMES[branch]


def test_a_candidate_core_is_trigger_condition_gate_and_evidence() -> None:
    core = CandidateCore(
        occurrence_ref="s#1",
        primary_signification_ref="anchor:1",
        trigger_ref="s#1",
        condition_evidence_ref="condition:1",
        gate_state=CandidateGateState.ADMITTED_AS_CANDIDATE,
        evidence_refs=("evidence:1",),
    )
    assert core.gate_state is CandidateGateState.ADMITTED_AS_CANDIDATE
    with pytest.raises(LexicalEvidenceSpecificationError):
        CandidateCore(
            occurrence_ref="s#1",
            primary_signification_ref="anchor:1",
            trigger_ref="s#2",
            condition_evidence_ref="condition:1",
            gate_state=CandidateGateState.ADMITTED_AS_CANDIDATE,
            evidence_refs=("evidence:1",),
        )
    with pytest.raises(LexicalEvidenceSpecificationError):
        CandidateCore(
            occurrence_ref="s#1",
            primary_signification_ref="anchor:1",
            trigger_ref="s#1",
            condition_evidence_ref="s#1",
            gate_state=CandidateGateState.ADMITTED_AS_CANDIDATE,
            evidence_refs=("evidence:1",),
        )


def test_no_lex0_type_carries_a_score_or_a_verdict_field() -> None:
    for candidate_type in (
        SurfaceOccurrence,
        SignifierCandidate,
        LexicalMatchCandidate,
        LexicalEvidenceCandidate,
        PrimarySignificationAnchor,
        LexicalPathCandidate,
        SignifiedKindCandidate,
        SignifierSignifiedRelationCandidate,
    ):
        refuse_numeric_or_verdict_fields(candidate_type)
    assert "ReferenceIsNotIssuance" in REFERENCE_IS_NOT_ISSUANCE_NOTE


# -------------------------------- الطبقة ---------------------------------


def test_the_raw_form_is_preserved_under_every_branch() -> None:
    trace = LexicalNormalizationTrace(
        branch=NormalizationBranch.NORMALIZE_TO_ALIF,
        raw_form="أمر",
        normalized_form="امر",
        what_it_destroys="تمييزُ الهمزة عن الألف",
    )
    signifier = SignifierCandidate(
        occurrence=SurfaceOccurrence(
            source_id="s",
            occurrence_id="1",
            raw_form="أمر",
            source_position="1:1",
            local_position=0,
        ),
        trace=trace,
    )
    assert signifier.exact_form == "أمر"
    assert signifier.normalized_form == "امر"
    assert trace.preserves_exact_form is True


def test_a_trace_that_does_not_start_from_its_own_occurrence_is_refused() -> None:
    with pytest.raises(LexicalEvidenceLayerError):
        SignifierCandidate(occurrence=_occurrence(), trace=_exact_trace("امر"))


def test_reported_morphology_never_enters_a_generator() -> None:
    reported = ReportedMorphologicalEvidence(
        reporting_source="external:1",
        reported_root="ك ت ب",
        source_trace="row 1",
    )
    assert reported.is_generative_input is False
    assert "is_generative_input" not in {
        field.name for field in fields(ReportedMorphologicalEvidence)
    }
    with pytest.raises(LexicalEvidenceLayerError):
        refuse_reported_morphology_as_generative_input(reported)


def test_the_agreement_record_prefers_neither_side() -> None:
    derived = DerivedMorphologicalCandidate(
        signifier=_signifier(), proposed_root="كتب", derivation_basis="حذفُ الزوائد"
    )
    reported = ReportedMorphologicalEvidence(
        reporting_source="external:1", reported_root="كتب", source_trace="row 1"
    )
    assert (
        MorphologicalAgreementRecord(derived=derived, reported=reported).agreement
        is MorphologicalAgreement.AGREE
    )
    assert (
        MorphologicalAgreementRecord(derived=derived, reported=None).agreement
        is MorphologicalAgreement.ONLY_DERIVED
    )
    assert (
        MorphologicalAgreementRecord(derived=None, reported=None).agreement
        is MorphologicalAgreement.NEITHER
    )
    names = {member.name for member in MorphologicalAgreement}
    assert not any(
        token in name for name in names for token in ("PREFER", "WIN", "CORRECT")
    )


def test_a_match_is_not_a_meaning() -> None:
    match = LexicalMatchCandidate(
        signifier=_signifier(),
        lexicon_id="maqayis",
        matched_entry_ref="root:كتب",
        indexing_unit="root",
    )
    evidence = LexicalEvidenceCandidate(
        match=match, evidence_ref="entry:1", source_trace="row 1"
    )
    assert evidence.is_a_meaning is False
    assert "AMatchIsNotAMeaning" in evidence.refusal_note


def test_ambiguity_is_recorded_and_never_resolved() -> None:
    record = LexicalAmbiguityRecord(occurrence_ref="s#1", candidate_refs=("a", "b"))
    assert "AmbiguityIsRecordedNotResolved" in record.resolution_note
    assert not any(
        "resolv" in field.name or "winner" in field.name
        for field in fields(LexicalAmbiguityRecord)
    )
    with pytest.raises(LexicalEvidenceLayerError):
        LexicalAmbiguityRecord(occurrence_ref="s#1", candidate_refs=("a",))


def test_task_outcome_is_independent_of_comparative_standing() -> None:
    assert (
        derive_task_outcome(reached_evidence=True, anchor_resolved=True)
        is LexicalTaskOutcome.MATCHED
    )
    assert (
        derive_comparative_standing(
            lexicon_indexing_unit="root",
            comparator_indexing_unit="root",
            lexical_reached=True,
            comparator_reached=True,
        )
        is LexicalComparativeStanding.BOTH_SUCCEED
    )


def test_differing_indexing_units_are_not_comparable_and_not_a_failure() -> None:
    standing = derive_comparative_standing(
        lexicon_indexing_unit="root",
        comparator_indexing_unit="surface",
        lexical_reached=True,
        comparator_reached=False,
    )
    assert standing is LexicalComparativeStanding.NOT_COMPARABLE
    assert standing is not LexicalComparativeStanding.BOTH_FAIL
    assert "NotComparableIsNotFailure" in standing.refusal_note


# -------------------------- المحاورُ الثلاثة ------------------------------


def test_each_axis_carries_its_own_proven_vocabulary_without_rewriting_it() -> None:
    anchor = _anchor()
    assert (
        MutabaqaCandidate(anchor=anchor, evidence_ref="e").proposed_kind
        is DalalaKind.مطابقة
    )
    assert (
        TadammunCandidate(
            anchor=anchor, claimed_part="جزء", evidence_ref="e"
        ).proposed_kind
        is DalalaKind.تضمن
    )
    assert (
        IltizamCandidate(
            anchor=anchor, claimed_lazim="لازم", evidence_ref="e"
        ).proposed_kind
        is DalalaKind.التزام
    )
    for name in _AXIS_MODULES:
        source = _source(name)
        assert "class DalalaKind" not in source
        assert "class MadlulSection" not in source
        assert "class LafzMadlulRelation" not in source


def test_carrying_a_proven_member_is_not_a_proven_assignment() -> None:
    candidate = SignifiedKindCandidate(
        anchor=_anchor(), section=MadlulSection.MEANING, evidence_ref="e"
    )
    assert candidate.is_proven_assignment is False
    assert "ProvenVocabularyIsNotProvenAssignment" in (
        PROVEN_VOCABULARY_IS_NOT_PROVEN_ASSIGNMENT_NOTE
    )


def test_a_condition_never_generates_a_candidate() -> None:
    with pytest.raises(SignifierAlgebraError) as tadammun_error:
        TadammunCandidate(anchor=None, claimed_part="جزء", evidence_ref="e")  # type: ignore[arg-type]
    assert "PartOfMeaningIsConditionNotGenerativeAuthority" in str(tadammun_error.value)
    with pytest.raises(SignifierAlgebraError) as iltizam_error:
        IltizamCandidate(anchor=None, claimed_lazim="لازم", evidence_ref="e")  # type: ignore[arg-type]
    assert "LazimIsConditionNotMujib" in str(iltizam_error.value)


def test_the_signified_section_is_never_defaulted_to_meaning() -> None:
    with pytest.raises(SignifiedKindError):
        SignifiedKindCandidate(anchor=_anchor(), section=None, evidence_ref="e")  # type: ignore[arg-type]


def test_majaz_requires_a_licensed_relation_and_haqiqa_names_its_genus() -> None:
    anchor = _anchor()
    with pytest.raises(SignifierSignifiedRelationError) as majaz_error:
        SignifierSignifiedRelationCandidate(
            anchor=anchor, relation=LafzMadlulRelation.MAJAZ, evidence_ref="e"
        )
    assert "MajazRequiresLicensedRelation" in str(majaz_error.value)
    with pytest.raises(SignifierSignifiedRelationError) as haqiqa_error:
        SignifierSignifiedRelationCandidate(
            anchor=anchor, relation=LafzMadlulRelation.HAQIQA, evidence_ref="e"
        )
    assert "OriginalHaqiqahIsNotUrfiHaqiqah" in str(haqiqa_error.value)
    licensed = SignifierSignifiedRelationCandidate(
        anchor=anchor,
        relation=LafzMadlulRelation.HAQIQA,
        evidence_ref="e",
        haqiqa_genus=HaqiqaGenus.LUGHAWIYYA,
    )
    assert licensed.is_generation_history is False


def test_particle_evidence_is_relational_not_independent() -> None:
    particle = ParticleRelationalEvidence(
        anchor=_anchor(), attached_to_ref="s#2", evidence_ref="e"
    )
    assert particle.word_class is WordClass.HARF
    assert particle.is_independent_lexical_meaning is False
    with pytest.raises(SignifierSignifiedRelationError) as error:
        ParticleRelationalEvidence(
            anchor=_anchor(), attached_to_ref="  ", evidence_ref="e"
        )
    assert "ParticleEvidenceIsRelational" in str(error.value)


def test_the_axes_are_independent_in_authority_and_share_only_the_anchor() -> None:
    assert "AxesAreIndependentInAuthorityNotInData" in (
        AXES_ARE_INDEPENDENT_IN_AUTHORITY_NOT_IN_DATA_NOTE
    )
    for name in _AXIS_MODULES:
        source = _source(name)
        for other in _AXIS_MODULES:
            if other != name:
                assert f"from .{other} import" not in source
                assert f"import {other}" not in source


# ------------------------------ طريقُ التوليد ------------------------------


def test_the_path_vocabulary_shares_no_name_with_the_relation_vocabulary() -> None:
    path_names = {member.name for member in LexicalGenerationPath}
    relation_names = {member.name for member in LafzMadlulRelation}
    assert path_names.isdisjoint(relation_names)
    assert "RelationStateIsNotGenerationHistory" in (
        RELATION_STATE_IS_NOT_GENERATION_HISTORY_NOTE
    )


def test_every_refused_path_evidence_kind_raises_with_its_own_law() -> None:
    expected = {
        RefusedPathEvidenceKind.DERIVATION_PATTERN: (
            "DerivationPatternIsNotDerivationHistory"
        ),
        RefusedPathEvidenceKind.FOREIGN_LOOK: "ForeignLookIsNotTarib",
        RefusedPathEvidenceKind.SEMANTIC_SHIFT: "SemanticShiftIsNotNaql",
        RefusedPathEvidenceKind.FREQUENCY: "FrequencyIsNotWadh",
    }
    assert set(expected) == set(RefusedPathEvidenceKind)
    for kind, law in expected.items():
        with pytest.raises(LexicalPathError) as error:
            refuse_path_evidence_kind(kind)
        assert law in str(error.value)


def test_a_claimed_path_needs_a_named_transmitter_and_residual_does_not() -> None:
    residual = LexicalPathCandidate(
        signifier_ref="s#1",
        path=LexicalGenerationPath.RESIDUAL,
        reported_by=None,
        source_trace="none",
    )
    assert residual.authorizes_derived_meaning is False
    assert "DerivedFormDoesNotAuthorizeDerivedMeaning" in residual.meaning_note
    with pytest.raises(LexicalPathError):
        LexicalPathCandidate(
            signifier_ref="s#1",
            path=LexicalGenerationPath.TARIB,
            reported_by=None,
            source_trace="row 1",
        )


# ------------------------------- المحوّلات --------------------------------


def test_the_core_reads_no_corpus_and_the_adapter_order_is_declared() -> None:
    assert ADAPTER_ORDER == ("SyntheticAdapter", "MASAQAdapter", "QuranAdapter")
    core_modules = tuple(
        name for name in _LEX0_MODULES if name != "synthetic_lexical_adapter"
    )
    for name in core_modules:
        source = _source(name)
        assert "corpora" not in source
        assert "read_text" not in source
        for line in source.splitlines():
            if line.startswith(("import ", "from ")):
                assert "masaq" not in line.lower()
                assert "quran" not in line.lower()


def test_the_synthetic_adapter_builds_four_hand_checked_cases() -> None:
    occurrences = synthetic_occurrences()
    assert len(occurrences) == 4
    assert len({occurrence.occurrence_id for occurrence in occurrences}) == 4
    assert all(
        occurrence.source_id.startswith("synthetic:") for occurrence in occurrences
    )


# --------------------------- حدودُ السلطة ---------------------------------


def test_no_lex0_module_imports_kernel_authority() -> None:
    for name in _LEX0_MODULES:
        imports = tuple(
            line
            for line in _source(name).splitlines()
            if line.startswith(("import ", "from "))
        )
        assert imports
        assert not any("kernel" in line for line in imports), name


def test_no_kernel_module_reads_this_registration() -> None:
    watched = (
        *_LEX0_MODULES,
        "PrimarySignificationAnchor",
        "LexicalEvidenceCandidate",
        "LexicalGenerationPath",
    )
    for module in pkgutil.walk_packages(
        kernel_package.__path__, prefix="alghanem.kernel."
    ):
        spec = module.module_finder.find_spec(module.name)  # type: ignore[union-attr]
        assert spec is not None and spec.origin is not None
        text = Path(spec.origin).read_text(encoding="utf-8")
        for name in watched:
            assert name not in text, (module.name, name)


def test_every_lex0_module_declares_it_is_a_registration_not_an_authority() -> None:
    for name in _LEX0_MODULES:
        assert "تسجيلٌ لا سلطة" in _source(name)
