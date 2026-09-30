"""اختباراتُ زِبف وإنتروبيا الكتل: كلُّ رقمٍ يُعاد من القرص، ولا حكمَ مكتوب."""

from __future__ import annotations

from dataclasses import fields

import pytest

from alghanem.arabic.zipf_block_entropy_measure import (
    THE_BLOCK_SIZES,
    THE_ENTROPY_TOLERANCE,
    THE_EXPONENT_TOLERANCE,
    THE_LADDER_AT_MEASUREMENT,
    THE_QUOTED_BLOCK_ENTROPY,
    THE_QUOTED_ZIPF,
    THE_R_SQUARED_TOLERANCE,
    THE_RANK_WINDOWS,
    THE_STRIDE_LADDER_AT_MEASUREMENT,
    THE_VOCABULARY_AT_MEASUREMENT,
    BlockEntropyLadder,
    QuotedZipf,
    SamplingRule,
    StreamKey,
    TypeTokenCensus,
    Verdict,
    ZipfBlockEntropyError,
    ZipfFit,
    block_entropy_ladder,
    the_block_entropy_comparison,
    the_corpus_gate_is_untouched,
    the_exponent_is_negative_on_every_window,
    the_folding_moves_the_exponent_by,
    the_ladders_have_drifted,
    the_quoted_pair_against_our_windows,
    the_stride_shift,
    the_vocabulary_has_drifted,
    the_window_that_hosts_the_quoted_pair,
    vocabulary_census,
    zipf_fit_for,
    zipf_ladder,
)
from alghanem.arabic.zipf_block_entropy_measure import (
    ZIPF_BLOCK_ENTROPY_NAMED_RESIDUALS as RESIDUALS,
)

# ---------------------------------------------------------------------------
# المقيسُ من البايتات المختومة
# ---------------------------------------------------------------------------


def test_the_ladder_covers_every_declared_window_once() -> None:
    assert tuple(fit.window for fit in zipf_ladder()) == THE_RANK_WINDOWS


def test_the_exponent_falls_on_every_window_as_zipf_requires() -> None:
    assert the_exponent_is_negative_on_every_window() is True
    for fit in zipf_ladder():
        assert fit.exponent < 0.0
        assert fit.magnitude > 0.5


def test_the_window_zero_reads_every_rank_and_the_others_truncate() -> None:
    census = vocabulary_census()
    assert zipf_fit_for(0).ranks == census.types
    for window in THE_RANK_WINDOWS[:-1]:
        assert zipf_fit_for(window).ranks == window


def test_an_undeclared_window_is_refused_and_not_rounded_to_a_neighbour() -> None:
    with pytest.raises(ZipfBlockEntropyError):
        zipf_fit_for(777)


# ---------------------------------------------------------------------------
# الأسُّ دالّةٌ في النافذة، وهذا مقيسٌ لا موصوف
# ---------------------------------------------------------------------------


def test_the_exponent_is_not_one_number_but_a_ladder_of_windows() -> None:
    magnitudes = [fit.magnitude for fit in zipf_ladder()]
    assert max(magnitudes) - min(magnitudes) > 0.2
    assert len(set(round(value, 4) for value in magnitudes)) == len(magnitudes)


def test_the_whole_vocabulary_fit_is_the_worst_bound_of_them_all() -> None:
    ladder = zipf_ladder()
    whole = zipf_fit_for(0)
    assert whole.r_squared == min(fit.r_squared for fit in ladder)


def test_the_quoted_pair_lands_in_exactly_one_of_our_windows() -> None:
    hosts = the_window_that_hosts_the_quoted_pair()
    assert hosts == (10000,)
    verdicts = the_quoted_pair_against_our_windows()
    assert sum(1 for verdict in verdicts if verdict.both_agree) == 1
    hosting = next(verdict for verdict in verdicts if verdict.both_agree)
    assert abs(hosting.exponent_gap) <= THE_EXPONENT_TOLERANCE
    assert abs(hosting.r_squared_gap) <= THE_R_SQUARED_TOLERANCE


def test_the_hosting_window_is_not_our_headline_figure() -> None:
    """موافقةُ نافذةٍ لا تُقرأ موافقةَ نصٍّ: نافذتُنا الكاملةُ تخالف المنقول."""

    whole = zipf_fit_for(0)
    assert abs(whole.magnitude - THE_QUOTED_ZIPF.magnitude) > THE_EXPONENT_TOLERANCE


def test_their_denominator_is_not_ours_so_the_agreement_is_local() -> None:
    census = vocabulary_census()
    assert census.tokens != THE_QUOTED_ZIPF.tokens
    assert census.types != THE_QUOTED_ZIPF.types


# ---------------------------------------------------------------------------
# الطيُّ والفكُّ: الدعوى تُقاس فتُردّ
# ---------------------------------------------------------------------------


def test_the_folding_moves_two_types_and_leaves_the_exponent_where_it_was() -> None:
    sealed = vocabulary_census(StreamKey.AS_SEALED)
    folded = vocabulary_census(StreamKey.FOLDED_AND_UNTIED)
    assert sealed.tokens == folded.tokens
    assert sealed.types - folded.types == 2
    assert the_folding_moves_the_exponent_by() < 0.001


def test_the_folded_stream_still_falls_on_every_window() -> None:
    assert the_exponent_is_negative_on_every_window(StreamKey.FOLDED_AND_UNTIED) is True


