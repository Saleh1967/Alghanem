"""العدُّ الخامّ لحالات الألف: جدولُ وقوعٍ كاملٌ لا حكمٌ على دعوى.

هذه هي **الخطوةُ الأولى** من بروتوكول اليقين المباشر
(`DirectCertaintyStep.RAW_COUNT`) مُنفَّذةً على نصٍّ عربيٍّ واحدٍ مُودَعٍ
بحروفه، لا أكثر. وكانت خمسُ خطواتٍ من الستّ بلا كودٍ في هذه الشجرة حين سجَّلت
المرحلةُ الرابعة عشرة ذلك في `STEP_BINDING_DISCOVERY`؛ وهذه الوحدةُ تملأ صفًّا
واحدًا من تلك الخمسة، وتترك الأربعةَ الباقية خاليةً كما هي::

    OneStepImplemented != ProtocolImplemented
    ZeroExceptionsHere != ClaimEstablished

**والدعوى المقيسة مكتوبةٌ نصًّا قبل عدِّها** في `ALIF_STATE_CLAIM`: أنّ الحاملَ
«ا» لا يحمل في مواضعه واحدةً من {الفتحة، الضمّة، الكسرة}، وأنّ كلَّ حاملٍ آخر
يحمل إحداها في مواضع حقيقية. وهي **فرضيةٌ تُقاس، لا قاعدةٌ تُفترَض**؛ وهذه
الوحدةُ تُخرِج عددًا وجدولًا، ولا تُخرِج حكمًا بصدقها ولا بكذبها
(`A_COUNT_IS_NOT_A_VERDICT`).

**والاستثناءُ يُسجَّل ولا يُخفى.** كلُّ ذرّةٍ حاملُها ألفٌ وفي حالتها واحدةٌ من
الثلاث تُحفَظ صفًّا مُسمًّى في `alif_rows_carrying_a_short_vowel`، ولا تُطرَح
من الجدول ولا تُلخَّص إلى رقم؛ وهو منوالُ `NormalizationResidualTable` نفسُه:
صفٌّ لكلّ وقوع، الموافقُ والمخالفُ سواء.

**وترتيبُ الخطوات مُلزِم، فالخطوةُ صفر تُشغَّل قبل العدّ لا بعده**:
`run_raw_count_on_the_deposited_fatiha` يُمرِّر الحروفَ على كاشف التلوّث
(`alghanem.arabic.encoding.contamination_gate.scan_lines`) ويرفض العدَّ إن ردَّ
الكاشفُ رمزًا واحدًا؛ فالعدُّ على نصٍّ لم يجتز الكاشفَ عدٌّ على ما لم يُعرَف.

**ومدخلُ هذه الوحدة بلا وسائط عن قصد.** `run_step` يستدعي مُعيدَ الإنتاج بلا
وسيط، فما وجب له وسيطٌ لا يصلح مُعيدًا للإنتاج مهما كان هو كودَ الخطوة؛ وهو
الحدُّ الذي أسقط `scan_lines` و`scan_tokens` وسمّاه
`THE_PROTOCOL_TEST_IS_NARROWED_TO_ZERO_ARGUMENT_ENTRY_POINTS`. فالعدُّ نفسُه
`count_alif_states` يأخذ سطورَه وسيطًا ويصلح لأيّ نصّ، والمدخلُ عديمُ الوسائط
يُثبِّت النصَّ المُودَع ويستدعيه.

**ولا سلطةَ لهذه الوحدة**: لا ولادةَ، ولا حكمَ ولادةٍ، ولا تجميد، ولا تقرؤها
بوّابةٌ في `kernel/`، ولا تُعدِّل `assess_freeze`. **ولا تستورد طبقةَ البرنامج**:
تسجيلُ هذا العدّ بآلة قاعدة النتيجتين قائمٌ في
`alghanem.program.alif_state_raw_count_record`، لأنّ اتّجاه الاعتماد بين
الطبقتين واحدٌ لا يُعكَس.
"""

from __future__ import annotations

import unicodedata
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Final

from .encoding.contamination_gate import scan_lines
from .fatiha_source_text import FATIHA_LINES, FATIHA_SOURCE_ID

