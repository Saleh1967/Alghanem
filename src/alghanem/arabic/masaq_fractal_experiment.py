"""تشغيلُ النواة الفراكتاليّة على مادّةِ MASAQ المُجمَّدة، تجريبًا لا ترخيصًا.

    ALGHANEM_MASAQ_PATH
      → بايتاتٌ موثَّقةٌ ببصمتها وطولها
      → FrozenExperimentBinding (الصورةُ مرئيّةٌ، والوَسْمُ محجوب)
      → ExperimentalRunPermit (ISSUED → ACTIVE)
      → تشغيلٌ فراكتاليٌّ لكلّ كلمة
      → ExperimentalNextScaleSeed
      → FractalExperimentalWitness
      → WitnessBundle
      → REVOKED

**والوَسْمُ المُودَع في MASAQ لا ينزل في مدخل المُولِّد**؛ فهو حكمُ بشرٍ لا
قياس، ولو نزل لكان المحرِّكُ يُلقِّن نفسَه جوابَه
(`FrozenExpectationIsNotGenerativeInput`). فالمُولِّد لا يرى إلا الصورةَ
المُقطَّعةَ وموضعَها، ويدخل الوَسْمُ في القراءة بعد التشغيل شاهدًا لا مدخلًا.

**ولا ترخيصَ هنا**: النجاحُ شاهدٌ، والإخفاقُ شاهد، وضعفُ القوّة شاهد؛ وأقصى ما
تبلغه الشواهدُ تجميعٌ في حزمةٍ بلا حكم (`ExperimentBeforeLicense`).

**والشاهدُ لا يُسمّى دعمًا بنيويًّا مميِّزًا ما دام نموذجٌ أضعفُ يبلغ المخرجَ
عينَه**؛ فصحّةُ المخرج ليست ضرورةَ البنية
(`WeakerModelTieBlocksDistinctiveStructuralSupport`). والوقوفُ يُشتقّ من شروطه
المُسجَّلة مجتمعةً، لا من الإغلاق وإعادة البناء وحدهما.

**ومع ذلك لا يُلغي التعادلُ نجاحَ المهمّة**: للكلمة الواحدة محوران مستقلّان،
حالُ المهمّة (`ExperimentalTaskOutcome`) وموقعُ المقارنة (`ComparativeStanding`)؛
فقد تكون إعادةُ البناء ناجحةً، والطريقتان متعادلتين، والوقوفُ التجريبيُّ
`UNDERPOWERED` معًا بلا تناقض (`TaskOutcome != ComparativeStanding`).

وخمسةُ قيودٍ تحكم مادّةَ الشاهد:

    WeakerModelTieBlocksDistinctiveStructuralSupport
    TaskOutcome     ≠  ComparativeStanding
    RawOccurrence   ≠  NormalizedProjection
    SourceWordNo    ≠  DerivedLocalPosition
    HeldOut         ≠  Dropped

ولا يُدَّعى هنا أنّ وحدةَ الكلمة لا تُردُّ إلى مقياس المقطع؛ فتلك دعوى لم تُقَس،
والنموذجُ الأضعفُ يبلغ الكلمةَ بالوصل المباشر. والرفعُ التجريبيُّ يبقى مفتوحًا
لأنّه يختبر الضرورةَ ولا يشهد بها.

الاتّجاه: `arabic → fractal_experiment → fractal_generation`، ولا عكس.

تسجيلٌ لا سلطة: لا ترخيصَ، ولا رتبةَ دائمة، ولا حكمَ كفاية.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from ..fractal_experiment import (
    NO_LICENSING_AUTHORITY,
    NO_SCALE_NECESSITY_CERTIFICATION_IN_EXPERIMENT,
    NO_SEMANTIC_AUTHORITY_IN_EXPERIMENT,
    NO_SUFFICIENCY_ASSESSMENT_AUTHORITY,
    ExperimentalFractalAuthority,
    ExperimentalLiftCandidate,
    ExperimentalLiftGate,
    ExperimentalLiftStatus,
    ExperimentalPermitState,
    ExperimentalRunPermit,
    ExperimentalStanding,
    ExperimentalTransitionGate,
    FractalExperimentalWitness,
    FrozenExperimentBinding,
    FrozenInputEntry,
    WitnessBundle,
    WitnessSufficiencyContract,
    issue_experimental_lift_permit,
)
from ..fractal_generation import (
    BranchAdjudicationDecision,
    BranchAdjudicationGate,
    BranchAssessment,
    BranchStanding,
    ClosureCandidate,
    ClosureGate,
    ClosureRequirement,
    DeclaredDifference,
    ExpansionCandidate,
    ExpansionSet,
    FractalIdentity,
    FractalNode,
    FractalResidual,
    FractalResidualKind,
    FractalScaleContract,
    FractalSeed,
    FractalTrace,
    FractalTransition,
    FractalTransitionGate,
    FractalTransitionTraceStep,
    IdentityPreservingTransformationCandidate,
    InvariantAudit,
    MinimumCompleteRequirement,
    PatternConformanceGate,
    PatternConformanceStatus,
    PatternConformantDifference,
    PatternContract,
    ProposalProvenance,
    ScaleClosureContract,
    ScaleRelation,
    ScaleRelationEdge,
    ScaleSpace,
)
from .masaq_corpus_deposit import (
    MORPH_TAG_COLUMN,
    SEGMENT_INDEX_COLUMN,
    WORD_KEY_COLUMN,
    masaq_records,
    read_masaq_bytes,
)
from .referent_candidate_preregistration import strip_surface

__all__ = [
    "ACCRETION_OPERATION",
    "ACCRETION_PATTERN",
    "GENERATOR_VISIBLE_COLUMNS",
    "HELD_OUT_MASAQ_COLUMN_ABSENT",
    "HELD_OUT_READOUT_COLUMNS",
    "HELD_OUT_IS_NOT_DROPPED",
    "LOCAL_SEGMENT_POSITION_FIELD",
    "MASAQ_EXPERIMENT_ID",
    "MASAQ_PREREGISTRATION",
    "MASAQ_PREREGISTRATION_CONTENT_ID",
    "MASAQ_SUFFICIENCY_CONTRACT",
    "RAW_OCCURRENCE_IS_NOT_NORMALIZED_PROJECTION",
    "SEGMENT_CLOSURE_CONTRACT",
    "SEGMENT_SCALE",
    "SEGMENT_SCALE_REF",
    "SOURCE_WORD_NO_IS_NOT_DERIVED_LOCAL_POSITION",
    "STRIP_SURFACE_TRANSFORMATION",
    "TASK_OUTCOME_IS_NOT_COMPARATIVE_STANDING",
    "UNRESOLVED_SCALE_NECESSITY_REASON",
    "WEAKER_MODEL_TIES_FRACTAL_MODEL",
    "WEAKER_MODEL_TIE_BLOCKS_DISTINCTIVE_STRUCTURAL_SUPPORT",
    "WORD_SCALE",
    "WORD_SCALE_REF",
    "ComparativeStanding",
    "ExperimentalTaskOutcome",
    "HeldOutMASAQAnnotation",
    "MasaqExperimentError",
    "MasaqExperimentReport",
    "MasaqSegmentOccurrence",
    "MasaqWordInput",
    "MasaqWordReading",
    "NegativeControlObservation",
    "NormalizationTrace",
    "StandingEvidence",
    "WeakerModelObservation",
    "build_frozen_binding",
    "build_word_inputs",
    "derive_comparative_standing",
    "derive_task_outcome",
    "derive_standing",
    "normalize_segment_surface",
    "read_masaq_word_inputs",
    "run_masaq_fractal_experiment",
]

SURA_COLUMN: Final[str] = "Sura_No"
VERSE_COLUMN: Final[str] = "Verse_No"
SEGMENTED_WORD_COLUMN: Final[str] = "Segmented_Word"

GENERATOR_VISIBLE_COLUMNS: Final[tuple[str, ...]] = (
    SURA_COLUMN,
    VERSE_COLUMN,
    WORD_KEY_COLUMN,
    SEGMENT_INDEX_COLUMN,
    SEGMENTED_WORD_COLUMN,
)
"""الحقولُ التي يراها المُولِّد: موضعُ الصورة وصورتُها، لا حكمَ أحدٍ عليها."""

HELD_OUT_READOUT_COLUMNS: Final[tuple[str, ...]] = (
    "Case_Mood",
    "Lemma",
    "Morph_type",
    MORPH_TAG_COLUMN,
    "Syntactic_Role",
)
"""الحقولُ المحجوبةُ عن المُولِّد؛ تُقرأ بعد التشغيل ولا تدخل فيه."""

LOCAL_SEGMENT_POSITION_FIELD: Final[str] = "LocalSegmentPosition"
"""اسمُ الموضع المحلّيِّ المشتقّ؛ ولا يُكتَب تحت اسم عمود المصدر."""

HELD_OUT_MASAQ_COLUMN_ABSENT: Final[str] = "HELD_OUT_COLUMN_ABSENT"
"""عَلَمُ غيابِ العمود عن السجلّ؛ يُفرَّق به الغيابُ عن القيمة الفارغة."""

STRIP_SURFACE_TRANSFORMATION: Final[str] = "strip_surface"
"""اسمُ التحويل المُعلَن بين الصورة الخام وصورة المُولِّد."""

WEAKER_MODEL_TIES_FRACTAL_MODEL: Final[str] = "WEAKER_MODEL_TIES_FRACTAL_MODEL"
"""اسمُ البقيّة حين يبلغ النموذجُ الأضعفُ مخرجَ النموذج الفراكتاليِّ عينَه."""

WEAKER_MODEL_TIE_BLOCKS_DISTINCTIVE_STRUCTURAL_SUPPORT: Final[str] = (
    "WeakerModelTieBlocksDistinctiveStructuralSupport: إذا بلغ النموذجُ الأضعفُ "
    "المخرجَ عينَه فلا تُسمَّ النتيجةُ دعمًا بنيويًّا مميِّزًا؛ ويبقى نجاحُ المهمّة "
    "نفسِه قائمًا، فالتعادلُ يمنع دعوى التمييز لا صحّةَ العمل"
)
"""قانونُ الوقوف: تعادلُ الأضعف يمنع دعوى التمييز لا نجاحَ المهمّة."""

TASK_OUTCOME_IS_NOT_COMPARATIVE_STANDING: Final[str] = (
    "TaskOutcome != ComparativeStanding: بلوغُ الجبرِ غايتَه في المدخل محورٌ، "
    "وموقعُه من نموذجٍ أضعفَ محورٌ آخر؛ ونجاحُ طريقتين صحيحتين ليس إخفاقًا"
)
"""قانونُ المحورين: التغطيةُ تُقاس على حدة، والتمييزُ يُقاس على حدة."""

RAW_OCCURRENCE_IS_NOT_NORMALIZED_PROJECTION: Final[str] = (
    "RawOccurrence != NormalizedProjection: الصورةُ الخامُّ تبقى محفوظةً في "
    "الشاهد، والتطبيعُ تحويلٌ مُعلَنٌ قابلٌ للتدقيق لا محوٌ للمادّة"
)
"""قانونُ المادّة: التحويلُ لا يُسقِط أصلَه."""

SOURCE_WORD_NO_IS_NOT_DERIVED_LOCAL_POSITION: Final[str] = (
    "SourceWordNo != DerivedLocalPosition: موضعُ المصدر يُحفَظ بعينه، "
    "والموضعُ المحلّيُّ المشتقُّ يُسمّى باسمه ولا ينتحل اسمَ عمود المصدر"
)
"""قانونُ الموضع: لا يُعاد اختراعُ ``Word_No``."""

HELD_OUT_IS_NOT_DROPPED: Final[str] = (
    "HeldOut != Dropped: الحقولُ المحجوبةُ تُجمَّد كاملةً في الشاهد ولا تنزل "
    "في مدخل المُولِّد؛ فحجبُها عن التوليد ليس إسقاطًا لها عن القراءة"
)
"""قانونُ الحجب: مفتاحُ الإجابة يُخفى ولا يُمزَّق."""

UNRESOLVED_SCALE_NECESSITY_REASON: Final[str] = (
    "ضرورةُ المقياس الأعلى تحت الاختبار، ولم تثبت عدمُ قابليّة الرَّدِّ في " "المقياس الجاري"
)
"""بقيّةٌ غيرُ حاسمة تحلُّ محلَّ دعوى عدم القابليّة للرَّدِّ قبل قياسها."""

MASAQ_EXPERIMENT_ID: Final[str] = "experiment.masaq.segment_accretion"

MASAQ_PREREGISTRATION: Final[Mapping[str, object]] = {
    "experiment_id": MASAQ_EXPERIMENT_ID,
    "target_claim": (
        "يُدَّعى أنّ كلمةَ MASAQ تُبلَغ من مقاطعها بحركاتٍ حافظةٍ للهويّة "
        "متتابعةٍ تُغلَق عند مقياس المقطع، وأنّ بلوغَ مقياس الكلمة يقتضي رفعًا"
    ),
    "generator_visible_columns": list(GENERATOR_VISIBLE_COLUMNS),
    "held_out_readout_columns": list(HELD_OUT_READOUT_COLUMNS),
    "what_would_be_observed_as_refutation": (
        "أن تُخالف إعادةُ بناء الصورة من مخرج الحركات الصورةَ المُجمَّدة، "
        "أو ألّا تُغلَق العقدةُ عند مقياس المقطع"
    ),
    "negative_control": (
        "عكسُ ترتيب المقاطع يجب أن يُخالف إعادةَ البناء إن تعدّدت المقاطع"
    ),
    "negative_controls_are_runs": [
        "يُشغَّل ضابطُ عكس الترتيب عبر مسار إعادة البناء عينِه لا مقارنةً نصّيّةً جانبيّة",
        "يُشغَّل ضابطُ إسقاط مقطعٍ عبر مسار إعادة البناء عينِه ويُسجَّل مدخلُه وتحويلُه ومخرجُه",
        "ضابطٌ لا يُحدِث فرقًا يُسجَّل عاجزًا عن التمييز ويُفضي إلى underpowered",
    ],
    "weaker_model": "وصلُ المقاطع نصًّا بلا حركاتٍ فراكتاليّةٍ يبلغ الصورةَ نفسَها",
    "weaker_model_tie_rule": (
        "إذا بلغ النموذجُ الأضعفُ مخرجَ النموذج الفراكتاليِّ عينَه فالوقوفُ "
        "underpowered لا observed_support، وتُسجَّل بقيّةٌ باسم "
        + WEAKER_MODEL_TIES_FRACTAL_MODEL
        + "؛ والتعادلُ يمنع دعوى التمييز ولا يمنع نجاحَ المهمّة"
    ),
    "irreducibility_is_not_asserted": (
        "لا يُدَّعى في هذه المرحلة أنّ وحدةَ الكلمة لا تُردُّ إلى مقياس المقطع؛ "
        "والرفعُ التجريبيُّ يختبر الضرورةَ ولا يشهد بها"
    ),
    "task_outcome_is_not_comparative_standing": (
        TASK_OUTCOME_IS_NOT_COMPARATIVE_STANDING
        + "؛ فتُسجَّل لكلِّ كلمةٍ حالُ مهمّةٍ وموقعُ مقارنةٍ ووقوفٌ تجريبيٌّ معًا"
    ),
    "task_outcome_vocabulary": ["success", "failure", "unresolved"],
    "comparative_standing_vocabulary": [
        "fractal_only",
        "weaker_only",
        "both_succeed",
        "both_fail",
        "not_comparable",
    ],
    "raw_occurrence_is_preserved": RAW_OCCURRENCE_IS_NOT_NORMALIZED_PROJECTION,
    "source_word_no_is_preserved": SOURCE_WORD_NO_IS_NOT_DERIVED_LOCAL_POSITION,
    "held_out_is_not_dropped": HELD_OUT_IS_NOT_DROPPED,
    "standing_vocabulary": [
        "observed_support",
        "observed_refutation",
        "underpowered",
        "run_failure",
    ],
    "no_licensing_in_this_stage": True,
}
"""تسجيلٌ مُسبَقٌ مُجمَّدٌ يُكتَب قبل التشغيل؛ ولا يُعدَّل بعد قراءة الشواهد."""

MASAQ_PREREGISTRATION_CONTENT_ID: Final[str] = canonical_digest(
    canonical_bytes(dict(MASAQ_PREREGISTRATION))
)

MASAQ_SUFFICIENCY_CONTRACT: Final[WitnessSufficiencyContract] = (
    WitnessSufficiencyContract(
        contract_id="contract.masaq.segment_accretion",
        target_claim=str(MASAQ_PREREGISTRATION["target_claim"]),
        required_scope="كلماتُ MASAQ المُقطَّعةُ في مدى التشغيل المُعلَن",
        independence_criterion="تشغيلاتٌ بمُعرِّفاتٍ متمايزةٍ على مدخلاتٍ متمايزة",
        positive_witness_requirement="نصابُ الشواهد المؤيِّدة يُحدَّد قبل عدِّها",
        negative_controls=(
            "عكسُ ترتيب المقاطع يُخالف إعادةَ البناء",
            "إسقاطُ مقطعٍ يُخالف إعادةَ البناء",
        ),
        weaker_model_requirement="أن يُبيَّن ما يعجز عنه وصلُ النصّ المجرَّد",
        counterexample_policy="كلُّ نقضٍ مرصودٍ يُحفَظ ولا يُمحى من الحزمة",
        replication_requirement="إعادةُ التشغيل على البصمة عينِها تُعطي الشواهدَ عينَها",
        reconstruction_requirement="الأثرُ يُعيد بناءَ المخرج من المدخل بلا فجوة",
        residual_tolerance="البقايا تُسمّى ولا تُمحى؛ وحدُّ احتمالها يُحدَّد لاحقًا",
        blocking_residuals=("بقيّةٌ تمنع الإغلاق عند مقياس المقطع",),
    )
)
"""عقدُ كفايةٍ **معلَنٌ فقط**؛ لا مُقيِّمَ له هنا، وقياسُه سلطةٌ لم تُفتَح."""

SEGMENT_SCALE: Final[FractalScaleContract] = FractalScaleContract(
    scale_id="masaq.segment",
    domain_id="domain.masaq.surface",
    unit_criterion="الوحدةُ مقطعٌ واحدٌ من تقطيع MASAQ لكلمةٍ واحدة",
    identity_criterion="الهويّةُ مُعرِّفُ كلمةٍ مُقطَّعةٍ على حاملها",
    admissible_operation_contract="ضمُّ مقطعٍ تالٍ مع حفظ عين الهويّة وترتيبِ المقاطع",
    closure_contract="أقلُّ التمام: هويّةٌ مُحَلّةٌ وأثرٌ متّصلٌ وسجلُّ فروعٍ تامّ",
)

WORD_SCALE: Final[FractalScaleContract] = FractalScaleContract(
    scale_id="masaq.word",
    domain_id="domain.masaq.surface",
    unit_criterion="الوحدةُ كلمةٌ مُجمَّعةٌ من مقاطعها",
    identity_criterion="الهويّةُ مُعرِّفُ تجميعٍ لا مُعرِّفُ مقطع",
    admissible_operation_contract="عملياتُ هذا المقياس غيرُ مفتوحةٍ في هذه المرحلة",
    closure_contract="عقدُ إغلاقِ هذا المقياس مؤجَّلٌ حتى تُفتَح سلطتُه",
)

SCALE_SPACE: Final[ScaleSpace] = ScaleSpace(
    contracts=(SEGMENT_SCALE, WORD_SCALE),
    relations=(
        ScaleRelationEdge(
            relation=ScaleRelation.AGGREGATES,
            lower_scale_id="masaq.segment",
            higher_scale_id="masaq.word",
        ),
    ),
)

SEGMENT_SCALE_REF: Final = SEGMENT_SCALE.as_ref()
WORD_SCALE_REF: Final = WORD_SCALE.as_ref()

PRESERVED: Final[tuple[str, ...]] = ("carrier_continuity", "segment_order")

ACCRETION_PATTERN: Final[PatternContract] = PatternContract(
    pattern_id="pattern.masaq.segment_accretion",
    domain_id="domain.masaq.surface",
    applicable_scales=(SEGMENT_SCALE_REF,),
    admissible_seed_contract="بذرةٌ هي المقطعُ الأوّلُ من كلمةٍ مُقطَّعةٍ غيرِ فارغة",
    operation_contract="ضمُّ المقطع التالي إلى المحتوى مع حفظ ترتيب المقاطع",
    preserved_invariants=PRESERVED,
    declared_variation_contract="الفرقُ مُصرَّحٌ في بُعد الضمّ لا في الهويّة",
    reapplication_condition="يُعاد الضمُّ ما بقي في الكلمة مقطعٌ لم يُضَمّ",
    closure_requirements=("MRK.masaq.segment.trace", "MRK.masaq.segment.branches"),
    branch_conditions=("لا ولادةَ فرعٍ في هذا التشغيل",),
    blockers=("morphological_tag", "syntactic_role"),
    residual_policy="كلُّ ما لم يُحسَم يُسمّى بقيّةً غيرَ ممحوّة",
    authority_scope="صوريٌّ على الصورة المُقطَّعة؛ لا سلطةَ دلاليّةَ فيه",
)

PATTERN_REF: Final = ACCRETION_PATTERN.as_ref()

ACCRETION_OPERATION: Final[str] = "masaq.segment_accretion"

SEGMENT_CLOSURE_CONTRACT: Final[ScaleClosureContract] = ScaleClosureContract(
    scale_ref=SEGMENT_SCALE_REF,
    requirements=(
        MinimumCompleteRequirement(
            requirement_id="MRK.masaq.segment.identity",
            statement="هويّةُ العقدة مُحَلّةٌ عند مقياسها بعقده",
            evidence_kind="resolved_scale_ref",
        ),
        MinimumCompleteRequirement(
            requirement_id="MRK.masaq.segment.trace",
            statement="أثرُ بلوغ العقدة متّصلٌ ببصماته",
            evidence_kind="transition_trace",
        ),
        MinimumCompleteRequirement(
            requirement_id="MRK.masaq.segment.branches",
            statement="سجلُّ الفروع تامٌّ بأحكامه وبقاياه",
            evidence_kind="branch_record",
        ),
    ),
)

PROVENANCE: Final[ProposalProvenance] = ProposalProvenance(
    proposer_id="proposer.masaq.segment_accretion",
    basis="عقدُ النمط وترتيبُ المقاطع المُجمَّد",
    reason="عرضُ ضمِّ المقطع التالي عند مقياس المقطع",
)


class MasaqExperimentError(ValueError):
    """رفضٌ عند بناء تشغيل MASAQ التجريبيِّ أو قراءةِ مادّته."""


@dataclass(frozen=True, slots=True)
class NormalizationTrace:
    """أثرُ التطبيع: التحويلُ، والأصلُ، والناتجُ، وما حُذِف بمواضعه."""

    transformation: str
    raw: str
    normalized: str
    removed: tuple[tuple[int, str], ...]

    def __post_init__(self) -> None:
        if not self.transformation.strip():
            raise MasaqExperimentError("اسمُ التحويل نصٌّ غير فارغ")

    def replay(self) -> str:
        """أعِد بناءَ الناتج من الأصل بحذف المواضع المُسجَّلة؛ تدقيقًا لا ثقة."""

        removed_positions = {position for position, _ in self.removed}
        return "".join(
            character
            for position, character in enumerate(self.raw)
            if position not in removed_positions
        )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الأثر للبصمة؛ الحذفُ مُسمًّى بمواضعه لا مطويّ."""

        return {
            "transformation": self.transformation,
            "raw": self.raw,
            "normalized": self.normalized,
            "removed": [[position, character] for position, character in self.removed],
        }


