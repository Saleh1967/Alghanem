"""قياسُ خطِّ الذهاب والإياب على جذور «مقاييس اللغة» المُودَعة: المجتمعُ لا النسبة.

المقيسُ قبل هذه الوحدة نصٌّ واحدٌ من تسعٍ وعشرين كلمةً مشكولةً بتمامها، ونسبةُ
استرجاعه تامّة. ورفعُ نسبةٍ بلغت غايتَها لا يُنتج عددًا، فالخطوةُ المُعلَنة
توسيعُ المجتمع. وبايتاتُ مدوّنةٍ ثانيةٍ **حاضرةٌ في هذه الشجرة ومُبصَّمة** —
`maqayis_by_root_csv_999.csv` — فتُشغَّل عليها الطبقاتُ الستُّ نفسُها بلا
انتظارِ ملفٍّ لم يصل، وتُقرأ النتيجةُ كما خرجت.

`THE_POPULATION_IS_DERIVED_FROM_DEPOSITED_BYTES`: مجتمعُ القياس ليس قائمةً
مكتوبةً بيدٍ، بل هو `root_full` المتمايزةُ من الصفوف التي `root_type` فيها
«ثلاثي» بالضبط — قاعدةُ العدّ نفسُها المُجمَّدةُ في
`TRILATERAL_ROOT_COUNTING_RULE` — مرتّبةً ترتيبًا مُعلَنًا ليكون التشغيلُ
مُعادًا لا مُقارَبًا. ولا تُحذَف سلسلةٌ بعد رؤية حكمها.

`A_ROOT_STRING_IS_NOT_A_WORD`: المقيسُ ههنا **سلاسلُ مداخلِ معجمٍ** غيرُ
مشكولة، لا كلماتٌ في سياق. فما يخرج من هذا القياس خبرٌ عن سلوك الخطّ على هذا
الجنس من السلاسل، لا عن كلمات العربية ولا عن نصٍّ منها.

`ZERO_IS_A_MEASURED_NUMBER_NOT_A_FAILURE_TO_HIDE`: لم يرجع من السلاسل شيءٌ
بايتاتُه كما دخلت، ونسبةُ الاسترجاع صفرٌ من أربعة آلافٍ وسبعةٍ وثمانين. ولا
يُخرِج هذا القياسَ من السجلّ ولا يُرفَع مقامُه إلى ما قبلته الطبقاتُ الدنيا:
المقامُ كلُّ ما دخل الخطّ، والصفرُ خبرٌ يُقال.

`THE_HALT_IS_ONE_NAMED_CAUSE_NOT_A_BLANKET_REFUSAL`: الوقوفُ كلُّه عند طبقةٍ
واحدةٍ بعلّةٍ واحدةٍ مُسمّاة — `SEGMENTATION_ONSETLESS_INITIAL_SAKIN` — إذ
تبلغ السلاسلُ كلُّها طبقةَ الحامل/الحالة وتعود منها كما دخلت، ثمّ يقف الخطُّ
عند المقطع لأنّ حركةً مكتوبةً واحدةً ليست في هذه السلاسل. فالمقيسُ حدُّ
**التقطيع على غير المشكول**، لا عجزٌ عامٌّ عن الجذور.

`AN_UNVOCALISED_LIMIT_IS_NOT_AN_ARABIC_LAW`: أنّ هذا الخطَّ لا يُقطِّع سلسلةً
بلا حركاتٍ مكتوبةٍ حكمٌ على دالّة التقطيع في هذه الشجرة، لا على العربية غيرِ
المشكولة؛ فليس في هذا القياس دعوى أنّ غيرَ المشكول لا يُقطَّع، وإنّما أنّ
**هذه** الدالّةَ لا تُقطِّعه، وهي لم تُبنَ له.

`A_COUNT_IN_A_FILE_IS_NOT_A_COUNT_IN_ARABIC`: أربعةُ آلافٍ وسبعةٌ وثمانون عددُ
جذورٍ متمايزةٍ **في هذا الملفّ** تحت قاعدة عدِّه، على رسمِ المعجم نفسِه؛ وليس
عددَ الجذور الثلاثيّة في العربية ولا عند ابن فارس.

`THIS_IS_A_MEASUREMENT_NOT_AN_AUTHORITY`: لا ولادةَ هنا، ولا حكمَ ولادة، ولا
تجميدَ `E0`، ولا استيرادَ من `kernel/`؛ ولا تُرفَع بهذه الوحدة طبقةٌ محجوبة،
ولا يُصدَر بها تصنيفُ جذرٍ ولا وزنٍ ولا مقطع.
"""

