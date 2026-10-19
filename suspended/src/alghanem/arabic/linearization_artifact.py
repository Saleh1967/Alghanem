"""الترتيبُ الخطّيُّ بين الحامل وعلامته: هل يحمل خبرًا، أم هو أثرُ ترميز؟

الدعوى المعروضة: أنّ يونيكود يفرض ترتيبًا خطّيًّا على شيءٍ غيرِ خطّيّ، وأنّ
المئةَ بالمئة أثرُ تسطيحِ بُعدَين في واحد، وأنّ CV نقطةٌ في فضاءٍ ذي بُعدين لا
زوجٌ مرتَّبٌ في تسلسل. وههنا تُفصَل إلى ما يُقاس، ويُقاس:

1. **وقوعُ العلامة بعد حاملها بنسبة مئةٍ بالمئة** — منعقدةٌ، و**خاليةٌ من
   الخبر**. فهي **مبرهنةٌ من نموذج الترميز** لا مرصودةٌ في اللغة: كلُّ علامةٍ
   من الخمس صنفُها التركيبيُّ غيرُ صفر، وذو الصنف غيرِ الصفر لاحقٌ لأساسه
   بتعريف يونيكود. فالنسبةُ تصدق على أيّ نصٍّ كيفما كان، وتصدق على النصّ الخالي
   — ولا يُشتَقّ من قضيّةٍ صادقةٍ فراغًا خبرٌ عن العربيّة
   (`AHundredPercentForcedByTheEncodingCarriesNoBits`).

2. **ترتيبُ العلامات على الحامل الواحد حرٌّ ثمّ يُسطَّح** — **منتقضة**. فليس
   حرًّا أصلًا: أصنافُ العلامات الستّ متمايزةٌ كلُّها، فالترتيبُ القانونيُّ
   يفرض على كلّ مجموعةٍ صورةً واحدةً لا ثانيةَ لها. لا اختيارَ سُطِّح، بل
   **حرّيّةٌ لم توجد قطّ** (`TheMarkOrderWasNeverFreeToBegin`).

3. **CV نقطةٌ في فضاءٍ ذي بُعدين لا زوجٌ في تسلسل** — منعقدةٌ ببرهانِ عكسٍ
   تامّ: تُعاد كلماتُ الإيداع كلُّها من (تتابعِ الحوامل + مجموعةِ علاماتِ كلِّ
   حاملٍ **غيرِ مرتَّبة**) فتطابق الأصلَ حرفًا بحرف. فالترتيبُ داخلَ الحامل
   لا يحمل بتًّا واحدًا، والقراءةُ ذاتُ البُعدين كافيةٌ وافية.

4. **«تسطيحُ بُعدَين في واحد»** — **تُصحَّح**. فالتسطيحُ **تقابلٌ لا يفقد
   شيئًا**، لا ضياعَ فيه: عكسُه تامٌّ، فلا بُعدَ ضاع. والذي تُزيله القراءةُ
   ذاتُ البُعدين ليس خبرًا مفقودًا بل **درجةَ حرّيّةٍ كاذبة**: ستّةَ عشرَ بتًّا
   من ترتيباتٍ يبدو أنّ الخطَّ يعرضها، وكلُّها تدلّ على النقطة نفسِها
   (`TheFlatteningLosesNothingItRemovesAFalseFreedom`).

**وفي دعوى الاستقلال نظر**: سندُ الصنف التركيبيِّ مستقلٌّ عن **المدوّنة** حقًّا
— يصدق بلا وقعةٍ واحدة — لكنّه **ليس مستقلًّا عن يونيكود**، وبنيةُ الليف
المقيسةُ قبلُ مقروءةٌ بيونيكود أيضًا. فالمحورُ الثاني مستقلُّ *المصدر الشاهد* لا
مستقلُّ *نظام الترميز* (`TheSecondAxisIsIndependentOfTheCorpusNotOfUnicode`).

وهذا كلُّه في هندسة الكتابة لا في الصوت؛ و`UnicodeIsNotRecordedSound` قائم. ولا
ولادةَ ههنا ولا حكمَ ولادةٍ كرنليًّا، ولا تُستورَد `kernel/` من هذه الوحدة.
"""

from __future__ import annotations

import math
import unicodedata
from dataclasses import dataclass
from enum import Enum
from itertools import permutations
from typing import Final

