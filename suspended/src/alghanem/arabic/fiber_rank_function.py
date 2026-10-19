"""دالّةُ الرتبة على ليف الحامل: أين تكفي وتوحَد، وأين يسقط الأمران معًا.

الدعوى المعروضة للبرهان: **لا انقسامَ داخليًّا في الخانة يستدعي `RefineSlot`،
بل تدرّجٌ متّصلٌ في حجم الليف؛ والمطلوبُ دالّةُ رتبةٍ لا عمليّةُ تقسيم.** وهذه
الوحدةُ تبرهن شطرَها الذي يقوم، وتفنّد شطرَها الذي لا يقوم، بالعدّ في
الموضعين لا بالوصف.

**والرتبةُ تُسأل عن موطنها قبل أن تُسأل عن قيمتها.** فالسؤال «أتوجد دالّةُ
رتبة؟» لا جوابَ له حتّى يُسمّى الترتيبُ الذي تُبنى عليه. وههنا ترتيبان لا
واحد:

* **الشبكةُ المحيطة** `2^{S_obs}`: كلُّ مجموعةٍ جزئيّةٍ من حالاتٍ رُصدت، مرتّبةً
  بالاحتواء. وهذه **مدرَّجةٌ ومتّصلة**، فدالّةُ الرتبة فيها قائمةٌ وواحدة.
* **تحت-الترتيبِ المرصود**: الألياف التي وقعت فعلًا وحدَها، مرتّبةً بالاحتواء.
  وهذه **ليست مدرَّجةً ولا متّصلة**، فلا دالّةَ رتبةٍ فيها أصلًا، ولا معنى
  لسؤال وحدانيّتها.

**فالنتيجةُ في جملة**: الكفايةُ والوحدانيّةُ تثبتان في المحيط، وتسقطان في
المرصود؛ ونقلُ الثابت من المحيط إلى المرصود استبدالُ مفردةٍ بمفردة
(`A_RANK_FUNCTION_LIVES_ON_THE_AMBIENT_LATTICE_NOT_ON_THE_OBSERVED_SUBPOSET`).

**وثلاثةُ شواهدَ مضادّةٍ مقيسةٍ تُغلق الشطرَ الساقط:**

* **لا تدرّجَ متّصل**: رتبُ الألياف المرصودة `{1, 2, 3, 4, 6}`، وفي المدى ثقبٌ
  عند الخمسة. فقولُ «من واحدٍ إلى ستّة» يُوهم اتّصالًا لم يُقَس
  (`THE_OBSERVED_SIZES_ARE_NOT_A_CONTINUOUS_GRADATION`).
* **ولا دالّةَ رتبةٍ أصلًا**: بين ليف «س» وليف «ل» سلسلتان تامّتان مختلفتا
  الطول، وشرطُ الرتبة `ρ(y) = ρ(x) + 1` على كلّ تغطيةٍ يستحيل إرضاؤه معًا.
  والسقوطُ ههنا في **الوجود**، فالوحدانيّةُ لا تُسأل بعده.
* **ولو وُجدت لما توحّدت**: بيانُ التقابل مفكَّكٌ إلى مركّبتين — ليفُ «ض» لا
  يقارَن بشيء — فلكلّ مركّبةٍ ثابتٌ حرّ، والوحدانيّةُ تصير «إلى ثابتٍ لكلّ
  مركّبة» لا إلى ثابتٍ واحد
  (`UNIQUENESS_IS_UP_TO_ONE_CONSTANT_PER_COMPONENT`).

**والرتبةُ تُفقِد ما ترتّبه**: ثلاثةٌ وعشرون حاملًا تعطي ستّةَ عشرَ ليفًا
متمايزًا، وترسمها الرتبةُ إلى خمس قيمٍ لا غير. و«م» و«ي» في رتبةٍ واحدة
وليفاهما مختلفان لا يحتوي أحدُهما الآخر. فالرتبةُ دالّةٌ غيرُ متباينة، وما
يُشتَقّ منها لا يردّ الليف (`RANK_LOSES_THE_FIBER_IT_RANKS`).

**ولا رتبةَ بلا آلةٍ مُسمّاة**: الليفُ المرصود يبلغ أقصى رتبةٍ ستًّا، والمِرمازُ
يبلغ أربعًا، على الإيداع نفسِه. فالرقمُ عن آلةٍ لا عن نصّ
(`RANK_IS_INSTRUMENT_RELATIVE`).

**وأثرُ ذلك على `RefineSlot`**: صدقتِ المقدّمة في أنّ المقيسَ ليس انقسامًا
داخليًّا في الخانة؛ وهذا **لا يرخّص `RefineSlot`** ولا يرخّص دالّةَ الرتبةِ
بديلًا عنها في المرصود، إذ البديلُ المقترَحُ لا وجودَ له هناك. فالعمليّتان
كلتاهما غيرُ مرخَّصتين، بعلّتين مختلفتين مكتوبتين. **وعدمُ الترخيص ليس
تفنيدًا**: ضرورةُ `RefineSlot` عمومًا تبقى **غيرَ مبرهنة**
(`A_RANK_FUNCTION_DOES_NOT_LICENSE_REFINE_SLOT`).

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
    ObservedFiberTable,
    run_observed_fiber_on_the_deposited_fatiha,
)
from .decomposition_reconstruction_theorem import (
    MeasurementInstrument,
    Population,
    census_of_observed_population,
)

__all__ = [
    "A_RANK_FUNCTION_DOES_NOT_LICENSE_REFINE_SLOT_NOTE",
    "A_RANK_FUNCTION_LIVES_ON_THE_AMBIENT_LATTICE_NOTE",
    "FIBER_RANK_NAMED_RESIDUALS",
    "RANK_IS_INSTRUMENT_RELATIVE_NOTE",
    "RANK_LOSES_THE_FIBER_IT_RANKS_NOTE",
    "THE_OBSERVED_SIZES_ARE_NOT_A_CONTINUOUS_GRADATION_NOTE",
    "UNIQUENESS_IS_UP_TO_ONE_CONSTANT_PER_COMPONENT_NOTE",
    "AmbientRankProof",
    "ClaimVerdict",
    "EqualRankWitness",
    "FiberRankError",
    "ObservedRankRefutation",
    "UnequalChainWitness",
    "maximum_rank_by_instrument",
    "observed_fibers",
    "prove_rank_on_the_ambient_lattice",
    "rank_by_carrier",
    "refute_rank_on_the_observed_population",
]


class FiberRankError(ValueError):
    """رفضٌ صريح: شاهدٌ لا يشهد، أو رتبةٌ تُسند إلى ترتيبٍ لم يُسمَّ."""


class ClaimVerdict(Enum):
    """حكمُ دعوى، مفردةٌ مغلقةٌ لا درجاتٍ بينها ولا نسبةَ نجاح."""

    PROVEN_BY_EXHAUSTION = "مبرهَنةٌ_باستقصاء_الحالات"
    REFUTED_BY_COUNTER_WITNESS = "مفنَّدةٌ_بشاهدٍ_مضادّ"
    NOT_ASKED_BECAUSE_EXISTENCE_FAILED = "لا_تُسأل_لأنّ_الوجود_سقط"


StateVector = tuple[tuple[str, str], ...]
"""حالةٌ واحدةٌ متَّجِهةً على محاورها، كما يُخرجها الليفُ المرصود."""

Fiber = frozenset[StateVector]
"""ليفُ حاملٍ واحد: مجموعةُ حالاته المرصودة، لا عددُها."""


def observed_fibers(table: ObservedFiberTable | None = None) -> Mapping[str, Fiber]:
    """أليافُ الحوامل كما رُصدت، مُشتقّةً من جدول القياس لا مكتوبةً بجانبه."""

    measured = run_observed_fiber_on_the_deposited_fatiha() if table is None else table
    return {fiber.carrier: frozenset(fiber.composition) for fiber in measured.fibers}


def rank_by_carrier(table: ObservedFiberTable | None = None) -> Mapping[str, int]:
    """`ρ(c) = |S_obs(c)|`، مُشتقّةً بالعدّ؛ وهي رتبةٌ بالاسم لا بالبرهان بعدُ."""

    return {carrier: len(fiber) for carrier, fiber in observed_fibers(table).items()}


def maximum_rank_by_instrument(
    table: ObservedFiberTable | None = None,
) -> Mapping[MeasurementInstrument, int]:
    """أقصى رتبةٍ بكلّ آلة، محسوبةً بالآلتين حيّتين لا منقولةً من نصّ."""

    fiber_maximum = max(rank_by_carrier(table).values())
    codec_capacities = census_of_observed_population().observed_capacities
    return {
        MeasurementInstrument.OBSERVED_FIBER: fiber_maximum,
        MeasurementInstrument.CODEC_UNIT: max(codec_capacities),
    }


# --- الشبكةُ المحيطة: ههنا تقوم الكفايةُ والوحدانيّة -------------------------


def _ambient_universe(fibers: Mapping[str, Fiber]) -> tuple[StateVector, ...]:
    universe: set[StateVector] = set()
    for fiber in fibers.values():
        universe |= fiber
    return tuple(sorted(universe))


def _ambient_lattice(universe: tuple[StateVector, ...]) -> tuple[Fiber, ...]:
    subsets: list[Fiber] = []
    for size in range(len(universe) + 1):
        for chosen in combinations(universe, size):
            subsets.append(frozenset(chosen))
    return tuple(subsets)


@dataclass(frozen=True, slots=True)
class AmbientRankProof:
    """برهانُ الرتبة على الشبكة المحيطة: وجودٌ بالاستقصاء، ووحدانيّةٌ بالإلزام."""

    universe_size: int
    lattice_size: int
    covers_examined: int
    every_cover_raises_the_rank_by_one: bool
    hasse_diagram_is_connected: bool
    forced_values_agree_on_every_decomposition: bool
    forced_values_equal_cardinality: bool

    def __post_init__(self) -> None:
        if self.universe_size <= 0:
            raise FiberRankError("شبكةٌ على مفردةٍ خاليةٍ لا يُبرهَن عليها شيء")
        if self.lattice_size != 2**self.universe_size:
            raise FiberRankError("حجمُ الشبكة `2^n` بالبناء؛ ورقمٌ يخالفه دليلُ عدٍّ ناقص")
        if self.covers_examined <= 0:
            raise FiberRankError("برهانٌ بلا تغطيةٍ مفحوصةٍ برهانٌ بلا فحص")

    @property
    def sufficiency(self) -> ClaimVerdict:
        """أتكفي السعةُ دالّةَ رتبةٍ ههنا؟ يُجاب باستقصاء التغطيات كلِّها."""

        if self.every_cover_raises_the_rank_by_one:
            return ClaimVerdict.PROVEN_BY_EXHAUSTION
        return ClaimVerdict.REFUTED_BY_COUNTER_WITNESS

    @property
    def uniqueness(self) -> ClaimVerdict:
        """أواحدةٌ هي؟ اتّصالُ البيان يلزم ثابتًا واحدًا، والإلزامُ يثبّت القيم."""

        if self.sufficiency is not ClaimVerdict.PROVEN_BY_EXHAUSTION:
            return ClaimVerdict.NOT_ASKED_BECAUSE_EXISTENCE_FAILED
        if (
            self.hasse_diagram_is_connected
            and self.forced_values_agree_on_every_decomposition
            and self.forced_values_equal_cardinality
        ):
            return ClaimVerdict.PROVEN_BY_EXHAUSTION
        return ClaimVerdict.REFUTED_BY_COUNTER_WITNESS

    @property
    def free_constants(self) -> int:
        """عددُ الثوابت الحرّة: مركّبةٌ واحدةٌ متّصلةٌ تعني ثابتًا واحدًا لا أكثر."""

        return 1 if self.hasse_diagram_is_connected else 0


def _covers_step_by_one(lattice: tuple[Fiber, ...]) -> tuple[bool, int]:
    examined = 0
    for lower in lattice:
        for upper in lattice:
            if not lower < upper:
                continue
            if any(lower < middle < upper for middle in lattice):
                continue
            examined += 1
            if len(upper) - len(lower) != 1:
                return False, examined
    return True, examined


def _hasse_is_connected(lattice: tuple[Fiber, ...]) -> bool:
    neighbours: dict[Fiber, list[Fiber]] = {node: [] for node in lattice}
    for lower in lattice:
        for upper in lattice:
            if lower < upper and len(upper) - len(lower) == 1:
                neighbours[lower].append(upper)
                neighbours[upper].append(lower)
    seen: set[Fiber] = {lattice[0]}
    stack: list[Fiber] = [lattice[0]]
    while stack:
        node = stack.pop()
        for adjacent in neighbours[node]:
            if adjacent not in seen:
                seen.add(adjacent)
                stack.append(adjacent)
    return len(seen) == len(lattice)


def _forced_values(lattice: tuple[Fiber, ...]) -> tuple[bool, bool]:
    """ألزِم القيمَ من `ρ(∅) = 0` و`ρ({s}) = 1` بالقاعدة الجمعيّة، ثمّ قابِلها.

    والقاعدةُ هي `ρ(A ∪ B) + ρ(A ∩ B) = ρ(A) + ρ(B)`؛ ومتى كان `A` غيرَ خالٍ
    فلكلّ عنصرٍ فيه تفكيكٌ يُلزِم قيمتَه. فإن اتّفقت التفكيكاتُ كلُّها فالقيمةُ
    واحدةٌ لا اختيارَ فيها، وتلك هي الوحدانيّة.
    """

    forced: dict[Fiber, int] = {frozenset(): 0}
    agree = True
    for node in sorted(lattice, key=len):
        if not node:
            continue
        candidates = {forced[node - {element}] + 1 for element in node}
        if len(candidates) != 1:
            agree = False
        forced[node] = min(candidates)
    equals_cardinality = all(forced[node] == len(node) for node in lattice)
    return agree, equals_cardinality


def prove_rank_on_the_ambient_lattice(
    table: ObservedFiberTable | None = None,
) -> AmbientRankProof:
    """برهِن على الشبكة المحيطة: الرتبةُ قائمةٌ، وواحدةٌ، وهي العدُّ نفسُه."""

    universe = _ambient_universe(observed_fibers(table))
    lattice = _ambient_lattice(universe)
    steps_by_one, examined = _covers_step_by_one(lattice)
    agree, equals_cardinality = _forced_values(lattice)
    return AmbientRankProof(
        universe_size=len(universe),
        lattice_size=len(lattice),
        covers_examined=examined,
        every_cover_raises_the_rank_by_one=steps_by_one,
        hasse_diagram_is_connected=_hasse_is_connected(lattice),
        forced_values_agree_on_every_decomposition=agree,
        forced_values_equal_cardinality=equals_cardinality,
    )


# --- تحت-الترتيبِ المرصود: ههنا يسقط الوجودُ قبل الوحدانيّة ------------------


@dataclass(frozen=True, slots=True)
class UnequalChainWitness:
    """شاهدٌ مضادّ: طرفان بينهما سلسلتان تامّتان مختلفتا الطول، فلا تدريج."""

    lower_carriers: tuple[str, ...]
    upper_carriers: tuple[str, ...]
    lower_rank: int
    upper_rank: int
    chain_lengths: tuple[int, ...]
    shortest_chain: tuple[str, ...]
    longest_chain: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.lower_carriers or not self.upper_carriers:
            raise FiberRankError("شاهدٌ بلا طرفين مُسمّيين لا يُراجَع")
        if len(set(self.chain_lengths)) < 2:
            raise FiberRankError(
                "سلسلتان متساويتا الطول لا تشهدان على سقوط التدريج؛ "
                "ولا يُسجَّل اتّفاقٌ في جدول شواهدَ مضادّة"
            )
        if self.lower_rank >= self.upper_rank:
            raise FiberRankError("الطرفُ الأدنى أدنى رتبةً بالبناء")
        if len(self.shortest_chain) >= len(self.longest_chain):
            raise FiberRankError("أقصرُ السلسلتين أقصرُ فعلًا، وإلّا فالتسميةُ خطأ")


@dataclass(frozen=True, slots=True)
class EqualRankWitness:
    """شاهدٌ على أنّ الرتبةَ لا تردّ ليفَها: حاملان في رتبةٍ واحدةٍ بليفين مختلفين."""

    first_carrier: str
    second_carrier: str
    shared_rank: int
    shared_states: int
    comparable: bool

    def __post_init__(self) -> None:
        if self.first_carrier == self.second_carrier:
            raise FiberRankError("حاملٌ لا يشهد على نفسه")
        if self.comparable:
            raise FiberRankError(
                "ليفان متساويا الرتبةِ ومتقارنان هما ليفٌ واحد؛ ولا شاهدَ فيه"
            )


@dataclass(frozen=True, slots=True)
class ObservedRankRefutation:
    """تفنيدُ الرتبة على المفردة المرصودة: الوجودُ أوّلًا، ثمّ ما يتفرّع عنه."""

    population: Population
    instrument: MeasurementInstrument
    source_id: str
    carrier_count: int
    distinct_fiber_count: int
    rank_values: tuple[int, ...]
    unequal_chain_witnesses: tuple[UnequalChainWitness, ...]
    comparability_component_count: int
    equal_rank_witnesses: tuple[EqualRankWitness, ...]

    def __post_init__(self) -> None:
        if self.population is not Population.OBSERVED:
            raise FiberRankError("هذا التفنيدُ على ما وقع؛ ولا يُوسَم بمفردةٍ مُعلَنة")
        if self.instrument is not MeasurementInstrument.OBSERVED_FIBER:
            raise FiberRankError("رتبُ الألياف تُقاس بالليف؛ ولا يُنسَب رقمُها لغيره")
        if self.distinct_fiber_count > self.carrier_count:
            raise FiberRankError("الأليافُ المتمايزةُ لا تزيد على حواملها")
        if tuple(sorted(set(self.rank_values))) != self.rank_values:
            raise FiberRankError("قيمُ الرتبة مجموعةٌ مرتّبةٌ بلا تكرار")

    @property
    def existence(self) -> ClaimVerdict:
        """أتوجد دالّةُ رتبةٍ ههنا أصلًا؟ سلسلتان مختلفتا الطول تمنعها."""

        if self.unequal_chain_witnesses:
            return ClaimVerdict.REFUTED_BY_COUNTER_WITNESS
        return ClaimVerdict.PROVEN_BY_EXHAUSTION

    @property
    def uniqueness(self) -> ClaimVerdict:
        """الوحدانيّةُ لا تُسأل بعد سقوط الوجود؛ ولو قامت لَتعدّدت بالتفكّك."""

        if self.existence is ClaimVerdict.REFUTED_BY_COUNTER_WITNESS:
            return ClaimVerdict.NOT_ASKED_BECAUSE_EXISTENCE_FAILED
        if self.comparability_component_count > 1:
            return ClaimVerdict.REFUTED_BY_COUNTER_WITNESS
        return ClaimVerdict.PROVEN_BY_EXHAUSTION

    @property
    def free_constants(self) -> int:
        """ثابتٌ حرٌّ لكلّ مركّبةٍ متّصلة؛ فالوحدانيّةُ «إلى ثابتٍ واحد» دعوى."""

        return self.comparability_component_count

    @property
    def rank_determines_the_fiber(self) -> bool:
        """أتردّ الرتبةُ ليفَها؟ يُجاب بمقابلة عدد الألياف بعدد القيم."""

        return self.distinct_fiber_count == len(self.rank_values)

    @property
    def rank_range_is_contiguous(self) -> bool:
        """أمتّصلٌ مدى الرتب المقيسة؟ يُجاب بالعدّ لا بوصف «من واحدٍ إلى ستّة»."""

        if not self.rank_values:
            return False
        low, high = self.rank_values[0], self.rank_values[-1]
        return tuple(range(low, high + 1)) == self.rank_values


def _observed_covers(fibers: tuple[Fiber, ...]) -> dict[Fiber, tuple[Fiber, ...]]:
    covers: dict[Fiber, tuple[Fiber, ...]] = {}
    for lower in fibers:
        above = [
            upper
            for upper in fibers
            if lower < upper and not any(lower < middle < upper for middle in fibers)
        ]
        covers[lower] = tuple(above)
    return covers


def _maximal_chains(
    lower: Fiber,
    upper: Fiber,
    covers: Mapping[Fiber, tuple[Fiber, ...]],
) -> tuple[tuple[Fiber, ...], ...]:
    if lower == upper:
        return ((lower,),)
    chains: list[tuple[Fiber, ...]] = []
    for step in covers[lower]:
        if step <= upper:
            for tail in _maximal_chains(step, upper, covers):
                chains.append((lower, *tail))
    return tuple(chains)


def _component_count(fibers: tuple[Fiber, ...]) -> int:
    parent: dict[Fiber, Fiber] = {node: node for node in fibers}

    def find(node: Fiber) -> Fiber:
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    for first, second in combinations(fibers, 2):
        if first < second or second < first:
            root_first, root_second = find(first), find(second)
            if root_first != root_second:
                parent[root_first] = root_second
    return len({find(node) for node in fibers})


def refute_rank_on_the_observed_population(
    table: ObservedFiberTable | None = None,
) -> ObservedRankRefutation:
    """فنِّد الرتبةَ على المرصود: بشاهدٍ مضادٍّ على الوجود، وبتفكّكٍ على الوحدانيّة."""

    measured = run_observed_fiber_on_the_deposited_fatiha() if table is None else table
    fibers = observed_fibers(measured)
    carriers_of: dict[Fiber, tuple[str, ...]] = {}
    for carrier, fiber in fibers.items():
        carriers_of[fiber] = (*carriers_of.get(fiber, ()), carrier)
    distinct = tuple(sorted(carriers_of, key=len))
    covers = _observed_covers(distinct)

    witnesses: list[UnequalChainWitness] = []
    for lower in distinct:
        for upper in distinct:
            if not lower < upper:
                continue
            chains = _maximal_chains(lower, upper, covers)
            lengths = {len(chain) - 1 for chain in chains}
            if len(lengths) < 2:
                continue
            shortest = min(chains, key=len)
            longest = max(chains, key=len)
            witnesses.append(
                UnequalChainWitness(
                    lower_carriers=carriers_of[lower],
                    upper_carriers=carriers_of[upper],
                    lower_rank=len(lower),
                    upper_rank=len(upper),
                    chain_lengths=tuple(sorted(lengths)),
                    shortest_chain=tuple(carriers_of[node][0] for node in shortest),
                    longest_chain=tuple(carriers_of[node][0] for node in longest),
                )
            )

    equal_rank: list[EqualRankWitness] = []
    for first, second in combinations(distinct, 2):
        if len(first) != len(second):
            continue
        equal_rank.append(
            EqualRankWitness(
                first_carrier=carriers_of[first][0],
                second_carrier=carriers_of[second][0],
                shared_rank=len(first),
                shared_states=len(first & second),
                comparable=first < second or second < first,
            )
        )

    return ObservedRankRefutation(
        population=Population.OBSERVED,
        instrument=MeasurementInstrument.OBSERVED_FIBER,
        source_id=measured.deposit.source_id,
        carrier_count=len(fibers),
        distinct_fiber_count=len(distinct),
        rank_values=tuple(sorted({len(fiber) for fiber in distinct})),
        unequal_chain_witnesses=tuple(witnesses),
        comparability_component_count=_component_count(distinct),
        equal_rank_witnesses=tuple(equal_rank),
    )


# --- البواقي المُسمّاة --------------------------------------------------------


A_RANK_FUNCTION_DOES_NOT_LICENSE_REFINE_SLOT_NOTE: Final[str] = (
    "ARankFunctionDoesNotLicenseRefineSlot: صدقَ أنّ المقيسَ ليس انقسامًا "
    "داخليًّا في الخانة، ولا يلزم من ذلك ترخيصُ `RefineSlot` ولا ترخيصُ دالّة "
    "الرتبة بديلًا عنها؛ فالبديلُ المقترَحُ لا وجودَ له في المفردة المرصودة، "
    "والعمليّتان غيرُ مرخَّصتين بعلّتين مختلفتين — وعدمُ الترخيص ليس تفنيدًا "
    "لضرورة `RefineSlot` عمومًا، فتلك غيرُ مبرهنةٍ لا منتقضة"
)

A_RANK_FUNCTION_LIVES_ON_THE_AMBIENT_LATTICE_NOTE: Final[str] = (
    "ARankFunctionLivesOnTheAmbientLatticeNotOnTheObservedSubposet: الكفايةُ "
    "والوحدانيّةُ تثبتان على `2^{S_obs}` مرتّبةً بالاحتواء، وتسقطان على "
    "الألياف الواقعة وحدَها؛ ونقلُ الثابت من المحيط إلى المرصود استبدالُ "
    "مفردةٍ بمفردة"
)

RANK_IS_INSTRUMENT_RELATIVE_NOTE: Final[str] = (
    "RankIsInstrumentRelative: أقصى رتبةٍ ستٌّ بالليف وأربعٌ بالمِرماز على "
    "الإيداع نفسِه؛ فلا تُقال «رتبةُ الحامل» مطلقًا، بل يُقال بأيّ آلةٍ قيست"
)

RANK_LOSES_THE_FIBER_IT_RANKS_NOTE: Final[str] = (
    "RankLosesTheFiberItRanks: ثلاثةٌ وعشرون حاملًا تعطي ستّةَ عشرَ ليفًا "
    "متمايزًا ترسمها الرتبةُ إلى خمس قيم؛ فهي غيرُ متباينة، ولا يُستردّ منها "
    "الليفُ الذي رتّبته"
)

THE_OBSERVED_SIZES_ARE_NOT_A_CONTINUOUS_GRADATION_NOTE: Final[str] = (
    "TheObservedSizesAreNotAContinuousGradation: رتبُ الألياف المرصودة "
    "`{1, 2, 3, 4, 6}`، وفي المدى ثقبٌ عند الخمسة؛ فالتدرّجُ المتّصلُ وصفٌ لم "
    "يُقَس، ويُجاب عنه بالعدّ"
)

UNIQUENESS_IS_UP_TO_ONE_CONSTANT_PER_COMPONENT_NOTE: Final[str] = (
    "UniquenessIsUpToOneConstantPerComponent: وحدانيّةُ الرتبة «إلى ثابتٍ» "
    "تلزمها مركّبةٌ متّصلةٌ واحدة؛ وبيانُ المرصود مركّبتان، فلكلٍّ ثابتُها، "
    "ولا وحدانيّةَ بثابتٍ واحد"
)

FIBER_RANK_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_RANK_FUNCTION_LIVES_ON_THE_AMBIENT_LATTICE_NOTE,
    THE_OBSERVED_SIZES_ARE_NOT_A_CONTINUOUS_GRADATION_NOTE,
    UNIQUENESS_IS_UP_TO_ONE_CONSTANT_PER_COMPONENT_NOTE,
    RANK_LOSES_THE_FIBER_IT_RANKS_NOTE,
    RANK_IS_INSTRUMENT_RELATIVE_NOTE,
    A_RANK_FUNCTION_DOES_NOT_LICENSE_REFINE_SLOT_NOTE,
)
"""ستُّ بقايا مُسمّاةٍ تُقابَل بها أيُّ إحالةٍ مرسَلةٍ إلى «دالّة الرتبة»."""
