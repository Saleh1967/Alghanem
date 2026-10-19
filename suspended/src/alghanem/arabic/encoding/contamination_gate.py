"""A positive-filter purity gate, run before any raw count over a raw text.

What this module is
-------------------
Step zero of the direct-certainty protocol
(`alghanem.program.direct_certainty`) forbids counting anything over a raw text
before the text has passed a contamination gate. This module is that gate. It
reads whitespace-separated tokens and reports, for every one of them, whether it
is admitted as a token of vocalized Arabic or rejected, and by which named
rejection. It reports one row per token, rejected rows included, on the
occurrence-complete pattern of
`alghanem.arabic.encoding.normalization.NormalizationResidualTable`: nothing is
subtracted before anyone can look at it.

Why the filter is positive and not negative
-------------------------------------------
A negative filter names the shapes of contamination it already knows, and is
blind to every shape nobody thought of. A positive filter names the single shape
the admitted token may have, and therefore needs no foreknowledge of what may
arrive. This is not argued here, it is derived:
`derive_negative_filter_blind_spots` runs both filters over
`CONTAMINATION_SAMPLE_LINES` and returns exactly the tokens that the historical
negative filter `[A-Za-z0-9]` admits and this gate rejects. A decorative rule
made of `#` and `=` holds neither a letter nor a digit, and a lone stop mark is
inside the Arabic block and is still not a word; neither is reachable by that
negative filter at all.

Why inspecting the first and last lines is not this gate
--------------------------------------------------------
Reading the head and the tail of a file is a sample, and a sample is evidence
about the positions it read and about no other position. `derive_head_tail_blind_spot`
takes the same sample and shows a contaminated line that a head-and-tail window
of any width short of the whole file does not reach. So head-and-tail inspection
may raise a suspicion, and it may not close one
(`HEAD_AND_TAIL_INSPECTION_IS_A_SAMPLE_NOT_A_GATE`).

What this module does not claim
-------------------------------
The admitted codepoint ranges and the rule "an admitted token holds at least one
Arabic letter" are declared in this module. They are not derived from any
property of Arabic and no authority issued them
(`ADMITTED_RANGES_ARE_DECLARED_NOT_DERIVED`). A token that passes this gate is
therefore *shaped* like vocalized Arabic; it is not thereby a word, not thereby
correctly transmitted, and not thereby the reading its source intends
(`ADMISSION_IS_A_SHAPE_NOT_AN_AUTHENTICATION`).

No rate over any text is recorded. This tree vendors no corpus, so no purity
figure quoted elsewhere is re-derivable here and none is written down
(`NO_CORPUS_IS_VENDORED_SO_NO_PURITY_RATE_IS_RECORDED`). `PurityScan` exists for
the day a digest arrives: it requires the source's `sha256`, byte length,
normalization form and Unicode database version, derives its counts by running
this gate rather than accepting them, and holds no percentage field.
`MEASURED_PURITY_SOURCES` is empty.
"""

from __future__ import annotations

import unicodedata
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from enum import Enum
from typing import Final

__all__ = [
    "ADMISSION_IS_A_SHAPE_NOT_AN_AUTHENTICATION",
    "ADMITTED_ARABIC_RANGES",
    "ADMITTED_RANGES_ARE_DECLARED_NOT_DERIVED",
    "CONTAMINATION_GATE_NAMED_RESIDUALS",
    "CONTAMINATION_SAMPLE_LINES",
    "HEAD_AND_TAIL_INSPECTION_IS_A_SAMPLE_NOT_A_GATE",
    "MEASURED_PURITY_SOURCES",
    "NEGATIVE_FILTER_DESCRIPTION",
    "NO_CORPUS_IS_VENDORED_SO_NO_PURITY_RATE_IS_RECORDED",
    "REJECTION_IS_NOT_A_DELETION",
    "ContaminationGateError",
    "PurityReport",
    "PurityScan",
    "TokenPurityRow",
    "TokenRejection",
    "derive_head_tail_blind_spot",
    "derive_negative_filter_blind_spots",
    "head_and_tail_lines",
    "is_admitted_codepoint",
    "is_arabic_letter",
    "negative_filter_rejects",
    "scan_lines",
    "scan_tokens",
    "tokenize",
]


class ContaminationGateError(ValueError):
    """A purity row or scan was asked to hold something it cannot hold."""


# --- the declared positive shape -------------------------------------------


