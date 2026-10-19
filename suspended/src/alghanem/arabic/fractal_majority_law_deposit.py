"""إيداعُ الجدول الفراكتاليّ **قانونًا غالبًا** بأربعة كسورٍ مسمّاةٍ بمواضعها.

قيل في المحادثة إنّ العمليات الثلاث — وصلٌ وقطعٌ وإعادةُ تركيب — تتكرّر في كلّ
مستوًى، وإنّ التكرار «غالبٌ لا تام». وهذا الملفُّ يُودِع تلك الدعوى **بصورتها
التي تصحّ أن تُبنى عليها**: جدولَ مستوياتٍ كلُّ صفٍّ فيه إمّا مقيسٌ على بايتاتٍ
مختومةٍ ههنا، أو منقولٌ يُسمّى ناقلَه، أو **مكسورٌ يُسمّى موضعَ كسره**. ويفترق
ههنا ثلاثةُ أجناسٍ كانت تُقرأ «قانونًا» واحدًا::

    AMajorityLaw             != ATotalLaw
    ABreakNamedWithItsPlace  != AnExceptionSwallowedIntoTheRule
    MeasuredOnOurSealedBytes != QuotedFromTheSiblingProgram

**أوّلًا: القانونُ غالبٌ، وهذا وصفُه لا عذرُه.** لا يُكتَب ههنا صفٌّ يقول
«تتكرّر العمليات الثلاث في كلّ مستوًى» ثمّ يُلحَق به استثناءٌ في حاشية. بل
تُعدّ الكسورُ أربعةً، لكلٍّ منها **موضعٌ ومصدر**، وتُحسَب نسبةُ الصفوف المقيسة
ههنا من جملة الصفوف بالحساب لا بالكتابة. فمن ادّعى تمامًا فقد ادّعى ما لا
يُصدِّقه الجدول (`A_MAJORITY_LAW_IS_STRONGER_THAN_A_FALSIFIED_TOTAL_ONE`).

**وثانيًا: التوقيعاتُ الثلاثُ تُودَع بما تُغيِّره لا بما تُزيِّنه.** «الحنجرةُ
ثلاثُ حالات» ليست تصحيحًا في هامش: إن كان الاهتزازُ صائتًا، والانفتاحُ بلا
اهتزازٍ صامتًا مهموسًا، والانغلاقُ التامُّ همزةً — فالعملياتُ الثلاثُ عملُ
**عضوٍ واحد**، والقطعُ حينئذٍ `NATIVE_TO_THE_STREAM` لا حدٌّ يُفرَض عليه من
خارج. و«الصوائتُ مجهورة» يُخرِج «بلا حاجز» من الحنجرة إلى الفم. و«غالبٌ لا
تام» هو التوقيعُ الذي يمنع الصفَّين السابقَين أن يصيرا دعوى تمام. والثلاثةُ
تُودَع تواقيعَ على الدعوى، **لا قياساتٍ على بايتة**
(`A_SIGNATURE_IS_A_COMMITMENT_NOT_A_MEASUREMENT`).

**وثالثًا: الشرطُ الثاني أُجري ههنا على بايتاتنا، فوافق في الداخل وخالف في
الطرف.** يُقاس في هذه الوحدة — من `corpora/quran-simple-enhanced.txt` عبر
الباب المختوم وحدَه — توزيعُ الحركات الثلاث **داخلَ اللفظ** و**عند خاتمته**،
بمفتاحَي خاتمةٍ مُعلَنَين لا بمفتاحٍ واحد. والمقيسُ اليوم:

| المفتاح | الموضع | فتحة | كسرة | ضمّة | H | سكون+تنوين |
|---|---|---|---|---|---|---|
| آخرُ حرفٍ | داخل اللفظ | 60.8% | 22.1% | 17.1% | 1.3535 | 10.53% |
| آخرُ حرفٍ | خاتمةُ اللفظ | 51.8% | 25.4% | 22.8% | 1.4805 | 21.38% |
| آخرُ مشكولٍ | داخل اللفظ | 61.0% | 22.3% | 16.7% | 1.3486 | 10.27% |
| آخرُ مشكولٍ | خاتمةُ اللفظ | 54.9% | 23.5% | 21.7% | 1.4441 | 22.90% |

فالاتّجاهُ الذي ادُّعي **يثبت على المفتاحين معًا**: الفتحةُ تنهار تسعَ نقاطٍ
على مفتاح آخرِ حرفٍ وستًّا على مفتاح آخرِ مشكول، والإنتروبيا ترتفع 0.127 بتٍّ
على الأوّل و0.096 على الثاني — ترتفع عند الطرف لا تنخفض. فليست الخاتمةُ موضعَ
الراحة. وأمّا المقاديرُ المنقولة فتُقابَل رقمًا رقمًا بحدِّ تسامحٍ مُعلَنٍ قبل
المقابلة (نقطةٌ مئويّةٌ في الحصص، وعُشرُ عُشرِ البتّ في الإنتروبيا)، فيقع
الجوابُ منقسمًا انقسامًا حادًّا: **مقابلاتُ الداخل توافق كلُّها — ثمانٍ من
ثمانٍ على المفتاحين** — و**مقابلاتُ الطرف تخالف تسعًا من عشر**، ولا يوافق منها
إلّا كسرةُ الطرف على مفتاح آخرِ حرف. و«29.0% سكونًا وتنوينًا عند الطرف» تخالف
بفارقٍ يقارب ربعَ قيمته على المفتاحين. وهذا متوقَّعٌ لا
مستنكَر: تلك الأرقامُ قِيست على `mujammad.txt` — 1,306,770 بايتًا — وبايتاتُنا
1,319,901، وقد سُجِّل فرقُ 13,131 بايتًا في `hamil_phase1_audit_deposit`. فما
قِيس في مقامٍ آخر لا يعبر إلى مقامنا، ويُسجَّل اتّفاقُ **الاتّجاه** حيث ثبت،
ولا يُلطَّف اختلافُ **المقدار** حيث وقع
(`A_DIRECTION_THAT_HOLDS_IS_NOT_A_MAGNITUDE_THAT_MATCHES`).

**ورابعًا: مقامُ الخاتمة اختيارٌ، والاختيارُ يُحرِّك الرقمَ.** التنوينُ في هذا
الرسم يقع مرّةً على الألف الأخيرة (`مَرَضاً`) ومرّةً على ما قبلها (`هُدًى`)،
فمفتاحُ «آخرِ حرف» يُسقط ثمانيةَ آلافٍ وثمانمئةٍ من تنوينات الطرف إلى الداخل،
ومفتاحُ «آخرِ مشكولٍ» يُبقيها. فلا يُنشَر ههنا رقمٌ مفردٌ للخاتمة بل **المفتاحان
معًا وفرقُهما**، على سنّة `ending_release_deposit`
(`AN_ENDING_KEY_IS_A_CHOICE_AND_ITS_LADDER_TRAVELS_WITH_THE_FIGURE`).

**وخامسًا: وسقط من الطريق مقامٌ منقولٌ في موضعه.** مقامُ «الموضع الأوّل»
المُودَع في `position_haraka_bit_account` نقلًا عن جدولٍ خارجيّ — 78,215 — هو
بعينه عددُ الكلمات الحاملة علامةً واحدةً فأكثرَ في بايتاتنا المختومة، يُعاد
اشتقاقُه ههنا بتنفيذٍ مستقلٍّ عن ذاك الجدول. وهذا **تقاطعُ تنفيذين** لا اتّساقٌ
داخليّ، وهو الجنسُ الوحيدُ ههنا الذي يستحقّ الاسم. ولا يُقرأ منه أنّ الجدولَين
يتقاسمان مجتمعًا: 78,076 مقامُ الموضع الأخير هناك، وبينه وبين هذا 139 كلمةً
مُخرَجةً مُعلَنةً عندهم (`ONLY_A_SECOND_IMPLEMENTATION_MAKES_A_CROSS_CHECK_HERE`).

**وسادسًا: الشرطُ الأوّل موقوفٌ، ووقفُه يُسمّى بما يَقف عليه.** «هل تنفصل
الحروفُ كلُّها؟» أجابت عنه بصمةُ `letter_fingerprint.py` في مستودع Algebra:
أربعةُ أبعادٍ، بعدان مقيسان وبعدان مكتوبان يدًا، والزوجُ (د، ق) **متصادمٌ
بنيويًّا**، والتفرُّدُ 28/29 **بلا خطِّ صفر**. ولا بايتةَ من ذلك الملفّ في هذه
الشجرة، فمنزلتُه ههنا `NOT_CHECKABLE_HERE` لا `AGREES` ولا `CONTRADICTS`؛
ويُودَع الزوجُ المُعلَنُ بنصّه كما أُعلِن. ورفعُ هذا الوقف واحدٌ لا اثنان:
إيداعُ بايتاتٍ عبر البوّابة، ثمّ إعادةُ التفرُّد **مع خطِّ صفرٍ** قبل أن يُقرأ
28/29 رقمًا (`A_UNIQUENESS_WITHOUT_A_ZERO_LINE_IS_A_NUMBER_WITHOUT_A_SCALE`).

**وسابعًا: الكسورُ أربعةٌ، ولكلٍّ موضعٌ ومصدر.** كسرٌ عند الكلمة مقيسٌ ههنا
(الخاتمةُ أعلى إنتروبيا لا أقلّ)، وكسرٌ عند الحرف منقولٌ موقوف (البصمةُ بلا خطِّ
صفر)، وكسرٌ عند التتابع مقيسٌ في هذه الشجرة في وحدةٍ أخرى (مربّعُ الاستقراء لا
ينغلق في `markov_order_induction`)، وكسرٌ عند الحقل 112 معلَنٌ عندهم موقوفٌ
عندنا على بايتاتٍ لم تُودَع كما سُجِّل في `hamil_round_two_preregistration`.
فليس في الأربعة كسرٌ يُذكَر بلا موضع، ولا موضعٌ يُذكَر بلا جنسِ دليل.

**خمولٌ سلطويّ**: لا ولادةَ هنا ولا حكمَ ولادةٍ ولا تجميدَ `E0`، ولا استيرادَ
من `kernel/` ولا من `program/`، ولا بوّابةَ في هذا المستودع تقرأ هذا الإيداع،
ولا تزحزح هذه الوحدةُ بوّابةَ ماركوف عمّا كانت عليه — وكلُّ ما يُقاس ههنا
إنتروبيا هامشيّةٌ لموضعٍ داخلَ الكلمة، لا انتروبيا شرطيّةٌ على توكناتٍ متجاورة.
"""

