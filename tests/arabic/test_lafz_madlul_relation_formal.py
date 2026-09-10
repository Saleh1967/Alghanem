"""البرهان الصوري الشامل على علاقة اللفظ بمدلوله، على نطاق سبعة شواهد مُثبَتة.

تُثبِّت هذه الاختبارات أربعة أمور: المجال الصوري مجمَّد وحالاته سبع بالضبط،
ودالة القرار كلّية على تلك السبع وترفض ما عداها بدل أن تحمله على أقربها،
والبرهان الشامل ينجح على العناقيد السبعة بلا استثناء، والوحدة خاملة سلطويًّا لا
تحرّك بوّابةً ولا تغيّر تدقيقًا خارجيًّا.
"""

import json
from pathlib import Path

import pytest

from alghanem.arabic.external_audit import audit_card
from alghanem.arabic.lafz_madlul_relation_formal import (
    ATTESTED_CLUSTERS,
    FROZEN_RELATION_DOMAIN,
    NOT_APPLICABLE_TEXT,
    RELATION_ADMISSIBLE_STATES,
    RELATION_FIFTH_QUESTION,
    RELATION_FIRST_QUESTION,
    RELATION_FOURTH_QUESTION,
    RELATION_SECOND_QUESTION,
    RELATION_SOURCE,
    RELATION_SUCCESS_TITLE,
    RELATION_THIRD_QUESTION,
    AttestedLexemeCluster,
    FrozenRelationDomain,
    InitialAssignmentCarrier,
    IntendedMeaning,
    LafzMadlulRelation,
    LafzMadlulRelationError,
    RelationAnswer,
    RelationCount,
    TransferFameCarrier,
    UsageIntentCarrier,
    canonical_intended_meaning,
    canonical_relation_answer,
    canonical_relation_count,
    classify_relation,
    is_fifth_question_asked,
    is_fourth_question_asked,
    is_third_question_asked,
    prove_relations_over_attested_corpus,
)

_EXAMPLES = Path(__file__).resolve().parents[2] / "examples" / "external_audit"

_CARDS = (
    "man_2_255.yaml",
    "maa_2_197.yaml",
    "imran_3_33.yaml",
    "hadhan_20_63.yaml",
)


def _cluster(relation: LafzMadlulRelation) -> AttestedLexemeCluster:
    (found,) = (
        cluster
        for cluster in ATTESTED_CLUSTERS
        if cluster.attested_relation is relation
    )
    return found


def test_the_relation_vocabulary_is_exactly_the_seven_declared_values() -> None:
    assert tuple(relation.value for relation in LafzMadlulRelation) == (
        "منفرد",
        "متباين",
        "مترادف",
        "مشترك",
        "منقول",
        "حقيقة",
        "مجاز",
    )
    assert tuple(count.value for count in RelationCount) == ("واحد", "متعدّد")
    assert tuple(answer.value for answer in RelationAnswer) == (
        "نعم",
        "لا",
        "غير_مطروح",
    )
    assert tuple(meaning.value for meaning in IntendedMeaning) == (
        "الأول",
        "الثاني",
        "غير_مطروح",
    )


def test_the_frozen_domain_states_the_five_questions_verbatim() -> None:
    assert RELATION_FIRST_QUESTION == "عدد الألفاظ في العنقود؟"
    assert RELATION_SECOND_QUESTION == "عدد المعاني المرتبطة به؟"
    assert RELATION_THIRD_QUESTION == "وُضع اللفظ لكل معنى من هذه المعاني ابتداءً؟"
    assert RELATION_FOURTH_QUESTION == (
        "هل اشتهر اللفظ في المعنى الثاني حتى هُجر الأول؟"
    )
    assert RELATION_FIFTH_QUESTION == (
        "أيّ معنى يُقصَد بإطلاق اللفظ في الاستعمال المُختبَر؟"
    )
    assert FROZEN_RELATION_DOMAIN.first_question == RELATION_FIRST_QUESTION
    assert FROZEN_RELATION_DOMAIN.fifth_question == RELATION_FIFTH_QUESTION
    assert FROZEN_RELATION_DOMAIN.source == RELATION_SOURCE
    assert "الشخصية الإسلامية" in RELATION_SOURCE


def test_the_domain_has_exactly_seven_admissible_states() -> None:
    assert FROZEN_RELATION_DOMAIN.cardinality == 7
    assert len(set(RELATION_ADMISSIBLE_STATES)) == 7
    assert (
        RelationCount.ONE,
        RelationCount.MANY,
        RelationAnswer.NO,
        RelationAnswer.NO,
        IntendedMeaning.SECOND,
    ) in set(RELATION_ADMISSIBLE_STATES)


