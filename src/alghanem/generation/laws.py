"""دستورُ `G0.GEN-0`: قوانينُ الإنتاج مُجمَّدةً قبل أن يُنتَج حرفٌ واحد.

القانونُ الأوّل أنّ الإنتاج ليس عكسَ التحليل آليًّا:

    Analysis ≠ Generation⁻¹

    Generation : LicensedStructure → SurfaceCandidate

فالتحليلُ يذهب من سطحٍ موجودٍ إلى بنيةٍ مرخَّصة، والإنتاجُ يذهب من بنيةٍ سبق
ترخيصُها إلى مرشَّحٍ سطحيّ؛ ولا تُشتَقّ إحدى الجهتين من الأخرى بقلبِ دالّة.

والقانونُ الأعلى الذي تُقاس به هذه الطبقةُ كلُّها
(`NoGenerationAuthorityBeyondItsSource`): لا تدّعي طبقةُ إنتاجٍ أكثرَ ممّا حمله
المصدرُ المرخَّصُ والدليلُ المتاحُ لها؛ فالسطحُ لا يُنشِئ ترخيصًا، والرسمُ لا
يُنشِئ صرفًا، والرتبةُ لا تُنشِئ شهادة.

**والنصوصُ هنا محتوًى مُبصَّم** (`GENERATION_LAW_SET_DIGEST`): تعديلُ نصِّ
قانونٍ يُغيِّر البصمةَ فيسقط اختبارُها، لأنّ تحسينَ صياغةِ دستورٍ مُجمَّدٍ بعد
الاعتماد عليه نقضٌ لترتيب المراحل.

تسجيلٌ لا سلطة: لا ولادةَ، ولا حكمَ ولادةٍ، ولا تجميدَ `E0`، ولا تقرؤها بوّابةٌ
في `kernel/`، ولا تدخل في `BirthExperimentSpecification`.
"""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest

__all__ = [
    "ANALYSIS_IS_NOT_INVERTED_GENERATION",
    "AN_UNREALIZED_LAYER_IS_A_WITHHELD_STAGE_NOT_A_NULL",
    "A_POSITION_IS_NOT_A_SEMANTIC_ROLE",
    "CALLER_DOES_NOT_OWN_GENERATION_RANK",
    "GENERATION_DOES_NOT_INVENT_INTENT",
    "GENERATION_LAWS",
    "GENERATION_LAW_SET_DIGEST",
    "GENERATION_LAW_SET_ID",
    "NO_CERTIFIED_GENERATION_WITHOUT_ROUND_TRIP",
    "NO_COMPOSITION_WITHOUT_RELATION",
    "NO_GENERATION_AUTHORITY_BEYOND_ITS_SOURCE",
    "NO_INFLECTION_WITHOUT_LICENSED_SLOT",
    "NO_LEXEME_OUTSIDE_A_FROZEN_LEXICAL_SOURCE",
    "NO_SURFACE_WITHOUT_SOURCE_ANCHOR",
    "NO_WORD_FORM_WITHOUT_MORPHOLOGICAL_TRACE",
    "ORTHOGRAPHY_NEED_NOT_CLAIM_PHONOLOGICAL_DERIVATION",
    "RESIDUALS_ARE_OBSERVED_NOT_AUTHORED",
]


GENERATION_LAW_SET_ID: Final[str] = "alghanem.generation.laws.G0.GEN-0"

NO_GENERATION_AUTHORITY_BEYOND_ITS_SOURCE: Final[str] = (
    "لا سلطةَ لإنتاجٍ فوق مصدره: كلُّ طبقةٍ هنا لا تدّعي أكثرَ ممّا حمله المصدرُ "
    "المرخَّصُ والدليلُ المتاحُ لها؛ فلا يُستخرَج من السطح ترخيصٌ لم يُمنَح، ولا "
    "من الرسم صرفٌ لم يُقَس، ولا من الرتبة شهادةٌ لم تُصدَر"
)

