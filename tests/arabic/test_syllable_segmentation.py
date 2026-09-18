"""اختباراتُ التقطيع المقطعيّ: تجزئةٌ عكوسةٌ، ورفضٌ مُسمًّى، ولا وزن."""

from __future__ import annotations

import pytest

from alghanem.arabic.encoding.carrier_state_candidate import (
    EMBEDDED_ROUND_TRIP_CASES,
    CarrierStateCodec,
    CarrierStateEncodingError,
)
from alghanem.arabic.encoding.syllable_segmentation import (
    NEUTRAL_ALEF_CARRIER,
    NUCLEUS_STATES,
    Syllable,
    SyllableOnset,
    SyllableRefusal,
    SyllableSegmentationError,
    desegment,
    segment,
)

_CODEC = CarrierStateCodec()


def test_every_syllable_opens_with_a_moving_carrier() -> None:
    units = _CODEC.generate("\u0628\u0650\u0633\u0652\u0645\u0650")
    for syllable in segment(units).syllables:
        assert syllable.units[0].state in NUCLEUS_STATES


def test_the_segmentation_covers_every_unit_exactly_once() -> None:
    for case in EMBEDDED_ROUND_TRIP_CASES:
        try:
            units = _CODEC.generate(case)
            parse = segment(units)
        except (CarrierStateEncodingError, SyllableSegmentationError):
            continue
        assert desegment(parse.syllables) == units
        assert parse.unit_total == len(units)
        starts = [syllable.start for syllable in parse.syllables]
        assert starts == sorted(starts)


def test_an_initial_sakin_that_is_not_an_alef_is_refused_by_name() -> None:
    """الحيادُ للألف العاري وحدَه؛ وساكنٌ آخرُ في الصدر يبقى رفضًا باسمه."""

    units = _CODEC.generate("\u0628\u0652\u062a\u064e")
    with pytest.raises(SyllableSegmentationError) as caught:
        segment(units)
    assert caught.value.refusal is SyllableRefusal.ONSETLESS_INITIAL_SAKIN


def test_a_word_opening_on_a_bare_alef_is_segmented_with_a_neutral_onset() -> None:
    """ألفُ الوصل تفتح مقطعًا ولا تدّعي نواةً، والعكسُ يردّها بعينها."""

    units = _CODEC.generate("\u0627\u0644\u0652\u062d\u064e\u0645\u0652\u062f\u064f")
    parse = segment(units)
    assert desegment(parse.syllables) == units
    assert parse.neutral_onset_count == 1
    first = parse.syllables[0]
    assert first.onset is SyllableOnset.NEUTRAL_ALEF
    assert first.claims_a_nucleus is False
    assert first.units[0].carrier == NEUTRAL_ALEF_CARRIER
    for later in parse.syllables[1:]:
        assert later.onset is SyllableOnset.MOVING_CARRIER
        assert later.claims_a_nucleus is True


def test_the_neutral_onset_does_not_repair_what_lies_after_it() -> None:
    """لامُ التعريف قبل مشدَّدٍ ساكنان متجاوران؛ والحيادُ لا يُصلِحهما."""

    units = _CODEC.generate("\u0627\u0644\u0644\u064e\u0651\u0647\u0650")
    with pytest.raises(SyllableSegmentationError) as caught:
        segment(units)
    assert caught.value.refusal is SyllableRefusal.TWO_ADJACENT_SAKINS


def test_the_neutral_onset_is_not_available_in_the_middle_of_a_word() -> None:
    """مدى الحياد مُعلَن: أوّلُ الكلمة وحدَه، ولا يُفتعَل في وسطها."""

    units = _CODEC.generate("\u0628\u064e\u0627")
    with pytest.raises(SyllableSegmentationError):
        Syllable(start=1, units=(units[1],), onset=SyllableOnset.NEUTRAL_ALEF)


def test_a_neutral_onset_is_refused_for_any_carrier_but_the_bare_alef() -> None:
    units = _CODEC.generate("\u0628\u064e\u062a\u064e")
    with pytest.raises(SyllableSegmentationError):
        Syllable(start=0, units=(units[0],), onset=SyllableOnset.NEUTRAL_ALEF)


def test_a_passthrough_symbol_is_refused_rather_than_swallowed() -> None:
    units = _CODEC.generate("\u0628\u064e!")
    with pytest.raises(SyllableSegmentationError) as caught:
        segment(units)
    assert caught.value.refusal is SyllableRefusal.PASSTHROUGH_IS_NOT_SYLLABIFIED


def test_two_adjacent_sakins_are_refused_and_not_joined_into_one_syllable() -> None:
    units = _CODEC.generate("\u0628\u064e\u0633\u0652\u0645\u0652")
    with pytest.raises(SyllableSegmentationError) as caught:
        segment(units)
    assert caught.value.refusal is SyllableRefusal.TWO_ADJACENT_SAKINS


def test_no_syllable_carries_more_than_one_coda() -> None:
    units = _CODEC.generate("\u0628\u0650\u0633\u0652\u0645\u0650")
    for syllable in segment(units).syllables:
        assert syllable.length in (1, 2)
        assert syllable.has_coda == (syllable.length == 2)


def test_an_empty_input_is_refused_and_not_read_as_a_wordless_parse() -> None:
    with pytest.raises(SyllableSegmentationError) as caught:
        segment(())
    assert caught.value.refusal is SyllableRefusal.NO_UNIT_AT_ALL


def test_a_syllable_cannot_be_built_on_a_sakin_onset() -> None:
    units = _CODEC.generate("\u0628\u0652")
    with pytest.raises(SyllableSegmentationError):
        Syllable(start=0, units=units)
