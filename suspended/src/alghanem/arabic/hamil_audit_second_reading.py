"""قراءةٌ ثانيةٌ لتدقيق hamil بعد نزول بايتات مدوّنته في موضع الإيداع.

أُودِع تدقيقُ «حلقة ث/ع» الأولى في `hamil_phase1_audit_deposit` وفيه فحصان
موقوفان على بايتاتٍ لم تكن ههنا. ثمّ نزلت تلك البايتاتُ — بدور
`AUDIT_CORPUS` لا بدور القياس — فوجب أن يُعاد التدقيقُ عليها، وأن **يُسجَّل
تحوُّلُ كلّ موقوفٍ بتاريخه** لا أن يُبدَّل حكمُه صامتًا. ويفترق ههنا ثلاثةٌ
كانت تُقرأ واحدًا::

    BytesArrived          != EveryBlockedCheckIsLifted
    AMeasuredGap          != AnAttributedDefect
    OurDeclaredRule       != TheirExecutedRule

**أوّلًا: نزولُ البايتات لا يرفع كلَّ وقف.** من الفحصَين الموقوفَين واحدٌ
وحدَه كان موقوفًا على بايتات، فرُفِع وقفُه وقِيس. والآخرُ — ربحُ الزوجيّ
المشترك 5.83 — موقوفٌ على **نموذجهم المُدرَّب**، ولا تُخرِجه بايتاتٌ مهما
نزلت؛ فتحوُّلُه إعادةُ تجنيسٍ لا رفعَ وقف. وتسميتُه أوّلًا «موقوفًا على
بايتات» كانت تجنيسًا خاطئًا يُسجَّل ههنا ولا يُطوى
(`ARRIVING_BYTES_DO_NOT_LIFT_A_BLOCK_ON_THEIR_MODEL`).

**وثانيًا: قاعدتُنا ليست قاعدتَهم، والفرقُ لا يُنسَب.** يُقاس ههنا بقواعدَ
مُعلَنةٍ في `CountingRule`، وتُعرَض القواعدُ كلُّها بنتائجها ولا تُنتقى واحدةٌ
لموافقتها رقمًا منقولًا. وحين يخرج فرقٌ — ثلاثةُ هياكلَ مثلًا — فهو **فرقٌ
مقيسٌ بقاعدةٍ مُعلَنة**، ولا يُقال إنّه خللٌ في تنفيذهم: شيفرتُهم ليست ههنا،
وقاعدتُهم المُنفَّذةُ غيرُ موصوفةٍ بدقّةٍ تكفي للمطابقة
(`A_GAP_UNDER_OUR_RULE_DOES_NOT_ATTRIBUTE_ITSELF`).

**وثالثًا: مقامُ `raw_words` يبتلع ذيلَ الوسم.** المنقولُ 82,406 خرج ههنا
**مطابقًا بالقياس** حين قُسِم الملفُّ كلُّه على البياض؛ وخرج 82,379 حين
أُسقِطت أسطرُ التعليق العشرةُ في ذيل الملفّ — وهي كتلةُ وسمٍ تصف المدوّنةَ
ولا قرآنَ فيها. فالفرقُ **27 رمزًا ليست من النصّ**، وهي داخلةٌ في مقام
تغطيتهم؛ وفرقُهم المُعلَنُ 4,605 بين المقامين هو 4,578 بعد إخراجها. وهذا
تقاطعٌ حقيقيّ: رقمُهم أُعيد من بايتاتهم بقاعدةٍ مُعلَنةٍ فطابق، ثمّ سمّى
القياسُ ما فيه (`THE_DENOMINATOR_SWALLOWS_THE_METADATA_FOOTER`).

**ورابعًا: لا يُقاس أحدُ المُودَعَين على الآخر.** كلُّ رقمٍ ههنا مقيسٌ على
`corpora/globalquran-simple-enhanced.txt` وحدَها، ولا يُجمَع إلى رقمٍ من
`corpora/quran-simple-enhanced.txt` ولا يُطرَح منه؛ والبابُ الذي يمنع الخلطَ
مكتوبٌ في `audit_corpus_deposit.refuse_to_read_one_against_the_other`.

**ولا تعديلَ في hamil من ههنا**: التدقيقُ اتّجاهٌ واحد، ولا تكتب هذه الوحدةُ
في ذاك المستودع شيئًا، ولا تستورد من `kernel/` ولا من `program/`، ولا تقرؤها
بوّابةٌ فيهما.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass, fields
from enum import Enum
from pathlib import Path
from typing import Final

from .audit_corpus_deposit import (
    THE_AUDIT_CORPUS,
    THE_MEASUREMENT_CORPUS,
    CorpusRole,
    audit_corpus_bytes_are_resolvable,
    read_audit_corpus_bytes,
)

__all__ = [
    "ARRIVING_BYTES_DO_NOT_LIFT_A_BLOCK_ON_THEIR_MODEL",
    "A_GAP_UNDER_OUR_RULE_DOES_NOT_ATTRIBUTE_ITSELF",
    "SECOND_READING_NAMED_RESIDUALS",
    "THE_COUNTS_AT_MEASUREMENT",
    "THE_DENOMINATOR_SWALLOWS_THE_METADATA_FOOTER",
    "THE_QUOTED_FIGURES",
    "THE_RECORDING_DATE",
    "THE_TRANSITIONS_RECORDED",
    "AuditCounts",
    "BlockedGenus",
    "CountingRule",
    "SecondReadingCheck",
    "SecondReadingError",
    "SecondReadingGenus",
    "SecondReadingVerdict",
    "TransitionRecord",
    "count_by_rule",
    "measure_the_audit_corpus",
    "second_reading_checks",
    "the_counts_have_drifted",
    "the_measurement_is_possible",
]

THE_RECORDING_DATE: Final[str] = "2026-09-27"
"""تاريخُ نزول البايتات وإعادةِ القراءة عليها، مكتوبًا في السجلّ لا في حارس."""


class SecondReadingError(ValueError):
    """رُفض مدخلٌ خارج مفردات هذه القراءة؛ ولا يُحمَل على أقرب حالة."""


class CountingRule(Enum):
    """قواعدُ العدّ، مُعلَنةٌ ومعروضةٌ كلُّها؛ ولا تُنتقى واحدةٌ لموافقتها."""

    WHITESPACE_TOKENS_IN_THE_WHOLE_FILE = "رموزٌ يفصلها بياضٌ في الملفّ كلِّه"
    """لا يُستثنى شيء: أسطرُ كتلة الوسم في الذيل معدودةٌ كسائر السطور."""

    WHITESPACE_TOKENS_OUTSIDE_THE_COMMENT_BLOCK = "رموزٌ يفصلها بياضٌ خارج أسطر `#`"
    """يُسقَط كلُّ سطرٍ أوّلُ غيرِ بياضه `#`، وهي كتلةُ وسمِ المدوّنة في ذيلها."""

    DISTINCT_TOKENS_OUTSIDE_THE_COMMENT_BLOCK = "رموزٌ متمايزةٌ خارج أسطر `#`"
    """تمايزُ الرموز بحروفها وعلاماتها معًا، بلا تجريدٍ ولا توحيد."""

    DISTINCT_MARK_STRIPPED_TOKENS = "رموزٌ متمايزةٌ بعد إسقاط علامات `Mn`"
    """يُسقَط كلُّ ما صنفُه `Mn` ثمّ يُعَدّ المتمايز؛ وهذا أقربُ ما يُسمّى «هيكلًا»."""


class SecondReadingGenus(Enum):
    """جنسُ فحصٍ في القراءة الثانية؛ والوقفُ يُسمّى بما يَقف عليه لا بتاريخه."""

    MEASURED_ON_THE_AUDIT_CORPUS = "مقيسٌ_على_مدوّنة_التدقيق_بقاعدةٍ_معلَنة"
    RECOMPUTED_FROM_THE_QUOTED_FIGURES = "مُعادٌ_من_الأرقام_المنقولة_وحدَها"
    REQUIRES_THEIR_MODEL_WHICH_BYTES_DO_NOT_LIFT = "موقوفٌ_على_نموذجهم_لا_على_بايتات"


class BlockedGenus(Enum):
    """جنسُ الوقف قبل التحوّل وبعده، ليُقرأ التحوُّلُ نوعًا لا مجرّدَ تبديل."""

    REQUIRES_BYTES_NOT_DEPOSITED = "موقوفٌ_على_بايتاتٍ_لم_تُودَع"
    MEASURED_ON_THE_AUDIT_CORPUS = "مقيسٌ_على_مدوّنة_التدقيق_بقاعدةٍ_معلَنة"
    REQUIRES_THEIR_MODEL_WHICH_BYTES_DO_NOT_LIFT = "موقوفٌ_على_نموذجهم_لا_على_بايتات"


class SecondReadingVerdict(Enum):
    """حكمُ الفحص؛ ولا يُكتَب في حقلٍ بل يُشتَقّ من الطرفَين عند القراءة."""

    AGREES = "تطابق"
    CONTRADICTS = "تخالف"
    STILL_BLOCKED = "باقٍ_موقوفًا"


def _require_text(value: str, what: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise SecondReadingError(f"{what} لا يكون فارغًا.")


THE_QUOTED_FIGURES: Final[dict[str, int]] = {
    "raw_words": 82_406,
    "Nw": 77_801,
    "الهياكل": 14_870,
    "فرقُ المقامين": 4_605,
}
"""أرقامُ ذاك البرنامج بحروفها؛ وحفظُها ليس تصديقَها، والمقابلةُ تحتها."""


@dataclass(frozen=True, slots=True)
class AuditCounts:
    """ما يُخرِجه القرصُ بالقواعد الأربع، مقيسًا على مدوّنة التدقيق وحدَها."""

    whole_file_tokens: int
    tokens_outside_the_comment_block: int
    distinct_tokens: int
    distinct_mark_stripped_tokens: int

    def __post_init__(self) -> None:
        for field in fields(self):
            if getattr(self, field.name) < 1:
                raise SecondReadingError("عددٌ دون الواحد لا يخرج من قياس.")

    @property
    def comment_block_tokens(self) -> int:
        """رموزُ كتلة الوسم في الذيل، مُشتَقّةً لا مكتوبةً في حقلٍ ثالث."""

        return self.whole_file_tokens - self.tokens_outside_the_comment_block


THE_COUNTS_AT_MEASUREMENT: Final[AuditCounts] = AuditCounts(
    whole_file_tokens=82_406,
    tokens_outside_the_comment_block=82_379,
    distinct_tokens=18_254,
    distinct_mark_stripped_tokens=14_873,
)
"""الأرقامُ كما ولَّدها القرصُ يوم الاستقبال، لتُقابَل بما يقيسه اليوم.

