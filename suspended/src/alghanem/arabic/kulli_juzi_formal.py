"""برهان صوري شامل على نطاق محدود: تقسيم الاسم إلى كلّي وجزئي وتفريعُ كلٍّ منهما.

المصدر النصّي — يُذكَر بالاسم لا إحالةً مبهمة — كتاب "الشخصية الإسلامية" الجزء
الثالث، في تقسيم الاسم إلى كلّي وجزئي:

    "فالكلي هو الذي لا يمنع نفس تصوره من وقوع الشركة فيه، سواء وقعت الشركة
    كالحيوان والإنسان والكاتب... وأما الجزئي فهو الذي لم يشترك في معناه
    كثيرون، مثل زيد علماً على رجل، ومثل الضمائر كهو وهي."

    "والكلي أيضاً نوعان: جنس ومشتق؛ وذلك لأنه إن دل على ذات غير معينة، كالفرس
    والإنسان والسواد... فهو الجنس... وإن دل الكلي على ذي صفة معينة فهو المشتق،
    كالأسود والفارس ونحوهما."

    "وأما الجزئي فهو نوعان علم وضمير... فإن استقل اللفظ بالدلالة... فهو العلم،
    كزيد وكعبد الله. وإن لم يستقل... فهو المضمر، مثل هو وهي."

وفي الموضع نفسه يُفرَّع الكلّي تفريعًا آخر إلى متواطئ يستوي معناه في أفراده
كالإنسان والفرس، ومشكِّك يختلف معناه في أفراده بالوجوب والإمكان أو الاستغناء
والافتقار أو الزيادة والنقصان كالوجود والنور.

بنية المجال — التصريح بالفارق البنيويّ عن الشهادات الثلاث السابقة، قبل الشيفرة
لا بعدها: هذا النصّ **لا يُنتج شجرة قرارٍ واحدة رباعية المستوى**. هو تقسيمٌ أوّل
للاسم (كلّي/جزئي) تتفرّع عنه ثلاثة تفريعاتٍ **مستقلّ بعضها عن بعض**: تفريعان
اثنان للكلّي نفسه — التواطؤ/التشكيك، والجنس/الاشتقاق — وتفريعٌ واحد للجزئي هو
العلم/الضمير. والتفريعان الأوّلان يقسمان المجموعة نفسها قسمتين مختلفتين، لا قسمةً
واحدة على مرحلتين.

ولهذا الفارق أثرٌ مباشر يمنع تزييفًا صامتًا: لو جُعل المجالُ ضربًا ديكارتيًّا في
حالةٍ واحدة صورتها `(كلّي، متواطئ، جنس)` لَلَزِم أن يُنسَب لكل شاهدٍ موضعٌ في
المحورين معًا، والنصّ لا يُثبت ذلك. فـ"الوجود" مُثبَتٌ مشكِّكًا ولم يُثبَت في محور
الجنس/الاشتقاق، و"الأسود" مُثبَتٌ مشتقًّا ولم يُثبَت في محور التواطؤ/التشكيك؛
فوضعُ أيٍّ منهما في خانةٍ جامعة للمحورين استنتاجٌ لا إثبات. فالشاهد هنا يُصرِّح
بمحورٍ واحدٍ مُثبَتٍ بعينه، ويُرفَض بنيويًّا أن يُسأل عن محورٍ آخر لم يُثبَت له،
وتُسجَّل هذه الحدود في حقلٍ مُلزَمٍ على شواهد محورَي الكلّي وحدها
(`ملاحظة استقلال المحورين`)، لا في تعليقٍ يُنسى.

فالحالات المقبولة ثمانٍ بالضبط، لا ستّ ولا اثنتا عشرة:

* `(كلّي، لا_محور_مُثبَت، غير_مطروح)` — الاسم مُثبَتٌ كلّيًّا في موضع التقسيم
  الأوّل وحده.
* `(كلّي، التواطؤ_والتشكيك، متواطئ)` و`(كلّي، التواطؤ_والتشكيك، مشكِّك)`.
* `(كلّي، الجنس_والاشتقاق، جنس)` و`(كلّي، الجنس_والاشتقاق، مشتق)`.
* `(جزئي، لا_محور_مُثبَت، غير_مطروح)` — الاسم مُثبَتٌ جزئيًّا في موضع التقسيم
  الأوّل وحده.
* `(جزئي، العلم_والضمير، علَم)` و`(جزئي، العلم_والضمير، ضمير)`.

وقيمة `غير_مطروح` قيمةٌ مصرَّح بها في المفردة المغلقة، لا `None` صامتة ولا غياب
حقل، كما في الشهادات الثلاث السابقة؛ وبها يُغلَق بنيويًّا كلُّ ما خرج عن الثماني:
محورٌ كلّيٌّ نُسب إلى جزئي، ومحورُ الجزئي نُسب إلى كلّي، ومحورٌ مُصرَّحٌ به بلا
مخرَجٍ مُصرَّح، ومخرَجٌ بلا محور.

ولا تُكتَب إجابةٌ اعتباطًا: إجابةُ التقسيم الأوّل تُشتَقّ من **حامل وقوع الشركة**،
وإجابةُ التفريع تُشتَقّ من **حامل التفريع**؛ ومن حامل التفريع نفسه يُشتَقّ المحورُ
المُصرَّح به، فلا يُكتَب محورٌ يخالف حامله. ويُرفَض أيّ شاهدٍ كُتبت فيه إجابةٌ
مخالفةٌ لحاملها.

ملاحظةٌ واجبة على مصطلح "الجنس" — تُسجَّل ولا تُبنى عليها دالّة: "الجنس" في هذا
النصّ اصطلاحٌ محدَّدٌ ضمن ثنائية جنس/مشتق تحت الكلّي، أي اللفظ الدالّ على ذات غير
معيَّنة. ولا تُثبِت هذه الشهادة أنه الجنسُ الأرسطيُّ المنطقيّ، ولا أنه يُطابق ما
يُسمّى في مفرداتٍ أخرى "الجامد". فمطابقةُ المصطلحين دعوى مستقلّة لم يُقَم عليها
دليلٌ هنا، وهي مسجَّلة بنصّها في `JINS_IS_NOT_A_PROVED_SYNONYM_NOTE` دعوى غير
مبرهَنة، على انضباط `RequestedVocabularyIsNotAttestedVocabulary` نفسه: ورودُ
اسمٍ في مفردتين لا يُثبت أنهما مفردةٌ واحدة.

نطاق الوحدة وحدودها — تسجيل صريح، لا اعتذار لاحق:

* النطاق شواهد مُثبَتة من نصّ واحد بعينه، وثمانية تصنيفات لا تاسع لها هنا. ولا
  تتناول هذه الوحدة الكلّيات الخمس الأرسطية، ولا مراتب التشكيك، ولا أقسام الضمير،
  ولا العلاقة بين هذا التقسيم وتقسيم اللفظ باعتبار الدالّ والمدلول: تلك تحتاج
  شاهدًا لكل قيمة يجعل المجال مكتمل الفروع بالبناء، ولا تملكه هذه الوحدة، وإدخالها
  الآن ادّعاءُ نطاقٍ غير مبرهَن.
* سلطويًّا: `FormalClassification != BirthVerdict`، و
  `DeclaredUniversality != BornOntology`. هذا توثيق وتصنيف صوري فقط: لا نوع في
  `kernel/`، ولا `Freeze`، ولا `E0`، ولا بوّابة نواة تقرأ هذه المخرجات. لا تدخل
  نتيجة هذه الوحدة في `BirthExperimentSpecification`، ولا يقرأها
  `IndependentClosureGate` ولا `BirthVerdictGate`، ولا تغيّر نتيجة التدقيق
  الخارجي، ويبقى كل حقل فيه مطابقًا بايتيًّا.
* عند نجاح البرهان الشامل تُستعمل التسمية الدقيقة وحدها: "شهادة صورية شاملة
  ناجحة على نطاق محدود" — لا "ولادة"، فتلك تسمية لاحقة تحتاج `Freeze` و`E0` لم
  يُبنَيا بعد.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from .text_key import comparison_key


class KulliJuziFormalError(ValueError):
    """رُفض مدخلٌ خارج المجال الصوري المجمَّد؛ لا يُحمَل على أقرب حالة."""


class Universality(Enum):
    """مفردة التقسيم الأوّل المغلقة: كلّي أو جزئي، لا ثالث لهما، وس١ تُطرَح دائمًا."""

    KULLI = "كلّي"
    JUZI = "جزئي"


class SubPartition(Enum):
    """محاور التفريع المغلقة؛ `لا_محور_مُثبَت` تصريحٌ لا صمت.

    المحوران الأوّلان يقسمان الكلّي قسمتين مستقلّتين لا قسمةً واحدة على مرحلتين،
    والثالث يقسم الجزئي وحده.
    """

    TAWATU_TASHKIK = "التواطؤ_والتشكيك"
    JINS_ISHTIQAQ = "الجنس_والاشتقاق"
    ALAM_DAMIR = "العلم_والضمير"
    NONE_ATTESTED = "لا_محور_مُثبَت"


class SubOutcome(Enum):
    """مخرَجات التفريع المغلقة؛ `غير_مطروح` تصريحٌ لا صمت."""

    MUTAWATI = "متواطئ"
    MUSHAKKIK = "مشكِّك"
    JINS = "جنس"
    MUSHTAQQ = "مشتق"
    ALAM = "علَم"
    DAMIR = "ضمير"
    NOT_ASKED = "غير_مطروح"


class KulliJuziClass(Enum):
    """التصنيفات الثمانية المغلقة بترتيب المصدر؛ لا تاسع لها في هذا النطاق."""

    KULLI_ALONE = "كلّي"
    KULLI_MUTAWATI = "كلّي_متواطئ"
    KULLI_MUSHAKKIK = "كلّي_مشكِّك"
    KULLI_JINS = "كلّي_جنس"
    KULLI_MUSHTAQQ = "كلّي_مشتق"
    JUZI_ALONE = "جزئي"
    JUZI_ALAM = "جزئي_علَم"
    JUZI_DAMIR = "جزئي_ضمير"


class SharingCarrier(Enum):
    """حامل وقوع الشركة؛ منه تُشتَقّ إجابة س١ ولا تُكتَب اعتباطًا."""

    SHARING_NOT_PRECLUDED = "لا_يمنع_نفس_تصوره_من_وقوع_الشركة"
    SHARING_PRECLUDED = "لم_يشترك_في_معناه_كثيرون"


class SubPartitionCarrier(Enum):
    """حامل التفريع؛ منه يُشتَقّ المحورُ ومخرَجُه معًا ولا يُكتَبان اعتباطًا."""

    EQUAL_IN_INSTANCES = "يستوي_معناه_في_أفراده"
    UNEQUAL_IN_INSTANCES = "يختلف_معناه_في_أفراده"
    UNDETERMINED_ESSENCE = "دلّ_على_ذات_غير_معيّنة"
    DETERMINED_ATTRIBUTE = "دلّ_على_ذي_صفة_معيّنة"
    INDEPENDENT_SIGNIFICATION = "استقلّ_اللفظ_بالدلالة"
    DEPENDENT_SIGNIFICATION = "لم_يستقلّ_اللفظ_بالدلالة"
    NOT_APPLICABLE = "لا_ينطبق"


KULLI_SOURCE: Final = "الشخصية الإسلامية، الجزء الثالث، في تقسيم الاسم إلى كلّي وجزئي"

KULLI_FIRST_QUESTION: Final = "هل يمنع نفسُ تصوّر المعنى من وقوع الشركة فيه؟"

KULLI_SECOND_QUESTION: Final = "أيُّ تفريعٍ مُثبَتٍ لهذا الاسم، وما مخرَجه فيه؟"

KULLI_SECOND_QUESTION_CONDITION: Final = (
    "لا تُطرَح س٢ إلا على محورٍ مُثبَتٍ لهذا الاسم بعينه، ولا يُطرَح محورُ الكلّي "
    "على جزئي ولا محورُ الجزئي على كلّي"
)

KULLI_SUCCESS_TITLE: Final = "شهادة صورية شاملة ناجحة على نطاق محدود"

KULLI_SCOPE_NOTE: Final = (
    "نطاق هذا البرهان شواهد مُثبَتة من مصدر واحد بعينه وثمانية تصنيفات مغلقة؛ "
    "فالكلّيات الخمس الأرسطية، ومراتب التشكيك، وأقسام الضمير، وصلةُ هذا التقسيم "
    "بتقسيم اللفظ باعتبار الدالّ والمدلول خارجه بالتصريح لا بالسهو، لافتقارها "
    "إلى شاهد لكل قيمة يجعل المجال مكتمل الفروع بالبناء"
)

KULLI_AUTHORITY_NOTE: Final = (
    "تصنيف صوري وتوثيق فقط: لا يُنتج ولادةً ولا حكم ولادة، ولا يُجمَّد، ولا "
    "تقرأه أيّ بوّابة في النواة"
)

KULLI_AXIS_INDEPENDENCE_NOTE: Final = (
    "محورا الكلّي — التواطؤ/التشكيك، والجنس/الاشتقاق — قسمتان مستقلّتان للمجموعة "
    "نفسها لا قسمةٌ واحدة على مرحلتين؛ وهذا الشاهد مُثبَتٌ في محوره وحده، ولم "
    "يُثبِت له النصّ موضعًا في المحور الآخر، فجمعُهما في حالةٍ واحدة استنتاجٌ لا "
    "إثبات"
)

JINS_IS_NOT_A_PROVED_SYNONYM_NOTE: Final = (
    "«الجنس» هنا اصطلاحٌ ضمن ثنائية جنس/مشتق تحت الكلّي: اللفظ الدالّ على ذات غير "
    "معيّنة. ولا تُثبِت هذه الشهادة أنه الجنس الأرسطي المنطقي ولا أنه يُطابق ما "
    "يُسمّى في مفرداتٍ أخرى «الجامد»؛ فتلك دعوى مستقلّة لم يُقَم عليها دليلٌ هنا، "
    "ولا تقرأها دالّةٌ في هذه الوحدة"
)

KULLI_NOT_APPLICABLE_TEXT: Final = "لا_ينطبق"

KulliJuziState = tuple[Universality, SubPartition, SubOutcome]

KULLI_ADMISSIBLE_STATES: Final[tuple[KulliJuziState, ...]] = (
    (Universality.KULLI, SubPartition.NONE_ATTESTED, SubOutcome.NOT_ASKED),
    (Universality.KULLI, SubPartition.TAWATU_TASHKIK, SubOutcome.MUTAWATI),
    (Universality.KULLI, SubPartition.TAWATU_TASHKIK, SubOutcome.MUSHAKKIK),
    (Universality.KULLI, SubPartition.JINS_ISHTIQAQ, SubOutcome.JINS),
    (Universality.KULLI, SubPartition.JINS_ISHTIQAQ, SubOutcome.MUSHTAQQ),
    (Universality.JUZI, SubPartition.NONE_ATTESTED, SubOutcome.NOT_ASKED),
    (Universality.JUZI, SubPartition.ALAM_DAMIR, SubOutcome.ALAM),
    (Universality.JUZI, SubPartition.ALAM_DAMIR, SubOutcome.DAMIR),
)

_DECISION: Final[dict[KulliJuziState, KulliJuziClass]] = {
    KULLI_ADMISSIBLE_STATES[0]: KulliJuziClass.KULLI_ALONE,
    KULLI_ADMISSIBLE_STATES[1]: KulliJuziClass.KULLI_MUTAWATI,
    KULLI_ADMISSIBLE_STATES[2]: KulliJuziClass.KULLI_MUSHAKKIK,
    KULLI_ADMISSIBLE_STATES[3]: KulliJuziClass.KULLI_JINS,
    KULLI_ADMISSIBLE_STATES[4]: KulliJuziClass.KULLI_MUSHTAQQ,
    KULLI_ADMISSIBLE_STATES[5]: KulliJuziClass.JUZI_ALONE,
    KULLI_ADMISSIBLE_STATES[6]: KulliJuziClass.JUZI_ALAM,
    KULLI_ADMISSIBLE_STATES[7]: KulliJuziClass.JUZI_DAMIR,
}

_FIRST_ANSWER_BY_CARRIER: Final = {
    SharingCarrier.SHARING_NOT_PRECLUDED: Universality.KULLI,
    SharingCarrier.SHARING_PRECLUDED: Universality.JUZI,
}

_SUB_PARTITION_BY_CARRIER: Final = {
    SubPartitionCarrier.EQUAL_IN_INSTANCES: SubPartition.TAWATU_TASHKIK,
    SubPartitionCarrier.UNEQUAL_IN_INSTANCES: SubPartition.TAWATU_TASHKIK,
    SubPartitionCarrier.UNDETERMINED_ESSENCE: SubPartition.JINS_ISHTIQAQ,
    SubPartitionCarrier.DETERMINED_ATTRIBUTE: SubPartition.JINS_ISHTIQAQ,
    SubPartitionCarrier.INDEPENDENT_SIGNIFICATION: SubPartition.ALAM_DAMIR,
    SubPartitionCarrier.DEPENDENT_SIGNIFICATION: SubPartition.ALAM_DAMIR,
    SubPartitionCarrier.NOT_APPLICABLE: SubPartition.NONE_ATTESTED,
}

_SUB_OUTCOME_BY_CARRIER: Final = {
    SubPartitionCarrier.EQUAL_IN_INSTANCES: SubOutcome.MUTAWATI,
    SubPartitionCarrier.UNEQUAL_IN_INSTANCES: SubOutcome.MUSHAKKIK,
    SubPartitionCarrier.UNDETERMINED_ESSENCE: SubOutcome.JINS,
    SubPartitionCarrier.DETERMINED_ATTRIBUTE: SubOutcome.MUSHTAQQ,
    SubPartitionCarrier.INDEPENDENT_SIGNIFICATION: SubOutcome.ALAM,
    SubPartitionCarrier.DEPENDENT_SIGNIFICATION: SubOutcome.DAMIR,
    SubPartitionCarrier.NOT_APPLICABLE: SubOutcome.NOT_ASKED,
}

_UNIVERSALITY_BY_SUB_PARTITION: Final[dict[SubPartition, Universality | None]] = {
    SubPartition.TAWATU_TASHKIK: Universality.KULLI,
    SubPartition.JINS_ISHTIQAQ: Universality.KULLI,
    SubPartition.ALAM_DAMIR: Universality.JUZI,
    SubPartition.NONE_ATTESTED: None,
}

_KULLI_SUB_PARTITIONS: Final = (
    SubPartition.TAWATU_TASHKIK,
    SubPartition.JINS_ISHTIQAQ,
)

if len(KULLI_ADMISSIBLE_STATES) != len(
    set(KULLI_ADMISSIBLE_STATES)
):  # pragma: no cover - guard
    raise RuntimeError("the admissible states are not eight distinct states")
if set(_DECISION) != set(KULLI_ADMISSIBLE_STATES):  # pragma: no cover - guard
    raise RuntimeError("the decision function does not cover the admissible domain")
if set(_DECISION.values()) != set(KulliJuziClass):  # pragma: no cover - guard
    raise RuntimeError("a declared class has no admissible state")
if len(_FIRST_ANSWER_BY_CARRIER) != len(SharingCarrier):  # pragma: no cover - guard
    raise RuntimeError("a sharing carrier derives no first answer")
if len(_SUB_PARTITION_BY_CARRIER) != len(
    SubPartitionCarrier
):  # pragma: no cover - guard
    raise RuntimeError("a sub-partition carrier derives no axis")
if len(_SUB_OUTCOME_BY_CARRIER) != len(SubPartitionCarrier):  # pragma: no cover - guard
    raise RuntimeError("a sub-partition carrier derives no outcome")
if len(_UNIVERSALITY_BY_SUB_PARTITION) != len(SubPartition):  # pragma: no cover - guard
    raise RuntimeError("a declared axis has no declared universality")
if set(_SUB_OUTCOME_BY_CARRIER.values()) != set(SubOutcome):  # pragma: no cover - guard
    raise RuntimeError("a declared outcome is derived by no carrier")


def _require_universality(value: Universality, field_name: str) -> Universality:
    if not isinstance(value, Universality):
        raise KulliJuziFormalError(f"{field_name} must come from the closed vocabulary")
    return value


def _require_sub_partition(value: SubPartition, field_name: str) -> SubPartition:
    if not isinstance(value, SubPartition):
        raise KulliJuziFormalError(f"{field_name} must come from the closed vocabulary")
    return value


def _require_sub_outcome(value: SubOutcome, field_name: str) -> SubOutcome:
    if not isinstance(value, SubOutcome):
        raise KulliJuziFormalError(f"{field_name} must come from the closed vocabulary")
    return value


@dataclass(frozen=True, slots=True)
class FrozenKulliJuziDomain:
    """المجال الصوري المجمَّد: سؤالاه، وشرط الثاني، وحالاته الثماني، ومصدره."""

    source: str = KULLI_SOURCE
    first_question: str = KULLI_FIRST_QUESTION
    second_question: str = KULLI_SECOND_QUESTION
    second_question_condition: str = KULLI_SECOND_QUESTION_CONDITION
    axis_independence_note: str = KULLI_AXIS_INDEPENDENCE_NOTE
    admissible_states: tuple[KulliJuziState, ...] = KULLI_ADMISSIBLE_STATES

    def __post_init__(self) -> None:
        for name in (
            "source",
            "first_question",
            "second_question",
            "second_question_condition",
            "axis_independence_note",
        ):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise KulliJuziFormalError(f"{name} must be non-blank text")
        if set(self.admissible_states) != set(KULLI_ADMISSIBLE_STATES):
            raise KulliJuziFormalError(
                "the frozen formal domain is exactly the eight admissible states"
            )

    @property
    def cardinality(self) -> int:
        """عدد الحالات المقبولة في المجال: ثمانٍ بالضبط."""

        return len(self.admissible_states)

    @property
    def kulli_sub_partitions(self) -> tuple[SubPartition, ...]:
        """محورا الكلّي المستقلّان، مشتقّين من جدول المحاور لا مكتوبَين."""

        return tuple(
            partition
            for partition, universality in _UNIVERSALITY_BY_SUB_PARTITION.items()
            if universality is Universality.KULLI
        )


FROZEN_KULLI_JUZI_DOMAIN: Final = FrozenKulliJuziDomain()

if FROZEN_KULLI_JUZI_DOMAIN.kulli_sub_partitions != _KULLI_SUB_PARTITIONS:
    raise RuntimeError(  # pragma: no cover - guard
        "the kulli axes derived from the axis table are not the declared two"
    )


def canonical_universality(value: str) -> Universality:
    """أعِد قسم التقسيم الأوّل المسمّى في `value`؛ وأيّ لفظ آخر يُرَدّ ولا يُقرَّب."""

    if not isinstance(value, str) or not value.strip():
        raise KulliJuziFormalError("التقسيم الأوّل must be non-blank text")
    key = comparison_key(value)
    for universality in Universality:
        if comparison_key(universality.value) == key:
            return universality
    raise KulliJuziFormalError(
        "التقسيم الأوّل must be one of: "
        + "، ".join(universality.value for universality in Universality)
    )


def canonical_sub_partition(value: str) -> SubPartition:
    """أعِد المحور المسمّى في `value`؛ وأيّ لفظ آخر يُرَدّ ولا يُقرَّب."""

    if not isinstance(value, str) or not value.strip():
        raise KulliJuziFormalError("المحور must be non-blank text")
    key = comparison_key(value)
    for partition in SubPartition:
        if comparison_key(partition.value) == key:
            return partition
    raise KulliJuziFormalError(
        "المحور must be one of: "
        + "، ".join(partition.value for partition in SubPartition)
    )


def canonical_sub_outcome(value: str) -> SubOutcome:
    """أعِد مخرَج التفريع المسمّى في `value`؛ وأيّ لفظ آخر يُرَدّ ولا يُقرَّب."""

    if not isinstance(value, str) or not value.strip():
        raise KulliJuziFormalError("مخرَج التفريع must be non-blank text")
    key = comparison_key(value)
    for outcome in SubOutcome:
        if comparison_key(outcome.value) == key:
            return outcome
    raise KulliJuziFormalError(
        "مخرَج التفريع must be one of: "
        + "، ".join(outcome.value for outcome in SubOutcome)
    )


def universality_of_sub_partition(partition: SubPartition) -> Universality | None:
    """القسمُ الذي يتفرّع عنه هذا المحور، و`None` حين لا محور مُثبَت أصلًا."""

    return _UNIVERSALITY_BY_SUB_PARTITION[_require_sub_partition(partition, "المحور")]


def is_sub_partition_askable(
    universality: Universality, partition: SubPartition
) -> bool:
    """أيُسأل هذا المحورُ عن هذا القسم؟ لا يُسأل محورُ قسمٍ عن قسمٍ آخر."""

    _require_universality(universality, "س١")
    owner = universality_of_sub_partition(partition)
    return owner is None or owner is universality


def classify_kulli_juzi(
    universality: Universality,
    partition: SubPartition,
    outcome: SubOutcome,
) -> KulliJuziClass:
    """التصنيف المشتقّ من الحالة اشتقاقًا مباشرًا، بلا تخمين ولا فرع افتراضي.

    كلّي بلا محورٍ مُثبَت → `كلّي`، وجزئي بلا محورٍ مُثبَت → `جزئي`. وكلٌّ من
    محورَي الكلّي ومحورِ الجزئي يُنتج مخرَجَيه المُثبَتَين لا غير. وأيّ حالة خارج
    الثماني — ومنها محورُ كلّيٍّ نُسب إلى جزئي، أو محورٌ مُصرَّحٌ به بلا مخرَج، أو
    مخرَجٌ بلا محور، أو مخرَجٌ لا يَنتمي إلى محوره — تُرَدّ بخطأ ولا تُصنَّف.
    """

    state: KulliJuziState = (
        _require_universality(universality, "س١"),
        _require_sub_partition(partition, "المحور"),
        _require_sub_outcome(outcome, "مخرَج التفريع"),
    )
    if not is_sub_partition_askable(state[0], state[1]):
        raise KulliJuziFormalError(KULLI_SECOND_QUESTION_CONDITION)
    partition_asked = state[1] is not SubPartition.NONE_ATTESTED
    outcome_given = state[2] is not SubOutcome.NOT_ASKED
    if partition_asked != outcome_given:
        raise KulliJuziFormalError(
            "المحور المُصرَّح به يلزمه مخرَجٌ مُصرَّح، ولا مخرَج بلا محور"
        )
    classification = _DECISION.get(state)
    if classification is None:
        raise KulliJuziFormalError("حالة خارج المجال الصوري المجمَّد")
    return classification


@dataclass(frozen=True, slots=True)
class AttestedNameWitness:
    """اسمٌ مُثبَت نصًّا في محورٍ واحدٍ بعينه: حواملُه وأدلّته وتصنيفه المنصوص."""

    lexeme: str
    first_answer: Universality
    first_evidence: str
    declared_sub_partition: SubPartition
    sub_outcome: SubOutcome
    sub_evidence: str
    sharing_carrier: SharingCarrier
    sub_partition_carrier: SubPartitionCarrier
    axis_independence_note: str
    attested_class: KulliJuziClass
    source: str

    def __post_init__(self) -> None:
        for name in (
            "lexeme",
            "first_evidence",
            "sub_evidence",
            "axis_independence_note",
            "source",
        ):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise KulliJuziFormalError(f"{name} must be non-blank text")
        _require_universality(self.first_answer, "س١")
        _require_sub_partition(self.declared_sub_partition, "المحور")
        _require_sub_outcome(self.sub_outcome, "مخرَج التفريع")
        if not isinstance(self.sharing_carrier, SharingCarrier):
            raise KulliJuziFormalError(
                "حامل وقوع الشركة must come from the closed vocabulary"
            )
        if not isinstance(self.sub_partition_carrier, SubPartitionCarrier):
            raise KulliJuziFormalError(
                "حامل التفريع must come from the closed vocabulary"
            )
        if not isinstance(self.attested_class, KulliJuziClass):
            raise KulliJuziFormalError(
                "التصنيف المنصوص must come from the closed vocabulary"
            )
        if self.first_answer is not _FIRST_ANSWER_BY_CARRIER[self.sharing_carrier]:
            raise KulliJuziFormalError(
                "إجابة س١ تُشتَقّ من حامل وقوع الشركة ولا تُكتَب اعتباطًا"
            )
        if (
            self.declared_sub_partition
            is not _SUB_PARTITION_BY_CARRIER[self.sub_partition_carrier]
        ):
            raise KulliJuziFormalError(
                "المحور المُصرَّح به يُشتَقّ من حامل التفريع ولا يُكتَب اعتباطًا"
            )
        if self.sub_outcome is not _SUB_OUTCOME_BY_CARRIER[self.sub_partition_carrier]:
            raise KulliJuziFormalError(
                "مخرَج التفريع يُشتَقّ من حامل التفريع ولا يُكتَب اعتباطًا"
            )
        declared_note_key = comparison_key(self.axis_independence_note)
        not_applicable_key = comparison_key(KULLI_NOT_APPLICABLE_TEXT)
        on_kulli_axis = self.declared_sub_partition in _KULLI_SUB_PARTITIONS
        if on_kulli_axis and declared_note_key == not_applicable_key:
            raise KulliJuziFormalError(
                "شاهدُ محورٍ كلّيٍّ يلزمه تصريحٌ باستقلال المحورين، فلا يُقرأ "
                "إثباتُه في محورٍ إثباتًا في المحور الآخر"
            )
        if not on_kulli_axis and declared_note_key != not_applicable_key:
            raise KulliJuziFormalError(
                f"ملاحظة استقلال المحورين تُصرَّح على شواهد محورَي الكلّي وحدها، "
                f"وعلى ما عداها تكون {KULLI_NOT_APPLICABLE_TEXT}"
            )

    @property
    def witness_key(self) -> tuple[str, SubPartition]:
        """هوية الشاهد: لفظُه مع محوره المُختبَر، لا اللفظ المجرَّد وحده."""

        return (comparison_key(self.lexeme), self.declared_sub_partition)

    @property
    def derived_class(self) -> KulliJuziClass:
        """التصنيف المشتقّ من الدالة الصورية وحدها، لا من التصنيف المنصوص."""

        return classify_kulli_juzi(
            self.first_answer,
            self.declared_sub_partition,
            self.sub_outcome,
        )


_SHAKHSIYYA: Final = KULLI_SOURCE

_KULLI_FIRST_EVIDENCE: Final = (
    "فالكلي هو الذي لا يمنع نفس تصوره من وقوع الشركة فيه، سواء وقعت الشركة "
    "كالحيوان والإنسان والكاتب"
)

_JUZI_FIRST_EVIDENCE: Final = (
    "وأما الجزئي فهو الذي لم يشترك في معناه كثيرون، مثل زيد علماً على رجل، "
    "ومثل الضمائر كهو وهي"
)

ATTESTED_NAME_WITNESSES: Final = (
    AttestedNameWitness(
        lexeme="الحيوان",
        first_answer=Universality.KULLI,
        first_evidence=_KULLI_FIRST_EVIDENCE,
        declared_sub_partition=SubPartition.NONE_ATTESTED,
        sub_outcome=SubOutcome.NOT_ASKED,
        sub_evidence=(
            "لم يُثبِت له النصّ في هذا الموضع محورًا من محورَي الكلّي، فلم يُسأل "
            "عن مخرَجٍ فيهما"
        ),
        sharing_carrier=SharingCarrier.SHARING_NOT_PRECLUDED,
        sub_partition_carrier=SubPartitionCarrier.NOT_APPLICABLE,
        axis_independence_note=KULLI_NOT_APPLICABLE_TEXT,
        attested_class=KulliJuziClass.KULLI_ALONE,
        source=_SHAKHSIYYA,
    ),
    AttestedNameWitness(
        lexeme="الكاتب",
        first_answer=Universality.KULLI,
        first_evidence=_KULLI_FIRST_EVIDENCE,
        declared_sub_partition=SubPartition.NONE_ATTESTED,
        sub_outcome=SubOutcome.NOT_ASKED,
        sub_evidence=(
            "لم يُثبِت له النصّ في هذا الموضع محورًا من محورَي الكلّي، فلم يُسأل "
            "عن مخرَجٍ فيهما"
        ),
        sharing_carrier=SharingCarrier.SHARING_NOT_PRECLUDED,
        sub_partition_carrier=SubPartitionCarrier.NOT_APPLICABLE,
        axis_independence_note=KULLI_NOT_APPLICABLE_TEXT,
        attested_class=KulliJuziClass.KULLI_ALONE,
        source=_SHAKHSIYYA,
    ),
    AttestedNameWitness(
        lexeme="الإنسان",
        first_answer=Universality.KULLI,
        first_evidence=_KULLI_FIRST_EVIDENCE,
        declared_sub_partition=SubPartition.TAWATU_TASHKIK,
        sub_outcome=SubOutcome.MUTAWATI,
        sub_evidence="المتواطئ يستوي معناه في أفراده، مثل الإنسان والفرس",
        sharing_carrier=SharingCarrier.SHARING_NOT_PRECLUDED,
        sub_partition_carrier=SubPartitionCarrier.EQUAL_IN_INSTANCES,
        axis_independence_note=KULLI_AXIS_INDEPENDENCE_NOTE,
        attested_class=KulliJuziClass.KULLI_MUTAWATI,
        source=_SHAKHSIYYA,
    ),
    AttestedNameWitness(
        lexeme="الوجود",
        first_answer=Universality.KULLI,
        first_evidence=_KULLI_FIRST_EVIDENCE,
        declared_sub_partition=SubPartition.TAWATU_TASHKIK,
        sub_outcome=SubOutcome.MUSHAKKIK,
        sub_evidence=(
            "المشكِّك يختلف معناه في أفراده بالوجوب والإمكان، أو الاستغناء "
            "والافتقار، أو الزيادة والنقصان، مثل الوجود والنور"
        ),
        sharing_carrier=SharingCarrier.SHARING_NOT_PRECLUDED,
        sub_partition_carrier=SubPartitionCarrier.UNEQUAL_IN_INSTANCES,
        axis_independence_note=KULLI_AXIS_INDEPENDENCE_NOTE,
        attested_class=KulliJuziClass.KULLI_MUSHAKKIK,
        source=_SHAKHSIYYA,
    ),
    AttestedNameWitness(
        lexeme="السواد",
        first_answer=Universality.KULLI,
        first_evidence=_KULLI_FIRST_EVIDENCE,
        declared_sub_partition=SubPartition.JINS_ISHTIQAQ,
        sub_outcome=SubOutcome.JINS,
        sub_evidence=(
            "والكلي أيضاً نوعان: جنس ومشتق؛ وذلك لأنه إن دل على ذات غير معينة، "
            "كالفرس والإنسان والسواد... فهو الجنس"
        ),
        sharing_carrier=SharingCarrier.SHARING_NOT_PRECLUDED,
        sub_partition_carrier=SubPartitionCarrier.UNDETERMINED_ESSENCE,
        axis_independence_note=KULLI_AXIS_INDEPENDENCE_NOTE,
        attested_class=KulliJuziClass.KULLI_JINS,
        source=_SHAKHSIYYA,
    ),
    AttestedNameWitness(
        lexeme="الأسود",
        first_answer=Universality.KULLI,
        first_evidence=_KULLI_FIRST_EVIDENCE,
        declared_sub_partition=SubPartition.JINS_ISHTIQAQ,
        sub_outcome=SubOutcome.MUSHTAQQ,
        sub_evidence=(
            "وإن دل الكلي على ذي صفة معينة فهو المشتق، كالأسود والفارس ونحوهما"
        ),
        sharing_carrier=SharingCarrier.SHARING_NOT_PRECLUDED,
        sub_partition_carrier=SubPartitionCarrier.DETERMINED_ATTRIBUTE,
        axis_independence_note=KULLI_AXIS_INDEPENDENCE_NOTE,
        attested_class=KulliJuziClass.KULLI_MUSHTAQQ,
        source=_SHAKHSIYYA,
    ),
    AttestedNameWitness(
        lexeme="زيد",
        first_answer=Universality.JUZI,
        first_evidence=_JUZI_FIRST_EVIDENCE,
        declared_sub_partition=SubPartition.NONE_ATTESTED,
        sub_outcome=SubOutcome.NOT_ASKED,
        sub_evidence=(
            "مضروبٌ مثلًا للجزئي نفسه في موضع التقسيم الأوّل، قبل تفريع الجزئي "
            "إلى علم وضمير"
        ),
        sharing_carrier=SharingCarrier.SHARING_PRECLUDED,
        sub_partition_carrier=SubPartitionCarrier.NOT_APPLICABLE,
        axis_independence_note=KULLI_NOT_APPLICABLE_TEXT,
        attested_class=KulliJuziClass.JUZI_ALONE,
        source=_SHAKHSIYYA,
    ),
    AttestedNameWitness(
        lexeme="عبد الله",
        first_answer=Universality.JUZI,
        first_evidence=_JUZI_FIRST_EVIDENCE,
        declared_sub_partition=SubPartition.ALAM_DAMIR,
        sub_outcome=SubOutcome.ALAM,
        sub_evidence=("فإن استقل اللفظ بالدلالة... فهو العلم، كزيد وكعبد الله"),
        sharing_carrier=SharingCarrier.SHARING_PRECLUDED,
        sub_partition_carrier=SubPartitionCarrier.INDEPENDENT_SIGNIFICATION,
        axis_independence_note=KULLI_NOT_APPLICABLE_TEXT,
        attested_class=KulliJuziClass.JUZI_ALAM,
        source=_SHAKHSIYYA,
    ),
    AttestedNameWitness(
        lexeme="هو",
        first_answer=Universality.JUZI,
        first_evidence=_JUZI_FIRST_EVIDENCE,
        declared_sub_partition=SubPartition.ALAM_DAMIR,
        sub_outcome=SubOutcome.DAMIR,
        sub_evidence="وإن لم يستقل... فهو المضمر، مثل هو وهي",
        sharing_carrier=SharingCarrier.SHARING_PRECLUDED,
        sub_partition_carrier=SubPartitionCarrier.DEPENDENT_SIGNIFICATION,
        axis_independence_note=KULLI_NOT_APPLICABLE_TEXT,
        attested_class=KulliJuziClass.JUZI_DAMIR,
        source=_SHAKHSIYYA,
    ),
)

if len({witness.witness_key for witness in ATTESTED_NAME_WITNESSES}) != len(
    ATTESTED_NAME_WITNESSES
):  # pragma: no cover - guard
    raise RuntimeError("two attested witnesses carry the same identity")
if {witness.attested_class for witness in ATTESTED_NAME_WITNESSES} != set(
    KulliJuziClass
):  # pragma: no cover - guard
    raise RuntimeError("the attested corpus does not cover every declared class")


@dataclass(frozen=True, slots=True)
class KulliJuziProofRow:
    """صفّ برهانٍ واحد: اسمٌ بمحوره ومخرَجه، وتصنيفه المشتقّ مقابل المنصوص."""

    lexeme: str
    first_answer: Universality
    declared_sub_partition: SubPartition
    sub_outcome: SubOutcome
    derived_class: KulliJuziClass
    attested_class: KulliJuziClass

    @property
    def matches(self) -> bool:
        return self.derived_class is self.attested_class


@dataclass(frozen=True, slots=True)
class KulliJuziProofReport:
    """تقرير البرهان الشامل: صفٌّ لكل شاهد، بلا توقّف عند أول فشل."""

    rows: tuple[KulliJuziProofRow, ...]
    domain: FrozenKulliJuziDomain
    source: str

    @property
    def is_complete_success(self) -> bool:
        """هل صُنِّف كل شاهد بلا استثناء واحد ولا حالة غموض؟"""

        return bool(self.rows) and all(row.matches for row in self.rows)

    @property
    def unmatched(self) -> tuple[KulliJuziProofRow, ...]:
        """الصفوف التي خالف فيها المشتقّ المنصوص؛ تُبلَّغ ولا تُرمَّم."""

        return tuple(row for row in self.rows if not row.matches)

    @property
    def title(self) -> str | None:
        """التسمية الدقيقة عند النجاح التامّ وحده، و`None` عند غيره."""

        return KULLI_SUCCESS_TITLE if self.is_complete_success else None


def prove_kulli_juzi_over_attested_corpus(
    witnesses: tuple[AttestedNameWitness, ...] = ATTESTED_NAME_WITNESSES,
) -> KulliJuziProofReport:
    """برهِن على كل شاهد من الشواهد بالدالة الصورية وحدها، تغطيةً شاملة.

    لا يُقرأ `attested_class` إلا للمقارنة بعد الاشتقاق، ولا يُستعمل في
    الاشتقاق نفسه. وعند عدم التطابق يُسجَّل الصفّ في `unmatched` كما هو: لا
    تُعدَّل الدالة الصورية ولا الشواهد لإخفاء الفشل.
    """

    if not witnesses:
        raise KulliJuziFormalError("البرهان الشامل لا يكون على مجموعة فارغة")
    rows = []
    for witness in witnesses:
        if not isinstance(witness, AttestedNameWitness):
            raise KulliJuziFormalError("البرهان يجري على شواهد مُثبَتة فقط")
        rows.append(
            KulliJuziProofRow(
                lexeme=witness.lexeme,
                first_answer=witness.first_answer,
                declared_sub_partition=witness.declared_sub_partition,
                sub_outcome=witness.sub_outcome,
                derived_class=witness.derived_class,
                attested_class=witness.attested_class,
            )
        )
    return KulliJuziProofReport(
        rows=tuple(rows), domain=FROZEN_KULLI_JUZI_DOMAIN, source=KULLI_SOURCE
    )
