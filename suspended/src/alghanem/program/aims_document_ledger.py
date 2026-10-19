"""قارئ وثيقة الغايات: السجلّ المكتوب يُقابَل بنصّه المصدر، فيُرفَض الانحراف.

هذه **المرحلة الرابعة من الطور الثاني** لـ AIM.1، وهي الدرجة التي تُخضِع طبقةَ
الغايات لما تُخضِع له غيرَها. المراحل الثلاث السابقة بنت سجلًّا (`aims`) ثم ثلاثة
قرّاءٍ يُقابلون المُعلَن بالمُشتَقّ في **وثيقة الدستور** و**شيفرة المستودع**؛
وبقي سجلُّ الغايات نفسُه منقولًا بيدٍ من نثر `docs/AIMS.md` بلا أيّ مقابلة. أي
أن الطبقة كانت تُلزِم غيرَها بقاعدةٍ لا تُلزِم نفسَها بها::

    AimsDocument      != AimRecord
    HandTranscription != DerivedCorrespondence
    AimsDocument      != Authority

وهذا إعمالُ `G0.F` في موضعه لا استعارةٌ لاسمه: القانون الذي طُبِّق في تجربةٍ
أدنى (`constitution_ledger` على وثيقة الدستور) يُعاد فتحُه في تجربةٍ أعلى على
الوثيقة التي تحكم القارئ نفسَه، بلا أن يُنسَخ ولا يُعاد تسميتُه.

**المصدر التصميمي المباشر، مُستشهَدًا به لا مُعادًا اشتقاقه.** شكلُ «الجهة
تُعلن، والقارئ لا يقبل إلا من مفردةٍ مغلقة يملكها هو، والمخالفة تُرفَض عند
الإنشاء» مأخوذٌ من سؤال التدقيق المفتوح
`DeclaredVersusDerivedRecurrenceNotExplained` بوصفه **مصدرًا مباشرًا** (إلزام §٥
من `docs/AIMS.md`)، لا بوصفه بديهةً تُعاد هنا صامتةً. وذلك السؤال مرصودٌ غير
مفسَّر، فلا يُستحدَث له اسمٌ عامّ ولا صنفُ أساسٍ مشترك يوحّد الشكل بين القرّاء
الأربعة؛ يُستعمل في موضعه ويُنسَب إلى سؤاله.

**ما يُقابَل هنا هوية وتصنيفٌ وبنية، لا نثرٌ حرفيّ.** نصُّ `AimRecord` **مُعاد
الصياغة** لا منقولٌ حرفيًّا عن §٢ (تُحذَف علامات الترميز، وتُوحَّد الحواشي،
ويُضاف اسم الملف إلى المستند)، فمقابلةُ النصّ حرفًا بحرف كانت سترفض السجلّ
القائم كلَّه أو تُجبره على شكلٍ لم تُصرّح به الوثيقة. فالمقابلة المُشتَقّة هنا
على ما تحتمله الوثيقة فعلًا: **حضورُ الغاية وترتيبُها**، و**وسومُ نقاطها
الأربع**، و**تصنيفُ §٣**، و**بقيّةُ البلوغ الجزئيّ**. وما لا يُقابَل مُسمّى في
`NAMED_RESIDUALS` لا مطويّ.

**استيراد `AimId` هنا ليس المؤشر.** القرّاء الثلاثة السابقون مُنعوا من استيراد
`AimId`، لأن ربط **عددٍ مقروء** بغايةٍ بعينها هو المؤشر نفسه. وهذا القارئ يربط
الغاية بـ**نصّها المصدر** لا بعددٍ: لا يُحصي صفوف دستورٍ ولا أسئلةَ تدقيقٍ ولا
قيمًا محجوزة، ولا يُرجّح غايةً على غاية، ولا يشتقّ منها كمًّا. والفارق بنيويّ لا
لفظيّ: لا تستورد هذه الوحدة أيًّا من القرّاء الثلاثة، ويُفحَص ذلك آليًّا.

**الرفض لا التخطّي الصامت، مرفوعًا إلى طبقة النقطة.** ارتفعت القاعدة في
`constitution_ledger` من الخلية إلى الجدول، ثم في `deferred_value_ledger` إلى
الحارس؛ وترتفع هنا إلى **النقطة**: كلّ نقطةٍ في §٢ و§٣ إمّا مقروءةٌ بوسمٍ من
مفردةٍ مغلقة، أو مُستبعَدةٌ بوسمٍ مُصرَّح باستبعاده، أو مرفوضةٌ باسمها وموضعها.
ونقطةٌ تسقط صامتةً تُنتج غايةً ناقصةَ الحقول تُقرَأ لاحقًا «هكذا صرّحت الوثيقة».

**التعداد خاصّيةٌ تُحسَب لا حقلٌ يُكتَب** (§٤): لا حقلَ عددٍ في أيّ صنفٍ هنا.

**خمولٌ سلطويّ**: `AimsDocumentLedger != BirthVerdict`؛ لا تُصدر هذه الوحدة
ولادةً ولا حكمًا ولا تجميدًا ولا `E0`، ولا تُصدر بلوغَ غايةٍ ولا تُرقّيه، ولا
تقرؤها أيّ وحدةٍ في `kernel/`، وهو ما يفحصه اختبارٌ يمسح وحداتها.

**وترتيب الغايات ترتيبُ ورودها في §٢**، لا ترتيبَ أهمّية ولا أولوية (§٦).
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from types import MappingProxyType
from typing import Final

from .aims import (
    AIM_RECORDS,
    DESIGN_SOURCE_OPEN_QUESTION,
    AimEngagement,
    AimId,
    AimRecord,
    AttainmentStanding,
)

AIMS_RELATIVE_PATH: Final = "docs/AIMS.md"

AIMS_DOCUMENT_LEDGER_AUTHORITY_NOTE: Final = (
    "قراءةٌ ومقابلةٌ فقط: لا يُنتج هذا الدفتر ولادةً ولا حكمًا ولا تجميدًا ولا "
    "`E0`، ولا يُصدر بلوغَ غايةٍ ولا يُرقّيه، ولا تقرؤه بوّابةٌ في النواة"
)

NO_INDICATOR_IN_THIS_READER_NOTE: Final = (
    "لا مؤشر هنا: المؤشر ربطُ عددٍ مُشتَقّ بغايةٍ بعينها، وهذا القارئ يربط "
    "الغاية بنصّها المصدر لا بعدد؛ فلا يستورد أيًّا من القرّاء الثلاثة ولا "
    "يُحصي صفًّا ولا سؤالًا ولا قيمةً محجوزة، ويُفحَص ذلك آليًّا"
)

DESIGN_SOURCE_CITATION_NOTE: Final = (
    "شكلُ «الوثيقة تُعلن، والقارئ لا يقبل إلا من مفردةٍ مغلقة يملكها، "
    f"والمخالفة تُرفَض» مأخوذٌ من `{DESIGN_SOURCE_OPEN_QUESTION}` مصدرًا "
    "مباشرًا، لا بديهةً تُعاد هنا صامتةً"
)

UNKNOWN_BULLET_LABEL_IS_REFUSED_NOTE: Final = (
    "نقطةٌ بوسمٍ خارج المفردة المغلقة تُوقف القراءة ولا تُتخطّى: النقطةُ "
    "الساقطة تُنتج غايةً ناقصةَ الحقول تُقرَأ لاحقًا «هكذا صرّحت الوثيقة»"
)

RECORD_DISAGREES_WITH_DOCUMENT_NOTE: Final = (
    "سجلٌّ يخالف وثيقته يُرفَض عند الإنشاء ولا يُقرَّر: السجلّ لا يُصحّح "
    "الوثيقة، والوثيقة لا يُعاد كتابتها لتوافق السجلّ"
)

FRACTAL_SELF_SUBJECTION_NOTE: Final = (
    "القاعدة التي طُبِّقت على وثيقة الدستور تُعاد هنا على وثيقة الغايات "
    "نفسها: طبقةٌ تُلزِم غيرَها بمقابلة المُعلَن بالمُشتَقّ ولا تُلزِم نفسَها "
    "بها تُعفي نفسَها من قانونها، وإعفاءُ النفس ليس حدًّا مُعلَنًا بل ثغرة"
)

RECORD_PROSE_IS_PARAPHRASE_NOT_TRANSCRIPTION: Final = (
    "RECORD_PROSE_IS_PARAPHRASE_NOT_TRANSCRIPTION"
)

TRANSCRIPTION_FIDELITY_IS_NOT_AIM_TRUTH: Final = (
    "TRANSCRIPTION_FIDELITY_IS_NOT_AIM_TRUTH"
)

SECTION_3_CLASSIFIES_SIX_OF_THIRTEEN: Final = "SECTION_3_CLASSIFIES_SIX_OF_THIRTEEN"

NAMED_RESIDUALS: Final[Mapping[str, str]] = MappingProxyType(
    {
        RECORD_PROSE_IS_PARAPHRASE_NOT_TRANSCRIPTION: (
            "نصّ `AimRecord` مُعاد الصياغة لا منقولٌ حرفيًّا عن §٢: تُحذَف "
            "علامات الترميز، وتُوحَّد الحواشي، ويُضاف اسم الملف إلى المستند. "
            "فالمقابلة هنا على الهوية والترتيب ووسوم النقاط والتصنيف "
            "والبقيّة، ولا تشمل النثر حرفًا بحرف؛ فغايةٌ نُقل نثرُها بمعنًى "
            "مغاير مع بقاء بنيتها لا يكشفها هذا القارئ، وإلزامُ النقل الحرفيّ "
            "يفرض على الوثيقة شكلًا لم تُصرّح به"
        ),
        TRANSCRIPTION_FIDELITY_IS_NOT_AIM_TRUTH: (
            "مطابقةُ السجلّ لوثيقته ليست تحقّقًا من صدق الغاية ولا من بلوغها: "
            "غايةٌ خاطئةٌ منقولةٌ بأمانةٍ تامّة تجتاز هذا القارئ كاملًا. "
            "فالمقابلة تُغلق فجوة النقل اليدويّ وحدها، ولا تُرقّي غايةً ولا "
            "تشهد لها"
        ),
        SECTION_3_CLASSIFIES_SIX_OF_THIRTEEN: (
            "§٣ تُصنّف ستًّا من ثلاث عشرة، والباقي يُشتَقّ له "
            "`UNCLASSIFIED_IN_RECORD`. وهذا يُقابَل بالسجلّ فيُرفَض خلافُه، "
            "لكنّ غيابَ التصنيف في الوثيقة يبقى غيابًا: لا شيء هنا يكشف أن "
            "غايةً غيرَ مُصنَّفة كان يجب أن تُصنَّف"
        ),
    }
)

_SECTION_2_HEADING: Final = "## ٢."
_SECTION_3_HEADING: Final = "## ٣."
_SECTION_4_HEADING: Final = "## ٤."

_AIM_HEADING: Final = re.compile(r"^### (?P<aim>AIM-[A-Z]\d) — (?P<title>.+)$")
_BULLET: Final = re.compile(r"^\* (?P<body>.+)$")
_CLASSIFICATION: Final = re.compile(r"^\* \*\*(?P<label>[^*]+)\*\*: (?P<body>.+)$")
_AIM_REFERENCE: Final = re.compile(r"AIM-[A-Z]\d")


class AimsDocumentLedgerError(ValueError):
    """قراءةٌ أو مقابلةٌ مرفوضة؛ لا تُحمَل الوثيقة على أقرب شكلٍ مقبول."""


class DeclaredAimBullet(Enum):
    """وسوم نقاط §٢، مفردةً مغلقة مُستخرَجة من نصّ الوثيقة لا مُبتكَرة.

    الوسمان `ATTAINMENT_REACHED_TODAY` و`NAMED_REMAINDER` واردان في غايةٍ واحدة
    (`AIM-X1`)؛ وإسقاطهما من المفردة لأنهما شاذّان يُسقط تلك الغاية صامتةً،
    وتوحيدُهما مع `ATTAINMENT` يُلغي الفارق الذي صرّحت به الوثيقة نفسها.
    """

    QUESTION = "السؤال"
    ATTAINMENT = "البلوغ"
    ATTAINMENT_REACHED_TODAY = "البلوغ الحاصل اليوم"
    NAMED_REMAINDER = "ما بقي مفتوحًا فيها"
    NOT_ATTAINMENT = "ليس بلوغًا"
    CITATION = "المستند"

    @property
    def declares_attainment(self) -> bool:
        """أهذا الوسمُ وسمَ بلوغٍ، بشكلَيه التامّ والجزئيّ؟"""

        return self in (
            DeclaredAimBullet.ATTAINMENT,
            DeclaredAimBullet.ATTAINMENT_REACHED_TODAY,
        )


class DeclaredEngagementClass(Enum):
    """تصنيفا §٣ كما وردا نصًّا بين علامتَي التوكيد، لا كما يُقدَّر."""

    NOT_STARTED = "لم تبدأ"
    BLOCKED_BY_NAMED_OBSTACLE = "بدأت واصطدمت بحاجزٍ مُسمّى"

    @property
    def engagement(self) -> AimEngagement:
        """رتبة الانشغال المقابلة في السجلّ؛ المفردتان لا تُدمَجان."""

        if self is DeclaredEngagementClass.NOT_STARTED:
            return AimEngagement.NOT_STARTED
        return AimEngagement.BLOCKED_BY_NAMED_OBSTACLE


_BULLET_BY_LABEL: Final[Mapping[str, DeclaredAimBullet]] = MappingProxyType(
    {member.value: member for member in DeclaredAimBullet}
)

_CLASS_BY_LABEL: Final[Mapping[str, DeclaredEngagementClass]] = MappingProxyType(
    {member.value: member for member in DeclaredEngagementClass}
)

_REQUIRED_BULLETS: Final = (
    DeclaredAimBullet.QUESTION,
    DeclaredAimBullet.NOT_ATTAINMENT,
    DeclaredAimBullet.CITATION,
)

if len(_BULLET_BY_LABEL) != len(DeclaredAimBullet):  # pragma: no cover - guard
    raise RuntimeError("two bullet labels must not share one declared text")
if len(_CLASS_BY_LABEL) != len(DeclaredEngagementClass):  # pragma: no cover - guard
    raise RuntimeError("two classes must not share one declared text")
if len(DeclaredEngagementClass) != 2:  # pragma: no cover - guard
    raise RuntimeError("section 3 declares exactly two classes")


def _require_non_blank(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise AimsDocumentLedgerError(f"{field_name} نصٌّ غير فارغ")
    return value


def _require_positive_line(value: int, field_name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise AimsDocumentLedgerError(f"{field_name} رقم سطرٍ موجب")
    return value


@dataclass(frozen=True, slots=True)
class ReadBullet:
    """نقطةٌ واحدة مقروءة بوسمٍ من المفردة المغلقة، بموضعها ونصّها."""

    label: DeclaredAimBullet
    body: str
    document_line: int

    def __post_init__(self) -> None:
        if not isinstance(self.label, DeclaredAimBullet):
            raise AimsDocumentLedgerError("وسم النقطة من مفردته المغلقة")
        _require_non_blank(self.body, "نصّ النقطة")
        _require_positive_line(self.document_line, "موضع النقطة")


@dataclass(frozen=True, slots=True)
class BulletCensus:
    """إحصاءُ نقاط §٢ كلِّها بترتيب ورودها، فلا تسقط نقطةٌ صامتةً.

    لا حقلَ عددٍ هنا؛ التعدادُ خاصّيةٌ تُحسَب من النقاط المرصودة.
    """

    bullets: tuple[ReadBullet, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.bullets, tuple) or not self.bullets:
            raise AimsDocumentLedgerError("إحصاء النقاط مجموعةٌ غير فارغة")
        previous_line = 0
        for bullet in self.bullets:
            if not isinstance(bullet, ReadBullet):
                raise AimsDocumentLedgerError("كل عنصرٍ نقطةٌ مقروءة")
            if bullet.document_line <= previous_line:
                raise AimsDocumentLedgerError("ترتيب النقاط ترتيبُ ورودها في الوثيقة")
            previous_line = bullet.document_line

    @property
    def bullet_count(self) -> int:
        """عدد النقاط المرصودة، محسوبًا لا مكتوبًا."""

        return len(self.bullets)

    def bullets_with_label(self, label: DeclaredAimBullet) -> tuple[ReadBullet, ...]:
        """نقاطُ وسمٍ بعينه بترتيب ورودها في الوثيقة."""

        if not isinstance(label, DeclaredAimBullet):
            raise AimsDocumentLedgerError("وسم النقطة من مفردته المغلقة")
        return tuple(bullet for bullet in self.bullets if bullet.label is label)


@dataclass(frozen=True, slots=True)
class ReadAimEntry:
    """مدخلُ غايةٍ واحد كما قُرئ من §٢: معرّفها وعنوانها ونقاطها."""

    aim_id: AimId
    title: str
    bullets: tuple[ReadBullet, ...]
    document_line: int

    def __post_init__(self) -> None:
        if not isinstance(self.aim_id, AimId):
            raise AimsDocumentLedgerError("معرّف الغاية من مفردته المغلقة")
        _require_non_blank(self.title, "عنوان الغاية")
        _require_positive_line(self.document_line, "موضع الغاية")
        if not isinstance(self.bullets, tuple) or not self.bullets:
            raise AimsDocumentLedgerError("نقاط الغاية مجموعةٌ غير فارغة")
        labels = []
        for bullet in self.bullets:
            if not isinstance(bullet, ReadBullet):
                raise AimsDocumentLedgerError("كل عنصرٍ نقطةٌ مقروءة")
            if bullet.label in labels:
                raise AimsDocumentLedgerError(
                    f"{self.aim_id.value}: وسمٌ مكرّر "
                    f"{bullet.label.value} — التكرار يُخفي نقطةً تحت أخرى"
                )
            labels.append(bullet.label)

        missing = [label for label in _REQUIRED_BULLETS if label not in labels]
        if missing:
            raise AimsDocumentLedgerError(
                f"{self.aim_id.value}: نقاطٌ لازمةٌ غائبة: "
                + "، ".join(label.value for label in missing)
            )
        attainment = [label for label in labels if label.declares_attainment]
        if len(attainment) != 1:
            raise AimsDocumentLedgerError(
                f"{self.aim_id.value}: تُعلَن نقطةُ بلوغٍ واحدة لا "
                f"{len(attainment)}؛ فغيابُها يُسقط ما تُصرّح به الوثيقة، "
                "واجتماعُ شكلَيها يُعلن بلوغين متنافيين"
            )
        remainder = DeclaredAimBullet.NAMED_REMAINDER in labels
        partial = DeclaredAimBullet.ATTAINMENT_REACHED_TODAY in labels
        if remainder and not partial:
            raise AimsDocumentLedgerError(
                f"{self.aim_id.value}: بقيّةٌ مُسمّاة بلا بلوغٍ حاصلٍ اليوم — "
                "البقيّة بقيّةُ بلوغٍ جزئيّ، ولا بقيّةَ لما لم يُبلَغ منه شيء"
            )
        if partial and not remainder:
            raise AimsDocumentLedgerError(
                f"{self.aim_id.value}: بلوغٌ حاصلٌ اليوم بلا بقيّةٍ مُسمّاة — "
                "البقيّة حقلٌ إلزاميّ مع البلوغ الجزئيّ، وإلا قُرئ بلوغًا تامًّا"
            )

    @property
    def declared_attainment(self) -> AttainmentStanding:
        """رتبةُ البلوغ كما تحتملها نقاطُ هذه الغاية، مُشتَقّةً لا مكتوبة."""

        for bullet in self.bullets:
            if bullet.label is DeclaredAimBullet.ATTAINMENT_REACHED_TODAY:
                return AttainmentStanding.PARTIALLY_REACHED_WITH_NAMED_REMAINDER
        return AttainmentStanding.NOT_REACHED

    def bullet(self, label: DeclaredAimBullet) -> ReadBullet | None:
        """نقطةُ وسمٍ بعينه إن وُجدت؛ وغيابُها `None` لا نصٌّ فارغ."""

        if not isinstance(label, DeclaredAimBullet):
            raise AimsDocumentLedgerError("وسم النقطة من مفردته المغلقة")
        for bullet in self.bullets:
            if bullet.label is label:
                return bullet
        return None


@dataclass(frozen=True, slots=True)
class ReadClassification:
    """صفُّ تصنيفٍ واحد من §٣: صنفُه والغاياتُ المذكورة فيه وموضعُه."""

    declared_class: DeclaredEngagementClass
    aim_ids: tuple[AimId, ...]
    document_line: int

    def __post_init__(self) -> None:
        if not isinstance(self.declared_class, DeclaredEngagementClass):
            raise AimsDocumentLedgerError("صنف الانشغال من مفردته المغلقة")
        _require_positive_line(self.document_line, "موضع التصنيف")
        if not isinstance(self.aim_ids, tuple) or not self.aim_ids:
            raise AimsDocumentLedgerError("صفُّ تصنيفٍ بلا غاياتٍ لا يُصنّف شيئًا")
        seen: set[AimId] = set()
        for aim_id in self.aim_ids:
            if not isinstance(aim_id, AimId):
                raise AimsDocumentLedgerError("كل معرّفٍ من مفردته المغلقة")
            if aim_id in seen:
                raise AimsDocumentLedgerError(f"غايةٌ مكرّرة في صفٍّ: {aim_id.value}")
            seen.add(aim_id)


@dataclass(frozen=True, slots=True)
class AimsDocumentLedger:
    """وثيقة الغايات مقروءةً: مداخلُ §٢، وتصنيفاتُ §٣، وإحصاءُ النقاط."""

    entries: tuple[ReadAimEntry, ...]
    classifications: tuple[ReadClassification, ...]
    bullets: BulletCensus

    def __post_init__(self) -> None:
        if not isinstance(self.entries, tuple) or not self.entries:
            raise AimsDocumentLedgerError("مداخل الغايات مجموعةٌ غير فارغة")
        if not isinstance(self.classifications, tuple) or not self.classifications:
            raise AimsDocumentLedgerError("تصنيفات §٣ مجموعةٌ غير فارغة")
        if not isinstance(self.bullets, BulletCensus):
            raise AimsDocumentLedgerError("إحصاء النقاط من نوعه")

        seen: set[AimId] = set()
        previous_line = 0
        for entry in self.entries:
            if not isinstance(entry, ReadAimEntry):
                raise AimsDocumentLedgerError("كل عنصرٍ مدخلُ غايةٍ مقروء")
            if entry.aim_id in seen:
                raise AimsDocumentLedgerError(
                    f"غايةٌ مكرّرة في §٢: {entry.aim_id.value} — التكرار يُفسد "
                    "المقابلة ولا يُطوى"
                )
            seen.add(entry.aim_id)
            if entry.document_line <= previous_line:
                raise AimsDocumentLedgerError("ترتيب الغايات ترتيبُ ورودها في §٢")
            previous_line = entry.document_line

        classified: set[AimId] = set()
        for row in self.classifications:
            if not isinstance(row, ReadClassification):
                raise AimsDocumentLedgerError("كل عنصرٍ صفُّ تصنيفٍ مقروء")
            for aim_id in row.aim_ids:
                if aim_id in classified:
                    raise AimsDocumentLedgerError(
                        f"غايةٌ مُصنَّفة مرّتين: {aim_id.value} — غايةٌ واحدة "
                        "لا تكون «لم تبدأ» و«بدأت» معًا"
                    )
                classified.add(aim_id)
                if aim_id not in seen:
                    raise AimsDocumentLedgerError(
                        f"§٣ تُصنّف غايةً لا مدخلَ لها في §٢: {aim_id.value}"
                    )

    @property
    def entry_count(self) -> int:
        """عدد الغايات المقروءة من §٢، محسوبًا لا مكتوبًا."""

        return len(self.entries)

    @property
    def classified_count(self) -> int:
        """عدد الغايات التي صنّفتها §٣، محسوبًا لا مكتوبًا."""

        return sum(len(row.aim_ids) for row in self.classifications)

    @property
    def declared_engagements(self) -> Mapping[AimId, AimEngagement]:
        """رتبةُ انشغالٍ لكلّ غاية، والجهلُ عضوٌ صريح لا فراغٌ يُطوى."""

        derived = dict.fromkeys(
            (entry.aim_id for entry in self.entries),
            AimEngagement.UNCLASSIFIED_IN_RECORD,
        )
        for row in self.classifications:
            for aim_id in row.aim_ids:
                derived[aim_id] = row.declared_class.engagement
        return MappingProxyType(derived)

    def entry(self, aim_id: AimId) -> ReadAimEntry:
        """مدخلُ غايةٍ بعينها؛ وغيابُه رفضٌ مُسمّى لا `None` يُطوى."""

        if not isinstance(aim_id, AimId):
            raise AimsDocumentLedgerError("معرّف الغاية من مفردته المغلقة")
        for entry in self.entries:
            if entry.aim_id is aim_id:
                return entry
        raise AimsDocumentLedgerError(f"لا مدخلَ في §٢ للغاية: {aim_id.value}")


@dataclass(frozen=True, slots=True)
class AimRecordCorrespondence:
    """مقابلةُ السجلّ المكتوب بوثيقته، مرفوضةً عند أوّل انحراف.

    لا حقلَ نتيجةٍ هنا ولا «مطابق/غير مطابق»: قيامُ هذا الصنف **هو** المطابقة،
    وانحرافُها استثناءٌ مُسمّى عند الإنشاء. فحقلُ نتيجةٍ يُتيح حملَ مقابلةٍ
    فاشلة والتقريرَ عنها، وهو بعينه ما تمنعه §٤ («المخالفة تُرفَض لا تُقرَّر»).
    """

    ledger: AimsDocumentLedger
    records: Mapping[AimId, AimRecord]

    def __post_init__(self) -> None:
        if not isinstance(self.ledger, AimsDocumentLedger):
            raise AimsDocumentLedgerError("دفتر الوثيقة من نوعه")
        if not isinstance(self.records, Mapping) or not self.records:
            raise AimsDocumentLedgerError("سجلّ الغايات مفردٌ غير فارغ")

        documented = tuple(entry.aim_id for entry in self.ledger.entries)
        recorded = tuple(self.records)
        if documented != recorded:
            missing = [aim.value for aim in documented if aim not in self.records]
            extra = [aim.value for aim in recorded if aim not in documented]
            raise AimsDocumentLedgerError(
                "ترتيبُ السجلّ أو محتواه يخالف §٢: "
                f"غاياتٌ في الوثيقة بلا سجلّ {missing}، "
                f"وغاياتٌ في السجلّ بلا مدخلٍ في الوثيقة {extra} — "
                f"{RECORD_DISAGREES_WITH_DOCUMENT_NOTE}"
            )

        engagements = self.ledger.declared_engagements
        for aim_id, record in self.records.items():
            if not isinstance(record, AimRecord):
                raise AimsDocumentLedgerError("كل عنصرٍ سجلُّ غايةٍ")
            if record.aim_id is not aim_id:
                raise AimsDocumentLedgerError(
                    f"مفتاحُ السجلّ {aim_id.value} يخالف معرّفه " f"{record.aim_id.value}"
                )
            declared = engagements[aim_id]
            if record.engagement is not declared:
                raise AimsDocumentLedgerError(
                    f"{aim_id.value}: انشغالٌ مُعلَنٌ في §٣ {declared.value} "
                    f"وانشغالٌ مكتوبٌ في السجلّ {record.engagement.value} — "
                    f"{RECORD_DISAGREES_WITH_DOCUMENT_NOTE}"
                )
            entry = self.ledger.entry(aim_id)
            if record.attainment is not entry.declared_attainment:
                raise AimsDocumentLedgerError(
                    f"{aim_id.value}: بلوغٌ مُشتَقٌّ من §٢ "
                    f"{entry.declared_attainment.value} وبلوغٌ مكتوبٌ في السجلّ "
                    f"{record.attainment.value} — "
                    f"{RECORD_DISAGREES_WITH_DOCUMENT_NOTE}"
                )

    @property
    def corresponded_count(self) -> int:
        """عدد الغايات التي قوبلت بنصّها، محسوبًا لا مكتوبًا."""

        return len(self.records)

    @property
    def unclassified_aims(self) -> tuple[AimId, ...]:
        """الغايات التي لم تُصنّفها §٣، بترتيب ورودها في §٢."""

        engagements = self.ledger.declared_engagements
        return tuple(
            aim_id
            for aim_id in engagements
            if engagements[aim_id] is AimEngagement.UNCLASSIFIED_IN_RECORD
        )


def _section_bounds(lines: list[str], heading: str, stop: str) -> tuple[int, int]:
    start = -1
    for index, line in enumerate(lines):
        if line.startswith(heading):
            start = index + 1
            break
    if start < 0:
        raise AimsDocumentLedgerError(f"قسمٌ مفقود في وثيقة الغايات: {heading}")
    for index in range(start, len(lines)):
        if lines[index].startswith(stop):
            return start, index
    raise AimsDocumentLedgerError(f"قسمٌ بلا نهايةٍ مُعلَنة: {heading}")


def _logical_bullets(lines: list[str], start: int, end: int) -> list[tuple[int, str]]:
    """اجمع كلّ نقطةٍ مع أسطر امتدادها في سطرٍ منطقيّ واحد، فلا يُبتَر نصّها."""

    bullets: list[tuple[int, str]] = []
    open_bullet = False
    for index in range(start, end):
        line = lines[index]
        if _BULLET.match(line):
            bullets.append((index + 1, line.rstrip()))
            open_bullet = True
            continue
        stripped = line.strip()
        if open_bullet and stripped and line[:1].isspace():
            number, body = bullets[-1]
            bullets[-1] = (number, f"{body} {stripped}")
            continue
        open_bullet = False
    return bullets


def _declared_label(body: str, number: int) -> tuple[DeclaredAimBullet, str]:
    """طابِق أطولَ وسمٍ مُصرَّح به، ورُدَّ ما خرج عن المفردة باسمه وموضعه."""

    for label in sorted(_BULLET_BY_LABEL, key=len, reverse=True):
        if not body.startswith(label):
            continue
        rest = body[len(label) :]
        if rest.startswith(":"):
            return _BULLET_BY_LABEL[label], rest[1:].strip()
        if rest.startswith(" — "):
            return _BULLET_BY_LABEL[label], rest[3:].strip()
    raise AimsDocumentLedgerError(
        f"نقطةٌ بوسمٍ خارج المفردة المغلقة عند السطر {number}: "
        f"{body[:60]!r} — {UNKNOWN_BULLET_LABEL_IS_REFUSED_NOTE}"
    )


def _read_entries(
    lines: list[str], start: int, end: int
) -> tuple[tuple[ReadAimEntry, ...], BulletCensus]:
    entries: list[ReadAimEntry] = []
    census: list[ReadBullet] = []
    heading_line = 0
    aim_id: AimId | None = None
    title = ""
    bullets: list[ReadBullet] = []

    def flush() -> None:
        if aim_id is None:
            return
        entries.append(
            ReadAimEntry(
                aim_id=aim_id,
                title=title,
                bullets=tuple(bullets),
                document_line=heading_line,
            )
        )

    index = start
    while index < end:
        line = lines[index]
        heading = _AIM_HEADING.match(line.rstrip())
        if heading is not None:
            flush()
            try:
                aim_id = AimId(heading.group("aim"))
            except ValueError as error:
                raise AimsDocumentLedgerError(
                    f"غايةٌ في §٢ خارج المفردة المغلقة عند السطر {index + 1}: "
                    f"{heading.group('aim')}"
                ) from error
            title = heading.group("title").strip()
            heading_line = index + 1
            bullets = []
            index += 1
            continue
        if _BULLET.match(line) and aim_id is not None:
            block_end = index + 1
            while block_end < end and not (
                _BULLET.match(lines[block_end]) or lines[block_end].startswith("#")
            ):
                block_end += 1
            for number, text in _logical_bullets(lines, index, block_end):
                body = _BULLET.match(text)
                assert body is not None
                label, value = _declared_label(body.group("body").strip(), number)
                bullet = ReadBullet(label=label, body=value, document_line=number)
                bullets.append(bullet)
                census.append(bullet)
            index = block_end
            continue
        index += 1
    flush()
    if not entries:
        raise AimsDocumentLedgerError("لم يُقرَأ أيّ مدخل غايةٍ من §٢")
    return tuple(entries), BulletCensus(bullets=tuple(census))


def _read_classifications(
    lines: list[str], start: int, end: int
) -> tuple[ReadClassification, ...]:
    rows: list[ReadClassification] = []
    for number, text in _logical_bullets(lines, start, end):
        match = _CLASSIFICATION.match(text)
        if match is None:
            continue
        label = match.group("label").strip()
        declared = _CLASS_BY_LABEL.get(label)
        if declared is None:
            raise AimsDocumentLedgerError(
                f"صنفٌ خارج المفردة المغلقة عند السطر {number}: {label!r} — "
                f"{UNKNOWN_BULLET_LABEL_IS_REFUSED_NOTE}"
            )
        names = _AIM_REFERENCE.findall(match.group("body"))
        rows.append(
            ReadClassification(
                declared_class=declared,
                aim_ids=tuple(AimId(name) for name in dict.fromkeys(names)),
                document_line=number,
            )
        )
    if not rows:
        raise AimsDocumentLedgerError("لم يُقرَأ أيّ تصنيفٍ من §٣")
    return tuple(rows)


def read_aims_document(document_text: str) -> AimsDocumentLedger:
    """اقرأ §٢ و§٣ من نصّ وثيقة الغايات، ورُدَّ ما خرج عن مفرداتها المغلقة."""

    if not isinstance(document_text, str) or not document_text.strip():
        raise AimsDocumentLedgerError("نصّ الوثيقة نصٌّ غير فارغ")
    lines = document_text.splitlines()
    entries_start, entries_end = _section_bounds(
        lines, _SECTION_2_HEADING, _SECTION_3_HEADING
    )
    entries, census = _read_entries(lines, entries_start, entries_end)
    classes_start, classes_end = _section_bounds(
        lines, _SECTION_3_HEADING, _SECTION_4_HEADING
    )
    classifications = _read_classifications(lines, classes_start, classes_end)
    return AimsDocumentLedger(
        entries=entries, classifications=classifications, bullets=census
    )


def aims_document_path() -> Path:
    """موضع وثيقة الغايات في شجرة المستودع، مشتقًّا من موضع هذه الوحدة."""

    return Path(__file__).resolve().parents[3] / AIMS_RELATIVE_PATH


def load_aims_document(path: Path | None = None) -> AimsDocumentLedger:
    """اقرأ الوثيقة نفسها؛ وغيابُها رفضٌ مُسمّى لا دفترٌ فارغ."""

    document = aims_document_path() if path is None else path
    if not isinstance(document, Path):
        raise AimsDocumentLedgerError("موضع الوثيقة مسارٌ")
    try:
        text = document.read_text(encoding="utf-8")
    except OSError as error:
        raise AimsDocumentLedgerError(
            f"تعذّرت قراءة وثيقة الغايات عند {document}: دفترٌ فارغ يُقرَأ "
            "«لا غايات» وهو ادّعاءٌ لم تُقرَأ الوثيقة لأجله"
        ) from error
    return read_aims_document(text)


def correspond_records_to_document(
    path: Path | None = None,
) -> AimRecordCorrespondence:
    """قابِل السجلّ المكتوب بوثيقته؛ وقيامُ المقابلة هو المطابقة نفسها."""

    return AimRecordCorrespondence(ledger=load_aims_document(path), records=AIM_RECORDS)


__all__ = [
    "AIMS_DOCUMENT_LEDGER_AUTHORITY_NOTE",
    "AIMS_RELATIVE_PATH",
    "DESIGN_SOURCE_CITATION_NOTE",
    "FRACTAL_SELF_SUBJECTION_NOTE",
    "NAMED_RESIDUALS",
    "NO_INDICATOR_IN_THIS_READER_NOTE",
    "RECORD_DISAGREES_WITH_DOCUMENT_NOTE",
    "RECORD_PROSE_IS_PARAPHRASE_NOT_TRANSCRIPTION",
    "SECTION_3_CLASSIFIES_SIX_OF_THIRTEEN",
    "TRANSCRIPTION_FIDELITY_IS_NOT_AIM_TRUTH",
    "UNKNOWN_BULLET_LABEL_IS_REFUSED_NOTE",
    "AimRecordCorrespondence",
    "AimsDocumentLedger",
    "AimsDocumentLedgerError",
    "BulletCensus",
    "DeclaredAimBullet",
    "DeclaredEngagementClass",
    "ReadAimEntry",
    "ReadBullet",
    "ReadClassification",
    "aims_document_path",
    "correspond_records_to_document",
    "load_aims_document",
    "read_aims_document",
]