from .carrier_state_observed_fiber import (
    ABSENT,
    ObservedFiberTable,
    OccurrenceRow,
    run_observed_fiber_on_the_deposited_fatiha,
)

__all__ = [
    "A_HUNDRED_PERCENT_CARRIES_NO_BITS_NOTE",
    "A_READING_HERE_IS_A_READING_OF_WRITING_NOTE",
    "LINEARIZATION_NAMED_RESIDUALS",
    "THE_CLAIM",
    "THE_FLATTENING_REMOVES_A_FALSE_FREEDOM_NOTE",
    "THE_MARK_ORDER_WAS_NEVER_FREE_NOTE",
    "THE_SECOND_AXIS_IS_INDEPENDENT_OF_THE_CORPUS_ONLY_NOTE",
    "LinearityReading",
    "LinearityVerdict",
    "LinearizationError",
    "MarkOrderFreedom",
    "OrderingCensus",
    "RoundTripAudit",
    "every_mark_follows_its_carrier_by_definition",
    "measure_mark_order_freedom",
    "measure_ordering_census",
    "read_the_linearity_claim",
    "round_trip_from_unordered_sets",
]


class LinearizationError(ValueError):
    """رفضٌ صريح: قياسٌ بلا مقام، أو حكمٌ بلا سببٍ مكتوب."""


THE_CLAIM: Final[str] = (
    "لا ترتيبَ مكانيًّا بين الحامل وحركته أصلًا؛ فيونيكود يفرض ترتيبًا خطّيًّا "
    "على غيرِ الخطّيّ، والمئةُ بالمئة أثرُ تسطيحِ بُعدَين في واحد"
)

_READ_MARKS: Final[tuple[str, ...]] = (
    "\u064e",  # فتحة
    "\u064f",  # ضمّة
    "\u0650",  # كسرة
    "\u0651",  # شدّة
    "\u0652",  # سكون
)

_DEFERRED_MARKS: Final[tuple[str, ...]] = ("\u0670",)  # ألفٌ خنجريّة: محورُ المدّ

_A_BASE_LETTER: Final[str] = "\u0628"


class LinearityReading(Enum):
    """قراءاتُ دعوى الخطّيّة، متمايزةَ الحكم."""

    THE_MARK_ALWAYS_FOLLOWS_ITS_CARRIER = "العلامةُ تقع بعد حاملها دائمًا"
    THE_MARK_ORDER_IS_A_FLATTENED_CHOICE = "ترتيبُ العلامات اختيارٌ سُطِّح"
    CV_IS_A_POINT_NOT_AN_ORDERED_PAIR = "CV نقطةٌ لا زوجٌ مرتَّب"
    THE_FLATTENING_LOSES_A_DIMENSION = "التسطيحُ يُضيّع بُعدًا"
    THE_SECOND_AXIS_IS_INDEPENDENT = "المحورُ الثاني مستقلّ"


class LinearityVerdict(Enum):
    """حكمُ القراءة؛ والصادقُ فراغًا غيرُ الصادق خبرًا."""

    HELD_BUT_CARRIES_NO_INFORMATION = "منعقدةٌ_بلا_خبر"
    HELD_BY_EXACT_INVERSION = "منعقدةٌ_بعكسٍ_تامّ"
    REFUTED = "منتقضة"
    HELD_ONLY_IN_A_NARROWER_SENSE = "منعقدةٌ_في_معنًى_أضيق"


@dataclass(frozen=True)
class LinearityVerdictReading:
    """حكمُ قراءةٍ واحدة، ومعه ما قرّره وما بقي عليه."""

    reading: LinearityReading
    verdict: LinearityVerdict
    what_decided_it: str
    residuals: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.what_decided_it.strip():
            raise LinearizationError("حكمٌ بلا سببٍ مكتوب")
        if not self.residuals:
            raise LinearizationError(
                f"«{self.reading.value}» بلا بقيّةٍ مُسمّاة؛ والخلوُّ ليس إعفاءً"
            )
        if any(not note.strip() for note in self.residuals):
            raise LinearizationError("في البقايا مدخلٌ فارغ")


# --- المئةُ بالمئة: مبرهنةٌ لا مرصودة ----------------------------------------------


