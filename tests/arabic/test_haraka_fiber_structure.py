"""يختبر البنيةَ الليفيّةَ مقروءةً من البتّات: ما قام منها وما لم يقم."""

from __future__ import annotations

from collections import Counter

import pytest

from alghanem.arabic.fath_ayah_source_text import FATH_AYAH_SOURCE_TEXT
from alghanem.arabic.fatiha_source_text import FATIHA_LINES
from alghanem.arabic.haraka_fiber_structure import (
    FIBER_STRUCTURE_NAMED_RESIDUALS,
    THE_CONTESTED_MARKS,
    FiberProfile,
    FiberStructureError,
    WideningEffect,
    fiber_over,
    fiber_profile_of,
    realized_sets_over_letters,
    total_sections_over,
    widening_effect_on,
)
from alghanem.arabic.written_haraka_mark import (
    THE_IMPORTED_HARAKAT,
    has_written_haraka_mark,
    positions_of,
)

_FATIHA = "\n".join(FATIHA_LINES)
_FATH = FATH_AYAH_SOURCE_TEXT
_SCOPES = (("الفاتحة", _FATIHA), ("الفتح ٢٩", _FATH))


def test_the_fibers_take_two_sizes_and_therefore_form_no_bundle() -> None:
    """شرطُ الحزمة تساوي الألياف، والمقيسُ حجمان: خالٍ ومفرد."""

    for scope, text in _SCOPES:
        profile = fiber_profile_of(text, scope)
        assert profile.distinct_sizes == (0, 1)
        assert not profile.is_equinumerous
        assert profile.largest_fiber == 1


def test_the_two_sizes_are_counted_and_not_merely_named() -> None:
    """والعددان مُعادان من البتّات لا منقولان."""

    fatiha = fiber_profile_of(_FATIHA, "الفاتحة")
    assert (fatiha.base_points, fatiha.empty_fibers) == (143, 40)

    fath = fiber_profile_of(_FATH, "الفتح ٢٩")
    assert (fath.base_points, fath.empty_fibers) == (249, 61)


def test_no_total_section_exists_because_a_fiber_is_empty() -> None:
    """القطاعُ يقتضي نقطةً فوق كلّ نقطة، وفوق الخالي لا نقطة."""

    for scope, text in _SCOPES:
        assert total_sections_over(fiber_profile_of(text, scope)) == 0


def test_over_the_marked_base_alone_the_section_is_one_and_not_many() -> None:
    """وفوق الموسومة وحدَها القطاعُ واحدٌ لأنّ الليفَ مفردٌ فلا اختيار."""

    for scope, text in _SCOPES:
        marked = FiberProfile(
            scope=scope,
            sizes=tuple(
                size for size in fiber_profile_of(text, scope).sizes if size > 0
            ),
        )
        assert marked.is_equinumerous
        assert total_sections_over(marked) == 1


def test_the_import_that_was_inert_in_the_predicate_moves_the_fiber() -> None:
    """الخمولُ صفةٌ للسؤال لا للاستيراد: صفرٌ ثنائيًّا، وستّةَ عشرَ ليفيًّا."""

    for scope, text in _SCOPES:
        effect = widening_effect_on(text, scope)
        assert effect.the_projection_is_inert
        assert effect.decisions_moved == 0
        assert effect.the_fiber_moves
        assert effect.fibers_enlarged == 16


def test_the_inertness_of_the_projection_is_rederived_and_not_quoted() -> None:
    """ويُعاد اشتقاقُ الصفر ههنا من المحمول نفسِه لا يُنقَل عنه."""

    widened = THE_IMPORTED_HARAKAT | THE_CONTESTED_MARKS
    for _, text in _SCOPES:
        moved = sum(
            1
            for position in positions_of(text)
            if bool(set(position.marks) & widened) != has_written_haraka_mark(position)
        )
        assert moved == 0


def test_the_two_sixteens_split_into_different_causes() -> None:
    """تساوي المجموعين لا يعني تساوي سببيهما، والتفصيلُ يفرّقهما."""

    fatiha = widening_effect_on(_FATIHA, "الفاتحة")
    assert (fatiha.by_shadda, fatiha.by_dagger) == (14, 2)

    fath = widening_effect_on(_FATH, "الفتح ٢٩")
    assert (fath.by_shadda, fath.by_dagger) == (16, 0)

    assert fatiha.fibers_enlarged == fath.fibers_enlarged
    assert (fatiha.by_shadda, fatiha.by_dagger) != (fath.by_shadda, fath.by_dagger)


def test_the_widened_fiber_reaches_two_where_the_narrow_one_cannot() -> None:
    """وبالتسعة يبلغ الليفُ اثنين، وبالسبعة لا يتجاوز واحدًا."""

    for scope, text in _SCOPES:
        narrow = fiber_profile_of(text, scope)
        wide = fiber_profile_of(
            text, scope, marks=THE_IMPORTED_HARAKAT | THE_CONTESTED_MARKS
        )
        assert narrow.largest_fiber == 1
        assert wide.largest_fiber == 2
        assert wide.distinct_sizes == (0, 1, 2)
        assert wide.empty_fibers == narrow.empty_fibers


