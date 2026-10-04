"""جدولُ الحرف والحركة: مئةٌ واثنتا عشرةَ خليّةً، وقسمتُها جشعًا وأمثلَ.

**أوّلًا: ومئةٌ واثنتا عشرةَ عددٌ مُعلَنٌ لا مكتشَف.** ١١٢ = ٢٨ × ٤، وكلا
العاملين **اختيارُ وحدةِ تحليلٍ** لا معطًى في البايتات::

    ADeclaredAlphabet      != AnAlphabetTheBytesContain
    AnEmptyCell            != AForbiddenCell
    AGreedyMerge           != AnOptimalPartition
    ACountOfPartitions     != ASearchThatWasRun

فالثمانيةُ والعشرون مقروءةٌ من `letter_fingerprint.LETTER_VOCABULARY` بعد نزع
الهمزة المفردة، والأربعُ هي الحركاتُ الثلاثُ والسكون. وما في الشجرة من
`أ إ آ ؤ ئ ٱ ى` مطويٌّ بطيّ `letter_fingerprint` نفسِه، لا بطيٍّ ثانٍ يُصطنَع؛
والتنوينُ والشدّةُ والخنجريّةُ **خارج** هذه الأربع قصدًا، لأنّ لها جدولَها في
`pair_sample_widening` (`THE_HUNDRED_AND_TWELVE_IS_A_DECLARATION_NOT_A_DISCOVERY`).

**وثانيًا: والجدولُ يمتلئ بالتوسيع، ولا يمتلئ.**

| المصدر | الخلايا المحقَّقة | الوقوعات | الحروفُ الحاضرة |
|---|---|---|---|
| الفاتحة | 41/112 | 100 | 20/28 |
| + الفتح ٢٩ | 74/112 | 270 | 27/28 |
| + نثر الشجرة | 111/112 | 105,607 | 28/28 |

فالباقيةُ واحدة: ألفٌ بسكون. **وكانت خامسةً — ظاءٌ بسكون — ثمّ رابعةً — ثاءٌ
بسكون — ثمّ ثالثةً — ألفٌ بفتحة — ثمّ ثانيةً — زايٌ بسكون — فامتلأن بنموّ نثر
الشجرة وحدَه**، ولم يتبدّل في الخطّ ولا
في المدوَّنة شيء. ونثرُ الدرجة الثالثة نثرُ الشجرة وقد أُخرِجَت هذه الوحدةُ منه
باسمها، لئلّا تتحرّك أرقامُها بتحريك وصفِها
(`A_MODULE_THAT_MEASURES_THE_TREE_LEAVES_ITSELF_OUT`)؛ وزحزحةُ ما بقي من النطاق تكشفها
`pair_sample_widening.prose_scope_has_drifted`.

**وثالثًا: والباقيةُ ندرةٌ لا منع.** السكونُ في هذا النطاق 642 من
105,607 — أي 0.61% — والألفُ كلُّ حظّها من الحركات ثلاثَ عشرةَ وقوعةً
لا غير، فمتوقَّعُ سكونها 0.079 واحتمالُ صفره 0.924. **فخليّةٌ واحدةٌ متّسقةٌ مع
الندرة** ولا تُقرأ منعًا. **وأمّا الألفُ بفتحةٍ فكانت خاليةً عند قياسٍ أسبق
(متوقَّعُها 3.107 واحتمالُ صفرها 0.045) ثمّ امتلأت بنموّ النثر وحدَه**؛ ولم يكن
خلوُّها كشفًا يومَ كان، ولا امتلاؤها كشفًا اليوم: الألفُ هي مدُّ الفتحة، فحملُها
إيّاها إعادةُ الشيء على نفسه. **وأمّا الزايُ بسكونٍ فكانت ندرةً عند قياسٍ أسبق
(2.951) ثمّ عبرت العتبةَ 2.996 بنموّ النثر ثمّ رجعت إلى دونها بنموّه
أيضًا ثمّ عبرتها ثالثةً (3.712 واحتمالُ صفرها 0.024) ثمّ امتلأت بوقوعٍ واحد**،
ولم يتبدّل في الخطّ شيء. فهذا أبينُ ما يُقال في أنّ منزلةَ الخلوّ مؤرَّخةٌ بهامشها لا ثابتةٌ بذاتها
(`AN_EMPTY_CELL_UNDER_A_SPARSE_MARGIN_IS_NOT_A_PROHIBITION`).

**ورابعًا: وسترلنج يُحصي الفضاءَ ولا يبحثه.** عددُ قسمات ٢٨ حرفًا على ‎k‎
صنفًا هو ‎S(28,k)‎، ومجموعُها عددُ بِل ‎B(28)‎، وهو
6,160,539,404,599,934,652,455 — من مرتبة ‎6.2×10²¹‎. فلا يُستقصى الأمثلُ
على الثمانية والعشرين، ولا يُدَّعى. ويُستقصى على مجموعاتٍ
صغيرةٍ **مُعلَنةٍ قبل العدّ**، فيُقاس فرقُ الجشع عن الأمثل هناك، ويُنقَل بما
هو: فجوةٌ على تلك المجموعات لا على الأبجديّة
(`A_BELL_NUMBER_IS_A_COUNT_OF_THE_SPACE_NOT_A_SEARCH_OF_IT`).

**وخامسًا: والجشعُ سقط، وسقوطُه هو الخبر.** الدمجُ الجشعُ يبلغ الأمثلَ في
ثلاث عشرةَ خليّةً من ستّ عشرة، ويُخطئه في ثلاث: 22.889 و3.002 و1.089.
فالشرطُ المُودَعُ يقتضي الصفرَ في كلّ خليّة، وقد خُرِق؛ والقربُ ليس بلوغًا،
ولا يُنقَل «الجشعُ يكفي» عن ثلاثَ عشرةَ إصابةً وثلاثِ إخفاقاتٍ معدودة. وأكبرُ
الإخفاق عند أوسع مجموعةٍ استُقصيت، فلا يُقال إنّ السعةَ تُصلِحه
(`A_GREEDY_MERGE_THAT_USUALLY_WINS_IS_NOT_AN_OPTIMISER`).

**وسادسًا: وهذه الوحدةُ لا ترفع حظرًا ولا تفكّ تجميدًا.** ما كان محجوبًا عند
`markov_readiness_gate` يبقى محجوبًا، وما كان مجمَّدًا في سجلٍّ يبقى مجمَّدًا؛
والقياسُ ههنا على نثر الشجرة والمُودَعَين القرآنيَّين، ولا يمسّ بايتاتِ
المدوّنة (`NO_MEASUREMENT_HERE_LIFTS_A_BLOCK_OR_THAWS_A_FREEZE`).

ولا سلطةَ لها: لا ولادةَ، ولا ترخيصَ، ولا تجميدَ، ولا استيرادَ من `kernel/`.
"""

