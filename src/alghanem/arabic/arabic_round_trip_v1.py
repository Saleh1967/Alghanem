"""`ArabicRoundTripV1`: من البايتات إلى البنية ثمّ رجوعًا، وجدولُ فقدٍ لكلّ طبقة.

في هذه الشجرة طرفان مقيسان لا يلتقيان: بايتاتٌ ↔ بايتاتٌ في نموذج الضغط، ونصٌّ
↔ حامل/حالة في `CarrierStateCodec`. وهذه الوحدةُ **توصلهما في خطٍّ واحدٍ
يُنفَّذ**، لا تُشرّع لهما. ومخرجُها جدولٌ عمليٌّ بستّة صفوف، لا شهادةٌ ولا دستور.

```
raw bytes → UTF-8 → NFC → carrier/state → syllable → word structure
          → reverse word structure → desegment → retrieve → raw bytes
```

`A_LAYER_ENTERS_ONLY_IF_IT_CAN_BE_REVERSED_OR_MEASURE_ITS_LOSS`: كلُّ طبقةٍ
هنا تأخذ مخرجَ ما تحتها بعينه، وتُخرِج شيئًا قابلًا للفحص، وتُعلن دالّتَها
الأماميّةَ والعكسيّة بالاسم. والطبقةُ التي لا تفعل ذلك لا تدخل الجدولَ لأنّها
مطلوبةٌ نظريًّا: النحوُ والصرفُ والدلالةُ **ليست في هذا الخطّ**، وغيابُها يُقرأ
في `LAYERS_NOT_IN_THIS_PIPELINE` لا في صفٍّ فارغ.

`NO_LAYER_REPAIRS_THE_DAMAGE_BENEATH_IT`: الكلمةُ التي رُفِضت أو اختلفت عند
طبقةٍ تقف عندها ولا تصعد؛ فمقامُ كلِّ طبقةٍ ما بلغها فعلًا، لا كلُّ ما دخل
الخطّ. ولذلك تتناقص الأعدادُ صعودًا، وهو إفصاحٌ لا نقص.

`REFUSAL_IS_NOT_A_ROUND_TRIP`: المرفوضُ خارجُ المقام، والمختلفُ داخلَه؛ فلا
تُرفَع نسبةُ استرجاعٍ بإخراج ما عجزت عنه من القسمة. وهذا عينُ ما جرى عليه
`InvertibilityMeasurement` في المرماز.

`A_REORDERING_IS_A_MISMATCH_WITH_NOTHING_LOST`: الفقدُ والزيادةُ يُعَدّان
بفرقِ كثرةِ الذرّات، فتسويةُ `NFC` التي تُعيد ترتيبَ علاماتٍ دون أن تُسقِط
واحدةً تخرج اختلافًا بفقدٍ صفر. وهذا خبرٌ دقيقٌ لا تناقض: البايتاتُ تغيّرت
والذرّاتُ لم تنقص.

ويُقرأ هذا في عمودِ `Reorder`: المرمازُ يكتب الشدّةَ قبل الحركة، فتخرج بايتاتُه
من `FINAL_BYTES` مخالفةً لترتيب `NFC` الداخل وإن لم تنقص ذرّةٌ واحدة. ولا
تُسوَّى هذه المخالفةُ في أعلى الخطّ تسويةً ثانية، لأنّ طبقةً تُصلِح ما تحتها
تُخفيه.

`THE_TABLE_IS_DERIVED_NOT_WRITTEN`: لا رقمَ في هذه الوحدةِ مكتوبٌ بيدٍ؛ كلُّ
عددٍ يخرج من تشغيل الطبقات على بايتاتٍ مُعطاة، وكلُّ نسبةٍ مشتقّةٌ من عدّادين.
"""

from __future__ import annotations

import unicodedata
from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum
from typing import Final

