"""اختباراتُ امتحان نجاح الجبر: الحكمُ يُشتَقّ، والمقدارُ يُعاد اشتقاقُه.

ولا يُجمَّد ههنا مقدارٌ ينمو بنموّ الشجرة؛ فالمقيسُ مُودَعٌ مختومُ الطول
والبصمة، وما يُؤكَّد إمّا علاقةٌ بين مقدارَين، وإمّا بنيةُ قراءةٍ في شاهد،
وإمّا ردٌّ على مدخلٍ غيرِ مشهود.
"""

from __future__ import annotations

import pytest

from alghanem.arabic import algebra_success_exam as exam
from alghanem.arabic import letter_haraka_partition as partition

# ---------------------------------------------------------------------------
# قراءةُ الحوامل
# ---------------------------------------------------------------------------


def test_a_carrier_outside_the_declared_alphabet_is_not_a_cell() -> None:
    """همزةُ القطع تُطوى إلى «ء» وهي خارجَ الثمانية والعشرين، فلا خليّةَ لها."""

    carriers = exam.carriers_of("وَأَقِيمُوا")
    site = carriers[1]
    assert site.letter is None
    assert site.haraka is not None
    assert site.cell is None
    assert site.standing is exam.CellStanding.OUTSIDE_THE_DECLARED_ALPHABET


def test_a_carrier_without_a_declared_haraka_is_not_a_cell_either() -> None:
    """ألفُ الوصل حرفٌ مُعلَنٌ بلا حركةٍ مُعلَنة؛ والعلّتان مختلفتان لا واحدة."""

    site = exam.carriers_of("وَاسْتَعِينُوا")[1]
    assert site.letter == "ا"
    assert site.haraka is None
    assert site.standing is exam.CellStanding.NO_DECLARED_HARAKA
    assert not site.is_a_cell


def test_a_readable_carrier_lands_in_a_cell_of_the_declared_table() -> None:
    first = exam.carriers_of("وَاسْتَعِينُوا")[0]
    assert first.is_a_cell
    cell = first.cell
    assert cell is not None
    assert cell[0] in partition.THE_DECLARED_LETTERS
    assert cell[1] in partition.THE_DECLARED_HARAKAT


# ---------------------------------------------------------------------------
# الشواهدُ مشهودةٌ أو لا تُمتحَن بها آلة
# ---------------------------------------------------------------------------


def test_every_named_witness_is_attested_in_the_sealed_deposit() -> None:
    named = (
        tuple(witness.form for witness in exam.THE_IBTIDA_WITNESSES)
        + exam.THE_ILAL_WITNESSES
        + exam.THE_SAKINAYN_WITNESSES
    )
    for form in named:
        assert exam.deposited_occurrences(form) > 0, form


def test_a_form_that_is_not_in_the_deposit_counts_zero() -> None:
    assert exam.deposited_occurrences("وانكسر") == 0


def test_a_decision_site_outside_its_form_is_refused() -> None:
    with pytest.raises(exam.AlgebraSuccessExamError):
        exam.IbtidaWitness(form="اهْدِنَا", site_index=-1, required_outcome="شيء")


def test_a_witness_that_declares_no_required_outcome_is_refused() -> None:
    with pytest.raises(exam.AlgebraSuccessExamError):
        exam.IbtidaWitness(form="اهْدِنَا", site_index=0, required_outcome="   ")


# ---------------------------------------------------------------------------
# المحطّاتُ: الحكمُ مُشتَقٌّ من المقدار لا مكتوبٌ في حقل
# ---------------------------------------------------------------------------


def _measured(reading: exam.StationReading, key: str) -> int:
    for name, value in reading.measured:
        if name == key:
            return value
    raise AssertionError(f"لا مقدارَ باسم {key} في محطّة {reading.name}")


