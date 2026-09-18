"""عُدَّةُ التشغيل التجريبيِّ التخليقيّ: مادّةٌ محايدةٌ ودورةُ سلطةٍ كاملة.

    FrozenSyntheticInput
      → ExperimentalRunPermit → ACTIVE
      → FGEN transition
      → ExperimentalLiftPermit → ExperimentalNextScaleSeed
      → FractalExperimentalWitness
      → WitnessBundle
      → REVOKED

ولا مادّةَ لغويّةً هنا ولا قراءةَ مِلفٍّ ولا وقت.
"""

from __future__ import annotations

from dataclasses import dataclass

from alghanem.canonical_content import canonical_bytes, canonical_digest
from alghanem.fractal_experiment import (
    NO_LICENSING_AUTHORITY,
    NO_SUFFICIENCY_ASSESSMENT_AUTHORITY,
    ExperimentalFractalAuthority,
    ExperimentalFractalTransition,
    ExperimentalLiftCandidate,
    ExperimentalLiftDecision,
    ExperimentalLiftGate,
    ExperimentalPermitState,
    ExperimentalRunPermit,
    ExperimentalStanding,
    ExperimentalTransitionGate,
    FractalExperimentalWitness,
    FrozenExperimentBinding,
    FrozenInputEntry,
    WitnessBundle,
    issue_experimental_lift_permit,
)
from alghanem.fractal_generation import (
    BranchAdjudicationGate,
    BranchAssessment,
    BranchStanding,
    ClosedFractalNode,
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
    FractalTransitionGate,
    IdentityPreservingTransformationCandidate,
    InvariantAudit,
    MinimumCompleteRequirement,
    PatternConformanceGate,
    PatternConformanceStatus,
    PatternContract,
    ProposalProvenance,
    ScaleClosureContract,
    ScaleRelation,
    ScaleRelationEdge,
    ScaleSpace,
)

LOWER_SCALE = FractalScaleContract(
    scale_id="scale.ex.lower",
    domain_id="domain.synthetic.experiment",
    unit_criterion="الوحدةُ عنصرٌ واحدٌ على الحامل",
    identity_criterion="الهويّةُ مُعرِّفُ نسخةٍ على حاملٍ واحد",
    admissible_operation_contract="تحويلٌ حافظٌ للهويّة عند المقياس الأدنى",
    closure_contract="أقلُّ التمام: هويّةٌ مُحَلّةٌ وأثرٌ متّصلٌ وسجلُّ فروعٍ تامّ",
)

UPPER_SCALE = FractalScaleContract(
    scale_id="scale.ex.upper",
    domain_id="domain.synthetic.experiment",
    unit_criterion="الوحدةُ تجميعُ عناصرَ من المقياس الأدنى",
    identity_criterion="الهويّةُ مُعرِّفُ تجميعٍ لا مُعرِّفُ عنصر",
    admissible_operation_contract="عملياتُ هذا المقياس غيرُ مفتوحةٍ في هذه المرحلة",
    closure_contract="عقدُ إغلاقِ هذا المقياس مؤجَّلٌ حتى تُفتَح سلطتُه",
)

SCALE_SPACE = ScaleSpace(
    contracts=(LOWER_SCALE, UPPER_SCALE),
    relations=(
        ScaleRelationEdge(
            relation=ScaleRelation.AGGREGATES,
            lower_scale_id="scale.ex.lower",
            higher_scale_id="scale.ex.upper",
        ),
    ),
)

LOWER_REF = LOWER_SCALE.as_ref()
UPPER_REF = UPPER_SCALE.as_ref()

PRESERVED = ("carrier_continuity", "unit_criterion")

