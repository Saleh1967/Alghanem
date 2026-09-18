"""قياسُ `ArabicRoundTripV1` على مدوّنةٍ مُبصَّمة، وموضعُ توقّفه فيها بالأرقام.

الجدولُ على ثماني عشرةَ حالةً مُضمَّنةً في وحدةٍ ليس مدوّنة؛ وهذه الوحدةُ
تُجمِّد قياسًا واحدًا على **نصٍّ مُودَعٍ في الشجرة تُشتَقّ بصمتُه منه**، فيُعاد
اشتقاقُ كلِّ عددٍ فيه بتشغيلٍ لا بقراءةِ سطر.

`A_FROZEN_FIGURE_IS_A_RE_RUN_NOT_A_QUOTATION`: كلُّ عددٍ هنا مكتوبٌ ليُكذَّب:
اختبارٌ يُعيد تشغيل الخطّ على البايتات نفسِها ويقارن **بصمةَ الجدول** لا عددًا
واحدًا منه، فتغيّرُ أيّ صفٍّ يُسقِط المطابقة.

`THE_MEASURED_TEXT_IS_A_TRANSCRIPTION_NOT_AN_EDITION`: النصُّ المقيسُ هنا نقلٌ
كُتب في هذه الشجرة ولم يُقابَل بطبعةٍ مُسمّاة، على ما صرّح به
`fatiha_source_text.A_TRANSCRIPTION_IS_NOT_AN_EDITION`؛ فالأرقامُ أرقامٌ عن هذا
النقل، لا عن مصحفٍ ولا عن رسمٍ عثمانيّ. والفرقُ بين الرسمين يقع في حوامل الألف
نفسِها، وهي بعينها موضعُ التوقّف المقيسُ أدناه، فلا يُنقَل هذا الرقمُ إلى نصٍّ
آخرَ بالقياس.

`A_MEASURED_TEXT_IS_NOT_A_MEASURED_LANGUAGE`: نصٌّ واحدٌ مقيسٌ لا يُقرأ حكمًا
على العربيّة، على منوال `THREE_SOURCES_ARE_CORPUS_BOUNDED` في المرماز؛ والمدوّنةُ
الكبرى المُبصَّمة تبقى في `UNMEASURED_ROUND_TRIP_SOURCES` بلا رقمٍ واحدٍ حتّى
تُشغَّل بايتاتُها.

`NO_FIGURE_IS_FROZEN_FOR_A_CORPUS_THIS_TREE_HAS_NOT_RUN`: ما لم تُشغَّل بايتاتُه
لا يُكتَب له عددٌ هنا ولو كان مُبصَّمًا في الشجرة؛ والبصمةُ تُعرِّف المصدرَ ولا
تُنتِج قياسًا.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest, is_canonical_digest
from .arabic_round_trip_v1 import (
    HaltCount,
    LayerOutcome,
    RoundTripLayer,
    RoundTripRefusal,
    RoundTripTable,
    measure_round_trip,
    tokens_from_text,
)
from .fatiha_source_text import (
    FATIHA_SOURCE_ID,
    source_byte_length,
    source_sha256,
)

__all__ = [
    "A_FROZEN_FIGURE_IS_A_RE_RUN_NOT_A_QUOTATION_NOTE",
    "A_MEASURED_TEXT_IS_NOT_A_MEASURED_LANGUAGE_NOTE",
    "FATIHA_ROUND_TRIP",
    "MEASURED_ROUND_TRIP_SOURCES",
    "NO_FIGURE_IS_FROZEN_FOR_A_CORPUS_THIS_TREE_HAS_NOT_RUN_NOTE",
    "THE_MEASURED_TEXT_IS_A_TRANSCRIPTION_NOT_AN_EDITION_NOTE",
    "UNMEASURED_ROUND_TRIP_SOURCES",
    "RoundTripCorpusMeasurement",
    "RoundTripCorpusError",
    "UnmeasuredRoundTripSource",
    "measure_deposited_text",
]


class RoundTripCorpusError(ValueError):
    """رفضٌ بنيويٌّ في قياس مدوّنة: مصدرٌ بلا بصمة، أو رقمٌ بلا تشغيل."""


@dataclass(frozen=True, slots=True)
class RoundTripCorpusMeasurement:
    """قياسُ الخطّ على مصدرٍ واحدٍ مُبصَّم، بجدولِه وموضعِ توقّفه وبصمتِه."""

    source_id: str
    source_sha256: str
    source_byte_length: int
    normalization_form: str
    unicode_database_version: str
    token_total: int
    end_to_end_reconstructed: int
    halt_profile: tuple[HaltCount, ...]
    table_digest: str

    def __post_init__(self) -> None:
        for value, name in (
            (self.source_id, "source id"),
            (self.normalization_form, "normalization form"),
            (self.unicode_database_version, "unicode database version"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise RoundTripCorpusError(f"{name} نصٌّ غيرُ خالٍ")
        if len(self.source_sha256) != 64:
            raise RoundTripCorpusError(
                "بصمةٌ ناقصةٌ لا يُعاد بها اشتقاقُ قياس؛ والبصمةُ أربعٌ وستّون حرفًا"
            )
        if not is_canonical_digest(self.table_digest):
            raise RoundTripCorpusError("بصمةُ الجدول بصمةٌ قانونيّةٌ مكتملة")
        if not isinstance(self.source_byte_length, int) or self.source_byte_length < 1:
            raise RoundTripCorpusError("طولُ المصدر بالبايت عددٌ موجب")
        if not isinstance(self.token_total, int) or self.token_total < 1:
            raise RoundTripCorpusError("قياسٌ على لا كلمةَ فيه ليس قياسًا على مدوّنةٍ خالية")
        if not 0 <= self.end_to_end_reconstructed <= self.token_total:
            raise RoundTripCorpusError(
                "ما رجع كما دخل لا يزيد على ما دخل ولا يكون سالبًا"
            )
        if not self.halt_profile:
            raise RoundTripCorpusError("قياسٌ بلا موضعِ توقّفٍ واحدٍ يُخفي أين وقف الخطّ")
        if sum(halt.count for halt in self.halt_profile) != self.token_total:
            raise RoundTripCorpusError(
                "مواضعُ التوقّف تستوعب كلَّ كلمةٍ دخلت مرّةً واحدة؛ وناقصُها "
                "يُسقِط كلماتٍ من السجلّ"
            )
        reconstructed = sum(
            halt.count
            for halt in self.halt_profile
            if halt.outcome is LayerOutcome.RECONSTRUCTED
            and halt.layer is RoundTripLayer.FINAL_BYTES
        )
        if reconstructed != self.end_to_end_reconstructed:
            raise RoundTripCorpusError(
                "عددُ ما رجع كما دخل يُقرأ من موضع التوقّف نفسِه؛ ورقمان "
                "مختلفان لواقعةٍ واحدةٍ دعوَيان متناقضتان"
            )

    @property
    def reconstruction_rate(self) -> float:
        """نسبةُ ما رجع بايتاتُه كما دخلت، على كلِّ ما دخل الخطّ لا على المقبول.

        وهذه النسبةُ **من أعلى الخطّ**: مقامُها كلُّ الكلمات، فما وقف عند
        طبقةٍ دونها يُخفِّضها ولا يخرج منها.
        """

        return self.end_to_end_reconstructed / self.token_total

    def halts_at(
        self, layer: RoundTripLayer, refusal: RoundTripRefusal | None = None
    ) -> int:
        """كم كلمةً وقفت عند طبقةٍ بعينها، وبسببٍ بعينه إن سُمّي."""

        return sum(
            halt.count
            for halt in self.halt_profile
            if halt.layer is layer and (refusal is None or halt.refusal is refusal)
        )

    def as_canonical_content(self) -> dict[str, object]:
        """المحتوى القانونيُّ للقياس، ومنه تُشتقّ بصمتُه."""

        return {
            "source_id": self.source_id,
            "source_sha256": self.source_sha256,
            "source_byte_length": self.source_byte_length,
            "normalization_form": self.normalization_form,
            "unicode_database_version": self.unicode_database_version,
            "token_total": self.token_total,
            "end_to_end_reconstructed": self.end_to_end_reconstructed,
            "halt_profile": [halt.as_canonical_content() for halt in self.halt_profile],
            "table_digest": self.table_digest,
        }

    @property
    def digest(self) -> str:
        """بصمةُ القياس كلِّه، مُشتقّةٌ لا مكتوبة."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))

    @classmethod
    def from_table(
        cls,
        table: RoundTripTable,
        *,
        source_id: str,
        source_sha256: str,
        source_byte_length: int,
    ) -> RoundTripCorpusMeasurement:
        """اقرأ القياسَ من جدولٍ شُغِّل؛ ولا يُنشأ قياسٌ من أعدادٍ مُمرَّرة."""

        if not isinstance(table, RoundTripTable):
            raise RoundTripCorpusError("القياسُ يُقرأ من جدولٍ شُغِّل لا من أرقام")
        return cls(
            source_id=source_id,
            source_sha256=source_sha256,
            source_byte_length=source_byte_length,
            normalization_form="NFC",
            unicode_database_version=unicodedata.unidata_version,
            token_total=table.token_total,
            end_to_end_reconstructed=table.end_to_end_reconstructed,
            halt_profile=table.halt_profile,
            table_digest=table.digest,
        )


