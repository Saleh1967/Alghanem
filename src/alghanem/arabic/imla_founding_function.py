"""دالّةُ التأسيس: تصنيفٌ إملائيٌّ جامعٌ مانعٌ، ونصفٌ صوتيٌّ نظريٌّ مُشتَقّ.

هذه الوحدةُ تُجيب سؤالًا سابقًا على العدّ كلِّه: **بأيّ حقٍّ يُعَدّ موضعٌ من
النصّ؟** فالعدُّ لا يبدأ إلّا بعد أن يُقسَم المُودَعُ قسمةً لا يسقط منها موضعٌ
ولا يُحسَب موضعٌ مرّتين. وما دون ذلك عدٌّ على رملٍ: يُخرِج رقمًا صحيحَ الحساب
على قسمةٍ لم تُبرهَن.

أوّلًا، الدالّةُ **جامعةٌ**: كلُّ موضعٍ في النصّ يجد بابًا. والبابُ الأخير
`OUTSIDE_THE_DECLARED_TABLE` ليس تمامًا مجّانيًّا بل **بقيّةٌ تُقاس**: إن وقع
فيه موضعٌ واحدٌ من المُودَع لم تُقرأ الدالّةُ جامعةً عليه
(`A_CATCH_ALL_IS_A_MEASURED_RESIDUE_NOT_A_PROOF_OF_TOTALITY`).

ثانيًا، الدالّةُ **مانعةٌ**: لا موضعَ يجد بابين. وهذا مبرهَنٌ **بنيويًّا** لا
بالتجربة: تُجمَع القواعدُ بحرفها، فإمّا قاعدةٌ واحدةٌ مطلقةُ الموضع، وإمّا
قاعدتان تقسمان الموضعَ قسمةً تامّةً (آخرُ الكلمة · ما دونه). وأيُّ خللٍ في
هذه القسمة يُردّ عند الاستيراد لا عند النداء.

ثالثًا، المجالُ المغطّى هو ما اقتضاه الطلبُ بتمامه: الألفُ بصورها (ممدودةٌ ·
وصلٌ · مقصورةٌ · مدّةٌ · خنجريّةٌ)، والهمزةُ **وكرسيُّها** الخمسة (ء · أ · إ ·
ؤ · ئ)، والتاءُ مفتوحةً ومربوطةً، والهاءُ **بموضع الوقف** مفروزةً عن الهاء في
حشو الكلمة، والتنوينُ بأنواعه الثلاثة، والشدّةُ، والحركاتُ الثلاث، والسكون.

رابعًا، الأُسَرُ تتقاطع والأبوابُ لا تتقاطع: فـ«آ» بابٌ واحدٌ وهي في أُسرة
الألف وأُسرة الهمزة معًا. فلا يُقرأ تقاطعُ الأُسَر نقضًا للمنع
(`A_FAMILY_OVERLAP_IS_NOT_A_CLASS_OVERLAP`).

خامسًا، الطيُّ **مقروءٌ لا مصطنَع**: أيُّ بابٍ يَجلس خانةً من الـ116 يُعرَف
بطيّ حرفه بـ`letter_fingerprint.fold_root` ومقابلتِه بالمفردة المُعلَنة. ولا
يُكتَب ههنا طيٌّ ثانٍ (`THE_FOLD_IS_READ_FROM_THE_FINGERPRINT_NOT_REWRITTEN`).

سادسًا — وهو الحدّ — النصفُ الصوتيُّ (مخارجُ وصفات) **نظريٌّ مُشتَقّ** لا
مكتوبُ الحال: يُقرأ من باب الحروف في «الكتاب» لسيبويه ببايتاته المختومة
(`sibawayh_phonetics`)، ويُستوفى إذا أخذ كلُّ حرفٍ تجلسه الأبوابُ مخرجًا وتوقيعَ
صفات، وانقسم الجهرُ والهمسُ قسمةً تامّة، وافترقت حروفُ كلِّ مخرج. وما لم
يُستوفَ يُسمّى ببقيّته المقيسة لا بوقفٍ مكتوب. أمّا **التسجيلُ الصوتيُّ** فمؤجَّلٌ
بقرار المالك خارجَ النطاق، ولا يدخل شرطَ الإمكان ولا يُعلِّق عددًا
(`A_DEFERRED_RECORDING_IS_NOT_A_SUSPENDED_THEORY`). ولا يُقرأ تمامُ النصف
الإملائيّ تمامًا للدالّة (`A_COMPLETE_HALF_IS_NOT_A_COMPLETE_FUNCTION`).

    ADeclaredTable          != ATableTheBytesContain
    AnOrthographicHalf      != AFoundingFunction
    AFamilyOfLetters        != AClassOfPositions
    ACatchAllBranch         != AProofOfTotality

ولا سلطانَ لهذه الوحدة: لا ولادةَ، ولا رفعَ حظر، ولا فكَّ تجميد، ولا استيرادَ
من `kernel/` (`NO_FOUNDING_HERE_LIFTS_A_BLOCK_OR_THAWS_A_FREEZE`).
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from typing import Final

from . import sibawayh_phonetics
from .letter_fingerprint import LETTER_VOCABULARY, fold_root
from .quran_mirror_collation import ayah_rows_of

__all__ = [
    "A_CATCH_ALL_IS_A_MEASURED_RESIDUE_NOT_A_PROOF_OF_TOTALITY",
    "A_COMPLETE_HALF_IS_NOT_A_COMPLETE_FUNCTION",
    "A_FAMILY_OVERLAP_IS_NOT_A_CLASS_OVERLAP",
    "IMLA_FOUNDING_NAMED_RESIDUALS",
    "ImlaClass",
    "ImlaFamily",
    "ImlaFoundingError",
    "ImlaRule",
    "NO_FOUNDING_HERE_LIFTS_A_BLOCK_OR_THAWS_A_FREEZE",
    "PhoneticDimension",
    "PossibilityCondition",
    "Position",
    "THE_EXAMINED_DEPOSIT",
    "THE_FOLD_IS_READ_FROM_THE_FINGERPRINT_NOT_REWRITTEN",
    "THE_IMLA_TABLE",
    "THE_ACOUSTIC_RECORDING_IS_DEFERRED_BY_OWNER_DECISION",
    "THE_PHONETIC_HALF",
    "phonetic_half_reading",
    "class_of",
    "classify",
    "deposit_coverage",
    "exclusivity_reading",
    "families_of",
    "matching_rules",
    "possibility_condition",
    "seating_classes",
    "the_block_and_the_freeze_are_untouched",
]

THE_EXAMINED_DEPOSIT: Final[str] = "quran-simple-enhanced.txt"
"""المُودَعُ الذي تُقاس عليه الجامعيّة؛ والمنعُ مبرهَنٌ قبله لا به."""


class ImlaFoundingError(RuntimeError):
    """خطأُ تأسيسٍ يُرفَع ولا يُتخطّى؛ فالقسمةُ شرطُ العدّ لا زينتُه."""


class Position(Enum):
    """موضعُ الحرف من كلمته؛ وهو ما تحتاجه الهاءُ في الوقف وحدَها ههنا."""

    ANY = "أيُّ موضع"
    WORD_FINAL = "آخرُ الكلمة"
    WITHIN_THE_WORD = "دون آخر الكلمة"


class ImlaFamily(Enum):
    """أُسَرُ الإملاء؛ وهي **تتقاطع** ولا يُقرأ تقاطعُها نقضًا للمنع."""

    ALIF = "الألف"
    HAMZA = "الهمزة وكرسيُّها"
    TA = "التاء"
    HA = "الهاء"
    TANWIN = "التنوين"
    SHADDA = "الشدّة"
    HARAKA = "الحركة"
    SUKUN = "السكون"
    PLAIN_CARRIER = "حاملٌ سائر"
    SEPARATOR = "فاصل"
    MARKUP = "زيادةُ ناشر"
    UNCLASSIFIED = "خارجَ الجدول"


class ImlaClass(Enum):
    """أبوابُ الدالّة؛ وهي **لا تتقاطع**، وموضعٌ واحدٌ لا يجد منها بابين."""

    ALIF_MAMDUDA = "ألفٌ ممدودة"
    ALIF_WASLA = "ألفُ وصل"
    ALIF_MAQSURA = "ألفٌ مقصورة"
    ALIF_MADDA = "ألفُ مدّةٍ حاملةُ همزة"
    DAGGER_ALIF = "ألفٌ خنجريّة"
    HAMZA_ALONE = "همزةٌ مفردةٌ بلا كرسيّ"
    HAMZA_ON_ALIF = "همزةٌ على كرسيّ الألف"
    HAMZA_UNDER_ALIF = "همزةٌ تحت كرسيّ الألف"
    HAMZA_ON_WAW = "همزةٌ على كرسيّ الواو"
    HAMZA_ON_YA = "همزةٌ على كرسيّ الياء"
    TA_MAFTUHA = "تاءٌ مفتوحة"
    TA_MARBUTA = "تاءٌ مربوطة"
    HA_AT_WORD_END = "هاءٌ في آخر الكلمة، يلحقها حكمُ الوقف"
    HA_WITHIN_THE_WORD = "هاءٌ في حشو الكلمة"
    PLAIN_CARRIER = "حاملٌ سائرٌ من المفردة"
    FATHA = "فتحة"
    DAMMA = "ضمّة"
    KASRA = "كسرة"
    SUKUN = "سكون"
    SHADDA = "شدّة"
    TANWIN_FATH = "تنوينُ فتح"
    TANWIN_DAMM = "تنوينُ ضمّ"
    TANWIN_KASR = "تنوينُ كسر"
    OTHER_COMBINING_MARK = "علامةٌ لاحقةٌ أخرى في النطاق العربيّ"
    WORD_SEPARATOR = "فاصلُ كلمة"
    LINE_SEPARATOR = "فاصلُ سطر"
    PUBLISHER_MARKUP = "زيادةُ ناشرٍ ليست من الرسم"
    OUTSIDE_THE_DECLARED_TABLE = "خارجَ الجدول المُعلَن"


@dataclass(frozen=True)
class ImlaRule:
    """قاعدةُ بابٍ: حرفُه وموضعُه وأُسَرُه؛ ولا قاعدةَ بلا حرفٍ مُعلَن."""

    cls: ImlaClass
    codepoints: frozenset[str]
    position: Position
    families: frozenset[ImlaFamily]

    def matches(self, text: str, index: int) -> bool:
        """أتنطبق على هذا الموضع؟ والموضعُ يُقرأ من النصّ لا يُفترَض."""

        char = text[index]
        if char not in self.codepoints:
            return False
        if self.position is Position.ANY:
            return True
        final = _is_word_final(text, index)
        return final if self.position is Position.WORD_FINAL else not final


def _rule(
    cls: ImlaClass,
    chars: str,
    *families: ImlaFamily,
    position: Position = Position.ANY,
) -> ImlaRule:
    return ImlaRule(
        cls=cls,
        codepoints=frozenset(chars),
        position=position,
        families=frozenset(families),
    )


_PLAIN_CARRIERS: Final[str] = "بثجحخدذرزسشصضطظعغفقكلمنوي"
_MARKUP: Final[str] = "<sel>"

THE_IMLA_TABLE: Final[tuple[ImlaRule, ...]] = (
    _rule(ImlaClass.ALIF_MAMDUDA, "\u0627", ImlaFamily.ALIF),
    _rule(ImlaClass.ALIF_WASLA, "\u0671", ImlaFamily.ALIF),
    _rule(ImlaClass.ALIF_MAQSURA, "\u0649", ImlaFamily.ALIF),
    _rule(ImlaClass.ALIF_MADDA, "\u0622", ImlaFamily.ALIF, ImlaFamily.HAMZA),
    _rule(ImlaClass.DAGGER_ALIF, "\u0670", ImlaFamily.ALIF),
    _rule(ImlaClass.HAMZA_ALONE, "\u0621", ImlaFamily.HAMZA),
    _rule(ImlaClass.HAMZA_ON_ALIF, "\u0623", ImlaFamily.HAMZA, ImlaFamily.ALIF),
    _rule(ImlaClass.HAMZA_UNDER_ALIF, "\u0625", ImlaFamily.HAMZA, ImlaFamily.ALIF),
    _rule(ImlaClass.HAMZA_ON_WAW, "\u0624", ImlaFamily.HAMZA),
    _rule(ImlaClass.HAMZA_ON_YA, "\u0626", ImlaFamily.HAMZA),
    _rule(ImlaClass.TA_MAFTUHA, "\u062a", ImlaFamily.TA),
    _rule(ImlaClass.TA_MARBUTA, "\u0629", ImlaFamily.TA, ImlaFamily.HA),
    _rule(
        ImlaClass.HA_AT_WORD_END,
        "\u0647",
        ImlaFamily.HA,
        position=Position.WORD_FINAL,
    ),
    _rule(
        ImlaClass.HA_WITHIN_THE_WORD,
        "\u0647",
        ImlaFamily.HA,
        position=Position.WITHIN_THE_WORD,
    ),
    _rule(ImlaClass.PLAIN_CARRIER, _PLAIN_CARRIERS, ImlaFamily.PLAIN_CARRIER),
    _rule(ImlaClass.FATHA, "\u064e", ImlaFamily.HARAKA),
    _rule(ImlaClass.DAMMA, "\u064f", ImlaFamily.HARAKA),
    _rule(ImlaClass.KASRA, "\u0650", ImlaFamily.HARAKA),
    _rule(ImlaClass.SUKUN, "\u0652", ImlaFamily.SUKUN),
    _rule(ImlaClass.SHADDA, "\u0651", ImlaFamily.SHADDA),
    _rule(ImlaClass.TANWIN_FATH, "\u064b", ImlaFamily.TANWIN),
    _rule(ImlaClass.TANWIN_DAMM, "\u064c", ImlaFamily.TANWIN),
    _rule(ImlaClass.TANWIN_KASR, "\u064d", ImlaFamily.TANWIN),
    _rule(ImlaClass.WORD_SEPARATOR, " ", ImlaFamily.SEPARATOR),
    _rule(ImlaClass.LINE_SEPARATOR, "\n\r", ImlaFamily.SEPARATOR),
    _rule(ImlaClass.PUBLISHER_MARKUP, _MARKUP, ImlaFamily.MARKUP),
)
"""جدولُ الأبواب المُعلَن؛ وما لم يُسمَّ فيه لا يُصنَّف ضمنًا بل يُسمّى بقيّةً."""


class PhoneticDimension(Enum):
    """نصيفُ الدالّة الصوتيُّ: بُعداه مُعلَنان، وقيمتاهما **موقوفتان**."""

    MAKHRAJ = "المخرج"
    SIFA = "الصفة"


THE_PHONETIC_HALF: Final[tuple[PhoneticDimension, ...]] = (
    PhoneticDimension.MAKHRAJ,
    PhoneticDimension.SIFA,
)
"""النصفُ الصوتيّ: يُسمّى ولا يُقاس، فالتسجيلُ موقوفٌ والاختبارُ نصٌّ إلى نصّ."""

THE_ACOUSTIC_RECORDING_IS_DEFERRED_BY_OWNER_DECISION: Final[str] = (
    "التسجيلُ الصوتيُّ وضابطُ السمع مؤجَّلان بقرار المالك خارجَ النطاق؛ والمقيسُ "
    "ههنا علمُ الصوت النظريُّ المنقول، فلا يدخل التأجيلُ شرطَ الإمكان."
)
"""التأجيلُ بقرارٍ مُسمًّى: يُحمَل مع الحال ولا يُعلِّقها."""


def _is_word_final(text: str, index: int) -> bool:
    """أهذا الحرفُ آخرُ كلمته؟ والتاليةُ علاماتٌ لاحقةٌ لا تُزحزح الآخريّة."""

    for char in text[index + 1 :]:
        if unicodedata.category(char) == "Mn":
            continue
        return not char.isalpha()
    return True


def matching_rules(text: str, index: int) -> tuple[ImlaRule, ...]:
    """كلُّ قاعدةٍ تنطبق على الموضع؛ وتُعاد كلُّها ليُرى الجمعُ والمنعُ عدًّا."""

    if not 0 <= index < len(text):
        raise ImlaFoundingError("موضعٌ خارجَ النصّ لا يُصنَّف.")
    return tuple(rule for rule in THE_IMLA_TABLE if rule.matches(text, index))


def classify(text: str, index: int) -> ImlaClass:
    """بابُ الموضع الواحد؛ والبابان خطأُ تأسيسٍ يُرفَع ولا يُرجَّح أحدُهما.

    وغيابُ البابِ ليس خطأً بل **بقيّةٌ مُسمّاة**: يخرج الموضعُ في
    `OUTSIDE_THE_DECLARED_TABLE` ليُعَدّ، لا ليُسكَت عنه.
    """

    rules = matching_rules(text, index)
    if len(rules) > 1:
        names = " · ".join(rule.cls.name for rule in rules)
        raise ImlaFoundingError(f"موضعٌ وجد بابين فأكثر: {names}؛ المنعُ منتقَض.")
    if not rules:
        return ImlaClass.OUTSIDE_THE_DECLARED_TABLE
    return rules[0].cls


def class_of(char: str, *, word_final: bool = False) -> ImlaClass:
    """بابُ حرفٍ مفردٍ بموضعٍ مُعلَن؛ ميسَّرٌ للفحص لا بديلٌ عن قراءة النصّ."""

    if len(char) != 1:
        raise ImlaFoundingError("حرفٌ واحدٌ لا سلسلةٌ.")
    text = char if word_final else char + "\u0628"
    return classify(text, 0)


def families_of(cls: ImlaClass) -> frozenset[ImlaFamily]:
    """أُسَرُ بابٍ؛ وقد تكون أكثرَ من واحدةٍ كما في «آ» ألفًا وهمزةً."""

    for rule in THE_IMLA_TABLE:
        if rule.cls is cls:
            return rule.families
    return frozenset({ImlaFamily.UNCLASSIFIED})


@lru_cache(maxsize=1)
def seating_classes() -> tuple[ImlaClass, ...]:
    """الأبوابُ التي تجلس خانةً من الـ116، **بطيٍّ مقروءٍ** من البصمة لا مكتوب."""

    vocabulary = set(LETTER_VOCABULARY)
    seats: list[ImlaClass] = []
    for rule in THE_IMLA_TABLE:
        if not rule.families & {
            ImlaFamily.ALIF,
            ImlaFamily.HAMZA,
            ImlaFamily.TA,
            ImlaFamily.HA,
            ImlaFamily.PLAIN_CARRIER,
        }:
            continue
        folded = {fold_root(char) for char in rule.codepoints}
        if folded and folded <= vocabulary:
            seats.append(rule.cls)
    return tuple(seats)


@dataclass(frozen=True)
class ExclusivityReading:
    """قراءةُ المنع: مبرهَنٌ بنيويًّا على الجدول، لا مستقرَأٌ من نصّ."""

    codepoints_declared: int
    codepoints_split_by_position: int
    overlapping_codepoints: tuple[str, ...]

    @property
    def is_exclusive(self) -> bool:
        """المنعُ: لا حرفَ يجد بابين في موضعٍ واحد."""

        return not self.overlapping_codepoints


def exclusivity_reading() -> ExclusivityReading:
    """برهانُ المنع: لكلّ حرفٍ إمّا بابٌ مطلقٌ، وإمّا بابان يقسمان الموضع."""

    by_char: dict[str, list[ImlaRule]] = {}
    for rule in THE_IMLA_TABLE:
        for char in rule.codepoints:
            by_char.setdefault(char, []).append(rule)
    overlapping: list[str] = []
    split = 0
    for char, rules in sorted(by_char.items()):
        positions = [rule.position for rule in rules]
        if len(rules) == 1 and positions[0] is Position.ANY:
            continue
        if len(rules) == 2 and set(positions) == {
            Position.WORD_FINAL,
            Position.WITHIN_THE_WORD,
        }:
            split += 1
            continue
        overlapping.append(char)
    return ExclusivityReading(
        codepoints_declared=len(by_char),
        codepoints_split_by_position=split,
        overlapping_codepoints=tuple(overlapping),
    )


@dataclass(frozen=True)
class CoverageReading:
    """قراءةُ الجمع على مُودَعٍ: كم موضعًا وجد بابًا، وكم بقي بلا باب."""

    positions: int
    classified: int
    unclassified: int
    classes_seen: int

    @property
    def is_total(self) -> bool:
        """الجمعُ: لا موضعَ بلا باب؛ والبقيّةُ تُعَدّ ولا تُقرَّب."""

        return self.unclassified == 0


@lru_cache(maxsize=2)
def deposit_coverage(name: str = THE_EXAMINED_DEPOSIT) -> CoverageReading:
    """قياسُ الجمع على بايتاتٍ مختومةٍ؛ وصفوفُ الآيات وحدَها هي المقروء."""

    text = "\n".join(ayah_rows_of(name))
    seen: set[ImlaClass] = set()
    unclassified = 0
    for index in range(len(text)):
        cls = classify(text, index)
        seen.add(cls)
        if cls is ImlaClass.OUTSIDE_THE_DECLARED_TABLE:
            unclassified += 1
    return CoverageReading(
        positions=len(text),
        classified=len(text) - unclassified,
        unclassified=unclassified,
        classes_seen=len(seen),
    )


class HalfStanding(Enum):
    """منزلةُ نصفٍ من الدالّة؛ والوقفُ منزلةٌ مُسمّاةٌ لا سكوت."""

    MET = "مستوفًى"
    SUSPENDED = "موقوف"
    UNMET_WITH_A_MEASURED_RESIDUE = "غيرُ مستوفًى ببقيّةٍ مقيسة"
    SOURCE_NOT_RESOLVABLE = "مصدرُه غيرُ حاضرٍ مختومًا"


@dataclass(frozen=True)
class PossibilityCondition:
    """شرطُ الإمكان للعدّ والبرهان: نصفان، ولا يُستوفى بأحدهما.

    فاستيفاءُ النصف الإملائيّ وحدَه **لا يُرخّص** العدَّ الصوتيّ ولا يُرقّي
    الدالّةَ إلى تأسيسٍ تامّ؛ وهذا هو
    `A_COMPLETE_HALF_IS_NOT_A_COMPLETE_FUNCTION` بعينه.
    """

    orthographic_half: HalfStanding
    phonetic_half: HalfStanding
    phonetic_residue: tuple[str, ...]
    completion_conditions: tuple[str, ...]
    deferred_out_of_scope: str = THE_ACOUSTIC_RECORDING_IS_DEFERRED_BY_OWNER_DECISION

    @property
    def is_met(self) -> bool:
        """أيُرخَّص العدُّ والبرهان؟ لا، ما دام نصفٌ موقوفًا أو ناقصًا."""

        return (
            self.orthographic_half is HalfStanding.MET
            and self.phonetic_half is HalfStanding.MET
        )

    @property
    def unmet_halves(self) -> tuple[str, ...]:
        """ما لم يُستوفَ بأسمائه؛ فلا يُقال «معلَّق» بلا تسميةِ المعلَّق."""

        unmet: list[str] = []
        if self.orthographic_half is not HalfStanding.MET:
            unmet.append(f"النصفُ الإملائيّ: {self.orthographic_half.value}")
        if self.phonetic_half is not HalfStanding.MET:
            named = "؛ ".join(self.phonetic_residue)
            unmet.append(f"النصفُ الصوتيّ النظريّ: {self.phonetic_half.value} — {named}")
        return tuple(unmet)


def possibility_condition(name: str = THE_EXAMINED_DEPOSIT) -> PossibilityCondition:
    """شرطُ الإمكان مُشتَقًّا: منعٌ بنيويٌّ وجمعٌ مقيسٌ، ونصفٌ صوتيٌّ موقوف."""

    coverage = deposit_coverage(name)
    exclusivity = exclusivity_reading()
    orthographic = (
        HalfStanding.MET
        if coverage.is_total and exclusivity.is_exclusive
        else HalfStanding.UNMET_WITH_A_MEASURED_RESIDUE
    )
    phonetic, residue, conditions = phonetic_half_reading()
    return PossibilityCondition(
        orthographic_half=orthographic,
        phonetic_half=phonetic,
        phonetic_residue=residue,
        completion_conditions=conditions,
    )


def phonetic_half_reading() -> tuple[HalfStanding, tuple[str, ...], tuple[str, ...]]:
    """حالُ النصف الصوتيّ النظريّ مُشتقّةً بالتشغيل، وبقيّتُها، وشروطُ سدّها.

    يُستوفى إذا أخذ **كلُّ حرفٍ تجلسه الأبوابُ** مخرجًا من باب سيبويه، وانقسم
    الجهرُ والهمسُ قسمةً تامّةً مطابقةً للمنصوص، وافترقت حروفُ كلِّ مخرجٍ
    بتواقيع صفاتها. والتسجيلُ الصوتيُّ لا يدخل هذا الشرط.
    """

    if not sibawayh_phonetics.source_is_resolvable():
        return (
            HalfStanding.SOURCE_NOT_RESOLVABLE,
            ("بايتاتُ «الكتاب» لسيبويه غيرُ حاضرةٍ مختومة",),
            (
                "إحضارُ KITAB_SIBAWAYH بطوله وبصمته عبر "
                f"{sibawayh_phonetics.THE_SOURCE.path_environment_variable}",
            ),
        )
    reading = sibawayh_phonetics.reading()
    seated = {
        fold_root(char) or char
        for rule in THE_IMLA_TABLE
        if rule.cls in seating_classes()
        for char in rule.codepoints
    }
    residue: list[str] = []
    conditions: list[str] = []
    missing = [
        letter for letter in reading.letters_without_a_makhraj if letter in seated
    ]
    if missing:
        residue.append("حروفٌ بلا مخرجٍ في النصّ المودَع: " + " ".join(missing))
        conditions.append("مقابلةُ جملةِ المخرج الساقطة بصفحةٍ مطبوعةٍ مُودَعةٍ بختمها")
    unsigned = sorted(letter for letter in seated if not reading.signature(letter))
    if unsigned:
        residue.append("حروفٌ بلا توقيعِ صفة: " + " ".join(unsigned))
        conditions.append("استخراجُ صفاتها من مرساةٍ في الباب نفسه")
    if not reading.voicing_is_a_partition:
        residue.append("الجهرُ والهمسُ لا يقسمان المفردةَ قسمةً تامّة")
        conditions.append("مراجعةُ مرساتَي الجهر والهمس على النصّ")
    if reading.unseparated_cells:
        residue.append("خاناتُ مخرجٍ لا تفترق حروفُها بصفاتها")
        conditions.append("صفةٌ فاصلةٌ من شاهدٍ ثانٍ مسمّى")
    if not residue:
        return HalfStanding.MET, (), ()
    return (
        HalfStanding.UNMET_WITH_A_MEASURED_RESIDUE,
        tuple(residue),
        tuple(conditions),
    )


A_FAMILY_OVERLAP_IS_NOT_A_CLASS_OVERLAP: Final[str] = (
    "A_FAMILY_OVERLAP_IS_NOT_A_CLASS_OVERLAP: «آ» في أُسرة الألف وأُسرة الهمزة "
    "معًا وهي بابٌ واحد؛ فتقاطعُ الأُسَر لا يُقرأ نقضًا لمنع الأبواب."
)

A_CATCH_ALL_IS_A_MEASURED_RESIDUE_NOT_A_PROOF_OF_TOTALITY: Final[str] = (
    "A_CATCH_ALL_IS_A_MEASURED_RESIDUE_NOT_A_PROOF_OF_TOTALITY: البابُ الأخير "
    "يُعَدّ ولا يُسكَت عنه؛ وموضعٌ واحدٌ فيه من المُودَع ينقض الجامعيّة عليه."
)

A_COMPLETE_HALF_IS_NOT_A_COMPLETE_FUNCTION: Final[str] = (
    "A_COMPLETE_HALF_IS_NOT_A_COMPLETE_FUNCTION: تمامُ النصف الإملائيّ لا يُرقّي "
    "الدالّةَ إلى تأسيسٍ تامّ؛ والنصفُ الصوتيُّ موقوفٌ فشرطُ الإمكان غيرُ مستوفًى."
)

THE_FOLD_IS_READ_FROM_THE_FINGERPRINT_NOT_REWRITTEN: Final[str] = (
    "THE_FOLD_IS_READ_FROM_THE_FINGERPRINT_NOT_REWRITTEN: جلوسُ البابِ خانةً "
    "يُعرَف بطيّ letter_fingerprint.fold_root ومفردتِه، ولا يُصطنَع طيٌّ ثانٍ."
)

NO_FOUNDING_HERE_LIFTS_A_BLOCK_OR_THAWS_A_FREEZE: Final[str] = (
    "NO_FOUNDING_HERE_LIFTS_A_BLOCK_OR_THAWS_A_FREEZE: لا ولادةَ ههنا، ولا حكمَ "
    "ولادة، ولا رفعَ حظرٍ، ولا فكَّ تجميد، ولا استيرادَ من kernel/."
)

IMLA_FOUNDING_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_FAMILY_OVERLAP_IS_NOT_A_CLASS_OVERLAP,
    A_CATCH_ALL_IS_A_MEASURED_RESIDUE_NOT_A_PROOF_OF_TOTALITY,
    A_COMPLETE_HALF_IS_NOT_A_COMPLETE_FUNCTION,
    THE_FOLD_IS_READ_FROM_THE_FINGERPRINT_NOT_REWRITTEN,
    NO_FOUNDING_HERE_LIFTS_A_BLOCK_OR_THAWS_A_FREEZE,
)
"""البقايا بأسمائها؛ وكلُّ واحدةٍ منها فرقٌ يُحتَجّ به لا شعارٌ يُردَّد."""


def the_block_and_the_freeze_are_untouched() -> bool:
    """لا حظرَ يُرفَع ولا تجميدَ يُفكّ بهذه الوحدة؛ وتُعاد الجملةُ ليُحتَجّ بها."""

    return NO_FOUNDING_HERE_LIFTS_A_BLOCK_OR_THAWS_A_FREEZE.startswith(
        "NO_FOUNDING_HERE_LIFTS_A_BLOCK_OR_THAWS_A_FREEZE"
    )


def _assert_the_table_is_exclusive() -> None:
    """المنعُ شرطُ تشغيلٍ لا نتيجةَ فحص؛ فيُصادَم الجدولُ عند الاستيراد."""

    reading = exclusivity_reading()
    if not reading.is_exclusive:
        overlap = " · ".join(reading.overlapping_codepoints)
        raise ImlaFoundingError(f"جدولٌ غيرُ مانعٍ عند: {overlap}.")
    classes = [rule.cls for rule in THE_IMLA_TABLE]
    if len(classes) != len(set(classes)):
        raise ImlaFoundingError("بابٌ بقاعدتين يُلبِس المنعَ؛ لكلّ بابٍ قاعدةٌ.")
    if ImlaClass.OUTSIDE_THE_DECLARED_TABLE in set(classes):
        raise ImlaFoundingError("بابُ البقيّة لا يُعلَن قاعدةً بل يُشتَقّ تكملةً.")


_assert_the_table_is_exclusive()