PATTERN = PatternContract(
    pattern_id="pattern.ex.transform",
    domain_id="domain.synthetic.experiment",
    applicable_scales=(LOWER_REF,),
    admissible_seed_contract="بذرةٌ على حاملٍ واحدٍ بمحتوًى غيرِ فارغ",
    operation_contract="تحويلُ محتوى الحامل مع حفظ معيار الوحدة",
    preserved_invariants=PRESERVED,
    declared_variation_contract="الفرقُ مُصرَّحٌ في بُعدٍ مُسمًّى لا في الهويّة",
    reapplication_condition="يُعاد التطبيقُ ما بقي معيارُ الوحدة محفوظًا",
    closure_requirements=("MRK.ex.trace", "MRK.ex.branches"),
    branch_conditions=("اختلافُ الهويّة مع واجهةٍ مشتركةٍ مُصرَّحة",),
    blockers=("semantic_role",),
    residual_policy="كلُّ ما لم يُحسَم يُسمّى بقيّةً غيرَ ممحوّة",
    authority_scope="صوريٌّ محايدٌ عن اللغات؛ لا سلطةَ دلاليّةَ فيه",
)

PATTERN_REF = PATTERN.as_ref()

OPERATION = "ex.transform"

IDENTITY = FractalIdentity(
    identity_id="identity.ex",
    scale_ref=LOWER_REF,
    identity_criterion_id="criterion.instance",
)

SEED = FractalSeed(
    seed_id="seed.ex",
    identity=IDENTITY,
    carrier_id="carrier.ex",
    content=(("mark", "m0"),),
)

SEED_NODE = FractalNode.from_seed(SEED, node_id="node.ex.0")

CLOSURE_CONTRACT = ScaleClosureContract(
    scale_ref=LOWER_REF,
    requirements=(
        MinimumCompleteRequirement(
            requirement_id="MRK.ex.identity",
            statement="هويّةُ العقدة مُحَلّةٌ عند مقياسها بعقده",
            evidence_kind="resolved_scale_ref",
        ),
        MinimumCompleteRequirement(
            requirement_id="MRK.ex.trace",
            statement="أثرُ بلوغ العقدة متّصلٌ ببصماته",
            evidence_kind="transition_trace",
        ),
        MinimumCompleteRequirement(
            requirement_id="MRK.ex.branches",
            statement="سجلُّ الفروع تامٌّ بأحكامه وبقاياه",
            evidence_kind="branch_record",
        ),
    ),
)

PREREGISTRATION_CONTENT_ID = canonical_digest(
    canonical_bytes(
        {
            "experiment_id": "experiment.synthetic",
            "target_claim": "يُدَّعى أنّ الحركةَ الحافظةَ للهويّة تُغلَق عند مقياسها",
            "what_would_be_observed_as_refutation": "ألّا ينتهي الأثرُ إلى العقدة",
        }
    )
)

FROZEN_ENTRY = FrozenInputEntry(
    input_id="input.ex.0",
    content_id=canonical_digest(canonical_bytes({"mark": "m0"})),
    admission_reason="مدخلٌ تخليقيٌّ مُجمَّدٌ قبل فتح أيِّ إذن",
)

BINDING = FrozenExperimentBinding(
    binding_id="binding.ex",
    source_id="source.synthetic",
    frozen_specification_ref=canonical_digest(
        canonical_bytes({"pattern": PATTERN.pattern_id, "operation": OPERATION})
    ),
    frozen_input_set_ref=canonical_digest(canonical_bytes([FROZEN_ENTRY.content_id])),
    preregistration_content_id=PREREGISTRATION_CONTENT_ID,
    entries=(FROZEN_ENTRY,),
    generator_visible_fields=("mark",),
    held_out_readout_fields=("expected_mark",),
)


def issue_permit(
    authority: ExperimentalFractalAuthority,
    *,
    run_id: str,
    permitted_experimental_lift: bool = True,
) -> ExperimentalRunPermit:
    """أصدِر إذنَ تشغيلٍ تخليقيًّا على الرباط المُجمَّد."""

    return authority.issue(
        binding=BINDING,
        experiment_id="experiment.synthetic",
        run_id=run_id,
        permitted_patterns=(PATTERN_REF,),
        permitted_operations=(OPERATION,),
        permitted_source_scales=(LOWER_REF,),
        permitted_target_scales=(LOWER_REF, UPPER_REF),
        permitted_branch_birth=False,
        permitted_experimental_lift=permitted_experimental_lift,
        authority_scope="تشغيلٌ تخليقيٌّ محايد؛ لا ترخيصَ فيه",
    )


