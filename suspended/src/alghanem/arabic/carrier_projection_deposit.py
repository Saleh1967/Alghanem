r"""إيداعُ المسقط قبل السلسلة: تسعةٌ وعشرون حاملًا، وحدُّ كلمةٍ، وحافةٌ معرَّفة.

بُنيت خارجَ الشجرة سلسلةُ ماركوف على «الحوامل التسعة والعشرين»، وخرجت منها
أرقامُ معلوماتٍ وأطوالُ ترميز. وهذه الوحدةُ **لا تبني تلك السلسلة ولا تقترب
منها**؛ إنّما تُودِع ما كانت تلك السلسلةُ تفترضه قبلَها ولم يُودَع: **مَن
الحوامل، وأين تنتهي الكلمة، وما الحافة**. فإنّ ما لا يُودَع مسقطُه لا يُقرأ
رقمُه، والحسابُ الصحيحُ على مسقطٍ غيرِ مُودَعٍ عددٌ بلا مرجع.

**أوّلًا: والتسعةُ والعشرون طَيٌّ لا كشف.** لم يُكتَب ههنا جدولٌ جديد. أُخذت
`DECLARED_CARRIERS` من `encoding.carrier_state_candidate` — وهي مُودَعةٌ من
قبلُ ومُعلَنةٌ أنّها **مكتوبةٌ لا مُشتقّة** — ثمّ طُويت ثمانيةُ رسومٍ إلى
أصولها: `أ إ ؤ ئ آ` إلى `ء`، و`ة` إلى `ت`، و`ى` إلى `ي`، و`ٱ` إلى `ا`. فبقي
تسعةٌ وعشرون. فالعددُ نتيجةُ **قرارِ طَيٍّ** يُقرأ في `THE_FOLDING`، ولو طُوي
غيرُه لخرج غيرُه. ومن قرأ «٢٩» خاصّيّةً للعربيّة فقد قرأ في الرقم ما ليس فيه
(`THE_TWENTY_NINE_ARE_A_FOLDING_NOT_A_DISCOVERY`).

**وثانيًا: وحدُّ الكلمة قرارٌ، وهذا القرارُ يختلق ستَّ حواف.** اقتُرح أن تكون
الكلمةُ **ما بين فراغَين**. فقيست القاعدتان على الوديعتَين: القسمةُ على
الفراغ `U+0020` وحدَه، والقسمةُ على كلّ بياض:

| الوديعة | القاعدة | كلمات | حوامل | حواف |
|---|---|---|---|---|
| الفاتحة | فراغٌ وحدَه | 23 | 143 | **120** |
| الفاتحة | كلُّ بياض | **29** | 143 | **114** |
| آيةُ الفتح | فراغٌ وحدَه | 54 | 249 | 195 |
| آيةُ الفتح | كلُّ بياض | 54 | 249 | 195 |

فالفاصلُ بين آيات الفاتحة في هذه الشجرة **سطرٌ جديدٌ لا فراغ**. فقاعدةُ
«ما بين فراغَين» تلحم آخِرَ كلّ آيةٍ بأوّلِ ما بعدها فتصير الكلماتُ ثلاثًا
وعشرين وفيها كلمةٌ طولُها أربعةَ عشرَ حاملًا، وتُولَد **ستُّ حوافَ لا وجودَ
لها في كتابة**: `م←ا` و`ن←ا` و`م←م` و`ن←ء` و`ن←ا` و`م←ص`. وعددُ الحوامل لا
يتحرّك بين القاعدتَين البتّة — فالخلافُ في **الحافة** وحدَها. والقاعدةُ
نفسُها **عديمةُ الأثر على آية الفتح** إذ هي سطرٌ واحد؛ **وقاعدةٌ لا تتحرّك
على نصٍّ ليست بذلك صحيحة**
(`A_WORD_BOUNDARY_IS_A_DECISION_AND_THE_SPACE_RULE_FABRICATES_SIX_EDGES`).

**وثالثًا: والحافةُ جوارٌ داخلَ كلمةٍ لا غير.** حافةُ كلمةٍ فيها `n` حاملًا
`n-1`، ولا تُؤخَذ حافةٌ عبر حدِّ كلمة. فالمرفوضُ **عددُ الكلمات ناقصًا
واحدًا**، ويُنشَر منشورًا لا مسكوتًا عنه: ثمانٍ وعشرون في الفاتحة وثلاثٌ
وخمسون في آية الفتح. ويُتحقَّق من التعريف حسابًا: `الحواف = الحوامل − الكلمات`
في كلّ قياسٍ ههنا، إذ ليس في الوديعتَين كلمةٌ خلت من حامل.

**ورابعًا: وثمنُ المسقط مقيس.** يُسقِط المسقطُ كلَّ حركةٍ وشدّةٍ وألفٍ خنجريّة:
مئةٌ وتسعةَ عشرَ حرفًا في الفاتحة من ستّة أجناس، ومئتان وأربعةٌ في آية الفتح من
ثمانية. وأثرُ ذلك يُقاس لا يُوصَف: في آية الفتح خمسون كلمةً مكتوبةً متمايزة
تصير **سبعًا وأربعين** هيكلًا، إذ تلتقي ثلاثةُ أزواج: `اللَّهُ` و`اللَّهِ`،
و`الْكُفَّارَ` و`الْكُفَّارِ`، و`مِنَ` و`مِنْ`. **والثلاثةُ كلُّها اختلافُ
آخِرٍ لا غير.** وفي الفاتحة لا يلتقي زوجٌ واحد. فالمسقطُ — على هذه البيّنة —
**أصمُّ عن الآخِر**، وهذا خبرٌ عن نصَّين لا قاعدةٌ في العربيّة
(`THE_PROJECTION_IS_DEAF_TO_THE_ENDING_ON_THIS_EVIDENCE`).

**وخامسًا: والتكرارُ يُصنَع لا يُكشَف.** طُلب تتبُّعُ التكرار على نصٍّ صغير،
فهذا هو: تتكرّر في آية الفتح **ثلاثُ** كلماتٍ مكتوبة، ويتكرّر بعد الإسقاط
**خمسةُ** هياكل. فالمسقطُ زاد المتكرِّرَ اثنين لم يكونا مكرَّرَين في الكتابة.
فمن عدَّ التكرارَ على الهياكل فقد عدَّ تكرارَ مسقطِه، لا تكرارَ النصّ.

**وسادسًا: ولا احتمالَ ههنا ولا معلومة.** ليس في هذه الوحدة مصفوفةُ انتقال،
ولا لوغاريتمُ إمكان، ولا إنتروبيا، ولا نموذجٌ يُقارَن بنموذج. وما نُشر خارجَ
الشجرة من `NLL` و`I(C_t;C_{t+1})` و«أدنى ذاكرةٍ مكتملة» **لا يُدخَل إلى ههنا
ولا يُشتقّ منها**؛ إنّما تُودَع أرضُه. ومن أراد سلسلةً فليَبنِها على هذا
المسقط بعد إيداعه، لا قبله
(`NO_PROBABILITY_IS_COMPUTED_HERE_AND_NONE_MAY_BE_READ_IN`).

**وسابعًا: ومدوَّنةُ MASAQ مُسمّاةٌ غيرُ مُودَعة.** الأرقامُ الخارجيّةُ قِيست
على ثمانيةٍ وسبعين ألفَ كلمةٍ من MASAQ، وبايتاتُها ليست في الشجرة — وموضعُها
وبصمتُها مسنونان في `corpora/README.md`. فكلُّ ما ههنا مقيسٌ على **وديعتَين
اثنتَين مجموعُهما ثلاثٌ وثمانون كلمةً**، وهو قَدْرٌ لا يُنتزع منه حكمٌ على
لغة. وما دامت تلك البايتاتُ خارجًا فسلسلتُها تبقى غيرَ مقروءة
(`MASAQ_IS_NAMED_AND_NOT_DEPOSITED_SO_ITS_CHAIN_STAYS_UNREAD`).
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, fields
from enum import Enum
from functools import cache
from typing import Final

from alghanem.arabic.encoding.carrier_state_candidate import DECLARED_CARRIERS
from alghanem.arabic.fath_ayah_source_text import (
    FATH_AYAH_SOURCE_ID,
    FATH_AYAH_SOURCE_TEXT,
)
from alghanem.arabic.fatiha_source_text import FATIHA_SOURCE_ID, FATIHA_SOURCE_TEXT

__all__ = [
    "A_WORD_BOUNDARY_IS_A_DECISION_AND_THE_SPACE_RULE_FABRICATES_SIX_EDGES",
    "CARRIER_PROJECTION_NAMED_RESIDUALS",
    "MASAQ_IS_NAMED_AND_NOT_DEPOSITED_SO_ITS_CHAIN_STAYS_UNREAD",
    "NO_PROBABILITY_IS_COMPUTED_HERE_AND_NONE_MAY_BE_READ_IN",
    "THE_DEPOSITS_PROJECTED",
    "THE_FOLDING",
    "THE_PROJECTION_IS_DEAF_TO_THE_ENDING_ON_THIS_EVIDENCE",
    "THE_TWENTY_NINE_ARE_A_FOLDING_NOT_A_DISCOVERY",
    "CarrierProjectionError",
    "ProjectionCensus",
    "WordBoundary",
    "census_of",
    "collisions_in",
    "deposited_text",
    "edges_of",
    "project_letter",
    "project_word",
    "repeated_skeletons_in",
    "repeated_words_in",
    "the_edges_only_the_space_rule_makes",
    "the_twenty_nine",
    "words_of",
]


class CarrierProjectionError(ValueError):
    """رفضٌ عند الإسقاط: وديعةٌ لا تُعرَف، أو حدٌّ لا يُقرأ، أو مسقطٌ اختلّ."""


# --- البقايا المسمّاة ------------------------------------------------------

THE_TWENTY_NINE_ARE_A_FOLDING_NOT_A_DISCOVERY: Final[str] = (
    "THE_TWENTY_NINE_ARE_A_FOLDING_NOT_A_DISCOVERY: التسعةُ والعشرون ناتجُ "
    "طَيِّ ثمانيةِ رسومٍ إلى أصولها في جدولٍ مكتوبٍ ههنا، مأخوذةً من مجموعةٍ "
    "أُعلِن في موضعها أنّها مكتوبةٌ لا مُشتقّة؛ فليست خاصّيّةً للعربيّة ولا "
    "نتيجةَ قياس، ولو طُوي غيرُ هذا لخرج عددٌ غيرُه"
)

A_WORD_BOUNDARY_IS_A_DECISION_AND_THE_SPACE_RULE_FABRICATES_SIX_EDGES: Final[str] = (
    "A_WORD_BOUNDARY_IS_A_DECISION_AND_THE_SPACE_RULE_FABRICATES_SIX_EDGES: "
    "قاعدةُ «ما بين فراغَين» تختلق ستَّ حوافَ في الفاتحة لأنّ فاصلَ آياتها "
    "سطرٌ جديد، ولا تُحرِّك آيةَ الفتح شيئًا لأنّها سطرٌ واحد؛ فسكونُ قاعدةٍ "
    "على نصٍّ ليس دليلَ صحّتها، وكلُّ رقمٍ ههنا مقرونٌ بحدِّه"
)

THE_PROJECTION_IS_DEAF_TO_THE_ENDING_ON_THIS_EVIDENCE: Final[str] = (
    "THE_PROJECTION_IS_DEAF_TO_THE_ENDING_ON_THIS_EVIDENCE: التقاءاتُ "
    "الهياكل الثلاثةُ في آية الفتح كلُّها اختلافُ آخِرٍ؛ وهذا خبرٌ عن هذين "
    "النصَّين لا قاعدةٌ في الصرف ولا في الإعراب، ولا يُدَّعى أنّ كلَّ التقاءٍ "
    "في نصٍّ آخرَ سيكون كذلك"
)

NO_PROBABILITY_IS_COMPUTED_HERE_AND_NONE_MAY_BE_READ_IN: Final[str] = (
    "NO_PROBABILITY_IS_COMPUTED_HERE_AND_NONE_MAY_BE_READ_IN: لا مصفوفةَ "
    "انتقالٍ ههنا ولا إنتروبيا ولا لوغاريتمَ إمكانٍ ولا مقارنةَ نماذج؛ هذه "
    "أرضُ السلسلة لا السلسلة، وما نُشر خارجَ الشجرة من أرقام لا يُشتقُّ من "
    "هذه الوحدة ولا يُسنَد إليها"
)

MASAQ_IS_NAMED_AND_NOT_DEPOSITED_SO_ITS_CHAIN_STAYS_UNREAD: Final[str] = (
    "MASAQ_IS_NAMED_AND_NOT_DEPOSITED_SO_ITS_CHAIN_STAYS_UNREAD: بايتاتُ "
    "MASAQ خارجَ الشجرة وموضعُها وبصمتُها مسنونان؛ فكلُّ ما ههنا مقيسٌ على "
    "وديعتَين مجموعُهما ثلاثٌ وثمانون كلمة، ولا يُنتزَع من هذا القَدْر حكمٌ "
    "على لغة"
)

CARRIER_PROJECTION_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "THE_TWENTY_NINE_ARE_A_FOLDING_NOT_A_DISCOVERY": (
        THE_TWENTY_NINE_ARE_A_FOLDING_NOT_A_DISCOVERY
    ),
    "A_WORD_BOUNDARY_IS_A_DECISION_AND_THE_SPACE_RULE_FABRICATES_SIX_EDGES": (
        A_WORD_BOUNDARY_IS_A_DECISION_AND_THE_SPACE_RULE_FABRICATES_SIX_EDGES
    ),
    "THE_PROJECTION_IS_DEAF_TO_THE_ENDING_ON_THIS_EVIDENCE": (
        THE_PROJECTION_IS_DEAF_TO_THE_ENDING_ON_THIS_EVIDENCE
    ),
    "NO_PROBABILITY_IS_COMPUTED_HERE_AND_NONE_MAY_BE_READ_IN": (
        NO_PROBABILITY_IS_COMPUTED_HERE_AND_NONE_MAY_BE_READ_IN
    ),
    "MASAQ_IS_NAMED_AND_NOT_DEPOSITED_SO_ITS_CHAIN_STAYS_UNREAD": (
        MASAQ_IS_NAMED_AND_NOT_DEPOSITED_SO_ITS_CHAIN_STAYS_UNREAD
    ),
}


# --- المسقط ----------------------------------------------------------------

THE_FOLDING: Final[dict[str, str]] = {
    "\u0623": "\u0621",  # أ
    "\u0625": "\u0621",  # إ
    "\u0624": "\u0621",  # ؤ
    "\u0626": "\u0621",  # ئ
    "\u0622": "\u0621",  # آ
    "\u0629": "\u062a",  # ة
    "\u0649": "\u064a",  # ى
    "\u0671": "\u0627",  # ٱ
}
"""قرارُ الطَّيِّ مكتوبًا؛ وهو ما يصنع العددَ تسعةً وعشرين لا خاصّيّةُ الخطّ."""


@cache
def the_twenty_nine() -> tuple[str, ...]:
    """الحواملُ بعد الطَّيّ، مُشتقّةً عند القراءة من المجموعة المُودَعة."""

    folded = {THE_FOLDING.get(letter, letter) for letter in DECLARED_CARRIERS}
    return tuple(sorted(folded))


def project_letter(character: str) -> str | None:
    """حاملُ الحرف بعد الطَّيّ، أو `None` إن لم يكن الحرفُ حاملًا أصلًا."""

    folded = THE_FOLDING.get(character, character)
    return folded if folded in the_twenty_nine() else None


def project_word(word: str) -> str:
    """هيكلُ الكلمة: حواملُها على ترتيبها، وما سواها مُسقَطٌ لا مُبدَّل."""

    return "".join(
        carrier for carrier in map(project_letter, word) if carrier is not None
    )


# --- حدُّ الكلمة -----------------------------------------------------------


class WordBoundary(Enum):
    """قاعدتا القسمة؛ كلتاهما تُقاس ولا تُقدَّم إحداهما بغير رقم."""

    SPACE_ONLY = "space-only"
    ANY_WHITESPACE = "any-whitespace"


def words_of(text: str, boundary: WordBoundary) -> tuple[str, ...]:
    """كلماتُ النصّ على القاعدة المطلوبة، والفارغُ مرفوضٌ لا مُبتلَع."""

    if boundary is WordBoundary.SPACE_ONLY:
        parts = text.split(" ")
    elif boundary is WordBoundary.ANY_WHITESPACE:
        parts = text.split()
    else:  # pragma: no cover - الحصرُ مغلقٌ بالتعداد
        raise CarrierProjectionError(f"حدُّ كلمةٍ لا يُعرَف: {boundary!r}.")
    return tuple(part for part in parts if part)


# --- الودائع ---------------------------------------------------------------

THE_DEPOSITS_PROJECTED: Final[tuple[str, ...]] = (
    FATIHA_SOURCE_ID,
    FATH_AYAH_SOURCE_ID,
)
"""الوديعتان المقروءتان ههنا باسمَيهما؛ ولا يُقاس من هذه الوحدة نصٌّ سواهما."""

_TEXTS: Final[dict[str, str]] = {
    FATIHA_SOURCE_ID: FATIHA_SOURCE_TEXT,
    FATH_AYAH_SOURCE_ID: FATH_AYAH_SOURCE_TEXT,
}


def deposited_text(source_id: str) -> str:
    """حروفُ الوديعة باسمها؛ ويُرفَض اسمٌ ليس في الشجرة ولا يُلتمَس خارجَها."""

    if source_id not in _TEXTS:
        raise CarrierProjectionError(
            f"وديعةٌ لا تُعرَف: {source_id!r}؛ ولا يُقرأ نصٌّ من خارج الشجرة."
        )
    return _TEXTS[source_id]


# --- الإحصاء ---------------------------------------------------------------


@dataclass(frozen=True)
class ProjectionCensus:
    """إحصاءُ مسقطٍ واحدٍ على وديعةٍ واحدةٍ بحدٍّ واحد؛ أعدادٌ لا أحكام."""

    source_id: str
    boundary: WordBoundary
    words: int
    carrier_occurrences: int
    edges: int
    boundary_edges_refused: int
    residue_occurrences: int
    residue_kinds: int
    longest_word: int
    distinct_words: int
    distinct_skeletons: int

    def __post_init__(self) -> None:
        if self.edges != self.carrier_occurrences - self.words:
            raise CarrierProjectionError(
                "تعريفُ الحافة اختلّ: الحوافُ ليست الحواملَ ناقصةً الكلمات."
            )
        if self.boundary_edges_refused != self.words - 1:
            raise CarrierProjectionError(
                "المرفوضُ عبر الحدود ليس عددَ الكلمات ناقصًا واحدًا."
            )


@cache
def census_of(source_id: str, boundary: WordBoundary) -> ProjectionCensus:
    """إحصاءُ وديعةٍ بحدٍّ معيَّن، مُشتقًّا من حروفها عند القراءة."""

    text = deposited_text(source_id)
    words = words_of(text, boundary)
    skeletons = tuple(map(project_word, words))
    residue = tuple(
        character
        for character in text
        if not character.isspace() and project_letter(character) is None
    )
    occurrences = sum(len(skeleton) for skeleton in skeletons)
    return ProjectionCensus(
        source_id=source_id,
        boundary=boundary,
        words=len(words),
        carrier_occurrences=occurrences,
        edges=sum(max(0, len(skeleton) - 1) for skeleton in skeletons),
        boundary_edges_refused=len(words) - 1,
        residue_occurrences=len(residue),
        residue_kinds=len(set(residue)),
        longest_word=max(len(skeleton) for skeleton in skeletons),
        distinct_words=len(set(words)),
        distinct_skeletons=len(set(skeletons)),
    )


def edges_of(source_id: str, boundary: WordBoundary) -> tuple[tuple[str, str], ...]:
    """حوافُ الوديعة على الترتيب: جوارُ حاملَين داخلَ كلمةٍ واحدةٍ لا غير."""

    found: list[tuple[str, str]] = []
    for word in words_of(deposited_text(source_id), boundary):
        skeleton = project_word(word)
        found.extend(zip(skeleton, skeleton[1:], strict=False))
    return tuple(found)


def the_edges_only_the_space_rule_makes(
    source_id: str,
) -> tuple[tuple[str, str], ...]:
    """الحوافُ التي يختلقها حدُّ الفراغ وحدَه؛ فارغةٌ حيث لا بياضَ سواه."""

    wider = Counter(edges_of(source_id, WordBoundary.ANY_WHITESPACE))
    narrow = Counter(edges_of(source_id, WordBoundary.SPACE_ONLY))
    extra = narrow - wider
    return tuple(sorted(extra.elements()))


def collisions_in(source_id: str) -> dict[str, tuple[str, ...]]:
    """ما التقى من كلماتٍ مكتوبةٍ متمايزةٍ تحت هيكلٍ واحدٍ بعد الإسقاط."""

    gathered: dict[str, set[str]] = {}
    for word in set(words_of(deposited_text(source_id), WordBoundary.ANY_WHITESPACE)):
        gathered.setdefault(project_word(word), set()).add(word)
    return {
        skeleton: tuple(sorted(written))
        for skeleton, written in sorted(gathered.items())
        if len(written) > 1
    }


def repeated_words_in(source_id: str) -> dict[str, int]:
    """ما تكرّر من الكلمات **مكتوبةً**، بعددِ وقوعه."""

    counted = Counter(words_of(deposited_text(source_id), WordBoundary.ANY_WHITESPACE))
    return {word: total for word, total in sorted(counted.items()) if total > 1}


def repeated_skeletons_in(source_id: str) -> dict[str, int]:
    """ما تكرّر من الهياكل **بعد الإسقاط**، وهو أكثرُ ممّا تكرّر مكتوبًا."""

    counted = Counter(
        project_word(word)
        for word in words_of(deposited_text(source_id), WordBoundary.ANY_WHITESPACE)
    )
    return {skeleton: total for skeleton, total in sorted(counted.items()) if total > 1}


# --- حرّاسُ الاستيراد ------------------------------------------------------


def _assert_no_authority_field() -> None:
    """حارسُ استيراد: لا حقلَ سلطةٍ في الإحصاء، فهو عددٌ لا حكم."""

    named = {field.name for field in fields(ProjectionCensus)}
    forbidden = {"verdict", "licensed", "born", "frozen", "authority", "rank"}
    if named & forbidden:
        raise CarrierProjectionError(f"حقلُ سلطةٍ في إحصاء: {sorted(named & forbidden)}.")


def _assert_the_carriers_are_twenty_nine() -> None:
    """حارسُ استيراد: العددُ مُشتقٌّ ويُتحقَّق منه، ولا يُكتَب في ثابت."""

    carriers = the_twenty_nine()
    if len(carriers) != 29:
        raise CarrierProjectionError(
            f"الطَّيُّ لم يُخرِج تسعةً وعشرين بل {len(carriers)}؛ فالمسقطُ يُراجَع."
        )
    if any(folded not in carriers for folded in THE_FOLDING.values()):
        raise CarrierProjectionError("طَيٌّ إلى أصلٍ ليس حاملًا؛ فالجدولُ مختلّ.")
    if any(written in carriers for written in THE_FOLDING):
        raise CarrierProjectionError("رسمٌ مطويٌّ بقي حاملًا؛ فالطَّيُّ لم يقع.")


def _assert_the_space_rule_fabricates_where_it_is_said_to() -> None:
    """حارسُ استيراد: الاختلاقُ مقيسٌ على الوديعتَين لا مأخوذٌ تسليمًا."""

    if len(the_edges_only_the_space_rule_makes(FATIHA_SOURCE_ID)) != 6:
        raise CarrierProjectionError(
            "لم يختلِق حدُّ الفراغ ستَّ حوافَ في الفاتحة؛ فالدعوى المنشورةُ تُراجَع."
        )
    if the_edges_only_the_space_rule_makes(FATH_AYAH_SOURCE_ID):
        raise CarrierProjectionError(
            "اختلق حدُّ الفراغ حافةً في آية الفتح؛ وهي سطرٌ واحدٌ فلا موضعَ لذلك."
        )


def _assert_the_projection_costs_something() -> None:
    """حارسُ استيراد: ثمنُ المسقط مقيسٌ، والوحدةُ قائمةٌ على وقوعه."""

    if not collisions_in(FATH_AYAH_SOURCE_ID):
        raise CarrierProjectionError("لم يلتقِ هيكلان في آية الفتح؛ فالثمنُ لم يُقَس.")
    if collisions_in(FATIHA_SOURCE_ID):
        raise CarrierProjectionError("التقى هيكلان في الفاتحة؛ والمنشورُ خلافُ ذلك.")


def _assert_no_probability_leaks_in() -> None:
    """حارسُ استيراد: لا اسمَ احتمالٍ في الواجهة، فالبقيّةُ مُلزِمةٌ لا واعظة."""

    banned = ("entropy", "probab", "nll", "likelihood", "markov", "transition_matrix")
    for name in __all__:
        if name in CARRIER_PROJECTION_NAMED_RESIDUALS:
            continue  # البقيّةُ تسمّي الممنوعَ لتمنعه، فلا تُحاكَم باسمه
        lowered = name.lower()
        if any(word in lowered for word in banned):
            raise CarrierProjectionError(f"اسمُ احتمالٍ في واجهة المسقط: {name}.")


def _assert_every_residual_is_named_by_its_key() -> None:
    """حارسُ استيراد: كلُّ بقيّةٍ تبدأ بمفتاحها فلا تُقتَبس منزوعةَ النسبة."""

    for key, text in CARRIER_PROJECTION_NAMED_RESIDUALS.items():
        if not text.startswith(f"{key}: "):
            raise CarrierProjectionError(f"بقيّةٌ لا تبدأ بمفتاحها: {key}.")


_assert_no_authority_field()
_assert_the_carriers_are_twenty_nine()
_assert_the_space_rule_fabricates_where_it_is_said_to()
_assert_the_projection_costs_something()
_assert_no_probability_leaks_in()
_assert_every_residual_is_named_by_its_key()
