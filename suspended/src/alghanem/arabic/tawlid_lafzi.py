"""أدواتُ التوليد اللفظيّ الثلاث بمجالاتها الحصرية، وحدُّ الخروج عن اللغة.

نقل القسمُ المُزوَّد في `usul_section_source_texts` حدًّا فئويًّا صارمًا: التعريبُ
«خاص بأسماء الأشياء... ولا يدخل الألفاظ الدالة على المعاني، ولا الجمل الدالة على
الخيال». فالأدواتُ ثلاثٌ لكلٍّ منها مجالُها الحصريّ — التعريبُ لأسماء الأشياء
والأعلام، والاشتقاقُ للمعاني، والمجازُ للتخييل والتشبيه — وخلطُها هو **الخطأُ
المُسمّى**: أن يُسمَّى شيءٌ ماديٌّ أعجميٌّ باشتقاقٍ من جذرٍ عربيٍّ مغايرٍ بدل
تعريب لفظه.

**والمعيارُ الحادُّ سؤالٌ واحدٌ ثنائيُّ الجواب** (`ForeignBorrowingMode`): أَأُخِذ
**اللفظُ الأعجميُّ نفسُه** فصِيغ على وزنٍ عربيّ — فهو تعريبٌ صحيحٌ ولفظُه عربيّ —
أم أُخِذ **المعنى وحده** فكُسِي بلفظٍ عربيٍّ **من جذرٍ مغاير** — فهو الخطأُ الذي
حكم فيه المنقولُ بأنّ اللفظ «لا يُعتبر من ألفاظ اللغة العربية مطلقاً... فلا تكون
عربية على الإطلاق»؟ و`غير_محسوم` عضوٌ مُصرَّحٌ به لا صمت: جهلُ جهة التوليد
يُعلَن ولا يُحمَل على أحد الطرفين.

**وهذا الحكمُ حكمٌ نصّيٌّ على جهة التوليد، لا شذوذٌ إحصائيّ**
(`OutsideTheLanguageIsNotADistributionalOutlier`): لا يُبنى على توزيعٍ ولا على
ندرةِ ورودٍ ولا على `distributional_probe_report`، ولا يُقلَب فيصير عدُّ
الاستعمالات دليلًا على الانتماء أو الخروج.

**ونفيُ الحقائق الثلاث منقولٌ لا مُشتَقّ**
(`HaqiqaGeneraExhaustionIsQuotedNotDerived`): المنقولُ نفى بنفسه اللغويةَ
والشرعيةَ والعرفيةَ نصًّا، ولم تُستنتَج هذه الثلاثةُ هنا من `HaqiqaGenus` في
`lafz_madlul_relation_formal` ولا أُكمِلت منه. وإنما يُقابَل الاثنان في حارسٍ
يتحقّق أنّ المنقول **سمّى الثلاثةَ جميعًا**، والمقابلةُ تحقُّقُ تغطيةٍ لا
اشتقاقُ حكم.

**والوحدةُ مُسجَّلةٌ غير مُفعَّلة** (`TawlidIsDeclaredNotActivated`): لا تقرؤها
دالّةُ القرار السباعية، ولا تُغيِّر موقفَ بندٍ في بطاقة الجملة، ولا تفتح عضوًا
في مفردةٍ مُجمَّدة. وشواهدُها (هاتف، سيارة، قطار، عربة، مقود) **شواهدُ منقولةٍ
مُسمّاة لا مُدخَلاتُ معجم**: لا تُضاف إلى `ImportedFeatureVocabulary` لأنّ تلك
مُجمَّدةٌ عند مصدرها الأجنبيّ بعدّ صفوفٍ متوقَّع، وإضافةُ صفٍّ إليها تُبطِل بصمةَ
الاستيراد.

**ولا سلطةَ لهذه الوحدة**: لا ولادةَ، ولا حكمَ ولادةٍ، ولا تجميد، ولا `E0`، ولا
تقرؤها بوّابةٌ في `kernel/`، ولا تدخل في `BirthExperimentSpecification`.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from types import MappingProxyType
from typing import Final

from .lafz_madlul_relation_formal import HaqiqaGenus
from .text_key import comparison_key
from .usul_section_source_texts import (
    OUTSIDE_THE_LANGUAGE_EXCERPT,
    TAWLID_TOOLS_DOMAIN_EXCERPT,
)

__all__ = [
    "CITED_LEXEMES_ARE_NOT_VOCABULARY_ROWS_NOTE",
    "CITED_LEXEME_WITNESSES",
    "HAQIQA_GENERA_EXHAUSTION_IS_QUOTED_NOT_DERIVED",
    "OUTSIDE_THE_LANGUAGE_IS_NOT_A_DISTRIBUTIONAL_OUTLIER_NOTE",
    "TAWLID_IS_DECLARED_NOT_ACTIVATED_NOTE",
    "TOOL_EXCLUSIVE_DOMAIN",
    "TOOL_MIXING_IS_THE_NAMED_ERROR_NOTE",
    "CitedLexemeWitness",
    "ForeignBorrowingMode",
    "GeneratedContentKind",
    "GeneratedLexemeStanding",
    "LafzGenerationTool",
    "TawlidLafziError",
    "cited_lexeme_witness_for",
    "required_tool_for",
    "standing_for_borrowing_mode",
    "tool_domain",
]


class TawlidLafziError(ValueError):
    """رُفض مدخلٌ خارج المفردات المغلقة؛ ولا يُحمَل على أقرب حالةٍ مقبولة."""


class LafzGenerationTool(Enum):
    """أدواتُ التوليد اللفظيّ الثلاث المغلقة؛ لا رابعَ لها في هذا النطاق."""

    TARIB = "تعريب"
    ISHTIQAQ = "اشتقاق"
    MAJAZ = "مجاز"


class GeneratedContentKind(Enum):
    """نوعُ المحتوى المُولَّد له لفظ؛ ثلاثيٌّ مغلقٌ يقابل الأدوات واحدًا بواحد."""

    THING_OR_PROPER_NAME = "اسم_شيء_أو_علم"
    MEANING = "معنى"
    IMAGINATION = "تخييل_وتشبيه"


class ForeignBorrowingMode(Enum):
    """جهةُ الأخذ عن الأعجميّ؛ `غير_محسوم` تصريحٌ لا صمت."""

    LAFZ_TAKEN_AND_SHAPED = "أُخِذ_اللفظ_الأعجمي_فصِيغ_على_وزن_عربي"
    MEANING_TAKEN_WITH_ALIEN_ROOT = "أُخِذ_المعنى_فكُسِي_بلفظ_من_جذر_مغاير"
    UNDECIDED = "غير_محسوم"


class GeneratedLexemeStanding(Enum):
    """موقفُ اللفظ المُولَّد؛ ثلاثيٌّ مغلق، ولا عضوَ فيه اسمُه «دخيل جزئي»."""

    ARABIC_BY_CORRECT_TARIB = "تعريب_صحيح_فعربي"
    OUTSIDE_THE_LANGUAGE = "معنى_مأخوذ_بجذر_مغاير_فخارج_اللغة"
    UNDECIDED = "غير_محسوم"


_ToolDomainMap = MappingProxyType[LafzGenerationTool, GeneratedContentKind]

TOOL_EXCLUSIVE_DOMAIN: Final[_ToolDomainMap] = MappingProxyType(
    {
        LafzGenerationTool.TARIB: GeneratedContentKind.THING_OR_PROPER_NAME,
        LafzGenerationTool.ISHTIQAQ: GeneratedContentKind.MEANING,
        LafzGenerationTool.MAJAZ: GeneratedContentKind.IMAGINATION,
    }
)

_DOMAIN_TO_TOOL: Final[dict[GeneratedContentKind, LafzGenerationTool]] = {
    kind: tool for tool, kind in TOOL_EXCLUSIVE_DOMAIN.items()
}

_STANDING_BY_MODE: Final[dict[ForeignBorrowingMode, GeneratedLexemeStanding]] = {
    ForeignBorrowingMode.LAFZ_TAKEN_AND_SHAPED: (
        GeneratedLexemeStanding.ARABIC_BY_CORRECT_TARIB
    ),
    ForeignBorrowingMode.MEANING_TAKEN_WITH_ALIEN_ROOT: (
        GeneratedLexemeStanding.OUTSIDE_THE_LANGUAGE
    ),
    ForeignBorrowingMode.UNDECIDED: GeneratedLexemeStanding.UNDECIDED,
}


TOOL_MIXING_IS_THE_NAMED_ERROR_NOTE: Final[str] = (
    "ToolMixingIsTheNamedError: لكلّ أداةٍ مجالُها الحصريّ، فتُصنَّف العمليةُ "
    "أوّلًا بنوع محتواها — أشيءٌ ماديٌّ أم معنًى مجرّدٌ أم تشبيهٌ — ثمّ يُحكَم "
    "على الأداة؛ واستعمالُ الاشتقاق لتسمية شيءٍ ماديٍّ أعجميٍّ بدل تعريب لفظه "
    "هو بعينه الخطأُ الذي أدان به المنقولُ ألفاظًا محدَثة"
)

OUTSIDE_THE_LANGUAGE_IS_NOT_A_DISTRIBUTIONAL_OUTLIER_NOTE: Final[str] = (
    "OutsideTheLanguageIsNotADistributionalOutlier: الحكمُ بالخروج عن اللغة "
    "حكمٌ نصّيٌّ على جهة التوليد — أَأُخِذ اللفظُ أم المعنى — لا شذوذٌ إحصائيّ "
    "في توزيعٍ ولا ندرةُ ورود؛ فلا يُبنى على `distributional_probe_report` ولا "
    "على عدّ استعمالاتٍ، ولا يُقلَب فيصير كثرةُ الاستعمال دليلَ انتماء"
)

HAQIQA_GENERA_EXHAUSTION_IS_QUOTED_NOT_DERIVED: Final[str] = (
    "HaqiqaGeneraExhaustionIsQuotedNotDerived: نفيُ اللغوية والشرعية والعرفية "
    "معًا منقولٌ بحروف المصدر، لا مُشتَقٌّ هنا من `HaqiqaGenus` ولا مُكمَّلٌ "
    "منه؛ والمقابلةُ بين المنقول والمفردة تحقُّقُ تغطيةٍ لا اشتقاقُ حكم"
)

TAWLID_IS_DECLARED_NOT_ACTIVATED_NOTE: Final[str] = (
    "TawlidIsDeclaredNotActivated: هذه المفرداتُ ودالّاتُها مُسجَّلةٌ غير "
    "مُفعَّلة، على حكم «الترادف خلاف الأصل» بحرفه: لا تقرؤها دالّةُ القرار "
    "السباعية، ولا تُغيِّر موقفَ بندٍ في بطاقة الجملة، ولا تفتح عضوًا في مفردةٍ "
    "مُجمَّدة"
)

CITED_LEXEMES_ARE_NOT_VOCABULARY_ROWS_NOTE: Final[str] = (
    "CitedLexemesAreNotVocabularyRows: الألفاظُ المذكورةُ هنا شواهدُ نقلٍ "
    "مُسمّاةٌ يُقرأ فيها حكمُ المصدر، لا مُدخَلاتُ معجم؛ ولا تُضاف إلى "
    "`ImportedFeatureVocabulary` لأنّ تلك مُجمَّدةٌ عند مصدرها الأجنبيّ بعدّ "
    "صفوفٍ متوقَّع، وإضافةُ صفٍّ إليها تُبطِل بصمةَ الاستيراد"
)


def tool_domain(tool: LafzGenerationTool) -> GeneratedContentKind:
    """مجالُ الأداة الحصريّ؛ ولا أداةَ بلا مجالٍ ولا مجالَ لأداتين."""

    if not isinstance(tool, LafzGenerationTool):
        raise TawlidLafziError("الأداةُ عضوٌ في مفردتها الثلاثية المغلقة.")
    return TOOL_EXCLUSIVE_DOMAIN[tool]


def required_tool_for(kind: GeneratedContentKind) -> LafzGenerationTool:
    """الأداةُ التي يوجبها نوعُ المحتوى؛ والتصنيفُ بالنوع سابقٌ للحكم بالأداة."""

    if not isinstance(kind, GeneratedContentKind):
        raise TawlidLafziError("نوعُ المحتوى عضوٌ في مفردته الثلاثية المغلقة.")
    return _DOMAIN_TO_TOOL[kind]


def standing_for_borrowing_mode(
    mode: ForeignBorrowingMode,
) -> GeneratedLexemeStanding:
    """المعيارُ الحادُّ الوحيد: جهةُ الأخذ تُعيِّن الموقف، ولا ثالثَ يُقدَّر.

    ولا يُقرأ من هذه الدالّة حكمٌ على لفظٍ لم تُعلَن جهةُ أخذه: `غير_محسوم`
    تُعيد `غير_محسوم` ولا تُحمَل على أحد الطرفين.
    """

    if not isinstance(mode, ForeignBorrowingMode):
        raise TawlidLafziError("جهةُ الأخذ عضوٌ في مفردتها الثلاثية المغلقة.")
    return _STANDING_BY_MODE[mode]


@dataclass(frozen=True, slots=True)
class CitedLexemeWitness:
    """لفظٌ محدَثٌ ذُكِر في المنقول، بجهة أخذه وأداته ونوع محتواه وبقاياه."""

    lafz: str
    arabic_root_note: str
    content_kind: GeneratedContentKind
    tool_used: LafzGenerationTool
    borrowing_mode: ForeignBorrowingMode
    named_residuals: tuple[str, ...]

    def __post_init__(self) -> None:
        for value, label in (
            (self.lafz, "اللفظ"),
            (self.arabic_root_note, "بيانُ الجذر العربيّ"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise TawlidLafziError(f"{label} نصٌّ غير فارغ؛ ولا يُترَك صمتًا.")
        if not isinstance(self.content_kind, GeneratedContentKind):
            raise TawlidLafziError("نوعُ المحتوى عضوٌ في مفردته الثلاثية المغلقة.")
        if not isinstance(self.tool_used, LafzGenerationTool):
            raise TawlidLafziError("الأداةُ عضوٌ في مفردتها الثلاثية المغلقة.")
        if not isinstance(self.borrowing_mode, ForeignBorrowingMode):
            raise TawlidLafziError("جهةُ الأخذ عضوٌ في مفردتها الثلاثية المغلقة.")
        if not isinstance(self.named_residuals, tuple) or not self.named_residuals:
            raise TawlidLafziError(
                f"شاهدُ {self.lafz} بلا بقيّةٍ مُسمّاةٍ واحدة؛ وحدودُ النقل "
                "تُسمّى ولا تُترَك للقارئ."
            )
        for residual in self.named_residuals:
            if not isinstance(residual, str) or not residual.strip():
                raise TawlidLafziError("كلُّ بقيّةٍ مُسمّاةٍ مفتاحٌ غيرُ فارغ.")

    @property
    def tool_matches_its_domain(self) -> bool:
        """هل استُعمِلت الأداةُ في مجالها الحصريّ؟ مُشتَقٌّ لا مُعلَنٌ في حقل."""

        return tool_domain(self.tool_used) is self.content_kind

    @property
    def standing(self) -> GeneratedLexemeStanding:
        """موقفُ اللفظ مُشتَقًّا من جهة الأخذ وحدها؛ ولا حقلَ يحمله."""

        return standing_for_borrowing_mode(self.borrowing_mode)


_MEANING_CLOTHED: Final[ForeignBorrowingMode] = (
    ForeignBorrowingMode.MEANING_TAKEN_WITH_ALIEN_ROOT
)

_CITED_RESIDUALS: Final[tuple[str, ...]] = (
    "SECTION_SOURCE_BOOK_IS_NOT_NAMED",
    "CITED_LEXEMES_ARE_NOT_VOCABULARY_ROWS",
    "FOREIGN_ETYMON_IS_NOT_TRANSCRIBED_FROM_THE_SOURCE",
)

_WITNESSES: Final[tuple[CitedLexemeWitness, ...]] = (
    CitedLexemeWitness(
        lafz="هاتف",
        arabic_root_note=(
            "اشتُقّ من الهُتاف على وزن فاعل، ولم يُعرَّب لفظُ الأعجميّ نفسُه؛ "
            "فالجذرُ عربيٌّ مغايرٌ لجذر اللفظ المأخوذ عنه معناه"
        ),
        content_kind=GeneratedContentKind.THING_OR_PROPER_NAME,
        tool_used=LafzGenerationTool.ISHTIQAQ,
        borrowing_mode=_MEANING_CLOTHED,
        named_residuals=_CITED_RESIDUALS,
    ),
    CitedLexemeWitness(
        lafz="سيارة",
        arabic_root_note=(
            "كُسِي معنى الآلة بلفظٍ عربيٍّ من مادة السير، ولم يُعرَّب لفظُ " "الأعجميّ نفسُه"
        ),
        content_kind=GeneratedContentKind.THING_OR_PROPER_NAME,
        tool_used=LafzGenerationTool.ISHTIQAQ,
        borrowing_mode=_MEANING_CLOTHED,
        named_residuals=_CITED_RESIDUALS,
    ),
    CitedLexemeWitness(
        lafz="قطار",
        arabic_root_note=(
            "كُسِي المعنى بلفظٍ عربيٍّ من مادة القَطْر، ولم يُعرَّب لفظُ " "الأعجميّ نفسُه"
        ),
        content_kind=GeneratedContentKind.THING_OR_PROPER_NAME,
        tool_used=LafzGenerationTool.ISHTIQAQ,
        borrowing_mode=_MEANING_CLOTHED,
        named_residuals=_CITED_RESIDUALS,
    ),
    CitedLexemeWitness(
        lafz="عربة",
        arabic_root_note=("كُسِي المعنى بلفظٍ عربيٍّ قائم، ولم يُعرَّب لفظُ الأعجميّ نفسُه"),
        content_kind=GeneratedContentKind.THING_OR_PROPER_NAME,
        tool_used=LafzGenerationTool.ISHTIQAQ,
        borrowing_mode=_MEANING_CLOTHED,
        named_residuals=_CITED_RESIDUALS,
    ),
    CitedLexemeWitness(
        lafz="مقود",
        arabic_root_note=(
            "كُسِي المعنى بلفظٍ عربيٍّ من مادة القَوْد، ولم يُعرَّب لفظُ " "الأعجميّ نفسُه"
        ),
        content_kind=GeneratedContentKind.THING_OR_PROPER_NAME,
        tool_used=LafzGenerationTool.ISHTIQAQ,
        borrowing_mode=_MEANING_CLOTHED,
        named_residuals=_CITED_RESIDUALS,
    ),
)

CITED_LEXEME_WITNESSES: Final[MappingProxyType[str, CitedLexemeWitness]] = (
    MappingProxyType({witness.lafz: witness for witness in _WITNESSES})
)


def cited_lexeme_witness_for(lafz: str) -> CitedLexemeWitness:
    """الشاهدُ بلفظه؛ ولفظٌ غيرُ مُسجَّلٍ يُرَدّ ولا يُحمَل على أقرب شاهد."""

    if not isinstance(lafz, str) or lafz not in CITED_LEXEME_WITNESSES:
        raise TawlidLafziError(
            f"لا شاهدَ منقولًا بهذا اللفظ: {lafz!r}؛ والشواهدُ مُسجَّلةٌ مغلقة."
        )
    return CITED_LEXEME_WITNESSES[lafz]


_FORBIDDEN_FIELD_TOKENS: Final[tuple[str, ...]] = (
    "result",
    "outcome",
    "verdict",
    "birth",
    "certificate",
    "score",
    "fractal",
)


def _assert_no_result_field() -> None:
    """حارسُ استيراد: لا حقلَ نتيجةٍ يتسلّل إلى شاهد النقل لاحقًا."""

    for declared in fields(CitedLexemeWitness):
        lowered = declared.name.lower()
        for token in _FORBIDDEN_FIELD_TOKENS:
            if token in lowered:
                raise TawlidLafziError(
                    f"حقلٌ يحمل نتيجة تسلّل إلى CitedLexemeWitness: "
                    f"{declared.name}؛ والشاهدُ لا نتيجة فيه."
                )


def _assert_quoted_genera_cover_the_vocabulary() -> None:
    """حارسُ تغطيةٍ لا اشتقاقُ حكم: أسمّى المنقولُ الحقائقَ الثلاث جميعًا؟"""

    haystack = comparison_key(OUTSIDE_THE_LANGUAGE_EXCERPT.verbatim_text)
    for genus in HaqiqaGenus:
        if comparison_key(genus.value) not in haystack:
            raise TawlidLafziError(
                f"المنقولُ لا يُسمّي «{genus.value}» بحروفه، فلا يُقرأ منه نفيُ "
                "الحقائق الثلاث جميعًا؛ "
                + HAQIQA_GENERA_EXHAUSTION_IS_QUOTED_NOT_DERIVED
            )


def _assert_tool_names_are_quoted() -> None:
    """حارسُ تغطيةٍ: أوقعت أسماءُ الأدوات الثلاث في نصّها المنقول؟"""

    haystack = comparison_key(TAWLID_TOOLS_DOMAIN_EXCERPT.verbatim_text)
    if comparison_key(LafzGenerationTool.TARIB.value) not in haystack:
        raise TawlidLafziError(
            "النصُّ المنقولُ لا يُسمّي «تعريب» بحروفه، وهو موضعُ الحدّ الأول."
        )


if len(LafzGenerationTool) != len(GeneratedContentKind):  # pragma: no cover - guard
    raise RuntimeError(
        "each generation tool has exactly one exclusive domain: an unmatched "
        "tool or domain would let one tool be used where another is required"
    )
if len(TOOL_EXCLUSIVE_DOMAIN) != len(LafzGenerationTool):  # pragma: no cover - guard
    raise RuntimeError("a generation tool was left without its exclusive domain")
if len(_DOMAIN_TO_TOOL) != len(GeneratedContentKind):  # pragma: no cover - guard
    raise RuntimeError("two generation tools collapse onto one content domain")
if len(_STANDING_BY_MODE) != len(ForeignBorrowingMode):  # pragma: no cover - guard
    raise RuntimeError("a borrowing mode was left without its standing")
if len(GeneratedLexemeStanding) != 3:  # pragma: no cover - guard
    raise RuntimeError(
        "a generated lexeme is Arabic by correct tarib, outside the language, "
        "or undecided: dropping the undecided member would force a verdict on "
        "a lexeme whose generation mode was never established"
    )

_assert_no_result_field()
_assert_quoted_genera_cover_the_vocabulary()
_assert_tool_names_are_quoted()
