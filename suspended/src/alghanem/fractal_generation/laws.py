"""دستورُ `G0.FGEN-0`: قوانينُ التوليد الفراكتاليِّ مُجمَّدةً قبل أن تُولَّد عقدةٌ واحدة.

القانونُ الأوّل أنّ التوليدَ الخطّيَّ حالةٌ خاصّةٌ من التوليد الفراكتاليّ:

    LinearGeneration  ⊂  FractalGeneration

**وهذا في هذه المرحلة قانونٌ معماريٌّ مُعلَن لا مبرهنٌ بالأنواع**
(`DeclaredArchitecturalLaw ≠ ProvenContainment`): لا مُحوِّلَ بعدُ يربط
`generation/` بهذه الطبقة، فلا يُقرأ الاحتواءُ مُثبَتًا برمجيًّا؛ وإثباتُه
التشغيليُّ مؤجَّلٌ إلى مرحلة المُحوِّل.

والقانونُ الثاني أنّ الاقتراحَ ليس حركة (`Candidate ≠ Transition`): المرشَّحُ
يُقترَح، والحركةُ تقع بعد فصلٍ أفقيٍّ كامل؛ فلا أثرَ انتقالٍ قبل أن يقع انتقال.

والقانونُ الثالث أنّ الإغلاقَ رتبةٌ مُقيَّدةٌ بمقياسها:

    Closure  =  MinimalCompleteAtCurrentScale

فلا يُقرَأ استنفادًا للمقياس الأعلى، ولا ضرورةً للرفع، ولا معنًى، ولا صدقًا.

**والنصوصُ هنا محتوًى مُبصَّم** (`FRACTAL_GENERATION_LAW_SET_DIGEST`): تعديلُ
نصِّ قانونٍ يُغيِّر البصمةَ فيسقط اختبارُها. **والمجموعةُ مستقلّةٌ تمامًا** عن
مجموعتَي `generation/`: بصمتاهما `GENERATION_LAW_SET_DIGEST` و
`GENERATION_SPEC_H_LAW_SET_DIGEST` لا تُقرآن هنا ولا تُمَسّان.

تسجيلٌ لا سلطة: لا ولادةَ، ولا حكمَ ولادةٍ، ولا تجميدَ `E0`، ولا تقرؤها بوّابةٌ
في `kernel/`.
"""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest

__all__ = [
    "CANDIDATE_IS_NOT_TRANSITION",
    "CLOSED_WITH_AUTHORED_NECESSITY_CLAIM_DOES_NOT_ENTAIL_LIFT",
    "CLOSURE_IS_NOT_EXHAUSTION",
    "CLOSURE_IS_NOT_LIFT_NECESSITY",
    "CLOSURE_IS_NOT_MEANING",
    "CLOSURE_IS_NOT_TRUTH",
    "DECLARED_DIFFERENCE_IS_NOT_LICENSED_DIFFERENCE",
    "FRACTAL_GENERATION_LAWS",
    "FRACTAL_GENERATION_LAW_SET_DIGEST",
    "FRACTAL_GENERATION_LAW_SET_ID",
    "LINEAR_GENERATION_IS_CONTAINED_IN_FRACTAL_GENERATION",
    "NO_FORCED_CHOICE_AMONG_CO_ADMISSIBLE_BRANCHES",
    "NO_FRACTAL_TRANSITION_WITHOUT_RECONSTRUCTIBLE_TRACE",
    "NO_HIGHER_SCALE_WITHOUT_NECESSITY",
    "NO_RESIDUAL_ERASURE",
    "PATTERN_DECLARATION_IS_NOT_PATTERN_PROOF",
    "RESIDUAL_IS_NOT_DISPOSITION",
    "RUNTIME_RESIDUAL_IS_NOT_ARCHITECTURAL_AUTHORITY_GAP",
]


FRACTAL_GENERATION_LAW_SET_ID: Final[str] = "alghanem.fractal_generation.laws.G0.FGEN-0"

LINEAR_GENERATION_IS_CONTAINED_IN_FRACTAL_GENERATION: Final[str] = (
    "التوليدُ الخطّيُّ حالةٌ خاصّةٌ من الفراكتاليّ: `LinearGeneration ⊂ "
    "FractalGeneration`؛ وهو في هذه المرحلة قانونٌ معماريٌّ مُعلَنٌ لا احتواءٌ "
    "مُبرهَنٌ بالأنواع، لأنّ المُحوِّلَ الذي يُثبِته لم يُفتَح بعد"
)

