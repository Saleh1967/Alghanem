"""المؤشر المعرفيّ: ربطُ الغاية بمصادرها المقروءة عبر نصّ استشهادها وحده.

هذه **المرحلة السادسة من الطور الثاني** لـ AIM.1، وهي الخطوة التي أُجِّلت
صراحةً في خواتيم المراحل الخمس السابقة كلِّها: «ربطُ عددٍ مقروء بغايةٍ بعينها هو
المؤشر نفسه». فالمصادر الثلاثة التي سمّتها §٤ من `docs/AIMS.md` صارت مقروءةً
كلَّها — صفوفُ الدستور وأسئلةُ تدقيقه في `constitution_ledger`، والقيمُ المُعلَنة
غير القابلة للبناء في `deferred_value_ledger` — وبقي الربط::

    CitedSource      != Attainment
    DerivedLink      != Progress
    LedgerCount      != AimMovement
    ReadableCitation != TrueCitation

**المنعُ السابق كان تأجيلًا لا حدًّا دائمًا.** مُنع القرّاء الثلاثة من استيراد
`AimId` و`AimRecord` لأن ذلك الاستيراد **هو** المؤشر، لا لأنه محظور في نفسه؛
وهذه الوحدة تستوردهم جميعًا لأوّل مرّة، فتُصرّح بذلك ولا تُهرّبه. والخمولُ
السلطويّ يبقى مفحوصًا كما كان، لكن من ناحيته الصحيحة: لا وحدة في `kernel/`
تستورد طبقة البرنامج، ويُفحَص ذلك بمسحٍ آليّ.

**الربط مُشتَقّ لا مكتوب** (§٤): لا حقلَ يُكتَب فيه «مؤشر الغاية» ولا عددَ يُكتَب
في صنف. الرابط الوحيد المشروع هو حقل `citation` المُعلَن أصلًا في `AimRecord`
منذ المرحلة الأولى: تُستخرَج منه رموزُه بأشكالٍ مُصرَّح بها، ثم يُبحَث عن كلّ
رمزٍ في دفاتر القرّاء الثلاثة وفي نصّ الدستور. فالمُعلَن نصُّ الاستشهاد،
والمُشتَقّ ما وُجد فعلًا، والمخالفة — رمزٌ لا يُعثَر له على مرجع — تُرفَض عند
الإنشاء ولا تُقرَّر.

**المصدر التصميميّ المباشر، مُستشهَدًا به لا مُعادًا اشتقاقه.** شكلُ «الجهة
تُعلن، والقارئ لا يقبل إلا من مفردةٍ مغلقة يملكها، والمخالفة تُرفَض» مأخوذٌ من
سؤال التدقيق المفتوح `DeclaredVersusDerivedRecurrenceNotExplained` مصدرًا
مباشرًا (إلزام §٥)، لا بديهةً تُعاد هنا صامتةً؛ فهو مرصودٌ غير مفسَّر، ولا
يُستحدَث له هنا اسمٌ عامّ ولا صنفُ أساسٍ مشترك يوحّد الشكل بين القرّاء.

**مفرداتٌ مغلقة متعدّدة لا مقياسٌ رتبيّ واحد** (§٥)، مع تعليلِ كلّ دمجٍ مرفوض:

* لا يُجمَع عددُ الصفوف مع عددِ الأسئلة مع عددِ القيم المحجوزة في رقمٍ واحد:
  المجموعُ يخلق استلزامًا كاذبًا هو أن صفًّا واحدًا يعادل سؤالًا واحدًا يعادل
  قيمةً محجوزة، ولا شيء في السجلّ يُصرّح بهذا التعادل.
* ولا تُرتَّب الغايات بحسب أعدادها: الترتيبُ بالعدد هو تقديرُ القرب من البلوغ
  الذي تمنعه §٦ نصًّا، وهو حكمٌ لا سلطةَ هنا تملكه.
* ولا يُدمَج «جنس المصدر» مع «هل قُرئ في دفتر»: الجنسُ يُسقط حالةً قائمة —
  مسارٌ في الشجرة وقسمٌ في الوثيقة كلاهما غيرُ مقروءٍ في دفتر، وهما مختلفان.

**الجهل عضوٌ في المفردة لا فراغٌ يُطوى** (§٤): غايةٌ لا يبلغ استشهادُها أيّ
دفترٍ من الثلاثة تحمل `NO_LEDGER_READABLE_SOURCE` صراحةً، لا صفرًا يُقرَأ
«لم تتقدّم» ولا فراغًا يُقرَأ «لا مصدر لها».

**الرفض لا التخطّي الصامت، مرفوعًا طبقةً خامسة: من النقطة إلى الاستشهاد.** كما
صار كلُّ جدولٍ ثم كلُّ حارسٍ ثم كلُّ نقطةٍ إمّا مقروءًا أو مُستبعَدًا بجنسٍ
مُصرَّح به أو مرفوضًا باسمه وموضعه، يصير كلُّ رمزٍ في نصّ الاستشهاد كذلك،
ويُحصى الكلّ في `CitationCensus` بلا عددٍ مكتوب. فرمزٌ يسقط صامتًا يُنتج غايةً
تبدو أقلّ استنادًا ممّا صرّحت به وثيقتها.

**لا ترقية ولا حقل نتيجة**: لا دالّة هنا تحوّل رابطًا إلى `Freeze` ولا `E0` ولا
حكمِ ولادة ولا `AttainmentStanding.REACHED`؛ ولا حقلَ في أيّ صنفٍ هنا يحمل
جوابًا أو حكمًا أو مؤشرَ قيمة، ويُفحَص ذلك على حقول الأصناف نفسها لا في نثر.

**وترتيب الروابط ترتيبُ §٢** لا ترتيبَ أهمّية ولا قربٍ من بلوغ (§٦).
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass, fields
from enum import Enum
from pathlib import Path
from types import MappingProxyType
from typing import Final

from .aims import AIM_RECORDS, DESIGN_SOURCE_OPEN_QUESTION, AimId, AimRecord
from .constitution_ledger import (
    ConstitutionLedger,
    constitution_document_path,
    read_constitution_ledger,
)
from .deferred_value_ledger import (
    DeferredValueLedger,
    DeferredValueSite,
    read_deferred_value_ledger,
)

AIM_INDICATOR_AUTHORITY_NOTE: Final = (
    "ربطٌ فقط: لا يُنتج هذا المؤشر ولادةً ولا حكمًا ولا تجميدًا ولا `E0`، ولا "
    "يرفع غايةً إلى بلوغ، ولا يُرتّب الغايات بأولوية، ولا تقرؤه بوّابةٌ في النواة"
)

DESIGN_SOURCE_CITATION_NOTE: Final = (
    "شكلُ «الجهة تُعلن، والقارئ لا يقبل إلا من مفردةٍ مغلقة يملكها، والمخالفة "
    f"تُرفَض» مأخوذٌ من `{DESIGN_SOURCE_OPEN_QUESTION}` مصدرًا مباشرًا، لا "
    "بديهةً تُعاد هنا صامتةً"
)

DEFERRAL_WAS_NOT_A_PERMANENT_BOUNDARY_NOTE: Final = (
    "منعُ القرّاء الثلاثة من استيراد `AimId` كان تأجيلًا للمؤشر لا حدًّا "
    "دائمًا عليه؛ وهذه الوحدة تستوردهم مُصرِّحةً، والخمولُ السلطويّ يبقى "
    "مفحوصًا من ناحيته الصحيحة: لا وحدة في `kernel/` تقرأ طبقة البرنامج"
)

UNKNOWN_CITATION_TOKEN_IS_REFUSED_NOTE: Final = (
    "رمزٌ في نصّ الاستشهاد لا يُعثَر له على مرجعٍ يُوقف القراءة باسمه وموضعه "
    "ولا يُتخطّى: الرمزُ الساقط لا يتعارض مع شيءٍ لأنه لم يُقرَأ أصلًا، فتبدو "
    "الغاية أقلّ استنادًا ممّا صرّحت به وثيقتها"
)

NO_SUM_ACROSS_READERS_NOTE: Final = (
    "لا مجموعَ واحدًا عبر القرّاء الثلاثة: جمعُ صفٍّ إلى سؤالٍ إلى قيمةٍ "
    "محجوزة يستلزم تعادلها، ولا شيء في السجلّ يُصرّح به؛ والترتيبُ بالعدد "
    "تقديرُ قربٍ من بلوغٍ تمنعه §٦"
)

CITATION_LINK_IS_NOT_ATTAINMENT: Final = "CITATION_LINK_IS_NOT_ATTAINMENT"

CITATION_PROSE_IS_NOT_A_TOKEN_STREAM: Final = "CITATION_PROSE_IS_NOT_A_TOKEN_STREAM"

LEDGER_COUNT_MOVEMENT_IS_NOT_AIM_MOVEMENT: Final = (
    "LEDGER_COUNT_MOVEMENT_IS_NOT_AIM_MOVEMENT"
)

DEFERRED_VALUE_READER_IS_NOT_REACHED_BY_ANY_CITATION: Final = (
    "DEFERRED_VALUE_READER_IS_NOT_REACHED_BY_ANY_CITATION"
)

NAMED_RESIDUALS: Final[Mapping[str, str]] = MappingProxyType(
    {
        CITATION_LINK_IS_NOT_ATTAINMENT: (
            "بلوغُ الرمز في دفترٍ يُثبت أن الغاية تستند إلى مصدرٍ قائم، لا أنها "
            "تقدّمت نحوه ولا أنها قاربته: غايةٌ مستندةٌ إلى عشرة صفوفٍ مقروءة "
            "لم تبلغ شيئًا، والبلوغُ حكمٌ على أثرٍ لا على استشهاد"
        ),
        CITATION_PROSE_IS_NOT_A_TOKEN_STREAM: (
            "نصّ الاستشهاد نثرٌ مُعاد الصياغة لا تعدادُ رموز: فيه ما يُسمّي "
            "أسرةً من الصفوف بلا شكلٍ مُستخرَج (مثل «صفوف G0 في الدستور»)، وما "
            "ليس بشكلٍ مُصرَّح به ليس رمزًا يُقرَأ ولا يُرفَع به خطأ؛ فالقراءة "
            "تبلغ ما احتملت الأشكالُ المُصرَّح بها وحدها، وهذا شقيقُ "
            "`RECORD_PROSE_IS_PARAPHRASE_NOT_TRANSCRIPTION`"
        ),
        LEDGER_COUNT_MOVEMENT_IS_NOT_AIM_MOVEMENT: (
            "أعدادُ الصفوف والأسئلة تتغيّر بتحرير الوثيقة وحده، وهذا الرابط "
            "يتغيّر معها؛ فتغيّرُ العدد لا يُقرَأ حركةً في غاية، ولا يُقابَل "
            "بعددٍ مرجعيّ مستقلّ، وهو شقيقُ `NO_DECLARED_TOTAL_TO_CROSS_CHECK`"
        ),
        DEFERRED_VALUE_READER_IS_NOT_REACHED_BY_ANY_CITATION: (
            "القارئ الثالث مقروءٌ هنا وجنسُه عضوٌ في المفردة وحاضرٌ في الإحصاء "
            "ولو بصفر، ولا يبلغه استشهادُ غايةٍ اليوم: أسماءُ القيم الثلاث "
            "تَرِد في أسئلة الغايات وحدودها لا في مستنداتها. وتوسيعُ الرابط "
            "إلى بقيّة حقول السجلّ يجعل كلّ ذكرٍ لقيمةٍ استشهادًا بها، وهو "
            "حكمٌ لا تملكه هذه المرحلة؛ فالبقيّة مُسمّاة لا مطويّة"
        ),
    }
)

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
    "indicator",
    "score",
    "percent",
    "estimate",
    "priority",
)

_REPOSITORY_PATH_SHAPE: Final = re.compile(r"^(?:docs|src|tests|examples)/[\w./-]*$")
_ROW_IDENTIFIER_SHAPE: Final = re.compile(r"^[A-Z]\d(?:\.[A-Z]+)+\.\d+[a-z]?$")

_TOKEN_PATTERN: Final = re.compile(
    r"«(?P<guillemet>[^»]+)»"
    r"|`(?P<backtick>[^`]+)`"
    r"|(?P<path>(?:docs|src|tests|examples)/[\w./-]*)"
    r"|(?<![A-Za-z0-9_.`])(?P<row_id>[A-Z]\d(?:\.[A-Z]+)+\.\d+[a-z]?)"
    r"|(?<![A-Za-z0-9_`])(?P<camel>[A-Z][a-z0-9]+(?:[A-Z][a-z0-9]+)+)(?![A-Za-z0-9_])"
)

_HEADING_LINE: Final = re.compile(r"^#{1,6} (?P<heading>.+)$")
_CLAIM_LINE: Final = re.compile(r"^- `(?P<claim>[^`]+)`\.?$")


class AimIndicatorError(ValueError):
    """ربطٌ مرفوض؛ لا يُحمَل الرمزُ على أقرب مرجعٍ مقبول."""


class CitedTokenShape(Enum):
    """أشكال الرمز في نصّ الاستشهاد، مفردةً مغلقة مُستخرَجة من السجلّ لا مُبتكَرة.

    الأشكال الخمسة قائمةٌ في `AimRecord.citation` اليوم معًا، والدمجُ بينها
    يُسقط شكلًا قائمًا: المسارُ يُكتَب عاريًا، واسمُ الصفّ النثريّ بين علامتَي
    اقتباسٍ مزدوجتين، واسمُ السؤال بين علامتَي تنصيصٍ مائلتين أو عاريًا مُدمَجًا،
    ومعرّفُ الصفّ بنقاطٍ وأرقام.
    """

    REPOSITORY_PATH_TEXT = "مسارٌ_في_الشجرة"
    GUILLEMET_SPAN = "بين_علامتَي_اقتباس"
    BACKTICK_SPAN = "بين_علامتَي_تنصيص"
    DOTTED_ROW_IDENTIFIER = "معرّفُ_صفٍّ_بنقاط"
    BARE_JOINED_NAME = "اسمٌ_مُدمَجٌ_عارٍ"


class CitedSourceGenus(Enum):
    """جنسُ المصدر المستشهَد به، والجهلُ عضوٌ فيه لا فراغٌ يُطوى.

    الأجناس الثلاثة الأولى وحدها مقروءةٌ في دفاتر §٤ الثلاثة؛ وما بعدها
    **مُستبعَدٌ مُصرَّحٌ باستبعاده** على منهج `DeclaredTableHeader`، لا مطويٌّ
    بصمت القارئ عنه: القسمُ في الوثيقة ليس صفًّا، والمسارُ في الشجرة ليس عددًا،
    وسطرُ الدعوى ليس قانونًا؛ وكلُّها مُتحقَّقٌ من وجودها قبل استبعادها.
    """

    CONSTITUTION_LAW_ROW = "صفٌّ_في_الدستور"
    AUDIT_QUESTION = "سؤالُ_تدقيق"
    DEFERRED_VALUE_SITE = "قيمةٌ_محجوزة"
    CONSTITUTION_SECTION = "قسمٌ_في_الدستور"
    CONSTITUTION_CLAIM_LINE = "سطرُ_دعوى_في_الدستور"
    REPOSITORY_PATH = "مسارٌ_في_المستودع"
    NO_LEDGER_READABLE_SOURCE = "لا_مصدرَ_مقروءًا_في_دفتر"

    @property
    def is_read_in_a_ledger(self) -> bool:
        """أقُرئ هذا الجنس في دفترٍ من دفاتر §٤ الثلاثة؟"""

        return self in _LEDGER_BACKED_GENERA


_LEDGER_BACKED_GENERA: Final[frozenset[CitedSourceGenus]] = frozenset(
    {
        CitedSourceGenus.CONSTITUTION_LAW_ROW,
        CitedSourceGenus.AUDIT_QUESTION,
        CitedSourceGenus.DEFERRED_VALUE_SITE,
    }
)

_TOKEN_GENERA: Final[tuple[CitedSourceGenus, ...]] = tuple(
    genus
    for genus in CitedSourceGenus
    if genus is not CitedSourceGenus.NO_LEDGER_READABLE_SOURCE
)

if len(CitedTokenShape) != 5:  # pragma: no cover - guard
    raise RuntimeError("a citation token takes one of exactly five observed shapes")
if len(_LEDGER_BACKED_GENERA) != 3:  # pragma: no cover - guard
    raise RuntimeError("section 4 names exactly three derivation readers")
if CitedSourceGenus.NO_LEDGER_READABLE_SOURCE.is_read_in_a_ledger:  # pragma: no cover
    raise RuntimeError("the ignorance member is not a ledger-backed genus")


def _require_non_blank(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise AimIndicatorError(f"{field_name} نصٌّ غير فارغ")
    return value


def _require_non_negative_offset(value: int, field_name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise AimIndicatorError(f"{field_name} موضعٌ غير سالب")
    return value


@dataclass(frozen=True, slots=True)
class ReadCitation:
    """رمزٌ واحد من نصّ استشهادٍ، بشكله المُصرَّح به وجنسه ومرجعه المُشتَقّ."""

    aim_id: AimId
    shape: CitedTokenShape
    text: str
    genus: CitedSourceGenus
    reference: str
    offset: int

    def __post_init__(self) -> None:
        if not isinstance(self.aim_id, AimId):
            raise AimIndicatorError("معرّف الغاية من مفردته المغلقة")
        if not isinstance(self.shape, CitedTokenShape):
            raise AimIndicatorError("شكل الرمز من مفردته المغلقة")
        if not isinstance(self.genus, CitedSourceGenus):
            raise AimIndicatorError("جنس المصدر من مفردته المغلقة")
        if self.genus is CitedSourceGenus.NO_LEDGER_READABLE_SOURCE:
            raise AimIndicatorError(
                "عضوُ الجهل رتبةُ غايةٍ لا جنسُ رمز: رمزٌ بلا مرجعٍ مرفوضٌ "
                f"باسمه وموضعه — {UNKNOWN_CITATION_TOKEN_IS_REFUSED_NOTE}"
            )
        _require_non_blank(self.text, "نصّ الرمز")
        _require_non_blank(self.reference, "مرجع الرمز المُشتَقّ")
        _require_non_negative_offset(self.offset, "موضع الرمز في الاستشهاد")

    @property
    def is_read_in_a_ledger(self) -> bool:
        """أبلغ هذا الرمزُ دفترًا من دفاتر §٤، أم استُبعد بجنسٍ مُصرَّح به؟"""

        return self.genus.is_read_in_a_ledger


@dataclass(frozen=True, slots=True)
class CitationCensus:
    """إحصاءُ رموز الاستشهادات كلِّها: المقروءُ منها والمُستبعَدُ مُصرَّحًا به.

    لا حقلَ عددٍ هنا؛ التعدادُ خاصّيةٌ تُحسَب من الرموز المرصودة. والمرفوضُ لا
    يبلغ هذا الإحصاء أصلًا، إذ يُوقِفه رفضٌ مُسمّى عند القراءة؛ وحضورُ الرمز
    المُستبعَد فيه هو الفارق بين «استُبعد بجنسٍ معروف» و«لم يُرَ أصلًا».
    """

    tokens: tuple[ReadCitation, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.tokens, tuple) or not self.tokens:
            raise AimIndicatorError("إحصاء الرموز مجموعةٌ غير فارغة")
        for token in self.tokens:
            if not isinstance(token, ReadCitation):
                raise AimIndicatorError("كل عنصرٍ رمزٌ مرصود")

    @property
    def token_count(self) -> int:
        """عدد الرموز المرصودة، محسوبًا لا مكتوبًا."""

        return len(self.tokens)

    @property
    def read_tokens(self) -> tuple[ReadCitation, ...]:
        """الرموز التي بلغت دفترًا من الثلاثة، بترتيب ورودها."""

        return tuple(token for token in self.tokens if token.is_read_in_a_ledger)

    @property
    def excluded_tokens(self) -> tuple[ReadCitation, ...]:
        """الرموز المُستبعَدة بجنسٍ مُصرَّح به، لا بصمتٍ ولا بتخطٍّ."""

        return tuple(token for token in self.tokens if not token.is_read_in_a_ledger)

    @property
    def genus_counts(self) -> Mapping[CitedSourceGenus, int]:
        """تعدادُ الرموز بحسب جنسها، وكلّ جنسِ رمزٍ حاضرٌ ولو بصفر."""

        counts = dict.fromkeys(_TOKEN_GENERA, 0)
        for token in self.tokens:
            counts[token.genus] += 1
        return MappingProxyType(counts)

    @property
    def shape_counts(self) -> Mapping[CitedTokenShape, int]:
        """تعدادُ الرموز بحسب شكلها المكتوب، وكلّ شكلٍ حاضرٌ ولو بصفر."""

        counts = dict.fromkeys(CitedTokenShape, 0)
        for token in self.tokens:
            counts[token.shape] += 1
        return MappingProxyType(counts)


@dataclass(frozen=True, slots=True)
class AimCitationLink:
    """رابطُ غايةٍ واحدة بمصادرها المقروءة، مُشتَقًّا من نصّ استشهادها وحده.

    لا حقلَ عددٍ ولا حقلَ نتيجةٍ ولا حقلَ بلوغ: قيامُ الرابط هو الربط نفسه،
    وكلُّ عددٍ خاصّيةٌ تُحسَب، وأعدادُ القرّاء الثلاثة تبقى مفصولةً لا مجموعة.
    """

    aim_id: AimId
    tokens: tuple[ReadCitation, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.aim_id, AimId):
            raise AimIndicatorError("معرّف الغاية من مفردته المغلقة")
        if not isinstance(self.tokens, tuple) or not self.tokens:
            raise AimIndicatorError(
                f"{self.aim_id.value}: استشهادٌ بلا رمزٍ واحد مقروء — "
                "مستندُ الغاية لازمٌ في السجلّ، وخلوُّه من كلّ شكلٍ مُصرَّح به "
                "يُقرَأ «لا مستند» وهو ادّعاءٌ لم تُقرَأ الوثيقة لأجله"
            )
        previous_offset = -1
        for token in self.tokens:
            if not isinstance(token, ReadCitation):
                raise AimIndicatorError("كل عنصرٍ رمزٌ مرصود")
            if token.aim_id is not self.aim_id:
                raise AimIndicatorError(
                    f"رمزٌ من استشهاد {token.aim_id.value} في رابط "
                    f"{self.aim_id.value}: الرمز لا يُنسَب إلى غير غايته"
                )
            if token.offset <= previous_offset:
                raise AimIndicatorError("ترتيب الرموز ترتيبُ ورودها في الاستشهاد")
            previous_offset = token.offset

    def references_of_genus(self, genus: CitedSourceGenus) -> tuple[str, ...]:
        """مراجعُ جنسٍ بعينه بترتيب ورودها، لا مجموعةً واحدة عبر الأجناس."""

        if not isinstance(genus, CitedSourceGenus):
            raise AimIndicatorError("جنس المصدر من مفردته المغلقة")
        if genus is CitedSourceGenus.NO_LEDGER_READABLE_SOURCE:
            raise AimIndicatorError("عضوُ الجهل رتبةُ غايةٍ لا جنسُ رمز، فلا مراجعَ تُطلَب به")
        return tuple(token.reference for token in self.tokens if token.genus is genus)

    @property
    def law_rows(self) -> tuple[str, ...]:
        """صفوفُ الدستور التي بلغها استشهادُ الغاية، بترتيب ورودها."""

        return self.references_of_genus(CitedSourceGenus.CONSTITUTION_LAW_ROW)

    @property
    def audit_questions(self) -> tuple[str, ...]:
        """أسئلةُ التدقيق التي بلغها استشهادُ الغاية، بترتيب ورودها."""

        return self.references_of_genus(CitedSourceGenus.AUDIT_QUESTION)

    @property
    def deferred_values(self) -> tuple[str, ...]:
        """القيمُ المحجوزة التي بلغها استشهادُ الغاية، بترتيب ورودها."""

        return self.references_of_genus(CitedSourceGenus.DEFERRED_VALUE_SITE)

    @property
    def law_row_count(self) -> int:
        """عددُ صفوف الدستور المبلوغة، محسوبًا وحده لا مجموعًا إلى غيره."""

        return len(self.law_rows)

    @property
    def audit_question_count(self) -> int:
        """عددُ أسئلة التدقيق المبلوغة، محسوبًا وحده لا مجموعًا إلى غيره."""

        return len(self.audit_questions)

    @property
    def deferred_value_count(self) -> int:
        """عددُ القيم المحجوزة المبلوغة، محسوبًا وحده لا مجموعًا إلى غيره."""

        return len(self.deferred_values)

    @property
    def ledger_backed_genera(self) -> tuple[CitedSourceGenus, ...]:
        """أجناسُ المصادر المقروءة في دفاتر §٤، أو عضوُ الجهل صريحًا."""

        reached = tuple(
            genus
            for genus in _TOKEN_GENERA
            if genus.is_read_in_a_ledger
            and any(token.genus is genus for token in self.tokens)
        )
        if reached:
            return reached
        return (CitedSourceGenus.NO_LEDGER_READABLE_SOURCE,)

    @property
    def has_ledger_readable_source(self) -> bool:
        """أبلغ استشهادُ الغاية دفترًا من الثلاثة؟ والغيابُ قيمةٌ لا فراغ."""

        return CitedSourceGenus.NO_LEDGER_READABLE_SOURCE not in (
            self.ledger_backed_genera
        )


@dataclass(frozen=True, slots=True)
class AimIndicator:
    """المؤشر المعرفيّ: روابطُ الغايات بمصادرها المقروءة، وإحصاءُ رموزها.

    وهو مؤشرُ **استنادٍ** لا مؤشرُ بلوغ: لا يحمل رتبةَ بلوغٍ ولا يُغيّرها ولا
    يُرتّب الغايات، ولا يجمع أعداد القرّاء الثلاثة في رقمٍ واحد.
    """

    links: tuple[AimCitationLink, ...]
    citations: CitationCensus

    def __post_init__(self) -> None:
        if not isinstance(self.links, tuple) or not self.links:
            raise AimIndicatorError("روابط الغايات مجموعةٌ غير فارغة")
        if not isinstance(self.citations, CitationCensus):
            raise AimIndicatorError("إحصاء الرموز من نوعه")
        seen: set[AimId] = set()
        for link in self.links:
            if not isinstance(link, AimCitationLink):
                raise AimIndicatorError("كل عنصرٍ رابطُ غايةٍ مقروء")
            if link.aim_id in seen:
                raise AimIndicatorError(
                    f"غايةٌ مكرّرة: {link.aim_id.value} — التكرار يُفسد التعداد "
                    "ولا يُطوى"
                )
            seen.add(link.aim_id)
        linked_tokens = tuple(token for link in self.links for token in link.tokens)
        if linked_tokens != self.citations.tokens:
            raise AimIndicatorError(
                "إحصاءُ الرموز يخالف رموزَ الروابط: إحصاءٌ ناقصٌ أو زائد يُقرَأ "
                f"قراءةً تامّة — {UNKNOWN_CITATION_TOKEN_IS_REFUSED_NOTE}"
            )

    @property
    def linked_aim_count(self) -> int:
        """عدد الغايات المربوطة بمصادرها، محسوبًا لا مكتوبًا."""

        return len(self.links)

    def link(self, aim_id: AimId) -> AimCitationLink:
        """رابطُ غايةٍ بعينها؛ وغيابُه رفضٌ مُسمّى لا `None` يُطوى."""

        if not isinstance(aim_id, AimId):
            raise AimIndicatorError("معرّف الغاية من مفردته المغلقة")
        for link in self.links:
            if link.aim_id is aim_id:
                return link
        raise AimIndicatorError(f"لا رابطَ لهذه الغاية: {aim_id.value}")

    @property
    def aims_without_ledger_readable_source(self) -> tuple[AimId, ...]:
        """الغايات التي لا يبلغ استشهادُها دفترًا، مُسمّاةً لا مطويّة."""

        return tuple(
            link.aim_id for link in self.links if not link.has_ledger_readable_source
        )

    def reached_references(self, genus: CitedSourceGenus) -> tuple[str, ...]:
        """مراجعُ جنسٍ بعينه عبر الغايات كلِّها، بلا تكرارٍ وبترتيب ورودها."""

        if not isinstance(genus, CitedSourceGenus):
            raise AimIndicatorError("جنس المصدر من مفردته المغلقة")
        if genus is CitedSourceGenus.NO_LEDGER_READABLE_SOURCE:
            raise AimIndicatorError("عضوُ الجهل رتبةُ غايةٍ لا جنسُ رمز، فلا مراجعَ تُطلَب به")
        seen: list[str] = []
        for link in self.links:
            for reference in link.references_of_genus(genus):
                if reference not in seen:
                    seen.append(reference)
        return tuple(seen)


def _assert_no_fields_matching(
    declaring_type: type, markers: tuple[str, ...], message: str
) -> None:
    for item in fields(declaring_type):
        if any(marker in item.name for marker in markers):
            raise RuntimeError(message)


for _declaring_type in (ReadCitation, CitationCensus, AimCitationLink, AimIndicator):
    _assert_no_fields_matching(
        _declaring_type,
        _ANSWER_BEARING_FIELD_MARKERS,
        "an indicator type may not carry an answer, verdict, or attainment field",
    )


@dataclass(frozen=True, slots=True)
class _CitationSources:
    """مراجعُ القراءة مجموعةً في موضعٍ واحد، داخليةً لا مُصدَّرة."""

    law_rows_by_identifier: Mapping[str, str]
    law_rows_by_name: Mapping[str, str]
    audit_questions: Mapping[str, str]
    deferred_values: Mapping[str, str]
    headings: tuple[str, ...]
    claim_lines: frozenset[str]
    repository_root: Path


def _law_row_identifier(law: str) -> str:
    head = law.split(" ", 1)[0]
    return head if _ROW_IDENTIFIER_SHAPE.match(head) else ""


def _collect_sources(
    constitution: ConstitutionLedger,
    deferred_values: DeferredValueLedger,
    document_text: str,
    repository_root: Path,
) -> _CitationSources:
    rows_by_identifier: dict[str, str] = {}
    rows_by_name: dict[str, str] = {}
    for row in constitution.laws.rows:
        rows_by_name[row.law] = row.law
        identifier = _law_row_identifier(row.law)
        if identifier:
            if identifier in rows_by_identifier:
                raise AimIndicatorError(
                    f"معرّفُ صفٍّ مكرّر في الدستور: {identifier} — الترجيح بين "
                    "صفّين بمعرّفٍ واحد حكمٌ لا يملكه هذا الرابط"
                )
            rows_by_identifier[identifier] = row.law

    questions = {
        question.name: question.name
        for question in constitution.audit_questions.questions
    }
    values = {site.member_name: site.member_name for site in DeferredValueSite}
    if tuple(values) != tuple(
        row.site.member_name for row in deferred_values.rows
    ):  # pragma: no cover - guard
        raise AimIndicatorError(
            "دفترُ القيم المحجوزة لا يوافق مواضعَه المُعلَنة، فلا يُقرَأ منه مرجع"
        )

    headings: list[str] = []
    claim_lines: set[str] = set()
    for line in document_text.splitlines():
        heading = _HEADING_LINE.match(line)
        if heading is not None:
            headings.append(heading.group("heading").strip())
            continue
        claim = _CLAIM_LINE.match(line)
        if claim is not None:
            claim_lines.add(claim.group("claim").strip())

    return _CitationSources(
        law_rows_by_identifier=MappingProxyType(rows_by_identifier),
        law_rows_by_name=MappingProxyType(rows_by_name),
        audit_questions=MappingProxyType(questions),
        deferred_values=MappingProxyType(values),
        headings=tuple(headings),
        claim_lines=frozenset(claim_lines),
        repository_root=repository_root,
    )


def _heading_reference(text: str, sources: _CitationSources) -> str:
    for heading in sources.headings:
        if heading == text or heading.startswith(f"{text} —"):
            return heading
    return ""


def _resolve_token(
    aim_id: AimId,
    shape: CitedTokenShape,
    text: str,
    offset: int,
    sources: _CitationSources,
) -> ReadCitation:
    """اشتقّ مرجعَ الرمز وجنسَه، ورُدَّ ما لا مرجعَ له باسمه وموضعه."""

    genus: CitedSourceGenus | None = None
    reference = ""

    if _REPOSITORY_PATH_SHAPE.match(text):
        if (sources.repository_root / text).exists():
            genus = CitedSourceGenus.REPOSITORY_PATH
            reference = text
    elif _ROW_IDENTIFIER_SHAPE.match(text):
        law = sources.law_rows_by_identifier.get(text, "")
        if law:
            genus = CitedSourceGenus.CONSTITUTION_LAW_ROW
            reference = law
        else:
            heading = _heading_reference(text, sources)
            if heading:
                genus = CitedSourceGenus.CONSTITUTION_SECTION
                reference = heading
    else:
        law = sources.law_rows_by_name.get(text, "") or sources.law_rows_by_name.get(
            f"`{text}`", ""
        )
        question = sources.audit_questions.get(text, "")
        value = sources.deferred_values.get(text, "")
        heading = _heading_reference(text, sources)
        if law:
            genus = CitedSourceGenus.CONSTITUTION_LAW_ROW
            reference = law
        elif question:
            genus = CitedSourceGenus.AUDIT_QUESTION
            reference = question
        elif value:
            genus = CitedSourceGenus.DEFERRED_VALUE_SITE
            reference = value
        elif heading:
            genus = CitedSourceGenus.CONSTITUTION_SECTION
            reference = heading
        elif text in sources.claim_lines:
            genus = CitedSourceGenus.CONSTITUTION_CLAIM_LINE
            reference = text

    if genus is None:
        raise AimIndicatorError(
            f"{aim_id.value}: رمزٌ لا مرجعَ له في الموضع {offset}: {text} — "
            f"{UNKNOWN_CITATION_TOKEN_IS_REFUSED_NOTE}"
        )
    return ReadCitation(
        aim_id=aim_id,
        shape=shape,
        text=text,
        genus=genus,
        reference=reference,
        offset=offset,
    )


_SHAPE_BY_GROUP: Final[Mapping[str, CitedTokenShape]] = MappingProxyType(
    {
        "guillemet": CitedTokenShape.GUILLEMET_SPAN,
        "backtick": CitedTokenShape.BACKTICK_SPAN,
        "path": CitedTokenShape.REPOSITORY_PATH_TEXT,
        "row_id": CitedTokenShape.DOTTED_ROW_IDENTIFIER,
        "camel": CitedTokenShape.BARE_JOINED_NAME,
    }
)

if set(_SHAPE_BY_GROUP.values()) != set(CitedTokenShape):  # pragma: no cover - guard
    raise RuntimeError("every declared token shape must have a reading group")


def _read_link(record: AimRecord, sources: _CitationSources) -> AimCitationLink:
    tokens: list[ReadCitation] = []
    for match in _TOKEN_PATTERN.finditer(record.citation):
        group = match.lastgroup
        if group is None or group not in _SHAPE_BY_GROUP:  # pragma: no cover - guard
            raise AimIndicatorError(
                f"{record.aim_id.value}: شكلُ رمزٍ بلا مجموعةٍ مُصرَّح بها — "
                f"{UNKNOWN_CITATION_TOKEN_IS_REFUSED_NOTE}"
            )
        text = (match.group(group) or "").strip()
        if not text:
            raise AimIndicatorError(
                f"{record.aim_id.value}: رمزٌ فارغ في الموضع {match.start()} — "
                f"{UNKNOWN_CITATION_TOKEN_IS_REFUSED_NOTE}"
            )
        tokens.append(
            _resolve_token(
                record.aim_id, _SHAPE_BY_GROUP[group], text, match.start(), sources
            )
        )
    return AimCitationLink(aim_id=record.aim_id, tokens=tuple(tokens))


def constitution_repository_root() -> Path:
    """جذرُ المستودع مشتقًّا من موضع هذه الوحدة، لا مكتوبًا ولا مُمرَّرًا."""

    return Path(__file__).resolve().parents[3]


def derive_aim_indicator(
    records: Mapping[AimId, AimRecord] = AIM_RECORDS,
    constitution: ConstitutionLedger | None = None,
    deferred_values: DeferredValueLedger | None = None,
    document_text: str | None = None,
) -> AimIndicator:
    """اربط كلّ غايةٍ بمصادرها المقروءة من نصّ استشهادها، ورُدَّ ما لا مرجعَ له."""

    if not isinstance(records, Mapping) or not records:
        raise AimIndicatorError("سجلّ الغايات مفردٌ غير فارغ")
    for aim_id, record in records.items():
        if not isinstance(record, AimRecord):
            raise AimIndicatorError("كل عنصرٍ سجلُّ غايةٍ")
        if record.aim_id is not aim_id:
            raise AimIndicatorError(
                f"مفتاحُ السجلّ {aim_id.value} يخالف معرّفه {record.aim_id.value}"
            )

    repository_root = constitution_repository_root()
    if document_text is None:
        document = constitution_document_path()
        try:
            text = document.read_text(encoding="utf-8")
        except OSError as error:
            raise AimIndicatorError(
                f"تعذّرت قراءة وثيقة الدستور عند {document}: رابطٌ فارغ يُقرَأ "
                "«لا مصادر للغايات» وهو ادّعاءٌ لم تُقرَأ الوثيقة لأجله"
            ) from error
    else:
        text = _require_non_blank(document_text, "نصّ وثيقة الدستور")

    ledger = read_constitution_ledger(text) if constitution is None else constitution
    if not isinstance(ledger, ConstitutionLedger):
        raise AimIndicatorError("دفتر الدستور من نوعه")
    values = (
        read_deferred_value_ledger() if deferred_values is None else deferred_values
    )
    if not isinstance(values, DeferredValueLedger):
        raise AimIndicatorError("دفتر القيم المحجوزة من نوعه")

    sources = _collect_sources(ledger, values, text, repository_root)
    links = tuple(_read_link(record, sources) for record in records.values())
    tokens = tuple(token for link in links for token in link.tokens)
    return AimIndicator(links=links, citations=CitationCensus(tokens=tokens))


__all__ = [
    "AIM_INDICATOR_AUTHORITY_NOTE",
    "CITATION_LINK_IS_NOT_ATTAINMENT",
    "CITATION_PROSE_IS_NOT_A_TOKEN_STREAM",
    "DEFERRAL_WAS_NOT_A_PERMANENT_BOUNDARY_NOTE",
    "DEFERRED_VALUE_READER_IS_NOT_REACHED_BY_ANY_CITATION",
    "DESIGN_SOURCE_CITATION_NOTE",
    "LEDGER_COUNT_MOVEMENT_IS_NOT_AIM_MOVEMENT",
    "NAMED_RESIDUALS",
    "NO_SUM_ACROSS_READERS_NOTE",
    "UNKNOWN_CITATION_TOKEN_IS_REFUSED_NOTE",
    "AimCitationLink",
    "AimIndicator",
    "AimIndicatorError",
    "CitationCensus",
    "CitedSourceGenus",
    "CitedTokenShape",
    "ReadCitation",
    "constitution_repository_root",
    "derive_aim_indicator",
]
