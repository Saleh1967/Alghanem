"""G0.ST — محورا المنزلة: البنيويّ والتجريبيّ، مفصولين بالبناء لا بالنصّ.

هذه الوحدةُ تحمل مفردتَي المنزلة وعقدَ جمعهما في سجلٍّ واحدٍ **دون دمجهما في
حقلٍ واحد**. ولا تُصدِر حكمًا: لا تقرأ دليلًا، ولا تشتقّ منزلةً من أخرى، ولا
تعرف بوّابةً واحدة.

**القانونُ المركزيّ الذي تحمله بالبناء:**

    MissingEmpiricalEvidence  ⇏  MissingStructuralProof
    FormalStructuralProof     ⇏  EmpiricalReality

والثاني معلنٌ من قبلُ في `G0.MA`؛ والأوّلُ هو الذي كان ناقصًا، وبغيابه صار
`INDEPENDENT_TARGET_MISSING` — وهو نقصٌ على المحور التجريبيّ وحدَه — يُقرأ سقفًا
على الدعوى البنيويّة كلِّها.

**والاستقلالُ المطلوب للمحور البنيويّ استقلالُ مواصفةٍ لا استقلالُ هدفٍ مقيس:**
أن يُجمَّد العقد `(Pre, Post, Inv, Cl, Trace)` ببصمة محتواه **قبل** أن توجد
الدالّةُ التي تدّعي تحقيقَه. وعقدٌ كُتب بعد دالّته ليس عقدًا
(`A_CONTRACT_WRITTEN_AFTER_ITS_FUNCTION_IS_NOT_A_CONTRACT`)، على منهج
`A_RIVAL_WRITTEN_AFTER_THE_RESULT_IS_NOT_A_RIVAL` المُجمَّد في تجربة `VV`.

**ولا منزلةَ بنيويّةً مطلقة:** كلُّ منزلةٍ بنيويّةٍ منسوبةٌ إلى `Σ` مُسمّاةٍ
مبصومةٍ بنطاقها، والنسبةُ في اسم القيمة نفسِها لا في حاشيةٍ بجانبها.

**ورتبةُ الاستقلال تاريخيّةٌ لا تُمنَح بأثرٍ رجعيّ:** تنفيذٌ كان قائمًا يومَ
جُمِّد عقدُه لا يبلغ أكثر من `RETROSPECTIVE_CONFORMANCE`؛ ومنحُه الرتبةَ الأقوى
يجعل التسجيلَ القبليَّ رجعيًّا، وهو العيبُ الذي وُجد التسجيلُ القبليُّ لمنعه.

تسجيلٌ لا سلطة: لا ولادةَ ولا تجميدَ `E0` ولا حكم، ولا تستورد هذه الوحدةُ من
`kernel/` حرفًا.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from ..canonical_content import is_canonical_digest

__all__ = [
    "A_CONTRACT_WRITTEN_AFTER_ITS_FUNCTION_IS_NOT_A_CONTRACT",
    "EMPIRICAL_TARGET_INDEPENDENCE_IS_EMPIRICAL_ONLY",
    "FORMAL_STRUCTURAL_PROOF_IS_NOT_EMPIRICAL_REALITY",
    "MISSING_EMPIRICAL_EVIDENCE_IS_NOT_MISSING_STRUCTURAL_PROOF",
    "NO_AXIS_COLLAPSE",
    "NO_STRUCTURAL_STANDING_WITHOUT_ITS_FROZEN_SIGMA",
    "SPECIFICATION_INDEPENDENCE_IS_NOT_EMPIRICAL_TARGET_INDEPENDENCE",
    "DualStanding",
    "EmpiricalStanding",
    "ImplementationConformanceRecord",
    "MetaAlgebraStandingError",
    "SpecificationIndependenceGrade",
    "SpecificationSetRef",
    "StructuralStanding",
]


class MetaAlgebraStandingError(ValueError):
    """رفضٌ عند الإنشاء: محورٌ يُدمَج بآخر، أو منزلةٌ بلا `Σ` تُنسَب إليها."""


MISSING_EMPIRICAL_EVIDENCE_IS_NOT_MISSING_STRUCTURAL_PROOF: Final[str] = (
    "غيابُ الشاهد التجريبيّ نقصٌ على المحور التجريبيّ وحدَه؛ لا يخفض منزلةً "
    "بنيويّةً ولا يؤجّلها ولا يقيّدها"
)

FORMAL_STRUCTURAL_PROOF_IS_NOT_EMPIRICAL_REALITY: Final[str] = (
    "البرهانُ البنيويّ على جبرٍ مُجمَّد لا يُثبت مطابقةَ تفسيرِه للواقع الخارجيّ؛ "
    "والاتّجاهُ هذا مُعلَنٌ في `G0.MA` ولا يُعاد اشتقاقُه هنا"
)

SPECIFICATION_INDEPENDENCE_IS_NOT_EMPIRICAL_TARGET_INDEPENDENCE: Final[str] = (
    "الاستقلالُ الذي يطلبه المحورُ البنيويّ استقلالُ العقد عن دالّته، لا استقلالُ "
    "هدفٍ مقيسٍ عن قواعد النموذج"
)

EMPIRICAL_TARGET_INDEPENDENCE_IS_EMPIRICAL_ONLY: Final[str] = (
    "استقلالُ هدف إعادة البناء شرطٌ على المحور التجريبيّ حيث وُضِع، ولا يُستورَد "
    "إلى المحور البنيويّ باسمٍ آخر"
)

A_CONTRACT_WRITTEN_AFTER_ITS_FUNCTION_IS_NOT_A_CONTRACT: Final[str] = (
    "A_CONTRACT_WRITTEN_AFTER_ITS_FUNCTION_IS_NOT_A_CONTRACT"
)

NO_STRUCTURAL_STANDING_WITHOUT_ITS_FROZEN_SIGMA: Final[str] = (
    "لا منزلةَ بنيويّةً بلا `Σ` مُسمّاةٍ مبصومةٍ بنطاقها؛ ولا `PROVED` مطلقةً في "
    "هذا المستودع"
)

NO_AXIS_COLLAPSE: Final[str] = (
    "لا يُجمَع المحوران في حقلٍ واحدٍ ولا يُرتَّب أحدُهما على الآخر ولا يُشتَقّ "
    "منه؛ والرفضُ عند الإنشاء لا تصحيحٌ عند القراءة"
)


class StructuralStanding(Enum):
    """منزلةُ الدعوى بالنسبة إلى مواصفةٍ مُجمَّدة، لا بالنسبة إلى العالم.

    ولا عضوَ فيها اسمُه `PROVED` مجرّدًا: النسبةُ إلى `Σ` جزءٌ من الاسم، فلا
    يُقرَأ العضوُ يومًا برهانًا مطلقًا بسهوٍ في القراءة.
    """

    STRUCTURALLY_PROVED_RELATIVE_TO_SIGMA = "STRUCTURALLY_PROVED_RELATIVE_TO_SIGMA"
    STRUCTURALLY_REFUTED_RELATIVE_TO_SIGMA = "STRUCTURALLY_REFUTED_RELATIVE_TO_SIGMA"
    STRUCTURALLY_UNDERPOWERED = "STRUCTURALLY_UNDERPOWERED"
    STRUCTURALLY_UNDEFINED = "STRUCTURALLY_UNDEFINED"
    NOT_ASSESSED = "NOT_ASSESSED"

    @property
    def requires_frozen_sigma(self) -> bool:
        """أتلزم هذه المنزلةُ `Σ` مُسمّاةً؟ الإلزامُ مُصرَّحٌ به لا مُستنتَج."""

        return self in _SIGMA_BEARING_STANDINGS


class EmpiricalStanding(Enum):
    """منزلةُ الدعوى بالنسبة إلى قياسٍ خارج المواصفة المُجمَّدة.

    و`INDEPENDENT_TARGET_MISSING` عضوٌ هنا وحدَه؛ ولا نظيرَ له في المفردة
    البنيويّة، لأنّه وصفُ نقصٍ في الشاهد لا وصفُ خللٍ في البنية.
    """

    NOT_TESTED = "NOT_TESTED"
    INDEPENDENT_TARGET_MISSING = "INDEPENDENT_TARGET_MISSING"
    EMPIRICALLY_UNDERPOWERED = "EMPIRICALLY_UNDERPOWERED"
    EMPIRICALLY_REFUTED_IN_SCOPE = "EMPIRICALLY_REFUTED_IN_SCOPE"
    EMPIRICALLY_SUPPORTED_IN_SCOPE = "EMPIRICALLY_SUPPORTED_IN_SCOPE"


class SpecificationIndependenceGrade(Enum):
    """رتبةُ استقلال العقد عن دالّته، مرتّبةً تاريخيًّا لا تقديريًّا."""

    PROSPECTIVE_SPECIFICATION_INDEPENDENT = "PROSPECTIVE_SPECIFICATION_INDEPENDENT"
    RETROSPECTIVE_CONFORMANCE = "RETROSPECTIVE_CONFORMANCE"
    NOT_ESTABLISHED = "NOT_ESTABLISHED"


_SIGMA_BEARING_STANDINGS: Final[frozenset[StructuralStanding]] = frozenset(
    {
        StructuralStanding.STRUCTURALLY_PROVED_RELATIVE_TO_SIGMA,
        StructuralStanding.STRUCTURALLY_REFUTED_RELATIVE_TO_SIGMA,
    }
)


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise MetaAlgebraStandingError(f"{label} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class SpecificationSetRef:
    """إشارةٌ إلى `Σ`: اسمُها، وبصمةُ محتواها، ونطاقُها المُعلَن.

    البصمةُ شرطُ إنشاءٍ لا زينة: «مواصفةٌ مُجمَّدة» بلا بصمةٍ دعوى تجميدٍ لا
    يمكن التحقّق منها لاحقًا.
    """

    sigma_id: str
    content_id: str
    scope: str

    def __post_init__(self) -> None:
        _require_text(self.sigma_id, "اسمُ المواصفة")
        _require_text(self.scope, "نطاقُ المواصفة")
        if not is_canonical_digest(self.content_id):
            raise MetaAlgebraStandingError(
                "بصمةُ المواصفة بصمةٌ قانونيّةٌ بشكلها؛ ومواصفةٌ بلا بصمةٍ ليست مُجمَّدة"
            )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الإشارة للبصمة."""

        return {
            "sigma_id": self.sigma_id,
            "content_id": self.content_id,
            "scope": self.scope,
        }


