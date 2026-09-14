"""بروتوكولُ اليقين المباشر: لا تُقبَل نتيجةٌ إلّا وكودُها يُشغَّل الآن.

هذه الوحدةُ تُرمِّز القاعدةَ الحاكمة: **مصدرُ القضية لا يُعفيها من إعادة
التشغيل**. سردٌ نثريٌّ من محادثةٍ أخرى، ونتيجةٌ لي في رسالةٍ سابقة، وبديهةٌ
رياضيةٌ «واضحة» — ثلاثتُها جنسٌ واحدٌ في هذا الباب: لا يقينَ فيها حتى تُعاد::

    QuotedFigure    != MeasuredFigure
    EarlierMessage  != RerunNow
    ObviousAxiom    != CountedResult

والاختبارُ العمليُّ وحده هو الفيصل: أتملك الآن، في عمليةٍ جديدة، الكودَ الذي
يُنتج الرقم؟ فإن كان الجوابُ «لا، لكنّه مذكورٌ في رسالةٍ سابقة» فالقضيةُ غيرُ
يقينية. ولهذا لا يُقبَل هنا تصريحٌ بالإتمام بلا `reproducer` يُستورَد ويُستدعى
فعلًا؛ و`run_step` هو ذلك الاستدعاء لا وصفُه.

**ترتيبُ الخطوات مُلزِم ولا تُتخطّى خطوة.** و`DirectCertaintyStep.DATA_PURITY_CHECK`
هي الخطوةُ صفر: لا يبدأ عدٌّ خامٌّ على نصٍّ لم يجتز كاشفَ التلوّث أوّلًا،
وتنفيذُ تلك الخطوة قائمٌ في `alghanem.arabic.encoding.contamination_gate`.
وكانت الخطواتُ خمسًا قبل إضافةِ هذه، فصارت ستًّا؛ وذلك أصلُ ذكرِ العددَين في
نصّ البروتوكول (`STEP_ZERO_WAS_ADDED_AFTER_THE_FIVE_NOTE`).

**وأرقامُ الحادثة نفسِها تخضع للقاعدة نفسِها.** الأرقامُ التي وردت في نصّ
البروتوكول (توكناتُ التلوّث، وموضعُ السطر، وأرقامُ النسب) وصلت هذه الشجرةَ
سردًا من محادثةٍ أخرى، ولا نصَّ مودَعًا هنا يُعيد اشتقاقَها. فلم تُقبَل قياسًا،
ولم تُحذَف أيضًا: سُجِّلت في `REPORTED_UNVERIFIED_FIGURES` بجنس مصدرها وبقيدها،
لأن حذفَ الخبر إخفاءٌ كما أن قبولَه تصديقٌ، وكلاهما مرفوض
(`RECORDING_IS_NOT_ENDORSING`). وهذا تطبيقُ البروتوكول على نصّه، لا استثناءٌ له.

**وقاعدةُ النتيجتين تقرأ هذه الوحدةَ ولا تُقرَأ منها.** ما بعد التجميد —
تصنيفُ كلّ محاولةِ إغلاقِ فجوةٍ في فئتين لا ثالثَ لهما — قائمٌ في
`alghanem.program.binary_outcome`، وهو يستدعي `assess_freeze` ليحسب قبولَ فئته
الأولى؛ ولا تستورد هذه الوحدةُ تلك، فاتّجاهُ الاعتماد واحدٌ لا يُعكَس.

**ولا سلطةَ لهذه الوحدة على النواة.** لا يقرؤها `BirthVerdictGate` ولا
`InvariantVerificationGate` ولا أيُّ وحدةٍ في `kernel/`؛ فهي سجلٌّ وحارسٌ لمن
استعملها، لا بابٌ يعبره غيرُه (`NO_KERNEL_MODULE_CONSUMES_THIS_PROTOCOL`).
"""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from enum import Enum
from typing import Any, Final

