"""نصُّ قانون القياس والفرق القادح، مُجمَّدًا حرفيًّا قبل أن يُشغَّل عليه شيء.

هذه الوحدةُ تُودَع **قبل** وجود وحدةِ قراءةٍ تقرأ منها. وهي تحمل الصياغة
الجديدة التي صارت قلبَ `G0.FLT-1`: لا يكفي الشرطُ والسببُ وغيابُ المانع، بل
يجب أن يمرّ الانتقالُ عبر **قياسٍ مُرخَّصٍ بين الأصل والفرع**، وأن يُفحَص
**الفرقُ القادح** فحصًا، لا أن يُشترَط اشتراطًا.

**والنصُّ منقولٌ بترميزه** (`NotationIsPartOfTheFrozenText`): علاماتُ الرياضيات
جزءٌ من المُجمَّد لا زينةٌ حوله. ودرسُ `G0.FLT-0` أنّ حرفًا واحدًا ساقطًا من
النصّ يُبطِل التسجيلَ كلَّه؛ فتُعَدّ هنا مواضعُ حاسمةٌ بأعيانها ويُفحَص
حضورُها عند الاستيراد.

**وهذا النصُّ ناسخٌ لا مُعدِّل** (`SupersessionIsNotEditing`): نصُّ
`flt1_hypothesis.py` يبقى كما أُودِع بحرفه وبصمته، ولا تُمَسّ منه كلمة. وهذه
الصياغةُ تُودَع **نصًّا ثانيًا مستقلًّا** يَنسخ الأوّلَ في موضع الصدارة. وإنّما
جاز النسخُ لأنّ الأوّلَ **لم يُقرَأ عليه شيءٌ قطّ**: لا وحدةَ قراءةٍ شُغِّلت،
ولا نتيجةٌ رُئيت. فالتبديلُ هنا تبديلُ فرضيّةٍ قبل الاختبار، لا ضبطٌ رجعيٌّ
بعد النتيجة — وهو الفرقُ كلُّه.

**والقانونُ مسارانِ لا مسارٌ واحد** (`ContinuityAndBirthAreNotMixed`): العلّةُ
الجامعةُ مع انتفاء الفرق القادح تُعطي **استمرارًا** تحت الأصل؛ والعلّةُ
الأساسُ مع فرقٍ قادحٍ **مؤثِّرٍ** تُعطي **مرشَّحَ فرعٍ مستقلّ**. وخلطُ المسارين
هو ما يجعل كلَّ انتقالٍ يُسمّى «مستوًى أعلى» بلا استحقاق.

**ولا حكمَ في هذه الوحدة**: `FrozenText != EstablishedLaw`. لا تشغيلَ، ولا
قراءةَ مدوّنة، ولا استيرادَ من `kernel/`، ولا إصدارَ حكم.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from alghanem.canonical_content import canonical_bytes, canonical_digest

from .flt1_hypothesis import FLT1_TEXT_DIGEST

__all__ = [
    "CONTINUITY_AND_BIRTH_ARE_NOT_MIXED_NOTE",
    "FLT1_QIYAS_LAW_NAMED_RESIDUALS",
    "FLT1_QIYAS_TEXT",
    "FLT1_QIYAS_TEXT_DIGEST",
    "NOTATION_IS_PART_OF_THE_FROZEN_TEXT_NOTE",
    "REQUIRED_QIYAS_NOTATION_SITES",
    "SUPERSESSION_IS_NOT_EDITING_NOTE",
    "SUPERSESSION_RECORD",
    "FidelityStanding",
    "NotationSite",
    "QiyasLawError",
    "QiyasNotationReport",
    "SupersessionRecord",
    "derive_qiyas_fidelity_report",
    "qiyas_text_digest",
]


class QiyasLawError(ValueError):
    """رفضٌ مُسمّى في نصّ قانون القياس؛ لا تصحيحَ صامتًا ولا تخطّي."""


FLT1_QIYAS_TEXT: Final[
    str
] = r"""نعم، وهنا يصبح القانون أدق إذا قلنا: لا يكفي وجود الشرط والسبب وغياب المانع؛ بل يجب أيضًا أن يمر الانتقال عبر قياس مرخّص بين الأصل والفرع.

