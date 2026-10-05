"""تسجيلُ آلة القرار في قانون القياس قبل تشغيلها: أصلٌ، ووصفٌ، وعلّةٌ، وفرقٌ.

هذه الوحدةُ تُودَع **قبل** وجود وحدةِ قراءةٍ تقرأ منها، وتُجمِّد ما يجب
تجميدُه قبل أيّ رقم: ما الأصلُ، وما الوصفُ المؤثِّر، وما العلّةُ الجامعة، وكيف
يُفحَص الفرقُ القادح، وبأيّ أسبقيّةٍ تُقرأ آلةُ القرار، وما هدفُ إعادة البناء
الذي تُقاس عليه النماذجُ الأضعف.

**والأسبقيّةُ جزءٌ من القانون** (`PrecedenceIsPartOfTheMachine`): آلةُ القرار
في النصّ مُرتَّبةٌ، وقراءةُ سطرٍ قبل سطرٍ تُبدِّل الحكم. فتُودَع القواعدُ
مُرتَّبةً ويُفحَص ترتيبُها عند الاستيراد، ولا يُترَك إلى ترتيب القاموس.

**والفرقُ القادح مفحوصٌ لا مشروط** (`TheQadihDifferenceIsTestedNotRequired`):
لا يُشترَط وجودُه لنجاح القياس ولا لسقوطه؛ بل يُسأل عنه. فإن انتفى جاز
الاستمرارُ تحت الأصل، وإن ثبت **وثبت تأثيرُه** فُتِح سؤالُ الولادة المستقلّة،
وإن ثبت ولم يُثبَت تأثيرُه فهو اختلافٌ شكليٌّ لا يُرخِّص شيئًا.

**والمساران لا يُخلَطان** (`ContinuityIsNotBirth`): مخرجُ
`CONTINUITY_UNDER_ORIGIN` ليس درجةً أدنى من `INDEPENDENT_BRANCH_CANDIDATE`،
بل حكمٌ آخرُ بمسارٍ آخر. ومَن عدّ الاستمرارَ فشلًا في الولادة خلط البابين.

**وهدفُ إعادة البناء مُعلَنٌ قبل الرقم** (`TheTargetIsFrozenBeforeTheScore`):
تُعاد سلسلةُ قوالب المقاطع بأعيانها وبترتيبها؛ والمُرخَّصُ والأضعفُ يُقاسان
على الهدف نفسِه لا على مخرج المُرخَّص. فمقارنةُ الأضعف بمخرج المُرخَّص تجعل
المُرخَّصَ صائبًا بالتعريف، وهي أُسُّ التدوير.

**ولا حكمَ في هذه الوحدة**: `Registration != Reading`. لا تشغيلَ، ولا قراءةَ
مدوّنة، ولا استيرادَ من `kernel/`، ولا إصدارَ حكم.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from alghanem.canonical_content import canonical_bytes, canonical_digest

from .flt1_preregistration import (
    FLT1_FROZEN_SURFACES,
    FLT1_PREREGISTRATION_DIGEST,
    WEAKER_REPRESENTATIONS,
)
from .flt1_qiyas_law import FLT1_QIYAS_TEXT_DIGEST

__all__ = [
    "CONTINUITY_IS_NOT_BIRTH_NOTE",
    "DECISION_RULES",
    "FLT1_QIYAS_PREREGISTRATION_DIGEST",
    "FLT1_QIYAS_PREREGISTRATION_NAMED_RESIDUALS",
    "GATE_DECLARATIONS",
    "GREAT_CHAIN",
    "ORIGIN_DECLARATION",
    "PRECEDENCE_IS_PART_OF_THE_MACHINE_NOTE",
    "RECONSTRUCTION_TARGET",
    "THE_QADIH_DIFFERENCE_IS_TESTED_NOT_REQUIRED_NOTE",
    "THE_TARGET_IS_FROZEN_BEFORE_THE_SCORE_NOTE",
    "DecisionRule",
    "GateDeclaration",
    "HigherCenterStanding",
    "OriginDeclaration",
    "QiyasOutcome",
    "QiyasPreregistrationError",
    "ReconstructionTarget",
    "flt1_qiyas_preregistration_digest",
    "gate_named",
    "rule_for_gate",
]


class QiyasPreregistrationError(ValueError):
    """رفضٌ مُسمّى في تسجيل آلة القياس؛ لا تصحيحَ صامتًا ولا تخطّي."""


def _require_text(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise QiyasPreregistrationError(
            f"{field_name} نصٌّ غيرُ فارغ؛ وبندٌ فارغٌ ليس بندًا مُسجَّلًا"
        )
    return value


class QiyasOutcome(Enum):
    """مخرجاتُ آلة القرار؛ ستّةٌ مُسمّاةٌ في النصّ بأعيانها وسابعٌ مُشتَقٌّ منه.

    والسابعُ `FORMAL_DIFFERENCE_ONLY` ليس زيادةً على القانون بل موضعٌ يفرضه:
    النصُّ يقول `\\Delta_q(O,F)=1\\Rightarrow Q(O,F)=0`، ويقول إنّ الولادة
    المستقلّة لا تُرخَّص إلّا بفرقٍ **مؤثِّر** «لا مجرد اختلاف». فبين
    الاستمرار والولادة موضعٌ ثالثٌ لازمٌ: فرقٌ ثابتٌ لم يثبت تأثيرُه، فلا
    يستمرّ الحكمُ ولا تُرخَّص الولادة. وتسميتُه صراحةً تمنع أن يُدسّ في أحد
    البابين بلا حقّ.
    """

    BLOCK = "BLOCK"
    DEFER_OR_BLOCK = "DEFER/BLOCK"
    NO_EFFECTIVE_DESCRIPTION = "NO_EFFECTIVE_DESCRIPTION"
    NO_QIYAS = "NO_QIYAS"
    CONTINUITY_UNDER_ORIGIN = "CONTINUITY_UNDER_ORIGIN"
    INDEPENDENT_BRANCH_CANDIDATE = "INDEPENDENT_BRANCH_CANDIDATE"
    FORMAL_DIFFERENCE_ONLY = "FORMAL_DIFFERENCE_ONLY"


class HigherCenterStanding(Enum):
    """منزلةُ المركز الأعلى بعد آلة القرار؛ الاسمُ يُستحَقّ أو يُحجَب أو يَقصُر."""

    BORN = "وُلِد_مركزٌ_أعلى"
    WITHHELD = "حُجِب_الاسمُ_لسقوط_شرط"
    UNDERPOWERED = "قاصرٌ_لا_يُثبِت_ولا_يَنفي"


@dataclass(frozen=True, slots=True)
class GateDeclaration:
    """بوّابةٌ واحدةٌ من بوّابات التوقيع التسع، بما تقرؤه وما يُسقطها."""

    symbol: str
    arabic_name: str
    what_it_reads_in_this_deposit: str
    what_would_make_it_fail: str
    is_a_preventer: bool = False

    def __post_init__(self) -> None:
        _require_text(self.symbol, "رمزُ البوّابة")
        _require_text(self.arabic_name, "اسمُ البوّابة")
        _require_text(self.what_it_reads_in_this_deposit, "ما تقرؤه البوّابة")
        _require_text(self.what_would_make_it_fail, "ما يُسقط البوّابة")
        if not isinstance(self.is_a_preventer, bool):
            raise QiyasPreregistrationError("كونُ البوّابة مانعًا قيمةٌ ثنائيّة")

    def as_canonical_mapping(self) -> dict[str, str | bool]:
        """صورةٌ معياريّةٌ تدخل البصمة؛ بنيويّةٌ لا سلسلةٌ موصولة."""

        return {
            "symbol": self.symbol,
            "arabic_name": self.arabic_name,
            "what_it_reads_in_this_deposit": self.what_it_reads_in_this_deposit,
            "what_would_make_it_fail": self.what_would_make_it_fail,
            "is_a_preventer": self.is_a_preventer,
        }


GATE_DECLARATIONS: Final[tuple[GateDeclaration, ...]] = (
    GateDeclaration(
        symbol="Sh",
        arabic_name="الشرط",
        what_it_reads_in_this_deposit=(
            "أن تُقطَّع الصورةُ المُجمَّدةُ كلُّها بلا تعذّرٍ باقٍ؛ فالقراءةُ "
            "شرطُ كلّ ما بعدها، ولا يُقاس على صورةٍ لم تُقرَأ"
        ),
        what_would_make_it_fail="بقاءُ تعذّرٍ واحدٍ مُسمًّى في تقطيع الصورة",
    ),
    GateDeclaration(
        symbol="Sb",
        arabic_name="السبب",
        what_it_reads_in_this_deposit=(
            "أن يحمل الفرعُ المرشَّحُ نواةً واحدةً مسبوقةً بحاملٍ صامت؛ أي أن "
            "يكون فيه زوجُ حامل/حالةٍ فعلًا لا دعوى"
        ),
        what_would_make_it_fail="فرعٌ بلا نواة، أو نواةٌ بلا حاملٍ يسبقها",
    ),
    GateDeclaration(
        symbol="Mn",
        arabic_name="المانع",
        what_it_reads_in_this_deposit=(
            "وقوعُ وحدةٍ ذاتِ دورٍ صامتٍ أو مُدغَمٍ أو ألفٍ فارقةٍ داخل الفرع؛ "
            "فهذه مواضعُ لا يُبَتّ فيها من الصورة وحدَها"
        ),
        what_would_make_it_fail="حضورُ مانعٍ واحدٍ يكفي؛ ووجودُه يُبطِل لا يُخفِّف",
        is_a_preventer=True,
    ),
    GateDeclaration(
        symbol=r"w^\*",
        arabic_name="الوصفُ المؤثِّر",
        what_it_reads_in_this_deposit=(
            "أن يكون طولُ النواة وعددُ الصوامت المُغلِقة وصفًا **يُغيِّر** "
            "القالبَ عند تبديله؛ ويُفحَص بالتبديل المضادّ لا بالتسمية"
        ),
        what_would_make_it_fail=(
            "أن يُخرِج التبديلُ المضادُّ القالبَ نفسَه؛ فالوصفُ حينئذٍ غيرُ مؤثِّر"
        ),
    ),
    GateDeclaration(
        symbol=r"\mu",
        arabic_name="العلّةُ الجامعة",
        what_it_reads_in_this_deposit=(
            "أن يشترك الأصلُ والفرعُ في افتتاحٍ واحد: حاملٌ صامتٌ واحدٌ تليه "
            "نواةٌ؛ وهي علّةُ الولادة نفسُها في `H_B`"
        ),
        what_would_make_it_fail="فرعٌ لا يفتتح بحاملٍ صامتٍ تليه نواةٌ؛ فلا جامعَ فلا قياس",
    ),
    GateDeclaration(
        symbol=r"\Delta_q",
        arabic_name="الفرقُ القادح",
        what_it_reads_in_this_deposit=(
            "فرقٌ في شكل الشرائح بين الأصل والفرع: طولُ النواة أو عددُ "
            "الصوامت المُغلِقة. وفرقُ عين الحامل وحدَه اختلافٌ شكليٌّ لا يُعَدّ قادحًا"
        ),
        what_would_make_it_fail=(
            "ألّا يوجد فرقٌ في الشكل أصلًا؛ وحينئذٍ يستمرّ الحكمُ تحت الأصل"
        ),
    ),
    GateDeclaration(
        symbol="J",
        arabic_name="الوصلُ المُرخَّص",
        what_it_reads_in_this_deposit=(
            "أن يُبنى المقطعُ وصلًا لمراكزَ دنيا متجاورةٍ بترتيبها، وأن يكون "
            "الوصلُ هو ما أنتج القالبَ لا مجرّدَ مجاورة"
        ),
        what_would_make_it_fail="أن يُنتَج القالبُ نفسُه بلا وصلٍ؛ فالوصلُ زينةٌ لا شرط",
    ),
    GateDeclaration(
        symbol="I",
        arabic_name="حفظُ الهويّة",
        what_it_reads_in_this_deposit=(
            "أن تُعاد مواضعُ الوحدات الداخلةِ في الفرع بأعيانها وبترتيبها من "
            "الفرع نفسِه؛ وهو `I_O(F)`: أثرُ الأصل باقٍ في الفرع"
        ),
        what_would_make_it_fail="موضعٌ يسقط أو يُزاد أو يُقلَب ترتيبُه عند الاستخراج",
    ),
    GateDeclaration(
        symbol="Cl",
        arabic_name="الإغلاق",
        what_it_reads_in_this_deposit=(
            "أن يقع قالبُ الفرع في القوالب الستّة المُجمَّدة، وألّا يبقى في "
            "الصورة موضعٌ خارجَ مقاطعها"
        ),
        what_would_make_it_fail="قالبٌ خارج الستّة، أو موضعٌ في الصورة لا يقع في مقطع",
    ),
)


@dataclass(frozen=True, slots=True)
class DecisionRule:
    """قاعدةٌ واحدةٌ من آلة القرار: شرطُ إطلاقها، ومخرجُها، وموضعُها في الأسبقيّة."""

    order: int
    gate_symbol: str
    fires_when: str
    outcome: QiyasOutcome

    def __post_init__(self) -> None:
        if isinstance(self.order, bool) or not isinstance(self.order, int):
            raise QiyasPreregistrationError("موضعُ القاعدة في الأسبقيّة عددٌ صحيح")
        if self.order < 1:
            raise QiyasPreregistrationError("الأسبقيّةُ تبدأ من واحد")
        _require_text(self.gate_symbol, "رمزُ بوّابة القاعدة")
        _require_text(self.fires_when, "شرطُ إطلاق القاعدة")
        if not isinstance(self.outcome, QiyasOutcome):
            raise QiyasPreregistrationError("مخرجُ القاعدة عضوٌ في المفردة المغلقة")


DECISION_RULES: Final[tuple[DecisionRule, ...]] = (
    DecisionRule(
        order=1,
        gate_symbol="Sh",
        fires_when="Sh=0",
        outcome=QiyasOutcome.BLOCK,
    ),
    DecisionRule(
        order=2,
        gate_symbol="Sb",
        fires_when="Sb=0",
        outcome=QiyasOutcome.DEFER_OR_BLOCK,
    ),
    DecisionRule(
        order=3,
        gate_symbol="Mn",
        fires_when="Mn=1",
        outcome=QiyasOutcome.BLOCK,
    ),
    DecisionRule(
        order=4,
        gate_symbol=r"w^\*",
        fires_when=r"w^\*=0",
        outcome=QiyasOutcome.NO_EFFECTIVE_DESCRIPTION,
    ),
    DecisionRule(
        order=5,
        gate_symbol=r"\mu",
        fires_when=r"\mu=0",
        outcome=QiyasOutcome.NO_QIYAS,
    ),
    DecisionRule(
        order=6,
        gate_symbol=r"\Delta_q",
        fires_when=r"\Delta_q=0",
        outcome=QiyasOutcome.CONTINUITY_UNDER_ORIGIN,
    ),
    DecisionRule(
        order=7,
        gate_symbol=r"\Delta_q",
        fires_when=r"\Delta_q=1\ \land\ \neg\operatorname{Effective}(\Delta_q)",
        outcome=QiyasOutcome.FORMAL_DIFFERENCE_ONLY,
    ),
    DecisionRule(
        order=8,
        gate_symbol=r"\Delta_q",
        fires_when=r"\Delta_q^\*=1",
        outcome=QiyasOutcome.INDEPENDENT_BRANCH_CANDIDATE,
    ),
)


@dataclass(frozen=True, slots=True)
class OriginDeclaration:
    """الأصلُ مُعلَنٌ قبل التشغيل؛ ولا قياسَ بلا أصلٍ مُسمًّى قبل أن يُرى الفرع."""

    origin_id: str
    what_the_origin_is: str
    why_this_origin_and_not_another: str
    what_would_make_this_origin_illegitimate: str

    def __post_init__(self) -> None:
        _require_text(self.origin_id, "مُعرِّفُ الأصل")
        _require_text(self.what_the_origin_is, "ما هو الأصل")
        _require_text(self.why_this_origin_and_not_another, "لِمَ هذا الأصلُ دون غيره")
        _require_text(
            self.what_would_make_this_origin_illegitimate, "ما يُبطِل هذا الأصل"
        )


ORIGIN_DECLARATION: Final[OriginDeclaration] = OriginDeclaration(
    origin_id="CV-open-center",
    what_the_origin_is=(
        "المقطعُ المفتوحُ `CV`: حاملٌ صامتٌ واحدٌ تليه نواةٌ قصيرةٌ واحدة، وهو "
        "مخرجُ الولادة في `H_B` بعينه"
    ),
    why_this_origin_and_not_another=(
        "لأنّه أصغرُ ما يُخرِجه الربطُ المُرخَّص وحدَه، وكلُّ قالبٍ آخرَ من "
        "الستّة يزيد عليه زيادةً تُفحَص؛ فاتّخاذُه أصلًا يجعل الفرقَ مقيسًا "
        "لا مُدَّعًى"
    ),
    what_would_make_this_origin_illegitimate=(
        "أن يُرصَد قالبٌ في الستّة لا يزيد على `CV` ولا يساويه، فيكون `CV` "
        "غيرَ أصلٍ بل واحدًا من فروعٍ متوازية"
    ),
)


@dataclass(frozen=True, slots=True)
class ReconstructionTarget:
    """هدفُ إعادة البناء مُجمَّدًا قبل الرقم؛ عليه يُقاس المُرخَّصُ والأضعفُ سواء."""

    target_id: str
    what_must_be_reproduced: str
    how_a_hit_is_counted: str
    why_it_is_not_the_licensed_model_output: str
    tie_rule: str

    def __post_init__(self) -> None:
        _require_text(self.target_id, "مُعرِّفُ الهدف")
        _require_text(self.what_must_be_reproduced, "ما يجب إعادةُ إنتاجه")
        _require_text(self.how_a_hit_is_counted, "كيف تُعَدّ الإصابة")
        _require_text(
            self.why_it_is_not_the_licensed_model_output, "لِمَ الهدفُ ليس مخرجَ المُرخَّص"
        )
        _require_text(self.tie_rule, "حكمُ التساوي")


RECONSTRUCTION_TARGET: Final[ReconstructionTarget] = ReconstructionTarget(
    target_id="syllable-template-sequence",
    what_must_be_reproduced=(
        "سلسلةُ قوالب المقاطع للصورة المُجمَّدة بأعيانها وبترتيبها، مأخوذةً "
        "من تقطيعٍ مُجمَّدٍ سابقٍ لهذا التسجيل"
    ),
    how_a_hit_is_counted=(
        "إصابةٌ واحدةٌ لكلّ مقطعٍ أصاب النموذجُ قالبَه بعينه؛ ولا درجاتِ "
        "تقريبٍ ولا قالبَ «قريب»"
    ),
    why_it_is_not_the_licensed_model_output=(
        "لو قِيس الأضعفُ على مخرج المُرخَّص لكان المُرخَّصُ صائبًا بالتعريف "
        "وكانت المقارنةُ دائرةً على نفسها؛ فالهدفُ خارجٌ عن النموذجين معًا"
    ),
    tie_rule=(
        "التساوي يُسقِط الأدنويّة؛ ولا يُشترَط تفوّقُ الأضعف. ومساواةُ نموذجٍ "
        "أضعفَ تعني أنّ الربطَ المُرخَّص لم يُسهِم بشيء"
    ),
)

GREAT_CHAIN: Final[tuple[str, ...]] = (
    "Origin",
    "Effective Description",
    "Common Illah",
    "Qadih-Difference Test",
    "Condition",
    "Cause",
    "Preventer",
    "Licensed Join",
    "Identity",
    "Closure",
    "Higher Center",
)

PRECEDENCE_IS_PART_OF_THE_MACHINE_NOTE: Final[str] = (
    "PrecedenceIsPartOfTheMachine: قواعدُ آلة القرار مُرتَّبةٌ، وقراءةُ سطرٍ "
    "قبل سطرٍ تُبدِّل الحكم؛ فيُفحَص الترتيبُ عند الاستيراد لا يُوكَل إلى القاموس"
)

THE_QADIH_DIFFERENCE_IS_TESTED_NOT_REQUIRED_NOTE: Final[str] = (
    "TheQadihDifferenceIsTestedNotRequired: الفرقُ القادح مفحوصٌ لا مشروط؛ "
    "فانتفاؤه استمرارٌ تحت الأصل، وثبوتُه بلا تأثيرٍ اختلافٌ شكليٌّ، ولا "
    "يُرخِّص الولادةَ إلّا ثبوتُه مع تأثيره"
)

CONTINUITY_IS_NOT_BIRTH_NOTE: Final[str] = (
    "ContinuityIsNotBirth: `CONTINUITY_UNDER_ORIGIN` حكمٌ في بابٍ آخرَ لا "
    "درجةٌ أدنى من `INDEPENDENT_BRANCH_CANDIDATE`؛ ومَن عدّه فشلًا في الولادة "
    "خلط البابين"
)

THE_TARGET_IS_FROZEN_BEFORE_THE_SCORE_NOTE: Final[str] = (
    "TheTargetIsFrozenBeforeTheScore: هدفُ إعادة البناء خارجٌ عن النموذجين "
    "معًا؛ ولو قِيس الأضعفُ على مخرج المُرخَّص لدار الاختبارُ على نفسه"
)

FLT1_QIYAS_PREREGISTRATION_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    PRECEDENCE_IS_PART_OF_THE_MACHINE_NOTE,
    THE_QADIH_DIFFERENCE_IS_TESTED_NOT_REQUIRED_NOTE,
    CONTINUITY_IS_NOT_BIRTH_NOTE,
    THE_TARGET_IS_FROZEN_BEFORE_THE_SCORE_NOTE,
)


def gate_named(symbol: str) -> GateDeclaration:
    """أعِد البوّابةَ المُعلَنة برمزها؛ وغيرُ المُعلَنة تُرَدّ لا تُنشَأ."""

    for declaration in GATE_DECLARATIONS:
        if declaration.symbol == symbol:
            return declaration
    raise QiyasPreregistrationError(
        f"البوّابة «{symbol}» غيرُ مُعلَنةٍ قبل التشغيل، فلا تُقرأ بعده"
    )


def rule_for_gate(symbol: str) -> tuple[DecisionRule, ...]:
    """أعِد قواعدَ البوّابة بترتيب أسبقيّتها؛ وقد تكون لبوّابةٍ قواعدُ عدّة."""

    gate_named(symbol)
    return tuple(rule for rule in DECISION_RULES if rule.gate_symbol == symbol)


def flt1_qiyas_preregistration_digest() -> str:
    """اشتقّ بصمةَ التسجيل من بنيته كاملةً؛ ولا تُكتَب ثابتًا منقولًا."""

    payload = {
        "qiyas_text_digest": FLT1_QIYAS_TEXT_DIGEST,
        "flt1_preregistration_digest": FLT1_PREREGISTRATION_DIGEST,
        "gates": [gate.as_canonical_mapping() for gate in GATE_DECLARATIONS],
        "decision_rules": [
            {
                "order": rule.order,
                "gate_symbol": rule.gate_symbol,
                "fires_when": rule.fires_when,
                "outcome": rule.outcome.value,
            }
            for rule in DECISION_RULES
        ],
        "origin": {
            "origin_id": ORIGIN_DECLARATION.origin_id,
            "what_the_origin_is": ORIGIN_DECLARATION.what_the_origin_is,
            "why_this_origin_and_not_another": (
                ORIGIN_DECLARATION.why_this_origin_and_not_another
            ),
            "what_would_make_this_origin_illegitimate": (
                ORIGIN_DECLARATION.what_would_make_this_origin_illegitimate
            ),
        },
        "reconstruction_target": {
            "target_id": RECONSTRUCTION_TARGET.target_id,
            "what_must_be_reproduced": RECONSTRUCTION_TARGET.what_must_be_reproduced,
            "how_a_hit_is_counted": RECONSTRUCTION_TARGET.how_a_hit_is_counted,
            "why_it_is_not_the_licensed_model_output": (
                RECONSTRUCTION_TARGET.why_it_is_not_the_licensed_model_output
            ),
            "tie_rule": RECONSTRUCTION_TARGET.tie_rule,
        },
        "great_chain": list(GREAT_CHAIN),
        "weaker_representations": [item.model_id for item in WEAKER_REPRESENTATIONS],
        "frozen_surfaces": [item.surface for item in FLT1_FROZEN_SURFACES],
        "named_residuals": list(FLT1_QIYAS_PREREGISTRATION_NAMED_RESIDUALS),
    }
    return canonical_digest(canonical_bytes(payload))


FLT1_QIYAS_PREREGISTRATION_DIGEST: Final[str] = flt1_qiyas_preregistration_digest()


def _refuse_rules_out_of_declared_precedence() -> None:
    orders = [rule.order for rule in DECISION_RULES]
    if orders != sorted(orders) or orders != list(range(1, len(orders) + 1)):
        raise QiyasPreregistrationError(
            "قواعدُ آلة القرار تُودَع مُرتَّبةً بأسبقيّةٍ متّصلةٍ تبدأ من واحد"
        )


def _refuse_a_rule_on_an_undeclared_gate() -> None:
    symbols = {gate.symbol for gate in GATE_DECLARATIONS}
    unknown = sorted({rule.gate_symbol for rule in DECISION_RULES} - symbols)
    if unknown:
        raise QiyasPreregistrationError(
            f"قاعدةٌ على بوّابةٍ غيرِ مُعلَنة: {'، '.join(unknown)}"
        )


def _refuse_a_signature_missing_a_gate() -> None:
    required = {"Sh", "Sb", "Mn", r"w^\*", r"\mu", r"\Delta_q", "J", "I", "Cl"}
    declared = {gate.symbol for gate in GATE_DECLARATIONS}
    if declared != required:
        raise QiyasPreregistrationError(
            "توقيعُ الولادة تسعُ بوّاباتٍ بأعيانها؛ وناقصُها أو زائدُها توقيعٌ آخر"
        )


def _refuse_a_chain_out_of_the_frozen_order() -> None:
    if GREAT_CHAIN[0] != "Origin" or GREAT_CHAIN[-1] != "Higher Center":
        raise QiyasPreregistrationError(
            "السلسلةُ الكبرى تبدأ بالأصل وتنتهي بالمركز الأعلى؛ وغيرُ ذلك سلسلةٌ أخرى"
        )
    if GREAT_CHAIN.index("Closure") != GREAT_CHAIN.index("Higher Center") - 1:
        raise QiyasPreregistrationError("الإغلاقُ يسبق المركزَ الأعلى مباشرةً في النصّ")


_refuse_a_signature_missing_a_gate()
_refuse_rules_out_of_declared_precedence()
_refuse_a_rule_on_an_undeclared_gate()
_refuse_a_chain_out_of_the_frozen_order()
