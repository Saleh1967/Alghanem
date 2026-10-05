"""تجاربُ فصل التفاسير: كلُّ حكمٍ يُشتَقّ من رقمه، ولا رقمَ يُكتَب باليد."""

from __future__ import annotations

import pytest

from alghanem.arabic.dal_alone_gloss import (
    DECLARED_TOLERANCE,
    ProfileAxis,
    profile_of,
    whole_table_entries,
)
from alghanem.arabic.maqayis_deviation_attribution import (
    A_RESIDUAL_IS_NOT_A_MEASURED_CAUSE,
    MAQAYIS_DEVIATION_ATTRIBUTION_NAMED_RESIDUALS,
    THE_DECLARED_NULL_PROFILE,
    THE_MEASURED_AXIS,
    THE_THREE_CANDIDATE_ACCOUNTS,
    AccountStanding,
    AttributionReading,
    CandidateAccount,
    ChapterExcess,
    HeaderForm,
    MaqayisDeviationAttributionError,
    NullProfile,
    classify_header,
    excess_over_the_size_null,
    extraction_defect_rate,
    header_strata,
    run_attribution,
    spearman_rank_correlation,
)

_READING = run_attribution()


def test_the_three_accounts_are_the_ones_that_were_named() -> None:
    """التفاسيرُ ثلاثةٌ كما سُمّيت حين سُجّلت البقيّة؛ لا رابعَ يُزاد بعد النتيجة."""

    assert len(THE_THREE_CANDIDATE_ACCOUNTS) == 3
    assert set(THE_THREE_CANDIDATE_ACCOUNTS) == set(CandidateAccount)
    for account in THE_THREE_CANDIDATE_ACCOUNTS:
        assert _READING.standing_of(account) is not AccountStanding.NOT_ASSESSED


def test_size_is_refuted_because_the_excess_sits_with_the_large_chapters() -> None:
    """العدّةُ منقوضةٌ تفسيرًا: الفائضُ في الكبار لا في الصغار حيث الضجيجُ أعلى."""

    assert _READING.excess_among_the_large > _READING.excess_among_the_small
    assert (
        _READING.standing_of(CandidateAccount.CHAPTER_SIZE)
        is AccountStanding.REFUTED_AS_THE_ACCOUNT
    )


def test_the_null_threshold_is_wider_for_the_smaller_chapter() -> None:
    """ومع نقضها تفسيرًا، أثرُ العدّة قائمٌ ومقروءٌ في حدّ نموذج العدم نفسِه."""

    ordered = sorted(_READING.excesses, key=lambda item: item.size)
    assert ordered[0].null_threshold > ordered[-1].null_threshold


def test_the_malformed_stratum_is_a_measured_contaminant() -> None:
    """الطبقةُ الفاسدةُ ملوِّثٌ مُثبَتٌ بالعدّ لا مُسمًّى فحسب."""

    assert _READING.malformed_rows > 0
    assert _READING.malformed_stratum_departs_from_the_whole
    assert abs(_READING.malformed_share - _READING.whole_share) > DECLARED_TOLERANCE


def test_the_contaminant_does_not_exhaust_the_excess() -> None:
    """ولا يستغرقها: يبقى بعد نزعها فائضٌ في أكثر صفوف المجال المنقّى."""

    assert _READING.cleaned_exceeding_chapters
    assert _READING.rows_in_cleaned_exceeding_chapters > 0
    assert (
        _READING.standing_of(CandidateAccount.EXTRACTION_UNEVENNESS)
        is AccountStanding.A_REAL_BUT_INSUFFICIENT_CONTRIBUTOR
    )


def test_cleaning_shrinks_the_domain_and_moves_the_baseline() -> None:
    """التنقيةُ تُضيّق المجالَ وتُزحزح خطَّ الأساس، فلا يُقرَأ القياسان واحدًا."""

    assert len(_READING.cleaned_excesses) < len(_READING.excesses)
    assert _READING.cleaned_whole_share != _READING.whole_share


def test_the_authorial_account_stays_a_residual_with_no_probe() -> None:
    """تفاوتُ التأليف بقيّةٌ دائمًا؛ فلا يُرقَّى بارتفاع منافسَيه."""

    assert (
        _READING.standing_of(CandidateAccount.AUTHORIAL_UNEVENNESS)
        is AccountStanding.A_NAMED_RESIDUAL_WITH_NO_PROBE_OF_ITS_OWN
    )


