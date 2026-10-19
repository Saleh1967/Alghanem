"""اختباراتُ `ArabicRoundTripV1`: كلُّ طبقةٍ تُنفَّذ أمامًا وخلفًا وتُقاس."""

from __future__ import annotations

import unicodedata

import pytest

from alghanem.arabic.arabic_round_trip_v1 import (
    LAYER_FUNCTIONS,
    LayerOutcome,
    LayerRow,
    RoundTripLayer,
    RoundTripRefusal,
    RoundTripV1Error,
    TokenTrace,
    declared_layer_functions,
    measure_round_trip,
    render_table,
    run_token,
    tokens_from_text,
)
from alghanem.arabic.encoding.carrier_state_candidate import (
    EMBEDDED_ROUND_TRIP_CASES,
    CarrierStateCodec,
)
from alghanem.arabic.encoding.syllable_segmentation import desegment, segment
from alghanem.arabic.word_structure_dictionary import (
    analyze_word,
    reverse_word_structure,
)
from alghanem.arabic.word_structure_dictionary_preregistration import (
    DictionaryLayer,
    LayerEpistemicStanding,
    layer_registration,
)

_NFC_CASES = tuple(
    case
    for case in EMBEDDED_ROUND_TRIP_CASES
    if unicodedata.normalize("NFC", case) == case
)


def test_every_layer_declares_a_forward_and_an_inverse_function() -> None:
    """لا تدخل طبقةٌ الخطَّ بلا دالّتين مُعلَنتين بالاسم."""

    assert tuple(functions.layer for functions in LAYER_FUNCTIONS) == tuple(
        RoundTripLayer
    )
    for layer in RoundTripLayer:
        functions = declared_layer_functions(layer)
        assert functions.forward.strip()
        assert functions.inverse.strip()


def test_the_table_has_one_row_per_layer_in_order() -> None:
    table = measure_round_trip([case.encode("utf-8") for case in _NFC_CASES])
    assert tuple(row.layer for row in table.rows) == tuple(RoundTripLayer)
    assert table.token_total == len(_NFC_CASES)
    assert table.row(RoundTripLayer.UTF8_BYTES).input_count == len(_NFC_CASES)


def test_an_nfc_surface_reaches_the_final_bytes_unchanged() -> None:
    """الكلمةُ المُسوّاةُ سلفًا تعود بايتاتُها كما دخلت، أو تُرفَع رفضًا مُسمًّى."""

    for case in _NFC_CASES:
        trace = run_token(case.encode("utf-8"))
        assert trace.outcome in (LayerOutcome.RECONSTRUCTED, LayerOutcome.REFUSED)
        if trace.outcome is LayerOutcome.RECONSTRUCTED:
            assert trace.reached is RoundTripLayer.FINAL_BYTES


def test_a_non_nfc_token_stops_at_the_normalisation_layer() -> None:
    """طبقةُ التسوية تُسجّل اختلافَها ولا تصعد به كأنّه سليم."""

    token = "\u0645\u0651\u064f".encode()
    trace = run_token(token)
    assert trace.reached is RoundTripLayer.UNICODE_NFC
    assert trace.outcome is LayerOutcome.MISMATCHED


def test_invalid_utf8_is_refused_by_name_and_never_read() -> None:
    trace = run_token(b"\xff\xfe")
    assert trace.reached is RoundTripLayer.UTF8_BYTES
    assert trace.outcome is LayerOutcome.REFUSED
    assert trace.refusal is RoundTripRefusal.NOT_VALID_UTF8


def test_an_empty_token_is_refused_rather_than_counted_clean() -> None:
    trace = run_token(b"")
    assert trace.outcome is LayerOutcome.REFUSED
    assert trace.refusal is RoundTripRefusal.EMPTY_TOKEN


def test_a_word_opening_on_a_bare_alef_crosses_the_syllable_layer() -> None:
    """الألفُ عنصرٌ محايد، فالكلمةُ تعبر طبقةَ المقطع بلا حركةٍ مُخمَّنة."""

    trace = run_token("\u0627\u0644\u0652\u062d\u064e\u0645\u0652\u062f\u064f".encode())
    assert trace.reached is RoundTripLayer.FINAL_BYTES
    assert trace.outcome is LayerOutcome.RECONSTRUCTED
    assert trace.refusal is None


