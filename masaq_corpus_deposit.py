"""إيداع مدوّنة MASAQ — شاهدٌ مُبصَّم، لا دعوى عن العربية.

`A_COUNT_IS_RELATIVE_TO_ITS_COUNTING_RULE`: كلُّ عددٍ هنا يحمل قاعدةَ عدِّه
بنصِّها، ودالّةَ إعادة اشتقاقه. فـ«عدد الأسطر» و«عدد السجلّات» رقمان
مختلفان لهذا الملفّ بعينه (١٥٧٬٨٥٤ مقابل ١٥٧٬٦٧٧)، والفارقُ سببُه مُقاسٌ
لا مُقدَّر: ١٥٤ سجلًّا تحوي فواصلَ أسطرٍ مضمّنةً داخل حقولها.

`CompleteInductionIsCorpusBounded`: كلُّ عددٍ هنا وصفٌ تامٌّ لهذه المدوّنة
وحدها. «٤٬٢١٦ مصدرًا» ليس عددَ المصادر في العربية، بل عددَ المقاطع
الموسومة GERUND في هذه البايتات بعينها.

`AnImportedTagIsAHumanJudgementNotAMeasurement`: الوسومُ اجتهادُ مُوسِّمين
بشريّين بمنهجية الإعراب التراثيّ. فصفرُ صنفٍ يعني «لم يُوسَم هنا»، لا
«لا وجود له في العربية».

`WITNESS_BYTES_ARE_NOT_VENDORED`: رخصةُ MASAQ (CC BY 3.0) تُجيز إعادةَ
التوزيع بشرط النسبة، خلافًا لـQAC وTanzil. ومع ذلك لا تُحشَر البايتات
هنا: المسارُ يُمرَّر، والبصمةُ تُطابَق قبل أيّ رقم.
"""
from __future__ import annotations

import csv
import hashlib
from dataclasses import dataclass
from typing import Final

MASAQ_SHA256: Final[str] = "d43d2a813afbe0490254bb26623d6041ed352a273d333e731ddbcda3bd0b6f3a"
MASAQ_BYTE_LENGTH: Final[int] = 20_302_008

ATTRIBUTION: Final[str] = (
    "MASAQ: Morphologically-Analyzed and Syntactically-Annotated Quran. "
    "Majdi Sawalha, University of Jordan. DOI 10.17632/9yvrzxktmr.2. "
    "Licensed CC BY 3.0 — attribution is a licence condition, not a courtesy."
)

LINE_COUNTING_RULE: Final[str] = (
    "عددُ الأسطر الخام (splitlines) = 157,854. وعددُ سجلّات CSV = 157,677 "
    "(بلا الترويسة). والفارقُ 176 سببُه مُقاسٌ لا مُقدَّر: 154 سجلًّا تحوي "
    "فواصلَ أسطرٍ مضمّنة، مع سطر الترويسة. الملفُّ ينتهي بفاصل سطر."
)

WORD_KEY_RULE: Final[str] = (
    "مفتاحُ الكلمة = (Sura_No, Verse_No, Column5). والعمودُ Word_No رقمُ "
    "المقطعِ داخلَ الكلمة لا رقمُ الكلمة — وخلطُهما يُسقِط المطابقةَ "
    "الموضعيّة مع QAC إلى الصفر تقريبًا."
)


class MasaqDepositError(RuntimeError):
    """رفضٌ عند القراءة: بايتاتٌ لا تطابق البصمةَ أو الطول."""


@dataclass(frozen=True, slots=True)
class RederivedFigure:
    """رقمٌ مع قاعدةِ عدِّه ودالّةِ إعادة اشتقاقه — لا رقمٌ عارٍ."""

    name: str
    value: int
    counting_rule: str

    def __post_init__(self) -> None:
        if not self.name.strip() or not self.counting_rule.strip():
            raise MasaqDepositError("رقمٌ بلا اسمٍ أو بلا قاعدةِ عدّ")
        if self.value < 0:
            raise MasaqDepositError("عددٌ سالب")


def read_masaq_bytes(path: str) -> bytes:
    """تُرجِع البايتات بعد مطابقةِ البصمةِ والطول، أو تَرفض."""
    with open(path, "rb") as handle:
        data = handle.read()
    if len(data) != MASAQ_BYTE_LENGTH:
        raise MasaqDepositError(f"طولٌ مخالف: {len(data)} ≠ {MASAQ_BYTE_LENGTH}")
    digest = hashlib.sha256(data).hexdigest()
    if digest != MASAQ_SHA256:
        raise MasaqDepositError(f"بصمةٌ مخالفة: {digest}")
    return data