__all__ = [
    "ALIF",
    "ALIF_STATE_CLAIM",
    "ALIF_STATE_RAW_COUNT_NAMED_RESIDUALS",
    "A_COUNT_IS_NOT_A_VERDICT",
    "ONE_TEXT_IS_NOT_A_CORPUS",
    "SHORT_VOWELS",
    "SUPERSCRIPT_ALEF_IS_READ_AS_A_MARK_NOT_A_CARRIER",
    "THE_CARRIER_SET_IS_DECLARED_NOT_DERIVED",
    "AlifStateRawCountError",
    "AlifStateRawCountTable",
    "CarrierAtomRow",
    "UnattachedMarkRow",
    "count_alif_states",
    "decompose_lines",
    "run_raw_count_on_the_deposited_fatiha",
]


class AlifStateRawCountError(ValueError):
    """سُئل العدُّ عمّا لا يقوم به؛ ولا يُحمَل على أقرب حالةٍ مقبولة."""


# --- الحوامل والحالات، مُعلَنةً لا مُستنبَطة ----------------------------------


ALIF: Final[str] = "\u0627"
"""الألفُ المجرّدة وحدَها؛ وألفُ الوصل والمقصورةُ والممدودةُ رموزٌ أُخَر."""


SHORT_VOWELS: Final[tuple[str, ...]] = (
    "\u064e",  # فتحة
    "\u064f",  # ضمّة
    "\u0650",  # كسرة
)
"""الحالاتُ الثلاث المقيسة؛ والسكونُ والشدّةُ والتنوينُ خارجَها عن قصد."""


ALIF_STATE_CLAIM: Final[str] = (
    "لكلّ ذرّة (حامل، حالة) في تفكيك كلمةٍ عربيةٍ مُشكَّلة: إن كان الحاملُ "
    "«ا» فحالتُها ليست واحدةً من {فتحة، ضمّة، كسرة}؛ وكلُّ حاملٍ آخر يحمل "
    "إحدى الثلاث في مواضع حقيقيةٍ من النصّ"
)
"""الدعوى المقيسة، مكتوبةً قبل العدّ لا مُستخلَصةً منه."""


# --- صفُّ الذرّة الواحدة -------------------------------------------------------


@dataclass(frozen=True)
class CarrierAtomRow:
    """حاملٌ واحدٌ وما لحقه من علامات، بموضعه في السطر والكلمة."""

    line_index: int
    word_index: int
    word: str
    carrier: str
    state_marks: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.line_index < 0 or self.word_index < 0:
            raise AlifStateRawCountError("موضعُ الذرّة لا يكون سالبًا.")
        if len(self.carrier) != 1:
            raise AlifStateRawCountError("حاملُ الذرّة رمزٌ واحد.")
        for mark in self.state_marks:
            if len(mark) != 1:
                raise AlifStateRawCountError("علامةُ الحالة رمزٌ واحد.")

    @property
    def is_alif_carrier(self) -> bool:
        """أحاملُ هذه الذرّة هو الألفُ المجرّدة بعينها؟"""
        return self.carrier == ALIF

    @property
    def short_vowels(self) -> tuple[str, ...]:
        """ما في حالة هذه الذرّة من الحالات الثلاث، بترتيب ورودها."""
        return tuple(mark for mark in self.state_marks if mark in SHORT_VOWELS)

    @property
    def carries_short_vowel(self) -> bool:
        """أفي حالة هذه الذرّة واحدةٌ من الثلاث؟"""
        return bool(self.short_vowels)


@dataclass(frozen=True)
class UnattachedMarkRow:
    """علامةٌ وردت قبل أيّ حاملٍ في كلمتها؛ تُحفَظ ولا تُطرَح."""

    line_index: int
    word_index: int
    word: str
    mark: str

    def __post_init__(self) -> None:
        if len(self.mark) != 1:
            raise AlifStateRawCountError("العلامةُ غيرُ المتّصلة رمزٌ واحد.")


def _is_carrier(char: str) -> bool:
    return unicodedata.category(char) == "Lo"


def _is_mark(char: str) -> bool:
    return unicodedata.category(char) == "Mn"


