"""قناتا المنطوق والمفهوم وحالُ الإفادة، مؤشرًا معرفيًّا مُشتقًّا لكلّ غاية.

هذه **المرحلة الثامنة من الطور الثاني** لـ AIM.1. المرحلة السادسة ربطت بكلّ غايةٍ
عددَ مستنداتها المقروءة، ولم تقرأ **كيف** بلغ الاستشهادُ مستنده: أبلفظه الذي
نطق به، أم بما فُهِم منه ولم يُنطَق. وهذا القارئ يقرأ ذلك، ولا يُرقّي قراءته إلى
حكم::

    Mantuq        != Performance
    DerivedCount  != Progress
    Ifada         != Attainment
    AimsDocument  != Authority

**«مؤشر أداء» اسمٌ مرفوضٌ هنا بنصّ §١، ولا يُهرَّب داخل هذه الوحدة.** §١ تفصل
«هل الشيفرة تعمل؟» عن «هل الحكمُ مُستحَقٌّ بدليله؟»، وتمنع المؤشر الهندسيّ
منعًا صريحًا. فما يُشتَقّ هنا مؤشرٌ **معرفيّ** بشروط §٤: عددٌ مقروءٌ مربوطٌ
بغايةٍ بعينها، بلا نسبةٍ ولا رتبةٍ ولا ترتيبٍ بين غايتين ولا تقديرِ قربٍ من
بلوغ (§٦). ومنعُ الرتبة بنيةٌ لا وعد: يُفحَص اسمُ كلّ حقلٍ في كلّ صنفٍ هنا عند
الاستيراد.

**المصدر التصميميّ المباشر، مُستشهَدًا به لا مُعادًا اشتقاقه.** شكلُ «الجهة
تُعلن، والقارئ لا يقبل إلا من مفردةٍ مغلقة يملكها هو، والمخالفة تُرفَض عند
الإنشاء» مأخوذٌ من سؤال التدقيق المفتوح
`DeclaredVersusDerivedRecurrenceNotExplained` بوصفه **مصدرًا مباشرًا** (إلزام §٥
من `docs/AIMS.md`)، لا بوصفه بديهةً تُعاد هنا صامتةً؛ فلا يُستحدَث له اسمٌ عامّ
ولا صنفُ أساسٍ مشترك يوحّد الشكل بين القرّاء السبعة.

**المفردات مستوردةٌ من الطبقة العربية لا مُستحدَثةٌ ثانيةً.** `DalalaChannel` و
`MafhumKind` و`IfadaStanding` مُعرَّفةٌ في
`src/alghanem/arabic/mantuq_mafhum_ifada.py`، وتُقرَأ هنا كما هي. واستحداثُ
مفردةٍ ثانيةٍ بالأسماء نفسها في طبقة البرنامج كان سيُنشئ مفهومَين باسمٍ واحد،
وهو بعينه ما تمنعه تلك الوحدة في تفريقها بين `مفهوم` القناة و`مفهوم` المحتوى.
والاتّجاه محفوظ: البرنامج يقرأ العربية، ولا وحدةَ في `arabic/` ولا في `kernel/`
تقرأ هذه الوحدة.

**القناةُ مُشتَقّةٌ بقراءةٍ ثانية مستقلّة، لا منقولةٌ عن المرحلة السادسة.** تلك
المرحلة تُخبر أن الإشارة حُلَّت وإلامَ حُلَّت، ولا تُخبر **بأيّ طريقٍ** حُلَّت.
فيبني هذا القارئ فهرسَه بنفسه من دفتر الدستور ونصّ الوثيقة والشجرة: اسمٌ حاضرٌ
بحروفه مستندًا قائمًا فالإشارةُ **منطوقٌ** بها، واسمٌ لا يُحَلّ إلا بما لم
يُنطَق — معرّفُ صفٍّ يُغني عن تمام اسمه، أو صدرُ عنوانٍ يُغني عن تمامه —
فالإشارةُ **مفهومةٌ** منه. وإشارةٌ حلّتها المرحلة السادسة ولم يبلغها فهرسُ هذا
القارئ تُرفَض باسمها وغايتها، فالقراءتان المستقلّتان إذا اختلفتا لم يُرجَّح
أحدهما على الأخرى.

**الإفادةُ هنا بلوغُ حالةٍ مقروءة، لا فائدةٌ لغوية.** الاسمُ مستعارٌ من نصّ
«الغرض من التركيب الإفادة، وهذا لا يفيد؛ ولكنه موجود»، والمُقاس به هنا: إشارةٌ
بلغت مستندًا ذا حالةٍ مُعلَنة فهي `مُفيد`، وإشارةٌ بلغت مستندًا لا حالةَ له
(قسمٌ أو مسار) فحالُها `غير_مقروء` لا `غير_مُفيد` — وهو إعمالُ
`SECTION_HEADING_CARRIES_NO_DECLARED_STATUS` في موضعه — وإشارةٌ مُستبعَدةٌ
بإعلانٍ فهي `غير_مُفيد`: قائمةٌ في النصّ ولا تبلغ مستندًا، وهي صورةُ «موجودٌ ولا
يفيد» بعينها. وهذا المُقاس مُسمًّى في `NAMED_RESIDUALS` حدًّا لا يُطوى.

**لا حقلَ عددٍ البتّة** (§٤): كلّ عددٍ خاصّيةٌ تُحسَب من الإشارات المقروءة، وكلّ
عضوٍ في كلّ مفردةٍ حاضرٌ في الإحصاء ولو بصفر.

**خمولٌ سلطويّ مفحوص**: `DalalaIndicatorLedger != BirthVerdict`؛ لا تُصدر هذه
الوحدة ولادةً ولا حكمًا ولا تجميدًا ولا `E0`، ولا تكتب بلوغًا ولا تُرقّيه، ولا
تقرؤها أيّ وحدةٍ في `kernel/`. وترتيبُ الصفوف ترتيبُ ورود الغايات في §٢ (§٦).
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass, fields
from pathlib import Path
from types import MappingProxyType
from typing import Final

from ..arabic.mantuq_mafhum_ifada import DalalaChannel, IfadaStanding, MafhumKind
from .aim_indicator import (
    AimIndicatorLedger,
    CitedSupportKind,
    ReadCitationReference,
    read_aim_indicator_ledger,
    repository_root_path,
)
from .aims import AIM_RECORDS, DESIGN_SOURCE_OPEN_QUESTION, AimId
from .constitution_ledger import (
    ConstitutionLedger,
    constitution_document_path,
    load_constitution_ledger,
)

DALALA_INDICATOR_AUTHORITY_NOTE: Final = (
    "مؤشرٌ معرفيّ فقط: لا يُصدر هذا الدفتر ولادةً ولا حكم ولادة، ولا يُجمِّد، "
    "ولا يكتب بلوغَ غايةٍ ولا يُرقّيه، ولا تقرؤه أيّ بوّابةٍ في النواة"
)

DESIGN_SOURCE_CITATION_NOTE: Final = (
    "شكلُ «المُعلَن مقابل المُشتَقّ» مأخوذٌ من سؤال التدقيق المفتوح "
    f"`{DESIGN_SOURCE_OPEN_QUESTION}` بوصفه مصدرًا مباشرًا لا بديهةً تُعاد "
    "اشتقاقًا صامتًا؛ فالسؤال مرصودٌ غير مفسَّر، والبناءُ عليه بلا تسميته "
    "يُحوّله أساسًا مُسلَّمًا به بلا مرور بحكم"
)

PERFORMANCE_INDICATOR_IS_REFUSED_BY_SECTION_ONE_NOTE: Final = (
    "«مؤشر أداء» اسمٌ تمنعه §١: المؤشر الهندسيّ يُجيب «هل الشيفرة تعمل؟»، وهذا "
    "الدفتر يقرأ قناةَ الدلالة وحالَ الإفادة في استشهادٍ مكتوب، فلا يُقرَأ "
    "أداءً ولا سرعةَ إنجازٍ ولا نسبةَ تقدّم"
)

CHANNEL_IS_DERIVED_BY_A_SECOND_INDEPENDENT_READING_NOTE: Final = (
    "قناةُ الإشارة مُشتَقّةٌ من فهرسٍ يبنيه هذا القارئ بنفسه، لا منقولةٌ عن "
    "المرحلة السادسة؛ وإشارةٌ حُلَّت هناك ولم يبلغها الفهرسُ هنا تُرفَض ولا "
    "يُرجَّح أحدُ القارئين على الآخر"
)

UNRESOLVED_REFERENCE_HAS_NO_CHANNEL: Final = "UNRESOLVED_REFERENCE_HAS_NO_CHANNEL"

MANTUQ_COUNT_IS_NOT_PERFORMANCE: Final = "MANTUQ_COUNT_IS_NOT_PERFORMANCE"

IFADA_HERE_IS_READ_STATUS_NOT_LINGUISTIC_BENEFIT: Final = (
    "IFADA_HERE_IS_READ_STATUS_NOT_LINGUISTIC_BENEFIT"
)

MUKHALAFA_IS_UNREAD_IN_TODAYS_TRACE: Final = "MUKHALAFA_IS_UNREAD_IN_TODAYS_TRACE"

CHANNEL_READS_THE_CITATION_NOT_THE_MEASURED_ARABIC_SURFACE: Final = (
    "CHANNEL_READS_THE_CITATION_NOT_THE_MEASURED_ARABIC_SURFACE"
)

NAMED_RESIDUALS: Final[Mapping[str, str]] = MappingProxyType(
    {
        UNRESOLVED_REFERENCE_HAS_NO_CHANNEL: (
            "الإشارةُ المُستبعَدةُ بإعلانٍ لا تُحَلّ إلى مستند، فلا قناةَ لها "
            "تُقرَأ ولا قسمَ مفهومٍ يُكتَب. وحملُها على `منطوق` لأنها منطوقٌ بها "
            "في النصّ كان سيخلط «نُطِق به» بـ«دلّ بمنطوقه على مستند»، فتُترَك "
            "قناتُها غيابًا مُسمًّى وتُحصى مع ذلك في حال الإفادة `غير_مُفيد`"
        ),
        MANTUQ_COUNT_IS_NOT_PERFORMANCE: (
            "عددُ الإشارات المنطوق بها لغايةٍ ليس أداءً ولا مسافةً إلى بلوغها، "
            "ولا استشهادٌ كلُّه منطوقٌ أجودَ من استشهادٍ فيه مفهوم: القناتان "
            "موضعان للدلالة لا درجتان في سُلَّم. وهو شقيقُ "
            "`SUPPORT_COUNT_IS_NOT_PROGRESS` في المرحلة السادسة"
        ),
        IFADA_HERE_IS_READ_STATUS_NOT_LINGUISTIC_BENEFIT: (
            "«الإفادة» هنا بلوغُ الإشارةِ مستندًا ذا حالةٍ مُعلَنة، لا فائدةٌ "
            "لغويةٌ في تركيبٍ عربيّ. والاسمُ مستعارٌ من نصّ «الغرض من التركيب "
            "الإفادة»، والاستعارةُ اجتهادُ تسميةٍ لا نقلٌ عن المصدر، على منهج "
            "`classical_kernel_map`"
        ),
        MUKHALAFA_IS_UNREAD_IN_TODAYS_TRACE: (
            "`MafhumKind.مخالفة` عددُها صفرٌ في الأثر المقروء اليوم، والصفرُ "
            "**مُشتَقٌّ** بفحص كلّ إشارةٍ مفهومة لا مفترَضٌ بإسقاط العضو من "
            "المفردة. فكلُّ ما حُلَّ بغير لفظه اليوم يحمل لفظَه المنطوق في "
            "تمام مستنده، ولو ورد مستندٌ يُحَلّ بنفيٍ أو بمقابلةٍ لقُرئ مخالفةً"
        ),
        CHANNEL_READS_THE_CITATION_NOT_THE_MEASURED_ARABIC_SURFACE: (
            "المقروءُ هنا نثرُ استشهادٍ في وثيقتين، لا سطحٌ عربيٌّ مقيسٌ بإثباتٍ "
            "ومصدر على منهج `ObservationProvenance`. فلا يُقرَأ هذا الدفتر "
            "قياسًا لغويًّا ولا شاهدًا على تقسيم المنطوق والمفهوم في العربية، "
            "ولا يدخل أيّ تجربةِ ولادة"
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
    "progress",
    "share",
    "ratio",
    "rank",
    "closeness",
    "attainment",
    "performance",
)

_ROW_IDENTIFIER: Final = re.compile(r"^[A-Z][A-Za-z0-9]*(?:\.[A-Za-z0-9]+)+$")

_HEADING_LINE: Final = re.compile(r"^#{2,4}\s+(.+?)\s*$")

_STATUS_BEARING_KINDS: Final[frozenset[CitedSupportKind]] = frozenset(
    {CitedSupportKind.LAW_ROW, CitedSupportKind.AUDIT_QUESTION}
)


class DalalaIndicatorError(ValueError):
    """قراءةٌ مرفوضة؛ لا تُحمَل الإشارة على أقرب قناةٍ مقبولة."""


@dataclass(frozen=True, slots=True)
class SupportNameIndex:
    """فهرسُ أسماء المستندات، مقسومًا إلى ما يُنطَق بحروفه وما يُفهَم من غيره.

    القسمة شرطُ القراءة لا تحسينُها: الاسمُ الحاضر بحروفه مستندًا قائمًا منطوقٌ
    به، والاسمُ الذي لا يبلغ مستندَه إلا بما لم يُنطَق — معرّفُ صفٍّ يُغني عن
    تمام اسمه، أو صدرُ عنوانٍ يُغني عن تمامه — مفهومٌ منه. ولا يُدمَج الفهرسان:
    دمجُهما يُسقط الفارق الذي تقوم عليه هذه المرحلة كلُّها.
    """

    uttered_names: frozenset[str]
    understood_names: Mapping[str, str]

    def __post_init__(self) -> None:
        if not isinstance(self.uttered_names, frozenset):
            raise DalalaIndicatorError("فهرسُ المنطوق مجموعةٌ مجمَّدة")
        if not isinstance(self.understood_names, Mapping):
            raise DalalaIndicatorError("فهرسُ المفهوم مقابلةُ اسمٍ بتمامه")
        for name, full in self.understood_names.items():
            if not isinstance(name, str) or not isinstance(full, str):
                raise DalalaIndicatorError("كلُّ مدخلٍ في الفهرس نصٌّ")
            if name in self.uttered_names:
                raise DalalaIndicatorError(
                    f"اسمٌ في الفهرسين معًا: {name} — القناةُ عندئذٍ ترجيحٌ من "
                    "القارئ لا اشتقاقٌ من الأثر"
                )


@dataclass(frozen=True, slots=True)
class ReadDalalaReference:
    """إشارةٌ واحدة مقروءةً بقناتها وقسمِ مفهومها وحالِ إفادتها، بلا حكم."""

    aim_id: AimId
    reference_name: str
    citation_offset: int
    ifada: IfadaStanding
    channel: DalalaChannel | None = None
    mafhum_kind: MafhumKind | None = None
    understood_through: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.aim_id, AimId):
            raise DalalaIndicatorError("معرّف الغاية من مفردته المغلقة")
        if not isinstance(self.reference_name, str) or not self.reference_name.strip():
            raise DalalaIndicatorError("اسم الإشارة نصٌّ غير فارغ")
        if (
            not isinstance(self.citation_offset, int)
            or isinstance(self.citation_offset, bool)
            or self.citation_offset < 0
        ):
            raise DalalaIndicatorError("موضع الإشارة عددٌ غير سالب")
        if not isinstance(self.ifada, IfadaStanding):
            raise DalalaIndicatorError("حال الإفادة من مفردتها المغلقة")

        if self.channel is None:
            if self.mafhum_kind is not None or self.understood_through:
                raise DalalaIndicatorError(
                    "إشارةٌ بلا قناةٍ لا تحمل قسمَ مفهومٍ ولا طريقَ فهم — "
                    f"{UNRESOLVED_REFERENCE_HAS_NO_CHANNEL}"
                )
            if self.ifada is not IfadaStanding.غير_مُفيد:
                raise DalalaIndicatorError(
                    "الإشارةُ التي لا تبلغ مستندًا حالُها `غير_مُفيد` وحدها: "
                    "موجودةٌ في النصّ ولا تفيد"
                )
            return

        if not isinstance(self.channel, DalalaChannel):
            raise DalalaIndicatorError("قناة الدلالة من مفردتها المغلقة")
        if not isinstance(self.mafhum_kind, MafhumKind):
            raise DalalaIndicatorError("قسم المفهوم من مفردته المغلقة")

        if self.channel is DalalaChannel.منطوق:
            if self.mafhum_kind is not MafhumKind.لا_ينطبق:
                raise DalalaIndicatorError(
                    "قسمةُ الموافقة والمخالفة قسمةٌ داخل المفهوم وحده؛ وملؤها "
                    "على منطوقٍ يرفع قسمًا إلى مقام قسيمه"
                )
            if self.understood_through:
                raise DalalaIndicatorError(
                    "المنطوقُ بلغ مستنده بلفظه، فلا طريقَ فهمٍ يُكتَب له"
                )
        else:
            if self.mafhum_kind is MafhumKind.لا_ينطبق:
                raise DalalaIndicatorError(
                    "المفهومُ يلزمه قسمُه: موافقٌ لحكم منطوقه أم مخالفٌ له"
                )
            if not self.understood_through.strip():
                raise DalalaIndicatorError(
                    "المفهومُ يلزمه تسميةُ تمام ما فُهِم منه، فطريقُ الفهم " "مقروءٌ لا مُقدَّر"
                )

    @property
    def is_understood(self) -> bool:
        """هل بلغت الإشارةُ مستندَها بغير لفظها؟"""

        return self.channel is DalalaChannel.مفهوم


@dataclass(frozen=True, slots=True)
class DalalaReferenceCensus:
    """إحصاءُ الإشارات المقروءة، وكلُّ عضوٍ من كلّ مفردةٍ حاضرٌ ولو بصفر."""

    references: tuple[ReadDalalaReference, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.references, tuple) or not self.references:
            raise DalalaIndicatorError("إحصاء الإشارات مجموعةٌ غير فارغة")
        for reference in self.references:
            if not isinstance(reference, ReadDalalaReference):
                raise DalalaIndicatorError("كل عنصرٍ إشارةٌ مقروءة")

    @property
    def reference_count(self) -> int:
        """عدد الإشارات كلِّها، محسوبًا لا مكتوبًا."""

        return len(self.references)

    @property
    def channel_counts(self) -> Mapping[DalalaChannel, int]:
        """تعدادُ الإشارات بحسب قناتها، وكلُّ عضوٍ حاضرٌ ولو بصفر."""

        counts = dict.fromkeys(DalalaChannel, 0)
        for reference in self.references:
            if reference.channel is not None:
                counts[reference.channel] += 1
        return MappingProxyType(counts)

    @property
    def mafhum_kind_counts(self) -> Mapping[MafhumKind, int]:
        """تعدادُ الإشارات بحسب قسم مفهومها، وكلُّ عضوٍ حاضرٌ ولو بصفر."""

        counts = dict.fromkeys(MafhumKind, 0)
        for reference in self.references:
            if reference.mafhum_kind is not None:
                counts[reference.mafhum_kind] += 1
        return MappingProxyType(counts)

    @property
    def ifada_counts(self) -> Mapping[IfadaStanding, int]:
        """تعدادُ الإشارات بحسب حال إفادتها، وكلُّ عضوٍ حاضرٌ ولو بصفر."""

        counts = dict.fromkeys(IfadaStanding, 0)
        for reference in self.references:
            counts[reference.ifada] += 1
        return MappingProxyType(counts)

    @property
    def references_without_channel(self) -> tuple[ReadDalalaReference, ...]:
        """الإشاراتُ التي لا قناةَ لها، حاضرةً في الإحصاء لا مطويّة."""

        return tuple(
            reference for reference in self.references if reference.channel is None
        )


@dataclass(frozen=True, slots=True)
class DalalaIndicatorRow:
    """صفُّ غايةٍ واحدة: إشاراتُها مقروءةً بقنواتها، بلا حقل عددٍ ولا رتبة."""

    aim_id: AimId
    references: tuple[ReadDalalaReference, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.aim_id, AimId):
            raise DalalaIndicatorError("معرّف الغاية من مفردته المغلقة")
        if not isinstance(self.references, tuple) or not self.references:
            raise DalalaIndicatorError(
                f"استشهادُ {self.aim_id.value} بلا إشارةٍ مقروءة: صفٌّ فارغ "
                "يُقرَأ «لا مستند» وهو ادّعاءُ غيابٍ لم يُقرَأ"
            )
        previous_offset = -1
        for reference in self.references:
            if not isinstance(reference, ReadDalalaReference):
                raise DalalaIndicatorError("كل عنصرٍ إشارةٌ مقروءة")
            if reference.aim_id is not self.aim_id:
                raise DalalaIndicatorError(
                    "إشارةٌ من استشهاد غايةٍ أخرى لا تُحسَب لهذه: الربط يُشتَقّ "
                    "من نصّ الغاية نفسها"
                )
            if reference.citation_offset <= previous_offset:
                raise DalalaIndicatorError("ترتيب الإشارات ترتيبُ ورودها في الاستشهاد")
            previous_offset = reference.citation_offset

    @property
    def census(self) -> DalalaReferenceCensus:
        """إحصاءُ إشارات هذه الغاية وحدها."""

        return DalalaReferenceCensus(references=self.references)

    @property
    def uttered_support_count(self) -> int:
        """عدد الإشارات المنطوق بها، محسوبًا لا مكتوبًا، ولا يُقرَأ أداءً."""

        return self.census.channel_counts[DalalaChannel.منطوق]

    @property
    def understood_support_count(self) -> int:
        """عدد الإشارات المفهومة من غير لفظها، محسوبًا لا مكتوبًا."""

        return self.census.channel_counts[DalalaChannel.مفهوم]

    @property
    def ifada_standing(self) -> IfadaStanding:
        """حالُ إفادة الاستشهاد كلِّه، مُشتَقّةً من حال إشاراته لا مكتوبة.

        `مُفيد` إن بلغت إشارةٌ واحدة مستندًا ذا حالةٍ مُعلَنة، و`غير_مقروء` إن
        بلغت الإشاراتُ مستنداتٍ لا حالةَ لها، و`غير_مُفيد` إن لم تبلغ إشارةٌ
        منها مستندًا أصلًا. وهذه حالٌ لا درجةُ قربٍ من بلوغ الغاية.
        """

        standings = {reference.ifada for reference in self.references}
        if IfadaStanding.مُفيد in standings:
            return IfadaStanding.مُفيد
        if IfadaStanding.غير_مقروء in standings:
            return IfadaStanding.غير_مقروء
        return IfadaStanding.غير_مُفيد


@dataclass(frozen=True, slots=True)
class DalalaIndicatorLedger:
    """دفترُ القنوات: صفٌّ لكلّ غايةٍ بترتيب §٢، وإحصاءٌ لكلّ إشارةٍ قُرئت."""

    rows: tuple[DalalaIndicatorRow, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.rows, tuple):
            raise DalalaIndicatorError("دفتر القنوات مجموعةٌ من الصفوف")
        read_ids = tuple(row.aim_id for row in self.rows)
        if read_ids != tuple(AIM_RECORDS):
            raise DalalaIndicatorError(
                "الدفتر يحمل صفًّا لكل غايةٍ بترتيب ورودها في §٢: غايةٌ ساقطةٌ "
                "تُقرَأ «لا مستند لها» وهو ادّعاءُ غيابٍ لم يُقرَأ، وترتيبٌ "
                "مغاير يُقرَأ ترتيبَ أولويةٍ لا تملكه هذه الطبقة"
            )
        for row in self.rows:
            if not isinstance(row, DalalaIndicatorRow):
                raise DalalaIndicatorError("كل عنصرٍ صفُّ غايةٍ مقروء")

    @property
    def row_count(self) -> int:
        """عدد صفوف الدفتر، محسوبًا لا مكتوبًا."""

        return len(self.rows)

    @property
    def rows_by_aim(self) -> Mapping[AimId, DalalaIndicatorRow]:
        """صفوف الدفتر مُفهرَسةً بغاياتها، بلا ترجيحٍ بينها."""

        return MappingProxyType({row.aim_id: row for row in self.rows})

    @property
    def census(self) -> DalalaReferenceCensus:
        """إحصاءُ كلّ إشارةٍ في كلّ استشهاد، ذاتِ القناة وعديمتِها."""

        return DalalaReferenceCensus(
            references=tuple(
                reference for row in self.rows for reference in row.references
            )
        )

    @property
    def ifada_standing_counts(self) -> Mapping[IfadaStanding, int]:
        """تعدادُ الغايات بحسب حال إفادة استشهادها، وكلُّ عضوٍ حاضرٌ ولو بصفر."""

        counts = dict.fromkeys(IfadaStanding, 0)
        for row in self.rows:
            counts[row.ifada_standing] += 1
        return MappingProxyType(counts)


def _assert_no_fields_matching(
    declaring_type: type, markers: tuple[str, ...], message: str
) -> None:
    for item in fields(declaring_type):
        if any(marker in item.name for marker in markers):  # pragma: no cover - guard
            raise RuntimeError(message)


for _declaring_type in (
    SupportNameIndex,
    ReadDalalaReference,
    DalalaReferenceCensus,
    DalalaIndicatorRow,
    DalalaIndicatorLedger,
):
    _assert_no_fields_matching(
        _declaring_type,
        _ANSWER_BEARING_FIELD_MARKERS,
        "a dalala indicator type may not carry an answer, verdict, attainment, "
        "performance, progress, or ranking field",
    )


def build_support_name_index(
    ledger: ConstitutionLedger, document_text: str
) -> SupportNameIndex:
    """ابنِ فهرسَ الأسماء قراءةً ثانيةً مستقلّة: ما يُنطَق بحروفه وما يُفهَم."""

    if not isinstance(ledger, ConstitutionLedger):
        raise DalalaIndicatorError("دفتر الدستور من نوعه")
    if not isinstance(document_text, str) or not document_text.strip():
        raise DalalaIndicatorError("نصّ وثيقة الدستور نصٌّ غير فارغ")

    uttered: set[str] = set()
    understood: dict[str, str] = {}

    for row in ledger.laws.rows:
        name = row.law.strip("`")
        uttered.add(name)
        tokens = name.split()
        if len(tokens) > 1 and _ROW_IDENTIFIER.match(tokens[0]):
            understood.setdefault(tokens[0], name)

    for question in ledger.audit_questions.questions:
        uttered.add(question.name)

    for line in document_text.splitlines():
        match = _HEADING_LINE.match(line)
        if match is None:
            continue
        heading = match.group(1)
        uttered.add(heading)
        prefix = heading.split(" — ")[0].strip()
        if prefix and prefix != heading:
            understood.setdefault(prefix, heading)

    return SupportNameIndex(
        uttered_names=frozenset(uttered),
        understood_names=MappingProxyType(
            {name: full for name, full in understood.items() if name not in uttered}
        ),
    )


def _ifada_of(reference: ReadCitationReference) -> IfadaStanding:
    if not reference.is_resolved:
        return IfadaStanding.غير_مُفيد
    if reference.kind in _STATUS_BEARING_KINDS:
        return IfadaStanding.مُفيد
    return IfadaStanding.غير_مقروء


def read_dalala_reference(
    reference: ReadCitationReference,
    index: SupportNameIndex,
    repository_root: Path,
) -> ReadDalalaReference:
    """اقرأ قناةَ إشارةٍ واحدة وقسمَ مفهومها وحالَ إفادتها، والمجهولُ يُرفَض."""

    if not isinstance(reference, ReadCitationReference):
        raise DalalaIndicatorError("الإشارة مقروءةٌ من المرحلة السادسة")
    if not isinstance(index, SupportNameIndex):
        raise DalalaIndicatorError("فهرس الأسماء من نوعه")
    if not isinstance(repository_root, Path):
        raise DalalaIndicatorError("جذر الشجرة مسارٌ")

    ifada = _ifada_of(reference)
    if not reference.is_resolved:
        return ReadDalalaReference(
            aim_id=reference.aim_id,
            reference_name=reference.reference_name,
            citation_offset=reference.citation_offset,
            ifada=ifada,
        )

    name = reference.reference_name
    is_uttered = name in index.uttered_names
    if not is_uttered and reference.kind is CitedSupportKind.REPOSITORY_PATH:
        is_uttered = (repository_root / name).exists()

    if is_uttered:
        return ReadDalalaReference(
            aim_id=reference.aim_id,
            reference_name=name,
            citation_offset=reference.citation_offset,
            ifada=ifada,
            channel=DalalaChannel.منطوق,
            mafhum_kind=MafhumKind.لا_ينطبق,
        )

    full = index.understood_names.get(name)
    if full is None:
        raise DalalaIndicatorError(
            f"إشارةٌ في استشهاد {reference.aim_id.value} عند الحرف "
            f"{reference.citation_offset} حُلَّت في المرحلة السادسة ولم يبلغها "
            f"فهرسُ هذا القارئ: {name} — "
            f"{CHANNEL_IS_DERIVED_BY_A_SECOND_INDEPENDENT_READING_NOTE}"
        )

    return ReadDalalaReference(
        aim_id=reference.aim_id,
        reference_name=name,
        citation_offset=reference.citation_offset,
        ifada=ifada,
        channel=DalalaChannel.مفهوم,
        mafhum_kind=(MafhumKind.موافقة if name in full else MafhumKind.مخالفة),
        understood_through=full,
    )


def read_dalala_indicator_ledger(
    indicator: AimIndicatorLedger,
    index: SupportNameIndex,
    repository_root: Path,
) -> DalalaIndicatorLedger:
    """اقرأ قنواتِ كلّ غايةٍ من إشاراتها، صفًّا لكل غايةٍ بترتيب §٢."""

    if not isinstance(indicator, AimIndicatorLedger):
        raise DalalaIndicatorError("دفتر المرحلة السادسة من نوعه")
    return DalalaIndicatorLedger(
        rows=tuple(
            DalalaIndicatorRow(
                aim_id=row.aim_id,
                references=tuple(
                    read_dalala_reference(
                        reference=reference,
                        index=index,
                        repository_root=repository_root,
                    )
                    for reference in row.references
                ),
            )
            for row in indicator.rows
        )
    )


def load_dalala_indicator_ledger(path: Path | None = None) -> DalalaIndicatorLedger:
    """اقرأ الدفتر من وثيقة الدستور نفسها؛ وغيابُها رفضٌ مُسمّى لا دفترٌ فارغ."""

    document = constitution_document_path() if path is None else path
    if not isinstance(document, Path):
        raise DalalaIndicatorError("موضع الوثيقة مسارٌ")
    try:
        text = document.read_text(encoding="utf-8")
    except OSError as error:
        raise DalalaIndicatorError(
            f"تعذّرت قراءة وثيقة الدستور عند {document}: دفترٌ فارغ يُقرَأ «لا "
            "مستند لأيّ غاية» وهو ادّعاءُ غيابٍ لم تُقرَأ الوثيقة لأجله"
        ) from error

    ledger = load_constitution_ledger(document)
    root = repository_root_path()
    return read_dalala_indicator_ledger(
        indicator=read_aim_indicator_ledger(
            ledger=ledger, document_text=text, repository_root=root
        ),
        index=build_support_name_index(ledger, text),
        repository_root=root,
    )


__all__ = [
    "CHANNEL_IS_DERIVED_BY_A_SECOND_INDEPENDENT_READING_NOTE",
    "CHANNEL_READS_THE_CITATION_NOT_THE_MEASURED_ARABIC_SURFACE",
    "DALALA_INDICATOR_AUTHORITY_NOTE",
    "DESIGN_SOURCE_CITATION_NOTE",
    "IFADA_HERE_IS_READ_STATUS_NOT_LINGUISTIC_BENEFIT",
    "MANTUQ_COUNT_IS_NOT_PERFORMANCE",
    "MUKHALAFA_IS_UNREAD_IN_TODAYS_TRACE",
    "NAMED_RESIDUALS",
    "PERFORMANCE_INDICATOR_IS_REFUSED_BY_SECTION_ONE_NOTE",
    "UNRESOLVED_REFERENCE_HAS_NO_CHANNEL",
    "DalalaIndicatorError",
    "DalalaIndicatorLedger",
    "DalalaIndicatorRow",
    "DalalaReferenceCensus",
    "ReadDalalaReference",
    "SupportNameIndex",
    "build_support_name_index",
    "load_dalala_indicator_ledger",
    "read_dalala_indicator_ledger",
    "read_dalala_reference",
]
