"""فجواتُ سلطةِ طبقةِ التجريب: ما لا تملكه هذه الطبقةُ مُسمًّى قبل أن يُسأل عنه.

**وهي نوعٌ مستقلٌّ عن `FractalAuthorityGap`**: فجواتُ النواة تُنسَب إلى
`RES.FGEN0.` ولا تُمَسّ، وفجواتُ هذه الطبقة تُنسَب إلى `RES.FGENEX0.`؛
فلا تُقرَأ فجوةُ طبقةٍ على أنّها فجوةُ الأخرى.

**وأكبرُ فجواتها معلومةٌ قبل أوّل تشغيل**: لا سلطةَ ترخيصٍ هنا ألبتّة، ولا
سلطةَ حكمٍ بكفاية الشواهد.

تسجيلٌ لا سلطة: لا ترخيصَ، ولا رتبةَ دائمة، ولا حكمَ كفاية.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Final

__all__ = [
    "EXPERIMENTAL_AUTHORITY_GAPS",
    "NO_LICENSING_AUTHORITY",
    "NO_SCALE_NECESSITY_CERTIFICATION_IN_EXPERIMENT",
    "NO_SEMANTIC_AUTHORITY_IN_EXPERIMENT",
    "NO_SUFFICIENCY_ASSESSMENT_AUTHORITY",
    "ExperimentalAuthorityGap",
    "ExperimentalAuthorityGapError",
]


class ExperimentalAuthorityGapError(ValueError):
    """رفضٌ عند تكوين فجوةِ سلطةٍ تجريبيّة."""


@dataclass(frozen=True, slots=True)
class ExperimentalAuthorityGap:
    """فجوةُ سلطةٍ في طبقة التجريب: دعوًى، وسلطةٌ غائبة، وشرطُ رفعٍ مُسمًّى."""

    gap_id: str
    claim: str
    missing_authority: str
    discharge_condition: str

    def __post_init__(self) -> None:
        for value, label in (
            (self.gap_id, "مُعرِّفُ الفجوة"),
            (self.claim, "الدعوى التي تقع في الفجوة"),
            (self.missing_authority, "السلطةُ الغائبة"),
            (self.discharge_condition, "شرطُ رفع الفجوة"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ExperimentalAuthorityGapError(f"{label} نصٌّ غير فارغ")
        if not self.gap_id.startswith("RES.FGENEX0."):
            raise ExperimentalAuthorityGapError(
                "مُعرِّفُ فجوةِ طبقة التجريب يبدأ بـ`RES.FGENEX0.`؛ فلا تُخلَط "
                "بفجوات النواة المنسوبةِ إلى `RES.FGEN0.`"
            )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الفجوة للبصمة."""

        return {
            "gap_id": self.gap_id,
            "claim": self.claim,
            "missing_authority": self.missing_authority,
            "discharge_condition": self.discharge_condition,
        }


NO_LICENSING_AUTHORITY: Final[ExperimentalAuthorityGap] = ExperimentalAuthorityGap(
    gap_id="RES.FGENEX0.NoLicensingAuthority",
    claim=(
        "تشغيلٌ تجريبيٌّ جرى تحت إذنٍ مؤقّتٍ فأنتج شواهدَ مُسجَّلةً بأثرها، "
        "ويُقال إنّ ما جرى صار مأذونًا فيه"
    ),
    missing_authority=(
        "لا سلطةَ ترخيصٍ في `G0.FGEN-EX-0`: لا `License` ولا `LicensedPattern` "
        "ولا `LicensedTransition` ولا رتبةَ دائمةً تصدر من هذه الطبقة"
    ),
    discharge_condition=(
        "مرحلةٌ مستقلّةٌ تفتح سلطةَ الترخيص بعد معيار كفايةٍ مُجمَّدٍ سابقٍ "
        "لقياسه، فتقرأ الشواهدَ المتراكمةَ وتُصدِر مرشَّحَ ترخيصٍ ثمّ ترخيصًا"
    ),
)

