"""رصيدُ الأنواع والقواعد: ما الذي يعرفه المحرِّكُ عن الأشياء قبل أن يسمع كلامًا.

هذا **المستوى الأوّل** من ثلاثة (رصيدٌ ← مضمونُ خطابٍ ← قضايا مقبولة). ويُبنى
على `O_0` القائمة لا بجانبها: كلُّ بندٍ هنا يُسمّي `OntologicalKind` مُسجَّلًا
في `GeneralOntology` المُؤسَّسة على `PK_0`، فإن لم يكن المرشَّحُ مُسجَّلًا
هناك رُفِض البندُ عند الإنشاء (`NO_ENTRY_OUTSIDE_THE_FOUNDED_CANDIDATES`).
وبهذا لا يكون هذا دفترًا ثانيًا يُكتَب بجانب الأوّل، بل تنفيذًا لقاعدةٍ
مُعتمَدةٍ هناك: `FOUNDING_A_KIND != APPLYING_A_FOUNDED_KIND`.

**وشرطُ الانتماء يُنفَّذ لا يُوصَف** (`A_MEMBERSHIP_CONDITION_IS_EXECUTED`):
`TypeDefinition.membership_conditions` بنودٌ تُختبَر على إسنادات الفرد، فتُخرِج
`KNOWN`/`UNKNOWN`/`DISPUTED`/`NOT_APPLICABLE`؛ ونوعٌ بلا شرطٍ قابلٍ للاختبار
يُصرَّح بذلك في حقلٍ مُلزَم ولا يُقرَأ انتماؤه مُستوفًى بالسهو.

**وخواصُّ العلاقة تُعلَن ولا تُستنتَج من اسمها**
(`A_RELATION_PROPERTY_IS_DECLARED_NOT_READ_OFF_ITS_NAME`): التعدّي والتماثلُ
والانعكاسُ ثلاثةُ حقولٍ ثلاثيّةِ القيمة (`نعم`/`لا`/`غيرُ مُعلَن`)، والمحرِّكُ
يرفض أن يستعمل خاصّيّةً `غيرَ مُعلَنة`. وتركيبُ علاقتين لا يقع إلّا برخصةِ
تركيبٍ مُسمّاةٍ بعينها (`CompositionLaw`)، فلا قاعدةَ عامّةً تحوِّل «جزءٌ من»
إلى «فردٌ من».

**ولكلّ بندٍ مصدرٌ ومنزلةٌ ونطاق**: `Evidence` من `epistemics`، ومضمونُ
المعلومة مُلزَمٌ فيه؛ فاسمُ المصدر وحدَه لا يُنشئ بندًا.

**وتعريفُ النوع ليس إثباتًا لفردٍ** (`A_TYPE_IS_NOT_AN_INSTANCE`): هذا المستوى
لا يحمل أفرادًا البتّة؛ الأفرادُ في `facts`، وهذا هو الفصلُ بعينه.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from .epistemics import EpistemicError, Evidence, EvidenceRef, Scope, ValueStatus
from .general import GeneralOntology, OntologicalKind

__all__ = [
    "A_MEMBERSHIP_CONDITION_IS_EXECUTED",
    "A_RELATION_PROPERTY_IS_DECLARED_NOT_READ_OFF_ITS_NAME",
    "A_TYPE_IS_NOT_AN_INSTANCE",
    "FOUNDING_A_KIND_IS_NOT_APPLYING_A_FOUNDED_KIND",
    "NO_ENTRY_OUTSIDE_THE_FOUNDED_CANDIDATES",
    "AttributeDefinition",
    "CapabilityDefinition",
    "CompositionLaw",
    "Declared",
    "EventTypeDefinition",
    "InferenceRule",
    "MembershipCondition",
    "MembershipTest",
    "PartDefinition",
    "RelationDefinition",
    "RoleDefinition",
    "RuleKind",
    "StateDefinition",
    "SubstanceError",
    "SubstanceStore",
    "SubsumptionLink",
    "TypeDefinition",
]


class SubstanceError(ValueError):
    """رفضٌ بنيويٌّ في رصيد الأنواع والقواعد؛ لا حملَ على أقرب حالة."""


NO_ENTRY_OUTSIDE_THE_FOUNDED_CANDIDATES: Final[str] = (
    "لا بندَ في الرصيد خارج المرشَّحين المُؤسَّسين: كلُّ نوعٍ وصفةٍ وحالةٍ "
    "وحدثٍ وعلاقةٍ يُسمّي مرشَّحَه في `O_0`، ومن أودع بندًا بلا مرشَّحٍ "
    "مُسجَّلٍ أنشأ دفترًا ثانيًا لا يحكمه ما يحكم الأوّل"
)

FOUNDING_A_KIND_IS_NOT_APPLYING_A_FOUNDED_KIND: Final[str] = (
    "تأسيسُ القاعدة غيرُ تنفيذِ قاعدةٍ معتمدة: `O_0` تقول أيّ المرشَّحين "
    "ضروريٌّ غيرُ مُختزَل، وهذه الطبقةُ تُنفِّذ ما اعتُمِد هناك على موادَّ "
    "بعينها؛ فليست سلطةً ثانية ولا دفترًا موازيًا"
)

A_MEMBERSHIP_CONDITION_IS_EXECUTED: Final[str] = (
    "شرطُ الانتماء يُنفَّذ لا يُوصَف: نوعٌ شرطُه نثرٌ لا يُختبَر لا يُقال فيه "
    "«انتمى» ولا «لم ينتمِ»، ويُصرَّح بذلك في حقله ولا يُطوى"
)

A_RELATION_PROPERTY_IS_DECLARED_NOT_READ_OFF_ITS_NAME: Final[str] = (
    "خاصّيّةُ العلاقة تُعلَن ولا تُقرَأ من اسمها: التعدّي والتماثلُ "
    "والانعكاسُ تُسأل عن كلّ علاقةٍ على حدة، و`غيرُ مُعلَن` عضوٌ مُصرَّحٌ به "
    "يمنع الاستعمالَ ولا يُقرَأ نفيًا"
)

A_TYPE_IS_NOT_AN_INSTANCE: Final[str] = (
    "تعريفُ النوع ليس إثباتًا لفردٍ منه: معرفةُ ما الباب لا تُثبِت أنّ بابًا "
    "بعينه موجود، ومعرفةُ شروط الفتح لا تُثبِت أنّ فتحًا وقع"
)


class Declared(Enum):
    """ثلاثيّةُ الإعلان: مُعلَنٌ إثباتًا، أو نفيًا، أو غيرُ مُعلَنٍ أصلًا."""

    YES = "yes"
    NO = "no"
    UNDECLARED = "undeclared"

    @property
    def is_usable(self) -> bool:
        """أيصلح استعمالُ هذه الخاصّيّة في استدلال؟ `غيرُ المُعلَن` لا يُستعمَل."""

        return self is not Declared.UNDECLARED


class MembershipTest(Enum):
    """جنسُ شرط الانتماء القابل للتنفيذ؛ ولكلٍّ منها دالّةُ اختبارٍ منفَّذة."""

    ATTRIBUTE_EQUALS = "attribute_equals"
    HAS_PART_OF_TYPE = "has_part_of_type"
    HAS_CAPABILITY = "has_capability"
    DECLARED_ONLY = "declared_only"


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SubstanceError(f"{label} نصٌّ غير فارغ")
    return value


def _require_evidence(value: object, label: str) -> Evidence:
    if not isinstance(value, Evidence):
        raise SubstanceError(f"{label} دليلٌ قائمٌ لا اسمٌ حرّ")
    if not value.genus.is_substance_founding:
        raise SubstanceError(
            f"{label} دليلٌ جنسُه غيرُ مقروء، ولا يُؤسَّس بندٌ على جنسٍ لم يُقرَأ"
        )
    return value


def _require_kind(
    value: object, allowed: tuple[OntologicalKind, ...]
) -> OntologicalKind:
    if not isinstance(value, OntologicalKind):
        raise SubstanceError(
            "مرشَّحُ البند عضوٌ في مفردة `O_0` المغلقة؛ و"
            + NO_ENTRY_OUTSIDE_THE_FOUNDED_CANDIDATES
        )
    if value not in allowed:
        raise SubstanceError(
            "مرشَّحُ البند خارج ما يسمح به جنسُه: المسموحُ "
            + "، ".join(kind.value for kind in allowed)
        )
    return value


@dataclass(frozen=True, slots=True)
class MembershipCondition:
    """شرطُ انتماءٍ واحدٌ **قابلٌ للتنفيذ**: جنسُه، وحاملُه، والقيمةُ المطلوبة."""

    condition_id: str
    test: MembershipTest
    target_id: str
    expected_value: str | None = None

    def __post_init__(self) -> None:
        _require_text(self.condition_id, "مُعرِّفُ شرط الانتماء")
        if not isinstance(self.test, MembershipTest):
            raise SubstanceError(
                "جنسُ شرط الانتماء عضوٌ في مفردته المغلقة؛ و"
                + A_MEMBERSHIP_CONDITION_IS_EXECUTED
            )
        _require_text(self.target_id, "حاملُ شرط الانتماء")
        if self.test is MembershipTest.ATTRIBUTE_EQUALS:
            _require_text(self.expected_value, "القيمةُ المطلوبة في شرط المساواة")
        elif self.expected_value is not None:
            raise SubstanceError("قيمةٌ مطلوبةٌ في شرطٍ لا يقارن قيمةً: حقلٌ يُكتَب ولا يُقرَأ")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الشرط للبصمة."""

        return {
            "condition_id": self.condition_id,
            "test": self.test.value,
            "target_id": self.target_id,
            "expected_value": self.expected_value,
        }


