"""تجاربُ إحصاء الأبواب: الأرقامُ تُشتَقّ ههنا كما تُشتَقّ هناك، ولا تُكتَب."""

from __future__ import annotations

import pytest

from alghanem.arabic.dal_alone_gloss import (
    DECLARED_TOLERANCE,
    THE_DAL_CHAPTER_HEADER,
    THE_PROFILE_AXES,
    ProfileAxis,
    whole_table_entries,
)
from alghanem.arabic.maqayis_chapter_census import (
    A_REFUTATION_IN_ONE_CHAPTER_IS_NOT_A_PROPERTY_OF_THAT_CHAPTER,
    MAQAYIS_CHAPTER_CENSUS_NAMED_RESIDUALS,
    THE_DECLARED_SIZE_STRATUM,
    THE_DECLARED_TOLERANCE_LADDER,
    ChapterCensus,
    ChapterReading,
    DivergenceLocality,
    MaqayisChapterCensusError,
    assess_divergence_locality,
    chapter_entries,
    chapter_headers,
    read_chapter,
    run_chapter_census,
)

_CENSUS = run_chapter_census()


def test_the_partition_is_read_from_the_bytes_and_does_not_cover_the_table() -> None:
    """الترويساتُ مقروءةٌ لا مصنوعة، والتقسيمُ بها لا يستغرق الجدول."""

    assert _CENSUS.chapter_count == len(chapter_headers())
    assert _CENSUS.entries_outside_any_chapter > 0
    assert not _CENSUS.partition_covers_the_table
    counted = sum(item.size for item in _CENSUS.readings)
    assert counted + _CENSUS.entries_outside_any_chapter == len(whole_table_entries())


def test_every_chapter_is_read_on_every_declared_axis() -> None:
    """لا بابَ يُقرَأ على محاورَ أقلَّ من المُعلَنة؛ وإسقاطُ محورٍ تشابهٌ صامت."""

    for item in _CENSUS.readings:
        assert len(item.part_shares) == len(THE_PROFILE_AXES)
        assert len(item.gaps_against_the_whole) == len(THE_PROFILE_AXES)
        assert len(item.gaps_against_the_complement) == len(THE_PROFILE_AXES)


def test_the_whole_share_is_the_same_for_every_chapter() -> None:
    """نصيبُ الكلّ واحدٌ في كلّ قراءة؛ فاختلافُه يعني اختلافَ المقروء."""

    first = _CENSUS.readings[0].whole_shares
    for item in _CENSUS.readings:
        assert item.whole_shares == first


def test_the_complement_comparison_only_widens_and_never_narrows() -> None:
    """التحيّزُ الاحتوائيُّ باتّجاهٍ واحدٍ، مقيسًا في كلّ قياسٍ لا مفترَضًا."""

    assert _CENSUS.the_complement_comparison_only_widens
    strictly_wider = sum(
        1
        for item in _CENSUS.readings
        for narrow, wide in zip(
            item.gaps_against_the_whole,
            item.gaps_against_the_complement,
            strict=True,
        )
        if wide > narrow
    )
    assert strictly_wider > 0


def test_the_complement_comparison_rescues_no_chapter() -> None:
    """ما سقط في المقابلة المتحيّزة لصالحه لا يقوم في المقابلة المنفصلة."""

    for item in _CENSUS.readings:
        against_whole = set(item.diverging_axes(DECLARED_TOLERANCE))
        against_rest = set(
            item.diverging_axes(DECLARED_TOLERANCE, against_complement=True)
        )
        assert against_whole <= against_rest


def test_the_dal_chapter_is_not_anomalous_on_the_poetry_axis() -> None:
    """الحكمُ المطلوب: الانحرافُ موزَّعٌ على الأبواب لا شاذٌّ ببابِ الدال."""

    verdict = assess_divergence_locality(_CENSUS)
    assert verdict.header == THE_DAL_CHAPTER_HEADER
    assert verdict.axis is ProfileAxis.SHARE_WITH_POETRY
    assert verdict.chapters_exceeding > 0
    assert 1 < verdict.rank < verdict.chapter_count
    assert verdict.standing is DivergenceLocality.SHARED_ACROSS_THE_CHAPTERS


