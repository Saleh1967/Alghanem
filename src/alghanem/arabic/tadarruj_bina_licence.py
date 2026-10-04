"""سُلَّمُ الترخيص المتدرِّج: لا تُرخَّص رتبةٌ حتّى تُستنفَد ما دونها.

الشرطُ المطلوبُ ههنا مسنونٌ قبل القياس: يُبدَأ بالمبنيّات، فتُرخَّص الأدواتُ،
ثمّ الأسماءُ المبنيّةُ — الضمائرُ منفصلةً ثمّ متّصلةً، ثمّ الإشارةُ، ثمّ
الموصولة — ثمّ يُوصَل بها الفعلُ الماضي مجرَّدًا ثمّ مزيدًا؛ **ولا يُنتقَل إلى
المعرَب قبل ترخيص ما دونه**. وبعد ذلك — وبعده وحدَه — يُقرَّر في «أعمل»
و«رجل».

وهذه الوحدةُ تُجري الشرطَ ولا تَحكيه. والمادّةُ المختومةُ `corpora/MASAQ.csv`
بوسمِها الصرفيِّ `Morph_tag` وعمودِها `Invariable_Declinable`، تُقرأ
بـ`masaq_corpus_deposit` التي تُطابِق الطولَ والبصمةَ قبل أن تُعيد بايتةً
واحدة؛ فإن غابت البايتاتُ **لم يخرج رقم**.

**أوّلًا: العمودُ سؤالان في خانةٍ واحدة، لا سؤالٌ واحد.**
`A_MIXED_COLUMN_IS_TWO_QUESTIONS_NOT_ONE`: في `Invariable_Declinable` أربعَ
عشرةَ قيمةً متمايزة، منها ما هو **حكم** (`مبني` · `معرب`)، ومنها ما هو **باب**
(`ضمير متصل` · `اسم موصول` · `اسم إشارة` · `اسم شرط` · `اسم استفهام` · `ضمير
منفصل مبني` · `ضمير فصل` · `ال التعريف` · `كافة ومكفوفة` · `اسم عدد مركب
مبني`). فمن قرأ العمودَ حكمًا ثنائيًّا وعدَّ خليّةَ `مبني` وحدَها أسقط ما
يقارب تسعةً وثلاثين ألفَ مقطعٍ مبنيٍّ كُتِب بابُها مكانَ حكمها. ولذلك تُصنَّف
كلُّ خليّةٍ أوّلًا بـ`cell_kind`، ولا يُقرَأ الحكمُ إلّا بعد تصنيفها.

**وثانيًا: الرتبةُ تُجرَد بوسمٍ مسنونٍ مُعدَّدٍ، لا بنمطٍ في اسم الوسم.**
`A_SUBSTRING_IN_A_TAG_NAME_IS_NOT_A_CLASS`: في المادّة `NOUN_ACTIVE_PART`
و`NOUN_PASSIVE_PART` — وهما اسمُ الفاعل واسمُ المفعول لا أداتان — ويقعان في
ثلاثة آلافٍ وستّمئةٍ وسبعةٍ وخمسين مقطعًا. فمن جرَد الأدواتِ بمطابقة `PART`
في اسم الوسم أدخل المشتقَّينِ في الحروف. ولذلك وسومُ كلّ رتبةٍ **مُعدَّدةٌ
بأعيانها** في `THE_RUNGS`، ولا تُجمَع بنمط.

**وثالثًا: الترخيصُ موافقةُ شاهدَين، والخلافُ ترخيصٌ ممنوعٌ لا تصويتُ أغلبيّة.**
`A_DISAGREEMENT_IS_A_WITHHELD_LICENCE_NOT_A_MAJORITY_VOTE`: لكلّ رتبةٍ حكمٌ
تدّعيه (`claimed_binding`)، والمقطعُ يُرخَّص حين يوافق عمودُ الحكم ما يدّعيه
وسمُه. وحيث خالفا لا يُحمَل أحدُهما على الآخر ولا يُؤخَذ بالأكثر: يُحصى
المخالفُ باسمه، ويبقى **غيرَ مُرخَّص**.

**ورابعًا: رتبةٌ لم تُستنفَد لا تُرخِّص ما فوقها.**
هذا `AN_UNEXHAUSTED_RUNG_LICENSES_NOTHING_ABOVE_IT` المسنونُ في
`mabni_generation_algebra`، يُستورَد ولا يُعاد صوغُه. والرتبةُ مستنفَدةٌ حين
**لا مخالفَ فيها البتّة**؛ فإن بقي مخالفٌ واحدٌ وقف السُّلَّمُ عندها، وكلُّ ما
فوقها `NOT_REACHED` — لا ناجحٌ ولا فاشلٌ سلوكيًّا، بل **لم يُبلَغ**.

**وخامسًا: المجرَّدُ والمزيدُ لا عمودَ لهما، فالرتبةُ موقوفةٌ لا مُجتهَدٌ فيها.**
`THE_BARE_AND_THE_AUGMENTED_PAST_HAVE_NO_COLUMN`: في ترويسة المادّة تسعةَ عشرَ
عمودًا ليس فيها جذرٌ ولا وزنٌ ولا صيغة. ففرزُ الماضي المجرَّدِ عن المزيد لا
مادّةَ له ههنا، وفرزُه بعدد الحروف هو بعينه الفرزُ بالصورة الذي نُقِض في
`A_SHAPE_THAT_CARRIES_SEVEN_HUNDRED_WORDS_SORTS_NOTHING`. فرتبةُ المزيد
`HAS_NO_COLUMN_IN_THE_MATERIAL`، وهذا وقفٌ مُسمًّى لا تقديرٌ ولا صفر.

**وسادسًا: وسمُ المُوسِّم خبرٌ عنه، لا ترخيصٌ منّا.**
`A_TAGGER_LABEL_IS_A_REPORT_NOT_OUR_LICENCE`: `report_on_word` تُخرِج لكلّ
كلمةٍ صفَّين منفصلَين لا يُدمَجان: ما قاله المُوسِّمُ — نقلًا بموضعٍ مختومٍ
يُعاد قراءتُه — وما رخَّصه سُلَّمُنا. فإن وقف السُّلَّمُ دون رتبتها كان
ترخيصُنا `NOT_REACHED` وإن كان وسمُ المُوسِّم جازمًا. وبهذا يُقرَّر في «أعمل»
و«رجل» بتقريرٍ لا بانتقالٍ مُتوهَّم.

**وسابعًا: السُّلَّمُ يقف عند رتبته الأولى، والسببُ مُسمًّى ومقيس.**
على المادّة المختومة، رتبةً رتبةً — (مقاطع · صورٌ متمايزة · مُرخَّص · مخالف ·
لا يُقرَأ):

| # | الرتبة | مقاطع | صور | مُرخَّص | مخالف | لا يُقرَأ |
|---|---|---|---|---|---|---|
| ١ | الأدواتُ والحروفُ الوظيفيّة | 46,336 | 61 | 43,697 | 18 | 2,621 |
| ٢ | الضمائرُ المنفصلة | 3,853 | 23 | 3,831 | 2 | 20 |
| ٣ | الضمائرُ المتّصلة | 20,792 | 41 | 19,770 | 16 | 1,006 |
| ٤ | أسماءُ الإشارة | 1,124 | 14 | 1,124 | 0 | 0 |
| ٥ | الأسماءُ الموصولة | 3,524 | 15 | 3,524 | 0 | 0 |
| ٦ | الفعلُ الماضي | 8,996 | 1,109 | 8,863 | 133 | 0 |
| ٧ | الماضي المزيدُ مفروزًا | — | — | — | — | — |
| ٨ | المعرَب | 26,353 | 2,252 | 23,798 | 2,555 | 0 |

فالوقوفُ عند **الرتبة الأولى**، ولم تُبلَغ رتبةٌ بعدها. وهذا ليس عيبًا في
التنفيذ، بل هو ما يقوله الشرطُ إذا أُخِذ على ظاهره.

وسببا الوقوف مُسمَّيان ومقيسان، وهما سببان لا سبب:

* `THE_ARTICLE_CELL_IS_FILLED_IN_SOME_ROWS_AND_BLANK_IN_OTHERS`: من المقاطع
  الـ2,621 التي لا تُقرَأ في الرتبة الأولى، **2,588** وسمُها `DET` وخانتُها
  خالية، بينما تُملأ في سائر مواضع `أل` بـ`ال التعريف`. فالخلوُّ ههنا ليس
  حكمًا بالإعراب ولا بالبناء، بل خانةٌ لم تُملأ؛ وحملُها على `معرب` يُفسِد
  القياس، وحملُها على `مبني` يُرخِّص ما لم يُقَس.
* ثمانيةَ عشرَ مقطعًا خالف فيها عمودُ الحكم وسمَه، أكثرُها «رب» سبعَ مرّاتٍ
  موسومةً `PREP` ومكتوبًا بإزائها `معرب`. وهذه زلّاتُ مُوسِّمٍ مفردةٌ
  تُحصى ولا تُصحَّح ههنا: تصحيحُها تعديلٌ للمادّة لا قراءةٌ لها.

والرتبةُ الثامنة لو بُلِغت لَما استُنفِدت: فيها 2,555 مقطعًا مخالفًا، 1,923
منها خانتُها `ضمير متصل` — أي أنّ المُوسِّمَ كتب **البابَ** مكانَ الحكم في
مقاطعَ وسمُها اسمٌ أو فعلٌ مضارع. وهذا هو الأوّلُ بعينه عائدًا في الرتبة
العليا.

**وثامنًا: «أعمل» و«رجل» يُقرَّر فيهما بتقرير، ولا يُنتقَل إليهما.**
كلتاهما واقعةٌ في الرتبة الثامنة، والسُّلَّمُ واقفٌ عند الأولى؛ فمنزلتُهما
عندنا `NOT_REACHED`. وما يقوله المُوسِّمُ فيهما — «أعمل» في ثمانية مقاطعَ،
أربعةٌ `IV` بإزائها `معرب` وأربعةٌ `IMPERF_PREF` بخانةٍ خالية؛ و«رجل» في
ثلاثةَ عشرَ مقطعًا كلُّها `NOUN_CONCRETE` بإزائها `معرب` — **خبرٌ عنه بموضعٍ
مختومٍ يُعاد قراءتُه**، لا ترخيصٌ منّا. فلا يُقال «فرَزَ سُلَّمُنا أنّهما
معربان»؛ يُقال: وقف سُلَّمُنا دونهما، ونقلنا عن المُوسِّم ما قال.

تسجيلٌ لا سلطة: لا ولادةَ ههنا ولا حكمَ ولادة ولا تجميدَ `E0`، ولا تستورد هذه
الوحدةُ من `kernel/` شيئًا.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Final

from .mabni_generation_algebra import (
    A_SHAPE_THAT_CARRIES_SEVEN_HUNDRED_WORDS_SORTS_NOTHING_NOTE,
    AN_UNEXHAUSTED_RUNG_LICENSES_NOTHING_ABOVE_IT_NOTE,
)
from .masaq_corpus_deposit import MASAQ_RELATIVE_PATH, MASAQ_SHA256

__all__ = [
    "AN_UNEXHAUSTED_RUNG_LICENSES_NOTHING_ABOVE_IT_NOTE",
    "A_DISAGREEMENT_IS_A_WITHHELD_LICENCE_NOT_A_MAJORITY_VOTE_NOTE",
    "A_MIXED_COLUMN_IS_TWO_QUESTIONS_NOT_ONE_NOTE",
    "A_SUBSTRING_IN_A_TAG_NAME_IS_NOT_A_CLASS_NOTE",
    "A_TAGGER_LABEL_IS_A_REPORT_NOT_OUR_LICENCE_NOTE",
    "BINDING_COLUMN",
    "Binding",
    "CellKind",
    "LadderReading",
    "Rung",
    "RungReading",
    "RungStanding",
    "SegmentRow",
    "TAG_COLUMN",
    "TADARRUJ_LICENCE_NAMED_RESIDUALS",
    "THE_BARE_AND_THE_AUGMENTED_PAST_HAVE_NO_COLUMN_NOTE",
    "THE_ARTICLE_CELL_IS_FILLED_IN_SOME_ROWS_AND_BLANK_IN_OTHERS_NOTE",
    "THE_DOOR_CELLS",
    "THE_LADDER_AT_MEASUREMENT",
    "THE_STOP_AT_MEASUREMENT",
    "THE_WORDS_DECIDED_AT_MEASUREMENT",
    "THE_JUDGEMENT_CELLS",
    "THE_RUNGS",
    "TadarrujLicenceError",
    "WordReport",
    "cell_kind",
    "ladder_reading",
    "licensing_stops_at",
    "reads_as",
    "report_on_word",
    "rung_named",
    "rung_reading",
]


class TadarrujLicenceError(ValueError):
    """رُفض مدخلٌ خارج السُّلَّم المسنون؛ لا يُحمَل على أقرب رتبةٍ إليه."""


TAG_COLUMN: Final[str] = "Morph_tag"
"""عمودُ الوسم الصرفيِّ في المادّة؛ منه تُجرَد الرتبة."""

BINDING_COLUMN: Final[str] = "Invariable_Declinable"
"""عمودُ البناء والإعراب في المادّة؛ به يُقابَل ما تدّعيه الرتبة."""

A_MIXED_COLUMN_IS_TWO_QUESTIONS_NOT_ONE_NOTE: Final[str] = (
    "AMixedColumnIsTwoQuestionsNotOne: خانةُ `Invariable_Declinable` تحمل "
    "حكمًا تارةً (`مبني`/`معرب`) وبابًا تارةً (`اسم موصول`...)، وهما سؤالان "
    "لا سؤال؛ فمن عدَّ خليّةَ `مبني` وحدَها أسقط كلَّ مبنيٍّ كُتِب بابُه "
    "مكانَ حكمه، ونقصانُ المقياس ههنا تسعةٌ وثلاثون ألفَ مقطعٍ تقريبًا"
)

A_SUBSTRING_IN_A_TAG_NAME_IS_NOT_A_CLASS_NOTE: Final[str] = (
    "ASubstringInATagNameIsNotAClass: `NOUN_ACTIVE_PART` و"
    "`NOUN_PASSIVE_PART` مشتقّان لا أداتان، وفيهما ثلاثة آلافٍ وستّمئةٍ "
    "وسبعةٌ وخمسون مقطعًا؛ فجردُ الأدوات بمطابقة `PART` في اسم الوسم يُدخِل "
    "المشتقَّينِ في الحروف. فالوسومُ مُعدَّدةٌ بأعيانها ولا تُجمَع بنمط"
)

A_DISAGREEMENT_IS_A_WITHHELD_LICENCE_NOT_A_MAJORITY_VOTE_NOTE: Final[str] = (
    "ADisagreementIsAWithheldLicenceNotAMajorityVote: حيث خالف عمودُ الحكم "
    "ما يدّعيه وسمُ الرتبة لا يُحمَل أحدُهما على الآخر ولا يُؤخَذ بالأكثر؛ "
    "يُحصى المخالفُ باسمه ويبقى المقطعُ غيرَ مُرخَّص"
)

THE_BARE_AND_THE_AUGMENTED_PAST_HAVE_NO_COLUMN_NOTE: Final[str] = (
    "TheBareAndTheAugmentedPastHaveNoColumn: ليس في أعمدة المادّة جذرٌ ولا "
    "وزنٌ ولا صيغة، ففرزُ الماضي المجرَّد عن المزيد لا مادّةَ له ههنا؛ "
    "وفرزُه بعدد الحروف هو الفرزُ بالصورة بعينه. فالرتبةُ موقوفةٌ باسمها، "
    "ولا تُقدَّر ولا تُصفَّر"
)

THE_ARTICLE_CELL_IS_FILLED_IN_SOME_ROWS_AND_BLANK_IN_OTHERS_NOTE: Final[str] = (
    "TheArticleCellIsFilledInSomeRowsAndBlankInOthers: 2,588 مقطعًا وسمُها "
    "`DET` وخانةُ حكمها خالية، بينما تُملأ في سائر مواضع `أل` بـ"
    "`ال التعريف`؛ فالخلوُّ خانةٌ لم تُملأ لا حكمٌ، ولا يُحمَل على أحد "
    "الحكمين. وهو وحدَه أكثرُ ما أوقف الرتبةَ الأولى"
)

A_TAGGER_LABEL_IS_A_REPORT_NOT_OUR_LICENCE_NOTE: Final[str] = (
    "ATaggerLabelIsAReportNotOurLicence: ما في عمود المادّة خبرٌ عن "
    "المُوسِّم بموضعٍ مختومٍ يُعاد قراءتُه، وما يُخرِجه السُّلَّمُ ترخيصٌ "
    "منّا؛ فيُعرَضان صفَّين لا يُدمَجان، وجزمُ المُوسِّم لا يرفع وقوفَ "
    "السُّلَّم دون رتبةِ الكلمة"
)


class CellKind(Enum):
    """صنفُ خليّة عمودِ البناء: أحكمٌ هي أم بابٌ أم خلوّ؟ تُصنَّف قبل أن تُقرأ."""

    A_JUDGEMENT = "حكمٌ مكتوبٌ صراحةً"
    A_DOOR = "بابٌ مكتوبٌ مكانَ الحكم"
    EMPTY = "خانةٌ خاليةٌ أو غيرُ مملوءة"
    UNKNOWN = "قيمةٌ خارج المُعدَّد؛ لا تُحمَل على أقربها"


class Binding(Enum):
    """حكمُ الكلمة بناءً أو إعرابًا؛ مفردةٌ مغلقةٌ فيها عضوُ امتناعٍ مُصرَّحٌ به."""

    BUILT = "مبني"
    DECLINED = "معرب"
    NOT_READABLE = "لا يُقرَأ من هذه الخليّة"


THE_JUDGEMENT_CELLS: Final[Mapping[str, Binding]] = {
    "مبني": Binding.BUILT,
    "معرب": Binding.DECLINED,
}
"""الخليّتان اللتان تحملان حكمًا صريحًا؛ وما عداهما لا يُقرَأ حكمًا ابتداءً."""

THE_DOOR_CELLS: Final[Mapping[str, Binding]] = {
    "ضمير متصل": Binding.BUILT,
    "ضمير منفصل مبني": Binding.BUILT,
    "ضمير فصل": Binding.BUILT,
    "اسم موصول": Binding.BUILT,
    "اسم إشارة": Binding.BUILT,
    "اسم شرط": Binding.BUILT,
    "اسم استفهام": Binding.BUILT,
    "ال التعريف": Binding.BUILT,
    "كافة ومكفوفة": Binding.BUILT,
    "اسم عدد مركب مبني": Binding.BUILT,
}
"""الأبوابُ المكتوبةُ مكانَ الحكم، وكلُّها مبنيّةٌ بابًا؛ وحكمُها يُشتَقّ منها.

