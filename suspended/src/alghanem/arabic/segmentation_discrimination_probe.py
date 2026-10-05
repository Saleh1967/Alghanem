"""أمرانِ يُفحصان مستقلَّين: رجوعُ البايتات، وصحّةُ التصنيف.

بلغ `ArabicRoundTripV1` على إيداع الفاتحة تسعًا وعشرين من تسعٍ وعشرين. وهذا
**عددُ استرجاعٍ لا عددُ فهم**. فالسؤالُ الذي يُطرَح بعده اثنان لا واحد:

١. أترجع «الَّذِينَ» بايتًا ببايت؟ — هذا **يُقاس ههنا بالتشغيل**.
٢. أتُحفَظ هويتُها اسمًا موصولًا، فلا تُخلَط بلام التعريف في «الضَّالِّينَ»؟ —
   هذا **لا يُقاس ههنا**، ويُرفَع رفضًا باسمه.

`RECONSTRUCTION_IS_NOT_CLASSIFICATION`: نجاحُ الاسترجاع يُثبت أنّ الدالّة
العكسيّة لم تُتلِف شيئًا، ولا يُثبت أنّ ما بينهما فهمٌ صحيح. فدالّةُ الهويّة
تسترجع كلَّ نصٍّ بتمامه ولا تفهم منه حرفًا، فالاسترجاعُ وحدَه لا يرقى دليلًا
على تصنيف.

**والمقيسُ ههنا شيءٌ ثالثٌ بينهما**: أيُفرِّق الخطُّ **شكلَي** الكلمتَين؟ وهذا
عددٌ يُشتَقّ بالتشغيل: يُقرأ من كلّ كلمةٍ توقيعُها البنيويُّ المُشتَقُّ من
التقطيع — صدرُ كلِّ مقطع، وطولُ المفتتح غيرِ المكتوب، وموضعُ التشديد، والإطالة،
والإغلاق — ثمّ يُقارَن بغيره. فإن اختلف التوقيعان فقد ثبت **عدمُ الخلط شكلًا**،
وهو أضعفُ من صحّة التصنيف وأقوى من لا شيء.

`A_SHAPE_DIFFERENCE_IS_NOT_AN_IDENTITY`: اختلافُ التوقيعَين لا يُسمّي أحدَهما
اسمًا موصولًا ولا الآخرَ لامَ تعريف؛ إنّما يقول إنّ الخطَّ لم يُخرِجهما
مُتشابهَين، فامتناعُ الخلط ممكنٌ لا محقَّق. واتّفاقُ التوقيعَين كذلك ليس تكذيبًا
للتصنيف بل **إخفاقٌ في التمييز** يُسجَّل بهذا الاسم.

`NO_INDEPENDENT_REFERENCE_IS_DEPOSITED`: ليس في هذه الشجرة تقطيعٌ مرجعيٌّ
مُبصَّمٌ لكلمةٍ واحدةٍ يُقابَل به تقطيعُ هذا الخطّ. فمنزلةُ صحّة التصنيف
`لم_تُقَس_لانعدام_المرجع`، وهي **متعذّرةٌ** لا موافقةٌ ولا مخالفة. وما يلزم
لرفعها مُسمًّى صنفًا صنفًا في `INDEPENDENT_REFERENCE_REQUIREMENTS`، فمن أودع
مرجعًا يفي بها انتقلت المنزلةُ بالتشغيل لا بالقول.

`THE_WIDER_POPULATION_IS_NOT_IN_THIS_TREE`: تسعٌ وعشرون كلمةً مجتمعُ اختبارٍ
صغير، ورفعُ نسبتها بعد تمامها لا يُنتج عددًا. والخطوةُ التالية توسيعُ المجتمع:
مدوّنةُ الـ٧٧٬٤٢٩ كلمةً مُسمّاةٌ في `UNMEASURED_ROUND_TRIP_SOURCES` ببصمتها بلا
رقم، وتُشغَّل ببايتاتها حين تتوافر عبر
`examples/arabic/measure_arabic_round_trip_v1.py <path>`، ويُعرَض رفضُها
واختلافُها **مع أمثلةٍ من كلّ صنف** لا بعددٍ مجرَّد.
"""