__all__ = [
    "COMPLETION_IS_A_RUN_NOT_A_DECLARATION",
    "DIRECT_CERTAINTY_NAMED_RESIDUALS",
    "NO_KERNEL_MODULE_CONSUMES_THIS_PROTOCOL",
    "RECORDING_IS_NOT_ENDORSING",
    "REPORTED_UNVERIFIED_FIGURES",
    "STEP_ZERO_WAS_ADDED_AFTER_THE_FIVE_NOTE",
    "UNREAD_STEP_ORDER_IS_NOT_A_RANKING",
    "CertaintySourceGenus",
    "DirectCertaintyError",
    "DirectCertaintyStep",
    "FigureConstraint",
    "FreezeAssessment",
    "FreezeStatus",
    "ProtocolRun",
    "StepRecord",
    "UnverifiedFigureRecord",
    "assess_freeze",
    "run_step",
]


class DirectCertaintyError(ValueError):
    """رُوجِع البروتوكولُ بما لا يقوم به: خطوةٌ متخطَّاة، أو تصريحٌ بلا كود."""


# --- جنسُ المصدر: لا استثناءَ لمصدرٍ بعينه ----------------------------------


class CertaintySourceGenus(Enum):
    """من أين وصلت القضية؛ والجنسُ وحدَه يقرّر أتصلح لتجميدٍ أم لا."""

    PROSE_FROM_ANOTHER_CONVERSATION = "prose_from_another_conversation"
    EARLIER_MESSAGE_IN_THIS_CONVERSATION = "earlier_message_in_this_conversation"
    DECLARED_MATHEMATICAL_INTUITION = "declared_mathematical_intuition"
    RERUN_NOW_IN_THIS_PROCESS = "rerun_now_in_this_process"

    @property
    def supports_freeze(self) -> bool:
        """أيصلح هذا الجنسُ وحدَه أساسًا لتجميدٍ نهائيّ؟"""
        return self is CertaintySourceGenus.RERUN_NOW_IN_THIS_PROCESS

    @property
    def requires_rerun_before_decisive_use(self) -> bool:
        """أيلزم إعادةُ تشغيلها قبل بناءِ استنتاجٍ حاسمٍ جديدٍ عليها؟

        نتيجتي أنا من رسالةٍ سابقة ليست استثناءً: تفصيلُ السردِ وإقناعُه ليسا
        من جنس الدليل، وقِدَمُ الرسالةِ في المحادثة نفسِها لا يُغني عن الكود.
        """
        return not self.supports_freeze


# --- الخطواتُ الستّ، مرتّبةً ولا تُتخطّى --------------------------------------


class DirectCertaintyStep(Enum):
    """خطواتُ بناء المعادلة بالترتيب الإلزاميّ، صفرُها كاشفُ التلوّث."""

    DATA_PURITY_CHECK = "data_purity_check"
    RAW_COUNT = "raw_count"
    RAW_SAMPLE_INSPECTION = "raw_sample_inspection"
    ONE_CONDITION_AT_A_TIME = "one_condition_at_a_time"
    ITERATE_UNTIL_FULL_CLASSIFICATION = "iterate_until_full_classification"
    FREEZE_ASSESSMENT = "freeze_assessment"

    @property
    def position(self) -> int:
        """موضعُ الخطوة في الترتيب، صفرًا فما فوق."""
        return _STEP_SEQUENCE.index(self)


_STEP_SEQUENCE: Final[tuple[DirectCertaintyStep, ...]] = (
    DirectCertaintyStep.DATA_PURITY_CHECK,
    DirectCertaintyStep.RAW_COUNT,
    DirectCertaintyStep.RAW_SAMPLE_INSPECTION,
    DirectCertaintyStep.ONE_CONDITION_AT_A_TIME,
    DirectCertaintyStep.ITERATE_UNTIL_FULL_CLASSIFICATION,
    DirectCertaintyStep.FREEZE_ASSESSMENT,
)


# --- تصريحُ خطوةٍ واحدة: كودٌ يُستدعى لا وصفٌ يُقرأ ----------------------------


