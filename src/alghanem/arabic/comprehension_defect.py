"""مفردة مغلقة لأسباب الإخلال بالفهم، مصدرها أصولي نصّي.

`ComprehensionDefectCause` هي المفردة الخماسية المغلقة التي عدّها الأصوليون
"الأمور المخلّة بفهم المراد" من اللفظ: الاشتراك، والنقل، والمجاز، والإضمار،
والتخصيص. ومعها ترتيب أولوية صريح عند التعارض:

    تخصيص > مجاز = إضمار > نقل > اشتراك

بمعنى: التخصيص أهون الخمسة إخلالًا وأولاها بالحمل عند التعارض، والاشتراك
أشدّها. وكل مقارنة في هذا الترتيب مصحوبة بحجّتها النصّية الكاملة في
`PRIORITY_ARGUMENTS`، فلا يبقى في الترتيب موضع تقدير غير مُعلَّل.

**والترتيب يستلزم استنفادًا لا مجرّد رتبة**: إعلانُ سببٍ متأخّرٍ في الترتيب
ادّعاءٌ ضمنيّ بأن كل ما هو أولى منه بالحمل قد استُبعِد بدليل. فتصنيفُ لفظٍ
بـ`اشتراك` — وهو آخر الخمسة رتبةً — سابقٌ لأوانه منهجيًّا ما لم تُستبعَد
الأربعة الأولى منه صراحةً، ولو صادف الصواب تاريخيًّا
(`EXHAUSTION_PRECEDES_CLASSIFICATION_NOTE`). والاستنفاد هنا **يُبلَّغ ولا
يَحكُم**، وهذا فارقٌ مُسمّى لا تطابقٌ مُدّعى مع
`NoBirthBeforeLicensedWeakerExhaustion` في G0: هناك استنفادٌ يُغلِق بوّابةً
ويمنع ولادة، وهنا حالةٌ تقريرية تُظهِر نقص الاستدلال بدل أن يمرّ صامتًا
(`REPORTED_EXHAUSTION_IS_NOT_A_GATE_NOTE`).

نطاق الإطار وحدوده — تسجيل صريح، لا اعتذار لاحق:

* هذا الإطار يعالج تحديدًا **غموض الدلالة في نصّ ثابت**: لفظٌ ثبت نصُّه ثم
  اختُلف في المراد منه.
* ولا يعالج **تعدّد القراءات** نفسه: اختلاف الرواة في اللفظ المقروء ليس أحد
  الخمسة، لأنه اختلاف في النصّ لا في فهم نصّ واحد.
* ولا يعالج **ضعف النقل**: ردُّ قراءةٍ لكونها آحادًا لا تواترًا حكمٌ على
  ثبوت النصّ لا على دلالته.

فانطباق الإطار انطباقًا **جزئيًّا** على بطاقة نزاعُها نزاع قراءات وإعراب
(كبطاقة هذان) نتيجة **بنيوية متوقَّعة**، لا نقص في التنفيذ. ولهذا كانت
`لا_ينطبق` قيمةً مصرَّحًا بها في المفردة، لا قيمة افتراضية صامتة: التصريح
بعدم الانطباق تصنيفٌ صادق، وإلزام منافسٍ بتصنيف لا يستحقّه تزوير.

سلطويًّا: هذا توثيق وتصنيف فقط. لا يقرأ هذا التصنيف أيُّ بوّابة نواة، ولا
يحرّك `IndependentClosureGate` ولا `BirthVerdictGate` نحو أي نتيجة، ولا يدخل
في بناء `BirthExperimentSpecification`، ولا يغيّر نتيجة التدقيق الخارجي.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Any, Final

from .text_key import comparison_key


class ComprehensionDefectError(ValueError):
    """رُفض تصنيفٌ خارج المفردة المغلقة لأسباب الإخلال بالفهم."""


class ComprehensionDefectCause(Enum):
    """المفردة الخماسية المغلقة؛ لا سادس لها في هذه الطبقة."""

    ISHTIRAK = "اشتراك"
    NAQL = "نقل"
    MAJAZ = "مجاز"
    IDMAR = "إضمار"
    TAKHSIS = "تخصيص"


NOT_APPLICABLE: Final = "لا_ينطبق"

CLOSED_VOCABULARY: Final = tuple(cause.value for cause in ComprehensionDefectCause)

DECLARABLE_VALUES: Final = CLOSED_VOCABULARY + (NOT_APPLICABLE,)

SCOPE_NOTE: Final = (
    "أسباب الإخلال بالفهم الخمسة تعالج غموض الدلالة في نصّ ثابت، لا تعدّد "
    "القراءات ولا ضعف النقل؛ فعدم انطباقها على منافسٍ ما نتيجة بنيوية "
    "متوقَّعة، لا نقص في التصنيف"
)

_PRIORITY_RANK: Final = {
    ComprehensionDefectCause.TAKHSIS: 1,
    ComprehensionDefectCause.MAJAZ: 2,
    ComprehensionDefectCause.IDMAR: 2,
    ComprehensionDefectCause.NAQL: 3,
    ComprehensionDefectCause.ISHTIRAK: 4,
}


@dataclass(frozen=True, slots=True)
class PriorityArgument:
    """حجّة مقارنة واحدة بين سببين، منقولةً لا مقدَّرة."""

    first: ComprehensionDefectCause
    second: ComprehensionDefectCause
    verdict: str
    argument: str
    source: str

    @property
    def pair(self) -> frozenset[ComprehensionDefectCause]:
        return frozenset((self.first, self.second))


_MINHAJ: Final = (
    "منهاج الوصول إلى علم الأصول للبيضاوي وشروحه (نهاية السول للإسنوي)، "
    "في عدّ الأمور المخلّة بفهم المراد وترتيبها عند التعارض"
)
_MUSTASFA: Final = "المستصفى للغزالي، في تعارض دلائل الألفاظ"
_TALWIH: Final = "التلويح على التوضيح للتفتازاني، في مباحث الحقيقة والمجاز والمشترك"

_ARGUMENTS: Final = (
    PriorityArgument(
        first=ComprehensionDefectCause.TAKHSIS,
        second=ComprehensionDefectCause.MAJAZ,
        verdict="التخصيص أولى",
        argument=(
            "العامّ بعد تخصيصه يبقى حجّةً في الباقي، فاللفظ مُعمَل في بعض ما "
            "وُضِع له لا مصروف عن موضوعه؛ والمجاز صرفٌ للفظ عن موضوعه رأسًا إلى "
            "غيره. والإعمال في بعض الموضوع أهون من الصرف عنه كلّه"
        ),
        source=_MUSTASFA,
    ),
    PriorityArgument(
        first=ComprehensionDefectCause.TAKHSIS,
        second=ComprehensionDefectCause.IDMAR,
        verdict="التخصيص أولى",
        argument=(
            "التخصيص تقليل لأفراد اللفظ مع بقاء دلالته على ما بقي، والإضمار "
            "زيادة محذوفٍ مقدَّر لم ينطق به النصّ؛ وتقليل الأفراد أهون من "
            "إضافة ما ليس في اللفظ"
        ),
        source=_MINHAJ,
    ),
    PriorityArgument(
        first=ComprehensionDefectCause.TAKHSIS,
        second=ComprehensionDefectCause.NAQL,
        verdict="التخصيص أولى",
        argument=(
            "التخصيص لا يُبطل الوضع الأول بحال، والنقل يُبطله ويُثبت وضعًا "
            "ثانيًا؛ وبقاء الوضع الأول مع قصر اللفظ على بعض أفراده أهون من "
            "رفع الوضع الأول جملةً"
        ),
        source=_MINHAJ,
    ),
    PriorityArgument(
        first=ComprehensionDefectCause.TAKHSIS,
        second=ComprehensionDefectCause.ISHTIRAK,
        verdict="التخصيص أولى",
        argument=(
            "التخصيص يُبقي اللفظ مفيدًا معنى معيّنًا في الباقي، والاشتراك "
            "يُبقي الإجمال قائمًا فلا يتعيّن المراد إلا بقرينة في كل استعمال؛ "
            "والمفيد المعيَّن أولى من المجمل المتوقَّف"
        ),
        source=_MINHAJ,
    ),
    PriorityArgument(
        first=ComprehensionDefectCause.MAJAZ,
        second=ComprehensionDefectCause.IDMAR,
        verdict="سواء",
        argument=(
            "الإضمار عند المحقّقين مجازٌ بالنقصان (مجاز الحذف)، فالإخلال فيهما "
            "من جنس واحد: صرف اللفظ عن ظاهره لعلاقة مع قرينة دالّة. وقد رتّب "
            "بعض الأصوليين المجاز على الإضمار لشهرة علاقاته، وهذه المفردة "
            "تتبنّى التسوية صراحةً وتسجّل الخلاف بدل إخفائه"
        ),
        source=_TALWIH,
    ),
    PriorityArgument(
        first=ComprehensionDefectCause.MAJAZ,
        second=ComprehensionDefectCause.NAQL,
        verdict="المجاز أولى",
        argument=(
            "المجاز يستعمل اللفظ في غير موضوعه لعلاقةٍ وقرينةٍ مع بقاء الوضع "
            "الأصلي قائمًا يُرجَع إليه عند انتفاء القرينة؛ والنقل يرفع الوضع "
            "الأول ويُثبت وضعًا ثانيًا، وهو خلاف الأصل ويفتقر إلى نقل تاريخي "
            "مستقلّ لا يثبت بمجرد الاستعمال"
        ),
        source=_TALWIH,
    ),
    PriorityArgument(
        first=ComprehensionDefectCause.MAJAZ,
        second=ComprehensionDefectCause.ISHTIRAK,
        verdict="المجاز أولى",
        argument=(
            "المجاز يتعيّن مراده بالقرينة مع بقاء الحقيقة أصلًا معلومًا، "
            "والاشتراك يجعل المعنيين سواءً في الوضع فلا أصل يُرجَع إليه عند "
            "فقد القرينة؛ فالمجاز أقلّ إخلالًا بمقصود الوضع من الإفهام"
        ),
        source=_MINHAJ,
    ),
    PriorityArgument(
        first=ComprehensionDefectCause.IDMAR,
        second=ComprehensionDefectCause.NAQL,
        verdict="الإضمار أولى",
        argument=(
            "الإضمار تقديرُ محذوفٍ يدلّ عليه سياق اللفظ نفسه مع بقاء وضع "
            "المنطوق به على حاله، والنقل إبطالٌ للوضع الأول؛ وتقديرُ ما دلّ "
            "عليه السياق أهون من رفع الوضع"
        ),
        source=_TALWIH,
    ),
    PriorityArgument(
        first=ComprehensionDefectCause.IDMAR,
        second=ComprehensionDefectCause.ISHTIRAK,
        verdict="الإضمار أولى",
        argument=(
            "الإضمار إجمالٌ عارض في موضع بعينه يزول بتقدير السياق، والاشتراك "
            "إجمالٌ لازم في الوضع نفسه يعود في كل استعمال؛ والعارض أهون من "
            "اللازم"
        ),
        source=_MINHAJ,
    ),
    PriorityArgument(
        first=ComprehensionDefectCause.NAQL,
        second=ComprehensionDefectCause.ISHTIRAK,
        verdict="النقل أولى",
        argument=(
            "المنقول يفيد في كل عصرٍ معنًى واحدًا معيَّنًا بعد استقرار النقل، "
            "فالإخلال فيه منقطع؛ والمشترك يبقي التوقّف على القرينة أبدًا، "
            "فالإخلال فيه دائم، والدائم أشدّ"
        ),
        source=_MINHAJ,
    ),
)

_ARGUMENT_BY_PAIR: Final = {argument.pair: argument for argument in _ARGUMENTS}

PRIORITY_ARGUMENTS: Final = _ARGUMENTS

_CAUSE_BY_KEY: Final = {
    comparison_key(cause.value): cause for cause in ComprehensionDefectCause
}
_NOT_APPLICABLE_KEY: Final = comparison_key(NOT_APPLICABLE)

if len(_CAUSE_BY_KEY) != len(ComprehensionDefectCause):  # pragma: no cover - guard
    raise RuntimeError("two defect causes collapse onto one comparison key")
if _NOT_APPLICABLE_KEY in _CAUSE_BY_KEY:  # pragma: no cover - guard
    raise RuntimeError("لا_ينطبق collides with a declared defect cause")
if len(_ARGUMENT_BY_PAIR) != len(_ARGUMENTS):  # pragma: no cover - guard
    raise RuntimeError("two priority arguments describe the same comparison")


def canonical_defect_classification(value: str) -> ComprehensionDefectCause | None:
    """أعِد السبب المسمَّى في `value`، أو `None` إن صُرِّح بـ`لا_ينطبق`.

    `None` هنا معناها التصريح بعدم الانطباق، لا الصمت ولا الغياب: الحقل نفسه
    اختياري، أمّا إذا ذُكِر فلا يُقبل فيه إلا أحد الخمسة أو `لا_ينطبق`. وأيّ
    لفظ آخر — تصحيفًا كان أو اصطلاحًا مُخترعًا — يُرَدّ ولا يُحمل على أقرب
    الخمسة.
    """

    if not isinstance(value, str) or not value.strip():
        raise ComprehensionDefectError("سبب_الإخلال_بالفهم must be non-blank text")
    key = comparison_key(value)
    if key == _NOT_APPLICABLE_KEY:
        return None
    cause = _CAUSE_BY_KEY.get(key)
    if cause is None:
        raise ComprehensionDefectError(
            "سبب_الإخلال_بالفهم must be one of: " + "، ".join(DECLARABLE_VALUES)
        )
    return cause


def defect_priority(cause: ComprehensionDefectCause) -> int:
    """رتبة السبب في الترتيب المنصوص؛ الأصغر أولى وأهون إخلالًا."""

    if not isinstance(cause, ComprehensionDefectCause):
        raise ComprehensionDefectError(
            "defect priority requires a closed-vocabulary cause"
        )
    return _PRIORITY_RANK[cause]


def compare_defect_priority(
    first: ComprehensionDefectCause, second: ComprehensionDefectCause
) -> int:
    """‏-1 إذا كان `first` أولى، و1 إذا كان `second` أولى، و0 عند التسوية."""

    difference = defect_priority(first) - defect_priority(second)
    return (difference > 0) - (difference < 0)


def priority_argument(
    first: ComprehensionDefectCause, second: ComprehensionDefectCause
) -> PriorityArgument:
    """الحجّة النصّية الموثَّقة لهذه المقارنة بعينها."""

    if first is second:
        raise ComprehensionDefectError("a cause is not compared with itself")
    argument = _ARGUMENT_BY_PAIR.get(
        frozenset((_require_cause(first), _require_cause(second)))
    )
    if argument is None:  # pragma: no cover - guard
        raise ComprehensionDefectError("no documented argument for this comparison")
    return argument


def _require_cause(cause: ComprehensionDefectCause) -> ComprehensionDefectCause:
    if not isinstance(cause, ComprehensionDefectCause):
        raise ComprehensionDefectError(
            "priority arguments compare closed-vocabulary causes only"
        )
    return cause


EXHAUSTION_PRECEDES_CLASSIFICATION_NOTE: Final = (
    "ExhaustionPrecedesClassification: إعلانُ سببٍ متأخّرٍ في ترتيب الخمسة "
    "ادّعاءٌ ضمنيّ بأن كلّ ما هو أولى منه بالحمل قد استُبعِد بدليل؛ فالتصنيف "
    "قبل استبعاد الأقوى رتبةً سابقٌ لأوانه منهجيًّا ولو صادف الصواب"
)
REPORTED_EXHAUSTION_IS_NOT_A_GATE_NOTE: Final = (
    "ReportedExhaustionIsNotAGate: استنفاد الأسباب الأقوى هنا حالةٌ تقريرية "
    "تُقرأ وتُذكَر، ولا تُسقِط بطاقةً ولا تغيّر نتيجة التدقيق الخارجي ولا "
    "تُحرّك بوّابة نواة؛ والفارق عن استنفاد G0 مُسمّى لا مُدّعى تطابقه"
)


class ExhaustionStatus(Enum):
    """حالة استنفاد الأسباب الأقوى رتبةً من التصنيف المُعلَن؛ مفردة ثلاثية."""

    COMPLETE = "استنفاد_مكتمل"
    INCOMPLETE = "استنفاد_ناقص"
    NOT_REQUIRED = "لا_يلزم_استنفاد"


@dataclass(frozen=True, slots=True)
class StrongerCauseExclusion:
    """استبعادٌ مُعلَنٌ لسببٍ أولى بالحمل، بدليله ومصدره المُسمّى."""

    cause: ComprehensionDefectCause
    evidence: str
    named_source: str


@dataclass(frozen=True, slots=True)
class ExhaustionAssessment:
    """حالةٌ مُشتَقّة من الترتيب القائم، وتسميةُ ما بقي بغير استبعاد."""

    status: ExhaustionStatus
    remaining: tuple[ComprehensionDefectCause, ...]


def stronger_causes(
    cause: ComprehensionDefectCause,
) -> tuple[ComprehensionDefectCause, ...]:
    """الأسباب الأولى بالحمل من `cause`، مُشتَقّةً من `_PRIORITY_RANK` وحده.

    لا جدولَ ثانيًا هنا: الأقوى هو الأصغر رتبةً في نفس الترتيب المُحتجّ له في
    `PRIORITY_ARGUMENTS`. فـ`اشتراك` يُعيد الأربعة، و`تخصيص` يُعيد الفارغ،
    و`مجاز` و`إضمار` متساويان فلا يُعدّ أحدهما أقوى من الآخر.
    """

    rank = defect_priority(cause)
    return tuple(
        other for other in ComprehensionDefectCause if _PRIORITY_RANK[other] < rank
    )


def read_stronger_cause_exclusions(
    entries: Any, declared: ComprehensionDefectCause
) -> tuple[StrongerCauseExclusion, ...]:
    """يقرأ استبعادات الأسباب الأقوى المُعلَنة تحت قراءةٍ منافسةٍ مصنَّفة.

    البطاقة لا تُعلن أيُّها أقوى — ذلك مُشتَقٌّ من الترتيب — وإنما تُعلن الاسم
    ودليل الاستبعاد ومصدره المُسمّى. ويُرفَض عند القراءة: السبب المكرَّر،
    والسبب الذي ليس أقوى رتبةً من المُعلَن (المساوي أو الأضعف)، فلا يُموَّه
    الاستنفاد بإضافاتٍ لا تلزم.
    """

    if not isinstance(entries, Sequence) or isinstance(entries, str | bytes):
        raise ComprehensionDefectError("استبعاد_الأسباب_الأقوى must be a list")
    allowed = set(stronger_causes(declared))
    exclusions: list[StrongerCauseExclusion] = []
    seen: set[ComprehensionDefectCause] = set()
    for entry in entries:
        if not isinstance(entry, Mapping):
            raise ComprehensionDefectError(
                "استبعاد_الأسباب_الأقوى[] entries must be mappings"
            )
        unknown = set(entry) - {"السبب", "دليل_الاستبعاد", "المصدر_المُسمّى"}
        if unknown:
            raise ComprehensionDefectError(
                "استبعاد_الأسباب_الأقوى[] accepts only: السبب، دليل_الاستبعاد،"
                " المصدر_المُسمّى"
            )
        cause = canonical_defect_classification(
            _require_text(entry.get("السبب"), "استبعاد_الأسباب_الأقوى[].السبب")
        )
        if cause is None:
            raise ComprehensionDefectError(
                "استبعاد_الأسباب_الأقوى[].السبب لا يقبل لا_ينطبق"
            )
        if cause not in allowed:
            raise ComprehensionDefectError(
                "استبعاد_الأسباب_الأقوى[].السبب يجب أن يكون أولى بالحمل من "
                f"({declared.value})؛ " + EXHAUSTION_PRECEDES_CLASSIFICATION_NOTE
            )
        if cause in seen:
            raise ComprehensionDefectError("استبعاد_الأسباب_الأقوى[].السبب لا يتكرّر")
        seen.add(cause)
        exclusions.append(
            StrongerCauseExclusion(
                cause=cause,
                evidence=_require_text(
                    entry.get("دليل_الاستبعاد"),
                    "استبعاد_الأسباب_الأقوى[].دليل_الاستبعاد",
                ),
                named_source=_require_text(
                    entry.get("المصدر_المُسمّى"),
                    "استبعاد_الأسباب_الأقوى[].المصدر_المُسمّى",
                ),
            )
        )
    return tuple(exclusions)


def assess_exhaustion(
    declared: ComprehensionDefectCause,
    exclusions: tuple[StrongerCauseExclusion, ...] = (),
) -> ExhaustionAssessment:
    """حالةٌ تقريرية لا حكم: ما بقي من الأقوى بلا استبعادٍ يُسمَّى بعينه."""

    required = stronger_causes(declared)
    if not required:
        return ExhaustionAssessment(ExhaustionStatus.NOT_REQUIRED, ())
    excluded = {item.cause for item in exclusions}
    remaining = tuple(cause for cause in required if cause not in excluded)
    if remaining:
        return ExhaustionAssessment(ExhaustionStatus.INCOMPLETE, remaining)
    return ExhaustionAssessment(ExhaustionStatus.COMPLETE, ())


def _require_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ComprehensionDefectError(f"{field_name} must be non-blank text")
    return value