def test_a_domain_that_changes_the_admissible_states_is_rejected() -> None:
    with pytest.raises(LafzMadlulRelationError):
        FrozenRelationDomain(
            admissible_states=RELATION_ADMISSIBLE_STATES
            + (
                (
                    RelationCount.MANY,
                    RelationCount.MANY,
                    RelationAnswer.YES,
                    RelationAnswer.NOT_ASKED,
                    IntendedMeaning.NOT_ASKED,
                ),
            )
        )


def test_each_conditional_question_is_asked_only_in_its_declared_condition() -> None:
    assert is_third_question_asked(RelationCount.ONE, RelationCount.MANY) is True
    assert is_third_question_asked(RelationCount.ONE, RelationCount.ONE) is False
    assert is_third_question_asked(RelationCount.MANY, RelationCount.MANY) is False
    assert is_fourth_question_asked(RelationAnswer.NO) is True
    assert is_fourth_question_asked(RelationAnswer.YES) is False
    assert is_fifth_question_asked(RelationAnswer.NO) is True
    assert is_fifth_question_asked(RelationAnswer.YES) is False


def test_the_decision_function_is_total_on_the_seven_admissible_states() -> None:
    assert (
        classify_relation(
            RelationCount.ONE,
            RelationCount.ONE,
            RelationAnswer.NOT_ASKED,
            RelationAnswer.NOT_ASKED,
            IntendedMeaning.NOT_ASKED,
        )
        is LafzMadlulRelation.MUNFARID
    )
    assert (
        classify_relation(
            RelationCount.MANY,
            RelationCount.MANY,
            RelationAnswer.NOT_ASKED,
            RelationAnswer.NOT_ASKED,
            IntendedMeaning.NOT_ASKED,
        )
        is LafzMadlulRelation.MUTABAYIN
    )
    assert (
        classify_relation(
            RelationCount.MANY,
            RelationCount.ONE,
            RelationAnswer.NOT_ASKED,
            RelationAnswer.NOT_ASKED,
            IntendedMeaning.NOT_ASKED,
        )
        is LafzMadlulRelation.MURADIF
    )
    assert (
        classify_relation(
            RelationCount.ONE,
            RelationCount.MANY,
            RelationAnswer.YES,
            RelationAnswer.NOT_ASKED,
            IntendedMeaning.NOT_ASKED,
        )
        is LafzMadlulRelation.MUSHTARAK
    )
    assert (
        classify_relation(
            RelationCount.ONE,
            RelationCount.MANY,
            RelationAnswer.NO,
            RelationAnswer.YES,
            IntendedMeaning.NOT_ASKED,
        )
        is LafzMadlulRelation.MANQUL
    )
    assert (
        classify_relation(
            RelationCount.ONE,
            RelationCount.MANY,
            RelationAnswer.NO,
            RelationAnswer.NO,
            IntendedMeaning.FIRST,
        )
        is LafzMadlulRelation.HAQIQA
    )
    assert (
        classify_relation(
            RelationCount.ONE,
            RelationCount.MANY,
            RelationAnswer.NO,
            RelationAnswer.NO,
            IntendedMeaning.SECOND,
        )
        is LafzMadlulRelation.MAJAZ
    )


@pytest.mark.parametrize(
    ("first", "second", "third", "fourth", "fifth"),
    (
        (
            RelationCount.MANY,
            RelationCount.MANY,
            RelationAnswer.YES,
            RelationAnswer.NOT_ASKED,
            IntendedMeaning.NOT_ASKED,
        ),
        (
            RelationCount.ONE,
            RelationCount.MANY,
            RelationAnswer.NOT_ASKED,
            RelationAnswer.NOT_ASKED,
            IntendedMeaning.NOT_ASKED,
        ),
        (
            RelationCount.ONE,
            RelationCount.MANY,
            RelationAnswer.YES,
            RelationAnswer.YES,
            IntendedMeaning.NOT_ASKED,
        ),
        (
            RelationCount.ONE,
            RelationCount.MANY,
            RelationAnswer.NO,
            RelationAnswer.YES,
            IntendedMeaning.FIRST,
        ),
        (
            RelationCount.ONE,
            RelationCount.MANY,
            RelationAnswer.NO,
            RelationAnswer.NO,
            IntendedMeaning.NOT_ASKED,
        ),
        (
            RelationCount.ONE,
            RelationCount.ONE,
            RelationAnswer.NO,
            RelationAnswer.NO,
            IntendedMeaning.FIRST,
        ),
    ),
)
def test_states_outside_the_domain_are_refused_not_approximated(
    first: RelationCount,
    second: RelationCount,
    third: RelationAnswer,
    fourth: RelationAnswer,
    fifth: IntendedMeaning,
) -> None:
    with pytest.raises(LafzMadlulRelationError):
        classify_relation(first, second, third, fourth, fifth)


