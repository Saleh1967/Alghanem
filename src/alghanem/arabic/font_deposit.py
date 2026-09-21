"""المصدرُ الثاني للبتات: وديعةُ الخطّ، وقراءتُها من بايتاتها الخام.

كلُّ ما قِيس في هذه الشجرة قبلَ هذه الوحدة مشتقٌّ من بايتات النصّ وجدولِ
يونيكود. **ويونيكود لا يخزّن هندسة الرسم**؛ فمن سأله كيف رُسم الحرفُ سأله ما
لا يملك. فلا سبيلَ إلى الهندسة إلّا بمصدرٍ ثانٍ من البتات:

```
TextBits ⊕ FontBits → GlyphGeometry
```

**أوّلًا: والإيداعُ شرطُ وجودِ النتيجة لا تحسينُها.** قُرئت هذه الخطوطُ أوّلَ
مرّةٍ من `/usr/share/fonts`، ثمّ اختفت بإعادةِ تهيئة البيئة، فسقط كلُّ رقمٍ
قِيس عليها سقوطًا تامًّا. فما لا يُعاد اشتقاقُه من بايتاتٍ مُودَعةٍ وقتَ
القراءة ليس رقمًا في هذه الشجرة، وإن صحّ حسابُه ساعةَ حُسب
(`A_FONT_READ_FROM_THE_SYSTEM_IS_NOT_A_DEPOSIT`).

**وثانيًا: والقراءةُ بالمكتبة القياسيّة وحدَها.** اعتماديّاتُ التشغيل في هذه
الشجرة **صفر**، ولم تُزَد لأجل هذا القياس. فجداولُ `head` و`maxp` و`loca`
و`cmap` و`glyf` تُقرأ من البايتات بـ`struct` لا غير. وثمنُ ذلك **محدوديّةٌ
معلَنة**: ما لا تفهمه هذه الوحدةُ **تَرفُضه ولا تخمّنه**؛ صيغةُ `cmap` غير
الرابعة تُرفَض، وتحويلُ المقياس في المركّب يُرفَض، ورسمُ `CFF` يُرفَض
(`WHAT_THIS_READER_CANNOT_PARSE_IT_REFUSES_AND_DOES_NOT_GUESS`).

**وثالثًا: والوديعةُ موصوفةٌ ببصمةٍ مجمَّدة.** لكلّ ملفٍّ `SHA-256` وطولُ
بايتاتٍ وعددُ رسومٍ وأسماءُ جداول، مجمَّدةٌ ههنا ومقروءةٌ من القرص عند كلّ
نداء. فإن زُحزح بايتٌ واحدٌ رُفض التحميلُ ولم يُصلَح ولم يُحذَّر
(`THE_MANIFEST_REFUSES_A_DRIFTED_DEPOSIT_AND_DOES_NOT_REPAIR_IT`).

**ورابعًا: والثلاثةُ طرفا تباينٍ وشاهدُ نقل.** أميري وشهرزاد نسخيّان من
صانعَين مستقلَّين، وكوفيُّ نوتو لا يعلن تفكيكًا ألبتّة. فبالأوّلَين يُختبَر
أنّ ما وُجد ليس تصميمَ خطٍّ واحد، وبالثالث يُفصَل **المُعلَنُ** عن **المقيس**.

**وخامسًا: وما ليس ههنا.** ليس ههنا محرّكُ تشكيل. فاختيارُ الرسم بحسب السياق
(`init/medi/fina`) يقتضي `GSUB` السياقيَّ، وهو خارجَ ما تُنجزه المكتبةُ
القياسيّةُ على وجهٍ يُوثَق به. فلا تُقرَأ ههنا إلّا الرسومُ المنفصلة، ولا
تُقارَن أوضاعٌ مختلفة بعضُها ببعض
(`THERE_IS_NO_SHAPING_ENGINE_HERE_ONLY_ISOLATED_GLYPHS`).
"""

from __future__ import annotations

import hashlib
import struct
from dataclasses import dataclass, fields
from functools import cache
from pathlib import Path
from typing import Final

