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

الاتّجاه: `arabic → fractal_experiment → fractal_generation`، ولا عكس.

تسجيلٌ لا سلطة: لا ترخيصَ، ولا رتبةَ دائمة، ولا حكمَ كفاية.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
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
    "HELD_OUT_READOUT_COLUMNS",
    "MASAQ_EXPERIMENT_ID",
    "MASAQ_PREREGISTRATION",
    "MASAQ_PREREGISTRATION_CONTENT_ID",
    "MASAQ_SUFFICIENCY_CONTRACT",
    "SEGMENT_CLOSURE_CONTRACT",
    "SEGMENT_SCALE",
    "SEGMENT_SCALE_REF",
    "WORD_SCALE",
    "WORD_SCALE_REF",
    "MasaqExperimentError",
    "MasaqExperimentReport",
    "MasaqWordInput",
    "build_frozen_binding",
    "build_word_inputs",
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
    "weaker_model": "وصلُ المقاطع نصًّا بلا حركاتٍ فراكتاليّةٍ يبلغ الصورةَ نفسَها",
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
class MasaqWordInput:
    """كلمةٌ مُجمَّدةٌ من MASAQ: موضعُها، ومقاطعُها، ووسومُها المحجوبةُ عن المُولِّد."""

    input_id: str
    sura_no: str
    verse_no: str
    word_key: str
    segments: tuple[str, ...]
    held_out_tags: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.input_id.strip():
            raise MasaqExperimentError("مُعرِّفُ الكلمة نصٌّ غير فارغ")
        if not self.segments:
            raise MasaqExperimentError("الكلمةُ مقطعٌ واحدٌ فأكثر")
        if len(self.held_out_tags) != len(self.segments):
            raise MasaqExperimentError("عددُ الوسوم المحجوبة عددُ المقاطع")

    @property
    def joined_surface(self) -> str:
        """صورةُ الكلمة موصولةً من مقاطعها؛ مرجعُ إعادة البناء لا حكمٌ عليها."""

        return "".join(self.segments)

    def generator_projection(self) -> dict[str, object]:
        """ما يراه المُولِّد: موضعُ الكلمة ومقاطعُها، ولا وَسْمَ فيه."""

        return {
            SURA_COLUMN: self.sura_no,
            VERSE_COLUMN: self.verse_no,
            WORD_KEY_COLUMN: self.word_key,
            SEGMENT_INDEX_COLUMN: tuple(
                str(index) for index in range(len(self.segments))
            ),
            SEGMENTED_WORD_COLUMN: self.segments,
        }

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الكلمة المُجمَّدةِ كاملًا للبصمة؛ الوَسْمُ مُجمَّدٌ وإن حُجِب."""

        return {
            "input_id": self.input_id,
            SURA_COLUMN: self.sura_no,
            VERSE_COLUMN: self.verse_no,
            WORD_KEY_COLUMN: self.word_key,
            "segments": list(self.segments),
            "held_out_tags": list(self.held_out_tags),
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
        segments = tuple(
            strip_surface(row.get(SEGMENTED_WORD_COLUMN, "")) for row in rows
        )
        if any(not segment for segment in segments):
            continue
        words.append(
            MasaqWordInput(
                input_id=f"masaq.word.{key[0]}.{key[1]}.{key[2]}",
                sura_no=key[0],
                verse_no=key[1],
                word_key=key[2],
                segments=segments,
                held_out_tags=tuple(row.get(MORPH_TAG_COLUMN, "") for row in rows),
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


def _content_upto(word: MasaqWordInput, index: int) -> tuple[tuple[str, str], ...]:
    return tuple(
        (f"segment.{position}", word.segments[position])
        for position in range(index + 1)
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

    @property
    def standings(self) -> dict[str, int]:
        """عددُ الشواهد بكلِّ وقوف؛ عدٌّ لا ترجيح."""

        counted: dict[str, int] = {
            standing.value: 0 for standing in ExperimentalStanding
        }
        for witness in self.witnesses:
            counted[witness.standing.value] += 1
        return counted


def _witness_of_underpowered(
    word: MasaqWordInput, *, permit: ExperimentalRunPermit, entry: FrozenInputEntry
) -> FractalExperimentalWitness:
    node = FractalNode.from_seed(
        FractalSeed(
            seed_id=f"seed.{word.input_id}",
            identity=_identity_of(word),
            carrier_id=f"carrier.{word.input_id}",
            content=_content_upto(word, 0),
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
) -> tuple[FractalExperimentalWitness, str | None]:
    entry = binding.entry_for(word.input_id)
    binding.refuse_held_out_fields(word.generator_projection())
    if len(word.segments) < 2:
        return _witness_of_underpowered(word, permit=permit, entry=entry), None

    identity = _identity_of(word)
    carrier_id = f"carrier.{word.input_id}"
    node = FractalNode.from_seed(
        FractalSeed(
            seed_id=f"seed.{word.input_id}",
            identity=identity,
            carrier_id=carrier_id,
            content=_content_upto(word, 0),
        ),
        node_id=f"node.{word.input_id}.0",
    )
    first_content_id = node.content_id
    steps: list[FractalTransitionTraceStep] = []
    adjudication = None
    for index in range(1, len(word.segments)):
        candidate_id = f"accretion.{word.input_id}.{index}"
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
            output_content=_content_upto(word, index),
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
            evidence_ref=entry.content_id,
            output_node_id=f"node.{word.input_id}.{index}",
        )
        steps.append(decision.trace_step)
        ExperimentalTransitionGate.record(
            authority=authority,
            permit=permit,
            run_id=run_id,
            binding=binding,
            frozen_input=entry,
            operation=ACCRETION_OPERATION,
            transition=decision.transition,
            trace=FractalTrace(steps=tuple(steps)),
            open_authority_gaps=(NO_LICENSING_AUTHORITY,),
        )
        node = decision.output_node

    trace = FractalTrace(steps=tuple(steps))
    assert adjudication is not None
    closure = ClosureGate.assess(
        candidate=ClosureCandidate(
            node=node,
            trace=trace,
            adjudication=adjudication,
            branch_transitions=(steps[-1],),
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
                    satisfied_by_content_id=first_content_id,
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
                    kind=FractalResidualKind.IRREDUCIBLE_AT_CURRENT_SCALE,
                    subject_id=word.input_id,
                    reason="وحدةُ الكلمة لا تُردّ إلى مقياس المقطع",
                ),
            ),
        ),
        gate_id="gate.closure.masaq.segment",
    )
    rebuilt = "".join(value for _, value in node.content)
    reconstructed = rebuilt == word.joined_surface
    reversed_surface = "".join(reversed(word.segments))
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
    if closed_node is not None and reconstructed:
        standing = ExperimentalStanding.OBSERVED_SUPPORT
    else:
        standing = ExperimentalStanding.OBSERVED_REFUTATION
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
        identity_before=first_content_id,
        identity_after=node.content_id,
        movement_kind="identity_preserving_transformation",
        observed_difference=f"ضُمَّ {len(word.segments) - 1} مقطعًا بحركاتٍ متتابعة",
        reconstruction_observation=(
            "إعادةُ البناء من مخرج الحركات طابقت الصورةَ المُجمَّدة"
            if reconstructed
            else "إعادةُ البناء خالفت الصورةَ المُجمَّدة"
        ),
        closure_observation=(f"حالُ الإغلاق عند مقياس المقطع: {closure.status.value}"),
        preserved_invariants_observed=PRESERVED,
        weaker_model_observations=(
            "وصلُ المقاطع نصًّا بلا حركاتٍ فراكتاليّةٍ يبلغ الصورةَ عينَها",
        ),
        negative_control_observations=(
            "عكسُ ترتيب المقاطع خالف الصورةَ المُجمَّدة"
            if reversed_surface != word.joined_surface
            else "عكسُ ترتيب المقاطع لم يُحدِث فرقًا؛ فالضابطُ السالبُ غيرُ فعّالٍ هنا",
        ),
        counterexample_observations=(
            () if reconstructed else (f"كلمةٌ خالفت إعادةُ بناؤها: {word.input_id}",)
        ),
        residuals=closure.residuals if closed_node is None else closed_node.residuals,
        authority_gaps=(
            NO_LICENSING_AUTHORITY,
            NO_SEMANTIC_AUTHORITY_IN_EXPERIMENT,
            NO_SCALE_NECESSITY_CERTIFICATION_IN_EXPERIMENT,
        ),
        trace=trace,
    )
    return witness, seed_id


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
    for word in words:
        try:
            witness, seed_id = _run_one_word(
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
    )
