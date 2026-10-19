"""طبقةٌ مرجعيّةٌ للنطق تُجرى عليها تجربةُ الحذف، وتُقرَأ نتيجتُها بمنزلتها.

**السؤالُ المُجاب عنه ههنا بحرفه**: هل يُولِّد هذا النقلُ المُودَعُ قانونًا
داخليًّا أدنى؟ والجوابُ الذي تُخرجه هذه الوحدةُ بالتشغيل لا بالدعوى: **لا**.
الذي يقوم بالتشغيل أدنى من ذلك وأوضحُ حدًّا: **ضرورةٌ نسبيّةٌ لترميزٍ مختار**.

    MinimalInternalLaw      != RelativeNecessityOfAChosenCoding
    ReferenceLayer          != MechanicalFiber
    ExpectedCodingTransition != ObservedArticulatoryMotion

وتفصيلُ ذلك بلا تلطيف:

* **المحاورُ الأربعةُ مُستورَدةٌ لا مُشتقّةٌ من الآية.** الطريقةُ والموضعُ
  والجهرُ والتفخيمُ اختيارُ ترميزٍ يسبق القياس، لا بُعدٌ استُخرِج من الحروف بلا
  مقدّمات. فكلُّ ضرورةٍ تُقاس هنا ضرورةٌ **لهذا الترميز**، ولو بُدِّلت المحاورُ
  لبُدِّلت (`THE_FOUR_AXES_ARE_AN_IMPORTED_CODING_NOT_A_MEASURED_BASIS`).
* **قيمُ السمات وصفيّةٌ حديثةٌ تخالف صفاتِ التجويد في مواضع.** الطاءُ ههنا
  مهموسة، وهي في التراث مجهورةٌ من حروف القلقلة؛ فالجدولُ تقريرٌ عن ترميزٍ
  وصفيٍّ لا نقلٌ عن سيبويه
  (`THE_FEATURE_VALUES_ARE_MODERN_DESCRIPTIVE_NOT_CLASSICAL`).
* **الجدولُ مولودٌ في هذه الوحدة لا مستورَدٌ من مواصفة.** فلا يمرّ من حاجز
  `gflk_feature_table_import_barrier`، ولا يُقرَأ جدولًا مُبصَّمًا من مصدرٍ
  أجنبيّ؛ وهو لذلك **دعوى هذه الشجرة وحدَها**، وعُهدتُه عليها
  (`THIS_TABLE_IS_BORN_HERE_SO_IT_CARRIES_NO_FOREIGN_WARRANT`).
* **التعيينُ بقاعدةٍ مُعلَنة لا بيدٍ حرفًا بحرف.** الرسمُ الملتبسُ بين صامتٍ
  ومدٍّ — الألفُ والواوُ والياءُ وما جرى مجراها — يُترَك **غيرَ مُعيَّن**،
  ولا يُحسَم بترجيحٍ يُدخِل في البيانات ما يُراد إخراجُه منها.
* **الوصلُ والوقفُ الصوتيّان باقيان على `DEFER`.** ما يُحصى هنا من الانتقالات
  انتقالاتٌ في **الترميز المتوقَّع**، لا مشاهداتٌ زمنيّةٌ لحركة الأعضاء؛ فلا
  يُرفَع بها مانعُ `ibtida_wasl_waqf_registration`
  (`A_CODING_TRANSITION_IS_NOT_AN_ARTICULATORY_OBSERVATION`).
* **المحايدُ تحصيلُ حاصلٍ من تعريف العملية.** `e = ∅` و`e ⊕ p = p` صادقتان
  ببناء `⊕`، فالتحقّقُ منهما فحصُ اتّساقٍ لا اكتشافُ خاصّيّةٍ في العربية، على
  منوال `AN_ANALYTIC_TRUTH_IS_NOT_A_DISCOVERY`.

**ولا سلطةَ لهذه الوحدة**: لا ولادةَ، ولا حكمَ ولادةٍ، ولا تجميد، ولا تقرؤها
بوّابةٌ في `kernel/`. وكلُّ عددٍ تُخرجه **يُشتقّ عند القراءة** ولا يُكتَب في
حقلٍ بجانبه، على ما قرّرته `minimal_complete_fiber`: نتيجةٌ مكتوبةٌ لا يُنتجها
تشغيلُها ليست نتيجة.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from enum import Enum
from typing import Final

from alghanem.arabic.fath_ayah_source_text import (
    FATH_AYAH_SOURCE_ID,
    FATH_AYAH_SOURCE_TEXT,
)

__all__ = [
    "AN_UNRESOLVED_GRAPHIC_IS_LEFT_UNRESOLVED_NOT_GUESSED",
    "A_CODING_TRANSITION_IS_NOT_AN_ARTICULATORY_OBSERVATION",
    "A_DELETION_COLLISION_IS_RELATIVE_TO_THE_CHOSEN_CODING",
    "Axis",
    "AxisDeletionResult",
    "CoarsePlace",
    "InternalLawStanding",
    "Manner",
    "NO_FIBONACCI_LAW_IS_EXTRACTED_HERE",
    "NO_MECHANICAL_FIBER_IS_BORN_HERE",
    "PhoneticWaslAndWaqfRemainDeferred",
    "Place",
    "REFERENCE_ARTICULATION_NAMED_RESIDUALS",
    "THE_FEATURE_VALUES_ARE_MODERN_DESCRIPTIVE_NOT_CLASSICAL",
    "THE_FOUR_AXES_ARE_AN_IMPORTED_CODING_NOT_A_MEASURED_BASIS",
    "THE_GRANULARITY_IS_A_KNOB_SO_THE_PAIRS_ARE_NOT_A_FINDING",
    "THE_NEUTRAL_ELEMENT_IS_ANALYTIC_NOT_MEASURED",
    "THIS_TABLE_IS_BORN_HERE_SO_IT_CARRIES_NO_FOREIGN_WARRANT",
    "THE_REAL_AIR_IS_AN_OPERATING_CONDITION_NOT_THE_EMPTY_CONSTRAINT",
    "PlaceGranularity",
    "ReferenceArticulationError",
    "ReferencePattern",
    "ReferenceOccurrence",
    "ReferenceReading",
    "THE_AXES",
    "THE_REFERENCE_INVENTORY",
    "THE_UNRESOLVED_GRAPHICS",
    "TransitionCensus",
    "Voicing",
    "add_constraint",
    "assess_internal_law",
    "axis_deletion_experiment",
    "granularity_sensitivity",
    "read_the_deposited_ayah",
    "the_empty_constraint",
    "transition_census",
]


class ReferenceArticulationError(ValueError):
    """خطأُ بناءٍ في هذه الطبقة؛ يُرفَض المُدخَلُ ولا يُصحَّح ضمنًا."""


# --- المحاورُ الأربعة، مُعلَنةً باختيارها لا مُشتقّةً من المادّة ------------------


class Manner(Enum):
    """طريقةُ النطق؛ قيمٌ وصفيّةٌ مُعلَنة، لا صفاتٌ منقولةٌ عن التجويد."""

    STOP = "شديد"
    FRICATIVE = "رخو"
    AFFRICATE = "مركّب"
    NASAL = "أنفيّ"
    TRILL = "مكرّر"
    LATERAL = "جانبيّ"
    APPROXIMANT = "مقارب"


class Place(Enum):
    """موضعُ النطق بالتصنيف الدقيق؛ إحدى عشرة فئةً مُعلَنة."""

    BILABIAL = "شفويّ"
    LABIODENTAL = "شفويّ_أسنانيّ"
    INTERDENTAL = "بين_أسنانيّ"
    DENTAL = "أسنانيّ"
    ALVEOLAR = "لثويّ"
    POSTALVEOLAR = "بعد_لثويّ"
    PALATAL = "غاريّ"
    VELAR = "طبقيّ"
    UVULAR = "لهويّ"
    PHARYNGEAL = "حلقيّ"
    GLOTTAL = "حنجريّ"


class CoarsePlace(Enum):
    """موضعُ النطق بالتصنيف الأوسع؛ أربعُ فئاتٍ تُطوى فيها الإحدى عشرة."""

    LABIAL = "شفهيّ_عامّ"
    CORONAL = "طرفيّ_عامّ"
    DORSAL = "ظهريّ_عامّ"
    GUTTURAL = "حلقيّ_عامّ"


_COARSENING: Final[dict[Place, CoarsePlace]] = {
    Place.BILABIAL: CoarsePlace.LABIAL,
    Place.LABIODENTAL: CoarsePlace.LABIAL,
    Place.INTERDENTAL: CoarsePlace.CORONAL,
    Place.DENTAL: CoarsePlace.CORONAL,
    Place.ALVEOLAR: CoarsePlace.CORONAL,
    Place.POSTALVEOLAR: CoarsePlace.CORONAL,
    Place.PALATAL: CoarsePlace.DORSAL,
    Place.VELAR: CoarsePlace.DORSAL,
    Place.UVULAR: CoarsePlace.DORSAL,
    Place.PHARYNGEAL: CoarsePlace.GUTTURAL,
    Place.GLOTTAL: CoarsePlace.GUTTURAL,
}
"""طيُّ التصنيف الدقيق في الأوسع؛ وهو **اختيارٌ ثانٍ** فوق الاختيار الأوّل."""


class Voicing(Enum):
    """الجهرُ والهمس؛ ثنائيّةٌ مُعلَنة."""

    VOICED = "مجهور"
    VOICELESS = "مهموس"


class Emphasis(Enum):
    """التفخيمُ والترقيق؛ ثنائيّةٌ تُقرَأ على الاستعلاء لا على الإطباق وحدَه."""

    EMPHATIC = "مفخّم"
    PLAIN = "مرقّق"


class Axis(Enum):
    """المحاورُ الأربعةُ مُسمّاةً؛ وهي مدارُ تجربة الحذف."""

    MANNER = "طريقة_النطق"
    PLACE = "موضع_النطق"
    VOICING = "الجهر"
    EMPHASIS = "التفخيم"


THE_AXES: Final[tuple[Axis, ...]] = tuple(Axis)
"""المحاورُ الأربعةُ مرتّبةً؛ وعددُها يُقرَأ من التعداد لا يُكتَب رقمًا."""


class PlaceGranularity(Enum):
    """دقّةُ تصنيف المخارج المُختارةُ لتشغيلةٍ بعينها."""

    FINE = "تصنيفٌ_دقيق"
    COARSE = "تصنيفٌ_أوسع"


@dataclass(frozen=True, slots=True)
class ReferencePattern:
    """نمطٌ صامتيٌّ مرجعيّ: حرفٌ مُسمًّى ومُتَّجِهُه على المحاور الأربعة.

    وهو **مرجعيٌّ** بمعنى أنّه ما يُتوقَّع لهذا الحرف في ترميزٍ مُعلَن، لا ما
    قِيس من أداءٍ منطوق؛ فلا أداءَ في هذه الشجرة يُقاس عليه.
    """

    letter: str
    manner: Manner
    place: Place
    voicing: Voicing
    emphasis: Emphasis

    def __post_init__(self) -> None:
        if len(self.letter) != 1:
            raise ReferenceArticulationError("النمطُ المرجعيُّ يُسمّى بحرفٍ واحد")

    @property
    def coarse_place(self) -> CoarsePlace:
        """موضعُه بالتصنيف الأوسع، مُشتقًّا من الدقيق لا مكتوبًا بجانبه."""

        return _COARSENING[self.place]

    def vector(
        self, granularity: PlaceGranularity = PlaceGranularity.FINE
    ) -> tuple[object, ...]:
        """مُتَّجِهُ سماته على المحاور الأربعة بالدقّة المطلوبة."""

        place: object = (
            self.place if granularity is PlaceGranularity.FINE else self.coarse_place
        )
        return (self.manner, place, self.voicing, self.emphasis)

    def projected(
        self, deleted: Axis, granularity: PlaceGranularity = PlaceGranularity.FINE
    ) -> tuple[object, ...]:
        """مُتَّجِهُه بعد حذف محورٍ مُسمًّى؛ وهو `T_{-i}` في هذه الطبقة."""

        values = list(self.vector(granularity))
        del values[THE_AXES.index(deleted)]
        return tuple(values)


def _pattern(
    letter: str,
    manner: Manner,
    place: Place,
    voicing: Voicing,
    emphasis: Emphasis = Emphasis.PLAIN,
) -> ReferencePattern:
    return ReferencePattern(
        letter=letter,
        manner=manner,
        place=place,
        voicing=voicing,
        emphasis=emphasis,
    )


THE_REFERENCE_INVENTORY: Final[tuple[ReferencePattern, ...]] = (
    _pattern("ء", Manner.STOP, Place.GLOTTAL, Voicing.VOICELESS),
    _pattern("ب", Manner.STOP, Place.BILABIAL, Voicing.VOICED),
    _pattern("ت", Manner.STOP, Place.DENTAL, Voicing.VOICELESS),
    _pattern("ث", Manner.FRICATIVE, Place.INTERDENTAL, Voicing.VOICELESS),
    _pattern("ج", Manner.AFFRICATE, Place.POSTALVEOLAR, Voicing.VOICED),
    _pattern("ح", Manner.FRICATIVE, Place.PHARYNGEAL, Voicing.VOICELESS),
    _pattern("خ", Manner.FRICATIVE, Place.UVULAR, Voicing.VOICELESS, Emphasis.EMPHATIC),
    _pattern("د", Manner.STOP, Place.DENTAL, Voicing.VOICED),
    _pattern("ذ", Manner.FRICATIVE, Place.INTERDENTAL, Voicing.VOICED),
    _pattern("ر", Manner.TRILL, Place.ALVEOLAR, Voicing.VOICED),
    _pattern("ز", Manner.FRICATIVE, Place.ALVEOLAR, Voicing.VOICED),
    _pattern("س", Manner.FRICATIVE, Place.ALVEOLAR, Voicing.VOICELESS),
    _pattern("ش", Manner.FRICATIVE, Place.POSTALVEOLAR, Voicing.VOICELESS),
    _pattern(
        "ص", Manner.FRICATIVE, Place.ALVEOLAR, Voicing.VOICELESS, Emphasis.EMPHATIC
    ),
    _pattern("ض", Manner.STOP, Place.DENTAL, Voicing.VOICED, Emphasis.EMPHATIC),
    _pattern("ط", Manner.STOP, Place.DENTAL, Voicing.VOICELESS, Emphasis.EMPHATIC),
    _pattern(
        "ظ", Manner.FRICATIVE, Place.INTERDENTAL, Voicing.VOICED, Emphasis.EMPHATIC
    ),
    _pattern("ع", Manner.FRICATIVE, Place.PHARYNGEAL, Voicing.VOICED),
    _pattern("غ", Manner.FRICATIVE, Place.UVULAR, Voicing.VOICED, Emphasis.EMPHATIC),
    _pattern("ف", Manner.FRICATIVE, Place.LABIODENTAL, Voicing.VOICELESS),
    _pattern("ق", Manner.STOP, Place.UVULAR, Voicing.VOICELESS, Emphasis.EMPHATIC),
    _pattern("ك", Manner.STOP, Place.VELAR, Voicing.VOICELESS),
    _pattern("ل", Manner.LATERAL, Place.ALVEOLAR, Voicing.VOICED),
    _pattern("م", Manner.NASAL, Place.BILABIAL, Voicing.VOICED),
    _pattern("ن", Manner.NASAL, Place.ALVEOLAR, Voicing.VOICED),
    _pattern("ه", Manner.FRICATIVE, Place.GLOTTAL, Voicing.VOICELESS),
    _pattern("و", Manner.APPROXIMANT, Place.BILABIAL, Voicing.VOICED),
    _pattern("ي", Manner.APPROXIMANT, Place.PALATAL, Voicing.VOICED),
)
"""ثمانيةٌ وعشرون نمطًا مرجعيًّا، الهمزةُ فيها حرفٌ والألفُ ليست منها."""


_BY_LETTER: Final[dict[str, ReferencePattern]] = {
    pattern.letter: pattern for pattern in THE_REFERENCE_INVENTORY
}


if len(_BY_LETTER) != len(THE_REFERENCE_INVENTORY):  # pragma: no cover - حارس استيراد
    raise RuntimeError("a reference letter is deposited twice")

if len(  # pragma: no cover - حارس استيراد
    {pattern.vector() for pattern in THE_REFERENCE_INVENTORY}
) != len(THE_REFERENCE_INVENTORY):
    raise RuntimeError("two reference patterns share one full vector")


# --- التعيينُ بقاعدةٍ مُعلَنة ---------------------------------------------------


THE_UNRESOLVED_GRAPHICS: Final[frozenset[str]] = frozenset("اوىيةآ")
"""الرسومُ الملتبسةُ بين صامتٍ ومدٍّ أو تاءٍ موقوفةٍ؛ تُترَك بلا تعيين.

