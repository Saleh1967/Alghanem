"""G0.FLT-1: تجميدُ نصّ القانون المُقترَح حرفيًّا، وفاحصُ أمانةٍ يُقابله قبل التشغيل.

هذه الوحدةُ تُكتَب بعد أن أسقط `G0.FLT-0` تسجيلَه بانحراف نصّه المُبصَّم عن
النصّ الوارد في موضعٍ يقرّر شرطَ النجاح. والدرسُ المُستفاد ليس «نُحسن النقل»،
بل أن يكون **الفحصُ آليًّا وقبليًّا**: تُسمّى مواضعُ الترميز الحاسمة واحدًا
واحدًا، ويُشتَقّ حضورُها من النصّ المودَع نفسِه، ويُعرَض تقريرُ الأمانة قبل أن
توجد وحدةُ قراءةٍ واحدة.

**ولا وحدةَ قراءةٍ في هذا الإيداع** (`NoReadoutExistsForFLT1Yet`): هذا الفرع
يُودِع النصَّ والتسجيلَ فقط. ولا يجوز أن تُبنى القراءةُ في الإيداع نفسِه، لأنّ
شاهدَ الترتيب في `G0.FLT-0` كان صحيحًا وحدَه من بين ما صحّ، فيُحفَظ. ومَن أراد
أن يقرأ فليُقابل النصَّ المودَع بالنصّ الوارد أوّلًا، ثمّ يبني القراءةَ في
إيداعٍ تالٍ.

**والفحصُ يُخرِج تقريرًا لا يَعِد وعدًا** (`FidelityIsDerivedNotPromised`):
`derive_fidelity_report` تُعيد لكلّ موضعٍ مُسمّى هل هو حاضرٌ في النصّ المودَع،
فالموضعُ الغائبُ يُسقِط الوحدةَ عند الاستيراد ولا يمرّ تنسيقًا. وهذا هو عينُ
ما لم يكن موجودًا حين جُمِّد نصُّ `G0.FLT-0`.

**و`28×4` نتيجةٌ متنبَّأٌ بها لا مُدخَلٌ مفروض**
(`TwentyEightIsAPredictionNotAnInput`): النصُّ يجعل `C_0` حاصلَ قسمةٍ يُشتَقّ
أوّلًا، **ثمّ** يُختبَر عددُه. فمَن أدخل العددَ في التعريف اختبر تعريفَه لا
دعواه.

**والتسميةُ «مركزًا أعلى» مشروطةٌ بأربعةٍ قبلها**
(`AHigherCenterIsEarnedByFourConditions`): إعادةُ البناء، والأدنويّة، وامتناعُ
التجاوز، والإغلاق. وواحدٌ منها ساقطٌ يُسقِط الاسمَ كلَّه.

**ولا ولادةَ هنا ولا تجميدَ `E0`**: `FrozenText != EstablishedLaw`، ولا وحدةَ
في `kernel/` تقرأ هذه المخرجات.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from alghanem.canonical_content import canonical_bytes, canonical_digest

__all__ = [
    "AN_UNCHECKED_FROZEN_TEXT_IS_WHAT_FAILED_BEFORE_NOTE",
    "A_HIGHER_CENTER_IS_EARNED_BY_FOUR_CONDITIONS_NOTE",
    "FIDELITY_IS_DERIVED_NOT_PROMISED_NOTE",
    "FLT1_HYPOTHESIS_NAMED_RESIDUALS",
    "FLT1_HYPOTHESIS_TEXT",
    "FLT1_TEXT_DIGEST",
    "HIGHER_CENTER_CONDITIONS",
    "NO_READOUT_EXISTS_FOR_FLT1_YET_NOTE",
    "REQUIRED_NOTATION_SITES",
    "TWENTY_EIGHT_IS_A_PREDICTION_NOT_AN_INPUT_NOTE",
    "FidelityReport",
    "FidelitySiteReading",
    "FidelityStanding",
    "FLT1HypothesisError",
    "NotationSite",
    "derive_fidelity_report",
    "flt1_text_digest",
]


class FLT1HypothesisError(ValueError):
    """رفضٌ مُسمّى في وحدة نصّ G0.FLT-1؛ لا تصحيحَ صامتًا ولا تخطّي."""


FLT1_HYPOTHESIS_TEXT: Final[str] = r"""\boxed{
\text{Carrier}
\rightarrow
\text{Carrier/State Center}
\rightarrow
\text{Licensed Join}
\rightarrow
\text{Closure}
\rightarrow
\text{Higher Center}
}