from __future__ import annotations

import math
import unicodedata
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from functools import cache
from typing import Final

from .fath_ayah_source_text import FATH_AYAH_SOURCE_TEXT
from .fatiha_source_text import FATIHA_LINES
from .letter_fingerprint import LETTER_VOCABULARY, fold_root
from .markov_readiness_gate import ChainReading, token_markov_standing
from .pair_sample_widening import prose_scope_files

__all__ = [
    "AN_EMPTY_CELL_UNDER_A_SPARSE_MARGIN_IS_NOT_A_PROHIBITION",
    "A_BELL_NUMBER_IS_A_COUNT_OF_THE_SPACE_NOT_A_SEARCH_OF_IT",
    "A_GREEDY_MERGE_THAT_USUALLY_WINS_IS_NOT_AN_OPTIMISER",
    "A_MODULE_THAT_MEASURES_THE_TREE_LEAVES_ITSELF_OUT",
    "LETTER_HARAKA_PARTITION_NAMED_RESIDUALS",
    "NO_MEASUREMENT_HERE_LIFTS_A_BLOCK_OR_THAWS_A_FREEZE",
    "THE_DECLARED_HARAKAT",
    "THE_DECLARED_LETTERS",
    "THE_DECLARED_PROBES",
    "THE_HUNDRED_AND_TWELVE",
    "THE_HUNDRED_AND_TWELVE_IS_A_DECLARATION_NOT_A_DISCOVERY",
    "THE_PREREGISTERED_GREEDY_CONDITION",
    "THE_SURPRISE_FLOOR",
    "AbsenceStanding",
    "CellAbsence",
    "GreedyStanding",
    "LetterHarakaPartitionError",
    "PartitionProbe",
    "ProbeReading",
    "SourceRung",
    "TableCensus",
    "absent_cells",
    "bell_number",
    "cell_counts",
    "greedy_partition",
    "greedy_standing",
    "letter_profiles",
    "measure_greedy_gap",
    "optimal_partition",
    "partition_criterion",
    "partitions_of",
    "rung_text",
    "stirling_second_kind",
    "table_census",
    "the_block_and_the_freeze_are_untouched",
    "the_declared_probes",
    "verify_stirling_matches_its_recurrence",
    "verify_the_enumeration_counts_what_stirling_says",
]


class LetterHarakaPartitionError(RuntimeError):
    """رفضٌ ههنا: أبجديّةٌ غيرُ مُعلَنة، أو قسمةٌ لا تغطّي حروفَها."""


# ---------------------------------------------------------------------------
# المُعلَنُ قبل العدّ
# ---------------------------------------------------------------------------

THE_DECLARED_LETTERS: Final[tuple[str, ...]] = tuple(
    letter for letter in LETTER_VOCABULARY if letter != "ء"
)
"""الثمانيةُ والعشرون، مقروءةً من مفردة `letter_fingerprint` لا مُعادةَ الكتابة."""

