"""بُناةٌ للاختبار وحدَها: توقيعاتٌ صوريّةٌ بلا مضمونٍ لغويّ.

المعرّفاتُ هنا رمزيّةٌ عمدًا (`L0`، `L1`، `alpha`)، لأنّ هذه الحزمةَ غيرُ
مخصوصةٍ بالعربيّة، ولأنّ تسميةَ طبقةٍ عربيّةٍ في اختبارٍ تسميةٌ سابقةٌ لولادتها.
"""

from __future__ import annotations

from alghanem.metaalgebra.clause import DeclarativeClause
from alghanem.metaalgebra.layer import (
    LAYER_COMPONENT_NAMES,
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
from alghanem.metaalgebra.realization import (
    REALIZED_TRANSITION_COMPONENT_NAMES,
    ComponentRealization,
    LayerRealization,
    Realization,
    RealizationDomainRef,
    ResidualDisposition,
    ResidualDispositionRealization,
    TransitionRealization,
)
from alghanem.metaalgebra.specification import AbstractSystemSpecification, SchemaRef
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


def specification(
    spec_id: str = "SIGMA_A.test",
    *,
    layer_ids: tuple[str, ...] = ("L0", "L1"),
    transition_ids: tuple[str, ...] = ("alpha",),
) -> AbstractSystemSpecification:
    layers = tuple(layer(layer_id) for layer_id in layer_ids)
    transitions = tuple(
        transition(
            transition_id,
            source_layer_id=layer_ids[0],
            target_layer_id=layer_ids[1],
        )
        for transition_id in transition_ids
    )
    return AbstractSystemSpecification(
        spec_id=spec_id,
        schema_ref=SchemaRef.of(),
        layers=layers,
        transitions=transitions,
    )


def component_realizations(
    names: tuple[str, ...],
    *,
    prefix: str = "D",
) -> tuple[ComponentRealization, ...]:
    return tuple(
        ComponentRealization(
            component_name=name,
            realized_as=f"{prefix}::{name}",
            realization_condition=DeclarativeClause(
                clause_id=f"{prefix}.{name}",
                clause_text=f"شرطُ تحقّق `{name}` في الميدان",
                why_not_executable="لم تُعطَ له دلالةٌ قابلةٌ للترجمة بعدُ",
            ),
            what_would_falsify_this_realization=f"موضعٌ في الميدان لا يستوفي `{name}`",
        )
        for name in names
    )


def layer_realization(layer_id: str = "L0", *, prefix: str = "D") -> LayerRealization:
    return LayerRealization(
        layer_id=layer_id,
        components=component_realizations(LAYER_COMPONENT_NAMES, prefix=prefix),
        residual_dispositions=tuple(
            ResidualDispositionRealization(
                disposition=disposition,
                holds_when=f"شرطُ `{disposition.value}` في الميدان",
            )
            for disposition in ResidualDisposition
        ),
    )


def transition_realization(
    transition_id: str = "alpha", *, prefix: str = "D"
) -> TransitionRealization:
    return TransitionRealization(
        transition_id=transition_id,
        components=component_realizations(
            REALIZED_TRANSITION_COMPONENT_NAMES, prefix=prefix
        ),
        unlicensed_outcome_realizations=(
            (TransitionOutcome.BLOCK, "منعٌ مُسمًّى في الميدان"),
            (TransitionOutcome.DEFER, "لا-جوابٍ معرفيٍّ في الميدان"),
        ),
    )


def realization(
    realization_id: str = "R.test",
    *,
    domain_id: str = "D0",
    spec: AbstractSystemSpecification | None = None,
    realize_transitions: bool = True,
) -> Realization:
    specification_value = specification() if spec is None else spec
    return Realization(
        realization_id=realization_id,
        domain=RealizationDomainRef(
            domain_id=domain_id,
            description=f"ميدانٌ صوريٌّ للاختبار `{domain_id}`",
            what_is_not_this_domain="ما لا يقع في هذا الميدان",
        ),
        specification=specification_value,
        layer_realizations=tuple(
            layer_realization(layer_id, prefix=domain_id)
            for layer_id in specification_value.layer_ids
        ),
        transition_realizations=(
            tuple(
                transition_realization(transition_id, prefix=domain_id)
                for transition_id in specification_value.transition_ids
            )
            if realize_transitions
            else ()
        ),
        deferred_transition_ids=(
            () if realize_transitions else specification_value.transition_ids
        ),
    )
