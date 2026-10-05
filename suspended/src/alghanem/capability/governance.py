"""`G0.METRIC-0`: مؤشّراتُ الحوكمة، هدفُ ثلاثةٍ منها صفرٌ لا «قليل».

ثلاثةٌ تُقاس صعودًا: حفظُ الهويّة، والإفصاحُ عن البواقي، والالتزامُ بعدم القفز.
وثلاثةٌ هدفُها **صفر**: القفزُ المحظور، والترقيةُ بلا إذن، والباقي غيرُ المُفصَح
عنه. وهذه الأخيرةُ تُشتَقّ من سِجِلّ الردّ لا من ادّعاءٍ بأنّها لم تقع: فدفترُ
الشواهد يردّ ويُسجِّل جنسَ ردّه، فيصير المقامُ **ما نُظِر فيه** لا ما قُبِل.
"""

from __future__ import annotations

from dataclasses import dataclass

from .aggregate import DerivedRatio
from .evidence import EvidenceLedger, RefusalCode, ResidualDisclosure
from .measure import LeafMeasurement
from .universe import CapabilityUniverse

__all__ = [
    "GovernanceIndicators",
    "derive_governance_indicators",
]


@dataclass(frozen=True)
class GovernanceIndicators:
    """مؤشّراتُ الحوكمة الستّة، كلٌّ منها نسبةٌ محمولةٌ بمقامها."""

    identity_preservation_rate: DerivedRatio
    residual_disclosure_rate: DerivedRatio
    no_jump_compliance_rate: DerivedRatio
    forbidden_jump_rate: DerivedRatio
    unauthorized_upgrade_rate: DerivedRatio
    undisclosed_residual_rate: DerivedRatio

    @property
    def zero_target_indicators(self) -> tuple[str, ...]:
        """أسماءُ المؤشّرات التي هدفُها صفر، مُعلَنةً لا مُستنبَطة."""

        return (
            "ForbiddenJumpRate",
            "UnauthorizedUpgradeRate",
            "UndisclosedResidualRate",
        )

    @property
    def zero_targets_are_met(self) -> bool:
        """هل بلغت الثلاثةُ هدفَها؟ صفرٌ صريحٌ لا «قريبٌ من الصفر»."""

        return all(
            ratio.numerator == 0
            for ratio in (
                self.forbidden_jump_rate,
                self.unauthorized_upgrade_rate,
                self.undisclosed_residual_rate,
            )
        )

    def as_canonical_content(self) -> dict[str, object]:
        """المحتوى القانونيّ لمؤشّرات الحوكمة."""

        return {
            "IdentityPreservationRate": (
                self.identity_preservation_rate.as_canonical_content()
            ),
            "ResidualDisclosureRate": (
                self.residual_disclosure_rate.as_canonical_content()
            ),
            "NoJumpComplianceRate": self.no_jump_compliance_rate.as_canonical_content(),
            "ForbiddenJumpRate": self.forbidden_jump_rate.as_canonical_content(),
            "UnauthorizedUpgradeRate": (
                self.unauthorized_upgrade_rate.as_canonical_content()
            ),
            "UndisclosedResidualRate": (
                self.undisclosed_residual_rate.as_canonical_content()
            ),
            "zero_target_indicators": list(self.zero_target_indicators),
            "zero_targets_are_met": self.zero_targets_are_met,
        }


def derive_governance_indicators(
    universe: CapabilityUniverse,
    ledger: EvidenceLedger,
    measurements: dict[str, LeafMeasurement],
) -> GovernanceIndicators:
    """اشتقّ المؤشّراتِ الستّة من الدفتر والقياس، لا من إعلانٍ عنهما."""

    considered = ledger.considered_count
    admitted = ledger.admitted
    refusals = ledger.refusals
    evidence_source = "EvidenceLedger.considered"
    leaves = universe.leaf_ids()
    leaf_source = universe.manifest.universe_id

    identity_numerator = sum(1 for item in admitted if item.identity_preserved)
    disclosure_numerator = sum(
        1
        for item in admitted
        if item.residual_disclosure is ResidualDisclosure.DISCLOSED
    )
    no_jump_numerator = sum(
        1 for leaf_id in leaves if measurements[leaf_id].has_no_jump
    )
    jump_numerator = len(leaves) - no_jump_numerator
    unauthorized = sum(
        1
        for refusal in refusals
        if refusal.refusal_code is RefusalCode.UNAUTHORIZED_UPGRADE
    )
    undisclosed = sum(
        1
        for refusal in refusals
        if refusal.refusal_code is RefusalCode.UNDISCLOSED_RESIDUALS
    )
    return GovernanceIndicators(
        identity_preservation_rate=DerivedRatio(
            numerator=identity_numerator,
            denominator=len(admitted),
            denominator_source="EvidenceLedger.admitted",
        ),
        residual_disclosure_rate=DerivedRatio(
            numerator=disclosure_numerator,
            denominator=len(admitted),
            denominator_source="EvidenceLedger.admitted",
        ),
        no_jump_compliance_rate=DerivedRatio(
            numerator=no_jump_numerator,
            denominator=len(leaves),
            denominator_source=leaf_source,
        ),
        forbidden_jump_rate=DerivedRatio(
            numerator=jump_numerator,
            denominator=len(leaves),
            denominator_source=leaf_source,
        ),
        unauthorized_upgrade_rate=DerivedRatio(
            numerator=unauthorized,
            denominator=considered,
            denominator_source=evidence_source,
        ),
        undisclosed_residual_rate=DerivedRatio(
            numerator=undisclosed,
            denominator=considered,
            denominator_source=evidence_source,
        ),
    )
