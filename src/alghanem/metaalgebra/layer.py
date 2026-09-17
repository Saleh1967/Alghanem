"""الميتا-جبر: توقيعُ الطبقة العامّ، نوعًا لا معماريّةً مُعلَنةً سلفًا.

هذه الوحدةُ تُجمّد **ما يجعل الشيءَ طبقةً**، ولا تُسمّي طبقةً واحدة:

    𝒜 = (C, S, Ω, Rel, Inv, Cl, Tr, R)

حيث `C` الحامل، و`S` فضاءُ الحالة، و`Ω` العملياتُ الجزئية، و`Rel` علاقاتُ
الترخيص، و`Inv` الثوابت، و`Cl` قانونُ الإغلاق، و`Tr` الأثرُ القابل للتدقيق،
و`R` البقايا.

**والفرقُ الذي يمنع تعارضَ هذه الوحدة مع `G0.MA`:**

    GenericLayerType  ≠  PredeclaredLayerArchitecture

فتعريفُ `Graph = (V, E)` ليس دعوى أنّ في العالم بيانًا بعدد عقدٍ بعينه؛ وكذلك
هنا: لا اسمَ طبقةٍ، ولا عددَ طبقات، ولا ترتيبَ بينها، ولا مثيلَ واحدًا تشحنه
هذه الوحدة. ومن أراد طبقةً عربيّةً بناها في موضعها ببياناتها، ولم تُعلَن هنا
سلفًا (`NoPatternNameBeforeIndependentBirth`).

**وفضاءُ الحالة مكوّنٌ مستقلٌّ لا حقلٌ داخل الحامل**، لأنّ `Carrier ≠ State`
نتيجةٌ من نتائج المشروع نفسِه لا تفصيلَ تنظيمٍ؛ ودفنُ `S` داخل `C` يُلغي تمييزًا
قام عليه ترميزُ الحامل والحالة كلُّه.

**والأثرُ مكوّنٌ ثامنٌ لا زيادة**، لأنّ التدقيقَ الرجعيّ التزامٌ دستوريٌّ في هذا
المستودع؛ وطبقةٌ لا تُصرّح بما يجب أن يستردَّه تدقيقُها طبقةٌ لا تُدقَّق.

**والعمليةُ الجزئيةُ تُصرّح بمواضع لا-تعريفها**: عمليةٌ لا تقول أين تنعدم تُقرَأ
كلّيّةً بالسهو، فتصير القفزةُ مُرخَّصةً بالصمت.

تسجيلٌ لا سلطة: لا حقلَ حكمٍ في صنفٍ هنا، ولا ولادةَ ولا تجميدَ `E0`، ولا
استيرادَ من `kernel/` حرفًا.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest

__all__ = [
    "A_LAYER_TYPE_IS_NOT_A_LAYER_ARCHITECTURE",
    "A_PARTIAL_OPERATION_DECLARES_WHERE_IT_IS_UNDEFINED",
    "CARRIER_IS_NOT_STATE",
    "LAYER_COMPONENT_NAMES",
    "NO_LAYER_IS_DECLARED_HERE",
    "CarrierSpecification",
    "ClosureLawSpecification",
    "InvariantComponentSpecification",
    "LayerSignature",
    "LayerSignatureError",
    "LicenseRelationSpecification",
    "PartialOperationSpecification",
    "ResidualSchemaSpecification",
    "StateSpaceSpecification",
    "TraceObligationSpecification",
]


class LayerSignatureError(ValueError):
    """رفضٌ عند الإنشاء: مكوّنٌ ناقص، أو عمليةٌ جزئيةٌ بلا مواضع لا-تعريف."""


A_LAYER_TYPE_IS_NOT_A_LAYER_ARCHITECTURE: Final[str] = (
    "تعريفُ نوعٍ عامٍّ يقبل أيّ معماريّةٍ ليس إعلانًا لمعماريّةٍ بعينها؛ ولا اسمَ "
    "طبقةٍ ولا عددَ طبقاتٍ مُعلَنٌ في هذه الوحدة"
)

CARRIER_IS_NOT_STATE: Final[str] = (
    "الحاملُ غيرُ الحالة: فضاءُ الحالة مكوّنٌ مستقلٌّ في التوقيع، ودفنُه داخل "
    "الحامل يُلغي تمييزًا قام عليه ترميزُ الحامل والحالة"
)

A_PARTIAL_OPERATION_DECLARES_WHERE_IT_IS_UNDEFINED: Final[str] = (
    "عمليةٌ جزئيةٌ لا تُصرّح بمواضع لا-تعريفها تُقرَأ كلّيّةً بالسهو، فتمرّ القفزةُ "
    "بالصمت لا بالترخيص"
)

NO_LAYER_IS_DECLARED_HERE: Final[str] = (
    "لا مثيلَ طبقةٍ واحدًا تشحنه هذه الوحدة: التوقيعُ نوعٌ يُملأ في موضعه، لا "
    "معماريّةٌ تُسبق بها التجربة"
)

LAYER_COMPONENT_NAMES: Final[tuple[str, ...]] = (
    "carrier",
    "state_space",
    "operations",
    "license_relations",
    "invariants",
    "closure",
    "trace",
    "residuals",
)
"""المكوّناتُ الثمانية بأسمائها؛ مفردةٌ مغلقةٌ لا تاسعَ لها في هذا التوقيع."""


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise LayerSignatureError(f"{label} نصٌّ غير فارغ")
    return value


def _require_text_tuple(value: object, label: str) -> tuple[str, ...]:
    if not isinstance(value, tuple) or not value:
        raise LayerSignatureError(f"{label} مجموعةٌ غير فارغة")
    for item in value:
        _require_text(item, f"عنصرٌ في {label}")
    if len(set(value)) != len(value):
        raise LayerSignatureError(f"{label} بلا تكرار؛ والمكرّرُ يُرفَض لا يُطوى")
    return value


@dataclass(frozen=True, slots=True)
class CarrierSpecification:
    """`C`: ما عناصرُ الحامل، وما شرطُ العضويّة، وما ليس عنصرًا فيه."""

    carrier_id: str
    membership_condition: str
    what_is_not_a_member: str

    def __post_init__(self) -> None:
        _require_text(self.carrier_id, "اسمُ الحامل")
        _require_text(self.membership_condition, "شرطُ العضويّة")
        _require_text(self.what_is_not_a_member, "ما ليس عنصرًا")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الحامل للبصمة."""

        return {
            "carrier_id": self.carrier_id,
            "membership_condition": self.membership_condition,
            "what_is_not_a_member": self.what_is_not_a_member,
        }


