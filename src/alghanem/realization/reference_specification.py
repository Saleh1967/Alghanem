"""مواصفةٌ مرجعيّةٌ `Σ_A^ref`: أصغرُ نظريّةٍ تكفي لممارسة التوليد والتحقيق.

    Σ_M  →  Σ_A^ref  →  { R_python(Σ_A^ref), R_arabic(Σ_A^ref) }

**ومعرّفاتُها رمزيّةٌ عمدًا** (`L0`، `L1`، `alpha`): تسميةُ طبقةٍ عربيّةٍ هنا
تسميةٌ سابقةٌ لولادتها، وتسميةٌ برمجيّةٌ هنا تجعل لغةَ التنفيذ أصلًا. فالأصلُ
محايدٌ عن ميدانيه، وهذا شرطُ أن يكون أصلًا لا ترجمةً لأحدهما.

**وهذه المواصفةُ تمرينُ توليدٍ لا دعوى نظريّة:** لا تدّعي أنّ `L0` و`L1` طبقتان
حقيقيّتان في أيِّ ميدان، بل تُثبت أنّ الآلة تشتغل على مواصفةٍ ما. والدعوى
الوحيدةُ المُستفادةُ منها دعوى **آليّة**: أنّ `G_py` دالّةٌ حتميّةٌ من `Σ_A`.
"""

from __future__ import annotations

from typing import Final

from ..metaalgebra.layer import (
    CarrierSpecification,
    ClosureLawSpecification,
    InvariantComponentSpecification,
    LayerSignature,
    LicenseRelationSpecification,
    PartialOperationSpecification,
    ResidualSchemaSpecification,
    StateSpaceSpecification,
    TraceObligationSpecification,
)
from ..metaalgebra.specification import AbstractSystemSpecification, SchemaRef
from ..metaalgebra.transition import (
    REQUIRED_AUDIT_CERTIFICATE_FACTS,
    DomainCondition,
    HandoffCondition,
    LicenseGateSpecification,
    PreservationObligation,
    ResidualRankPolicy,
    TransformationSpecification,
    TransitionOutcome,
    TransitionSignature,
    TransitionTraceObligation,
)

__all__ = [
    "A_REFERENCE_SPECIFICATION_IS_A_GENERATION_EXERCISE",
    "REFERENCE_SPECIFICATION",
    "REFERENCE_SPECIFICATION_ID",
]

REFERENCE_SPECIFICATION_ID: Final = "SIGMA_A.reference"

A_REFERENCE_SPECIFICATION_IS_A_GENERATION_EXERCISE: Final = (
    "المواصفةُ المرجعيّةُ تمرينُ توليدٍ لا دعوى نظريّة؛ "
    "ورمزيّةُ معرّفاتها شرطُ حيادِ الأصل عن ميدانيه"
)


def _reference_layer(layer_id: str) -> LayerSignature:
    return LayerSignature(
        layer_id=layer_id,
        carrier=CarrierSpecification(
            carrier_id=f"{layer_id}.C",
            membership_condition=f"عضوُ `{layer_id}.C` ما استوفى شرطَ الحمل المُصرَّحَ به",
            what_is_not_a_member="ما لم يُعرَض عليه شرطُ الحمل أصلًا",
        ),
        state_space=StateSpaceSpecification(
            state_space_id=f"{layer_id}.S",
            state_condition=f"حالُ `{layer_id}` إسنادٌ قابلٌ للتغيّر على حاملٍ ثابت",
            why_not_folded_into_carrier="الحالُ يتغيّر والحاملُ يبقى؛ ودمجُهما يُخفي التغيّر",
        ),
        operations=(
            PartialOperationSpecification(
                operation_id=f"{layer_id}.op",
                input_condition="المُدخَلُ عضوٌ في الحامل وحالُه معرَّف",
                result_condition="المخرَجُ عضوٌ في الحامل نفسِه بحالٍ معرَّف",
                undefined_when=("المُدخَلُ خارجَ الحامل", "حالُ المُدخَل غيرُ معرَّف"),
            ),
        ),
        license_relations=(
            LicenseRelationSpecification(
                relation_id=f"{layer_id}.rel",
                holds_when="حين يستوفي الموضعُ شرطَ العلاقة المُصرَّحَ به",
                refused_when="حين يتخلّف شرطُ العلاقة، فلا ترخيصَ بالسكوت",
            ),
        ),
        invariants=(
            InvariantComponentSpecification(
                component_name="identity",
                extracted_question="أهو هو بعدَ التشغيل أم صار غيرَه؟",
                forbidden_provenance=("استنتاجُ الهُويّة من ثبات الاسم",),
            ),
        ),
        closure=ClosureLawSpecification(
            law_id=f"{layer_id}.cl",
            quotient_condition="موضعان مغلَقان متساويان إن تطابقا في كلّ ملاحظةٍ مُصرَّحٍ بها",
            observation_condition="الملاحظاتُ المُصرَّحُ بها وحدَها تُميّز",
            underpowered_when="حين تعجز الملاحظاتُ عن التمييز بين موضعين مختلفين",
        ),
        trace=TraceObligationSpecification(
            obligation_id=f"{layer_id}.tr",
            recoverable_facts=("سببُ الترخيص", "الشرطُ المستوفى"),
            minimality_condition="يكفي لتفسير الترخيص ولا يحمل الجوابَ كاملًا",
        ),
        residuals=ResidualSchemaSpecification(
            schema_id=f"{layer_id}.R",
            row_condition="صفٌّ لكلّ واقعةِ تشغيلٍ لا لكلّ واقعةِ تغيُّر",
            completeness_condition="تمامٌ بالوقائع لا بالمُتغيِّرات منها",
        ),
    )


