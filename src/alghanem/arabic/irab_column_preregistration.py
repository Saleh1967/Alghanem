"""تجميدُ أعمدة الإعراب في MASAQ وأرقامِها الواردة قبل إعادة اشتقاقها.

**السؤالُ الذي وُضِعت له هذه الوحدة**: وصل أنّ MASAQ ليست وَسْمًا صرفيًّا
فحسب، بل تحمل **إعرابًا موسومًا** في ثلاثة أعمدة: `Syntactic_Role` بستّةٍ
وستّين قيمة، و`Case_Mood_Marker` بأربعَ عشرةَ علامة، و`Phrasal_Function`.
ووصلت معها ثلاثةَ عشرَ رقمًا: فاعل ١٠٬٤٨٣، ومفعولٌ به ٨٬٨٧٨، ومضافٌ إليه
٩٬١٢٣، ومبتدأٌ ٣٬٥٩٨، وثبوتُ النون ٢٬٦١١، وحذفُها ١٬٩١٣، والياءُ ١٬٨٨٤،
والواوُ ٧٢٣، وضمّةٌ مقدَّرةٌ ١٬٦٣٢، وفتحةٌ مقدَّرةٌ ١٬٤٠٤، ونائبُ فاعلٍ ٥٧.
والرقمُ لا يُقرأ قياسًا ما لم يحمل **قاعدةَ عدِّه** و**حدَّ ما يُثبِته**؛
فيُجمَّد هنا، ويقع القياسُ في `irab_column_census`.

`THIS_REGISTRATION_IS_NOT_PRIOR_TO_THE_NUMBER`: وصلت الأرقامُ قبل هذه القواعد،
فمنزلةُ التسجيل `مُصاغ_بعد_الرقم` كما في `masdar_priority_preregistration`. ومن
قرأ قواعدَه تنبّؤًا تحقّق قرأ ما لم يقع.

`THE_FIGURES_ARRIVED_FROM_THE_HOLDER_OF_THE_BYTES`: هذه الأرقامُ **قِيست عند
حائز البايتات لا في هذه الشجرة**. فالمُجمَّدُ هنا **دعوى رقمٍ** لا رقمٌ مقيس،
وتجميدُها ليس تصديقًا لها: هو تثبيتُ المُدَّعى كي يكون الفرقُ — إن وقع — قابلًا
للعرض بدل أن تُعدَّل القاعدةُ حتى تُطابق.

`A_COLUMN_NAME_IS_A_DECLARATION_UNTIL_THE_HEADER_IS_READ`: أسماءُ الأعمدة
الخمسةِ ودلالاتُها **تصريحُ حائز البايتات**، ولم تُقرأ ترويسةً في هذه الشجرة.
وعمودٌ غائبٌ عن الترويسة **يُوقِف العدَّ** في وحدة القياس ولا يُحمَل على أقرب
اسمٍ إليه، على منوال `AColumnBindingIsLegislatedNotRead`.

`AN_ANNOTATED_IRAB_IS_A_HUMAN_JUDGEMENT`: «فاعل» و«مفعول به» أحكامُ مُوسِّمٍ
بشرٍ على منهجٍ إعرابيٍّ بعينه، لا خواصُّ تُقاس من البايتات. فالعددُ عددُ
**ما وُسِم كذلك في هذه المدوَّنة**، وخلافُ النحاة في البابِ نفسِه لا يظهر في
العدّ ولا يُحسَم به.

`AN_ESTIMATED_MARKER_HAS_NO_WRITTEN_TRACE`: «ضمّةٌ مقدَّرة» و«فتحةٌ مقدَّرة»
حكمان على ما **لا أثرَ له في الرسم**؛ فهما أبعدُ من غيرهما عن المقيس: لا
يُعادُ اشتقاقُهما من صورة الكلمة البتّة، وإنّما يُعَدُّ وَسْمُهما. وهذا بابٌ
عجزت هذه الشجرة عن حسمه قبلُ، والعددُ **لا يحسمه**: يُحصي أحكامًا لا يُثبِت
تقديرًا.

`A_CLAIMED_VALUE_ABSENT_IS_NOT_A_ZERO_COUNT`: إن لم تَرِد القيمةُ المُدَّعاة
في العمود البتّة فالجوابُ **«ليست من قيم هذا العمود»** لا «صفر». والفرقُ
جوهريّ: الصفرُ خبرٌ عن المدوَّنة، والغيابُ خبرٌ عن **اسم القيمة** قد يكون
خطأً في النقل أو اختلافَ صياغةٍ أو ترميزٍ لا خبرًا عن العربية.

وهذه الوحدة تجميدٌ لا سلطة: لا ولادةَ فيها، ولا حكمَ ولادة، ولا تجميدَ `E0`،
ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه. ولا حقلَ نتيجةٍ فيها،
وحارسٌ في آخرها يرفض إضافتَه.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest

__all__ = [
    "ARRIVING_IRAB_FIGURES",
    "A_CLAIMED_VALUE_ABSENT_IS_NOT_A_ZERO_COUNT_NOTE",
    "A_COLUMN_NAME_IS_A_DECLARATION_UNTIL_THE_HEADER_IS_READ_NOTE",
    "AN_ANNOTATED_IRAB_IS_A_HUMAN_JUDGEMENT_NOTE",
    "AN_ESTIMATED_MARKER_HAS_NO_WRITTEN_TRACE_NOTE",
    "CASE_MOOD_MARKER_COLUMN",
    "IRAB_COLUMNS",
    "IRAB_PREREGISTRATION_DIGEST",
    "IRAB_PREREGISTRATION_NAMED_RESIDUALS",
    "PHRASAL_FUNCTION_COLUMN",
    "PRE_REGISTERED_EXPECTATION",
    "SEGMENT_INDEX_COLUMN_NAME",
    "STANDING",
    "SYNTACTIC_ROLE_COLUMN",
    "THE_FIGURES_ARRIVED_FROM_THE_HOLDER_OF_THE_BYTES_NOTE",
    "THIS_REGISTRATION_IS_NOT_PRIOR_TO_THE_NUMBER_NOTE",
    "WORD_KEY_COLUMN_NAME",
    "ArrivingIrabFigure",
    "IrabColumn",
    "IrabCountingRule",
    "IrabPreregistrationError",
    "RegistrationStanding",
    "column_named",
    "figures_for_column",
    "preregistration_digest",
]


class IrabPreregistrationError(ValueError):
    """تُرفَع حين يُوصَف عمودٌ أو رقمٌ وصفًا لا يُعاد به اشتقاقُه."""


class RegistrationStanding(Enum):
    """منزلةُ التسجيل؛ والقيمةُ الأقوى معلنةٌ ليُرى أنّ هذا ليس إيّاها."""

    PRIOR_TO_THE_NUMBER = "سابق_للرقم"
    FORMULATED_AFTER_THE_NUMBER = "مُصاغ_بعد_الرقم"


STANDING: Final[RegistrationStanding] = RegistrationStanding.FORMULATED_AFTER_THE_NUMBER
"""منزلةُ هذا التسجيل بعينه؛ وهي الأضعف، مُعلَنةً لا مُؤوَّلة."""


THIS_REGISTRATION_IS_NOT_PRIOR_TO_THE_NUMBER_NOTE: Final[str] = (
    "ThisRegistrationIsNotPriorToTheNumber: وصلت أرقامُ الإعراب قبل صوغ هذه "
    "القواعد، فمنزلةُ التسجيل `مُصاغ_بعد_الرقم`؛ ومن قرأه تنبّؤًا تحقّق قرأ "
    "ما لم يقع"
)

THE_FIGURES_ARRIVED_FROM_THE_HOLDER_OF_THE_BYTES_NOTE: Final[str] = (
    "TheFiguresArrivedFromTheHolderOfTheBytes: الأرقامُ الثلاثةَ عشرَ قِيست "
    "عند حائز البايتات لا في هذه الشجرة، فالمُجمَّدُ دعوى رقمٍ لا رقمٌ مقيس؛ "
    "وتجميدُها تثبيتُ المُدَّعى كي يُعرَض الفرقُ لا كي يُصدَّق"
)

A_COLUMN_NAME_IS_A_DECLARATION_UNTIL_THE_HEADER_IS_READ_NOTE: Final[str] = (
    "AColumnNameIsADeclarationUntilTheHeaderIsRead: أسماءُ الأعمدة ودلالاتُها "
    "تصريحُ حائز البايتات ولم تُقرأ ترويسةً هنا؛ وعمودٌ غائبٌ يُوقِف العدَّ "
    "ولا يُحمَل على أقرب اسمٍ إليه"
)

AN_ANNOTATED_IRAB_IS_A_HUMAN_JUDGEMENT_NOTE: Final[str] = (
    "AnAnnotatedIrabIsAHumanJudgement: «فاعل» و«مفعول به» أحكامُ مُوسِّمٍ بشرٍ "
    "على منهجٍ إعرابيٍّ بعينه لا خواصُّ تُقاس من البايتات؛ فالعددُ عددُ ما "
    "وُسِم كذلك، وخلافُ النحاة في البابِ نفسِه لا يظهر فيه ولا يُحسَم به"
)

AN_ESTIMATED_MARKER_HAS_NO_WRITTEN_TRACE_NOTE: Final[str] = (
    "AnEstimatedMarkerHasNoWrittenTrace: «ضمّةٌ مقدَّرة» و«فتحةٌ مقدَّرة» "
    "حكمان على ما لا أثرَ له في الرسم، فلا يُعادُ اشتقاقُهما من صورة الكلمة "
    "البتّة؛ والمعدودُ وَسْمُهما، والعددُ يُحصي أحكامًا ولا يُثبِت تقديرًا"
)

A_CLAIMED_VALUE_ABSENT_IS_NOT_A_ZERO_COUNT_NOTE: Final[str] = (
    "AClaimedValueAbsentIsNotAZeroCount: قيمةٌ لم تَرِد في العمود البتّة "
    "جوابُها «ليست من قيم هذا العمود» لا «صفر»؛ فالصفرُ خبرٌ عن المدوَّنة، "
    "والغيابُ خبرٌ عن اسم القيمة قد يكون خطأَ نقلٍ أو اختلافَ صياغةٍ أو ترميز"
)

IRAB_PREREGISTRATION_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "ThisRegistrationIsNotPriorToTheNumber": (
        THIS_REGISTRATION_IS_NOT_PRIOR_TO_THE_NUMBER_NOTE
    ),
    "TheFiguresArrivedFromTheHolderOfTheBytes": (
        THE_FIGURES_ARRIVED_FROM_THE_HOLDER_OF_THE_BYTES_NOTE
    ),
    "AColumnNameIsADeclarationUntilTheHeaderIsRead": (
        A_COLUMN_NAME_IS_A_DECLARATION_UNTIL_THE_HEADER_IS_READ_NOTE
    ),
    "AnAnnotatedIrabIsAHumanJudgement": AN_ANNOTATED_IRAB_IS_A_HUMAN_JUDGEMENT_NOTE,
    "AnEstimatedMarkerHasNoWrittenTrace": (
        AN_ESTIMATED_MARKER_HAS_NO_WRITTEN_TRACE_NOTE
    ),
    "AClaimedValueAbsentIsNotAZeroCount": (
        A_CLAIMED_VALUE_ABSENT_IS_NOT_A_ZERO_COUNT_NOTE
    ),
}


SYNTACTIC_ROLE_COLUMN: Final[str] = "Syntactic_Role"
CASE_MOOD_MARKER_COLUMN: Final[str] = "Case_Mood_Marker"
PHRASAL_FUNCTION_COLUMN: Final[str] = "Phrasal_Function"
SEGMENT_INDEX_COLUMN_NAME: Final[str] = "Word_No"
WORD_KEY_COLUMN_NAME: Final[str] = "Column5"


class IrabCountingRule(Enum):
    """قواعدُ العدّ بنصّها؛ ورقمٌ بلا واحدةٍ منها ليس عددًا."""

    DISTINCT_COLUMN_VALUES = (
        "القيمةُ المتمايزة: قيمةٌ غيرُ فارغةٍ بعد تجريد الفراغ الطرفيّ، "
        "متمايزةً **بالمطابقة الحرفيّة** لا بالاحتواء ولا بتطبيعٍ يُوحِّد "
        "صورتين؛ والقيمةُ الفارغةُ لا تُعَدُّ قيمةً ولا تُحمَل على غيرها"
    )
    SEGMENTS_WITH_VALUE = (
        "المقطعُ ذو القيمة: سجلٌّ في `csv` قيمةُ عموده المُعلَن **مطابقةٌ "
        "حرفيًّا** للقيمة المطلوبة؛ والوحدةُ المعدودةُ مقطعٌ لا كلمة، لأنّ "
        "`Word_No` فهرسُ مقطعٍ ومفتاحُ الكلمة `Column5`"
    )
    WORDS_WITH_VALUE = (
        "الكلمةُ ذاتُ القيمة: ثلاثيّةُ `(Sura_No، Verse_No، Column5)` متمايزةً "
        "ورد فيها مقطعٌ واحدٌ فأكثرُ بالقيمة المطلوبة؛ وهو غيرُ عدِّ المقاطع، "
        "ويُودَع معه ليُرى الفرقُ بدل أن يُقرأ أحدُهما مكان الآخر"
    )


@dataclass(frozen=True, slots=True)
class IrabColumn:
    """عمودٌ مُعلَنٌ: اسمُه، وما يَسِمه، وما لا يَسِمه، وحدُّ ما يُقرأ منه."""

    name: str
    arabic_name: str
    what_it_annotates: str
    what_it_does_not_annotate: str

    def __post_init__(self) -> None:
        for field in fields(self):
            value = getattr(self, field.name)
            if not isinstance(value, str) or not value.strip():
                raise IrabPreregistrationError(
                    f"{field.name} نصٌّ غير فارغ؛ وعمودٌ بلا حدٍّ مكتوبٍ "
                    "يُقرأ بعد جلساتٍ خاصّيّةً في العربية."
                )


IRAB_COLUMNS: Final[tuple[IrabColumn, ...]] = (
    IrabColumn(
        name=SYNTACTIC_ROLE_COLUMN,
        arabic_name="الوظيفةُ النحوية",
        what_it_annotates=(
            "بابَ الكلمة في الإعراب كما وسمه المُوسِّم: فاعلٌ ومفعولٌ به "
            "ومضافٌ إليه ومبتدأٌ وسواها"
        ),
        what_it_does_not_annotate=(
            "صوابَ الوَسْم ولا اتّفاقَ النحاة عليه: بابٌ مختلَفٌ فيه يظهر هنا "
            "بقيمةٍ واحدةٍ هي اختيارُ المُوسِّم. "
            + AN_ANNOTATED_IRAB_IS_A_HUMAN_JUDGEMENT_NOTE
        ),
    ),
    IrabColumn(
        name=CASE_MOOD_MARKER_COLUMN,
        arabic_name="علامةُ الإعراب",
        what_it_annotates=(
            "العلامةَ التي حُكِم بها على الموضع: أصليّةً كالضمّة، وفرعيّةً "
            "كثبوت النون وحذفها والياء والواو، ومقدَّرةً لا أثرَ لها في الرسم"
        ),
        what_it_does_not_annotate=(
            "أنّ العلامةَ مقروءةٌ من الرسم: المقدَّرةُ حكمٌ لا أثرَ له فيه. "
            + AN_ESTIMATED_MARKER_HAS_NO_WRITTEN_TRACE_NOTE
        ),
    ),
    IrabColumn(
        name=PHRASAL_FUNCTION_COLUMN,
        arabic_name="وظيفةُ التركيب",
        what_it_annotates=(
            "وظيفةَ الوحدة في تركيبها، ومنها «نائبُ فاعل» شاهدًا على المجهول "
            "موسومًا في هذه المدوَّنة وحدَها"
        ),
        what_it_does_not_annotate=(
            "مجهولًا مقيسًا في مدوَّنةٍ أخرى: «نائبُ فاعل» هنا غيرُ `PASS` في "
            "مدوَّنة القرآن الصرفية، ولا يُجمَع عددٌ من هذه إلى عددٍ من تلك"
        ),
    ),
    IrabColumn(
        name=SEGMENT_INDEX_COLUMN_NAME,
        arabic_name="فهرسُ المقطع",
        what_it_annotates=(
            "رتبةَ المقطع داخل كلمته؛ فهو الذي يجعل وحدةَ العدّ الافتراضيّةَ "
            "مقطعًا لا كلمة"
        ),
        what_it_does_not_annotate=(
            "رتبةَ الكلمة في آيتها: من قرأه فهرسَ كلمةٍ أهبط قياسَ محاذاةٍ من "
            "٢٣٫٣٪ إلى ٠٫٣٪ قبل أن يُمسَك"
        ),
    ),
    IrabColumn(
        name=WORD_KEY_COLUMN_NAME,
        arabic_name="مفتاحُ الكلمة",
        what_it_annotates=(
            "رتبةَ الكلمة في آيتها، وبه وحدَه تُجمَع مقاطعُ الكلمة الواحدة في " "عدِّ الكلمات"
        ),
        what_it_does_not_annotate=(
            "وجودَه في كلّ نسخةٍ من MASAQ: مرآةٌ عامّةٌ ببصمةٍ أخرى ليس فيها "
            "هذا العمود أصلًا، فالعدُّ بالكلمة موقوفٌ على ترويسة هذه البايتات. "
            + A_COLUMN_NAME_IS_A_DECLARATION_UNTIL_THE_HEADER_IS_READ_NOTE
        ),
    ),
)
"""الأعمدةُ الخمسةُ: ثلاثةٌ تحمل الإعراب، واثنان يُحدِّدان وحدةَ العدّ."""


def column_named(name: str) -> IrabColumn:
    """العمودُ باسمه؛ واسمٌ غيرُ مُعلَنٍ يُرفَع به خطأٌ لا يُتخطّى صامتًا."""

    for column in IRAB_COLUMNS:
        if column.name == name:
            return column
    raise IrabPreregistrationError(
        f"لا عمودَ مُعلَنًا بهذا الاسم: {name}؛ ولا يُعلَن عمودٌ بعد رؤية رقمه."
    )


@dataclass(frozen=True, slots=True)
class ArrivingIrabFigure:
    """رقمٌ وصل من حائز البايتات، مُجمَّدًا بقاعدةِ عدِّه قبل إعادة اشتقاقه.

    ولا يُقرأ إيداعُه تصديقًا: `TheFiguresArrivedFromTheHolderOfTheBytes`.
    """

    label: str
    column: str
    value: str | None
    claimed_count: int
    counting_rule: IrabCountingRule

    def __post_init__(self) -> None:
        for text, label in ((self.label, "اسمُ الرقم"), (self.column, "اسمُ العمود")):
            if not isinstance(text, str) or not text.strip():
                raise IrabPreregistrationError(f"{label} نصٌّ غير فارغ.")
        column_named(self.column)
        if not isinstance(self.counting_rule, IrabCountingRule):
            raise IrabPreregistrationError("لكلِّ رقمٍ قاعدةُ عدٍّ مُسمّاة.")
        if isinstance(self.claimed_count, bool) or not isinstance(
            self.claimed_count, int
        ):
            raise IrabPreregistrationError("العددُ المُدَّعى عددٌ صحيح.")
        if self.claimed_count < 0:
            raise IrabPreregistrationError("عددٌ مُدَّعًى لا يكون سالبًا.")
        if self.counting_rule is IrabCountingRule.DISTINCT_COLUMN_VALUES:
            if self.value is not None:
                raise IrabPreregistrationError(
                    "عدُّ القيم المتمايزة عدُّ عمودٍ كلِّه، فلا يُقيَّد بقيمة."
                )
        elif not isinstance(self.value, str) or not self.value.strip():
            raise IrabPreregistrationError(
                "عدُّ المقاطع ذواتِ القيمة لا يقوم بلا قيمةٍ مُصرَّحٍ بها."
            )


ARRIVING_IRAB_FIGURES: Final[tuple[ArrivingIrabFigure, ...]] = (
    ArrivingIrabFigure(
        label="قيمُ الوظيفة النحوية المتمايزة",
        column=SYNTACTIC_ROLE_COLUMN,
        value=None,
        claimed_count=66,
        counting_rule=IrabCountingRule.DISTINCT_COLUMN_VALUES,
    ),
    ArrivingIrabFigure(
        label="فاعل",
        column=SYNTACTIC_ROLE_COLUMN,
        value="فاعل",
        claimed_count=10_483,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="مفعولٌ به",
        column=SYNTACTIC_ROLE_COLUMN,
        value="مفعول به",
        claimed_count=8_878,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="مضافٌ إليه",
        column=SYNTACTIC_ROLE_COLUMN,
        value="مضاف إليه",
        claimed_count=9_123,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="مبتدأ",
        column=SYNTACTIC_ROLE_COLUMN,
        value="مبتدأ",
        claimed_count=3_598,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="علاماتُ الإعراب المتمايزة",
        column=CASE_MOOD_MARKER_COLUMN,
        value=None,
        claimed_count=14,
        counting_rule=IrabCountingRule.DISTINCT_COLUMN_VALUES,
    ),
    ArrivingIrabFigure(
        label="ثبوتُ النون",
        column=CASE_MOOD_MARKER_COLUMN,
        value="ثبوت النون",
        claimed_count=2_611,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="حذفُ النون",
        column=CASE_MOOD_MARKER_COLUMN,
        value="حذف النون",
        claimed_count=1_913,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="الياء",
        column=CASE_MOOD_MARKER_COLUMN,
        value="الياء",
        claimed_count=1_884,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="الواو",
        column=CASE_MOOD_MARKER_COLUMN,
        value="الواو",
        claimed_count=723,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="ضمّةٌ مقدَّرة",
        column=CASE_MOOD_MARKER_COLUMN,
        value="ضمة مقدرة",
        claimed_count=1_632,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="فتحةٌ مقدَّرة",
        column=CASE_MOOD_MARKER_COLUMN,
        value="فتحة مقدرة",
        claimed_count=1_404,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="نائبُ فاعل",
        column=PHRASAL_FUNCTION_COLUMN,
        value="نائب فاعل",
        claimed_count=57,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
)
"""ثلاثةَ عشرَ رقمًا كما وصلت، بقيمها المُصرَّح بها؛ ولا يُقرأ واحدٌ منها مقيسًا هنا.