@dataclass(frozen=True, slots=True)
class TypeDefinition:
    """نوعٌ واحد: تعريفُه نصًّا، وشروطُ انتمائه منفَّذةً، ومصدرُه ونطاقُه."""

    type_id: str
    definition: str
    membership_conditions: tuple[MembershipCondition, ...]
    evidence_ref: EvidenceRef
    scope: Scope
    kind: OntologicalKind = OntologicalKind.THING

    def __post_init__(self) -> None:
        _require_text(self.type_id, "مُعرِّفُ النوع")
        _require_text(self.definition, "تعريفُ النوع")
        if not isinstance(self.membership_conditions, tuple):
            raise SubstanceError("شروطُ الانتماء صفٌّ مجمَّد")
        for condition in self.membership_conditions:
            if not isinstance(condition, MembershipCondition):
                raise SubstanceError("عضوٌ في شروط الانتماء خارج نوعه")
        if not isinstance(self.evidence_ref, EvidenceRef):
            raise SubstanceError("مصدرُ النوع إشارةٌ مبصومةٌ لا اسمٌ حرّ")
        if not isinstance(self.scope, Scope):
            raise SubstanceError("نطاقُ النوع نطاقٌ قائم")
        _require_kind(self.kind, (OntologicalKind.THING, OntologicalKind.EVENT))

    @property
    def has_executable_conditions(self) -> bool:
        """أله شرطُ انتماءٍ قابلٌ للتنفيذ؟ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب."""

        return any(
            condition.test is not MembershipTest.DECLARED_ONLY
            for condition in self.membership_conditions
        )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى النوع للبصمة."""

        return {
            "type_id": self.type_id,
            "definition": self.definition,
            "kind": self.kind.value,
            "membership_conditions": [
                condition.as_canonical_content()
                for condition in self.membership_conditions
            ],
            "evidence_ref": self.evidence_ref.as_canonical_content(),
            "scope": self.scope.as_canonical_content(),
        }


@dataclass(frozen=True, slots=True)
class SubsumptionLink:
    """«نوعٌ من»: نوعٌ أخصُّ تحت نوعٍ أعمّ، بمصدرٍ مُسمًّى.

    وهذه الوصلةُ **ليست** «فردٌ من» ولا «جزءٌ من»؛ وجمعُها بهما هو ما يُفقِد
    المحرِّكَ القدرةَ على منعِ انتقالِ الصنف.
    """

    narrower_type_id: str
    broader_type_id: str
    evidence_ref: EvidenceRef

    def __post_init__(self) -> None:
        _require_text(self.narrower_type_id, "النوعُ الأخصّ")
        _require_text(self.broader_type_id, "النوعُ الأعمّ")
        if self.narrower_type_id == self.broader_type_id:
            raise SubstanceError("النوعُ ليس أخصَّ من نفسه في هذه الوصلة")
        if not isinstance(self.evidence_ref, EvidenceRef):
            raise SubstanceError("مصدرُ الوصلة إشارةٌ مبصومة")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الوصلة للبصمة."""

        return {
            "narrower_type_id": self.narrower_type_id,
            "broader_type_id": self.broader_type_id,
            "evidence_ref": self.evidence_ref.as_canonical_content(),
        }