def normalize_segment_surface(raw: str) -> NormalizationTrace:
    """طبِّع صورةَ المقطع تحويلًا مُعلَنًا مدخلُه الصورةُ الخامُّ بعينها لا مُجرَّدَها.

    ``raw`` هو نصُّ MASAQ حرفيًّا؛ وحذفُ الفراغ الطرفيِّ نفسُه عمليّةٌ من عمليّات
    التحويل تُسجَّل بموضعها الأصليّ، لا خطوةٌ تسبق الأثرَ فتغيب عنه.
    """

    exact_raw = raw or ""
    normalized = strip_surface(exact_raw)
    removed: list[tuple[int, str]] = []
    cursor = 0
    for position, character in enumerate(exact_raw):
        if cursor < len(normalized) and normalized[cursor] == character:
            cursor += 1
            continue
        removed.append((position, character))
    if cursor != len(normalized):
        raise MasaqExperimentError(
            "التطبيعُ ليس حذفًا خالصًا؛ ولا يُطوى تحويلٌ لا يُعاد بناؤه"
        )
    return NormalizationTrace(
        transformation=STRIP_SURFACE_TRANSFORMATION,
        raw=exact_raw,
        normalized=normalized,
        removed=tuple(removed),
    )


@dataclass(frozen=True, slots=True)
class HeldOutMASAQAnnotation:
    """وسومُ MASAQ المحجوبةُ عن المُولِّد، مُجمَّدةً كاملةً للقراءة بعد التشغيل."""

    values: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        names = tuple(name for name, _ in self.values)
        if names != HELD_OUT_READOUT_COLUMNS:
            raise MasaqExperimentError(
                "الوسومُ المحجوبةُ تُجمَّد بأعمدتها الخمسة بترتيبها؛ و"
                + HELD_OUT_IS_NOT_DROPPED
            )

    @classmethod
    def from_record(cls, record: Mapping[str, str]) -> HeldOutMASAQAnnotation:
        """اقرأ الأعمدةَ الخمسةَ من سجلٍّ واحد؛ والغيابُ يُسمّى ولا يُخلَط بالفراغ."""

        return cls(
            values=tuple(
                (
                    name,
                    record[name] if name in record else HELD_OUT_MASAQ_COLUMN_ABSENT,
                )
                for name in HELD_OUT_READOUT_COLUMNS
            )
        )

    def value_of(self, column: str) -> str:
        """قيمةُ عمودٍ محجوبٍ بعينه؛ قراءةٌ بعد التشغيل لا مدخلٌ فيه."""

        for name, value in self.values:
            if name == column:
                return value
        raise MasaqExperimentError(f"العمودُ «{column}» ليس من المحجوبة الخمسة")

    def as_canonical_content(self) -> dict[str, str]:
        """محتوى الوسوم المحجوبة للبصمة؛ مُجمَّدةٌ وإن حُجِبت."""

        return {name: value for name, value in self.values}