from __future__ import annotations

import math
import unicodedata
from dataclasses import dataclass, fields
from enum import Enum
from functools import lru_cache
from typing import Final

from .markov_readiness_gate import ChainReading, token_markov_standing
from .quran_corpus_word_total import read_quran_corpus_bytes

__all__ = [
    "AN_ENDING_KEY_IS_A_CHOICE_AND_ITS_LADDER_TRAVELS_WITH_THE_FIGURE",
    "A_DIRECTION_THAT_HOLDS_IS_NOT_A_MAGNITUDE_THAT_MATCHES",
    "A_MAJORITY_LAW_IS_STRONGER_THAN_A_FALSIFIED_TOTAL_ONE",
    "A_SIGNATURE_IS_A_COMMITMENT_NOT_A_MEASUREMENT",
    "A_UNIQUENESS_WITHOUT_A_ZERO_LINE_IS_A_NUMBER_WITHOUT_A_SCALE",
    "FRACTAL_MAJORITY_LAW_NAMED_RESIDUALS",
    "ONLY_A_SECOND_IMPLEMENTATION_MAKES_A_CROSS_CHECK_HERE",
    "THE_ENDING_SHAPE_AS_TRANSCRIBED",
    "THE_FIRST_CONDITION",
    "THE_FOUR_BREAKS",
    "THE_LEVELS",
    "THE_QUOTED_ENDING_SHAPE",
    "THE_QUOTED_ENDING_SUKUN_AND_TANWIN",
    "THE_QUOTED_FIRST_POSITION_DENOMINATOR",
    "THE_SECOND_CONDITION",
    "THE_SHARE_TOLERANCE",
    "THE_THREE_SIGNATURES",
    "THE_ENTROPY_TOLERANCE",
    "BreakGenus",
    "ConditionStanding",
    "EndingKey",
    "FractalMajorityLawError",
    "KeyReading",
    "LevelRow",
    "LevelStanding",
    "NamedBreak",
    "PositionCensus",
    "QuotedRow",
    "Signature",
    "SlotClass",
    "StandingCondition",
    "TranscribedRow",
    "Verdict",
    "measured_rows",
    "measured_share_of_the_table",
    "reading_for",
    "the_corpus_gate_is_untouched",
    "the_direction_holds_on_every_key",
    "the_marked_word_count",
    "the_measured_ladder",
    "the_transcription_verdicts",
    "transcribed_rows_from_disk",
]


class FractalMajorityLawError(ValueError):
    """رُفض مدخلٌ خارج مفردات هذا الإيداع؛ ولا يُحمَل على أقرب حالة."""


# ---------------------------------------------------------------------------
# العلاماتُ وقاعدةُ التصنيف، مُعلَنةً قبل أن يُقرأ رقم
# ---------------------------------------------------------------------------