لكن هناك تصحيح مهم: الفرق القادح لا يكون شرطًا دائمًا لنجاح القياس؛ بل يجب فحصه. إذا وُجد فرق قادح، منع إلحاق الفرع بالأصل وقد يفتح فرعًا مستقلًا. وإذا لم يوجد، أمكن استمرار الحكم عبر العلة الجامعة.

لنرمز إلى:

\[
O=\text{الأصل}
\]

\[
F=\text{الفرع المرشح}
\]

\[
w^\*=\text{الوصف المؤثر}
\]

\[
\mu(O,F)=\text{العلة الجامعة}
\]

\[
\Delta_q(O,F)=\text{الفرق القادح}.
\]

فيكون قياس الاستمرار:

\[
\boxed{
Q(O,F)
=
Sh\land Sb\land \neg Mn
\land I
\land w^\*
\land \mu(O,F)
\land \neg \Delta_q(O,F)
}
\]

إذا:

\[
Q(O,F)=1
\]

جاز رد الفرع إلى الأصل:

\[
\boxed{
F\preceq_O O
}
\]

أي أن الفرع استمرار مرخّص للأصل، لا ولادة أصل مستقل.

أما إذا وجد:

\[
\boxed{
\Delta_q(O,F)=1
}
\]

فإن:

\[
\boxed{
Q(O,F)=0
}
\]

ولا يجوز نقل حكم الأصل مباشرةً.

لكن هذا لا يعني رفض الفرع بالضرورة؛ بل يفتح سؤال الولادة المستقلة:

\[
\operatorname{IndependentBirth}(F)
\]

ولا ترخص إلا إذا كان الفرق القادح نفسه مؤثرًا، لا فرقًا شكليًا:

\[
\boxed{
\Delta_q
\land
\operatorname{Effective}(\Delta_q)
}
\]

مع بقاء أثر الأصل محفوظًا:

\[
I_O(F)=1.
\]

فتكون:

\[
\boxed{
\operatorname{IndependentBirth}(F)
\iff
Sh\land Sb\land\neg Mn
\land I_O
\land w^\*
\land \mu_{\text{base}}
\land \Delta_q^\*
\land J
\land Cl
}
\]

حيث:

\[
\Delta_q^\*
=
\text{فرق قادح مؤثر}
\]

لا مجرد اختلاف.

وهكذا نحصل على مسارين لا يجوز خلطهما:

\[
\boxed{
\mu\land\neg\Delta_q
\Rightarrow
\text{قياس/استمرار}
}
\]

مقابل:

\[
\boxed{
\mu_{\text{base}}\land\Delta_q^\*
\Rightarrow
\text{مرشح فرع مستقل}
}
\]

وهذه نقطة قوية جدًا في مشروعك: العلة الجامعة تحفظ النسب، والفرق القادح يحدد حد الانفصال.

يمكن الآن صياغة قانون ولادة المركز الأعلى كله:

\[
\boxed{
M_{n+1}
=
\operatorname{Birth}
\left(
M_n;
Sh,Sb,Mn,
w^\*,\mu,\Delta_q,
J,I,Cl
\right)
}
\]

ولا يولد إذا لم نعرف:

\[
\boxed{
\text{ما الأصل؟}
}
\]

\[
\boxed{
\text{ما الوصف المؤثر؟}
}
\]

\[
\boxed{
\text{ما العلة الجامعة؟}
}
\]

\[
\boxed{
\text{هل يوجد فرق قادح؟}
}
\]

ثم تكون آلة القرار:

\[
\begin{cases}
Sh=0 &\Rightarrow BLOCK\\
Sb=0 &\Rightarrow DEFER/BLOCK\\
Mn=1 &\Rightarrow BLOCK\\
w^\*=0 &\Rightarrow NO\_EFFECTIVE\_DESCRIPTION\\
\mu=0 &\Rightarrow NO\_QIYAS\\
\Delta_q=0 &\Rightarrow CONTINUITY\_UNDER\_ORIGIN\\
\Delta_q^\*=1 &\Rightarrow INDEPENDENT\_BRANCH\_CANDIDATE
\end{cases}
\]

