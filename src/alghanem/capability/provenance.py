"""`G0.METRIC-0.HARDEN`: توثيقُ المصدر اتّجاهًا، وأصلُ بوّابة الأهليّة اتّجاهًا.

اتّجاهُ الاستشهادات يعرض المراتبَ الخمسَ بأعدادها، ولا يُقرأ سُلَّمَ نجاحٍ
ورسوب: `SECTION_LEVEL_LOCUS` ليس «فشلًا» و`MODERN_FORMAL_EXTENSION` ليس عيبًا،
وإنّما كلٌّ منها **إفصاحٌ عن جنس الربط**. وما يُقاس نسبةً هنا واحدٌ صريحٌ وحدَه:
`TextuallyAnchoredCoverage`، ولا يدخل فيه إلّا `EXACT_TEXTUAL_LOCUS`.

وتوثيقُ المصدر لا يرفع درجةَ نضجٍ واحدة
(`SourceCitationDoesNotLicenseSystemCapability`): هو يُثبِت مصدرَ السؤال لا قدرةَ
النظام. وكذلك أصلُ بوّابة الأهليّة يبقى مُعلَنًا لا مُشتَقًّا
(`UniformReadinessGate != DerivedReadinessRequirement`).
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from .aggregate import DerivedRatio
from .laws import (
    CITATION_NAME_IS_NOT_A_VERIFIED_SOURCE_LOCUS,
    SOURCE_CITATION_DOES_NOT_LICENSE_SYSTEM_CAPABILITY,
    UNIFORM_READINESS_GATE_IS_NOT_A_DERIVED_READINESS_REQUIREMENT,
)
from .node import CITATION_STANDING_SEQUENCE, CitationStanding, ReadinessGateOrigin
from .universe import CapabilityUniverse

__all__ = [
    "CitationProvenanceProfile",
    "ReadinessGateOriginProfile",
    "derive_citation_provenance_profile",
    "derive_readiness_gate_origin_profile",
]

_STANDING_COUNT_NAMES: Mapping[CitationStanding, str] = {
    CitationStanding.EXACT_TEXTUAL_LOCUS: "ExactTextualLocusCount",
    CitationStanding.SECTION_LEVEL_LOCUS: "SectionLevelLocusCount",
    CitationStanding.CONCEPTUAL_CORRESPONDENCE: "ConceptualCorrespondenceCount",
    CitationStanding.MODERN_FORMAL_EXTENSION: "ModernFormalExtensionCount",
    CitationStanding.UNVERIFIED_LOCUS: "UnverifiedLocusCount",
}
"""أسماءُ عدّادات المراتب؛ أعدادٌ مُفصَحٌ عنها لا رقمُ جودةٍ واحد."""


@dataclass(frozen=True)
class CitationProvenanceProfile:
    """اتّجاهُ توثيق الاستشهادات: خمسةُ أعداد، ونسبةٌ واحدةٌ صريحةُ المعيار."""

    standing_counts: Mapping[CitationStanding, int]
    textually_anchored_coverage: DerivedRatio

    @property
    def citation_law(self) -> str:
        """سقفُ قراءة الاتّجاه، محمولًا معه لا مفصولًا عنه."""

        return CITATION_NAME_IS_NOT_A_VERIFIED_SOURCE_LOCUS

    @property
    def maturity_law(self) -> str:
        """توثيقُ المصدر لا يرخّص درجةَ نضج؛ القانونُ محمولٌ مع الاتّجاه."""

        return SOURCE_CITATION_DOES_NOT_LICENSE_SYSTEM_CAPABILITY

    def as_canonical_content(self) -> dict[str, object]:
        """المحتوى القانونيّ لاتّجاه التوثيق."""

        content: dict[str, object] = {
            _STANDING_COUNT_NAMES[standing]: self.standing_counts[standing]
            for standing in CITATION_STANDING_SEQUENCE
        }
        content["TextuallyAnchoredCoverage"] = (
            self.textually_anchored_coverage.as_canonical_content()
        )
        content["anchored_standings"] = [CitationStanding.EXACT_TEXTUAL_LOCUS.value]
        return content


def derive_citation_provenance_profile(
    universe: CapabilityUniverse,
) -> CitationProvenanceProfile:
    """اشتقّ اتّجاهَ التوثيق من استشهادات الأوراق وحدَها، لا من ادّعاءٍ عنها."""

    leaves = universe.leaf_ids()
    standings = [
        universe.node(leaf_id).citation.citation_standing for leaf_id in leaves
    ]
    counts = {
        standing: sum(1 for value in standings if value is standing)
        for standing in CITATION_STANDING_SEQUENCE
    }
    return CitationProvenanceProfile(
        standing_counts=counts,
        textually_anchored_coverage=DerivedRatio(
            numerator=counts[CitationStanding.EXACT_TEXTUAL_LOCUS],
            denominator=len(leaves),
            denominator_source=universe.manifest.universe_id,
        ),
    )


@dataclass(frozen=True)
class ReadinessGateOriginProfile:
    """اتّجاهُ أصلِ بوّابات الأهليّة: ما صُرِّح به، وما اشتُقَّ من دور القدرة."""

    origin_counts: Mapping[ReadinessGateOrigin, int]
    derived_readiness_coverage: DerivedRatio

    @property
    def readiness_origin_law(self) -> str:
        """سقفُ قراءة الاتّجاه، محمولًا معه لا مفصولًا عنه."""

        return UNIFORM_READINESS_GATE_IS_NOT_A_DERIVED_READINESS_REQUIREMENT

    def as_canonical_content(self) -> dict[str, object]:
        """المحتوى القانونيّ لاتّجاه أصل بوّابات الأهليّة."""

        return {
            "DeclaredUniformV1Count": self.origin_counts[
                ReadinessGateOrigin.DECLARED_UNIFORM_V1
            ],
            "DerivedFromCapabilityRoleCount": self.origin_counts[
                ReadinessGateOrigin.DERIVED_FROM_CAPABILITY_ROLE
            ],
            "DerivedReadinessCoverage": (
                self.derived_readiness_coverage.as_canonical_content()
            ),
        }


def derive_readiness_gate_origin_profile(
    universe: CapabilityUniverse,
) -> ReadinessGateOriginProfile:
    """اشتقّ اتّجاهَ أصل بوّابات الأهليّة من إعلان العقد وحدَه."""

    leaves = universe.leaf_ids()
    origins = [universe.node(leaf_id).readiness_gate_origin for leaf_id in leaves]
    counts = {
        origin: sum(1 for value in origins if value is origin)
        for origin in ReadinessGateOrigin
    }
    return ReadinessGateOriginProfile(
        origin_counts=counts,
        derived_readiness_coverage=DerivedRatio(
            numerator=counts[ReadinessGateOrigin.DERIVED_FROM_CAPABILITY_ROLE],
            denominator=len(leaves),
            denominator_source=universe.manifest.universe_id,
        ),
    )