@dataclass(frozen=True, slots=True)
class AttributeDefinition:
    """صفةٌ واحدة: حواملُها المسموحة، ومجالُ قيمها المغلق، ومصدرُها.

    وقيدُ الانطباق مُنفَّذ: صفةٌ تُحمَل على نوعٍ ليس في `applies_to_type_ids`
    تُخرِج `NOT_APPLICABLE` لا `UNKNOWN`، على معنى
    `NO_RECORDED_VALUE_IS_NOT_A_RECORDED_ABSENCE`.
    """

    attribute_id: str
    applies_to_type_ids: tuple[str, ...]
    value_domain: tuple[str, ...]
    evidence_ref: EvidenceRef
    kind: OntologicalKind = OntologicalKind.ATTRIBUTE

    def __post_init__(self) -> None:
        _require_text(self.attribute_id, "مُعرِّفُ الصفة")
        if not self.applies_to_type_ids:
            raise SubstanceError("الصفةُ تُسمّي حواملَها؛ وصفةٌ بلا حاملٍ صفةٌ لكلّ شيء")
        if not self.value_domain:
            raise SubstanceError("مجالُ قيم الصفة مغلقٌ غيرُ فارغ")
        if len(set(self.value_domain)) != len(self.value_domain):
            raise SubstanceError("قيمةٌ مكرَّرةٌ في مجال الصفة تُرفَض لا تُطوى")
        if not isinstance(self.evidence_ref, EvidenceRef):
            raise SubstanceError("مصدرُ الصفة إشارةٌ مبصومة")
        _require_kind(self.kind, (OntologicalKind.ATTRIBUTE, OntologicalKind.QUANTITY))

    def applies_to(self, type_ids: Sequence[str]) -> bool:
        """أتنطبق هذه الصفةُ على حاملٍ أنواعُه المُعطاة؟"""

        return any(type_id in self.applies_to_type_ids for type_id in type_ids)

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الصفة للبصمة."""

        return {
            "attribute_id": self.attribute_id,
            "kind": self.kind.value,
            "applies_to_type_ids": list(self.applies_to_type_ids),
            "value_domain": list(self.value_domain),
            "evidence_ref": self.evidence_ref.as_canonical_content(),
        }


@dataclass(frozen=True, slots=True)
class StateDefinition:
    """حالٌ واحدة: حاملُها، وقيمُها المتعاقبةُ المتنافية، ومصدرُها.

    والحالُ **ليست حدثًا**: الحدثُ يقع في زمنٍ وينتهي، والحالُ تستمرّ على فترة؛
    وهذا هو الفارقُ الذي يمنع قراءةَ نفيِ الحدثِ تعيينًا لحالٍ.
    """

    state_id: str
    bearer_type_id: str
    mutually_exclusive_values: tuple[str, ...]
    evidence_ref: EvidenceRef
    kind: OntologicalKind = OntologicalKind.STATE

    def __post_init__(self) -> None:
        _require_text(self.state_id, "مُعرِّفُ الحال")
        _require_text(self.bearer_type_id, "حاملُ الحال")
        if len(self.mutually_exclusive_values) < 2:
            raise SubstanceError("الحالُ قيمتانِ متنافيتانِ فأكثر؛ وقيمةٌ واحدةٌ ليست حالًا")
        if len(set(self.mutually_exclusive_values)) != len(
            self.mutually_exclusive_values
        ):
            raise SubstanceError("قيمةٌ مكرَّرةٌ في الحال تُرفَض لا تُطوى")
        if not isinstance(self.evidence_ref, EvidenceRef):
            raise SubstanceError("مصدرُ الحال إشارةٌ مبصومة")
        _require_kind(self.kind, (OntologicalKind.STATE,))

    def excludes(self, one: str, other: str) -> bool:
        """أتتنافى القيمتانِ في هذه الحال؟ ولا يُقاس التنافي على قيمةٍ غريبة."""

        for value in (one, other):
            if value not in self.mutually_exclusive_values:
                raise SubstanceError(f"`{value}` ليست قيمةً في الحال `{self.state_id}`")
        return one != other

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الحال للبصمة."""

        return {
            "state_id": self.state_id,
            "kind": self.kind.value,
            "bearer_type_id": self.bearer_type_id,
            "mutually_exclusive_values": list(self.mutually_exclusive_values),
            "evidence_ref": self.evidence_ref.as_canonical_content(),
        }


