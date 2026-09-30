"""شواهدُ مختبر الاكتشاف: تُصادم بروتوكولَه ولا تنقل حصيلتَه."""

from __future__ import annotations

from pathlib import Path

import pytest

from alghanem.arabic.discovery_lab import (
    THE_DEPOSITS,
    THE_FITTING_DEPOSIT,
    THE_HELD_OUT_DEPOSIT,
    THE_LADDER,
    THE_RIVAL_EXPLANATIONS,
    THE_RUN_LEDGER,
    DiscoveryLabError,
    Explanation,
    ExplanationStanding,
    LabDeposit,
    Rung,
    RungStanding,
    enacted_explanations,
    explanation_reading,
    held_out_agreement,
    ordering_flips_on_leaving_one_word_out,
    reading_of,
    reads_a_prior_ledger,
    run,
    rung_standing,
    separating_positions,
)


def test_the_lab_holds_at_least_two_rival_explanations() -> None:
    """تفسيرٌ بلا منافسٍ لا يُختبَر؛ فالشرطُ اثنان فصاعدًا بأسماءَ متمايزة."""

    assert len(THE_RIVAL_EXPLANATIONS) >= 2
    assert len({item.name for item in THE_RIVAL_EXPLANATIONS}) == len(
        THE_RIVAL_EXPLANATIONS
    )


def test_the_material_separates_the_rivals_on_every_deposit() -> None:
    """اختبارٌ لا يفرّق بين التفسيرَين ليس اختبارًا؛ فيُعَدُّ فرقُه قبل الحكم."""

    for deposit in THE_DEPOSITS:
        assert separating_positions(deposit) > 0


def test_a_material_that_does_not_separate_yields_no_ranking() -> None:
    """مادّةٌ يتّفق عليها التفسيران تُخرِج صفرًا، فلا يُقرأ منها ترجيح."""

    agreed = LabDeposit(name="مصنوع", text="بَا", domain="مصنوعٌ للشاهد")
    assert separating_positions(agreed) == 0


def test_both_explanations_fall_and_neither_is_smuggled_as_standing() -> None:
    """الحصيلةُ المقيسة: كلتا الدعويَين مُكافِئةٌ ومنقوضةٌ في المُودَعَين."""

    report = run()
    assert report.stood == ()
    assert len(report.fell) == len(THE_DEPOSITS) * len(THE_RIVAL_EXPLANATIONS)
    for _, _, counterexamples in report.fell:
        assert counterexamples > 0


def test_a_counterexample_from_either_side_suffices_to_fell_a_claim() -> None:
    """الكفايةُ والخصوصيّةُ مطلوبتان معًا؛ فالتجاوزُ وحدَه يُسقِط الدعوى."""

    deposit = THE_DEPOSITS[0]
    structural = next(item for item in THE_RIVAL_EXPLANATIONS if item.name == "البنيويّ")
    reading = explanation_reading(structural, deposit)
    assert reading.overreached
    assert reading.standing is ExplanationStanding.FELL_ON_A_COUNTEREXAMPLE


def test_the_residue_is_counted_and_not_swept() -> None:
    """ما لم يفسّره تفسيرٌ منهما يُعَدُّ ويُخرَج، ولا يُطوى ليبدو كلُّ شيءٍ مفسَّرًا."""

    report = run()
    assert len(report.pending) == len(THE_DEPOSITS)
    for deposit_name, unexplained, overreached in report.pending:
        assert deposit_name in {deposit.name for deposit in THE_DEPOSITS}
        assert unexplained > 0
        assert overreached > 0


def test_the_unexplained_positions_are_missed_by_every_explanation() -> None:
    """المعلَّقُ الأوّلُ ما فات التفسيرَين جميعًا، لا ما فات أحدَهما."""

    for deposit in THE_DEPOSITS:
        deposition = reading_of(deposit)
        for item in deposition.unexplained:
            assert not item.is_marked
            for explanation in THE_RIVAL_EXPLANATIONS:
                assert not explanation.predicate(item)


def test_the_weaker_ordering_claim_stands_where_the_biconditionals_fell() -> None:
    """ما ثبت أضعفُ ممّا سقط ويُسمّى بحدّه: ترتيبُ النقض لا قاعدةُ تكافؤ."""

    assert run().ordering_holds is True


def test_the_ordering_is_not_carried_by_a_single_word() -> None:
    """حكمٌ يقلبه حذفُ كلمةٍ واحدةٍ محمولٌ بها؛ فيُصادَم بحذف كلّ كلمةٍ على حدة."""

    assert ordering_flips_on_leaving_one_word_out() == ()


