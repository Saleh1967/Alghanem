"""جسرُ المبنيّات: توليدٌ واسترجاعٌ بثلاثة أجناس، مقيسًا على مرجعٍ بشريٍّ مستقلّ.

## المرجعُ المستقلّ

المرجعُ ‎R‎ وسمُ MASAQ البشريّ المودَع في `corpora/MASAQ.csv`: كلُّ قطعةٍ (سابقة،
جذع، لاحقة) فيها عمودُ `Invariable_Declinable`. والمبنيُّ ما كان وسمُه في
`MABNI_LABELS` (مجمَّدةً قبل القياس). ولا يُعرَّف المبنيُّ هنا بما يقبله النظام.

## الأجناسُ الثلاثة — والقسمةُ مقيسةٌ لا مفترضة

المبنيُّ في العربيّة ليس جنسًا واحدًا، وهذا يظهر بالقياس:

* **معجميٌّ مغلق** (`LEXICAL`): الحروفُ والضمائرُ والإشارةُ والموصولُ وأسماءُ
  الشرط والاستفهام والظروفُ المبنيّة وأسماءُ الأفعال والأفعالُ الجامدة. هو قائمةٌ
  بالوضع (نقل). وعلامةُ انغلاقه مقيسة: قائمةٌ من السور الزوجيّة تغطّي وقوعاتِ
  السور الفرديّة كلَّها تقريبًا (`closedness_readings`).
* **صرفيٌّ منتِج** (`MORPHOLOGICAL`): الماضي والأمرُ والمضارعُ المتّصلُ بنونٍ. لا
  يُحصى بقائمة، بل يُولَّد من جذرٍ ووزن: `mabni_verbs.verb_forms` يولِّده من كلّ
  جذرٍ في «مقاييس اللغة» بالصحيح والمهموز والمضاعف والأجوف والناقص والمثال، وفي
  الأوزان كلّها، ويُسترجَع بعكس التوليد (`recover_verb`).
* **موضعيٌّ تركيبيّ** (`POSITIONAL`): اسمٌ مُعرَبٌ في أصله يُبنى بموضعه (المنادى
  المفرد العلم، اسمُ «لا» النافية للجنس). لا يُعرَف من الكلمة وحدها بل من
  التركيب (الطبقة ٥)، فلا يُولَّد ولا يُسترجَع هنا، ويُعَدّ باسمه.

## التوليدُ إلى الـ116 والاسترجاعُ منها

كلُّ جذعٍ معجميٍّ وكلُّ فعلٍ مولَّدٍ يُمرَّر على الجسر (البروتوكول 1.1) في الابتداء
مع الاستمرار ومع الوقف، فيخرج سلسلةً من الـ116 أو تعليقًا مسمّى. ثمّ تُبنى ألياف:
الصورُ التي تقع على سلسلةٍ واحدة، مرتّبةً، فيُسترجَع الرسمُ من ‎(الذرّات، الرتبة)‎
(`A116/Fiber.lean`: `decode_encode`). والألياف ذاتُ العضوين فأكثر هي المبنيّاتُ
المتّحدةُ النطق المختلفةُ الرسم.

## ما لا يدّعيه

ليس القائمةُ المعجميّةُ نقلًا عن كتاب نحو، بل عن وسمٍ بشريٍّ لمتنٍ واحد؛ فما لم
يقع في القرآن لا يدخلها. ولا يُولَّد المزيدُ ولا المعتلُّ ولا المضاعفُ ولا المهموز
بعد (يُعَدّ كلٌّ باسمه). وبابُ الفعل المسترجَع مرصودٌ من السطح لا منقولٌ عن معجم.
"""

from __future__ import annotations

import csv
import itertools
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Any, Final

__all__ = [
    "MABNI_LABELS",
    "MabniGenus",
    "MabniSegment",
    "ClosednessReading",
    "VerbAnalysis",
    "VerbOutcome",
    "genus_of",
    "masaq_words",
    "mabni_segments",
    "closedness_readings",
    "lexical_inventory",
    "project_form",
    "fibers_of",
    "verb_tokens",
    "recover_verb",
    "verb_readings",
    "verb_generation_reading",
    "lexical_generation_reading",
    "wasl_start_vowel",
    "lexical_recognition_reading",
    "report",
]

_ROOT = Path(__file__).resolve().parents[1]
MASAQ_PATH: Final[Path] = _ROOT / "corpora" / "MASAQ.csv"

MABNI_LABELS: Final[frozenset[str]] = frozenset(
    {
        "مبني",
        "ضمير متصل",
        "ضمير منفصل مبني",
        "اسم موصول",
        "اسم إشارة",
        "اسم شرط",
        "اسم استفهام",
        "ضمير فصل",
        "كافة ومكفوفة",
        "اسم عدد مركب مبني",
        "ال التعريف",
    }
)
"""قيمُ `Invariable_Declinable` التي تعني «مبنيّ» في MASAQ؛ مجمَّدةٌ قبل القياس."""

