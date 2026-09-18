"""`G0.EXEC-0.LAWS`: قوانينُ آليّة التنفيذ المربوط، مُجمَّدةً قبل أيّ تشغيل.

    EvaluationBoundary != ExecutionMechanism

طبقةُ التقييم نقيّةٌ: أنواعٌ وعقودٌ وبصمات، لا عمليّاتٌ ولا ملفّاتٌ مؤقّتة. وهذه
الحزمةُ آليّةُ التشغيل فوقها، وتستوردها ولا تُستورَد منها؛ فلو فُتِح في تلك
الطبقة بابُ `subprocess` و`open` ثمّ قيل إنّ عزلَها كما كان، كان ذلك ادّعاءً
صامتًا بعزلٍ لم يَعُد قائمًا.

    SeparateProcess != Sandbox

عمليّةٌ منفصلةٌ ببيئةٍ مُقلَّمةٍ ومساحةِ عملٍ مؤقّتةٍ خارج الشجرة أقوى من تنفيذٍ
داخل عمليّة التقييم نفسها، وليست حبسًا مُثبَتًا: لا `seccomp`، ولا قطعَ شبكة،
ولا حبسَ نظام ملفّاتٍ تامّ. فالحالُ `SEPARATE_PROCESS_DECLARED`، و`is_proven`
كاذبةٌ بالبناء.

    MeasuredBytesAreExecutedBytes
    ExecutedReaderIdentity == FrozenReaderIdentity
    ImplementationChangedDuringExecution -> NoReferenceRunReport
    NoComparisonBeforeBoundExecution
"""

from __future__ import annotations

from typing import Final

from ..evaluation import (
    A_HARNESS_IS_NOT_AN_EXECUTION_AUTHORITY,
    AN_IN_PROCESS_SEAL_IS_NOT_UNFORGEABLE_PROVENANCE,
    FAILURE_IS_RECEIPTED_BUT_NOT_PROMOTED_TO_REFERENCE_RUN,
    NO_RUN_REPORT_WITHOUT_BOUND_EXECUTION,
    ONLY_EXECUTION_AUTHORITY_ISSUES_EXECUTION_RECEIPTS,
    RECEIPT_ISSUANCE_IS_KEYED_NOT_MERELY_SEALED,
    STATIC_IMPORT_AUDIT_IS_NOT_PROCESS_ISOLATION,
)

__all__ = [
    "AN_IN_PROCESS_SEAL_IS_NOT_UNFORGEABLE_PROVENANCE",
    "A_HARNESS_IS_NOT_AN_EXECUTION_AUTHORITY",
    "A_TIMEOUT_IS_NAMED_NOT_FOLDED_INTO_A_NONZERO_EXIT",
    "A_WIRE_VALUE_IS_REFUSED_NOT_COERCED",
    "CONFIGURATION_IS_EXECUTED_NOT_ONLY_IDENTIFIED",
    "EVALUATION_BOUNDARY_IS_NOT_THE_EXECUTION_MECHANISM",
    "EXECUTED_READER_IDENTITY_EQUALS_FROZEN_READER_IDENTITY",
    "EXECUTION_LAWS",
    "FAILURE_IS_RECEIPTED_BUT_NOT_PROMOTED_TO_REFERENCE_RUN",
    "IMPLEMENTATION_CHANGED_DURING_EXECUTION_MEANS_NO_REFERENCE_RUN",
    "MEASURED_BYTES_ARE_EXECUTED_BYTES",
    "NO_COMPARISON_BEFORE_BOUND_EXECUTION",
    "NO_RUN_REPORT_WITHOUT_BOUND_EXECUTION",
    "ONLY_EXECUTION_AUTHORITY_ISSUES_EXECUTION_RECEIPTS",
    "RECEIPT_ISSUANCE_IS_KEYED_NOT_MERELY_SEALED",
    "SEPARATE_PROCESS_IS_NOT_A_SANDBOX",
    "STATIC_IMPORT_AUDIT_IS_NOT_PROCESS_ISOLATION",
    "ExecutionError",
]


class ExecutionError(ValueError):
    """رفضٌ بنيويٌّ مُسمًّى في طبقة التنفيذ؛ لا حملَ على أقرب حالة."""


SEPARATE_PROCESS_IS_NOT_A_SANDBOX: Final[str] = (
    "SeparateProcess != Sandbox: عمليّةٌ منفصلةٌ ببيئةٍ مُقلَّمةٍ ومساحةِ عملٍ "
    "مؤقّتةٍ خارج الشجرة تُضيّق الطريقَ ولا تُثبِت حبسًا؛ فلا `seccomp` ولا قطعَ "
    "شبكةٍ ولا حبسَ نظام ملفّاتٍ في هذا الطور، ومن سمّاها حبسًا ادّعى ما لم يُبنَ"
)

EVALUATION_BOUNDARY_IS_NOT_THE_EXECUTION_MECHANISM: Final[str] = (
    "EvaluationBoundary != ExecutionMechanism: حدُّ التقييم أنواعٌ وعقودٌ "
    "وبصماتٌ لا تُشغِّل عمليّةً ولا تفتح ملفًّا، وآليّةُ التنفيذ حزمةٌ فوقه "
    "تستورده ولا يستوردها؛ فمن أضعف تدقيقَ الطبقة النقيّة ثمّ قال إنّه كما كان "
    "ادّعى عزلًا لم يَعُد قائمًا"
)

MEASURED_BYTES_ARE_EXECUTED_BYTES: Final[str] = (
    "MeasuredBytesAreExecutedBytes: لا يكفي قياسُ ملفٍّ ثمّ تشغيلُ مساره، فبينهما "
    "لحظةٌ يتغيّر فيها؛ إنّما تُنسَخ البايتاتُ المقيسةُ نفسُها إلى مساحة التنفيذ "
    "وتُشغَّل، فما قيس هو ما نُفِّذ"
)