@dataclass(frozen=True, slots=True)
class StateSpaceSpecification:
    """`S`: فضاءُ الحالة مستقلًّا عن الحامل، مع تصريحٍ بسبب استقلاله."""

    state_space_id: str
    state_condition: str
    why_not_folded_into_carrier: str

    def __post_init__(self) -> None:
        _require_text(self.state_space_id, "اسمُ فضاء الحالة")
        _require_text(self.state_condition, "شرطُ الحالة")
        _require_text(self.why_not_folded_into_carrier, "سببُ استقلال الحالة")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى فضاء الحالة للبصمة."""

        return {
            "state_space_id": self.state_space_id,
            "state_condition": self.state_condition,
            "why_not_folded_into_carrier": self.why_not_folded_into_carrier,
        }


@dataclass(frozen=True, slots=True)
class PartialOperationSpecification:
    """عضوٌ في `Ω`: عمليةٌ جزئيةٌ بمدخلها ومخرَجها **ومواضع لا-تعريفها**."""

    operation_id: str
    input_condition: str
    result_condition: str
    undefined_when: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_text(self.operation_id, "اسمُ العملية")
        _require_text(self.input_condition, "شرطُ المُدخَل")
        _require_text(self.result_condition, "لازمُ المخرَج")
        if not isinstance(self.undefined_when, tuple) or not self.undefined_when:
            raise LayerSignatureError(
                A_PARTIAL_OPERATION_DECLARES_WHERE_IT_IS_UNDEFINED
            )
        _require_text_tuple(self.undefined_when, "مواضعُ لا-التعريف")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى العملية للبصمة."""

        return {
            "operation_id": self.operation_id,
            "input_condition": self.input_condition,
            "result_condition": self.result_condition,
            "undefined_when": list(self.undefined_when),
        }