FATHA, DAMMA, KASRA, SUKUN, SHADDA = "َ", "ُ", "ِ", "ْ", "ّ"
_MARKS: Final[frozenset[str]] = frozenset(
    {FATHA, DAMMA, KASRA, SUKUN, SHADDA, "ً", "ٌ", "ٍ"}
)


class MabniGenus(Enum):
    LEXICAL = "معجميّ مغلق: قائمةٌ بالوضع"
    MORPHOLOGICAL = "صرفيّ منتِج: يولَّد من جذرٍ ووزن"
    POSITIONAL = "موضعيّ: اسمٌ يُبنى بموضعه في التركيب"


_MORPHOLOGICAL_TAGS: Final[frozenset[str]] = frozenset(
    {"PV", "PV_PASS", "CV", "IV", "IV_PASS", "CV_PREF", "NOON_V5", "EMPHATIC_NUN"}
)
_POSITIONAL_PREFIXES: Final[tuple[str, ...]] = ("NOUN", "ADJ", "GERUND")


def genus_of(tag: str) -> MabniGenus:
    """الجنسُ من وسم الصرف وحده؛ والقاعدةُ معلنةٌ قبل القياس."""

    if tag in _MORPHOLOGICAL_TAGS:
        return MabniGenus.MORPHOLOGICAL
    if tag.startswith(_POSITIONAL_PREFIXES) and tag != "NOUN_VERB_LIKE":
        return MabniGenus.POSITIONAL
    return MabniGenus.LEXICAL


# --- قراءةُ MASAQ ومحاذاةُ القطع بالشكل --------------------------------------


@dataclass(frozen=True)
class MabniSegment:
    sura: int
    verse: int
    word: str
    index: int
    morph_type: str
    tag: str
    label: str
    role: str
    bare: str
    vocalized: str
    genus: MabniGenus


def _clusters(text: str) -> list[str]:
    out: list[str] = []
    for ch in unicodedata.normalize("NFC", text):
        if unicodedata.category(ch) == "Mn" and out:
            out[-1] += ch
        else:
            out.append(ch)
    return out


def align(word: str, pieces: list[str]) -> list[str] | None:
    """يقسم الكلمةَ المشكولةَ على قطعها غيرِ المشكولة؛ ولا يُحاذي ما تغيّر رسمُه."""

    clusters = _clusters(word)
    out: list[str] = []
    i = 0
    for piece in pieces:
        part = clusters[i : i + len(piece)]
        if "".join(c[0] for c in part) != piece:
            return None
        out.append("".join(part))
        i += len(piece)
    return out if i == len(clusters) else None


@lru_cache(maxsize=1)
def masaq_words() -> tuple[tuple[dict[str, str], ...], ...]:
    """كلماتُ MASAQ: صفوفٌ متتاليةٌ لها السورةُ والآيةُ وموضعُ الكلمة نفسُها."""

    with MASAQ_PATH.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    def key(row: dict[str, str]) -> tuple[str, str, str, str]:
        return row["Sura_No"], row["Verse_No"], row["Column5"], row["Word"]

    return tuple(tuple(group) for _, group in itertools.groupby(rows, key=key))


def _real(row: dict[str, str]) -> bool:
    return row["Segmented_Word"] not in ("(null)", "None", "")


@lru_cache(maxsize=1)
def mabni_segments() -> tuple[tuple[MabniSegment, ...], Counter[str]]:
    """القطعُ المبنيّةُ بشكلها، وعدُّ ما لم يُحاذَ باسمه."""

    out: list[MabniSegment] = []
    stats: Counter[str] = Counter()
    for group in masaq_words():
        stats["words"] += 1
        segs = [row for row in group if _real(row)]
        vocalized = align(group[0]["Word"], [row["Segmented_Word"] for row in segs])
        if vocalized is None:
            stats["UNDERLYING_SEGMENTATION_NOT_ALIGNED"] += 1
            stats["mabni_in_unaligned"] += sum(
                row["Invariable_Declinable"] in MABNI_LABELS for row in segs
            )
            continue
        for index, (row, piece) in enumerate(zip(segs, vocalized, strict=True)):
            if row["Invariable_Declinable"] not in MABNI_LABELS:
                continue
            out.append(
                MabniSegment(
                    int(row["Sura_No"]),
                    int(row["Verse_No"]),
                    group[0]["Word"],
                    index,
                    row["Morph_type"],
                    row["Morph_tag"],
                    row["Invariable_Declinable"],
                    row["Syntactic_Role"],
                    row["Segmented_Word"],
                    piece,
                    genus_of(row["Morph_tag"]),
                )
            )
    stats["mabni_segments"] = len(out)
    return tuple(out), stats


