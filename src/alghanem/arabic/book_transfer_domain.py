"""مجالٌ ثانٍ — نقلُ كتابٍ بين شخصَين — بالعملياتِ نفسِها لا بمحرِّكٍ آخر.

غايةُ هذه الوحدةِ **امتحانُ عموميّة النواة**: هل عملياتُ الرصيد والمضمون
والسجلّ والاستدلال والتحقّق آلةٌ عامّةٌ في نطاقها، أم برنامجٌ خاصٌّ بكلمة «باب»؟
ولذلك لا تُضيف هذه الوحدةُ عمليةً واحدة: تستورد `door` ما تستورده من `arabic`
— وهو الأرضيّةُ وحدَها — ثمّ تستعمل `operations` و`inference` و`question` و
`verification` كما هي.

**والمعجمُ يختلف والآلةُ لا تختلف** (`THE_MACHINERY_IS_SHARED_NOT_THE_LEXICON`):
قواعدُ المعنى هنا غيرُها هناك — لا جذرَ «فتح» ولا صيغةً سابعة — ولكنّ آليّةَ
التطبيق والتتبّع والتحقّق واحدة.

**ومعرفةُ النوع لا تُثبِت وقوعَ حدث** (`KNOWING_A_TYPE_IS_NOT_WITNESSING_AN_EVENT`):
إيداعُ `حدث_نقل` ودورِه ونتيجتِه لا يقول إنّ كتابًا انتقل؛ والانتقالُ قضيّةٌ
تحتاج دليلَها.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from typing import Final

from ..ontology import (
    Declared,
    DesignationMethod,
    EventTypeDefinition,
    Evidence,
    EvidenceGenus,
    ExistenceStanding,
    FactRegister,
    Individual,
    InferenceRule,
    OntologicalKind,
    Polarity,
    Proposition,
    PropositionForm,
    Question,
    QuestionKind,
    RelationDefinition,
    RoleDefinition,
    RuleKind,
    Scope,
    StateDefinition,
    SubstanceStore,
    TypeDefinition,
    assess_support,
    hold_state,
)
from .ontology_domain_foundation import domain_ontology, domain_prior_base

__all__ = [
    "KNOWING_A_TYPE_IS_NOT_WITNESSING_AN_EVENT",
    "THE_BOOK_DOMAIN_SCOPE",
    "THE_MACHINERY_IS_SHARED_NOT_THE_LEXICON",
    "AT_THE_TABLE",
    "BOOK_HOLDING_STATE_ID",
    "BOOK_LOCATION_STATE_ID",
    "BOOK_OWNERSHIP_STATE_ID",
    "IN_THE_SATCHEL",
    "OWNED_BY_FIRST",
    "OWNED_BY_SECOND",
    "THREE_STATES_ARE_NOT_ONE",
    "BOOK_INDIVIDUAL_ID",
    "BOOK_TRANSFER_EVENT_ID",
    "BOOK_TYPE_ID",
    "FIRST_PERSON_ID",
    "HELD_BY_FIRST",
    "HELD_BY_SECOND",
    "SECOND_PERSON_ID",
    "book_holding_question",
    "holding_before_and_after",
    "transfer_observation",
    "book_transfer_store",
    "book_world_register",
]

THE_MACHINERY_IS_SHARED_NOT_THE_LEXICON: Final[str] = (
    "المشتركُ بين المجالَين آليّةُ التطبيق والتتبّع والتحقّق، لا قواعدُ "
    "المعنى: هنا لا جذرَ «فتح» ولا صيغةَ سابعة، ومع ذلك تُستعمَل العملياتُ "
    "نفسُها بلا سطرٍ جديدٍ في المحرِّك"
)

THREE_STATES_ARE_NOT_ONE: Final[str] = (
    "الموضعُ والحيازةُ والملكيّةُ ثلاثُ حالاتٍ لا واحدة: كتابٌ على مائدةِ "
    "زيدٍ قد يكون في حيازة عمرٍو وفي ملكِ ثالث. وقاعدةُ `حدث_نقل` في هذا "
    "النموذج تُعيِّن **الحيازةَ** وحدَها؛ فلا يُستنتَج منها موضعٌ ولا تُقرأ "
    "نقلًا للملكيّة. والملكيّةُ لا تتحرّك إلّا بسببٍ مُعلَنٍ لها، ولا سببَ "
    "لها في هذا الرصيد؛ فتبقى قيمتُها مجهولةً لا منفيّة"
)

KNOWING_A_TYPE_IS_NOT_WITNESSING_AN_EVENT: Final[str] = (
    "إيداعُ نوع الحدث وأدوارِه ونتيجتِه معرفةٌ عن النوع، لا خبرٌ عن فرد: "
    "ومن قرأ وجودَ `حدث_نقل` في الرصيد انتقالًا واقعًا خلط الرصيدَ بالسجلّ"
)

THE_BOOK_DOMAIN_SCOPE: Final[Scope] = Scope(
    domain_id="مجال-الكتب", timeline_id=None, start=None, end=None
)

_TIMELINE: Final[str] = "خطّ-زمن-المجلس"
_DOMAIN: Final[str] = "مجال-الكتب"
_WIDE: Final[Scope] = Scope(domain_id=_DOMAIN, timeline_id=_TIMELINE, start=0, end=100)

BOOK_TYPE_ID: Final[str] = "كتاب"
_PERSON_TYPE_ID: Final[str] = "شخص"
BOOK_HOLDING_STATE_ID: Final[str] = "حال_الحيازة"
BOOK_LOCATION_STATE_ID: Final[str] = "حال_الموضع"
BOOK_OWNERSHIP_STATE_ID: Final[str] = "حال_الملكيّة"
AT_THE_TABLE: Final[str] = "على_المائدة"
IN_THE_SATCHEL: Final[str] = "في_الحقيبة"
OWNED_BY_FIRST: Final[str] = "مِلكُ_الأوّل"
OWNED_BY_SECOND: Final[str] = "مِلكُ_الثاني"
HELD_BY_FIRST: Final[str] = "عند_الأوّل"
HELD_BY_SECOND: Final[str] = "عند_الثاني"
BOOK_TRANSFER_EVENT_ID: Final[str] = "حدث_نقل"

BOOK_INDIVIDUAL_ID: Final[str] = "فرد-الكتاب"
FIRST_PERSON_ID: Final[str] = "فرد-الأوّل"
SECOND_PERSON_ID: Final[str] = "فرد-الثاني"


def _stipulation(evidence_id: str, statement: str) -> Evidence:
    return Evidence(
        evidence_id=evidence_id,
        genus=EvidenceGenus.STIPULATED_DEFINITION,
        statement=statement,
        source_name="اصطلاحُ مجال الكتب المُعلَن",
        scope=THE_BOOK_DOMAIN_SCOPE,
        source_digest=None,
    )


def book_transfer_store(store_id: str = "رصيد-الكتب") -> SubstanceStore:
    """أودِع رصيدَ مجال نقلِ الكتب بالبنى نفسِها التي أُودِع بها مجالُ الأبواب.

    المدخل: مُعرِّفُ رصيد.
    الشرط: كلُّ بندٍ جنسُه من مرشَّحي `O_0` نفسِها، ويُشير إلى دليلٍ قائم.
    المخرج: رصيدٌ ثانٍ تُجرَّب عليه العملياتُ بلا تعديلٍ فيها.
    حدُّها: لا يُودِع فردًا ولا واقعة؛ ومعرفةُ النوع لا تُثبِت وقوعَ حدث.
    """

    types_evidence = _stipulation(
        "اصطلاح-أنواع-الكتب",
        "أنواعُ هذا المجال: شيءٌ، وكتابٌ أخصُّ منه، وشخصٌ؛ والحيازةُ حالٌ "
        "للكتاب قيمتُها عند الأوّل أو عند الثاني لا ثالثَ لهما في هذا النموذج؛ "
        + THREE_STATES_ARE_NOT_ONE,
    )
    events_evidence = _stipulation(
        "اصطلاح-حدث-النقل",
        KNOWING_A_TYPE_IS_NOT_WITNESSING_AN_EVENT
        + "؛ ونوعُ `حدث_نقل` سببيٌّ له ثلاثةُ أدوار: ناقلٌ ومنقولٌ ومتلقٍّ",
    )
    rule_evidence = _stipulation(
        "اصطلاح-قاعدة-أثر-النقل",
        "في هذا النموذج المُعلَن: وقوعُ `حدث_نقل` في فترةٍ يُعيِّن الحيازةَ عند "
        "المتلقّي في تلك الفترة؛ قطعيّةٌ **داخل النموذج** لا في العالَم. "
        "ولا تمسُّ هذه القاعدةُ `حال_الموضع` ولا `حال_الملكيّة` بحال",
    )
    relations_evidence = _stipulation(
        "اصطلاح-علاقات-الكتب",
        "علاقةُ `نوع_من` متعدّيةٌ بالتصريح في هذا المجال أيضًا؛ والتصريحُ "
        "يتكرّر لأنّه لا يُستنتَج من اسم العلاقة",
    )
    evidence = (types_evidence, events_evidence, rule_evidence, relations_evidence)
    types = (
        TypeDefinition(
            type_id="شيء",
            definition="ما يُحاز ويُنقَل في هذا المجال",
            membership_conditions=(),
            evidence_ref=types_evidence.ref,
            scope=THE_BOOK_DOMAIN_SCOPE,
            kind=OntologicalKind.THING,
        ),
        TypeDefinition(
            type_id=BOOK_TYPE_ID,
            definition="شيءٌ مكتوبٌ مجموعٌ يُحاز ويُنقَل",
            membership_conditions=(),
            evidence_ref=types_evidence.ref,
            scope=THE_BOOK_DOMAIN_SCOPE,
            kind=OntologicalKind.THING,
        ),
        TypeDefinition(
            type_id=_PERSON_TYPE_ID,
            definition="حائزٌ قادرٌ على النقل في هذا المجال",
            membership_conditions=(),
            evidence_ref=types_evidence.ref,
            scope=THE_BOOK_DOMAIN_SCOPE,
            kind=OntologicalKind.THING,
        ),
    )
    states = (
        StateDefinition(
            state_id=BOOK_HOLDING_STATE_ID,
            bearer_type_id=BOOK_TYPE_ID,
            mutually_exclusive_values=(HELD_BY_FIRST, HELD_BY_SECOND),
            evidence_ref=types_evidence.ref,
            kind=OntologicalKind.STATE,
        ),
        StateDefinition(
            state_id=BOOK_LOCATION_STATE_ID,
            bearer_type_id=BOOK_TYPE_ID,
            mutually_exclusive_values=(AT_THE_TABLE, IN_THE_SATCHEL),
            evidence_ref=types_evidence.ref,
            kind=OntologicalKind.STATE,
        ),
        StateDefinition(
            state_id=BOOK_OWNERSHIP_STATE_ID,
            bearer_type_id=BOOK_TYPE_ID,
            mutually_exclusive_values=(OWNED_BY_FIRST, OWNED_BY_SECOND),
            evidence_ref=types_evidence.ref,
            kind=OntologicalKind.STATE,
        ),
    )
    event_types = (
        EventTypeDefinition(
            event_type_id=BOOK_TRANSFER_EVENT_ID,
            roles=(
                RoleDefinition(
                    role_id="دور_الناقل",
                    filler_type_id=_PERSON_TYPE_ID,
                    obligatory=False,
                    kind=OntologicalKind.ROLE,
                ),
                RoleDefinition(
                    role_id="دور_المنقول",
                    filler_type_id=BOOK_TYPE_ID,
                    obligatory=True,
                    kind=OntologicalKind.ROLE,
                ),
                RoleDefinition(
                    role_id="دور_المتلقّي",
                    filler_type_id=_PERSON_TYPE_ID,
                    obligatory=False,
                    kind=OntologicalKind.ROLE,
                ),
            ),
            resulting_state_id=BOOK_HOLDING_STATE_ID,
            resulting_state_value=HELD_BY_SECOND,
            is_causative=True,
            evidence_ref=events_evidence.ref,
            kind=OntologicalKind.EVENT,
        ),
    )
    relations = (
        RelationDefinition(
            relation_id="نوع_من",
            domain_type_id="شيء",
            range_type_id="شيء",
            transitive=Declared.YES,
            symmetric=Declared.NO,
            reflexive=Declared.NO,
            justification="الأخصُّ من الأخصِّ أخصُّ، تصريحًا في هذا المجال أيضًا",
            evidence_ref=relations_evidence.ref,
            kind=OntologicalKind.RELATION,
        ),
    )
    rules = (
        InferenceRule(
            rule_id="قاعدة-أثر-النقل",
            version="١",
            kind=RuleKind.STRICT_IN_THE_DECLARED_MODEL,
            premise_patterns=(f"وقع `{BOOK_TRANSFER_EVENT_ID}` في فترةٍ، إثباتًا",),
            conclusion_pattern=(
                f"`{BOOK_HOLDING_STATE_ID}` = `{HELD_BY_SECOND}` في تلك الفترة"
            ),
            applicability_note=("تنطبق على المُثبَت وحدَه؛ والمنفيُّ لا يُستخرَج منه عكسُها"),
            blocker_ids=(),
            evidence_ref=rule_evidence.ref,
        ),
    )
    base = domain_prior_base("pk0-الكتب", "الكتبُ وأحداثُ نقلها وحالاتُ حيازتها")
    return SubstanceStore(
        store_id=store_id,
        ontology=domain_ontology("o0-الكتب", base),
        evidence=evidence,
        types=types,
        subsumptions=(),
        attributes=(),
        states=states,
        parts=(),
        capabilities=(),
        event_types=event_types,
        relations=relations,
        composition_laws=(),
        rules=rules,
    )


def book_world_register() -> FactRegister:
    """أقِم سجلَّ المجلس: كتابٌ وشخصان مُثبَتو الوجود، ولا حالَ حيازةٍ بعد."""

    existence = Evidence(
        evidence_id="مشاهدة-وجود-المجلس",
        genus=EvidenceGenus.DIRECT_OBSERVATION,
        statement="شوهد في المجلس كتابٌ وشخصان",
        source_name="مشاهدةُ هذا العالَم المُعلَن",
        scope=_WIDE,
        source_digest=None,
    )
    register = FactRegister(
        register_id="سجلّ-المجلس",
        evidence=(existence,),
        individuals=(),
        propositions=(),
    )
    for individual_id, type_id in (
        (BOOK_INDIVIDUAL_ID, BOOK_TYPE_ID),
        (FIRST_PERSON_ID, _PERSON_TYPE_ID),
        (SECOND_PERSON_ID, _PERSON_TYPE_ID),
    ):
        register = register.with_individual(
            Individual(
                individual_id=individual_id,
                designation_method=DesignationMethod.DEFINITE_DESCRIPTION,
                candidate_type_ids=(type_id,),
                existence=ExistenceStanding.ESTABLISHED,
                evidence_ref=existence.ref,
            )
        )
    return register


def book_holding_question(scope: Scope) -> Question:
    """سؤالُ الحيازة: هل الكتابُ عند الثاني في الفترة؟"""

    return Question(
        question_id="سؤال-الحيازة",
        text="هل الكتابُ عند الثاني في الفترة المُعلَنة؟",
        kind=QuestionKind.CURRENT_STATE,
        subject_id=BOOK_INDIVIDUAL_ID,
        predicate_id=BOOK_HOLDING_STATE_ID,
        scope=scope,
    )


def _target(value: str, scope: Scope, evidence: Evidence) -> Proposition:
    return Proposition(
        proposition_id="هدف-الحيازة",
        form=PropositionForm.STATE_HOLDS,
        subject_id=BOOK_INDIVIDUAL_ID,
        predicate_id=BOOK_HOLDING_STATE_ID,
        value=value,
        polarity=Polarity.AFFIRMED,
        scope=scope,
        evidence_ref=evidence.ref,
    )


def transfer_observation(value: str, scope: Scope) -> Evidence:
    """دليلُ مشاهدةٍ لحال الحيازة في فترةٍ، بالصنف نفسِه المستعمَل في الأبواب."""

    return Evidence(
        evidence_id="مشاهدة-حال-الحيازة",
        genus=EvidenceGenus.DIRECT_OBSERVATION,
        statement=f"شوهد الكتابُ «{value}» في الفترة المُعلَنة",
        source_name="مشاهدةُ هذا العالَم المُعلَن",
        scope=scope,
        source_digest=None,
    )


def holding_before_and_after(scope: Scope) -> tuple[str, str]:
    """شغِّل العملياتِ نفسَها على المجال الثاني، وأخرِج الحكمَ قبل الدليل وبعده.

    المدخل: فترةُ السؤال.
    الشرط: لا شيء؛ العالَمُ والرصيدُ مُعلَنان هنا.
    المخرج: حالا الحكم قبل إيداع دليل الحيازة وبعده.
    حدُّها: لا تُضيف عمليةً؛ وهذا عينُ المقصود من المجال الثاني.
    """

    store = book_transfer_store()
    register = book_world_register()
    question = book_holding_question(scope)
    probe = transfer_observation(HELD_BY_SECOND, _WIDE)
    before = assess_support(
        question.question_id,
        _target(HELD_BY_SECOND, scope, probe),
        register.with_evidence(probe),
        store,
    )
    observation = transfer_observation(HELD_BY_SECOND, scope)
    after_register = hold_state(
        individual_id=BOOK_INDIVIDUAL_ID,
        state_id=BOOK_HOLDING_STATE_ID,
        value=HELD_BY_SECOND,
        scope=scope,
        evidence=observation,
        proposition_id="قضيّة-حال-الحيازة",
        register=register,
        store=store,
    )
    after = assess_support(
        question.question_id,
        _target(HELD_BY_SECOND, scope, observation),
        after_register,
        store,
    )
    return before.status.value, after.status.value
