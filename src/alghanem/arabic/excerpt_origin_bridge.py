"""جسرُ هُويّة المقتطف إلى مصدره: عنوانٌ لا يصير هويّةً إلّا بمصدرٍ مختوم.

وصل هذه الشجرةَ طلبُ تسليمِ شهادةٍ من التمثيل المعياريّ للوحدات المئةِ والستَّ
عشرةَ إلى **الكلمة في سياقها**، ومعه انقطاعٌ مُسمًّى: مقتطفٌ معرِّفُه `L329:W3`
وسطحُه «وَفِي الْفَرْقِ نَظَرٌ .»، لا يُعرَف من أيّ بايتاتٍ خرج.

وأوّلُ ما تُخرجه هذه الوحدةُ ليس جسرًا بل **قياسُ الانقطاع نفسِه**. فالمعرِّفُ
`L329:W3` ليس هويّةً أصلًا: إنّما هو إزاحةٌ في مصدرٍ لم يُسَمَّ. ويُقاس ذلك لا
يُوصَف — يُحَلُّ العنوانُ نفسُه في كلّ مصدرٍ مختومٍ في قائمة البحث، فيُخرج في
المودَعَين جميعًا كلمةً أخرى غيرَ «نَظَرٌ». فالعنوانُ الواحدُ يدلّ على مدلولاتٍ
عدّةٍ بعددِ المصادر، وهذه خاصّةُ الإزاحة لا خاصّةُ الهويّة
(`THE_ADDRESS_WITHOUT_A_SOURCE_IS_NOT_AN_IDENTITY`).

**والدعاوى ثلاثٌ تُفصَل ولا تُستنتَج إحداها من أختيها:**

| الدعوى | ما يُثبتها | ما لا يُثبتها |
|---|---|---|
| أ — العبارةُ موجودةٌ في مصدر | وجدانُها في بايتاتٍ مختومة | لا شيءَ عن منشأ المقتطف |
| ب — موضعُها متفرّدٌ في قائمة البحث | عدُّ مواضعها في القائمة المُعلَنة | لا شيءَ عن منشأ المقتطف |
| ج — هذا الموضعُ أصلُ المقتطف | شهادةُ منشأٍ مُسمّاةُ المنهج والمنفِّذ | «أ» و«ب» معًا لا تُنتجانها |

وتفرّدُ «ب» مقيَّدٌ بقائمته لا مطلقًا: فما كان متفرّدًا في مصدرٍ قد يقع مرّتين
في قائمةٍ من مصدرَين، والعددُ يتبدّل بتبدّل القائمة لا بتبدّل النصّ
(`UNIQUENESS_IS_RELATIVE_TO_A_DECLARED_SEARCH_LIST`).

**والفكُّ صارمٌ ههنا، وأثرُ المتسامح مقيسٌ لا مُجازٌ.** في
`tools/daleel/build_bab.py` يُفَكّ مصدرُ ذلك الباب بـ`errors="ignore"`، وهو
صالحٌ لمادّته لأنّها مفحوصةٌ بعينها؛ ولا يُعمَّم على مصدرٍ جديدٍ ههنا. فكلُّ
مصدرٍ في هذه الوحدة يُفَكّ بـ`errors="strict"`، ويُقاس في `DecodeAudit` ما كان
الفكُّ المتسامحُ **سيُسقطه** من بايتاتٍ ومحارف. وكونُ المقيس صفرًا على هذين
المودَعَين خبرٌ عنهما لا رخصةٌ لغيرهما
(`A_LENIENT_DECODE_IS_NEVER_GENERALISED_WITHOUT_A_MEASURED_RESIDUE`).

**ولا يُنقَل سياقٌ إلى مقتطفٍ مجهولِ المنشأ.** فمتى بقيت «ج» معلَّقةً امتنع
تسليمُ ما قبلَ الموضعِ وما بعده إلى ذلك المقتطف، لأنّ السياقَ خاصّةُ الموضع
المُثبَت لا خاصّةُ العبارة. وتجاورُ سطرَين في مجموعةِ بياناتٍ ليس دليلَ تجاورٍ
في الأصل ما لم يُودَع دليلُ ترتيبها
(`THE_ADJACENCY_OF_DATASET_LINES_IS_NOT_A_CONTINUOUS_CONTEXT`).

ولا تدّعي هذه الوحدةُ تحليلًا صرفيًّا ولا نحويًّا ولا معجميًّا: كلُّ ما تُخرجه
**موضعٌ وبايتاتُه وسياقُه ومنزلةُ دعاواه**. والتحليلُ وأحكامُه في
`word_certificate_chain`، ولا تُقرأ هذه الوحدةُ ترخيصًا له.
"""