والواوُ والياءُ ههنا **رسمان ملتبسان** وإن كان لهما نمطان مرجعيّان: فالرسمُ
وحدَه لا يفصل صامتَهما من مدّهما، والحسمُ يحتاج ما ليس في هذا النقل.
"""


_HAMZA_SEATS: Final[dict[str, str]] = {
    "ء": "ء",
    "أ": "ء",
    "إ": "ء",
    "ؤ": "ء",
    "ئ": "ء",
}
"""كراسيُّ الهمزة تُردّ إلى الهمزة؛ فالكرسيُّ رسمٌ لها لا حرفٌ ثانٍ."""


@dataclass(frozen=True, slots=True)
class ReferenceOccurrence:
    """وقعةٌ مكتوبةٌ ومآلُها: نمطٌ مرجعيٌّ أو امتناعُ تعيينٍ مُسمًّى بموضعه."""

    word_index: int
    letter_index: int
    graphic: str
    pattern: ReferencePattern | None

    @property
    def is_resolved(self) -> bool:
        """أعُيِّنت هذه الوقعةُ إلى نمطٍ مرجعيّ؟ يُقرَأ من التعيين لا من وسم."""

        return self.pattern is not None


@dataclass(frozen=True, slots=True)
class ReferenceReading:
    """قراءةُ نصٍّ مُودَعٍ في الطبقة المرجعيّة؛ وكلُّ عددٍ فيها مُشتقٌّ."""

    source_id: str
    occurrences: tuple[ReferenceOccurrence, ...]

    @property
    def written_occurrence_count(self) -> int:
        """عددُ الوقعات المكتوبة المعروضة على القاعدة."""

        return len(self.occurrences)

    @property
    def resolved(self) -> tuple[ReferenceOccurrence, ...]:
        """الوقعاتُ المُعيَّنة، مُرشَّحةً عند القراءة."""

        return tuple(one for one in self.occurrences if one.is_resolved)

    @property
    def unresolved(self) -> tuple[ReferenceOccurrence, ...]:
        """الوقعاتُ الممتنعةُ عن التعيين؛ وامتناعُها مُسجَّلٌ لا مطويّ."""

        return tuple(one for one in self.occurrences if not one.is_resolved)

    @property
    def unresolved_by_graphic(self) -> dict[str, int]:
        """توزيعُ الممتنع على رسومه؛ فالامتناعُ يُنسَب إلى رسمه لا يُجمَل."""

        counts: dict[str, int] = {}
        for one in self.unresolved:
            counts[one.graphic] = counts.get(one.graphic, 0) + 1
        return counts

    @property
    def observed_patterns(self) -> frozenset[ReferencePattern]:
        """الأنماطُ المرجعيّةُ التي شُوهدت مُعيَّنةً في هذا النصّ."""

        return frozenset(
            one.pattern for one in self.resolved if one.pattern is not None
        )

    @property
    def unobserved_patterns(self) -> tuple[ReferencePattern, ...]:
        """أنماطُ الجدول التي لم تُشاهَد مُعيَّنةً؛ وغيابُها يُسمّى لا يُهمَل."""

        observed = self.observed_patterns
        return tuple(
            pattern for pattern in THE_REFERENCE_INVENTORY if pattern not in observed
        )


def _letters_of(text: str) -> Iterable[tuple[int, int, str]]:
    for word_index, word in enumerate(text.split()):
        letter_index = 0
        for character in word:
            if character in _HAMZA_SEATS or character in THE_UNRESOLVED_GRAPHICS:
                yield (word_index, letter_index, character)
                letter_index += 1
                continue
            if character in _BY_LETTER:
                yield (word_index, letter_index, character)
                letter_index += 1
                continue
            # شكلٌ أو شدّةٌ أو سكونٌ أو تنوين: علاماتٌ لا وقعاتُ حروف.


def read_the_deposited_ayah(text: str = FATH_AYAH_SOURCE_TEXT) -> ReferenceReading:
    """اقرأ نصًّا مُودَعًا في الطبقة المرجعيّة بالقاعدة المُعلَنة وحدَها.

    والقاعدةُ ثلاثُ خطواتٍ لا رابعَ لها: تُطرَح علاماتُ الشكل، ويُردّ كرسيُّ
    الهمزة إلى الهمزة، ويُترَك الرسمُ الملتبسُ **غيرَ مُعيَّن**. ولا ترجيحَ
    ولا سياقَ ولا استثناءَ لحرفٍ بعينه
    (`AN_UNRESOLVED_GRAPHIC_IS_LEFT_UNRESOLVED_NOT_GUESSED`).
    """

    occurrences: list[ReferenceOccurrence] = []
    for word_index, letter_index, graphic in _letters_of(text):
        if graphic in THE_UNRESOLVED_GRAPHICS:
            pattern: ReferencePattern | None = None
        else:
            pattern = _BY_LETTER[_HAMZA_SEATS.get(graphic, graphic)]
        occurrences.append(
            ReferenceOccurrence(
                word_index=word_index,
                letter_index=letter_index,
                graphic=graphic,
                pattern=pattern,
            )
        )
    return ReferenceReading(
        source_id=FATH_AYAH_SOURCE_ID, occurrences=tuple(occurrences)
    )


# --- تجربةُ الحذف: ضرورةٌ نسبيّةٌ تُقاس بالتصادم ---------------------------------


@dataclass(frozen=True, slots=True)
class AxisDeletionResult:
    """نتيجةُ حذف محورٍ واحد: ما اندمج من الأنماط تحت `T_{-i}`، مُشتقًّا."""

    deleted: Axis
    granularity: PlaceGranularity
    merged_groups: tuple[tuple[str, ...], ...]

    @property
    def distinct_output_count(self) -> int:
        """عددُ المخرجات المتمايزة بعد الحذف، مُشتقًّا من الاندماج."""

        merged_letters = sum(len(group) for group in self.merged_groups)
        return len(THE_REFERENCE_INVENTORY) - merged_letters + len(self.merged_groups)

    @property
    def axis_is_necessary_here(self) -> bool:
        """أضروريٌّ هذا المحورُ لهذا الترميز؟ نعم متى أدمج حذفُه نمطين.

        وهي **ضرورةٌ نسبيّةٌ** لا مطلقة: نسبتُها إلى الجدول المُعلَن وإلى دقّة
        المخرج المُختارة، لا إلى العربية
        (`A_DELETION_COLLISION_IS_RELATIVE_TO_THE_CHOSEN_CODING`).
        """

        return bool(self.merged_groups)


def axis_deletion_experiment(
    deleted: Axis, granularity: PlaceGranularity = PlaceGranularity.FINE
) -> AxisDeletionResult:
    """احذف محورًا مُسمًّى من الجدول كلِّه، واقرأ ما اندمج؛ يُجرى عند كلّ طلب."""

    grouped: dict[tuple[object, ...], list[str]] = {}
    for pattern in THE_REFERENCE_INVENTORY:
        grouped.setdefault(pattern.projected(deleted, granularity), []).append(
            pattern.letter
        )
    merged = tuple(
        tuple(sorted(letters)) for letters in grouped.values() if len(letters) > 1
    )
    return AxisDeletionResult(
        deleted=deleted,
        granularity=granularity,
        merged_groups=tuple(sorted(merged)),
    )


def granularity_sensitivity(
    deleted: Axis = Axis.EMPHASIS,
) -> dict[PlaceGranularity, AxisDeletionResult]:
    """أجرِ الحذفَ نفسَه تحت الدقّتين، فيُقرَأ أثرُ الدقّة على النتيجة.

    وهذه هي **النتيجةُ السالبةُ الأقوى** في هذا الإيداع: أزواجُ الروادف — أي
    ما يتصادم عند حذف التفخيم — ليست معطًى في المادّة، بل دالّةٌ في دقّة تصنيف
    المخارج المُختارة (`THE_GRANULARITY_IS_A_KNOB_SO_THE_PAIRS_ARE_NOT_A_FINDING`).
    """

    return {
        granularity: axis_deletion_experiment(deleted, granularity)
        for granularity in PlaceGranularity
    }


# --- الانتقالاتُ: إحصاءٌ في الترميز المتوقَّع لا مشاهدةٌ زمنيّة --------------------


class PhoneticWaslAndWaqfRemainDeferred(Enum):
    """حالُ الوصل والوقف الصوتيَّين بعد هذا الإحصاء؛ مُخرَجٌ واحدٌ لا ثالثَ له."""

    DEFER = "مُرجأٌ_لانتفاء_مشاهدةٍ_زمنيّة"


@dataclass(frozen=True, slots=True)
class TransitionCensus:
    """إحصاءُ الأزواج المتجاورة داخل الكلمات، وأنواعِ انتقالها المُشتقّة."""

    source_id: str
    pairs: tuple[tuple[str, str], ...]
    """أزواجُ **الحروف المرجعيّة** لا أزواجُ الرسم؛ فكرسيُّ الهمزة مردودٌ إليها."""

    @property
    def pair_count(self) -> int:
        """عددُ الأزواج المتجاورة المُعيَّنِ طرفاها، مُشتقًّا."""

        return len(self.pairs)

    @property
    def transition_types(self) -> tuple[tuple[CoarsePlace, CoarsePlace], ...]:
        """أنواعُ انتقال فئة الممرّ الفمويّ، مرتّبةً ومتمايزة."""

        seen = {
            (
                _BY_LETTER[first].coarse_place,
                _BY_LETTER[second].coarse_place,
            )
            for first, second in self.pairs
        }
        return tuple(sorted(seen, key=lambda pair: (pair[0].value, pair[1].value)))

    @property
    def phonetic_wasl_and_waqf(self) -> PhoneticWaslAndWaqfRemainDeferred:
        """مهما بلغ العددُ، الوصلُ والوقفُ الصوتيّان مُرجآن؛ والعلّةُ بنيويّة.

        فالمُحصى انتقالاتٌ بين **قيمٍ متوقَّعةٍ في ترميز**، ولا زمنَ فيها ولا
        حركةَ عضوٍ مقيسة؛ ورفعُ الإرجاء بها استدلالٌ من جنسٍ على جنسٍ آخر
        (`A_CODING_TRANSITION_IS_NOT_AN_ARTICULATORY_OBSERVATION`).
        """

        return PhoneticWaslAndWaqfRemainDeferred.DEFER


def transition_census(reading: ReferenceReading) -> TransitionCensus:
    """أحصِ الأزواجَ المتجاورة **داخل الكلمة الواحدة** المُعيَّنَ طرفاها.

    ويُشترَط التجاورُ في الرسم داخل كلمةٍ واحدة: فما بين كلمتين يمسّ الوصلَ،
    وهو مُرجأٌ؛ وما تخلّله رسمٌ غيرُ مُعيَّنٍ فليس متجاورًا في هذه الطبقة.
    """

    pairs: list[tuple[str, str]] = []
    previous: ReferenceOccurrence | None = None
    for current in reading.occurrences:
        if (
            previous is not None
            and previous.is_resolved
            and current.is_resolved
            and previous.word_index == current.word_index
            and previous.letter_index + 1 == current.letter_index
        ):
            assert previous.pattern is not None
            assert current.pattern is not None
            pairs.append((previous.pattern.letter, current.pattern.letter))
        previous = current
    return TransitionCensus(source_id=reading.source_id, pairs=tuple(pairs))


# --- المحايدُ: تحصيلُ حاصلٍ يُفحَص ولا يُقرَأ اكتشافًا ---------------------------


Constraint = Mapping[Axis, object]
"""قيدٌ: تعيينُ قيمٍ لبعض المحاور؛ وما لم يُعيَّن فغيرُ مقيَّد."""


def the_empty_constraint() -> dict[Axis, object]:
    """`e = ∅`: القيدُ الفارغ، لا محورَ فيه مُعيَّنًا."""

    return {}


def add_constraint(first: Constraint, second: Constraint) -> dict[Axis, object]:
    """`⊕`: ضمُّ قيدٍ إلى قيد؛ ويُرفَض التعارضُ ولا يُرجَّح أحدُ الطرفين.

    وبهذا البناء يصدق `e ⊕ p = p` لكلّ `p` **بالتعريف**؛ فالتحقّقُ منه فحصُ
    اتّساقٍ للشفرة، لا خبرٌ عن العربية ولا عن الهواء
    (`THE_NEUTRAL_ELEMENT_IS_ANALYTIC_NOT_MEASURED`).
    """

    joined = dict(first)
    for axis, value in second.items():
        if axis in joined and joined[axis] != value:
            raise ReferenceArticulationError(
                "قيدان متعارضان على محورٍ واحدٍ لا يُضمّان؛ والترجيحُ ليس ضمًّا"
            )
        joined[axis] = value
    return joined


# --- المُخرَجُ: منزلةٌ مُعلَنةٌ لا دعوى ولادة ------------------------------------


class InternalLawStanding(Enum):
    """حالُ دعوى «القانون الداخليّ الأدنى» بعد التشغيل؛ ثلاثةٌ مغلقة."""

    A_MINIMAL_INTERNAL_LAW_IS_BORN = "قانونٌ_داخليٌّ_أدنى_مولود"
    RELATIVE_NECESSITY_OF_A_CHOSEN_CODING = "ضرورةٌ_نسبيّةٌ_لترميزٍ_مختار"
    NOT_EVEN_A_RELATIVE_NECESSITY = "لا_ضرورةَ_حتّى_نسبيّة"


@dataclass(frozen=True, slots=True)
class InternalLawDecision:
    """قرارٌ مُشتقٌّ من التشغيل: أَوَلَد النصُّ قانونًا، أم ضرورةً نسبيّة؟"""

    standing: InternalLawStanding
    necessary_axes: tuple[Axis, ...]
    granularity_changes_the_result: bool

    @property
    def a_mechanical_fiber_is_born(self) -> bool:
        """لا. والمنفيُّ يُكتَب منفيًّا لئلّا يُقرَأ سكوتُ الشفرة احتمالًا."""

        return False

    @property
    def a_fibonacci_law_is_extracted(self) -> bool:
        """لا. ولم تُجرَ ههنا تجربةٌ تبحث عنه أصلًا، فالنفيُ نفيُ دعوى لا نتيجة."""

        return False


def assess_internal_law(
    granularity: PlaceGranularity = PlaceGranularity.FINE,
) -> InternalLawDecision:
    """اقرأ منزلةَ الدعوى من تجربة الحذف نفسِها، لا من وسمٍ يُكتَب.

    فإن كان كلُّ محورٍ ضروريًّا — يُدمِج حذفُه نمطين — فالمُخرَجُ **ضرورةٌ
    نسبيّةٌ لترميزٍ مختار**، لا قانونٌ داخليٌّ أدنى: المحاورُ لم تُشتقّ من
    المادّة، وأثرُ دقّة المخرج على النتيجة مُشتقٌّ ومُسجَّلٌ في القرار نفسِه.
    """

    results = {axis: axis_deletion_experiment(axis, granularity) for axis in THE_AXES}
    necessary = tuple(axis for axis in THE_AXES if results[axis].axis_is_necessary_here)
    sensitivity = granularity_sensitivity()
    changes = (
        sensitivity[PlaceGranularity.FINE].merged_groups
        != sensitivity[PlaceGranularity.COARSE].merged_groups
    )
    if not necessary:
        standing = InternalLawStanding.NOT_EVEN_A_RELATIVE_NECESSITY
    else:
        standing = InternalLawStanding.RELATIVE_NECESSITY_OF_A_CHOSEN_CODING
    return InternalLawDecision(
        standing=standing,
        necessary_axes=necessary,
        granularity_changes_the_result=changes,
    )


# --- ما لا تحسمه هذه التجربة، مُسمًّى ------------------------------------------


THE_FOUR_AXES_ARE_AN_IMPORTED_CODING_NOT_A_MEASURED_BASIS: Final[str] = (
    "THE_FOUR_AXES_ARE_AN_IMPORTED_CODING_NOT_A_MEASURED_BASIS: الطريقةُ "
    "والموضعُ والجهرُ والتفخيمُ اختيارُ ترميزٍ سابقٌ للقياس، لم يُشتقّ من حروف "
    "الآية بلا مقدّمات؛ فكلُّ ضرورةٍ تُقاس هنا ضرورةٌ لهذا الاختيار"
)

A_DELETION_COLLISION_IS_RELATIVE_TO_THE_CHOSEN_CODING: Final[str] = (
    "A_DELETION_COLLISION_IS_RELATIVE_TO_THE_CHOSEN_CODING: تصادمُ نمطين عند "
    "حذف محورٍ يُثبِت ضرورةَ المحور **في هذا الجدول**؛ ولا يُقرأ قانونًا في "
    "العربية ولا ضرورةً في جهاز النطق"
)

THE_FEATURE_VALUES_ARE_MODERN_DESCRIPTIVE_NOT_CLASSICAL: Final[str] = (
    "THE_FEATURE_VALUES_ARE_MODERN_DESCRIPTIVE_NOT_CLASSICAL: قيمُ السمات "
    "وصفيّةٌ حديثة، وتخالف صفاتِ التجويد في مواضعَ مُسمّاة — منها الطاءُ "
    "مهموسةً ههنا ومجهورةً في التراث؛ فالجدولُ لا يُنسَب إلى مصدرٍ تراثيّ"
)

THIS_TABLE_IS_BORN_HERE_SO_IT_CARRIES_NO_FOREIGN_WARRANT: Final[str] = (
    "THIS_TABLE_IS_BORN_HERE_SO_IT_CARRIES_NO_FOREIGN_WARRANT: الجدولُ مكتوبٌ "
    "في هذه الوحدة، لم يُستورَد من مواصفةٍ مُبصَّمةٍ ولم يمرّ بحاجز الاستيراد؛ "
    "فهو دعوى هذه الشجرة وحدَها، ولا يُحتجّ به على أنّه منقولٌ عن مصدرٍ مستقلّ"
)

AN_UNRESOLVED_GRAPHIC_IS_LEFT_UNRESOLVED_NOT_GUESSED: Final[str] = (
    "AN_UNRESOLVED_GRAPHIC_IS_LEFT_UNRESOLVED_NOT_GUESSED: الرسمُ الملتبسُ بين "
    "صامتٍ ومدٍّ يُترَك بلا تعيين؛ وترجيحُه بالسياق يُدخِل في البيانات ما يُراد "
    "إخراجُه منها، فتصير النتيجةُ صدًى للترجيح"
)

A_CODING_TRANSITION_IS_NOT_AN_ARTICULATORY_OBSERVATION: Final[str] = (
    "A_CODING_TRANSITION_IS_NOT_AN_ARTICULATORY_OBSERVATION: الانتقالاتُ "
    "المُحصاةُ انتقالاتٌ بين قيمٍ متوقَّعةٍ في ترميز، لا مشاهداتٌ زمنيّةٌ لحركة "
    "الأعضاء؛ فلا يُرفَع بها إرجاءُ الوصل والوقف الصوتيَّين"
)

THE_GRANULARITY_IS_A_KNOB_SO_THE_PAIRS_ARE_NOT_A_FINDING: Final[str] = (
    "THE_GRANULARITY_IS_A_KNOB_SO_THE_PAIRS_ARE_NOT_A_FINDING: أزواجُ الروادف "
    "المتصادمةُ عند حذف التفخيم تتبدّل بتبدّل دقّة تصنيف المخارج؛ فهي نتيجةُ "
    "مقبضٍ في الأداة لا خاصّيّةٌ في المادّة"
)

THE_NEUTRAL_ELEMENT_IS_ANALYTIC_NOT_MEASURED: Final[str] = (
    "THE_NEUTRAL_ELEMENT_IS_ANALYTIC_NOT_MEASURED: صدقُ `e = ∅` و`e ⊕ p = p` "
    "تحصيلُ حاصلٍ من تعريف `⊕`؛ والتحقّقُ منه فحصُ اتّساقٍ للشفرة لا اكتشافٌ"
)

THE_REAL_AIR_IS_AN_OPERATING_CONDITION_NOT_THE_EMPTY_CONSTRAINT: Final[str] = (
    "THE_REAL_AIR_IS_AN_OPERATING_CONDITION_NOT_THE_EMPTY_CONSTRAINT: الهواءُ "
    "الحقيقيُّ شرطُ تشغيلٍ لا قيدٌ فارغ، والألفُ المكتوبةُ ليست تلقائيًّا أيًّا "
    "منهما؛ وثلاثتُها تُفصَل ولا يُحمَل أحدُها على الآخر"
)

NO_MECHANICAL_FIBER_IS_BORN_HERE: Final[str] = (
    "NO_MECHANICAL_FIBER_IS_BORN_HERE: هذه طبقةٌ مرجعيّةٌ يمكن أن تُختبَر بها "
    "هندسةُ الشفتين واللسان والأنف والحنجرة؛ ولم تُثبَت بها ولادةُ ليفٍ "
    "ميكانيكيٍّ مكتمل، ولا يُقرَأ قيامُها قيامًا له"
)

NO_FIBONACCI_LAW_IS_EXTRACTED_HERE: Final[str] = (
    "NO_FIBONACCI_LAW_IS_EXTRACTED_HERE: لم يُستخرَج من هذه الطبقة قانونٌ "
    "فيبوناتشيّ، ولم تُجرَ تجربةٌ تبحث عنه؛ والنفيُ مكتوبٌ لئلّا يُقرَأ سكوتُ "
    "الشفرة عنه احتمالًا مفتوحًا"
)

REFERENCE_ARTICULATION_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "THE_FOUR_AXES_ARE_AN_IMPORTED_CODING_NOT_A_MEASURED_BASIS": (
        THE_FOUR_AXES_ARE_AN_IMPORTED_CODING_NOT_A_MEASURED_BASIS
    ),
    "A_DELETION_COLLISION_IS_RELATIVE_TO_THE_CHOSEN_CODING": (
        A_DELETION_COLLISION_IS_RELATIVE_TO_THE_CHOSEN_CODING
    ),
    "THE_FEATURE_VALUES_ARE_MODERN_DESCRIPTIVE_NOT_CLASSICAL": (
        THE_FEATURE_VALUES_ARE_MODERN_DESCRIPTIVE_NOT_CLASSICAL
    ),
    "THIS_TABLE_IS_BORN_HERE_SO_IT_CARRIES_NO_FOREIGN_WARRANT": (
        THIS_TABLE_IS_BORN_HERE_SO_IT_CARRIES_NO_FOREIGN_WARRANT
    ),
    "AN_UNRESOLVED_GRAPHIC_IS_LEFT_UNRESOLVED_NOT_GUESSED": (
        AN_UNRESOLVED_GRAPHIC_IS_LEFT_UNRESOLVED_NOT_GUESSED
    ),
    "A_CODING_TRANSITION_IS_NOT_AN_ARTICULATORY_OBSERVATION": (
        A_CODING_TRANSITION_IS_NOT_AN_ARTICULATORY_OBSERVATION
    ),
    "THE_GRANULARITY_IS_A_KNOB_SO_THE_PAIRS_ARE_NOT_A_FINDING": (
        THE_GRANULARITY_IS_A_KNOB_SO_THE_PAIRS_ARE_NOT_A_FINDING
    ),
    "THE_NEUTRAL_ELEMENT_IS_ANALYTIC_NOT_MEASURED": (
        THE_NEUTRAL_ELEMENT_IS_ANALYTIC_NOT_MEASURED
    ),
    "THE_REAL_AIR_IS_AN_OPERATING_CONDITION_NOT_THE_EMPTY_CONSTRAINT": (
        THE_REAL_AIR_IS_AN_OPERATING_CONDITION_NOT_THE_EMPTY_CONSTRAINT
    ),
    "NO_MECHANICAL_FIBER_IS_BORN_HERE": NO_MECHANICAL_FIBER_IS_BORN_HERE,
    "NO_FIBONACCI_LAW_IS_EXTRACTED_HERE": NO_FIBONACCI_LAW_IS_EXTRACTED_HERE,
}
"""ما لا تحسمه هذه التجربة، مُسمًّى هنا لا متروكًا ليُفترَض."""
