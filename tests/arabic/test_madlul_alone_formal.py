"""البرهان الصوري الشامل على تقسيم المدلول وحده، على نطاق خمسة شواهد مُثبَتة.

تُثبِّت هذه الاختبارات أربعة أمور: المجال الصوري مجمَّد وحالاته خمس بالضبط،
ودالة القرار كلّية على تلك الخمس وترفض ما عداها بدل أن تحمله على أقربها، والبرهان
الشامل ينجح على الشواهد الخمسة بلا استثناء، والوحدة خاملة سلطويًّا لا تحرّك
بوّابةً ولا تغيّر تدقيقًا خارجيًّا.
"""

import json
from pathlib import Path

import pytest

from alghanem.arabic.external_audit import audit_card
from alghanem.arabic.madlul_alone_formal import (
    ATTESTED_SIGNIFIED_WITNESSES,
    FROZEN_MADLUL_DOMAIN,
    MADLUL_ADMISSIBLE_STATES,
    MADLUL_FIFTH_SECTION_SCOPE_NOTE,
    MADLUL_FIRST_QUESTION,
    MADLUL_NOT_APPLICABLE_TEXT,
    MADLUL_SECOND_QUESTION,
    MADLUL_SOURCE,
    MADLUL_SUCCESS_TITLE,
    MADLUL_THIRD_QUESTION,
    AttestedSignifiedWitness,
    FrozenMadlulDomain,
    MadlulAloneError,
    MadlulSection,
    SignifiedAssignmentCarrier,
    SignifiedComposition,
    SignifiedKind,
    SignifiedNatureCarrier,
    SignifiedStructureCarrier,
    SignifiedUsageState,
    canonical_signified_composition,
    canonical_signified_kind,
    canonical_signified_usage_state,
    classify_madlul,
    is_second_question_asked,
    is_third_question_asked,
    prove_madlul_over_attested_corpus,
)

_EXAMPLES = Path(__file__).resolve().parents[2] / "examples" / "external_audit"

_CARDS = (
    "man_2_255.yaml",
    "maa_2_197.yaml",
    "imran_3_33.yaml",
    "hadhan_20_63.yaml",
)


def _witness(section: MadlulSection) -> AttestedSignifiedWitness:
    (found,) = (
        witness
        for witness in ATTESTED_SIGNIFIED_WITNESSES
        if witness.attested_section is section
    )
    return found


def test_the_section_vocabulary_is_exactly_the_five_declared_values() -> None:
    assert tuple(section.value for section in MadlulSection) == (
        "معنى",
        "لفظ_مفرد_مستعمَل",
        "لفظ_مفرد_مهمَل",
        "لفظ_مركّب_مستعمَل",
        "هذيان",
    )
    assert tuple(kind.value for kind in SignifiedKind) == ("معنى", "لفظ")
    assert tuple(item.value for item in SignifiedComposition) == (
        "مفرد",
        "مركّب",
        "غير_مطروح",
    )
    assert tuple(item.value for item in SignifiedUsageState) == (
        "مستعمَل",
        "مهمَل",
        "غير_مطروح",
    )


def test_the_frozen_domain_states_the_three_questions_verbatim() -> None:
    assert FROZEN_MADLUL_DOMAIN.source == MADLUL_SOURCE
    assert FROZEN_MADLUL_DOMAIN.first_question == "نوع مدلول اللفظ؟"
    assert FROZEN_MADLUL_DOMAIN.second_question == "تركيب اللفظ المدلول؟"
    assert FROZEN_MADLUL_DOMAIN.third_question == "حالة وضعه؟"
    assert "س١ = لفظ" in FROZEN_MADLUL_DOMAIN.second_question_condition
    assert "س١ = لفظ" in FROZEN_MADLUL_DOMAIN.third_question_condition