وأقترح تجميده على شكل فرضيات منفصلة لا كقانون واحد ضخم:

H_1:
C_0=\operatorname{Quotient}(\widetilde C)
\quad\text{ثم يُختبر}\quad |C_0|=28

H_2:
V_0=\operatorname{Quotient}(\widetilde V)
\quad\text{ثم يُختبر}\quad
V_0=\{\َ,\ُ,\ِ,\ْ\}

ثم:

\boxed{
M_0=C_0\times V_0
}

لكن 28\times4 نتيجة متنبأ بها، لا مدخلًا مفروضًا.

ثم اختبار الولادة:

v\in\{\َ,\ُ,\ِ\}
\Longrightarrow
B(c,v)=CV

مقابل الضابط السلبي:

B(c,\ْ)\neq CV.

ثم اختبار السكون:

CV+(c,\ْ)\longrightarrow CVC

أي:

\boxed{
\text{الحركة تفتح، والسكون يغلق}
}

لا بوصفها تسمية نحوية، بل نتيجة يجب أن يعيدها المرمّز.

ثم يأتي القانون الأقوى:

M_1=
\operatorname{Close}
\bigl(
\operatorname{Join}(M_0^{(1)},\ldots,M_0^{(k)})
\bigr).

ويُسمح بتسمية M_1 «مركزًا أعلى» فقط إذا ثبتت أربعة شروط مسبقًا:

\boxed{
\text{Reconstruction}
\land
\text{Minimality}
\land
\text{NoBypass}
\land
\text{Closure}
}

أي يجب أن يستطيع المقطع إعادة وحداته الدنيا، وألا يعيده نموذج أضعف، وألا توجد طريقة تتجاوز الوصل المفترض، وأن يغلق كوحدة واحدة.

وأهم ضابط سلبي لـFLT-1:

\text{Carrier alone}

و:

\text{State alone}

و:

\text{unordered }(C,V)

يجب ألا تعطي النتيجة نفسها التي يعطيها:

(c,v)

المربوط ترخيصًا. فإذا أعاد نموذج من هذه النماذج المقطع بنفس الكفاءة، تسقط دعوى أن حامل/حالة هو المركز الأدنى.

إذًا التجربة القادمة ينبغي أن تكون:

\boxed{
\text{G0.FLT-1:
Does a licensed Carrier/State center generate syllabic closure
better than every weaker representation?}
}
"""  # noqa: E501


class FidelityStanding(Enum):
    """منزلةُ النصّ المودَع من النصّ الوارد؛ ثنائيّةٌ لأن الموضعَ إمّا حضر أو غاب."""

    ALL_REQUIRED_SITES_PRESENT = "كلُّ_المواضع_الحاسمة_حاضرةٌ_في_النصّ_المودَع"
    A_REQUIRED_SITE_IS_ABSENT = "موضعٌ_حاسمٌ_غائبٌ_فالتسجيلُ_باطلٌ_قبل_تشغيله"


@dataclass(frozen=True, slots=True)
class NotationSite:
    """موضعُ ترميزٍ حاسمٌ في النصّ الوارد، بما يقرّره وبما يسقط بسقوطه."""

    site_id: str
    literal: str
    what_it_decides: str
    what_its_absence_invalidates: str

    def __post_init__(self) -> None:
        for value, name in (
            (self.site_id, "مُعرِّفُ الموضع"),
            (self.literal, "حرفيّةُ الموضع"),
            (self.what_it_decides, "ما يقرّره الموضع"),
            (self.what_its_absence_invalidates, "ما يُبطله غيابُه"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise FLT1HypothesisError(
                    f"{name} نصٌّ غيرُ فارغ؛ وموضعٌ بلا حرفيّةٍ لا يُفحَص"
                )


REQUIRED_NOTATION_SITES: Final[tuple[NotationSite, ...]] = (
    NotationSite(
        site_id="the-law-chain",
        literal=r"\text{Carrier/State Center}",
        what_it_decides="أنّ المركزَ الأدنى حامل/حالةٌ لا حاملٌ وحدَه",
        what_its_absence_invalidates="سلسلةَ القانون كلَّها، فلا مركزَ يُختبَر",
    ),
    NotationSite(
        site_id="quotient-of-carriers",
        literal=r"C_0=\operatorname{Quotient}(\widetilde C)",
        what_it_decides="أنّ `C_0` حاصلُ قسمةٍ يُشتَقّ، لا قائمةٌ تُملى",
        what_its_absence_invalidates="`H_1` بتمامه، فيصير العددُ مُدخَلًا",
    ),
    NotationSite(
        site_id="the-predicted-count",
        literal=r"|C_0|=28",
        what_it_decides="أنّ العددَ يُختبَر **بعد** الاشتقاق لا قبله",
        what_its_absence_invalidates="التنبّؤَ نفسَه، فلا شيءَ يُكذَّب",
    ),
    NotationSite(
        site_id="quotient-of-states",
        literal=r"V_0=\operatorname{Quotient}(\widetilde V)",
        what_it_decides="أنّ `V_0` حاصلُ قسمةٍ كذلك",
        what_its_absence_invalidates="`H_2`، فتصير الحركاتُ مفروضةً",
    ),
    NotationSite(
        site_id="the-product-center",
        literal=r"M_0=C_0\times V_0",
        what_it_decides="أنّ المركزَ الأدنى جداءٌ متنبَّأٌ به",
        what_its_absence_invalidates="الرابطَ بين `H_1` و`H_2` والمركز",
    ),
    NotationSite(
        site_id="birth-under-a-vowel",
        literal=r"B(c,v)=CV",
        what_it_decides="ولادةَ المقطع تحت حركةٍ مفتِّحة",
        what_its_absence_invalidates="اختبارَ الولادة، فلا موجَبَ يُقاس",
    ),
    NotationSite(
        site_id="the-negative-control",
        literal=r"B(c,\ْ)\neq CV",
        what_it_decides="الضابطَ السلبيَّ للولادة: السكونُ لا يفتح",
        what_its_absence_invalidates="قدرةَ الاختبار على أن يفشل أصلًا",
    ),
    NotationSite(
        site_id="closure-by-sukun",
        literal=r"CV+(c,\ْ)\longrightarrow CVC",
        what_it_decides="أنّ السكونَ يُغلِق، نتيجةً يعيدها المرمِّز",
        what_its_absence_invalidates="اختبارَ الإغلاق",
    ),
    NotationSite(
        site_id="the-higher-center",
        literal=r"\operatorname{Join}(M_0^{(1)},\ldots,M_0^{(k)})",
        what_it_decides="أنّ المركزَ الأعلى إغلاقُ وصلٍ لمراكزَ دنيا",
        what_its_absence_invalidates="القانونَ الأقوى، وهو مقصدُ التجربة",
    ),
    NotationSite(
        site_id="the-four-conditions",
        literal=(
            r"\text{Reconstruction}"
            "\n"
            r"\land"
            "\n"
            r"\text{Minimality}"
            "\n"
            r"\land"
            "\n"
            r"\text{NoBypass}"
            "\n"
            r"\land"
            "\n"
            r"\text{Closure}"
        ),
        what_it_decides="شروطَ استحقاق اسم «مركزٍ أعلى»، مجتمعةً بالعطف",
        what_its_absence_invalidates="الاسمَ نفسَه، فيصير تسميةً بلا استحقاق",
    ),
    NotationSite(
        site_id="weaker-carrier-alone",
        literal=r"\text{Carrier alone}",
        what_it_decides="أوّلَ النماذج الأضعف",
        what_its_absence_invalidates="الضابطَ السلبيَّ الأهمّ للتجربة",
    ),
    NotationSite(
        site_id="weaker-state-alone",
        literal=r"\text{State alone}",
        what_it_decides="ثانيَ النماذج الأضعف",
        what_its_absence_invalidates="الضابطَ السلبيَّ الأهمّ للتجربة",
    ),
    NotationSite(
        site_id="weaker-unordered-pair",
        literal=r"\text{unordered }(C,V)",
        what_it_decides="ثالثَ النماذج الأضعف: أنّ الترتيبَ نفسَه مُختبَر",
        what_its_absence_invalidates="دعوى أنّ الربطَ المُرخَّص هو الفارق",
    ),
    NotationSite(
        site_id="the-question",
        literal=(
            r"\text{G0.FLT-1:"
            "\n"
            r"Does a licensed Carrier/State center generate syllabic closure"
            "\n"
            r"better than every weaker representation?}"
        ),
        what_it_decides="صياغةَ السؤال المُختبَر بحروفه",
        what_its_absence_invalidates="التجربةَ كلَّها، فلا سؤالَ مُجمَّد",
    ),
)

HIGHER_CENTER_CONDITIONS: Final[tuple[str, ...]] = (
    "Reconstruction",
    "Minimality",
    "NoBypass",
    "Closure",
)


@dataclass(frozen=True, slots=True)
class FidelitySiteReading:
    """قراءةُ موضعٍ واحد: حاضرٌ في النصّ المودَع أم غائب."""

    site_id: str
    is_present: bool
    what_it_decides: str
    what_its_absence_invalidates: str


@dataclass(frozen=True, slots=True)
class FidelityReport:
    """تقريرُ الأمانة كاملًا؛ يُعرَض قبل وجود أيّ قراءة."""

    standing: FidelityStanding
    sites: tuple[FidelitySiteReading, ...]
    absent_site_ids: tuple[str, ...]
    text_digest: str

    @property
    def is_fit_to_be_run(self) -> bool:
        """التسجيلُ صالحٌ للتشغيل متى حضرت المواضعُ الحاسمة كلُّها."""

        return self.standing is FidelityStanding.ALL_REQUIRED_SITES_PRESENT


def flt1_text_digest(text: str | None = None) -> str:
    """اشتقّ بصمةَ النصّ من بايتاته المعياريّة؛ ولا تُكتَب بجانبه ثابتًا."""

    text = FLT1_HYPOTHESIS_TEXT if text is None else text
    if not isinstance(text, str) or not text.strip():
        raise FLT1HypothesisError("النصُّ المُجمَّد نصٌّ غيرُ فارغ")
    return canonical_digest(canonical_bytes(text))


FLT1_TEXT_DIGEST: Final[str] = flt1_text_digest()


def derive_fidelity_report(text: str | None = None) -> FidelityReport:
    """اشتقّ حضورَ كلّ موضعٍ حاسمٍ من النصّ المودَع؛ ولا تُصرِّح بأمانةٍ منقولة."""

    text = FLT1_HYPOTHESIS_TEXT if text is None else text
    readings: list[FidelitySiteReading] = []
    absent: list[str] = []
    for site in REQUIRED_NOTATION_SITES:
        present = site.literal in text
        if not present:
            absent.append(site.site_id)
        readings.append(
            FidelitySiteReading(
                site_id=site.site_id,
                is_present=present,
                what_it_decides=site.what_it_decides,
                what_its_absence_invalidates=site.what_its_absence_invalidates,
            )
        )
    standing = (
        FidelityStanding.ALL_REQUIRED_SITES_PRESENT
        if not absent
        else FidelityStanding.A_REQUIRED_SITE_IS_ABSENT
    )
    return FidelityReport(
        standing=standing,
        sites=tuple(readings),
        absent_site_ids=tuple(absent),
        text_digest=flt1_text_digest(text),
    )


NO_READOUT_EXISTS_FOR_FLT1_YET_NOTE: Final[str] = (
    "NoReadoutExistsForFLT1Yet: هذا الإيداعُ نصٌّ وتسجيلٌ فقط؛ ولا تُبنى "
    "القراءةُ فيه، لأن شاهدَ الترتيب لا يُصنَع بعد أن تُرى النتيجة"
)

FIDELITY_IS_DERIVED_NOT_PROMISED_NOTE: Final[str] = (
    "FidelityIsDerivedNotPromised: أمانةُ النقل تُشتَقّ موضعًا بموضعٍ من النصّ "
    "المودَع، ويُعرَض تقريرُها قبل التشغيل؛ والوعدُ بالحرفيّة ليس فحصًا لها"
)

AN_UNCHECKED_FROZEN_TEXT_IS_WHAT_FAILED_BEFORE_NOTE: Final[str] = (
    "AnUncheckedFrozenTextIsWhatFailedBefore: سقط `G0.FLT-0` لأنّ نصَّه بُصِّم "
    "ولم يُقابَل بالوارد قبل تشغيله؛ فالمقابلةُ الآليّةُ القبليّة شرطُ دخولٍ "
    "لا حاشيةُ جودة"
)

TWENTY_EIGHT_IS_A_PREDICTION_NOT_AN_INPUT_NOTE: Final[str] = (
    "TwentyEightIsAPredictionNotAnInput: `C_0` يُشتَقّ حاصلَ قسمةٍ أوّلًا ثمّ "
    "يُختبَر عددُه؛ ومن أدخل العددَ في التعريف اختبر تعريفَه لا دعواه"
)

A_HIGHER_CENTER_IS_EARNED_BY_FOUR_CONDITIONS_NOTE: Final[str] = (
    "AHigherCenterIsEarnedByFourConditions: إعادةُ البناء، والأدنويّة، "
    "وامتناعُ التجاوز، والإغلاق، مجتمعةً؛ وساقطٌ منها يُسقِط الاسمَ لا يُخفِّفه"
)

FLT1_HYPOTHESIS_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    NO_READOUT_EXISTS_FOR_FLT1_YET_NOTE,
    FIDELITY_IS_DERIVED_NOT_PROMISED_NOTE,
    AN_UNCHECKED_FROZEN_TEXT_IS_WHAT_FAILED_BEFORE_NOTE,
    TWENTY_EIGHT_IS_A_PREDICTION_NOT_AN_INPUT_NOTE,
    A_HIGHER_CENTER_IS_EARNED_BY_FOUR_CONDITIONS_NOTE,
)


def _refuse_a_text_that_lost_a_required_site() -> None:
    report = derive_fidelity_report()
    if not report.is_fit_to_be_run:
        raise FLT1HypothesisError(
            "مواضعُ حاسمةٌ غائبةٌ من النصّ المودَع: "
            f"{'، '.join(report.absent_site_ids)}؛ وموضعٌ غائبٌ يُسقِط "
            "التسجيلَ قبل تشغيله ولا يمرّ تنسيقًا"
        )


def _refuse_a_duplicated_site() -> None:
    ids = [site.site_id for site in REQUIRED_NOTATION_SITES]
    if len(ids) != len(set(ids)):
        raise FLT1HypothesisError("موضعٌ مكرَّرٌ يُنقص العدَّ ويُقرأ تمامًا")


def _refuse_a_fifth_higher_center_condition() -> None:
    if len(HIGHER_CENTER_CONDITIONS) != 4 or len(set(HIGHER_CENTER_CONDITIONS)) != 4:
        raise FLT1HypothesisError(
            "شروطُ المركز الأعلى أربعةٌ متمايزةٌ بنصّ الفرضية؛ لا خامسَ ولا مكرَّر"
        )


_refuse_a_duplicated_site()
_refuse_a_text_that_lost_a_required_site()
_refuse_a_fifth_higher_center_condition()