ADMITTED_ARABIC_RANGES: Final[tuple[tuple[int, int], ...]] = (
    (0x0600, 0x06FF),  # Arabic
    (0x0750, 0x077F),  # Arabic Supplement
    (0x08A0, 0x08FF),  # Arabic Extended-A
    (0xFB50, 0xFDFF),  # Arabic Presentation Forms-A
    (0xFE70, 0xFEFF),  # Arabic Presentation Forms-B
)
"""The codepoint ranges an admitted token may be built from, declared here."""


def is_admitted_codepoint(char: str) -> bool:
    """Does this single character fall inside a declared Arabic range?"""
    if len(char) != 1:
        raise ContaminationGateError("a codepoint test reads exactly one character")
    point = ord(char)
    return any(low <= point <= high for low, high in ADMITTED_ARABIC_RANGES)


def is_arabic_letter(char: str) -> bool:
    """Is this character an Arabic letter, as opposed to a mark or a digit?

    A vowel mark, a stop mark, an end-of-verse sign and an Arabic-Indic digit
    all sit inside the declared ranges and none of them is a letter. A token
    that holds no letter at all is not a word, whatever block it came from.
    """
    return is_admitted_codepoint(char) and unicodedata.category(char) == "Lo"


class TokenRejection(Enum):
    """Why a token is not admitted as a token of vocalized Arabic."""

    EMPTY_TOKEN = "empty_token"
    NON_ARABIC_CODEPOINT = "non_arabic_codepoint"
    NO_ARABIC_LETTER = "no_arabic_letter"


# --- one token --------------------------------------------------------------


@dataclass(frozen=True)
class TokenPurityRow:
    """One token, admitted or rejected by name, kept either way.

    `offending` holds the codepoints that reached the rejection, so a reader can
    see what the gate saw rather than take the verdict on trust. It is empty for
    an admitted row and for a rejection that no single codepoint caused.
    """

    index: int
    token: str
    rejection: TokenRejection | None
    offending: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.index < 0:
            raise ContaminationGateError("a token index is never negative")
        if self.rejection is None and self.offending:
            raise ContaminationGateError(
                "an admitted token names no offending codepoint"
            )

    @property
    def is_admitted(self) -> bool:
        """Was this token admitted for counting?"""
        return self.rejection is None


def _classify(token: str) -> tuple[TokenRejection | None, tuple[str, ...]]:
    if not token:
        return TokenRejection.EMPTY_TOKEN, ()
    offending = tuple(
        dict.fromkeys(char for char in token if not is_admitted_codepoint(char))
    )
    if offending:
        return TokenRejection.NON_ARABIC_CODEPOINT, offending
    if not any(is_arabic_letter(char) for char in token):
        return TokenRejection.NO_ARABIC_LETTER, tuple(dict.fromkeys(token))
    return None, ()


def tokenize(text: str) -> tuple[str, ...]:
    """Split on whitespace only, dropping nothing else.

    The gate has to see what the file holds, so no character class is removed
    before the classification runs: a token that is entirely a decorative rule
    must arrive at the gate to be rejected by it.
    """
    return tuple(text.split())


# --- the occurrence-complete report -----------------------------------------


@dataclass(frozen=True)
class PurityReport:
    """One row per token read, rejected rows kept beside admitted ones."""

    rows: tuple[TokenPurityRow, ...]

    def __iter__(self) -> Iterator[TokenPurityRow]:
        return iter(self.rows)

    @property
    def admitted(self) -> tuple[TokenPurityRow, ...]:
        """The rows a later count may read."""
        return tuple(row for row in self.rows if row.is_admitted)

    @property
    def rejected(self) -> tuple[TokenPurityRow, ...]:
        """The rows this gate stopped, kept and not deleted."""
        return tuple(row for row in self.rows if not row.is_admitted)

    def rejection_counts(self) -> dict[TokenRejection, int]:
        """How many tokens each named rejection reached, zeros included."""
        counts = {rejection: 0 for rejection in TokenRejection}
        for row in self.rejected:
            assert row.rejection is not None
            counts[row.rejection] += 1
        return counts


def scan_tokens(tokens: Iterable[str]) -> PurityReport:
    """Classify every token in order and keep every row."""
    rows: list[TokenPurityRow] = []
    for index, token in enumerate(tokens):
        rejection, offending = _classify(token)
        rows.append(
            TokenPurityRow(
                index=index,
                token=token,
                rejection=rejection,
                offending=offending,
            )
        )
    return PurityReport(rows=tuple(rows))


def scan_lines(lines: Iterable[str]) -> PurityReport:
    """Tokenize every line and classify the tokens as one ordered report."""
    tokens: list[str] = []
    for line in lines:
        tokens.extend(tokenize(line))
    return scan_tokens(tokens)


