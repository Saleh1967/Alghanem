r"""توسيعُ السؤال من موضعٍ إلى أربعة: العشرُ كانت خبرًا عن موضعَين لا عن الخطّ.

قاست `blind_skeleton_transport` عشرَ فئاتٍ تنتقل إلى الودائع الثلاث، وسمَّت
حدَّها صراحةً: **لا شكلَ إلّا المنفصل**
(`THERE_IS_NO_SHAPING_ENGINE_HERE_ONLY_ISOLATED_GLYPHS`). وهذه الوحدةُ توسّع
ذلك الحدَّ وحدَه: تقرأ استبدالَ `init` و`medi` و`fina` من `GSUB` فتصير الأسئلةُ
أربعةً بدل واحد. والنتيجةُ أنّ العشرَ لم تصمد.

**أوّلًا: وما يُقرأ ههنا استبدالٌ مفردٌ لا مُشكِّل.** يُقرأ من `GSUB` نوعا
البحث الأوّل (`SingleSubst`) والثاني (`MultipleSubst`) في سمات المواضع الثلاث،
ولا يُقرأ سياقٌ ولا ارتباطٌ ولا تركيب. فليس ههنا محرّكُ تشكيل، ولا يُدَّعى أنّ
الشكلَ المُستخرَج هو ما يظهر في كلمةٍ بعينها: إنّما هو **الشكلُ الذي يسمّيه
الخطُّ لذلك الموضع**. وما خرج من `MultipleSubst` بأكثرَ من رسمٍ واحدٍ **يُرفَض
ولا يُخمَّن**: خمسةٌ في أميري (١ و١ و٣) وصفرٌ في الآخرَين
(`A_NAMED_POSITION_IS_NOT_A_SHAPED_WORD`).

**وثانيًا: والتغطيةُ تنتقل انتقالًا تامًّا، والشكلُ لا ينتقل.** هذا أوضحُ ما
في الباب. ما لا تغطّيه سمةُ الموضع من نطاق العيّنة العمياء:

| السمة | أميري | شهرزاد | الكوفيّ |
|---|---|---|---|
| `init` | 18 | 18 | 18 |
| `medi` | 18 | 18 | 18 |
| `fina` | 7 | 7 | 7 |

وليست الأعدادُ وحدَها متساوية، بل **المجموعاتُ نفسُها متطابقةٌ حرفًا حرفًا**
في الثلاثة: ثمانيةَ عشرَ لا مبدأَ لها ولا وسط، وهي `ء آ أ ؤ إ ا ة د ذ ر ز ـ و`
والحركاتُ الخمس؛ وسبعةٌ لا آخِرَ لها، وهي `ء` و`ـ` والحركاتُ الخمس. وتُكتَب
الأعضاءُ مفرَّقةً لأنّها **مجموعةٌ لا نصّ**: لو رُصَّت لصار جوارُ حركتين فيها
مزدوجًا يقرؤه `pair_sample_widening` ولا وجودَ له في كتابة.
فالخطوطُ الثلاثةُ **تُجمِع إجماعًا تامًّا على أيِّ حرفٍ له أيُّ موضع**،
وتختلف اختلافًا واسعًا في **كيف يُرسَم**. فحقيقةُ الوصل خبرٌ عن الكتابة ينتقل،
وحقيقةُ الرسم خبرٌ عن الخطّ لا ينتقل إلّا بقدر
(`THE_JOINING_COVERAGE_TRANSPORTS_WHERE_THE_GEOMETRY_DOES_NOT`).

**وثالثًا: والفئاتُ المقيسةُ في المواضع الأربعة.** عدَدُها في كلّ خطٍّ وموضع:

والعددُ الأوّلُ قسمةُ العيّنة كاملةً — يدخلها الحرفُ المنفرد — والثاني ما
زاد على حرفٍ واحد، وهو وحدَه ما تنشره `blind_skeleton_transport`:

| الخطّ | `isol` | `init` | `medi` | `fina` |
|---|---|---|---|---|
| أميري | 27 / 13 | 11 / 8 | 11 / 8 | 21 / 13 |
| شهرزاد | 25 / 14 | 11 / 8 | 11 / 8 | 19 / 13 |
| الكوفيّ | 25 / 14 | 10 / 6 | 11 / 7 | 19 / 13 |

وما تحت المنفصلِ في العمود الثاني — 13 و14 و14 — هو بعينه ما قِيس من قبل،
فالوحدتان تتّفقان عند الموضع المشترك ولا تُعاد قسمةٌ بغير ما قُسمت به.

**ورابعًا: وهذا هو المِلْستون: النقلُ ينهار بتوسيع الموضع.**

| الموضع | ينتقل إلى الثلاثة |
|---|---|
| `isol` | **10** |
| `init` | **3** |
| `medi` | **4** |
| `fina` | **10** |
| **الأربعةُ جميعًا** | **2** |

فالعشرُ المنشورةُ من قبلُ صحيحةٌ ولم تُنقَض، لكنّها **خبرٌ عن موضعَين من
أربعة**: المنفصلِ والآخِر، وهما متطابقان تطابقًا تامًّا. وما يصمد في المواضع
الأربعة كلِّها **اثنتان لا غير: سش وعغ**. وأمّا **بتث** — وهي واجهةُ النتيجة
السابقة — فتسقط في المبدأ والوسط، إذ يبتلعها في النسخيَّين سِنٌّ واحدةٌ تجمع
`ئبتثؽؾؿنىي`، ويقسمها الكوفيُّ قسمةً أخرى. فالسقوطُ ليس خلافًا على ب ت ث،
بل **اتّساعُ الفئة حتّى تختلف حدودُها**
(`THE_TEN_WERE_A_FACT_ABOUT_TWO_POSITIONS_NOT_ABOUT_THE_SCRIPT`).

**وخامسًا: والتوسيعُ يُنقِص ويَزيد معًا.** ليس أثرُه تقليمًا فحسب. فئةُ **فق**
لا وجودَ لها في المنفصل ولا في الآخِر — إذ يفترق ذَيلاهما — وتنتقل إلى الودائع
الثلاث في المبدأ والوسط جميعًا. فلو لم يُوسَّع السؤالُ ما رُئيت ألبتّة. واتّحادُ
المنتقِل على المواضع الأربعة **إحدى عشرةَ** فئةً، وتقاطعُه **اثنتان**؛ وبين
العددَين تقع كلُّ دعوى
(`WIDENING_THE_QUESTION_ADDS_A_CLASS_AS_WELL_AS_REMOVING_ONE`).

**وسادسًا: ولا يُقارَن موضعٌ بموضع.** كلُّ فئةٍ ههنا مقيسةٌ **داخلَ** موضعها،
ولم يُسأل قطُّ أيتقاسم شكلُ المبدأ كنتورًا مع شكلِ المنفصل. فالعمودُ يُقرأ
ولا تُقرأ السطور، ولا يُشتقُّ من هذا الجدول قولٌ في ثبات الحرف عبر مواضعه
(`NO_CLASS_HERE_CROSSES_A_POSITION_BOUNDARY`).
"""

