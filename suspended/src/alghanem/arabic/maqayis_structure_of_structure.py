"""معادلةُ «بنيةِ البنية» مصوغةً بلا مِقبَضٍ يُدار بعد رؤية النتيجة.

قِيست دعوى «الجزءُ يُمثِّل الكلَّ» في `dal_alone_gloss` بفرقٍ خامٍّ وسماحيّةٍ
مُعلَنةٍ خمسًا من المئة، ثمّ عُدَّت في `maqayis_chapter_census` على الأبواب
جميعًا، فخرج أنّ الحكمَ يتبدّل بتبديل السماحيّة وحدَها. وسُمّي ذلك حينئذٍ
عيبًا في الإجراء لا في المادّة. وهذه الوحدة تُعيد صياغةَ الدعوى صياغةً
تُسقِط العتبةَ من أصلها، وتفصل::

    APartMatchingItsWhole   != AStructureRepeatingAcrossScales
    ARawGapUnderAThreshold  != ANormalisedStructureValue
    AChosenTolerance        != ADerivedNullQuantile
    AFlatCoverOfOneRecord   != ANestedCoverOfTwoDepths

**أوّلًا: دالّةُ بنيةٍ مُعيَّرةٌ لا فرقٌ خامّ.** لكلّ خليّةٍ من التغطية ولكلّ
محورٍ من المحاور المُعلَنة تُقاس معلومةٌ متبادلةٌ بين عضويّة الخليّة وقيمة
المحور، مصحَّحةً تصحيحَ ميلر–مادو، ثمّ تُقسَم على سقفها البنيويّ
`min(H(العضويّة), H(المحور))`. والمقامُ هو الذي كان غائبًا في القياسات
السابقة، وهو يُسقِط دفعةً واحدةً أثرَ عدّةِ الخليّة وأثرَ سَعةِ أبجديّة
المحور، فتصير الخليّةُ الصغيرةُ والكبيرةُ مقيستَين بمسطرةٍ واحدة. والصفرُ
انطباقٌ تامٌّ للجزء على الكلّ، والواحدُ تمايزٌ تامّ.

**ثانيًا: الصفريُّ مُشتَقٌّ لا مختار.** لا عتبةَ فرقٍ ههنا البتّة. تُبدَّل
قيمُ المحور على صفوف الجدول مرارًا بعددٍ مُعلَنٍ قبل القياس، فيخرج لكلّ
(خليّة، محور) مئينُها الخاصُّ من الجدول نفسِه، ويكون الفائضُ هو المرصودَ فوق
مئينه. فالسماحيّةُ صارت **دالّةً في عدّة الخليّة** لا رقمًا يُختار: أوسعَ
للصغيرة وأضيقَ للكبيرة، بالبناء لا بالتفضّل. ويُصحَّح التعدّدُ تصحيحَ هولم
على `|التغطية| × |المحاور|` اختبارًا، مُعلَنًا قبل القراءة.

**ثالثًا: المقيسُ حقلٌ لا قيمةٌ مفردة.** ما تقدّم كلُّه لا يزال جزءًا وكلًّا.
و«بنيةُ البنية» إنّما تكون في **ثبات قانونِ حقلِ الفوائض عبر المقاييس**: أن
يكون النمطُ الذي تنحرف به الأبوابُ عن الكتاب هو النمطَ الذي تنحرف به الفصولُ
عن الباب. وذلك هو `FSS`، ويُقاس باختبار عيّنتين على الحقلين.

**ورابعًا وهو الحاصلُ اليوم: العمقُ الثاني غيرُ مستردٍّ من هذه البايتات.**
عمودُ الترويسة يحمل إمّا صورةَ كتابٍ وإمّا صورةَ باب، ولا يحمل الاثنتين، فليس
في الجدول رابطُ أبوّةٍ مكتوب. وقد أُعلِنت قاعدةُ استردادٍ قبل النظر — أنّ
تصفيرَ `entry_num` حدُّ كتابٍ — ثمّ دُقِّقت فانتُقضت انتقاضًا تامًّا: كلُّ
تصفيرٍ واقعٌ **داخل** كتلةِ ترويسةٍ لا عند حدّها، وكلُّ مُستهَلِّ كتابٍ بلا
تصفير. فمسارُ `THE_LAW_IS_THE_SAME_ACROSS_THE_TWO_DEPTHS` قائمٌ في الشفرة
وغيرُ مسلوكٍ اليوم، والحكمُ إرجاءٌ يُبقي الدعوى مفتوحةً ولا يُنتقَض بها
المجال (`A_DEFERRAL_IS_NOT_A_REFUTATION_OF_THE_EQUATION`).

**خمولٌ سلطويّ**: لا ولادةَ هنا ولا حكمَ ولادةٍ ولا تجميدَ `E0`، ولا استيرادَ
من `kernel/`.
"""

