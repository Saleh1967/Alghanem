"""اختباراتُ مقام الجذوع وكواشفِ العامل والمعمول، بأسطرٍ مُصرَّحٍ باصطناعها.

`SyntheticLinesAreDeclaredNotHidden`: الصفوفُ هنا **مُصطنَعة**، تُحاكي بنيةَ
الصفّ وحدَها؛ ولا يخرج منها رقمٌ عن MASAQ البتّة. والتغطيةُ ٩٩٫٦٨٣٨٪ والبقيّةُ
٢٤٦ لا تُقاسان إلّا من البايتات المُبصَّمة، واختبارُهما الواحدُ يُفعَّل حين
تكون في `corpora/MASAQ.csv` أو في `ALGHANEM_MASAQ_PATH`.
"""

from __future__ import annotations

import pytest

from alghanem.arabic.irab_column_census import SURA_COLUMN, VERSE_COLUMN
from alghanem.arabic.irab_column_preregistration import (
    ANCHOR_COLUMN_NAME,
    SEGMENT_INDEX_COLUMN_NAME,
    SYNTACTIC_ROLE_COLUMN,
    WORD_KEY_COLUMN_NAME,
    IrabPreregistrationError,
    RegistrationStanding,
    figures_for_column,
)
from alghanem.arabic.irab_operator_census import (
    ARRIVING_RESIDUE_STEMS,
    ARRIVING_RESIDUE_VERSES,
    IRAB_OPERATOR_CENSUS_NAMED_RESIDUALS,
    DependentStanding,
    IrabOperatorCensusError,
    census_from_bytes,
    measure_relations,
    measure_residue,
    read_stem_coverage,
    stem_positions,
    stem_records,
    unroled_stem_positions,
)
from alghanem.arabic.irab_operator_preregistration import (
    ACCEPTANCE_THRESHOLD_PERCENTAGE,
    ARRIVING_RESIDUE_ACCOUNT,
    ARRIVING_ROLE_COVERAGE_ON_STEMS,
    ARRIVING_STEM_TOTAL,
    DEPENDENT_ROLE_VALUES,
    IRAB_OPERATOR_PREREGISTRATION_DIGEST,
    IRAB_OPERATOR_PREREGISTRATION_NAMED_RESIDUALS,
    NEUTRAL_ROLE_VALUES,
    OPERATOR_CENSUS_COLUMNS,
    OPERATOR_ROLE_VALUES,
    PRE_MEASUREMENT_EXPECTATION,
    STEM_DENOMINATOR,
    STEM_MORPH_TYPE,
    ArrivingResidueAccount,
    ArrivingStemCoverage,
    DeclaredDenominator,
    ResiduePattern,
    RoleDetector,
    RoleSide,
    detector_for_value,
    operator_preregistration_digest,
    role_side_of,
)
from alghanem.arabic.masaq_corpus_deposit import (
    MASAQ_RELATIVE_PATH,
    masaq_bytes_are_resolvable,
    masaq_records,
    read_masaq_bytes,
)


def _row(
    *,
    sura: str,
    verse: str,
    word: str,
    segment: str = "1",
    morph_type: str = STEM_MORPH_TYPE,
    role: str = "",
) -> dict[str, str]:
    """صفٌّ مُصطنَعٌ واحد؛ بنيةً لا مدوَّنة."""

    return {
        ANCHOR_COLUMN_NAME: morph_type,
        SYNTACTIC_ROLE_COLUMN: role,
        SURA_COLUMN: sura,
        VERSE_COLUMN: verse,
        WORD_KEY_COLUMN_NAME: word,
        SEGMENT_INDEX_COLUMN_NAME: segment,
    }