# --- الانغلاق: قائمةٌ من نصف المتن تغطّي النصفَ الآخر؟ ------------------------


@dataclass(frozen=True)
class ClosednessReading:
    genus: MabniGenus
    train_types: int
    test_types: int
    test_types_covered: int
    test_tokens: int
    test_tokens_covered: int
    unseen: tuple[tuple[str, str, int], ...]

    @property
    def token_coverage(self) -> float:
        return self.test_tokens_covered / self.test_tokens if self.test_tokens else 0.0

    @property
    def type_coverage(self) -> float:
        return self.test_types_covered / self.test_types if self.test_types else 0.0


def _train(segment: MabniSegment) -> bool:
    """القسمةُ بزوجيّة رقم السورة: قاعدةٌ لا علاقةَ لها بالجواب، مجمَّدة."""

    return segment.sura % 2 == 0


def closedness_readings() -> tuple[ClosednessReading, ...]:
    segments, _ = mabni_segments()
    out = []
    for genus in MabniGenus:
        pool = [s for s in segments if s.genus is genus and s.morph_type == "Stem"]
        train = {(s.tag, s.bare) for s in pool if _train(s)}
        test = [s for s in pool if not _train(s)]
        test_types = {(s.tag, s.bare) for s in test}
        unseen = Counter((s.tag, s.bare) for s in test if (s.tag, s.bare) not in train)
        out.append(
            ClosednessReading(
                genus,
                len(train),
                len(test_types),
                len(test_types & train),
                len(test),
                sum((s.tag, s.bare) in train for s in test),
                tuple((t, b, n) for (t, b), n in unseen.most_common()),
            )
        )
    return tuple(out)


def lexical_inventory(
    train_only: bool = False,
) -> dict[tuple[str, str], Counter[str]]:
    """القائمةُ المعجميّة: ‎(الجنس الصرفيّ، المفرد بلا شكل)‎ ← صورُه المشكولةُ بعددها."""

    segments, _ = mabni_segments()
    inventory: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    for s in segments:
        if s.genus is not MabniGenus.LEXICAL:
            continue
        if train_only and not _train(s):
            continue
        inventory[(s.morph_type, s.bare)][s.vocalized] += 1
    return dict(inventory)


# --- التوليدُ إلى الـ116 والليف ------------------------------------------------


CONTEXTS: Final[dict[str, dict[str, dict[str, str]]]] = {
    "start_continue": {"0": {"entry": "start", "exit": "continue"}},
    "start_pause": {"0": {"entry": "start", "exit": "pause"}},
}


def wasl_start_vowel(form: str) -> str | None:
    """حركةُ الابتداء بهمزة وصلٍ في فعلٍ مولَّد: ضمٌّ إن ضُمّ ثالثُه، وإلا كسر (نقل).

    تُعَدّ الحروفُ بفكّ الشدّة حرفين (‎اُتُّبِعَ‎: ا ت ت ب، فالثالثُ تاءٌ مضمومة).
    ولا يُعيدها إلا لصورةٍ تبدأ بألفٍ عاريةٍ يليها ساكنٌ أو مشدَّد.
    """

    letters: list[str] = []
    marks: list[str] = []
    for cluster in _clusters(unicodedata.normalize("NFD", form)):
        base, rest = cluster[0], cluster[1:]
        if SHADDA in rest:
            letters += [base, base]
            marks += [SUKUN, rest.replace(SHADDA, "")]
        else:
            letters.append(base)
            marks.append(rest)
    if len(letters) < 3 or letters[0] != "ا" or marks[0]:
        return None
    if marks[1] != SUKUN:
        return None
    return DAMMA if DAMMA in marks[2] else KASRA


def _starts_with_definite_article(form: str) -> bool:
    """«ال» في أوّل اسمٍ مبنيٍّ معجميّ: ألفٌ عاريةٌ ثمّ لامٌ ساكنةٌ أو مشدَّدة.

    ولا تُعَدّ لامٌ بلا علامة (فواتحُ السور: الم، الر تُقرأ بأسماء الحروف).
    """

    clusters = _clusters(unicodedata.normalize("NFD", form))
    if len(clusters) < 3 or clusters[0] != "ا" or clusters[1][0] != "ل":
        return False
    marks = clusters[1][1:]
    return SUKUN in marks or SHADDA in marks


