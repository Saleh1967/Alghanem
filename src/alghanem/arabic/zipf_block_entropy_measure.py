"""الدالّةُ الفراكتاليّة المطلوبة — زِبف وإنتروبيا الكتل — مقيسةً على بايتاتنا.

وردت دعوى: «زِبف مؤكَّد: α = 1.026 بـ R² = 0.979 على 15,490 لفظًا مميّزًا من
77,801 كلمةٍ نظيفة، وإنتروبيا كتلٍ تهبط من 4.115 إلى 1.910» — مقيسةً على
`mujammad.norm.txt`. وليست تلك البايتاتُ في هذه الشجرة، فلا تُصدَّق ههنا ولا
تُكذَّب بغير حساب. وهذه الوحدةُ **تُجري المقياسين نفسَيهما** على البايتات
المختومة عندنا — `corpora/quran-simple-enhanced.txt` عبر بابها المبصوم وحدَه —
ثمّ تُقابل المنقولَ بالمقيس بحدِّ تسامحٍ مُعلَنٍ قبل المقابلة. ويفترق ههنا
أربعةٌ كانت تُقرأ «دالّةً فراكتاليّةً» واحدة::

    AnExponentWithItsWindow != AnExponentWithoutOne
    ADeclaredStride         != AnInertStride
    AFallingEntropyLadder   != AMeasuredFractalDimension
    AnotherCorpusFigure     != AFigureOnOurBytes

**أوّلًا: الأسُّ دالّةٌ في نافذة الرتب، لا ثابتٌ للنصّ.** يُقاس ههنا انحدارُ
`log f` على `log r` بالمربّعات الصغرى على سبع نوافذَ مُعلَنةٍ من البايتات
نفسِها، فيخرج سُلَّمٌ لا رقم:

| النافذة | 100 | 500 | 1,000 | 2,000 | 5,000 | 10,000 | كلُّ الرتب |
|---|---|---|---|---|---|---|---|
| \\|α\\| | 0.7766 | 0.8847 | 0.9239 | 0.9507 | 0.9734 | 1.0041 | 0.8678 |
| R² | 0.9759 | 0.9922 | 0.9944 | 0.9956 | 0.9915 | 0.9771 | 0.9469 |

فالأسُّ على بايتةٍ واحدةٍ يتراوح بين **0.7766 و1.0041** بحسب النافذة وحدَها،
و R² بين **0.9469 و0.9956**. فمن نشر «α = 1.026 بـ R² = 0.979» بلا نافذةٍ
مُعلَنةٍ نشر رقمًا لا يُقابَل: لأنّ المقابلَ له عندنا سبعةٌ لا واحد
(`AN_EXPONENT_WITHOUT_ITS_WINDOW_IS_NOT_A_CONSTANT`).

**وثانيًا: ومع ذلك يقع المنقولُ في سُلَّمنا، وموضعُه يُسمّى.** النافذةُ
العاشرةُ الألفيّة تُخرِج **|α| = 1.0041 و R² = 0.9771**، فيبعد المنقولُ عنها
0.0219 في الأسّ و0.0019 في جودة الربط — داخلَ حدِّ التسامح المُعلَن في
الاثنين معًا، وحدَه من بين النوافذ السبع. وهذا **موافقةُ نافذةٍ بعينها لا
موافقةُ نصّ**: فمقامُهم 77,801 كلمةً و15,490 لفظًا مميّزًا، ومقامُنا 82,532
كلمةً و18,201 لفظًا؛ فالاتّفاقُ يُسجَّل بموضعه ولا يُقرأ تصديقًا لمقامٍ لم
يصل (`A_FIGURE_MEASURED_ON_ANOTHER_CORPUS_DOES_NOT_CROSS_TO_OURS`).

**وثالثًا: التحيّزُ المُعلَنُ ليس تحيّزًا خاملًا.** أُعلن في الدعوى أنّ
عيّنةَ الإنتروبيا منتظمةٌ بخطوة سبعة (`i += 7`)، وأُعلِن أنّه «معلَنٌ لا
مستور». والإعلانُ صدقٌ، لكنّه لا يُغني عن **تسعيره**: تُقاس ههنا سُلَّمُ
`H(k)/k` لِـ `k` من واحدٍ إلى ثمانيةٍ مرّتين — على كلّ موضعٍ، وبخطوة سبعة —
فيتبيّن أنّ الخطوةَ تُنقِص **0.130 بتٍّ في الحرف عند `k = 8`** ولا تكاد تمسّ
`k = 1`. فأثرُ الوسيط يكبر مع المقياس، وهو الاتّجاه الذي يُقرأ منه «التدرّج»
نفسُه؛ فلا يُنشَر سُلَّمُ كتلٍ إلّا وخطوةُ عيّنته معه
(`A_DECLARED_STRIDE_IS_PRICED_NOT_MERELY_DECLARED`). وأمّا سُلَّمُهم نفسُه
فيُقابَل بسُلَّمنا على خطوتهم، فيخالف في **سبعٍ من ثمانٍ** بحدِّ نصفِ عُشرِ
البتّ، ولا يوافق إلّا عند `k = 8`؛ فالذي يوافق من الدعوى موضعٌ في سُلَّمٍ لا
السُّلَّمُ كلُّه.

**ورابعًا: طيُّ الهمزة وفكُّ الشدّة لا يُعيدان رسمَ التردّدات ههنا.** قيل إنّ
التطبيعَ «أعاد رسمَ الترددات» فصار للنظيف زِبفُه الخاصّ. وهذا يُقاس لا
يُقال: يُعاد القياسُ على مفتاحٍ ثانٍ يطوي الهمزات إلى الألف ويفكّ الشدّة إلى
تكرارِ الحرف، فتتحرّك المفرداتُ **لفظين اثنين من 18,201**، ويتحرّك الأسُّ
أقلَّ من 0.001 على كلّ نافذةٍ من السبع. فالدعوى مردودةٌ على بايتاتنا بالعدد لا
بالرأي (`THE_FOLDING_MOVES_TWO_TYPES_AND_NOT_THE_EXPONENT`).

**وخامسًا: سُلَّمٌ هابطٌ ليس بُعدًا فراكتاليًّا.** `H(k)/k` يهبط في كلِّ
تيّارٍ غيرِ مستقلِّ الرموز، وهبوطُه شاهدٌ على الارتباط لا قياسٌ لبُعدٍ: لا
يُقاس ههنا بُعدُ هاوسدورف، ولا أسُّ هيرست، ولا يُخرِج هذا الملفُّ لفظَ
«فراكتال» حكمًا على النصّ. وما يُخرَج ثلاثةٌ لا رابعَ لها: سُلَّمُ أسٍّ
بنوافذه، وسُلَّمُ إنتروبيا كتلٍ بخطوته، وأحكامُ مقابلةٍ بحدودها
(`A_FALLING_BLOCK_ENTROPY_LADDER_IS_NOT_A_MEASURED_FRACTAL_DIMENSION`).

**خمولٌ سلطويّ**: لا ولادةَ هنا ولا حكمَ ولادةٍ ولا تجميدَ `E0`، ولا استيرادَ
من `kernel/` ولا من `program/`، ولا تزحزح هذه الوحدةُ بوّابةَ ماركوف عمّا
كانت عليه؛ وكلُّ إنتروبيا ههنا إنتروبيا **كتلٍ من محارفَ متجاورة** على تيّار
المحارف، لا إنتروبيا شرطيّةٌ على توكناتٍ ولا سلسلةُ ماركوف.
"""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass, fields
from enum import Enum
from functools import lru_cache
from typing import Final