THE_DECLARED_HARAKAT: Final[tuple[str, ...]] = ("\u064e", "\u064f", "\u0650", "\u0652")
"""الفتحةُ والضمّةُ والكسرةُ والسكون؛ والتنوينُ والشدّةُ خارجَها قصدًا."""

THE_HUNDRED_AND_TWELVE: Final[int] = len(THE_DECLARED_LETTERS) * len(
    THE_DECLARED_HARAKAT
)
"""عدّةُ الخلايا: ٢٨ × ٤؛ محسوبٌ من المُعلَنَين لا منقولًا رقمًا."""

THE_SURPRISE_FLOOR: Final[float] = 0.05
"""عتبةُ الاستغراب: خليّةٌ خاليةٌ احتمالُ خلوِّها فوقها ليست دعوى منع."""


class SourceRung(Enum):
    """درجاتُ المصدر الثلاثُ، تراكميّةً لا متوازية."""

    FATIHA = "الفاتحة"
    WITH_FATH = "الفاتحة + الفتح ٢٩"
    WITH_PROSE = "وزيادةُ نثر الشجرة"


class AbsenceStanding(Enum):
    """منزلةُ خليّةٍ خالية: متّسقةٌ مع الندرة، أو خلوٌّ يستحقّ النظر."""

    CONSISTENT_WITH_SCARCITY = "خلوٌّ متّسقٌ مع ندرة الهامش"
    SURPRISING_UNDER_THE_MARGIN = "خلوٌّ مستغرَبٌ تحت الهامش"


class GreedyStanding(Enum):
    """منزلةُ الجشع بالشرط المُودَع: بلوغٌ، أو إخفاقٌ معدود."""

    REACHES_THE_OPTIMUM = "بلغ الأمثلَ في كلّ خليّةٍ مُعلَنة"
    FALLS_SHORT = "أخفق في خليّةٍ فأكثر"


# ---------------------------------------------------------------------------
# البقايا المسمّاة
# ---------------------------------------------------------------------------

THE_HUNDRED_AND_TWELVE_IS_A_DECLARATION_NOT_A_DISCOVERY: Final[str] = (
    "THE_HUNDRED_AND_TWELVE_IS_A_DECLARATION_NOT_A_DISCOVERY: ١١٢ = ٢٨ × ٤، "
    "وكلا العاملين اختيارُ وحدةِ تحليل: الأبجديّةُ مطويّةٌ بطيٍّ مُعلَن، "
    "والحركاتُ أربعٌ بإخراج التنوين والشدّة والخنجريّة؛ فلو تغيّر الطيُّ أو "
    "أُدخِلت الشدّةُ تغيّر العددُ ولم تتغيّر البايتات"
)

AN_EMPTY_CELL_UNDER_A_SPARSE_MARGIN_IS_NOT_A_PROHIBITION: Final[str] = (
    "AN_EMPTY_CELL_UNDER_A_SPARSE_MARGIN_IS_NOT_A_PROHIBITION: الخليّةُ "
    "الخاليةُ التي متوقَّعُها من هوامشها أقلُّ من وقوعٍ أو وقوعين خلوُّها "
    "متوقَّع؛ فلا تُقرَأ منعًا في الخطّ حتّى يكون خلوُّها مستغرَبًا تحت هامشها"
)

A_BELL_NUMBER_IS_A_COUNT_OF_THE_SPACE_NOT_A_SEARCH_OF_IT: Final[str] = (
    "A_BELL_NUMBER_IS_A_COUNT_OF_THE_SPACE_NOT_A_SEARCH_OF_IT: عددُ بِل "
    "للثمانية والعشرين من مرتبة 6.2×10²¹، فلا أمثلَ مُستقصًى على الأبجديّة "
    "كلِّها؛ وما يُقاس من فجوةٍ فهو على مجموعاتٍ صغيرةٍ مُعلَنةٍ لا عليها"
)

A_GREEDY_MERGE_THAT_USUALLY_WINS_IS_NOT_AN_OPTIMISER: Final[str] = (
    "A_GREEDY_MERGE_THAT_USUALLY_WINS_IS_NOT_AN_OPTIMISER: بلوغُ الأمثل في "
    "أكثر الخلايا لا يجعل الدمجَ الجشعَ أمثلَ؛ والشرطُ يقتضي الصفرَ في كلّ "
    "خليّةٍ مُعلَنة، وخليّةٌ واحدةٌ تُخرِق الدعوى كلَّها"
)

A_MODULE_THAT_MEASURES_THE_TREE_LEAVES_ITSELF_OUT: Final[str] = (
    "A_MODULE_THAT_MEASURES_THE_TREE_LEAVES_ITSELF_OUT: نثرُ الشجرة مادّةُ "
    "الدرجة الثالثة، وهذه الوحدةُ منه؛ فلو بقيت فيه لتحرّكت أرقامُها كلّما "
    "حُرِّك وصفُها، فأُخرِجَت باسمها كما تُخرِج `pair_sample_widening` نفسَها"
)