from .encoding.carrier_state_candidate import (
    CarrierStateCodec,
    CarrierStateEncodingError,
    CarrierStateUnit,
)
from .encoding.syllable_segmentation import (
    SyllableSegmentationError,
    desegment,
    segment,
)
from .word_structure_dictionary import (
    WordStructureDictionaryError,
    analyze_word,
    reverse_word_structure,
)

__all__ = [
    "A_LAYER_ENTERS_ONLY_IF_IT_CAN_BE_REVERSED_OR_MEASURE_ITS_LOSS_NOTE",
    "LAYERS_NOT_IN_THIS_PIPELINE",
    "LAYER_FUNCTIONS",
    "NO_LAYER_REPAIRS_THE_DAMAGE_BENEATH_IT_NOTE",
    "THE_TABLE_IS_DERIVED_NOT_WRITTEN_NOTE",
    "LayerAtom",
    "LayerFunctions",
    "LayerOutcome",
    "LayerRow",
    "RoundTripLayer",
    "RoundTripRefusal",
    "RoundTripTable",
    "RoundTripV1Error",
    "TokenTrace",
    "declared_layer_functions",
    "measure_round_trip",
    "render_table",
    "run_token",
    "tokens_from_text",
]


class RoundTripV1Error(ValueError):
    """رفضٌ بنيويٌّ في بناء الجدول نفسِه، لا في الكلمة المقيسة."""


class RoundTripLayer(Enum):
    """طبقاتُ الخطّ الستّ بترتيب التنفيذ؛ مفردةٌ مغلقةٌ لا سابعةَ لها هنا."""

    UTF8_BYTES = "UTF8_BYTES"
    UNICODE_NFC = "UNICODE_NFC"
    CARRIER_STATE = "CARRIER_STATE"
    SYLLABLE = "SYLLABLE"
    WORD_STRUCTURE = "WORD_STRUCTURE"
    FINAL_BYTES = "FINAL_BYTES"


class LayerAtom(Enum):
    """ذرّةُ القياس في كلّ طبقة؛ فالفقدُ يُعَدّ بذرّةِ طبقته لا بذرّةٍ واحدة."""

    BYTE = "BYTE"
    CODEPOINT = "CODEPOINT"
    UNIT = "UNIT"


class LayerOutcome(Enum):
    """ما جرى لكلمةٍ عند طبقةٍ بعينها. ثلاثةٌ لا رابعَ لها، ولا `مقبولٌ تقريبًا`."""

    RECONSTRUCTED = "RECONSTRUCTED"
    REFUSED = "REFUSED"
    MISMATCHED = "MISMATCHED"


class RoundTripRefusal(Enum):
    """أسبابُ الرفض؛ مفردةٌ مغلقةٌ تُقرأ في الجدول ولا تُختصر إلى «فشل»."""

    NOT_VALID_UTF8 = "NOT_VALID_UTF8"
    EMPTY_TOKEN = "EMPTY_TOKEN"
    CODEC_REFUSED_THE_SURFACE = "CODEC_REFUSED_THE_SURFACE"
    SEGMENTATION_REFUSED_THE_UNITS = "SEGMENTATION_REFUSED_THE_UNITS"
    DICTIONARY_REFUSED_THE_SURFACE = "DICTIONARY_REFUSED_THE_SURFACE"


@dataclass(frozen=True, slots=True)
class LayerFunctions:
    """اسمُ الدالّة الأماميّة واسمُ العكسيّة لطبقةٍ واحدة، وذرّةُ قياسها."""

    layer: RoundTripLayer
    forward: str
    inverse: str
    atom: LayerAtom

    def __post_init__(self) -> None:
        if not isinstance(self.layer, RoundTripLayer):
            raise RoundTripV1Error("الطبقةُ عضوٌ في مفردتها المغلقة")
        if not isinstance(self.atom, LayerAtom):
            raise RoundTripV1Error("ذرّةُ القياس عضوٌ في مفردتها المغلقة")
        for name in ("forward", "inverse"):
            if not str(getattr(self, name)).strip():
                raise RoundTripV1Error(
                    "طبقةٌ بلا دالّةٍ أماميّةٍ أو بلا عكسيّةٍ مُسمّاةٍ لا تدخل هذا "
                    "الخطّ؛ والوصفُ ليس دالّة"
                )


