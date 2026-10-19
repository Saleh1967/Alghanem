"""مجرّد/مزيد: عدُّ خاناتٍ ومطابقةُ هيكلٍ كامل على جدول الجذور المُبصَّم.

المعيارُ وحدُّه الدائمُ مُجمَّدان قبل هذه الوحدة في
`jarad_mazid_preregistration`، وتُطابَق بصمتُهما عند الاستيراد.

`THE_ROOT_TABLE_IS_DIGEST_CHECKED_ON_EVERY_READ`: كلُّ قراءةٍ لجدول الجذور تمرّ
بـ`maqayis_root_table_deposit.root_table_rows`، وهي تتحقّق من طول البايتات
وبصمتِها وترويستِها قبل أن تُخرِج صفًّا واحدًا؛ فلا تُقرأ نسخةٌ أخرى بصمت.

`MATCHING_IS_ON_THE_FULL_SKELETON_NEVER_ON_A_PREFIX`: لا مطابقةَ بادئةٍ هنا
بحال. والمطابقةُ صنفان مُسمّيان — تطابقُ الهيكل كلِّه، ووقوعُ حروف الجذر
بترتيبها داخل الهيكل — ولا يُدمَجان في «مطابقة» واحدة، ولا تُرجَّح إحداهما
على الأخرى في هذه الوحدة.

`NO_CORPUS_FIGURE_IS_ISSUED_HERE`: هذه أداةٌ على كلمةٍ واحدة. ولا تُصدِر عددًا
على مدوّنة، ولا تتبنّى الأعدادَ الأربعةَ المُودَعة: شروطُ إصدارها الأربعةُ
مكتوبةٌ في التسجيل القبْليّ، وليس واحدٌ منها متحقّقًا في هذه الجلسة.

`LENGTH_ONLY_NEVER_THE_IDENTITY_OF_THE_WEAK_LETTER`: ما يخرج من هنا عددُ
خاناتٍ ومطابقاتٌ مُسمّاة؛ ولا يخرج منه أنّ حرفًا بعينه أصليٌّ أو زائد.

`THIS_IS_A_READING_NOT_A_BIRTH`: لا ولادةَ هنا، ولا حكم، ولا تجميدَ `E0`، ولا
استيرادَ من `kernel/`، ولا يُرفَع بها حجبُ طبقة `JARAD_ANALYSIS`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Final

from .encoding.carrier_state_candidate import CarrierSeat, CarrierState
from .jarad_mazid_preregistration import (
    MAZID_MINIMUM_SLOTS,
    MUJARRAD_SLOT_COUNT,
    PREREGISTRATION_DIGEST,
)
from .maqayis_root_table_deposit import root_table_rows
from .p_extractor import LetterReading, PExtractorReading, PhoneticRole, read_surface

__all__ = [
    "JARAD_MAZID_NAMED_RESIDUALS",
    "LENGTH_ONLY_NEVER_THE_IDENTITY_OF_THE_WEAK_LETTER_NOTE",
    "MATCHING_IS_ON_THE_FULL_SKELETON_NEVER_ON_A_PREFIX_NOTE",
    "NO_CORPUS_FIGURE_IS_ISSUED_HERE_NOTE",
    "THE_ROOT_TABLE_IS_DIGEST_CHECKED_ON_EVERY_READ_NOTE",
    "THIS_IS_A_READING_NOT_A_BIRTH_NOTE",
    "JaradMazidError",
    "JaradMazidReading",
    "RootMatch",
    "RootMatchKind",
    "SlotCount",
    "consonant_skeleton",
    "classify_slot_count",
    "match_roots",
    "read_jarad_mazid",
    "root_skeletons",
]


class JaradMazidError(ValueError):
    """رفضٌ عند القراءة: هيكلٌ فارغ، أو قراءةٌ ببصمةِ تسجيلٍ أخرى."""


class SlotCount(Enum):
    """قراءةُ عدد الخانات. ثلاثةٌ مغلقة، وفيها رفضٌ مُسمًّى لا قيمةٌ خالية."""

    MUJARRAD = "ثلاثُ خاناتٍ: مجرّد"
    MAZID = "أربعُ خاناتٍ فأكثر: مزيد"
    TOO_SHORT_TO_CLASSIFY = "أقلُّ من ثلاث خاناتٍ: لا يُصنَّف"


class RootMatchKind(Enum):
    """صنفا المطابقة، مُسمّيان ولا يُدمَجان؛ وليس فيهما مطابقةُ بادئة."""

    EXACT_SKELETON = "الهيكلُ كلُّه هو الجذرُ نفسُه"
    ORDERED_SUBSEQUENCE = "حروفُ الجذر واقعةٌ بترتيبها داخل الهيكل"


@dataclass(frozen=True, slots=True)
class RootMatch:
    """مطابقةٌ واحدةٌ بجذرها وصنفها؛ ولا تُرجَّح مطابقةٌ على أخرى هنا."""

    root: str
    kind: RootMatchKind

    def __post_init__(self) -> None:
        if not isinstance(self.root, str) or not self.root:
            raise JaradMazidError("الجذرُ نصٌّ غير فارغ")
        if not isinstance(self.kind, RootMatchKind):
            raise JaradMazidError("صنفُ المطابقة عضوٌ في مفردته المغلقة")


@dataclass(frozen=True, slots=True)
class JaradMazidReading:
    """قراءةُ كلمةٍ واحدة: هيكلُها، وعددُ خاناتها، ومطابقاتُها المُسمّاة."""

    surface: str
    skeleton: tuple[str, ...]
    slot_count: SlotCount
    matches: tuple[RootMatch, ...] = ()
    preregistration_digest: str = PREREGISTRATION_DIGEST

    def __post_init__(self) -> None:
        if not isinstance(self.surface, str):
            raise JaradMazidError("الصورةُ نصّ")
        if not isinstance(self.slot_count, SlotCount):
            raise JaradMazidError("عددُ الخانات مقروءٌ من مفردته المغلقة")
        if self.preregistration_digest != PREREGISTRATION_DIGEST:
            raise JaradMazidError("قراءةٌ ببصمةِ تسجيلٍ غيرِ القائمة قراءةٌ بمعيارٍ آخر")

    @property
    def slots(self) -> int:
        """عددُ الخانات عددًا، مُشتقًّا من الهيكل لا مُخزَّنًا معه."""

        return len(self.skeleton)

    @property
    def exact_matches(self) -> tuple[RootMatch, ...]:
        """المطابقاتُ التي الهيكلُ فيها هو الجذرُ نفسُه، مُشتقّةً عند السؤال."""

        return tuple(
            match
            for match in self.matches
            if match.kind is RootMatchKind.EXACT_SKELETON
        )


_ALEF: Final[str] = "\u0627"
_SHORT_VOWELS: Final[frozenset[CarrierState]] = frozenset(
    {CarrierState.FATHA, CarrierState.DAMMA, CarrierState.KASRA}
)


def _is_dropped(letter: LetterReading) -> bool:
    """أتسقط هذه الوحدةُ من الهيكل: ساكتةٌ، أو مَقعدُ تنوينٍ، أو حرفٌ مُمرَّر؟"""

    unit = letter.unit
    if unit.state is CarrierState.PASSTHROUGH or unit.silent:
        return True
    if letter.has_role(PhoneticRole.SILENT_DIFFERENTIATING_ALIF):
        return True
    return (
        letter.has_role(PhoneticRole.TANWEEN_ALIF_CARRIER)
        and unit.carrier == _ALEF
        and unit.state is CarrierState.SUKUN_IMPLICIT
    )


def consonant_skeleton(reading: PExtractorReading) -> tuple[str, ...]:
    """الهيكلُ الساكن: صامتٌ حقيقيٌّ أو حرفُ مدٍّ لكلّ خانة، بترتيب الصورة.

    والمدُّ خانةٌ بنصّ المعيار المُصحَّح، لا حرفًا يُسقَط؛ وهذا عينُ ما تقول
    المواصفةُ إنّ تصحيحَها صحّحه.
    """

    skeleton: list[str] = []
    for letter in reading.letters:
        if _is_dropped(letter):
            continue
        skeleton.append(letter.unit.carrier)
        if letter.unit.seat is CarrierSeat.MADD:
            skeleton.append(_ALEF)
    return tuple(skeleton)


def classify_slot_count(skeleton: tuple[str, ...]) -> SlotCount:
    """اقرأ عددَ الخانات بالحدّ المُجمَّد؛ وما قصُر عنه يُسمّى ولا يُقرَّب."""

    if len(skeleton) == MUJARRAD_SLOT_COUNT:
        return SlotCount.MUJARRAD
    if len(skeleton) >= MAZID_MINIMUM_SLOTS:
        return SlotCount.MAZID
    return SlotCount.TOO_SHORT_TO_CLASSIFY


def root_skeletons(root: Path | None = None) -> tuple[tuple[str, ...], ...]:
    """هياكلُ الجذور من الملفّ المُبصَّم، متمايزةً ومرتّبةً؛ والبصمةُ مفحوصةٌ قبلها."""

    seen = {row["root_full"] for row in root_table_rows(root)}
    return tuple(sorted(tuple(value) for value in seen if value))


def _is_ordered_subsequence(needle: tuple[str, ...], haystack: tuple[str, ...]) -> bool:
    position = 0
    for letter in haystack:
        if position < len(needle) and letter == needle[position]:
            position += 1
    return position == len(needle)


def match_roots(
    skeleton: tuple[str, ...],
    roots: tuple[tuple[str, ...], ...] | None = None,
    root: Path | None = None,
) -> tuple[RootMatch, ...]:
    """طابِق الهيكلَ الكاملَ على الجذور؛ ولا مطابقةَ بادئةٍ في هذه الدالّة.

    وتُقبَل الجذورُ مُمرَّرةً للمُنادي الذي قرأها مرّةً واحدةً بفحص بصمتها،
    فلا يُعاد فحصُ البصمة لكلّ كلمةٍ في مسارٍ طويل؛ وتُقرأ عند الغياب.
    """

    if not skeleton:
        raise JaradMazidError("لا مطابقةَ لهيكلٍ فارغ؛ والفراغُ يُسمّى ولا يُطابَق")
    table = root_skeletons(root) if roots is None else roots
    matches: list[RootMatch] = []
    for candidate in table:
        if candidate == skeleton:
            matches.append(
                RootMatch(root="".join(candidate), kind=RootMatchKind.EXACT_SKELETON)
            )
        elif len(candidate) < len(skeleton) and _is_ordered_subsequence(
            candidate, skeleton
        ):
            matches.append(
                RootMatch(
                    root="".join(candidate), kind=RootMatchKind.ORDERED_SUBSEQUENCE
                )
            )
    return tuple(matches)


def read_jarad_mazid(
    surface: str,
    roots: tuple[tuple[str, ...], ...] | None = None,
    root: Path | None = None,
) -> JaradMazidReading:
    """اقرأ كلمةً واحدة: هيكلُها، وعددُ خاناتها، ومطابقاتُها على الجدول المُبصَّم."""

    reading = read_surface(surface)
    skeleton = consonant_skeleton(reading)
    slot_count = classify_slot_count(skeleton)
    matches = match_roots(skeleton, roots=roots, root=root) if skeleton else ()
    return JaradMazidReading(
        surface=surface,
        skeleton=skeleton,
        slot_count=slot_count,
        matches=matches,
    )


LENGTH_ONLY_NEVER_THE_IDENTITY_OF_THE_WEAK_LETTER_NOTE: Final[str] = (
    "LengthOnlyNeverTheIdentityOfTheWeakLetter: يخرج من هنا عددُ خاناتٍ "
    "ومطابقاتٌ مُسمّاة، ولا يخرج أنّ حرفًا بعينه أصليٌّ أو زائد"
)

MATCHING_IS_ON_THE_FULL_SKELETON_NEVER_ON_A_PREFIX_NOTE: Final[str] = (
    "MatchingIsOnTheFullSkeletonNeverOnAPrefix: صنفا المطابقة مُسمّيان "
    "منفصلان، وليس فيهما مطابقةُ بادئةٍ ولا تُرجَّح إحداهما هنا"
)

NO_CORPUS_FIGURE_IS_ISSUED_HERE_NOTE: Final[str] = (
    "NoCorpusFigureIsIssuedHere: أداةٌ على كلمةٍ واحدة؛ ولا عددَ مدوّنةٍ "
    "يُصدَر بها، ولا تُتبنّى الأعدادُ الأربعةُ المُودَعة"
)

THE_ROOT_TABLE_IS_DIGEST_CHECKED_ON_EVERY_READ_NOTE: Final[str] = (
    "TheRootTableIsDigestCheckedOnEveryRead: كلُّ قراءةٍ للجدول تتحقّق من "
    "الطول والبصمة والترويسة قبل أن تُخرِج صفًّا"
)

THIS_IS_A_READING_NOT_A_BIRTH_NOTE: Final[str] = (
    "ThisIsAReadingNotABirth: لا حكمَ ولا ولادةَ ولا رفعَ حجبٍ عن طبقة "
    "`JARAD_ANALYSIS` بهذه الأداة"
)

JARAD_MAZID_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    LENGTH_ONLY_NEVER_THE_IDENTITY_OF_THE_WEAK_LETTER_NOTE,
    MATCHING_IS_ON_THE_FULL_SKELETON_NEVER_ON_A_PREFIX_NOTE,
    NO_CORPUS_FIGURE_IS_ISSUED_HERE_NOTE,
    THE_ROOT_TABLE_IS_DIGEST_CHECKED_ON_EVERY_READ_NOTE,
    THIS_IS_A_READING_NOT_A_BIRTH_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة، مرتّبةً كما تُرتَّب في بقيّة الطبقة."""