from __future__ import annotations

import hashlib
import unicodedata
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Final

__all__ = [
    "A_LENIENT_DECODE_IS_NEVER_GENERALISED_WITHOUT_A_MEASURED_RESIDUE",
    "ClaimReading",
    "ClaimStanding",
    "DecodeAudit",
    "ExcerptOriginError",
    "LocatedWord",
    "OriginClaim",
    "OriginWitness",
    "PriorAuditMaterial",
    "SourceReading",
    "SourceStanding",
    "THE_ADDRESS_WITHOUT_A_SOURCE_IS_NOT_AN_IDENTITY",
    "THE_ADJACENCY_OF_DATASET_LINES_IS_NOT_A_CONTINUOUS_CONTEXT",
    "THE_PRIOR_AUDIT",
    "THE_SEARCH_LIST",
    "THE_THIRD_CLAIM_IS_NEVER_DERIVED_FROM_THE_FIRST_TWO",
    "TextSource",
    "UNIQUENESS_IS_RELATIVE_TO_A_DECLARED_SEARCH_LIST",
    "WordAddress",
    "address_collisions",
    "decode_audit",
    "locate",
    "origin_readings",
    "prior_audit_standing",
    "source_by_key",
    "source_reading",
    "source_text",
    "transferable_context",
]


class ExcerptOriginError(Exception):
    """خطأُ جسرِ المنشأ: يُرفَع ولا يُبتلَع، ويُسمّى سببُه في نصّه."""


THE_ADDRESS_WITHOUT_A_SOURCE_IS_NOT_AN_IDENTITY: Final[str] = (
    "عنوانُ سطرٍ وكلمةٍ بلا مصدرٍ مُسمًّى إزاحةٌ لا هويّة: يُحَلّ في كلّ مصدرٍ "
    "فيُخرج مدلولًا آخَر، فلا يُحتجّ به على عينِ كلمةٍ بعينها"
)

THE_THIRD_CLAIM_IS_NEVER_DERIVED_FROM_THE_FIRST_TWO: Final[str] = (
    "وجدانُ العبارة في مصدرٍ وتفرُّدُ موضعها فيه لا يُنتجان أنّ هذا الموضع أصلُ "
    "المقتطف: الأوّلان خبرٌ عن النصّ، والثالثة خبرٌ عن تاريخِ نقلٍ لا يُقرأ من "
    "النصّ، ولا تُثبَت إلّا بشهادةِ منشأٍ مُسمّاةِ المنهج والمنفِّذ"
)

UNIQUENESS_IS_RELATIVE_TO_A_DECLARED_SEARCH_LIST: Final[str] = (
    "التفرّدُ صفةُ موضعٍ في قائمةٍ مُعلَنة لا صفةُ عبارةٍ في نفسها: تتبدّل "
    "القائمةُ فيتبدّل العدد، ولم يتبدّل في النصّ حرفٌ واحد"
)

A_LENIENT_DECODE_IS_NEVER_GENERALISED_WITHOUT_A_MEASURED_RESIDUE: Final[str] = (
    "الفكُّ المتسامحُ يحذف أخطاءَ الترميز صامتًا، فلا يُنقَل من مادّةٍ فُحِصت "
    "إلى مادّةٍ جديدةٍ إلّا بسجلٍّ يُبيّن ما أسقطه ههنا بالعدد"
)

