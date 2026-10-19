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
    "IrabDifferenceClass",
    "THE_ANCHOR_IS_READ_BEFORE_THE_FIGURES_NOTE",
    "A_DIFFERENCE_IS_CLASSIFIED_NOT_ABSORBED_NOTE",
    "ANCHOR_COLUMN_NAME",
    "ArrivingColumnCoverage",
    "SPELLING_CHECK_BESIDE_THE_EXPECTATION",
    "SECOND_CONSIGNMENT_IRAB_FIGURES",
    "INVARIABLE_DECLINABLE_COLUMN",
    "FIRST_CONSIGNMENT_IRAB_FIGURES",
    "CASE_MOOD_COLUMN",
    "A_TRANSMITTED_SPELLING_IS_NOT_THE_HEADER_NOTE",
    "A_THINLY_COVERED_COLUMN_IS_NOT_A_CENSUS_OF_ARABIC_NOTE",
    "A_COVERAGE_IS_NOT_A_COUNT_NOTE",
    "ARRIVING_SEGMENT_TOTAL",
    "ARRIVING_COLUMN_COVERAGE",
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

A_TRANSMITTED_SPELLING_IS_NOT_THE_HEADER_NOTE: Final[str] = (
    "ATransmittedSpellingIsNotTheHeader: وصلت الصياغةُ الحرفيّةُ للقيم فطابقت "
    "المُجمَّدَ هنا حرفًا حرفًا؛ وذلك يُثبِت موافقةَ المنقول للناقل لا موافقتَه "
    "للبايتات، فخطرُ «ليست من قيم هذا العمود» انخفض ولم يزل"
)

A_COVERAGE_IS_NOT_A_COUNT_NOTE: Final[str] = (
    "ACoverageIsNotACount: نسبةُ الامتلاء تُقارَن عند منازلها المُصرَّح بها "
    "وحدَها — ٨٤٫٤٥٪ منزلتان لا أربع — وضربُها في المقام لا يُخرِج عددًا "
    "مقيسًا بل مدًى عرضُه ألوفُ المقاطع؛ فالعددُ يُعَدُّ ولا يُشتَقُّ منها"
)

A_THINLY_COVERED_COLUMN_IS_NOT_A_CENSUS_OF_ARABIC_NOTE: Final[str] = (
    "AThinlyCoveredColumnIsNotACensusOfArabic: عمودٌ تغطيتُه ١٫٧٩٪ عددُه خبرٌ "
    "عمّا وُسِم فيه لا عمّا في القرآن؛ فـ«نائبُ فاعلٍ ٥٧» ليس عددَ المجهول، "
    "ولا يُقابَل بعددٍ من عمودٍ تغطيتُه ٧٦٪ ولا بعددٍ من مدوَّنةٍ أخرى"
)

A_CLAIMED_VALUE_ABSENT_IS_NOT_A_ZERO_COUNT_NOTE: Final[str] = (
    "AClaimedValueAbsentIsNotAZeroCount: قيمةٌ لم تَرِد في العمود البتّة "
    "جوابُها «ليست من قيم هذا العمود» لا «صفر»؛ فالصفرُ خبرٌ عن المدوَّنة، "
    "والغيابُ خبرٌ عن اسم القيمة قد يكون خطأَ نقلٍ أو اختلافَ صياغةٍ أو ترميز"
)

THE_ANCHOR_IS_READ_BEFORE_THE_FIGURES_NOTE: Final[str] = (
    "TheAnchorIsReadBeforeTheFigures: `Morph_type` وحدَه مُصرَّحٌ بامتلائه "
    "١٠٠٪، فيُقرأ **قبل** رقمٍ من أرقام الإعراب؛ فإن خالف فالمُتَّهَمُ "
    "القراءةُ نفسُها — تقطيعُ السجلّات أو أسطرٌ مضمَّنةٌ في حقلٍ مقتبَس — لا "
    "الأرقامُ المُجمَّدة، وقراءةُ فرقٍ في رقمٍ حينئذٍ قراءةُ عطبٍ في الأنبوب"
)