from .markov_readiness_gate import ChainReading, token_markov_standing
from .quran_corpus_word_total import read_quran_corpus_bytes

__all__ = [
    "AN_EXPONENT_WITHOUT_ITS_WINDOW_IS_NOT_A_CONSTANT",
    "A_DECLARED_STRIDE_IS_PRICED_NOT_MERELY_DECLARED",
    "A_FALLING_BLOCK_ENTROPY_LADDER_IS_NOT_A_MEASURED_FRACTAL_DIMENSION",
    "A_FIGURE_MEASURED_ON_ANOTHER_CORPUS_DOES_NOT_CROSS_TO_OURS",
    "THE_BLOCK_SIZES",
    "THE_ENTROPY_TOLERANCE",
    "THE_EXPONENT_TOLERANCE",
    "THE_FOLDING_MOVES_TWO_TYPES_AND_NOT_THE_EXPONENT",
    "THE_LADDER_AT_MEASUREMENT",
    "THE_QUOTED_BLOCK_ENTROPY",
    "THE_QUOTED_ZIPF",
    "THE_R_SQUARED_TOLERANCE",
    "THE_RANK_WINDOWS",
    "THE_STRIDE_LADDER_AT_MEASUREMENT",
    "THE_VOCABULARY_AT_MEASUREMENT",
    "ZIPF_BLOCK_ENTROPY_NAMED_RESIDUALS",
    "BlockEntropyLadder",
    "QuotedBlockEntropy",
    "QuotedZipf",
    "SamplingRule",
    "StreamKey",
    "TypeTokenCensus",
    "Verdict",
    "WindowVerdict",
    "ZipfBlockEntropyError",
    "ZipfFit",
    "block_entropy_ladder",
    "the_block_entropy_comparison",
    "the_corpus_gate_is_untouched",
    "the_exponent_is_negative_on_every_window",
    "the_folding_moves_the_exponent_by",
    "the_ladders_have_drifted",
    "the_quoted_pair_against_our_windows",
    "the_stride_shift",
    "the_vocabulary_has_drifted",
    "the_window_that_hosts_the_quoted_pair",
    "vocabulary_census",
    "zipf_fit_for",
    "zipf_ladder",
]


