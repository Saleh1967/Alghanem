"""قيدُ التجاور بين مخارج الحروف، مقيسًا على الجذور المُودَعة وحدَها.

قيل إنّ العربيّة تتجنّب تماثلَ المخرج بين الحرفَين الأوّل والثاني من الجذر
تجنّبًا شبهَ تامّ، وتسمح به بين الثاني والثالث؛ وإنّ القافَ مخصوصةٌ بقيدٍ في
جيرانها. والقيدُ قائمٌ في هذه البايتات فعلًا، وأمّا الأسيميّةُ الموضعيّةُ
والخصوصيّةُ القافيّةُ فتسقطان عند التدقيق. وهذه الوحدة تفصل::

    AConstraintOnNeighbours  != AnAccountOfHowOftenALetterOccurs
    AGeminateSpelling        != ASecondPositionAgreement
    TwoSeparateZScores       != ATestOfTheDifferenceBetweenThem
    ALetterAtTheFloor        != ALetterSingledOutByTheFloor

**أوّلًا: الإحصاءُ يُسقِط أزواجَ الحرف الواحد.** الجذرُ المضاعفُ مكتوبٌ في هذا
المُودَع مُظهَرَ التضعيف (`أجج` بإزاء `أج`)، فحرفُه الثاني والثالثُ حرفٌ واحد.
وتماثلُ المخرج في مثل ذلك مُعطًى بالكتابة لا مقيسًا في المادّة. فالمقيسُ ههنا
نسبةُ تماثل المخرج **بين الحرفَين المختلفَين** وحدَها، ويُعرَض الخامُّ بجانبها
لا بدلَها ليُرى مقدارُ ما يصنعه الاصطلاح.

**ثانيًا: الأسيميّةُ تُختبَر مباشرةً لا بمقابلة قيمتَي z.** قيمتان منفصلتان
في وجه صفريَّين ليستا اختبارًا للفرق بينهما؛ وz تكبر بكبر العدّة وحدَها. فيُقاس
الفرقُ نفسُه في وجه صفريٍّ واحد، ويخرج حكمٌ ثلاثيّ: الأوّلُ أشدّ، أو الثاني
أشدّ، أو **لا يُفرَّق بينهما**. والحاصلُ على هذه البايتات هو الثالث.

**ثالثًا: خصوصيّةُ حرفٍ دعوى انفرادٍ لا دعوى صفر.** يُرتَّب كلُّ حرفٍ بنسبة
مرصودِه إلى متوقَّعه، والمتوقَّعُ محسوبٌ من الهوامش حسابًا تامًّا لا مسحوبًا.
فلا يُقال «القافُ مقيَّدة» حتّى تكون **وحدَها** في قاع الترتيب. وهي ليست
وحدَها.

**رابعًا: القيدُ دعوى مستقرّةٌ لا كشفٌ ههنا.** تنافرُ الجذر مذكورٌ عند
غرينبرغ منذ ١٩٥٠. فظهورُه في هذه البايتات فحصُ سلامةٍ للاستخراج، وإليه يُقرأ
(`THE_CONSTRAINT_IS_A_STANDING_CLAIM_AND_NOT_A_FINDING_HERE`).

**خمولٌ سلطويّ**: لا ولادةَ هنا ولا حكمَ ولادةٍ ولا تجميدَ `E0`، ولا استيرادَ
من `kernel/`.
"""

from __future__ import annotations

import math
import operator
import random
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Final

from .maqayis_root_table_deposit import root_table_rows

__all__ = [
    "ADJACENCY_CONSTRAINT_NAMED_RESIDUALS",
    "AdjacencyConstraintReading",
    "AdjacentPosition",
    "AsymmetryStanding",
    "LetterDepression",
    "MaqayisAdjacencyConstraintError",
    "NullProfile",
    "PairReading",
    "QafStanding",
    "THE_DECLARED_NULL_PROFILE",
    "THE_DECLARED_PLACE_CLASSES",
    "THE_LETTER_FOLD",
    "expected_same_place_rate",
    "fold_letter",
    "folded_roots",
    "holm_rejections",
    "place_of",
    "run_adjacency_constraint",
    "same_place_rate",
]


