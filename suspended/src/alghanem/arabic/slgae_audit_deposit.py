"""إيداعُ تدقيقِ SLGAE: تقريرٌ عن بحثٍ خارجيّ، يُسجَّل بقيده ولا يُصدَّق.

وصل إلى هذه الشجرة تقريرُ تدقيقٍ على بحثٍ خارجيٍّ مُسمّى SLGAE: ما صمد فيه، وما
سقط، وما قام نتيجةً وسقط سندُه، وما كُشف فيه بالحساب. وكلُّ رقمٍ في ذلك التقرير
— قيمُ z، وأرجحياتُ فيشر، وفروقُ BIC، وARI، وλ — وصل **سردًا من محادثةٍ أخرى**،
ولا بايتَ واحدًا في `corpora/` ولا في `case_data/` يُعيد اشتقاقَ واحدٍ منها.
فالقاعدةُ الحاكمة مكتوبةٌ سلفًا في `alghanem.program.direct_certainty`::

    QuotedFigure       != MeasuredFigure
    NamedCriterion     != ABuiltGate
    AStandingResult    != AStandingSupport

**أوّلًا: هذه الوحدةُ سجلٌّ لا إعادةُ تجربة.** لا تُجري شيئًا من تجارب SLGAE،
ولا تُصدِّق واحدةً منها، ولا تنفيها؛ إنّما تُثبِّت ما ادُّعي، وجنسَ سنده، وقيدَ
قراءته، في مفرداتٍ مغلقةٍ تُرفَض القيمةُ خارجها عند الإنشاء لا عند القراءة
(`A_DEPOSITED_AUDIT_IS_NOT_A_RERUN_EXPERIMENT`).

**وثانيًا: كلُّ رقمٍ منقولٍ هنا له نظيرٌ في السجلّ الواحد.** لا يُفتَح لهذا
التقرير مخزنٌ ثانٍ للأرقام: كلُّ رقمٍ يُسجَّل في
`alghanem.program.direct_certainty.REPORTED_UNVERIFIED_FIGURES` بجنس مصدره
وبقيده، ويُقابَل الإيداعُ بالسجلّ في الشواهد. واتّجاهُ الاعتماد واحدٌ لا
يُعكَس: `program` يقرأ `arabic`، وهذه الوحدةُ لا تستورد `program` ولا `kernel`
(`THE_FIGURES_LIVE_IN_THE_ONE_REGISTER_NOT_IN_A_SECOND_STORE`).

**وثالثًا: السندُ الساقطُ جنسٌ ثالثٌ لا هو نجاحٌ ولا فشل.** أن تقوم نتيجةٌ ثمّ
يسقط سندُها — لدائريّة الوسوم، أو لحكمٍ يدويٍّ لاحق، أو لقربٍ من التعريف، أو
لعتبةٍ اختارها الباحثُ نفسُه — حالٌ لم يكن لها اسمٌ في هذه الشجرة قبل اليوم.
و`SupportStanding.RESULT_STANDS_SUPPORT_WITHDRAWN` تُسمّيها ولا تقرؤها سقوطًا،
ولا تقرؤها صمودًا (`A_WITHDRAWN_SUPPORT_IS_NOT_A_REFUTED_RESULT`).

**ورابعًا: التناقضان الحسابيّان موقوفان على بايتاتٍ لم تُودَع.** عدمُ إعادةِ
بناء λ، وتعذُّرُ نسبة γ/β، دعويان **قابلتان للفحص لو** أُودع جدولُ exp(β)
بايتاتٍ في هذه الشجرة. ولم يُودَع؛ فتُسجَّلان غيرَ قابلتين لإعادة الاشتقاق هنا،
ولا يُقال في نثرٍ إنّهما «فُحصتا في هذه الشجرة». وتسميةُ معيارٍ لا تجعله
بوّابةً مبنيّة (`A_NAMED_CRITERION_IS_NOT_A_BUILT_GATE`).

**وخامسًا: أرقامُ بنائنا نحن جنسان لا جنسٌ واحد.** ما يُقاس من هذه الشجرة
يُقاس عند القراءة — عددُ وحدات المصدر، وعددُ دوالّ الاختبار — ويُقابَل به
المنقول في `the_quoted_build_counts_against_disk()`؛ ولا يُجمَّد المنقولُ ولا
يُكتَب مكانَ المقيس. وما لا يُقاس هنا — ثماني بتّاتٍ لكلّ وحدةٍ مشكولة،
و224 مُسنَدًا و32 مردودًا — يبقى خبرًا بقيده، لأنّ شجرةً أخرى قاسته لا هذه
(`A_COUNT_FROM_ANOTHER_TREE_IS_NOT_A_MEASUREMENT_HERE`).

**وسادسًا: الفشلُ المُسمّى يُودَع فشلًا لا «عملًا جاريًا».** محورُ المخرج لا
يحسم الحرف، ومحورُ الحركة حسم صفرًا، والصفاتُ المولودة تترك متعادلاتٍ
وموقوفات: هذه تُودَع مانعًا أو تأجيلًا بالاسم، لا بصيغةِ ما سيتمّ غدًا
(`A_NAMED_FAILURE_IS_DEPOSITED_AS_ONE`).

**خمولٌ سلطويّ**: لا ولادةَ هنا ولا حكمَ ولادةٍ ولا تجميدَ `E0`، ولا استيرادَ
من `kernel/`، ولا بوّابةَ فيه تقرأ هذه الوحدة.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, fields
from enum import Enum
from pathlib import Path
from typing import Final

from .text_key import comparison_key

__all__ = [
    "A_COUNT_FROM_ANOTHER_TREE_IS_NOT_A_MEASUREMENT_HERE",
    "A_DEPOSITED_AUDIT_IS_NOT_A_RERUN_EXPERIMENT",
    "A_NAMED_CRITERION_IS_NOT_A_BUILT_GATE",
    "A_NAMED_FAILURE_IS_DEPOSITED_AS_ONE",
    "A_WITHDRAWN_SUPPORT_IS_NOT_A_REFUTED_RESULT",
    "SLGAE_AUDIT_DEPOSIT",
    "SLGAE_NAMED_RESIDUALS",
    "THE_FIGURES_LIVE_IN_THE_ONE_REGISTER_NOT_IN_A_SECOND_STORE",
    "BuildStanding",
    "FailureGenus",
    "IndependentMeasure",
    "OwnBuildRecord",
    "QuotedAgainstMeasured",
    "QuotedFigure",
    "ReDerivability",
    "SlgaeAuditDeposit",
    "SlgaeDepositError",
    "SlgaeDiscrepancy",
    "SlgaeFinding",
    "SlgaeOutcome",
    "SlgaeSection",
    "SupportDefect",
    "SupportStanding",
    "WithdrawnSupportRecord",
    "source_module_count",
    "counted_test_functions",
    "the_quoted_build_counts_against_disk",
]


class SlgaeDepositError(ValueError):
    """رُفض مدخلٌ خارج الإيداع المُجمَّد؛ ولا يُحمَل على أقرب حالة."""


class SlgaeSection(Enum):
    """مواضعُ التقرير المُسمّاة؛ لا موضعَ خارجها يُقبَل هنا."""

    GROSS_STRUCTURE = "البنية_الكبرى"
    MARKOV_FIVE_YA = "ماركوف_٥ي"
    VOWEL_FIRST_FIVE_KAF = "تجربتا_٥ك"
    OUR_OWN_BUILD = "بناؤنا_نحن"


class SlgaeOutcome(Enum):
    """منزلةُ النتيجة في التقرير: صمدت أو سقطت، ولا ثالثَ في هذا الحقل."""

    HELD_WITH_INDEPENDENT_MEASURE = "صمد_بمقياسٍ_مستقلّ"
    FAILED_NAMED = "سقط_مُسمًّى"


class IndependentMeasure(Enum):
    """سببُ قوّةِ ما صمد؛ ولا صمودَ يُقبَل هنا بلا واحدٍ منهما مُسمًّى."""

    PREREGISTERED_PREDICTION = "تنبؤ_مسجّل_قبل_الرؤية"
    MEASURED_OFF_THE_RULE = "مقياس_مستقلّ_عن_القاعدة"


class FailureGenus(Enum):
    """نوعُ السقوط؛ والسقوطُ بلا نوعٍ مُسمًّى خبرٌ ناقص."""

    BEATEN_BY_A_RIVAL = "هُزم_بمنافس"
    CONTRADICTED_BY_THE_COUNT = "خالفه_العدّ"
    FELL_STATISTICALLY = "سقط_إحصائيًّا"
    DIRECTION_REVERSED = "انقلب_اتّجاهه"
    FRAGILE_UNDER_SCOPE_CHANGE = "هشٌّ_بتغيّر_النطاق"
    METHOD_COLLAPSED = "انهارت_طريقتُه"


class SupportStanding(Enum):
    """جنسٌ ثالثٌ: النتيجةُ قائمةٌ والسندُ ساقط، ولا يُقرأ نجاحًا ولا فشلًا."""

    RESULT_STANDS_SUPPORT_WITHDRAWN = "النتيجة_قائمة_والسند_ساقط"


class SupportDefect(Enum):
    """عِلّةُ سقوطِ السند، مُسمّاةً لا مُجمَلة."""

    CIRCULAR_ON_THE_TAGS = "دائريّة_الوسوم"
    MANUAL_POST_HOC_JUDGMENT = "حكم_يدويّ_لاحق"
    NEAR_DEFINITIONAL = "قريب_من_التعريف"
    ANALYST_CHOSEN_THRESHOLD = "عتبةٌ_اختارها_الباحث"
    TRADITIONAL_CLASSIFICATION_RENAMED = "تصنيفٌ_تراثيٌّ_بأسماءٍ_جديدة"


class ReDerivability(Enum):
    """قيدُ قراءةِ الرقم: أيُعاد اشتقاقُه من هذه الشجرة أم لا؟"""

    NOT_RE_DERIVABLE_IN_THIS_TREE = "غير_قابلٍ_لإعادة_الاشتقاق_في_هذه_الشجرة"
    RE_DERIVABLE_FROM_THIS_TREE = "قابلٌ_لإعادة_الاشتقاق_من_هذه_الشجرة"


class BuildStanding(Enum):
    """منزلةُ ما في بنائنا نحن: مانعٌ مقيس، أو تأجيلٌ مُسمًّى، أو قياسٌ قائم."""

    BLOCKED_BY_A_MEASURED_ZERO = "مانعٌ_بصفرٍ_مقيس"
    DEFERRED_UNDECIDED = "مؤجَّلٌ_غيرُ_محسوم"
    MEASURED_AND_STANDING = "مقيسٌ_قائم"


A_DEPOSITED_AUDIT_IS_NOT_A_RERUN_EXPERIMENT: Final[str] = (
    "A_DEPOSITED_AUDIT_IS_NOT_A_RERUN_EXPERIMENT: هذا الإيداعُ يُثبِّت ما "
    "ادّعاه تقريرُ تدقيقٍ خارجيّ، ولا يُعيد تجربةً منه ولا يُصدِّقها ولا "
    "ينفيها؛ فمن قرأ سطرًا منه نتيجةً لهذه الشجرة قرأ غيرَ ما كُتب"
)

THE_FIGURES_LIVE_IN_THE_ONE_REGISTER_NOT_IN_A_SECOND_STORE: Final[str] = (
    "THE_FIGURES_LIVE_IN_THE_ONE_REGISTER_NOT_IN_A_SECOND_STORE: كلُّ رقمٍ "
    "منقولٍ هنا له نظيرٌ في `REPORTED_UNVERIFIED_FIGURES` بجنس مصدره وبقيده؛ "
    "ولا يُفتَح لهذا التقرير مخزنٌ ثانٍ للأرقام، ولا تستورد هذه الوحدةُ "
    "`program` فينعكسَ اتّجاهُ الاعتماد"
)

A_WITHDRAWN_SUPPORT_IS_NOT_A_REFUTED_RESULT: Final[str] = (
    "A_WITHDRAWN_SUPPORT_IS_NOT_A_REFUTED_RESULT: سقوطُ السند غيرُ سقوط "
    "النتيجة؛ فما سُجِّل تحت `RESULT_STANDS_SUPPORT_WITHDRAWN` لا يُقرأ فشلًا "
    "مُسمًّى ولا يُقرأ صمودًا، وإنّما يُقرأ نتيجةً بلا شهادةٍ تحملها"
)

A_NAMED_CRITERION_IS_NOT_A_BUILT_GATE: Final[str] = (
    "A_NAMED_CRITERION_IS_NOT_A_BUILT_GATE: λ و γ/β دعويان حسابيّتان قابلتان "
    "للفحص لو أُودع جدولُ exp(β) بايتاتٍ في هذه الشجرة؛ ولم يُودَع، فلا يُقال "
    "إنّهما فُحصتا هنا، وتسميةُ المعيار لا تُنشئ البوّابة"
)

A_COUNT_FROM_ANOTHER_TREE_IS_NOT_A_MEASUREMENT_HERE: Final[str] = (
    "A_COUNT_FROM_ANOTHER_TREE_IS_NOT_A_MEASUREMENT_HERE: عددُ الملفّات وعددُ "
    "الاختبارات المنقولان لقطةٌ من شجرةٍ أخرى أو من وقتٍ آخر؛ فيُقابَلان بما "
    "يقيسه القرصُ الآن في `the_quoted_build_counts_against_disk`، ولا يُجمَّد "
    "المنقولُ ولا يُكتَب مكانَ المقيس"
)

A_NAMED_FAILURE_IS_DEPOSITED_AS_ONE: Final[str] = (
    "A_NAMED_FAILURE_IS_DEPOSITED_AS_ONE: ما لم يُحسَم يُودَع مانعًا أو "
    "تأجيلًا بالاسم، لا بصيغةِ عملٍ جارٍ؛ و«حسم صفرًا» خبرٌ مقيسٌ يُكتَب كما "
    "هو ولا يُلطَّف"
)

SLGAE_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "A_DEPOSITED_AUDIT_IS_NOT_A_RERUN_EXPERIMENT": (
        A_DEPOSITED_AUDIT_IS_NOT_A_RERUN_EXPERIMENT
    ),
    "THE_FIGURES_LIVE_IN_THE_ONE_REGISTER_NOT_IN_A_SECOND_STORE": (
        THE_FIGURES_LIVE_IN_THE_ONE_REGISTER_NOT_IN_A_SECOND_STORE
    ),
    "A_WITHDRAWN_SUPPORT_IS_NOT_A_REFUTED_RESULT": (
        A_WITHDRAWN_SUPPORT_IS_NOT_A_REFUTED_RESULT
    ),
    "A_NAMED_CRITERION_IS_NOT_A_BUILT_GATE": A_NAMED_CRITERION_IS_NOT_A_BUILT_GATE,
    "A_COUNT_FROM_ANOTHER_TREE_IS_NOT_A_MEASUREMENT_HERE": (
        A_COUNT_FROM_ANOTHER_TREE_IS_NOT_A_MEASUREMENT_HERE
    ),
    "A_NAMED_FAILURE_IS_DEPOSITED_AS_ONE": A_NAMED_FAILURE_IS_DEPOSITED_AS_ONE,
}
"""ما لا تحسمه هذه الوحدة، مُسمًّى هنا لا متروكًا ليُفترَض."""

_FORBIDDEN_FIELD_TOKENS: Final[tuple[str, ...]] = (
    "verdict",
    "birth",
    "certificate",
    "proof",
    "score",
    "freeze",
)


def _require_text(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SlgaeDepositError(
            f"{field_name} يجب أن يكون نصًّا غير فارغ؛ ولا يُقبَل فيه الفراغ صمتًا."
        )
    return value


@dataclass(frozen=True, slots=True)
class QuotedFigure:
    """رقمٌ وصل سردًا، بموضوعه ونصّه وقيد قراءته؛ ولا رقمَ هنا بلا قيد."""

    subject: str
    figure_text: str
    rederivability: ReDerivability

    def __post_init__(self) -> None:
        _require_text(self.subject, "موضوعُ الرقم")
        _require_text(self.figure_text, "نصُّ الرقم")
        if not isinstance(self.rederivability, ReDerivability):
            raise SlgaeDepositError("قيدُ الرقم عضوٌ في `ReDerivability`.")

    @property
    def is_measured_in_this_tree(self) -> bool:
        """`False` على كلّ رقمٍ منقول: النقلُ ليس قياسًا ولو صدق."""

        return False


@dataclass(frozen=True, slots=True)
class SlgaeFinding:
    """نتيجةٌ واحدةٌ من التقرير: صمدت بمقياسٍ مُسمًّى، أو سقطت بنوعٍ مُسمًّى."""

    experiment: str
    section: SlgaeSection
    statement: str
    figure: QuotedFigure
    outcome: SlgaeOutcome
    independent_measure: IndependentMeasure | None
    failure_genus: FailureGenus | None

    def __post_init__(self) -> None:
        _require_text(self.experiment, "اسمُ التجربة")
        _require_text(self.statement, "نصُّ النتيجة")
        if not isinstance(self.section, SlgaeSection):
            raise SlgaeDepositError("الموضعُ عضوٌ في `SlgaeSection`.")
        if not isinstance(self.outcome, SlgaeOutcome):
            raise SlgaeDepositError("المنزلةُ عضوٌ في `SlgaeOutcome`.")
        if not isinstance(self.figure, QuotedFigure):
            raise SlgaeDepositError("كلُّ نتيجةٍ مقرونةٌ برقمٍ مُسجَّلٍ بقيده.")
        if self.section is SlgaeSection.OUR_OWN_BUILD:
            raise SlgaeDepositError(
                "بناؤنا نحن لا يُسجَّل نتيجةً من نتائج البحث الخارجيّ؛ "
                "وله `OwnBuildRecord` بابًا على حدة."
            )
        held = self.outcome is SlgaeOutcome.HELD_WITH_INDEPENDENT_MEASURE
        if held:
            if not isinstance(self.independent_measure, IndependentMeasure):
                raise SlgaeDepositError(
                    "لا صمودَ بلا مقياسٍ مستقلٍّ مُسمًّى؛ والصمودُ المُرسَل دعوى."
                )
            if self.failure_genus is not None:
                raise SlgaeDepositError("ما صمد لا يحمل نوعَ سقوط.")
        else:
            if not isinstance(self.failure_genus, FailureGenus):
                raise SlgaeDepositError(
                    "لا سقوطَ بلا نوعٍ مُسمًّى؛ والسقوطُ المُجمَل خبرٌ ناقص."
                )
            if self.independent_measure is not None:
                raise SlgaeDepositError("ما سقط لا يحمل مقياسَ صمود.")

    @property
    def held(self) -> bool:
        """أصمدت هذه النتيجةُ في التقرير؟ مُشتَقٌّ من المنزلة لا حقلٌ ثانٍ."""

        return self.outcome is SlgaeOutcome.HELD_WITH_INDEPENDENT_MEASURE


@dataclass(frozen=True, slots=True)
class WithdrawnSupportRecord:
    """نتيجةٌ قائمةٌ سقط سندُها؛ بعلّةِ السقوط مُسمّاةً وبنصّها."""

    subject: str
    statement: str
    standing: SupportStanding
    defect: SupportDefect

    def __post_init__(self) -> None:
        _require_text(self.subject, "موضوعُ السند")
        _require_text(self.statement, "بيانُ سقوط السند")
        if self.standing is not SupportStanding.RESULT_STANDS_SUPPORT_WITHDRAWN:
            raise SlgaeDepositError(
                "لا منزلةَ في هذا الباب غيرُ `RESULT_STANDS_SUPPORT_WITHDRAWN`."
            )
        if not isinstance(self.defect, SupportDefect):
            raise SlgaeDepositError("عِلّةُ السقوط عضوٌ في `SupportDefect`.")

    @property
    def result_is_refuted(self) -> bool:
        """`False` دائمًا: سقوطُ السند ليس نقضًا للنتيجة."""

        return False


@dataclass(frozen=True, slots=True)
class SlgaeDiscrepancy:
    """تناقضٌ كشفه الفحصُ بالحساب لا بالقراءة، بأرقامه وقيدِ فحصها."""

    name: str
    statement: str
    figures: tuple[QuotedFigure, ...]
    checkable_if_bytes_were_deposited: bool

    def __post_init__(self) -> None:
        _require_text(self.name, "اسمُ التناقض")
        _require_text(self.statement, "بيانُ التناقض")
        if not self.figures:
            raise SlgaeDepositError("تناقضٌ بلا رقمٍ مُسجَّلٍ ليس تناقضًا مفحوصًا.")
        seen: set[str] = set()
        for figure in self.figures:
            if not isinstance(figure, QuotedFigure):
                raise SlgaeDepositError("كلُّ رقمٍ هنا `QuotedFigure` بقيده.")
            if figure.rederivability is not (
                ReDerivability.NOT_RE_DERIVABLE_IN_THIS_TREE
            ):
                raise SlgaeDepositError(
                    "أرقامُ التناقضات وصلت سردًا، ولا تُسجَّل قابلةً لإعادة "
                    "الاشتقاق من هذه الشجرة."
                )
            key = comparison_key(figure.subject)
            if key in seen:
                raise SlgaeDepositError(
                    f"موضوعٌ مكرّرٌ في تناقض {self.name}: {figure.subject}."
                )
            seen.add(key)

    @property
    def was_checked_in_this_tree(self) -> bool:
        """`False` دائمًا: لا بايتاتِ التقرير في هذه الشجرة فتُفحَص."""

        return False


@dataclass(frozen=True, slots=True)
class OwnBuildRecord:
    """سجلٌّ من بنائنا نحن: مقيسٌ قائم، أو مانعٌ بصفر، أو تأجيلٌ مُسمًّى."""

    subject: str
    statement: str
    standing: BuildStanding
    figure: QuotedFigure

    def __post_init__(self) -> None:
        _require_text(self.subject, "موضوعُ السجلّ")
        _require_text(self.statement, "بيانُ السجلّ")
        if not isinstance(self.standing, BuildStanding):
            raise SlgaeDepositError("المنزلةُ عضوٌ في `BuildStanding`.")
        if not isinstance(self.figure, QuotedFigure):
            raise SlgaeDepositError("كلُّ سجلٍّ مقرونٌ برقمٍ مُسجَّلٍ بقيده.")

    @property
    def is_work_in_progress(self) -> bool:
        """`False` دائمًا: ما لم يُحسَم يُودَع فشلًا مُسمًّى لا عملًا جاريًا."""

        return False


@dataclass(frozen=True, slots=True)
class QuotedAgainstMeasured:
    """منقولٌ بإزاء مقيس؛ والمقيسُ يُقرأ من القرص عند كلّ نداء."""

    subject: str
    quoted: int
    measured: int

    def __post_init__(self) -> None:
        _require_text(self.subject, "موضوعُ المقابلة")
        if self.quoted < 1 or self.measured < 1:
            raise SlgaeDepositError("عددٌ دون الواحد لا يدخل مقابلةً.")

    @property
    def agrees(self) -> bool:
        """أيطابق المنقولُ ما يقيسه القرصُ الآن؟ يُشتَقّ ولا يُكتَب."""

        return self.quoted == self.measured


def _source_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _repository_root() -> Path:
    return _source_root().parent.parent


def source_module_count() -> int:
    """عددُ وحدات المصدر تحت `src/alghanem/`، مقيسًا من القرص الآن."""

    return sum(1 for path in _source_root().rglob("*.py") if path.is_file())


def counted_test_functions() -> int:
    """عددُ دوالّ الاختبار المعدودةِ نصًّا تحت `tests/`، بلا تشغيلٍ لها."""

    tests_root = _repository_root() / "tests"
    if not tests_root.is_dir():
        raise SlgaeDepositError("شجرةُ الشواهد غيرُ قائمة؛ والعدُّ يقف ولا يُقدَّر.")
    total = 0
    for path in sorted(tests_root.rglob("test_*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                if node.name.startswith("test_"):
                    total += 1
    return total


THE_QUOTED_MODULE_COUNT: Final[int] = 424
"""عددُ الملفّات كما نُقل في التقرير؛ لقطةٌ من وقتٍ آخر، تُقابَل ولا تُجمَّد."""

THE_QUOTED_TEST_COUNT: Final[int] = 62
"""عددُ الاختبارات كما نُقل في التقرير؛ لقطةٌ من وقتٍ آخر، تُقابَل ولا تُجمَّد."""


def the_quoted_build_counts_against_disk() -> tuple[QuotedAgainstMeasured, ...]:
    """المنقولان عن بنائنا بإزاء ما يقيسه القرصُ الآن، لا بإزاء رقمٍ مُجمَّد."""

    return (
        QuotedAgainstMeasured(
            subject="عددُ وحدات المصدر التي يمرّ عليها الفحصُ الساكن",
            quoted=THE_QUOTED_MODULE_COUNT,
            measured=source_module_count(),
        ),
        QuotedAgainstMeasured(
            subject="عددُ دوالّ الاختبار المعدودةِ نصًّا",
            quoted=THE_QUOTED_TEST_COUNT,
            measured=counted_test_functions(),
        ),
    )


_QUOTED: Final = ReDerivability.NOT_RE_DERIVABLE_IN_THIS_TREE


def _held(
    experiment: str,
    section: SlgaeSection,
    statement: str,
    subject: str,
    figure_text: str,
    measure: IndependentMeasure,
) -> SlgaeFinding:
    return SlgaeFinding(
        experiment=experiment,
        section=section,
        statement=statement,
        figure=QuotedFigure(
            subject=subject, figure_text=figure_text, rederivability=_QUOTED
        ),
        outcome=SlgaeOutcome.HELD_WITH_INDEPENDENT_MEASURE,
        independent_measure=measure,
        failure_genus=None,
    )


def _failed(
    experiment: str,
    section: SlgaeSection,
    statement: str,
    subject: str,
    figure_text: str,
    genus: FailureGenus,
) -> SlgaeFinding:
    return SlgaeFinding(
        experiment=experiment,
        section=section,
        statement=statement,
        figure=QuotedFigure(
            subject=subject, figure_text=figure_text, rederivability=_QUOTED
        ),
        outcome=SlgaeOutcome.FAILED_NAMED,
        independent_measure=None,
        failure_genus=genus,
    )


THE_HELD: Final[tuple[SlgaeFinding, ...]] = (
    _held(
        experiment="تجنّبُ الجذور: الكتلُ الخمس وصفاتُها",
        section=SlgaeSection.GROSS_STRUCTURE,
        statement=("خمسُ كتلٍ وصفاتُها مُستخرَجةٌ من تجنّب الجذور، ثابتةٌ في أ وب " "وQAC معًا"),
        subject="قيمتا z في كتل تجنّب الجذور بحسب تقرير SLGAE",
        figure_text="z = −9.4 و z = −8.4",
        measure=IndependentMeasure.MEASURED_OFF_THE_RULE,
    ),
    _held(
        experiment="التركيباتُ التسعَ عشرةَ الممنوعة",
        section=SlgaeSection.GROSS_STRUCTURE,
        statement="التركيباتُ التسعَ عشرةَ الممنوعةُ غائبةٌ عن الجذوع كلِّها",
        subject="غيابُ التركيبات الممنوعة عن الجذوع بحسب تقرير SLGAE",
        figure_text="0 من 4,331 جذعًا",
        measure=IndependentMeasure.PREREGISTERED_PREDICTION,
    ),
    _held(
        experiment="المقاطعُ فائقةُ الثقل في الوصل",
        section=SlgaeSection.GROSS_STRUCTURE,
        statement=(
            "انحصارُ المقاطع فائقة الثقل في الوصل، وكلُّها مُفسَّرة، ولا حالةَ "
            "غيرَ مُفسَّرة؛ ودعوى «لا حالة» تنتقض بحالةٍ واحدة"
        ),
        subject="نسبةُ المقاطع فائقة الثقل في الوصل بحسب تقرير SLGAE",
        figure_text="1.43% وكلُّها مُفسَّرة",
        measure=IndependentMeasure.MEASURED_OFF_THE_RULE,
    ),
    _held(
        experiment="الابتداءُ بساكنٍ دون إصلاح",
        section=SlgaeSection.GROSS_STRUCTURE,
        statement="لا بدايةَ بساكنٍ دون إصلاحٍ ألبتّة، بلا استثناءٍ في المقام",
        subject="بداياتُ الساكن دون إصلاح بحسب تقرير SLGAE",
        figure_text="صفرُ بدايةٍ بساكنٍ دون إصلاح",
        measure=IndependentMeasure.PREREGISTERED_PREDICTION,
    ),
    _held(
        experiment="الرباعيُّ المكرَّر من الثلاثيّ المُضعَّف",
        section=SlgaeSection.GROSS_STRUCTURE,
        statement="الرباعيُّ المكرَّر يخرج من الثلاثيّ المُضعَّف فوق المصادفة",
        subject="الرباعيُّ المكرَّر من الثلاثيّ المُضعَّف بحسب تقرير SLGAE",
        figure_text="16/40 = 40% مقابل 0.67% مصادفةً، p ≈ 0.0015",
        measure=IndependentMeasure.PREREGISTERED_PREDICTION,
    ),
    _held(
        experiment="الحلقُ وعينُ المضارع",
        section=SlgaeSection.GROSS_STRUCTURE,
        statement=(
            "الحلقُ يقترن بالفتح في عين المضارع اقترانًا هو أصغرُ أرجحيّةٍ في " "التقرير كلِّه"
        ),
        subject="اقترانُ الحلق بالفتح في عين المضارع بحسب تقرير SLGAE",
        figure_text="81% مقابل 17%، Fisher p = 1.5×10⁻¹⁴",
        measure=IndependentMeasure.MEASURED_OFF_THE_RULE,
    ),
    _held(
        experiment="الفتحُ بعد إنّ على نصٍّ مشكولٍ بلا وسوم",
        section=SlgaeSection.GROSS_STRUCTURE,
        statement=(
            "قِيس على الحركات المكتوبة لا على وسوم مُعرِبٍ، فنجا وحدَه من تهمة "
            "الدائريّة، ولم تقع ضمّةٌ واحدة"
        ),
        subject="الفتحُ بعد إنّ على النصّ المشكول بحسب تقرير SLGAE",
        figure_text="500/548 = 91.2% ولا ضمّةَ واحدة",
        measure=IndependentMeasure.MEASURED_OFF_THE_RULE,
    ),
    _held(
        experiment="ماركوف P3: التعيينُ بين المستويات",
        section=SlgaeSection.MARKOV_FIVE_YA,
        statement="التعيينُ لا ينتقل بين المستويات، وكلُّ الارتباطات دون الحدّ",
        subject="ارتباطاتُ P3 بين المستويات بحسب تقرير SLGAE",
        figure_text="كلُّ |ρ| ≤ 0.15",
        measure=IndependentMeasure.PREREGISTERED_PREDICTION,
    ),
    _held(
        experiment="V0: الواو والياء وصائتُهما",
        section=SlgaeSection.VOWEL_FIRST_FIVE_KAF,
        statement="الواو والياء تتجنّبان صائتَهما، والواوُ المضمومةُ هي الأدنى",
        subject="تجنّبُ الواو والياء صائتَهما بحسب تقرير SLGAE",
        figure_text="وُ = 0.19 وهي الأدنى",
        measure=IndependentMeasure.PREREGISTERED_PREDICTION,
    ),
    _held(
        experiment="الإعلالُ: الانغلاقُ والموقع",
        section=SlgaeSection.VOWEL_FIRST_FIVE_KAF,
        statement="الانغلاقُ أقوى من الموقع في الإعلال، وهو تنبؤٌ سُجِّل قبل العدّ",
        subject="الانغلاقُ مقابل الموقع في الإعلال بحسب تقرير SLGAE",
        figure_text="47.6% مقابل 38.1%",
        measure=IndependentMeasure.PREREGISTERED_PREDICTION,
    ),
)

THE_FAILURES: Final[tuple[SlgaeFinding, ...]] = (
    _failed(
        experiment="أوزانُ شابلي مقابل تقسيم الخليل",
        section=SlgaeSection.GROSS_STRUCTURE,
        statement=(
            "الجدولُ السباعيُّ الموزون هُزم في التنبؤ بالتنافر بتقسيمٍ تراثيّ " "لم يُوزَن"
        ),
        subject="تنبؤُ شابلي مقابل الخليل بالتنافر بحسب تقرير SLGAE",
        figure_text="ρ = 0.39 للخليل مقابل ρ = 0.18 لشابلي",
        genus=FailureGenus.BEATEN_BY_A_RIVAL,
    ),
    _failed(
        experiment="دعوى «المجرّد لا ينتج CVC»",
        section=SlgaeSection.GROSS_STRUCTURE,
        statement="العدُّ خالف الدعوى مباشرةً، فسقطت بلا تأويل",
        subject="أوزانُ المجرّد التي فيها CVC بحسب تقرير SLGAE",
        figure_text="26 وزنًا فيه CVC",
        genus=FailureGenus.CONTRADICTED_BY_THE_COUNT,
    ),
    _failed(
        experiment="الفراكتاليّة على المحور المولود",
        section=SlgaeSection.GROSS_STRUCTURE,
        statement="فشلٌ جزئيّ: المدى الهندسيُّ لم يصمد على المحور المولود",
        subject="المدى الهندسيّ على المحور المولود بحسب تقرير SLGAE",
        figure_text="فشلٌ جزئيٌّ على المحور المولود وحده",
        genus=FailureGenus.FELL_STATISTICALLY,
    ),
    _failed(
        experiment="دعوى «الماضي يحفظ الحرف صامتًا»",
        section=SlgaeSection.GROSS_STRUCTURE,
        statement=(
            "تجميدٌ سابقٌ مسحوب: الإخلاءُ المقيسُ خالف المُجمَّد بمقدارٍ يزيد على "
            "خمسةَ عشرَ ضعفًا"
        ),
        subject="نسبةُ الإخلاء في دعوى الماضي بحسب تقرير SLGAE",
        figure_text="77.3% مقابل 5.2% المُجمَّدة",
        genus=FailureGenus.CONTRADICTED_BY_THE_COUNT,
    ),
    _failed(
        experiment="طريقةُ «الحذف الفردي»",
        section=SlgaeSection.GROSS_STRUCTURE,
        statement="انهارت الطريقةُ: أعطت الحقولَ المشتركةَ صفرًا فضاع تمييزُ ل/ر",
        subject="مخرَجُ الحذف الفردي على الحقول المشتركة بحسب تقرير SLGAE",
        figure_text="صفرٌ على الحقول المشتركة، فضاع تمييزُ ل/ر",
        genus=FailureGenus.METHOD_COLLAPSED,
    ),
    _failed(
        experiment="ماركوف P1 عند L4",
        section=SlgaeSection.MARKOV_FIVE_YA,
        statement="منعُ الكتلة يختفي اختفاءً تامًّا بين الكلمتين",
        subject="منعُ الكتلة بين الكلمتين عند L4 بحسب تقرير SLGAE",
        figure_text="اختفاءٌ تامٌّ لمنع الكتلة عند L4",
        genus=FailureGenus.FELL_STATISTICALLY,
    ),
    _failed(
        experiment="ماركوف P2",
        section=SlgaeSection.MARKOV_FIVE_YA,
        statement="سقوطٌ بفروقٍ كبيرةٍ في معيار المعلومات، لا بفرقٍ حدّيّ",
        subject="فروقُ BIC في P2 بحسب تقرير SLGAE",
        figure_text="ΔBIC ≈ +1500 و +4000",
        genus=FailureGenus.FELL_STATISTICALLY,
    ),
    _failed(
        experiment="ماركوف P2b على الرموز",
        section=SlgaeSection.MARKOV_FIVE_YA,
        statement=(
            "سقط على الرموز ونجح على الأنواع، واختيارُ الأنواع جاء بعد رؤية "
            "الرموز؛ وهذا أخطرُ من السقوط نفسِه"
        ),
        subject="فروقُ BIC في P2b على الرموز بحسب تقرير SLGAE",
        figure_text="ΔBIC = +149 و +187 على الرموز",
        genus=FailureGenus.FELL_STATISTICALLY,
    ),
    _failed(
        experiment="P1 في تجربة ٥ك",
        section=SlgaeSection.VOWEL_FIRST_FIVE_KAF,
        statement="القيمةُ المقيسةُ دون العتبة المُعلَنة",
        subject="إحصاءةُ F في P1 من تجربة ٥ك بحسب تقرير SLGAE",
        figure_text="F = 1.48 دون العتبة 1.88",
        genus=FailureGenus.FELL_STATISTICALLY,
    ),
    _failed(
        experiment="P3 في تجربة ٥ك",
        section=SlgaeSection.VOWEL_FIRST_FIVE_KAF,
        statement="التجميعُ أسوأ من العشوائيّ لا ضعيفٌ فحسب، إذ خرج المؤشّرُ سالبًا",
        subject="مؤشّرُ ARI في P3 من تجربة ٥ك بحسب تقرير SLGAE",
        figure_text="ARI = −0.08",
        genus=FailureGenus.FELL_STATISTICALLY,
    ),
    _failed(
        experiment="V2 في تجربة ٥ك",
        section=SlgaeSection.VOWEL_FIRST_FIVE_KAF,
        statement="فرقُ النقاء لم يبلغ حدَّ الدلالة",
        subject="نقاءُ V2 وأرجحيّتُه بحسب تقرير SLGAE",
        figure_text="نقاء 0.654 مقابل 0.569، p = 0.12",
        genus=FailureGenus.FELL_STATISTICALLY,
    ),
    _failed(
        experiment="V3 في تجربة ٥ك",
        section=SlgaeSection.VOWEL_FIRST_FIVE_KAF,
        statement=(
            "انقلب الاتّجاه: النونُ انضمّت إلى ل ر لا إلى الميم، عكسَ التصنيف "
            "الخيشوميّ؛ والشفويّاتُ لا تميل إلى الضمّ"
        ),
        subject="انضمامُ النون في V3 بحسب تقرير SLGAE",
        figure_text="النون مع ل ر لا مع الميم",
        genus=FailureGenus.DIRECTION_REVERSED,
    ),
    _failed(
        experiment="V1 في تجربة ٥ك",
        section=SlgaeSection.VOWEL_FIRST_FIVE_KAF,
        statement=(
            "ثباتٌ مُعلَنٌ انقلب كلّيًّا بعد استبعاد أوّل الجذع، فكان ثباتُه أثرَ "
            "مواقع الأوزان لا أثرَ القاعدة"
        ),
        subject="ثباتُ V1 قبل استبعاد أوّل الجذع وبعده بحسب تقرير SLGAE",
        figure_text="ثابت 25/26 ثمّ تغيّرٌ كلّيّ",
        genus=FailureGenus.FRAGILE_UNDER_SCOPE_CHANGE,
    ),
)

THE_WITHDRAWN_SUPPORTS: Final[tuple[WithdrawnSupportRecord, ...]] = (
    WithdrawnSupportRecord(
        subject="المقولاتُ النحويّة المُسمّاة «مؤكَّدة»",
        statement=(
            "وسومُ QAC وضعها مُعرِبون بالقواعد نفسِها التي تُختبَر، فالقياسُ "
            "عليها يقيس الوسمَ لا اللغة"
        ),
        standing=SupportStanding.RESULT_STANDS_SUPPORT_WITHDRAWN,
        defect=SupportDefect.CIRCULAR_ON_THE_TAGS,
    ),
    WithdrawnSupportRecord(
        subject="نسبةُ العدد المُعلَنة",
        statement="حكمٌ يدويٌّ لاحقٌ على الحالات، لا قياسٌ جرى بآلةٍ تُشغَّل",
        standing=SupportStanding.RESULT_STANDS_SUPPORT_WITHDRAWN,
        defect=SupportDefect.MANUAL_POST_HOC_JUDGMENT,
    ),
    WithdrawnSupportRecord(
        subject="CVV وحيادُ الألف وغيابُ CVV عن المجرّد",
        statement=(
            "CVV = CV + زمن، وحيادُ الألف جزئيًّا، وغيابُ CVV عن المجرّد: ثلاثتُها "
            "قريبةٌ من التعريف، فلا تُقرأ كشفًا عن المادّة"
        ),
        standing=SupportStanding.RESULT_STANDS_SUPPORT_WITHDRAWN,
        defect=SupportDefect.NEAR_DEFINITIONAL,
    ),
    WithdrawnSupportRecord(
        subject="«ما يولد وما يُدوَّر» وقائمةُ الستّةِ والعشرين ومتنبّئاتُ نوع الحركة",
        statement=(
            "اختيارُ الباحث نفسِه: تغيُّرُ العتبة يُغيّر الحكم، فالحكمُ نسبيٌّ إلى "
            "عتبةٍ لم تُشتَقّ من المادّة"
        ),
        standing=SupportStanding.RESULT_STANDS_SUPPORT_WITHDRAWN,
        defect=SupportDefect.ANALYST_CHOSEN_THRESHOLD,
    ),
    WithdrawnSupportRecord(
        subject="«العوامل» المُعلَنة",
        statement="أغلبُها تصنيفُ الصرف التراثيّ نفسُه بأسماءٍ جديدة، لا عاملًا مُكتشَفًا",
        standing=SupportStanding.RESULT_STANDS_SUPPORT_WITHDRAWN,
        defect=SupportDefect.TRADITIONAL_CLASSIFICATION_RENAMED,
    ),
)

THE_DISCREPANCIES: Final[tuple[SlgaeDiscrepancy, ...]] = (
    SlgaeDiscrepancy(
        name="LambdaIsNotRebuiltFromTheColumn",
        statement=(
            "λ المنشورة لا تُعاد بناؤها من عمود exp(β) في المستويات الثلاثة، "
            "حتى بعد حساب مجال التقريب؛ والفحصُ الحاسم موقوفٌ على إيداع الجدول "
            "بايتاتٍ في هذه الشجرة"
        ),
        figures=(
            QuotedFigure(
                subject="λ المنشورة ومجالُها المحسوب بحسب تقرير SLGAE",
                figure_text="0.43 مقابل المجال [0.462, 0.491]",
                rederivability=_QUOTED,
            ),
        ),
        checkable_if_bytes_were_deposited=True,
    ),
    SlgaeDiscrepancy(
        name="TheGammaBetaRatioCannotBeChecked",
        statement=(
            "مستويان يتعذّران لانعدام المشاهدة ولأنّ لوغاريتم الواحد صفر، "
            "والمحسوبان لا يتّفقان على ثابت؛ والفحصُ موقوفٌ على البايتات نفسِها"
        ),
        figures=(
            QuotedFigure(
                subject="نسبةُ γ/β المُعلَنة والمحسوبتان بحسب تقرير SLGAE",
                figure_text="1.55 مُعلَنةً، والمحسوبان 1.388 و 1.479",
                rederivability=_QUOTED,
            ),
        ),
        checkable_if_bytes_were_deposited=True,
    ),
    SlgaeDiscrepancy(
        name="OneIdentifierOnTwoExperiments",
        statement=(
            "قسمان يحملان المعرّفَ نفسَه، ولا اسمَ اختبارٍ واحدًا مشتركًا بينهما؛ "
            "فالمعرّفُ لا يُعيّن التجربة"
        ),
        figures=(
            QuotedFigure(
                subject="المعرّفُ الواحد على تجربتين بحسب تقرير SLGAE",
                figure_text=(
                    "قسمان بالرقم ٥ك و VOWEL-FIRST-BIRTH-AR-1،" " وصفرُ أسماءٍ مشتركة"
                ),
                rederivability=_QUOTED,
            ),
        ),
        checkable_if_bytes_were_deposited=False,
    ),
    SlgaeDiscrepancy(
        name="TheThroatBridgeCarriesTwoMagnitudes",
        statement=(
            "جسرُ الحلق يُنشَر بمقدارين متباعدين في موضعين، والفرقُ بينهما مرتبةٌ "
            "كاملةٌ في الأرجحيّة"
        ),
        figures=(
            QuotedFigure(
                subject="نسبتا جسر الحلق بحسب تقرير SLGAE",
                figure_text="1.148 مقابل 4.765، أي ×4.15",
                rederivability=_QUOTED,
            ),
            QuotedFigure(
                subject="أرجحيّتا جسر الحلق بحسب تقرير SLGAE",
                figure_text="1.39 مقابل 20.81، أي ×15",
                rederivability=_QUOTED,
            ),
        ),
        checkable_if_bytes_were_deposited=False,
    ),
)

THE_OWN_BUILD: Final[tuple[OwnBuildRecord, ...]] = (
    OwnBuildRecord(
        subject="عرضُ الترميز لكلّ وحدةٍ مشكولة",
        statement=(
            "رقمٌ وصل عن بناءٍ في شجرةٍ أخرى؛ ولا دالّةَ في هذه الشجرة تُعيد "
            "اشتقاقَه، فيبقى خبرًا بقيده"
        ),
        standing=BuildStanding.MEASURED_AND_STANDING,
        figure=QuotedFigure(
            subject="عرضُ الترميز المنقول لكلّ وحدةٍ مشكولة",
            figure_text="ثماني بتّاتٍ لكلّ وحدةٍ مشكولة",
            rederivability=_QUOTED,
        ),
    ),
    OwnBuildRecord(
        subject="مسحُ التقابل التامّ المذكور",
        statement=(
            "مُسنَدٌ ومردودٌ في مسحٍ مذكور؛ ولا بايتاتِ ذلك المسح في هذه الشجرة "
            "فتُعاد قراءتُها"
        ),
        standing=BuildStanding.MEASURED_AND_STANDING,
        figure=QuotedFigure(
            subject="مسحُ التقابل التامّ المنقول في بناءٍ آخر",
            figure_text="224 مُسنَدًا و 32 مردودًا",
            rederivability=_QUOTED,
        ),
    ),
    OwnBuildRecord(
        subject="محورُ المخرج: حسمُ الحرف",
        statement="فشلٌ مُسمًّى: محورُ المخرج لا يحسم الحرف، وتبقى الحالاتُ معلَّقة",
        standing=BuildStanding.DEFERRED_UNDECIDED,
        figure=QuotedFigure(
            subject="ما تركه محورُ المخرج معلَّقًا بحسب التقرير",
            figure_text="20 حالةً معلَّقة",
            rederivability=_QUOTED,
        ),
    ),
    OwnBuildRecord(
        subject="محورُ الحركة: حسمُ الحرف",
        statement=(
            "مانعٌ بصفرٍ مقيس: قِيس المحورُ فخرج صفرًا، ولا يُلطَّف الصفرُ بعبارةِ " "عملٍ جارٍ"
        ),
        standing=BuildStanding.BLOCKED_BY_A_MEASURED_ZERO,
        figure=QuotedFigure(
            subject="ما حسمه محورُ الحركة من الحالات المعلَّقة",
            figure_text="صفرٌ من 20",
            rederivability=_QUOTED,
        ),
    ),
    OwnBuildRecord(
        subject="الصفاتُ المولودة: ما حسمته وما تركته",
        statement=(
            "حسمٌ جزئيّ: ثمانٍ محسومة، وتسعٌ متعادلة، وثلاثٌ موقوفة؛ والمتعادلُ "
            "والموقوفُ يُودَعان بالاسم"
        ),
        standing=BuildStanding.DEFERRED_UNDECIDED,
        figure=QuotedFigure(
            subject="قسمةُ الصفات المولودة على الحالات المعلَّقة",
            figure_text="8 محسومة و 9 متعادلة و 3 موقوفة",
            rederivability=_QUOTED,
        ),
    ),
    OwnBuildRecord(
        subject="عددُ الملفّات وعددُ الاختبارات المنقولان",
        statement=(
            "لقطةٌ من وقتٍ آخر: تُقابَل بما يقيسه القرصُ الآن في "
            "`the_quoted_build_counts_against_disk`، ولا تُجمَّد"
        ),
        standing=BuildStanding.MEASURED_AND_STANDING,
        figure=QuotedFigure(
            subject="عددُ الملفّات وعددُ الاختبارات المنقولان عن بناءٍ آخر",
            figure_text="62 اختبارًا و 424 ملفًّا",
            rederivability=_QUOTED,
        ),
    ),
)


@dataclass(frozen=True, slots=True)
class SlgaeAuditDeposit:
    """الإيداعُ كلُّه؛ تغطيةٌ قبل حكم، وكلُّ موضعٍ مُسمًّى له سجلٌّ فيه."""

    held: tuple[SlgaeFinding, ...]
    failures: tuple[SlgaeFinding, ...]
    withdrawn_supports: tuple[WithdrawnSupportRecord, ...]
    discrepancies: tuple[SlgaeDiscrepancy, ...]
    own_build: tuple[OwnBuildRecord, ...]

    def __post_init__(self) -> None:
        if not self.held or not self.failures:
            raise SlgaeDepositError("إيداعٌ بلا صامدٍ أو بلا ساقطٍ يُخفي أحدَ وجهَي التقرير.")
        for finding in self.held:
            if not finding.held:
                raise SlgaeDepositError("سجلٌّ ساقطٌ في باب الصامد.")
        for finding in self.failures:
            if finding.held:
                raise SlgaeDepositError("سجلٌّ صامدٌ في باب الساقط.")
        experiments: set[str] = set()
        for finding in (*self.held, *self.failures):
            key = comparison_key(finding.experiment)
            if key in experiments:
                raise SlgaeDepositError(
                    f"تجربةٌ مكرّرةٌ في الإيداع: {finding.experiment}؛ "
                    "والتكرارُ يُخفي منزلةً تحت أخرى."
                )
            experiments.add(key)
        names: set[str] = set()
        for discrepancy in self.discrepancies:
            if discrepancy.name in names:
                raise SlgaeDepositError(f"تناقضٌ مكرّرٌ في الإيداع: {discrepancy.name}.")
            names.add(discrepancy.name)
        covered = {finding.section for finding in (*self.held, *self.failures)}
        missing = tuple(
            section
            for section in SlgaeSection
            if section is not SlgaeSection.OUR_OWN_BUILD and section not in covered
        )
        if missing:
            raise SlgaeDepositError(
                "موضعٌ مُسمًّى بلا سجلٍّ في الإيداع: "
                + "، ".join(section.value for section in missing)
            )
        if not self.own_build:
            raise SlgaeDepositError(
                "إيداعٌ بلا سجلٍّ عن بنائنا نحن يُسكِت أقربَ ما يُسأل عنه."
            )

    @property
    def failure_count(self) -> int:
        """عددُ السقوطات المُسمّاة، مُشتَقًّا من السجلّات لا مكتوبًا في نثر."""

        return len(self.failures)

    @property
    def failures_by_genus(self) -> dict[FailureGenus, tuple[SlgaeFinding, ...]]:
        """قسمةُ السقوطات بنوعها، وكلُّ نوعٍ له مدخلٌ ولو خلا."""

        return {
            genus: tuple(
                finding for finding in self.failures if finding.failure_genus is genus
            )
            for genus in FailureGenus
        }

    @property
    def quoted_figures(self) -> tuple[QuotedFigure, ...]:
        """كلُّ رقمٍ منقولٍ في الإيداع، بترتيب أبوابه."""

        figures: list[QuotedFigure] = [
            finding.figure for finding in (*self.held, *self.failures)
        ]
        for discrepancy in self.discrepancies:
            figures.extend(discrepancy.figures)
        figures.extend(record.figure for record in self.own_build)
        return tuple(figures)

    @property
    def any_figure_is_measured_here(self) -> bool:
        """`False` دائمًا: ليس في الإيداع رقمٌ قِيس في هذه الشجرة."""

        return any(figure.is_measured_in_this_tree for figure in self.quoted_figures)

    @property
    def deposit_is_operative(self) -> bool:
        """`False` دائمًا: لا بوّابةَ في هذا المستودع تقرأ هذا الإيداع."""

        return False


SLGAE_AUDIT_DEPOSIT: Final[SlgaeAuditDeposit] = SlgaeAuditDeposit(
    held=THE_HELD,
    failures=THE_FAILURES,
    withdrawn_supports=THE_WITHDRAWN_SUPPORTS,
    discrepancies=THE_DISCREPANCIES,
    own_build=THE_OWN_BUILD,
)

for _dataclass in (
    QuotedFigure,
    SlgaeFinding,
    WithdrawnSupportRecord,
    SlgaeDiscrepancy,
    OwnBuildRecord,
    QuotedAgainstMeasured,
    SlgaeAuditDeposit,
):  # pragma: no cover - guard
    for _field in fields(_dataclass):
        if any(token in _field.name for token in _FORBIDDEN_FIELD_TOKENS):
            raise RuntimeError(
                "a deposit type carries a verdict, birth, freeze, or proof field"
            )

if SLGAE_AUDIT_DEPOSIT.deposit_is_operative:  # pragma: no cover - guard
    raise RuntimeError("the deposit declares itself operative")
if SLGAE_AUDIT_DEPOSIT.any_figure_is_measured_here:  # pragma: no cover - guard
    raise RuntimeError("a quoted figure declares itself measured in this tree")
