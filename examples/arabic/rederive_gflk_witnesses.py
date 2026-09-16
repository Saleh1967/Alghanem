"""Re-derive, in one pass, every GFLK figure this tree can actually re-derive.

This script is reference material, not part of the kernel or the Arabic layer.
It exists because an audit of the deposited GFLK specification found that most
of its figures rest on bytes that are **not in this tree**, while a small set
rests on bytes that are. Those two sets were easy to confuse when read as
prose, so they are separated here and re-derived from the bytes on every run.

Three registers, kept apart on purpose:

``REDERIVED``
    A figure the specification names, whose bytes are in this tree, with a
    declared counting rule, re-derived here and compared. A mismatch exits
    non-zero.

``SELF_REFERENTIAL``
    A freeze check whose inputs are embedded in this repository's own source.
    Re-deriving it proves **immutability**, not truth about Arabic — the table
    is being matched against itself. It is printed under its own heading so a
    reader does not read it as an external witness.

``NOT_IN_THIS_TREE``
    A figure whose named source is absent. The absence is asserted rather than
    assumed: if such a file ever arrives, this script fails, because the figure
    would then be measurable and this register would have gone stale.

What this script does **not** do: it adopts no figure, issues no verdict,
lifts no blocked milestone, and imports nothing from ``alghanem.kernel``. That
a count re-derives shows the counter counted these bytes under this rule; it
does not show the claim built on the count is true. Each ``REDERIVED`` figure
carries its own written limit in
``alghanem.arabic.maqayis_root_table_deposit.REDERIVED_SPECIFICATION_FIGURES``.
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from dataclasses import dataclass

from alghanem.arabic.classical_makharij_table import (
    CLASSICAL_MAKHARIJ,
    CLASSICAL_TABLE_DIGEST,
    rederive_classical_table_digest,
)
from alghanem.arabic.encoding import EMBEDDED_ROUND_TRIP_CASES
from alghanem.arabic.encoding.carrier_state_candidate import round_trip_holds
from alghanem.arabic.maqayis_root_table_deposit import (
    FROZEN_ROOT_TABLE,
    REDERIVED_DISTINCT_TRILATERAL_ROOTS,
    REDERIVED_FILE_LINE_COUNT,
    REDERIVED_RECORD_COUNT,
    TRILATERAL_ROOT_TYPE,
    file_ends_with_a_line_separator,
    read_root_table_bytes,
    rederive_distinct_trilateral_roots,
    rederive_file_line_count,
    rederive_record_count,
    root_table_digest,
    root_table_rows,
)
from alghanem.arabic.pipeline_stations import repository_root_path


@dataclass(frozen=True, slots=True)
class Witness:
    """A figure, the rule that produced it, and the value re-derived now."""

    name: str
    counting_rule: str
    expected: object
    derive: Callable[[], object]


def _trilateral_row_count() -> int:
    return sum(
        1 for row in root_table_rows() if row["root_type"] == TRILATERAL_ROOT_TYPE
    )


def _duplicated_trilateral_roots() -> tuple[str, ...]:
    """The roots that occupy two rows — the whole of the 4,089/4,087 gap."""

    seen: dict[str, int] = {}
    for row in root_table_rows():
        if row["root_type"] == TRILATERAL_ROOT_TYPE:
            seen[row["root_full"]] = seen.get(row["root_full"], 0) + 1
    return tuple(sorted(root for root, count in seen.items() if count > 1))


def _round_trip_successes() -> int:
    return sum(1 for surface in EMBEDDED_ROUND_TRIP_CASES if round_trip_holds(surface))


REDERIVED: tuple[Witness, ...] = (
    Witness(
        name="Maqāyīs root table — byte length",
        counting_rule="the length of the bytes on disk, unnormalised",
        expected=FROZEN_ROOT_TABLE.byte_length,
        derive=lambda: len(read_root_table_bytes()),
    ),
    Witness(
        name="Maqāyīs root table — SHA-256",
        counting_rule="SHA-256 over those same bytes",
        expected=FROZEN_ROOT_TABLE.sha256_hex,
        derive=root_table_digest,
    ),
    Witness(
        name="Maqāyīs root table — CSV records",
        counting_rule="a record is a CSV row after the header, quotes honoured",
        expected=REDERIVED_RECORD_COUNT,
        derive=rederive_record_count,
    ),
    Witness(
        name="Maqāyīs root table — file lines",
        counting_rule="a line is a line separator in the bytes (the `wc -l` rule)",
        expected=REDERIVED_FILE_LINE_COUNT,
        derive=rederive_file_line_count,
    ),
    Witness(
        name="Maqāyīs root table — no final line separator",
        counting_rule=(
            "whether the bytes end in a separator; the two line rules differ "
            "by exactly this"
        ),
        expected=False,
        derive=file_ends_with_a_line_separator,
    ),
    Witness(
        name="Maqāyīs root table — rows typed ثلاثي",
        counting_rule="rows, not distinct roots",
        expected=4_089,
        derive=_trilateral_row_count,
    ),
    Witness(
        name="Maqāyīs root table — distinct trilateral roots",
        counting_rule="distinct `root_full` values among those rows",
        expected=REDERIVED_DISTINCT_TRILATERAL_ROOTS,
        derive=rederive_distinct_trilateral_roots,
    ),
    Witness(
        name="Maqāyīs root table — the roots behind the 4,089/4,087 gap",
        counting_rule="the roots appearing in more than one row, named not counted",
        expected=("بنى", "كتو"),
        derive=_duplicated_trilateral_roots,
    ),
    Witness(
        name="Embedded round-trip cases that hold",
        counting_rule="`round_trip_holds` over `EMBEDDED_ROUND_TRIP_CASES`",
        expected=len(EMBEDDED_ROUND_TRIP_CASES),
        derive=_round_trip_successes,
    ),
)


SELF_REFERENTIAL: tuple[Witness, ...] = (
    Witness(
        name="Classical makhārij table — frozen digest",
        counting_rule=(
            "SHA-256 over the table's own ordinals, embedded in this "
            "repository's source; matching it proves immutability, not phonetics"
        ),
        expected=CLASSICAL_TABLE_DIGEST,
        derive=rederive_classical_table_digest,
    ),
    Witness(
        name="Classical makhārij table — members",
        counting_rule="entries in `CLASSICAL_MAKHARIJ`, likewise embedded here",
        expected=len(CLASSICAL_MAKHARIJ),
        derive=lambda: len(CLASSICAL_MAKHARIJ),
    ),
)


NOT_IN_THIS_TREE: tuple[tuple[str, str], ...] = (
    (
        "quran-simple-enhanced.txt",
        (
            "the compression ladder (85.11 / 87.67 / 88.01 / 88.34%) and the "
            "four jarād/mazīd corpus counts"
        ),
    ),
    ("quranic-corpus-morphology-0.4.txt", "the iʿrāb corpus witness"),
)
"""Named sources the specification measures against, whose bytes are absent.

