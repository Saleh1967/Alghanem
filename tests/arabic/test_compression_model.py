"""اختبارُ قياس الضغط: مطابقةٌ شرطًا، وبصمةٌ حارسة، وتعادلٌ محسوم.

لا يُقرأ هنا النصُّ الكبير — بايتاتُه غيرُ محشورةٍ في الشجرة — فتُبنى بايتاتٌ
صغيرةٌ تحمل حركاتٍ ومسافةً وسطرًا ووسمَ `<sel>`، وتُحقَن في الدالّات بعد
تثبيت مرجعٍ مؤقّتٍ ببصمتها هي.
"""

from __future__ import annotations

import hashlib
from collections import Counter

import pytest

from alghanem.arabic import compression_model_measurement as measurement
from alghanem.arabic.compression_model_preregistration import (
    FROZEN_CORPUS,
    NAMED_RESIDUALS,
    PREREGISTRATION_DIGEST,
    CompressionCorpusReference,
    CompressionPreregistrationError,
    TieBreakRule,
    preregistration_digest,
)
from alghanem.arabic.compression_model_revision_audit import (
    SUPERSEDED_COMPRESSION_CLAIMS,
)

SAMPLE_TEXT = "بِسْمِ ٱللَّهِ\nٱلرَّحْمَٰنِ ٱلرَّحِيمِ <sel> مِنْ مَنْ أَمْ أُمّ\n"


@pytest.fixture
def sample(monkeypatch: pytest.MonkeyPatch) -> bytes:
    data = SAMPLE_TEXT.encode("utf-8")
    monkeypatch.setattr(
        measurement,
        "FROZEN_CORPUS",
        CompressionCorpusReference(
            source_name="عيّنةُ اختبار",
            byte_length=len(data),
            sha256_hex=hashlib.sha256(data).hexdigest(),
            encoding="utf-8-without-bom",
            normalization_policy="لا تطبيع",
        ),
    )
    return data


def test_the_frozen_corpus_records_the_measured_bytes_not_a_representation() -> None:
    assert FROZEN_CORPUS.byte_length == 1_319_901
    assert FROZEN_CORPUS.sha256_hex == (
        "37633090743d403886b334d12dd911d1994e49767faa9f2be0f01fd48b466c5a"
    )
    assert "لا تطبيع" in FROZEN_CORPUS.normalization_policy


def test_the_preregistration_digest_guards_every_frozen_clause() -> None:
    assert preregistration_digest() == PREREGISTRATION_DIGEST


def test_a_reference_without_a_sha256_is_refused() -> None:
    with pytest.raises(CompressionPreregistrationError):
        CompressionCorpusReference(
            source_name="نصّ",
            byte_length=10,
            sha256_hex="ليست بصمة",
            encoding="utf-8",
            normalization_policy="لا تطبيع",
        )


def test_bytes_that_do_not_match_the_frozen_digest_are_refused(sample: bytes) -> None:
    with pytest.raises(measurement.CompressionMeasurementError):
        measurement.measure_order_zero(sample + b" ")
    tampered = bytearray(sample)
    tampered[0] ^= 0x01
    with pytest.raises(measurement.CompressionMeasurementError):
        measurement.measure_order_zero(bytes(tampered))


@pytest.mark.parametrize("rule", list(TieBreakRule))
def test_both_orders_round_trip_byte_identically(
    rule: TieBreakRule, sample: bytes
) -> None:
    for measure in (measurement.measure_order_zero, measurement.measure_order_one):
        result = measure(sample, rule)
        assert result.round_trip_verified
        assert result.payload_bits > 0
        assert result.table_bits > 0


def test_the_alphabet_is_counted_from_the_bytes_not_declared(sample: bytes) -> None:
    result = measurement.measure_order_zero(sample)
    assert result.alphabet_size == len(Counter(SAMPLE_TEXT))
    assert "<" in SAMPLE_TEXT and "\n" in SAMPLE_TEXT and "\u0651" in SAMPLE_TEXT


