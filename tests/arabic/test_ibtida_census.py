"""اختباراتُ مقام الابتداء وفئاتِه، بأسطرٍ مُصرَّحٍ باصطناعها.

`SyntheticLinesAreDeclaredNotHidden`: الصفوفُ هنا **مُصطنَعة**، تُحاكي بنيةَ
الصفّ وحدَها؛ ولا يخرج منها رقمٌ عن MASAQ البتّة. والمقامُ ١١٬٣٤٩ والأرقامُ
الثمانيةُ لا تُقاس إلّا من البايتات المُبصَّمة، واختبارُها الواحدُ يُفعَّل حين
تكون في `corpora/MASAQ.csv` أو في `ALGHANEM_MASAQ_PATH`.
"""

from __future__ import annotations

from dataclasses import fields

import pytest

from alghanem.arabic.ibtida_census import (
    ACCUSATIVE_CASE_VALUE,
    ARRIVING_INCHOATIVE_TOTAL,
    IBTIDA_CENSUS_NAMED_RESIDUALS,
    AccusativeMubtadaCensus,
    GovernorCensus,
    GovernorStanding,
    IbtidaCensusError,
    InchoativeDenominatorReading,
    InchoativeRelationCensus,
    MubtadaStanding,
    SentenceClassCensus,
    census_from_bytes,
    classify_positions,
    inchoative_positions,
    measure_accusative_mubtada,
    measure_governors,
    measure_inchoative_relations,
    read_inchoative_denominator,
    stem_records,
)
from alghanem.arabic.ibtida_preregistration import (
    ARRIVING_INCHOATIVE_POSITIONS,
    ARRIVING_MUBTADA_BREAKDOWN,
    IBTIDA_CENSUS_COLUMNS,
    IBTIDA_PREREGISTRATION_DIGEST,
    IBTIDA_PREREGISTRATION_NAMED_RESIDUALS,
    INCHOATIVE_POSITION_DENOMINATOR,
    INCHOATIVE_POSITION_TOTAL,
    INCHOATIVE_POSITION_VALUES,
    NAMED_RESIDUES,
    PRE_MEASUREMENT_EXPECTATION,
    THE_RETRACTED_TOTAL_DENIAL,
    ArrivingInchoativeFigure,
    ArrivingMubtadaBreakdown,
    NamedResidue,
    PositionSide,
    ResidueDerivation,
    SentenceClass,
    class_of_value,
    figure_for_value,
    figures_of_class,
    ibtida_preregistration_digest,
    side_of_value,
)
from alghanem.arabic.irab_column_census import SURA_COLUMN, VERSE_COLUMN
from alghanem.arabic.irab_column_preregistration import (
    ANCHOR_COLUMN_NAME,
    ARRIVING_SEGMENT_TOTAL,
    CASE_MOOD_COLUMN,
    CASE_MOOD_MARKER_COLUMN,
    PHRASAL_FUNCTION_COLUMN,
    SEGMENT_INDEX_COLUMN_NAME,
    SYNTACTIC_ROLE_COLUMN,
    WORD_KEY_COLUMN_NAME,
    IrabCountingRule,
    IrabPreregistrationError,
    RegistrationStanding,
    figures_for_column,
)
from alghanem.arabic.irab_operator_preregistration import (
    ARRIVING_STEM_TOTAL,
    STEM_MORPH_TYPE,
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
    case_mood: str = "مرفوع",
    marker: str = "الضمة",
) -> dict[str, str]:
    """صفٌّ مُصطنَعٌ واحد؛ بنيةً لا مدوَّنة."""

    return {
        ANCHOR_COLUMN_NAME: morph_type,
        SYNTACTIC_ROLE_COLUMN: role,
        CASE_MOOD_COLUMN: case_mood,
        CASE_MOOD_MARKER_COLUMN: marker,
        SURA_COLUMN: sura,
        VERSE_COLUMN: verse,
        WORD_KEY_COLUMN_NAME: word,
        SEGMENT_INDEX_COLUMN_NAME: segment,
    }


