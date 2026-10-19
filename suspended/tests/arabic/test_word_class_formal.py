"""البرهان الصوري الشامل على تقسيم اللفظ المفرد، على نطاق أربعة ألفاظ مُثبَتة.

تُثبِّت هذه الاختبارات أربعة أمور: المجال الصوري مجمَّد وحالاته ثلاث بالضبط،
ودالة القرار كلّية على تلك الثلاث وترفض ما عداها بدل أن تحمله على أقربها،
والبرهان الشامل ينجح على الألفاظ الأربعة بلا استثناء، والوحدة خاملة سلطويًّا
لا تحرّك بوّابةً ولا تغيّر تدقيقًا خارجيًّا.
"""

import json
from pathlib import Path

import pytest

from alghanem.arabic.external_audit import audit_card
from alghanem.arabic.word_class_formal import (
    ADMISSIBLE_STATES,
    ATTESTED_LEXEMES,
    FIRST_QUESTION,
    FROZEN_FORMAL_DOMAIN,
    SECOND_QUESTION,
    SOURCE,
    SUCCESS_TITLE,
    AttestedLexeme,
    FormalAnswer,
    FrozenFormalDomain,
    TemporalSignifierCarrier,
    WordClass,
    WordClassFormalError,
    canonical_answer,
    classify,
    is_second_question_asked,
    prove_over_attested_corpus,
)

_EXAMPLES = Path(__file__).resolve().parents[2] / "examples" / "external_audit"

_CARDS = (
    "man_2_255.yaml",
    "maa_2_197.yaml",
    "imran_3_33.yaml",
    "hadhan_20_63.yaml",
)


def test_the_class_vocabulary_is_exactly_ism_fil_harf() -> None:
    assert tuple(word_class.value for word_class in WordClass) == (
        "حرف",
        "فعل",
        "اسم",
    )
    assert tuple(answer.value for answer in FormalAnswer) == (
        "نعم",
        "لا",
        "غير_مطروح",
    )


def test_the_frozen_domain_states_the_two_questions_verbatim() -> None:
    assert FIRST_QUESTION == "هل يستقلّ اللفظ بمعناه بلا حاجة للفظ آخر؟"
    assert SECOND_QUESTION == (
        "هل يدلّ اللفظ بهيئته الصرفية (لا بذاته) على أحد الأزمنة الثلاثة؟"
    )
    assert FROZEN_FORMAL_DOMAIN.first_question == FIRST_QUESTION
    assert FROZEN_FORMAL_DOMAIN.second_question == SECOND_QUESTION
    assert FROZEN_FORMAL_DOMAIN.source == SOURCE
    assert "الشخصية الإسلامية" in SOURCE


def test_the_domain_has_exactly_three_admissible_states() -> None:
    assert FROZEN_FORMAL_DOMAIN.cardinality == 3
    assert set(ADMISSIBLE_STATES) == {
        (FormalAnswer.NO, FormalAnswer.NOT_ASKED),
        (FormalAnswer.YES, FormalAnswer.YES),
        (FormalAnswer.YES, FormalAnswer.NO),
    }


def test_a_domain_that_changes_the_admissible_states_is_rejected() -> None:
    with pytest.raises(WordClassFormalError):
        FrozenFormalDomain(
            admissible_states=(
                (FormalAnswer.NO, FormalAnswer.NOT_ASKED),
                (FormalAnswer.NO, FormalAnswer.NO),
                (FormalAnswer.YES, FormalAnswer.YES),
                (FormalAnswer.YES, FormalAnswer.NO),
            )
        )


def test_the_second_question_is_asked_only_when_the_first_answer_is_yes() -> None:
    assert is_second_question_asked(FormalAnswer.YES) is True
    assert is_second_question_asked(FormalAnswer.NO) is False


def test_the_decision_function_is_total_on_the_three_admissible_states() -> None:
    assert classify(FormalAnswer.NO, FormalAnswer.NOT_ASKED) is WordClass.HARF
    assert classify(FormalAnswer.YES, FormalAnswer.YES) is WordClass.FIL
    assert classify(FormalAnswer.YES, FormalAnswer.NO) is WordClass.ISM


@pytest.mark.parametrize(
    ("first", "second"),
    (
        (FormalAnswer.NO, FormalAnswer.YES),
        (FormalAnswer.NO, FormalAnswer.NO),
        (FormalAnswer.YES, FormalAnswer.NOT_ASKED),
        (FormalAnswer.NOT_ASKED, FormalAnswer.NOT_ASKED),
    ),
)
def test_states_outside_the_domain_are_refused_not_approximated(
    first: FormalAnswer, second: FormalAnswer
) -> None:
    with pytest.raises(WordClassFormalError):
        classify(first, second)


def test_answers_outside_the_closed_vocabulary_are_refused() -> None:
    assert canonical_answer("نعم") is FormalAnswer.YES
    assert canonical_answer("لا") is FormalAnswer.NO
    assert canonical_answer("غير_مطروح") is FormalAnswer.NOT_ASKED
    with pytest.raises(WordClassFormalError):
        canonical_answer("ربما")
    with pytest.raises(WordClassFormalError):
        canonical_answer("   ")
    with pytest.raises(WordClassFormalError):
        classify("نعم", "لا")  # type: ignore[arg-type]