@dataclass(frozen=True, slots=True)
class MasaqSegmentOccurrence:
    """سجلُّ مقطعٍ واحدٍ من MASAQ: موضعُه الأصليُّ، وصورتُه الخامُّ، وتطبيعُها."""

    source_word_no: str
    local_segment_position: int
    raw_segment_surface: str
    normalization: NormalizationTrace
    held_out: HeldOutMASAQAnnotation

    def __post_init__(self) -> None:
        if self.local_segment_position < 0:
            raise MasaqExperimentError("الموضعُ المحلّيُّ عددٌ غيرُ سالب")
        if not isinstance(self.normalization, NormalizationTrace):
            raise MasaqExperimentError("أثرُ التطبيع من نوعه")
        if self.normalization.raw != self.raw_segment_surface:
            raise MasaqExperimentError(
                "مدخلُ أثر التطبيع هو الصورةُ الخامُّ بعينها؛ و"
                + RAW_OCCURRENCE_IS_NOT_NORMALIZED_PROJECTION
            )
        if not isinstance(self.held_out, HeldOutMASAQAnnotation):
            raise MasaqExperimentError("الوسومُ المحجوبةُ من نوعها")

    @property
    def normalized_segment_surface(self) -> str:
        """الصورةُ التي يراها المُولِّد؛ إسقاطٌ مُعلَنٌ لا أصلٌ مُنتحَل."""

        return self.normalization.normalized

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى السجلّ كاملًا للبصمة: الخامُّ والمُطبَّعُ والموضعان والوسوم."""

        return {
            SEGMENT_INDEX_COLUMN: self.source_word_no,
            LOCAL_SEGMENT_POSITION_FIELD: self.local_segment_position,
            "raw_segment_surface": self.raw_segment_surface,
            "normalized_segment_surface": self.normalized_segment_surface,
            "normalization": self.normalization.as_canonical_content(),
            "held_out": self.held_out.as_canonical_content(),
        }


@dataclass(frozen=True, slots=True)
class MasaqWordInput:
    """كلمةٌ مُجمَّدةٌ من MASAQ: موضعُها، وسجلّاتُ مقاطعها بخامِّها ووسومِها المحجوبة."""

    input_id: str
    sura_no: str
    verse_no: str
    word_key: str
    occurrences: tuple[MasaqSegmentOccurrence, ...]

    def __post_init__(self) -> None:
        if not self.input_id.strip():
            raise MasaqExperimentError("مُعرِّفُ الكلمة نصٌّ غير فارغ")
        if not self.occurrences:
            raise MasaqExperimentError("الكلمةُ مقطعٌ واحدٌ فأكثر")
        positions = tuple(
            occurrence.local_segment_position for occurrence in self.occurrences
        )
        if positions != tuple(range(len(self.occurrences))):
            raise MasaqExperimentError(
                "المواضعُ المحلّيّةُ متتابعةٌ من الصفر؛ و"
                + SOURCE_WORD_NO_IS_NOT_DERIVED_LOCAL_POSITION
            )

    @property
    def segments(self) -> tuple[str, ...]:
        """صورُ المقاطع مُطبَّعةً؛ مُشتَقّةٌ من السجلّات لا مكتوبةٌ بدلًا عنها."""

        return tuple(
            occurrence.normalized_segment_surface for occurrence in self.occurrences
        )

    @property
    def raw_segments(self) -> tuple[str, ...]:
        """صورُ المقاطع كما وردت في MASAQ قبل أيِّ تحويل."""

        return tuple(occurrence.raw_segment_surface for occurrence in self.occurrences)

    @property
    def source_word_numbers(self) -> tuple[str, ...]:
        """قيمُ ``Word_No`` الأصليّةُ بأعيانها؛ لا تُعاد صياغتُها."""

        return tuple(occurrence.source_word_no for occurrence in self.occurrences)

    @property
    def local_segment_positions(self) -> tuple[int, ...]:
        """المواضعُ المحلّيّةُ المشتقّة؛ حقلٌ باسمه لا انتحالٌ لاسم المصدر."""

        return tuple(
            occurrence.local_segment_position for occurrence in self.occurrences
        )

    @property
    def held_out_tags(self) -> tuple[str, ...]:
        """وسومُ ``Morph_Tag`` المحجوبة؛ مُشتَقّةٌ من الوسوم الخمسة المُجمَّدة."""

        return tuple(
            occurrence.held_out.value_of(MORPH_TAG_COLUMN)
            for occurrence in self.occurrences
        )

    @property
    def joined_surface(self) -> str:
        """صورةُ الكلمة موصولةً من مقاطعها؛ مرجعُ إعادة البناء لا حكمٌ عليها."""

        return "".join(self.segments)

    def generator_projection(self) -> dict[str, object]:
        """ما يراه المُولِّد: موضعُ الكلمة وصورُ مقاطعها بموضعها الأصليّ، ولا وَسْمَ فيه."""

        return {
            SURA_COLUMN: self.sura_no,
            VERSE_COLUMN: self.verse_no,
            WORD_KEY_COLUMN: self.word_key,
            SEGMENT_INDEX_COLUMN: self.source_word_numbers,
            SEGMENTED_WORD_COLUMN: self.segments,
        }

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الكلمة المُجمَّدةِ كاملًا للبصمة؛ الوَسْمُ مُجمَّدٌ وإن حُجِب."""

        return {
            "input_id": self.input_id,
            SURA_COLUMN: self.sura_no,
            VERSE_COLUMN: self.verse_no,
            WORD_KEY_COLUMN: self.word_key,
            "occurrences": [
                occurrence.as_canonical_content() for occurrence in self.occurrences
            ],
        }

    @property
    def content_id(self) -> str:
        """بصمةُ الكلمة المُجمَّدة؛ مُشتَقّةٌ لا مكتوبة."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


def build_word_inputs(
    records: Sequence[Mapping[str, str]], *, limit: int | None = None
) -> tuple[MasaqWordInput, ...]:
    """اجمع سجلّاتِ MASAQ كلماتٍ مُقطَّعةً بترتيب ورودها؛ ولا تُرتِّب ترجيحًا."""

    order: list[tuple[str, str, str]] = []
    grouped: dict[tuple[str, str, str], list[Mapping[str, str]]] = {}
    for record in records:
        key = (
            record.get(SURA_COLUMN, ""),
            record.get(VERSE_COLUMN, ""),
            record.get(WORD_KEY_COLUMN, ""),
        )
        if key not in grouped:
            grouped[key] = []
            order.append(key)
        grouped[key].append(record)
        if limit is not None and len(order) > limit:
            order.pop()
            del grouped[key]
            break
    words: list[MasaqWordInput] = []
    for key in order:
        rows = grouped[key]
        occurrences = tuple(
            MasaqSegmentOccurrence(
                source_word_no=row.get(SEGMENT_INDEX_COLUMN, ""),
                local_segment_position=position,
                raw_segment_surface=row.get(SEGMENTED_WORD_COLUMN, ""),
                normalization=normalize_segment_surface(
                    row.get(SEGMENTED_WORD_COLUMN, "")
                ),
                held_out=HeldOutMASAQAnnotation.from_record(row),
            )
            for position, row in enumerate(rows)
        )
        if any(not occurrence.normalized_segment_surface for occurrence in occurrences):
            continue
        words.append(
            MasaqWordInput(
                input_id=f"masaq.word.{key[0]}.{key[1]}.{key[2]}",
                sura_no=key[0],
                verse_no=key[1],
                word_key=key[2],
                occurrences=occurrences,
            )
        )
    return tuple(words)


def read_masaq_word_inputs(*, limit: int | None = None) -> tuple[MasaqWordInput, ...]:
    """اقرأ بايتاتِ MASAQ الموثَّقةَ ببصمتها ثمّ اجمعها كلماتٍ مُقطَّعة."""

    return build_word_inputs(masaq_records(read_masaq_bytes()), limit=limit)


def _frozen_specification_ref() -> str:
    return canonical_digest(
        canonical_bytes(
            {
                "scale_space": [SEGMENT_SCALE.scale_id, WORD_SCALE.scale_id],
                "pattern": ACCRETION_PATTERN.pattern_id,
                "operation": ACCRETION_OPERATION,
                "preserved_invariants": list(PRESERVED),
                "closure_contract": [
                    requirement.requirement_id
                    for requirement in SEGMENT_CLOSURE_CONTRACT.requirements
                ],
            }
        )
    )


def build_frozen_binding(
    words: Sequence[MasaqWordInput], *, binding_id: str, source_id: str
) -> FrozenExperimentBinding:
    """اربط التشغيلَ بكلماتٍ مُجمَّدةٍ بأعيانها، وسمِّ المرئيَّ والمحجوب."""

    if not words:
        raise MasaqExperimentError("الرباطُ كلمةٌ مُجمَّدةٌ واحدةٌ فأكثر")
    entries = tuple(
        FrozenInputEntry(
            input_id=word.input_id,
            content_id=word.content_id,
            admission_reason="كلمةٌ مُقطَّعةٌ في مدى التشغيل المُعلَن قبل قراءة شواهده",
        )
        for word in words
    )
    return FrozenExperimentBinding(
        binding_id=binding_id,
        source_id=source_id,
        frozen_specification_ref=_frozen_specification_ref(),
        frozen_input_set_ref=canonical_digest(
            canonical_bytes([entry.content_id for entry in entries])
        ),
        preregistration_content_id=MASAQ_PREREGISTRATION_CONTENT_ID,
        entries=entries,
        generator_visible_fields=GENERATOR_VISIBLE_COLUMNS,
        held_out_readout_fields=HELD_OUT_READOUT_COLUMNS,
    )


def _identity_of(word: MasaqWordInput) -> FractalIdentity:
    return FractalIdentity(
        identity_id=f"identity.{word.input_id}",
        scale_ref=SEGMENT_SCALE_REF,
        identity_criterion_id="criterion.masaq.word_instance",
    )


def _content_of(segments: Sequence[str], upto: int) -> tuple[tuple[str, str], ...]:
    return tuple(
        (f"segment.{position}", segments[position]) for position in range(upto + 1)
    )


def _conformant(
    candidate: ExpansionCandidate, node: FractalNode
) -> PatternConformantDifference:
    decision = PatternConformanceGate.assess(
        candidate=candidate,
        pattern=ACCRETION_PATTERN,
        node=node,
        space=SCALE_SPACE,
    )
    if decision.status is not PatternConformanceStatus.CONFORMANT or (
        decision.conformant is None
    ):
        raise MasaqExperimentError("اقتراحُ الضمّ لم يُطابِق عقدَ نمطه")
    return decision.conformant


@dataclass(frozen=True, slots=True)
class WeakerModelObservation:
    """تشغيلُ النموذج الأضعف على المدخل عينِه، ومقارنتُه بالمهمّة وبمخرج الفركتال."""

    model_id: str
    description: str
    output: str
    fractal_output: str
    task_target: str

    @property
    def ties(self) -> bool:
        """أبلَغ الأضعفُ مخرجَ الفركتال عينَه؟ فإن بلغه امتنعت دعوى التميُّز."""

        return self.output == self.fractal_output

    @property
    def succeeds_at_task(self) -> bool:
        """أبلَغ الأضعفُ غايةَ المهمّة؟ سؤالٌ عن صحّة الطريق لا عن تميُّز غيره."""

        return self.output == self.task_target

    def as_statement(self) -> str:
        """رصدُ النموذج الأضعف نصًّا يدخل الشاهد؛ تسجيلٌ لا حكم."""

        verdict = (
            "بلغ المخرجَ عينَه فلم تثبت دعوى تميُّز الفركتال"
            if self.ties
            else "لم يبلغ المخرجَ عينَه"
        )
        task = "وبلغ غايةَ المهمّة" if self.succeeds_at_task else "ولم يبلغ غايةَ المهمّة"
        return f"{self.description}: {verdict}؛ {task}"


@dataclass(frozen=True, slots=True)
class NegativeControlObservation:
    """ضابطٌ سالبٌ شُغِّل عبر مسار التشغيل عينِه؛ مدخلُه وتحويلُه ومخرجُه مُسجَّلة."""

    control_id: str
    transformation: str
    control_input_content_id: str
    control_input_description: str
    output: str
    reference_output: str
    preregistered_expectation: str

    @property
    def differs(self) -> bool:
        """أخالف مخرجُ الضابط مرجعَه؟"""

        return self.output != self.reference_output

    @property
    def discriminates(self) -> bool:
        """أميَّز الضابطُ فعلًا، أم كان عاجزًا عن التمييز في هذه الحال؟"""

        return self.differs

    def as_statement(self) -> str:
        """رصدُ الضابط نصًّا يدخل الشاهد؛ شاهدُ تشغيلٍ لا مقارنةٌ جانبيّة."""

        verdict = (
            "خالف إعادةَ البناء كما سُجِّل مُسبَقًا"
            if self.differs
            else "لم يُحدِث فرقًا؛ فالضابطُ عاجزٌ عن التمييز هنا"
        )
        return (
            f"{self.control_id} [{self.transformation}] "
            f"على {self.control_input_description} "
            f"(بصمةُ المدخل {self.control_input_content_id}): {verdict}"
        )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الضابط للبصمة؛ مدخلٌ وتحويلٌ ومخرجٌ ومقارنة."""

        return {
            "control_id": self.control_id,
            "transformation": self.transformation,
            "control_input_content_id": self.control_input_content_id,
            "control_input_description": self.control_input_description,
            "output": self.output,
            "reference_output": self.reference_output,
            "preregistered_expectation": self.preregistered_expectation,
            "differs": self.differs,
        }


