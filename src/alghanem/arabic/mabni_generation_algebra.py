"""جبرُ التوليد: فضاءُ القوالب يُولَّد حسابًا، ثمّ يُقاس كم منه أثبتته البايتات.

الدعوى المعروضةُ ههنا: «ثمانيةٌ وعشرون صامتًا في أربعة صوائتَ تُخرِج مئةً
واثنتي عشرةَ، ثمّ تتدرّج القوالبُ فتُخرِج المبنيّاتِ كلَّها، ثمّ ينفرز المبنيُّ
من المعرَب وفق قوانينَ رياضيّة». وههنا تُفكَّك إلى ثلاث طبقات، ولكلٍّ حكمُها:

**أوّلًا: السكونُ ليس صائتًا، فالـ112 خلايا لا مقاطع.**
`THE_HUNDRED_AND_TWELVE_IS_A_CELL_COUNT_NOT_A_SYLLABLE_COUNT`: الأربعةُ في
`letter_haraka_partition.THE_DECLARED_HARAKAT` ثلاثُ حركاتٍ **وسكون**، والسكونُ
عدمُ الحركة لا حركة. و`syllable_preregistration.template_of` ترفض نواةً خارج
`{1, 2}` من الصوائت، فالصامتُ الساكنُ لا يُنشئ مقطعًا بل يُغلِقه. فثمنُ عدِّ
السكون صائتًا مقيسٌ لا مُجادَلٌ فيه: **ثمانٍ وعشرون** من المئةِ والاثنتي عشرةَ
خليّةٌ لا تقع مقطعًا ألبتّة، فـ`CV` أربعٌ وثمانون لا مئةٌ واثنتا عشرة.

**وثانيًا: الفضاءُ يُولَّد، والبايتاتُ تُثبِت أقلَّ منه وتُثبِت خارجَه معًا.**
على المدوّنة المختومة، ومن الأرخص إلى الأغلى:

| القالب | الفضاء | المُثبَت | خارجَ الفضاء | التغطية | الوقوعات |
|---|---|---|---|---|---|
| CV | 84 | 84 | 3 | 96.429% | 82,992 |
| CVV | 84 | 85 | 4 | 96.429% | 35,846 |
| CVC | 2,352 | 1,434 | 119 | 55.910% | 53,046 |
| CVVC | 2,352 | 75 | 2 | 3.104% | 1,492 |
| CVCC | 65,856 | 36 | 1 | 0.053% | 234 |
| CVVCC | 65,856 | 0 | 0 | 0.000% | 0 |

وفي الصفّ الثاني **فائضٌ**: المُثبَتُ خمسةٌ وثمانون والفضاءُ أربعٌ وثمانون.
فالدعوى تنتقض من جهتين معًا لا من جهة: الفضاءُ **يَفضُل** عمّا أُثبِت (ثلاثُ
خلايا من أربعٍ وثمانين لم تقع)، و**يَقصُر** عمّا أُثبِت (أربعُ خلايا وقعت وهو
لا يُخرِجها). وسببُ القصور مُسمًّى: **الهمزةُ حاملٌ تاسعٌ وعشرون** في قراءة
`p_extractor`، وهي خارجَ الثمانية والعشرين المُعلَنة
(`THE_ATTESTED_CARRIERS_EXCEED_THE_DECLARED_ALPHABET`).

**وثالثًا: «الاستنفادُ قبل الترخيص» يوقف السُّلَّم عند درجته الأولى.**
الشرطُ المطلوبُ أن لا يُرخَّص قالبٌ أغلى حتّى يُستنفَد الأرخص. والأرخصُ
`CV` لم يُستنفَد على هذه البايتات: إحدى وثمانون خليّةً من أربعٍ وثمانين داخلَ
الفضاء. فلا تُرخَّص درجةٌ ثانية، ولا ثالثة
(`AN_UNEXHAUSTED_RUNG_LICENSES_NOTHING_ABOVE_IT`). وهذا **ليس عيبًا في
التنفيذ** بل هو ما يقوله الشرطُ إذا أُخِذ على ظاهره؛ ومن رخَّص الدرجاتِ كلَّها
مع ذلك فقد ترك الشرطَ ولم يُعمِله.

**ورابعًا: الوزنُ لا يَفرِز، فالفرزُ الآليُّ مُنتقَض لا مؤجَّل.**
على المدوّنة المختومة **426** وزنًا متمايزًا تحمل **15,054** كلمةً متمايزة،
وأكبرُ ليفٍ `CVC·CV·CV` يحمل **725** كلمةً، ومئةٌ واثنتان من الأوزان وحدَها
مُفردةُ الليف. فالدالّةُ من الكلمة إلى وزنها ليست متباينة، ولا مقلوبَ لها؛
فلا تُستخرَج من الوزن وحدَه هويّةُ الكلمة، فضلًا عن بابها إعرابًا أو بناءً
(`A_SHAPE_THAT_CARRIES_SEVEN_HUNDRED_WORDS_SORTS_NOTHING`). وهذا حكمٌ على
**هذه** البايتات بهذه القوالب، لا على العربيّة.

**وخامسًا: البناءاتُ الاثنتا عشرة المطلوبةُ لا تُبنى ههنا، وتُسمّى.**
الحروفُ الوظيفيّةُ والأدواتُ والضمائرُ والمبنيّاتُ والأفعالُ والمشتقّاتُ
والجامدُ والأزمنةُ والعددُ والتذكيرُ والتعريفُ والفرزُ إعرابًا وبناءً: كلُّها
تطلب موادَّ موسومةً غيرَ مُودَعةٍ في هذه الشجرة — ومادّتا `nahw_lexicon`
(المغني وسيبويه) غيرُ مودَعتَين عمدًا. فتُسجَّل كلُّ واحدةٍ بمادّتها الناقصة
ومنزلتها في `THE_TWELVE_REQUESTED_BUILDS`، ولا يُخرَج منها شيءٌ بالتخمين
(`AN_UNDEPOSITED_MATERIAL_IS_A_NAMED_SUSPENSION_NOT_A_DEFAULT`).

**وسادسًا: المتعذِّرُ محمولٌ لا مطروح.** من ثمانيةٍ وسبعين ألفًا ومئتين
وخمسةٍ وأربعين رمزًا فيه حرفٌ عربيّ، **15,972** — أي 20.41% — لم يُقطِّعها
المُقطِّعُ وأكثرُها مبدوءٌ بألفٍ عاريةٍ لا تُميَّز همزةُ وصلها؛ وهي محمولةٌ في
المقام لا مطروحةٌ منه، لأنّ طرحَها يرفع كلَّ نسبةٍ أعلاه بإخفاء ما لم يُقرأ
(`AN_UNSEGMENTED_WORD_IS_CARRIED_IN_THE_DENOMINATOR`).

تسجيلٌ لا سلطة: لا ولادةَ ههنا ولا حكمَ ولادةٍ كرنليًّا ولا تجميدَ `E0`، ولا
تستورد هذه الوحدةُ من `kernel/` شيئًا.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Final

from .letter_haraka_partition import THE_DECLARED_HARAKAT, THE_DECLARED_LETTERS
from .p_extractor import LetterReading, read_surface
from .syllabifier import Syllable, syllabify_surface
from .syllable_preregistration import SyllableTemplate

__all__ = [
    "AN_UNEXHAUSTED_RUNG_LICENSES_NOTHING_ABOVE_IT_NOTE",
    "AN_UNSEGMENTED_WORD_IS_CARRIED_IN_THE_DENOMINATOR_NOTE",
    "A_SHAPE_THAT_CARRIES_SEVEN_HUNDRED_WORDS_SORTS_NOTHING_NOTE",
    "AN_UNDEPOSITED_MATERIAL_IS_A_NAMED_SUSPENSION_NOT_A_DEFAULT_NOTE",
    "BuildStanding",
    "ExhaustionRung",
    "LadderReading",
    "MabniGenerationError",
    "RequestedBuild",
    "RungStanding",
    "THE_ATTESTED_CARRIERS_EXCEED_THE_DECLARED_ALPHABET_NOTE",
    "THE_CHEAPEST_FIRST_ORDER",
    "THE_HUNDRED_AND_TWELVE_IS_A_CELL_COUNT_NOT_A_SYLLABLE_COUNT_NOTE",
    "THE_LADDER_AT_MEASUREMENT",
    "THE_LONG_VOWEL_COUNT",
    "THE_SHORT_VOWELS",
    "THE_TWELVE_REQUESTED_BUILDS",
    "MABNI_GENERATION_ALGEBRA_NAMED_RESIDUALS",
    "WaznFibreReading",
    "cells_that_are_not_syllables",
    "declared_consonant_count",
    "exhaustion_ladder",
    "licensing_stops_at",
    "template_space",
    "wazn_fibres",
]


class MabniGenerationError(ValueError):
    """خطأُ جبر التوليد: يُرفَع ولا يُبتلَع، ولا يُستبدَل بقيمةٍ افتراضيّة."""


THE_HUNDRED_AND_TWELVE_IS_A_CELL_COUNT_NOT_A_SYLLABLE_COUNT_NOTE: Final[str] = (
    "المئةُ والاثنتا عشرةَ حاصلُ ضربِ حاملٍ في حال، والحالاتُ أربعٌ فيها "
    "السكون؛ والسكونُ عدمُ الحركة فلا يكون نواةً. فثمانٍ وعشرون من الخلايا "
    "ليست مقاطعَ، و`CV` أربعٌ وثمانون."
)

THE_ATTESTED_CARRIERS_EXCEED_THE_DECLARED_ALPHABET_NOTE: Final[str] = (
    "الهمزةُ `ء` حاملٌ مقروءٌ في `p_extractor` وليست من الثمانية والعشرين "
    "المُعلَنة؛ فخلايا أُثبِتَت وهي خارجَ الفضاء المولَّد. وفضاءٌ لا يُخرِج ما "
    "أُثبِتَ عليه فضاءٌ ناقصٌ لا جردٌ تامّ."
)

AN_UNEXHAUSTED_RUNG_LICENSES_NOTHING_ABOVE_IT_NOTE: Final[str] = (
    "شرطُ «الاستنفاد قبل الترخيص» يوقف السُّلَّم عند أوّلِ درجةٍ لم تُستنفَد؛ "
    "ومن رخَّص ما فوقها فقد ترك الشرطَ ولم يُعمِله."
)

A_SHAPE_THAT_CARRIES_SEVEN_HUNDRED_WORDS_SORTS_NOTHING_NOTE: Final[str] = (
    "الدالّةُ من الكلمة إلى وزنها ليست متباينةً على هذه البايتات، فلا مقلوبَ "
    "لها؛ ولا يُستخرَج من الوزن وحدَه بابٌ إعرابًا ولا بناءً."
)

AN_UNDEPOSITED_MATERIAL_IS_A_NAMED_SUSPENSION_NOT_A_DEFAULT_NOTE: Final[str] = (
    "البناءُ الذي تنقصه مادّةٌ موسومةٌ يُسجَّل معلَّقًا باسم مادّته، ولا يُخرَج "
    "منه شيءٌ بالتخمين ولا يُحذَف من الطلب."
)

AN_UNSEGMENTED_WORD_IS_CARRIED_IN_THE_DENOMINATOR_NOTE: Final[str] = (
    "الكلمةُ المتعذِّرةُ محمولةٌ في المقام لا مطروحةٌ منه؛ وطرحُها يرفع كلَّ "
    "نسبةٍ بإخفاء ما لم يُقرأ."
)


THE_SHORT_VOWELS: Final[tuple[str, ...]] = ("َ", "ُ", "ِ")
"""الصوائتُ القصيرةُ ثلاثٌ؛ والسكونُ من `THE_DECLARED_HARAKAT` وليس منها."""

THE_LONG_VOWEL_COUNT: Final[int] = 3
"""الصوائتُ الطويلةُ ثلاثٌ أيضًا: امتدادُ كلِّ حركةٍ من الثلاث، لا أكثر."""


def declared_consonant_count() -> int:
    """عددُ الصوامت المُعلَن، مقروءًا من أبجديّة `letter_haraka_partition`."""

    return len(THE_DECLARED_LETTERS)


def cells_that_are_not_syllables() -> int:
    """كم خليّةً من خلايا الحامل×الحال لا تقع مقطعًا؟ خلايا السكون كلُّها."""

    sukun_states = len(THE_DECLARED_HARAKAT) - len(THE_SHORT_VOWELS)
    if sukun_states < 1:
        raise MabniGenerationError(
            "الحالاتُ المُعلَنةُ لا تزيد على الصوائت القصيرة؛ فالجردُ متبدّل."
        )
    return declared_consonant_count() * sukun_states


THE_CHEAPEST_FIRST_ORDER: Final[tuple[SyllableTemplate, ...]] = (
    SyllableTemplate.CV,
    SyllableTemplate.CVV,
    SyllableTemplate.CVC,
    SyllableTemplate.CVVC,
    SyllableTemplate.CVCC,
    SyllableTemplate.CVVCC,
)
"""ترتيبُ الدرجات من الأرخص إلى الأغلى؛ وهو ترتيبُ السعة لا ترتيبُ الذوق."""


def template_space(template: SyllableTemplate) -> int:
    """سعةُ فضاء القالب: صامتٌ لكلِّ `C`، وصائتٌ واحدٌ للنواة مهما طالت.

    النواةُ تختار من الثلاث سواءٌ أقصرت أم طالت، لأنّ الطويلَ امتدادُ القصير
    لا جنسٌ خامس؛ فـ`CV` و`CVV` متساويتا السعة، وفرقُهما في الزمن لا في العدد.
    """

    if not isinstance(template, SyllableTemplate):
        raise MabniGenerationError("القالبُ عضوٌ في القوالب الستّة المغلقة.")
    consonants = str(template.value).count("C")
    space = declared_consonant_count() ** consonants * len(THE_SHORT_VOWELS)
    return int(space)


class RungStanding(Enum):
    """منزلةُ الدرجة. ليس فيها «مقبولةٌ تقريبًا»؛ والقربُ ليس استنفادًا."""

    EXHAUSTED = "مستنفَدةٌ فيُرخَّص ما فوقها"
    UNEXHAUSTED = "غيرُ مستنفَدةٍ فلا يُرخَّص ما فوقها"
    OVERFLOWS_THE_SPACE = "فائضةٌ على فضائها فالفضاءُ منقوض"
    UNATTESTED_HERE = "لم تُثبَت على هذه البايتات"


@dataclass(frozen=True, slots=True)
class ExhaustionRung:
    """درجةٌ واحدةٌ من السُّلَّم: فضاؤها، ومُثبَتُها، وما أُثبِتَ خارجَ فضائها."""

    template: SyllableTemplate
    space: int
    attested_cells: int
    attested_outside_space: int
    occurrences: int

    def __post_init__(self) -> None:
        if self.space <= 0:
            raise MabniGenerationError("فضاءٌ غيرُ موجبٍ ليس فضاءً.")
        for value in (self.attested_cells, self.attested_outside_space):
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise MabniGenerationError("عددُ الخلايا صحيحٌ غيرُ سالب.")
        if self.attested_outside_space > self.attested_cells:
            raise MabniGenerationError("ما أُثبِتَ خارجَ الفضاء لا يزيد على جملة ما أُثبِت.")

    @property
    def attested_inside_space(self) -> int:
        """المُثبَتُ داخلَ الفضاء وحدَه؛ وهو بسطُ التغطية لا جملةُ المُثبَت."""

        return self.attested_cells - self.attested_outside_space

    @property
    def standing(self) -> RungStanding:
        """منزلةُ الدرجة مُشتَقّةٌ من أرقامها، ولا تُكتَب حقلًا يُملى باليد."""

        if self.attested_cells == 0:
            return RungStanding.UNATTESTED_HERE
        if self.attested_cells > self.space:
            return RungStanding.OVERFLOWS_THE_SPACE
        if self.attested_inside_space >= self.space:
            return RungStanding.EXHAUSTED
        return RungStanding.UNEXHAUSTED

    @property
    def coverage(self) -> float:
        """نسبةُ تغطية الفضاء، وهي داخلُه على سعته لا جملةُ المُثبَت عليها."""

        return self.attested_inside_space / self.space

    @property
    def unfilled_cells(self) -> int:
        """كم خليّةً في الفضاء لم تقع؟ فضلُ الفضاء عمّا أُثبِتَ داخلَه."""

        return self.space - self.attested_inside_space


@dataclass(frozen=True, slots=True)
class LadderReading:
    """قراءةُ السُّلَّم كلِّه: درجاتُه، والمحمولُ المتعذِّرُ في مقامه."""

    rungs: tuple[ExhaustionRung, ...]
    words_read: int
    words_unsegmented: int

    def __post_init__(self) -> None:
        if self.words_read < 0 or self.words_unsegmented < 0:
            raise MabniGenerationError("عددُ الكلمات صحيحٌ غيرُ سالب.")
        if self.words_unsegmented > self.words_read:
            raise MabniGenerationError("المتعذِّرُ لا يزيد على المقروء.")
        seen = [rung.template for rung in self.rungs]
        if seen != list(THE_CHEAPEST_FIRST_ORDER):
            raise MabniGenerationError(
                "السُّلَّمُ يُخرِج القوالبَ الستّةَ كلَّها بترتيب الرخص؛ "
                "وحذفُ درجةٍ لم تُثبَت يرفع التغطيةَ بإخفاء خلوٍّ مقيس."
            )

    @property
    def unsegmented_share(self) -> float:
        """حصّةُ المتعذِّر من المقروء؛ تُعرَض ولا تُطرَح من مقامٍ آخر."""

        if self.words_read == 0:
            raise MabniGenerationError("لا حصّةَ على مقامٍ خالٍ.")
        return self.words_unsegmented / self.words_read


def _cell_of(
    letters: Sequence[LetterReading], syllable: Syllable
) -> tuple[tuple[str, str, int], ...]:
    """خليّةُ المقطع: حاملُ كلِّ شريحةٍ وحالُها وطولُها، بترتيب الشرائح."""

    cell: list[tuple[str, str, int]] = []
    for slot in syllable.slots:
        if slot.letter_index >= len(letters):
            raise MabniGenerationError("شريحةٌ تشير خارجَ وحدات الصورة.")
        unit = letters[slot.letter_index].unit
        cell.append((unit.carrier, unit.state.value, slot.length))
    return tuple(cell)


def _is_outside_the_space(cell: Sequence[tuple[str, str, int]]) -> bool:
    """أخارجَ الفضاء المولَّد هذه الخليّة؟ حاملٌ غيرُ مُعلَنٍ يُخرِجها منه."""

    declared = set(THE_DECLARED_LETTERS)
    return any(carrier not in declared for carrier, _state, _length in cell)


def _read_words(
    words: Iterable[str],
) -> tuple[
    dict[SyllableTemplate, set[tuple[tuple[str, str, int], ...]]],
    dict[SyllableTemplate, set[tuple[tuple[str, str, int], ...]]],
    dict[SyllableTemplate, int],
    dict[str, set[str]],
    int,
    int,
]:
    """قراءةٌ واحدةٌ تُخرِج الخلايا والوقوعات وألياف الوزن والمتعذِّر معًا."""

    cells: dict[SyllableTemplate, set[tuple[tuple[str, str, int], ...]]] = {
        template: set() for template in THE_CHEAPEST_FIRST_ORDER
    }
    outside: dict[SyllableTemplate, set[tuple[tuple[str, str, int], ...]]] = {
        template: set() for template in THE_CHEAPEST_FIRST_ORDER
    }
    occurrences: dict[SyllableTemplate, int] = dict.fromkeys(
        THE_CHEAPEST_FIRST_ORDER, 0
    )
    fibres: dict[str, set[str]] = {}
    read = 0
    unsegmented = 0
    for word in words:
        if not word:
            continue
        read += 1
        try:
            reading = syllabify_surface(word)
        except Exception:  # noqa: BLE001 — تعذُّرُ القراءة محمولٌ لا مطروح
            unsegmented += 1
            continue
        if not reading.syllables:
            unsegmented += 1
            continue
        shape: list[str] = []
        letters = read_surface(word).letters
        for syllable in reading.syllables:
            template = syllable.template
            occurrences[template] += 1
            shape.append(template.value)
            cell = _cell_of(letters, syllable)
            cells[template].add(cell)
            if _is_outside_the_space(cell):
                outside[template].add(cell)
        fibres.setdefault("·".join(shape), set()).add(word)
    return cells, outside, occurrences, fibres, read, unsegmented


def exhaustion_ladder(words: Iterable[str]) -> LadderReading:
    """سُلَّمُ الاستنفاد على كلماتٍ مُمرَّرة، من الأرخص إلى الأغلى.

    القوالبُ الستّةُ كلُّها تخرج ولو لم تُثبَت واحدةٌ منها، لأنّ حذفَ درجةٍ
    خاليةٍ يرفع التغطيةَ بإخفاء خلوٍّ مقيس.
    """

    cells, outside, occurrences, _fibres, read, unsegmented = _read_words(words)
    rungs = tuple(
        ExhaustionRung(
            template=template,
            space=template_space(template),
            attested_cells=len(cells[template]),
            attested_outside_space=len(outside[template]),
            occurrences=occurrences[template],
        )
        for template in THE_CHEAPEST_FIRST_ORDER
    )
    return LadderReading(rungs=rungs, words_read=read, words_unsegmented=unsegmented)


def licensing_stops_at(reading: LadderReading) -> ExhaustionRung | None:
    """أوّلُ درجةٍ لم تُستنفَد؛ وما فوقها غيرُ مُرخَّصٍ بشرط المهمّة نفسِه.

    و`None` لا تُخرَج إلّا إذا استُنفِدت الدرجاتُ كلُّها، وهو ما لم يقع على
    بايتاتٍ مُودَعةٍ ههنا؛ فلا تُقرأ غيابًا للشرط.
    """

    for rung in reading.rungs:
        if rung.standing is not RungStanding.EXHAUSTED:
            return rung
    return None


@dataclass(frozen=True, slots=True)
class WaznFibreReading:
    """قراءةُ ألياف الوزن: كم وزنًا، وكم كلمةً، وأثقلُ ليفٍ وكم مُفردًا فيه."""

    distinct_wazn: int
    distinct_words: int
    heaviest_wazn: str
    heaviest_fibre: int
    singleton_fibres: int

    def __post_init__(self) -> None:
        if self.distinct_wazn <= 0:
            raise MabniGenerationError("لا ألياف بلا وزنٍ واحدٍ على الأقلّ.")
        if self.heaviest_fibre < 1:
            raise MabniGenerationError("ليفٌ بلا كلمةٍ ليس ليفًا.")
        if self.singleton_fibres > self.distinct_wazn:
            raise MabniGenerationError("المُفردُ لا يزيد على جملة الأوزان.")

    @property
    def is_injective(self) -> bool:
        """أمتباينةٌ دالّةُ الوزن؟ لا تكون إلّا إذا كان كلُّ ليفٍ مُفردًا."""

        return self.heaviest_fibre == 1

    @property
    def mean_fibre(self) -> float:
        """متوسّطُ حملِ الوزن الواحد؛ وهو حدُّ أيِّ فرزٍ يُدَّعى من الوزن."""

        return self.distinct_words / self.distinct_wazn


def wazn_fibres(words: Iterable[str]) -> WaznFibreReading:
    """ألياف الوزن على كلماتٍ مُمرَّرة: الوزنُ مفتاحًا والكلماتُ ليفَه."""

    _cells, _outside, _occurrences, fibres, _read, _unsegmented = _read_words(words)
    if not fibres:
        raise MabniGenerationError(
            "لا وزنَ خرج من هذه الكلمات، فلا ليفَ يُقرأ؛ ولا يُخرَج صفرٌ " "مكانَ امتناع."
        )
    heaviest = max(fibres.items(), key=lambda item: (len(item[1]), item[0]))
    return WaznFibreReading(
        distinct_wazn=len(fibres),
        distinct_words=sum(len(fibre) for fibre in fibres.values()),
        heaviest_wazn=heaviest[0],
        heaviest_fibre=len(heaviest[1]),
        singleton_fibres=sum(1 for fibre in fibres.values() if len(fibre) == 1),
    )


class BuildStanding(Enum):
    """منزلةُ البناء المطلوب. ليس فيها «مبنيٌّ تقريبًا» ولا «مؤجَّلٌ بلا سبب»."""

    SUSPENDED_FOR_AN_UNDEPOSITED_MATERIAL = "معلَّقٌ لمادّةٍ غيرِ مُودَعة"
    REFUTED_AS_A_FUNCTION_OF_SHAPE = "منقوضٌ بوصفه دالّةً من الوزن"


@dataclass(frozen=True, slots=True)
class RequestedBuild:
    """بناءٌ مطلوبٌ في المهمّة، بمادّته الناقصة ومنزلته وسببها."""

    name: str
    required_material: str
    standing: BuildStanding
    reason: str

    def __post_init__(self) -> None:
        for field_value in (self.name, self.required_material, self.reason):
            if not field_value.strip():
                raise MabniGenerationError("حقلٌ خالٍ في بناءٍ مطلوبٍ ليس تسجيلًا.")


_SHAPE_IS_NOT_A_FUNCTION = (
    "الوزنُ الواحدُ يحمل مئاتِ الكلمات على البايتات المختومة، فلا دالّةَ "
    "عكسيّةَ منه إلى هذا الباب؛ والنقضُ مقيسٌ بـ`wazn_fibres` لا مُدَّعى."
)
_NO_LABELLED_GRAMMAR = (
    "لا مادّةَ موسومةً مُودَعةً في الشجرة تُسمّي هذا الباب لكلمةٍ بعينها؛ "
    "ومادّتا `nahw_lexicon` غيرُ مُودَعتَين عمدًا، فالبابُ معلَّقٌ باسمه."
)

THE_TWELVE_REQUESTED_BUILDS: Final[tuple[RequestedBuild, ...]] = (
    RequestedBuild(
        name="الحروفُ الوظيفيّةُ والأدوات",
        required_material="جردٌ موسومٌ للأدوات من مادّةٍ نحويّةٍ مُودَعة",
        standing=BuildStanding.SUSPENDED_FOR_AN_UNDEPOSITED_MATERIAL,
        reason=_NO_LABELLED_GRAMMAR,
    ),
    RequestedBuild(
        name="الضمائر",
        required_material="جدولُ ضمائرَ موسومٌ بالشخص والعدد والجنس",
        standing=BuildStanding.SUSPENDED_FOR_AN_UNDEPOSITED_MATERIAL,
        reason=_NO_LABELLED_GRAMMAR,
    ),
    RequestedBuild(
        name="الأسماءُ المبنيّة",
        required_material="وسمُ بناءٍ لكلّ اسمٍ من مادّةٍ نحويّةٍ مُودَعة",
        standing=BuildStanding.SUSPENDED_FOR_AN_UNDEPOSITED_MATERIAL,
        reason=_NO_LABELLED_GRAMMAR,
    ),
    RequestedBuild(
        name="الأفعالُ المبنيّة",
        required_material="وسمُ بناءٍ لكلّ فعلٍ من مادّةٍ نحويّةٍ مُودَعة",
        standing=BuildStanding.SUSPENDED_FOR_AN_UNDEPOSITED_MATERIAL,
        reason=_NO_LABELLED_GRAMMAR,
    ),
    RequestedBuild(
        name="المشتقّات",
        required_material="تصريفٌ موسومٌ يربط الصورةَ بجذرها وصيغتها",
        standing=BuildStanding.SUSPENDED_FOR_AN_UNDEPOSITED_MATERIAL,
        reason=_NO_LABELLED_GRAMMAR,
    ),
    RequestedBuild(
        name="الجامد",
        required_material="تصريفٌ موسومٌ يفصل الجامدَ من المشتقّ",
        standing=BuildStanding.SUSPENDED_FOR_AN_UNDEPOSITED_MATERIAL,
        reason=_NO_LABELLED_GRAMMAR,
    ),
    RequestedBuild(
        name="أزمنةُ الفعل وأحوالُه",
        required_material="وسمُ زمنٍ وحالٍ لكلّ فعلٍ في مدوّنةٍ موسومة",
        standing=BuildStanding.SUSPENDED_FOR_AN_UNDEPOSITED_MATERIAL,
        reason=_NO_LABELLED_GRAMMAR,
    ),
    RequestedBuild(
        name="الأسماءُ المشتقّة",
        required_material="جدولُ صيغٍ موسومٌ بأوزان المشتقّات",
        standing=BuildStanding.SUSPENDED_FOR_AN_UNDEPOSITED_MATERIAL,
        reason=_NO_LABELLED_GRAMMAR,
    ),
    RequestedBuild(
        name="العددُ والعدُّ والمعدود",
        required_material="وسمُ عددٍ وتمييزٍ في مدوّنةٍ موسومة",
        standing=BuildStanding.SUSPENDED_FOR_AN_UNDEPOSITED_MATERIAL,
        reason=_NO_LABELLED_GRAMMAR,
    ),
    RequestedBuild(
        name="التذكيرُ والتأنيث",
        required_material="وسمُ جنسٍ موسومٌ لا علامةٌ تُقرأ وكيلًا عنه",
        standing=BuildStanding.REFUTED_AS_A_FUNCTION_OF_SHAPE,
        reason=_SHAPE_IS_NOT_A_FUNCTION,
    ),
    RequestedBuild(
        name="المعرَّفُ والنكرة",
        required_material="فصلُ `أل` تعريفًا من `أل` وصلًا بوسمٍ لا بصورة",
        standing=BuildStanding.REFUTED_AS_A_FUNCTION_OF_SHAPE,
        reason=_SHAPE_IS_NOT_A_FUNCTION,
    ),
    RequestedBuild(
        name="فرزُ المبنيِّ من المعرَب",
        required_material="وسمُ بناءٍ وإعرابٍ لكلّ كلمةٍ في مدوّنةٍ موسومة",
        standing=BuildStanding.REFUTED_AS_A_FUNCTION_OF_SHAPE,
        reason=_SHAPE_IS_NOT_A_FUNCTION,
    ),
)
"""البناءاتُ الاثنتا عشرة المطلوبة، كلٌّ بمادّتها ومنزلتها؛ لا ثالثةَ عشرةَ."""


THE_LADDER_AT_MEASUREMENT: Final[Mapping[str, tuple[int, int, int, int]]] = {
    "CV": (84, 84, 3, 82992),
    "CVV": (84, 85, 4, 35846),
    "CVC": (2352, 1434, 119, 53046),
    "CVVC": (2352, 75, 2, 1492),
    "CVCC": (65856, 36, 1, 234),
    "CVVCC": (65856, 0, 0, 0),
}
"""السُّلَّمُ وقتَ القياس على المدوّنة المختومة: (فضاء · مُثبَت · خارجه · وقوعات).

