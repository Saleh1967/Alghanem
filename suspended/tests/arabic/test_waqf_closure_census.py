"""اختباراتُ قانون الوقف: أنماطٌ مانعةٌ جامعة، وحفظُ المقام، وحدودٌ مكتوبة.

`SyntheticLinesAreDeclaredNotHidden`: الصفوفُ هنا **مُصطنَعة**، تُحاكي بنيةَ
الصفّ وحدَها؛ ولا يخرج منها رقمٌ عن MASAQ البتّة. والقياسُ على البايتات
المُبصَّمة اختبارُه واحدٌ يُفعَّل حين تكون في `corpora/MASAQ.csv` أو في
`ALGHANEM_MASAQ_PATH`.
"""

from __future__ import annotations

from dataclasses import fields

import pytest

from alghanem.arabic.irab_column_census import SURA_COLUMN, VERSE_COLUMN
from alghanem.arabic.irab_column_preregistration import (
    ANCHOR_COLUMN_NAME,
    PHRASAL_FUNCTION_COLUMN,
    SEGMENT_INDEX_COLUMN_NAME,
    SYNTACTIC_ROLE_COLUMN,
    WORD_KEY_COLUMN_NAME,
    RegistrationStanding,
    figures_for_column,
)
from alghanem.arabic.irab_operator_preregistration import STEM_MORPH_TYPE
from alghanem.arabic.masaq_corpus_deposit import (
    MASAQ_RELATIVE_PATH,
    masaq_bytes_are_resolvable,
    masaq_records,
    read_masaq_bytes,
)
from alghanem.arabic.waqf_closure_census import (
    CLAIMED_KEYS_BY_KIND,
    CLOSURE_SCANNED_COLUMNS,
    WAQF_CLOSURE_CENSUS_NAMED_RESIDUALS,
    ClauseUnit,
    ClosureCensus,
    WaqfClosureCensusError,
    clause_units,
    closing_values_absent_from_their_columns,
    measure_closure,
    scan_column_values,
    tagged_terms,
    value_is_absent_from_the_column,
)
from alghanem.arabic.waqf_closure_preregistration import (
    CLOSURE_CENSUS_COLUMNS,
    CLOSURE_DETECTORS,
    KEY_DENOMINATOR,
    NOMINAL_TERM_COVERAGE_GAP,
    PRE_MEASUREMENT_EXPECTATION,
    SUSPENDED_ARRIVING_VALUES,
    WAQF_CLOSURE_PREREGISTRATION_DIGEST,
    WAQF_CLOSURE_PREREGISTRATION_NAMED_RESIDUALS,
    ClauseKind,
    ClosureDetector,
    ClosureStanding,
    CoverageGap,
    SuspendedArrivingValue,
    TermSide,
    WaqfClosurePreregistrationError,
    closing_detectors_for,
    detector_for,
    opening_detectors_for,
    waqf_closure_preregistration_digest,
)


def _row(
    *,
    sura: str,
    verse: str,
    word: str,
    segment: str = "1",
    morph_type: str = STEM_MORPH_TYPE,
    role: str = "",
    phrasal: str = "",
) -> dict[str, str]:
    """صفٌّ مُصطنَعٌ واحد؛ بنيةً لا مدوَّنة."""

    return {
        ANCHOR_COLUMN_NAME: morph_type,
        SYNTACTIC_ROLE_COLUMN: role,
        PHRASAL_FUNCTION_COLUMN: phrasal,
        SURA_COLUMN: sura,
        VERSE_COLUMN: verse,
        WORD_KEY_COLUMN_NAME: word,
        SEGMENT_INDEX_COLUMN_NAME: segment,
    }