from __future__ import annotations

import hashlib
import unicodedata
from dataclasses import dataclass
from enum import Enum
from typing import Final

from .arabic_round_trip_v1 import (
    LayerOutcome,
    RoundTripLayer,
    RoundTripRefusal,
    run_token,
)
from .encoding.carrier_state_candidate import CarrierStateCodec
from .encoding.syllable_segmentation import (
    SyllableOnset,
    SyllableSegmentationError,
    segment,
)

__all__ = [
    "A_SHAPE_DIFFERENCE_IS_NOT_AN_IDENTITY_NOTE",
    "DISCRIMINATION_PROBE_WORDS",
    "INDEPENDENT_REFERENCE_REQUIREMENTS",
    "NO_INDEPENDENT_REFERENCE_IS_DEPOSITED_NOTE",
    "RECONSTRUCTION_IS_NOT_CLASSIFICATION_NOTE",
    "THE_WIDER_POPULATION_IS_NOT_IN_THIS_TREE_NOTE",
    "ClassificationStanding",
    "DiscriminationProbeError",
    "PairDiscrimination",
    "ProbeClass",
    "ProbeReport",
    "ProbeRow",
    "ProbeWord",
    "ReferenceRequirement",
    "ShapeReadout",
    "SyllableShape",
    "declared_pairs",
    "render_report",
    "run_probe",
]


class DiscriminationProbeError(ValueError):
    """رُوجِع المِسبارُ بما لا يقوم به؛ ولا يُحمَل على أقرب حالةٍ مقبولة."""


class ProbeClass(Enum):
    """أصنافُ المِسبار؛ مفردةٌ مغلقةٌ تُسمّي سببَ إدخال الكلمة لا معناها."""

    RELATIVE_NOUN_SHAPE = "RELATIVE_NOUN_SHAPE"
    SUN_LAM_SHAPE = "SUN_LAM_SHAPE"
    MOON_LAM_SHAPE = "MOON_LAM_SHAPE"
    MADD_SHAPE = "MADD_SHAPE"
    SHADDA_WITHOUT_AN_OPENING = "SHADDA_WITHOUT_AN_OPENING"


class ClassificationStanding(Enum):
    """منزلةُ صحّة التصنيف؛ والدنيا مرتبةٌ لأنّ فوقها مرتبتَين مُسمّاتَين."""

    MEASURED_AGAINST_A_DEPOSITED_REFERENCE = "مقيسة_بمرجعٍ_مُودَع"
    DECLARED_AND_AWAITING_A_REFERENCE = "مُعلَنة_تنتظر_مرجعًا"
    NOT_ASSESSED_NO_REFERENCE_DEPOSITED = "لم_تُقَس_لانعدام_المرجع"


@dataclass(frozen=True, slots=True)
class ProbeWord:
    """كلمةٌ في المِسبار: مفتاحُها، وسطحُها، وصنفُها، وسببُ إدخالها."""

    key: str
    surface: str
    probe_class: ProbeClass
    why_it_is_here: str

    def __post_init__(self) -> None:
        if not self.key.strip():
            raise DiscriminationProbeError("لكلّ كلمةٍ في المِسبار مفتاحٌ غيرُ فارغ")
        if not self.surface.strip():
            raise DiscriminationProbeError("لا كلمةَ بلا سطحٍ مكتوب")
        if self.surface != unicodedata.normalize("NFC", self.surface):
            raise DiscriminationProbeError(
                "سطحُ المِسبار مُسوًّى بـ`NFC` كما يقرؤه المرماز، ولا يُخزَّن خامًا"
            )
        if not isinstance(self.probe_class, ProbeClass):
            raise DiscriminationProbeError("صنفُ المِسبار مفردةٌ مغلقةٌ لا نصٌّ حُرّ")
        if not self.why_it_is_here.strip():
            raise DiscriminationProbeError("لا تدخل كلمةٌ المِسبارَ بلا سببٍ مكتوب")

    @property
    def raw_bytes(self) -> bytes:
        """بايتاتُ هذه الكلمة كما تدخل الخطَّ؛ مشتقّةٌ لا مكتوبة."""

        return self.surface.encode("utf-8")


