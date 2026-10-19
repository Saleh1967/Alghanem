"""سجلُّ الوسم المرجعيّ: موضعٌ يُحَلّ، ووسمٌ تكتبه جهةٌ مُسمّاةٌ لا صاحبُ الدعوى.

**شهادةُ ورودِ اللفظ ليست شهادةَ صحّةِ تفسيره.** قد يُثبَت أنّ «عين» وقعت في
موضعٍ مُحدَّدٍ من مدوّنةٍ مُبصَّمة، ولا يُثبِت ذلك جنسَها ولا محمولَها ولا مضمونَ
إفادتها؛ فتعيينُ ذلك وسمٌ يحتاج **جهةً** تُسمّى وتُقارَن بمُعلِن المجال
(`AN_OCCURRENCE_CITATION_IS_NOT_A_READING_CERTIFICATE`).

ولذلك تحمل هذه الوحدةُ ثلاثةَ أشياءَ لا غير:

* **نحوُ محدِّد الموضع**: رقمُ سطرٍ يبدأ من واحد، ثمّ مجالٌ نصفُ مفتوحٍ
  `[start, end)` بوحدات نقاط Unicode بعد التسوية المُعلَنة. و`word_number`
  حقلٌ **للقراءة البشريّة وحدَها** لا يُحَلّ به موضع، فلا يكون مرجعًا بديلًا
  غامضًا (`A_WORD_NUMBER_IS_FOR_READING_NOT_FOR_RESOLUTION`).
* **حلُّ الموضع في مصدرٍ مُسجَّل**: يُقرأ نصُّ المصدر من الشجرة، ويُسوّى،
  ويُقتطَع المجال؛ ومحدِّدٌ خارجَ حدود السطر **لا يُحَلّ**، ولا يُقرأ عدمُ
  الحلّ مطابقةً.
* **قارئُ سجلّ الوسم**: يقرأ بايتاتِ ملفٍّ مبصَّمٍ مفصولٍ عن الشفرة، ويردّ كلَّ
  حقلٍ لا يعرفه رأسًا، ويُلزِم بتسمية الجهة الواسمة وبيانها وإصدارها.

**وفصلُ الملفّ عن الشفرة لا يُثبت استقلالَ الجهة.** إنّما يجعلها مكتوبةً
تُقارَن؛ والمقارنةُ نفسُها في `minimal_complete_fiber`، إذ هناك يُعرَف مُعلِنُ
المجال (`SEPARATING_THE_FILE_DOES_NOT_MAKE_THE_AUTHORITY_INDEPENDENT`).

ولا سلطةَ لهذه الوحدة: لا ولادةَ، ولا حكمَ ولادة، ولا تجميدَ، ولا استيرادَ من
`kernel/`.
"""

from __future__ import annotations

import hashlib
import json
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, Literal

from .fatiha_source_text import FATIHA_SOURCE_ID, FATIHA_SOURCE_TEXT

__all__ = [
    "AN_OCCURRENCE_CITATION_IS_NOT_A_READING_CERTIFICATE_NOTE",
    "A_SELF_AUTHORED_GLOSS_IS_NOT_INDEPENDENT_EVIDENCE_NOTE",
    "A_WORD_NUMBER_IS_FOR_READING_NOT_FOR_RESOLUTION_NOTE",
    "DEPOSITED_GLOSS_REGISTRY_SHA256",
    "GLOSS_DATA_DIRECTORY",
    "GLOSS_REGISTRY_NAMED_RESIDUALS",
    "GLOSS_REGISTRY_RELATIVE_PATH",
    "NORMALIZATION_FORM",
    "SANCTIONED_GLOSS_DATA_FILENAMES",
    "SEPARATING_THE_FILE_DOES_NOT_MAKE_THE_AUTHORITY_INDEPENDENT_NOTE",
    "GlossEntry",
    "GlossRegistry",
    "GlossRegistryError",
    "SourceLocator",
    "an_empty_registry",
    "gloss_data_directory_path",
    "gloss_registry_path",
    "in_tree_gloss_registry",
    "normalize",
    "read_gloss_registry",
    "registered_source_text",
    "registered_source_ids",
    "resolve_locator",
    "unsanctioned_gloss_data_files",
]


class GlossRegistryError(ValueError):
    """رفضٌ صريح: محدِّدٌ غيرُ سويٍّ، أو سجلٌّ بحقلٍ لا يعرفه القارئ."""


