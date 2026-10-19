"""«لا صامتَ بلا صائتٍ رياضيًّا»: الدعوى مفصولةً إلى أربع قراءاتٍ لكلٍّ حكمُها.

العبارةُ بإطلاقها تجمع أربعَ دعاوى متمايزةَ الحكم، فجمعُها يُخفي انتقاضَ
إحداها في انعقاد أخرى (`AnAbsoluteReadingHidesADividedVerdict`). وههنا تُفصَل،
ويُقاس لكلِّ قراءةٍ حكمُها من هذه الشجرة وحدَها:

1. **لا مقطعَ بلا صائت** — منعقدةٌ **بالبناء** في جبر القوالب المُجمَّد: ستّةُ
   قوالبَ كلُّها `CV…`، و`template_of` ترفض افتتاحًا غيرَ الواحد وترفض نواةً
   خارج `{1, 2}`. فالنواةُ لازمةٌ في كلّ قالب، والانعقادُ نتيجةُ تعريفٍ لا
   نتيجةُ عدّ (`ThisHoldsByTheFrozenAlgebraNotByTheCorpus`).

2. **لا صامتَ مفتتِحًا بلا صائت** — منعقدةٌ **رفضًا لا إقرارًا**: المُقطِّعُ لا
   يقبل صامتًا ساكنًا لا يحمل حركةً ولا يُغلِق نواةً قبله، بل يقف ويُسمّي
   موضعَه. وانعقادُها مقروءٌ من وقوفه لا من سكوته.

3. **لا صامتَ بلا صائتٍ بإطلاق** — **منتقضةٌ** في هذه الشجرة: الإغلاقُ صامتٌ
   لا حركةَ له، و`CVC` و`CVCC` في القوالب المُجمَّدة، والإغلاقاتُ معدودةٌ في
   المقاطع المُخرَجة. فالقراءةُ الثالثةُ تنتقض بالقالب قبل أن تنتقض بالعدّ.

4. **لا صامتَ يُنطَق بلا صائتٍ يُنطَق** — **غيرُ قابلةٍ للاختبار ههنا**:
   `UnicodeIsNotRecordedSound` قائم، فلا قطعةَ في هذه الشجرة صوتٌ مُسجَّل.
   وتُكتَب محجوبةً بمانعها لا تُحذَف (`AnUntestableReadingIsWrittenNotDropped`).

**والأعدادُ مُشتَقّةٌ لا منقولة**: تُعاد من بايتات الإيداع المُبصَّمة عند كلّ
تشغيل، وبصمتُها في المخرَج. والمتعذِّرُ من الكلمات يُحمَل في المخرَج بعلّته ولا
يُطرَح من المقام، لأنّ طرحَه يرفع نسبةً بإخفاء ما لم يُقرأ
(`AnUnsegmentedWordIsCarriedNotDropped`).

**وحدودُ الدعوى حدودُ مصدرها**: ما يُقاس ههنا نصٌّ واحدٌ بعينه بوزنٍ واحدٍ من
قوالبَ مُجمَّدة، فلا يُقرأ حكمًا على العربيّة ولا على المقطع في ذاته
(`AVerdictHereIsAVerdictOnThisDepositUnderTheseTemplates`).

تسجيلٌ لا سلطة: لا ولادةَ ههنا ولا حكمَ ولادةٍ كرنليًّا ولا تجميدَ `E0`، ولا
تُوصَل `BirthVerdictGate` بهذه الوحدة، ولا تستورد من `kernel/` شيئًا.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from .carrier_state_observed_fiber import (
    ABSENT,
    ObservedFiberTable,
    run_observed_fiber_on_the_deposited_fatiha,
)
from .syllabifier import SlotKind, syllabify_surface
from .syllable_preregistration import (
    SyllablePreregistrationError,
    SyllableTemplate,
    template_of,
)

__all__ = [
    "AN_ABSOLUTE_READING_HIDES_A_DIVIDED_VERDICT_NOTE",
    "AN_UNSEGMENTED_WORD_IS_CARRIED_NOT_DROPPED_NOTE",
    "AN_UNTESTABLE_READING_IS_WRITTEN_NOT_DROPPED_NOTE",
    "A_VERDICT_HERE_IS_A_VERDICT_ON_THIS_DEPOSIT_NOTE",
    "NO_CONSONANT_WITHOUT_A_VOWEL_NAMED_RESIDUALS",
    "THE_CLAIM",
    "THIS_HOLDS_BY_THE_FROZEN_ALGEBRA_NOT_BY_THE_CORPUS_NOTE",
    "ClaimReading",
    "ClaimVerdict",
    "NoConsonantWithoutAVowelError",
    "ReadingVerdict",
    "SyllableCensus",
    "every_frozen_template_has_a_nucleus",
    "no_template_opens_without_a_vowel",
    "read_the_claim",
    "take_syllable_census",
]


class NoConsonantWithoutAVowelError(ValueError):
    """رفضٌ صريح: حكمٌ بلا سببٍ مكتوب، أو عدٌّ يخالف المقام المُعلَن."""


THE_CLAIM: Final[str] = "لا صامتَ بلا صائتٍ رياضيًّا"


class ClaimReading(Enum):
    """القراءاتُ الأربعُ للدعوى، متمايزةً لا تُجمَع في حكمٍ واحد."""

    NO_SYLLABLE_WITHOUT_A_NUCLEUS = "لا مقطعَ بلا صائت"
    NO_ONSET_WITHOUT_A_VOWEL = "لا صامتَ مفتتِحًا بلا صائت"
    NO_CONSONANT_AT_ALL_WITHOUT_A_VOWEL = "لا صامتَ بلا صائتٍ بإطلاق"
    NO_PRONOUNCED_CONSONANT_WITHOUT_A_PRONOUNCED_VOWEL = "لا صامتَ يُنطَق بلا صائتٍ يُنطَق"


class ClaimVerdict(Enum):
    """حكمُ القراءة الواحدة؛ والانتقاضُ غيرُ التعذّر، والبناءُ غيرُ العدّ."""

    HELD_BY_CONSTRUCTION = "منعقدةٌ_بالبناء"
    HELD_AS_A_REFUSAL = "منعقدةٌ_رفضًا"
    REFUTED = "منتقضة"
    UNTESTABLE_HERE = "غيرُ_قابلةٍ_للاختبار_ههنا"


@dataclass(frozen=True)
class ReadingVerdict:
    """حكمُ قراءةٍ واحدة، ومعه ما حمله من عددٍ وما بقي عليه من حدّ."""

    reading: ClaimReading
    verdict: ClaimVerdict
    what_decided_it: str
    witness_count: int
    residuals: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.what_decided_it.strip():
            raise NoConsonantWithoutAVowelError("حكمٌ بلا سببٍ مكتوب")
        if self.witness_count < 0:
            raise NoConsonantWithoutAVowelError("عددُ الشواهد غيرُ سالب")
        if not self.residuals:
            raise NoConsonantWithoutAVowelError(
                f"«{self.reading.value}» بلا بقيّةٍ مُسمّاة؛ والخلوُّ ليس إعفاءً"
            )
        if any(not item.strip() for item in self.residuals):
            raise NoConsonantWithoutAVowelError("في البقايا مدخلٌ فارغ")
        if self.verdict is ClaimVerdict.UNTESTABLE_HERE and self.witness_count:
            raise NoConsonantWithoutAVowelError(
                "قراءةٌ متعذّرةٌ تحمل شواهدَ عدٍّ؛ والتعذّرُ لا يُعَدّ"
            )


# --- العدُّ من الإيداع -----------------------------------------------------------


@dataclass(frozen=True)
class SyllableCensus:
    """إحصاءُ المقاطع على إيداعٍ مُبصَّم؛ والمتعذّرُ محمولٌ لا مطروح."""

    deposit_sha256: str
    word_total: int
    segmented_words: int
    unsegmented_words: int
    syllable_total: int
    syllables_without_a_nucleus: int
    coda_consonants: int
    onsetless_halts: int
    surface_carriers: int
    surface_carriers_bearing_a_vowel: int
    surface_carriers_bearing_a_sukun: int
    templates_seen: tuple[tuple[str, int], ...]

    def __post_init__(self) -> None:
        if self.segmented_words + self.unsegmented_words != self.word_total:
            raise NoConsonantWithoutAVowelError(
                "المقطَّعُ والمتعذّرُ لا يجمعان مجتمعَ الكلمات؛ والمقامُ لا يُنقَص"
            )
        if self.surface_carriers_bearing_a_vowel > self.surface_carriers:
            raise NoConsonantWithoutAVowelError("الحاملُ المتحرّكُ أكثرُ من الحوامل")


def _distinct_words_in_order(table: ObservedFiberTable) -> tuple[str, ...]:
    """كلماتُ الإيداع بترتيب ورودها؛ مفتاحُها موضعُها لا نصُّها."""

    seen: set[tuple[int, int]] = set()
    words: list[str] = []
    for row in table.rows:
        key = (row.line_index, row.word_index)
        if key in seen:
            continue
        seen.add(key)
        words.append(row.word)
    return tuple(words)


def _axis(state_vector: tuple[tuple[str, str], ...], axis_id: str) -> str:
    for measured_axis, value in state_vector:
        if measured_axis == axis_id:
            return value
    raise NoConsonantWithoutAVowelError(f"المحورُ «{axis_id}» ليس في المتَّجِه المقيس")


def take_syllable_census(table: ObservedFiberTable | None = None) -> SyllableCensus:
    """أحصِ المقاطعَ والإغلاقاتِ والمواضعَ المتعذّرة من إيداعٍ مُبصَّم."""

    measured = run_observed_fiber_on_the_deposited_fatiha() if table is None else table
    words = _distinct_words_in_order(measured)

    segmented = 0
    unsegmented = 0
    syllable_total = 0
    nucleusless = 0
    codas = 0
    onsetless_halts = 0
    templates: dict[str, int] = {}

    for surface in words:
        word = syllabify_surface(surface)
        if not word.is_resolved:
            unsegmented += 1
            onsetless_halts += len(word.wazn_unresolved)
            continue
        segmented += 1
        for syllable in word.syllables:
            syllable_total += 1
            templates[syllable.template.value] = (
                templates.get(syllable.template.value, 0) + 1
            )
            vowels = [slot for slot in syllable.slots if slot.kind is SlotKind.VOWEL]
            consonants = [
                slot for slot in syllable.slots if slot.kind is SlotKind.CONSONANT
            ]
            if not vowels:
                nucleusless += 1
            codas += len(consonants) - 1

    return SyllableCensus(
        deposit_sha256=measured.deposit.sha256,
        word_total=len(words),
        segmented_words=segmented,
        unsegmented_words=unsegmented,
        syllable_total=syllable_total,
        syllables_without_a_nucleus=nucleusless,
        coda_consonants=codas,
        onsetless_halts=onsetless_halts,
        surface_carriers=len(measured.rows),
        surface_carriers_bearing_a_vowel=sum(
            1 for row in measured.rows if _axis(row.state_vector, "vowel") != ABSENT
        ),
        surface_carriers_bearing_a_sukun=sum(
            1
            for row in measured.rows
            if _axis(row.state_vector, "quiescence") != ABSENT
        ),
        templates_seen=tuple(sorted(templates.items())),
    )


# --- الجبرُ المُجمَّد، مقروءًا لا مُعادًا كتابته -------------------------------------


def every_frozen_template_has_a_nucleus() -> bool:
    """أفي كلّ قالبٍ من الستّة نواةٌ صائتة؟ يُقرَأ من شكل القالب نفسِه."""

    return all("V" in template.value for template in SyllableTemplate)


def no_template_opens_without_a_vowel() -> bool:
    """أترفض `template_of` افتتاحًا بغير صامتٍ واحد، ونواةً خارجَ `{1, 2}`؟"""

    for onset in (0, 2):
        try:
            template_of(onset, 1, 0)
        except SyllablePreregistrationError:
            continue
        return False
    for nucleus in (0, 3):
        try:
            template_of(1, nucleus, 0)
        except SyllablePreregistrationError:
            continue
        return False
    return True


# --- قراءةُ الدعوى ----------------------------------------------------------------


_NO_RECORDED_SOUND_PREVENTER: Final[str] = (
    "UnicodeIsNotRecordedSound: لا قطعةَ في هذه الشجرة صوتٌ مُسجَّل، فالقراءةُ "
    "الصوتيّة غيرُ قابلةٍ للاختبار ههنا بحال"
)

_THIS_DEPOSIT_ONLY: Final[str] = (
    "العددُ عددُ وقوعاتٍ في نصٍّ واحدٍ بعينه على رسم ناسخه، لا حكمٌ على العربيّة"
)


def read_the_claim(
    census: SyllableCensus | None = None,
) -> tuple[ReadingVerdict, ...]:
    """اقرأ الدعوى قراءاتِها الأربعَ، ولكلِّ قراءةٍ حكمٌ وشاهدٌ وبقيّة."""

    counted = take_syllable_census() if census is None else census

    if not every_frozen_template_has_a_nucleus():
        raise NoConsonantWithoutAVowelError(
            "قالبٌ في الستّة بلا نواة؛ والقراءةُ الأولى تُقرَأ من الجبر لا تُفترَض"
        )
    if not no_template_opens_without_a_vowel():
        raise NoConsonantWithoutAVowelError(
            "`template_of` قبلت افتتاحًا أو نواةً خارجَ المُعلَن"
        )
    if counted.syllables_without_a_nucleus:
        raise NoConsonantWithoutAVowelError(
            "مقطعٌ مُخرَجٌ بلا نواة؛ وذلك يناقض الجبرَ المُجمَّد فيُرفَع لا يُطوى"
        )

    return (
        ReadingVerdict(
            reading=ClaimReading.NO_SYLLABLE_WITHOUT_A_NUCLEUS,
            verdict=ClaimVerdict.HELD_BY_CONSTRUCTION,
            what_decided_it=(
                "القوالبُ الستّةُ كلُّها `CV…`، و`template_of` ترفض افتتاحًا غيرَ "
                "الواحد ونواةً خارج {1, 2}؛ فالنواةُ لازمةٌ بالتعريف، ولم يُخرِج "
                f"المُقطِّعُ مقطعًا واحدًا بلا نواةٍ في {counted.syllable_total} مقطعًا"
            ),
            witness_count=counted.syllable_total,
            residuals=(
                "THIS_HOLDS_BY_THE_FROZEN_ALGEBRA_NOT_BY_THE_CORPUS: انعقادُها "
                "نتيجةُ تعريفٍ لا شهادةُ استقراء، والمدوّنةُ توافقه ولا تُثبِته",
                "القوالبُ الستّةُ مُجمَّدةٌ قبل العدّ، فلو وقع شكلٌ خارجَها لرُدَّت "
                "الكلمةُ ولم يُوسَّع القالب",
            ),
        ),
        ReadingVerdict(
            reading=ClaimReading.NO_ONSET_WITHOUT_A_VOWEL,
            verdict=ClaimVerdict.HELD_AS_A_REFUSAL,
            what_decided_it=(
                "المُقطِّعُ يقف عند صامتٍ ساكنٍ لا يحمل حركةً ولا يُغلِق نواةً "
                f"قبله، ويُسمّي موضعَه؛ ووقف {counted.onsetless_halts} مرّةً في "
                f"{counted.unsegmented_words} كلمةً من {counted.word_total}"
            ),
            witness_count=counted.onsetless_halts,
            residuals=(
                "AN_UNSEGMENTED_WORD_IS_CARRIED_NOT_DROPPED: الكلماتُ المتعذّرةُ "
                "محمولةٌ في المقام بعلّتها، ولا تُطرَح لترتفع نسبة",
                "الوقوفُ حدٌّ على دالّة التقطيع في هذه الشجرة، وأكثرُه عند ألفٍ "
                "عاريةٍ لا تُميّز همزةَ الوصل؛ فليس نفيًا لوجود الصورة في اللغة",
                _THIS_DEPOSIT_ONLY,
            ),
        ),
        ReadingVerdict(
            reading=ClaimReading.NO_CONSONANT_AT_ALL_WITHOUT_A_VOWEL,
            verdict=ClaimVerdict.REFUTED,
            what_decided_it=(
                "الإغلاقُ صامتٌ لا حركةَ له، و`CVC` و`CVCC` و`CVVC` و`CVVCC` في "
                f"القوالب المُجمَّدة؛ ووقع في المُخرَج {counted.coda_consonants} "
                f"إغلاقًا في {counted.syllable_total} مقطعًا، وحمل "
                f"{counted.surface_carriers_bearing_a_sukun} حاملًا في الرسم "
                f"علامةَ سكونٍ من {counted.surface_carriers}"
            ),
            witness_count=counted.coda_consonants,
            residuals=(
                "انتقاضُها بالقالب قبل العدّ: لو خلا الإيداعُ من إغلاقٍ واحدٍ "
                "لبقيت منتقضةً بوجود CVC في الجبر المُجمَّد",
                "الإغلاقُ في الرسم غيرُ الإغلاق في النطق، وهذا حكمٌ على الأوّل",
                _THIS_DEPOSIT_ONLY,
            ),
        ),
        ReadingVerdict(
            reading=ClaimReading.NO_PRONOUNCED_CONSONANT_WITHOUT_A_PRONOUNCED_VOWEL,
            verdict=ClaimVerdict.UNTESTABLE_HERE,
            what_decided_it=_NO_RECORDED_SOUND_PREVENTER,
            witness_count=0,
            residuals=(
                "AN_UNTESTABLE_READING_IS_WRITTEN_NOT_DROPPED: بقاؤها مكتوبةً "
                "محجوبةً شاهدٌ على أنّها لم تُحذَف لتعذّرها",
                "تعذُّرُ اختبارها ههنا ليس نفيًا لها ولا إثباتًا",
            ),
        ),
    )


# --- الحدودُ مُسمّاةً -------------------------------------------------------------


AN_ABSOLUTE_READING_HIDES_A_DIVIDED_VERDICT_NOTE: Final[str] = (
    "AnAbsoluteReadingHidesADividedVerdict: «لا صامتَ بلا صائت» بإطلاقها تجمع "
    "أربعَ دعاوى مختلفةَ الحكم؛ فجمعُها يُخفي انتقاضَ إحداها في انعقاد أخرى، "
    "ولذلك تُفصَل ولا يُصدَر لها حكمٌ واحد"
)

THIS_HOLDS_BY_THE_FROZEN_ALGEBRA_NOT_BY_THE_CORPUS_NOTE: Final[str] = (
    "ThisHoldsByTheFrozenAlgebraNotByTheCorpus: «لا مقطعَ بلا صائت» منعقدةٌ "
    "لأنّ القوالبَ الستّةَ عُرِّفت كذلك، لا لأنّ المدوّنةَ شهدت؛ وموافقةُ "
    "المدوّنة تصديقٌ لا برهان"
)

AN_UNSEGMENTED_WORD_IS_CARRIED_NOT_DROPPED_NOTE: Final[str] = (
    "AnUnsegmentedWordIsCarriedNotDropped: الكلمةُ المتعذّرةُ محمولةٌ في المقام "
    "بعلّتها؛ وطرحُها يرفع نسبةً بإخفاء ما لم يُقرأ"
)

AN_UNTESTABLE_READING_IS_WRITTEN_NOT_DROPPED_NOTE: Final[str] = (
    "AnUntestableReadingIsWrittenNotDropped: القراءةُ الصوتيّةُ مكتوبةٌ محجوبةٌ "
    "بمانعها لا محذوفةٌ لتعذّرها، وتعذّرُها ليس نفيًا ولا إثباتًا"
)

A_VERDICT_HERE_IS_A_VERDICT_ON_THIS_DEPOSIT_NOTE: Final[str] = (
    "AVerdictHereIsAVerdictOnThisDepositUnderTheseTemplates: ما يُقاس نصٌّ "
    "واحدٌ بعينه بقوالبَ مُجمَّدةٍ بعينها؛ فلا يُقرَأ حكمًا على العربيّة ولا "
    "على المقطع في ذاته، ولا ولادةَ ههنا ولا حكمَ ولادة"
)

NO_CONSONANT_WITHOUT_A_VOWEL_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    AN_ABSOLUTE_READING_HIDES_A_DIVIDED_VERDICT_NOTE,
    THIS_HOLDS_BY_THE_FROZEN_ALGEBRA_NOT_BY_THE_CORPUS_NOTE,
    AN_UNSEGMENTED_WORD_IS_CARRIED_NOT_DROPPED_NOTE,
    AN_UNTESTABLE_READING_IS_WRITTEN_NOT_DROPPED_NOTE,
    A_VERDICT_HERE_IS_A_VERDICT_ON_THIS_DEPOSIT_NOTE,
)
