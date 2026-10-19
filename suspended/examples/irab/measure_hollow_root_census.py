"""Re-derive the frozen `hollow_root_root_census` counts from the corpus itself.

This script is reference material, not part of the kernel or the Arabic layer.
It derives no kernel object, licenses no transition, and asserts no Arabic
cardinality. It only recomputes the numbers frozen in
``src/alghanem/arabic/hollow_root_root_census.py`` and fails loudly if they
drift.

The corpus is deliberately **not** vendored: the Quranic Arabic Corpus is
GPL-licensed and the Tanzil Uthmani text it embeds is CC BY-ND, and both forbid
modification. Obtain the exact file named in
``alghanem.arabic.irab_corpus_witness.QURANIC_ARABIC_CORPUS_WITNESS``, then::

    python examples/irab/measure_hollow_root_census.py path/to/morphology-0.4.txt

The script verifies the recorded SHA-256 and byte length first and refuses to
report numbers for any other file, so a silently updated corpus cannot be
mistaken for the frozen census.

What a match does establish: one side of each competing hollow-root pair is not
tagged in this corpus at all. What it does not establish: any rule that takes a
surface form and returns its root. See
``THE_CENSUS_IS_NOT_A_ROOT_EXTRACTOR_NOTE``.

Source: the Quranic Arabic Corpus, http://corpus.quran.com — built on the
Tanzil Quran text, http://tanzil.info. Both attributions are conditions of the
licences above, not courtesies.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from alghanem.arabic.hollow_root_root_census import (
    COMPETING_ROOT_PAIRS,
    QYL_EXAMINED_OCCURRENCES,
    REDERIVED_ROOT_COUNTS,
    REDERIVED_SEGMENT_COUNT,
    HollowRootCensusError,
    RootCensusRow,
    RootCountingRule,
    census_rows,
    corpus_lines,
    parse_segment_line,
    rederive_segment_count,
)
from alghanem.arabic.irab_corpus_witness import QURANIC_ARABIC_CORPUS_WITNESS


def _requested_roots() -> tuple[tuple[str, str], ...]:
    roots: list[tuple[str, str]] = []
    for pair in COMPETING_ROOT_PAIRS:
        roots.append((pair.waw_root_buckwalter, pair.waw_root_arabic))
        roots.append((pair.ya_root_buckwalter, pair.ya_root_arabic))
    return tuple(roots)


def _format_row(row: RootCensusRow) -> str:
    return (
        f"{row.root_buckwalter:>4} ({row.root_arabic})  "
        f"segments={row.count_under(RootCountingRule.SEGMENTS):>6}  "
        f"words={row.count_under(RootCountingRule.WORDS):>6}  "
        f"verses={row.count_under(RootCountingRule.VERSES):>6}"
        + (f"  at {', '.join(row.locations)}" if row.locations else "")
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "corpus",
        type=Path,
        help="path to the exact quranic-corpus-morphology-0.4.txt bytes",
    )
    arguments = parser.parse_args(argv)

    try:
        lines = corpus_lines(arguments.corpus)
    except HollowRootCensusError as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2

    witness = QURANIC_ARABIC_CORPUS_WITNESS
    print(f"corpus: {witness.corpus} {witness.version}")
    print(f"sha256: {witness.sha256}")
    print(f"bytes:  {witness.byte_length}")
    print("source: http://corpus.quran.com — text: http://tanzil.info")
    print()

    segment_count = rederive_segment_count(lines)
    records = [
        record
        for record in (parse_segment_line(line) for line in lines)
        if record is not None
    ]
    rows = census_rows(records, _requested_roots())

    print(f"segments: {segment_count} (frozen {REDERIVED_SEGMENT_COUNT})")
    for row in rows:
        print(_format_row(row))
    print()
    for occurrence in QYL_EXAMINED_OCCURRENCES:
        print(f"{occurrence.location} {occurrence.form_arabic}: {occurrence.features}")

    drifted = False
    if segment_count != REDERIVED_SEGMENT_COUNT:
        print(
            f"DRIFT: segment count {segment_count} != {REDERIVED_SEGMENT_COUNT}",
            file=sys.stderr,
        )
        drifted = True
    if rows != REDERIVED_ROOT_COUNTS:
        print("DRIFT: root counts differ from the frozen census", file=sys.stderr)
        drifted = True
    if drifted:
        return 1

    print()
    print("the frozen census re-derives exactly from these bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