@dataclass(frozen=True, slots=True)
class PartDefinition:
    """«جزءٌ من»: جزءٌ من أيّ نوعٍ، وبأيّ معنًى؛ وليس «فردًا من» نوع الكلّ."""

    part_id: str
    part_type_id: str
    whole_type_id: str
    sense: str
    evidence_ref: EvidenceRef
    kind: OntologicalKind = OntologicalKind.THING

    def __post_init__(self) -> None:
        _require_text(self.part_id, "مُعرِّفُ الجزء")
        _require_text(self.part_type_id, "نوعُ الجزء")
        _require_text(self.whole_type_id, "نوعُ الكلّ")
        _require_text(self.sense, "معنى الجزئيّة؛ فـ«جزءٌ» بلا معنًى وصلةٌ عامّة")
        if not isinstance(self.evidence_ref, EvidenceRef):
            raise SubstanceError("مصدرُ الجزء إشارةٌ مبصومة")
        _require_kind(self.kind, (OntologicalKind.THING,))

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الجزء للبصمة."""

        return {
            "part_id": self.part_id,
            "part_type_id": self.part_type_id,
            "whole_type_id": self.whole_type_id,
            "sense": self.sense,
            "evidence_ref": self.evidence_ref.as_canonical_content(),
        }


@dataclass(frozen=True, slots=True)
class CapabilityDefinition:
    """قدرةٌ واحدة: حاملُها، وما تُمكِّن منه من أنواع الأحداث، ومصدرُها."""

    capability_id: str
    bearer_type_id: str
    enables_event_type_id: str
    evidence_ref: EvidenceRef

    def __post_init__(self) -> None:
        _require_text(self.capability_id, "مُعرِّفُ القدرة")
        _require_text(self.bearer_type_id, "حاملُ القدرة")
        _require_text(self.enables_event_type_id, "نوعُ الحدث الذي تُمكِّن منه القدرة")
        if not isinstance(self.evidence_ref, EvidenceRef):
            raise SubstanceError("مصدرُ القدرة إشارةٌ مبصومة")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى القدرة للبصمة."""

        return {
            "capability_id": self.capability_id,
            "bearer_type_id": self.bearer_type_id,
            "enables_event_type_id": self.enables_event_type_id,
            "evidence_ref": self.evidence_ref.as_canonical_content(),
        }


