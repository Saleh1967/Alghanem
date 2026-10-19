"""اختباراتُ قياسِ الخطّ على مدوّنةٍ مُبصَّمة: كلُّ رقمٍ مُجمَّدٍ يُعاد تشغيلُه."""

from __future__ import annotations

import unicodedata
from dataclasses import replace

import pytest

from alghanem.arabic.arabic_round_trip_corpus import (
    FATIHA_ROUND_TRIP,
    MEASURED_ROUND_TRIP_SOURCES,
    UNMEASURED_ROUND_TRIP_SOURCES,
    RoundTripCorpusError,
    RoundTripCorpusMeasurement,
    measure_deposited_text,
)
from alghanem.arabic.arabic_round_trip_v1 import (
    HaltCount,
    LayerOutcome,
    RoundTripLayer,
    RoundTripRefusal,
    measure_round_trip,
    tokens_from_text,
)
from alghanem.arabic.fatiha_source_text import (
    FATIHA_SOURCE_ID,
    FATIHA_SOURCE_TEXT,
    source_byte_length,
    source_sha256,
)


def _rerun() -> RoundTripCorpusMeasurement:
    return measure_deposited_text(
        FATIHA_SOURCE_TEXT,
        source_id=FATIHA_SOURCE_ID,
        source_sha256=source_sha256(),
        source_byte_length=source_byte_length(),
    )


def test_the_frozen_corpus_figure_is_re_derived_by_running_the_pipeline() -> None:
    """الرقمُ المُجمَّد يُكذَّب بتشغيلٍ لا يُصدَّق بقراءةِ سطر."""

    rerun = _rerun()
    assert rerun.table_digest == FATIHA_ROUND_TRIP.table_digest
    assert rerun.halt_profile == FATIHA_ROUND_TRIP.halt_profile
    assert rerun.figures_digest == FATIHA_ROUND_TRIP.figures_digest
    assert rerun.agrees_in_figures_with(FATIHA_ROUND_TRIP)


def test_the_full_digest_binds_the_environment_and_says_so() -> None:
    """البصمةُ الكاملةُ تشمل البيئة؛ فتطابقُها مشروطٌ بها ولا يُخفى الشرط."""

    rerun = _rerun()
    if rerun.ran_in_the_same_environment_as(FATIHA_ROUND_TRIP):
        assert rerun.digest == FATIHA_ROUND_TRIP.digest
    else:
        assert rerun.unicode_database_version == unicodedata.unidata_version
        assert rerun.digest != FATIHA_ROUND_TRIP.digest
        assert rerun.figures_digest == FATIHA_ROUND_TRIP.figures_digest


def test_the_environment_alone_moves_the_full_digest_and_not_the_figures() -> None:
    """نسخةُ يونيكود تُحرّك `digest` وحدَه؛ والأرقامُ لا تتحرّك بها."""

    elsewhere = replace(FATIHA_ROUND_TRIP, unicode_database_version="0.0.0-not-a-run")
    assert elsewhere.digest != FATIHA_ROUND_TRIP.digest
    assert elsewhere.figures_digest == FATIHA_ROUND_TRIP.figures_digest
    assert elsewhere.agrees_in_figures_with(FATIHA_ROUND_TRIP)
    assert not elsewhere.ran_in_the_same_environment_as(FATIHA_ROUND_TRIP)


def test_a_moved_figure_moves_both_digests() -> None:
    """وتغيّرُ رقمٍ واحدٍ يُسقِط البصمتين معًا، فلا تستر البيئةُ انحرافًا."""

    moved = replace(FATIHA_ROUND_TRIP, source_byte_length=1 + source_byte_length())
    assert moved.figures_digest != FATIHA_ROUND_TRIP.figures_digest
    assert moved.digest != FATIHA_ROUND_TRIP.digest
    assert not moved.agrees_in_figures_with(FATIHA_ROUND_TRIP)


def test_figures_are_compared_against_a_measurement_not_against_a_number() -> None:
    with pytest.raises(RoundTripCorpusError):
        FATIHA_ROUND_TRIP.agrees_in_figures_with(FATIHA_ROUND_TRIP.figures_digest)  # type: ignore[arg-type]
    with pytest.raises(RoundTripCorpusError):
        FATIHA_ROUND_TRIP.ran_in_the_same_environment_as("15.0.0")  # type: ignore[arg-type]


def test_the_halt_profile_accounts_for_every_token_exactly_once() -> None:
    assert (
        sum(halt.count for halt in FATIHA_ROUND_TRIP.halt_profile)
        == FATIHA_ROUND_TRIP.token_total
    )


def test_no_layer_halts_a_token_in_this_deposit() -> None:
    """لم يبقَ في هذا الإيداع وقوفٌ عند طبقةٍ واحدة؛ والعددُ مُشتَقٌّ لا مكتوب."""

    for layer in RoundTripLayer:
        if layer is RoundTripLayer.FINAL_BYTES:
            continue
        assert FATIHA_ROUND_TRIP.halts_at(layer) == 0
    assert FATIHA_ROUND_TRIP.halts_at(RoundTripLayer.FINAL_BYTES) == 29
    assert (
        FATIHA_ROUND_TRIP.halts_at(
            RoundTripLayer.SYLLABLE,
            RoundTripRefusal.SEGMENTATION_TWO_ADJACENT_SAKINS,
        )
        == 0
    )


def test_the_neutral_alef_left_no_onsetless_halt_in_this_deposit() -> None:
    """بعد الحياد لم يبقَ في هذا الإيداع وقوفٌ واحدٌ على ألفٍ عارية."""

    assert (
        FATIHA_ROUND_TRIP.halts_at(
            RoundTripLayer.SYLLABLE,
            RoundTripRefusal.SEGMENTATION_ONSETLESS_INITIAL_SAKIN,
        )
        == 0
    )