SYNTHETIC_RECORDS: tuple[dict[str, str], ...] = (
    # ١:١ — مجرَّدة تامّة: مبتدأ وخبرُه.
    _row(sura="1", verse="1", word="1", role="مبتدأ"),
    _row(sura="1", verse="1", word="2", role="خبر"),
    _row(sura="1", verse="1", word="2", segment="2", morph_type="Suffix"),
    # ١:٢ — مبتدأ بلا خبرٍ موسومٍ في آيته.
    _row(sura="1", verse="2", word="1", role="مبتدأ", marker="السكون"),
    _row(sura="1", verse="2", word="2", role="مضاف إليه", case_mood="مجرور"),
    # ١:٣ — مبتدأ له خبران مرشَّحان.
    _row(sura="1", verse="3", word="1", role="مبتدأ"),
    _row(sura="1", verse="3", word="2", role="خبر"),
    _row(sura="1", verse="3", word="3", role="خبر"),
    # ١:٤ — منسوخةٌ بحرف: ناسخٌ واسمُه وخبرُه.
    _row(sura="1", verse="4", word="1", role="حرف ناسخ", case_mood="مبني"),
    _row(sura="1", verse="4", word="2", role="اسم حرف ناسخ"),
    _row(sura="1", verse="4", word="3", role="خبر حرف ناسخ"),
    # ١:٥ — ناسخٌ بلا اسمٍ موسومٍ في آيته.
    _row(sura="1", verse="5", word="1", role="حرف ناسخ", case_mood="مبني"),
    # ١:٦ — منسوخةٌ بفعل: اسمٌ بلا خبرٍ موسوم.
    _row(sura="1", verse="6", word="1", role="اسم فعل ناسخ"),
    # ١:٧ — اسمُ لا النافية للجنس: فئةٌ لا قيمةَ خبرٍ لها في العمود.
    _row(sura="1", verse="7", word="1", role="اسم لا النافية للجنس", case_mood="مبني"),
    # ١:٨ — مبتدأ منصوب: يُفحَص فرديًّا ولا يُلخَّص.
    _row(
        sura="1",
        verse="8",
        word="1",
        role="مبتدأ",
        case_mood=ACCUSATIVE_CASE_VALUE,
        marker="الفتحة",
    ),
    # ٢:١ — خبرٌ في آيةٍ أخرى؛ ولا يُوصَل بمبتدأ ١:٢.
    _row(sura="2", verse="1", word="1", role="خبر"),
)
"""سبعةَ عشرَ صفًّا مُصطنَعًا: المنازلُ الثلاث، وناسخٌ بلا اسم، ومبتدأ منصوب."""


def test_the_registration_is_declared_weaker_than_prior_to_the_number() -> None:
    """منزلةُ التسجيل `مُصاغ_بعد_الرقم`، ومخلَّفاتُه تقول ذلك صراحةً."""

    from alghanem.arabic.irab_column_preregistration import STANDING

    assert STANDING is RegistrationStanding.FORMULATED_AFTER_THE_NUMBER
    assert "ThisRegistrationIsNotPriorToTheNumber" in (
        IBTIDA_PREREGISTRATION_NAMED_RESIDUALS
    )
    assert "TheFiguresArrivedFromTheHolderOfTheBytes" in (
        IBTIDA_PREREGISTRATION_NAMED_RESIDUALS
    )
    assert ibtida_preregistration_digest() == IBTIDA_PREREGISTRATION_DIGEST
    assert len(IBTIDA_PREREGISTRATION_DIGEST) == 64


