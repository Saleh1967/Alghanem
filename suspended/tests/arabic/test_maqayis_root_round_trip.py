"""اختباراتُ قياسِ الخطّ على جذور المقاييس: كلُّ عددٍ مُجمَّدٍ يُعاد تشغيلُه."""

from __future__ import annotations

import unicodedata

import pytest

from alghanem.arabic.arabic_round_trip_corpus import (
    RoundTripCorpusError,
    RoundTripCorpusMeasurement,
)
from alghanem.arabic.arabic_round_trip_v1 import (
    LayerOutcome,
    RoundTripLayer,
    RoundTripRefusal,
)
from alghanem.arabic.maqayis_root_round_trip import (
    MAQAYIS_TRILATERAL_ROOT_ROUND_TRIP,
    MAQAYIS_TRILATERAL_ROOT_SOURCE_ID,
    TRILATERAL_ROOT_ORDERING_RULE,
    measure_trilateral_roots,
    trilateral_root_strings,
    trilateral_root_tokens,
)
from alghanem.arabic.maqayis_root_table_deposit import (
    FROZEN_ROOT_TABLE,
    REDERIVED_DISTINCT_TRILATERAL_ROOTS,
)


@pytest.fixture(scope="module")
def rerun() -> RoundTripCorpusMeasurement:
    return measure_trilateral_roots()


def test_the_frozen_figures_are_re_derived_by_running_the_pipeline(
    rerun: RoundTripCorpusMeasurement,
) -> None:
    """الرقمُ المُجمَّد يُكذَّب بتشغيلٍ لا يُصدَّق بقراءةِ سطر."""

    assert rerun.table_digest == MAQAYIS_TRILATERAL_ROOT_ROUND_TRIP.table_digest
    assert rerun.halt_profile == MAQAYIS_TRILATERAL_ROOT_ROUND_TRIP.halt_profile
    assert rerun.figures_digest == MAQAYIS_TRILATERAL_ROOT_ROUND_TRIP.figures_digest
    assert rerun.agrees_in_figures_with(MAQAYIS_TRILATERAL_ROOT_ROUND_TRIP)


def test_the_population_is_the_deposit_s_own_counting_rule(
    rerun: RoundTripCorpusMeasurement,
) -> None:
    """المجتمعُ مُشتقٌّ بقاعدة عدِّ الإيداع نفسِها، لا قائمةً مكتوبةً بيد."""

    strings = trilateral_root_strings()
    assert len(strings) == REDERIVED_DISTINCT_TRILATERAL_ROOTS
    assert len(set(strings)) == len(strings)
    assert rerun.token_total == REDERIVED_DISTINCT_TRILATERAL_ROOTS


def test_the_ordering_is_declared_and_followed() -> None:
    """الترتيبُ مُعلَنٌ بنصّه ومتَّبَعٌ في المجتمع، فالتشغيلُ يُعاد لا يُقارَب."""

    strings = trilateral_root_strings()
    assert strings == tuple(sorted(strings))
    assert "sorted" in TRILATERAL_ROOT_ORDERING_RULE
    assert trilateral_root_tokens() == tuple(
        string.encode("utf-8") for string in strings
    )


def test_nothing_returned_as_it_entered_and_the_zero_keeps_its_denominator(
    rerun: RoundTripCorpusMeasurement,
) -> None:
    """الصفرُ رقمٌ مقيسٌ بمقامٍ كامل، لا قياسٌ يُخرَج من السجلّ."""

    assert rerun.end_to_end_reconstructed == 0
    assert rerun.reconstruction_rate == 0.0
    assert sum(halt.count for halt in rerun.halt_profile) == rerun.token_total


def test_the_halt_is_one_named_cause_at_the_syllable_layer(
    rerun: RoundTripCorpusMeasurement,
) -> None:
    """الوقوفُ كلُّه عند المقطع بعلّةٍ واحدةٍ مُسمّاة، لا رفضًا عامًّا."""

    (halt,) = rerun.halt_profile
    assert halt.layer is RoundTripLayer.SYLLABLE
    assert halt.outcome is LayerOutcome.REFUSED
    assert halt.refusal is RoundTripRefusal.SEGMENTATION_ONSETLESS_INITIAL_SAKIN
    assert halt.count == rerun.token_total
    assert (
        rerun.halts_at(
            RoundTripLayer.SYLLABLE,
            RoundTripRefusal.SEGMENTATION_ONSETLESS_INITIAL_SAKIN,
        )
        == rerun.token_total
    )


def test_the_lower_layers_pass_without_a_lost_atom(
    rerun: RoundTripCorpusMeasurement,
) -> None:
    """ما دون المقطع مقامُه كاملٌ بلا رفضٍ ولا مخالفة، وهو موضعُ الخبر."""

    for layer in (
        RoundTripLayer.UTF8_BYTES,
        RoundTripLayer.UNICODE_NFC,
        RoundTripLayer.CARRIER_STATE,
    ):
        assert rerun.halts_at(layer) == 0
    for layer in (RoundTripLayer.WORD_STRUCTURE, RoundTripLayer.FINAL_BYTES):
        assert rerun.halts_at(layer) == 0


def test_the_measurement_is_bound_to_the_deposited_bytes(
    rerun: RoundTripCorpusMeasurement,
) -> None:
    """القياسُ منسوبٌ إلى بصمة الملفّ وطولِه، لا إلى اسمٍ مُرسَل."""

    assert rerun.source_id == MAQAYIS_TRILATERAL_ROOT_SOURCE_ID
    assert rerun.source_sha256 == FROZEN_ROOT_TABLE.sha256_hex
    assert rerun.source_byte_length == FROZEN_ROOT_TABLE.byte_length


def test_the_full_digest_binds_the_environment_and_says_so(
    rerun: RoundTripCorpusMeasurement,
) -> None:
    """البصمةُ الكاملةُ تشمل البيئة؛ فتطابقُها مشروطٌ بها ولا يُخفى الشرط."""

    if rerun.ran_in_the_same_environment_as(MAQAYIS_TRILATERAL_ROOT_ROUND_TRIP):
        assert rerun.digest == MAQAYIS_TRILATERAL_ROOT_ROUND_TRIP.digest
    else:
        assert rerun.unicode_database_version == unicodedata.unidata_version


def test_a_comparison_is_between_two_measurements(
    rerun: RoundTripCorpusMeasurement,
) -> None:
    """المقارنةُ بين قياسين لا بين رقمٍ وقياس."""

    with pytest.raises(RoundTripCorpusError):
        rerun.agrees_in_figures_with("4087")  # type: ignore[arg-type]
