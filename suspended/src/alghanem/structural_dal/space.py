"""`G0.SDAL-0.SPACE`: فضاءُ المقاييس وعقدُ النمط لجبر `zero-one`.

العقودُ هنا تُستعار من النواة الفراكتاليّة المحايدة عن اللغات، فلا يُكتَب عقدُ
انتقالٍ ثانٍ بجانب عقدِها، ولا يُستورد لسانٌ ولا معجمٌ ولا سلطةُ نواة.
"""

from __future__ import annotations

from typing import Final

from alghanem.fractal_generation import (
    FractalScaleContract,
    PatternContract,
    ProposalProvenance,
    ScaleRelation,
    ScaleRelationEdge,
    ScaleSpace,
)

__all__ = [
    "ACCRETION_PATTERN",
    "AGGREGATE_SCALE",
    "AGGREGATE_SCALE_REF",
    "PATTERN_REF",
    "PRESERVED_INVARIANTS",
    "PROPOSAL_PROVENANCE",
    "SCALE_SPACE",
    "SLOT_SCALE",
    "SLOT_SCALE_REF",
]

SLOT_SCALE: Final[FractalScaleContract] = FractalScaleContract(
    scale_id="structural_dal.slot",
    domain_id="domain.structural_dal.synthetic",
    unit_criterion="الوحدةُ خانةٌ واحدةٌ مُصطنَعةٌ يحملها رمزٌ مُبهَم",
    identity_criterion="الهويّةُ مِرساةُ كلٍّ واحدٍ على حامله",
    admissible_operation_contract="ضمُّ خانةٍ واحدةٍ تالية مع حفظ عين المِرساة",
    closure_contract="أقلُّ التمام: تغطيةٌ تامّةٌ للخانات وأثرٌ متّصلٌ وبقايا مُصنَّفة",
)

AGGREGATE_SCALE: Final[FractalScaleContract] = FractalScaleContract(
    scale_id="structural_dal.aggregate",
    domain_id="domain.structural_dal.synthetic",
    unit_criterion="الوحدةُ كلٌّ مُجمَّعٌ من خاناته",
    identity_criterion="الهويّةُ مُعرِّفُ تجميعٍ لا مُعرِّفُ خانة",
    admissible_operation_contract="عملياتُ هذا المقياس غيرُ مفتوحةٍ في هذا الطور",
    closure_contract="عقدُ إغلاق هذا المقياس مؤجَّلٌ حتّى تُفتَح سلطتُه",
)

SCALE_SPACE: Final[ScaleSpace] = ScaleSpace(
    contracts=(SLOT_SCALE, AGGREGATE_SCALE),
    relations=(
        ScaleRelationEdge(
            relation=ScaleRelation.AGGREGATES,
            lower_scale_id="structural_dal.slot",
            higher_scale_id="structural_dal.aggregate",
        ),
    ),
)

SLOT_SCALE_REF: Final = SLOT_SCALE.as_ref()
AGGREGATE_SCALE_REF: Final = AGGREGATE_SCALE.as_ref()

PRESERVED_INVARIANTS: Final[tuple[str, ...]] = ("anchor_identity", "slot_order")

ACCRETION_PATTERN: Final[PatternContract] = PatternContract(
    pattern_id="pattern.structural_dal.slot_accretion",
    domain_id="domain.structural_dal.synthetic",
    applicable_scales=(SLOT_SCALE_REF,),
    admissible_seed_contract="بذرةٌ هي كلٌّ مكتملٌ بخانةٍ واحدة",
    operation_contract="ضمُّ خانةٍ تاليةٍ إلى المحتوى مع حفظ ترتيب الخانات",
    preserved_invariants=PRESERVED_INVARIANTS,
    declared_variation_contract="الفرقُ مُصرَّحٌ في بُعد الضمّ لا في المِرساة",
    reapplication_condition="يُعاد الضمُّ ما لم يُبلَغ حدُّ هذا الطور",
    closure_requirements=(
        "MRK.structural_dal.slot.trace",
        "MRK.structural_dal.slot.coverage",
    ),
    branch_conditions=("لا ولادةَ فرعٍ في هذا التشغيل",),
    blockers=("declared_role_justification", "cross_scale_authority"),
    residual_policy="كلُّ ما لم يُحسَم يُسمّى بقيّةً مُصنَّفةً غيرَ ممحوّة",
    authority_scope="صوريٌّ على خاناتٍ مُصطنَعة؛ لا سلطةَ لسانٍ فيه ولا دلالة",
)

PATTERN_REF: Final = ACCRETION_PATTERN.as_ref()

PROPOSAL_PROVENANCE: Final[ProposalProvenance] = ProposalProvenance(
    proposer_id="proposer.structural_dal.slot_accretion",
    basis="عقدُ النمط وترتيبُ الخانات المُصرَّح",
    reason="عرضُ ضمِّ الخانة التالية عند مقياس الخانة",
)
