"""Re-derive the Maqāyīs witness census from bytes that are already here.

``maqayis_by_root_csv_999.csv`` is in this tree and fingerprinted, so unlike the
MASAQ figures these counts need no declaration and no waiting. This script
re-derives each of them and prints it beside the counting rule that produced it
and the written limit on what it still does not establish::

    python examples/arabic/measure_maqayis_witnesses.py

**No claim preceded these numbers.** The i'rab figures were transmitted before
they were measured, so matching them tested a transmitter. These were measured
here first; a figure that re-derives shows only that the count is tied to a
digest and to a rule, not that anyone was proved right. The rules themselves
were written **after** the file was looked at, which is recorded rather than
hidden: what keeps a rule from having been cut to fit a pleasing number is that
it is written out in full and every figure is re-derived from fingerprinted
bytes, so a reader who rejects the rule rejects the number with it.

Three things are printed that a single number would hide. The separators ``|``
and ``…`` are the file producer's, not the poets': a segment count is a count of
his separators, so the segments bearing the hemistich marker are counted beside
the segments themselves, and their equality raises — but does not close — the
question of a bar falling inside a line. A segment is not a verse: its metre,
its attribution and its completeness are unverified, so 4,176 is a count of
segments in a file, not of witnesses in Arabic or in Ibn Fāris. And a blank is
not a zero: the records that declare no ``axes_count`` are a third class of
their own, never folded into agreement or into disagreement, which is why no
agreement ratio is printed here — the denominator itself would be in dispute.

Where the file's own declared ``axes_count`` disagrees with the segments of its
own ``semantic_axes`` cell, the difference is printed with its size and its
largest identified kind, and neither side is adjusted to remove it.

This script re-derives nothing about MASAQ. Those bytes are still absent and
their tests are still skipped on the bytes themselves; a figure reached from one
file does not stand in for the bytes of another. It adopts no figure, issues no
verdict, and imports nothing from ``alghanem.kernel``.
"""

from __future__ import annotations

import sys

from alghanem.arabic.maqayis_root_table_deposit import (
    REDERIVED_RECORD_COUNT,
    MaqayisRootTableError,
    root_table_digest,
)
from alghanem.arabic.maqayis_witness_census import (
    BLANK_AXES_WITH_A_DECLARED_ONE,
    FROZEN_AXES_AGREEMENT,
    MAQAYIS_WITNESS_NAMED_RESIDUALS,
    MEASURED_WITNESS_FIGURES,
    RECORDS_CARRYING_POETRY_EVIDENCE,
    ROOT_TYPE_CENSUS,
    SEGMENTS_BEARING_THE_HEMISTICH_MARKER,
    WITNESS_SEGMENTS,
    count_blank_axes_with_a_declared_one,
    count_records_carrying_poetry_evidence,
    count_segments_bearing_the_hemistich_marker,
    count_witness_segments,
    measure_axes_agreement,
    rederive_root_type_census,
)


def main() -> int:
    try:
        digest = root_table_digest()
        records_with_evidence = count_records_carrying_poetry_evidence()
        segments = count_witness_segments()
        marked_segments = count_segments_bearing_the_hemistich_marker()
        census = rederive_root_type_census()
        agreement = measure_axes_agreement()
        blank_with_one = count_blank_axes_with_a_declared_one()
    except MaqayisRootTableError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    print(f"root table digest: {digest}")
    print("no claim preceded these numbers; they were measured here first")
    print("the counting rules were written after the file was seen")
    print()

    drifted: list[str] = []
    for measured, frozen, name in (
        (records_with_evidence, RECORDS_CARRYING_POETRY_EVIDENCE, "witness records"),
        (segments, WITNESS_SEGMENTS, "witness segments"),
        (
            marked_segments,
            SEGMENTS_BEARING_THE_HEMISTICH_MARKER,
            "segments bearing the hemistich marker",
        ),
        (blank_with_one, BLANK_AXES_WITH_A_DECLARED_ONE, "blank axes declared as 1"),
    ):
        mark = "ok" if measured == frozen else "DIFFERS"
        print(f"  [{mark}] {name}: {measured} (frozen {frozen})")
        if measured != frozen:
            drifted.append(name)
    print()

    if segments == marked_segments:
        print(
            f"  every one of the {segments} segments bears the hemistich marker; "
            "this raises the likelihood that the bar fell where expected, and "
            "closes nothing"
        )
    else:
        print(
            f"  {marked_segments} of {segments} segments bear the hemistich "
            "marker: some segment was cut where no hemistich break is written"
        )
    print()

    total = 0
    for value, count in census:
        print(f"  root_type {value}: {count} rows")
        total += count
    mark = "ok" if census == ROOT_TYPE_CENSUS else "DIFFERS"
    print(
        f"  [{mark}] the four classes sum to {total} of {REDERIVED_RECORD_COUNT} rows"
    )
    if census != ROOT_TYPE_CENSUS:
        drifted.append("root_type census")
    if total != REDERIVED_RECORD_COUNT:
        drifted.append("root_type census total")
    print()

    mark = "ok" if agreement == FROZEN_AXES_AGREEMENT else "DIFFERS"
    print(
        f"  [{mark}] declared axes_count against its own semantic_axes cell: "
        f"{agreement.agreeing} agreeing, {agreement.differing} differing, "
        f"{agreement.blank} blank"
    )
    print(
        f"         {blank_with_one} of the {agreement.differing} differing "
        "records have an empty axes cell and a declared 1"
    )
    print(
        "         a blank is a third class, not a zero, so no agreement ratio "
        "is printed: the denominator itself is in dispute"
    )
    if agreement != FROZEN_AXES_AGREEMENT:
        drifted.append("axes agreement")
    print()

    for figure in MEASURED_WITNESS_FIGURES:
        print(f"  {figure.figure} ({figure.measured_count})")
        print(f"         rule: {figure.counting_rule}")
        print(
            f"         still not established: {figure.what_it_still_does_not_establish}"
        )
    print()

    for name in sorted(MAQAYIS_WITNESS_NAMED_RESIDUALS):
        print(f"  residual: {name}")
    print()

    if drifted:
        print(
            f"error: {len(drifted)} figure(s) did not re-derive: {drifted}",
            file=sys.stderr,
        )
        return 1
    print(
        f"{len(MEASURED_WITNESS_FIGURES)} measured figures re-derived from the "
        "fingerprinted root table"
    )
    print("the MASAQ bytes remain absent; nothing here stands in for them")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