from __future__ import annotations

import math
import random
from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Final

from .dal_alone_gloss import (
    THE_PROFILE_AXES,
    DalGlossEntry,
    ProfileAxis,
    whole_table_entries,
)
from .maqayis_root_table_deposit import root_table_rows

__all__ = [
    "A_DEFERRAL_IS_NOT_A_REFUTATION_OF_THE_EQUATION",
    "CellReading",
    "CoverLevel",
    "FractalStanding",
    "MAQAYIS_STRUCTURE_OF_STRUCTURE_NAMED_RESIDUALS",
    "MaqayisStructureOfStructureError",
    "NullProfile",
    "ParenthoodProbe",
    "ParenthoodStanding",
    "StructureOfStructureReading",
    "THE_DECLARED_NULL_PROFILE",
    "THE_DECLARED_PARENTHOOD_RULE",
    "assess_parenthood_recovery",
    "axis_indicator",
    "binary_entropy",
    "classify_cover_level",
    "compare_excess_fields",
    "exact_null_distribution",
    "exact_null_reading",
    "holm_rejections",
    "miller_madow_mutual_information",
    "normalised_structure",
    "run_structure_of_structure",
    "smallest_attainable_p",
    "structure_from_counts",
]


class MaqayisStructureOfStructureError(ValueError):
    """خطأٌ في بناء المعادلة أو في قراءة تغطيةٍ لا تصلح حاملًا لها."""


def binary_entropy(share: float) -> float:
    """إنتروبيا متغيّرٍ ثنائيٍّ بالبتّات، وحدُّها صفرٌ عند الطرفين."""

    if not 0.0 <= share <= 1.0:
        raise MaqayisStructureOfStructureError(
            f"نصيبٌ خارجَ [0, 1] لا يُقرَأ احتمالًا: {share}"
        )
    if share in (0.0, 1.0):
        return 0.0
    return -share * math.log2(share) - (1.0 - share) * math.log2(1.0 - share)


def miller_madow_mutual_information(
    left: Sequence[bool], right: Sequence[bool]
) -> float:
    """معلومةٌ متبادلةٌ بين ثنائيَّين بالبتّات، مطروحًا منها تحيّزُ التوصيل.

    والتصحيحُ هو حدُّ ميلر–مادو `(r-1)(c-1) / (2 n ln 2)` محسوبًا بالخلايا
    المرئيّة؛ ولذلك يجوز أن يخرج سالبًا حيث لا ارتباط، وذلك معنًى لا عطب.
    """

    if len(left) != len(right):
        raise MaqayisStructureOfStructureError(
            "لا تُقاس معلومةٌ بين متتاليتين مختلفتَي الطول"
        )
    total = len(left)
    if total == 0:
        raise MaqayisStructureOfStructureError("لا معلومةَ في متتاليةٍ خالية")
    joint = [[0, 0], [0, 0]]
    for left_value, right_value in zip(left, right, strict=True):
        joint[int(left_value)][int(right_value)] += 1
    plugin = 0.0
    for a in (0, 1):
        for b in (0, 1):
            count = joint[a][b]
            if count == 0:
                continue
            row = joint[a][0] + joint[a][1]
            column = joint[0][b] + joint[1][b]
            plugin += count / total * math.log2((count * total) / (row * column))
    seen_rows = sum(1 for a in (0, 1) if joint[a][0] + joint[a][1] > 0)
    seen_columns = sum(1 for b in (0, 1) if joint[0][b] + joint[1][b] > 0)
    bias = (seen_rows - 1) * (seen_columns - 1) / (2 * total * math.log(2))
    return plugin - bias


