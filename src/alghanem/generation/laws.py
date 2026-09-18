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

**ومراجعةُ `G0.GEN-0.SPEC-H` مُعلنة**: أُضيفت ثلاثةُ قوانينَ بأسمائها —
`ContractMustBindClassNotFactory` و`ConformanceIsNotLicensing` و
`LexicalChoiceRefIsAClaimUntilTheReadout` — فتغيّرت بصمةُ المجموعة تغيُّرَ
مراجعةٍ مُصرَّحٍ بها لا تحسينَ صياغةٍ صامتًا. ولم يُحذَف نصُّ قانونٍ ولم يُبدَّل.

**والبقايا المعماريّةُ ليست قوانين** (`GENERATION_ARCHITECTURAL_RESIDUALS`): ما
لم تُثبِته هذه الطبقةُ يُسمّى بمُعرِّفه `RES.GEN0.…` خارج مجموعة القوانين، فلا
يدخل في بصمتها ولا يُقرأ حكمًا.

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
    "CONFORMANCE_IS_NOT_LICENSING",
    "CONTRACT_MUST_BIND_CLASS_NOT_FACTORY",
    "GENERATION_ARCHITECTURAL_RESIDUALS",
    "GENERATION_DOES_NOT_INVENT_INTENT",
    "GENERATION_LAWS",
    "GENERATION_LAW_SET_DIGEST",
    "GENERATION_LAW_SET_ID",
    "LEXICAL_CHOICE_REF_IS_A_CLAIM_UNTIL_THE_READOUT",
    "NO_INDEPENDENT_ANCHOR_TO_SYNTACTIC_FUNCTION_AUTHORITY",
    "NO_INDEPENDENT_ANCHOR_TO_SYNTACTIC_FUNCTION_AUTHORITY_ID",
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

CONTRACT_MUST_BIND_CLASS_NOT_FACTORY: Final[str] = (
    "العقدُ يلزم النوعَ لا طريقَ إنشائه: شرطٌ يُفحَص في مصنعٍ وحدَه شرطٌ "
    "اختياريّ، لأنّ المستدعي يبني النوعَ مباشرةً فيتجاوزه؛ فما لزم النوعَ "
    "لزمه في كلِّ طريقٍ إليه"
)

CONFORMANCE_IS_NOT_LICENSING: Final[str] = (
    "المطابقةُ ليست ترخيصًا: `CallerClaim → ConformsToCallerClaim ⇏ Licensed`؛ "
    "فبوّابةٌ تقيس المنتَجَ على دعوى صاحبه تُثبِت أنّ الدعوى حُفِظت لا أنّها "
    "مرخَّصةٌ من المصدر، والدعوى لا تكون دليلَ نفسها"
)

LEXICAL_CHOICE_REF_IS_A_CLAIM_UNTIL_THE_READOUT: Final[str] = (
    "المرجعُ المعجميُّ دعوى حتى القراءة: `LexicalChoiceRef_SPEC ≠ "
    "VerifiedLexicalChoice_READOUT`؛ فمُعرِّفُ المدخلة وبصمتُها وبصمةُ مصدرها "
    "مكتوبةٌ في المواصفة، ولا يُثبِت أنّ الصورةَ صورةُ تلك المدخلة إلّا معجمٌ "
    "مُجمَّدٌ في `GEN-0.DATA` ثمّ مطابقةٌ في `GEN-0.READOUT`"
)

NO_INDEPENDENT_ANCHOR_TO_SYNTACTIC_FUNCTION_AUTHORITY_ID: Final[str] = (
    "RES.GEN0.NoIndependentAnchorToSyntacticFunctionAuthority"
)

NO_INDEPENDENT_ANCHOR_TO_SYNTACTIC_FUNCTION_AUTHORITY: Final[str] = (
    "لا سلطةَ مستقلّةً تربط المرساةَ بوظيفةٍ نحويّة: `Anchor ⇏ فاعل/مفعولٌ به` "
    "باختيار المستدعي. والمصدرُ المرخَّصُ اليومَ — `AnchoredNisbahSignatureV3` — "
    "يحمل مراسيَ ومحمولًا ومواضعَ حجج، ولا يحمل رابطةَ ملءٍ بين مرساةٍ وموضعِ "
    "حجّة، بل يرفض `ArgumentSlot` أسماءَ الأدوار صراحةً. فإسنادُ الفاعليّة "
    "والمفعوليّة في `ProductionSpecification` دعوى صاحبِ المواصفة، وبوّابةُ "
    "المطابقة تُثبِت حفظَها لا ترخيصَها. ولا تُرفَع هذه البقيّةُ إلّا بشهادةِ "
    "ربطٍ مستقلّةٍ — `SyntacticBindingCertificate` — تُثبِت "
    "`Anchor →evidence→ LicensedSyntacticPosition`؛ وعندها وحدَها يُفتَح اسمُ "
    "`StructurallyLicensedSurface`"
)

GENERATION_ARCHITECTURAL_RESIDUALS: Final[Mapping[str, str]] = MappingProxyType(
    {
        NO_INDEPENDENT_ANCHOR_TO_SYNTACTIC_FUNCTION_AUTHORITY_ID: (
            NO_INDEPENDENT_ANCHOR_TO_SYNTACTIC_FUNCTION_AUTHORITY
        ),
    }
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
        "ContractMustBindClassNotFactory": CONTRACT_MUST_BIND_CLASS_NOT_FACTORY,
        "ConformanceIsNotLicensing": CONFORMANCE_IS_NOT_LICENSING,
        "LexicalChoiceRefIsAClaimUntilTheReadout": (
            LEXICAL_CHOICE_REF_IS_A_CLAIM_UNTIL_THE_READOUT
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
