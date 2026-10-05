"""قطاعاتُ العقدة الليفيّة فوق الثنائيّ {0,1}: تعدادُها، وتمييزُ أجناسها.

وصلت هذه الشجرةَ بنيةٌ صاعدةٌ من التمييز الثنائيّ بين الساكن والمتحرّك، قيل
إنّ قمّتها **ثلاثةُ قطاعاتٍ لحزمةٍ واحدة**: قانونُ الابتداء، وقانونُ الوقف،
وقانونُ الوصل العامّ. وهذه الوحدة تُعدّ القطاعاتِ عدًّا وتُميّز الأجناسَ
تمييزًا، فتفترق الأربعةُ التي جُمِعت في جدولٍ واحد::

    Section(B → E)        != Labelling(Occurrences → E)
    ALabelling            != ItsPushforwardMeasure
    AStipulatedConstant   != AMeasuredConstant
    ADeclaredChainStep    != ItsRecomputedValue

**أوّلًا: القطاعُ يُعدّ فلا يُوصَف.** القطاعُ `s: B → E` بشرط `π∘s = id_B`
يُسنِد نقطةً **فوق كلّ نقطةٍ قاعديّة**، فعدّتُه حاصلُ ضرب أحجام الألياف:
`|Γ(π)| = 1 × 3 = 3`. والثلاثةُ مُعدَّدةٌ ههنا بأعيانها، وكلُّ واحدٍ منها
يأخذ «سكون» عند `b=0` وحركةً عند `b=1`؛ فتمايزُها في **اختيار الحركة** لا في
اختيار الليف. وموافقةُ العدد ٣ للعدد ٣ في الجدول الوارد موافقةٌ حسابيّةٌ لا
بنيويّة، وتُسجَّل كذلك (`THE_COUNT_THREE_IS_NOT_THE_SAME_THREE`).

**ثانيًا: «كلُّ كلمة» ليست نقطةً قاعديّة.** `s(كل كلمة) = 1` دالّةٌ مجالُها
الكلماتُ ومُستقَرُّها `B`؛ فلا مجالُها القاعدةُ ولا مُستقَرُّها الفضاءَ
الكلّيّ، ولا يوجد إسقاطٌ `E → W` تكون قطاعًا فوقه. فهي **وسمُ وقوعٍ** لا
قطاع، وحارسُ الإنشاء في `Section` يردُّ ما مجالُه غيرُ القاعدة
(`A_SECTION_HAS_THE_BASE_FOR_ITS_DOMAIN`).

**ثالثًا: التوزيعُ المقيسُ دفعٌ أماميٌّ لا عضوٌ ثالث.** `s_g` ليس موضوعًا
بإزاء الاثنين، بل هو `(π ∘ ℓ)_* μ` — صورةُ وسمِ الوقوع نفسِه مدفوعًا على
القاعدة. فالمعدودُ واحدٌ يُقرأ بثلاث جهات، لا ثلاثةٌ
(`A_PUSHFORWARD_IS_NOT_A_THIRD_OBJECT`).

**رابعًا: الثابتان القطعيّان مكذوبان بالجدولين المُرسَلين أنفسِهما.** «`b=1`
دومًا» في الابتداء يُكذِّبه عمودُ السكون في الجدول الأوّل، و«`b=0` دومًا
و`H=0`» في الوقف يُكذِّبه عمودُ السكون في الجدول الثاني — وهو العمودُ الذي
يُخرِج ١٢٫١٧٪ المكتوبةَ في صفّ `s_g` نفسِه. فالصفّان دعويان مضروبتان بالصفّ
الثالث في الجدول الواحد (`A_STIPULATED_CONSTANT_IS_NOT_A_MEASURED_ONE`).

**خامسًا: سلسلةُ الصعود تُعاد حوسبتُها لا تُنسَخ.** `116 × 734/29 = 2936` لا
`21286`؛ والمكتوبُ حاصلُ `734 × 29`. فالخطوةُ الأخيرةُ تُسقِط العاملَ ٤ — وهو
`|E₁|` كلُّه، أي الفضاءُ الذي تُنسَب السلسلةُ إلى اشتقاقه من {0,1} — وتضع
مكانَه ٢٩ (`THE_LAST_STEP_DROPS_THE_STATE_SPACE`).

**ولا سلطةَ لهذه الوحدة**: لا ولادةَ فيها، ولا حكمَ ولادة، ولا تجميدَ `E0`،
ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه.
"""

