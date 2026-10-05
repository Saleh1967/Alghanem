"""`Σ_L`: تسجيلُ النماذج الأضعف وشروطِ استقلال المدوّنة، بلا تشغيلٍ ولا اختيار.

**التسجيلُ ليس تشغيلًا** (`RegistrationIsNotARun`): تُجمَّد هنا النماذجُ
الأضعفُ التي يجب أن تُقابَل بها دعوى النسبة، وشروطُ المدوّنة التي يصحّ أن
تُقاس عليها؛ ولا مدوّنةَ تُسمّى، ولا درجةَ تُحسَب، ولا قراءةَ تُخرَج.

**والمدوّنةُ لا تُختار بعد رؤية النتيجة** (`TheCorpusIsNamedBeforeTheResult`):
شروطُ الاستقلال مُجمَّدةٌ الآن، وتشغيلُها **مؤجَّلٌ مُصرَّحٌ بتأجيله** حتى
تُسمّى مجموعةٌ محجوزةٌ لم تدخل في بناء الفرضية ولا في تجارب `G0.FLT` السابقة.
فالمدوّنةُ المختارةُ بعد الرقم تُثبِت ما اختِيرت لأجله.

**والتعادلُ يُسقِط الدعوى** (`AWeakerRepresentationThatTiesDefeatsTheClaim`،
مُعادُ الاستعمال لا مُعادُ الاختراع): نموذجٌ أضعفُ يعيد الهدفَ نفسَه بالكفاءة
نفسِها يُسقِط دعوى أنّ النسبةَ مستوًى زائدٌ على التمثيل؛ ولا يُشترَط تفوُّقُه.

تسجيلٌ لا سلطة: لا حكمَ هنا، ولا استيرادَ من `kernel/` ولا من `arabic/`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

__all__ = [
    "A_WEAKER_REPRESENTATION_THAT_TIES_DEFEATS_THE_CLAIM",
    "CORPUS_INDEPENDENCE_CONDITIONS",
    "NISBAH_NULL_MODELS",
    "REGISTRATION_IS_NOT_A_RUN",
    "THE_CORPUS_IS_NAMED_BEFORE_THE_RESULT",
    "CorpusIndependenceCondition",
    "NullModelRegistration",
    "NullModelRegistrationError",
    "RunStanding",
]


class NullModelRegistrationError(ValueError):
    """رفضٌ عند الإنشاء: نموذجٌ بلا ما يُسقِطه، أو تسجيلٌ يُعلن تشغيلًا."""


REGISTRATION_IS_NOT_A_RUN: Final[str] = (
    "التسجيلُ ليس تشغيلًا: لا مدوّنةَ مُسمّاةٌ هنا ولا درجةٌ محسوبةٌ ولا قراءةٌ "
    "مُخرَجة؛ وكلُّ ما يفعله هذا الموضعُ تجميدُ ما يجب أن يُقابَل قبل أن يُقاس"
)

THE_CORPUS_IS_NAMED_BEFORE_THE_RESULT: Final[str] = (
    "المدوّنةُ تُسمّى قبل النتيجة لا بعدها: مجموعةٌ محجوزةٌ لم تدخل في بناء "
    "الفرضية ولا في تجاربِ `G0.FLT` السابقة؛ ومدوّنةٌ تُختار بعد الرقم تُثبِت "
    "ما اختِيرت لأجله"
)

A_WEAKER_REPRESENTATION_THAT_TIES_DEFEATS_THE_CLAIM: Final[str] = (
    "نموذجٌ أضعفُ يتعادل يُسقِط الدعوى: التعادلُ كافٍ، ولا يُشترَط تفوُّقُ "
    "النموذج الأضعف حتى تسقط دعوى أنّ النسبةَ مستوًى زائدٌ على التمثيل"
)


class RunStanding(Enum):
    """موقفُ التشغيل؛ عضوانِ، والقابلُ للتشغيل غيرُ قابلٍ للبناء اليوم."""

    DEFERRED_UNTIL_A_HELD_OUT_CORPUS_IS_NAMED = "مؤجَّلٌ_حتى_تُسمّى_مدوّنةٌ_محجوزة"
    RUNNABLE = "قابلٌ_للتشغيل"


@dataclass(frozen=True, slots=True)
class NullModelRegistration:
    """نموذجٌ أضعفُ مُسجَّلٌ قبل التشغيل: ما يمثّله، وما يُسقِطه إن تعادل."""

    model_id: str
    what_it_represents: str
    what_its_tie_defeats: str
    run_standing: RunStanding

    def __post_init__(self) -> None:
        for value, label in (
            (self.model_id, "اسمُ النموذج"),
            (self.what_it_represents, "ما يمثّله النموذج"),
            (self.what_its_tie_defeats, "ما يُسقِطه تعادلُه"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise NullModelRegistrationError(f"{label} نصٌّ غير فارغ")
        if not isinstance(self.run_standing, RunStanding):
            raise NullModelRegistrationError("موقفُ التشغيل عضوٌ في مفردته المغلقة")
        if self.run_standing is RunStanding.RUNNABLE:
            raise NullModelRegistrationError(THE_CORPUS_IS_NAMED_BEFORE_THE_RESULT)


@dataclass(frozen=True, slots=True)
class CorpusIndependenceCondition:
    """شرطُ استقلالٍ واحدٌ للمدوّنة المحجوزة، وما يُبطله خرقُه."""

    condition_id: str
    requirement: str
    what_its_breach_invalidates: str

    def __post_init__(self) -> None:
        for value, label in (
            (self.condition_id, "اسمُ الشرط"),
            (self.requirement, "نصُّ الشرط"),
            (self.what_its_breach_invalidates, "ما يُبطله خرقُ الشرط"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise NullModelRegistrationError(f"{label} نصٌّ غير فارغ")


NISBAH_NULL_MODELS: Final[tuple[NullModelRegistration, ...]] = (
    NullModelRegistration(
        model_id="carrier-alone",
        what_it_represents="الحاملَ وحدَه بلا حالةٍ ولا دورٍ نسبيّ",
        what_its_tie_defeats="دعوى أنّ التمثيلَ الثنائيَّ نفسَه زائدٌ على الحامل",
        run_standing=RunStanding.DEFERRED_UNTIL_A_HELD_OUT_CORPUS_IS_NAMED,
    ),
    NullModelRegistration(
        model_id="carrier-state-pair",
        what_it_represents="الحاملَ والحالةَ مربوطَين بلا دورٍ نسبيٍّ ولا محمول",
        what_its_tie_defeats="دعوى أنّ الدورَ النسبيَّ مستوًى زائدٌ على التمثيل",
        run_standing=RunStanding.DEFERRED_UNTIL_A_HELD_OUT_CORPUS_IS_NAMED,
    ),
    NullModelRegistration(
        model_id="unordered-term-pair",
        what_it_represents="طرفَين بلا محمولٍ ولا ترتيبَ حججٍ بينهما",
        what_its_tie_defeats="دعوى أنّ المحمولَ ومواضعَ حججه هي الفارق",
        run_standing=RunStanding.DEFERRED_UNTIL_A_HELD_OUT_CORPUS_IS_NAMED,
    ),
    NullModelRegistration(
        model_id="arguments-only-closure",
        what_it_represents="إغلاقًا يُقرَأ من امتلاء الحجج وحدَه",
        what_its_tie_defeats="دعوى أنّ المكوّناتِ الأربعةَ الباقيةَ تُضيف تمييزًا",
        run_standing=RunStanding.DEFERRED_UNTIL_A_HELD_OUT_CORPUS_IS_NAMED,
    ),
)
"""النماذجُ الأضعفُ الأربعة، مُسجَّلةً قبل أيّ مدوّنةٍ وقبل أيّ درجة."""


CORPUS_INDEPENDENCE_CONDITIONS: Final[tuple[CorpusIndependenceCondition, ...]] = (
    CorpusIndependenceCondition(
        condition_id="held-out-from-the-hypothesis",
        requirement="ألّا تكون أسطحُها قد دخلت في صياغة فرضية النسبة",
        what_its_breach_invalidates="الاختبارَ كلَّه، فيصير فحصًا للتعريف",
    ),
    CorpusIndependenceCondition(
        condition_id="disjoint-from-prior-flt-surfaces",
        requirement="أن تكون منفصلةً عن أسطح `G0.FLT-0` و`G0.FLT-1` المُجمَّدة",
        what_its_breach_invalidates="استقلالَ النتيجة عن تجربةٍ سبق أن قُرِئت",
    ),
    CorpusIndependenceCondition(
        condition_id="named-before-any-score",
        requirement="أن تُسمّى ويُجمَّد هدفُ إعادة البناء قبل حساب أيّ درجة",
        what_its_breach_invalidates="أن يكون الهدفُ محايدًا بين النموذج ونظيره الأضعف",
    ),
    CorpusIndependenceCondition(
        condition_id="analytic-gates-excluded",
        requirement="أن تُعلَن تحليليّةً كلُّ بوّابةٍ تصدق ببنية القارئ لا بالمدوّنة",
        what_its_breach_invalidates="وزنَ الدليل، فتُعَدّ صحّةٌ بالتعريف شاهدًا",
    ),
)
"""شروطُ استقلال المدوّنة، مُجمَّدةً الآن ومؤجَّلٌ تشغيلُها بالتصريح."""
