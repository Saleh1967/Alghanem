"""Read the projection identity certificate: fibers, standings, transport.

python examples/arabic/read_projection_identity_certificate.py
"""

from __future__ import annotations

from alghanem.arabic.carrier_projection_deposit import (
    THE_DEPOSITS_PROJECTED,
    WordBoundary,
    repeated_skeletons_in,
    repeated_words_in,
)
from alghanem.arabic.projection_identity_certificate import (
    PROJECTION_IDENTITY_NAMED_RESIDUALS,
    THE_DESTRUCTION_WITNESSES,
    THE_LICENSE_REGISTER,
    THE_ORDER,
    THE_SCOPE_RANK,
    CollapseStanding,
    ProjectionIdentityError,
    certificate_of,
    the_commutation_table,
    uncertified_carrier_distinctions,
)


def main() -> None:
    print("the declared order:")
    for step in THE_ORDER:
        print(f"  {step}")
    print("  P: probability — refused here, and refused an import guard")

    print("\ndoes the fold commute with the boundary? measured, not assumed:")
    for (source_id, boundary), holds in the_commutation_table().items():
        print(f"  {source_id:<44}{boundary.value:<16}{'yes' if holds else 'NO'}")

    print("\ncertificates:")
    for source_id in THE_DEPOSITS_PROJECTED:
        certificate = certificate_of(source_id)
        print(f"  {source_id}")
        print(f"    fold rule       {certificate.fold_rule[:16]}…")
        print(f"    boundary rule   {certificate.boundary_rule.value}")
        print(
            f"    fibers          {certificate.written_forms} written -> "
            f"{certificate.skeleton_count} skeletons, loss {certificate.loss}"
        )
        print(
            f"    residue         {certificate.residue_occurrences} of "
            f"{certificate.residue_kinds} kinds"
        )
        print(f"    scope rank      {certificate.scope_rank}")
        standings = certificate.standings()
        for standing in CollapseStanding:
            print(f"    {standing.value:<24}{len(standings[standing])}")
        findings = {finding.skeleton: finding for finding in certificate.findings}
        for fiber in certificate.collapsed:
            finding = findings[fiber.skeleton]
            print(
                f"      {fiber.skeleton} <- {' , '.join(fiber.written)} "
                f"at {fiber.occurrences} "
                f"[{finding.standing.value} / {finding.mechanism.value}]"
            )

    print("\nno certificate where the two orders disagree:")
    try:
        certificate_of("fatiha-transcription-in-tree", WordBoundary.SPACE_ONLY)
    except ProjectionIdentityError as refusal:
        print(f"  refused: {refusal}")

    print(
        f"\nthe license register holds {len(THE_LICENSE_REGISTER)} entries, "
        f"the destruction witnesses {len(THE_DESTRUCTION_WITNESSES)}: "
        "a declared fold is a mechanism, not a license"
    )

    classes = uncertified_carrier_distinctions()
    print(f"\ncarrier distinctions not certified by transport: {len(classes)} classes")
    for klass in classes:
        print(f"  {''.join(sorted(klass))}")
    print("  (a failure to transport withholds a certificate; it locates nothing)")

    print("\nrepetition made by the projection, not found by it:")
    for source_id in THE_DEPOSITS_PROJECTED:
        print(
            f"  {source_id}: {len(repeated_words_in(source_id))} written, "
            f"{len(repeated_skeletons_in(source_id))} projected"
        )

    print(f"\nscope: {THE_SCOPE_RANK}")
    print("named residuals:")
    for key in PROJECTION_IDENTITY_NAMED_RESIDUALS:
        print(f"  {key}")


if __name__ == "__main__":
    main()