from __future__ import annotations

import itertools
from collections.abc import Mapping
from dataclasses import dataclass, fields
from enum import Enum
from math import log2
from typing import Final

__all__ = [
    "ASCENT_CHAIN_AS_DECLARED",
    "A_PUSHFORWARD_IS_NOT_A_THIRD_OBJECT",
    "A_SECTION_HAS_THE_BASE_FOR_ITS_DOMAIN",
    "A_STIPULATED_CONSTANT_IS_NOT_A_MEASURED_ONE",
    "POSITION_BUNDLE_NAMED_RESIDUALS",
    "THE_COUNT_THREE_IS_NOT_THE_SAME_THREE",
    "THE_DECLARED_FIBRE",
    "THE_FINAL_POSITION_GRID",
    "THE_FIRST_POSITION_GRID",
    "THE_LAST_STEP_DROPS_THE_STATE_SPACE",
    "THE_SUPPLIED_GRIDS_ARE_NOT_REDERIVABLE_HERE",
    "AscentStep",
    "AscentStepReading",
    "BaseState",
    "ConstantLawStanding",
    "ConstantLawReading",
    "OccurrenceLabelling",
    "PositionBundleError",
    "PositionBundleReading",
    "Section",
    "assess_constant_law",
    "entropy_bits",
    "fibre_of",
    "pushforward_to_base",
    "read_ascent_chain",
    "run_position_bundle",
    "sections",
    "total_space",
]


class PositionBundleError(RuntimeError):
    """تُرفَع حين يُطلَب من هذه الوحدة بناءٌ لا تحمله أجناسُها."""


class BaseState(Enum):
    """القاعدةُ الثنائيّة `B = {0, 1}`: أبسطُ تمييزٍ مُعلَنٍ قبل البناء."""

    QUIESCENT = 0
    MOVING = 1

    @property
    def label(self) -> str:
        """اسمُ النقطة القاعديّة منطوقًا."""

        return "ساكن" if self is BaseState.QUIESCENT else "متحرّك"


THE_DECLARED_FIBRE: Final[Mapping[BaseState, tuple[str, ...]]] = {
    BaseState.QUIESCENT: ("سكون",),
    BaseState.MOVING: ("فتحة", "كسرة", "ضمة"),
}
"""الليفُ فوق كلّ نقطةٍ قاعديّة، مُعلَنًا قبل أيّ عدّ.

و`{1, 3}` ههنا **مُدخَلان لا مُشتقّان**: عددُ الحركات القصيرة ثلاثٌ في
الاصطلاح المأخوذ، ولا يُستخرَج الثلاثُ من الثنائيّ `{0,1}` بحال
(`THE_FIBRE_SIZES_ARE_INPUTS_NOT_DERIVATIONS`).
"""


def fibre_of(base: BaseState) -> tuple[str, ...]:
    """ليفُ النقطة القاعديّة، `π⁻¹(b)`."""

    return THE_DECLARED_FIBRE[base]


def total_space() -> tuple[tuple[BaseState, str], ...]:
    """الفضاءُ الكلّيُّ `E₁ = ⨆_b π⁻¹(b)`، مرتَّبًا ترتيبًا ثابتًا."""

    return tuple(
        (base, point) for base in BaseState for point in THE_DECLARED_FIBRE[base]
    )


