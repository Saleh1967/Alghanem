"""حدُّ المادّة في «مقاييس اللغة»، مقيسًا قبل أن يُوصَل المعجمُ بشيء.

**ما تفعله هذه الوحدة**: تقيس — من البايتات المُبصَّمة في
`maqayis_root_table_deposit` — أين تبتدئ مادّةُ ابن فارس وأين تنتهي، فتُخرِج
**مادّةً مبتلَعةً في صفِّ غيرها** باسمها ومضيفها، وتنزع عن حقلَي المحاور صفةَ
الشهادة. وليست تُصحِّح الملفّ ولا تكتب فوق بايتةٍ منه؛ المخرجُ **قراءةُ
مصالحةٍ** مفاتيحُها أرقامُ الصفوف الأصليّة.

**ولمَ قبل الربط لا بعده**: وصلُ معجمٍ بشاهدٍ أو بوسمٍ صرفيٍّ يجعل حدَّ المادّة
مفتاحًا في كلّ وصلةٍ بعده. فلو وُصِّل الملفُّ بحاله، لنُسِبت مادّةُ «أحّ»
بتمامها إلى الجذر «أجج» في كلّ معنًى وكلّ شاهدٍ يُستخرَج منها، **وتضاعف الخطأُ
بالترخيص ولم يظهر في عدّادٍ واحد**
(`A_BOUNDARY_DEFECT_MULTIPLIES_DOWNSTREAM_AND_SHOWS_IN_NO_COUNTER`).

`THE_OPENING_FORMULA_IS_MEASURED_NOT_ASSUMED`: فاتحةُ ابن فارس تسميةُ حروف
الجذر («الهمزة والجيم…»، «وللهمزة والحاء…»). وليست هذه قاعدةً مفترضةً تُصدَّق
لأنّها معقولة: هي **مقيسةٌ على الملفّ كلِّه**، تُصيب مطلعَ كلِّ صفٍّ من
الصفوف الأربعة آلافٍ والخمسمائة والستّة والسبعين بلا استثناءٍ واحد. وعلى هذا
الاطّراد — لا على حُسن الظنّ — يقوم استعمالُها علامةَ حدّ. وتسقط العلامةُ
بسقوط اطّرادها، فيُفحَص الاطّرادُ في كلّ تشغيل.

`A_COARSE_DETECTOR_OVER_DETECTS_SO_BOTH_ARE_REPORTED`: التسميةُ تقع في المتن
لغيرِ الافتتاح — إحالةً («وقد مضى تفسير ذلك فى الهمزة والواو والراء») أو
تنبيهًا («لأنّ هذين الحرفين — أعنى الهمزة والهاء — متقاربان»). فيُقاس كاشفان
لا واحد: **موسَّعٌ** يعُدّ كلَّ تسميةٍ متأخّرة، و**محافِظٌ** يشترط أن تفتتح
التسميةُ سطرَها وأن يسبقها سطرٌ هو عنوانُ مادّةٍ مفردة. ويُعرَض الفرقُ بينهما
عددًا مُسمًّى، ولا يُطوى أحدُهما في الآخر: فمن عرض الموسَّعَ وحدَه ضخّم، ومن
عرض المحافِظَ وحدَه أوهم أنّ ما عداه سليم.

`A_CHAPTER_HEADER_IS_NOT_A_SWALLOWED_ENTRY`: أكثرُ التسميات المتأخّرة
فواتحُ **أبواب** («باب الهمزة والتاء وما يثلثهما») تخلّفت في ذيل الصفّ، وهي
حدٌّ أعلى لا مادّةٌ مبتلَعة. فتُفرَز بصنفها ولا تُحشَر في عدّ الخلل، وإلّا
لصار الرقمُ أضعافَ ما وقع.

`A_SWALLOWED_ENTRY_IS_A_LOST_MATERIAL_NOT_ONLY_A_BLURRED_BOUNDARY`: الضررُ
ضِعفان لا واحد. فالصفُّ المضيفُ يُنسَب إليه ما ليس له، **ولا صفَّ للمادّة
المبتلَعة أصلًا**: لا بـ`root_full` ولا بـ`root_display` ولا بتضعيف عنوانها.
فمن عدَّ الصفوفَ عدَّ المعجمَ ناقصًا وهو يحسبه تامًّا. وهذا ما يُثبته
`swallowed_entries` بمطابقةٍ تُجرى على الملفّ لا بدعوى.

`A_HEAD_THAT_CANNOT_BE_READ_IS_NOT_A_NAMED_MATERIAL`: من العناوين المكشوفة ما
ليس عنوانًا، بل قوسُ محرِّرٍ لا حرفَ فيه. فيُفرَز صنفًا ثالثًا
`عنوانٌ غيرُ مقروء`، ولا يُعَدّ في المادّة المفقودة ولا يُحذَف من التقرير: فإنّ
حذفَه يُوهم دقّةً لم تقع، وعدَّه يُسمّي مفقودًا بلا اسم.

`THE_AXES_FIELDS_ARE_A_TOOL_OUTPUT_NOT_A_WITNESS_ON_THE_LEXICON`: `axes_count`
يخالف عددَ ما في `semantic_axes` في ألفٍ ومئتين وسبعةٍ وخمسين صفًّا — أي أكثر
من ربع الملفّ. وليست العلّةُ في صفّ «أجج» وحدَه حتّى تُعالَج مفردةً. فالحقلان
**مخرجُ أداةٍ غيرِ مُسمّاةٍ لا شهادةٌ على نصّ ابن فارس**، ولا يُقرأ أيٌّ منهما
محورًا دلاليًّا للمادّة. والمتنُ وحدَه أصلُ الاستخراج.

`RECONCILIATION_IS_DEPOSITED_AND_THE_BYTES_ARE_NEVER_WRITTEN_OVER`: لا تُحرَّر
بايتةٌ واحدة. فلكلّ صفٍّ معرّفٌ مُشتَقٌّ من **بصمة الملفّ ورقم الصفّ**، وتُعلَّق
عليه قراءةُ حدِّه؛ فيُصحَّح الحدُّ ويبقى الأصلُ مقروءًا كما ورد، على منوال
`A_COUNT_IS_RELATIVE_TO_ITS_COUNTING_RULE` في وحدة الإيداع.

وهذه الوحدة تسجيلٌ لا سلطة: لا ولادةَ فيها، ولا حكمَ ولادة، ولا تجميدَ `E0`،
ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه. ولا تُصدِر معنًى لجذرٍ
ولا وصلةً إلى شاهدٍ ولا قاعدةً نحويّة: تلك كلُّها أطوارٌ بعد هذا الطور، وهذا
شرطُ صحّتها لا بديلٌ عنها.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from typing import Final

from .maqayis_root_table_deposit import (
    root_table_digest,
    root_table_rows,
)

__all__ = [
    "A_BOUNDARY_DEFECT_MULTIPLIES_DOWNSTREAM_AND_SHOWS_IN_NO_COUNTER_NOTE",
    "A_CHAPTER_HEADER_IS_NOT_A_SWALLOWED_ENTRY_NOTE",
    "A_COARSE_DETECTOR_OVER_DETECTS_SO_BOTH_ARE_REPORTED_NOTE",
    "A_HEAD_THAT_CANNOT_BE_READ_IS_NOT_A_NAMED_MATERIAL_NOTE",
    "A_SWALLOWED_ENTRY_IS_A_LOST_MATERIAL_NOT_ONLY_A_BLURRED_BOUNDARY_NOTE",
    "AXES_DISAGREEMENT_COUNTING_RULE",
    "CHAPTER_HEAD_MARKER",
    "COARSE_DETECTOR_RULE",
    "CONSERVATIVE_DETECTOR_RULE",
    "LETTER_NAMES",
    "OPENING_FORMULA_RULE",
    "RECONCILIATION_IS_DEPOSITED_AND_THE_BYTES_ARE_NEVER_WRITTEN_OVER_NOTE",
    "THE_AXES_FIELDS_ARE_A_TOOL_OUTPUT_NOT_A_WITNESS_ON_THE_LEXICON_NOTE",
    "THE_BOUNDARY_READING_AT_MEASUREMENT",
    "THE_OPENING_FORMULA_IS_MEASURED_NOT_ASSUMED_NOTE",
    "THIS_IS_REGISTRATION_NOT_AUTHORITY_NOTE",
    "BoundaryReading",
    "LaterNaming",
    "MaqayisEntryBoundaryError",
    "NamingGenus",
    "SwallowedEntry",
    "axes_disagreement_rows",
    "boundary_reading",
    "boundary_reading_has_drifted",
    "chapter_header_namings",
    "every_row_opens_with_the_formula",
    "later_namings",
    "reconciliation_rows",
    "strip_editorial_marks",
    "row_identifier",
    "rows_without_an_axes_count",
    "swallowed_entries",
]


class MaqayisEntryBoundaryError(ValueError):
    """رفضٌ صريح: صفٌّ بلا متنٍ، أو رقمُ صفٍّ خارج الملفّ، أو حقلٌ ناقص."""


class NamingGenus(Enum):
    """جنسُ التسمية المتأخّرة؛ مفردةٌ مغلقةٌ ثلاثيّة، ولا يُحمَل جنسٌ على آخر."""

    فاتحة_باب = "فاتحة_باب"
    مادة_مبتلعة = "مادة_مبتلعة"
    تسمية_في_سياق = "تسمية_في_سياق"


LETTER_NAMES: Final[tuple[str, ...]] = (
    "همزة",
    "ألف",
    "باء",
    "تاء",
    "ثاء",
    "جيم",
    "حاء",
    "خاء",
    "دال",
    "ذال",
    "راء",
    "زاء",
    "زاي",
    "سين",
    "شين",
    "صاد",
    "ضاد",
    "طاء",
    "ظاء",
    "عين",
    "غين",
    "فاء",
    "قاف",
    "كاف",
    "لام",
    "ميم",
    "نون",
    "هاء",
    "واو",
    "ياء",
)
"""أسماءُ الحروف مجرَّدةً من «ال»، إذ تُدغَم في «لـ» فتصير «وللهمزة»."""

CHAPTER_HEAD_MARKER: Final[str] = "باب"
"""لفظُ فاتحة الباب؛ وجودُه قبل التسمية يُخرِجها من عدّ المادّة المبتلَعة."""

_HEAD_WINDOW: Final[int] = 40
"""نافذةُ المطلع بالمحارف: تسميةٌ داخلها فاتحةُ الصفّ، وما بعدها متأخّرة."""

_MAXIMUM_ENTRY_HEAD_LENGTH: Final[int] = 8
"""أقصى طولِ سطرٍ يُقرأ عنوانَ مادّةٍ مفردة؛ وما طال عنه نثرٌ لا عنوان."""

_ARABIC_LETTER_RANGE: Final[str] = "\u0620-\u064a"

_EDITORIAL_MARKS: Final[str] = "[]()*«»"

_NAME_ALTERNATION: Final[str] = "|".join(LETTER_NAMES)

_NAMING_TOKEN: Final[str] = rf"(?:ال|لل)?(?:{_NAME_ALTERNATION})"

_NAMING_PATTERN: Final[re.Pattern[str]] = re.compile(
    rf"(?<![{_ARABIC_LETTER_RANGE}])(?:و|ف|ب|ل)?{_NAMING_TOKEN}"
    rf"(?:\s*و{_NAMING_TOKEN}){{1,3}}(?![{_ARABIC_LETTER_RANGE}])"
)


OPENING_FORMULA_RULE: Final[str] = (
    "فاتحةُ المادّة تسميةُ حرفين إلى أربعةٍ من حروف الجذر معطوفةً بالواو، "
    "واقعةً في أوّل أربعين محرفًا من المتن. والاسمُ يُقبَل بـ«ال» وبإدغامها "
    "في لامِ الجرّ («وللهمزة»)، وبواوِ العطف وفائه وبائه ولامه قبله. وهذه "
    "قاعدةُ كشفٍ تُعلَن قبل الرقم، لا وصفٌ يُفصَّل بعد رؤية النتيجة"
)

COARSE_DETECTOR_RULE: Final[str] = (
    "الكاشفُ الموسَّع يعُدّ كلَّ تسميةٍ تقع بعد نافذة المطلع، مهما كان موضعُها "
    "من السطر وما قبلها. وهو يُصيب الإحالاتِ والتنبيهاتِ كما يُصيب المادّةَ "
    "المبتلَعة، فعددُه حدٌّ أعلى لا عددُ خلل"
)

CONSERVATIVE_DETECTOR_RULE: Final[str] = (
    "الكاشفُ المحافِظ يشترط ثلاثةً معًا: أن تقع التسميةُ بعد نافذة المطلع، "
    "وأن تفتتح سطرَها فلا يسبقها في سطرها محرفٌ غيرُ فراغ، وأن يكون آخرُ سطرٍ "
    "غيرِ فارغٍ قبلها عنوانَ مادّةٍ مفردة — كلمةً واحدةً لا تتجاوز ثمانية "
    "محارف. وما سبقته لفظةُ «باب» مصروفٌ عنه إلى صنف فاتحة الباب"
)

AXES_DISAGREEMENT_COUNTING_RULE: Final[str] = (
    "الصفُّ مُتخالِفٌ إذا كان `axes_count` رقمًا وخالف عددَ المحاور في "
    "`semantic_axes` مفصولةً بالفاصلة العربية (U+060C) بعد إسقاط الفارغ. "
    "و`axes_count` الخالي **ليس صفرًا**: هو غيابُ عدٍّ لا عددٌ مخالف، فيُفرَز "
    "صنفًا ثانيًا يُعَدّ على حدة. وقراءتُه صفرًا تُدخِل في الخلاف صفوفًا لم "
    "يُعلَن لها عددٌ أصلًا، فتُخلَط مخالفةُ الأداة بسكوتها"
)

A_BOUNDARY_DEFECT_MULTIPLIES_DOWNSTREAM_AND_SHOWS_IN_NO_COUNTER_NOTE: Final[str] = (
    "خللُ الحدّ لا يظهر في عدّادٍ بعده: الصفوفُ تبقى أربعةَ آلافٍ وخمسمائةٍ "
    "وستّةً وسبعين، والجذورُ تبقى متمايزة، وكلُّ وصلةٍ تُبنى فوقه تخرج "
    "«ناجحة». فيُقاس الحدُّ قبل أن يُوصَل المعجمُ بشيء، لا بعد أن تُبنى عليه "
    "المعاني والشواهد والقواعد."
)

THE_OPENING_FORMULA_IS_MEASURED_NOT_ASSUMED_NOTE: Final[str] = (
    "استعمالُ فاتحة التسمية علامةَ حدٍّ مرخَّصٌ باطّرادها المقيس — تصيب مطلعَ "
    "كلّ صفٍّ في الملفّ بلا استثناء — لا بمعقوليّتها. فالاطّرادُ يُفحَص في كلّ "
    "تشغيل، وسقوطُه يُسقِط العلامةَ ومعها كلُّ عددٍ بُني عليها."
)

A_COARSE_DETECTOR_OVER_DETECTS_SO_BOTH_ARE_REPORTED_NOTE: Final[str] = (
    "التسميةُ تقع في المتن إحالةً وتنبيهًا لا افتتاحًا وحدَه، فيُقاس كاشفان: "
    "موسَّعٌ حدُّه الأعلى، ومحافِظٌ حدُّه الأدنى. ويُعرَض الفرقُ عددًا مُسمًّى: "
    "فمن عرض الموسَّعَ وحدَه ضخّم الخلل، ومن عرض المحافِظَ وحدَه أوهم أنّ ما "
    "عداه سليمٌ مفحوص."
)

A_CHAPTER_HEADER_IS_NOT_A_SWALLOWED_ENTRY_NOTE: Final[str] = (
    "فاتحةُ الباب («باب الهمزة والتاء وما يثلثهما») حدٌّ أعلى تخلّف في ذيل "
    "الصفّ، لا مادّةٌ ابتُلعت. فتُفرَز بصنفها ولا تُحشَر في عدّ الخلل، وحشرُها "
    "يُضاعف الرقمَ أضعافًا ويُفقِده دلالتَه."
)

A_SWALLOWED_ENTRY_IS_A_LOST_MATERIAL_NOT_ONLY_A_BLURRED_BOUNDARY_NOTE: Final[str] = (
    "المادّةُ المبتلَعة ضرران لا ضرر: يُنسَب إلى المضيف ما ليس له، ولا يبقى "
    "للمبتلَعة صفٌّ في الملفّ ألبتّة — لا بعنوانها ولا بتضعيفه. فمن عدَّ "
    "الصفوفَ عدَّ معجمًا ناقصًا وهو يحسبه تامًّا."
)

A_HEAD_THAT_CANNOT_BE_READ_IS_NOT_A_NAMED_MATERIAL_NOTE: Final[str] = (
    "عنوانٌ لا حرفَ فيه بعد إسقاط أقواس المحرِّر ليس مادّةً مُسمّاة: يُفرَز "
    "`عنوانٌ غيرُ مقروء` ويبقى في التقرير. فحذفُه يُوهم دقّةً لم تقع، وعدُّه "
    "في المفقود يُسمّي مفقودًا بلا اسم."
)

THE_AXES_FIELDS_ARE_A_TOOL_OUTPUT_NOT_A_WITNESS_ON_THE_LEXICON_NOTE: Final[str] = (
    "`semantic_axes` و`axes_count` مخرجُ أداةٍ غيرِ مُسمّاةٍ لا شهادةٌ على نصّ "
    "ابن فارس: يتخالفان في أكثرَ من ربع الملفّ، ويسكت العدُّ في قرابة خُمسه "
    "سكوتًا تامًّا. والسكوتُ غيرُ المخالفة، فيُفرَزان صنفين ولا يُقرأ الخالي "
    "صفرًا. فالعلّةُ منهجيّةٌ لا مفردةٌ تُعالَج في صفّ، ولا يُقرأ أيٌّ منهما "
    "محورًا دلاليًّا، والمتنُ وحدَه أصلُ الاستخراج."
)

RECONCILIATION_IS_DEPOSITED_AND_THE_BYTES_ARE_NEVER_WRITTEN_OVER_NOTE: Final[str] = (
    "لا تُحرَّر بايتةٌ من الملفّ: لكلّ صفٍّ معرّفٌ مُشتَقٌّ من بصمة الملفّ ورقمِ "
    "الصفّ، وتُعلَّق عليه قراءةُ حدّه. فيُصحَّح الحدُّ في القراءة ويبقى الأصلُ "
    "مقروءًا كما ورد، فلا يُفقَد أصلٌ بتصحيح."
)

THIS_IS_REGISTRATION_NOT_AUTHORITY_NOTE: Final[str] = (
    "لا ولادةَ هنا، ولا حكمَ ولادة، ولا تجميدَ `E0`، ولا استيرادَ من "
    "`kernel/`؛ ولا يُصدَر بهذه الوحدة معنًى لجذرٍ ولا وصلةٌ إلى شاهدٍ ولا "
    "قاعدةٌ نحويّة."
)


def _require_body(row: dict[str, str], index: int) -> str:
    body = row.get("body_text")
    if body is None:
        raise MaqayisEntryBoundaryError(f"الصفُّ {index} بلا عمود `body_text`")
    if not body.strip():
        raise MaqayisEntryBoundaryError(f"الصفُّ {index} بمتنٍ فارغ")
    return body


def strip_editorial_marks(text: str) -> str:
    """العنوانُ مجرَّدًا من الحركات وأقواس المحرِّر؛ لا يُطوى حرفٌ في حرف."""

    return "".join(
        character
        for character in text
        if unicodedata.category(character) != "Mn" and character not in _EDITORIAL_MARKS
    ).strip()


def row_identifier(row_index: int, digest: str | None = None) -> str:
    """معرّفُ الصفّ: بصمةُ نسخة الملفّ ورقمُ الصفّ، فيُتتبَّع الأصلُ بعد المصالحة."""

    if isinstance(row_index, bool) or not isinstance(row_index, int):
        raise MaqayisEntryBoundaryError("رقمُ الصفّ عددٌ صحيح")
    if row_index < 0:
        raise MaqayisEntryBoundaryError("رقمُ الصفّ غيرُ سالب")
    return f"{(digest or root_table_digest())[:12]}#{row_index}"


@dataclass(frozen=True, slots=True)
class LaterNaming:
    """تسميةُ حروفٍ وقعت بعد نافذة المطلع، بجنسها وموضعها ونصّها."""

    row_index: int
    host_root: str
    offset: int
    naming_text: str
    genus: NamingGenus
    preceding_head: str | None

    def __post_init__(self) -> None:
        if self.offset < _HEAD_WINDOW:
            raise MaqayisEntryBoundaryError(
                "التسميةُ المتأخّرة تقع بعد نافذة المطلع، وما فيها فاتحةٌ لا تأخُّر"
            )
        if not self.naming_text.strip():
            raise MaqayisEntryBoundaryError("نصُّ التسمية لا يكون فارغًا")


@dataclass(frozen=True, slots=True)
class SwallowedEntry:
    """مادّةٌ ابتُلعت في صفِّ غيرها: عنوانُها، ومضيفُها، وهل لها صفٌّ أصلًا."""

    row_index: int
    host_root: str
    swallowed_head: str
    normalized_head: str
    has_its_own_row: bool

    @property
    def head_is_readable(self) -> bool:
        """أبقي في العنوان حرفٌ بعد إسقاط أقواس المحرِّر، فيكون مادّةً مُسمّاة؟"""

        return bool(self.normalized_head)


@dataclass(frozen=True, slots=True)
class BoundaryReading:
    """قراءةُ الحدّ: اطّرادُ الفاتحة، وكاشفان، وأصنافُ التسمية، وخلافُ المحاور."""

    rows: int
    rows_opening_with_the_formula: int
    coarse_later_namings: int
    chapter_header_namings: int
    conservative_swallowed_entries: int
    swallowed_entries_with_a_readable_head: int
    swallowed_entries_without_their_own_row: int
    rows_whose_axes_fields_disagree: int
    rows_without_an_axes_count: int

    @property
    def opening_formula_is_exceptionless(self) -> bool:
        """أتصيب الفاتحةُ كلَّ صفٍّ؟ وعلى هذا وحده تُرخَّص علامةُ الحدّ."""

        return self.rows_opening_with_the_formula == self.rows

    @property
    def detector_gap(self) -> int:
        """الفرقُ بين الحدّ الأعلى والأدنى، مُسمًّى لا مطويًّا في أحدهما."""

        return self.coarse_later_namings - self.conservative_swallowed_entries


@lru_cache(maxsize=1)
def _rows() -> tuple[dict[str, str], ...]:
    return root_table_rows()


@lru_cache(maxsize=1)
def every_row_opens_with_the_formula() -> bool:
    """أتفتتح كلُّ صفوف الملفّ بتسمية حروفها؟ مقيسًا لا مفترضًا."""

    for index, row in enumerate(_rows()):
        match = _NAMING_PATTERN.search(_require_body(row, index))
        if match is None or match.start() >= _HEAD_WINDOW:
            return False
    return True


@lru_cache(maxsize=1)
def later_namings() -> tuple[LaterNaming, ...]:
    """كلُّ تسميةٍ بعد نافذة المطلع، مصنَّفةً بجنسها؛ وهذا الكاشفُ الموسَّع."""

    findings: list[LaterNaming] = []
    for index, row in enumerate(_rows()):
        body = _require_body(row, index)
        for match in _NAMING_PATTERN.finditer(body):
            if match.start() < _HEAD_WINDOW:
                continue
            genus, head = _classify(body, match.start())
            findings.append(
                LaterNaming(
                    row_index=index,
                    host_root=row["root_full"],
                    offset=match.start(),
                    naming_text=match.group(0),
                    genus=genus,
                    preceding_head=head,
                )
            )
    return tuple(findings)


def _classify(body: str, offset: int) -> tuple[NamingGenus, str | None]:
    """جنسُ التسمية مُشتَقٌّ من موضعها وما قبلها، لا مكتوبٌ في حقل."""

    if CHAPTER_HEAD_MARKER in body[max(0, offset - 12) : offset]:
        return NamingGenus.فاتحة_باب, None
    line_start = body.rfind("\n", 0, offset)
    if line_start == -1 or body[line_start + 1 : offset].strip():
        return NamingGenus.تسمية_في_سياق, None
    preceding = [line for line in body[:line_start].split("\n") if line.strip()]
    if not preceding:
        return NamingGenus.تسمية_في_سياق, None
    head = preceding[-1].strip()
    if len(head) > _MAXIMUM_ENTRY_HEAD_LENGTH or " " in head:
        return NamingGenus.تسمية_في_سياق, None
    return NamingGenus.مادة_مبتلعة, head


def chapter_header_namings() -> tuple[LaterNaming, ...]:
    """فواتحُ الأبواب المتخلّفة في ذيول الصفوف؛ حدٌّ أعلى لا مادّةٌ مبتلَعة."""

    return tuple(
        naming for naming in later_namings() if naming.genus is NamingGenus.فاتحة_باب
    )


@lru_cache(maxsize=1)
def swallowed_entries() -> tuple[SwallowedEntry, ...]:
    """الموادُّ المبتلَعة بالكاشف المحافِظ، ولكلٍّ هل لها صفٌّ في الملفّ."""

    rows = _rows()
    declared = {row["root_full"] for row in rows} | {
        row["root_display"] for row in rows
    }
    declared |= {strip_editorial_marks(value) for value in declared}
    found: list[SwallowedEntry] = []
    for naming in later_namings():
        if naming.genus is not NamingGenus.مادة_مبتلعة:
            continue
        head = naming.preceding_head or ""
        normalized = strip_editorial_marks(head)
        found.append(
            SwallowedEntry(
                row_index=naming.row_index,
                host_root=rows[naming.row_index]["root_full"],
                swallowed_head=head,
                normalized_head=normalized,
                has_its_own_row=bool(normalized)
                and (
                    normalized in declared
                    or _geminate_expansion(normalized) in declared
                ),
            )
        )
    return tuple(found)


def _geminate_expansion(head: str) -> str:
    """عنوانُ المضاعف يُكتَب بحرفين وشدّة؛ فيُجرَّب تضعيفُ آخره قبل الحكم بالغياب."""

    return head + head[-1] if head else head


@lru_cache(maxsize=1)
def axes_disagreement_rows() -> tuple[int, ...]:
    """أرقامُ الصفوف التي يخالف فيها `axes_count` الرقميُّ عددَ `semantic_axes`."""

    disagreeing: list[int] = []
    for index, row in enumerate(_rows()):
        raw = (row["axes_count"] or "").strip()
        if not raw.isdigit():
            continue
        axes = [part for part in row["semantic_axes"].split("،") if part.strip()]
        if int(raw) != len(axes):
            disagreeing.append(index)
    return tuple(disagreeing)


@lru_cache(maxsize=1)
def rows_without_an_axes_count() -> tuple[int, ...]:
    """أرقامُ الصفوف التي لا عددَ محاورَ لها أصلًا؛ سكوتٌ لا مخالفة."""

    return tuple(
        index
        for index, row in enumerate(_rows())
        if not (row["axes_count"] or "").strip().isdigit()
    )


def reconciliation_rows() -> tuple[dict[str, object], ...]:
    """قراءةُ المصالحة: معرّفُ الصفّ الأصليّ، ومضيفُه، وما نُسب إليه خطأً."""

    digest = root_table_digest()
    return tuple(
        {
            "row_identifier": row_identifier(entry.row_index, digest),
            "host_root": entry.host_root,
            "swallowed_head": entry.swallowed_head,
            "normalized_head": entry.normalized_head,
            "head_is_readable": entry.head_is_readable,
            "has_its_own_row": entry.has_its_own_row,
        }
        for entry in swallowed_entries()
    )


def boundary_reading() -> BoundaryReading:
    """القراءةُ كاملةً، مُشتقّةً من البايتات المُبصَّمة عند كلّ نداء."""

    rows = _rows()
    entries = swallowed_entries()
    readable = [entry for entry in entries if entry.head_is_readable]
    return BoundaryReading(
        rows=len(rows),
        rows_opening_with_the_formula=sum(
            1
            for index, row in enumerate(rows)
            if (match := _NAMING_PATTERN.search(_require_body(row, index))) is not None
            and match.start() < _HEAD_WINDOW
        ),
        coarse_later_namings=len(later_namings()),
        chapter_header_namings=len(chapter_header_namings()),
        conservative_swallowed_entries=len(entries),
        swallowed_entries_with_a_readable_head=len(readable),
        swallowed_entries_without_their_own_row=sum(
            1 for entry in readable if not entry.has_its_own_row
        ),
        rows_whose_axes_fields_disagree=len(axes_disagreement_rows()),
        rows_without_an_axes_count=len(rows_without_an_axes_count()),
    )


THE_BOUNDARY_READING_AT_MEASUREMENT: Final[BoundaryReading] = BoundaryReading(
    rows=4_576,
    rows_opening_with_the_formula=4_576,
    coarse_later_namings=696,
    chapter_header_namings=551,
    conservative_swallowed_entries=17,
    swallowed_entries_with_a_readable_head=15,
    swallowed_entries_without_their_own_row=15,
    rows_whose_axes_fields_disagree=1_257,
    rows_without_an_axes_count=864,
)
"""القراءةُ المُجمَّدةُ يوم القياس؛ تُصادَم بما يُشتَقّ من البايتات لا تُصدَّق."""


def boundary_reading_has_drifted() -> bool:
    """أانزاحت القراءةُ عن المُجمَّد؟ يُستدعى في البوّابة الواحدة للأرقام."""

    return boundary_reading() != THE_BOUNDARY_READING_AT_MEASUREMENT