def test_adjoining_absence_restores_the_bundle_by_stipulation() -> None:
    """إلحاقُ الغياب يردّ الحزمة تافهةً — بالاصطلاح لا بالقياس."""

    for scope, text in _SCOPES:
        profile = fiber_profile_of(text, scope)
        adjoined = FiberProfile(
            scope=scope, sizes=tuple(max(size, 1) for size in profile.sizes)
        )
        assert adjoined.is_equinumerous
        assert total_sections_over(adjoined) == 1
        assert not profile.is_equinumerous


def test_absence_is_not_a_codepoint_so_the_eighth_member_comes_from_outside() -> None:
    """وثمنُ الإلحاق مقيس: لا نقطةَ ترميزٍ في النصّين تُمثّل الغياب."""

    for _, text in _SCOPES:
        for position in positions_of(text):
            assert all(mark in THE_IMPORTED_HARAKAT for mark in position.haraka_marks)
            if not position.haraka_marks:
                assert not set(position.marks) & THE_IMPORTED_HARAKAT


def test_the_realized_sets_over_letters_are_not_equinumerous_either() -> None:
    """ولا تفاهةَ فوق الحروف: الأحجامُ تختلف ولا حرفَ يحمل السبع."""

    fatiha = realized_sets_over_letters(_FATIHA)
    assert dict(sorted(Counter(len(v) for v in fatiha.values()).items())) == {
        0: 1,
        1: 8,
        2: 9,
        3: 3,
        4: 2,
    }

    fath = realized_sets_over_letters(_FATH)
    assert dict(sorted(Counter(len(v) for v in fath.values()).items())) == {
        0: 3,
        1: 10,
        2: 9,
        3: 4,
        4: 5,
        5: 3,
    }

    for realized in (fatiha, fath):
        assert max(len(marks) for marks in realized.values()) < len(
            THE_IMPORTED_HARAKAT
        )


def test_the_base_points_are_the_letters_and_they_are_counted() -> None:
    """وقاعدةُ الحروف المتمايزة معدودةٌ لا موصوفة."""

    assert len(realized_sets_over_letters(_FATIHA)) == 23
    assert len(realized_sets_over_letters(_FATH)) == 34


def test_the_fiber_of_a_position_is_its_haraka_marks_in_order() -> None:
    """وليفُ الموضع ما لصق به من السبع، بترتيب وروده."""

    for _, text in _SCOPES:
        for position in positions_of(text):
            assert fiber_over(position) == position.haraka_marks
            assert bool(fiber_over(position)) == has_written_haraka_mark(position)


def test_a_profile_refuses_a_nameless_scope_and_a_negative_fiber() -> None:
    """ولا يُقبَل قياسٌ بلا نطاقٍ يُنسَب إليه ولا ليفٌ سالب."""

    with pytest.raises(FiberStructureError):
        FiberProfile(scope="  ", sizes=(1,))
    with pytest.raises(FiberStructureError):
        FiberProfile(scope="نطاق", sizes=(-1,))
    with pytest.raises(FiberStructureError):
        WideningEffect(
            scope="نطاق",
            decisions_moved=-1,
            fibers_enlarged=0,
            by_shadda=0,
            by_dagger=0,
        )


def test_an_empty_base_has_exactly_one_section_and_no_size() -> None:
    """وحدُّ القاعدة الخالية: قطاعٌ واحدٌ خالٍ، لا صفر."""

    empty = FiberProfile(scope="خالية", sizes=())
    assert empty.base_points == 0
    assert empty.largest_fiber == 0
    assert empty.is_equinumerous is False
    assert total_sections_over(empty) == 1


def test_every_residual_is_named_by_its_own_key() -> None:
    """وكلُّ بقيّةٍ تبدأ بمفتاحها فلا تُقتَبس منزوعةَ النسبة."""

    assert set(FIBER_STRUCTURE_NAMED_RESIDUALS) == {
        "THE_FIBERS_ARE_NOT_EQUINUMEROUS_SO_THIS_IS_NOT_A_BUNDLE",
        "A_PARTIAL_SECTION_IS_NOT_A_SECTION",
        "AN_INERT_IMPORT_IN_THE_PROJECTION_IS_DECISIVE_IN_THE_FIBER",
        "THE_TWO_SIXTEENS_DO_NOT_HAVE_THE_SAME_CAUSE",
        "ADJOINING_ABSENCE_RESTORES_THE_BUNDLE_BY_STIPULATION_NOT_BY_MEASUREMENT",
        "THE_REALIZED_SETS_OVER_LETTERS_ARE_NOT_EQUINUMEROUS",
        "A_FIBER_MEASURED_ON_TWO_TEXTS_IS_NOT_A_CORPUS_FIBER",
    }
    for key, text in FIBER_STRUCTURE_NAMED_RESIDUALS.items():
        assert text.startswith(f"{key}: ")


def test_this_measurement_carries_no_authority_field() -> None:
    """وقياسٌ لا سلطةَ فيه لا يحمل حقلَ سلطةٍ ولا رتبة."""

    for holder in (FiberProfile, WideningEffect):
        for name in holder.__dataclass_fields__:
            lowered = name.lower()
            for token in ("authority", "born", "birth", "gate", "rank", "verdict"):
                assert token not in lowered