from __future__ import annotations

import struct
from dataclasses import dataclass, fields
from functools import cache
from typing import Final

from alghanem.arabic.blind_skeleton_transport import (
    BLIND_SAMPLE_RANGE,
    THE_DEPOSITS_READ,
    group_blindly,
)
from alghanem.arabic.font_deposit import deposit_bytes, load_font

__all__ = [
    "A_NAMED_POSITION_IS_NOT_A_SHAPED_WORD",
    "NO_CLASS_HERE_CROSSES_A_POSITION_BOUNDARY",
    "POSITIONS",
    "POSITIONAL_WIDENING_NAMED_RESIDUALS",
    "PositionalCensus",
    "PositionalWideningError",
    "THE_JOINING_COVERAGE_TRANSPORTS_WHERE_THE_GEOMETRY_DOES_NOT",
    "THE_TEN_WERE_A_FACT_ABOUT_TWO_POSITIONS_NOT_ABOUT_THE_SCRIPT",
    "WIDENING_THE_QUESTION_ADDS_A_CLASS_AS_WELL_AS_REMOVING_ONE",
    "census_at",
    "classes_that_transport_at",
    "classes_that_transport_everywhere",
    "letters_present_in",
    "letters_uncovered_by",
    "positional_classes_of",
    "positional_map",
    "positional_sample_of",
    "shared_classes_of",
    "substitutions_refused_in",
    "the_classes_only_a_wider_question_finds",
    "the_uncovered_set_is_the_same_in_every_deposit",
]

