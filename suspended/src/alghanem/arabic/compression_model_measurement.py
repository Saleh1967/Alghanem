"""قياسُ الضغط: هفمان قانونيّ رتبةَ صفرٍ ورتبةً أولى على البايتات المُجمَّدة.

هذه وحدةُ **القياس** وحدها. البايتاتُ وتمثيلُ الجدول وقاعدتا التعادل مُجمَّدةٌ
قبلها في `compression_model_preregistration`، وتُتحقَّق بصمةُ المُجمَّد عند
الاستيراد؛ فقياسٌ يختار مدخلَه أثناءه ليس قياسًا.

`MeasurementReadsFrozenBytes`: لا تقبل الدالّاتُ هنا نصًّا مُعادَ بناؤه ولا
قائمةَ وحدات، بل بايتاتٍ يُتحقَّق من طولها وبصمتها ثمّ تُفَكّ هنا مرّةً واحدة.

`RoundTripIsAPreconditionOfIssuance`: كلُّ دالّةِ قياسٍ تُرمِّز ثمّ تفكّ ثمّ
تقارن بالأصل بايتًا-ببايت، وترفع `CompressionMeasurementError` إن اختلف شيء.
فلا يوجد في هذا الملفّ طريقٌ يُخرج نسبةَ ضغطٍ بلا مطابقةٍ محقَّقة.

`TwoSizesOrNone`: `ModelMeasurement` يحمل الحمولةَ والجدولَ معًا، ولا تُعرَض
نسبةُ الحمولة إلا ومعها النسبةُ الكليّة في المُخرَج نفسه.

`TheTableIsRelativeToItsTieBreak`: حجمُ الجدول يختلف باختلاف قاعدة التعادل
— الحمولةُ لا تختلف — فكلُّ قياسٍ يحمل اسمَ قاعدته، ولا يُقارَن جدولان
بقاعدتين مختلفتين كأنّهما رقمٌ واحد.

`ThisIsRegistrationNotAuthority`: لا ولادةَ هنا ولا حكمَ ولادةٍ ولا بوّابة.
"""

from __future__ import annotations

import hashlib
import heapq
from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Final

from .compression_model_preregistration import (
    FIRST_SYMBOL_CONTEXT,
    FROZEN_CORPUS,
    PREREGISTRATION_DIGEST,
    TABLE_ENTRY_CODEPOINT_BITS,
    TABLE_ENTRY_LENGTH_FIELD_BITS,
    TieBreakRule,
    preregistration_digest,
)

__all__ = [
    "FROZEN_ORDER_ONE_MEASUREMENT",
    "FROZEN_ORDER_ZERO_MEASUREMENT",
    "FROZEN_ZLIB_REFERENCE_BYTES",
    "CompressionMeasurementError",
    "ModelMeasurement",
    "canonical_codes",
    "code_lengths",
    "decode_corpus_bytes",
    "measure_order_one",
    "measure_order_zero",
    "table_bits",
]


class CompressionMeasurementError(ValueError):
    """رفضٌ عند القياس: بايتاتٌ لا تطابق المُجمَّد، أو مطابقةٌ لم تتحقّق."""


def decode_corpus_bytes(data: bytes) -> str:
    """يتحقّق من طول البايتات وبصمتها قبل فكّ ترميزها، ويرفض ما سواها."""

    if len(data) != FROZEN_CORPUS.byte_length:
        raise CompressionMeasurementError(
            f"طولُ البايتات {len(data)} لا يطابق المُجمَّد {FROZEN_CORPUS.byte_length}"
        )
    digest = hashlib.sha256(data).hexdigest()
    if digest != FROZEN_CORPUS.sha256_hex:
        raise CompressionMeasurementError(
            f"بصمةُ البايتات {digest} لا تطابق المُجمَّد {FROZEN_CORPUS.sha256_hex}"
        )
    return data.decode("utf-8")


def _tie_key(
    rule: TieBreakRule, depth: int, size: int, smallest: int
) -> tuple[int, ...]:
    if rule is TieBreakRule.SMALLEST_CODEPOINT:
        return (smallest,)
    return (depth, size, smallest)


