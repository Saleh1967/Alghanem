"""اختباراتُ جدول التغطية: محاورُ لا تُخلَط، وتحليلٌ لا يُحسَم بلا مرجع."""

from __future__ import annotations

from dataclasses import replace

import pytest

from alghanem.arabic.classification_coverage_scheme import (
    ANALYSIS_REFERENCE,
    AXIS_REFERENCE_REQUIREMENTS,
    COVERAGE_ITEMS,
    AnalysisCheck,
    AnalysisOutcome,
    AnalysisQuestion,
    AnalysisReference,
    CategoryClaim,
    ClassificationAxis,
    ClassificationCategory,
    ClassificationCoverageError,
    CoverageItem,
    ReferenceStanding,
    RootRecord,
    RootStanding,
    axis_of,
    deposit_tokens,
    render_coverage,
    run_coverage,
)

_REPORT = run_coverage()
_CATEGORIES_IN_THE_REPORT = {coverage.category for coverage in _REPORT.coverages}


def _row(key: str):
    for row in _REPORT.rows:
        if row.item.key == key:
            return row
    raise AssertionError(f"لا صفَّ لـ{key!r}")


def test_every_category_has_exactly_one_axis() -> None:
    """لا فئةَ بلا محور، ولا فئةَ في محورَين؛ وإلّا اختلط عدّادان."""

    for category in ClassificationCategory:
        assert isinstance(axis_of(category), ClassificationAxis)
    covered = {axis_of(category) for category in ClassificationCategory}
    assert covered == set(ClassificationAxis)


def test_the_root_is_not_a_category_beside_the_structure_descriptions() -> None:
    """الجذرُ أصلٌ محتمَل لا وصفُ بنية، فلا عضوَ له في مفردة الفئات."""

    names = {category.value for category in ClassificationCategory}
    assert not {name for name in names if "ROOT" in name}
    structure = {
        category
        for category in ClassificationCategory
        if axis_of(category) is ClassificationAxis.ORIGIN_AND_MORPHOLOGICAL_STRUCTURE
    }
    assert structure == {
        ClassificationCategory.JAMID,
        ClassificationCategory.MASDAR,
        ClassificationCategory.MUSHTAQQ,
    }


def test_the_masdar_is_its_own_category_and_is_not_folded_into_the_derived() -> None:
    assert ClassificationCategory.MASDAR in _CATEGORIES_IN_THE_REPORT
    assert ClassificationCategory.MASDAR is not ClassificationCategory.MUSHTAQQ


def test_no_root_is_written_and_none_is_forced_on_a_built_noun() -> None:
    """لا يُكتَب جذرٌ بلا مرجعٍ مُودَع، والاسمُ المبنيُّ يُصرَّح بامتناعه."""

    for item in COVERAGE_ITEMS:
        assert item.root_record.root is None
        assert item.root_record.why.strip()
    assert (
        _row("allathina").item.root_record.standing
        is RootStanding.NOT_LICENSED_FOR_THIS_WORD
    )
    assert (
        _row("ad_dallina").item.root_record.standing
        is RootStanding.AWAITING_THE_REFERENCE
    )


def test_a_root_read_from_a_reference_cannot_be_written_today() -> None:
    with pytest.raises(ClassificationCoverageError):
        RootRecord(
            standing=RootStanding.READ_FROM_A_DEPOSITED_REFERENCE,
            root=None,
            why="دعوى قراءة",
        )
    with pytest.raises(ClassificationCoverageError):
        RootRecord(
            standing=RootStanding.AWAITING_THE_REFERENCE,
            root="ض ل ل",
            why="جذرٌ مُنتزَع",
        )


def test_a_word_is_not_placed_in_two_categories_of_one_axis() -> None:
    """الخلطُ يبدأ من نسبة كلمةٍ إلى فئتَين من محورٍ واحد، فيُرفَض بنيويًّا."""

    with pytest.raises(ClassificationCoverageError):
        CoverageItem(
            key="mixed",
            token_index=21,
            claims=(
                CategoryClaim(
                    category=ClassificationCategory.MABNI,
                    declared_marker="علامة",
                    declared_evidence="دليل",
                ),
                CategoryClaim(
                    category=ClassificationCategory.MURAB,
                    declared_marker="علامة",
                    declared_evidence="دليل",
                ),
            ),
            root_record=RootRecord(
                standing=RootStanding.AWAITING_THE_REFERENCE,
                root=None,
                why="سبب",
            ),
            why_it_is_here="محاولةُ جمعِ البناء والإعراب في كلمةٍ واحدة",
        )