def test_a_figure_without_a_declared_denominator_is_refused() -> None:
    """`ADenominatorIsDeclaredNotAssumed`: رقمٌ بلا مقامه لا يُبنى أصلًا."""

    with pytest.raises(IrabPreregistrationError):
        ArrivingMubtadaBreakdown(
            positions=0,
            declared_nominative_percentage="99.5",
            accusative_positions=3,
            invariable_positions=2_354,
            declinable_positions=1_219,
            top_marker_label="السكون",
            top_marker_positions=1_274,
        )
    with pytest.raises(IrabPreregistrationError):
        ArrivingMubtadaBreakdown(
            positions=3_598,
            declared_nominative_percentage="99.5",
            accusative_positions=3,
            invariable_positions=2_354,
            declinable_positions=1_219,
            top_marker_label="السكون",
            top_marker_positions=4_000,
        )
    with pytest.raises(IrabPreregistrationError):
        ArrivingMubtadaBreakdown(
            positions=3_598,
            declared_nominative_percentage="99",
            accusative_positions=3,
            invariable_positions=2_354,
            declinable_positions=1_219,
            top_marker_label="السكون",
            top_marker_positions=1_274,
        )


def test_the_denominator_is_the_inchoative_positions_not_the_stems() -> None:
    """المقامُ ١١٬٣٤٩ لا ٧٧٬٧٩٧ ولا ١٥٧٬٦٧٧؛ وثلاثتُها ثلاثةُ مقامات."""

    assert INCHOATIVE_POSITION_TOTAL == 11_349
    assert INCHOATIVE_POSITION_TOTAL != ARRIVING_STEM_TOTAL == 77_797
    assert INCHOATIVE_POSITION_TOTAL != ARRIVING_SEGMENT_TOTAL == 157_677
    assert INCHOATIVE_POSITION_DENOMINATOR.column == SYNTACTIC_ROLE_COLUMN
    assert ARRIVING_INCHOATIVE_TOTAL == INCHOATIVE_POSITION_TOTAL

    reading = read_inchoative_denominator(SYNTHETIC_RECORDS)

    assert reading.denominator is INCHOATIVE_POSITION_DENOMINATOR
    assert reading.denominator_count == len(inchoative_positions(SYNTHETIC_RECORDS))
    assert reading.denominator_count < reading.stem_count < reading.segment_count
    assert reading.stem_count == len(stem_records(SYNTHETIC_RECORDS))
    assert reading.segment_count == len(SYNTHETIC_RECORDS)
    assert not reading.agrees_with_the_declared_total
    assert reading.preregistration_digest == IBTIDA_PREREGISTRATION_DIGEST


def test_the_denominator_is_the_sum_of_the_eight_not_a_ninth_figure() -> None:
    """المقامُ مجموعُ الثمانية؛ ورقمٌ تاسعٌ مكتوبٌ رقمان يفترقان."""

    assert len(ARRIVING_INCHOATIVE_POSITIONS) == 8
    assert (
        sum(figure.claimed_segment_count for figure in ARRIVING_INCHOATIVE_POSITIONS)
        == INCHOATIVE_POSITION_TOTAL
    )
    mubtada = figure_for_value("مبتدأ")
    assert mubtada is not None and mubtada.imported_from_the_first_freeze
    claimed = {
        figure.value: figure.claimed_count
        for figure in figures_for_column(SYNTACTIC_ROLE_COLUMN)
        if figure.value is not None
    }
    assert mubtada.claimed_segment_count == claimed["مبتدأ"] == 3_598
    assert ARRIVING_MUBTADA_BREAKDOWN.positions == mubtada.claimed_segment_count


def test_a_ratio_is_never_taken_over_a_denominator_it_was_not_declared_on() -> None:
    """نسبةُ السكون من المبتدأ وحدَه — ٣٥٫٤٪ — لا من الجذوع ولا من المقاطع."""

    breakdown = ARRIVING_MUBTADA_BREAKDOWN
    assert breakdown.top_marker_label == "السكون"
    assert f"{100 * breakdown.top_marker_share:.1f}" == "35.4"
    assert breakdown.build_total == 3_573
    assert breakdown.unaccounted_by_build == 25
    assert breakdown.nominative_positions_if_only_the_accusative_are_excepted == 3_595
    assert "AnInchoativeGovernorIsSemanticNotLexical" in (
        IBTIDA_PREREGISTRATION_NAMED_RESIDUALS
    )