def test_the_pausal_faces_outnumber_the_states_the_law_admits() -> None:
    """ثلاثةٌ مطلوبةٌ في واحدةٍ متاحة؛ والحكمُ يتبع هذه العلاقةَ لا العكس."""

    reading = exam.waqf_station()
    faces = _measured(reading, "الأوجهُ المنقولة")
    admitted = _measured(reading, "ما يقبله قانونُ الوقف من الحركات المُعلَنة")
    assert faces == len(exam.THE_PAUSAL_FACES)
    assert admitted < faces
    assert reading.verdict is exam.StationVerdict.DISCRIMINATION_IMPOSSIBLE_BY_COUNT


def test_the_admitted_pausal_state_is_derived_from_the_declared_harakat() -> None:
    """الحالةُ المقبولةُ تُرشَّح من الحركات المُعلَنة، فلا تُكتَب عددًا مستقلًّا."""

    admitted = [
        mark
        for mark in partition.THE_DECLARED_HARAKAT
        if mark in exam.THE_PAUSAL_LAW_ADMITS
    ]
    assert admitted == ["\u0652"]


def test_no_decision_site_of_the_ibtida_station_is_readable_as_a_cell() -> None:
    """الإخفاقُ ههنا غيابُ حالةٍ لا جوابٌ خاطئ؛ ويُقاس بعدد المواضع المقروءة."""

    reading = exam.ibtida_station()
    witnesses = _measured(reading, "الشواهدُ المشهودة")
    readable = _measured(reading, "المواضعُ التي تُقرأ خليّة")
    assert witnesses == len(exam.THE_IBTIDA_WITNESSES)
    assert readable == 0
    assert reading.verdict is exam.StationVerdict.UNREADABLE_AT_THE_DECISION_SITE


def test_the_three_required_outcomes_collapse_into_one_projection() -> None:
    reading = exam.ibtida_station()
    assert _measured(reading, "المطلوباتُ المتمايزة") == 3
    assert _measured(reading, "الصورُ المتمايزة في الجدول") == 1


def test_the_ibtida_sites_fail_for_two_different_named_reasons() -> None:
    """العلّتان مختلفتان، فلا تُجمَعان في علّةٍ واحدةٍ تُخفي إحداهما."""

    standings = {site.standing for site in exam.read_decision_sites()}
    assert standings == {
        exam.CellStanding.OUTSIDE_THE_DECLARED_ALPHABET,
        exam.CellStanding.NO_DECLARED_HARAKA,
    }


def test_the_surface_ilal_rule_fires_on_an_attested_form_and_is_falsified() -> None:
    """إيقادٌ واحدٌ على صورةٍ مشهودةٍ يكفي؛ والعددُ يُعاد اشتقاقُه لا يُجمَّد."""

    reading = exam.ilal_station()
    firings = _measured(reading, "الإيقاداتُ كلُّها")
    tokens = _measured(reading, "الكلماتُ التي أوقدت")
    distinct = _measured(reading, "الصورُ المتمايزةُ التي أوقدت")
    assert firings >= tokens >= distinct > 0
    assert reading.verdict is exam.StationVerdict.FALSIFIED_BY_AN_ATTESTED_FORM


def test_each_named_ilal_witness_fires_the_rule_by_itself() -> None:
    for form in exam.THE_ILAL_WITNESSES:
        assert exam.ilal_rule_fires_at(form), form


def test_the_rule_does_not_fire_where_the_preceding_carrier_is_not_fathated() -> None:
    """القاعدةُ تُشترَط لا تُعمَّم؛ فموضعٌ لا فتحةَ قبله لا يُوقِدها."""

    assert exam.ilal_rule_fires_at("وَأَقِيمُوا") == ()
    assert exam.ilal_rule_fires_at("وَاسْتَعِينُوا") == ()


def test_the_sakinayn_shape_is_attested_so_an_absolute_ban_is_refused() -> None:
    reading = exam.sakinayn_station()
    occurrences = _measured(reading, "وقوعاتُ الشكل")
    distinct = _measured(reading, "الصورُ المتمايزةُ الحاملةُ له")
    named = _measured(reading, "الشاهدان المُسمَّيان الحاملان له")
    assert occurrences >= distinct > 0
    assert named == len(exam.THE_SAKINAYN_WITNESSES)
    assert reading.verdict is exam.StationVerdict.FALSIFIED_BY_AN_ATTESTED_FORM


