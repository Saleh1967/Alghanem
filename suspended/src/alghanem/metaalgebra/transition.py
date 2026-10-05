"""الميتا-جبر: توقيعُ الانتقال العامّ، وقانونا مَنعِ القفز والتسليم.

    𝒯 = (D, G, T, P, τ, ρ)

حيث `D` شرطُ المجال، و`G` بوّابةُ الترخيص، و`T` التحويل، و`P` ما يجب حفظُه من
الثوابت، و`τ` التزامُ الأثر، و`ρ` سياسةُ البقايا والرتبة.

**قانونُ مَنعِ القفز، بصيغته الدقيقة:**

    D_i(x) ∧ G_i(x)  ⇒  T_i(x) ∈ C_{i+1}
    ¬G_i(x)          ⇒  T_i(x) غيرُ معرَّف، أو BLOCK/DEFER، ولا شهادةَ نجاح

والشطرُ الثاني **لا يقول** إنّ الناتج ليس عضوًا في الحامل الهدف، فقد يبلغه
طريقٌ آخرُ مرخَّصٌ فيكون عضوًا صحيحًا فيه. الممنوعُ هذا الانتقالُ بعينه وسلطتُه،
لا وجودُ القيمة في `C_{i+1}` مطلقًا
(`NO_JUMP_CONSTRAINS_THE_PATH_NOT_THE_TARGET_MEMBERSHIP`).

**وقانونُ التسليم مشروطٌ بشرطين لا بشرطٍ واحد:**

    Cl_i(y) ∧ Handoff_i(y)  ⇒  y ∈ Dom(T_{i+1})

فالإغلاقُ داخل الطبقة لا يمنح حقَّ الخروج منها: قد يكون الشيءُ مغلقًا في طبقته
وغيرَ مؤهّلٍ بعدُ لعلاقة الطبقة الأعلى (`CLOSURE_IS_NOT_A_RIGHT_OF_EXIT`). وهذا
موضعٌ يظهر أثرُه في الانتقالات الأعلى — من الوزن إلى الاشتقاق، ومن الكلمة إلى
الموقع النحويّ — حيث الإغلاقُ الداخليّ متحقّقٌ والتأهّلُ للخروج ليس متحقّقًا.

**ولا عضوَ في مفردة المخرَج اسمُه `PROVED`:** أعلى ما يُسجَّل
`CONDITIONALLY_LICENSED_RELATIVE_TO_SIGMA`، منسوبًا إلى مواصفةٍ مُجمَّدة.

تسجيلٌ لا سلطة: لا بوّابةَ تُشغَّل هنا، ولا حكمَ يُصدَر، ولا استيرادَ من
`kernel/` حرفًا.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest

__all__ = [
    "CLOSURE_IS_NOT_A_RIGHT_OF_EXIT",
    "HANDOFF_LAW",
    "NO_JUMP_CONSTRAINS_THE_PATH_NOT_THE_TARGET_MEMBERSHIP",
    "NO_JUMP_LAW",
    "REQUIRED_AUDIT_CERTIFICATE_FACTS",
    "TRANSITION_COMPONENT_NAMES",
    "DomainCondition",
    "HandoffCondition",
    "LicenseGateSpecification",
    "PreservationObligation",
    "ResidualRankPolicy",
    "TransitionOutcome",
    "TransitionSignature",
    "TransitionSignatureError",
    "TransitionTraceObligation",
    "TransformationSpecification",
]


class TransitionSignatureError(ValueError):
    """رفضٌ عند الإنشاء: بوّابةٌ بلا مخرَج رفضٍ، أو تسليمٌ يُختزَل في الإغلاق."""


class TransitionOutcome(Enum):
    """مخرَجاتُ الانتقال المُجمَّدة؛ ولا `PROVED` مطلقةً فيها.

    و`BLOCK` و`DEFER` وحدَهما مخرَجا عدمِ الترخيص: الأولى منعٌ مُسمًّى، والثانية
    لا-جوابٍ معرفيّ؛ وبينهما فرقٌ لا يُطوى.
    """

    CONDITIONALLY_LICENSED_RELATIVE_TO_SIGMA = (
        "CONDITIONALLY_LICENSED_RELATIVE_TO_SIGMA"
    )
    BLOCK = "BLOCK"
    DEFER = "DEFER"
    UNDEFINED = "UNDEFINED"
    REFUTED = "REFUTED"


_UNLICENSED_OUTCOMES: Final[frozenset[TransitionOutcome]] = frozenset(
    {TransitionOutcome.BLOCK, TransitionOutcome.DEFER}
)


NO_JUMP_LAW: Final[str] = (
    "D_i(x) ∧ G_i(x) ⇒ T_i(x) ∈ C_{i+1}؛ و¬G_i(x) ⇒ T_i(x) غيرُ معرَّفٍ أو "
    "BLOCK/DEFER، ولا تُصدَر شهادةُ انتقالٍ ناجح"
)

NO_JUMP_CONSTRAINS_THE_PATH_NOT_THE_TARGET_MEMBERSHIP: Final[str] = (
    "مَنعُ القفز يقيّد هذا المسارَ وسلطتَه، لا عضويّةَ القيمة في الحامل الهدف: "
    "قد يبلغها طريقٌ آخرُ مرخَّصٌ فتكون عضوًا صحيحًا فيه"
)

HANDOFF_LAW: Final[str] = (
    "Cl_i(y) ∧ Handoff_i(y) ⇒ y ∈ Dom(T_{i+1})؛ شرطان مستقلّان لا شرطٌ واحد"
)

CLOSURE_IS_NOT_A_RIGHT_OF_EXIT: Final[str] = (
    "الإغلاقُ داخل الطبقة لا يمنح حقَّ الخروج منها: مغلقٌ في طبقته قد يكون غيرَ "
    "مؤهّلٍ بعدُ لعلاقة الطبقة الأعلى، والتأهّلُ شرطٌ مستقلٌّ يُصرَّح به"
)

REQUIRED_AUDIT_CERTIFICATE_FACTS: Final[tuple[str, ...]] = (
    "source_class",
    "operation",
    "license",
    "preserved_invariants",
    "residuals",
)
"""ما يجب أن تستردَّه شهادةُ التدقيق الرجعيّ؛ خمسةٌ لا أقلّ، والأصلُ ليس منها."""

TRANSITION_COMPONENT_NAMES: Final[tuple[str, ...]] = (
    "domain",
    "gate",
    "transformation",
    "preservation",
    "trace",
    "residual_policy",
)
"""المكوّناتُ الستّة بأسمائها؛ والتسليمُ شرطٌ سابعٌ مُصرَّحٌ به على حدة."""


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise TransitionSignatureError(f"{label} نصٌّ غير فارغ")
    return value


def _require_text_tuple(value: object, label: str) -> tuple[str, ...]:
    if not isinstance(value, tuple) or not value:
        raise TransitionSignatureError(f"{label} مجموعةٌ غير فارغة")
    for item in value:
        _require_text(item, f"عنصرٌ في {label}")
    if len(set(value)) != len(value):
        raise TransitionSignatureError(f"{label} بلا تكرار؛ والمكرّرُ يُرفَض")
    return value


@dataclass(frozen=True, slots=True)
class DomainCondition:
    """`D`: متى يكون `x` في مجال الانتقال، ومتى يخرج منه."""

    condition_id: str
    holds_when: str
    fails_when: str

    def __post_init__(self) -> None:
        _require_text(self.condition_id, "اسمُ شرط المجال")
        _require_text(self.holds_when, "شرطُ الدخول في المجال")
        _require_text(self.fails_when, "شرطُ الخروج من المجال")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى شرط المجال للبصمة."""

        return {
            "condition_id": self.condition_id,
            "holds_when": self.holds_when,
            "fails_when": self.fails_when,
        }


