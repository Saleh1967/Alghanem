"""سجلُّ الأختام: ختمٌ بلا مولِّدٍ حيٍّ قبرٌ لا ختم.

كان الرقمُ المنقولُ في هذه الشجرة يُحرَس — إن حُرِس — بمصادمةٍ مكتوبةٍ في
وحدته وحدَها. فما كُتِب له كاشفٌ حُرِس، وما لم يُكتَب بقي في النثر ينزاح
صامتًا مع نموّ الشجرة. وليست العلّةُ في التجميد: التجميدُ معقِلٌ سليم. العلّةُ
أن يبقى الرقمُ **مجمَّدًا بلا مولِّدٍ يقابله**، فيُقارَن ويُطبَع ولا يولَد.

فالختمُ ههنا ثلاثةٌ لا ينفكّ عنها: **اسمٌ · مولِّدٌ حيٌّ · موضعُ نقله**. ولا
يحمل الختمُ قيمةً في نفسه: القيمةُ تبقى حيث كُتبت — ثابتًا في وحدتها أو سطرًا
في نثرها — ويبقى المولِّدُ حيث عُرِّف، وكلُّ ما يفعله السجلُّ أن يجمع الجانبين
فيُصادما ويُسمّى الفارقُ باسم حقلِه. ولو حمل السجلُّ نسخةً ثانيةً من الرقم
لصار هو نفسُه القبرَ الذي جاء يفتحه
(`A_REGISTRY_THAT_STORES_A_VALUE_IS_A_SECOND_GRAVE`).

وتُفرَّق الأختامُ ثلاثةَ أجناس، ولا يُخلَط جنسٌ بجنس::

    AGeneratedSeal   != ATranscribedSeal   != AQuotedWitness

* `GENERATED` — ثابتٌ منقولٌ يقابله مولِّدٌ حيّ، فيُصادَم حقلًا حقلًا.
* `TRANSCRIBED` — رقمٌ يولَّد حيًّا ثمّ يُنقَل إلى نثرٍ بشريّ، فيُطلَب حضورُ
  صورته المولَّدة في ذلك النثر بعينه؛ وغيابُها انزياحُ نثرٍ لا انزياحُ قياس.
* `QUOTED` — وارِدٌ من خارجٍ لا مولِّدَ له عندنا: يُعلَن بمصدره و**لا
  يُصادَم**، إذ ليس ادّعاءَ هذه الشجرة حتى يُحاسَب حسابَها
  (`A_QUOTATION_IS_NOT_A_CLAIM_OF_THIS_TREE`).

وهذه الوحدةُ **عدّةُ محاسبةٍ لا دعوى لغويّة**: لا تقيس حرفًا ولا حركة، ولا
ترفع حظرًا ولا تفكّ تجميدًا؛ وإنّما تُلزِم كلَّ رقمٍ أن يُسمّي مولِّدَه.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator, Mapping
from dataclasses import dataclass
from enum import Enum
from typing import Final

__all__ = [
    "A_QUOTATION_IS_NOT_A_CLAIM_OF_THIS_TREE",
    "A_REGISTRY_THAT_STORES_A_VALUE_IS_A_SECOND_GRAVE",
    "A_SEAL_WITHOUT_A_LIVE_GENERATOR_IS_A_GRAVE_NOT_A_SEAL",
    "Seal",
    "SealError",
    "SealGenus",
    "SealReading",
    "SealRegistry",
    "SealVerdict",
    "TWO_SIDES_THAT_NAME_DIFFERENT_FIELDS_DO_NOT_COLLIDE",
]


class SealError(Exception):
    """رفضٌ مُسمّى في سجلّ الأختام؛ ولا يُبتلَع خللٌ ههنا بصمت."""


A_SEAL_WITHOUT_A_LIVE_GENERATOR_IS_A_GRAVE_NOT_A_SEAL: Final[str] = (
    "A_SEAL_WITHOUT_A_LIVE_GENERATOR_IS_A_GRAVE_NOT_A_SEAL: ختمٌ لا أمرَ "
    "توليدٍ معه رقمٌ مجمَّدٌ يُقارَن ولا يولَد؛ وذاك قبرٌ لا معقِل."
)

A_REGISTRY_THAT_STORES_A_VALUE_IS_A_SECOND_GRAVE: Final[str] = (
    "A_REGISTRY_THAT_STORES_A_VALUE_IS_A_SECOND_GRAVE: سجلٌّ يحمل نسخةً "
    "ثانيةً من الرقم يصير هو نفسُه ما جاء يفتحه؛ فالختمُ يُشير ولا يَخزُن."
)

A_QUOTATION_IS_NOT_A_CLAIM_OF_THIS_TREE: Final[str] = (
    "A_QUOTATION_IS_NOT_A_CLAIM_OF_THIS_TREE: الواردُ من خارجٍ يُعلَن بمصدره "
    "ولا يُصادَم؛ ومحاسبتُه حسابَ المولَّد ادّعاءُ ملكيّةٍ لم تقع."
)

TWO_SIDES_THAT_NAME_DIFFERENT_FIELDS_DO_NOT_COLLIDE: Final[str] = (
    "TWO_SIDES_THAT_NAME_DIFFERENT_FIELDS_DO_NOT_COLLIDE: جانبان يسمّيان "
    "حقولًا مختلفةً لا يتصادمان؛ والفارقُ حينئذٍ فارقُ جدولين لا فارقُ رقم."
)


class SealGenus(Enum):
    """جنسُ الختم: أهو مولَّدٌ مصادَم، أم نقلٌ في نثر، أم شاهدٌ وارد؟"""

    GENERATED = "مولَّدٌ ومصادَم"
    TRANSCRIBED = "منقولٌ إلى نثر"
    QUOTED = "شاهدٌ لا يولَّد"


@dataclass(frozen=True)
class SealReading:
    """حقلٌ واحد: ما نُقل، وما وَلَّده القرصُ الآن."""

    field: str
    transcribed: str
    measured: str

    def __post_init__(self) -> None:
        if not self.field.strip():
            raise SealError("حقلٌ بلا اسمٍ لا يُصادَم.")

    @property
    def agrees(self) -> bool:
        """أيطابق المنقولُ ما يولِّده القرصُ الآن، حرفًا بحرف؟"""

        return self.transcribed == self.measured


@dataclass(frozen=True)
class Seal:
    """ختمٌ = اسمٌ · أمرُ توليدٍ حيّ · موضعُ نقله؛ ولا قيمةَ محمولةٌ فيه."""

    name: str
    genus: SealGenus
    origin: str
    generate: Callable[[], Mapping[str, str]]
    transcription: Callable[[], Mapping[str, str]]

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise SealError("ختمٌ بلا اسمٍ لا يُسجَّل.")
        if not self.origin.strip():
            raise SealError(
                "ختمٌ بلا أمرِ توليدٍ مُعلَن: "
                f"{A_SEAL_WITHOUT_A_LIVE_GENERATOR_IS_A_GRAVE_NOT_A_SEAL}"
            )
        for side in (self.generate, self.transcription):
            if not callable(side):
                raise SealError(
                    "جانبا الختم يُستدعَيان عند كلّ مصادمة ولا يُخزَنان: "
                    f"{A_REGISTRY_THAT_STORES_A_VALUE_IS_A_SECOND_GRAVE}"
                )

    def collide(self) -> tuple[SealReading, ...]:
        """يستدعي الجانبين الآن — لا يقرأ خزينًا — ويُسمّي كلَّ حقل."""

        transcribed = dict(self.transcription())
        measured = dict(self.generate())
        if not transcribed:
            raise SealError(f"ختمٌ بلا حقلٍ يحرسه: {self.name}")
        if set(transcribed) != set(measured):
            raise SealError(
                f"{self.name}: {TWO_SIDES_THAT_NAME_DIFFERENT_FIELDS_DO_NOT_COLLIDE}"
            )
        return tuple(
            SealReading(
                field=field,
                transcribed=transcribed[field],
                measured=measured[field],
            )
            for field in sorted(transcribed)
        )


@dataclass(frozen=True)
class SealVerdict:
    """حكمُ ختمٍ بعد مصادمته: قراءاتُه، وما انزاح منها مسمًّى."""

    seal: Seal
    readings: tuple[SealReading, ...]

    @property
    def is_quoted(self) -> bool:
        """أشاهدٌ وارِدٌ هو؟ فالشاهدُ يُعلَن ولا يُصادَم."""

        return self.seal.genus is SealGenus.QUOTED

    @property
    def discrepancies(self) -> tuple[SealReading, ...]:
        """الحقولُ المنزاحةُ وحدَها، وكلُّها مسمّاةٌ باسمها لا مبتلَعة."""

        if self.is_quoted:
            return ()
        return tuple(reading for reading in self.readings if not reading.agrees)

    @property
    def has_drifted(self) -> bool:
        """أانزاح هذا الختمُ عمّا يولِّده القرصُ الآن؟"""

        return bool(self.discrepancies)


@dataclass(frozen=True)
class SealRegistry:
    """سجلُّ أختامٍ لا يحمل رقمًا: يجمع الجانبين ويصادمهما عند كلّ نداء."""

    seals: tuple[Seal, ...]

    def __post_init__(self) -> None:
        if not self.seals:
            raise SealError("سجلٌّ بلا ختمٍ واحدٍ لا يحرس شيئًا.")
        names = [seal.name for seal in self.seals]
        if len(set(names)) != len(names):
            raise SealError("اسمُ ختمٍ مكرَّرٌ؛ ولا يُحرَس رقمان باسمٍ واحد.")

    def __iter__(self) -> Iterator[Seal]:
        return iter(self.seals)

    def collide_all(self) -> tuple[SealVerdict, ...]:
        """يعيد توليدَ كلّ ختمٍ ويصادمه، فلا يمرّ رقمٌ بلا مولِّدٍ يقابله."""

        return tuple(
            SealVerdict(seal=seal, readings=seal.collide()) for seal in self.seals
        )

    def drifted(self) -> tuple[SealVerdict, ...]:
        """الأختامُ المنزاحةُ وحدَها؛ وكلُّ انزياحٍ يستلزم فاتورةً معلَنة."""

        return tuple(verdict for verdict in self.collide_all() if verdict.has_drifted)

    def genera(self) -> Mapping[SealGenus, int]:
        """تعدادُ الأختام بأجناسها، مولَّدًا من السجلّ لا منقولًا عنه."""

        tally: dict[SealGenus, int] = {genus: 0 for genus in SealGenus}
        for seal in self.seals:
            tally[seal.genus] += 1
        return tally
