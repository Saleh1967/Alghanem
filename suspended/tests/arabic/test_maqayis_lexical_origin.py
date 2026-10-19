"""اختباراتُ مرجع الأصل المعجميّ: شهادةٌ تُقاس، وربطٌ وصرفٌ لا يُقرآن منها."""

from __future__ import annotations

from dataclasses import replace

import pytest

from alghanem.arabic.classification_coverage_scheme import (
    COVERAGE_ITEMS,
    ClassificationCategory,
)
from alghanem.arabic.maqayis_lexical_origin import (
    DECLARED_CANDIDATE_ROOTS,
    LEXICAL_ORIGIN_REFERENCE,
    MORPHOLOGICAL_WORK_STILL_OWED,
    BindingStanding,
    CandidateRoot,
    LexicalOriginError,
    LexicalOriginReference,
    MorphologicalDebt,
    MorphologicalQuestion,
    RootAttestation,
    attested_root_types,
    render_lexical_origin,
    root_index,
    run_lexical_origin,
)
from alghanem.arabic.maqayis_root_table_deposit import FROZEN_ROOT_TABLE

_REPORT = run_lexical_origin()


def test_the_reference_is_maqayis_bound_to_the_deposited_digest() -> None:
    """مرجعُ الأصل مُبصَّمٌ ببصمة الإيداع نفسِها، لا بحقلٍ منسوخٍ بيد."""

    assert LEXICAL_ORIGIN_REFERENCE.name == "MAQAYIS"
    assert LEXICAL_ORIGIN_REFERENCE.digest == FROZEN_ROOT_TABLE.sha256_hex
    assert LEXICAL_ORIGIN_REFERENCE.what_it_settles.strip()
    assert LEXICAL_ORIGIN_REFERENCE.what_it_does_not_settle.strip()


def test_a_reference_without_a_stated_limit_is_refused() -> None:
    """من لم يكتب ما لا يحسمه مرجعُه قرأ شهادتَه فهمًا، فالحدُّ لازمٌ بنيويًّا."""

    with pytest.raises(LexicalOriginError):
        LexicalOriginReference(
            name="MAQAYIS",
            digest=FROZEN_ROOT_TABLE.sha256_hex,
            what_it_settles="وقوعُ سلسلة",
            what_it_does_not_settle="   ",
        )
    with pytest.raises(LexicalOriginError):
        LexicalOriginReference(
            name="MAQAYIS",
            digest="not-a-digest",
            what_it_settles="وقوعُ سلسلة",
            what_it_does_not_settle="لا يحسم صرفًا",
        )


def test_the_attestation_is_read_by_lookup_in_the_fingerprinted_bytes() -> None:
    """الشهادةُ مُشتَقّةٌ بالبحث في بايتاتٍ مُبصَّمة، لا مكتوبةٌ في هذه الشجرة."""

    index = root_index()
    assert index["ضلل"] == ("مضاعف",)
    assert attested_root_types("عبد") == ("ثلاثي",)
    assert attested_root_types("هدي") == ()
    assert _REPORT.row("ad_dallina").attested_types == ("مضاعف",)


def test_the_measured_attestation_figures_are_derived_by_running() -> None:
    """أربعةٌ بُحث عنها، وثلاثٌ شُهد لها، وواحدةٌ لم يُرخَّص لها أصلًا."""

    assert _REPORT.searched_total == 4
    assert _REPORT.attested_total == 3
    assert _REPORT.unattested_total == 1
    assert _REPORT.not_licensed_total == 1
    assert _REPORT.attestation_rate == 3 / 4


def test_an_unattested_root_is_shown_as_it_came_out() -> None:
    """«هدي» بالياء غيرُ مشهودة، وتُعرَض ولا تُبدَّل بعد رؤية النتيجة."""

    row = _REPORT.row("ihdina")
    assert row.candidate.root == "هدي"
    assert row.attestation is RootAttestation.NOT_ATTESTED
    assert row.attested_types == ()
    assert row.searched is True


def test_the_unattested_case_is_an_orthographic_limit_of_the_reference() -> None:
    """الشهادةُ تابعةٌ لرسم الجذر في المرجع: «هدى» مدخلٌ و«هدي» ليست."""

    assert attested_root_types("هدى") == ("ثلاثي",)
    assert attested_root_types("هدي") == ()


def test_a_word_with_no_licensed_root_is_not_counted_as_a_failed_search() -> None:
    """«الَّذِينَ» تخرج من المقسوم عليه بالتصريح لا بالإهمال."""

    row = _REPORT.row("allathina")
    assert row.candidate.licensed is False
    assert row.candidate.root is None
    assert row.attestation is RootAttestation.NOT_LICENSED_FOR_THIS_WORD
    assert row.searched is False
    assert _REPORT.searched_total == len(_REPORT.rows) - 1


