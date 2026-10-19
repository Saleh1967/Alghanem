"""مرجعُ شرطٍ سابقٍ مبصوم: ملكُ `PK_0` لا ملكُ الطبقة التي تستعمله.

    PriorConditionRef = ConditionId + Place + BaseId + BaseDigest

**والمرجعُ ملكُ المعلومات السابقة** (`AConditionReferenceBelongsToThePriorBase`):
الشرطُ يُسجَّل هنا، فمرجعُه يُسجَّل هنا؛ ولو وُضِع في الأنطولوجيا العامّة
لاضطرّت كلُّ طبقةٍ فوقها أن تستوردها لتُشير إلى شيءٍ تملكه القاعدةُ السابقة.
وتستعمله `O_0` و`O_L²` وما فوقهما مرجعًا واحدًا لا نسخًا تتفرّق.

**والمرجعُ يُشتَقّ ولا يُنشَأ** (`AReferenceIsDerivedNotConstructed`): لا يوجد
مرجعٌ تامُّ البنية إلّا من طريق `of(...)`. والنداءُ المباشرُ لا يُصدِر مرجعًا
ضعيفَ المنزلة يُقرَأ بعدُ ويُردّ، بل **لا يُصدِر مرجعًا أصلًا**: السلطةُ شرطُ
تكوُّنٍ لا صفةٌ تُضاف بعد الوجود. ومع ذلك يبقى `verify_against` موضعَ إعادةِ
اشتقاقٍ من القاعدة الحيّة، فحقولٌ صحيحةٌ شكلًا لا تُقرَأ اشتقاقًا.

**والشرطُ هنا قائمٌ مُسجَّلٌ مُرخَّصٌ صالحٌ للاستعمال، لا «مولود»**
(`NoBirthLanguageAtThisStage`): لا بوّابةَ ولادةٍ في هذه المرحلة، فوصفُ الشرط
بالولادة يرفع رتبةَ التسجيل إلى رتبةٍ لم تَقُم بعد.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`، ولا استيرادَ من
`ontology/` ولا `metaalgebra/` ولا `linguistic/` ولا `arabic/` ولا `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final

from .conditions import (
    PriorCondition,
    PriorConditionKind,
    PriorInformationBase,
    PriorInformationError,
)

__all__ = [
    "A_CONDITION_REFERENCE_BELONGS_TO_THE_PRIOR_BASE",
    "A_REFERENCE_IS_DERIVED_NOT_CONSTRUCTED",
    "NO_BIRTH_LANGUAGE_AT_THIS_STAGE",
    "PriorConditionRef",
]


A_CONDITION_REFERENCE_BELONGS_TO_THE_PRIOR_BASE: Final[str] = (
    "مرجعُ الشرط ملكُ المعلومات السابقة: الشرطُ مُسجَّلٌ في `PK_0`، فمرجعُه "
    "مُسجَّلٌ معه؛ ونسخُه في طبقةٍ فوقه يجعل لكلّ طبقةٍ مرجعًا خاصًّا يتفرّق عن "
    "أصله بلا ما يردُّه"
)

A_REFERENCE_IS_DERIVED_NOT_CONSTRUCTED: Final[str] = (
    "المرجعُ يُشتَقّ ولا يُنشَأ: لا مرجعَ تامَّ البنية إلّا من طريق الاشتقاق من "
    "قاعدةٍ قائمة، فالسلطةُ شرطُ تكوُّنٍ لا صفةٌ تُضاف بعد الوجود؛ ونداءٌ مباشرٌ "
    "بحقولٍ صحيحةٍ شكلًا لا يُصدِر مرجعًا من جنس المراجع أصلًا"
)

NO_BIRTH_LANGUAGE_AT_THIS_STAGE: Final[str] = (
    "الشرطُ مُسجَّلٌ قائمٌ مُرخَّصٌ صالحٌ للاستعمال، لا «مولود»: لا بوّابةَ ولادةٍ "
    "في هذه المرحلة، ووصفُ التسجيل بالولادة يرفعه إلى رتبةٍ لم تَقُم بعدُ"
)


class _DerivationWitness:
    """شاهدُ اشتقاقٍ واحدٌ لا يُنشَأ ثانيةً؛ يُوصَد بابُه عند تمام الاستيراد."""

    __slots__ = ()

    def __init__(self) -> None:
        if _WITNESS_IS_ISSUED:
            raise PriorInformationError(A_REFERENCE_IS_DERIVED_NOT_CONSTRUCTED)


_WITNESS_IS_ISSUED: bool = False
_DERIVATION_WITNESS: Final[_DerivationWitness] = _DerivationWitness()
_WITNESS_IS_ISSUED = True


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PriorInformationError(f"{label} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class PriorConditionRef:
    """إشارةٌ إلى شرطٍ قائمٍ مُرخَّصٍ في `PK_0`: موضعُه، ومُعرِّفُه، وبصمةُ قاعدته."""

    condition_id: str
    place: PriorConditionKind
    base_id: str
    base_content_id: str
    derivation_witness: object = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self.derivation_witness is not _DERIVATION_WITNESS:
            raise PriorInformationError(A_REFERENCE_IS_DERIVED_NOT_CONSTRUCTED)
        _require_text(self.condition_id, "مُعرِّفُ الشرط المُشارِ إليه")
        if not isinstance(self.place, PriorConditionKind):
            raise PriorInformationError("موضعُ الشرط عضوٌ في مفردة `PK_0` المغلقة")
        _require_text(self.base_id, "مُعرِّفُ القاعدة المُشارِ إليها")
        _require_text(self.base_content_id, "بصمةُ القاعدة المُشارِ إليها")

    @classmethod
    def of(
        cls, base: PriorInformationBase, place: PriorConditionKind
    ) -> PriorConditionRef:
        """اشتقّ المرجعَ من قاعدةٍ قائمة؛ وشرطٌ غيرُ صالحٍ للاستعمال لا يُشار إليه."""

        if not isinstance(base, PriorInformationBase):
            raise PriorInformationError(
                "المرجعُ يُشتَقّ من قاعدةٍ قائمةٍ لا من اسمٍ حرّ؛ و"
                + A_REFERENCE_IS_DERIVED_NOT_CONSTRUCTED
            )
        if not isinstance(place, PriorConditionKind):
            raise PriorInformationError("موضعُ الشرط عضوٌ في مفردة `PK_0` المغلقة")
        condition: PriorCondition = base.condition(place)
        if not condition.is_usable:
            raise PriorInformationError(
                f"الشرطُ `{condition.condition_id}` غيرُ مُرخَّصٍ للاستعمال، فلا "
                "يُشار إليه ولا يُبنى عليه ترخيصٌ فوقه"
            )
        return cls(
            condition_id=condition.condition_id,
            place=condition.kind,
            base_id=base.base_id,
            base_content_id=base.content_id,
            derivation_witness=_DERIVATION_WITNESS,
        )

    def verify_against(self, base: PriorInformationBase) -> bool:
        """أعِد اشتقاقَ المرجع من القاعدة الحيّة وقارنه حقلًا حقلًا."""

        if not isinstance(base, PriorInformationBase):
            raise PriorInformationError("إعادةُ التحقّق تكون من قاعدةٍ قائمةٍ لا من اسم")
        if base.base_id != self.base_id or base.content_id != self.base_content_id:
            return False
        try:
            rederived = PriorConditionRef.of(base, self.place)
        except PriorInformationError:
            return False
        return rederived == self

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المرجع للبصمة؛ وشاهدُ الاشتقاق ليس محتوًى يُنقَل."""

        return {
            "condition_id": self.condition_id,
            "place": self.place.value,
            "base_id": self.base_id,
            "base_content_id": self.base_content_id,
        }


def _refuse_a_second_witness() -> None:  # pragma: no cover - import guard
    try:
        _DerivationWitness()
    except PriorInformationError:
        return
    raise RuntimeError(A_REFERENCE_IS_DERIVED_NOT_CONSTRUCTED)


_refuse_a_second_witness()