def project_form(
    form: str, context: str, generated: bool = False, lexical: bool = False
) -> tuple[str, tuple[str, ...] | str]:
    """صورةٌ قائمةٌ بنفسها ← ‎(الحال، الذرّات أو سببُ التعليق)‎ على الجسر 1.1.

    وألفُ الوصل في أوّل صورةٍ مولَّدة تُورَّد للجسر بحركة ابتدائها ودليلِها
    (`wasl_start_vowel`)، لأنّ المولِّدَ يعرف قالبَها؛ ولا تُورَّد لغير المولَّد.
    """

    from gate.bridge import bridge

    notes: dict[str, dict[str, str]] = {}
    vowel = wasl_start_vowel(form) if generated else None
    if lexical and _starts_with_definite_article(form):
        vowel = FATHA
    if vowel is not None:
        notes["0"] = {
            "role": "WASL",
            "start_vowel": vowel,
            "evidence": "همزةُ وصلٍ في قالبٍ مولَّد: تُضمّ إن ضُمّ الثالث وإلا تُكسر"
            if generated
            else "همزةُ وصل «ال» تُفتح في الابتداء",
        }
    clusters = _clusters(unicodedata.normalize("NFD", form))
    if generated or lexical:
        for k in range(1, len(clusters)):
            letter, previous = clusters[k], clusters[k - 1]
            madd = (letter == "و" and DAMMA in previous) or (
                letter == "ي" and KASRA in previous
            )
            # في المعجميّ لا يُعَدّ مدًّا إلا الطرف (فِي، الَّذِي)؛ فواوُ «أُولَئِكَ» الوسطى
            # رسمٌ لا يُنطق، والجسرُ لا دورَ فيه لواوٍ صامتة، فيبقى معلَّقًا.
            if madd and lexical and k != len(clusters) - 1:
                madd = False
            if madd:
                notes[str(k)] = {
                    "state": SUKUN,
                    "evidence": "حرفُ مدٍّ في قالبٍ مولَّد: واوٌ بعد ضمٍّ أو ياءٌ بعد كسر",
                }
            silent = previous[0] == "و" and not set(previous[1:]) & {
                FATHA,
                DAMMA,
                KASRA,
            }
            if letter == "ا" and k == len(clusters) - 1 and silent:
                notes[str(k)] = {
                    "role": "SILENT_SUPPORT",
                    "evidence": "الألفُ الفارقةُ بعد واو الجماعة في قالبٍ مولَّد: لا تُنطق",
                }
    annotations = {"0": notes} if notes else None
    record: dict[str, Any] = bridge(
        form, contexts=CONTEXTS[context], annotations=annotations
    )
    if record["status"] == "READY":
        return "READY", tuple(record["canonical_atoms"])
    reasons = [r["reason"] for r in record["deferrals"] + record["rejections"]]
    return record["status"], reasons[0] if reasons else "NO_REASON"


def fibers_of(
    forms: list[str], context: str, generated: bool = False, lexical: bool = False
) -> tuple[dict[tuple[str, ...], tuple[str, ...]], Counter[str]]:
    """الألياف: الصورُ الجاهزةُ المجموعةُ بذرّاتها، مرتّبةً ببايتات UTF-8."""

    fibers: dict[tuple[str, ...], list[str]] = defaultdict(list)
    outcomes: Counter[str] = Counter()
    for form in sorted(set(forms), key=lambda f: f.encode("utf-8")):
        status, value = project_form(form, context, generated, lexical)
        if status == "READY" and isinstance(value, tuple):
            fibers[value].append(form)
            outcomes["READY"] += 1
        else:
            outcomes[f"{status}:{value}"] += 1
    return {k: tuple(v) for k, v in fibers.items()}, outcomes


# --- الصرفيُّ المنتِج: الأفعالُ المبنيّة (التوليدُ في `mabni_verbs`) ---------------


class VerbOutcome(Enum):
    RECOVERED = "الصورةُ مولَّدةٌ من جذرٍ في المقاييس: استُرجع جذرُها ووزنُها وإسنادُها"
    NOT_GENERATED = "لا جذرَ في المقاييس يولِّد هذه الصورةَ بالقواعد المعلنة"


@dataclass(frozen=True)
class VerbAnalysis:
    root: str
    kind: str
    form: str
    person: str


def recover_verb(
    surface: str, before_object: bool = False
) -> tuple[VerbOutcome, tuple[VerbAnalysis, ...]]:
    """عكسُ التوليد: الصورةُ المطبَّعةُ في الفهرس المعكوس ← تحليلاتُها كلُّها."""

    from .mabni_verbs import normalize, verb_index

    found = verb_index(before_object).get(normalize(surface), ())
    if not found:
        return VerbOutcome.NOT_GENERATED, ()
    return VerbOutcome.RECOVERED, tuple(VerbAnalysis(*a) for a in found)


_SUBJECT_TAGS: Final[tuple[str, ...]] = ("SUBJ_PRON", "PVSUFF_SUBJ", "SUFF_FEM_TA")


