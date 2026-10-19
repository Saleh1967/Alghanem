"""Read the lexical artifact closure: standing, mechanism, extent, dominance.

python examples/arabic/read_lexical_artifact_closure.py
"""

from __future__ import annotations

from alghanem.arabic.carrier_projection_deposit import THE_DEPOSITS_PROJECTED
from alghanem.arabic.lexical_artifact_closure import (
    LEXICAL_ARTIFACT_NAMED_RESIDUALS,
    THE_CLOSED_CLAIMS,
    LexicalArtifactError,
    dominance_of,
    refuse_to_freeze,
    the_probe_witness,
)


def main() -> None:
    witness = the_probe_witness()
    print("the deposited probe witness:")
    print(f"  surface forms: {witness.surface_forms}")
    print(f"  selected k: {witness.selected_k}")
    print(f"  cluster sizes: {witness.cluster_sizes}")
    print(f"  mixed members: {' '.join(witness.mixed_members)}")

    print("\ndominance on the deposits:")
    for source_id in sorted(THE_DEPOSITS_PROJECTED):
        for projected in (False, True):
            reading = dominance_of(source_id, projected)
            layer = "projected" if projected else "written"
            print(
                f"  {source_id} [{layer}]: "
                f"{reading.tokens} tokens, {reading.types} types, "
                f"leading {reading.leading_type!r} x{reading.leading_occurrences} "
                f"({reading.leading_share:.3%}), "
                f"exposed {reading.exposed_share:.3%}"
            )

    print("\nthe closed claims:")
    for claim in THE_CLOSED_CLAIMS:
        print(f"  {claim.claim_key}: {claim.standing.value} / {claim.extent.value}")
        print(f"    mechanism: {claim.mechanism.value}")

    print("\nasking a closed claim to be frozen:")
    for claim in THE_CLOSED_CLAIMS:
        try:
            refuse_to_freeze(claim.claim_key)
        except LexicalArtifactError as refusal:
            print(f"  {claim.claim_key}: {refusal}")

    print("\nnamed residuals:")
    for key in LEXICAL_ARTIFACT_NAMED_RESIDUALS:
        print(f"  {key}")


if __name__ == "__main__":
    main()