ونقلُها إلى هذا النصّ لا يجعلها منقولةً عن عرضٍ خارجيّ: مصدرُها
`measure_the_audit_corpus()` على البايتات المُودَعة، و`the_counts_have_drifted`
تُعيد توليدَها من القرص في كلّ نداء فتُكشَف الزحزحةُ ولا تُخفى.
"""


def _lines_outside_the_comment_block(text: str) -> list[str]:
    return [line for line in text.split("\n") if not line.lstrip().startswith("#")]


def _strip_marks(token: str) -> str:
    return "".join(
        character for character in token if unicodedata.category(character) != "Mn"
    )


def count_by_rule(text: str, rule: CountingRule) -> int:
    """عددٌ واحدٌ بقاعدةٍ واحدةٍ مُعلَنة؛ ولا عددَ يخرج من هنا بلا قاعدته."""

    body = text.lstrip("\ufeff")
    if rule is CountingRule.WHITESPACE_TOKENS_IN_THE_WHOLE_FILE:
        return len(body.split())
    outside = "\n".join(_lines_outside_the_comment_block(body)).split()
    if rule is CountingRule.WHITESPACE_TOKENS_OUTSIDE_THE_COMMENT_BLOCK:
        return len(outside)
    if rule is CountingRule.DISTINCT_TOKENS_OUTSIDE_THE_COMMENT_BLOCK:
        return len(set(outside))
    return len({_strip_marks(token) for token in outside})


def measure_the_audit_corpus(path: Path | str | None = None) -> AuditCounts:
    """يقيس القواعدَ الأربعَ على البايتات المُودَعة بعد مطابقة ختمها.

    ولا رقمَ يخرج بغير البايتات: غيابُها رفضُ إخراجٍ لا قيمةٌ افتراضيّة، وهي
    تُقرأ عبر `read_audit_corpus_bytes` فتُطابَق طولًا وبصمةً قبل أيّ عدّ.
    """

    text = read_audit_corpus_bytes(path).decode("utf-8")
    return AuditCounts(
        whole_file_tokens=count_by_rule(
            text, CountingRule.WHITESPACE_TOKENS_IN_THE_WHOLE_FILE
        ),
        tokens_outside_the_comment_block=count_by_rule(
            text, CountingRule.WHITESPACE_TOKENS_OUTSIDE_THE_COMMENT_BLOCK
        ),
        distinct_tokens=count_by_rule(
            text, CountingRule.DISTINCT_TOKENS_OUTSIDE_THE_COMMENT_BLOCK
        ),
        distinct_mark_stripped_tokens=count_by_rule(
            text, CountingRule.DISTINCT_MARK_STRIPPED_TOKENS
        ),
    )


def the_measurement_is_possible(path: Path | str | None = None) -> bool:
    """أحاضرةٌ بايتاتُ مدوّنة التدقيق؟ وهو شرطُ القياس، لا متغيّرُ بيئة."""

    return audit_corpus_bytes_are_resolvable(path)


def the_counts_have_drifted(path: Path | str | None = None) -> bool:
    """أزحزح المقيسُ اليومَ عمّا نُقل إلى `THE_COUNTS_AT_MEASUREMENT`؟"""

    return measure_the_audit_corpus(path) != THE_COUNTS_AT_MEASUREMENT


@dataclass(frozen=True, slots=True)
class SecondReadingCheck:
    """فحصٌ واحدٌ في القراءة الثانية؛ وحكمُه مُشتَقٌّ من طرفَيه لا مكتوب."""

    name: str
    statement: str
    genus: SecondReadingGenus
    rule: CountingRule | None
    quoted: float | None
    measured: float | None

    def __post_init__(self) -> None:
        _require_text(self.name, "اسمُ الفحص")
        _require_text(self.statement, "بيانُ الفحص")
        if not isinstance(self.genus, SecondReadingGenus):
            raise SecondReadingError("جنسُ الفحص عضوٌ في `SecondReadingGenus`.")
        their_model = SecondReadingGenus.REQUIRES_THEIR_MODEL_WHICH_BYTES_DO_NOT_LIFT
        blocked = self.genus is their_model
        if blocked and (self.measured is not None):
            raise SecondReadingError(
                "فحصٌ موقوفٌ على نموذجهم لا يحمل طرفًا مقيسًا؛ وحملُه يُوهِم قياسًا لم يقع."
            )
        if not blocked and (self.quoted is None or self.measured is None):
            raise SecondReadingError("فحصٌ غيرُ موقوفٍ بلا طرفَين ليس فحصًا.")
        if (
            self.genus is SecondReadingGenus.MEASURED_ON_THE_AUDIT_CORPUS
            and self.rule is None
        ):
            raise SecondReadingError("قياسٌ بلا قاعدةٍ مُعلَنةٍ ليس قياسًا.")

    @property
    def verdict(self) -> SecondReadingVerdict:
        """الحكمُ تابعًا للطرفَين؛ ولا حقلَ يحمله فيُبدَّل وحدَه."""

        if self.measured is None or self.quoted is None:
            return SecondReadingVerdict.STILL_BLOCKED
        if self.measured == self.quoted:
            return SecondReadingVerdict.AGREES
        return SecondReadingVerdict.CONTRADICTS

    @property
    def gap(self) -> float | None:
        """فرقُ المقيس عن المنقول، أو `None` حيث لا قياس؛ ولا يُصفَّر تلطّفًا."""

        if self.measured is None or self.quoted is None:
            return None
        return self.measured - self.quoted


def second_reading_checks(
    path: Path | str | None = None,
) -> tuple[SecondReadingCheck, ...]:
    """فحوصُ القراءة الثانية، يُقاس ما يُقاس منها من القرص عند كلّ نداء."""

    counts = measure_the_audit_corpus(path)
    return (
        SecondReadingCheck(
            name="raw_words على الملفّ كلِّه",
            statement=(
                "المنقولُ 82,406 من القسمة على البياض، بإزاء ما يُخرِجه القرصُ "
                "بالقاعدة نفسِها على بايتات مدوّنة التدقيق"
            ),
            genus=SecondReadingGenus.MEASURED_ON_THE_AUDIT_CORPUS,
            rule=CountingRule.WHITESPACE_TOKENS_IN_THE_WHOLE_FILE,
            quoted=float(THE_QUOTED_FIGURES["raw_words"]),
            measured=float(counts.whole_file_tokens),
        ),
        SecondReadingCheck(
            name="raw_words خارج كتلة الوسم",
            statement=(
                "المنقولُ 82,406 بإزاء الرموز خارج أسطر `#` — وكتلةُ الوسم في "
                "الذيل ليست قرآنًا، ورموزُها داخلةٌ في مقام التغطية"
            ),
            genus=SecondReadingGenus.MEASURED_ON_THE_AUDIT_CORPUS,
            rule=CountingRule.WHITESPACE_TOKENS_OUTSIDE_THE_COMMENT_BLOCK,
            quoted=float(THE_QUOTED_FIGURES["raw_words"]),
            measured=float(counts.tokens_outside_the_comment_block),
        ),
        SecondReadingCheck(
            name="بصمةُ الهياكل 14,870",
            statement=(
                "المُجمَّدُ في `assert` بإزاء الرموز المتمايزة بعد إسقاط `Mn` "
                "على البايتات نفسِها؛ والقاعدةُ قاعدتُنا لا قاعدتُهم"
            ),
            genus=SecondReadingGenus.MEASURED_ON_THE_AUDIT_CORPUS,
            rule=CountingRule.DISTINCT_MARK_STRIPPED_TOKENS,
            quoted=float(THE_QUOTED_FIGURES["الهياكل"]),
            measured=float(counts.distinct_mark_stripped_tokens),
        ),
        SecondReadingCheck(
            name="فرقُ المقامين 4,605",
            statement=(
                "فرقُهم المُعلَنُ بين 82,406 و77,801، بإزاء الفرق بعد إخراج "
                "رموز كتلة الوسم من المقام الأعلى"
            ),
            genus=SecondReadingGenus.RECOMPUTED_FROM_THE_QUOTED_FIGURES,
            rule=None,
            quoted=float(THE_QUOTED_FIGURES["فرقُ المقامين"]),
            measured=float(
                counts.tokens_outside_the_comment_block - THE_QUOTED_FIGURES["Nw"]
            ),
        ),
        SecondReadingCheck(
            name="ربحُ الزوجيّ المشترك",
            statement=(
                "المنقولُ 5.83 بتًّا/زوجيّ-مشترك: مخرَجُ نموذجٍ مُدرَّبٍ عندهم، "
                "لا مخرَجُ عدٍّ على بايتات؛ فنزولُ البايتات لا يرفع وقفَه"
            ),
            genus=SecondReadingGenus.REQUIRES_THEIR_MODEL_WHICH_BYTES_DO_NOT_LIFT,
            rule=None,
            quoted=5.83,
            measured=None,
        ),
        SecondReadingCheck(
            name="Nw من parse_verses",
            statement=(
                "المنقولُ 77,801: مخرَجُ دالّةِ تقطيعٍ عندهم لم تُودَع، فلا "
                "تُعاد ههنا بقاعدةٍ مُعلَنةٍ إلّا تخمينًا"
            ),
            genus=SecondReadingGenus.REQUIRES_THEIR_MODEL_WHICH_BYTES_DO_NOT_LIFT,
            rule=None,
            quoted=float(THE_QUOTED_FIGURES["Nw"]),
            measured=None,
        ),
    )


@dataclass(frozen=True, slots=True)
class TransitionRecord:
    """تحوُّلُ وقفٍ بتاريخه: من أيّ جنسٍ إلى أيّ جنسٍ، وبأيّ شيءٍ تحوّل."""

    check_name: str
    was: BlockedGenus
    became: BlockedGenus
    on_date: str
    lifted_by: str | None
    note: str

    def __post_init__(self) -> None:
        _require_text(self.check_name, "اسمُ الفحص المتحوِّل")
        _require_text(self.on_date, "تاريخُ التحوّل")
        _require_text(self.note, "بيانُ التحوّل")
        for genus in (self.was, self.became):
            if not isinstance(genus, BlockedGenus):
                raise SecondReadingError("جنسُ الوقف عضوٌ في `BlockedGenus`.")
        if self.was is self.became:
            raise SecondReadingError("تحوُّلٌ إلى الجنس نفسِه ليس تحوّلًا.")
        if self.became is BlockedGenus.MEASURED_ON_THE_AUDIT_CORPUS:
            if not self.lifted_by:
                raise SecondReadingError(
                    "لا يصير فحصٌ مقيسًا بلا ما رفع وقفَه مُسمًّى؛ وقياسٌ بلا رافعٍ دعوى."
                )
        elif self.lifted_by:
            raise SecondReadingError("إعادةُ تجنيسٍ ليست رفعَ وقف، فلا يُسمّى لها رافع.")

    @property
    def the_bytes_lifted_it(self) -> bool:
        """أرفعت البايتاتُ وقفَه فعلًا؟ مُشتَقًّا من المقصد لا مكتوبًا."""

        return self.became is BlockedGenus.MEASURED_ON_THE_AUDIT_CORPUS


THE_TRANSITIONS_RECORDED: Final[tuple[TransitionRecord, ...]] = (
    TransitionRecord(
        check_name="بصمةُ الهياكل 14,870",
        was=BlockedGenus.REQUIRES_BYTES_NOT_DEPOSITED,
        became=BlockedGenus.MEASURED_ON_THE_AUDIT_CORPUS,
        on_date=THE_RECORDING_DATE,
        lifted_by=(
            "نزولُ `corpora/globalquran-simple-enhanced.txt` عبر بوّابة "
            "الاستقبال بدور `AUDIT_CORPUS`"
        ),
        note=(
            "قِيس بقاعدةٍ مُعلَنةٍ فخرج 14,873 بإزاء 14,870، وفرقُ ثلاثةٍ "
            "مقيسٌ لا منسوبٌ: قاعدتُنا ليست قاعدتَهم المُنفَّذة"
        ),
    ),
    TransitionRecord(
        check_name="ربحُ الزوجيّ المشترك",
        was=BlockedGenus.REQUIRES_BYTES_NOT_DEPOSITED,
        became=BlockedGenus.REQUIRES_THEIR_MODEL_WHICH_BYTES_DO_NOT_LIFT,
        on_date=THE_RECORDING_DATE,
        lifted_by=None,
        note=(
            "لم ترفع البايتاتُ وقفَه: مخرَجُ نموذجٍ مُدرَّبٍ لا مخرَجُ عدّ. "
            "فتسميتُه أوّلًا «موقوفًا على بايتات» تجنيسٌ خاطئٌ صُحِّح ههنا، "
            "والتحوّلُ إعادةُ تجنيسٍ لا رفعَ وقف"
        ),
    ),
)
"""التحوُّلان بتاريخهما: واحدٌ رُفِع وقفُه فقِيس، وآخرُ أُعيد تجنيسُه ولم يُرفَع."""


ARRIVING_BYTES_DO_NOT_LIFT_A_BLOCK_ON_THEIR_MODEL: Final[str] = (
    "ARRIVING_BYTES_DO_NOT_LIFT_A_BLOCK_ON_THEIR_MODEL: من الفحصَين الموقوفَين "
    "في الإيداع الأوّل واحدٌ وحدَه كان موقوفًا على بايتات فقِيس لمّا نزلت؛ "
    "والآخرُ موقوفٌ على نموذجٍ مُدرَّبٍ عندهم لا تُخرِجه بايتاتٌ، فتحوُّلُه "
    "إعادةُ تجنيسٍ تُسجَّل بتاريخها لا رفعُ وقفٍ يُدَّعى"
)

A_GAP_UNDER_OUR_RULE_DOES_NOT_ATTRIBUTE_ITSELF: Final[str] = (
    "A_GAP_UNDER_OUR_RULE_DOES_NOT_ATTRIBUTE_ITSELF: 14,873 مقيسةٌ ههنا "
    "بقاعدةٍ مُعلَنةٍ بإزاء 14,870 المُجمَّدة في `assert` عندهم؛ والفرقُ ثلاثةٌ "
    "**مقيسٌ** ولا يُنسَب إلى خللٍ في تنفيذهم، إذ شيفرتُهم ليست ههنا وقاعدتُهم "
    "المُنفَّذةُ غيرُ موصوفةٍ بدقّةٍ تكفي للمطابقة"
)

THE_DENOMINATOR_SWALLOWS_THE_METADATA_FOOTER: Final[str] = (
    "THE_DENOMINATOR_SWALLOWS_THE_METADATA_FOOTER: 82,406 أُعيدت من بايتاتهم "
    "بالقسمة على البياض فطابقت بالحرف، ثمّ سمّى القياسُ ما فيها: 27 رمزًا من "
    "كتلة وسمٍ في ذيل الملفّ ليست قرآنًا. فمقامُ تغطيتهم أوسعُ من نصّهم، "
    "وفرقُهم المُعلَنُ 4,605 هو 4,578 بعد إخراجها"
)

SECOND_READING_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "ARRIVING_BYTES_DO_NOT_LIFT_A_BLOCK_ON_THEIR_MODEL": (
        ARRIVING_BYTES_DO_NOT_LIFT_A_BLOCK_ON_THEIR_MODEL
    ),
    "A_GAP_UNDER_OUR_RULE_DOES_NOT_ATTRIBUTE_ITSELF": (
        A_GAP_UNDER_OUR_RULE_DOES_NOT_ATTRIBUTE_ITSELF
    ),
    "THE_DENOMINATOR_SWALLOWS_THE_METADATA_FOOTER": (
        THE_DENOMINATOR_SWALLOWS_THE_METADATA_FOOTER
    ),
}


def _verify_no_reading_type_carries_a_verdict_field() -> None:
    """مبرهنة: لا حقلَ حكمٍ في أنواع هذه القراءة؛ فالحكمُ يتبع الطرفَين."""

    for _dataclass in (SecondReadingCheck, TransitionRecord, AuditCounts):
        for _field in fields(_dataclass):
            if "verdict" in _field.name:
                raise RuntimeError("a second-reading type carries a verdict field")


def _verify_the_two_roles_stay_apart() -> None:
    """مبرهنة بنيويّة: مدوّنةُ هذه القراءة هي مدوّنةُ التدقيق لا مدوّنةُ القياس."""

    if THE_AUDIT_CORPUS.role is not CorpusRole.AUDIT_CORPUS:
        raise RuntimeError("the audited corpus is not declared an audit corpus")
    if THE_MEASUREMENT_CORPUS.role is not CorpusRole.MEASUREMENT_CORPUS:
        raise RuntimeError("the measurement corpus lost its declared role")


def _verify_every_transition_names_its_kind() -> None:
    """مبرهنة: تحوُّلٌ إلى «مقيس» يلزمه رافعٌ مُسمًّى، وغيرُه لا رافعَ له."""

    for transition in THE_TRANSITIONS_RECORDED:
        if transition.the_bytes_lifted_it and not transition.lifted_by:
            raise RuntimeError("a lifted transition names no lifter")


_verify_no_reading_type_carries_a_verdict_field()
_verify_the_two_roles_stay_apart()
_verify_every_transition_names_its_kind()