@dataclass(frozen=True, slots=True)
class RoleDefinition:
    """دورٌ في حدث: مُعرِّفُه، ونوعُ شاغله المسموح، وهل هو لازمٌ لتمام الحدث."""

    role_id: str
    filler_type_id: str
    obligatory: bool
    kind: OntologicalKind = OntologicalKind.ROLE

    def __post_init__(self) -> None:
        _require_text(self.role_id, "مُعرِّفُ الدور")
        _require_text(self.filler_type_id, "نوعُ شاغل الدور")
        if not isinstance(self.obligatory, bool):
            raise SubstanceError("لزومُ الدور قيمةٌ ثنائيّةٌ مُصرَّح بها")
        _require_kind(self.kind, (OntologicalKind.ROLE,))

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الدور للبصمة."""

        return {
            "role_id": self.role_id,
            "kind": self.kind.value,
            "filler_type_id": self.filler_type_id,
            "obligatory": self.obligatory,
        }


@dataclass(frozen=True, slots=True)
class EventTypeDefinition:
    """نوعُ حدث: أدوارُه، وشرطُه السابق، وأثرُه في الحال، وهل هو سببيّ.

    و`resulting_state` أثرٌ **مُعلَن** بالنوع والقيمة، لا يُستنتَج من الاسم؛
    و`is_causative` حقلٌ مُصرَّحٌ به يمنع أن يُقرَأ كلُّ حدثٍ ذا فاعلٍ سببيّ.
    """

    event_type_id: str
    roles: tuple[RoleDefinition, ...]
    resulting_state_id: str | None
    resulting_state_value: str | None
    is_causative: bool
    evidence_ref: EvidenceRef
    kind: OntologicalKind = OntologicalKind.EVENT

    def __post_init__(self) -> None:
        _require_text(self.event_type_id, "مُعرِّفُ نوع الحدث")
        if not self.roles:
            raise SubstanceError("نوعُ الحدث دورٌ فأكثر؛ وحدثٌ بلا أدوارٍ حدثٌ بلا مشاركين")
        seen: set[str] = set()
        for role in self.roles:
            if not isinstance(role, RoleDefinition):
                raise SubstanceError("عضوٌ في الأدوار خارج نوعه")
            if role.role_id in seen:
                raise SubstanceError("دورٌ مكرَّرٌ في نوع الحدث يُرفَض لا يُطوى")
            seen.add(role.role_id)
        if (self.resulting_state_id is None) != (self.resulting_state_value is None):
            raise SubstanceError(
                "أثرُ الحدث حالٌ وقيمتُها معًا أو لا أثرَ مُعلَن؛ ونصفُ أثرٍ لا يُقرَأ"
            )
        if not isinstance(self.is_causative, bool):
            raise SubstanceError("سببيّةُ الحدث قيمةٌ ثنائيّةٌ مُصرَّح بها")
        if not isinstance(self.evidence_ref, EvidenceRef):
            raise SubstanceError("مصدرُ نوع الحدث إشارةٌ مبصومة")
        _require_kind(self.kind, (OntologicalKind.EVENT,))

    def role(self, role_id: str) -> RoleDefinition:
        """الدورُ بمُعرِّفه؛ والغيابُ رفضٌ لا `None` يُقرأ صمتًا."""

        for role in self.roles:
            if role.role_id == role_id:
                return role
        raise SubstanceError(f"لا دورَ `{role_id}` في نوع الحدث `{self.event_type_id}`")

    @property
    def obligatory_role_ids(self) -> tuple[str, ...]:
        """الأدوارُ اللازمة؛ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب."""

        return tuple(role.role_id for role in self.roles if role.obligatory)

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى نوع الحدث للبصمة."""

        return {
            "event_type_id": self.event_type_id,
            "kind": self.kind.value,
            "roles": [role.as_canonical_content() for role in self.roles],
            "resulting_state_id": self.resulting_state_id,
            "resulting_state_value": self.resulting_state_value,
            "is_causative": self.is_causative,
            "evidence_ref": self.evidence_ref.as_canonical_content(),
        }


