"""اختباراتُ التقطيع المقطعيّ: تجزئةٌ عكوسةٌ، ورفضٌ مُسمًّى، ولا وزن."""

from __future__ import annotations

import pytest

from alghanem.arabic.encoding.carrier_state_candidate import (
    EMBEDDED_ROUND_TRIP_CASES,
    CarrierStateCodec,
    CarrierStateEncodingError,
)
from alghanem.arabic.encoding.syllable_segmentation import (
    NUCLEUS_STATES,
    Syllable,
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


def test_an_initial_sakin_is_refused_by_name() -> None:
    units = _CODEC.generate("\u0627\u0644\u0644\u064e\u0651\u0647\u0650")
    with pytest.raises(SyllableSegmentationError) as caught:
        segment(units)
    assert caught.value.refusal is SyllableRefusal.ONSETLESS_INITIAL_SAKIN


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
