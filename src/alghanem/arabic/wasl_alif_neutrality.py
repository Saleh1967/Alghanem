"""حسابُ همزة الوصل بأثرها، وحيادُ الألف محدودًا بما لا صفَّ له.

سؤالان اثنان يُجابان ههنا من جدولَي المواضع المُودَعَين وحدَهما::

    AlifCarriesNoVowelAtTheOnset  → مرصودٌ في 66,076، ومحدودٌ بـ12,139
    HamzatAlWaslHasNoCellAtAll    → فتُعَدُّ بأثرها: 10,182 سكونَ ابتداء

**أوّلًا: صفُّ الألف في الابتداء أصفارٌ أربعة.** من بين ثمانيةٍ وعشرين صفًّا
مطبوعًا، صفُّ الألف وحدَه (0,0,0,0)، وسائرُها حيٌّ. وهذا رصدٌ على 66,076 وقعةً،
أي أضعافَ ما قِيس عليه حيادُ الألف في `alif_neutrality` (ثلاثٌ وعشرون وقعةً من
الفاتحة). فسَعةُ الرصد تغيّرت تغيُّرًا جنسيًّا، **ومنزلتُه لم تتغيّر**: ذاك
مقيسٌ من بايتاتٍ مُبصَّمة، وهذا منقولٌ من وثيقةٍ لا بايتاتِ لها هنا.

**ثانيًا: والصفرُ محدودٌ لا مُثبَت.** في جدول الابتداء 12,139 وقعةً لا صفَّ
لها (`position_haraka_bit_account`)، ولا يُعرَف ما فيها. فأقصى ما يُقال إنّ
نصيبَ الألف من مواضع الابتداء **بين صفرٍ و15.520%**، لا إنّه صفر. والفرقُ
بين «رُصِد صفرًا» و«ثبت أنّه صفر» هو الفرقُ كلُّه
(`A_PRINTED_ZERO_UNDER_AN_OPEN_SHORTFALL_IS_A_BOUND_NOT_A_ZERO`).

**ثالثًا: همزةُ الوصل لا خليّةَ لها في الجدولين أصلًا**، لا صفًّا ولا عمودًا.
فحسابُها لا يكون بعدِّ خلاياها، بل بعدِّ **ما تتركه**: 10,182 موضعَ ابتداءٍ
عليها سكون، 15.410% من الخلايا المطبوعة. والعربيّةُ لا يُبتدأ فيها بساكن —
وهي الآليّةُ التي تُجلَب همزةُ الوصل لها، ودعوًى مستقرّةٌ مقيسةٌ في
`imperative_wasla_census` لا كشفٌ ههنا. فهذه الخلايا العشرةُ آلافٍ **لا تستقيم
إلّا إن كانت ألفُ الوصل قد رُفِعت من التمثيل قبل قراءة الموضع**، فانكشف
الساكنُ بعدها أوّلًا. فحيادُ الألف ليس زينةً في الجدول: هو الذي **يصنع** هذه
المواضع (`THE_ONSET_SUKUN_IS_THE_TRACE_NOT_THE_HAMZA_ITSELF`).

**رابعًا: ونصيبُ اللام والميم يتبدّل بتبدّل المقام.** ورد في الوثيقة أنّ
(ل,سكون) و(م,سكون) يشكّلان 52.4% من سكون الابتداء. والعددان 3150 و2268
مجموعُهما 5418، وهو **53.212%** من السكون المشتقّ (10,182) و**52.404%** من
السكون المُعلَن (10,339). فالرقمُ المنقول محسوبٌ على مقامٍ لا تُخرِجه صفوفُ
الجدول نفسِه (`A_SHARE_MOVES_WITH_ITS_DENOMINATOR`).

**خامسًا: وأشدُّ ما في الباب أنّ العاجزَ له بصمةُ همزة.** نصيبُ السكون من
الاثني عشرَ ألفًا الناقصة **1.293%**، ونصيبُ السكون من صفّ الهمزة في جدول
الوصل **1.312%** — وبينهما جزءان من مئةٍ من النقطة — بينما نصيبُه من الجدول
المطبوع 15.410%. وهمزةُ القطع لا تكاد تسكن ابتداءً، فهذه بصمةٌ لا صدفة. ومع
ذلك **لا تُقبَل حسابًا**: بقيّةُ الأعمدة تفترق عن صفّ همزة الوصل أحدَ عشرَ
جزءًا في الفتحة وتسعةً في الضمّة، والموضعان موضعان لا موضعٌ واحد. فهي مرشَّحٌ
مُسمًّى يناقض قولَ الوثيقة إنّ الهمزةَ «مطويّةٌ ضمن الحروف أعلاه»: لو طُوِيت
ما بقي عجز (`THE_SHORTFALL_CARRIES_A_HAMZA_SIGNATURE_AND_IS_STILL_NOT_A_ROW`).

**خمولٌ سلطويّ**: لا ولادةَ هنا ولا حكمَ ولادةٍ ولا تجميدَ `E0`، ولا استيرادَ
من `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from .position_haraka_bit_account import (
    THE_FIRST_POSITION_TABLE,
    THE_HARAKA_COLUMNS,
    THE_LAST_POSITION_TABLE,
    DepositedTable,
    closure_of,
)

__all__ = [
    "A_LARGER_SCOPE_IS_NOT_A_HIGHER_STANDING",
    "A_PRINTED_ZERO_UNDER_AN_OPEN_SHORTFALL_IS_A_BOUND_NOT_A_ZERO",
    "A_SHARE_MOVES_WITH_ITS_DENOMINATOR",
    "NO_SOUND_IS_MEASURED_HERE",
    "THE_ALIF_ROW_AT_THE_END_IS_THE_TANWIN_ARTEFACT",
    "THE_ONSET_LAW_IS_A_STANDING_CLAIM_NOT_A_FINDING_HERE",
    "THE_ONSET_SUKUN_IS_THE_TRACE_NOT_THE_HAMZA_ITSELF",
    "THE_SHORTFALL_CARRIES_A_HAMZA_SIGNATURE_AND_IS_STILL_NOT_A_ROW",
    "WASL_ALIF_NEUTRALITY_NAMED_RESIDUALS",
    "AlifNeutralityBound",
    "NeutralityStanding",
    "SignatureStanding",
    "SukunOnsetReading",
    "WaslAlifNeutralityError",
    "alif_neutrality_bound",
    "assess_shortfall_signature",
    "carrier_sukun_share",
    "sukun_onset_reading",
]

THE_ALIF: Final[str] = "ا"
"""الحاملُ المعنيُّ بالحياد، ولا يُقرأ عن غيره."""

THE_HAMZA: Final[str] = "ء"
"""همزةُ القطع، ولها صفٌّ في جدول الوصل ولا صفَّ لها في جدول الابتداء."""

_SUKUN_INDEX: Final[int] = THE_HARAKA_COLUMNS.index("سكون")


class WaslAlifNeutralityError(ValueError):
    """رفضٌ عند القراءة: حاملٌ غائبٌ، أو مقامٌ غيرُ موجبٍ يُقسَم عليه."""


class NeutralityStanding(Enum):
    """حالُ صفرِ الألف من العجز المفتوح، حكمًا ثلاثيًّا مغلقًا."""

    ZERO_OBSERVED_AND_BOUNDED = "صفرٌ مرصودٌ ومحدودٌ بعجزٍ مفتوح"
    ZERO_OBSERVED_AND_CLOSED = "صفرٌ مرصودٌ وجدولُه مُغلَق"
    NOT_ZERO = "غيرُ صفرٍ في المطبوع"


class SignatureStanding(Enum):
    """حالُ بصمة العجز من صفّ الهمزة، ولا رابعَ يُفتَح."""

    CONSISTENT_ON_SUKUN_APART_ELSEWHERE = "موافقٌ في السكون مفترقٌ في سواه"
    CONSISTENT_THROUGHOUT = "موافقٌ في الأعمدة كلّها"
    APART = "مفترقٌ"


@dataclass(frozen=True)
class AlifNeutralityBound:
    """صفرُ الألف المرصود، ومعه أقصى ما يمكن أن يخرقه من العجز."""

    table_name: str
    carrier: str
    printed_occurrences: int
    printed_cells: tuple[int, ...]
    counted_occurrences: int
    unaccounted_occurrences: int
    standing: NeutralityStanding

    def __post_init__(self) -> None:
        if self.counted_occurrences <= 0:
            raise WaslAlifNeutralityError("حدٌّ على صفرِ وقعاتٍ ليس حدًّا.")
        if self.unaccounted_occurrences < 0:
            raise WaslAlifNeutralityError("عجزٌ سالبٌ لا يكون.")

    @property
    def maximum_share(self) -> float:
        """أقصى نصيبٍ يمكن أن يبلغه الحاملُ لو كان العجزُ كلُّه له، نسبةً مئويّة."""

        denominator = self.counted_occurrences + self.unaccounted_occurrences
        return 100.0 * (
            (self.printed_occurrences + self.unaccounted_occurrences) / denominator
        )

    @property
    def observed_share(self) -> float:
        """نصيبُ الحامل من المطبوع وحدَه، نسبةً مئويّة."""

        return 100.0 * self.printed_occurrences / self.counted_occurrences

    def zero_is_established(self) -> bool:
        """هل الصفرُ مُثبَتٌ لا مرصودًا فحسب؟ ولا يكون إلّا مع جدولٍ مُغلَق."""

        return self.standing is NeutralityStanding.ZERO_OBSERVED_AND_CLOSED


@dataclass(frozen=True)
class SukunOnsetReading:
    """سكونُ الابتداء: عدّتُه، ونصيبُه، وأثقلُ حامليه تحت مقامَيه معًا."""

    table_name: str
    derived_sukun: int
    stated_sukun: int
    printed_occurrences: int
    carriers_with_a_sukun_onset: int
    heaviest_carriers: tuple[tuple[str, int], ...]

    def __post_init__(self) -> None:
        if self.printed_occurrences <= 0:
            raise WaslAlifNeutralityError("قراءةٌ على صفرِ وقعاتٍ ليست قراءة.")
        if self.derived_sukun <= 0:
            raise WaslAlifNeutralityError("سكونٌ غيرُ موجبٍ لا يُقرأ أثرًا.")

    @property
    def share_of_printed(self) -> float:
        """نصيبُ سكون الابتداء من الخلايا المطبوعة، نسبةً مئويّة."""

        return 100.0 * self.derived_sukun / self.printed_occurrences

    @property
    def heaviest_total(self) -> int:
        """مجموعُ أثقل الحاملَين سكونًا في الابتداء."""

        return sum(count for _, count in self.heaviest_carriers)

    def heaviest_share_on_derived(self) -> float:
        """نصيبُهما من السكون المشتقّ من صفوف الجدول."""

        return 100.0 * self.heaviest_total / self.derived_sukun

    def heaviest_share_on_stated(self) -> float:
        """نصيبُهما من السكون المُعلَن في الوثيقة، وهو مقامٌ آخر."""

        if self.stated_sukun <= 0:
            raise WaslAlifNeutralityError("مقامٌ مُعلَنٌ غيرُ موجبٍ لا يُقسَم عليه.")
        return 100.0 * self.heaviest_total / self.stated_sukun


def _row_of(table: DepositedTable, carrier: str) -> tuple[int, ...]:
    for letter, cells in table.rows:
        if letter == carrier:
            return tuple(cells)
    raise WaslAlifNeutralityError(
        f"لا صفَّ للحامل {carrier} في {table.table_name}؛ وقراءةُ غائبٍ وهمٌ."
    )


def carrier_sukun_share(cells: tuple[int, ...]) -> float:
    """نصيبُ السكون من صفٍّ أو من بقيّةٍ، نسبةً مئويّة؛ وهو محورُ البصمة."""

    total = sum(cells)
    if total <= 0:
        raise WaslAlifNeutralityError("نصيبٌ على مجموعٍ غيرِ موجبٍ لا يُحسَب.")
    return 100.0 * cells[_SUKUN_INDEX] / total


def alif_neutrality_bound(
    table: DepositedTable = THE_FIRST_POSITION_TABLE,
    carrier: str = THE_ALIF,
) -> AlifNeutralityBound:
    """يقرأ صفرَ الحامل المرصود ويحدُّه بما لا صفَّ له، فلا يُقرأ الصفرُ إثباتًا."""

    cells = _row_of(table, carrier)
    closure = closure_of(table)
    printed = sum(cells)
    if printed:
        standing = NeutralityStanding.NOT_ZERO
    elif closure.shortfall:
        standing = NeutralityStanding.ZERO_OBSERVED_AND_BOUNDED
    else:
        standing = NeutralityStanding.ZERO_OBSERVED_AND_CLOSED
    return AlifNeutralityBound(
        table_name=table.table_name,
        carrier=carrier,
        printed_occurrences=printed,
        printed_cells=cells,
        counted_occurrences=closure.cell_sum,
        unaccounted_occurrences=max(closure.shortfall, 0),
        standing=standing,
    )


def sukun_onset_reading(
    table: DepositedTable = THE_FIRST_POSITION_TABLE,
    heaviest: int = 2,
) -> SukunOnsetReading:
    """يعدّ أثرَ همزة الوصل: مواضعُ الابتداء الساكنة، وأثقلُ حامليها."""

    if heaviest <= 0:
        raise WaslAlifNeutralityError("عددُ أثقل الحاملين يجب أن يكون موجبًا.")
    onsets = [
        (letter, cells[_SUKUN_INDEX])
        for letter, cells in table.rows
        if cells[_SUKUN_INDEX]
    ]
    onsets.sort(key=lambda item: (-item[1], item[0]))
    return SukunOnsetReading(
        table_name=table.table_name,
        derived_sukun=sum(count for _, count in onsets),
        stated_sukun=table.stated_column_totals[_SUKUN_INDEX],
        printed_occurrences=table.cell_sum(),
        carriers_with_a_sukun_onset=len(onsets),
        heaviest_carriers=tuple(onsets[:heaviest]),
    )


def assess_shortfall_signature(
    table: DepositedTable = THE_FIRST_POSITION_TABLE,
    reference_table: DepositedTable = THE_LAST_POSITION_TABLE,
    reference_carrier: str = THE_HAMZA,
    sukun_tolerance: float = 0.1,
    profile_tolerance: float = 0.05,
) -> tuple[SignatureStanding, float, float]:
    """يقابل بصمةَ العجز بصفّ الهمزة، ويُخرج الحكمَ مع نصيبَي السكون معًا."""

    closure = closure_of(table)
    if closure.shortfall <= 0:
        raise WaslAlifNeutralityError("لا عجزَ في هذا الجدول، فلا بصمةَ تُقابَل.")
    shortfall_share = carrier_sukun_share(closure.column_shortfalls)
    reference_share = carrier_sukun_share(_row_of(reference_table, reference_carrier))
    if abs(shortfall_share - reference_share) > sukun_tolerance:
        return SignatureStanding.APART, shortfall_share, reference_share

    reference_cells = _row_of(reference_table, reference_carrier)
    reference_total = sum(reference_cells)
    distance = 0.5 * sum(
        abs((shortfall / closure.shortfall) - (reference / reference_total))
        for shortfall, reference in zip(
            closure.column_shortfalls, reference_cells, strict=True
        )
    )
    standing = (
        SignatureStanding.CONSISTENT_THROUGHOUT
        if distance <= profile_tolerance
        else SignatureStanding.CONSISTENT_ON_SUKUN_APART_ELSEWHERE
    )
    return standing, shortfall_share, reference_share


A_PRINTED_ZERO_UNDER_AN_OPEN_SHORTFALL_IS_A_BOUND_NOT_A_ZERO: Final[str] = (
    "A_PRINTED_ZERO_UNDER_AN_OPEN_SHORTFALL_IS_A_BOUND_NOT_A_ZERO: صفُّ الألف "
    "في الابتداء أصفارٌ أربعةٌ مطبوعة، وفي الجدول 12,139 وقعةً لا صفَّ لها ولا "
    "يُعرَف ما فيها. فنصيبُ الألف بين صفرٍ و15.520%، والصفرُ **مرصودٌ محدودٌ** "
    "لا مُثبَت. ونزولُ الصفّ الناقص يحسم هذا بلا سطرِ تعديل."
)

THE_ONSET_SUKUN_IS_THE_TRACE_NOT_THE_HAMZA_ITSELF: Final[str] = (
    "THE_ONSET_SUKUN_IS_THE_TRACE_NOT_THE_HAMZA_ITSELF: همزةُ الوصل لا خليّةَ "
    "لها في الجدولين، فما يُعَدُّ ههنا أثرُها لا هي: 10,182 موضعَ ابتداءٍ "
    "ساكنًا. وعدُّ الأثر ليس عدَّ المؤثِّر: ليس كلُّ سكونِ ابتداءٍ همزةَ وصل "
    "بالضرورة، ولا يُعرَف من هذا الجدول كم منها كذلك، إذ لا عمودَ فيه للوصل."
)

THE_ONSET_LAW_IS_A_STANDING_CLAIM_NOT_A_FINDING_HERE: Final[str] = (
    "THE_ONSET_LAW_IS_A_STANDING_CLAIM_NOT_A_FINDING_HERE: امتناعُ الابتداء "
    "بساكنٍ دعوًى نحويّةٌ مستقرّةٌ، ومقيسةٌ في هذه الشجرة على بايتاتٍ مُبصَّمة "
    "في `imperative_wasla_census`. فاستعمالُها ههنا مقدّمةٌ مأخوذةٌ من هناك، "
    "لا كشفٌ يُنسَب إلى هذين الجدولين."
)

A_SHARE_MOVES_WITH_ITS_DENOMINATOR: Final[str] = (
    "A_SHARE_MOVES_WITH_ITS_DENOMINATOR: (ل,سكون)+(م,سكون) = 5418، وهي "
    "53.212% من السكون المشتقّ من الصفوف (10,182) و52.404% من السكون المُعلَن "
    "(10,339). والوثيقةُ نقلت الثاني. فالنسبةُ الواحدةُ رقمان حتّى يُسمّى "
    "مقامُها، ويُعرَض ههنا المقامان معًا لا أحدُهما."
)

THE_SHORTFALL_CARRIES_A_HAMZA_SIGNATURE_AND_IS_STILL_NOT_A_ROW: Final[str] = (
    "THE_SHORTFALL_CARRIES_A_HAMZA_SIGNATURE_AND_IS_STILL_NOT_A_ROW: نصيبُ "
    "السكون من العجز 1.293% ومن صفّ همزة جدول الوصل 1.312% ومن الجدول "
    "المطبوع 15.410%. فالعجزُ يسلك مسلكَ همزةٍ لا مسلكَ الجدول. ومع ذلك "
    "بقيّةُ أعمدته تفترق عن صفّ الهمزة أحدَ عشرَ جزءًا في الفتحة وتسعةً في "
    "الضمّة، والموضعان مختلفان أصلًا فلا يلزم توافقُهما. فهذا مرشَّحٌ "
    "**يُناقض** قولَ الوثيقة إنّ الهمزةَ مطويّةٌ في الحروف — ولو طُوِيت لأغلق "
    "الجدول — ولا يُرقّى إلى حسابٍ بلا الصفّ نفسِه."
)

THE_ALIF_ROW_AT_THE_END_IS_THE_TANWIN_ARTEFACT: Final[str] = (
    "THE_ALIF_ROW_AT_THE_END_IS_THE_TANWIN_ARTEFACT: صفُّ الألف في جدول الوصل "
    "(17,0,0,0): سبعَ عشرةَ فتحةً ولا كسرةَ ولا ضمّةَ ولا سكون. وانفرادُ "
    "الفتحة وحدَها يوافق أن تكون ألفَ تنوين الفتح المرسومة سُجِّلت خليّةً، لا "
    "ألفًا حاملةً حركةً. وهذا **موافقةُ صورةٍ** لا إسنادٌ مقيس: لا سبيلَ من "
    "هذا الجدول إلى النظر في الكلمات السبعَ عشرةَ نفسِها."
)

A_LARGER_SCOPE_IS_NOT_A_HIGHER_STANDING: Final[str] = (
    "A_LARGER_SCOPE_IS_NOT_A_HIGHER_STANDING: رُصِد حيادُ الألف ههنا في 66,076 "
    "وقعةً، وفي `alif_neutrality` في ثلاثٍ وعشرين. والسَّعةُ أكبرُ بأضعافٍ "
    "والمنزلةُ أدنى: ذاك مقيسٌ من بايتاتٍ مُبصَّمة، وهذا منقولٌ من وثيقةٍ لا "
    "بايتاتِ لها في الشجرة. فلا يُقرأ الكبرُ ترقيةً، ولا يُطرَح الأصغرُ "
    "لصِغَره."
)

NO_SOUND_IS_MEASURED_HERE: Final[str] = (
    "NO_SOUND_IS_MEASURED_HERE: كلُّ ما ههنا خلايا تمثيلٍ كتابيّ. ولم يُقَس "
    "نطقٌ ولا وصلٌ ولا ابتداءٌ مسموع، ولا يُقال إنّ الألفَ «لا تُنطَق»؛ وإنّما "
    "يُقال إنّها **لا تشغل خليّةَ حركةٍ في هذا التمثيل**. والفرقُ بينهما هو "
    "الفرقُ بين الرسم والصوت، وهو قائمٌ في `alif_neutrality` قبل هذه الوحدة."
)

WASL_ALIF_NEUTRALITY_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "A_PRINTED_ZERO_UNDER_AN_OPEN_SHORTFALL_IS_A_BOUND_NOT_A_ZERO": (
        A_PRINTED_ZERO_UNDER_AN_OPEN_SHORTFALL_IS_A_BOUND_NOT_A_ZERO
    ),
    "THE_ONSET_SUKUN_IS_THE_TRACE_NOT_THE_HAMZA_ITSELF": (
        THE_ONSET_SUKUN_IS_THE_TRACE_NOT_THE_HAMZA_ITSELF
    ),
    "THE_ONSET_LAW_IS_A_STANDING_CLAIM_NOT_A_FINDING_HERE": (
        THE_ONSET_LAW_IS_A_STANDING_CLAIM_NOT_A_FINDING_HERE
    ),
    "A_SHARE_MOVES_WITH_ITS_DENOMINATOR": A_SHARE_MOVES_WITH_ITS_DENOMINATOR,
    "THE_SHORTFALL_CARRIES_A_HAMZA_SIGNATURE_AND_IS_STILL_NOT_A_ROW": (
        THE_SHORTFALL_CARRIES_A_HAMZA_SIGNATURE_AND_IS_STILL_NOT_A_ROW
    ),
    "THE_ALIF_ROW_AT_THE_END_IS_THE_TANWIN_ARTEFACT": (
        THE_ALIF_ROW_AT_THE_END_IS_THE_TANWIN_ARTEFACT
    ),
    "A_LARGER_SCOPE_IS_NOT_A_HIGHER_STANDING": (
        A_LARGER_SCOPE_IS_NOT_A_HIGHER_STANDING
    ),
    "NO_SOUND_IS_MEASURED_HERE": NO_SOUND_IS_MEASURED_HERE,
}
"""ما لا تُثبِته هذه القراءةُ مُسمًّى باسمه، لا مطويًّا في حكمٍ عامّ."""

_FORBIDDEN_FIELD_TOKENS: Final[tuple[str, ...]] = (
    "authority",
    "born",
    "birth",
    "gate",
    "rank",
    "verdict",
)


def _assert_no_authority_field() -> None:
    """حارسُ استيراد: لا حقلَ سلطةٍ ولا رتبةٍ يتسلّل إلى قراءةٍ لا سلطةَ فيها."""

    for dataclass_type in (AlifNeutralityBound, SukunOnsetReading):
        for declared in fields(dataclass_type):
            lowered = declared.name.lower()
            for token in _FORBIDDEN_FIELD_TOKENS:
                if token in lowered:
                    raise WaslAlifNeutralityError(
                        f"حقلٌ يحمل سلطةً أو رتبةً تسلّل إلى "
                        f"{dataclass_type.__name__}: {declared.name}؛ وهذه "
                        "قراءةٌ لا سلطةَ فيها ولا رتبة."
                    )


_assert_no_authority_field()

if alif_neutrality_bound().zero_is_established():
    raise WaslAlifNeutralityError(
        "صفرُ الألف لا يُقرأ مُثبَتًا ما دام في الجدول عجزٌ مفتوح؛ وترقيتُه "
        "بلا الصفّ الناقص هي عينُ ما تمنعه هذه الوحدة."
    )

if sukun_onset_reading().derived_sukun >= sukun_onset_reading().stated_sukun:
    raise WaslAlifNeutralityError(
        "سكونُ الابتداء المشتقُّ بلغ المُعلَنَ أو تجاوزه، وهذا يعني أنّ العجزَ "
        "سُدَّ من غير صفٍّ — وهو تلفيقٌ لا تصحيح."
    )