def decompose_lines(
    lines: Iterable[str],
) -> tuple[tuple[CarrierAtomRow, ...], tuple[UnattachedMarkRow, ...], tuple[str, ...]]:
    """فكِّك السطورَ إلى ذرّات (حامل، حالة)، واحفظ ما لم ينتظم منها.

    ويُرَدّ ثلاثةُ أشياء لا واحد: صفوفُ الذرّات بترتيبها، والعلاماتُ التي سبقت
    حاملَها، والرموزُ التي ليست حاملًا ولا علامةً (كالتطويل والأرقام)؛ فطرحُ
    أيّها بصمتٍ يجعل العددَ أنظفَ ممّا رآه القارئ.
    """
    atoms: list[CarrierAtomRow] = []
    unattached: list[UnattachedMarkRow] = []
    unclassified: list[str] = []
    for line_index, line in enumerate(lines):
        for word_index, word in enumerate(line.split()):
            carrier: str | None = None
            marks: list[str] = []

            def flush(
                carrier: str | None,
                marks: list[str],
                line_index: int = line_index,
                word_index: int = word_index,
                word: str = word,
            ) -> None:
                if carrier is None:
                    return
                atoms.append(
                    CarrierAtomRow(
                        line_index=line_index,
                        word_index=word_index,
                        word=word,
                        carrier=carrier,
                        state_marks=tuple(marks),
                    )
                )

            for char in word:
                if _is_carrier(char):
                    flush(carrier, marks)
                    carrier = char
                    marks = []
                elif _is_mark(char):
                    if carrier is None:
                        unattached.append(
                            UnattachedMarkRow(
                                line_index=line_index,
                                word_index=word_index,
                                word=word,
                                mark=char,
                            )
                        )
                    else:
                        marks.append(char)
                else:
                    unclassified.append(char)
            flush(carrier, marks)
    return tuple(atoms), tuple(unattached), tuple(unclassified)


# --- الجدول: صفٌّ لكلّ وقوع، والعددُ مُشتَقٌّ منه لا مكتوبٌ بجانبه -------------


@dataclass(frozen=True)
class AlifStateRawCountTable:
    """عدٌّ خامٌّ واحد: اسمُ مصدره، وكلُّ ذرّةٍ قُرئت فيه، وما لم ينتظم.

    ولا حقلَ حكمٍ هنا: لا «مُثبَت» ولا «مردود». الأعدادُ خصائصُ مُشتقّةٌ من
    الصفوف، فمن أراد مراجعتَها راجع الصفوف لا الرقم.
    """

    source_id: str
    rows: tuple[CarrierAtomRow, ...]
    unattached_marks: tuple[UnattachedMarkRow, ...]
    unclassified_codepoints: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.source_id.strip():
            raise AlifStateRawCountError("عدٌّ بلا اسمِ مصدرٍ لا يُراجَع.")

    @property
    def alif_rows(self) -> tuple[CarrierAtomRow, ...]:
        """كلُّ ذرّةٍ حاملُها ألفٌ مجرّدة."""
        return tuple(row for row in self.rows if row.is_alif_carrier)

    @property
    def alif_rows_carrying_a_short_vowel(self) -> tuple[CarrierAtomRow, ...]:
        """استثناءاتُ الدعوى إن وُجدت: ألفٌ في حالتها واحدةٌ من الثلاث.

        وخلوُّ هذا الحقل في نصٍّ واحدٍ ليس إثباتًا للدعوى، وامتلاؤه ليس إبطالًا
        لها؛ هو موضعٌ مُسمًّى يُقرأ، وذلك كلُّ ما يقوله العدُّ الخامّ.
        """
        return tuple(row for row in self.alif_rows if row.carries_short_vowel)

    @property
    def other_carrier_rows(self) -> tuple[CarrierAtomRow, ...]:
        """كلُّ ذرّةٍ حاملُها غيرُ الألف المجرّدة."""
        return tuple(row for row in self.rows if not row.is_alif_carrier)

    @property
    def other_rows_carrying_a_short_vowel(self) -> tuple[CarrierAtomRow, ...]:
        """الشقُّ الثاني من الدعوى مقيسًا: حواملُ أُخَر حملت إحدى الثلاث."""
        return tuple(row for row in self.other_carrier_rows if row.carries_short_vowel)

    @property
    def distinct_carriers(self) -> tuple[str, ...]:
        """الحواملُ المختلفةُ التي وردت، بترتيب أوّل ورودها."""
        return tuple(dict.fromkeys(row.carrier for row in self.rows))


def count_alif_states(
    lines: Iterable[str], *, source_id: str
) -> AlifStateRawCountTable:
    """عُدَّ ذرّات (حامل، حالة) في هذه السطور واحفظ كلَّ صفٍّ قُرئ.

    وهذه هي الدالّةُ العامّة: تأخذ أيّ نصٍّ عربيٍّ مُشكَّل، ولا تعرف الفاتحةَ
    ولا سواها. وتثبيتُ نصٍّ بعينه شأنُ المدخل عديم الوسائط وحده.
    """
    atoms, unattached, unclassified = decompose_lines(lines)
    return AlifStateRawCountTable(
        source_id=source_id,
        rows=atoms,
        unattached_marks=unattached,
        unclassified_codepoints=unclassified,
    )


