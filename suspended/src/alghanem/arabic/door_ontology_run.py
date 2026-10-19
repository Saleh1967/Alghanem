"""مسارٌ كاملٌ موصولٌ: سؤالٌ ← تحليلٌ ← مضمونٌ ← رصيدٌ ← استدلالٌ ← تحقّقٌ ← قبول.

هذه الوحدةُ **تشغيلٌ** لا وصف: تُقيم عالَمًا صغيرًا مُعلَنًا (زيدٌ، وبابٌ،
ومصراعُه)، وتقرأ عباراتِ عائلة الفتح من بايتاتها، وتعبر بها إلى مضمون، وتُودِع
ما يُودَع منه بدليلٍ يُثبِت، ثمّ تُجيب عن سؤالين مختلفَي المتطلّبات، وتفحص
الجوابَ فحصًا مستقلًّا، ثمّ تقبله أو تمتنع.

**والجوابُ يتغيّر إذا تغيّرت معرفةٌ ذاتُ صلة** (`THE_JUDGMENT_FOLLOWS_ITS_EVIDENCE`):
وهذا هو مَحكُّ الإنجاز لا عددُ الجمل المقبولة. ولذلك تُخرِج `full_run` حالَ
السؤالين **قبل** إيداع دليلِ حالِ الباب و**بعده**، ومعهما شاهدُ عدم اللزوم
بنموذجين يختلفان في حال الباب ويتّفقان على كلّ ما سواه.

**وعدمُ الحسم ليس إثباتًا لعدم اللزوم** (`A_SILENCE_IS_NOT_A_PROOF`): فلا
يُكتفى بخروج `UNDECIDED_BY_AVAILABLE_PREMISES` عن سؤال حال الباب؛ بل يُقدَّم
النموذجان صراحةً.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Final

from ..ontology import (
    Answer,
    Derivation,
    DesignationMethod,
    Evidence,
    EvidenceGenus,
    ExistenceStanding,
    FactRegister,
    Individual,
    MinimalityReading,
    ModelConstraint,
    NonEntailmentWitness,
    Polarity,
    Proposition,
    PropositionForm,
    Question,
    QuestionKind,
    Scope,
    SubstanceStore,
    SupportStatus,
    VerificationReport,
    accept,
    assess_support,
    deletion_test,
    hold_state,
    non_entailment_witness,
    verify,
)
from .door_domain_deposit import (
    DOOR_OPENING_EVENT_ID,
    DOOR_STATE_ID,
    DOOR_STATE_OPEN,
    DOOR_STATE_SHUT,
    DOOR_TYPE_ID,
    HUMAN_TYPE_ID,
    door_domain_store,
)
from .fath_ontology_bridge import (
    BridgeResult,
    ProvenanceGenus,
    TraceItem,
    bridge_utterance,
)
from .fath_surface_analysis import read_utterance

__all__ = [
    "door_model_constraints",
    "A_SILENCE_IS_NOT_A_PROOF",
    "THE_JUDGMENT_FOLLOWS_ITS_EVIDENCE",
    "THE_NEGATION_UTTERANCE",
    "THE_OBSERVED_INTERVAL",
    "THE_QUESTION_INTERVAL",
    "DOOR_INDIVIDUAL_ID",
    "LEAF_INDIVIDUAL_ID",
    "RunOutcome",
    "ZAYD_INDIVIDUAL_ID",
    "door_state_observation",
    "door_world_register",
    "full_run",
    "occurrence_question",
    "state_question",
    "surface_candidates",
]

A_SILENCE_IS_NOT_A_PROOF: Final[str] = (
    "خروجُ الحكم `UNDECIDED_BY_AVAILABLE_PREMISES` بيانُ عجزِ المقدّمات، وليس "
    "برهانًا على أنّ «لم يفتح زيدٌ البابَ» لا تستلزم «البابُ مغلق»؛ والبرهانُ "
    "نموذجان متوافقان مع المقدّمات يختلفان في حال الباب"
)

THE_JUDGMENT_FOLLOWS_ITS_EVIDENCE: Final[str] = (
    "محكُّ النواة أن يتغيّر الحكمُ حين تتغيّر معرفةٌ ذاتُ صلة، وأن يثبت حين "
    "تتغيّر معرفةٌ لا صلةَ لها؛ لا أن يكثر ما يقبله من الجمل"
)

THE_NEGATION_UTTERANCE: Final[bytes] = "لَمْ يَفْتَحْ زَيْدٌ الْبَابَ".encode()
"""العبارةُ المُشغَّلة؛ **بايتاتٌ** لأنّ البصمةَ والقراءةَ عليهما لا على نصٍّ جاهز."""

ZAYD_INDIVIDUAL_ID: Final[str] = "فرد-زيد"
DOOR_INDIVIDUAL_ID: Final[str] = "فرد-باب-الدار"
LEAF_INDIVIDUAL_ID: Final[str] = "فرد-مصراع-باب-الدار"

_TIMELINE: Final[str] = "خطّ-زمن-الدار"
_DOMAIN: Final[str] = "مجال-الأبواب"

THE_QUESTION_INTERVAL: Final[Scope] = Scope(
    domain_id=_DOMAIN, timeline_id=_TIMELINE, start=10, end=20
)
"""فترةُ السؤال؛ مُعلَنةٌ لأنّ «الآن» بلا خطِّ زمنٍ لا يُفحَص."""

THE_OBSERVED_INTERVAL: Final[Scope] = Scope(
    domain_id=_DOMAIN, timeline_id=_TIMELINE, start=10, end=20
)
"""فترةُ المشاهدة؛ وما خرج عنها لا يُعمَّم إليه بلا قاعدةِ استمرارٍ مُصرَّحة."""

_WIDE: Final[Scope] = Scope(domain_id=_DOMAIN, timeline_id=_TIMELINE, start=0, end=100)


def surface_candidates() -> dict[str, tuple[str, ...]]:
    """مرشَّحو الإحالة لكلّ سطحٍ اسميّ؛ **مستوردون** لا مُستخرَجون من العبارة."""

    return {
        "زَيْدٌ": (ZAYD_INDIVIDUAL_ID,),
        "الْبَابَ": (DOOR_INDIVIDUAL_ID,),
        "الْبَابُ": (DOOR_INDIVIDUAL_ID,),
    }


def _observation(evidence_id: str, statement: str, scope: Scope) -> Evidence:
    return Evidence(
        evidence_id=evidence_id,
        genus=EvidenceGenus.DIRECT_OBSERVATION,
        statement=statement,
        source_name="مشاهدةُ هذا العالَم المُعلَن",
        scope=scope,
        source_digest=None,
    )


def door_world_register(store: SubstanceStore) -> FactRegister:
    """أقِم سجلَّ الوقائع: أفرادٌ مُثبَتو الوجود، وصفاتٌ وأجزاءٌ وقدراتٌ بأدلّتها.

    المدخل: رصيدُ مجال الأبواب.
    الشرط: كلُّ فردٍ مُثبَتٍ له دليلٌ قائمٌ، وكلُّ قضيّةٍ دليلُها مُثبِتٌ للوقائع.
    المخرج: سجلٌّ تُختبَر عليه العمليات.
    حدُّها: لا حالَ للباب فيه بعد؛ وذلك مقصودٌ ليظهر أثرُ إيداع الدليل.
    """

    existence = _observation(
        "مشاهدة-وجود-الأطراف",
        "شوهد في الدار بابٌ له مصراعٌ يُدار، وشوهد زيدٌ إنسانًا حاضرًا",
        _WIDE,
    )
    register = FactRegister(
        register_id="سجلّ-الدار",
        evidence=(existence,),
        individuals=(),
        propositions=(),
    )
    register = register.with_individual(
        Individual(
            individual_id=ZAYD_INDIVIDUAL_ID,
            designation_method=DesignationMethod.PROPER_NAME,
            candidate_type_ids=(HUMAN_TYPE_ID,),
            existence=ExistenceStanding.ESTABLISHED,
            evidence_ref=existence.ref,
        )
    )
    register = register.with_individual(
        Individual(
            individual_id=DOOR_INDIVIDUAL_ID,
            designation_method=DesignationMethod.DEFINITE_DESCRIPTION,
            candidate_type_ids=(DOOR_TYPE_ID,),
            existence=ExistenceStanding.ESTABLISHED,
            evidence_ref=existence.ref,
        )
    )
    register = register.with_individual(
        Individual(
            individual_id=LEAF_INDIVIDUAL_ID,
            designation_method=DesignationMethod.DEFINITE_DESCRIPTION,
            candidate_type_ids=("مصراع",),
            existence=ExistenceStanding.ESTABLISHED,
            evidence_ref=existence.ref,
        )
    )
    register = register.with_proposition(
        Proposition(
            proposition_id="قضيّة-وظيفة-الباب",
            form=PropositionForm.ATTRIBUTE_VALUE,
            subject_id=DOOR_INDIVIDUAL_ID,
            predicate_id="صفة_الوظيفة",
            value="ساترُ منفذٍ يُدار",
            polarity=Polarity.AFFIRMED,
            scope=_WIDE,
            evidence_ref=existence.ref,
        )
    )
    register = register.with_proposition(
        Proposition(
            proposition_id="قضيّة-قدرة-الباب",
            form=PropositionForm.RELATION_HOLDS,
            subject_id=DOOR_INDIVIDUAL_ID,
            predicate_id="له_قدرة",
            value="قدرة_الانفتاح",
            polarity=Polarity.AFFIRMED,
            scope=_WIDE,
            evidence_ref=existence.ref,
        )
    )
    return register.with_proposition(
        Proposition(
            proposition_id="قضيّة-جزئيّة-المصراع",
            form=PropositionForm.RELATION_HOLDS,
            subject_id=LEAF_INDIVIDUAL_ID,
            predicate_id="جزء_من",
            value=DOOR_INDIVIDUAL_ID,
            polarity=Polarity.AFFIRMED,
            scope=_WIDE,
            evidence_ref=existence.ref,
        )
    )


def door_state_observation(value: str = DOOR_STATE_SHUT) -> Evidence:
    """دليلُ مشاهدةٍ **مستقلٌّ** لحال الباب في فترةٍ معلومة.

    المدخل: قيمةُ الحال المشاهَدة.
    الشرط: القيمةُ من قيم الحال المغلقة، ويُفحَص ذلك عند الحمل لا هنا.
    المخرج: دليلٌ جنسُه مشاهدةٌ مباشرة، نطاقُه فترةُ المشاهدة وحدَها.
    حدُّها: لا يمتدّ خارج فترته؛ وتعميمُه يحتاج قاعدةَ استمرارٍ بموانعها.
    """

    return _observation(
        "مشاهدة-حال-الباب",
        f"شوهد بابُ الدار «{value}» في الفترة المُعلَنة، ولم يُشاهَد خارجها",
        THE_OBSERVED_INTERVAL,
    )


def occurrence_question() -> Question:
    """سؤالُ الوقوع: هل فتح زيدٌ البابَ في الفترة؟"""

    return Question(
        question_id="سؤال-الوقوع",
        text="هل فتح زيدٌ البابَ في الفترة المُعلَنة؟",
        kind=QuestionKind.EVENT_OCCURRENCE,
        subject_id=ZAYD_INDIVIDUAL_ID,
        predicate_id=DOOR_OPENING_EVENT_ID,
        scope=THE_QUESTION_INTERVAL,
    )


def state_question() -> Question:
    """سؤالُ الحال: هل البابُ مغلقٌ في الفترة؟"""

    return Question(
        question_id="سؤال-الحال",
        text="هل بابُ الدار مغلقٌ في الفترة المُعلَنة؟",
        kind=QuestionKind.CURRENT_STATE,
        subject_id=DOOR_INDIVIDUAL_ID,
        predicate_id=DOOR_STATE_ID,
        scope=THE_QUESTION_INTERVAL,
    )


def _occurrence_target() -> Proposition:
    evidence = _observation("هدف-صوريّ", "قضيّةٌ مسؤولٌ عنها لا مُودَعة", _WIDE)
    return Proposition(
        proposition_id="هدف-الوقوع",
        form=PropositionForm.EVENT_OCCURRED,
        subject_id=ZAYD_INDIVIDUAL_ID,
        predicate_id=DOOR_OPENING_EVENT_ID,
        value=None,
        polarity=Polarity.AFFIRMED,
        scope=THE_QUESTION_INTERVAL,
        evidence_ref=evidence.ref,
    )


def _state_target(value: str = DOOR_STATE_SHUT) -> Proposition:
    evidence = _observation("هدف-صوريّ", "قضيّةٌ مسؤولٌ عنها لا مُودَعة", _WIDE)
    return Proposition(
        proposition_id="هدف-الحال",
        form=PropositionForm.STATE_HOLDS,
        subject_id=DOOR_INDIVIDUAL_ID,
        predicate_id=DOOR_STATE_ID,
        value=value,
        polarity=Polarity.AFFIRMED,
        scope=THE_QUESTION_INTERVAL,
        evidence_ref=evidence.ref,
    )


def _answer(question: Question, derivation: Derivation, statement: str) -> Answer:
    return Answer(
        question_id=question.question_id,
        status=derivation.status,
        derivation=derivation,
        statement=statement,
    )


def _restricted(register: FactRegister, keep: Sequence[str]) -> FactRegister:
    kept = tuple(item for item in register.propositions if item.proposition_id in keep)
    return FactRegister(
        register_id=register.register_id,
        evidence=register.evidence,
        individuals=register.individuals,
        propositions=kept,
    )


@dataclass(frozen=True, slots=True)
class RunOutcome:
    """مخرجُ التشغيل كلِّه: ما قبل إيداع دليل الحال وما بعده، بأثرٍ مُوسَّم."""

    bridge: BridgeResult
    occurrence_before: Derivation
    state_before: Derivation
    witness: NonEntailmentWitness
    state_after: Derivation
    occurrence_after: Derivation
    state_after_irrelevant_change: Derivation
    minimality: MinimalityReading
    report: VerificationReport
    accepted: bool
    trace: tuple[TraceItem, ...]

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التشغيل للبصمة والمراجعة."""

        return {
            "bridge": self.bridge.as_canonical_content(),
            "occurrence_before": self.occurrence_before.as_canonical_content(),
            "state_before": self.state_before.as_canonical_content(),
            "witness": self.witness.as_canonical_content(),
            "state_after": self.state_after.as_canonical_content(),
            "occurrence_after": self.occurrence_after.as_canonical_content(),
            "state_after_irrelevant_change": (
                self.state_after_irrelevant_change.as_canonical_content()
            ),
            "minimality": self.minimality.as_canonical_content(),
            "report": self.report.as_canonical_content(),
            "accepted": self.accepted,
            "trace": [item.as_canonical_content() for item in self.trace],
        }