from __future__ import annotations

from pathlib import Path
from typing import Final

from .arabic_round_trip_corpus import (
    RoundTripCorpusError,
    RoundTripCorpusMeasurement,
)
from .arabic_round_trip_v1 import (
    HaltCount,
    LayerOutcome,
    RoundTripLayer,
    RoundTripRefusal,
    measure_round_trip,
)
from .maqayis_root_table_deposit import (
    FROZEN_ROOT_TABLE,
    TRILATERAL_ROOT_TYPE,
    root_table_rows,
)

__all__ = [
    "A_COUNT_IN_A_FILE_IS_NOT_A_COUNT_IN_ARABIC_NOTE",
    "AN_UNVOCALISED_LIMIT_IS_NOT_AN_ARABIC_LAW_NOTE",
    "A_ROOT_STRING_IS_NOT_A_WORD_NOTE",
    "MAQAYIS_TRILATERAL_ROOT_ROUND_TRIP",
    "MAQAYIS_TRILATERAL_ROOT_SOURCE_ID",
    "THE_HALT_IS_ONE_NAMED_CAUSE_NOT_A_BLANKET_REFUSAL_NOTE",
    "THE_POPULATION_IS_DERIVED_FROM_DEPOSITED_BYTES_NOTE",
    "TRILATERAL_ROOT_ORDERING_RULE",
    "ZERO_IS_A_MEASURED_NUMBER_NOT_A_FAILURE_TO_HIDE_NOTE",
    "measure_trilateral_roots",
    "trilateral_root_strings",
    "trilateral_root_tokens",
]


MAQAYIS_TRILATERAL_ROOT_SOURCE_ID: Final[str] = (
    "Maqāyīs al-Lugha root table (maqayis_by_root_csv_999.csv), distinct "
    "`root_full` values of rows whose `root_type` is «ثلاثي», as written"
)
"""اسمُ المصدر ومجتمعُه في عبارةٍ واحدة؛ فلا يُقرأ الرقمُ على ملفٍّ كلِّه."""


TRILATERAL_ROOT_ORDERING_RULE: Final[str] = (
    "السلاسلُ مرتّبةٌ ترتيبَ نقاط يونيكود تصاعديًّا (`sorted`) بعد رفع "
    "التكرار، لا ترتيبَ ورودها في الملفّ؛ والترتيبُ مُعلَنٌ لأنّ فهرسَ "
    "الكلمة في الجدول المُشتقّ يتبعه، ولا يتبعه عددٌ من أعداد القياس"
)
"""قاعدةُ الترتيب تُعلَن مع قاعدة العدّ: تشغيلٌ يُعاد لا يُقارَب."""


A_ROOT_STRING_IS_NOT_A_WORD_NOTE: Final[str] = (
    "المقيسُ سلاسلُ مداخلِ معجمٍ غيرُ مشكولةٍ لا كلماتٌ في سياق؛ فالخبرُ عن "
    "سلوك الخطّ على هذا الجنس من السلاسل لا عن كلمات العربية"
)

THE_POPULATION_IS_DERIVED_FROM_DEPOSITED_BYTES_NOTE: Final[str] = (
    "المجتمعُ مُشتقٌّ من البايتات المُبصَّمة بقاعدةٍ مُعلَنة، لا قائمةً "
    "مكتوبةً بيدٍ تُنتقى بعد رؤية أحكامها"
)

ZERO_IS_A_MEASURED_NUMBER_NOT_A_FAILURE_TO_HIDE_NOTE: Final[str] = (
    "صفرُ الاسترجاع رقمٌ مقيسٌ يُسجَّل بمقامه كاملًا، ولا يُرفَع مقامُ "
    "القياس إلى ما قبلته الطبقاتُ الدنيا لتحسين نسبته"
)

THE_HALT_IS_ONE_NAMED_CAUSE_NOT_A_BLANKET_REFUSAL_NOTE: Final[str] = (
    "الوقوفُ كلُّه عند طبقة المقطع بعلّةٍ واحدةٍ مُسمّاةٍ في مفردةٍ مغلقة، "
    "فيُقرأ موضعُ الحدّ ولا يُطوى في رفضٍ عامّ"
)

AN_UNVOCALISED_LIMIT_IS_NOT_AN_ARABIC_LAW_NOTE: Final[str] = (
    "الحدُّ على دالّة التقطيع في هذه الشجرة لا على العربية غيرِ المشكولة؛ "
    "فالدالّةُ لم تُبنَ لها، وامتناعُها ليس دعوى امتناعٍ في اللغة"
)