NORMALIZATION_FORM: Final[Literal["NFC"]] = "NFC"
"""التسويةُ المُعلَنة؛ وعليها تُعَدّ نقاطُ الشفرة في محدِّد الموضع."""


def normalize(text: str) -> str:
    """النصُّ مُسوًّى بالصورة المُعلَنة؛ ولا تُعَدّ نقطةٌ قبل تسويتها."""

    return unicodedata.normalize(NORMALIZATION_FORM, text)


_REPOSITORY_ROOT: Final[Path] = Path(__file__).resolve().parents[3]

GLOSS_DATA_DIRECTORY: Final[str] = "gloss_data"
"""مجلَّدُ سجلّ الوسم؛ مفصولٌ عن الشفرة وعن مجلَّد المدوّنات."""

GLOSS_REGISTRY_RELATIVE_PATH: Final[str] = "gloss_data/arabic_glosses_v1.json"
"""موضعُ بايتات السجلّ داخل الشجرة؛ موضعٌ مسنونٌ لا مُخمَّن."""

SANCTIONED_GLOSS_DATA_FILENAMES: Final[tuple[str, ...]] = (
    "README.md",
    "arabic_glosses_v1.json",
)
"""ما يجوز أن يسكن مجلَّد الوسم: بيانُه وسجلُّه، ولا ثالثَ لهما."""

DEPOSITED_GLOSS_REGISTRY_SHA256: Final[str] = (
    "6ab6646267acc23fece138b7a13aef45f279c6adb50e7a533d74cfaa2fba685e"
)
"""بصمةُ البايتات المُودَعة؛ تُعاد حوسبتُها عند كلّ قراءةٍ وتُقابَل بها.

وهي فحصُ سلامةٍ لا فحصُ سلطة: تمنع أن تتبدّل بايتاتُ السجلّ في الشجرة بلا
إيداعٍ جديد، ولا تجعل كاتبَ السجلّ جهةً مستقلّة.
"""


def gloss_data_directory_path() -> Path:
    """مسارُ مجلَّد الوسم، محسوبًا من موضع هذه الوحدة لا من `cwd`."""

    return _REPOSITORY_ROOT / GLOSS_DATA_DIRECTORY


def gloss_registry_path() -> Path:
    """مسارُ بايتات السجلّ داخل الشجرة."""

    return _REPOSITORY_ROOT / GLOSS_REGISTRY_RELATIVE_PATH


def unsanctioned_gloss_data_files(
    directory: Path | str | None = None,
) -> tuple[Path, ...]:
    """الملفّاتُ الساكنةُ في مجلَّد الوسم بلا إذن، مرتَّبةً بأسمائها."""

    place = Path(directory) if directory is not None else gloss_data_directory_path()
    if not place.is_dir():
        return ()
    return tuple(
        sorted(
            item
            for item in place.iterdir()
            if item.is_file() and item.name not in SANCTIONED_GLOSS_DATA_FILENAMES
        )
    )


# --- المصادرُ المُسجَّلةُ ونصوصُها ------------------------------------------------


def registered_source_text(source_id: str) -> str | None:
    """نصُّ مصدرٍ مُسجَّلٍ في الشجرة مُسوًّى، أو `None` إن لم يكن مُسجَّلًا.

    فالمصدرُ لا يُصدَّق باسمه: ما ليس في هذه المقابلة فليس مصدرًا في هذه الشجرة.
    """

    if source_id == FATIHA_SOURCE_ID:
        return normalize(FATIHA_SOURCE_TEXT)
    return None


def registered_source_ids() -> tuple[str, ...]:
    """أسماءُ المصادر المُسجَّلة، مرتَّبةً."""

    return (FATIHA_SOURCE_ID,)