SYNTHETIC_RECORDS: tuple[dict[str, str], ...] = (
    # ١:١ — اسميةٌ مُغلَقة: مبتدأٌ وخبرُه في الآية نفسِها.
    _row(sura="1", verse="1", word="1", role="مبتدأ"),
    _row(sura="1", verse="1", word="2", phrasal="خبر"),
    # ١:٢ — اسميةٌ مفتوحة: مبتدأٌ بلا خبرٍ موسوم، وهو حالُ عمودٍ خالٍ لا جملةٍ.
    _row(sura="1", verse="2", word="1", role="مبتدأ"),
    _row(sura="1", verse="2", word="2", role="مضاف إليه"),
    # ١:٣ — فعليةٌ مُغلَقة بفاعل، وشبهُ جملةٍ معها لها متعلَّقٌ مرصود.
    _row(sura="1", verse="3", word="1", role="فعل ماضٍ"),
    _row(sura="1", verse="3", word="2", role="فاعل"),
    _row(sura="1", verse="3", word="3", role="حرف جر"),
    _row(sura="1", verse="3", word="4", role="اسم مجرور"),
    # ١:٤ — فعليةٌ مُغلَقة بنائب فاعلٍ من عمودٍ آخر، ولاحقةٌ ليست جذعًا.
    _row(sura="1", verse="4", word="1", role="فعل مضارع"),
    _row(sura="1", verse="4", word="2", phrasal="نائب فاعل"),
    _row(sura="1", verse="4", word="2", segment="2", morph_type="Suffix", role="فاعل"),
    # ١:٥ — فعليةٌ مفتوحة: فعلٌ بلا فاعلٍ موسومٍ في آيته.
    _row(sura="1", verse="5", word="1", role="فعل ماضٍ"),
    # ٢:١ — شبهُ جملةٍ وحدَها: تابعةٌ بلا متعلَّقٍ مرصود.
    _row(sura="2", verse="1", word="1", role="حرف جر"),
    _row(sura="2", verse="1", word="2", role="اسم مجرور"),
    # ٢:٢ — قيمةٌ خارج الكواشف: لا تفتح وحدةً ولا تُغلِقها.
    _row(sura="2", verse="2", word="1", role="حرف عطف"),
)
"""ستةَ عشرَ صفًّا مُصطنَعًا: المنازلُ الثلاثُ في الأنماط الثلاثة، وقيمةٌ خارجها."""


def test_the_registration_is_declared_weaker_than_prior_to_the_number() -> None:
    """منزلةُ التجميد `مُصاغ_بعد_الرقم`، ومخلَّفاتُه تقول ذلك صراحةً."""

    from alghanem.arabic.irab_column_preregistration import STANDING

    assert STANDING is RegistrationStanding.FORMULATED_AFTER_THE_NUMBER
    assert "ThisRegistrationIsNotPriorToTheNumber" in (
        WAQF_CLOSURE_PREREGISTRATION_NAMED_RESIDUALS
    )


def test_the_digest_is_derived_from_the_content_not_written_by_hand() -> None:
    """البصمةُ تُشتَقّ من المحتوى؛ فلا تُصادِق على ما لم يُبصَّم."""

    assert WAQF_CLOSURE_PREREGISTRATION_DIGEST == waqf_closure_preregistration_digest()
    assert len(WAQF_CLOSURE_PREREGISTRATION_DIGEST) == 64


def test_the_kinds_are_mutually_exclusive_and_jointly_exhaustive_over_pairs() -> None:
    """كلُّ زوجٍ مُجمَّدٍ في نمطٍ واحدٍ حصرًا وطرفٍ واحدٍ حصرًا؛ ولا زوجَ مكرَّر."""

    keys = [detector.key for detector in CLOSURE_DETECTORS]
    assert len(keys) == len(set(keys))
    for detector in CLOSURE_DETECTORS:
        kinds = {other.kind for other in CLOSURE_DETECTORS if other.key == detector.key}
        sides = {other.side for other in CLOSURE_DETECTORS if other.key == detector.key}
        assert len(kinds) == 1
        assert len(sides) == 1
    named = {
        kind for kind in ClauseKind if kind is not ClauseKind.OUTSIDE_THE_DETECTORS
    }
    assert {detector.kind for detector in CLOSURE_DETECTORS} == named


def test_a_value_is_two_values_when_its_column_differs() -> None:
    """«فاعل» في عمودين قيمتان بعددين؛ وهو شاهدُ `AValueWithoutItsColumnIsTwoValues`."""

    role_counts = {
        figure.value: figure.claimed_count
        for figure in figures_for_column(SYNTACTIC_ROLE_COLUMN)
    }
    phrasal_counts = {
        figure.value: figure.claimed_count
        for figure in figures_for_column(PHRASAL_FUNCTION_COLUMN)
    }
    assert role_counts["فاعل"] == 10_483
    assert phrasal_counts["فاعل"] == 1
    assert role_counts["فاعل"] != phrasal_counts["فاعل"]

    role_detector = detector_for(SYNTACTIC_ROLE_COLUMN, "فاعل")
    assert role_detector is not None
    assert role_detector.claimed_segment_count == role_counts["فاعل"]
    assert detector_for(PHRASAL_FUNCTION_COLUMN, "فاعل") is None