THE_ARABIC_COMBINING_MARKS: Final[frozenset[str]] = frozenset(
    chr(codepoint)
    for codepoint in range(0x0600, 0x0700)
    if unicodedata.category(chr(codepoint)) == "Mn"
)
"""علاماتُ الكتلة العربيّة غيرُ المتباعدة؛ تُشتقّ من قاعدة يونيكود لا تُسرَد."""

THE_FATHA: Final[str] = "\u064e"
THE_KASRA: Final[str] = "\u0650"
THE_DAMMA: Final[str] = "\u064f"
THE_SUKUN: Final[str] = "\u0652"
THE_TANWIN: Final[frozenset[str]] = frozenset({"\u064b", "\u064c", "\u064d"})

THE_THREE_SHORT_VOWELS: Final[tuple[str, str, str]] = (
    THE_FATHA,
    THE_KASRA,
    THE_DAMMA,
)


class SlotClass(Enum):
    """صنفُ الخانة: حركةٌ قصيرةٌ، أو تنوينٌ، أو سكونٌ، أو خلوٌّ من العلامة."""

    FATHA = "فتحة"
    KASRA = "كسرة"
    DAMMA = "ضمّة"
    TANWIN = "تنوين"
    SUKUN = "سكون"
    UNMARKED = "بلا_علامة"


_THE_PRECEDENCE: Final[str] = (
    "حركةٌ قصيرةٌ ثمّ تنوينٌ ثمّ سكون؛ والشدّةُ لا تُصنِّف خانةً وحدَها، "
    "وخلوُّ الخانة من هذه الثلاثة يجعلها `UNMARKED` لا سكونًا مقدَّرًا"
)


class EndingKey(Enum):
    """مفتاحُ الخاتمة: أيُّ خانةٍ في الكلمة تُعَدّ خاتمتَها؟"""

    LAST_BASE_SLOT = "آخرُ_حرفٍ_في_الكلمة"
    """الخاتمةُ خانةُ آخرِ حرفٍ مرسوم، مشكولًا كان أو خاليًا."""

    LAST_MARKED_SLOT = "آخرُ_خانةٍ_مشكولةٍ_في_الكلمة"
    """الخاتمةُ آخرُ خانةٍ تحمل صنفًا؛ وكلمةٌ بلا علامةٍ أصلًا لا خاتمةَ لها."""


# ---------------------------------------------------------------------------
# القراءةُ من البايتات المختومة
# ---------------------------------------------------------------------------


def _slot_classes(word: str) -> tuple[SlotClass, ...]:
    """خاناتُ الكلمة: حرفٌ مرسومٌ وما يليه من علامات، مصنَّفةً بالسبق المُعلَن."""

    slots: list[list[str]] = []
    for character in word:
        if character in THE_ARABIC_COMBINING_MARKS:
            if slots:
                slots[-1].append(character)
        else:
            slots.append([])
    return tuple(_classify(marks) for marks in slots)


def _classify(marks: list[str]) -> SlotClass:
    for mark in marks:
        if mark == THE_FATHA:
            return SlotClass.FATHA
        if mark == THE_KASRA:
            return SlotClass.KASRA
        if mark == THE_DAMMA:
            return SlotClass.DAMMA
    for mark in marks:
        if mark in THE_TANWIN:
            return SlotClass.TANWIN
    for mark in marks:
        if mark == THE_SUKUN:
            return SlotClass.SUKUN
    return SlotClass.UNMARKED


@dataclass(frozen=True, slots=True)
class PositionCensus:
    """إحصاءُ موضعٍ واحدٍ: أعدادٌ خام، وكلُّ نسبةٍ فوقها مُشتَقّةٌ عند القراءة."""

    where: str
    counts: tuple[tuple[SlotClass, int], ...]

    def __post_init__(self) -> None:
        if not self.where.strip():
            raise FractalMajorityLawError("موضعُ الإحصاء لا يكون فارغًا.")
        seen = [member for member, _ in self.counts]
        if sorted(seen, key=lambda member: member.name) != sorted(
            SlotClass, key=lambda member: member.name
        ):
            raise FractalMajorityLawError(
                "إحصاءُ الموضع يذكر أصنافَ `SlotClass` كلَّها مرّةً مرّةً."
            )
        if any(count < 0 for _, count in self.counts):
            raise FractalMajorityLawError("عددٌ دون الصفر لا يُودَع.")

    @property
    def as_mapping(self) -> dict[SlotClass, int]:
        return dict(self.counts)

    @property
    def total_slots(self) -> int:
        return sum(count for _, count in self.counts)

    @property
    def three_vowel_total(self) -> int:
        mapping = self.as_mapping
        return (
            mapping[SlotClass.FATHA]
            + mapping[SlotClass.KASRA]
            + mapping[SlotClass.DAMMA]
        )

    @property
    def three_vowel_shares(self) -> tuple[float, float, float]:
        """حصصُ الفتحة والكسرة والضمّة من مجموعها وحدَه، لا من الخانات كلِّها."""

        total = self.three_vowel_total
        if total == 0:
            raise FractalMajorityLawError("لا حصّةَ على مقامٍ صفر.")
        mapping = self.as_mapping
        return (
            mapping[SlotClass.FATHA] / total,
            mapping[SlotClass.KASRA] / total,
            mapping[SlotClass.DAMMA] / total,
        )

    @property
    def three_vowel_entropy(self) -> float:
        """إنتروبيا الحركات الثلاث بالبتّ؛ هامشيّةٌ لا شرطيّةٌ على جوارٍ."""

        return -sum(
            share * math.log2(share) for share in self.three_vowel_shares if share > 0.0
        )

    @property
    def sukun_and_tanwin_share(self) -> float:
        """حصّةُ «الساكن عند الطرف» بمعناها الواسع: سكونٌ وتنوينٌ من كلّ الخانات."""

        total = self.total_slots
        if total == 0:
            raise FractalMajorityLawError("لا حصّةَ على مقامٍ صفر.")
        mapping = self.as_mapping
        return (mapping[SlotClass.SUKUN] + mapping[SlotClass.TANWIN]) / total


@dataclass(frozen=True, slots=True)
class KeyReading:
    """قراءةُ مفتاحٍ واحد: داخلُ اللفظ وخاتمتُه، مقيسَين على البايتات نفسِها."""

    key: EndingKey
    interior: PositionCensus
    ending: PositionCensus

    @property
    def fatha_collapse(self) -> float:
        """هبوطُ الفتحة من الداخل إلى الطرف، بالنقاط المئويّة."""

        return self.interior.three_vowel_shares[0] - self.ending.three_vowel_shares[0]

    @property
    def entropy_rise(self) -> float:
        """ارتفاعُ الإنتروبيا من الداخل إلى الطرف؛ موجبٌ يعني أنّ الطرف أغزر."""

        return self.ending.three_vowel_entropy - self.interior.three_vowel_entropy