SYNTHETIC_RECORDS: tuple[dict[str, str], ...] = (
    # آيةٌ ١:١ — عاملٌ ثمّ معمولُه على مسافة كلمةٍ واحدة، ولاحقةٌ ليست جذعًا.
    _row(sura="1", verse="1", word="1", role="حرف جر"),
    _row(sura="1", verse="1", word="2", role="اسم مجرور"),
    _row(sura="1", verse="1", word="2", segment="2", morph_type="Suffix", role=""),
    # آيةٌ ١:٢ — جذعٌ واحدٌ بلا دورٍ وبقيّتُها مُغطّاة: سهوٌ موضعيّ.
    _row(sura="1", verse="2", word="1", role="فعل ماضٍ"),
    _row(sura="1", verse="2", word="2", role=""),
    _row(sura="1", verse="2", word="3", role="فاعل"),
    # آيةٌ ١:٣ — لا جذعَ فيها حمل دورًا: آيةٌ مُهمَلةٌ بأكملها.
    _row(sura="1", verse="3", word="1", role=""),
    _row(sura="1", verse="3", word="2", role=""),
    # آيةٌ ١:٤ — جذعان بلا دورٍ وفيها مُغطًّى: لا هذا ولا ذاك.
    _row(sura="1", verse="4", word="1", role="حرف عطف"),
    _row(sura="1", verse="4", word="2", role=""),
    _row(sura="1", verse="4", word="3", role=""),
    # آيةٌ ٢:١ — معمولٌ لا عاملَ في آيته البتّة.
    _row(sura="2", verse="1", word="1", role="مفعول به"),
)
"""اثنا عشرَ صفًّا مُصطنَعًا: أربعةُ أنماطٍ للبقيّة، ومعمولٌ بلا عامل."""


def test_the_registration_is_declared_weaker_than_prior_to_the_number() -> None:
    """منزلةُ التسجيل `مُصاغ_بعد_الرقم`، ومخلَّفاتُه تقول ذلك صراحةً."""

    from alghanem.arabic.irab_column_preregistration import STANDING

    assert STANDING is RegistrationStanding.FORMULATED_AFTER_THE_NUMBER
    assert "ThisRegistrationIsNotPriorToTheNumber" in (
        IRAB_OPERATOR_PREREGISTRATION_NAMED_RESIDUALS
    )
    assert "TheFiguresArrivedFromTheHolderOfTheBytes" in (
        IRAB_OPERATOR_PREREGISTRATION_NAMED_RESIDUALS
    )


def test_the_preregistration_digest_is_derived_from_its_content() -> None:
    assert operator_preregistration_digest() == IRAB_OPERATOR_PREREGISTRATION_DIGEST
    assert len(IRAB_OPERATOR_PREREGISTRATION_DIGEST) == 64


def test_a_ratio_without_a_declared_denominator_is_refused() -> None:
    """`ADenominatorIsDeclaredNotAssumed`: نسبةٌ بلا مقامٍ لا تُبنى أصلًا."""

    with pytest.raises(IrabPreregistrationError):
        DeclaredDenominator(
            name="الجذوع", column=ANCHOR_COLUMN_NAME, value="Stem", counting_rule="  "
        )
    with pytest.raises(IrabPreregistrationError):
        ArrivingStemCoverage(
            column=SYNTACTIC_ROLE_COLUMN,
            denominator=STEM_DENOMINATOR,
            denominator_count=10,
            covered_count=11,
            declared_percentage="99.00",
        )
    with pytest.raises(IrabPreregistrationError):
        ArrivingStemCoverage(
            column=SYNTACTIC_ROLE_COLUMN,
            denominator=STEM_DENOMINATOR,
            denominator_count=10,
            covered_count=10,
            declared_percentage="100",
        )


def test_the_denominator_is_the_stems_not_the_segments() -> None:
    """المقامُ الجذوعُ وحدَها؛ ومقامُ المقاطع يُخرِج نسبةً أخرى فيُسقَط."""

    assert STEM_DENOMINATOR.column == ANCHOR_COLUMN_NAME
    assert STEM_DENOMINATOR.value == STEM_MORPH_TYPE

    reading = read_stem_coverage(SYNTHETIC_RECORDS)

    stems = stem_records(SYNTHETIC_RECORDS)
    assert reading.denominator_count == len(stems) == len(SYNTHETIC_RECORDS) - 1
    assert reading.denominator_count != len(SYNTHETIC_RECORDS)
    assert reading.denominator is STEM_DENOMINATOR
    assert reading.covered_count + reading.residue_count == reading.denominator_count
    assert reading.preregistration_digest == IRAB_OPERATOR_PREREGISTRATION_DIGEST