@dataclass(frozen=True)
class StepRecord:
    """خطوةٌ مُصرَّحٌ بإتمامها، ومعها الكودُ الذي يُعيد إنتاجها الآن.

    `reproducer_module` و`reproducer_callable` ليسا توثيقًا: `run_step`
    يستوردهما ويستدعيهما فعلًا، فتصريحٌ بلا كودٍ يُستورَد ساقطٌ عند أوّل استدعاء.
    """

    step: DirectCertaintyStep
    reproducer_module: str
    reproducer_callable: str
    source_genus: CertaintySourceGenus

    def __post_init__(self) -> None:
        if not isinstance(self.step, DirectCertaintyStep):
            raise DirectCertaintyError("الخطوةُ عضوٌ في `DirectCertaintyStep`.")
        if not self.reproducer_module.strip():
            raise DirectCertaintyError(
                "خطوةٌ بلا وحدةٍ تُعيد إنتاجَها تصريحٌ لا دليل؛ والاسمُ لا يُترك فارغًا."
            )
        if not self.reproducer_callable.strip():
            raise DirectCertaintyError(
                "خطوةٌ بلا دالةٍ تُستدعى لا تُعاد، وما لا يُعاد لا يُجمَّد."
            )
        if not isinstance(self.source_genus, CertaintySourceGenus):
            raise DirectCertaintyError("جنسُ المصدر عضوٌ في `CertaintySourceGenus`.")

    @property
    def is_directly_verified(self) -> bool:
        """أجاء إتمامُ هذه الخطوة من تشغيلٍ الآن لا من نقلٍ عن رسالة؟"""
        return self.source_genus.supports_freeze


def run_step(record: StepRecord) -> Any:
    """استورد دالةَ الخطوة واستدعِها الآن، وأعِد ناتجَها كما هو.

    هذا هو الاختبارُ العمليُّ مُرمَّزًا: إن لم تُستورَد الوحدةُ أو لم تُوجَد
    الدالةُ أو لم تكن قابلةً للاستدعاء، فالخطوةُ غيرُ قائمةٍ مهما قيل عنها.
    ولا يُفحَص الناتجُ هنا ولا يُحكَم عليه؛ المُتحقَّقُ منه هو قابليةُ الإعادة.
    """
    try:
        module = importlib.import_module(record.reproducer_module)
    except ImportError as error:
        raise DirectCertaintyError(
            f"وحدةُ إعادة الإنتاج لا تُستورَد: {record.reproducer_module}؛ "
            "وما لا يُستورَد لا يُشغَّل."
        ) from error
    try:
        target = getattr(module, record.reproducer_callable)
    except AttributeError as error:
        raise DirectCertaintyError(
            f"لا دالةَ باسم {record.reproducer_callable} في "
            f"{record.reproducer_module}؛ والاسمُ المكتوبُ غيرُ المقروء."
        ) from error
    if not callable(target):
        raise DirectCertaintyError(
            f"{record.reproducer_callable} ليس قابلًا للاستدعاء، والتصريحُ به "
            "إعادةَ إنتاجٍ دعوى بلا تشغيل."
        )
    return target()


# --- مسارُ البروتوكول: بلا قفزةٍ ولا تكرار ------------------------------------