وهذا اشتقاقٌ **من باب الكلمة** لا من صورتها: «اسم موصول» بابٌ لا يكون صاحبُه
إلّا مبنيًّا، فاشتقاقُ البناء منه قراءةُ ما في الخانة لا زيادةٌ عليه. ولو وردت
خانةٌ خارج هذا المُعدَّد وخارج `THE_JUDGEMENT_CELLS` لم تُحمَل على أقربها، بل
صُنِّفت `UNKNOWN` ولم يُقرَأ منها حكم.
"""

_EMPTY_CELLS: Final[frozenset[str]] = frozenset({"", "None"})


def cell_kind(value: str) -> CellKind:
    """صنِّف خليّةَ عمود البناء قبل أن تُقرَأ حكمًا.

    المدخل: نصُّ الخليّة كما ورد في المادّة، بلا تطبيع.
    الشرط: لا شرطَ؛ وكلُّ نصٍّ يقع في صنفٍ واحدٍ من أربعة.
    المخرج: صنفُ الخليّة من `CellKind`.
    حدُّها: التصنيفُ خبرٌ عن **شكل الخانة**، لا عن صحّة ما فيها.
    """

    if value in _EMPTY_CELLS:
        return CellKind.EMPTY
    if value in THE_JUDGEMENT_CELLS:
        return CellKind.A_JUDGEMENT
    if value in THE_DOOR_CELLS:
        return CellKind.A_DOOR
    return CellKind.UNKNOWN


def reads_as(value: str) -> Binding:
    """اقرأ حكمَ البناء من خليّةٍ بعد تصنيفها؛ والخاليةُ والمجهولةُ لا تُقرَآن.

    المدخل: نصُّ الخليّة كما ورد.
    الشرط: لا شرطَ؛ والخلوُّ والجهلُ يُسمَّيان ولا يُحمَلان على `معرب`.
    المخرج: `Binding.BUILT` أو `Binding.DECLINED` أو `Binding.NOT_READABLE`.
    حدُّها: هذا نقلُ حكمِ المُوسِّم، لا حكمُنا نحن على الكلمة.
    """

    kind = cell_kind(value)
    if kind is CellKind.A_JUDGEMENT:
        return THE_JUDGEMENT_CELLS[value]
    if kind is CellKind.A_DOOR:
        return THE_DOOR_CELLS[value]
    return Binding.NOT_READABLE


class RungStanding(Enum):
    """منزلةُ الرتبة في السُّلَّم؛ و«لم يُبلَغ» منزلةٌ مُصرَّحٌ بها لا صمت."""

    LICENSED_AND_EXHAUSTED = "مُرخَّصةٌ ومستنفَدة"
    LICENSED_NOT_EXHAUSTED = "مُرخَّصةٌ ولم تُستنفَد؛ يقف السُّلَّمُ عندها"
    HAS_NO_COLUMN_IN_THE_MATERIAL = "موقوفةٌ: لا عمودَ لها في المادّة"
    NOT_REACHED = "لم تُبلَغ؛ وقف السُّلَّمُ دونها"


@dataclass(frozen=True, slots=True)
class Rung:
    """رتبةٌ في السُّلَّم: وسومُها مُعدَّدةٌ بأعيانها، وحكمُها مُدَّعًى قبل القياس."""

    index: int
    name: str
    tags: tuple[str, ...]
    claimed_binding: Binding
    has_a_column: bool = True

    def __post_init__(self) -> None:
        if self.index < 1:
            raise TadarrujLicenceError("رتبُ السُّلَّم تبدأ من واحد.")
        if not self.name.strip():
            raise TadarrujLicenceError("لكلّ رتبةٍ اسمٌ غيرُ فارغ.")
        if self.claimed_binding is Binding.NOT_READABLE:
            raise TadarrujLicenceError(
                f"الرتبةُ `{self.name}` تدّعي حكمًا؛ و«لا يُقرَأ» ليس دعوى."
            )
        if self.has_a_column and not self.tags:
            raise TadarrujLicenceError(
                f"الرتبةُ `{self.name}` ذاتُ عمودٍ بلا وسمٍ واحد؛ "
                "والجردُ الفارغُ يُرخِّص بلا مقياس."
            )
        if self.tags and not self.has_a_column:
            raise TadarrujLicenceError(
                f"الرتبةُ `{self.name}` موقوفةٌ لانعدام العمود، فلا تُعدَّد "
                "لها وسوم؛ وتعديدُها يُوهِم أنّها تُقاس."
            )
        if len(set(self.tags)) != len(self.tags):
            raise TadarrujLicenceError(f"وسمٌ مكرَّرٌ في الرتبة `{self.name}`.")


THE_RUNGS: Final[tuple[Rung, ...]] = (
    Rung(
        index=1,
        name="الأدواتُ والحروفُ الوظيفيّة",
        tags=(
            "PREP",
            "CONJ",
            "NEG_PART",
            "ANNUL_PART",
            "INF_ANNUL_PART",
            "SUBJUNC_PART",
            "INF_SUBJUNC_PART",
            "JUSSIVE_PART",
            "CONDITION_PART",
            "EXCEPT_PART",
            "CERT_PART",
            "FUT_PART",
            "FUTURE_PART",
            "FUTUR_PART",
            "INTERROG_PART",
            "VOC_PART",
            "YES_NO_RESP_PART",
            "DET",
        ),
        claimed_binding=Binding.BUILT,
    ),
    Rung(
        index=2,
        name="الضمائرُ المنفصلة",
        tags=(
            "PRON",
            "PRON_1S",
            "PRON_1P",
            "PRON_2MS",
            "PRON_2MP",
            "PRON_3MS",
            "PRON_3MP",
            "PRON_3FS",
            "PRON_3FP",
            "PRON_3D",
        ),
        claimed_binding=Binding.BUILT,
    ),
    Rung(
        index=3,
        name="الضمائرُ المتّصلة",
        tags=(
            "SUBJ_PRON",
            "OBJ_PRON",
            "POSS_PRON",
            "POSS_PRON_1S",
            "POSS_PRON_1P",
            "POSS_PRON_2MS",
            "POSS_PRON_3MS",
            "POSS_PRON_3MP",
            "POSS_PRON_3FS",
            "POSS_PRON_3D",
            "PVSUFF_SUBJ:1S",
            "PVSUFF_SUBJ:1P",
            "PVSUFF_SUBJ:2MP",
            "PVSUFF_SUBJ:3MS",
            "PVSUFF_SUBJ:3MP",
            "PVSUFF_SUBJ:3FS",
            "PVSUFF_DO:3MS",
            "PVSUFF_DO:3MP",
            "PVSUFF_DO:3FS",
            "IVSUFF_DO:3MS",
        ),
        claimed_binding=Binding.BUILT,
    ),
    Rung(
        index=4,
        name="أسماءُ الإشارة",
        tags=("DEM_PRON", "DEM_PRON_F", "DEM_PRON_FS", "DEM_PRON_MS", "DEM_PRON_MP"),
        claimed_binding=Binding.BUILT,
    ),
    Rung(
        index=5,
        name="الأسماءُ الموصولة",
        tags=("REL_PRON",),
        claimed_binding=Binding.BUILT,
    ),
    Rung(
        index=6,
        name="الفعلُ الماضي",
        tags=("PV", "PV_PASS"),
        claimed_binding=Binding.BUILT,
    ),
    Rung(
        index=7,
        name="الفعلُ الماضي المزيدُ مفروزًا عن المجرَّد",
        tags=(),
        claimed_binding=Binding.BUILT,
        has_a_column=False,
    ),
    Rung(
        index=8,
        name="المعرَب",
        tags=("IV", "IV_PASS", "NOUN_CONCRETE", "NOUN_ABSTRACT", "NOUN_PROP"),
        claimed_binding=Binding.DECLINED,
    ),
)
"""رتبُ السُّلَّم مسنونةً بترتيبها؛ لا تاسعةَ، ولا يُقدَّم متأخِّرٌ عن موضعه.

