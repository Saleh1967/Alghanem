"""مقابلةُ النسختين المُودَعتين: فروقٌ تُسمّى رتبةً رتبةً، لا تُؤجَّل جملةً.

عُرِض على هذه الشجرة تقريرُ بوّاباتٍ يقول: «تثبيتُ اللقطة المرجعيّة وبصمتها —
`PASS`»، و«مقابلةُ جميع الأسطر — `PASS_6236_ROWS`»، و«تطابقُ الملفّ كلِّه مع
المرجع — `DEFER_DIFFERENCES`»، و«مطابقةُ نوع الوقف — …» مقطوعًا. وهذه الوحدةُ
تُشغِّل تلك البوّابات على البايتات المُودَعة ههنا، فتُخرِج لكلِّ بوّابةٍ حالًا
مُعادَ الاشتقاق بدل حالٍ مرويّة.

**أوّلًا: والمرجعُ ههنا مُودَعٌ مختوم، لا لقطةٌ مرويّة.**
في `corpora/` نسختان لا واحدة، وكلتاهما بايتاتٌ تُفتَح:

| المُودَع | البايتات | الأسطر | وقفٌ | خنجريّة | `<sel>` |
|---|---|---|---|---|---|
| `quran-simple-enhanced.txt` | 1,319,901 | 6,236 | **0** | **0** | 4,287 |
| `globalquran-simple-enhanced.txt` | 1,306,770 | 6,248 | **4,578** | **3,216** | 0 |

`A_SNAPSHOT_WITHOUT_DEPOSITED_BYTES_IS_A_REPORT_NOT_A_REFERENCE`: فالبوّابةُ
الأولى تُقرأ ههنا على هاتين وحدَهما. وأمّا «اللقطةُ المُؤرشَفة» التي في
التقرير المعروض فلا بايتاتِ لها في هذه الشجرة، فلا تُصدَّق ولا تُكذَّب:
تُوسَم **غيرَ مفحوصةٍ**، ويُقرأ هذا الحكمُ على مُودَعينا لا عليها.

**وثانيًا: و«ستّةُ آلافٍ ومئتان وستّةٌ وثلاثون» صادقةٌ بشرطٍ يُسمّى.**
`THE_ROW_COUNT_AGREES_ONLY_AFTER_NAMING_THE_TWELVE_DROPPED_LINES`: المرجعُ
**6,248** سطرًا لا 6,236؛ فيه بعد السطر الأخير اثنا عشرَ سطرًا: بياضٌ وكتلةُ
ناشرٍ تبدأ بـ`#`. فالموافقةُ على 6,236 تقع **بعد** إسقاط الاثني عشر، وإسقاطُها
صوابٌ — لكنّه صوابٌ يُكتَب. وبوّابةٌ تُخرِج `PASS_6236_ROWS` ولا تُسمّي ما
أسقطته تُخفي خطوةً يحتاجها من يُعيد العدّ.

**وثالثًا: و«تأجيلُ الفروق» بلا عددٍ ليس تأجيلًا.**
`A_DEFERRED_DIFFERENCE_THAT_IS_NOT_COUNTED_IS_NOT_DEFERRED_BUT_UNEXAMINED`:
تأجيلٌ يَعرِف عدَّ ما أجَّله وصنفَه تأجيل، وتأجيلٌ لا يعرفهما **سكوتٌ**. وههنا
عُدَّت: من 6,236 صفًّا تطابق **1,864** كما أُودِعا، واختلف **4,372**. ثمّ
يُفَكُّ المختلفُ برتباتٍ مُعلَنةٍ **مرتَّبة**، وكلُّ رتبةٍ تُخرِج ما أزالته:

| الرتبة | يبقى مختلفًا | أزالت |
|---|---|---|
| كما أُودِعا | 4,372 | — |
| علامةُ ترتيب البايتات | 4,372 | 0 |
| وسمُ الناشر `<sel>` | 4,372 | 0 |
| علاماتُ الوقف | 3,688 | **684** |
| الألفُ الخنجريّة | 2,299 | **1,389** |
| البياض | 2,129 | 170 |
| ترتيبُ التنوين مع الألف | 114 | **2,015** |
| طيُّ الهمزة المتّفقُ عليه | 111 | 3 |
| البسملةُ في مطلع السور | **1** | 110 |

والرتبتان الأوليان تُخرِجان **صفرًا**، وهو صفرٌ مقروءٌ لا محذوف: `<sel>` أربعةُ
آلافٍ ومئتان وسبعةٌ وثمانون وسمًا عندنا، لكنّ صفوفَها مختلفةٌ لأسبابٍ أخرى
معها، فلا تُزيل صفًّا بمفردها. وحذفُ صفٍّ خالٍ من السُّلَّم يرفع التفسيرَ
بإخفاء خطوةٍ لم تُفسِّر شيئًا.

**ورابعًا: والبقيّةُ صفٌّ واحدٌ يُسمّى ولا يُدوَّر.**
`THE_RESIDUE_IS_ONE_ROW_AND_IT_IS_NAMED_NOT_ROUNDED`: بعد الرتبات كلِّها يبقى
صفٌّ واحدٌ لا تُفسِّره قاعدةٌ مُعلَنة: الصفُّ **3,189**. وعندنا فيه «إِنَّهُ
مِن سُلَيْمَانَ وَإِنَّهُ بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ»، وفي المرجع
«إِنَّهُ مِن سُلَيْمَانَ وَإِنَّهُ» — مقطوعًا.

وهذا ليس فرقَ رسمٍ ولا فرقَ علامة: قاعدةُ المرجع في نزع البسملة من مطالع
السور **أصابت بسملةً هي من متن الآية نفسِها**، فحذفت ما ليس مطلعًا. وهو ما
تُخرِجه البقيّةُ دائمًا إذا سُمّيت: موضعُ تجاوزِ قاعدةٍ آليّةٍ حدَّها. ولو
أُجِّلت الفروقُ جملةً لَما ظهر هذا الصفُّ ألبتّة؛ فالتسميةُ هي التي أظهرته،
لا التأجيل.

**وخامسًا: وبوّابةُ الوقف لا تُقاس على مُودَعنا، ومع ذلك تُخرِج خبرًا.**
`A_ZERO_ON_ONE_SIDE_IS_NOT_AGREEMENT_WHEN_THE_OTHER_SIDE_IS_FULL`: في مُودَعنا
**صفرُ** علامةِ وقفٍ من نطاق `U+06D6`–`U+06ED`؛ وهو موافقٌ لما هو مكتوبٌ في
الشجرة بالاسم في `fath_ayah_source_text`: أُسقطت علاماتُ الوقف من هذا النقل،
«ولا يُحتجّ بخلوّه منها على شيء». فبوّابةٌ تُطابق «نوعَ الوقف» على مُودَعنا
وحدَه تُخرِج موافقةً كاذبة: صفرٌ يوافق صفرًا لأنّ العلامةَ ليست في الطرفين.

والعدّادُ ليس أصمَّ، وهذا مقيسٌ لا مُدَّعًى: هو نفسُه يُخرِج **4,578** علامةَ
وقفٍ على المُودَع الثاني في المجلَّد نفسِه. فالصفرُ عندنا صفةُ **هذا النقل**
لا صفةُ الأداة. وعليه تُخرَج البوّابةُ الرابعةُ **معلَّقةً باسم مادّتها**: لا
نوعَ وقفٍ يُطابَق حيث لا علامةَ وقفٍ تُقرأ، ولا تُخرَج «ناجحة».

وهذه الوحدةُ قراءةٌ لا سلطة: لا ولادةَ فيها، ولا حكمَ ولادة، ولا تجميدَ `E0`،
ولا استيرادَ من `kernel/`، ولا يُرفَع بها حجبُ طبقة. وكلُّ رقمٍ فيها محكومٌ
بهذين المُودَعين وحدَهما، وليس حكمًا على نسخةٍ ثالثةٍ لم تُفتَح.
"""