LAYER_FUNCTIONS: Final[tuple[LayerFunctions, ...]] = (
    LayerFunctions(
        layer=RoundTripLayer.UTF8_BYTES,
        forward="bytes.decode('utf-8')",
        inverse="str.encode('utf-8')",
        atom=LayerAtom.BYTE,
    ),
    LayerFunctions(
        layer=RoundTripLayer.UNICODE_NFC,
        forward="unicodedata.normalize('NFC', text)",
        inverse="identity",
        atom=LayerAtom.CODEPOINT,
    ),
    LayerFunctions(
        layer=RoundTripLayer.CARRIER_STATE,
        forward="CarrierStateCodec.generate",
        inverse="CarrierStateCodec.retrieve",
        atom=LayerAtom.CODEPOINT,
    ),
    LayerFunctions(
        layer=RoundTripLayer.SYLLABLE,
        forward="syllable_segmentation.segment",
        inverse="syllable_segmentation.desegment",
        atom=LayerAtom.UNIT,
    ),
    LayerFunctions(
        layer=RoundTripLayer.WORD_STRUCTURE,
        forward="word_structure_dictionary.analyze_word",
        inverse="word_structure_dictionary.reverse_word_structure",
        atom=LayerAtom.UNIT,
    ),
    LayerFunctions(
        layer=RoundTripLayer.FINAL_BYTES,
        forward="CarrierStateCodec.retrieve → str.encode('utf-8')",
        inverse="comparison against the entering bytes",
        atom=LayerAtom.BYTE,
    ),
)
"""كلُّ طبقةٍ تُعلن أمامَها وخلفَها؛ واختبارٌ يُلزِم الجدولَ بهذه المفردة."""


LAYERS_NOT_IN_THIS_PIPELINE: Final[tuple[str, ...]] = (
    "المخرج والصفة: حاجزُ الاستيراد مفتوحٌ في `gflk_feature_table_import_barrier`",
    "أل تعريفًا أو وصلًا: متعذّرٌ من العلامات المكتوبة",
    "مجرّد أو مزيد: فرضٌ مُعلَنُ العطب في القاموس البنيويّ",
    "الوزن: تقطيعُ هذا الخطّ مدًى على وحداتٍ لا وزنًا مشتقًّا",
    "الصرفُ والنحوُ والإعرابُ والدلالة: لا دالّةَ أماميّةً ولا عكسيّةً لها هنا",
)
"""ما ليس في الخطّ، مُسمًّى بسببه؛ فالغيابُ يُقرأ ولا يُخمَّن من صفٍّ فارغ."""


_CODEC: Final[CarrierStateCodec] = CarrierStateCodec()


@dataclass(frozen=True, slots=True)
class TokenTrace:
    """أثرُ كلمةٍ واحدةٍ في الخطّ: أين وقفت، وبأيّ حكمٍ، وبأيّ فقدٍ مقيس."""

    token_index: int
    reached: RoundTripLayer
    outcome: LayerOutcome
    refusal: RoundTripRefusal | None = None
    lost: int = 0
    added: int = 0

    def __post_init__(self) -> None:
        if not isinstance(self.outcome, LayerOutcome):
            raise RoundTripV1Error("حكمُ الطبقة عضوٌ في مفردته المغلقة")
        if (self.outcome is LayerOutcome.REFUSED) != (self.refusal is not None):
            raise RoundTripV1Error(
                "الرفضُ يحمل سببَه المُسنون، وغيرُ المرفوض لا يحمل سببَ رفض"
            )
        if self.lost < 0 or self.added < 0:
            raise RoundTripV1Error("الفقدُ والزيادةُ عددان غيرُ سالبين")
        if self.outcome is not LayerOutcome.MISMATCHED and (self.lost or self.added):
            raise RoundTripV1Error(
                "لا يُسجَّل فقدٌ ولا زيادةٌ لكلمةٍ رجعت كما دخلت أو رُفِضت قبل أن " "تُقرأ"
            )

    @property
    def is_ordering_only(self) -> bool:
        """اختلافٌ بلا ذرّةٍ ناقصةٍ ولا زائدة: ترتيبُ علاماتٍ تغيّر لا معنًى سقط."""

        return (
            self.outcome is LayerOutcome.MISMATCHED
            and self.lost == 0
            and self.added == 0
        )


