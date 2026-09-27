"""إيداعُ تدقيقِ «حلقة ث/ع» الأولى من برنامج hamil: فحصٌ حسابيٌّ لا تصديقُ نقل.

وصل إلى هذه الشجرة إيداعٌ من مستودعٍ آخر (`hamil-hala-zaman-program`) فيه
`dictionary_engine.py` و`dictionary_v0.json` و`induction/results.json`
و`PHASE1-STATUS.md`. وبايتاتُ مدوّنته — `mujammad.txt`، 1,306,770 بايتًا من
`GlobalQuran` — **ليست في هذه الشجرة**، ولا بايتَ من مُخرَجاته أُودِع هنا.
فلا تُعاد تجربةٌ منه ههنا.

غير أنّ أكثرَ أرقامه **لا تحتاج المدوّنةَ لتُفحَص**: مجموعُ الأصناف الأربعة،
وتفكيكُ خواتم «ق»، ومصالحةُ العدّ، ومجموعُ الانتقالات والهوامش، وفرقُ
التمويهين، وجدولُ سترلنج وبِلّ، وقاعدةُ السلسلة في الإنتروبيا — كلُّها متطابقاتٌ
**داخل النقل نفسِه**، تُعاد بالحساب من الأعداد المنقولة وحدَها. فيفترق ههنا
جنسان كانا يُقرآن واحدًا::

    AQuotedFigure                != AnUncheckableFigure
    RecomputedFromTheQuotation   != MeasuredOnTheCorpus
    AnAgreementOnATotal          != AnAgreementOnASource

**أوّلًا: الفحصُ يجري فعلًا، ولا يُدّعى.** كلُّ متطابقةٍ في `THE_CHECKS`
تُعاد حسابًا عند الاستيراد، ويُسجَّل حكمُها `AGREES` أو `CONTRADICTS` **مشتقًّا
من الحساب لا مكتوبًا في حقل**. فليس في هذا الملفّ حكمٌ يُكتَب باليد ثم يُصدَّق
(`A_VERDICT_HERE_IS_RECOMPUTED_NOT_TRANSCRIBED`).

**وثانيًا: اتّفاقُ المجموع ليس اتّفاقًا على المصدر.** أن يجمع تفكيكُ «ق»
خواتمَه إلى 22,317 يُثبت أنّ النقلَ **متّسقٌ داخليًّا**، ولا يُثبت أنّ 22,317
مقيسةٌ على مدوّنةٍ صحيحة: عددان مختلقان متّسقان يمرّان هذا الفحصَ بعينه. فحكمُ
`AGREES` ههنا **نفيُ عطلٍ لا إثباتُ صحّة**
(`AN_INTERNAL_IDENTITY_IS_NOT_AN_EXTERNAL_CONFIRMATION`).

**وثالثًا: ما قِيس في مقامٍ آخر لا يعبر إلى مقامنا.** `mujammad.txt` غيرُ
`corpora/quran-simple-enhanced.txt`: 1,306,770 بايتًا مقابل 1,319,901، وفرقُ
13,131 بايتًا. فلا يُقرأ رقمٌ من ذاك سندًا لرقمٍ من هذا، ولا يُجمَعان ولا
يُطرَحان. والختمُ `8b387e8` الذي طُلِب فحصُه ههنا **من ذاك المستودع**، ولذلك لم
يكن كائنًا صالحًا في هذه الشجرة — وهذا حسمُ سؤالٍ كان معلَّقًا، لا عجزٌ عنه
(`A_SEAL_FROM_ANOTHER_REPOSITORY_IS_NOT_A_MISSING_OBJECT_HERE`).

**ورابعًا: سترلنج هو موضعُ التقاطع الحقيقيّ الوحيد.** S(28,4) و S(28,2..6)
و log₂Bell(28) و log₂Bell(112) تُعاد ههنا من `letter_haraka_partition` — وهي
كتابةٌ لا صلةَ لها بذاك التنفيذ. فاتّفاقُ رقمٍ من سبع عشرة خانةً بين تنفيذين
مستقلّين **شهادةٌ على الحسابين معًا**، وهو الجنسُ الوحيد ههنا الذي يستحقّ اسم
«تحقُّقٍ متقاطع» (`ONLY_A_SECOND_IMPLEMENTATION_MAKES_A_CROSS_CHECK`).

**وخامسًا: التناقضاتُ تُسمّى ولا تُلطَّف.** ثلاثةُ معدّلاتٍ في واجهة ذاك
الإيداع لا تُشتقّ من ملفّ نتائجه بأيّ مقام، وقاعدةُ السلسلة مخروقةٌ بفرقٍ
أكبرَ من التقريب، والهامشُ `T` يخالف ما نُقل شفاهًا بالضعف. وهذه تُودَع
`CONTRADICTS` بالحساب، لا «فروقًا تحتاج مراجعة»
(`A_CONTRADICTION_IS_NAMED_NOT_SOFTENED`).

**وسادسًا: عيوبُ شيفرةٍ أخرى تُوصَف ولا تُقاس.** ما قيل في
`dictionary_engine.py` — كافٌ معلَنةٌ لا تُنفَّذ، ودالّةٌ لا تُستدعى، ومقامان
يُقرآن واحدًا، و`assert` يُجمِّد واقعةً مؤرَّخة — وُصِف بقراءة نصٍّ لُصِق في
محادثة، لا بتشغيلِ ملفٍّ في هذه الشجرة. فيُسجَّل `NOT_CHECKABLE_HERE` ولو كان
بيّنًا (`READING_A_PASTED_LISTING_IS_NOT_RUNNING_IT`).

**خمولٌ سلطويّ**: لا ولادةَ هنا ولا حكمَ ولادةٍ ولا تجميدَ `E0`، ولا استيرادَ
من `kernel/` ولا من `program/`، ولا بوّابةَ في هذا المستودع تقرأ هذا الإيداع.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from math import log2
from typing import Final

from .letter_haraka_partition import bell_number, stirling_second_kind
from .text_key import comparison_key

__all__ = [
    "AN_INTERNAL_IDENTITY_IS_NOT_AN_EXTERNAL_CONFIRMATION",
    "A_CONTRADICTION_IS_NAMED_NOT_SOFTENED",
    "A_SEAL_FROM_ANOTHER_REPOSITORY_IS_NOT_A_MISSING_OBJECT_HERE",
    "A_VERDICT_HERE_IS_RECOMPUTED_NOT_TRANSCRIBED",
    "HAMIL_PHASE1_AUDIT_DEPOSIT",
    "HAMIL_PHASE1_NAMED_RESIDUALS",
    "ONLY_A_SECOND_IMPLEMENTATION_MAKES_A_CROSS_CHECK",
    "READING_A_PASTED_LISTING_IS_NOT_RUNNING_IT",
    "THE_CHECKS",
    "THE_CLASS_COUNTS",
    "THE_CODE_DEFECTS",
    "THE_CORPUS_IS_NOT_OURS",
    "THE_MARGINALS",
    "THE_QAF_ENDINGS",
    "THE_TRANSITIONS",
    "ArithmeticCheck",
    "CheckGenus",
    "CheckVerdict",
    "CodeDefect",
    "DefectGenus",
    "HamilPhase1AuditDeposit",
    "HamilPhase1DepositError",
    "ForeignCorpusNote",
    "the_chain_rule_gap",
    "the_rate_denominators",
    "the_stirling_cross_check",
]


class HamilPhase1DepositError(ValueError):
    """رُفض مدخلٌ خارج الإيداع المُجمَّد؛ ولا يُحمَل على أقرب حالة."""


class CheckGenus(Enum):
    """جنسُ الفحص: من النقل وحدَه، أو بتنفيذٍ ثانٍ، أو متعذِّرٌ بلا بايتات."""

    RECOMPUTED_FROM_THE_QUOTED_FIGURES = "مُعادٌ_من_الأرقام_المنقولة_وحدَها"
    RECOMPUTED_BY_AN_INDEPENDENT_IMPLEMENTATION = "مُعادٌ_بتنفيذٍ_مستقلٍّ_ههنا"
    REQUIRES_BYTES_NOT_DEPOSITED = "موقوفٌ_على_بايتاتٍ_لم_تُودَع"


class CheckVerdict(Enum):
    """حكمُ الفحص؛ ولا يُكتَب في حقلٍ بل يُشتَقّ من الحساب عند الإنشاء."""

    AGREES = "تطابق"
    CONTRADICTS = "تخالف"
    NOT_CHECKABLE_HERE = "غيرُ_قابلٍ_للفحص_ههنا"


class DefectGenus(Enum):
    """نوعُ عيبِ الشيفرة الموصوف، مُسمًّى لا مُجمَلًا."""

    DECLARED_RULE_NOT_EXECUTED = "قاعدةٌ_معلَنةٌ_لا_تُنفَّذ"
    DEFINED_AND_NEVER_CALLED = "معرَّفةٌ_ولا_تُستدعى"
    TWO_DENOMINATORS_READ_AS_ONE = "مقامان_يُقرآن_واحدًا"
    A_DATED_FACT_FROZEN_IN_A_GUARD = "واقعةٌ_مؤرَّخةٌ_مُجمَّدةٌ_في_حاجب"
    A_RESIDUAL_COUNTED_OVER_ITS_OWN_RULE = "متبقٍّ_يبتلع_قاعدتَه"


A_VERDICT_HERE_IS_RECOMPUTED_NOT_TRANSCRIBED: Final[str] = (
    "A_VERDICT_HERE_IS_RECOMPUTED_NOT_TRANSCRIBED: كلُّ حكمٍ في `THE_CHECKS` "
    "يُشتَقّ من مقارنةِ يسارٍ بيمينٍ محسوبَين عند الاستيراد، ولا يُقبَل حقلُ "
    "حكمٍ مكتوبٍ باليد؛ فمن بدّل رقمًا ولم يبدّل المتطابقةَ انقلب حكمُه وحدَه"
)

AN_INTERNAL_IDENTITY_IS_NOT_AN_EXTERNAL_CONFIRMATION: Final[str] = (
    "AN_INTERNAL_IDENTITY_IS_NOT_AN_EXTERNAL_CONFIRMATION: اتّفاقُ مجموعٍ مع "
    "مجموعِ أجزائه يُثبت اتّساقَ النقل داخلَه ولا يُثبت صحّةَ قياسه على "
    "مدوّنة؛ فعددان مختلقان متّسقان يمرّان الفحصَ نفسَه، و`AGREES` ههنا نفيُ "
    "عطلٍ لا إثباتُ صحّة"
)

ONLY_A_SECOND_IMPLEMENTATION_MAKES_A_CROSS_CHECK: Final[str] = (
    "ONLY_A_SECOND_IMPLEMENTATION_MAKES_A_CROSS_CHECK: ما أُعيد ههنا من "
    "`letter_haraka_partition` — سترلنج وبِلّ — هو وحدَه التحقُّقُ المتقاطع في "
    "هذا الإيداع، لأنّه كُتب في شجرةٍ أخرى بخوارزميّةٍ أخرى؛ وما سواه اتّساقٌ "
    "داخليٌّ لا تقاطعُ تنفيذين"
)

A_CONTRADICTION_IS_NAMED_NOT_SOFTENED: Final[str] = (
    "A_CONTRADICTION_IS_NAMED_NOT_SOFTENED: ما خالف يُودَع `CONTRADICTS` "
    "بالحساب ولا يُكتَب «فرقًا يحتاج مراجعةً»؛ وخرقُ قاعدة السلسلة، وتعذُّرُ "
    "اشتقاقِ المعدّلات، واختلافُ الهامش `T`، ثلاثتُها مخالفاتٌ مقيسةٌ لا ظنون"
)

A_SEAL_FROM_ANOTHER_REPOSITORY_IS_NOT_A_MISSING_OBJECT_HERE: Final[str] = (
    "A_SEAL_FROM_ANOTHER_REPOSITORY_IS_NOT_A_MISSING_OBJECT_HERE: الختمُ "
    "`8b387e8` لم يكن كائنًا صالحًا في هذه الشجرة لأنّه ختمُ مستودعٍ آخر، لا "
    "لأنّ شيئًا ضاع ههنا؛ وهذا حسمُ سؤالٍ كان معلَّقًا لا عجزٌ عنه"
)

READING_A_PASTED_LISTING_IS_NOT_RUNNING_IT: Final[str] = (
    "READING_A_PASTED_LISTING_IS_NOT_RUNNING_IT: عيوبُ `dictionary_engine.py` "
    "موصوفةٌ عن نصٍّ لُصِق في محادثة، لا عن ملفٍّ شُغِّل ههنا؛ فتُسجَّل "
    "`NOT_CHECKABLE_HERE` ولو كانت بيّنةً في القراءة، إذ البيانُ في العين غيرُ "
    "التشغيل في الشجرة"
)

THE_CORPUS_IS_NOT_OURS: Final[str] = (
    "THE_CORPUS_IS_NOT_OURS: `mujammad.txt` (1,306,770 بايتًا من GlobalQuran) "
    "غيرُ `corpora/quran-simple-enhanced.txt` (1,319,901)، وبينهما 13,131 "
    "بايتًا؛ فلا رقمَ من ذاك يُسنِد رقمًا من هذا، ولا يُجمَعان ولا يُطرَحان"
)

HAMIL_PHASE1_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "A_VERDICT_HERE_IS_RECOMPUTED_NOT_TRANSCRIBED": (
        A_VERDICT_HERE_IS_RECOMPUTED_NOT_TRANSCRIBED
    ),
    "AN_INTERNAL_IDENTITY_IS_NOT_AN_EXTERNAL_CONFIRMATION": (
        AN_INTERNAL_IDENTITY_IS_NOT_AN_EXTERNAL_CONFIRMATION
    ),
    "ONLY_A_SECOND_IMPLEMENTATION_MAKES_A_CROSS_CHECK": (
        ONLY_A_SECOND_IMPLEMENTATION_MAKES_A_CROSS_CHECK
    ),
    "A_CONTRADICTION_IS_NAMED_NOT_SOFTENED": A_CONTRADICTION_IS_NAMED_NOT_SOFTENED,
    "A_SEAL_FROM_ANOTHER_REPOSITORY_IS_NOT_A_MISSING_OBJECT_HERE": (
        A_SEAL_FROM_ANOTHER_REPOSITORY_IS_NOT_A_MISSING_OBJECT_HERE
    ),
    "READING_A_PASTED_LISTING_IS_NOT_RUNNING_IT": (
        READING_A_PASTED_LISTING_IS_NOT_RUNNING_IT
    ),
    "THE_CORPUS_IS_NOT_OURS": THE_CORPUS_IS_NOT_OURS,
}
"""ما لا تحسمه هذه الوحدة، مُسمًّى هنا لا متروكًا ليُفترَض."""

_FORBIDDEN_FIELD_TOKENS: Final[tuple[str, ...]] = (
    "birth",
    "certificate",
    "freeze",
    "proof",
    "score",
)


def _require_text(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise HamilPhase1DepositError(
            f"{field_name} يجب أن يكون نصًّا غير فارغ؛ ولا يُقبَل فيه الفراغ صمتًا."
        )
    return value


# --- الأعدادُ المنقولةُ كما وصلت، بلا تعديلِ رقمٍ واحد ------------------------

THE_CLASS_COUNTS: Final[dict[str, int]] = {
    "ث": 24735,
    "ع": 27596,
    "ز": 3153,
    "ق": 22317,
}
"""أصنافُ `dictionary_v0.json` الأربعة كما نُقلت؛ مجموعُها يُفحَص أدناه."""

THE_QAF_ENDINGS: Final[dict[str, int]] = {
    "آ": 1,
    "ا": 13959,
    "ب": 10,
    "ت": 17,
    "ث": 1,
    "د": 8,
    "ذ": 3,
    "ر": 9,
    "س": 2,
    "ص": 3,
    "ع": 2,
    "ف": 1,
    "ق": 2,
    "ل": 110,
    "م": 1346,
    "ن": 3282,
    "ه": 1,
    "و": 109,
    "ى": 590,
    "ي": 2861,
}
"""تفكيكُ «ق» بخواتمه كما نُقل؛ عشرون خاتمةً يُفحَص مجموعُها أدناه."""

THE_MARGINALS: Final[dict[str, int]] = {
    "A": 190,
    "B": 2890,
    "C": 2888,
    "J": 166,
    "T": 102,
}
"""هوامشُ البوّابات الخمس كما نُقلت في `results.json`."""

THE_TRANSITIONS: Final[dict[str, int]] = {
    "A→A": 9,
    "A→B": 43,
    "A→C": 35,
    "A→J": 3,
    "A→T": 2,
    "B→A": 42,
    "B→B": 759,
    "B→C": 589,
    "B→J": 33,
    "B→T": 28,
    "C→A": 42,
    "C→B": 576,
    "C→C": 773,
    "C→J": 34,
    "C→T": 21,
    "J→A": 3,
    "J→B": 39,
    "J→C": 33,
    "J→J": 6,
    "J→T": 7,
    "T→A": 2,
    "T→B": 22,
    "T→C": 12,
    "T→J": 2,
    "T→T": 3,
}
"""جدولُ الانتقالات الخمسة في الخمسة كما نُقل؛ مجموعُه يُفحَص أدناه."""

_NW: Final[int] = 77801
_NV: Final[int] = 6236
_NP: Final[int] = 6235
_NTR: Final[int] = 3118
_NTE: Final[int] = 3117

_FIELD_112: Final[int] = 223611
_RAW_ABJAD: Final[int] = 243797
_COMPOUND_HAMZAS: Final[int] = 16082
_THE_FOUR_EXTRA: Final[int] = 5831
_TANWIN_OUTSIDE: Final[int] = 1727

_MARKOV_WHOLE: Final[float] = 4688.915798692156
_MARKOV_FITTED: Final[float] = 4398.7441027578025
_UNIGRAM_CODE: Final[float] = 4518.0773095090935
_GREEDY_CODE: Final[float] = 4529.68694998353
_OPTIMAL_CODE: Final[float] = 4529.68694998353
_FOR_THEN_ON: Final[float] = 3929.5897159494452

_H_LETTER: Final[float] = 4.2043
_H_STATE: Final[float] = 1.7859
_H_LETTER_GIVEN_STATE: Final[float] = 4.1379
_H_STATE_GIVEN_LETTER: Final[float] = 1.7511

_TEST_CE_BASE: Final[float] = 1.4060566676833182
_TEST_CE_FITTED: Final[float] = 1.3900509620491968

_QUOTED_ON_RATE: Final[float] = 0.2133
_QUOTED_PAIR_GAIN: Final[float] = 5.83
_QUOTED_HELD_OUT_GAIN: Final[float] = 4.96

_QUOTED_T_HERE: Final[int] = 102
_QUOTED_T_IN_SPEECH: Final[int] = 209


# --- الفحوصُ المُعادةُ حسابًا ------------------------------------------------


@dataclass(frozen=True, slots=True)
class ArithmeticCheck:
    """متطابقةٌ واحدةٌ تُعاد حسابًا؛ وحكمُها مُشتَقٌّ لا مكتوب."""

    name: str
    statement: str
    genus: CheckGenus
    left: float | None
    right: float | None
    tolerance: float

    def __post_init__(self) -> None:
        _require_text(self.name, "اسمُ الفحص")
        _require_text(self.statement, "بيانُ الفحص")
        if not isinstance(self.genus, CheckGenus):
            raise HamilPhase1DepositError("جنسُ الفحص عضوٌ في `CheckGenus`.")
        if self.tolerance < 0.0:
            raise HamilPhase1DepositError("هامشُ تقريبٍ سالبٌ لا معنى له.")
        uncheckable = self.genus is CheckGenus.REQUIRES_BYTES_NOT_DEPOSITED
        if uncheckable:
            if self.left is not None or self.right is not None:
                raise HamilPhase1DepositError(
                    "فحصٌ موقوفٌ على بايتاتٍ لا يحمل طرفَين محسوبَين؛ "
                    "وحملُهما يُوهِم فحصًا لم يقع."
                )
        elif self.left is None or self.right is None:
            raise HamilPhase1DepositError("فحصٌ قابلٌ للحساب بلا طرفَين ليس فحصًا.")

    @property
    def verdict(self) -> CheckVerdict:
        """الحكمُ مُشتَقًّا من الطرفَين؛ ولا حقلَ يحمله فيُبدَّل وحدَه."""

        if self.genus is CheckGenus.REQUIRES_BYTES_NOT_DEPOSITED:
            return CheckVerdict.NOT_CHECKABLE_HERE
        assert self.left is not None and self.right is not None
        if abs(self.left - self.right) <= self.tolerance:
            return CheckVerdict.AGREES
        return CheckVerdict.CONTRADICTS

    @property
    def gap(self) -> float | None:
        """فرقُ الطرفَين، أو `None` حيث لا طرفَين؛ ولا يُصفَّر الفرقُ تلطّفًا."""

        if self.left is None or self.right is None:
            return None
        return self.left - self.right

    @property
    def is_an_external_confirmation(self) -> bool:
        """أهذا تقاطعُ تنفيذين؟ لا يصدق إلّا على ما أُعيد بتنفيذٍ مستقلٍّ ههنا."""

        return self.genus is CheckGenus.RECOMPUTED_BY_AN_INDEPENDENT_IMPLEMENTATION


def the_chain_rule_gap() -> float:
    """فرقُ تفكيكَي الإنتروبيا المنقولَين؛ ويجب أن يكون صفرًا بالتعريف."""

    return (_H_LETTER + _H_STATE_GIVEN_LETTER) - (_H_STATE + _H_LETTER_GIVEN_STATE)


def the_rate_denominators() -> dict[str, float]:
    """ربحُ ماركوف المنقول مقسومًا على كلّ مقامٍ معلَنٍ في الملفّ نفسِه."""

    gain = _MARKOV_WHOLE - _MARKOV_FITTED
    return {
        "Ntr": gain / _NTR,
        "Nte": gain / _NTE,
        "Np": gain / _NP,
        "Nv": gain / _NV,
    }


def the_stirling_cross_check() -> tuple[ArithmeticCheck, ...]:
    """سترلنج وبِلّ مُعادةً من تنفيذ هذه الشجرة؛ وهو التقاطعُ الحقيقيّ الوحيد."""

    quoted_s28: Final[dict[int, int]] = {
        2: 134217727,
        3: 3812664524766,
        4: 2998587019946701,
        5: 307440364830580800,
        6: 8220146115188676396,
    }
    checks: list[ArithmeticCheck] = []
    for classes, quoted in sorted(quoted_s28.items()):
        checks.append(
            ArithmeticCheck(
                name=f"سترلنج S(28,{classes})",
                statement=(
                    f"عددُ تقسيمات الثمانيةِ والعشرين على {classes} صفوفٍ غيرِ "
                    "خاليةٍ كما نُقل، بإزاء ما يحسبه هذا المستودع"
                ),
                genus=CheckGenus.RECOMPUTED_BY_AN_INDEPENDENT_IMPLEMENTATION,
                left=float(quoted),
                right=float(stirling_second_kind(28, classes)),
                tolerance=0.0,
            )
        )
    checks.append(
        ArithmeticCheck(
            name="سقفُ الجدوى log2 Bell(112)",
            statement="سقفُ الجدوى المنقول 443 بتًّا، بإزاء لوغاريتم بِلّ المحسوب ههنا",
            genus=CheckGenus.RECOMPUTED_BY_AN_INDEPENDENT_IMPLEMENTATION,
            left=443.0,
            right=float(int(log2(bell_number(112)))),
            tolerance=0.0,
        )
    )
    checks.append(
        ArithmeticCheck(
            name="سقفُ الحروف log2 Bell(28)",
            statement="سقفُ تقسيمات الحروف المنقول 72 بتًّا، بإزاء المحسوب ههنا",
            genus=CheckGenus.RECOMPUTED_BY_AN_INDEPENDENT_IMPLEMENTATION,
            left=72.0,
            right=float(int(log2(bell_number(28)))),
            tolerance=0.0,
        )
    )
    return tuple(checks)


def _identity(name: str, statement: str, left: float, right: float) -> ArithmeticCheck:
    return ArithmeticCheck(
        name=name,
        statement=statement,
        genus=CheckGenus.RECOMPUTED_FROM_THE_QUOTED_FIGURES,
        left=left,
        right=right,
        tolerance=0.0,
    )


def _build_checks() -> tuple[ArithmeticCheck, ...]:
    checks: list[ArithmeticCheck] = [
        _identity(
            "مجموعُ الأصناف الأربعة",
            "ث+ع+ز+ق بإزاء عدد الكلمات المُعلَن Nw",
            float(sum(THE_CLASS_COUNTS.values())),
            float(_NW),
        ),
        _identity(
            "تفكيكُ «ق» بخواتمه",
            "مجموعُ العشرين خاتمةً بإزاء صنف «ق» المُعلَن",
            float(sum(THE_QAF_ENDINGS.values())),
            float(THE_CLASS_COUNTS["ق"]),
        ),
        _identity(
            "مصالحةُ العدّ: الإقفال",
            "الحقلُ 112 المرخَّص زائدَ الفارق الكامل، بإزاء الأبجد الخام",
            float(_FIELD_112 + (_RAW_ABJAD - _FIELD_112)),
            float(_RAW_ABJAD),
        ),
        _identity(
            "مصالحةُ العدّ: تفكيكُ الفارق",
            "الهمزاتُ المركّبة زائدَ الزائدين ناقصَ التنوينات، بإزاء الفارق",
            float(_COMPOUND_HAMZAS + _THE_FOUR_EXTRA - _TANWIN_OUTSIDE),
            float(_RAW_ABJAD - _FIELD_112),
        ),
        _identity(
            "مجموعُ الهوامش الخمسة",
            "A+B+C+J+T بإزاء عدد البوّابات المُعلَن Nv",
            float(sum(THE_MARGINALS.values())),
            float(_NV),
        ),
        _identity(
            "مجموعُ الانتقالات",
            "الخمسةُ في الخمسة بإزاء حجم شطر التدريب Ntr",
            float(sum(THE_TRANSITIONS.values())),
            float(_NTR),
        ),
        _identity(
            "قسمةُ الأزواج على الشطرين",
            "Ntr+Nte بإزاء عدد الأزواج Np",
            float(_NTR + _NTE),
            float(_NP),
        ),
        _identity(
            "الأزواجُ من البوّابات",
            "Nv−1 بإزاء عدد الأزواج Np",
            float(_NV - 1),
            float(_NP),
        ),
        _identity(
            "فجوةُ الترتيبين FOR→ON",
            "الفرقُ المنقول −600.097 بإزاء ما تُخرِجه كلفتا الترتيبين",
            _FOR_THEN_ON - _GREEDY_CODE,
            -600.097234034085,
        ),
        _identity(
            "الجشعُ مطابقٌ الاستنفاد",
            "كلفةُ الجشع بإزاء كلفة الأمثل على الحقل نفسِه",
            _GREEDY_CODE,
            _OPTIMAL_CODE,
        ),
        ArithmeticCheck(
            name="قاعدةُ السلسلة في الحقل 112",
            statement=(
                "H(ح)+H(هـ|ح) بإزاء H(هـ)+H(ح|هـ) — متطابقةٌ بالتعريف، "
                "والفرقُ ههنا أكبرُ من تقريبِ أربعِ منازل"
            ),
            genus=CheckGenus.RECOMPUTED_FROM_THE_QUOTED_FIGURES,
            left=_H_LETTER + _H_STATE_GIVEN_LETTER,
            right=_H_STATE + _H_LETTER_GIVEN_STATE,
            tolerance=0.0001,
        ),
        ArithmeticCheck(
            name="معدّلُ ربح ماركوف لكلّ بوّابة",
            statement=(
                "المنقولُ 0.2133 بتًّا/بوّابة بإزاء أقربِ ما تُخرِجه المقامات "
                "المعلَنةُ في الملفّ نفسِه، وهو القسمةُ على Ntr"
            ),
            genus=CheckGenus.RECOMPUTED_FROM_THE_QUOTED_FIGURES,
            left=_QUOTED_ON_RATE,
            right=the_rate_denominators()["Ntr"],
            tolerance=0.0005,
        ),
        ArithmeticCheck(
            name="ربحُ خارج العيّنة",
            statement=(
                "المنقولُ 4.96 بتًّا بإزاء فرقِ الإنتروبيتين المتقاطعتين "
                "مضروبًا في حجم شطر الاختبار"
            ),
            genus=CheckGenus.RECOMPUTED_FROM_THE_QUOTED_FIGURES,
            left=_QUOTED_HELD_OUT_GAIN,
            right=(_TEST_CE_BASE - _TEST_CE_FITTED) * _NTE,
            tolerance=0.01,
        ),
        ArithmeticCheck(
            name="التقسيمُ بإزاء اللاتقسيم",
            statement=(
                "كلفةُ الأمثل بإزاء كلفةِ الأحاديّ: المنقولُ «لا يشتري»، "
                "والمحسوبُ أنّه يبيع بخسارة"
            ),
            genus=CheckGenus.RECOMPUTED_FROM_THE_QUOTED_FIGURES,
            left=_OPTIMAL_CODE,
            right=_UNIGRAM_CODE,
            tolerance=0.0,
        ),
        ArithmeticCheck(
            name="الهامشُ T بين نقلين",
            statement=(
                "T=102 في `results.json` بإزاء T=209 المنقولِ شفاهًا عن "
                "hamil §16؛ والتقاطعُ المُعلَن يُعرَض بأحدهما ويُسكَت عن الآخر"
            ),
            genus=CheckGenus.RECOMPUTED_FROM_THE_QUOTED_FIGURES,
            left=float(_QUOTED_T_HERE),
            right=float(_QUOTED_T_IN_SPEECH),
            tolerance=0.0,
        ),
        ArithmeticCheck(
            name="الهامشُ C بين نقلين",
            statement="C=2,888 في `results.json` بإزاء C≈2,888 المنقولِ عن hamil §16",
            genus=CheckGenus.RECOMPUTED_FROM_THE_QUOTED_FIGURES,
            left=float(THE_MARGINALS["C"]),
            right=2888.0,
            tolerance=0.0,
        ),
        ArithmeticCheck(
            name="ربحُ الزوجيّ المشترك",
            statement=(
                "المنقولُ 5.83 بتًّا/زوجيّ-مشترك: لا مقامَ في الملفّ يُخرِجه، "
                "ولا يُفحَص إلّا بتشغيل الأنبوب على مدوّنته"
            ),
            genus=CheckGenus.REQUIRES_BYTES_NOT_DEPOSITED,
            left=None,
            right=None,
            tolerance=0.0,
        ),
        ArithmeticCheck(
            name="بصمةُ الهياكل 14,870",
            statement=(
                "عددُ الهياكل المُجمَّد في `assert`: موقوفٌ على `mujammad.txt`، "
                "وليست بايتاتُها في هذه الشجرة"
            ),
            genus=CheckGenus.REQUIRES_BYTES_NOT_DEPOSITED,
            left=None,
            right=None,
            tolerance=0.0,
        ),
    ]
    checks.extend(the_stirling_cross_check())
    return tuple(checks)


THE_CHECKS: Final[tuple[ArithmeticCheck, ...]] = _build_checks()


@dataclass(frozen=True, slots=True)
class CodeDefect:
    """عيبٌ موصوفٌ في شيفرةٍ لم تُشغَّل ههنا؛ بنوعه وموضعه ونصّه."""

    locus: str
    statement: str
    genus: DefectGenus

    def __post_init__(self) -> None:
        _require_text(self.locus, "موضعُ العيب")
        _require_text(self.statement, "بيانُ العيب")
        if not isinstance(self.genus, DefectGenus):
            raise HamilPhase1DepositError("نوعُ العيب عضوٌ في `DefectGenus`.")

    @property
    def was_run_in_this_tree(self) -> bool:
        """`False` دائمًا: الوصفُ عن نصٍّ مقروءٍ لا عن تشغيل."""

        return False


THE_CODE_DEFECTS: Final[tuple[CodeDefect, ...]] = (
    CodeDefect(
        locus="dictionary_engine.py — قاعدةُ «ح-جار»",
        statement=(
            'القاعدةُ معلَنةٌ «ب/ل/ك الملتصقة»، والشيفرةُ تفحص `ch in "بل"` — '
            "فالكافُ لا تُطلِق أبدًا، والرقمُ 1,588 محسوبٌ بقاعدتين لا بثلاث"
        ),
        genus=DefectGenus.DECLARED_RULE_NOT_EXECUTED,
    ),
    CodeDefect(
        locus="dictionary_engine.py — `has_shadda`",
        statement=(
            "الدالّةُ معرَّفةٌ ولا تُستدعى قطّ؛ ورقمُ الشدّة يأتي من مسارٍ "
            "آخرَ يقسم على الفراغ، فالقاعدةُ المعلَنةُ غيرُ القاعدةِ المُنفَّذة"
        ),
        genus=DefectGenus.DEFINED_AND_NEVER_CALLED,
    ),
    CodeDefect(
        locus="dictionary_engine.py — `raw_words` بإزاء `Nw`",
        statement=(
            "82,406 بالقسمة على الفراغ و77,801 من `parse_verses`، وبينهما "
            "4,605؛ وتغطيةُ المبني محسوبةٌ على الأوّل والتصنيفُ على الثاني"
        ),
        genus=DefectGenus.TWO_DENOMINATORS_READ_AS_ONE,
    ),
    CodeDefect(
        locus="dictionary_engine.py — `scream`",
        statement=(
            "`raw_words − shadda_words` يُسقِط قاعدةَ الجار كلَّها، فتُعَدّ "
            "1,588 كلمةً مصنَّفةً في «المتبقّي بلا قاعدة»؛ فـ60,701 حدٌّ أعلى "
            "لا متبقٍّ"
        ),
        genus=DefectGenus.A_RESIDUAL_COUNTED_OVER_ITS_OWN_RULE,
    ),
    CodeDefect(
        locus="dictionary_engine.py — الـ`assert` الثلاثة",
        statement=(
            "14,870 و77,801 و3,153 مُجمَّدةٌ في `assert`: مدوّنةٌ مشروعةٌ "
            "مختلفةٌ تُسقِط البرنامجَ بدل أن تُخرِج تقريرَ فرق، و`assert` "
            "يختفي تحت `python -O` فيغيب الحارسُ حين يُحتاج"
        ),
        genus=DefectGenus.A_DATED_FACT_FROZEN_IN_A_GUARD,
    ),
)


@dataclass(frozen=True, slots=True)
class ForeignCorpusNote:
    """مدوّنةُ ذاك البرنامج بإزاء مدوّنتنا؛ والفرقُ مُشتَقٌّ لا مكتوب."""

    their_path: str
    their_length: int
    our_path: str
    our_length: int

    def __post_init__(self) -> None:
        _require_text(self.their_path, "مسارُ مدوّنتهم")
        _require_text(self.our_path, "مسارُ مدوّنتنا")
        if self.their_length < 1 or self.our_length < 1:
            raise HamilPhase1DepositError("طولٌ دون الواحد لا يدخل مقابلة.")

    @property
    def byte_gap(self) -> int:
        """فرقُ الطولين، مُشتَقًّا لا مكتوبًا في حقلٍ ثالث."""

        return self.our_length - self.their_length

    @property
    def are_the_same_corpus(self) -> bool:
        """`False` ما دام الطولان مختلفَين؛ ولا يُقال «قريبةٌ منها»."""

        return self.their_length == self.our_length


THE_FOREIGN_CORPUS: Final[ForeignCorpusNote] = ForeignCorpusNote(
    their_path="mujammad.txt (GlobalQuran)",
    their_length=1306770,
    our_path="corpora/quran-simple-enhanced.txt (Tanzil)",
    our_length=1319901,
)


@dataclass(frozen=True, slots=True)
class HamilPhase1AuditDeposit:
    """الإيداعُ كلُّه: فحوصٌ مُعادةٌ حسابًا، وعيوبٌ موصوفة، ومدوّنةٌ ليست لنا."""

    checks: tuple[ArithmeticCheck, ...]
    defects: tuple[CodeDefect, ...]
    corpus: ForeignCorpusNote

    def __post_init__(self) -> None:
        if not self.checks:
            raise HamilPhase1DepositError("إيداعُ تدقيقٍ بلا فحصٍ واحدٍ ليس تدقيقًا.")
        if not self.defects:
            raise HamilPhase1DepositError("إيداعٌ بلا عيبٍ موصوفٍ يُخفي أحدَ وجهَيه.")
        if not isinstance(self.corpus, ForeignCorpusNote):
            raise HamilPhase1DepositError("لا بدّ من مقابلةِ المدوّنتين بالاسم.")
        seen: set[str] = set()
        for check in self.checks:
            key = comparison_key(check.name)
            if key in seen:
                raise HamilPhase1DepositError(
                    f"فحصٌ مكرّرٌ في الإيداع: {check.name}؛ والتكرارُ يُخفي حكمًا."
                )
            seen.add(key)
        genera = {check.genus for check in self.checks}
        missing = tuple(genus for genus in CheckGenus if genus not in genera)
        if missing:
            raise HamilPhase1DepositError(
                "جنسُ فحصٍ مُسمًّى بلا سجلٍّ في الإيداع: "
                + "، ".join(genus.value for genus in missing)
            )

    def by_verdict(self, verdict: CheckVerdict) -> tuple[ArithmeticCheck, ...]:
        """فحوصُ حكمٍ واحد؛ والقسمةُ تُشتَقّ من الحساب عند كلّ نداء."""

        return tuple(check for check in self.checks if check.verdict is verdict)

    @property
    def agreement_count(self) -> int:
        """عددُ ما تطابق، مُشتَقًّا من الفحوص لا مكتوبًا في نثر."""

        return len(self.by_verdict(CheckVerdict.AGREES))

    @property
    def contradiction_count(self) -> int:
        """عددُ ما خالف، مُشتَقًّا كذلك؛ ولا يُخفَّض ولا يُلطَّف."""

        return len(self.by_verdict(CheckVerdict.CONTRADICTS))

    @property
    def cross_checked_count(self) -> int:
        """ما أُعيد بتنفيذٍ مستقلٍّ ههنا وحدَه؛ وهو التقاطعُ الحقيقيّ."""

        return sum(1 for check in self.checks if check.is_an_external_confirmation)

    @property
    def any_check_measures_the_foreign_corpus(self) -> bool:
        """`False` دائمًا: لا بايتَ من `mujammad.txt` في هذه الشجرة."""

        return any(
            check.genus is CheckGenus.REQUIRES_BYTES_NOT_DEPOSITED
            and check.verdict is not CheckVerdict.NOT_CHECKABLE_HERE
            for check in self.checks
        )

    @property
    def deposit_is_operative(self) -> bool:
        """`False` دائمًا: لا بوّابةَ في هذا المستودع تقرأ هذا الإيداع."""

        return False


HAMIL_PHASE1_AUDIT_DEPOSIT: Final[HamilPhase1AuditDeposit] = HamilPhase1AuditDeposit(
    checks=THE_CHECKS,
    defects=THE_CODE_DEFECTS,
    corpus=THE_FOREIGN_CORPUS,
)


def _verify_every_verdict_is_recomputed() -> None:
    """مبرهنة: لا حقلَ حكمٍ في هذا الملفّ؛ فالحكمُ يتبع الطرفَين حتمًا."""

    for _dataclass in (ArithmeticCheck, CodeDefect, ForeignCorpusNote):
        for _field in fields(_dataclass):
            if "verdict" in _field.name:
                raise RuntimeError("a check carries a hand-written verdict field")
            if any(token in _field.name for token in _FORBIDDEN_FIELD_TOKENS):
                raise RuntimeError("a deposit type carries a forbidden field")


def _verify_the_contradictions_are_present() -> None:
    """مبرهنة: الإيداعُ يحمل مخالفاتٍ فعلًا؛ وإيداعٌ كلُّه تطابقٌ يُتّهَم."""

    if HAMIL_PHASE1_AUDIT_DEPOSIT.contradiction_count < 1:
        raise RuntimeError("the deposit records no contradiction at all")
    if HAMIL_PHASE1_AUDIT_DEPOSIT.cross_checked_count < 1:
        raise RuntimeError("the deposit records no independent cross-check")


_verify_every_verdict_is_recomputed()
_verify_the_contradictions_are_present()

if HAMIL_PHASE1_AUDIT_DEPOSIT.deposit_is_operative:  # pragma: no cover - guard
    raise RuntimeError("the deposit declares itself operative")
if HAMIL_PHASE1_AUDIT_DEPOSIT.any_check_measures_the_foreign_corpus:
    raise RuntimeError("a check claims to measure a corpus absent from this tree")