def test_values_outside_the_closed_vocabularies_are_refused() -> None:
    assert canonical_relation_count("واحد") is RelationCount.ONE
    assert canonical_relation_count("متعدّد") is RelationCount.MANY
    assert canonical_relation_answer("نعم") is RelationAnswer.YES
    assert canonical_relation_answer("غير_مطروح") is RelationAnswer.NOT_ASKED
    assert canonical_intended_meaning("الأول") is IntendedMeaning.FIRST
    assert canonical_intended_meaning("الثاني") is IntendedMeaning.SECOND
    with pytest.raises(LafzMadlulRelationError):
        canonical_relation_count("ثلاثة")
    with pytest.raises(LafzMadlulRelationError):
        canonical_relation_answer("ربما")
    with pytest.raises(LafzMadlulRelationError):
        canonical_intended_meaning("   ")
    with pytest.raises(LafzMadlulRelationError):
        classify_relation(
            "واحد",  # type: ignore[arg-type]
            RelationCount.ONE,
            RelationAnswer.NOT_ASKED,
            RelationAnswer.NOT_ASKED,
            IntendedMeaning.NOT_ASKED,
        )


def test_the_exhaustive_proof_classifies_all_seven_clusters_without_exception() -> None:
    report = prove_relations_over_attested_corpus()

    assert tuple(row.lexemes for row in report.rows) == (
        ("الله",),
        ("السواد", "البياض"),
        ("الأسد", "السبع"),
        ("العين",),
        ("الصلاة",),
        ("الأسد",),
        ("الأسد",),
    )
    assert tuple(row.derived_relation for row in report.rows) == (
        LafzMadlulRelation.MUNFARID,
        LafzMadlulRelation.MUTABAYIN,
        LafzMadlulRelation.MURADIF,
        LafzMadlulRelation.MUSHTARAK,
        LafzMadlulRelation.MANQUL,
        LafzMadlulRelation.HAQIQA,
        LafzMadlulRelation.MAJAZ,
    )
    assert all(row.derived_relation is row.attested_relation for row in report.rows)
    assert report.unmatched == ()
    assert report.is_complete_success is True
    assert report.title == RELATION_SUCCESS_TITLE
    assert report.title == "شهادة صورية شاملة ناجحة على نطاق محدود"


def test_the_first_two_answers_are_derived_from_the_actual_counts() -> None:
    munfarid = _cluster(LafzMadlulRelation.MUNFARID)
    mutabayin = _cluster(LafzMadlulRelation.MUTABAYIN)
    muradif = _cluster(LafzMadlulRelation.MURADIF)

    assert munfarid.first_answer is RelationCount.ONE
    assert munfarid.second_answer is RelationCount.ONE
    assert mutabayin.first_answer is RelationCount.MANY
    assert mutabayin.second_answer is RelationCount.MANY
    assert muradif.first_answer is RelationCount.MANY
    assert muradif.second_answer is RelationCount.ONE


def test_the_cluster_identity_separates_haqiqa_from_majaz() -> None:
    haqiqa = _cluster(LafzMadlulRelation.HAQIQA)
    majaz = _cluster(LafzMadlulRelation.MAJAZ)

    assert haqiqa.lexemes == majaz.lexemes == ("الأسد",)
    assert haqiqa.cluster_key != majaz.cluster_key
    assert haqiqa.fifth_evidence == "فإن أُطلق على المعنى الموضوع له فهو الحقيقة"
    assert majaz.fifth_evidence == "وإن أُطلق على المعنى المنقول إليه فهو المجاز"


