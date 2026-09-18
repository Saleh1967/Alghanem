"""فجواتُ السلطة المعماريّة: ما لا تملك هذه الطبقةُ إثباتَه، مُسمًّى قبل أن يُسأل عنه.

**وهي ليست بقايا تشغيليّة** (`RuntimeResidual ≠ ArchitecturalAuthorityGap`):
`GenerationResidual` تخرج من انتقالٍ جرى فسمّى ما لم يُحسَم فيه —

    Transition  →  ObservedResidual

أمّا الفجوةُ هنا فمعلومةٌ قبل أيِّ تشغيل: بنيةُ الطبقة نفسُها لا تحمل السلطةَ
المطلوبة، فلا يرفعها نجاحُ خطوةٍ ولا يُنشئها فشلُها. ولذلك لا تُسجَّل في أثرٍ
ولا تُقرأ بقيّةً، بل تُعلَن في القرار الذي يقع في مداها:

    ConformantSurface  =  ProvedConformance  +  ExplicitAuthorityBoundary

وكلُّ فجوةٍ تحمل شرطَ رفعها (`discharge_condition`) صريحًا، فلا تبقى نقصًا
مفتوحًا بلا بابٍ يُغلِقه.

تسجيلٌ لا سلطة: لا ولادةَ، ولا حكمَ ولادةٍ، ولا تجميدَ `E0`.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Final

__all__ = [
    "GENERATION_AUTHORITY_GAPS",
    "GenerationAuthorityGap",
    "GenerationAuthorityGapError",
    "NO_INDEPENDENT_ANCHOR_TO_SYNTACTIC_FUNCTION_AUTHORITY",
    "NO_VERIFIED_LEXICAL_ATTESTATION",
]


class GenerationAuthorityGapError(ValueError):
    """رفضٌ عند تكوين فجوةِ سلطة."""


@dataclass(frozen=True, slots=True)
class GenerationAuthorityGap:
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
                raise GenerationAuthorityGapError(f"{label} نصٌّ غير فارغ")
        if not self.gap_id.startswith("RES.GEN0."):
            raise GenerationAuthorityGapError(
                "مُعرِّفُ فجوةِ هذه الطبقة يبدأ بـ`RES.GEN0.`؛ فالفجوةُ تُنسَب إلى "
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


NO_INDEPENDENT_ANCHOR_TO_SYNTACTIC_FUNCTION_AUTHORITY: Final[GenerationAuthorityGap] = (
    GenerationAuthorityGap(
        gap_id="RES.GEN0.NoIndependentAnchorToSyntacticFunctionAuthority",
        claim=(
            "المواصفةُ تُسنِد مرساةً إلى موضع الفاعل وأخرى إلى موضع المفعول به، "
            "وبوّابةُ المطابقة تُثبِت أنّ المنتَجَ حفِظ هذا الإسناد"
        ),
        missing_authority=(
            "لا سلطةَ مستقلّةً تربط المرساةَ بوظيفةٍ نحويّة: `Anchor ⇏ فاعل/مفعولٌ "
            "به` باختيار المستدعي. والمصدرُ المرخَّصُ — `AnchoredNisbahSignatureV3` — "
            "يحمل مراسيَ ومحمولًا ومواضعَ حجج، ولا يحمل رابطةَ ملءٍ بين مرساةٍ وموضعِ "
            "حجّة، بل يرفض `ArgumentSlot` أسماءَ الأدوار صراحةً؛ فالإسنادُ دعوى "
            "صاحبِ المواصفة، والمطابقةُ حفظٌ لها لا ترخيصٌ من المصدر"
        ),
        discharge_condition=(
            "شهادةُ ربطٍ مستقلّةٌ — `SyntacticBindingCertificate` — تُثبِت "
            "`Anchor →evidence→ LicensedSyntacticPosition`؛ وعندها وحدَها يُفتَح "
            "اسمُ `StructurallyLicensedSurface`"
        ),
    )
)

NO_VERIFIED_LEXICAL_ATTESTATION: Final[GenerationAuthorityGap] = GenerationAuthorityGap(
    gap_id="RES.GEN0.NoVerifiedLexicalAttestation",
    claim=("الرمزُ يحمل صورةً عربيّةً ومرجعًا معجميًّا بمُعرِّف مدخلةٍ وبصمتِها " "وبصمةِ مصدرها"),
    missing_authority=(
        "لا معجمَ مُجمَّدًا في `SPEC` تُقاس عليه هذه المراجع: "
        "`LexicalChoiceRef_SPEC ≠ VerifiedLexicalChoice_READOUT`، فلا تُثبِت هذه "
        "الطبقةُ أنّ `surface` صورةُ تلك المدخلة، ولا أنّها ليست نصًّا عربيًّا "
        "مُلفَّقًا موافقًا للوصف"
    ),
    discharge_condition=(
        "تجميدُ المعجم في `G0.GEN-0.DATA`، ثمّ مطابقةٌ في `G0.GEN-0.READOUT` بين "
        "`entry_id` و`entry_content_id` و`lexical_source_digest` و`surface`"
    ),
)

GENERATION_AUTHORITY_GAPS: Final[Mapping[str, GenerationAuthorityGap]] = (
    MappingProxyType(
        {
            gap.gap_id: gap
            for gap in (
                NO_INDEPENDENT_ANCHOR_TO_SYNTACTIC_FUNCTION_AUTHORITY,
                NO_VERIFIED_LEXICAL_ATTESTATION,
            )
        }
    )
)