def _corpus_words() -> tuple[str, ...]:
    text = read_quran_corpus_bytes().decode("utf-8")
    return tuple(text.split())


@lru_cache(maxsize=1)
def the_measured_ladder() -> tuple[KeyReading, ...]:
    """سُلَّمُ المفتاحين، مقيسًا من البايتات المختومة عند كلّ طلبٍ أوّل."""

    words = _corpus_words()
    readings: list[KeyReading] = []
    for key in EndingKey:
        interior: dict[SlotClass, int] = {member: 0 for member in SlotClass}
        ending: dict[SlotClass, int] = {member: 0 for member in SlotClass}
        for word in words:
            classes = _slot_classes(word)
            if not classes:
                continue
            ending_index = _ending_index(classes, key)
            for index, slot in enumerate(classes):
                target = ending if index == ending_index else interior
                target[slot] += 1
        readings.append(
            KeyReading(
                key=key,
                interior=PositionCensus("داخل اللفظ", tuple(interior.items())),
                ending=PositionCensus("خاتمة اللفظ", tuple(ending.items())),
            )
        )
    return tuple(readings)


def _ending_index(classes: tuple[SlotClass, ...], key: EndingKey) -> int | None:
    if key is EndingKey.LAST_BASE_SLOT:
        return len(classes) - 1
    marked = [
        index for index, slot in enumerate(classes) if slot is not SlotClass.UNMARKED
    ]
    return marked[-1] if marked else None


def reading_for(key: EndingKey) -> KeyReading:
    """قراءةُ مفتاحٍ بعينه من السُّلَّم المقيس."""

    for reading in the_measured_ladder():
        if reading.key is key:
            return reading
    raise FractalMajorityLawError("مفتاحٌ خارج `EndingKey` لا قراءةَ له.")


def the_direction_holds_on_every_key() -> bool:
    """أتنهار الفتحةُ وترتفع الإنتروبيا عند الطرف على المفتاحين معًا؟"""

    return all(
        reading.fatha_collapse > 0.0 and reading.entropy_rise > 0.0
        for reading in the_measured_ladder()
    )


@lru_cache(maxsize=1)
def the_marked_word_count() -> int:
    """عددُ الكلمات الحاملة علامةً واحدةً فأكثرَ في البايتات المختومة."""

    return sum(
        1
        for word in _corpus_words()
        if any(character in THE_ARABIC_COMBINING_MARKS for character in word)
    )


THE_QUOTED_FIRST_POSITION_DENOMINATOR: Final[int] = 78215
"""مقامُ «الموضع الأوّل» كما نُقل في `position_haraka_bit_account` عن جدولٍ خارجيّ."""


# ---------------------------------------------------------------------------
# المنقولُ من المحادثة، وحدُّ التسامح مُعلَنٌ قبل المقابلة
# ---------------------------------------------------------------------------


THE_SHARE_TOLERANCE: Final[float] = 0.010
"""حدُّ التسامح في الحصص: نقطةٌ مئويّةٌ واحدة، مُعلَنةً قبل أن يُقابَل رقم."""

THE_ENTROPY_TOLERANCE: Final[float] = 0.010
"""حدُّ التسامح في الإنتروبيا: عُشرُ عُشرِ البتّ، مُعلَنًا قبل المقابلة."""


@dataclass(frozen=True, slots=True)
class QuotedRow:
    """صفٌّ منقولٌ من المحادثة: حصصٌ وإنتروبيا، بلا حكمٍ مكتوبٍ في حقل."""

    where: str
    fatha: float
    kasra: float
    damma: float
    entropy: float

    def __post_init__(self) -> None:
        shares = (self.fatha, self.kasra, self.damma)
        if any(not 0.0 < share < 1.0 for share in shares):
            raise FractalMajorityLawError("حصّةٌ منقولةٌ خارج المجال لا تُودَع.")
        if abs(sum(shares) - 1.0) > 0.002:
            raise FractalMajorityLawError("حصصُ الصفّ المنقول لا تجمع الواحد.")
        if self.entropy <= 0.0:
            raise FractalMajorityLawError("إنتروبيا منقولةٌ غيرُ موجبةٍ لا تُودَع.")


THE_QUOTED_ENDING_SHAPE: Final[tuple[QuotedRow, QuotedRow]] = (
    QuotedRow("داخل اللفظ", 0.612, 0.219, 0.170, 1.348),
    QuotedRow("خاتمة اللفظ", 0.498, 0.262, 0.239, 1.501),
)
"""جدولُ الشرط الثاني كما ورد في المحادثة؛ منقولٌ لا مقيسٌ ههنا."""

THE_QUOTED_ENDING_SUKUN_AND_TANWIN: Final[float] = 0.290
"""«سكون+تنوين عند الخاتمة = 29.0%» كما ورد؛ منقولٌ يُقابَل بما يقيسه القرص."""


class Verdict(Enum):
    """حكمُ المقابلة؛ يُشتَقّ من الحساب ولا يُكتَب في حقل."""

    AGREES = "تطابق"
    CONTRADICTS = "تخالف"
    NOT_CHECKABLE_HERE = "غيرُ_قابلٍ_للفحص_ههنا"


@dataclass(frozen=True, slots=True)
class Comparison:
    """مقابلةُ رقمٍ منقولٍ برقمٍ مقيس؛ والحكمُ صفةٌ مشتقّةٌ لا حقلٌ مكتوب."""

    name: str
    key: EndingKey
    quoted: float
    measured: float
    tolerance: float

    def __post_init__(self) -> None:
        if self.tolerance <= 0.0:
            raise FractalMajorityLawError("حدُّ تسامحٍ غيرُ موجبٍ يُصيِّر كلَّ شيءٍ موافقًا.")

    @property
    def gap(self) -> float:
        return abs(self.quoted - self.measured)

    @property
    def verdict(self) -> Verdict:
        return Verdict.AGREES if self.gap <= self.tolerance else Verdict.CONTRADICTS