def test_the_four_classes_are_exclusive_and_exhaustive() -> None:
    """لا موضعَ في فئتين، ولا موضعَ خارجَ الأربع؛ ومجموعُها المقامُ بعينه."""

    seen: list[str] = []
    total = 0
    for sentence_class in SentenceClass:
        for figure in figures_of_class(sentence_class):
            seen.append(figure.value)
            total += figure.claimed_segment_count
    assert sorted(seen) == sorted(INCHOATIVE_POSITION_VALUES)
    assert len(seen) == len(set(seen)) == 8
    assert total == INCHOATIVE_POSITION_TOTAL
    assert class_of_value("مبتدأ") is SentenceClass.BARE
    assert class_of_value("خبر حرف ناسخ") is SentenceClass.NASIKH_PARTICLE
    assert class_of_value("مضاف إليه") is None
    assert side_of_value("خبر") is PositionSide.PREDICATE
    assert side_of_value("مضاف إليه") is None
    assert (
        figures_of_class(SentenceClass.LA_OF_ABSOLUTE_NEGATION)[0].side
        is PositionSide.INCHOATIVE
    )
    assert (
        len(
            [
                figure
                for figure in figures_of_class(SentenceClass.LA_OF_ABSOLUTE_NEGATION)
                if figure.side is PositionSide.PREDICATE
            ]
        )
        == 0
    )


def test_the_measured_classes_conserve_the_measured_denominator() -> None:
    """اختبارُ الحفظ: الفئاتُ الأربعُ + ما خرج عن المقام = الجذوعُ كلُّها."""

    census = classify_positions(SYNTHETIC_RECORDS)
    reading = read_inchoative_denominator(SYNTHETIC_RECORDS)

    assert census.conserves_the_denominator
    assert census.positions_in_the_four_classes == reading.denominator_count
    assert (
        census.positions_in_the_four_classes + census.stems_outside_the_denominator
        == reading.stem_count
    )
    assert census.positions_by_class == {
        SentenceClass.BARE.name: 8,
        SentenceClass.NASIKH_PARTICLE.name: 2,
        SentenceClass.NASIKH_VERB.name: 1,
        SentenceClass.LA_OF_ABSOLUTE_NEGATION.name: 1,
    }


def test_a_relation_is_not_counted_across_the_verse_boundary() -> None:
    """`ARelationNeedsTwoPresentTerms`: خبرُ ٢:١ لا يُوصَل بمبتدأ ١:٢."""

    census = measure_inchoative_relations(SYNTHETIC_RECORDS)

    assert census.standings[MubtadaStanding.HAS_ONE_TAGGED_PREDICATE.name] == 2
    assert census.standings[MubtadaStanding.NO_TAGGED_PREDICATE.name] == 3
    assert census.standings[MubtadaStanding.MORE_THAN_ONE_CANDIDATE.name] == 1
    assert census.counted_inchoatives == 6
    assert census.inchoatives == 7
    assert census.inchoatives_whose_class_has_no_predicate_value == 1
    assert [
        reference.split(" — ")[0] for reference in census.positions_without_a_predicate
    ] == ["1:2:1", "1:6:1", "1:8:1"]
    assert "ARelationNeedsTwoPresentTerms" in IBTIDA_CENSUS_NAMED_RESIDUALS


def test_the_absent_predicate_is_named_by_its_place_not_summed_into_a_zero() -> None:
    """«لا خبرَ موسوم» تُسمّى بموضعها؛ ولا تُجمَع مع «له أكثرُ من خبر»."""

    census = measure_inchoative_relations(SYNTHETIC_RECORDS)

    assert (
        len(census.positions_without_a_predicate)
        == (census.standings[MubtadaStanding.NO_TAGGED_PREDICATE.name])
    )
    assert "1:2:1 — مبتدأ" in census.positions_without_a_predicate