__all__ = [
    "AMIRI",
    "A_FONT_READ_FROM_THE_SYSTEM_IS_NOT_A_DEPOSIT",
    "Contour",
    "FONT_DEPOSIT",
    "FONT_DEPOSIT_DIRECTORY",
    "FONT_DEPOSIT_NAMED_RESIDUALS",
    "FontBits",
    "FontDepositError",
    "FontManifest",
    "NOTO_KUFI",
    "SCHEHERAZADE",
    "THERE_IS_NO_SHAPING_ENGINE_HERE_ONLY_ISOLATED_GLYPHS",
    "THE_MANIFEST_REFUSES_A_DRIFTED_DEPOSIT_AND_DOES_NOT_REPAIR_IT",
    "WHAT_THIS_READER_CANNOT_PARSE_IT_REFUSES_AND_DOES_NOT_GUESS",
    "deposit_bytes",
    "deposit_path",
    "every_deposit_matches_its_manifest",
    "load_font",
    "measured_manifest_of",
]

FONT_DEPOSIT_DIRECTORY: Final[str] = "fonts"

AMIRI: Final[str] = "Amiri-Regular.ttf"
SCHEHERAZADE: Final[str] = "Scheherazade-Regular.ttf"
NOTO_KUFI: Final[str] = "NotoKufiArabic-Regular.ttf"

_TRUETYPE_SFNT_VERSION: Final[bytes] = b"\x00\x01\x00\x00"
_SUPPORTED_CMAP_FORMAT: Final[int] = 4
_REQUIRED_TABLES: Final[tuple[str, ...]] = ("cmap", "glyf", "head", "loca", "maxp")

_ARG_WORDS: Final[int] = 0x0001
_ROUND_TO_GRID: Final[int] = 0x0004
_SIMPLE_SCALE: Final[int] = 0x0008
_MORE_COMPONENTS: Final[int] = 0x0020
_XY_SCALE: Final[int] = 0x0040
_TWO_BY_TWO: Final[int] = 0x0080
_ARGS_ARE_XY: Final[int] = 0x0002

_ON_CURVE: Final[int] = 0x01
_X_SHORT: Final[int] = 0x02
_Y_SHORT: Final[int] = 0x04
_REPEAT: Final[int] = 0x08
_X_SAME: Final[int] = 0x10
_Y_SAME: Final[int] = 0x20


class FontDepositError(ValueError):
    """رفضٌ عند البتات: وديعةٌ زُحزحت، أو بنيةٌ لا يفهمها هذا القارئ."""


Contour = tuple[tuple[int, int, bool], ...]


@dataclass(frozen=True)
class FontManifest:
    """وصفُ وديعةٍ مجمَّد: بصمتُها وطولُها ورسومُها وجداولُها."""

    filename: str
    sha256: str
    byte_length: int
    glyph_count: int
    units_per_em: int
    tables: tuple[str, ...]

    def __post_init__(self) -> None:
        if len(self.sha256) != 64:
            raise FontDepositError(f"بصمةٌ ليست SHA-256 لـ{self.filename}.")
        if self.byte_length < 1 or self.glyph_count < 1 or self.units_per_em < 1:
            raise FontDepositError(f"وصفٌ خالٍ لا يوصَف به خطّ: {self.filename}.")
        if tuple(sorted(self.tables)) != self.tables:
            raise FontDepositError(f"جداولُ {self.filename} غيرُ مرتَّبة.")
        for required in _REQUIRED_TABLES:
            if required not in self.tables:
                raise FontDepositError(
                    f"وديعةٌ بلا جدول `{required}`: {self.filename}؛ ولا تُقرأ هندستُها."
                )