def test_the_arriving_coverage_and_residue_are_one_arithmetic_not_three_numbers() -> (
    None
):
    """٧٧٬٧٩٧ و٧٧٬٥٥١ و٢٤٦ حسابٌ واحد؛ ولا يُكتَب ثالثُها رقمًا مستقلًّا."""

    coverage = ARRIVING_ROLE_COVERAGE_ON_STEMS
    assert coverage.denominator_count == ARRIVING_STEM_TOTAL
    assert coverage.residue_count == ARRIVING_RESIDUE_STEMS == 246
    measured = 100.0 * coverage.covered_count / coverage.denominator_count
    assert f"{measured:.{coverage.decimal_places}f}" == coverage.declared_percentage
    assert measured >= float(ACCEPTANCE_THRESHOLD_PERCENTAGE)


def test_the_residue_account_sums_to_the_arriving_verses_and_names_the_rest() -> None:
    """١٦٤ + ٤ + ٢٢ = ١٩٠ آية؛ والجذوعُ غيرُ المُصرَّح بها `None` لا صفر."""

    assert sum(account.verses for account in ARRIVING_RESIDUE_ACCOUNT) == (
        ARRIVING_RESIDUE_VERSES
    )
    assert ARRIVING_RESIDUE_VERSES == 190
    by_pattern = {account.pattern: account for account in ARRIVING_RESIDUE_ACCOUNT}
    assert len(by_pattern) == len(ResiduePattern)
    single = by_pattern[ResiduePattern.SINGLE_UNROLED_STEM_IN_VERSE]
    assert single.verses == single.stems == 164
    assert by_pattern[ResiduePattern.WHOLLY_UNANNOTATED_VERSE].stems is None
    assert by_pattern[ResiduePattern.NEITHER_PATTERN].stems is None
    undeclared = ARRIVING_RESIDUE_STEMS - 164
    assert undeclared == 82
    assert "AnUndeclaredSplitIsNotAZero" in (
        IRAB_OPERATOR_PREREGISTRATION_NAMED_RESIDUALS
    )


def test_a_residue_account_with_fewer_stems_than_verses_is_refused() -> None:
    """لكلّ آيةٍ في البقيّة جذعٌ واحدٌ فأكثرُ بلا دور؛ وأقلُّ من ذلك يُرفَض."""

    with pytest.raises(IrabPreregistrationError):
        ArrivingResidueAccount(
            pattern=ResiduePattern.NEITHER_PATTERN, verses=5, stems=4
        )


def test_the_detectors_import_their_figures_rather_than_restate_them() -> None:
    """رقمٌ مُجمَّدٌ مرّتين رقمان يفترقان؛ فالكواشفُ تستورد أعدادَها."""

    claimed = {
        figure.value: figure.claimed_count
        for figure in figures_for_column(SYNTACTIC_ROLE_COLUMN)
        if figure.value is not None
    }
    for value in OPERATOR_ROLE_VALUES + DEPENDENT_ROLE_VALUES + NEUTRAL_ROLE_VALUES:
        detector = detector_for_value(value)
        assert detector is not None
        assert detector.claimed_segment_count == claimed[value]
    assert OPERATOR_ROLE_VALUES == ("حرف جر", "فعل ماضٍ", "فعل مضارع")
    assert DEPENDENT_ROLE_VALUES == ("اسم مجرور", "فاعل", "مفعول به")
    assert NEUTRAL_ROLE_VALUES == ("حرف غير عامل", "حرف عطف")


