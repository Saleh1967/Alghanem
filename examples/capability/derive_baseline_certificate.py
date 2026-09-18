"""Derive the baseline ``ArabicStateCertificate`` over the declared denominator.

    python examples/capability/derive_baseline_certificate.py

Nothing here is entered by hand. The denominator is
``DeclaredArabicCapabilityUniverseV1`` — a declared universe of Arabic
capabilities, each with a classical citation, built outside the implementation
and forbidden by its own import policy from reading ``arabic/``, ``kernel/`` or
any other built module. That is what
``ADenominatorDerivedFromTheImplementationIsNotAMeasure`` buys: a capability
nobody has built yet is a **zero inside the ratio**, not a question outside it.

The only evidence seeded below is the declaration evidence the manifest derives
from itself: every declared leaf is, by the fact of being declared, at
``S1_DECLARED``. No implementation, no test, no gold, no blind evaluation and no
transfer is claimed here, and none is silently assumed. So the baseline reads
``DeclaredCoverage = 1.0`` and every one of the eight remaining coverages reads
``0.0`` over the same denominator. That is the intended shape of a first
certificate: a truthful floor, not a flattering estimate.

No composite Arabic percentage is printed, because none is defined: nine
qualitative gates do not become one number without a declared weight protocol
(``NoOrdinalGateArithmeticWithoutDeclaredWeights``), so ``CompositeCoverage``,
``DomainBalancedCoverage`` and ``DependencyWeightedCoverage`` each print as
``UNDEFINED`` with the reason that keeps them undefined. The seventeen domains
are printed one row at a time rather than averaged, because weighting them
equally is itself a weighting protocol
(``EqualDomainWeightingIsStillAWeightingProtocol``). ``Coverage`` and
``Readiness`` are printed as two figures, never as one
(``Breadth != Readiness``).

This script issues no verdict, freezes nothing, and imports nothing from
``alghanem.kernel``.
"""

from __future__ import annotations

import sys

from alghanem.capability import (
    CITATION_STANDING_SEQUENCE,
    DECLARED_ARABIC_CAPABILITY_UNIVERSE_V1,
    ArabicStateCertificate,
    DerivedRatio,
    EvidenceLedger,
    MaturityStage,
    ReadinessGateOrigin,
    UndeclaredScalar,
    derive_arabic_state_certificate,
    derive_declaration_evidence,
)

_UNIVERSE = DECLARED_ARABIC_CAPABILITY_UNIVERSE_V1


def _render_ratio(name: str, ratio: DerivedRatio) -> str:
    """اعرض النسبةَ ومعها بسطُها ومقامُها؛ ولا نسبةَ مجرّدة."""

    value = "undefined" if ratio.value is None else f"{ratio.value:.4f}"
    return f"  {name:<28} {ratio.numerator:>4} / {ratio.denominator:<5} = {value}"


def _render_undeclared(scalar: UndeclaredScalar) -> str:
    """اعرض الرقمَ غيرَ المعرَّف بسببه؛ الامتناعُ مُفصَحٌ عنه لا مسكوتٌ عليه."""

    return (
        f"  {scalar.name:<28} {scalar.standing.value:<10} "
        f"value: undefined   reason: {scalar.reason.value}"
    )


def _derive_baseline() -> ArabicStateCertificate:
    """اشتقّ الشهادةَ الأساس: المقامُ كاملًا، وشاهدُ الإعلان وحدَه."""

    ledger = EvidenceLedger(_UNIVERSE.leaf_ids())
    for evidence in derive_declaration_evidence(_UNIVERSE):
        ledger.consider(evidence)
    return derive_arabic_state_certificate(_UNIVERSE, ledger)


