"""بُناةٌ للاختبار وحدَها: توقيعاتٌ صوريّةٌ بلا مضمونٍ لغويّ.

المعرّفاتُ هنا رمزيّةٌ عمدًا (`L0`، `L1`، `alpha`)، لأنّ هذه الحزمةَ غيرُ
مخصوصةٍ بالعربيّة، ولأنّ تسميةَ طبقةٍ عربيّةٍ في اختبارٍ تسميةٌ سابقةٌ لولادتها.
"""

from __future__ import annotations

from alghanem.metaalgebra.layer import (
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
from alghanem.metaalgebra.transition import (
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


def layer(
    layer_id: str = "L0",
    *,
    invariant_names: tuple[str, ...] = ("identity",),
) -> LayerSignature:
    return LayerSignature(
        layer_id=layer_id,
        carrier=CarrierSpecification(
            carrier_id=f"{layer_id}.C",
            membership_condition="شرطُ عضويّةٍ مُصرَّحٌ به",
            what_is_not_a_member="ما لا يستوفي الشرط",
        ),
        state_space=StateSpaceSpecification(
            state_space_id=f"{layer_id}.S",
            state_condition="شرطُ الحالة",
            why_not_folded_into_carrier="الحالةُ تتغيّر والحاملُ يبقى",
        ),
        operations=(
            PartialOperationSpecification(
                operation_id=f"{layer_id}.op",
                input_condition="لازمُ المُدخَل",
                result_condition="لازمُ المخرَج",
                undefined_when=("خارجَ لازم المُدخَل",),
            ),
        ),
        license_relations=(
            LicenseRelationSpecification(
                relation_id=f"{layer_id}.rel",
                holds_when="شرطُ التحقّق",
                refused_when="شرطُ الرفض",
            ),
        ),
        invariants=tuple(
            InvariantComponentSpecification(
                component_name=name,
                extracted_question=f"ما سؤالُ {name}؟",
                forbidden_provenance=("مصدرٌ ممنوع",),
            )
            for name in invariant_names
        ),
        closure=ClosureLawSpecification(
            law_id=f"{layer_id}.cl",
            quotient_condition="شرطُ خارج القسمة",
            observation_condition="شرطُ الملاحظة",
            underpowered_when="عند تعذّر التشغيل",
        ),
        trace=TraceObligationSpecification(
            obligation_id=f"{layer_id}.tr",
            recoverable_facts=("سببُ الترخيص",),
            minimality_condition="لا يحمل الجوابَ كاملًا",
        ),
        residuals=ResidualSchemaSpecification(
            schema_id=f"{layer_id}.R",
            row_condition="صفٌّ لكلّ واقعة",
            completeness_condition="تمامٌ بالوقائع",
        ),
    )


def transition(
    transition_id: str = "alpha",
    *,
    source_layer_id: str = "L0",
    target_layer_id: str = "L1",
    preserved_components: tuple[str, ...] = ("identity",),
) -> TransitionSignature:
    return TransitionSignature(
        transition_id=transition_id,
        source_layer_id=source_layer_id,
        target_layer_id=target_layer_id,
        domain=DomainCondition(
            condition_id=f"{transition_id}.D",
            holds_when="عندما يكون المُدخَل في الحامل المصدر",
            fails_when="عندما يكون خارجه",
        ),
        gate=LicenseGateSpecification(
            gate_id=f"{transition_id}.G",
            licensed_when="عند استيفاء علاقة الترخيص",
            unlicensed_outcomes=(TransitionOutcome.BLOCK, TransitionOutcome.DEFER),
            unlicensed_reason="لا شهادةَ انتقالٍ ناجحٍ بغير ترخيص",
        ),
        transformation=TransformationSpecification(
            transformation_id=f"{transition_id}.T",
            steps=("خطوةٌ أولى",),
            undefined_when=("خارجَ المجال",),
        ),
        preservation=PreservationObligation(
            preserved_components=preserved_components,
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
            residual_condition="ما لم يُنقَل يُسجَّل",
            rank_relation="لا تنقص الرتبةُ بلا تصريح",
            violation_outcome=TransitionOutcome.BLOCK,
        ),
        handoff=HandoffCondition(
            condition_id=f"{transition_id}.handoff",
            holds_when="عند تأهّل المغلَق لعلاقة الطبقة الأعلى",
            beyond_closure="يزيد على الإغلاق تأهّلَ الخروج، والإغلاقُ داخليّ",
            failure_outcome=TransitionOutcome.DEFER,
        ),
    )