@dataclass(frozen=True)
class Section:
    """قطاعٌ واحد: اختيارُ نقطةِ ليفٍ **فوق كلّ** نقطةٍ قاعديّة.

    والحارسُ يفحص الشرطَين معًا: استغراقَ القاعدة، ووقوعَ كلّ قيمةٍ في ليف
    نقطتها — وهو `π∘s = id_B` بعينه. فما تُرك فيه `b` بلا قيمةٍ ليس قطاعًا
    ناقصًا بل ليس بقطاع.
    """

    choice: Mapping[BaseState, str]

    def __post_init__(self) -> None:
        missing = [base for base in BaseState if base not in self.choice]
        if missing:
            raise PositionBundleError(
                "القطاعُ يُسنِد نقطةً فوق كلّ نقطةٍ قاعديّة؛ وما غابت عنه "
                f"{[base.label for base in missing]} ليس قطاعًا ناقصًا بل ليس "
                "بقطاع. " + A_SECTION_HAS_THE_BASE_FOR_ITS_DOMAIN
            )
        for base, point in self.choice.items():
            if not isinstance(base, BaseState):
                raise PositionBundleError(
                    f"مجالُ القطاع القاعدةُ وحدَها؛ و{base!r} ليس نقطةً "
                    "قاعديّة. " + A_SECTION_HAS_THE_BASE_FOR_ITS_DOMAIN
                )
            if point not in THE_DECLARED_FIBRE[base]:
                raise PositionBundleError(
                    f"«{point}» خارجُ ليف {base.label}، فلا يُسنَد فوقه؛ "
                    "و`π∘s = id` هو هذا الشرطُ بعينه."
                )

    def projects_to_identity(self) -> bool:
        """`π∘s = id_B` مفحوصًا صراحةً لا مُفترَضًا من الإنشاء."""

        return all(
            self.choice[base] in THE_DECLARED_FIBRE[base] for base in BaseState
        ) and set(self.choice) == set(BaseState)

    @property
    def reference(self) -> str:
        """القطاعُ منطوقًا: قيمتُه عند الساكن ثمّ عند المتحرّك."""

        return " / ".join(f"{base.label}→{self.choice[base]}" for base in BaseState)


def sections() -> tuple[Section, ...]:
    """قطاعاتُ `π` كلُّها معدودةً بأعيانها؛ وعدّتُها حاصلُ ضرب أحجام الألياف."""

    bases = tuple(BaseState)
    return tuple(
        Section(choice=dict(zip(bases, points, strict=True)))
        for points in itertools.product(*(THE_DECLARED_FIBRE[b] for b in bases))
    )


def entropy_bits(counts: Mapping[str, int]) -> float:
    """عطالةُ شانون بالبِتّات على عدٍّ مُعطًى؛ والصفرُ لا يدخل اللوغاريتم."""

    total = sum(counts.values())
    if total <= 0:
        raise PositionBundleError("لا عطالةَ تُقاس على مجموعٍ غيرِ موجب.")
    if any(count < 0 for count in counts.values()):
        raise PositionBundleError("عدٌّ سالبٌ لا يُقرأ تكرارًا.")
    return -sum(
        (count / total) * log2(count / total) for count in counts.values() if count > 0
    )


