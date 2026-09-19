"""مبرهنةُ التفكيك وإعادة البناء، ومفردتان مُسمّاتان لا تُستبدَل إحداهما بالأخرى.

**المخرجُ الجبريُّ الأوّلُ القابلُ للإغلاق ليس ولادةَ CV**، بل أن يُبرهَن أنّ
التفكيكَ إلى عناصرَ مصنَّفةٍ **عكوسٌ تامّ**: إن رددتَ ما فكّكتَه عاد السطحُ
حرفًا حرفًا. وهذه مبرهنةٌ تُغلَق ههنا بحدودها، ولا تُستعار منها ولادة.

**ومفردتان تُسمَّيان ولا تُخلَطان**:

* `OBSERVED_POPULATION`: ما وقع فعلًا في الإيداع المبصوم — حواملُه معدودةٌ
  بالوقوع، وسعاتُه مقيسةٌ لا مُعلَنة.
* `DECLARED_POPULATION`: ما تُجيزه المفردةُ المُعلَنة في المِرماز — حواملُها
  مكتوبةٌ في الشجرة لا مُستخرَجةٌ من نصّ، وجداءُ حواملها بحالاتها **حدٌّ أعلى**
  لا إحصاءُ مواضع.

وبينهما `PopulationSubstitutionError`: كلُّ دالّةٍ ههنا تطلب مفردتَها بالاسم،
وترفض أن يُمرَّر رقمُ إحداهما في موضع الأخرى. فالسعةُ المقيسةُ لا تُسند إلى
المُعلَن، والحدُّ الأعلى المُعلَن لا يُقدَّم شاهدًا على ما وقع
(`A_MEASURED_CAPACITY_IS_NOT_A_DECLARED_UPPER_BOUND`).

**والبقيّةُ حاملةٌ للوزن**: العناصرُ المصنَّفة وحدَها **لا تكفي** لإعادة البناء.
فهي لا تحمل نوعَ السكون (أمكتوبٌ أم مقدَّر)، ولا المقعدَ، ولا التنوين، ولا
الحالاتِ البنيويّةَ المحضة. فالتفكيكُ يُخرِج `(عناصر، بقيّة)` معًا، وإعادةُ
البناء تلزمهما. وقد قيس أنّ إسقاطَ البقيّة **يكسر** البناء، فليست البقيّةُ
زينةً تُحتمَل (`THE_RESIDUE_IS_LOAD_BEARING_NOT_DECORATIVE`).

**ولا `RefineSlot` ههنا**: إضافةُ عمليّةِ تنقيحٍ إلى الجبر تلزمها برهانُ
**ضرورتها لوظيفةٍ مستقلّة**، ولم يُقَم. ونسبةُ نجاحٍ في مدوّنةٍ ليست برهانَ
ضرورة (`REFINEMENT_NECESSITY_IS_UNPROVEN_SO_REFINE_SLOT_IS_UNLICENSED`).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from .encoding.carrier_state_candidate import (
    DECLARED_CARRIERS,
    CarrierSeat,
    CarrierState,
    CarrierStateCodec,
    CarrierStateUnit,
    GeminationRole,
)
from .fatiha_source_text import FATIHA_LINES, FATIHA_SOURCE_ID
from .letter_haraka_operational_algebra import (
    JoinInputStatus,
    LicensedJoinInput,
    decompose_word,
)

__all__ = [
    "A_MEASURED_CAPACITY_IS_NOT_A_DECLARED_UPPER_BOUND_NOTE",
    "DECOMPOSITION_THEOREM_NAMED_RESIDUALS",
    "REFINEMENT_NECESSITY_IS_UNPROVEN_NOTE",
    "THE_RESIDUE_IS_LOAD_BEARING_NOT_DECORATIVE_NOTE",
    "THE_THEOREM_CLOSES_ON_A_NAMED_POPULATION_ONLY_NOTE",
    "THIS_IS_NOT_A_CV_BIRTH_THEOREM_NOTE",
    "INSTRUMENT_DIVERGENCES",
    "THE_SAME_DEPOSIT_MEASURED_TWICE_GIVES_TWO_LEGITIMATE_NUMBERS_NOTE",
    "DeclaredPopulationCensus",
    "InstrumentDivergence",
    "MeasurementInstrument",
    "ObservedPopulationCensus",
    "Population",
    "PopulationSubstitutionError",
    "ReconstructionReport",
    "ResidueField",
    "UnitResidue",
    "WordDecomposition",
    "census_of_declared_population",
    "census_of_observed_population",
    "decompose_with_residue",
    "prove_decomposition_reconstructs",
    "prove_the_residue_is_necessary",
    "reconstruct",
]


class PopulationSubstitutionError(ValueError):
    """رفضُ إسنادِ رقمِ مفردةٍ إلى مفردةٍ أخرى؛ الخلطُ ههنا خطأٌ لا تقريب."""


class Population(Enum):
    """مفردتان مُسمَّاتان: ما وقع، وما يُجيزه المُعلَن. ولا ثالثَ ولا خلط."""

    OBSERVED = "المرصودة_في_الإيداع"
    DECLARED = "المُعلَنة_في_المِرماز"


class MeasurementInstrument(Enum):
    """آلتا قياسٍ على الإيداع نفسِه، تختلف أرقامُهما اختلافًا مشروعًا.

    ولا يُقال «عددُ الحوامل» مطلقًا: يُقال بأيّ آلةٍ عُدَّ.
    """

    CODEC_UNIT = "وحدة_المِرماز"
    OBSERVED_FIBER = "الليف_المرصود"


@dataclass(frozen=True)
class InstrumentDivergence:
    """فارقٌ بين آلتين على إيداعٍ واحد، يُسمّى ولا يُسوّى ولا يُرجَّح."""

    quantity: str
    codec_value: int
    fiber_value: int
    why_they_differ: str

    def __post_init__(self) -> None:
        if not self.why_they_differ.strip():
            raise PopulationSubstitutionError(
                "فارقٌ بلا علّةٍ مكتوبة يُغري بالتسوية؛ والعلّةُ شرطُ تسجيله"
            )
        if self.codec_value == self.fiber_value:
            raise PopulationSubstitutionError(
                "لا فارقَ ههنا؛ ولا يُسجَّل اتّفاقٌ في جدول فوارق"
            )


INSTRUMENT_DIVERGENCES: Final[tuple[InstrumentDivergence, ...]] = (
    InstrumentDivergence(
        quantity="عددُ الحوامل المتمايزة",
        codec_value=22,
        fiber_value=23,
        why_they_differ=(
            "المِرمازُ يردّ «أ» و«إ» إلى همزةٍ واحدةٍ ويسجّل المقعدَ حقلًا، "
            "فيراهما حاملًا واحدًا؛ والليفُ يبقيهما كما كُتبا فيراهما حاملَين"
        ),
    ),
    InstrumentDivergence(
        quantity="عددُ المواضع",
        codec_value=159,
        fiber_value=143,
        why_they_differ=(
            "المِرمازُ يولّد موضعًا لكلّ حاملٍ مكتوب، والليفُ يقيس وقوعاتٍ "
            "بتعريفٍ آخر؛ فالعددان عن آلتين لا عن نصّين"
        ),
    ),
    InstrumentDivergence(
        quantity="أقصى سعةٍ لحامل",
        codec_value=4,
        fiber_value=6,
        why_they_differ=(
            "المِرمازُ يعدّ قيمَ `CarrierState` المتمايزة، والليفُ يعدّ متّجهاتِ "
            "حالةٍ متعدّدةَ المحاور؛ فسعةُ ستٍّ في أحدهما ليست سعةَ ستٍّ في الآخر"
        ),
    ),
)
"""فوارقُ مقيسةٌ بين الآلتين، مكتوبةٌ لتُقابَل بها أيُّ إحالةٍ مرسَلة."""


@dataclass(frozen=True)
class ObservedPopulationCensus:
    """إحصاءُ ما وقع: محسوبٌ من الإيداع، ولا يُقرأ حدًّا أعلى لشيء."""

    population: Population
    source_id: str
    word_count: int
    unit_count: int
    distinct_carriers: int
    observed_capacities: tuple[int, ...]
    instrument: MeasurementInstrument = MeasurementInstrument.CODEC_UNIT

    def __post_init__(self) -> None:
        if self.population is not Population.OBSERVED:
            raise PopulationSubstitutionError(
                "إحصاءُ الوقوع لا يُوسَم بغير المفردة المرصودة"
            )
        if self.distinct_carriers > len(DECLARED_CARRIERS):
            raise PopulationSubstitutionError(
                "حواملُ الوقوع لا تتجاوز المُعلَنة؛ ورقمٌ أكبرُ دليلُ خلط"
            )

    @property
    def capacity_range_is_contiguous(self) -> bool:
        """أمتّصلٌ مدى السعات المقيسة؟ سؤالٌ يُجاب بالعدّ لا بالوصف.

        فقولُ «من واحدٍ إلى ستّة» يُوهِم اتّصالًا، وقد يكون في المدى ثقبٌ.
        """

        if not self.observed_capacities:
            return False
        low, high = self.observed_capacities[0], self.observed_capacities[-1]
        return tuple(range(low, high + 1)) == self.observed_capacities


@dataclass(frozen=True)
class DeclaredPopulationCensus:
    """إحصاءُ المُعلَن: جداءٌ هو حدٌّ أعلى، ولا يُقدَّم إحصاءَ مواضعَ واقعة."""

    population: Population
    carrier_count: int
    state_count: int

    def __post_init__(self) -> None:
        if self.population is not Population.DECLARED:
            raise PopulationSubstitutionError(
                "إحصاءُ المُعلَن لا يُوسَم بغير المفردة المُعلَنة"
            )

    @property
    def upper_bound(self) -> int:
        """جداءُ المفردتين: سقفٌ لا يقع تحته كلُّ ما عُدّ، ولا يُقرأ عددَ وقوع."""

        return self.carrier_count * self.state_count


def census_of_observed_population(
    lines: tuple[str, ...] | None = None, *, source_id: str | None = None
) -> ObservedPopulationCensus:
    """عُدَّ ما وقع فعلًا؛ ولا يُستعان في هذا العدّ بأيّ رقمٍ مُعلَن."""

    text = FATIHA_LINES if lines is None else lines
    identifier = FATIHA_SOURCE_ID if source_id is None else source_id
    codec = CarrierStateCodec()

    states_by_carrier: dict[str, set[CarrierState]] = {}
    words = 0
    units = 0
    for line in text:
        for word in line.split():
            words += 1
            for unit in codec.generate(word):
                units += 1
                states_by_carrier.setdefault(unit.carrier, set()).add(unit.state)

    capacities = tuple(sorted({len(states) for states in states_by_carrier.values()}))
    return ObservedPopulationCensus(
        population=Population.OBSERVED,
        source_id=identifier,
        word_count=words,
        unit_count=units,
        distinct_carriers=len(states_by_carrier),
        observed_capacities=capacities,
    )


def census_of_declared_population() -> DeclaredPopulationCensus:
    """عُدَّ المفردةَ المُعلَنة كما كُتبت في الشجرة؛ ولا تُستخرَج من نصّ."""

    return DeclaredPopulationCensus(
        population=Population.DECLARED,
        carrier_count=len(DECLARED_CARRIERS),
        state_count=len(CarrierState),
    )


# --- البقيّة -----------------------------------------------------------------------


class ResidueField(Enum):
    """حقولُ البنية التي لا تحملها العناصرُ المصنَّفة، فتُحمَل بقيّةً مُسمّاة."""

    SUKUN_KIND = "نوع_السكون"
    SEAT = "المقعد"
    TANWIN = "التنوين"
    TANWIN_ALIF_SEAT = "مقعد_ألف_التنوين"
    SILENT = "الصامت_غير_المنطوق"
    WAW_MADDA = "واو_المدّة"
    STRUCTURAL_STATE = "حالة_بنيويّة_محضة"


@dataclass(frozen=True)
class UnitResidue:
    """ما فضل عن موضعٍ بعد انتزاع عنصرَيه المصنَّفين؛ محفوظٌ لا مطروح."""

    unit_index: int
    state: CarrierState
    seat: CarrierSeat | None
    tanwin: bool
    tanwin_alif_seat: bool
    silent: bool
    waw_madda: bool
    gemination: GeminationRole | None

    @property
    def carried_fields(self) -> tuple[ResidueField, ...]:
        """سمِّ ما تحمله هذه البقيّةُ فعلًا؛ عدٌّ مُشتَقٌّ لا وصفٌ مكتوب."""

        fields: list[ResidueField] = []
        if self.state.is_structural_only:
            fields.append(ResidueField.STRUCTURAL_STATE)
        if self.state in (CarrierState.SUKUN_EXPLICIT, CarrierState.SUKUN_IMPLICIT):
            fields.append(ResidueField.SUKUN_KIND)
        if self.seat is not None:
            fields.append(ResidueField.SEAT)
        if self.tanwin:
            fields.append(ResidueField.TANWIN)
        if self.tanwin_alif_seat:
            fields.append(ResidueField.TANWIN_ALIF_SEAT)
        if self.silent:
            fields.append(ResidueField.SILENT)
        if self.waw_madda:
            fields.append(ResidueField.WAW_MADDA)
        return tuple(fields)


@dataclass(frozen=True)
class WordDecomposition:
    """كلمةٌ مفكَّكةٌ إلى `(عناصرَ مصنَّفة، بقيّةٍ مُسمّاة)`؛ وكلاهما لازم."""

    surface: str
    population: Population
    elements: tuple[LicensedJoinInput, ...]
    residue: tuple[UnitResidue, ...]

    def __post_init__(self) -> None:
        if self.population is not Population.OBSERVED:
            raise PopulationSubstitutionError(
                "التفكيكُ يجري على ما وقع؛ ولا يُفكَّك حدٌّ أعلى مُعلَن"
            )
        if len(self.elements) != len(self.residue):
            raise PopulationSubstitutionError(
                "لكلّ موضعٍ عنصرُه وبقيّتُه؛ واختلافُ العدد دليلُ فقدٍ صامت"
            )

    @property
    def residue_bearing_units(self) -> tuple[UnitResidue, ...]:
        """المواضعُ التي فضلت عنها بنيةٌ فعلًا؛ لا كلُّ موضعٍ يفضل عنه شيء."""

        return tuple(item for item in self.residue if item.carried_fields)


def decompose_with_residue(
    surface: str, word_index: int = 0, *, codec: CarrierStateCodec | None = None
) -> WordDecomposition:
    """فكِّك كلمةً إلى عناصرَ مصنَّفةٍ وبقيّةٍ مُسمّاة، موضعًا بموضع."""

    reader = CarrierStateCodec() if codec is None else codec
    units = reader.generate(surface)
    elements = decompose_word(surface, word_index, codec=reader)
    if len(elements) != len(units):
        raise PopulationSubstitutionError(
            "عددُ العناصر لا يوافق عددَ المواضع؛ ولا يُبنى برهانٌ على فارق"
        )

    residue = tuple(
        UnitResidue(
            unit_index=index,
            state=unit.state,
            seat=unit.seat,
            tanwin=unit.tanwin,
            tanwin_alif_seat=unit.tanwin_alif_seat,
            silent=unit.silent,
            waw_madda=unit.waw_madda,
            gemination=unit.gemination,
        )
        for index, unit in enumerate(units)
    )
    return WordDecomposition(
        surface=surface,
        population=Population.OBSERVED,
        elements=elements,
        residue=residue,
    )


def reconstruct(
    decomposition: WordDecomposition,
    *,
    with_residue: bool = True,
    codec: CarrierStateCodec | None = None,
) -> str:
    """أعِد بناءَ السطح من العناصر والبقيّة؛ وأسقِط البقيّةَ لترى الكسر.

    و`with_residue=False` ليست خيارَ استعمال، بل **أداةُ برهان**: تُري أنّ
    البقيّةَ حاملةٌ للوزن لأنّ إسقاطها يغيّر المخرَج.
    """

    writer = CarrierStateCodec() if codec is None else codec
    original = writer.generate(decomposition.surface)
    units: list[CarrierStateUnit] = []

    for index, element in enumerate(decomposition.elements):
        residue = decomposition.residue[index]
        carrier = original[index].carrier

        if element.status is JoinInputStatus.NOT_AN_ELEMENT:
            if not with_residue:
                continue
            units.append(CarrierStateUnit(carrier=carrier, state=residue.state))
            continue

        if element.vowel is not None:
            state = _VOWEL_STATE_OF[element.vowel.identity.value]
        elif with_residue:
            state = residue.state
        else:
            state = CarrierState.SUKUN_IMPLICIT

        if not with_residue:
            units.append(
                CarrierStateUnit(
                    carrier=carrier,
                    state=state,
                    gemination=(
                        GeminationRole.PAIR_START
                        if element.consonant is not None
                        and element.consonant.is_gemination_pair_start
                        else None
                    ),
                )
            )
            continue

        units.append(
            CarrierStateUnit(
                carrier=carrier,
                state=state,
                gemination=residue.gemination,
                tanwin=residue.tanwin,
                seat=residue.seat,
                tanwin_alif_seat=residue.tanwin_alif_seat,
                silent=residue.silent,
                waw_madda=residue.waw_madda,
            )
        )

    return writer.retrieve(units)


_VOWEL_STATE_OF: Final[dict[str, CarrierState]] = {
    "fatha": CarrierState.FATHA,
    "damma": CarrierState.DAMMA,
    "kasra": CarrierState.KASRA,
}


# --- المبرهنة ----------------------------------------------------------------------


@dataclass(frozen=True)
class ReconstructionReport:
    """تقريرُ البناء على مفردةٍ مُسمّاة: ما عاد، وما انكسر، وأين."""

    population: Population
    source_id: str
    word_count: int
    exact_rebuilds: int
    broken_words: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.exact_rebuilds + len(self.broken_words) != self.word_count:
            raise PopulationSubstitutionError(
                "مجموعُ العائد والمكسور لا يساوي المعدود؛ ولا يُطوى الفارق"
            )

    @property
    def closes(self) -> bool:
        """أتُغلَق المبرهنةُ على هذه المفردة؟ لا نسبةَ نجاحٍ ههنا بل إغلاقٌ تامّ."""

        return self.word_count > 0 and not self.broken_words


def _report(
    lines: tuple[str, ...] | None, source_id: str | None, *, with_residue: bool
) -> ReconstructionReport:
    text = FATIHA_LINES if lines is None else lines
    identifier = FATIHA_SOURCE_ID if source_id is None else source_id
    codec = CarrierStateCodec()
    words = 0
    exact = 0
    broken: list[str] = []
    for line in text:
        for word in line.split():
            words += 1
            decomposition = decompose_with_residue(word, words - 1, codec=codec)
            rebuilt = reconstruct(decomposition, with_residue=with_residue, codec=codec)
            if rebuilt == word:
                exact += 1
            else:
                broken.append(word)
    return ReconstructionReport(
        population=Population.OBSERVED,
        source_id=identifier,
        word_count=words,
        exact_rebuilds=exact,
        broken_words=tuple(broken),
    )


def prove_decomposition_reconstructs(
    lines: tuple[str, ...] | None = None, *, source_id: str | None = None
) -> ReconstructionReport:
    """المبرهنة: فكِّك ثمّ أعِد البناءَ بالبقيّة، فيعود السطحُ حرفًا حرفًا."""

    return _report(lines, source_id, with_residue=True)


def prove_the_residue_is_necessary(
    lines: tuple[str, ...] | None = None, *, source_id: str | None = None
) -> ReconstructionReport:
    """الشاهدُ المضادّ: أسقِط البقيّةَ فينكسر البناء، فتثبت ضرورتُها بالفشل."""

    return _report(lines, source_id, with_residue=False)


# --- الحدودُ مُسمّاةً -------------------------------------------------------------


A_MEASURED_CAPACITY_IS_NOT_A_DECLARED_UPPER_BOUND_NOTE: Final[str] = (
    "AMeasuredCapacityIsNotADeclaredUpperBound: سعةُ حاملٍ مقيسةٌ في إيداعٍ "
    "مبصوم، وجداءُ المفردة المُعلَنة حدٌّ أعلى؛ ولا يُوضَع أحدُهما موضعَ الآخر "
    "في برهان، ولا يُوصَف مدًى بأنّه متّصلٌ قبل عدِّ ثقوبه"
)

THE_RESIDUE_IS_LOAD_BEARING_NOT_DECORATIVE_NOTE: Final[str] = (
    "TheResidueIsLoadBearingNotDecorative: العناصرُ المصنَّفةُ وحدَها لا تعيد "
    "بناءَ السطح؛ نوعُ السكون والمقعدُ والحالاتُ البنيويّةُ تُحمَل بقيّةً "
    "مُسمّاة، وإسقاطُها يكسر البناءَ قياسًا لا تقديرًا"
)

THE_THEOREM_CLOSES_ON_A_NAMED_POPULATION_ONLY_NOTE: Final[str] = (
    "TheTheoremClosesOnANamedPopulationOnly: الإغلاقُ ههنا على المفردة "
    "المرصودة بعينها؛ ولا يمتدّ إلى المفردة المُعلَنة ولا إلى مدوّنةٍ أخرى إلّا "
    "بإجرائه عليها وتسميتها"
)

THIS_IS_NOT_A_CV_BIRTH_THEOREM_NOTE: Final[str] = (
    "ThisIsNotACVBirthTheorem: ما أُغلق تفكيكٌ وإعادةُ بناء، لا ولادةُ صامتٍ "
    "وصائتٍ ومقطع؛ والانتقالُ إليها يلزمه اختبارٌ مستقلٌّ لم يُجرَ بعد"
)

REFINEMENT_NECESSITY_IS_UNPROVEN_NOTE: Final[str] = (
    "RefinementNecessityIsUnprovenSoRefineSlotIsUnlicensed: لا تُضاف عمليّةُ "
    "تنقيحٍ إلى الجبر قبل برهانِ ضرورتها لوظيفةٍ مستقلّة؛ ونسبةُ نجاحٍ في "
    "مدوّنةٍ ليست برهانَ ضرورة"
)

THE_SAME_DEPOSIT_MEASURED_TWICE_GIVES_TWO_LEGITIMATE_NUMBERS_NOTE: Final[str] = (
    "TheSameDepositMeasuredTwiceGivesTwoLegitimateNumbers: المِرمازُ والليفُ "
    "يقيسان الإيداعَ نفسَه فيختلفان في عدد الحوامل وعدد المواضع وأقصى سعة؛ "
    "ولا يُرجَّح أحدُهما ولا يُسوّى الفارق، بل تُسمّى الآلةُ مع كلّ رقم"
)

DECOMPOSITION_THEOREM_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_MEASURED_CAPACITY_IS_NOT_A_DECLARED_UPPER_BOUND_NOTE,
    THE_SAME_DEPOSIT_MEASURED_TWICE_GIVES_TWO_LEGITIMATE_NUMBERS_NOTE,
    THE_RESIDUE_IS_LOAD_BEARING_NOT_DECORATIVE_NOTE,
    THE_THEOREM_CLOSES_ON_A_NAMED_POPULATION_ONLY_NOTE,
    THIS_IS_NOT_A_CV_BIRTH_THEOREM_NOTE,
    REFINEMENT_NECESSITY_IS_UNPROVEN_NOTE,
)
