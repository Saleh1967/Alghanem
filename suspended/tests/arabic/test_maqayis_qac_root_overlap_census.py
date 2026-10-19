"""اختباراتُ تقاطع جذور «مقاييس» بجذور مدوَّنة القرآن، وتجميدِه قبل التشغيل.

**جانبُ «مقاييس» يُقاس هنا فعلًا**: بايتاتُه في الشجرة مُبصَّمة. **وجانبُ
المدوَّنة موقوفٌ على حائز بايتاتها**: رخصتُها ورخصةُ نصّها تمنعان نسخَها،
فاختباراتُه تُتخطّى **مُصرَّحًا بالتخطّي** إن لم يُصرَّح بمسارها في
`ALGHANEM_QAC_MORPHOLOGY_PATH`؛ وصمتٌ يُقرأ نجاحًا أسوأُ من تخطٍّ مكتوب.

وجذورُ المدوَّنة المكتوبةُ هنا **مُصطنَعةٌ مُصرَّحٌ بجنسها**، لا مقتطعةٌ من
بايتاتها؛ وبنيتُها وحدَها هي المُحاكاة.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from alghanem.arabic.maqayis_qac_root_overlap_census import (
    OVERLAP_CENSUS_NAMED_RESIDUALS,
    AlphabetReadout,
    OverlapCensusError,
    OverlapReadout,
    maqayis_roots,
    maqayis_trilateral_roots,
    overlap_readouts,
    qac_root_alphabet,
    qac_roots,
    readout_at,
    stage_fusions,
)
from alghanem.arabic.maqayis_qac_root_overlap_preregistration import (
    ARRIVING_OVERLAP_FIGURES,
    HAMZA_DIAGNOSIS_HYPOTHESES,
    OVERLAP_PREREGISTRATION_DIGEST,
    OVERLAP_STAGES,
    STANDING,
    UNANSWERED_COUNTING_DECISIONS,
    FigureStanding,
    OverlapCountingRule,
    OverlapPreregistrationError,
    OverlapStage,
    RegistrationStanding,
    figure_by_label,
    preregistration_digest,
    stage_by_name,
)
from alghanem.arabic.root_orthography_bridge import (
    ALIF_MAQSURA_RULE,
    HAMZA_TO_BARE_ALIF_RULE,
)

CORPUS_PATH_VARIABLE = "ALGHANEM_QAC_MORPHOLOGY_PATH"

HAND_BUILT_QAC_ROOTS: tuple[str, ...] = ("Abd", "qwl", "sAl", "$hd", "rmY")
"""جذورٌ مُصطنَعةٌ على بنية خانة `ROOT`، لا مقتطعةٌ من بايتاتٍ ممنوعةِ النسخ."""


def test_the_standing_says_the_numbers_came_first() -> None:
    assert STANDING is RegistrationStanding.FORMULATED_AFTER_THE_NUMBER


def test_every_arriving_figure_carries_a_rule_a_standing_and_a_limit() -> None:
    for figure in ARRIVING_OVERLAP_FIGURES:
        assert isinstance(figure.counting_rule, OverlapCountingRule)
        assert isinstance(figure.standing, FigureStanding)
        assert figure.what_it_does_not_establish.strip()
        assert figure.declared_stage is None


def test_the_arriving_values_are_frozen_verbatim() -> None:
    assert figure_by_label("جذور_مقاييس").claimed_value == 4_565
    assert figure_by_label("جذور_المدوَّنة").claimed_value == 1_532
    assert figure_by_label("التقاطع").claimed_value == 1_204
    assert figure_by_label("غير_المغطّى").claimed_value == 3_361
    assert figure_by_label("غير_المغطّى_الثلاثي").claimed_value == 3_011
    assert figure_by_label("الفجوة_العكسية").claimed_value == 328


def test_a_figure_is_not_invented_after_seeing_a_count() -> None:
    with pytest.raises(OverlapPreregistrationError):
        figure_by_label("رقم_لم_يَرِد")


def test_the_two_sides_are_marked_checkable_and_not_checkable() -> None:
    assert (
        figure_by_label("جذور_مقاييس").standing
        is FigureStanding.CHECKABLE_FROM_TREE_BYTES
    )
    assert (
        figure_by_label("التقاطع").standing
        is FigureStanding.AWAITING_BYTES_NOT_IN_THE_TREE
    )


def test_the_stages_are_six_and_the_raw_one_transliterates_nothing() -> None:
    assert len(OVERLAP_STAGES) == 6
    raw = stage_by_name("خام")
    assert raw.transliterates_qac is False
    assert raw.rules == ()
    assert stage_by_name("تحويل_فقط").transliterates_qac is True
    assert stage_by_name("تحويل_فقط").rules == ()


def test_a_stage_that_normalises_without_transliterating_is_refused() -> None:
    with pytest.raises(OverlapPreregistrationError):
        OverlapStage(
            name="مقام_مصنوع",
            statement="تطبيعٌ بلا تحويل",
            transliterates_qac=False,
            rules=(HAMZA_TO_BARE_ALIF_RULE,),
        )


def test_a_stage_with_a_repeated_rule_is_refused() -> None:
    with pytest.raises(OverlapPreregistrationError):
        OverlapStage(
            name="مقام_مكرَّر",
            statement="قاعدةٌ مرّتين",
            transliterates_qac=True,
            rules=(ALIF_MAQSURA_RULE, ALIF_MAQSURA_RULE),
        )


def test_both_hamza_targets_have_a_stage_because_no_answer_arrived() -> None:
    names = {stage.name for stage in OVERLAP_STAGES}

    assert "تحويل_وهمزة_عارية" in names
    assert "تحويل_وهمزة_حاملة" in names
    assert len(UNANSWERED_COUNTING_DECISIONS) == 6
    for decision in UNANSWERED_COUNTING_DECISIONS:
        assert decision.how_it_was_handled_without_an_answer.strip()


def test_the_two_diagnoses_are_frozen_together_with_a_deciding_observation() -> None:
    labels = {hypothesis.label for hypothesis in HAMZA_DIAGNOSIS_HYPOTHESES}

    assert labels == {"عطل_في_الأداة", "عُرف_مُطبَّع_في_المدوَّنة"}
    for hypothesis in HAMZA_DIAGNOSIS_HYPOTHESES:
        assert hypothesis.what_it_predicts_about_the_root_alphabet.strip()
        assert hypothesis.what_would_refute_it.strip()


def test_the_preregistration_digest_is_derived_not_copied() -> None:
    assert preregistration_digest() == OVERLAP_PREREGISTRATION_DIGEST
    assert len(OVERLAP_PREREGISTRATION_DIGEST) == 64


def test_the_maqayis_side_re_derives_from_the_bytes_in_this_tree() -> None:
    roots = maqayis_roots()
    trilateral = maqayis_trilateral_roots()

    assert len(roots) == figure_by_label("جذور_مقاييس").claimed_value
    assert len(trilateral) == figure_by_label("جذور_مقاييس_الثلاثية").claimed_value
    assert trilateral <= roots


def test_the_root_alphabet_readout_names_the_hamza_characters_present() -> None:
    readout = qac_root_alphabet(HAND_BUILT_QAC_ROOTS)

    assert isinstance(readout, AlphabetReadout)
    assert readout.hamza_characters_present == ()
    assert dict(readout.characters)["A"] == 2


def test_the_root_alphabet_readout_reports_a_hamza_when_one_is_there() -> None:
    readout = qac_root_alphabet((">bd", "qwl"))

    assert readout.hamza_characters_present == (">",)


def test_an_empty_alphabet_is_refused_rather_than_emitted() -> None:
    with pytest.raises(OverlapCensusError):
        AlphabetReadout(characters=())
    with pytest.raises(OverlapCensusError):
        AlphabetReadout(characters=(("A", 0),))


def test_all_six_stages_leave_together_and_none_alone() -> None:
    readouts = overlap_readouts(("أبد", "قول", "رمى"), HAND_BUILT_QAC_ROOTS)

    assert tuple(readout.stage_name for readout in readouts) == tuple(
        stage.name for stage in OVERLAP_STAGES
    )
    with pytest.raises(OverlapCensusError):
        overlap_readouts(("أبد",), HAND_BUILT_QAC_ROOTS, stages=(OVERLAP_STAGES[2],))


def test_the_raw_stage_intersects_at_zero_as_the_join_note_measured() -> None:
    readouts = overlap_readouts(("أبد", "قول"), HAND_BUILT_QAC_ROOTS)

    assert readout_at(readouts, "خام").intersection == 0


def test_normalisation_changes_the_number_and_the_change_is_visible() -> None:
    readouts = overlap_readouts(("أبد", "قول"), ("Abd", "qwl"))
    transliterated = readout_at(readouts, "تحويل_فقط")
    bare = readout_at(readouts, "تحويل_وهمزة_عارية")
    carried = readout_at(readouts, "تحويل_وهمزة_حاملة")

    assert transliterated.intersection == 1
    assert transliterated.qac_only == 1
    assert bare.intersection == 2
    assert bare.qac_only == 0
    assert carried.intersection == 1
    assert carried.qac_only == 1


def test_a_readout_whose_parts_do_not_sum_to_its_side_is_refused() -> None:
    with pytest.raises(OverlapCensusError):
        OverlapReadout(
            stage_name="خام",
            maqayis_size=10,
            qac_size=5,
            intersection=3,
            maqayis_only=6,
            qac_only=2,
        )


def test_readout_at_refuses_a_stage_absent_from_the_run() -> None:
    readouts = overlap_readouts(("أبد",), ("Abd",))

    with pytest.raises(OverlapCensusError):
        readout_at(readouts, "مقام_لم_يُجمَّد")


def test_an_empty_side_is_refused_rather_than_counted_as_zero() -> None:
    with pytest.raises(OverlapCensusError):
        overlap_readouts((), ("Abd",))
    with pytest.raises(OverlapCensusError):
        overlap_readouts(("أبد",), ())


def test_the_price_of_a_stage_is_emitted_beside_its_gain() -> None:
    fusions = stage_fusions(("سأل", "سال"), ("Abd", ">bd"))
    raw = next(record for record in fusions if record.stage_name == "خام")
    bare = next(
        record for record in fusions if record.stage_name == "تحويل_وهمزة_عارية"
    )

    assert raw.maqayis_fusions == ()
    assert bare.maqayis_distinctions_lost == 1
    assert bare.qac_distinctions_lost == 1
    assert bare.maqayis_fusions[0].sources == ("سأل", "سال")


def test_the_named_residuals_are_carried_verbatim() -> None:
    assert len(OVERLAP_CENSUS_NAMED_RESIDUALS) == 4
    assert all(note.strip() for note in OVERLAP_CENSUS_NAMED_RESIDUALS.values())


@pytest.mark.skipif(
    not os.environ.get(CORPUS_PATH_VARIABLE),
    reason=(
        "بايتاتُ المدوَّنة ليست في هذه الشجرة ولا تُنسَخ إليها؛ فيُصرَّح بمسارها "
        f"في {CORPUS_PATH_VARIABLE} أو يُتخطّى هذا الاختبار مُصرَّحًا بالتخطّي"
    ),
)
def test_the_corpus_side_and_the_overlap_when_the_bytes_are_declared() -> None:
    path = Path(os.environ[CORPUS_PATH_VARIABLE])
    corpus_roots = qac_roots(path)
    alphabet = qac_root_alphabet(corpus_roots)
    readouts = overlap_readouts(maqayis_roots(), corpus_roots)

    assert len(corpus_roots) > 0
    assert alphabet.characters
    assert readout_at(readouts, "خام").intersection == 0
    assert len(readouts) == len(OVERLAP_STAGES)
    for readout in readouts:
        assert 0.0 <= readout.uncovered_share <= 1.0
        assert 0.0 <= readout.reverse_uncovered_share <= 1.0