@dataclass(frozen=True, slots=True)
class SyllableShape:
    """توقيعُ مقطعٍ واحد: ما يُقرأ منه بنيويًّا بلا تسميةٍ صرفيّةٍ ولا نحويّة."""

    onset: SyllableOnset
    unit_count: int
    undecided_opening_length: int
    carries_a_madd: bool
    has_coda: bool
    gemination_starts_at: tuple[int, ...]

    @property
    def signature(self) -> tuple[object, ...]:
        """توقيعٌ قابلٌ للمقارنة؛ مشتقٌّ من الحقول لا مكتوبٌ إلى جانبها."""

        return (
            self.onset.value,
            self.unit_count,
            self.undecided_opening_length,
            self.carries_a_madd,
            self.has_coda,
            self.gemination_starts_at,
        )


@dataclass(frozen=True, slots=True)
class ShapeReadout:
    """توقيعُ كلمةٍ كاملة: مقاطعُها بتوقيعاتها، وعددُ وحداتها الداخلة."""

    syllables: tuple[SyllableShape, ...]
    unit_total: int

    def __post_init__(self) -> None:
        if not self.syllables:
            raise DiscriminationProbeError("توقيعٌ بلا مقطعٍ واحدٍ ليس توقيعَ كلمة")
        covered = sum(shape.unit_count for shape in self.syllables)
        if covered != self.unit_total:
            raise DiscriminationProbeError("مقاطعُ التوقيع تستوعب كلَّ وحدةٍ مرّةً واحدة")

    @property
    def signature(self) -> tuple[object, ...]:
        """توقيعُ الكلمة كلِّها؛ هو المقارَنُ في التمييز لا النصُّ ولا الوحدات."""

        return tuple(shape.signature for shape in self.syllables)

    @property
    def digest(self) -> str:
        """بصمةُ التوقيع؛ تُشتَقّ عند الطلب ولا تُكتَب في الشجرة."""

        return hashlib.sha256(repr(self.signature).encode("utf-8")).hexdigest()


def _read_shape(surface: str) -> ShapeReadout | None:
    """اقرأ توقيعَ الكلمة من تقطيعها، أو أعِد لا شيءَ إن امتنع التقطيع."""

    units = CarrierStateCodec().generate(surface)
    try:
        parse = segment(units)
    except SyllableSegmentationError:
        return None
    shapes: list[SyllableShape] = []
    for syllable in parse.syllables:
        starts = tuple(
            index
            for index, unit in enumerate(syllable.units)
            if unit.gemination is not None
        )
        shapes.append(
            SyllableShape(
                onset=syllable.onset,
                unit_count=syllable.length,
                undecided_opening_length=len(syllable.undecided_opening),
                carries_a_madd=syllable.carries_a_madd,
                has_coda=syllable.has_coda,
                gemination_starts_at=starts,
            )
        )
    return ShapeReadout(syllables=tuple(shapes), unit_total=parse.unit_total)


@dataclass(frozen=True, slots=True)
class ProbeRow:
    """نتيجةُ كلمةٍ واحدة: رجوعُ بايتاتها، وتوقيعُها، ومنزلةُ تصنيفها."""

    word: ProbeWord
    reached: RoundTripLayer
    outcome: LayerOutcome
    refusal: RoundTripRefusal | None
    shape: ShapeReadout | None
    classification_standing: ClassificationStanding

    def __post_init__(self) -> None:
        if self.classification_standing is not (
            ClassificationStanding.NOT_ASSESSED_NO_REFERENCE_DEPOSITED
        ):
            raise DiscriminationProbeError(
                "لا مرجعَ مُودَعًا في هذه الشجرة، فلا تُرفَع منزلةُ التصنيف بالكتابة"
            )

    @property
    def bytes_returned(self) -> bool:
        """أعادت الكلمةُ بايتاتها كما دخلت؟ مقروءٌ من التشغيل لا من دعوى."""

        return (
            self.reached is RoundTripLayer.FINAL_BYTES
            and self.outcome is LayerOutcome.RECONSTRUCTED
        )