@dataclass(frozen=True, slots=True)
class ImplementationConformanceRecord:
    """موقفُ تنفيذٍ بعينه من عقدٍ مُجمَّد، برتبةٍ تحكمها الأسبقيّةُ التاريخيّة.

    `implementation_predates_contract` واقعةٌ تاريخيّةٌ يُصرّح بها المُسجِّل، ومنها
    تُقيَّد الرتبة: تنفيذٌ سابقٌ لعقده لا يبلغ
    `PROSPECTIVE_SPECIFICATION_INDEPENDENT` بحال.
    """

    implementation_id: str
    specification: SpecificationSetRef
    implementation_predates_contract: bool
    grade: SpecificationIndependenceGrade
    reason: str

    def __post_init__(self) -> None:
        _require_text(self.implementation_id, "اسمُ التنفيذ")
        _require_text(self.reason, "سببُ الرتبة")
        if not isinstance(self.specification, SpecificationSetRef):
            raise MetaAlgebraStandingError("المواصفةُ إشارةُ `Σ` لا نصٌّ مرسَل")
        if type(self.implementation_predates_contract) is not bool:
            raise MetaAlgebraStandingError(
                "أسبقيّةُ التنفيذ على عقده واقعةٌ منطقيّةٌ مُصرَّحٌ بها، لا قيمةٌ تُحمَل"
            )
        if not isinstance(self.grade, SpecificationIndependenceGrade):
            raise MetaAlgebraStandingError("الرتبةُ عضوٌ في مفردتها المغلقة")
        if (
            self.implementation_predates_contract
            and self.grade
            is SpecificationIndependenceGrade.PROSPECTIVE_SPECIFICATION_INDEPENDENT
        ):
            raise MetaAlgebraStandingError(
                "تنفيذٌ سابقٌ لعقده أقصى ما يبلغ `RETROSPECTIVE_CONFORMANCE`؛ "
                f"و{A_CONTRACT_WRITTEN_AFTER_ITS_FUNCTION_IS_NOT_A_CONTRACT}"
            )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الموقف للبصمة."""

        return {
            "implementation_id": self.implementation_id,
            "specification": self.specification.as_canonical_content(),
            "implementation_predates_contract": self.implementation_predates_contract,
            "grade": self.grade.value,
            "reason": self.reason,
        }


@dataclass(frozen=True, slots=True)
class DualStanding:
    """محورا المنزلة مجموعَين في سجلٍّ واحدٍ **بحقلين اثنين لا بحقلٍ واحد**.

    ولا دالّةَ في هذه الوحدةِ تُرجِع منزلةً واحدةً تجمعهما، ولا تُشتَقّ إحداهما
    من الأخرى؛ فالزوج:

        (STRUCTURALLY_PROVED_RELATIVE_TO_SIGMA, INDEPENDENT_TARGET_MISSING)

    زوجٌ مقبولٌ بالبناء، لا تناقضٌ يُصحَّح.
    """

    structural: StructuralStanding
    empirical: EmpiricalStanding
    specification: SpecificationSetRef | None
    independence_grade: SpecificationIndependenceGrade
    reason: str

    def __post_init__(self) -> None:
        if not isinstance(self.structural, StructuralStanding):
            raise MetaAlgebraStandingError("المنزلةُ البنيويّة عضوٌ في مفردتها المغلقة")
        if not isinstance(self.empirical, EmpiricalStanding):
            raise MetaAlgebraStandingError("المنزلةُ التجريبيّة عضوٌ في مفردتها المغلقة")
        if not isinstance(self.independence_grade, SpecificationIndependenceGrade):
            raise MetaAlgebraStandingError("رتبةُ الاستقلال عضوٌ في مفردتها المغلقة")
        _require_text(self.reason, "سببُ المنزلتين")
        if self.structural.requires_frozen_sigma:
            if not isinstance(self.specification, SpecificationSetRef):
                raise MetaAlgebraStandingError(
                    NO_STRUCTURAL_STANDING_WITHOUT_ITS_FROZEN_SIGMA
                )
            if (
                self.independence_grade
                is SpecificationIndependenceGrade.NOT_ESTABLISHED
            ):
                raise MetaAlgebraStandingError(
                    "منزلةٌ بنيويّةٌ منسوبةٌ إلى `Σ` تلزمها رتبةُ استقلالٍ مُثبَتة؛ "
                    f"و{SPECIFICATION_INDEPENDENCE_IS_NOT_EMPIRICAL_TARGET_INDEPENDENCE}"
                )
        elif self.specification is not None and not isinstance(
            self.specification, SpecificationSetRef
        ):
            raise MetaAlgebraStandingError("المواصفةُ إشارةُ `Σ` أو غيابٌ مُصرَّحٌ به")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المنزلتين للبصمة؛ حقلان اثنان، ولا ثالثَ يجمعهما."""

        specification = (
            None
            if self.specification is None
            else self.specification.as_canonical_content()
        )
        return {
            "structural": self.structural.value,
            "empirical": self.empirical.value,
            "specification": specification,
            "independence_grade": self.independence_grade.value,
            "reason": self.reason,
        }


_COLLAPSING_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "combined",
    "overall",
    "merged",
    "verdict",
    "score",
    "rank",
)

_AXIS_BEARING_TYPES: Final[tuple[type, ...]] = (
    DualStanding,
    ImplementationConformanceRecord,
    SpecificationSetRef,
)

for _declaring_type in _AXIS_BEARING_TYPES:  # pragma: no cover - import guard
    for _field in fields(_declaring_type):
        if any(marker in _field.name for marker in _COLLAPSING_FIELD_MARKERS):
            raise RuntimeError(NO_AXIS_COLLAPSE)