from __future__ import annotations

import hashlib
import re
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from types import MappingProxyType
from typing import Final

from .tajsir_bridge import fold_map

__all__ = [
    "AYAH_ROWS",
    "A_DEFERRED_DIFFERENCE_THAT_IS_NOT_COUNTED_IS_NOT_DEFERRED_NOTE",
    "A_SNAPSHOT_WITHOUT_DEPOSITED_BYTES_IS_NOT_A_REFERENCE_NOTE",
    "A_ZERO_ON_ONE_SIDE_IS_NOT_AGREEMENT_NOTE",
    "THE_COLLATION_AT_MEASUREMENT",
    "THE_DEPOSITS",
    "THE_RESIDUE_IS_ONE_ROW_AND_IT_IS_NAMED_NOT_ROUNDED_NOTE",
    "THE_ROW_COUNT_AGREES_ONLY_AFTER_NAMING_THE_DROPPED_LINES_NOTE",
    "THE_SUBMITTED_GATES",
    "THE_WAQF_RANGE",
    "CollationLadder",
    "DepositReading",
    "FoldRung",
    "GateStanding",
    "MirrorCollationError",
    "ResidueRow",
    "SubmittedGate",
    "ayah_rows_of",
    "collation_ladder",
    "deposit_reading",
    "gate_readings",
    "residue_rows",
    "the_declared_rungs",
]


