"""`G0.FIBER-0.NODE`: عقدةُ المعلومات السابقة المنظَّمة، باثني عشر موضعًا مُصرَّحًا.

العقدةُ لا تُخزِّن وقائعَ جاهزة ولا تُسنِد أدوارًا: إنّما تُصرِّح بما يجوز أن
يُسأَل عنه، وبما يجوز أن يُفرَّق به، وبما يلزم من دليلٍ قبل أيّ إسناد. وهي
مبنيّةٌ **فوق** `PriorInformationBase` القائمة لا نسخةً منها، فمواضعُ الإمكان
التسعةُ تبقى مصدرَ الترخيص الوحيد، ولا تُخترَع هنا قاعدةٌ ثانية.

وحالةُ الخانات ابتداءً محايدةٌ كلُّها: `UNASSIGNED` تصريحٌ لا `None` صامتة، وأيُّ
دورٍ إيجابيٍّ لاحقٍ يلزمه ترخيصٌ من داخل الليف بدليلٍ مُسمًّى.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from ..prior import PriorConditionKind, PriorInformationBase
from .laws import (
    NO_POSITIVE_ROLE_FROM_A_NEUTRAL_FIBER_INPUT,
    THE_FIBER_DEFERS_ITS_RANK_TO_AN_EXTERNAL_AUTHORITY,
    PriorFiberError,
)

__all__ = [
    "PRIOR_FIBER_NODE_POSITIONS",
    "AdmissibleDistinction",
    "ExternalRankReference",
    "PriorFiberNode",
    "SlotStanding",
]


class SlotStanding(Enum):
    """حالُ الخانة في العقدة؛ والمحايدُ عضوٌ مُصرَّحٌ به لا غيابُ قيمة."""

    UNASSIGNED = "unassigned"

    @property
    def is_positive(self) -> bool:
        """أدورٌ إيجابيٌّ هو؟ ولا عضوَ إيجابيًّا في هذا الطور بالبناء."""

        return False


PRIOR_FIBER_NODE_POSITIONS: Final[tuple[str, ...]] = (
    "origin_id",
    "instance_id",
    "prior_base",
    "slot_geometry",
    "admissible_distinctions",
    "relations",
    "capabilities",
    "evidence_requirements",
    "gates",
    "rank_reference",
    "residual_policy",
    "trace",
)
"""مواضعُ العقدة الاثنا عشر؛ تُشتَقُّ الأسماءُ منها ولا تُكتَب نسخةٌ ثانية."""


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PriorFiberError(f"{label} نصٌّ غير فارغ")
    return value


def _require_texts(value: object, label: str, *, allow_empty: bool) -> tuple[str, ...]:
    if not isinstance(value, tuple):
        raise PriorFiberError(f"{label} صفٌّ مُجمَّد لا قائمة")
    if not value and not allow_empty:
        raise PriorFiberError(f"{label} لا يكون فارغًا")
    for item in value:
        _require_text(item, f"عضوٌ في {label}")
    if len(set(value)) != len(value):
        raise PriorFiberError(f"{label} لا يُكرِّر عضوًا؛ والمكرّرُ يُرفَض لا يُطوى")
    return value


@dataclass(frozen=True, slots=True)
class ExternalRankReference:
    """إحالةُ الرتبة: مرجعُ الدليل وسقفُ الرتبة، إحالةً لا سلّمًا ثانيًا."""

    evidence_ref: str
    rank_ceiling_ref: str
    issuing_authority: str

    def __post_init__(self) -> None:
        _require_text(self.evidence_ref, "مرجعُ الدليل")
        _require_text(self.rank_ceiling_ref, "مرجعُ سقف الرتبة")
        _require_text(
            self.issuing_authority,
            "سلطةُ إصدار الرتبة؛ و" + THE_FIBER_DEFERS_ITS_RANK_TO_AN_EXTERNAL_AUTHORITY,
        )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الإحالة للبصمة."""

        return {
            "evidence_ref": self.evidence_ref,
            "rank_ceiling_ref": self.rank_ceiling_ref,
            "issuing_authority": self.issuing_authority,
        }