The codec revision audit's 99.992251% is a neighbour of this register worth
naming: the arithmetic ``(77429 - 6) / 77429`` re-derives here, but the 77,429
itself was measured against a corpus that is not in this tree. The computation
is reproducible; the measurement is not.
"""


def _report(heading: str, witnesses: tuple[Witness, ...]) -> list[str]:
    failures: list[str] = []
    print(heading)
    for witness in witnesses:
        derived = witness.derive()
        holds = derived == witness.expected
        print(f"  [{'ok' if holds else 'DRIFT'}] {witness.name}: {derived!r}")
        print(f"         rule: {witness.counting_rule}")
        if not holds:
            failures.append(f"{witness.name}: expected {witness.expected!r}")
    print()
    return failures


def main() -> int:
    failures = _report(
        "re-derived from bytes in this tree (real witnesses):", REDERIVED
    )
    failures.extend(
        _report(
            "self-referential freeze checks (immutability, NOT external witnesses):",
            SELF_REFERENTIAL,
        )
    )

    print("named sources absent from this tree, so their figures stay uncarried:")
    root = repository_root_path()
    for source_name, what_it_would_carry in NOT_IN_THIS_TREE:
        present = [
            path.relative_to(root).as_posix() for path in root.rglob(source_name)
        ]
        if present:
            failures.append(
                f"{source_name} is now present at {present}: this register is "
                "stale and the figure it withholds may be measurable"
            )
            print(f"  [DRIFT] {source_name} has arrived at {present}")
        else:
            print(f"  [absent] {source_name} — withholds {what_it_would_carry}")
    print()

    if failures:
        print(
            f"error: {len(failures)} witness(es) drifted: {failures}", file=sys.stderr
        )
        return 1
    print(
        f"{len(REDERIVED)} figures re-derived, {len(SELF_REFERENTIAL)} freeze checks "
        f"held, {len(NOT_IN_THIS_TREE)} named sources still absent"
    )
    print("this script adopts no figure and lifts no blocked milestone")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
