"""مربّعُ الاستقراء في رتبة ماركوف: «على» ثمّ «لـ»، و«لـ» ثمّ «على».

**أوّلًا: والمقيسُ ههنا مربّعٌ لا رتبة.** لا تدّعي هذه الوحدةُ أنّ للجذر
العربيِّ رتبةَ ماركوف بعينها. وإنّما تسأل سؤالًا واحدًا: هل الرتبةُ التي
نُخرِجها من هذه البايتات خاصّةٌ في المادّة، أم خاصّةٌ في **ترتيب استقرائنا**؟
فلذلك أُخِذ الطريقان معًا وقُوبِل بينهما::

    ARungSelectedOnTheWhole   != ARungSelectedInsideTheSeen
    ACriterionThatPenalises   != ACriterionThatPredicts
    AgreementOfTwoRoutes      != ATrueOrder

**وثانيًا: والسلّمُ أربعُ درجاتٍ متداخلةٍ تداخلًا تامًّا.** يُطوى الجذرُ إلى
ثلاثةِ مخارجَ من المخارج الإحدى عشرةَ المُعلَنة، فيصير جدولًا ثلاثيَّ الرتبة
عدّتُه ١١×١١×١١. والدرجاتُ نماذجُ لوغاريتميّةٌ خطّيّةٌ مرتَّبةٌ بالاحتواء:

| الدرجة | ما تُبقيه | درجاتُ الحرّيّة |
|---|---|---|
| الاستقلال | الهوامشُ الثلاثةُ وحدَها | ٣٠ |
| السلسلة | زوجا التجاور | ٢٣٠ |
| المثلّث | الأزواجُ الثلاثةُ بلا تفاعلٍ ثلاثيّ | ٣٣٠ |
| المشبَع | الجدولُ كما هو | ١٣٣٠ |

والاحتواءُ صارمٌ: استقلالٌ ⊂ سلسلةٌ ⊂ مثلّثٌ ⊂ مشبَع؛ يُفحَص آليًّا عند
الاستيراد لا يُوصَف (`verify_the_ladder_is_strictly_nested`). ودرجةُ المثلّث
وحدَها لا حلَّ مغلقًا لها، فتُقدَّر بالتناسب التكراريّ، ويُفحَص أنّ حلَّه
يُعيد الهوامشَ الثنائيّةَ الثلاثةَ جميعًا (`verify_the_triangle_fit_...`).

**وثالثًا: و«على» و«لـ» معرَّفتان لا مترادفتان.**

- **الاستقراءُ على الرتبة**: صعودٌ في السلّم على المادّة **كلِّها**، واختيارُ
  الدرجة بمعيارٍ يعاقب الحرّيّة (BIC). وهو استقراءٌ على دليلٍ مرتَّب.
- **الاستقراءُ لغير المرئيّ**: قسمةُ المادّة مرئيًّا ومحجوبًا، والحكمُ لما لم
  يُرَ. وهو استقراءٌ لغايةٍ لا على دليل.

فالمسارُ الأوّل «على ثمّ لـ»: تُختار الدرجةُ على الكلّ، ثمّ تُحمَل إلى
المحجوب فيُسأل: أهي أفضلُ ما يتنبّأ؟ والمسارُ الثاني «لـ ثمّ على»: تُقسَم
المادّةُ أوّلًا، ثمّ يُصعَد السلّمُ **داخل المرئيّ** بالمعيار نفسِه. والمربّعُ
ينغلق إن اتّفق طرفاه، ولا ينغلق إن اختلفا؛ والاختلافُ أنفعُ، لأنّه يُبطِل أن
تكون «الرتبة» قراءةً في المادّة
(`A_RUNG_THAT_MOVES_WITH_THE_ROUTE_IS_NOT_A_PROPERTY_OF_THE_SOURCE`).

**ورابعًا: والملساران اثنان لئلّا يكون الحكمُ أثرَ ملسار.** القياسُ على
المحجوب يمرّ بخلايا لم تُرَ في المرئيّ، فيلزم ملسارٌ جمعيّ. والملسارُ اختيارٌ،
فأُعلِن اثنان قبل العدّ؛ فإن اختلفا على الفائز لم يُقرَأ الطرفُ أصلًا وخرجت
المنزلةُ `UNREADABLE` (`THE_HELD_OUT_LEG_IS_NOT_READ_WHEN_THE_TWO_SMOOTHINGS_DISAGREE`).

**وخامسًا: والشرطُ مُودَعٌ قبل التشغيل المسجَّل، لا قبل كلّ نظر.** سبق الشرطَ
مسحٌ استكشافيٌّ لعتبة الانقلاب في حجم العيّنة، وقد رُئِيت أرقامُه. فالشرطُ
عتبةٌ ثُبِّتت قبل الجولة المسجَّلة، وليس تنبّؤًا مسجَّلًا؛ ويُقال ذلك صراحةً
لا يُسكَت عنه (`A_CONDITION_FIXED_AFTER_A_PROBE_IS_NOT_A_PREDICTION`).

**وسادسًا: والبوّابةُ القرآنيّةُ لا تُرفَع ههنا.** المقيسُ جدولُ الجذور
المُبصَّمُ لا بايتاتُ المدوّنة؛ فـ`token_markov_standing` يبقى محجوبًا بشرطه
الثالث، ولا يُحسَب في هذه الوحدة رقمٌ قرآنيٌّ واحد
(`MEASURING_MARKOV_ON_THE_ROOT_TABLE_DOES_NOT_OPEN_THE_CORPUS_GATE`).

ولا سلطةَ لهذه الوحدة: لا ولادةَ، ولا ترخيصَ، ولا تجميدَ، ولا استيرادَ من
`kernel/`.
"""