def the_transcription_verdicts() -> tuple[Comparison, ...]:
    """مقابلةُ المنقول بالمقيس على المفتاحين؛ يُعاد حسابُها عند كلّ طلب."""

    comparisons: list[Comparison] = []
    for reading in the_measured_ladder():
        for quoted, census in (
            (THE_QUOTED_ENDING_SHAPE[0], reading.interior),
            (THE_QUOTED_ENDING_SHAPE[1], reading.ending),
        ):
            measured_shares = census.three_vowel_shares
            for label, quoted_share, measured_share in zip(
                ("فتحة", "كسرة", "ضمّة"),
                (quoted.fatha, quoted.kasra, quoted.damma),
                measured_shares,
            ):
                comparisons.append(
                    Comparison(
                        name=f"{quoted.where} — {label}",
                        key=reading.key,
                        quoted=quoted_share,
                        measured=measured_share,
                        tolerance=THE_SHARE_TOLERANCE,
                    )
                )
            comparisons.append(
                Comparison(
                    name=f"{quoted.where} — H",
                    key=reading.key,
                    quoted=quoted.entropy,
                    measured=census.three_vowel_entropy,
                    tolerance=THE_ENTROPY_TOLERANCE,
                )
            )
        comparisons.append(
            Comparison(
                name="خاتمة اللفظ — سكون+تنوين",
                key=reading.key,
                quoted=THE_QUOTED_ENDING_SUKUN_AND_TANWIN,
                measured=reading.ending.sukun_and_tanwin_share,
                tolerance=THE_SHARE_TOLERANCE,
            )
        )
    return tuple(comparisons)


@dataclass(frozen=True, slots=True)
class TranscribedRow:
    """صفُّ الجدول كما كُتب في نثر هذه الوحدة، ليُقابَل بما يقيسه القرص."""

    key: EndingKey
    where: str
    fatha: float
    kasra: float
    damma: float
    entropy: float
    sukun_and_tanwin: float


THE_ENDING_SHAPE_AS_TRANSCRIBED: Final[tuple[TranscribedRow, ...]] = (
    TranscribedRow(
        EndingKey.LAST_BASE_SLOT, "داخل اللفظ", 0.608, 0.221, 0.171, 1.3535, 0.1053
    ),
    TranscribedRow(
        EndingKey.LAST_BASE_SLOT, "خاتمة اللفظ", 0.518, 0.254, 0.228, 1.4805, 0.2138
    ),
    TranscribedRow(
        EndingKey.LAST_MARKED_SLOT, "داخل اللفظ", 0.610, 0.223, 0.167, 1.3486, 0.1027
    ),
    TranscribedRow(
        EndingKey.LAST_MARKED_SLOT, "خاتمة اللفظ", 0.549, 0.235, 0.217, 1.4441, 0.2290
    ),
)
"""أرقامُ جدول النثر أعلاه، مجمَّدةً لتُقابَل بالقرص لا لتُصدَّق."""


def transcribed_rows_from_disk() -> tuple[TranscribedRow, ...]:
    """الصفوفُ نفسُها مولَّدةً من القياس، بتقريب النثر لا بتقريبٍ آخر."""

    rows: list[TranscribedRow] = []
    for reading in the_measured_ladder():
        for census in (reading.interior, reading.ending):
            fatha, kasra, damma = census.three_vowel_shares
            rows.append(
                TranscribedRow(
                    key=reading.key,
                    where=census.where,
                    fatha=round(fatha, 3),
                    kasra=round(kasra, 3),
                    damma=round(damma, 3),
                    entropy=round(census.three_vowel_entropy, 4),
                    sukun_and_tanwin=round(census.sukun_and_tanwin_share, 4),
                )
            )
    return tuple(rows)


# ---------------------------------------------------------------------------
# الجدولُ الفراكتاليُّ: مستوياتٌ ومنازل
# ---------------------------------------------------------------------------


class LevelStanding(Enum):
    """منزلةُ صفٍّ في الجدول: بأيّ جنسٍ من الدليل يقف؟"""

    MEASURED_IN_THIS_UNIT = "مقيسٌ_في_هذه_الوحدة"
    MEASURED_ELSEWHERE_IN_THIS_TREE = "مقيسٌ_في_وحدةٍ_أخرى_من_هذه_الشجرة"
    QUOTED_FROM_THE_SIBLING_PROGRAM = "منقولٌ_من_البرنامج_الشقيق"
    ASSERTED_AND_NOT_MEASURED = "مُدَّعًى_ولم_يُقَس"


@dataclass(frozen=True, slots=True)
class LevelRow:
    """صفُّ مستوًى: العمليات الثلاث كما تظهر فيه، ومنزلتُه، وموضعُ سنده."""

    level: str
    joining: str
    cutting: str
    recomposition: str
    standing: LevelStanding
    where: str

    def __post_init__(self) -> None:
        for value, what in (
            (self.level, "اسمُ المستوى"),
            (self.joining, "الوصلُ في المستوى"),
            (self.cutting, "القطعُ في المستوى"),
            (self.recomposition, "إعادةُ التركيب في المستوى"),
            (self.where, "موضعُ السند"),
        ):
            if not value.strip():
                raise FractalMajorityLawError(f"{what} لا يكون فارغًا.")
        if not isinstance(self.standing, LevelStanding):
            raise FractalMajorityLawError("منزلةُ الصفّ عضوٌ في `LevelStanding`.")


THE_LEVELS: Final[tuple[LevelRow, ...]] = (
    LevelRow(
        level="الحنجرة",
        joining="اهتزازٌ متّصل",
        cutting="انغلاقٌ تامّ (الهمزة)",
        recomposition="انفتاحٌ بلا اهتزازٍ يُعيد تشكيل التيار",
        standing=LevelStanding.ASSERTED_AND_NOT_MEASURED,
        where="توقيعُ «الحنجرة ثلاثُ حالات»؛ دعوًى تشريحيّةٌ لا بايتة تحتها ههنا",
    ),
    LevelRow(
        level="الخانة (حرفٌ وحركتُه)",
        joining="حركةٌ تصل الحاملَ بما بعده",
        cutting="سكونٌ يقطع",
        recomposition="تنوينٌ وشدّةٌ يُعيدان تركيب الخانة",
        standing=LevelStanding.MEASURED_IN_THIS_UNIT,
        where="`the_measured_ladder` على البايتات المختومة",
    ),
    LevelRow(
        level="الكلمة",
        joining="خاتمةٌ موصولةٌ تحمل الهيئة",
        cutting="وقفٌ عند الطرف: سكونٌ أو تنوين",
        recomposition="الخاتمةُ تُعيد نسبةَ الكلمة إلى ما حولها",
        standing=LevelStanding.MEASURED_IN_THIS_UNIT,
        where="`the_transcription_verdicts` ومعها كسرُ «الخاتمةُ ليست راحة»",
    ),
    LevelRow(
        level="التتابع",
        joining="تجاورٌ يُقيَّد بدرجةٍ في سُلَّم ماركوف",
        cutting="حدُّ الجذر",
        recomposition="صعودُ السُّلَّم درجةً فدرجة",
        standing=LevelStanding.MEASURED_ELSEWHERE_IN_THIS_TREE,
        where="`markov_order_induction`؛ والمربّعُ لا ينغلق ثَمّ",
    ),
    LevelRow(
        level="الحرف",
        joining="أبعادٌ تجمع الحروفَ في خاناتٍ مشتركة",
        cutting="بُعدٌ يفصل حرفًا عن حرف",
        recomposition="إعادةُ التفرُّد ببُعدٍ زائد",
        standing=LevelStanding.QUOTED_FROM_THE_SIBLING_PROGRAM,
        where="`letter_fingerprint.py` في Algebra؛ لا بايتةَ منه ههنا",
    ),
    LevelRow(
        level="الحقل 112",
        joining="وصلٌ في ثنائيّة الوقف/الوصل",
        cutting="وقفٌ في الثنائيّة نفسِها",
        recomposition="استثناءاتٌ معجميّةٌ مسمّاة",
        standing=LevelStanding.QUOTED_FROM_THE_SIBLING_PROGRAM,
        where="`hamil_round_two_preregistration`؛ موقوفٌ على بايتاتٍ لم تُودَع",
    ),
)
"""صفوفُ الجدول الفراكتاليّ؛ ولا صفَّ بلا منزلةٍ وموضعِ سند."""