FONT_DEPOSIT: Final[tuple[FontManifest, ...]] = (
    FontManifest(
        filename=AMIRI,
        sha256="316c56966b5ceb7ccd7f6fc490b3c3b31033523cfabd3d591395642c4b86ea62",
        byte_length=627240,
        glyph_count=6712,
        units_per_em=1000,
        tables=(
            "GDEF",
            "GPOS",
            "GSUB",
            "OS/2",
            "cmap",
            "gasp",
            "glyf",
            "head",
            "hhea",
            "hmtx",
            "loca",
            "maxp",
            "name",
            "post",
            "prep",
        ),
    ),
    FontManifest(
        filename=SCHEHERAZADE,
        sha256="034c3ed203ccf91e20a75181350759cc5878e0e369bb0e2e83acee15a829184f",
        byte_length=500396,
        glyph_count=1411,
        units_per_em=2048,
        tables=(
            "Feat",
            "GDEF",
            "GPOS",
            "GSUB",
            "Glat",
            "Gloc",
            "OS/2",
            "Silf",
            "Sill",
            "Silt",
            "cmap",
            "cvt ",
            "fpgm",
            "gasp",
            "glyf",
            "head",
            "hhea",
            "hmtx",
            "loca",
            "maxp",
            "name",
            "post",
            "prep",
        ),
    ),
    FontManifest(
        filename=NOTO_KUFI,
        sha256="befb9d07506942ba2a7e0e85c65a24a76792c937d812bc80f1095d0f660cf330",
        byte_length=176740,
        glyph_count=733,
        units_per_em=1000,
        tables=(
            "DSIG",
            "GDEF",
            "GPOS",
            "GSUB",
            "OS/2",
            "cmap",
            "cvt ",
            "fpgm",
            "gasp",
            "glyf",
            "head",
            "hhea",
            "hmtx",
            "loca",
            "maxp",
            "name",
            "post",
            "prep",
        ),
    ),
)


def _repository_root() -> Path:
    return Path(__file__).resolve().parents[3]


def deposit_path(filename: str) -> Path:
    """مسارُ وديعةٍ في الشجرة؛ ولا يُقرأ خطٌّ من خارجها."""

    return _repository_root() / FONT_DEPOSIT_DIRECTORY / filename


def deposit_bytes(filename: str) -> bytes:
    """بايتاتُ وديعةٍ خامًّا، وهي أصلُ كلّ رقمٍ هندسيٍّ ههنا."""

    path = deposit_path(filename)
    if not path.is_file():
        raise FontDepositError(
            f"لا وديعةَ باسم {filename} في `{FONT_DEPOSIT_DIRECTORY}/`؛ "
            "ولا يُقرأ خطُّ النظام بديلًا عنها."
        )
    return path.read_bytes()


def measured_manifest_of(filename: str) -> FontManifest:
    """وصفُ الوديعةِ **الآن**، مقروءًا من بايتاتها لا من المجمَّد."""

    raw = deposit_bytes(filename)
    tables = _table_directory(raw)
    head_offset = tables["head"][0]
    maxp_offset = tables["maxp"][0]
    return FontManifest(
        filename=filename,
        sha256=hashlib.sha256(raw).hexdigest(),
        byte_length=len(raw),
        glyph_count=struct.unpack(">H", raw[maxp_offset + 4 : maxp_offset + 6])[0],
        units_per_em=struct.unpack(">H", raw[head_offset + 18 : head_offset + 20])[0],
        tables=tuple(sorted(tables)),
    )


def every_deposit_matches_its_manifest() -> bool:
    """أطابقت الودائعُ أوصافَها المجمَّدة؟ يُقاس من القرص لا يُفترَض."""

    return all(
        measured_manifest_of(manifest.filename) == manifest for manifest in FONT_DEPOSIT
    )


def _table_directory(raw: bytes) -> dict[str, tuple[int, int]]:
    if raw[:4] != _TRUETYPE_SFNT_VERSION:
        raise FontDepositError(
            "ليست وديعةً بنسق `glyf` التقليديّ؛ ورسمُ `CFF` يُرفَض ولا يُخمَّن."
        )
    count = struct.unpack(">H", raw[4:6])[0]
    directory: dict[str, tuple[int, int]] = {}
    for index in range(count):
        entry = 12 + 16 * index
        tag, _checksum, offset, length = struct.unpack(
            ">4sIII", raw[entry : entry + 16]
        )
        directory[tag.decode("ascii")] = (offset, length)
    for required in _REQUIRED_TABLES:
        if required not in directory:
            raise FontDepositError(f"وديعةٌ بلا جدول `{required}`؛ ولا تُقرأ هندستُها.")
    return directory


