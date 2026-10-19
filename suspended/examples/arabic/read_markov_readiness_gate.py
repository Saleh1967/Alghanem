"""Read the Markov readiness gate: prerequisites, standings, projection-made regularity.

python examples/arabic/read_markov_readiness_gate.py
"""

from __future__ import annotations

from alghanem.arabic.carrier_projection_deposit import THE_DEPOSITS_PROJECTED
from alghanem.arabic.markov_readiness_gate import (
    MARKOV_READINESS_NAMED_RESIDUALS,
    functional_markov_standing,
    projection_made_regularity_on,
    the_prerequisite_chain,
    token_markov_standing,
)


def main() -> None:
    print("the prerequisite chain, in order:")
    for index, reading in enumerate(the_prerequisite_chain(), start=1):
        mark = "met" if reading.met else "UNMET"
        print(f"  {index}. {reading.prerequisite.value}: {mark}")

    print("\nthe two state-space licenses:")
    for reading in (token_markov_standing(), functional_markov_standing()):
        print(f"  {reading.chain_name}: {reading.standing.value}")
        if reading.blocking_prerequisite is not None:
            print(f"    blocked at: {reading.blocking_prerequisite.value}")
        print(f"    {reading.ground}")

    print("\nregularity the projection itself made:")
    for source_id in sorted(THE_DEPOSITS_PROJECTED):
        regularity = projection_made_regularity_on(source_id)
        print(
            f"  {source_id}: written {regularity.repeated_written} -> "
            f"projected {regularity.repeated_projected} "
            f"(made by the projection: {regularity.made_by_the_projection})"
        )

    print("\nnamed residuals:")
    for key in MARKOV_READINESS_NAMED_RESIDUALS:
        print(f"  {key}")


if __name__ == "__main__":
    main()
