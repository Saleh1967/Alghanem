"""`G0.EVAL-0.LAWS`: قوانينُ حدِّ التقييم، مُجمَّدةً قبل أيّ تشغيلٍ ونتيجة.

هذه الطبقةُ تبني آلةَ امتحانٍ قابلةً لإعادة التدقيق، ولا تُصدِر حكمًا. سقفُها
`GoldRevealRecord`: إثباتُ أنّ الجوابَ الملتزَم به فُتِح بعد تجميد كلِّ ما يجب
تجميدُه. وليس فيها مقارنةٌ ولا سيطرةٌ ولا `Ω_M`، ولا دالّةَ حكمٍ أصلًا.

    NoEvaluationVerdictBefore:
          FrozenContract
        ∧ FrozenSystemIdentity
        ∧ FrozenProtocol
        ∧ BoundRequest
        ∧ FrozenFirstRunReports
        ∧ ValidGoldReveal

وحدُّ القارئ هنا حدُّ مصدرٍ مُصرَّح لا حبسُ عمليّة، ويُسجَّل ذلك تصريحًا:
`StaticImportAudit != ProcessIsolation`.
"""

from __future__ import annotations

from enum import Enum
from typing import Final

from ..import_boundary import STATIC_IMPORT_AUDIT_IS_NOT_PROCESS_ISOLATION
from ..prior_fiber import (
    DIGEST_ONLY_IS_NOT_CRYPTOGRAPHICALLY_HIDDEN_GOLD,
    FROZEN_CONTRACT_BEFORE_READERS,
    NO_SYSTEM_DEFINES_THE_CONTRACT_IT_IS_READ_BY,
    OBSERVED_DOMINANCE_IS_BOUNDED_BY_ITS_FROZEN_DOMAIN,
)

__all__ = [
    "A_FIRST_RUN_HAPPENS_ONCE",
    "A_RESIDUAL_IS_NAMED_NOT_STRINGLY",
    "A_REVEAL_RECORD_IS_NOT_A_VERDICT",
    "A_HARNESS_IS_NOT_AN_EXECUTION_AUTHORITY",
    "A_SERIALIZED_CONTRACT_IS_WHAT_THE_READER_RECEIVES",
    "A_SYSTEM_NAME_IS_NOT_A_SYSTEM_IDENTITY",
    "DIGEST_ONLY_IS_NOT_CRYPTOGRAPHICALLY_HIDDEN_GOLD",
    "EVALUATION_LAWS",
    "FAILURE_IS_RECEIPTED_BUT_NOT_PROMOTED_TO_REFERENCE_RUN",
    "FROZEN_CONTRACT_BEFORE_READERS",
    "NO_EVALUATION_VERDICT_BEFORE",
    "NO_RUN_REPORT_WITHOUT_BOUND_EXECUTION",
    "NO_SYSTEM_DEFINES_THE_CONTRACT_IT_IS_READ_BY",
    "OBSERVED_DOMINANCE_IS_BOUNDED_BY_ITS_FROZEN_DOMAIN",
    "ONLY_EXECUTION_AUTHORITY_ISSUES_EXECUTION_RECEIPTS",
    "STATIC_IMPORT_AUDIT_IS_NOT_PROCESS_ISOLATION",
    "EvaluationError",
    "ProcessConfinementStanding",
]


class EvaluationError(ValueError):
    """رفضٌ بنيويٌّ مُسمًّى في طبقة التقييم؛ لا حملَ على أقرب حالة."""


class ProcessConfinementStanding(Enum):
    """حالُ حبس العمليّة؛ ويُسجَّل تأجيلُه تصريحًا لا يُدَّعى إنجازُه صمتًا."""

    DECLARED_DEFERRED = "declared_deferred"
    SEPARATE_PROCESS_DECLARED = "separate_process_declared"

    @property
    def is_proven(self) -> bool:
        """أمُثبَتٌ حبسُ العمليّة في هذا الطور؟ ولا عضوَ مُثبَتًا فيه بالبناء."""

        return False


A_SYSTEM_NAME_IS_NOT_A_SYSTEM_IDENTITY: Final[str] = (
    "ASystemNameIsNotASystemIdentity: اسمُ النظام نصٌّ ينتحله برنامجٌ آخر؛ "
    "وهويّتُه بصمةُ تنفيذه وإعداده وحدِّ اعتماده وإصدارِ واجهته معًا، وأيُّ بايتٍ "
    "يتغيّر في مصدر قارئٍ يُغيِّر هويّتَه"
)

A_SERIALIZED_CONTRACT_IS_WHAT_THE_READER_RECEIVES: Final[str] = (
    "ASerializedContractIsWhatTheReaderReceives: القارئُ يستلم بايتاتٍ قانونيّةً "
    "مُسلسَلة، لا كائنَ بايثون ولا مُحوِّلَ مجالٍ ولا مصدرَ الجواب؛ فمن سلّم "
    "كائنًا سلّم معه طريقًا إلى ما بناه"
)

A_FIRST_RUN_HAPPENS_ONCE: Final[str] = (
    "AFirstRunHappensOnce: التشغيلُ الأوّل بهويّة نظامٍ وطلبٍ بعينهما مرجعٌ لا "
    "يُستبدَل؛ وإعادةٌ مطابقةٌ تُسجَّل شاهدًا على الحتميّة، وإعادةٌ مختلفةٌ "
    "تُرفَض وتُسجَّل مخالفةً ولا تُطوى"
)