NO_MEASUREMENT_HERE_LIFTS_A_BLOCK_OR_THAWS_A_FREEZE: Final[str] = (
    "NO_MEASUREMENT_HERE_LIFTS_A_BLOCK_OR_THAWS_A_FREEZE: المقيسُ نثرُ الشجرة "
    "والمُودَعان القرآنيّان؛ وبوّابةُ ماركوف على المدوّنة تبقى محجوبةً بشرطها، "
    "وكلُّ رقمٍ مجمَّدٍ في سجلٍّ يبقى مجمَّدًا، فالقياسُ لا يفكّ حظرًا ولا تجميدًا"
)

LETTER_HARAKA_PARTITION_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "THE_HUNDRED_AND_TWELVE_IS_A_DECLARATION_NOT_A_DISCOVERY": (
        THE_HUNDRED_AND_TWELVE_IS_A_DECLARATION_NOT_A_DISCOVERY
    ),
    "AN_EMPTY_CELL_UNDER_A_SPARSE_MARGIN_IS_NOT_A_PROHIBITION": (
        AN_EMPTY_CELL_UNDER_A_SPARSE_MARGIN_IS_NOT_A_PROHIBITION
    ),
    "A_BELL_NUMBER_IS_A_COUNT_OF_THE_SPACE_NOT_A_SEARCH_OF_IT": (
        A_BELL_NUMBER_IS_A_COUNT_OF_THE_SPACE_NOT_A_SEARCH_OF_IT
    ),
    "A_GREEDY_MERGE_THAT_USUALLY_WINS_IS_NOT_AN_OPTIMISER": (
        A_GREEDY_MERGE_THAT_USUALLY_WINS_IS_NOT_AN_OPTIMISER
    ),
    "A_MODULE_THAT_MEASURES_THE_TREE_LEAVES_ITSELF_OUT": (
        A_MODULE_THAT_MEASURES_THE_TREE_LEAVES_ITSELF_OUT
    ),
    "NO_MEASUREMENT_HERE_LIFTS_A_BLOCK_OR_THAWS_A_FREEZE": (
        NO_MEASUREMENT_HERE_LIFTS_A_BLOCK_OR_THAWS_A_FREEZE
    ),
}


# ---------------------------------------------------------------------------
# الجدول
# ---------------------------------------------------------------------------


def rung_text(rung: SourceRung) -> str:
    """نصُّ الدرجة تراكميًّا؛ ولا تُقرأ درجةٌ إلّا وما قبلها فيها."""

    fatiha = "\n".join(FATIHA_LINES)
    if rung is SourceRung.FATIHA:
        return fatiha
    with_fath = f"{fatiha}\n{FATH_AYAH_SOURCE_TEXT}"
    if rung is SourceRung.WITH_FATH:
        return with_fath
    return f"{with_fath}\n{_prose_without_this_module()}"


_MARK_WINDOW: Final[int] = 3

_THIS_MODULE_FILE: Final[str] = "letter_haraka_partition.py"


@cache
def _prose_without_this_module() -> str:
    """نثرُ الشجرة وقد أُخرِجَت هذه الوحدةُ من نطاقها، على سنّة `pair_sample_widening`.

    ولولا الإخراجُ لتحرّك المقيسُ كلّما حُرِّك وصفُه، فصار كلُّ رقمٍ مُثبَتٍ في
    هذا النصّ ناقضًا لنفسه (`A_MODULE_THAT_MEASURES_THE_TREE_LEAVES_ITSELF_OUT`).
    """

    return "\n".join(
        path.read_text(encoding="utf-8")
        for path in prose_scope_files()
        if path.name != _THIS_MODULE_FILE
    )


@cache
def cell_counts(rung: SourceRung) -> Mapping[tuple[str, str], int]:
    """عدّةُ كلّ خليّةٍ في الدرجة: الحرفُ مطويًّا، وأوّلُ حركةٍ تليه.

    والقراءةُ تقف عند أوّل رمزٍ ليس علامةً متّصلة، فلا تُنسَب حركةٌ إلى حرفٍ
    يفصلها عنه فراغٌ أو حرفٌ آخر.
    """

    text = rung_text(rung)
    declared = set(THE_DECLARED_LETTERS)
    marks = set(THE_DECLARED_HARAKAT)
    tally: dict[tuple[str, str], int] = {}
    limit = len(text)
    for position, raw in enumerate(text):
        letter = fold_root(raw)
        if letter not in declared:
            continue
        for offset in range(position + 1, min(position + 1 + _MARK_WINDOW, limit)):
            follower = text[offset]
            if unicodedata.category(follower) != "Mn":
                break
            if follower in marks:
                key = (letter, follower)
                tally[key] = tally.get(key, 0) + 1
                break
    return tally


