"""ربطُ الخطوة بكودها: أن يُستدعى شيءٌ ليس أن يُستدعى كودُ هذه الخطوة.

كشفت المرحلةُ الثالثة عشرة، وهي تبني أمثلتَها، ثغرةً في الخطوة الثانية من
بروتوكول اليقين المباشر: `StepRecord` يُلزِم باسم وحدةٍ ودالة، و`run_step`
يستوردهما ويستدعيهما، ولا شيءَ في ذلك يربط الدالةَ بالخطوة التي صُرِّح بها::

    ImportsAndRuns  != RunsThisStep
    CallableExists  != StepIsImplemented
    ReaderSaysNo    != GateRefuses

فمسارٌ تُوجَّه خطواتُه الستُّ كلُّها إلى دالةٍ واحدةٍ من كاشف التلوّث يُخرِج
`FROZEN_ADMISSIBLE` اليوم؛ وذلك ما تفعله أمثلةُ الاختبارات نفسُها، لا لتحايلٍ
بل لأنّ الشجرة لم تملك كودًا لخمسٍ من الخطوات يوم كُتب هذا (وهي أربعٌ اليوم بعد
ملء صفّ `RAW_COUNT`). وهذه نتيجةٌ من الفئة
الثانية بمصطلح `binary_outcome`: لم تُغلَق الفجوة، وضاق المجهولُ بمعلومةٍ
مُسمّاة؛ ولذلك سُجِّلت هنا في `STEP_BINDING_DISCOVERY` بتلك الآلة نفسِها لا
بنثرٍ على هامشها.

**والمُسجَّلُ هنا ثلاثةُ أحوالٍ لا حالان.** أن تكون الدالةُ مُسجَّلةً لخطوتها،
أو مُسجَّلةً لخطوةٍ أخرى، أو **غيرَ مُسجَّلةٍ أصلًا**. والثالثةُ ليست رفضًا:
سجلُّ هذه الوحدة مكتوبٌ لا مُستقصًى، فدالةٌ صالحةٌ خارجه تُقرأ «لم يَحكم فيها»
لا «مردودة» (`ABSENCE_FROM_THE_REGISTRY_IS_NOT_A_REFUSAL`).

**وهذه الوحدة قارئٌ لا بوّابة.** لا تُعدِّل `assess_freeze` ولا تُغلِّظ شرطَه،
ولا تستوردها `direct_certainty`؛ فالمسارُ الذي يرفضه هذا القارئ يبقى مقبولًا
عند ذلك الحكم كما كان (`THIS_READER_IS_NOT_A_GATE`). وإغلاقُ الثغرة في موضع
الحكم قرارٌ لم يُتَّخذ هنا، وتركُه مكتوبٌ لا مطويّ.

**وكشفت القراءةُ حدًّا ثانيًا لم يكن مقصودًا.** `run_step` يستدعي الدالةَ بلا
وسائط، فما لا يقوم بلا وسيطٍ لا يصلح مُعيدًا للإنتاج مهما كان هو الكودَ نفسَه:
`scan_lines` و`scan_tokens` هما كاشفُ التلوّث عينُه ولا يُستدعيان فارغَين.
و`derive_reproducers_run_step_cannot_call` يُخرج ذلك اشتقاقًا من التواقيع لا
إعلانًا (`THE_PROTOCOL_TEST_IS_NARROWED_TO_ZERO_ARGUMENT_ENTRY_POINTS`).

**ولا تستورد هذه الوحدةُ وحدةً عربيةً في رأسها.** مُعيدُ إنتاج الخطوة الأولى
يُستورَد داخل `derive_raw_count_record` وحدَها، وبقيةُ السجلّ أسماءٌ تُحَلّ عند
الطلب؛ فالقارئُ يبقى قارئًا لا مالكًا لكودٍ بعينه.
"""

from __future__ import annotations

import importlib
import inspect
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Final

from .binary_outcome import DeeperLayerRecord, MidFigureClassification
from .direct_certainty import DirectCertaintyStep, ProtocolRun, StepRecord