def test_an_unfrozen_role_is_outside_the_detectors_not_pushed_into_a_side() -> None:
    """ما لم يُجمَّد يخرج «خارج الكواشف»؛ وهو حدُّ الأداة لا خبرٌ عن العربية."""

    assert role_side_of("حرف جر") is RoleSide.OPERATOR
    assert role_side_of("مضاف إليه") is RoleSide.OUTSIDE_THE_DETECTORS
    assert detector_for_value("مضاف إليه") is None
    with pytest.raises(IrabPreregistrationError):
        RoleDetector(
            value="مضاف إليه",
            side=RoleSide.OUTSIDE_THE_DETECTORS,
            claimed_segment_count=9_123,
        )


def test_the_phrase_column_is_not_among_the_columns_this_census_reads() -> None:
    """`ThePhraseColumnIsNotUsed`: لا يُقرأ عمودٌ منحازٌ بنيويًّا هنا."""

    assert "Phrase" not in OPERATOR_CENSUS_COLUMNS
    assert "ThePhraseColumnIsNotUsed" in IRAB_OPERATOR_PREREGISTRATION_NAMED_RESIDUALS
    assert "TheMarkerIsNotInferredFromTheCase" in (
        IRAB_OPERATOR_PREREGISTRATION_NAMED_RESIDUALS
    )


def test_a_missing_column_stops_the_count_rather_than_zeroing_it() -> None:
    """عمودٌ غائبٌ يُوقِف العدَّ؛ فالصفرُ يمرّ كأنّه قياس، والخطأُ يقف."""

    with pytest.raises(IrabOperatorCensusError):
        stem_records(({ANCHOR_COLUMN_NAME: STEM_MORPH_TYPE},))
    with pytest.raises(IrabOperatorCensusError):
        stem_records(())
    with pytest.raises(IrabOperatorCensusError):
        census_from_bytes(b"Sura_No,Verse_No\n1,2\n")


def test_the_residue_is_classified_by_the_two_patterns_and_a_declared_third() -> None:
    """آيةٌ بجذعٍ واحدٍ بلا دور، وآيةٌ مُهمَلةٌ بأكملها، وبابٌ ثالثٌ مُعلَن."""

    census = measure_residue(SYNTHETIC_RECORDS)

    assert census.verses_by_pattern == {
        ResiduePattern.SINGLE_UNROLED_STEM_IN_VERSE.name: 1,
        ResiduePattern.WHOLLY_UNANNOTATED_VERSE.name: 1,
        ResiduePattern.NEITHER_PATTERN.name: 1,
    }
    assert census.stems_by_pattern == {
        ResiduePattern.SINGLE_UNROLED_STEM_IN_VERSE.name: 1,
        ResiduePattern.WHOLLY_UNANNOTATED_VERSE.name: 2,
        ResiduePattern.NEITHER_PATTERN.name: 2,
    }
    assert census.residue_stems == len(unroled_stem_positions(SYNTHETIC_RECORDS)) == 5
    assert census.residue_verses == 3
    assert census.stems_per_verse == pytest.approx(5 / 3)
    assert census.residue_stems == read_stem_coverage(SYNTHETIC_RECORDS).residue_count


def test_a_relation_is_not_counted_across_the_verse_boundary() -> None:
    """`ARelationNeedsTwoPresentTerms`: معمولُ ٢:١ لا يُوصَل بعامل ١:٤."""

    census = measure_relations(SYNTHETIC_RECORDS)

    assert census.standings[DependentStanding.HAS_PRECEDING_OPERATOR.name] == 2
    assert census.standings[DependentStanding.HAS_FOLLOWING_OPERATOR.name] == 0
    assert census.standings[DependentStanding.NO_OPERATOR_OBSERVED.name] == 1
    assert census.dependents == 3
    assert census.decided == 2
    assert census.distances == {1: 1, 2: 1}
    assert census.most_common_distance == 1
    assert "ARelationNeedsTwoPresentTerms" in IRAB_OPERATOR_CENSUS_NAMED_RESIDUALS


