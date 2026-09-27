"""المصادرُ المنهجيّة (T₃): تُنقَل نصًّا وتُسمّى أبوابُها، ولا تُحوَّل عدًّا.

في هذه الشجرة جنسان من الوارد كانا يُقرآن واحدًا وليسا واحدًا::

    AQuotedFigure          != AMethodologicalSource
    رقمٌ وارِدٌ يُصادَم أو  != تحديدٌ وتقسيمٌ وشرطٌ يُنقَل
    يُعلَن شاهدًا             ويُسمّى البابُ الذي يُطبِّقه

فالرقمُ الوارِدُ — كـ78,215 — له صورةٌ واحدةٌ تُقارَن، فإمّا وُلِّد عندنا
وإمّا أُعلِن شاهدًا لا يولَّد. وأمّا **المصدرُ المنهجيّ** فليس رقمًا ألبتّة:
هو كتابٌ يُؤخَذ عنه تحديدُ حدٍّ أو تقسيمُ بابٍ أو اشتراطُ شرط. فلا يُسأل عن
مولِّدٍ يولّده، لأنّه لا عددَ فيه ليولَّد؛ ويُسأل عن أمرين اثنين لا ثالثَ
لهما: **أمنقولٌ بنصّه؟** و**أيَّ بابٍ من أبواب الآلة يُطبِّقه؟**

**أوّلًا: لا يُحوَّل عدًّا.** أن يُقال «أربعةُ شروطٍ للعقل» فذلك تقسيمُ
المصدر نفسِه لا قياسٌ على مادّة؛ وأن يُؤخَذ هذا العددُ فيُدخَل في حسابٍ أو
يُعرَض مخرَجًا مقيسًا اختلاقُ قياسٍ لم يقع
(`A_METHODOLOGICAL_SOURCE_IS_CITED_NOT_COUNTED`). ولذلك لا تحمل هذه الوحدةُ
رقمًا واحدًا مقيسًا؛ وما فيها من أعدادٍ فأعدادُ بنودٍ **مشتقّةٌ من السجلّ
نفسِه** عند القراءة، لا منقولةٌ عن المصدر.

**وثانيًا: الحيُّ فيها موضعُ التطبيق لا القيمة.** فالختمُ الذي يحرس هذه
الوحدةَ لا يصادم رقمًا؛ إنّما يفتح ملفَّ كلِّ بابٍ مُعلَنٍ **نافذًا** ويسأل:
أفيه ذكرُ مصدرِه بنصّه؟ فإن سقط الذكرُ — بحذفٍ أو إعادةِ صياغة — انكشف حالًا.
فهذا مولِّدٌ حيٌّ بحقٍّ، وإن لم يكن مولِّدَ عدد
(`THE_LIVE_SIDE_OF_A_SOURCE_IS_ITS_CITATION_SITE_NOT_A_MAGNITUDE`).

**وثالثًا: البابُ المُعلَنُ غيرُ المنفَّذ يُسمّى ولا يُموَّه.** من الأبواب
الثلاثةِ المُعلَنة ههنا بابٌ واحدٌ نافذٌ في الشجرة — `wad_naql` — وبابان
مُعلَنان **لم يُنفَّذا بعدُ**: شروطُ العقل الأربعة، وأسبابُ الربط الاثنا عشر.
وهذان يُودَعان غيابًا مسمًّى بموضعه المرتقَب، لا يُكتَبان كأنّهما قائمان، ولا
يُحذَفان كأنّهما لم يُطلَبا
(`AN_UNIMPLEMENTED_DOOR_IS_DEPOSITED_AS_A_NAMED_ABSENCE`).

**ورابعًا: ولا سلطانَ لهذه الوحدة على حكم.** لا تُرخّص ولادةً، ولا ترفع
حظرًا، ولا تُدخِل نصًّا مصدريًّا في قياس. وإنّما تُسجِّل: هذا المصدر، وهذا
موضعُ نقله، وهذه أبوابُه.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Final

__all__ = [
    "AN_UNIMPLEMENTED_DOOR_IS_DEPOSITED_AS_A_NAMED_ABSENCE",
    "A_SOURCE_HERE_CARRIES_NO_MEASURED_MAGNITUDE",
    "ApplicationDoor",
    "DoorStanding",
    "MethodologicalSource",
    "MethodologicalSourceError",
    "THE_METHODOLOGICAL_SOURCES",
    "THE_LIVE_SIDE_OF_A_SOURCE_IS_ITS_CITATION_SITE_NOT_A_MAGNITUDE",
    "citation_sites",
    "doors_by_standing",
    "missing_citations",
]


class MethodologicalSourceError(ValueError):
    """رفضٌ مُسمًّى في سجلّ المصادر المنهجيّة؛ لا يُبتلَع خللٌ ههنا صمتًا."""


class DoorStanding(Enum):
    """منزلةُ بابٍ من أبواب التطبيق: أنافذٌ في الشجرة أم مُعلَنٌ مرتقَب؟"""

    IN_FORCE = "نافذٌ في وحدةٍ قائمة"
    DECLARED_NOT_IMPLEMENTED = "مُعلَنٌ لم يُنفَّذ بعد"


@dataclass(frozen=True)
class ApplicationDoor:
    """بابٌ تُطبِّق فيه الآلةُ مصدرًا: اسمُه، ومنزلتُه، وموضعُه إن كان."""

    name: str
    standing: DoorStanding
    module: str | None

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise MethodologicalSourceError("بابٌ بلا اسمٍ لا يُسجَّل.")
        if self.standing is DoorStanding.IN_FORCE and not self.module:
            raise MethodologicalSourceError(
                "بابٌ يُعلَن نافذًا يلزمه موضعٌ يُفتَح ويُقرَأ؛ وإلّا فهو دعوى."
            )
        if self.standing is DoorStanding.DECLARED_NOT_IMPLEMENTED and self.module:
            raise MethodologicalSourceError(
                "بابٌ مُعلَنٌ غيرُ منفَّذٍ لا يُنسَب إلى وحدةٍ قائمة."
            )


@dataclass(frozen=True)
class MethodologicalSource:
    """مصدرٌ منهجيٌّ: عنوانُه ومؤلِّفُه وأجزاؤه المنقولة وأبوابُه."""

    title: str
    author: str
    parts: tuple[str, ...]
    what_is_taken: str
    doors: tuple[ApplicationDoor, ...]

    def __post_init__(self) -> None:
        for field_value, complaint in (
            (self.title, "مصدرٌ بلا عنوانٍ لا يُنقَل عنه."),
            (self.author, "مصدرٌ بلا مؤلِّفٍ لا يُنسَب."),
            (self.what_is_taken, "مصدرٌ لا يُسمّى المأخوذُ عنه نقلٌ مبهَم."),
        ):
            if not field_value.strip():
                raise MethodologicalSourceError(complaint)
        if not self.parts:
            raise MethodologicalSourceError("مصدرٌ بلا جزءٍ مُسمًّى لا يُراجَع.")
        if not self.doors:
            raise MethodologicalSourceError(
                "مصدرٌ بلا بابٍ تُطبِّقه الآلةُ سجلٌّ لا أثرَ له؛ ولا يُودَع."
            )
        names = [door.name for door in self.doors]
        if len(set(names)) != len(names):
            raise MethodologicalSourceError("بابٌ مكرَّرُ الاسم في مصدرٍ واحد.")

    @property
    def citation_marker(self) -> str:
        """النصُّ الذي يُبحَث عنه في وحدةِ كلِّ بابٍ نافذ؛ عنوانُه بحروفه."""

        return self.title


THE_METHODOLOGICAL_SOURCES: Final[tuple[MethodologicalSource, ...]] = (
    MethodologicalSource(
        title="الشخصية الإسلامية",
        author="تقي الدين النبهاني",
        parts=("الجزء الأول", "الجزء الثالث"),
        what_is_taken=(
            "تحديدُ الوضع وطريقِ معرفته، وشروطُ العقل، وتقسيماتُ أصول "
            "الدلالة — تُنقَل نصًّا ولا تُحوَّل عدًّا."
        ),
        doors=(
            ApplicationDoor(
                name="بابُ الوضع والنقل",
                standing=DoorStanding.IN_FORCE,
                module="alghanem.arabic.wad_naql",
            ),
            ApplicationDoor(
                name="شروطُ العقل الأربعة",
                standing=DoorStanding.DECLARED_NOT_IMPLEMENTED,
                module=None,
            ),
        ),
    ),
    MethodologicalSource(
        title="الجملة في القرآن الكريم",
        author="نقلٌ منهجيٌّ في بابِ الجملة",
        parts=("المجلَّد المنقولُ عنه بطاقةُ الجملة",),
        what_is_taken=(
            "تقسيمُ الجملة وأسبابُ الربط بين أجزائها — تُنقَل نصًّا ولا "
            "تُحوَّل عدًّا."
        ),
        doors=(
            ApplicationDoor(
                name="أسبابُ الربط الاثنا عشر",
                standing=DoorStanding.DECLARED_NOT_IMPLEMENTED,
                module=None,
            ),
        ),
    ),
)


def _module_path(dotted: str) -> Path:
    """موضعُ وحدةٍ على القرص من اسمها المنقوط، ولا يُستورَد ما يُقرَأ."""

    tail = dotted.split(".")[-1]
    path = Path(__file__).resolve().parent / f"{tail}.py"
    if not path.is_file():
        raise MethodologicalSourceError(f"بابٌ يُعلَن نافذًا وموضعُه غائب: {dotted}")
    return path


def citation_sites() -> tuple[tuple[str, str], ...]:
    """كلُّ بابٍ نافذٍ مقرونًا بعنوان مصدره؛ وهذان جانبا الفحص الحيّ."""

    return tuple(
        (door.module, source.citation_marker)
        for source in THE_METHODOLOGICAL_SOURCES
        for door in source.doors
        if door.standing is DoorStanding.IN_FORCE and door.module is not None
    )


def missing_citations() -> tuple[str, ...]:
    """الأبوابُ النافذةُ التي سقط من نصّها ذكرُ مصدرها؛ تُسمّى ولا تُخفى."""

    absent: list[str] = []
    for dotted, marker in citation_sites():
        if marker not in _module_path(dotted).read_text(encoding="utf-8"):
            absent.append(dotted)
    return tuple(absent)


def doors_by_standing() -> dict[DoorStanding, tuple[str, ...]]:
    """أبوابُ التطبيقِ مفروزةً بمنزلتها، مُشتقّةً من السجلّ لا منقولةً عنه."""

    fold: dict[DoorStanding, list[str]] = {standing: [] for standing in DoorStanding}
    for source in THE_METHODOLOGICAL_SOURCES:
        for door in source.doors:
            fold[door.standing].append(door.name)
    return {standing: tuple(names) for standing, names in fold.items()}


A_SOURCE_HERE_CARRIES_NO_MEASURED_MAGNITUDE: Final[str] = (
    "A_SOURCE_HERE_CARRIES_NO_MEASURED_MAGNITUDE: المصدرُ المنهجيُّ ليس "
    "رقمًا؛ فلا يُسأل عن مولِّدٍ يولّده، ولا يُعرَض مخرَجًا مقيسًا."
)

THE_LIVE_SIDE_OF_A_SOURCE_IS_ITS_CITATION_SITE_NOT_A_MAGNITUDE: Final[str] = (
    "THE_LIVE_SIDE_OF_A_SOURCE_IS_ITS_CITATION_SITE_NOT_A_MAGNITUDE: الجانبُ "
    "الحيُّ لمصدرٍ منهجيٍّ حضورُ ذكره في وحدةِ بابه؛ فإن سقط انكشف."
)

AN_UNIMPLEMENTED_DOOR_IS_DEPOSITED_AS_A_NAMED_ABSENCE: Final[str] = (
    "AN_UNIMPLEMENTED_DOOR_IS_DEPOSITED_AS_A_NAMED_ABSENCE: بابٌ مُعلَنٌ لم "
    "يُنفَّذ يُودَع غيابًا مسمًّى، لا يُكتَب قائمًا ولا يُحذَف مطلوبًا."
)


def _assert_no_magnitude_is_deposited_here() -> None:
    """حارسٌ بنيويّ: لا يحمل بندٌ ههنا حقلًا عدديًّا يُقرأ قياسًا."""

    for source in THE_METHODOLOGICAL_SOURCES:
        for door in source.doors:
            if isinstance(door.module, int | float):
                raise MethodologicalSourceError(
                    A_SOURCE_HERE_CARRIES_NO_MEASURED_MAGNITUDE
                )


def _assert_every_in_force_door_has_a_readable_site() -> None:
    """حارسٌ بنيويّ: كلُّ بابٍ نافذٍ موضعُه مقروءٌ على القرص الآن."""

    for dotted, _ in citation_sites():
        _module_path(dotted)


_assert_no_magnitude_is_deposited_here()
_assert_every_in_force_door_has_a_readable_site()