def measure_deposited_text(
    text: str, *, source_id: str, source_sha256: str, source_byte_length: int
) -> RoundTripCorpusMeasurement:
    """شغِّل الخطَّ على نصٍّ مُودَعٍ بعد التحقّق من بصمته، ثمّ اقرأ قياسَه.

    والبصمةُ تُقاس على بايتات النصّ الواصلة، فلا يُقاس نصٌّ ويُنسَب إلى بصمةِ
    غيره.
    """

    encoded = text.encode("utf-8")
    measured_digest = canonical_digest(encoded)
    if measured_digest != source_sha256:
        raise RoundTripCorpusError(
            "بايتاتُ النصّ لا تُطابق البصمةَ المُعلَنة؛ وقياسُها تحت اسمها "
            "نسبةُ رقمٍ إلى مصدرٍ لم يُقَس"
        )
    if len(encoded) != source_byte_length:
        raise RoundTripCorpusError("طولُ البايتات لا يُطابق المُعلَن")
    table = measure_round_trip(tokens_from_text(text))
    return RoundTripCorpusMeasurement.from_table(
        table,
        source_id=source_id,
        source_sha256=source_sha256,
        source_byte_length=source_byte_length,
    )


FATIHA_ROUND_TRIP: Final[RoundTripCorpusMeasurement] = RoundTripCorpusMeasurement(
    source_id=FATIHA_SOURCE_ID,
    source_sha256=source_sha256(),
    source_byte_length=source_byte_length(),
    normalization_form="NFC",
    unicode_database_version="15.0.0",
    token_total=29,
    end_to_end_reconstructed=11,
    halt_profile=(
        HaltCount(
            layer=RoundTripLayer.SYLLABLE,
            outcome=LayerOutcome.REFUSED,
            refusal=RoundTripRefusal.SEGMENTATION_ONSETLESS_INITIAL_SAKIN,
            count=14,
        ),
        HaltCount(
            layer=RoundTripLayer.FINAL_BYTES,
            outcome=LayerOutcome.MISMATCHED,
            refusal=None,
            count=4,
        ),
        HaltCount(
            layer=RoundTripLayer.FINAL_BYTES,
            outcome=LayerOutcome.RECONSTRUCTED,
            refusal=None,
            count=11,
        ),
    ),
    table_digest="7025007494c12056566167d9712e8e5701122769cefbdbe488aa082ba2aa948b",
)
"""تسعٌ وعشرون كلمةً من إيداع الفاتحة، وموضعُ التوقّف واحدٌ مُسمًّى.

أربعَ عشرةَ كلمةً تقف عند طبقة المقطع بسببٍ واحدٍ بعينه: ساكنٌ لا متحرّكَ يفتح
له مقطعًا — وهو في كلِّ واقعةٍ منها ألفٌ عاريةٌ في أوّل الكلمة، أي همزةُ الوصل
التي سبق أن قرّرت الشجرةُ تعذُّرَها من العلامات المكتوبة
(`ibtida_wasl_waqf_registration.HAMZAT_WASL_IS_NOT_DECIDABLE_FROM_THE_WRITTEN_MARKS`).
فليس هذا عطبًا في التقطيع بل بلوغُه حدًّا قرّرته الشجرةُ قبله بجلسات.

وأربعُ كلماتٍ تصل أعلى الخطّ ثمّ تخرج بايتاتُها بترتيبٍ آخر — الشدّةُ قبل
الحركة في كتابة المرماز — بفقدٍ صفرٍ وزيادةٍ صفر. وإحدى عشرةَ كلمةً تعود
بايتاتُها كما دخلت.

ويُعاد اشتقاقُ هذه الأعداد كلِّها من
`examples/arabic/measure_arabic_round_trip_v1.py --deposit`، ويقارنها اختبارٌ
ببصمة الجدول لا بعددٍ واحدٍ منه.
"""