def test_a_following_operator_is_a_third_standing_not_an_absence() -> None:
    """المعمولُ الذي عاملُه بعده يُسمّى، ولا يُجمَع مع «لا عامل مرصود»."""

    records = (
        _row(sura="3", verse="1", word="1", role="مفعول به"),
        _row(sura="3", verse="1", word="3", role="فعل ماضٍ"),
    )

    census = measure_relations(records)

    assert census.standings[DependentStanding.HAS_FOLLOWING_OPERATOR.name] == 1
    assert census.standings[DependentStanding.NO_OPERATOR_OBSERVED.name] == 0
    assert census.distances == {2: 1}
    assert census.preceding_share_of_decided == 0.0


def test_an_unreadable_word_key_is_counted_rather_than_dropped_in_silence() -> None:
    """مفتاحُ كلمةٍ لا يُقرأ عددًا يُعَدُّ في حقلٍ باسمه ولا يدخل مسافة."""

    records = (
        _row(sura="4", verse="1", word="لا عدد", role="حرف جر"),
        _row(sura="4", verse="1", word="2", role="اسم مجرور"),
    )

    census = measure_relations(records)

    assert census.unreadable_word_keys == 1
    assert census.standings[DependentStanding.NO_OPERATOR_OBSERVED.name] == 1
    assert census.distances == {}
    assert census.most_common_distance is None
    assert [position.word_number for position in stem_positions(records)] == [None, 2]
    assert "AnUnreadableWordKeyIsCountedNotDropped" in (
        IRAB_OPERATOR_CENSUS_NAMED_RESIDUALS
    )


def test_the_expectation_is_written_before_the_relation_was_measured() -> None:
    """التوقّعُ قابلٌ للتكذيب، ومكتوبٌ قبل أن يُقاس اقترانُ الطرفين."""

    assert "PreMeasurementExpectation" in PRE_MEASUREMENT_EXPECTATION
    assert "AnOperatorTagIsNotAProvenGovernment" in PRE_MEASUREMENT_EXPECTATION
    assert "CoverageIsNotCorrectness" in (IRAB_OPERATOR_PREREGISTRATION_NAMED_RESIDUALS)
    assert "CompleteInductionIsCorpusBounded" in (
        IRAB_OPERATOR_PREREGISTRATION_NAMED_RESIDUALS
    )


@pytest.mark.skipif(
    not masaq_bytes_are_resolvable(),
    reason=(
        f"no MASAQ bytes resolve from {MASAQ_RELATIVE_PATH} nor from a "
        "declared path; the stem coverage, the 246-stem residue and the "
        "operator/dependent relations are derived only from the "
        "fingerprinted bytes. Bytes that resolve and differ are not skipped: "
        "they fail"
    ),
)
def test_the_stem_coverage_and_residue_are_rederived_from_the_deposited_bytes() -> None:
    """يُعرَض المُدَّعى والمُشتَقّ معًا؛ ولا يُعدَّل رقمٌ ليُطابِق ما قِيس."""

    records = masaq_records(read_masaq_bytes())
    coverage, residue, relations = (
        read_stem_coverage(records),
        measure_residue(records),
        measure_relations(records),
    )

    assert coverage.denominator_count == ARRIVING_STEM_TOTAL, (
        "مقامُ الجذوع خالف المُدَّعى قبل قراءة نسبةٍ واحدة: "
        f"{coverage.denominator_count} لا {ARRIVING_STEM_TOTAL}"
    )
    assert coverage.agrees_with_the_declared, (
        "التغطيةُ على مقام الجذوع خالفت المُدَّعى: "
        f"{coverage.measured_percentage:.4f}٪ لا {coverage.declared_percentage}٪"
    )
    assert coverage.meets_threshold
    assert coverage.residue_count == ARRIVING_RESIDUE_STEMS
    assert residue.residue_stems == coverage.residue_count
    assert residue.residue_verses == ARRIVING_RESIDUE_VERSES
    assert relations.dependents == sum(relations.standings.values())