THE_ADJACENCY_OF_DATASET_LINES_IS_NOT_A_CONTINUOUS_CONTEXT: Final[str] = (
    "تجاورُ سطرَين في مجموعةِ بيانات ترتيبُ ملفٍّ لا ترتيبُ أصل: فلا يُقرأ "
    "أحدُهما سياقًا متّصلًا للآخَر ما لم يُودَع دليلُ ترتيبها في مصدرها"
)


# ----- المصدر: هُويّةٌ وإصدارٌ وختمٌ وسياسةُ استخراج -----


class SourceStanding(Enum):
    """منزلةُ مصدرٍ على القرص، مقيسةٌ عند كلّ قراءةٍ لا محفوظةٌ في حقل."""

    SEALED_AND_PRESENT = "مختومٌ حاضر"
    ABSENT_FROM_THIS_TREE = "غائبٌ عن هذه الشجرة"
    SEAL_BROKEN = "حاضرٌ مكسورُ الختم"

    @property
    def is_readable(self) -> bool:
        """لا يُقرأ نصٌّ إلّا من حاضرٍ سليمِ الختم؛ وما عداه يُرفَع به خطأ."""

        return self is SourceStanding.SEALED_AND_PRESENT


@dataclass(frozen=True, slots=True)
class TextSource:
    """مصدرٌ نصّيٌّ مُعلَنٌ: هويّةٌ وإصدارٌ وبصمةُ بايتاتٍ وسياساتُ استخراج."""

    key: str
    title: str
    edition: str
    relative_path: str
    declared_byte_length: int
    declared_sha256: str
    decode_policy: str
    normalization_policy: str
    line_policy: str

    def __post_init__(self) -> None:
        if not self.key.strip() or not self.title.strip():
            raise ExcerptOriginError("مصدرٌ بلا مفتاحٍ أو عنوانٍ لا يُسجَّل.")
        if not self.edition.strip():
            raise ExcerptOriginError(
                f"«{self.key}»: مصدرٌ بلا إصدارٍ مُسمًّى لا يُؤرَّخ فلا يُسجَّل."
            )
        if self.declared_byte_length <= 0:
            raise ExcerptOriginError(f"«{self.key}»: طولُ بايتاتٍ غيرُ موجب.")
        if len(self.declared_sha256) != 64 or any(
            character not in "0123456789abcdef" for character in self.declared_sha256
        ):
            raise ExcerptOriginError(f"«{self.key}»: الختمُ ليس SHA-256 تامًّا.")
        for field_name, value in (
            ("سياسة الفكّ", self.decode_policy),
            ("سياسة التطبيع", self.normalization_policy),
            ("سياسة الأسطر", self.line_policy),
        ):
            if not value.strip():
                raise ExcerptOriginError(f"«{self.key}»: {field_name} غيرُ مُعلَنة.")
        if "strict" not in self.decode_policy:
            raise ExcerptOriginError(
                f"«{self.key}»: الفكُّ ههنا صارمٌ وجوبًا — "
                f"{A_LENIENT_DECODE_IS_NEVER_GENERALISED_WITHOUT_A_MEASURED_RESIDUE}"
            )


_STRICT_UTF8: Final[str] = (
    "utf-8 بـerrors=strict؛ وتُنزَع علامةُ الترتيب إن وُجدت ولا تُفَكّ محرفًا"
)

_NO_FOLDING: Final[str] = (
    "لا تطبيعَ ولا طيّ: لا NFC ولا NFD ولا تجريدَ شكلٍ ولا توحيدَ همزةٍ أو ألف؛ "
    "البايتاتُ تُقرأ كما هي، والمقارنةُ تقع على المحارف لا على صورةٍ مطويّة"
)

_LINE_POLICY: Final[str] = (
    "السطرُ ما بين U+000A، مرقومٌ من الواحد؛ والكلمةُ ما بين بياضٍ داخل السطر، "
    "مرقومةٌ من الواحد — وهذا حدٌّ مُعلَنٌ لا قسمةٌ لغويّة"
)