@dataclass(frozen=True, slots=True)
class LicenseRelationSpecification:
    """عضوٌ في `Rel`: متى يُرخَّص، ومتى يُرفَض الترخيصُ رفضًا مُسمًّى."""

    relation_id: str
    holds_when: str
    refused_when: str

    def __post_init__(self) -> None:
        _require_text(self.relation_id, "اسمُ علاقة الترخيص")
        _require_text(self.holds_when, "شرطُ التحقّق")
        _require_text(self.refused_when, "شرطُ الرفض")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى علاقة الترخيص للبصمة."""

        return {
            "relation_id": self.relation_id,
            "holds_when": self.holds_when,
            "refused_when": self.refused_when,
        }


@dataclass(frozen=True, slots=True)
class InvariantComponentSpecification:
    """عضوٌ في `Inv`: مكوّنٌ محفوظٌ بسؤاله، ومصادرُ ممنوعةٌ أن تكون هويّتَه.

    والمنعُ بالمصدر لا بالاسم: حقلٌ يُعاد تسميتُه يعبر منعَ الأسماء، ولا يعبر
    منعَ المصادر.
    """

    component_name: str
    extracted_question: str
    forbidden_provenance: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_text(self.component_name, "اسمُ المكوّن المحفوظ")
        _require_text(self.extracted_question, "سؤالُ الاستخراج")
        _require_text_tuple(self.forbidden_provenance, "المصادرُ الممنوعة")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المكوّن المحفوظ للبصمة."""

        return {
            "component_name": self.component_name,
            "extracted_question": self.extracted_question,
            "forbidden_provenance": list(self.forbidden_provenance),
        }


@dataclass(frozen=True, slots=True)
class ClosureLawSpecification:
    """`Cl`: قانونُ إغلاقٍ يُشغَّل، وحالةُ تعذّرِ تشغيلِه مُسمّاة.

    والإغلاقُ **داخل الطبقة**: أنّ شيئًا مغلقٌ في طبقته لا يعني أنّه مؤهّلٌ
    للخروج منها؛ وذلك شرطُ تسليمٍ مستقلٌّ في `transition.HandoffCondition`.
    """

    law_id: str
    quotient_condition: str
    observation_condition: str
    underpowered_when: str

    def __post_init__(self) -> None:
        _require_text(self.law_id, "اسمُ قانون الإغلاق")
        _require_text(self.quotient_condition, "شرطُ خارج القسمة")
        _require_text(self.observation_condition, "شرطُ الملاحظة")
        _require_text(self.underpowered_when, "حالةُ تعذّر التشغيل")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى قانون الإغلاق للبصمة."""

        return {
            "law_id": self.law_id,
            "quotient_condition": self.quotient_condition,
            "observation_condition": self.observation_condition,
            "underpowered_when": self.underpowered_when,
        }


@dataclass(frozen=True, slots=True)
class TraceObligationSpecification:
    """`Tr`: ما يجب أن يستردَّه التدقيقُ، وشرطُ أدنويّةِ الأثر.

    والأثرُ ليس نسخةَ المُدخَل: أثرٌ يحمل الجوابَ كاملًا لا يُحتسَب إعادةَ بناء.
    """

    obligation_id: str
    recoverable_facts: tuple[str, ...]
    minimality_condition: str

    def __post_init__(self) -> None:
        _require_text(self.obligation_id, "اسمُ التزام الأثر")
        _require_text_tuple(self.recoverable_facts, "ما يستردُّه التدقيق")
        _require_text(self.minimality_condition, "شرطُ أدنويّة الأثر")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التزام الأثر للبصمة."""

        return {
            "obligation_id": self.obligation_id,
            "recoverable_facts": list(self.recoverable_facts),
            "minimality_condition": self.minimality_condition,
        }