def test_the_carriers_are_load_bearing_not_decorative() -> None:
    majaz = _cluster(LafzMadlulRelation.MAJAZ)

    assert majaz.derived_relation is LafzMadlulRelation.MAJAZ

    became_manqul = AttestedLexemeCluster(
        lexemes=majaz.lexemes,
        meanings=majaz.meanings,
        tested_usage="الأسد (فرض مخالف: اشتهار المعنى الثاني)",
        first_evidence=majaz.first_evidence,
        second_evidence=majaz.second_evidence,
        third_answer=RelationAnswer.NO,
        third_evidence=majaz.third_evidence,
        fourth_answer=RelationAnswer.YES,
        fourth_evidence=majaz.fourth_evidence,
        fifth_answer=IntendedMeaning.NOT_ASKED,
        fifth_evidence=majaz.fifth_evidence,
        initial_assignment_carrier=InitialAssignmentCarrier.FOR_ONE_MEANING,
        transfer_fame_carrier=TransferFameCarrier.FAMOUS_UNTIL_FIRST_ABANDONED,
        usage_intent_carrier=UsageIntentCarrier.NOT_APPLICABLE,
        majaz_relation=NOT_APPLICABLE_TEXT,
        attested_relation=majaz.attested_relation,
        source=majaz.source,
    )
    became_haqiqa = AttestedLexemeCluster(
        lexemes=majaz.lexemes,
        meanings=majaz.meanings,
        tested_usage="الأسد (فرض مخالف: قصد المعنى الأول)",
        first_evidence=majaz.first_evidence,
        second_evidence=majaz.second_evidence,
        third_answer=majaz.third_answer,
        third_evidence=majaz.third_evidence,
        fourth_answer=majaz.fourth_answer,
        fourth_evidence=majaz.fourth_evidence,
        fifth_answer=IntendedMeaning.FIRST,
        fifth_evidence=majaz.fifth_evidence,
        initial_assignment_carrier=majaz.initial_assignment_carrier,
        transfer_fame_carrier=majaz.transfer_fame_carrier,
        usage_intent_carrier=UsageIntentCarrier.ASSIGNED_MEANING,
        majaz_relation=NOT_APPLICABLE_TEXT,
        attested_relation=majaz.attested_relation,
        source=majaz.source,
    )

    assert became_manqul.derived_relation is LafzMadlulRelation.MANQUL
    assert became_haqiqa.derived_relation is LafzMadlulRelation.HAQIQA


def test_an_answer_contradicting_its_carrier_is_refused() -> None:
    majaz = _cluster(LafzMadlulRelation.MAJAZ)
    mushtarak = _cluster(LafzMadlulRelation.MUSHTARAK)

    with pytest.raises(LafzMadlulRelationError):
        AttestedLexemeCluster(
            lexemes=mushtarak.lexemes,
            meanings=mushtarak.meanings,
            tested_usage=mushtarak.tested_usage,
            first_evidence=mushtarak.first_evidence,
            second_evidence=mushtarak.second_evidence,
            third_answer=RelationAnswer.NO,
            third_evidence=mushtarak.third_evidence,
            fourth_answer=RelationAnswer.NOT_ASKED,
            fourth_evidence=mushtarak.fourth_evidence,
            fifth_answer=IntendedMeaning.NOT_ASKED,
            fifth_evidence=mushtarak.fifth_evidence,
            initial_assignment_carrier=InitialAssignmentCarrier.FOR_EACH_MEANING,
            transfer_fame_carrier=TransferFameCarrier.NOT_APPLICABLE,
            usage_intent_carrier=UsageIntentCarrier.NOT_APPLICABLE,
            majaz_relation=NOT_APPLICABLE_TEXT,
            attested_relation=mushtarak.attested_relation,
            source=mushtarak.source,
        )
    with pytest.raises(LafzMadlulRelationError):
        AttestedLexemeCluster(
            lexemes=majaz.lexemes,
            meanings=majaz.meanings,
            tested_usage=majaz.tested_usage,
            first_evidence=majaz.first_evidence,
            second_evidence=majaz.second_evidence,
            third_answer=majaz.third_answer,
            third_evidence=majaz.third_evidence,
            fourth_answer=RelationAnswer.YES,
            fourth_evidence=majaz.fourth_evidence,
            fifth_answer=majaz.fifth_answer,
            fifth_evidence=majaz.fifth_evidence,
            initial_assignment_carrier=majaz.initial_assignment_carrier,
            transfer_fame_carrier=TransferFameCarrier.NOT_FAMOUS,
            usage_intent_carrier=majaz.usage_intent_carrier,
            majaz_relation=majaz.majaz_relation,
            attested_relation=majaz.attested_relation,
            source=majaz.source,
        )
    with pytest.raises(LafzMadlulRelationError):
        AttestedLexemeCluster(
            lexemes=majaz.lexemes,
            meanings=majaz.meanings,
            tested_usage=majaz.tested_usage,
            first_evidence=majaz.first_evidence,
            second_evidence=majaz.second_evidence,
            third_answer=majaz.third_answer,
            third_evidence=majaz.third_evidence,
            fourth_answer=majaz.fourth_answer,
            fourth_evidence=majaz.fourth_evidence,
            fifth_answer=IntendedMeaning.FIRST,
            fifth_evidence=majaz.fifth_evidence,
            initial_assignment_carrier=majaz.initial_assignment_carrier,
            transfer_fame_carrier=majaz.transfer_fame_carrier,
            usage_intent_carrier=UsageIntentCarrier.TRANSFERRED_MEANING,
            majaz_relation=majaz.majaz_relation,
            attested_relation=majaz.attested_relation,
            source=majaz.source,
        )