def verb_tokens() -> list[tuple[str, str, str, int]]:
    """‎(السطح، حروفُ الجذع، الوسم، السورة)‎ لكلّ فعلٍ مبنيٍّ في المرجع.

    السطحُ من بادئة الأمر (إن فُصلت) إلى آخر لاحقةِ فاعل؛ والسوابقُ (و، ف) وما بعد
    الفاعل (ضميرُ المفعول، نونُ الوقاية) خارجه، ويُوسَم الوسمُ ‎+OBJ‎ إن تلاه ذلك.
    """

    out: list[tuple[str, str, str, int]] = []
    for group in masaq_words():
        segs = [row for row in group if _real(row)]
        vocal = align(group[0]["Word"], [row["Segmented_Word"] for row in segs])
        if vocal is None:
            continue
        tags = [row["Morph_tag"] for row in segs]
        for i, tag in enumerate(tags):
            if tag not in ("PV", "PV_PASS", "CV"):
                continue
            if segs[i]["Invariable_Declinable"] not in MABNI_LABELS:
                continue
            start = i - 1 if i > 0 and tags[i - 1] == "CV_PREF" else i
            end = i + 1
            while end < len(tags) and tags[end].startswith(_SUBJECT_TAGS):
                end += 1
            letters = "".join(row["Segmented_Word"] for row in segs[start : i + 1])
            before_object = end < len(tags)
            out.append(
                (
                    "".join(vocal[start:end]),
                    letters,
                    tag + ("+OBJ" if before_object else ""),
                    int(group[0]["Sura_No"]),
                )
            )
    return out


def _stem_class(letters: str) -> str:
    """صنفُ الجذع من حروفه بلا شكل، لتسمية ما لم يُولَّد (تشخيصٌ لا حكم)."""

    core = letters.lstrip("ا")
    if any(c in "أإؤئءآ" for c in letters):
        return "HAMZATED"
    if any(c in "اويى" for c in core):
        return "WEAK"
    return "SOUND_LETTERS"


_OBJECT_PIECES: Final[tuple[str, ...]] = (
    "هُنَّ",
    "هُمَا",
    "هُمْ",
    "كُمْ",
    "نَا",
    "نِي",
    "هُ",
    "هَا",
    "كَ",
    "نِ",
)
"""ضمائرُ نصبٍ متّصلةٌ يُجرَّب نزعُها لتشخيص وسمٍ مرجعيٍّ جعلها ضميرَ رفع."""


_SUBJECT_PIECES: Final[tuple[str, ...]] = ("وا", "و", "تُ", "تَ", "تْ", "نَا", "تُمْ")
"""لواحقُ فاعلٍ يُجرَّب إكمالُ السطح بها: قطعةٌ فصلها المرجعُ عن جذعها (‎خَرَجُ + وا‎)."""


def verb_readings() -> dict[str, Any]:
    """الأفعالُ المبنيّةُ في المرجع: كم استُرجع، وبأيّ صنفِ جذر، وكم تحليلًا، وما لم يُولَّد."""

    from .mabni_verbs import root_class

    outcomes: Counter[str] = Counter()
    by_tag: Counter[str] = Counter()
    by_class: Counter[str] = Counter()
    missing_class: Counter[str] = Counter()
    ambiguity: Counter[int] = Counter()
    misses: Counter[str] = Counter()
    for surface, letters, tag, _ in verb_tokens():
        outcome, found = recover_verb(surface, tag.endswith("+OBJ"))
        outcomes[outcome.name] += 1
        by_tag[f"{tag.removesuffix('+OBJ')}:{outcome.name}"] += 1
        if outcome is VerbOutcome.RECOVERED:
            distinct = {a.root for a in found}
            ambiguity[min(len(distinct), 4)] += 1
            by_class[root_class(found[0].root)] += 1
        else:
            missing_class[_stem_class(letters)] += 1
            misses[surface] += 1
    from .mabni_verbs import maqayis_roots, roots_generating

    lexicon = set(maqayis_roots())
    gap_roots: Counter[str] = Counter()
    unexplained: Counter[str] = Counter()
    diagnosis: Counter[str] = Counter()
    for surface, n in misses.items():
        roots = [
            r
            for obj in (False, True)
            for r in roots_generating(surface, obj)
            if r not in lexicon
        ]
        if roots:
            diagnosis["ROOT_ABSENT_FROM_THE_DEPOSITED_LEXICON"] += n
            for r in dict.fromkeys(roots):
                gap_roots[r] += n
            continue
        stripped = [
            surface[: -len(p)]
            for p in _OBJECT_PIECES
            if surface.endswith(p) and len(surface) > len(p)
        ]
        if any(recover_verb(x, True)[0] is VerbOutcome.RECOVERED for x in stripped):
            diagnosis["OBJECT_PRONOUN_TAGGED_AS_SUBJECT_IN_THE_REFERENCE"] += n
            continue
        completed = [surface + p for p in _SUBJECT_PIECES]
        if any(
            recover_verb(x, obj)[0] is VerbOutcome.RECOVERED
            for x in completed
            for obj in (False, True)
        ):
            diagnosis["SUBJECT_SUFFIX_SPLIT_OFF_BY_THE_REFERENCE"] += n
            continue
        diagnosis["UNEXPLAINED"] += n
        unexplained[surface] += n
    return {
        "outcomes": dict(outcomes),
        "not_generated_diagnosis": dict(diagnosis),
        "roots_absent_from_the_lexicon": gap_roots.most_common(),
        "not_generated_and_unexplained": unexplained.most_common(),
        "by_tag": dict(by_tag),
        "recovered_by_root_class": dict(by_class),
        "roots_per_recovered_token": {str(k): v for k, v in sorted(ambiguity.items())},
        "not_generated_by_stem_letters": dict(missing_class),
        "most_frequent_not_generated": misses.most_common(40),
    }


