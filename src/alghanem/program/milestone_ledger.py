"""مقابلةُ مراحل §٧ بوحداتها في الشجرة، مُشتَقّةً لا مقروءةً بالعين.

هذه **المرحلة السابعة من الطور الثاني** لـ AIM.1، وهي أداءُ الدَّين الذي سمّاه
الهبوط المزدوج للمرحلة السادسة في خاتمته حرفًا بحرف: «لا شيء في السجلّ يمنع
ترميزَ مرحلةٍ مرّتين، ولا دفترَ يشتقّ أن قسمًا في §٧ يقابله ترميزٌ واحد في
الشجرة»، وسمّاه `MILESTONE_SECTION_TO_MODULE_CORRESPONDENCE_IS_NOT_DERIVED`.
فما بقي هناك حاجزًا مُسمّى يقوم هنا موضوعًا لمرحلةٍ، لا طيًّا للحاجز::

    MilestoneSection != CodedModule
    ModuleExists     != MilestoneCodedIt
    DerivedMap       != Attainment
    AimsDocument     != Authority

**المصدر التصميميّ المباشر، مُستشهَدًا به لا مُعادًا اشتقاقه.** شكلُ «الوثيقة
تُعلن، والقارئ لا يقبل إلا من مفردةٍ مغلقة يملكها هو، والمخالفة تُرفَض عند
الإنشاء» مأخوذٌ من سؤال التدقيق المفتوح
`DeclaredVersusDerivedRecurrenceNotExplained` بوصفه **مصدرًا مباشرًا** (إلزام §٥
من `docs/AIMS.md`)، لا بوصفه بديهةً تُعاد هنا صامتةً. وذلك السؤال مرصودٌ غير
مفسَّر، فلا يُستحدَث له اسمٌ عامّ ولا صنفُ أساسٍ مشترك يوحّد الشكل بين القرّاء
الستّة؛ يُستعمل في موضعه ويُنسَب إلى سؤاله.

**الإعلان موضعان لا موضعٌ واحد، والمقابلة بينهما شرطُ قراءةٍ لا تزيّدٌ.** ترويسةُ
الوثيقة تُسمّي وحدةَ كلّ مرحلةٍ في جملةٍ واحدة، و§٧ تُسمّيها ثانيةً في قسم تلك
المرحلة؛ فهما إعلانان مستقلّان لخريطةٍ واحدة. واختلافُهما يُرفَض عند الإنشاء ولا
يُرجَّح أحدهما على الآخر، فترجيحُ أحدهما اختيارٌ من القارئ لا إعلانٌ من الوثيقة.

**الوجودُ في الشجرة مُشتَقٌّ، والتأليفُ ليس مُشتَقًّا.** أن الوحدة المُسمّاة
قائمةٌ في الشجرة يُقرأ من الشجرة نفسها؛ وأن **تلك المرحلة** هي التي رمّزتها لا
يُقرأ من شيءٍ هنا، وهو مُسمًّى في `NAMED_RESIDUALS` لا مطويّ.

**الرفض لا التخطّي الصامت، مرفوعًا إلى طبقة القسم.** ارتفعت القاعدة في
`constitution_ledger` من الخلية إلى الجدول، وفي `deferred_value_ledger` إلى
الحارس، وفي `aims_document_ledger` إلى النقطة، وفي `aim_indicator` إلى الإشارة؛
وترتفع هنا إلى **القسم**: كلّ عنوانٍ فرعيٍّ في §٧ إمّا قسمُ مرحلةٍ بشكلٍ من
المفردة، أو قسمُ واقعةٍ مُسجَّلة بشكلٍ منها، أو مرفوضٌ باسمه وموضع سطره. وقسمٌ
يسقط صامتًا يُنتج خريطةً ناقصةً تُقرَأ لاحقًا «هكذا صرّحت الوثيقة».

**وتكرارُ قسم المرحلة الواحدة يُرفَض عند الإنشاء**، وهو بعينه ما وقع في الهبوط
المزدوج فلم يمنعه شيء: قسمان باسم «المرحلة السادسة» في §٧ وفقرتان في `README.md`.
فما كُشف بالقراءة يُشتَقّ هنا بالبنية.

**التعداد خاصّيةٌ تُحسَب لا حقلٌ يُكتَب** (§٤): لا حقلَ عددٍ في أيّ صنفٍ هنا.

**لا مؤشرَ هنا**: المؤشر ربطُ عددٍ مُشتَقّ **بغايةٍ بعينها**، وهذا الدفتر يربط
مرحلةَ ترميزٍ بوحدةِ شيفرة؛ فلا يستورد `AimId` ولا أيًّا من الدفاتر الأربعة، ولا
يُحصي غايةً ولا مستندًا، ويُفحَص ذلك آليًّا.

**خمولٌ سلطويّ**: `MilestoneLedger != BirthVerdict`؛ لا تُصدر هذه الوحدة ولادةً
ولا حكمًا ولا تجميدًا ولا `E0`، ولا تُصدر بلوغَ غايةٍ ولا تُرقّيه، ولا تقرؤها أيّ
وحدةٍ في `kernel/`. وترتيبُ المراحل ترتيبُ إعلانها، لا ترتيبَ أولويةٍ ولا أهمّية
(§٦)، وتعاقبُ المراحل ليس تقدّمًا نحو بلوغ أيّ غاية.
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

AIMS_RELATIVE_PATH: Final = "docs/AIMS.md"

PROGRAMME_PACKAGE_RELATIVE_PATH: Final = "src/alghanem/program"

MILESTONE_LEDGER_AUTHORITY_NOTE: Final = (
    "قراءةٌ ومقابلةٌ فقط: لا يُنتج هذا الدفتر ولادةً ولا حكمًا ولا تجميدًا ولا "
    "`E0`، ولا يُصدر بلوغَ غايةٍ ولا يُرقّيه، ولا تقرؤه بوّابةٌ في النواة"
)

NO_INDICATOR_IN_THIS_LEDGER_NOTE: Final = (
    "لا مؤشر هنا: المؤشر ربطُ عددٍ مُشتَقّ بغايةٍ بعينها، وهذا الدفتر يربط "
    "مرحلةَ ترميزٍ بوحدةِ شيفرة؛ فلا يستورد `AimId` ولا أيًّا من الدفاتر "
    "الأربعة، ولا يُحصي غايةً ولا مستندًا، ويُفحَص ذلك آليًّا"
)

DESIGN_SOURCE_CITATION_NOTE: Final = (
    "شكلُ «الوثيقة تُعلن، والقارئ لا يقبل إلا من مفردةٍ مغلقة يملكها، "
    f"والمخالفة تُرفَض» مأخوذٌ من `{DESIGN_SOURCE_OPEN_QUESTION}` مصدرًا "
    "مباشرًا، لا بديهةً تُعاد هنا صامتةً"
)

UNKNOWN_SECTION_HEADING_IS_REFUSED_NOTE: Final = (
    "عنوانٌ فرعيّ في §٧ خارج المفردة المغلقة يُوقف القراءة ولا يُتخطّى: القسمُ "
    "الساقط يُنتج خريطةً ناقصةً تُقرَأ لاحقًا «هكذا صرّحت الوثيقة»"
)

DUPLICATE_MILESTONE_SECTION_IS_REFUSED_NOTE: Final = (
    "قسمان لمرحلةٍ واحدة يُرفَضان عند الإنشاء: هذا بعينه ما وقع في الهبوط "
    "المزدوج للمرحلة السادسة ولم يمنعه شيء، فما كُشف بالقراءة يُشتَقّ هنا "
    "بالبنية"
)

DECLARATIONS_DISAGREE_IS_REFUSED_NOTE: Final = (
    "الترويسة و§٧ إعلانان مستقلّان لخريطةٍ واحدة، واختلافُهما يُرفَض ولا "
    "يُرجَّح أحدهما: الترجيحُ اختيارٌ من القارئ لا إعلانٌ من الوثيقة"
)

UNCLAIMED_MODULE_IS_REFUSED_NOTE: Final = (
    "وحدةٌ في طبقة البرنامج لا تُطالِب بها مرحلةٌ في §٧ تُرفَض: الوحدة التي لا "
    "مرحلةَ لها شيفرةٌ هبطت بلا تسجيلٍ لما كشفه ترميزها، وهو ما تمنعه §٥"
)

MODULE_EXISTENCE_IS_NOT_MODULE_AUTHORSHIP: Final = (
    "MODULE_EXISTENCE_IS_NOT_MODULE_AUTHORSHIP"
)

BOTH_DECLARATIONS_ARE_PROSE_NOT_TREE_DERIVED: Final = (
    "BOTH_DECLARATIONS_ARE_PROSE_NOT_TREE_DERIVED"
)

FIRST_MILESTONE_NAMES_ITS_MODULE_IN_THE_PREAMBLE: Final = (
    "FIRST_MILESTONE_NAMES_ITS_MODULE_IN_THE_PREAMBLE"
)

REOPENING_IS_DERIVED_BUT_ITS_REASON_IS_NOT: Final = (
    "REOPENING_IS_DERIVED_BUT_ITS_REASON_IS_NOT"
)

INCIDENT_SECTIONS_CARRY_NO_MODULE_CLAIM: Final = (
    "INCIDENT_SECTIONS_CARRY_NO_MODULE_CLAIM"
)

NAMED_RESIDUALS: Final[Mapping[str, str]] = MappingProxyType(
    {
        MODULE_EXISTENCE_IS_NOT_MODULE_AUTHORSHIP: (
            "وجودُ الوحدة في الشجرة مُشتَقٌّ، وأن تلك المرحلة بعينها هي التي "
            "رمّزتها ليس مُشتَقًّا من شيءٍ هنا: لو نُسبت وحدةٌ قائمة إلى "
            "مرحلةٍ لم ترمّزها لاجتازت هذه المقابلة كاملةً. فالمُغلَق هو فجوةُ "
            "«قسمٌ بلا وحدة» و«وحدةٌ بلا قسم»، لا فجوةُ نسبةِ التأليف"
        ),
        BOTH_DECLARATIONS_ARE_PROSE_NOT_TREE_DERIVED: (
            "الإعلانان المُقابَلان هنا نثرٌ كلاهما: الترويسة و§٧. ومقابلتُهما "
            "تكشف اختلافَهما ولا تكشف اتّفاقهما على خطأ؛ فلو سُمّيت الوحدةُ "
            "نفسها الخطأ في الموضعين معًا لم يكشفه إلا وجودُها في الشجرة، "
            "وهو ما يُفحَص، أمّا مطابقةُ محتواها لما يصفه القسم فلا يُفحَص"
        ),
        FIRST_MILESTONE_NAMES_ITS_MODULE_IN_THE_PREAMBLE: (
            "قسمُ المرحلة الأولى لا يُسمّي وحدتَه في متنه، وإنما تُسمّيها "
            "ديباجةُ §٧ قبل الأقسام. فالقراءةُ تقبل ذلك بوسمٍ صريح "
            "`NAMED_IN_SECTION_PREAMBLE` لا بتخطٍّ صامت، والوسمُ يُبقي الشذوذ "
            "مرئيًّا بدل أن يُسوّى بغيره"
        ),
        REOPENING_IS_DERIVED_BUT_ITS_REASON_IS_NOT: (
            "أن مرحلةً لاحقة أعادت فتح وحدةِ مرحلةٍ سابقة مُشتَقٌّ هنا "
            "(`constitution_ledger.py` للثانية ثم للخامسة)، وأمّا لماذا "
            "أُعيد فتحُها فنثرٌ في §٧ لا يشتقّه هذا الدفتر. وإعادةُ الفتح "
            "ليست تكرارًا مرفوضًا ولا تقدّمًا: هي حالةٌ ثالثة مُسمّاة"
        ),
        INCIDENT_SECTIONS_CARRY_NO_MODULE_CLAIM: (
            "قسمُ الواقعة المُسجَّلة (الهبوط المزدوج) لا يُطالِب بوحدة، ويُحصى "
            "مع ذلك ليُرى: إسقاطُه من التعداد يجعل عددَ أقسام §٧ يخالف ما "
            "يُقرَأ فيها بلا سببٍ مُسمّى، وهو إخفاءُ قسمٍ خلف صمت"
        ),
    }
)

_SECTION_1_HEADING: Final = "## ١."
_SECTION_7_HEADING: Final = "## ٧."

_SUBSECTION: Final = re.compile(r"^### (?P<heading>.+?)\s*$")
_MODULE_TOKEN: Final = re.compile(r"`(?P<module>[A-Za-z0-9_][A-Za-z0-9_./-]*\.py)`")


class MilestoneLedgerError(ValueError):
    """قراءةٌ أو مقابلةٌ مرفوضة؛ لا تُحمَل الوثيقة على أقرب شكلٍ مقبول."""


class MilestoneOrdinal(Enum):
    """رتبُ المراحل كما تُسمّيها الوثيقة نصًّا، مفردةً مغلقة لا عدّادًا مفتوحًا.

    الرتبةُ اسمٌ مقروء لا رقمُ تقدّم: «السابعة» بعد «السادسة» في الإعلان، ولا
    يُقرَأ هذا قربًا من بلوغ أيّ غاية (§٦).
    """

    FIRST = "الأولى"
    SECOND = "الثانية"
    THIRD = "الثالثة"
    FOURTH = "الرابعة"
    FIFTH = "الخامسة"
    SIXTH = "السادسة"
    SEVENTH = "السابعة"
    EIGHTH = "الثامنة"
    NINTH = "التاسعة"

    @property
    def declaration_position(self) -> int:
        """موضعُ الرتبة في تعاقب الإعلان، مُشتَقًّا من ترتيب المفردة لا مكتوبًا."""

        return _ORDINAL_SEQUENCE.index(self)


class SeventhSectionKind(Enum):
    """جنسا القسم الفرعيّ في §٧ كما وردا نصًّا، ولا ثالثَ لهما يُفترَض."""

    MILESTONE_REVELATION = "ما كشفته المرحلة"
    RECORDED_INCIDENT = "ما كشفه الهبوط المزدوج للمرحلة"

    @property
    def claims_a_module(self) -> bool:
        """أيُطالِب هذا الجنسُ بوحدةٍ في الشجرة؟"""

        return self is SeventhSectionKind.MILESTONE_REVELATION


class DeclaredModuleShape(Enum):
    """شكلا تسمية الوحدة في النثر: مسارٌ تامّ أو اسمُ ملفٍّ مجرّد.

    لا يُدمَجان: المسارُ التامّ يُحَلّ من جذر المستودع، والاسمُ المجرّد لا يُحَلّ
    إلا داخل طبقة البرنامج؛ ودمجُهما يُخفي أن الوثيقة سمّت الوحدة الواحدة
    بشكلين، وهو فارقٌ كُتب فيها لا يُقدَّر هنا.
    """

    FULL_PATH = "مسارٌ تامّ"
    BARE_FILENAME = "اسمُ ملفٍّ مجرّد"


class ModuleNamingSite(Enum):
    """موضعُ تسمية الوحدة داخل §٧: متنُ القسم، أو ديباجةُ §٧ قبل الأقسام."""

    NAMED_IN_SECTION_BODY = "متنُ القسم"
    NAMED_IN_SECTION_PREAMBLE = "ديباجةُ §٧"


class ModuleClaimStanding(Enum):
    """رتبةُ مطالبةِ المرحلة بوحدتها، مُشتَقّةً من تعاقب المطالبات لا مكتوبة.

    `REOPENED_BY_THIS_MILESTONE` ليست تكرارًا مرفوضًا ولا درجةً في سُلَّم تقدّم:
    هي حالةٌ ثالثة مُسمّاة، ولولاها لوجب إمّا رفضُ المرحلة الخامسة وإمّا طيُّ
    أنها عادت إلى وحدة المرحلة الثانية.
    """

    FIRST_CODED_HERE = "أوّلُ مرحلةٍ تُطالِب بها"
    REOPENED_BY_THIS_MILESTONE = "إعادةُ فتحٍ لوحدةِ مرحلةٍ سابقة"


_ORDINAL_SEQUENCE: Final = tuple(MilestoneOrdinal)

_ORDINAL_BY_TEXT: Final[Mapping[str, MilestoneOrdinal]] = MappingProxyType(
    {member.value: member for member in MilestoneOrdinal}
)

_SECTION_KINDS_LONGEST_FIRST: Final = tuple(
    sorted(SeventhSectionKind, key=lambda kind: len(kind.value), reverse=True)
)

if len(_ORDINAL_BY_TEXT) != len(MilestoneOrdinal):  # pragma: no cover - guard
    raise RuntimeError("two ordinals must not share one declared text")
if len(SeventhSectionKind) != 2:  # pragma: no cover - guard
    raise RuntimeError("section seven declares exactly two subsection kinds")


def _require_non_blank(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise MilestoneLedgerError(f"{field_name} نصٌّ غير فارغ")
    return value


def _require_positive_line(value: int, field_name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise MilestoneLedgerError(f"{field_name} رقم سطرٍ موجب")
    return value


def _module_shape(token: str) -> DeclaredModuleShape:
    return (
        DeclaredModuleShape.FULL_PATH
        if "/" in token
        else DeclaredModuleShape.BARE_FILENAME
    )


def _resolved_relative_path(token: str) -> str:
    """حُلَّ الشكلَ المُعلَن إلى مسارٍ واحد من جذر المستودع، بلا ترجيحٍ ضمنيّ."""

    if _module_shape(token) is DeclaredModuleShape.FULL_PATH:
        return token
    return f"{PROGRAMME_PACKAGE_RELATIVE_PATH}/{token}"


@dataclass(frozen=True, slots=True)
class DeclaredModuleReference:
    """تسميةُ وحدةٍ واحدة كما وردت في النثر: نصُّها وشكلُها وموضعُها."""

    token: str
    shape: DeclaredModuleShape
    document_line: int

    def __post_init__(self) -> None:
        _require_non_blank(self.token, "اسم الوحدة")
        if not isinstance(self.shape, DeclaredModuleShape):
            raise MilestoneLedgerError("شكل التسمية من مفردته المغلقة")
        if self.shape is not _module_shape(self.token):
            raise MilestoneLedgerError(
                f"شكلٌ مُعلَنٌ يخالف نصَّه: {self.token!r} — الشكلُ مُشتَقٌّ من "
                "النصّ لا مكتوبٌ معه"
            )
        _require_positive_line(self.document_line, "موضع التسمية")

    @property
    def relative_path(self) -> str:
        """مسارُ الوحدة من جذر المستودع، مُشتَقًّا من شكل تسميتها."""

        return _resolved_relative_path(self.token)


@dataclass(frozen=True, slots=True)
class ReadSeventhSection:
    """قسمٌ فرعيّ واحد من §٧: جنسُه ورتبةُ مرحلته وعنوانُه وموضعُه."""

    kind: SeventhSectionKind
    ordinal: MilestoneOrdinal
    heading: str
    document_line: int
    module: DeclaredModuleReference | None = None
    naming_site: ModuleNamingSite | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.kind, SeventhSectionKind):
            raise MilestoneLedgerError("جنس القسم من مفردته المغلقة")
        if not isinstance(self.ordinal, MilestoneOrdinal):
            raise MilestoneLedgerError("رتبة المرحلة من مفردتها المغلقة")
        _require_non_blank(self.heading, "عنوان القسم")
        _require_positive_line(self.document_line, "موضع القسم")

        if self.kind.claims_a_module:
            if self.module is None or self.naming_site is None:
                raise MilestoneLedgerError(
                    f"قسمُ المرحلة {self.ordinal.value} بلا وحدةٍ مُسمّاة — "
                    "قسمٌ يصف ترميزًا بلا وحدةٍ يُقرَأ ترميزًا بلا أثر"
                )
        elif self.module is not None or self.naming_site is not None:
            raise MilestoneLedgerError(
                f"قسمُ واقعةٍ يُطالِب بوحدة عند السطر {self.document_line} — "
                f"{INCIDENT_SECTIONS_CARRY_NO_MODULE_CLAIM}"
            )

        if self.module is not None and not isinstance(
            self.module, DeclaredModuleReference
        ):
            raise MilestoneLedgerError("تسمية الوحدة من نوعها")
        if self.naming_site is not None and not isinstance(
            self.naming_site, ModuleNamingSite
        ):
            raise MilestoneLedgerError("موضع التسمية من مفردته المغلقة")


@dataclass(frozen=True, slots=True)
class HeaderMilestoneDeclaration:
    """تسميةُ الترويسة لوحدة مرحلةٍ واحدة، وهي الإعلان الأوّل من الإعلانين."""

    ordinal: MilestoneOrdinal
    module: DeclaredModuleReference

    def __post_init__(self) -> None:
        if not isinstance(self.ordinal, MilestoneOrdinal):
            raise MilestoneLedgerError("رتبة المرحلة من مفردتها المغلقة")
        if not isinstance(self.module, DeclaredModuleReference):
            raise MilestoneLedgerError("تسمية الوحدة من نوعها")


@dataclass(frozen=True, slots=True)
class SectionCensus:
    """إحصاءُ أقسام §٧ كلِّها بترتيب ورودها، فلا يسقط قسمٌ صامتًا.

    لا حقلَ عددٍ هنا؛ التعدادُ خاصّيةٌ تُحسَب من الأقسام المرصودة.
    """

    sections: tuple[ReadSeventhSection, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.sections, tuple) or not self.sections:
            raise MilestoneLedgerError("إحصاء الأقسام مجموعةٌ غير فارغة")
        previous_line = 0
        for section in self.sections:
            if not isinstance(section, ReadSeventhSection):
                raise MilestoneLedgerError("كل عنصرٍ قسمٌ مقروء")
            if section.document_line <= previous_line:
                raise MilestoneLedgerError("ترتيب الأقسام ترتيبُ ورودها في §٧")
            previous_line = section.document_line

    @property
    def section_count(self) -> int:
        """عدد أقسام §٧ المرصودة، محسوبًا لا مكتوبًا."""

        return len(self.sections)

    def sections_of_kind(
        self, kind: SeventhSectionKind
    ) -> tuple[ReadSeventhSection, ...]:
        """أقسامُ جنسٍ بعينه بترتيب ورودها في الوثيقة."""

        if not isinstance(kind, SeventhSectionKind):
            raise MilestoneLedgerError("جنس القسم من مفردته المغلقة")
        return tuple(section for section in self.sections if section.kind is kind)


@dataclass(frozen=True, slots=True)
class MilestoneRow:
    """صفُّ مرحلةٍ واحدة: رتبتُها، ووحدتُها المُقابَلة، ورتبةُ مطالبتها بها.

    لا حقلَ «مطابق/غير مطابق» هنا: قيامُ الصفّ **هو** المطابقة، وانحرافُها
    استثناءٌ مُسمّى عند الإنشاء (§٤: «المخالفة تُرفَض لا تُقرَّر»).
    """

    ordinal: MilestoneOrdinal
    relative_path: str
    header_shape: DeclaredModuleShape
    section_shape: DeclaredModuleShape
    naming_site: ModuleNamingSite
    claim_standing: ModuleClaimStanding
    section_line: int

    def __post_init__(self) -> None:
        if not isinstance(self.ordinal, MilestoneOrdinal):
            raise MilestoneLedgerError("رتبة المرحلة من مفردتها المغلقة")
        _require_non_blank(self.relative_path, "مسار الوحدة")
        for shape in (self.header_shape, self.section_shape):
            if not isinstance(shape, DeclaredModuleShape):
                raise MilestoneLedgerError("شكل التسمية من مفردته المغلقة")
        if not isinstance(self.naming_site, ModuleNamingSite):
            raise MilestoneLedgerError("موضع التسمية من مفردته المغلقة")
        if not isinstance(self.claim_standing, ModuleClaimStanding):
            raise MilestoneLedgerError("رتبة المطالبة من مفردتها المغلقة")
        _require_positive_line(self.section_line, "موضع القسم")

    @property
    def shapes_agree(self) -> bool:
        """أسمّى الإعلانان الوحدةَ بالشكل نفسه؟ اختلافُ الشكل لا يُرفَض."""

        return self.header_shape is self.section_shape


@dataclass(frozen=True, slots=True)
class MilestoneLedger:
    """خريطةُ مراحل §٧ بوحداتها، مُقابَلةً بالترويسة ومُشتَقَّةً بالشجرة."""

    rows: tuple[MilestoneRow, ...]
    census: SectionCensus

    def __post_init__(self) -> None:
        if not isinstance(self.rows, tuple) or not self.rows:
            raise MilestoneLedgerError("صفوف المراحل مجموعةٌ غير فارغة")
        if not isinstance(self.census, SectionCensus):
            raise MilestoneLedgerError("إحصاء الأقسام من نوعه")

        seen: set[MilestoneOrdinal] = set()
        previous_position = -1
        for row in self.rows:
            if not isinstance(row, MilestoneRow):
                raise MilestoneLedgerError("كل عنصرٍ صفُّ مرحلةٍ")
            if row.ordinal in seen:
                raise MilestoneLedgerError(
                    f"مرحلةٌ مكرّرة: {row.ordinal.value} — "
                    f"{DUPLICATE_MILESTONE_SECTION_IS_REFUSED_NOTE}"
                )
            seen.add(row.ordinal)
            if row.ordinal.declaration_position <= previous_position:
                raise MilestoneLedgerError(
                    "ترتيب الصفوف ترتيبُ تعاقب المراحل في الإعلان"
                )
            previous_position = row.ordinal.declaration_position

        expected = _ORDINAL_SEQUENCE[: len(self.rows)]
        if tuple(row.ordinal for row in self.rows) != expected:
            raise MilestoneLedgerError(
                "تعاقبُ المراحل منقطع: المراحل المقروءة "
                f"{[row.ordinal.value for row in self.rows]} والمتوقَّع "
                f"{[ordinal.value for ordinal in expected]} — مرحلةٌ غائبةٌ من "
                "الوسط تُقرَأ تعاقبًا متّصلًا وهي انقطاع"
            )

        claimed: dict[str, MilestoneOrdinal] = {}
        for row in self.rows:
            first = claimed.get(row.relative_path)
            if first is None:
                if row.claim_standing is not ModuleClaimStanding.FIRST_CODED_HERE:
                    raise MilestoneLedgerError(
                        f"{row.ordinal.value}: إعادةُ فتحٍ لوحدةٍ لم تُطالِب بها "
                        f"مرحلةٌ قبلها: {row.relative_path}"
                    )
                claimed[row.relative_path] = row.ordinal
                continue
            if row.claim_standing is not ModuleClaimStanding.REOPENED_BY_THIS_MILESTONE:
                raise MilestoneLedgerError(
                    f"{row.ordinal.value}: وحدةٌ طالبت بها {first.value} قبلها "
                    f"({row.relative_path}) ورتبةُ المطالبة ليست إعادةَ فتح — "
                    f"{REOPENING_IS_DERIVED_BUT_ITS_REASON_IS_NOT}"
                )

    @property
    def milestone_count(self) -> int:
        """عدد المراحل المقروءة، محسوبًا لا مكتوبًا."""

        return len(self.rows)

    @property
    def incident_count(self) -> int:
        """عدد أقسام الوقائع المُسجَّلة في §٧، محسوبًا لا مكتوبًا."""

        return len(self.census.sections_of_kind(SeventhSectionKind.RECORDED_INCIDENT))

    @property
    def claimed_modules(self) -> tuple[str, ...]:
        """الوحداتُ المُطالَبُ بها بترتيب أوّل مطالبةٍ بها، بلا تكرار."""

        return tuple(dict.fromkeys(row.relative_path for row in self.rows))

    @property
    def reopened_modules(self) -> Mapping[str, tuple[MilestoneOrdinal, ...]]:
        """الوحداتُ التي طالبت بها أكثرُ من مرحلة، بترتيب مطالباتها."""

        gathered: dict[str, list[MilestoneOrdinal]] = {}
        for row in self.rows:
            gathered.setdefault(row.relative_path, []).append(row.ordinal)
        return MappingProxyType(
            {
                path: tuple(ordinals)
                for path, ordinals in gathered.items()
                if len(ordinals) > 1
            }
        )

    @property
    def rows_by_ordinal(self) -> Mapping[MilestoneOrdinal, MilestoneRow]:
        """صفُّ كلّ مرحلةٍ بمفتاح رتبتها، بترتيب تعاقبها."""

        return MappingProxyType({row.ordinal: row for row in self.rows})

    def row(self, ordinal: MilestoneOrdinal) -> MilestoneRow:
        """صفُّ مرحلةٍ بعينها؛ وغيابُه رفضٌ مُسمّى لا `None` يُطوى."""

        if not isinstance(ordinal, MilestoneOrdinal):
            raise MilestoneLedgerError("رتبة المرحلة من مفردتها المغلقة")
        for row in self.rows:
            if row.ordinal is ordinal:
                return row
        raise MilestoneLedgerError(f"لا صفَّ للمرحلة: {ordinal.value}")


def _section_bounds(
    lines: list[str], heading: str, stop: str | None
) -> tuple[int, int]:
    start = -1
    for index, line in enumerate(lines):
        if line.startswith(heading):
            start = index + 1
            break
    if start < 0:
        raise MilestoneLedgerError(f"قسمٌ مفقود في وثيقة الغايات: {heading}")
    if stop is None:
        for index in range(start, len(lines)):
            if lines[index].startswith("## "):
                return start, index
        return start, len(lines)
    for index in range(start, len(lines)):
        if lines[index].startswith(stop):
            return start, index
    raise MilestoneLedgerError(f"قسمٌ بلا نهايةٍ مُعلَنة: {heading}")


def _first_module_reference(
    lines: list[str], start: int, end: int
) -> DeclaredModuleReference | None:
    for index in range(start, end):
        match = _MODULE_TOKEN.search(lines[index])
        if match is None:
            continue
        token = match.group("module")
        return DeclaredModuleReference(
            token=token, shape=_module_shape(token), document_line=index + 1
        )
    return None


def _read_header_declarations(
    lines: list[str], end: int
) -> tuple[HeaderMilestoneDeclaration, ...]:
    """اقرأ خريطة الترويسة: كلُّ رتبةٍ مذكورة تتلوها تسميةُ وحدتها قبل التالية.

    القراءةُ على النصّ الموصول لا على الأسطر: تسميةُ وحدةٍ قد تقع في السطر نفسه
    قبل الرتبة التالية، فبدءُ البحث من أوّل السطر يُعطي رتبةً وحدةَ رتبةٍ قبلها.
    """

    joined = "\n".join(lines[:end])
    positions: list[tuple[int, MilestoneOrdinal]] = []
    for text, ordinal in _ORDINAL_BY_TEXT.items():
        start = joined.find(text)
        if start < 0:
            continue
        if joined.find(text, start + 1) >= 0:
            raise MilestoneLedgerError(
                f"رتبةٌ مكرّرة في الترويسة: {ordinal.value} — "
                f"{DUPLICATE_MILESTONE_SECTION_IS_REFUSED_NOTE}"
            )
        positions.append((start + len(text), ordinal))
    positions.sort()

    declarations: list[HeaderMilestoneDeclaration] = []
    for order, (offset, ordinal) in enumerate(positions):
        stop = positions[order + 1][0] if order + 1 < len(positions) else len(joined)
        match = _MODULE_TOKEN.search(joined, offset, stop)
        if match is None:
            raise MilestoneLedgerError(
                f"الترويسة تذكر المرحلة {ordinal.value} بلا تسميةِ وحدةٍ — "
                "رتبةٌ بلا وحدةٍ تُقرَأ مرحلةً بلا أثرٍ في الشجرة"
            )
        token = match.group("module")
        declarations.append(
            HeaderMilestoneDeclaration(
                ordinal=ordinal,
                module=DeclaredModuleReference(
                    token=token,
                    shape=_module_shape(token),
                    document_line=joined.count("\n", 0, match.start()) + 1,
                ),
            )
        )

    if not declarations:
        raise MilestoneLedgerError("لم تُقرَأ أيّ مرحلةٍ من ترويسة الوثيقة")
    ordinals = tuple(declaration.ordinal for declaration in declarations)
    if ordinals != _ORDINAL_SEQUENCE[: len(ordinals)]:
        raise MilestoneLedgerError(
            "تعاقبُ المراحل في الترويسة منقطعٌ أو غيرُ مرتَّب: "
            f"{[ordinal.value for ordinal in ordinals]}"
        )
    return tuple(declarations)


def _classify_heading(
    heading: str, number: int
) -> tuple[SeventhSectionKind, MilestoneOrdinal]:
    """طابِق أطولَ جنسٍ مُصرَّح به ثم رتبتَه، ورُدَّ ما خرج باسمه وموضعه."""

    for kind in _SECTION_KINDS_LONGEST_FIRST:
        if not heading.startswith(f"{kind.value} "):
            continue
        rest = heading[len(kind.value) + 1 :].strip()
        for text, ordinal in _ORDINAL_BY_TEXT.items():
            if rest == text or rest.startswith(f"{text} ("):
                return kind, ordinal
        raise MilestoneLedgerError(
            f"رتبةُ مرحلةٍ خارج المفردة المغلقة عند السطر {number}: {rest[:60]!r}"
            f" — {UNKNOWN_SECTION_HEADING_IS_REFUSED_NOTE}"
        )
    raise MilestoneLedgerError(
        f"عنوانٌ فرعيّ خارج المفردة المغلقة عند السطر {number}: {heading[:60]!r}"
        f" — {UNKNOWN_SECTION_HEADING_IS_REFUSED_NOTE}"
    )


def _read_sections(lines: list[str], start: int, end: int) -> SectionCensus:
    boundaries: list[tuple[int, str]] = []
    for index in range(start, end):
        match = _SUBSECTION.match(lines[index])
        if match is not None:
            boundaries.append((index, match.group("heading").strip()))
    if not boundaries:
        raise MilestoneLedgerError("لم يُقرَأ أيّ قسمٍ فرعيّ من §٧")

    preamble_module = _first_module_reference(lines, start, boundaries[0][0])
    sections: list[ReadSeventhSection] = []
    for order, (index, heading) in enumerate(boundaries):
        number = index + 1
        kind, ordinal = _classify_heading(heading, number)
        stop = boundaries[order + 1][0] if order + 1 < len(boundaries) else end
        if not kind.claims_a_module:
            sections.append(
                ReadSeventhSection(
                    kind=kind, ordinal=ordinal, heading=heading, document_line=number
                )
            )
            continue
        module = _first_module_reference(lines, index + 1, stop)
        site = ModuleNamingSite.NAMED_IN_SECTION_BODY
        if module is None:
            module = preamble_module
            site = ModuleNamingSite.NAMED_IN_SECTION_PREAMBLE
        if module is None:
            raise MilestoneLedgerError(
                f"قسمُ المرحلة {ordinal.value} عند السطر {number} بلا تسميةِ "
                "وحدةٍ في متنه ولا في ديباجة §٧"
            )
        sections.append(
            ReadSeventhSection(
                kind=kind,
                ordinal=ordinal,
                heading=heading,
                document_line=number,
                module=module,
                naming_site=site,
            )
        )
    return SectionCensus(sections=tuple(sections))


def _correspond(
    declarations: tuple[HeaderMilestoneDeclaration, ...], census: SectionCensus
) -> tuple[MilestoneRow, ...]:
    by_ordinal: dict[MilestoneOrdinal, ReadSeventhSection] = {}
    for section in census.sections_of_kind(SeventhSectionKind.MILESTONE_REVELATION):
        if section.ordinal in by_ordinal:
            raise MilestoneLedgerError(
                f"قسمان للمرحلة {section.ordinal.value} في §٧ — "
                f"{DUPLICATE_MILESTONE_SECTION_IS_REFUSED_NOTE}"
            )
        by_ordinal[section.ordinal] = section

    for section in census.sections_of_kind(SeventhSectionKind.RECORDED_INCIDENT):
        if section.ordinal not in by_ordinal:
            raise MilestoneLedgerError(
                f"واقعةٌ مُسجَّلة لمرحلةٍ بلا قسمٍ في §٧: {section.ordinal.value}"
            )

    declared = {declaration.ordinal for declaration in declarations}
    missing_section = sorted(
        ordinal.value for ordinal in declared if ordinal not in by_ordinal
    )
    if missing_section:
        raise MilestoneLedgerError(
            f"الترويسة تُسمّي مراحلَ بلا قسمٍ في §٧: {missing_section} — "
            f"{DECLARATIONS_DISAGREE_IS_REFUSED_NOTE}"
        )
    missing_header = sorted(
        ordinal.value for ordinal in by_ordinal if ordinal not in declared
    )
    if missing_header:
        raise MilestoneLedgerError(
            f"§٧ تحمل أقسامَ مراحلَ لا تُسمّيها الترويسة: {missing_header} — "
            f"{DECLARATIONS_DISAGREE_IS_REFUSED_NOTE}"
        )

    rows: list[MilestoneRow] = []
    claimed: set[str] = set()
    for declaration in declarations:
        section = by_ordinal[declaration.ordinal]
        assert section.module is not None and section.naming_site is not None
        header_path = declaration.module.relative_path
        section_path = section.module.relative_path
        if header_path != section_path:
            raise MilestoneLedgerError(
                f"{declaration.ordinal.value}: الترويسة تُسمّي {header_path} "
                f"و§٧ تُسمّي {section_path} — "
                f"{DECLARATIONS_DISAGREE_IS_REFUSED_NOTE}"
            )
        standing = (
            ModuleClaimStanding.REOPENED_BY_THIS_MILESTONE
            if header_path in claimed
            else ModuleClaimStanding.FIRST_CODED_HERE
        )
        claimed.add(header_path)
        rows.append(
            MilestoneRow(
                ordinal=declaration.ordinal,
                relative_path=header_path,
                header_shape=declaration.module.shape,
                section_shape=section.module.shape,
                naming_site=section.naming_site,
                claim_standing=standing,
                section_line=section.document_line,
            )
        )
    return tuple(rows)


def read_milestone_ledger(document_text: str) -> MilestoneLedger:
    """اقرأ ترويسة الوثيقة و§٧، وقابِل إعلانيهما؛ والمخالفةُ تُرفَض لا تُقرَّر."""

    if not isinstance(document_text, str) or not document_text.strip():
        raise MilestoneLedgerError("نصّ الوثيقة نصٌّ غير فارغ")
    lines = document_text.splitlines()
    _header_start, header_end = 0, _section_bounds(lines, "# ", _SECTION_1_HEADING)[1]
    declarations = _read_header_declarations(lines, header_end)
    section_start, section_end = _section_bounds(lines, _SECTION_7_HEADING, None)
    census = _read_sections(lines, section_start, section_end)
    return MilestoneLedger(rows=_correspond(declarations, census), census=census)


def repository_root_path() -> Path:
    """جذرُ المستودع، مشتقًّا من موضع هذه الوحدة لا مكتوبًا."""

    return Path(__file__).resolve().parents[3]


def aims_document_path() -> Path:
    """موضع وثيقة الغايات في شجرة المستودع."""

    return repository_root_path() / AIMS_RELATIVE_PATH


def programme_module_paths(root: Path | None = None) -> tuple[str, ...]:
    """وحداتُ طبقة البرنامج القائمة في الشجرة، بترتيب أسمائها، بلا `__init__`."""

    base = repository_root_path() if root is None else root
    if not isinstance(base, Path):
        raise MilestoneLedgerError("جذر المستودع مسارٌ")
    package = base / PROGRAMME_PACKAGE_RELATIVE_PATH
    if not package.is_dir():
        raise MilestoneLedgerError(
            f"طبقة البرنامج غير موجودة عند {package}: شجرةٌ فارغة تُقرَأ "
            "«لا وحدات» وهو ادّعاءٌ لم تُقرَأ الشجرة لأجله"
        )
    return tuple(
        sorted(
            f"{PROGRAMME_PACKAGE_RELATIVE_PATH}/{item.name}"
            for item in package.iterdir()
            if item.is_file() and item.suffix == ".py" and item.name != "__init__.py"
        )
    )


def correspond_milestones_to_tree(
    path: Path | None = None, root: Path | None = None
) -> MilestoneLedger:
    """قابِل خريطةَ §٧ بشجرة المستودع؛ وقيامُ الدفتر هو المقابلة نفسها."""

    document = aims_document_path() if path is None else path
    if not isinstance(document, Path):
        raise MilestoneLedgerError("موضع الوثيقة مسارٌ")
    try:
        text = document.read_text(encoding="utf-8")
    except OSError as error:
        raise MilestoneLedgerError(
            f"تعذّرت قراءة وثيقة الغايات عند {document}: دفترٌ فارغ يُقرَأ "
            "«لا مراحل» وهو ادّعاءٌ لم تُقرَأ الوثيقة لأجله"
        ) from error

    ledger = read_milestone_ledger(text)
    base = repository_root_path() if root is None else root
    for claimed in ledger.claimed_modules:
        if not (base / claimed).is_file():
            raise MilestoneLedgerError(
                f"وحدةٌ مُسمّاةٌ في §٧ لا وجود لها في الشجرة: {claimed} — "
                f"{MODULE_EXISTENCE_IS_NOT_MODULE_AUTHORSHIP}"
            )
    present = set(programme_module_paths(base))
    unclaimed = sorted(present - set(ledger.claimed_modules))
    if unclaimed:
        raise MilestoneLedgerError(
            f"وحداتٌ في طبقة البرنامج لا تُطالِب بها مرحلة: {unclaimed} — "
            f"{UNCLAIMED_MODULE_IS_REFUSED_NOTE}"
        )
    return ledger


__all__ = [
    "AIMS_RELATIVE_PATH",
    "BOTH_DECLARATIONS_ARE_PROSE_NOT_TREE_DERIVED",
    "DECLARATIONS_DISAGREE_IS_REFUSED_NOTE",
    "DESIGN_SOURCE_CITATION_NOTE",
    "DUPLICATE_MILESTONE_SECTION_IS_REFUSED_NOTE",
    "FIRST_MILESTONE_NAMES_ITS_MODULE_IN_THE_PREAMBLE",
    "INCIDENT_SECTIONS_CARRY_NO_MODULE_CLAIM",
    "MILESTONE_LEDGER_AUTHORITY_NOTE",
    "MODULE_EXISTENCE_IS_NOT_MODULE_AUTHORSHIP",
    "NAMED_RESIDUALS",
    "NO_INDICATOR_IN_THIS_LEDGER_NOTE",
    "PROGRAMME_PACKAGE_RELATIVE_PATH",
    "REOPENING_IS_DERIVED_BUT_ITS_REASON_IS_NOT",
    "UNCLAIMED_MODULE_IS_REFUSED_NOTE",
    "UNKNOWN_SECTION_HEADING_IS_REFUSED_NOTE",
    "DeclaredModuleReference",
    "DeclaredModuleShape",
    "HeaderMilestoneDeclaration",
    "MilestoneLedger",
    "MilestoneLedgerError",
    "MilestoneOrdinal",
    "MilestoneRow",
    "ModuleClaimStanding",
    "ModuleNamingSite",
    "ReadSeventhSection",
    "SectionCensus",
    "SeventhSectionKind",
    "aims_document_path",
    "correspond_milestones_to_tree",
    "programme_module_paths",
    "read_milestone_ledger",
    "repository_root_path",
]