وصورةُ القيمة نفسُها **دعوى**: إن خالفت صياغةُ المُوسِّم ما كُتِب هنا خرج
الجوابُ «ليست من قيم هذا العمود» لا صفرًا، وذلك نصُّ
`AClaimedValueAbsentIsNotAZeroCount`.
"""


def figures_for_column(name: str) -> tuple[ArrivingIrabFigure, ...]:
    """الأرقامُ الواردةُ لعمودٍ بعينه؛ واسمٌ غيرُ مُعلَنٍ يُرفَع به خطأ."""

    column_named(name)
    return tuple(figure for figure in ARRIVING_IRAB_FIGURES if figure.column == name)


PRE_REGISTERED_EXPECTATION: Final[str] = (
    "PreRegisteredExpectation: المُصرَّحُ به — وقد وصلت الأرقامُ قبل الصوغ، "
    "فليس تنبّؤًا — ثلاثةُ أمور. **أوّلًا**: يُتوقَّع أن تُطابِق أعدادُ "
    "المقاطع إن طابقت صياغةُ القيم حرفيًّا، وأن يخرج «ليست من قيم هذا العمود» "
    "لواحدةٍ فأكثرَ إن اختلفت الصياغةُ في التشكيل أو المسافة أو صورة الهمزة؛ "
    "والثاني ليس تكذيبًا للرقم بل تكذيبٌ لاسم قيمته. **ثانيًا**: يُتوقَّع أن "
    "يخالف عدُّ الكلمات عدَّ المقاطع في القيم كلِّها أو أكثرِها، لأنّ الوحدةَ "
    "مقطعٌ لا كلمة؛ ولذلك أُودِعت القاعدتان معًا. **ثالثًا**: لا يُتوقَّع من "
    "«ضمّةٍ مقدَّرة» و«فتحةٍ مقدَّرة» أن تحسما بابَ المقدَّر: عددُهما إحصاءُ "
    "أحكامٍ، والحسمُ يحتاج قاعدةً تُسَنّ لا عددًا يُقرأ"
)


def preregistration_digest() -> str:
    """بصمةُ محتوى التسجيل؛ فزيادةُ رقمٍ أو تبديلُ قيمةٍ تُغيّرها."""

    return canonical_digest(
        canonical_bytes(
            {
                "standing": STANDING.value,
                "counting_rules": {rule.name: rule.value for rule in IrabCountingRule},
                "columns": [
                    [
                        column.name,
                        column.arabic_name,
                        column.what_it_annotates,
                        column.what_it_does_not_annotate,
                    ]
                    for column in IRAB_COLUMNS
                ],
                "arriving_figures": [
                    [
                        figure.label,
                        figure.column,
                        figure.value if figure.value is not None else "",
                        figure.claimed_count,
                        figure.counting_rule.name,
                    ]
                    for figure in ARRIVING_IRAB_FIGURES
                ],
                "expectation": PRE_REGISTERED_EXPECTATION,
                "residuals": sorted(IRAB_PREREGISTRATION_NAMED_RESIDUALS),
            }
        )
    )


IRAB_PREREGISTRATION_DIGEST: Final[str] = preregistration_digest()
"""بصمةُ التسجيل مُشتقّةً من محتواه؛ ولا تُكتَب بيدٍ فتُصادِق على ما لم يُبصَّم."""


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
    """احرسْ خلوَّ وحدة التجميد من حقلِ نتيجةٍ أو مُخرَجٍ مقيس."""

    for dataclass_type in (IrabColumn, ArrivingIrabFigure):
        for field in fields(dataclass_type):
            lowered = field.name.lower()
            for marker in _FORBIDDEN_FIELD_MARKERS:
                if marker in lowered:
                    raise RuntimeError(
                        f"{dataclass_type.__name__}.{field.name} حقلٌ ممنوع: "
                        "هذه وحدةُ تجميدٍ قبل القياس. "
                        + THIS_REGISTRATION_IS_NOT_PRIOR_TO_THE_NUMBER_NOTE
                    )


def _assert_the_columns_and_figures_are_distinct() -> None:
    """احرسْ إفرادَ الأعمدة والأرقام: تكرارٌ في الاسم يُوهِم تعدُّدَ شواهد."""

    names = [column.name for column in IRAB_COLUMNS]
    if len(set(names)) != len(names):
        raise RuntimeError("عمودٌ مكرَّرُ الاسم؛ والتكرارُ يُوهِم قراءتين.")
    labels = [figure.label for figure in ARRIVING_IRAB_FIGURES]
    if len(set(labels)) != len(labels):
        raise RuntimeError("رقمٌ مكرَّرُ الاسم؛ فلا يُعرَف أيُّهما خالف.")
    keyed = [
        (figure.column, figure.value, figure.counting_rule.name)
        for figure in ARRIVING_IRAB_FIGURES
    ]
    if len(set(keyed)) != len(keyed):
        raise RuntimeError("رقمان بعمودٍ وقيمةٍ وقاعدةٍ واحدة؛ فهما رقمٌ قُرِئ مرّتين.")


_assert_no_outcome_field()
_assert_the_columns_and_figures_are_distinct()
