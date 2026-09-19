"""اختباراتُ جدول التغطية: محاورُ لا تُخلَط، وفحصٌ يُسمّى بعلّته لا يُطوى."""

from __future__ import annotations

from pathlib import Path

import pytest

from alghanem.arabic.classification_coverage_scheme import (
    ANALYSIS_REFERENCE,
    AXIS_REFERENCE_REQUIREMENTS,
    CATEGORY_TAGS,
    COVERAGE_ITEMS,
    TAGS_NOT_ASSIGNED_TO_A_CATEGORY,
    AnalysisCheck,
    AnalysisOutcome,
    AnalysisQuestion,
    AnalysisReference,
    CategoryClaim,
    ClassificationAxis,
    ClassificationCategory,
    ClassificationCoverageError,
    CoverageItem,
    ReferenceAddress,
    ReferenceStanding,
    RootRecord,
    RootStanding,
    axis_of,
    deposit_tokens,
    letters_only,
    masaq_reference,
    render_coverage,
    run_coverage,
    word_tags,
)
from alghanem.arabic.masaq_corpus_deposit import (
    DERIVED_NOUN_TAGS,
    MASAQ_PATH_VARIABLE,
    MASAQ_SHA256,
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
            reference_address=ReferenceAddress(sura="1", verse="7"),
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


def test_no_analysis_is_resolved_while_the_reference_bytes_are_absent() -> None:
    """لا فحصَ محسومًا ما دامت البايتاتُ غائبة، ولا يُحسَب غيرُ المحسوم صحيحًا."""

    for row in _REPORT.rows:
        for check in row.checks:
            assert check.is_resolved is False
    assert _REPORT.unresolved_total == sum(len(row.checks) for row in _REPORT.rows)
    for coverage in _REPORT.coverages:
        assert coverage.resolved_total == 0
        assert coverage.matched_total == 0
        assert coverage.analysis_accuracy is None


def test_every_unresolved_check_names_its_own_cause() -> None:
    """العلّةُ تُسمّى واحدةً واحدة، ولا تُجمَع تحت «لم يجرِ تحليل»."""

    causes = _REPORT.unresolved_by_cause
    assert sum(causes.values()) == _REPORT.unresolved_total == 26
    assert causes == {
        AnalysisOutcome.UNRESOLVED_NO_ATTESTED_TAG_FOR_THIS_CATEGORY: 9,
        AnalysisOutcome.UNRESOLVED_REFERENCE_BYTES_NOT_RESOLVED: 1,
        AnalysisOutcome.UNRESOLVED_THE_REFERENCE_HAS_NO_COLUMN_FOR_THIS_QUESTION: 16,
    }


def test_the_marker_and_evidence_questions_fail_in_the_reference_not_the_bytes() -> (
    None
):
    """عجزُ المرجع عن سؤالٍ يُقال قبل طلب بايتاته، فلا يُحمَل على غيابٍ عارض."""

    for row in _REPORT.rows:
        for check in row.checks:
            if check.question is AnalysisQuestion.CATEGORY:
                continue
            assert check.outcome is (
                AnalysisOutcome.UNRESOLVED_THE_REFERENCE_HAS_NO_COLUMN_FOR_THIS_QUESTION
            )


def test_only_the_categories_with_an_attested_tag_wait_on_the_bytes() -> None:
    """ما لا وَسْمَ مُثبَتًا له لا ينتظر البايتات؛ علّتُه غيرُ علّتها."""

    for row in _REPORT.rows:
        for check in row.checks:
            if check.question is not AnalysisQuestion.CATEGORY:
                continue
            waits = check.outcome is (
                AnalysisOutcome.UNRESOLVED_REFERENCE_BYTES_NOT_RESOLVED
            )
            assert waits is (check.category in CATEGORY_TAGS)


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


def test_the_reference_is_masaq_and_its_digest_is_read_not_copied() -> None:
    """اسمُ المرجع `MASAQ`، وبصمتُه مقروءةٌ من الإيداع لا منسوخةً باليد."""

    assert ANALYSIS_REFERENCE.name == "MASAQ"
    assert ANALYSIS_REFERENCE.digest == MASAQ_SHA256
    assert ANALYSIS_REFERENCE.can_settle_an_analysis is False


def test_the_reference_standing_is_run_on_the_bytes_not_written(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """ثلاثُ حالاتٍ تُفرَّق بالتشغيل: لا تُحَلّ، وحُلَّت فخالفت، وحُلَّت فطابقت."""

    monkeypatch.delenv(MASAQ_PATH_VARIABLE, raising=False)
    absent = tmp_path / "لا_ملفّ.csv"
    assert (
        masaq_reference(absent).standing
        is ReferenceStanding.FINGERPRINTED_BUT_BYTES_NOT_RESOLVED
    )
    wrong = tmp_path / "MASAQ.csv"
    wrong.write_bytes(b"\xd8\xa8\xd8\xa7\xd9\x8a\xd8\xaa")
    reference = masaq_reference(wrong)
    assert reference.standing is ReferenceStanding.BYTES_PRESENT_BUT_DIGEST_MISMATCHED
    assert reference.can_settle_an_analysis is False


def test_a_fingerprinted_standing_needs_a_digest_and_a_named_one_refuses_it() -> None:
    with pytest.raises(ClassificationCoverageError):
        AnalysisReference(
            name="MASAQ",
            standing=ReferenceStanding.DEPOSITED_AND_FINGERPRINTED,
            digest=None,
            how_it_is_being_obtained="دعوى إيداع",
        )
    with pytest.raises(ClassificationCoverageError):
        AnalysisReference(
            name="MASAQ",
            standing=ReferenceStanding.NAMED_ONLY,
            digest="0" * 64,
            how_it_is_being_obtained="بصمةٌ بلا بايتات",
        )


def _synthetic_records(tag: str) -> tuple[dict[str, str], ...]:
    """سجلّاتٌ **مُصطنَعةٌ مُصرَّحٌ بجنسها**، تُحاكي بنيةَ الصفّ ولا تُقرأ رقمًا."""

    return (
        {
            "Sura_No": "1",
            "Verse_No": "7",
            "Column5": "9",
            "Word_No": "1",
            "Segmented_Word": "ال",
            "Morph_Tag": "DET",
        },
        {
            "Sura_No": "1",
            "Verse_No": "7",
            "Column5": "9",
            "Word_No": "2",
            "Segmented_Word": "ضالين",
            "Morph_Tag": tag,
        },
    )


def _deposited_reference() -> AnalysisReference:
    return AnalysisReference(
        name="MASAQ",
        standing=ReferenceStanding.DEPOSITED_AND_FINGERPRINTED,
        digest=MASAQ_SHA256,
        how_it_is_being_obtained="سجلّاتٌ مُصطنَعةٌ مُصرَّحٌ بجنسها في الاختبار",
    )


def _dallina() -> CoverageItem:
    return next(item for item in COVERAGE_ITEMS if item.key == "ad_dallina")


def test_a_word_is_found_by_its_letters_under_the_word_key_not_the_segment_index() -> (
    None
):
    """المقاطعُ تُجمَع بـ`Column5`، وتُطابَق بحروف الكلمة لا بشكلها."""

    item = _dallina()
    found = word_tags(
        _synthetic_records("NOUN_ACTIVE_PART"), item.reference_address, item.surface
    )
    assert found == ("DET", "NOUN_ACTIVE_PART")
    assert letters_only(item.surface) == "الضالين"


def test_the_reader_settles_the_category_question_when_the_tag_agrees() -> None:
    """الوصلُ يعمل: وَسْمٌ من وسوم المشتقّ يُخرِج دقّةً مئةً بالمئة في فئته."""

    report = run_coverage(
        items=(_dallina(),),
        reference=_deposited_reference(),
        records=_synthetic_records("NOUN_ACTIVE_PART"),
    )
    coverage = report.coverage(ClassificationCategory.MUSHTAQQ)
    assert coverage.resolved_total == 1
    assert coverage.matched_total == 1
    assert coverage.analysis_accuracy == 1.0


def test_a_contradicting_tag_is_counted_against_the_claim_not_hidden() -> None:
    """وَسْمٌ من بابٍ آخرَ يُخرِج مخالفةً محسومة، ودقّةً صفرًا لا امتناعًا."""

    report = run_coverage(
        items=(_dallina(),),
        reference=_deposited_reference(),
        records=_synthetic_records("GERUND"),
    )
    coverage = report.coverage(ClassificationCategory.MUSHTAQQ)
    assert coverage.resolved_total == 1
    assert coverage.matched_total == 0
    assert coverage.analysis_accuracy == 0.0


def test_a_word_absent_from_the_reference_is_named_absent_not_contradicted() -> None:
    report = run_coverage(
        items=(_dallina(),),
        reference=_deposited_reference(),
        records=(),
    )
    causes = report.unresolved_by_cause
    assert causes[AnalysisOutcome.UNRESOLVED_WORD_NOT_FOUND_IN_THE_REFERENCE] == 1
    assert report.coverage(ClassificationCategory.MUSHTAQQ).analysis_accuracy is None


def test_every_tag_written_here_is_attested_in_the_deposit() -> None:
    """لا يُكتَب وَسْمٌ لم يُقرأ في هذه الشجرة، ولو كان مُرجَّحًا."""

    attested = {item.tag for item in DERIVED_NOUN_TAGS}
    for tags in CATEGORY_TAGS.values():
        assert tags <= attested
    assert set(TAGS_NOT_ASSIGNED_TO_A_CATEGORY) <= attested
    assert set(TAGS_NOT_ASSIGNED_TO_A_CATEGORY).isdisjoint(
        tag for tags in CATEGORY_TAGS.values() for tag in tags
    )
    for reason in TAGS_NOT_ASSIGNED_TO_A_CATEGORY.values():
        assert reason.strip()


def test_nine_of_eleven_categories_have_no_attested_tag_in_this_tree() -> None:
    """المرجعُ يحسم بابَي البنية المُثبَتَين، وما عداهما يُقال بعلّته لا بتخمين."""

    assert set(CATEGORY_TAGS) == {
        ClassificationCategory.MASDAR,
        ClassificationCategory.MUSHTAQQ,
    }


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
    assert "MASAQ" in rendered
    for outcome in _REPORT.unresolved_by_cause:
        assert outcome.name in rendered


def test_a_check_outside_the_closed_vocabulary_is_refused() -> None:
    with pytest.raises(ClassificationCoverageError):
        AnalysisCheck(
            category=ClassificationCategory.MABNI,
            question=AnalysisQuestion.CATEGORY,
            outcome="طابق_المرجع",  # type: ignore[arg-type]
        )
    with pytest.raises(ClassificationCoverageError):
        AnalysisCheck(
            category=ClassificationCategory.MABNI,
            question="CATEGORY",  # type: ignore[arg-type]
            outcome=AnalysisOutcome.MATCHED_THE_REFERENCE,
        )
