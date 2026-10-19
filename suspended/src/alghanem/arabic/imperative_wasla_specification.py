"""مواصفةُ قياس همزة الوصل في الأمر المجرَّد — **مُصاغةٌ بعد الرقم، مُصرَّحٌ به**.

`THIS_SPECIFICATION_IS_NOT_PRIOR_TO_THE_EVIDENCE`: لم تُجمَّد هذه المواصفةُ قبل
القياس. فقد شُغِّل العدُّ على البايتات أوّلًا، فظهر أنّ **الرقمَ يتبع تعريفَ
حرف العلّة لا البايتات**؛ وعندئذٍ صيغت المواصفة. فمنزلتُها المُعلَنة
`مُصاغة_بعد_الرقم` لا `سابقة_للدليل`، وهي أضعفُ المنزلتين تصريحًا لا تأويلًا.
ومن قرأ أرقامَها على أنّها تنبّؤٌ تحقّق فقد قرأ ما لم يقع.

**والسببُ الذي أوجب التصريح هو عينُ النتيجة**: الفارقُ الوارد في النصّ
(٩٦٫٩٪ للسالم) **لا يخرج إلا إذا عُدَّت الهمزةُ حرفَ علّة**. وعدُّها كذلك
**يخلط المهموزَ بالمعتلّ**، وهما بابان متمايزان في الصرف. فلم تُختَر قاعدةٌ
واحدةٌ ويُسكَت عن أخواتها؛ بل تُعلَن **أربع قواعدَ متنافسةٍ معًا**، ويُعرَض
الرقمُ تحت كلِّ واحدةٍ منها، ليُرى أيُّ رقمٍ ثابتٌ وأيُّه صنيعةُ القاعدة.

`THE_RULE_IS_DECLARED_BEFORE_ITS_NUMBER_IS_PREFERRED`: القواعدُ الأربعُ
مُعرَّفةٌ هنا بأعيانها ومُجمَّدةٌ ببصمةٍ واحدة، ويُلزَم القياسُ بإخراج الجدول
**تحتها كلِّها**. فمن أراد ترجيحَ إحداها لزِمَه أن يُرجِّحها بحجّةٍ صرفيةٍ
مُعلَنة، لا بأنّ رقمَها أجمل.

`ABSENCE_OF_A_FORM_IS_NOT_ABSENCE_OF_ITS_POSSIBILITY`: دعوى «المضارعُ شرطُ
إمكانٍ للأمر» لا تُحسَم من مدوَّنةٍ محدودة. فغيابُ مضارعِ جذرٍ عن القرآن غيابُ
دليلٍ لا دليلُ غياب، ويُعَدُّ ويُسمّى ولا يُبنى عليه نفيٌ للإمكان.

`THE_WASL_IS_READ_FROM_ONE_CHARACTER_NOT_INFERRED`: حضورُ همزة الوصل يُقرأ من
ابتداء صورة المقطع بمحرف `{` وحدَه (وهو ألفُ الوصل في ترميز Buckwalter)، لا
من تخمينِ نطقٍ ولا من قياسٍ على وزن. ومحرفُ `>` همزةُ قطعٍ لا وصل، فلا يُعَدُّ
منها؛ ومن سوّى بينهما عدَّ البابين بابًا.

وهذه الوحدة تسجيلٌ لا سلطة: لا ولادةَ فيها، ولا حكمَ ولادة، ولا تجميدَ `E0`،
ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest

__all__ = [
    "ABSENCE_OF_A_FORM_IS_NOT_ABSENCE_OF_ITS_POSSIBILITY_NOTE",
    "ARRIVING_IMPERATIVE_FIGURES",
    "IMPERATIVE_WASL_NAMED_RESIDUALS",
    "IMPERATIVE_WASL_SPECIFICATION_DIGEST",
    "PERMUTATION_PROTOCOL",
    "THE_RULE_IS_DECLARED_BEFORE_ITS_NUMBER_IS_PREFERRED_NOTE",
    "THE_WASL_IS_READ_FROM_ONE_CHARACTER_NOT_INFERRED_NOTE",
    "THIS_SPECIFICATION_IS_NOT_PRIOR_TO_THE_EVIDENCE_NOTE",
    "WASL_CHARACTER",
    "WEAKNESS_RULES",
    "ArrivingImperativeFigure",
    "ImperativeWaslSpecificationError",
    "PermutationProtocol",
    "RootShape",
    "SpecificationStanding",
    "WeaknessRule",
    "specification_digest",
]


class ImperativeWaslSpecificationError(ValueError):
    """تُرفَع حين تُوصَف قاعدةُ العدّ وصفًا لا يُعاد به اشتقاقُ رقمها."""


class SpecificationStanding(Enum):
    """منزلةُ المواصفة؛ والقيمةُ الأقوى معلنةٌ ليُرى أنّ هذه ليست إيّاها."""

    PRIOR_TO_THE_EVIDENCE = "سابقة_للدليل"
    FORMULATED_AFTER_THE_NUMBER = "مُصاغة_بعد_الرقم"


STANDING: Final[SpecificationStanding] = (
    SpecificationStanding.FORMULATED_AFTER_THE_NUMBER
)
"""منزلةُ هذه المواصفة بعينها؛ وهي الأضعف، مُعلَنةً لا مُؤوَّلة."""


THIS_SPECIFICATION_IS_NOT_PRIOR_TO_THE_EVIDENCE_NOTE: Final[str] = (
    "ThisSpecificationIsNotPriorToTheEvidence: شُغِّل العدُّ قبل صوغ المواصفة، "
    "فمنزلتُها `مُصاغة_بعد_الرقم`؛ ومن قرأ أرقامَها تنبّؤًا تحقّق قرأ ما لم يقع"
)

THE_RULE_IS_DECLARED_BEFORE_ITS_NUMBER_IS_PREFERRED_NOTE: Final[str] = (
    "TheRuleIsDeclaredBeforeItsNumberIsPreferred: أربعُ قواعدَ متنافسةٍ "
    "مُعلَنةٌ معًا ويُعرَض الرقمُ تحتها كلِّها؛ فما ثبت تحت الأربع ثابتٌ، وما "
    "تبدّل بتبدّلها صنيعةُ القاعدة لا خبرٌ عن البايتات"
)

ABSENCE_OF_A_FORM_IS_NOT_ABSENCE_OF_ITS_POSSIBILITY_NOTE: Final[str] = (
    "AbsenceOfAFormIsNotAbsenceOfItsPossibility: غيابُ مضارعِ جذرٍ عن هذه "
    "المدوَّنة غيابُ دليلٍ لا دليلُ غياب؛ فيُعَدُّ ويُسمّى ولا يُنفى به إمكان"
)

THE_WASL_IS_READ_FROM_ONE_CHARACTER_NOT_INFERRED_NOTE: Final[str] = (
    "TheWaslIsReadFromOneCharacterNotInferred: همزةُ الوصل تُقرأ من ابتداء "
    "الصورة بمحرف `{` وحدَه، و`>` همزةُ قطعٍ لا تُعَدُّ منها؛ ومن سوّى بينهما "
    "عدَّ البابين بابًا"
)

THE_HAMZA_IS_NOT_A_WEAK_LETTER_IN_THE_GRAMMARIANS_SENSE_NOTE: Final[str] = (
    "TheHamzaIsNotAWeakLetterInTheGrammariansSense: حروفُ العلّة عند أهل "
    "الصرف الألفُ والواوُ والياء، والمهموزُ بابٌ آخر؛ فعَدُّ الهمزة منها "
    "قاعدةٌ تُسَنّ وتُعلَن، لا قراءةٌ تُقرأ من المدوَّنة"
)

IMPERATIVE_WASL_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "ThisSpecificationIsNotPriorToTheEvidence": (
        THIS_SPECIFICATION_IS_NOT_PRIOR_TO_THE_EVIDENCE_NOTE
    ),
    "TheRuleIsDeclaredBeforeItsNumberIsPreferred": (
        THE_RULE_IS_DECLARED_BEFORE_ITS_NUMBER_IS_PREFERRED_NOTE
    ),
    "AbsenceOfAFormIsNotAbsenceOfItsPossibility": (
        ABSENCE_OF_A_FORM_IS_NOT_ABSENCE_OF_ITS_POSSIBILITY_NOTE
    ),
    "TheWaslIsReadFromOneCharacterNotInferred": (
        THE_WASL_IS_READ_FROM_ONE_CHARACTER_NOT_INFERRED_NOTE
    ),
    "TheHamzaIsNotAWeakLetterInTheGrammariansSense": (
        THE_HAMZA_IS_NOT_A_WEAK_LETTER_IN_THE_GRAMMARIANS_SENSE_NOTE
    ),
}


WASL_CHARACTER: Final[str] = "{"
"""ألفُ الوصل في ترميز Buckwalter؛ وهي المحرفُ الوحيدُ الذي يُقرأ منه الحضور."""


class RootShape(Enum):
    """أصنافُ الجذر الثلاثيّ كما تُقسَم في هذا القياس، والمضاعفُ منها مُفرَد."""

    SALIM = "سالم"
    MUDAAF = "مضاعف"
    MITHAL = "مثال"
    AJWAF = "أجوف"
    NAQIS = "ناقص"
    LAFIF = "لفيف"


@dataclass(frozen=True, slots=True)
class WeaknessRule:
    """قاعدةُ تصنيفٍ واحدة: ما يُعَدُّ حرفَ علّة، وهل يُفرَد المضاعف."""

    name: str
    weak_letters: tuple[str, ...]
    separates_the_doubled_root: bool
    what_it_assumes: str

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ImperativeWaslSpecificationError("اسمُ القاعدة نصٌّ غير فارغ.")
        if not self.weak_letters:
            raise ImperativeWaslSpecificationError(
                "قاعدةٌ بلا حرفِ علّةٍ واحدٍ لا تُصنِّف شيئًا."
            )
        if len(set(self.weak_letters)) != len(self.weak_letters):
            raise ImperativeWaslSpecificationError(
                "حرفُ علّةٍ مكرّرٌ في القاعدة؛ والتكرارُ يُوهِم سَعةً."
            )
        if not isinstance(self.separates_the_doubled_root, bool):
            raise ImperativeWaslSpecificationError(
                "إفرادُ المضاعف قرارٌ ثنائيٌّ مُصرَّحٌ به لا مسكوتٌ عنه."
            )
        if (
            not isinstance(self.what_it_assumes, str)
            or not self.what_it_assumes.strip()
        ):
            raise ImperativeWaslSpecificationError(
                "لكلِّ قاعدةٍ مُصادَرةٌ تُنطَق؛ وقاعدةٌ بلا مُصادَرةٍ مُعلَنةٍ "
                "تُمرِّر رأيًا في صورة قياس."
            )


WEAKNESS_RULES: Final[tuple[WeaknessRule, ...]] = (
    WeaknessRule(
        name="علّة_فقط",
        weak_letters=("w", "y"),
        separates_the_doubled_root=False,
        what_it_assumes=(
            "حروفُ العلّة الواوُ والياءُ وحدَهما، كما عند أهل الصرف؛ والمهموزُ "
            "يُعَدُّ سالمًا، والمضاعفُ يُعَدُّ سالمًا"
        ),
    ),
    WeaknessRule(
        name="علّة_فقط_والمضاعف_مُفرَد",
        weak_letters=("w", "y"),
        separates_the_doubled_root=True,
        what_it_assumes=(
            "حروفُ العلّة الواوُ والياءُ وحدَهما، والمضاعفُ بابٌ قائمٌ بنفسه "
            "لأنّ الإدغام يُحرِّك أوّلَه كما يفعل الإعلال"
        ),
    ),
    WeaknessRule(
        name="علّة_وهمزة",
        weak_letters=("w", "y", "A"),
        separates_the_doubled_root=False,
        what_it_assumes=(
            "تُعَدُّ الهمزةُ حرفَ علّة، وهي مُصادَرةٌ تخلط المهموزَ بالمعتلّ "
            "وتُنتِج الرقمَ الوارد في النصّ؛ فتُعلَن ولا تُدَسّ"
        ),
    ),
    WeaknessRule(
        name="علّة_وهمزة_والمضاعف_مُفرَد",
        weak_letters=("w", "y", "A"),
        separates_the_doubled_root=True,
        what_it_assumes=(
            "الهمزةُ حرفُ علّةٍ والمضاعفُ بابٌ مُفرَد؛ وهي القاعدةُ الأسخى على "
            "الفرضية، فيُعرَض رقمُها بوصفه أقصى ما تحتمله لا بوصفه الرقم"
        ),
    ),
)
"""القواعدُ الأربعُ مُعلَنةٌ معًا؛ ولا تُحذَف منها واحدةٌ بعد رؤية رقمها."""


@dataclass(frozen=True, slots=True)
class PermutationProtocol:
    """بروتوكولُ التبديل ببذرته وعدده وصيغة احتماله؛ ولا يُبدَّل بعد التجميد."""

    statistic: str
    permutations: int
    seed: int
    generator: str
    p_value_formula: str

    def __post_init__(self) -> None:
        if self.permutations < 1000:
            raise ImperativeWaslSpecificationError(
                "عددُ التبديلات دون الألف يُضيّق أرضيةَ الاحتمال؛ فلا يُقبَل."
            )


PERMUTATION_PROTOCOL: Final[PermutationProtocol] = PermutationProtocol(
    statistic="القيمةُ المطلقةُ لفارق نسبتَي حضور همزة الوصل بين صنفَي جذر",
    permutations=5_000,
    seed=20_260_916,
    generator="random.Random(seed).shuffle على قائمةٍ مدموجةٍ مرتَّبة",
    p_value_formula="(1 + عددُ التبديلات التي بلغت الفارقَ المرصود) / (1 + 5000)",
)

P_VALUE_FLOOR: Final[str] = "1/5001"
"""أصغرُ احتمالٍ يُخرِجه البروتوكول؛ و`0.0000` لا يقع منه أبدًا."""


@dataclass(frozen=True, slots=True)
class ArrivingImperativeFigure:
    """رقمٌ وارِدٌ بنصّه، مُودَعٌ كما وصل قبل أن يُقاس."""

    label: str
    claimed_value: str

    def __post_init__(self) -> None:
        for value, name in ((self.label, "وصفُ الرقم"), (self.claimed_value, "قيمتُه")):
            if not isinstance(value, str) or not value.strip():
                raise ImperativeWaslSpecificationError(f"{name} نصٌّ غير فارغ.")


ARRIVING_IMPERATIVE_FIGURES: Final[tuple[ArrivingImperativeFigure, ...]] = (
    ArrivingImperativeFigure("الناقصُ بهمزة وصل", "70/71"),
    ArrivingImperativeFigure("نسبةُ الناقص", "98.6"),
    ArrivingImperativeFigure("السالمُ بهمزة وصل", "404/417"),
    ArrivingImperativeFigure("نسبةُ السالم", "96.9"),
    ArrivingImperativeFigure("اللفيفُ بهمزة وصل", "14/44"),
    ArrivingImperativeFigure("نسبةُ اللفيف", "31.8"),
    ArrivingImperativeFigure("المثالُ بهمزة وصل", "0/52"),
    ArrivingImperativeFigure("الأجوفُ بهمزة وصل", "0/421"),
    ArrivingImperativeFigure("فارقُ السالم والأجوف بالنقاط", "96.9"),
    ArrivingImperativeFigure("احتمالُ الفارق", "0.0000"),
    ArrivingImperativeFigure("حجمُ عيّنة السالم والأجوف", "838"),
    ArrivingImperativeFigure("جذورٌ لها أمرٌ ومضارع", "217/258"),
    ArrivingImperativeFigure("نسبةُ ما له أمرٌ ومضارع", "84.1"),
    ArrivingImperativeFigure("جذورٌ لها أمرٌ بلا مضارع", "41"),
    ArrivingImperativeFigure("نسبةُ ما له أمرٌ بلا مضارع", "15.9"),
    ArrivingImperativeFigure("استثناءاتُ السالم", "13"),
    ArrivingImperativeFigure("استثناءاتُ الناقص", "1"),
)
"""الأرقامُ الواردةُ بنصّها؛ ومطابقتُها أو مخالفتُها تُعرَض في وحدة القياس."""


WHAT_THIS_SPECIFICATION_EXPECTS: Final[str] = (
    "WhatThisSpecificationExpects: المُصرَّحُ به — وقد رُئي الرقمُ قبل الصوغ، "
    "فليس تنبّؤًا — ثلاثةُ أمور. **أوّلًا**: صفرُ الأجوف وصفرُ المثال ثابتان "
    "تحت القواعد الأربع جميعًا، فهما خبرٌ عن البايتات لا عن القاعدة. "
    "**ثانيًا**: نسبةُ السالم تتبدّل تبدّلًا كبيرًا بتبدّل القاعدة، فرقمُها "
    "الواحدُ المنزوعُ من قاعدته دعوى لا قياس. **ثالثًا**: المضاعفُ يُقسَم "
    "داخلَه بالإدغام والفكّ، وهو اختبارُ الآليّة نفسِها داخل صنفٍ واحد، فإن "
    "صدَق فيه فذاك أقوى من ارتباطٍ بين صنفين"
)


def specification_digest() -> str:
    """بصمةُ محتوى المواصفة؛ فحذفُ قاعدةٍ أو تبديلُ بذرةٍ تُغيّرها."""

    return canonical_digest(
        canonical_bytes(
            {
                "standing": STANDING.value,
                "wasl_character": WASL_CHARACTER,
                "root_shapes": [shape.value for shape in RootShape],
                "weakness_rules": [
                    [
                        rule.name,
                        list(rule.weak_letters),
                        rule.separates_the_doubled_root,
                        rule.what_it_assumes,
                    ]
                    for rule in WEAKNESS_RULES
                ],
                "permutation_protocol": {
                    "statistic": PERMUTATION_PROTOCOL.statistic,
                    "permutations": PERMUTATION_PROTOCOL.permutations,
                    "seed": PERMUTATION_PROTOCOL.seed,
                    "generator": PERMUTATION_PROTOCOL.generator,
                    "p_value_formula": PERMUTATION_PROTOCOL.p_value_formula,
                },
                "arriving_figures": [
                    [item.label, item.claimed_value]
                    for item in ARRIVING_IMPERATIVE_FIGURES
                ],
                "expectation": WHAT_THIS_SPECIFICATION_EXPECTS,
            }
        )
    )


IMPERATIVE_WASL_SPECIFICATION_DIGEST: Final[str] = (
    "994d8b9e837bc5659de5d36004254a214c3e1cdab72ba41645bf6cfdc70e6e23"
)
"""البصمةُ المُجمَّدة؛ وحارسُ الاستيراد يرفض أيّ تبديلٍ صامتٍ بعد التجميد."""


_FORBIDDEN_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "outcome",
    "result",
    "observed",
    "measured",
    "rederived",
    "verdict",
    "birth",
)


def _assert_no_outcome_field() -> None:
    for dataclass_type in (WeaknessRule, PermutationProtocol, ArrivingImperativeFigure):
        for field in fields(dataclass_type):
            for word in field.name.split("_"):
                if word in _FORBIDDEN_FIELD_MARKERS:
                    raise ImperativeWaslSpecificationError(
                        f"`{field.name}` حقلُ نتيجةٍ في وحدةِ تجميد؛ والنتيجةُ "
                        f"تُقاس في موضعها لا تُودَع هنا."
                    )


def _assert_the_rules_are_four_and_distinct() -> None:
    names = [rule.name for rule in WEAKNESS_RULES]
    if len(set(names)) != len(names):
        raise ImperativeWaslSpecificationError(
            "قاعدةٌ مكرّرةُ الاسم؛ والتكرارُ يُوهِم تعدُّدَ اختبارات."
        )
    signatures = {
        (tuple(sorted(rule.weak_letters)), rule.separates_the_doubled_root)
        for rule in WEAKNESS_RULES
    }
    if len(signatures) != len(WEAKNESS_RULES):
        raise ImperativeWaslSpecificationError(
            "قاعدتان بمضمونٍ واحد؛ وتكرارُ المضمون يُوهِم اتّساعَ الفحص."
        )
    if len(WEAKNESS_RULES) < 2:
        raise ImperativeWaslSpecificationError(
            "قاعدةٌ واحدةٌ لا تكشف تبعيةَ الرقم لقاعدته؛ فلا تُقبَل وحدَها."
        )


def _assert_the_standing_is_the_weaker_one() -> None:
    if STANDING is not SpecificationStanding.FORMULATED_AFTER_THE_NUMBER:
        raise ImperativeWaslSpecificationError(
            "منزلةُ هذه المواصفة `مُصاغة_بعد_الرقم`؛ ورفعُها إلى `سابقة_للدليل` "
            "بعد رؤية الرقم دعوى كاذبةٌ عن تاريخ القياس."
        )


def _assert_the_specification_is_frozen() -> None:
    current = specification_digest()
    if current != IMPERATIVE_WASL_SPECIFICATION_DIGEST:
        raise ImperativeWaslSpecificationError(
            f"بصمةُ المواصفة الآن {current}، والمُجمَّدةُ "
            f"{IMPERATIVE_WASL_SPECIFICATION_DIGEST}؛ فقد بُدِّل فيها شيءٌ بعد "
            "التجميد، ولا يُمرَّر التبديلُ بتحذير."
        )


_assert_no_outcome_field()
_assert_the_rules_are_four_and_distinct()
_assert_the_standing_is_the_weaker_one()
_assert_the_specification_is_frozen()