POSITIONS: Final[tuple[str, ...]] = ("isol", "init", "medi", "fina")

_SUBSTITUTED_POSITIONS: Final[tuple[str, ...]] = ("init", "medi", "fina")

_SINGLE_SUBST: Final[int] = 1
_MULTIPLE_SUBST: Final[int] = 2


class PositionalWideningError(ValueError):
    """رفضٌ عند القياس: موضعٌ لا يُعرَف، أو استبدالٌ لا يُقرأ فلا يُخمَّن."""


def _table_offsets(raw: bytes) -> dict[str, int]:
    count = struct.unpack(">H", raw[4:6])[0]
    found: dict[str, int] = {}
    for index in range(count):
        at = 12 + 16 * index
        tag = raw[at : at + 4].decode("latin-1")
        found[tag] = struct.unpack(">I", raw[at + 8 : at + 12])[0]
    return found


def _coverage(raw: bytes, at: int) -> tuple[int, ...]:
    shape, count = struct.unpack(">HH", raw[at : at + 4])
    if shape == 1:
        return struct.unpack(f">{count}H", raw[at + 4 : at + 4 + 2 * count])
    if shape != 2:
        raise PositionalWideningError(f"صيغةُ تغطيةٍ لا تُقرأ: {shape}؛ ولا تُخمَّن.")
    spread: list[int] = []
    for index in range(count):
        start, end, _ = struct.unpack(
            ">HHH", raw[at + 4 + 6 * index : at + 10 + 6 * index]
        )
        spread.extend(range(start, end + 1))
    return tuple(spread)


def _lookups_for(raw: bytes, gsub: int, feature: str) -> tuple[int, ...]:
    features = gsub + struct.unpack(">H", raw[gsub + 6 : gsub + 8])[0]
    count = struct.unpack(">H", raw[features : features + 2])[0]
    found: list[int] = []
    for index in range(count):
        at = features + 2 + 6 * index
        if raw[at : at + 4].decode("latin-1") != feature:
            continue
        table = features + struct.unpack(">H", raw[at + 4 : at + 6])[0]
        total = struct.unpack(">H", raw[table + 2 : table + 4])[0]
        found.extend(
            struct.unpack(f">{total}H", raw[table + 4 : table + 4 + 2 * total])
        )
    return tuple(sorted(set(found)))


def _subtables(raw: bytes, gsub: int, index: int) -> tuple[int, tuple[int, ...]]:
    lookups = gsub + struct.unpack(">H", raw[gsub + 8 : gsub + 10])[0]
    at = (
        lookups
        + struct.unpack(">H", raw[lookups + 2 + 2 * index : lookups + 4 + 2 * index])[0]
    )
    kind, _flag, count = struct.unpack(">HHH", raw[at : at + 6])
    offsets = struct.unpack(f">{count}H", raw[at + 6 : at + 6 + 2 * count])
    return kind, tuple(at + offset for offset in offsets)


def _read_feature(filename: str, feature: str) -> tuple[dict[int, int], int]:
    raw = deposit_bytes(filename)
    offsets = _table_offsets(raw)
    if "GSUB" not in offsets:
        raise PositionalWideningError(f"لا جدولَ GSUB في {filename}؛ فلا مواضعَ تُقرأ.")
    gsub = offsets["GSUB"]
    substituted: dict[int, int] = {}
    refused = 0
    for index in _lookups_for(raw, gsub, feature):
        kind, subtables = _subtables(raw, gsub, index)
        if kind not in (_SINGLE_SUBST, _MULTIPLE_SUBST):
            raise PositionalWideningError(
                f"نوعُ بحثٍ لا يُقرأ ههنا: {kind}؛ وهذه قراءةُ استبدالٍ مفردٍ لا مُشكِّل."
            )
        for subtable in subtables:
            shape = struct.unpack(">H", raw[subtable : subtable + 2])[0]
            covered = _coverage(
                raw, subtable + struct.unpack(">H", raw[subtable + 2 : subtable + 4])[0]
            )
            if kind == _SINGLE_SUBST and shape == 1:
                delta = struct.unpack(">h", raw[subtable + 4 : subtable + 6])[0]
                for glyph in covered:
                    substituted.setdefault(glyph, (glyph + delta) & 0xFFFF)
                continue
            if kind == _SINGLE_SUBST:
                total = struct.unpack(">H", raw[subtable + 4 : subtable + 6])[0]
                targets = struct.unpack(
                    f">{total}H", raw[subtable + 6 : subtable + 6 + 2 * total]
                )
                for place, glyph in enumerate(covered):
                    substituted.setdefault(glyph, targets[place])
                continue
            for place, glyph in enumerate(covered):
                sequence = (
                    subtable
                    + struct.unpack(
                        ">H", raw[subtable + 6 + 2 * place : subtable + 8 + 2 * place]
                    )[0]
                )
                total = struct.unpack(">H", raw[sequence : sequence + 2])[0]
                if total != 1:
                    refused += 1
                    continue
                substituted.setdefault(
                    glyph, struct.unpack(">H", raw[sequence + 2 : sequence + 4])[0]
                )
    return substituted, refused