from __future__ import annotations

import math
import random
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from functools import cache
from typing import Final

from .maqayis_adjacency_constraint import place_of
from .markov_readiness_gate import ChainReading, token_markov_standing
from .slot_rights_composition_algebra import algebra_substrate

__all__ = [
    "A_CONDITION_FIXED_AFTER_A_PROBE_IS_NOT_A_PREDICTION",
    "A_RUNG_THAT_MOVES_WITH_THE_ROUTE_IS_NOT_A_PROPERTY_OF_THE_SOURCE",
    "AN_AGREEING_SQUARE_IS_NOT_A_TRUE_ORDER",
    "A_PENALTY_ON_SPARSE_CELLS_IS_A_COMPARISON_NOT_A_TEST",
    "MARKOV_ORDER_INDUCTION_NAMED_RESIDUALS",
    "MEASURING_MARKOV_ON_THE_ROOT_TABLE_DOES_NOT_OPEN_THE_CORPUS_GATE",
    "THE_DECLARED_SMOOTHINGS",
    "THE_HELD_OUT_LEG_IS_NOT_READ_WHEN_THE_TWO_SMOOTHINGS_DISAGREE",
    "THE_LADDER_ORDER",
    "THE_PREREGISTERED_COMMUTATION_CONDITION",
    "THE_REQUIRED_AGREEMENT_SHARE",
    "THE_REQUIRED_DRAW_FLOOR",
    "CommutationReading",
    "CommutationStanding",
    "CrossoverRow",
    "InductionDirection",
    "LadderRung",
    "MarkovOrderInductionError",
    "SplitReading",
    "degrees_of_freedom",
    "fit_rung",
    "held_out_winner",
    "information_criterion",
    "log_likelihood",
    "measure_commutation",
    "place_alphabet",
    "place_sequences",
    "rung_crossover_scan",
    "select_rung",
    "the_corpus_gate_is_untouched",
    "verify_the_ladder_is_strictly_nested",
    "verify_the_triangle_fit_reproduces_every_margin",
]


class MarkovOrderInductionError(RuntimeError):
    """رفضٌ في هذه الوحدة: سلّمٌ غيرُ متداخل، أو قراءةٌ بلا سندٍ مقيس."""


# ---------------------------------------------------------------------------
# السلّمُ والجهتان
# ---------------------------------------------------------------------------


class LadderRung(Enum):
    """درجاتُ السلّم مُسمّاةً؛ وترتيبُها في `THE_LADDER_ORDER`."""

    INDEPENDENT = "استقلالُ الخانات الثلاث"
    CHAIN = "سلسلةُ ماركوف على زوجَي التجاور"
    TRIANGLE = "المثلّثُ بلا تفاعلٍ ثلاثيّ"
    SATURATED = "الجدولُ المشبَع"


THE_LADDER_ORDER: Final[tuple[LadderRung, ...]] = (
    LadderRung.INDEPENDENT,
    LadderRung.CHAIN,
    LadderRung.TRIANGLE,
    LadderRung.SATURATED,
)
"""ترتيبُ الدرجات بالاحتواء الصارم، من أضيقها إلى أوسعها."""


class InductionDirection(Enum):
    """جهتا الاستقراء، وهما تركيبا المربّع لا نهجان مترادفان."""

    ON_THEN_FOR = "على الرتبة ثمّ لغير المرئيّ"
    FOR_THEN_ON = "لغير المرئيّ ثمّ على الرتبة"


class CommutationStanding(Enum):
    """منزلةُ المربّع: انغلاقٌ، أو اختلافٌ، أو تعذّرُ قراءة."""

    COMMUTES_ON_THIS_SOURCE = "انغلق المربّعُ على هذا المصدر"
    DOES_NOT_COMMUTE = "لم ينغلق: الدرجةُ تتبع الطريق"
    UNREADABLE = "غيرُ مقروءٍ بحارسه المُعلَن"


# ---------------------------------------------------------------------------
# البقايا المسمّاة
# ---------------------------------------------------------------------------

A_RUNG_THAT_MOVES_WITH_THE_ROUTE_IS_NOT_A_PROPERTY_OF_THE_SOURCE: Final[str] = (
    "A_RUNG_THAT_MOVES_WITH_THE_ROUTE_IS_NOT_A_PROPERTY_OF_THE_SOURCE: درجةٌ "
    "تتغيّر بتغيّر ترتيب الاستقراء على المادّة نفسِها ليست قراءةً في المادّة؛ "
    "فلا يُنقَل عنها «رتبةُ الجذر كذا» بل «رتبتُه تحت هذا الطريق كذا»"
)