@dataclass(frozen=True, slots=True)
class RelationDefinition:
    """علاقةٌ ثنائيّةٌ مرتّبةُ الأطراف، بخواصَّ **مُعلَنةٍ** لا مستنتَجةٍ من اسمها."""

    relation_id: str
    domain_type_id: str
    range_type_id: str
    transitive: Declared
    symmetric: Declared
    reflexive: Declared
    justification: str
    evidence_ref: EvidenceRef
    kind: OntologicalKind = OntologicalKind.RELATION

    def __post_init__(self) -> None:
        _require_text(self.relation_id, "مُعرِّفُ العلاقة")
        _require_text(self.domain_type_id, "نوعُ الطرف الأوّل")
        _require_text(self.range_type_id, "نوعُ الطرف الثاني")
        for value, label in (
            (self.transitive, "تعدّي العلاقة"),
            (self.symmetric, "تماثلُ العلاقة"),
            (self.reflexive, "انعكاسُ العلاقة"),
        ):
            if not isinstance(value, Declared):
                raise SubstanceError(
                    f"{label} ثلاثيُّ الإعلان؛ و"
                    + A_RELATION_PROPERTY_IS_DECLARED_NOT_READ_OFF_ITS_NAME
                )
        _require_text(self.justification, "تعليلُ خواصّ العلاقة")
        if not isinstance(self.evidence_ref, EvidenceRef):
            raise SubstanceError("مصدرُ العلاقة إشارةٌ مبصومة")
        _require_kind(self.kind, (OntologicalKind.RELATION,))

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى العلاقة للبصمة."""

        return {
            "relation_id": self.relation_id,
            "kind": self.kind.value,
            "domain_type_id": self.domain_type_id,
            "range_type_id": self.range_type_id,
            "transitive": self.transitive.value,
            "symmetric": self.symmetric.value,
            "reflexive": self.reflexive.value,
            "justification": self.justification,
            "evidence_ref": self.evidence_ref.as_canonical_content(),
        }


@dataclass(frozen=True, slots=True)
class CompositionLaw:
    """رخصةُ تركيبٍ بين علاقتين بعينهما؛ ولا قاعدةَ عامّةً تُركِّب أيَّ علاقتين."""

    law_id: str
    first_relation_id: str
    second_relation_id: str
    composed_relation_id: str
    justification: str
    evidence_ref: EvidenceRef

    def __post_init__(self) -> None:
        _require_text(self.law_id, "مُعرِّفُ رخصة التركيب")
        for value, label in (
            (self.first_relation_id, "العلاقةُ الأولى"),
            (self.second_relation_id, "العلاقةُ الثانية"),
            (self.composed_relation_id, "العلاقةُ الناتجة"),
        ):
            _require_text(value, label)
        _require_text(self.justification, "تعليلُ رخصة التركيب")
        if not isinstance(self.evidence_ref, EvidenceRef):
            raise SubstanceError("مصدرُ رخصة التركيب إشارةٌ مبصومة")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الرخصة للبصمة."""

        return {
            "law_id": self.law_id,
            "first_relation_id": self.first_relation_id,
            "second_relation_id": self.second_relation_id,
            "composed_relation_id": self.composed_relation_id,
            "justification": self.justification,
            "evidence_ref": self.evidence_ref.as_canonical_content(),
        }


class RuleKind(Enum):
    """جنسُ القاعدة: قطعيّةٌ في النموذج المُعلَن، أو افتراضٌ قابلٌ للنقض."""

    STRICT_IN_THE_DECLARED_MODEL = "strict_in_the_declared_model"
    DEFEASIBLE = "defeasible"

    @property
    def is_defeasible(self) -> bool:
        """أهي قابلةٌ للنقض؟ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب."""

        return self is RuleKind.DEFEASIBLE


