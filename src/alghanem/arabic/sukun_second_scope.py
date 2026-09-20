"""نصٌّ ثانٍ للسكون المُضمَر: اتّفاقٌ قريبٌ، وليس نسبةَ مصحف.

خرجت `implicit_sukun_treatment` بنسبةٍ مقيسةٍ على تسعٍ وعشرين كلمةً من
الفاتحة، وسمّت حدَّها بنفسها: `A_RATE_MEASURED_ON_ONE_SURA_IS_NOT_A_CORPUS_RATE`.
وحدُّ النسبة لا يُرفَع بالكلام، وإنّما **بموضعِ قياسٍ ثانٍ**. وفي هذه الشجرة
نصٌّ ثانٍ مُودَعٌ بحروفه: الآيةُ التاسعةُ والعشرون من سورة الفتح
(`fath_ayah_source_text`)، أربعٌ وخمسون كلمة. فأُجري عليها **القياسُ نفسُه
بالمولّد نفسِه**، ووُضع الإحصاءان جنبًا إلى جنب.

| | الفاتحة | الفتح ٢٩ | الفرق |
|---|---|---|---|
| الكلمات | 29 | 54 | |
| الحواملُ الساكنة | 75 | 104 | |
| المكتوبُ منها | 21 | 27 | |
| نصيبُ المكتوب | 28.000% | 25.962% | 2.038 نقطة |

فالنسبةُ **لم تنقلب**: في النصّين جميعًا أكثرُ السكون غيرُ مكتوب، والفارقُ
نقطتان. وأقربُ منه بابُ الألف: نصيبُها من المُضمَر 42.593% هناك و42.857% ههنا،
**ربعُ نقطةٍ بينهما**. وأبعدُها زوجُ الشدّة: 25.926% مقابل 20.779%، خمسُ نقاط.

**والألفُ تكرّرت بتمامها.** في الفتح ثلاثٌ وثلاثون ألفًا مكتوبة، **كلُّها**
بسكونٍ مُضمَر، ولا واحدةَ بعلامةٍ ولا بحركة — كما الثلاثُ والعشرون في
الفاتحة سواءً بسواء. فمجموعُ الشاهد ستٌّ وخمسون ألفًا في نصّين، ولا علامةَ
على واحدةٍ منها. **والألفُ الخنجريّة ليست منها**: وحدتان في الفاتحة وصفرٌ في
الفتح، وهي علامةٌ فوق حرفٍ لا ألفٌ مكتوبة، فتُعدّ على حدةٍ ولا تُمحى. وهذا
**يوسّع
الشاهد ولا يغيّر جنسَه**: ما زال المقروءُ غيابًا يُقرأ من غياب، وتكرارُ
الغياب غيابٌ مُكرَّر لا بايتٌ جديد
(`THE_ALIF_REPLICATION_IS_STILL_READ_FROM_ABSENCE`).

**وموضعُ الابتداء افترق.** بعد رفع الألف: أربعةَ عشرَ ابتداءً ساكنًا في
الفاتحة، خمسةٌ منها مكتوبةٌ (35.714%)؛ واثنا عشرَ في الفتح، ثلاثةٌ مكتوبةٌ
(25.000%). عشرُ نقاطٍ ونصف. فالنصُّ الذي وافق في المجموع خالف في الموضع
الأوّل، وذلك وحدَه ينهى عن حملِ نسبةِ نصٍّ على موضعٍ من آخر. وأمّا المُضمَرُ
من الابتداء فتسعةٌ ههنا وتسعةٌ هناك، بالتقسيم نفسِه (لا ألفَ، وواحدٌ من زوج
شدّة، وثمانيةٌ عارية) — **تطابقُ أعدادٍ صغيرةٍ لا قانون**: تسعةٌ من تسعةٍ
تتطابق بيسر، ولا يُقرأ من التطابق قاعدةٌ لم تُقَس.

**وما لا يُثبِته هذا الاتّفاق.** ثلاثةٌ وثمانون كلمةً من 78,245 — عُشرُ
واحدٍ في المئة من المصحف؛ فالاتّفاقُ توسيعُ سَعةٍ من ألفٍ إلى ألفٍ، لا بلوغُ
نسبةٍ للمصحف (`TWO_TEXTS_ARE_STILL_NOT_A_CORPUS`). والنصّان كلاهما **نقلٌ
كُتب في هذه الشجرة ولم يُقابَل** — رتبتُهما واحدةٌ دُنيا
(`TRANSCRIBED_IN_TREE_NOT_COLLATED`)، وكاتبُهما واحد؛ فاتّفاقُهما اتّفاقُ يدٍ
مع نفسِها، لا شاهدان مستقلّان
(`TWO_TRANSCRIPTIONS_OF_ONE_HAND_ARE_NOT_TWO_WITNESSES`). وقُرئ النصّان
بمولّد الحالات نفسِه؛ فأيُّ ميلٍ في المولّد يحرّك الرقمين معًا، والاتّفاقُ لا
ينفيه بل يُخفيه (`A_SHARED_CODEC_IS_A_SHARED_LIMIT`). ونقطتان بين قياسين
ليستا اتّجاهًا: نقطتان تصنعان خطًّا مهما كان موضعُهما
(`A_GAP_BETWEEN_TWO_SCOPES_IS_NOT_A_TREND`).

**خمولٌ سلطويّ**: لا ولادةَ ولا حكمَ ولا تجميد، ولا استيرادَ من `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Final

from .encoding.carrier_state_candidate import CarrierState, CarrierStateCodec
from .fath_ayah_source_text import FATH_AYAH_SOURCE_TEXT
from .fath_ayah_source_text import (
    TRANSCRIPTION_STANDING as FATH_TRANSCRIPTION_STANDING,
)
from .fatiha_source_text import FATIHA_LINES
from .fatiha_source_text import (
    TRANSCRIPTION_STANDING as FATIHA_TRANSCRIPTION_STANDING,
)
from .implicit_sukun_treatment import (
    THE_ALIF,
    SukunCensus,
    SukunSource,
    census_over,
    measured_onset_census,
    measured_text_census,
    onset_census_over,
    words_of,
)

__all__ = [
    "A_GAP_BETWEEN_TWO_SCOPES_IS_NOT_A_TREND",
    "A_SHARED_CODEC_IS_A_SHARED_LIMIT",
    "FATH_AYAH_LINES",
    "SECOND_SCOPE_NAMED_RESIDUALS",
    "THE_ALIF_REPLICATION_IS_STILL_READ_FROM_ABSENCE",
    "TWO_TEXTS_ARE_STILL_NOT_A_CORPUS",
    "TWO_TRANSCRIPTIONS_OF_ONE_HAND_ARE_NOT_TWO_WITNESSES",
    "AlifReplication",
    "ScopeComparison",
    "SecondScopeError",
    "alif_replication",
    "measured_onset_comparison",
    "measured_text_comparison",
    "second_onset_census",
    "second_text_census",
]

FATH_AYAH_LINES: Final[tuple[str, ...]] = (FATH_AYAH_SOURCE_TEXT,)
"""النصُّ الثاني سطرًا واحدًا، كما أُودِع آيةً واحدة."""

_CODEC: Final[CarrierStateCodec] = CarrierStateCodec()

_FIRST_SCOPE: Final[str] = "الفاتحة"
_SECOND_SCOPE: Final[str] = "الفتح ٢٩"


class SecondScopeError(ValueError):
    """رفضٌ عند المقابلة: موضعٌ يُقابَل بنفسه، أو إحصاءٌ ليس له ما يُقابِله."""


@dataclass(frozen=True)
class ScopeComparison:
    """إحصاءان من موضعين، مقابلان لا مجموعان؛ والفروقُ تُحسَب ولا تُخزَّن."""

    first: SukunCensus
    second: SukunCensus

    def __post_init__(self) -> None:
        if self.first.scope == self.second.scope:
            raise SecondScopeError(
                "موضعٌ يُقابَل بنفسه ليس مقابلةً؛ والمقابلةُ تقتضي موضعين."
            )

    @property
    def written_share_gap(self) -> float:
        """الفرقُ بين نصيبَي المكتوب، بالنقاط المئويّة لا بالنسبة."""

        return self.first.written_share - self.second.written_share

    def unwritten_share_gap(self, source: SukunSource) -> float:
        """الفرقُ بين نصيبَي بابٍ مُضمَرٍ من المُضمَر، بالنقاط المئويّة."""

        return self.first.share_of_unwritten(source) - self.second.share_of_unwritten(
            source
        )

    @property
    def words(self) -> int:
        """كلماتُ الموضعين معًا، وهي سَعةُ ما قِيس لا سَعةُ ما يُعمَّم عليه."""

        return self.first.words + self.second.words

    @property
    def pooled_written_share(self) -> float:
        """نصيبُ المكتوب لو جُمع الموضعان؛ ويُقرأ بحدّه المُسمّى لا وحدَه."""

        total = self.first.total + self.second.total
        if not total:
            raise SecondScopeError("جمعُ نصيبٍ على مجموعٍ خالٍ لا يكون.")
        return 100.0 * (self.first.written + self.second.written) / total

    def rows(self) -> tuple[tuple[str, int, int], ...]:
        """العمودان مفصولين بمصادرهما، موضعًا إلى موضع، لا رقمًا جامعًا."""

        return tuple(
            (
                source.value,
                self.first.count_of(source),
                self.second.count_of(source),
            )
            for source in SukunSource
        )


@dataclass(frozen=True)
class AlifReplication:
    """شهادةُ الألف في موضع: كم ألفًا مكتوبة، وكم منها بحركةٍ أو سكونٍ مرسوم."""

    scope: str
    alifs: int
    marked: int
    dagger_units: int

    def __post_init__(self) -> None:
        if min(self.alifs, self.marked, self.dagger_units) < 0:
            raise SecondScopeError("عدّةٌ سالبةٌ لا تكون.")
        if self.marked > self.alifs:
            raise SecondScopeError("الموسومُ أكثرُ من المعدود؛ وهذا عدٌّ مزدوج.")

    @property
    def unmarked(self) -> int:
        """ما لا يحمل حركةً ولا سكونًا مرسومًا، وهو ما يُقرأ من غياب."""

        return self.alifs - self.marked

    @property
    def is_entirely_unmarked(self) -> bool:
        """أكلُّ ألفٍ مكتوبةٍ ههنا بلا علامة؟ وصفرُ ألفاتٍ ليس شهادة."""

        return self.alifs > 0 and self.marked == 0


def second_text_census() -> SukunCensus:
    """إحصاءُ الفتح ٢٩ كاملًا، مقيسًا عند القراءة لا مكتوبًا في ثابت."""

    return census_over(FATH_AYAH_LINES, scope=f"{_SECOND_SCOPE} — كلُّ المواضع")


def second_onset_census() -> SukunCensus:
    """إحصاءُ سكون الابتداء في الفتح ٢٩، بعد رفع الألف التي لا تحمل علامة."""

    return onset_census_over(
        FATH_AYAH_LINES,
        scope=f"{_SECOND_SCOPE} — الموضع الأوّل بعد رفع ألف الوصل",
    )


def measured_text_comparison() -> ScopeComparison:
    """مقابلةُ النصّين كاملين، إحصاءً بإحصاء."""

    return ScopeComparison(first=measured_text_census(), second=second_text_census())


def measured_onset_comparison() -> ScopeComparison:
    """مقابلةُ موضع الابتداء في النصّين، بعد رفع الألف في كليهما."""

    return ScopeComparison(first=measured_onset_census(), second=second_onset_census())


def _alif_replication_over(lines: tuple[str, ...], scope: str) -> AlifReplication:
    alifs = 0
    marked = 0
    daggers = 0
    for word in words_of(lines):
        for unit in _CODEC.generate(word):
            if unit.carrier != THE_ALIF:
                continue
            if unit.state is CarrierState.DAGGER:
                daggers += 1
                continue
            alifs += 1
            if unit.state is not CarrierState.SUKUN_IMPLICIT:
                marked += 1
    return AlifReplication(
        scope=scope, alifs=alifs, marked=marked, dagger_units=daggers
    )


def alif_replication() -> tuple[AlifReplication, ...]:
    """شهادةُ الألف في الموضعين معًا، كلٌّ باسم موضعه لا مجموعةً في رقم."""

    return (
        _alif_replication_over(FATIHA_LINES, _FIRST_SCOPE),
        _alif_replication_over(FATH_AYAH_LINES, _SECOND_SCOPE),
    )


TWO_TEXTS_ARE_STILL_NOT_A_CORPUS: Final[str] = (
    "TWO_TEXTS_ARE_STILL_NOT_A_CORPUS: قِيس ههنا 83 كلمةً — 29 من الفاتحة و54 "
    "من الفتح — من 78,245 في المدوّنة المقيسة في `quran_corpus_word_total`، "
    "أي 0.106%. فالنصُّ الثاني يرفع السَعةَ من جزءٍ من ألفين إلى جزءٍ من ألف، "
    "ولا يبلغ بها نسبةً للمصحف. وحدُّ `A_RATE_MEASURED_ON_ONE_SURA_IS_NOT_A_"
    "CORPUS_RATE` **مُوسَّعٌ لا مرفوع**."
)

TWO_TRANSCRIPTIONS_OF_ONE_HAND_ARE_NOT_TWO_WITNESSES: Final[str] = (
    "TWO_TRANSCRIPTIONS_OF_ONE_HAND_ARE_NOT_TWO_WITNESSES: النصّان كلاهما عند "
    "رتبة `TRANSCRIBED_IN_TREE_NOT_COLLATED` — نقلٌ كُتب في هذه الشجرة ولم "
    "يُقابَل بطبعةٍ رقميّةٍ ولا بمصحفٍ مطبوع. فما اتّفقا عليه قد يكون عادةَ "
    "الناقل في الشكل لا عادةَ الرسم؛ والمقابلةُ بشاهدٍ خارجَ هذه اليد هي "
    "وحدَها التي تفرّق بينهما، وهي غيرُ مُنجَزةٍ ههنا."
)

A_SHARED_CODEC_IS_A_SHARED_LIMIT: Final[str] = (
    "A_SHARED_CODEC_IS_A_SHARED_LIMIT: قُرئ النصّان بـ`CarrierStateCodec` "
    "نفسِه، وهو الذي يسمّي السكونَ المُضمَر أصلًا. فأيُّ ميلٍ فيه — في زوج "
    "الشدّة أو في الألف — يحرّك الرقمين في جهةٍ واحدة، فيظهر اتّفاقًا بين "
    "نصّين وهو اتّفاقُ أداةٍ مع نفسها. واتّفاقُ قياسين بأداةٍ واحدةٍ لا يشهد "
    "للأداة."
)

THE_ALIF_REPLICATION_IS_STILL_READ_FROM_ABSENCE: Final[str] = (
    "THE_ALIF_REPLICATION_IS_STILL_READ_FROM_ABSENCE: 33 ألفًا مكتوبةً في "
    "الفتح، كلُّها بلا علامةٍ ولا حركة، فوق 23 في الفاتحة: 56 ألفًا في "
    "نصّين، ومعها ألفان خنجريّتان في الفاتحة معدودتان على حدةٍ لأنّهما علامةٌ "
    "لا ألفٌ مكتوبة. وهذا توسيعُ شاهدٍ لا تغييرُ جنسِه — ما زال "
    "`THE_ALIFS_NEUTRALITY_RESTS_ENTIRELY_ON_AN_ABSENCE` قائمًا بحرفه، "
    "وتكرارُ الغياب لا يصير بايتًا."
)

A_GAP_BETWEEN_TWO_SCOPES_IS_NOT_A_TREND: Final[str] = (
    "A_GAP_BETWEEN_TWO_SCOPES_IS_NOT_A_TREND: بين نصيبَي المكتوب 2.038 نقطة، "
    "وبين نصيبَي الابتداء 10.714 نقطة. ونقطتان تصنعان خطًّا مهما كانتا، فلا "
    "يُقرأ من هذين الرقمين ميلٌ ولا اتّجاهٌ ولا تقديرُ ما بينهما: يُقرأ منهما "
    "أنّ النصيبَ في هذين الموضعين بهذين الرقمين، وأنّ الابتداءَ افترق أكثرَ "
    "من المجموع."
)

SECOND_SCOPE_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "TWO_TEXTS_ARE_STILL_NOT_A_CORPUS": TWO_TEXTS_ARE_STILL_NOT_A_CORPUS,
    "TWO_TRANSCRIPTIONS_OF_ONE_HAND_ARE_NOT_TWO_WITNESSES": (
        TWO_TRANSCRIPTIONS_OF_ONE_HAND_ARE_NOT_TWO_WITNESSES
    ),
    "A_SHARED_CODEC_IS_A_SHARED_LIMIT": A_SHARED_CODEC_IS_A_SHARED_LIMIT,
    "THE_ALIF_REPLICATION_IS_STILL_READ_FROM_ABSENCE": (
        THE_ALIF_REPLICATION_IS_STILL_READ_FROM_ABSENCE
    ),
    "A_GAP_BETWEEN_TWO_SCOPES_IS_NOT_A_TREND": A_GAP_BETWEEN_TWO_SCOPES_IS_NOT_A_TREND,
}
"""ما لا يُثبِته هذا الموضعُ الثاني مُسمًّى باسمه، لا مطويًّا في اتّفاقٍ قريب."""

_FORBIDDEN_FIELD_TOKENS: Final[tuple[str, ...]] = (
    "authority",
    "born",
    "birth",
    "gate",
    "rank",
    "verdict",
)


def _assert_no_authority_field() -> None:
    """حارسُ استيراد: لا حقلَ سلطةٍ ولا رتبةٍ في مقابلةٍ لا سلطةَ فيها."""

    for holder in (ScopeComparison, AlifReplication):
        for declared in fields(holder):
            lowered = declared.name.lower()
            for token in _FORBIDDEN_FIELD_TOKENS:
                if token in lowered:
                    raise SecondScopeError(
                        f"حقلٌ يحمل سلطةً أو رتبةً تسلّل إلى {holder.__name__}: "
                        f"{declared.name}؛ وهذه مقابلةٌ لا سلطةَ فيها."
                    )


def _assert_the_two_scopes_keep_one_standing() -> None:
    """حارسُ استيراد: لو ارتفعت رتبةُ أحد النقلين لبطل وصفُ «يدٍ واحدة»."""

    if FATIHA_TRANSCRIPTION_STANDING.value != FATH_TRANSCRIPTION_STANDING.value:
        raise SecondScopeError(
            "افترقت رتبتا النقلين، فوصفُ اتّفاقِهما باتّفاق يدٍ واحدةٍ لم يعد "
            "صادقًا؛ ويُعاد النظرُ في "
            "TWO_TRANSCRIPTIONS_OF_ONE_HAND_ARE_NOT_TWO_WITNESSES قبل أيّ رقم."
        )


def _assert_the_second_text_has_sukun_to_measure() -> None:
    """حارسُ استيراد: نصٌّ ثانٍ بلا سكونٍ مُضمَرٍ ليس موضعَ قياسٍ لهذه المسألة."""

    census = second_text_census()
    if not census.unwritten:
        raise SecondScopeError(
            "لا سكونَ مُضمَرًا في النصّ الثاني، فلا مسألةَ فيه تُقابَل بالأوّل."
        )


_assert_no_authority_field()
_assert_the_two_scopes_keep_one_standing()
_assert_the_second_text_has_sukun_to_measure()