@dataclass(frozen=True, slots=True)
class LayerRow:
    """صفُّ طبقةٍ واحدةٍ في الجدول: عدّاداتٌ مُشتقّةٌ من تشغيلٍ لا أرقامٌ مكتوبة."""

    layer: RoundTripLayer
    atom: LayerAtom
    input_count: int
    refused_count: int
    mismatch_count: int
    information_lost: int
    information_added: int
    ordering_only_count: int = 0

    def __post_init__(self) -> None:
        for name in (
            "input_count",
            "refused_count",
            "mismatch_count",
            "information_lost",
            "information_added",
            "ordering_only_count",
        ):
            value = getattr(self, name)
            if not isinstance(value, int) or value < 0:
                raise RoundTripV1Error(f"{name} عددٌ صحيحٌ غيرُ سالب")
        if self.refused_count + self.mismatch_count > self.input_count:
            raise RoundTripV1Error(
                "مرفوضٌ ومختلفٌ أكثرُ ممّا دخل الطبقةَ دعوَيان متناقضتان في صفٍّ " "واحد"
            )
        unaccounted = self.information_lost or self.information_added
        if self.mismatch_count == 0 and unaccounted:
            raise RoundTripV1Error("فقدٌ أو زيادةٌ بلا اختلافٍ واحدٍ رقمٌ بلا واقعةٍ تحته")
        if self.ordering_only_count > self.mismatch_count:
            raise RoundTripV1Error(
                "اختلافُ ترتيبٍ أكثرُ من الاختلاف كلِّه دعوَيان متناقضتان في صفٍّ " "واحد"
            )

    @property
    def accepted_count(self) -> int:
        """ما قرأته الطبقةُ فعلًا؛ والمرفوضُ ليس منه."""

        return self.input_count - self.refused_count

    @property
    def reconstructed_count(self) -> int:
        """المقبولُ الذي رجع كما دخل، مشتقًّا من العدّادين."""

        return self.accepted_count - self.mismatch_count

    @property
    def reconstruction_rate(self) -> float | None:
        """نسبةُ الاسترجاع على المقبول وحدَه، و`None` على مقامٍ خالٍ.

        `REFUSAL_IS_NOT_A_ROUND_TRIP`: المرفوضُ خارجَ القسمة لا في بسطها ولا
        في مقامها؛ ومقامٌ خالٍ لا تُكتَب له نسبةٌ ولا يُقرأ صفرًا.
        """

        if self.accepted_count == 0:
            return None
        return self.reconstructed_count / self.accepted_count