@cache
def positional_map(filename: str, position: str) -> dict[int, int]:
    """خريطةُ رسمٍ إلى رسمٍ كما تسمّيها سمةُ الموضع، رسمًا واحدًا لا غير."""

    if position not in _SUBSTITUTED_POSITIONS:
        raise PositionalWideningError(
            f"موضعٌ لا استبدالَ له: {position}؛ والمنفصلُ يُقرأ من `cmap` لا من `GSUB`."
        )
    return dict(_read_feature(filename, position)[0])


@cache
def substitutions_refused_in(filename: str, position: str) -> int:
    """كم استبدالًا أخرج أكثرَ من رسمٍ فرُفض؟ ويُنشَر العددُ ولا يُطوى."""

    if position not in _SUBSTITUTED_POSITIONS:
        raise PositionalWideningError(f"موضعٌ لا استبدالَ له: {position}.")
    return _read_feature(filename, position)[1]


@cache
def letters_present_in(filename: str) -> tuple[str, ...]:
    """حروفُ العيّنة العمياء التي للخطّ رسمٌ لها، مرتَّبةً بترميزها."""

    font = load_font(filename)
    low, high = BLIND_SAMPLE_RANGE
    return tuple(
        chr(code) for code in range(low, high + 1) if font.glyph_for(chr(code)) != 0
    )


@cache
def letters_uncovered_by(filename: str, position: str) -> frozenset[str]:
    """ما لا تغطّيه سمةُ الموضع من حروف الخطّ؛ وهو خبرُ الوصل لا خبرُ الرسم."""

    substituted = positional_map(filename, position)
    font = load_font(filename)
    return frozenset(
        letter
        for letter in letters_present_in(filename)
        if font.glyph_for(letter) not in substituted
    )


def the_uncovered_set_is_the_same_in_every_deposit(position: str) -> bool:
    """أتُجمِع الودائعُ الثلاثُ على **أيِّ** حرفٍ له هذا الموضع؟"""

    seen = {letters_uncovered_by(filename, position) for filename in THE_DEPOSITS_READ}
    return len(seen) == 1


def positional_sample_of(filename: str, position: str) -> tuple[int, ...]:
    """أرقامُ رسومِ الحروف في موضعٍ، معتمةً كما تقتضي دعوى العمى."""

    if position not in POSITIONS:
        raise PositionalWideningError(f"موضعٌ لا يُعرَف: {position}.")
    font = load_font(filename)
    if position == "isol":
        found = {font.glyph_for(letter) for letter in letters_present_in(filename)}
    else:
        substituted = positional_map(filename, position)
        found = {
            substituted[glyph]
            for letter in letters_present_in(filename)
            if (glyph := font.glyph_for(letter)) in substituted
        }
    if not found:
        raise PositionalWideningError(
            f"لا رسمَ في موضع {position} من {filename}؛ ولا عيّنةَ تُقاس."
        )
    return tuple(sorted(found))


def _letters_behind(filename: str, position: str) -> dict[int, str]:
    font = load_font(filename)
    behind: dict[int, str] = {}
    substituted = None if position == "isol" else positional_map(filename, position)
    for letter in letters_present_in(filename):
        glyph = font.glyph_for(letter)
        if substituted is None:
            behind.setdefault(glyph, letter)
        elif glyph in substituted:
            behind.setdefault(substituted[glyph], letter)
    return behind