__all__ = [
    "ABSENCE_FROM_THE_REGISTRY_IS_NOT_A_REFUSAL",
    "A_BOUND_STEP_IS_NOT_A_CORRECT_MEASUREMENT",
    "REGISTRY_IS_DECLARED_NOT_DISCOVERED",
    "STEP_BINDING_DISCOVERY",
    "STEP_REPRODUCERS",
    "STEP_REPRODUCERS_NAMED_RESIDUALS",
    "THE_PROTOCOL_TEST_IS_NARROWED_TO_ZERO_ARGUMENT_ENTRY_POINTS",
    "THIS_READER_IS_NOT_A_GATE",
    "BindingRow",
    "BindingStanding",
    "ReproducerRef",
    "StepImplementationStanding",
    "StepReproducerError",
    "assess_record_binding",
    "assess_run_bindings",
    "derive_implemented_steps",
    "derive_raw_count_record",
    "derive_reproducers_run_step_cannot_call",
    "derive_unimplemented_steps",
    "step_implementation_standing",
]


class StepReproducerError(ValueError):
    """رُوجِع السجلُّ بما لا يقوم به: مرجعٌ بلا اسم، أو خطوةٌ خارج مفردتها."""


# --- مرجعُ الكود: وحدةٌ ودالةٌ تُستورَدان لا تُوصَفان --------------------------


@dataclass(frozen=True)
class ReproducerRef:
    """اسمُ وحدةٍ واسمُ دالةٍ فيها، مقروءان لا مُفترَضَين."""

    module: str
    callable_name: str

    def __post_init__(self) -> None:
        if not isinstance(self.module, str) or not self.module.strip():
            raise StepReproducerError("مرجعُ الكود يُسمّي وحدتَه، والاسمُ غيرُ فارغ.")
        if not isinstance(self.callable_name, str) or not self.callable_name.strip():
            raise StepReproducerError("مرجعُ الكود يُسمّي دالتَه، والاسمُ غيرُ فارغ.")

    def resolve(self) -> object:
        """استورد الوحدةَ وأخرِج الدالةَ؛ وما لا يُستورَد لا يُقال إنه قائم."""
        try:
            module = importlib.import_module(self.module)
        except ImportError as error:
            raise StepReproducerError(
                f"وحدةٌ لا تُستورَد: {self.module}؛ ومرجعٌ لا يُحَلّ ليس مرجعًا."
            ) from error
        try:
            return getattr(module, self.callable_name)
        except AttributeError as error:
            raise StepReproducerError(
                f"لا دالةَ باسم {self.callable_name} في {self.module}."
            ) from error


_GATE_MODULE: Final[str] = "alghanem.arabic.encoding.contamination_gate"
_RAW_COUNT_MODULE: Final[str] = "alghanem.arabic.alif_state_raw_count"
_INSPECTION_MODULE: Final[str] = "alghanem.arabic.alif_carrier_inspection"


STEP_REPRODUCERS: Final[Mapping[DirectCertaintyStep, tuple[ReproducerRef, ...]]] = (
    MappingProxyType(
        {
            DirectCertaintyStep.DATA_PURITY_CHECK: (
                ReproducerRef(_GATE_MODULE, "scan_tokens"),
                ReproducerRef(_GATE_MODULE, "scan_lines"),
                ReproducerRef(_GATE_MODULE, "derive_negative_filter_blind_spots"),
                ReproducerRef(_GATE_MODULE, "derive_head_tail_blind_spot"),
            ),
            DirectCertaintyStep.RAW_COUNT: (
                ReproducerRef(
                    _RAW_COUNT_MODULE, "run_raw_count_on_the_deposited_fatiha"
                ),
            ),
            DirectCertaintyStep.RAW_SAMPLE_INSPECTION: (
                ReproducerRef(
                    _INSPECTION_MODULE,
                    "inspect_the_deposited_fatiha_alif_carriers",
                ),
            ),
            DirectCertaintyStep.ONE_CONDITION_AT_A_TIME: (),
            DirectCertaintyStep.ITERATE_UNTIL_FULL_CLASSIFICATION: (),
            DirectCertaintyStep.FREEZE_ASSESSMENT: (),
        }
    )
)
"""كودُ كلّ خطوةٍ في هذه الشجرة؛ وثلاثُ خطواتٍ خاليةٌ، وخلوُّها مقروءٌ لا مطويّ.

وكانت خمسًا حين سُجِّل `STEP_BINDING_DISCOVERY`، ثمّ مُلئ صفُّ `RAW_COUNT`
بمدخلٍ عديم الوسائط في `alghanem.arabic.alif_state_raw_count` يُشغِّل كاشفَ
التلوّث ثمّ يعُدّ ذرّات نصٍّ عربيٍّ مُودَعٍ بحروفه، ثمّ مُلئ صفُّ
`RAW_SAMPLE_INSPECTION` بمدخلٍ عديم الوسائط في
`alghanem.arabic.alif_carrier_inspection` يقرأ صفوفَ ذلك العدّ بسياقها ولا
يُعيد عدَّها.

و`FREEZE_ASSESSMENT` خاليةٌ عن قصدٍ لا عن سهو: `assess_freeze` يحكم على المسار
كلِّه، فجعلُه خطوةً داخل المسار يجعل المسارَ يشهد لنفسه.
"""