@dataclass(frozen=True)
class ProtocolRun:
    """تسلسلُ خطواتٍ مُصرَّحٍ بها، مرتّبٌ من الصفر بلا فجوةٍ ولا تكرار."""

    records: tuple[StepRecord, ...]

    def __post_init__(self) -> None:
        seen: set[DirectCertaintyStep] = set()
        expected = 0
        for record in self.records:
            if not isinstance(record, StepRecord):
                raise DirectCertaintyError("كلُّ عنصرٍ في المسار `StepRecord`.")
            if record.step in seen:
                raise DirectCertaintyError(
                    f"خطوةٌ مكرّرة: {record.step.value}؛ وتكرارُ خطوةٍ لا يُغني عن أخرى."
                )
            if record.step.position != expected:
                raise DirectCertaintyError(
                    f"الخطوةُ {record.step.value} في الموضع {record.step.position} "
                    f"بينما المنتظَرُ الموضع {expected}؛ ولا تُتخطّى خطوةٌ ولا تُقدَّم."
                )
            seen.add(record.step)
            expected += 1

    @property
    def completed_steps(self) -> tuple[DirectCertaintyStep, ...]:
        """الخطواتُ المُصرَّحُ بها بترتيبها."""
        return tuple(record.step for record in self.records)

    @property
    def missing_steps(self) -> tuple[DirectCertaintyStep, ...]:
        """ما لم يُصرَّح به من الخطوات الستّ، بترتيبها."""
        done = set(self.completed_steps)
        return tuple(step for step in _STEP_SEQUENCE if step not in done)

    @property
    def unverified_steps(self) -> tuple[DirectCertaintyStep, ...]:
        """خطواتٌ صُرِّح بها من مصدرٍ لم يُشغَّل الآن."""
        return tuple(
            record.step for record in self.records if not record.is_directly_verified
        )


class FreezeStatus(Enum):
    """حكمُ التجميد؛ ولا حالةَ ثالثةَ تُقرأ قبولًا ضمنيًّا."""

    FROZEN_ADMISSIBLE = "frozen_admissible"
    REFUSED_INCOMPLETE_STEPS = "refused_incomplete_steps"
    REFUSED_UNVERIFIED_SOURCE = "refused_unverified_source"


@dataclass(frozen=True)
class FreezeAssessment:
    """حكمُ التجميد ومعه علّتُه وما نقص وما لم يُتحقَّق منه مباشرة."""

    status: FreezeStatus
    reason: str
    missing_steps: tuple[DirectCertaintyStep, ...]
    unverified_steps: tuple[DirectCertaintyStep, ...]

    def __post_init__(self) -> None:
        if not self.reason.strip():
            raise DirectCertaintyError("حكمٌ بلا علّةٍ مكتوبةٍ لا يُقرأ ولا يُردّ.")
        if self.status is FreezeStatus.FROZEN_ADMISSIBLE and (
            self.missing_steps or self.unverified_steps
        ):
            raise DirectCertaintyError(
                "لا يجتمع تجميدٌ مقبولٌ مع خطوةٍ ناقصةٍ أو غيرِ مُتحقَّقٍ منها مباشرة."
            )


def assess_freeze(run: ProtocolRun) -> FreezeAssessment:
    """احكم على التجميد: النقصُ أوّلًا، ثمّ جنسُ المصدر، ولا قبولَ بغيرهما.

    ويُقدَّم النقصُ على جنس المصدر لأن خطوةً لم تُصرَّح أصلًا لا يُسأل عن جنس
    مصدرها؛ ويُسمّى النقصان كلاهما في الحكم فلا يُخفي أحدُهما الآخر.
    """
    missing = run.missing_steps
    unverified = run.unverified_steps
    if missing:
        return FreezeAssessment(
            status=FreezeStatus.REFUSED_INCOMPLETE_STEPS,
            reason=(
                "لم تكتمل الخطواتُ الستّ، والناقصُ منها: "
                + "، ".join(step.value for step in missing)
            ),
            missing_steps=missing,
            unverified_steps=unverified,
        )
    if unverified:
        return FreezeAssessment(
            status=FreezeStatus.REFUSED_UNVERIFIED_SOURCE,
            reason=(
                "خطواتٌ صُرِّح بإتمامها من مصدرٍ لم يُشغَّل الآن: "
                + "، ".join(step.value for step in unverified)
            ),
            missing_steps=(),
            unverified_steps=unverified,
        )
    return FreezeAssessment(
        status=FreezeStatus.FROZEN_ADMISSIBLE,
        reason="اكتملت الخطواتُ الستّ، وكلُّ خطوةٍ منها مُعادةٌ تشغيلًا الآن.",
        missing_steps=(),
        unverified_steps=(),
    )


