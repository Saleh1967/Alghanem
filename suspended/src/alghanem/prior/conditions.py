"""`PK_0`: الحدُّ الأدنى للمعلومات السابقة المنظَّمة — شروطُ الإمكان لا الحقائق.

    PK_0 = {Domain, UnitCriterion, IdentityCriterion, AttributePossibility,
            RelationPossibility, TransformationConditions,
            ConditionsAndPreventers, PreservedTrace, ClosureBlockingRemainder}

**وهي تنظّم الإمكانَ ولا تختار النتيجة** (`PriorInformationOrdersPossibilityNotResult`):
لا يقول هذا المستوى «هذا الشيءُ جنس»، بل يقول: ما الشروطُ التي تجعل من المشروع
أن يُولَد نوعٌ اسمُه «جنس»؟ فمن أودع الجوابَ هنا أودعه في موضع البرهان.

**ولا واقعةَ جاهزةً في هذا المستوى** (`NoReadyMadeFactInThePriorBase`): لا اسمَ
نوعٍ ولا مثيلَ موجودٍ ولا لفظَ لغةٍ مخصوصة؛ ويُفحَص ذلك على أسماء الحقول عند
الاستيراد، لا يُوصَف في التوثيق.

**والتغطيةُ تامّةٌ أو رفض** (`PriorCoverageIsExactNotBestEffort`)، على منهج
`assess_relational_closure` في الطبقة اللغويّة وبوّابةِ الثوابت في النواة:
تُقيَّم المواضعُ التسعةُ كلُّها، ولا يُقبَل نقصٌ ولا تكرار، ولا يُوقَف التقييمُ
عند أوّل ساقط — فالساقطون يُسمَّون جميعًا.

**وكلُّ شرطٍ يُسمّي ما يمنعه ومصدرَ ترخيصه**: شرطٌ لا يمنع شيئًا لا يقيّد
مجالَ الإمكان، وشرطٌ بلا مصدرِ ترخيصٍ دعوى لا شرط.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`، ولا استيرادَ من
`metaalgebra/` ولا `linguistic/` ولا `arabic/` ولا `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest

__all__ = [
    "AN_UNREAD_CONDITION_IS_NOT_A_SATISFIED_ONE",
    "A_CONDITION_NAMES_WHAT_IT_FORBIDS",
    "NO_READY_MADE_FACT_IN_THE_PRIOR_BASE",
    "PRIOR_CONDITION_NAMES",
    "PRIOR_COVERAGE_IS_EXACT_NOT_BEST_EFFORT",
    "PriorCondition",
    "PriorConditionKind",
    "PriorInformationBase",
    "PriorInformationError",
    "PriorLicenseGenus",
]


class PriorInformationError(ValueError):
    """رفضٌ عند الإنشاء في المعلومات السابقة؛ لا حملَ على أقرب حالة."""


NO_READY_MADE_FACT_IN_THE_PRIOR_BASE: Final[str] = (
    "لا واقعةَ جاهزةً في المعلومات السابقة: لا اسمَ نوعٍ ولا مثيلَ موجودٍ ولا "
    "لفظَ لغةٍ مخصوصة؛ ومن أودع «هذا جنس» هنا أودع الجوابَ في موضع البرهان"
)

PRIOR_COVERAGE_IS_EXACT_NOT_BEST_EFFORT: Final[str] = (
    "تغطيةُ شروط الإمكان تامّةٌ بلا نقصٍ ولا تكرار: ناقصُ التغطية يُقرَأ "
    "مكتملًا بالسهو، والمكرّرُ يُرجّح صياغةً على أخرى بلا مُرجِّح"
)

A_CONDITION_NAMES_WHAT_IT_FORBIDS: Final[str] = (
    "الشرطُ يُسمّي ما يمنعه: شرطٌ لا يمنع شيئًا لا يقيّد مجالَ الإمكان، فهو "
    "وصفٌ يُقرَأ قيدًا بالسهو ولا يُسقِط شيئًا عند المخالفة"
)

AN_UNREAD_CONDITION_IS_NOT_A_SATISFIED_ONE: Final[str] = (
    "شرطٌ لم يُقرَأ ليس شرطًا مستوفًى: عضوُ الجهل مُصرَّحٌ به في مفردة الترخيص، "
    "فغيابُ القراءة يُسجَّل غيابًا ولا يُقرَأ استيفاءً"
)


class PriorConditionKind(Enum):
    """مواضعُ المعلومات السابقة التسعة؛ مفردةٌ مغلقةٌ لا عاشرَ لها في هذا المستوى."""

    DOMAIN = "domain"
    UNIT_CRITERION = "unit_criterion"
    IDENTITY_CRITERION = "identity_criterion"
    ATTRIBUTE_POSSIBILITY = "attribute_possibility"
    RELATION_POSSIBILITY = "relation_possibility"
    TRANSFORMATION_CONDITIONS = "transformation_conditions"
    CONDITIONS_AND_PREVENTERS = "conditions_and_preventers"
    PRESERVED_TRACE = "preserved_trace"
    CLOSURE_BLOCKING_REMAINDER = "closure_blocking_remainder"


PRIOR_CONDITION_NAMES: Final[tuple[str, ...]] = tuple(
    kind.value for kind in PriorConditionKind
)
"""أسماءُ المواضع مُشتَقّةٌ من المفردة نفسِها؛ ولا نسخةَ ثانيةً تنحرف عنها."""


class PriorLicenseGenus(Enum):
    """جنسُ ترخيص الشرط؛ وفيه عضوُ جهلٍ مُصرَّحٌ به وعضوٌ مرفوضٌ بالبناء."""

    STIPULATED_FOR_THE_DOMAIN = "stipulated_for_the_domain"
    PRIOR_PROOF = "prior_proof"
    PREFROZEN_INDEPENDENT_INFERENCE = "prefrozen_independent_inference"
    UNREAD = "unread"
    DERIVED_FROM_THE_ONTOLOGY_IT_LICENSES = "derived_from_the_ontology_it_licenses"

    @property
    def licenses_use(self) -> bool:
        """أيُرخِّص هذا الجنسُ استعمالَ الشرط؟ والمرفوضُ مُسمًّى لا مُستنتَج."""

        return self not in (
            PriorLicenseGenus.UNREAD,
            PriorLicenseGenus.DERIVED_FROM_THE_ONTOLOGY_IT_LICENSES,
        )


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PriorInformationError(f"{label} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class PriorCondition:
    """شرطُ إمكانٍ واحد: موضعُه، ونصُّه، وما يمنعه، وجنسُ ترخيصه."""

    condition_id: str
    kind: PriorConditionKind
    statement: str
    what_it_forbids: str
    licensed_by: PriorLicenseGenus

    def __post_init__(self) -> None:
        _require_text(self.condition_id, "مُعرِّفُ الشرط")
        if not isinstance(self.kind, PriorConditionKind):
            raise PriorInformationError("موضعُ الشرط عضوٌ في مفردته المغلقة لا نصٌّ حرّ")
        _require_text(self.statement, f"نصُّ `{self.condition_id}`")
        _require_text(
            self.what_it_forbids,
            f"ما يمنعه `{self.condition_id}`؛ و" + A_CONDITION_NAMES_WHAT_IT_FORBIDS,
        )
        if not isinstance(self.licensed_by, PriorLicenseGenus):
            raise PriorInformationError("جنسُ الترخيص عضوٌ في مفردته المغلقة")

    @property
    def is_usable(self) -> bool:
        """أيصلح هذا الشرطُ أساسًا يُبنى عليه؟ خاصّيّةٌ تُشتَقّ من جنس ترخيصه."""

        return self.licensed_by.licenses_use

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الشرط للبصمة."""

        return {
            "condition_id": self.condition_id,
            "kind": self.kind.value,
            "statement": self.statement,
            "what_it_forbids": self.what_it_forbids,
            "licensed_by": self.licensed_by.value,
        }


