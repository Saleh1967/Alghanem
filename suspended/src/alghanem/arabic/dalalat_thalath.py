"""الدلالاتُ الثلاث: مطابقةٌ وتضمُّنٌ والتزام، مفردةً مستقلّةً لا توسيعًا لغيرها.

نصُّ هذه الدلالات **مُزوَّدٌ بحروفه** في `sentence_card_source_texts` تحت مفتاح
`MUTABAQA_TADAMMUN_ILTIZAM_SHAKHSIYYA_THREE`، وقد سقط عن بند البطاقة نقصُ النقل
وبقي بلا مفردةٍ ولا دالّةِ اشتقاق. وهذه الوحدةُ تُقيم المفردةَ والدالّة.

**والمفردةُ ثلاثيةٌ مستقلّةٌ لا توسيعٌ لـ`DalalaChannel`** — وهذا شرطُ وجودها لا
تفصيلٌ فيها: `DalalaChannel` ثنائيةٌ مُجمَّدة (منطوق/مفهوم) بحارسٍ عند الاستيراد،
وفي بطاقة الجملة رفضٌ مُسمّى بعينه لهذا: `ThreeDalalatAreNotTheDalalaChannelPair`
— «ولا تُوسَّع إلى ثلاث لتستوعب هذه الدلالات؛ وتوسيعُ مفردةٍ مُجمَّدةٍ بعد رؤية
حالةٍ بعينها هو ما يمنعه `MarkerVocabularyIsFrozenBeforeItsText`». فالمفردتان
تبقيان اثنتين، وبينهما **دالّةُ اشتقاقٍ في اتّجاهٍ واحد** لا دمج.

**واتّجاهُ الاشتقاق واحدٌ لا ينعكس** (`ChannelDoesNotDetermineDalala`): من
الدلالةِ الثلاثية تُشتَقّ القناة (مطابقة → منطوق، تضمُّن → منطوق، التزام →
مفهوم)، ولا يُشتَقّ من القناة دلالةٌ بعينها؛ لأن `منطوق` يقابلها اثنتان فاشتقاقُ
إحداهما منها ترجيحٌ بلا مُرجِّح. والانعكاسُ مرفوضٌ بالبناء لا بالتحذير.

**والحصرُ مربوطٌ بالنصّ المُزوَّد لا مكتوبًا حرًّا**: تُفحَص عند الاستيراد وقوعُ
لفظِ كلِّ فرعٍ في النصّ المنقول بحروفه عبر `require_attested_excerpt`، فلو أُضيف
فرعٌ رابعٌ أو أُعيدت تسميةُ فرعٍ بما لا يُسمّيه النصُّ لَسقط الاستيراد بدل أن
يمضي الادّعاء صامتًا. وهذا أضعفُ من حصرٍ منصوصٍ بجملةِ عددٍ صريحة — كجملة
السبعة في `lafz_madlul_relation_formal` — وبقيّتُه مُسمّاةٌ في
`ENUMERATIVE_CLOSURE_IS_NOT_A_STATED_COUNT`: النصُّ المُزوَّد يذكر الثلاث ولا
يقول «ثلاثة لا رابع لها».

**و«اللزومُ شرطٌ وليس بموجِب» رفضٌ مُسمًّى لا عَلَمٌ منطقيّ**
(`IltizamConditionIsNotItsCause`): الدالُّ على اللازم هو **اللفظُ** نفسه، واللزومُ
شرطُ تفعيلٍ لا سببٌ للدلالة. فلا يُكتَب هنا حقلٌ منطقيٌّ للّزوم ولا تُقرأ الدلالةُ
من قوّته؛ ومن قرأ اللزومَ سببًا صار عنده كلُّ لازمٍ ذهنيٍّ دلالةً، وهو ما يُبطل
كونَ الدلالة دلالةَ لفظ. ويُضاف إليه ما نصّت عليه البطاقةُ نفسها:
`IltizamIsNotLogicalEntailment` — الالتزامُ لازمٌ ذهنيٌّ لا استلزامٌ منطقيٌّ `⊨`.

**وهذه الوحدة تسجيلٌ لا سلطة**: لا ولادة، ولا تجميد، ولا `E0`، ولا تستورد من
`kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from types import MappingProxyType
from typing import Final

from .mantuq_mafhum_ifada import DalalaChannel
from .sentence_card_source_texts import require_attested_excerpt

__all__ = [
    "CHANNEL_DOES_NOT_DETERMINE_DALALA_NOTE",
    "DALALAT_BY_CHANNEL",
    "DALALAT_THALATH_IS_NOT_A_GATE_NOTE",
    "DALALAT_THALATH_SOURCE_TEXT_KEY",
    "ENUMERATIVE_CLOSURE_IS_NOT_A_STATED_COUNT",
    "ILTIZAM_CONDITION_IS_NOT_ITS_CAUSE_NOTE",
    "ILTIZAM_IS_NOT_LOGICAL_ENTAILMENT_NOTE",
    "THREE_DALALAT_ARE_NOT_THE_CHANNEL_PAIR_NOTE",
    "DalalaKind",
    "DalalatThalathError",
    "SignificationReading",
    "channel_of_dalala",
    "dalalat_of_channel",
]


DALALAT_THALATH_SOURCE_TEXT_KEY: Final[str] = (
    "MUTABAQA_TADAMMUN_ILTIZAM_SHAKHSIYYA_THREE"
)


class DalalatThalathError(ValueError):
    """رفضٌ صريحٌ في قراءة الدلالات الثلاث؛ لا يُحمَل على أقرب فرعٍ مقبول."""


class DalalaKind(Enum):
    """الدلالاتُ الثلاث؛ مفردةٌ مستقلّةٌ مغلقةٌ لا تُدمَج في قناة الدلالة.

    مطابقةٌ: دلالةُ اللفظ على تمام مسمّاه. وتضمُّنٌ: دلالتُه على جزء المسمّى.
    والتزامٌ: دلالتُه على لازم معناه. وأسماؤها الثلاثةُ مفحوصةٌ عند الاستيراد
    بوقوعها في النصّ المُزوَّد بحروفه.
    """

    مطابقة = "مطابقة"
    تضمن = "تضمن"
    التزام = "التزام"


THREE_DALALAT_ARE_NOT_THE_CHANNEL_PAIR_NOTE: Final[str] = (
    "ThreeDalalatAreNotTheDalalaChannelPair: `DalalaChannel` ثنائيةٌ مُجمَّدة "
    "ولا تُوسَّع إلى ثلاثٍ لتستوعب هذه الدلالات؛ فالمفردتان اثنتان بينهما "
    "دالّةُ اشتقاقٍ في اتّجاهٍ واحد، لا مفردةٌ واحدةٌ وُسِّعت بعد رؤية نصّها"
)

CHANNEL_DOES_NOT_DETERMINE_DALALA_NOTE: Final[str] = (
    "ChannelDoesNotDetermineDalala: الاشتقاقُ من الدلالة إلى القناة لا العكس؛ "
    "فـ`منطوق` تقابلها المطابقةُ والتضمُّن معًا، واشتقاقُ إحداهما منها ترجيحٌ "
    "بلا مُرجِّح. و`dalalat_of_channel` تُرجِع ما يقابلها كلَّه ولا تختار منه"
)

ENUMERATIVE_CLOSURE_IS_NOT_A_STATED_COUNT: Final[str] = (
    "ENUMERATIVE_CLOSURE_IS_NOT_A_STATED_COUNT: النصُّ المُزوَّد يذكر الدلالات "
    "الثلاث ويُسمّيها، ولا يقول «ثلاثةٌ لا رابع لها» كما قالت جملةُ الحصر "
    "السباعية في `lafz_madlul_relation_formal`؛ فانغلاقُ الثلاثة هنا مربوطٌ "
    "بورود أسمائها في النصّ لا بجملةِ عددٍ مُصرَّحةٍ فيه، وهذا فارقٌ في قوّة "
    "السند يُسجَّل ولا يُطوى"
)

ILTIZAM_CONDITION_IS_NOT_ITS_CAUSE_NOTE: Final[str] = (
    "IltizamConditionIsNotItsCause: «اللزومُ شرطٌ وليس بموجِب» — الدالُّ هو "
    "اللفظُ نفسه، واللزومُ شرطُ تفعيلٍ لا سببٌ للدلالة؛ فلا حقلَ هنا يحمل "
    "قوّةَ اللزوم ولا تُقرأ الدلالةُ منها، ومن قرأ اللزومَ سببًا صار كلُّ "
    "لازمٍ ذهنيٍّ عنده دلالةً فبطل كونُها دلالةَ لفظ"
)

ILTIZAM_IS_NOT_LOGICAL_ENTAILMENT_NOTE: Final[str] = (
    "IltizamIsNotLogicalEntailment: الالتزامُ دلالةُ لفظٍ على لازمٍ ذهنيّ، لا "
    "الاستلزامَ المنطقيَّ `⊨`؛ وهذا أقربُ سوءِ قراءةٍ لهذه المفردة"
)

DALALAT_THALATH_IS_NOT_A_GATE_NOTE: Final[str] = (
    "تسجيلٌ لا سلطة: لا تُصدر هذه الوحدة ولادةً ولا حكمَ ولادة ولا تجميدًا ولا "
    "`E0`، ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه"
)


_CHANNEL_BY_DALALA: Final[dict[DalalaKind, DalalaChannel]] = {
    DalalaKind.مطابقة: DalalaChannel.منطوق,
    DalalaKind.تضمن: DalalaChannel.منطوق,
    DalalaKind.التزام: DalalaChannel.مفهوم,
}

_FORBIDDEN_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "count",
    "total",
    "score",
    "rank",
    "strength",
    "قوة",
    "entail",
    "verdict",
    "birth",
    "freeze",
)


def channel_of_dalala(kind: DalalaKind) -> DalalaChannel:
    """اشتقّ قناةَ الدلالة من جنسها؛ ولا موضعَ تُكتَب فيه القناةُ حرّةً."""

    if not isinstance(kind, DalalaKind):
        raise DalalatThalathError(
            "جنسُ الدلالة عضوٌ في مفردته الثلاثية المستقلّة؛ "
            f"{THREE_DALALAT_ARE_NOT_THE_CHANNEL_PAIR_NOTE}"
        )
    return _CHANNEL_BY_DALALA[kind]


def dalalat_of_channel(channel: DalalaChannel) -> tuple[DalalaKind, ...]:
    """ما يقابل القناةَ من الدلالات كلَّه؛ ولا تُختار منه واحدةٌ ترجيحًا."""

    if not isinstance(channel, DalalaChannel):
        raise DalalatThalathError(
            "القناةُ من مفردة `DalalaChannel` وحدها، مستورَدةً لا منسوخة."
        )
    return tuple(kind for kind in DalalaKind if _CHANNEL_BY_DALALA[kind] is channel)


@dataclass(frozen=True, slots=True)
class SignificationReading:
    """قراءةُ دلالةٍ واحدة: لفظُها، والمعنى المقروءُ منها، وجنسُ الدلالة.

    ولا حقلَ للقناة: تُشتَقّ من الجنس في موضعها الواحد ولا تُكتَب هنا ثانية،
    فالكتابةُ تسمح بقراءةٍ تخالف جنسَها ولا يردُّها شيء.
    """

    lafz: str
    read_meaning: str
    kind: DalalaKind

    def __post_init__(self) -> None:
        for value, label in (
            (self.lafz, "اللفظُ المقروء"),
            (self.read_meaning, "المعنى المقروء"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise DalalatThalathError(f"{label} نصٌّ غير فارغ.")
        if not isinstance(self.kind, DalalaKind):
            raise DalalatThalathError("جنسُ الدلالة عضوٌ في مفردته الثلاثية المغلقة.")

    @property
    def channel(self) -> DalalaChannel:
        """القناةُ مُشتَقّةً من الجنس وحده، لا مكتوبةً في حقل."""

        return channel_of_dalala(self.kind)

    @property
    def is_mantuq(self) -> bool:
        """أمنطوقٌ هو؟ مُشتَقٌّ من القناة المُشتَقّة، لا حقلٌ ثالثٌ يُكتَب."""

        return self.channel is DalalaChannel.منطوق


def _assert_no_fields_matching(markers: tuple[str, ...]) -> None:
    for field in fields(SignificationReading):
        for marker in markers:
            if marker in field.name.lower():
                raise RuntimeError(
                    f"SignificationReading يحمل حقلاً محظورًا: {field.name}"
                )


if len(DalalaKind) != 3:  # pragma: no cover - guard
    raise RuntimeError("الدلالاتُ ثلاثٌ في هذه المفردة المستقلّة.")
if len(DalalaChannel) != 2:  # pragma: no cover - guard
    raise RuntimeError(THREE_DALALAT_ARE_NOT_THE_CHANNEL_PAIR_NOTE)
if set(_CHANNEL_BY_DALALA) != set(DalalaKind):  # pragma: no cover - guard
    raise RuntimeError("اشتقاقُ القناة غيرُ تامٍّ على الدلالات الثلاث.")
if set(_CHANNEL_BY_DALALA.values()) != set(DalalaChannel):  # pragma: no cover - guard
    raise RuntimeError(
        "القناتان مقصودتان معًا في الاشتقاق؛ وقناةٌ بلا دلالةٍ تقابلها فراغ."
    )
for _kind in DalalaKind:  # pragma: no cover - guard
    require_attested_excerpt(DALALAT_THALATH_SOURCE_TEXT_KEY, _kind.value)
_assert_no_fields_matching(_FORBIDDEN_FIELD_MARKERS)

DALALAT_BY_CHANNEL: Final[MappingProxyType[DalalaChannel, tuple[DalalaKind, ...]]] = (
    MappingProxyType(
        {channel: dalalat_of_channel(channel) for channel in DalalaChannel}
    )
)