@dataclass(frozen=True, slots=True)
class StandingEvidence:
    """شروطُ الوقوف المُسجَّلةُ مُسبَقًا، مرصودةً واحدًا واحدًا قبل اشتقاق الحكم."""

    reconstruction_passed: bool
    closure_passed: bool
    negative_controls_behave_as_preregistered: bool
    weaker_model_ties: bool
    blocking_residual_present: bool
    run_failed: bool = False


def derive_standing(evidence: StandingEvidence) -> ExperimentalStanding:
    """اشتقّ وقوفَ دعوى التميُّز من شروطها؛ ولا يكفي الإغلاقُ وإعادةُ البناء لها."""

    if evidence.run_failed:
        return ExperimentalStanding.RUN_FAILURE
    if not evidence.reconstruction_passed:
        return ExperimentalStanding.OBSERVED_REFUTATION
    if (
        not evidence.closure_passed
        or not evidence.negative_controls_behave_as_preregistered
        or evidence.weaker_model_ties
        or evidence.blocking_residual_present
    ):
        return ExperimentalStanding.UNDERPOWERED
    return ExperimentalStanding.OBSERVED_SUPPORT


class ExperimentalTaskOutcome(Enum):
    """حالُ المهمّة نفسِها: أبلغ الجبرُ غايتَه في هذا المدخل أم لا؟"""

    SUCCESS = "success"
    FAILURE = "failure"
    UNRESOLVED = "unresolved"