A_PENALTY_ON_SPARSE_CELLS_IS_A_COMPARISON_NOT_A_TEST: Final[str] = (
    "A_PENALTY_ON_SPARSE_CELLS_IS_A_COMPARISON_NOT_A_TEST: الجدولُ ١٣٣١ خليّةً "
    "وأكثرُها خالٍ، فشرطُ المقاربة غيرُ مستوفًى؛ ومعيارُ العقوبة ههنا ترتيبٌ "
    "بين أربعةٍ معروضةٍ لا اختبارُ فرضٍ، ولا يُقرَأ منه احتمالُ خطأ"
)

THE_HELD_OUT_LEG_IS_NOT_READ_WHEN_THE_TWO_SMOOTHINGS_DISAGREE: Final[str] = (
    "THE_HELD_OUT_LEG_IS_NOT_READ_WHEN_THE_TWO_SMOOTHINGS_DISAGREE: القياسُ "
    "على المحجوب يحتاج ملسارًا، والملسارُ اختيار؛ فأُعلِن اثنان قبل العدّ، وإن "
    "اختلفا على الفائز خرجت المنزلةُ `UNREADABLE` ولم يُرجَّح أحدُهما بعدُ"
)

A_CONDITION_FIXED_AFTER_A_PROBE_IS_NOT_A_PREDICTION: Final[str] = (
    "A_CONDITION_FIXED_AFTER_A_PROBE_IS_NOT_A_PREDICTION: سبق الشرطَ مسحٌ "
    "استكشافيٌّ لعتبة الانقلاب رُئِيت أرقامُه؛ فالعتبةُ مُثبَّتةٌ قبل الجولة "
    "المسجَّلة لا قبل كلّ نظر، ولا تُنقَل على أنّها تنبّؤٌ مُودَع"
)

AN_AGREEING_SQUARE_IS_NOT_A_TRUE_ORDER: Final[str] = (
    "AN_AGREEING_SQUARE_IS_NOT_A_TRUE_ORDER: لو اتّفق الطريقان لم يثبت بذلك "
    "أنّ الدرجةَ رتبةُ اللغة؛ وإنّما ثبت أنّ هذه البايتات لا تفرّق بين "
    "الطريقين، وهو نفيُ تمييزٍ لا إثباتُ بنية"
)

MEASURING_MARKOV_ON_THE_ROOT_TABLE_DOES_NOT_OPEN_THE_CORPUS_GATE: Final[str] = (
    "MEASURING_MARKOV_ON_THE_ROOT_TABLE_DOES_NOT_OPEN_THE_CORPUS_GATE: المقيسُ "
    "جدولُ الجذور المُبصَّم، وبوّابةُ ماركوف على المدوّنة تبقى محجوبةً بشرطها "
    "الثالث؛ ولا يُقرَأ شيءٌ ممّا ههنا على القرآن ولا يُعَدّ استيفاءً لشرطها"
)

MARKOV_ORDER_INDUCTION_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "A_RUNG_THAT_MOVES_WITH_THE_ROUTE_IS_NOT_A_PROPERTY_OF_THE_SOURCE": (
        A_RUNG_THAT_MOVES_WITH_THE_ROUTE_IS_NOT_A_PROPERTY_OF_THE_SOURCE
    ),
    "A_PENALTY_ON_SPARSE_CELLS_IS_A_COMPARISON_NOT_A_TEST": (
        A_PENALTY_ON_SPARSE_CELLS_IS_A_COMPARISON_NOT_A_TEST
    ),
    "THE_HELD_OUT_LEG_IS_NOT_READ_WHEN_THE_TWO_SMOOTHINGS_DISAGREE": (
        THE_HELD_OUT_LEG_IS_NOT_READ_WHEN_THE_TWO_SMOOTHINGS_DISAGREE
    ),
    "A_CONDITION_FIXED_AFTER_A_PROBE_IS_NOT_A_PREDICTION": (
        A_CONDITION_FIXED_AFTER_A_PROBE_IS_NOT_A_PREDICTION
    ),
    "AN_AGREEING_SQUARE_IS_NOT_A_TRUE_ORDER": AN_AGREEING_SQUARE_IS_NOT_A_TRUE_ORDER,
    "MEASURING_MARKOV_ON_THE_ROOT_TABLE_DOES_NOT_OPEN_THE_CORPUS_GATE": (
        MEASURING_MARKOV_ON_THE_ROOT_TABLE_DOES_NOT_OPEN_THE_CORPUS_GATE
    ),
}


# ---------------------------------------------------------------------------
# الشرطُ المُودَع
# ---------------------------------------------------------------------------

THE_DECLARED_SMOOTHINGS: Final[tuple[float, float]] = (0.5, 1.0)
"""الملساران الجمعيّان المُعلَنان قبل العدّ؛ ولا ثالثَ يُضاف بعده."""

THE_REQUIRED_DRAW_FLOOR: Final[int] = 30
"""أدنى عددِ قسماتٍ تُقرَأ عندها المنزلة؛ وما دونه `UNREADABLE`."""

THE_REQUIRED_AGREEMENT_SHARE: Final[float] = 0.95
"""نصيبُ القسمات الذي يلزم اتّفاقُه مع درجةِ الكلّ ليُقال «انغلق»."""