# --- the negative filter, kept only to derive where it is blind --------------


NEGATIVE_FILTER_DESCRIPTION: Final[str] = (
    "reject a token that holds a Latin letter or an ASCII digit ([A-Za-z0-9])"
)
"""The historical negative filter, named so its blind spots can be derived."""


def negative_filter_rejects(token: str) -> bool:
    """Would the negative filter have stopped this token?"""
    return any(("a" <= c <= "z") or ("A" <= c <= "Z") or c.isdigit() for c in token)


CONTAMINATION_SAMPLE_LINES: Final[tuple[str, ...]] = (
    "\u0628\u0650\u0633\u0652\u0645\u0650 \u0671\u0644\u0644\u064e\u0651\u0647\u0650",
    "\u0671\u0644\u0652\u062d\u064e\u0645\u0652\u062f\u064f "
    "\u0644\u0650\u0644\u064e\u0651\u0647\u0650",
    "\u0648\u064e\u0645\u064e\u0627 \u0623\u064e\u062f\u0652\u0631\u064e\u0649\u0670"
    "\u0643\u064e \u06d6",
    "#=====================================",
    "# PLEASE DO NOT REMOVE THIS NOTICE",
    "# Copyright (C) 2007-2015 Tanzil Project",
    "#=====================================",
)
"""A sample shaped like the incident: Arabic lines, a decorative rule, a notice.

The contaminated lines are placed at the end, which is where a head-only
inspection does not look. The Arabic content is short and ordinary; nothing here
is a corpus and nothing here supports a rate.
"""


def derive_negative_filter_blind_spots(
    lines: Iterable[str] = CONTAMINATION_SAMPLE_LINES,
) -> tuple[tuple[str, TokenRejection], ...]:
    """Return the tokens this gate rejects that the negative filter admits.

    This is the derivation behind the rule, not a restatement of it. Over
    `CONTAMINATION_SAMPLE_LINES` the negative filter reaches the English notice
    and stops there: a rule of `#` and `=` holds no Latin letter and no digit,
    and a lone stop mark is inside the Arabic block and is still not a word. A
    filter that names contamination has to be extended for every shape nobody
    anticipated; a filter that names the admitted shape does not.
    """
    blind: list[tuple[str, TokenRejection]] = []
    for row in scan_lines(lines).rejected:
        assert row.rejection is not None
        if not negative_filter_rejects(row.token):
            blind.append((row.token, row.rejection))
    return tuple(blind)


def head_and_tail_lines(
    lines: Iterable[str], window: int
) -> tuple[tuple[int, str], ...]:
    """Return the first and last `window` lines, each with its line number."""
    if window < 1:
        raise ContaminationGateError("an inspection window reads at least one line")
    numbered = tuple(enumerate(lines))
    if len(numbered) <= 2 * window:
        return numbered
    return numbered[:window] + numbered[-window:]


def derive_head_tail_blind_spot(
    lines: Iterable[str] = CONTAMINATION_SAMPLE_LINES,
    window: int = 1,
) -> tuple[int, ...]:
    """Return the line numbers holding rejected tokens that the window misses.

    Head-and-tail inspection is a sample. Its silence is evidence about the
    lines it read and about no others, so it can raise a suspicion and cannot
    close one. A non-empty result here is that fact derived rather than asserted.
    """
    materialized = tuple(lines)
    inspected = {number for number, _ in head_and_tail_lines(materialized, window)}
    missed: list[int] = []
    for number, line in enumerate(materialized):
        if number in inspected:
            continue
        if scan_tokens(tokenize(line)).rejected:
            missed.append(number)
    return tuple(missed)


# --- measurement, withheld until a digest arrives ---------------------------