@dataclass(frozen=True, slots=True)
class ResidualSchemaSpecification:
    """`R`: شكلُ البقايا وشرطُ تمامها؛ وبقيّةٌ غيرُ مُسمّاةٍ بقيّةٌ مطويّة."""

    schema_id: str
    row_condition: str
    completeness_condition: str

    def __post_init__(self) -> None:
        _require_text(self.schema_id, "اسمُ جدول البقايا")
        _require_text(self.row_condition, "شرطُ الصفّ")
        _require_text(self.completeness_condition, "شرطُ التمام")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى جدول البقايا للبصمة."""

        return {
            "schema_id": self.schema_id,
            "row_condition": self.row_condition,
            "completeness_condition": self.completeness_condition,
        }


@dataclass(frozen=True, slots=True)
class LayerSignature:
    """`𝒜 = (C, S, Ω, Rel, Inv, Cl, Tr, R)`: الطبقةُ نوعًا لا اسمًا.

    `layer_id` معرّفُ مثيلٍ يكتبه مَن يبنيه، لا عضوٌ في مفردةٍ مغلقةٍ من أسماء
    طبقاتٍ مُعلَنةٍ سلفًا؛ فلا مفردةَ من هذا الجنس في هذه الوحدة أصلًا.
    """

    layer_id: str
    carrier: CarrierSpecification
    state_space: StateSpaceSpecification
    operations: tuple[PartialOperationSpecification, ...]
    license_relations: tuple[LicenseRelationSpecification, ...]
    invariants: tuple[InvariantComponentSpecification, ...]
    closure: ClosureLawSpecification
    trace: TraceObligationSpecification
    residuals: ResidualSchemaSpecification

    def __post_init__(self) -> None:
        _require_text(self.layer_id, "اسمُ الطبقة")
        if not isinstance(self.carrier, CarrierSpecification):
            raise LayerSignatureError("الحاملُ مواصفةُ حاملٍ لا نصٌّ مرسَل")
        if not isinstance(self.state_space, StateSpaceSpecification):
            raise LayerSignatureError(CARRIER_IS_NOT_STATE)
        _require_members(
            self.operations, PartialOperationSpecification, "العمليّاتُ الجزئية"
        )
        _require_members(
            self.license_relations, LicenseRelationSpecification, "علاقاتُ الترخيص"
        )
        _require_members(self.invariants, InvariantComponentSpecification, "الثوابت")
        if not isinstance(self.closure, ClosureLawSpecification):
            raise LayerSignatureError("الإغلاقُ قانونٌ مُشغَّلٌ لا عضويّةُ قالب")
        if not isinstance(self.trace, TraceObligationSpecification):
            raise LayerSignatureError("الأثرُ التزامٌ مُصرَّحٌ به لا سجلٌّ ضمنيّ")
        if not isinstance(self.residuals, ResidualSchemaSpecification):
            raise LayerSignatureError("البقايا جدولٌ بشرطه لا حقلٌ حرّ")
        if self.carrier.carrier_id == self.state_space.state_space_id:
            raise LayerSignatureError(CARRIER_IS_NOT_STATE)
        _require_unique(
            tuple(item.operation_id for item in self.operations), "أسماءُ العمليات"
        )
        _require_unique(
            tuple(item.relation_id for item in self.license_relations),
            "أسماءُ علاقات الترخيص",
        )
        _require_unique(
            tuple(item.component_name for item in self.invariants),
            "أسماءُ الثوابت",
        )

    @property
    def invariant_component_names(self) -> frozenset[str]:
        """أسماءُ الثوابت خاصّيّةٌ تُشتَقّ من الأعضاء، لا حقلٌ يُكتَب بجانبها."""

        return frozenset(item.component_name for item in self.invariants)

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التوقيع الكامل للبصمة؛ المكوّناتُ الثمانيةُ كلُّها داخلة."""

        return {
            "layer_id": self.layer_id,
            "carrier": self.carrier.as_canonical_content(),
            "state_space": self.state_space.as_canonical_content(),
            "operations": [item.as_canonical_content() for item in self.operations],
            "license_relations": [
                item.as_canonical_content() for item in self.license_relations
            ],
            "invariants": [item.as_canonical_content() for item in self.invariants],
            "closure": self.closure.as_canonical_content(),
            "trace": self.trace.as_canonical_content(),
            "residuals": self.residuals.as_canonical_content(),
        }

    @property
    def content_id(self) -> str:
        """بصمةُ محتوى التوقيع؛ وبها وحدَها يُقال «عقدٌ مُجمَّد»."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


def _require_members(value: object, member_type: type, label: str) -> None:
    if not isinstance(value, tuple) or not value:
        raise LayerSignatureError(f"{label} مجموعةٌ غير فارغة")
    for item in value:
        if not isinstance(item, member_type):
            raise LayerSignatureError(f"عضوٌ في {label} خارج نوعه")


def _require_unique(names: tuple[str, ...], label: str) -> None:
    if len(set(names)) != len(names):
        raise LayerSignatureError(f"{label} بلا تكرار؛ والمكرّرُ يُرفَض لا يُرجَّح")


_JUDGEMENT_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "outcome",
    "verdict",
    "status",
    "standing",
    "result_status",
    "birth",
)

_SIGNATURE_TYPES: Final[tuple[type, ...]] = (
    CarrierSpecification,
    ClosureLawSpecification,
    InvariantComponentSpecification,
    LayerSignature,
    LicenseRelationSpecification,
    PartialOperationSpecification,
    ResidualSchemaSpecification,
    StateSpaceSpecification,
    TraceObligationSpecification,
)

for _declaring_type in _SIGNATURE_TYPES:  # pragma: no cover - import guard
    for _field in fields(_declaring_type):
        if any(marker in _field.name for marker in _JUDGEMENT_FIELD_MARKERS):
            raise RuntimeError("توقيعُ الطبقة يحمل شروطَه لا أحكامَه؛ ولا حقلَ حكمٍ فيه")
