"""`G0.SDAL-0.LAWS`: قوانينُ جبرِ `StructuralDal` عند `zero-one`، مُجمَّدةً قبل القياس.

هذه الطبقةُ أسبقُ من كلِّ دعوى لغويّة: لا جذرَ، ولا وزنَ، ولا زيادةَ، ولا معنى،
ولا معجم. خاناتٌ مُصطنَعةٌ وحدَها تُبنى عليها صحّةُ عملياتها، ودعوى هذه الطبقة
مخفوضةٌ إلى غايتها:

    StructuralOperatorProof  →  EligibleForFiberIntegration

فليس في هذا الطور إسقاطٌ على لسانٍ بعينه، ولا ترشيحُ أصلٍ، ولا سلطةُ مقارنةٍ
بين نظامين. وأهليّةُ الاندماج في ليفٍ لاحقٍ ليست اندماجًا، ولا تُصدَّق عملياتُ
هذه الطبقة نفسَها.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from alghanem.canonical_content import canonical_bytes, canonical_digest

__all__ = [
    "A_NEW_ANCHOR_REQUIRES_PROVENANCE",
    "NO_BRANCH_BIRTH_WITHOUT_EXTERNAL_CERTIFICATE",
    "NO_IMPLICIT_IDENTITY_MODE",
    "NO_POSITIVE_STRUCTURE_FROM_NEUTRAL_INPUT",
    "SELF_DEFINED_CONTRACT_DOES_NOT_ESTABLISH_COMPARATIVE_STRENGTH",
    "STRUCTURAL_OPERATOR_PROOF_IS_ONLY_ELIGIBLE_FOR_FIBER_INTEGRATION",
    "THE_PART_HAS_ITS_OWN_IDENTITY",
    "UNPROVED_ROLE_BASIS_IS_BLOCKING",
    "BLOCKING_RESIDUAL_FORBIDS_POSITIVE_PROMOTION",
    "NO_EXPECTED_COUNT_IS_FROZEN",
    "NO_FORCED_WINNER_AMONG_SHAPE_PARTITIONS",
    "NO_LINGUISTIC_VOCABULARY_IN_THE_ZERO_ONE_ALGEBRA",
    "NO_SILENT_DROPPED_SLOT",
    "PREREGISTRATION_DIGEST",
    "SHAPE_PARTITION_HYPOTHESIS_IS_NOT_AN_UTTERANCE_BENEFIT_CANDIDATE",
    "SHAPE_PARTITION_HYPOTHESIS_IS_NOT_A_ROOT_CANDIDATE",
    "SHAPE_PARTITION_HYPOTHESIS_IS_NOT_A_SIGNIFIED_CANDIDATE",
    "SHAPE_PARTITION_HYPOTHESIS_IS_NOT_A_WEIGHT_CANDIDATE",
    "STRUCTURAL_ACCEPTANCE_CONDITIONS",
    "STRUCTURAL_BASE_CASE_IS_NOT_A_LINGUISTIC_ROOT_PROOF",
    "STRUCTURAL_DAL_LAWS",
    "STRUCTURAL_PART_IS_NOT_A_SUBSTRING",
    "STRUCTURAL_TRANSITION_CONTRACT_FIELDS",
    "THE_PART_KEEPS_ITS_PARENT_ANCHOR",
    "THE_TRACE_IS_CUMULATIVE_NOT_RECONSTRUCTED",
    "ZERO_ONE_BOUND",
    "AcceptanceItem",
    "OutputContractComponent",
    "Scale",
    "StructuralAcceptanceCondition",
    "StructuralDalError",
    "condition_named",
    "preregistration_digest",
]


class StructuralDalError(ValueError):
    """رفضٌ بنيويٌّ مُسمًّى في جبر `StructuralDal`."""


ZERO_ONE_BOUND: Final[int] = 2
"""حدُّ هذا الطور: خانةٌ واحدةٌ ثمّ خانتان؛ وما فوقَه سلطةٌ لم تُفتَح."""


class Scale(Enum):
    """مقياسا هذا الطور؛ مفردةٌ مغلقةٌ لا عددٌ حرّ."""

    ZERO = "zero"
    ONE = "one"

    @property
    def slot_count(self) -> int:
        """عددُ الخانات عند المقياس؛ مُشتَقٌّ لا مكتوب."""

        return 1 if self is Scale.ZERO else 2


class OutputContractComponent(Enum):
    """مُركّباتُ عقدِ المخرج؛ المقارنةُ تقع عليها لا على نصِّ المخرج."""

    WHOLE_RECONSTRUCTION = "whole_reconstruction"
    TYPED_SLOT_PARTITION = "typed_slot_partition"
    PART_WHOLE_IDENTITY = "part_whole_identity"
    EXPLICIT_RESIDUALS = "explicit_residuals"
    TRACE_COMPLETENESS = "trace_completeness"


class AcceptanceItem(Enum):
    """بنودُ القبول المطلوبةُ من هذا التشغيل بأعيانها؛ ولا عددَ لها مُجمَّد."""

    ZERO_RECONSTRUCTS_EXACTLY = "zero_reconstructs_exactly"
    ZERO_ASSIGNS_NO_POSITIVE_ROLE = "zero_assigns_no_positive_role"
    ONE_PRODUCES_MULTIPLE_HYPOTHESES = "one_produces_multiple_hypotheses"
    NO_SLOT_SILENTLY_DROPPED = "no_slot_silently_dropped"
    PART_IDENTITY_IS_DISTINCT_FROM_LINEAGE = "part_identity_is_distinct_from_lineage"
    SAME_ENTITY_RESCALING_PRESERVES_IDENTITY = (
        "same_entity_rescaling_preserves_identity"
    )
    BRANCH_BIRTH_IS_UNAVAILABLE_HERE = "branch_birth_is_unavailable_here"
    UNPROVED_ROLE_BASIS_BLOCKS_PROMOTION = "unproved_role_basis_blocks_promotion"
    BLOCKING_RESIDUAL_PREVENTS_PROMOTION = "blocking_residual_prevents_promotion"
    TRACE_IS_CUMULATIVE = "trace_is_cumulative"
    LAYER_IS_STRUCTURALLY_ISOLATED = "layer_is_structurally_isolated"
    NO_LINGUISTIC_CLAIM_IN_OUTPUT = "no_linguistic_claim_in_output"


STRUCTURAL_BASE_CASE_IS_NOT_A_LINGUISTIC_ROOT_PROOF: Final[str] = (
    "StructuralBaseCase != LinguisticRootProof: أصغرُ كلٍّ مكتملٍ يثبت إعادةَ البناء "
    "وحفظَ الهويّة، ولا يمنح الخانةَ صفةَ أصلٍ لغويٍّ ولا سلطةً صرفيّة."
)

SHAPE_PARTITION_HYPOTHESIS_IS_NOT_A_ROOT_CANDIDATE: Final[str] = (
    "ShapePartitionHypothesis != RootCandidate: فرضيّةُ التقسيم صورةٌ بنيويّةٌ "
    "مُصرَّحة، لا دعوى أصلٍ ولا ترشيحَ جذر."
)

SHAPE_PARTITION_HYPOTHESIS_IS_NOT_A_WEIGHT_CANDIDATE: Final[str] = (
    "ShapePartitionHypothesis != WeightCandidate: توزيعُ الأدوار على الخانات "
    "لا يُنشئ وزنًا ولا يستمدّ منه سلطة."
)

SHAPE_PARTITION_HYPOTHESIS_IS_NOT_A_SIGNIFIED_CANDIDATE: Final[str] = (
    "ShapePartitionHypothesis != MadlulCandidate: توزيعُ الأدوار على الخانات "
    "صورةٌ بنيويّةٌ لا مدلولَ لها، ولا يُقرَأ منه معنًى ولا مرجعٌ ولا إشارة."
)

SHAPE_PARTITION_HYPOTHESIS_IS_NOT_AN_UTTERANCE_BENEFIT_CANDIDATE: Final[str] = (
    "ShapePartitionHypothesis != IfadaCandidate: الفرضيّةُ لا تُفيد ولا تُسنِد "
    "ولا تبلغ تركيبًا؛ ولا تُشتَقُّ إفادةٌ من هذا الجبر ولا يُحتَجُّ به عليها."
)

NO_FORCED_WINNER_AMONG_SHAPE_PARTITIONS: Final[str] = (
    "لا يُرفَع تقسيمٌ على أقرانه ابتداءً؛ ومجموعةُ الفرضيّات تُعرَض بلا ترتيبِ "
    "تفضيلٍ ولا فائزٍ مفروض."
)

NO_SILENT_DROPPED_SLOT: Final[str] = (
    "لا خانةَ تسقط صامتةً: كلُّ خانةٍ في الكلّ تقع في جزءٍ واحدٍ بدورٍ مُسمًّى، "
    "ولا فائضَ ولا تكرار."
)

STRUCTURAL_PART_IS_NOT_A_SUBSTRING: Final[str] = (
    "StructuralPart != Substring: الجزءُ إسقاطٌ مرتّبٌ على خاناتٍ قد تكون "
    "متباعدة، لا مقطعٌ متّصلٌ من نصّ."
)

THE_PART_KEEPS_ITS_PARENT_ANCHOR: Final[str] = (
    "PartAtScaleN -> WholeAtScaleNPlus1: إذا صار الجزءُ كلًّا في المقياس التالي "
    "فلا يفقد نسبَه، و`child.parent_anchor_id == parent.anchor_id`."
)

A_NEW_ANCHOR_REQUIRES_PROVENANCE: Final[str] = (
    "لا تُنشَأ مِرساةٌ جديدةٌ منفصلةٌ بلا نسب؛ وكلُّ كلٍّ مُرقًّى يحمل مصدرَه " "ومِرساةَ أبيه."
)

BLOCKING_RESIDUAL_FORBIDS_POSITIVE_PROMOTION: Final[str] = (
    "BlockingResidual -> NoPositivePromotion: قد تُعيد البنيةُ بناءَ نفسها مع "
    "بقيّةٍ حاجبة، ولا يجوز لها الانتقالُ إلى رتبةٍ أعلى."
)

THE_TRACE_IS_CUMULATIVE_NOT_RECONSTRUCTED: Final[str] = (
    "أثرُ المخرج يمتدُّ على أثر المدخل بعينه خطوةً واحدةً زائدة؛ ولا يُعاد بناؤه "
    "بعد وقوع الانتقال."
)

NO_LINGUISTIC_VOCABULARY_IN_THE_ZERO_ONE_ALGEBRA: Final[str] = (
    "مفرداتُ هذه الطبقة بنيويّةٌ محضة؛ فلا اسمَ نوعٍ ولا حقلَ ولا عضوَ مفردةٍ "
    "يحمل جذرًا ولا وزنًا ولا معنًى ولا معجمًا ولا انتسابًا إلى لسانٍ بعينه."
)

NO_EXPECTED_COUNT_IS_FROZEN: Final[str] = (
    "لا عددَ متوقَّعٌ يُجمَّد قبل التشغيل؛ والأعدادُ تُشتَقُّ من البنية وقتَ " "القياس ولا تُكتَب يدًا."
)

NO_POSITIVE_STRUCTURE_FROM_NEUTRAL_INPUT: Final[str] = (
    "NeutralFiberInput ↛ PositiveStructuralRole: المدخلُ المحايد لا يُنتِج دورًا "
    "إيجابيًّا من نفسه؛ فحالةُ الابتداء غيرُ مُسنَدةٍ بالتصريح، ولا تُقلَب أساسًا "
    "بمجرّد كونها الخانةَ الوحيدة."
)

UNPROVED_ROLE_BASIS_IS_BLOCKING: Final[str] = (
    "UnprovedRoleBasis -> BlockingResidual: إسنادُ دورٍ إيجابيٍّ بلا مُرجِّحٍ "
    "مُبرهنٍ بقيّةٌ حاجبةٌ لا مُلاحظةٌ جانبيّة؛ ولا ترقيةَ حتّى يأتي الدليلُ من "
    "سلطةٍ خارج هذه الطبقة."
)

THE_PART_HAS_ITS_OWN_IDENTITY: Final[str] = (
    "LineagePreservation != PartIdentityPreservation: للجزء مِرساتُه الخاصّة، "
    "و`parent_anchor_id` نسبٌ لا هويّة؛ فمن جعل النسبَ هويّةً أسقط الجزءَ في أبيه."
)

NO_IMPLICIT_IDENTITY_MODE: Final[str] = (
    "NoImplicitIdentityMode: نمطُ انتقال الهويّة مُصرَّحٌ في كلِّ انتقال، ولا "
    "افتراضَ بين `SameEntityRescaling` و`CertifiedBranchBirth`؛ وعدمُ التصريح رفضٌ."
)

NO_BRANCH_BIRTH_WITHOUT_EXTERNAL_CERTIFICATE: Final[str] = (
    "NoBranchBirthWithoutExternalCertificate: لا تُصدِر هذه الطبقةُ لنفسها شهادةَ "
    "ولادةِ فرعٍ ولا رخصتَه؛ ومسارُ `CertifiedBranchBirth` مُسمًّى مؤجَّلٌ حتّى "
    "تقوم سلطةٌ خارجيّةٌ تُصدِر شهادتَه."
)

SELF_DEFINED_CONTRACT_DOES_NOT_ESTABLISH_COMPARATIVE_STRENGTH: Final[str] = (
    "SelfDefinedContract ⇏ ComparativeStrength: عقدُ المخرج هنا مُعرَّفٌ من هذه "
    "الطبقة نفسِها، فقراءتُه وصفٌ داخلَ عقدِها لا حكمَ قوّةٍ على نموذجٍ آخر؛ "
    "والمقارنةُ الحقيقيّةُ تأتي من عقدٍ محايدٍ لا يملك أيُّ نظامٍ تعريفَه."
)

STRUCTURAL_OPERATOR_PROOF_IS_ONLY_ELIGIBLE_FOR_FIBER_INTEGRATION: Final[str] = (
    "StructuralOperatorProof -> EligibleForFiberIntegration: غايةُ هذا الطور "
    "أهليّةُ عملياته للاندماج في ليفٍ لاحق، لا إسقاطٌ على لسانٍ بعينه ولا ترشيحُ "
    "أصلٍ ولا سلطةُ مقارنة."
)

STRUCTURAL_DAL_LAWS: Final[tuple[str, ...]] = (
    STRUCTURAL_BASE_CASE_IS_NOT_A_LINGUISTIC_ROOT_PROOF,
    SHAPE_PARTITION_HYPOTHESIS_IS_NOT_A_ROOT_CANDIDATE,
    SHAPE_PARTITION_HYPOTHESIS_IS_NOT_A_WEIGHT_CANDIDATE,
    SHAPE_PARTITION_HYPOTHESIS_IS_NOT_A_SIGNIFIED_CANDIDATE,
    SHAPE_PARTITION_HYPOTHESIS_IS_NOT_AN_UTTERANCE_BENEFIT_CANDIDATE,
    NO_FORCED_WINNER_AMONG_SHAPE_PARTITIONS,
    NO_SILENT_DROPPED_SLOT,
    STRUCTURAL_PART_IS_NOT_A_SUBSTRING,
    THE_PART_KEEPS_ITS_PARENT_ANCHOR,
    A_NEW_ANCHOR_REQUIRES_PROVENANCE,
    BLOCKING_RESIDUAL_FORBIDS_POSITIVE_PROMOTION,
    THE_TRACE_IS_CUMULATIVE_NOT_RECONSTRUCTED,
    NO_LINGUISTIC_VOCABULARY_IN_THE_ZERO_ONE_ALGEBRA,
    NO_EXPECTED_COUNT_IS_FROZEN,
    NO_POSITIVE_STRUCTURE_FROM_NEUTRAL_INPUT,
    UNPROVED_ROLE_BASIS_IS_BLOCKING,
    THE_PART_HAS_ITS_OWN_IDENTITY,
    NO_IMPLICIT_IDENTITY_MODE,
    NO_BRANCH_BIRTH_WITHOUT_EXTERNAL_CERTIFICATE,
    SELF_DEFINED_CONTRACT_DOES_NOT_ESTABLISH_COMPARATIVE_STRENGTH,
    STRUCTURAL_OPERATOR_PROOF_IS_ONLY_ELIGIBLE_FOR_FIBER_INTEGRATION,
)

STRUCTURAL_TRANSITION_CONTRACT_FIELDS: Final[tuple[str, ...]] = (
    "input_identity",
    "difference",
    "invariant",
    "gate",
    "output_identity",
    "residual",
    "trace",
)
"""حقولُ عقد الانتقال السبعة:

    StructuralTransition =
        <Input, Difference, Invariant, Gate, Output, Residual, Trace>