class ComparativeStanding(Enum):
    """موقعُ الفركتال من النموذج الأضعف؛ محورٌ مستقلٌّ عن نجاح المهمّة."""

    FRACTAL_ONLY = "fractal_only"
    WEAKER_ONLY = "weaker_only"
    BOTH_SUCCEED = "both_succeed"
    BOTH_FAIL = "both_fail"
    NOT_COMPARABLE = "not_comparable"


def derive_task_outcome(
    *, reconstruction_passed: bool, closure_passed: bool, run_failed: bool = False
) -> ExperimentalTaskOutcome:
    """اشتقّ حالَ المهمّة وحدَها؛ ولا يدخل فيه تعادلُ نموذجٍ أضعفَ ولا تميُّزُه."""

    if run_failed:
        return ExperimentalTaskOutcome.UNRESOLVED
    if not reconstruction_passed:
        return ExperimentalTaskOutcome.FAILURE
    if not closure_passed:
        return ExperimentalTaskOutcome.UNRESOLVED
    return ExperimentalTaskOutcome.SUCCESS


def derive_comparative_standing(
    *,
    task_outcome: ExperimentalTaskOutcome,
    fractal_succeeded: bool,
    weaker_model_succeeded: bool | None,
) -> ComparativeStanding:
    """قارِن الطريقين على غاية المهمّة؛ ونجاحُ طريقين صحيحين ليس مشكلة."""

    if (
        task_outcome is ExperimentalTaskOutcome.UNRESOLVED
        or weaker_model_succeeded is None
    ):
        return ComparativeStanding.NOT_COMPARABLE
    if fractal_succeeded and weaker_model_succeeded:
        return ComparativeStanding.BOTH_SUCCEED
    if fractal_succeeded:
        return ComparativeStanding.FRACTAL_ONLY
    if weaker_model_succeeded:
        return ComparativeStanding.WEAKER_ONLY
    return ComparativeStanding.BOTH_FAIL


