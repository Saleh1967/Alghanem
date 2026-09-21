"""توسيعُ مجتمع البحث: علاماتٌ مكتوبةٌ لا يراها القياسُ، لأنّها صارت حروفًا.

وُسِّعت العيّنةُ من قبل، والعيّنةُ توسيعُ **الشواهد**. وههنا يُوسَّع
**المجتمعُ** نفسُه: لا مَن يُسأل، بل ما يُسأل عنه. فقد كان المجتمعُ تسعَ
علاماتٍ فوق مواضعَ مُودَعة، فصار **كلَّ** ما في كتل العربيّة من حروفٍ
وعلامات: `Lo` سبعُمئةٍ وسبعون، و`Mn` مئةٌ وخمس. ووجدنا في المجتمع الموسَّع
ما لم يكن في العيّنة الموسَّعة: **ثغرةً في المسند لا نقصًا في الشواهد**.

**أوّلًا: ثمانيةُ حروفٍ ليست حروفًا بسيطة.** من السبعمئة والسبعين، **ثمانيةٌ**
— أي **0.825%** — لها تفكّكٌ قانونيٌّ في الجدول؛ أي أنّ كلَّ واحدٍ منها
**حاملٌ وعلامةٌ مُلحَمان** في نقطةِ ترميزٍ واحدة:

| الحرف | النقطة | حاملُه | علامتُه المخفيّة |
|---|---|---|---|
| آ | U+0622 | ا | U+0653 مدّة |
| أ | U+0623 | ا | U+0654 همزة فوق |
| ؤ | U+0624 | و | U+0654 |
| إ | U+0625 | ا | U+0655 همزة تحت |
| ئ | U+0626 | ي | U+0654 |
| ۀ ۂ ۓ | U+06C0 06C2 06D3 | ە ہ ے | U+0654 |

والثلاثةُ الأخيرةُ فارسيّةٌ أرديّةٌ لا تقع في المُودَع. فالواقعُ في العربيّة
خمسةٌ، والألفُ قاعدةُ ثلاثةٍ منها — أكثرُ من أيّ حاملٍ آخر.

**وثانيًا: العلاماتُ المخفيّةُ ثلاثٌ، وليست من التسع في شيء.** المدّةُ
والهمزتان كلُّها من `Mn` المئةِ والخمس، فهي علاماتٌ بحكم الجدول؛ ولا واحدةَ
منها في التسع التي بُني عليها `mark_pair_census` و`written_haraka_mark`.
والمجموعتان منفصلتان تقاطعًا، ولا يشترك صنفٌ لاصقٌ بين الأسرتين.

فالنتيجةُ أنّ **علامةً مكتوبةً في البايتات لا يراها أيٌّ من مقاييسنا**، لا
لأنّها استُثنيت بل لأنّها لم تَعُد علامةً في صورة النصّ: صارت داخلَ الحرف.
وهذا عمًى بنيويٌّ لا سهو
(`A_MARK_THAT_BECAME_A_LETTER_IS_INVISIBLE_TO_A_MARK_CENSUS`).

**وثالثًا: وقياسُه على المُودَعَين قاطع.** وقوعاتُ الثلاثِ **قائمةً بنفسها**:
صفرٌ في الفاتحة، وصفرٌ في الفتح — قبل التسوية وبعدها. ووقوعاتُها **مخفيّةً
داخلَ الحروف**: ثلاثٌ وثمانٍ. فالتعدادُ المرئيُّ يقول «صفر» عن إحدى عشرة
علامةً مكتوبة، أي **لا يرى منها شيئًا ألبتّة**.

**ورابعًا: ونقيضُ ما قُرِّر عن التسع.** قُرِّر أنّ أصنافَ التسع اللاصقةَ
متمايزةٌ كلُّها (27–35)، فالترتيبُ داخلَ المزدوج لا يحمل خبرًا. والثلاثُ
**ليست كذلك**: المدّةُ 230، والهمزةُ فوق 230، والهمزةُ تحت 220. فصنفان منها
**متّحدان**، والتسويةُ القانونيّةُ لا تُرتّب المتّحدَين؛ فترتيبُ «مدّة +
همزةٍ فوق» **محفوظٌ يحمل خبرًا**، وهو عينُ نقيض ما صحّ في التسع. فتلك خاصّةُ
تلك التسعِ بأعيانها، لا خاصّةُ العلامات العربيّة
(`THE_ORDER_RULE_PROVED_FOR_THE_NINE_FAILS_IN_THE_WIDER_POPULATION`).

**وخامسًا: والتسويةُ تُلحِم عبرَ الحركة.** `ا + فتحة + همزة` تُخرِج `أ +
فتحة`؛ لأنّ صنفَ الفتحة 30 دون صنف الهمزة 230، فلا يَحجُب. فالحركةُ لا تحمي
الهمزةَ من الالتحام، والترتيبان يُخرِجان الشيءَ نفسَه. أي أنّ **التسويةَ
نفسَها تنقل علامةً من مجرى العلامات إلى داخل الحرف**، عند القراءة لا عند
الكتابة
(`NORMALIZATION_ITSELF_MOVES_A_MARK_OUT_OF_THE_MARK_STREAM`).

**وسادسًا: والحوامل المُلحَمةُ هي كلُّ سبب حساسيّة التسوية.** فعددُ الحوامل
المُلحَمة يساوي فرقَ `NFD` عن `NFC` بالضبط حيث النصُّ عربيٌّ خالص: ثلاثٌ
بثلاث، وثمانٍ بثمانٍ. وينكسر في نثر الشجرة بمقدار **117**، وهو محسوبٌ بتمامه
ولم يُترَك: كلُّه غيرُ عربيّ — رموزُ نفيٍ رياضيّةٌ (≠ 86، ⇏ 15، ↛ 11، وأربعةٌ
مفردة) وحرفان لاتينيّان. فالهُويّةُ تصحّ على الخالص، وانكسارُها مُعلَّلٌ
بالخلط لا مُهمَل
(`THE_IDENTITY_HOLDS_ON_PURE_ARABIC_AND_ITS_BREAK_IS_ACCOUNTED`).

**وسابعًا: والألفُ وحدَها تعبر الحدّ.** من `Mn` المئةِ والخمس، **واحدةٌ
فقط** اسمُها في الجدول فيه كلمةُ `LETTER`: `U+0670 ARABIC LETTER SUPERSCRIPT
ALEF`. فالحدُّ بين الحرف والعلامة ليس حدًّا محكمًا في هذا الجدول، والألفُ
تقع على جانبيه: حرفًا `U+0627` وعلامةً `U+0670`، وقاعدةً لثلاثةٍ من الثمانية.
**ولا يُقرأ من هذا حكمٌ صوتيٌّ ولا صرفيّ**؛ إنّما هو وصفُ موقعِها في جدولٍ
واحد
(`THE_LETTER_MARK_BOUNDARY_IS_A_TABLE_FACT_NOT_A_LINGUISTIC_ONE`).

**وثامنًا: وما لا تُصلحه هذه الوحدة.** هي **تُسمّي** الثغرةَ وتقيسها ولا
تسدّها: لم تُستورَد الثلاثُ إلى `written_haraka_mark`، ولم يُوسَّع
`mark_pair_census` من ستٍّ وثلاثين إلى ستٍّ وستّين. فاستيرادُها قرارٌ يُتّخَذ
على بيّنةٍ لا أثرٌ جانبيٌّ لقياس، وهذا القياسُ هو البيّنة
(`THE_GAP_IS_NAMED_AND_MEASURED_HERE_BUT_NOT_CLOSED`).
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass, fields
from itertools import combinations
from typing import Final

from alghanem.arabic.mark_pair_census import THE_NINE_MARKS
from alghanem.arabic.written_haraka_mark import (
    ARABIC_BLOCK_RANGES,
    UNICODE_VERSION,
    arabic_combining_marks,
    positions_of,
)

MADDAH_ABOVE: Final[str] = "\u0653"
HAMZA_ABOVE: Final[str] = "\u0654"
HAMZA_BELOW: Final[str] = "\u0655"

_LETTER_CATEGORY: Final[str] = "Lo"


class HiddenMarkError(ValueError):
    """رفضٌ عند القياس: مجتمعٌ لا يُشتقّ، أو هُويّةٌ تُدَّعى بلا حساب."""


def arabic_letters() -> tuple[str, ...]:
    """نقاطُ `Lo` في كتل العربيّة؛ وهي مجتمعُ الحروف الموسَّع."""

    return tuple(
        chr(code)
        for low, high in ARABIC_BLOCK_RANGES
        for code in range(low, high + 1)
        if unicodedata.category(chr(code)) == _LETTER_CATEGORY
    )


def _is_canonically_fused(letter: str) -> bool:
    decomposition = unicodedata.decomposition(letter)
    return bool(decomposition) and "<" not in decomposition


def fused_letters() -> tuple[str, ...]:
    """الحروفُ التي هي حاملٌ وعلامةٌ مُلحَمان، مشتقّةً من الجدول لا مكتوبة."""

    return tuple(letter for letter in arabic_letters() if _is_canonically_fused(letter))


def hidden_marks() -> tuple[str, ...]:
    """العلاماتُ الساكنةُ داخلَ الحروف المُلحَمة، مرتَّبةً بنقطتها."""

    found = {
        mark
        for letter in fused_letters()
        for mark in unicodedata.normalize("NFD", letter)[1:]
    }
    return tuple(sorted(found, key=ord))


def hidden_marks_are_disjoint_from_the_nine() -> bool:
    """أبينَ الأسرتين تقاطعٌ؟ فإن كان بطل قولُ «لا تراها التسع»."""

    return not (set(hidden_marks()) & set(THE_NINE_MARKS))


def hidden_marks_are_all_combining() -> bool:
    """أكلُّ مخفيٍّ من `Mn` كتلِ العربيّة؟ فهو علامةٌ بحكم الجدول لا بالدعوى."""

    return set(hidden_marks()) <= set(arabic_combining_marks())


def combining_classes_of(marks: tuple[str, ...]) -> tuple[int, ...]:
    """الأصنافُ اللاصقةُ لأسرةٍ من العلامات، بترتيب ورودها."""

    return tuple(unicodedata.combining(mark) for mark in marks)


def classes_are_pairwise_distinct(marks: tuple[str, ...]) -> bool:
    """أتمايزت أصنافُ الأسرة كلُّها؟ وعليه يدور حكمُ الترتيب."""

    return len(set(combining_classes_of(marks))) == len(marks)


def order_bearing_pairs(marks: tuple[str, ...]) -> tuple[tuple[str, str], ...]:
    """المزدوجاتُ التي يحمل ترتيبُها خبرًا، أي المتّحدةُ الصنف."""

    return tuple(
        (first, second)
        for first, second in combinations(marks, 2)
        if unicodedata.combining(first) == unicodedata.combining(second)
    )


def fusion_passes_through(haraka: str) -> bool:
    """أتلتحم الهمزةُ بالألف عبرَ حركةٍ بينهما؟ يُقاس بالتسوية لا بالظنّ."""

    if unicodedata.combining(haraka) == 0:
        raise HiddenMarkError("الحاجزُ المُختبَرُ علامةٌ لاصقةٌ لا حرف.")
    composed = unicodedata.normalize("NFC", f"\u0627{haraka}{HAMZA_ABOVE}")
    return composed[0] == "\u0623"


def fusion_is_order_indifferent(haraka: str) -> bool:
    """أيُخرِج الترتيبان الشيءَ نفسَه؟ فالحركةُ لا تحجب ولا تُقدَّم."""

    if unicodedata.combining(haraka) == 0:
        raise HiddenMarkError("الحاجزُ المُختبَرُ علامةٌ لاصقةٌ لا حرف.")
    before = unicodedata.normalize("NFC", f"\u0627{haraka}{HAMZA_ABOVE}")
    after = unicodedata.normalize("NFC", f"\u0627{HAMZA_ABOVE}{haraka}")
    return before == after


@dataclass(frozen=True)
class InvisibilityReading:
    """قراءةُ نصٍّ واحد: ما رُئي من الثلاث قائمًا، وما اختفى داخلَ الحروف."""

    scope: str
    standalone: int
    hidden: int
    fused_carriers_also_marked: int

    def __post_init__(self) -> None:
        if not self.scope.strip():
            raise HiddenMarkError("لا بدّ للنطاق من اسمٍ يُنسَب إليه القياس.")
        for value in (self.standalone, self.hidden, self.fused_carriers_also_marked):
            if value < 0:
                raise HiddenMarkError("عددُ وقوعٍ سالبٌ لا يكون.")
        if self.fused_carriers_also_marked > self.hidden:
            raise HiddenMarkError("حواملُ مشكولةٌ أكثرُ من الحوامل نفسِها.")

    @property
    def written(self) -> int:
        """جملةُ ما كُتب من الثلاث في هذا النصّ، ظاهرًا ومخفيًّا."""

        return self.standalone + self.hidden

    @property
    def seen_by_a_mark_census(self) -> int:
        """ما يراه تعدادُ العلامات منها؛ وهو القائمُ بنفسه لا غير."""

        return self.standalone

    @property
    def invisible_share(self) -> float:
        """نصيبُ المخفيِّ من المكتوب، نسبةً مئويّةً محسوبةً عند القراءة."""

        if self.written == 0:
            raise HiddenMarkError("لا نسبةَ لمكتوبٍ معدوم؛ ولا يُفترَض صفرًا.")
        return 100.0 * self.hidden / self.written


def read_invisibility(text: str, scope: str) -> InvisibilityReading:
    """يقرأ نصًّا فيعدّ الظاهرَ من الثلاث والمخفيَّ داخلَ حروفه."""

    three = set(hidden_marks())
    fused = set(fused_letters())
    normalized = unicodedata.normalize("NFC", text)
    standalone = sum(1 for character in normalized if character in three)
    hidden = 0
    also_marked = 0
    for position in positions_of(normalized):
        if position.carrier in fused:
            hidden += 1
            if position.marks:
                also_marked += 1
    return InvisibilityReading(
        scope=scope,
        standalone=standalone,
        hidden=hidden,
        fused_carriers_also_marked=also_marked,
    )


def normalization_delta(text: str) -> int:
    """فرقُ طول `NFD` عن `NFC` بنقاط الترميز؛ وهو ما تُفسّره الحوامل."""

    return len(unicodedata.normalize("NFD", text)) - len(
        unicodedata.normalize("NFC", text)
    )


def foreign_decomposables(text: str) -> int:
    """المتفكّكاتُ القانونيّةُ من خارج حروف العربيّة؛ وبها يُعلَّل الانكسار."""

    arabic_fused = set(fused_letters())
    return sum(
        1
        for character in unicodedata.normalize("NFC", text)
        if _is_canonically_fused(character) and character not in arabic_fused
    )


def the_identity_holds_on(text: str) -> bool:
    """أعدَدُ الحوامل المُلحَمة هو كلُّ فرق التسوية في هذا النصّ؟"""

    reading = read_invisibility(text, "هُويّة")
    return reading.hidden == normalization_delta(text)


def letter_named_marks() -> tuple[str, ...]:
    """نقاطُ `Mn` التي يسمّيها الجدولُ حرفًا؛ وبها يُقاس عبورُ الحدّ."""

    return tuple(
        mark for mark in arabic_combining_marks() if "LETTER" in unicodedata.name(mark)
    )


def fused_bases() -> tuple[tuple[str, int], ...]:
    """حواملُ الثمانيةِ وعددُ ما بُني على كلٍّ منها، من الأكثر فالأكثر."""

    tally: dict[str, int] = {}
    for letter in fused_letters():
        base = unicodedata.normalize("NFD", letter)[0]
        tally[base] = tally.get(base, 0) + 1
    return tuple(sorted(tally.items(), key=lambda entry: (-entry[1], ord(entry[0]))))


A_MARK_THAT_BECAME_A_LETTER_IS_INVISIBLE_TO_A_MARK_CENSUS: Final[str] = (
    "A_MARK_THAT_BECAME_A_LETTER_IS_INVISIBLE_TO_A_MARK_CENSUS: المدّةُ "
    "والهمزتان علاماتٌ من `Mn` كتلِ العربيّة، ولا واحدةَ منها في التسع؛ "
    "ووقوعُها في المُودَعَين قائمةً بنفسها صفرٌ، ومخفيّةً داخلَ الحروف ثلاثٌ "
    "وثمانٍ. فالتعدادُ المرئيُّ لا يرى من إحدى عشرة علامةً مكتوبةً شيئًا، "
    "وهذا عمًى بنيويٌّ في المسند لا نقصٌ في الشواهد."
)

THE_ORDER_RULE_PROVED_FOR_THE_NINE_FAILS_IN_THE_WIDER_POPULATION: Final[str] = (
    "THE_ORDER_RULE_PROVED_FOR_THE_NINE_FAILS_IN_THE_WIDER_POPULATION: أصنافُ "
    "التسع متمايزةٌ كلُّها فلا يحمل ترتيبُ مزدوجها خبرًا؛ وأصنافُ الثلاث "
    "230 و230 و220، فاثنتان متّحدتان لا تُرتّبهما التسوية. فترتيبُ «مدّة + "
    "همزةٍ فوق» محفوظٌ حاملٌ للخبر، وتلك خاصّةُ التسعِ بأعيانها لا خاصّةُ "
    "علامات العربيّة، ولا تُعمَّم على المجتمع الموسَّع."
)

NORMALIZATION_ITSELF_MOVES_A_MARK_OUT_OF_THE_MARK_STREAM: Final[str] = (
    "NORMALIZATION_ITSELF_MOVES_A_MARK_OUT_OF_THE_MARK_STREAM: صنفُ الحركة "
    "دون صنف الهمزة، فلا يَحجُب؛ فـ`ا + فتحة + همزة` تُخرِج `أ + فتحة`، "
    "والترتيبان سواء. فالاختفاءُ ليس صفةَ بايتاتٍ مُودَعةٍ وحدَها، بل تُحدِثه "
    "التسويةُ عند القراءة؛ وكلُّ قياسٍ مُسوّىً يرث هذا الأثر."
)

THE_IDENTITY_HOLDS_ON_PURE_ARABIC_AND_ITS_BREAK_IS_ACCOUNTED: Final[str] = (
    "THE_IDENTITY_HOLDS_ON_PURE_ARABIC_AND_ITS_BREAK_IS_ACCOUNTED: عددُ "
    "الحوامل المُلحَمة يساوي فرقَ NFD عن NFC بالضبط في المُودَعَين: ثلاثٌ "
    "بثلاث وثمانٍ بثمانٍ. وينكسر في نثر الشجرة بمقدار 117، كلُّها متفكّكاتٌ "
    "غيرُ عربيّة؛ فالهُويّةُ مشروطةٌ بخلوص النصّ، وشرطُها مقيسٌ عند القراءة "
    "بـ foreign_decomposables ولا يُفترَض."
)

THE_LETTER_MARK_BOUNDARY_IS_A_TABLE_FACT_NOT_A_LINGUISTIC_ONE: Final[str] = (
    "THE_LETTER_MARK_BOUNDARY_IS_A_TABLE_FACT_NOT_A_LINGUISTIC_ONE: واحدةٌ "
    "من مئةٍ وخمسٍ من `Mn` يسمّيها الجدولُ حرفًا، وهي الألفُ الخنجريّة؛ "
    "والألفُ قاعدةُ ثلاثةٍ من الثمانية. وهذا وصفُ موقعٍ في جدولِ يونيكود "
    "15.0.0 وحدَه، لا حكمَ فيه على صوتٍ ولا صرفٍ ولا رسمٍ عند النحاة."
)

THE_GAP_IS_NAMED_AND_MEASURED_HERE_BUT_NOT_CLOSED: Final[str] = (
    "THE_GAP_IS_NAMED_AND_MEASURED_HERE_BUT_NOT_CLOSED: لم تُستورَد الثلاثُ "
    "إلى written_haraka_mark، ولم يُوسَّع mark_pair_census من ستٍّ وثلاثين "
    "إلى ستٍّ وستّين. فهذه الوحدةُ بيّنةٌ لقرارٍ لم يُتَّخَذ بعدُ، لا "
    "تنفيذٌ له؛ وكلُّ رقمٍ نُشر قبلها عن التسع يبقى صحيحًا عن التسع، محدودًا بها."
)

HIDDEN_MARK_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "A_MARK_THAT_BECAME_A_LETTER_IS_INVISIBLE_TO_A_MARK_CENSUS": (
        A_MARK_THAT_BECAME_A_LETTER_IS_INVISIBLE_TO_A_MARK_CENSUS
    ),
    "THE_ORDER_RULE_PROVED_FOR_THE_NINE_FAILS_IN_THE_WIDER_POPULATION": (
        THE_ORDER_RULE_PROVED_FOR_THE_NINE_FAILS_IN_THE_WIDER_POPULATION
    ),
    "NORMALIZATION_ITSELF_MOVES_A_MARK_OUT_OF_THE_MARK_STREAM": (
        NORMALIZATION_ITSELF_MOVES_A_MARK_OUT_OF_THE_MARK_STREAM
    ),
    "THE_IDENTITY_HOLDS_ON_PURE_ARABIC_AND_ITS_BREAK_IS_ACCOUNTED": (
        THE_IDENTITY_HOLDS_ON_PURE_ARABIC_AND_ITS_BREAK_IS_ACCOUNTED
    ),
    "THE_LETTER_MARK_BOUNDARY_IS_A_TABLE_FACT_NOT_A_LINGUISTIC_ONE": (
        THE_LETTER_MARK_BOUNDARY_IS_A_TABLE_FACT_NOT_A_LINGUISTIC_ONE
    ),
    "THE_GAP_IS_NAMED_AND_MEASURED_HERE_BUT_NOT_CLOSED": (
        THE_GAP_IS_NAMED_AND_MEASURED_HERE_BUT_NOT_CLOSED
    ),
}

_FORBIDDEN_FIELD_TOKENS: Final[tuple[str, ...]] = (
    "authority",
    "born",
    "birth",
    "gate",
    "rank",
    "verdict",
)


def _assert_no_authority_field() -> None:
    """حارسُ استيراد: لا حقلَ سلطةٍ ولا رتبةٍ في قياسٍ لا سلطةَ فيه."""

    for declared in fields(InvisibilityReading):
        lowered = declared.name.lower()
        for token in _FORBIDDEN_FIELD_TOKENS:
            if token in lowered:
                raise HiddenMarkError(
                    "حقلٌ يحمل سلطةً أو رتبةً تسلّل إلى InvisibilityReading: "
                    f"{declared.name}؛ وهذا قياسٌ لا سلطةَ فيه."
                )


def _assert_the_hidden_are_marks_outside_the_nine() -> None:
    """حارسُ استيراد: لو دخلت مخفيّةٌ في التسع بطلت دعوى العمى كلُّها."""

    if not hidden_marks_are_all_combining():
        raise HiddenMarkError(
            f"مخفيٌّ خارج `Mn` كتلِ العربيّة في يونيكود {UNICODE_VERSION}؛ "
            "فلا يصحّ تسميتُه علامةً، ويُعاد النظرُ في الوحدة."
        )
    if not hidden_marks_are_disjoint_from_the_nine():
        raise HiddenMarkError(
            "تقاطعت المخفيّاتُ مع التسع؛ فدعوى «لا يراها التعداد» باطلة."
        )


def _assert_the_wider_population_breaks_the_order_rule() -> None:
    """حارسُ استيراد: هذه الوحدةُ قائمةٌ على نقضٍ، فيُتحقَّق منه لا يُفترَض."""

    if classes_are_pairwise_distinct(hidden_marks()):
        raise HiddenMarkError(
            "تمايزت أصنافُ الثلاث؛ فالنقضُ الذي بُنيت عليه الوحدةُ لم يقع."
        )
    if not classes_are_pairwise_distinct(THE_NINE_MARKS):
        raise HiddenMarkError(
            "لم تتمايز أصنافُ التسع؛ فطرفا المقابلة انهارا ولا مقابلة."
        )


def _assert_every_residual_is_named_by_its_key() -> None:
    """حارسُ استيراد: كلُّ بقيّةٍ تبدأ بمفتاحها فلا تُقتَبس منزوعةَ النسبة."""

    for key, text in HIDDEN_MARK_NAMED_RESIDUALS.items():
        if not text.startswith(f"{key}: "):
            raise HiddenMarkError(f"بقيّةٌ لا تبدأ بمفتاحها: {key}.")


_assert_no_authority_field()
_assert_the_hidden_are_marks_outside_the_nine()
_assert_the_wider_population_breaks_the_order_rule()
_assert_every_residual_is_named_by_its_key()