def measured_rows() -> tuple[LevelRow, ...]:
    """الصفوفُ التي تقف على بايتاتٍ في هذه الشجرة، لا على نقلٍ ولا على دعوى."""

    return tuple(
        row
        for row in THE_LEVELS
        if row.standing
        in (
            LevelStanding.MEASURED_IN_THIS_UNIT,
            LevelStanding.MEASURED_ELSEWHERE_IN_THIS_TREE,
        )
    )


def measured_share_of_the_table() -> float:
    """حصّةُ الصفوف المقيسة من صفوف الجدول؛ مُشتَقّةٌ لا مكتوبة."""

    return len(measured_rows()) / len(THE_LEVELS)


# ---------------------------------------------------------------------------
# الكسورُ الأربعة، مسمّاةً بمواضعها
# ---------------------------------------------------------------------------


class BreakGenus(Enum):
    """جنسُ الكسر: بأيّ دليلٍ عُرِف موضعُ كسره؟"""

    MEASURED_ON_OUR_SEALED_BYTES = "مقيسٌ_على_بايتاتنا_المختومة"
    MEASURED_IN_ANOTHER_UNIT_HERE = "مقيسٌ_في_وحدةٍ_أخرى_ههنا"
    DECLARED_BY_THE_SIBLING_AND_BLOCKED_HERE = "معلَنٌ_عندهم_موقوفٌ_عندنا"


@dataclass(frozen=True, slots=True)
class NamedBreak:
    """كسرٌ مسمًّى: أين انكسر القانون، وبأيّ دليل، وما الذي بقي غالبًا."""

    name: str
    level: str
    where_it_breaks: str
    genus: BreakGenus
    source: str

    def __post_init__(self) -> None:
        for value, what in (
            (self.name, "اسمُ الكسر"),
            (self.level, "مستوى الكسر"),
            (self.where_it_breaks, "موضعُ الكسر"),
            (self.source, "مصدرُ الكسر"),
        ):
            if not value.strip():
                raise FractalMajorityLawError(f"{what} لا يكون فارغًا.")
        if not isinstance(self.genus, BreakGenus):
            raise FractalMajorityLawError("جنسُ الكسر عضوٌ في `BreakGenus`.")


THE_FOUR_BREAKS: Final[tuple[NamedBreak, ...]] = (
    NamedBreak(
        name="الخاتمةُ ليست موضعَ الراحة",
        level="الكلمة",
        where_it_breaks=(
            "يُتوقَّع أن يهدأ التيارُ عند الطرف، والمقيسُ أنّ الإنتروبيا ترتفع "
            "عنده على المفتاحين معًا وأنّ الفتحةَ تنهار"
        ),
        genus=BreakGenus.MEASURED_ON_OUR_SEALED_BYTES,
        source="`the_measured_ladder` في هذه الوحدة",
    ),
    NamedBreak(
        name="البصمةُ بلا خطِّ صفر",
        level="الحرف",
        where_it_breaks=(
            "لا تنفصل الحروفُ كلُّها: الزوجُ (د، ق) متصادمٌ بنيويًّا، والتفرُّدُ "
            "28/29 رقمٌ بلا مقياسٍ ما لم يُعَد مع خطِّ صفر"
        ),
        genus=BreakGenus.DECLARED_BY_THE_SIBLING_AND_BLOCKED_HERE,
        source="`letter_fingerprint.py` في مستودع Algebra؛ لا بايتةَ منه ههنا",
    ),
    NamedBreak(
        name="مربّعُ الاستقراء لا ينغلق",
        level="التتابع",
        where_it_breaks=(
            "الدرجةُ تتحرّك بتحرُّك ترتيب الاستقراء: الكلُّ سلسلةٌ، والنصفُ "
            "المرئيُّ استقلالٌ، والمحجوبُ مثلّث"
        ),
        genus=BreakGenus.MEASURED_IN_ANOTHER_UNIT_HERE,
        source="`markov_order_induction` في هذه الشجرة",
    ),
    NamedBreak(
        name="ثنائيّةُ الحقل 112 غالبةٌ لا تامّة",
        level="الحقل 112",
        where_it_breaks=(
            "الوقف/الوصل يغلب ولا يعمّ، والاستثناءاتُ معجميّةٌ مسمّاةٌ عندهم؛ "
            "وبايتاتُها لم تُودَع ههنا فلا تُقاس"
        ),
        genus=BreakGenus.DECLARED_BY_THE_SIBLING_AND_BLOCKED_HERE,
        source="`hamil_round_two_preregistration`: `FIELD_112_LAWS` موقوفة",
    ),
)
"""الكسورُ الأربعة؛ ولا يُزاد فيها كسرٌ بلا موضعٍ ولا يُطوى منها كسرٌ بتلطيف."""


# ---------------------------------------------------------------------------
# التوقيعاتُ الثلاث
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Signature:
    """توقيعٌ على الدعوى: ما يقوله، وما يُغيِّره، وأنّه ليس قياسًا."""

    name: str
    what_it_says: str
    what_it_changes: str

    def __post_init__(self) -> None:
        for value, what in (
            (self.name, "اسمُ التوقيع"),
            (self.what_it_says, "نصُّ التوقيع"),
            (self.what_it_changes, "ما يُغيِّره التوقيع"),
        ):
            if not value.strip():
                raise FractalMajorityLawError(f"{what} لا يكون فارغًا.")