def test_no_compression_number_is_issued_without_a_verified_round_trip() -> None:
    with pytest.raises(measurement.CompressionMeasurementError):
        measurement.ModelMeasurement(
            model="مُختلَق",
            tie_break=TieBreakRule.SMALLEST_CODEPOINT,
            alphabet_size=51,
            raw_byte_length=1_319_901,
            payload_bits=2_240_471,
            table_bits=21_589,
            round_trip_verified=False,
        )


def test_the_two_sizes_are_emitted_together(sample: bytes) -> None:
    payload_line, total_line = measurement.measure_order_one(sample).as_two_sizes()
    assert "حمولة" in payload_line
    assert "كلّي" in total_line


def test_the_payload_is_invariant_under_the_tie_break_and_the_table_is_not() -> None:
    # تردّداتٌ مُشبَعةٌ بالتعادل: الكلفةُ أمثلُ فهي وحيدة، ومجموعُ الأطوال ليس كذلك.
    frequencies = {chr(0x0621 + index): 1 + (index % 3) for index in range(12)}
    costs = set()
    tables = set()
    for rule in TieBreakRule:
        lengths = measurement.code_lengths(frequencies, rule)
        costs.add(sum(frequencies[symbol] * lengths[symbol] for symbol in frequencies))
        tables.add(measurement.table_bits(lengths))
    assert len(costs) == 1
    assert min(tables) == measurement.table_bits(
        measurement.code_lengths(frequencies, TieBreakRule.MINIMAL_TABLE)
    )


def test_the_minimal_table_rule_never_exceeds_the_simple_rule() -> None:
    for seed in range(1, 40):
        frequencies = {
            chr(0x0621 + index): 1 + ((index * seed) % 5)
            for index in range(2 + seed % 20)
        }
        simple = measurement.table_bits(
            measurement.code_lengths(frequencies, TieBreakRule.SMALLEST_CODEPOINT)
        )
        minimal = measurement.table_bits(
            measurement.code_lengths(frequencies, TieBreakRule.MINIMAL_TABLE)
        )
        assert minimal <= simple


def test_a_declared_rule_is_deterministic_across_repeated_runs() -> None:
    frequencies = {chr(0x0621 + index): 1 + (index % 3) for index in range(20)}
    for rule in TieBreakRule:
        first = measurement.code_lengths(frequencies, rule)
        for _ in range(5):
            assert measurement.code_lengths(frequencies, rule) == first


def test_canonical_codes_are_a_prefix_free_decodable_set() -> None:
    frequencies = Counter(SAMPLE_TEXT)
    codes = measurement.canonical_codes(
        measurement.code_lengths(frequencies, TieBreakRule.MINIMAL_TABLE)
    )
    ordered = sorted(codes.values())
    assert all(
        not later.startswith(earlier)
        for earlier, later in zip(ordered, ordered[1:], strict=False)
    )


def test_the_frozen_corpus_figures_carry_both_ratios() -> None:
    order_zero = measurement.FROZEN_ORDER_ZERO_MEASUREMENT
    order_one = measurement.FROZEN_ORDER_ONE_MEASUREMENT
    assert round(order_zero.payload_ratio_percent, 2) == 68.88
    assert round(order_zero.total_ratio_percent, 2) == 68.87
    assert round(order_one.payload_ratio_percent, 2) == 78.78
    assert round(order_one.total_ratio_percent, 2) == 78.58


def test_the_superseded_figures_are_recorded_with_their_closure() -> None:
    assert len(SUPERSEDED_COMPRESSION_CLAIMS) == 4
    figures = {claim.superseded_figure for claim in SUPERSEDED_COMPRESSION_CLAIMS}
    assert any("78.45%" in figure for figure in figures)
    assert any("PILOT-1" in figure for figure in figures)
    for claim in SUPERSEDED_COMPRESSION_CLAIMS:
        assert claim.defect.strip()
        assert claim.structural_closure.strip()


def test_the_named_residuals_declare_the_ratio_is_not_a_linguistic_claim() -> None:
    assert "A_COMPRESSION_RATIO_IS_NOT_A_LINGUISTIC_CLAIM" in NAMED_RESIDUALS
    assert "THIS_IS_REGISTRATION_NOT_AUTHORITY" in NAMED_RESIDUALS