if set(STEP_REPRODUCERS) != set(DirectCertaintyStep):  # pragma: no cover - guard
    raise RuntimeError("every protocol step needs a row, occupied or empty")


# --- رتبةُ الخطوة: أتملك هذه الشجرةُ كودًا لها؟ -------------------------------


class StepImplementationStanding(Enum):
    """أفي الشجرة كودٌ مُسجَّلٌ لهذه الخطوة، أم لا؟ مُشتَقٌّ من السجلّ لا مكتوب."""

    IMPLEMENTED_IN_THIS_TREE = "implemented_in_this_tree"
    NO_IMPLEMENTATION_IN_THIS_TREE = "no_implementation_in_this_tree"


def step_implementation_standing(
    step: DirectCertaintyStep,
) -> StepImplementationStanding:
    """رتبةُ خطوةٍ بعينها، محسوبةً من شغور صفّها في السجلّ لا من إعلان."""
    if not isinstance(step, DirectCertaintyStep):
        raise StepReproducerError("الخطوةُ عضوٌ في `DirectCertaintyStep`.")
    if STEP_REPRODUCERS[step]:
        return StepImplementationStanding.IMPLEMENTED_IN_THIS_TREE
    return StepImplementationStanding.NO_IMPLEMENTATION_IN_THIS_TREE


def derive_implemented_steps() -> tuple[DirectCertaintyStep, ...]:
    """الخطواتُ التي تملك هذه الشجرةُ كودًا لها، بترتيب البروتوكول."""
    return tuple(
        step
        for step in DirectCertaintyStep
        if step_implementation_standing(step)
        is StepImplementationStanding.IMPLEMENTED_IN_THIS_TREE
    )


def derive_unimplemented_steps() -> tuple[DirectCertaintyStep, ...]:
    """الخطواتُ التي لا كودَ لها هنا؛ وهي المعلومةُ التي ضاق بها المجهول."""
    return tuple(
        step
        for step in DirectCertaintyStep
        if step_implementation_standing(step)
        is StepImplementationStanding.NO_IMPLEMENTATION_IN_THIS_TREE
    )


# --- رتبةُ الربط: أهذا كودُ هذه الخطوة، أم كودُ غيرها، أم لم يُحكَم فيه؟ -------


class BindingStanding(Enum):
    """أحوالُ ربطِ التصريح بالكود الثلاثة؛ والثالثةُ امتناعٌ عن الحكم لا رفض."""

    BOUND_TO_ITS_OWN_STEP = "bound_to_its_own_step"
    BOUND_TO_ANOTHER_STEPS_CODE = "bound_to_another_steps_code"
    UNJUDGED_NOT_IN_THE_REGISTRY = "unjudged_not_in_the_registry"

    @property
    def is_a_named_mismatch(self) -> bool:
        """أهذه الحالُ مخالفةٌ مُسمّاة، لا امتناعًا عن الحكم ولا موافقة؟"""
        return self is BindingStanding.BOUND_TO_ANOTHER_STEPS_CODE


@dataclass(frozen=True)
class BindingRow:
    """صفُّ تصريحٍ واحد: خطوتُه، ومرجعُه، ورتبةُ ربطه، ورتبةُ خطوته.

    ويُكتَب صفٌّ لكلّ تصريحٍ مقروء — الموافقُ والمخالفُ وما لم يُحكَم فيه —
    على نمط `NormalizationResidualTable`: لا يُطرَح شيءٌ قبل أن يراه أحد.
    """

    step: DirectCertaintyStep
    declared: ReproducerRef
    standing: BindingStanding
    step_standing: StepImplementationStanding
    registered_for: tuple[DirectCertaintyStep, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.step, DirectCertaintyStep):
            raise StepReproducerError("الخطوةُ عضوٌ في `DirectCertaintyStep`.")
        if not isinstance(self.declared, ReproducerRef):
            raise StepReproducerError("المرجعُ المُصرَّحُ به `ReproducerRef`.")
        if not isinstance(self.standing, BindingStanding):
            raise StepReproducerError("رتبةُ الربط عضوٌ في `BindingStanding`.")
        if not isinstance(self.step_standing, StepImplementationStanding):
            raise StepReproducerError("رتبةُ الخطوة عضوٌ في مفردتها المغلقة.")
        if self.standing is BindingStanding.BOUND_TO_ITS_OWN_STEP and (
            self.step not in self.registered_for
        ):
            raise StepReproducerError(
                "ربطٌ موافقٌ لخطوةٍ ليست في مواضع تسجيل مرجعه تناقضٌ في الصفّ."
            )
        if (
            self.standing is BindingStanding.UNJUDGED_NOT_IN_THE_REGISTRY
            and self.registered_for
        ):
            raise StepReproducerError(
                "امتناعٌ عن الحكم مع مرجعٍ مُسجَّلٍ لخطوةٍ تناقضٌ في الصفّ."
            )