class MaqayisAdjacencyConstraintError(RuntimeError):
    """يُرفَع حين يُطلَب من هذه الوحدة حكمٌ لا تحمله بايتاتُها."""


THE_DECLARED_PLACE_CLASSES: Final[Mapping[str, str]] = {
    "حلقٌ أقصى": "ءه",
    "حلقٌ وسط": "عح",
    "حلقٌ أدنى": "غخ",
    "لهويّ": "قك",
    "شجريّ": "جشي",
    "ضاديّ": "ض",
    "ذلقيّ": "لنر",
    "نطعيّ": "طدت",
    "أسليّ": "صزس",
    "لثويّ": "ظذث",
    "شفويّ": "فبمو",
}
"""أحدَ عشرَ مخرجًا مُعلَنةً قبل القياس، تستغرق الثمانيةَ والعشرين حرفًا.

وهي **تصنيفٌ مُعلَنٌ لا حاصر**: سيبويه يعدّ ستّةَ عشرَ مخرجًا، وخشونةُ التصنيف
ترفع الأساسَ المتوقَّعَ وتُضخِّم الانخفاضَ الظاهر. فالعددُ داخلٌ في الحكم،
ومُسمًّى في البقايا (`THE_ELEVEN_PLACES_ARE_DECLARED_AND_NOT_FORCED`).
"""

_PLACE_OF: Final[dict[str, str]] = {
    letter: place
    for place, letters in THE_DECLARED_PLACE_CLASSES.items()
    for letter in letters
}

THE_LETTER_FOLD: Final[Mapping[str, str]] = {
    "أ": "ء",
    "إ": "ء",
    "آ": "ء",
    "ؤ": "ء",
    "ئ": "ء",
    "ا": "ء",
    "ى": "ي",
    "ة": "ت",
}
"""طَيُّ صور الهمزة والألف والياء والتاء إلى أصولها قبل القياس.

وهو طيٌّ مُعلَنٌ قبل النظر، وأثرُه أنّ كلَّ صور الهمزة تُعَدّ حرفًا واحدًا في
«حلقٍ أقصى». وما لا يُطوى ولا يُصنَّف يُسقِط جذرَه كلَّه ويُعَدّ إسقاطُه.
"""


def fold_letter(letter: str) -> str:
    """يَرُدّ الحرفَ إلى صورته المطويّة، أو يُعيده كما هو إن لم يكن مطويًّا."""

    if len(letter) != 1:
        raise MaqayisAdjacencyConstraintError("الطيُّ يقع على حرفٍ واحدٍ لا أكثر.")
    return THE_LETTER_FOLD.get(letter, letter)


def place_of(letter: str) -> str:
    """مخرجُ الحرف المطويّ، أو رفعٌ إن كان خارجَ التصنيف المُعلَن."""

    folded = fold_letter(letter)
    place = _PLACE_OF.get(folded)
    if place is None:
        raise MaqayisAdjacencyConstraintError(
            f"الحرفُ {letter!r} خارجُ المخارج المُعلَنة، فلا يُقاس صمتًا."
        )
    return place


def folded_roots() -> tuple[tuple[str, str, str], ...]:
    """الجذورُ الثلاثيّةُ المميَّزةُ مطويّةً، مرتَّبةً ترتيبًا ثابتًا.

    ويُقرَأ `root_full` لا `root_display`، فالمضاعفُ فيه مُظهَرُ التضعيف،
    وإظهارُه هو المحكُّ الذي تقوم عليه هذه الوحدة.
    """

    seen: set[str] = set()
    ordered: list[str] = []
    for row in root_table_rows():
        root = str(row["root_full"])
        if root not in seen:
            seen.add(root)
            ordered.append(root)
    ordered.sort()
    roots: list[tuple[str, str, str]] = []
    for root in ordered:
        folded = tuple(fold_letter(letter) for letter in root)
        if len(folded) != 3:
            continue
        if any(letter not in _PLACE_OF for letter in folded):
            continue
        roots.append((folded[0], folded[1], folded[2]))
    return tuple(roots)


class AdjacentPosition(Enum):
    """موضعُ الزوج المتجاور داخل الجذر."""

    FIRST_PAIR = "الحرفان الأوّل والثاني"
    SECOND_PAIR = "الحرفان الثاني والثالث"