والرتبةُ الثامنة — المعرَب — آخرُ السُّلَّم عمدًا: هي الغايةُ التي لا تُبلَغ
إلّا بعد استنفاد ما دونها، وفيها «أعمل» و«رجل».
"""


THE_LADDER_AT_MEASUREMENT: Final[Mapping[str, tuple[int, int, int, int, int]]] = {
    "الأدواتُ والحروفُ الوظيفيّة": (46336, 61, 43697, 18, 2621),
    "الضمائرُ المنفصلة": (3853, 23, 3831, 2, 20),
    "الضمائرُ المتّصلة": (20792, 41, 19770, 16, 1006),
    "أسماءُ الإشارة": (1124, 14, 1124, 0, 0),
    "الأسماءُ الموصولة": (3524, 15, 3524, 0, 0),
    "الفعلُ الماضي": (8996, 1109, 8863, 133, 0),
    "الفعلُ الماضي المزيدُ مفروزًا عن المجرَّد": (0, 0, 0, 0, 0),
    "المعرَب": (26353, 2252, 23798, 2555, 0),
}
"""السُّلَّمُ وقتَ القياس: (مقاطع · صورٌ متمايزة · مُرخَّص · مخالف · لا يُقرَأ).

منقولٌ لا مولَّدٌ ههنا، لأنّ بايتات المادّة لا تُحَلّ في كلّ بيئة؛ ومن حلَّها
يُعيد هذه الأعدادَ بـ`ladder_reading` على سجلّاتها. وخلافُها زحزحةٌ تُعرَض ولا
تُسوَّى بتعديل الرقم.
"""

THE_STOP_AT_MEASUREMENT: Final[str] = "الأدواتُ والحروفُ الوظيفيّة"
"""الرتبةُ التي وقف عندها السُّلَّمُ وقتَ القياس: أولاهنّ، فلم تُبلَغ رتبةٌ بعدها."""

THE_WORDS_DECIDED_AT_MEASUREMENT: Final[Mapping[str, tuple[int, str]]] = {
    "أعمل": (8, "المعرَب"),
    "رجل": (13, "المعرَب"),
}
"""الكلمتان المسؤولُ عنهما: (عددُ مقاطعهما · رتبتُهما في سُلَّمنا).