منقولٌ لا مولَّدٌ ههنا، لأنّ بايتات المدوّنة لا تُحَلّ في كلّ بيئة؛ ومن حلَّها
يُعيد هذه الأعدادَ بـ`exhaustion_ladder` على رموزها. وخلافُها زحزحةٌ تُعرَض.
"""


MABNI_GENERATION_ALGEBRA_NAMED_RESIDUALS: Final[Mapping[str, str]] = {
    "AN_UNDEPOSITED_MATERIAL_IS_A_NAMED_SUSPENSION_NOT_A_DEFAULT": (
        AN_UNDEPOSITED_MATERIAL_IS_A_NAMED_SUSPENSION_NOT_A_DEFAULT_NOTE
    ),
    "AN_UNEXHAUSTED_RUNG_LICENSES_NOTHING_ABOVE_IT": (
        AN_UNEXHAUSTED_RUNG_LICENSES_NOTHING_ABOVE_IT_NOTE
    ),
    "AN_UNSEGMENTED_WORD_IS_CARRIED_IN_THE_DENOMINATOR": (
        AN_UNSEGMENTED_WORD_IS_CARRIED_IN_THE_DENOMINATOR_NOTE
    ),
    "A_SHAPE_THAT_CARRIES_SEVEN_HUNDRED_WORDS_SORTS_NOTHING": (
        A_SHAPE_THAT_CARRIES_SEVEN_HUNDRED_WORDS_SORTS_NOTHING_NOTE
    ),
    "THE_ATTESTED_CARRIERS_EXCEED_THE_DECLARED_ALPHABET": (
        THE_ATTESTED_CARRIERS_EXCEED_THE_DECLARED_ALPHABET_NOTE
    ),
    "THE_HUNDRED_AND_TWELVE_IS_A_CELL_COUNT_NOT_A_SYLLABLE_COUNT": (
        THE_HUNDRED_AND_TWELVE_IS_A_CELL_COUNT_NOT_A_SYLLABLE_COUNT_NOTE
    ),
}
"""البواقي المُسمّاةُ في هذه الوحدة؛ كلُّ اسمٍ مُصدَّرٌ ومقابلُه نصُّه."""