"""


@dataclass(frozen=True, slots=True)
class StructuralAcceptanceCondition:
    """شرطُ قبولٍ مُسمًّى: ما يُقاس، وما لا يُعَدُّ قياسًا له."""

    condition_id: str
    statement: str
    disqualifier: str

    def __post_init__(self) -> None:
        for name, value in (
            ("مُعرِّفُ الشرط", self.condition_id),
            ("نصُّ الشرط", self.statement),
            ("مُبطِلُ الشرط", self.disqualifier),
        ):
            if not isinstance(value, str) or not value.strip():
                raise StructuralDalError(f"{name} نصٌّ غيرُ فارغ")

    def as_canonical_content(self) -> dict[str, str]:
        """محتوى الشرط للبصمة."""

        return {
            "condition_id": self.condition_id,
            "statement": self.statement,
            "disqualifier": self.disqualifier,
        }


STRUCTURAL_ACCEPTANCE_CONDITIONS: Final[tuple[StructuralAcceptanceCondition, ...]] = (
    StructuralAcceptanceCondition(
        condition_id="SDAL0.EXACT_RECONSTRUCTION",
        statement="إعادةُ بناء الكلّ من أجزائه تُطابق الكلَّ خانةً خانة",
        disqualifier="تطابقُ نصٍّ مسطّحٍ دون تطابق الخانات ليس إعادةَ بناء",
    ),
    StructuralAcceptanceCondition(
        condition_id="SDAL0.COMPLETE_SLOT_COVERAGE",
        statement="كلُّ خانةٍ مُغطّاةٌ مرّةً واحدةً بالضبط",
        disqualifier="بقيّةٌ تبتلع الخاناتِ غيرَ المُصنَّفة ليست تغطية",
    ),
    StructuralAcceptanceCondition(
        condition_id="SDAL0.IDENTITY_PRESERVATION",
        statement="مِرساةُ الكلّ باقيةٌ عبر الصعود، ومِرساةُ أبٍ محفوظةٌ عبر الترقية",
        disqualifier="مِرساةٌ جديدةٌ بلا نسبٍ ليست حفظًا للهويّة",
    ),
    StructuralAcceptanceCondition(
        condition_id="SDAL0.TRACE_PRESERVATION",
        statement="أثرُ المخرج يمتدُّ على أثر المدخل بعينه",
        disqualifier="أثرٌ يُعاد بناؤه بعد الانتقال ليس أثرًا تراكميًّا",
    ),
    StructuralAcceptanceCondition(
        condition_id="SDAL0.NO_FORCED_WINNER",
        statement="مجموعةُ الفرضيّات تُعرَض كاملةً بلا ترجيح",
        disqualifier="ترتيبٌ أو درجةٌ أو اختيارٌ واحدٌ يُبطِل الشرط",
    ),
    StructuralAcceptanceCondition(
        condition_id="SDAL0.CLASSIFIED_RESIDUALS",
        statement="كلُّ بقيّةٍ مُسمّاةٌ ومُصنَّفةٌ حاجبةً أو غيرَ حاجبة",
        disqualifier="بقيّةٌ بلا تصنيفٍ تجعل كلَّ اختبارٍ ناجحًا",
    ),
    StructuralAcceptanceCondition(
        condition_id="SDAL0.BLOCKED_PROMOTION",
        statement="بقيّةٌ حاجبةٌ تمنع الترقيةَ ولو صحّت إعادةُ البناء",
        disqualifier="ترقيةٌ تقع مع بقيّةٍ حاجبةٍ تُبطِل القانون",
    ),
    StructuralAcceptanceCondition(
        condition_id="SDAL0.STRUCTURAL_ISOLATION",
        statement="الحزمةُ لا تستورد لسانًا ولا معجمًا ولا سلطةَ نواة",
        disqualifier="استيرادٌ غيرُ مباشرٍ يُبطِل العزلَ كالمباشر",
    ),
    StructuralAcceptanceCondition(
        condition_id="SDAL0.NO_LINGUISTIC_CLAIM",
        statement="مفرداتُ المخرج بنيويّةٌ لا لغويّة",
        disqualifier="اسمُ حقلٍ أو عضوِ مفردةٍ لغويٌّ يُبطِل الشرط",
    ),
    StructuralAcceptanceCondition(
        condition_id="SDAL0.NEUTRAL_START",
        statement="حالةُ الابتداء غيرُ مُسنَدةٍ بالتصريح، ولا دورَ إيجابيَّ فيها",
        disqualifier="منحُ الخانة الوحيدة دورَ الأساس تلقائيًّا يُبطِل الحياد",
    ),
    StructuralAcceptanceCondition(
        condition_id="SDAL0.UNPROVED_ROLE_BASIS_BLOCKS",
        statement="أساسُ الدور غيرُ المُبرهن بقيّةٌ حاجبةٌ تمنع الترقية",
        disqualifier="تسجيلُ عدم البرهان بقيّةً غيرَ حاجبةٍ يُجيز الترقيةَ بلا دليل",
    ),
    StructuralAcceptanceCondition(
        condition_id="SDAL0.PART_IDENTITY",
        statement="للجزء مِرساتُه الخاصّةُ المتميّزةُ عن مِرساة أبيه",
        disqualifier="حفظُ النسب وحدَه ليس حفظًا لهويّة الجزء",
    ),
    StructuralAcceptanceCondition(
        condition_id="SDAL0.EXPLICIT_IDENTITY_MODE",
        statement="نمطُ انتقال الهويّة مُصرَّحٌ، والمفتوحُ منه هنا إعادةُ المقياس وحدَها",
        disqualifier="نمطٌ ضمنيٌّ أو شهادةُ ولادةٍ تُصدِرها الطبقةُ لنفسها يُبطِل الشرط",
    ),
    StructuralAcceptanceCondition(
        condition_id="SDAL0.NO_SELF_DEFINED_STRENGTH",
        statement="قراءةُ عقد المخرج وصفٌ داخلَ عقدِ هذه الطبقة لا حكمُ قوّة",
        disqualifier="قراءةُ تفوّقٍ على نموذجٍ آخر من عقدٍ عرّفته الطبقةُ نفسُها",
    ),
    StructuralAcceptanceCondition(
        condition_id="SDAL0.NO_PRESET_COUNT",
        statement="الأعدادُ مُشتقّةٌ وقتَ القياس",
        disqualifier="عددٌ متوقَّعٌ مُجمَّدٌ في الوحدة يُبطِل الشرط",
    ),
)


def condition_named(condition_id: str) -> StructuralAcceptanceCondition:
    """أعطِ شرطَ القبول بمُعرِّفه، أو ارفض باسم ما لا يُعرَف."""

    for condition in STRUCTURAL_ACCEPTANCE_CONDITIONS:
        if condition.condition_id == condition_id:
            return condition
    raise StructuralDalError(f"شرطُ قبولٍ غيرُ مُسجَّل: {condition_id}")


def preregistration_digest() -> str:
    """بصمةُ التسجيل المسبق؛ مُشتَقّةٌ لا مكتوبة."""

    return canonical_digest(
        canonical_bytes(
            {
                "zero_one_bound": ZERO_ONE_BOUND,
                "scales": [scale.value for scale in Scale],
                "contract_components": [
                    component.value for component in OutputContractComponent
                ],
                "acceptance_items": [item.value for item in AcceptanceItem],
                "transition_contract_fields": list(
                    STRUCTURAL_TRANSITION_CONTRACT_FIELDS
                ),
                "laws": list(STRUCTURAL_DAL_LAWS),
                "conditions": [
                    condition.as_canonical_content()
                    for condition in STRUCTURAL_ACCEPTANCE_CONDITIONS
                ],
            }
        )
    )


PREREGISTRATION_DIGEST: Final[str] = preregistration_digest()


def _refuse_an_incomplete_registration() -> None:
    """ارفض عند الاستيراد تسجيلًا ناقصًا أو مُكرَّرًا أو يُجمِّد عددًا متوقَّعًا."""

    identifiers = [
        condition.condition_id for condition in STRUCTURAL_ACCEPTANCE_CONDITIONS
    ]
    if len(set(identifiers)) != len(identifiers):
        raise StructuralDalError("شرطُ قبولٍ مُكرَّرُ المُعرِّف")
    if len(set(STRUCTURAL_DAL_LAWS)) != len(STRUCTURAL_DAL_LAWS):
        raise StructuralDalError("قانونٌ مُكرَّرٌ في مجموعة القوانين")
    if len(set(STRUCTURAL_TRANSITION_CONTRACT_FIELDS)) != 7:
        raise StructuralDalError("عقدُ الانتقال سباعيُّ الحقول لا أقلَّ ولا أكثر")
    if ZERO_ONE_BOUND != max(scale.slot_count for scale in Scale):
        raise StructuralDalError("حدُّ zero-one يخالف أكبرَ مقياسٍ مُسجَّل")
    for name in globals():
        if name.startswith("EXPECTED") or name.endswith("_EXPECTED_COUNT"):
            raise StructuralDalError(
                f"اسمٌ يُجمِّد عددًا متوقَّعًا: {name}؛ و" + NO_EXPECTED_COUNT_IS_FROZEN
            )


_refuse_an_incomplete_registration()