def test_a_governor_without_a_tagged_name_falsifies_the_third_expectation() -> None:
    """لكل ناسخٍ اسمٌ في آيته؛ والخارجُ عن ذلك يُسمّى بموضعه لا يُبتلَع."""

    census = measure_governors(SYNTHETIC_RECORDS)

    assert census.standings[GovernorStanding.HAS_A_TAGGED_NAME.name] == 1
    assert census.standings[GovernorStanding.NO_TAGGED_NAME.name] == 1
    assert census.governors_without_a_name == ("1:5:1 — حرف ناسخ",)
    assert census.absent_values == ("فعل ناسخ",)
    assert census.governors_by_value == {"حرف ناسخ": 2}


def test_the_accusative_mubtada_is_returned_position_by_position() -> None:
    """ثلاثةٌ عددٌ يُفحَص فرديًّا؛ فتُخرَج المواضعُ لا العددُ وحدَه."""

    census = measure_accusative_mubtada(SYNTHETIC_RECORDS)

    assert census.references == ("1:8:1",)
    assert census.markers == ("الفتحة",)
    assert census.count == len(census.references)
    residue = NAMED_RESIDUES[0]
    assert residue.name == "مبتدأ منصوب"
    assert residue.claimed_size == 3
    assert residue.requires_individual_inspection


def test_the_named_residues_are_derived_where_they_can_be_and_named_where_not() -> None:
    """١٬١٥٧ و٤٠٠ مُشتقّان طرحًا؛ و١٨٧ وصل عددًا، والرابعةُ بلا عدد."""

    by_name = {residue.name: residue for residue in NAMED_RESIDUES}
    particle = by_name["فارق اسم الحرف الناسخ وخبره"]
    verb = by_name["فارق اسم الفعل الناسخ وخبره"]
    assert particle.derivation is ResidueDerivation.DERIVED_BY_SUBTRACTION
    assert particle.claimed_size == 1_157
    assert verb.claimed_size == 400
    assert by_name["فارق مبتدأ/خبر"].derivation is ResidueDerivation.ARRIVED_AS_A_COUNT
    assert by_name["فارق مبتدأ/خبر"].claimed_size == 187
    fronted = by_name["لا وسمَ لخبرٍ مقدَّم"]
    assert fronted.derivation is ResidueDerivation.NAMED_WITHOUT_A_COUNT
    assert fronted.claimed_size is None
    assert "AnUndeclaredSplitIsNotAZero" in IBTIDA_PREREGISTRATION_NAMED_RESIDUALS

    with pytest.raises(IrabPreregistrationError):
        NamedResidue(
            name="فارقٌ لا يُشتَقّ",
            description="طرفاه مُسمَّيان وحاصلُهما غيرُ المكتوب",
            claimed_size=1_000,
            derivation=ResidueDerivation.DERIVED_BY_SUBTRACTION,
            minuend_value="اسم حرف ناسخ",
            subtrahend_value="خبر حرف ناسخ",
            requires_individual_inspection=False,
        )
    with pytest.raises(IrabPreregistrationError):
        NamedResidue(
            name="بقيّةٌ بلا عددٍ صُفِّرت",
            description="صفرٌ مكانَ «لا مقيسَ له»",
            claimed_size=0,
            derivation=ResidueDerivation.NAMED_WITHOUT_A_COUNT,
            minuend_value=None,
            subtrahend_value=None,
            requires_individual_inspection=False,
        )


def test_an_accuracy_field_is_refused_in_an_output_structure() -> None:
    """لا ذهبَ لعلاقة المبتدأ بخبره؛ فحقلُ دقّةٍ دعوى مرجعٍ لا وجودَ له."""

    forbidden = ("accuracy", "precision", "recall", "f1", "gold", "score")
    for dataclass_type in (
        InchoativeDenominatorReading,
        SentenceClassCensus,
        InchoativeRelationCensus,
        GovernorCensus,
        AccusativeMubtadaCensus,
    ):
        for field in fields(dataclass_type):
            assert not any(marker in field.name.lower() for marker in forbidden)
    assert "NoGoldForTheInchoativeLink" in IBTIDA_CENSUS_NAMED_RESIDUALS
    assert "ARoleTagIsNotALink" in IBTIDA_CENSUS_NAMED_RESIDUALS