@dataclass(frozen=True, slots=True)
class PairDiscrimination:
    """مقارنةُ كلمتَين مُعلَنتَين: أاختلف توقيعاهما؟ ولا هويّةَ تُقرأ من ذلك."""

    left: str
    right: str
    why_the_pair_matters: str
    shapes_differ: bool
    both_returned_their_bytes: bool

    @property
    def conflated_in_shape(self) -> bool:
        """أخرجهما الخطُّ متشابهَين؟ إخفاقٌ في التمييز يُسمّى ولا يُستَر."""

        return not self.shapes_differ


@dataclass(frozen=True, slots=True)
class ReferenceRequirement:
    """ما يلزم من مرجعٍ مستقلٍّ ليُقاس صنفٌ من أصناف المِسبار."""

    probe_class: ProbeClass
    what_the_reference_must_supply: str

    def __post_init__(self) -> None:
        if not isinstance(self.probe_class, ProbeClass):
            raise DiscriminationProbeError("صنفُ المِسبار مفردةٌ مغلقةٌ لا نصٌّ حُرّ")
        if not self.what_the_reference_must_supply.strip():
            raise DiscriminationProbeError("شرطُ المرجع يُكتَب ولا يُترَك فارغًا")


@dataclass(frozen=True, slots=True)
class ProbeReport:
    """تقريرُ المِسبار: صفوفُه، ومقارناتُه، ومنزلةُ التصنيف فيه كلِّه."""

    rows: tuple[ProbeRow, ...]
    pairs: tuple[PairDiscrimination, ...]

    def __post_init__(self) -> None:
        if not self.rows:
            raise DiscriminationProbeError("تقريرٌ بلا صفٍّ واحدٍ ليس تقريرًا")
        keys = [row.word.key for row in self.rows]
        if len(set(keys)) != len(keys):
            raise DiscriminationProbeError("مفاتيحُ المِسبار لا تتكرّر")

    @property
    def returned_total(self) -> int:
        """كم كلمةً رجعت بايتاتُها؟ مشتقٌّ بالعدّ لا مكتوب."""

        return sum(1 for row in self.rows if row.bytes_returned)

    @property
    def word_total(self) -> int:
        """كم كلمةً دخلت المِسبار؟ مشتقٌّ لا مكتوب."""

        return len(self.rows)

    @property
    def distinct_shape_total(self) -> int:
        """كم توقيعًا مختلفًا أخرجه الخطُّ؟ فالتساوي إخفاقُ تمييزٍ يُعَدّ."""

        return len({row.shape.signature for row in self.rows if row.shape is not None})

    @property
    def conflated_pairs(self) -> tuple[PairDiscrimination, ...]:
        """المقارناتُ التي لم يُفرِّق الخطُّ فيها؛ تُعرَض ولا تُحذَف."""

        return tuple(pair for pair in self.pairs if pair.conflated_in_shape)

    @property
    def classification_standing(self) -> ClassificationStanding:
        """منزلةُ صحّة التصنيف في هذا التقرير كلِّه؛ واحدةٌ لا تتجزّأ."""

        return ClassificationStanding.NOT_ASSESSED_NO_REFERENCE_DEPOSITED