@dataclass(frozen=True, slots=True)
class RoundTripTable:
    """جدولُ `ArabicRoundTripV1`: ستّةُ صفوفٍ وآثارُ ما لم يصعد، لا شهادة."""

    rows: tuple[LayerRow, ...]
    traces: tuple[TokenTrace, ...]
    token_total: int

    def __post_init__(self) -> None:
        layers = tuple(row.layer for row in self.rows)
        if layers != tuple(RoundTripLayer):
            raise RoundTripV1Error(
                "الجدولُ ستّةُ صفوفٍ بترتيب الطبقات؛ وحذفُ صفٍّ يُخفي طبقةً " "وُضِعت في الخطّ"
            )
        if self.token_total < 0:
            raise RoundTripV1Error("عددُ الكلمات عددٌ غيرُ سالب")
        if self.rows[0].input_count != self.token_total:
            raise RoundTripV1Error(
                "أوّلُ طبقةٍ تستقبل كلَّ ما دخل الخطّ؛ ومقامٌ أصغرُ يُسقِط كلماتٍ " "قبل أن تُقاس"
            )

    def row(self, layer: RoundTripLayer) -> LayerRow:
        """صفُّ طبقةٍ بعينها، مقروءًا من الجدول لا مُنشأً عند النداء."""

        for candidate in self.rows:
            if candidate.layer is layer:
                return candidate
        raise RoundTripV1Error(f"لا صفَّ للطبقة {layer!r}")

    @property
    def end_to_end_reconstructed(self) -> int:
        """الكلماتُ التي خرجت بايتاتُها كما دخلت، من أعلى الخطّ لا من أدناه."""

        return self.row(RoundTripLayer.FINAL_BYTES).reconstructed_count


@dataclass
class _LayerLedger:
    """عدّاداتُ طبقةٍ أثناء التشغيل؛ تُجمَّد صفًّا عند الفراغ."""

    layer: RoundTripLayer
    atom: LayerAtom
    input_count: int = 0
    refused_count: int = 0
    mismatch_count: int = 0
    information_lost: int = 0
    information_added: int = 0
    ordering_only_count: int = 0

    def freeze(self) -> LayerRow:
        return LayerRow(
            layer=self.layer,
            atom=self.atom,
            input_count=self.input_count,
            refused_count=self.refused_count,
            mismatch_count=self.mismatch_count,
            information_lost=self.information_lost,
            information_added=self.information_added,
            ordering_only_count=self.ordering_only_count,
        )


def _atom_delta(before: Iterable[object], after: Iterable[object]) -> tuple[int, int]:
    """كم ذرّةً سقطت وكم زادت، بفرقِ كثرتين لا بطولٍ واحد."""

    entering = Counter(before)
    leaving = Counter(after)
    lost = sum((entering - leaving).values())
    added = sum((leaving - entering).values())
    return lost, added


