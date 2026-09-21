"""Read the composition ordering law: commutes, order required, unresolved.

python examples/arabic/read_projection_composition_order.py
"""

from __future__ import annotations

from alghanem.arabic.projection_composition_order import (
    COMPOSITION_ORDER_NAMED_RESIDUALS,
    THE_ORDER_REGISTER,
    CompositionStanding,
    the_composition_table,
    usable_for_composition,
)


def main() -> None:
    print(f"deposited orders: {len(THE_ORDER_REGISTER)}")
    print("\nthe composition table:")
    for finding in the_composition_table():
        usable = usable_for_composition(
            finding.source_identity, finding.boundary_rule
        )
        print(
            f"  {finding.source_identity} x {finding.boundary_rule.name}: "
            f"{finding.standing.value} (usable: {usable})"
        )

    unresolved = [
        finding
        for finding in the_composition_table()
        if finding.standing is CompositionStanding.UNRESOLVED
    ]
    print(f"\nunresolved compositions: {len(unresolved)}")
    for finding in unresolved:
        print(f"  {finding.source_identity} x {finding.boundary_rule.name}")
        print(f"    {finding.ground}")

    print("\nnamed residuals:")
    for key in COMPOSITION_ORDER_NAMED_RESIDUALS:
        print(f"  {key}")


if __name__ == "__main__":
    main()