THE_PREREGISTERED_COMMUTATION_CONDITION: Final[str] = (
    "شرطُ حكم هذه الوحدة، مكتوبٌ قبل جولتها المسجَّلة: يُقال «انغلق المربّعُ "
    "على هذا المصدر» إذا اجتمعت ثلاثٌ معًا — (أ) أن تكون الدرجةُ المختارةُ "
    "بمعيار العقوبة على المادّة كلِّها هي الدرجةَ الأكثرَ اختيارًا داخل "
    "المرئيّ في القسمات؛ و(ب) أن يبلغ نصيبُ القسمات الموافقةِ "
    f"{THE_REQUIRED_AGREEMENT_SHARE:.2f} فأكثر؛ و(ج) أن يكون الفائزُ بالتنبّؤ "
    "على المحجوب تلك الدرجةَ نفسَها عند الملسارَين المُعلَنَين كليهما. فإن "
    "تخلّفت واحدةٌ منهنّ قيل «لم ينغلق: الدرجةُ تتبع الطريق». ولا تُقرَأ "
    "المنزلةُ أصلًا إن نقصت القسماتُ عن "
    f"{THE_REQUIRED_DRAW_FLOOR} أو اختلف الملساران على الفائز، فتلك "
    "`UNREADABLE` لا انغلاقٌ ولا اختلاف. ولا يُمنَح ههنا وسمُ ترخيصٍ بحال، "
    "لأنّ المصدرَ واحدٌ والمقيسُ طريقُ الاستقراء لا اللغة."
)


# ---------------------------------------------------------------------------
# المادّةُ: الجذرُ مطويًّا إلى ثلاثة مخارج
# ---------------------------------------------------------------------------


@cache
def place_sequences() -> tuple[tuple[str, str, str], ...]:
    """الجذورُ المُودَعةُ مقروءةً سلاسلَ مخارجَ ثلاثيّة، بترتيبٍ ثابت.

    والمادّةُ هي ركيزةُ جبر الحقوق نفسُها (`algebra_substrate`)، لئلّا يُصطنَع
    معجمٌ ثانٍ فيختلف الرقمان على مصدرٍ واحد.
    """

    return tuple(
        (place_of(first), place_of(middle), place_of(last))
        for first, middle, last in algebra_substrate()
    )


@cache
def place_alphabet() -> tuple[str, ...]:
    """المخارجُ الحاضرةُ في المادّة مرتَّبةً؛ وهي أبجديّةُ السلاسل."""

    return tuple(sorted({place for row in place_sequences() for place in row}))


def _indexed(
    sample: Iterable[tuple[str, str, str]],
    alphabet: Sequence[str],
) -> list[tuple[int, int, int]]:
    order = {place: position for position, place in enumerate(alphabet)}
    rows: list[tuple[int, int, int]] = []
    for first, middle, last in sample:
        try:
            rows.append((order[first], order[middle], order[last]))
        except KeyError as unknown:  # pragma: no cover - حراسةُ أبجديّة
            raise MarkovOrderInductionError(
                f"المخرجُ {unknown.args[0]!r} خارجُ الأبجديّة المُعلَنة."
            ) from None
    return rows


def _counts(rows: Sequence[tuple[int, int, int]], width: int) -> list[float]:
    table = [0.0] * (width * width * width)
    for first, middle, last in rows:
        table[(first * width + middle) * width + last] += 1.0
    return table


# ---------------------------------------------------------------------------
# الدرجاتُ: درجاتُ الحرّيّة والملاءمة
# ---------------------------------------------------------------------------


def degrees_of_freedom(rung: LadderRung, width: int) -> int:
    """درجاتُ حرّيّة الدرجة على أبجديّةٍ عدّتُها ``width``، محسوبةً لا منقولة."""

    if width < 2:
        raise MarkovOrderInductionError("الأبجديّةُ دون حرفين لا سلّمَ عليها.")
    free = width - 1
    if rung is LadderRung.INDEPENDENT:
        return 3 * free
    if rung is LadderRung.CHAIN:
        return 3 * free + 2 * free * free
    if rung is LadderRung.TRIANGLE:
        return 3 * free + 3 * free * free
    return width**3 - 1


def _fit_independent(table: Sequence[float], width: int, total: float) -> list[float]:
    first = [0.0] * width
    middle = [0.0] * width
    last = [0.0] * width
    for a in range(width):
        for b in range(width):
            base = (a * width + b) * width
            for c in range(width):
                value = table[base + c]
                first[a] += value
                middle[b] += value
                last[c] += value
    fitted = [0.0] * (width * width * width)
    for a in range(width):
        for b in range(width):
            base = (a * width + b) * width
            head = first[a] * middle[b]
            for c in range(width):
                fitted[base + c] = head * last[c] / (total * total)
    return fitted


def _fit_chain(table: Sequence[float], width: int) -> list[float]:
    head = [0.0] * (width * width)
    tail = [0.0] * (width * width)
    waist = [0.0] * width
    for a in range(width):
        for b in range(width):
            base = (a * width + b) * width
            for c in range(width):
                value = table[base + c]
                head[a * width + b] += value
                tail[b * width + c] += value
                waist[b] += value
    fitted = [0.0] * (width * width * width)
    for a in range(width):
        for b in range(width):
            if waist[b] == 0.0:
                continue
            base = (a * width + b) * width
            share = head[a * width + b] / waist[b]
            for c in range(width):
                fitted[base + c] = share * tail[b * width + c]
    return fitted