def door_model_constraints() -> tuple[ModelConstraint, ...]:
    """الصورةُ المنفَّذةُ للقاعدة الصارمة `قاعدة-أثر-الفتح`، مربوطةً بمُعرِّفها.

    المدخل: لا شيء؛ القاعدةُ مودَعةٌ في رصيد هذا المجال.
    الشرط: لكلّ قاعدةٍ صارمةٍ في الرصيد قيدٌ ههنا، وإلّا رفض `check_model`
        إخراجَ شهادةِ عدمِ لزومٍ وسمّى القاعدةَ غيرَ منفَّذة.
    المخرج: قيودٌ تُنفَّذ على النماذج.
    حدُّها: نمطُ القاعدة في الرصيد نثرٌ، وهذا القيدُ **نقلٌ مُعلَنٌ** له لا
        اشتقاقٌ منه؛ فمن غيَّر النثرَ لزمه تغييرُ القيد بيده.
    """

    return (
        ModelConstraint(
            constraint_id="قيد-أثر-الفتح",
            rule_versioned_id="قاعدة-أثر-الفتح@١",
            individual_id=DOOR_INDIVIDUAL_ID,
            trigger_event_type_id=DOOR_OPENING_EVENT_ID,
            required_state_id=DOOR_STATE_ID,
            required_value=DOOR_STATE_OPEN,
        ),
    )