THE_SEARCH_LIST: Final[tuple[TextSource, ...]] = (
    TextSource(
        key="QURAN_SIMPLE",
        title="المصحف، رواية حفص — نسخةُ tanzil المبسَّطة المحسَّنة",
        edition="quran-simple-enhanced · مودَعٌ في corpora/",
        relative_path="corpora/quran-simple-enhanced.txt",
        declared_byte_length=1_319_901,
        declared_sha256=(
            "37633090743d403886b334d12dd911d1994e49767faa9f2be0f01fd48b466c5a"
        ),
        decode_policy=_STRICT_UTF8,
        normalization_policy=_NO_FOLDING,
        line_policy=_LINE_POLICY,
    ),
    TextSource(
        key="GLOBALQURAN_SIMPLE",
        title="المصحف، رواية حفص — نسخةُ globalquran المبسَّطة المحسَّنة",
        edition="globalquran-simple-enhanced · مودَعٌ في corpora/",
        relative_path="corpora/globalquran-simple-enhanced.txt",
        declared_byte_length=1_306_770,
        declared_sha256=(
            "8b387ea811bc8c658e1cab75488ce1aa69606deafd62759eeaf49ffe15c6d215"
        ),
        decode_policy=_STRICT_UTF8,
        normalization_policy=_NO_FOLDING,
        line_policy=_LINE_POLICY,
    ),
)


def source_by_key(key: str) -> TextSource:
    """المصدرُ بمفتاحه من قائمة البحث؛ ومفتاحٌ غيرُ مُعلَنٍ يُرفَع به خطأ."""

    for source in THE_SEARCH_LIST:
        if source.key == key:
            return source
    declared = " · ".join(one.key for one in THE_SEARCH_LIST)
    raise ExcerptOriginError(
        f"مفتاحُ مصدرٍ غيرُ مُعلَنٍ: «{key}». والمُعلَنُ: {declared}."
    )


def _repo_root(root: Path | None) -> Path:
    return root if root is not None else Path(__file__).resolve().parents[3]


@dataclass(frozen=True, slots=True)
class DecodeAudit:
    """أثرُ الفكّ: أيصحّ الصارمُ؟ وكم كان المتسامحُ سيُسقط ههنا بالعدد؟"""

    strict_succeeds: bool
    bytes_read: int
    characters_strict: int | None
    characters_lenient: int
    characters_dropped_by_lenient: int

    @property
    def lenient_would_hide(self) -> bool:
        """أكان المتسامحُ سيُخفي شيئًا؟ مقيسٌ بالفرق لا مُستنتَجٌ بالظنّ."""

        return self.characters_dropped_by_lenient != 0 or not self.strict_succeeds


def decode_audit(source: TextSource, root: Path | None = None) -> DecodeAudit:
    """يقيس أثرَ الفكّ المتسامح على بايتات هذا المصدر عينِه قبل أن يُمنَع."""

    path = _repo_root(root) / source.relative_path
    if not path.is_file():
        raise ExcerptOriginError(f"«{source.key}»: بايتاتُه غائبةٌ عن الشجرة.")
    raw = path.read_bytes()
    lenient = raw.decode("utf-8", errors="ignore")
    try:
        strict: str | None = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        strict = None
    return DecodeAudit(
        strict_succeeds=strict is not None,
        bytes_read=len(raw),
        characters_strict=None if strict is None else len(strict),
        characters_lenient=len(lenient),
        characters_dropped_by_lenient=(
            0 if strict is None else len(strict) - len(lenient)
        ),
    )


@dataclass(frozen=True, slots=True)
class SourceReading:
    """قراءةُ مصدرٍ الآن: منزلتُه وطولُه وختمُه كما يُقاسان من القرص."""

    source: TextSource
    standing: SourceStanding
    measured_byte_length: int | None
    measured_sha256: str | None


def source_reading(source: TextSource, root: Path | None = None) -> SourceReading:
    """يُصادِم المُعلَنَ بالمقيس عند كلّ نداء؛ ولا يحفظ حكمًا من نداءٍ سابق."""

    path = _repo_root(root) / source.relative_path
    if not path.is_file():
        return SourceReading(source, SourceStanding.ABSENT_FROM_THIS_TREE, None, None)
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    agrees = len(raw) == source.declared_byte_length and digest == source.declared_sha256
    return SourceReading(
        source=source,
        standing=(
            SourceStanding.SEALED_AND_PRESENT
            if agrees
            else SourceStanding.SEAL_BROKEN
        ),
        measured_byte_length=len(raw),
        measured_sha256=digest,
    )