def test_the_detectors_import_their_figures_rather_than_restate_them() -> None:
    """عددُ كلّ كاشفٍ مستوردٌ من موضع تجميده؛ ولا رقمَ ثانٍ يُكتَب له هنا."""

    for detector in CLOSURE_DETECTORS:
        frozen = {
            figure.value: figure.claimed_count
            for figure in figures_for_column(detector.column)
        }
        assert detector.claimed_segment_count == frozen[detector.value]


def test_an_unfrozen_value_is_suspended_by_name_rather_than_guessed() -> None:
    """القيمُ الواصلةُ بلا عمودٍ مُسمًّى مُعلَّقةٌ بعلّتها، ولا كاشفَ لها."""

    suspended = {value.name for value in SUSPENDED_ARRIVING_VALUES}
    assert {"ظرف زمان", "ظرف مكان", "نائب فاعل", "اسم ناسخ"} <= suspended
    for value in SUSPENDED_ARRIVING_VALUES:
        assert value.reason.strip()
    # «نائب فاعل» مُعلَّقٌ بعدده الواصل ٧٤٧، والكاشفُ يحمل ٥٧ المُجمَّدَ بعموده.
    detector = detector_for(PHRASAL_FUNCTION_COLUMN, "نائب فاعل")
    assert detector is not None
    assert detector.claimed_segment_count == 57
    arriving = next(
        value for value in SUSPENDED_ARRIVING_VALUES if value.name == "نائب فاعل"
    )
    assert arriving.claimed_count == 747
    assert arriving.claimed_count != detector.claimed_segment_count


def test_a_suspended_value_without_a_reason_is_refused() -> None:
    """تعليقُ قيمةٍ بلا علّةٍ مكتوبةٍ إسقاطٌ صامت، فيُرفَض."""

    with pytest.raises(WaqfClosurePreregistrationError):
        SuspendedArrivingValue(
            name="ظرف زمان", claimed_count=1_426, kind=ClauseKind.PHRASE, reason="  "
        )


def test_a_phrase_has_no_closing_detector() -> None:
    """شبهُ الجملة لا طرفَ مُغلِقَ لها، ولا يُجمَّد لها واحد."""

    assert closing_detectors_for(ClauseKind.PHRASE) == ()
    assert opening_detectors_for(ClauseKind.PHRASE)
    with pytest.raises(WaqfClosurePreregistrationError):
        ClosureDetector(
            column=SYNTACTIC_ROLE_COLUMN,
            value="اسم مجرور",
            kind=ClauseKind.PHRASE,
            side=TermSide.CLOSING,
            claimed_segment_count=12_243,
        )


def test_the_thin_column_limit_is_written_with_both_percentages() -> None:
    """حدُّ العمودين مكتوبٌ بنسبتيه مقروءتين من موضع تجميدهما لا بيدٍ."""

    assert NOMINAL_TERM_COVERAGE_GAP.opening_column == SYNTACTIC_ROLE_COLUMN
    assert NOMINAL_TERM_COVERAGE_GAP.closing_column == PHRASAL_FUNCTION_COLUMN
    assert NOMINAL_TERM_COVERAGE_GAP.opening_percentage == "76.3631"
    assert NOMINAL_TERM_COVERAGE_GAP.closing_percentage == "1.79"
    assert NOMINAL_TERM_COVERAGE_GAP.opening_exceeds_closing
    assert "AThinColumnIsNotAThickOne" in WAQF_CLOSURE_PREREGISTRATION_NAMED_RESIDUALS


def test_the_phrase_column_is_not_among_the_columns_this_census_reads() -> None:
    """`Phrase` مستبعَدٌ عمدًا، ولا يُقاس به شيءٌ هنا."""

    assert "Phrase" not in CLOSURE_CENSUS_COLUMNS
    assert "Phrase" not in CLOSURE_SCANNED_COLUMNS
    assert "ThePhraseColumnIsNotUsed" in WAQF_CLOSURE_PREREGISTRATION_NAMED_RESIDUALS
    with pytest.raises(WaqfClosureCensusError):
        scan_column_values(list(SYNTHETIC_RECORDS), "Phrase")


def test_a_missing_column_stops_the_count_rather_than_zeroing_it() -> None:
    """غيابُ عمودٍ يُوقِف العدَّ ولا يُصفِّره."""

    stripped = [
        {key: value for key, value in record.items() if key != PHRASAL_FUNCTION_COLUMN}
        for record in SYNTHETIC_RECORDS
    ]
    with pytest.raises(WaqfClosureCensusError):
        measure_closure(stripped)
    with pytest.raises(WaqfClosureCensusError):
        measure_closure([])


