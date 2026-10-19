"""فجواتُ السلطة الفراكتاليّة: ما لا تملك هذه المرحلةُ إثباتَه، مُسمًّى قبل أن يُسأل عنه.

**وهي ليست بقايا تشغيليّة** (`RuntimeResidual ≠ ArchitecturalAuthorityGap`):
`FractalResidual` تخرج من حركةٍ جرت فسمّت ما لم يُحسَم فيه —

    Transition  →  ObservedResidual

أمّا الفجوةُ هنا فمعلومةٌ قبل أيِّ تشغيل: بنيةُ المرحلة نفسُها لا تحمل السلطةَ
المطلوبة، فلا يرفعها نجاحُ حركةٍ ولا يُنشئها فشلُها.

**وكلُّ فجوةٍ مرحليّةٌ لا أبديّة**: `NotIssuedAtThisStage ≠ MustNeverExist`؛
فحقلُ `discharge_condition` يُسمّي البابَ الذي يُغلِقها، والسلطةُ تُفتَح في
مرحلةٍ مستقلّةٍ لاحقة، فلا تُقرَأ الفجوةُ منعًا دائمًا.

تسجيلٌ لا سلطة: لا ولادةَ، ولا حكمَ ولادةٍ، ولا تجميدَ `E0`.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Final

__all__ = [
    "FRACTAL_AUTHORITY_GAPS",
    "FractalAuthorityGap",
    "FractalAuthorityGapError",
    "NO_ARABIC_SPECIALIZATION_AUTHORITY",
    "NO_PATTERN_PROOF_WITHOUT_READOUT",
    "NO_SCALE_NECESSITY_AUTHORITY",
    "NO_SEMANTIC_AUTHORITY_IN_FORMAL_GENERATION",
]


class FractalAuthorityGapError(ValueError):
    """رفضٌ عند تكوين فجوةِ سلطة."""


@dataclass(frozen=True, slots=True)
class FractalAuthorityGap:
    """فجوةُ سلطةٍ معماريّة: دعوًى قائمة، وسلطةٌ غائبة، وشرطُ رفعٍ مُسمًّى."""

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
                raise FractalAuthorityGapError(f"{label} نصٌّ غير فارغ")
        if not self.gap_id.startswith("RES.FGEN0."):
            raise FractalAuthorityGapError(
                "مُعرِّفُ فجوةِ هذه المرحلة يبدأ بـ`RES.FGEN0.`؛ فالفجوةُ تُنسَب إلى "
                "المرحلة التي عجزت عنها لا تُترَك بلا موضع"
            )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الفجوة للبصمة."""

        return {
            "gap_id": self.gap_id,
            "claim": self.claim,
            "missing_authority": self.missing_authority,
            "discharge_condition": self.discharge_condition,
        }


NO_SCALE_NECESSITY_AUTHORITY: Final[FractalAuthorityGap] = FractalAuthorityGap(
    gap_id="RES.FGEN0.NoScaleNecessityAuthority",
    claim=(
        "عقدةٌ بلغت أقلَّ التمام عند مقياسها، ويُقال إنّ بنيةً أعلى لازمةٌ لها "
        "فتستحقّ بذرةَ مقياسٍ تالٍ"
    ),
    missing_authority=(
        "لا سلطةَ في `G0.FGEN-0` تُصدِر `ScaleNecessityCertificate`: لا مصنعَ "
        "لها ولا بوّابةَ تشهد باستنفاد المقياس وبعدم قابليّة البقيّة للردّ فيه"
    ),
    discharge_condition=(
        "مرحلةٌ مستقلّةٌ تفتح سلطةَ الضرورة ببوّابةٍ تقرأ استنفادَ المقياس وبقيّةً "
        "غيرَ قابلةٍ للردّ، فتُصدِر الشهادةَ ثمّ يصير الرفعُ ممكنًا"
    ),
)

NO_PATTERN_PROOF_WITHOUT_READOUT: Final[FractalAuthorityGap] = FractalAuthorityGap(
    gap_id="RES.FGEN0.NoPatternProofWithoutReadout",
    claim=(
        "عقدُ النمط يُصرِّح بثوابتَ يحفظها وبفرقٍ يسمح به، وبوّابةُ المطابقة "
        "تُثبِت أنّ المرشَّحَ وافق ما صُرِّح به"
    ),
    missing_authority=(
        "لا قراءةَ مستقلّةً تُثبِت أنّ النمطَ نفسَه صادقٌ فيما وعد: `PatternDeclaration "
        "≠ PatternProof`، والمطابقةُ قياسٌ على دعوى صاحبها لا ترخيصٌ لها"
    ),
    discharge_condition=(
        "قراءةٌ مستقلّةٌ (`READOUT`) تُعيد بناءَ أثر التطبيق وتُطابِق الثوابتَ "
        "المُصرَّحةَ بما رُصِد فعلًا، فتُصدِر برهانَ النمط خارج إعلانه"
    ),
)

NO_SEMANTIC_AUTHORITY_IN_FORMAL_GENERATION: Final[FractalAuthorityGap] = (
    FractalAuthorityGap(
        gap_id="RES.FGEN0.NoSemanticAuthorityInFormalGeneration",
        claim=(
            "العقدةُ المغلقةُ تامّةٌ عند مقياسها، وأثرُها متّصلٌ ببصماته، "
            "وفروعُها محفوظةٌ كاملة"
        ),
        missing_authority=(
            "لا سلطةَ دلاليّةً في توليدٍ صوريّ: `Closure ≠ Meaning` و`Closure ≠ "
            "Truth`؛ فلا يُقرَأ التمامُ الصوريُّ معنًى مقصودًا ولا مطابقةً للواقع"
        ),
        discharge_condition=(
            "طبقةٌ دلاليّةٌ مستقلّةٌ بمصدرِ دليلٍ خاصٍّ بها تُسنِد المعنى بسلطتها، "
            "ولا تستمدّه من تمام البنية الصوريّة"
        ),
    )
)

NO_ARABIC_SPECIALIZATION_AUTHORITY: Final[FractalAuthorityGap] = FractalAuthorityGap(
    gap_id="RES.FGEN0.NoArabicSpecializationAuthority",
    claim=(
        "النواةُ الفراكتاليّةُ محايدةٌ عن اللغات، ويُنتظَر أن تُطبَّق على مادّةٍ "
        "عربيّةٍ بمقاييسها وأنماطها"
    ),
    missing_authority=(
        "لا سلطةَ تخصيصٍ عربيٍّ في هذه النواة: لا مقياسَ عربيًّا مُسجَّلًا، ولا "
        "نمطَ صرفٍ أو نحوٍ، ولا دليلَ معجميًّا؛ ومثالُ التشغيل محايدٌ تخليقيّ"
    ),
    discharge_condition=(
        "مُحوِّلٌ عربيٌّ مستقلٌّ (`G0.FGEN-AR-0`) يستورد النواةَ ولا يُعدِّلها، "
        "ويبني مقاييسَه وأنماطَه على مصادرَ مُجمَّدةٍ قائمةٍ في المستودع"
    ),
)

FRACTAL_AUTHORITY_GAPS: Final[Mapping[str, FractalAuthorityGap]] = MappingProxyType(
    {
        gap.gap_id: gap
        for gap in (
            NO_SCALE_NECESSITY_AUTHORITY,
            NO_PATTERN_PROOF_WITHOUT_READOUT,
            NO_SEMANTIC_AUTHORITY_IN_FORMAL_GENERATION,
            NO_ARABIC_SPECIALIZATION_AUTHORITY,
        )
    }
)