def test_the_exhaustive_proof_classifies_all_four_lexemes_without_exception() -> None:
    report = prove_over_attested_corpus()

    assert tuple(row.lexeme for row in report.rows) == ("مِن", "قام", "زيد", "أمس")
    assert tuple(row.derived_class for row in report.rows) == (
        WordClass.HARF,
        WordClass.FIL,
        WordClass.ISM,
        WordClass.ISM,
    )
    assert all(row.derived_class is row.attested_class for row in report.rows)
    assert report.unmatched == ()
    assert report.is_complete_success is True
    assert report.title == SUCCESS_TITLE
    assert report.title == "أول شهادة صورية شاملة ناجحة على نطاق محدود"


def test_min_is_a_harf_because_the_second_question_is_never_asked() -> None:
    (min_lexeme,) = (item for item in ATTESTED_LEXEMES if item.lexeme == "مِن")

    assert min_lexeme.first_answer is FormalAnswer.NO
    assert min_lexeme.second_answer is FormalAnswer.NOT_ASKED
    assert min_lexeme.derived_class is WordClass.HARF
    assert "باعتبار لفظ آخر" in min_lexeme.first_evidence


def test_ams_is_an_ism_because_its_temporal_signification_is_by_essence() -> None:
    (ams,) = (item for item in ATTESTED_LEXEMES if item.lexeme == "أمس")

    assert ams.temporal_carrier is TemporalSignifierCarrier.BY_ESSENCE
    assert ams.second_answer is FormalAnswer.NO
    assert ams.derived_class is WordClass.ISM
    assert ams.second_evidence == "يدلّ عليه لكن لا بهيئته بل بذاته"

    by_form = AttestedLexeme(
        lexeme="أمس (فرض مخالف)",
        first_answer=ams.first_answer,
        first_evidence=ams.first_evidence,
        second_answer=FormalAnswer.YES,
        second_evidence=ams.second_evidence,
        temporal_carrier=TemporalSignifierCarrier.BY_FORM,
        attested_class=ams.attested_class,
        source=ams.source,
    )

    assert by_form.derived_class is WordClass.FIL


def test_the_second_answer_is_derived_from_the_carrier_not_written_freely() -> None:
    with pytest.raises(WordClassFormalError):
        AttestedLexeme(
            lexeme="أمس",
            first_answer=FormalAnswer.YES,
            first_evidence="يستقلّ بمعناه",
            second_answer=FormalAnswer.YES,
            second_evidence="يدلّ عليه لكن لا بهيئته بل بذاته",
            temporal_carrier=TemporalSignifierCarrier.BY_ESSENCE,
            attested_class=WordClass.ISM,
            source=SOURCE,
        )
    with pytest.raises(WordClassFormalError):
        AttestedLexeme(
            lexeme="مِن",
            first_answer=FormalAnswer.NO,
            first_evidence="لا يُفهَم معناه إلا باعتبار لفظ آخر",
            second_answer=FormalAnswer.NO,
            second_evidence="س٢ لا تُطرَح هنا",
            temporal_carrier=TemporalSignifierCarrier.NONE,
            attested_class=WordClass.HARF,
            source=SOURCE,
        )


def test_the_proof_reports_every_row_and_never_stops_at_the_first_failure() -> None:
    misreported = AttestedLexeme(
        lexeme="قام (تصنيف منصوص مخالف)",
        first_answer=FormalAnswer.YES,
        first_evidence="يستقلّ بمعناه",
        second_answer=FormalAnswer.YES,
        second_evidence="دلّ بهيئته على الماضي",
        temporal_carrier=TemporalSignifierCarrier.BY_FORM,
        attested_class=WordClass.ISM,
        source=SOURCE,
    )

    report = prove_over_attested_corpus(ATTESTED_LEXEMES + (misreported,))

    assert len(report.rows) == len(ATTESTED_LEXEMES) + 1
    assert report.is_complete_success is False
    assert report.title is None
    assert tuple(row.lexeme for row in report.unmatched) == (misreported.lexeme,)
    assert report.unmatched[0].derived_class is WordClass.FIL
    assert report.unmatched[0].attested_class is WordClass.ISM


def test_the_proof_refuses_an_empty_corpus_and_non_attested_items() -> None:
    with pytest.raises(WordClassFormalError):
        prove_over_attested_corpus(())
    with pytest.raises(WordClassFormalError):
        prove_over_attested_corpus(("قام",))  # type: ignore[arg-type]


def test_the_module_reads_no_kernel_authority() -> None:
    source = (
        Path(__file__).resolve().parents[2]
        / "src"
        / "alghanem"
        / "arabic"
        / "word_class_formal.py"
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

    prove_over_attested_corpus()

    after = json.dumps(
        audit_card(_EXAMPLES / card).to_dict(), ensure_ascii=False, sort_keys=True
    )
    assert before == after
