"""فحصُ العيّنة الخامّ: قراءةُ صفوف العدّ صفًّا صفًّا قبل أن يُستبعَد شيء.

هذه هي **الخطوةُ الثانية** من بروتوكول اليقين المباشر
(`DirectCertaintyStep.RAW_SAMPLE_INSPECTION`) مُنفَّذةً على الجدول الذي أخرجته
الخطوةُ الأولى، لا على نصٍّ يُعاد عدُّه::

    ReadingTheRows != RecountingTheText
    OneMoreStepFilled != ProtocolImplemented

**ولا تُعيد هذه الوحدةُ العدَّ ولا تمسّ كودَه.** `alif_state_raw_count` يُخرِج
`AlifStateRawCountTable`، وهذه الوحدةُ تقرؤه: تُخرِج لكلّ صفِّ ألفٍ سياقَه الذي
يقرأ به الإنسانُ — سطرَ الآية، وموضعَه فيه، وجارَيه عن يمينه وشماله — ولا
تُجمِّع ولا تُرشِّح ولا تكتب شرطَ استبعاد؛ فالشرطُ خطوةٌ ثالثةٌ لا تُستبقَ ولو
بدا الفحصُ يُلوِّح بها (`INSPECTION_WRITES_NO_CONDITION`).

**وصفوفُ الألف تُقرأ كلُّها لا عيّنةٌ منها.** المُودَعُ صغيرٌ، فالثلاثةُ
والعشرون كاملةً هي المُخرَج، و«العيّنة» في اسم الخطوة لا تصدق عليها
(`FULL_SET_NOT_A_SAMPLE`)؛ والعيّنةُ الحقيقيةُ هي شريحةُ الحوامل الأُخَر،
ومبدأُ اختيارها مكتوبٌ في الكود ومحفوظٌ في السجلّ لا مشروحٌ في تعليق
(`ONE_ROW_PER_VERSE_LINE_IS_THE_SLICE_PRINCIPLE`).

**والمقروءُ بعينه هو ما تُحذِّر منه بقيّةُ الرسم.** `RASM_IS_IMLAI_NOT_UTHMANI`
في `fatiha_source_text` يقول إنّ الفرقَ بين الرسمَين يقع في حوامل الألف نفسِها،
فيُقرأ لكلّ صفٍّ **أيُّ صورةٍ من صورتَي الألف** وردت فيه: المجرّدةُ «ا» أم ألفُ
الوصل «ٱ»، حقلًا على الصفّ لا رقمًا مُلخَّصًا. وخلوُّ المُودَع من ألف الوصل
بالكلّية ليس صفرًا يُمرّ عليه: يُقيَّد صفًّا مُسمًّى
(`WASLA_FORM_ABSENT_FROM_THIS_DEPOSIT`)، لأنّ قياسًا لم يلقَ الصورةَ التي
تُحذِّر منها البقيّةُ أضيقُ ممّا يبدو، وضيقُه يُقال ولا يُترَك ليُفترَض. ولا
تُغلِق هذه القراءةُ تلك البقيّة (`RASM_RESIDUAL_STAYS_OPEN`).

**ووحدةٌ مستقلّةٌ لا امتدادٌ في وحدة العدّ**، اتّباعًا لما قرأته الشجرةُ من
منوالها: المرحلةُ السابقة أودعت نصَّها في وحدةٍ وعَدَّته في وحدةٍ أُخرى، فشأنٌ
واحدٌ لكلّ وحدة.

**ولا سلطةَ لهذه الوحدة**: لا حكمَ، ولا ولادة، ولا تجميد، ولا حقلَ «مقبول /
مردود» في صفٍّ من صفوفها، ولا تقرؤها بوّابةٌ في `kernel/`. **ولا تستورد طبقةَ
البرنامج**، فاتّجاهُ الاعتماد بين الطبقتين واحدٌ لا يُعكَس.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from enum import Enum
from typing import Final

from .alif_state_raw_count import (
    ALIF,
    AlifStateRawCountTable,
    CarrierAtomRow,
    run_raw_count_on_the_deposited_fatiha,
)

__all__ = [
    "ALIF_CARRIER_INSPECTION_NAMED_RESIDUALS",
    "FULL_SET_NOT_A_SAMPLE",
    "INSPECTION_WRITES_NO_CONDITION",
    "ONE_ROW_PER_VERSE_LINE_IS_THE_SLICE_PRINCIPLE",
    "RASM_RESIDUAL_STAYS_OPEN",
    "THE_SLICE_IS_CHOSEN_NOT_REPRESENTATIVE",
    "THE_VERSE_LINE_IS_REBUILT_FROM_THE_COUNTED_WORDS",
    "WASLA_FORM_ABSENT_FROM_THIS_DEPOSIT",
    "WASL_ALIF",
    "AlifCarrierInspection",
    "AlifCarrierInspectionError",
    "AlifCarrierSample",
    "RasmForm",
    "SampledCarrierRow",
    "inspect_alif_carrier_rows",
    "inspect_carrier_rows",
    "inspect_the_deposited_fatiha_alif_carriers",
    "sample_other_carrier_rows",
]


class AlifCarrierInspectionError(ValueError):
    """سُئل الفحصُ عمّا لا يقوم به؛ ولا يُحمَل على أقرب حالةٍ مقبولة."""


# --- صورتا الألف، مُعلَنتان لأنّ البقيّةَ تُفرِّق بينهما ----------------------


WASL_ALIF: Final[str] = "\u0671"
"""ألفُ الوصل المرسومةُ صراحةً «ٱ»؛ رمزٌ غيرُ الألف المجرّدة لا صورةٌ منها."""


class RasmForm(Enum):
    """صورةُ الألف المقروءةُ في الصفّ؛ اثنتان مغلقتان لا ثالثةَ لهما هنا."""

    PLAIN_ALIF = ALIF
    WASL_ALIF = WASL_ALIF


_RASM_FORM_BY_CHARACTER: Final[dict[str, RasmForm]] = {
    form.value: form for form in RasmForm
}


ONE_ROW_PER_VERSE_LINE_IS_THE_SLICE_PRINCIPLE: Final[str] = (
    "ONE_ROW_PER_VERSE_LINE_IS_THE_SLICE_PRINCIPLE: شريحةُ الحوامل الأُخَر هي "
    "أوّلُ صفٍّ حاملُه غيرُ ألفٍ وفي حالته واحدةٌ من الثلاث، في كلّ سطر آيةٍ "
    "على حدة؛ مبدأٌ مكتوبٌ يُعيد الشريحةَ نفسَها في كلّ تشغيل، ويمرّ على كلّ "
    "سطرٍ فلا يسقط سطرٌ من الفحص"
)
"""مبدأُ اختيار الشريحة، مكتوبًا في الكود ومحفوظًا في السجلّ لا في تعليق."""


# --- سياقُ الصفّ الواحد: ما يقرأ به الإنسانُ الصفَّ لا ما يُلخِّصه ------------


@dataclass(frozen=True)
class AlifCarrierSample:
    """صفُّ ألفٍ واحدٌ وسياقُه: سطرُه، وموضعُه فيه، وجاراه، وصورةُ رسمه."""

    row: CarrierAtomRow
    line_index: int
    verse_line: str
    position_in_line: int
    preceding_carrier: CarrierAtomRow | None
    following_carrier: CarrierAtomRow | None
    rasm_form: RasmForm

    def __post_init__(self) -> None:
        _check_context(self)

    @property
    def carries_the_wasl_form(self) -> bool:
        """أوردت هذه الألفُ مرسومةً ألفَ وصلٍ صريحة؟"""
        return self.rasm_form is RasmForm.WASL_ALIF


@dataclass(frozen=True)
class SampledCarrierRow:
    """صفٌّ من شريحة الحوامل الأُخَر، بسياقه نفسِه وبحالته الثلاثية."""

    row: CarrierAtomRow
    line_index: int
    verse_line: str
    position_in_line: int
    preceding_carrier: CarrierAtomRow | None
    following_carrier: CarrierAtomRow | None
    short_vowels: tuple[str, ...]

    def __post_init__(self) -> None:
        _check_context(self)


def _check_context(sample: AlifCarrierSample | SampledCarrierRow) -> None:
    if sample.line_index < 0 or sample.position_in_line < 0:
        raise AlifCarrierInspectionError("موضعُ الصفّ لا يكون سالبًا.")
    if not sample.verse_line.strip():
        raise AlifCarrierInspectionError("صفٌّ بلا سطرٍ يُقرأ فيه ليس سياقًا.")
    if sample.row.line_index != sample.line_index:
        raise AlifCarrierInspectionError("سطرُ السياق غيرُ سطر الصفّ تناقضٌ فيه.")


# --- الفحصُ نفسُه: قراءةُ الجدول، لا إعادةُ عدِّه -----------------------------


def _lines_by_index(table: AlifStateRawCountTable) -> dict[int, str]:
    words: dict[int, dict[int, str]] = {}
    for row in table.rows:
        words.setdefault(row.line_index, {})[row.word_index] = row.word
    return {
        line_index: " ".join(word for _, word in sorted(line_words.items()))
        for line_index, line_words in words.items()
    }


def _rows_by_line(
    table: AlifStateRawCountTable,
) -> dict[int, tuple[CarrierAtomRow, ...]]:
    by_line: dict[int, list[CarrierAtomRow]] = {}
    for row in table.rows:
        by_line.setdefault(row.line_index, []).append(row)
    return {line_index: tuple(rows) for line_index, rows in by_line.items()}


def _read_rasm_form(row: CarrierAtomRow, ordinal_in_word: int) -> RasmForm:
    """اقرأ صورةَ الألف من حروف كلمتها في موضعها، لا من مُرشِّح العدّ.

    وموضعُ الحامل في كلمته معلومٌ من ترتيبه بين حوامل تلك الكلمة، فيُؤخَذ الحرفُ
    من الكلمة نفسِها ويُقارَن بحامل الصفّ؛ فإن اختلفا فالقراءةُ لم تقع على ما
    عُدّ، وتوقُّفُها خيرٌ من صورةٍ مُفترَضة.
    """
    carriers = [character for character in row.word if _is_carrier_character(character)]
    if ordinal_in_word >= len(carriers):  # pragma: no cover - حارس قراءة
        raise AlifCarrierInspectionError("موضعُ الحامل خارج حروف كلمته.")
    character = carriers[ordinal_in_word]
    if character != row.carrier:  # pragma: no cover - حارس قراءة
        raise AlifCarrierInspectionError("الحرفُ المقروءُ غيرُ حامل الصفّ المعدود.")
    form = _RASM_FORM_BY_CHARACTER.get(character)
    if form is None:
        raise AlifCarrierInspectionError("حاملٌ ليس صورةً من صورتَي الألف.")
    return form


def _is_carrier_character(character: str) -> bool:
    return unicodedata.category(character) == "Lo"


def _is_an_alif_carrier(row: CarrierAtomRow) -> bool:
    return row.carrier in _RASM_FORM_BY_CHARACTER


def _ordinal_in_word(rows: tuple[CarrierAtomRow, ...], position: int) -> int:
    """ترتيبُ الحامل بين حوامل كلمته، محسوبًا من صفوف سطره لا من مُعرِّف كائن."""
    word_index = rows[position].word_index
    return sum(1 for row in rows[:position] if row.word_index == word_index)


def _neighbours(
    rows: tuple[CarrierAtomRow, ...], position: int
) -> tuple[CarrierAtomRow | None, CarrierAtomRow | None]:
    preceding = rows[position - 1] if position > 0 else None
    following = rows[position + 1] if position + 1 < len(rows) else None
    return preceding, following


def inspect_alif_carrier_rows(
    table: AlifStateRawCountTable,
) -> tuple[AlifCarrierSample, ...]:
    """أخرِج لكلّ صفِّ ألفٍ في هذا الجدول سياقَه، بلا ترشيحٍ ولا تجميع.

    وكلُّ صفٍّ حاملُه صورةٌ من صورتَي الألف يُقرأ هنا — المجرّدةُ وألفُ الوصل
    سواء — لأنّ البقيّةَ المقروءةَ هي التفريقُ بينهما، فقصرُ الفحص على ما
    رشَّحه العدُّ يجعل الغيابَ نتيجةَ الترشيح لا قراءةً في النصّ.
    """
    if not isinstance(table, AlifStateRawCountTable):
        raise AlifCarrierInspectionError("المقروءُ `AlifStateRawCountTable`.")
    lines = _lines_by_index(table)
    rows_by_line = _rows_by_line(table)
    samples: list[AlifCarrierSample] = []
    for line_index, rows in sorted(rows_by_line.items()):
        for position, row in enumerate(rows):
            if not _is_an_alif_carrier(row):
                continue
            preceding, following = _neighbours(rows, position)
            samples.append(
                AlifCarrierSample(
                    row=row,
                    line_index=line_index,
                    verse_line=lines[line_index],
                    position_in_line=position,
                    preceding_carrier=preceding,
                    following_carrier=following,
                    rasm_form=_read_rasm_form(row, _ordinal_in_word(rows, position)),
                )
            )
    return tuple(samples)


def sample_other_carrier_rows(
    table: AlifStateRawCountTable,
) -> tuple[SampledCarrierRow, ...]:
    """اختر شريحةَ الحوامل الأُخَر على المبدأ المكتوب: صفٌّ لكلّ سطر آية.

    والمبدأُ هو `ONE_ROW_PER_VERSE_LINE_IS_THE_SLICE_PRINCIPLE`: أوّلُ صفٍّ في
    السطر حاملُه غيرُ ألفٍ وفي حالته واحدةٌ من الثلاث؛ وما لم يقع في سطرٍ صفٌّ
    كهذا فلا يُصطنَع له بديل، ويبقى السطرُ بلا صفٍّ في الشريحة.
    """
    if not isinstance(table, AlifStateRawCountTable):
        raise AlifCarrierInspectionError("المقروءُ `AlifStateRawCountTable`.")
    lines = _lines_by_index(table)
    rows_by_line = _rows_by_line(table)
    sampled: list[SampledCarrierRow] = []
    for line_index, rows in sorted(rows_by_line.items()):
        for position, row in enumerate(rows):
            if _is_an_alif_carrier(row) or not row.carries_short_vowel:
                continue
            preceding, following = _neighbours(rows, position)
            sampled.append(
                SampledCarrierRow(
                    row=row,
                    line_index=line_index,
                    verse_line=lines[line_index],
                    position_in_line=position,
                    preceding_carrier=preceding,
                    following_carrier=following,
                    short_vowels=row.short_vowels,
                )
            )
            break
    return tuple(sampled)


# --- سجلُّ الفحص: صفوفٌ ومبدأٌ وما قُيِّد من المُسمَّيات، بلا حكم -------------


@dataclass(frozen=True)
class AlifCarrierInspection:
    """فحصٌ واحد: صفوفُ الألف كلُّها، وشريحةٌ من غيرها، ومبدأُ اختيارها.

    ولا حقلَ حكمٍ هنا كما لا حقلَ حكمٍ في `AlifStateRawCountTable`: لا «مُثبَت»
    ولا «مردود»؛ والمُقيَّدُ من المُسمَّيات يُشتَقّ من الصفوف عند البناء، فلا
    يبقى مُسمًّى مكتوبًا في الشجرة بعد زوال ما قُرئ منه.
    """

    source_id: str
    alif_samples: tuple[AlifCarrierSample, ...]
    sampled_other_rows: tuple[SampledCarrierRow, ...]
    slice_principle: str
    filed_findings: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.source_id.strip():
            raise AlifCarrierInspectionError("فحصٌ بلا اسمِ مصدرٍ لا يُراجَع.")
        if not self.slice_principle.strip():
            raise AlifCarrierInspectionError("شريحةٌ بلا مبدأٍ مكتوبٍ لا تُراجَع.")
        for name in self.filed_findings:
            if name not in ALIF_CARRIER_INSPECTION_NAMED_RESIDUALS:
                raise AlifCarrierInspectionError(
                    f"مُسمًّى لا نصَّ له في هذه الوحدة: {name}."
                )

    @property
    def samples_carrying_the_wasl_form(self) -> tuple[AlifCarrierSample, ...]:
        """صفوفُ ألف الوصل الصريحة إن وردت؛ وخلوُّها قراءةٌ في هذا المُودَع."""
        return tuple(
            sample for sample in self.alif_samples if sample.carries_the_wasl_form
        )

    @property
    def lines_inspected(self) -> tuple[int, ...]:
        """أرقامُ السطور التي وقع فيها صفُّ ألفٍ مقروء، بترتيبها."""
        return tuple(dict.fromkeys(sample.line_index for sample in self.alif_samples))

    def finding_text(self, name: str) -> str:
        """نصُّ مُسمًّى مُقيَّدٍ في هذا الفحص؛ وما لم يُقيَّد لا يُقرأ منه."""
        if name not in self.filed_findings:
            raise AlifCarrierInspectionError(f"مُسمًّى غيرُ مُقيَّدٍ في هذا الفحص: {name}.")
        return ALIF_CARRIER_INSPECTION_NAMED_RESIDUALS[name]


def _file_findings(alif_samples: tuple[AlifCarrierSample, ...]) -> tuple[str, ...]:
    filed = [
        "FULL_SET_NOT_A_SAMPLE",
        "THE_SLICE_IS_CHOSEN_NOT_REPRESENTATIVE",
        "THE_VERSE_LINE_IS_REBUILT_FROM_THE_COUNTED_WORDS",
        "INSPECTION_WRITES_NO_CONDITION",
        "RASM_RESIDUAL_STAYS_OPEN",
    ]
    if not any(sample.carries_the_wasl_form for sample in alif_samples):
        filed.append("WASLA_FORM_ABSENT_FROM_THIS_DEPOSIT")
    return tuple(filed)


def inspect_carrier_rows(table: AlifStateRawCountTable) -> AlifCarrierInspection:
    """افحص جدولَ عدٍّ خامٍّ أيًّا كان مصدرُه، وأخرِج سجلَّ فحصه."""
    alif_samples = inspect_alif_carrier_rows(table)
    return AlifCarrierInspection(
        source_id=table.source_id,
        alif_samples=alif_samples,
        sampled_other_rows=sample_other_carrier_rows(table),
        slice_principle=ONE_ROW_PER_VERSE_LINE_IS_THE_SLICE_PRINCIPLE,
        filed_findings=_file_findings(alif_samples),
    )


# --- المدخلُ عديمُ الوسائط: يقرأ الخطوةَ الأولى ولا يُعيد عدَّها -------------


def inspect_the_deposited_fatiha_alif_carriers() -> AlifCarrierInspection:
    """شغِّل عدَّ الخطوة الأولى على النصّ المُودَع، ثمّ اقرأ صفوفَه.

    وهو مُعيدُ إنتاج الخطوة الثانية كما يستدعيه `run_step`: بلا وسائط، ويُخرِج
    سجلَّ الفحص نفسَه لا وصفَه. والعدُّ يُستدعى كما هو ولا يُعاد بناؤه هنا،
    فمصدرُ الصفوف واحدٌ لا اثنان.
    """
    return inspect_carrier_rows(run_raw_count_on_the_deposited_fatiha())


# --- ما لا يحسمه هذا الفحص، مُسمًّى -------------------------------------------


FULL_SET_NOT_A_SAMPLE: Final[str] = (
    "FULL_SET_NOT_A_SAMPLE: صفوفُ الألف تُقرأ كلُّها لا عيّنةً منها، فلم يقع "
    "اختيارٌ فيها ولا يُقرأ خلوُّها من المخالف نتيجةَ انتقاء؛ و«العيّنة» في "
    "اسم الخطوة تصدق على شريحة الحوامل الأُخَر وحدَها"
)

WASLA_FORM_ABSENT_FROM_THIS_DEPOSIT: Final[str] = (
    "WASLA_FORM_ABSENT_FROM_THIS_DEPOSIT: لم يقع في المُودَع المقروء حاملٌ "
    "واحدٌ صورتُه ألفُ وصلٍ صريحة «ٱ»؛ فالقياسُ على الألف لم يلقَ الصورةَ "
    "التي تُحذِّر منها `RASM_IS_IMLAI_NOT_UTHMANI` أصلًا، وهو أضيقُ ممّا "
    "يبدو، وضيقُه مُقيَّدٌ صفًّا لا متروكٌ في رقمٍ صفر"
)

THE_SLICE_IS_CHOSEN_NOT_REPRESENTATIVE: Final[str] = (
    "THE_SLICE_IS_CHOSEN_NOT_REPRESENTATIVE: شريحةُ الحوامل الأُخَر مُختارةٌ "
    "بمبدأٍ مكتوبٍ لا مسحوبةٌ سحبًا إحصائيًّا من المئة والعشرين؛ فما صحّ فيها "
    "لا يُعمَّم على بقيّة الصفوف، وتعميمُه يجعل المبدأَ عيّنةً وهو ليس بها"
)

INSPECTION_WRITES_NO_CONDITION: Final[str] = (
    "INSPECTION_WRITES_NO_CONDITION: قراءةُ الصفوف ليست كتابةَ شرط استبعاد؛ "
    "وشرطٌ واحدٌ في كلّ مرّة خطوةٌ ثالثةٌ لم تُملأ هنا، ولو بدا الشرطُ ظاهرًا "
    "من الصفوف فظهورُه لا يجعله مكتوبًا"
)

RASM_RESIDUAL_STAYS_OPEN: Final[str] = (
    "RASM_RESIDUAL_STAYS_OPEN: هذا الفحصُ يصف ما ظهر لـ"
    "`RASM_IS_IMLAI_NOT_UTHMANI` على مُودَعٍ واحد، ولا يُغلِقها؛ فالبقيّةُ "
    "مفتوحةٌ كما كانت، وإنّما صارت أدقَّ وصفًا"
)

THE_VERSE_LINE_IS_REBUILT_FROM_THE_COUNTED_WORDS: Final[str] = (
    "THE_VERSE_LINE_IS_REBUILT_FROM_THE_COUNTED_WORDS: سطرُ الآية في الصفّ "
    "مُعادُ البناء من كلمات الصفوف المعدودة في ذلك السطر مفصولةً بفراغٍ واحد، "
    "لا مقروءٌ من مُودَعٍ تستورده هذه الوحدة؛ فما سقط من الجدول قبل هذا الفحص "
    "لا يعود في السطر المُعاد"
)

ALIF_CARRIER_INSPECTION_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "FULL_SET_NOT_A_SAMPLE": FULL_SET_NOT_A_SAMPLE,
    "WASLA_FORM_ABSENT_FROM_THIS_DEPOSIT": WASLA_FORM_ABSENT_FROM_THIS_DEPOSIT,
    "THE_SLICE_IS_CHOSEN_NOT_REPRESENTATIVE": THE_SLICE_IS_CHOSEN_NOT_REPRESENTATIVE,
    "INSPECTION_WRITES_NO_CONDITION": INSPECTION_WRITES_NO_CONDITION,
    "RASM_RESIDUAL_STAYS_OPEN": RASM_RESIDUAL_STAYS_OPEN,
    "THE_VERSE_LINE_IS_REBUILT_FROM_THE_COUNTED_WORDS": (
        THE_VERSE_LINE_IS_REBUILT_FROM_THE_COUNTED_WORDS
    ),
}
"""ما لا يحسمه هذا الفحص، مُسمًّى هنا لا متروكًا ليُفترَض."""