@dataclass(frozen=True)
class OccurrenceLabelling:
    """وسمُ وقوعٍ مقيسٌ على موضعٍ واحد: أعمدتُه الأربعةُ ومقامُها المُعلَن.

    وهذا **ليس قطاعًا**: مجالُه الوقوعاتُ لا القاعدة، فلا يُقابَل بـ`Section`
    ولا يُجمَع معه في جدولٍ واحد (`A_LABELLING_IS_NOT_A_SECTION`).
    """

    position: str
    fatha: int
    kasra: int
    damma: int
    sukun: int
    declared_denominator: int
    source: str

    def __post_init__(self) -> None:
        for name in ("fatha", "kasra", "damma", "sukun"):
            if getattr(self, name) < 0:
                raise PositionBundleError("عدٌّ سالبٌ لا يُقرأ عمودًا.")
        if self.declared_denominator <= 0:
            raise PositionBundleError("مقامٌ غيرُ موجبٍ لا تُقسَم عليه نسبة.")

    @property
    def counts(self) -> Mapping[str, int]:
        """الأعمدةُ الأربعةُ بأسمائها، بترتيب الليف المُعلَن."""

        return {
            "فتحة": self.fatha,
            "كسرة": self.kasra,
            "ضمة": self.damma,
            "سكون": self.sukun,
        }

    @property
    def recomputed_total(self) -> int:
        """مجموعُ الأعمدة الأربعة محسوبًا، لا منقولًا عن المقام المُعلَن."""

        return self.fatha + self.kasra + self.damma + self.sukun

    @property
    def conserves_the_declared_denominator(self) -> bool:
        """أيُطابق المحسوبُ المُعلَن؟ والجوابُ حقلٌ يُقرأ لا تصحيحٌ يُجرى."""

        return self.recomputed_total == self.declared_denominator

    def base_counts(self) -> Mapping[BaseState, int]:
        """الدفعُ الأماميُّ على القاعدة: `(π ∘ ℓ)_* μ` عدًّا لا نسبة."""

        return {
            BaseState.QUIESCENT: self.sukun,
            BaseState.MOVING: self.fatha + self.kasra + self.damma,
        }

    def share_of(self, base: BaseState) -> float:
        """نصيبُ نقطةٍ قاعديّةٍ من المجموع المحسوب."""

        return self.base_counts()[base] / self.recomputed_total

    @property
    def base_entropy_bits(self) -> float:
        """عطالةُ القاعدة `H(B)`؛ وسقفُها بِتٌّ واحد."""

        return entropy_bits(
            {base.label: count for base, count in self.base_counts().items()}
        )

    @property
    def total_entropy_bits(self) -> float:
        """عطالةُ الفضاء الكلّيّ على الخلايا الأربع؛ وسقفُها بِتّان."""

        return entropy_bits(self.counts)


def pushforward_to_base(labelling: OccurrenceLabelling) -> Mapping[BaseState, float]:
    """الدفعُ الأماميُّ نسبةً؛ وهو **مُشتَقٌّ** من الوسم لا موضوعٌ بإزائه."""

    return {base: labelling.share_of(base) for base in BaseState}


class ConstantLawStanding(Enum):
    """منزلةُ دعوى «ثابتٌ قطعيّ» على وسمٍ مقيس."""

    REFUTED_BY_THE_SUPPLIED_COLUMN = "مكذوبةٌ بالعمود المُرسَل نفسِه"
    NOT_REFUTED_IN_THESE_COUNTS = "لم تُكذَّب في هذه الأعداد"


@dataclass(frozen=True)
class ConstantLawReading:
    """قراءةُ دعوى ثابتٍ قطعيّ: منزلتُها، وعدّةُ ما يُخالفها، ونصيبُه."""

    position: str
    claimed_base: BaseState
    standing: ConstantLawStanding
    counterexamples: int
    denominator: int
    base_entropy_bits: float

    @property
    def counterexample_share(self) -> float:
        """نصيبُ المخالف من المقام المحسوب."""

        return self.counterexamples / self.denominator


def assess_constant_law(
    labelling: OccurrenceLabelling, claimed_base: BaseState
) -> ConstantLawReading:
    """احكمْ على «`b` دومًا» بعدِّ ما يقع خارجَها، لا بقراءة نصِّ الدعوى."""

    counts = labelling.base_counts()
    counterexamples = sum(
        count for base, count in counts.items() if base is not claimed_base
    )
    standing = (
        ConstantLawStanding.REFUTED_BY_THE_SUPPLIED_COLUMN
        if counterexamples > 0
        else ConstantLawStanding.NOT_REFUTED_IN_THESE_COUNTS
    )
    return ConstantLawReading(
        position=labelling.position,
        claimed_base=claimed_base,
        standing=standing,
        counterexamples=counterexamples,
        denominator=labelling.recomputed_total,
        base_entropy_bits=labelling.base_entropy_bits,
    )


THE_FIRST_POSITION_GRID: Final[OccurrenceLabelling] = OccurrenceLabelling(
    position="الموضع الأوّل (قانون الابتداء)",
    fatha=47487,
    kasra=12485,
    damma=7904,
    sukun=10339,
    declared_denominator=78215,
    source="جدولٌ وارد في رسالةٍ خارجيّة؛ بايتاتُه ليست في هذه الشجرة",
)
"""أعمدةُ الجدول الأوّل كما وردت؛ ومجموعُها المحسوبُ يُطابق مقامَها المُعلَن."""