EXECUTED_READER_IDENTITY_EQUALS_FROZEN_READER_IDENTITY: Final[str] = (
    "ExecutedReaderIdentity == FrozenReaderIdentity: تُعاد مكوّناتُ الهويّة "
    "الأربعةُ قياسًا من الصفر قبل التشغيل — بايتاتُ التنفيذ، والإعداد، وحدُّ "
    "الاعتماد المُعاد فحصُه، وإصدارُ الواجهة — فإن لم تُركَّب بصمةً هي بصمةُ "
    "الهويّة المُجمَّدة فلا تشغيلَ يُنسَب إليها"
)

IMPLEMENTATION_CHANGED_DURING_EXECUTION_MEANS_NO_REFERENCE_RUN: Final[str] = (
    "ImplementationChangedDuringExecution -> NoReferenceRunReport: يُعاد قياسُ "
    "المصدر بعد انتهاء العمليّة؛ فإن اختلف عمّا قيس قبلها لم يُعرَف أيُّ البايتات "
    "أنتج المخرجات، فيُوصَل الحدثُ بإيصالٍ ولا يُرقّى إلى تشغيلٍ مرجعيّ"
)

CONFIGURATION_IS_EXECUTED_NOT_ONLY_IDENTIFIED: Final[str] = (
    "ConfigurationIsExecutedNotOnlyIdentified: إعدادٌ يدخل تركيبَ الهويّة ولا "
    "يبلغ نداءَ القارئ يُثبِت هويّةَ إعدادٍ لا تنفيذَه؛ فالإعدادُ الذي قيس هو "
    "بعينه الذي يعبُر مغلّفَ التنفيذ إلى القارئ، ويشهد المُشغِّلُ ببصمة ما "
    "استلمه فتُقارَن ببصمة ما كُتِب، والاختلافُ حالٌ مُسمّاةٌ لا ناتجٌ يُقرَأ"
)

A_WIRE_VALUE_IS_REFUSED_NOT_COERCED: Final[str] = (
    'AWireValueIsRefusedNotCoerced: `"false"` ليست `False`، و`None` ليست '
    '`"None"`، وعددٌ ليس مُعرِّفَ عضو؛ فالتطبيعُ المتسامح يُنتِج تقريرًا صادقَ '
    "الشكل كاذبَ المعنى، والقناةُ المغلقةُ ترفض النوعَ الخاطئ ولا تُحوِّله"
)

A_TIMEOUT_IS_NAMED_NOT_FOLDED_INTO_A_NONZERO_EXIT: Final[str] = (
    "ATimeoutIsNamedNotFoldedIntoANonzeroExit: تجاوزُ السقف الزمنيّ حدثٌ غيرُ "
    "الخروج برمزٍ غيرِ صفر، والقتلُ بإشارةٍ غيرُهما؛ فلكلٍّ حالُ خروجٍ مُسمّاة، "
    "ولا يُصطنَع رمزٌ حارسٌ يتصادم برمزِ عمليّةٍ قُتلت"
)

NO_COMPARISON_BEFORE_BOUND_EXECUTION: Final[str] = (
    "NoComparisonBeforeBoundExecution: لا مقارنةَ ولا سيطرةَ ولا `Ω_M` قبل أن "
    "تصير نسبةُ المخرجات إلى النظام حدثَ تنفيذٍ مُوثَّقًا؛ وهذا الطورُ يقف عند "
    "الإيصال، ولا يبني نظامًا ثانيًا ولا يُقارن"
)

EXECUTION_LAWS: Final[tuple[str, ...]] = (
    NO_RUN_REPORT_WITHOUT_BOUND_EXECUTION,
    A_HARNESS_IS_NOT_AN_EXECUTION_AUTHORITY,
    ONLY_EXECUTION_AUTHORITY_ISSUES_EXECUTION_RECEIPTS,
    RECEIPT_ISSUANCE_IS_KEYED_NOT_MERELY_SEALED,
    AN_IN_PROCESS_SEAL_IS_NOT_UNFORGEABLE_PROVENANCE,
    CONFIGURATION_IS_EXECUTED_NOT_ONLY_IDENTIFIED,
    A_WIRE_VALUE_IS_REFUSED_NOT_COERCED,
    A_TIMEOUT_IS_NAMED_NOT_FOLDED_INTO_A_NONZERO_EXIT,
    EXECUTED_READER_IDENTITY_EQUALS_FROZEN_READER_IDENTITY,
    MEASURED_BYTES_ARE_EXECUTED_BYTES,
    IMPLEMENTATION_CHANGED_DURING_EXECUTION_MEANS_NO_REFERENCE_RUN,
    FAILURE_IS_RECEIPTED_BUT_NOT_PROMOTED_TO_REFERENCE_RUN,
    EVALUATION_BOUNDARY_IS_NOT_THE_EXECUTION_MECHANISM,
    SEPARATE_PROCESS_IS_NOT_A_SANDBOX,
    STATIC_IMPORT_AUDIT_IS_NOT_PROCESS_ISOLATION,
    NO_COMPARISON_BEFORE_BOUND_EXECUTION,
)


def _refuse_a_duplicated_law() -> None:
    """ارفض عند الاستيراد قانونًا مُكرَّرًا أو فارغًا."""

    if len(set(EXECUTION_LAWS)) != len(EXECUTION_LAWS):
        raise ExecutionError("قانونٌ مُكرَّرٌ في مجموعة قوانين التنفيذ")
    for law in EXECUTION_LAWS:
        if not law.strip():
            raise ExecutionError("قانونٌ بلا نصّ")


_refuse_a_duplicated_law()