@dataclass(frozen=True, slots=True)
class AdmissibleDistinction:
    """فرقٌ مقبولٌ واحد: سؤالُه، وقيمُه المغلقة، وشرطُ طرحه مُصرَّحًا."""

    distinction_id: str
    question: str
    options: tuple[str, ...]
    asked_when: str

    def __post_init__(self) -> None:
        _require_text(self.distinction_id, "مُعرِّفُ الفرق")
        _require_text(self.question, f"سؤالُ `{self.distinction_id}`")
        _require_texts(self.options, f"قيمُ `{self.distinction_id}`", allow_empty=False)
        if len(self.options) < 2:
            raise PriorFiberError(
                f"فرقٌ بقيمةٍ واحدة لا يُفرِّق شيئًا: `{self.distinction_id}`"
            )
        _require_text(self.asked_when, f"شرطُ طرح `{self.distinction_id}`")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الفرق للبصمة."""

        return {
            "distinction_id": self.distinction_id,
            "question": self.question,
            "options": list(self.options),
            "asked_when": self.asked_when,
        }


@dataclass(frozen=True, slots=True)
class PriorFiberNode:
    """عقدةٌ ليفيّةٌ واحدة: هندسةُ إمكانٍ مُرخَّصةٌ لا وقائعُ جاهزة."""

    origin_id: str
    instance_id: str
    prior_base: PriorInformationBase
    slot_geometry: tuple[str, ...]
    admissible_distinctions: tuple[AdmissibleDistinction, ...]
    relations: tuple[str, ...]
    capabilities: tuple[str, ...]
    evidence_requirements: tuple[str, ...]
    gates: tuple[str, ...]
    rank_reference: ExternalRankReference
    residual_policy: str
    trace: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_text(self.origin_id, "مُعرِّفُ الأصل")
        _require_text(self.instance_id, "مُعرِّفُ النسخة")
        if self.origin_id == self.instance_id:
            raise PriorFiberError(
                "الأصلُ والنسخةُ مُعرِّفان متمايزان؛ فالنسخةُ ليست الأصلَ نفسَه"
            )
        if not isinstance(self.prior_base, PriorInformationBase):
            raise PriorFiberError("قاعدةُ المعلومات السابقة من نوعها لا نصًّا حرًّا")
        if not self.prior_base.is_fit_to_found_an_ontology:
            missing = "، ".join(self.prior_base.unusable_condition_ids)
            raise PriorFiberError(
                "المعلوماتُ السابقة المنظَّمة هندسةٌ مُرخَّصة؛ وهذه شروطُها غيرُ "
                f"المُرخَّصة: {missing}"
            )
        _require_texts(self.slot_geometry, "هندسةُ الخانات", allow_empty=False)
        if not isinstance(self.admissible_distinctions, tuple):
            raise PriorFiberError("الفروقُ المقبولة صفٌّ مُجمَّد")
        if not self.admissible_distinctions:
            raise PriorFiberError("عقدةٌ بلا فرقٍ مقبولٍ لا تُنظِّم شيئًا")
        for distinction in self.admissible_distinctions:
            if not isinstance(distinction, AdmissibleDistinction):
                raise PriorFiberError("عضوٌ في الفروق خارج نوعه")
        distinction_ids = tuple(
            distinction.distinction_id for distinction in self.admissible_distinctions
        )
        if len(set(distinction_ids)) != len(distinction_ids):
            raise PriorFiberError("مُعرِّفُ الفرق لا يتكرّر؛ والمكرّرُ يُرفَض لا يُطوى")
        _require_texts(self.relations, "العلاقاتُ الممكنة", allow_empty=True)
        _require_texts(self.capabilities, "القدرات", allow_empty=True)
        _require_texts(self.evidence_requirements, "شروطُ الدليل", allow_empty=False)
        _require_texts(self.gates, "البوّابات", allow_empty=False)
        if not isinstance(self.rank_reference, ExternalRankReference):
            raise PriorFiberError(THE_FIBER_DEFERS_ITS_RANK_TO_AN_EXTERNAL_AUTHORITY)
        _require_text(self.residual_policy, "سياسةُ البقايا")
        _require_texts(self.trace, "الأثر", allow_empty=False)

    @property
    def domain_note(self) -> str:
        """بيانُ المجال؛ يُقرَأ من شرط المجال في القاعدة لا يُكتَب هنا ثانيةً."""

        return self.prior_base.condition(PriorConditionKind.DOMAIN).statement

    @property
    def neutral_slot_state(self) -> tuple[tuple[str, SlotStanding], ...]:
        """حالُ الخانات ابتداءً: محايدةٌ كلُّها بالتصريح لا بالصمت."""

        return tuple((slot, SlotStanding.UNASSIGNED) for slot in self.slot_geometry)

    @property
    def assigns_no_positive_role(self) -> bool:
        """أتخلو العقدةُ من كلِّ دورٍ إيجابيٍّ غيرِ مُرخَّص؟"""

        return all(
            standing.is_positive is False for _, standing in self.neutral_slot_state
        )

    @property
    def refusal_of_a_positive_role(self) -> str:
        """قانونُ منع الدور الإيجابيّ من مدخلٍ محايد."""

        return NO_POSITIVE_ROLE_FROM_A_NEUTRAL_FIBER_INPUT

    def distinction(self, distinction_id: str) -> AdmissibleDistinction:
        """الفرقُ بمعرِّفه؛ والغيابُ رفضٌ لا `None` يُقرأ صمتًا."""

        for distinction in self.admissible_distinctions:
            if distinction.distinction_id == distinction_id:
                return distinction
        raise PriorFiberError(f"لا فرقَ في العقدة بمعرِّف `{distinction_id}`")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى العقدة للبصمة."""

        return {
            "origin_id": self.origin_id,
            "instance_id": self.instance_id,
            "prior_base": self.prior_base.as_canonical_content(),
            "slot_geometry": list(self.slot_geometry),
            "admissible_distinctions": [
                distinction.as_canonical_content()
                for distinction in sorted(
                    self.admissible_distinctions,
                    key=lambda item: item.distinction_id,
                )
            ],
            "relations": list(self.relations),
            "capabilities": list(self.capabilities),
            "evidence_requirements": list(self.evidence_requirements),
            "gates": list(self.gates),
            "rank_reference": self.rank_reference.as_canonical_content(),
            "residual_policy": self.residual_policy,
            "trace": list(self.trace),
        }

    @property
    def content_id(self) -> str:
        """بصمةُ العقدة؛ وليفٌ على بصمةٍ غيرِها ليفُ عقدةٍ أخرى."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


def _refuse_a_position_without_a_field() -> None:
    """ارفض عند الاستيراد اختلافَ المواضع المُصرَّحة عن حقول العقدة."""

    declared = tuple(PriorFiberNode.__dataclass_fields__)
    if declared != PRIOR_FIBER_NODE_POSITIONS:
        raise PriorFiberError("مواضعُ العقدة المُصرَّحة تخالف حقولَها")


_refuse_a_position_without_a_field()
