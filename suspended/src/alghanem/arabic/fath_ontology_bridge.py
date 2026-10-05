"""الجسرُ من قراءةٍ نحويّةٍ مشتقّةٍ إلى مضمونٍ أنطولوجيّ، بما استقبله وما أضافه.

الجسرُ هنا دالّةٌ من ثلاثةٍ لا من واحد:

    وظيفةٌ نحويّةٌ مقروءة + معنًى معتمدٌ بمصدره + تركيبٌ ونطاق
        ⟵⟶ علاقةٌ أنطولوجيّةٌ محدّدةُ النطاق

**ولا يُنقَل «فاعل» إلى «فاعلِ حدث»** (`NO_LABEL_TRANSPORT_WITHOUT_A_BRIDGE`):
المرفوعُ بعد الفعل في «فُتح البابُ» هو **المفتوح** لا الفاتح؛ ولذلك يُقرَأ
التركيبُ أوّلًا، ثمّ يُسنَد الدور. وكلُّ إسنادٍ يُسجَّل في الأثر: ما جاء من
التحليل، وما جاء من المعجم، وما جاء اصطلاحًا، وما بقي مجهولًا.

**والمسكوتُ عنه ليس منفيًّا** (`SILENCE_IS_NOT_DENIAL`): في المبنيّ للمجهول
دورُ الفاعل **غيرُ مُسمًّى** `UNNAMED_IN_THE_UTTERANCE`، وفي الصيغة السابعة
الدورُ **غيرُ مُصوَّرٍ** في بنية الحدث `ROLE_NOT_PROFILED`؛ وليس واحدٌ منهما
`DENIED_BY_THE_UTTERANCE`. فلا «فُتح» برهانٌ على فاعلٍ بشريٍّ معيَّن، ولا
«انفتح» نفيٌ لوجود سبب.

**ومواضعُ الامتداد مُسمّاةٌ لا مفتوحة** (`THE_EXTENSION_POINTS`): الحالُ
والتمييزُ والمشتقّاتُ والحقيقةُ والمجاز لها مواضعُها هنا، **معلَّقةً** بأسمائها.
وتعارضُ قيدٍ نوعيٍّ لا يُسمّى مجازًا تلقائيًّا: قد يكون خطأ تحليلٍ، أو معنًى
آخرَ للّفظ، أو قولًا غيرَ صحيح؛ وترخيصُ المجاز يحتاج معناه وقرينتَه وعلاقتَه.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Final

from ..ontology import (
    Designation,
    DesignationMethod,
    DiscourseContent,
    EventContent,
    FactRegister,
    FillerStanding,
    Modality,
    NegationScope,
    Polarity,
    RoleFilling,
    Scope,
    SubstanceStore,
    build_event_content,
    content_of_utterance,
    resolve_reference,
)
from .door_domain_deposit import (
    DOOR_AGENT_ROLE_ID,
    DOOR_OPENING_EVENT_ID,
    DOOR_PATIENT_ROLE_ID,
    DOOR_TYPE_ID,
    FORM_VII_EVENT_ID,
    FORM_VII_PATIENT_ROLE_ID,
    HUMAN_TYPE_ID,
)
from .fath_surface_analysis import Construction, SyntacticFunction, UtteranceReading

__all__ = [
    "NO_LABEL_TRANSPORT_WITHOUT_A_BRIDGE",
    "SILENCE_IS_NOT_DENIAL",
    "THE_EXTENSION_POINTS",
    "THE_FATH_ROOT",
    "BridgeError",
    "BridgeResult",
    "ProvenanceGenus",
    "TraceItem",
    "bridge_utterance",
]


class BridgeError(ValueError):
    """رفضٌ بنيويٌّ في الجسر؛ لا حملَ على أقرب تركيب."""


NO_LABEL_TRANSPORT_WITHOUT_A_BRIDGE: Final[str] = (
    "لا يُنقَل وسمٌ نحويٌّ إلى خانةٍ دلاليّةٍ بمجرّد التسمية: «المرفوعُ بعد "
    "الفعل» في المبنيّ للمجهول هو المفتوحُ لا الفاتح؛ والنقلُ يلزمه وزنٌ "
    "وتركيبٌ ومعنًى معتمدٌ ونطاق"
)

SILENCE_IS_NOT_DENIAL: Final[str] = (
    "غيرُ المُسمّى غيرُ المنفيّ: `UNNAMED_IN_THE_UTTERANCE` سكوتُ العبارة عن "
    "شاغلِ دورٍ مُصوَّر، و`ROLE_NOT_PROFILED` خلوُّ بنيةِ الحدث من الدور "
    "أصلًا؛ وليس واحدٌ منهما نفيًا لوجود شاغلٍ في الواقع"
)

THE_EXTENSION_POINTS: Final[tuple[str, ...]] = (
    "الحال: قيدٌ على حاملٍ أو مشاركٍ في سياق؛ ويحتاج تعيينَ حامله ونطاقِه، "
    "وهو معلَّقٌ هنا لأنّ التحليل المشتقَّ لا يُخرِجه بعد",
    "التمييز: يُحدِّد جهةَ إبهامٍ أو قياس، ولا يتحوّل إلى جنسٍ أنطولوجيٍّ " "مستقلّ؛ معلَّقٌ هنا",
    "المصدر والمشتقّ: يُرشِّحان بنيةً دلاليّةً ولا يُثبِتان وقوعَ حدثٍ ولا "
    "مهنةَ حاملٍ ولا هويّتَه؛ معلَّقان هنا",
    "الحقيقة والمجاز: تعارضُ قيدٍ نوعيٍّ ليس مجازًا تلقائيًّا؛ قد يكون خطأ "
    "تحليلٍ أو معنًى آخرَ أو قولًا غيرَ صحيح، وترخيصُ المجاز يحتاج معناه "
    "وقرينتَه وعلاقتَه؛ معلَّقٌ هنا",
)
"""مواضعُ الامتداد مُسمّاةً ومعلَّقةً؛ والتعليقُ تصريحٌ لا صمت."""

THE_FATH_ROOT: Final[tuple[str, ...]] = ("ف", "ت", "ح")
"""الجذرُ الذي يقبله هذا الجسر؛ وغيرُه يُرَدّ باسمه لا يُحمَل عليه."""


class ProvenanceGenus(Enum):
    """من أين جاءت كلُّ معلومةٍ في الأثر؛ مفردةٌ مغلقةٌ فيها عضوُ الجهل."""

    DERIVED_FROM_BYTES = "derived_from_bytes"
    IMPORTED_FROM_A_SOURCE = "imported_from_a_source"
    STIPULATED_FOR_THE_DOMAIN = "stipulated_for_the_domain"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class TraceItem:
    """بندٌ في أثر التشغيل: ما هو، ومن أين جاء، وبأيّ بيان."""

    label: str
    genus: ProvenanceGenus
    statement: str

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى البند للبصمة."""

        return {
            "label": self.label,
            "genus": self.genus.value,
            "statement": self.statement,
        }