def every_mark_follows_its_carrier_by_definition() -> bool:
    """أصنفُ كلِّ علامةٍ تركيبيٌّ غيرُ صفر، فهي لاحقةٌ لأساسها بتعريف الترميز؟

    ولا تُقرأ هذه من المدوّنة: تصدق بلا وقعةٍ واحدة، وذلك عينُ خلوِّها من الخبر.
    """

    return all(
        unicodedata.combining(mark) != 0 for mark in _READ_MARKS + _DEFERRED_MARKS
    )


# --- حرّيّةُ الترتيب: هل وُجدت أصلًا؟ ---------------------------------------------


@dataclass(frozen=True)
class MarkOrderFreedom:
    """أكانَ ترتيبُ العلامات على حاملٍ واحدٍ حرًّا قبل التسطيح؟"""

    multisets_examined: int
    multisets_with_a_single_canonical_form: int
    distinct_combining_classes: int
    marks_examined: int

    def __post_init__(self) -> None:
        if self.multisets_with_a_single_canonical_form > self.multisets_examined:
            raise LinearizationError("المُثبَتُ أكثرُ من المفحوص؛ ومقامٌ كهذا مُحال")

    @property
    def order_was_ever_free(self) -> bool:
        """أبقيت مجموعةٌ واحدةٌ تحتمل أكثرَ من صورةٍ قانونيّة؟"""

        return self.multisets_with_a_single_canonical_form != self.multisets_examined

    @property
    def classes_are_pairwise_distinct(self) -> bool:
        """أصنافُ العلامات متمايزةٌ كلُّها؟ وهو سببُ انحتام الترتيب."""

        return self.distinct_combining_classes == self.marks_examined


def measure_mark_order_freedom() -> MarkOrderFreedom:
    """افحص كلَّ مجموعةِ علاماتٍ ممكنة: أتحتمل أكثرَ من صورةٍ قانونيّة؟"""

    marks = _READ_MARKS + _DEFERRED_MARKS
    examined = 0
    single = 0
    for size in range(2, len(marks) + 1):
        for combination in permutations(marks, size):
            if list(combination) != sorted(combination):
                continue
            examined += 1
            forms = {
                unicodedata.normalize("NFC", _A_BASE_LETTER + "".join(order))
                for order in permutations(combination)
            }
            if len(forms) == 1:
                single += 1
    return MarkOrderFreedom(
        multisets_examined=examined,
        multisets_with_a_single_canonical_form=single,
        distinct_combining_classes=len({unicodedata.combining(mark) for mark in marks}),
        marks_examined=len(marks),
    )


# --- العكسُ التامّ: القراءةُ ذاتُ البُعدين كافيةٌ أو غيرُ كافية ---------------------


def _marks_of(row: OccurrenceRow) -> frozenset[str]:
    """علاماتُ الوقوع **غيرَ مرتَّبة**: المقروءةُ والمؤجَّلةُ وما لم يُقرأ."""

    read = {value for _axis, value in row.state_vector if value != ABSENT}
    return frozenset(read | set(row.deferred_axis_marks) | set(row.unread_marks))


@dataclass(frozen=True)
class RoundTripAudit:
    """عكسُ الكلمات من مجموعاتٍ غيرِ مرتَّبة: ما طابق، وما اختلف وبأيّ علامة."""

    words_examined: int
    words_reconstructed: int
    mismatching_words: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.words_reconstructed > self.words_examined:
            raise LinearizationError("المُعادُ أكثرُ من المفحوص؛ ومقامٌ كهذا مُحال")
        if len(self.mismatching_words) != (
            self.words_examined - self.words_reconstructed
        ):
            raise LinearizationError(
                "المختلفُ لا يُطابق فرقَ المفحوص والمُعاد؛ ولا يُطوى منه شيء"
            )

    @property
    def is_lossless(self) -> bool:
        """أعادت القراءةُ ذاتُ البُعدين كلَّ كلمةٍ حرفًا بحرف؟"""

        return self.words_reconstructed == self.words_examined