@cache
def positional_classes_of(filename: str, position: str) -> tuple[frozenset[str], ...]:
    """فئاتُ خطٍّ في موضعٍ، مجموعةً عمياءَ ثمّ مفتوحةً على الحروف."""

    sample = positional_sample_of(filename, position)
    behind = _letters_behind(filename, position)
    grouped = group_blindly(filename, sample)
    opened = {
        frozenset(behind[glyph] for glyph in members if glyph in behind)
        for members in grouped
    }
    return tuple(
        sorted(
            (letters for letters in opened if letters),
            key=lambda letters: (-len(letters), sorted(letters)),
        )
    )


def shared_classes_of(filename: str, position: str) -> tuple[frozenset[str], ...]:
    """ما زاد على حرفٍ واحدٍ من فئات موضعٍ؛ وهي وحدَها ما يُسأل عن نقله."""

    return tuple(
        letters
        for letters in positional_classes_of(filename, position)
        if len(letters) > 1
    )


def classes_that_transport_at(
    position: str, filenames: tuple[str, ...] = THE_DEPOSITS_READ
) -> tuple[frozenset[str], ...]:
    """الفئاتُ التي تصحّ في كلّ وديعةٍ **داخلَ** موضعٍ واحد."""

    if len(filenames) < 2:
        raise PositionalWideningError("النقلُ لا يُقاس على وديعةٍ واحدة؛ فلا مقابلَ لها.")
    shared = set(shared_classes_of(filenames[0], position))
    for filename in filenames[1:]:
        shared &= set(shared_classes_of(filename, position))
    return tuple(
        sorted(
            (letters for letters in shared if len(letters) > 1),
            key=lambda letters: (-len(letters), sorted(letters)),
        )
    )


def classes_that_transport_everywhere() -> tuple[frozenset[str], ...]:
    """ما يصمد في الودائع الثلاث وفي المواضع الأربعة جميعًا."""

    shared = set(classes_that_transport_at(POSITIONS[0]))
    for position in POSITIONS[1:]:
        shared &= set(classes_that_transport_at(position))
    return tuple(sorted(shared, key=lambda letters: (-len(letters), sorted(letters))))


def the_classes_only_a_wider_question_finds() -> tuple[frozenset[str], ...]:
    """ما لا يُرى في المنفصل ألبتّة ويَنتقل في موضعٍ موصول."""

    isolated = set(classes_that_transport_at("isol"))
    widened: set[frozenset[str]] = set()
    for position in _SUBSTITUTED_POSITIONS:
        widened |= set(classes_that_transport_at(position))
    return tuple(
        sorted(widened - isolated, key=lambda letters: (-len(letters), sorted(letters)))
    )


@dataclass(frozen=True, slots=True)
class PositionalCensus:
    """تعدادُ موضعٍ في وديعة: كم حرفًا له شكلٌ، وكم فئةً أخرجت هندستُه."""

    filename: str
    position: str
    covered: int
    classes: int
    shared: int

    def __post_init__(self) -> None:
        if self.position not in POSITIONS:
            raise PositionalWideningError(f"موضعٌ لا يُعرَف: {self.position}.")
        if self.covered < 1:
            raise PositionalWideningError(
                f"موضعٌ بلا حرفٍ مُغطًّى: {self.filename}/{self.position}."
            )
        if not 1 <= self.classes <= self.covered:
            raise PositionalWideningError(
                "عددُ الفئات لا يقع بين الواحد وعدد المُغطّى: "
                f"{self.classes} من {self.covered}."
            )
        if not 0 <= self.shared <= self.classes:
            raise PositionalWideningError(
                "عددُ الفئات المتقاسَمة لا يقع بين الصفر وعدد الفئات: "
                f"{self.shared} من {self.classes}."
            )


def census_at(filename: str, position: str) -> PositionalCensus:
    """يقرأ تعدادَ موضعٍ من البتات عند القراءة، لا من رقمٍ محفوظ."""

    return PositionalCensus(
        filename=filename,
        position=position,
        covered=len(positional_sample_of(filename, position)),
        classes=len(positional_classes_of(filename, position)),
        shared=len(shared_classes_of(filename, position)),
    )