class MirrorCollationError(ValueError):
    """رفضٌ صريح: مُودَعٌ متبدّلُ البصمة، أو رتبةٌ بلا اسم، أو صفٌّ خارج الجرد."""


A_SNAPSHOT_WITHOUT_DEPOSITED_BYTES_IS_NOT_A_REFERENCE_NOTE: Final[str] = (
    "لقطةٌ مُؤرشَفةٌ لا بايتاتِ لها في الشجرة ليست مرجعًا يُقابَل به، بل خبرٌ "
    "عن مرجع؛ فلا تُصدَّق ولا تُكذَّب، وتُوسَم غيرَ مفحوصة"
)

THE_ROW_COUNT_AGREES_ONLY_AFTER_NAMING_THE_DROPPED_LINES_NOTE: Final[str] = (
    "موافقةُ عدد الأسطر تقع بعد إسقاط كتلة الناشر الأخيرة؛ وبوّابةٌ تُخرِج "
    "العددَ ولا تُسمّي ما أسقطته تُخفي خطوةً يحتاجها من يُعيد العدّ"
)

A_DEFERRED_DIFFERENCE_THAT_IS_NOT_COUNTED_IS_NOT_DEFERRED_NOTE: Final[str] = (
    "تأجيلٌ يعرف عدَّ ما أجّله وصنفَه تأجيل، وتأجيلٌ لا يعرفهما سكوتٌ؛ "
    "والفرقُ بينهما أنّ الأوّلَ يُعيد اشتقاقَ عدده والثاني لا يملك عددًا"
)

THE_RESIDUE_IS_ONE_ROW_AND_IT_IS_NAMED_NOT_ROUNDED_NOTE: Final[str] = (
    "ما لم تُفسِّره رتبةٌ مُعلَنةٌ يُخرَج بسطره ونصَّيه، ولو كان صفًّا واحدًا؛ "
    "فالبقيّةُ المسمّاةُ تُظهِر موضعَ تجاوزِ قاعدةٍ آليّةٍ حدَّها"
)

A_ZERO_ON_ONE_SIDE_IS_NOT_AGREEMENT_NOTE: Final[str] = (
    "خلوُّ نقلٍ من علامةٍ ليس موافقةً لنقلٍ آخرَ خالٍ منها؛ والعدّادُ يُثبِت "
    "بصرَه بإخراجه العلامةَ حيث هي، ثمّ يُقرأ صفرُه صفةً للنقل لا للأداة"
)

AYAH_ROWS: Final[int] = 6_236
"""عددُ صفوف الآيات المقابَلة؛ سطرٌ لكلّ آيةٍ في المُودَعين معًا."""