def test_the_domain_has_exactly_five_admissible_states() -> None:
    assert FROZEN_MADLUL_DOMAIN.cardinality == 5
    assert len(set(MADLUL_ADMISSIBLE_STATES)) == 5
    assert MADLUL_ADMISSIBLE_STATES == (
        (
            SignifiedKind.MEANING,
            SignifiedComposition.NOT_ASKED,
            SignifiedUsageState.NOT_ASKED,
        ),
        (
            SignifiedKind.UTTERANCE,
            SignifiedComposition.SIMPLE,
            SignifiedUsageState.USED,
        ),
        (
            SignifiedKind.UTTERANCE,
            SignifiedComposition.SIMPLE,
            SignifiedUsageState.NEGLECTED,
        ),
        (
            SignifiedKind.UTTERANCE,
            SignifiedComposition.COMPOUND,
            SignifiedUsageState.USED,
        ),
        (
            SignifiedKind.UTTERANCE,
            SignifiedComposition.COMPOUND,
            SignifiedUsageState.NEGLECTED,
        ),
    )


def test_a_domain_that_changes_the_admissible_states_is_rejected() -> None:
    with pytest.raises(MadlulAloneError):
        FrozenMadlulDomain(admissible_states=MADLUL_ADMISSIBLE_STATES[:4])
    with pytest.raises(MadlulAloneError):
        FrozenMadlulDomain(
            admissible_states=MADLUL_ADMISSIBLE_STATES
            + (
                (
                    SignifiedKind.MEANING,
                    SignifiedComposition.SIMPLE,
                    SignifiedUsageState.USED,
                ),
            )
        )
    with pytest.raises(MadlulAloneError):
        FrozenMadlulDomain(first_question="   ")


def test_each_conditional_question_is_asked_only_in_its_declared_condition() -> None:
    assert is_second_question_asked(SignifiedKind.UTTERANCE) is True
    assert is_second_question_asked(SignifiedKind.MEANING) is False
    assert is_third_question_asked(SignifiedKind.UTTERANCE) is True
    assert is_third_question_asked(SignifiedKind.MEANING) is False


def test_the_decision_function_is_total_on_the_five_admissible_states() -> None:
    assert (
        classify_madlul(
            SignifiedKind.MEANING,
            SignifiedComposition.NOT_ASKED,
            SignifiedUsageState.NOT_ASKED,
        )
        is MadlulSection.MEANING
    )
    assert (
        classify_madlul(
            SignifiedKind.UTTERANCE,
            SignifiedComposition.SIMPLE,
            SignifiedUsageState.USED,
        )
        is MadlulSection.SIMPLE_USED_UTTERANCE
    )
    assert (
        classify_madlul(
            SignifiedKind.UTTERANCE,
            SignifiedComposition.SIMPLE,
            SignifiedUsageState.NEGLECTED,
        )
        is MadlulSection.SIMPLE_NEGLECTED_UTTERANCE
    )
    assert (
        classify_madlul(
            SignifiedKind.UTTERANCE,
            SignifiedComposition.COMPOUND,
            SignifiedUsageState.USED,
        )
        is MadlulSection.COMPOUND_USED_UTTERANCE
    )
    assert (
        classify_madlul(
            SignifiedKind.UTTERANCE,
            SignifiedComposition.COMPOUND,
            SignifiedUsageState.NEGLECTED,
        )
        is MadlulSection.HADHAYAN
    )


@pytest.mark.parametrize(
    ("kind", "composition", "usage"),
    (
        (
            SignifiedKind.MEANING,
            SignifiedComposition.SIMPLE,
            SignifiedUsageState.NOT_ASKED,
        ),
        (
            SignifiedKind.MEANING,
            SignifiedComposition.NOT_ASKED,
            SignifiedUsageState.USED,
        ),
        (
            SignifiedKind.MEANING,
            SignifiedComposition.COMPOUND,
            SignifiedUsageState.NEGLECTED,
        ),
        (
            SignifiedKind.UTTERANCE,
            SignifiedComposition.NOT_ASKED,
            SignifiedUsageState.USED,
        ),
        (
            SignifiedKind.UTTERANCE,
            SignifiedComposition.SIMPLE,
            SignifiedUsageState.NOT_ASKED,
        ),
        (
            SignifiedKind.UTTERANCE,
            SignifiedComposition.NOT_ASKED,
            SignifiedUsageState.NOT_ASKED,
        ),
    ),
)
def test_states_outside_the_domain_are_refused_not_approximated(
    kind: SignifiedKind,
    composition: SignifiedComposition,
    usage: SignifiedUsageState,
) -> None:
    with pytest.raises(MadlulAloneError):
        classify_madlul(kind, composition, usage)


