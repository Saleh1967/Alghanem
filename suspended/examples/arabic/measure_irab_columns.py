"""Re-derive the arriving i'rab figures and coverages from the fingerprinted bytes.

MASAQ annotates more than morphology: five of its columns carry i'rab —
``Syntactic_Role``, ``Case_Mood``, ``Case_Mood_Marker``, ``Phrasal_Function``
and ``Invariable_Declinable`` — and two more, ``Word_No`` and ``Column5``,
decide whether a count is a count of segments or of words. The figures frozen
in ``alghanem.arabic.irab_column_preregistration`` arrived **from the holder of
the bytes** in two consignments; they were not measured in this tree, and
freezing them is not believing them. This script re-derives each one and prints
the claim beside the derivation::

    ALGHANEM_MASAQ_PATH=/path/to/MASAQ.csv \\
        python examples/arabic/measure_irab_columns.py

The bytes are read from ``corpora/MASAQ.csv`` when they are there; the
variable above is for bytes held elsewhere. Either way the byte length and the
SHA-256 are matched before a single record is parsed.

Three standings are printed, never collapsed into one: a value that is present
and agrees, a value that is present and differs, and a value that **is not a
value of that column at all**. The third is a statement about the label, not
about the corpus — a transcription difference in spacing, hamza or vowelling
would produce it, and reading it as a zero would turn an unread name into a
measured absence.

``Morph_type`` is read before any figure: it is the one column declared full
in 100% of segments, so if it is not, the reading itself — record splitting,
embedded newlines in a quoted field — is what is at fault, not the frozen
figures, and every later difference is classed as a difference in the bytes.

A figure that differs is neither edited nor explained away: it is recorded as
it fell and classed by a rule written before it was seen — a counting-rule
difference (the word count, not the segment count, is what the claim matched),
a value-name difference (the frozen spelling is not a value of that column at
all), a difference in the bytes, or **not yet classified**, which is a class of
its own so that no difference is pushed into a box too small for it.

Coverage is printed too, and it is what keeps a count from being read as a
census of Arabic: 57 nāʾib fāʿil sit in a column filled in 1.79% of segments,
so that is 57 of what was annotated, not 57 passives in the Quran. A coverage
is compared at the precision it was declared to and no further — 84.45% is two
places — and it is never multiplied back into a count.

This script adopts no figure, issues no verdict, joins no corpus to another,
and imports nothing from ``alghanem.kernel``. Counting an annotator's
judgement is not settling it: the 1,632 "estimated ḍamma" segments are a count
of judgements about something with no written trace, and no count decides that
question.
"""

from __future__ import annotations

import sys

from alghanem.arabic.irab_column_census import (
    IrabCensusError,
    IrabValueStanding,
    column_census,
    read_anchor,
    read_coverage,
    read_figures,
    record_differences,
)
from alghanem.arabic.irab_column_preregistration import (
    A_DIFFERENCE_IS_CLASSIFIED_NOT_ABSORBED_NOTE,
    ARRIVING_COLUMN_COVERAGE,
    ARRIVING_SEGMENT_TOTAL,
    IRAB_COLUMNS,
    IRAB_PREREGISTRATION_DIGEST,
    SPELLING_CHECK_BESIDE_THE_EXPECTATION,
    STANDING,
)
from alghanem.arabic.masaq_corpus_deposit import (
    MASAQ_ATTRIBUTION,
    MASAQ_PATH_VARIABLE,
    MASAQ_RELATIVE_PATH,
    MasaqDepositError,
    masaq_records,
    read_masaq_bytes,
)