def same_place_rate(
    left: Sequence[str], right: Sequence[str], *, drop_identical: bool = True
) -> tuple[int, int]:
    """عددُ الأزواج المتماثلةِ المخرجِ وعدّةُ الأزواج المقروءة.

    ويُسقَط زوجُ الحرف الواحد افتراضًا، لأنّ تماثلَ مخرجه مُعطًى بالهويّة لا
    مقيسٌ في المادّة. وقراءتُه بلا إسقاطٍ مُتاحةٌ لتُرى كلفةُ الاصطلاح.
    """

    if len(left) != len(right):
        raise MaqayisAdjacencyConstraintError(
            "الزوجان يُقرآن على عدّةٍ واحدة، فلا يُقابَل عمودان مختلفا الطول."
        )
    if not left:
        raise MaqayisAdjacencyConstraintError("لا قراءةَ على عمودٍ خالٍ.")
    same = 0
    read = 0
    for first, second in zip(left, right, strict=True):
        if drop_identical and first == second:
            continue
        read += 1
        if place_of(first) == place_of(second):
            same += 1
    return same, read


def expected_same_place_rate(
    left: Sequence[str], right: Sequence[str], *, drop_identical: bool = True
) -> float:
    """المتوقَّعُ تحت استقلال العمودين، محسوبًا من الهوامش حسابًا تامًّا.

    ولا يُسحَب هذا المتوقَّعُ سحبًا: احتمالُ أن يقع حرفٌ من العمود الأيمن في
    مخرج نظيره من الأيسر محسوبٌ من عدّتَي المخرجين مباشرةً. وهو الذي تُقاس به
    نسبةُ الانخفاض لكلّ حرفٍ على حدة، فلا يدخل بذرٌ في ترتيب الحروف.
    """

    if len(left) != len(right) or not left:
        raise MaqayisAdjacencyConstraintError(
            "المتوقَّعُ يُقاس على عمودين متساويَين غيرِ خاليين."
        )
    total = len(left)
    right_letters: dict[str, int] = {}
    right_places: dict[str, int] = {}
    for letter in right:
        right_letters[letter] = right_letters.get(letter, 0) + 1
        place = place_of(letter)
        right_places[place] = right_places.get(place, 0) + 1
    same = 0.0
    read = 0.0
    for letter in left:
        identical = right_letters.get(letter, 0) / total
        agreeing = right_places.get(place_of(letter), 0) / total
        if drop_identical:
            read += 1.0 - identical
            same += agreeing - identical
        else:
            read += 1.0
            same += agreeing
    if read <= 0.0:
        raise MaqayisAdjacencyConstraintError("عدّةٌ متوقَّعةٌ صفرٌ لا تُقسَم عليها نسبة.")
    return same / read


@dataclass(frozen=True)
class NullProfile:
    """صفةُ الصفريّ مُعلَنةً قبل القياس: عدّتُه، وسماحيّتُه، وبذرُه."""

    replicates: int
    alpha: float
    seed: int

    def __post_init__(self) -> None:
        if self.replicates < 1000:
            raise MaqayisAdjacencyConstraintError(
                "عدّةٌ دون الألف تُقرِّب أرضيّةَ الدقّة من العتبة المُصحَّحة، "
                "فيموت الاختبارُ قبل أن يُقاس به شيء."
            )
        if not 0.0 < self.alpha < 0.5:
            raise MaqayisAdjacencyConstraintError("سماحيّةٌ خارجَ (0, 0.5) لا تُخرِج حكمًا.")

    @property
    def smallest_attainable_p(self) -> float:
        """أصغرُ قيمةِ p تبلغها هذه العدّة، وهي أرضيّةُ دقّتها لا قياس."""

        return 1.0 / (self.replicates + 1)


