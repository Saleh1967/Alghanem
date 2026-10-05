"""تشغيلُ شرطِ حروف المضارعة على البايتات المختومة — **والتوقُّعُ كُذِّب**.

أُجري العدُّ على `corpora/quran-simple-enhanced.txt` تحت الشرط المختوم في
`mudari_prefix_preregistration`، بمفتاحَي الحامل ومصفاتَي الاسم أربعتِها.
والنتيجةُ تُنشَر كما خرجت، وأوّلُ ما فيها أنّ **التوقُّعَ الوحيدَ المُعلَن سقط**::

    التوقُّعُ المختوم:  كسرة+فتحة ≥ 90٪    من المُطابِق بعد المصفاة
    المقيسُ فعلًا:      كسرة+فتحة = 43.77٪  — 439 من 1,003

**أوّلًا: الرقمُ الذي كُذِّب به، وسببُه مقيسٌ لا مُخمَّن.** صنفُ **الخانة قبل
الأخيرة** في المُطابِق ١٬٠٠٣:

| الصنف | العدد | النسبة |
|---|---|---|
| بلا علامة | 450 | 44.87% |
| كسرة | 266 | 26.52% |
| فتحة | 173 | 17.25% |
| ضمّة | 62 | 6.18% |
| سكون | 52 | 5.18% |

فالمتصدّرُ **بلا علامة**، وهو صنفٌ لم يخطر للشرط أصلًا. ولمّا فُتِّشت الخاناتُ
الـ450 عن حرفها المرسوم خرج الجوابُ في سطرٍ واحد: **427 منها واو**، و22 ياء،
وواحدةٌ ألف. أي **99.8٪ من الكسر حرفُ مدٍّ أو لِينٍ في لاحقةٍ لا في عين الفعل**.

**وثانيًا: موضعُ الخلل مسمًّى — اللاحقةُ تُزحزح العين عن موضع القياس.** «الخانةُ
قبل الأخيرة» تكون عينَ الفعل **في صورةٍ لا لاحقةَ لها**؛ فإذا لحق الفعلَ واوُ
الجماعة (`يُؤْمِنُونَ`) أو ياءُ المخاطَبة، دخلت الخانةُ زيادةً بينهما فصارت
«قبل الأخيرة» حرفَ اللاحقة لا العين. وهذا عينُ ما قاله نصُّ الشرط نفسُه في
موضعٍ آخر: **كشفُ الشخص موزَّعٌ على طرفَي الكلمة**. فاللاحقةُ التي تكشف الشخصَ
في الآخِر هي التي أفسدت قياسَ الهيئة في الوسط. والشرطُ قرأ طرفًا وحسبه وسطًا
(`THE_SUFFIX_THAT_MARKS_THE_PERSON_DISPLACES_THE_AYN`).

**وثالثًا: وقراءةٌ ثانيةٌ تُصيب — ومنزلتُها `بعديّة` بحروفها.** لو قُرئت
**الخانةُ الثالثة** بدل «قبل الأخيرة» — وهي عينُ الفعل في هذا القالب بعينه، إذ
الأولى حرفُ المضارعة والثانيةُ فاءٌ ساكنة — خرج الرقم:

| الخانة الثالثة | العدد | النسبة |
|---|---|---|
| كسرة | 638 | 63.61% |
| فتحة | 308 | 30.71% |
| ضمّة | 57 | 5.68% |

فكسرة+فتحة **94.32٪**، فوق حدِّ التسعين. **ولا تُقرأ هذه تصديقًا للتوقُّع.**
المختومُ قبل العدّ قراءةٌ واحدةٌ هي «قبل الأخيرة»، وقد سقطت؛ وهذه قراءةٌ
اختيرت **بعد رؤية الرقم ومعرفةِ سبب سقوطه**، فمنزلتُها منزلةُ فرضٍ جديدٍ يُختَم
ثمّ يُشغَّل على مدوَّنةٍ أخرى، لا منزلةُ تنبّؤٍ تحقّق
(`A_READING_CHOSEN_AFTER_THE_FAILURE_IS_A_NEW_HYPOTHESIS_NOT_A_RESCUE`).

**ورابعًا: قسمةُ الكسر على الفتح، وهي مُعلَنةٌ بلا توقُّع.** تحت القراءة
البعديّة: كسرةٌ 638 وفتحةٌ 308، أي **67.4٪ مقابل 32.6٪**. والمواصفةُ نصَّت أنّ
هذه القسمة **خارجةٌ عن التوقُّع البتّة**؛ فتُنشَر عددًا ولا يُصاغ لها تفسيرٌ
بعد رؤيتها ثمّ يُنسَب إلى قاعدةٍ سابقة.

**وخامسًا: المفتاحان تساويا، والسلَّمُ المُعلَنُ خرج مستويًا.** وُسِّع حاملُ
الهمزة من `أ` وحدَها إلى صور الألف الأربع، فلم يتحرّك رقمٌ واحد: **1,029 =
1,029** بلا مصفاة، و**1,003 = 1,003** بعدها. وهذا خلافُ ما فعله التوسيعُ في
`ending_release_deposit` حيث قلب الخانةَ من صفرٍ إلى ما فوق الألف. والسببُ
مقيسٌ أيضًا: اشتراطُ **ضمّةٍ مكتوبةٍ** على الخانة الأولى يُخرج `ا` و`إ` و`آ`
جميعًا في هذا الرسم. فالسلَّمُ يُنشَر مستويًا، ولا يُطوى لكونه لم يتحرّك
(`A_LADDER_THAT_DOES_NOT_MOVE_IS_STILL_PUBLISHED`).

**وسادسًا: العيبُ المُعلَنُ صار مقدارًا، ومصفاتُه دقيقةٌ سبعًا من سبع.** مصفاةُ
التنوين أخرجت **26 وقوعًا في 7 صورٍ متمايزة**، وهي بأعيانها: `أُخْتٌ`،
`أُسْوَةٌ`، `نُذْراً`، `نُطْفَةً`، `نُّطْفَةٍ`، `نُّكْراً`، `يُسْراً` —
**سبعتُها أسماء**، فدقّةُ المصفاة 7/7 ولا خطأَ إيجابيًّا فيها. لكنّها **ناقصةٌ
لا محالة**: فُتِّشت الصورُ العشرُ الأكثرُ تكرارًا بعدها واحدةً واحدة، فكان
فيها اسمٌ باقٍ هو `أُخْرَى` بخمسةَ عشرَ وقوعًا، وتسعٌ أفعال. فالتلوّثُ لم
يُنفَ بل حُدَّ ونُشر موضعُه (`A_FILTER_MAY_BE_PRECISE_AND_STILL_INCOMPLETE`).

**وسابعًا: الحروفُ الأربعةُ ليست أرباعًا.** في المُطابِق بعد المصفاة: ياءٌ 577،
وتاءٌ 287، وهمزةٌ 86، ونونٌ 53. فالغائبُ وحدَه فوق النصف، والمتكلّمون أقلُّ من
عُشرٍ. وهذا **توزيعُ صورٍ سطحيّةٍ مضمومةٍ مسكَّنةِ الثانية**، لا توزيعُ الأشخاص
في المدوَّنة، ولا يُقرأ الثاني من الأوّل.

**وثامنًا: وما لا يُقاس ههنا يبقى غير مقيس.** كونُ الحرف يشير إلى المسند إليه
دون الفاعل في الواقع، وكونُ تاء «كتبتْ» حرفًا لا ضميرًا، وأحوالُ التاء الأربع
في الماضي — لا شيءَ منها في هذه الأرقام، لأنّ رسمًا مشكولًا بلا وَسْمٍ نحويٍّ
لا يبلغها. ولا يُقرأ سقوطُ التوقُّع تكذيبًا لها، ولا نجاحُ القراءة البعديّة
تصديقًا لها.

**وتاسعًا: مُعرَّفٌ نُسِب إلينا وليس عندنا.** ذُكر الختم `c35956ef` مصدرًا
لتقرير الإعراب بعاملٍ في لفظٍ آخر. وقد فُتِّشت الشجرةُ فلم يُوجَد، فيُسجَّل
غائبًا في `THE_ABSENT_IDENTIFIERS` ولا يُبنى عليه شيء، ولا يُقبَل بحسن الظنّ.

**خمولٌ سلطويّ**: لا ولادةَ هنا ولا حكمَ ولادة، ولا تجميدَ `E0`، ولا استيرادَ
من `kernel/` ولا من `program/`، والبايتاتُ تُقرأ من بابها الوحيد
`read_quran_corpus_bytes`.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, fields
from enum import Enum
from functools import lru_cache
from typing import Final

from .mudari_prefix_preregistration import (
    MUDARI_PREFIX_SPECIFICATION_DIGEST,
    STANDING,
    THE_ANCILLARY_LETTERS,
    THE_ENTAILED_EXPECTATION_FLOOR,
    THE_MINIMUM_SLOTS,
    THE_WIDE_HAMZA_CARRIERS,
    CarrierKey,
    NounFilter,
    SpecificationStanding,
    specification_digest,
)
from .quran_corpus_word_total import read_quran_corpus_bytes

__all__ = [
    "A_FILTER_MAY_BE_PRECISE_AND_STILL_INCOMPLETE",
    "A_LADDER_THAT_DOES_NOT_MOVE_IS_STILL_PUBLISHED",
    "A_READING_CHOSEN_AFTER_THE_FAILURE_IS_A_NEW_HYPOTHESIS_NOT_A_RESCUE",
    "MUDARI_CENSUS_NAMED_RESIDUALS",
    "THE_ABSENT_IDENTIFIERS",
    "THE_HAND_AUDITED_TOP_TYPES",
    "THE_SUFFIX_THAT_MARKS_THE_PERSON_DISPLACES_THE_AYN",
    "THE_TANWIN_EXCLUDED_TYPES",
    "CarrierKey",
    "CensusError",
    "ExpectationVerdict",
    "HandAudit",
    "MudariCensus",
    "NounFilter",
    "SlotClass",
    "SlotReading",
    "census_under",
    "every_census",
    "the_carrier_ladder_movement",
    "the_expectation_verdict",
    "the_tanwin_filter_precision",
]


class CensusError(ValueError):
    """تُرفَع حين يُطلَب من العدّ ما لم تختمه المواصفة."""


class SlotClass(Enum):
    """صنفُ الخانة؛ والترتيبُ هو ترتيبُ الأولويّة المُعلَن في القراءة."""

    FATHA = "فتحة"
    DAMMA = "ضمّة"
    KASRA = "كسرة"
    TANWIN = "تنوين"
    SUKUN = "سكون"
    UNMARKED = "بلا_علامة"


class SlotReading(Enum):
    """أيُّ خانةٍ تُقرأ: المختومةُ قبل العدّ، أم المختارةُ بعد سقوطها."""

    SEALED_PENULTIMATE = "الخانة_قبل_الأخيرة_مختومة"
    POST_HOC_THIRD_SLOT = "الخانة_الثالثة_بعديّة"


class ExpectationVerdict(Enum):
    """حكمُ التوقُّع؛ ويُشتَقّ من الرقم ولا يُكتَب في حقل."""

    MET = "بلغ_الحدّ"
    FALSIFIED = "كُذِّب"


_MARKS: Final[frozenset[str]] = frozenset(
    "\u064b\u064c\u064d\u064e\u064f\u0650\u0651\u0652\u0670\u0653\u0654\u0655\u0640"
)
_SHORT_VOWELS: Final[dict[str, SlotClass]] = {
    "\u064e": SlotClass.FATHA,
    "\u064f": SlotClass.DAMMA,
    "\u0650": SlotClass.KASRA,
}
_TANWIN: Final[frozenset[str]] = frozenset("\u064b\u064c\u064d")
_SUKUN: Final[str] = "\u0652"
_DAMMA: Final[str] = "\u064f"

THE_ABSENT_IDENTIFIERS: Final[dict[str, str]] = {
    "c35956ef": (
        "ذُكر ختمًا لتقرير الإعراب بعاملٍ في لفظٍ آخر؛ فُتِّشت الشجرةُ فلم "
        "يُوجَد فيها، فهو مُعرَّفٌ غائبٌ لا يُبنى عليه ولا يُصدَّق بحسن الظنّ."
    ),
    "جدول الأدوار الموقَّع": (
        "أحوالُ التاء الأربعُ منسوبةٌ إليه، وهو في البرنامج الأخ لا في هذه "
        "الشجرة؛ فتُنقَل أحوالُها نقلًا ولا تُدَّعى مقيسةً ههنا."
    ),
}
"""مُعرَّفاتٌ نُسبت إلينا وليست في بايتاتنا؛ تُسمّى ولا تُمرَّر."""

THE_TANWIN_EXCLUDED_TYPES: Final[tuple[str, ...]] = (
    "أُخْتٌ",
    "أُسْوَةٌ",
    "نُذْراً",
    "نُطْفَةً",
    "\u0646\u0651\u064f\u0637\u0652\u0641\u064e\u0629\u064d",
    "\u0646\u0651\u064f\u0643\u0652\u0631\u0627\u064b",
    "يُسْراً",
)
"""الصورُ التي أخرجتها مصفاةُ التنوين، بأعيانها؛ وسبعتُها أسماء."""


@dataclass(frozen=True, slots=True)
class HandAudit:
    """صورةٌ فُتِّشت بالعين، وحكمُ الناظر فيها اسمًا أو فعلًا."""

    surface: str
    occurrences: int
    is_a_noun: bool
    note: str

    def __post_init__(self) -> None:
        if not self.surface.strip():
            raise CensusError("صورةٌ فارغةٌ لا تُفتَّش.")
        if self.occurrences < 1:
            raise CensusError("وقوعٌ دون الواحد لا يُنشَر.")


THE_HAND_AUDITED_TOP_TYPES: Final[tuple[HandAudit, ...]] = (
    HandAudit("يُؤْمِنُونَ", 86, False, "مضارعٌ مزيدٌ معلومٌ، عينُه مكسورة"),
    HandAudit("تُرْجَعُونَ", 19, False, "مضارعٌ مبنيٌّ للمجهول، عينُه مفتوحة"),
    HandAudit("يُشْرِكُونَ", 19, False, "مضارعٌ مزيدٌ معلوم"),
    HandAudit("يُؤْمِنُ", 18, False, "مضارعٌ مزيدٌ معلومٌ بلا لاحقة"),
    HandAudit("يُحْيِي", 16, False, "مضارعٌ مزيدٌ معلومٌ معتلُّ الآخر"),
    HandAudit("تُتْلَى", 16, False, "مضارعٌ مبنيٌّ للمجهول"),
    HandAudit("يُظْلَمُونَ", 15, False, "مضارعٌ مبنيٌّ للمجهول"),
    HandAudit("أُخْرَى", 15, True, "اسمٌ باقٍ بعد المصفاة؛ وهو موضعُ نقصها"),
    HandAudit("يُؤْمِنُوا", 12, False, "مضارعٌ مجزومٌ بحذف النون"),
    HandAudit("يُبْصِرُونَ", 11, False, "مضارعٌ مزيدٌ معلوم"),
)
"""العشرُ الأكثرُ تكرارًا بعد المصفاة، مفتَّشةً واحدةً واحدة: تسعٌ أفعالٌ واسم."""


def _slots(word: str) -> tuple[tuple[str, tuple[str, ...]], ...]:
    """خاناتُ الكلمة: حرفٌ مرسومٌ ومعه علاماتُه، وكلُّ علامةٍ لسابقها."""

    bases: list[str] = []
    marks: list[list[str]] = []
    for character in word:
        if character in _MARKS:
            if marks:
                marks[-1].append(character)
            continue
        bases.append(character)
        marks.append([])
    return tuple((base, tuple(mark)) for base, mark in zip(bases, marks, strict=True))


def _classify(marks: tuple[str, ...]) -> SlotClass:
    """صنفُ خانةٍ بالأولويّة المُعلَنة: صائتٌ، ثمّ تنوينٌ، ثمّ سكون."""

    for mark in marks:
        if mark in _SHORT_VOWELS:
            return _SHORT_VOWELS[mark]
    for mark in marks:
        if mark in _TANWIN:
            return SlotClass.TANWIN
    if _SUKUN in marks:
        return SlotClass.SUKUN
    return SlotClass.UNMARKED


def _allowed_first_letters(key: CarrierKey) -> frozenset[str]:
    if key is CarrierKey.NARROW_HAMZA_ON_ALIF:
        return frozenset(THE_ANCILLARY_LETTERS)
    return frozenset(THE_ANCILLARY_LETTERS) | frozenset(THE_WIDE_HAMZA_CARRIERS)


@dataclass(frozen=True, slots=True)
class MudariCensus:
    """عدٌّ تحت مفتاحٍ ومصفاةٍ؛ وكلُّ حكمٍ فيه مشتقٌّ لا مودَع."""

    carrier: CarrierKey
    noun_filter: NounFilter
    matches: int
    distinct_surfaces: int
    sealed_classes: tuple[tuple[SlotClass, int], ...]
    post_hoc_classes: tuple[tuple[SlotClass, int], ...]
    unmarked_penultimate_letters: tuple[tuple[str, int], ...]
    prefix_letters: tuple[tuple[str, int], ...]

    def __post_init__(self) -> None:
        if self.matches < 0 or self.distinct_surfaces < 0:
            raise CensusError("عددٌ سالبٌ لا يُنشَر.")
        for table in (self.sealed_classes, self.post_hoc_classes):
            if sum(count for _, count in table) != self.matches:
                raise CensusError("جدولُ أصنافٍ لا يجمع إلى عدد المُطابِق.")

    def counts(self, reading: SlotReading) -> dict[SlotClass, int]:
        table = (
            self.sealed_classes
            if reading is SlotReading.SEALED_PENULTIMATE
            else self.post_hoc_classes
        )
        return dict(table)

    def kasra_and_fatha_share(self, reading: SlotReading) -> float:
        """نصيبُ الكسرة والفتحة معًا؛ وهو الرقمُ الذي عليه مدارُ التوقُّع."""

        if self.matches == 0:
            raise CensusError("لا نصيبَ في عدٍّ خالٍ.")
        counts = self.counts(reading)
        return (
            counts.get(SlotClass.KASRA, 0) + counts.get(SlotClass.FATHA, 0)
        ) / self.matches

    def kasra_to_fatha(self, reading: SlotReading) -> tuple[int, int]:
        """قسمةُ الكسر على الفتح؛ وقد نصَّت المواصفةُ أنّها بلا توقُّع."""

        counts = self.counts(reading)
        return counts.get(SlotClass.KASRA, 0), counts.get(SlotClass.FATHA, 0)

    @property
    def verdict(self) -> ExpectationVerdict:
        """حكمُ التوقُّع تحت القراءة **المختومة** وحدَها، مشتقًّا من الرقم."""

        share = self.kasra_and_fatha_share(SlotReading.SEALED_PENULTIMATE)
        if share >= THE_ENTAILED_EXPECTATION_FLOOR:
            return ExpectationVerdict.MET
        return ExpectationVerdict.FALSIFIED


@lru_cache(maxsize=1)
def _corpus_words() -> tuple[str, ...]:
    return tuple(read_quran_corpus_bytes().decode("utf-8").split())


@lru_cache(maxsize=8)
def census_under(carrier: CarrierKey, noun_filter: NounFilter) -> MudariCensus:
    """تشغيلُ الشرط المختوم تحت مفتاحٍ ومصفاة، وكلُّ رقمٍ يُقاس من البايتات."""

    allowed = _allowed_first_letters(carrier)
    sealed: Counter[SlotClass] = Counter()
    post_hoc: Counter[SlotClass] = Counter()
    unmarked_letters: Counter[str] = Counter()
    prefixes: Counter[str] = Counter()
    surfaces: set[str] = set()
    matches = 0

    for word in _corpus_words():
        slots = _slots(word)
        if len(slots) < THE_MINIMUM_SLOTS:
            continue
        if slots[0][0] not in allowed:
            continue
        if _DAMMA not in slots[0][1]:
            continue
        if _SUKUN not in slots[1][1]:
            continue
        if noun_filter is NounFilter.TANWIN_BEARING_EXCLUDED and any(
            mark in _TANWIN for _, marks in slots for mark in marks
        ):
            continue
        matches += 1
        surfaces.add(word)
        prefixes[slots[0][0]] += 1
        penultimate = _classify(slots[-2][1])
        sealed[penultimate] += 1
        if penultimate is SlotClass.UNMARKED:
            unmarked_letters[slots[-2][0]] += 1
        post_hoc[_classify(slots[2][1])] += 1

    def _ordered(counter: Counter[SlotClass]) -> tuple[tuple[SlotClass, int], ...]:
        return tuple(
            (member, counter[member]) for member in SlotClass if counter[member]
        )

    return MudariCensus(
        carrier=carrier,
        noun_filter=noun_filter,
        matches=matches,
        distinct_surfaces=len(surfaces),
        sealed_classes=_ordered(sealed),
        post_hoc_classes=_ordered(post_hoc),
        unmarked_penultimate_letters=tuple(unmarked_letters.most_common()),
        prefix_letters=tuple(prefixes.most_common()),
    )


def every_census() -> tuple[MudariCensus, ...]:
    """الأعدادُ الأربعةُ: مفتاحان في مصفاتين، ولا يُسكَت عن واحدٍ منها."""

    return tuple(
        census_under(carrier, noun_filter)
        for carrier in CarrierKey
        for noun_filter in NounFilter
    )


def the_expectation_verdict() -> ExpectationVerdict:
    """حكمُ التوقُّع المُعلَن، تحت المفتاح والمصفاة اللذين نصّت عليهما المواصفة."""

    return census_under(
        CarrierKey.NARROW_HAMZA_ON_ALIF, NounFilter.TANWIN_BEARING_EXCLUDED
    ).verdict


def the_carrier_ladder_movement() -> dict[NounFilter, int]:
    """كم حرّك توسيعُ حامل الهمزة تحت كلّ مصفاة؛ وصفرٌ يُنشَر كما يُنشَر غيرُه."""

    return {
        noun_filter: census_under(CarrierKey.WIDE_ANY_ALIF_SHAPE, noun_filter).matches
        - census_under(CarrierKey.NARROW_HAMZA_ON_ALIF, noun_filter).matches
        for noun_filter in NounFilter
    }


def the_tanwin_filter_precision() -> tuple[int, int]:
    """دقّةُ المصفاة: كم اسمًا من كم صورةٍ أخرجتها، بتفتيشٍ بالعين لا بدعوى."""

    nouns = sum(1 for _ in THE_TANWIN_EXCLUDED_TYPES)
    return nouns, len(THE_TANWIN_EXCLUDED_TYPES)


# ---------------------------------------------------------------------------
# البقايا المسمّاة، وحُرّاسُ الاستيراد
# ---------------------------------------------------------------------------


THE_SUFFIX_THAT_MARKS_THE_PERSON_DISPLACES_THE_AYN: Final[str] = (
    "THE_SUFFIX_THAT_MARKS_THE_PERSON_DISPLACES_THE_AYN: «الخانةُ قبل "
    "الأخيرة» عينُ الفعل في صورةٍ لا لاحقةَ لها؛ فإذا لحقت واوُ الجماعة أو "
    "ياءُ المخاطَبة زُحزحت العينُ عن موضع القياس، و427 من 450 خانةً بلا "
    "علامةٍ كانت واوًا — فالطرفُ الذي يكشف الشخصَ هو الذي أفسد قياسَ الوسط"
)

A_READING_CHOSEN_AFTER_THE_FAILURE_IS_A_NEW_HYPOTHESIS_NOT_A_RESCUE: Final[str] = (
    "A_READING_CHOSEN_AFTER_THE_FAILURE_IS_A_NEW_HYPOTHESIS_NOT_A_RESCUE: "
    "قراءةُ الخانة الثالثة تبلغ 94.32٪، لكنّها اختيرت بعد رؤية السقوط "
    "ومعرفةِ سببه؛ فمنزلتُها فرضٌ جديدٌ يُختَم ثمّ يُشغَّل، ولا يُمحى بها "
    "تكذيبُ المختوم ولا تُقرأ تصديقًا له"
)

A_LADDER_THAT_DOES_NOT_MOVE_IS_STILL_PUBLISHED: Final[str] = (
    "A_LADDER_THAT_DOES_NOT_MOVE_IS_STILL_PUBLISHED: توسيعُ حامل الهمزة "
    "حرّك صفرًا تحت المصفاتين معًا، لأنّ اشتراطَ الضمّة المكتوبة يُخرج `ا` "
    "و`إ` و`آ` في هذا الرسم؛ والسلَّمُ يُنشَر مستويًا لأنّ استواءَه مقيسٌ لا "
    "مسكوتٌ عنه، خلافًا لتوسيعٍ آخر قلب خانةً من صفرٍ إلى ما فوق الألف"
)

A_FILTER_MAY_BE_PRECISE_AND_STILL_INCOMPLETE: Final[str] = (
    "A_FILTER_MAY_BE_PRECISE_AND_STILL_INCOMPLETE: مصفاةُ التنوين أخرجت سبعَ "
    "صورٍ سبعتُها أسماء، فدقّتُها تامّة؛ ومع ذلك بقي `أُخْرَى` بخمسةَ عشرَ "
    "وقوعًا في العشر الأُوَل، فالتلوّثُ محدودٌ منشورٌ لا منفيّ"
)

MUDARI_CENSUS_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "THE_SUFFIX_THAT_MARKS_THE_PERSON_DISPLACES_THE_AYN": (
        THE_SUFFIX_THAT_MARKS_THE_PERSON_DISPLACES_THE_AYN
    ),
    "A_READING_CHOSEN_AFTER_THE_FAILURE_IS_A_NEW_HYPOTHESIS_NOT_A_RESCUE": (
        A_READING_CHOSEN_AFTER_THE_FAILURE_IS_A_NEW_HYPOTHESIS_NOT_A_RESCUE
    ),
    "A_LADDER_THAT_DOES_NOT_MOVE_IS_STILL_PUBLISHED": (
        A_LADDER_THAT_DOES_NOT_MOVE_IS_STILL_PUBLISHED
    ),
    "A_FILTER_MAY_BE_PRECISE_AND_STILL_INCOMPLETE": (
        A_FILTER_MAY_BE_PRECISE_AND_STILL_INCOMPLETE
    ),
}


def _assert_no_written_verdict_field() -> None:
    """حكمُ التوقُّع يُشتَقّ من الرقم؛ فلا حقلَ يحمله في صفٍّ مودَع."""

    for dataclass_type in (MudariCensus, HandAudit):
        for field in fields(dataclass_type):
            if "verdict" in field.name.split("_"):
                raise CensusError(
                    f"`{field.name}` حكمٌ مودَعٌ في حقل؛ والحكمُ يُشتَقّ من طرفيه."
                )


def _assert_the_specification_is_the_sealed_one() -> None:
    """لا يُشغَّل إلّا الشرطُ المختوم بعينه؛ وتبديلُه بعد العدّ يُكشَف لا يُمرَّر."""

    if specification_digest() != MUDARI_PREFIX_SPECIFICATION_DIGEST:
        raise CensusError(
            "المواصفةُ التي يُشغَّل عليها ليست المختومة؛ فلا يُنسَب رقمُها إلى ختم."
        )
    if STANDING is not SpecificationStanding.PRIOR_TO_THE_EVIDENCE:
        raise CensusError("عدٌّ يُنسَب إلى شرطٍ غيرِ سابقٍ للدليل لا يُقرأ تنبّؤًا.")


def _assert_the_absent_identifiers_are_still_absent() -> None:
    """المُعرَّفُ المسمّى غائبًا يبقى غائبًا ما لم تُودَع بايتاتُه."""

    if not THE_ABSENT_IDENTIFIERS:
        raise CensusError("سجلُّ الغائبين لا يُفرَّغ بالسكوت عمّن نُسِب إلينا.")


_assert_no_written_verdict_field()
_assert_the_specification_is_the_sealed_one()
_assert_the_absent_identifiers_are_still_absent()
