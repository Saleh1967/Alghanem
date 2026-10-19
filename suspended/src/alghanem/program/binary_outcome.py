"""قاعدةُ النتيجتين فقط: لا فئةَ ثالثة تُقرأ «نجاحًا جزئيًّا» فيُبنى عليها.

كلُّ محاولةِ إغلاقِ فجوةٍ تنتهي بواحدةٍ من اثنتين لا ثالثَ بينهما: يقينٌ تامّ،
أو كشفُ طبقةٍ أعمق لم تكن ظاهرة. والفرقُ بينهما فرقُ جنسٍ لا فرقُ درجة::

    TotalCertainty     != StrongerThan(DeeperLayer)
    DeeperLayer        != FailedAttempt
    MiddleFigure       != Outcome

**والثالثةُ ممنوعةٌ بالمفردة لا بالنصيحة.** ليس في `GapClosureOutcome` عضوٌ
ثالث، فالنتيجةُ المختلطةُ المريحة غيرُ قابلةٍ للتعبير هنا أصلًا، لا مذمومةٌ
يُنصَح بتركها؛ وهذا شكلُ `RungStanding` نفسُه في `certainty_ladder`: ما لا يجوز
إسنادُه لا يُترك في المفردة ليُسنَد ثم يُعتذَر عنه.

**واليقينُ التامّ محسوبٌ من الآلة القائمة لا مُعلَنٌ هنا.** `TotalCertaintyRecord`
لا يقوم إلا مربوطًا بـ`ProtocolRun` من `alghanem.program.direct_certainty` حكمُ
`assess_freeze` عليه `FROZEN_ADMISSIBLE`؛ فالقبولُ مأخوذٌ من خطوات §١–§٥ لا
مُستأنَفٌ في هذه الوحدة. واتّجاهُ الاعتماد واحدٌ لا يُعكَس: هذه الوحدة تقرأ
`direct_certainty`، ولا تقرؤها هي ولا تُملي على `assess_freeze` شيئًا
(`TOTAL_CERTAINTY_IS_RELATIVE_TO_ITS_BOUND_RUN`).

**وكشفُ الطبقة الأعمق خطوةٌ تشخيصيةٌ ناجحة، لا اعتذارٌ عن فشل.**
`DeeperLayerRecord` يُلزِم بتسميةِ ما ضاق به المجهول: تلوّثٌ لم يكن معروفًا،
أو تصميمٌ تبيَّن أنه يحتاج إعادةَ بناءٍ لا تمديدًا، أو فئةٌ رابعةٌ مُتشابكةٌ لم
تكن مرصودة. ورقمٌ وسطٌ لا يحمل يقينًا لا يُترك معلَّقًا: يُصنَّف في
`MidFigureClassification` قياسًا صحيحًا على سؤالٍ خاطئ، أو قياسًا ناقصًا على
سؤالٍ صحيح؛ وكلاهما من الفئة الثانية، محدَّدُ الاسم.

**وعباراتُ التعليق مرفوضةٌ بشكلها المُعلَن لا بمعناها المُدرَك.**
`REFUSED_CLOSING_PHRASES` مفردةٌ مكتوبة تُفحَص عليها علّةُ النتيجة، وهي فحصُ
شكلٍ على قائمةٍ مُعلَنة لا برهانٌ أن كلَّ تعليقٍ مُراوِغٍ مسدود
(`REFUSED_PHRASES_ARE_DECLARED_NOT_DERIVED`) — وهو الصدقُ نفسُه الذي يُعلنه
كاشفُ التلوّث عن مداه المُعلَن.

**وأرقامُ نصّ القاعدة تخضع للقاعدة قبلها.** تسلسلُ الانزلاق المذكور فيها
(٦٩٫٢٪ ← ٩٦٫٥٥٪ ← ٩٩٫٨٣٪ ← «١٠٠٪»)، ورقمُ CV+CV الوسط، وأمثلةُ الجلسة
المذكورة — وصلت سردًا من محادثةٍ أخرى، ولا كودَ هنا يُعيد اشتقاقَها. فسُجِّلت في
`REPORTED_UNVERIFIED_FIGURES` في `direct_certainty` نفسِه لا في سجلٍّ ثانٍ:
سجلّان للخبر الواحد يقسمانه فيُقرأ كلٌّ منهما تامًّا وهو ناقص.

**ولا سلطةَ لهذه الوحدة**: لا تقرؤها بوّابةٌ في `kernel/`، ولا تُجمِّد ولا
تُولِد (`NO_KERNEL_MODULE_CONSUMES_THE_BINARY_OUTCOME_RULE`).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Final

from .direct_certainty import FreezeStatus, ProtocolRun, assess_freeze

__all__ = [
    "BINARY_OUTCOME_NAMED_RESIDUALS",
    "NO_KERNEL_MODULE_CONSUMES_THE_BINARY_OUTCOME_RULE",
    "REFUSED_CLOSING_PHRASES",
    "REFUSED_PHRASES_ARE_DECLARED_NOT_DERIVED",
    "TOTAL_CERTAINTY_IS_RELATIVE_TO_ITS_BOUND_RUN",
    "TWO_OUTCOMES_ARE_A_PARTITION_NOT_A_SCALE",
    "AttemptRecord",
    "BinaryOutcomeError",
    "ClassifiedAttempt",
    "DeeperLayerRecord",
    "GapClosureOutcome",
    "MidFigureClassification",
    "TotalCertaintyRecord",
    "classify_attempt",
]


class BinaryOutcomeError(ValueError):
    """رُوجِعت القاعدةُ بما لا تقوم به: نتيجةٌ بلا فئة، أو يقينٌ بلا تشغيله."""


# --- النتيجتان، ولا ثالثةَ في المفردة ----------------------------------------


class GapClosureOutcome(Enum):
    """فئتا نتيجةِ المحاولة؛ **ولا عضوَ ثالثَ هنا**، وذلك عينُ الحراسة.

    وليستا درجتين في سُلَّمِ قوّة: كشفُ الطبقة الأعمق لا يقع «تحت» اليقين
    التامّ ولا فوقه؛ هو جوابٌ عن سؤالٍ آخر، وضمُّهما في سُلَّمٍ واحد يُعيد
    الفئةَ الثالثة من باب التعداد بعد منعها من باب التسمية.
    """

    TOTAL_CERTAINTY = "total_certainty"
    DEEPER_LAYER_REVEALED = "deeper_layer_revealed"


class MidFigureClassification(Enum):
    """تصنيفُ الرقم الوسط الذي لا يحمل يقينًا؛ وكلاهما من الفئة الثانية.

    وليس بينهما ترتيبٌ ولا تفضيل: أحدهما يقول إنّ السؤال نفسَه يحتاج إعادةَ
    بناء، والآخر يقول إنّ السؤال صحيحٌ والبياناتِ ناقصة؛ وهما علّتان مختلفتان
    لا مقداران من علّةٍ واحدة.
    """

    CORRECT_MEASUREMENT_ON_A_WRONG_QUESTION = "correct_measurement_on_a_wrong_question"
    INCOMPLETE_MEASUREMENT_ON_A_RIGHT_QUESTION = (
        "incomplete_measurement_on_a_right_question"
    )

    @property
    def outcome(self) -> GapClosureOutcome:
        """الفئةُ التي ينتمي إليها هذا التصنيف؛ وكلاهما كشفُ طبقةٍ أعمق."""
        return GapClosureOutcome.DEEPER_LAYER_REVEALED


# --- عباراتُ التعليق المرفوضة، مُعلَنةً لا مُستنبَطة ---------------------------


REFUSED_CLOSING_PHRASES: Final[tuple[str, ...]] = (
    "النتيجة جزئية",
    "نجاح جزئي",
    "إشارة أولية تحتاج مزيدا من العمل",
    "إشارة أولية",
    "تحتاج مزيدا من العمل",
    "قريب من الهدف",
    "قريبون من الهدف",
)
"""صيغُ الإنهاء المُراوِغة المُسمّاة في نصّ القاعدة، مكتوبةً بلا تشكيل لتُطابَق."""


_ARABIC_MARKS: Final = re.compile("[\u064b-\u0652\u0670\u0640]")


def _comparable(text: str) -> str:
    """جرِّد النصَّ من التشكيل والتطويل واجمع فراغَه، ليُقابَل بالمفردة المُعلَنة.

    ولا يُبدَّل حرفٌ بحرف: التجريدُ هنا للعلامات التي تُكتَب وتُترَك في النصّ
    الواحد، لا توحيدٌ لرسمٍ يُغيِّر الكلمة.
    """
    return " ".join(_ARABIC_MARKS.sub("", text).split())


def _refused_phrase_in(text: str) -> str | None:
    """أوّلُ عبارةٍ مرفوضةٍ وردت في النصّ، أو `None` إن لم ترد واحدةٌ منها."""
    haystack = _comparable(text)
    for phrase in REFUSED_CLOSING_PHRASES:
        if _comparable(phrase) in haystack:
            return phrase
    return None


def _require_named(value: str, message: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise BinaryOutcomeError(message)


def _refuse_evasive(value: str, field_name: str) -> None:
    phrase = _refused_phrase_in(value)
    if phrase is not None:
        raise BinaryOutcomeError(
            f"{field_name} تنتهي بعبارةٍ مُعلَّقة: {phrase!r}؛ والنتيجةُ تُصنَّف "
            "باسم إحدى الفئتين ولا تُترك بين بين."
        )


# --- الفئة الأولى: يقينٌ تامّ، محسوبٌ من تشغيلٍ قائم ---------------------------


@dataclass(frozen=True)
class TotalCertaintyRecord:
    """رقمٌ صريحٌ مربوطٌ بمسارٍ أُعيد تشغيلُه الآن، بلا استثناءٍ يحتاج تبريرًا.

    والقبولُ هنا **محسوبٌ لا مُصرَّحٌ به**: `assess_freeze` هو الذي يحكم على
    المسار المربوط، وهذا الصنفُ يقرأ حكمَه ولا يستأنفه ولا يُنشئ حكمًا موازيًا.
    """

    subject: str
    figure_text: str
    run: ProtocolRun
    reason: str
    declared_exceptions: tuple[str, ...] = field(default=())

    def __post_init__(self) -> None:
        _require_named(self.subject, "يقينٌ بلا موضوعٍ مُسمًّى لا يُراجَع.")
        _require_named(
            self.figure_text,
            "الفئةُ الأولى رقمٌ صريح؛ ويقينٌ بلا رقمٍ مكتوبٍ دعوى لا نتيجة.",
        )
        _require_named(self.reason, "نتيجةٌ بلا علّةٍ مكتوبةٍ لا تُقرأ ولا تُردّ.")
        _refuse_evasive(self.reason, "علّةُ اليقين التامّ")
        if not isinstance(self.run, ProtocolRun):
            raise BinaryOutcomeError(
                "اليقينُ التامّ مربوطٌ بـ`ProtocolRun`؛ وبلا مسارٍ مربوطٍ لا "
                "يُحسَب قبولُه من شيء."
            )
        if not isinstance(self.declared_exceptions, tuple) or any(
            not isinstance(item, str) for item in self.declared_exceptions
        ):
            raise BinaryOutcomeError("الاستثناءاتُ المُعلَنة نصوصٌ في مجموعة.")
        if self.declared_exceptions:
            raise BinaryOutcomeError(
                "يقينٌ تامٌّ مع استثناءٍ يحتاج تبريرًا إضافيًّا ليس من الفئة "
                f"الأولى: {list(self.declared_exceptions)}؛ وموضعُه الفئةُ "
                "الثانية باسمها."
            )
        assessment = assess_freeze(self.run)
        if assessment.status is not FreezeStatus.FROZEN_ADMISSIBLE:
            raise BinaryOutcomeError(
                "لا يقينَ تامٌّ على مسارٍ لم يُقبَل تجميدُه: "
                f"{assessment.status.value} — {assessment.reason}"
            )

    @property
    def outcome(self) -> GapClosureOutcome:
        """فئةُ هذا السجلّ، وهي الأولى بالإنشاء لا بالوصف."""
        return GapClosureOutcome.TOTAL_CERTAINTY


# --- الفئة الثانية: كشفُ طبقةٍ أعمق، خطوةٌ تشخيصيةٌ ناجحة ----------------------


@dataclass(frozen=True)
class DeeperLayerRecord:
    """محاولةٌ لم تُغلِق الفجوة لكنّها ضيَّقت المجهولَ بمعلومةٍ قابلةٍ للقياس.

    وهذا سجلُّ **نجاحٍ تشخيصيّ** يُقرأ بدرجة وضوح الفئة الأولى نفسِها، لا
    اعتذارٌ عن فشل: تسميةُ تلوّثٍ لم يكن معروفًا، أو كشفُ أنّ التصميم نفسَه
    يحتاج إعادةَ بناءٍ لا تمديدًا، أو تمييزُ فئةٍ رابعةٍ مُتشابكةٍ لم تكن مرصودة
    — كلُّها معلوماتٌ لم تكن في اليد قبل المحاولة.

    ورقمٌ وسطٌ لا يحمل يقينًا لا يُترك معلَّقًا: متى ذُكر وجب تصنيفُه في
    `MidFigureClassification`، فلا يبقى رقمًا بلا فئةٍ يُبنى عليه لاحقًا كأنه
    يقين.
    """

    subject: str
    narrowed_unknown: str
    reason: str
    opening_mid_figure: str = ""
    mid_figure_classification: MidFigureClassification | None = None

    def __post_init__(self) -> None:
        _require_named(self.subject, "كشفٌ بلا موضوعٍ مُسمًّى لا يُراجَع.")
        _require_named(
            self.narrowed_unknown,
            "الفئةُ الثانية تُلزِم بتسميةِ ما ضاق به المجهول؛ وكشفٌ بلا "
            "معلومةٍ مُسمّاةٍ قابلةٍ للقياس ليس كشفًا.",
        )
        _require_named(self.reason, "نتيجةٌ بلا علّةٍ مكتوبةٍ لا تُقرأ ولا تُردّ.")
        _refuse_evasive(self.narrowed_unknown, "المعلومةُ التي ضاق بها المجهول")
        _refuse_evasive(self.reason, "علّةُ كشفِ الطبقة الأعمق")
        if not isinstance(self.opening_mid_figure, str):
            raise BinaryOutcomeError("الرقمُ الوسط نصٌّ مكتوب.")
        has_figure = bool(self.opening_mid_figure.strip())
        if self.mid_figure_classification is not None and not isinstance(
            self.mid_figure_classification, MidFigureClassification
        ):
            raise BinaryOutcomeError("تصنيفُ الرقم الوسط عضوٌ في مفردته المغلقة.")
        if has_figure and self.mid_figure_classification is None:
            raise BinaryOutcomeError(
                f"رقمٌ وسطٌ بلا تصنيف: {self.opening_mid_figure!r}؛ إمّا قياسٌ "
                "صحيحٌ على سؤالٍ خاطئ وإمّا قياسٌ ناقصٌ على سؤالٍ صحيح، ولا "
                "يبقى معلَّقًا."
            )
        if not has_figure and self.mid_figure_classification is not None:
            raise BinaryOutcomeError(
                "تصنيفُ رقمٍ وسطٍ بلا رقمٍ مكتوبٍ يُصنِّف ما لا يُقرأ؛ فيُكتَب "
                "الرقمُ أو يُرفَع تصنيفُه."
            )

    @property
    def outcome(self) -> GapClosureOutcome:
        """فئةُ هذا السجلّ، وهي الثانية بالإنشاء لا بالوصف."""
        return GapClosureOutcome.DEEPER_LAYER_REVEALED


AttemptRecord = TotalCertaintyRecord | DeeperLayerRecord
"""ما يصلح أن يكون محاولةً مُصنَّفة؛ وما خرج عنهما لا فئةَ له فيُرفَض."""


@dataclass(frozen=True)
class ClassifiedAttempt:
    """محاولةٌ مُصنَّفةٌ بفئتها وعلّتها؛ ولا حقلَ «غيرُ مُصنَّفة» يُقرأ سكوتًا."""

    outcome: GapClosureOutcome
    reason: str

    def __post_init__(self) -> None:
        if not isinstance(self.outcome, GapClosureOutcome):
            raise BinaryOutcomeError("الفئةُ عضوٌ في `GapClosureOutcome`.")
        _require_named(self.reason, "تصنيفٌ بلا علّةٍ مكتوبةٍ لا يُقرأ ولا يُردّ.")


def classify_attempt(record: AttemptRecord) -> ClassifiedAttempt:
    """صنِّف المحاولةَ في إحدى الفئتين، أو ارفُضها؛ ولا مخرجَ ثالثَ من هنا.

    وليس في هذه الدالة مسارُ عودةٍ يحمل «غيرَ مُصنَّفة»: ما لم يقم سجلًّا من
    أحد الصنفين لم يجتز شروطَ فئته، فبقاؤه بلا تصنيفٍ رفضٌ مُسمًّى لا سكوت.
    """
    if isinstance(record, TotalCertaintyRecord | DeeperLayerRecord):
        return ClassifiedAttempt(outcome=record.outcome, reason=record.reason)
    raise BinaryOutcomeError(
        "محاولةٌ ليست من الفئتين لا تُصنَّف: الفئةُ الأولى `TotalCertaintyRecord` "
        "والثانية `DeeperLayerRecord`، ولا ثالثةَ تُقبَل هنا."
    )


# --- ما تتركه هذه القاعدة مفتوحًا، مُسمًّى ------------------------------------


TWO_OUTCOMES_ARE_A_PARTITION_NOT_A_SCALE: Final[str] = (
    "TWO_OUTCOMES_ARE_A_PARTITION_NOT_A_SCALE: الفئتان قسمةٌ لمحاولاتِ إغلاق "
    "الفجوة لا درجتانِ في سُلَّمِ قوّة؛ فلا يُقرَأ كشفُ الطبقة الأعمق نتيجةً "
    "أدنى من اليقين التامّ، ولا تُجمَعان في ترتيبٍ واحد فتعود الفئةُ الثالثة "
    "تعدادًا بعد منعها تسميةً"
)

TOTAL_CERTAINTY_IS_RELATIVE_TO_ITS_BOUND_RUN: Final[str] = (
    "TOTAL_CERTAINTY_IS_RELATIVE_TO_ITS_BOUND_RUN: قبولُ الفئة الأولى محسوبٌ "
    "من `assess_freeze` على المسار المربوط وحده؛ فهو يقينٌ نسبةً إلى ذلك "
    "المسار وخطواته الستّ، لا يقينٌ مطلقٌ تُصدره هذه الوحدة، ولا تُراجَع فيه "
    "صحّةُ ما أنتجه الكودُ المُعاد"
)

REFUSED_PHRASES_ARE_DECLARED_NOT_DERIVED: Final[str] = (
    "REFUSED_PHRASES_ARE_DECLARED_NOT_DERIVED: `REFUSED_CLOSING_PHRASES` "
    "قائمةٌ مكتوبةٌ في هذه الوحدة، وفحصُها فحصُ شكلٍ على نصٍّ مُجرَّدٍ من "
    "التشكيل؛ فاجتيازُها لا يُثبت خلوَّ العلّة من تعليقٍ مُراوِغٍ بصياغةٍ أخرى، "
    "والحارسُ الأخيرُ التصنيفُ باسمه لا مطابقةُ العبارات"
)

NO_KERNEL_MODULE_CONSUMES_THE_BINARY_OUTCOME_RULE: Final[str] = (
    "NO_KERNEL_MODULE_CONSUMES_THE_BINARY_OUTCOME_RULE: لا تقرأ هذه القاعدةَ "
    "أيُّ بوّابةٍ في `kernel/`، ولا تُجمِّد ولا تُولِد ولا تُرخِّص انتقالًا؛ "
    "فحكمُها على من استعملها لا على الشجرة كلّها"
)

BINARY_OUTCOME_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "TWO_OUTCOMES_ARE_A_PARTITION_NOT_A_SCALE": (
        TWO_OUTCOMES_ARE_A_PARTITION_NOT_A_SCALE
    ),
    "TOTAL_CERTAINTY_IS_RELATIVE_TO_ITS_BOUND_RUN": (
        TOTAL_CERTAINTY_IS_RELATIVE_TO_ITS_BOUND_RUN
    ),
    "REFUSED_PHRASES_ARE_DECLARED_NOT_DERIVED": (
        REFUSED_PHRASES_ARE_DECLARED_NOT_DERIVED
    ),
    "NO_KERNEL_MODULE_CONSUMES_THE_BINARY_OUTCOME_RULE": (
        NO_KERNEL_MODULE_CONSUMES_THE_BINARY_OUTCOME_RULE
    ),
}
"""ما لا تحسمه هذه القاعدة، مُسمًّى هنا لا متروكًا ليُفترَض."""