def source_text(source: TextSource, root: Path | None = None) -> str:
    """نصُّ المصدر مفكوكًا فكًّا صارمًا، بعد مصادمةِ ختمه؛ ولا يُطبَّع."""

    reading = source_reading(source, root)
    if not reading.standing.is_readable:
        raise ExcerptOriginError(
            f"«{source.key}»: {reading.standing.value} — لا نصَّ يُقرأ منه."
        )
    raw = (_repo_root(root) / source.relative_path).read_bytes()
    text = raw.decode("utf-8", errors="strict")
    return text.lstrip("\ufeff")


# ----- العنوان والموضع -----


@dataclass(frozen=True, slots=True)
class WordAddress:
    """عنوانُ كلمةٍ: مفتاحُ مصدرٍ وسطرٌ وكلمة. ولا عنوانَ بلا مفتاح مصدر."""

    source_key: str
    line: int
    word: int

    def __post_init__(self) -> None:
        if not self.source_key.strip():
            raise ExcerptOriginError(
                f"عنوانٌ بلا مفتاح مصدر: {THE_ADDRESS_WITHOUT_A_SOURCE_IS_NOT_AN_IDENTITY}"
            )
        if self.line < 1 or self.word < 1:
            raise ExcerptOriginError("السطرُ والكلمةُ مرقومان من الواحد.")

    @property
    def rendered(self) -> str:
        """صورةُ العنوان مكتوبةً، ومفتاحُ المصدر جزءٌ منها لا يُحذَف."""

        return f"{self.source_key}@L{self.line}:W{self.word}"


@dataclass(frozen=True, slots=True)
class LocatedWord:
    """كلمةٌ محلولةُ الموضع: سطحُها وإزاحتاها وسطرُها وسياقاها."""

    address: WordAddress
    surface: str
    char_offset: int
    char_length: int
    byte_offset: int
    byte_length: int
    line_text: str
    preceding_context: str
    following_context: str
    preceding_word: str | None
    following_word: str | None

    @property
    def excerpt_bounds(self) -> tuple[int, int]:
        """حدَّا المقتطف بالمحارف في نصّ المصدر المفكوك: بدايةٌ ونهاية."""

        return (self.char_offset, self.char_offset + self.char_length)


def locate(
    address: WordAddress, root: Path | None = None, context: int = 40
) -> LocatedWord:
    """يَحُلُّ عنوانًا إلى موضعٍ في بايتاتٍ مختومة، ويَردُّ ما لا تحتمله."""

    if context < 0:
        raise ExcerptOriginError("مدى السياق لا يكون سالبًا.")
    source = source_by_key(address.source_key)
    text = source_text(source, root)
    lines = text.split("\n")
    if address.line > len(lines):
        raise ExcerptOriginError(
            f"«{address.rendered}»: المصدرُ {len(lines)} سطرًا، فلا سطرَ "
            f"{address.line} فيه."
        )
    line_text = lines[address.line - 1]
    words = line_text.split()
    if address.word > len(words):
        raise ExcerptOriginError(
            f"«{address.rendered}»: السطرُ {len(words)} كلمةً، فلا كلمةَ "
            f"{address.word} فيه."
        )
    line_start = sum(len(one) + 1 for one in lines[: address.line - 1])
    cursor = 0
    for one in words[: address.word - 1]:
        cursor = line_text.index(one, cursor) + len(one)
    surface = words[address.word - 1]
    in_line = line_text.index(surface, cursor)
    char_offset = line_start + in_line
    return LocatedWord(
        address=address,
        surface=surface,
        char_offset=char_offset,
        char_length=len(surface),
        byte_offset=len(text[:char_offset].encode("utf-8")),
        byte_length=len(surface.encode("utf-8")),
        line_text=line_text,
        preceding_context=text[max(0, char_offset - context) : char_offset],
        following_context=text[
            char_offset + len(surface) : char_offset + len(surface) + context
        ],
        preceding_word=words[address.word - 2] if address.word > 1 else None,
        following_word=(
            words[address.word] if address.word < len(words) else None
        ),
    )