def structure_from_counts(
    total: int, cell_size: int, axis_positives: int, joint_hits: int
) -> float | None:
    """دالّةُ البنية مُشتقّةً من عدّ الخلايا الأربع وحدَه.

    وهذه هي الصورةُ التي يُقاس بها الصفريُّ، إذ لا تدخل في `D` من الصفوف إلّا
    أعدادُها؛ وصورةُ المتتاليتين في `normalised_structure` تُقابِلها وتُدقَّق
    بها في التجربة.
    """

    if total <= 0:
        raise MaqayisStructureOfStructureError("لا بنيةَ في جدولٍ خالٍ")
    if not 0 <= joint_hits <= min(cell_size, axis_positives):
        raise MaqayisStructureOfStructureError(
            "تقاطعٌ يجاوز أصغرَ الهامشين لا يُقرَأ عدًّا ممكنًا"
        )
    ceiling = min(
        binary_entropy(cell_size / total), binary_entropy(axis_positives / total)
    )
    if ceiling <= 0.0:
        return None
    joint = (
        (total - cell_size - axis_positives + joint_hits, axis_positives - joint_hits),
        (cell_size - joint_hits, joint_hits),
    )
    rows = (total - cell_size, cell_size)
    columns = (total - axis_positives, axis_positives)
    plugin = 0.0
    for a in (0, 1):
        for b in (0, 1):
            count = joint[a][b]
            if count == 0:
                continue
            plugin += (
                count / total * math.log2((count * total) / (rows[a] * columns[b]))
            )
    seen_rows = sum(1 for a in (0, 1) if rows[a] > 0)
    seen_columns = sum(1 for b in (0, 1) if columns[b] > 0)
    bias = (seen_rows - 1) * (seen_columns - 1) / (2 * total * math.log(2))
    return (plugin - bias) / ceiling


def normalised_structure(
    membership: Sequence[bool], indicator: Sequence[bool]
) -> float | None:
    """دالّةُ البنية `D`: معلومةٌ مصحَّحةٌ مقسومةً على سقفها البنيويّ.

    وتخرج `None` حيث السقفُ صفرٌ — أي حين تستوعب الخليّةُ الجدولَ كلَّه أو
    يسكت المحورُ عن كلّ صفٍّ — لأنّ القسمةَ هناك على صفر، والصفرُ المقروءُ
    انطباقًا تامًّا خبرٌ مُختلَقٌ من عجزِ مقياسٍ لا من مادّة.
    """

    if len(membership) != len(indicator):
        raise MaqayisStructureOfStructureError(
            "لا تُقاس بنيةٌ بين متتاليتين مختلفتَي الطول"
        )
    ceiling = min(
        binary_entropy(sum(membership) / len(membership)),
        binary_entropy(sum(indicator) / len(indicator)),
    )
    if ceiling <= 0.0:
        return None
    return miller_madow_mutual_information(membership, indicator) / ceiling


def axis_indicator(entry: DalGlossEntry, axis: ProfileAxis) -> bool:
    """قيمةُ محورٍ واحدٍ على مدخلٍ واحد، مُشتقّةً بالعدّ لا مقروءةً من حقل."""

    if axis is ProfileAxis.SHARE_MUDAAF:
        return entry.root_type == "مضاعف"
    if axis is ProfileAxis.SHARE_THULATHI:
        return entry.root_type == "ثلاثي"
    if axis is ProfileAxis.SHARE_THULATHI_MUTALL:
        return entry.root_type == "ثلاثي معتل"
    if axis is ProfileAxis.SHARE_WITH_POETRY:
        return entry.carries_poetry_evidence
    if axis is ProfileAxis.SHARE_WITH_ANY_AXIS:
        return entry.derived_axis_count > 0
    raise MaqayisStructureOfStructureError(f"محورٌ غيرُ مُعلَنٍ لا يُقاس: {axis}")


@dataclass(frozen=True, slots=True)
class NullProfile:
    """صفةُ الصفريّ مُعلَنةٌ قبل القياس: ألفا، وعدّةُ التبديل، وبذرتُها.

    وصفريُّ كلّ (خليّة، محور) لا يُبدَّل بل **يُحصى إحصاءً تامًّا**، إذ توزيعُ
    التقاطع تحت التبديل هو التوزيعُ فوقَ الهندسيُّ بعينه بهامشين مثبتين. وإنّما
    تدخل `replicates` و`seed` في مقابلة حقلَي العمقين، حيث لا إحصاءَ تامًّا.
    والفرقُ بينهما مقصود: حيث أمكن العدُّ لا تُستعمَل عيّنة، فلا تُقيَّد دقّةُ
    قيمةِ p بعدد سحباتٍ يُختار.
    """

    replicates: int
    alpha: float
    seed: int

    def __post_init__(self) -> None:
        if self.replicates < 100:
            raise MaqayisStructureOfStructureError(
                "تبديلاتٌ دون المئة لا تُخرِج قيمةَ p يُعتَدّ بها"
            )
        if not 0.0 < self.alpha < 0.5:
            raise MaqayisStructureOfStructureError(
                f"ألفا خارجَ (0, 0.5) لا تُقرَأ مستوى دلالة: {self.alpha}"
            )