# --- أرقامٌ وصلت سردًا: تُسجَّل بقيدها ولا تُحذَف ولا تُصدَّق --------------------


class FigureConstraint(Enum):
    """القيدُ الذي يُقرأ الرقمُ تحته، مكتوبًا معه لا مفصولًا عنه."""

    COMPUTED_ON_UNPURIFIED_DATA = "computed_on_unpurified_data"
    NOT_RE_DERIVABLE_IN_THIS_TREE = "not_re_derivable_in_this_tree"
    CLASSIFICATION_INCOMPLETE = "classification_incomplete"


@dataclass(frozen=True)
class UnverifiedFigureRecord:
    """رقمٌ وصل خبرًا لا قياسًا، مُسجَّلٌ بجنس مصدره وبقيده.

    ولا يقوم هذا السجلُّ على جنسٍ يصلح للتجميد: رقمٌ أُعيد تشغيلُه الآن ليس
    «غيرَ مُتحقَّقٍ منه»، وإقحامُه هنا يُلبِس السجلَّ غيرَ بابه.
    """

    subject: str
    figure_text: str
    source_genus: CertaintySourceGenus
    constraint: FigureConstraint

    def __post_init__(self) -> None:
        if not self.subject.strip():
            raise DirectCertaintyError("رقمٌ بلا موضوعٍ مُسمًّى لا يُراجَع.")
        if not self.figure_text.strip():
            raise DirectCertaintyError("سجلُّ رقمٍ بلا رقمٍ مكتوبٍ ليس سجلًّا.")
        if not isinstance(self.constraint, FigureConstraint):
            raise DirectCertaintyError("القيدُ عضوٌ في `FigureConstraint`.")
        if not isinstance(self.source_genus, CertaintySourceGenus):
            raise DirectCertaintyError("جنسُ المصدر عضوٌ في `CertaintySourceGenus`.")
        if self.source_genus.supports_freeze:
            raise DirectCertaintyError(
                "ما أُعيد تشغيلُه الآن لا يُسجَّل غيرَ مُتحقَّقٍ منه؛ وهذا السجلُّ "
                "لِما وصل خبرًا لا لِما قام قياسًا."
            )