# --- محدِّدُ الموضع ------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class SourceLocator:
    """موضعٌ في مصدرٍ مُسجَّل: سطرٌ، ثمّ مجالٌ نصفُ مفتوحٍ بنقاط الشفرة.

    و`word_number` **للقراءة البشريّة وحدَها**: لا يُحَلّ به موضعٌ ولا يُقابَل
    به وقوع، فلا يصير مرجعًا بديلًا غامضًا
    (`A_WORD_NUMBER_IS_FOR_READING_NOT_FOR_RESOLUTION`).
    """

    line: int
    start: int
    end: int
    word_number: int | None = None

    def __post_init__(self) -> None:
        if self.line < 1:
            raise GlossRegistryError("سطرٌ يبدأ من واحدٍ؛ وما دونه ليس موضعًا")
        if self.start < 0:
            raise GlossRegistryError("بدايةٌ سالبةٌ ليست موضعًا في نصّ")
        if self.end <= self.start:
            raise GlossRegistryError(
                "مجالٌ نصفُ مفتوحٍ يلزمه `start < end`؛ والخالي لا يُقابَل بوقوع"
            )
        if self.word_number is not None and self.word_number < 1:
            raise GlossRegistryError("رقمُ كلمةٍ يبدأ من واحدٍ أو لا يُكتَب")

    @property
    def rendered(self) -> str:
        """صورةٌ مقروءةٌ للموضع؛ ورقمُ الكلمة فيها بيانٌ لا مرجع."""

        word = "" if self.word_number is None else f"#w{self.word_number}"
        return f"L{self.line}:[{self.start},{self.end}){word}"


def resolve_locator(source_id: str, locator: SourceLocator) -> str | None:
    """السطحُ الواقعُ عند الموضع، أو `None` إن تعذّر الحلُّ.

    ولا يُقرأ تعذُّرُ الحلّ مطابقةً ولا مخالفة: هو **عدمُ حلٍّ** يُسمّى في
    الحكم، ويمنع رفعَ الحالة إلى موثَّقة.
    """

    text = registered_source_text(source_id)
    if text is None:
        return None
    lines = text.split("\n")
    if locator.line > len(lines):
        return None
    line = lines[locator.line - 1]
    if locator.end > len(line):
        return None
    return line[locator.start : locator.end]


# --- مداخلُ الوسم وسجلُّها ------------------------------------------------------


@dataclass(frozen=True, slots=True)
class GlossEntry:
    """وسمُ موضعٍ: جنسُه ومحمولُه ومضمونُ إفادته، منسوبًا إلى موضعٍ يُحَلّ."""

    source_id: str
    locator: SourceLocator
    genus: str
    predicate: str
    content: str

    def __post_init__(self) -> None:
        if not self.source_id.strip():
            raise GlossRegistryError("وسمٌ بلا مصدرٍ مُسمًّى لا يُراجَع")
        for value, name in (
            (self.genus, "جنس"),
            (self.predicate, "محمول"),
            (self.content, "مضمونُ إفادة"),
        ):
            if not value.strip():
                raise GlossRegistryError(f"وسمٌ بلا {name} مكتوبٍ لا يُقابَل بحالة")

    @property
    def resolved_surface(self) -> str | None:
        """سطحُ الموضع الموسوم، محلولًا الآن من نصّ المصدر لا محفوظًا مكتوبًا."""

        return resolve_locator(self.source_id, self.locator)


@dataclass(frozen=True, slots=True)
class GlossRegistry:
    """سجلُّ وسمٍ مقروءٌ: جهتُه وبيانُها وإصدارُها وبصمةُ بايتاته ومداخلُه."""

    registry_id: str
    authority_id: str
    authority_note: str
    version: str
    payload_sha256: str
    entries: tuple[GlossEntry, ...]

    def __post_init__(self) -> None:
        for value, name in (
            (self.registry_id, "اسم"),
            (self.authority_id, "جهةٌ واسمة"),
            (self.authority_note, "بيانُ جهة"),
            (self.version, "إصدار"),
        ):
            if not value.strip():
                raise GlossRegistryError(f"سجلُّ وسمٍ بلا {name} لا يُقرَأ سندًا")
        seen: set[tuple[str, int, int, int]] = set()
        for entry in self.entries:
            key = (
                entry.source_id,
                entry.locator.line,
                entry.locator.start,
                entry.locator.end,
            )
            if key in seen:
                raise GlossRegistryError(
                    "موضعٌ وُسِم مرّتين في سجلٍّ واحد؛ والتكرارُ يُخفي تعارضَ الوسم"
                )
            seen.add(key)

    @property
    def entry_count(self) -> int:
        """عددُ المداخل، مُشتقًّا بالعدّ."""

        return len(self.entries)

    def lookup(self, source_id: str, locator: SourceLocator) -> GlossEntry | None:
        """وسمُ هذا الموضع بعينه إن وُجد؛ ولا يُقابَل برقم الكلمة ولا بالجوار."""

        for entry in self.entries:
            if (
                entry.source_id == source_id
                and entry.locator.line == locator.line
                and entry.locator.start == locator.start
                and entry.locator.end == locator.end
            ):
                return entry
        return None


