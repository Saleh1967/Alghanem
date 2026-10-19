"""Read the sukun state contract: two states, one eviction, no merged total.

python examples/arabic/read_sukun_state_contract.py
"""

from __future__ import annotations

from alghanem.arabic.sukun_state_contract import (
    SUKUN_STATE_NAMED_RESIDUALS,
    NonSukunCategory,
    SukunStateContractError,
    refuse_a_merged_total,
    the_state_space_of,
    the_sukun_splits,
)


def main() -> None:
    print("the split column:")
    for split in the_sukun_splits():
        print(f"  {split.scope}")
        for state, count in the_state_space_of(split.scope).items():
            print(f"    {state.value}: {count}")
        print(
            f"    {NonSukunCategory.GEMINATION_FIRST_HALF.value} "
            f"(evicted): {split.evicted}"
        )
        print(
            f"    in the state space: {split.in_state_space} "
            f"of a raw column of {split.raw_column}"
        )

    print("\nasking for a single sukun total:")
    for split in the_sukun_splits():
        try:
            refuse_a_merged_total(split.scope)
        except SukunStateContractError as refusal:
            print(f"  {refusal}")

    print("\nnamed residuals:")
    for key in SUKUN_STATE_NAMED_RESIDUALS:
        print(f"  {key}")


if __name__ == "__main__":
    main()