def _reference_transition(
    transition_id: str, *, source_layer_id: str, target_layer_id: str
) -> TransitionSignature:
    return TransitionSignature(
        transition_id=transition_id,
        source_layer_id=source_layer_id,
        target_layer_id=target_layer_id,
        domain=DomainCondition(
            condition_id=f"{transition_id}.D",
            holds_when=f"حين يكون المُدخَلُ عضوًا مغلَقًا في `{source_layer_id}.C`",
            fails_when="حين يكون خارجَ الحامل المصدر أو غيرَ مغلَق",
        ),
        gate=LicenseGateSpecification(
            gate_id=f"{transition_id}.G",
            licensed_when="حين تستوفى علاقةُ الترخيص في الطبقة المصدر",
            unlicensed_outcomes=(TransitionOutcome.BLOCK, TransitionOutcome.DEFER),
            unlicensed_reason="لا شهادةَ انتقالٍ ناجحٍ بغير ترخيصٍ مُصرَّحٍ به",
        ),
        transformation=TransformationSpecification(
            transformation_id=f"{transition_id}.T",
            steps=("قراءةُ الموضع المصدر", "بناءُ الموضع الهدف بحالٍ معرَّف"),
            undefined_when=("خارجَ شرطِ المجال", "حين يتخلّف شرطُ التسليم"),
        ),
        preservation=PreservationObligation(
            preserved_components=("identity",),
            changed_components=("quantity",),
            preservation_condition="Inv_i(x) = Inv_{i+1}(T_i(x)) في المُسمّى وحدَه",
        ),
        trace=TransitionTraceObligation(
            obligation_id=f"{transition_id}.tau",
            certificate_facts=REQUIRED_AUDIT_CERTIFICATE_FACTS,
            minimality_condition="تكفي لتفسير الترخيص لا لاستعادة الأصل",
        ),
        residual_policy=ResidualRankPolicy(
            policy_id=f"{transition_id}.rho",
            residual_condition="ما لم يُنقَل إلى الهدف يُسجَّل بقيّةً لا يُهمَل",
            rank_relation="لا تنقص رتبةُ البقايا بلا تصريحٍ بسبب النقص",
            violation_outcome=TransitionOutcome.BLOCK,
        ),
        handoff=HandoffCondition(
            condition_id=f"{transition_id}.handoff",
            holds_when="حين يتأهّل المغلَقُ لعلاقةِ الطبقة الأعلى",
            beyond_closure="يزيد على الإغلاق تأهّلَ الخروج، والإغلاقُ داخليٌّ لا يُخرِج",
            failure_outcome=TransitionOutcome.DEFER,
        ),
    )


REFERENCE_SPECIFICATION: Final = AbstractSystemSpecification(
    spec_id=REFERENCE_SPECIFICATION_ID,
    schema_ref=SchemaRef.of(),
    layers=(_reference_layer("L0"), _reference_layer("L1")),
    transitions=(
        _reference_transition("alpha", source_layer_id="L0", target_layer_id="L1"),
    ),
)
