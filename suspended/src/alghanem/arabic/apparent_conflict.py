"""مفردة مغلقة لأسباب التعارض **الظاهر** بين شاهدين، مصدرها أصولي نصّي.

هذه الوحدة **مستقلّة** عن `comprehension_defect` ولا تُدمَج فيها، كما فُصِل
`mantuq_mafhum_ifada` عن أخواته: تلك تُشخِّص غموض **لفظٍ مفرد** في نصٍّ ثابت،
وهذه تُشخِّص **دعوى تعارضٍ بين شاهدين**. والموضوعان متغايران، فدمجُهما في
مفردةٍ واحدة يُسقِط الفارق::

    ApparentConflict  != RealContradiction
    الاشتباه           != الاشتراك

**القاعدة الحاكمة: الأصل عدم التعارض.** مجرّد ظهور التشابه بين نصّين لا يُنشئ
تناقضًا؛ فالأصل فيهما **الاختلاف** — أي أنهما يُعالِجان حالتين متغايرتين حتى
يُثبَت خلاف ذلك. والتعارض **دعوى تحتاج إثباتًا**، لا حالةً افتراضية تُقبَل
بمجرّد التشابه (`DEFAULT_IS_DIFFERENCE_NOT_CONTRADICTION_NOTE`).

**والأسباب المُنتِجة لوهم التعارض ثلاثة مُسمّاة، ولا رابع في هذه الطبقة**:

* `التعميم` — معاملة حكمٍ خاصٍّ بحادثةٍ معيّنة كأنه عامٌّ لكل ما يُشبهها.
* `التجريد` — تجريد الحادثة من ظروفها الخاصّة قبل المقارنة.
* `الاشتباه` — تشابهٌ سطحيّ بين حادثتين مختلفتين في جوهرهما.

**ولا ترتيب أولوية بينها**، وهذه سلبيةٌ مُسجَّلة لا مسكوتٌ عنها: الثلاثة
أجناسٌ متغايرة لا درجاتٌ في شدّةٍ واحدة، فلا تُستنسخ هنا دالّة
`defect_priority` ولا رتبةٌ ولا مقارنة
(`NO_PRIORITY_AMONG_APPARENT_CONFLICT_CAUSES_NOTE`).

**والعلاج المنهجي ثلاثيٌّ مربوطٌ بكل سبب**: إفراد كل حادثة عن الأخرى، وربط
العلاج بالحادثة نفسها، وربط الحادثة بظروفها — أي **إعادة كل نصٍّ إلى سياقه
الكامل قبل أي مقارنة**، لا مقارنة الأحكام المجرَّدة.

**وحدود النطاق مُصرَّحٌ بها لا معتذَرٌ عنها لاحقًا**: هذه المفردة تُشخِّص دعوى
تعارضٍ بين شاهدين أو قراءتين، ولا تُشخِّص غموض لفظٍ مفرد (ذاك اختصاص الخمسة في
`comprehension_defect`)، ولا تمسّ ثبوت النصّ ولا قوّة نقله. ولهذا كانت
`لا_ينطبق` قيمةً مصرَّحًا بها في المفردة لا صمتًا: التصريح بعدم الانطباق
تصنيفٌ صادق.

**والمصدر شهادةٌ لا قياس**: نصّ الأسباب الثلاثة وعلاجها منقولٌ بوصفه شهادةً
مُسمّاة، ولا تُعاد هنا قراءةُ مدوَّنةٍ ولا اشتقاقُ بصمةِ ملفّ، على نفس الفارق
الذي يُقرِّره `docs/reference/arabic_identity_confusion_catalog.md` بين القياس
والشهادة (`SOURCE_IS_TESTIMONY_NOT_MEASUREMENT_NOTE`).

سلطويًّا: هذا توثيق وتصنيف فقط. لا يقرأ هذا التصنيف أيُّ بوّابة نواة، ولا
يدخل في بناء `BirthExperimentSpecification`، ولا يغيّر `نتيجة_التدقيق_الخارجي`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from .comprehension_defect import CLOSED_VOCABULARY as _DEFECT_VOCABULARY
from .text_key import comparison_key


class ApparentConflictError(ValueError):
    """رُفض تصنيفٌ خارج المفردة المغلقة لأسباب التعارض الظاهر."""


class ApparentConflictCause(Enum):
    """المفردة الثلاثية المغلقة؛ لا رابع لها في هذه الطبقة."""

    TAMIM = "التعميم"
    TAJRID = "التجريد"
    ISHTIBAH = "الاشتباه"


NOT_APPLICABLE: Final = "لا_ينطبق"

CLOSED_VOCABULARY: Final = tuple(cause.value for cause in ApparentConflictCause)

DECLARABLE_VALUES: Final = CLOSED_VOCABULARY + (NOT_APPLICABLE,)

SOURCE: Final = (
    "باب التعارض والترجيح في أصول الفقه، في أن الأصل عدم التعارض وأن التعارض "
    "الظاهر يرجع إلى التعميم أو التجريد أو الاشتباه"
)

DEFAULT_IS_DIFFERENCE_NOT_CONTRADICTION_NOTE: Final = (
    "DefaultIsDifferenceNotContradiction: مجرّد ظهور التشابه بين نصّين لا "
    "يُنشئ تناقضًا، والأصل فيهما الاختلاف؛ فالتعارض دعوى تحتاج إثباتًا لا "
    "حالة افتراضية"
)
NO_PRIORITY_AMONG_APPARENT_CONFLICT_CAUSES_NOTE: Final = (
    "NoPriorityAmongApparentConflictCauses: أسباب التعارض الظاهر أجناسٌ "
    "متغايرة لا درجاتٌ في شدّةٍ واحدة، فلا رتبة بينها ولا مقارنة ولا ترتيب "
    "أولوية؛ وهذه سلبيةٌ مُسجَّلة لا مسكوتٌ عنها"
)
ISHTIBAH_IS_NOT_ISHTIRAK_NOTE: Final = (
    "IshtibahIsNotIshtirak: الاشتباه تشابهٌ سطحيّ بين حادثتين مختلفتين في "
    "جوهرهما، والاشتراك تعدّدُ وضعٍ في لفظٍ واحد؛ فهما موضوعان متغايران وإن "
    "تقاربت عبارتهما، ولا يُحمل أحدهما على الآخر"
)
SOURCE_IS_TESTIMONY_NOT_MEASUREMENT_NOTE: Final = (
    "SourceIsTestimonyNotMeasurement: الأسباب الثلاثة وعلاجها منقولةٌ عن "
    "مصدرٍ مُسمّى بوصفها شهادةً، ولا تُقرأ هنا مدوَّنةٌ ولا تُعاد بصمةُ ملفّ"
)
SCOPE_NOTE: Final = (
    "أسباب التعارض الظاهر الثلاثة تُشخِّص دعوى تعارضٍ بين شاهدين، لا غموض "
    "لفظٍ مفرد ولا ثبوت النصّ ولا قوّة نقله؛ فعدم انطباقها على منافسٍ ما "
    "نتيجة بنيوية متوقَّعة، لا نقص في التصنيف"
)

REMEDY_STEPS: Final = (
    "إفراد كل حادثة عن الأخرى",
    "ربط العلاج بالحادثة نفسها",
    "ربط الحادثة بظروفها",
)

REMEDY_PRINCIPLE: Final = (
    "إعادة كل نصٍّ إلى سياقه الكامل قبل أي مقارنة، لا مقارنة الأحكام المجرَّدة"
)


@dataclass(frozen=True, slots=True)
class ApparentConflictDiagnosis:
    """سببٌ واحد بتعريفه وعلاجه ومصدره؛ لا رتبةَ فيه ولا حكم."""

    cause: ApparentConflictCause
    definition: str
    remedy: str
    source: str


_DIAGNOSES: Final = (
    ApparentConflictDiagnosis(
        cause=ApparentConflictCause.TAMIM,
        definition=(
            "معاملة حكمٍ خاصٍّ بحادثةٍ معيّنة كأنه عامٌّ لكل ما يُشبهها في "
            "الجنس، فيُصطدم به ما وقع في حادثةٍ أخرى"
        ),
        remedy=REMEDY_STEPS[0],
        source=SOURCE,
    ),
    ApparentConflictDiagnosis(
        cause=ApparentConflictCause.TAJRID,
        definition=(
            "تجريد الحادثة من ظروفها الخاصّة قبل المقارنة، فتُقارَن أحكامٌ "
            "مجرَّدة لا حوادثُ بسياقها"
        ),
        remedy=REMEDY_STEPS[2],
        source=SOURCE,
    ),
    ApparentConflictDiagnosis(
        cause=ApparentConflictCause.ISHTIBAH,
        definition=(
            "تشابهٌ سطحيّ بين حادثتين مختلفتين فعلًا في جوهرهما، فيُظَنّ " "اتحادُ موضوعهما"
        ),
        remedy=REMEDY_STEPS[1],
        source=SOURCE,
    ),
)

DIAGNOSES: Final = _DIAGNOSES

_DIAGNOSIS_BY_CAUSE: Final = {item.cause: item for item in _DIAGNOSES}

_CAUSE_BY_KEY: Final = {
    comparison_key(cause.value): cause for cause in ApparentConflictCause
}
_NOT_APPLICABLE_KEY: Final = comparison_key(NOT_APPLICABLE)
_DEFECT_KEYS: Final = frozenset(comparison_key(value) for value in _DEFECT_VOCABULARY)

if len(_CAUSE_BY_KEY) != len(ApparentConflictCause):  # pragma: no cover - guard
    raise RuntimeError("two apparent-conflict causes collapse onto one comparison key")
if _NOT_APPLICABLE_KEY in _CAUSE_BY_KEY:  # pragma: no cover - guard
    raise RuntimeError("لا_ينطبق collides with a declared apparent-conflict cause")
if _DEFECT_KEYS & set(_CAUSE_BY_KEY):  # pragma: no cover - guard
    raise RuntimeError(ISHTIBAH_IS_NOT_ISHTIRAK_NOTE)
if len(_DIAGNOSIS_BY_CAUSE) != len(ApparentConflictCause):  # pragma: no cover - guard
    raise RuntimeError("a declared cause carries no diagnosis")


def canonical_apparent_conflict_classification(
    value: str,
) -> ApparentConflictCause | None:
    """أعِد السبب المسمَّى في `value`، أو `None` إن صُرِّح بـ`لا_ينطبق`.

    `None` هنا معناها التصريح بعدم الانطباق، لا الصمت ولا الغياب: الحقل نفسه
    اختياري، أمّا إذا ذُكِر فلا يُقبل فيه إلا أحد الثلاثة أو `لا_ينطبق`. وأيّ
    لفظ آخر — تصحيفًا كان أو اصطلاحًا مُخترَعًا — يُرَدّ ولا يُحمل على أقرب
    الثلاثة، ولا يُحمل على أحد الخمسة في `comprehension_defect`.
    """

    if not isinstance(value, str) or not value.strip():
        raise ApparentConflictError("سبب_التعارض_الظاهر must be non-blank text")
    key = comparison_key(value)
    if key == _NOT_APPLICABLE_KEY:
        return None
    cause = _CAUSE_BY_KEY.get(key)
    if cause is None:
        raise ApparentConflictError(
            "سبب_التعارض_الظاهر must be one of: " + "، ".join(DECLARABLE_VALUES)
        )
    return cause


def apparent_conflict_diagnosis(
    cause: ApparentConflictCause,
) -> ApparentConflictDiagnosis:
    """تعريفُ السبب وعلاجه ومصدره، منقولةً لا مقدَّرة."""

    if not isinstance(cause, ApparentConflictCause):
        raise ApparentConflictError(
            "apparent-conflict diagnosis requires a closed-vocabulary cause"
        )
    return _DIAGNOSIS_BY_CAUSE[cause]