def test_the_structure_axis_carries_no_irab_marker() -> None:
    """لا علامةَ إعرابٍ في محور البنية؛ ولا فئةَ إعرابيّةً بلا علامةٍ ودليل."""

    with pytest.raises(ClassificationCoverageError):
        CategoryClaim(
            category=ClassificationCategory.MUSHTAQQ,
            declared_marker="مجرورٌ بالياء",
            declared_evidence="دليل",
        )
    with pytest.raises(ClassificationCoverageError):
        CategoryClaim(
            category=ClassificationCategory.PRESENT_MARFU,
            declared_marker="مرفوعٌ بالضمّة",
            declared_evidence=None,
        )


def test_an_inflected_verb_claim_asks_three_questions_not_one() -> None:
    """السؤالُ يطلب الحالةَ وعلامتَها ودليلَها، فثلاثةُ فحوصٍ لا فحصٌ واحد."""

    claim = _row("nabudu").item.claims[0]
    assert claim.category is ClassificationCategory.PRESENT_MARFU
    assert claim.questions == (
        AnalysisQuestion.CATEGORY,
        AnalysisQuestion.MARKER,
        AnalysisQuestion.EVIDENCE,
    )
    structure = _row("ad_dallina").item.claims[0]
    assert structure.questions == (AnalysisQuestion.CATEGORY,)


def test_every_declared_word_returns_its_bytes_and_this_is_run_not_written() -> None:
    """عمودُ الاسترجاع مُشتَقٌّ بالتشغيل، وموضعُ الفشل يُعرَض لو وقع."""

    assert _REPORT.word_total == len(COVERAGE_ITEMS)
    assert _REPORT.returned_total == _REPORT.word_total
    for row in _REPORT.rows:
        assert row.bytes_returned is True
        assert row.failure_position == "—"


def test_the_surfaces_come_from_the_deposit_and_are_not_retyped() -> None:
    """السطحُ يُقرأ من بايتات الإيداع بموضعه، فلا نصَّ ثانٍ يُقابَل به."""

    tokens = deposit_tokens()
    for item in COVERAGE_ITEMS:
        assert item.raw_bytes == tokens[item.token_index]
    assert _row("allathina").item.surface == "الَّذِينَ"
    assert _row("ad_dallina").item.surface == "الضَّالِّينَ"


def test_no_analysis_is_resolved_and_none_is_counted_correct() -> None:
    """كلُّ فحصٍ غيرُ محسوم، ولا يُحسَب صحيحًا، والدقّةُ ممتنعةٌ لا صفر."""

    for row in _REPORT.rows:
        for check in row.checks:
            assert check.outcome is AnalysisOutcome.UNRESOLVED_NO_ANALYZER_RAN
            assert check.is_resolved is False
    assert _REPORT.unresolved_total == sum(len(row.checks) for row in _REPORT.rows)
    for coverage in _REPORT.coverages:
        assert coverage.resolved_total == 0
        assert coverage.matched_total == 0
        assert coverage.analysis_accuracy is None


def test_a_settled_analysis_cannot_be_written_while_no_reference_is_deposited() -> None:
    check = _row("nabudu").checks[0]
    for outcome in (
        AnalysisOutcome.MATCHED_THE_REFERENCE,
        AnalysisOutcome.CONTRADICTED_THE_REFERENCE,
    ):
        with pytest.raises(ClassificationCoverageError):
            replace(check, outcome=outcome)


def test_round_trip_success_does_not_produce_any_analysis_accuracy() -> None:
    """نجاحُ الاسترجاع تامًّا لا يُنتج رقمًا في عمود التحليل؛ والعمودان مفصولان."""

    jamid = _REPORT.coverage(ClassificationCategory.JAMID)
    assert jamid.round_trip == 1.0
    assert jamid.analysis_accuracy is None


def test_an_empty_category_keeps_a_row_and_has_no_rate() -> None:
    """الفئةُ الخاليةُ لا تُحذَف ولا تُكتَب مئةً بالمئة؛ نسبتُها ممتنعة."""

    empty = _REPORT.empty_categories
    assert set(empty) == {
        ClassificationCategory.MASDAR,
        ClassificationCategory.BUILT_PRESENT_VERB,
        ClassificationCategory.PRESENT_MANSUB,
        ClassificationCategory.PRESENT_MAJZUM,
    }
    for category in empty:
        coverage = _REPORT.coverage(category)
        assert coverage.word_total == 0
        assert coverage.round_trip is None
        assert coverage.analysis_accuracy is None