ANALYSIS_IS_NOT_INVERTED_GENERATION: Final[str] = (
    "التحليلُ ليس إنتاجًا مقلوبًا: `Analysis ≠ Generation⁻¹`؛ فالإنتاجُ تحويلٌ "
    "مُرخَّصٌ من بنيةٍ مغلقةٍ إلى مرشَّحٍ سطحيّ، لا دالّةٌ تُقلَب على التحليل"
)

GENERATION_DOES_NOT_INVENT_INTENT: Final[str] = (
    "الإنتاجُ لا يخترع مقصدًا: `IntentCreation ≠ LanguageRealization`؛ فالمولِّدُ "
    "يُحقِّق بنيةً مقصودةً مرخَّصةً سابقةً، ولا يقرّر من نفسه ما يريد المتكلّمُ قولَه"
)

NO_SURFACE_WITHOUT_SOURCE_ANCHOR: Final[str] = (
    "لا سطحَ بلا مرساةِ مصدر: كلُّ رمزٍ منتَجٍ يُردّ إلى مرساةٍ في البنية المرخَّصة "
    "التي وُلِّد منها، ورمزٌ بلا مرساةٍ لفظٌ بلا سبب"
)

NO_INFLECTION_WITHOUT_LICENSED_SLOT: Final[str] = (
    "لا تصريفَ بلا موقعٍ مرخَّص: أثرُ الإعراب يتبع موقعًا تركيبيًّا مُسمًّى في "
    "العائلة الإنتاجيّة، ولا تُكتَب حركةُ آخرٍ من غير موقعٍ يقتضيها"
)

NO_WORD_FORM_WITHOUT_MORPHOLOGICAL_TRACE: Final[str] = (
    "لا صيغةَ بلا أثرٍ صرفيّ: كلُّ صورةِ كلمةٍ تحمل جهةَ تحصيلها مُسمّاةً، "
    "و«اختيارُ صورةٍ معجميّةٍ مشهودة» أثرٌ مُصرَّحٌ به لا اشتقاقٌ من جذر"
)

NO_COMPOSITION_WITHOUT_RELATION: Final[str] = (
    "لا تركيبَ بلا علاقة: ضمُّ الكلمات يتبع نسبةً مرخَّصةً في المصدر، ولا تُجاور "
    "كلمتان لأنّ ترتيبَ السطح سمح بذلك"
)

NO_CERTIFIED_GENERATION_WITHOUT_ROUND_TRIP: Final[str] = (
    "لا إنتاجَ مُشهَدًا بلا ذهابٍ وإياب: لا يبلغ المنتَجُ رتبتَه العليا إلّا "
    "بتحليلٍ يعيد بناءَ بنيته ويُطابِق ثوابتَها المطلوبة"
)

CALLER_DOES_NOT_OWN_GENERATION_RANK: Final[str] = (
    "المستدعي لا يملك رتبةَ الإنتاج: الرتبةُ ناتجُ بوّابةٍ لا حقلٌ يكتبه صاحبُ "
    "المواصفة، فمواصفةُ الإنتاج لا تحمل رتبةً ألبتّة"
)

RESIDUALS_ARE_OBSERVED_NOT_AUTHORED: Final[str] = (
    "البقايا مرصودةٌ لا مكتوبة: تخرج من انتقالٍ جرى فسمّى ما لم يُحسَم، ولا "
    "تُملى في المدخل؛ ومدخلٌ يحمل بقاياه يَعِد بما لم يُقَس"
)

A_POSITION_IS_NOT_A_SEMANTIC_ROLE: Final[str] = (
    "الموقعُ التركيبيُّ ليس دورًا دلاليًّا: فاعل ≠ Agent، ومفعولٌ به ≠ Patient "
    "دائمًا؛ فهدفُ التحقّق النحويِّ يقول أين تتحقّق المرساةُ، لا ما هي في الوجود"
)