@dataclass(frozen=True, slots=True)
class BridgeResult:
    """مخرجُ الجسر: المضمونُ، وأثرُه المُوسَّم، ومواضعُ الامتداد المعلَّقة."""

    content: DiscourseContent
    trace: tuple[TraceItem, ...]
    suspended_extension_points: tuple[str, ...]

    def items_of(self, genus: ProvenanceGenus) -> tuple[TraceItem, ...]:
        """بنودُ الأثر التي جاءت من جنسٍ بعينه."""

        return tuple(item for item in self.trace if item.genus is genus)

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المخرج للبصمة."""

        return {
            "content": self.content.as_canonical_content(),
            "trace": [item.as_canonical_content() for item in self.trace],
            "suspended_extension_points": list(self.suspended_extension_points),
        }


def _designation_for(
    surface: str,
    method: DesignationMethod,
    expected_type_id: str,
    surface_candidates: Mapping[str, Sequence[str]],
    register: FactRegister,
    store: SubstanceStore,
) -> tuple[Designation, TraceItem]:
    offered = tuple(surface_candidates.get(surface, ()))
    probe = Designation(
        surface=surface,
        method=method,
        candidate_individual_ids=offered,
    )
    resolution = resolve_reference(probe, register, store, expected_type_id)
    designation = Designation(
        surface=surface,
        method=method,
        candidate_individual_ids=resolution.candidate_individual_ids,
    )
    if resolution.is_empty:
        genus = ProvenanceGenus.UNKNOWN
        statement = (
            f"«{surface}» لم ينحصر في فردٍ مودَع تحت `{expected_type_id}`؛ "
            "ووجودُ الاسم في الخطاب ليس إثباتًا لوجود فرد"
        )
    elif resolution.is_resolved:
        genus = ProvenanceGenus.IMPORTED_FROM_A_SOURCE
        statement = (
            f"«{surface}» عُيِّن في `{resolution.candidate_individual_ids[0]}` "
            f"بمرشَّحين مستوردين وبشرط النوع `{expected_type_id}`"
        )
    else:
        genus = ProvenanceGenus.UNKNOWN
        statement = (
            f"«{surface}» بقي على {len(resolution.candidate_individual_ids)} "
            "مرشَّحين؛ والمجموعةُ تُحفَظ ولا يُختار منها واحدٌ بلا ترخيص"
        )
    return designation, TraceItem(
        label=f"تعيين:{surface}", genus=genus, statement=statement
    )


def _nominal(reading: UtteranceReading, function: SyntacticFunction) -> str:
    word = reading.function_of(function)
    if word is None:
        raise BridgeError(f"لا كلمةَ بوظيفة `{function.value}` في هذه القراءة")
    return word.surface


def bridge_utterance(
    reading: UtteranceReading,
    store: SubstanceStore,
    register: FactRegister,
    time_scope: Scope,
    surface_candidates: Mapping[str, Sequence[str]],
    bridge_id: str = "جسر-الفتح-١",
) -> BridgeResult:
    """اعبر من القراءة النحويّة إلى مضمونٍ أنطولوجيّ، وسجِّل كلَّ ما أضفتَه.

    المدخل: قراءةٌ مشتقّةٌ من بايتات العبارة، ورصيدٌ وسجلٌّ ونطاقٌ زمنيّ،
        ومرشَّحو إحالةٍ لكلّ سطحٍ اسميّ.
    الشرط: التركيبُ مقروءٌ لا مجهول، وجذرُ الفعل هو `ف ت ح`.
    المخرج: مضمونُ العبارة، وأثرٌ يُميِّز المشتقَّ من المستوردِ من المصطَلحِ من المجهول.
    ما تحفظه: الوظيفةُ النحويّةُ لا تصير دورًا إلّا بالتركيب؛ والسكوتُ لا يصير نفيًا.
    حدُّها: لا تُودِع واقعةً، ولا تحسم مرجعًا لم ينحصر، ولا تفتح مواضعَ الامتداد.
    """

    if reading.construction is Construction.UNRECOGNISED:
        raise BridgeError(
            "تركيبٌ لم تُصِبه قواعدُ القراءة؛ والجسرُ يقف ولا يحمله على أقربِ تركيب"
        )
    verb = reading.verb
    if verb is None or verb.root_letters != THE_FATH_ROOT:
        raise BridgeError(
            "هذا الجسرُ مقصورٌ على جذر `ف ت ح` المشتقِّ من الوزن؛ والفعلُ "
            f"المقروءُ جذرُه {verb.root_letters if verb else ()}"
        )
    trace: list[TraceItem] = [
        TraceItem(
            label="التركيب",
            genus=ProvenanceGenus.DERIVED_FROM_BYTES,
            statement=(
                f"التركيبُ `{reading.construction.value}` مقروءٌ من أوزان الكلمات "
                "وحركاتِ إعرابها، لا من جدولٍ مكتوبٍ بإزاء العبارة"
            ),
        ),
        TraceItem(
            label="جذر-الفعل",
            genus=ProvenanceGenus.DERIVED_FROM_BYTES,
            statement=(
                f"جذرُ الفعل `{' '.join(verb.root_letters)}` مُستخرَجٌ بحذف "
                f"زوائدَ مقروءةٍ من الوزن `{verb.shape.value}`"
            ),
        ),
        TraceItem(
            label="المعنى-المعتمد",
            genus=ProvenanceGenus.IMPORTED_FROM_A_SOURCE,
            statement=(
                "محورُ «خلاف الإغلاق» مستوردٌ من مادّة «فتح» في مقاييس اللغة، "
                "بدليلٍ جنسُه شهادةُ معجمٍ لا يُودِع واقعة"
            ),
        ),
        TraceItem(
            label="تضييق-المعنى",
            genus=ProvenanceGenus.STIPULATED_FOR_THE_DOMAIN,
            statement=(
                "قصرُ المحور على الفتح الحسّيِّ لبابٍ اصطلاحٌ مُعلَنٌ لهذا "
                "المجال، لا قراءةٌ من المعجم"
            ),
        ),
    ]

    polarity = Polarity.AFFIRMED
    negation_scope = NegationScope.NOT_NEGATED
    modality = Modality.ASSERTED
    construction = reading.construction

    if construction is Construction.NEGATED_ACTIVE_TRANSITIVE:
        polarity = Polarity.NEGATED
        negation_scope = NegationScope.WHOLE_EVENT_OCCURRENCE
        trace.append(
            TraceItem(
                label="النفي",
                genus=ProvenanceGenus.DERIVED_FROM_BYTES,
                statement=(
                    "«لَمْ» مقروءةٌ من حركاتها، والفعلُ بعدها مجزومٌ مقروءُ "
                    "الوزن؛ فالمنفيُّ وقوعُ الحدث كلِّه في النطاق، لا شَغْلُ دورٍ بعينه"
                ),
            )
        )
    elif construction is Construction.CONDITIONAL_ACTIVE_TRANSITIVE:
        modality = Modality.CONDITIONAL
        trace.append(
            TraceItem(
                label="الشرط",
                genus=ProvenanceGenus.DERIVED_FROM_BYTES,
                statement=(
                    "«إِنْ» مقروءةٌ من حركاتها؛ والجهةُ شرطيّةٌ، فالعبارةُ لا "
                    "تلتزم بوقوع الحدث ولا بعدمه"
                ),
            )
        )

    fillings: list[RoleFilling] = []
    if construction in (
        Construction.ACTIVE_TRANSITIVE,
        Construction.NEGATED_ACTIVE_TRANSITIVE,
        Construction.CONDITIONAL_ACTIVE_TRANSITIVE,
    ):
        event_type_id = DOOR_OPENING_EVENT_ID
        agent_surface = _nominal(reading, SyntacticFunction.NOMINATIVE_AFTER_VERB)
        patient_surface = _nominal(reading, SyntacticFunction.ACCUSATIVE_AFTER_VERB)
        agent_designation, agent_trace = _designation_for(
            agent_surface,
            DesignationMethod.PROPER_NAME,
            HUMAN_TYPE_ID,
            surface_candidates,
            register,
            store,
        )
        patient_designation, patient_trace = _designation_for(
            patient_surface,
            DesignationMethod.DEFINITE_DESCRIPTION,
            DOOR_TYPE_ID,
            surface_candidates,
            register,
            store,
        )
        trace.extend((agent_trace, patient_trace))
        fillings.append(
            RoleFilling(
                role_id=DOOR_AGENT_ROLE_ID,
                standing=FillerStanding.DESIGNATED,
                designation=agent_designation,
            )
        )
        fillings.append(
            RoleFilling(
                role_id=DOOR_PATIENT_ROLE_ID,
                standing=FillerStanding.DESIGNATED,
                designation=patient_designation,
            )
        )
        trace.append(
            TraceItem(
                label="إسناد-الأدوار",
                genus=ProvenanceGenus.STIPULATED_FOR_THE_DOMAIN,
                statement=(
                    "في المبنيّ للمعلوم المتعدّي: المرفوعُ بعد الفعل شاغلُ "
                    f"`{DOOR_AGENT_ROLE_ID}`، والمنصوبُ شاغلُ "
                    f"`{DOOR_PATIENT_ROLE_ID}`؛ و" + NO_LABEL_TRANSPORT_WITHOUT_A_BRIDGE
                ),
            )
        )
    elif construction is Construction.PASSIVE_ONE_NOMINATIVE:
        event_type_id = DOOR_OPENING_EVENT_ID
        patient_surface = _nominal(reading, SyntacticFunction.NOMINATIVE_AFTER_VERB)
        patient_designation, patient_trace = _designation_for(
            patient_surface,
            DesignationMethod.DEFINITE_DESCRIPTION,
            DOOR_TYPE_ID,
            surface_candidates,
            register,
            store,
        )
        trace.append(patient_trace)
        fillings.append(
            RoleFilling(
                role_id=DOOR_PATIENT_ROLE_ID,
                standing=FillerStanding.DESIGNATED,
                designation=patient_designation,
            )
        )
        fillings.append(
            RoleFilling(
                role_id=DOOR_AGENT_ROLE_ID,
                standing=FillerStanding.UNNAMED_IN_THE_UTTERANCE,
                designation=None,
            )
        )
        trace.append(
            TraceItem(
                label="إسناد-الأدوار",
                genus=ProvenanceGenus.STIPULATED_FOR_THE_DOMAIN,
                statement=(
                    "في المبنيّ للمجهول: المرفوعُ بعد الفعل شاغلُ "
                    f"`{DOOR_PATIENT_ROLE_ID}` لا `{DOOR_AGENT_ROLE_ID}`؛ "
                    "والفاعلُ غيرُ مُسمًّى في العبارة، و" + SILENCE_IS_NOT_DENIAL
                ),
            )
        )
    else:
        event_type_id = FORM_VII_EVENT_ID
        patient_surface = _nominal(reading, SyntacticFunction.NOMINATIVE_AFTER_VERB)
        patient_designation, patient_trace = _designation_for(
            patient_surface,
            DesignationMethod.DEFINITE_DESCRIPTION,
            DOOR_TYPE_ID,
            surface_candidates,
            register,
            store,
        )
        trace.append(patient_trace)
        fillings.append(
            RoleFilling(
                role_id=FORM_VII_PATIENT_ROLE_ID,
                standing=FillerStanding.DESIGNATED,
                designation=patient_designation,
            )
        )
        trace.append(
            TraceItem(
                label="إسناد-الأدوار",
                genus=ProvenanceGenus.STIPULATED_FOR_THE_DOMAIN,
                statement=(
                    f"الصيغةُ السابعةُ تُحيل على `{FORM_VII_EVENT_ID}` وليس في "
                    "بنيته دورُ فاعلٍ أصلًا؛ فالدورُ غيرُ مُصوَّرٍ لا منفيّ، و"
                    + SILENCE_IS_NOT_DENIAL
                ),
            )
        )

    event: EventContent = build_event_content(
        event_type_id=event_type_id,
        role_fillings=fillings,
        time_scope=time_scope,
        polarity=polarity,
        negation_scope=negation_scope,
        modality=modality,
        store=store,
    )
    content = content_of_utterance(
        content_ref=f"مضمون-{reading.utterance_digest[:12]}",
        utterance_digest=reading.utterance_digest,
        bridge_id=bridge_id,
        event=event,
    )
    for point in THE_EXTENSION_POINTS:
        trace.append(
            TraceItem(
                label="موضع-امتداد",
                genus=ProvenanceGenus.UNKNOWN,
                statement=point,
            )
        )
    return BridgeResult(
        content=content,
        trace=tuple(trace),
        suspended_extension_points=THE_EXTENSION_POINTS,
    )