A_NAMED_POSITION_IS_NOT_A_SHAPED_WORD: Final[str] = (
    "A_NAMED_POSITION_IS_NOT_A_SHAPED_WORD: يُقرأ ههنا استبدالُ `GSUB` المفردُ "
    "لسمات `init` و`medi` و`fina` وحدَها، ولا يُقرأ سياقٌ ولا ارتباطٌ ولا تركيب. "
    "فالشكلُ المُستخرَج هو ما **يسمّيه الخطُّ** لذلك الموضع، لا ما يظهر في كلمةٍ "
    "بعينها؛ وبين الاثنين قواعدُ وصلٍ ومزجٍ لم تُقرأ. وما أخرج أكثرَ من رسمٍ "
    "واحدٍ رُفض ولم يُخمَّن: خمسةٌ في أميري وصفرٌ في الآخرَين."
)

THE_JOINING_COVERAGE_TRANSPORTS_WHERE_THE_GEOMETRY_DOES_NOT: Final[str] = (
    "THE_JOINING_COVERAGE_TRANSPORTS_WHERE_THE_GEOMETRY_DOES_NOT: الودائعُ الثلاثُ "
    "تُجمِع إجماعًا تامًّا على أيِّ حرفٍ له أيُّ موضع — ثمانيةَ عشرَ بلا مبدأٍ "
    "ولا وسط، وسبعةً بلا آخِر، والمجموعاتُ متطابقةٌ حرفًا حرفًا لا عددًا فحسب — "
    "وتختلف اختلافًا واسعًا في كيف يُرسَم كلُّ شكل. فالتغطيةُ خبرٌ عن الكتابة "
    "ينتقل، والهندسةُ خبرٌ عن الخطّ لا ينتقل إلّا بقدر. ولا يُقرأ من التطابق "
    "أنّه قانونُ الخطّ العربيّ: ثلاثُ ودائعَ تتبع جدولَ يونيكود نفسَه."
)

THE_TEN_WERE_A_FACT_ABOUT_TWO_POSITIONS_NOT_ABOUT_THE_SCRIPT: Final[str] = (
    "THE_TEN_WERE_A_FACT_ABOUT_TWO_POSITIONS_NOT_ABOUT_THE_SCRIPT: العشرُ "
    "المنشورةُ في `blind_skeleton_transport` صحيحةٌ ولم تُنقَض، لكنّها خبرٌ عن "
    "المنفصل والآخِر وهما متطابقان، لا عن المواضع الأربعة. فالنقلُ ثلاثٌ في "
    "المبدأ وأربعٌ في الوسط، والصامدُ في الأربعة جميعًا **اثنتان: سش وعغ**. "
    "وتسقط بتث في المبدأ والوسط لا خلافًا عليها بل لاتّساع فئتها حتّى تختلف "
    "حدودُها: سِنٌّ تجمع عشرةً في النسخيَّين، وقسمةٌ أخرى في الكوفيّ."
)

WIDENING_THE_QUESTION_ADDS_A_CLASS_AS_WELL_AS_REMOVING_ONE: Final[str] = (
    "WIDENING_THE_QUESTION_ADDS_A_CLASS_AS_WELL_AS_REMOVING_ONE: ليس أثرُ "
    "التوسيع تقليمًا فحسب. فئةُ **فق** لا وجودَ لها في المنفصل ولا في الآخِر — "
    "إذ يفترق ذَيلاهما — وتنتقل إلى الثلاث في المبدأ والوسط جميعًا؛ فلولا "
    "التوسيعُ ما رُئيت. واتّحادُ المنتقِل على المواضع إحدى عشرةَ فئةً وتقاطعُه "
    "اثنتان، وبين العددَين تقع كلُّ دعوى؛ فليُذكَر أيُّهما يُقصَد."
)

NO_CLASS_HERE_CROSSES_A_POSITION_BOUNDARY: Final[str] = (
    "NO_CLASS_HERE_CROSSES_A_POSITION_BOUNDARY: كلُّ فئةٍ مقيسةٌ **داخلَ** موضعها، "
    "ولم يُسأل قطُّ أيتقاسم شكلُ المبدأ كنتورًا مع شكل المنفصل. فالعمودُ يُقرأ "
    "ولا تُقرأ السطور، ولا يُشتقُّ من هذا الجدول قولٌ في ثبات الحرف عبر مواضعه "
    "ولا في كون المواضع الأربعة صورًا لشيءٍ واحد."
)