def main() -> int:
    try:
        data = read_masaq_bytes()
        records = masaq_records(data)
    except MasaqDepositError as error:
        print(f"error: {error}", file=sys.stderr)
        print(
            f"place the MASAQ.csv whose digest is deposited in "
            f"{MASAQ_RELATIVE_PATH}, or set {MASAQ_PATH_VARIABLE} to it",
            file=sys.stderr,
        )
        return 2

    print(MASAQ_ATTRIBUTION)
    print("(attribution is a licence condition, not a courtesy)")
    print(f"preregistration digest: {IRAB_PREREGISTRATION_DIGEST}")
    print(f"registration standing: {STANDING.value}")
    print(SPELLING_CHECK_BESIDE_THE_EXPECTATION)
    print()

    try:
        anchor = read_anchor(records)
    except IrabCensusError as error:
        print(f"error: {error}", file=sys.stderr)
        return 3

    if anchor.segment_total_agrees:
        print(f"  [ok] segment total: {anchor.total_records}")
    else:
        print(
            f"  [DIFFERS] segment total: {anchor.total_records} != "
            f"{ARRIVING_SEGMENT_TOTAL}"
        )
    if anchor.every_segment_is_filled:
        print(f"  [ok] anchor {anchor.column}: filled in every segment")
    else:
        print(
            f"  [DIFFERS] anchor {anchor.column}: "
            f"{anchor.filled_cells}/{anchor.total_records} segments filled, "
            f"claimed {anchor.declared_percentage}%"
        )
    if not anchor.holds:
        print(
            "  the anchor is read before the figures: a difference here "
            "indicts the reading (record splitting, embedded newlines), "
            "not the frozen figures"
        )
    print()

    try:
        readings = read_figures(records)
    except IrabCensusError as error:
        print(f"error: {error}", file=sys.stderr)
        return 3

    unresolved: list[str] = []
    for reading in readings:
        figure = reading.figure
        mark = {
            IrabValueStanding.PRESENT_AND_AGREES: "ok",
            IrabValueStanding.PRESENT_AND_DIFFERS: "DIFFERS",
            IrabValueStanding.NOT_A_VALUE_OF_THIS_COLUMN: "ABSENT LABEL",
        }[reading.standing]
        print(f"  [{mark}] {figure.label} ({figure.column})")
        print(f"         claimed: {figure.claimed_count}")
        print(f"         derived: {reading.derived_count} segments")
        if reading.word_count is not None:
            print(f"         and {reading.word_count} words (a second count)")
        print(f"         rule: {figure.counting_rule.value}")
        if not reading.agrees:
            unresolved.append(f"{figure.label}: {reading.standing.value}")
    print()

    differences = record_differences(readings, anchor=anchor)
    if differences:
        print(A_DIFFERENCE_IS_CLASSIFIED_NOT_ABSORBED_NOTE)
        for difference in differences:
            print(
                f"  [{difference.difference_class.name}] {difference.label}: "
                f"claimed {difference.claimed_count}, "
                f"derived {difference.derived_count}, "
                f"standing {difference.standing.value}"
            )
        print()

    for column in IRAB_COLUMNS:
        try:
            census = column_census(records, column.name)
        except IrabCensusError as error:
            print(f"  [STOPPED] {column.name}: {error}")
            unresolved.append(f"{column.name}: العمودُ غائبٌ عن الترويسة")
            continue
        print(
            f"  {column.name} ({column.arabic_name}): "
            f"{census.distinct_values} distinct values, "
            f"{census.annotated_segments} annotated segments, "
            f"{census.unannotated_segments} unannotated"
        )
        print(f"         limit: {column.what_it_does_not_annotate}")
    print()

    for coverage in ARRIVING_COLUMN_COVERAGE:
        try:
            reading = read_coverage(records, coverage)
        except IrabCensusError as error:
            print(f"  [STOPPED] {coverage.column}: {error}")
            unresolved.append(f"{coverage.column}: العمودُ غائبٌ عن الترويسة")
            continue
        mark = "ok" if reading.agrees else "DIFFERS"
        print(
            f"  [{mark}] coverage {coverage.column}: "
            f"claimed {coverage.declared_percentage}%, "
            f"derived {reading.measured_percentage:.4f}% "
            f"({reading.non_empty_cells}/{reading.total_records} segments)"
        )
        if not reading.agrees:
            unresolved.append(f"coverage {coverage.column}")
    print()

    if unresolved:
        print(
            f"error: {len(unresolved)} figure(s) did not re-derive: {unresolved}",
            file=sys.stderr,
        )
        return 1
    print(
        f"{len(readings)} arriving figures and "
        f"{len(ARRIVING_COLUMN_COVERAGE)} coverages re-derived from the "
        "deposited bytes"
    )
    print("this script adopts nothing and deposits no cross-corpus figure")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