def test_the_three_standings_are_measured_on_the_synthetic_rows() -> None:
    """المنازلُ الثلاثُ تخرج كما سُنَّت على أسطرٍ مُصرَّحٍ باصطناعها."""

    census = measure_closure(list(SYNTHETIC_RECORDS), corpus_digest="synthetic")

    assert census.count(ClauseKind.NOMINAL, ClosureStanding.CLOSED) == 1
    assert census.count(ClauseKind.NOMINAL, ClosureStanding.OPEN) == 1
    assert census.count(ClauseKind.VERBAL, ClosureStanding.CLOSED) == 2
    assert census.count(ClauseKind.VERBAL, ClosureStanding.OPEN) == 1
    assert census.count(ClauseKind.PHRASE, ClosureStanding.DEPENDENT) == 2
    assert census.keys_total == 7


def test_the_three_standings_conserve_the_declared_denominator() -> None:
    """مُغلَقة + مفتوحة + تابعة = المفاتيحُ بالضبط؛ حفظًا يُفحَص لا يُفترَض."""

    census = measure_closure(list(SYNTHETIC_RECORDS), corpus_digest="synthetic")

    assert census.conserves_the_denominator
    assert census.denominator is KEY_DENOMINATOR
    assert census.keys_total == len(
        [unit for unit in clause_units(list(SYNTHETIC_RECORDS))]
    )
    assert census.keys_total == sum(
        census.keys_of(kind)
        for kind in ClauseKind
        if kind is not ClauseKind.OUTSIDE_THE_DETECTORS
    )


def test_a_phrase_is_never_closed_even_with_an_attachment_in_its_verse() -> None:
    """شبهُ الجملة تابعةٌ ولو حضر متعلَّقُها؛ وحضورُه يُعَدُّ في حقلٍ باسمه."""

    census = measure_closure(list(SYNTHETIC_RECORDS), corpus_digest="synthetic")

    assert census.no_phrase_is_closed
    assert census.attachments_observed[ClauseKind.PHRASE.name] == 1
    with pytest.raises(WaqfClosureCensusError):
        ClauseUnit(
            key=tagged_terms(list(SYNTHETIC_RECORDS))[0],
            standing=ClosureStanding.DEPENDENT,
            attachment_observed=False,
        )


def test_a_closure_is_not_counted_across_the_verse_boundary() -> None:
    """طرفٌ مُغلِقٌ في آيةٍ أخرى لا يُغلِق وحدةً؛ وحدُّ الآية ليس حدَّ الجملة."""

    split = [
        _row(sura="3", verse="1", word="1", role="مبتدأ"),
        _row(sura="3", verse="2", word="1", phrasal="خبر"),
    ]
    census = measure_closure(split, corpus_digest="synthetic")

    assert census.count(ClauseKind.NOMINAL, ClosureStanding.OPEN) == 1
    assert census.count(ClauseKind.NOMINAL, ClosureStanding.CLOSED) == 0
    assert "AVerseBoundaryIsNotASentenceBoundary" in WAQF_CLOSURE_CENSUS_NAMED_RESIDUALS


def test_a_partial_scan_forbids_a_total_denial() -> None:
    """لا نفيَ لقيمةٍ إلّا بعد المرور على قيم العمود كلِّها."""

    records = list(SYNTHETIC_RECORDS)
    scan = scan_column_values(records, SYNTACTIC_ROLE_COLUMN)

    assert scan.distinct_values == len(set(scan.scanned_values))
    assert scan.contains("مبتدأ")
    assert not scan.contains("ظرف زمان")
    assert value_is_absent_from_the_column(records, SYNTACTIC_ROLE_COLUMN, "ظرف زمان")
    # القيمُ الممسوحةُ هي قيمُ العمود كلُّها، لا القيمُ المُجمَّدةُ وحدَها:
    # فحصُ الكواشف ثمّ النفيُ عن العمود استدلالٌ بالجزء على الكلّ.
    assert set(scan.scanned_values) >= {"مبتدأ", "فاعل", "حرف جر", "حرف عطف"}
    assert "حرف عطف" in scan.scanned_values
    absent = closing_values_absent_from_their_columns(records)
    assert ("Phrasal_Function", "خبر حرف ناسخ") in absent
    assert ("Phrasal_Function", "خبر") not in absent