def test_the_dal_chapter_is_among_the_chapters_closest_to_the_whole() -> None:
    """بل بابُ الدال أقربُ إلى الكلّ من أكثر الأبواب، لا أبعدُ عنه."""

    dal = next(
        item for item in _CENSUS.readings if item.header == THE_DAL_CHAPTER_HEADER
    )
    closer = sum(
        1
        for item in _CENSUS.readings
        if item.smallest_tolerance_that_passes < dal.smallest_tolerance_that_passes
    )
    assert closer * 2 < _CENSUS.chapter_count


def test_the_refutation_stands_for_the_dal_chapter_too() -> None:
    """ونقضُ الدعوى في باب الدال باقٍ؛ فالتوزّعُ لا يُرقّي محورًا ساقطًا."""

    dal = next(
        item for item in _CENSUS.readings if item.header == THE_DAL_CHAPTER_HEADER
    )
    assert not dal.mirrors_the_whole(DECLARED_TOLERANCE)
    assert dal.diverging_axes(DECLARED_TOLERANCE) == (ProfileAxis.SHARE_WITH_POETRY,)


def test_almost_no_chapter_mirrors_the_whole_at_the_declared_band() -> None:
    """الاجتيازُ عند السماحيّة المُعلَنة نادرٌ جدًّا، فالنقضُ هو القاعدة."""

    mirroring = _CENSUS.mirroring_chapters(DECLARED_TOLERANCE)
    assert 0 < len(mirroring) * 10 < _CENSUS.chapter_count


def test_the_tolerance_ladder_is_monotone_and_widens_the_pass() -> None:
    """المنحنى مطّردٌ صعودًا: كلّما وُسّعت السماحيّةُ لم ينقص المجتازون."""

    rungs = _CENSUS.tolerance_ladder()
    assert tuple(item.tolerance for item in rungs) == THE_DECLARED_TOLERANCE_LADDER
    counts = [item.mirroring_chapters for item in rungs]
    assert counts == sorted(counts)
    assert counts[-1] > counts[0]


def test_the_verdict_flips_inside_the_declared_ladder() -> None:
    """والحكمُ دالّةٌ في العتبة: بابُ الدال يسقط ويقوم داخل السُّلَّم نفسِه."""

    dal = next(
        item for item in _CENSUS.readings if item.header == THE_DAL_CHAPTER_HEADER
    )
    assert not dal.mirrors_the_whole(THE_DECLARED_TOLERANCE_LADDER[0])
    assert dal.mirrors_the_whole(THE_DECLARED_TOLERANCE_LADDER[-1])


def test_the_smallest_passing_tolerance_is_the_largest_gap() -> None:
    """أصغرُ سماحيّةٍ يجتاز بها البابُ أكبرُ فروقه، وتُشتَقّ لا تُكتَب."""

    for item in _CENSUS.readings:
        needed = item.smallest_tolerance_that_passes
        assert item.mirrors_the_whole(needed)
        assert needed == max(item.gaps_against_the_whole)


def test_powerless_passes_are_counted_apart() -> None:
    """اجتيازُ محورٍ نصيبُه صفرٌ مُعطًى بالبناء، فيُعَدّ على حدةٍ لا يُجمَع."""

    total = sum(len(item.powerless_passes) for item in _CENSUS.readings)
    assert total > 0
    for item in _CENSUS.readings:
        for powerless in item.powerless_passes:
            index = THE_PROFILE_AXES.index(powerless.axis)
            assert item.part_shares[index] == 0.0
            assert item.gaps_against_the_whole[index] == powerless.whole_share


def test_the_size_stratum_is_reported_and_filters_nothing() -> None:
    """حدُّ العدّة طبقةٌ تُعلَن، ولا يُسقِط بابًا من الإحصاء."""

    assert _CENSUS.chapters_below_the_size_stratum > 0
    assert _CENSUS.chapters_below_the_size_stratum < _CENSUS.chapter_count
    assert min(item.size for item in _CENSUS.readings) < THE_DECLARED_SIZE_STRATUM
    for item in _CENSUS.readings:
        assert item.is_below_the_size_stratum == (item.size < THE_DECLARED_SIZE_STRATUM)


def test_every_axis_is_measured_across_the_chapters() -> None:
    """كلُّ محورٍ يُحصى انحرافُه عبر الأبواب، فلا محورَ يُقرَأ وحدَه."""

    for axis in THE_PROFILE_AXES:
        diverging = _CENSUS.diverging_chapters_on(axis)
        assert 0 <= len(diverging) <= _CENSUS.chapter_count
        for item in diverging:
            assert item.gap_on(axis) > DECLARED_TOLERANCE