@dataclass(frozen=True)
class SyntheticExperimentalRun:
    """ناتجُ الدورة التجريبيّة كاملةً؛ يُقرأ ولا يُعاد تشغيلُه."""

    authority: ExperimentalFractalAuthority
    permit: ExperimentalRunPermit
    experimental_transition: ExperimentalFractalTransition
    closed: ClosedFractalNode
    lift: ExperimentalLiftDecision
    witness: FractalExperimentalWitness
    bundle: WitnessBundle
    final_state: ExperimentalPermitState


def build_run(run_id: str = "run.ex.1") -> SyntheticExperimentalRun:
    """شغِّل الدورةَ التجريبيّةَ كاملةً من التجميد إلى سحب الإذن."""

    authority = ExperimentalFractalAuthority(authority_id="authority.synthetic")
    permit = authority.activate(issue_permit(authority, run_id=run_id))

    candidate = ExpansionCandidate(
        candidate_id="branch.ex",
        source=SEED_NODE.as_ref(),
        pattern_ref=PATTERN_REF,
        declared_difference=DeclaredDifference(
            difference_id="difference.ex",
            dimension="mark_shape",
            description="تحويلُ صورةِ العلامة مع بقاء الهويّة عينِها",
            preserved_invariants=PRESERVED,
        ),
        proposal_provenance=ProposalProvenance(
            proposer_id="proposer.synthetic",
            basis="عقدُ النمط ومحتوى البذرة",
            reason="عرضُ فرقٍ ممكنٍ عند المقياس الأدنى",
        ),
    )
    conformance = PatternConformanceGate.assess(
        candidate=candidate, pattern=PATTERN, node=SEED_NODE, space=SCALE_SPACE
    )
    assert conformance.status is PatternConformanceStatus.CONFORMANT
    assert conformance.conformant is not None
    adjudication = BranchAdjudicationGate.adjudicate(
        expansion_set=ExpansionSet(source=SEED_NODE.as_ref(), candidates=(candidate,)),
        assessments=(
            BranchAssessment(
                candidate_id="branch.ex",
                standing=BranchStanding.ADMITTED,
                reason="فرقٌ مُطابِقٌ في بُعدٍ غيرِ مانعٍ مع حفظ عين الهويّة",
                residuals=(),
                movement=IdentityPreservingTransformationCandidate(
                    conformant=conformance.conformant,
                    carrier_id="carrier.ex",
                    identity_before=IDENTITY,
                    identity_after=IDENTITY,
                    preserved_invariants=PRESERVED,
                    output_content=(("mark", "m1"),),
                ),
            ),
        ),
        gate_id="gate.adjudication.ex",
    )
    decision = FractalTransitionGate.open_transition(
        adjudication=adjudication,
        candidate_id="branch.ex",
        source_node=SEED_NODE,
        transition_id="transition.ex",
        gate_id="gate.transition.ex",
        evidence_ref=FROZEN_ENTRY.content_id,
        output_node_id="node.ex.1",
    )
    trace = FractalTrace(steps=(decision.trace_step,))
    experimental_transition = ExperimentalTransitionGate.record(
        authority=authority,
        permit=permit,
        run_id=run_id,
        binding=BINDING,
        frozen_input=FROZEN_ENTRY,
        operation=OPERATION,
        transition=decision.transition,
        trace=trace,
        residuals=(
            FractalResidual(
                kind=FractalResidualKind.UNRESOLVED_DIFFERENCE,
                subject_id="branch.ex",
                reason="ما وراء الفرق المُصرَّح غيرُ محسومٍ عند هذا المقياس",
            ),
        ),
        open_authority_gaps=(NO_LICENSING_AUTHORITY,),
    )
    node = decision.output_node
    closure = ClosureGate.assess(
        candidate=ClosureCandidate(
            node=node,
            trace=trace,
            adjudication=adjudication,
            branch_transitions=(decision.trace_step,),
            contract=CLOSURE_CONTRACT,
            coverage=(
                ClosureRequirement(
                    requirement_id="MRK.ex.identity",
                    satisfied_by_content_id=node.identity.content_id,
                    reason="هويّةُ العقدة مُحَلّةٌ في فضاء المقاييس بعقدها",
                ),
                ClosureRequirement(
                    requirement_id="MRK.ex.trace",
                    satisfied_by_content_id=trace.output_content_id,
                    reason="الأثرُ ينتهي إلى هذه العقدة ببصمتها",
                ),
                ClosureRequirement(
                    requirement_id="MRK.ex.branches",
                    satisfied_by_content_id=SEED_NODE.content_id,
                    reason="سجلُّ الفروع تامٌّ بأحكامه وبقاياه",
                ),
            ),
            invariant_audit=InvariantAudit(
                audited_invariants=PRESERVED,
                passed=True,
                reason="ثوابتُ النمط مُدقَّقةٌ على مخرج الحركة",
            ),
            residuals=(),
        ),
        gate_id="gate.closure.ex",
    )
    assert closure.closed is not None
    lift = ExperimentalLiftGate.assess(
        authority=authority,
        permit=permit,
        run_id=run_id,
        candidate=ExperimentalLiftCandidate(
            closed_node=closure.closed,
            lift_permit=issue_experimental_lift_permit(
                authority=authority,
                permit=permit,
                run_id=run_id,
                source_scale_ref=LOWER_REF,
                target_scale_ref=UPPER_REF,
                necessity_claim_under_test=("يُدَّعى أنّ بلوغَ التجميع يقتضي مقياسًا أعلى"),
            ),
            carried_residuals=experimental_transition.residuals,
        ),
        seed_id=f"experimental-seed.{run_id}",
    )
    witness = FractalExperimentalWitness(
        witness_id=f"witness.{run_id}",
        experiment_id=permit.experiment_id,
        run_id=run_id,
        permit_content_id=permit.content_id,
        frozen_input_content_id=FROZEN_ENTRY.content_id,
        preregistration_content_id=PREREGISTRATION_CONTENT_ID,
        standing=ExperimentalStanding.OBSERVED_SUPPORT,
        source_scale=LOWER_REF,
        pattern_ref=PATTERN_REF,
        target_scale=UPPER_REF,
        identity_before=SEED_NODE.content_id,
        identity_after=node.content_id,
        movement_kind=experimental_transition.movement_kind.value,
        observed_difference="تحوّلت صورةُ العلامة مع بقاء عين الهويّة",
        reconstruction_observation="الأثرُ يُعيد بناءَ المخرج من المدخل بلا فجوة",
        closure_observation=f"حالُ الإغلاق: {closure.status.value}",
        preserved_invariants_observed=PRESERVED,
        weaker_model_observations=("نموذجٌ أضعفُ يبلغ الصورةَ نفسَها",),
        negative_control_observations=("قلبُ الفرق يُخالف المخرجَ المرصود",),
        residuals=experimental_transition.residuals,
        authority_gaps=(NO_LICENSING_AUTHORITY,),
        trace=trace,
    )
    bundle = WitnessBundle(
        bundle_id=f"bundle.{run_id}",
        target_claim_ref="يُدَّعى أنّ الحركةَ الحافظةَ للهويّة تُغلَق عند مقياسها",
        preregistration_ref=PREREGISTRATION_CONTENT_ID,
        witnesses=(witness,),
        input_coverage=(FROZEN_ENTRY.input_id,),
        open_authority_gaps=(NO_SUFFICIENCY_ASSESSMENT_AUTHORITY,),
    )
    revoked = authority.revoke(permit)
    return SyntheticExperimentalRun(
        authority=authority,
        permit=revoked,
        experimental_transition=experimental_transition,
        closed=closure.closed,
        lift=lift,
        witness=witness,
        bundle=bundle,
        final_state=authority.state_of(revoked),
    )