def run_token(token: bytes, *, token_index: int = 0) -> TokenTrace:
    """شغِّل الخطَّ كلَّه على بايتاتِ كلمةٍ واحدةٍ وسجِّل أين وقفت وبأيّ حكم."""

    if not isinstance(token, bytes):
        raise RoundTripV1Error("مدخلُ الخطّ بايتاتٌ خام، لا نصٌّ مقروءٌ سلفًا")

    if not token:
        return TokenTrace(
            token_index=token_index,
            reached=RoundTripLayer.UTF8_BYTES,
            outcome=LayerOutcome.REFUSED,
            refusal=RoundTripRefusal.EMPTY_TOKEN,
        )

    try:
        text = token.decode("utf-8")
    except UnicodeDecodeError:
        return TokenTrace(
            token_index=token_index,
            reached=RoundTripLayer.UTF8_BYTES,
            outcome=LayerOutcome.REFUSED,
            refusal=RoundTripRefusal.NOT_VALID_UTF8,
        )
    if text.encode("utf-8") != token:
        lost, added = _atom_delta(token, text.encode("utf-8"))
        return TokenTrace(
            token_index=token_index,
            reached=RoundTripLayer.UTF8_BYTES,
            outcome=LayerOutcome.MISMATCHED,
            lost=lost,
            added=added,
        )

    normalized = unicodedata.normalize("NFC", text)
    if normalized != text:
        lost, added = _atom_delta(text, normalized)
        return TokenTrace(
            token_index=token_index,
            reached=RoundTripLayer.UNICODE_NFC,
            outcome=LayerOutcome.MISMATCHED,
            lost=lost,
            added=added,
        )

    try:
        units = _CODEC.generate(normalized)
        retrieved = _CODEC.retrieve(units)
    except CarrierStateEncodingError:
        return TokenTrace(
            token_index=token_index,
            reached=RoundTripLayer.CARRIER_STATE,
            outcome=LayerOutcome.REFUSED,
            refusal=RoundTripRefusal.CODEC_REFUSED_THE_SURFACE,
        )
    if unicodedata.normalize("NFC", retrieved) != normalized:
        lost, added = _atom_delta(normalized, unicodedata.normalize("NFC", retrieved))
        return TokenTrace(
            token_index=token_index,
            reached=RoundTripLayer.CARRIER_STATE,
            outcome=LayerOutcome.MISMATCHED,
            lost=lost,
            added=added,
        )

    try:
        parse = segment(units)
        desegmented = desegment(parse.syllables)
    except SyllableSegmentationError:
        return TokenTrace(
            token_index=token_index,
            reached=RoundTripLayer.SYLLABLE,
            outcome=LayerOutcome.REFUSED,
            refusal=RoundTripRefusal.SEGMENTATION_REFUSED_THE_UNITS,
        )
    if desegmented != units:
        lost, added = _atom_delta(units, desegmented)
        return TokenTrace(
            token_index=token_index,
            reached=RoundTripLayer.SYLLABLE,
            outcome=LayerOutcome.MISMATCHED,
            lost=lost,
            added=added,
        )

    try:
        dictionary = analyze_word(_CODEC.retrieve(desegmented))
        rebuilt: tuple[CarrierStateUnit, ...] = reverse_word_structure(dictionary)
    except (WordStructureDictionaryError, CarrierStateEncodingError):
        return TokenTrace(
            token_index=token_index,
            reached=RoundTripLayer.WORD_STRUCTURE,
            outcome=LayerOutcome.REFUSED,
            refusal=RoundTripRefusal.DICTIONARY_REFUSED_THE_SURFACE,
        )
    if rebuilt != desegmented:
        lost, added = _atom_delta(desegmented, rebuilt)
        return TokenTrace(
            token_index=token_index,
            reached=RoundTripLayer.WORD_STRUCTURE,
            outcome=LayerOutcome.MISMATCHED,
            lost=lost,
            added=added,
        )

    final_bytes = _CODEC.retrieve(rebuilt).encode("utf-8")
    if final_bytes != token:
        lost, added = _atom_delta(token, final_bytes)
        return TokenTrace(
            token_index=token_index,
            reached=RoundTripLayer.FINAL_BYTES,
            outcome=LayerOutcome.MISMATCHED,
            lost=lost,
            added=added,
        )
    return TokenTrace(
        token_index=token_index,
        reached=RoundTripLayer.FINAL_BYTES,
        outcome=LayerOutcome.RECONSTRUCTED,
    )


def measure_round_trip(tokens: Iterable[bytes]) -> RoundTripTable:
    """شغِّل الخطَّ على بايتاتِ كلماتٍ واردة، وأخرِج جدولَها المشتقَّ بستّة صفوف.

    `NO_LAYER_REPAIRS_THE_DAMAGE_BENEATH_IT`: ما وقف عند طبقةٍ لا يُعَدّ داخلًا
    فيما فوقها؛ فمقامُ كلِّ صفٍّ ما بلغه، وتناقصُ المقامات صعودًا هو الخبر.
    """

    ledgers: dict[RoundTripLayer, _LayerLedger] = {
        functions.layer: _LayerLedger(layer=functions.layer, atom=functions.atom)
        for functions in LAYER_FUNCTIONS
    }
    ordered: tuple[RoundTripLayer, ...] = tuple(RoundTripLayer)
    traces: list[TokenTrace] = []
    total = 0

    for index, token in enumerate(tokens):
        trace = run_token(token, token_index=index)
        traces.append(trace)
        total += 1
        stop = ordered.index(trace.reached)
        for layer in ordered[: stop + 1]:
            ledgers[layer].input_count += 1
        ledger = ledgers[trace.reached]
        if trace.outcome is LayerOutcome.REFUSED:
            ledger.refused_count += 1
        elif trace.outcome is LayerOutcome.MISMATCHED:
            ledger.mismatch_count += 1
            ledger.information_lost += trace.lost
            ledger.information_added += trace.added
            if trace.is_ordering_only:
                ledger.ordering_only_count += 1

    rows = tuple(ledgers[layer].freeze() for layer in ordered)
    return RoundTripTable(rows=rows, traces=tuple(traces), token_total=total)