A_DIFFERENCE_IS_CLASSIFIED_NOT_ABSORBED_NOTE: Final[str] = (
    "ADifferenceIsClassifiedNotAbsorbed: إن خالف رقمٌ فلا يُعدَّل المُجمَّدُ "
    "ولا قاعدةُ عدِّه حتّى يُطابِق؛ يُسجَّل الفرقُ كما هو ويُصنَّف بـ"
    "`IrabDifferenceClass` المسنونةِ **قبل رؤيته**: خلافُ قاعدةِ عدٍّ، أو "
    "خلافُ اسم قيمةٍ، أو خلافٌ في البايتات نفسِها، أو لم يُصنَّف بعد — "
    "و«لم يُصنَّف» بابٌ مُعلَنٌ كي لا يُدفَع فرقٌ إلى بابٍ لا يسعه"
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
    "ATransmittedSpellingIsNotTheHeader": (
        A_TRANSMITTED_SPELLING_IS_NOT_THE_HEADER_NOTE
    ),
    "ACoverageIsNotACount": A_COVERAGE_IS_NOT_A_COUNT_NOTE,
    "AThinlyCoveredColumnIsNotACensusOfArabic": (
        A_THINLY_COVERED_COLUMN_IS_NOT_A_CENSUS_OF_ARABIC_NOTE
    ),
    "TheAnchorIsReadBeforeTheFigures": THE_ANCHOR_IS_READ_BEFORE_THE_FIGURES_NOTE,
    "ADifferenceIsClassifiedNotAbsorbed": (
        A_DIFFERENCE_IS_CLASSIFIED_NOT_ABSORBED_NOTE
    ),
}


SYNTACTIC_ROLE_COLUMN: Final[str] = "Syntactic_Role"
CASE_MOOD_COLUMN: Final[str] = "Case_Mood"
CASE_MOOD_MARKER_COLUMN: Final[str] = "Case_Mood_Marker"
INVARIABLE_DECLINABLE_COLUMN: Final[str] = "Invariable_Declinable"
PHRASAL_FUNCTION_COLUMN: Final[str] = "Phrasal_Function"
SEGMENT_INDEX_COLUMN_NAME: Final[str] = "Word_No"
WORD_KEY_COLUMN_NAME: Final[str] = "Column5"
ANCHOR_COLUMN_NAME: Final[str] = "Morph_type"
"""العمودُ المُصرَّحُ بامتلائه ١٠٠٪؛ وهو المرساةُ لا رقمٌ من أرقام الإعراب."""


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
    NON_EMPTY_COLUMN_CELLS = (
        "الخليةُ المملوءة: سجلٌّ قيمةُ عموده المُعلَن غيرُ فارغةٍ بعد تجريد "
        "الفراغ الطرفيّ، منسوبًا إلى جملة السجلّات؛ والمقامُ مقاطعُ الملفِّ "
        "كلُّها لا المُعرَبُ منها وحدَه"
    )