def test_the_held_out_deposit_is_not_the_fitting_deposit() -> None:
    """المادّةُ المستقلّةُ غيرُ مادّة الترجيح، وإلّا فالنجاحُ نجاحٌ على النفس."""

    assert THE_FITTING_DEPOSIT != THE_HELD_OUT_DEPOSIT
    names = {deposit.name for deposit in THE_DEPOSITS}
    assert {THE_FITTING_DEPOSIT, THE_HELD_OUT_DEPOSIT} <= names


def test_the_held_out_agreement_is_measured_and_named_a_presumption() -> None:
    """يتّفق الترجيحان على المُودَعَين، ولا يُرفَع الاتّفاقُ إلى استيفاء درجة."""

    fitted, held_out, agreed = held_out_agreement()
    assert agreed is True
    assert fitted == held_out == "البنيويّ"


def test_every_explanation_text_is_found_in_the_units_own_bytes() -> None:
    """سندُ منع الدرجة الثانية: القاعدتان مسنونتان بيدٍ، ونصُّهما ههنا."""

    assert set(enacted_explanations()) == {
        explanation.name for explanation in THE_RIVAL_EXPLANATIONS
    }


def test_the_ladder_has_four_rungs_each_with_a_success_and_a_blocker() -> None:
    """لكلّ درجةٍ معيارُ نجاحٍ ومانعُ انتقالٍ وسدادٌ مُسمًّى، مكتوبةً قبل الجري."""

    assert [rung.number for rung in THE_LADDER] == [1, 2, 3, 4]
    for rung in THE_LADDER:
        assert rung.success.strip()
        assert rung.blocker.strip()
        assert rung.discharge.strip()


def test_a_rung_without_a_blocker_is_refused_at_construction() -> None:
    """درجةٌ بلا مانعٍ مُعلَنٍ تُبلَغ بالتسامح، فتُرَدّ عند البناء."""

    with pytest.raises(DiscoveryLabError):
        Rung(number=1, name="درجة", success="نجاح", blocker="  ", discharge="سداد")


def test_only_the_first_rung_is_reached_and_the_rest_are_blocked() -> None:
    """المنزلةُ تُقاس لا تُعلَن: الأولى مبلوغةٌ والثلاثُ ممنوعةٌ بموانعها."""

    standings = {rung.number: standing for rung, standing, _ in rung_standing()}
    assert standings[1] is RungStanding.REACHED_ON_THIS_EVIDENCE
    for number in (2, 3, 4):
        assert standings[number] is RungStanding.BLOCKED_BY_ITS_DECLARED_BLOCKER


def test_the_third_rungs_blocker_is_an_absent_deposit_on_disk() -> None:
    """مانعُ الثالثة غيابُ سجلٍّ يُلتمَس على القرص؛ ولو أُودِع لانقلب الحكم."""

    assert reads_a_prior_ledger() is False
    assert not (Path(THE_RUN_LEDGER)).is_file()


def test_the_fourth_rungs_blocker_is_counted_from_declared_domains() -> None:
    """عدّةُ المجالات تُعَدُّ من إعلانات المُودَعات لا تُقدَّر."""

    assert len({deposit.domain for deposit in THE_DEPOSITS}) == 1


def test_every_rung_standing_carries_a_measured_reason() -> None:
    """لا منزلةَ بلا تعليلٍ مشتقٍّ عند القراءة؛ فالإعلانُ وحدَه لا يُبلِغ درجة."""

    for rung, standing, why in rung_standing():
        assert isinstance(rung, Rung)
        assert standing in set(RungStanding)
        assert why.strip()


def test_a_deposit_without_a_declared_domain_is_refused() -> None:
    """مُودَعٌ بلا مجالٍ مُعلَنٍ لا يُعَدُّ في الانتقال، فيُرَدّ عند البناء."""

    with pytest.raises(DiscoveryLabError):
        LabDeposit(name="مُودَع", text="بَ", domain=" ")


def test_an_explanation_without_a_claim_is_refused() -> None:
    """تفسيرٌ بلا نصِّ دعوًى لا يُقابَل ببايتات، فيُرَدّ قبل أن يُختبَر."""

    with pytest.raises(DiscoveryLabError):
        Explanation(name="بلا دعوى", claim="", predicate=lambda reading: True)


def test_an_unknown_deposit_or_explanation_is_refused_not_guessed() -> None:
    """لا يُحمَل مطلوبٌ غائبٌ على أقرب حاضر."""

    report = run()
    with pytest.raises(DiscoveryLabError):
        report.deposition_for("مُودَعٌ ليس ههنا")
    with pytest.raises(DiscoveryLabError):
        report.depositions[0].reading_for("تفسيرٌ ليس ههنا")