A_RESIDUAL_IS_NAMED_NOT_STRINGLY: Final[str] = (
    "AResidualIsNamedNotStringly: البقيّةُ عضوٌ مُسمًّى برمزٍ من مفردةٍ مغلقةٍ "
    "وسببٍ وشاهدٍ وصفةِ إعاقة، لا نصٌّ حرٌّ تتغيّر دلالتُه بين طورٍ وطور؛ "
    "وصفةُ الإعاقة تُسجَّل ولا يُبنى عليها حكمٌ في طورها"
)

A_REVEAL_RECORD_IS_NOT_A_VERDICT: Final[str] = (
    "ARevealRecordIsNotAVerdict: سجلُّ الفتح يُثبِت أنّ الالتزامَ فُتِح بعد "
    "تجميدٍ تامّ، ولا يقول أيُّ قارئٍ أصاب؛ فلا مقارنةَ في هذا الطور ولا حكمَ "
    "سيطرة"
)

NO_RUN_REPORT_WITHOUT_BOUND_EXECUTION: Final[str] = (
    "NoRunReportWithoutBoundExecution: تقريرُ التشغيل يُشتَقُّ من إيصالِ تنفيذٍ "
    "مربوطٍ صادرٍ عن سلطة التنفيذ، ولا يُكتَب بيدٍ؛ فحملُ التقريرِ بصمةَ هويّةٍ "
    "دعوى، وإثباتُ أنّ تلك البايتاتِ نفسَها شُغِّلت فأخرجت هذه البايتاتِ شهادة"
)

A_HARNESS_IS_NOT_AN_EXECUTION_AUTHORITY: Final[str] = (
    "AHarnessIsNotAnExecutionAuthority: من بنى المخرجاتِ في إطاره ثمّ نسبها إلى "
    "قارئٍ لم يُشغِّله فقد بنى دعوى لا شهادة؛ ولا تُنسَب مخرجاتٌ إلى هويّةٍ إلّا "
    "عبر سلطةِ تنفيذٍ قاست تلك الهويّةَ وشغّلت بايتاتِها"
)

ONLY_EXECUTION_AUTHORITY_ISSUES_EXECUTION_RECEIPTS: Final[str] = (
    "OnlyExecutionAuthorityIssuesExecutionReceipts: التجميدُ يمنع التعديلَ بعد "
    "الإنشاء ولا يمنع تزويرَ الإنشاء؛ فالإيصالُ لا يُبنى من الواجهة العامّة، "
    "ولا يصدُر إلّا عن سلطةِ تنفيذٍ تملك ختمَ إصداره"
)

FAILURE_IS_RECEIPTED_BUT_NOT_PROMOTED_TO_REFERENCE_RUN: Final[str] = (
    "FailureIsReceiptedButNotPromotedToReferenceRun: ما بدأ تنفيذُه يُوصَل به "
    "إيصالٌ يشهد بما جرى وإن فشل، فلا يُطوى حدث؛ ولا يُرقّى إيصالٌ غيرُ تامٍّ "
    "إلى تقريرِ تشغيلٍ مرجعيّ"
)

NO_EVALUATION_VERDICT_BEFORE: Final[str] = (
    "NoEvaluationVerdictBefore(FrozenContract ∧ FrozenSystemIdentity ∧ "
    "FrozenProtocol ∧ BoundRequest ∧ FrozenFirstRunReports ∧ ValidGoldReveal): "
    "ولا حكمَ في هذا الطور أصلًا، فالسقفُ سجلُّ فتحٍ مشروطٌ لا نتيجة"
)

EVALUATION_LAWS: Final[tuple[str, ...]] = (
    FROZEN_CONTRACT_BEFORE_READERS,
    DIGEST_ONLY_IS_NOT_CRYPTOGRAPHICALLY_HIDDEN_GOLD,
    A_SYSTEM_NAME_IS_NOT_A_SYSTEM_IDENTITY,
    A_SERIALIZED_CONTRACT_IS_WHAT_THE_READER_RECEIVES,
    STATIC_IMPORT_AUDIT_IS_NOT_PROCESS_ISOLATION,
    A_FIRST_RUN_HAPPENS_ONCE,
    A_RESIDUAL_IS_NAMED_NOT_STRINGLY,
    NO_SYSTEM_DEFINES_THE_CONTRACT_IT_IS_READ_BY,
    A_REVEAL_RECORD_IS_NOT_A_VERDICT,
    NO_RUN_REPORT_WITHOUT_BOUND_EXECUTION,
    A_HARNESS_IS_NOT_AN_EXECUTION_AUTHORITY,
    ONLY_EXECUTION_AUTHORITY_ISSUES_EXECUTION_RECEIPTS,
    FAILURE_IS_RECEIPTED_BUT_NOT_PROMOTED_TO_REFERENCE_RUN,
    NO_EVALUATION_VERDICT_BEFORE,
    OBSERVED_DOMINANCE_IS_BOUNDED_BY_ITS_FROZEN_DOMAIN,
)


def _refuse_a_duplicated_law() -> None:
    """ارفض عند الاستيراد قانونًا مُكرَّرًا أو فارغًا."""

    if len(set(EVALUATION_LAWS)) != len(EVALUATION_LAWS):
        raise EvaluationError("قانونٌ مُكرَّرٌ في مجموعة قوانين التقييم")
    for law in EVALUATION_LAWS:
        if not law.strip():
            raise EvaluationError("قانونٌ بلا نصّ")


_refuse_a_duplicated_law()