class ZipfBlockEntropyError(ValueError):
    """رُفض مدخلٌ خارج مفردات هذه الوحدة؛ ولا يُحمَل على أقرب حالة."""


# ---------------------------------------------------------------------------
# المفاتيحُ والقواعدُ، مُعلَنةً قبل أن يُقرأ رقم
# ---------------------------------------------------------------------------


THE_HAMZA_CARRIERS: Final[str] = "\u0623\u0625\u0622\u0671"
"""الهمزاتُ المرسومةُ على الألف وما يُطوى معها؛ تُطوى إلى ألفٍ في المفتاح الثاني."""

THE_ALIF: Final[str] = "\u0627"
THE_SHADDA: Final[str] = "\u0651"
THE_TATWEEL: Final[str] = "\u0640"

THE_ARABIC_BASE_LETTERS: Final[str] = "".join(
    chr(codepoint) for codepoint in range(0x0621, 0x064B)
)

THE_RANK_WINDOWS: Final[tuple[int, ...]] = (100, 500, 1000, 2000, 5000, 10000, 0)
"""نوافذُ الرتب التي يُقاس عليها الانحدار؛ و**الصفرُ** يعني كلَّ الرتب."""

THE_BLOCK_SIZES: Final[tuple[int, ...]] = (1, 2, 3, 4, 5, 6, 7, 8)
"""أحجامُ الكتل كما في الدعوى: من حرفٍ إلى ثمانيةٍ لا أقلَّ ولا أكثر."""

THE_EXPONENT_TOLERANCE: Final[float] = 0.05
"""حدُّ التسامح في الأسّ، مُعلَنٌ قبل المقابلة لا بعد رؤية الفارق."""

THE_R_SQUARED_TOLERANCE: Final[float] = 0.01
"""حدُّ التسامح في جودة الربط، مُعلَنٌ قبل المقابلة."""

THE_ENTROPY_TOLERANCE: Final[float] = 0.05
"""حدُّ التسامح في `H(k)/k` بالبتّ في الحرف، مُعلَنٌ قبل المقابلة."""


class StreamKey(Enum):
    """مفتاحُ التيّار: أيُّ رسمٍ يُقاس؟ والاختيارُ يُعلَن ولا يُضمَر."""

    AS_SEALED = "كما_خُتمت_البايتات"
    """التيّارُ كما هو في المدوّنة المبصومة، بلا طيٍّ ولا فكّ."""

    FOLDED_AND_UNTIED = "مطويُّ_الهمزة_مفكوكُ_الشدّة"
    """الهمزاتُ تُطوى إلى ألفٍ، والشدّةُ تُفَكّ تكرارًا للحرف، والتطويلُ يُسقَط."""


class SamplingRule(Enum):
    """قاعدةُ العيّنة في سُلَّم الكتل: كلُّ موضعٍ، أم خطوةُ سبعةٍ كما أُعلن."""

    EVERY_POSITION = "كلُّ_موضع"
    EVERY_SEVENTH = "خطوةُ_سبعة"

    @property
    def stride(self) -> int:
        return 1 if self is SamplingRule.EVERY_POSITION else 7


class Verdict(Enum):
    """حكمُ مقابلةٍ واحدة؛ يُشتَقّ بالحساب ولا يُكتَب حقلًا."""

    AGREES = "يوافق"
    CONTRADICTS = "يخالف"


# ---------------------------------------------------------------------------
# المنقولُ، مُودَعًا بنصّه ومقامِه
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class QuotedZipf:
    """دعوى زِبف كما وردت: أسٌّ وجودةُ ربطٍ ومقامٌ ليس في هذه الشجرة."""

    corpus: str
    certificate: str
    magnitude: float
    r_squared: float
    types: int
    tokens: int

    def __post_init__(self) -> None:
        if not self.corpus.strip() or not self.certificate.strip():
            raise ZipfBlockEntropyError("نقلٌ بلا مقامٍ ولا شهادةٍ لا يُودَع.")
        if self.magnitude <= 0.0:
            raise ZipfBlockEntropyError("أسُّ زِبف يُودَع بمقداره موجبًا.")
        if not 0.0 <= self.r_squared <= 1.0:
            raise ZipfBlockEntropyError("جودةُ ربطٍ خارج [0، 1] لا تُودَع.")
        if self.types < 1 or self.tokens < self.types:
            raise ZipfBlockEntropyError("مفرداتٌ أكثرُ من الكلمات لا تُودَع.")


THE_QUOTED_ZIPF: Final[QuotedZipf] = QuotedZipf(
    corpus="mujammad.norm.txt",
    certificate="CERT-FR",
    magnitude=1.026,
    r_squared=0.979,
    types=15490,
    tokens=77801,
)
"""الدعوى بنصّها؛ ونافذةُ رتبها غيرُ مُعلَنةٍ فيها، وذلك أوّلُ ما يُسجَّل عنها."""


