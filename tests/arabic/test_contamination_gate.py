"""Tests for the positive-filter contamination gate."""

from __future__ import annotations

import pytest

from alghanem.arabic.encoding.contamination_gate import (
    ADMITTED_ARABIC_RANGES,
    CONTAMINATION_GATE_NAMED_RESIDUALS,
    CONTAMINATION_SAMPLE_LINES,
    MEASURED_PURITY_SOURCES,
    ContaminationGateError,
    PurityScan,
    TokenPurityRow,
    TokenRejection,
    derive_head_tail_blind_spot,
    derive_negative_filter_blind_spots,
    head_and_tail_lines,
    is_admitted_codepoint,
    is_arabic_letter,
    negative_filter_rejects,
    scan_lines,
    scan_tokens,
    tokenize,
)

_BISM = "\u0628\u0650\u0633\u0652\u0645\u0650"  # بِسْمِ
_STOP_MARK = "\u06d6"  # ۖ
_DECORATIVE_RULE = "#====="
_ARABIC_INDIC_ONE = "\u0661"  # ١
_TATWEEL = "\u0640"


# --- the positive shape ------------------------------------------------------


def test_the_admitted_ranges_are_arabic_only() -> None:
    assert is_admitted_codepoint("\u0628")
    assert is_admitted_codepoint(_STOP_MARK)
    assert not is_admitted_codepoint("a")
    assert not is_admitted_codepoint("#")
    assert not is_admitted_codepoint("=")
    for low, high in ADMITTED_ARABIC_RANGES:
        assert low <= high


def test_a_codepoint_test_reads_exactly_one_character() -> None:
    with pytest.raises(ContaminationGateError, match="exactly one character"):
        is_admitted_codepoint("ab")


def test_a_mark_a_digit_and_a_tatweel_are_in_range_and_are_not_letters() -> None:
    for char in (_STOP_MARK, _ARABIC_INDIC_ONE, _TATWEEL):
        assert is_admitted_codepoint(char)
        assert not is_arabic_letter(char)
    assert is_arabic_letter("\u0628")


# --- one row per token, rejected rows kept -----------------------------------


def test_every_token_gets_a_row_and_no_row_is_subtracted() -> None:
    tokens = (_BISM, "Copyright", _DECORATIVE_RULE, _STOP_MARK)
    report = scan_tokens(tokens)
    assert len(report.rows) == len(tokens)
    assert tuple(row.token for row in report.rows) == tokens
    assert len(report.admitted) + len(report.rejected) == len(report.rows)


def test_each_rejection_names_what_the_gate_saw() -> None:
    report = scan_tokens(("Copyright", _DECORATIVE_RULE, _STOP_MARK, ""))
    by_token = {row.token: row for row in report.rows}
    assert by_token["Copyright"].rejection is TokenRejection.NON_ARABIC_CODEPOINT
    assert "C" in by_token["Copyright"].offending
    assert by_token[_DECORATIVE_RULE].rejection is TokenRejection.NON_ARABIC_CODEPOINT
    assert set(by_token[_DECORATIVE_RULE].offending) == {"#", "="}
    assert by_token[_STOP_MARK].rejection is TokenRejection.NO_ARABIC_LETTER
    assert by_token[""].rejection is TokenRejection.EMPTY_TOKEN


def test_an_arabic_word_is_admitted_with_its_vowel_marks() -> None:
    report = scan_tokens((_BISM,))
    assert report.rows[0].is_admitted
    assert report.rejected == ()


def test_a_number_written_in_arabic_indic_digits_is_not_a_word() -> None:
    report = scan_tokens((_ARABIC_INDIC_ONE + _ARABIC_INDIC_ONE,))
    assert report.rows[0].rejection is TokenRejection.NO_ARABIC_LETTER


def test_rejection_counts_keep_the_zeros_readable() -> None:
    counts = scan_tokens((_BISM,)).rejection_counts()
    assert set(counts) == set(TokenRejection)
    assert all(value == 0 for value in counts.values())


def test_an_admitted_row_may_not_name_an_offending_codepoint() -> None:
    with pytest.raises(ContaminationGateError, match="offending codepoint"):
        TokenPurityRow(index=0, token=_BISM, rejection=None, offending=("#",))


def test_a_token_index_is_never_negative() -> None:
    with pytest.raises(ContaminationGateError, match="never negative"):
        TokenPurityRow(index=-1, token=_BISM, rejection=None)


def test_tokenizing_drops_nothing_but_whitespace() -> None:
    assert tokenize(f"  {_BISM}\t{_DECORATIVE_RULE}\n") == (_BISM, _DECORATIVE_RULE)


# --- the derivation that settles positive against negative -------------------


def test_the_negative_filter_is_blind_to_shapes_it_never_named() -> None:
    blind = derive_negative_filter_blind_spots()
    assert blind != ()
    tokens = {token for token, _ in blind}
    assert _STOP_MARK in tokens
    assert any(token.startswith("#") for token in tokens)
    for token, _ in blind:
        assert not negative_filter_rejects(token)