def test_a_single_meaning_cluster_cannot_claim_a_famous_transfer() -> None:
    munfarid = _cluster(LafzMadlulRelation.MUNFARID)

    with pytest.raises(LafzMadlulRelationError):
        AttestedLexemeCluster(
            lexemes=munfarid.lexemes,
            meanings=munfarid.meanings,
            tested_usage=munfarid.tested_usage,
            first_evidence=munfarid.first_evidence,
            second_evidence=munfarid.second_evidence,
            third_answer=RelationAnswer.NOT_ASKED,
            third_evidence=munfarid.third_evidence,
            fourth_answer=RelationAnswer.YES,
            fourth_evidence=munfarid.fourth_evidence,
            fifth_answer=IntendedMeaning.NOT_ASKED,
            fifth_evidence=munfarid.fifth_evidence,
            initial_assignment_carrier=InitialAssignmentCarrier.NOT_APPLICABLE,
            transfer_fame_carrier=TransferFameCarrier.FAMOUS_UNTIL_FIRST_ABANDONED,
            usage_intent_carrier=UsageIntentCarrier.NOT_APPLICABLE,
            majaz_relation=NOT_APPLICABLE_TEXT,
            attested_relation=munfarid.attested_relation,
            source=munfarid.source,
        )


def test_the_majaz_relation_is_declared_on_the_majaz_branch_alone() -> None:
    majaz = _cluster(LafzMadlulRelation.MAJAZ)
    haqiqa = _cluster(LafzMadlulRelation.HAQIQA)

    assert "مشابهة" in majaz.majaz_relation
    assert haqiqa.majaz_relation == NOT_APPLICABLE_TEXT

    with pytest.raises(LafzMadlulRelationError):
        AttestedLexemeCluster(
            lexemes=majaz.lexemes,
            meanings=majaz.meanings,
            tested_usage=majaz.tested_usage,
            first_evidence=majaz.first_evidence,
            second_evidence=majaz.second_evidence,
            third_answer=majaz.third_answer,
            third_evidence=majaz.third_evidence,
            fourth_answer=majaz.fourth_answer,
            fourth_evidence=majaz.fourth_evidence,
            fifth_answer=majaz.fifth_answer,
            fifth_evidence=majaz.fifth_evidence,
            initial_assignment_carrier=majaz.initial_assignment_carrier,
            transfer_fame_carrier=majaz.transfer_fame_carrier,
            usage_intent_carrier=majaz.usage_intent_carrier,
            majaz_relation=NOT_APPLICABLE_TEXT,
            attested_relation=majaz.attested_relation,
            source=majaz.source,
        )
    with pytest.raises(LafzMadlulRelationError):
        AttestedLexemeCluster(
            lexemes=haqiqa.lexemes,
            meanings=haqiqa.meanings,
            tested_usage=haqiqa.tested_usage,
            first_evidence=haqiqa.first_evidence,
            second_evidence=haqiqa.second_evidence,
            third_answer=haqiqa.third_answer,
            third_evidence=haqiqa.third_evidence,
            fourth_answer=haqiqa.fourth_answer,
            fourth_evidence=haqiqa.fourth_evidence,
            fifth_answer=haqiqa.fifth_answer,
            fifth_evidence=haqiqa.fifth_evidence,
            initial_assignment_carrier=haqiqa.initial_assignment_carrier,
            transfer_fame_carrier=haqiqa.transfer_fame_carrier,
            usage_intent_carrier=haqiqa.usage_intent_carrier,
            majaz_relation="مشابهة",
            attested_relation=haqiqa.attested_relation,
            source=haqiqa.source,
        )