def test_values_outside_the_closed_vocabularies_are_refused() -> None:
    assert canonical_signified_kind("لفظ") is SignifiedKind.UTTERANCE
    assert canonical_signified_composition("مركب") is SignifiedComposition.COMPOUND
    assert canonical_signified_usage_state("مهمل") is SignifiedUsageState.NEGLECTED
    for reader in (
        canonical_signified_kind,
        canonical_signified_composition,
        canonical_signified_usage_state,
    ):
        with pytest.raises(MadlulAloneError):
            reader("قريب")
        with pytest.raises(MadlulAloneError):
            reader("   ")
    with pytest.raises(MadlulAloneError):
        classify_madlul(
            "لفظ",  # type: ignore[arg-type]
            SignifiedComposition.SIMPLE,
            SignifiedUsageState.USED,
        )


def test_the_exhaustive_proof_classifies_all_five_witnesses_without_exception() -> None:
    report = prove_madlul_over_attested_corpus()

    assert len(report.rows) == 5
    assert report.domain is FROZEN_MADLUL_DOMAIN
    assert report.source == MADLUL_SOURCE
    assert report.is_complete_success is True
    assert report.unmatched == ()
    assert report.title == MADLUL_SUCCESS_TITLE
    assert tuple(row.lexeme for row in report.rows) == (
        "الحيوان",
        "الكلمة",
        "الضاد",
        "الخبر",
        "الهذيان",
    )
    assert tuple(row.derived_section for row in report.rows) == tuple(MadlulSection)
    assert all(row.matches for row in report.rows)


def test_the_carriers_are_load_bearing_not_decorative() -> None:
    kalima = _witness(MadlulSection.SIMPLE_USED_UTTERANCE)
    flipped_usage = AttestedSignifiedWitness(
        lexeme=kalima.lexeme,
        signified_description=kalima.signified_description,
        first_answer=kalima.first_answer,
        first_evidence=kalima.first_evidence,
        second_answer=kalima.second_answer,
        second_evidence=kalima.second_evidence,
        third_answer=SignifiedUsageState.NEGLECTED,
        third_evidence=kalima.third_evidence,
        signified_nature_carrier=kalima.signified_nature_carrier,
        signified_structure_carrier=kalima.signified_structure_carrier,
        signified_assignment_carrier=(
            SignifiedAssignmentCarrier.UNASSIGNED_AND_NEGLECTED
        ),
        outside_assignment_note=MADLUL_NOT_APPLICABLE_TEXT,
        attested_section=kalima.attested_section,
        source=kalima.source,
    )
    assert flipped_usage.derived_section is MadlulSection.SIMPLE_NEGLECTED_UTTERANCE

    khabar = _witness(MadlulSection.COMPOUND_USED_UTTERANCE)
    flipped_structure = AttestedSignifiedWitness(
        lexeme=khabar.lexeme,
        signified_description=khabar.signified_description,
        first_answer=khabar.first_answer,
        first_evidence=khabar.first_evidence,
        second_answer=SignifiedComposition.SIMPLE,
        second_evidence=khabar.second_evidence,
        third_answer=khabar.third_answer,
        third_evidence=khabar.third_evidence,
        signified_nature_carrier=khabar.signified_nature_carrier,
        signified_structure_carrier=SignifiedStructureCarrier.SIMPLE_STRUCTURE,
        signified_assignment_carrier=khabar.signified_assignment_carrier,
        outside_assignment_note=MADLUL_NOT_APPLICABLE_TEXT,
        attested_section=khabar.attested_section,
        source=khabar.source,
    )
    assert flipped_structure.derived_section is MadlulSection.SIMPLE_USED_UTTERANCE