def test_the_residual_standing_does_not_depend_on_the_other_two() -> None:
    """وبنيويًّا: منزلتُه هي هي مهما انقلب مِسبارا العدّة والاستخراج."""

    flipped = AttributionReading(
        excesses=_READING.cleaned_excesses,
        cleaned_excesses=_READING.cleaned_excesses,
        malformed_share=_READING.whole_share,
        whole_share=_READING.whole_share,
        cleaned_whole_share=_READING.cleaned_whole_share,
        malformed_rows=0,
        defect_correlation=0.0,
        correlated_chapters=3,
    )
    assert (
        flipped.standing_of(CandidateAccount.EXTRACTION_UNEVENNESS)
        is AccountStanding.REFUTED_AS_THE_ACCOUNT
    )
    assert (
        flipped.standing_of(CandidateAccount.AUTHORIAL_UNEVENNESS)
        is AccountStanding.A_NAMED_RESIDUAL_WITH_NO_PROBE_OF_ITS_OWN
    )


def test_the_cleaning_rule_reads_the_header_and_not_the_measured_column() -> None:
    """قاعدةُ التصنيف دالّةٌ في نصّ الترويسة وحدَه؛ فلا تنظر إلى ما يُقاس."""

    assert classify_header("كتاب الدّال") is HeaderForm.LETTER_BOOK
    assert classify_header("باب الزاءِ والجيم وما يثلثهما") is HeaderForm.SUB_CHAPTER
    assert classify_header("كتاب رسول اللّه ﵌") is HeaderForm.MALFORMED
    assert classify_header("   ") is HeaderForm.ABSENT
    for entry in whole_table_entries()[:200]:
        assert classify_header(entry.chapter_header) == classify_header(
            entry.chapter_header.strip()
        )


def test_the_strata_partition_the_table_without_loss() -> None:
    """الطبقاتُ تستغرق الجدولَ ولا تُسقِط صفًّا ولا تُكرّره."""

    strata = header_strata()
    assert set(strata) == set(HeaderForm)
    assert sum(len(items) for items in strata.values()) == len(whole_table_entries())
    assert strata[HeaderForm.ABSENT]
    assert strata[HeaderForm.MALFORMED]


def test_the_defect_probe_never_touches_the_measured_column() -> None:
    """مِسبارُ الخلل يقرأ عمودَ المحاور، لا عمودَ الشاهد؛ فاستقلالُه بنيويّ."""

    entries = whole_table_entries()
    rate = extraction_defect_rate(entries)
    silent = sum(1 for entry in entries if not entry.written_axis_count)
    assert rate == silent / len(entries)
    assert 0.0 < rate < 1.0
    with pytest.raises(MaqayisDeviationAttributionError):
        extraction_defect_rate(())


def test_the_correlation_is_reported_and_carries_no_verdict() -> None:
    """الارتباطُ يخرج رقمًا يُقرَأ، ولا يدخل في منزلة تفسيرٍ البتّة."""

    assert -1.0 <= _READING.defect_correlation <= 1.0
    assert _READING.correlated_chapters >= 3
    moved = AttributionReading(
        excesses=_READING.excesses,
        cleaned_excesses=_READING.cleaned_excesses,
        malformed_share=_READING.malformed_share,
        whole_share=_READING.whole_share,
        cleaned_whole_share=_READING.cleaned_whole_share,
        malformed_rows=_READING.malformed_rows,
        defect_correlation=-_READING.defect_correlation,
        correlated_chapters=_READING.correlated_chapters,
    )
    for account in THE_THREE_CANDIDATE_ACCOUNTS:
        assert moved.standing_of(account) is _READING.standing_of(account)


def test_spearman_is_exact_on_a_monotone_pair() -> None:
    """ارتباطُ الرتب مُشتَقٌّ صحيحًا على متتاليةٍ مطّردةٍ صعودًا وهبوطًا."""

    assert spearman_rank_correlation((1.0, 2.0, 3.0, 4.0), (1.0, 2.0, 3.0, 4.0)) == 1.0
    assert spearman_rank_correlation((1.0, 2.0, 3.0, 4.0), (4.0, 3.0, 2.0, 1.0)) == -1.0
    with pytest.raises(MaqayisDeviationAttributionError):
        spearman_rank_correlation((1.0, 2.0), (1.0, 2.0))
    with pytest.raises(MaqayisDeviationAttributionError):
        spearman_rank_correlation((1.0, 2.0, 3.0), (1.0, 2.0))
    with pytest.raises(MaqayisDeviationAttributionError):
        spearman_rank_correlation((1.0, 1.0, 1.0), (1.0, 2.0, 3.0))
    assert spearman_rank_correlation((1.0, 1.0, 2.0, 2.0), (5.0, 5.0, 9.0, 9.0)) == 1.0
    assert spearman_rank_correlation((1.0, 1.0, 2.0, 2.0), (9.0, 9.0, 5.0, 5.0)) == -1.0


