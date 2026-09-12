"""قارئا الاشتقاق: صفوف الدستور وأسئلة تدقيقه، مقروءةً آليًّا بلا تقدير.

هذه **المرحلة الثانية من الطور الثاني** لـ AIM.1. المرحلة الأولى
(`alghanem.program.aims`) أنشأت سجلّ الغايات وحده وصرّحت بأن «قارئَي الاشتقاق
(تعداد صفوف الدستور، وتعداد أسئلة التدقيق) والمؤشرَ المُشتَقّ منهما مؤجَّلان».
وهذه الوحدة تُنشئ **القارئَين وحدهما**، ولا تُنشئ المؤشر::

    DocumentProse      != DerivedLedger
    DerivedCount       != Indicator
    ConstitutionLedger != Authority

**لا مؤشر هنا، ولا ربط بغاية.** لا تستورد هذه الوحدة `AimRecord` ولا `AimId`،
ولا تحمل حقلًا يُنسَب إلى غاية، ولا تُرجِّح صفًّا على صفّ. فربطُ العدد بالغاية هو
المؤشر بعينه، وهو المرحلة التالية المُقيَّدة سلفًا بـ§٤ من `docs/AIMS.md`؛
وبناؤه في الدفعة نفسها يجعل القارئ يُصمَّم على مقاس جوابٍ مرغوب.

**العدد خاصّيةٌ تُحسَب لا حقلٌ يُكتَب** (§٤): لا حقلَ عددٍ في أيّ صنفٍ هنا؛
التعداد خاصّيةٌ مشتقّة من الصفوف المقروءة، فلا يمكن كتابة عددٍ يخالف الأثر.

**المصدر التصميمي المباشر، مُستشهَدًا به لا مُعادًا اشتقاقه.** شكلُ «الوثيقة
تُعلن حالةً، والقارئ لا يقبل إلا من مفردةٍ مغلقة يملكها هو، والمخالفة تُرفَض عند
الإنشاء» مأخوذٌ من سؤال التدقيق المفتوح `DeclaredVersusDerivedRecurrenceNotExplained`
بوصفه **مصدرًا مباشرًا** (إلزام §٥ من `docs/AIMS.md`)، لا بوصفه بديهةً تُعاد
هنا صامتةً. وذلك السؤال مرصودٌ غير مفسَّر، فلا يُستحدَث له هنا اسمٌ عامّ ولا صنفُ
أساسٍ مشترك يوحّد الشكل بين القارئَين؛ يُستعمل في موضعه ويُنسَب إلى سؤاله.

**الرفض لا التخطّي الصامت.** حالةٌ في عمود الوثيقة خارج المفردة المغلقة تُوقف
القراءة باستثناءٍ مُسمّى، ولا يُتخطّى الصفّ. فالتخطّي يُنتج جدولًا ناقصًا يُقرَأ
لاحقًا «لا صفوف مؤجَّلة هنا»، وهو خطأٌ أخطر من التوقّف؛ وتعدادٌ صامتُ النقص أسوأ
من غياب تعداد.

**والقاعدة نفسها تُرفَع طبقةً: من الخلية إلى الجدول.** كان اختيارُ الجداول
بترويسةِ `Law | Status` شرطَ صحّة، لكنّ *عدم* الاختيار كان صامتًا: جدولُ قوانينَ
ترويستُه مختلفةٌ قليلًا (مسافةٌ زائدة، حرفٌ كبير مغاير، اسمٌ مجاور) يسقط من
التعداد بلا خطأٍ يُرفَع، لأن شيئًا لم *يتعارض*، بل شيئًا **لم يُحسَب أصلًا**.
فصار للترويسات مفردةٌ مغلقة مُستخرَجة من الوثيقة كما استُخرجت مفردةُ الحالات،
وكلّ جدولٍ إمّا مقروءٌ أو مُستبعَدٌ مُصرَّحًا به أو مرفوضٌ باسمه؛ ولا تخطّي صامت.

**والقاعدة نفسها تُرفَع طبقةً ثانية هنا: من الجدول إلى نقطة سؤال التدقيق.** كان
قارئُ الأسئلة يُطابق شكلًا واحدًا متوقَّعًا ويتخطّى ما عداه صامتًا: نقطةٌ عليا
كُتبت بشكلٍ آخر تسقط بلا خطأ فيسقط سؤالُها من التعداد، ووسمٌ فرعيٌّ غيرُ معروف
يُقرَأ فراغًا فيُقرَأ سؤالٌ ناطقٌ بحالته «لا حالة مُعلَنة في السجل». فصار لأشكال
النقطة العليا مفردةٌ مغلقة (`DeclaredQuestionBulletShape`) ولوسوم النقاط الفرعية
مفردةٌ مغلقة (`DeclaredQuestionBulletLabel`) فيها الوسومُ المقروءة والوسومُ
**المُستبعَدة مُصرَّحًا باستبعادها**، على منهج `DeclaredTableHeader`؛ وكلّ نقطةٍ
في القسمين إمّا مقروءةٌ أو مُستبعَدةٌ بوسمٍ مُصرَّح به أو مرفوضةٌ باسمها وموضعها،
وتُحصى كلُّها في `QuestionBulletCensus`. ووسمٌ يتكرّر في السؤال الواحد يُرفَض ولا
يُرجَّح أوّلُه، ونقطةٌ فرعيةٌ قبل أوّل سؤالٍ مُسمّى وسمٌ بلا صاحبٍ فتُرفَض.

**وما بقي بعد ذلك مُسمّى لا مطويّ** (`NAMED_RESIDUALS`): الوثيقة لا تُعلن مجموعًا
يُقابَل بالمُشتَقّ، فالتعدادُ قائمٌ على «لم يُكتشَف نقص» لا على «أُثبِت عدم وجود
نقص»؛ ومفردةُ الوسوم مُستخرَجةٌ من نصّ اليوم ولا صفَّ في الدستور يُلزم السؤال
بشكلٍ منها؛ ووسمٌ مُستبعَدٌ مُصرَّحٌ باستبعاده قد يحمل غدًا حالةً مُعلَنة فيسقط
بلا رفض. وهذه حدودٌ صادقة يُصرَّح بها، لا عيوبٌ تُخفى ولا ثقةٌ تُدَّعى.

**الجهل عضوٌ في المفردة لا فراغٌ يُطوى** (§٤): سؤالُ تدقيقٍ مفتوحٌ لا يُصرّح
السجلّ بحالته يحمل `NO_STATUS_DECLARED_IN_RECORD`، لا سلسلةً فارغة تُقرَأ لاحقًا
`OPEN` بحكم موقعها.

**خمولٌ سلطويّ**: `ConstitutionLedger != BirthVerdict`؛ لا تُصدر هذه الوحدة
ولادةً ولا حكمًا ولا تجميدًا ولا `E0`، ولا ترفع حالة أيّ صفٍّ في الدستور ولا
تُغيّرها، ولا تقرؤها أيّ وحدةٍ في `kernel/`، وهو ما يفحصه اختبارٌ يمسح كل وحداتها.

**وترتيب الصفوف ترتيبُ ورودها في الوثيقة**، لا ترتيبَ أهمّية ولا أولوية (§٦).
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from types import MappingProxyType
from typing import Final

from .aims import DESIGN_SOURCE_OPEN_QUESTION

CONSTITUTION_RELATIVE_PATH: Final = "docs/CONSTITUTION.md"

NO_STATUS_DECLARED_IN_RECORD: Final = "لا_حالة_مُعلَنة_في_السجل"

LEDGER_AUTHORITY_NOTE: Final = (
    "قراءةٌ فقط: لا يُنتج هذا الدفتر ولادةً ولا حكمًا ولا تجميدًا ولا `E0`، "
    "ولا يُغيّر حالة صفٍّ في الدستور، ولا تقرؤه بوّابةٌ في النواة"
)

NO_INDICATOR_IN_THIS_READER_NOTE: Final = (
    "لا مؤشر في هذه المرحلة ولا ربطَ بغاية: القارئان وحدهما مُنشآن هنا، "
    "وربطُ العدد بغايةٍ بعينها هو المؤشر نفسه، وهو مرحلةٌ تالية"
)

DESIGN_SOURCE_CITATION_NOTE: Final = (
    "شكلُ «الوثيقة تُعلن، والقارئ لا يقبل إلا من مفردةٍ مغلقة يملكها، "
    f"والمخالفة تُرفَض» مأخوذٌ من `{DESIGN_SOURCE_OPEN_QUESTION}` مصدرًا "
    "مباشرًا، لا بديهةً تُعاد هنا صامتةً"
)

UNKNOWN_STATUS_IS_REFUSED_NOTE: Final = (
    "حالةٌ خارج المفردة المغلقة تُوقف القراءة ولا يُتخطّى صفّها: التخطّي "
    "الصامت يُنتج تعدادًا ناقصًا يُقرَأ جدولًا تامًّا"
)

UNKNOWN_TABLE_HEADER_IS_REFUSED_NOTE: Final = (
    "ترويسةٌ خارج المفردة المغلقة تُوقف القراءة ولا يُتخطّى جدولها: الجدولُ "
    "غيرُ المُطابَق لا يتعارض مع شيءٍ لأنه لم يُحسَب أصلًا، والسقوطُ الصامت "
    "لجدولٍ كامل أخطر من رفضٍ مُسمّى"
)

TABLE_HEADER_MATCH_COMPLETENESS_UNVERIFIED: Final = (
    "TABLE_HEADER_MATCH_COMPLETENESS_UNVERIFIED"
)

NO_DECLARED_TOTAL_TO_CROSS_CHECK: Final = "NO_DECLARED_TOTAL_TO_CROSS_CHECK"

UNKNOWN_QUESTION_BULLET_IS_REFUSED_NOTE: Final = (
    "نقطةٌ في قسمَي الأسئلة خارج مفردتَي الأشكال والوسوم تُوقف القراءة ولا "
    "تُتخطّى: النقطةُ الساقطة لا تتعارض مع شيءٍ لأنها لم تُقرَأ أصلًا، فيُقرَأ "
    "سؤالٌ ناقصٌ أو يسقط سؤالٌ بتمامه بلا أثرٍ يدلّ عليه"
)

QUESTION_BULLET_LABEL_VOCABULARY_IS_NOT_DECLARED_IN_RECORD: Final = (
    "QUESTION_BULLET_LABEL_VOCABULARY_IS_NOT_DECLARED_IN_RECORD"
)

EXCLUDED_QUESTION_BULLET_MAY_CARRY_A_DECLARED_STATUS: Final = (
    "EXCLUDED_QUESTION_BULLET_MAY_CARRY_A_DECLARED_STATUS"
)

NAMED_RESIDUALS: Final[Mapping[str, str]] = MappingProxyType(
    {
        TABLE_HEADER_MATCH_COMPLETENESS_UNVERIFIED: (
            "صار كلّ جدولٍ في الوثيقة إمّا مقروءًا أو مُستبعَدًا بترويسةٍ "
            "مُصرَّح بها أو مرفوضًا باسمه، فانتفى التخطّي الصامت؛ وتبقى حالةٌ "
            "غيرُ قابلةٍ للكشف من داخل النصّ: جدولُ قوانينَ كُتبت ترويستُه "
            "بترويسةٍ أخرى مُصرَّح باستبعادها يُستبعَد بلا رفض"
        ),
        NO_DECLARED_TOTAL_TO_CROSS_CHECK: (
            "الوثيقة لا تُصرّح بمجموع صفوفها ولا بعدد أسئلتها، فالتعدادُ "
            "المُشتَقّ قائمٌ على «لم يُرفَع خطأ» لا على مقابلةٍ بعددٍ مرجعيّ "
            "مستقلّ: «لم يُكتشَف نقص» لا «أُثبِت عدم وجود نقص»؛ واستحداثُ عددٍ "
            "«مُعلَن» في الوثيقة لإغلاقه افتعالٌ لا تحقّق، فقاعدة «المخالفة "
            "تُرفَض لا تُقرَّر» تفترض قيمةً مُعلَنةً أصلًا"
        ),
        QUESTION_BULLET_LABEL_VOCABULARY_IS_NOT_DECLARED_IN_RECORD: (
            "مفردتا شكل النقطة العليا ووسم النقطة الفرعية مُستخرَجتان من نصّ "
            "الوثيقة اليوم، ولا صفَّ في الدستور يُلزم سؤال التدقيق بشكلٍ منهما؛ "
            "فوسمٌ جديدٌ يُكتَب غدًا يُرفَع به خطأٌ هنا باسمه، وهو رفضُ القارئ "
            "لا إلزامُ السجلّ"
        ),
        EXCLUDED_QUESTION_BULLET_MAY_CARRY_A_DECLARED_STATUS: (
            "صارت كلّ نقطةٍ إمّا مقروءةً أو مُستبعَدةً بوسمٍ مُصرَّح به أو "
            "مرفوضةً باسمها، فانتفى التخطّي الصامت؛ وتبقى حالةٌ غيرُ قابلةٍ "
            "للكشف من داخل النصّ: حالةٌ مُعلَنة تُكتَب غدًا تحت وسمٍ مُصرَّح "
            "باستبعاده تُستبعَد بلا رفض، إذ الاستبعاد على الوسم لا على المحتوى"
        ),
    }
)

_OPEN_SECTION_HEADING: Final = "### OpenAuditQuestions"
_RESOLVED_SECTION_HEADING: Final = "### ResolvedAuditQuestions"

_UNESCAPED_PIPE: Final = re.compile(r"(?<!\\)\|")
_TOP_LEVEL_NAME_ONLY: Final = re.compile(r"^- `(?P<name>[^`]+)`$")
_TOP_LEVEL_NAME_WITH_INLINE_NOTE: Final = re.compile(r"^- `(?P<name>[^`]+)`: \S.*$")
_SUB_BULLET: Final = re.compile(r"^\s+- (?P<body>.*)$")


class ConstitutionLedgerError(ValueError):
    """قراءةٌ مرفوضة؛ لا تُحمَل الوثيقة على أقرب شكلٍ مقبول."""


class DeclaredLawStatus(Enum):
    """حالات صفوف الدستور كما وردت نصًّا، مفردةً مغلقة مُستخرَجة لا مُبتكَرة."""

    ENFORCED = "ENFORCED"
    PARTIALLY_ENFORCED = "PARTIALLY_ENFORCED"
    ENFORCED_AT_CONTENT_ENCODER = "ENFORCED_AT_CONTENT_ENCODER"
    ENFORCED_AT_INVARIANT_GATE = "ENFORCED_AT_INVARIANT_GATE"
    ENFORCED_AT_VERDICT_GATE = "ENFORCED_AT_VERDICT_GATE"
    ENFORCED_AT_CLOSURE_GATE = "ENFORCED_AT_CLOSURE_GATE"
    ENFORCED_AT_EXECUTION_GATE = "ENFORCED_AT_EXECUTION_GATE"
    ENFORCED_AT_DERIVATION_GATE = "ENFORCED_AT_DERIVATION_GATE"
    ENFORCED_AT_ACQUISITION_AUTHORITY = "ENFORCED_AT_ACQUISITION_AUTHORITY"
    ENFORCED_AT_PROBE_PREREGISTRATION = "ENFORCED_AT_PROBE_PREREGISTRATION"
    ENFORCED_AT_CANONICAL_PRIMITIVE = "ENFORCED_AT_CANONICAL_PRIMITIVE"
    ENFORCED_AT_READINESS_RECORD = "ENFORCED_AT_READINESS_RECORD"
    ENFORCED_AT_IMPORT_CONTRACT = "ENFORCED_AT_IMPORT_CONTRACT"
    ENFORCED_AT_INTERVENTION_FOOTPRINT = "ENFORCED_AT_INTERVENTION_FOOTPRINT"
    ENFORCED_AT_AIM_RECORD = "ENFORCED_AT_AIM_RECORD"
    ENFORCED_AT_WAD_NAQL = "ENFORCED_AT_WAD_NAQL"
    ENFORCED_AT_UMUM_KHUSUS = "ENFORCED_AT_UMUM_KHUSUS"
    ENFORCED_AT_DECISION_CHAIN = "ENFORCED_AT_DECISION_CHAIN"
    PROVED_AT_CONTRACT_LEVEL = "PROVED (at contract level)"
    PROVED_WITHIN_PROVIDER_SCOPE = "PROVED (within provider scope)"
    CONSTITUTIONAL_REQUIREMENT = "CONSTITUTIONAL REQUIREMENT"
    DECLARED_DEFERRED = "DECLARED_DEFERRED"
    DECLARED_DEFERRED_CONTRACT_ONLY = "DECLARED_DEFERRED_CONTRACT_ONLY"
    DECLARED_LAW_ONLY = "DECLARED_LAW_ONLY"
    DOCUMENTED_OPEN_QUESTION = "DOCUMENTED_OPEN_QUESTION"
    DOCUMENTED_CLASSIFICATION_ONLY = "DOCUMENTED_CLASSIFICATION_ONLY"


class AuditQuestionStanding(Enum):
    """موقف سؤال التدقيق كما قسّمه الدستور قسمين، لا كما يُقدَّر."""

    OPEN = "OpenAuditQuestions"
    RESOLVED = "ResolvedAuditQuestions"


class DeclaredTableHeader(Enum):
    """ترويسات جداول الوثيقة، مفردةً مغلقة مُستخرَجة من نصّها لا مُبتكَرة.

    القيمة هي العمودان الأوّلان كما وردا نصًّا؛ وما بعدهما وصفُ نطاقٍ لا يُقرَأ
    (`Kernel v0.1 scope` مرّةً و`Scope` مرارًا)، فلا يدخل في التمييز.
    """

    LAW_ROWS = ("Law", "Status")
    EXPLANATORY_CANDIDATES = ("Explanatory candidate", "Piercing question")

    @property
    def carries_law_rows(self) -> bool:
        """أجدولُ قوانينَ هذا؟ الاستبعادُ مُصرَّحٌ به لا مُستنتَجٌ من صمت."""

        return self is DeclaredTableHeader.LAW_ROWS


class DeclaredQuestionBulletShape(Enum):
    """أشكال النقطة العليا في قسمَي الأسئلة، مفردةً مغلقة مُستخرَجة من النصّ.

    الشكلان قائمان في الوثيقة معًا: سؤالٌ اسمُه وحده ثم نقاطٌ فرعية تحته،
    وسؤالٌ يليه نصٌّ داخليّ في سطره نفسه. ودمجُهما في شكلٍ واحدٍ متساهل يُعيد
    التخطّي الصامت من باب آخر، وإسقاطُ أحدهما يُسقط أسئلةً قائمة.
    """

    NAME_ONLY = "- `Name`"
    NAME_WITH_INLINE_NOTE = "- `Name`: text"


class DeclaredQuestionBulletLabel(Enum):
    """وسوم النقاط الفرعية كما وردت نصًّا، مقروءَها ومُستبعَدَها مُصرَّحًا به.

    على منهج `DeclaredTableHeader`: الاستبعادُ مُعلَنٌ لا مُستنتَجٌ من صمت،
    فوسمٌ خارج هذه المفردة يُرفَض باسمه وموضعه ولا يُقرَأ فراغًا.
    """

    STATUS = "Status"
    PREVIOUS_AUDIT_LABEL = "Previous audit label"
    CLOSURE_LAW = "Closure law"
    NOTE = "Note"
    QUESTION = "Question"
    STANDING_EVIDENCE = "Standing evidence"
    MEASURED_STANDING = "Measured standing"
    NOT_DECIDED_HERE = "Not decided here"
    OBSERVATION = "Observation"
    TWO_DISTINCT_SUB_SHAPES = "Two distinct sub-shapes, not one"
    NOT_A_LAW_AND_NOT_NAMED = "Not a law and not named"

    @property
    def is_read_into_the_row(self) -> bool:
        """أيُقرَأ هذا الوسم في صفّ السؤال؟ الاستبعادُ مُصرَّحٌ به لا مطويّ."""

        return self in _ROW_BEARING_LABELS


_ROW_BEARING_LABELS: Final[frozenset[DeclaredQuestionBulletLabel]] = frozenset(
    {
        DeclaredQuestionBulletLabel.STATUS,
        DeclaredQuestionBulletLabel.PREVIOUS_AUDIT_LABEL,
        DeclaredQuestionBulletLabel.CLOSURE_LAW,
    }
)


_STATUS_BY_TEXT: Final[Mapping[str, DeclaredLawStatus]] = MappingProxyType(
    {member.value: member for member in DeclaredLawStatus}
)

_TABLE_HEADER_BY_COLUMNS: Final[Mapping[tuple[str, ...], DeclaredTableHeader]] = (
    MappingProxyType({member.value: member for member in DeclaredTableHeader})
)

_LABELS_LONGEST_FIRST: Final[tuple[DeclaredQuestionBulletLabel, ...]] = tuple(
    sorted(
        DeclaredQuestionBulletLabel, key=lambda label: len(label.value), reverse=True
    )
)

if len(_STATUS_BY_TEXT) != len(DeclaredLawStatus):  # pragma: no cover - guard
    raise RuntimeError("two law statuses must not share one declared text")
if len(_TABLE_HEADER_BY_COLUMNS) != len(DeclaredTableHeader):  # pragma: no cover
    raise RuntimeError("two table headers must not share one declared column pair")
if len({label.value for label in DeclaredQuestionBulletLabel}) != len(
    DeclaredQuestionBulletLabel
):  # pragma: no cover - guard
    raise RuntimeError("two bullet labels must not share one declared text")
if len(AuditQuestionStanding) != 2:  # pragma: no cover - guard
    raise RuntimeError("audit standing is deliberately two-valued")


def _require_non_blank(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ConstitutionLedgerError(f"{field_name} نصٌّ غير فارغ")
    return value


def _require_blank(value: str, field_name: str, reason: str) -> str:
    if not isinstance(value, str):
        raise ConstitutionLedgerError(f"{field_name} نصّ")
    if value.strip():
        raise ConstitutionLedgerError(f"{field_name} يبقى فارغًا: {reason}")
    return value


def _require_positive_line(value: int, field_name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ConstitutionLedgerError(f"{field_name} رقم سطرٍ موجب")
    return value


@dataclass(frozen=True, slots=True)
class LawRow:
    """صفٌّ واحد من جداول الدستور: اسمه وحالته المُعلَنة وموضعه."""

    law: str
    status: DeclaredLawStatus
    document_line: int

    def __post_init__(self) -> None:
        _require_non_blank(self.law, "اسم الصفّ")
        if not isinstance(self.status, DeclaredLawStatus):
            raise ConstitutionLedgerError("حالة الصفّ من مفردتها المغلقة")
        _require_positive_line(self.document_line, "موضع الصفّ")


@dataclass(frozen=True, slots=True)
class AuditQuestionRow:
    """سؤال تدقيقٍ واحد بموقفه وحالته المُعلَنة، والجهلُ عضوٌ فيها."""

    name: str
    standing: AuditQuestionStanding
    declared_status: str
    document_line: int
    previous_audit_label: str = ""
    closure_law: str = ""

    def __post_init__(self) -> None:
        _require_non_blank(self.name, "اسم سؤال التدقيق")
        if not isinstance(self.standing, AuditQuestionStanding):
            raise ConstitutionLedgerError("موقف السؤال من مفردته المغلقة")
        _require_non_blank(self.declared_status, "حالة السؤال المُعلَنة")
        _require_positive_line(self.document_line, "موضع السؤال")

        if self.standing is AuditQuestionStanding.RESOLVED:
            _require_non_blank(self.previous_audit_label, "الوسم السابق")
            _require_non_blank(self.closure_law, "قانون الإغلاق")
            if self.declared_status == NO_STATUS_DECLARED_IN_RECORD:
                raise ConstitutionLedgerError(
                    "سؤالٌ مُغلَق بلا حالةٍ مُعلَنة: الإغلاق يُسنَد إلى حالته "
                    "المُصرَّح بها في السجلّ لا يُستنتَج من موقعه"
                )
        else:
            _require_blank(
                self.previous_audit_label,
                "الوسم السابق",
                "النَّسَب لا يُذكَر إلا لسؤالٍ أُغلق",
            )
            _require_blank(
                self.closure_law,
                "قانون الإغلاق",
                "قانون الإغلاق لا يُذكَر إلا لسؤالٍ أُغلق",
            )

    @property
    def status_is_declared_in_record(self) -> bool:
        """هل صرّح السجلّ بحالة هذا السؤال؟ الجهلُ قيمةٌ لا فراغ."""

        return self.declared_status != NO_STATUS_DECLARED_IN_RECORD

    @property
    def remains_open(self) -> bool:
        """هل ما زال السؤال مفتوحًا في السجلّ؟"""

        return self.standing is AuditQuestionStanding.OPEN


@dataclass(frozen=True, slots=True)
class ReadTable:
    """جدولٌ واحد كما وُجد في الوثيقة: ترويستُه المُصرَّح بها وموضعُها ونصُّها."""

    declared_header: DeclaredTableHeader
    header_text: str
    header_line: int

    def __post_init__(self) -> None:
        if not isinstance(self.declared_header, DeclaredTableHeader):
            raise ConstitutionLedgerError("ترويسة الجدول من مفردتها المغلقة")
        _require_non_blank(self.header_text, "نصّ الترويسة")
        _require_positive_line(self.header_line, "موضع الترويسة")

    @property
    def carries_law_rows(self) -> bool:
        """أقُرئت صفوفُ هذا الجدول قوانينَ، أم استُبعد بترويسةٍ مُصرَّح بها؟"""

        return self.declared_header.carries_law_rows


@dataclass(frozen=True, slots=True)
class TableCensus:
    """إحصاءُ جداول الوثيقة كلِّها: المقروءُ منها والمُستبعَدُ مُصرَّحًا به.

    لا حقلَ عددٍ هنا أيضًا؛ التعدادُ خاصّيةٌ تُحسَب من الجداول المرصودة، فلا
    يُكتَب عددٌ يخالف الأثر. وحضورُ الجدول المُستبعَد في الإحصاء هو الفارق بين
    «استُبعد بترويسةٍ معروفة» و«لم يُرَ أصلًا».
    """

    tables: tuple[ReadTable, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.tables, tuple) or not self.tables:
            raise ConstitutionLedgerError("إحصاء الجداول مجموعةٌ غير فارغة")
        previous_line = 0
        for table in self.tables:
            if not isinstance(table, ReadTable):
                raise ConstitutionLedgerError("كل عنصرٍ جدولٌ مرصود")
            if table.header_line <= previous_line:
                raise ConstitutionLedgerError("ترتيب الجداول ترتيبُ ورودها في الوثيقة")
            previous_line = table.header_line

    @property
    def table_count(self) -> int:
        """عدد الجداول المرصودة، محسوبًا لا مكتوبًا."""

        return len(self.tables)

    @property
    def law_tables(self) -> tuple[ReadTable, ...]:
        """الجداول التي قُرئت صفوفُها قوانينَ، بترتيب ورودها."""

        return tuple(table for table in self.tables if table.carries_law_rows)

    @property
    def excluded_tables(self) -> tuple[ReadTable, ...]:
        """الجداول المُستبعَدة بترويسةٍ مُصرَّح بها، لا بصمتٍ ولا بتخطٍّ."""

        return tuple(table for table in self.tables if not table.carries_law_rows)


@dataclass(frozen=True, slots=True)
class ReadQuestionBullet:
    """نقطةٌ واحدة من قسمَي الأسئلة، بشكلها المُصرَّح به أو وسمها المُصرَّح به.

    حقلا الشكل والوسم لا يجتمعان ولا يرتفعان: النقطة العليا شكلٌ من مفردته،
    والنقطة الفرعية وسمٌ من مفردته، وما عداهما مرفوضٌ عند القراءة لا مُسجَّلٌ
    هنا. وحضورُ النقطة المُستبعَدة في هذا الأثر هو الفارق بين «استُبعدت بوسمٍ
    معروف» و«لم تُرَ أصلًا».
    """

    document_line: int
    standing: AuditQuestionStanding
    question_name: str
    shape: DeclaredQuestionBulletShape | None = None
    label: DeclaredQuestionBulletLabel | None = None

    def __post_init__(self) -> None:
        _require_positive_line(self.document_line, "موضع النقطة")
        if not isinstance(self.standing, AuditQuestionStanding):
            raise ConstitutionLedgerError("موقف النقطة من مفردته المغلقة")
        _require_non_blank(self.question_name, "اسم سؤال النقطة")
        if self.shape is not None and not isinstance(
            self.shape, DeclaredQuestionBulletShape
        ):
            raise ConstitutionLedgerError("شكل النقطة العليا من مفردته المغلقة")
        if self.label is not None and not isinstance(
            self.label, DeclaredQuestionBulletLabel
        ):
            raise ConstitutionLedgerError("وسم النقطة الفرعية من مفردته المغلقة")
        if (self.shape is None) == (self.label is None):
            raise ConstitutionLedgerError(
                "النقطة إمّا عليا بشكلٍ مُصرَّح به أو فرعيةٌ بوسمٍ مُصرَّح به، "
                "ولا تجمع الاثنين ولا تخلو منهما"
            )

    @property
    def is_question_head(self) -> bool:
        """أنقطةٌ عليا تُسمّي سؤالًا هذه؟"""

        return self.shape is not None

    @property
    def is_read_into_the_row(self) -> bool:
        """أدخلت هذه النقطة في صفّ السؤال، أم استُبعدت بوسمٍ مُصرَّح به؟"""

        return self.label is None or self.label.is_read_into_the_row


@dataclass(frozen=True, slots=True)
class QuestionBulletCensus:
    """إحصاءُ نقاط قسمَي الأسئلة كلِّها: المقروءُ منها والمُستبعَدُ مُصرَّحًا به.

    لا حقلَ عددٍ هنا؛ التعدادُ خاصّيةٌ تُحسَب من النقاط المرصودة. والمرفوضةُ
    لا تبلغ هذا الإحصاء أصلًا، إذ يُوقِفها رفضٌ مُسمّى عند القراءة.
    """

    bullets: tuple[ReadQuestionBullet, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.bullets, tuple) or not self.bullets:
            raise ConstitutionLedgerError("إحصاء النقاط مجموعةٌ غير فارغة")
        previous_line = 0
        for bullet in self.bullets:
            if not isinstance(bullet, ReadQuestionBullet):
                raise ConstitutionLedgerError("كل عنصرٍ نقطةٌ مرصودة")
            if bullet.document_line <= previous_line:
                raise ConstitutionLedgerError("ترتيب النقاط ترتيبُ ورودها في الوثيقة")
            previous_line = bullet.document_line

    @property
    def bullet_count(self) -> int:
        """عدد النقاط المرصودة، محسوبًا لا مكتوبًا."""

        return len(self.bullets)

    @property
    def head_bullets(self) -> tuple[ReadQuestionBullet, ...]:
        """النقاط العليا التي سمّت أسئلةً، بترتيب ورودها."""

        return tuple(bullet for bullet in self.bullets if bullet.is_question_head)

    @property
    def read_bullets(self) -> tuple[ReadQuestionBullet, ...]:
        """النقاط التي دخلت صفوف الأسئلة، بترتيب ورودها."""

        return tuple(bullet for bullet in self.bullets if bullet.is_read_into_the_row)

    @property
    def excluded_bullets(self) -> tuple[ReadQuestionBullet, ...]:
        """النقاط المُستبعَدة بوسمٍ مُصرَّح به، لا بصمتٍ ولا بتخطٍّ."""

        return tuple(
            bullet for bullet in self.bullets if not bullet.is_read_into_the_row
        )


@dataclass(frozen=True, slots=True)
class LawRowLedger:
    """دفتر صفوف الدستور: تعدادُه خاصّيةٌ تُحسَب، ولا حقلَ عددٍ فيه."""

    rows: tuple[LawRow, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.rows, tuple) or not self.rows:
            raise ConstitutionLedgerError("دفتر الصفوف مجموعةٌ غير فارغة")
        seen: set[str] = set()
        previous_line = 0
        for row in self.rows:
            if not isinstance(row, LawRow):
                raise ConstitutionLedgerError("كل عنصرٍ صفٌّ مقروء")
            if row.law in seen:
                raise ConstitutionLedgerError(
                    f"اسم صفٍّ مكرّر: {row.law} — التكرار يُفسد التعداد ولا يُطوى"
                )
            seen.add(row.law)
            if row.document_line <= previous_line:
                raise ConstitutionLedgerError("ترتيب الصفوف ترتيبُ ورودها في الوثيقة")
            previous_line = row.document_line

    @property
    def row_count(self) -> int:
        """عدد الصفوف المقروءة، محسوبًا لا مكتوبًا."""

        return len(self.rows)

    @property
    def status_counts(self) -> Mapping[DeclaredLawStatus, int]:
        """تعدادُ الصفوف بحسب حالتها المُعلَنة، وكل عضوٍ حاضرٌ ولو بصفر."""

        counts = dict.fromkeys(DeclaredLawStatus, 0)
        for row in self.rows:
            counts[row.status] += 1
        return MappingProxyType(counts)

    def rows_with_status(self, status: DeclaredLawStatus) -> tuple[LawRow, ...]:
        """صفوفُ حالةٍ بعينها بترتيب ورودها في الوثيقة."""

        if not isinstance(status, DeclaredLawStatus):
            raise ConstitutionLedgerError("حالة الصفّ من مفردتها المغلقة")
        return tuple(row for row in self.rows if row.status is status)


@dataclass(frozen=True, slots=True)
class AuditQuestionLedger:
    """دفتر أسئلة التدقيق مفتوحِها ومُغلَقِها، بتعدادٍ مُشتَقّ لا مكتوب."""

    questions: tuple[AuditQuestionRow, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.questions, tuple) or not self.questions:
            raise ConstitutionLedgerError("دفتر الأسئلة مجموعةٌ غير فارغة")
        seen: set[str] = set()
        for question in self.questions:
            if not isinstance(question, AuditQuestionRow):
                raise ConstitutionLedgerError("كل عنصرٍ سؤالُ تدقيقٍ مقروء")
            if question.name in seen:
                raise ConstitutionLedgerError(
                    f"سؤالٌ مكرّر: {question.name} — سؤالٌ واحد لا يكون مفتوحًا "
                    "ومُغلَقًا معًا، ولا يُرجَّح أحد موضعيه على الآخر"
                )
            seen.add(question.name)

    @property
    def open_questions(self) -> tuple[AuditQuestionRow, ...]:
        """الأسئلة المفتوحة بترتيب ورودها."""

        return tuple(question for question in self.questions if question.remains_open)

    @property
    def resolved_questions(self) -> tuple[AuditQuestionRow, ...]:
        """الأسئلة المُغلَقة بترتيب ورودها، ونَسَبُها محفوظٌ معها."""

        return tuple(
            question for question in self.questions if not question.remains_open
        )

    @property
    def open_count(self) -> int:
        """عدد الأسئلة المفتوحة، محسوبًا لا مكتوبًا."""

        return len(self.open_questions)

    @property
    def resolved_count(self) -> int:
        """عدد الأسئلة المُغلَقة، محسوبًا لا مكتوبًا."""

        return len(self.resolved_questions)


@dataclass(frozen=True, slots=True)
class ConstitutionLedger:
    """دفترا الاشتقاق معًا كما قُرئا من وثيقةٍ واحدة، بلا مؤشرٍ ولا غاية."""

    laws: LawRowLedger
    audit_questions: AuditQuestionLedger
    tables: TableCensus
    question_bullets: QuestionBulletCensus

    def __post_init__(self) -> None:
        if not isinstance(self.laws, LawRowLedger):
            raise ConstitutionLedgerError("دفتر الصفوف من نوعه")
        if not isinstance(self.audit_questions, AuditQuestionLedger):
            raise ConstitutionLedgerError("دفتر الأسئلة من نوعه")
        if not isinstance(self.tables, TableCensus):
            raise ConstitutionLedgerError("إحصاء الجداول من نوعه")
        if not isinstance(self.question_bullets, QuestionBulletCensus):
            raise ConstitutionLedgerError("إحصاء النقاط من نوعه")


def _split_row(line: str) -> tuple[str, ...]:
    stripped = line.strip()
    cells = _UNESCAPED_PIPE.split(stripped)[1:-1]
    return tuple(cell.replace("\\|", "|").strip() for cell in cells)


def _is_delimiter_row(cells: tuple[str, ...]) -> bool:
    return bool(cells) and all(cell and set(cell) <= {"-", ":", " "} for cell in cells)


def _declared_header(
    cells: tuple[str, ...], number: int, line: str
) -> DeclaredTableHeader:
    header = _TABLE_HEADER_BY_COLUMNS.get(tuple(cells[:2]))
    if header is None:
        raise ConstitutionLedgerError(
            f"ترويسةُ جدولٍ خارج المفردة المغلقة عند السطر {number}: "
            f"{line.strip()!r} — {UNKNOWN_TABLE_HEADER_IS_REFUSED_NOTE}"
        )
    return header


def _read_tables(lines: list[str]) -> tuple[tuple[LawRow, ...], TableCensus]:
    """امسح جداول الوثيقة كلَّها: تُقرَأ أو تُستبعَد مُصرَّحًا بها أو تُرفَض."""

    rows: list[LawRow] = []
    tables: list[ReadTable] = []
    index = 0
    total = len(lines)
    while index < total:
        line = lines[index]
        if not line.startswith("|"):
            index += 1
            continue
        number = index + 1
        cells = _split_row(line)
        if len(cells) < 2:
            raise ConstitutionLedgerError(f"صفُّ جدولٍ ناقص الأعمدة عند السطر {number}")
        if index + 1 >= total or not _is_delimiter_row(_split_row(lines[index + 1])):
            raise ConstitutionLedgerError(
                f"جدولٌ بلا سطر فصلٍ بعد ترويسته عند السطر {number}: جدولٌ "
                "مقطوعٌ يُقرَأ صفُّه ترويسةً فيسقط من التعداد صامتًا"
            )
        header = _declared_header(cells, number, line)
        tables.append(
            ReadTable(
                declared_header=header,
                header_text=line.strip(),
                header_line=number,
            )
        )
        index += 2
        while index < total and lines[index].startswith("|"):
            body_number = index + 1
            body_cells = _split_row(lines[index])
            index += 1
            if not header.carries_law_rows:
                continue
            if len(body_cells) < 2:
                raise ConstitutionLedgerError(
                    f"صفُّ قانونٍ ناقص الأعمدة عند السطر {body_number}"
                )
            status = _STATUS_BY_TEXT.get(body_cells[1])
            if status is None:
                raise ConstitutionLedgerError(
                    f"حالةٌ خارج المفردة المغلقة عند السطر {body_number}: "
                    f"{body_cells[1]!r} — {UNKNOWN_STATUS_IS_REFUSED_NOTE}"
                )
            rows.append(
                LawRow(law=body_cells[0], status=status, document_line=body_number)
            )
    if not tables:
        raise ConstitutionLedgerError("لم يُقرَأ أيّ جدولٍ من الوثيقة")
    if not rows:
        raise ConstitutionLedgerError("لم يُقرَأ أيّ صفّ قانونٍ من الوثيقة")
    return tuple(rows), TableCensus(tables=tuple(tables))


def _section_bounds(lines: list[str], heading: str) -> tuple[int, int]:
    start = -1
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped == heading or stripped.startswith(f"{heading} "):
            start = index + 1
            break
    if start < 0:
        raise ConstitutionLedgerError(f"قسمٌ مفقود في الوثيقة: {heading}")
    for index in range(start, len(lines)):
        if lines[index].startswith("#"):
            return start, index
    return start, len(lines)


def _logical_bullets(lines: list[str], start: int, end: int) -> list[tuple[int, str]]:
    """اجمع كلّ نقطةٍ مع أسطر امتدادها في سطرٍ منطقيّ واحد، فلا يُبتَر نصّها."""

    bullets: list[tuple[int, str]] = []
    open_bullet = False
    for index in range(start, end):
        line = lines[index]
        stripped = line.strip()
        if stripped.startswith("- "):
            bullets.append((index + 1, line.rstrip()))
            open_bullet = True
            continue
        if open_bullet and stripped and line[:1].isspace():
            number, body = bullets[-1]
            bullets[-1] = (number, f"{body} {stripped}")
            continue
        open_bullet = False
    return bullets


def _bullet_value(body: str, label: DeclaredQuestionBulletLabel) -> str:
    value = body[len(label.value) + 1 :].strip()
    candidate = value[:-1].strip() if value.endswith(".") else value
    if (
        len(candidate) > 2
        and candidate.startswith("`")
        and candidate.endswith("`")
        and "`" not in candidate[1:-1]
    ):
        return candidate[1:-1]
    return value


def _declared_bullet_label(
    body: str, number: int, text: str
) -> DeclaredQuestionBulletLabel:
    for label in _LABELS_LONGEST_FIRST:
        if body.startswith(f"{label.value}:"):
            return label
    raise ConstitutionLedgerError(
        f"وسمُ نقطةٍ خارج المفردة المغلقة عند السطر {number}: "
        f"{text.strip()!r} — {UNKNOWN_QUESTION_BULLET_IS_REFUSED_NOTE}"
    )


def _declared_bullet_shape(
    text: str, number: int
) -> tuple[DeclaredQuestionBulletShape, str]:
    name_only = _TOP_LEVEL_NAME_ONLY.match(text)
    if name_only is not None:
        return DeclaredQuestionBulletShape.NAME_ONLY, name_only.group("name")
    with_note = _TOP_LEVEL_NAME_WITH_INLINE_NOTE.match(text)
    if with_note is not None:
        return (
            DeclaredQuestionBulletShape.NAME_WITH_INLINE_NOTE,
            with_note.group("name"),
        )
    raise ConstitutionLedgerError(
        f"نقطةٌ عليا خارج مفردة الأشكال عند السطر {number}: "
        f"{text.strip()!r} — {UNKNOWN_QUESTION_BULLET_IS_REFUSED_NOTE}"
    )


def _read_section_questions(
    lines: list[str], heading: str, standing: AuditQuestionStanding
) -> tuple[list[AuditQuestionRow], list[ReadQuestionBullet]]:
    start, end = _section_bounds(lines, heading)
    questions: list[AuditQuestionRow] = []
    bullets: list[ReadQuestionBullet] = []
    name = ""
    line_number = 0
    values: dict[DeclaredQuestionBulletLabel, str] = {}

    def flush() -> None:
        if not name:
            return
        questions.append(
            AuditQuestionRow(
                name=name,
                standing=standing,
                declared_status=(
                    values.get(DeclaredQuestionBulletLabel.STATUS)
                    or NO_STATUS_DECLARED_IN_RECORD
                ),
                document_line=line_number,
                previous_audit_label=values.get(
                    DeclaredQuestionBulletLabel.PREVIOUS_AUDIT_LABEL, ""
                ),
                closure_law=values.get(DeclaredQuestionBulletLabel.CLOSURE_LAW, ""),
            )
        )

    for number, text in _logical_bullets(lines, start, end):
        sub = _SUB_BULLET.match(text)
        if sub is None:
            shape, read_name = _declared_bullet_shape(text, number)
            flush()
            name = read_name
            line_number = number
            values = {}
            bullets.append(
                ReadQuestionBullet(
                    document_line=number,
                    standing=standing,
                    question_name=name,
                    shape=shape,
                )
            )
            continue
        if not name:
            raise ConstitutionLedgerError(
                f"نقطةٌ فرعية قبل أيّ سؤالٍ مُسمّى عند السطر {number}: "
                f"{text.strip()!r} — وسمٌ بلا صاحبٍ لا يُطوى ولا يُنسَب إلى "
                "سؤالٍ لاحق"
            )
        body = sub.group("body").strip()
        label = _declared_bullet_label(body, number, text)
        if label in values:
            raise ConstitutionLedgerError(
                f"وسمٌ مكرّر في السؤال {name} عند السطر {number}: {label.value} — "
                "لا يُرجَّح أوّلُ الموضعين على الآخر"
            )
        values[label] = _bullet_value(body, label)
        bullets.append(
            ReadQuestionBullet(
                document_line=number,
                standing=standing,
                question_name=name,
                label=label,
            )
        )
    flush()
    if not questions:
        raise ConstitutionLedgerError(f"لم يُقرَأ أيّ سؤالٍ من القسم: {heading}")
    return questions, bullets


def read_constitution_ledger(document_text: str) -> ConstitutionLedger:
    """اقرأ دفترَي الاشتقاق من نصّ الدستور، ورُدَّ ما خرج عن مفرداته المغلقة."""

    if not isinstance(document_text, str) or not document_text.strip():
        raise ConstitutionLedgerError("نصّ الوثيقة نصٌّ غير فارغ")
    lines = document_text.splitlines()
    open_questions, open_bullets = _read_section_questions(
        lines, _OPEN_SECTION_HEADING, AuditQuestionStanding.OPEN
    )
    resolved_questions, resolved_bullets = _read_section_questions(
        lines, _RESOLVED_SECTION_HEADING, AuditQuestionStanding.RESOLVED
    )
    questions = open_questions + resolved_questions
    bullets = sorted(
        open_bullets + resolved_bullets, key=lambda bullet: bullet.document_line
    )
    rows, census = _read_tables(lines)
    return ConstitutionLedger(
        laws=LawRowLedger(rows=rows),
        audit_questions=AuditQuestionLedger(questions=tuple(questions)),
        tables=census,
        question_bullets=QuestionBulletCensus(bullets=tuple(bullets)),
    )


def constitution_document_path() -> Path:
    """موضع وثيقة الدستور في شجرة المستودع، مشتقًّا من موضع هذه الوحدة."""

    return Path(__file__).resolve().parents[3] / CONSTITUTION_RELATIVE_PATH


def load_constitution_ledger(path: Path | None = None) -> ConstitutionLedger:
    """اقرأ الدفترين من الوثيقة نفسها؛ وغيابُها رفضٌ مُسمّى لا دفترٌ فارغ."""

    document = constitution_document_path() if path is None else path
    if not isinstance(document, Path):
        raise ConstitutionLedgerError("موضع الوثيقة مسارٌ")
    try:
        text = document.read_text(encoding="utf-8")
    except OSError as error:
        raise ConstitutionLedgerError(
            f"تعذّرت قراءة وثيقة الدستور عند {document}: دفترٌ فارغ يُقرَأ "
            "«لا صفوف» وهو ادّعاءٌ لم تُقرَأ الوثيقة لأجله"
        ) from error
    return read_constitution_ledger(text)


__all__ = [
    "CONSTITUTION_RELATIVE_PATH",
    "DESIGN_SOURCE_CITATION_NOTE",
    "LEDGER_AUTHORITY_NOTE",
    "NAMED_RESIDUALS",
    "NO_DECLARED_TOTAL_TO_CROSS_CHECK",
    "EXCLUDED_QUESTION_BULLET_MAY_CARRY_A_DECLARED_STATUS",
    "NO_INDICATOR_IN_THIS_READER_NOTE",
    "NO_STATUS_DECLARED_IN_RECORD",
    "QUESTION_BULLET_LABEL_VOCABULARY_IS_NOT_DECLARED_IN_RECORD",
    "TABLE_HEADER_MATCH_COMPLETENESS_UNVERIFIED",
    "UNKNOWN_QUESTION_BULLET_IS_REFUSED_NOTE",
    "UNKNOWN_STATUS_IS_REFUSED_NOTE",
    "UNKNOWN_TABLE_HEADER_IS_REFUSED_NOTE",
    "AuditQuestionLedger",
    "AuditQuestionRow",
    "AuditQuestionStanding",
    "ConstitutionLedger",
    "ConstitutionLedgerError",
    "DeclaredLawStatus",
    "DeclaredQuestionBulletLabel",
    "DeclaredQuestionBulletShape",
    "DeclaredTableHeader",
    "LawRow",
    "LawRowLedger",
    "QuestionBulletCensus",
    "ReadQuestionBullet",
    "ReadTable",
    "TableCensus",
    "constitution_document_path",
    "load_constitution_ledger",
    "read_constitution_ledger",
]
