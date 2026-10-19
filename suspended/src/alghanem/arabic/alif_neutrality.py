"""«حيادُ الألف» رياضيًّا لا صوتيًّا: ما انعقد منه بالقياس، وما انتقض.

الدعوى المعروضة ثلاثُ دعاوى متمايزةِ الحكم، تُقرأ كلُّ واحدةٍ على حدةٍ من
الإيداع المُبصَّم وحدَه:

1. **الألفُ لا تُشارك في الليف: تقبل تركيبًا واحدًا** — منعقدةٌ قياسًا، وبفصلٍ
   حاسمٍ عن الشُّح. فسَعةُ الألف واحدةٌ في ثلاثٍ وعشرين وقعة، بينما سائرُ ما
   سَعتُه واحدةٌ نادرُ الوقوع، وثباتُه يُفسَّر بقلّة العيّنة لا بخاصّيّة.
   والفصلُ يُقاس لا يُدَّعى: `constancy_exponent` يحسب احتمالَ ثباتٍ كهذا لو
   سُحبت حالاتُ الحامل من توزيع سائر الحوامل.

2. **ثباتُها على العنصر المحايد** — منعقدةٌ، وهي أقوى من المعروض: الألفُ لا
   تقبل تركيبًا واحدًا فحسب، بل تقبل **التركيبَ الصفريَّ** وحدَه — مُتَّجِهًا
   كلُّ محاورِه غائبة، وهو محايدُ الضرب في المحاور الأربعة. وهي الحاملُ الوحيدُ
   الذي ليفُه كلُّه هذا المحايد. فقولُ «عنصرٌ محايدٌ للعملية لا عنصرٌ في C»
   قراءةٌ يحتملها المقيس، لكنّها **قرارُ نمذجةٍ لا نتيجةَ قياس**
   (`NeutralityIsMeasuredButExclusionFromCIsChosen`).

3. **«إدخالُها كسر حاصلَ الضرب، وإخراجُها أعاده»** — **منتقضة**. فلا حاصلَ ضربٍ
   ينكسر ولا يعود: المستطيلُ ممتلئٌ ٥٤ من ١٦١ بالألف، و٥٣ من ١٥٤ بدونها،
   والسَّعاتُ تبقى مُضرَّسةً من واحدٍ إلى ستٍّ في الحالين. فإخراجُ الألف يُنقِص
   خانةً ولا يُعيد بناءً (`RemovingAlifRestoresNoRectangle`).

**والمانعُ الأكبرُ مُسمًّى**: محورُ المدّ مُجمَّدٌ على
`DEFERRED_NOT_READ_AS_A_STATE`، والألفُ أَولى الحوامل بحملِه. فقد يكون حيادُها
أثرًا لتأجيلِ المحورِ الذي عليه وحدَها تتغيّر، لا خاصّيّةً فيها
(`AlifsNeutralityMayBeAnArtifactOfTheDeferredMaddAxis`). وهذا مانعٌ قائمٌ لا
يرفعه عددٌ من هذا الإيداع.

وهذا كلُّه في **الرسم** لا في الصوت، وفاقًا لتقييد العارض؛ و
`UnicodeIsNotRecordedSound` قائمٌ على كلّ حال. ولا ولادةَ ههنا ولا حكمَ ولادةٍ
كرنليًّا، ولا تُستورَد `kernel/` من هذه الوحدة.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from typing import Final

from .carrier_state_observed_fiber import (
    ABSENT,
    ObservedFiberTable,
    OccurrenceRow,
    capacity_by_carrier,
    run_observed_fiber_on_the_deposited_fatiha,
)

__all__ = [
    "ALIF",
    "ALIF_NEUTRALITY_NAMED_RESIDUALS",
    "ALIF_NEUTRALITY_MAY_BE_AN_ARTIFACT_NOTE",
    "NEUTRALITY_IS_MEASURED_BUT_EXCLUSION_IS_CHOSEN_NOTE",
    "REMOVING_ALIF_RESTORES_NO_RECTANGLE_NOTE",
    "SCARCITY_EXPLAINS_A_SMALL_FIBER_NOTE",
    "THE_CLAIM",
    "AlifClaimReading",
    "AlifNeutralityError",
    "AlifVerdict",
    "CarrierConstancy",
    "NeutralityReading",
    "RectangleFill",
    "identity_state",
    "measure_constancies",
    "measure_rectangle_fill",
    "read_the_alif_claim",
]


class AlifNeutralityError(ValueError):
    """رفضٌ صريح: قياسٌ بلا مقام، أو حكمٌ بلا سببٍ مكتوب."""


ALIF: Final[str] = "\u0627"

THE_CLAIM: Final[str] = (
    "الألفُ لا تُشارك في الليف: تقبل تركيبًا واحدًا؛ فهي عنصرٌ محايدٌ للعملية "
    "لا عنصرٌ في C، وإدخالُها كسر حاصلَ الضرب وإخراجُها أعاده"
)

_SIGNIFICANCE_CEILING: Final[Fraction] = Fraction(1, 1000)


class AlifClaimReading(Enum):
    """قراءاتُ دعوى الحياد، متمايزةَ الحكم."""

    ALIF_ACCEPTS_ONE_COMBINATION = "الألفُ تقبل تركيبًا واحدًا"
    THAT_COMBINATION_IS_THE_IDENTITY = "وذلك التركيبُ هو المحايد"
    ALIF_IS_NOT_AN_ELEMENT_OF_C = "الألفُ ليست عنصرًا في C"
    REMOVING_ALIF_RESTORES_THE_PRODUCT = "إخراجُ الألف يُعيد حاصلَ الضرب"


class AlifVerdict(Enum):
    """حكمُ القراءة؛ والمقيسُ غيرُ المختار، والمنتقضُ غيرُ المتعذّر."""

    HELD_BY_MEASUREMENT = "منعقدةٌ_قياسًا"
    ADMISSIBLE_BUT_CHOSEN = "محتمَلةٌ_قرارًا_لا_قياسًا"
    REFUTED = "منتقضة"


@dataclass(frozen=True)
class NeutralityReading:
    """حكمُ قراءةٍ واحدة، ومعه ما قرّره وما بقي عليه."""

    reading: AlifClaimReading
    verdict: AlifVerdict
    what_decided_it: str
    residuals: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.what_decided_it.strip():
            raise AlifNeutralityError("حكمٌ بلا سببٍ مكتوب")
        if not self.residuals:
            raise AlifNeutralityError(
                f"«{self.reading.value}» بلا بقيّةٍ مُسمّاة؛ والخلوُّ ليس إعفاءً"
            )
        if any(not note.strip() for note in self.residuals):
            raise AlifNeutralityError("في البقايا مدخلٌ فارغ")


# --- المحايدُ مقروءًا من المحاور لا مفروضًا عليها ----------------------------------


def identity_state(table: ObservedFiberTable) -> tuple[str, ...]:
    """المُتَّجِهُ المحايد: غيابٌ في كلّ محورٍ مقيس، مقروءًا من عدد المحاور."""

    if not table.rows:
        raise AlifNeutralityError("جدولٌ بلا وقعات؛ ولا يُقاس على خلاء")
    width = len(table.rows[0].state_vector)
    if width < 1:
        raise AlifNeutralityError("متَّجِهُ حالةٍ بلا محاور")
    return (ABSENT,) * width


def _state_of(row: OccurrenceRow) -> tuple[str, ...]:
    return tuple(value for _axis, value in row.state_vector)


# --- الثباتُ مقيسًا ضدّ الشُّح ------------------------------------------------------


@dataclass(frozen=True)
class CarrierConstancy:
    """ثباتُ حاملٍ على حالةٍ واحدة، ومعه ما يفصله عن كونه أثرَ قلّةِ عيّنة."""

    carrier: str
    occurrences: int
    capacity: int
    sole_state: tuple[str, ...] | None
    background_share: Fraction
    constancy_exponent: Fraction

    def __post_init__(self) -> None:
        if self.occurrences < 1:
            raise AlifNeutralityError("حاملٌ بلا وقعةٍ لا يُحصى")
        if self.capacity < 1:
            raise AlifNeutralityError("سَعةٌ دون الواحد")
        if (self.capacity == 1) != (self.sole_state is not None):
            raise AlifNeutralityError("الحالةُ الوحيدةُ تُذكَر عند السَّعةِ الواحدة وحدَها")

    @property
    def is_constant(self) -> bool:
        """أثبت الحاملُ على حالةٍ واحدة؟ مُشتَقٌّ لا مُخزَّن."""

        return self.capacity == 1

    @property
    def survives_the_scarcity_control(self) -> bool:
        """أثباتٌ لا يُفسَّر بقلّة العيّنة عند السقف المُعلَن؟"""

        return self.is_constant and self.constancy_exponent < _SIGNIFICANCE_CEILING


def measure_constancies(
    table: ObservedFiberTable | None = None,
) -> tuple[CarrierConstancy, ...]:
    """قِس ثباتَ كلِّ حامل، واضبطه بتوزيع سائر الحوامل لا بتوزيعه هو."""

    measured = run_observed_fiber_on_the_deposited_fatiha() if table is None else table
    capacities = capacity_by_carrier(measured)

    readings: list[CarrierConstancy] = []
    for carrier in sorted(capacities):
        mine = [row for row in measured.rows if row.carrier == carrier]
        others = [row for row in measured.rows if row.carrier != carrier]
        capacity = capacities[carrier]

        if capacity != 1:
            readings.append(
                CarrierConstancy(
                    carrier=carrier,
                    occurrences=len(mine),
                    capacity=capacity,
                    sole_state=None,
                    background_share=Fraction(0),
                    constancy_exponent=Fraction(1),
                )
            )
            continue

        sole = _state_of(mine[0])
        if not others:
            raise AlifNeutralityError(
                "لا خلفيّةَ يُضبَط بها الثبات؛ والضبطُ بالنفس ليس ضبطًا"
            )
        share = Fraction(
            sum(1 for row in others if _state_of(row) == sole), len(others)
        )
        readings.append(
            CarrierConstancy(
                carrier=carrier,
                occurrences=len(mine),
                capacity=1,
                sole_state=sole,
                background_share=share,
                constancy_exponent=share ** len(mine),
            )
        )
    return tuple(readings)


# --- المستطيلُ ممتلئًا، بالألف وبدونها ---------------------------------------------


@dataclass(frozen=True)
class RectangleFill:
    """امتلاءُ مستطيلِ (حامل × حالة)، وسَعاتُه مُضرَّسةً أو مستويةً."""

    carriers: int
    states: int
    realized_pairs: int
    capacity_spread: tuple[int, ...]

    def __post_init__(self) -> None:
        if self.realized_pairs > self.carriers * self.states:
            raise AlifNeutralityError("المُحقَّقُ أكثرُ من المستطيل؛ ومقامٌ كهذا مُحال")

    @property
    def rectangle(self) -> int:
        """مساحةُ المستطيل لو كان حاصلَ ضربٍ تامًّا."""

        return self.carriers * self.states

    @property
    def is_a_full_product(self) -> bool:
        """أهو حاصلُ ضربٍ فعلًا؟ لا يكون إلّا باستواء السَّعات وامتلاء المستطيل."""

        return self.realized_pairs == self.rectangle


def measure_rectangle_fill(
    table: ObservedFiberTable | None = None, *, excluding: str | None = None
) -> RectangleFill:
    """قِس امتلاءَ المستطيل، مع إخراجِ حاملٍ مُسمًّى أو بدونه."""

    measured = run_observed_fiber_on_the_deposited_fatiha() if table is None else table
    rows = [row for row in measured.rows if row.carrier != excluding]
    if not rows:
        raise AlifNeutralityError("لا وقعاتِ بعد الإخراج؛ ولا يُقاس على خلاء")

    carriers = sorted({row.carrier for row in rows})
    states = sorted({_state_of(row) for row in rows})
    spread = tuple(
        sorted(
            len({_state_of(row) for row in rows if row.carrier == carrier})
            for carrier in carriers
        )
    )
    return RectangleFill(
        carriers=len(carriers),
        states=len(states),
        realized_pairs=len({(row.carrier, _state_of(row)) for row in rows}),
        capacity_spread=spread,
    )


# --- قراءةُ الدعوى ----------------------------------------------------------------


def read_the_alif_claim(
    table: ObservedFiberTable | None = None,
) -> tuple[NeutralityReading, ...]:
    """اقرأ دعوى حيادِ الألف قراءاتِها، ولكلِّ قراءةٍ حكمٌ وسببٌ وبقيّة."""

    measured = run_observed_fiber_on_the_deposited_fatiha() if table is None else table
    constancies = measure_constancies(measured)
    identity = identity_state(measured)

    alif = next((item for item in constancies if item.carrier == ALIF), None)
    if alif is None:
        raise AlifNeutralityError(
            "لا ألفَ في الإيداع؛ ولا تُقرأ دعوى حيادِها على غير موردها"
        )
    if not alif.is_constant:
        raise AlifNeutralityError(
            "الألفُ ليست ثابتةً في هذا الإيداع؛ والدعوى تنتقض من أصلها " "فتُرفَع ولا تُطوى"
        )

    rivals = tuple(
        item
        for item in constancies
        if item.carrier != ALIF and item.survives_the_scarcity_control
    )
    at_identity = tuple(
        item for item in constancies if item.is_constant and item.sole_state == identity
    )
    with_alif = measure_rectangle_fill(measured)
    without_alif = measure_rectangle_fill(measured, excluding=ALIF)

    rival_note = (
        "ولم ينجُ من ضبط الشُّح سواها"
        if not rivals
        else "وعلى حافّة السقف "
        + "، ".join(f"«{item.carrier}»" for item in rivals)
        + " ولا يفصلها هذا الإيداعُ فصلًا"
    )

    return (
        NeutralityReading(
            reading=AlifClaimReading.ALIF_ACCEPTS_ONE_COMBINATION,
            verdict=AlifVerdict.HELD_BY_MEASUREMENT,
            what_decided_it=(
                f"سَعةُ الألف واحدةٌ في {alif.occurrences} وقعة، واحتمالُ ثباتٍ "
                f"كهذا من توزيع سائر الحوامل {float(alif.constancy_exponent):.2e}؛ "
                f"{rival_note}"
            ),
            residuals=(
                "SCARCITY_EXPLAINS_A_SMALL_FIBER: سائرُ ما سَعتُه واحدةٌ نادرُ "
                "الوقوع، فثباتُه أثرُ قلّةِ عيّنةٍ لا خاصّيّة؛ والألفُ وحدَها "
                "ثبتت على كثرة",
                "الثباتُ في هذا الإيداع لا يمنع تركيبًا آخرَ في غيره؛ والخلوُّ "
                "من وقوعٍ ليس نفيًا لإمكانه",
            ),
        ),
        NeutralityReading(
            reading=AlifClaimReading.THAT_COMBINATION_IS_THE_IDENTITY,
            verdict=AlifVerdict.HELD_BY_MEASUREMENT,
            what_decided_it=(
                "التركيبُ الذي تثبت عليه الألفُ هو المحايدُ نفسُه — غيابٌ في "
                f"المحاور الـ{len(identity)} كلِّها — وعددُ الحوامل الثابتة على "
                f"المحايد {len(at_identity)}، فهي واحدتُها"
            ),
            residuals=(
                "ALIF_NEUTRALITY_MAY_BE_AN_ARTIFACT: محورُ المدّ مُجمَّدٌ "
                "مؤجَّلًا لا يُقرأ حالةً، والألفُ أَولى الحوامل بحملِه؛ فقد "
                "يكون حيادُها أثرَ تأجيلِ المحورِ الذي عليه وحدَها تتغيّر",
                "الحيادُ ههنا في الرسم لا في الصوت، وفاقًا لتقييد الدعوى؛ "
                "و`UnicodeIsNotRecordedSound` قائمٌ على كلّ حال",
            ),
        ),
        NeutralityReading(
            reading=AlifClaimReading.ALIF_IS_NOT_AN_ELEMENT_OF_C,
            verdict=AlifVerdict.ADMISSIBLE_BUT_CHOSEN,
            what_decided_it=(
                "المقيسُ يحتمل القراءتين سواءً: حاملٌ ليفُه المحايدُ وحدَه، أو "
                "محايدٌ للعملية خارجَ C. ولا يفصل بينهما عددٌ من هذا الإيداع، "
                "فالإخراجُ من C قرارُ نمذجةٍ يُعلَن ولا يُنسَب إلى القياس"
            ),
            residuals=(
                "NEUTRALITY_IS_MEASURED_BUT_EXCLUSION_FROM_C_IS_CHOSEN: الحيادُ "
                "مقيس، والإخراجُ مختار؛ وخلطُهما ينسب إلى الرصد ما قرّره النموذج",
                "ولو أُخرجت الألفُ من C لوجب أن يُسمّى أثرُ إخراجها في كلّ قراءةٍ "
                "تعتمد عدّ الحوامل، ولا يُطوى",
            ),
        ),
        NeutralityReading(
            reading=AlifClaimReading.REMOVING_ALIF_RESTORES_THE_PRODUCT,
            verdict=AlifVerdict.REFUTED,
            what_decided_it=(
                f"لا حاصلَ ضربٍ ينكسر ولا يعود: المستطيلُ ممتلئٌ "
                f"{with_alif.realized_pairs} من {with_alif.rectangle} بالألف، و"
                f"{without_alif.realized_pairs} من {without_alif.rectangle} "
                f"بدونها، والسَّعاتُ تبقى مُضرَّسةً من "
                f"{min(without_alif.capacity_spread)} إلى "
                f"{max(without_alif.capacity_spread)} بعد الإخراج"
            ),
            residuals=(
                "REMOVING_ALIF_RESTORES_NO_RECTANGLE: إخراجُ الألف يُنقِص خانةً "
                "ولا يُعيد بناءً؛ وانكسارُ الضرب سابقٌ عليها وباقٍ بعدها",
                "ولا يُقرأ هذا نفيًا لبنيةِ ضربٍ في العربيّة، بل نفيًا لوجودها "
                "في هذا الإيداع بهذه المحاور",
            ),
        ),
    )


# --- الحدودُ مُسمّاةً -------------------------------------------------------------


SCARCITY_EXPLAINS_A_SMALL_FIBER_NOTE: Final[str] = (
    "ScarcityExplainsASmallFiber: سَعةٌ واحدةٌ في وقعةٍ أو وقعتين ليست حيادًا؛ "
    "وثمانيةُ حواملَ سَعتُها واحدةٌ في هذا الإيداع، ولا ينجو من ضبط الشُّح "
    "منها إلّا الألف"
)

ALIF_NEUTRALITY_MAY_BE_AN_ARTIFACT_NOTE: Final[str] = (
    "AlifsNeutralityMayBeAnArtifactOfTheDeferredMaddAxis: محورُ المدّ مُجمَّدٌ "
    "على أنّه لا يُقرأ حالةً، والألفُ أَولى الحوامل بحملِه؛ فقد يكون حيادُها "
    "أثرَ تأجيلِ المحورِ الذي عليه وحدَها تتغيّر، ولا يرفع هذا المانعَ عددٌ "
    "من هذا الإيداع"
)

NEUTRALITY_IS_MEASURED_BUT_EXCLUSION_IS_CHOSEN_NOTE: Final[str] = (
    "NeutralityIsMeasuredButExclusionFromCIsChosen: ثباتُ الألف على المحايد "
    "مقيس، وإخراجُها من C قرارُ نمذجةٍ لا نتيجةَ قياس؛ وخلطُهما ينسب إلى "
    "الرصد ما قرّره النموذج"
)

REMOVING_ALIF_RESTORES_NO_RECTANGLE_NOTE: Final[str] = (
    "RemovingAlifRestoresNoRectangle: المستطيلُ مُضرَّسُ السَّعات قبل إخراج "
    "الألف وبعده؛ فإخراجُها يُنقِص خانةً ولا يُعيد حاصلَ ضرب، والدعوى "
    "بإعادته منتقضة"
)

A_NEUTRALITY_HERE_IS_A_NEUTRALITY_IN_WRITING_NOTE: Final[str] = (
    "ANeutralityHereIsANeutralityInWriting: ما قيس رسمُ ناسخٍ واحدٍ لنصٍّ واحد "
    "بأربعة محاورَ مُعلَنة؛ فلا يُقرأ حكمًا على الألف في العربيّة ولا في النطق، "
    "ولا ولادةَ ههنا ولا حكمَ ولادة"
)

ALIF_NEUTRALITY_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    SCARCITY_EXPLAINS_A_SMALL_FIBER_NOTE,
    ALIF_NEUTRALITY_MAY_BE_AN_ARTIFACT_NOTE,
    NEUTRALITY_IS_MEASURED_BUT_EXCLUSION_IS_CHOSEN_NOTE,
    REMOVING_ALIF_RESTORES_NO_RECTANGLE_NOTE,
    A_NEUTRALITY_HERE_IS_A_NEUTRALITY_IN_WRITING_NOTE,
)
