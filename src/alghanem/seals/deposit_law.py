"""قانونُ الوديعة: لا وديعةَ تُقبَل بلا فاتورةٍ سالبةٍ وحارسِ انحلال.

كان المُخرَجُ يُعرَض فيُقرَأ حُجّةً: عدّادٌ يرتفع، وجدولٌ يمتلئ، ووديعةٌ
«تُحسِّن» — بلا ثمنٍ مقرونٍ بها. والشَّرِهُ يرفع العدّادَ زورًا: يَزيد وصفَه
حتى يبتلع الشاهدَ فيبدو رابحًا، وإنّما دفع من وصفِه أكثرَ ممّا ربح من شاهدِه.
فالعرضُ بلا فاتورةٍ عرضٌ بلا حارس (`AN_EXHIBIT_WITHOUT_A_PRICE_IS_NOT_EVIDENCE`).

والفاتورةُ ههنا شيءٌ واحدٌ مُعرَّف: **الكلفةُ بعدُ ناقصَ الكلفةِ قبلُ على
نطاقٍ واحدٍ بعينه**. فإن كان الفارقُ سالبًا فقد دفعت الوديعةُ ثمنَ نفسِها،
وإن كان صفرًا أو موجبًا فهي زيادةُ وصفٍ لا كسب. وتحمل الفاتورةُ نطاقَها في
حقلٍ واحدٍ **عمدًا**: فارقٌ بين نطاقين ليس فارقًا، بل مقابلةُ عالمين
(`A_DELTA_ACROSS_TWO_SCOPES_IS_NOT_A_DELTA`).

ولا تكفي الفاتورة وحدَها. فأرخصُ طرق الربح أن يُضيَّق ما تُحاسَب عليه: تُسقِط
الوديعةُ شواهدَ من تغطيتها فتَرخُص، ويُقرَأ نقصُ الحِمل كسبًا. فحارسُ
الانحلال شرطٌ ثانٍ لا بديل: **ألّا تقلَّ الشواهدُ المُغطّاةُ بعدُ عمّا كانت
قبلُ**؛ فما رَبِح بإسقاط شاهدٍ فقد انحلّ ولم يربح
(`A_GAIN_BOUGHT_BY_DROPPING_EVIDENCE_IS_DECAY_NOT_GAIN`).

والشرطُ الثالث يصل هذا القانونَ بسجلّ الأختام: كلُّ رقمٍ تُنتجه وديعةٌ مقبولةٌ
يدخل السجلَّ بختمٍ له مولِّدٌ حيّ من يومه الأوّل، فلا يولد عندنا مجمَّدٌ قطّ
(`A_DEPOSIT_THAT_BRINGS_NO_LIVE_SEAL_IS_NOT_ADMITTED`).

وهذه الوحدةُ **مصادِقٌ لا محرّك**: لا تقيس نصًّا ولا تدّعي لغةً؛ وإنّما تقرأ
فاتورةً مُقدَّمةً وتحكم عليها بشرطين معلنين قبل العرض. وحكمُها **مشتقٌّ من
حقولها لا مكتوبٌ في حقل**: ليس ههنا خانةُ «مقبول» تُملأ باليد.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

__all__ = [
    "AN_EXHIBIT_WITHOUT_A_PRICE_IS_NOT_EVIDENCE",
    "A_DELTA_ACROSS_TWO_SCOPES_IS_NOT_A_DELTA",
    "A_DEPOSIT_THAT_BRINGS_NO_LIVE_SEAL_IS_NOT_ADMITTED",
    "A_GAIN_BOUGHT_BY_DROPPING_EVIDENCE_IS_DECAY_NOT_GAIN",
    "DepositLawError",
    "DepositRuling",
    "Invoice",
    "rule_on_deposit",
]


class DepositLawError(Exception):
    """رفضٌ مُسمّى في قانون الوديعة؛ ولا يُبتلَع خللٌ ههنا بصمت."""


AN_EXHIBIT_WITHOUT_A_PRICE_IS_NOT_EVIDENCE: Final[str] = (
    "AN_EXHIBIT_WITHOUT_A_PRICE_IS_NOT_EVIDENCE: مُخرَجٌ يُعرَض بلا فاتورةٍ "
    "مقرونةٍ به عرضٌ لا حُجّة؛ والعدّادُ يرتفع بالشَّرَه كما يرتفع بالكسب."
)

A_GAIN_BOUGHT_BY_DROPPING_EVIDENCE_IS_DECAY_NOT_GAIN: Final[str] = (
    "A_GAIN_BOUGHT_BY_DROPPING_EVIDENCE_IS_DECAY_NOT_GAIN: ربحٌ اشتُري "
    "بإسقاط شاهدٍ من التغطية انحلالٌ لا كسب؛ ورخصُ الوصف حينئذٍ رخصُ حِمل."
)

A_DELTA_ACROSS_TWO_SCOPES_IS_NOT_A_DELTA: Final[str] = (
    "A_DELTA_ACROSS_TWO_SCOPES_IS_NOT_A_DELTA: فارقٌ بين كلفتين على نطاقين "
    "مختلفين مقابلةُ عالمين لا فارقُ كلفة؛ فالفاتورةُ تحمل نطاقًا واحدًا."
)

A_DEPOSIT_THAT_BRINGS_NO_LIVE_SEAL_IS_NOT_ADMITTED: Final[str] = (
    "A_DEPOSIT_THAT_BRINGS_NO_LIVE_SEAL_IS_NOT_ADMITTED: وديعةٌ تُنتج رقمًا "
    "بلا ختمٍ له مولِّدٌ حيّ تُدخِل مجمَّدًا جديدًا؛ والقانونُ يأبى ولادةَ قبر."
)


@dataclass(frozen=True)
class Invoice:
    """فاتورةُ وديعة: كلفتان وتغطيتان على **نطاقٍ واحدٍ** مُسمًّى.

    والنطاقُ حقلٌ واحدٌ لا حقلان، كيلا يُطرَح رقمُ عالمٍ من رقمِ عالمٍ آخر
    فيُقرَأ الفرقُ كسبًا (`A_DELTA_ACROSS_TWO_SCOPES_IS_NOT_A_DELTA`).
    """

    deposit: str
    scope: str
    units: str
    cost_before: float
    cost_after: float
    covered_before: int
    covered_after: int

    def __post_init__(self) -> None:
        for name in ("deposit", "scope", "units"):
            if not str(getattr(self, name)).strip():
                raise DepositLawError(f"فاتورةٌ بلا «{name}» لا تُقرأ.")
        if self.cost_before < 0.0 or self.cost_after < 0.0:
            raise DepositLawError("كلفةٌ سالبةٌ لا تُقاس؛ والكلفةُ طولُ وصفٍ لا ربح.")
        if self.covered_before < 0 or self.covered_after < 0:
            raise DepositLawError("تغطيةٌ سالبةٌ محال.")
        if self.covered_before < 1:
            raise DepositLawError(
                "فاتورةٌ على تغطيةٍ خاويةٍ قبلُ لا تُحاسِب شيئًا: "
                f"{A_GAIN_BOUGHT_BY_DROPPING_EVIDENCE_IS_DECAY_NOT_GAIN}"
            )

    @property
    def delta(self) -> float:
        """Δ = الكلفةُ بعدُ ناقصَ الكلفةِ قبلُ؛ والسالبُ وحدَه دفعٌ."""

        return self.cost_after - self.cost_before

    @property
    def pays_for_itself(self) -> bool:
        """أدفعت الوديعةُ ثمنَ نفسِها؟ Δ<0 وحدَها، ولا يُقبَل الصفر."""

        return self.delta < 0.0

    @property
    def coverage_delta(self) -> int:
        """فارقُ الشواهد المُغطّاة؛ والنقصُ ههنا انحلالٌ لا اقتصاد."""

        return self.covered_after - self.covered_before

    @property
    def decays(self) -> bool:
        """أاشتُري الرخصُ بإسقاط شاهد؟ فذاك انحلالٌ يُسمّى."""

        return self.coverage_delta < 0


@dataclass(frozen=True)
class DepositRuling:
    """حكمُ القانون على وديعة: رفضاتٌ مسمّاةٌ، والقبولُ عدمُها لا حقلٌ يُملأ."""

    invoice: Invoice
    refusals: tuple[str, ...]

    @property
    def is_admitted(self) -> bool:
        """القبولُ **مشتقٌّ** من خلوّ الرفضات، ولا يُكتَب في حقلٍ باليد."""

        return not self.refusals


def rule_on_deposit(invoice: Invoice, *, brings_a_live_seal: bool) -> DepositRuling:
    """يحكم على وديعةٍ بشرطيها المعلنين قبل العرض، ويُسمّي كلَّ رفض.

    ولا شرطَ ثالثًا مستورًا: ما لم يُذكَر ههنا لا يُحتجّ به، وما ذُكِر لا
    يُتجاوَز عنه لقربٍ ولا لحسن عرض.
    """

    refusals: list[str] = []
    if not invoice.pays_for_itself:
        refusals.append(AN_EXHIBIT_WITHOUT_A_PRICE_IS_NOT_EVIDENCE)
    if invoice.decays:
        refusals.append(A_GAIN_BOUGHT_BY_DROPPING_EVIDENCE_IS_DECAY_NOT_GAIN)
    if not brings_a_live_seal:
        refusals.append(A_DEPOSIT_THAT_BRINGS_NO_LIVE_SEAL_IS_NOT_ADMITTED)
    return DepositRuling(invoice=invoice, refusals=tuple(refusals))