@dataclass(frozen=True, slots=True)
class LicenseGateSpecification:
    """`G`: بوّابةُ الترخيص، ومخرَجُ عدمِه مُصرَّحٌ به قبل التشغيل.

    ولا يجوز أن يكون مخرَجُ عدمِ الترخيص خارجَ `{BLOCK, DEFER}`: نجاحٌ صامتٌ عند
    عدم الترخيص هو القفزةُ بعينها.
    """

    gate_id: str
    licensed_when: str
    unlicensed_outcomes: tuple[TransitionOutcome, ...]
    unlicensed_reason: str

    def __post_init__(self) -> None:
        _require_text(self.gate_id, "اسمُ البوّابة")
        _require_text(self.licensed_when, "شرطُ الترخيص")
        _require_text(self.unlicensed_reason, "سببُ الرفض عند عدم الترخيص")
        if not isinstance(self.unlicensed_outcomes, tuple):
            raise TransitionSignatureError("مخرَجاتُ عدم الترخيص مجموعةٌ مُصرَّحٌ بها")
        if not self.unlicensed_outcomes:
            raise TransitionSignatureError(
                "بوّابةٌ بلا مخرَجِ رفضٍ بوّابةٌ لا ترفض؛ والرفضُ هو عملُها"
            )
        for outcome in self.unlicensed_outcomes:
            if outcome not in _UNLICENSED_OUTCOMES:
                raise TransitionSignatureError(
                    "مخرَجُ عدم الترخيص `BLOCK` أو `DEFER` لا غير؛ " f"و{NO_JUMP_LAW}"
                )
        if len(set(self.unlicensed_outcomes)) != len(self.unlicensed_outcomes):
            raise TransitionSignatureError("مخرَجُ رفضٍ مكرّرٌ يُرفَض لا يُطوى")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى البوّابة للبصمة."""

        return {
            "gate_id": self.gate_id,
            "licensed_when": self.licensed_when,
            "unlicensed_outcomes": [
                outcome.value for outcome in self.unlicensed_outcomes
            ],
            "unlicensed_reason": self.unlicensed_reason,
        }


@dataclass(frozen=True, slots=True)
class TransformationSpecification:
    """`T`: قاعدةُ التحويل خطوةً خطوة، ومواضعُ لا-تعريفها."""

    transformation_id: str
    steps: tuple[str, ...]
    undefined_when: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_text(self.transformation_id, "اسمُ التحويل")
        _require_text_tuple(self.steps, "خطواتُ التحويل")
        _require_text_tuple(self.undefined_when, "مواضعُ لا-تعريف التحويل")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التحويل للبصمة."""

        return {
            "transformation_id": self.transformation_id,
            "steps": list(self.steps),
            "undefined_when": list(self.undefined_when),
        }


