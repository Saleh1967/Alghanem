"""رصيدُ مجالِ الأبواب: أنواعُه وحالاتُه وأحداثُه وأدوارُه وقواعدُه، بمصادرها.

هذا **مضمونُ** الرصيد لا اسمُه: لكلّ بندٍ تعريفٌ وشرطُ انتماءٍ قابلٌ للتنفيذ
حيث أمكن، ومصدرٌ بمنزلة اعتمادٍ ونطاق. والمصادرُ هنا صنفان لا ثالثَ لهما في
الرصيد: شهادةُ معجمٍ مستوردةٌ من المقاييس، واصطلاحاتٌ مُعلَنةٌ لهذا المجال. وكلا
الصنفين **لا يُودِع واقعة**؛ الوقائعُ لها سجلُّها ودليلُها.

**وفتحٌ حدثٌ وانفتاحٌ حدثٌ، والمفتوحُ حالٌ** (`AN_EVENT_IS_NOT_A_STATE`): نوعُ
`حدث_فتح` سببيٌّ له دورُ فاعلٍ **غيرُ لازم** — لأنّ «فُتح البابُ» لا يُسمّيه —
ودورُ متعلَّقٍ لازم. ونوعُ `حدث_انفتاح` **غيرُ سببيٍّ** وليس فيه دورُ فاعلٍ
أصلًا؛ وهذا غيرُ نفيِ وجودِ سبب، بل عدمُ تصويرِه في بنية الحدث.

**وقاعدةُ الاستمرار قابلةٌ للنقض** (`PERSISTENCE_IS_DECLARED_WITH_ITS_BLOCKERS`):
تُودَع `DEFEASIBLE` ومعها موانعُها بأسمائها، فلا تُقرَأ قطعيّةً ولا يُعمَّم بها
حالٌ مشاهَدٌ إلى فترةٍ لم تُشاهَد بلا تصريح.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from typing import Final

from ..ontology import (
    AttributeDefinition,
    CapabilityDefinition,
    CompositionLaw,
    Declared,
    EventTypeDefinition,
    Evidence,
    EvidenceGenus,
    InferenceRule,
    MembershipCondition,
    MembershipTest,
    OntologicalKind,
    PartDefinition,
    RelationDefinition,
    RoleDefinition,
    RuleKind,
    Scope,
    StateDefinition,
    SubstanceStore,
    SubsumptionLink,
    TypeDefinition,
)
from .fath_sense_import import import_sense_of_root, physical_opening_stipulation
from .ontology_domain_foundation import domain_ontology, domain_prior_base

__all__ = [
    "AN_EVENT_IS_NOT_A_STATE",
    "PERSISTENCE_IS_DECLARED_WITH_ITS_BLOCKERS",
    "THE_DOOR_DOMAIN_SCOPE",
    "DOOR_AGENT_ROLE_ID",
    "DOOR_OPENING_EVENT_ID",
    "DOOR_PATIENT_ROLE_ID",
    "DOOR_STATE_ID",
    "DOOR_STATE_OPEN",
    "DOOR_STATE_SHUT",
    "DOOR_TYPE_ID",
    "FORM_VII_EVENT_ID",
    "FORM_VII_PATIENT_ROLE_ID",
    "HUMAN_TYPE_ID",
    "door_domain_store",
]

AN_EVENT_IS_NOT_A_STATE: Final[str] = (
    "الفتحُ حدثٌ، والمفتوحُ حالٌ: الحدثُ يقع في وقتٍ وله مشاركون، والحالُ "
    "تدوم في فترةٍ ولها حامل؛ ونفيُ وقوع الحدث ليس تعيينًا لقيمة الحال، "
    "ولا قيمةُ الحال إخبارًا عن وقوع الحدث"
)

PERSISTENCE_IS_DECLARED_WITH_ITS_BLOCKERS: Final[str] = (
    "استمرارُ الحال قاعدةٌ قابلةٌ للنقض تُودَع بموانعها: حدثٌ يُغيِّر الحال في "
    "الفترة، أو دليلٌ مُعارِضٌ فيها؛ ومن استعملها بلا تصريحٍ بموانعها حوّل "
    "مشاهدةَ لحظةٍ إلى خبرٍ عن فترة"
)

THE_DOOR_DOMAIN_SCOPE: Final[Scope] = Scope(
    domain_id="مجال-الأبواب", timeline_id=None, start=None, end=None
)
"""نطاقُ الرصيد: مجالُ الأبواب بلا زمن؛ فالتعريفاتُ لا تُؤرَّخ، والوقائعُ تُؤرَّخ."""

DOOR_TYPE_ID: Final[str] = "باب"
HUMAN_TYPE_ID: Final[str] = "إنسان"
DOOR_STATE_ID: Final[str] = "حال_الباب"
DOOR_STATE_OPEN: Final[str] = "مفتوح"
DOOR_STATE_SHUT: Final[str] = "مغلق"
DOOR_OPENING_EVENT_ID: Final[str] = "حدث_فتح"
DOOR_AGENT_ROLE_ID: Final[str] = "دور_الفاتح"
DOOR_PATIENT_ROLE_ID: Final[str] = "دور_المفتوح"
FORM_VII_EVENT_ID: Final[str] = "حدث_انفتاح"
FORM_VII_PATIENT_ROLE_ID: Final[str] = "دور_المنفتح"

_FUNCTION_ATTRIBUTE_ID: Final[str] = "صفة_الوظيفة"
_DOOR_FUNCTION_VALUE: Final[str] = "ساترُ منفذٍ يُدار"
_OPENABILITY_ID: Final[str] = "قدرة_الانفتاح"
_LEAF_TYPE_ID: Final[str] = "مصراع"


def _stipulation(evidence_id: str, statement: str) -> Evidence:
    return Evidence(
        evidence_id=evidence_id,
        genus=EvidenceGenus.STIPULATED_DEFINITION,
        statement=statement,
        source_name="اصطلاحُ مجال الأبواب المُعلَن",
        scope=THE_DOOR_DOMAIN_SCOPE,
        source_digest=None,
    )


def door_domain_store(store_id: str = "رصيد-الأبواب") -> SubstanceStore:
    """أودِع رصيدَ مجال الأبواب كاملًا، مؤسَّسًا على `O_0`، بمصادرَ مُسمّاة.

    المدخل: مُعرِّفُ رصيد.
    الشرط: كلُّ بندٍ جنسُه من مرشَّحي `O_0`، ويُشير إلى دليلٍ قائمٍ في الرصيد.
    المخرج: رصيدٌ فيه الأنواعُ والصفاتُ والحالاتُ والأجزاءُ والقدراتُ
        والأحداثُ والعلاقاتُ ورخصُ التركيب والقواعد.
    حدُّها: لا يُودِع فردًا ولا واقعة؛ ولا يقول إنّ في العالَم بابًا.
    """

    sense = import_sense_of_root("فتح", THE_DOOR_DOMAIN_SCOPE)
    narrowing = physical_opening_stipulation(THE_DOOR_DOMAIN_SCOPE)
    types_evidence = _stipulation(
        "اصطلاح-أنواع-الأبواب",
        "أنواعُ هذا المجال: جسمٌ، وبابٌ أخصُّ منه، وإنسانٌ، ومصراعٌ جزءٌ من باب؛ "
        "وشرطُ البابِ صفةُ وظيفةٍ وقدرةُ انفتاحٍ، وكلاهما قابلٌ للتنفيذ",
    )
    events_evidence = _stipulation(
        "اصطلاح-أحداث-الفتح",
        AN_EVENT_IS_NOT_A_STATE + "؛ ولذلك أُودِع `حدث_فتح` سببيًّا بدورِ فاعلٍ غيرِ لازم، و"
        "`حدث_انفتاح` غيرَ سببيٍّ بلا دورِ فاعلٍ أصلًا",
    )
    effect_rule_evidence = _stipulation(
        "اصطلاح-قاعدة-أثر-الفتح",
        "في هذا النموذج المُعلَن: وقوعُ `حدث_فتح` على بابٍ في فترةٍ يُعيِّن قيمةَ "
        "`حال_الباب` مفتوحًا في تلك الفترة؛ وهذه قطعيّةٌ **داخل النموذج** لا في العالَم",
    )
    persistence_rule_evidence = _stipulation(
        "اصطلاح-قاعدة-استمرار-الحال", PERSISTENCE_IS_DECLARED_WITH_ITS_BLOCKERS
    )
    relations_evidence = _stipulation(
        "اصطلاح-علاقات-الأبواب",
        "علاقاتُ هذا المجال: `جزء_من` و`له_قدرة` و`نوع_من`؛ ولكلٍّ خواصُّها "
        "مُعلَنةً على حدة، ولا تُقرَأ من اسمها",
    )
    evidence = (
        sense.evidence,
        narrowing,
        types_evidence,
        events_evidence,
        effect_rule_evidence,
        persistence_rule_evidence,
        relations_evidence,
    )
    types = (
        TypeDefinition(
            type_id="جسم",
            definition="ما له امتدادٌ وموضعٌ في هذا المجال",
            membership_conditions=(),
            evidence_ref=types_evidence.ref,
            scope=THE_DOOR_DOMAIN_SCOPE,
            kind=OntologicalKind.THING,
        ),
        TypeDefinition(
            type_id=DOOR_TYPE_ID,
            definition="جسمٌ ساترُ منفذٍ يُدار، له قدرةُ الانفتاح",
            membership_conditions=(
                MembershipCondition(
                    condition_id="شرط-وظيفة-الباب",
                    test=MembershipTest.ATTRIBUTE_EQUALS,
                    target_id=_FUNCTION_ATTRIBUTE_ID,
                    expected_value=_DOOR_FUNCTION_VALUE,
                ),
                MembershipCondition(
                    condition_id="شرط-قدرة-الانفتاح",
                    test=MembershipTest.HAS_CAPABILITY,
                    target_id=_OPENABILITY_ID,
                    expected_value=None,
                ),
            ),
            evidence_ref=types_evidence.ref,
            scope=THE_DOOR_DOMAIN_SCOPE,
            kind=OntologicalKind.THING,
        ),
        TypeDefinition(
            type_id=_LEAF_TYPE_ID,
            definition="جسمٌ مُدارٌ على محورٍ، يكون جزءًا من باب",
            membership_conditions=(),
            evidence_ref=types_evidence.ref,
            scope=THE_DOOR_DOMAIN_SCOPE,
            kind=OntologicalKind.THING,
        ),
        TypeDefinition(
            type_id=HUMAN_TYPE_ID,
            definition="حاملُ فعلٍ قاصدٍ في هذا المجال",
            membership_conditions=(),
            evidence_ref=types_evidence.ref,
            scope=THE_DOOR_DOMAIN_SCOPE,
            kind=OntologicalKind.THING,
        ),
    )
    subsumptions = (
        SubsumptionLink(
            narrower_type_id=DOOR_TYPE_ID,
            broader_type_id="جسم",
            evidence_ref=types_evidence.ref,
        ),
        SubsumptionLink(
            narrower_type_id=_LEAF_TYPE_ID,
            broader_type_id="جسم",
            evidence_ref=types_evidence.ref,
        ),
    )
    attributes = (
        AttributeDefinition(
            attribute_id=_FUNCTION_ATTRIBUTE_ID,
            applies_to_type_ids=("جسم",),
            value_domain=(_DOOR_FUNCTION_VALUE, "غيرُ ساترِ منفذ"),
            evidence_ref=types_evidence.ref,
            kind=OntologicalKind.ATTRIBUTE,
        ),
    )
    states = (
        StateDefinition(
            state_id=DOOR_STATE_ID,
            bearer_type_id=DOOR_TYPE_ID,
            mutually_exclusive_values=(DOOR_STATE_OPEN, DOOR_STATE_SHUT),
            evidence_ref=types_evidence.ref,
            kind=OntologicalKind.STATE,
        ),
    )
    parts = (
        PartDefinition(
            part_id="جزء-المصراع",
            part_type_id=_LEAF_TYPE_ID,
            whole_type_id=DOOR_TYPE_ID,
            sense="جزءٌ تركيبيٌّ قائمٌ ما دام البابُ قائمًا",
            evidence_ref=types_evidence.ref,
            kind=OntologicalKind.THING,
        ),
    )
    capabilities = (
        CapabilityDefinition(
            capability_id=_OPENABILITY_ID,
            bearer_type_id=DOOR_TYPE_ID,
            enables_event_type_id=DOOR_OPENING_EVENT_ID,
            evidence_ref=types_evidence.ref,
        ),
    )
    event_types = (
        EventTypeDefinition(
            event_type_id=DOOR_OPENING_EVENT_ID,
            roles=(
                RoleDefinition(
                    role_id=DOOR_AGENT_ROLE_ID,
                    filler_type_id=HUMAN_TYPE_ID,
                    obligatory=False,
                    kind=OntologicalKind.ROLE,
                ),
                RoleDefinition(
                    role_id=DOOR_PATIENT_ROLE_ID,
                    filler_type_id=DOOR_TYPE_ID,
                    obligatory=True,
                    kind=OntologicalKind.ROLE,
                ),
            ),
            resulting_state_id=DOOR_STATE_ID,
            resulting_state_value=DOOR_STATE_OPEN,
            is_causative=True,
            evidence_ref=events_evidence.ref,
            kind=OntologicalKind.EVENT,
        ),
        EventTypeDefinition(
            event_type_id=FORM_VII_EVENT_ID,
            roles=(
                RoleDefinition(
                    role_id=FORM_VII_PATIENT_ROLE_ID,
                    filler_type_id=DOOR_TYPE_ID,
                    obligatory=True,
                    kind=OntologicalKind.ROLE,
                ),
            ),
            resulting_state_id=DOOR_STATE_ID,
            resulting_state_value=DOOR_STATE_OPEN,
            is_causative=False,
            evidence_ref=events_evidence.ref,
            kind=OntologicalKind.EVENT,
        ),
    )
    relations = (
        RelationDefinition(
            relation_id="جزء_من",
            domain_type_id="جسم",
            range_type_id="جسم",
            transitive=Declared.YES,
            symmetric=Declared.NO,
            reflexive=Declared.NO,
            justification=(
                "الجزئيّةُ التركيبيّةُ في هذا المجال متعدّيةٌ بالتصريح: جزءُ "
                "المصراعِ جزءٌ من الباب؛ ولا تُقرَأ هذه الخاصّيّةُ من اسم العلاقة"
            ),
            evidence_ref=relations_evidence.ref,
            kind=OntologicalKind.RELATION,
        ),
        RelationDefinition(
            relation_id="له_قدرة",
            domain_type_id="جسم",
            range_type_id="جسم",
            transitive=Declared.NO,
            symmetric=Declared.NO,
            reflexive=Declared.NO,
            justification="حملُ القدرةِ على حاملها ليس متعدّيًا ولا متماثلًا",
            evidence_ref=relations_evidence.ref,
            kind=OntologicalKind.RELATION,
        ),
        RelationDefinition(
            relation_id="نوع_من",
            domain_type_id="جسم",
            range_type_id="جسم",
            transitive=Declared.YES,
            symmetric=Declared.NO,
            reflexive=Declared.NO,
            justification="الأخصُّ من الأخصِّ أخصُّ، تصريحًا لا استنتاجًا من الاسم",
            evidence_ref=relations_evidence.ref,
            kind=OntologicalKind.RELATION,
        ),
    )
    composition_laws = (
        CompositionLaw(
            law_id="قانون-تركيب-الجزئيّة",
            first_relation_id="جزء_من",
            second_relation_id="جزء_من",
            composed_relation_id="جزء_من",
            justification=(
                "تركيبُ الجزئيّةِ بالجزئيّةِ جزئيّةٌ في هذا المجال؛ ولا قانونَ "
                "يُركِّب `جزء_من` بـ`نوع_من`، فلا يُنقَل الجزءُ فردًا لنوع الكلّ"
            ),
            evidence_ref=relations_evidence.ref,
        ),
    )
    rules = (
        InferenceRule(
            rule_id="قاعدة-أثر-الفتح",
            version="١",
            kind=RuleKind.STRICT_IN_THE_DECLARED_MODEL,
            premise_patterns=(
                f"وقع `{DOOR_OPENING_EVENT_ID}` على بابٍ في فترةٍ، إثباتًا",
            ),
            conclusion_pattern=f"`{DOOR_STATE_ID}` = `{DOOR_STATE_OPEN}` في تلك الفترة",
            applicability_note=(
                "تنطبق على القضايا المُثبَتةِ وحدَها؛ والمنفيُّ لا يُطبَّق عليه "
                "هذا الأثرُ ولا عكسُه، و" + AN_EVENT_IS_NOT_A_STATE
            ),
            blocker_ids=(),
            evidence_ref=effect_rule_evidence.ref,
        ),
        InferenceRule(
            rule_id="قاعدة-استمرار-الحال",
            version="١",
            kind=RuleKind.DEFEASIBLE,
            premise_patterns=(f"`{DOOR_STATE_ID}` = قيمةٌ في فترةٍ سابقة",),
            conclusion_pattern=f"`{DOOR_STATE_ID}` = القيمةُ نفسُها في فترةٍ لاحقة",
            applicability_note=PERSISTENCE_IS_DECLARED_WITH_ITS_BLOCKERS,
            blocker_ids=(
                "مانع-حدثٌ-مغيِّرٌ-في-الفترة",
                "مانع-دليلٌ-معارضٌ-في-الفترة",
            ),
            evidence_ref=persistence_rule_evidence.ref,
        ),
    )
    base = domain_prior_base("pk0-الأبواب", "الأبوابُ وأحداثُ فتحها وحالاتُها")
    return SubstanceStore(
        store_id=store_id,
        ontology=domain_ontology("o0-الأبواب", base),
        evidence=evidence,
        types=types,
        subsumptions=subsumptions,
        attributes=attributes,
        states=states,
        parts=parts,
        capabilities=capabilities,
        event_types=event_types,
        relations=relations,
        composition_laws=composition_laws,
        rules=rules,
    )