def test_an_answer_contradicting_its_carrier_is_refused() -> None:
    hayawan = _witness(MadlulSection.MEANING)
    with pytest.raises(MadlulAloneError):
        AttestedSignifiedWitness(
            lexeme=hayawan.lexeme,
            signified_description=hayawan.signified_description,
            first_answer=SignifiedKind.UTTERANCE,
            first_evidence=hayawan.first_evidence,
            second_answer=hayawan.second_answer,
            second_evidence=hayawan.second_evidence,
            third_answer=hayawan.third_answer,
            third_evidence=hayawan.third_evidence,
            signified_nature_carrier=SignifiedNatureCarrier.NOT_AN_UTTERANCE,
            signified_structure_carrier=hayawan.signified_structure_carrier,
            signified_assignment_carrier=hayawan.signified_assignment_carrier,
            outside_assignment_note=hayawan.outside_assignment_note,
            attested_section=hayawan.attested_section,
            source=hayawan.source,
        )

    kalima = _witness(MadlulSection.SIMPLE_USED_UTTERANCE)
    with pytest.raises(MadlulAloneError):
        AttestedSignifiedWitness(
            lexeme=kalima.lexeme,
            signified_description=kalima.signified_description,
            first_answer=kalima.first_answer,
            first_evidence=kalima.first_evidence,
            second_answer=SignifiedComposition.COMPOUND,
            second_evidence=kalima.second_evidence,
            third_answer=kalima.third_answer,
            third_evidence=kalima.third_evidence,
            signified_nature_carrier=kalima.signified_nature_carrier,
            signified_structure_carrier=SignifiedStructureCarrier.SIMPLE_STRUCTURE,
            signified_assignment_carrier=kalima.signified_assignment_carrier,
            outside_assignment_note=kalima.outside_assignment_note,
            attested_section=kalima.attested_section,
            source=kalima.source,
        )
    with pytest.raises(MadlulAloneError):
        AttestedSignifiedWitness(
            lexeme=kalima.lexeme,
            signified_description=kalima.signified_description,
            first_answer=kalima.first_answer,
            first_evidence=kalima.first_evidence,
            second_answer=kalima.second_answer,
            second_evidence=kalima.second_evidence,
            third_answer=SignifiedUsageState.NEGLECTED,
            third_evidence=kalima.third_evidence,
            signified_nature_carrier=kalima.signified_nature_carrier,
            signified_structure_carrier=kalima.signified_structure_carrier,
            signified_assignment_carrier=SignifiedAssignmentCarrier.ASSIGNED_AND_USED,
            outside_assignment_note=kalima.outside_assignment_note,
            attested_section=kalima.attested_section,
            source=kalima.source,
        )


def test_the_outside_assignment_note_is_declared_on_the_hadhayan_branch_alone() -> None:
    hadhayan = _witness(MadlulSection.HADHAYAN)
    assert hadhayan.outside_assignment_note == MADLUL_FIFTH_SECTION_SCOPE_NOTE
    assert "لم تضعه العرب" in hadhayan.outside_assignment_note
    assert all(
        witness.outside_assignment_note == MADLUL_NOT_APPLICABLE_TEXT
        for witness in ATTESTED_SIGNIFIED_WITNESSES
        if witness.attested_section is not MadlulSection.HADHAYAN
    )

    with pytest.raises(MadlulAloneError):
        AttestedSignifiedWitness(
            lexeme=hadhayan.lexeme,
            signified_description=hadhayan.signified_description,
            first_answer=hadhayan.first_answer,
            first_evidence=hadhayan.first_evidence,
            second_answer=hadhayan.second_answer,
            second_evidence=hadhayan.second_evidence,
            third_answer=hadhayan.third_answer,
            third_evidence=hadhayan.third_evidence,
            signified_nature_carrier=hadhayan.signified_nature_carrier,
            signified_structure_carrier=hadhayan.signified_structure_carrier,
            signified_assignment_carrier=hadhayan.signified_assignment_carrier,
            outside_assignment_note=MADLUL_NOT_APPLICABLE_TEXT,
            attested_section=hadhayan.attested_section,
            source=hadhayan.source,
        )

    khabar = _witness(MadlulSection.COMPOUND_USED_UTTERANCE)
    with pytest.raises(MadlulAloneError):
        AttestedSignifiedWitness(
            lexeme=khabar.lexeme,
            signified_description=khabar.signified_description,
            first_answer=khabar.first_answer,
            first_evidence=khabar.first_evidence,
            second_answer=khabar.second_answer,
            second_evidence=khabar.second_evidence,
            third_answer=khabar.third_answer,
            third_evidence=khabar.third_evidence,
            signified_nature_carrier=khabar.signified_nature_carrier,
            signified_structure_carrier=khabar.signified_structure_carrier,
            signified_assignment_carrier=khabar.signified_assignment_carrier,
            outside_assignment_note=MADLUL_FIFTH_SECTION_SCOPE_NOTE,
            attested_section=khabar.attested_section,
            source=khabar.source,
        )