def test_a_cluster_with_a_repeated_lexeme_or_meaning_is_refused() -> None:
    muradif = _cluster(LafzMadlulRelation.MURADIF)

    with pytest.raises(LafzMadlulRelationError):
        AttestedLexemeCluster(
            lexemes=("الأسد", "الأسد"),
            meanings=muradif.meanings,
            tested_usage=muradif.tested_usage,
            first_evidence=muradif.first_evidence,
            second_evidence=muradif.second_evidence,
            third_answer=muradif.third_answer,
            third_evidence=muradif.third_evidence,
            fourth_answer=muradif.fourth_answer,
            fourth_evidence=muradif.fourth_evidence,
            fifth_answer=muradif.fifth_answer,
            fifth_evidence=muradif.fifth_evidence,
            initial_assignment_carrier=muradif.initial_assignment_carrier,
            transfer_fame_carrier=muradif.transfer_fame_carrier,
            usage_intent_carrier=muradif.usage_intent_carrier,
            majaz_relation=muradif.majaz_relation,
            attested_relation=muradif.attested_relation,
            source=muradif.source,
        )
    with pytest.raises(LafzMadlulRelationError):
        AttestedLexemeCluster(
            lexemes=muradif.lexemes,
            meanings=(),
            tested_usage=muradif.tested_usage,
            first_evidence=muradif.first_evidence,
            second_evidence=muradif.second_evidence,
            third_answer=muradif.third_answer,
            third_evidence=muradif.third_evidence,
            fourth_answer=muradif.fourth_answer,
            fourth_evidence=muradif.fourth_evidence,
            fifth_answer=muradif.fifth_answer,
            fifth_evidence=muradif.fifth_evidence,
            initial_assignment_carrier=muradif.initial_assignment_carrier,
            transfer_fame_carrier=muradif.transfer_fame_carrier,
            usage_intent_carrier=muradif.usage_intent_carrier,
            majaz_relation=muradif.majaz_relation,
            attested_relation=muradif.attested_relation,
            source=muradif.source,
        )


def test_the_proof_reports_every_row_and_never_stops_at_the_first_failure() -> None:
    mushtarak = _cluster(LafzMadlulRelation.MUSHTARAK)
    misreported = AttestedLexemeCluster(
        lexemes=mushtarak.lexemes,
        meanings=mushtarak.meanings,
        tested_usage="العين (تصنيف منصوص مخالف)",
        first_evidence=mushtarak.first_evidence,
        second_evidence=mushtarak.second_evidence,
        third_answer=mushtarak.third_answer,
        third_evidence=mushtarak.third_evidence,
        fourth_answer=mushtarak.fourth_answer,
        fourth_evidence=mushtarak.fourth_evidence,
        fifth_answer=mushtarak.fifth_answer,
        fifth_evidence=mushtarak.fifth_evidence,
        initial_assignment_carrier=mushtarak.initial_assignment_carrier,
        transfer_fame_carrier=mushtarak.transfer_fame_carrier,
        usage_intent_carrier=mushtarak.usage_intent_carrier,
        majaz_relation=mushtarak.majaz_relation,
        attested_relation=LafzMadlulRelation.MANQUL,
        source=mushtarak.source,
    )

    report = prove_relations_over_attested_corpus(ATTESTED_CLUSTERS + (misreported,))

    assert len(report.rows) == len(ATTESTED_CLUSTERS) + 1
    assert report.is_complete_success is False
    assert report.title is None
    assert tuple(row.tested_usage for row in report.unmatched) == (
        misreported.tested_usage,
    )
    assert report.unmatched[0].derived_relation is LafzMadlulRelation.MUSHTARAK
    assert report.unmatched[0].attested_relation is LafzMadlulRelation.MANQUL


def test_the_proof_refuses_an_empty_corpus_and_non_attested_items() -> None:
    with pytest.raises(LafzMadlulRelationError):
        prove_relations_over_attested_corpus(())
    with pytest.raises(LafzMadlulRelationError):
        prove_relations_over_attested_corpus(("الأسد",))  # type: ignore[arg-type]


def test_the_module_reads_no_kernel_authority() -> None:
    source = (
        Path(__file__).resolve().parents[2]
        / "src"
        / "alghanem"
        / "arabic"
        / "lafz_madlul_relation_formal.py"
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

    prove_relations_over_attested_corpus()

    after = json.dumps(
        audit_card(_EXAMPLES / card).to_dict(), ensure_ascii=False, sort_keys=True
    )
    assert before == after