THE_DECLARED_NULL_PROFILE: Final[NullProfile] = NullProfile(
    replicates=400, alpha=0.05, seed=20260920
)
"""الصفريُّ مُعلَنٌ ههنا قبل أيّ قراءة، ولا يُبدَّل بعد رؤية حكمٍ منه."""


def _log_choose(total: int, chosen: int) -> float:
    """لوغاريتمُ عددِ التوافيق، محسوبًا بدالّة غاما لئلّا تُبنى أعدادٌ ضخمة."""

    if chosen < 0 or chosen > total:
        return -math.inf
    return (
        math.lgamma(total + 1)
        - math.lgamma(chosen + 1)
        - math.lgamma(total - chosen + 1)
    )


def exact_null_distribution(
    total: int, cell_size: int, axis_positives: int
) -> tuple[tuple[float, float], ...]:
    """توزيعُ `D` الصفريُّ تامًّا: كلُّ تقاطعٍ ممكنٍ ووزنُه فوقَ الهندسيّ.

    وهو صفريُّ التبديل بعينه لا تقريبَه، إذ تثبيتُ الهامشين يجعل التقاطعَ
    فوقَ هندسيٍّ بالضبط. فلا بذرةَ ههنا ولا عدُّ سحبات، ولا أرضيّةَ دقّةٍ
    تمنع قيمةَ p من النزول تحت عتبةٍ مُصحَّحة.
    """

    lowest = max(0, cell_size + axis_positives - total)
    highest = min(cell_size, axis_positives)
    base = _log_choose(total, cell_size)
    out: list[tuple[float, float]] = []
    for hits in range(lowest, highest + 1):
        weight = math.exp(
            _log_choose(axis_positives, hits)
            + _log_choose(total - axis_positives, cell_size - hits)
            - base
        )
        value = structure_from_counts(total, cell_size, axis_positives, hits)
        if value is not None:
            out.append((value, weight))
    return tuple(out)


def exact_null_reading(
    total: int,
    cell_size: int,
    axis_positives: int,
    observed: float | None,
    alpha: float = 0.05,
) -> tuple[float | None, float]:
    """المئينُ المُشتَقُّ وقيمةُ p، مأخوذين من التوزيع التامّ لا من عيّنة."""

    distribution = exact_null_distribution(total, cell_size, axis_positives)
    if not distribution or observed is None:
        return None, 1.0
    ordered = sorted(distribution, key=lambda pair: -pair[0])
    p_value = sum(weight for value, weight in ordered if value >= observed)
    quantile = ordered[0][0]
    carried = 0.0
    for value, weight in ordered:
        carried += weight
        if carried > alpha:
            quantile = value
            break
    return quantile, min(1.0, p_value)


def smallest_attainable_p(total: int, cell_size: int, axis_positives: int) -> float:
    """أصغرُ قيمةِ p يبلغها هذا الحاملُ ولو بلغ أقصى تمايزٍ ممكن.

    وهي وزنُ أقصى قيمةٍ في التوزيع التامّ. فإن جاوزت العتبةَ المُصحَّحةَ فتلك
    قراءةٌ **عاجزةٌ بالبناء**: لا يُرفَض فيها شيءٌ مهما كانت المادّة، فاجتيازُها
    ليس شهادةً على انطباق. وتُعَدّ ولا تُطوى في نجاح.
    """

    distribution = exact_null_distribution(total, cell_size, axis_positives)
    if not distribution:
        return 1.0
    return min(1.0, max(distribution, key=lambda pair: pair[0])[1])


def holm_rejections(
    p_values: Sequence[float], alpha: float = THE_DECLARED_NULL_PROFILE.alpha
) -> tuple[bool, ...]:
    """تصحيحُ هولم على جملة الاختبارات، مُعلَنًا قبل قراءة أيّ حكم.

    وهو يوقف الرفضَ عند أوّل اختبارٍ لا يجتاز عتبتَه، فلا يُرفَض ما بعده ولو
    صغُرت قيمتُه — وذلك شرطُ ضبطِ الخطأ العائليّ، لا تشدّدٌ زائد.
    """

    if not p_values:
        return ()
    order = sorted(range(len(p_values)), key=lambda index: p_values[index])
    out = [False] * len(p_values)
    total = len(p_values)
    for position, index in enumerate(order):
        if p_values[index] <= alpha / (total - position):
            out[index] = True
        else:
            break
    return tuple(out)


