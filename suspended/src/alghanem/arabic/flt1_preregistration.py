"""تسجيلُ G0.FLT-1 قبل تشغيله: فرضياتٌ منفصلةٌ، وضوابطُ سلبيّةٌ، وشروطُ حكمٍ مُجمَّدة.

هذه الوحدةُ تُودَع **قبل** وجود أيّ وحدةِ قراءةٍ تقرأ منها، وتُقابَل بالنصّ
الوارد قبل أن تُشغَّل. ولا تُشغِّل شيئًا، ولا تقرأ مدوّنة، ولا تستورد من
`kernel/`، ولا تُصدِر حكمًا.

**والفرضياتُ منفصلةٌ لا قانونٌ واحدٌ ضخم** (`SeparateHypothesesFailSeparately`):
`H_1` و`H_2` و`H_{M0}` و`H_B` و`H_{Close}` و`H_{M1}` تُختبَر كلٌّ على حدة، ويسقط
الساقطُ منها وحدَه. فجمعُها في دعوى واحدةٍ يجعل نجاحَ أسهلها سترًا على فشل
أصعبها.

**والعددُ متنبَّأٌ به لا مفروض** (`TheCountIsTestedAfterTheQuotient`): يُشتَقّ
`C_0` حاصلَ قسمةٍ بعلاقةِ تكافؤٍ **مُعلَنةٍ قبل التشغيل**، ثمّ يُعَدّ. فالعددُ
`28` تنبّؤٌ يُكذَّب، ولو أُدخِل في التعريف لصار الاختبارُ اختبارَ التعريف.

**وأهمُّ ما في هذا التسجيل ضوابطُه السلبيّة**
(`AWeakerRepresentationThatTiesDefeatsTheClaim`): ثلاثةُ تمثيلاتٍ أضعفَ —
الحاملُ وحدَه، والحالةُ وحدَها، والزوجُ غيرُ المرتَّب — تُشغَّل على الصور
نفسِها. فإن ساوى أحدُها الربطَ المُرخَّص سقطت دعوى أنّ حامل/حالةٍ هو المركزُ
الأدنى. والمساواةُ كافيةٌ للإسقاط، ولا يُشترَط التفوّق.

**والاسمُ يُستحَقّ بأربعةٍ لا بواحد** (`FourConditionsOrNoHigherCenter`): إعادةُ
البناء، والأدنويّة، وامتناعُ التجاوز، والإغلاق.

**وحفظُ الهويّةِ مُتحقَّقٌ أو الزوجُ قاصر** (`IdentityIsVerifiedOrThePairIsUnderpowered`):
درسُ `G0.FLT-0` أنّ بولًا يخرج من مُرمِّزٍ ليس ثابتًا مُتحقَّقًا منه. فإن لم
يمرّ الحفظُ ببوّابة التحقّق فالحكمُ `UNDERPOWERED`، لا إصابةٌ تُعَدّ.

**والصورُ لم تُقرأ في `G0.FLT-0`** (`SeenSurfacesAreNotEvidenceAgain`): صورُ
`G0.FLT-0` الخمسُ ممنوعةٌ هنا بالاسم، ويُفحَص المنعُ عند الاستيراد لا يُوكَل
إلى الانتباه.

**ولا حكمَ في هذه الوحدة**: `Registration != Reading`، و`FrozenText !=
EstablishedLaw`، ولا `E0`، ولا ولادة.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from alghanem.canonical_content import canonical_bytes, canonical_digest

from .flt1_hypothesis import (
    FLT1_HYPOTHESIS_TEXT,
    FLT1_TEXT_DIGEST,
    HIGHER_CENTER_CONDITIONS,
)
from .fractal_transition_preregistration import (
    FROZEN_CASES as FLT0_FROZEN_CASES,
)

__all__ = [
    "AWEAKER_REPRESENTATION_THAT_TIES_DEFEATS_THE_CLAIM_NOTE",
    "DECLARED_HYPOTHESES",
    "FLT1_FROZEN_SURFACES",
    "FLT1_PREREGISTRATION_DIGEST",
    "FLT1_PREREGISTRATION_NAMED_RESIDUALS",
    "FOUR_CONDITIONS_OR_NO_HIGHER_CENTER_NOTE",
    "HIGHER_CENTER_CONDITION_DECLARATIONS",
    "IDENTITY_IS_VERIFIED_OR_THE_PAIR_IS_UNDERPOWERED_NOTE",
    "SEEN_SURFACES_ARE_NOT_EVIDENCE_AGAIN_NOTE",
    "SEPARATE_HYPOTHESES_FAIL_SEPARATELY_NOTE",
    "THE_COUNT_IS_TESTED_AFTER_THE_QUOTIENT_NOTE",
    "WEAKER_REPRESENTATIONS",
    "ConditionDeclaration",
    "FLT1PreregistrationError",
    "FrozenSurface",
    "HypothesisDeclaration",
    "HypothesisKind",
    "WeakerRepresentation",
    "flt1_preregistration_digest",
    "hypothesis_named",
]


class FLT1PreregistrationError(ValueError):
    """رفضٌ مُسمّى في تسجيل G0.FLT-1؛ لا تصحيحَ صامتًا ولا تخطّي."""


def _require_text(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise FLT1PreregistrationError(
            f"{field_name} نصٌّ غيرُ فارغ؛ وبندٌ فارغٌ ليس بندًا مُسجَّلًا"
        )
    return value


class HypothesisKind(Enum):
    """جنسُ الفرضية؛ مغلقٌ لأنّ كلَّ جنسٍ يُفحَص فحصًا مختلفًا."""

    QUOTIENT_THEN_COUNT = "حاصلُ_قسمةٍ_يُشتَقّ_ثمّ_يُعَدّ"
    PREDICTED_PRODUCT = "جداءٌ_متنبَّأٌ_به_لا_مفروض"
    GENERATIVE_WITH_A_NEGATIVE_CONTROL = "توليدٌ_له_ضابطٌ_سلبيٌّ_مُعلَن"
    STRUCTURE_BUILDING = "بناءُ_بنيةٍ_أعلى_بشروطٍ_مسبقة"


@dataclass(frozen=True, slots=True)
class HypothesisDeclaration:
    """فرضيّةٌ واحدةٌ مُسجَّلةٌ قبل تشغيلها، بما يُثبتها وما يُسقطها وما يُقصِرها."""

    hypothesis_id: str
    kind: HypothesisKind
    statement: str
    derivation_before_the_test: str
    predicted_result: str
    what_would_falsify_it: str
    underpowered_condition: str
    what_would_lift_underpowered: str

    def __post_init__(self) -> None:
        _require_text(self.hypothesis_id, "مُعرِّفُ الفرضية")
        _require_text(self.statement, "نصُّ الفرضية")
        _require_text(self.derivation_before_the_test, "الاشتقاقُ السابق للاختبار")
        _require_text(self.predicted_result, "النتيجةُ المتنبَّأُ بها")
        _require_text(self.what_would_falsify_it, "ما يُكذِّبها")
        _require_text(self.underpowered_condition, "شرطُ القصور")
        _require_text(self.what_would_lift_underpowered, "ما يرفع القصور")
        if not isinstance(self.kind, HypothesisKind):
            raise FLT1PreregistrationError("جنسُ الفرضية من المفردة المغلقة وحدَها")

    def as_canonical_mapping(self) -> dict[str, str]:
        """صورةٌ معياريّةٌ تدخل البصمة؛ بنيويّةٌ لا سلسلةٌ موصولةٌ بفواصل."""

        return {
            "hypothesis_id": self.hypothesis_id,
            "kind": self.kind.value,
            "statement": self.statement,
            "derivation_before_the_test": self.derivation_before_the_test,
            "predicted_result": self.predicted_result,
            "what_would_falsify_it": self.what_would_falsify_it,
            "underpowered_condition": self.underpowered_condition,
            "what_would_lift_underpowered": self.what_would_lift_underpowered,
        }


DECLARED_HYPOTHESES: Final[tuple[HypothesisDeclaration, ...]] = (
    HypothesisDeclaration(
        hypothesis_id="H1-carrier-quotient",
        kind=HypothesisKind.QUOTIENT_THEN_COUNT,
        statement=r"C_0=\operatorname{Quotient}(\widetilde C)\ \text{ثمّ}\ |C_0|=28",
        derivation_before_the_test=(
            "تُعلَن علاقةُ التكافؤ على الحوامل المرصودة قبل التشغيل — أيُّ "
            "صورتين تُعَدّان حاملًا واحدًا — ثمّ يُشتَقّ حاصلُ القسمة منها؛ "
            "ولا يدخل العددُ المتوقَّع في العلاقة بأيّ وجه"
        ),
        predicted_result="عددُ صفوف التكافؤ يساوي 28",
        what_would_falsify_it=(
            "أن يُخرِج حاصلُ القسمة المُشتَقّ عددًا غيرَ 28 على المدوّنة "
            "المُجمَّدة؛ والعددُ الأقربُ ليس نجاحًا مُقرَّبًا"
        ),
        underpowered_condition=(
            "ألّا تكون علاقةُ التكافؤ مُعلَنةً قبل التشغيل، أو ألّا تُخرِج "
            "المدوّنةُ المُجمَّدة كلَّ الحوامل المرصودة"
        ),
        what_would_lift_underpowered=(
            "علاقةُ تكافؤٍ مُودَعةٌ ببصمتها، ومدوّنةٌ تُحَلّ بايتاتُها في النسخة"
        ),
    ),
    HypothesisDeclaration(
        hypothesis_id="H2-state-quotient",
        kind=HypothesisKind.QUOTIENT_THEN_COUNT,
        statement=(
            r"V_0=\operatorname{Quotient}(\widetilde V)\ \text{ثمّ}\ " r"V_0=\{\َ,\ُ,\ِ,\ْ\}"
        ),
        derivation_before_the_test=(
            "تُعلَن علاقةُ التكافؤ على الحالات المرصودة قبل التشغيل، ثمّ "
            "يُشتَقّ حاصلُ القسمة؛ ولا تُملى الحالاتُ الأربع في العلاقة"
        ),
        predicted_result="صفوفُ التكافؤ هي الأربعُ المُسمّاةُ في النصّ بأعيانها",
        what_would_falsify_it=(
            "أن يُخرِج حاصلُ القسمة صفًّا خامسًا، أو أن يدمج اثنين من الأربعة، "
            "أو أن يُخرِج صفًّا لا يقابل واحدةً منها"
        ),
        underpowered_condition=(
            "ألّا يُميَّز السكونُ الوقفيُّ من الوصليّ في المُدخَل، فتكون "
            "الحالةُ الرابعةُ غيرَ مقروءةٍ أصلًا"
        ),
        what_would_lift_underpowered=(
            "مُدخَلٌ مُصرَّحٌ بحاله وصلًا أو وقفًا، أو علامةٌ تفرزهما في المدوّنة"
        ),
    ),
    HypothesisDeclaration(
        hypothesis_id="HM0-product-center",
        kind=HypothesisKind.PREDICTED_PRODUCT,
        statement=r"M_0=C_0\times V_0",
        derivation_before_the_test=(
            "يُبنى المركزُ الأدنى جداءً للحاصلين المُشتقَّين في `H_1` و`H_2`، "
            "بعد اشتقاقهما لا قبله"
        ),
        predicted_result=(
            "حجمُ `M_0` هو جداءُ الحجمين المُشتقَّين، ويقع 28×4 نتيجةً إن صحّ " "الفرضان قبله"
        ),
        what_would_falsify_it=(
            "أن يسقط `H_1` أو `H_2`، أو أن تُرصَد مراكزُ لا يُنتجها الجداء، "
            "أو أن يبقى من الجداء ما لا يُرصَد له مقابلٌ ولا يُسمّى فراغُه"
        ),
        underpowered_condition="قصورُ أحد الفرضين قبله يجعل الجداءَ غيرَ مقيس",
        what_would_lift_underpowered="رفعُ قصور `H_1` و`H_2` معًا",
    ),
    HypothesisDeclaration(
        hypothesis_id="HB-birth-under-a-vowel",
        kind=HypothesisKind.GENERATIVE_WITH_A_NEGATIVE_CONTROL,
        statement=r"v\in\{\َ,\ُ,\ِ\}\Longrightarrow B(c,v)=CV",
        derivation_before_the_test=(
            "تُشغَّل الولادةُ على كلّ مركزٍ مرصودٍ في الصور المُجمَّدة، ويُقارَن "
            "مخرجُها بالقالب؛ والضابطُ السلبيّ يُشغَّل في المرور نفسِه"
        ),
        predicted_result=(
            r"كلُّ زوجٍ بحركةٍ مفتِّحةٍ يُخرِج `CV`، وكلُّ زوجٍ بسكونٍ يُخرِج " r"`B(c,\ْ)\neq CV`"
        ),
        what_would_falsify_it=(
            "زوجٌ بحركةٍ مفتِّحةٍ لا يُخرِج `CV`، أو زوجٌ بسكونٍ يُخرِجه؛ "
            "والثاني أشدُّ، لأنّه يُسقِط تمييزَ الاختبار نفسَه"
        ),
        underpowered_condition=(
            "ألّا تُرصَد في الصور المُجمَّدة أزواجٌ بسكونٍ أصلًا، فيكون الضابطُ "
            "السلبيُّ غيرَ مُشغَّل"
        ),
        what_would_lift_underpowered="صورٌ تحمل الحالتين معًا بعددٍ مُعلَنٍ قبلها",
    ),
    HypothesisDeclaration(
        hypothesis_id="HClose-sukun-closes",
        kind=HypothesisKind.GENERATIVE_WITH_A_NEGATIVE_CONTROL,
        statement=r"CV+(c,\ْ)\longrightarrow CVC",
        derivation_before_the_test=(
            "يُضَمّ مركزٌ ساكنٌ إلى مقطعٍ مفتوحٍ مرصودٍ، ويُقرأ القالبُ الناتج "
            "من المرمِّز لا من التسمية النحويّة"
        ),
        predicted_result="القالبُ الناتجُ `CVC`، يعيده المرمِّزُ نتيجةً",
        what_would_falsify_it=(
            "أن يُخرِج المرمِّزُ قالبًا آخرَ، أو أن يَقبل الضمَّ بحركةٍ مفتِّحةٍ "
            "فيُخرِج `CVC` كذلك — فيسقط أنّ السكونَ هو المُغلِق"
        ),
        underpowered_condition="ألّا يُرصَد مقطعٌ مفتوحٌ يليه ساكنٌ في الصور",
        what_would_lift_underpowered="صورٌ يُعلَن فيها موضعُ الضمّ قبل تشغيله",
    ),
    HypothesisDeclaration(
        hypothesis_id="HM1-higher-center",
        kind=HypothesisKind.STRUCTURE_BUILDING,
        statement=(
            r"M_1=\operatorname{Close}"
            r"\bigl(\operatorname{Join}(M_0^{(1)},\ldots,M_0^{(k)})\bigr)"
        ),
        derivation_before_the_test=(
            "يُوصَل عددٌ من المراكز الدنيا المرصودة ثمّ يُغلَق الناتج، وتُفحَص "
            "الشروطُ الأربعة عليه كلُّها قبل أن يُسمّى مركزًا أعلى"
        ),
        predicted_result=(
            "يثبت للناتج: إعادةُ البناء، والأدنويّة، وامتناعُ التجاوز، " "والإغلاق، مجتمعةً"
        ),
        what_would_falsify_it=(
            "سقوطُ شرطٍ واحدٍ من الأربعة؛ أو أن يعيد تمثيلٌ أضعفُ المقطعَ بكفاءةٍ "
            "مساوية، فتسقط الأدنويّةُ ومعها الدعوى"
        ),
        underpowered_condition=(
            "ألّا يُتحقَّق من حفظ الهويّة ببوّابة الثوابت، فيبقى مُعلَنًا؛ "
            "أو ألّا تبلغ المراكزُ المرصودةُ عددَ الوصل المُعلَن"
        ),
        what_would_lift_underpowered=(
            "مرورُ حفظ الهويّة ببوّابة التحقّق فيكون `VERIFIED`، وبلوغُ عدد "
            "المراكز المُعلَن قبل التشغيل"
        ),
    ),
)


@dataclass(frozen=True, slots=True)
class ConditionDeclaration:
    """شرطٌ من شروط استحقاق اسم «مركزٍ أعلى»، بما يعنيه وما يُسقطه."""

    condition: str
    what_it_requires: str
    what_would_fail_it: str

    def __post_init__(self) -> None:
        _require_text(self.condition, "اسمُ الشرط")
        _require_text(self.what_it_requires, "ما يطلبه الشرط")
        _require_text(self.what_would_fail_it, "ما يُسقط الشرط")


HIGHER_CENTER_CONDITION_DECLARATIONS: Final[tuple[ConditionDeclaration, ...]] = (
    ConditionDeclaration(
        condition="Reconstruction",
        what_it_requires=(
            "أن يُعيد المقطعُ وحداتِه الدنيا: يُستخرَج من `M_1` تسلسلُ المراكز "
            "الداخلة فيه بعينها وبترتيبها"
        ),
        what_would_fail_it=(
            "مركزٌ داخلٌ لا يُستخرَج، أو يُستخرَج بترتيبٍ غيرِ ترتيبه، أو "
            "يُستخرَج مركزٌ لم يدخل"
        ),
    ),
    ConditionDeclaration(
        condition="Minimality",
        what_it_requires=(
            "ألّا يُعيده تمثيلٌ أضعفُ بالكفاءة نفسِها؛ والمقارنةُ مع الثلاثة "
            "المُسجَّلة في `WEAKER_REPRESENTATIONS` لا مع نموذجٍ يُختار بعد النتيجة"
        ),
        what_would_fail_it=(
            "أن يبلغ أحدُ التمثيلات الأضعف الكفاءةَ نفسَها؛ والتساوي كافٍ "
            "للإسقاط ولا يُشترَط تفوّقه"
        ),
    ),
    ConditionDeclaration(
        condition="NoBypass",
        what_it_requires=(
            "ألّا يوجد مسارٌ يُنتج `M_1` من غير المرور بالوصل المفترَض؛ ويُعلَن "
            "المسارُ المفحوصُ قبل التشغيل"
        ),
        what_would_fail_it=(
            "مسارٌ واحدٌ يُخرِج الناتجَ نفسَه بلا وصل؛ فالوصلُ حينئذٍ زينةٌ لا شرط"
        ),
    ),
    ConditionDeclaration(
        condition="Closure",
        what_it_requires=(
            "أن يُغلِق `M_1` وحدةً واحدةً: لا يقبل زيادةً من جنسه بلا إعادة "
            "وصل، ولا يبقى فيه موضعٌ مفتوحٌ غيرُ مُسمّى"
        ),
        what_would_fail_it=(
            "أن يقبل ضمًّا صامتًا فيتغيّر قالبُه بلا وصلٍ مُعلَن، أو أن يبقى "
            "فيه موضعٌ مفتوحٌ لا يُسمّى"
        ),
    ),
)


@dataclass(frozen=True, slots=True)
class WeakerRepresentation:
    """تمثيلٌ أضعفُ مُسجَّلٌ قبل تشغيله؛ يُشغَّل على الصور نفسِها بلا استثناء."""

    model_id: str
    what_it_reads: str
    what_it_deliberately_ignores: str
    why_a_tie_defeats_the_claim: str

    def __post_init__(self) -> None:
        _require_text(self.model_id, "مُعرِّفُ النموذج")
        _require_text(self.what_it_reads, "ما يقرؤه النموذج")
        _require_text(self.what_it_deliberately_ignores, "ما يتجاهله قصدًا")
        _require_text(self.why_a_tie_defeats_the_claim, "لِمَ يُسقِط التساوي الدعوى")


WEAKER_REPRESENTATIONS: Final[tuple[WeakerRepresentation, ...]] = (
    WeakerRepresentation(
        model_id="carrier-alone",
        what_it_reads="الحاملَ وحدَه، بلا حالةٍ تُعلَّق عليه",
        what_it_deliberately_ignores="الحالةَ كلَّها، حركةً كانت أو سكونًا",
        why_a_tie_defeats_the_claim=(
            "إن بلغ المقطعَ نفسَه بالحامل وحدَه فالحالةُ لا تُسهم، ودعوى أنّ "
            "المركزَ حامل/حالةٌ ساقطة"
        ),
    ),
    WeakerRepresentation(
        model_id="state-alone",
        what_it_reads="الحالةَ وحدَها، بلا حاملٍ تُعلَّق عليه",
        what_it_deliberately_ignores="الحاملَ كلَّه",
        why_a_tie_defeats_the_claim=(
            "إن بلغ المقطعَ نفسَه بالحالة وحدَها فالحاملُ لا يُسهم، والدعوى ساقطة"
        ),
    ),
    WeakerRepresentation(
        model_id="unordered-carrier-state-pair",
        what_it_reads="الحاملَ والحالةَ معًا بوصفهما مجموعةً لا زوجًا مرتَّبًا",
        what_it_deliberately_ignores="الترتيبَ والربطَ المُرخَّص بينهما",
        why_a_tie_defeats_the_claim=(
            "هذا أدقُّ الثلاثة: إن استوى غيرُ المرتَّب بالمرتَّب فالمُسهِمُ "
            "اجتماعُ العنصرين لا ترخيصُ الربط، وهو غيرُ ما تدّعيه الفرضية"
        ),
    ),
)


@dataclass(frozen=True, slots=True)
class FrozenSurface:
    """صورةٌ مُجمَّدةٌ قبل التشغيل، لم تُقرأ في `G0.FLT-0`، بسبب إدخالها."""

    surface: str
    why_it_is_included: str

    def __post_init__(self) -> None:
        _require_text(self.surface, "الصورةُ المُجمَّدة")
        _require_text(self.why_it_is_included, "سببُ إدخال الصورة")


FLT1_FROZEN_SURFACES: Final[tuple[FrozenSurface, ...]] = (
    FrozenSurface(
        surface="فَتَحَ",
        why_it_is_included="ثلاثةُ مقاطعَ مفتوحةٍ متتاليةٍ: الموجَبُ الخالصُ للولادة",
    ),
    FrozenSurface(
        surface="يَكْتُبُ",
        why_it_is_included="سكونٌ داخليٌّ يُغلِق: موضعُ اختبار `CVC` صراحةً",
    ),
    FrozenSurface(
        surface="مَسْجِدٌ",
        why_it_is_included="إغلاقٌ داخليٌّ مع تنوينٍ في الآخر: وصلٌ متعدّدُ المراكز",
    ),
    FrozenSurface(
        surface="بَابٌ",
        why_it_is_included="حرفُ مدٍّ: يُمتحَن به فرزُ الحالة عن الحامل",
    ),
    FrozenSurface(
        surface="شَدَّ",
        why_it_is_included="شدّةٌ: شقّان يُمتحَن بهما امتناعُ التجاوز",
    ),
    FrozenSurface(
        surface="اِسْتَغْفَرَ",
        why_it_is_included="همزةُ وصلٍ وسكونان: أشدُّ الصور على الضابط السلبيّ",
    ),
    FrozenSurface(
        surface="قِفْ",
        why_it_is_included="مقطعٌ واحدٌ مُغلَق: أصغرُ حالةٍ يُختبَر بها الإغلاق",
    ),
)

SEPARATE_HYPOTHESES_FAIL_SEPARATELY_NOTE: Final[str] = (
    "SeparateHypothesesFailSeparately: ستُّ فرضياتٍ تُختبَر كلٌّ على حدة؛ "
    "وجمعُها في دعوى واحدةٍ يجعل نجاحَ أسهلها سترًا على فشل أصعبها"
)

THE_COUNT_IS_TESTED_AFTER_THE_QUOTIENT_NOTE: Final[str] = (
    "TheCountIsTestedAfterTheQuotient: علاقةُ التكافؤ تُعلَن أوّلًا ويُشتَقّ "
    "حاصلُ القسمة، ثمّ يُعَدّ؛ ومَن أدخل `28` في العلاقة اختبر تعريفَه"
)

AWEAKER_REPRESENTATION_THAT_TIES_DEFEATS_THE_CLAIM_NOTE: Final[str] = (
    "AWeakerRepresentationThatTiesDefeatsTheClaim: التمثيلاتُ الثلاثةُ "
    "تُشغَّل على الصور نفسِها، والتساوي كافٍ لإسقاط دعوى المركز الأدنى؛ "
    "ولا يُشترَط تفوّقُ الأضعف"
)

FOUR_CONDITIONS_OR_NO_HIGHER_CENTER_NOTE: Final[str] = (
    "FourConditionsOrNoHigherCenter: إعادةُ البناء والأدنويّة وامتناعُ "
    "التجاوز والإغلاق مجتمعةً؛ وساقطٌ منها يمنع الاسمَ ولا يُخفِّفه"
)

IDENTITY_IS_VERIFIED_OR_THE_PAIR_IS_UNDERPOWERED_NOTE: Final[str] = (
    "IdentityIsVerifiedOrThePairIsUnderpowered: حفظُ الهويّة يُعَدّ شاهدًا متى "
    "مرّ ببوّابة التحقّق؛ وإلّا فالحكمُ `UNDERPOWERED` لا إصابةٌ تُعَدّ"
)

SEEN_SURFACES_ARE_NOT_EVIDENCE_AGAIN_NOTE: Final[str] = (
    "SeenSurfacesAreNotEvidenceAgain: صورُ `G0.FLT-0` الخمسُ ممنوعةٌ هنا "
    "بالاسم، ويُفحَص المنعُ عند الاستيراد لا يُوكَل إلى الانتباه"
)

FLT1_PREREGISTRATION_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    SEPARATE_HYPOTHESES_FAIL_SEPARATELY_NOTE,
    THE_COUNT_IS_TESTED_AFTER_THE_QUOTIENT_NOTE,
    AWEAKER_REPRESENTATION_THAT_TIES_DEFEATS_THE_CLAIM_NOTE,
    FOUR_CONDITIONS_OR_NO_HIGHER_CENTER_NOTE,
    IDENTITY_IS_VERIFIED_OR_THE_PAIR_IS_UNDERPOWERED_NOTE,
    SEEN_SURFACES_ARE_NOT_EVIDENCE_AGAIN_NOTE,
)


def hypothesis_named(hypothesis_id: str) -> HypothesisDeclaration:
    """أعِد الفرضيةَ المُعلَنة بمُعرِّفها؛ وغيرُ المُعلَنة تُرَدّ لا تُنشَأ."""

    for declaration in DECLARED_HYPOTHESES:
        if declaration.hypothesis_id == hypothesis_id:
            return declaration
    raise FLT1PreregistrationError(
        f"الفرضية «{hypothesis_id}» غيرُ مُعلَنةٍ قبل التشغيل، فلا تُقرأ بعده"
    )


def flt1_preregistration_digest() -> str:
    """اشتقّ بصمةَ التسجيل من بنيته كاملةً؛ ولا تُكتَب ثابتًا منقولًا."""

    payload = {
        "hypothesis_text_digest": FLT1_TEXT_DIGEST,
        "hypotheses": [
            declaration.as_canonical_mapping() for declaration in DECLARED_HYPOTHESES
        ],
        "higher_center_conditions": [
            {
                "condition": item.condition,
                "what_it_requires": item.what_it_requires,
                "what_would_fail_it": item.what_would_fail_it,
            }
            for item in HIGHER_CENTER_CONDITION_DECLARATIONS
        ],
        "weaker_representations": [
            {
                "model_id": item.model_id,
                "what_it_reads": item.what_it_reads,
                "what_it_deliberately_ignores": item.what_it_deliberately_ignores,
                "why_a_tie_defeats_the_claim": item.why_a_tie_defeats_the_claim,
            }
            for item in WEAKER_REPRESENTATIONS
        ],
        "frozen_surfaces": [
            {
                "surface": item.surface,
                "why_it_is_included": item.why_it_is_included,
            }
            for item in FLT1_FROZEN_SURFACES
        ],
        "named_residuals": list(FLT1_PREREGISTRATION_NAMED_RESIDUALS),
    }
    return canonical_digest(canonical_bytes(payload))


FLT1_PREREGISTRATION_DIGEST: Final[str] = flt1_preregistration_digest()


def _refuse_a_surface_already_read_in_flt0() -> None:
    seen = {case.surface for case in FLT0_FROZEN_CASES}
    repeated = [item.surface for item in FLT1_FROZEN_SURFACES if item.surface in seen]
    if repeated:
        raise FLT1PreregistrationError(
            "صورٌ قُرِئت في `G0.FLT-0` لا تصلح شاهدًا استباقيًّا: " f"{'، '.join(repeated)}"
        )


def _refuse_a_duplicated_surface() -> None:
    surfaces = [item.surface for item in FLT1_FROZEN_SURFACES]
    if len(surfaces) != len(set(surfaces)):
        raise FLT1PreregistrationError("صورةٌ مكرَّرةٌ تُعَدّ مرّتين وتُقرأ صورتين")


def _refuse_a_condition_outside_the_frozen_four() -> None:
    declared = tuple(item.condition for item in HIGHER_CENTER_CONDITION_DECLARATIONS)
    if declared != HIGHER_CENTER_CONDITIONS:
        raise FLT1PreregistrationError(
            "شروطُ المركز الأعلى هي الأربعةُ المُجمَّدةُ بالنصّ وبترتيبها؛ "
            "وزيادةٌ أو نقصٌ أو إعادةُ ترتيبٍ تغييرٌ للمعيار بعد تجميده"
        )


def _refuse_a_hypothesis_whose_statement_is_absent_from_the_text() -> None:
    for declaration in DECLARED_HYPOTHESES:
        if declaration.kind is HypothesisKind.PREDICTED_PRODUCT and (
            declaration.statement not in FLT1_HYPOTHESIS_TEXT
        ):
            raise FLT1PreregistrationError(
                f"صيغةُ «{declaration.hypothesis_id}» غيرُ موجودةٍ بحرفها في "
                "النصّ المُجمَّد؛ وتسجيلٌ يُعيد صياغةَ نصّه ليس تسجيلًا له"
            )


def _refuse_a_weaker_model_that_is_not_weaker() -> None:
    ids = [item.model_id for item in WEAKER_REPRESENTATIONS]
    if len(ids) != len(set(ids)) or len(ids) != 3:
        raise FLT1PreregistrationError(
            "التمثيلاتُ الأضعفُ ثلاثةٌ متمايزةٌ بنصّ الفرضية؛ لا رابعَ ولا مكرَّر"
        )


_refuse_a_duplicated_surface()
_refuse_a_surface_already_read_in_flt0()
_refuse_a_condition_outside_the_frozen_four()
_refuse_a_hypothesis_whose_statement_is_absent_from_the_text()
_refuse_a_weaker_model_that_is_not_weaker()