@dataclass(frozen=True, slots=True)
class PreservationObligation:
    """`P`: ما يجب حفظُه مُسمًّى، وما يُصرَّح بتغيّره؛ ولا «كلُّ شيء».

    `Inv_i(x) = Inv_{i+1}(T_i(x))` مطلوبةٌ في الجزء المُسمّى وحدَه؛ ودعوى حفظِ
    كلِّ شيءٍ دعوى بلا مُفنِّد.
    """

    preserved_components: tuple[str, ...]
    changed_components: tuple[str, ...]
    preservation_condition: str

    def __post_init__(self) -> None:
        _require_text_tuple(self.preserved_components, "المكوّناتُ المحفوظة")
        if not isinstance(self.changed_components, tuple):
            raise TransitionSignatureError("المكوّناتُ المتغيّرة مجموعةٌ مُصرَّحٌ بها")
        for item in self.changed_components:
            _require_text(item, "عنصرٌ في المكوّنات المتغيّرة")
        if len(set(self.changed_components)) != len(self.changed_components):
            raise TransitionSignatureError("مكوّنٌ متغيّرٌ مكرّرٌ يُرفَض")
        overlap = set(self.preserved_components) & set(self.changed_components)
        if overlap:
            raise TransitionSignatureError(
                "مكوّنٌ محفوظٌ ومتغيّرٌ معًا دعوى متناقضة: " + "، ".join(sorted(overlap))
            )
        _require_text(self.preservation_condition, "شرطُ الحفظ")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التزام الحفظ للبصمة."""

        return {
            "preserved_components": list(self.preserved_components),
            "changed_components": list(self.changed_components),
            "preservation_condition": self.preservation_condition,
        }


@dataclass(frozen=True, slots=True)
class TransitionTraceObligation:
    """`τ`: شهادةُ التدقيق الرجعيّ، لا معكوسُ التحويل.

    لا يُطلَب `T⁻¹`، لأنّ التحويلَ قد يكون ضاغطًا؛ ويُطلَب أن تكفي الشهادةُ
    لتفسير **سببِ ترخيص** الانتقال: الحقولُ الخمسةُ في
    `REQUIRED_AUDIT_CERTIFICATE_FACTS` كلُّها، ولا يُستعاض عن واحدٍ منها بآخر.
    """

    obligation_id: str
    certificate_facts: tuple[str, ...]
    minimality_condition: str

    def __post_init__(self) -> None:
        _require_text(self.obligation_id, "اسمُ التزام الأثر")
        _require_text_tuple(self.certificate_facts, "حقولُ الشهادة")
        _require_text(self.minimality_condition, "شرطُ أدنويّة الأثر")
        missing = set(REQUIRED_AUDIT_CERTIFICATE_FACTS) - set(self.certificate_facts)
        if missing:
            raise TransitionSignatureError(
                "شهادةُ التدقيق ناقصةُ الحقول: " + "، ".join(sorted(missing))
            )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التزام الأثر للبصمة."""

        return {
            "obligation_id": self.obligation_id,
            "certificate_facts": list(self.certificate_facts),
            "minimality_condition": self.minimality_condition,
        }