A_COUNT_IN_A_FILE_IS_NOT_A_COUNT_IN_ARABIC_NOTE: Final[str] = (
    "عددُ الجذور عددٌ في هذا الملفّ تحت قاعدة عدِّه وعلى رسمِه، لا عددٌ في "
    "العربية ولا عند ابن فارس"
)


def trilateral_root_strings(root: Path | None = None) -> tuple[str, ...]:
    """سلاسلُ الجذور الثلاثيّة المتمايزة من البايتات المُبصَّمة، مرتّبةً بقاعدتها."""

    strings = {
        row["root_full"]
        for row in root_table_rows(root)
        if row["root_type"] == TRILATERAL_ROOT_TYPE
    }
    if not strings:
        raise RoundTripCorpusError(
            "لا جذرَ ثلاثيًّا في البايتات المقروءة؛ ومجتمعٌ خالٍ لا يُقاس عليه"
        )
    return tuple(sorted(strings))


def trilateral_root_tokens(root: Path | None = None) -> tuple[bytes, ...]:
    """بايتاتُ تلك السلاسل بترميز الملفّ نفسِه؛ ومدخلُ الخطّ بايتاتٌ خام."""

    return tuple(string.encode("utf-8") for string in trilateral_root_strings(root))


def measure_trilateral_roots(root: Path | None = None) -> RoundTripCorpusMeasurement:
    """شغِّل الطبقاتِ الستَّ على مجتمع الجذور، واقرأ القياسَ من جدولٍ شُغِّل."""

    table = measure_round_trip(trilateral_root_tokens(root))
    return RoundTripCorpusMeasurement.from_table(
        table,
        source_id=MAQAYIS_TRILATERAL_ROOT_SOURCE_ID,
        source_sha256=FROZEN_ROOT_TABLE.sha256_hex,
        source_byte_length=FROZEN_ROOT_TABLE.byte_length,
    )


MAQAYIS_TRILATERAL_ROOT_ROUND_TRIP: Final[RoundTripCorpusMeasurement] = (
    RoundTripCorpusMeasurement(
        source_id=MAQAYIS_TRILATERAL_ROOT_SOURCE_ID,
        source_sha256=FROZEN_ROOT_TABLE.sha256_hex,
        source_byte_length=FROZEN_ROOT_TABLE.byte_length,
        normalization_form="NFC",
        unicode_database_version="15.0.0",
        token_total=4_087,
        end_to_end_reconstructed=0,
        halt_profile=(
            HaltCount(
                layer=RoundTripLayer.SYLLABLE,
                outcome=LayerOutcome.REFUSED,
                refusal=RoundTripRefusal.SEGMENTATION_ONSETLESS_INITIAL_SAKIN,
                count=4_087,
            ),
        ),
        table_digest=(
            "03d3db248491a2c8cbd9da2b5e66c0e3e2b6cdf9411974fed5e2f63d3d717ccb"
        ),
    )
)
"""أربعةُ آلافٍ وسبعةٌ وثمانون سلسلةً، لم ترجع واحدةٌ منها بايتاتُها كما دخلت.

والخبرُ في **موضع الوقوف** لا في النسبة: السلاسلُ كلُّها تُفَكّ بـ UTF-8،
وتُطابق تسويةَ `NFC` كما وردت، وتدخل الحامل/الحالة وتعود منها ذرّةً ذرّةً؛ ثمّ
يقف الخطُّ كلُّه عند طبقة المقطع بعلّةٍ واحدةٍ مُسمّاة: مفتتحٌ بلا حركةٍ
مكتوبة. فهذه أوّلُ مرّةٍ يُقاس فيها الخطُّ على سلاسلَ غيرِ مشكولة، والمقيسُ
حدُّه هو عليها.

وثلاثُ طبقاتٍ من ستٍّ تُصرِّح بمقامٍ كاملٍ (٤٠٨٧ من ٤٠٨٧) بلا رفضٍ ولا
مخالفةٍ ولا ذرّةٍ مفقودة، وطبقتان فوق المقطع مقامُهما صفرٌ لأنّه لم يبلغهما
شيء. والصفرُ فوقُ إفصاحٌ عن التوقّف تحتَه، لا نتيجةً ثانية.

ويُعاد اشتقاقُ هذه الأعداد كلِّها من
`examples/arabic/measure_maqayis_root_round_trip.py`، ويقارنها اختبارٌ ببصمة
الجدول لا بعددٍ واحدٍ منه. و`unicode_database_version` تسجيلٌ للبيئة التي
جُمِّد فيها القياس لا شرطٌ على من يُعيد تشغيله؛ والواجبُ إعادةُ اشتقاق
`figures_digest` بعينه.
"""