def test_an_unmarked_article_lam_now_crosses_the_syllable_layer() -> None:
    """حالةُ تلك اللام غيرُ مكتوبة، فتدخل المفتتحَ ولا تُرفَع رفضًا."""

    trace = run_token("\u0627\u0644\u0644\u064e\u0651\u0647\u0650".encode())
    assert trace.reached is RoundTripLayer.FINAL_BYTES
    assert trace.refusal is None
    assert trace.lost == 0
    assert trace.added == 0


def test_a_madd_before_a_shadda_now_returns_its_own_bytes() -> None:
    """المدُّ إطالةُ نواةٍ لا ساكنٌ، فالكلمةُ تعبر وتعود بايتاتُها كما دخلت."""

    trace = run_token(
        "\u0627\u0644\u0636\u064e\u0651\u0627\u0644\u0650\u0651\u064a\u0646\u064e".encode()
    )
    assert trace.reached is RoundTripLayer.FINAL_BYTES
    assert trace.outcome is LayerOutcome.RECONSTRUCTED
    assert trace.refusal is None


def test_no_layer_counts_a_token_that_never_reached_it() -> None:
    """المقاماتُ تتناقص صعودًا؛ ولا طبقةَ تعدّ ما وقف تحتها."""

    table = measure_round_trip(
        [case.encode("utf-8") for case in EMBEDDED_ROUND_TRIP_CASES]
    )
    counts = [row.input_count for row in table.rows]
    assert counts == sorted(counts, reverse=True)
    for row in table.rows:
        assert row.accepted_count == row.input_count - row.refused_count
        assert row.reconstructed_count == row.accepted_count - row.mismatch_count


def test_a_refused_token_is_outside_the_rate_and_not_a_zero_in_it() -> None:
    table = measure_round_trip([b"\xff", "\u0628\u064e".encode()])
    utf8_row = table.row(RoundTripLayer.UTF8_BYTES)
    assert utf8_row.input_count == 2
    assert utf8_row.refused_count == 1
    assert utf8_row.accepted_count == 1
    assert utf8_row.reconstruction_rate == 1.0


def test_a_rate_over_an_empty_denominator_is_none_and_never_zero() -> None:
    table = measure_round_trip([b"\xff"])
    assert table.row(RoundTripLayer.FINAL_BYTES).input_count == 0
    assert table.row(RoundTripLayer.FINAL_BYTES).reconstruction_rate is None


def test_information_lost_is_counted_in_atoms_not_asserted() -> None:
    """الفقدُ يخرج من فرقِ كثرتين، فحذفُ حرفٍ يُعَدّ ولا يُوصَف."""

    table = measure_round_trip([b"\xd8\xa8\xff"])
    row = table.row(RoundTripLayer.UTF8_BYTES)
    assert row.refused_count == 1
    assert row.information_lost == 0


def test_the_syllable_layer_is_a_segmentation_and_its_inverse_is_exact() -> None:
    codec = CarrierStateCodec()
    units = codec.generate("\u0628\u0650\u0633\u0652\u0645\u0650")
    parse = segment(units)
    assert parse.unit_total == len(units)
    assert desegment(parse.syllables) == units
    assert sum(syllable.length for syllable in parse.syllables) == len(units)


def test_reverse_word_structure_returns_the_units_the_codec_produced() -> None:
    codec = CarrierStateCodec()
    for case in EMBEDDED_ROUND_TRIP_CASES:
        dictionary = analyze_word(case)
        assert reverse_word_structure(dictionary) == codec.generate(case)


def test_a_passthrough_symbol_returns_as_a_passthrough_not_as_a_letter() -> None:
    codec = CarrierStateCodec()
    surface = "\u0627\u0644\u0639\u0631\u0628\u064a\u0629!"
    rebuilt = reverse_word_structure(analyze_word(surface))
    assert codec.retrieve(rebuilt) == surface