def _registered_for(ref: ReproducerRef) -> tuple[DirectCertaintyStep, ...]:
    return tuple(step for step, refs in STEP_REPRODUCERS.items() if ref in refs)


def assess_record_binding(record: StepRecord) -> BindingRow:
    """اقرأ تصريحًا واحدًا وأخرِج رتبةَ ربطه؛ ولا يُحكَم على ما ليس في السجلّ."""
    if not isinstance(record, StepRecord):
        raise StepReproducerError("المقروءُ `StepRecord`.")
    declared = ReproducerRef(
        module=record.reproducer_module, callable_name=record.reproducer_callable
    )
    registered = _registered_for(declared)
    if not registered:
        standing = BindingStanding.UNJUDGED_NOT_IN_THE_REGISTRY
    elif record.step in registered:
        standing = BindingStanding.BOUND_TO_ITS_OWN_STEP
    else:
        standing = BindingStanding.BOUND_TO_ANOTHER_STEPS_CODE
    return BindingRow(
        step=record.step,
        declared=declared,
        standing=standing,
        step_standing=step_implementation_standing(record.step),
        registered_for=registered,
    )


def assess_run_bindings(run: ProtocolRun) -> tuple[BindingRow, ...]:
    """صفٌّ لكلّ تصريحٍ في المسار بترتيبه؛ ولا يُختصَر المسارُ إلى حكمٍ واحد.

    ولا تُرَدّ هنا حصيلةٌ جامعة عن قصد: جمعُ الصفوف في «مقبول/مرفوض» يُنشئ
    حكمًا ثانيًا بجانب `assess_freeze`، وهذه الوحدةُ قارئٌ لا بوّابة.
    """
    if not isinstance(run, ProtocolRun):
        raise StepReproducerError("المقروءُ `ProtocolRun`.")
    return tuple(assess_record_binding(record) for record in run.records)


# --- حدُّ الاختبار العمليّ نفسِه، مُشتَقًّا من التواقيع ------------------------


def derive_reproducers_run_step_cannot_call() -> tuple[ReproducerRef, ...]:
    """المراجعُ المُسجَّلة التي لا يستطيع `run_step` استدعاءها، مُشتَقّةً.

    و`run_step` يستدعي بلا وسائط، فما وجب له وسيطٌ لا يصلح مُعيدًا للإنتاج وإن
    كان هو كودَ الخطوة بعينه. وهذا حدٌّ في الاختبار العمليّ لا في الكود
    المُستبعَد، ويُخرَج اشتقاقًا من التوقيع لا كتابةً في قائمة.
    """
    unreachable: list[ReproducerRef] = []
    for refs in STEP_REPRODUCERS.values():
        for ref in refs:
            target = ref.resolve()
            if not callable(target):  # pragma: no cover - السجلُّ دوالُّ كلُّه
                unreachable.append(ref)
                continue
            try:
                inspect.signature(target).bind()
            except TypeError:
                unreachable.append(ref)
    return tuple(unreachable)


# --- الكشفُ نفسُه، مُسجَّلًا بآلة قاعدة النتيجتين لا بنثرٍ على هامشها ----------

