"""Check the jarād/mazīd criterion against its frozen inputs and worked examples.

This script is reference material, not part of the kernel or the Arabic layer.
It issues **no corpus figure**: the four deposited counts (recorded, not
adopted, in ``alghanem.arabic.gflk_specification_deposit``) still lack a
``MeasurementRunManifest`` and a written pre-measurement expectation, which are
two of the four prerequisites frozen in
``alghanem.arabic.jarad_mazid_preregistration.PublicationPrerequisite``.

What it does check, exiting non-zero on any drift:

* the preregistration digest matches the criterion the tool reports using;
* the Maqāyīs root table still verifies byte length, SHA-256 and header;
* a small set of worked examples still reads the way the criterion says —
  a slot is a real consonant **or a madd**, matching is on the full skeleton,
  and a root that is a prefix of a longer skeleton is never reported as an
  exact match.

The permanent limit is restated here because the script is the place a reader
meets the numbers: this criterion measures **length only** and says nothing
about whether a given wāw or yāʾ is root or augment.
"""

from __future__ import annotations

import sys

from alghanem.arabic.jarad_mazid import (
    RootMatchKind,
    SlotCount,
    read_jarad_mazid,
    root_skeletons,
)
from alghanem.arabic.jarad_mazid_preregistration import (
    CORPUS_BUCKET_RULES,
    PREREGISTRATION_DIGEST,
    preregistration_digest,
    root_table_reference,
)

_WORKED_EXAMPLES: tuple[tuple[str, str, SlotCount, bool], ...] = (
    ("كَتَبَ", "كتب", SlotCount.MUJARRAD, True),
    ("كِتَابٌ", "كتاب", SlotCount.MAZID, False),
    ("نَارًا", "نار", SlotCount.MUJARRAD, False),
    ("اسْتَغْفَرَ", "استغفر", SlotCount.MAZID, False),
)


def main() -> int:
    """Re-derive the criterion's frozen inputs and re-read the worked examples."""

    if preregistration_digest() != PREREGISTRATION_DIGEST:
        print("error: the preregistration digest drifted", file=sys.stderr)
        return 1
    print(f"preregistration digest: {PREREGISTRATION_DIGEST}")

    roots = root_skeletons()
    print(f"root table digest: {root_table_reference()}")
    print(f"distinct root skeletons: {len(roots)}")

    failures: list[str] = []
    for surface, skeleton, expected, expect_exact in _WORKED_EXAMPLES:
        reading = read_jarad_mazid(surface, roots=roots)
        got = "".join(reading.skeleton)
        exact = bool(reading.exact_matches)
        ok = (
            got == skeleton and reading.slot_count is expected and exact is expect_exact
        )
        print(
            f"[{'ok ' if ok else 'DRIFT'}] {surface}: {got} "
            f"({reading.slots} slots, {reading.slot_count.name}, "
            f"exact={exact})"
        )
        if not ok:
            failures.append(surface)

    prefix_check = read_jarad_mazid("كِتَابٌ", roots=roots)
    if any(
        match.kind is RootMatchKind.EXACT_SKELETON
        and len(match.root) != prefix_check.slots
        for match in prefix_check.matches
    ):
        failures.append("prefix reported as an exact skeleton")

    print(
        "deposited corpus counts, recorded and not adopted: "
        + ", ".join(
            f"{bucket.name}={bucket.deposited_figure}" for bucket in CORPUS_BUCKET_RULES
        )
    )
    print("this script issues no corpus figure of its own")

    if failures:
        print(f"error: the criterion drifted on {failures}", file=sys.stderr)
        return 1
    print("the criterion reads its worked examples unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
