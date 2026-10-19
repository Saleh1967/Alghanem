"""اختباراتُ وسم الدال وحدَه، ودعوى كونِه بنيةَ البنية الكليّة.

الأرقامُ كلُّها **مُعادةُ الاشتقاق** من بايتات «مقاييس اللغة» المُبصَّمة عند
كلّ تشغيل؛ ولا رقمَ مكتوبٌ ههنا إلّا مقابَلًا بمُشتَقّه.
"""

from __future__ import annotations

import pytest

from alghanem.arabic.dal_alone_gloss import (
    DAL_ALONE_GLOSS_NAMED_RESIDUALS,
    DECLARED_TOLERANCE,
    THE_DAL_CHAPTER_HEADER,
    THE_PROFILE_AXES,
    DalAloneGlossError,
    DalGlossEntry,
    MasaqBlocker,
    ProfileAxis,
    SelfSimilarityStanding,
    assess_masaq_side,
    assess_self_similarity,
    audit_declared_axis_counts,
    dal_gloss_from_maqayis,
    entries_outside_any_chapter,
    profile_of,
    whole_table_entries,
)


def _entry(
    root: str = "دلل",
    root_type: str = "مضاعف",
    axes_text: str = "ابانة الشي بامارة",
    poetry_text: str = "",
    written: str = "1",
) -> DalGlossEntry:
    return DalGlossEntry(
        root_full=root,
        root_type=root_type,
        root_display=root[:2],
        axes_text=axes_text,
        poetry_text=poetry_text,
        chapter_header=THE_DAL_CHAPTER_HEADER,
        written_axis_count=written,
    )


# --- التقسيمُ مصدريٌّ، وانطباقُه يُفحَص ولا يُفترَض ------------------------------


def test_the_chapter_and_the_letter_coincide() -> None:
    """كلُّ صفٍّ في باب الدال جذرُه بالدال، ولا جذرَ بالدال خارجَه."""

    dal = dal_gloss_from_maqayis()
    assert dal
    assert all(entry.opens_with_dal for entry in dal)
    outside = [
        entry
        for entry in whole_table_entries()
        if entry.opens_with_dal and entry.chapter_header != THE_DAL_CHAPTER_HEADER
    ]
    assert outside == []


def test_the_chapter_partition_does_not_cover_the_whole_table() -> None:
    """صفوفٌ لا ترويسةَ لها قائمةٌ فعلًا، فالتقسيمُ ليس تجزئةً تامّة."""

    orphans = entries_outside_any_chapter()
    assert orphans
    assert all(not entry.belongs_to_a_named_chapter for entry in orphans)
    assert all(not entry.opens_with_dal for entry in orphans)
    assert len(orphans) < len(whole_table_entries())


def test_an_entry_without_a_root_is_refused() -> None:
    """وسمٌ بلا جذرٍ يُرفَض عند الإنشاء ولا يُقرَأ مدخلًا خاليًا."""

    with pytest.raises(DalAloneGlossError):
        _entry(root="   ")


# --- عددُ المحاور مُشتَقٌّ لا مقروءٌ من عمود العدّ ---------------------------------


def test_the_axis_count_is_derived_from_the_text_not_from_the_column() -> None:
    """العددُ يُحسَب من نصّ المحاور ولو خالفه العمودُ المكتوب."""

    entry = _entry(axes_text="الاول | الثاني | الثالث", written="1")
    assert entry.derived_axis_count == 3
    assert entry.axes == ("الاول", "الثاني", "الثالث")


def test_an_empty_axis_text_derives_zero_axes() -> None:
    """نصُّ محاورَ خالٍ يُشتَقّ منه صفر، ولا يُجبَر بالعمود المكتوب."""

    entry = _entry(axes_text="  |  ", written="1")
    assert entry.derived_axis_count == 0
    assert entry.carries_any_axis is False


def test_the_declared_column_disagrees_with_the_derivation_on_the_dal_chapter() -> None:
    """في باب الدال خلافٌ قائمٌ بين العمود المكتوب والعدد المُشتَقّ."""

    audit = audit_declared_axis_counts(dal_gloss_from_maqayis())
    assert audit.disagreeing_count > 0
    assert audit.agreeing_count > audit.disagreeing_count
    assert audit.is_a_complete_partition


def test_silence_is_counted_apart_from_disagreement() -> None:
    """الساكتُ صنفٌ ثالثٌ لا يُدمَج في المخالف ولا في الموافق."""

    audit = audit_declared_axis_counts(
        (
            _entry(axes_text="واحد", written=""),
            _entry(root="درر", axes_text="واحد", written="1"),
            _entry(root="دسس", axes_text="واحد", written="3"),
        )
    )
    assert (audit.silent_count, audit.agreeing_count, audit.disagreeing_count) == (
        1,
        1,
        1,
    )
    assert audit.unreadable_count == 0
    assert audit.is_a_complete_partition


def test_an_unreadable_column_is_neither_agreement_nor_silence() -> None:
    """عمودٌ غيرُ خالٍ ولا يُقرَأ عددًا يُحصى في صنفه، ولا يُصمَت عنه."""

    audit = audit_declared_axis_counts((_entry(written="نعم"),))
    assert audit.unreadable_count == 1
    assert audit.silent_count == 0
    assert audit.agreeing_count == 0
    assert audit.disagreeing_count == 0
    assert audit.is_a_complete_partition


# --- بنيةُ البنية الكليّة ---------------------------------------------------------


def test_an_empty_profile_is_refused_not_read_as_zero() -> None:
    """صورةُ مجموعةٍ خاليةٍ قسمةٌ على صفر، فتُرفَض ولا تُقرَأ أصفارًا."""

    with pytest.raises(DalAloneGlossError):
        profile_of("خالية", ())