_REGISTRY_KEYS: Final[frozenset[str]] = frozenset(
    {
        "registry_id",
        "authority_id",
        "authority_note",
        "version",
        "normalization_form",
        "entries",
    }
)

_ENTRY_KEYS: Final[frozenset[str]] = frozenset(
    {
        "source_id",
        "line",
        "start",
        "end",
        "word_number",
        "genus",
        "predicate",
        "content",
    }
)

_REQUIRED_ENTRY_KEYS: Final[frozenset[str]] = _ENTRY_KEYS - {"word_number"}


def _require_exact_keys(
    payload: dict[str, Any],
    expected: frozenset[str],
    required: frozenset[str],
    what: str,
) -> None:
    keys = set(payload)
    unknown = sorted(keys - expected)
    if unknown:
        raise GlossRegistryError(
            f"{what}: حقلٌ لا يعرفه القارئ «{unknown[0]}»؛ وما لا يُعرَف لا يُتجاوَز"
        )
    missing = sorted(required - keys)
    if missing:
        raise GlossRegistryError(f"{what}: حقلٌ لازمٌ ناقص «{missing[0]}»")


def _require_str(payload: dict[str, Any], key: str, what: str) -> str:
    value = payload[key]
    if not isinstance(value, str):
        raise GlossRegistryError(f"{what}: «{key}» يُكتَب نصًّا")
    return value


def _require_int(payload: dict[str, Any], key: str, what: str) -> int:
    value = payload[key]
    if isinstance(value, bool) or not isinstance(value, int):
        raise GlossRegistryError(f"{what}: «{key}» يُكتَب عددًا صحيحًا")
    return int(value)


def read_gloss_registry(payload: bytes) -> GlossRegistry:
    """اقرأ سجلَّ وسمٍ من بايتاته، وردَّ كلَّ حقلٍ لا يعرفه القارئ.

    والبصمةُ محسوبةٌ ههنا من البايتات نفسِها، فلا تُكتَب في السجلّ فيُصدَّق
    باسمها.
    """

    digest = hashlib.sha256(payload).hexdigest()
    try:
        document = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise GlossRegistryError(f"سجلُّ وسمٍ لا يُقرَأ: {error}") from error
    if not isinstance(document, dict):
        raise GlossRegistryError("سجلُّ وسمٍ يُكتَب قاموسًا برأسٍ ومداخل")
    _require_exact_keys(document, _REGISTRY_KEYS, _REGISTRY_KEYS, "رأسُ السجلّ")

    form = _require_str(document, "normalization_form", "رأسُ السجلّ")
    if form != NORMALIZATION_FORM:
        raise GlossRegistryError(
            f"سجلٌّ بتسويةٍ «{form}» لا تُقابَل بمواضعَ عُدَّت على «{NORMALIZATION_FORM}»"
        )

    raw_entries = document["entries"]
    if not isinstance(raw_entries, list):
        raise GlossRegistryError("مداخلُ السجلّ تُكتَب قائمةً ولو خاليةً")

    entries: list[GlossEntry] = []
    for index, raw in enumerate(raw_entries, start=1):
        what = f"المدخلُ رقم {index}"
        if not isinstance(raw, dict):
            raise GlossRegistryError(f"{what}: يُكتَب قاموسًا")
        _require_exact_keys(raw, _ENTRY_KEYS, _REQUIRED_ENTRY_KEYS, what)
        word_number = raw.get("word_number")
        if word_number is not None and (
            isinstance(word_number, bool) or not isinstance(word_number, int)
        ):
            raise GlossRegistryError(f"{what}: «word_number» يُكتَب عددًا أو يُترَك")
        entries.append(
            GlossEntry(
                source_id=_require_str(raw, "source_id", what),
                locator=SourceLocator(
                    line=_require_int(raw, "line", what),
                    start=_require_int(raw, "start", what),
                    end=_require_int(raw, "end", what),
                    word_number=word_number,
                ),
                genus=_require_str(raw, "genus", what),
                predicate=_require_str(raw, "predicate", what),
                content=_require_str(raw, "content", what),
            )
        )

    return GlossRegistry(
        registry_id=_require_str(document, "registry_id", "رأسُ السجلّ"),
        authority_id=_require_str(document, "authority_id", "رأسُ السجلّ"),
        authority_note=_require_str(document, "authority_note", "رأسُ السجلّ"),
        version=_require_str(document, "version", "رأسُ السجلّ"),
        payload_sha256=digest,
        entries=tuple(entries),
    )