def _pair_margins(
    table: Sequence[float], width: int
) -> tuple[list[float], list[float], list[float]]:
    head = [0.0] * (width * width)
    tail = [0.0] * (width * width)
    flank = [0.0] * (width * width)
    for a in range(width):
        for b in range(width):
            base = (a * width + b) * width
            for c in range(width):
                value = table[base + c]
                head[a * width + b] += value
                tail[b * width + c] += value
                flank[a * width + c] += value
    return head, tail, flank


_TRIANGLE_TOLERANCE: Final[float] = 1e-9
_TRIANGLE_SWEEPS: Final[int] = 512


def _fit_triangle(table: Sequence[float], width: int) -> list[float]:
    """تقديرُ درجة المثلّث بالتناسب التكراريّ؛ ولا حلَّ مغلقًا لها."""

    targets = _pair_margins(table, width)
    fitted = [1.0] * (width * width * width)
    for _ in range(_TRIANGLE_SWEEPS):
        gap = 0.0
        for which, target in enumerate(targets):
            current = [0.0] * (width * width)
            for a in range(width):
                for b in range(width):
                    base = (a * width + b) * width
                    for c in range(width):
                        current[_pair_key(which, a, b, c, width)] += fitted[base + c]
            for a in range(width):
                for b in range(width):
                    base = (a * width + b) * width
                    for c in range(width):
                        key = _pair_key(which, a, b, c, width)
                        if current[key] == 0.0:
                            fitted[base + c] = 0.0
                        else:
                            fitted[base + c] *= target[key] / current[key]
            for key in range(width * width):
                gap = max(gap, abs(current[key] - target[key]))
        if gap < _TRIANGLE_TOLERANCE:
            break
    return fitted


def _pair_key(which: int, a: int, b: int, c: int, width: int) -> int:
    if which == 0:
        return a * width + b
    if which == 1:
        return b * width + c
    return a * width + c


def fit_rung(
    rung: LadderRung,
    sample: Sequence[tuple[str, str, str]],
    alphabet: Sequence[str] | None = None,
) -> list[float]:
    """العدَدُ المتوقَّعُ في كلّ خليّةٍ تحت الدرجة، مقدَّرًا من التشكيلة نفسِها."""

    letters = tuple(alphabet) if alphabet is not None else place_alphabet()
    width = len(letters)
    rows = _indexed(sample, letters)
    if not rows:
        raise MarkovOrderInductionError("لا تُقدَّر درجةٌ على تشكيلةٍ خالية.")
    table = _counts(rows, width)
    total = float(len(rows))
    if rung is LadderRung.INDEPENDENT:
        return _fit_independent(table, width, total)
    if rung is LadderRung.CHAIN:
        return _fit_chain(table, width)
    if rung is LadderRung.TRIANGLE:
        return _fit_triangle(table, width)
    return list(table)


def log_likelihood(
    sample: Sequence[tuple[str, str, str]],
    fitted: Sequence[float],
    alphabet: Sequence[str] | None = None,
) -> float:
    """لوغاريتمُ الأرجحيّة المتعدِّدةِ الحدود، منسوبًا إلى عدّة التشكيلة."""

    letters = tuple(alphabet) if alphabet is not None else place_alphabet()
    width = len(letters)
    rows = _indexed(sample, letters)
    table = _counts(rows, width)
    total = float(len(rows))
    reading = 0.0
    for cell, observed in enumerate(table):
        if observed <= 0.0:
            continue
        expected = fitted[cell]
        if expected <= 0.0:
            return -math.inf
        reading += observed * math.log(expected / total)
    return reading


def information_criterion(
    rung: LadderRung,
    sample: Sequence[tuple[str, str, str]],
    alphabet: Sequence[str] | None = None,
) -> float:
    """معيارُ العقوبة: ‎−2·لوغاريتم الأرجحيّة + درجاتُ الحرّيّة × لوغاريتم العدّة.

    وهو ترتيبٌ بين معروضاتٍ لا اختبارُ فرض
    (`A_PENALTY_ON_SPARSE_CELLS_IS_A_COMPARISON_NOT_A_TEST`).
    """

    letters = tuple(alphabet) if alphabet is not None else place_alphabet()
    fitted = fit_rung(rung, sample, letters)
    reading = log_likelihood(sample, fitted, letters)
    if reading == -math.inf:  # pragma: no cover - لا تقع على درجاتِ السلّم
        return math.inf
    penalty = degrees_of_freedom(rung, len(letters)) * math.log(len(sample))
    return -2.0 * reading + penalty


def select_rung(
    sample: Sequence[tuple[str, str, str]],
    alphabet: Sequence[str] | None = None,
) -> LadderRung:
    """الصعودُ على الرتبة: أدنى درجةٍ في المعيار، وعند التساوي أضيقُ الدرجتين."""

    letters = tuple(alphabet) if alphabet is not None else place_alphabet()
    chosen: LadderRung | None = None
    best = math.inf
    for rung in THE_LADDER_ORDER:
        reading = information_criterion(rung, sample, letters)
        if reading < best - 1e-9:
            best = reading
            chosen = rung
    if chosen is None:  # pragma: no cover - حراسةُ اكتمال
        raise MarkovOrderInductionError("لم تُختَر درجةٌ، والسلّمُ غيرُ خالٍ.")
    return chosen