STEP_BINDING_DISCOVERY: Final[DeeperLayerRecord] = DeeperLayerRecord(
    subject="ربطُ خطوات بروتوكول اليقين المباشر بكودها في هذه الشجرة",
    narrowed_unknown=(
        "تصريحُ الخطوة لا يُقيِّد الدالةَ المُسمّاة بأن تكون كودَ تلك الخطوة، "
        "فمسارٌ تُوجَّه خطواتُه الستُّ إلى دالةٍ واحدةٍ يُقبَل تجميدُه اليوم؛ "
        "وكانت خمسٌ من الخطوات الستّ بلا كودٍ في هذه الشجرة يوم سُجِّل هذا "
        "الكشف، فلا يقوم لها ربطٌ موافقٌ ولو أُريد، ثمّ مُلئ صفُّ `RAW_COUNT` "
        "بمدخلٍ عديم الوسائط، ثمّ صفُّ `RAW_SAMPLE_INSPECTION` بمدخلٍ مثله، "
        "فبقيت ثلاثٌ خاليةً"
    ),
    reason=(
        "المحاولةُ لم تُغلِق الفجوة في موضع الحكم، وسمَّت بدلًا من ذلك موضعَين "
        "قابلَين للقياس: خلوَّ خمسِ خطواتٍ من كودٍ مُسجَّل، وانفصالَ اسم الدالة "
        "عن الخطوة المُصرَّح بها"
    ),
)
"""نتيجةٌ من الفئة الثانية، مكتوبةٌ بصنفها لا موصوفةٌ في تعليق."""


_UNIMPLEMENTED_AT_IMPORT: Final = derive_unimplemented_steps()

if not _UNIMPLEMENTED_AT_IMPORT:  # pragma: no cover - guard
    raise RuntimeError(
        "the recorded discovery names empty step rows; re-read it if they fill"
    )

if STEP_BINDING_DISCOVERY.mid_figure_classification is not None:  # pragma: no cover
    raise RuntimeError("this discovery opens on no middle figure")

_DISCOVERY_GENUS_IF_A_FIGURE_ARRIVES: Final = (
    MidFigureClassification.CORRECT_MEASUREMENT_ON_A_WRONG_QUESTION
)
"""لو قِيس هذا الموضع برقمٍ وسط، فجنسُه هذا: السؤالُ نفسُه يحتاج إعادةَ بناء.

ولا رقمَ اليوم، فالتصنيفُ غيرُ مُسنَدٍ إلى السجلّ ولا يُقرأ قياسًا قائمًا.
"""


def derive_raw_count_record() -> DeeperLayerRecord:
    """شغِّل مُعيدَ إنتاج الخطوة الأولى الآن وأخرِج سجلَّ فئته الثانية بأرقامه.

    والعدُّ نفسُه قائمٌ في `alghanem.arabic.alif_state_raw_count`، ولا تستورد
    طبقةُ العربية طبقةَ البرنامج؛ فموضعُ التصنيف هنا لا هناك، ويُستورَد العدُّ
    داخل الدالّة فلا يصير هذا القارئُ مالكًا لوحدةٍ عربيةٍ بعينها.

    **وهو من الفئة الثانية لا الأولى**: نصٌّ واحدٌ مُشكَّلٌ غيرُ مقابَلٍ لا
    يُغلِق دعوى الألف، وإنّما يُضيِّق المجهولَ بموضعٍ مُسمًّى قابلٍ للعدّ.
    وأرقامُه تُحسَب عند الطلب ولا تُكتَب ثوابتَ، فلا يبقى رقمٌ في الشجرة بعد
    تغيُّر النصّ الذي اشتُقّ منه.
    """
    from ..arabic.alif_state_raw_count import run_raw_count_on_the_deposited_fatiha

    table = run_raw_count_on_the_deposited_fatiha()
    exceptions = table.alif_rows_carrying_a_short_vowel
    return DeeperLayerRecord(
        subject=(
            "حالاتُ الحامل «ا» في نقلٍ مُشكَّلٍ واحدٍ مُودَعٍ في هذه الشجرة "
            f"({table.source_id})"
        ),
        narrowed_unknown=(
            f"في هذا النقل {len(table.rows)} ذرّةَ حامل، منها "
            f"{len(table.alif_rows)} حاملُها ألفٌ مجرّدة، وعددُ الألفات التي "
            "حملت واحدةً من {فتحة، ضمّة، كسرة} هو "
            f"{len(exceptions)}؛ وحملت "
            f"{len(table.other_rows_carrying_a_short_vowel)} ذرّةً من "
            f"{len(table.other_carrier_rows)} ذرّةٍ حاملُها غيرُ الألف إحدى "
            "الثلاث"
        ),
        reason=(
            "عدٌّ خامٌّ على نصٍّ واحدٍ مُشكَّلٍ بالرسم الإملائيّ لم يُقابَل "
            "بطبعةٍ مُسمّاة؛ فهو يُسمّي موضعًا قابلًا للعدّ ولا يمتدّ حكمُه "
            "إلى العربية ولا إلى رسمٍ آخر"
        ),
        opening_mid_figure=(
            f"{len(exceptions)} استثناءً للألف في {len(table.alif_rows)} موضعَ ألف"
        ),
        mid_figure_classification=(
            MidFigureClassification.INCOMPLETE_MEASUREMENT_ON_A_RIGHT_QUESTION
        ),
    )