@dataclass(frozen=True)
class TableCensus:
    """إحصاءُ درجةٍ واحدة: كم خليّةً امتلأت، وبكم وقوعًا، وكم حرفًا حضر."""

    rung: SourceRung
    realized_cells: int
    occurrences: int
    letters_present: int

    def __post_init__(self) -> None:
        if not 0 <= self.realized_cells <= THE_HUNDRED_AND_TWELVE:
            raise LetterHarakaPartitionError(
                "الخلايا المحقَّقةُ خارجَ المئة والاثنتي عشرة، وهو محال."
            )

    @property
    def empty_cells(self) -> int:
        """الخلايا الخاليةُ في هذه الدرجة."""

        return THE_HUNDRED_AND_TWELVE - self.realized_cells


def table_census(rung: SourceRung) -> TableCensus:
    """إحصاءُ الدرجة، مقيسًا من بايتاتها لا منقولًا."""

    counts = cell_counts(rung)
    return TableCensus(
        rung=rung,
        realized_cells=len(counts),
        occurrences=sum(counts.values()),
        letters_present=len({letter for letter, _ in counts}),
    )


@dataclass(frozen=True)
class CellAbsence:
    """خليّةٌ خاليةٌ ومعها متوقَّعُها من الهوامش، ومنزلتُها المُشتقّةُ منه."""

    letter: str
    haraka: str
    row_total: int
    expected: float

    def __post_init__(self) -> None:
        if self.expected < 0.0:
            raise LetterHarakaPartitionError("متوقَّعٌ سالبٌ، وهو محال.")

    @property
    def probability_of_zero(self) -> float:
        """احتمالُ الصفر تحت بواسون بالمتوقَّع نفسِه؛ حدٌّ أعلى متحفِّظ."""

        return math.exp(-self.expected)

    @property
    def standing(self) -> AbsenceStanding:
        """أخلوٌّ متّسقٌ مع الندرة، أم مستغرَبٌ تحت هامشه؟"""

        if self.probability_of_zero >= THE_SURPRISE_FLOOR:
            return AbsenceStanding.CONSISTENT_WITH_SCARCITY
        return AbsenceStanding.SURPRISING_UNDER_THE_MARGIN


def absent_cells(rung: SourceRung = SourceRung.WITH_PROSE) -> tuple[CellAbsence, ...]:
    """الخلايا الخاليةُ في الدرجة، وكلُّ واحدةٍ ومعها متوقَّعُها لا وحدَها."""

    counts = cell_counts(rung)
    grand = sum(counts.values())
    if grand == 0:
        raise LetterHarakaPartitionError("درجةٌ بلا وقوعٍ واحد لا تُقرَأ خلاياها.")
    column: dict[str, int] = {}
    row: dict[str, int] = {}
    for (letter, haraka), value in counts.items():
        row[letter] = row.get(letter, 0) + value
        column[haraka] = column.get(haraka, 0) + value
    empty: list[CellAbsence] = []
    for letter in THE_DECLARED_LETTERS:
        for haraka in THE_DECLARED_HARAKAT:
            if (letter, haraka) in counts:
                continue
            empty.append(
                CellAbsence(
                    letter=letter,
                    haraka=haraka,
                    row_total=row.get(letter, 0),
                    expected=row.get(letter, 0) * column.get(haraka, 0) / grand,
                )
            )
    return tuple(empty)


@cache
def letter_profiles(
    rung: SourceRung = SourceRung.WITH_PROSE,
) -> Mapping[str, tuple[int, ...]]:
    """صفُّ كلّ حرفٍ على الحركات الأربع، بترتيب `THE_DECLARED_HARAKAT`."""

    counts = cell_counts(rung)
    return {
        letter: tuple(
            counts.get((letter, haraka), 0) for haraka in THE_DECLARED_HARAKAT
        )
        for letter in THE_DECLARED_LETTERS
    }


# ---------------------------------------------------------------------------
# سترلنج وبِل
# ---------------------------------------------------------------------------


def stirling_second_kind(count: int, classes: int) -> int:
    """عددُ قسمات ``count`` عنصرًا على ``classes`` صنفًا غيرِ خالٍ، صحيحًا تامًّا."""

    if count < 0 or classes < 0:
        raise LetterHarakaPartitionError("سترلنج لا يُحسب على عددٍ سالب.")
    if classes == 0:
        return 1 if count == 0 else 0
    if classes > count:
        return 0
    total = 0
    for index in range(classes + 1):
        term = math.comb(classes, index) * index**count
        total += -term if (classes - index) % 2 else term
    return total // math.factorial(classes)


def bell_number(count: int) -> int:
    """عددُ بِل: مجموعُ قسمات ``count`` عنصرًا على كلّ عدّةِ أصناف."""

    return sum(stirling_second_kind(count, classes) for classes in range(count + 1))