THE_FINAL_POSITION_GRID: Final[OccurrenceLabelling] = OccurrenceLabelling(
    position="الموضع الأخير (قانونا الوقف والوصل)",
    fatha=32023,
    kasra=19613,
    damma=16940,
    sukun=9500,
    declared_denominator=78076,
    source="جدولٌ وارد في رسالةٍ خارجيّة؛ بايتاتُه ليست في هذه الشجرة",
)
"""أعمدةُ الجدول الثاني كما وردت؛ ومجموعُها المحسوبُ يُطابق مقامَها المُعلَن."""


@dataclass(frozen=True)
class AscentStep:
    """خطوةٌ مُعلَنةٌ في سلسلة الصعود: مُدخَلُها، وعاملُها، ومُخرَجُها المكتوب."""

    name: str
    declared_input: int
    factor_numerator: int
    factor_denominator: int
    declared_output: int

    def __post_init__(self) -> None:
        if self.factor_denominator == 0:
            raise PositionBundleError("عاملٌ مقامُه صفرٌ لا يُحسَب.")


@dataclass(frozen=True)
class AscentStepReading:
    """قراءةُ خطوةٍ: المكتوبُ بإزاء المُعادِ حوسبتُه، والفرقُ بينهما."""

    step: AscentStep
    recomputed_output: float

    @property
    def agrees(self) -> bool:
        """أيُطابق المكتوبُ المحسوب؟ والجوابُ يُقرأ ولا يُصحَّح أحدُ طرفيه."""

        return self.recomputed_output == float(self.step.declared_output)

    @property
    def declared_over_recomputed(self) -> float:
        """نسبةُ المكتوب إلى المحسوب؛ وهي تُسمّي العاملَ المُبدَّل عند الخلاف."""

        if self.recomputed_output == 0.0:
            raise PositionBundleError("لا تُقاس نسبةٌ إلى محسوبٍ صفر.")
        return self.step.declared_output / self.recomputed_output


ASCENT_CHAIN_AS_DECLARED: Final[tuple[AscentStep, ...]] = (
    AscentStep(
        name="{0,1} ⟶ E₁",
        declared_input=2,
        factor_numerator=2,
        factor_denominator=1,
        declared_output=4,
    ),
    AscentStep(
        name="E₁ ⟶ E₂ = E₁ × L",
        declared_input=4,
        factor_numerator=29,
        factor_denominator=1,
        declared_output=116,
    ),
    AscentStep(
        name="E₂ ⟶ E₃ عبر قيد OCP",
        declared_input=116,
        factor_numerator=734,
        factor_denominator=29,
        declared_output=21286,
    ),
)
"""سلسلةُ الصعود بخطواتها المكتوبة؛ تُعاد حوسبتُها في `read_ascent_chain`.

والخطوةُ الأولى مكتوبةٌ بعاملٍ ٢ لأنّ `1+3 = 2×2`؛ وهي موافقةٌ حسابيّةٌ لا
اشتقاقٌ من `{0,1}`، فالعددان `{1,3}` مُدخَلان مُعلَنان.
"""


def read_ascent_chain() -> tuple[AscentStepReading, ...]:
    """أعدْ حوسبةَ كلّ خطوةٍ من مُدخَلها وعاملها، ولا تنسخْ مُخرَجًا مكتوبًا."""

    return tuple(
        AscentStepReading(
            step=step,
            recomputed_output=step.declared_input
            * step.factor_numerator
            / step.factor_denominator,
        )
        for step in ASCENT_CHAIN_AS_DECLARED
    )