@dataclass(frozen=True, slots=True)
class QuotedBlockEntropy:
    """سُلَّمُ الكتل كما ورد: ثماني قيمٍ، وخطوةُ عيّنةٍ مُعلَنةٌ في الدعوى."""

    corpus: str
    certificate: str
    per_character: tuple[float, ...]
    declared_stride: int

    def __post_init__(self) -> None:
        if len(self.per_character) != len(THE_BLOCK_SIZES):
            raise ZipfBlockEntropyError("سُلَّمُ الكتل ثماني قيمٍ لا تزيد ولا تنقص.")
        if any(value <= 0.0 for value in self.per_character):
            raise ZipfBlockEntropyError("إنتروبيا دون الصفر لا تُودَع.")
        if self.declared_stride < 1:
            raise ZipfBlockEntropyError("خطوةُ عيّنةٍ دون الواحد لا تُودَع.")


THE_QUOTED_BLOCK_ENTROPY: Final[QuotedBlockEntropy] = QuotedBlockEntropy(
    corpus="mujammad.norm.txt",
    certificate="CERT-FR",
    per_character=(4.115, 3.943, 3.671, 3.271, 2.843, 2.464, 2.158, 1.910),
    declared_stride=7,
)
"""سُلَّمُهم بنصّه وخطوتِه؛ والخطوةُ تُسعَّر ههنا على بايتاتنا لا تُقبَل وصفًا."""


# ---------------------------------------------------------------------------
# القراءةُ من البايتات المختومة
# ---------------------------------------------------------------------------


@lru_cache(maxsize=len(StreamKey))
def _stream(key: StreamKey) -> str:
    text = read_quran_corpus_bytes().decode("utf-8")
    if key is StreamKey.AS_SEALED:
        return text
    return _fold_and_untie(text)


def _fold_and_untie(text: str) -> str:
    """طيُّ الهمزة إلى ألفٍ، وفكُّ الشدّة تكرارًا للحرف، وإسقاطُ التطويل."""

    folded: list[str] = []
    last_base: str | None = None
    for character in text:
        if character == THE_TATWEEL:
            continue
        if character == THE_SHADDA:
            if last_base is not None:
                folded.append(last_base)
            continue
        if character in THE_HAMZA_CARRIERS:
            character = THE_ALIF
        folded.append(character)
        if character in THE_ARABIC_BASE_LETTERS:
            last_base = character
    return "".join(folded)


@lru_cache(maxsize=len(StreamKey))
def _descending_frequencies(key: StreamKey) -> tuple[int, ...]:
    counts = Counter(_stream(key).split())
    return tuple(sorted(counts.values(), reverse=True))


@dataclass(frozen=True, slots=True)
class TypeTokenCensus:
    """مقامُ القياس: كلماتُه ومفرداتُه وما ورد منها مرّةً واحدة."""

    key: StreamKey
    tokens: int
    types: int
    hapax: int

    def __post_init__(self) -> None:
        if self.tokens < self.types or self.types < self.hapax or self.hapax < 0:
            raise ZipfBlockEntropyError("مقامٌ لا يستقيم ترتيبُ أعداده لا يُودَع.")


def vocabulary_census(key: StreamKey = StreamKey.AS_SEALED) -> TypeTokenCensus:
    """كلماتُ البايتات المختومة ومفرداتُها على مفتاحٍ مُعلَن."""

    frequencies = _descending_frequencies(key)
    return TypeTokenCensus(
        key=key,
        tokens=sum(frequencies),
        types=len(frequencies),
        hapax=sum(1 for value in frequencies if value == 1),
    )


@dataclass(frozen=True, slots=True)
class ZipfFit:
    """انحدارُ زِبف على نافذةٍ مُعلَنة؛ الأسُّ سالبٌ ومقدارُه يُشتَقّ."""

    key: StreamKey
    window: int
    ranks: int
    exponent: float
    r_squared: float

    def __post_init__(self) -> None:
        if self.window < 0:
            raise ZipfBlockEntropyError("نافذةٌ سالبةٌ لا تُقاس؛ والصفرُ كلُّ الرتب.")
        if self.ranks < 2:
            raise ZipfBlockEntropyError("رتبةٌ واحدةٌ لا يُقام عليها انحدار.")
        if not 0.0 <= self.r_squared <= 1.0:
            raise ZipfBlockEntropyError("جودةُ ربطٍ خارج [0، 1] لا تُقرأ.")

    @property
    def magnitude(self) -> float:
        """مقدارُ الأسّ؛ يُقابَل به المنقولُ لأنّه يُنشَر موجبًا في الدعاوى."""

        return abs(self.exponent)

    @property
    def is_falling(self) -> bool:
        """أينحدر التردُّدُ بالرتبة كما يقتضي زِبف؟ سؤالٌ يُحسَب لا يُوصَف."""

        return self.exponent < 0.0


