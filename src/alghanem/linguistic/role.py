"""`Σ_L`: الدورُ النسبيُّ نوعٌ مستقلٌّ عن مرجع التمثيل، فصلًا بالبناء لا بالتسمية.

القاعدةُ الجامعة:

    LinguisticObject(x) = Representation(x) + RelationalRole(x)

فالحامل والحالة يجيبان: **كيف يوجد الكيانُ في النظام؟**، والدورُ النسبيُّ يجيب:
**ماذا يفعل هذا الكيانُ بوصفه لغة؟**. وهما سؤالان لا سؤالٌ واحدٌ بصيغتين، ولذلك:

    RepresentationRef  ≠  RelationalRoleRef

**والفصلُ نوعيٌّ لا اصطلاحُ تسمية** (`RelationIsNotRepresentation`): لا يكفي أن
يُفحَص اسمُ حقلٍ، لأنّ التسميةَ تُغيَّر وتبقى البنيةُ مدموجة. فالنوعان صنفان
متباينان، لا يقبل أحدُهما حقلًا من نوع الآخر، ويُفحَص ذلك **على أنواع الحقول**
عند الاستيراد؛ فدفنُ الدور داخل التمثيل — أو العكس — غيرُ قابلٍ للقول لا مرفوضٌ
بعد وقوعه.

**والجهلُ عضوٌ مُصرَّحٌ به لا فراغٌ يُطوى**: `RelationalRole.UNREAD` عضوٌ في
المفردة على مثال `غير_مقروء` في الطبقة العربية، فغيابُ قراءةِ الدور لا يُقرَأ
انتفاءً له.

تسجيلٌ لا سلطة: لا حكمَ هنا، ولا استيرادَ من `kernel/` ولا من `arabic/`.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

__all__ = [
    "AN_UNREAD_ROLE_IS_NOT_AN_ABSENT_ONE",
    "RELATION_IS_NOT_REPRESENTATION",
    "LinguisticObjectSignature",
    "RelationalRole",
    "RelationalRoleError",
    "RelationalRoleRef",
    "RepresentationRef",
]


class RelationalRoleError(ValueError):
    """رفضٌ عند الإنشاء: دورٌ في موضع تمثيل، أو تمثيلٌ في موضع دور."""


RELATION_IS_NOT_REPRESENTATION: Final[str] = (
    "الدورُ النسبيُّ غيرُ مرجع التمثيل: صنفان متباينان لا يحمل أحدُهما حقلًا من "
    "نوع الآخر، والفصلُ يُفحَص على أنواع الحقول لا على أسمائها؛ فاتّفاقُ "
    "التسمية لا يُنشئ فصلًا، واختلافُها لا يمنع دمجًا"
)

AN_UNREAD_ROLE_IS_NOT_AN_ABSENT_ONE: Final[str] = (
    "دورٌ غيرُ مقروءٍ ليس دورًا منتفيًا: العضوُ مُصرَّحٌ به في المفردة، فلا "
    "يُقرَأ غيابُ القراءة نفيًا للوظيفة اللغويّة"
)


class RelationalRole(Enum):
    """الوظيفةُ اللغويّةُ العليا للكيان؛ مفردةٌ مغلقةٌ بعضوِ جهلٍ مُصرَّحٍ به."""

    TERM_ANCHOR = "term_anchor"
    PREDICATE = "predicate"
    OPERATOR = "operator"
    CONSTRAINT = "constraint"
    UNREAD = "unread"


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RelationalRoleError(f"{label} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class RepresentationRef:
    """إشارةُ تمثيلٍ: حاملٌ وحالة، بمنزلة `Σ_M` لا بمنزلة النسبة.

    ولا حقلَ دورٍ فيها البتّة؛ فما يجيب «كيف يوجد» لا يجيب «ماذا يفعل».
    """

    carrier_id: str
    state_id: str

    def __post_init__(self) -> None:
        _require_text(self.carrier_id, "مُعرِّفُ الحامل")
        _require_text(self.state_id, "مُعرِّفُ الحالة")
        if self.carrier_id == self.state_id:
            raise RelationalRoleError(
                "الحاملُ غيرُ الحالة: مُعرِّفٌ واحدٌ لهما يُلغي التمييزَ الذي "
                "قام عليه ترميزُ الحامل والحالة"
            )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الإشارة للبصمة."""

        return {"carrier_id": self.carrier_id, "state_id": self.state_id}


@dataclass(frozen=True, slots=True)
class RelationalRoleRef:
    """إشارةُ دورٍ نسبيّ: وظيفةٌ لغويّةٌ وحاملُ قراءتها، بلا حاملٍ ولا حالة."""

    role: RelationalRole
    read_from: str

    def __post_init__(self) -> None:
        if not isinstance(self.role, RelationalRole):
            raise RelationalRoleError("الدورُ عضوٌ في مفردته المغلقة لا نصٌّ حرّ")
        _require_text(self.read_from, "حاملُ قراءة الدور")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الإشارة للبصمة."""

        return {"role": self.role.value, "read_from": self.read_from}


@dataclass(frozen=True, slots=True)
class LinguisticObjectSignature:
    """الكيانُ اللغويّ: تمثيلٌ **ودورٌ** معًا، لا أحدُهما مختزِلًا للآخر."""

    object_id: str
    representation: RepresentationRef
    relational_role: RelationalRoleRef

    def __post_init__(self) -> None:
        _require_text(self.object_id, "مُعرِّفُ الكيان اللغويّ")
        if not isinstance(self.representation, RepresentationRef):
            raise RelationalRoleError(RELATION_IS_NOT_REPRESENTATION)
        if not isinstance(self.relational_role, RelationalRoleRef):
            raise RelationalRoleError(RELATION_IS_NOT_REPRESENTATION)

    @property
    def is_role_read(self) -> bool:
        """أقُرِئ دورُه؟ خاصّيّةٌ تُشتَقّ، ولا تُكتَب حقلًا يخالف مرجعَه."""

        return self.relational_role.role is not RelationalRole.UNREAD

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الكيان للبصمة."""

        return {
            "object_id": self.object_id,
            "representation": self.representation.as_canonical_content(),
            "relational_role": self.relational_role.as_canonical_content(),
        }


def _refuse_a_buried_component() -> None:
    """افحص الفصلَ على **أنواع** الحقول لا على أسمائها."""

    pairs = (
        (RepresentationRef, RelationalRoleRef),
        (RelationalRoleRef, RepresentationRef),
    )
    for declaring, forbidden in pairs:
        for field in fields(declaring):
            annotation = field.type
            name = (
                annotation.__name__
                if isinstance(annotation, type)
                else str(annotation)
            )
            if forbidden.__name__ in name:
                raise RuntimeError(RELATION_IS_NOT_REPRESENTATION)
        for field in fields(declaring):
            if isinstance(field.type, type) and issubclass(field.type, forbidden):
                raise RuntimeError(RELATION_IS_NOT_REPRESENTATION)


_refuse_a_buried_component()
