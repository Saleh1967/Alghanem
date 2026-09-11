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

_LAW_TABLE_HEADER: Final = ("Law", "Status")
_OPEN_SECTION_HEADING: Final = "### OpenAuditQuestions"
_RESOLVED_SECTION_HEADING: Final = "### ResolvedAuditQuestions"

_UNESCAPED_PIPE: Final = re.compile(r"(?<!\\)\|")
_TOP_LEVEL_BULLET: Final = re.compile(r"^- `(?P<name>[^`]+)`")
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
    ENFORCED_AT_ACQUISITION_AUTHORITY = "ENFORCED_AT_ACQUISITION_AUTHORITY"
    ENFORCED_AT_PROBE_PREREGISTRATION = "ENFORCED_AT_PROBE_PREREGISTRATION"
    ENFORCED_AT_CANONICAL_PRIMITIVE = "ENFORCED_AT_CANONICAL_PRIMITIVE"
    ENFORCED_AT_READINESS_RECORD = "ENFORCED_AT_READINESS_RECORD"
    ENFORCED_AT_IMPORT_CONTRACT = "ENFORCED_AT_IMPORT_CONTRACT"
    ENFORCED_AT_INTERVENTION_FOOTPRINT = "ENFORCED_AT_INTERVENTION_FOOTPRINT"
    ENFORCED_AT_AIM_RECORD = "ENFORCED_AT_AIM_RECORD"
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


_STATUS_BY_TEXT: Final[Mapping[str, DeclaredLawStatus]] = MappingProxyType(
    {member.value: member for member in DeclaredLawStatus}
)

if len(_STATUS_BY_TEXT) != len(DeclaredLawStatus):  # pragma: no cover - guard
    raise RuntimeError("two law statuses must not share one declared text")
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

    def __post_init__(self) -> None:
        if not isinstance(self.laws, LawRowLedger):
            raise ConstitutionLedgerError("دفتر الصفوف من نوعه")
        if not isinstance(self.audit_questions, AuditQuestionLedger):
            raise ConstitutionLedgerError("دفتر الأسئلة من نوعه")


def _split_row(line: str) -> tuple[str, ...]:
    stripped = line.strip()
    cells = _UNESCAPED_PIPE.split(stripped)[1:-1]
    return tuple(cell.replace("\\|", "|").strip() for cell in cells)


def _is_delimiter_row(cells: tuple[str, ...]) -> bool:
    return all(cell and set(cell) <= {"-", ":", " "} for cell in cells)


def _read_law_rows(lines: list[str]) -> tuple[LawRow, ...]:
    rows: list[LawRow] = []
    header: tuple[str, ...] | None = None
    for number, line in enumerate(lines, start=1):
        if not line.startswith("|"):
            header = None
            continue
        cells = _split_row(line)
        if header is None:
            header = cells
            continue
        if _is_delimiter_row(cells):
            continue
        if tuple(header[:2]) != _LAW_TABLE_HEADER:
            continue
        if len(cells) < 2:
            raise ConstitutionLedgerError(f"صفُّ قانونٍ ناقص الأعمدة عند السطر {number}")
        status = _STATUS_BY_TEXT.get(cells[1])
        if status is None:
            raise ConstitutionLedgerError(
                f"حالةٌ خارج المفردة المغلقة عند السطر {number}: {cells[1]!r} — "
                f"{UNKNOWN_STATUS_IS_REFUSED_NOTE}"
            )
        rows.append(LawRow(law=cells[0], status=status, document_line=number))
    if not rows:
        raise ConstitutionLedgerError("لم يُقرَأ أيّ صفّ قانونٍ من الوثيقة")
    return tuple(rows)


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


def _labelled_value(body: str, label: str) -> str:
    prefix = f"{label}:"
    if not body.startswith(prefix):
        return ""
    value = body[len(prefix) :].strip()
    candidate = value[:-1].strip() if value.endswith(".") else value
    if (
        len(candidate) > 2
        and candidate.startswith("`")
        and candidate.endswith("`")
        and "`" not in candidate[1:-1]
    ):
        return candidate[1:-1]
    return value


def _read_section_questions(
    lines: list[str], heading: str, standing: AuditQuestionStanding
) -> list[AuditQuestionRow]:
    start, end = _section_bounds(lines, heading)
    questions: list[AuditQuestionRow] = []
    name = ""
    line_number = 0
    declared_status = ""
    previous_label = ""
    closure_law = ""

    def flush() -> None:
        if not name:
            return
        questions.append(
            AuditQuestionRow(
                name=name,
                standing=standing,
                declared_status=declared_status or NO_STATUS_DECLARED_IN_RECORD,
                document_line=line_number,
                previous_audit_label=previous_label,
                closure_law=closure_law,
            )
        )

    for number, text in _logical_bullets(lines, start, end):
        top = _TOP_LEVEL_BULLET.match(text)
        if top is not None:
            flush()
            name = top.group("name")
            line_number = number
            declared_status = ""
            previous_label = ""
            closure_law = ""
            continue
        if not name:
            continue
        sub = _SUB_BULLET.match(text)
        if sub is None:
            continue
        body = sub.group("body").strip()
        declared_status = declared_status or _labelled_value(body, "Status")
        previous_label = previous_label or _labelled_value(body, "Previous audit label")
        closure_law = closure_law or _labelled_value(body, "Closure law")
    flush()
    if not questions:
        raise ConstitutionLedgerError(f"لم يُقرَأ أيّ سؤالٍ من القسم: {heading}")
    return questions


def read_constitution_ledger(document_text: str) -> ConstitutionLedger:
    """اقرأ دفترَي الاشتقاق من نصّ الدستور، ورُدَّ ما خرج عن مفرداته المغلقة."""

    if not isinstance(document_text, str) or not document_text.strip():
        raise ConstitutionLedgerError("نصّ الوثيقة نصٌّ غير فارغ")
    lines = document_text.splitlines()
    questions = _read_section_questions(
        lines, _OPEN_SECTION_HEADING, AuditQuestionStanding.OPEN
    )
    questions.extend(
        _read_section_questions(
            lines, _RESOLVED_SECTION_HEADING, AuditQuestionStanding.RESOLVED
        )
    )
    return ConstitutionLedger(
        laws=LawRowLedger(rows=_read_law_rows(lines)),
        audit_questions=AuditQuestionLedger(questions=tuple(questions)),
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
    "NO_INDICATOR_IN_THIS_READER_NOTE",
    "NO_STATUS_DECLARED_IN_RECORD",
    "UNKNOWN_STATUS_IS_REFUSED_NOTE",
    "AuditQuestionLedger",
    "AuditQuestionRow",
    "AuditQuestionStanding",
    "ConstitutionLedger",
    "ConstitutionLedgerError",
    "DeclaredLawStatus",
    "LawRow",
    "LawRowLedger",
    "constitution_document_path",
    "load_constitution_ledger",
    "read_constitution_ledger",
]