THE_THREE_SIGNATURES: Final[tuple[Signature, ...]] = (
    Signature(
        name="الحنجرةُ ثلاثُ حالات",
        what_it_says=(
            "الاهتزازُ صائتٌ، والانفتاحُ بلا اهتزازٍ صامتٌ مهموس، والانغلاقُ " "التامُّ همزة"
        ),
        what_it_changes=(
            "العملياتُ الثلاثُ عملُ عضوٍ واحدٍ لا عملُ آلة النطق كلِّها، فالقطعُ "
            "أصيلٌ في التيار لا حدٌّ يُفرَض عليه من خارج"
        ),
    ),
    Signature(
        name="الصوائتُ مجهورة",
        what_it_says="الجهرُ صفةُ الصائت، و«بلا حاجز» وصفٌ فمويٌّ لا حنجريّ",
        what_it_changes=(
            "يُنقَل شرطُ «بلا حاجز» من الحنجرة إلى الفم، فلا يُخلَط موضعُ "
            "الاهتزاز بموضع المرور"
        ),
    ),
    Signature(
        name="غالبٌ لا تام",
        what_it_says="التكرارُ الفراكتاليُّ قانونُ غالبٍ تُعلَن كسورُه",
        what_it_changes=(
            "يمنع التوقيعَين قبله أن يصيرا دعوى تمام، ويُلزِم كلَّ كسرٍ أن "
            "يُذكَر بموضعه لا أن يُطوى في حاشية"
        ),
    ),
)
"""توقيعاتُ صاحب الدعوى الثلاثة؛ التزاماتٌ تُودَع، لا أرقامٌ تُقاس."""


# ---------------------------------------------------------------------------
# الشرطان، مُقيَّدَين بمصدريهما
# ---------------------------------------------------------------------------


class ConditionStanding(Enum):
    """منزلةُ الشرط: أُجري على بايتاتنا، أم وقف على بايتاتٍ ليست عندنا؟"""

    RUN_ON_OUR_SEALED_BYTES = "أُجري_على_بايتاتنا_المختومة"
    BLOCKED_ON_BYTES_NOT_DEPOSITED_HERE = "موقوفٌ_على_بايتاتٍ_لم_تُودَع_ههنا"


@dataclass(frozen=True, slots=True)
class StandingCondition:
    """شرطُ قياسٍ مُقيَّدٌ بمصدره؛ ولا يُقرأ خارجَ مصدره ولو وافق."""

    question: str
    standing: ConditionStanding
    bound_to: str
    reading: str

    def __post_init__(self) -> None:
        for value, what in (
            (self.question, "سؤالُ الشرط"),
            (self.bound_to, "مصدرُ الشرط"),
            (self.reading, "قراءةُ الشرط"),
        ):
            if not value.strip():
                raise FractalMajorityLawError(f"{what} لا يكون فارغًا.")
        if not isinstance(self.standing, ConditionStanding):
            raise FractalMajorityLawError("منزلةُ الشرط عضوٌ في `ConditionStanding`.")

    @property
    def verdict_genus(self) -> Verdict | None:
        """الموقوفُ لا حكمَ له ههنا؛ والمُجرى حكمُه يُشتَقّ من المقابلة لا يُكتَب."""

        if self.standing is ConditionStanding.BLOCKED_ON_BYTES_NOT_DEPOSITED_HERE:
            return Verdict.NOT_CHECKABLE_HERE
        return None


THE_FIRST_CONDITION: Final[StandingCondition] = StandingCondition(
    question="هل تنفصل الحروفُ كلُّها؟",
    standing=ConditionStanding.BLOCKED_ON_BYTES_NOT_DEPOSITED_HERE,
    bound_to="ختمُ المجمَّد: `letter_fingerprint.py` في مستودع Algebra",
    reading=(
        "الجوابُ المُعلَن ثَمّ: ليس صفرًا — الزوجُ (د، ق) متصادمٌ في خانةٍ "
        "واحدةٍ ببعدين مكتوبين يدًا، والتفرُّدُ 28/29 بلا خطِّ صفر. ولا يُقرأ "
        "ههنا `AGREES` ولا `CONTRADICTS`، إذ لا بايتةَ منه في هذه الشجرة"
    ),
)

THE_SECOND_CONDITION: Final[StandingCondition] = StandingCondition(
    question="هل الخاتمةُ مختلفةٌ عن داخل اللفظ؟",
    standing=ConditionStanding.RUN_ON_OUR_SEALED_BYTES,
    bound_to="ختمُ المدوّنة: `corpora/quran-simple-enhanced.txt` عبر بابها المختوم",
    reading=(
        "نعم: الفتحةُ تنهار والإنتروبيا ترتفع عند الطرف على المفتاحين معًا. "
        "وأمّا المقاديرُ المنقولة فتوافق في مقابلات الداخل كلِّها وتخالف في "
        "تسعٍ من عشر مقابلاتِ الخاتمة، وتلك قِيست على مدوّنةٍ أخرى تفارق "
        "مدوّنتَنا بـ13,131 بايتًا"
    ),
)


# ---------------------------------------------------------------------------
# بوّابةُ ماركوف: تُقرأ ولا تُزحزَح
# ---------------------------------------------------------------------------


_THE_GATE_AS_READ_AT_IMPORT: Final[ChainReading] = token_markov_standing()


def the_corpus_gate_is_untouched() -> bool:
    """أزحزح شيءٌ من هذا الإيداع بوّابةَ ماركوف عمّا كانت عليه عند الاستيراد؟"""

    return token_markov_standing() == _THE_GATE_AS_READ_AT_IMPORT


# ---------------------------------------------------------------------------
# البقايا المسمّاة
# ---------------------------------------------------------------------------


A_MAJORITY_LAW_IS_STRONGER_THAN_A_FALSIFIED_TOTAL_ONE: Final[str] = (
    "A_MAJORITY_LAW_IS_STRONGER_THAN_A_FALSIFIED_TOTAL_ONE: الجدولُ يُودَع "
    "قانونَ غالبٍ بأربعة كسورٍ مسمّاةٍ بمواضعها، لا قانونَ تمامٍ يُستثنى منه في "
    "حاشية؛ وحصّةُ الصفوف المقيسة تُشتَقّ من الجدول ولا تُكتَب في حقل"
)

A_SIGNATURE_IS_A_COMMITMENT_NOT_A_MEASUREMENT: Final[str] = (
    "A_SIGNATURE_IS_A_COMMITMENT_NOT_A_MEASUREMENT: التوقيعاتُ الثلاثُ — "
    "الحنجرةُ ثلاثٌ، والصوائتُ مجهورةٌ، وغالبٌ لا تام — تُودَع التزاماتٍ على "
    "الدعوى؛ ولا يخرج منها رقمٌ ولا يُقرأ صفُّ الحنجرة مقيسًا"
)

