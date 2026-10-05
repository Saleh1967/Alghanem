"""سلّم رتب الجاهزية للطور الثاني، مفروضًا بالبنية لا مسرودًا في نثر.

الجدول الرباعي الذي يصف حالة الطور الثاني اليوم -- بناءٌ مفحوص، ومواصفةٌ
مستقبلية غير مُجمَّدة بعد، وقياسٌ لم يبدأ، وسؤالٌ مفتوح -- كان يعيش نثرًا في
وصف طلب دمج فقط، لا في شفرة ولا في توثيق المستودع. ونثرٌ خارج البنية يُقرَأ
لاحقًا حقيقةً مُنفَذة وهو غير محروس؛ وهذا بعينه النمط الذي وُجدت
`probe_preregistration` لإغلاقه، مرفوعًا درجةً واحدة::

    FrozenProbeSpecification != EnforcedPreEvidenceSpecification
    RecordedStatusProse      != EnforcedReadinessRecord

**أربع مفردات مغلقة مستقلة، لا مفردةٌ واحدة بأربع قيم.** مفردةٌ واحدة تُوحي
بترتيب كلّي زائف، فيُقرَأ «بدأ القياس» كأنه يستلزم «تُجمِّدت المواصفة» بحكم
موقعه في السلّم، والاستلزام هنا شرطٌ أساسيٌّ سابق لا موضعٌ في سُلَّم.

**ولماذا أربعٌ تحديدًا لا أقلّ؟** لأن دمج أيّ اثنتين يُسقِط حالةً قائمةً
فعلًا اليوم أو يخلق استلزامًا كاذبًا:

* دمج `StructuralReadiness` مع `SpecificationFreeze` في محور واحد يجعل
  «بُني وفُحص» درجةً أدنى من «مُجمَّد»، فيصير التجميد ترقيةً تلقائية للبناء؛
  والحال أن البناء مفحوص اليوم بلا أيّ مواصفة مستقبلية مُجمَّدة، وهي حالةٌ
  صحيحة قائمة لا استثناء.
* دمج `SpecificationFreeze` مع `MeasurementProgress` يُلغي التمييز بين
  «مواصفة مُجمَّدة بلا قياس بعد» و«لا مواصفة أصلًا»، وهما مختلفتان: الأولى
  تُلزِم كل قياس لاحق، والثانية لا تُلزِم شيئًا.
* دمج `MeasurementProgress` مع `QuestionStatus` يجعل اكتمال القياس حسمًا
  للسؤال؛ وقياسٌ مكتملٌ لا يحسم سؤالًا ما لم تكن تجربته مُجمَّدة قبل دليلها
  وناطقةً بمعيار تقويمه.

فالأربع هي العدد الأدنى الذي يُبقي كل حالة قائمة اليوم قابلةً للتعبير بلا
استلزام مُختلَق. وزيادةُ خامسة (كـ«حالة النشر» أو «مرتبة الثقة») ليست بُعدًا
مستقلًّا مُثبَتًا هنا، فلا تُضاف بالحدس.

**الاستلزام باتجاه واحد فقط.** ما يُفرَض شرطٌ أساسيٌّ سابق::

    measurement ∈ {STARTED, COMPLETED} ⟹ specification_freeze = FROZEN
    specification_freeze = FROZEN      ⟹ structural_readiness = BUILT_AND_CHECKED
    question = CLOSED_BY_FROZEN_EXPERIMENT ⟹ measurement = COMPLETED

والعكس لا يُفرَض ولا يُلمَّح إليه: مواصفةٌ مُجمَّدة بلا قياسٍ بعد حالةٌ صحيحة
فعليًّا الآن، وقياسٌ مكتملٌ وسؤالٌ مفتوح حالةٌ صحيحة كذلك.

**`CLOSED_BY_FROZEN_EXPERIMENT` مُعلَنة لا مُغيَّبة، وغير قابلة للبناء اليوم**،
بنفس انضباط `EvidenceGenus.MORPHO_FUNCTIONAL`: إسقاطها من المفردة يُخفي أن
الإغلاق ممكنٌ مبدئيًّا، وقبولها يُتيح كتابة إغلاقٍ لا بوّابة ولادة أصدرته.
والرفض عند الإنشاء نفسه لا عند `PHASE2_READINESS` وحدها، وإلا لأمكن بناء
سجلٍّ آخر يحمل القيمة بلا رادع -- وهي الثغرة عينها التي فُتح هذا العمل
لإغلاقها.

وترتيب الفحوص مقصود: يُقدَّم الرفض المُسمّى للإغلاق على رسالة الاستلزام
العامة، فرفضٌ سببه «لا سلطة ولادة موجودة أصلًا» أعمق من رفضٍ سببه «لم يكتمل
القياس بعد»، ولا يُقرَأ الأعمق كأنه الأسطح.

ملاحظة تسمية، مُسجَّلة لا متجنَّبة صمتًا: هذه المفردات ليست `EvidenceGenus`
ولا `ProbeOutcome` ولا `EvidenceProvenanceGenus`؛ الجاهزية بُعدٌ مستقل عن جنس
الدليل وعن مَصْدريته وعن نتيجة تحقيق، واسمٌ واحد فوق بُعدين هو الانحراف الذي
وُجدت `alghanem.canonical_content` لمنع مثله.

والوحدة خاملة سلطويًّا: `ReadinessRankRecord != BirthVerdict`،
`SpecificationFreeze != Freeze`؛ لا تُنتج ولادةً ولا تُجمِّد في النواة، ولا
تقرؤها أيّ بوّابة فيها، وهو ما يفحصه اختبارٌ يمسح كل وحدات `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from .probe_preregistration import PHASE2_OPEN_QUESTION

_ANSWER_BEARING_FIELD_MARKERS: Final = (
    "answer",
    "verdict",
    "conclusion",
    "resolution",
    "decision",
    "result",
    "outcome",
    "birth",
    "promotion",
)


class ReadinessRankError(ValueError):
    """رُتبةٌ مرفوضة؛ لا تُحمَل على أقرب رتبةٍ مقبولة."""


class StructuralReadiness(Enum):
    """رتبة البناء: أبُني الأثر وفُحص، أم لم يُبنَ بعد؟"""

    NOT_BUILT = "لم_يُبنَ"
    BUILT_AND_CHECKED = "بُني_وفُحص"


class SpecificationFreeze(Enum):
    """رتبة التجميد: أمُجمَّدةٌ مواصفةُ التجربة القادمة قبل دليلها؟"""

    NOT_YET_FROZEN = "لم_تُجمَّد_بعد"
    FROZEN = "مُجمَّدة"


class MeasurementProgress(Enum):
    """رتبة القياس: أبدأ، وأاكتمل؟ ثلاث قيم، فالبدء ليس اكتمالًا."""

    NOT_STARTED = "لم_يبدأ"
    STARTED = "بدأ"
    COMPLETED = "اكتمل"


class QuestionStatus(Enum):
    """رتبة السؤال: أما زال مفتوحًا، أم أغلقته تجربةٌ مُجمَّدة قبل دليلها؟"""

    OPEN = "مفتوح"
    CLOSED_BY_FROZEN_EXPERIMENT = "أُغلق_بتجربة_مُجمَّدة"


if len(StructuralReadiness) != 2:  # pragma: no cover - guard
    raise RuntimeError("structural readiness is deliberately two-valued")
if len(SpecificationFreeze) != 2:  # pragma: no cover - guard
    raise RuntimeError("specification freeze is deliberately two-valued")
if len(MeasurementProgress) != 3:  # pragma: no cover - guard
    raise RuntimeError("measurement progress is deliberately three-valued")
if len(QuestionStatus) != 2:  # pragma: no cover - guard
    raise RuntimeError("question status is deliberately two-valued")


FOUR_INDEPENDENT_RANKS_NOTE: Final = (
    "أربع مفردات مستقلة لا مفردةٌ واحدة بأربع قيم: المفردة الواحدة تُوحي "
    "بترتيب كلّي زائف، فتُقرَأ رتبةٌ أعلى كأنها تستلزم ما دونها بحكم موقعها؛ "
    "ودمج أيّ اثنتين منها يُسقِط حالةً قائمةً اليوم أو يخلق استلزامًا كاذبًا، "
    "فالأربع أدنى عددٍ كافٍ لا عددٌ مُقدَّر"
)

WEAKER_RANK_DOES_NOT_IMPLY_HIGHER_NOTE: Final = (
    "الاستلزام باتجاه واحد فقط: الرتبة الأعلى تشترط ما دونها شرطًا أساسيًّا "
    "سابقًا، ولا يُفرَض العكس؛ فمواصفةٌ مُجمَّدة بلا قياسٍ بعد حالةٌ صحيحة "
    "فعليًّا الآن، وقياسٌ مكتملٌ مع سؤالٍ مفتوح حالةٌ صحيحة كذلك"
)

QUESTION_CLOSURE_DEFERRAL_NOTE: Final = (
    "إغلاق السؤال بتجربة مُجمَّدة مُعلَنٌ في المفردة وغير قابل للبناء اليوم: "
    "لا بوّابة ولادة ولا سلطة حكمٍ موجودة هنا لتُصدره، فكتابته ادّعاءُ إغلاقٍ "
    "لم يُصدره أحد -- ويُرفض عند الإنشاء نفسه لا عند سجلٍّ بعينه"
)

READINESS_AUTHORITY_NOTE: Final = (
    "تسجيلٌ فقط: لا يُنتج هذا السلّم ولادةً ولا حكم ولادة، ولا يُجمَّد في "
    "النواة، ولا تقرأه أيّ بوّابة فيها"
)


def _require_non_blank(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ReadinessRankError(f"{field_name} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class ReadinessRankRecord:
    """حالةٌ واحدة من كل رتبة، بتبريرها، مرفوضةً متى كانت التوافيق كذبًا."""

    question_id: str
    structural_readiness: StructuralReadiness
    specification_freeze: SpecificationFreeze
    measurement: MeasurementProgress
    question: QuestionStatus
    structural_readiness_justification: str
    specification_freeze_justification: str
    measurement_justification: str
    question_justification: str

    def __post_init__(self) -> None:
        _require_non_blank(self.question_id, "معرّف السؤال")
        for value, expected, name in (
            (self.structural_readiness, StructuralReadiness, "رتبة البناء"),
            (self.specification_freeze, SpecificationFreeze, "رتبة التجميد"),
            (self.measurement, MeasurementProgress, "رتبة القياس"),
            (self.question, QuestionStatus, "رتبة السؤال"),
        ):
            if not isinstance(value, expected):
                raise ReadinessRankError(f"{name} must come from its closed vocabulary")
        for justification, name in (
            (self.structural_readiness_justification, "تبرير رتبة البناء"),
            (self.specification_freeze_justification, "تبرير رتبة التجميد"),
            (self.measurement_justification, "تبرير رتبة القياس"),
            (self.question_justification, "تبرير رتبة السؤال"),
        ):
            _require_non_blank(justification, name)

        if self.question is QuestionStatus.CLOSED_BY_FROZEN_EXPERIMENT:
            raise ReadinessRankError(QUESTION_CLOSURE_DEFERRAL_NOTE)
        if (
            self.measurement is not MeasurementProgress.NOT_STARTED
            and self.specification_freeze is not SpecificationFreeze.FROZEN
        ):
            raise ReadinessRankError(
                "قياسٌ بدأ أو اكتمل فوق مواصفةٍ غير مُجمَّدة: هذا اختيار "
                "المعيار بعد رؤية الدليل، وهو ما يمنعه التجميد المسبق"
            )
        if (
            self.specification_freeze is SpecificationFreeze.FROZEN
            and self.structural_readiness is not StructuralReadiness.BUILT_AND_CHECKED
        ):
            raise ReadinessRankError(
                "مواصفةٌ مُجمَّدة فوق بناءٍ لم يُبنَ ويُفحَص: التجميد يقع على "
                "بنيةٍ قائمة لا على نيّةٍ بها"
            )

    @property
    def question_remains_open(self) -> bool:
        """هل بقي السؤال مفتوحًا؟ نعم بنيويًّا في هذه المرحلة، لا اختيارًا."""

        return self.question is QuestionStatus.OPEN


def _assert_no_fields_matching(
    declaring_type: type, markers: tuple[str, ...], message: str
) -> None:
    for item in fields(declaring_type):
        if any(marker in item.name for marker in markers):
            raise RuntimeError(message)


_assert_no_fields_matching(
    ReadinessRankRecord,
    _ANSWER_BEARING_FIELD_MARKERS,
    "a readiness record may not carry an answer, verdict, or birth field",
)


PHASE2_READINESS: Final = ReadinessRankRecord(
    question_id=PHASE2_OPEN_QUESTION.question_id,
    structural_readiness=StructuralReadiness.BUILT_AND_CHECKED,
    specification_freeze=SpecificationFreeze.NOT_YET_FROZEN,
    measurement=MeasurementProgress.NOT_STARTED,
    question=QuestionStatus.OPEN,
    structural_readiness_justification=(
        "بنية التسجيل المسبق مبنيّة ومفحوصة باختباراتها: مواصفةٌ بلا حقل "
        "نتيجة، وسجلّ تجميدٍ وحيد المُصدِر، وربطُ محتوًى يُعيد الترميز ويقارن "
        "البايتات، وإلحاقُ نتيجةٍ غير قابل للبناء بلا ذلك الربط"
    ),
    specification_freeze_justification=(
        "لم تُجمَّد بعدُ أيّ مواصفة تجربةٍ قادمة: البنية تُتيح التجميد ولا "
        "تُنجزه، وإعلانُ التجميد بلا بيانٍ صادر عن السجلّ ادّعاءٌ لا واقع"
    ),
    measurement_justification=(
        "لا قياس بدأ: لا خطّ قياس ولا مدوّنة في هذا المستودع، واختلاق أيّهما "
        "لغرض إظهار تقدّمٍ تزويرٌ لا قياس"
    ),
    question_justification=(
        "سؤال الطور الثاني مسجَّلٌ مفتوحًا باحتمالاته الثلاثة كاملةً، ولا "
        "تجربةَ مُجمَّدة قبل دليلها تفصل بينها، فبقاؤه مفتوحًا هو الحال "
        "الصادقة لا نقصًا يُستدرَك بجواب"
    ),
)


if PHASE2_READINESS.question_id != PHASE2_OPEN_QUESTION.question_id:  # pragma: no cover
    raise RuntimeError("the recorded readiness must reference the recorded question")
if (
    PHASE2_READINESS.question_remains_open is not PHASE2_OPEN_QUESTION.remains_open
):  # pragma: no cover - guard
    raise RuntimeError("readiness and question must not drift about openness")


__all__ = [
    "FOUR_INDEPENDENT_RANKS_NOTE",
    "PHASE2_READINESS",
    "QUESTION_CLOSURE_DEFERRAL_NOTE",
    "READINESS_AUTHORITY_NOTE",
    "WEAKER_RANK_DOES_NOT_IMPLY_HIGHER_NOTE",
    "MeasurementProgress",
    "QuestionStatus",
    "ReadinessRankError",
    "ReadinessRankRecord",
    "SpecificationFreeze",
    "StructuralReadiness",
]
