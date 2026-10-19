"""النموذجُ الصفريُّ المحافظ: استقلالٌ شرطيٌّ يُختبَر، لا مقارنةُ أعدادٍ عارية.

هذه الوحدةُ تُشغِّل الاختبارَ الذي جُمِّدت مواصفتُه في
`carrier_fiber_preregistration` على جدولٍ مقيسٍ من `carrier_state_observed_fiber`،
ولا تُبنى نتيجةٌ فيها إلا مربوطةً بتلك المواصفة محتوًى وبصمةً.

**والمحكُّ استقلالٌ شرطيّ لا سعةُ ليفٍ عارية:**

    H0: State ⟂ Carrier | Frequency, Position, Boundary
    H1: State ⟂̸ Carrier | Frequency, Position, Boundary

وإعادةُ التوزيع تُنفِّذ الضبطَ بالبناء لا بالتصريح: الحواملُ تبقى في مواضعها
كما هي — فيبقى `freq(C)` وموضعُ كلّ وقوعٍ وطرفيّتُه كما رُصِدت — وتُخلَط
الحالاتُ **داخلَ الطبقة الواحدة** `(position_in_word, boundary)` ولا تعبر
الطبقاتِ. فما بقي من فرقٍ بعد ذلك لا يفسّره تردّدٌ ولا موضعٌ ولا طرفيّة.

**ومقياسان لا واحد، ولا حقلَ يجمعهما:**

    Capacity(C)    = |S_obs(C)|
    Composition(C) = المسافةُ بين P(S | C) وبين ما تتوقّعه طبقاتُ C وحدَها

فحاملان قد يتساويان في السعة ويختلفان في التركيب، فقراءتُهما حقلان اثنان في
كلّ صفّ، ودمجُهما في حكمٍ واحدٍ مرفوضٌ بالبناء
(`NO_MEASURE_COLLAPSE`). والأرقامُ كلُّها صحيحةٌ بالألف لا عائمة، فلا يدخل
فرقُ تقريبٍ بين تشغيلين.

**والمخرجُ من مفردةٍ ثلاثيةٍ مُجمَّدةٍ قبل الدليل**: `NARROWER_THAN_CHANCE` أو
`INDISTINGUISHABLE_FROM_CHANCE` أو `UNDETERMINED`؛ وحاملٌ دعمُه دون الحدّ
المُجمَّد يُقرأ `UNDETERMINED` ولا يُقرأ تأييدًا ولا تفنيدًا
(`LOW_SUPPORT_IS_UNDETERMINED_NOT_SUPPORT`).

**وما لا تقوله هذه الوحدةُ مكتوبٌ باسمه**: ضيقٌ أكثرَ من الصدفة ليس ليفًا
مرخَّصًا (`NARROWER_THAN_CHANCE_IS_NOT_A_LICENSED_FIBER`)، وضبطُ ثلاثِ
مشاركاتٍ ليس ضبطًا لكلّ مشاركة (`THREE_CONTROLS_ARE_NOT_ALL_CONTROLS`)، ونموذجُ
إعادة التوزيع ليس نموذجًا توليديًّا للغة
(`A_PERMUTATION_NULL_IS_NOT_A_GENERATIVE_MODEL`).

**ولا سلطةَ لهذه الوحدة**: لا ولادةَ، ولا حكمَ ولادة، ولا تجميدَ `E0`، ولا
تقرؤها بوّابةٌ في `kernel/`.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, fields
from fractions import Fraction
from typing import Final

from .carrier_fiber_preregistration import (
    CarrierFiberSpecificationContentBinding,
    FiberOutcome,
    freeze_declared_specification,
)
from .carrier_state_observed_fiber import (
    ObservedFiberTable,
    run_observed_fiber_on_the_deposited_fatiha,
)

__all__ = [
    "A_PERMUTATION_NULL_IS_NOT_A_GENERATIVE_MODEL",
    "CARRIER_FIBER_NULL_MODEL_NAMED_RESIDUALS",
    "LOW_SUPPORT_IS_UNDETERMINED_NOT_SUPPORT",
    "NARROWER_THAN_CHANCE_IS_NOT_A_LICENSED_FIBER",
    "NO_MEASURE_COLLAPSE",
    "SEEDED_DETERMINISM_IS_INTERPRETER_RELATIVE",
    "THREE_CONTROLS_ARE_NOT_ALL_CONTROLS",
    "CarrierFiberNullModelError",
    "CarrierFiberReading",
    "ConditionalIndependenceReadout",
    "StateVector",
    "assess_conditional_independence",
    "run_null_model_on_the_deposited_fatiha",
]


class CarrierFiberNullModelError(ValueError):
    """رفضٌ عند الإنشاء: نتيجةٌ بلا مواصفةٍ سبقتها، أو حقلٌ يجمع المقياسين."""


StateVector = tuple[tuple[str, str], ...]
"""الحالةُ متَّجِهًا على المحاور المقيسة؛ الاسمُ مختصرٌ للقراءة لا نوعٌ جديد."""


_PERMILLE: Final = 1000


def _permille_floor(value: Fraction) -> int:
    return int(value * _PERMILLE)


# --- قراءةُ حاملٍ واحد: مقياسان في حقلين، ومخرجان في حقلين -------------------


@dataclass(frozen=True, slots=True)
class CarrierFiberReading:
    """قراءةُ ليف حاملٍ واحد تحت النموذج الصفريّ؛ مقياسان لا مقياسٌ مدموج.

    والاحتمالُ مذكورٌ بالألف صحيحًا، ومُشتَقٌّ من عدّ إعادات التوزيع التي بلغت
    المرصودَ أو جاوزته في الاتّجاه المُعلَن، بقاعدة الإضافة الواحدة؛ فلا يُقرأ
    صفرٌ احتمالًا معدومًا في عيّنةٍ منتهية.
    """

    carrier: str
    frequency: int
    observed_capacity: int
    null_capacity_at_or_below_observed: int
    observed_composition_divergence_permille: int
    null_composition_at_or_above_observed: int
    resampling_count: int
    capacity_outcome: FiberOutcome
    composition_outcome: FiberOutcome

    def __post_init__(self) -> None:
        if len(self.carrier) != 1:
            raise CarrierFiberNullModelError("حاملُ القراءة رمزٌ واحد")
        if self.frequency <= 0 or self.observed_capacity <= 0:
            raise CarrierFiberNullModelError("قراءةٌ بلا وقوعٍ لا تُكتَب")
        if self.resampling_count <= 0:
            raise CarrierFiberNullModelError("إعادةُ التوزيع مرّةً فأكثر")
        for outcome in (self.capacity_outcome, self.composition_outcome):
            if not isinstance(outcome, FiberOutcome):
                raise CarrierFiberNullModelError("المخرجُ عضوٌ في المفردة المُجمَّدة")

    @property
    def capacity_p_value_permille(self) -> int:
        """احتمالُ السعة بالألف، صعودًا، بقاعدة `(k+1)/(N+1)`."""

        value = Fraction(
            self.null_capacity_at_or_below_observed + 1, self.resampling_count + 1
        )
        return -((-value * _PERMILLE).__floor__())

    @property
    def composition_p_value_permille(self) -> int:
        """احتمالُ التركيب بالألف، صعودًا، بالقاعدة نفسِها."""

        value = Fraction(
            self.null_composition_at_or_above_observed + 1, self.resampling_count + 1
        )
        return -((-value * _PERMILLE).__floor__())


@dataclass(frozen=True, slots=True)
class ConditionalIndependenceReadout:
    """قراءةُ تشغيلٍ واحد: مواصفتُه، ومصدرُه، وصفُّ كلّ حاملٍ، وقراءةٌ إجمالية."""

    binding: CarrierFiberSpecificationContentBinding
    source_id: str
    source_sha256: str
    rows: tuple[CarrierFiberReading, ...]
    observed_support_size: int
    null_support_at_or_below_observed: int
    observed_mean_divergence_permille: int
    null_mean_divergence_at_or_above_observed: int
    resampling_count: int
    carriers_below_support_threshold: tuple[str, ...]

    def __post_init__(self) -> None:
        if type(self.binding) is not CarrierFiberSpecificationContentBinding:
            raise CarrierFiberNullModelError(
                "لا تُبنى نتيجةٌ إلا مربوطةً بمواصفةٍ سبقتها تجميدًا ومحتوًى"
            )
        if not self.source_sha256:
            raise CarrierFiberNullModelError("نتيجةٌ بلا بصمةِ مصدرها لا تُعاد")
        if not self.rows:
            raise CarrierFiberNullModelError("قراءةٌ بلا صفوفٍ لا تُكتَب")

    @property
    def content_id_digest(self) -> str:
        """بصمةُ المواصفة التي سبقت هذه النتيجة."""

        return self.binding.content_id.digest

    def reading_for(self, carrier: str) -> CarrierFiberReading:
        """صفُّ حاملٍ بعينه؛ وحاملٌ لم يُقرأ يُرَدّ باسمه لا بصفٍّ فارغ."""

        for row in self.rows:
            if row.carrier == carrier:
                return row
        raise CarrierFiberNullModelError("حاملٌ لا صفَّ له في هذه القراءة")

    @property
    def carriers_narrower_than_chance(self) -> tuple[str, ...]:
        """الحواملُ التي ضاق ليفُها أكثرَ ممّا يفسّره الضبطُ المُجمَّد."""

        return tuple(
            row.carrier
            for row in self.rows
            if row.capacity_outcome is FiberOutcome.NARROWER_THAN_CHANCE
        )

    @property
    def carriers_with_distinctive_composition(self) -> tuple[str, ...]:
        """الحواملُ التي تميّز تركيبُ ليفها أكثرَ ممّا يفسّره الضبطُ المُجمَّد."""

        return tuple(
            row.carrier
            for row in self.rows
            if row.composition_outcome is FiberOutcome.NARROWER_THAN_CHANCE
        )


_COLLAPSING_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "combined",
    "overall",
    "merged",
    "verdict",
    "final",
)

for _declaring_type in (
    CarrierFiberReading,
    ConditionalIndependenceReadout,
):  # pragma: no cover - import guard
    for _field in fields(_declaring_type):
        if any(marker in _field.name for marker in _COLLAPSING_FIELD_MARKERS):
            raise RuntimeError(
                "capacity and composition may not be merged into one field"
            )


# --- الإحصاءتان، مُشتقّتين من الصفوف لا مكتوبتين بجانبها ---------------------


def _support_size(assignment: list[tuple[str, StateVector]]) -> int:
    seen: set[tuple[str, StateVector]] = set()
    for carrier, state in assignment:
        seen.add((carrier, state))
    return len(seen)


def _capacity_by_carrier(
    assignment: list[tuple[str, StateVector]],
) -> dict[str, int]:
    states: dict[str, set[StateVector]] = {}
    for carrier, state in assignment:
        states.setdefault(carrier, set()).add(state)
    return {carrier: len(values) for carrier, values in states.items()}


def _pooled_reference(
    strata: list[tuple[int, str]], states: list[StateVector]
) -> dict[tuple[int, str], dict[StateVector, Fraction]]:
    counts: dict[tuple[int, str], dict[StateVector, int]] = {}
    sizes: dict[tuple[int, str], int] = {}
    for stratum, state in zip(strata, states):
        bucket = counts.setdefault(stratum, {})
        bucket[state] = bucket.get(state, 0) + 1
        sizes[stratum] = sizes.get(stratum, 0) + 1
    return {
        stratum: {
            state: Fraction(count, sizes[stratum]) for state, count in bucket.items()
        }
        for stratum, bucket in counts.items()
    }


def _divergence_by_carrier(
    carriers: list[str],
    strata: list[tuple[int, str]],
    states: list[StateVector],
    pooled: dict[tuple[int, str], dict[StateVector, Fraction]],
) -> dict[str, Fraction]:
    observed: dict[str, dict[StateVector, int]] = {}
    expected: dict[str, dict[StateVector, Fraction]] = {}
    totals: dict[str, int] = {}
    for carrier, stratum, state in zip(carriers, strata, states):
        totals[carrier] = totals.get(carrier, 0) + 1
        bucket = observed.setdefault(carrier, {})
        bucket[state] = bucket.get(state, 0) + 1
        reference = expected.setdefault(carrier, {})
        for pooled_state, probability in pooled[stratum].items():
            reference[pooled_state] = reference.get(pooled_state, Fraction(0))
            reference[pooled_state] += probability
    divergence: dict[str, Fraction] = {}
    for carrier, total in totals.items():
        seen = set(observed[carrier]) | set(expected[carrier])
        distance = Fraction(0)
        for state in seen:
            observed_share = Fraction(observed[carrier].get(state, 0), total)
            expected_share = expected[carrier].get(state, Fraction(0)) / total
            distance += abs(observed_share - expected_share)
        divergence[carrier] = distance / 2
    return divergence


def _mean_divergence(
    divergence: dict[str, Fraction], frequency: dict[str, int]
) -> Fraction:
    total = sum(frequency.values())
    if total == 0:  # pragma: no cover - guarded by caller
        return Fraction(0)
    weighted = sum(divergence[carrier] * frequency[carrier] for carrier in divergence)
    return Fraction(weighted, 1) / total


# --- التشغيل: إعادةُ توزيعٍ داخلَ الطبقة، والحواملُ لا تتحرّك ----------------


def assess_conditional_independence(
    table: ObservedFiberTable,
    *,
    binding: CarrierFiberSpecificationContentBinding,
) -> ConditionalIndependenceReadout:
    """اختبِر استقلالَ الحالة عن الحامل بعد ضبط التردّد والموضع والطرفيّة.

    والمواصفةُ تُقرأ من الربط لا تُؤخَذ وسيطًا: عددُ إعادات التوزيع، والبذرة،
    ومستوى الرفض، وأدنى دعمٍ للحامل، كلُّها مُجمَّدةٌ قبل هذا التشغيل، فلا
    يُختار شيءٌ منها بعد رؤية الأرقام.
    """

    if type(table) is not ObservedFiberTable:
        raise CarrierFiberNullModelError("الاختبارُ يلزمه جدولَ وقوعاتٍ مقيسًا")
    if type(binding) is not CarrierFiberSpecificationContentBinding:
        raise CarrierFiberNullModelError(
            "لا يُشغَّل اختبارٌ إلا بربطٍ متحقَّقٍ بمواصفةٍ مُجمَّدةٍ قبل دليلها"
        )
    specification = binding.specification
    if table.schema != specification.state_schema:
        raise CarrierFiberNullModelError(
            "مخطَّطُ الحالة في الجدول يخالف المُجمَّد في المواصفة؛ وقياسٌ بمخطَّطٍ "
            "آخرَ قياسُ شيءٍ آخر"
        )

    carriers = [row.carrier for row in table.rows]
    strata = [row.stratum for row in table.rows]
    states: list[StateVector] = [row.state_vector for row in table.rows]
    frequency: dict[str, int] = {}
    for carrier in carriers:
        frequency[carrier] = frequency.get(carrier, 0) + 1

    pooled = _pooled_reference(strata, states)
    observed_assignment = list(zip(carriers, states))
    observed_support = _support_size(observed_assignment)
    observed_capacity = _capacity_by_carrier(observed_assignment)
    observed_divergence = _divergence_by_carrier(carriers, strata, states, pooled)
    observed_mean = _mean_divergence(observed_divergence, frequency)

    by_stratum: dict[tuple[int, str], list[int]] = {}
    for index, stratum in enumerate(strata):
        by_stratum.setdefault(stratum, []).append(index)

    generator = random.Random(specification.resampling_seed)
    capacity_at_or_below = {carrier: 0 for carrier in frequency}
    divergence_at_or_above = {carrier: 0 for carrier in frequency}
    support_at_or_below = 0
    mean_at_or_above = 0
    for _ in range(specification.resampling_count):
        permuted: list[StateVector] = list(states)
        for indices in by_stratum.values():
            pool = [states[index] for index in indices]
            generator.shuffle(pool)
            for index, state in zip(indices, pool):
                permuted[index] = state
        assignment = list(zip(carriers, permuted))
        if _support_size(assignment) <= observed_support:
            support_at_or_below += 1
        null_capacity = _capacity_by_carrier(assignment)
        for carrier, capacity in null_capacity.items():
            if capacity <= observed_capacity[carrier]:
                capacity_at_or_below[carrier] += 1
        null_divergence = _divergence_by_carrier(carriers, strata, permuted, pooled)
        for carrier, value in null_divergence.items():
            if value >= observed_divergence[carrier]:
                divergence_at_or_above[carrier] += 1
        if _mean_divergence(null_divergence, frequency) >= observed_mean:
            mean_at_or_above += 1

    rows: list[CarrierFiberReading] = []
    low_support: list[str] = []
    for carrier in table.carriers:
        support = frequency[carrier]
        under_powered = support < specification.minimum_carrier_support
        if under_powered:
            low_support.append(carrier)
        reading = CarrierFiberReading(
            carrier=carrier,
            frequency=support,
            observed_capacity=observed_capacity[carrier],
            null_capacity_at_or_below_observed=capacity_at_or_below[carrier],
            observed_composition_divergence_permille=_permille_floor(
                observed_divergence[carrier]
            ),
            null_composition_at_or_above_observed=divergence_at_or_above[carrier],
            resampling_count=specification.resampling_count,
            capacity_outcome=FiberOutcome.UNDETERMINED,
            composition_outcome=FiberOutcome.UNDETERMINED,
        )
        rows.append(
            _decide(reading, alpha_permille=specification.alpha_permille)
            if not under_powered
            else reading
        )

    return ConditionalIndependenceReadout(
        binding=binding,
        source_id=table.deposit.source_id,
        source_sha256=table.deposit.sha256,
        rows=tuple(rows),
        observed_support_size=observed_support,
        null_support_at_or_below_observed=support_at_or_below,
        observed_mean_divergence_permille=_permille_floor(observed_mean),
        null_mean_divergence_at_or_above_observed=mean_at_or_above,
        resampling_count=specification.resampling_count,
        carriers_below_support_threshold=tuple(low_support),
    )


def _decide(
    reading: CarrierFiberReading, *, alpha_permille: int
) -> CarrierFiberReading:
    capacity_outcome = (
        FiberOutcome.NARROWER_THAN_CHANCE
        if reading.capacity_p_value_permille <= alpha_permille
        else FiberOutcome.INDISTINGUISHABLE_FROM_CHANCE
    )
    composition_outcome = (
        FiberOutcome.NARROWER_THAN_CHANCE
        if reading.composition_p_value_permille <= alpha_permille
        else FiberOutcome.INDISTINGUISHABLE_FROM_CHANCE
    )
    return CarrierFiberReading(
        carrier=reading.carrier,
        frequency=reading.frequency,
        observed_capacity=reading.observed_capacity,
        null_capacity_at_or_below_observed=(reading.null_capacity_at_or_below_observed),
        observed_composition_divergence_permille=(
            reading.observed_composition_divergence_permille
        ),
        null_composition_at_or_above_observed=(
            reading.null_composition_at_or_above_observed
        ),
        resampling_count=reading.resampling_count,
        capacity_outcome=capacity_outcome,
        composition_outcome=composition_outcome,
    )


def run_null_model_on_the_deposited_fatiha() -> ConditionalIndependenceReadout:
    """شغِّل الاختبارَ كاملًا على النصّ المُودَع: تجميدٌ، فقياسٌ، فإعادةُ توزيع.

    ومدخلٌ عديمُ الوسائط عن قصد؛ وما يخرج منه معايرةٌ على نصٍّ قصيرٍ لا اختبارٌ
    حاسم، وهو مكتوبٌ في `A_CALIBRATION_RUN_IS_NOT_A_DECISIVE_RUN`.
    """

    binding = freeze_declared_specification()
    table = run_observed_fiber_on_the_deposited_fatiha()
    return assess_conditional_independence(table, binding=binding)


# --- ما لا يحسمه هذا الاختبار، مُسمًّى ----------------------------------------


NARROWER_THAN_CHANCE_IS_NOT_A_LICENSED_FIBER: Final[str] = (
    "NARROWER_THAN_CHANCE_IS_NOT_A_LICENSED_FIBER: ضيقٌ يبقى بعد ضبط التردّد "
    "والموضع والطرفيّة شاهدٌ على أنّ الحالةَ تعتمد على الحامل في هذه المدوّنة؛ "
    "وليس ترخيصًا لحالةٍ ولا منعًا لأخرى، ولا يُنشئ `S_licensed(c)`"
)

THREE_CONTROLS_ARE_NOT_ALL_CONTROLS: Final[str] = (
    "THREE_CONTROLS_ARE_NOT_ALL_CONTROLS: المضبوطُ هنا التردّدُ والموضعُ "
    "والطرفيّة؛ ودورُ الكلمة مؤجَّلٌ بتصريح، فما بقي من فرقٍ قد يفسّره مشاركٌ "
    "لم يُضبَط بعد"
)

A_PERMUTATION_NULL_IS_NOT_A_GENERATIVE_MODEL: Final[str] = (
    "A_PERMUTATION_NULL_IS_NOT_A_GENERATIVE_MODEL: إعادةُ التوزيع تُعيد خلطَ "
    "الحالات المرصودة داخلَ طبقاتها؛ فهي مرجعٌ صفريٌّ مشتقٌّ من المدوّنة نفسِها، "
    "لا نموذجٌ يولّد العربيةَ ولا يدّعي وصفَها"
)

LOW_SUPPORT_IS_UNDETERMINED_NOT_SUPPORT: Final[str] = (
    "LOW_SUPPORT_IS_UNDETERMINED_NOT_SUPPORT: حاملٌ دعمُه دون الحدّ المُجمَّد "
    "يُقرأ `UNDETERMINED`؛ وقراءةُ قلّةِ الدليل تأييدًا أو تفنيدًا هي عينُ ما "
    "تمنعه المفردةُ الثلاثية"
)

NO_MEASURE_COLLAPSE: Final[str] = (
    "NO_MEASURE_COLLAPSE: السعةُ والتركيبُ حقلان اثنان في كلّ صفّ، ولا يُجمَعان "
    "في حكمٍ واحدٍ ولا يُشتَقّ أحدُهما من الآخر؛ والرفضُ عند الاستيراد لا "
    "تصحيحٌ عند القراءة"
)

SEEDED_DETERMINISM_IS_INTERPRETER_RELATIVE: Final[str] = (
    "SEEDED_DETERMINISM_IS_INTERPRETER_RELATIVE: البذرةُ مُجمَّدةٌ في المواصفة "
    "فيُعاد التشغيلُ بالأرقام نفسِها على المفسِّر نفسِه؛ وثباتُها عبر مفسِّراتٍ "
    "أُخَر دعوى لم تُقَس هنا"
)

CARRIER_FIBER_NULL_MODEL_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "NARROWER_THAN_CHANCE_IS_NOT_A_LICENSED_FIBER": (
        NARROWER_THAN_CHANCE_IS_NOT_A_LICENSED_FIBER
    ),
    "THREE_CONTROLS_ARE_NOT_ALL_CONTROLS": THREE_CONTROLS_ARE_NOT_ALL_CONTROLS,
    "A_PERMUTATION_NULL_IS_NOT_A_GENERATIVE_MODEL": (
        A_PERMUTATION_NULL_IS_NOT_A_GENERATIVE_MODEL
    ),
    "LOW_SUPPORT_IS_UNDETERMINED_NOT_SUPPORT": LOW_SUPPORT_IS_UNDETERMINED_NOT_SUPPORT,
    "NO_MEASURE_COLLAPSE": NO_MEASURE_COLLAPSE,
    "SEEDED_DETERMINISM_IS_INTERPRETER_RELATIVE": (
        SEEDED_DETERMINISM_IS_INTERPRETER_RELATIVE
    ),
}
"""ما لا يحسمه هذا الاختبار، مُسمًّى هنا لا متروكًا ليُفترَض."""
