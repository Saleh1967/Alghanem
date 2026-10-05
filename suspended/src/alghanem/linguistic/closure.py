"""`Σ_L`: الإغلاقُ النسبيُّ خمسةُ مكوّناتٍ مجتمعة، وناتجُه ما قبلَ الإفادة لا الإفادة.

    RelationalClosure =
        ArgumentsClosed
        ∧ OperatorsScoped
        ∧ ConstraintsLicensed
        ∧ ReferencesResolved
        ∧ NoCrossBoundaryActiveResidual

**وامتلاءُ الحجج مكوّنٌ لا إغلاق** (`ArgumentFillingIsNotClosure`): قد تمتلئ
المواضعُ ويبقى مرجعٌ غيرُ محلول، أو نطاقُ نفيٍ غيرُ محسوم، أو شرطٌ مفتوح، أو
مُشغِّلٌ بلا نطاق، أو قيدٌ زمنيٌّ متعارض، أو بقيّةٌ عابرةٌ للحدّ. فمن قرأ
الامتلاءَ إغلاقًا قرأ خُمسَ الشرط كلَّه.

**والتغطيةُ تامّةٌ أو رفض** (`ClosureCoverageIsExactNotBestEffort`)، على منهج
بوّابة الثوابت في النواة: تُقيَّم المكوّناتُ الخمسةُ كلُّها، ولا يُقبَل نقصٌ
ولا تكرار، ولا يُوقَف التقييمُ عند أوّل ساقط — فالساقطون يُسمَّون جميعًا.

**والإغلاقُ لا يُنتج الإفادةَ آليًّا** (`RelationalClosureIsNotIfadah`): ناتجُه
الأوّلُ `PreIfadahClosure` وحدَه، والإفادةُ تحتاج بعده قوّةً مُرخَّصةً وسياقًا
لازمًا. فـ«هل قام زيد؟» نسبتُها مكتملةٌ وليست إخبارًا.

**ولا مفردةَ إفادةٍ ثانيةٌ هنا** (`IfadaVocabularyIsNotDuplicated`): مفردةُ
الإفادة القائمةُ في الطبقة العربيّة (`IfadaStanding`) هي الوحيدة، وربطُها بهذا
الإغلاق دالّةُ اشتقاقٍ في اتّجاهٍ واحدٍ تُبنى في `Σ_AR` لا هنا؛ وبناؤها هنا
يقلب التبعيّةَ `linguistic → arabic` ويُنشئ نسختين لمفردةٍ واحدة.

تسجيلٌ لا سلطة: لا حكمَ هنا، ولا استيرادَ من `kernel/` ولا من `arabic/`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

__all__ = [
    "ARGUMENT_FILLING_IS_NOT_CLOSURE",
    "CLOSURE_COMPONENT_NAMES",
    "CLOSURE_COVERAGE_IS_EXACT_NOT_BEST_EFFORT",
    "IFADA_PREREQUISITE_NAMES",
    "IFADA_VOCABULARY_IS_NOT_DUPLICATED",
    "RELATIONAL_CLOSURE_IS_NOT_IFADAH",
    "ClosureComponent",
    "ClosureComponentReading",
    "IfadaPrerequisite",
    "RelationalClosureAssessment",
    "RelationalClosureError",
    "RelationalClosureStanding",
    "assess_relational_closure",
]


class RelationalClosureError(ValueError):
    """رفضٌ عند التقييم: تغطيةٌ ناقصةٌ أو مكرّرةٌ لمكوّنات الإغلاق."""


ARGUMENT_FILLING_IS_NOT_CLOSURE: Final[str] = (
    "امتلاءُ مواضع الحجج مكوّنٌ من الإغلاق لا الإغلاقُ نفسُه: مرجعٌ غيرُ محلولٍ "
    "أو نطاقٌ غيرُ محسومٍ أو بقيّةٌ عابرةٌ للحدّ تُبقي النسبةَ مفتوحةً وإن امتلأت"
)

CLOSURE_COVERAGE_IS_EXACT_NOT_BEST_EFFORT: Final[str] = (
    "تغطيةُ مكوّنات الإغلاق تامّةٌ بلا نقصٍ ولا تكرار: ناقصُ التغطية يُقرَأ "
    "مغلقًا بالسهو، والمكرّرُ يُرجّح قراءةً على أخرى بلا مُرجِّح"
)

RELATIONAL_CLOSURE_IS_NOT_IFADAH: Final[str] = (
    "الإغلاقُ النسبيُّ ليس إفادة: ناتجُه `PreIfadahClosure`، والإفادةُ نسبةٌ "
    "مغلقةٌ مع قوّةٍ مُرخَّصةٍ وسياقٍ لازم؛ فـ«هل قام زيد؟» مكتملةُ النسبة وليست خبرًا"
)

IFADA_VOCABULARY_IS_NOT_DUPLICATED: Final[str] = (
    "لا مفردةَ إفادةٍ ثانية: المفردةُ القائمةُ في الطبقة العربيّة هي الوحيدة، "
    "وربطُها بالإغلاق اشتقاقٌ في اتّجاهٍ واحدٍ موضعُه `Σ_AR` لا هذه النواة"
)


class ClosureComponent(Enum):
    """مكوّناتُ الإغلاق الخمسة؛ مفردةٌ مغلقةٌ لا سادسَ لها في هذا التوقيع."""

    ARGUMENTS_CLOSED = "arguments_closed"
    OPERATORS_SCOPED = "operators_scoped"
    CONSTRAINTS_LICENSED = "constraints_licensed"
    REFERENCES_RESOLVED = "references_resolved"
    NO_CROSS_BOUNDARY_ACTIVE_RESIDUAL = "no_cross_boundary_active_residual"


CLOSURE_COMPONENT_NAMES: Final[tuple[str, ...]] = tuple(
    component.value for component in ClosureComponent
)
"""أسماءُ المكوّنات مُشتَقّةٌ من المفردة نفسِها؛ ولا نسخةَ ثانيةً تنحرف عنها."""


class IfadaPrerequisite(Enum):
    """شروطُ الإفادة الثلاثة؛ تُسمّى هنا ولا تُقاس هنا."""

    CLOSED_NISBAH = "closed_nisbah"
    LICENSED_FORCE = "licensed_force"
    REQUIRED_CONTEXT = "required_context"


IFADA_PREREQUISITE_NAMES: Final[tuple[str, ...]] = tuple(
    prerequisite.value for prerequisite in IfadaPrerequisite
)
"""الشروطُ الثلاثة بأسمائها؛ والإغلاقُ أوّلُها لا كلُّها."""


class RelationalClosureStanding(Enum):
    """منزلةُ النسبة بعد التقييم؛ وأعلى ما تبلغه هنا ما قبلَ الإفادة."""

    PRE_IFADAH_CLOSURE_REACHED = "بلغت_إغلاقًا_نسبيًّا_ما_قبل_الإفادة"
    NOT_CLOSED = "لم_تُغلَق_ومكوّناتُ_نقصها_مُسمّاة"


@dataclass(frozen=True, slots=True)
class ClosureComponentReading:
    """قراءةُ مكوّنٍ واحد: أتحقّق؟ وما الذي بقي إن لم يتحقّق؟"""

    component: ClosureComponent
    is_satisfied: bool
    what_remains_open: str

    def __post_init__(self) -> None:
        if not isinstance(self.component, ClosureComponent):
            raise RelationalClosureError("المكوّنُ عضوٌ في مفردته المغلقة")
        if type(self.is_satisfied) is not bool:
            raise RelationalClosureError("تحقُّقُ المكوّن قيمةٌ ثنائيّةٌ صريحة")
        if not isinstance(self.what_remains_open, str):
            raise RelationalClosureError("ما بقي مفتوحًا نصٌّ مُصرَّحٌ به")
        if not self.is_satisfied and not self.what_remains_open.strip():
            raise RelationalClosureError(
                "مكوّنٌ غيرُ متحقّقٍ يُسمّي ما بقي مفتوحًا؛ والصمتُ عنه يُخفي سببَ عدم الإغلاق"
            )


@dataclass(frozen=True, slots=True)
class RelationalClosureAssessment:
    """تقييمُ الإغلاق كاملًا: منزلةٌ مُشتَقّةٌ، ومكوّناتٌ ساقطةٌ مُسمّاةٌ كلُّها."""

    nisbah_id: str
    readings: tuple[ClosureComponentReading, ...]
    standing: RelationalClosureStanding
    unsatisfied_components: tuple[ClosureComponent, ...]

    @property
    def is_pre_ifadah_closed(self) -> bool:
        """أبلغت ما قبلَ الإفادة؟ ولا تُقرَأ هذه إفادةً بحال."""

        return self.standing is RelationalClosureStanding.PRE_IFADAH_CLOSURE_REACHED

    @property
    def remaining_ifada_prerequisites(self) -> tuple[IfadaPrerequisite, ...]:
        """ما بقي من شروط الإفادة بعد الإغلاق؛ وهما اثنان لا يُنتجهما الإغلاق."""

        if not self.is_pre_ifadah_closed:
            return tuple(IfadaPrerequisite)
        return (
            IfadaPrerequisite.LICENSED_FORCE,
            IfadaPrerequisite.REQUIRED_CONTEXT,
        )


def assess_relational_closure(
    nisbah_id: str, readings: tuple[ClosureComponentReading, ...]
) -> RelationalClosureAssessment:
    """قيّم الإغلاقَ بتغطيةٍ تامّةٍ للمكوّنات الخمسة؛ ولا تقف عند أوّل ساقط."""

    if not isinstance(nisbah_id, str) or not nisbah_id.strip():
        raise RelationalClosureError("مُعرِّفُ النسبة نصٌّ غير فارغ")
    if not isinstance(readings, tuple):
        raise RelationalClosureError("القراءاتُ مجموعةٌ مُصرَّحٌ بها")
    for reading in readings:
        if not isinstance(reading, ClosureComponentReading):
            raise RelationalClosureError("عضوٌ في القراءات خارج نوعه")
    covered = tuple(reading.component for reading in readings)
    if len(set(covered)) != len(covered):
        raise RelationalClosureError(CLOSURE_COVERAGE_IS_EXACT_NOT_BEST_EFFORT)
    if set(covered) != set(ClosureComponent):
        raise RelationalClosureError(CLOSURE_COVERAGE_IS_EXACT_NOT_BEST_EFFORT)
    unsatisfied = tuple(
        reading.component for reading in readings if not reading.is_satisfied
    )
    standing = (
        RelationalClosureStanding.PRE_IFADAH_CLOSURE_REACHED
        if not unsatisfied
        else RelationalClosureStanding.NOT_CLOSED
    )
    return RelationalClosureAssessment(
        nisbah_id=nisbah_id,
        readings=readings,
        standing=standing,
        unsatisfied_components=unsatisfied,
    )