def main() -> int:
    """اطبع الشهادةَ الأساس، ثم تحقّق من أنّ أرقامها تُعيد اشتقاقَ نفسِها."""

    certificate = _derive_baseline()
    manifest = certificate.universe_manifest

    print(f"universe            : {manifest.universe_id}")
    print(f"universe digest     : {manifest.content_digest}")
    print(f"declared nodes      : {manifest.node_count}")
    print(f"declared leaves     : {manifest.leaf_count}")
    print(f"certificate digest  : {certificate.certificate_digest}")
    print()
    print(f"schema version      : {certificate.schema_version}")
    print()
    print(certificate.headline_statement)
    print()
    print("Gate profile (nine, kept apart, never merged):")
    for name, ratio in certificate.gate_profile.items():
        print(_render_ratio(name, ratio))
    print()
    print("Coverage is not readiness:")
    print(_render_ratio("CertifiedCompletion", certificate.certified_completion))
    print(_render_ratio("Readiness", certificate.readiness))
    print()
    print("Undefined scalars (no weighting protocol has been declared):")
    print(_render_undeclared(certificate.composite_coverage))
    print(_render_undeclared(certificate.domain_balanced_coverage))
    print(_render_undeclared(certificate.dependency_weighted_coverage))
    print()
    print("DomainCoverageProfile (seventeen domains, never averaged):")
    for row in certificate.domain_coverage_profile.rows:
        declared = row.coverage[MaturityStage.S1_DECLARED]
        modeled = row.coverage[MaturityStage.S2_MODELED]
        print(
            f"  {row.domain_id:<5} leaves {row.leaf_total:>3}"
            f"   declared {declared.numerator:>3}/{declared.denominator:<3}"
            f"   modeled {modeled.numerator:>3}/{modeled.denominator:<3}"
            f"   readiness {row.readiness.numerator:>3}/{row.readiness.denominator}"
        )
    print()
    print("CitationProvenanceProfile (documentation standings, not a score):")
    provenance = certificate.citation_provenance
    for standing in CITATION_STANDING_SEQUENCE:
        print(f"  {standing.value:<28} {provenance.standing_counts[standing]:>4}")
    print(
        _render_ratio(
            "TextuallyAnchoredCoverage", provenance.textually_anchored_coverage
        )
    )
    print()
    print("ReadinessGateOriginProfile:")
    origins = certificate.readiness_gate_origins
    for origin in ReadinessGateOrigin:
        print(f"  {origin.value:<28} {origins.origin_counts[origin]:>4}")
    print(_render_ratio("DerivedReadinessCoverage", origins.derived_readiness_coverage))
    print()
    print("Governance indicators:")
    governance = certificate.governance
    for name, ratio in (
        ("IdentityPreservationRate", governance.identity_preservation_rate),
        ("ResidualDisclosureRate", governance.residual_disclosure_rate),
        ("NoJumpComplianceRate", governance.no_jump_compliance_rate),
        ("ForbiddenJumpRate", governance.forbidden_jump_rate),
        ("UnauthorizedUpgradeRate", governance.unauthorized_upgrade_rate),
        ("UndisclosedResidualRate", governance.undisclosed_residual_rate),
    ):
        print(_render_ratio(name, ratio))
    print(f"  zero targets met           : {governance.zero_targets_are_met}")
    print()
    print("Ranked blockers (highest first):")
    for blocker in certificate.blockers[:5]:
        print(
            f"  {blocker.blocking_reason:<28} blocks {blocker.blocked_leaf_count:>4}"
            f" leaves across {len(blocker.blocked_domains)} domains"
        )
    print(f"  next gate                  : {certificate.next_gate}")
    print()
    for law in certificate.laws:
        print(f"law: {law.split(':', 1)[0]}")

    reproduced = _derive_baseline()
    outcomes = (
        reproduced.certificate_digest == certificate.certificate_digest,
        certificate.gate_profile["DeclaredCoverage"].numerator == manifest.leaf_count,
        all(
            ratio.numerator == 0
            for name, ratio in certificate.gate_profile.items()
            if name != "DeclaredCoverage"
        ),
        certificate.composite_coverage.value is None,
        certificate.domain_balanced_coverage.value is None,
        certificate.dependency_weighted_coverage.value is None,
        governance.zero_targets_are_met,
    )
    if all(outcomes):
        print()
        print("the baseline certificate re-derives byte for byte from the denominator")
        return 0
    print(
        "error: the certificate did not re-derive from the same denominator and "
        "ledger; the figure is not edited to match",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