def verify_stirling_matches_its_recurrence() -> bool:
    """فحصُ المبرهنة الأولى آليًّا: ‎S(n,k) = k·S(n−1,k) + S(n−1,k−1)‎.

    والصيغةُ المستعملةُ أعلاه جامعةٌ متناوبةُ الإشارة، فمطابقتُها للتكرار فحصٌ
    مستقلٌّ لا إعادةُ حساب.
    """

    for count in range(1, 13):
        for classes in range(1, count + 1):
            direct = stirling_second_kind(count, classes)
            recurrent = classes * stirling_second_kind(
                count - 1, classes
            ) + stirling_second_kind(count - 1, classes - 1)
            if direct != recurrent:
                raise LetterHarakaPartitionError(
                    f"سترلنج خالف تكرارَه عند ({count}, {classes})."
                )
    return True


def partitions_of(
    items: Sequence[str], classes: int
) -> Iterable[tuple[tuple[str, ...], ...]]:
    """كلُّ قسمات ``items`` على ``classes`` صنفًا، مُولَّدةً واحدةً واحدة."""

    if classes <= 0 or classes > len(items):
        return
    if classes == 1:
        yield (tuple(items),)
        return
    if classes == len(items):
        yield tuple((item,) for item in items)
        return
    first, rest = items[0], items[1:]
    for block in partitions_of(rest, classes):
        for index in range(len(block)):
            yield block[:index] + ((first, *block[index]),) + block[index + 1 :]
    for block in partitions_of(rest, classes - 1):
        yield ((first,), *block)


def verify_the_enumeration_counts_what_stirling_says() -> bool:
    """فحصُ المبرهنة الثانية آليًّا: المولِّدُ يُخرِج ‎S(n,k)‎ قسمةً متمايزة.

    ولو أخرج أقلَّ لسقط الأمثلُ إلى بحثٍ ناقص، ولو أخرج مكرَّرًا لكان العدُّ
    وهمًا؛ فيُفحَص العددُ والتمايزُ معًا.
    """

    for count in range(2, 8):
        items = tuple(f"ع{index}" for index in range(count))
        for classes in range(1, count + 1):
            seen = {
                frozenset(frozenset(block) for block in partition)
                for partition in partitions_of(items, classes)
            }
            expected = stirling_second_kind(count, classes)
            produced = sum(1 for _ in partitions_of(items, classes))
            if produced != expected or len(seen) != expected:
                raise LetterHarakaPartitionError(
                    f"المولِّدُ أخرج {produced} ({len(seen)} متمايزة) "
                    f"بإزاء {expected} عند ({count}, {classes})."
                )
    return True


# ---------------------------------------------------------------------------
# الجشعُ والأمثل
# ---------------------------------------------------------------------------


def _class_log_likelihood(
    partition: Sequence[Sequence[str]],
    profiles: Mapping[str, tuple[int, ...]],
) -> float:
    reading = 0.0
    for block in partition:
        merged = [0] * len(THE_DECLARED_HARAKAT)
        for letter in block:
            for index, value in enumerate(profiles[letter]):
                merged[index] += value
        total = sum(merged)
        if total == 0:
            continue
        for value in merged:
            if value > 0:
                reading += value * math.log(value / total)
    return reading


def partition_criterion(
    partition: Sequence[Sequence[str]],
    profiles: Mapping[str, tuple[int, ...]],
) -> float:
    """معيارُ العقوبة على قسمةٍ: ‎−2·لوغاريتم الأرجحيّة + الحرّيّة × لوغاريتم العدّة.

    والحرّيّةُ ثلاثٌ لكلّ صنف، وهي ما يُطلِقه الصنفُ الواحد على الحركات الأربع.
    وهذا هو معيارُ `markov_order_induction` نفسُه، لئلّا يكون لكلّ وحدةٍ ميزانُها.
    """

    letters = [letter for block in partition for letter in block]
    if len(letters) != len(set(letters)):
        raise LetterHarakaPartitionError("قسمةٌ كرّرت حرفًا، فليست قسمة.")
    total = sum(sum(profiles[letter]) for letter in letters)
    if total <= 0:
        raise LetterHarakaPartitionError("قسمةٌ لا وقوعَ تحتها لا تُقاس.")
    freedom = len(partition) * (len(THE_DECLARED_HARAKAT) - 1)
    return -2.0 * _class_log_likelihood(partition, profiles) + freedom * math.log(total)