@dataclass(frozen=True, slots=True)
class CellReading:
    """قراءةُ (خليّة، محور): دالّةُ البنية، ومئينُها، وقيمةُ p التبديليّة."""

    cell_label: str
    axis: ProfileAxis
    size: int
    structure: float | None
    null_quantile: float | None
    p_value: float
    floor_p: float

    @property
    def is_powerless(self) -> bool:
        """خليّةٌ سقفُها صفرٌ لا تشهد لانطباقٍ ولا عليه."""

        return self.structure is None

    def is_unresolvable_at(self, threshold: float) -> bool:
        """هل يعجز هذا الحاملُ عن بلوغ العتبة المُصحَّحة مهما كانت المادّة؟"""

        return self.floor_p > threshold

    @property
    def excess(self) -> float | None:
        """الفائضُ فوق المئين المُشتَقّ، لا فوق عتبةٍ مختارة."""

        if self.structure is None or self.null_quantile is None:
            return None
        return self.structure - self.null_quantile


class CoverLevel(Enum):
    """صورةُ الترويسة، مُصنَّفةً بشكلها وحدَه لا بما تحته من صفوف."""

    BOOK_FORM = "صورةُ_كتاب"
    SECTION_FORM = "صورةُ_باب"
    UNNAMED = "بلا_ترويسة"


def classify_cover_level(header: str) -> CoverLevel:
    """صنِّف ترويسةً بشكلها؛ والقاعدةُ مُعلَنةٌ ولا تنظر إلى عمودٍ مقيس."""

    text = header.strip()
    if not text:
        return CoverLevel.UNNAMED
    if text.startswith("كتاب"):
        return CoverLevel.BOOK_FORM
    if text.startswith("باب"):
        return CoverLevel.SECTION_FORM
    return CoverLevel.UNNAMED


THE_DECLARED_PARENTHOOD_RULE: Final[str] = (
    "تصفيرُ عمود entry_num حدُّ كتابٍ: فيقع عند حدّ كتلةِ ترويسة، وتكون "
    "ترويستُه صورةَ كتاب، ويكون لكلّ مُستهَلِّ كتابٍ تصفيرُه. ولا تُستردّ "
    "أبوّةٌ إلّا بانتفاء المخالفات الثلاث جميعًا."
)
"""قاعدةُ استردادِ العمق الثاني، مُعلَنةً بحروفها قبل عدّ مخالفةٍ واحدة."""


class ParenthoodStanding(Enum):
    """حالُ استرداد العمق الثاني من البايتات، بثلاث قيمٍ لا بقيمتين."""

    RECOVERED = "مستردٌّ_بقاعدةٍ_مُدقَّقة"
    REFUTED = "منقوضٌ_بعدِّ_مخالفاته"


@dataclass(frozen=True, slots=True)
class ParenthoodProbe:
    """حصيلةُ مِسبار الأبوّة: المخالفاتُ الثلاثُ معدودةً، وحكمُها."""

    resets: int
    book_starts: int
    resets_off_a_header_boundary: int
    resets_not_on_a_book_header: int
    book_starts_without_a_reset: int

    @property
    def violations(self) -> int:
        """جملةُ المخالفات؛ والقاعدةُ لا تُردّ إلّا بانتفائها كلِّها."""

        return (
            self.resets_off_a_header_boundary
            + self.resets_not_on_a_book_header
            + self.book_starts_without_a_reset
        )

    @property
    def standing(self) -> ParenthoodStanding:
        """حكمُ المِسبار، مُشتقًّا من العدّ لا مكتوبًا في حقل."""

        if self.violations == 0:
            return ParenthoodStanding.RECOVERED
        return ParenthoodStanding.REFUTED

    @property
    def recovers_a_second_depth(self) -> bool:
        """هل فُتِح عمقٌ ثانٍ تُقاس عليه المعادلة؟"""

        return self.standing is ParenthoodStanding.RECOVERED


def assess_parenthood_recovery() -> ParenthoodProbe:
    """دقِّق قاعدةَ الأبوّة المُعلَنة على البايتات، وأخرِج مخالفاتها معدودة."""

    rows = root_table_rows()
    numbers = [int(row["entry_num"]) for row in rows]
    headers = [row["chapter_header"].strip() for row in rows]
    resets = [
        index
        for index in range(1, len(numbers))
        if numbers[index] <= numbers[index - 1]
    ]
    boundaries = {
        index
        for index in range(1, len(headers))
        if headers[index] != headers[index - 1]
    }
    book_starts = {
        index
        for index in boundaries
        if classify_cover_level(headers[index]) is CoverLevel.BOOK_FORM
    }
    return ParenthoodProbe(
        resets=len(resets),
        book_starts=len(book_starts),
        resets_off_a_header_boundary=sum(
            1 for index in resets if index not in boundaries
        ),
        resets_not_on_a_book_header=sum(
            1
            for index in resets
            if classify_cover_level(headers[index]) is not CoverLevel.BOOK_FORM
        ),
        book_starts_without_a_reset=sum(
            1 for index in book_starts if index not in resets
        ),
    )