def test_the_phrase_column_would_invert_the_ratio_it_is_excluded_from() -> None:
    """إسقاطُ `Phrase` مُبرهَنٌ لا مُعلَن: وسمُ المُضمَّن دون الرئيسيّ يقلب النسبة."""

    # صفوفٌ تُحاكي وسمَ `Phrase` للجملة المُضمَّنة وحدَها: الجملةُ الرئيسيةُ
    # فعليةٌ في ٤:١، والمُضمَّنةُ اسميةٌ هي وحدَها الموسومةُ في `Phrase`.
    embedded = [
        {**_row(sura="4", verse="1", word="1", role="فعل ماضٍ"), "Phrase": ""},
        {**_row(sura="4", verse="1", word="2", role="فاعل"), "Phrase": ""},
        {
            **_row(sura="4", verse="1", word="3", role="مبتدأ"),
            "Phrase": "جملة اسمية",
        },
        {**_row(sura="4", verse="1", word="4", phrasal="خبر"), "Phrase": "جملة اسمية"},
    ]
    phrase_counts = {record["Phrase"] for record in embedded if record["Phrase"]}
    assert phrase_counts == {"جملة اسمية"}

    census = measure_closure(embedded, corpus_digest="synthetic")
    assert census.keys_of(ClauseKind.VERBAL) == 1
    assert census.keys_of(ClauseKind.NOMINAL) == 1
    # بعمود `Phrase` وحدَه تخرج الاسميةُ ١٠٠٪ والفعليةُ صفرًا، والقياسُ هنا
    # يُخرِجهما واحدةً وواحدة؛ فالفرقُ فرقٌ في شرط الوسم لا في العربية.
    assert "Phrase" not in CLOSURE_CENSUS_COLUMNS


def test_no_accuracy_field_is_admitted_in_either_unit() -> None:
    """لا حقلَ دقّةٍ ولا ثقةٍ ولا نتيجةٍ في بنى الوحدتين."""

    forbidden = ("accuracy", "precision", "confidence", "verdict", "outcome")
    for dataclass_type in (
        CoverageGap,
        ClosureDetector,
        SuspendedArrivingValue,
        ClauseUnit,
        ClosureCensus,
    ):
        for field in fields(dataclass_type):
            assert not any(marker in field.name.lower() for marker in forbidden)


def test_the_claimed_keys_are_a_sum_not_a_fourth_number() -> None:
    """مفاتيحُ كلّ نمطٍ مجموعُ كواشفه الفاتحة؛ ولا رقمَ رابعٌ يُكتَب لها."""

    assert CLAIMED_KEYS_BY_KIND[ClauseKind.VERBAL.name] == 7_321 + 7_527
    assert CLAIMED_KEYS_BY_KIND[ClauseKind.NOMINAL.name] == 3_598
    assert CLAIMED_KEYS_BY_KIND[ClauseKind.PHRASE.name] == 13_034


def test_the_expectation_is_written_before_the_closure_was_measured() -> None:
    """التوقّعُ مكتوبٌ قبل قياسه، وثالثُه مُعلَنٌ أنّه قراءةُ تعريفٍ لا اكتشاف."""

    assert "PreMeasurementExpectation" in PRE_MEASUREMENT_EXPECTATION
    assert "ليس اكتشافًا" in PRE_MEASUREMENT_EXPECTATION
    assert "AThinColumnIsNotAThickOne" in PRE_MEASUREMENT_EXPECTATION


@pytest.mark.skipif(
    not masaq_bytes_are_resolvable(),
    reason=(
        f"MASAQ bytes are not resolvable: place them at {MASAQ_RELATIVE_PATH} or "
        "set ALGHANEM_MASAQ_PATH. No closure figure is issued without the "
        "fingerprinted bytes. Bytes that resolve and differ are not skipped: "
        "they fail"
    ),
)
def test_the_closure_is_measured_on_the_deposited_bytes() -> None:
    """يُقاس الانغلاقُ على البايتات المُبصَّمة، ويُفحَص الحفظُ لا يُفترَض."""

    records = masaq_records(read_masaq_bytes())
    census = measure_closure(records)

    assert census.conserves_the_denominator
    assert census.no_phrase_is_closed
    assert census.keys_total > 0
    for column in CLOSURE_SCANNED_COLUMNS:
        scan = scan_column_values(records, column)
        assert scan.distinct_values > 0