def lexical_generation_reading(context: str = "start_continue") -> dict[str, Any]:
    """جذوعُ المعجم المبنيّ كلُّها على الجسر، بالقاعدتين المعلنتين، ثمّ أليافُها."""

    inventory = lexical_inventory()
    stems = [v for (t, _), c in inventory.items() if t == "Stem" for v in c]
    fibers, outcomes = fibers_of(stems, context, lexical=True)
    return {
        "lemmas": sum(1 for (t, _) in inventory if t == "Stem"),
        "forms": len(set(stems)),
        "projection": dict(outcomes),
        "fiber_sizes": dict(Counter(len(v) for v in fibers.values())),
        "shared_fibers": [v for v in fibers.values() if len(v) > 1],
    }


def verb_generation_reading(context: str = "start_pause") -> dict[str, Any]:
    """التوليدُ إلى الـ116 ثمّ الاسترجاع، لكلّ جذرٍ استُرجع من المرجع.

    لكلّ جذرٍ استُرجع فعلٌ منه: تُولَّد صورُه كلُّها، وتُسقَط على الجسر، وتُبنى
    الألياف. ثمّ يُقابَل كلُّ فعلٍ استُرجع من المتن: ذرّاتُ سطحه على الجسر بذرّات
    صورته المولَّدة. والمقابلةُ في الوقف أصدق، إذ يسقط آخرُ الحركة في الطرفين كما في
    التطبيع.
    """

    from .mabni_verbs import normalize, verb_forms

    roots: set[str] = set()
    agree: Counter[str] = Counter()
    for surface, _, tag, _ in verb_tokens():
        obj = tag.endswith("+OBJ")
        outcome, found = recover_verb(surface, obj)
        if outcome is not VerbOutcome.RECOVERED:
            continue
        roots.update(a.root for a in found)
        if obj:
            agree["before_object_not_compared"] += 1
            continue
        generated = [
            w for w in verb_forms(found[0].root) if normalize(w) == normalize(surface)
        ]
        s_status, s_atoms = project_form(surface, context)
        g_status, g_atoms = project_form(generated[0], context, generated=True)
        if s_status != "READY":
            agree[f"surface_{s_status}"] += 1
        elif g_status != "READY":
            agree[f"generated_{g_status}"] += 1
        elif s_atoms == g_atoms:
            agree["same_atoms"] += 1
        else:
            agree["different_atoms"] += 1
    forms: list[str] = []
    for root in sorted(roots):
        forms.extend(verb_forms(root))
    fibers, outcomes = fibers_of(forms, context, generated=True)
    sizes = Counter(len(v) for v in fibers.values())
    return {
        "roots": len(roots),
        "generated_forms": len(set(forms)),
        "projection": dict(outcomes),
        "fiber_sizes": dict(sizes),
        "largest_fibers": sorted(fibers.values(), key=len, reverse=True)[:5],
        "corpus_vs_generated_atoms": dict(agree),
    }


# --- التعرّفُ على المبنيّ المعجميّ في نصفٍ لم يُرَ ----------------------------------