ورتبتُهما الثامنةُ لم تُبلَغ، فمنزلتُهما `NOT_REACHED`؛ وهذا تقريرُ موضعهما من
السُّلَّم لا حكمٌ عليهما.
"""


def rung_named(name: str) -> Rung:
    """الرتبةُ باسمها؛ واسمٌ خارجَ المُعدَّد يُرفَع به خطأٌ ولا يُقرَّب.

    المدخل: اسمُ رتبةٍ كما وردت في `THE_RUNGS`.
    الشرط: الاسمُ مطابقٌ تمامًا.
    المخرج: الرتبةُ المسمّاة.
    حدُّها: لا تُنشَأ ههنا رتبةٌ جديدة.
    """

    for rung in THE_RUNGS:
        if rung.name == name:
            return rung
    raise TadarrujLicenceError(f"لا رتبةَ في السُّلَّم بهذا الاسم: `{name}`")


@dataclass(frozen=True, slots=True)
class RungReading:
    """قراءةُ رتبةٍ على المادّة: المُرخَّصُ والمخالفُ وما لا يُقرَأ، وكلٌّ باسمه."""

    rung: Rung
    segments: int
    distinct_forms: int
    licensed: int
    disagreeing: int
    unreadable: int
    disagreeing_cells: tuple[tuple[str, int], ...]
    standing: RungStanding

    def __post_init__(self) -> None:
        total = self.licensed + self.disagreeing + self.unreadable
        if total != self.segments:
            raise TadarrujLicenceError(
                f"الرتبةُ `{self.rung.name}`: المُرخَّصُ والمخالفُ وما لا "
                f"يُقرَأ لا يجمعون المقاطعَ ({total} ≠ {self.segments}); "
                "ومقطعٌ يسقط من القسمة يرفع كلَّ نسبةٍ بعدها."
            )

    @property
    def is_exhausted(self) -> bool:
        """أاستُنفِدت الرتبةُ؟ لا مخالفَ فيها ولا خليّةَ لا تُقرَأ، وفيها مقاطع."""

        return self.segments > 0 and self.disagreeing == 0 and self.unreadable == 0


def _records_of(
    records: Iterable[Mapping[str, str]], rung: Rung
) -> list[Mapping[str, str]]:
    tags = set(rung.tags)
    return [row for row in records if row.get(TAG_COLUMN, "") in tags]


def rung_reading(
    records: Sequence[Mapping[str, str]],
    rung: Rung,
    *,
    reached: bool = True,
) -> RungReading:
    """اقرأ رتبةً على سجلّات المادّة، وأخرِج مُرخَّصَها ومخالفَها باسمه.

    المدخل: سجلّاتُ المادّة المختومة، ورتبةٌ من `THE_RUNGS`، وهل بُلِغت.
    الشرط: لكلّ سجلٍّ عمودا الوسم والبناء؛ وغيابُ أحدهما يُرفَع به خطأ.
    المخرج: `RungReading` يجمع أجزاؤها المقاطعَ بلا بقيّة.
    حدُّها: «مُرخَّص» يعني **موافقةَ عمودَي هذه المادّة**، لا صحّةَ الحكم في
        العربيّة؛ ومُوسِّمان متوافقان قد يُخطئان معًا.
    """

    if not rung.has_a_column:
        return RungReading(
            rung=rung,
            segments=0,
            distinct_forms=0,
            licensed=0,
            disagreeing=0,
            unreadable=0,
            disagreeing_cells=(),
            standing=RungStanding.HAS_NO_COLUMN_IN_THE_MATERIAL,
        )
    rows = _records_of(records, rung)
    licensed = 0
    unreadable = 0
    tally: dict[str, int] = {}
    forms: set[str] = set()
    for row in rows:
        if TAG_COLUMN not in row or BINDING_COLUMN not in row:
            raise TadarrujLicenceError(
                f"سجلٌّ بلا عمود `{TAG_COLUMN}` أو `{BINDING_COLUMN}`؛ "
                "والعمودُ الغائبُ يوقف العدَّ ولا يُعَدُّ صفرًا."
            )
        forms.add(row.get("Segmented_Word", ""))
        cell = row[BINDING_COLUMN]
        read = reads_as(cell)
        if read is Binding.NOT_READABLE:
            unreadable += 1
        elif read is rung.claimed_binding:
            licensed += 1
        else:
            tally[cell] = tally.get(cell, 0) + 1
    disagreeing = sum(tally.values())
    if not reached:
        standing = RungStanding.NOT_REACHED
    elif disagreeing == 0 and unreadable == 0 and rows:
        standing = RungStanding.LICENSED_AND_EXHAUSTED
    else:
        standing = RungStanding.LICENSED_NOT_EXHAUSTED
    return RungReading(
        rung=rung,
        segments=len(rows),
        distinct_forms=len(forms),
        licensed=licensed,
        disagreeing=disagreeing,
        unreadable=unreadable,
        disagreeing_cells=tuple(sorted(tally.items(), key=lambda pair: -pair[1])),
        standing=standing,
    )


@dataclass(frozen=True, slots=True)
class LadderReading:
    """قراءةُ السُّلَّم كلِّه: رتبةٌ رتبةً، وموضعُ الوقوف مُسمًّى."""

    rungs: tuple[RungReading, ...]

    def __post_init__(self) -> None:
        if len(self.rungs) != len(THE_RUNGS):
            raise TadarrujLicenceError(
                "قراءةُ السُّلَّم تحمل رتبَه كلَّها؛ وحذفُ رتبةٍ يُقصِّر "
                "السُّلَّمَ ويُوهِم بلوغَ ما لم يُبلَغ."
            )

    @property
    def stops_at(self) -> RungReading:
        """أوّلُ رتبةٍ لم تُستنفَد؛ وعندها يقف السُّلَّم."""

        for reading in self.rungs:
            if not reading.is_exhausted:
                return reading
        return self.rungs[-1]

    def reading_of(self, name: str) -> RungReading:
        """قراءةُ رتبةٍ باسمها؛ واسمٌ خارجَ المُعدَّد يُرفَع به خطأ."""

        for reading in self.rungs:
            if reading.rung.name == name:
                return reading
        raise TadarrujLicenceError(f"لا رتبةَ مقروءةً بهذا الاسم: `{name}`")


def ladder_reading(records: Sequence[Mapping[str, str]]) -> LadderReading:
    """اصعد السُّلَّمَ رتبةً رتبةً، وقِف عند أوّل رتبةٍ لم تُستنفَد.

    المدخل: سجلّاتُ المادّة المختومة.
    الشرط: الرتبُ تُقرَأ بترتيب `THE_RUNGS`؛ ولا تُقدَّم رتبةٌ على ما دونها.
    المخرج: `LadderReading` فيه لكلّ رتبةٍ قراءتُها ومنزلتُها.
    حدُّها: الوقوفُ حكمٌ على **هذه المادّة** بهذين العمودين، لا على العربيّة؛
        ورتبةٌ `NOT_REACHED` لم تُفحَص، فلا تُقرَأ نجاحًا ولا فشلًا.
    """

    readings: list[RungReading] = []
    still_climbing = True
    for rung in THE_RUNGS:
        reading = rung_reading(records, rung, reached=still_climbing)
        readings.append(reading)
        if still_climbing and not reading.is_exhausted:
            still_climbing = False
    return LadderReading(rungs=tuple(readings))


def licensing_stops_at(records: Sequence[Mapping[str, str]]) -> RungReading:
    """الرتبةُ التي يقف عندها الترخيص؛ وما فوقها لم يُبلَغ.

    المدخل: سجلّاتُ المادّة المختومة.
    الشرط: لا شرطَ زائدٌ على شرط `ladder_reading`.
    المخرج: قراءةُ أوّل رتبةٍ لم تُستنفَد.
    حدُّها: هذا موضعُ الوقوف لا سببُ الخلاف؛ والسببُ في `disagreeing_cells`.
    """

    return ladder_reading(records).stops_at


@dataclass(frozen=True, slots=True)
class SegmentRow:
    """مقطعٌ واحدٌ من المادّة كما ورد: موضعُه ووسمُه وخليّةُ حكمه."""

    sura: str
    verse: str
    segment: str
    tag: str
    cell: str

    @property
    def transmitted_binding(self) -> Binding:
        """حكمُ المُوسِّم كما يُقرَأ من خليّته؛ نقلٌ لا ترخيص."""

        return reads_as(self.cell)


@dataclass(frozen=True, slots=True)
class WordReport:
    """تقريرُ كلمةٍ: ما نقله المُوسِّمُ، وما رخَّصه سُلَّمُنا؛ صفّان لا يُدمَجان."""

    word: str
    rows: tuple[SegmentRow, ...]
    our_rung: Rung | None
    our_standing: RungStanding
    source_path: str = MASAQ_RELATIVE_PATH
    source_digest: str = MASAQ_SHA256

    @property
    def is_licensed_by_our_ladder(self) -> bool:
        """أرخَّص سُلَّمُنا هذه الكلمة؟ وبلوغُ الرتبة شرطٌ في ذلك."""

        return self.our_standing is RungStanding.LICENSED_AND_EXHAUSTED

    @property
    def transmitted_bindings(self) -> tuple[Binding, ...]:
        """أحكامُ المُوسِّم على مقاطع الكلمة، بترتيب ورودها ودون توحيد."""

        return tuple(row.transmitted_binding for row in self.rows)

    @property
    def verdict_line(self) -> str:
        """سطرُ التقرير: يفصل نقلَ المُوسِّم عن ترخيصنا، ولا يُلبِس أحدَهما الآخر."""

        rung = "خارجَ رتبِ السُّلَّم" if self.our_rung is None else self.our_rung.name
        return (
            f"«{self.word}»: المُوسِّمُ — {len(self.rows)} مقطعًا في "
            f"`{self.source_path}` ختمُه {self.source_digest[:12]}…؛ "
            f"وسُلَّمُنا — رتبتُها {rung}، ومنزلتُها {self.our_standing.value}. و"
            + A_TAGGER_LABEL_IS_A_REPORT_NOT_OUR_LICENCE_NOTE
        )


def _rung_of_tag(tag: str) -> Rung | None:
    for rung in THE_RUNGS:
        if tag in rung.tags:
            return rung
    return None


def report_on_word(
    records: Sequence[Mapping[str, str]],
    word: str,
    *,
    reading: LadderReading | None = None,
) -> WordReport:
    """قرِّر في كلمةٍ بتقرير: نقلُ المُوسِّم في صفٍّ، وترخيصُ سُلَّمِنا في صفّ.

    المدخل: سجلّاتُ المادّة، وكلمةٌ بلا شكلٍ كما في `Without_Diacritics`.
    الشرط: الكلمةُ واقعةٌ في المادّة؛ وغيابُها يُسمّى ولا يُحمَل على شبيهها.
    المخرج: `WordReport` فيه مقاطعُ الكلمة وأحكامُ المُوسِّم ومنزلةُ ترخيصنا.
    حدُّها: إن وقف السُّلَّمُ دون رتبة الكلمة كانت منزلتُنا `NOT_REACHED`
        **وإن جزم المُوسِّم**؛ فالوقوفُ لا يُرفَع بخبرِ غيرنا.
    """

    if not word.strip():
        raise TadarrujLicenceError("الكلمةُ المسؤولُ عنها غيرُ فارغة.")
    rows = tuple(
        SegmentRow(
            sura=row.get("Sura_No", ""),
            verse=row.get("Verse_No", ""),
            segment=row.get("Segmented_Word", ""),
            tag=row.get(TAG_COLUMN, ""),
            cell=row.get(BINDING_COLUMN, ""),
        )
        for row in records
        if row.get("Without_Diacritics", "") == word
    )
    if not rows:
        raise TadarrujLicenceError(
            f"الكلمةُ `{word}` غيرُ واقعةٍ في المادّة؛ وغيابُها يُسمّى ولا "
            "يُقرَّر فيها بالقياس على شبيهها."
        )
    ladder = ladder_reading(records) if reading is None else reading
    rungs = [_rung_of_tag(row.tag) for row in rows]
    named = [rung for rung in rungs if rung is not None]
    our_rung = max(named, key=lambda rung: rung.index) if named else None
    if our_rung is None:
        standing = RungStanding.NOT_REACHED
    else:
        standing = ladder.reading_of(our_rung.name).standing
    return WordReport(word=word, rows=rows, our_rung=our_rung, our_standing=standing)


TADARRUJ_LICENCE_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "AMixedColumnIsTwoQuestionsNotOne": A_MIXED_COLUMN_IS_TWO_QUESTIONS_NOT_ONE_NOTE,
    "ASubstringInATagNameIsNotAClass": A_SUBSTRING_IN_A_TAG_NAME_IS_NOT_A_CLASS_NOTE,
    "ADisagreementIsAWithheldLicenceNotAMajorityVote": (
        A_DISAGREEMENT_IS_A_WITHHELD_LICENCE_NOT_A_MAJORITY_VOTE_NOTE
    ),
    "AnUnexhaustedRungLicensesNothingAboveIt": (
        AN_UNEXHAUSTED_RUNG_LICENSES_NOTHING_ABOVE_IT_NOTE
    ),
    "TheBareAndTheAugmentedPastHaveNoColumn": (
        THE_BARE_AND_THE_AUGMENTED_PAST_HAVE_NO_COLUMN_NOTE
    ),
    "AShapeThatCarriesSevenHundredWordsSortsNothing": (
        A_SHAPE_THAT_CARRIES_SEVEN_HUNDRED_WORDS_SORTS_NOTHING_NOTE
    ),
    "ATaggerLabelIsAReportNotOurLicence": (
        A_TAGGER_LABEL_IS_A_REPORT_NOT_OUR_LICENCE_NOTE
    ),
}
"""البقايا المُسمّاةُ لهذه الوحدة؛ تُقرَأ حدودًا مُعلَنةً لا اعتذارًا لاحقًا."""