def full_run() -> RunOutcome:
    """شغِّل المسارَ كاملًا، وأخرِج الحكمَ قبل تغيّر المعرفة وبعده.

    المدخل: لا شيء؛ العالَمُ والرصيدُ مُعلَنان في هذه الوحدة.
    الشرط: العبارةُ تُقرَأ من بايتاتها، والجسرُ يقبل تركيبَها.
    المخرج: `RunOutcome` فيه الأثرُ المُوسَّم، والأحكامُ قبل الدليل وبعده،
        وشاهدُ عدم اللزوم، واختبارُ الحذف، وتقريرُ التحقّق، وحالُ القبول.
    حدُّها: لا تقول شيئًا عن أبوابٍ خارج هذا العالَم المُعلَن.
    """

    store = door_domain_store()
    register = door_world_register(store)
    reading = read_utterance(THE_NEGATION_UTTERANCE)
    bridge = bridge_utterance(
        reading=reading,
        store=store,
        register=register,
        time_scope=THE_QUESTION_INTERVAL,
        surface_candidates=surface_candidates(),
    )
    report_evidence = Evidence(
        evidence_id="خبر-معتمد-عن-العبارة",
        genus=EvidenceGenus.ACCEPTED_REPORT,
        statement=(
            "قائلٌ معتمدٌ أخبر بمضمون «لم يفتح زيدٌ البابَ» في الفترة المُعلَنة؛ "
            "والمقبولُ مضمونُه بقطبيّته، لا تحويلُه إلى موجب"
        ),
        source_name="خبرُ هذا العالَم المُعلَن",
        scope=THE_QUESTION_INTERVAL,
        source_digest=None,
    )
    register = register.deposit_from_discourse(
        bridge.content, report_evidence, "قضيّة-نفي-الفتح"
    )

    occurrence_question_ = occurrence_question()
    state_question_ = state_question()
    occurrence_before = assess_support(
        occurrence_question_.question_id, _occurrence_target(), register, store
    )
    state_before = assess_support(
        state_question_.question_id,
        _state_target(),
        register,
        store,
        missing_premise_note=(
            "لا دليلَ على حال الباب في الفترة؛ والمنفيُّ وقوعُ فتحٍ من زيدٍ "
            "وحدَه، و" + A_SILENCE_IS_NOT_A_PROOF
        ),
    )
    witness = non_entailment_witness(
        question_ref=state_question_.question_id,
        individual_id=DOOR_INDIVIDUAL_ID,
        state_id=DOOR_STATE_ID,
        values=(DOOR_STATE_SHUT, DOOR_STATE_OPEN),
        shared_occurred_event_keys=(),
        store=store,
        constraints=door_model_constraints(),
        content=bridge.content,
        declared_model_note=(
            "نموذجان يتّفقان على أنّ زيدًا لم يفتح البابَ في الفترة، ويختلفان "
            "في حاله: في الأوّل كان مغلقًا، وفي الثاني كان مفتوحًا أصلًا أو "
            "فتحه غيرُه؛ وكلاهما متوافقٌ مع المقدّمات المُعلَنة"
        ),
    )

    observation = door_state_observation(DOOR_STATE_SHUT)
    after = hold_state(
        individual_id=DOOR_INDIVIDUAL_ID,
        state_id=DOOR_STATE_ID,
        value=DOOR_STATE_SHUT,
        scope=THE_OBSERVED_INTERVAL,
        evidence=observation,
        proposition_id="قضيّة-حال-الباب",
        register=register,
        store=store,
    )
    state_after = assess_support(
        state_question_.question_id, _state_target(), after, store
    )
    occurrence_after = assess_support(
        occurrence_question_.question_id, _occurrence_target(), after, store
    )

    unrelated = Evidence(
        evidence_id="مشاهدة-وجود-الأطراف",
        genus=EvidenceGenus.DIRECT_OBSERVATION,
        statement=(
            "شوهد في الدار بابٌ له مصراعٌ يُدار، وشوهد زيدٌ إنسانًا حاضرًا، "
            "وشوهد معهما سراجٌ لا أثرَ له في حال الباب"
        ),
        source_name="مشاهدةُ هذا العالَم المُعلَن",
        scope=_WIDE,
        source_digest=None,
    )
    after_unrelated = after.amend_evidence(unrelated)
    state_after_irrelevant_change = assess_support(
        state_question_.question_id, _state_target(), after_unrelated, store
    )

    target = _state_target()
    proof_premises = state_after.premise_proposition_ids

    def _prove(premise_ids: Sequence[str]) -> SupportStatus:
        return assess_support(
            state_question_.question_id, target, _restricted(after, premise_ids), store
        ).status

    minimality = deletion_test(proof_premises, _prove)

    answer = _answer(
        state_question_,
        state_after,
        "نعم، بابُ الدار مغلقٌ في الفترة المُعلَنة؛ بدليل مشاهدةٍ مستقلّةٍ "
        "نطاقُها يشمل فترةَ السؤال، لا بنفي فتحِ زيد",
    )
    report = verify(state_question_, answer, after, store)
    accepted = report.passed
    if accepted:
        accept(state_question_, answer, report, store, after, bridge.content)

    trace = (
        *bridge.trace,
        TraceItem(
            label="إيداع-المضمون",
            genus=ProvenanceGenus.IMPORTED_FROM_A_SOURCE,
            statement=(
                "مضمونُ العبارة أُودِع قضيّةً منفيّةً بخبرٍ معتمد؛ والمضمونُ "
                "وحدَه لا يُودِع شيئًا"
            ),
        ),
        TraceItem(
            label="حال-الباب-قبل",
            genus=ProvenanceGenus.UNKNOWN,
            statement=A_SILENCE_IS_NOT_A_PROOF,
        ),
        TraceItem(
            label="حال-الباب-بعد",
            genus=ProvenanceGenus.IMPORTED_FROM_A_SOURCE,
            statement=(
                "بعد إيداع مشاهدةٍ مستقلّةٍ لحال الباب في الفترة، حُسِم السؤالُ "
                "داخلَ زمن الدليل وحدَه"
            ),
        ),
    )
    return RunOutcome(
        bridge=bridge,
        occurrence_before=occurrence_before,
        state_before=state_before,
        witness=witness,
        state_after=state_after,
        occurrence_after=occurrence_after,
        state_after_irrelevant_change=state_after_irrelevant_change,
        minimality=minimality,
        report=report,
        accepted=accepted,
        trace=trace,
    )