# --- ما تتركه هذه القراءة مفتوحًا، مُسمًّى ------------------------------------


THIS_READER_IS_NOT_A_GATE: Final[str] = (
    "THIS_READER_IS_NOT_A_GATE: لا تُعدِّل هذه الوحدةُ `assess_freeze` ولا "
    "تُغلِّظ شرطَه ولا تستوردها `direct_certainty`؛ فالمسارُ الذي تُسمّيه هذه "
    "القراءةُ مخالفًا يبقى مقبولًا عند ذلك الحكم كما كان، وإغلاقُ الثغرة في "
    "موضع الحكم قرارٌ لم يُتَّخذ هنا"
)

REGISTRY_IS_DECLARED_NOT_DISCOVERED: Final[str] = (
    "REGISTRY_IS_DECLARED_NOT_DISCOVERED: `STEP_REPRODUCERS` مكتوبٌ في هذه "
    "الوحدة، ولا يُستقصى منه شجرةٌ ولا يُشتقّ من خاصّةٍ في الكود؛ فخلوُّ صفٍّ "
    "يقول إنّ أحدًا لم يُسجِّل له كودًا هنا، لا إنّ الشجرة خاليةٌ منه"
)

ABSENCE_FROM_THE_REGISTRY_IS_NOT_A_REFUSAL: Final[str] = (
    "ABSENCE_FROM_THE_REGISTRY_IS_NOT_A_REFUSAL: دالةٌ خارج السجلّ تُقرأ "
    "`UNJUDGED_NOT_IN_THE_REGISTRY`، وهي امتناعٌ عن الحكم لا حكمٌ بالردّ؛ "
    "وقراءتُها رفضًا تجعل سجلًّا مكتوبًا يُكذِّب كودًا صحيحًا لم يُسجَّل"
)

A_BOUND_STEP_IS_NOT_A_CORRECT_MEASUREMENT: Final[str] = (
    "A_BOUND_STEP_IS_NOT_A_CORRECT_MEASUREMENT: ربطٌ موافقٌ يقول إنّ الدالةَ "
    "مُسجَّلةٌ لهذه الخطوة، ولا يقول إنّ ما أخرجته صحيحٌ ولا إنّ الخطوةَ "
    "أُدّيت على البيانات المقصودة؛ وهو حدُّ `run_step` نفسُه مرفوعًا طبقةً"
)

THE_PROTOCOL_TEST_IS_NARROWED_TO_ZERO_ARGUMENT_ENTRY_POINTS: Final[str] = (
    "THE_PROTOCOL_TEST_IS_NARROWED_TO_ZERO_ARGUMENT_ENTRY_POINTS: `run_step` "
    "يستدعي بلا وسائط، فسؤالُ البروتوكول «أتملك الكود؟» يضيق عمليًّا إلى "
    "«أتملك مدخلًا بلا وسيط؟»؛ و`scan_lines` و`scan_tokens` كاشفُ التلوّث "
    "عينُه ولا يجتازان ذلك، وهو مُشتَقٌّ من التواقيع لا مكتوبٌ في قائمة"
)

STEP_REPRODUCERS_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "THIS_READER_IS_NOT_A_GATE": THIS_READER_IS_NOT_A_GATE,
    "REGISTRY_IS_DECLARED_NOT_DISCOVERED": REGISTRY_IS_DECLARED_NOT_DISCOVERED,
    "ABSENCE_FROM_THE_REGISTRY_IS_NOT_A_REFUSAL": (
        ABSENCE_FROM_THE_REGISTRY_IS_NOT_A_REFUSAL
    ),
    "A_BOUND_STEP_IS_NOT_A_CORRECT_MEASUREMENT": (
        A_BOUND_STEP_IS_NOT_A_CORRECT_MEASUREMENT
    ),
    "THE_PROTOCOL_TEST_IS_NARROWED_TO_ZERO_ARGUMENT_ENTRY_POINTS": (
        THE_PROTOCOL_TEST_IS_NARROWED_TO_ZERO_ARGUMENT_ENTRY_POINTS
    ),
}
"""ما لا تحسمه هذه القراءة، مُسمًّى هنا لا متروكًا ليُفترَض."""