NO_SUFFICIENCY_ASSESSMENT_AUTHORITY: Final[ExperimentalAuthorityGap] = (
    ExperimentalAuthorityGap(
        gap_id="RES.FGENEX0.NoSufficiencyAssessmentAuthority",
        claim=(
            "حزمةُ الشواهد تجمع تشغيلاتٍ مستقلّةً وشواهدَ مؤيِّدةً ومُكذِّبةً "
            "وضعيفةَ القوّة، ويُقال إنّ ذلك يكفي"
        ),
        missing_authority=(
            "لا سلطةَ حكمٍ بالكفاية هنا: `WitnessBundle ≠ "
            "EvidenceSufficiencyAssessment`، و`WitnessSufficiencyContract` "
            "إعلانٌ مُجمَّدٌ بلا مقياسٍ يُشغِّله في هذه المرحلة"
        ),
        discharge_condition=(
            "طبقةٌ مستقلّةٌ تقيس الحزمةَ على عقد كفايةٍ مُجمَّدٍ قبلها فتُصدِر "
            "تقييمَ كفايةٍ، ثمّ تُحيله إلى سلطة الترخيص"
        ),
    )
)

NO_SCALE_NECESSITY_CERTIFICATION_IN_EXPERIMENT: Final[ExperimentalAuthorityGap] = (
    ExperimentalAuthorityGap(
        gap_id="RES.FGENEX0.NoScaleNecessityCertificationInExperiment",
        claim=(
            "رفعٌ تجريبيٌّ جرى من عقدةٍ مغلقةٍ إلى مقياسٍ أعلى تحت إذنٍ مؤقّت، "
            "ويُقال إنّ ضرورةَ المقياس ثبتت به"
        ),
        missing_authority=(
            "لا شهادةَ ضرورةِ مقياسٍ تصدر هنا: `ExperimentalNextScaleSeed ≠ "
            "NextScaleSeed`، و`ScaleNecessityCertificate` في النواة مغلقةٌ عمدًا"
        ),
        discharge_condition=(
            "المرحلةُ التي تفتح سلطةَ الضرورة في النواة هي وحدَها التي تُصدِر "
            "الشهادةَ؛ وشواهدُ هذه الطبقة مادّةٌ لها لا بديلٌ عنها"
        ),
    )
)

NO_SEMANTIC_AUTHORITY_IN_EXPERIMENT: Final[ExperimentalAuthorityGap] = (
    ExperimentalAuthorityGap(
        gap_id="RES.FGENEX0.NoSemanticAuthorityInExperiment",
        claim=(
            "شاهدٌ رصد إعادةَ بناءٍ وإغلاقًا عند مقياسٍ، ويُقال إنّ ذلك يُثبِت "
            "معنًى أو قاعدةً لغويّة"
        ),
        missing_authority=(
            "لا سلطةَ دلاليّةً في تشغيلٍ صوريّ: الرصدُ بنيويٌّ، والوسمُ الوارد "
            "مع المدخل حكمُ مُوسِّمٍ بشرٍ لا قياسٌ من البنية"
        ),
        discharge_condition=(
            "طبقةٌ دلاليّةٌ مستقلّةٌ بمصدرِ دليلٍ خاصٍّ بها تُسنِد المعنى بسلطتها"
        ),
    )
)

EXPERIMENTAL_AUTHORITY_GAPS: Final[Mapping[str, ExperimentalAuthorityGap]] = (
    MappingProxyType(
        {
            gap.gap_id: gap
            for gap in (
                NO_LICENSING_AUTHORITY,
                NO_SUFFICIENCY_ASSESSMENT_AUTHORITY,
                NO_SCALE_NECESSITY_CERTIFICATION_IN_EXPERIMENT,
                NO_SEMANTIC_AUTHORITY_IN_EXPERIMENT,
            )
        }
    )
)
