"""Read the deposited carrier projection: the 29, the boundary, the edge.

python examples/arabic/read_carrier_projection_deposit.py
"""

from __future__ import annotations

from alghanem.arabic.carrier_projection_deposit import (
    CARRIER_PROJECTION_NAMED_RESIDUALS,
    THE_DEPOSITS_PROJECTED,
    THE_FOLDING,
    WordBoundary,
    census_of,
    collisions_in,
    repeated_skeletons_in,
    repeated_words_in,
    the_edges_only_the_space_rule_makes,
    the_twenty_nine,
)
from alghanem.arabic.fath_ayah_source_text import FATH_AYAH_SOURCE_ID
from alghanem.arabic.fatiha_source_text import FATIHA_SOURCE_ID


def main() -> None:
    carriers = the_twenty_nine()
    print(f"the carriers: {len(carriers)}  {''.join(carriers)}")
    print(f"the folding that makes them: {len(THE_FOLDING)} written forms")
    for written, base in THE_FOLDING.items():
        print(f"  {written} -> {base}")

    print("\nthe two boundary rules, measured on both deposits:")
    header = f"{'deposit':<44}{'rule':<16}{'words':>7}{'carriers':>10}{'edges':>7}"
    print(header)
    for source_id in THE_DEPOSITS_PROJECTED:
        for boundary in WordBoundary:
            census = census_of(source_id, boundary)
            print(
                f"{source_id:<44}{boundary.value:<16}"
                f"{census.words:>7}{census.carrier_occurrences:>10}{census.edges:>7}"
            )

    fabricated = the_edges_only_the_space_rule_makes(FATIHA_SOURCE_ID)
    print(f"\nedges the space-only rule fabricates on the Fatiha: {len(fabricated)}")
    for left, right in fabricated:
        print(f"  {left} -> {right}")
    print(
        "on the Fath ayah it fabricates "
        f"{len(the_edges_only_the_space_rule_makes(FATH_AYAH_SOURCE_ID))} "
        "— one line, so the rule is inert, not right"
    )

    print("\nwhat the projection costs:")
    for source_id in THE_DEPOSITS_PROJECTED:
        census = census_of(source_id, WordBoundary.ANY_WHITESPACE)
        print(
            f"  {source_id}: residue {census.residue_occurrences} "
            f"of {census.residue_kinds} kinds; "
            f"{census.distinct_words} written words -> "
            f"{census.distinct_skeletons} skeletons"
        )
    for skeleton, written in collisions_in(FATH_AYAH_SOURCE_ID).items():
        print(f"    {skeleton} <- {' , '.join(written)}")

    print("\nrepetition, written and projected:")
    for source_id in THE_DEPOSITS_PROJECTED:
        print(
            f"  {source_id}: {len(repeated_words_in(source_id))} written, "
            f"{len(repeated_skeletons_in(source_id))} projected"
        )

    print("\nnamed residuals:")
    for key in CARRIER_PROJECTION_NAMED_RESIDUALS:
        print(f"  {key}")


if __name__ == "__main__":
    main()
