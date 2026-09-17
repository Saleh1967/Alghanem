"""`Σ_L`: تجميدُ نصّ فرضية النسبة حرفيًّا، وفاحصُ أمانةٍ يُقابله قبل أيّ قراءة.

هذه الوحدةُ تُودِع **فرضيةً داخليّةً للمشروع** لا قولًا منقولًا من مصدرٍ تراثيّ
(`AnInternalHypothesisIsNotATransmittedSource`): لا `TransmissionStanding` لها،
ولا سندَ نقلٍ يُدّعى لها، ولا تُقرَأ شاهدًا على أحد. وإن أُضيفت مصادرُ خارجيّةٌ
لاحقًا فهي **شواهدُ مستقلّةٌ** تُقابَل بها الفرضية، لا أساسٌ مُصطنَعٌ لفرضيةٍ
وُلِدت هنا.

**والفحصُ يُشتَقّ ولا يُوعَد به** (`FidelityIsDerivedNotPromised`)، على منهج
`flt1_hypothesis` بعينه: تُسمّى مواضعُ الترميز الحاسمة واحدًا واحدًا، ويُشتَقّ
حضورُها من النصّ المودَع نفسِه، ويسقط الاستيرادُ عند غياب موضعٍ منها.

**ولا قراءةَ في هذا الإيداع** (`NoReadoutExistsForNSB0Yet`): نصٌّ وبنيةٌ صوريّةٌ
وتسجيلٌ فقط. والقراءةُ التجريبيّةُ الأولى ممنوعةٌ قبل أن تُسمّى مدوّنةٌ مستقلّةٌ
لم تدخل في بناء الفرضية ولا في تجارب `G0.FLT` السابقة.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادة ولا تجميدَ `E0`، ولا استيرادَ من
`kernel/` ولا من `arabic/`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest

__all__ = [
    "AN_INTERNAL_HYPOTHESIS_IS_NOT_A_TRANSMITTED_SOURCE_NOTE",
    "FIDELITY_IS_DERIVED_NOT_PROMISED_NOTE",
    "NISBAH_HYPOTHESIS_NAMED_RESIDUALS",
    "NISBAH_HYPOTHESIS_TEXT",
    "NISBAH_TEXT_DIGEST",
    "NO_READOUT_EXISTS_FOR_NSB0_YET_NOTE",
    "REQUIRED_NOTATION_SITES",
    "THREE_LEVELS_ARE_NOT_TWO_NOTE",
    "FidelityReport",
    "FidelitySiteReading",
    "FidelityStanding",
    "NisbahHypothesisError",
    "NotationSite",
    "derive_fidelity_report",
    "nisbah_text_digest",
]


class NisbahHypothesisError(ValueError):
    """رفضٌ مُسمّى في وحدة نصّ `G0.NSB-0`؛ لا تصحيحَ صامتًا ولا تخطّي."""


NISBAH_HYPOTHESIS_TEXT: Final[str] = r"""فرضيةٌ داخليّةٌ للمشروع، لا قولٌ منقول.

الأصل المُقترَح:

\boxed{\text{اللغةُ نظامٌ لإنشاء النِّسَب بين الأجناس والصفات}}

ودعوى هذه الفرضية أنّ:

\forall X,\quad X=(Carrier,State)

تصلح نواةَ تمثيلٍ وتنفيذ، ولا تصلح وحدَها نواةً عليا للغة؛ لأنّ حاملَين
وحالتَين لا يُنتجان نسبةً، فالمفقود كيانٌ ثالث:

\boxed{Relation / Nisbah}

فالحدُّ الأدنى اللغويّ أقرب إلى:

\boxed{(Term,\ Predicate,\ Relation)}

ولا يُؤخَذ الطرفُ الأوّل جنسًا بالمعنى المنطقيّ الضيّق، لأنّ «زيد» و«هذا»
و«أنا» و«خمسة رجال» ليست أجناسًا بذلك المعنى. فالأصلُ الأعمّ:

\boxed{TermAnchor}

ومن فروعه المرشَّحة:

Genus,\ Individual,\ Reference,\ EventAnchor,\ QuantityAnchor
\subseteq TermAnchor.

وليست كلُّ صفةٍ أحاديّة، فالمحمولُ ذو رتبة:

\boxed{
Predicate_n(t_1,\ldots,t_n)
}

ومواضعُ الحجج مواضعُ داخلَ المحمول:

\boxed{ArgumentSlot}

بلا تسميةٍ دلاليّةٍ مسبقة؛ فـ Agent و Patient و Cause و Result تُولَد من
طبقتها الخاصّة إن وُلِدت، ولا تدخل النواةَ قبل ولادتها.

والمستوياتُ ثلاثةٌ لا مستويان:

\boxed{
\Sigma_M
\rightarrow
\Sigma_L
\rightarrow
\Sigma_{AR}
}

حيث \Sigma_M قانونُ التمثيل العامّ، و\Sigma_L النواةُ اللغويّةُ العامّة التي
تُولِّد:

TermAnchor,\ Predicate,\ Operator,\ ArgumentSlot,\ Nisbah,\ Constraint,\ RelationalClosure

و\Sigma_{AR} تحقيقُها العربيّ.

ولا تناقضَ بين الأصلين، فلكلٍّ سؤالُه:

\boxed{
Representation(x)=(Carrier,State)
}

يجيب: كيف يوجد الكيانُ في النظام؟ بينما:

\boxed{
LinguisticFunction(x)=RelationalRole(x)
}

يجيب: ماذا يفعل هذا الكيانُ بوصفه لغة؟ فالجديدُ يُرتّب المنزلةَ ولا يُفنّد
النتيجةَ القديمة، ولا يُسمّى منافسًا إلا إن أُثبِت تناقضٌ منطقيٌّ محدَّد.

فالقاعدةُ الكاملة:

\boxed{
LinguisticObject(x)
=
Representation(x)
+
RelationalRole(x)
}

ورتبةُ المحمول لا تُنتزَع من الحالة المستهدَفة بعد رؤيتها:

\boxed{
ArityMustBeLicensedBeforeUse
}

فقد تأتي من مواصفةٍ سابقة، أو مصدرٍ معجميّ، أو برهانٍ سابق، أو استدلالٍ مستقلٍّ
مُجمَّدٍ مسبقًا؛ ولا تأتي من الحالة التي تُثبَت بها.

وإغلاقُ النسبة ليس امتلاءَ الحجج وحدَه:

\boxed{
RelationalClosure
=
ArgumentsClosed
\land
OperatorsScoped
\land
ConstraintsLicensed
\land
ReferencesResolved
\land
NoCrossBoundaryActiveResidual
}

والإغلاقُ لا يُنتج الإفادةَ آليًّا:

\boxed{
RelationalClosure
\Rightarrow
PreIfadahClosure
}

ثمّ:

\boxed{
Ifadah=
ClosedNisbah+LicensedForce+RequiredContext
}

فتبقى «لا إفادة بلا نسبة» ولا تصير «كلُّ نسبةٍ مغلقةٍ إفادة»؛ فـ«هل قام زيد؟»
نسبتُها مكتملةٌ وليست إخبارًا.

والمعيارُ النهائيّ:

\boxed{
MetaRepresentation \neq LinguisticRelation \neq ArabicInstantiation
}

مع بقاء كلّ مستوًى قابلًا للفشل مستقلًّا عن الآخر:

\boxed{
Carrier/State
\;\text{ليس غاية اللغة، بل وعاء تحققها}
}

ثمّ:

\boxed{
Term+Predicate+Operator
\rightarrow Nisbah
\rightarrow PreIfadahClosure
\rightarrow Ifadah
}
"""  # noqa: E501


class FidelityStanding(Enum):
    """منزلةُ النصّ المودَع؛ ثنائيّةٌ لأنّ الموضعَ إمّا حضر أو غاب."""

    ALL_REQUIRED_SITES_PRESENT = "كلُّ_المواضع_الحاسمة_حاضرةٌ_في_النصّ_المودَع"
    A_REQUIRED_SITE_IS_ABSENT = "موضعٌ_حاسمٌ_غائبٌ_فالتسجيلُ_باطلٌ_قبل_تشغيله"


@dataclass(frozen=True, slots=True)
class NotationSite:
    """موضعُ ترميزٍ حاسمٌ في النصّ، بما يقرّره وبما يسقط بسقوطه."""

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
                raise NisbahHypothesisError(
                    f"{name} نصٌّ غيرُ فارغ؛ وموضعٌ بلا حرفيّةٍ لا يُفحَص"
                )


REQUIRED_NOTATION_SITES: Final[tuple[NotationSite, ...]] = (
    NotationSite(
        site_id="the-three-levels",
        literal=(
            r"\Sigma_M"
            "\n"
            r"\rightarrow"
            "\n"
            r"\Sigma_L"
            "\n"
            r"\rightarrow"
            "\n"
            r"\Sigma_{AR}"
        ),
        what_it_decides="أنّ المستوياتِ ثلاثةٌ لا مستويان، وأنّ `Σ_L` مستوًى مستقلّ",
        what_its_absence_invalidates="التصحيحَ المعماريَّ كلَّه، فيعود الثنائيُّ الزائف",
    ),
    NotationSite(
        site_id="the-minimal-linguistic-triple",
        literal=r"\boxed{(Term,\ Predicate,\ Relation)}",
        what_it_decides="أنّ الحدَّ الأدنى اللغويَّ ثلاثيٌّ لا ثنائيّ",
        what_its_absence_invalidates="دعوى أنّ النسبةَ كيانٌ ثالثٌ لا يُغني عنه طرفاه",
    ),
    NotationSite(
        site_id="the-term-anchor",
        literal=r"\boxed{TermAnchor}",
        what_it_decides="أنّ الأصلَ الأعمَّ مرساةُ طرفٍ لا جنسٌ منطقيٌّ ضيّق",
        what_its_absence_invalidates="تعميمَ الطرف، فتسقط «زيد» و«هذا» خارج النواة",
    ),
    NotationSite(
        site_id="the-candidate-branches",
        literal=(
            r"Genus,\ Individual,\ Reference,\ EventAnchor,\ QuantityAnchor"
            "\n"
            r"\subseteq TermAnchor."
        ),
        what_it_decides="أنّ الجنسَ فرعٌ مرشَّحٌ من `TermAnchor` لا أصلٌ بإزائه",
        what_its_absence_invalidates="ترتيبَ الأصل والفرع في طرف النسبة",
    ),
    NotationSite(
        site_id="the-n-ary-predicate",
        literal=r"Predicate_n(t_1,\ldots,t_n)",
        what_it_decides="أنّ المحمولَ ذو رتبةٍ لا صفةٌ أحاديّةٌ دائمًا",
        what_its_absence_invalidates=(
            "`Greater(x,y)` و`Give(x,y,z)`، فتضيق النواةُ عنهما"
        ),
    ),
    NotationSite(
        site_id="the-argument-slot",
        literal=r"\boxed{ArgumentSlot}",
        what_it_decides="أنّ موضعَ الحجّة أوّليٌّ بلا تسميةٍ دلاليّةٍ مسبقة",
        what_its_absence_invalidates="تأجيلَ Agent/Patient، فتدخل النواةَ قبل ولادتها",
    ),
    NotationSite(
        site_id="representation-question",
        literal=r"\boxed{" "\n" r"Representation(x)=(Carrier,State)" "\n" r"}",
        what_it_decides="أنّ الحامل/الحالة يجيب سؤالَ كيفيّة التحقّق",
        what_its_absence_invalidates="طرفَ النسبيّة الأعلى، فيعود التنافسُ المُلغى",
    ),
    NotationSite(
        site_id="relational-function-question",
        literal=r"\boxed{" "\n" r"LinguisticFunction(x)=RelationalRole(x)" "\n" r"}",
        what_it_decides="أنّ النسبةَ تجيب سؤالَ الوظيفة اللغويّة لا سؤالَ الوجود",
        what_its_absence_invalidates="الطرفَ الثانيَ من النسبيّة، فتصير دعوى نسخ",
    ),
    NotationSite(
        site_id="the-complete-rule",
        literal=(
            r"LinguisticObject(x)"
            "\n"
            r"="
            "\n"
            r"Representation(x)"
            "\n"
            r"+"
            "\n"
            r"RelationalRole(x)"
        ),
        what_it_decides="أنّ الكيانَ اللغويَّ تمثيلٌ **ودورٌ** معًا",
        what_its_absence_invalidates="القاعدةَ الجامعةَ التي تمنع الاختزالَ في أحدهما",
    ),
    NotationSite(
        site_id="arity-must-be-licensed",
        literal=r"\boxed{" "\n" r"ArityMustBeLicensedBeforeUse" "\n" r"}",
        what_it_decides="أنّ الرتبةَ تُرخَّص قبل استعمالها ولا تُنتزَع من الحالة الهدف",
        what_its_absence_invalidates="القانونَ الذي يمنع دورَ الإثبات على نفسه",
    ),
    NotationSite(
        site_id="the-five-fold-closure",
        literal=(
            r"RelationalClosure"
            "\n"
            r"="
            "\n"
            r"ArgumentsClosed"
            "\n"
            r"\land"
            "\n"
            r"OperatorsScoped"
            "\n"
            r"\land"
            "\n"
            r"ConstraintsLicensed"
            "\n"
            r"\land"
            "\n"
            r"ReferencesResolved"
            "\n"
            r"\land"
            "\n"
            r"NoCrossBoundaryActiveResidual"
        ),
        what_it_decides="أنّ الإغلاقَ خمسةُ مكوّناتٍ مجتمعةٍ لا امتلاءُ الحجج وحدَه",
        what_its_absence_invalidates="الإغلاقَ نفسَه، فيُقرَأ ناقصًا مغلقًا",
    ),
    NotationSite(
        site_id="closure-yields-pre-ifadah",
        literal=(r"RelationalClosure" "\n" r"\Rightarrow" "\n" r"PreIfadahClosure"),
        what_it_decides="أنّ ناتجَ الإغلاق الأوّلَ ما قبلَ الإفادة لا الإفادة",
        what_its_absence_invalidates="الخطوةَ التي تمنع قفزَ الإغلاق إلى الإفادة",
    ),
    NotationSite(
        site_id="ifadah-needs-force-and-context",
        literal=r"Ifadah=" "\n" r"ClosedNisbah+LicensedForce+RequiredContext",
        what_it_decides="أنّ الإفادةَ نسبةٌ مغلقةٌ وقوّةٌ مُرخَّصةٌ وسياقٌ لازم",
        what_its_absence_invalidates="الفرقَ بين «هل قام زيد؟» وبين الإخبار",
    ),
    NotationSite(
        site_id="the-final-criterion",
        literal=(
            r"MetaRepresentation \neq LinguisticRelation \neq ArabicInstantiation"
        ),
        what_it_decides="المعيارَ النهائيَّ للدفعة: ثلاثةُ مستوياتٍ تفشل مستقلّةً",
        what_its_absence_invalidates="قابليّةَ كلّ مستوًى للفشل وحدَه",
    ),
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


def nisbah_text_digest(text: str | None = None) -> str:
    """اشتقّ بصمةَ النصّ من بايتاته المعياريّة؛ ولا تُكتَب بجانبه ثابتًا."""

    text = NISBAH_HYPOTHESIS_TEXT if text is None else text
    if not isinstance(text, str) or not text.strip():
        raise NisbahHypothesisError("النصُّ المُجمَّد نصٌّ غيرُ فارغ")
    return canonical_digest(canonical_bytes(text))


NISBAH_TEXT_DIGEST: Final[str] = nisbah_text_digest()


def derive_fidelity_report(text: str | None = None) -> FidelityReport:
    """اشتقّ حضورَ كلّ موضعٍ حاسمٍ من النصّ المودَع؛ ولا تُصرِّح بأمانةٍ منقولة."""

    text = NISBAH_HYPOTHESIS_TEXT if text is None else text
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
        text_digest=nisbah_text_digest(text),
    )


AN_INTERNAL_HYPOTHESIS_IS_NOT_A_TRANSMITTED_SOURCE_NOTE: Final[str] = (
    "AnInternalHypothesisIsNotATransmittedSource: هذا النصُّ فرضيةٌ وُلِدت في "
    "المشروع، فلا سندَ نقلٍ يُدّعى لها ولا منزلةَ روايةٍ تُقرَأ فيها؛ وما يُضاف "
    "من مصادرَ خارجيّةٍ لاحقًا شاهدٌ مستقلٌّ يُقابَل به، لا أساسٌ يُصطنَع لها"
)

FIDELITY_IS_DERIVED_NOT_PROMISED_NOTE: Final[str] = (
    "FidelityIsDerivedNotPromised: أمانةُ النصّ تُشتَقّ موضعًا بموضعٍ ويسقط "
    "الاستيرادُ عند غياب موضعٍ حاسم؛ والوعدُ بالحرفيّة ليس فحصًا لها"
)

NO_READOUT_EXISTS_FOR_NSB0_YET_NOTE: Final[str] = (
    "NoReadoutExistsForNSB0Yet: هذا الإيداعُ نصٌّ وبنيةٌ صوريّةٌ وتسجيلٌ فقط؛ "
    "ولا قراءةَ تجريبيّةً فيه، ولا تُختار مدوّنةٌ بعد رؤية نتيجة"
)

THREE_LEVELS_ARE_NOT_TWO_NOTE: Final[str] = (
    "ThreeLevelsAreNotTwo: سؤالُ «أفي `Σ_M` أم في `Σ_A`؟» ثنائيٌّ زائف؛ "
    "و`Σ_L` مستوًى ثالثٌ قائمٌ بنفسه بين قانون التمثيل وتحقيقه العربيّ"
)

NISBAH_HYPOTHESIS_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    AN_INTERNAL_HYPOTHESIS_IS_NOT_A_TRANSMITTED_SOURCE_NOTE,
    FIDELITY_IS_DERIVED_NOT_PROMISED_NOTE,
    NO_READOUT_EXISTS_FOR_NSB0_YET_NOTE,
    THREE_LEVELS_ARE_NOT_TWO_NOTE,
)


def _refuse_a_text_that_lost_a_required_site() -> None:
    report = derive_fidelity_report()
    if not report.is_fit_to_be_run:
        raise NisbahHypothesisError(
            "سقط موضعٌ حاسمٌ من النصّ المودَع: "
            + "، ".join(report.absent_site_ids)
            + "؛ والتسجيلُ باطلٌ قبل تشغيله لا ناقصُ تنسيق"
        )


_refuse_a_text_that_lost_a_required_site()