def tokens_from_text(text: str) -> tuple[bytes, ...]:
    """قسِّم نصًّا على البياض وأخرِج بايتاتِ كلماته؛ التقسيمُ مُعلَنٌ لا مُخفًى."""

    if not isinstance(text, str):
        raise RoundTripV1Error("التقسيمُ يجري على نصٍّ مقروء")
    return tuple(word.encode("utf-8") for word in text.split())


def render_table(table: RoundTripTable) -> str:
    """اطبع الجدولَ صفوفًا نصّيّة؛ العرضُ قراءةٌ للأعداد لا مصدرٌ لها."""

    header = (
        f"{'Layer':<16}{'In':>8}{'Accepted':>10}{'Refused':>9}"
        f"{'Mismatch':>10}{'Reorder':>9}{'Lost':>8}{'Added':>8}{'RoundTrip':>12}"
    )
    lines = [header, "-" * len(header)]
    for row in table.rows:
        rate = row.reconstruction_rate
        rendered = "—" if rate is None else f"{rate * 100:.4f}%"
        lines.append(
            f"{row.layer.value:<16}{row.input_count:>8}{row.accepted_count:>10}"
            f"{row.refused_count:>9}{row.mismatch_count:>10}"
            f"{row.ordering_only_count:>9}"
            f"{row.information_lost:>8}{row.information_added:>8}{rendered:>12}"
        )
    return "\n".join(lines)


def declared_layer_functions(layer: RoundTripLayer) -> LayerFunctions:
    """دالّتا طبقةٍ بعينها، مقروءتان من المفردة المُجمَّدة لا مكتوبتين عند النداء."""

    for functions in LAYER_FUNCTIONS:
        if functions.layer is layer:
            return functions
    raise RoundTripV1Error(f"لا دالّتين مُعلَنتين للطبقة {layer!r}")


A_LAYER_ENTERS_ONLY_IF_IT_CAN_BE_REVERSED_OR_MEASURE_ITS_LOSS_NOTE: Final[str] = (
    "ALayerEntersOnlyIfItCanBeReversedOrMeasureItsLoss: لا تدخل طبقةٌ هذا الخطَّ "
    "لأنّها مطلوبةٌ نظريًّا؛ تدخل إن أخذت مخرجَ ما تحتها، وأعلنت دالّتَها "
    "الأماميّةَ والعكسيّة بالاسم، وسمحت بإعادة البناء أو سجّلت بالضبط ما فقدته"
)

NO_LAYER_REPAIRS_THE_DAMAGE_BENEATH_IT_NOTE: Final[str] = (
    "NoLayerRepairsTheDamageBeneathIt: الكلمةُ التي رُفِضت أو اختلفت عند طبقةٍ "
    "تقف عندها ولا تُحسَب فيما فوقها؛ فتناقصُ المقامات صعودًا خبرٌ لا عطب"
)

THE_TABLE_IS_DERIVED_NOT_WRITTEN_NOTE: Final[str] = (
    "TheTableIsDerivedNotWritten: لا رقمَ هنا مكتوبٌ بيدٍ؛ كلُّ عددٍ من تشغيلِ "
    "الطبقات على بايتاتٍ مُعطاة، وكلُّ نسبةٍ مشتقّةٌ من عدّادين"
)
