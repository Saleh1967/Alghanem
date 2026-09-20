"""اختباراتُ الموضع الثاني للسكون المُضمَر: اتّفاقٌ يُقاس، وحدٌّ يبقى مُسمًّى."""

from __future__ import annotations

import pytest

from alghanem.arabic.fath_ayah_source_text import (
    TRANSCRIPTION_STANDING as FATH_TRANSCRIPTION_STANDING,
)
from alghanem.arabic.fatiha_source_text import (
    TRANSCRIPTION_STANDING as FATIHA_TRANSCRIPTION_STANDING,
)
from alghanem.arabic.implicit_sukun_treatment import (
    SukunSource,
    VisibilityStanding,
    measured_text_census,
)
from alghanem.arabic.sukun_second_scope import (
    SECOND_SCOPE_NAMED_RESIDUALS,
    AlifReplication,
    ScopeComparison,
    SecondScopeError,
    alif_replication,
    measured_onset_comparison,
    measured_text_comparison,
    second_onset_census,
    second_text_census,
)


def test_the_second_text_is_measured_not_quoted() -> None:
    census = second_text_census()
    assert census.words == 54
    assert census.total == 104
    assert census.written == 27
    assert census.unwritten == 77
    assert census.written_share == pytest.approx(25.961538, abs=1e-6)


def test_the_sukun_is_mostly_unwritten_in_the_second_text_too() -> None:
    assert second_text_census().standing is VisibilityStanding.MOSTLY_UNWRITTEN
    assert measured_text_census().standing is VisibilityStanding.MOSTLY_UNWRITTEN


def test_the_two_scopes_sit_two_points_apart() -> None:
    comparison = measured_text_comparison()
    assert comparison.written_share_gap == pytest.approx(2.038462, abs=1e-6)
    assert comparison.words == 83


def test_the_alif_share_is_the_closest_and_the_shadda_the_furthest() -> None:
    comparison = measured_text_comparison()
    assert comparison.unwritten_share_gap(
        SukunSource.ALIF_WITHOUT_A_MARK
    ) == pytest.approx(-0.264550, abs=1e-6)
    assert comparison.unwritten_share_gap(
        SukunSource.GEMINATION_PAIR_START
    ) == pytest.approx(5.146705, abs=1e-6)
    assert comparison.unwritten_share_gap(SukunSource.BARE_CARRIER) == pytest.approx(
        -4.882155, abs=1e-6
    )


def test_the_onset_parted_further_than_the_whole_text() -> None:
    onset = measured_onset_comparison()
    assert onset.second == second_onset_census()
    assert onset.first.total == 14
    assert onset.first.written == 5
    assert onset.second.total == 12
    assert onset.second.written == 3
    assert onset.written_share_gap == pytest.approx(10.714286, abs=1e-6)
    assert abs(onset.written_share_gap) > abs(
        measured_text_comparison().written_share_gap
    )


def test_every_written_alif_in_both_texts_is_unmarked() -> None:
    fatiha, fath = alif_replication()
    assert (fatiha.alifs, fatiha.marked, fatiha.dagger_units) == (23, 0, 2)
    assert (fath.alifs, fath.marked, fath.dagger_units) == (33, 0, 0)
    assert fatiha.is_entirely_unmarked and fath.is_entirely_unmarked
    assert fatiha.unmarked + fath.unmarked == 56


def test_a_dagger_alif_is_counted_apart_and_not_erased() -> None:
    fatiha, _ = alif_replication()
    assert fatiha.dagger_units == 2
    assert fatiha.dagger_units not in (fatiha.alifs, fatiha.marked)


def test_no_alif_replication_is_read_from_an_empty_scope() -> None:
    empty = AlifReplication(scope="لا شيء", alifs=0, marked=0, dagger_units=0)
    assert not empty.is_entirely_unmarked


def test_a_scope_is_not_compared_with_itself() -> None:
    census = second_text_census()
    with pytest.raises(SecondScopeError):
        ScopeComparison(first=census, second=census)


def test_a_marked_count_above_the_alif_count_is_refused() -> None:
    with pytest.raises(SecondScopeError):
        AlifReplication(scope="مستحيل", alifs=3, marked=4, dagger_units=0)
    with pytest.raises(SecondScopeError):
        AlifReplication(scope="سالب", alifs=-1, marked=0, dagger_units=0)


def test_the_pooled_share_is_offered_only_with_its_scope() -> None:
    comparison = measured_text_comparison()
    assert comparison.pooled_written_share == pytest.approx(26.815642, abs=1e-6)
    assert comparison.words == 83
    assert comparison.words < 78_245


def test_the_split_is_still_the_output_and_no_bare_total_is_returned() -> None:
    rows = measured_text_comparison().rows()
    assert len(rows) == len(tuple(SukunSource))
    assert all(len(row) == 3 for row in rows)
    assert sum(row[1] for row in rows) == measured_text_census().total
    assert sum(row[2] for row in rows) == second_text_census().total


def test_the_two_deposits_share_one_transcription_standing() -> None:
    assert FATIHA_TRANSCRIPTION_STANDING.value == FATH_TRANSCRIPTION_STANDING.value
    assert (
        "TWO_TRANSCRIPTIONS_OF_ONE_HAND_ARE_NOT_TWO_WITNESSES"
        in SECOND_SCOPE_NAMED_RESIDUALS
    )


def test_what_this_second_scope_does_not_establish_is_named() -> None:
    assert set(SECOND_SCOPE_NAMED_RESIDUALS) == {
        "TWO_TEXTS_ARE_STILL_NOT_A_CORPUS",
        "TWO_TRANSCRIPTIONS_OF_ONE_HAND_ARE_NOT_TWO_WITNESSES",
        "A_SHARED_CODEC_IS_A_SHARED_LIMIT",
        "THE_ALIF_REPLICATION_IS_STILL_READ_FROM_ABSENCE",
        "A_GAP_BETWEEN_TWO_SCOPES_IS_NOT_A_TREND",
    }
    for key, text in SECOND_SCOPE_NAMED_RESIDUALS.items():
        assert text.startswith(f"{key}: ")


def test_the_second_scope_carries_no_authority_field() -> None:
    from dataclasses import fields

    for holder in (ScopeComparison, AlifReplication):
        names = {declared.name.lower() for declared in fields(holder)}
        for token in ("authority", "born", "birth", "gate", "rank", "verdict"):
            assert not any(token in name for name in names)


def test_the_second_scope_reads_no_kernel_module() -> None:
    import ast
    from pathlib import Path

    import alghanem.arabic.sukun_second_scope as module

    tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            assert "kernel" not in (node.module or "")
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert "kernel" not in alias.name
