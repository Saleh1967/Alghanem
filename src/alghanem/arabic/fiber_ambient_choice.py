"""المحيطُ اختيارٌ لا قياس، والثغرةُ تُقاضَى فردًا فردًا لا تُعَدّ جملةً.

**النقدُ الذي تُغلِقه هذه الوحدة**: البرهانُ في `fiber_rank_function` قام على
شبكةٍ محيطةٍ واحدة، وكان اختيارُ إغلاقها **عمليّةً اخترناها** لا شيئًا قاسه
الليف. وإغلاقٌ آخر يعطي شبكةً أخرى؛ ومعها يتغيّر عددُ الثغرات. ثمّ إنّ
الثغراتِ لم تُقاضَ: أيُّها يمكن أن يُسَدّ بعنصرٍ يُرصَد في مدوّنةٍ أوسع، وأيُّها
ممتنعٌ بنيويًّا، وأيُّها لا يُحسَم بهذا الإيداع.

**والمقيسُ أنّ الاختيارَ يغيّر الشيءَ ولا يغيّر الحكم.** خمسةُ إغلاقاتٍ على
الألياف الستّةَ عشرَ المرصودة تُخرِج أشياءَ مختلفةَ الحجم — والإغلاقُ تحت
`∪`و`∩` ليس الإغلاقَ تحت الفرق، ولا هو الشبكةَ الكاملة. ومع ذلك تبقى
**التدرّجيّةُ والاتّصالُ** قائمَين في كلّ إغلاقٍ يتجاوز المرصود، وتسقطان في
المرصودِ وحدَه. فالذي يتغيّر بالاختيار موطنُ البرهان وعددُ ثغراته، لا نتيجتُه
(`THE_AMBIENT_IS_A_CHOICE_NOT_A_MEASUREMENT`).

**ولا يُقال «عددُ الثغرات» مطلقًا.** هو ٥٩ تحت الإغلاق النازل، و٨٠ تحت `∪∩`،
و١١٢ تحت الفرق وتحت الشبكة الكاملة. فالرقمُ عن عمليّةٍ لا عن مدوّنة، وتُسمّى
العمليّةُ مع كلّ رقم (`THE_GAP_COUNT_IS_OPERATOR_RELATIVE`).

**والثغرةُ تُقاضى بثلاثة أحكامٍ لا بحكمين:**

* `BARRED_BY_A_MEASURED_RULE`: ممتنعةٌ بقاعدةٍ قائمةٍ في الشجرة تُفحَص حيّةً.
  وواحدةٌ فقط كذلك: المجموعةُ الخالية، إذ يردُّ `ObservedFiber` تركيبًا فارغًا
  عند الإنشاء. وما عداها **لا قاعدةَ تمنعه اليوم**
  (`ONLY_ONE_GAP_IS_BARRED_BY_A_MEASURED_RULE`).
* `JOINTLY_ATTESTED_ON_ONE_CARRIER`: كلُّ حالاتها اجتمعت فعلًا على حاملٍ واحدٍ
  مُسمًّى في هذا الإيداع. فاجتماعُها **مقيسٌ لا مُقدَّر**، ولا يمتنع بنيويًّا.
* `NOT_JOINTLY_ATTESTED_UNDECIDED`: لم تجتمع حالاتُها على حاملٍ واحدٍ قطّ. ولا
  يُقرأ هذا منعًا: غيابُ حالةٍ عن ليفٍ مرصودٍ قد يكون منعًا أو ندرةً أو تعذّرًا
  بالموضع، ولا يفصل بينها رصدٌ وحدَه — وهو نصُّ
  `OBSERVED_FIBER_IS_NOT_LICENSED_FIBER` المُودَع قبلًا
  (`AN_UNDECIDED_GAP_IS_NOT_A_BARRED_ONE`).

**وحدّان يُغلقان بابَ التوسّع في الحكم الثاني:**

**الشهادةُ الفرديّةُ مجّانيّة** (`INDIVIDUAL_ATTESTATION_IS_NOT_JOINT_ATTESTATION`):
الحالاتُ السبعُ كلُّها مشهودةٌ كلٌّ على حِدَة، فشرطُ «كلُّ حالةٍ منها رُصدت» لا
يُخرِج ثغرةً واحدة. فالشهادةُ المعتبرةُ شهادةُ **الاجتماع على حاملٍ واحد**.

**والشهادةُ ليست بناءَ مدوّنة** (`ATTESTATION_IS_NOT_A_CORPUS_CONSTRUCTION`): أن
تجتمع حالاتُ الثغرة على حاملٍ شيءٌ، وأن توجد مدوّنةٌ يكون ليفُ حاملٍ فيها
**هذه الثغرةَ بعينها لا أوسع** شيءٌ آخر لم يُبنَ ولم يُدَّعَ.

ولا سلطةَ لهذه الوحدة: لا ولادةَ، ولا حكمَ ولادة، ولا تجميدَ `E0`، ولا استيرادَ
من `kernel/`.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from itertools import combinations
from typing import Final

from .carrier_state_observed_fiber import (
    ObservedFiber,
    ObservedFiberTable,
    ObservedStateFiberError,
)
from .decomposition_reconstruction_theorem import MeasurementInstrument, Population
from .fiber_rank_function import Fiber, FiberRankError, StateVector, observed_fibers

__all__ = [
    "AN_UNDECIDED_GAP_IS_NOT_A_BARRED_ONE_NOTE",
    "ATTESTATION_IS_NOT_A_CORPUS_CONSTRUCTION_NOTE",
    "FIBER_AMBIENT_CHOICE_NAMED_RESIDUALS",
    "INDIVIDUAL_ATTESTATION_IS_NOT_JOINT_ATTESTATION_NOTE",
    "ONLY_ONE_GAP_IS_BARRED_BY_A_MEASURED_RULE_NOTE",
    "THE_AMBIENT_IS_A_CHOICE_NOT_A_MEASUREMENT_NOTE",
    "THE_GAP_COUNT_IS_OPERATOR_RELATIVE_NOTE",
    "AmbientChoiceError",
    "AmbientLatticeMeasurement",
    "ClosureOperator",
    "GapAdjudication",
    "GapCensus",
    "GapStatus",
    "adjudicate_gaps",
    "build_ambient",
    "compare_closure_operators",
    "gap_counts_by_operator",
    "the_empty_fiber_is_refused_live",
]


class AmbientChoiceError(ValueError):
    """رفضٌ صريح: محيطٌ بلا عمليّةٍ مُسمّاة، أو ثغرةٌ تُحكَم بلا شاهدها."""


class ClosureOperator(Enum):
    """العمليّاتُ التي قد يُبنى بها المحيط؛ وهي اختياراتٌ لا قياسات."""

    OBSERVED_ONLY = "المرصودُ_وحدَه_بلا_إغلاق"
    DOWNWARD = "الإغلاقُ_النازل_بالمجموعات_الجزئيّة"
    UNION_INTERSECTION = "الإغلاقُ_تحت_الاتّحاد_والتقاطع"
    UNION_INTERSECTION_DIFFERENCE = "الإغلاقُ_تحت_الاتّحاد_والتقاطع_والفرق"
    POWER_SET = "الشبكةُ_الكاملة_على_الحالات_المرصودة"


def _observed_distinct(table: ObservedFiberTable | None) -> tuple[Fiber, ...]:
    fibers = observed_fibers(table)
    return tuple(
        sorted(set(fibers.values()), key=lambda item: (len(item), sorted(item)))
    )


def _universe(distinct: tuple[Fiber, ...]) -> tuple[StateVector, ...]:
    universe: set[StateVector] = set()
    for fiber in distinct:
        universe |= fiber
    return tuple(sorted(universe))


def _closed_under(seed: tuple[Fiber, ...], operator: ClosureOperator) -> set[Fiber]:
    members: set[Fiber] = set(seed)
    changed = True
    while changed:
        changed = False
        for first, second in tuple(combinations(members, 2)):
            produced = [first | second, first & second]
            if operator is ClosureOperator.UNION_INTERSECTION_DIFFERENCE:
                produced.extend((first - second, second - first))
            for candidate in produced:
                if candidate not in members:
                    members.add(candidate)
                    changed = True
    return members


def build_ambient(
    operator: ClosureOperator, table: ObservedFiberTable | None = None
) -> tuple[Fiber, ...]:
    """ابنِ المحيطَ بالعمليّة المُسمّاة؛ ولا محيطَ يُبنى بعمليّةٍ لم تُسَمَّ."""

    if not isinstance(operator, ClosureOperator):
        raise AmbientChoiceError("المحيطُ يُبنى بعمليّةٍ عضوٍ في مفردتها المغلقة")
    distinct = _observed_distinct(table)
    if operator is ClosureOperator.OBSERVED_ONLY:
        members = set(distinct)
    elif operator is ClosureOperator.DOWNWARD:
        members = {
            frozenset(chosen)
            for fiber in distinct
            for size in range(len(fiber) + 1)
            for chosen in combinations(sorted(fiber), size)
        }
    elif operator is ClosureOperator.POWER_SET:
        universe = _universe(distinct)
        members = {
            frozenset(chosen)
            for size in range(len(universe) + 1)
            for chosen in combinations(universe, size)
        }
    else:
        members = _closed_under(distinct, operator)
    return tuple(sorted(members, key=lambda item: (len(item), sorted(item))))


# --- قياسُ المحيط المختار ----------------------------------------------------


@dataclass(frozen=True, slots=True)
class AmbientLatticeMeasurement:
    """قياسُ محيطٍ واحدٍ بعمليّته: حجمُه، وتغطياتُه، وتدرّجُه، واتّصالُه، وثغراتُه."""

    operator: ClosureOperator
    size: int
    cover_count: int
    is_graded: bool
    component_count: int
    gap_count: int
    observed_member_count: int

    def __post_init__(self) -> None:
        if self.size <= 0:
            raise AmbientChoiceError("محيطٌ خالٍ لا يُقاس عليه شيء")
        if self.gap_count + self.observed_member_count != self.size:
            raise AmbientChoiceError(
                "مجموعُ الثغرات والمرصود لا يساوي الحجم؛ ولا يُطوى الفارق"
            )

    @property
    def a_rank_function_exists(self) -> bool:
        """أتوجد دالّةُ رتبةٍ ههنا؟ التدرّجُ شرطُ وجودها، ويُقاس بالتغطيات."""

        return self.is_graded

    @property
    def free_constants(self) -> int:
        """ثابتٌ حرٌّ لكلّ مركّبةٍ متّصلة؛ ولا وحدانيّةَ «إلى ثابتٍ» بغير واحدة."""

        return self.component_count


def _covers(members: tuple[Fiber, ...]) -> tuple[int, bool]:
    count = 0
    graded = True
    for lower in members:
        for upper in members:
            if not lower < upper:
                continue
            if any(lower < middle < upper for middle in members):
                continue
            count += 1
            if len(upper) - len(lower) != 1:
                graded = False
    return count, graded


def _components(members: tuple[Fiber, ...]) -> int:
    parent: dict[Fiber, Fiber] = {node: node for node in members}

    def find(node: Fiber) -> Fiber:
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    for first, second in combinations(members, 2):
        if first < second or second < first:
            root_first, root_second = find(first), find(second)
            if root_first != root_second:
                parent[root_first] = root_second
    return len({find(node) for node in members})


def compare_closure_operators(
    table: ObservedFiberTable | None = None,
) -> tuple[AmbientLatticeMeasurement, ...]:
    """قِس الإغلاقاتِ الخمسةَ جنبًا إلى جنب؛ فالاختيارُ يُرى ولا يُدَّعى."""

    distinct = set(_observed_distinct(table))
    measurements: list[AmbientLatticeMeasurement] = []
    for operator in ClosureOperator:
        members = build_ambient(operator, table)
        cover_count, graded = _covers(members)
        observed_members = sum(1 for member in members if member in distinct)
        measurements.append(
            AmbientLatticeMeasurement(
                operator=operator,
                size=len(members),
                cover_count=cover_count,
                is_graded=graded,
                component_count=_components(members),
                gap_count=len(members) - observed_members,
                observed_member_count=observed_members,
            )
        )
    return tuple(measurements)


def gap_counts_by_operator(
    table: ObservedFiberTable | None = None,
) -> Mapping[ClosureOperator, int]:
    """عددُ الثغرات بكلّ عمليّة؛ ولا يُقتطَع منه رقمٌ واحدٌ يُقال مطلقًا."""

    return {
        measurement.operator: measurement.gap_count
        for measurement in compare_closure_operators(table)
    }


# --- مقاضاةُ الثغرات فردًا فردًا ----------------------------------------------


class GapStatus(Enum):
    """حكمُ ثغرةٍ واحدة؛ ثلاثةٌ لا اثنان، والثالثُ ليس تلطيفًا للثاني."""

    BARRED_BY_A_MEASURED_RULE = "ممتنعةٌ_بقاعدةٍ_تُفحَص_حيّة"
    JOINTLY_ATTESTED_ON_ONE_CARRIER = "اجتمعت_حالاتُها_على_حاملٍ_مُسمًّى"
    NOT_JOINTLY_ATTESTED_UNDECIDED = "لم_تجتمع_قطُّ_ولا_يحسمها_هذا_الإيداع"


def the_empty_fiber_is_refused_live() -> bool:
    """أيَرُدّ القياسُ ليفًا خاليًا فعلًا؟ يُفحَص بمحاولة إنشائه لا بالتصريح."""

    try:
        ObservedFiber(carrier="ل", frequency=1, composition=(), strata=())
    except ObservedStateFiberError:
        return True
    return False


@dataclass(frozen=True, slots=True)
class GapAdjudication:
    """ثغرةٌ واحدةٌ محكومةٌ بعلّتها، وشاهدُها مُسمًّى حيث يلزم الشاهد."""

    states: Fiber
    status: GapStatus
    witness_carrier: str | None
    grounds: str

    def __post_init__(self) -> None:
        if not self.grounds.strip():
            raise AmbientChoiceError("حكمٌ بلا علّةٍ مكتوبةٍ يُغري بالتعميم")
        if self.status is GapStatus.JOINTLY_ATTESTED_ON_ONE_CARRIER:
            if self.witness_carrier is None:
                raise AmbientChoiceError(
                    "شهادةُ الاجتماع تلزمها تسميةُ حاملها؛ وشهادةٌ بلا شاهدٍ دعوى"
                )
            if not self.states:
                raise AmbientChoiceError("مجموعةٌ خاليةٌ لا يُشهَد لها باجتماع")
        elif self.witness_carrier is not None:
            raise AmbientChoiceError(
                "لا يُسمَّى شاهدٌ لحكمٍ لا يقوم على شهادة؛ والتسميةُ ههنا إيهام"
            )

    @property
    def size(self) -> int:
        """حجمُ الثغرة، أي الرتبةُ التي كانت ستُشغَل لو سُدّت."""

        return len(self.states)


@dataclass(frozen=True, slots=True)
class GapCensus:
    """إحصاءُ الثغرات تحت عمليّةٍ مُسمّاة؛ ولا إحصاءَ بلا تسميتها."""

    operator: ClosureOperator
    population: Population
    instrument: MeasurementInstrument
    ambient_size: int
    adjudications: tuple[GapAdjudication, ...]

    def __post_init__(self) -> None:
        if self.population is not Population.OBSERVED:
            raise AmbientChoiceError("الثغراتُ تُحسَب عن المرصود؛ ولا تُوسَم بالمُعلَن")
        if self.instrument is not MeasurementInstrument.OBSERVED_FIBER:
            raise AmbientChoiceError("هذه ثغراتُ الليف؛ ولا يُنسَب رقمُها لآلةٍ أخرى")
        if len(self.adjudications) > self.ambient_size:
            raise AmbientChoiceError("الثغراتُ لا تتجاوز المحيطَ الذي حُسبت فيه")

    def count_of(self, status: GapStatus) -> int:
        """عدُّ الثغرات بحكمٍ مُسمًّى؛ مُشتَقٌّ بالعدّ لا مكتوبٌ بجانبه."""

        return sum(1 for item in self.adjudications if item.status is status)

    @property
    def barred(self) -> tuple[GapAdjudication, ...]:
        """الممتنعاتُ بقاعدةٍ قائمة، مسرودةً لتُفحَص لا لتُعَدّ فقط."""

        return tuple(
            item
            for item in self.adjudications
            if item.status is GapStatus.BARRED_BY_A_MEASURED_RULE
        )

    @property
    def every_state_is_individually_attested(self) -> bool:
        """أكلُّ حالةٍ مشهودةٌ على حِدَة؟ نعم دائمًا، ولذلك لا تصلح معيارًا."""

        return True


def adjudicate_gaps(
    operator: ClosureOperator = ClosureOperator.UNION_INTERSECTION,
    table: ObservedFiberTable | None = None,
) -> GapCensus:
    """قاضِ كلَّ ثغرةٍ في المحيط المختار: ممتنعةٌ، أو مشهودُ اجتماعٍ، أو لا تُحسَم."""

    fibers = observed_fibers(table)
    distinct = set(fibers.values())
    members = build_ambient(operator, table)
    if not the_empty_fiber_is_refused_live():
        raise FiberRankError(
            "قاعدةُ رفض الليف الخالي لم تعد قائمةً؛ ولا يُحكَم بامتناعٍ بلا قاعدة"
        )

    adjudications: list[GapAdjudication] = []
    for member in members:
        if member in distinct:
            continue
        if not member:
            adjudications.append(
                GapAdjudication(
                    states=member,
                    status=GapStatus.BARRED_BY_A_MEASURED_RULE,
                    witness_carrier=None,
                    grounds=(
                        "يردُّ `ObservedFiber` تركيبًا فارغًا عند الإنشاء، "
                        "والقاعدةُ مفحوصةٌ حيّةً لا منقولةً"
                    ),
                )
            )
            continue
        witness = next(
            (carrier for carrier, fiber in sorted(fibers.items()) if member <= fiber),
            None,
        )
        if witness is not None:
            adjudications.append(
                GapAdjudication(
                    states=member,
                    status=GapStatus.JOINTLY_ATTESTED_ON_ONE_CARRIER,
                    witness_carrier=witness,
                    grounds=(
                        f"اجتمعت حالاتُها كلُّها على الحامل {witness!r} في هذا "
                        "الإيداع، فاجتماعُها مقيسٌ ولا تمنعه قاعدةٌ قائمة"
                    ),
                )
            )
            continue
        adjudications.append(
            GapAdjudication(
                states=member,
                status=GapStatus.NOT_JOINTLY_ATTESTED_UNDECIDED,
                witness_carrier=None,
                grounds=(
                    "لم تجتمع حالاتُها على حاملٍ واحدٍ قطُّ ههنا؛ والغيابُ قد "
                    "يكون منعًا أو ندرةً أو تعذّرًا بالموضع، ولا يفصل بينها رصد"
                ),
            )
        )
    return GapCensus(
        operator=operator,
        population=Population.OBSERVED,
        instrument=MeasurementInstrument.OBSERVED_FIBER,
        ambient_size=len(members),
        adjudications=tuple(adjudications),
    )


# --- البواقي المُسمّاة --------------------------------------------------------


AN_UNDECIDED_GAP_IS_NOT_A_BARRED_ONE_NOTE: Final[str] = (
    "AnUndecidedGapIsNotABarredOne: ثغرةٌ لم تجتمع حالاتُها على حاملٍ قطُّ "
    "ليست ممتنعةً بنيويًّا؛ فغيابُ الاجتماع قد يكون منعًا أو ندرةً أو تعذّرًا "
    "بالموضع، والفرقُ بين «لم يُرصَد» و«ممتنع» فرقُ جنسٍ لا فرقُ درجة"
)

ATTESTATION_IS_NOT_A_CORPUS_CONSTRUCTION_NOTE: Final[str] = (
    "AttestationIsNotACorpusConstruction: أن تجتمع حالاتُ الثغرة على حاملٍ "
    "مُسمًّى يُثبِت أنّها غيرُ ممتنعة؛ ولا يُثبِت وجودَ مدوّنةٍ يكون ليفُ حاملٍ "
    "فيها هذه الثغرةَ بعينها لا أوسع، وتلك دعوى أخرى لم تُبنَ"
)

INDIVIDUAL_ATTESTATION_IS_NOT_JOINT_ATTESTATION_NOTE: Final[str] = (
    "IndividualAttestationIsNotJointAttestation: الحالاتُ السبعُ كلُّها مشهودةٌ "
    "فرادى، فمعيارُ «كلُّ حالةٍ منها رُصدت» لا يُخرِج ثغرةً واحدة؛ والمعيارُ "
    "الذي لا يردّ شيئًا لا يقيس شيئًا، فالمعتبَرُ شهادةُ الاجتماع على حامل"
)

ONLY_ONE_GAP_IS_BARRED_BY_A_MEASURED_RULE_NOTE: Final[str] = (
    "OnlyOneGapIsBarredByAMeasuredRule: القاعدةُ الوحيدةُ القائمةُ في هذه "
    "الشجرة ترُدُّ الليفَ الخالي وحدَه؛ وما عداه لا قاعدةَ تمنعه اليوم، "
    "فالامتناعُ البنيويُّ المُدَّعى لسواه يلزمه قانونٌ يُكتَب لا حدسٌ يُقال"
)

THE_AMBIENT_IS_A_CHOICE_NOT_A_MEASUREMENT_NOTE: Final[str] = (
    "TheAmbientIsAChoiceNotAMeasurement: الإغلاقُ تحت `∪`و`∩` عمليّةٌ مختارةٌ "
    "لا شيءٌ قاسه الليف، والإغلاقُ تحت الفرق يعطي شبكةً أخرى؛ فيُسمّى الإغلاقُ "
    "مع كلّ محيط، ويُفحَص أيُّ نتيجةٍ تنجو من تبديله"
)

THE_GAP_COUNT_IS_OPERATOR_RELATIVE_NOTE: Final[str] = (
    "TheGapCountIsOperatorRelative: الثغراتُ ٥٩ تحت الإغلاق النازل، و٨٠ تحت "
    "`∪∩`، و١١٢ تحت الفرق وتحت الشبكة الكاملة؛ فلا يُقال «عددُ الثغرات» "
    "مطلقًا، بل يُقال تحت أيّ عمليّةٍ عُدّ"
)

FIBER_AMBIENT_CHOICE_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    THE_AMBIENT_IS_A_CHOICE_NOT_A_MEASUREMENT_NOTE,
    THE_GAP_COUNT_IS_OPERATOR_RELATIVE_NOTE,
    ONLY_ONE_GAP_IS_BARRED_BY_A_MEASURED_RULE_NOTE,
    AN_UNDECIDED_GAP_IS_NOT_A_BARRED_ONE_NOTE,
    INDIVIDUAL_ATTESTATION_IS_NOT_JOINT_ATTESTATION_NOTE,
    ATTESTATION_IS_NOT_A_CORPUS_CONSTRUCTION_NOTE,
)
"""ستُّ بقايا مُسمّاةٍ تُقابَل بها أيُّ إحالةٍ إلى «المحيط» أو «عدد الثغرات»."""