def held_out_winner(
    seen: Sequence[tuple[str, str, str]],
    hidden: Sequence[tuple[str, str, str]],
    smoothing: float,
    alphabet: Sequence[str] | None = None,
) -> LadderRung:
    """الدرجةُ الأعلى تنبّؤًا لما لم يُرَ، بملسارٍ جمعيٍّ مُعلَن."""

    if smoothing <= 0.0:
        raise MarkovOrderInductionError("الملسارُ الجمعيُّ موجبٌ، ولا يكون صفرًا.")
    letters = tuple(alphabet) if alphabet is not None else place_alphabet()
    width = len(letters)
    cells = width**3
    hidden_table = _counts(_indexed(hidden, letters), width)
    chosen: LadderRung | None = None
    best = -math.inf
    for rung in THE_LADDER_ORDER:
        fitted = fit_rung(rung, seen, letters)
        mass = math.fsum(fitted) + smoothing * cells
        reading = 0.0
        for cell, observed in enumerate(hidden_table):
            if observed > 0.0:
                reading += observed * math.log((fitted[cell] + smoothing) / mass)
        if reading > best + 1e-9:
            best = reading
            chosen = rung
    if chosen is None:  # pragma: no cover - حراسةُ اكتمال
        raise MarkovOrderInductionError("لم تُختَر درجةٌ على المحجوب.")
    return chosen


# ---------------------------------------------------------------------------
# مبرهنتا الاستيراد
# ---------------------------------------------------------------------------


def _woven_sample(width: int, seed: int) -> list[tuple[str, str, str]]:
    """تشكيلةٌ مصنوعةٌ فيها تفاعلٌ ثلاثيٌّ حقيقيّ، لئلّا يُفحَص السلّمُ على مستوٍ."""

    letters = [f"م{position}" for position in range(width)]
    stream = random.Random(seed)
    rows: list[tuple[str, str, str]] = []
    for _ in range(width * width * width * 4):
        first = stream.randrange(width)
        middle = (first + stream.randrange(width)) % width
        last = (first * middle + stream.randrange(width)) % width
        rows.append((letters[first], letters[middle], letters[last]))
    return rows


def verify_the_ladder_is_strictly_nested() -> bool:
    """فحصُ المبرهنة الأولى آليًّا: الحرّيّةُ تزيد والأرجحيّةُ لا تنقص.

    ويُفحَص على تشكيلةٍ مصنوعةٍ ذاتِ تفاعلٍ ثلاثيّ، وعلى أبجديّتين، لئلّا يكون
    الترتيبُ أثرَ حالةٍ واحدة. وسقوطُه سقوطُ التقدير لا سقوطُ دعوى لغويّة.
    """

    for width in (3, 4):
        letters = tuple(f"م{position}" for position in range(width))
        sample = _woven_sample(width, seed=20260926 + width)
        previous_freedom = -1
        previous_reading = -math.inf
        for rung in THE_LADDER_ORDER:
            freedom = degrees_of_freedom(rung, width)
            if freedom <= previous_freedom:
                raise MarkovOrderInductionError(
                    f"درجاتُ الحرّيّة لم تزد عند {rung.name}، فالسلّمُ غيرُ مرتَّب."
                )
            reading = log_likelihood(sample, fit_rung(rung, sample, letters), letters)
            if reading < previous_reading - 1e-6:
                raise MarkovOrderInductionError(
                    f"الأرجحيّةُ نقصت عند {rung.name}، فالاحتواءُ غيرُ متحقّق."
                )
            previous_freedom = freedom
            previous_reading = reading
    return True


def verify_the_triangle_fit_reproduces_every_margin() -> bool:
    """فحصُ المبرهنة الثانية آليًّا: حلُّ المثلّث يُعيد الهوامشَ الثلاثةَ كلَّها.

    والهوامشُ الثلاثةُ هي حدُّ النموذج نفسِه؛ فلو أعاد اثنين وأخطأ الثالثَ لكان
    المقيسُ سلسلةً بثوب مثلّث.
    """

    for width in (3, 4):
        letters = tuple(f"م{position}" for position in range(width))
        sample = _woven_sample(width, seed=20260926 + width)
        table = _counts(_indexed(sample, letters), width)
        fitted = _fit_triangle(table, width)
        for observed, expected in zip(
            _pair_margins(table, width), _pair_margins(fitted, width), strict=True
        ):
            for wanted, got in zip(observed, expected, strict=True):
                if abs(wanted - got) > 1e-6:
                    raise MarkovOrderInductionError(
                        "حلُّ المثلّث لم يُعِد هامشًا ثنائيًّا، فالتقديرُ ليس مثلّثًا."
                    )
        if math.isclose(math.fsum(fitted), 0.0):  # pragma: no cover - حراسة
            raise MarkovOrderInductionError("حلُّ المثلّث خالٍ من الكتلة.")
    return True