@dataclass(frozen=True, slots=True)
class MasaqWordReading:
    """قراءةُ كلمةٍ واحدةٍ على محورين: نجاحُ المهمّة، وموقعُها من النموذج الأضعف."""

    input_id: str
    reconstruction_passed: bool
    closure_passed: bool
    task_outcome: ExperimentalTaskOutcome
    weaker_model_succeeded: bool | None
    weaker_model_ties: bool
    comparative_standing: ComparativeStanding
    experimental_standing: ExperimentalStanding
    residuals: tuple[FractalResidual, ...]
    experimental_lift_issued: bool
    negative_controls: tuple[NegativeControlObservation, ...] = ()
    weaker_model_observation: WeakerModelObservation | None = None

    def __post_init__(self) -> None:
        if not self.input_id.strip():
            raise MasaqExperimentError("مُعرِّفُ المدخل في القراءة نصٌّ غير فارغ")

    @property
    def undiscriminating_controls(self) -> tuple[NegativeControlObservation, ...]:
        """الضوابطُ التي لم تُميِّز؛ تُعَدُّ ولا تُطوى."""

        return tuple(
            control for control in self.negative_controls if not control.discriminates
        )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى القراءة للبصمة؛ محوران مُسمّيان لا حكمٌ واحدٌ مُدمَج."""

        return {
            "input_id": self.input_id,
            "reconstruction_passed": self.reconstruction_passed,
            "closure_passed": self.closure_passed,
            "task_outcome": self.task_outcome.value,
            "weaker_model_succeeded": self.weaker_model_succeeded,
            "weaker_model_ties": self.weaker_model_ties,
            "comparative_standing": self.comparative_standing.value,
            "experimental_standing": self.experimental_standing.value,
            "residuals": [
                residual.as_canonical_content() for residual in self.residuals
            ],
            "experimental_lift_issued": self.experimental_lift_issued,
            "negative_controls": [
                control.as_canonical_content() for control in self.negative_controls
            ],
        }


@dataclass(frozen=True, slots=True)
class MasaqExperimentReport:
    """قراءةُ تشغيلٍ تجريبيٍّ واحدٍ على MASAQ؛ شواهدُ وحزمةٌ، بلا ترخيصٍ ولا حكم."""

    experiment_id: str
    run_id: str
    binding: FrozenExperimentBinding
    permit: ExperimentalRunPermit
    final_permit_state: ExperimentalPermitState
    witnesses: tuple[FractalExperimentalWitness, ...]
    experimental_seed_ids: tuple[str, ...]
    bundle: WitnessBundle
    readings: tuple[MasaqWordReading, ...] = ()

    @property
    def standings(self) -> dict[str, int]:
        """عددُ الشواهد بكلِّ وقوف؛ عدٌّ لا ترجيح."""

        counted: dict[str, int] = {
            standing.value: 0 for standing in ExperimentalStanding
        }
        for witness in self.witnesses:
            counted[witness.standing.value] += 1
        return counted

    @property
    def negative_controls(self) -> tuple[NegativeControlObservation, ...]:
        """ضوابطُ التشغيل كلُّها مجموعةً من قراءات كلماته."""

        return tuple(
            control
            for reading in self.readings
            for control in reading.negative_controls
        )

    @property
    def weaker_model_observations(self) -> tuple[WeakerModelObservation, ...]:
        """تشغيلاتُ النموذج الأضعف كلُّها مجموعةً من قراءات كلماته."""

        return tuple(
            reading.weaker_model_observation
            for reading in self.readings
            if reading.weaker_model_observation is not None
        )

    def reading_for(self, input_id: str) -> MasaqWordReading:
        """قراءةُ مدخلٍ بعينه؛ مربوطةٌ بـ``input_id`` لا بترتيبٍ عارض."""

        for reading in self.readings:
            if reading.input_id == input_id:
                return reading
        raise MasaqExperimentError(f"لا قراءةَ للمدخل «{input_id}» في هذا التشغيل")

    @property
    def task_outcomes(self) -> dict[str, int]:
        """عددُ الكلمات بكلِّ حالِ مهمّة؛ محورٌ مستقلٌّ عن دعوى التميُّز."""

        counted: dict[str, int] = {
            outcome.value: 0 for outcome in ExperimentalTaskOutcome
        }
        for reading in self.readings:
            counted[reading.task_outcome.value] += 1
        return counted

    @property
    def comparative_standings(self) -> dict[str, int]:
        """عددُ الكلمات بكلِّ موقعٍ من النموذج الأضعف؛ ونجاحُ الطريقين ليس فشلًا."""

        counted: dict[str, int] = {
            standing.value: 0 for standing in ComparativeStanding
        }
        for reading in self.readings:
            counted[reading.comparative_standing.value] += 1
        return counted

    @property
    def coverage_tally(self) -> dict[str, int]:
        """جدولُ التغطية: المدخلاتُ، وحالُ المهمّة، وموقعُ المقارنة، والضوابطُ العاجزة."""

        tally: dict[str, int] = {"total_inputs": len(self.readings)}
        tally.update(self.task_outcomes)
        tally.update(self.comparative_standings)
        tally["undiscriminating_controls"] = sum(
            len(reading.undiscriminating_controls) for reading in self.readings
        )
        return tally


@dataclass(frozen=True, slots=True)
class _AccretionRun:
    """مخرجُ مسار الضمّ الواحد؛ يسلكه الفرعُ الأصليُّ والضوابطُ السالبةُ سواءً."""

    first_content_id: str
    node: FractalNode
    trace: FractalTrace | None
    adjudication: BranchAdjudicationDecision | None
    readout: str


_TransitionRecorder = Callable[[FractalTransition, FractalTrace], None]
"""تسجيلُ الانتقال في السجلّ التجريبيّ؛ يُمرَّر للفرع الأصليِّ ويُمنَع عن الضوابط."""


def _readout(node: FractalNode) -> str:
    """قراءةُ مخرج العقدة صورةً موصولة؛ عقدُ قراءةٍ واحدٌ للأصل وللضوابط."""

    return "".join(value for _, value in node.content)


def _accrete(
    *,
    subject_id: str,
    segments: Sequence[str],
    identity: FractalIdentity,
    carrier_id: str,
    evidence_ref: str,
    recorder: _TransitionRecorder | None,
) -> _AccretionRun:
    """شغِّل ضمَّ المقاطع بالترتيب عبر بوّاباتها؛ مسارٌ واحدٌ لا مسارٌ للضابط آخر."""

    node = FractalNode.from_seed(
        FractalSeed(
            seed_id=f"seed.{subject_id}",
            identity=identity,
            carrier_id=carrier_id,
            content=_content_of(segments, 0),
        ),
        node_id=f"node.{subject_id}.0",
    )
    first_content_id = node.content_id
    steps: list[FractalTransitionTraceStep] = []
    adjudication: BranchAdjudicationDecision | None = None
    for index in range(1, len(segments)):
        candidate_id = f"accretion.{subject_id}.{index}"
        candidate = ExpansionCandidate(
            candidate_id=candidate_id,
            source=node.as_ref(),
            pattern_ref=PATTERN_REF,
            declared_difference=DeclaredDifference(
                difference_id=f"difference.{candidate_id}",
                dimension="segment_accretion",
                description=f"ضمُّ المقطع رقم {index} إلى محتوى الكلمة",
                preserved_invariants=PRESERVED,
            ),
            proposal_provenance=PROVENANCE,
        )
        movement = IdentityPreservingTransformationCandidate(
            conformant=_conformant(candidate, node),
            carrier_id=carrier_id,
            identity_before=identity,
            identity_after=identity,
            preserved_invariants=PRESERVED,
            output_content=_content_of(segments, index),
        )
        adjudication = BranchAdjudicationGate.adjudicate(
            expansion_set=ExpansionSet(source=node.as_ref(), candidates=(candidate,)),
            assessments=(
                BranchAssessment(
                    candidate_id=candidate_id,
                    standing=BranchStanding.ADMITTED,
                    reason="ضمُّ المقطع التالي مُطابِقٌ لعقد النمط مع حفظ عين الهويّة",
                    residuals=(),
                    movement=movement,
                ),
            ),
            gate_id="gate.adjudication.masaq.segment",
        )
        decision = FractalTransitionGate.open_transition(
            adjudication=adjudication,
            candidate_id=candidate_id,
            source_node=node,
            transition_id=f"transition.{candidate_id}",
            gate_id="gate.transition.masaq.segment",
            evidence_ref=evidence_ref,
            output_node_id=f"node.{subject_id}.{index}",
        )
        steps.append(decision.trace_step)
        if recorder is not None:
            recorder(decision.transition, FractalTrace(steps=tuple(steps)))
        node = decision.output_node
    return _AccretionRun(
        first_content_id=first_content_id,
        node=node,
        trace=FractalTrace(steps=tuple(steps)) if steps else None,
        adjudication=adjudication,
        readout=_readout(node),
    )


def _weaker_model_run(
    segments: Sequence[str], *, fractal_output: str, task_target: str
) -> WeakerModelObservation:
    """شغِّل النموذجَ الأضعف: وصلُ المقاطع نصًّا بلا حركاتٍ فراكتاليّة."""

    return WeakerModelObservation(
        model_id="weaker_model.direct_concatenation",
        description="وصلُ المقاطع نصًّا بلا حركاتٍ فراكتاليّة",
        output="".join(segments),
        fractal_output=fractal_output,
        task_target=task_target,
    )


def _control_input_content_id(segments: Sequence[str]) -> str:
    return canonical_digest(canonical_bytes(list(segments)))


def _negative_controls(
    word: MasaqWordInput,
    *,
    identity: FractalIdentity,
    carrier_id: str,
    evidence_ref: str,
    reference_output: str,
) -> tuple[NegativeControlObservation, ...]:
    """شغِّل الضوابطَ السالبةَ عبر مسار الضمّ عينِه، لا مقارنةً نصّيّةً جانبيّة."""

    controls: list[NegativeControlObservation] = []
    reversed_segments = tuple(reversed(word.segments))
    dropped_segments = word.segments[:-1]
    for suffix, transformation, transformed, description, expectation in (
        (
            "reversed",
            "reversed_order",
            reversed_segments,
            "المقاطعُ معكوسةَ الترتيب",
            "يُتوقَّع أن يُخالف مخرجُه إعادةَ البناء",
        ),
        (
            "dropped",
            "dropped_segment",
            dropped_segments,
            "المقاطعُ بإسقاط آخرها",
            "يُتوقَّع أن يُخالف مخرجُه إعادةَ البناء",
        ),
    ):
        if not transformed:
            continue
        control_run = _accrete(
            subject_id=f"{word.input_id}.control.{suffix}",
            segments=transformed,
            identity=identity,
            carrier_id=carrier_id,
            evidence_ref=evidence_ref,
            recorder=None,
        )
        controls.append(
            NegativeControlObservation(
                control_id=f"control.{word.input_id}.{suffix}",
                transformation=transformation,
                control_input_content_id=_control_input_content_id(transformed),
                control_input_description=description,
                output=control_run.readout,
                reference_output=reference_output,
                preregistered_expectation=expectation,
            )
        )
    return tuple(controls)


def _witness_of_underpowered(
    word: MasaqWordInput, *, permit: ExperimentalRunPermit, entry: FrozenInputEntry
) -> FractalExperimentalWitness:
    node = FractalNode.from_seed(
        FractalSeed(
            seed_id=f"seed.{word.input_id}",
            identity=_identity_of(word),
            carrier_id=f"carrier.{word.input_id}",
            content=_content_of(word.segments, 0),
        ),
        node_id=f"node.{word.input_id}.0",
    )
    return FractalExperimentalWitness(
        witness_id=f"witness.{permit.run_id}.{word.input_id}",
        experiment_id=permit.experiment_id,
        run_id=permit.run_id,
        permit_content_id=permit.content_id,
        frozen_input_content_id=entry.content_id,
        preregistration_content_id=MASAQ_PREREGISTRATION_CONTENT_ID,
        standing=ExperimentalStanding.UNDERPOWERED,
        source_scale=SEGMENT_SCALE_REF,
        identity_before=node.content_id,
        identity_after=node.content_id,
        movement_kind="no_movement_observed",
        observed_difference="كلمةٌ بمقطعٍ واحدٍ لا تعرض ضمًّا يُختبَر",
        reconstruction_observation="لا حركةَ فلا إعادةَ بناءٍ تُقاس",
        closure_observation="لم يُطلَب إغلاقٌ لعدم وقوع حركة",
        preserved_invariants_observed=(),
        weaker_model_observations=("وصلُ النصّ يبلغ الصورةَ عينَها في مقطعٍ واحد",),
        residuals=(
            FractalResidual(
                kind=FractalResidualKind.UNRESOLVED_DIFFERENCE,
                subject_id=word.input_id,
                reason="مقطعٌ واحدٌ لا يعرض فرقَ ضمٍّ عند هذا المقياس",
            ),
        ),
        authority_gaps=(
            NO_LICENSING_AUTHORITY,
            NO_SEMANTIC_AUTHORITY_IN_EXPERIMENT,
        ),
    )


def _run_one_word(
    word: MasaqWordInput,
    *,
    authority: ExperimentalFractalAuthority,
    permit: ExperimentalRunPermit,
    run_id: str,
    binding: FrozenExperimentBinding,
) -> tuple[FractalExperimentalWitness, str | None, MasaqWordReading]:
    entry = binding.entry_for(word.input_id)
    binding.refuse_held_out_fields(word.generator_projection())
    if len(word.segments) < 2:
        witness = _witness_of_underpowered(word, permit=permit, entry=entry)
        return (
            witness,
            None,
            MasaqWordReading(
                input_id=word.input_id,
                reconstruction_passed=False,
                closure_passed=False,
                task_outcome=ExperimentalTaskOutcome.UNRESOLVED,
                weaker_model_succeeded=None,
                weaker_model_ties=False,
                comparative_standing=ComparativeStanding.NOT_COMPARABLE,
                experimental_standing=witness.standing,
                residuals=witness.residuals,
                experimental_lift_issued=False,
            ),
        )

    identity = _identity_of(word)
    carrier_id = f"carrier.{word.input_id}"

    def recorder(transition: FractalTransition, trace: FractalTrace) -> None:
        ExperimentalTransitionGate.record(
            authority=authority,
            permit=permit,
            run_id=run_id,
            binding=binding,
            frozen_input=entry,
            operation=ACCRETION_OPERATION,
            transition=transition,
            trace=trace,
            open_authority_gaps=(NO_LICENSING_AUTHORITY,),
        )

    accretion = _accrete(
        subject_id=word.input_id,
        segments=word.segments,
        identity=identity,
        carrier_id=carrier_id,
        evidence_ref=entry.content_id,
        recorder=recorder,
    )
    node = accretion.node
    trace = accretion.trace
    assert trace is not None
    assert accretion.adjudication is not None
    closure = ClosureGate.assess(
        candidate=ClosureCandidate(
            node=node,
            trace=trace,
            adjudication=accretion.adjudication,
            branch_transitions=(trace.steps[-1],),
            contract=SEGMENT_CLOSURE_CONTRACT,
            coverage=(
                ClosureRequirement(
                    requirement_id="MRK.masaq.segment.identity",
                    satisfied_by_content_id=node.identity.content_id,
                    reason="هويّةُ العقدة مُحَلّةٌ في فضاء المقاييس بعقدها",
                ),
                ClosureRequirement(
                    requirement_id="MRK.masaq.segment.trace",
                    satisfied_by_content_id=trace.output_content_id,
                    reason="الأثرُ ينتهي إلى هذه العقدة ببصمتها",
                ),
                ClosureRequirement(
                    requirement_id="MRK.masaq.segment.branches",
                    satisfied_by_content_id=accretion.first_content_id,
                    reason="سجلُّ الفروع تامٌّ بأحكامه وبقاياه",
                ),
            ),
            invariant_audit=InvariantAudit(
                audited_invariants=PRESERVED,
                passed=True,
                reason="ثوابتُ النمط مُدقَّقةٌ على مخرج آخر حركة",
            ),
            residuals=(
                FractalResidual(
                    kind=FractalResidualKind.UNRESOLVED_DIFFERENCE,
                    subject_id=word.input_id,
                    reason=UNRESOLVED_SCALE_NECESSITY_REASON,
                ),
            ),
        ),
        gate_id="gate.closure.masaq.segment",
    )
    reconstructed = accretion.readout == word.joined_surface
    weaker = _weaker_model_run(
        word.segments,
        fractal_output=accretion.readout,
        task_target=word.joined_surface,
    )
    controls = _negative_controls(
        word,
        identity=identity,
        carrier_id=carrier_id,
        evidence_ref=entry.content_id,
        reference_output=accretion.readout,
    )
    closed_node = closure.closed
    seed_id: str | None = None
    if closed_node is not None:
        lift_permit = issue_experimental_lift_permit(
            authority=authority,
            permit=permit,
            run_id=run_id,
            source_scale_ref=SEGMENT_SCALE_REF,
            target_scale_ref=WORD_SCALE_REF,
            necessity_claim_under_test=(
                "يُدَّعى أنّ بلوغَ وحدة الكلمة يقتضي مقياسًا أعلى من المقطع"
            ),
        )
        lift = ExperimentalLiftGate.assess(
            authority=authority,
            permit=permit,
            run_id=run_id,
            candidate=ExperimentalLiftCandidate(
                closed_node=closed_node,
                lift_permit=lift_permit,
                carried_residuals=(),
            ),
            seed_id=f"experimental-seed.{run_id}.{word.input_id}",
        )
        if (
            lift.status is ExperimentalLiftStatus.EXPERIMENTAL_SEED_ISSUED
            and lift.experimental_seed is not None
        ):
            seed_id = lift.experimental_seed.seed_id
    base_residuals = closure.residuals if closed_node is None else closed_node.residuals
    residuals = tuple(base_residuals)
    if weaker.ties:
        residuals += (
            FractalResidual(
                kind=FractalResidualKind.UNRESOLVED_DIFFERENCE,
                subject_id=word.input_id,
                reason=(
                    f"{WEAKER_MODEL_TIES_FRACTAL_MODEL}: "
                    + WEAKER_MODEL_TIE_BLOCKS_DISTINCTIVE_STRUCTURAL_SUPPORT
                ),
            ),
        )
    standing = derive_standing(
        StandingEvidence(
            reconstruction_passed=reconstructed,
            closure_passed=closed_node is not None,
            negative_controls_behave_as_preregistered=bool(controls)
            and all(control.discriminates for control in controls),
            weaker_model_ties=weaker.ties,
            blocking_residual_present=any(residual.blocking for residual in residuals),
        )
    )
    witness = FractalExperimentalWitness(
        witness_id=f"witness.{run_id}.{word.input_id}",
        experiment_id=permit.experiment_id,
        run_id=run_id,
        permit_content_id=permit.content_id,
        frozen_input_content_id=entry.content_id,
        preregistration_content_id=MASAQ_PREREGISTRATION_CONTENT_ID,
        standing=standing,
        source_scale=SEGMENT_SCALE_REF,
        pattern_ref=PATTERN_REF,
        target_scale=WORD_SCALE_REF if seed_id is not None else None,
        identity_before=accretion.first_content_id,
        identity_after=node.content_id,
        movement_kind="identity_preserving_transformation",
        observed_difference=f"ضُمَّ {len(word.segments) - 1} مقطعًا بحركاتٍ متتابعة",
        reconstruction_observation=(
            "إعادةُ البناء من مخرج الحركات طابقت الصورةَ المُجمَّدة"
            if reconstructed
            else "إعادةُ البناء خالفت الصورةَ المُجمَّدة"
        ),
        closure_observation=(
            f"حالُ الإغلاق عند مقياس المقطع: {closure.status.value}"
            + (
                "؛ والرفعُ التجريبيُّ وقع لاختبار ضرورة مقياس الكلمة لا لإثباتها"
                if seed_id is not None
                else ""
            )
        ),
        preserved_invariants_observed=PRESERVED,
        weaker_model_observations=(weaker.as_statement(),),
        negative_control_observations=tuple(
            control.as_statement() for control in controls
        ),
        counterexample_observations=(
            () if reconstructed else (f"كلمةٌ خالفت إعادةُ بناؤها: {word.input_id}",)
        ),
        residuals=residuals,
        authority_gaps=(
            NO_LICENSING_AUTHORITY,
            NO_SEMANTIC_AUTHORITY_IN_EXPERIMENT,
            NO_SCALE_NECESSITY_CERTIFICATION_IN_EXPERIMENT,
        ),
        trace=trace,
    )
    task_outcome = derive_task_outcome(
        reconstruction_passed=reconstructed,
        closure_passed=closed_node is not None,
    )
    reading = MasaqWordReading(
        input_id=word.input_id,
        reconstruction_passed=reconstructed,
        closure_passed=closed_node is not None,
        task_outcome=task_outcome,
        weaker_model_succeeded=weaker.succeeds_at_task,
        weaker_model_ties=weaker.ties,
        comparative_standing=derive_comparative_standing(
            task_outcome=task_outcome,
            fractal_succeeded=reconstructed,
            weaker_model_succeeded=weaker.succeeds_at_task,
        ),
        experimental_standing=standing,
        residuals=residuals,
        experimental_lift_issued=seed_id is not None,
        negative_controls=controls,
        weaker_model_observation=weaker,
    )
    return witness, seed_id, reading


def run_masaq_fractal_experiment(
    words: Sequence[MasaqWordInput],
    *,
    run_id: str,
    binding_id: str = "binding.masaq.segment_accretion",
    source_id: str = "corpus.masaq",
    bundle_id: str = "bundle.masaq.segment_accretion",
) -> MasaqExperimentReport:
    """شغِّل الفركتال على كلماتٍ مُجمَّدةٍ تحت إذنٍ مؤقّت، ثمّ اسحب الإذن."""

    binding = build_frozen_binding(words, binding_id=binding_id, source_id=source_id)
    authority = ExperimentalFractalAuthority(
        authority_id="authority.masaq.experimental"
    )
    permit = authority.issue(
        binding=binding,
        experiment_id=MASAQ_EXPERIMENT_ID,
        run_id=run_id,
        permitted_patterns=(PATTERN_REF,),
        permitted_operations=(ACCRETION_OPERATION,),
        permitted_source_scales=(SEGMENT_SCALE_REF,),
        permitted_target_scales=(SEGMENT_SCALE_REF, WORD_SCALE_REF),
        permitted_branch_birth=False,
        permitted_experimental_lift=True,
        authority_scope="تشغيلٌ تجريبيٌّ على صور MASAQ المُقطَّعة؛ لا ترخيصَ فيه",
    )
    permit = authority.activate(permit)
    witnesses: list[FractalExperimentalWitness] = []
    seed_ids: list[str] = []
    readings: list[MasaqWordReading] = []
    for word in words:
        try:
            witness, seed_id, reading = _run_one_word(
                word,
                authority=authority,
                permit=permit,
                run_id=run_id,
                binding=binding,
            )
        except (ValueError, KeyError, IndexError) as error:
            witness = FractalExperimentalWitness(
                witness_id=f"witness.{run_id}.{word.input_id}",
                experiment_id=MASAQ_EXPERIMENT_ID,
                run_id=run_id,
                permit_content_id=permit.content_id,
                frozen_input_content_id=word.content_id,
                preregistration_content_id=MASAQ_PREREGISTRATION_CONTENT_ID,
                standing=ExperimentalStanding.RUN_FAILURE,
                source_scale=SEGMENT_SCALE_REF,
                identity_before=word.content_id,
                identity_after=word.content_id,
                movement_kind="no_movement_observed",
                observed_difference="أخفق التشغيلُ قبل بلوغ حركةٍ تامّة",
                reconstruction_observation="لا إعادةَ بناءٍ لإخفاق التشغيل",
                closure_observation=f"إخفاقُ تشغيل: {type(error).__name__}",
                residuals=(
                    FractalResidual(
                        kind=FractalResidualKind.UNRESOLVED_DIFFERENCE,
                        subject_id=word.input_id,
                        reason="أخفق التشغيلُ ولم تُحسَم حركتُه",
                        blocking=True,
                    ),
                ),
                authority_gaps=(NO_LICENSING_AUTHORITY,),
            )
            seed_id = None
            reading = MasaqWordReading(
                input_id=word.input_id,
                reconstruction_passed=False,
                closure_passed=False,
                task_outcome=derive_task_outcome(
                    reconstruction_passed=False,
                    closure_passed=False,
                    run_failed=True,
                ),
                weaker_model_succeeded=None,
                weaker_model_ties=False,
                comparative_standing=ComparativeStanding.NOT_COMPARABLE,
                experimental_standing=witness.standing,
                residuals=witness.residuals,
                experimental_lift_issued=False,
            )
        readings.append(reading)
        witnesses.append(witness)
        if seed_id is not None:
            seed_ids.append(seed_id)
    bundle = WitnessBundle(
        bundle_id=bundle_id,
        target_claim_ref=str(MASAQ_PREREGISTRATION["target_claim"]),
        preregistration_ref=MASAQ_PREREGISTRATION_CONTENT_ID,
        witnesses=tuple(witnesses),
        input_coverage=tuple(word.input_id for word in words),
        open_authority_gaps=(NO_SUFFICIENCY_ASSESSMENT_AUTHORITY,),
    )
    revoked = authority.revoke(permit)
    return MasaqExperimentReport(
        experiment_id=MASAQ_EXPERIMENT_ID,
        run_id=run_id,
        binding=binding,
        permit=revoked,
        final_permit_state=authority.state_of(revoked),
        witnesses=tuple(witnesses),
        experimental_seed_ids=tuple(seed_ids),
        bundle=bundle,
        readings=tuple(readings),
    )