@dataclass(frozen=True)
class PositionBundleReading:
    """قراءةُ المستوى الرابع كاملةً: القطاعات، والأوسمة، والدعاوى، والسلسلة."""

    sections: tuple[Section, ...]
    total_space_size: int
    first_position: OccurrenceLabelling
    final_position: OccurrenceLabelling
    inchoative_law: ConstantLawReading
    pausal_law: ConstantLawReading
    chain: tuple[AscentStepReading, ...]

    @property
    def section_count(self) -> int:
        """عدّةُ القطاعات الحقيقيّة `|Γ(π)|`."""

        return len(self.sections)

    @property
    def every_section_is_quiescent_at_zero(self) -> bool:
        """كلُّ قطاعٍ يأخذ «سكون» عند `b=0`، فلا قطاعَ «متحرّكٌ دومًا»."""

        return all(
            section.choice[BaseState.QUIESCENT] == "سكون" for section in self.sections
        )

    @property
    def chain_disagreements(self) -> tuple[AscentStepReading, ...]:
        """خطواتُ السلسلة التي خالف مكتوبُها محسوبَها، مُسمّاةً لا مطويّة."""

        return tuple(reading for reading in self.chain if not reading.agrees)


def run_position_bundle() -> PositionBundleReading:
    """شغِّلْ قراءةَ المستوى الرابع كلَّها على الأعمدة المُعلَنة."""

    return PositionBundleReading(
        sections=sections(),
        total_space_size=len(total_space()),
        first_position=THE_FIRST_POSITION_GRID,
        final_position=THE_FINAL_POSITION_GRID,
        inchoative_law=assess_constant_law(THE_FIRST_POSITION_GRID, BaseState.MOVING),
        pausal_law=assess_constant_law(THE_FINAL_POSITION_GRID, BaseState.QUIESCENT),
        chain=read_ascent_chain(),
    )


A_SECTION_HAS_THE_BASE_FOR_ITS_DOMAIN: Final[str] = (
    "A_SECTION_HAS_THE_BASE_FOR_ITS_DOMAIN: القطاعُ `s: B → E` بشرط "
    "`π∘s = id_B`، فمجالُه القاعدةُ ومُستقَرُّه الفضاءُ الكلّيّ. و"
    "«`s(كل كلمة) = 1`» مجالُها الكلماتُ ومُستقَرُّها `B`، ولا إسقاطَ "
    "`E → W` تكون قطاعًا فوقه؛ فهي وسمُ وقوعٍ لا قطاع، ولا يُصحَّح الجنسُ "
    "بتسميةٍ."
)

THE_COUNT_THREE_IS_NOT_THE_SAME_THREE: Final[str] = (
    "THE_COUNT_THREE_IS_NOT_THE_SAME_THREE: `|Γ(π)| = 1 × 3 = 3`، وعددُ "
    "القوانين المُرسَلة ثلاثةٌ كذلك. والموافقةُ حسابيّةٌ لا بنيويّة: القطاعاتُ "
    "الثلاثةُ تتمايز باختيار الحركة فوق `b=1` وتشترك كلُّها في «سكون» فوق "
    "`b=0`، والقوانينُ الثلاثةُ لا تتمايز باختيار حركةٍ البتّة."
)

A_PUSHFORWARD_IS_NOT_A_THIRD_OBJECT: Final[str] = (
    "A_PUSHFORWARD_IS_NOT_A_THIRD_OBJECT: توزيعُ `s_g` هو `(π ∘ ℓ)_* μ` — "
    "صورةُ وسم الوقوع نفسِه مدفوعًا على القاعدة — لا موضوعٌ ثالثٌ بإزاء "
    "الاثنين. فالمعدودُ واحدٌ قُرِئ بثلاث جهات، وعدُّه ثلاثةً تكثيرٌ للواحد."
)

A_STIPULATED_CONSTANT_IS_NOT_A_MEASURED_ONE: Final[str] = (
    "A_STIPULATED_CONSTANT_IS_NOT_A_MEASURED_ONE: «ثابتٌ قطعيّ» في الصفّين "
    "الأوّلين دعوًى، وعمودُ السكون في الجدولين يُكذِّبها في الموضعين. ودعوى "
    "«H=0» للوقف يُكذِّبها الصفُّ الثالثُ في الجدول نفسِه، إذ ١٢٫١٧٪ هي عينُها "
    "عمودُ السكون الذي قيل إنّه يستغرق الموضع."
)

