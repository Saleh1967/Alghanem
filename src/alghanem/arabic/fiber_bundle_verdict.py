"""حزمةُ ألياف: الرتبةُ قائمةٌ عموديًّا، ساقطةٌ أفقيًّا، والمقياسُ الجمعيُّ هو الباقي.

**التصحيحُ الذي تُودِعه هذه الوحدة**: الكفايةُ والوحدانيّةُ التي بُرهنتا في
`fiber_rank_function` كانتا على **الشبكة المحيطة**، والسقوطُ كان على **المفردة
المرصودة**؛ فالحكمان لم يتناقضا بل تخاطبا محورين. والصياغةُ الأدقّ:

> حزمةُ أليافٍ قاعدتُها غيرُ مُدرَّجة، وأليافُها مُدرَّجةٌ كلُّها، ومعها
> مقياسٌ جمعيٌّ تامّ.

`π: E → B`، حيث `B` حواملُ الإيداع و`E_b` ليفُ الحامل. والمقيسُ ههنا **على
إيداع الفاتحة وحدَه** — ٢٣ حاملًا، و١٦ ليفًا متمايزًا، و٧ حالات:

* **عموديًّا**: الفترةُ `[∅, E_b]` مُدرَّجةٌ بـ`|·|` في **٢٣ من ٢٣**، صفرُ
  استثناء. والأعماقُ المرصودةُ `{1,2,3,4,6}`.
* **أفقيًّا**: ترتيبُ الألياف غيرُ مُدرَّجٍ (أزواجٌ بسلاسلَ متفاوتة) وغيرُ
  متّصلٍ (مركّبتان)، فلا دالّةَ رتبةٍ على `B`
  (`RANK_IS_VERTICAL_NOT_HORIZONTAL`).

**والمرخَّصُ فعلًا مقياسٌ لا رتبة.** `μ(X) = |X|` جمعيٌّ تامّ: القانونُ
الموجِّهُ `μ(X∪Y) + μ(X∩Y) = μ(X) + μ(Y)` يصدق على **٩٢١٦** زوجًا من أزواج
الإغلاق تحت `∪∩` بلا خرقٍ واحد. والمقياسُ يقيس الفرقَ ولا يُرتِّب بخطوات
(`AN_ADDITIVE_MEASURE_IS_NOT_A_RANK_FUNCTION`).

**والسؤالان ليسا سؤالًا واحدًا، ولا يسقطان معًا.** «كم يزيد ليفُ `ل` على ليف
`ا`؟» جوابُه `μ`-فرقٌ معرَّفٌ في **كلّ** الأزواج المتقارنة الستّة والأربعين.
أمّا «كم درجةً بينهما؟» فيُعرَّف في **٤٢** منها ويلتبس في **٤** — فليس بلا
جوابٍ مطلقًا كما قد يُقال: بين `ا` و`ل` سلسلةٌ واحدةٌ طولُها **٣**، وبين `س`
و`ل` طولان `{3, 4}`. فالساقطُ **دالّةُ خطوةٍ كلّيّة** لا كلُّ عدّ خطوات
(`THE_STEP_COUNT_FAILS_GLOBALLY_NOT_PAIRWISE`).

**والإغلاقُ النزوليُّ يسقط في ١٠ من ٢٣** — لا كلُّ جزءٍ غيرِ خالٍ من ليفٍ
مرصودٍ هو نفسُه ليفٌ مرصود. ولا يُقرأ ذلك منعًا: البديلُ أن يكون الغيابُ
**صفرَ معاينة** لا صفرَ إمكان، وهو بديلٌ **لم يُقَس** ولا أداةَ له في هذه
الشجرة (`A_DOWNWARD_GAP_MAY_BE_A_SAMPLING_ZERO`).

**وأرقامُ المدوّنة الأوسع تُسجَّل دعوى لا قياسًا.** `|B|=36` و`|A|=8`
و`8464` و`89` و`16` و`76.9%` مُسنَدةٌ إلى `FROZEN_CORPUS`؛ وبايتاتُها ليست في
الشجرة، فلا تُشتَقّ ههنا ولا تُنسَخ بوصفها مقيسة
(`A_WIDER_CORPUS_NUMBER_IS_A_CLAIM_HERE`). ومع ذلك **البصمةُ مُودَعة**: اسمُ
المصدر وطولُه وSHA-256 وسياسةُ «لا تطبيع البتّة» مُجمَّدةٌ في
`compression_model_preregistration`. فالمدوّنةُ غيرُ مُطبَّعةٍ بتصريحٍ مكتوب،
لا غيرَ مُودَعةٍ بلا بصمة — والغائبُ البايتاتُ عمدًا لا الإيداع
(`THE_CORPUS_IS_FINGERPRINTED_THOUGH_ITS_BYTES_ARE_ABSENT`).

ولا سلطةَ لهذه الوحدة: لا ولادةَ، ولا ترخيصَ `RefineSlot`، ولا ترخيصَ
`FiberRank` على القاعدة، ولا استيرادَ من `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from itertools import combinations
from typing import Final

from .carrier_state_observed_fiber import ObservedFiberTable
from .compression_model_preregistration import FROZEN_CORPUS
from .decomposition_reconstruction_theorem import MeasurementInstrument, Population
from .fiber_ambient_choice import ClosureOperator, build_ambient
from .fiber_rank_function import Fiber, observed_fibers

__all__ = [
    "AN_ADDITIVE_MEASURE_IS_NOT_A_RANK_FUNCTION_NOTE",
    "A_DOWNWARD_GAP_MAY_BE_A_SAMPLING_ZERO_NOTE",
    "A_WIDER_CORPUS_NUMBER_IS_A_CLAIM_HERE_NOTE",
    "FIBER_BUNDLE_NAMED_RESIDUALS",
    "RANK_IS_VERTICAL_NOT_HORIZONTAL_NOTE",
    "THE_CORPUS_IS_FINGERPRINTED_THOUGH_ITS_BYTES_ARE_ABSENT_NOTE",
    "THE_STEP_COUNT_FAILS_GLOBALLY_NOT_PAIRWISE_NOTE",
    "Axis",
    "BundleVerdict",
    "FiberBundleError",
    "PairStepVerdict",
    "StepCensus",
    "WiderCorpusClaim",
    "WIDER_CORPUS_CLAIMS",
    "additive_measure_holds",
    "downward_closure_failures",
    "measure_the_bundle",
    "survey_step_counts",
    "vertical_grading_census",
]


class FiberBundleError(ValueError):
    """رفضٌ صريح: حكمٌ بلا محورٍ مُسمًّى، أو دعوى مدوّنةٍ تُلبَس ثوبَ القياس."""


class Axis(Enum):
    """المحورُ الذي يُسأل عنه؛ وخلطُه هو الذي أنتج الحكمين المتعارضين."""

    VERTICAL_WITHIN_A_FIBER = "عموديًّا_داخلَ_الليف"
    HORIZONTAL_ACROSS_THE_BASE = "أفقيًّا_عبرَ_القاعدة"


# --- عموديًّا: التدريجُ داخلَ كلّ ليف ------------------------------------------


@dataclass(frozen=True, slots=True)
class BundleVerdict:
    """حكمُ الحزمة بمحوريها؛ ولا يُقرأ أحدُهما نقضًا للآخر."""

    carrier_count: int
    distinct_fiber_count: int
    state_count: int
    fibers_graded: int
    base_is_graded: bool
    base_component_count: int
    observed_depths: tuple[int, ...]

    def __post_init__(self) -> None:
        if self.fibers_graded > self.carrier_count:
            raise FiberBundleError("مُدرَّجٌ أكثرُ من الحوامل كلِّها؛ عدٌّ فاسد")
        if self.distinct_fiber_count > self.carrier_count:
            raise FiberBundleError("أليافٌ متمايزةٌ أكثرُ من حواملها")
        if not self.observed_depths:
            raise FiberBundleError("حزمةٌ بلا عمقٍ مرصودٍ لا تُحكَم")

    @property
    def vertical_grading_is_exceptionless(self) -> bool:
        """أمُدرَّجةٌ الأليافُ كلُّها بلا استثناء؟ يُعَدّ ولا يُصرَّح."""

        return self.fibers_graded == self.carrier_count

    def rank_exists_on(self, axis: Axis) -> bool:
        """أتوجد دالّةُ رتبةٍ على هذا المحور؟ والسؤالُ لا يُطرَح بلا محور."""

        if axis is Axis.VERTICAL_WITHIN_A_FIBER:
            return self.vertical_grading_is_exceptionless
        if axis is Axis.HORIZONTAL_ACROSS_THE_BASE:
            return self.base_is_graded
        raise FiberBundleError("محورٌ غيرُ مُسمًّى؛ ولا حكمَ بلا تسميته")


def _interval_is_graded(fiber: Fiber) -> bool:
    members = [
        frozenset(chosen)
        for size in range(len(fiber) + 1)
        for chosen in combinations(sorted(fiber), size)
    ]
    return all(
        len(upper) - len(lower) == 1
        for lower in members
        for upper in members
        if lower < upper and not any(lower < middle < upper for middle in members)
    )


def vertical_grading_census(table: ObservedFiberTable | None = None) -> tuple[int, int]:
    """كم ليفًا مُدرَّجٌ من كم؟ مُشتقٌّ بفحص كلّ فترةٍ `[∅, E_b]` على حِدَة."""

    fibers = observed_fibers(table)
    graded = sum(1 for fiber in fibers.values() if _interval_is_graded(fiber))
    return graded, len(fibers)


def measure_the_bundle(table: ObservedFiberTable | None = None) -> BundleVerdict:
    """قِس الحزمةَ بمحوريها معًا؛ فالحكمُ الواحدُ على محورٍ واحدٍ مُضلِّل."""

    fibers = observed_fibers(table)
    distinct = sorted(set(fibers.values()), key=lambda item: (len(item), sorted(item)))
    graded, total = vertical_grading_census(table)
    base_graded = all(
        len(upper) - len(lower) == 1
        for lower in distinct
        for upper in distinct
        if lower < upper and not any(lower < middle < upper for middle in distinct)
    )
    parent = {node: node for node in distinct}

    def find(node: Fiber) -> Fiber:
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    for first, second in combinations(distinct, 2):
        if first < second or second < first:
            root_first, root_second = find(first), find(second)
            if root_first != root_second:
                parent[root_first] = root_second
    return BundleVerdict(
        carrier_count=total,
        distinct_fiber_count=len(distinct),
        state_count=len(set().union(*fibers.values())),
        fibers_graded=graded,
        base_is_graded=base_graded,
        base_component_count=len({find(node) for node in distinct}),
        observed_depths=tuple(sorted({len(fiber) for fiber in fibers.values()})),
    )


# --- المقياسُ الجمعيّ ---------------------------------------------------------


def additive_measure_holds(
    operator: ClosureOperator = ClosureOperator.UNION_INTERSECTION,
    table: ObservedFiberTable | None = None,
) -> tuple[int, int]:
    """`μ(X)=|X|`: كم زوجًا فُحِص، وكم خرقًا وُجِد؟ والخرقُ يُعَدّ لا يُنفى."""

    members = build_ambient(operator, table)
    lattice = set(members)
    breaches = 0
    for first in members:
        for second in members:
            union, meet = first | second, first & second
            if union not in lattice or meet not in lattice:
                breaches += 1
            elif len(union) + len(meet) != len(first) + len(second):
                breaches += 1
    return len(members) ** 2, breaches


# --- الخطوةُ والفرق: سؤالان لا سؤال ------------------------------------------


@dataclass(frozen=True, slots=True)
class PairStepVerdict:
    """زوجٌ متقارنٌ واحد: فرقُ مقياسه معرَّفٌ دائمًا، وعدُّ خطواته قد يلتبس."""

    lower_carrier: str
    upper_carrier: str
    measure_difference: int
    step_counts: tuple[int, ...]

    def __post_init__(self) -> None:
        if self.measure_difference <= 0:
            raise FiberBundleError("زوجٌ متقارنٌ بفرقِ مقياسٍ غيرِ موجب")
        if not self.step_counts:
            raise FiberBundleError("زوجٌ متقارنٌ بلا سلسلةٍ واحدةٍ بينهما")

    @property
    def step_count_is_well_defined(self) -> bool:
        """أللزوج عددُ خطواتٍ واحد؟ يُقرأ من تعدّد السلاسل لا من دعوى."""

        return len(self.step_counts) == 1


@dataclass(frozen=True, slots=True)
class StepCensus:
    """إحصاءُ الأزواج المتقارنة، مفصولًا فيه المعرَّفُ عن الملتبس."""

    population: Population
    instrument: MeasurementInstrument
    verdicts: tuple[PairStepVerdict, ...]

    def __post_init__(self) -> None:
        if self.population is not Population.OBSERVED:
            raise FiberBundleError("هذا إحصاءُ المرصود؛ ولا يُوسَم بالمُعلَن")
        if self.instrument is not MeasurementInstrument.OBSERVED_FIBER:
            raise FiberBundleError("هذه أرقامُ الليف؛ ولا تُنسَب لآلةٍ أخرى")

    @property
    def comparable_pairs(self) -> int:
        """عددُ الأزواج المتقارنة كلِّها."""

        return len(self.verdicts)

    @property
    def well_defined_steps(self) -> int:
        """ما استقام فيه عدُّ الخطوات؛ وهو أكثرُ من الملتبس لا أقلّ."""

        return sum(1 for item in self.verdicts if item.step_count_is_well_defined)

    @property
    def ambiguous_steps(self) -> int:
        """ما التبس فيه العدّ؛ ووجودُ واحدٍ منه يُسقِط الدالّةَ الكلّيّة."""

        return self.comparable_pairs - self.well_defined_steps

    @property
    def the_measure_difference_is_always_defined(self) -> bool:
        """أفرقُ المقياس معرَّفٌ في كلّ زوج؟ يُفحَص بالعدّ لا يُفترَض."""

        return all(item.measure_difference > 0 for item in self.verdicts)


def survey_step_counts(table: ObservedFiberTable | None = None) -> StepCensus:
    """افحص كلَّ زوجٍ متقارنٍ: أله عددُ خطواتٍ واحد، أم أطوالٌ متفاوتة؟"""

    fibers = observed_fibers(table)
    distinct = sorted(set(fibers.values()), key=lambda item: (len(item), sorted(item)))
    naming = {fiber: carrier for carrier, fiber in sorted(fibers.items(), reverse=True)}

    def lengths(lower: Fiber, upper: Fiber) -> frozenset[int]:
        if lower == upper:
            return frozenset({0})
        found: set[int] = set()
        for middle in distinct:
            if lower < middle <= upper and not any(
                lower < other < middle for other in distinct
            ):
                found |= {1 + step for step in lengths(middle, upper)}
        return frozenset(found)

    verdicts: list[PairStepVerdict] = []
    for lower in distinct:
        for upper in distinct:
            if not lower < upper:
                continue
            verdicts.append(
                PairStepVerdict(
                    lower_carrier=naming[lower],
                    upper_carrier=naming[upper],
                    measure_difference=len(upper) - len(lower),
                    step_counts=tuple(sorted(lengths(lower, upper))),
                )
            )
    return StepCensus(
        population=Population.OBSERVED,
        instrument=MeasurementInstrument.OBSERVED_FIBER,
        verdicts=tuple(verdicts),
    )


def downward_closure_failures(
    table: ObservedFiberTable | None = None,
) -> tuple[str, ...]:
    """الحواملُ التي لجزءٍ غيرِ خالٍ من ليفها لا ليفٌ مرصودٌ يساويه."""

    fibers = observed_fibers(table)
    observed = set(fibers.values())
    return tuple(
        sorted(
            carrier
            for carrier, fiber in fibers.items()
            if not all(
                frozenset(chosen) in observed
                for size in range(1, len(fiber))
                for chosen in combinations(sorted(fiber), size)
            )
        )
    )


# --- دعاوى المدوّنة الأوسع: تُسجَّل ولا تُنسَخ قياسًا ---------------------------


@dataclass(frozen=True, slots=True)
class WiderCorpusClaim:
    """رقمٌ من خارج هذا الإيداع، مقرونًا بمصدره وبسبب تعذّر اشتقاقه ههنا."""

    label: str
    value: str
    why_not_derivable_here: str

    def __post_init__(self) -> None:
        if not self.label.strip() or not self.value.strip():
            raise FiberBundleError("دعوى بلا وسمٍ أو بلا قيمةٍ لا تُسجَّل")
        if not self.why_not_derivable_here.strip():
            raise FiberBundleError(
                "دعوى بلا سببٍ مكتوبٍ لتعذّر اشتقاقها تُقرَأ قياسًا بعد حين"
            )

    @property
    def is_a_measurement_here(self) -> bool:
        """أهي مقيسةٌ في هذه الشجرة؟ لا — والجوابُ ثابتٌ بالبناء لا بالحال."""

        return False


_ABSENT: Final[str] = (
    "بايتاتُ المدوّنة ليست في الشجرة عمدًا؛ فالرقمُ لا يُعاد اشتقاقُه ههنا، "
    f"وإنّما تُودَع بصمتُه: {FROZEN_CORPUS.source_name} بطول "
    f"{FROZEN_CORPUS.byte_length} بايتًا"
)

WIDER_CORPUS_CLAIMS: Final[tuple[WiderCorpusClaim, ...]] = (
    WiderCorpusClaim("حجمُ القاعدة", "36", _ABSENT),
    WiderCorpusClaim("حجمُ أبجديّة الحالات", "8", _ABSENT),
    WiderCorpusClaim("أزواجُ القانون الموجِّه", "8464", _ABSENT),
    WiderCorpusClaim("أزواجٌ بسلاسلَ متفاوتة", "89، و16 بعد الإغلاق تحت ∪∩", _ABSENT),
    WiderCorpusClaim("الإغلاقُ النزوليُّ الساقط", "13 من 36", _ABSENT),
    WiderCorpusClaim("ما تُفسِّره الحواملُ الثلاثةُ المتجاورة", "76.9٪", _ABSENT),
    WiderCorpusClaim("ما تُفسِّره البوّاباتُ على النوع", "15.7٪", _ABSENT),
    WiderCorpusClaim("الشدّةُ المنفردة", "246 موضعًا", _ABSENT),
)
"""ثماني دعاوى مُسنَدةٍ إلى مدوّنةٍ مُبصَّمةٍ غائبةِ البايتات؛ لا مقيسٌ فيها."""


# --- البواقي المُسمّاة --------------------------------------------------------


AN_ADDITIVE_MEASURE_IS_NOT_A_RANK_FUNCTION_NOTE: Final[str] = (
    "AnAdditiveMeasureIsNotARankFunction: `μ(X)=|X|` جمعيٌّ تامٌّ بلا خرقٍ "
    "واحدٍ على المُغلَق، ويقيس الفرقَ بين ليفين؛ ولا يجعله ذلك رتبةً، إذ "
    "الرتبةُ تعِد الخطواتِ والمقياسُ يزِن الفرق، وهما سؤالان لا سؤال"
)

A_DOWNWARD_GAP_MAY_BE_A_SAMPLING_ZERO_NOTE: Final[str] = (
    "ADownwardGapMayBeASamplingZero: سقوطُ الإغلاق النزوليِّ في عشرةٍ من "
    "ثلاثةٍ وعشرين لا يُقرَأ امتناعًا؛ فالبديلُ أن يكون الغيابُ صفرَ معاينةٍ "
    "لا صفرَ إمكان، وهو بديلٌ لم يُقَس ولا أداةَ له في هذه الشجرة بعدُ"
)

A_WIDER_CORPUS_NUMBER_IS_A_CLAIM_HERE_NOTE: Final[str] = (
    "AWiderCorpusNumberIsAClaimHere: أرقامُ المدوّنة الأوسع مُسنَدةٌ إلى بصمةٍ "
    "بايتاتُها غائبةٌ عن الشجرة عمدًا؛ فتُسجَّل دعاوى مقرونةً بسبب تعذّر "
    "اشتقاقها، ولا تُنسَخ في موضع المقيس ولو كانت صادقة"
)

RANK_IS_VERTICAL_NOT_HORIZONTAL_NOTE: Final[str] = (
    "RankIsVerticalNotHorizontal: الحكمان المتعارضان — «موجودة» ثمّ «معدومة» — "
    "كانا خلطَ محورٍ لا خطأَ حساب؛ فالتدريجُ قائمٌ داخلَ كلّ ليفٍ بلا استثناء، "
    "ساقطٌ على القاعدة، والدالّةُ تُطلَب على محورٍ مُسمًّى أو لا تُطلَب"
)

THE_CORPUS_IS_FINGERPRINTED_THOUGH_ITS_BYTES_ARE_ABSENT_NOTE: Final[str] = (
    "TheCorpusIsFingerprintedThoughItsBytesAreAbsent: قولُ «بلا إيداعٍ مُبصَّم "
    "في الشجرة» لا يصدق: الاسمُ والطولُ وبصمةُ SHA-256 وسياسةُ «لا تطبيع "
    "البتّة» مُجمَّدةٌ في `compression_model_preregistration`؛ والغائبُ "
    "البايتاتُ عمدًا، وغيابُ التطبيع مُصرَّحٌ به لا مُغفَل"
)

THE_STEP_COUNT_FAILS_GLOBALLY_NOT_PAIRWISE_NOTE: Final[str] = (
    "TheStepCountFailsGloballyNotPairwise: «كم درجةً بين ا وَل» له جوابٌ ههنا "
    "وهو ثلاث، ولـ«س وَل» جوابان `{3,4}`؛ فالساقطُ دالّةُ خطوةٍ كلّيّةٌ على "
    "القاعدة لا كلُّ عدِّ خطوات، والتعميمُ إلى «بلا جواب» يزيد على المقيس"
)

FIBER_BUNDLE_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    RANK_IS_VERTICAL_NOT_HORIZONTAL_NOTE,
    AN_ADDITIVE_MEASURE_IS_NOT_A_RANK_FUNCTION_NOTE,
    THE_STEP_COUNT_FAILS_GLOBALLY_NOT_PAIRWISE_NOTE,
    A_DOWNWARD_GAP_MAY_BE_A_SAMPLING_ZERO_NOTE,
    A_WIDER_CORPUS_NUMBER_IS_A_CLAIM_HERE_NOTE,
    THE_CORPUS_IS_FINGERPRINTED_THOUGH_ITS_BYTES_ARE_ABSENT_NOTE,
)
"""ستُّ بقايا مُسمّاةٍ تُقابَل بها أيُّ إحالةٍ إلى «الرتبة» أو «المقياس» بعدُ."""
