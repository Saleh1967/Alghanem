"""تحضيرُ جولة تدقيقٍ ثانيةٍ لـhamil: أجناسٌ تُولَد مُعلَنةً، ولا تشغيلَ ههنا.

طبقاتٌ ثلاثٌ جديدةٌ على `main` في ذاك البرنامج لم تُدقَّق بعد: الوقفُ العثمانيّ،
وi3lal، وقوانينُ الحقل 112. وقالبُ `hamil_phase1_audit_deposit` قابلٌ للتوسيع
**جنسًا لا نسخًا**: فلا تُنسَخ بنيتُه ههنا ولا تُعاد فحوصُه، وإنّما تُعلَن
ثلاثةُ أجناسٍ جديدةٍ بمواليدها وشروط وقفها. ويفترق ههنا ثلاثةٌ كانت تُقرأ
واحدًا::

    APreparedAudit       != ARunAudit
    ABlockOnBytes        != ABlockOnASealNotYetDeclared
    AQuotedPreTestFigure != AMeasuredFigure

**أوّلًا: مُحضَّرٌ لا مُشغَّل، والتحضيرُ لا يتنكّر تدقيقًا وقع.** ليس في هذه
الوحدة دالّةٌ تقرأ بايتةً ولا تُخرِج رقمًا مقيسًا؛ و`was_run` صفةٌ مُشتَقّةٌ
`False` في كلّ مولودٍ ما دام شرطُ وقفه قائمًا. فمن قرأ هذا الملفَّ تدقيقًا
فقد قرأ استعدادًا حكمًا (`A_PREPARED_AUDIT_IS_NOT_A_RUN_AUDIT`).

**وثانيًا: الوقفُ يُسمّى بما يَقف عليه.** طبقتا الوقف والحقل 112 موقوفتان على
**بايتاتٍ لم تُودَع ههنا**، وi3lal موقوفةٌ على **ختمٍ لم يُعلَن بعدُ**
(تفرُّعُ QAC معلَّق). وهما وقفان مختلفان: الأوّلُ يرفعه إيداعٌ عبر البوّابة،
والثاني لا يرفعه إيداعٌ حتى يُعلَن ختمٌ يُطابَق عليه. فلا يُجمَعان تحت اسمٍ
واحدٍ (`A_BLOCK_ON_BYTES_IS_NOT_A_BLOCK_ON_AN_UNDECLARED_SEAL`).

**وثالثًا: أرقامُ ما قبل الاختبار واردةٌ تُسمّى واردة.** 99.03% بـ754 غيرِ
مُواءَم، و86.6% لـ`L0` المُعلَنِ قبل الاختبار — كلُّها
`QUOTED_INCOMING_NOT_REPRODUCED` بمصطلح `audit_corpus_deposit`: دخلت من
إعلانهم لا من قرصنا، فلا تُقرأ مقيسةً ولا يُبنى عليها. وإعلانُ رقمٍ قبل
الاختبار فضيلةٌ في مَن أعلنه، ولا يجعله عندنا مقيسًا
(`A_PRE_TEST_DECLARATION_IS_NOT_A_MEASUREMENT_HERE`).

**ورابعًا: التدقيقُ اتّجاهٌ واحد.** لا تكتب هذه الوحدةُ في ذاك المستودع شيئًا،
ولا تقترح فيه تعديلًا؛ والردُّ على ما يُسجَّل من عنده هو.

**ولا سلطةَ لهذه الوحدة**: لا ولادةَ نموذجٍ فيها — و«المولود» ههنا مولودُ
`AuditGenus` لا مولودُ `G0` — ولا حكمَ ولادة، ولا تجميدَ `E0`، ولا تستورد من
`kernel/` ولا من `program/`.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from .audit_corpus_deposit import (
    THE_AUDIT_CORPUS,
    DepositedFigure,
    FigureProvenance,
)

__all__ = [
    "A_BLOCK_ON_BYTES_IS_NOT_A_BLOCK_ON_AN_UNDECLARED_SEAL",
    "A_PREPARED_AUDIT_IS_NOT_A_RUN_AUDIT",
    "A_PRE_TEST_DECLARATION_IS_NOT_A_MEASUREMENT_HERE",
    "ROUND_TWO_NAMED_RESIDUALS",
    "THE_CARRIER_STATE_BIRTH_WAITING_CONDITION",
    "THE_ROUND_TWO_BIRTHS",
    "AuditGenus",
    "BlockingKind",
    "DeclaredGenusBirth",
    "RoundTwoError",
    "WaitingCondition",
]


class RoundTwoError(ValueError):
    """رُفض مدخلٌ خارج مفردات هذا التحضير؛ ولا يُحمَل على أقرب حالة."""


class AuditGenus(Enum):
    """أجناسُ التدقيق الثلاثةُ الجديدة، مواليدَ مُعلَنةً لا نسخًا للقالب."""

    UTHMANI_WAQF_LAYER = "طبقةُ_الوقف_العثمانيّ"
    ILAL_LAYER = "طبقةُ_الإعلال"
    FIELD_112_LAWS = "قوانينُ_الحقل_112"


class BlockingKind(Enum):
    """نوعُ الوقف؛ وهو يُسمّى بما يَقف عليه لا بتاريخ وقوفه."""

    BYTES_NOT_DEPOSITED_HERE = "بايتاتٌ_لم_تُودَع_ههنا"
    SEAL_NOT_YET_DECLARED = "ختمٌ_لم_يُعلَن_بعدُ"


def _require_text(value: str, what: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise RoundTwoError(f"{what} لا يكون فارغًا.")


@dataclass(frozen=True, slots=True)
class DeclaredGenusBirth:
    """مولودُ جنسٍ مُعلَنٌ: ختمُه إن أُعلِن، وأرقامُه الواردة، وشرطُ وقفه."""

    genus: AuditGenus
    seal: str | None
    blocking: BlockingKind
    what_would_lift_it: str
    declared_figures: tuple[DepositedFigure, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.genus, AuditGenus):
            raise RoundTwoError("جنسُ المولود عضوٌ في `AuditGenus`.")
        if not isinstance(self.blocking, BlockingKind):
            raise RoundTwoError("نوعُ الوقف عضوٌ في `BlockingKind`.")
        _require_text(self.what_would_lift_it, "ما يرفع الوقف")
        if self.seal is not None:
            _require_text(self.seal, "ختمُ الطبقة")
        if (self.seal is None) != (self.blocking is BlockingKind.SEAL_NOT_YET_DECLARED):
            raise RoundTwoError(
                "الوقفُ على ختمٍ غيرِ مُعلَنٍ يلزمه ختمٌ خالٍ، والعكسُ بالعكس؛ "
                "ولا يُسمّى وقفُ بايتاتٍ وقفَ ختم."
            )
        for figure in self.declared_figures:
            if figure.is_generated:
                raise RoundTwoError(
                    "رقمُ ما قبل الاختبار واردٌ من إعلانهم لا مولَّدٌ من قرصنا؛ "
                    "فلا يُوسَم مولَّدًا ههنا."
                )

    @property
    def was_run(self) -> bool:
        """`False` بالبنية: هذا تحضيرٌ، ولا دالّةَ ههنا تُشغِّل شيئًا."""

        return False

    @property
    def bytes_would_suffice(self) -> bool:
        """أيكفي إيداعُ بايتاتٍ لرفع وقفه؟ مُشتَقٌّ من نوع الوقف لا مكتوب.

        و`False` حيث الوقفُ على ختمٍ لم يُعلَن: بايتاتٌ بلا ختمٍ تُطابَق عليه
        وديعةٌ بلا باب، فلا تُقرأ منها أرقام.
        """

        return self.blocking is BlockingKind.BYTES_NOT_DEPOSITED_HERE


THE_ROUND_TWO_BIRTHS: Final[tuple[DeclaredGenusBirth, ...]] = (
    DeclaredGenusBirth(
        genus=AuditGenus.UTHMANI_WAQF_LAYER,
        seal="16d65358",
        blocking=BlockingKind.BYTES_NOT_DEPOSITED_HERE,
        what_would_lift_it=(
            "إيداعُ بايتات طبقة الوقف العثمانيّ عبر بوّابة الاستقبال بختمها "
            "المُعلَن، كما أُودِعت مدوّنةُ التدقيق"
        ),
        declared_figures=(
            DepositedFigure(
                name="نسبةُ المواءمة المُعلَنة",
                value="99.03%",
                provenance=FigureProvenance.QUOTED_INCOMING_NOT_REPRODUCED,
            ),
            DepositedFigure(
                name="غيرُ المُواءَم المُعلَن",
                value="754",
                provenance=FigureProvenance.QUOTED_INCOMING_NOT_REPRODUCED,
            ),
        ),
    ),
    DeclaredGenusBirth(
        genus=AuditGenus.ILAL_LAYER,
        seal=None,
        blocking=BlockingKind.SEAL_NOT_YET_DECLARED,
        what_would_lift_it=(
            "إعلانُ ختمِ تفرُّع QAC — وهو معلَّقٌ عندهم — ليُطابَق عليه قبل أيّ "
            "قراءة؛ ولا يرفع هذا الوقفَ إيداعُ بايتاتٍ بلا ختمٍ تُطابَق عليه"
        ),
        declared_figures=(
            DepositedFigure(
                name="`L0` المُعلَنُ قبل الاختبار",
                value="86.6%",
                provenance=FigureProvenance.QUOTED_INCOMING_NOT_REPRODUCED,
            ),
        ),
    ),
    DeclaredGenusBirth(
        genus=AuditGenus.FIELD_112_LAWS,
        seal=None,
        blocking=BlockingKind.SEAL_NOT_YET_DECLARED,
        what_would_lift_it=(
            "إعلانُ ختمِ حارسَي التيار في الحقل 112 ثمّ إيداعُ بايتاتهما؛ "
            "والحارسان مذكوران بلا ختمٍ يُطابَق عليه اليوم"
        ),
        declared_figures=(
            DepositedFigure(
                name="حارسا التيار المُعلَنان",
                value="2",
                provenance=FigureProvenance.QUOTED_INCOMING_NOT_REPRODUCED,
            ),
        ),
    ),
)
"""الأجناسُ الثلاثةُ مواليدَ مُعلَنة: لكلٍّ ختمُه أو خلوُّه، ووقفُه، ورافعُه."""


@dataclass(frozen=True, slots=True)
class WaitingCondition:
    """شرطٌ انتظاريٌّ مُسجَّلٌ قبل تشغيل تجربته، لا بعد رؤية مخرجها."""

    subject: str
    the_condition: str
    what_discharged_it: str
    opens_where: str

    def __post_init__(self) -> None:
        _require_text(self.subject, "موضوعُ الشرط")
        _require_text(self.the_condition, "نصُّ الشرط")
        _require_text(self.what_discharged_it, "ما أنهى الانتظار")
        _require_text(self.opens_where, "موضعُ الفتح")

    @property
    def is_run_here(self) -> bool:
        """`False` بالبنية: التسجيلُ المسبق ليس تشغيلًا، وموضعُ التشغيل غيرُه."""

        return False


THE_CARRIER_STATE_BIRTH_WAITING_CONDITION: Final[WaitingCondition] = WaitingCondition(
    subject="تجربةُ ولادة حامل–حالةٍ كتابيّ",
    the_condition=(
        "عُلِّقت صراحةً بشرطَين: دمجُ بوّابتَي الإسناد والإغلاق والتحقّقُ منهما، "
        "ونزولُ بايتاتٍ جديدةٍ يُقاس عليها"
    ),
    what_discharged_it=(
        "دُمِجت البوّابتان، ثمّ نزلت بايتاتُ مدوّنة التدقيق عبر بوّابة "
        "الاستقبال بختمها ودورها المُعلَنَين"
    ),
    opens_where=(
        "طلبٌ مستقلٌّ بعد التحقّق من هذا الإيداع؛ ولا تُشغَّل ههنا، وهذا "
        "تسجيلُ شرطها مسبقًا كما أُودِع شرطُ الطبقة الرابعة قبل تشغيلها"
    ),
)
"""تسجيلٌ مسبقٌ لشرطٍ انتظاريٍّ انقضى، والتشغيلُ مؤجَّلٌ إلى طلبه المستقلّ."""


A_PREPARED_AUDIT_IS_NOT_A_RUN_AUDIT: Final[str] = (
    "A_PREPARED_AUDIT_IS_NOT_A_RUN_AUDIT: هذه الوحدةُ تُعلِن أجناسًا وتصف "
    "شروطَ وقفها، ولا تقرأ بايتةً ولا تُخرِج رقمًا مقيسًا؛ و`was_run` `False` "
    "بالبنية في كلّ مولودٍ منها. فالاستعدادُ للتدقيق لا يُقرأ تدقيقًا وقع"
)

A_BLOCK_ON_BYTES_IS_NOT_A_BLOCK_ON_AN_UNDECLARED_SEAL: Final[str] = (
    "A_BLOCK_ON_BYTES_IS_NOT_A_BLOCK_ON_AN_UNDECLARED_SEAL: طبقةُ الوقف "
    "موقوفةٌ على بايتاتٍ يرفعها إيداعٌ عبر البوّابة بختمها المُعلَن "
    "`16d65358`؛ وi3lal وقوانينُ الحقل 112 موقوفةٌ على ختمٍ **لم يُعلَن**، "
    "فلا يرفع وقفَها إيداعُ بايتاتٍ بلا ختمٍ تُطابَق عليه. والوقفان يُسمَّيان "
    "ولا يُجمَعان"
)

A_PRE_TEST_DECLARATION_IS_NOT_A_MEASUREMENT_HERE: Final[str] = (
    "A_PRE_TEST_DECLARATION_IS_NOT_A_MEASUREMENT_HERE: 99.03% و754 و86.6% "
    "أرقامٌ أُعلِنت عندهم قبل الاختبار، ودخلت ههنا "
    "`QUOTED_INCOMING_NOT_REPRODUCED`؛ وإعلانُ الرقم قبل اختباره فضيلةٌ في "
    "مُعلِنه ولا يجعله عندنا مقيسًا، ولا يُبنى عليه حتى يُولَّد من قرصٍ"
)

ROUND_TWO_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "A_PREPARED_AUDIT_IS_NOT_A_RUN_AUDIT": A_PREPARED_AUDIT_IS_NOT_A_RUN_AUDIT,
    "A_BLOCK_ON_BYTES_IS_NOT_A_BLOCK_ON_AN_UNDECLARED_SEAL": (
        A_BLOCK_ON_BYTES_IS_NOT_A_BLOCK_ON_AN_UNDECLARED_SEAL
    ),
    "A_PRE_TEST_DECLARATION_IS_NOT_A_MEASUREMENT_HERE": (
        A_PRE_TEST_DECLARATION_IS_NOT_A_MEASUREMENT_HERE
    ),
}


def _verify_every_genus_has_exactly_one_birth() -> None:
    """مبرهنة: كلُّ جنسٍ مُسمًّى له مولودٌ واحدٌ، ولا مولودَ بلا جنسٍ مُعلَن."""

    born = [birth.genus for birth in THE_ROUND_TWO_BIRTHS]
    if sorted(genus.value for genus in set(born)) != sorted(
        genus.value for genus in AuditGenus
    ):
        raise RuntimeError("a declared audit genus has no birth here")
    if len(born) != len(set(born)):
        raise RuntimeError("a genus is born twice")


def _verify_nothing_here_declares_itself_run() -> None:
    """مبرهنة: لا مولودَ يدّعي تشغيلًا، ولا شرطَ يدّعي أنّه شُغِّل ههنا."""

    for birth in THE_ROUND_TWO_BIRTHS:
        if birth.was_run:
            raise RuntimeError("a prepared genus declares itself run")
    if THE_CARRIER_STATE_BIRTH_WAITING_CONDITION.is_run_here:
        raise RuntimeError("a preregistered condition declares itself run here")


def _verify_no_birth_carries_a_verdict_field() -> None:
    """مبرهنة: لا حقلَ حكمٍ ولا نتيجةٍ في أنواع هذا التحضير."""

    for _dataclass in (DeclaredGenusBirth, WaitingCondition):
        for _field in fields(_dataclass):
            if any(token in _field.name for token in ("verdict", "result", "outcome")):
                raise RuntimeError("a prepared type carries a verdict field")


def _verify_the_audit_corpus_is_not_read_as_a_round_two_source() -> None:
    """مبرهنة: مدوّنةُ التدقيق المُودَعةُ ليست بايتاتِ أيٍّ من الطبقات الثلاث."""

    for birth in THE_ROUND_TWO_BIRTHS:
        if birth.seal is not None and THE_AUDIT_CORPUS.sha256_hex.startswith(
            birth.seal
        ):
            raise RuntimeError("a round-two layer is confused with the audit corpus")


_verify_every_genus_has_exactly_one_birth()
_verify_nothing_here_declares_itself_run()
_verify_no_birth_carries_a_verdict_field()
_verify_the_audit_corpus_is_not_read_as_a_round_two_source()