def round_trip_from_unordered_sets(
    table: ObservedFiberTable | None = None,
) -> RoundTripAudit:
    """أعِد كلَّ كلمةٍ من تتابع حواملها ومجموعةِ علاماتِ كلِّ حاملٍ غيرِ مرتَّبة."""

    measured = run_observed_fiber_on_the_deposited_fatiha() if table is None else table
    if not measured.rows:
        raise LinearizationError("جدولٌ بلا وقعات؛ ولا يُعكَس على خلاء")

    grouped: dict[tuple[int, int], list[OccurrenceRow]] = {}
    for row in measured.rows:
        grouped.setdefault((row.line_index, row.word_index), []).append(row)

    reconstructed = 0
    mismatching: list[str] = []
    for rows in grouped.values():
        ordered = sorted(rows, key=lambda row: row.position_in_word)
        rebuilt = "".join(
            unicodedata.normalize("NFC", row.carrier + "".join(sorted(_marks_of(row))))
            for row in ordered
        )
        original = ordered[0].word
        if unicodedata.normalize("NFC", rebuilt) == unicodedata.normalize(
            "NFC", original
        ):
            reconstructed += 1
        else:
            mismatching.append(original)

    return RoundTripAudit(
        words_examined=len(grouped),
        words_reconstructed=reconstructed,
        mismatching_words=tuple(mismatching),
    )


# --- الترتيباتُ المطويّة، معدودةً بالبتّ -------------------------------------------


@dataclass(frozen=True)
class OrderingCensus:
    """كم ترتيبًا يبدو أنّ الخطَّ يعرضه، وكلُّها تدلّ على النقطة نفسِها؟"""

    carriers_bearing_marks: int
    carriers_bearing_more_than_one_mark: int
    orderings_denoting_the_same_reading: int

    def __post_init__(self) -> None:
        if self.orderings_denoting_the_same_reading < 1:
            raise LinearizationError("عددُ الترتيبات لا ينزل عن واحد")
        if self.carriers_bearing_more_than_one_mark > self.carriers_bearing_marks:
            raise LinearizationError("ذو العلامتين أكثرُ من ذي العلامة؛ ومقامٌ مُحال")

    @property
    def bits_of_apparent_freedom(self) -> float:
        """درجةُ الحرّيّة الكاذبة بالبتّ؛ وهي المطويّةُ لا المفقودة."""

        return math.log2(self.orderings_denoting_the_same_reading)


def measure_ordering_census(
    table: ObservedFiberTable | None = None,
) -> OrderingCensus:
    """عُدَّ الترتيباتِ التي تدلّ كلُّها على القراءة الواحدة نفسِها."""

    measured = run_observed_fiber_on_the_deposited_fatiha() if table is None else table
    bearing = 0
    many = 0
    product = 1
    for row in measured.rows:
        count = len(_marks_of(row))
        if count:
            bearing += 1
        if count > 1:
            many += 1
        product *= math.factorial(count)
    return OrderingCensus(
        carriers_bearing_marks=bearing,
        carriers_bearing_more_than_one_mark=many,
        orderings_denoting_the_same_reading=product,
    )


# --- قراءةُ الدعوى ----------------------------------------------------------------