@dataclass(frozen=True, slots=True)
class ResidualRankPolicy:
    """`ρ`: ما يبقى بعد الانتقال، وعلاقةُ الرتبة، ومخرَجُ مخالفتها."""

    policy_id: str
    residual_condition: str
    rank_relation: str
    violation_outcome: TransitionOutcome

    def __post_init__(self) -> None:
        _require_text(self.policy_id, "اسمُ سياسة البقايا")
        _require_text(self.residual_condition, "شرطُ البقايا")
        _require_text(self.rank_relation, "علاقةُ الرتبة")
        if self.violation_outcome not in _UNLICENSED_OUTCOMES:
            raise TransitionSignatureError(
                "مخالفةُ الرتبة تُخرِج `BLOCK` أو `DEFER`، ولا تمرّ نجاحًا"
            )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى سياسة البقايا للبصمة."""

        return {
            "policy_id": self.policy_id,
            "residual_condition": self.residual_condition,
            "rank_relation": self.rank_relation,
            "violation_outcome": self.violation_outcome.value,
        }


@dataclass(frozen=True, slots=True)
class HandoffCondition:
    """شرطُ التسليم: حقُّ الخروج من الطبقة، مستقلًّا عن إغلاقها الداخليّ.

    ويُشترَط التصريحُ بما يضيفه هذا الشرطُ فوق الإغلاق؛ فشرطُ تسليمٍ يُعيد نصَّ
    الإغلاق ليس شرطًا مستقلًّا، بل الإغلاقُ باسمٍ ثانٍ.
    """

    condition_id: str
    holds_when: str
    beyond_closure: str
    failure_outcome: TransitionOutcome

    def __post_init__(self) -> None:
        _require_text(self.condition_id, "اسمُ شرط التسليم")
        _require_text(self.holds_when, "شرطُ التأهّل للخروج")
        _require_text(self.beyond_closure, "ما يزيده التسليمُ على الإغلاق")
        if self.failure_outcome not in _UNLICENSED_OUTCOMES:
            raise TransitionSignatureError(
                "تخلّفُ شرط التسليم يُخرِج `BLOCK` أو `DEFER`؛ "
                f"و{CLOSURE_IS_NOT_A_RIGHT_OF_EXIT}"
            )
        if self.beyond_closure.strip() == self.holds_when.strip():
            raise TransitionSignatureError(CLOSURE_IS_NOT_A_RIGHT_OF_EXIT)

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى شرط التسليم للبصمة."""

        return {
            "condition_id": self.condition_id,
            "holds_when": self.holds_when,
            "beyond_closure": self.beyond_closure,
            "failure_outcome": self.failure_outcome.value,
        }