def rederive_record_count(data: bytes) -> int:
    text = data.decode("utf-8-sig")
    return sum(1 for _ in csv.DictReader(text.splitlines()))


def rederive_word_position_count(data: bytes) -> int:
    text = data.decode("utf-8-sig")
    return len({
        (row["Sura_No"], row["Verse_No"], row["Column5"])
        for row in csv.DictReader(text.splitlines())
    })


def rederive_tag_count(data: bytes, tag: str) -> int:
    text = data.decode("utf-8-sig")
    return sum(1 for row in csv.DictReader(text.splitlines()) if row["Morph_tag"] == tag)


SEGMENT_RULE: Final[str] = "عددُ المقاطع الصرفية الموسومة بهذا الوسم، لا عددُ الكلمات ولا الآيات"

DEPOSITED_FIGURES: Final[tuple[RederivedFigure, ...]] = (
    RederivedFigure("raw_lines", 157_854, "splitlines على النصّ بعد حذف BOM"),
    RederivedFigure("csv_records", 157_677, "سجلّات csv.DictReader، بلا الترويسة"),
    RederivedFigure("embedded_newline_records", 154, "سجلّاتٌ يحوي أحدُ حقولها فاصلَ سطر"),
    RederivedFigure("columns", 19, "عددُ الحقول في كلّ سجلّ؛ ثابتٌ في 157,678 سجلًّا"),
    RederivedFigure("word_positions", 77_411, WORD_KEY_RULE),
    RederivedFigure("distinct_morph_tags", 133, "قيمُ Morph_tag المميّزة، شاملةً الفارغ"),
    RederivedFigure("GERUND", 4_216, SEGMENT_RULE),
    RederivedFigure("GERUND_MEEM", 125, SEGMENT_RULE),
    RederivedFigure("GERUND_INSTANT", 84, SEGMENT_RULE),
    RederivedFigure("GERUND_PROFESSION", 38, SEGMENT_RULE),
    RederivedFigure("GERUND_STATE", 2, SEGMENT_RULE),
    RederivedFigure("NOUN_TIME_PLACE", 225, SEGMENT_RULE),
    RederivedFigure("NOUN_INSTRUMENT", 24, SEGMENT_RULE),
    RederivedFigure("NOUN_ACTIVE_PART", 3_156, SEGMENT_RULE),
    RederivedFigure("NOUN_PASSIVE_PART", 501, SEGMENT_RULE),
    RederivedFigure("ADJ_QUALIT", 1_646, SEGMENT_RULE),
    RederivedFigure("ADJ_INTENS", 459, SEGMENT_RULE),
    RederivedFigure("ADJ_COMP", 643, SEGMENT_RULE),
    RederivedFigure("NOUN_RELATIVE", 125, SEGMENT_RULE),
    RederivedFigure("NOUN_DIMINUTIVE", 1, SEGMENT_RULE),
)

WHAT_THIS_CLOSES: Final[str] = (
    "الأصنافُ الاشتقاقية التي لا يَسِمها QAC — المصدرُ بأنواعه، واسمُ "
    "الزمان/المكان، واسمُ الآلة، والصفةُ المشبّهة، وصيغةُ المبالغة، واسمُ "
    "التفضيل — موسومةٌ هنا بوسمٍ بشريٍّ صريح. وهذا يُخرِجها من مرتبةِ "
    "«مرشَّحٌ بلا مرجع» إلى مرتبةِ «قابلٌ للقياس ضدّ ذهبٍ بشريّ»."
)

WHAT_THIS_DOES_NOT_CLOSE: Final[str] = (
    "لا عمودَ جذرٍ في MASAQ. فالربطُ بـQAC وبمقاييس يقع موضعيًّا "
    "(سورة، آية، كلمة) لا بالجذر — وهذا يُدخِل مخاطرَ محاذاةٍ مُقاسةً "
    "لا مُفترَضة: خلطُ Word_No بـColumn5 أسقط الدقّةَ من 23.3% إلى 0.3% "
    "في قياسٍ فعليّ."
)