def test_the_negative_filter_does_reach_the_latin_notice() -> None:
    assert negative_filter_rejects("Copyright")
    assert negative_filter_rejects("2007-2015")
    assert not negative_filter_rejects(_DECORATIVE_RULE)
    assert not negative_filter_rejects(_STOP_MARK)


def test_the_positive_gate_reaches_every_contaminated_token_in_the_sample() -> None:
    report = scan_lines(CONTAMINATION_SAMPLE_LINES)
    assert report.rejected != ()
    for row in report.admitted:
        assert not negative_filter_rejects(row.token)
        assert any(is_arabic_letter(char) for char in row.token)


# --- head and tail inspection is a sample, derived not asserted --------------


def test_a_head_and_tail_window_misses_lines_that_hold_contamination() -> None:
    missed = derive_head_tail_blind_spot(CONTAMINATION_SAMPLE_LINES, window=1)
    assert missed != ()
    for number in missed:
        assert scan_lines((CONTAMINATION_SAMPLE_LINES[number],)).rejected != ()


def test_a_wide_enough_window_reads_the_whole_file_and_misses_nothing() -> None:
    window = len(CONTAMINATION_SAMPLE_LINES)
    assert derive_head_tail_blind_spot(CONTAMINATION_SAMPLE_LINES, window) == ()
    inspected = head_and_tail_lines(CONTAMINATION_SAMPLE_LINES, window)
    assert len(inspected) == len(CONTAMINATION_SAMPLE_LINES)


def test_an_inspection_window_reads_at_least_one_line() -> None:
    with pytest.raises(ContaminationGateError, match="at least one line"):
        head_and_tail_lines(CONTAMINATION_SAMPLE_LINES, 0)


# --- measurement withheld until a digest arrives ------------------------------


_DIGEST = "0" * 64


def test_no_purity_rate_is_recorded_in_this_tree() -> None:
    assert MEASURED_PURITY_SOURCES == ()
    assert not any(
        "percent" in name.lower() or "rate" in name.lower()
        for name in PurityScan.__dataclass_fields__
    )


def test_a_scan_derives_its_counts_by_running_the_gate() -> None:
    scan = PurityScan.measure(
        source_id="sample",
        source_sha256=_DIGEST,
        source_byte_length=len("".join(CONTAMINATION_SAMPLE_LINES).encode("utf-8")),
        normalization_form="NFC",
        unicode_database_version="15.0.0",
        lines=CONTAMINATION_SAMPLE_LINES,
    )
    report = scan_lines(CONTAMINATION_SAMPLE_LINES)
    assert scan.token_total == len(report.rows)
    assert scan.admitted_total == len(report.admitted)
    assert scan.rejected_total == len(report.rejected)
    assert 0.0 < scan.admitted_fraction < 1.0


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("source_id", "  ", "non-blank id"),
        ("source_sha256", "abc", "64 hexadecimal"),
        ("source_byte_length", 0, "positive byte length"),
        ("normalization_form", " ", "normalization form"),
        ("unicode_database_version", " ", "Unicode database version"),
    ],
)
def test_a_scan_without_its_provenance_is_refused(
    field: str, value: object, message: str
) -> None:
    kwargs: dict[str, object] = {
        "source_id": "sample",
        "source_sha256": _DIGEST,
        "source_byte_length": 10,
        "normalization_form": "NFC",
        "unicode_database_version": "15.0.0",
        "token_total": 4,
        "admitted_total": 2,
    }
    kwargs[field] = value
    with pytest.raises(ContaminationGateError, match=message):
        PurityScan(**kwargs)  # type: ignore[arg-type]


def test_more_tokens_admitted_than_read_is_refused() -> None:
    with pytest.raises(ContaminationGateError, match="admitted than were read"):
        PurityScan(
            source_id="sample",
            source_sha256=_DIGEST,
            source_byte_length=10,
            normalization_form="NFC",
            unicode_database_version="15.0.0",
            token_total=2,
            admitted_total=3,
        )


def test_no_share_is_derivable_from_an_empty_scan() -> None:
    scan = PurityScan(
        source_id="sample",
        source_sha256=_DIGEST,
        source_byte_length=10,
        normalization_form="NFC",
        unicode_database_version="15.0.0",
        token_total=0,
        admitted_total=0,
    )
    with pytest.raises(ContaminationGateError, match="empty scan"):
        _ = scan.admitted_fraction


# --- what the gate leaves open -----------------------------------------------


def test_every_named_residual_is_reachable_and_says_something() -> None:
    assert len(CONTAMINATION_GATE_NAMED_RESIDUALS) == 5
    for name, text in CONTAMINATION_GATE_NAMED_RESIDUALS.items():
        assert name.isupper()
        assert len(text) > 40