class IrabDifferenceClass(Enum):
    """أبوابُ الفرق، مسنونةً **قبل رؤيته**؛ ولا يُفتَح بابٌ بعد وقوعه.

    `ADifferenceIsClassifiedNotAbsorbed`: التصنيفُ تسجيلٌ للفرق لا مَعذِرةٌ
    له، ولا يُعدَّل به رقمٌ مُجمَّدٌ ولا قاعدةُ عدّ.
    """

    COUNTING_RULE = (
        "خلافُ قاعدةِ عدٍّ: وردت القيمةُ وخالف عددُ المقاطع، وعددُ الكلمات "
        "بالثلاثيّة `(Sura_No، Verse_No، Column5)` هو المطابقُ للمُدَّعى؛ "
        "فالمُدَّعى عُدَّ بالكلمة والمقيسُ بالمقطع، والوحدتان اثنتان"
    )
    VALUE_NAME = (
        "خلافُ اسم قيمةٍ: لم تَرِد الصورةُ المُجمَّدةُ في العمود البتّة، "
        "فالخبرُ عن **اسم القيمة** — تشكيلًا أو مسافةً أو صورةَ همزةٍ أو "
        "ترميزًا — لا عن المدوَّنة؛ ولا يُقرأ صفرًا ولا تكذيبًا للرقم"
    )
    THE_BYTES_THEMSELVES = (
        "خلافٌ في البايتات أو في قراءتها: مرساةُ `Morph_type` لم تكتمل أو "
        "جملةُ السجلّات خالفت، فالمُتَّهَمُ الأنبوبُ لا الأرقام؛ ولا يُصنَّف "
        "فرقٌ آخرُ ما دامت المرساةُ ساقطة"
    )
    NOT_YET_CLASSIFIED = (
        "لم يُصنَّف بعد: وردت القيمةُ وخالف عددُها ولم يُفسِّره عدُّ الكلمات، "
        "والمرساةُ قائمة؛ فيُسجَّل الفرقُ بلا بابٍ يسعه، ولا يُدفَع إلى بابٍ "
        "ليختفي"
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
        name=CASE_MOOD_COLUMN,
        arabic_name="بابُ الإعراب",
        what_it_annotates=(
            "حالَ الموضع لا علامتَها: مبنيٌّ ومرفوعٌ ومجرورٌ ومنصوبٌ ومجزوم، "
            "خمسُ قيمٍ لا سادسَ لها في هذه البايتات"
        ),
        what_it_does_not_annotate=(
            "العلامةَ نفسَها: تلك في `Case_Mood_Marker`، وتغطيةُ العمودين "
            "واحدةٌ فلا يُقرأ ذلك توكيدًا لأحدهما بالآخر"
        ),
    ),
    IrabColumn(
        name=INVARIABLE_DECLINABLE_COLUMN,
        arabic_name="البناءُ والإعراب",
        what_it_annotates=(
            "كونَ الكلمة مبنيّةً أو معربة، ومعهما أصنافُ المبنيّات: الضميرُ "
            "المتّصل، وألْ التعريف، والموصولُ، والإشارةُ، والشرطُ، والاستفهام"
        ),
        what_it_does_not_annotate=(
            "قسمةً مُطَّردةً بين قيمتين: «مبني» و«معرب» قيمتان من اثنتَي عشرةَ، "
            "وبقيّتُها أصنافٌ لا أقسامٌ، فلا يُجمَع بعضُها إلى بعضٍ مجموعًا"
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


FIRST_CONSIGNMENT_IRAB_FIGURES: Final[tuple[ArrivingIrabFigure, ...]] = (
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
"""ثلاثةَ عشرَ رقمًا كما وصلت أوّلَ مرّة، بقيمها المُصرَّح بها؛ ولا يُقرأ واحدٌ
منها مقيسًا هنا.

وصورةُ القيمة نفسُها **دعوى**: إن خالفت صياغةُ المُوسِّم ما كُتِب هنا خرج
الجوابُ «ليست من قيم هذا العمود» لا صفرًا، وذلك نصُّ
`AClaimedValueAbsentIsNotAZeroCount`.
"""


SECOND_CONSIGNMENT_IRAB_FIGURES: Final[tuple[ArrivingIrabFigure, ...]] = (
    ArrivingIrabFigure(
        label="حرف جر — Syntactic_Role",
        column=SYNTACTIC_ROLE_COLUMN,
        value="حرف جر",
        claimed_count=13_034,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="اسم مجرور — Syntactic_Role",
        column=SYNTACTIC_ROLE_COLUMN,
        value="اسم مجرور",
        claimed_count=12_243,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="حرف غير عامل — Syntactic_Role",
        column=SYNTACTIC_ROLE_COLUMN,
        value="حرف غير عامل",
        claimed_count=9_999,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="حرف عطف — Syntactic_Role",
        column=SYNTACTIC_ROLE_COLUMN,
        value="حرف عطف",
        claimed_count=8_909,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="فعل مضارع — Syntactic_Role",
        column=SYNTACTIC_ROLE_COLUMN,
        value="فعل مضارع",
        claimed_count=7_527,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="فعل ماضٍ — Syntactic_Role",
        column=SYNTACTIC_ROLE_COLUMN,
        value="فعل ماضٍ",
        claimed_count=7_321,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="قيمُ باب الإعراب المتمايزة",
        column=CASE_MOOD_COLUMN,
        value=None,
        claimed_count=5,
        counting_rule=IrabCountingRule.DISTINCT_COLUMN_VALUES,
    ),
    ArrivingIrabFigure(
        label="مبني — Case_Mood",
        column=CASE_MOOD_COLUMN,
        value="مبني",
        claimed_count=53_687,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="مرفوع — Case_Mood",
        column=CASE_MOOD_COLUMN,
        value="مرفوع",
        claimed_count=27_015,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="مجرور — Case_Mood",
        column=CASE_MOOD_COLUMN,
        value="مجرور",
        claimed_count=23_255,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="منصوب — Case_Mood",
        column=CASE_MOOD_COLUMN,
        value="منصوب",
        claimed_count=19_327,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="مجزوم — Case_Mood",
        column=CASE_MOOD_COLUMN,
        value="مجزوم",
        claimed_count=1_490,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="السكون — Case_Mood_Marker",
        column=CASE_MOOD_MARKER_COLUMN,
        value="السكون",
        claimed_count=43_056,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="الفتحة — Case_Mood_Marker",
        column=CASE_MOOD_MARKER_COLUMN,
        value="الفتحة",
        claimed_count=39_700,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="الكسرة — Case_Mood_Marker",
        column=CASE_MOOD_MARKER_COLUMN,
        value="الكسرة",
        claimed_count=16_953,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="الضمة — Case_Mood_Marker",
        column=CASE_MOOD_MARKER_COLUMN,
        value="الضمة",
        claimed_count=13_668,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="قيمُ وظيفة التركيب المتمايزة",
        column=PHRASAL_FUNCTION_COLUMN,
        value=None,
        claimed_count=9,
        counting_rule=IrabCountingRule.DISTINCT_COLUMN_VALUES,
    ),
    ArrivingIrabFigure(
        label="خبر — Phrasal_Function",
        column=PHRASAL_FUNCTION_COLUMN,
        value="خبر",
        claimed_count=1_398,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="خبر حرف ناسخ — Phrasal_Function",
        column=PHRASAL_FUNCTION_COLUMN,
        value="خبر حرف ناسخ",
        claimed_count=783,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="خبر فعل ناسخ — Phrasal_Function",
        column=PHRASAL_FUNCTION_COLUMN,
        value="خبر فعل ناسخ",
        claimed_count=551,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="خبر لا النافية للجنس — Phrasal_Function",
        column=PHRASAL_FUNCTION_COLUMN,
        value="خبر لا النافية للجنس",
        claimed_count=34,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="حال — Phrasal_Function",
        column=PHRASAL_FUNCTION_COLUMN,
        value="حال",
        claimed_count=4,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="بدل — Phrasal_Function",
        column=PHRASAL_FUNCTION_COLUMN,
        value="بدل",
        claimed_count=1,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="فاعل — Phrasal_Function",
        column=PHRASAL_FUNCTION_COLUMN,
        value="فاعل",
        claimed_count=1,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="نعت — Phrasal_Function",
        column=PHRASAL_FUNCTION_COLUMN,
        value="نعت",
        claimed_count=1,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="قيمُ البناء والإعراب المتمايزة",
        column=INVARIABLE_DECLINABLE_COLUMN,
        value=None,
        claimed_count=12,
        counting_rule=IrabCountingRule.DISTINCT_COLUMN_VALUES,
    ),
    ArrivingIrabFigure(
        label="مبني — Invariable_Declinable",
        column=INVARIABLE_DECLINABLE_COLUMN,
        value="مبني",
        claimed_count=54_734,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="معرب — Invariable_Declinable",
        column=INVARIABLE_DECLINABLE_COLUMN,
        value="معرب",
        claimed_count=39_509,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="ضمير متصل — Invariable_Declinable",
        column=INVARIABLE_DECLINABLE_COLUMN,
        value="ضمير متصل",
        claimed_count=23_579,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="ال التعريف — Invariable_Declinable",
        column=INVARIABLE_DECLINABLE_COLUMN,
        value="ال التعريف",
        claimed_count=8_372,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="اسم موصول — Invariable_Declinable",
        column=INVARIABLE_DECLINABLE_COLUMN,
        value="اسم موصول",
        claimed_count=3_242,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="ضمير منفصل مبني — Invariable_Declinable",
        column=INVARIABLE_DECLINABLE_COLUMN,
        value="ضمير منفصل مبني",
        claimed_count=1_265,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="اسم إشارة — Invariable_Declinable",
        column=INVARIABLE_DECLINABLE_COLUMN,
        value="اسم إشارة",
        claimed_count=1_071,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="اسم شرط — Invariable_Declinable",
        column=INVARIABLE_DECLINABLE_COLUMN,
        value="اسم شرط",
        claimed_count=833,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="اسم استفهام — Invariable_Declinable",
        column=INVARIABLE_DECLINABLE_COLUMN,
        value="اسم استفهام",
        claimed_count=417,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
    ArrivingIrabFigure(
        label="ضمير فصل — Invariable_Declinable",
        column=INVARIABLE_DECLINABLE_COLUMN,
        value="ضمير فصل",
        claimed_count=125,
        counting_rule=IrabCountingRule.SEGMENTS_WITH_VALUE,
    ),
)
"""الدُّفعةُ الثانيةُ كما وصلت بصياغتها الحرفيّة، ومعها عمودان لم يكونا مُعلَنين.

ومنزلتُها منزلةُ الأولى سواءً: `TheFiguresArrivedFromTheHolderOfTheBytes` يشملها،
فوصولُ الصياغة الحرفيّةِ رفعَ احتمالَ خطأِ النقل ولم يجعل الرقمَ مقيسًا هنا.
"""


ARRIVING_IRAB_FIGURES: Final[tuple[ArrivingIrabFigure, ...]] = (
    FIRST_CONSIGNMENT_IRAB_FIGURES + SECOND_CONSIGNMENT_IRAB_FIGURES
)
"""الدُّفعتان مجموعتين؛ وكلُّ رقمٍ فيهما دعوًى حتى يُعادَ اشتقاقُه من البايتات."""


ARRIVING_SEGMENT_TOTAL: Final[int] = 157_677
"""جملةُ المقاطع كما وصلت: مقامُ كلِّ نسبةِ تغطيةٍ أدناه.

ووصل أنّ `Morph_type` مملوءٌ في ١٠٠٪ منها، فهو المرساةُ الوحيدةُ المكتملة؛
وهذا العددُ نفسُه يُعاد اشتقاقُه سجلًّا سجلًّا، فلا يُؤخَذ من النسبة.
"""


@dataclass(frozen=True, slots=True)
class ArrivingColumnCoverage:
    """نسبةُ امتلاء عمودٍ كما وصلت، بدقّتها المُصرَّح بها لا بأكثرَ منها."""

    column: str
    declared_percentage: str

    def __post_init__(self) -> None:
        if not isinstance(self.column, str) or not self.column.strip():
            raise IrabPreregistrationError("اسمُ العمود نصٌّ غير فارغ.")
        if not isinstance(self.declared_percentage, str):
            raise IrabPreregistrationError("النسبةُ تُحفَظ بنصِّها لا بعائمٍ يُقرَّب.")
        try:
            value = float(self.declared_percentage)
        except ValueError as error:
            raise IrabPreregistrationError(
                f"نسبةٌ لا تُقرأ عددًا: {self.declared_percentage}"
            ) from error
        if not 0.0 <= value <= 100.0:
            raise IrabPreregistrationError("النسبةُ بين صفرٍ ومئة.")
        if "." not in self.declared_percentage:
            raise IrabPreregistrationError(
                "تُكتَب النسبةُ بمنازلها العشرية كما وصلت، فبها تُعرَف دقّةُ "
                "المقارنة؛ ونسبةٌ بلا منازلَ تُقارَن بدقّةٍ لم تُصرَّح."
            )

    @property
    def decimal_places(self) -> int:
        """عددُ المنازل المُصرَّح بها؛ وعندها تقف المقارنةُ ولا تتجاوزها."""

        return len(self.declared_percentage.split(".")[1])


ARRIVING_COLUMN_COVERAGE: Final[tuple[ArrivingColumnCoverage, ...]] = (
    ArrivingColumnCoverage(column=ANCHOR_COLUMN_NAME, declared_percentage="100.0000"),
    ArrivingColumnCoverage(column="Segmented_Word", declared_percentage="98.2553"),
    ArrivingColumnCoverage(column="Morph_tag", declared_percentage="98.2039"),
    ArrivingColumnCoverage(
        column=INVARIABLE_DECLINABLE_COLUMN, declared_percentage="84.45"
    ),
    ArrivingColumnCoverage(column="Possessive_Construct", declared_percentage="79.14"),
    ArrivingColumnCoverage(column=CASE_MOOD_COLUMN, declared_percentage="79.13"),
    ArrivingColumnCoverage(column=CASE_MOOD_MARKER_COLUMN, declared_percentage="79.13"),
    ArrivingColumnCoverage(column=SYNTACTIC_ROLE_COLUMN, declared_percentage="76.3631"),
    ArrivingColumnCoverage(column="Phrase", declared_percentage="1.80"),
    ArrivingColumnCoverage(column=PHRASAL_FUNCTION_COLUMN, declared_percentage="1.79"),
)
"""تغطيةُ الأعمدة العشرةِ كما وصلت؛ وأربعةٌ منها ليست من أعمدة الإعراب الخمسة.

وهي مُودَعةٌ لأنّها تحسم ما لا يحسمه العدُّ وحدَه: «نائبُ فاعلٍ ٥٧» في عمودٍ
تغطيتُه ١٫٧٩٪ ليس ٥٧ مجهولًا في القرآن، بل ٥٧ ممّا وُسِم في جزءٍ من مئةٍ من
المقاطع؛ ومن قرأه الأوّلَ قرأ عمودًا شبهَ خالٍ خبرًا عن العربية.
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


SPELLING_CHECK_BESIDE_THE_EXPECTATION: Final[str] = (
    "SpellingCheckBesideTheExpectation: بعد صوغ `PRE_REGISTERED_EXPECTATION` "
    "وصلت الصياغةُ الحرفيّةُ للقيم، فقُوبِلت بالمُجمَّد هنا فطابقته في القيم "
    "الثلاثَ عشرةَ كلِّها. ولم يُعدَّل نصُّ التوقّع: تعديلُه بعد بلوغ الخبر "
    "يمحو ما كان يُقاس به. فيُكتَب الفحصُ إلى جانبه لا مكانَه، وحدُّ ما "
    "يُثبِته في " + A_TRANSMITTED_SPELLING_IS_NOT_THE_HEADER_NOTE
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
                "segment_total": ARRIVING_SEGMENT_TOTAL,
                "column_coverage": [
                    [coverage.column, coverage.declared_percentage]
                    for coverage in ARRIVING_COLUMN_COVERAGE
                ],
                "difference_classes": {
                    item.name: item.value for item in IrabDifferenceClass
                },
                "anchor_column": ANCHOR_COLUMN_NAME,
                "expectation": PRE_REGISTERED_EXPECTATION,
                "spelling_check": SPELLING_CHECK_BESIDE_THE_EXPECTATION,
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

    for dataclass_type in (IrabColumn, ArrivingIrabFigure, ArrivingColumnCoverage):
        for field in fields(dataclass_type):
            lowered = field.name.lower()
            for marker in _FORBIDDEN_FIELD_MARKERS:
                if marker in lowered:
                    raise RuntimeError(
                        f"{dataclass_type.__name__}.{field.name} حقلٌ ممنوع: "
                        "هذه وحدةُ تجميدٍ قبل القياس. "
                        + THIS_REGISTRATION_IS_NOT_PRIOR_TO_THE_NUMBER_NOTE
                    )


def _assert_the_two_consignments_do_not_overlap() -> None:
    """احرسْ ألّا تُعادَ دفعةٌ في الأخرى: إعادةُ رقمٍ تُوهِم وصولَه مرّتين."""

    first = {
        (figure.column, figure.value, figure.counting_rule.name)
        for figure in FIRST_CONSIGNMENT_IRAB_FIGURES
    }
    for figure in SECOND_CONSIGNMENT_IRAB_FIGURES:
        key = (figure.column, figure.value, figure.counting_rule.name)
        if key in first:
            raise RuntimeError(
                f"{figure.label} وصل في الدُّفعتين؛ والتكرارُ يُوهِم شاهدين. "
                + THE_FIGURES_ARRIVED_FROM_THE_HOLDER_OF_THE_BYTES_NOTE
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
    covered = [coverage.column for coverage in ARRIVING_COLUMN_COVERAGE]
    if len(set(covered)) != len(covered):
        raise RuntimeError("عمودٌ بنسبتَي تغطية؛ فلا يُعرَف أيُّهما تُقارَن به.")


_assert_no_outcome_field()
_assert_the_columns_and_figures_are_distinct()
_assert_the_two_consignments_do_not_overlap()