def test_a_witness_with_blank_text_is_refused() -> None:
    kalima = _witness(MadlulSection.SIMPLE_USED_UTTERANCE)
    with pytest.raises(MadlulAloneError):
        AttestedSignifiedWitness(
            lexeme="   ",
            signified_description=kalima.signified_description,
            first_answer=kalima.first_answer,
            first_evidence=kalima.first_evidence,
            second_answer=kalima.second_answer,
            second_evidence=kalima.second_evidence,
            third_answer=kalima.third_answer,
            third_evidence=kalima.third_evidence,
            signified_nature_carrier=kalima.signified_nature_carrier,
            signified_structure_carrier=kalima.signified_structure_carrier,
            signified_assignment_carrier=kalima.signified_assignment_carrier,
            outside_assignment_note=kalima.outside_assignment_note,
            attested_section=kalima.attested_section,
            source=kalima.source,
        )


def test_the_proof_reports_every_row_and_never_stops_at_the_first_failure() -> None:
    daad = _witness(MadlulSection.SIMPLE_NEGLECTED_UTTERANCE)
    misreported = AttestedSignifiedWitness(
        lexeme=daad.lexeme,
        signified_description="حرف الهجاء نفسه، منسوبًا خطأً إلى قسمٍ آخر",
        first_answer=daad.first_answer,
        first_evidence=daad.first_evidence,
        second_answer=daad.second_answer,
        second_evidence=daad.second_evidence,
        third_answer=daad.third_answer,
        third_evidence=daad.third_evidence,
        signified_nature_carrier=daad.signified_nature_carrier,
        signified_structure_carrier=daad.signified_structure_carrier,
        signified_assignment_carrier=daad.signified_assignment_carrier,
        outside_assignment_note=daad.outside_assignment_note,
        attested_section=MadlulSection.SIMPLE_USED_UTTERANCE,
        source=daad.source,
    )

    report = prove_madlul_over_attested_corpus(
        ATTESTED_SIGNIFIED_WITNESSES + (misreported,)
    )

    assert len(report.rows) == len(ATTESTED_SIGNIFIED_WITNESSES) + 1
    assert report.is_complete_success is False
    assert report.title is None
    assert tuple(row.signified_description for row in report.unmatched) == (
        misreported.signified_description,
    )
    assert (
        report.unmatched[0].derived_section is MadlulSection.SIMPLE_NEGLECTED_UTTERANCE
    )
    assert report.unmatched[0].attested_section is MadlulSection.SIMPLE_USED_UTTERANCE


def test_the_proof_refuses_an_empty_corpus_and_non_attested_items() -> None:
    with pytest.raises(MadlulAloneError):
        prove_madlul_over_attested_corpus(())
    with pytest.raises(MadlulAloneError):
        prove_madlul_over_attested_corpus(("الضاد",))  # type: ignore[arg-type]


def test_the_module_reads_no_kernel_authority() -> None:
    source = (
        Path(__file__).resolve().parents[2]
        / "src"
        / "alghanem"
        / "arabic"
        / "madlul_alone_formal.py"
    ).read_text(encoding="utf-8")

    imports = tuple(
        line for line in source.splitlines() if line.startswith(("import ", "from "))
    )

    assert imports
    assert not any("kernel" in line for line in imports)


@pytest.mark.parametrize("card", _CARDS)
def test_the_classification_changes_no_external_audit_field(card: str) -> None:
    before = json.dumps(
        audit_card(_EXAMPLES / card).to_dict(), ensure_ascii=False, sort_keys=True
    )

    prove_madlul_over_attested_corpus()

    after = json.dumps(
        audit_card(_EXAMPLES / card).to_dict(), ensure_ascii=False, sort_keys=True
    )
    assert before == after


def test_the_first_question_text_is_the_one_the_domain_declares() -> None:
    assert MADLUL_FIRST_QUESTION == FROZEN_MADLUL_DOMAIN.first_question
    assert MADLUL_SECOND_QUESTION == FROZEN_MADLUL_DOMAIN.second_question
    assert MADLUL_THIRD_QUESTION == FROZEN_MADLUL_DOMAIN.third_question