def test_the_folding_is_not_a_no_op_on_the_bytes_themselves() -> None:
    """الطيُّ يُغيّر التيّارَ فعلًا؛ وخمولُه على الأسّ نتيجةٌ لا فراغُ تنفيذ."""

    sealed = block_entropy_ladder(StreamKey.AS_SEALED).per_character
    folded = block_entropy_ladder(StreamKey.FOLDED_AND_UNTIED).per_character
    assert folded[0] < sealed[0]


# ---------------------------------------------------------------------------
# خطوةُ السبعة: مُعلَنةٌ ومسعَّرة
# ---------------------------------------------------------------------------


def test_both_ladders_fall_strictly_from_one_character_to_eight() -> None:
    for rule in SamplingRule:
        ladder = block_entropy_ladder(StreamKey.AS_SEALED, rule)
        assert ladder.is_strictly_falling is True
        assert len(ladder.per_character) == len(THE_BLOCK_SIZES)


def test_the_stride_barely_touches_one_character_and_bites_at_eight() -> None:
    shift = the_stride_shift()
    assert abs(shift[0]) < 0.01
    assert shift[-1] > 0.12
    assert shift[-1] > shift[0]


def test_the_stride_shift_grows_with_the_block_size_after_the_first_rung() -> None:
    shift = the_stride_shift()[1:]
    assert list(shift) == sorted(shift)


def test_their_ladder_agrees_with_ours_in_one_rung_of_eight_only() -> None:
    comparison = the_block_entropy_comparison()
    assert len(comparison) == len(THE_BLOCK_SIZES)
    agreeing = [row.size for row in comparison if row.standing is Verdict.AGREES]
    assert agreeing == [8]
    assert all(
        abs(row.gap) > THE_ENTROPY_TOLERANCE
        for row in comparison
        if row.size not in agreeing
    )


def test_the_quoted_ladder_carries_its_own_stride_and_corpus() -> None:
    assert THE_QUOTED_BLOCK_ENTROPY.declared_stride == SamplingRule.EVERY_SEVENTH.stride
    assert THE_QUOTED_BLOCK_ENTROPY.corpus == THE_QUOTED_ZIPF.corpus


# ---------------------------------------------------------------------------
# الأرقامُ المؤرَّخةُ وكاشفاها
# ---------------------------------------------------------------------------


def test_the_frozen_vocabulary_matches_what_the_disk_measures_now() -> None:
    assert the_vocabulary_has_drifted() is False
    census = vocabulary_census()
    assert (census.tokens, census.types, census.hapax) == THE_VOCABULARY_AT_MEASUREMENT


def test_the_frozen_ladders_match_what_the_disk_measures_now() -> None:
    assert the_ladders_have_drifted() is False
    measured = tuple(
        (fit.window, round(fit.magnitude, 4), round(fit.r_squared, 4))
        for fit in zipf_ladder()
    )
    assert measured == THE_LADDER_AT_MEASUREMENT
    stride = block_entropy_ladder(StreamKey.AS_SEALED, SamplingRule.EVERY_SEVENTH)
    assert tuple(round(value, 4) for value in stride.per_character) == (
        THE_STRIDE_LADDER_AT_MEASUREMENT
    )


def test_the_transcribed_prose_figures_are_the_measured_ones() -> None:
    """أرقامُ النثر في الوحدة تُصادَم بالمقيس، فلا تبقى زخرفةً لا يحرسها شيء."""

    from pathlib import Path

    from alghanem.arabic import zipf_block_entropy_measure as unit

    prose = Path(unit.__file__).read_text(encoding="utf-8")
    census = vocabulary_census()
    assert f"{census.tokens:,}" in prose
    assert f"{census.types:,}" in prose
    for _, magnitude, r_squared in THE_LADDER_AT_MEASUREMENT:
        assert f"{magnitude:.4f}" in prose
        assert f"{r_squared:.4f}" in prose


# ---------------------------------------------------------------------------
# الحدودُ والمفردات
# ---------------------------------------------------------------------------


def test_the_gate_is_read_and_never_moved_by_this_unit() -> None:
    assert the_corpus_gate_is_untouched() is True


def test_no_structure_here_carries_a_written_verdict_field() -> None:
    for structure in (BlockEntropyLadder, TypeTokenCensus, ZipfFit):
        names = {field.name for field in fields(structure)}
        assert not any("verdict" in name or "standing" in name for name in names)


def test_a_quoted_claim_with_no_corpus_or_more_types_than_tokens_is_refused() -> None:
    with pytest.raises(ZipfBlockEntropyError):
        QuotedZipf(
            corpus="   ",
            certificate="CERT-FR",
            magnitude=1.0,
            r_squared=0.9,
            types=10,
            tokens=100,
        )
    with pytest.raises(ZipfBlockEntropyError):
        QuotedZipf(
            corpus="x",
            certificate="CERT-FR",
            magnitude=1.0,
            r_squared=0.9,
            types=100,
            tokens=10,
        )


def test_a_ladder_of_the_wrong_length_or_a_negative_entropy_is_refused() -> None:
    with pytest.raises(ZipfBlockEntropyError):
        BlockEntropyLadder(
            key=StreamKey.AS_SEALED,
            rule=SamplingRule.EVERY_POSITION,
            per_character=(1.0, 2.0),
        )
    with pytest.raises(ZipfBlockEntropyError):
        BlockEntropyLadder(
            key=StreamKey.AS_SEALED,
            rule=SamplingRule.EVERY_POSITION,
            per_character=tuple(0.0 for _ in THE_BLOCK_SIZES),
        )


def test_every_named_residual_names_itself_in_its_own_text() -> None:
    assert len(RESIDUALS) == 5
    for name, text in RESIDUALS.items():
        assert text.startswith(f"{name}: ")
