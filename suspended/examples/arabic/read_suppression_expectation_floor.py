"""Read the suppression expectation floor: null, floor, contributors, standings.

python examples/arabic/read_suppression_expectation_floor.py
"""

from __future__ import annotations

from alghanem.arabic.suppression_expectation_floor import (
    SUPPRESSION_FLOOR_NAMED_RESIDUALS,
    THE_CONTRACT_REGISTER,
    THE_NAMED_UNDEPOSITED_TESTS,
    NullHypothesis,
    SuppressionContract,
    SuppressionFloorError,
    TypeContributor,
    contract_for,
    read_zero_cell,
)


def main() -> None:
    print(f"deposited contracts: {len(THE_CONTRACT_REGISTER)}")
    print("named but undeposited tests:")
    for name in THE_NAMED_UNDEPOSITED_TESTS:
        try:
            contract_for(name)
        except SuppressionFloorError as refusal:
            print(f"  {name}: {refusal}")

    illustration = SuppressionContract(
        test_identity="illustration-only",
        null_hypothesis=NullHypothesis.INDEPENDENT_MARGINALS,
        minimum_expectation=5.0,
        type_contributors=(
            TypeContributor(type_key="type-a", occurrences=4),
            TypeContributor(type_key="type-b", occurrences=6),
        ),
    )
    print("\nreading zero cells under an illustrative contract:")
    for observed, expected in ((0, 0.4), (0, 12.0), (3, 12.0)):
        reading = read_zero_cell(illustration, observed=observed, expected=expected)
        print(
            f"  obs={observed} E={expected}: {reading.standing.value} "
            f"(largest contributor {reading.largest_contributor_share:.3%})"
        )

    print("\nnamed residuals:")
    for key in SUPPRESSION_FLOOR_NAMED_RESIDUALS:
        print(f"  {key}")


if __name__ == "__main__":
    main()