def read_the_linearity_claim(
    table: ObservedFiberTable | None = None,
) -> tuple[LinearityVerdictReading, ...]:
    """اقرأ دعوى الخطّيّة قراءاتِها، ولكلِّ قراءةٍ حكمٌ وسببٌ وبقيّة."""

    measured = run_observed_fiber_on_the_deposited_fatiha() if table is None else table
    freedom = measure_mark_order_freedom()
    audit = round_trip_from_unordered_sets(measured)
    census = measure_ordering_census(measured)

    if not every_mark_follows_its_carrier_by_definition():
        raise LinearizationError(
            "علامةٌ صنفُها التركيبيُّ صفر؛ والدعوى تُبنى على غير ذلك فتُرفَع"
        )

    return (
        LinearityVerdictReading(
            reading=LinearityReading.THE_MARK_ALWAYS_FOLLOWS_ITS_CARRIER,
            verdict=LinearityVerdict.HELD_BUT_CARRIES_NO_INFORMATION,
            what_decided_it=(
                f"أصنافُ العلامات الـ{freedom.marks_examined} كلُّها غيرُ صفر، "
                "وذو الصنف غيرِ الصفر لاحقٌ لأساسه بتعريف الترميز؛ فالنسبةُ "
                "مبرهنةٌ لا مرصودة، تصدق على أيّ نصٍّ وعلى النصّ الخالي، ولا "
                "تفصل بين لغةٍ ولغة"
            ),
            residuals=(
                "A_HUNDRED_PERCENT_FORCED_BY_THE_ENCODING_CARRIES_NO_BITS: ما "
                "صدق فراغًا لا يُشتَقّ منه خبر؛ والمئةُ بالمئة ههنا قضيّةٌ في "
                "يونيكود لا كشفٌ عن العربيّة",
                "ولو رُصد خرقٌ لها لكان خرقًا في قارئ الترميز لا في اللغة",
            ),
        ),
        LinearityVerdictReading(
            reading=LinearityReading.THE_MARK_ORDER_IS_A_FLATTENED_CHOICE,
            verdict=LinearityVerdict.REFUTED,
            what_decided_it=(
                f"لم يكن حرًّا ليُسطَّح: أصنافُ العلامات الـ"
                f"{freedom.distinct_combining_classes} متمايزةٌ كلُّها، فكلُّ "
                f"مجموعةٍ من المجموعات الـ{freedom.multisets_examined} "
                f"المفحوصة لها صورةٌ قانونيّةٌ واحدةٌ لا ثانيةَ لها "
                f"({freedom.multisets_with_a_single_canonical_form} من "
                f"{freedom.multisets_examined})"
            ),
            residuals=(
                "THE_MARK_ORDER_WAS_NEVER_FREE_TO_BEGIN: لا اختيارَ سُطِّح، بل "
                "حرّيّةٌ لم توجد؛ والانحتامُ من الترتيب القانونيّ لا من اللغة",
                "ولو تساوى صنفانِ لعادت الحرّيّةُ وصار للترتيب خبر؛ فالحكمُ "
                "معلَّقٌ بتمايز الأصناف لا بعدد العلامات",
            ),
        ),
        LinearityVerdictReading(
            reading=LinearityReading.CV_IS_A_POINT_NOT_AN_ORDERED_PAIR,
            verdict=LinearityVerdict.HELD_BY_EXACT_INVERSION,
            what_decided_it=(
                f"أُعيدت {audit.words_reconstructed} من "
                f"{audit.words_examined} كلمةً حرفًا بحرف من تتابع الحوامل "
                "ومجموعةِ علاماتِ كلِّ حاملٍ غيرِ مرتَّبة؛ فالترتيبُ داخلَ "
                "الحامل لا يحمل بتًّا واحدًا"
            ),
            residuals=(
                "العكسُ تامٌّ بشرط حمل المؤجَّل وما لم يُقرأ في المجموعة؛ ولو "
                "طُرح المؤجَّلُ لاختلّت كلمتان بالألف الخنجريّة، والاختلالُ "
                "حينئذٍ من طرحِ محورٍ لا من الترتيب",
                "تتابعُ الحوامل نفسُه خطّيٌّ وحاملٌ للخبر؛ والمنفيُّ ترتيبُ "
                "الحامل مع علامته لا ترتيبُ الحوامل بينها",
            ),
        ),
        LinearityVerdictReading(
            reading=LinearityReading.THE_FLATTENING_LOSES_A_DIMENSION,
            verdict=LinearityVerdict.REFUTED,
            what_decided_it=(
                "التسطيحُ تقابلٌ لا يفقد شيئًا: عكسُه تامٌّ، فلا بُعدَ ضاع. "
                f"والذي تُزيله القراءةُ ذاتُ البُعدين "
                f"{census.orderings_denoting_the_same_reading} ترتيبًا "
                f"({census.bits_of_apparent_freedom:.0f} بتًّا) من "
                f"{census.carriers_bearing_more_than_one_mark} حاملًا ذي أكثرَ "
                "من علامة، وكلُّها تدلّ على النقطة نفسِها"
            ),
            residuals=(
                "THE_FLATTENING_LOSES_NOTHING_IT_REMOVES_A_FALSE_FREEDOM: "
                "الحرّيّةُ المطويّةُ كاذبةٌ لا مفقودة؛ وقوّةُ الدعوى في نفي "
                "درجةِ حرّيّةٍ لا في استرجاع خبر",
                "ولو كانت الحرّيّةُ صادقةً لظهر فرقٌ في العكس؛ ولم يظهر",
            ),
        ),
        LinearityVerdictReading(
            reading=LinearityReading.THE_SECOND_AXIS_IS_INDEPENDENT,
            verdict=LinearityVerdict.HELD_ONLY_IN_A_NARROWER_SENSE,
            what_decided_it=(
                "سندُ الصنف التركيبيِّ مستقلٌّ عن المدوّنة حقًّا: يصدق بلا "
                "وقعةٍ واحدة، ولا يستمدّ من عدد. لكنّه ليس مستقلًّا عن يونيكود، "
                "وبنيةُ الليف المقيسةُ قبلُ مقروءةٌ بيونيكود أيضًا؛ فالمحورانِ "
                "يشتركان في نظام الترميز وإن افترقا في المصدر الشاهد"
            ),
            residuals=(
                "THE_SECOND_AXIS_IS_INDEPENDENT_OF_THE_CORPUS_NOT_OF_UNICODE: "
                "استقلالُ المصدر الشاهد ليس استقلالَ النظام؛ ونسبةُ الثاني "
                "إلى الأوّل تُقوّي السندَ أكثرَ ممّا يحتمل",
                "ولا يُرفَع هذا القيدُ إلّا بمحورٍ لا يمرّ بيونيكود أصلًا، "
                "كرسمٍ مخطوطٍ يُقاس بغير ترميزٍ محارف",
            ),
        ),
    )