class FractalStanding(Enum):
    """حالُ معادلة بنيةِ البنية، بثلاث قيمٍ والإرجاءُ منها لا يُنتقَض به."""

    THE_LAW_IS_THE_SAME_ACROSS_THE_TWO_DEPTHS = "قائمةٌ_على_عمقين_مُدقَّقين"
    THE_LAW_DIFFERS_ACROSS_THE_TWO_DEPTHS = "منقوضةٌ_بفرقٍ_بين_الحقلين"
    DEFERRED_FOR_WANT_OF_A_SECOND_DEPTH = "مُرجأةٌ_لانعدام_عمقٍ_ثانٍ"


def compare_excess_fields(
    first: Sequence[float],
    second: Sequence[float],
    profile: NullProfile = THE_DECLARED_NULL_PROFILE,
) -> float:
    """قابِل حقلَي فوائضَ باختبار تبديلٍ على علامة العمق، وأخرِج قيمة p.

    والمقيسُ فرقُ الوسطين مُطلَقًا؛ وتُبدَّل علاماتُ العمق على الاتّحاد مرارًا،
    فيُقرَأ نصيبُ التبديلات التي بلغت الفرقَ المرصودَ أو جاوزته.
    """

    if len(first) < 2 or len(second) < 2:
        raise MaqayisStructureOfStructureError(
            "لا يُقابَل حقلٌ فيه أقلُّ من قيمتين؛ وحقلٌ كهذا لا قانونَ له"
        )
    pool = list(first) + list(second)
    cut = len(first)

    def separation(values: Sequence[float]) -> float:
        left = sum(values[:cut]) / cut
        right = sum(values[cut:]) / (len(values) - cut)
        return abs(left - right)

    observed = separation(pool)
    rng = random.Random(profile.seed)
    hits = 0
    for _ in range(profile.replicates):
        shuffled = pool[:]
        rng.shuffle(shuffled)
        if separation(shuffled) >= observed:
            hits += 1
    return (hits + 1) / (profile.replicates + 1)


def _cell_readings(
    entries: Sequence[DalGlossEntry], profile: NullProfile
) -> tuple[CellReading, ...]:
    """اقرأ كلَّ (خليّة، محور) بدالّة البنية وبصفريٍّ مُحصًى تامًّا لا مُعايَن."""

    total = len(entries)
    labels = sorted({entry.chapter_header for entry in entries if entry.chapter_header})
    if not labels:
        raise MaqayisStructureOfStructureError(
            "تغطيةٌ بلا خليّةٍ مُسمّاةٍ لا تُقاس عليها بنية"
        )
    indicators = {
        axis: [axis_indicator(entry, axis) for entry in entries]
        for axis in THE_PROFILE_AXES
    }
    memberships = {
        label: [entry.chapter_header == label for entry in entries] for label in labels
    }
    readings: list[CellReading] = []
    for label in labels:
        membership = memberships[label]
        size = sum(membership)
        for axis in THE_PROFILE_AXES:
            values = indicators[axis]
            positives = sum(values)
            hits = sum(
                1
                for flag, value in zip(membership, values, strict=True)
                if flag and value
            )
            observed = structure_from_counts(total, size, positives, hits)
            quantile, p_value = exact_null_reading(
                total, size, positives, observed, profile.alpha
            )
            floor = smallest_attainable_p(total, size, positives)
            readings.append(
                CellReading(
                    cell_label=label,
                    axis=axis,
                    size=size,
                    structure=observed,
                    null_quantile=quantile,
                    p_value=p_value,
                    floor_p=floor,
                )
            )
    return tuple(readings)