DISCRIMINATION_PROBE_WORDS: Final[tuple[ProbeWord, ...]] = (
    ProbeWord(
        key="allathina",
        surface=unicodedata.normalize(
            "NFC", "\u0627\u0644\u0651\u064e\u0630\u0650\u064a\u0646\u064e"
        ),
        probe_class=ProbeClass.RELATIVE_NOUN_SHAPE,
        why_it_is_here=(
            "الشدّةُ مكتوبةٌ على اللام نفسِها، فحالتُها مكتوبةٌ ولا تدخل المفتتحَ "
            "غيرَ المكتوب؛ وهذا هو الموضعُ الذي يُخشى فيه الخلطُ بلام التعريف"
        ),
    ),
    ProbeWord(
        key="ad_dallina",
        surface=unicodedata.normalize(
            "NFC",
            "\u0627\u0644\u0636\u064e\u0651\u0627\u0644\u0650\u0651\u064a\u0646\u064e",
        ),
        probe_class=ProbeClass.SUN_LAM_SHAPE,
        why_it_is_here=(
            "الشدّةُ مكتوبةٌ على الضاد لا على اللام، فاللامُ عاريةٌ تدخل المفتتحَ "
            "غيرَ المكتوب؛ وفيها كذلك ألفُ مدٍّ قبل مشدَّد"
        ),
    ),
    ProbeWord(
        key="ash_shamsi",
        surface=unicodedata.normalize(
            "NFC", "\u0627\u0644\u0634\u064e\u0651\u0645\u0652\u0633\u0650"
        ),
        probe_class=ProbeClass.SUN_LAM_SHAPE,
        why_it_is_here="لامٌ عاريةٌ قبل مشدَّدٍ بلا مدٍّ بعده، لتُفصَل عن أثر المدّ",
    ),
    ProbeWord(
        key="al_qamari",
        surface=unicodedata.normalize(
            "NFC", "\u0627\u0644\u0652\u0642\u064e\u0645\u064e\u0631\u0650"
        ),
        probe_class=ProbeClass.MOON_LAM_SHAPE,
        why_it_is_here=(
            "سكونٌ مكتوبٌ على اللام، فحالتُها مقروءةٌ من الخطّ وتقف عندها حدودُ "
            "المفتتح غيرِ المكتوب"
        ),
    ),
    ProbeWord(
        key="qala",
        surface=unicodedata.normalize("NFC", "\u0642\u064e\u0627\u0644\u064e"),
        probe_class=ProbeClass.MADD_SHAPE,
        why_it_is_here="ألفُ مدٍّ بعد فتحةٍ بلا مفتتحٍ ولا تشديد",
    ),
    ProbeWord(
        key="yaqulu",
        surface=unicodedata.normalize(
            "NFC", "\u064a\u064e\u0642\u064f\u0648\u0644\u064f"
        ),
        probe_class=ProbeClass.MADD_SHAPE,
        why_it_is_here="واوُ مدٍّ بعد ضمّة، ليُفحَص شرطُ المُجانَسة لا الألفُ وحدَها",
    ),
    ProbeWord(
        key="baytin",
        surface=unicodedata.normalize("NFC", "\u0628\u064e\u064a\u0652\u062a\u0650"),
        probe_class=ProbeClass.MADD_SHAPE,
        why_it_is_here=(
            "ياءٌ بسكونٍ مكتوبٍ بعد فتحة: ليست مُجانِسةً ولا عاريةً، فلا تُقرأ "
            "إطالةً — وهذا هو الحدُّ السالب للمدّ"
        ),
    ),
    ProbeWord(
        key="rabbuka",
        surface=unicodedata.normalize(
            "NFC", "\u0631\u064e\u0628\u0651\u064f\u0643\u064e"
        ),
        probe_class=ProbeClass.SHADDA_WITHOUT_AN_OPENING,
        why_it_is_here="تشديدٌ في وسط الكلمة بلا مفتتحٍ غيرِ مكتوبٍ قبله",
    ),
)
"""كلماتُ المِسبار: ثمانٍ، كلُّ واحدةٍ مُعلَّلةٌ بموضعِ الاشتباه الذي أُدخلت له."""


_DECLARED_PAIRS: Final[tuple[tuple[str, str, str], ...]] = (
    (
        "allathina",
        "ad_dallina",
        "الشدّةُ على اللام أو على ما بعدها: هذا موضعُ الخلط المسؤول عنه",
    ),
    (
        "ad_dallina",
        "ash_shamsi",
        "لامان عاريتان، إحداهما يتلوها مدٌّ والأخرى لا؛ ليُفصَل الأثران",
    ),
    (
        "al_qamari",
        "ash_shamsi",
        "سكونٌ مكتوبٌ على اللام مقابلَ لامٍ عارية",
    ),
    (
        "qala",
        "baytin",
        "حاملٌ مُجانِسٌ عارٍ مقابلَ حاملٍ عليه سكونٌ مكتوب",
    ),
    (
        "allathina",
        "rabbuka",
        "تشديدٌ بعد مفتتحٍ غيرِ مكتوبٍ مقابلَ تشديدٍ بلا مفتتحٍ أصلًا",
    ),
)