THE_DECLARED_NULL_PROFILE: Final[NullProfile] = NullProfile(
    replicates=2000, alpha=0.05, seed=20260920
)
"""الصفريُّ المُعلَن: ألفا تبديلةٍ مضاعفة، وسماحيّةٌ خمسٌ من المئة، وبذرٌ ثابت.

وأرضيّةُ دقّته 1/2001 ≈ 0.0005، وأضيقُ عتبةٍ في سُلَّم هولم على الاختبارات
الثلاثة المُعلَنة 0.05/3 ≈ 0.0167. فالرفضُ مُتاحٌ بالبناء، وليس هذا اختبارًا
ميّتًا تُقرَأ أرضيّتُه نتيجةً.
"""


def holm_rejections(
    p_values: Sequence[float], *, alpha: float = 0.05
) -> tuple[bool, ...]:
    """تصحيحُ هولم: يقف عند أوّل إخفاق فلا يُرفَض ما بعده مهما صغُر."""

    ordered = sorted(range(len(p_values)), key=lambda index: p_values[index])
    rejected = [False] * len(p_values)
    remaining = len(p_values)
    for rank, index in enumerate(ordered):
        if p_values[index] <= alpha / (remaining - rank):
            rejected[index] = True
        else:
            break
    return tuple(rejected)


@dataclass(frozen=True)
class PairReading:
    """قراءةُ موضعٍ واحد: مرصودُه، ومتوقَّعُه المسحوب، وقيمتُه الاحتماليّة."""

    position: AdjacentPosition
    observed_same: int
    observed_pairs: int
    identical_pairs: int
    null_mean: float
    null_sd: float
    p_value: float
    raw_same: int
    raw_pairs: int

    @property
    def rate(self) -> float:
        """نسبةُ تماثل المخرج بين الحرفَين المختلفَين."""

        return self.observed_same / self.observed_pairs

    @property
    def raw_rate(self) -> float:
        """النسبةُ الخامّةُ قبل إسقاط أزواج الحرف الواحد."""

        return self.raw_same / self.raw_pairs

    @property
    def z_score(self) -> float:
        """بُعدُ المرصود عن متوسّط صفريّه بوحدات انحرافه."""

        if self.null_sd <= 0.0:
            raise MaqayisAdjacencyConstraintError("صفريٌّ بلا تبعثرٍ لا يُقاس به بُعد.")
        return (self.rate - self.null_mean) / self.null_sd

    @property
    def depression_ratio(self) -> float:
        """نسبةُ المرصود إلى متوقَّعه: دونَ الواحد قيدٌ، وفوقَه ميلٌ إلى التماثل."""

        if self.null_mean <= 0.0:
            raise MaqayisAdjacencyConstraintError("متوقَّعٌ صفرٌ لا تُقاس إليه نسبة.")
        return self.rate / self.null_mean


class AsymmetryStanding(Enum):
    """حكمُ الأسيميّة الموضعيّة، مقيسًا على الفرق نفسِه لا على قيمتَي z."""

    THE_FIRST_PAIR_IS_MORE_CONSTRAINED = "الزوجُ الأوّلُ أشدُّ تقييدًا"
    THE_SECOND_PAIR_IS_MORE_CONSTRAINED = "الزوجُ الثاني أشدُّ تقييدًا"
    THE_TWO_POSITIONS_ARE_NOT_DISTINGUISHED = "لا يُفرَّق بين الموضعين"


class QafStanding(Enum):
    """حكمُ خصوصيّة القاف: انفرادٌ في القاع، أو تعادلٌ فيه، أو غيابٌ عنه."""

    SINGLED_OUT_AT_THE_FLOOR = "منفردةٌ في قاع الترتيب"
    TIED_AT_THE_FLOOR = "متعادلةٌ في القاع مع غيرها"
    NOT_AT_THE_FLOOR = "ليست في القاع"


@dataclass(frozen=True)
class LetterDepression:
    """نسبةُ انخفاض حرفٍ واحدٍ في الزوج الأوّل، مرصودةً إلى متوقَّعٍ تامّ."""

    letter: str
    observed: int
    neighbours: int
    expected: float

    @property
    def ratio(self) -> float:
        """مرصودُ الحرف مقسومًا على متوقَّعه؛ والصفرُ قاعٌ لا انفراد."""

        if self.expected <= 0.0:
            raise MaqayisAdjacencyConstraintError("حرفٌ بلا متوقَّعٍ لا تُقاس نسبتُه.")
        return self.observed / self.expected

    @property
    def is_at_the_floor(self) -> bool:
        """هل بلغ الحرفُ قاعَ الترتيب، أي لم يُجاوِر مخرجَه ولا مرّةً واحدة؟"""

        return self.observed == 0