@dataclass(frozen=True, slots=True)
class TransitionSignature:
    """`𝒯 = (D, G, T, P, τ, ρ)` مع شرط التسليم، بين طبقتين مُسمّاتين.

    والطبقتان تُسمّيان بمعرّفيهما لا بأنواعٍ مُعلَنةٍ سلفًا؛ فلا مفردةَ أسماءِ
    طبقاتٍ في هذه الحزمة أصلًا.
    """

    transition_id: str
    source_layer_id: str
    target_layer_id: str
    domain: DomainCondition
    gate: LicenseGateSpecification
    transformation: TransformationSpecification
    preservation: PreservationObligation
    trace: TransitionTraceObligation
    residual_policy: ResidualRankPolicy
    handoff: HandoffCondition

    def __post_init__(self) -> None:
        _require_text(self.transition_id, "اسمُ الانتقال")
        _require_text(self.source_layer_id, "اسمُ الطبقة المصدر")
        _require_text(self.target_layer_id, "اسمُ الطبقة الهدف")
        if self.source_layer_id == self.target_layer_id:
            raise TransitionSignatureError(
                "انتقالٌ بين طبقةٍ ونفسِها ليس انتقالًا بين طبقتين"
            )
        for value, member_type, label in (
            (self.domain, DomainCondition, "شرطُ المجال"),
            (self.gate, LicenseGateSpecification, "بوّابةُ الترخيص"),
            (self.transformation, TransformationSpecification, "التحويل"),
            (self.preservation, PreservationObligation, "التزامُ الحفظ"),
            (self.trace, TransitionTraceObligation, "التزامُ الأثر"),
            (self.residual_policy, ResidualRankPolicy, "سياسةُ البقايا"),
            (self.handoff, HandoffCondition, "شرطُ التسليم"),
        ):
            if not isinstance(value, member_type):
                raise TransitionSignatureError(f"{label} خارج نوعه")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى توقيع الانتقال للبصمة."""

        return {
            "transition_id": self.transition_id,
            "source_layer_id": self.source_layer_id,
            "target_layer_id": self.target_layer_id,
            "domain": self.domain.as_canonical_content(),
            "gate": self.gate.as_canonical_content(),
            "transformation": self.transformation.as_canonical_content(),
            "preservation": self.preservation.as_canonical_content(),
            "trace": self.trace.as_canonical_content(),
            "residual_policy": self.residual_policy.as_canonical_content(),
            "handoff": self.handoff.as_canonical_content(),
        }

    @property
    def content_id(self) -> str:
        """بصمةُ محتوى العقد؛ وبها يُقال إنّ العقدَ جُمِّد قبل دالّته."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


_JUDGEMENT_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "standing",
    "verdict",
    "birth",
    "proved",
)

_SIGNATURE_TYPES: Final[tuple[type, ...]] = (
    DomainCondition,
    HandoffCondition,
    LicenseGateSpecification,
    PreservationObligation,
    ResidualRankPolicy,
    TransformationSpecification,
    TransitionSignature,
    TransitionTraceObligation,
)

for _declaring_type in _SIGNATURE_TYPES:  # pragma: no cover - import guard
    for _field in fields(_declaring_type):
        if any(marker in _field.name for marker in _JUDGEMENT_FIELD_MARKERS):
            raise RuntimeError("توقيعُ الانتقال يحمل شروطَه لا أحكامَه؛ ولا حقلَ حكمٍ فيه")

if any(
    member.name == "PROVED" or member.name.endswith("_PROVED")
    for member in TransitionOutcome
):  # pragma: no cover - import guard
    raise RuntimeError("لا `PROVED` مطلقةً في مفردة مخرَج الانتقال")
