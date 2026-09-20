"""محاسبةُ بتّاتٍ لجدولَي الموضع الأوّل والموضع الأخير، وحسابُ إغلاقهما.

وصل جدولان من خارج الشجرة: حركةُ **الموضع الأوّل** (قانون الابتداء) بمقامٍ
منقولٍ قدرُه 78,215، وحركةُ **الموضع الأخير** (شكل الوصل) بمقامٍ منقولٍ قدرُه
78,076. والمطلوبُ منهما واحد: كم بتًّا تحمل الحركةُ فعلًا، وكم من ذلك فائضٌ
يُغني عنه الحرفُ نفسُه. وهذه الوحدة تفصل أربعةَ أشياء يُخلَط بينها::

    ADepositedTable       != AMeasurementFromTheBytes
    AStatedGrandTotal     != TheSumOfThePrintedCells
    AnExcludedCase        != AnErasedCase
    ASignificantMutualInformation != ALargeOne

**أوّلًا: العددُ مُودَعٌ لا مُعادُ اشتقاقِه.** بايتاتُ المدوّنة ليست في هذه
الشجرة — لا `MASAQ.csv` ولا مدوّنةُ القرآن المُبصَّمة — فلا يُقاس ههنا شيءٌ
من نصّ. الجدولان يُودَعان بحروفهما أعدادًا منقولة، ومنزلتُهما
`QUOTED_NOT_REDERIVED`، على منوال `word_hierarchy_deposit`
(`A_DEPOSITED_TABLE_IS_NOT_A_MEASUREMENT_FROM_THE_BYTES`).

**ثانيًا: وكلُّ بتٍّ يخرج من هنا دالّةٌ في الأعداد المُودَعة وحدَها.** فالبتّاتُ
تُشتقّ عند القراءة من الخلايا، لا تُكتَب في حقل، ولا تُنقَل من الوثيقة
الواردة. فمنزلةُ الأعداد منقولة، ومنزلةُ الحساب فوقها **مُعادةُ الاشتقاق
تمامًا** — وهما منزلتان لا واحدة
(`THE_ARITHMETIC_ABOVE_A_QUOTED_TABLE_IS_STILL_DERIVED`).

**ثالثًا: المجموعُ المُعلَن يُقابَل بمجموع الخلايا، فيسقط أحدُهما.** جدولُ
الوصل يغلق إغلاقًا تامًّا: صفوفُه وأعمدتُه ومجموعُه الكلّيُّ 78,076 بلا باقٍ.
وجدولُ الابتداء **لا يغلق**: صفوفُه متّسقةٌ مع مجاميعها، لكنّ مجموع خلاياه
66,076 لا 78,215، فبينهما **12,139 وقعةً (15.520%) لا صفَّ لها أصلًا**. وقد
جاء في الوثيقة نصًّا «تحقّق المجموع تام: 78,215»، وهذا **مكذوبٌ حسابًا** لا
اختلافَ فيه (`THE_STATED_GRAND_TOTAL_OF_THE_FIRST_TABLE_IS_REFUTED`).

**رابعًا: المستبعَدُ يُسجَّل لا يُمحى.** ثلاثُ استبعاداتٍ تخصّ هذين الجدولين:
139 كلمةً أُخرِجت قبل وصولهما، و17 خليّةَ ألفٍ داخلَ جدول الوصل، و12,139
العاجزةُ في جدول الابتداء. ويُحسَب أثرُ استبعاد السبعةَ عشرَ بالتشغيل لا
بالدعوى: مقاديرُ **الحركة** تتحرّك دون 4×10⁻⁴ بتٍّ، وإنتروبيا **الحرف**
تتحرّك 2.1×10⁻³ لأنّ صفًّا حُذِف لا لأنّ سبعةَ عشرَ خرجت. فلا حكمَ يتغيّر،
وحدُّ ذلك مذكورٌ بمقداره (`AN_EXCLUDED_CASE_IS_RECORDED_AND_NOT_ERASED`).

**خامسًا: المعلومةُ المتبادلةُ دالّةٌ ومعنويّةٌ وصغيرة معًا.** I تفوق مستوى
المصادفة مئاتِ الأضعاف، ومع ذلك لا تتجاوز 10.3% من إنتروبيا حركة الوصل
و18.8% من إنتروبيا حركة الابتداء. فمعرفةُ الحرف تُقلّص كلفةَ الحركة تقليصًا
مقيسًا، ولا تُعيّنها (`A_SIGNIFICANT_DEPENDENCE_IS_NOT_A_DETERMINING_ONE`).

**خمولٌ سلطويّ**: لا ولادةَ هنا ولا حكمَ ولادةٍ ولا تجميدَ `E0`، ولا استيرادَ
من `kernel/`، ولا يقرأ هذه الوحدةَ بابٌ فيه.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

__all__ = [
    "A_DEPOSITED_TABLE_IS_NOT_A_MEASUREMENT_FROM_THE_BYTES",
    "A_SIGNIFICANT_DEPENDENCE_IS_NOT_A_DETERMINING_ONE",
    "AN_EXCLUDED_CASE_IS_RECORDED_AND_NOT_ERASED",
    "CHANCE_LEVEL_IS_A_FLOOR_NOT_A_NULL_MODEL",
    "NO_DIRECTION_OF_DETERMINATION_IS_MEASURED_HERE",
    "POSITION_HARAKA_BIT_ACCOUNT_NAMED_RESIDUALS",
    "THE_ARITHMETIC_ABOVE_A_QUOTED_TABLE_IS_STILL_DERIVED",
    "THE_DECLARED_EXCLUSIONS",
    "THE_FIRST_POSITION_TABLE",
    "THE_LAST_POSITION_TABLE",
    "THE_STATED_GRAND_TOTAL_OF_THE_FIRST_TABLE_IS_REFUTED",
    "THE_TWO_TABLES_DO_NOT_SHARE_A_DENOMINATOR",
    "BitAccount",
    "ClosureReading",
    "ClosureStanding",
    "DeclaredExclusion",
    "DepositedTable",
    "LetterInformation",
    "PositionHarakaBitAccountError",
    "TableStanding",
    "bit_account",
    "closure_of",
    "entropy_of",
    "letter_information",
    "table_without_letter",
]

THE_HARAKA_COLUMNS: Final[tuple[str, ...]] = ("فتحة", "كسرة", "ضمة", "سكون")
"""الأعمدةُ الأربعةُ بترتيبها في الوثيقة الواردة، ولا عمودَ خامسٌ يُفتَح هنا."""


class PositionHarakaBitAccountError(ValueError):
    """رفضٌ عند الإنشاء أو القراءة: صفٌّ لا يتّسق، أو مقامٌ صفرٌ يُقسَم عليه."""


class TableStanding(Enum):
    """منزلةُ أعداد الجدول نفسِها، لا منزلةُ الحساب فوقها."""

    QUOTED_NOT_REDERIVED = "منقولٌ لا مُعادُ الاشتقاق"


class ClosureStanding(Enum):
    """حالُ الجدول من مجموعه المُعلَن، حكمًا ثلاثيًّا مغلقًا."""

    CLOSES_EXACTLY = "يغلق تمامًا"
    CELLS_FALL_SHORT = "خلاياه دون مجموعه المُعلَن"
    CELLS_OVERSHOOT = "خلاياه فوق مجموعه المُعلَن"


@dataclass(frozen=True)
class DepositedTable:
    """جدولُ 29×4 مُودَعٌ بحروفه: صفوفُه، ومجموعُه المُعلَن، ومنزلتُه."""

    table_name: str
    position: str
    rows: tuple[tuple[str, tuple[int, int, int, int]], ...]
    stated_grand_total: int
    stated_column_totals: tuple[int, ...]
    standing: TableStanding

    def __post_init__(self) -> None:
        if not self.rows:
            raise PositionHarakaBitAccountError("جدولٌ بلا صفوفٍ ليس جدولًا.")
        seen: set[str] = set()
        for letter, cells in self.rows:
            if letter in seen:
                raise PositionHarakaBitAccountError(
                    f"حرفٌ مكرَّرٌ في صفوف الجدول: {letter}"
                )
            seen.add(letter)
            if len(cells) != len(THE_HARAKA_COLUMNS):
                raise PositionHarakaBitAccountError(
                    f"صفُّ {letter} لا يحمل أربعَ خلايا بعدد الأعمدة المُعلَنة."
                )
            if any(cell < 0 for cell in cells):
                raise PositionHarakaBitAccountError(
                    f"خليّةٌ سالبةٌ في صفّ {letter}؛ والعدُّ لا يكون سالبًا."
                )
        if self.stated_grand_total <= 0:
            raise PositionHarakaBitAccountError("مجموعٌ مُعلَنٌ غيرُ موجبٍ لا يصلح مقامًا.")
        if len(self.stated_column_totals) != len(THE_HARAKA_COLUMNS):
            raise PositionHarakaBitAccountError(
                "مجاميعُ الأعمدة المُعلَنةُ لا تُطابق عددَ الأعمدة المُصرَّح به."
            )

    def cell_sum(self) -> int:
        """مجموعُ الخلايا المطبوعة وحدَها، لا المجموعُ المُعلَن فوقها."""

        return sum(sum(cells) for _, cells in self.rows)

    def live_rows(self) -> tuple[tuple[str, tuple[int, int, int, int]], ...]:
        """الصفوفُ ذاتُ المجموع الموجب؛ وصفُّ الأصفار يُعرَض ولا يُعَدُّ حرفًا حيًّا."""

        return tuple((letter, cells) for letter, cells in self.rows if sum(cells))

    def column_totals(self) -> tuple[int, ...]:
        """مجاميعُ الأعمدة الأربعة مشتقّةً من الخلايا، لا منقولةً من الوثيقة."""

        return tuple(
            sum(cells[index] for _, cells in self.rows)
            for index in range(len(THE_HARAKA_COLUMNS))
        )


@dataclass(frozen=True)
class ClosureReading:
    """قراءةُ إغلاقٍ: المُعلَنُ، والمشتقُّ، والفرقُ بينهما، وأين وقع."""

    table_name: str
    stated_grand_total: int
    cell_sum: int
    standing: ClosureStanding
    column_shortfalls: tuple[int, ...]

    @property
    def shortfall(self) -> int:
        """ما لا صفَّ له: المُعلَنُ ناقصًا مجموعَ الخلايا."""

        return self.stated_grand_total - self.cell_sum

    @property
    def shortfall_share(self) -> float:
        """نصيبُ العجز من المقام المُعلَن، نسبةً مئويّة."""

        return 100.0 * self.shortfall / self.stated_grand_total


@dataclass(frozen=True)
class BitAccount:
    """محاسبةُ بتّاتٍ كاملةٌ لجدولٍ واحد، كلُّ حقلٍ فيها مشتقٌّ من الخلايا."""

    table_name: str
    occurrences: int
    live_letters: int
    haraka_entropy: float
    letter_entropy: float
    joint_entropy: float

    def __post_init__(self) -> None:
        if self.occurrences <= 0:
            raise PositionHarakaBitAccountError("محاسبةٌ على صفرِ وقعاتٍ ليست محاسبة.")

    @property
    def conditional_haraka_entropy(self) -> float:
        """H(حركة | حرف): ما يبقى من كلفة الحركة بعد معرفة الحرف."""

        return self.joint_entropy - self.letter_entropy

    @property
    def mutual_information(self) -> float:
        """I(حرف؛حركة): ما يُغني عنه الحرفُ من كلفة الحركة."""

        return self.haraka_entropy + self.letter_entropy - self.joint_entropy

    @property
    def uniform_haraka_slack(self) -> float:
        """الفائضُ عن العشوائيّ: بُعدُ الحركة عن بتَّين تامَّين بسبب ميل توزيعها."""

        return math.log2(len(THE_HARAKA_COLUMNS)) - self.haraka_entropy

    @property
    def explained_share(self) -> float:
        """نصيبُ الحرف من إنتروبيا الحركة، نسبةً مئويّة."""

        return 100.0 * self.mutual_information / self.haraka_entropy

    @property
    def chance_level_mutual_information(self) -> float:
        """أرضيّةُ المصادفة: ما تُخرجه جداولُ مستقلّةٌ بهذا الحجم بحكم التحيّز."""

        degrees = (self.live_letters - 1) * (len(THE_HARAKA_COLUMNS) - 1)
        return degrees / (2.0 * self.occurrences * math.log(2.0))

    @property
    def times_chance_level(self) -> float:
        """كم ضعفًا تفوق المعلومةُ المتبادلةُ أرضيّةَ المصادفة."""

        floor = self.chance_level_mutual_information
        if floor <= 0.0:
            raise PositionHarakaBitAccountError("أرضيّةُ مصادفةٍ غيرُ موجبةٍ لا يُقسَم عليها.")
        return self.mutual_information / floor

    def haraka_bits_unconditioned(self) -> float:
        """جملةُ البتّات التي تحملها الحركةُ في هذا الجدول قبل معرفة الحرف."""

        return self.occurrences * self.haraka_entropy

    def haraka_bits_conditioned(self) -> float:
        """جملةُ البتّات الباقيةُ بعد معرفة الحرف."""

        return self.occurrences * self.conditional_haraka_entropy

    def bits_saved_by_the_letter(self) -> float:
        """ما يوفّره الحرفُ من بتّات على كامل الجدول."""

        return self.occurrences * self.mutual_information


@dataclass(frozen=True)
class LetterInformation:
    """نصيبُ حرفٍ واحدٍ من المعلومة المتبادلة، وعدّتُه."""

    letter: str
    occurrences: int
    contribution: float


@dataclass(frozen=True)
class DeclaredExclusion:
    """استبعادٌ مُصرَّحٌ به: عدّتُه، وسببُه، وأين وقع، ومَن أخرجه."""

    exclusion_name: str
    excluded_occurrences: int
    table_name: str
    reason: str
    excluded_before_deposit: bool

    def __post_init__(self) -> None:
        if self.excluded_occurrences <= 0:
            raise PositionHarakaBitAccountError(
                "استبعادٌ بلا عدّةٍ موجبةٍ لا يُسجَّل استبعادًا."
            )


def entropy_of(counts: Sequence[int]) -> float:
    """إنتروبيا شانون بالبتّ على عدّاتٍ خام؛ والخليّةُ الصفرُ لا تُسهِم."""

    total = sum(counts)
    if total <= 0:
        raise PositionHarakaBitAccountError("إنتروبيا على مجموعٍ غيرِ موجبٍ لا تُحسَب.")
    if any(count < 0 for count in counts):
        raise PositionHarakaBitAccountError("عدّةٌ سالبةٌ لا تدخل في إنتروبيا.")
    return -sum((count / total) * math.log2(count / total) for count in counts if count)


def closure_of(table: DepositedTable) -> ClosureReading:
    """يقابل المجموعَ المُعلَنَ بمجموع الخلايا، ويُخرج الفرقَ موزَّعًا على الأعمدة."""

    cell_sum = table.cell_sum()
    if cell_sum == table.stated_grand_total:
        standing = ClosureStanding.CLOSES_EXACTLY
    elif cell_sum < table.stated_grand_total:
        standing = ClosureStanding.CELLS_FALL_SHORT
    else:
        standing = ClosureStanding.CELLS_OVERSHOOT
    return ClosureReading(
        table_name=table.table_name,
        stated_grand_total=table.stated_grand_total,
        cell_sum=cell_sum,
        standing=standing,
        column_shortfalls=tuple(
            stated - derived
            for stated, derived in zip(
                table.stated_column_totals, table.column_totals(), strict=True
            )
        ),
    )


def bit_account(table: DepositedTable) -> BitAccount:
    """يشتقّ المحاسبةَ كاملةً من الخلايا المطبوعة وحدَها، لا من المجموع المُعلَن."""

    live = table.live_rows()
    if not live:
        raise PositionHarakaBitAccountError("جدولٌ كلُّ صفوفه أصفارٌ لا محاسبةَ فيه.")
    row_totals = [sum(cells) for _, cells in live]
    column_totals = [
        sum(cells[index] for _, cells in live)
        for index in range(len(THE_HARAKA_COLUMNS))
    ]
    joint = [cell for _, cells in live for cell in cells]
    return BitAccount(
        table_name=table.table_name,
        occurrences=sum(row_totals),
        live_letters=len(live),
        haraka_entropy=entropy_of(column_totals),
        letter_entropy=entropy_of(row_totals),
        joint_entropy=entropy_of(joint),
    )


def letter_information(table: DepositedTable) -> tuple[LetterInformation, ...]:
    """يفكّ المعلومةَ المتبادلةَ إلى نصيب كلّ حرفٍ، مرتَّبةً تنازليًّا."""

    live = table.live_rows()
    total = sum(sum(cells) for _, cells in live)
    column_totals = [
        sum(cells[index] for _, cells in live)
        for index in range(len(THE_HARAKA_COLUMNS))
    ]
    readings: list[LetterInformation] = []
    for letter, cells in live:
        row_total = sum(cells)
        contribution = sum(
            (cell / total)
            * math.log2((cell / total) / ((row_total / total) * (column / total)))
            for cell, column in zip(cells, column_totals, strict=True)
            if cell
        )
        readings.append(
            LetterInformation(
                letter=letter, occurrences=row_total, contribution=contribution
            )
        )
    return tuple(sorted(readings, key=lambda item: -item.contribution))


def table_without_letter(table: DepositedTable, letter: str) -> DepositedTable:
    """ينسخ الجدولَ بلا صفِّ حرفٍ بعينه، ليُقاس أثرُ استبعادٍ بالتشغيل لا بالدعوى."""

    kept = tuple((row, cells) for row, cells in table.rows if row != letter)
    if len(kept) == len(table.rows):
        raise PositionHarakaBitAccountError(
            f"لا صفَّ للحرف {letter} في {table.table_name}؛ واستبعادُ غائبٍ وهمٌ."
        )
    dropped_row = next(cells for row, cells in table.rows if row == letter)
    return DepositedTable(
        table_name=f"{table.table_name} — بلا صفّ {letter}",
        position=table.position,
        rows=kept,
        stated_grand_total=table.stated_grand_total - sum(dropped_row),
        stated_column_totals=tuple(
            stated - dropped
            for stated, dropped in zip(
                table.stated_column_totals, dropped_row, strict=True
            )
        ),
        standing=table.standing,
    )


THE_FIRST_POSITION_TABLE: Final[DepositedTable] = DepositedTable(
    table_name="حركة الموضع الأوّل",
    position="الموضع الأوّل — قانون الابتداء",
    rows=(
        ("ب", (1568, 1394, 121, 164)),
        ("ت", (1650, 58, 378, 374)),
        ("ث", (121, 10, 356, 30)),
        ("ج", (1009, 113, 95, 126)),
        ("ح", (1127, 168, 118, 138)),
        ("خ", (882, 63, 62, 105)),
        ("د", (209, 115, 185, 249)),
        ("ذ", (673, 648, 126, 118)),
        ("ر", (1694, 158, 151, 646)),
        ("ز", (286, 105, 36, 21)),
        ("س", (1385, 107, 239, 429)),
        ("ش", (943, 55, 93, 187)),
        ("ص", (547, 81, 91, 118)),
        ("ض", (160, 25, 31, 36)),
        ("ط", (192, 19, 29, 57)),
        ("ظ", (285, 18, 139, 76)),
        ("ع", (3555, 528, 85, 757)),
        ("غ", (454, 14, 43, 75)),
        ("ف", (1996, 1778, 76, 91)),
        ("ق", (2356, 113, 932, 130)),
        ("ك", (2111, 66, 781, 247)),
        ("ل", (5475, 515, 43, 3150)),
        ("م", (2311, 2098, 1074, 2268)),
        ("ن", (1050, 81, 249, 420)),
        ("ه", (613, 51, 659, 55)),
        ("و", (5091, 20, 62, 113)),
        ("ي", (2513, 0, 983, 2)),
        ("ا", (0, 0, 0, 0)),
    ),
    stated_grand_total=78_215,
    stated_column_totals=(47_487, 12_485, 7_904, 10_339),
    standing=TableStanding.QUOTED_NOT_REDERIVED,
)
"""ثمانيةٌ وعشرون صفًّا، ومجموعُ خلاياها 66,076 بإزاء 78,215 مُعلَنة."""

THE_LAST_POSITION_TABLE: Final[DepositedTable] = DepositedTable(
    table_name="حركة الموضع الأخير",
    position="الموضع الأخير — شكل الوصل",
    rows=(
        ("ء", (1435, 1071, 428, 39)),
        ("ب", (831, 1033, 916, 130)),
        ("ت", (1359, 1965, 1062, 144)),
        ("ث", (117, 94, 109, 42)),
        ("ج", (123, 83, 173, 66)),
        ("ح", (272, 147, 191, 46)),
        ("خ", (35, 25, 16, 8)),
        ("د", (933, 897, 975, 467)),
        ("ذ", (870, 1534, 136, 287)),
        ("ر", (1234, 1264, 2012, 318)),
        ("ز", (46, 102, 123, 22)),
        ("س", (620, 340, 192, 27)),
        ("ش", (56, 46, 15, 8)),
        ("ص", (34, 66, 43, 12)),
        ("ض", (198, 435, 170, 40)),
        ("ط", (76, 76, 64, 10)),
        ("ظ", (15, 42, 30, 2)),
        ("ع", (499, 121, 659, 129)),
        ("غ", (53, 30, 56, 24)),
        ("ف", (388, 1405, 321, 71)),
        ("ق", (511, 413, 602, 104)),
        ("ك", (1428, 293, 538, 65)),
        ("ل", (6178, 1605, 2162, 966)),
        ("م", (5211, 2703, 1875, 3383)),
        ("ن", (6214, 1554, 1408, 1065)),
        ("ه", (1832, 2039, 2540, 27)),
        ("و", (668, 64, 35, 707)),
        ("ي", (770, 166, 89, 1291)),
        ("ا", (17, 0, 0, 0)),
    ),
    stated_grand_total=78_076,
    stated_column_totals=(32_023, 19_613, 16_940, 9_500),
    standing=TableStanding.QUOTED_NOT_REDERIVED,
)
"""تسعةٌ وعشرون صفًّا، ومجموعُ خلاياها 78,076 مطابقًا لمجموعه المُعلَن."""

THE_DECLARED_EXCLUSIONS: Final[tuple[DeclaredExclusion, ...]] = (
    DeclaredExclusion(
        exclusion_name="التمثيلُ المنتهي بعلامة تشكيلٍ مجرَّدة",
        excluded_occurrences=139,
        table_name="حركة الموضع الأخير",
        reason=(
            "ينتهي تمثيلُها الصرفيُّ بشدّةٍ أو تنوينٍ لا بحرفٍ حقيقيّ، "
            "فأُخرِجت قبل وصول الجدول ولم تدخل خليّةً."
        ),
        excluded_before_deposit=True,
    ),
    DeclaredExclusion(
        exclusion_name="خليّةُ الألف المفتوحة",
        excluded_occurrences=17,
        table_name="حركة الموضع الأخير",
        reason=(
            "الأرجحُ أنّها ألفُ تنوين الفتح المرسومة، سُجِّلت خليّةً مستقلّةً "
            "بدل أن تُطوى في تنوين ما قبلها؛ وهي داخلُ الجدول لا خارجَه."
        ),
        excluded_before_deposit=False,
    ),
    DeclaredExclusion(
        exclusion_name="العاجزُ بلا صفّ",
        excluded_occurrences=12_139,
        table_name="حركة الموضع الأوّل",
        reason=(
            "فرقُ ما بين المجموع المُعلَن ومجموع الخلايا المطبوعة؛ لا صفَّ له "
            "في الجدول الوارد، ولم يُصرَّح باستبعاده فيه."
        ),
        excluded_before_deposit=False,
    ),
)
"""ثلاثةُ استبعاداتٍ مُسمّاةٌ بعدّتها وسببها، ولا رابعَ مطويٌّ في حكمٍ عامّ."""

A_DEPOSITED_TABLE_IS_NOT_A_MEASUREMENT_FROM_THE_BYTES: Final[str] = (
    "A_DEPOSITED_TABLE_IS_NOT_A_MEASUREMENT_FROM_THE_BYTES: خلايا الجدولين "
    "أعدادٌ منقولةٌ من وثيقةٍ خارجيّة، لا مقيسةٌ من بايتاتٍ مُبصَّمة. ولا "
    "`MASAQ.csv` في الشجرة ولا مدوّنةُ القرآن، فلا سبيلَ ههنا إلى إعادة عدِّ "
    "خليّةٍ واحدة. ونزولُ البايتات ينقل منزلةَ الأعداد بلا سطرِ تعديل."
)

THE_ARITHMETIC_ABOVE_A_QUOTED_TABLE_IS_STILL_DERIVED: Final[str] = (
    "THE_ARITHMETIC_ABOVE_A_QUOTED_TABLE_IS_STILL_DERIVED: منزلةُ الأعداد "
    "منقولةٌ، ومنزلةُ البتّات فوقها مُعادةُ الاشتقاق تمامًا: كلُّ إنتروبيا "
    "ومعلومةٍ متبادلةٍ هنا دالّةٌ في الخلايا تُحسَب عند القراءة ولا تُكتَب في "
    "حقل. فلا يُقرأ صحّةُ الحساب تصديقًا للأعداد، ولا نقلُ الأعداد طعنًا في "
    "الحساب: منزلتان لا واحدة."
)

THE_STATED_GRAND_TOTAL_OF_THE_FIRST_TABLE_IS_REFUTED: Final[str] = (
    "THE_STATED_GRAND_TOTAL_OF_THE_FIRST_TABLE_IS_REFUTED: صفوفُ جدول "
    "الابتداء متّسقةٌ كلُّها مع مجاميعها، ومجموعُ خلاياه 66,076 لا 78,215؛ "
    "فبينهما 12,139 وقعةً (15.520%) لا صفَّ لها. وجاء في الوثيقة نصًّا "
    "«تحقّق المجموع تام: 78,215» وهو مكذوبٌ حسابًا. وما ينقص موزَّعٌ على "
    "الأعمدة (7231، 4084، 667، 157)، ولا يُعرَف أيُّ صفٍّ سقط: الوثيقةُ "
    "تقول إنّ الهمزةَ «مطويّةٌ ضمن الحروف أعلاه»، ولو طُويت لأغلق الجدول. "
    "فالطيُّ مدفوعٌ حسابًا، وموضعُ الاثني عشرَ ألفًا بقيّةٌ بلا جواب."
)

AN_EXCLUDED_CASE_IS_RECORDED_AND_NOT_ERASED: Final[str] = (
    "AN_EXCLUDED_CASE_IS_RECORDED_AND_NOT_ERASED: طُلِب محوُ المخالفات، "
    "والمحوُ يُخرِج الشجرةَ من قانونها. فتُستبعَد من نطاق القياس وتبقى في "
    "`THE_DECLARED_EXCLUSIONS` بعدّتها وسببها وموضعها. وأثرُ استبعاد "
    "السبعةَ عشرَ مقيسٌ بالتشغيل عبر `table_without_letter`: مقاديرُ الحركة "
    "تتحرّك دون 4×10⁻⁴ بتٍّ، وإنتروبيا الحرف 2.1×10⁻³ لأنّ صفًّا حُذِف لا "
    "لأنّ سبعةَ عشرَ خرجت. فلا حكمَ يتغيّر، وهذا **مقيسٌ** بحدِّه لا مُعمَّم."
)

A_SIGNIFICANT_DEPENDENCE_IS_NOT_A_DETERMINING_ONE: Final[str] = (
    "A_SIGNIFICANT_DEPENDENCE_IS_NOT_A_DETERMINING_ONE: تفوق المعلومةُ "
    "المتبادلةُ أرضيّةَ المصادفة مئاتِ الأضعاف، ومع ذلك لا تتجاوز 10.3% من "
    "إنتروبيا حركة الوصل ولا 18.8% من إنتروبيا حركة الابتداء. فمعرفةُ الحرف "
    "تُقلّص كلفةَ الحركة ولا تُعيّنها، ومَن قرأ المعنويّةَ تعيينًا قرأ صِغَرَ "
    "احتمالٍ قوّةَ أثر."
)

CHANCE_LEVEL_IS_A_FLOOR_NOT_A_NULL_MODEL: Final[str] = (
    "CHANCE_LEVEL_IS_A_FLOOR_NOT_A_NULL_MODEL: `chance_level_mutual_information` "
    "تقريبُ تحيّزٍ تحليليٌّ لجداولَ مستقلّةٍ بهذا الحجم، لا صفريٌّ مُشتقٌّ بتبديلٍ "
    "على وقعاتٍ فعليّة. والوقعاتُ ليست ههنا أصلًا، فلا سبيلَ إلى تبديل. "
    "فيُقرأ الرقمُ أرضيّةً تُقارَن بها، لا قيمةَ احتمالٍ ولا اختبارًا."
)

NO_DIRECTION_OF_DETERMINATION_IS_MEASURED_HERE: Final[str] = (
    "NO_DIRECTION_OF_DETERMINATION_IS_MEASURED_HERE: I(حرف؛حركة) مقدارٌ "
    "متناظرٌ بحكم تعريفه، فلا يُقرأ منه أنّ الحرفَ يُحدِّد الحركةَ دون العكس، "
    "ولا أنّ بينهما سببًا أصلًا. والعرضُ هنا مشروطٌ بالحرف لأنّ السؤال ورد "
    "كذلك، لا لأنّ الاتّجاهَ قِيس."
)

THE_TWO_TABLES_DO_NOT_SHARE_A_DENOMINATOR: Final[str] = (
    "THE_TWO_TABLES_DO_NOT_SHARE_A_DENOMINATOR: مقامُ الأوّل 78,215 ومقامُ "
    "الثاني 78,076، ومجموعُ خلايا الأوّل 66,076. فالبتّاتُ الجمليّةُ بين "
    "الجدولين **لا تُطرَح إحداها من الأخرى**، وإنّما تُقارَن المقاديرُ "
    "المعياريّةُ وحدَها (الإنتروبيا والنصيب)."
)

POSITION_HARAKA_BIT_ACCOUNT_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "A_DEPOSITED_TABLE_IS_NOT_A_MEASUREMENT_FROM_THE_BYTES": (
        A_DEPOSITED_TABLE_IS_NOT_A_MEASUREMENT_FROM_THE_BYTES
    ),
    "THE_ARITHMETIC_ABOVE_A_QUOTED_TABLE_IS_STILL_DERIVED": (
        THE_ARITHMETIC_ABOVE_A_QUOTED_TABLE_IS_STILL_DERIVED
    ),
    "THE_STATED_GRAND_TOTAL_OF_THE_FIRST_TABLE_IS_REFUTED": (
        THE_STATED_GRAND_TOTAL_OF_THE_FIRST_TABLE_IS_REFUTED
    ),
    "AN_EXCLUDED_CASE_IS_RECORDED_AND_NOT_ERASED": (
        AN_EXCLUDED_CASE_IS_RECORDED_AND_NOT_ERASED
    ),
    "A_SIGNIFICANT_DEPENDENCE_IS_NOT_A_DETERMINING_ONE": (
        A_SIGNIFICANT_DEPENDENCE_IS_NOT_A_DETERMINING_ONE
    ),
    "CHANCE_LEVEL_IS_A_FLOOR_NOT_A_NULL_MODEL": (
        CHANCE_LEVEL_IS_A_FLOOR_NOT_A_NULL_MODEL
    ),
    "NO_DIRECTION_OF_DETERMINATION_IS_MEASURED_HERE": (
        NO_DIRECTION_OF_DETERMINATION_IS_MEASURED_HERE
    ),
    "THE_TWO_TABLES_DO_NOT_SHARE_A_DENOMINATOR": (
        THE_TWO_TABLES_DO_NOT_SHARE_A_DENOMINATOR
    ),
}
"""ما لا تُثبِته هذه المحاسبةُ مُسمًّى باسمه، لا مطويًّا في حكمٍ عامّ."""

_FORBIDDEN_FIELD_TOKENS: Final[tuple[str, ...]] = (
    "authority",
    "born",
    "birth",
    "gate",
    "rank",
    "verdict",
)


def _assert_no_authority_field() -> None:
    """حارسُ استيراد: لا حقلَ سلطةٍ ولا رتبةٍ يتسلّل إلى محاسبةٍ لا سلطةَ فيها."""

    for dataclass_type in (
        BitAccount,
        ClosureReading,
        DeclaredExclusion,
        DepositedTable,
        LetterInformation,
    ):
        for declared in fields(dataclass_type):
            lowered = declared.name.lower()
            for token in _FORBIDDEN_FIELD_TOKENS:
                if token in lowered:
                    raise PositionHarakaBitAccountError(
                        f"حقلٌ يحمل سلطةً أو رتبةً تسلّل إلى "
                        f"{dataclass_type.__name__}: {declared.name}؛ وهذه "
                        "محاسبةٌ لا سلطةَ فيها ولا رتبة."
                    )


_assert_no_authority_field()

if closure_of(THE_LAST_POSITION_TABLE).standing is not ClosureStanding.CLOSES_EXACTLY:
    raise PositionHarakaBitAccountError(
        "جدولُ الوصل كان يغلق عند الإيداع، فاختلالُه بعدُ تحريفٌ لا يُمرَّر."
    )

if closure_of(THE_FIRST_POSITION_TABLE).standing is ClosureStanding.CLOSES_EXACTLY:
    raise PositionHarakaBitAccountError(
        "جدولُ الابتداء لا يغلق، وإغلاقُه بعدُ يعني أنّ صفًّا أُقحِم لتصحيح "
        "مجموعٍ — وهذا ما تمنعه هذه الوحدة صراحةً."
    )

if (
    sum(exclusion.excluded_occurrences for exclusion in THE_DECLARED_EXCLUSIONS)
    != 139 + 17 + 12_139
):
    raise PositionHarakaBitAccountError(
        "عدّةُ الاستبعادات المُصرَّح بها تغيّرت؛ ومحوُ استبعادٍ من السجلّ محوٌ "
        "لمخالفةٍ لا تهذيبٌ لرقم."
    )
