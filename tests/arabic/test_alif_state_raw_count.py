"""اختباراتُ العدّ الخامّ لحالات الألف: تُشغِّل العدَّ ولا تكتفي بوجوده."""

from __future__ import annotations

import unicodedata

import pytest

from alghanem.arabic.alif_state_raw_count import (
    ALIF,
    ALIF_STATE_CLAIM,
    ALIF_STATE_RAW_COUNT_NAMED_RESIDUALS,
    SHORT_VOWELS,
    AlifStateRawCountError,
    CarrierAtomRow,
    count_alif_states,
    decompose_lines,
    run_raw_count_on_the_deposited_fatiha,
)
from alghanem.arabic.encoding.contamination_gate import scan_lines
from alghanem.arabic.fatiha_source_text import (
    FATIHA_LINES,
    FATIHA_SOURCE_ID,
    FATIHA_SOURCE_TEXT,
    NORMALIZATION_FORM,
    TRANSCRIPTION_STANDING,
    TranscriptionStanding,
    source_byte_length,
    source_sha256,
)

_FATHA, _DAMMA, _KASRA = SHORT_VOWELS
_SUKUN = "\u0652"
_SUPERSCRIPT_ALEF = "\u0670"


# --- النصُّ المُودَع: حروفٌ في الشجرة، ورتبةُ تحقُّقٍ مُصرَّحٌ بها -------------


def test_the_deposited_text_is_seven_lines_in_its_declared_normal_form() -> None:
    assert len(FATIHA_LINES) == 7
    assert unicodedata.is_normalized(NORMALIZATION_FORM, FATIHA_SOURCE_TEXT)


def test_the_digest_is_derived_from_the_letters_not_written_beside_them() -> None:
    import hashlib

    assert (
        source_sha256()
        == hashlib.sha256(FATIHA_SOURCE_TEXT.encode("utf-8")).hexdigest()
    )
    assert source_byte_length() == len(FATIHA_SOURCE_TEXT.encode("utf-8"))


def test_the_deposit_declares_it_was_not_collated_against_any_edition() -> None:
    assert (
        TRANSCRIPTION_STANDING is TranscriptionStanding.TRANSCRIBED_IN_TREE_NOT_COLLATED
    )
    assert len(TranscriptionStanding) == 3


def test_the_deposited_text_passes_step_zero_before_any_count() -> None:
    assert scan_lines(FATIHA_LINES).rejected == ()


# --- التفكيك: صفٌّ لكلّ حامل، وما لم ينتظم محفوظٌ لا مطروح --------------------


def test_a_carrier_takes_the_marks_that_follow_it_until_the_next_carrier() -> None:
    atoms, unattached, unclassified = decompose_lines(("كَتَبْتُ",))
    assert tuple(row.carrier for row in atoms) == ("ك", "ت", "ب", "ت")
    assert tuple(row.state_marks for row in atoms) == (
        (_FATHA,),
        (_FATHA,),
        (_SUKUN,),
        (_DAMMA,),
    )
    assert unattached == ()
    assert unclassified == ()


def test_a_mark_before_any_carrier_is_kept_rather_than_dropped() -> None:
    _, unattached, _ = decompose_lines((_FATHA + "ب",))
    assert len(unattached) == 1
    assert unattached[0].mark == _FATHA


def test_a_codepoint_that_is_neither_carrier_nor_mark_is_kept() -> None:
    _, _, unclassified = decompose_lines(("ب\u0640ب",))
    assert unclassified == ("\u0640",)


def test_the_superscript_alef_is_read_as_a_state_not_as_a_carrier() -> None:
    atoms, _, _ = decompose_lines(("رَحْمَ" + _SUPERSCRIPT_ALEF + "نِ",))
    carriers = tuple(row.carrier for row in atoms)
    assert ALIF not in carriers
    assert any(_SUPERSCRIPT_ALEF in row.state_marks for row in atoms)


def test_a_row_outside_its_shape_is_refused() -> None:
    with pytest.raises(AlifStateRawCountError, match="رمزٌ واحد"):
        CarrierAtomRow(
            line_index=0, word_index=0, word="با", carrier="با", state_marks=()
        )
    with pytest.raises(AlifStateRawCountError, match="لا يكون سالبًا"):
        CarrierAtomRow(
            line_index=-1, word_index=0, word="ب", carrier="ب", state_marks=()
        )


# --- العدُّ نفسُه، مُشغَّلًا على النصّ المُودَع لا مُتحقَّقًا من وجوده ---------


def test_the_zero_argument_entry_point_actually_counts_the_deposited_text() -> None:
    table = run_raw_count_on_the_deposited_fatiha()
    assert table.source_id == FATIHA_SOURCE_ID
    assert len(table.rows) == 143
    assert len(table.alif_rows) == 23
    assert len(table.other_carrier_rows) == 120
    assert table.unattached_marks == ()
    assert table.unclassified_codepoints == ()


def test_the_first_half_of_the_claim_is_measured_not_assumed() -> None:
    """صفرُ استثناءٍ في هذا النقل، مقيسًا؛ ولو ظهر استثناءٌ لظهر صفُّه هنا."""
    table = run_raw_count_on_the_deposited_fatiha()
    assert table.alif_rows_carrying_a_short_vowel == ()
    assert all(not row.carries_short_vowel for row in table.alif_rows)


def test_the_second_half_of_the_claim_is_measured_on_real_positions() -> None:
    table = run_raw_count_on_the_deposited_fatiha()
    assert len(table.other_rows_carrying_a_short_vowel) == 82
    assert {
        vowel
        for row in table.other_rows_carrying_a_short_vowel
        for vowel in row.short_vowels
    } == {_FATHA, _DAMMA, _KASRA}


def test_an_exception_is_carried_as_a_named_row_rather_than_hidden() -> None:
    """ألفٌ حاملةٌ لفتحةٍ تُقرأ استثناءً مُسمًّى، لا تُطرَح ولا تُلخَّص إلى رقم."""
    table = count_alif_states((ALIF + _FATHA + "ب",), source_id="نصٌّ مصنوعٌ للاختبار")
    exceptions = table.alif_rows_carrying_a_short_vowel
    assert len(exceptions) == 1
    assert exceptions[0].carrier == ALIF
    assert exceptions[0].short_vowels == (_FATHA,)
    assert exceptions[0] in table.rows


def test_the_count_takes_any_text_and_knows_no_particular_sura() -> None:
    table = count_alif_states(("بَابٌ", "دَارٌ"), source_id="نصٌّ آخر")
    assert len(table.alif_rows) == 2
    assert table.alif_rows_carrying_a_short_vowel == ()


def test_a_count_without_a_named_source_is_refused() -> None:
    with pytest.raises(AlifStateRawCountError, match="اسمِ مصدرٍ"):
        count_alif_states(FATIHA_LINES, source_id="   ")


# --- ما لا يقوله هذا العدّ، مُسمًّى -------------------------------------------


def test_the_measured_claim_is_written_before_it_is_counted() -> None:
    assert "فتحة" in ALIF_STATE_CLAIM
    assert ALIF_STATE_CLAIM.strip()


def test_the_table_carries_no_verdict_field() -> None:
    table = run_raw_count_on_the_deposited_fatiha()
    names = set(vars(table))
    assert "verdict" not in names
    assert "status" not in names
    assert "established" not in names


def test_every_named_residual_is_reachable_and_says_something() -> None:
    assert len(ALIF_STATE_RAW_COUNT_NAMED_RESIDUALS) == 4
    for name, text in ALIF_STATE_RAW_COUNT_NAMED_RESIDUALS.items():
        assert name.isupper()
        assert name in text