def test_every_category_appears_even_when_it_has_no_word() -> None:
    assert _CATEGORIES_IN_THE_REPORT == set(ClassificationCategory)
    assert len(_REPORT.coverages) == len(ClassificationCategory)


def test_an_axis_reads_only_its_own_categories() -> None:
    for axis in ClassificationAxis:
        for coverage in _REPORT.axis_coverages(axis):
            assert coverage.axis is axis
    counted = sum(len(_REPORT.axis_coverages(axis)) for axis in ClassificationAxis)
    assert counted == len(ClassificationCategory)


def test_a_category_counts_only_the_checks_declared_for_it() -> None:
    """فحصُ فئةٍ لا يُحسَب لفئةٍ أخرى، وإن جمعتهما كلمةٌ واحدة."""

    mabni = _REPORT.coverage(ClassificationCategory.MABNI)
    assert mabni.word_total == 3
    assert len(mabni.checks) == 9
    assert {check.category for check in mabni.checks} == {ClassificationCategory.MABNI}
    jamid = _REPORT.coverage(ClassificationCategory.JAMID)
    assert len(jamid.checks) == 1


def test_the_named_reference_is_not_deposited_and_cannot_settle_a_check() -> None:
    """`MAQSAD` مُسمًّى يُطبَع يدويًّا، ولا بصمةَ له، فلا يحسم فحصًا."""

    assert ANALYSIS_REFERENCE.name == "MAQSAD"
    assert ANALYSIS_REFERENCE.standing is ReferenceStanding.BEING_TRANSCRIBED_BY_HAND
    assert ANALYSIS_REFERENCE.digest is None
    assert ANALYSIS_REFERENCE.can_settle_an_analysis is False


def test_a_deposited_reference_needs_a_digest_and_a_digest_needs_a_deposit() -> None:
    with pytest.raises(ClassificationCoverageError):
        AnalysisReference(
            name="MAQSAD",
            standing=ReferenceStanding.DEPOSITED_AND_FINGERPRINTED,
            digest=None,
            how_it_is_being_obtained="دعوى إيداع",
        )
    with pytest.raises(ClassificationCoverageError):
        AnalysisReference(
            name="MAQSAD",
            standing=ReferenceStanding.NAMED_ONLY,
            digest="0" * 64,
            how_it_is_being_obtained="بصمةٌ بلا بايتات",
        )


def test_this_table_refuses_to_run_against_a_reference_it_does_not_read() -> None:
    """لو أُعلن المرجعُ مُودَعًا لم يُشغَّل هذا الجدول، فهو لا يقرأ مرجعًا."""

    deposited = AnalysisReference(
        name="MAQSAD",
        standing=ReferenceStanding.DEPOSITED_AND_FINGERPRINTED,
        digest="a" * 64,
        how_it_is_being_obtained="مُودَعٌ مُبصَّم",
    )
    with pytest.raises(ClassificationCoverageError):
        run_coverage(COVERAGE_ITEMS, deposited)


def test_every_axis_names_what_a_reference_must_supply_to_lift_it() -> None:
    axes = {requirement.axis for requirement in AXIS_REFERENCE_REQUIREMENTS}
    assert axes == set(ClassificationAxis)
    for requirement in AXIS_REFERENCE_REQUIREMENTS:
        assert requirement.question_the_axis_asks.strip()
        assert requirement.what_the_reference_must_supply.strip()


def test_an_empty_table_is_refused_rather_than_reported_as_complete() -> None:
    with pytest.raises(ClassificationCoverageError):
        run_coverage(())


def test_the_rendered_table_shows_the_columns_the_measurement_requires() -> None:
    rendered = render_coverage(_REPORT)
    for axis in ClassificationAxis:
        assert axis.value in rendered
    for category in ClassificationCategory:
        assert category.value in rendered
    for column in ("RoundTrip", "REFUSED", "MISMATCH", "UNRESOLVED", "Accuracy"):
        assert column in rendered
    assert "bytes returned: 5/5" in rendered
    assert "unresolved analyses: 26" in rendered
    assert "MAQSAD" in rendered


def test_a_check_outside_the_closed_outcome_is_refused() -> None:
    with pytest.raises(ClassificationCoverageError):
        AnalysisCheck(
            category=ClassificationCategory.MABNI,
            question=AnalysisQuestion.CATEGORY,
            outcome=AnalysisOutcome.MATCHED_THE_REFERENCE,
        )