@dataclass(frozen=True)
class FontBits:
    """خطٌّ مقروءٌ من بايتاته: رسومُه وهندستُها، بلا محرّك تشكيل."""

    manifest: FontManifest
    _raw: bytes
    _tables: dict[str, tuple[int, int]]
    _long_loca: bool
    _cmap_subtable: int

    @property
    def glyph_count(self) -> int:
        """عددُ الرسوم في الوديعة، مقروءًا من `maxp`."""

        return self.manifest.glyph_count

    def glyph_for(self, character: str) -> int:
        """رقمُ رسمِ حرفٍ منفصلٍ من `cmap`؛ وصفرٌ يعني لا رسمَ له."""

        if len(character) != 1:
            raise FontDepositError("يُسأل `cmap` عن حرفٍ واحدٍ لا عن نصّ.")
        return self._lookup(ord(character))

    def _lookup(self, code: int) -> int:
        raw = self._raw
        base = self._cmap_subtable
        segment_bytes = struct.unpack(">H", raw[base + 6 : base + 8])[0]
        ends = base + 14
        starts = ends + segment_bytes + 2
        deltas = starts + segment_bytes
        ranges = deltas + segment_bytes
        for index in range(segment_bytes // 2):
            end = struct.unpack(">H", raw[ends + 2 * index : ends + 2 * index + 2])[0]
            if code > end:
                continue
            start = struct.unpack(
                ">H", raw[starts + 2 * index : starts + 2 * index + 2]
            )[0]
            if code < start:
                return 0
            delta = int(
                struct.unpack(">h", raw[deltas + 2 * index : deltas + 2 * index + 2])[0]
            )
            offset = struct.unpack(
                ">H", raw[ranges + 2 * index : ranges + 2 * index + 2]
            )[0]
            if offset == 0:
                return (code + delta) & 0xFFFF
            at = ranges + 2 * index + offset + 2 * (code - start)
            glyph = int(struct.unpack(">H", raw[at : at + 2])[0])
            return 0 if glyph == 0 else (glyph + delta) & 0xFFFF
        return 0

    def _glyph_span(self, glyph: int) -> tuple[int, int]:
        if not 0 <= glyph < self.glyph_count:
            raise FontDepositError(f"رقمُ رسمٍ خارج الوديعة: {glyph}.")
        loca = self._tables["loca"][0]
        if self._long_loca:
            at = loca + 4 * glyph
            first, second = struct.unpack(">II", self._raw[at : at + 8])
            return int(first), int(second)
        at = loca + 2 * glyph
        first, second = struct.unpack(">HH", self._raw[at : at + 4])
        return int(first) * 2, int(second) * 2

    def is_composite(self, glyph: int) -> bool:
        """أرسمٌ مركّبٌ هو، أي أنّ الخطّ **يعلن** تفكيكَه في بتاته؟"""

        start, end = self._glyph_span(glyph)
        if start == end:
            return False
        at = self._tables["glyf"][0] + start
        return bool(struct.unpack(">h", self._raw[at : at + 2])[0] < 0)

    def components_of(self, glyph: int) -> tuple[tuple[int, int, int], ...]:
        """مكوّناتُ رسمٍ مركّبٍ كما أعلنها الخطّ: رقمٌ وإزاحتان."""

        if not self.is_composite(glyph):
            raise FontDepositError(f"رسمٌ غيرُ مركّبٍ لا مكوّناتِ له: {glyph}.")
        raw = self._raw
        start, _end = self._glyph_span(glyph)
        at = self._tables["glyf"][0] + start + 10
        found: list[tuple[int, int, int]] = []
        while True:
            flags, index = struct.unpack(">HH", raw[at : at + 4])
            at += 4
            if flags & _ARG_WORDS:
                first, second = struct.unpack(">hh", raw[at : at + 4])
                at += 4
            else:
                first, second = struct.unpack(">bb", raw[at : at + 2])
                at += 2
            if not flags & _ARGS_ARE_XY:
                raise FontDepositError(
                    "مكوّنٌ مركّبٌ يُركَّب بمطابقة نقطتين لا بإزاحة؛ وهذا يُرفَض."
                )
            if flags & (_SIMPLE_SCALE | _XY_SCALE | _TWO_BY_TWO):
                raise FontDepositError(
                    "مكوّنٌ مركّبٌ بتحويل مقياسٍ أو مصفوفة؛ وهذا القارئُ يرفضه "
                    "ولا يخمّن هندستَه."
                )
            if flags & _ROUND_TO_GRID:
                pass
            found.append((index, first, second))
            if not flags & _MORE_COMPONENTS:
                break
        return tuple(found)

    def contours_of(self, glyph: int) -> tuple[Contour, ...]:
        """كنتوراتُ رسمٍ بسيط: نقاطُه بإحداثيّاتها المطلقة داخل الرسم."""

        if self.is_composite(glyph):
            raise FontDepositError(f"رسمٌ مركّبٌ لا كنتوراتِ له مباشرةً: {glyph}.")
        start, end = self._glyph_span(glyph)
        if start == end:
            return ()
        raw = self._raw
        at = self._tables["glyf"][0] + start
        count = struct.unpack(">h", raw[at : at + 2])[0]
        ends = [
            struct.unpack(">H", raw[at + 10 + 2 * i : at + 12 + 2 * i])[0]
            for i in range(count)
        ]
        total = ends[-1] + 1
        cursor = at + 10 + 2 * count
        instructions = struct.unpack(">H", raw[cursor : cursor + 2])[0]
        cursor += 2 + instructions
        flags: list[int] = []
        while len(flags) < total:
            flag = raw[cursor]
            cursor += 1
            flags.append(flag)
            if flag & _REPEAT:
                repeats = raw[cursor]
                cursor += 1
                flags.extend([flag] * repeats)
        flags = flags[:total]
        xs, cursor = self._deltas(flags, cursor, _X_SHORT, _X_SAME)
        ys, cursor = self._deltas(flags, cursor, _Y_SHORT, _Y_SAME)
        contours: list[Contour] = []
        first = 0
        for last in ends:
            contours.append(
                tuple(
                    (xs[i], ys[i], bool(flags[i] & _ON_CURVE))
                    for i in range(first, last + 1)
                )
            )
            first = last + 1
        return tuple(contours)

    def _deltas(
        self, flags: list[int], cursor: int, short: int, same: int
    ) -> tuple[list[int], int]:
        raw = self._raw
        values: list[int] = []
        running = 0
        for flag in flags:
            if flag & short:
                step = raw[cursor]
                cursor += 1
                running += step if flag & same else -step
            elif not flag & same:
                running += struct.unpack(">h", raw[cursor : cursor + 2])[0]
                cursor += 2
            values.append(running)
        return values, cursor

    def outline_of(self, glyph: int, depth: int = 0) -> tuple[Contour, ...]:
        """هندسةُ رسمٍ مبسوطةً: يُحَلُّ المركّبُ إلى كنتورات مكوّناته مُزاحةً."""

        if depth > 8:
            raise FontDepositError(f"تركيبٌ متداخلٌ بلا قرارٍ عند الرسم {glyph}.")
        if not self.is_composite(glyph):
            return self.contours_of(glyph)
        spread: list[Contour] = []
        for index, shift_x, shift_y in self.components_of(glyph):
            for contour in self.outline_of(index, depth + 1):
                spread.append(
                    tuple(
                        (x + shift_x, y + shift_y, on_curve)
                        for x, y, on_curve in contour
                    )
                )
        return tuple(spread)

    def outline_hash(self, glyph: int) -> str:
        """بصمةُ هندسةِ رسمٍ مبسوطةً؛ وبها يُربَط كلُّ ادّعاءٍ بالبتات."""

        digest = hashlib.sha256()
        for contour in self.outline_of(glyph):
            for x, y, on_curve in contour:
                digest.update(f"{x},{y},{int(on_curve)};".encode("ascii"))
            digest.update(b"|")
        return digest.hexdigest()


@cache
def load_font(filename: str) -> FontBits:
    """يحمّل وديعةً بعد مطابقةِ وصفِها المجمَّد؛ ويرفض عند أيّ انزياح."""

    frozen = {manifest.filename: manifest for manifest in FONT_DEPOSIT}
    if filename not in frozen:
        raise FontDepositError(f"خطٌّ لا وصفَ مجمَّدًا له: {filename}.")
    measured = measured_manifest_of(filename)
    if measured != frozen[filename]:
        raise FontDepositError(
            f"وديعةُ {filename} لا تطابق وصفَها المجمَّد؛ فالقراءةُ مرفوضة "
            "ولا تُصلَح ولا يُكتفى بالتحذير."
        )
    raw = deposit_bytes(filename)
    tables = _table_directory(raw)
    head_offset = tables["head"][0]
    index_to_loc = struct.unpack(">h", raw[head_offset + 50 : head_offset + 52])[0]
    if index_to_loc not in (0, 1):
        raise FontDepositError("صيغةُ `loca` غيرُ معروفة؛ وتُرفَض ولا تُخمَّن.")
    cmap_offset = tables["cmap"][0]
    subtable_count = struct.unpack(">H", raw[cmap_offset + 2 : cmap_offset + 4])[0]
    chosen = 0
    for index in range(subtable_count):
        entry = cmap_offset + 4 + 8 * index
        _platform, _encoding, offset = struct.unpack(">HHI", raw[entry : entry + 8])
        at = cmap_offset + offset
        if struct.unpack(">H", raw[at : at + 2])[0] == _SUPPORTED_CMAP_FORMAT:
            chosen = at
            break
    if chosen == 0:
        raise FontDepositError(
            f"لا جدولَ `cmap` بالصيغة {_SUPPORTED_CMAP_FORMAT} في {filename}؛ "
            "وسائرُ الصيغ تُرفَض ولا تُخمَّن."
        )
    return FontBits(
        manifest=measured,
        _raw=raw,
        _tables=tables,
        _long_loca=index_to_loc == 1,
        _cmap_subtable=chosen,
    )


A_FONT_READ_FROM_THE_SYSTEM_IS_NOT_A_DEPOSIT: Final[str] = (
    "A_FONT_READ_FROM_THE_SYSTEM_IS_NOT_A_DEPOSIT: قُرئت هذه الخطوطُ أوّلَ "
    "مرّةٍ من `/usr/share/fonts` فاختفت بإعادةِ تهيئة البيئة، وسقط كلُّ رقمٍ "
    "قِيس عليها. فالإيداعُ ههنا شرطُ وجودِ النتيجة لا تحسينُها، ولا يُقرأ خطُّ "
    "النظام بديلًا عن وديعةٍ ناقصة: يُرفَض القياسُ ولا يُستعاض عنه."
)

WHAT_THIS_READER_CANNOT_PARSE_IT_REFUSES_AND_DOES_NOT_GUESS: Final[str] = (
    "WHAT_THIS_READER_CANNOT_PARSE_IT_REFUSES_AND_DOES_NOT_GUESS: اعتماديّاتُ "
    "التشغيل صفرٌ ولم تُزَد، فالقراءةُ بـ`struct` وحدَه. وثمنُها محدوديّةٌ "
    "معلَنة: رسمُ `CFF` يُرفَض، وصيغةُ `cmap` غيرُ الرابعة تُرفَض، وتحويلُ "
    "المقياس في المركّب يُرفَض. فهذه أرقامٌ عن خطوطٍ بنسق `glyf` لا عن الخطوط."
)

THE_MANIFEST_REFUSES_A_DRIFTED_DEPOSIT_AND_DOES_NOT_REPAIR_IT: Final[str] = (
    "THE_MANIFEST_REFUSES_A_DRIFTED_DEPOSIT_AND_DOES_NOT_REPAIR_IT: بصمةُ كلّ "
    "وديعةٍ وطولُها ورسومُها وجداولُها مجمَّدةٌ في FONT_DEPOSIT ومقروءةٌ من "
    "القرص عند كلّ تحميل. فإن زُحزح بايتٌ واحدٌ رُفض التحميلُ ولم يُصلَح ولم "
    "يُكتفَ بتحذير؛ وإعادةُ التجميد قياسٌ يُعاد لا صيانةٌ تُجرى."
)

THERE_IS_NO_SHAPING_ENGINE_HERE_ONLY_ISOLATED_GLYPHS: Final[str] = (
    "THERE_IS_NO_SHAPING_ENGINE_HERE_ONLY_ISOLATED_GLYPHS: اختيارُ الرسم بحسب "
    "السياق يقتضي `GSUB` السياقيَّ، وهو خارجَ ما تُنجزه المكتبةُ القياسيّةُ "
    "على وجهٍ يُوثَق به. فلا يُقرَأ ههنا إلّا الرسمُ المنفصل، ولا يُقارَن وضعٌ "
    "بوضع؛ وكلُّ رقمٍ ههنا عن المنفصل وحدَه، ولا يُعمَّم على أوضاع الكلمة."
)

FONT_DEPOSIT_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "A_FONT_READ_FROM_THE_SYSTEM_IS_NOT_A_DEPOSIT": (
        A_FONT_READ_FROM_THE_SYSTEM_IS_NOT_A_DEPOSIT
    ),
    "WHAT_THIS_READER_CANNOT_PARSE_IT_REFUSES_AND_DOES_NOT_GUESS": (
        WHAT_THIS_READER_CANNOT_PARSE_IT_REFUSES_AND_DOES_NOT_GUESS
    ),
    "THE_MANIFEST_REFUSES_A_DRIFTED_DEPOSIT_AND_DOES_NOT_REPAIR_IT": (
        THE_MANIFEST_REFUSES_A_DRIFTED_DEPOSIT_AND_DOES_NOT_REPAIR_IT
    ),
    "THERE_IS_NO_SHAPING_ENGINE_HERE_ONLY_ISOLATED_GLYPHS": (
        THERE_IS_NO_SHAPING_ENGINE_HERE_ONLY_ISOLATED_GLYPHS
    ),
}