THE_WAQF_RANGE: Final[frozenset[int]] = frozenset(
    {0x0615, 0x06DD, *range(0x06D6, 0x06ED + 1)}
)
"""نطاقُ علامات الوقف المصحفيّة المقروءُ ههنا؛ مُعلَنٌ قبل القياس لا بعده."""


@dataclass(frozen=True, slots=True)
class DepositReading:
    """قراءةُ مُودَعٍ من قرصه: بصمتُه وطولُه وأسطرُه وما يحمل من وسوم."""

    name: str
    byte_length: int
    sha256: str
    lines: int
    waqf_marks: int
    dagger_alifs: int
    publisher_tags: int

    @property
    def rows_beyond_the_ayahs(self) -> int:
        """ما زاد على صفوف الآيات؛ كتلةُ ناشرٍ تُسمّى ولا تُطوى صامتة."""

        return self.lines - AYAH_ROWS


THE_DEPOSITS: Final[MappingProxyType[str, tuple[int, str]]] = MappingProxyType(
    {
        "quran-simple-enhanced.txt": (
            1_319_901,
            "37633090743d403886b334d12dd911d1994e49767faa9f2be0f01fd48b466c5a",
        ),
        "globalquran-simple-enhanced.txt": (
            1_306_770,
            "8b387ea811bc8c658e1cab75488ce1aa69606deafd62759eeaf49ffe15c6d215",
        ),
    }
)
"""المُودَعان بطولهما وبصمتهما؛ ولا يُقرأ ملفٌّ خالفَ أحدَهما."""


def _corpora_dir(root: Path | None = None) -> Path:
    return (root or Path(__file__).resolve().parents[3]) / "corpora"


def _read_sealed(name: str, root: Path | None = None) -> str:
    if name not in THE_DEPOSITS:
        raise MirrorCollationError("مُودَعٌ غيرُ مُعلَنٍ لا يُقرأ ولو حضرت بايتاتُه.")
    path = _corpora_dir(root) / name
    if not path.is_file():
        raise MirrorCollationError(f"بايتاتُ {name} غائبةٌ عن الشجرة؛ لا إخراجَ بدونها.")
    raw = path.read_bytes()
    declared_length, declared_sha = THE_DEPOSITS[name]
    if len(raw) != declared_length:
        raise MirrorCollationError(f"طولُ {name} خالفَ المُعلَن؛ وقفٌ لا تخطٍّ.")
    if hashlib.sha256(raw).hexdigest() != declared_sha:
        raise MirrorCollationError(f"بصمةُ {name} خالفت المُعلَن؛ وقفٌ لا تخطٍّ.")
    return raw.decode("utf-8")


def deposit_reading(name: str, root: Path | None = None) -> DepositReading:
    """قراءةُ مُودَعٍ بعد مطابقة طوله وبصمته معًا؛ والمخالفُ يَفشَل ولا يُتخطّى."""

    text = _read_sealed(name, root)
    declared_length, declared_sha = THE_DEPOSITS[name]
    return DepositReading(
        name=name,
        byte_length=declared_length,
        sha256=declared_sha,
        lines=len(text.splitlines()),
        waqf_marks=sum(1 for ch in text if ord(ch) in THE_WAQF_RANGE),
        dagger_alifs=text.count("\u0670"),
        publisher_tags=text.count("<sel>"),
    )


def ayah_rows_of(name: str, root: Path | None = None) -> tuple[str, ...]:
    """صفوفُ الآيات وحدَها؛ وما زاد عليها مقطوعٌ بعدٍّ مُعلَنٍ لا بتخمين."""

    lines = _read_sealed(name, root).splitlines()
    if len(lines) < AYAH_ROWS:
        raise MirrorCollationError("مُودَعٌ أقصرُ من صفوف الآيات لا يُقابَل به.")
    return tuple(lines[:AYAH_ROWS])


def _strip_bom(form: str) -> str:
    return form.lstrip("\ufeff")


def _strip_publisher_tags(form: str) -> str:
    return form.replace("<sel>", "")


def _strip_waqf(form: str) -> str:
    return "".join(ch for ch in form if ord(ch) not in THE_WAQF_RANGE)