def test_no_root_is_written_for_a_word_that_is_not_licensed_one() -> None:
    with pytest.raises(LexicalOriginError):
        CandidateRoot(word_key="allathina", root="ذو", licensed=False, why="جذرٌ مُنتزَع")
    with pytest.raises(LexicalOriginError):
        CandidateRoot(word_key="x", root=None, licensed=True, why="بلا سلسلة")
    with pytest.raises(LexicalOriginError):
        CandidateRoot(word_key="x", root="عبد", licensed=True, why="   ")


def test_attestation_never_establishes_that_the_word_derives_from_the_root() -> None:
    """الشهادةُ ليست ربطًا؛ ومنزلةُ الربط العليا لا تُبلَغ بالكتابة."""

    assert _REPORT.established_binding_total == 0
    for row in _REPORT.rows:
        assert row.binding is BindingStanding.NOT_ESTABLISHED_NO_MORPHOLOGY_RAN
    attested = _REPORT.row("nabudu")
    assert attested.attestation is RootAttestation.ATTESTED
    with pytest.raises(LexicalOriginError):
        replace(
            attested,
            binding=BindingStanding.ESTABLISHED_BY_A_MORPHOLOGICAL_DERIVATION,
        )


def test_the_morphological_debt_is_named_in_full_for_every_searched_word() -> None:
    """أربعةُ أسئلةٍ لكلّ كلمةٍ بُحث عن جذرها؛ ولا يُسقَط سؤالٌ بلا عملٍ يُسقطه."""

    assert set(MORPHOLOGICAL_WORK_STILL_OWED) == set(MorphologicalQuestion)
    assert len(_REPORT.debts) == _REPORT.searched_total
    assert _REPORT.owed_question_total == 4 * _REPORT.searched_total
    assert {debt.word_key for debt in _REPORT.debts} == {
        row.item.key for row in _REPORT.rows if row.searched
    }


def test_a_partial_morphological_debt_is_refused() -> None:
    with pytest.raises(LexicalOriginError):
        MorphologicalDebt(
            word_key="nabudu",
            questions=(MorphologicalQuestion.THE_PATTERN_OF_THE_WORD,),
        )
    with pytest.raises(LexicalOriginError):
        MorphologicalDebt(word_key="nabudu", questions=())


def test_the_structure_categories_are_shown_but_nothing_is_settled_by_lookup() -> None:
    """الشهادةُ لا تحسم أجامدةٌ الكلمةُ أم مصدرٌ أم مشتقّ؛ الفئاتُ تُعرَض فقط."""

    assert _REPORT.row("ad_dallina").structural_categories == (
        ClassificationCategory.MUSHTAQQ,
    )
    assert _REPORT.row("allathina").structural_categories == (
        ClassificationCategory.JAMID,
    )
    assert _REPORT.row("nabudu").structural_categories == ()


def test_a_type_cannot_be_written_without_an_attesting_entry() -> None:
    row = _REPORT.row("ihdina")
    with pytest.raises(LexicalOriginError):
        replace(row, attested_types=("ثلاثي",))
    attested = _REPORT.row("nabudu")
    with pytest.raises(LexicalOriginError):
        replace(attested, attested_types=())


def test_a_declared_root_cannot_be_attached_to_another_word() -> None:
    row = _REPORT.row("nabudu")
    other = next(item for item in COVERAGE_ITEMS if item.key == "anamta")
    with pytest.raises(LexicalOriginError):
        replace(row, item=other)


def test_a_candidate_pointing_outside_the_coverage_table_is_refused() -> None:
    stray = CandidateRoot(
        word_key="not_in_the_table", root="عبد", licensed=True, why="كلمةٌ غريبة"
    )
    with pytest.raises(LexicalOriginError):
        run_lexical_origin((stray,))


def test_an_empty_run_is_refused_rather_than_reported_as_complete() -> None:
    with pytest.raises(LexicalOriginError):
        run_lexical_origin(())


def test_every_declared_candidate_states_why_it_is_licensed_or_not() -> None:
    keys = {item.key for item in COVERAGE_ITEMS}
    for candidate in DECLARED_CANDIDATE_ROOTS:
        assert candidate.word_key in keys
        assert candidate.why.strip()


def test_the_rendered_report_keeps_the_lookup_apart_from_the_morphology() -> None:
    rendered = render_lexical_origin(_REPORT)
    assert "attestation rate: 75.0000%" in rendered
    assert "bindings established: 0/4" in rendered
    assert "morphological questions still owed: 16" in rendered
    assert "MAQAYIS" in rendered
    assert FROZEN_ROOT_TABLE.sha256_hex[:16] in rendered