MEASURED_ROUND_TRIP_SOURCES: Final[tuple[RoundTripCorpusMeasurement, ...]] = (
    FATIHA_ROUND_TRIP,
)
"""المصادرُ التي شُغِّل عليها الخطُّ فعلًا. واحدٌ، وهو نصٌّ صغيرٌ مُودَع."""


@dataclass(frozen=True, slots=True)
class UnmeasuredRoundTripSource:
    """مصدرٌ مُبصَّمٌ في الشجرة لم يُشغَّل عليه الخطُّ: اسمُه وبصمتُه وسببُ امتناعه."""

    source_id: str
    source_sha256: str
    source_byte_length: int
    why_no_figure_is_frozen: str

    def __post_init__(self) -> None:
        if len(self.source_sha256) != 64:
            raise RoundTripCorpusError("بصمةُ المصدر أربعٌ وستّون حرفًا")
        if not self.why_no_figure_is_frozen.strip():
            raise RoundTripCorpusError(
                "مصدرٌ بلا سببٍ مُسمًّى لامتناع قياسه يُقرأ بعد جلساتٍ مقيسًا"
            )


UNMEASURED_ROUND_TRIP_SOURCES: Final[tuple[UnmeasuredRoundTripSource, ...]] = (
    UnmeasuredRoundTripSource(
        source_id=(
            "Quranic Arabic Corpus (morphology) 0.4, segments joined into word "
            "tokens by (sura:aya:word)"
        ),
        source_sha256=(
            "a1d12923815341face765083805d2148ed2d9f5cc3f7d6665219d887675d8c46"
        ),
        source_byte_length=6_309_503,
        why_no_figure_is_frozen=(
            "بايتاتُها ليست في هذه الشجرة، ولم يُشغَّل عليها الخطُّ هنا؛ "
            "و`QURANIC_CORPUS_INVERTIBILITY` قياسٌ لطبقة الحامل/الحالة وحدَها "
            "لا للخطّ كلِّه، فلا يُقرأ عددُه عددًا لهذا الخطّ. ويُشغَّل عليها "
            "بتسليم بايتاتها إلى "
            "`examples/arabic/measure_arabic_round_trip_v1.py`"
        ),
    ),
)
"""مصدرٌ مُبصَّمٌ بلا رقمٍ واحدٍ هنا؛ والبصمةُ تُعرِّفه ولا تقيسه."""