def greedy_partition(
    letters: Sequence[str],
    classes: int,
    profiles: Mapping[str, tuple[int, ...]] | None = None,
) -> tuple[tuple[str, ...], ...]:
    """الدمجُ الجشع: كلُّ حرفٍ صنفٌ، ثمّ يُدمَج أفضلُ زوجٍ حتّى تبلغ العدّة."""

    table = profiles if profiles is not None else letter_profiles()
    if classes <= 0 or classes > len(letters):
        raise LetterHarakaPartitionError("عدّةُ الأصناف خارجَ ما تحتمله الحروف.")
    blocks: list[tuple[str, ...]] = [(letter,) for letter in letters]
    while len(blocks) > classes:
        best: tuple[float, int, int] | None = None
        for left in range(len(blocks)):
            for right in range(left + 1, len(blocks)):
                candidate = [
                    block
                    for index, block in enumerate(blocks)
                    if index not in (left, right)
                ]
                candidate.append(blocks[left] + blocks[right])
                reading = partition_criterion(candidate, table)
                if best is None or reading < best[0]:
                    best = (reading, left, right)
        if best is None:  # pragma: no cover - حراسةُ اكتمال
            raise LetterHarakaPartitionError("لم يوجد زوجٌ يُدمَج، والعدّةُ فوق المطلوب.")
        _, left, right = best
        merged = blocks[left] + blocks[right]
        blocks = [
            block for index, block in enumerate(blocks) if index not in (left, right)
        ]
        blocks.append(merged)
    return tuple(blocks)


def optimal_partition(
    letters: Sequence[str],
    classes: int,
    profiles: Mapping[str, tuple[int, ...]] | None = None,
) -> tuple[tuple[tuple[str, ...], ...], float]:
    """الأمثلُ باستقصاءِ قسمات سترلنج كلِّها؛ ولا يُدعى إلّا حيث يُستقصى."""

    table = profiles if profiles is not None else letter_profiles()
    best: tuple[tuple[tuple[str, ...], ...], float] | None = None
    for partition in partitions_of(tuple(letters), classes):
        reading = partition_criterion(partition, table)
        if best is None or reading < best[1]:
            best = (partition, reading)
    if best is None:
        raise LetterHarakaPartitionError("لا قسمةَ على هذه العدّة، فلا أمثلَ.")
    return best


# ---------------------------------------------------------------------------
# الشرطُ المُودَع، والمسبار
# ---------------------------------------------------------------------------

_GAP_TOLERANCE: Final[float] = 1e-6

THE_PREREGISTERED_GREEDY_CONDITION: Final[str] = (
    "شرطُ حكم الجشع، مكتوبٌ قبل جولته المسجَّلة: يُقاس فرقُ معيارِ الدمج الجشع "
    "عن معيارِ الأمثل المُستقصى على كلّ مجموعةٍ من `THE_DECLARED_PROBES` وعند "
    "كلّ عدّةِ أصنافٍ فيها؛ فإن كان الفرقُ صفرًا — في حدود "
    f"{_GAP_TOLERANCE:g} — في **كلّ** خليّةٍ بلا استثناء، قيل «بلغ الجشعُ "
    "الأمثلَ على هذه المجموعات». وإن أخفق في خليّةٍ واحدةٍ قيل «أخفق»، ولا "
    "يُعوَّض الإخفاقُ بكثرة النجاح. ولا يُعمَّم الحكمُ على الثمانية والعشرين "
    "بحال، لأنّ عددَ بِل لها يمنع الاستقصاء؛ فالمقيسُ فجوةٌ على مجموعاتٍ "
    "مُعلَنةٍ لا خاصّةٌ في الأبجديّة."
)


@dataclass(frozen=True)
class PartitionProbe:
    """مسبارٌ مُعلَن: اسمُه، وحروفُه، وعدّاتُ الأصناف التي يُستقصى عندها."""

    name: str
    letters: tuple[str, ...]
    class_counts: tuple[int, ...]

    def __post_init__(self) -> None:
        if len(set(self.letters)) != len(self.letters):
            raise LetterHarakaPartitionError("مسبارٌ كرّر حرفًا في حروفه.")
        if not set(self.letters) <= set(THE_DECLARED_LETTERS):
            raise LetterHarakaPartitionError("مسبارٌ فيه حرفٌ خارجَ الثمانية والعشرين.")
        if any(count <= 0 or count >= len(self.letters) for count in self.class_counts):
            raise LetterHarakaPartitionError("عدّةُ أصنافٍ لا يقع عليها استقصاءٌ معنيّ.")


def _by_mass() -> tuple[str, ...]:
    profiles = letter_profiles()
    return tuple(
        sorted(
            THE_DECLARED_LETTERS, key=lambda letter: (-sum(profiles[letter]), letter)
        )
    )


@cache
def the_declared_probes() -> tuple[PartitionProbe, ...]:
    """المجموعاتُ المُعلَنةُ قبل العدّ، مبنيّةٌ على ترتيب الثقل لا على النتيجة."""

    ordered = _by_mass()
    return (
        PartitionProbe("أعلى عشرة", ordered[:10], (2, 3, 4, 5)),
        PartitionProbe("أدنى عشرة", ordered[-10:], (2, 3, 4, 5)),
        PartitionProbe("أعلى أحدَ عشرَ", ordered[:11], (2, 3, 4, 5)),
        PartitionProbe("واحدٌ من كلّ ثلاثة", ordered[::3][:10], (2, 3, 4, 5)),
    )