def address_collisions(
    line: int, word: int, root: Path | None = None
) -> tuple[tuple[str, str | None], ...]:
    """يَحُلُّ عنوانًا عاريًا في كلّ مصدرٍ ليُرى أنّه إزاحةٌ لا هويّة.

    ويُخرِج لكلّ مفتاحِ مصدرٍ ما يُحَلّ إليه العنوانُ فيه، أو `None` إن لم
    يحتمله ذلك المصدر. فاختلافُ المدلولات هو البرهان، لا الوصف.
    """

    found: list[tuple[str, str | None]] = []
    for source in THE_SEARCH_LIST:
        try:
            located = locate(WordAddress(source.key, line, word), root, context=0)
        except ExcerptOriginError:
            found.append((source.key, None))
        else:
            found.append((source.key, located.surface))
    return tuple(found)


# ----- الدعاوى الثلاث -----


class OriginClaim(Enum):
    """الدعاوى الثلاثُ مفصولةً بأسمائها، ولا تُدمَج اثنتان في حكمٍ واحد."""

    PRESENT_IN_A_SOURCE = "العبارةُ موجودةٌ في مصدر"
    UNIQUE_IN_THE_SEARCH_LIST = "موضعُها متفرّدٌ داخل قائمة البحث"
    IS_THE_ORIGIN_OF_THE_EXCERPT = "هذا الموضعُ أصلُ مقتطفِ مجموعة البيانات"


class ClaimStanding(Enum):
    """منازلُ ثلاثٌ لا اثنتان: غيابُ الدليل ليس امتناعًا بدليل."""

    ESTABLISHED = "مُثبَتة"
    REFUTED = "ممتنعةٌ بدليل"
    SUSPENDED = "معلَّقةٌ بسببٍ مسمًّى"


@dataclass(frozen=True, slots=True)
class ClaimReading:
    """قراءةُ دعوى: منزلتُها ودليلُها ومواضعُها المقيسة."""

    claim: OriginClaim
    standing: ClaimStanding
    evidence: str
    positions: tuple[tuple[str, int], ...] = ()

    @property
    def is_established(self) -> bool:
        """لا يُقرأ معلَّقٌ مُثبَتًا، ولا ممتنعٌ معلَّقًا."""

        return self.standing is ClaimStanding.ESTABLISHED


@dataclass(frozen=True, slots=True)
class OriginWitness:
    """شهادةُ منشأ: لا تُقبَل إلّا مُسمّاةَ المجموعة والسطر والمصدر والمنهج."""

    dataset_id: str
    dataset_line_id: str
    source_key: str
    source_char_offset: int
    method: str
    examiner: str

    def __post_init__(self) -> None:
        for name, value in (
            ("مُعرِّف مجموعة البيانات", self.dataset_id),
            ("مُعرِّف سطرها", self.dataset_line_id),
            ("مفتاح المصدر", self.source_key),
            ("منهج الربط", self.method),
            ("المنفِّذ", self.examiner),
        ):
            if not value.strip():
                raise ExcerptOriginError(
                    f"شهادةُ منشأٍ بلا {name} لا تُقبَل: "
                    f"{THE_THIRD_CLAIM_IS_NEVER_DERIVED_FROM_THE_FIRST_TWO}"
                )
        if self.source_char_offset < 0:
            raise ExcerptOriginError("إزاحةُ شهادةِ المنشأ لا تكون سالبة.")


def _occurrences(
    phrase: str, root: Path | None, sources: tuple[TextSource, ...]
) -> tuple[tuple[str, int], ...]:
    found: list[tuple[str, int]] = []
    for source in sources:
        text = source_text(source, root)
        start = text.find(phrase)
        while start >= 0:
            found.append((source.key, start))
            start = text.find(phrase, start + 1)
    return tuple(found)