# --- الحدودُ مُسمّاةً -------------------------------------------------------------


A_HUNDRED_PERCENT_CARRIES_NO_BITS_NOTE: Final[str] = (
    "AHundredPercentForcedByTheEncodingCarriesNoBits: وقوعُ العلامة بعد حاملها "
    "مبرهنٌ من صنفها التركيبيِّ غيرِ الصفر، فيصدق على أيّ نصٍّ وعلى النصّ "
    "الخالي؛ وما صدق فراغًا لا يُشتَقّ منه خبرٌ عن اللغة"
)

THE_MARK_ORDER_WAS_NEVER_FREE_NOTE: Final[str] = (
    "TheMarkOrderWasNeverFreeToBegin: أصنافُ العلامات متمايزةٌ كلُّها، فالترتيبُ "
    "القانونيُّ يفرض لكلّ مجموعةٍ صورةً واحدة؛ فلا اختيارَ سُطِّح، بل حرّيّةٌ لم "
    "توجد قطّ، والحكمُ معلَّقٌ بتمايز الأصناف لو زال"
)

THE_FLATTENING_REMOVES_A_FALSE_FREEDOM_NOTE: Final[str] = (
    "TheFlatteningLosesNothingItRemovesAFalseFreedom: العكسُ من المجموعات غيرِ "
    "المرتَّبة تامّ، فلا بُعدَ ضاع في التسطيح؛ والقراءةُ ذاتُ البُعدين تُزيل "
    "درجةَ حرّيّةٍ كاذبةً لا تسترجع خبرًا مفقودًا"
)

THE_SECOND_AXIS_IS_INDEPENDENT_OF_THE_CORPUS_ONLY_NOTE: Final[str] = (
    "TheSecondAxisIsIndependentOfTheCorpusNotOfUnicode: سندُ الصنف التركيبيِّ "
    "لا يستمدّ من عددٍ في المدوّنة، لكنّه يمرّ بيونيكود كما مرّت به بنيةُ الليف؛ "
    "فلا يُسنَد أحدُهما بالآخر إسنادَ محورٍ مستقلٍّ تمامًا"
)

A_READING_HERE_IS_A_READING_OF_WRITING_NOTE: Final[str] = (
    "AReadingHereIsAReadingOfWriting: ما قيس هندسةُ كتابةٍ بترميزٍ مُعلَن، لا "
    "نطقٌ ولا بنيةٌ في اللغة؛ و`UnicodeIsNotRecordedSound` قائم، ولا ولادةَ "
    "ههنا ولا حكمَ ولادة"
)

LINEARIZATION_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_HUNDRED_PERCENT_CARRIES_NO_BITS_NOTE,
    THE_MARK_ORDER_WAS_NEVER_FREE_NOTE,
    THE_FLATTENING_REMOVES_A_FALSE_FREEDOM_NOTE,
    THE_SECOND_AXIS_IS_INDEPENDENT_OF_THE_CORPUS_ONLY_NOTE,
    A_READING_HERE_IS_A_READING_OF_WRITING_NOTE,
)