@dataclass(frozen=True, slots=True)
class InferenceRule:
    """قاعدةُ ربطٍ واحدة: مقدّماتُها، ونتيجتُها، وموانعُها، وجنسُها، وإصدارُها.

    و**الموانعُ حقلٌ مُلزَمٌ على القابلة للنقض**: قاعدةٌ قابلةٌ للنقض بلا مانعٍ
    مُسمًّى قاعدةٌ قطعيّةٌ في ثوبِ افتراض.
    """

    rule_id: str
    version: str
    kind: RuleKind
    premise_patterns: tuple[str, ...]
    conclusion_pattern: str
    applicability_note: str
    blocker_ids: tuple[str, ...]
    evidence_ref: EvidenceRef

    def __post_init__(self) -> None:
        _require_text(self.rule_id, "مُعرِّفُ القاعدة")
        _require_text(self.version, "إصدارُ القاعدة")
        if not isinstance(self.kind, RuleKind):
            raise SubstanceError("جنسُ القاعدة عضوٌ في مفردته المغلقة")
        if not self.premise_patterns:
            raise SubstanceError("القاعدةُ مقدّمةٌ فأكثر")
        _require_text(self.conclusion_pattern, "نتيجةُ القاعدة")
        _require_text(self.applicability_note, "شرطُ تطبيق القاعدة")
        if self.kind.is_defeasible and not self.blocker_ids:
            raise SubstanceError(
                "قاعدةٌ قابلةٌ للنقض بلا مانعٍ مُسمًّى قاعدةٌ قطعيّةٌ في ثوبِ افتراض"
            )
        if not isinstance(self.evidence_ref, EvidenceRef):
            raise SubstanceError("مصدرُ القاعدة إشارةٌ مبصومة")

    @property
    def versioned_id(self) -> str:
        """هويّةُ القاعدة بإصدارها؛ فتغييرُ الإصدار يُبطِل الربطَ بالحكم السابق."""

        return f"{self.rule_id}@{self.version}"

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى القاعدة للبصمة."""

        return {
            "rule_id": self.rule_id,
            "version": self.version,
            "kind": self.kind.value,
            "premise_patterns": list(self.premise_patterns),
            "conclusion_pattern": self.conclusion_pattern,
            "applicability_note": self.applicability_note,
            "blocker_ids": list(self.blocker_ids),
            "evidence_ref": self.evidence_ref.as_canonical_content(),
        }


@dataclass(frozen=True, slots=True)
class SubstanceStore:
    """الرصيدُ كلُّه: مؤسَّسٌ على `O_0`، ومفهرسٌ بمُعرِّفات، ومبصومٌ بمضمونه."""

    store_id: str
    ontology: GeneralOntology
    evidence: tuple[Evidence, ...]
    types: tuple[TypeDefinition, ...]
    subsumptions: tuple[SubsumptionLink, ...]
    attributes: tuple[AttributeDefinition, ...]
    states: tuple[StateDefinition, ...]
    parts: tuple[PartDefinition, ...]
    capabilities: tuple[CapabilityDefinition, ...]
    event_types: tuple[EventTypeDefinition, ...]
    relations: tuple[RelationDefinition, ...]
    composition_laws: tuple[CompositionLaw, ...]
    rules: tuple[InferenceRule, ...]

    def __post_init__(self) -> None:
        _require_text(self.store_id, "مُعرِّفُ الرصيد")
        if not isinstance(self.ontology, GeneralOntology):
            raise SubstanceError(
                "الرصيدُ مؤسَّسٌ على أنطولوجيا قائمة؛ و"
                + FOUNDING_A_KIND_IS_NOT_APPLYING_A_FOUNDED_KIND
            )
        founded = {candidate.kind for candidate in self.ontology.candidates}
        declared_kinds: list[OntologicalKind] = []
        declared_kinds.extend(item.kind for item in self.types)
        declared_kinds.extend(item.kind for item in self.attributes)
        declared_kinds.extend(item.kind for item in self.states)
        declared_kinds.extend(item.kind for item in self.parts)
        declared_kinds.extend(item.kind for item in self.event_types)
        declared_kinds.extend(item.kind for item in self.relations)
        declared_kinds.extend(
            role.kind for event in self.event_types for role in event.roles
        )
        for kind in declared_kinds:
            if kind not in founded:
                raise SubstanceError(
                    NO_ENTRY_OUTSIDE_THE_FOUNDED_CANDIDATES
                    + f"؛ والمرشَّحُ غيرُ المُسجَّل: `{kind.value}`"
                )
        known_refs = {item.ref for item in self.evidence}
        for ref in self._declared_refs():
            if ref not in known_refs:
                raise SubstanceError(
                    "بندٌ يُشير إلى دليلٍ ليس في الرصيد، أو تغيّر مضمونُه بعد "
                    f"الإشارة: `{ref.evidence_id}`"
                )

    def _declared_refs(self) -> tuple[EvidenceRef, ...]:
        refs: list[EvidenceRef] = []
        refs.extend(item.evidence_ref for item in self.types)
        refs.extend(item.evidence_ref for item in self.subsumptions)
        refs.extend(item.evidence_ref for item in self.attributes)
        refs.extend(item.evidence_ref for item in self.states)
        refs.extend(item.evidence_ref for item in self.parts)
        refs.extend(item.evidence_ref for item in self.capabilities)
        refs.extend(item.evidence_ref for item in self.event_types)
        refs.extend(item.evidence_ref for item in self.relations)
        refs.extend(item.evidence_ref for item in self.composition_laws)
        refs.extend(item.evidence_ref for item in self.rules)
        return tuple(refs)

    def evidence_of(self, ref: EvidenceRef) -> Evidence:
        """الدليلُ المُشارُ إليه بمُعرِّفه **وبصمته**؛ والاختلافُ رفضٌ لا تجاوز."""

        for item in self.evidence:
            if item.evidence_id != ref.evidence_id:
                continue
            if item.content_id != ref.content_id:
                raise EpistemicError(
                    "الدليلُ تغيّر مضمونُه بعد الإشارة إليه؛ فالإشارةُ تُشير إلى "
                    f"مضمونٍ لم يعد قائمًا: `{ref.evidence_id}`"
                )
            return item
        raise SubstanceError(f"لا دليلَ في الرصيد مُعرِّفُه `{ref.evidence_id}`")

    def type_of(self, type_id: str) -> TypeDefinition:
        """تعريفُ النوع بمُعرِّفه؛ والغيابُ رفضٌ مُسمًّى."""

        for definition in self.types:
            if definition.type_id == type_id:
                return definition
        raise SubstanceError(f"لا نوعَ في الرصيد مُعرِّفُه `{type_id}`")

    def attribute_of(self, attribute_id: str) -> AttributeDefinition:
        """تعريفُ الصفة بمُعرِّفها."""

        for definition in self.attributes:
            if definition.attribute_id == attribute_id:
                return definition
        raise SubstanceError(f"لا صفةَ في الرصيد مُعرِّفُها `{attribute_id}`")

    def state_of(self, state_id: str) -> StateDefinition:
        """تعريفُ الحال بمُعرِّفها."""

        for definition in self.states:
            if definition.state_id == state_id:
                return definition
        raise SubstanceError(f"لا حالَ في الرصيد مُعرِّفُها `{state_id}`")

    def event_type_of(self, event_type_id: str) -> EventTypeDefinition:
        """تعريفُ نوع الحدث بمُعرِّفه."""

        for definition in self.event_types:
            if definition.event_type_id == event_type_id:
                return definition
        raise SubstanceError(f"لا نوعَ حدثٍ في الرصيد مُعرِّفُه `{event_type_id}`")

    def relation_of(self, relation_id: str) -> RelationDefinition:
        """تعريفُ العلاقة بمُعرِّفها."""

        for definition in self.relations:
            if definition.relation_id == relation_id:
                return definition
        raise SubstanceError(f"لا علاقةَ في الرصيد مُعرِّفُها `{relation_id}`")

    def rule_of(self, rule_id: str) -> InferenceRule:
        """القاعدةُ بمُعرِّفها؛ والإصدارُ جزءٌ من هويّتها لا زينةٌ بجانبها."""

        for rule in self.rules:
            if rule.rule_id == rule_id:
                return rule
        raise SubstanceError(f"لا قاعدةَ في الرصيد مُعرِّفُها `{rule_id}`")

    def composition_law_for(
        self, first_relation_id: str, second_relation_id: str
    ) -> CompositionLaw | None:
        """رخصةُ تركيبِ علاقتين إن وُجدت؛ وغيابُها منعٌ لا تجاوزٌ صامت."""

        for law in self.composition_laws:
            if (
                law.first_relation_id == first_relation_id
                and law.second_relation_id == second_relation_id
            ):
                return law
        return None

    def broader_type_ids(self, type_id: str) -> tuple[str, ...]:
        """الأنواعُ الأعمُّ فوق نوعٍ، مغلقةً بالتعدّي **المُعلَن** في `نوع_من`.

        والإغلاقُ لا يقع إلّا إذا كانت علاقةُ `نوع_من` مُعلَنةَ التعدّي في
        الرصيد؛ فإن كانت `غيرَ مُعلَنة` خرجت الطبقةُ الأولى وحدَها.
        """

        direct = tuple(
            link.broader_type_id
            for link in self.subsumptions
            if link.narrower_type_id == type_id
        )
        try:
            relation = self.relation_of("نوع_من")
        except SubstanceError:
            return direct
        if relation.transitive is not Declared.YES:
            return direct
        reached: list[str] = []
        frontier = list(direct)
        while frontier:
            current = frontier.pop(0)
            if current in reached:
                continue
            reached.append(current)
            frontier.extend(
                link.broader_type_id
                for link in self.subsumptions
                if link.narrower_type_id == current
            )
        return tuple(reached)

    def attribute_status_for(
        self, attribute_id: str, bearer_type_ids: Sequence[str]
    ) -> ValueStatus:
        """أتنطبق الصفةُ على حاملٍ بهذه الأنواع؟ وعدمُ الانطباق يُسمَّى ولا يُطوى."""

        definition = self.attribute_of(attribute_id)
        expanded: list[str] = []
        for type_id in bearer_type_ids:
            expanded.append(type_id)
            expanded.extend(self.broader_type_ids(type_id))
        if definition.applies_to(expanded):
            return ValueStatus.UNKNOWN
        return ValueStatus.NOT_APPLICABLE

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الرصيد للبصمة؛ مرتّبًا ترتيبًا قانونيًّا لا ترتيبَ إدخال."""

        return {
            "store_id": self.store_id,
            "ontology_content_id": self.ontology.content_id,
            "evidence": [
                {"evidence_id": item.evidence_id, **item.as_canonical_content()}
                for item in sorted(self.evidence, key=lambda item: item.evidence_id)
            ],
            "types": [
                item.as_canonical_content()
                for item in sorted(self.types, key=lambda item: item.type_id)
            ],
            "subsumptions": [
                item.as_canonical_content()
                for item in sorted(
                    self.subsumptions,
                    key=lambda item: (item.narrower_type_id, item.broader_type_id),
                )
            ],
            "attributes": [
                item.as_canonical_content()
                for item in sorted(self.attributes, key=lambda item: item.attribute_id)
            ],
            "states": [
                item.as_canonical_content()
                for item in sorted(self.states, key=lambda item: item.state_id)
            ],
            "parts": [
                item.as_canonical_content()
                for item in sorted(self.parts, key=lambda item: item.part_id)
            ],
            "capabilities": [
                item.as_canonical_content()
                for item in sorted(
                    self.capabilities, key=lambda item: item.capability_id
                )
            ],
            "event_types": [
                item.as_canonical_content()
                for item in sorted(
                    self.event_types, key=lambda item: item.event_type_id
                )
            ],
            "relations": [
                item.as_canonical_content()
                for item in sorted(self.relations, key=lambda item: item.relation_id)
            ],
            "composition_laws": [
                item.as_canonical_content()
                for item in sorted(self.composition_laws, key=lambda item: item.law_id)
            ],
            "rules": [
                item.as_canonical_content()
                for item in sorted(self.rules, key=lambda item: item.versioned_id)
            ],
        }

    @property
    def content_id(self) -> str:
        """بصمةُ الرصيد؛ وتغييرُ بندٍ واحدٍ يُغيِّرها فيُكشَف الحكمُ المعتمِد عليه."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))