@dataclass(frozen=True, slots=True)
class StructureOfStructureReading:
    """قراءةُ المعادلة كلِّها: حقلُ الفوائض، ومِسبارُ الأبوّة، والحال."""

    readings: tuple[CellReading, ...]
    parenthood: ParenthoodProbe
    profile: NullProfile

    def __post_init__(self) -> None:
        if not self.readings:
            raise MaqayisStructureOfStructureError("حقلٌ خالٍ لا يُقرَأ انطباقًا ولا تمايزًا")

    @property
    def rejections(self) -> tuple[bool, ...]:
        """رفضُ هولم على `|التغطية| × |المحاور|` اختبارًا، بترتيب القراءات."""

        return holm_rejections([r.p_value for r in self.readings], self.profile.alpha)

    @property
    def distinguished_cells(self) -> tuple[str, ...]:
        """الخلايا التي تمايز فيها محورٌ واحدٌ فأكثرُ بعد تصحيح التعدّد."""

        out: list[str] = []
        for reading, rejected in zip(self.readings, self.rejections, strict=True):
            if rejected and reading.cell_label not in out:
                out.append(reading.cell_label)
        return tuple(sorted(out))

    @property
    def cells_distinguished_before_correction(self) -> tuple[str, ...]:
        """الخلايا التي تتمايز لو قُرئت قيمُ p عاريةً عن تصحيح التعدّد.

        وتُعرَض معها لا بدلها: تصحيحُ هولم مُعلَنٌ قبل القراءة ولا يُرخى بعدها،
        لكنّ كتمانَ الفرق بين القراءتين يُخفي أنّ حكمَ بعض الخلايا دالّةٌ في
        التصحيح. فيُعرَض العددان ويُقرأ أيُّهما بيّنٌ من أيّ.
        """

        out: list[str] = []
        for reading in self.readings:
            if reading.p_value <= self.profile.alpha and reading.cell_label not in out:
                out.append(reading.cell_label)
        return tuple(sorted(out))

    @property
    def cells(self) -> tuple[str, ...]:
        """خلايا التغطية مُشتقّةً من القراءات لا مكتوبةً في حقل."""

        return tuple(sorted({reading.cell_label for reading in self.readings}))

    @property
    def self_similar_cells(self) -> tuple[str, ...]:
        """الخلايا التي انطبقت على كلّها: لا محورَ فيها تجاوز صفريَّه."""

        distinguished = set(self.distinguished_cells)
        return tuple(cell for cell in self.cells if cell not in distinguished)

    @property
    def powerless_readings(self) -> int:
        """قراءاتٌ سقفُها صفرٌ فلا تشهد؛ تُعَدّ ولا تُطوى في نجاح."""

        return sum(1 for reading in self.readings if reading.is_powerless)

    @property
    def corrected_threshold(self) -> float:
        """أضيقُ عتبةٍ في سُلَّم هولم، وهي التي يُقاس بها العجزُ البنيويّ."""

        return self.profile.alpha / len(self.readings)

    @property
    def unresolvable_readings(self) -> int:
        """قراءاتٌ لا تبلغ العتبةَ المُصحَّحةَ ولو بلغت أقصى تمايزٍ ممكن."""

        return sum(
            1
            for reading in self.readings
            if reading.is_unresolvable_at(self.corrected_threshold)
        )

    @property
    def cells_with_no_resolvable_axis(self) -> tuple[str, ...]:
        """خلايا عجز فيها كلُّ محورٍ عن العتبة؛ انطباقُها عجزٌ لا شهادة."""

        out: list[str] = []
        for cell in self.cells:
            axes = [r for r in self.readings if r.cell_label == cell]
            if all(r.is_unresolvable_at(self.corrected_threshold) for r in axes):
                out.append(cell)
        return tuple(out)

    @property
    def excess_field(self) -> tuple[float, ...]:
        """حقلُ الفوائض عند هذا العمق، وهو مادّةُ المقابلة بين المقاييس."""

        return tuple(
            reading.excess for reading in self.readings if reading.excess is not None
        )

    @property
    def standing(self) -> FractalStanding:
        """حالُ المعادلة؛ وبغير عمقٍ ثانٍ مُدقَّقٍ لا تُقرَأ قائمةً ولا منقوضة."""

        if not self.parenthood.recovers_a_second_depth:
            return FractalStanding.DEFERRED_FOR_WANT_OF_A_SECOND_DEPTH
        raise MaqayisStructureOfStructureError(
            "استُردَّ عمقٌ ثانٍ ولم تُقابَل حقولُه؛ ولا يُحكَم بغير مقابلة"
        )

    def structure_of(self, cell_label: str, axis: ProfileAxis) -> float | None:
        """دالّةُ البنية لخليّةٍ ومحورٍ بعينهما، مقروءةً من القراءات."""

        for reading in self.readings:
            if reading.cell_label == cell_label and reading.axis is axis:
                return reading.structure
        raise MaqayisStructureOfStructureError(
            f"لا قراءةَ لخليّة «{cell_label}» على المحور {axis}"
        )


def run_structure_of_structure(
    profile: NullProfile = THE_DECLARED_NULL_PROFILE,
) -> StructureOfStructureReading:
    """أجرِ المعادلةَ كلَّها على البايتات المُبصَّمة، وأخرِج حالَها أيًّا كان."""

    return StructureOfStructureReading(
        readings=_cell_readings(whole_table_entries(), profile),
        parenthood=assess_parenthood_recovery(),
        profile=profile,
    )