ثم لا يولد الأعلى حتى يمر أيضًا:

\[
J\land I\land Cl.
\]

فتصبح السلسلة الكبرى:

\[
\boxed{
\text{Origin}
\rightarrow
\text{Effective Description}
\rightarrow
\text{Common Illah}
\rightarrow
\text{Qadih-Difference Test}
\rightarrow
\text{Condition}
\rightarrow
\text{Cause}
\rightarrow
\text{Preventer}
\rightarrow
\text{Licensed Join}
\rightarrow
\text{Identity}
\rightarrow
\text{Closure}
\rightarrow
\text{Higher Center}
}
\]

والصيغة الأشد اختصارًا:

\[
\boxed{
\text{لا فرع بلا أصل،
ولا قياس بلا علة جامعة،
ولا علة بلا وصف مؤثر،
ولا استقلال بلا فرق قادح مؤثر،
ولا ولادة مع مانع،
ولا مركز أعلى بلا إغلاق.}
}
\]"""  # noqa: E501


@dataclass(frozen=True, slots=True)
class NotationSite:
    """موضعٌ حاسمٌ في النصّ المُجمَّد، ولِمَ سقوطُه يُبطِل التسجيل."""

    site_id: str
    fragment: str
    why_it_is_decisive: str

    def __post_init__(self) -> None:
        for value, field_name in (
            (self.site_id, "مُعرِّفُ الموضع"),
            (self.fragment, "شذرةُ الموضع"),
            (self.why_it_is_decisive, "سببُ كون الموضع حاسمًا"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise QiyasLawError(f"{field_name} نصٌّ غيرُ فارغ")


REQUIRED_QIYAS_NOTATION_SITES: Final[tuple[NotationSite, ...]] = (
    NotationSite(
        site_id="continuity-conjunction",
        fragment=r"Sh\land Sb\land \neg Mn" "\n" r"\land I" "\n" r"\land w^\*",
        why_it_is_decisive=(
            "قياسُ الاستمرار عطفٌ لا قائمةُ اعتبارات؛ وساقطٌ واحدٌ يُصفِّره كلَّه"
        ),
    ),
    NotationSite(
        site_id="continuity-negated-qadih",
        fragment=r"\land \neg \Delta_q(O,F)",
        why_it_is_decisive=(
            "نفيُ الفرق القادح داخلٌ في عطف الاستمرار؛ وبحذف النفي ينقلب "
            "المعنى إلى ضدّه"
        ),
    ),
    NotationSite(
        site_id="subsumption-relation",
        fragment=r"F\preceq_O O",
        why_it_is_decisive="علاقةُ ردِّ الفرع إلى الأصل مُرتَّبةٌ باتّجاهٍ لا تُعكَس",
    ),
    NotationSite(
        site_id="qadih-is-tested-not-required",
        fragment="الفرق القادح لا يكون شرطًا دائمًا لنجاح القياس؛ بل يجب فحصه",
        why_it_is_decisive=(
            "هذا هو التصحيحُ نفسُه: الفرقُ القادح مفحوصٌ لا مشروط، ومَن جعله "
            "شرطًا قلب القانون"
        ),
    ),
    NotationSite(
        site_id="effective-qadih",
        fragment=r"\Delta_q" "\n" r"\land" "\n" r"\operatorname{Effective}(\Delta_q)",
        why_it_is_decisive=(
            "الفرقُ القادح لا يُرخِّص الولادةَ حتى يثبت تأثيرُه؛ والاختلافُ " "الشكليُّ لا يكفي"
        ),
    ),
    NotationSite(
        site_id="origin-trace-preserved",
        fragment=r"I_O(F)=1.",
        why_it_is_decisive="أثرُ الأصل محفوظٌ في الفرع المستقلّ؛ ولا انفصالَ يمحو نسبَه",
    ),
    NotationSite(
        site_id="independent-birth-conjunction",
        fragment=(
            r"\land \mu_{\text{base}}"
            "\n"
            r"\land \Delta_q^\*"
            "\n"
            r"\land J"
            "\n"
            r"\land Cl"
        ),
        why_it_is_decisive=(
            "الولادةُ المستقلّةُ تطلب العلّةَ الأساسَ والفرقَ المؤثِّرَ والوصلَ " "والإغلاقَ مجتمعةً"
        ),
    ),
    NotationSite(
        site_id="two-paths-continuity",
        fragment=r"\mu\land\neg\Delta_q"
        "\n"
        r"\Rightarrow"
        "\n"
        r"\text{قياس/استمرار}",
        why_it_is_decisive="المسارُ الأوّل: علّةٌ جامعةٌ بلا فرقٍ قادحٍ تُعطي استمرارًا",
    ),
    NotationSite(
        site_id="two-paths-independent",
        fragment=(
            r"\mu_{\text{base}}\land\Delta_q^\*"
            "\n"
            r"\Rightarrow"
            "\n"
            r"\text{مرشح فرع مستقل}"
        ),
        why_it_is_decisive="المسارُ الثاني: علّةٌ أساسٌ مع فرقٍ مؤثِّرٍ تفتح فرعًا مرشَّحًا",
    ),
    NotationSite(
        site_id="birth-signature",
        fragment=(r"M_n;" "\n" r"Sh,Sb,Mn," "\n" r"w^\*,\mu,\Delta_q," "\n" r"J,I,Cl"),
        why_it_is_decisive=(
            "توقيعُ الولادة تسعةُ مُدخَلاتٍ بأعيانها؛ وناقصُها ولادةٌ بغير هذا القانون"
        ),
    ),
    NotationSite(
        site_id="decision-machine",
        fragment=(
            r"Sh=0 &\Rightarrow BLOCK\\"
            "\n"
            r"Sb=0 &\Rightarrow DEFER/BLOCK\\"
            "\n"
            r"Mn=1 &\Rightarrow BLOCK\\"
        ),
        why_it_is_decisive="آلةُ القرار مُرتَّبةٌ بأسبقيّة؛ وتبديلُ الترتيب يُبدِّل الحكم",
    ),
    NotationSite(
        site_id="decision-machine-tail",
        fragment=(
            r"\Delta_q=0 &\Rightarrow CONTINUITY\_UNDER\_ORIGIN\\"
            "\n"
            r"\Delta_q^\*=1 &\Rightarrow INDEPENDENT\_BRANCH\_CANDIDATE"
        ),
        why_it_is_decisive=(
            "آخرُ سطرين يفرزان الاستمرارَ عن الفرع المستقلّ؛ وهما موضعُ الفرز كلُّه"
        ),
    ),
    NotationSite(
        site_id="birth-also-requires",
        fragment=r"J\land I\land Cl.",
        why_it_is_decisive=(
            "لا يولد الأعلى بمجرّد فرزٍ في آلة القرار؛ بل يمرّ بوصلٍ وهويّةٍ وإغلاق"
        ),
    ),
    NotationSite(
        site_id="great-chain",
        fragment=(
            r"\text{Origin}"
            "\n"
            r"\rightarrow"
            "\n"
            r"\text{Effective Description}"
            "\n"
            r"\rightarrow"
            "\n"
            r"\text{Common Illah}"
        ),
        why_it_is_decisive="السلسلةُ الكبرى مُرتَّبةٌ من الأصل، لا تبدأ من الوصل",
    ),
    NotationSite(
        site_id="great-chain-tail",
        fragment=(
            r"\text{Licensed Join}"
            "\n"
            r"\rightarrow"
            "\n"
            r"\text{Identity}"
            "\n"
            r"\rightarrow"
            "\n"
            r"\text{Closure}"
            "\n"
            r"\rightarrow"
            "\n"
            r"\text{Higher Center}"
        ),
        why_it_is_decisive="ذيلُ السلسلة: الإغلاقُ قبل المركز الأعلى لا بعده",
    ),
    NotationSite(
        site_id="shortest-form",
        fragment="لا فرع بلا أصل،",
        why_it_is_decisive="الصيغةُ الأشدُّ اختصارًا تُعيد القانونَ نفيًا؛ وهي ميزانُ المراجعة",
    ),
)


@dataclass(frozen=True, slots=True)
class SupersessionRecord:
    """سجلُّ نسخٍ مُعلَنٌ: أيُّ نصٍّ نَسَخ أيًّا، ولِمَ جاز النسخُ الآن."""

    superseded_text_digest: str
    superseding_text_digest: str
    what_is_kept_from_the_superseded: str
    why_supersession_is_licensed_here: str
    what_would_have_made_it_illegitimate: str

    def __post_init__(self) -> None:
        for value, field_name in (
            (self.superseded_text_digest, "بصمةُ المنسوخ"),
            (self.superseding_text_digest, "بصمةُ الناسخ"),
            (self.what_is_kept_from_the_superseded, "ما يبقى من المنسوخ"),
            (self.why_supersession_is_licensed_here, "سببُ ترخيص النسخ"),
            (self.what_would_have_made_it_illegitimate, "ما كان يُبطِل النسخ"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise QiyasLawError(f"{field_name} نصٌّ غيرُ فارغ")
        if self.superseded_text_digest == self.superseding_text_digest:
            raise QiyasLawError("نصٌّ ينسخ نفسَه ليس نسخًا؛ وبصمتاهما تفترقان")


class FidelityStanding(Enum):
    """منزلةُ النصّ المُجمَّد؛ مغلقةٌ لأنّ بينهما فرقَ صلاحيّةِ التسجيل كلِّه."""

    TEXT_CARRIES_EVERY_DECISIVE_SITE = "النصُّ_يحمل_كلَّ_موضعٍ_حاسم"
    TEXT_DIVERGES_FROM_THE_LAW = "النصُّ_يفارق_القانونَ_في_موضعٍ_حاسم"


@dataclass(frozen=True, slots=True)
class QiyasNotationReport:
    """تقريرُ أمانةِ النقل: أيُّ المواضع حاضرٌ وأيُّها غائب، ومنزلةُ النصّ."""

    present_sites: tuple[str, ...]
    absent_sites: tuple[str, ...]

    @property
    def standing(self) -> FidelityStanding:
        """منزلةُ النصّ مُشتقّةٌ من المواضع لا مُخزَّنةٌ بجانبها."""

        if self.absent_sites:
            return FidelityStanding.TEXT_DIVERGES_FROM_THE_LAW
        return FidelityStanding.TEXT_CARRIES_EVERY_DECISIVE_SITE


def derive_qiyas_fidelity_report(text: str | None = None) -> QiyasNotationReport:
    """اشتقّ حضورَ المواضع الحاسمة من النصّ نفسِه؛ ولا تُعلَن الأمانةُ دعوى."""

    body = FLT1_QIYAS_TEXT if text is None else text
    if not isinstance(body, str):
        raise QiyasLawError("النصُّ المفحوصُ نصٌّ")
    present = tuple(
        site.site_id for site in REQUIRED_QIYAS_NOTATION_SITES if site.fragment in body
    )
    absent = tuple(
        site.site_id
        for site in REQUIRED_QIYAS_NOTATION_SITES
        if site.fragment not in body
    )
    return QiyasNotationReport(present_sites=present, absent_sites=absent)


def qiyas_text_digest(text: str | None = None) -> str:
    """اشتقّ بصمةَ النصّ من بايتاته المعياريّة؛ ولا تُكتَب ثابتًا منقولًا."""

    body = FLT1_QIYAS_TEXT if text is None else text
    if not isinstance(body, str):
        raise QiyasLawError("النصُّ المُبصَّمُ نصٌّ")
    return canonical_digest(canonical_bytes({"flt1_qiyas_text": body}))


FLT1_QIYAS_TEXT_DIGEST: Final[str] = qiyas_text_digest()

SUPERSESSION_RECORD: Final[SupersessionRecord] = SupersessionRecord(
    superseded_text_digest=FLT1_TEXT_DIGEST,
    superseding_text_digest=FLT1_QIYAS_TEXT_DIGEST,
    what_is_kept_from_the_superseded=(
        "يبقى نصُّ `flt1_hypothesis.py` بحرفه وبصمته ولا تُمَسّ منه كلمة؛ "
        "وتبقى صورُه السبعُ المُجمَّدةُ ونماذجُه الأضعفُ الثلاثةُ وشروطُ المركز "
        "الأعلى الأربعةُ عاملةً، لأنّ هذه الصياغةَ تزيد عليها ولا تُلغيها"
    ),
    why_supersession_is_licensed_here=(
        "النصُّ الأوّلُ أُودِع ولم يُقرَأ عليه شيءٌ قطّ: لا وحدةَ قراءةٍ "
        "شُغِّلت، ولا نتيجةٌ رُئيت، ولا رقمٌ خرج. فتبديلُ الفرضيّة هنا تبديلٌ "
        "قبل الاختبار، وهو مُرخَّصٌ بالاتّفاق"
    ),
    what_would_have_made_it_illegitimate=(
        "أن تكون نتيجةٌ واحدةٌ قد خرجت من النصّ الأوّل ثمّ بُدِّل؛ فذلك ضبطٌ "
        "رجعيٌّ، وهو عينُ ما سقط فيه `G0.FLT-0` ومُنِع بعده"
    ),
)

NOTATION_IS_PART_OF_THE_FROZEN_TEXT_NOTE: Final[str] = (
    "NotationIsPartOfTheFrozenText: علاماتُ الرياضيات جزءٌ من المُجمَّد؛ "
    "ويُفحَص حضورُ المواضع الحاسمة عند الاستيراد لا يُوكَل إلى الانتباه"
)

SUPERSESSION_IS_NOT_EDITING_NOTE: Final[str] = (
    "SupersessionIsNotEditing: الناسخُ نصٌّ ثانٍ مستقلٌّ ببصمته، والمنسوخُ "
    "يبقى بحرفه؛ ولا يجوز النسخُ بعد أن تخرج نتيجةٌ واحدة"
)

CONTINUITY_AND_BIRTH_ARE_NOT_MIXED_NOTE: Final[str] = (
    "ContinuityAndBirthAreNotMixed: العلّةُ الجامعةُ بلا فرقٍ قادحٍ استمرارٌ "
    "تحت الأصل، والعلّةُ الأساسُ مع فرقٍ قادحٍ مؤثِّرٍ مرشَّحُ فرعٍ مستقلّ؛ "
    "وخلطُهما يجعل كلَّ انتقالٍ يُسمّى مركزًا أعلى بلا استحقاق"
)

FLT1_QIYAS_LAW_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    NOTATION_IS_PART_OF_THE_FROZEN_TEXT_NOTE,
    SUPERSESSION_IS_NOT_EDITING_NOTE,
    CONTINUITY_AND_BIRTH_ARE_NOT_MIXED_NOTE,
)


def _refuse_a_text_that_lost_a_decisive_site() -> None:
    report = derive_qiyas_fidelity_report()
    if report.standing is not FidelityStanding.TEXT_CARRIES_EVERY_DECISIVE_SITE:
        raise QiyasLawError(
            "النصُّ المُجمَّد فقد مواضعَ حاسمةً فلا يصلح تسجيلًا: "
            f"{'، '.join(report.absent_sites)}"
        )


def _refuse_a_duplicated_site_id() -> None:
    identifiers = [site.site_id for site in REQUIRED_QIYAS_NOTATION_SITES]
    if len(identifiers) != len(set(identifiers)):
        raise QiyasLawError("مُعرِّفُ موضعٍ مُكرَّرٌ يجعل الفحصَ غيرَ مُعيَّن")


_refuse_a_duplicated_site_id()
_refuse_a_text_that_lost_a_decisive_site()