def code_lengths(freqs: Mapping[str, int], rule: TieBreakRule) -> dict[str, int]:
    """أطوالُ شفرات هفمان تحت قاعدةِ تعادلٍ كليّة.

    الكلفةُ (الحمولة) واحدةٌ تحت أيّ قاعدة، وما تختاره القاعدةُ هو شكلُ الشجرة
    ومنه مجموعُ الأطوال ومنه حجمُ الجدول.
    """

    if not freqs:
        raise CompressionMeasurementError("لا شفرةَ لتوزيعٍ خالٍ من الرموز")
    if len(freqs) == 1:
        return {next(iter(freqs)): 1}
    heap: list[tuple[int, tuple[int, ...], int]] = []
    subtrees: list[dict[str, int]] = []
    for symbol, frequency in sorted(freqs.items()):
        point = ord(symbol)
        heap.append((frequency, _tie_key(rule, 0, 1, point), len(subtrees)))
        subtrees.append({symbol: 0})
    heapq.heapify(heap)
    while len(heap) > 1:
        first_frequency, _, first_index = heapq.heappop(heap)
        second_frequency, _, second_index = heapq.heappop(heap)
        merged = {symbol: depth + 1 for symbol, depth in subtrees[first_index].items()}
        merged.update(
            {symbol: depth + 1 for symbol, depth in subtrees[second_index].items()}
        )
        key = _tie_key(
            rule,
            max(merged.values()),
            len(merged),
            min(ord(symbol) for symbol in merged),
        )
        heapq.heappush(heap, (first_frequency + second_frequency, key, len(subtrees)))
        subtrees.append(merged)
    return subtrees[heap[0][2]]


def canonical_codes(lengths: Mapping[str, int]) -> dict[str, str]:
    """الشفرةُ القانونيّة: تتحدّد بـ(الطول، الرمز) وحدهما لا بشكل الشجرة."""

    codes: dict[str, str] = {}
    code = 0
    previous: int | None = None
    for symbol in sorted(lengths, key=lambda item: (lengths[item], item)):
        length = lengths[symbol]
        if previous is not None:
            code = (code + 1) << (length - previous)
        previous = length
        codes[symbol] = format(code, f"0{length}b")
    return codes


def table_bits(lengths: Mapping[str, int]) -> int:
    """حجمُ الجدول بالتمثيل المُعلَن: نقطةُ كودٍ، ثمّ طولٌ، ثمّ الشفرةُ نفسها."""

    return sum(
        TABLE_ENTRY_CODEPOINT_BITS + TABLE_ENTRY_LENGTH_FIELD_BITS + length
        for length in lengths.values()
    )


@dataclass(frozen=True, slots=True)
class ModelMeasurement:
    """قياسُ نموذجٍ واحد: حمولةٌ وجدولٌ معًا، ومطابقةٌ محقّقةٌ شرطًا للإصدار."""

    model: str
    tie_break: TieBreakRule
    alphabet_size: int
    raw_byte_length: int
    payload_bits: int
    table_bits: int
    round_trip_verified: bool

    def __post_init__(self) -> None:
        if not self.round_trip_verified:
            raise CompressionMeasurementError(
                "رقمُ ضغطٍ بلا مطابقةٍ محقّقةٍ لا يُصدَر: المطابقةُ شرطُ إصدارٍ " "لا بندُ تقرير"
            )
        if self.alphabet_size <= 0 or self.raw_byte_length <= 0:
            raise CompressionMeasurementError("قياسٌ بلا رموزٍ أو بلا بايتاتٍ مقيسة")
        if self.payload_bits <= 0 or self.table_bits <= 0:
            raise CompressionMeasurementError("الحمولةُ والجدولُ موجبان معًا")

    @property
    def total_bits(self) -> int:
        """الحجمُ الكلّيُّ القابل لفكّ الترميز من الصفر: حمولةٌ وجداول."""

        return self.payload_bits + self.table_bits

    @property
    def payload_ratio_percent(self) -> float:
        return 100.0 * (1.0 - (self.payload_bits / 8.0) / self.raw_byte_length)

    @property
    def total_ratio_percent(self) -> float:
        return 100.0 * (1.0 - (self.total_bits / 8.0) / self.raw_byte_length)

    def as_two_sizes(self) -> tuple[str, str]:
        """الرقمان معًا دائمًا: حمولةٌ وحدها، ثمّ كلّيٌّ قابلٌ لفكّ الترميز."""

        return (
            f"حمولة {self.payload_bits:,} بت = {self.payload_ratio_percent:.4f}%",
            f"كلّي {self.total_bits:,} بت = {self.total_ratio_percent:.4f}%",
        )


def _encode(text: str, codes: Mapping[str, str]) -> str:
    return "".join([codes[character] for character in text])


def _decode_order_zero(bits: str, codes: Mapping[str, str]) -> str:
    inverse = {code: symbol for symbol, code in codes.items()}
    decoded: list[str] = []
    current = ""
    for bit in bits:
        current += bit
        symbol = inverse.get(current)
        if symbol is not None:
            decoded.append(symbol)
            current = ""
    if current:
        raise CompressionMeasurementError("بقيت بتّاتٌ لا تُكوِّن شفرةً تامّة")
    return "".join(decoded)