def origin_readings(
    phrase: str,
    *,
    witnesses: tuple[OriginWitness, ...] = (),
    sources: tuple[TextSource, ...] | None = None,
    root: Path | None = None,
) -> tuple[ClaimReading, ...]:
    """الدعاوى الثلاثُ مقروءةً بأدلّتها؛ والثالثةُ لا تُشتَقّ من الأوليَين.

    فالأولى والثانيةُ تُقاسان من البايتات، والثالثةُ لا تُقاس منها البتّة:
    لا تُثبَت إلّا بشهادةِ منشأٍ تُطابق مفتاحَ مصدرٍ وإزاحةً من المواضع
    المقيسة. وما عداه تعليقٌ مُسمّى السبب، لا امتناعٌ ولا إثبات.
    """

    if not phrase:
        raise ExcerptOriginError("عبارةٌ خاليةٌ لا يُبحَث عن منشئها.")
    if unicodedata.normalize("NFC", phrase) != phrase:
        raise ExcerptOriginError(
            "العبارةُ غيرُ مطبَّعةٍ تطبيعَ NFC، والمصادرُ تُقرأ بلا طيّ؛ "
            "فالمقارنةُ ملتبسةٌ ولا تُجرى."
        )
    scope = THE_SEARCH_LIST if sources is None else sources
    if not scope:
        raise ExcerptOriginError("قائمةُ بحثٍ خاليةٌ لا يُقاس عليها تفرّد.")
    positions = _occurrences(phrase, root, scope)
    listed = " · ".join(one.key for one in scope)

    present = ClaimReading(
        claim=OriginClaim.PRESENT_IN_A_SOURCE,
        standing=(
            ClaimStanding.ESTABLISHED if positions else ClaimStanding.REFUTED
        ),
        evidence=(
            f"وُجدت في {len(positions)} موضعًا ضمن [{listed}]"
            if positions
            else f"لم تُوجَد في أيّ بايتةٍ من [{listed}]"
        ),
        positions=positions,
    )

    if not positions:
        unique = ClaimReading(
            claim=OriginClaim.UNIQUE_IN_THE_SEARCH_LIST,
            standing=ClaimStanding.SUSPENDED,
            evidence=(
                "لا موضعَ أصلًا، فلا يُقال متفرّدٌ ولا غيرُ متفرّد — "
                f"{UNIQUENESS_IS_RELATIVE_TO_A_DECLARED_SEARCH_LIST}"
            ),
        )
    else:
        unique = ClaimReading(
            claim=OriginClaim.UNIQUE_IN_THE_SEARCH_LIST,
            standing=(
                ClaimStanding.ESTABLISHED
                if len(positions) == 1
                else ClaimStanding.REFUTED
            ),
            evidence=(
                f"{len(positions)} موضعًا في [{listed}] — "
                f"{UNIQUENESS_IS_RELATIVE_TO_A_DECLARED_SEARCH_LIST}"
            ),
            positions=positions,
        )

    matched = tuple(
        one
        for one in witnesses
        if (one.source_key, one.source_char_offset) in positions
    )
    if matched:
        origin = ClaimReading(
            claim=OriginClaim.IS_THE_ORIGIN_OF_THE_EXCERPT,
            standing=ClaimStanding.ESTABLISHED,
            evidence=(
                f"شهادةُ منشأٍ مُطابِقةٌ لموضعٍ مقيس: مجموعة «{matched[0].dataset_id}» "
                f"سطر «{matched[0].dataset_line_id}» بمنهج «{matched[0].method}» "
                f"عن «{matched[0].examiner}»"
            ),
            positions=tuple(
                (one.source_key, one.source_char_offset) for one in matched
            ),
        )
    elif witnesses:
        origin = ClaimReading(
            claim=OriginClaim.IS_THE_ORIGIN_OF_THE_EXCERPT,
            standing=ClaimStanding.REFUTED,
            evidence=(
                "شهادةُ المنشأ تُحيل إلى موضعٍ لا تُخرجه البايتاتُ لهذه العبارة، "
                "فالمصدرُ صحيحٌ والموضعُ خاطئ"
            ),
        )
    else:
        origin = ClaimReading(
            claim=OriginClaim.IS_THE_ORIGIN_OF_THE_EXCERPT,
            standing=ClaimStanding.SUSPENDED,
            evidence=(
                "لا شهادةَ منشأٍ مُودَعة — "
                f"{THE_THIRD_CLAIM_IS_NEVER_DERIVED_FROM_THE_FIRST_TWO}"
            ),
        )
    return (present, unique, origin)