INDEPENDENT_REFERENCE_REQUIREMENTS: Final[tuple[ReferenceRequirement, ...]] = (
    ReferenceRequirement(
        probe_class=ProbeClass.RELATIVE_NOUN_SHAPE,
        what_the_reference_must_supply=(
            "تقطيعٌ مرجعيٌّ مُبصَّمٌ لـ«الَّذِينَ» يُصرِّح أنّ لامَها من بنية "
            "الاسم الموصول لا لامُ تعريفٍ داخلةٌ عليه، وأنّ ذلك مقروءٌ من مصدرٍ "
            "مُسمًّى بطبعةٍ وموضع"
        ),
    ),
    ReferenceRequirement(
        probe_class=ProbeClass.SUN_LAM_SHAPE,
        what_the_reference_must_supply=(
            "قائمةٌ مرجعيّةٌ مُبصَّمةٌ تفصل لامَ التعريف الشمسيّةَ عن غيرها موضعًا "
            "موضعًا، لا قاعدةٌ تُستنبَط من الشكل المكتوب نفسِه الذي يُقاس"
        ),
    ),
    ReferenceRequirement(
        probe_class=ProbeClass.MOON_LAM_SHAPE,
        what_the_reference_must_supply=(
            "مواضعُ لام التعريف القمريّة مُبصَّمةً، ليُعلَم أنّ السكونَ المكتوب "
            "عليها مُطَّردٌ في المرجع لا في هذا الإيداع وحدَه"
        ),
    ),
    ReferenceRequirement(
        probe_class=ProbeClass.MADD_SHAPE,
        what_the_reference_must_supply=(
            "تقطيعٌ مرجعيٌّ يُعلِن مواضعَ المدّ وطولَ نواتها، ليُقابَل به "
            "`carries_a_madd` بدل أن يُصدَّق لأنّه رجعت بايتاتُه"
        ),
    ),
    ReferenceRequirement(
        probe_class=ProbeClass.SHADDA_WITHOUT_AN_OPENING,
        what_the_reference_must_supply=(
            "مواضعُ التشديد مُعلَنةً في المرجع، ليُفصَل تشديدُ البنية عن تشديد "
            "الإدغام، وهو فصلٌ لا يُقرأ من العلامات وحدَها"
        ),
    ),
)
"""شرطُ رفع المنزلة، صنفًا صنفًا؛ ولا يُرفَع صنفٌ بمرجعٍ لصنفٍ آخر."""


def declared_pairs() -> tuple[tuple[str, str, str], ...]:
    """المقارناتُ المُعلَنةُ قبل التشغيل؛ لا تُختار بعد رؤية التوقيعات."""

    return _DECLARED_PAIRS


def run_probe(words: tuple[ProbeWord, ...] = DISCRIMINATION_PROBE_WORDS) -> ProbeReport:
    """شغِّل المِسبار: استرجاعٌ بالتشغيل، وتوقيعٌ بالاشتقاق، وتصنيفٌ لا يُقاس."""

    if not words:
        raise DiscriminationProbeError("مِسبارٌ بلا كلمةٍ واحدةٍ لا يُشغَّل")
    rows: list[ProbeRow] = []
    for word in words:
        trace = run_token(word.raw_bytes)
        rows.append(
            ProbeRow(
                word=word,
                reached=trace.reached,
                outcome=trace.outcome,
                refusal=trace.refusal,
                shape=_read_shape(word.surface),
                classification_standing=(
                    ClassificationStanding.NOT_ASSESSED_NO_REFERENCE_DEPOSITED
                ),
            )
        )
    by_key = {row.word.key: row for row in rows}
    pairs: list[PairDiscrimination] = []
    for left, right, why in _DECLARED_PAIRS:
        if left not in by_key or right not in by_key:
            raise DiscriminationProbeError(
                f"المقارنةُ المُعلَنة {left!r}/{right!r} تُحيل إلى كلمةٍ ليست في المِسبار"
            )
        one, other = by_key[left], by_key[right]
        if one.shape is None or other.shape is None:
            differ = False
        else:
            differ = one.shape.signature != other.shape.signature
        pairs.append(
            PairDiscrimination(
                left=left,
                right=right,
                why_the_pair_matters=why,
                shapes_differ=differ,
                both_returned_their_bytes=(one.bytes_returned and other.bytes_returned),
            )
        )
    return ProbeReport(rows=tuple(rows), pairs=tuple(pairs))