def an_empty_registry(authority_id: str = "لا-جهةَ-واسمةً-مُودَعة") -> GlossRegistry:
    """سجلٌّ خالٍ يُستعمَل حين لا تُقرَأ بايتاتٌ؛ وخلوُّه يُقرَأ عدمَ وسمٍ لا وسمًا."""

    return GlossRegistry(
        registry_id="سجلٌّ-غيرُ-مُودَع",
        authority_id=authority_id,
        authority_note="لا بايتاتِ سجلٍّ مقروءةً في هذه الشجرة الآن",
        version="بلا-إصدار",
        payload_sha256="0" * 64,
        entries=(),
    )


def in_tree_gloss_registry() -> GlossRegistry:
    """سجلُّ الوسم المُودَع في الشجرة، مقروءًا ببصمةٍ مُعادةِ الحوسبة.

    وغيابُ البايتات يُقرأ سجلًّا خاليًا لا استيفاءً؛ ومخالفةُ البصمة رفضٌ
    صريح، إذ بايتاتٌ لم تُودَع ليست السجلَّ المُودَع.
    """

    path = gloss_registry_path()
    if not path.is_file():
        return an_empty_registry()
    payload = path.read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    if digest != DEPOSITED_GLOSS_REGISTRY_SHA256:
        raise GlossRegistryError(
            "بايتاتُ سجلّ الوسم تخالف البصمةَ المُودَعة؛ وتبدُّلٌ بلا إيداعٍ لا يُقرَأ"
        )
    return read_gloss_registry(payload)


# --- البواقي المُسمّاة ----------------------------------------------------------


AN_OCCURRENCE_CITATION_IS_NOT_A_READING_CERTIFICATE_NOTE: Final[str] = (
    "AnOccurrenceCitationIsNotAReadingCertificate: إثباتُ وقوع اللفظ في موضعٍ "
    "مُبصَّمٍ يرفع تهمةَ الاختلاق في **الورود** وحدَه؛ ولا يُعيِّن جنسَه ولا "
    "محمولَه ولا مضمونَ إفادته، وتلك دعاوى وسمٍ تحتاج جهةً تُسمّى وتُقارَن"
)

A_SELF_AUTHORED_GLOSS_IS_NOT_INDEPENDENT_EVIDENCE_NOTE: Final[str] = (
    "ASelfAuthoredGlossIsNotIndependentEvidence: وسمٌ كتبه مُعلِنُ المجال على "
    "دعواه ليس دليلًا مستقلًّا عليها، وإن أُودِع في ملفٍّ منفصلٍ مبصَّم؛ "
    "والمقارنةُ على هويّة الجهة لا على موضع الملفّ"
)

SEPARATING_THE_FILE_DOES_NOT_MAKE_THE_AUTHORITY_INDEPENDENT_NOTE: Final[str] = (
    "SeparatingTheFileDoesNotMakeTheAuthorityIndependent: فصلُ سجلّ الوسم عن "
    "الشفرة وإبصامُه يمنعان التبدّلَ الصامت، ولا يُنشئان جهةً مستقلّة؛ فالسجلُّ "
    "يحمل هويّةَ جهته وإصدارَها لتُقارَن، وهذا كلُّ ما يفعله الفصل"
)

A_WORD_NUMBER_IS_FOR_READING_NOT_FOR_RESOLUTION_NOTE: Final[str] = (
    "AWordNumberIsForReadingNotForResolution: رقمُ الكلمة يُكتَب في المحدِّد "
    "ليقرأه إنسان، ولا يُحَلّ به موضعٌ ولا يُقابَل به وسمٌ بوقوع؛ فمرجعان "
    "أحدُهما غامضٌ ليسا مرجعين"
)

GLOSS_REGISTRY_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    AN_OCCURRENCE_CITATION_IS_NOT_A_READING_CERTIFICATE_NOTE,
    A_SELF_AUTHORED_GLOSS_IS_NOT_INDEPENDENT_EVIDENCE_NOTE,
    SEPARATING_THE_FILE_DOES_NOT_MAKE_THE_AUTHORITY_INDEPENDENT_NOTE,
    A_WORD_NUMBER_IS_FOR_READING_NOT_FOR_RESOLUTION_NOTE,
)
"""أربعُ بقايا مُسمّاةٍ تُقابَل بها أيُّ إحالةٍ إلى «سجلّ الوسم»."""