REPORTED_UNVERIFIED_FIGURES: Final[tuple[UnverifiedFigureRecord, ...]] = (
    UnverifiedFigureRecord(
        subject="توكناتُ التلوّث في ملفّ النصّ المذكور في نصّ البروتوكول",
        figure_text="٤٥٣٣ من أصل ٨٢٤١٤",
        source_genus=CertaintySourceGenus.PROSE_FROM_ANOTHER_CONVERSATION,
        constraint=FigureConstraint.NOT_RE_DERIVABLE_IN_THIS_TREE,
    ),
    UnverifiedFigureRecord(
        subject="موضعُ السطر الذي حمل التذييل",
        figure_text="السطر ٦٢٣٨",
        source_genus=CertaintySourceGenus.PROSE_FROM_ANOTHER_CONVERSATION,
        constraint=FigureConstraint.NOT_RE_DERIVABLE_IN_THIS_TREE,
    ),
    UnverifiedFigureRecord(
        subject="ما أوقفه الفلترُ السلبيُّ الأوّل",
        figure_text="١٣٨ توكنًا",
        source_genus=CertaintySourceGenus.PROSE_FROM_ANOTHER_CONVERSATION,
        constraint=FigureConstraint.NOT_RE_DERIVABLE_IN_THIS_TREE,
    ),
    UnverifiedFigureRecord(
        subject="نسبةُ التصنيف قبل التنقية",
        figure_text="٩٠٫٤٧٪ و٩٢٫٦١٪",
        source_genus=CertaintySourceGenus.PROSE_FROM_ANOTHER_CONVERSATION,
        constraint=FigureConstraint.COMPUTED_ON_UNPURIFIED_DATA,
    ),
    UnverifiedFigureRecord(
        subject="نسبةُ التصنيف بعد التنقية، وباقيها غيرُ المُصنَّف كليًّا",
        figure_text="٩٣٫١١٪، والباقي ٦٫٨٩٪",
        source_genus=CertaintySourceGenus.PROSE_FROM_ANOTHER_CONVERSATION,
        constraint=FigureConstraint.CLASSIFICATION_INCOMPLETE,
    ),
    UnverifiedFigureRecord(
        subject="تمامُ فضاء الحامل/الحالة المذكور في سُلَّم اليقين",
        figure_text="١٣١/١٣١",
        source_genus=CertaintySourceGenus.PROSE_FROM_ANOTHER_CONVERSATION,
        constraint=FigureConstraint.NOT_RE_DERIVABLE_IN_THIS_TREE,
    ),
    UnverifiedFigureRecord(
        subject="انعكاسُ الحامل/الحالة إلى نصٍّ مُشكَّل على مُدوَّنةٍ مغلقة",
        figure_text="١٠٠٫٠٠٠٠٪ على ٧٨٬٢٤٥ كلمة",
        source_genus=CertaintySourceGenus.PROSE_FROM_ANOTHER_CONVERSATION,
        constraint=FigureConstraint.NOT_RE_DERIVABLE_IN_THIS_TREE,
    ),
    UnverifiedFigureRecord(
        subject="المطابقةُ المذكورة بلا استثناء في مقدّمة سُلَّم اليقين",
        figure_text="٢٨/٢٨",
        source_genus=CertaintySourceGenus.PROSE_FROM_ANOTHER_CONVERSATION,
        constraint=FigureConstraint.NOT_RE_DERIVABLE_IN_THIS_TREE,
    ),
    UnverifiedFigureRecord(
        subject="تسلسلُ الانزلاق المذكور في قاعدة النتيجتين",
        figure_text="٦٩٫٢٪ ← ٩٦٫٥٥٪ ← ٩٩٫٨٣٪ ← «١٠٠٪»",
        source_genus=CertaintySourceGenus.PROSE_FROM_ANOTHER_CONVERSATION,
        constraint=FigureConstraint.NOT_RE_DERIVABLE_IN_THIS_TREE,
    ),
    UnverifiedFigureRecord(
        subject="الرقمُ الوسط غيرُ المُفسَّر في اختبار CV+CV الأوّل",
        figure_text="٦٩٫٥٧٪",
        source_genus=CertaintySourceGenus.PROSE_FROM_ANOTHER_CONVERSATION,
        constraint=FigureConstraint.CLASSIFICATION_INCOMPLETE,
    ),
    UnverifiedFigureRecord(
        subject="نسبةُ الفتحة في «إنّ وأخواتها» المذكورة مثالًا لليقين التامّ",
        figure_text="٥٣٫٠٪",
        source_genus=CertaintySourceGenus.PROSE_FROM_ANOTHER_CONVERSATION,
        constraint=FigureConstraint.NOT_RE_DERIVABLE_IN_THIS_TREE,
    ),
    UnverifiedFigureRecord(
        subject="تمامُ الأسماء الخمسة المذكور مثالًا لليقين التامّ",
        figure_text="١٥/١٥",
        source_genus=CertaintySourceGenus.PROSE_FROM_ANOTHER_CONVERSATION,
        constraint=FigureConstraint.NOT_RE_DERIVABLE_IN_THIS_TREE,
    ),
    UnverifiedFigureRecord(
        subject="عددُ قواعد «النحو الواضح» المذكورُ في اقتراح المصدر النحويّ",
        figure_text="٤٢١ قاعدة",
        source_genus=CertaintySourceGenus.PROSE_FROM_ANOTHER_CONVERSATION,
        constraint=FigureConstraint.NOT_RE_DERIVABLE_IN_THIS_TREE,
    ),
    UnverifiedFigureRecord(
        subject="عددُ أجزاء «النحو الواضح» المذكورُ في الاقتراح نفسِه",
        figure_text="٣ أجزاء",
        source_genus=CertaintySourceGenus.PROSE_FROM_ANOTHER_CONVERSATION,
        constraint=FigureConstraint.NOT_RE_DERIVABLE_IN_THIS_TREE,
    ),
)
"""أرقامُ نصّ البروتوكول نفسِه، مقروءةً بقاعدته: خبرٌ مُسجَّلٌ لا قياسٌ مقبول."""