def measure_order_zero(
    data: bytes, rule: TieBreakRule = TieBreakRule.SMALLEST_CODEPOINT
) -> ModelMeasurement:
    """هفمان رتبةَ صفرٍ على توزيع الرمز الواحد، بمطابقةٍ شرطًا للإصدار."""

    text = decode_corpus_bytes(data)
    frequencies = Counter(text)
    lengths = code_lengths(frequencies, rule)
    codes = canonical_codes(lengths)
    bits = _encode(text, codes)
    payload = sum(frequencies[symbol] * lengths[symbol] for symbol in frequencies)
    if len(bits) != payload:
        raise CompressionMeasurementError("طولُ البتّات المكتوبة يخالف الكلفةَ المحسوبة")
    round_trip = _decode_order_zero(bits, codes).encode("utf-8") == data
    return ModelMeasurement(
        model="هفمان رتبة صفر",
        tie_break=rule,
        alphabet_size=len(frequencies),
        raw_byte_length=len(data),
        payload_bits=payload,
        table_bits=table_bits(lengths),
        round_trip_verified=round_trip,
    )


def _context_frequencies(text: str) -> dict[str, Counter[str]]:
    per_context: dict[str, Counter[str]] = {}
    previous = FIRST_SYMBOL_CONTEXT
    for character in text:
        per_context.setdefault(previous, Counter())[character] += 1
        previous = character
    return per_context


def _decode_order_one(
    bits: str, codes: Mapping[str, Mapping[str, str]], symbol_count: int
) -> str:
    inverse = {
        context: {code: symbol for symbol, code in table.items()}
        for context, table in codes.items()
    }
    decoded: list[str] = []
    current = ""
    context = FIRST_SYMBOL_CONTEXT
    for bit in bits:
        current += bit
        symbol = inverse[context].get(current)
        if symbol is not None:
            decoded.append(symbol)
            context = symbol
            current = ""
            if len(decoded) == symbol_count:
                break
    if current:
        raise CompressionMeasurementError("بقيت بتّاتٌ لا تُكوِّن شفرةً تامّة")
    return "".join(decoded)


def measure_order_one(
    data: bytes, rule: TieBreakRule = TieBreakRule.SMALLEST_CODEPOINT
) -> ModelMeasurement:
    """هفمان رتبةً أولى بالجوار الحرفيّ: شفرةٌ لكلّ سياقِ رمزٍ سابقٍ حقيقيّ."""

    text = decode_corpus_bytes(data)
    per_context = _context_frequencies(text)
    lengths = {
        context: code_lengths(frequencies, rule)
        for context, frequencies in per_context.items()
    }
    codes = {context: canonical_codes(table) for context, table in lengths.items()}
    payload = sum(
        frequency * lengths[context][symbol]
        for context, frequencies in per_context.items()
        for symbol, frequency in frequencies.items()
    )
    emitted: list[str] = []
    context = FIRST_SYMBOL_CONTEXT
    for character in text:
        emitted.append(codes[context][character])
        context = character
    bits = "".join(emitted)
    if len(bits) != payload:
        raise CompressionMeasurementError("طولُ البتّات المكتوبة يخالف الكلفةَ المحسوبة")
    round_trip = _decode_order_one(bits, codes, len(text)).encode("utf-8") == data
    return ModelMeasurement(
        model="هفمان رتبة أولى",
        tie_break=rule,
        alphabet_size=len(Counter(text)),
        raw_byte_length=len(data),
        payload_bits=payload,
        table_bits=sum(table_bits(table) for table in lengths.values()),
        round_trip_verified=round_trip,
    )


FROZEN_ORDER_ZERO_MEASUREMENT: Final[ModelMeasurement] = ModelMeasurement(
    model="هفمان رتبة صفر",
    tie_break=TieBreakRule.SMALLEST_CODEPOINT,
    alphabet_size=51,
    raw_byte_length=FROZEN_CORPUS.byte_length,
    payload_bits=3_285_636,
    table_bits=1_721,
    round_trip_verified=True,
)
"""٦٨٫٨٨٣٧٪ حمولةً، و٦٨٫٨٦٧٤٪ كلّيًّا. يُعيد `examples/` اشتقاقَهما من البايتات."""

FROZEN_ORDER_ONE_MEASUREMENT: Final[ModelMeasurement] = ModelMeasurement(
    model="هفمان رتبة أولى",
    tie_break=TieBreakRule.SMALLEST_CODEPOINT,
    alphabet_size=51,
    raw_byte_length=FROZEN_CORPUS.byte_length,
    payload_bits=2_240_471,
    table_bits=21_589,
    round_trip_verified=True,
)
"""٧٨٫٧٨١٨٪ حمولةً، و**٧٨٫٥٧٧٤٪ كلّيًّا** — والرقمُ الثاني هو الرسميّ."""

FROZEN_ZLIB_REFERENCE_BYTES: Final[int] = 256_654
"""مرجعٌ خارجيّ (`zlib` مستوى ٩) = ٨٠٫٥٥٥١٪؛ سقفُ مقارنةٍ لا نموذجٌ من هنا."""


if preregistration_digest() != PREREGISTRATION_DIGEST:
    raise CompressionMeasurementError(
        "بصمةُ التجميد تغيّرت بعد كتابة القياس: يُعاد التجميد ولا تُصحَّح البصمة"
    )