THE_LAST_STEP_DROPS_THE_STATE_SPACE: Final[str] = (
    "THE_LAST_STEP_DROPS_THE_STATE_SPACE: `116 × 734/29 = 2936` لا `21286`؛ "
    "والمكتوبُ حاصلُ `734 × 29`. فالخطوةُ تُسقِط العاملَ ٤ — وهو `|E₁|` كلُّه، "
    "أي فضاءُ الحالات الذي تُنسَب السلسلةُ إلى اشتقاقه من `{0,1}` — وتضع "
    "مكانَه ٢٩. فآخرُ خطوةٍ في سلسلةٍ مبناها على الثنائيّ خاليةٌ من الثنائيّ."
)

THE_FIBRE_SIZES_ARE_INPUTS_NOT_DERIVATIONS: Final[str] = (
    "THE_FIBRE_SIZES_ARE_INPUTS_NOT_DERIVATIONS: `{1, 3}` مُعلَنان قبل البناء "
    "ولا يُستخرَجان من `{0,1}`. فقولُ «كلُّ رقمٍ مُشتقٌّ لا مفترَض» يصدق على "
    "حاصل الضرب لا على عوامله: الثلاثُ اصطلاحُ الحركات القصيرة، والتسعُ "
    "والعشرون عدّةُ حروفٍ مُعلَنة."
)

A_LABELLING_IS_NOT_A_SECTION: Final[str] = (
    "A_LABELLING_IS_NOT_A_SECTION: وسمُ الوقوع `ℓ: Occurrences → E` والقطاعُ "
    "`s: B → E` جنسان مختلفان مجالًا وشرطًا. وجمعُهما في جدولٍ واحدٍ تحت عنوان "
    "«ثلاثةُ أقسامٍ لحزمةٍ واحدة» يُسوّي بين ما لا يُسوَّى، ولا يُصلِحه ترقيمٌ."
)

LOCAL_TRIVIALITY_IS_VACUOUS_OVER_A_DISCRETE_BASE: Final[str] = (
    "LOCAL_TRIVIALITY_IS_VACUOUS_OVER_A_DISCRETE_BASE: فوق قاعدةٍ منفصلةٍ "
    "منتهيةٍ كلُّ مفردةٍ مفتوحة، فـ`E|{b} ≅ {b} × F_b` قائمٌ دائمًا. فالساقطُ "
    "ليس التفاهةَ الموضعيّة بل **ثباتُ الليف النموذجيّ**، وهو شرطٌ آخر لا "
    "يلزم فوق قاعدةٍ غير متّصلة؛ فالتسميةُ تُصحَّح ههنا ولا يُبنى عليها نقض."
)

THE_SUPPLIED_GRIDS_ARE_NOT_REDERIVABLE_HERE: Final[str] = (
    "THE_SUPPLIED_GRIDS_ARE_NOT_REDERIVABLE_HERE: أعمدةُ الجدولين مُسجَّلةٌ "
    "بحروفها ولا تُعاد حوسبتُها من بايتاتٍ في هذه الشجرة، فلا مدوَّنةَ "
    "مُودَعةً تُخرِجها. وكلُّ ما تفعله هذه الوحدة حسابٌ **على الأعمدة كما "
    "وردت**: تسجيلُ عددٍ ليس تصديقًا له، والنِّسَبُ المُشتقّةُ منه تَرِث "
    "منزلتَه لا تَرفعها."
)

THE_TWO_GRIDS_READ_TWO_POSITIONS_NOT_ONE_BASE: Final[str] = (
    "THE_TWO_GRIDS_READ_TWO_POSITIONS_NOT_ONE_BASE: الجدولُ الأوّلُ يقرأ "
    "الموضعَ الأوّلَ والثاني يقرأ الأخير، ومقاماهما مختلفان (78,215 و78,076). "
    "فلا تُقرأ الدعويان قطاعين فوق قاعدةٍ واحدة، ونصيبا السكون فيهما "
    "(13.2187% و12.1676%) عددان مختلفان لا قراءتان لعددٍ واحد."
)

