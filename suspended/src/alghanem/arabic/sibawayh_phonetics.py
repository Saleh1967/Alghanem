"""مخارجُ سيبويه وصفاتُه مستخرَجةً من بايتات «الكتاب» المختومة، لا من محفوظ.

المصدرُ بابٌ واحدٌ بعينه: «هذا بابُ عددِ الحروف العربيّة ومخارجِها ومهموسِها
ومجهورِها وأحوالِ مجهورِها ومهموسِها واختلافِها» (الجزء الرابع، علاماتُ الصفحات
‎V04P431–V04P435‎ في النسخة الرقميّة)، من المادّة `KITAB_SIBAWAYH` المُعلَنة
بطولها وبصمتها في `nahw_lexicon`. ولا يُكتَب في هذه الوحدة صفٌّ واحدٌ من صفات
العربيّة: كلُّ صفةٍ تُقرأ **بين مرساتين منقولتين بحروفهما من الباب نفسه**،
وكلُّ مرساةٍ يجب أن تقع في الباب مرّةً واحدةً وإلّا سقط الاستخراج
(`A_FEATURE_IS_READ_BETWEEN_TWO_SOURCE_ANCHORS_NOT_WRITTEN_FROM_MEMORY`).

    ASourceAnchor          != ARowWrittenHere
    AStatedCount           != ADerivedCount
    ASeparatingSignature   != APhoneticMeasurement
    ADeferredRecording     != ASuspendedTheory

**أوّلًا: والعددُ المنصوصُ يُصادَم بالمشتقّ.** يقول الباب: المجهورةُ «تسعةَ
عشرَ حرفًا»، والمهموسةُ «عشرةُ أحرف»، والمخارجُ «ستّةَ عشرَ». فتُشتَقّ الأعدادُ
من القوائم المستخرجة ثمّ تُقابَل بالمنصوص، ولا يُقرأ المنصوصُ وحدَه شهادةً
(`A_STATED_COUNT_IS_COLLIDED_WITH_A_DERIVED_ONE`).

**وثانيًا: والجهرُ والهمسُ قسمةٌ جامعةٌ مانعةٌ على حوامل الـ116.** المجهورةُ
والمهموسةُ تُصادَمان بمفردة `letter_fingerprint.LETTER_VOCABULARY` — تسعةٌ
وعشرون فيها الهمزةُ والألف — فإن لم تستغرقاها أو تداخلتا سقطت القسمة.

**وثالثًا: والصفاتُ تفصل ما جمعه المخرج.** كلُّ خانةِ مخرجٍ فيها أكثرُ من حرفٍ
يُسأل عنها: أتفترق حروفُها بتوقيع صفاتها؟ والفصلُ خبرٌ عن **هذا الترميز
المنقول**، لا قياسٌ صوتيّ (`A_SEPARATING_SIGNATURE_IS_NOT_A_PHONETIC_MEASUREMENT`).

**ورابعًا: ومخرجُ اللام ساقطٌ من النصّ المُودَع، والسقوطُ يُسمّى ولا يُسَدّ.**
البابُ يُعلن ستّةَ عشرَ مخرجًا، والمذكورُ صراحةً أربعةَ عشرَ ومعها الخياشيم.
والموضعُ بعينه: وصفُ حافة اللسان ينتهي بـ«مخرج النون» فيُطوى بين الوصفين ما
كان للّام، فلا يقع في الباب مخرجٌ يُسنَد إليها. ولا يُكمَل من محفوظٍ ولا من
جدولٍ آخرَ صامتًا؛ يُعرَض بقيّةً مقيسةً حتّى تُقابَل صفحةٌ مطبوعة
(`THE_LAM_MAKHRAJ_CLAUSE_IS_ABSENT_FROM_THE_DEPOSITED_TEXT`).

**وخامسًا: والتسجيلُ الصوتيُّ مؤجَّلٌ بقرار المالك، والنظريُّ ليس مؤجَّلًا.**
ما في هذه الوحدة علمُ الصوت النظريُّ المنقول: مخرجٌ وصفة. أمّا التسجيلُ
الصوتيُّ وضابطُ السمع فخارجَ النطاق بقرارٍ مُسمًّى، ولا يُعلِّق بغيابه حكمًا
من أحكام النظريّ (`A_DEFERRED_RECORDING_IS_NOT_A_SUSPENDED_THEORY`).

**وسادسًا: وما ليس في هذا الباب لا يُنسَب إليه.** الاستعلاءُ والقلقلةُ والصفيرُ
والتفشّي يذكرها سيبويه في أبوابٍ أخرى متفرّقة، والإذلاقُ غائبٌ عن «الكتاب»
كلِّه؛ فلا تدخل هذا الجدولَ، وموضعُها شاهدٌ ثانٍ يُسمّى مصدرُه
(`WHAT_THIS_CHAPTER_DOES_NOT_SAY_IS_NOT_ATTRIBUTED_TO_IT`).

ولا سلطانَ لهذه الوحدة: لا ولادةَ، ولا رفعَ حظر، ولا فكَّ تجميد، ولا استيرادَ
من `kernel/` (`NO_PHONETIC_TABLE_HERE_LIFTS_A_BLOCK_OR_THAWS_A_FREEZE`).
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from pathlib import Path
from types import MappingProxyType
from typing import Final

from .letter_fingerprint import LETTER_VOCABULARY
from .nahw_lexicon import (
    THE_MATERIALS,
    DeclaredMaterial,
    SealStanding,
    seal_reading_for,
)

__all__ = [
    "A_DEFERRED_RECORDING_IS_NOT_A_SUSPENDED_THEORY",
    "A_FEATURE_IS_READ_BETWEEN_TWO_SOURCE_ANCHORS_NOT_WRITTEN_FROM_MEMORY",
    "A_SEPARATING_SIGNATURE_IS_NOT_A_PHONETIC_MEASUREMENT",
    "A_STATED_COUNT_IS_COLLIDED_WITH_A_DERIVED_ONE",
    "NO_PHONETIC_TABLE_HERE_LIFTS_A_BLOCK_OR_THAWS_A_FREEZE",
    "SIBAWAYH_PHONETICS_NAMED_RESIDUALS",
    "THE_CHAPTER_END",
    "THE_CHAPTER_START",
    "THE_FEATURE_SPANS",
    "THE_LAM_MAKHRAJ_CLAUSE_IS_ABSENT_FROM_THE_DEPOSITED_TEXT",
    "THE_LETTER_NAMES",
    "THE_MAKHARIJ_SPAN",
    "THE_SOURCE",
    "WHAT_THIS_CHAPTER_DOES_NOT_SAY_IS_NOT_ATTRIBUTED_TO_IT",
    "FeatureRule",
    "FeatureSpan",
    "SibawayhPhoneticsError",
    "SibawayhReading",
    "chapter_text",
    "reading",
    "source_is_resolvable",
]


class SibawayhPhoneticsError(RuntimeError):
    """خطأُ استخراجٍ يُرفَع ولا يُتخطّى؛ فالمرساةُ الغائبةُ لا تُستبدَل بظنّ."""


THE_SOURCE: Final[DeclaredMaterial] = next(
    material for material in THE_MATERIALS if material.key == "KITAB_SIBAWAYH"
)
"""المادّةُ المُعلَنةُ في `nahw_lexicon` بطولها وبصمتها؛ لا نسخةَ ثانيةً منها."""

THE_CHAPTER_START: Final[str] = "هذا باب عدد الحروف العربية ومخارجها ومهموسها ومجهورها"
THE_CHAPTER_END: Final[str] = "وإنما وصفت لك حروف المعجم بهذه الصفات"

THE_LETTER_NAMES: Final[Mapping[str, str]] = MappingProxyType(
    {
        "الهمزة": "ء",
        "الألف": "ا",
        "الهاء": "ه",
        "العين": "ع",
        "الحاء": "ح",
        "الغين": "غ",
        "الخاء": "خ",
        "الكاف": "ك",
        "القاف": "ق",
        "الضاد": "ض",
        "الجيم": "ج",
        "الشين": "ش",
        "الياء": "ي",
        "اللام": "ل",
        "الراء": "ر",
        "النون": "ن",
        "الطاء": "ط",
        "الدال": "د",
        "التاء": "ت",
        "الصاد": "ص",
        "الزاي": "ز",
        "السين": "س",
        "الظاء": "ظ",
        "الذال": "ذ",
        "الثاء": "ث",
        "الفاء": "ف",
        "الباء": "ب",
        "الميم": "م",
        "الواو": "و",
    }
)
"""أسماءُ الحروف كما ينطق بها الباب، وحرفُ كلٍّ في المفردة؛ والإسنادُ منّا مُعلَن."""


class FeatureRule(Enum):
    """قاعدةُ قراءة الصفة من مقطعها؛ ثلاثٌ لا رابعَ لها."""

    LISTED = "كلُّ اسمِ حرفٍ في المقطع"
    COMPLEMENT = "ما سوى صفةٍ مسمّاةٍ من المفردة، بنصّ «كلّ ما سوى ذلك»"


@dataclass(frozen=True)
class FeatureSpan:
    """صفةٌ باسمها في الباب، ومرساتاها المنقولتان، وقاعدةُ قراءتها."""

    name: str
    start: str
    end: str
    rule: FeatureRule = FeatureRule.LISTED
    complement_of: str | None = None


THE_FEATURE_SPANS: Final[tuple[FeatureSpan, ...]] = (
    FeatureSpan("المجهورة", "فأما المجهورة", "فذلك تسعة عشر حرفا"),
    FeatureSpan("المهموسة", "وأما المهموسة", "فذلك عشرة أحرف"),
    FeatureSpan(
        "الشديد", "الشديد وهو الذي يمنع الصوت أن يجري فيه وهو", "وذلك أنك لو قلت"
    ),
    FeatureSpan("الرخوة", "ومنها الرخوة وهي", "وذلك إذا قلت"),
    FeatureSpan("بين الرخوة والشديدة", "وأما", "فبين الرخوة والشديدة"),
    FeatureSpan(
        "المنحرف", "ولم يعترض على الصوت كاعتراض الحروف الشديدة وهو", "وإن شئت مددت"
    ),
    FeatureSpan("الغنة", "لم يجر معه الصوت وهو", "ومنها المكرر"),
    FeatureSpan("المكرر", "لم يجر الصوت فيه وهو", "ومنها اللينة"),
    FeatureSpan("اللينة", "ومنها اللينة وهي", "لأن مخرجهما"),
    FeatureSpan("الهاوي", "لسانك قبل الحنك وهي", "وهذه الثلاثة"),
    FeatureSpan("المطبقة", "فأما المطبقة", "والمنفتحة كل"),
    FeatureSpan(
        "المنفتحة",
        "والمنفتحة كل",
        "من الحروف",
        rule=FeatureRule.COMPLEMENT,
        complement_of="المطبقة",
    ),
)
"""الصفاتُ بمرساتيها؛ والمرساتان من نصّ الباب لا من صياغتنا."""

THE_STATED_COUNTS: Final[Mapping[str, tuple[str, int]]] = MappingProxyType(
    {
        "المجهورة": ("فذلك تسعة عشر حرفا", 19),
        "المهموسة": ("فذلك عشرة أحرف", 10),
    }
)
"""العددُ المنصوصُ لكلّ صفةٍ مع موضعِ نصّه؛ ويُصادَم بالمشتقّ لا يُقرأ وحدَه."""

THE_MAKHARIJ_SPAN: Final[tuple[str, str]] = (
    "ولحروف العربية ستة عشر مخرجا",
    "فأما المجهورة",
)
THE_STATED_MAKHARIJ_COUNT: Final[int] = 16
"""«ستّة عشر» بنصّ الباب في مرساة المخارج نفسِها."""

_KHAYSHUM: Final[str] = "الخياشيم"
_PIECE_SPLIT: Final[re.Pattern[str]] = re.compile(r"\|| ومن | ومما | وأدناها ")
_NOISE: Final[re.Pattern[str]] = re.compile(r"PageV\d+P\d+|ms\d+|~~|#")
_NAME: Final[re.Pattern[str]] = re.compile(r"ال[ء-ي]+")


def source_is_resolvable(root: Path | None = None) -> bool:
    """أبايتاتُ «الكتاب» حاضرةٌ مطابقةٌ لطولها وبصمتها؟ والجوابُ من القرص."""

    return (
        seal_reading_for(THE_SOURCE, root).standing is SealStanding.SEALED_AND_PRESENT
    )


def _unique_index(text: str, anchor: str, start: int = 0) -> int:
    first = text.find(anchor, start)
    if first < 0:
        raise SibawayhPhoneticsError(f"المرساةُ غائبةٌ عن الباب: «{anchor}»")
    return first


@lru_cache(maxsize=4)
def chapter_text(root: Path | None = None) -> str:
    """نصُّ الباب بين مرساتيه، مُسوًّى بإزالة علامات الصفحات والحواشي وحدَها."""

    seal = seal_reading_for(THE_SOURCE, root)
    if (
        seal.standing is not SealStanding.SEALED_AND_PRESENT
        or seal.resolved_path is None
    ):
        raise SibawayhPhoneticsError(
            f"«{THE_SOURCE.title}» ليست مختومةً حاضرة: {seal.standing.value}"
        )
    raw = Path(seal.resolved_path).read_bytes().decode("utf-8")
    flat = re.sub(r"\s+", " ", _NOISE.sub(" ", raw))
    if flat.count(THE_CHAPTER_START) != 1:
        raise SibawayhPhoneticsError("مرساةُ بدء الباب ليست فريدةً في الكتاب.")
    begin = flat.index(THE_CHAPTER_START)
    end = _unique_index(flat, THE_CHAPTER_END, begin)
    return flat[begin:end]


def _names_in(span: str) -> tuple[str, ...]:
    found: list[str] = []
    for match in _NAME.finditer(span):
        letter = THE_LETTER_NAMES.get(match.group(0))
        if letter is not None and letter not in found:
            found.append(letter)
    return tuple(found)


def _between(text: str, start: str, end: str) -> str:
    if text.count(start) != 1 and start != "وأما":
        raise SibawayhPhoneticsError(f"مرساةُ البدء ليست فريدة: «{start}»")
    stop = _unique_index(text, end)
    begin = text.rfind(start, 0, stop) if start == "وأما" else text.find(start)
    if begin < 0 or begin >= stop:
        raise SibawayhPhoneticsError(f"المقطعُ مقلوبٌ بين «{start}» و«{end}»")
    return text[begin + len(start) : stop]


@dataclass(frozen=True)
class SibawayhReading:
    """ما استُخرج من الباب: صفاتٌ، ومخارجُ، وأعدادٌ منصوصةٌ ومشتقّة."""

    features: Mapping[str, frozenset[str]]
    makharij: tuple[frozenset[str], ...]
    khayshum_is_stated: bool
    stated_counts: Mapping[str, int]

    @property
    def derived_makharij_count(self) -> int:
        """المخارجُ المذكورةُ صراحةً، ومعها الخياشيمُ إن ذُكرت."""

        return len(self.makharij) + (1 if self.khayshum_is_stated else 0)

    @property
    def letters_without_a_makhraj(self) -> tuple[str, ...]:
        """حروفُ المفردة التي لا يُسنِد إليها البابُ المودَعُ مخرجًا."""

        seated = set().union(*self.makharij)
        return tuple(letter for letter in LETTER_VOCABULARY if letter not in seated)

    @property
    def voicing_is_a_partition(self) -> bool:
        """الجهرُ والهمسُ: مستغرِقان للمفردة، متباينان، ومطابقان للمنصوص عدًّا."""

        voiced = self.features["المجهورة"]
        voiceless = self.features["المهموسة"]
        return (
            not voiced & voiceless
            and voiced | voiceless == frozenset(LETTER_VOCABULARY)
            and len(voiced) == self.stated_counts["المجهورة"]
            and len(voiceless) == self.stated_counts["المهموسة"]
        )

    def signature(self, letter: str) -> frozenset[str]:
        """توقيعُ الحرف: أسماءُ الصفات التي ينطق الباب بها فيه."""

        return frozenset(
            name for name, members in self.features.items() if letter in members
        )

    @property
    def unseparated_cells(self) -> tuple[frozenset[str], ...]:
        """خاناتُ مخرجٍ لا تفترق حروفُها بتواقيع صفاتها."""

        return tuple(
            cell
            for cell in self.makharij
            if len({self.signature(letter) for letter in cell}) < len(cell)
        )


@lru_cache(maxsize=4)
def reading(root: Path | None = None) -> SibawayhReading:
    """يُستخرج الجدولُ من الباب عند كلّ قراءةٍ جديدة؛ ولا يُحفَظ صفٌّ منه نصًّا."""

    text = chapter_text(root)
    features: dict[str, frozenset[str]] = {}
    for span in THE_FEATURE_SPANS:
        if span.rule is FeatureRule.COMPLEMENT:
            if span.complement_of is None or span.complement_of not in features:
                raise SibawayhPhoneticsError(f"متمّمٌ بلا أصلٍ مستخرج: {span.name}")
            _unique_index(text, span.start)
            features[span.name] = (
                frozenset(LETTER_VOCABULARY) - features[span.complement_of]
            )
            continue
        members = _names_in(_between(text, span.start, span.end))
        if not members:
            raise SibawayhPhoneticsError(f"صفةٌ بلا حرفٍ في مقطعها: {span.name}")
        features[span.name] = frozenset(members)
    stated: dict[str, int] = {}
    for name, (phrase, value) in THE_STATED_COUNTS.items():
        _unique_index(text, phrase)
        stated[name] = value
    _unique_index(text, THE_MAKHARIJ_SPAN[0])
    section = _between(text, *THE_MAKHARIJ_SPAN)
    makharij: list[frozenset[str]] = []
    khayshum = False
    for piece in _PIECE_SPLIT.split(section):
        if "مخرج" not in piece:
            continue
        if _KHAYSHUM in piece:
            khayshum = True
            continue
        tail = piece[piece.rfind("مخرج") :]
        letters = _names_in(tail)
        if letters:
            makharij.append(frozenset(letters))
    return SibawayhReading(
        features=MappingProxyType(features),
        makharij=tuple(makharij),
        khayshum_is_stated=khayshum,
        stated_counts=MappingProxyType(stated),
    )


A_FEATURE_IS_READ_BETWEEN_TWO_SOURCE_ANCHORS_NOT_WRITTEN_FROM_MEMORY: Final[str] = (
    "كلُّ صفةٍ تُقرأ بين مرساتين منقولتين بحروفهما من الباب، ولا يُكتَب صفٌّ من محفوظ."
)
A_STATED_COUNT_IS_COLLIDED_WITH_A_DERIVED_ONE: Final[str] = (
    "العددُ المنصوصُ في الباب يُصادَم بعددِ ما استُخرج، ولا يُقرأ وحدَه شهادة."
)
A_SEPARATING_SIGNATURE_IS_NOT_A_PHONETIC_MEASUREMENT: Final[str] = (
    "افتراقُ التواقيع خبرٌ عن الترميز المنقول، لا قياسٌ صوتيٌّ لحناجر."
)
THE_LAM_MAKHRAJ_CLAUSE_IS_ABSENT_FROM_THE_DEPOSITED_TEXT: Final[str] = (
    "البابُ يُعلن ستّةَ عشرَ مخرجًا ويذكر خمسةَ عشرَ؛ ومخرجُ اللام ساقطٌ من النصّ "
    "المودَع، فيُسمّى بقيّةً حتّى تُقابَل صفحةٌ مطبوعة، ولا يُكمَل من محفوظ."
)
A_DEFERRED_RECORDING_IS_NOT_A_SUSPENDED_THEORY: Final[str] = (
    "التسجيلُ الصوتيُّ مؤجَّلٌ بقرار المالك خارجَ النطاق، ولا يُعلِّق علمَ الصوت "
    "النظريَّ ولا عددًا يُبنى عليه."
)
WHAT_THIS_CHAPTER_DOES_NOT_SAY_IS_NOT_ATTRIBUTED_TO_IT: Final[str] = (
    "الاستعلاءُ والقلقلةُ والصفيرُ والتفشّي في أبوابٍ أخرى، والإذلاقُ غائبٌ عن "
    "الكتاب؛ فلا تُنسَب إلى هذا الباب، وموضعُها شاهدٌ ثانٍ مسمّى."
)
NO_PHONETIC_TABLE_HERE_LIFTS_A_BLOCK_OR_THAWS_A_FREEZE: Final[str] = (
    "لا ولادةَ ولا رفعَ حظرٍ ولا فكَّ تجميدٍ ولا استيرادَ من kernel/."
)

SIBAWAYH_PHONETICS_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    "A_FEATURE_IS_READ_BETWEEN_TWO_SOURCE_ANCHORS_NOT_WRITTEN_FROM_MEMORY",
    "A_STATED_COUNT_IS_COLLIDED_WITH_A_DERIVED_ONE",
    "A_SEPARATING_SIGNATURE_IS_NOT_A_PHONETIC_MEASUREMENT",
    "THE_LAM_MAKHRAJ_CLAUSE_IS_ABSENT_FROM_THE_DEPOSITED_TEXT",
    "A_DEFERRED_RECORDING_IS_NOT_A_SUSPENDED_THEORY",
    "WHAT_THIS_CHAPTER_DOES_NOT_SAY_IS_NOT_ATTRIBUTED_TO_IT",
    "NO_PHONETIC_TABLE_HERE_LIFTS_A_BLOCK_OR_THAWS_A_FREEZE",
)