def test_the_rate_is_over_everything_that_entered_the_pipeline() -> None:
    assert FATIHA_ROUND_TRIP.end_to_end_reconstructed == 29
    assert FATIHA_ROUND_TRIP.token_total == 29
    assert FATIHA_ROUND_TRIP.reconstruction_rate == 1.0


def test_every_halt_reason_in_the_profile_is_a_sealed_member() -> None:
    for halt in FATIHA_ROUND_TRIP.halt_profile:
        assert isinstance(halt.layer, RoundTripLayer)
        assert isinstance(halt.outcome, LayerOutcome)
        if halt.outcome is LayerOutcome.REFUSED:
            assert isinstance(halt.refusal, RoundTripRefusal)
        else:
            assert halt.refusal is None


def test_a_text_that_does_not_match_its_digest_is_refused() -> None:
    with pytest.raises(RoundTripCorpusError):
        measure_deposited_text(
            FATIHA_SOURCE_TEXT + "\u0628\u064e",
            source_id=FATIHA_SOURCE_ID,
            source_sha256=source_sha256(),
            source_byte_length=source_byte_length(),
        )


def test_a_measurement_cannot_claim_more_reconstruction_than_it_holds() -> None:
    with pytest.raises(RoundTripCorpusError):
        RoundTripCorpusMeasurement(
            source_id=FATIHA_SOURCE_ID,
            source_sha256=source_sha256(),
            source_byte_length=source_byte_length(),
            normalization_form="NFC",
            unicode_database_version="15.0.0",
            token_total=2,
            end_to_end_reconstructed=2,
            halt_profile=(
                HaltCount(
                    layer=RoundTripLayer.FINAL_BYTES,
                    outcome=LayerOutcome.RECONSTRUCTED,
                    refusal=None,
                    count=1,
                ),
                HaltCount(
                    layer=RoundTripLayer.SYLLABLE,
                    outcome=LayerOutcome.REFUSED,
                    refusal=RoundTripRefusal.SEGMENTATION_TWO_ADJACENT_SAKINS,
                    count=1,
                ),
            ),
            table_digest=FATIHA_ROUND_TRIP.table_digest,
        )


def test_a_halt_profile_that_drops_a_token_is_refused() -> None:
    with pytest.raises(RoundTripCorpusError):
        RoundTripCorpusMeasurement(
            source_id=FATIHA_SOURCE_ID,
            source_sha256=source_sha256(),
            source_byte_length=source_byte_length(),
            normalization_form="NFC",
            unicode_database_version="15.0.0",
            token_total=5,
            end_to_end_reconstructed=1,
            halt_profile=(
                HaltCount(
                    layer=RoundTripLayer.FINAL_BYTES,
                    outcome=LayerOutcome.RECONSTRUCTED,
                    refusal=None,
                    count=1,
                ),
            ),
            table_digest=FATIHA_ROUND_TRIP.table_digest,
        )


def test_the_unmeasured_corpus_carries_no_figure_at_all() -> None:
    """المدوّنةُ التي لم تُشغَّل بايتاتُها تبقى بلا عددٍ واحد."""

    assert UNMEASURED_ROUND_TRIP_SOURCES
    for source in UNMEASURED_ROUND_TRIP_SOURCES:
        assert source.why_no_figure_is_frozen.strip()
        assert not hasattr(source, "token_total")
        assert not hasattr(source, "reconstruction_rate")
    measured_ids = {entry.source_id for entry in MEASURED_ROUND_TRIP_SOURCES}
    unmeasured_ids = {entry.source_id for entry in UNMEASURED_ROUND_TRIP_SOURCES}
    assert not measured_ids & unmeasured_ids


def test_the_table_digest_moves_when_any_row_moves() -> None:
    """البصمةُ تُمسِك الجدولَ كلَّه، فتغيّرُ كلمةٍ واحدةٍ يُسقِط المطابقة."""

    widened = measure_round_trip(
        tokens_from_text(FATIHA_SOURCE_TEXT + "\n\u0628\u0650\u0633\u0652\u0645\u0650")
    )
    assert widened.digest != FATIHA_ROUND_TRIP.table_digest


def test_the_profile_is_one_row_and_no_mismatch_is_left_in_it() -> None:
    """صفٌّ واحدٌ في السجلّ: لا رفضَ ولا مخالفةَ ترتيبٍ في هذا الإيداع."""

    assert len(FATIHA_ROUND_TRIP.halt_profile) == 1
    only = FATIHA_ROUND_TRIP.halt_profile[0]
    assert only.outcome is LayerOutcome.RECONSTRUCTED
    assert only.layer is RoundTripLayer.FINAL_BYTES
    assert only.count == FATIHA_ROUND_TRIP.token_total
    assert not [
        halt
        for halt in FATIHA_ROUND_TRIP.halt_profile
        if halt.outcome is LayerOutcome.MISMATCHED
    ]


def test_completeness_here_is_this_deposit_not_a_claim_about_arabic() -> None:
    """التمامُ عددُ إيداعٍ واحدٍ مُبصَّم، ولا يُقرأ دعوى تمامٍ في العربية."""

    assert FATIHA_ROUND_TRIP.source_id == FATIHA_SOURCE_ID
    assert FATIHA_ROUND_TRIP.source_sha256 == source_sha256()
    assert FATIHA_ROUND_TRIP.token_total == 29
    assert UNMEASURED_ROUND_TRIP_SOURCES
    for unmeasured in UNMEASURED_ROUND_TRIP_SOURCES:
        assert unmeasured.why_no_figure_is_frozen.strip()