_THE_GATE_AS_READ_AT_IMPORT: Final[ChainReading] = token_markov_standing()
"""قراءةُ البوّابة قبل أيّ قياسٍ ههنا، لتكون المقارنةُ إلى ملحوظٍ لا إلى منزلةٍ مُرمَّزة."""


def the_corpus_gate_is_untouched() -> bool:
    """أزحزح شيءٌ من هذا القياس بوّابةَ ماركوف عمّا كانت عليه عند الاستيراد؟

    والمقارنةُ إلى القراءة الملحوظة لا إلى `BLOCKED` مُرمَّزة: فلو رُمِّزت
    لصار إيداعُ البايتات — وهو استيفاءُ شرطٍ لا عطب — يُقرَأ ههنا خللًا.
    """

    return token_markov_standing() == _THE_GATE_AS_READ_AT_IMPORT


# ---------------------------------------------------------------------------
# الطريقان، والمربّع
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SplitReading:
    """قراءةُ قسمةٍ واحدة: ما اختِير داخل المرئيّ، وما تنبّأ بالمحجوب."""

    seen_count: int
    hidden_count: int
    rung_inside_the_seen: LadderRung
    winners_by_smoothing: tuple[tuple[float, LadderRung], ...]

    def __post_init__(self) -> None:
        if self.seen_count <= 0 or self.hidden_count <= 0:
            raise MarkovOrderInductionError("قسمةٌ أحدُ طرفيها خالٍ ليست قسمة.")
        if len(self.winners_by_smoothing) != len(THE_DECLARED_SMOOTHINGS):
            raise MarkovOrderInductionError(
                "عددُ الفائزين لا يطابق عددَ الملسارات المُعلَنة."
            )

    @property
    def smoothings_agree(self) -> bool:
        """أاتّفق الملساران على فائزٍ واحد؟ وعليه يدور قبولُ الطرف."""

        return len({winner for _, winner in self.winners_by_smoothing}) == 1

    @property
    def held_out_winner(self) -> LadderRung | None:
        """الفائزُ المتّفَقُ عليه، أو لا شيءَ إن اختلف الملساران."""

        if not self.smoothings_agree:
            return None
        return self.winners_by_smoothing[0][1]


@dataclass(frozen=True)
class CommutationReading:
    """قراءةُ المربّع: طرفاه، وحارسُه، ومنزلتُه المُشتقّةُ من الشرط المُودَع."""

    rung_on_the_whole: LadderRung
    splits: tuple[SplitReading, ...]
    condition: str = THE_PREREGISTERED_COMMUTATION_CONDITION

    def __post_init__(self) -> None:
        if not self.condition.strip():
            raise MarkovOrderInductionError("قراءةُ مربّعٍ بلا شرطٍ مكتوب.")

    @property
    def agreement_share(self) -> float:
        """نصيبُ القسمات التي وافقت درجتُها درجةَ الكلّ."""

        if not self.splits:
            return 0.0
        agreeing = sum(
            1
            for split in self.splits
            if split.rung_inside_the_seen is self.rung_on_the_whole
        )
        return agreeing / len(self.splits)

    @property
    def modal_rung_inside_the_seen(self) -> LadderRung:
        """الدرجةُ الأكثرُ اختيارًا داخل المرئيّ؛ وعند التساوي أضيقُهما."""

        tally = {rung: 0 for rung in THE_LADDER_ORDER}
        for split in self.splits:
            tally[split.rung_inside_the_seen] += 1
        return max(THE_LADDER_ORDER, key=lambda rung: (tally[rung], -rung_index(rung)))

    @property
    def held_out_rung(self) -> LadderRung | None:
        """الفائزُ بالتنبّؤ إن اتّفقت عليه كلُّ القسمات والملسارات، وإلّا فلا."""

        winners = {split.held_out_winner for split in self.splits}
        if len(winners) != 1:
            return None
        return next(iter(winners))

    @property
    def standing(self) -> CommutationStanding:
        """منزلةُ المربّع بالشرط المُودَع وحدَه، لا بتقديرٍ بعد النظر."""

        if len(self.splits) < THE_REQUIRED_DRAW_FLOOR:
            return CommutationStanding.UNREADABLE
        if any(not split.smoothings_agree for split in self.splits):
            return CommutationStanding.UNREADABLE
        if self.modal_rung_inside_the_seen is not self.rung_on_the_whole:
            return CommutationStanding.DOES_NOT_COMMUTE
        if self.agreement_share < THE_REQUIRED_AGREEMENT_SHARE:
            return CommutationStanding.DOES_NOT_COMMUTE
        if self.held_out_rung is not self.rung_on_the_whole:
            return CommutationStanding.DOES_NOT_COMMUTE
        return CommutationStanding.COMMUTES_ON_THIS_SOURCE

    def rung_by_direction(self) -> Mapping[InductionDirection, LadderRung | None]:
        """طرفا المربّع صريحَين: ما انتهى إليه كلُّ ترتيبٍ من الترتيبين."""

        return {
            InductionDirection.ON_THEN_FOR: self.rung_on_the_whole,
            InductionDirection.FOR_THEN_ON: self.modal_rung_inside_the_seen,
        }