# --- المدخلُ عديمُ الوسائط: الخطوةُ صفر أوّلًا، ثمّ العدّ ---------------------


def run_raw_count_on_the_deposited_fatiha() -> AlifStateRawCountTable:
    """شغِّل كاشفَ التلوّث على النصّ المُودَع، ثمّ عُدَّ ذرّاته.

    وهو مُعيدُ إنتاج الخطوة الأولى كما يستدعيه `run_step`: بلا وسائط، ويُخرِج
    الجدولَ نفسَه لا وصفَه. والعدُّ يقف إن ردَّ الكاشفُ رمزًا واحدًا، فترتيبُ
    الخطوتين قائمٌ في الكود لا في التصريح.
    """
    report = scan_lines(FATIHA_LINES)
    rejected = report.rejected
    if rejected:
        raise AlifStateRawCountError(
            "ردَّ كاشفُ التلوّث رموزًا من النصّ المُودَع، ولا يبدأ عدٌّ خامٌّ "
            "على ما لم يجتز الخطوةَ صفر: " + "، ".join(row.token for row in rejected)
        )
    return count_alif_states(FATIHA_LINES, source_id=FATIHA_SOURCE_ID)


# --- ما لا يحسمه هذا العدّ، مُسمًّى -------------------------------------------


A_COUNT_IS_NOT_A_VERDICT: Final[str] = (
    "A_COUNT_IS_NOT_A_VERDICT: هذه الوحدةُ تُخرِج جدولًا وأعدادًا، ولا تُخرِج "
    "حكمًا بصدق الدعوى ولا بكذبها؛ وقراءةُ خلوّ الاستثناءات إثباتًا تجعل "
    "العدَّ شهادةً لنفسه"
)

ONE_TEXT_IS_NOT_A_CORPUS: Final[str] = (
    "ONE_TEXT_IS_NOT_A_CORPUS: المقيسُ نصٌّ واحدٌ قصيرٌ مُودَعٌ في الشجرة؛ "
    "وما صحّ فيه لا يمتدّ إلى العربية ولا إلى رسمٍ آخر، والامتدادُ يحتاج "
    "نصوصًا أُخَر تُودَع ويُعاد العدُّ عليها"
)

THE_CARRIER_SET_IS_DECLARED_NOT_DERIVED: Final[str] = (
    "THE_CARRIER_SET_IS_DECLARED_NOT_DERIVED: «الحاملُ حرفٌ فئتُه Lo، والحالةُ "
    "علامةٌ فئتُها Mn» قاعدةٌ مكتوبةٌ في هذه الوحدة مأخوذةٌ من قاعدة يونيكود، "
    "ولا تُشتَقّ من خاصّةٍ في العربية؛ فالهمزةُ المرسومةُ على ألفٍ (أ، إ) "
    "تُقرأ هنا حاملًا مستقلًّا لا ألفًا"
)

SUPERSCRIPT_ALEF_IS_READ_AS_A_MARK_NOT_A_CARRIER: Final[str] = (
    "SUPERSCRIPT_ALEF_IS_READ_AS_A_MARK_NOT_A_CARRIER: الألفُ الخنجرية "
    "(U+0670) فئتُها Mn فتُقرأ حالةً لا حاملًا، وألفُ الوصل (U+0671) والألفُ "
    "المقصورة رموزٌ غيرُ U+0627 فلا تدخل عدَّ الألف هنا؛ وهذا حدُّ القياس "
    "لا نتيجتُه"
)

ALIF_STATE_RAW_COUNT_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "A_COUNT_IS_NOT_A_VERDICT": A_COUNT_IS_NOT_A_VERDICT,
    "ONE_TEXT_IS_NOT_A_CORPUS": ONE_TEXT_IS_NOT_A_CORPUS,
    "THE_CARRIER_SET_IS_DECLARED_NOT_DERIVED": (
        THE_CARRIER_SET_IS_DECLARED_NOT_DERIVED
    ),
    "SUPERSCRIPT_ALEF_IS_READ_AS_A_MARK_NOT_A_CARRIER": (
        SUPERSCRIPT_ALEF_IS_READ_AS_A_MARK_NOT_A_CARRIER
    ),
}
"""ما لا يحسمه هذا العدّ، مُسمًّى هنا لا متروكًا ليُفترَض."""