def test_the_two_columns_are_not_read_as_one_figure() -> None:
    """«خبر ٢٬٠٥٧» في عمود الدور، و«خبر ١٬٣٩٨» في عمود التركيب؛ عمودان."""

    assert PHRASAL_FUNCTION_COLUMN not in IBTIDA_CENSUS_COLUMNS
    phrasal = {
        figure.value: figure.claimed_count
        for figure in figures_for_column(PHRASAL_FUNCTION_COLUMN)
        if figure.value is not None
    }
    assert phrasal["خبر"] == 1_398
    assert phrasal["خبر حرف ناسخ"] == 783
    assert phrasal["خبر فعل ناسخ"] == 551
    role_khabar = figure_for_value("خبر")
    assert role_khabar is not None
    assert role_khabar.claimed_segment_count == 2_057 != phrasal["خبر"]
    assert "TheTwoColumnsAreNotOneFigure" in IBTIDA_PREREGISTRATION_NAMED_RESIDUALS

    with pytest.raises(IrabPreregistrationError):
        ArrivingInchoativeFigure(
            label="خبر — Phrasal_Function",
            column=PHRASAL_FUNCTION_COLUMN,
            value="خبر",
            sentence_class=SentenceClass.BARE,
            side=PositionSide.PREDICATE,
            claimed_segment_count=1_398,
            counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
            imported_from_the_first_freeze=False,
        )


def test_the_retraction_is_written_in_the_unit_and_its_law_is_enacted() -> None:
    """الاعترافُ مُثبَّتٌ في الوحدة، و`APartialScanForbidsATotalDenial` مسنون."""

    assert "APartialScanForbidsATotalDenial" in (IBTIDA_PREREGISTRATION_NAMED_RESIDUALS)
    assert "TheRetractedTotalDenial" in IBTIDA_PREREGISTRATION_NAMED_RESIDUALS
    assert "٣٬٧٨٥" in THE_RETRACTED_TOTAL_DENIAL
    assert "٤٬٣٥٥" in THE_RETRACTED_TOTAL_DENIAL
    predicates = [
        figure
        for figure in ARRIVING_INCHOATIVE_POSITIONS
        if figure.side is PositionSide.PREDICATE
    ]
    assert sum(figure.claimed_segment_count for figure in predicates) == 3_785
    postponed = figure_for_value("مبتدأ مؤخر")
    assert postponed is not None
    assert 3_785 + postponed.claimed_segment_count == 4_355


def test_the_expectation_is_written_before_the_relation_was_measured() -> None:
    """التوقّعُ ثلاثيٌّ قابلٌ للتكذيب، ومكتوبٌ قبل أن يُقاس اقترانُ الطرفين."""

    assert "PreMeasurementExpectation" in PRE_MEASUREMENT_EXPECTATION
    assert "ARoleTagIsNotALink" in PRE_MEASUREMENT_EXPECTATION
    assert "٢٫٢٥:١" in PRE_MEASUREMENT_EXPECTATION
    assert "١٫٥:١" in PRE_MEASUREMENT_EXPECTATION
    particle_name = figure_for_value("اسم حرف ناسخ")
    particle_khabar = figure_for_value("خبر حرف ناسخ")
    verb_name = figure_for_value("اسم فعل ناسخ")
    verb_khabar = figure_for_value("خبر فعل ناسخ")
    assert particle_name is not None and particle_khabar is not None
    assert verb_name is not None and verb_khabar is not None
    particle_ratio = (
        particle_name.claimed_segment_count / particle_khabar.claimed_segment_count
    )
    verb_ratio = verb_name.claimed_segment_count / verb_khabar.claimed_segment_count
    assert f"{particle_ratio:.2f}" == "2.25"
    assert f"{verb_ratio:.2f}" == "1.50"
    assert "CoverageIsNotCorrectness" in IBTIDA_PREREGISTRATION_NAMED_RESIDUALS
    assert "CompleteInductionIsCorpusBounded" in (
        IBTIDA_PREREGISTRATION_NAMED_RESIDUALS
    )