def transferable_context(
    readings: tuple[ClaimReading, ...], located: LocatedWord
) -> tuple[str, str]:
    """سياقا موضعٍ، ولا يُسلَّمان إلّا بعد إثبات أنّه أصلُ المقتطف.

    فإن بقيت دعوى المنشأ معلَّقةً أو ممتنعةً امتنع النقلُ ورُفِع الخطأ باسمه:
    السياقُ خاصّةُ الموضعِ المُثبَت لا خاصّةُ العبارة الموجودة.
    """

    for reading in readings:
        if reading.claim is OriginClaim.IS_THE_ORIGIN_OF_THE_EXCERPT:
            if reading.is_established:
                return (located.preceding_context, located.following_context)
            raise ExcerptOriginError(
                f"مُنِع نقلُ السياق: دعوى المنشأ {reading.standing.value} — "
                f"{reading.evidence}"
            )
    raise ExcerptOriginError("لا قراءةَ لدعوى المنشأ في المُعطى، فلا سياقَ يُنقَل.")


# ----- التدقيقُ السابق: غيابٌ يُقاس لا يُوصَف -----


@dataclass(frozen=True, slots=True)
class PriorAuditMaterial:
    """مادّةُ التدقيق السابق كما وُصفت لنا، ومواضعُ البحث عنها."""

    archive_name: str
    declared_sections: tuple[str, ...]
    declared_identifier: str
    declared_surface: str
    searched_names: tuple[str, ...]


THE_PRIOR_AUDIT: Final[PriorAuditMaterial] = PriorAuditMaterial(
    archive_name="Arabic_Letter_Exhaustive_Audit.zip",
    declared_sections=("القسم ٣٨", "القسم ٣٩"),
    declared_identifier="L329:W3",
    declared_surface="نَظَرٌ",
    searched_names=(
        "Arabic_Letter_Exhaustive_Audit.zip",
        "*Arabic_Letter*",
        "*Exhaustive_Audit*",
        "وَفِي الْفَرْقِ نَظَرٌ",
        "L329:W3",
        "غذاء الألباب",
        "التختم",
        "البنصر",
    ),
)


@dataclass(frozen=True, slots=True)
class PriorAuditStanding:
    """منزلةُ مادّة التدقيق السابق الآن: حضورُها، وما يُحَلّ إليه معرِّفُها."""

    archive_present: bool
    surface_present_in_tree: bool
    identifier_resolves_to: tuple[tuple[str, str | None], ...]

    @property
    def is_reproducible(self) -> bool:
        """لا تُعاد نتيجةٌ من مادّةٍ غائبة، ولا يُسَدّ الغيابُ بعنوانٍ عارٍ."""

        return self.archive_present and self.surface_present_in_tree


def prior_audit_standing(root: Path | None = None) -> PriorAuditStanding:
    """يقيس غيابَ مادّة التدقيق، ويُحِلّ معرِّفَها في كلّ مصدرٍ مختوم.

    والمقصودُ من الإحلال ليس إيجادَ بديلٍ عن «نَظَرٌ»، بل إظهارُ أنّ العنوانَ
    العاريَ يُخرج في كلّ مصدرٍ كلمةً أخرى — فهو إزاحةٌ لا هويّة.
    """

    base = _repo_root(root)
    archive = (base / THE_PRIOR_AUDIT.archive_name).is_file()
    surface = any(
        THE_PRIOR_AUDIT.declared_surface in source_text(one, root)
        for one in THE_SEARCH_LIST
        if source_reading(one, root).standing.is_readable
    )
    return PriorAuditStanding(
        archive_present=archive,
        surface_present_in_tree=surface,
        identifier_resolves_to=address_collisions(329, 3, root),
    )