def _least_squares(xs: tuple[float, ...], ys: tuple[float, ...]) -> tuple[float, float]:
    """انحدارُ المربّعات الصغرى: يُخرِج الميلَ وجودةَ الربط، ولا يستورد مكتبة."""

    count = len(xs)
    mean_x = sum(xs) / count
    mean_y = sum(ys) / count
    variance_x = sum((x - mean_x) ** 2 for x in xs)
    if variance_x <= 0.0:
        raise ZipfBlockEntropyError("رتبٌ بلا تباينٍ لا يُقام عليها انحدار.")
    slope = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys)) / variance_x
    intercept = mean_y - slope * mean_x
    residual = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(xs, ys))
    total = sum((y - mean_y) ** 2 for y in ys)
    if total <= 0.0:
        raise ZipfBlockEntropyError("تردّداتٌ متساويةٌ لا تُخرِج جودةَ ربط.")
    return slope, 1.0 - residual / total


@lru_cache(maxsize=len(StreamKey) * len(THE_RANK_WINDOWS))
def zipf_fit_for(window: int, key: StreamKey = StreamKey.AS_SEALED) -> ZipfFit:
    """انحدارُ نافذةٍ بعينها؛ والصفرُ يُقرأ «كلَّ الرتب» لا نافذةً خالية."""

    if window not in THE_RANK_WINDOWS:
        raise ZipfBlockEntropyError(
            "نافذةٌ خارج `THE_RANK_WINDOWS` لا تُقاس؛ والنوافذُ تُعلَن قبل القياس."
        )
    frequencies = _descending_frequencies(key)
    if window:
        frequencies = frequencies[:window]
    xs = tuple(math.log(rank) for rank in range(1, len(frequencies) + 1))
    ys = tuple(math.log(value) for value in frequencies)
    slope, r_squared = _least_squares(xs, ys)
    return ZipfFit(
        key=key,
        window=window,
        ranks=len(frequencies),
        exponent=slope,
        r_squared=r_squared,
    )


def zipf_ladder(key: StreamKey = StreamKey.AS_SEALED) -> tuple[ZipfFit, ...]:
    """سُلَّمُ النوافذ السبع على مفتاحٍ واحد؛ وهو الجوابُ لا الرقمُ المفرد."""

    return tuple(zipf_fit_for(window, key) for window in THE_RANK_WINDOWS)


def the_exponent_is_negative_on_every_window(
    key: StreamKey = StreamKey.AS_SEALED,
) -> bool:
    """أيهبط التردُّدُ بالرتبة على النوافذ كلِّها؟ شرطُ زِبف الأوّل."""

    return all(fit.is_falling for fit in zipf_ladder(key))


def the_folding_moves_the_exponent_by() -> float:
    """أكبرُ ما حرّكه الطيُّ والفكُّ في مقدار الأسّ عبر النوافذ السبع."""

    return max(
        abs(
            zipf_fit_for(window, StreamKey.AS_SEALED).magnitude
            - zipf_fit_for(window, StreamKey.FOLDED_AND_UNTIED).magnitude
        )
        for window in THE_RANK_WINDOWS
    )


# ---------------------------------------------------------------------------
# إنتروبيا الكتل، بخطوةِ عيّنتها مُعلَنةً معها
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class BlockEntropyLadder:
    """سُلَّمُ `H(k)/k` بمفتاحه وخطوته؛ ولا تُنشَر قيمةٌ منه بغيرهما."""

    key: StreamKey
    rule: SamplingRule
    per_character: tuple[float, ...]

    def __post_init__(self) -> None:
        if len(self.per_character) != len(THE_BLOCK_SIZES):
            raise ZipfBlockEntropyError("سُلَّمُ الكتل يُقاس على الأحجام المُعلَنة كلِّها.")
        if any(value <= 0.0 for value in self.per_character):
            raise ZipfBlockEntropyError("إنتروبيا دون الصفر لا تُقرأ.")

    @property
    def is_strictly_falling(self) -> bool:
        """أيهبط `H(k)/k` في كلّ درجةٍ؟ شاهدُ ارتباطٍ لا قياسُ بُعد."""

        values = self.per_character
        return all(later < earlier for earlier, later in zip(values, values[1:]))


@lru_cache(maxsize=len(StreamKey) * len(SamplingRule))
def block_entropy_ladder(
    key: StreamKey = StreamKey.AS_SEALED,
    rule: SamplingRule = SamplingRule.EVERY_POSITION,
) -> BlockEntropyLadder:
    """إنتروبيا الكتل على تيّار المحارف، مقسومةً على حجم الكتلة."""

    stream = _stream(key)
    stride = rule.stride
    values: list[float] = []
    for size in THE_BLOCK_SIZES:
        last = len(stream) - size + 1
        if last < 1:
            raise ZipfBlockEntropyError("تيّارٌ أقصرُ من كتلته لا يُقاس.")
        counts = Counter(
            stream[index : index + size] for index in range(0, last, stride)
        )
        total = sum(counts.values())
        entropy = -sum(
            (value / total) * math.log2(value / total) for value in counts.values()
        )
        values.append(entropy / size)
    return BlockEntropyLadder(key=key, rule=rule, per_character=tuple(values))