def lexical_recognition_reading() -> dict[str, int]:
    """يُبنى المعجمُ من السور الزوجيّة، ويُتعرَّف به على كلمات السور الفرديّة.

    التعرّفُ على كلمةٍ مشكولة بلا MASAQ (`_recognize`): سوابقُ من أوّلها، ولواحقُ
    من آخرها، وجذعٌ إن كان في المعجم. ويُقارَن ما تعرّف عليه بالقطع المبنيّة
    المعجميّة التي وسمها MASAQ في الكلمة نفسها، صورةً مشكولةً بصورة.
    """

    inventory = lexical_inventory(train_only=True)
    pieces = {
        kind: {v for (t, _), c in inventory.items() if t == kind for v in c}
        for kind in ("Prefix", "Stem", "Suffix")
    }
    counts: Counter[str] = Counter()
    for group in masaq_words():
        if int(group[0]["Sura_No"]) % 2 == 0:
            continue
        segs = [row for row in group if _real(row)]
        vocal = align(group[0]["Word"], [row["Segmented_Word"] for row in segs])
        if vocal is None:
            counts["words_not_aligned"] += 1
            continue
        expected = Counter(
            (row["Morph_type"], piece)
            for row, piece in zip(segs, vocal, strict=True)
            if row["Invariable_Declinable"] in MABNI_LABELS
            and genus_of(row["Morph_tag"]) is MabniGenus.LEXICAL
        )
        predicted = Counter(
            _recognize(
                group[0]["Word"], pieces["Prefix"], pieces["Stem"], pieces["Suffix"]
            )
        )
        counts["words"] += 1
        for kind in ("Prefix", "Stem", "Suffix"):
            e = Counter({k: v for k, v in expected.items() if k[0] == kind})
            q = Counter({k: v for k, v in predicted.items() if k[0] == kind})
            counts[f"{kind}:gold"] += sum(e.values())
            counts[f"{kind}:predicted"] += sum(q.values())
            counts[f"{kind}:correct"] += sum((e & q).values())
    return dict(counts)


def _chains(
    clusters: list[str], start: int, pieces: set[str], forward: bool
) -> list[int]:
    """مواضعُ انتهاءِ كلّ سلسلةِ قطعٍ ممكنةٍ من `start`.

    السوابقُ تُقرأ إلى الأمام، واللواحقُ إلى الخلف.
    """

    ends = [start]
    frontier = [start]
    while frontier:
        nxt = []
        for k in frontier:
            for n in (1, 2, 3):
                lo, hi = (k, k + n) if forward else (k - n, k)
                if lo < 0 or hi > len(clusters):
                    continue
                if "".join(clusters[lo:hi]) in pieces:
                    target = hi if forward else lo
                    if target not in ends:
                        ends.append(target)
                        nxt.append(target)
        frontier = nxt
    return ends


def _recognize(
    word: str, prefixes: set[str], stems: set[str], suffixes: set[str]
) -> list[tuple[str, str]]:
    """أقلُّ تقسيمٍ يجعل الجذعَ مبنيًّا معجميًّا؛ وإلا فأطولُ السوابق واللواحق.

    الجذعُ المعجميُّ يُقبَل إن انقسمت الكلمةُ كلُّها: سوابقُ من المعجم، ثمّ جذعٌ من
    المعجم، ثمّ لواحقُ من المعجم. فإن لم يوجد، فالجذعُ غيرُ مبنيٍّ معجميًّا (معرَبٌ
    أو فعل)، ويُخرَج أطولُ ما يُنزَع من السوابق واللواحق — وهو تخمينٌ تكشف دقّتَه
    القراءةُ لا تعريفُه.
    """

    clusters = _clusters(word)
    pre_ends = _chains(clusters, 0, prefixes, forward=True)
    suf_starts = _chains(clusters, len(clusters), suffixes, forward=False)
    best: tuple[int, int] | None = None
    for i in pre_ends:
        for j in suf_starts:
            if i < j and "".join(clusters[i:j]) in stems:
                cost = i + (len(clusters) - j)
                if best is None or cost < best[0] + (len(clusters) - best[1]):
                    best = (i, j)
    if best is not None:
        i, j = best
        found = [("Stem", "".join(clusters[i:j]))]
    else:
        i = max((e for e in pre_ends if e < len(clusters)), default=0)
        j = min((e for e in suf_starts if e > i), default=len(clusters))
        found = []
    out = _split_chain(clusters[:i], prefixes, "Prefix") + found
    return out + _split_chain(clusters[j:], suffixes, "Suffix")


def _split_chain(
    clusters: list[str], pieces: set[str], kind: str
) -> list[tuple[str, str]]:
    """تقسيمُ سلسلةٍ معلومةٍ إلى قطعها (أطولُها أوّلًا)."""

    out: list[tuple[str, str]] = []
    k = 0
    while k < len(clusters):
        for n in (3, 2, 1):
            piece = "".join(clusters[k : k + n])
            if k + n <= len(clusters) and piece in pieces:
                out.append((kind, piece))
                k += n
                break
        else:
            return out
    return out


# --- التقرير -------------------------------------------------------------------