def test_a_missing_column_stops_the_count_rather_than_zeroing_it() -> None:
    """عمودٌ غائبٌ يُوقِف العدَّ؛ فالصفرُ يمرّ كأنّه قياس، والخطأُ يقف."""

    with pytest.raises(IbtidaCensusError):
        stem_records(({ANCHOR_COLUMN_NAME: STEM_MORPH_TYPE},))
    with pytest.raises(IbtidaCensusError):
        stem_records(())
    with pytest.raises(IbtidaCensusError):
        census_from_bytes(b"Sura_No,Verse_No\n1,2\n")


def test_a_frozen_value_absent_from_the_column_is_not_a_zero() -> None:
    """قيمةٌ لم تَرِد تخرج في `absent_values`؛ وذلك خبرٌ عن اسمها لا عن العربية."""

    reading = read_inchoative_denominator(SYNTHETIC_RECORDS)

    assert "مبتدأ مؤخر" in reading.absent_values
    assert "مبتدأ مؤخر" not in reading.counts_by_value
    assert "AClaimedValueAbsentIsNotAZeroCount" in (
        IBTIDA_PREREGISTRATION_NAMED_RESIDUALS
    )


def test_an_unreadable_word_key_is_counted_rather_than_dropped_in_silence() -> None:
    """مفتاحُ كلمةٍ لا يُقرأ عددًا يُعَدُّ في حقلٍ باسمه ويُسمّى موضعُه «؟»."""

    records = (
        _row(sura="9", verse="1", word="لا عدد", role="مبتدأ"),
        _row(sura="9", verse="1", word="2", role="خبر"),
    )

    census = measure_inchoative_relations(records)

    assert census.unreadable_word_keys == 1
    assert census.standings[MubtadaStanding.HAS_ONE_TAGGED_PREDICATE.name] == 1
    assert inchoative_positions(records)[0].reference == "9:1:؟"
    assert "AnUnreadableWordKeyIsCountedNotDropped" in IBTIDA_CENSUS_NAMED_RESIDUALS


@pytest.mark.skipif(
    not masaq_bytes_are_resolvable(),
    reason=(
        f"no MASAQ bytes resolve from {MASAQ_RELATIVE_PATH} nor from a "
        "declared path; the 11,349-position denominator, the four sentence "
        "classes and the mubtadaʾ standings are derived only from the "
        "fingerprinted bytes. Bytes that resolve and differ are not skipped: "
        "they fail"
    ),
)
def test_the_inchoative_denominator_is_rederived_from_the_deposited_bytes() -> None:
    """يُعرَض المُدَّعى والمُشتَقّ معًا؛ ولا يُعدَّل رقمٌ ليُطابِق ما قِيس."""

    records = masaq_records(read_masaq_bytes())
    reading = read_inchoative_denominator(records)
    classes = classify_positions(records)

    assert reading.stem_count == ARRIVING_STEM_TOTAL, (
        "مقامُ الجذوع خالف المُدَّعى قبل قراءة رقمٍ واحد: "
        f"{reading.stem_count} لا {ARRIVING_STEM_TOTAL}"
    )
    assert reading.denominator_count == INCHOATIVE_POSITION_TOTAL, (
        "مقامُ الابتداء خالف المُدَّعى: "
        f"{reading.denominator_count} لا {INCHOATIVE_POSITION_TOTAL}"
    )
    for figure in ARRIVING_INCHOATIVE_POSITIONS:
        assert reading.counts_by_value.get(figure.value) == (
            figure.claimed_segment_count
        ), (
            f"«{figure.value}» خالف المُدَّعى: "
            f"{reading.counts_by_value.get(figure.value)} لا "
            f"{figure.claimed_segment_count}"
        )
    assert classes.conserves_the_denominator