def the_stride_shift(key: StreamKey = StreamKey.AS_SEALED) -> tuple[float, ...]:
    """ما تُنقِصه خطوةُ السبعة من كلّ درجةٍ؛ موجبٌ يعني أنّها تُهبِط الرقم."""

    dense = block_entropy_ladder(key, SamplingRule.EVERY_POSITION).per_character
    sparse = block_entropy_ladder(key, SamplingRule.EVERY_SEVENTH).per_character
    return tuple(before - after for before, after in zip(dense, sparse))


def the_stride_is_inert_within(tolerance: float) -> bool:
    """أتبقى خطوةُ السبعة تحت حدٍّ مُعلَنٍ في الدرجات كلِّها؟"""

    if tolerance <= 0.0:
        raise ZipfBlockEntropyError("حدُّ خمولٍ دون الصفر لا يُفحَص به.")
    return all(abs(shift) < tolerance for shift in the_stride_shift())


# ---------------------------------------------------------------------------
# المقابلة: المنقولُ يُقابَل بالمقيس بحدودٍ مُعلَنةٍ قبلها
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class WindowVerdict:
    """مقابلةُ المنقول بنافذةٍ واحدة؛ الحكمُ صفةٌ مشتقّةٌ لا حقلٌ مكتوب."""

    fit: ZipfFit
    exponent_gap: float
    r_squared_gap: float

    @property
    def exponent_standing(self) -> Verdict:
        return (
            Verdict.AGREES
            if abs(self.exponent_gap) <= THE_EXPONENT_TOLERANCE
            else Verdict.CONTRADICTS
        )

    @property
    def r_squared_standing(self) -> Verdict:
        return (
            Verdict.AGREES
            if abs(self.r_squared_gap) <= THE_R_SQUARED_TOLERANCE
            else Verdict.CONTRADICTS
        )

    @property
    def both_agree(self) -> bool:
        return (
            self.exponent_standing is Verdict.AGREES
            and self.r_squared_standing is Verdict.AGREES
        )


def the_quoted_pair_against_our_windows(
    key: StreamKey = StreamKey.AS_SEALED,
) -> tuple[WindowVerdict, ...]:
    """المنقولُ (1.026 · 0.979) مقابَلًا بالنوافذ السبع، نافذةً نافذة."""

    return tuple(
        WindowVerdict(
            fit=fit,
            exponent_gap=fit.magnitude - THE_QUOTED_ZIPF.magnitude,
            r_squared_gap=fit.r_squared - THE_QUOTED_ZIPF.r_squared,
        )
        for fit in zipf_ladder(key)
    )


def the_window_that_hosts_the_quoted_pair(
    key: StreamKey = StreamKey.AS_SEALED,
) -> tuple[int, ...]:
    """نوافذُنا التي يقع فيها المنقولُ بحدَّيه معًا؛ قد تكون واحدةً أو صفرًا."""

    return tuple(
        verdict.fit.window
        for verdict in the_quoted_pair_against_our_windows(key)
        if verdict.both_agree
    )


@dataclass(frozen=True, slots=True)
class BlockComparison:
    """مقابلةُ درجةٍ واحدةٍ من سُلَّم الكتل: حجمُها، والمنقولُ، والمقيسُ."""

    size: int
    quoted: float
    measured: float

    @property
    def gap(self) -> float:
        return self.measured - self.quoted

    @property
    def standing(self) -> Verdict:
        return (
            Verdict.AGREES
            if abs(self.gap) <= THE_ENTROPY_TOLERANCE
            else Verdict.CONTRADICTS
        )


def the_block_entropy_comparison(
    key: StreamKey = StreamKey.AS_SEALED,
    rule: SamplingRule = SamplingRule.EVERY_SEVENTH,
) -> tuple[BlockComparison, ...]:
    """سُلَّمُهم مقابَلًا بسُلَّمنا على قاعدةِ عيّنةٍ تُختار وتُعلَن."""

    measured = block_entropy_ladder(key, rule).per_character
    return tuple(
        BlockComparison(size=size, quoted=quoted, measured=value)
        for size, quoted, value in zip(
            THE_BLOCK_SIZES, THE_QUOTED_BLOCK_ENTROPY.per_character, measured
        )
    )


# ---------------------------------------------------------------------------
# الأرقامُ المؤرَّخةُ وكاشفاها
# ---------------------------------------------------------------------------