def test_the_null_is_reproducible_from_its_declared_seed() -> None:
    """البذرةُ مكتوبةٌ، فيُعاد حدُّ نموذج العدم عينُه في كلّ تشغيل."""

    entries = whole_table_entries()
    chapter = tuple(entry for entry in entries if entry.chapter_header == "كتاب الدّال")
    first = excess_over_the_size_null(chapter, entries)
    assert first == excess_over_the_size_null(chapter, entries)
    observed, _ = first
    expected = abs(
        profile_of("د", chapter).share(THE_MEASURED_AXIS)
        - profile_of("كلّ", entries).share(THE_MEASURED_AXIS)
    )
    assert observed == expected


def test_a_wider_null_profile_is_accepted_and_a_broken_one_is_refused() -> None:
    """صفةُ نموذج العدم تُعلَن وتُفحَص؛ والفاسدةُ تُردّ عند الإنشاء."""

    entries = whole_table_entries()
    chapter = tuple(entry for entry in entries if entry.chapter_header == "كتاب الدّال")
    wider = NullProfile(replicates=40, percentile=0.5, seed=7)
    observed, threshold = excess_over_the_size_null(chapter, entries, profile=wider)
    assert threshold < excess_over_the_size_null(chapter, entries)[1]
    assert observed > 0.0
    with pytest.raises(MaqayisDeviationAttributionError):
        NullProfile(replicates=0, percentile=0.95, seed=1)
    with pytest.raises(MaqayisDeviationAttributionError):
        NullProfile(replicates=10, percentile=1.0, seed=1)


def test_an_empty_or_oversized_group_is_refused() -> None:
    """مجموعةٌ خاليةٌ أو أوسعُ من مجالها لا تُقابَل بنموذج عدم."""

    entries = whole_table_entries()
    with pytest.raises(MaqayisDeviationAttributionError):
        excess_over_the_size_null((), entries)
    with pytest.raises(MaqayisDeviationAttributionError):
        excess_over_the_size_null(entries, entries[:10])
    with pytest.raises(MaqayisDeviationAttributionError):
        ChapterExcess(header="باب", size=0, observed_gap=0.1, null_threshold=0.2)


def test_an_unmeasured_axis_is_refused() -> None:
    """محورٌ غيرُ مُعلَنٍ لا يُقاس به؛ والمحورُ المقيسُ مُسمًّى قبل القراءة."""

    assert THE_MEASURED_AXIS is ProfileAxis.SHARE_WITH_POETRY
    assert THE_DECLARED_NULL_PROFILE.seed == 20260920
    with pytest.raises(MaqayisDeviationAttributionError):
        run_attribution(minimum_size_for_correlation=100000)


def test_an_empty_reading_is_refused() -> None:
    """قراءةٌ بلا بابٍ مقيسٍ لا تُحكَم، ولا تُقرَأ حكمًا فارغًا."""

    with pytest.raises(MaqayisDeviationAttributionError):
        AttributionReading(
            excesses=(),
            cleaned_excesses=_READING.cleaned_excesses,
            malformed_share=0.6,
            whole_share=0.4,
            cleaned_whole_share=0.4,
            malformed_rows=1,
            defect_correlation=0.0,
            correlated_chapters=3,
        )


def test_the_named_residuals_are_self_labelled() -> None:
    """كلُّ باقيةٍ تفتتح باسمها؛ فلا تُنقَل عبارةٌ بلا اسمها."""

    assert MAQAYIS_DEVIATION_ATTRIBUTION_NAMED_RESIDUALS
    for name, text in MAQAYIS_DEVIATION_ATTRIBUTION_NAMED_RESIDUALS.items():
        assert text.startswith(f"{name}: ")
    assert (
        MAQAYIS_DEVIATION_ATTRIBUTION_NAMED_RESIDUALS[
            "A_RESIDUAL_IS_NOT_A_MEASURED_CAUSE"
        ]
        == A_RESIDUAL_IS_NOT_A_MEASURED_CAUSE
    )