def test_every_declared_axis_is_compared_and_none_is_dropped() -> None:
    """المحاورُ الخمسةُ تُقابَل كلُّها؛ وإسقاطُ واحدٍ تشابهٌ صامت."""

    verdict = assess_self_similarity(
        profile_of("جزء", dal_gloss_from_maqayis()),
        profile_of("كلّ", whole_table_entries()),
    )
    assert len(verdict.comparisons) == len(THE_PROFILE_AXES)
    assert {item.axis for item in verdict.comparisons} == set(ProfileAxis)


def test_the_dal_chapter_mirrors_the_whole_in_root_type_shares() -> None:
    """أنصبةُ أنواع الجذر في باب الدال داخلَ السماحيّة المُعلَنة."""

    verdict = assess_self_similarity(
        profile_of("جزء", dal_gloss_from_maqayis()),
        profile_of("كلّ", whole_table_entries()),
    )
    by_axis = {item.axis: item for item in verdict.comparisons}
    for axis in (
        ProfileAxis.SHARE_MUDAAF,
        ProfileAxis.SHARE_THULATHI,
        ProfileAxis.SHARE_THULATHI_MUTALL,
    ):
        assert by_axis[axis].is_within_band


def test_the_dal_chapter_diverges_on_the_poetry_share() -> None:
    """ونصيبُ الشاهد الشعريّ خارجَها؛ فالدعوى منقوضةٌ في محورٍ مُسمًّى."""

    verdict = assess_self_similarity(
        profile_of("جزء", dal_gloss_from_maqayis()),
        profile_of("كلّ", whole_table_entries()),
    )
    by_axis = {item.axis: item for item in verdict.comparisons}
    poetry = by_axis[ProfileAxis.SHARE_WITH_POETRY]
    assert poetry.is_within_band is False
    assert poetry.gap > DECLARED_TOLERANCE
    assert poetry.part_share < poetry.whole_share
    assert verdict.diverging_axes == (ProfileAxis.SHARE_WITH_POETRY,)
    assert verdict.standing is SelfSimilarityStanding.DIVERGES_ON_A_NAMED_AXIS


def test_a_matching_profile_without_a_second_source_defers_not_passes() -> None:
    """قيامُ المحاور كلِّها لا يُقرَأ إثباتًا ما لم يقم مصدرٌ ثانٍ."""

    entries = dal_gloss_from_maqayis()
    same = profile_of("نفسُها", entries)
    verdict = assess_self_similarity(same, profile_of("نفسُها أيضًا", entries))
    assert verdict.diverging_axes == ()
    assert verdict.standing is (
        SelfSimilarityStanding.DEFERRED_FOR_WANT_OF_A_SECOND_SOURCE
    )
    corroborated = assess_self_similarity(
        same, profile_of("نفسُها أيضًا", entries), second_source_corroborates=True
    )
    assert corroborated.standing is (
        SelfSimilarityStanding.MIRRORS_THE_WHOLE_ON_EVERY_DECLARED_AXIS
    )


def test_a_negative_tolerance_is_refused() -> None:
    """سماحيّةٌ سالبةٌ ليست سماحيّة، فتُرفَض ولا تُقرَّب."""

    entries = dal_gloss_from_maqayis()
    with pytest.raises(DalAloneGlossError):
        assess_self_similarity(
            profile_of("جزء", entries), profile_of("كلّ", entries), tolerance=-0.1
        )


def test_a_wide_enough_band_would_swallow_the_divergence() -> None:
    """السماحيّةُ مِقبَضٌ: بتوسيعها يختفي الخلاف، فالحكمُ دالّةٌ فيها لا مطلق."""

    verdict = assess_self_similarity(
        profile_of("جزء", dal_gloss_from_maqayis()),
        profile_of("كلّ", whole_table_entries()),
        tolerance=0.5,
        second_source_corroborates=False,
    )
    assert verdict.diverging_axes == ()
    assert verdict.standing is (
        SelfSimilarityStanding.DEFERRED_FOR_WANT_OF_A_SECOND_SOURCE
    )


# --- شقُّ MASAQ -------------------------------------------------------------------


def test_the_masaq_side_names_two_blockers_not_one() -> None:
    """مانعا MASAQ اثنان، والثاني باقٍ ولو حضرت البايتات."""

    extraction = assess_masaq_side()
    assert (
        MasaqBlocker.NO_ROOT_COLUMN_SO_DAL_IS_A_SURFACE_NOT_A_ROOT
        in extraction.blockers
    )
    assert extraction.a_root_gloss_can_be_extracted is False


def test_present_bytes_lift_the_first_blocker_only() -> None:
    """حضورُ البايتات يرفع المانعَ العارضَ وحدَه ولا يفتح الاستخراج."""

    from alghanem.arabic.dal_alone_gloss import MasaqDalExtraction

    present = MasaqDalExtraction(bytes_are_resolvable=True)
    assert present.blockers == (
        MasaqBlocker.NO_ROOT_COLUMN_SO_DAL_IS_A_SURFACE_NOT_A_ROOT,
    )
    assert present.a_root_gloss_can_be_extracted is False


# --- البقايا ----------------------------------------------------------------------


def test_every_named_residual_carries_its_own_key() -> None:
    """كلُّ بقيّةٍ تبدأ باسمها، فلا يُنقَل نصٌّ عن مفتاحٍ آخر."""

    assert DAL_ALONE_GLOSS_NAMED_RESIDUALS
    for key, text in DAL_ALONE_GLOSS_NAMED_RESIDUALS.items():
        assert text.startswith(f"{key}: ")
