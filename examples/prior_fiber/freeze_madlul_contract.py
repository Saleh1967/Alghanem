"""Freeze the `G0.FIBER-0` madlul fiber contract and print what it does not carry.

Run it::

    python examples/prior_fiber/freeze_madlul_contract.py

**Prior organized information is a licensed geometry, not a slot with a role.**
The node is built on top of the existing nine possibility conditions
(`PriorInformationBase`); an unlicensed condition refuses the node outright. Its
slots start `UNASSIGNED` by declaration, never `None` by silence:
`NeutralFiberInput -/-> PositiveStructuralRole`.

**The three fibers are parallel, not sequential.** Carrier alone, content alone,
and carrier-and-content-together are projected from the one node together. A
fiber that declares itself derived from another fiber is refused by construction.

**The contract is neutral between the systems that will read it.** Its author is
the domain adapter, never one of the two fractal systems: whoever defines the
exam wins the exam. The withheld answer is sealed as a digest only; the
attested sections never enter the contract content.

Nothing here is a comparison, a verdict, or a birth. The ceiling of any later
reading is `ObservedDominanceWithinFrozenDomain`, and it is frozen here, before
any result exists.
"""

from __future__ import annotations

from alghanem.arabic.fiber_contracts import (
    build_madlul_fiber_contract,
    build_madlul_fiber_node,
    madlul_parallel_fibers,
)
from alghanem.arabic.madlul_alone_formal import MadlulSection
from alghanem.prior_fiber import PRIOR_FIBER_LAWS, fiber_import_isolation_audit


def main() -> None:
    """Freeze the contract and report its geometry, its parallelism and its seal."""

    node = build_madlul_fiber_node()
    bundle = madlul_parallel_fibers()
    contract = build_madlul_fiber_contract()

    print("== the prior fiber node ==")
    print(f"origin             : {node.origin_id}")
    print(f"instance           : {node.instance_id}")
    print(f"prior conditions   : {len(node.prior_base.conditions)}")
    print(f"licensed base      : {node.prior_base.is_fit_to_found_an_ontology}")
    print(f"slots              : {len(node.slot_geometry)}")
    print(f"positive roles     : {0 if node.assigns_no_positive_role else 'assigned'}")
    print(f"rank authority     : {node.rank_reference.issuing_authority}")
    print(f"content id         : {node.content_id[:16]}")

    print()
    print("== the parallel fibers ==")
    print(f"parallel           : {bundle.is_parallel}")
    for fiber in bundle.fibers:
        print(
            f"  {fiber.axis.value:<32} carrier={fiber.axis.reads_the_carrier} "
            f"content={fiber.axis.reads_the_content}"
        )

    print()
    print("== the frozen contract ==")
    print(f"members            : {len(contract.members)}")
    print(f"success criteria   : {len(contract.success_criteria)}")
    print(f"author             : {contract.authored_by}")
    print(f"readers            : {', '.join(contract.reading_systems)}")
    print(f"neutral            : {contract.is_neutral_between_its_readers}")
    print(f"gold digest        : {contract.gold_seal.gold_digest[:16]}")
    print(f"preregistration    : {contract.preregistration_digest[:16]}")

    print()
    print("== what the contract does not carry ==")
    for section in MadlulSection:
        print(f"  withheld({section.value:<24}) = {contract.withholds(section.value)}")

    report = fiber_import_isolation_audit()
    print()
    print("== what this layer may not reach ==")
    print(f"isolated           : {report.is_isolated}")
    print(f"reached packages   : {len(report.alghanem_imports)}")
    print(f"laws               : {len(PRIOR_FIBER_LAWS)}")
    print(f"claim ceiling      : {contract.strength_claim_ceiling[:60]}…")


if __name__ == "__main__":
    main()