@dataclass(frozen=True, slots=True)
class PriorInformationBase:
    """`PK_0`: شروطُ الإمكان التسعةُ مجتمعةً، بتغطيةٍ تامّةٍ ومصدرِ ترخيصٍ لكلٍّ."""

    base_id: str
    domain_note: str
    conditions: tuple[PriorCondition, ...]

    def __post_init__(self) -> None:
        _require_text(self.base_id, "مُعرِّفُ قاعدة المعلومات السابقة")
        _require_text(self.domain_note, "بيانُ المجال الذي تنظّمه القاعدة")
        if not isinstance(self.conditions, tuple) or not self.conditions:
            raise PriorInformationError("القاعدةُ شرطٌ فأكثر")
        for condition in self.conditions:
            if not isinstance(condition, PriorCondition):
                raise PriorInformationError("عضوٌ في الشروط خارج نوعه")
        ids = tuple(condition.condition_id for condition in self.conditions)
        if len(set(ids)) != len(ids):
            raise PriorInformationError("مُعرِّفُ الشرط لا يتكرّر؛ والمكرّرُ يُرفَض لا يُطوى")
        covered = tuple(condition.kind for condition in self.conditions)
        if len(set(covered)) != len(covered):
            raise PriorInformationError(PRIOR_COVERAGE_IS_EXACT_NOT_BEST_EFFORT)
        missing = tuple(
            kind.value for kind in PriorConditionKind if kind not in set(covered)
        )
        if missing:
            raise PriorInformationError(
                PRIOR_COVERAGE_IS_EXACT_NOT_BEST_EFFORT
                + "؛ والمواضعُ الغائبة: "
                + "، ".join(missing)
            )

    @property
    def unusable_condition_ids(self) -> tuple[str, ...]:
        """الشروطُ غيرُ الصالحة أساسًا؛ تُسمَّى جميعًا ولا يُوقَف عند أوّلها."""

        return tuple(
            condition.condition_id
            for condition in self.conditions
            if not condition.is_usable
        )

    @property
    def is_fit_to_found_an_ontology(self) -> bool:
        """أتصلح هذه القاعدةُ أساسًا لأنطولوجيا؟ متى كان كلُّ شرطٍ فيها مُرخَّصًا."""

        return not self.unusable_condition_ids

    def condition(self, kind: PriorConditionKind) -> PriorCondition:
        """الشرطُ بموضعه؛ والغيابُ رفضٌ لا `None` يُقرأ صمتًا."""

        for condition in self.conditions:
            if condition.kind is kind:
                return condition
        raise PriorInformationError(f"لا شرطَ في القاعدة بموضع `{kind.value}`")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى القاعدة للبصمة."""

        return {
            "base_id": self.base_id,
            "domain_note": self.domain_note,
            "conditions": [
                condition.as_canonical_content()
                for condition in sorted(
                    self.conditions, key=lambda item: item.condition_id
                )
            ],
        }

    @property
    def content_id(self) -> str:
        """بصمةُ القاعدة؛ وأنطولوجيا على بصمةٍ غيرِها أنطولوجيا قاعدةٍ أخرى."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


_FORBIDDEN_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "genus",
    "individual",
    "event",
    "quantity",
    "reference",
    "term",
    "predicate",
    "nisbah",
    "arabic",
    "root",
    "fact",
)
"""أسماءٌ لا يجوز أن تظهر حقلًا في هذا المستوى؛ فالواقعةُ الجاهزةُ تُمنَع بالبناء."""

_DECLARING_TYPES: Final[tuple[type, ...]] = (PriorCondition, PriorInformationBase)

for _declaring_type in _DECLARING_TYPES:  # pragma: no cover - import guard
    for _field in fields(_declaring_type):
        for _marker in _FORBIDDEN_FIELD_MARKERS:
            if _marker in _field.name.lower():
                raise RuntimeError(NO_READY_MADE_FACT_IN_THE_PRIOR_BASE)

if len(PRIOR_CONDITION_NAMES) != 9:  # pragma: no cover - import guard
    raise RuntimeError(PRIOR_COVERAGE_IS_EXACT_NOT_BEST_EFFORT)