POSITIONAL_WIDENING_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "A_NAMED_POSITION_IS_NOT_A_SHAPED_WORD": A_NAMED_POSITION_IS_NOT_A_SHAPED_WORD,
    "THE_JOINING_COVERAGE_TRANSPORTS_WHERE_THE_GEOMETRY_DOES_NOT": (
        THE_JOINING_COVERAGE_TRANSPORTS_WHERE_THE_GEOMETRY_DOES_NOT
    ),
    "THE_TEN_WERE_A_FACT_ABOUT_TWO_POSITIONS_NOT_ABOUT_THE_SCRIPT": (
        THE_TEN_WERE_A_FACT_ABOUT_TWO_POSITIONS_NOT_ABOUT_THE_SCRIPT
    ),
    "WIDENING_THE_QUESTION_ADDS_A_CLASS_AS_WELL_AS_REMOVING_ONE": (
        WIDENING_THE_QUESTION_ADDS_A_CLASS_AS_WELL_AS_REMOVING_ONE
    ),
    "NO_CLASS_HERE_CROSSES_A_POSITION_BOUNDARY": (
        NO_CLASS_HERE_CROSSES_A_POSITION_BOUNDARY
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
    """حارسُ استيراد: لا حقلَ سلطةٍ ولا رتبةٍ في قياسٍ لا سلطةَ فيه."""

    for declared in fields(PositionalCensus):
        lowered = declared.name.lower()
        for token in _FORBIDDEN_FIELD_TOKENS:
            if token in lowered:
                raise PositionalWideningError(
                    f"حقلٌ يحمل سلطةً أو رتبةً في PositionalCensus: {declared.name}."
                )


def _assert_the_sample_stays_blind() -> None:
    """حارسُ استيراد: لو خرج من العيّنة حرفٌ لبطل العمى الموروثُ عن الوحدة الأمّ."""

    if positional_sample_of.__annotations__.get("return") != "tuple[int, ...]":
        raise PositionalWideningError(
            "عيّنةُ الموضع تُخرِج غيرَ أرقامٍ معتمة؛ فدعوى العمى باطلة."
        )


def _assert_the_widening_costs_and_pays() -> None:
    """حارسُ استيراد: الوحدةُ قائمةٌ على انهيارٍ وزيادةٍ، فيُقاسان لا يُفترَضان."""

    isolated = len(classes_that_transport_at("isol"))
    everywhere = len(classes_that_transport_everywhere())
    if everywhere >= isolated:
        raise PositionalWideningError(
            "لم ينهَر النقلُ بتوسيع الموضع؛ فالدعوى التي بُنيت عليها الوحدةُ "
            "لم تقع، ويُعاد النظرُ فيها كلِّها."
        )
    if not the_classes_only_a_wider_question_finds():
        raise PositionalWideningError(
            "لم يُضِف التوسيعُ فئةً؛ فنصفُ المقابلة ساقط، ولا يُنشَر نصفُها."
        )


def _assert_the_coverage_agrees_where_the_shape_does_not() -> None:
    """حارسُ استيراد: إجماعُ التغطية مقيسٌ في كلّ موضعٍ لا مأخوذٌ تسليمًا."""

    for position in _SUBSTITUTED_POSITIONS:
        if not the_uncovered_set_is_the_same_in_every_deposit(position):
            raise PositionalWideningError(
                f"اختلفت الودائعُ في تغطية {position}؛ فدعوى الإجماع ساقطة."
            )


def _assert_every_residual_is_named_by_its_key() -> None:
    """حارسُ استيراد: كلُّ بقيّةٍ تبدأ بمفتاحها فلا تُقتَبس منزوعةَ النسبة."""

    for key, text in POSITIONAL_WIDENING_NAMED_RESIDUALS.items():
        if not text.startswith(f"{key}: "):
            raise PositionalWideningError(f"بقيّةٌ لا تبدأ بمفتاحها: {key}.")


_assert_no_authority_field()
_assert_the_sample_stays_blind()
_assert_the_widening_costs_and_pays()
_assert_the_coverage_agrees_where_the_shape_does_not()
_assert_every_residual_is_named_by_its_key()