def _strip_dagger_alif(form: str) -> str:
    return form.replace("\u0670", "")


def _normalise_space(form: str) -> str:
    return re.sub(r"\s+", " ", form).strip()


_TANWIN_BEFORE_ALIF: Final[re.Pattern[str]] = re.compile("([\u064b\u064c\u064d])\u0627")


def _normalise_tanwin_order(form: str) -> str:
    return _TANWIN_BEFORE_ALIF.sub("\u0627\\1", form)


def _apply_agreed_fold(form: str) -> str:
    folding = fold_map()
    return "".join(folding.get(ch, ch) for ch in form)


@dataclass(frozen=True, slots=True)
class FoldRung:
    """رتبةٌ من سُلَّم الطيّ: اسمُها، وما بقي مختلفًا بعدها، وما أزالته."""

    name: str
    still_differing: int
    removed: int

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise MirrorCollationError("رتبةٌ بلا اسمٍ لا تُسعَّر ولا تُقرأ.")
        for value in (self.still_differing, self.removed):
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise MirrorCollationError("عددٌ في السُّلَّم صحيحٌ غيرُ سالب.")
        if self.still_differing > AYAH_ROWS:
            raise MirrorCollationError("مختلفٌ يزيد على صفوف الآيات ليس عدًّا.")

    @property
    def explains_nothing(self) -> bool:
        """رتبةٌ لم تُزِل صفًّا واحدًا؛ تُخرَج بصفرها ولا تُحذَف من السُّلَّم."""

        return self.removed == 0


def the_declared_rungs() -> tuple[tuple[str, Callable[[str], str]], ...]:
    """الرتباتُ مُعلَنةٌ **مرتَّبة**؛ وتبديلُ ترتيبها يُبدِّل ما تُزيله كلُّ واحدة."""

    return (
        ("علامةُ ترتيب البايتات", _strip_bom),
        ("وسمُ الناشر <sel>", _strip_publisher_tags),
        ("علاماتُ الوقف", _strip_waqf),
        ("الألفُ الخنجريّة", _strip_dagger_alif),
        ("البياض", _normalise_space),
        ("ترتيبُ التنوين مع الألف", _normalise_tanwin_order),
        ("طيُّ الهمزة المتّفقُ عليه", _apply_agreed_fold),
    )


@dataclass(frozen=True, slots=True)
class ResidueRow:
    """صفٌّ لم تُفسِّره رتبةٌ مُعلَنة؛ يُخرَج بسطره ونصَّيه ولا يُدوَّر."""

    row_number: int
    ours: str
    reference: str

    def __post_init__(self) -> None:
        if not 1 <= self.row_number <= AYAH_ROWS:
            raise MirrorCollationError("رقمُ صفٍّ خارج الجرد لا يُسجَّل بقيّة.")
        if self.ours == self.reference:
            raise MirrorCollationError("صفٌّ متطابقٌ ليس بقيّةً غيرَ مفسَّرة.")


@dataclass(frozen=True, slots=True)
class CollationLadder:
    """جملةُ المقابلة: المتطابقُ، والمختلفُ، وسُلَّمُ الرتبات، والبقيّة."""

    identical_as_deposited: int
    differing_as_deposited: int
    rungs: tuple[FoldRung, ...]
    basmala_prefixed_rows: int
    residue: tuple[ResidueRow, ...]

    def __post_init__(self) -> None:
        if self.identical_as_deposited + self.differing_as_deposited != AYAH_ROWS:
            raise MirrorCollationError("المتطابقُ والمختلفُ لا يستوفيان صفوفَ الآيات.")
        if not self.rungs:
            raise MirrorCollationError("سُلَّمٌ بلا رتبةٍ ليس سُلَّمًا.")
        last = self.rungs[-1].still_differing
        if self.basmala_prefixed_rows + len(self.residue) != last:
            raise MirrorCollationError(
                "البسملةُ والبقيّةُ لا تستوفيان ما بقي بعد الرتبات؛ "
                "وتفسيرٌ لا يُجمَع ليس تفسيرًا."
            )

    @property
    def unexplained_rows(self) -> int:
        """ما لم تُفسِّره قاعدةٌ مُعلَنة؛ وهو وحدَه ما يُقال إنّه غيرُ محسوم."""

        return len(self.residue)