# --- ما تتركه هذه الوحدة مفتوحًا، مُسمًّى ------------------------------------


COMPLETION_IS_A_RUN_NOT_A_DECLARATION: Final[str] = (
    "COMPLETION_IS_A_RUN_NOT_A_DECLARATION: `StepRecord` يُلزِم باسم وحدةٍ "
    "ودالةٍ، و`run_step` يستوردهما ويستدعيهما؛ فلا تقوم خطوةٌ بتصريحٍ مكتوبٍ "
    "وحده. ولا يُفحَص ناتجُ الدالة هنا: المُتحقَّقُ منه قابليةُ الإعادة لا صحّةُ "
    "المُعاد"
)

RECORDING_IS_NOT_ENDORSING: Final[str] = (
    "RECORDING_IS_NOT_ENDORSING: `REPORTED_UNVERIFIED_FIGURES` يحفظ أرقامَ "
    "نصّ البروتوكول بجنس مصدرها وقيدها؛ فلا تُحذَف فيُخفى الخبر، ولا تُقرَأ "
    "قياسًا فيُصدَّق ما لم يُشغَّل"
)

STEP_ZERO_WAS_ADDED_AFTER_THE_FIVE_NOTE: Final[str] = (
    "STEP_ZERO_WAS_ADDED_AFTER_THE_FIVE: كانت الخطواتُ خمسًا، ثمّ أُضيف كاشفُ "
    "التلوّث خطوةً صفرًا قبلها، فصارت ستًّا؛ وذكرُ العددَين في نصّ البروتوكول "
    "أثرُ هذه الإضافة لا تناقضٌ فيه"
)

UNREAD_STEP_ORDER_IS_NOT_A_RANKING: Final[str] = (
    "UNREAD_STEP_ORDER_IS_NOT_A_RANKING: ترتيبُ الخطوات شرطُ إجراءٍ لا سُلَّمُ "
    "قوّةٍ معرفية؛ فلا يُقرَأ تقدُّمُ خطوةٍ على أخرى تفضيلًا لدليلها"
)

NO_KERNEL_MODULE_CONSUMES_THIS_PROTOCOL: Final[str] = (
    "NO_KERNEL_MODULE_CONSUMES_THIS_PROTOCOL: لا تقرأ هذه الوحدةَ أيُّ بوّابةٍ "
    "في `kernel/`، ولا تدخل في ولادةٍ ولا في ترخيصِ انتقال؛ فحكمُها على من "
    "استعملها لا على الشجرة كلّها"
)

DIRECT_CERTAINTY_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "COMPLETION_IS_A_RUN_NOT_A_DECLARATION": COMPLETION_IS_A_RUN_NOT_A_DECLARATION,
    "RECORDING_IS_NOT_ENDORSING": RECORDING_IS_NOT_ENDORSING,
    "STEP_ZERO_WAS_ADDED_AFTER_THE_FIVE": STEP_ZERO_WAS_ADDED_AFTER_THE_FIVE_NOTE,
    "UNREAD_STEP_ORDER_IS_NOT_A_RANKING": UNREAD_STEP_ORDER_IS_NOT_A_RANKING,
    "NO_KERNEL_MODULE_CONSUMES_THIS_PROTOCOL": NO_KERNEL_MODULE_CONSUMES_THIS_PROTOCOL,
}
"""ما لا تحسمه هذه الوحدة، مُسمًّى هنا لا متروكًا ليُفترَض."""