CANDIDATE_IS_NOT_TRANSITION: Final[str] = (
    "المرشَّحُ ليس حركة: `Candidate ≠ Transition`؛ فالاقتراحُ يُعرَض ويُقاس "
    "ويُفصَل فيه، ولا يحمل أثرَ انتقالٍ لأنّ الانتقالَ لم يقع بعد"
)

RESIDUAL_IS_NOT_DISPOSITION: Final[str] = (
    "البقيّةُ ليست حكمًا: `Residual ≠ Disposition`؛ فالبقيّةُ ما لم يُحسَم في "
    "حركةٍ جرت، والحكمُ رتبةُ الفرع نفسِه؛ فلا تُجعَل البقيّةُ حالةً من حالات الوقوف"
)

PATTERN_DECLARATION_IS_NOT_PATTERN_PROOF: Final[str] = (
    "إعلانُ النمط ليس برهانَه: `PatternDeclaration ≠ PatternProof`؛ فعقدُ النمط "
    "يُصرِّح بما يَعِد بحفظه، ولا يُثبِت أنّه حَفِظه في تشغيلٍ لم يُقرَأ"
)

DECLARED_DIFFERENCE_IS_NOT_LICENSED_DIFFERENCE: Final[str] = (
    "الفرقُ المُصرَّحُ ليس فرقًا مرخَّصًا: `DeclaredDifference ≠ "
    "LicensedDifference`؛ ومطابقةُ الفرق لعقد نمطه تُثبِت المطابقةَ وحدَها، "
    "والدعوى لا تكون دليلَ نفسها"
)

CLOSURE_IS_NOT_EXHAUSTION: Final[str] = (
    "الإغلاقُ ليس استنفادًا: `Closure ≠ Exhaustion`؛ فالإغلاقُ أقلُّ تمامٍ عند "
    "المقياس الجاري، لا استيفاءٌ لكلِّ ما يمكن أن يُقال في المقياس الأعلى"
)

CLOSURE_IS_NOT_LIFT_NECESSITY: Final[str] = (
    "الإغلاقُ ليس ضرورةَ رفع: `Closure ≠ LiftNecessity`؛ فعقدةٌ مغلقةٌ تامّةٌ عند "
    "مقياسها لا تقتضي بذاتها مقياسًا أعلى"
)

CLOSURE_IS_NOT_MEANING: Final[str] = (
    "الإغلاقُ ليس معنًى: `Closure ≠ Meaning`؛ فتمامُ البنية عند مقياسها لا "
    "يُنشِئ دلالةً، ولا سلطةَ دلاليّةً في توليدٍ صوريّ"
)

CLOSURE_IS_NOT_TRUTH: Final[str] = (
    "الإغلاقُ ليس صدقًا: `Closure ≠ Truth`؛ فالبنيةُ المغلقةُ مُقاسةٌ على عقدها "
    "لا على العالَم، وتمامُ الصورة ليس مطابقتَها للواقع"
)

CLOSED_WITH_AUTHORED_NECESSITY_CLAIM_DOES_NOT_ENTAIL_LIFT: Final[str] = (
    "الإغلاقُ مع دعوى ضرورةٍ من المستدعي لا يُنتِج رفعًا: `Closed ∧ "
    "AuthoredNecessityClaim ⇏ Lift`؛ فدعوى الضرورة مكتوبةٌ بيد صاحبها، "
    "وشهادةُ الضرورة سلطةٌ لم تُفتَح في هذه المرحلة"
)

RUNTIME_RESIDUAL_IS_NOT_ARCHITECTURAL_AUTHORITY_GAP: Final[str] = (
    "بقيّةُ التشغيل ليست فجوةَ سلطةٍ معماريّة: `RuntimeResidual ≠ "
    "ArchitecturalAuthorityGap`؛ فالأولى ترصدها حركةٌ جرت، والثانيةُ معلومةٌ "
    "قبل أيِّ تشغيلٍ لأنّ بنيةَ الطبقة لا تحمل السلطةَ المطلوبة"
)