A_FROZEN_FIGURE_IS_A_RE_RUN_NOT_A_QUOTATION_NOTE: Final[str] = (
    "AFrozenFigureIsARerunNotAQuotation: كلُّ عددٍ مُجمَّدٍ هنا يُعاد اشتقاقُه "
    "بتشغيل الخطّ على البايتات نفسِها، ويُقارَن ببصمة الجدول لا بعددٍ واحدٍ منه"
)

A_MEASURED_TEXT_IS_NOT_A_MEASURED_LANGUAGE_NOTE: Final[str] = (
    "AMeasuredTextIsNotAMeasuredLanguage: نصٌّ واحدٌ مقيسٌ لا يُقرأ حكمًا على "
    "العربيّة؛ والاستقراءُ على نصٍّ مغلقٍ محدودٌ به"
)

THE_MEASURED_TEXT_IS_A_TRANSCRIPTION_NOT_AN_EDITION_NOTE: Final[str] = (
    "TheMeasuredTextIsATranscriptionNotAnEdition: المقيسُ نقلٌ في الشجرة لم "
    "يُقابَل بطبعةٍ مُسمّاة، ورسمُه إملائيٌّ لا عثمانيّ؛ والفرقُ بينهما يقع في "
    "حوامل الألف، وهي بعينها موضعُ التوقّف المقيس"
)

NO_FIGURE_IS_FROZEN_FOR_A_CORPUS_THIS_TREE_HAS_NOT_RUN_NOTE: Final[str] = (
    "NoFigureIsFrozenForACorpusThisTreeHasNotRun: المدوّنةُ المُبصَّمةُ التي لم "
    "تُشغَّل بايتاتُها تبقى بلا عددٍ واحد؛ والبصمةُ تُعرِّف المصدرَ ولا تُنتِج "
    "قياسًا"
)