THE_VOCABULARY_AT_MEASUREMENT: Final[tuple[int, int, int]] = (82532, 18201, 11352)
"""كلماتُ البايتات المختومة ومفرداتُها وأحاديّاتُها وقتَ القياس."""

THE_LADDER_AT_MEASUREMENT: Final[tuple[tuple[int, float, float], ...]] = (
    (100, 0.7766, 0.9759),
    (500, 0.8847, 0.9922),
    (1000, 0.9239, 0.9944),
    (2000, 0.9507, 0.9956),
    (5000, 0.9734, 0.9915),
    (10000, 1.0041, 0.9771),
    (0, 0.8678, 0.9469),
)
"""سُلَّمُ النوافذ وقتَ القياس: نافذةٌ ومقدارُ أسٍّ وجودةُ ربطٍ، بأربع منازل."""

THE_STRIDE_LADDER_AT_MEASUREMENT: Final[tuple[float, ...]] = (
    4.5926,
    3.8173,
    3.3283,
    2.9409,
    2.6047,
    2.3222,
    2.085,
    1.8858,
)
"""سُلَّمُ الكتل بخطوة سبعةٍ وقتَ القياس — على قاعدة عيّنتهم لا على قاعدتنا."""

_PLACES: Final[int] = 4


def the_vocabulary_has_drifted() -> bool:
    """أانزاح مقامُ القياس عمّا جُمِّد في هذا النثر؟"""

    census = vocabulary_census()
    return (census.tokens, census.types, census.hapax) != THE_VOCABULARY_AT_MEASUREMENT


def the_ladders_have_drifted() -> bool:
    """أانزاح سُلَّمُ النوافذ أو سُلَّمُ الخطوة عمّا جُمِّد في هذا النثر؟"""

    measured_zipf = tuple(
        (fit.window, round(fit.magnitude, _PLACES), round(fit.r_squared, _PLACES))
        for fit in zipf_ladder()
    )
    measured_stride = tuple(
        round(value, _PLACES)
        for value in block_entropy_ladder(
            StreamKey.AS_SEALED, SamplingRule.EVERY_SEVENTH
        ).per_character
    )
    return (
        measured_zipf != THE_LADDER_AT_MEASUREMENT
        or measured_stride != THE_STRIDE_LADDER_AT_MEASUREMENT
    )


# ---------------------------------------------------------------------------
# بوّابةُ ماركوف: تُقرأ ولا تُزحزَح
# ---------------------------------------------------------------------------


_THE_GATE_AS_READ_AT_IMPORT: Final[ChainReading] = token_markov_standing()


def the_corpus_gate_is_untouched() -> bool:
    """أزحزحت هذه الوحدةُ بوّابةَ ماركوف عمّا كانت عليه عند الاستيراد؟"""

    return token_markov_standing() == _THE_GATE_AS_READ_AT_IMPORT


# ---------------------------------------------------------------------------
# البقايا المسمّاة
# ---------------------------------------------------------------------------


AN_EXPONENT_WITHOUT_ITS_WINDOW_IS_NOT_A_CONSTANT: Final[str] = (
    "AN_EXPONENT_WITHOUT_ITS_WINDOW_IS_NOT_A_CONSTANT: أسُّ زِبف على بايتاتنا "
    "يتراوح بين 0.7766 و1.0041 بتغيُّر نافذة الرتب وحدَها، وجودةُ الربط بين "
    "0.9469 و0.9956؛ فرقمٌ يُنشَر بلا نافذةٍ مُعلَنةٍ لا يُقابَل رقمًا واحدًا"
)

A_FIGURE_MEASURED_ON_ANOTHER_CORPUS_DOES_NOT_CROSS_TO_OURS: Final[str] = (
    "A_FIGURE_MEASURED_ON_ANOTHER_CORPUS_DOES_NOT_CROSS_TO_OURS: بايتاتُ "
    "`mujammad.norm.txt` ليست في هذه الشجرة، ومقامُها 77,801 كلمةً و15,490 "
    "لفظًا مميّزًا يفارق مقامَنا 82,532 و18,201؛ فوقوعُ المنقول في إحدى "
    "نوافذنا موافقةُ نافذةٍ بعينها لا تصديقٌ لمدوّنةٍ لم تصل"
)

A_DECLARED_STRIDE_IS_PRICED_NOT_MERELY_DECLARED: Final[str] = (
    "A_DECLARED_STRIDE_IS_PRICED_NOT_MERELY_DECLARED: خطوةُ السبعة في عيّنة "
    "الإنتروبيا مُعلَنةٌ في الدعوى، وأثرُها يُقاس ههنا لا يُوصَف: تكاد لا تمسّ "
    "`k = 1` وتُنقِص نحوَ 0.13 بتٍّ في الحرف عند `k = 8`، فتُهبِط الطرفَ الذي "
    "يُقرأ منه التدرُّجُ نفسُه"
)