NO_LEXEME_OUTSIDE_A_FROZEN_LEXICAL_SOURCE: Final[str] = (
    "لا لفظَ خارج مصدرٍ معجميٍّ مُجمَّد: الاختيارُ مرجعٌ مُبصَّمٌ إلى مدخلةٍ "
    "مُراجَعة، لا صورةٌ سطحيّةٌ تُكتَب في المواصفة ولا بحثٌ في مدوَّنةٍ أثناء التشغيل"
)

ORTHOGRAPHY_NEED_NOT_CLAIM_PHONOLOGICAL_DERIVATION: Final[str] = (
    "الرسمُ لا يلزمه ادّعاءُ اشتقاقٍ صوتيّ: الإسقاطان أخوان بعد التكوين لا "
    "ابنٌ عن أب، فتُنتَج الصورةُ الكتابيّةُ من مصدرٍ معجميٍّ مُجمَّدٍ بينما تبقى "
    "الطبقةُ الصوتيّةُ محجوزةً، ولا يُقرَأ الرسمُ دليلًا على وزنٍ أو مقطعٍ لم يُقَس"
)

AN_UNREALIZED_LAYER_IS_A_WITHHELD_STAGE_NOT_A_NULL: Final[str] = (
    "الطبقةُ غيرُ المُحقَّقة مرحلةٌ محجوزةٌ لا فراغ: `Generated ≠ Withheld` "
    "بالنوع لا بقيمةِ حقل، فلا يستوي «لم يُنتَج» و«أُنتِج فكان لا شيء»"
)

GENERATION_LAWS: Final[Mapping[str, str]] = MappingProxyType(
    {
        "NoGenerationAuthorityBeyondItsSource": (
            NO_GENERATION_AUTHORITY_BEYOND_ITS_SOURCE
        ),
        "AnalysisIsNotInvertedGeneration": ANALYSIS_IS_NOT_INVERTED_GENERATION,
        "GenerationDoesNotInventIntent": GENERATION_DOES_NOT_INVENT_INTENT,
        "NoSurfaceWithoutSourceAnchor": NO_SURFACE_WITHOUT_SOURCE_ANCHOR,
        "NoInflectionWithoutLicensedSlot": NO_INFLECTION_WITHOUT_LICENSED_SLOT,
        "NoWordFormWithoutMorphologicalTrace": NO_WORD_FORM_WITHOUT_MORPHOLOGICAL_TRACE,
        "NoCompositionWithoutRelation": NO_COMPOSITION_WITHOUT_RELATION,
        "NoCertifiedGenerationWithoutRoundTrip": (
            NO_CERTIFIED_GENERATION_WITHOUT_ROUND_TRIP
        ),
        "CallerDoesNotOwnGenerationRank": CALLER_DOES_NOT_OWN_GENERATION_RANK,
        "ResidualsAreObservedNotAuthored": RESIDUALS_ARE_OBSERVED_NOT_AUTHORED,
        "APositionIsNotASemanticRole": A_POSITION_IS_NOT_A_SEMANTIC_ROLE,
        "NoLexemeOutsideAFrozenLexicalSource": (
            NO_LEXEME_OUTSIDE_A_FROZEN_LEXICAL_SOURCE
        ),
        "OrthographyNeedNotClaimPhonologicalDerivation": (
            ORTHOGRAPHY_NEED_NOT_CLAIM_PHONOLOGICAL_DERIVATION
        ),
        "AnUnrealizedLayerIsAWithheldStageNotANull": (
            AN_UNREALIZED_LAYER_IS_A_WITHHELD_STAGE_NOT_A_NULL
        ),
    }
)

GENERATION_LAW_SET_DIGEST: Final[str] = canonical_digest(
    canonical_bytes(
        {
            "law_set_id": GENERATION_LAW_SET_ID,
            "laws": dict(GENERATION_LAWS),
        }
    )
)
