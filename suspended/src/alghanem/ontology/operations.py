"""العمليّاتُ الأنطولوجيّة: لكلّ واحدةٍ مدخلٌ وشرطٌ ومخرجٌ وما تحفظه وما تُضيفه.

الأصنافُ وحدَها لا تُفسِّر شيئًا؛ وههنا **ما يُنفَّذ فعلًا**:

| العمليّة | ما تُضيفه | مصدرُ الإضافة | حدُّها |
|---|---|---|---|
| `resolve_reference` | حصرُ مرشَّحين أو إبقاؤهم | سجلُّ الأفراد | لا تختار واحدًا من متعدّد |
| `check_membership` | حكمُ انتماءٍ بحال قيمة | شروطُ النوع المنفَّذة | لا تُكمِل شرطًا غائبًا |
| `compose_relations` | علاقةٌ ناتجة | رخصةُ تركيبٍ مُسمّاة | لا تركيبَ بلا رخصة |
| `hold_state` | قضيّةُ حالٍ على فترة | دليلٌ يُثبِت | لا تتجاوز فترةَ دليلها |
| `build_event_content` | مضمونُ حدث | تحليلٌ + معنًى معتمد | لا تُسنِد دورًا لم يرد |
| `apply_rule` | قضيّةٌ مُستنتَجة بسندها | قاعدةٌ بإصدارها | تقف عند أوّل مانع |
| `recompute_after_evidence_change` | تعليقُ التابع | تغيّرُ البصمة | التابعُ وحدَه |

**ولا قاعدةَ عامّةً تنقل بين الوصلات** (`NO_CROSS_GENUS_TRANSPORT`): «جزءٌ من»
لا تصير «فردًا من»، و«يتّصف بـ» لا تصير «نوعًا من»؛ والتركيبُ لا يقع إلّا
برخصةٍ تُسمّي العلاقتين والناتجةَ بأعيانها.

**ولا تعدٍّ بلا إعلان** (`NO_TRANSITIVITY_WITHOUT_A_DECLARATION`): خاصّيّةٌ
`UNDECLARED` تمنع الاستعمالَ ولا تُقرَأ نفيًا.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Final

from .content import (
    Designation,
    DiscourseContent,
    EventContent,
    Modality,
    NegationScope,
    Polarity,
    RoleFilling,
)
from .epistemics import Evidence, Scope, ValueStatus
from .facts import FactRegister, Proposition, PropositionForm
from .substance import Declared, InferenceRule, MembershipTest, SubstanceStore

__all__ = [
    "AN_OPERATION_NAMES_WHAT_IT_ADDS",
    "NO_CROSS_GENUS_TRANSPORT",
    "NO_TRANSITIVITY_WITHOUT_A_DECLARATION",
    "MembershipVerdict",
    "OperationError",
    "ReferenceResolution",
    "RelationComposition",
    "RuleApplication",
    "apply_rule",
    "content_of_utterance",
    "build_event_content",
    "compose_relations",
    "hold_state",
    "recompute_after_evidence_change",
    "refuse_part_as_instance",
    "resolve_reference",
    "check_membership",
    "transitive_closure",
]


class OperationError(ValueError):
    """رفضٌ بنيويٌّ في عمليّةٍ أنطولوجيّة؛ لا حملَ على أقرب حالة."""


NO_CROSS_GENUS_TRANSPORT: Final[str] = (
    "لا نقلَ بين أجناس الوصلات: «جزءٌ من» لا تصير «فردًا من»، و«يتّصف بـ» لا "
    "تصير «نوعًا من»؛ ومن ركّب وصلتين بلا رخصةٍ تُسمّيهما والناتجةَ جمعَهما "
    "تحت وصلةٍ عامّةٍ ثمّ استدلّ بها"
)

NO_TRANSITIVITY_WITHOUT_A_DECLARATION: Final[str] = (
    "لا تعدٍّ ولا تماثلَ بلا إعلان: خاصّيّةٌ غيرُ مُعلَنةٍ تمنع الاستعمال ولا "
    "تُقرَأ نفيًا، واستنتاجُها من اسم العلاقة قراءةٌ للّفظ مكان القاعدة"
)

AN_OPERATION_NAMES_WHAT_IT_ADDS: Final[str] = (
    "العمليّةُ تُسمّي ما أضافته ومن أين: مخرجٌ لا يُميِّز المستوردَ من المشتقِّ "
    "من المفترضِ من المجهول يُسلِّم للقارئ حكمًا لا يستطيع مراجعتَه"
)


@dataclass(frozen=True, slots=True)
class ReferenceResolution:
    """مخرجُ التعيين: المرشَّحون الباقون، وما أسقطه، وهل انحصر في واحد."""

    surface: str
    candidate_individual_ids: tuple[str, ...]
    excluded_individual_ids: tuple[str, ...]
    exclusion_reason: str

    @property
    def is_resolved(self) -> bool:
        """أانحصر في فردٍ واحد؟ والصفرُ والمتعدّدُ يُسمَّيان ولا يُبتلَعان."""

        return len(self.candidate_individual_ids) == 1

    @property
    def is_empty(self) -> bool:
        """أخلا من كلّ مرشَّح؟ منزلةٌ مُسمّاةٌ لا تُقرَأ حصرًا."""

        return not self.candidate_individual_ids


def resolve_reference(
    designation: Designation,
    register: FactRegister,
    store: SubstanceStore,
    expected_type_id: str | None = None,
) -> ReferenceResolution:
    """حاصِر مرشَّحي الإحالة بشرط النوع، ولا تختر واحدًا من متعدّدٍ بحال.

    المدخل: تعيينٌ من الخطاب، وسجلُّ أفراد، ورصيدٌ فيه الأنواع.
    الشرط: كلُّ مرشَّحٍ مودَعٌ في السجلّ.
    المخرج: مرشَّحون باقون ومُسقَطون وسببُ الإسقاط.
    ما تحفظه: لا تُنشئ فردًا ولا تُثبِت وجودًا.
    """

    if not isinstance(designation, Designation):
        raise OperationError("التعيينُ تعيينٌ قائمٌ من الخطاب")
    kept: list[str] = []
    dropped: list[str] = []
    for individual_id in designation.candidate_individual_ids:
        individual = register.individual_of(individual_id)
        if expected_type_id is None:
            kept.append(individual_id)
            continue
        expanded: list[str] = []
        for type_id in individual.candidate_type_ids:
            expanded.append(type_id)
            expanded.extend(store.broader_type_ids(type_id))
        if expected_type_id in expanded:
            kept.append(individual_id)
        else:
            dropped.append(individual_id)
    reason = (
        "لا شرطَ نوعٍ مطلوب"
        if expected_type_id is None
        else f"لا يقع تحت النوع `{expected_type_id}` ولا تحت ما يعمّه"
    )
    return ReferenceResolution(
        surface=designation.surface,
        candidate_individual_ids=tuple(kept),
        excluded_individual_ids=tuple(dropped),
        exclusion_reason=reason,
    )


@dataclass(frozen=True, slots=True)
class MembershipVerdict:
    """حكمُ انتماءٍ: حالُ القيمة، والشروطُ المستوفاةُ والمتخلّفةُ والمجهولة."""

    individual_id: str
    type_id: str
    status: ValueStatus
    satisfied_condition_ids: tuple[str, ...]
    failed_condition_ids: tuple[str, ...]
    unknown_condition_ids: tuple[str, ...]

    @property
    def is_member(self) -> bool:
        """أثبت الانتماءُ؟ `KNOWN` مع خلوِّ المتخلِّف والمجهول."""

        return (
            self.status is ValueStatus.KNOWN
            and not self.failed_condition_ids
            and not self.unknown_condition_ids
        )


def check_membership(
    individual_id: str,
    type_id: str,
    register: FactRegister,
    store: SubstanceStore,
) -> MembershipVerdict:
    """اختبِر انتماءَ فردٍ إلى نوعٍ **بشروطه المنفَّذة** لا باسمه.

    المدخل: فردٌ مودَع، ونوعٌ في الرصيد.
    الشرط: للنوع شرطُ انتماءٍ قابلٌ للتنفيذ، وإلّا خرج `DECLARED_ONLY` مجهولًا.
    المخرج: حالُ قيمةٍ وثلاثُ قوائمَ مُسمّاة.
    ما تحفظه: لا تُكمِل شرطًا غائبًا ولا تقرأ السكوتَ استيفاءً.
    """

    individual = register.individual_of(individual_id)
    definition = store.type_of(type_id)
    satisfied: list[str] = []
    failed: list[str] = []
    unknown: list[str] = []
    for condition in definition.membership_conditions:
        if condition.test is MembershipTest.DECLARED_ONLY:
            unknown.append(condition.condition_id)
            continue
        if condition.test is MembershipTest.ATTRIBUTE_EQUALS:
            status = store.attribute_status_for(
                condition.target_id, individual.candidate_type_ids
            )
            if status is ValueStatus.NOT_APPLICABLE:
                failed.append(condition.condition_id)
                continue
            holds = _attribute_value_of(individual_id, condition.target_id, register)
            if holds is None:
                unknown.append(condition.condition_id)
            elif holds == condition.expected_value:
                satisfied.append(condition.condition_id)
            else:
                failed.append(condition.condition_id)
            continue
        if condition.test is MembershipTest.HAS_PART_OF_TYPE:
            if _has_part_of_type(individual_id, condition.target_id, register, store):
                satisfied.append(condition.condition_id)
            else:
                unknown.append(condition.condition_id)
            continue
        if _has_capability(individual_id, condition.target_id, register):
            satisfied.append(condition.condition_id)
        else:
            unknown.append(condition.condition_id)
    if failed:
        status = ValueStatus.KNOWN if not unknown else ValueStatus.DISPUTED
        return MembershipVerdict(
            individual_id=individual_id,
            type_id=type_id,
            status=status,
            satisfied_condition_ids=tuple(satisfied),
            failed_condition_ids=tuple(failed),
            unknown_condition_ids=tuple(unknown),
        )
    if unknown or not definition.has_executable_conditions:
        return MembershipVerdict(
            individual_id=individual_id,
            type_id=type_id,
            status=ValueStatus.UNKNOWN,
            satisfied_condition_ids=tuple(satisfied),
            failed_condition_ids=(),
            unknown_condition_ids=tuple(unknown),
        )
    return MembershipVerdict(
        individual_id=individual_id,
        type_id=type_id,
        status=ValueStatus.KNOWN,
        satisfied_condition_ids=tuple(satisfied),
        failed_condition_ids=(),
        unknown_condition_ids=(),
    )


def _attribute_value_of(
    individual_id: str, attribute_id: str, register: FactRegister
) -> str | None:
    for item in register.active_propositions:
        if (
            item.form is PropositionForm.ATTRIBUTE_VALUE
            and item.subject_id == individual_id
            and item.predicate_id == attribute_id
            and item.polarity is Polarity.AFFIRMED
        ):
            return item.value
    return None


def _has_part_of_type(
    individual_id: str,
    part_type_id: str,
    register: FactRegister,
    store: SubstanceStore,
) -> bool:
    for item in register.active_propositions:
        if (
            item.form is PropositionForm.RELATION_HOLDS
            and item.predicate_id == "جزء_من"
            and item.value == individual_id
            and item.polarity is Polarity.AFFIRMED
        ):
            part = register.individual_of(item.subject_id)
            expanded: list[str] = []
            for type_id in part.candidate_type_ids:
                expanded.append(type_id)
                expanded.extend(store.broader_type_ids(type_id))
            if part_type_id in expanded:
                return True
    return False


def _has_capability(
    individual_id: str, capability_id: str, register: FactRegister
) -> bool:
    for item in register.active_propositions:
        if (
            item.form is PropositionForm.RELATION_HOLDS
            and item.predicate_id == "له_قدرة"
            and item.subject_id == individual_id
            and item.value == capability_id
            and item.polarity is Polarity.AFFIRMED
        ):
            return True
    return False


@dataclass(frozen=True, slots=True)
class RelationComposition:
    """مخرجُ تركيبِ علاقتين: العلاقةُ الناتجةُ إن رُخِّصت، أو سببُ المنع."""

    first_relation_id: str
    second_relation_id: str
    composed_relation_id: str | None
    law_id: str | None
    refusal: str | None

    @property
    def is_licensed(self) -> bool:
        """أوقع التركيبُ برخصة؟ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب."""

        return self.composed_relation_id is not None


def compose_relations(
    first_relation_id: str, second_relation_id: str, store: SubstanceStore
) -> RelationComposition:
    """ركِّب علاقتين **برخصةٍ مُسمّاة** لا بقاعدةٍ عامّة.

    المدخل: علاقتان في الرصيد.
    الشرط: رخصةُ تركيبٍ تُسمّيهما والناتجةَ بأعيانها.
    المخرج: العلاقةُ الناتجةُ ومُعرِّفُ رخصتها، أو سببُ المنع مُسمًّى.
    ما تحفظه: لا تنقل بين أجناس الوصلات.
    """

    store.relation_of(first_relation_id)
    store.relation_of(second_relation_id)
    law = store.composition_law_for(first_relation_id, second_relation_id)
    if law is None:
        return RelationComposition(
            first_relation_id=first_relation_id,
            second_relation_id=second_relation_id,
            composed_relation_id=None,
            law_id=None,
            refusal=NO_CROSS_GENUS_TRANSPORT,
        )
    store.relation_of(law.composed_relation_id)
    return RelationComposition(
        first_relation_id=first_relation_id,
        second_relation_id=second_relation_id,
        composed_relation_id=law.composed_relation_id,
        law_id=law.law_id,
        refusal=None,
    )


def hold_state(
    individual_id: str,
    state_id: str,
    value: str,
    scope: Scope,
    evidence: Evidence,
    proposition_id: str,
    register: FactRegister,
    store: SubstanceStore,
) -> FactRegister:
    """احمِل حالًا على حاملها في **فترةٍ** بعينها، بدليلٍ يُثبِت.

    المدخل: فردٌ، وحالٌ في الرصيد، وقيمةٌ من قيمها، وفترةٌ، ودليل.
    الشرط: الحاملُ من نوع حاملِ الحال، والقيمةُ من قيمها المغلقة.
    المخرج: سجلٌّ جديدٌ فيه قضيّةُ الحال.
    حدُّها: نطاقُ القضيّة لا يتجاوز نطاقَ دليلها، وهذا مفحوصٌ لا موصوف.
    """

    definition = store.state_of(state_id)
    if value not in definition.mutually_exclusive_values:
        raise OperationError(f"`{value}` ليست قيمةً في الحال `{state_id}`؛ والقيمُ مغلقة")
    individual = register.individual_of(individual_id)
    expanded: list[str] = []
    for type_id in individual.candidate_type_ids:
        expanded.append(type_id)
        expanded.extend(store.broader_type_ids(type_id))
    if definition.bearer_type_id not in expanded:
        raise OperationError(
            f"الحالُ `{state_id}` تُحمَل على `{definition.bearer_type_id}`، "
            f"والحاملُ المُقدَّمُ ليس منه"
        )
    if not evidence.scope.covers(scope):
        raise OperationError(
            "نطاقُ القضيّة يتجاوز نطاقَ دليلها: إثباتُ الحال في زمنٍ مشاهَدٍ "
            "غيرُ تعميمها إلى فترةٍ لم تُشاهَد"
        )
    return register.with_evidence(evidence).with_proposition(
        Proposition(
            proposition_id=proposition_id,
            form=PropositionForm.STATE_HOLDS,
            subject_id=individual_id,
            predicate_id=state_id,
            value=value,
            polarity=Polarity.AFFIRMED,
            scope=scope,
            evidence_ref=evidence.ref,
        )
    )


def build_event_content(
    event_type_id: str,
    role_fillings: Sequence[RoleFilling],
    time_scope: Scope,
    polarity: Polarity,
    negation_scope: NegationScope,
    modality: Modality,
    store: SubstanceStore,
    negated_role_id: str | None = None,
) -> EventContent:
    """ابنِ مضمونَ حدثٍ من أدوارٍ **مُسمّاةٍ في الرصيد** لا من أسماءٍ حرّة.

    المدخل: نوعُ حدثٍ في الرصيد، وشواغلُ أدوارٍ، وزمنٌ وقطبيّةٌ وجهة.
    الشرط: كلُّ دورٍ مُسمًّى في نوع الحدث؛ ودورٌ غريبٌ رفضٌ لا تجاوز.
    المخرج: مضمونُ حدثٍ منسوبٌ إلى العبارة.
    ما تحفظه: لا تُسنِد دورًا لم يرد، ولا تقرأ السكوتَ نفيًا.
    """

    definition = store.event_type_of(event_type_id)
    for filling in role_fillings:
        definition.role(filling.role_id)
    return EventContent(
        event_type_id=event_type_id,
        role_fillings=tuple(role_fillings),
        time_scope=time_scope,
        polarity=polarity,
        negation_scope=negation_scope,
        modality=modality,
        negated_role_id=negated_role_id,
    )


@dataclass(frozen=True, slots=True)
class RuleApplication:
    """مخرجُ تطبيق قاعدة: السجلُّ بعده، والمقدّماتُ المستعمَلة، والمانعُ إن وُجد."""

    register: FactRegister
    rule_versioned_id: str
    premise_proposition_ids: tuple[str, ...]
    conclusion_proposition_id: str | None
    blocked_by: str | None

    @property
    def fired(self) -> bool:
        """أأنتجت القاعدةُ قضيّةً؟ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب."""

        return self.conclusion_proposition_id is not None


def apply_rule(
    rule: InferenceRule,
    premise_proposition_ids: Sequence[str],
    conclusion: Proposition,
    register: FactRegister,
    active_blocker_ids: Sequence[str] = (),
) -> RuleApplication:
    """طبِّق قاعدةً بإصدارها على مقدّماتٍ قائمة، وقِف عند أوّل مانعٍ مُسمًّى.

    المدخل: قاعدةٌ، ومُعرِّفاتُ مقدّماتٍ في السجلّ، ونتيجةٌ مصوغة.
    الشرط: كلُّ مقدّمةٍ قائمةٌ غيرُ معلَّقة، ولا مانعَ من موانع القاعدة قائم.
    المخرج: سجلٌّ فيه النتيجةُ **موصولةً بسندها** (مقدّماتٍ وقاعدةً بإصدارها).
    حدُّها: لا تُثبِت المقدّمات، ولا تُرقّي قاعدةً قابلةً للنقض إلى قطعيّة.
    """

    if not isinstance(rule, InferenceRule):
        raise OperationError("القاعدةُ قاعدةٌ قائمةٌ في الرصيد")
    for blocker in active_blocker_ids:
        if blocker in rule.blocker_ids:
            return RuleApplication(
                register=register,
                rule_versioned_id=rule.versioned_id,
                premise_proposition_ids=tuple(premise_proposition_ids),
                conclusion_proposition_id=None,
                blocked_by=blocker,
            )
    for premise_id in premise_proposition_ids:
        premise = register.proposition_of(premise_id)
        if premise.suspended:
            return RuleApplication(
                register=register,
                rule_versioned_id=rule.versioned_id,
                premise_proposition_ids=tuple(premise_proposition_ids),
                conclusion_proposition_id=None,
                blocked_by=f"مقدّمةٌ معلَّقة: `{premise_id}`",
            )
    if conclusion.derived_by_rule != rule.versioned_id:
        raise OperationError(
            "النتيجةُ تحمل قاعدتَها بإصدارها؛ ونتيجةٌ تنسب نفسَها إلى إصدارٍ آخرَ "
            "حكمٌ بلا سند"
        )
    if tuple(conclusion.derived_from_proposition_ids) != tuple(premise_proposition_ids):
        raise OperationError("النتيجةُ تُسمّي مقدّماتِها بأعيانها لا بعضَها")
    return RuleApplication(
        register=register.with_proposition(conclusion),
        rule_versioned_id=rule.versioned_id,
        premise_proposition_ids=tuple(premise_proposition_ids),
        conclusion_proposition_id=conclusion.proposition_id,
        blocked_by=None,
    )


def recompute_after_evidence_change(
    register: FactRegister, evidence: Evidence
) -> FactRegister:
    """حدِّث التابعَ عند تغيّر مضمون دليل: يُعلَّق ما استند إليه وحدَه.

    المدخل: سجلٌّ، ودليلٌ بمضمونٍ جديدٍ ومُعرِّفٍ قائم.
    الشرط: المضمونُ تغيّر فعلًا، فتغيّرت بصمتُه.
    المخرج: سجلٌّ جديدٌ فيه التابعُ معلَّقًا وغيرُه كما هو.
    حدُّها: لا تُسقِط حكمًا لا يستند إلى هذا الدليل.
    """

    return register.amend_evidence(evidence)


def refuse_part_as_instance(relation_id: str) -> None:
    """ارفض أن تُقرَأ «جزءٌ من» «فردًا من»؛ `NO_CROSS_GENUS_TRANSPORT`."""

    if relation_id == "جزء_من":
        raise OperationError(NO_CROSS_GENUS_TRANSPORT)


def transitive_closure(
    relation_id: str, pairs: Sequence[tuple[str, str]], store: SubstanceStore
) -> tuple[tuple[str, str], ...]:
    """أغلِق علاقةً بالتعدّي **إن أُعلِن**؛ وغيرُ المُعلَنِ يُخرِج الأزواجَ كما هي.

    المدخل: علاقةٌ في الرصيد، وأزواجُها المباشرة.
    الشرط: `transitive` مُعلَنةٌ إثباتًا.
    المخرج: الأزواجُ مغلقةً أو كما دخلت، ولا يُقرَأ الثاني إغلاقًا.
    """

    definition = store.relation_of(relation_id)
    if definition.transitive is Declared.UNDECLARED:
        return tuple(pairs)
    if definition.transitive is Declared.NO:
        return tuple(pairs)
    closed = set(pairs)
    changed = True
    while changed:
        changed = False
        for left, middle in tuple(closed):
            for other_left, right in tuple(closed):
                if middle == other_left and (left, right) not in closed:
                    closed.add((left, right))
                    changed = True
    return tuple(sorted(closed))


def content_of_utterance(
    content_ref: str,
    utterance_digest: str,
    bridge_id: str,
    event: EventContent,
) -> DiscourseContent:
    """اجمع مضمونَ الحدث في مضمونِ عبارةٍ منسوبٍ إلى بايتاتها وجسرِه."""

    return DiscourseContent(
        content_ref=content_ref,
        utterance_digest=utterance_digest,
        bridge_id=bridge_id,
        event=event,
    )