THE_DECLARED_PROBES: Final[str] = (
    "أربعةُ مساباتٍ مُعلَنة، مبنيّةٌ على ترتيب الحروف بثقلها في الجدول لا على "
    "نتيجةِ قياسٍ سابق: أعلى عشرة، وأدنى عشرة، وأعلى أحدَ عشرَ، وواحدٌ من كلّ "
    "ثلاثة؛ وكلٌّ منها يُستقصى عند عدّاتِ الأصناف ٢ و٣ و٤ و٥، فتلك ستّ عشرةَ "
    "خليّةً يلزم الصفرُ في كلّ واحدةٍ منهنّ."
)


@dataclass(frozen=True)
class ProbeReading:
    """قراءةُ خليّةٍ واحدة: المسبارُ، وعدّةُ الأصناف، وقيمتا الطرفين."""

    probe: str
    classes: int
    greedy_criterion: float
    optimal_criterion: float

    def __post_init__(self) -> None:
        if self.greedy_criterion < self.optimal_criterion - _GAP_TOLERANCE:
            raise LetterHarakaPartitionError(
                "الجشعُ سبق الأمثلَ، فالاستقصاءُ ناقصٌ أو المعيارُ مختلف."
            )

    @property
    def gap(self) -> float:
        """فجوةُ الجشع عن الأمثل؛ وهي صفرٌ أو موجبةٌ ولا تكون سالبة."""

        return max(0.0, self.greedy_criterion - self.optimal_criterion)

    @property
    def reached(self) -> bool:
        """أبلغ الجشعُ الأمثلَ في هذه الخليّة؟"""

        return self.gap <= _GAP_TOLERANCE


def measure_greedy_gap(
    probes: Sequence[PartitionProbe] | None = None,
) -> tuple[ProbeReading, ...]:
    """قياسُ الفجوة في كلّ خليّةٍ من خلايا المسابات المُعلَنة."""

    table = letter_profiles()
    readings: list[ProbeReading] = []
    for probe in probes if probes is not None else the_declared_probes():
        for classes in probe.class_counts:
            greedy = greedy_partition(probe.letters, classes, table)
            _, optimal = optimal_partition(probe.letters, classes, table)
            readings.append(
                ProbeReading(
                    probe=probe.name,
                    classes=classes,
                    greedy_criterion=partition_criterion(greedy, table),
                    optimal_criterion=optimal,
                )
            )
    return tuple(readings)


def greedy_standing(readings: Sequence[ProbeReading]) -> GreedyStanding:
    """منزلةُ الجشع بالشرط المُودَع وحدَه: خليّةٌ واحدةٌ تكفي للإخفاق."""

    if not readings:
        raise LetterHarakaPartitionError("لا منزلةَ تُقرأ من قراءاتٍ خالية.")
    if all(reading.reached for reading in readings):
        return GreedyStanding.REACHES_THE_OPTIMUM
    return GreedyStanding.FALLS_SHORT


_THE_GATE_AS_READ_AT_IMPORT: Final[ChainReading] = token_markov_standing()
"""قراءةُ البوّابة قبل أيّ قياسٍ ههنا، لتكون المقارنةُ إلى ملحوظٍ لا إلى منزلةٍ مُرمَّزة."""


def the_block_and_the_freeze_are_untouched() -> bool:
    """أزحزح شيءٌ ممّا ههنا بوّابةَ ماركوف عمّا كانت عليه عند الاستيراد؟

    والمقارنةُ إلى القراءة الملحوظة لا إلى `BLOCKED` مُرمَّزة، إذ ليست مهمّةُ
    هذه الوحدة أن تُبقيَ الحظرَ قائمًا، بل ألّا تكون هي التي حرّكته.
    """

    return token_markov_standing() == _THE_GATE_AS_READ_AT_IMPORT


# ---------------------------------------------------------------------------
# فحصُ المبرهنات وحراسةُ الخمول عند الاستيراد
# ---------------------------------------------------------------------------


def _refuse_operative_vocabulary() -> None:
    """حراسةُ الخمول: لا اسمَ ههنا يَعِد بفكّ حظرٍ أو تجميدٍ أو ولادة."""

    for name in __all__:
        if name.startswith(("birth_", "licence_", "freeze_", "unblock_", "thaw_")):
            raise LetterHarakaPartitionError(
                f"الاسمُ {name!r} يَعِد بسلطةٍ لا تملكها هذه الوحدة."
            )
    if len(THE_DECLARED_LETTERS) != 28:  # pragma: no cover - حراسةُ مفردة
        raise LetterHarakaPartitionError("الأبجديّةُ المُعلَنةُ ليست ثمانيةً وعشرين.")
    if THE_HUNDRED_AND_TWELVE != 112:  # pragma: no cover - حراسةُ مفردة
        raise LetterHarakaPartitionError("عدّةُ الخلايا ليست مئةً واثنتي عشرة.")


_refuse_operative_vocabulary()
verify_stirling_matches_its_recurrence()
verify_the_enumeration_counts_what_stirling_says()