def report() -> str:
    """القراءاتُ كلُّها جدولًا؛ كلُّ رقمٍ مشتقٌّ من التشغيل لا مكتوب."""

    segments, stats = mabni_segments()
    lines = ["# جسر المبنيّات — قراءةٌ مشتقّة من التشغيل", ""]
    lines.append(
        f"كلماتُ MASAQ {stats['words']:,}؛ لم تُحاذَ بالشكل "
        f"{stats['UNDERLYING_SEGMENTATION_NOT_ALIGNED']:,} (رسمٌ تغيّر بالتقطيع، فيها "
        f"{stats['mabni_in_unaligned']:,} قطعةً مبنيّة). والقطعُ المبنيّةُ المحاذاةُ بالشكل "
        f"{len(segments):,}."
    )
    lines += ["", "## الأجناس", "", "| الجنس | القطع | منها جذوع |", "|---|---|---|"]
    for genus in MabniGenus:
        pool = [s for s in segments if s.genus is genus]
        stems = sum(1 for s in pool if s.morph_type == "Stem")
        lines.append(f"| {genus.name} | {len(pool):,} | {stems:,} |")
    lines += [
        "",
        "## الانغلاق: معجمٌ من السور الزوجيّة، اختبارٌ على الفرديّة (جذوعًا)",
        "",
        "| الجنس | أنواعُ التدريب | تغطيةُ الوقوعات | تغطيةُ الأنواع |",
        "|---|---|---|---|",
    ]
    for r in closedness_readings():
        lines.append(
            f"| {r.genus.name} | {r.train_types:,} | "
            f"{r.test_tokens_covered:,}/{r.test_tokens:,} "
            f"({100 * r.token_coverage:.2f}%) | "
            f"{r.test_types_covered:,}/{r.test_types:,} "
            f"({100 * r.type_coverage:.2f}%) |"
        )
    rec = lexical_recognition_reading()
    lines += [
        "",
        "## التعرّفُ على المعجميّ في السور الفرديّة بلا MASAQ",
        "",
        "| القطعة | في المرجع | تعرّف عليها | صحيح | الدقّة | الاستدعاء |",
        "|---|---|---|---|---|---|",
    ]
    for kind in ("Prefix", "Stem", "Suffix"):
        g, p, c = rec[f"{kind}:gold"], rec[f"{kind}:predicted"], rec[f"{kind}:correct"]
        lines.append(
            f"| {kind} | {g:,} | {p:,} | {c:,} | "
            f"{100 * c / p:.1f}% | {100 * c / g:.1f}% |"
        )
    verbs = verb_readings()
    outcomes = verbs["outcomes"]
    total = sum(outcomes.values())
    lines += ["", "## الأفعالُ المبنيّة: عكسُ التوليد من جذور المقاييس", ""]
    lines += ["| المآل | العدد | النسبة |", "|---|---|---|"]
    for name, n in outcomes.items():
        lines.append(f"| {name} | {n:,} | {100 * n / total:.2f}% |")
    lines.append(f"| المجموع | {total:,} | |")
    lines += ["", "تشخيصُ ما لم يُولَّد:", ""]
    for name, n in verbs["not_generated_diagnosis"].items():
        lines.append(f"* {name}: {n:,}")
    lines += [
        "",
        f"المسترجَعُ بصنف الجذر: {verbs['recovered_by_root_class']}؛ "
        f"وعددُ الجذور المحتملة لكلّ وقوع: {verbs['roots_per_recovered_token']}.",
        "",
        "جذورٌ تولِّد أفعالًا في المتن وليست في جدول المقاييس المودَع (مرشَّحاتٌ من "
        "حروف السطح؛ قد يُرشَّح للوقوع الواحد جذران كـ عمو/عمي): "
        + "، ".join(f"{r} ({n})" for r, n in verbs["roots_absent_from_the_lexicon"]),
        "",
        "ما بقي بلا تفسير: "
        + "، ".join(f"{w} ({n})" for w, n in verbs["not_generated_and_unexplained"]),
    ]
    for context in ("start_continue", "start_pause"):
        lex = lexical_generation_reading(context)
        gen = verb_generation_reading(context)
        lines += [
            "",
            f"## التوليدُ إلى الـ116 ({context})",
            "",
            f"* المعجميّ: {lex['forms']:,} صورةً لـ{lex['lemmas']:,} مفردة؛ الإسقاط "
            f"{lex['projection']}؛ أحجامُ الألياف {lex['fiber_sizes']}.",
            f"* الأفعال: {gen['roots']:,} جذرًا، {gen['generated_forms']:,} صورةً مولَّدة؛ "
            f"الإسقاط {gen['projection']}؛ أحجامُ الألياف {gen['fiber_sizes']}؛ "
            f"ذرّاتُ المتن مقابلَ المولَّد {gen['corpus_vs_generated_atoms']}.",
        ]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    print(report())