NO_FORCED_CHOICE_AMONG_CO_ADMISSIBLE_BRANCHES: Final[str] = (
    "لا ترجيحَ مفروضًا بين فروعٍ مقبولةٍ معًا: إن قُبِل فرعان فلا تختر أحدَهما "
    "ولا ترتِّبهما، فترتيبُ العرض ليس حكمًا، وأفضليّةٌ بلا سلطةٍ اختلاقُ حكم"
)

NO_RESIDUAL_ERASURE: Final[str] = (
    "لا محوَ لبقيّة: ما رُصِد يبقى مُسمًّى في القرار وفي العقدة المغلقة، "
    "وفرعٌ مُنِع أو أُجِّل يبقى في السجلّ؛ فالحذفُ ليس حسمًا"
)

NO_HIGHER_SCALE_WITHOUT_NECESSITY: Final[str] = (
    "لا مقياسَ أعلى بلا ضرورة: الرفعُ يقتضي تمامًا عند المقياس الجاري، "
    "واستنفادًا له، وبقيّةً غيرَ قابلةٍ للردّ فيه، وبنيةً أعلى لازمةً؛ "
    "وما لم تُثبَت الضرورةُ بسلطتها فالتأجيلُ هو الحكم"
)

NO_FRACTAL_TRANSITION_WITHOUT_RECONSTRUCTIBLE_TRACE: Final[str] = (
    "لا انتقالَ فراكتاليَّ بلا أثرٍ قابلٍ لإعادة البناء: كلُّ حركةٍ تُسمّي "
    "حاملَها وهويّتَها قبلَ وبعد ونمطَها وبوّابتَها ومقياسَها وبقاياها، "
    "ومخرجُ خطوةٍ هو مدخلُ التالية بعينه"
)

FRACTAL_GENERATION_LAWS: Final[Mapping[str, str]] = MappingProxyType(
    {
        "LinearGenerationIsContainedInFractalGeneration": (
            LINEAR_GENERATION_IS_CONTAINED_IN_FRACTAL_GENERATION
        ),
        "CandidateIsNotTransition": CANDIDATE_IS_NOT_TRANSITION,
        "ResidualIsNotDisposition": RESIDUAL_IS_NOT_DISPOSITION,
        "PatternDeclarationIsNotPatternProof": PATTERN_DECLARATION_IS_NOT_PATTERN_PROOF,
        "DeclaredDifferenceIsNotLicensedDifference": (
            DECLARED_DIFFERENCE_IS_NOT_LICENSED_DIFFERENCE
        ),
        "ClosureIsNotExhaustion": CLOSURE_IS_NOT_EXHAUSTION,
        "ClosureIsNotLiftNecessity": CLOSURE_IS_NOT_LIFT_NECESSITY,
        "ClosureIsNotMeaning": CLOSURE_IS_NOT_MEANING,
        "ClosureIsNotTruth": CLOSURE_IS_NOT_TRUTH,
        "ClosedWithAuthoredNecessityClaimDoesNotEntailLift": (
            CLOSED_WITH_AUTHORED_NECESSITY_CLAIM_DOES_NOT_ENTAIL_LIFT
        ),
        "RuntimeResidualIsNotArchitecturalAuthorityGap": (
            RUNTIME_RESIDUAL_IS_NOT_ARCHITECTURAL_AUTHORITY_GAP
        ),
        "NoForcedChoiceAmongCoAdmissibleBranches": (
            NO_FORCED_CHOICE_AMONG_CO_ADMISSIBLE_BRANCHES
        ),
        "NoResidualErasure": NO_RESIDUAL_ERASURE,
        "NoHigherScaleWithoutNecessity": NO_HIGHER_SCALE_WITHOUT_NECESSITY,
        "NoFractalTransitionWithoutReconstructibleTrace": (
            NO_FRACTAL_TRANSITION_WITHOUT_RECONSTRUCTIBLE_TRACE
        ),
    }
)

FRACTAL_GENERATION_LAW_SET_DIGEST: Final[str] = canonical_digest(
    canonical_bytes(
        {
            "law_set_id": FRACTAL_GENERATION_LAW_SET_ID,
            "laws": dict(FRACTAL_GENERATION_LAWS),
        }
    )
)