THE_FOLDING_MOVES_TWO_TYPES_AND_NOT_THE_EXPONENT: Final[str] = (
    "THE_FOLDING_MOVES_TWO_TYPES_AND_NOT_THE_EXPONENT: دعوى أنّ طيَّ الهمزة "
    "وفكَّ الشدّة «أعادا رسمَ الترددات» مردودةٌ على بايتاتنا: المفرداتُ تتحرّك "
    "لفظين من 18,201، والأسُّ يتحرّك أقلَّ من 0.001 على النوافذ السبع كلِّها"
)

A_FALLING_BLOCK_ENTROPY_LADDER_IS_NOT_A_MEASURED_FRACTAL_DIMENSION: Final[str] = (
    "A_FALLING_BLOCK_ENTROPY_LADDER_IS_NOT_A_MEASURED_FRACTAL_DIMENSION: هبوطُ "
    "`H(k)/k` لازمٌ لكلّ تيّارٍ مرتبطِ الرموز، فهو شاهدُ ارتباطٍ لا بُعدٌ؛ ولا "
    "يُقاس ههنا هاوسدورف ولا هيرست ولا يُخرَج من هذه الوحدة حكمٌ بفراكتاليّة"
)

ZIPF_BLOCK_ENTROPY_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "AN_EXPONENT_WITHOUT_ITS_WINDOW_IS_NOT_A_CONSTANT": (
        AN_EXPONENT_WITHOUT_ITS_WINDOW_IS_NOT_A_CONSTANT
    ),
    "A_FIGURE_MEASURED_ON_ANOTHER_CORPUS_DOES_NOT_CROSS_TO_OURS": (
        A_FIGURE_MEASURED_ON_ANOTHER_CORPUS_DOES_NOT_CROSS_TO_OURS
    ),
    "A_DECLARED_STRIDE_IS_PRICED_NOT_MERELY_DECLARED": (
        A_DECLARED_STRIDE_IS_PRICED_NOT_MERELY_DECLARED
    ),
    "THE_FOLDING_MOVES_TWO_TYPES_AND_NOT_THE_EXPONENT": (
        THE_FOLDING_MOVES_TWO_TYPES_AND_NOT_THE_EXPONENT
    ),
    "A_FALLING_BLOCK_ENTROPY_LADDER_IS_NOT_A_MEASURED_FRACTAL_DIMENSION": (
        A_FALLING_BLOCK_ENTROPY_LADDER_IS_NOT_A_MEASURED_FRACTAL_DIMENSION
    ),
}
"""بقايا هذه الوحدة مسمّاةً؛ ولا تُقرأ واحدةٌ منها ترخيصًا لرقمٍ بلا نافذة."""


_FORBIDDEN_FIELD_TOKENS: Final[tuple[str, ...]] = (
    "verdict",
    "standing",
    "authority",
    "birth",
    "fractal",
)


def _assert_no_written_verdict_field() -> None:
    """لا حكمَ مكتوبٌ حقلًا في بنيةٍ ههنا؛ وكلُّ حكمٍ صفةٌ تُشتَقّ عند القراءة."""

    for structure in (
        BlockComparison,
        BlockEntropyLadder,
        QuotedBlockEntropy,
        QuotedZipf,
        TypeTokenCensus,
        WindowVerdict,
        ZipfFit,
    ):
        for field in fields(structure):
            if any(token in field.name for token in _FORBIDDEN_FIELD_TOKENS):
                raise ZipfBlockEntropyError(
                    f"الحقلُ `{field.name}` في `{structure.__name__}` يُكتَب حكمًا، "
                    "وحكمُ هذه الوحدة يُشتَقّ بالحساب."
                )


def _assert_the_windows_are_declared_and_ordered() -> None:
    """النوافذُ مُعلَنةٌ صاعدةً، وآخرُها الصفرُ الذي يعني كلَّ الرتب."""

    windows = THE_RANK_WINDOWS
    if len(set(windows)) != len(windows) or windows[-1] != 0:
        raise ZipfBlockEntropyError("نوافذُ الرتب تُعلَن متمايزةً وآخرُها كلُّ الرتب.")
    if list(windows[:-1]) != sorted(windows[:-1]):
        raise ZipfBlockEntropyError("نوافذُ الرتب تُعلَن صاعدةً قبل كلِّ قياس.")


def _assert_the_tolerances_precede_the_comparison() -> None:
    """حدودُ التسامح موجبةٌ ومُعلَنةٌ قبل أن يُقرأ فارق."""

    for tolerance in (
        THE_ENTROPY_TOLERANCE,
        THE_EXPONENT_TOLERANCE,
        THE_R_SQUARED_TOLERANCE,
    ):
        if tolerance <= 0.0:
            raise ZipfBlockEntropyError("حدُّ تسامحٍ دون الصفر لا يُقابَل به.")


_assert_no_written_verdict_field()
_assert_the_windows_are_declared_and_ordered()
_assert_the_tolerances_precede_the_comparison()