def render_report(report: ProbeReport) -> str:
    """اعرض التقريرَ عمودَين لا عمودًا: بايتاتٌ رجعت، وتوقيعٌ اختلف."""

    lines = [
        f"{'word':<14}{'class':<28}{'bytes':<10}{'shape digest':<18}refusal",
        "-" * 88,
    ]
    for row in report.rows:
        returned = "returned" if row.bytes_returned else "halted"
        digest = "—" if row.shape is None else row.shape.digest[:16]
        refusal = "—" if row.refusal is None else row.refusal.value
        lines.append(
            f"{row.word.key:<14}{row.word.probe_class.value:<28}"
            f"{returned:<10}{digest:<18}{refusal}"
        )
    lines.append("")
    lines.append("declared pairs, compared by shape only:")
    for pair in report.pairs:
        verdict = "distinct" if pair.shapes_differ else "CONFLATED"
        lines.append(f"  {pair.left} / {pair.right}: {verdict}")
    lines.append("")
    lines.append(
        f"bytes returned: {report.returned_total}/{report.word_total}; "
        f"distinct shapes: {report.distinct_shape_total}/{report.word_total}"
    )
    lines.append(
        f"classification standing: {report.classification_standing.value} "
        "— لا مرجعَ مُودَعًا، فلا يُقرأ الاسترجاعُ تصنيفًا"
    )
    return "\n".join(lines)


RECONSTRUCTION_IS_NOT_CLASSIFICATION_NOTE: Final[str] = (
    "ReconstructionIsNotClassification: رجوعُ البايتات يُثبت سلامةَ الدالّة "
    "العكسيّة ولا يُثبت صحّةَ ما بينهما؛ فدالّةُ الهويّة تسترجع كلَّ شيءٍ ولا "
    "تفهم منه حرفًا، والأمران يُفحصان مستقلَّين ولا يُدمَج عددُهما"
)

A_SHAPE_DIFFERENCE_IS_NOT_AN_IDENTITY_NOTE: Final[str] = (
    "AShapeDifferenceIsNotAnIdentity: اختلافُ توقيعَي «الَّذِينَ» و«الضَّالِّينَ» "
    "يقول إنّ الخطَّ لم يُخرِجهما متشابهَين، ولا يُسمّي إحداهما اسمًا موصولًا ولا "
    "الأخرى لامَ تعريف؛ واتّفاقُهما يُسجَّل إخفاقًا في التمييز لا تكذيبًا لتصنيف"
)

NO_INDEPENDENT_REFERENCE_IS_DEPOSITED_NOTE: Final[str] = (
    "NoIndependentReferenceIsDeposited: ليس في الشجرة تقطيعٌ مرجعيٌّ مُبصَّمٌ "
    "يُقابَل به تقطيعُ هذا الخطّ، فمنزلةُ صحّة التصنيف `لم_تُقَس_لانعدام_المرجع` "
    "وهي متعذّرةٌ لا موافقةٌ ولا مخالفة؛ وشرطُ رفعها مكتوبٌ صنفًا صنفًا"
)

THE_WIDER_POPULATION_IS_NOT_IN_THIS_TREE_NOTE: Final[str] = (
    "TheWiderPopulationIsNotInThisTree: تسعٌ وعشرون كلمةً مجتمعُ اختبارٍ صغير، "
    "والخطوةُ التالية توسيعُه لا رفعُ نسبته؛ ومدوّنةُ الـ٧٧٬٤٢٩ كلمةً مُسمّاةٌ "
    "ببصمتها بلا رقم، وتُشغَّل حين تتوافر بايتاتُها ويُعرَض رفضُها واختلافُها "
    "مع أمثلةٍ من كلّ صنف"
)