def rung_index(rung: LadderRung) -> int:
    """موضعُ الدرجة في السلّم؛ وعليه يُفضَّل الأضيقُ عند التساوي."""

    return THE_LADDER_ORDER.index(rung)


def measure_commutation(
    *,
    draws: int = 60,
    seen_share: float = 0.5,
    seed: int = 20260926,
    sample: Sequence[tuple[str, str, str]] | None = None,
) -> CommutationReading:
    """قياسُ المربّع: «على ثمّ لـ» في وجه «لـ ثمّ على» على المادّة نفسِها.

    ``seen_share`` نصيبُ المرئيّ من كلّ قسمة، و``draws`` عدّةُ القسمات؛ وكلاهما
    مُعلَنٌ في التوقيع لا مخبوءٌ في الجسم.
    """

    material = tuple(sample) if sample is not None else place_sequences()
    if draws <= 0:
        raise MarkovOrderInductionError("عدّةُ القسمات موجبةٌ، ولا تكون صفرًا.")
    if not 0.0 < seen_share < 1.0:
        raise MarkovOrderInductionError("نصيبُ المرئيّ بين الصفر والواحد حصرًا.")
    letters = tuple(sorted({place for row in material for place in row}))
    whole = select_rung(material, letters)
    stream = random.Random(seed)
    positions = list(range(len(material)))
    cut = int(len(material) * seen_share)
    if cut <= 0 or cut >= len(material):
        raise MarkovOrderInductionError("القسمةُ لا تترك طرفًا خاليًا.")
    splits: list[SplitReading] = []
    for _ in range(draws):
        stream.shuffle(positions)
        seen = [material[position] for position in positions[:cut]]
        hidden = [material[position] for position in positions[cut:]]
        winners = tuple(
            (smoothing, held_out_winner(seen, hidden, smoothing, letters))
            for smoothing in THE_DECLARED_SMOOTHINGS
        )
        splits.append(
            SplitReading(
                seen_count=len(seen),
                hidden_count=len(hidden),
                rung_inside_the_seen=select_rung(seen, letters),
                winners_by_smoothing=winners,
            )
        )
    return CommutationReading(rung_on_the_whole=whole, splits=tuple(splits))


@dataclass(frozen=True)
class CrossoverRow:
    """صفٌّ من مسح العتبة: كم رُئِي، وأيَّ درجةٍ اختار، وبأيّ إجماع."""

    seen_count: int
    rungs: tuple[LadderRung, ...]

    def __post_init__(self) -> None:
        if not self.rungs:
            raise MarkovOrderInductionError("صفُّ مسحٍ بلا اختيارٍ واحد.")

    @property
    def is_unanimous(self) -> bool:
        """أاتّفقت السحباتُ كلُّها على درجةٍ واحدة عند هذا الحجم؟"""

        return len(set(self.rungs)) == 1


def rung_crossover_scan(
    *,
    shares: Sequence[float] = (0.25, 0.5, 0.7, 0.8, 0.9, 1.0),
    draws: int = 8,
    seed: int = 20260926,
    sample: Sequence[tuple[str, str, str]] | None = None,
) -> tuple[CrossoverRow, ...]:
    """مسحُ الدرجة المختارة في حجومٍ صاعدة، ليُرى أين تنقلب لا أن يُدَّعى ثباتُها.

    وهذا المسحُ هو الشاهدُ على أنّ خلافَ الطرفين تابعٌ للحجم لا خللٌ في التقدير
    (`A_RUNG_THAT_MOVES_WITH_THE_ROUTE_IS_NOT_A_PROPERTY_OF_THE_SOURCE`).
    """

    material = tuple(sample) if sample is not None else place_sequences()
    letters = tuple(sorted({place for row in material for place in row}))
    stream = random.Random(seed)
    positions = list(range(len(material)))
    rows: list[CrossoverRow] = []
    for share in shares:
        if not 0.0 < share <= 1.0:
            raise MarkovOrderInductionError("نصيبُ المسح بين الصفر والواحد.")
        cut = int(len(material) * share)
        if cut < 2:
            raise MarkovOrderInductionError("حجمٌ دون جذرين لا تُقدَّر عليه درجة.")
        chosen: list[LadderRung] = []
        for _ in range(1 if share == 1.0 else draws):
            stream.shuffle(positions)
            chosen.append(
                select_rung(
                    [material[position] for position in positions[:cut]], letters
                )
            )
        rows.append(CrossoverRow(seen_count=cut, rungs=tuple(chosen)))
    return tuple(rows)


# ---------------------------------------------------------------------------
# فحصُ المبرهنات وحراسةُ الخمول عند الاستيراد
# ---------------------------------------------------------------------------


def _refuse_operative_vocabulary() -> None:
    """حراسةُ الخمول: لا اسمَ ههنا يَعِد بولادةٍ أو ترخيصٍ أو تجميد."""

    for name in __all__:
        if name.startswith(("birth_", "licence_", "freeze_", "grant_")):
            raise MarkovOrderInductionError(
                f"الاسمُ {name!r} يَعِد بسلطةٍ لا تملكها هذه الوحدة."
            )


_refuse_operative_vocabulary()
verify_the_ladder_is_strictly_nested()
verify_the_triangle_fit_reproduces_every_margin()