@dataclass(frozen=True)
class PurityScan:
    """A gate run over one source text, re-derivable only by a holder of its bytes.

    The pattern is `alghanem.arabic.level_two_source_texts.QaydAttributionScan`
    and `alghanem.arabic.encoding.sakin_adjacency.SakinClashScan`: the text is
    not vendored, and the digest, byte length, normalization form and Unicode
    database version are what let a reader re-derive the counts. The counts are
    produced by running the gate rather than accepted, and no percentage is a
    field, because a stored rate is a figure nobody can check.
    """

    source_id: str
    source_sha256: str
    source_byte_length: int
    normalization_form: str
    unicode_database_version: str
    token_total: int
    admitted_total: int

    def __post_init__(self) -> None:
        if not self.source_id.strip():
            raise ContaminationGateError("a scanned source carries a non-blank id")
        digest = self.source_sha256
        if len(digest) != 64 or any(
            char not in "0123456789abcdef" for char in digest.lower()
        ):
            raise ContaminationGateError("a source digest is 64 hexadecimal characters")
        if self.source_byte_length <= 0:
            raise ContaminationGateError("a scanned source has a positive byte length")
        if not self.normalization_form.strip():
            raise ContaminationGateError(
                "a scan records the normalization form it used"
            )
        if not self.unicode_database_version.strip():
            raise ContaminationGateError("a scan records the Unicode database version")
        if self.token_total < 0 or self.admitted_total < 0:
            raise ContaminationGateError("a scanned total is never negative")
        if self.admitted_total > self.token_total:
            raise ContaminationGateError("more tokens were admitted than were read")

    @property
    def rejected_total(self) -> int:
        """How many tokens the gate stopped."""
        return self.token_total - self.admitted_total

    @property
    def admitted_fraction(self) -> float:
        """The admitted share, derived on request and never stored."""
        if self.token_total == 0:
            raise ContaminationGateError("no share is derivable from an empty scan")
        return self.admitted_total / self.token_total

    @classmethod
    def measure(
        cls,
        *,
        source_id: str,
        source_sha256: str,
        source_byte_length: int,
        normalization_form: str,
        unicode_database_version: str,
        lines: Iterable[str],
    ) -> PurityScan:
        """Run the gate over the lines and derive the counts from it."""
        report = scan_lines(lines)
        return cls(
            source_id=source_id,
            source_sha256=source_sha256,
            source_byte_length=source_byte_length,
            normalization_form=normalization_form,
            unicode_database_version=unicode_database_version,
            token_total=len(report.rows),
            admitted_total=len(report.admitted),
        )


MEASURED_PURITY_SOURCES: Final[tuple[PurityScan, ...]] = ()
"""Empty: no source text was supplied with a digest, so no rate is written."""


# --- what this gate leaves open, named ---------------------------------------


ADMITTED_RANGES_ARE_DECLARED_NOT_DERIVED: Final[str] = (
    "the admitted codepoint ranges, and the rule that an admitted token holds "
    "at least one Arabic letter, are written in this module; no authority "
    "issued them and no property of Arabic derives them"
)

ADMISSION_IS_A_SHAPE_NOT_AN_AUTHENTICATION: Final[str] = (
    "an admitted token is shaped like vocalized Arabic; it is not thereby a "
    "word, not thereby correctly transmitted, and not thereby the reading its "
    "source intends"
)

HEAD_AND_TAIL_INSPECTION_IS_A_SAMPLE_NOT_A_GATE: Final[str] = (
    "reading the first and last lines of a file is evidence about the lines "
    "read and about no others; derive_head_tail_blind_spot returns the lines "
    "such a window misses, so a silent sample never closes the question"
)

REJECTION_IS_NOT_A_DELETION: Final[str] = (
    "a rejected token keeps its row and its offending codepoints, so a later "
    "reader can re-judge this gate instead of inheriting its verdict"
)

NO_CORPUS_IS_VENDORED_SO_NO_PURITY_RATE_IS_RECORDED: Final[str] = (
    "no source text is vendored in this tree, so no purity rate quoted "
    "elsewhere can be re-derived here; PurityScan holds no percentage field "
    "and MEASURED_PURITY_SOURCES is empty until a digest is supplied"
)

CONTAMINATION_GATE_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "ADMITTED_RANGES_ARE_DECLARED_NOT_DERIVED": (
        ADMITTED_RANGES_ARE_DECLARED_NOT_DERIVED
    ),
    "ADMISSION_IS_A_SHAPE_NOT_AN_AUTHENTICATION": (
        ADMISSION_IS_A_SHAPE_NOT_AN_AUTHENTICATION
    ),
    "HEAD_AND_TAIL_INSPECTION_IS_A_SAMPLE_NOT_A_GATE": (
        HEAD_AND_TAIL_INSPECTION_IS_A_SAMPLE_NOT_A_GATE
    ),
    "REJECTION_IS_NOT_A_DELETION": REJECTION_IS_NOT_A_DELETION,
    "NO_CORPUS_IS_VENDORED_SO_NO_PURITY_RATE_IS_RECORDED": (
        NO_CORPUS_IS_VENDORED_SO_NO_PURITY_RATE_IS_RECORDED
    ),
}
"""What this gate does not settle, named here rather than left to be assumed."""