A_DEFERRAL_IS_NOT_A_REFUTATION_OF_THE_EQUATION: Final[str] = (
    "A_DEFERRAL_IS_NOT_A_REFUTATION_OF_THE_EQUATION: إرجاءُ المعادلة لانعدام "
    "عمقٍ ثانٍ يُبقيها مفتوحةً ولا يُنتقَض بها المجال. فالذي انتُقِض قاعدةُ "
    "استردادٍ بعينها لا الدعوى، وبايتاتٌ أخرى تحمل الأبوّةَ مكتوبةً قد تفتح "
    "العمقَ الثاني من غير تبديل حرفٍ في هذه الصياغة."
)

A_NORMALISED_VALUE_IS_NOT_A_CAUSE: Final[str] = (
    "A_NORMALISED_VALUE_IS_NOT_A_CAUSE: دالّةُ البنية تقيس مقدارَ التمايز ولا "
    "تُعيّن مصدرَه. وقد فُصِلت ثلاثةُ حسابٍ للانحراف في وحدةٍ أخرى وبقي حسابُ "
    "التأليف بلا مِسبار، ولا شيءَ ههنا يُرقّيه."
)

THE_AXES_ARE_DECLARED_AND_NOT_EXHAUSTIVE: Final[str] = (
    "THE_AXES_ARE_DECLARED_AND_NOT_EXHAUSTIVE: المحاورُ خمسةٌ مُعلَنةٌ قبل "
    "القياس، وانطباقُ خليّةٍ عليها جميعًا لا يمتدّ إلى محورٍ لم يُقَس. فالخليّةُ "
    "المنطبقةُ ههنا منطبقةٌ على هذه الخمسة لا على كلّ وصفٍ ممكن."
)

TWO_DEPTHS_WOULD_NOT_MAKE_A_FRACTAL: Final[str] = (
    "TWO_DEPTHS_WOULD_NOT_MAKE_A_FRACTAL: لو استُردَّ العمقُ الثاني لقامت "
    "مقابلةٌ بين مقياسين اثنين لا أكثر، والتكرارُ عبر مقياسين ليس فراكتاليّةً. "
    "فاسمُ المعادلة وصفٌ لصورتها لا دعوى تشابهٍ بلا حدّ."
)

THE_FLAT_COVER_MIXES_TWO_LEVELS: Final[str] = (
    "THE_FLAT_COVER_MIXES_TWO_LEVELS: تغطيةُ هذا الجدول تخلط ترويساتِ كتبٍ "
    "بترويسات أبواب في مستوًى واحد، وقد قيست القياساتُ السابقةُ كلُّها على هذا "
    "الخليط. فبعضُ تبعثرها قد يكون أثرَ الخلط لا أثرَ المادّة، وذلك غيرُ "
    "مفصولٍ ههنا."
)

A_POWERLESS_READING_IS_COUNTED_AND_NOT_PASSED: Final[str] = (
    "A_POWERLESS_READING_IS_COUNTED_AND_NOT_PASSED: قراءةٌ سقفُها صفرٌ لا تُقرَأ "
    "انطباقًا؛ تُعَدّ وتُسمّى، ولا تُحسَب شهادةً في صفّ الدعوى ولا عليها."
)

MAQAYIS_STRUCTURE_OF_STRUCTURE_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "A_DEFERRAL_IS_NOT_A_REFUTATION_OF_THE_EQUATION": (
        A_DEFERRAL_IS_NOT_A_REFUTATION_OF_THE_EQUATION
    ),
    "A_NORMALISED_VALUE_IS_NOT_A_CAUSE": A_NORMALISED_VALUE_IS_NOT_A_CAUSE,
    "THE_AXES_ARE_DECLARED_AND_NOT_EXHAUSTIVE": (
        THE_AXES_ARE_DECLARED_AND_NOT_EXHAUSTIVE
    ),
    "TWO_DEPTHS_WOULD_NOT_MAKE_A_FRACTAL": TWO_DEPTHS_WOULD_NOT_MAKE_A_FRACTAL,
    "THE_FLAT_COVER_MIXES_TWO_LEVELS": THE_FLAT_COVER_MIXES_TWO_LEVELS,
    "A_POWERLESS_READING_IS_COUNTED_AND_NOT_PASSED": (
        A_POWERLESS_READING_IS_COUNTED_AND_NOT_PASSED
    ),
}
"""ما لا تُثبِته هذه المعادلةُ مُسمًّى باسمه، لا مطويًّا في حكمٍ عامّ."""
