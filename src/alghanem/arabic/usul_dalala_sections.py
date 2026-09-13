"""الأقسامُ الخمسةُ الحاكمةُ لمباحث الدلالة، وسقفُها التصنيفيّ قبل أيّ محتوى.

تُبنى هذه الوحدة **قبل** الوحدتين التاليتين لها في هذه الحلقة، لا بعدهما: فهي
المعيارُ الذي يُقاس به البندُ الدلاليُّ الجديد، وبناؤها بعدهما يجعلها وصفًا لما
حدث لا سقفًا يحكمه. والفارقُ عمليٌّ لا بلاغيّ: سقفٌ يُكتَب بعد المحتوى يُفصَّل
مقاسُه عليه، فلا يردُّ شيئًا أبدًا.

**والأقسامُ خمسةٌ لا سادس لها** (`FiveSectionsAreClosed`): الأوامرُ والنواهي،
والعمومُ والخصوص، والمطلقُ والمقيَّد، والمجملُ والبيانُ والمبيَّن، والناسخُ
والمنسوخ. وكلُّ بندٍ دلاليٍّ يُقترَح بعد اليوم يُردُّ إلى واحدٍ منها **بالاسم**،
أو يُرفَض ويُسمّى وجهُ ردِّه: رجوعًا إلى اللغة، أو تمحُّلًا لا يزيد على تكرارِ
قسمٍ قائمٍ بلفظٍ آخر.

**وسابقةُ الردِّ مُسجَّلةٌ لا مرويّة**: «الظاهر والمؤوَّل» عُرِض قسمًا سادسًا
فرُدَّ، وهو مُسجَّلٌ هنا بعينه في `REJECTED_PROPOSALS` مع وجه ردِّه؛ لأنّ سابقةً
تُذكَر في تقريرٍ ثم تُنسى لا تردُّ ثانيةً، وسابقةً في الشجرة تردُّ كلَّ مرّة.

**وخريطةُ التغطية مُشتَقّةٌ من الشجرة لا مكتوبةً في تقرير** (`read_sections`):
حالُ كلِّ قسمٍ (`مُرمَّز` / `غير_مُرمَّز`) تُقرأ من وجود وحداته في
`src/alghanem/arabic` على منوال `read_stations` و`read_chain`، فلا يبقى في
المستودع جدولُ تغطيةٍ يصدق يومَ كُتِب ويكذب بعده بأسبوع.

**ومفردةُ هذه الوحدة مطلوبةٌ لا مُثبَتة** (`RequestedSectionsAreNotAttested`، على
نصّ `COMPOUND_REQUESTED_NOT_ATTESTED_NOTE`): الأقسامُ الخمسةُ منقولةٌ في **طلبٍ**
يُحيل إلى الشخصية الإسلامية ج٣، ولم يُنقَل نصُّ الحصر بحروفه في هذا المستودع.
فكونُها مطلوبةً لا يُثبت أنها مفردةُ المصدر بلفظه، ولذلك هذه الوحدة **تسجيل**
لا شهادة، وبقيّتُها مُسمّاةٌ في `SECTION_CLOSURE_WORDING_NOT_TRANSCRIBED`.

**والناسخُ والمنسوخ بقيّةٌ بحثيةٌ مُسمّاة** (`NASKH_TEXT_NOT_EXTRACTED_RESIDUAL`)
ولا وحدةَ له اليوم: لم يُستخرَج له نصٌّ واحد، وبناءُ مفردةٍ له الآن كتابةُ مفردةٍ
قبل مصدرها ثمّ تفصيلُ مقاسها عليه حين يجيء — وهو بعينه ما يمنعه
`MarkerVocabularyIsFrozenBeforeItsText`. فالقسمُ مذكورٌ في المفردة لا محذوفٌ
منها، وحالُه تُقرأ `غير_مُرمَّز` من الشجرة نفسها.

**وهذه الوحدة تسجيلٌ لا سلطة**: لا ولادة، ولا حكمَ ولادة، ولا تجميد، ولا `E0`،
ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from pathlib import Path
from types import MappingProxyType
from typing import Final

from .pipeline_stations import ARABIC_PACKAGE_RELATIVE_PATH, repository_root_path

__all__ = [
    "COVERAGE_IS_READ_FROM_THE_TREE_NOTE",
    "FIVE_SECTIONS_ARE_CLOSED_NOTE",
    "NASKH_TEXT_NOT_EXTRACTED_RESIDUAL",
    "REJECTED_PROPOSALS",
    "REQUESTED_SECTIONS_ARE_NOT_ATTESTED_NOTE",
    "SECTION_CLOSURE_WORDING_NOT_TRANSCRIBED",
    "SECTION_MODULES",
    "USUL_DALALA_IS_NOT_A_GATE_NOTE",
    "AttributionOutcome",
    "DalalaSection",
    "ProposalRejection",
    "RejectionGround",
    "SectionCoding",
    "SectionCoverageLedger",
    "SectionReading",
    "UsulDalalaSectionsError",
    "attribute_proposal",
    "modules_of_section",
    "read_sections",
]


class UsulDalalaSectionsError(ValueError):
    """رفضٌ صريحٌ في إسناد بندٍ إلى قسمه؛ لا يُحمَل على أقرب قسمٍ مقبول."""


class DalalaSection(Enum):
    """الأقسامُ الخمسةُ الحاكمة؛ مفردةٌ مغلقةٌ لا سادس لها."""

    الأوامر_والنواهي = "الأوامر_والنواهي"
    العموم_والخصوص = "العموم_والخصوص"
    المطلق_والمقيد = "المطلق_والمقيد"
    المجمل_والبيان_والمبين = "المجمل_والبيان_والمبين"
    الناسخ_والمنسوخ = "الناسخ_والمنسوخ"


class RejectionGround(Enum):
    """وجهُ ردِّ المقترَح؛ ثلاثةٌ مغلقة، ولا يُردّ بندٌ بلا وجهٍ مُسمّى.

    و`راجع_إلى_قسم_قائم` غيرُ `تمحل_لا_يزيد_شيئا`: الأولُ مقبولُ المضمون
    مرفوضُ الاستقلال فيُدرَج في قسمه، والثاني مرفوضٌ أصلًا. وجمعُهما في وجهٍ
    واحد يُسقط الفارقَ بين بندٍ صحيحٍ في غير موضعه وبندٍ لا موضعَ له.
    """

    راجع_إلى_قسم_قائم = "راجع_إلى_قسم_قائم"
    راجع_إلى_اللغة = "راجع_إلى_اللغة"
    تمحل_لا_يزيد_شيئا = "تمحل_لا_يزيد_شيئا"


class AttributionOutcome(Enum):
    """نتيجةُ عرضِ بندٍ على السقف؛ ثنائيةٌ مغلقةٌ لا ثالثَ بينهما."""

    مسند_إلى_قسم = "مسند_إلى_قسم"
    مردود = "مردود"


class SectionCoding(Enum):
    """حالُ ترميز القسم، مقروءةً من الشجرة لا مُعلَنةً في حقل."""

    مُرمَّز = "مُرمَّز"
    غير_مُرمَّز = "غير_مُرمَّز"


FIVE_SECTIONS_ARE_CLOSED_NOTE: Final[str] = (
    "FiveSectionsAreClosed: مباحثُ الدلالة تندرج في خمسةٍ لا سادس لها، فكلُّ "
    "بندٍ يُقترَح يُردُّ إلى واحدٍ منها بالاسم أو يُرفَض بوجهٍ مُسمّى؛ ولا "
    "يُقبَل بندٌ «مستقلٌّ» بلا قسمٍ يرجع إليه، لأنّ قبولَه فتحُ سادسٍ في مفردةٍ "
    "مغلقة من غير أن يُسمّى ذلك فتحًا"
)

REQUESTED_SECTIONS_ARE_NOT_ATTESTED_NOTE: Final[str] = (
    "RequestedSectionsAreNotAttested: هذه الأقسامُ منقولةٌ في طلبٍ يُحيل إلى "
    "الشخصية الإسلامية ج٣، لا في نصٍّ مُثبَتٍ بحروفه في هذا المستودع؛ فكونُها "
    "مطلوبةً لا يُثبت أنها مفردةُ المصدر بلفظه ولا أنها مكتملةُ الفروع، "
    "والمُخرَجُ «تسجيل» لا «شهادة»"
)

SECTION_CLOSURE_WORDING_NOT_TRANSCRIBED: Final[str] = (
    "SECTION_CLOSURE_WORDING_NOT_TRANSCRIBED: جملةُ الحصر نفسها — التي تقول "
    "إنّ الأقسام خمسةٌ وتُسمّيها — لم تُنقَل بحروفها كما نُقلت جملةُ الحصر "
    "السباعية في `lafz_madlul_relation_formal`؛ فانغلاقُ الخمسة هنا مكتوبٌ في "
    "المفردة لا مربوطٌ بنصٍّ مفحوصٍ عند الاستيراد، وهذا فارقٌ في قوّة السند "
    "يُسجَّل ولا يُطوى"
)

NASKH_TEXT_NOT_EXTRACTED_RESIDUAL: Final[str] = (
    "NASKH_TEXT_NOT_EXTRACTED: الناسخُ والمنسوخ قسمٌ من الخمسة لم يُستخرَج له "
    "نصٌّ واحدٌ بعد، فلا وحدةَ له اليوم؛ وبناءُ مفردةٍ له قبل نصّها يجعل النصَّ "
    "حين يجيء يُفصَّل على مفردةٍ سبقته بدل أن تُشتَقّ منه، وهو ما يمنعه "
    "`MarkerVocabularyIsFrozenBeforeItsText`. فالقسمُ مذكورٌ في المفردة لا "
    "محذوفٌ منها، وحالُه تُقرأ من الشجرة `غير_مُرمَّز`"
)

COVERAGE_IS_READ_FROM_THE_TREE_NOTE: Final[str] = (
    "خريطةُ التغطية مُشتَقّةٌ من وجود الوحدات في الشجرة لا مكتوبةً في جدول: "
    "فجدولُ تغطيةٍ مكتوبٌ يصدق يومَ كُتِب ويكذب بعده، وقراءةُ الشجرة تُخطئ معها "
    "أو تصدق معها ولا تنفصل عنها"
)

USUL_DALALA_IS_NOT_A_GATE_NOTE: Final[str] = (
    "تسجيلٌ لا سلطة: لا تُصدر هذه الوحدة ولادةً ولا حكمَ ولادة ولا تجميدًا ولا "
    "`E0`، ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه"
)


_SECTION_MODULES: Final[dict[DalalaSection, tuple[str, ...]]] = {
    DalalaSection.الأوامر_والنواهي: ("mantuq_mafhum_ifada.py",),
    DalalaSection.العموم_والخصوص: ("umum_khusus.py",),
    DalalaSection.المطلق_والمقيد: ("mutlaq_muqayyad.py",),
    DalalaSection.المجمل_والبيان_والمبين: (
        "manat_verification.py",
        "comprehension_defect.py",
    ),
    DalalaSection.الناسخ_والمنسوخ: (),
}

SECTION_MODULES: Final[MappingProxyType[DalalaSection, tuple[str, ...]]] = (
    MappingProxyType(_SECTION_MODULES)
)

_FORBIDDEN_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "count",
    "total",
    "score",
    "rank",
    "percent",
    "ratio",
    "progress",
    "verdict",
    "birth",
    "freeze",
    "certificate",
)


def _require_non_blank(value: str, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise UsulDalalaSectionsError(f"{label} نصٌّ غير فارغ.")
    return value


@dataclass(frozen=True, slots=True)
class ProposalRejection:
    """بندٌ عُرِض على السقف فرُدَّ: اسمُه، ووجهُ ردِّه، وبيانُه.

    و`returns_to` يلزم متى كان الوجهُ `راجع_إلى_قسم_قائم` فلا يُقال «راجعٌ» بلا
    مرجعٍ يُسمّى، ويبقى `None` في الوجهين الآخرين فلا يُفتعَل له قسمٌ لم يرجع
    إليه.
    """

    proposal: str
    ground: RejectionGround
    statement: str
    returns_to: DalalaSection | None = None

    def __post_init__(self) -> None:
        _require_non_blank(self.proposal, "اسمُ البند المقترَح")
        _require_non_blank(self.statement, "بيانُ الردّ")
        if not isinstance(self.ground, RejectionGround):
            raise UsulDalalaSectionsError("وجهُ الردّ من مفردته المغلقة الثلاثية.")
        if self.ground is RejectionGround.راجع_إلى_قسم_قائم:
            if not isinstance(self.returns_to, DalalaSection):
                raise UsulDalalaSectionsError(
                    "«راجعٌ إلى قسمٍ قائم» يلزمه تسميةُ القسم؛ ورجوعٌ بلا مرجعٍ "
                    "مُسمًّى ردٌّ بلا وجه."
                )
        elif self.returns_to is not None:
            raise UsulDalalaSectionsError(
                "لا يُسمّى قسمٌ يرجع إليه بندٌ رُدَّ إلى اللغة أو رُدَّ تمحُّلًا؛ "
                "وتسميتُه تُقرأ إدراجًا وهو ردٌّ."
            )

    @property
    def outcome(self) -> AttributionOutcome:
        """كلُّ مردودٍ مردود؛ حالٌ مُشتَقّةٌ من جنس الصنف لا حقلٌ يُكتَب."""

        return AttributionOutcome.مردود


REJECTED_PROPOSALS: Final[tuple[ProposalRejection, ...]] = (
    ProposalRejection(
        proposal="الظاهر والمؤوَّل",
        ground=RejectionGround.تمحل_لا_يزيد_شيئا,
        statement=(
            "عُرِض قسمًا سادسًا فرُدَّ: لا يزيد على ما في الأقسام الخمسة، "
            "وإفرادُه بقسمٍ يُوهِم بابًا جديدًا وهو إعادةُ تسميةٍ لما فيها. "
            "والسابقةُ مُسجَّلةٌ هنا لا مرويّةً في تقرير، لأنّ سابقةً تُنسى لا "
            "تردُّ ثانيةً"
        ),
    ),
)


def attribute_proposal(
    proposal: str, section: DalalaSection | None
) -> AttributionOutcome:
    """اعرِض بندًا على السقف: يُسنَد إلى قسمٍ مُسمًّى، أو يُردّ.

    و`None` ليست قبولًا بلا قسم: هي تصريحٌ بأنّ البند لا يرجع إلى شيءٍ من
    الخمسة، ونتيجتُها الردُّ لا الإدراج. فمن أراد إدراجَ بندٍ لا يرجع إليها
    فعليه أن يُسمّي فتحَ السادس فتحًا، وهذه الدالّةُ لا تُسمّيه له.
    """

    _require_non_blank(proposal, "اسمُ البند المقترَح")
    if section is None:
        return AttributionOutcome.مردود
    if not isinstance(section, DalalaSection):
        raise UsulDalalaSectionsError(
            "القسمُ عضوٌ في المفردة الخماسية المغلقة أو لا شيء؛ "
            f"{FIVE_SECTIONS_ARE_CLOSED_NOTE}"
        )
    return AttributionOutcome.مسند_إلى_قسم


def modules_of_section(section: DalalaSection) -> tuple[str, ...]:
    """وحداتُ القسم المُعلَنةُ بأسمائها؛ والقسمُ بلا وحدةٍ يُرجِع تعدادًا فارغًا."""

    if not isinstance(section, DalalaSection):
        raise UsulDalalaSectionsError("القسمُ عضوٌ في المفردة الخماسية المغلقة.")
    return _SECTION_MODULES[section]


@dataclass(frozen=True, slots=True)
class SectionReading:
    """قراءةُ قسمٍ واحد: إعلانُه، ووحداتُه الموجودةُ فعلًا في الشجرة."""

    section: DalalaSection
    present_modules: tuple[str, ...]
    absent_modules: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.section, DalalaSection):
            raise UsulDalalaSectionsError("القسمُ عضوٌ في المفردة الخماسية المغلقة.")
        for value, label in (
            (self.present_modules, "الوحداتُ الموجودة"),
            (self.absent_modules, "الوحداتُ الغائبة"),
        ):
            if not isinstance(value, tuple):
                raise UsulDalalaSectionsError(f"{label} تعدادٌ مرتَّب.")
            for name in value:
                _require_non_blank(name, "اسمُ وحدة")
        declared = set(modules_of_section(self.section))
        if set(self.present_modules) | set(self.absent_modules) != declared:
            raise UsulDalalaSectionsError(
                f"قراءةُ قسم {self.section.value} لا تُغطّي وحداتِه المُعلَنة "
                "تغطيةً تامّة؛ وقراءةٌ ناقصةٌ تُخفي وحدةً لم يُقرَأ وجودُها."
            )

    @property
    def coding(self) -> SectionCoding:
        """`مُرمَّز` متى وُجدت وحدةٌ واحدةٌ من وحداته؛ مُشتَقًّا لا مكتوبًا."""

        return SectionCoding.مُرمَّز if self.present_modules else SectionCoding.غير_مُرمَّز

    @property
    def is_partial(self) -> bool:
        """قسمٌ بعضُ وحداته موجودٌ وبعضُها غائب؛ لا يُقرأ مُغطًّى ولا غيرَ مُغطًّى."""

        return bool(self.present_modules) and bool(self.absent_modules)


@dataclass(frozen=True, slots=True)
class SectionCoverageLedger:
    """سجلُّ الأقسام الخمسة كاملةً؛ ولا يُقرأ سجلٌّ ناقصُ قسم."""

    readings: tuple[SectionReading, ...]

    def __post_init__(self) -> None:
        seen: list[DalalaSection] = []
        for reading in self.readings:
            if not isinstance(reading, SectionReading):
                raise UsulDalalaSectionsError("كلُّ عنصرٍ قراءةُ قسمٍ مُصاغة.")
            if reading.section in seen:
                raise UsulDalalaSectionsError(
                    f"قسمٌ مكرّر في السجلّ: {reading.section.value}."
                )
            seen.append(reading.section)
        missing = tuple(section for section in DalalaSection if section not in seen)
        if missing:
            raise UsulDalalaSectionsError(
                "قسمٌ مفقودٌ من السجلّ: "
                + "، ".join(section.value for section in missing)
                + "؛ والتغطيةُ تسبق القراءة، وقسمٌ لم يُقرَأ ليس قسمًا مُغطًّى."
            )

    def reading_for(self, section: DalalaSection) -> SectionReading:
        """قراءةُ قسمٍ بعينه؛ والقسمُ موجودٌ بحكم التغطية."""

        for reading in self.readings:
            if reading.section is section:
                return reading
        raise UsulDalalaSectionsError(f"لا قراءةَ للقسم {section.value}.")

    @property
    def uncoded_sections(self) -> tuple[DalalaSection, ...]:
        """الأقسامُ التي لا وحدةَ لها في الشجرة، مُشتَقّةً من القراءة نفسها."""

        return tuple(
            reading.section
            for reading in self.readings
            if reading.coding is SectionCoding.غير_مُرمَّز
        )


def read_sections(root: Path | None = None) -> SectionCoverageLedger:
    """اقرأ الأقسامَ الخمسة، مُشتقًّا حالَ كلِّ قسمٍ من وجود وحداته في الشجرة."""

    base = repository_root_path() if root is None else root
    if not isinstance(base, Path):
        raise UsulDalalaSectionsError("جذرُ المستودع مسار.")
    package = base / ARABIC_PACKAGE_RELATIVE_PATH
    if not package.is_dir():
        raise UsulDalalaSectionsError(
            f"طبقةُ العربية غير موجودة عند {package}: شجرةٌ غائبةٌ تُقرأ «لا "
            "وحدات» وهو ادّعاءٌ لم تُقرأ الشجرة لأجله."
        )
    readings: list[SectionReading] = []
    for section in DalalaSection:
        present: list[str] = []
        absent: list[str] = []
        for name in modules_of_section(section):
            if (package / name).is_file():
                present.append(name)
            else:
                absent.append(name)
        readings.append(
            SectionReading(
                section=section,
                present_modules=tuple(present),
                absent_modules=tuple(absent),
            )
        )
    return SectionCoverageLedger(readings=tuple(readings))


def _assert_no_fields_matching(markers: tuple[str, ...]) -> None:
    for declaring_type in (ProposalRejection, SectionReading, SectionCoverageLedger):
        for field in fields(declaring_type):
            for marker in markers:
                if marker in field.name.lower():
                    raise RuntimeError(
                        f"{declaring_type.__name__} يحمل حقلاً محظورًا: {field.name}"
                    )


if len(DalalaSection) != 5:  # pragma: no cover - guard
    raise RuntimeError("الأقسامُ الحاكمةُ خمسةٌ لا سادس لها.")
if len(RejectionGround) != 3:  # pragma: no cover - guard
    raise RuntimeError("وجوهُ الردّ ثلاثةٌ مغلقة.")
if len(AttributionOutcome) != 2:  # pragma: no cover - guard
    raise RuntimeError("نتيجةُ العرض ثنائيةٌ مغلقة.")
if set(_SECTION_MODULES) != set(DalalaSection):  # pragma: no cover - guard
    raise RuntimeError("خريطةُ الوحدات غيرُ تامّةٍ على الأقسام الخمسة.")
if _SECTION_MODULES[DalalaSection.الناسخ_والمنسوخ]:  # pragma: no cover - guard
    raise RuntimeError(
        "الناسخُ والمنسوخ بلا وحدةٍ حتى يُنقَل نصُّه: " + NASKH_TEXT_NOT_EXTRACTED_RESIDUAL
    )
if not REJECTED_PROPOSALS:  # pragma: no cover - guard
    raise RuntimeError("سابقةُ الردّ مُسجَّلةٌ في الشجرة لا مرويّةٌ في تقرير.")
_assert_no_fields_matching(_FORBIDDEN_FIELD_MARKERS)