def test_the_withheld_dictionary_layers_stay_withheld() -> None:
    """بناءُ وحدةِ سيلبنةٍ لا يرفع حجبَ «المقطع والوزن» ولا حجبَ غيره."""

    for layer in (
        DictionaryLayer.SYLLABLES_AND_WAZN,
        DictionaryLayer.PHONETIC_FEATURES,
        DictionaryLayer.AL_ANALYSIS,
        DictionaryLayer.JARAD_ANALYSIS,
    ):
        standing = layer_registration(layer).standing
        assert standing is not LayerEpistemicStanding.MEASURED_BY_AN_EXISTING_CODEC


def test_tokens_from_text_declares_its_own_split() -> None:
    assert tokens_from_text("\u0628\u064e \u062a\u064e") == (
        "\u0628\u064e".encode(),
        "\u062a\u064e".encode(),
    )


def test_render_table_prints_one_line_per_layer() -> None:
    table = measure_round_trip([case.encode("utf-8") for case in _NFC_CASES])
    rendered = render_table(table)
    assert len(rendered.splitlines()) == len(RoundTripLayer) + 2


def test_a_row_cannot_claim_loss_without_a_single_mismatch() -> None:
    with pytest.raises(RoundTripV1Error):
        LayerRow(
            layer=RoundTripLayer.CARRIER_STATE,
            atom=declared_layer_functions(RoundTripLayer.CARRIER_STATE).atom,
            input_count=1,
            refused_count=0,
            mismatch_count=0,
            information_lost=3,
            information_added=0,
        )


def test_a_refusal_carries_its_sealed_reason_and_a_clean_trace_does_not() -> None:
    with pytest.raises(RoundTripV1Error):
        TokenTrace(
            token_index=0,
            reached=RoundTripLayer.UTF8_BYTES,
            outcome=LayerOutcome.REFUSED,
        )
    with pytest.raises(RoundTripV1Error):
        TokenTrace(
            token_index=0,
            reached=RoundTripLayer.FINAL_BYTES,
            outcome=LayerOutcome.RECONSTRUCTED,
            refusal=RoundTripRefusal.EMPTY_TOKEN,
        )


def test_the_pipeline_refuses_a_text_input_and_reads_bytes_only() -> None:
    with pytest.raises(RoundTripV1Error):
        run_token("\u0628\u064e")  # type: ignore[arg-type]


def test_a_geminated_token_no_longer_comes_back_reordered() -> None:
    """العكسُ الكتابيُّ يكتب بالترتيب القانونيّ، فذهب اختلافُ الترتيب بتمامه."""

    token = unicodedata.normalize("NFC", "\u0631\u064e\u0628\u0651\u064f\u0643\u064e")
    table = measure_round_trip([token.encode("utf-8")])
    row = table.row(RoundTripLayer.FINAL_BYTES)
    assert row.mismatch_count == 0
    assert row.ordering_only_count == 0
    assert table.traces[0].outcome is LayerOutcome.RECONSTRUCTED


def test_an_ordering_only_mismatch_is_still_readable_as_such() -> None:
    """بابُ «اختلافِ ترتيبٍ بلا فقد» يبقى مقروءًا وإن خلا منه هذا الإيداع."""

    reordered = TokenTrace(
        token_index=0,
        reached=RoundTripLayer.FINAL_BYTES,
        outcome=LayerOutcome.MISMATCHED,
        refusal=None,
        lost=0,
        added=0,
    )
    assert reordered.is_ordering_only is True
    lossy = TokenTrace(
        token_index=1,
        reached=RoundTripLayer.FINAL_BYTES,
        outcome=LayerOutcome.MISMATCHED,
        refusal=None,
        lost=1,
        added=0,
    )
    assert lossy.is_ordering_only is False


def test_ordering_only_can_never_exceed_the_mismatches_it_is_part_of() -> None:
    with pytest.raises(RoundTripV1Error):
        LayerRow(
            layer=RoundTripLayer.FINAL_BYTES,
            atom=declared_layer_functions(RoundTripLayer.FINAL_BYTES).atom,
            input_count=2,
            refused_count=0,
            mismatch_count=1,
            information_lost=0,
            information_added=0,
            ordering_only_count=2,
        )
