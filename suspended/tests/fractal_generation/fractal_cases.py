"""حالاتٌ تخليقيّةٌ محايدةٌ لتشغيل النواة الفراكتاليّة؛ ولا مادّةَ لغويّةً فيها.

المثالُ محايد: مقياسان `scale.alpha` و`scale.beta`، وحاملٌ `carrier.alpha`،
ونمطٌ `pattern.transform`، وثلاثةُ فروعٍ `A` و`B` و`C`.
"""

from __future__ import annotations

from alghanem.fractal_generation import (
    DeclaredDifference,
    ExpansionCandidate,
    ExpansionSet,
    FractalIdentity,
    FractalNode,
    FractalScaleContract,
    FractalSeed,
    MinimumCompleteRequirement,
    PatternContract,
    ProposalProvenance,
    ScaleClosureContract,
    ScaleRelation,
    ScaleRelationEdge,
    ScaleSpace,
)

ALPHA_SCALE = FractalScaleContract(
    scale_id="scale.alpha",
    domain_id="domain.synthetic",
    unit_criterion="الوحدةُ عنصرٌ واحدٌ على الحامل",
    identity_criterion="الهويّةُ مُعرِّفُ نسخةٍ على حاملٍ واحد",
    admissible_operation_contract="تحويلٌ حافظٌ للهويّة أو ولادةُ فرعٍ أفقيّ",
    closure_contract="أقلُّ التمام: هويّةٌ مُحَلّةٌ وأثرٌ متّصلٌ وسجلُّ فروعٍ تامّ",
)

BETA_SCALE = FractalScaleContract(
    scale_id="scale.beta",
    domain_id="domain.synthetic",
    unit_criterion="الوحدةُ تجميعُ عناصرَ من المقياس الأدنى",
    identity_criterion="الهويّةُ مُعرِّفُ تجميعٍ لا مُعرِّفُ عنصر",
    admissible_operation_contract="عملياتُ هذا المقياس غيرُ مفتوحةٍ في هذه المرحلة",
    closure_contract="عقدُ إغلاقِ هذا المقياس مؤجَّلٌ حتى تُفتَح سلطتُه",
)

SCALE_SPACE = ScaleSpace(
    contracts=(ALPHA_SCALE, BETA_SCALE),
    relations=(
        ScaleRelationEdge(
            relation=ScaleRelation.AGGREGATES,
            lower_scale_id="scale.alpha",
            higher_scale_id="scale.beta",
        ),
    ),
)

ALPHA_REF = ALPHA_SCALE.as_ref()
BETA_REF = BETA_SCALE.as_ref()

PRESERVED = ("carrier_continuity", "unit_criterion")

TRANSFORM_PATTERN = PatternContract(
    pattern_id="pattern.transform",
    domain_id="domain.synthetic",
    applicable_scales=(ALPHA_REF,),
    admissible_seed_contract="بذرةٌ على حاملٍ واحدٍ بمحتوًى غيرِ فارغ",
    operation_contract="تحويلُ محتوى الحامل مع حفظ معيار الوحدة",
    preserved_invariants=PRESERVED,
    declared_variation_contract="الفرقُ مُصرَّحٌ في بُعدٍ مُسمًّى لا في الهويّة",
    reapplication_condition="يُعاد التطبيقُ ما بقي معيارُ الوحدة محفوظًا",
    closure_requirements=("MRK.alpha.trace", "MRK.alpha.branches"),
    branch_conditions=("اختلافُ الهويّة مع واجهةٍ مشتركةٍ مُصرَّحة",),
    blockers=("semantic_role",),
    residual_policy="كلُّ ما لم يُحسَم يُسمّى بقيّةً غيرَ ممحوّة",
    authority_scope="صوريٌّ محايدٌ عن اللغات؛ لا سلطةَ دلاليّةَ فيه",
)

PATTERN_REF = TRANSFORM_PATTERN.as_ref()

ALPHA_IDENTITY = FractalIdentity(
    identity_id="identity.alpha",
    scale_ref=ALPHA_REF,
    identity_criterion_id="criterion.instance",
)

BRANCH_IDENTITY = FractalIdentity(
    identity_id="identity.alpha.branch-b",
    scale_ref=ALPHA_REF,
    identity_criterion_id="criterion.instance",
)

SEED = FractalSeed(
    seed_id="seed.alpha",
    identity=ALPHA_IDENTITY,
    carrier_id="carrier.alpha",
    content=(("mark", "m0"),),
)

SEED_NODE = FractalNode.from_seed(SEED, node_id="node.alpha.0")

PROVENANCE = ProposalProvenance(
    proposer_id="proposer.synthetic",
    basis="عقدُ النمط ومحتوى البذرة",
    reason="عرضُ فروقٍ ممكنةٍ عند المقياس الأدنى",
)


def _candidate(
    *,
    candidate_id: str,
    difference_id: str,
    dimension: str,
    description: str,
    preserved: tuple[str, ...] = PRESERVED,
) -> ExpansionCandidate:
    """اقتراحُ توسّعٍ من عقدة البذرة بفرقٍ مُصرَّحٍ مُسمًّى."""

    return ExpansionCandidate(
        candidate_id=candidate_id,
        source=SEED_NODE.as_ref(),
        pattern_ref=PATTERN_REF,
        declared_difference=DeclaredDifference(
            difference_id=difference_id,
            dimension=dimension,
            description=description,
            preserved_invariants=preserved,
        ),
        proposal_provenance=PROVENANCE,
    )


CANDIDATE_A = _candidate(
    candidate_id="branch.A",
    difference_id="difference.A",
    dimension="mark_shape",
    description="تحويلُ صورةِ العلامة مع بقاء الهويّة عينِها",
)

CANDIDATE_B = _candidate(
    candidate_id="branch.B",
    difference_id="difference.B",
    dimension="mark_split",
    description="انفصالُ فرعٍ أخٍ بواجهةٍ مشتركةٍ مُصرَّحة",
)

CANDIDATE_C = _candidate(
    candidate_id="branch.C",
    difference_id="difference.C",
    dimension="mark_order",
    description="فرقُ ترتيبٍ لا دليلَ عليه في هذه المرحلة",
)

EXPANSION_SET = ExpansionSet(
    source=SEED_NODE.as_ref(),
    candidates=(CANDIDATE_A, CANDIDATE_B, CANDIDATE_C),
)

ALPHA_CLOSURE_CONTRACT = ScaleClosureContract(
    scale_ref=ALPHA_REF,
    requirements=(
        MinimumCompleteRequirement(
            requirement_id="MRK.alpha.identity",
            statement="هويّةُ العقدة مُحَلّةٌ عند مقياسها بعقده",
            evidence_kind="resolved_scale_ref",
        ),
        MinimumCompleteRequirement(
            requirement_id="MRK.alpha.trace",
            statement="أثرُ بلوغ العقدة متّصلٌ ببصماته",
            evidence_kind="transition_trace",
        ),
        MinimumCompleteRequirement(
            requirement_id="MRK.alpha.branches",
            statement="سجلُّ الفروع تامٌّ بأحكامه وبقاياه",
            evidence_kind="branch_record",
        ),
    ),
)