_FORBIDDEN_FIELD_TOKENS: Final[tuple[str, ...]] = (
    "authority",
    "born",
    "birth",
    "gate",
    "rank",
    "verdict",
)


def _assert_no_authority_field() -> None:
    """حارسُ استيراد: لا حقلَ سلطةٍ ولا رتبةٍ في وصفِ بتاتٍ لا حكمَ فيه."""

    for described in (FontManifest, FontBits):
        for declared in fields(described):
            lowered = declared.name.lower()
            for token in _FORBIDDEN_FIELD_TOKENS:
                if token in lowered:
                    raise FontDepositError(
                        f"حقلٌ يحمل سلطةً أو رتبةً في {described.__name__}: "
                        f"{declared.name}؛ وهذه وديعةُ بتاتٍ لا سلطةَ فيها."
                    )


def _assert_the_deposit_is_present_and_unmoved() -> None:
    """حارسُ استيراد: لا تُحمَّل الوحدةُ على ودائعَ غائبةٍ أو مزحزَحة."""

    if not every_deposit_matches_its_manifest():
        raise FontDepositError(
            "وديعةُ خطٍّ غائبةٌ أو مزحزَحةٌ عن وصفها المجمَّد؛ فلا يُقرأ منها "
            "رقمٌ، ولا يُقرأ خطُّ النظام بديلًا عنها."
        )


def _assert_every_residual_is_named_by_its_key() -> None:
    """حارسُ استيراد: كلُّ بقيّةٍ تبدأ بمفتاحها فلا تُقتَبس منزوعةَ النسبة."""

    for key, text in FONT_DEPOSIT_NAMED_RESIDUALS.items():
        if not text.startswith(f"{key}: "):
            raise FontDepositError(f"بقيّةٌ لا تبدأ بمفتاحها: {key}.")


_assert_no_authority_field()
_assert_the_deposit_is_present_and_unmoved()
_assert_every_residual_is_named_by_its_key()