def test_the_ranking_is_total_and_ranks_agree_with_the_order() -> None:
    """الترتيبُ تامٌّ ومرتبةُ كلّ بابٍ موضعُه فيه؛ ولا مرتبةَ مكتوبة."""

    ordered = _CENSUS.ranked_by_gap_on(ProfileAxis.SHARE_WITH_POETRY)
    assert len(ordered) == _CENSUS.chapter_count
    gaps = [item.gap_on(ProfileAxis.SHARE_WITH_POETRY) for item in ordered]
    assert gaps == sorted(gaps, reverse=True)
    for position, item in enumerate(ordered, start=1):
        assert _CENSUS.rank_of(item.header, ProfileAxis.SHARE_WITH_POETRY) == position


def test_reading_one_chapter_agrees_with_the_census() -> None:
    """قراءةُ بابٍ منفردًا تُطابِق قراءتَه في الإحصاء؛ ولا طريقَ ثانٍ للرقم."""

    assert read_chapter(THE_DAL_CHAPTER_HEADER) == next(
        item for item in _CENSUS.readings if item.header == THE_DAL_CHAPTER_HEADER
    )
    assert (
        len(chapter_entries(THE_DAL_CHAPTER_HEADER))
        == read_chapter(THE_DAL_CHAPTER_HEADER).size
    )


def test_an_unknown_chapter_stops_the_reading_and_is_not_read_as_empty() -> None:
    """بابٌ لا صفَّ له يُوقِف القراءةَ ولا يُقرَأ صورةً فارغة."""

    with pytest.raises(MaqayisChapterCensusError):
        read_chapter("بابٌ لا وجودَ له في البايتات")
    with pytest.raises(MaqayisChapterCensusError):
        chapter_entries("بابٌ لا وجودَ له في البايتات")
    with pytest.raises(MaqayisChapterCensusError):
        assess_divergence_locality(_CENSUS, header="بابٌ لا وجودَ له في البايتات")
    with pytest.raises(MaqayisChapterCensusError):
        _CENSUS.rank_of("بابٌ لا وجودَ له", ProfileAxis.SHARE_WITH_POETRY)


def test_a_negative_tolerance_is_refused() -> None:
    """السماحيّةُ السالبةُ ليست سماحيّةً، فتُردّ عند السؤال."""

    with pytest.raises(MaqayisChapterCensusError):
        _CENSUS.readings[0].diverging_axes(-0.01)


def test_a_repeated_chapter_is_refused_at_construction() -> None:
    """بابٌ تكرّر في الإحصاء يُضخّم العدَّ، فيُردّ ولا يُطوى."""

    one = _CENSUS.readings[0]
    with pytest.raises(MaqayisChapterCensusError):
        ChapterCensus(readings=(one, one), entries_outside_any_chapter=0)
    with pytest.raises(MaqayisChapterCensusError):
        ChapterCensus(readings=(), entries_outside_any_chapter=0)


def test_a_reading_with_missing_axes_is_refused() -> None:
    """قراءةٌ ناقصةُ المحاور لا تُبنى؛ والنقصُ لا يُسدّ بصفر."""

    with pytest.raises(MaqayisChapterCensusError):
        ChapterReading(
            header="باب",
            size=3,
            part_shares=(0.1,),
            whole_shares=(0.1,),
            complement_shares=(0.1,),
        )


def test_the_named_residuals_are_self_labelled() -> None:
    """كلُّ باقيةٍ تفتتح باسمها؛ فلا تُنقَل عبارةٌ بلا اسمها."""

    assert MAQAYIS_CHAPTER_CENSUS_NAMED_RESIDUALS
    for name, text in MAQAYIS_CHAPTER_CENSUS_NAMED_RESIDUALS.items():
        assert text.startswith(f"{name}: ")
    assert (
        MAQAYIS_CHAPTER_CENSUS_NAMED_RESIDUALS[
            "A_REFUTATION_IN_ONE_CHAPTER_IS_NOT_A_PROPERTY_OF_THAT_CHAPTER"
        ]
        == A_REFUTATION_IN_ONE_CHAPTER_IS_NOT_A_PROPERTY_OF_THAT_CHAPTER
    )