def test_the_measured_shape_is_wider_than_the_two_named_witnesses() -> None:
    """الشكلُ وكيلٌ يجمع مصادرَ شتّى، فلا يُقرأ عددُه عددَ الظاهرة المسمّاة."""

    reading = exam.sakinayn_station()
    assert _measured(reading, "الصورُ المتمايزةُ الحاملةُ له") > len(
        exam.THE_SAKINAYN_WITNESSES
    )


# ---------------------------------------------------------------------------
# الحصيلة
# ---------------------------------------------------------------------------


def test_every_station_names_its_question_and_its_passing_condition() -> None:
    for reading in exam.exam_stations():
        assert reading.question.strip()
        assert reading.passing_condition.strip()
        assert reading.measured
        assert reading.detail.strip()


def test_a_station_without_a_measured_magnitude_is_refused() -> None:
    """محطّةٌ بلا مقدارٍ لا تُخرِج حكمًا؛ فلا يُصطنَع اجتيازٌ من فراغ."""

    with pytest.raises(exam.AlgebraSuccessExamError):
        exam.StationReading(
            name="محطّةٌ",
            question="سؤالٌ؟",
            passing_condition="شرطٌ",
            measured=(),
            verdict=exam.StationVerdict.PASSED,
            detail="تفصيلٌ",
        )


def test_a_station_that_hides_its_passing_condition_is_refused() -> None:
    with pytest.raises(exam.AlgebraSuccessExamError):
        exam.StationReading(
            name="محطّةٌ",
            question="سؤالٌ؟",
            passing_condition="  ",
            measured=(("مقدارٌ", 1),),
            verdict=exam.StationVerdict.PASSED,
            detail="تفصيلٌ",
        )


def test_the_exam_standing_is_broken_by_one_station_and_not_averaged() -> None:
    stations = exam.exam_stations()
    assert len(stations) == 4
    assert not any(station.passed for station in stations)
    assert exam.exam_standing(stations) is exam.ExamStanding.FAILED_AT_A_NAMED_STATION


def test_a_single_failing_station_outweighs_every_passing_one() -> None:
    """لو اجتازت ثلاثٌ وأخفقت واحدةٌ لم تُجمَع الحصيلةُ أغلبيّةً."""

    passing = exam.StationReading(
        name="مجتازةٌ",
        question="سؤالٌ؟",
        passing_condition="شرطٌ",
        measured=(("مقدارٌ", 0),),
        verdict=exam.StationVerdict.PASSED,
        detail="تفصيلٌ",
    )
    failing = exam.StationReading(
        name="مخفقةٌ",
        question="سؤالٌ؟",
        passing_condition="شرطٌ",
        measured=(("مقدارٌ", 1),),
        verdict=exam.StationVerdict.FALSIFIED_BY_AN_ATTESTED_FORM,
        detail="تفصيلٌ",
    )
    assert (
        exam.exam_standing((passing, passing, passing, failing))
        is exam.ExamStanding.FAILED_AT_A_NAMED_STATION
    )
    assert (
        exam.exam_standing((passing, passing)) is exam.ExamStanding.PASSED_EVERY_STATION
    )


def test_an_exam_without_a_station_yields_no_standing() -> None:
    with pytest.raises(exam.AlgebraSuccessExamError):
        exam.exam_standing(())


def test_the_documentation_debt_is_deferred_and_named_not_silently_paid() -> None:
    """المصادرُ غيرُ المُودَعة تُسمّى دَينًا، ولا تُقرأ موافقةً ولا مخالفة."""

    debt = exam.THE_DOCUMENTATION_DEBT_IS_DEFERRED_AND_NAMED
    for name in ("بَطّوش", "Beesley", "Hulden"):
        assert name in debt


def test_no_exam_here_lifts_a_block_or_thaws_a_freeze() -> None:
    assert exam.the_block_and_the_freeze_are_untouched() is True


def test_every_named_residual_opens_with_its_own_token() -> None:
    for token, text in exam.ALGEBRA_SUCCESS_EXAM_NAMED_RESIDUALS.items():
        assert text.startswith(f"{token}:")