A_DIRECTION_THAT_HOLDS_IS_NOT_A_MAGNITUDE_THAT_MATCHES: Final[str] = (
    "A_DIRECTION_THAT_HOLDS_IS_NOT_A_MAGNITUDE_THAT_MATCHES: انهيارُ الفتحة "
    "وارتفاعُ الإنتروبيا عند الطرف يثبتان على المفتاحين، وأرقامُ الخاتمة "
    "المنقولةُ تخالف المقيسَ في تسعٍ من عشر مقابلاتٍ؛ فيُسجَّل الاتّفاقُ في "
    "الاتّجاه والاختلافُ في المقدار، ولا يُقرأ أحدُهما بالآخر"
)

AN_ENDING_KEY_IS_A_CHOICE_AND_ITS_LADDER_TRAVELS_WITH_THE_FIGURE: Final[str] = (
    "AN_ENDING_KEY_IS_A_CHOICE_AND_ITS_LADDER_TRAVELS_WITH_THE_FIGURE: خاتمةُ "
    "الكلمة تُعرَّف بمفتاحٍ لا بطبيعة؛ ومفتاحا `EndingKey` يفترقان في التنوين "
    "الواقع على الألف الأخيرة، فلا يُنشَر رقمُ خاتمةٍ إلّا ومفتاحُه معه"
)

A_UNIQUENESS_WITHOUT_A_ZERO_LINE_IS_A_NUMBER_WITHOUT_A_SCALE: Final[str] = (
    "A_UNIQUENESS_WITHOUT_A_ZERO_LINE_IS_A_NUMBER_WITHOUT_A_SCALE: 28/29 "
    "تفرُّدًا لا يُقرأ حتى يُعاد مع خطِّ صفرٍ يُبيّن ما تُعطيه أبعادٌ عشوائيّةٌ "
    "بعددها؛ وبُعدان من أربعةٍ مكتوبان يدًا فالتصادمُ مقرَّرٌ قبل المدوّنة"
)

ONLY_A_SECOND_IMPLEMENTATION_MAKES_A_CROSS_CHECK_HERE: Final[str] = (
    "ONLY_A_SECOND_IMPLEMENTATION_MAKES_A_CROSS_CHECK_HERE: مقامُ 78,215 "
    "المنقولُ في `position_haraka_bit_account` يُعاد ههنا عدًّا للكلمات "
    "المشكولة في بايتاتنا فيتطابق؛ وهذا تقاطعُ تنفيذين لا اتّساقٌ داخليّ، "
    "ولا يُقرأ منه أنّ الجدولين يتقاسمان مجتمعًا"
)

FRACTAL_MAJORITY_LAW_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "A_MAJORITY_LAW_IS_STRONGER_THAN_A_FALSIFIED_TOTAL_ONE": (
        A_MAJORITY_LAW_IS_STRONGER_THAN_A_FALSIFIED_TOTAL_ONE
    ),
    "A_SIGNATURE_IS_A_COMMITMENT_NOT_A_MEASUREMENT": (
        A_SIGNATURE_IS_A_COMMITMENT_NOT_A_MEASUREMENT
    ),
    "A_DIRECTION_THAT_HOLDS_IS_NOT_A_MAGNITUDE_THAT_MATCHES": (
        A_DIRECTION_THAT_HOLDS_IS_NOT_A_MAGNITUDE_THAT_MATCHES
    ),
    "AN_ENDING_KEY_IS_A_CHOICE_AND_ITS_LADDER_TRAVELS_WITH_THE_FIGURE": (
        AN_ENDING_KEY_IS_A_CHOICE_AND_ITS_LADDER_TRAVELS_WITH_THE_FIGURE
    ),
    "A_UNIQUENESS_WITHOUT_A_ZERO_LINE_IS_A_NUMBER_WITHOUT_A_SCALE": (
        A_UNIQUENESS_WITHOUT_A_ZERO_LINE_IS_A_NUMBER_WITHOUT_A_SCALE
    ),
    "ONLY_A_SECOND_IMPLEMENTATION_MAKES_A_CROSS_CHECK_HERE": (
        ONLY_A_SECOND_IMPLEMENTATION_MAKES_A_CROSS_CHECK_HERE
    ),
}
"""بقايا هذا الإيداع مسمّاةً؛ ولا تُقرأ واحدةٌ منها ترخيصًا لرقمٍ بلا مصدر."""


_FORBIDDEN_FIELD_TOKENS: Final[tuple[str, ...]] = (
    "verdict",
    "authority",
    "birth",
)


def _assert_no_written_verdict_field() -> None:
    """لا حقلَ حكمٍ مكتوبٍ في بنيةٍ من بنى هذا الإيداع؛ والحكمُ صفةٌ مشتقّة."""

    for structure in (
        Comparison,
        KeyReading,
        LevelRow,
        NamedBreak,
        PositionCensus,
        QuotedRow,
        Signature,
        StandingCondition,
        TranscribedRow,
    ):
        for field in fields(structure):
            if any(token in field.name for token in _FORBIDDEN_FIELD_TOKENS):
                raise FractalMajorityLawError(
                    f"الحقلُ `{field.name}` في `{structure.__name__}` يُكتَب حكمًا "
                    "أو سلطةً، وحكمُ هذا الإيداع يُشتَقّ بالحساب."
                )


def _assert_the_breaks_are_four_and_placed() -> None:
    """الكسورُ أربعةٌ بأسماءٍ متمايزةٍ ومستوياتٍ متمايزة؛ يُفحَص لا يُوصَف."""

    if len(THE_FOUR_BREAKS) != 4:
        raise FractalMajorityLawError("الكسورُ المُعلَنةُ أربعةٌ لا تزيد ولا تنقص.")
    names = {a_break.name for a_break in THE_FOUR_BREAKS}
    levels = {a_break.level for a_break in THE_FOUR_BREAKS}
    if len(names) != 4 or len(levels) != 4:
        raise FractalMajorityLawError("كسرانِ باسمٍ واحدٍ أو بمستوًى واحدٍ لا يُودَعان.")
    declared_levels = {row.level for row in THE_LEVELS}
    for a_break in THE_FOUR_BREAKS:
        if a_break.level not in declared_levels:
            raise FractalMajorityLawError(
                f"مستوى الكسر «{a_break.level}» ليس صفًّا في `THE_LEVELS`."
            )


def _assert_the_law_is_not_claimed_total() -> None:
    """لا يُودَع الجدولُ تامًّا: لا بدّ أن يُعلِن كسرًا، وألّا يكون كلُّه كسرًا."""

    if not 0.0 < measured_share_of_the_table() < 1.0:
        raise FractalMajorityLawError(
            "جدولٌ كلُّه مقيسٌ أو كلُّه غيرُ مقيسٍ لا يُودَع قانونَ غالب."
        )


_assert_no_written_verdict_field()
_assert_the_breaks_are_four_and_placed()
_assert_the_law_is_not_claimed_total()