def _collate(root: Path | None = None) -> tuple[list[str], list[str]]:
    ours = list(ayah_rows_of("quran-simple-enhanced.txt", root))
    reference = list(ayah_rows_of("globalquran-simple-enhanced.txt", root))
    return ours, reference


def collation_ladder(root: Path | None = None) -> CollationLadder:
    """المقابلةُ كاملةً، مُعادَ اشتقاقُها من البايتات في كلِّ نداء."""

    ours, reference = _collate(root)
    differing = sum(1 for x, y in zip(ours, reference) if x != y)
    rungs: list[FoldRung] = []
    previous = differing
    for name, rule in the_declared_rungs():
        ours = [rule(form) for form in ours]
        reference = [rule(form) for form in reference]
        now = sum(1 for x, y in zip(ours, reference) if x != y)
        rungs.append(FoldRung(name=name, still_differing=now, removed=previous - now))
        previous = now
    remaining = [i for i in range(AYAH_ROWS) if ours[i] != reference[i]]
    prefixes = {
        ours[i][: len(ours[i]) - len(reference[i])]
        for i in remaining
        if reference[i] and ours[i].endswith(reference[i])
    }
    basmala = max(prefixes, key=len) if prefixes else ""
    prefixed = [
        i
        for i in remaining
        if basmala
        and reference[i]
        and ours[i].endswith(reference[i])
        and ours[i][: len(ours[i]) - len(reference[i])] == basmala
    ]
    raw_ours, raw_reference = _collate(root)
    residue = tuple(
        ResidueRow(
            row_number=i + 1,
            ours=raw_ours[i],
            reference=raw_reference[i],
        )
        for i in remaining
        if i not in set(prefixed)
    )
    return CollationLadder(
        identical_as_deposited=AYAH_ROWS - differing,
        differing_as_deposited=differing,
        rungs=tuple(rungs),
        basmala_prefixed_rows=len(prefixed),
        residue=residue,
    )


def residue_rows(root: Path | None = None) -> tuple[ResidueRow, ...]:
    """البقيّةُ وحدَها؛ وهي الموضعُ الذي يُقال عنه «غيرُ محسوم» ولا يُقال لغيره."""

    return collation_ladder(root).residue


class GateStanding(Enum):
    """منزلةُ بوّابةٍ معروضةٍ بعد تشغيلها على البايتات المُودَعة."""

    REDERIVED_AS_SUBMITTED = "أُعيد اشتقاقُها فوافقت ما عُرِض"
    REDERIVED_WITH_A_NAMED_CONDITION = "أُعيد اشتقاقُها فوافقت بشرطٍ لم يُكتَب"
    REFUSED_FOR_ABSENT_REFERENCE_BYTES = "مرجعُها غيرُ مُودَعٍ فلا تُقرأ ههنا"
    REPLACED_BY_A_NAMED_COUNT = "أُبدِل تأجيلُها بعدٍّ مُسمًّى وبقيّةٍ مُسمّاة"
    SUSPENDED_FOR_ABSENT_MARKS = "مادّتُها غائبةٌ عن هذا النقل فتُعلَّق باسمها"


@dataclass(frozen=True, slots=True)
class SubmittedGate:
    """بوّابةٌ معروضةٌ بحالها المرويّة، وحالِها المقيسة، وسببِ الفرق."""

    gate: str
    submitted: str
    standing: GateStanding
    because: str

    def __post_init__(self) -> None:
        for field in (self.gate, self.submitted, self.because):
            if not field.strip():
                raise MirrorCollationError("بوّابةٌ بحقلٍ فارغٍ لا تُقرأ.")

    @property
    def is_read_as_submitted(self) -> bool:
        """هل قُرئت كما عُرِضت بلا شرطٍ ولا إبدال؟ وما عداه يُسمّى سببُه."""

        return self.standing is GateStanding.REDERIVED_AS_SUBMITTED