def _column(roots: Sequence[tuple[str, str, str]], index: int) -> list[str]:
    return [root[index] for root in roots]


def _rate(left: Sequence[str], right: Sequence[str]) -> float:
    same, read = same_place_rate(left, right)
    return same / read


def _sampled_rates(
    roots: Sequence[tuple[str, str, str]], profile: NullProfile
) -> tuple[list[float], list[float]]:
    """يُبدِّل الأعمدةَ الثلاثةَ مستقلّةً ويقيس الموضعين على التبديلة نفسِها.

    وتبديلُ كلِّ عمودٍ على حدةٍ يحفظ تواترَ الحروف في موضعها، فلا يكون الفرقُ
    المرصودُ بين الموضعين أثرًا لاختلاف تواترهما. والتبديلةُ الواحدةُ تخدم
    الموضعين معًا، ليكون الفرقُ بينهما مقيسًا على صفريٍّ واحد.

    والإحصاءُ إنّما يقرأ **المحاذاةَ النسبيّة** بين العمودين، فتبديلُ ثلاثتها
    وتثبيتُ الأوسط وتبديلُ طرفَيه يُخرِجان القانونَ نفسَه بعينه: إذ تعتمد
    الأزواجُ على σ₁σ₂⁻¹ وσ₂σ₃⁻¹ وهما مستقلّتان منتظمتان في الحالين. فيُثبَّت
    الأوسطُ توفيرًا لا تخفيفًا للصفريّ.
    """

    first = _column(roots, 0)
    middle = _column(roots, 1)
    last = _column(roots, 2)
    alphabet = sorted(set(first) | set(middle) | set(last))
    places = sorted({place_of(letter) for letter in alphabet})
    code = {
        letter: places.index(place_of(letter)) * 64 + index
        for index, letter in enumerate(alphabet)
    }
    place_code = [value // 64 for value in range(len(alphabet) + 64 * len(places))]
    total = len(first)
    columns = [[code[letter] for letter in column] for column in (first, middle, last)]
    rng = random.Random(profile.seed)
    first_rates: list[float] = []
    second_rates: list[float] = []
    equals = operator.eq
    lookup = place_code.__getitem__
    for _ in range(profile.replicates):
        rng.shuffle(columns[0])
        rng.shuffle(columns[2])
        for left, right, sink in (
            (columns[0], columns[1], first_rates),
            (columns[1], columns[2], second_rates),
        ):
            identical = sum(map(equals, left, right))
            agreeing = sum(map(equals, map(lookup, left), map(lookup, right)))
            sink.append((agreeing - identical) / (total - identical))
    return first_rates, second_rates


def _moments(values: Sequence[float]) -> tuple[float, float]:
    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    return mean, math.sqrt(variance)


@dataclass(frozen=True)
class AdjacencyConstraintReading:
    """قراءةٌ واحدةٌ لقيد التجاور: موضعان، وفرقُهما، وترتيبُ الحروف."""

    roots: tuple[tuple[str, str, str], ...]
    dropped_roots: int
    pairs: tuple[PairReading, PairReading]
    asymmetry_p_value: float
    asymmetry_observed: float
    asymmetry_null_mean: float
    asymmetry_null_sd: float
    depressions: tuple[LetterDepression, ...]
    profile: NullProfile

    @property
    def first_pair(self) -> PairReading:
        """قراءةُ الحرفَين الأوّل والثاني."""

        return self.pairs[0]

    @property
    def second_pair(self) -> PairReading:
        """قراءةُ الحرفَين الثاني والثالث."""

        return self.pairs[1]

    @property
    def geminate_roots(self) -> int:
        """جذورٌ حرفُها الثاني والثالثُ حرفٌ واحد، وهي صورةُ المضاعف في المُودَع."""

        return self.second_pair.identical_pairs

    @property
    def corrected_threshold(self) -> float:
        """أضيقُ عتبةٍ في سُلَّم هولم على الاختبارات الثلاثة المُعلَنة."""

        return self.profile.alpha / 3

    @property
    def the_null_can_reach_the_threshold(self) -> bool:
        """هل تبلغ أرضيّةُ دقّة الصفريّ العتبةَ المُصحَّحة؟ وإلّا فالاختبارُ ميّت."""

        return self.profile.smallest_attainable_p < self.corrected_threshold

    @property
    def rejections(self) -> tuple[bool, ...]:
        """رفضُ هولم على الاختبارات الثلاثة بترتيبها المُعلَن."""

        return holm_rejections(
            (
                self.first_pair.p_value,
                self.second_pair.p_value,
                self.asymmetry_p_value,
            ),
            alpha=self.profile.alpha,
        )

    @property
    def constraint_holds_at_both_positions(self) -> bool:
        """هل قام القيدُ في الموضعين معًا بعد التصحيح؟"""

        rejected = self.rejections
        return rejected[0] and rejected[1]

    @property
    def asymmetry_standing(self) -> AsymmetryStanding:
        """حكمُ الأسيميّة، مأخوذًا من اختبار الفرق لا من مقابلة قيمتَي z."""

        if not self.rejections[2]:
            return AsymmetryStanding.THE_TWO_POSITIONS_ARE_NOT_DISTINGUISHED
        if self.first_pair.depression_ratio < self.second_pair.depression_ratio:
            return AsymmetryStanding.THE_FIRST_PAIR_IS_MORE_CONSTRAINED
        return AsymmetryStanding.THE_SECOND_PAIR_IS_MORE_CONSTRAINED

    @property
    def raw_asymmetry_would_be_claimed(self) -> bool:
        """هل تبدو الأسيميّةُ قائمةً لو قُرئ الخامُّ بأزواج الحرف الواحد؟

        وهي تبدو كذلك: الفرقُ الخامُّ واسعٌ، وكلُّه من إظهار التضعيف. فتُعرَض
        هذه القراءةُ لتُسمّى كلفةُ الاصطلاح، لا لتُحسَب نتيجة.
        """

        return self.first_pair.raw_rate * 2.0 < self.second_pair.raw_rate

    @property
    def letters_at_the_floor(self) -> tuple[str, ...]:
        """الحروفُ التي لم تُجاوِر مخرجَها ولا مرّةً في الزوج الأوّل."""

        return tuple(
            depression.letter
            for depression in self.depressions
            if depression.is_at_the_floor
        )

    @property
    def qaf_standing(self) -> QafStanding:
        """حكمُ القاف: انفرادٌ في القاع لا يقوم إلّا إن كانت وحدَها فيه."""

        floor = self.letters_at_the_floor
        if "ق" not in floor:
            return QafStanding.NOT_AT_THE_FLOOR
        if len(floor) == 1:
            return QafStanding.SINGLED_OUT_AT_THE_FLOOR
        return QafStanding.TIED_AT_THE_FLOOR

    def depression_of(self, letter: str) -> LetterDepression:
        """قراءةُ حرفٍ بعينه، أو رفعٌ إن كان خارجَ المقروء."""

        folded = fold_letter(letter)
        for depression in self.depressions:
            if depression.letter == folded:
                return depression
        raise MaqayisAdjacencyConstraintError(
            f"الحرفُ {letter!r} ليس في المقروء، فلا تُختلَق له قراءة."
        )


def _depressions(
    roots: Sequence[tuple[str, str, str]],
) -> tuple[LetterDepression, ...]:
    first = _column(roots, 0)
    middle = _column(roots, 1)
    total = len(roots)
    first_letters: dict[str, int] = {}
    middle_letters: dict[str, int] = {}
    for letter in first:
        first_letters[letter] = first_letters.get(letter, 0) + 1
    for letter in middle:
        middle_letters[letter] = middle_letters.get(letter, 0) + 1
    observed: dict[str, int] = {}
    neighbours: dict[str, int] = {}
    for left, right in zip(first, middle, strict=True):
        if left == right:
            continue
        agreeing = place_of(left) == place_of(right)
        for letter in (left, right):
            neighbours[letter] = neighbours.get(letter, 0) + 1
            if agreeing:
                observed[letter] = observed.get(letter, 0) + 1
    expected: dict[str, float] = {}
    for letter in set(first) | set(middle):
        place = place_of(letter)
        opposite_place = sum(
            count for other, count in middle_letters.items() if place_of(other) == place
        )
        own_place = sum(
            count for other, count in first_letters.items() if place_of(other) == place
        )
        share = first_letters.get(letter, 0) * (
            opposite_place - middle_letters.get(letter, 0)
        )
        share += middle_letters.get(letter, 0) * (
            own_place - first_letters.get(letter, 0)
        )
        expected[letter] = share / total
    rows = [
        LetterDepression(
            letter=letter,
            observed=observed.get(letter, 0),
            neighbours=neighbours.get(letter, 0),
            expected=expected[letter],
        )
        for letter in sorted(expected)
        if expected[letter] > 0.0
    ]
    rows.sort(key=lambda row: (row.ratio, row.letter))
    return tuple(rows)


def run_adjacency_constraint(
    profile: NullProfile = THE_DECLARED_NULL_PROFILE,
) -> AdjacencyConstraintReading:
    """يُجري القياسَ كلَّه على الجذور المُودَعة، ويُخرِج قراءةً واحدةً لا حكمًا."""

    roots = folded_roots()
    if not roots:
        raise MaqayisAdjacencyConstraintError("لا جذورَ مقروءةً في المُودَع.")
    dropped = len({str(row["root_full"]) for row in root_table_rows()}) - len(roots)
    columns = [_column(roots, index) for index in range(3)]
    first_null, second_null = _sampled_rates(roots, profile)
    pairs: list[PairReading] = []
    for position, left, right, sampled in (
        (AdjacentPosition.FIRST_PAIR, columns[0], columns[1], first_null),
        (AdjacentPosition.SECOND_PAIR, columns[1], columns[2], second_null),
    ):
        same, read = same_place_rate(left, right)
        raw_same, raw_read = same_place_rate(left, right, drop_identical=False)
        rate = same / read
        mean, sd = _moments(sampled)
        below = sum(1 for value in sampled if value <= rate)
        pairs.append(
            PairReading(
                position=position,
                observed_same=same,
                observed_pairs=read,
                identical_pairs=raw_read - read,
                null_mean=mean,
                null_sd=sd,
                p_value=(below + 1) / (profile.replicates + 1),
                raw_same=raw_same,
                raw_pairs=raw_read,
            )
        )
    observed_gap = pairs[1].rate - pairs[0].rate
    gaps = [
        second - first for first, second in zip(first_null, second_null, strict=True)
    ]
    gap_mean, gap_sd = _moments(gaps)
    extreme = sum(
        1 for gap in gaps if abs(gap - gap_mean) >= abs(observed_gap - gap_mean)
    )
    return AdjacencyConstraintReading(
        roots=tuple(roots),
        dropped_roots=dropped,
        pairs=(pairs[0], pairs[1]),
        asymmetry_p_value=(extreme + 1) / (profile.replicates + 1),
        asymmetry_observed=observed_gap,
        asymmetry_null_mean=gap_mean,
        asymmetry_null_sd=gap_sd,
        depressions=_depressions(roots),
        profile=profile,
    )


THE_ELEVEN_PLACES_ARE_DECLARED_AND_NOT_FORCED: Final[str] = (
    "THE_ELEVEN_PLACES_ARE_DECLARED_AND_NOT_FORCED: المخارجُ أحدَ عشرَ ههنا، "
    "وسيبويه يعدّ ستّةَ عشرَ. وخشونةُ التصنيف ترفع الأساسَ المتوقَّعَ وتُضخِّم "
    "نسبةَ الانخفاض. فالعددُ داخلٌ في كلّ رقمٍ في هذه الوحدة، ووصفُه بأنّه "
    "جامعٌ مانعٌ لا يجعله غيرَ مختار."
)

THE_GEMINATE_SPELLING_IS_A_CONVENTION_NOT_A_MEASUREMENT: Final[str] = (
    "THE_GEMINATE_SPELLING_IS_A_CONVENTION_NOT_A_MEASUREMENT: المضاعفُ مكتوبٌ في "
    "هذا المُودَع مُظهَرَ التضعيف، فتماثلُ مخرج حرفَيه الثاني والثالث مُعطًى "
    "بالكتابة. وكلُّ أسيميّةٍ موضعيّةٍ تُقرَأ من الخامّ أثرُ هذا الاصطلاح، لا "
    "أثرُ قانونٍ في اللسان."
)

THE_GLIDES_CARRY_THE_SURVIVING_VIOLATIONS: Final[str] = (
    "THE_GLIDES_CARRY_THE_SURVIVING_VIOLATIONS: جُلُّ ما ينجو من القيد في "
    "الزوج الأوّل أزواجٌ طرفُها واوٌ أو ياء. فحكمُ الباقي دالّةٌ في إلحاقهما "
    "بالشفويّ والشجريّ، وذلك إلحاقٌ مُتنازَعٌ فيه صوتيًّا وغيرُ مفصولٍ ههنا."
)

A_CONSTRAINT_ON_NEIGHBOURS_IS_NOT_AN_ACCOUNT_OF_FREQUENCY: Final[str] = (
    "A_CONSTRAINT_ON_NEIGHBOURS_IS_NOT_AN_ACCOUNT_OF_FREQUENCY: هذه الوحدة تقيس "
    "مَن يُجاوِر مَن، ولا تقيس كم يحضر حرفٌ في المعجم. فقيامُ القيد لا يُفسِّر "
    "تواترَ حرفٍ ولا يصل ثِقَلَ النطق بالحضور الجذريّ، وذلك سؤالٌ آخرُ باقٍ "
    "بلا جواب."
)

THE_CONSTRAINT_IS_A_STANDING_CLAIM_AND_NOT_A_FINDING_HERE: Final[str] = (
    "THE_CONSTRAINT_IS_A_STANDING_CLAIM_AND_NOT_A_FINDING_HERE: تنافرُ الجذر "
    "دعوًى مستقرّةٌ منذ غرينبرغ ١٩٥٠. فظهورُه في هذه البايتات يُقرَأ فحصَ "
    "سلامةٍ للاستخراج، لا كشفًا جديدًا تُنسَب إليه هذه الشجرة."
)

NO_PHYSIOLOGICAL_CAUSE_IS_MEASURED_HERE: Final[str] = (
    "NO_PHYSIOLOGICAL_CAUSE_IS_MEASURED_HERE: قيامُ القيد لا يُعيِّن سببَه. لم "
    "يُقَس ههنا ثِقَلُ نطقٍ ولا كلفةُ مخرجٍ ولا أثرُ استخراجٍ من المصدر، "
    "فالعزوُ إلى فسيولوجيا اللسان بقيّةٌ بلا مِسبار."
)

ADJACENCY_CONSTRAINT_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "THE_ELEVEN_PLACES_ARE_DECLARED_AND_NOT_FORCED": (
        THE_ELEVEN_PLACES_ARE_DECLARED_AND_NOT_FORCED
    ),
    "THE_GEMINATE_SPELLING_IS_A_CONVENTION_NOT_A_MEASUREMENT": (
        THE_GEMINATE_SPELLING_IS_A_CONVENTION_NOT_A_MEASUREMENT
    ),
    "THE_GLIDES_CARRY_THE_SURVIVING_VIOLATIONS": (
        THE_GLIDES_CARRY_THE_SURVIVING_VIOLATIONS
    ),
    "A_CONSTRAINT_ON_NEIGHBOURS_IS_NOT_AN_ACCOUNT_OF_FREQUENCY": (
        A_CONSTRAINT_ON_NEIGHBOURS_IS_NOT_AN_ACCOUNT_OF_FREQUENCY
    ),
    "THE_CONSTRAINT_IS_A_STANDING_CLAIM_AND_NOT_A_FINDING_HERE": (
        THE_CONSTRAINT_IS_A_STANDING_CLAIM_AND_NOT_A_FINDING_HERE
    ),
    "NO_PHYSIOLOGICAL_CAUSE_IS_MEASURED_HERE": NO_PHYSIOLOGICAL_CAUSE_IS_MEASURED_HERE,
}
"""ما لا يُثبِته هذا القياسُ مُسمًّى باسمه، لا مطويًّا في حكمٍ عامّ."""