A_FINAL_SUKUN_IS_NOT_SORTED_PAUSAL_FROM_CONNECTED: Final[str] = (
    "A_FINAL_SUKUN_IS_NOT_SORTED_PAUSAL_FROM_CONNECTED: عمودُ السكون في "
    "الموضع الأخير لا يُفرَز في هذه الشجرة وقفًا من وصل، وهذا امتناعٌ قائمٌ "
    "قبل وصول الجدول. فقراءةُ العمود نفسِه مرّةً قانونَ وقفٍ ومرّةً قانونَ "
    "وصلٍ قراءتان لنظامين على موضعٍ واحدٍ لا قطاعان."
)

POSITION_BUNDLE_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "A_SECTION_HAS_THE_BASE_FOR_ITS_DOMAIN": A_SECTION_HAS_THE_BASE_FOR_ITS_DOMAIN,
    "THE_COUNT_THREE_IS_NOT_THE_SAME_THREE": THE_COUNT_THREE_IS_NOT_THE_SAME_THREE,
    "A_PUSHFORWARD_IS_NOT_A_THIRD_OBJECT": A_PUSHFORWARD_IS_NOT_A_THIRD_OBJECT,
    "A_STIPULATED_CONSTANT_IS_NOT_A_MEASURED_ONE": (
        A_STIPULATED_CONSTANT_IS_NOT_A_MEASURED_ONE
    ),
    "THE_LAST_STEP_DROPS_THE_STATE_SPACE": THE_LAST_STEP_DROPS_THE_STATE_SPACE,
    "THE_FIBRE_SIZES_ARE_INPUTS_NOT_DERIVATIONS": (
        THE_FIBRE_SIZES_ARE_INPUTS_NOT_DERIVATIONS
    ),
    "A_LABELLING_IS_NOT_A_SECTION": A_LABELLING_IS_NOT_A_SECTION,
    "LOCAL_TRIVIALITY_IS_VACUOUS_OVER_A_DISCRETE_BASE": (
        LOCAL_TRIVIALITY_IS_VACUOUS_OVER_A_DISCRETE_BASE
    ),
    "THE_SUPPLIED_GRIDS_ARE_NOT_REDERIVABLE_HERE": (
        THE_SUPPLIED_GRIDS_ARE_NOT_REDERIVABLE_HERE
    ),
    "THE_TWO_GRIDS_READ_TWO_POSITIONS_NOT_ONE_BASE": (
        THE_TWO_GRIDS_READ_TWO_POSITIONS_NOT_ONE_BASE
    ),
    "A_FINAL_SUKUN_IS_NOT_SORTED_PAUSAL_FROM_CONNECTED": (
        A_FINAL_SUKUN_IS_NOT_SORTED_PAUSAL_FROM_CONNECTED
    ),
}
"""ما لا تُثبِته هذه القراءةُ مُسمًّى باسمه، لا مطويًّا في حكمٍ عامّ."""


_FORBIDDEN_FIELD_TOKENS: Final[tuple[str, ...]] = (
    "accuracy",
    "adopted",
    "birth",
    "certificate",
    "confirmed",
    "rank",
    "verdict",
)


def _assert_no_authority_field() -> None:
    """حارسُ استيراد: لا حقلَ سلطةٍ ولا رتبةٍ يتسلّل إلى هذه البنى لاحقًا."""

    for dataclass_type in (
        AscentStep,
        AscentStepReading,
        ConstantLawReading,
        OccurrenceLabelling,
        PositionBundleReading,
        Section,
    ):
        for declared in fields(dataclass_type):
            lowered = declared.name.lower()
            for token in _FORBIDDEN_FIELD_TOKENS:
                if token in lowered:
                    raise PositionBundleError(
                        f"حقلٌ يحمل سلطةً أو رتبةً تسلّل إلى "
                        f"{dataclass_type.__name__}: {declared.name}؛ وهذه "
                        "قراءةٌ لا سلطةَ فيها ولا رتبة."
                    )


_assert_no_authority_field()

if len(sections()) != 3:  # pragma: no cover - حارس
    raise RuntimeError("عدّةُ القطاعات حاصلُ ضرب أحجام الألياف، وهي ثلاثةٌ ههنا.")
if not all(section.projects_to_identity() for section in sections()):
    raise RuntimeError("قطاعٌ لا يُحقّق `π∘s = id` لا يخرج من هذه الوحدة.")