THE_SUBMITTED_GATES: Final[tuple[SubmittedGate, ...]] = (
    SubmittedGate(
        gate="تثبيت اللقطة المرجعية وبصمتها",
        submitted="PASS_ARCHIVED_SNAPSHOT",
        standing=GateStanding.REFUSED_FOR_ABSENT_REFERENCE_BYTES,
        because=(
            "لا بايتاتِ للّقطة المُؤرشَفة في هذه الشجرة؛ والمقابلةُ ههنا بين "
            "مُودَعَين مختومَين حاضرَين، فيُقرأ حكمُها عليهما لا عليها"
        ),
    ),
    SubmittedGate(
        gate="مقابلة جميع الأسطر وإبقاء الفروق",
        submitted="PASS_6236_ROWS",
        standing=GateStanding.REDERIVED_WITH_A_NAMED_CONDITION,
        because=(
            "المرجعُ 6,248 سطرًا لا 6,236؛ والموافقةُ تقع بعد إسقاط اثني عشرَ "
            "سطرًا من كتلة الناشر، وهو شرطٌ صوابٌ لكنّه لم يُكتَب"
        ),
    ),
    SubmittedGate(
        gate="تطابق الملف كله مع المرجع",
        submitted="DEFER_DIFFERENCES",
        standing=GateStanding.REPLACED_BY_A_NAMED_COUNT,
        because=(
            "الفروقُ 4,372 صفًّا، تُفَكُّ برتباتٍ مُعلَنةٍ إلى 111، منها 110 "
            "بسملةُ مطلعٍ وصفٌّ واحدٌ غيرُ مفسَّر؛ فلا يبقى ما يُؤجَّل جملةً"
        ),
    ),
    SubmittedGate(
        gate="مطابقة نوع الوقف",
        submitted="(مقطوعٌ في العرض)",
        standing=GateStanding.SUSPENDED_FOR_ABSENT_MARKS,
        because=(
            "مُودَعُنا خالٍ من علامات الوقف بالكلّيّة، والعدّادُ يُخرِج 4,578 "
            "منها على المُودَع الثاني؛ فالخلوُّ صفةُ النقل، ولا نوعَ يُطابَق"
        ),
    ),
)
"""البوّاباتُ الأربعُ المعروضةُ بحالها المقيسة؛ والمقطوعةُ تُقرأ بموضوعها."""


def gate_readings() -> tuple[SubmittedGate, ...]:
    """أحكامُ البوّابات المعروضة؛ ولا واحدةَ منها قُرئت كما عُرِضت."""

    return THE_SUBMITTED_GATES


THE_COLLATION_AT_MEASUREMENT: Final[CollationLadder] = CollationLadder(
    identical_as_deposited=1_864,
    differing_as_deposited=4_372,
    rungs=(
        FoldRung(name="علامةُ ترتيب البايتات", still_differing=4_372, removed=0),
        FoldRung(name="وسمُ الناشر <sel>", still_differing=4_372, removed=0),
        FoldRung(name="علاماتُ الوقف", still_differing=3_688, removed=684),
        FoldRung(name="الألفُ الخنجريّة", still_differing=2_299, removed=1_389),
        FoldRung(name="البياض", still_differing=2_129, removed=170),
        FoldRung(name="ترتيبُ التنوين مع الألف", still_differing=114, removed=2_015),
        FoldRung(name="طيُّ الهمزة المتّفقُ عليه", still_differing=111, removed=3),
    ),
    basmala_prefixed_rows=110,
    residue=(
        ResidueRow(
            row_number=3_189,
            ours=("إِنَّهُ مِن سُلَيْمَانَ وَإِنَّهُ " "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ"),
            reference="إِنَّهُ مِن سُلَيْمَانَ وَإِنَّهُ",
        ),
    ),
)
"""المقيسُ على المُودَعين المختومَين؛ تُعيده الاختباراتُ من البايتات."""
