"""G0.VV-BIRTH-1 — فضاءاتُ التجربة وفرضياتُها، مُصنَّفةً قبل أيّ تشغيل.

هذه الوحدةُ تحمل **الأجسامَ الرياضية** للتجربة القادمة: فضاءاتٌ مصنَّفةٌ صريحة،
وإسقاطان مُعرَّفان بدلالتهما، وفرضياتٌ كلُّ واحدةٍ بمُفنِّدها، ونماذجُ أضعفُ
تُشغَّل قبل أن يُدَّعى شيء. ولا تحمل نتيجةً واحدة: لا حقلَ فيها يُكتَب فيه حكم،
ولا تُصدِر `Outcome`، وحارسُ الاستيراد يمسح الحقولَ بأسمائها
(`NO_JUDGEMENT_IS_FROZEN_ONLY_ITS_CONDITIONS`).

**سبعةُ عيوبٍ منطقيةٍ أُغلقت هنا بالبناء لا بالوعد:**

* **«محايد» أقوى ممّا يُثبته حفظُ الهوية.** فُصلت فرضيتان: `H_E` تقول إنّ ثمّة
  مؤثّرًا `E` يحفظ `π_I` ويرفع `π_Q`، و`H_N` — وهي **أقوى ومستقلّة** — تقول إنّ
  `E` يُمثَّل فعلَ عنصرٍ محايدٍ بالنسبة إلى عمليةٍ ثنائيةٍ `⊗` وتكافؤٍ `∼_I`.
  و`NEUTRAL_ELEMENT_SUPPORTED` **غيرُ متاحةٍ أصلًا** ما لم تُعرَّف `⊗` و`∼_I`
  تعريفًا مُشغَّلًا (`NO_NEUTRALITY_WITHOUT_AN_OPERATION_AND_AN_EQUIVALENCE`).
* **`I` و`Q` كانا بلا فضاء، فكانت `I(VV)=I(V)` غيرَ قابلةٍ للتفنيد.** صار لكلٍّ
  منهما `ProjectionSpecification` تحمل مجالَه وما ينساه وما يُبطِله. و
  **`letter_index` ممنوعٌ بالاسم** أن يكون هويّةً صوتية: هو موضعٌ برمجيٌّ في
  `syllabifier.Slot`، ومن جعله هويّةً أثبت حفظَ الترقيم لا حفظَ الصوت
  (`A_PROGRAM_INDEX_IS_NOT_A_PHONETIC_IDENTITY`).
* **«`CV` و`CVV` مركزٌ واحد» حُسمت قبل قياسها.** صارتا فرضيتين متنافستين
  تُسجَّلان معًا ولا تُحسَم إحداهما هنا: `H_SAME_TYPE` مع اختلافِ الحالة، مقابل
  `H_DIFFERENT_TYPE`.
* **الإغلاقُ كان عضويّةً في جدول قوالب.** صار قانونَ خارجِ قسمةٍ يُشغَّل: لكلّ
  سياقٍ خارجيٍّ مرخَّصٍ `k` يلزم `Obs(k[g]) == Obs(k[π(g)])`، مع
  `NoCrossBoundaryActiveResidual`. وإن تعذّر اختبارُ السياقات فالنتيجةُ
  `BEHAVIORAL_CLOSURE_UNDERPOWERED`، ولا تنوب عنها عضويّةُ القالب
  (`MEMBERSHIP_IN_A_TEMPLATE_IS_NOT_BEHAVIOURAL_CLOSURE`).
* **الأثرُ قد يكون نسخةَ الجواب.** `TraceMinimalityCriterion` يشترط أن يُعيد
  `Audit(E(v), T)` الزوجَ `(v, e)` وأن **يفشل كلُّ `T' ⊊ T`**؛ فإن حمل الأثرُ
  الجوابَ كاملًا فالنتيجةُ `TRACE_TAUTOLOGY` ولا تُحتسَب إعادةُ بناء.
* **الهدفُ كان مُخرَجَ النموذج نفسِه.** `ReconstructionTarget` يحمل استقلالَه
  مُعلَّلًا؛ وكلُّ هدفٍ يستعمل قواعدَ النموذج المرشَّح **مُستبعَدٌ بالبناء**،
  ومنه `syllabifier` بعينه (`A_TARGET_MADE_BY_THE_MODEL_IS_NOT_A_TARGET`).
* **`BORN` كانت حكمًا قابلًا للإصدار من نجاح القالب.** حُذفت من المفردة رأسًا:
  أعلى ما تُصدِره هذه التجربةُ `CONDITIONAL_STRUCTURAL_BIRTH`، وسقفُها مكتوبٌ
  في `vv_birth_preregistration` بسببه.

**وثلاثةُ دعاوى مفصولةٌ لا تُجمَع:** `IDENTITY_PRESERVATION` و
`QUANTITY_TRANSFORMATION` و`HISTORICAL_RECOVERABILITY`؛ ونجاحُ الأولَيين لا
يُثبت الثالثة (`SUCCESS_IN_TWO_CLAIMS_IS_NOT_SUCCESS_IN_THE_THIRD`).

**ووسمُ `MADD_EXTENSION` ليس دليلًا على نفسه:** وجودُ اسمٍ في
`p_extractor.PhoneticRole` ملاحظةٌ على الرسم، لا برهانٌ على أنّ العملية محايدة
(`AN_OBSERVED_LABEL_IS_NOT_A_PROVED_NEUTRALITY`).

تسجيلٌ لا سلطة: لا ولادةَ ولا تجميدَ `E0` ولا حكم، ولا تستورد هذه الوحدةُ من
`kernel/` حرفًا، ولا تقرؤها وحدةٌ فيها.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

__all__ = [
    "A_PROGRAM_INDEX_IS_NOT_A_PHONETIC_IDENTITY",
    "AN_OBSERVED_LABEL_IS_NOT_A_PROVED_NEUTRALITY",
    "A_TARGET_MADE_BY_THE_MODEL_IS_NOT_A_TARGET",
    "BANNED_IDENTITY_PROXIES",
    "BEHAVIOURAL_CLOSURE_LAW",
    "COMPETING_TYPE_HYPOTHESES",
    "HYPOTHESES",
    "IDENTITY_PROJECTION",
    "LICENSED_JOIN_SPECIFICATION",
    "MEMBERSHIP_IN_A_TEMPLATE_IS_NOT_BEHAVIOURAL_CLOSURE",
    "NO_JUDGEMENT_IS_FROZEN_ONLY_ITS_CONDITIONS",
    "NO_NEUTRALITY_WITHOUT_AN_OPERATION_AND_AN_EQUIVALENCE",
    "QUANTITY_PROJECTION",
    "SEPARATED_CLAIMS",
    "SUCCESS_IN_TWO_CLAIMS_IS_NOT_SUCCESS_IN_THE_THIRD",
    "TRACE_MINIMALITY_CRITERION",
    "TYPED_SPACES",
    "WEAKER_MODELS",
    "BehaviouralClosureLaw",
    "ExperimentOutcome",
    "Hypothesis",
    "HypothesisIdentifier",
    "LicensedJoinSpecification",
    "ProjectionAxis",
    "ProjectionSpecification",
    "SeparatedClaim",
    "TraceMinimalityCriterion",
    "TypedSpace",
    "TypedSpaceIdentifier",
    "VvBirthHypothesisError",
    "WeakerModel",
    "WeakerModelRole",
    "hypothesis_named",
    "weaker_model_named",
]


class VvBirthHypothesisError(ValueError):
    """رفضٌ عند الإنشاء: حقلٌ فارغ، أو حكمٌ يُكتَب حيث لا يُكتَب إلّا شرطُه."""


# --- الفضاءاتُ المصنَّفة ----------------------------------------------------


class TypedSpaceIdentifier(Enum):
    """الفضاءاتُ الثلاثةُ بأسمائها؛ مفردةٌ مغلقةٌ لا رابعَ لها في هذه التجربة."""

    X_V = "X_V"
    X_C = "X_C"
    X_S = "X_S"


@dataclass(frozen=True, slots=True)
class TypedSpace:
    """فضاءٌ مصنَّفٌ واحد: ما عناصرُه، وما يُخرِجه منه، وما لا يُقال فيه."""

    identifier: TypedSpaceIdentifier
    elements: str
    membership_condition: str
    what_is_not_an_element: str

    def __post_init__(self) -> None:
        if not isinstance(self.identifier, TypedSpaceIdentifier):
            raise VvBirthHypothesisError("مُعرِّفُ الفضاء عضوٌ في مفردته المغلقة")
        for value, label in (
            (self.elements, "وصفُ العناصر"),
            (self.membership_condition, "شرطُ العضوية"),
            (self.what_is_not_an_element, "ما ليس عنصرًا"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise VvBirthHypothesisError(f"{label} نصٌّ غير فارغ")

    def as_canonical_content(self) -> dict[str, str]:
        """محتوى الفضاء للبصمة؛ الترتيبُ من المفتاح لا من الكتابة."""

        return {
            "identifier": self.identifier.value,
            "elements": self.elements,
            "membership_condition": self.membership_condition,
            "what_is_not_an_element": self.what_is_not_an_element,
        }


TYPED_SPACES: Final[tuple[TypedSpace, ...]] = (
    TypedSpace(
        identifier=TypedSpaceIdentifier.X_V,
        elements="مواضعُ الصائت: حالةٌ صائتةٌ على حاملٍ واحد، بامتدادها إن وُجد",
        membership_condition=(
            "أن تكون الحالةُ فتحةً أو ضمّةً أو كسرةً في "
            "`encoding.carrier_state_candidate.CarrierState`، مع صفرٍ أو أكثرَ "
            "من مواضع الامتداد التالية لها"
        ),
        what_is_not_an_element=(
            "الحرفُ المكتوبُ بذاته ليس عنصرًا: `ا` و`و` و`ي` رسومٌ قد تحمل "
            "امتدادًا وقد تكون صوامتَ، والتمييزُ بالحالة لا بالرسم"
        ),
    ),
    TypedSpace(
        identifier=TypedSpaceIdentifier.X_C,
        elements="مواضعُ الصامت: حاملٌ بحالةٍ غيرِ صائتة",
        membership_condition=(
            "أن تكون الحالةُ سكونًا صريحًا أو ضمنيًّا، أو شقًّا أوّلَ من شدّةٍ "
            "بـ`GeminationRole.PAIR_START`"
        ),
        what_is_not_an_element=(
            "نقطةُ ترميزٍ خارجَ مجموعة الحوامل المُعلَنة ليست عنصرًا؛ تخرج "
            "`PASSTHROUGH` ولا تُقحَم صامتًا"
        ),
    ),
    TypedSpace(
        identifier=TypedSpaceIdentifier.X_S,
        elements="نواتجُ الوصل المرخَّص: `S(c, v, q)` بكمّيّةٍ `q`",
        membership_condition=(
            "أن يكون الناتجُ صورةَ `J` على زوجٍ من `X_C × X_V` حيث `J` مُعرَّفة"
        ),
        what_is_not_an_element=(
            "اسمُ قالبٍ من `SyllableTemplate` ليس عنصرًا: القالبُ وسمٌ على "
            "الشكل، والعنصرُ ناتجُ عمليةٍ مُعرَّفة"
        ),
    ),
)
"""الفضاءاتُ الثلاثةُ مُعرَّفةً قبل أيّ تشغيل، وكلُّ واحدٍ بما يخرج عنه."""


# --- الإسقاطان -------------------------------------------------------------


class ProjectionAxis(Enum):
    """المحوران المستقلّان: هويّةٌ يُفترَض حفظُها، وكمّيّةٌ يُفترَض تغيّرُها."""

    IDENTITY = "π_I"
    QUANTITY = "π_Q"


BANNED_IDENTITY_PROXIES: Final[tuple[str, ...]] = (
    "carrier_codepoint",
    "letter_index",
    "slot_position",
    "surface_offset",
)
"""حواملُ ممنوعةٌ بالاسم أن تكون هويّةً صوتية؛ كلُّها مواضعُ برمجيّةٌ لا أصوات."""


@dataclass(frozen=True, slots=True)
class ProjectionSpecification:
    """إسقاطٌ واحد: مجالُه، وما يحفظه، وما ينساه، وما يجعله فارغَ المعنى."""

    axis: ProjectionAxis
    codomain: str
    what_it_keeps: str
    what_it_forgets: str
    what_would_make_it_vacuous: str
    banned_proxies: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.axis, ProjectionAxis):
            raise VvBirthHypothesisError("محورُ الإسقاط عضوٌ في مفردته المغلقة")
        for value, label in (
            (self.codomain, "مجالُ الإسقاط"),
            (self.what_it_keeps, "ما يحفظه"),
            (self.what_it_forgets, "ما ينساه"),
            (self.what_would_make_it_vacuous, "ما يجعله فارغَ المعنى"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise VvBirthHypothesisError(f"{label} نصٌّ غير فارغ")
        if not isinstance(self.banned_proxies, tuple) or not self.banned_proxies:
            raise VvBirthHypothesisError(
                "لكلّ إسقاطٍ حواملُ ممنوعةٌ مُسمّاة؛ والقائمةُ الفارغةُ إذنٌ مفتوح"
            )
        for proxy in self.banned_proxies:
            if proxy not in BANNED_IDENTITY_PROXIES:
                raise VvBirthHypothesisError(
                    f"الحاملُ الممنوع {proxy!r} يُسمّى في `BANNED_IDENTITY_PROXIES`"
                )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الإسقاط للبصمة."""

        return {
            "axis": self.axis.value,
            "codomain": self.codomain,
            "what_it_keeps": self.what_it_keeps,
            "what_it_forgets": self.what_it_forgets,
            "what_would_make_it_vacuous": self.what_would_make_it_vacuous,
            "banned_proxies": list(self.banned_proxies),
        }


IDENTITY_PROJECTION: Final[ProjectionSpecification] = ProjectionSpecification(
    axis=ProjectionAxis.IDENTITY,
    codomain=(
        "`𝓘` = مفردةٌ مغلقةٌ من ثلاث قيمٍ هي جودةُ الصائت " "{FATHA, DAMMA, KASRA}، لا أكثر"
    ),
    what_it_keeps="جودةَ الصائت وحدَها: أفتحةٌ هي أم ضمّةٌ أم كسرة",
    what_it_forgets=(
        "الطولَ، والرسمَ الذي تحقّق به الامتدادُ، وموضعَ الوحدة من الكلمة، "
        "ونقطةَ ترميز الحامل"
    ),
    what_would_make_it_vacuous=(
        "أن يُحسَب `π_I` من رسمِ الامتداد نفسِه: فيصير حفظُ الهوية لازمًا عن "
        "طريقة الحساب، وتصير `H_E` غيرَ قابلةٍ للتفنيد"
    ),
    banned_proxies=BANNED_IDENTITY_PROXIES,
)
"""`π_I` بمجالٍ ثلاثيٍّ مغلق؛ ولو اتّسع لغيرِ الجودة لصار حفظُه غيرَ ذي دلالة."""

QUANTITY_PROJECTION: Final[ProjectionSpecification] = ProjectionSpecification(
    axis=ProjectionAxis.QUANTITY,
    codomain=(
        "`𝓠` = `{1, 2}` عددًا صحيحًا يعدّ مواضعَ الصائت؛ **وليس زمنًا "
        "فيزيائيًّا بالثواني**، إذ لا قطعةَ في هذه الشجرة صوتٌ مُسجَّل"
    ),
    what_it_keeps="عددَ مواضع الصائت: واحدًا للقصير واثنين للممدود",
    what_it_forgets="جودةَ الصائت، وكلَّ ما يحفظه `π_I`",
    what_would_make_it_vacuous=(
        "أن يُقرأ `𝓠` مدّةً زمنيةً حقيقيةً: فتصير الدعوى عن النطق المسموع "
        "وهو خارجَ ما تقيسه هذه الشجرة رأسًا"
    ),
    banned_proxies=BANNED_IDENTITY_PROXIES,
)
"""`π_Q` عدّيٌّ لا زمنيّ؛ وهذا تصريحٌ بسقف الدعوى لا اختيارُ تبسيط."""


# --- الفرضيات --------------------------------------------------------------


class HypothesisIdentifier(Enum):
    """الفرضياتُ الخمس، كلٌّ تُختبَر وحدَها ولا يُقرأ نجاحُ إحداها نجاحَ أخرى."""

    H_E = "H_E"
    H_N = "H_N"
    H_S = "H_S"
    H_SAME_TYPE = "H_same_type"
    H_DIFFERENT_TYPE = "H_different_type"


class ExperimentOutcome(Enum):
    """حالاتُ المخرَج المُجمَّدةُ قبل التشغيل. **ولا `BORN` فيها البتّة.**"""

    PASS = "PASS"
    REFUTED = "REFUTED"
    UNDERPOWERED = "UNDERPOWERED"
    UNDEFINED = "UNDEFINED"
    CIRCULAR_TARGET = "CIRCULAR_TARGET"
    TRACE_TAUTOLOGY = "TRACE_TAUTOLOGY"
    WEAKER_MODEL_RECONSTRUCTS = "WEAKER_MODEL_RECONSTRUCTS"
    REPRESENTATION_LEAK = "REPRESENTATION_LEAK"
    INDEPENDENT_TARGET_MISSING = "INDEPENDENT_TARGET_MISSING"
    BEHAVIOURAL_CLOSURE_UNDERPOWERED = "BEHAVIOURAL_CLOSURE_UNDERPOWERED"
    CONDITIONAL_STRUCTURAL_BIRTH = "CONDITIONAL_STRUCTURAL_BIRTH"


@dataclass(frozen=True, slots=True)
class Hypothesis:
    """فرضيةٌ واحدة: نصُّها، ومُفنِّدُها المستقلّ، وما يُشترَط قبل اختبارها.

    ولا حقلَ للنتيجة: `admissible_outcomes` مفردةُ ما **قد** يخرج، لا ما خرج؛
    وحارسُ الاستيراد يمنع أن يُضاف حقلٌ يحمل حكمًا.
    """

    identifier: HypothesisIdentifier
    statement: str
    independent_falsifier: str
    precondition: str
    admissible_outcomes: tuple[ExperimentOutcome, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.identifier, HypothesisIdentifier):
            raise VvBirthHypothesisError("مُعرِّفُ الفرضية عضوٌ في مفردته المغلقة")
        for value, label in (
            (self.statement, "نصُّ الفرضية"),
            (self.independent_falsifier, "المُفنِّدُ المستقلّ"),
            (self.precondition, "شرطُ ما قبل الاختبار"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise VvBirthHypothesisError(f"{label} نصٌّ غير فارغ")
        if (
            not isinstance(self.admissible_outcomes, tuple)
            or len(self.admissible_outcomes) < 2
        ):
            raise VvBirthHypothesisError(
                "فرضيةٌ بمخرَجٍ واحدٍ مقبولٍ محسومةٌ بتعريفها؛ فالمقبولُ اثنان فأكثر"
            )
        for outcome in self.admissible_outcomes:
            if not isinstance(outcome, ExperimentOutcome):
                raise VvBirthHypothesisError("المخرَجُ المقبولُ عضوٌ في مفردته المغلقة")
        if ExperimentOutcome.REFUTED not in self.admissible_outcomes:
            raise VvBirthHypothesisError(
                "فرضيةٌ لا يجوز تفنيدُها ليست فرضيةً؛ `REFUTED` لازمةٌ في المقبول"
            )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الفرضية للبصمة."""

        return {
            "identifier": self.identifier.value,
            "statement": self.statement,
            "independent_falsifier": self.independent_falsifier,
            "precondition": self.precondition,
            "admissible_outcomes": [
                outcome.value for outcome in self.admissible_outcomes
            ],
        }


_COMMON_OUTCOMES: Final[tuple[ExperimentOutcome, ...]] = (
    ExperimentOutcome.PASS,
    ExperimentOutcome.REFUTED,
    ExperimentOutcome.UNDERPOWERED,
    ExperimentOutcome.UNDEFINED,
)


HYPOTHESES: Final[tuple[Hypothesis, ...]] = (
    Hypothesis(
        identifier=HypothesisIdentifier.H_E,
        statement=(
            "توجد دالّةٌ جزئيّةٌ `E: X_V ⇀ X_V` بحيث متى كان الامتدادُ مرخَّصًا "
            "كان `π_I(E(v)) = π_I(v)` و`π_Q(E(v)) > π_Q(v)`"
        ),
        independent_falsifier=(
            "موضعٌ واحدٌ مرخَّصٌ يخرج فيه `π_I(E(v)) ≠ π_I(v)`، أو لا يزيد فيه "
            "`π_Q`؛ فيُسجَّل `REFUTED` ولا يُضيَّق نطاقُ الترخيص بعد رؤيته"
        ),
        precondition=(
            "أن يكون `π_I` مُشغَّلًا من الحالة لا من رسم الامتداد، وإلّا فحفظُ "
            "الهوية لازمٌ عن الحساب فتخرج `UNDEFINED`"
        ),
        admissible_outcomes=_COMMON_OUTCOMES + (ExperimentOutcome.REPRESENTATION_LEAK,),
    ),
    Hypothesis(
        identifier=HypothesisIdentifier.H_N,
        statement=(
            "توجد عمليةٌ ثنائيةٌ `⊗` وعنصرٌ `e` وعلاقةُ تكافؤٍ `∼_I` بحيث "
            "`v ⊗ e ∼_I v` و`v ⊗ e = E(v)`؛ فيصير الحيادُ حيادًا بخارج قسمة"
        ),
        independent_falsifier=(
            "أن يُبنى `⊗` فيلزم منه `v ⊗ e ≠ E(v)` على موضعٍ واحد، أو أن تكون "
            "`∼_I` غيرَ متعديّةٍ فلا تكون تكافؤًا أصلًا"
        ),
        precondition=(
            "تعريفُ `⊗` و`∼_I` تعريفًا مُشغَّلًا قبل القراءة؛ وما لم يُعرَّفا "
            "فالمخرَجُ `UNDEFINED` ولا يُقال «محايد» بحال"
        ),
        admissible_outcomes=_COMMON_OUTCOMES,
    ),
    Hypothesis(
        identifier=HypothesisIdentifier.H_S,
        statement=(
            "الوصلُ المرخَّصُ `J(c, v_q)` يُنتج `S(c, v, q)` بكمّيّةٍ "
            "`q ∈ {1, 2}`، ولا يُعيد بناءَ سلوكِه نموذجٌ أضعف"
        ),
        independent_falsifier=(
            "نموذجٌ أضعفُ واحدٌ يبلغ الهدفَ المستقلَّ نفسَه؛ فيُسجَّل "
            "`WEAKER_MODEL_RECONSTRUCTS` وتسقط دعوى الولادة"
        ),
        precondition=(
            "هدفُ إعادةِ بناءٍ مستقلٌّ عن قواعد النموذج المرشَّح؛ وإلّا "
            "فـ`INDEPENDENT_TARGET_MISSING` ولا يُستبدَل بمُخرَج `syllabifier`"
        ),
        admissible_outcomes=_COMMON_OUTCOMES
        + (
            ExperimentOutcome.CIRCULAR_TARGET,
            ExperimentOutcome.INDEPENDENT_TARGET_MISSING,
            ExperimentOutcome.WEAKER_MODEL_RECONSTRUCTS,
            ExperimentOutcome.TRACE_TAUTOLOGY,
            ExperimentOutcome.BEHAVIOURAL_CLOSURE_UNDERPOWERED,
            ExperimentOutcome.CONDITIONAL_STRUCTURAL_BIRTH,
        ),
    ),
    Hypothesis(
        identifier=HypothesisIdentifier.H_SAME_TYPE,
        statement=(
            "`Type(CV) = Type(CVV)` مع `State(CV) ≠ State(CVV)`: نوعٌ مقطعيٌّ "
            "واحدٌ بحالتَي كمّيّة"
        ),
        independent_falsifier=(
            "سياقٌ خارجيٌّ مرخَّصٌ واحدٌ يفرّق بين `CV` و`CVV` تفريقًا لا " "تفسّره الكمّيّةُ وحدَها"
        ),
        precondition=(
            "أن يكون ثمّة سياقٌ خارجيٌّ يُشغَّل أصلًا؛ وإلّا فالمخرَجُ " "`UNDERPOWERED` لا `PASS`"
        ),
        admissible_outcomes=_COMMON_OUTCOMES
        + (ExperimentOutcome.BEHAVIOURAL_CLOSURE_UNDERPOWERED,),
    ),
    Hypothesis(
        identifier=HypothesisIdentifier.H_DIFFERENT_TYPE,
        statement="`Type(CV) ≠ Type(CVV)`: نوعان مقطعيّان مستقلّان",
        independent_falsifier=(
            "انعدامُ سياقٍ خارجيٍّ يفرّق بينهما تفريقًا لا تفسّره الكمّيّة، مع "
            "قدرةِ `S(c, v, q)` على توليد الشكلين بتغيير `q` وحدَه"
        ),
        precondition="الشرطُ نفسُه المكتوبُ لـ`H_SAME_TYPE`، فهما تُقاسان معًا",
        admissible_outcomes=_COMMON_OUTCOMES
        + (ExperimentOutcome.BEHAVIOURAL_CLOSURE_UNDERPOWERED,),
    ),
)
"""الفرضياتُ الخمسُ بمُفنِّداتها؛ ولا تُحسَم المتنافستان في هذا التسجيل."""


COMPETING_TYPE_HYPOTHESES: Final[tuple[HypothesisIdentifier, HypothesisIdentifier]] = (
    HypothesisIdentifier.H_SAME_TYPE,
    HypothesisIdentifier.H_DIFFERENT_TYPE,
)
"""المتنافستان مُسمّاتان معًا، كي يستحيل أن تُقرأ إحداهما مُجمَّدةً دون ضدّها."""


def hypothesis_named(identifier: HypothesisIdentifier) -> Hypothesis:
    """الفرضيةُ بمُعرِّفها؛ ولا مُعرِّفَ خارجَ المفردة المغلقة."""

    for hypothesis in HYPOTHESES:
        if hypothesis.identifier is identifier:
            return hypothesis
    raise VvBirthHypothesisError(f"لا فرضيةَ بالمُعرِّف {identifier!r}")


# --- الوصلُ المرخَّص ---------------------------------------------------------


@dataclass(frozen=True, slots=True)
class LicensedJoinSpecification:
    """`J: X_C × X_V ⇀ X_S` عمليةٌ جزئيّةٌ مصنَّفة، لا اسمٌ يُعلَّق على تجاور."""

    domain: str
    codomain: str
    definedness_conditions: tuple[str, ...]
    undefinedness_conditions: tuple[str, ...]
    why_partiality_is_not_a_defect: str

    def __post_init__(self) -> None:
        for value, label in (
            (self.domain, "مجالُ الوصل"),
            (self.codomain, "مجالُ الصورة"),
            (self.why_partiality_is_not_a_defect, "لماذا الجزئيّةُ ليست نقصًا"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise VvBirthHypothesisError(f"{label} نصٌّ غير فارغ")
        for conditions, label in (
            (self.definedness_conditions, "شروطُ التعريف"),
            (self.undefinedness_conditions, "موانعُ التعريف"),
        ):
            if not isinstance(conditions, tuple) or not conditions:
                raise VvBirthHypothesisError(f"{label} غيرُ خالية")
            for condition in conditions:
                if not isinstance(condition, str) or not condition.strip():
                    raise VvBirthHypothesisError(f"بندٌ في {label} نصٌّ غير فارغ")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الوصل للبصمة."""

        return {
            "domain": self.domain,
            "codomain": self.codomain,
            "definedness_conditions": list(self.definedness_conditions),
            "undefinedness_conditions": list(self.undefinedness_conditions),
            "why_partiality_is_not_a_defect": self.why_partiality_is_not_a_defect,
        }


LICENSED_JOIN_SPECIFICATION: Final[LicensedJoinSpecification] = (
    LicensedJoinSpecification(
        domain="`X_C × X_V`",
        codomain="`X_S`",
        definedness_conditions=(
            "الصامتُ يسبق الصائتَ في التسلسل المقروء، بلا فاصلٍ بينهما",
            "الصائتُ يحمل كمّيّةً في `{1, 2}` مُشتقّةً من `π_Q` لا مكتوبةً",
            "الصامتُ ليس شقًّا ثانيًا من شدّةٍ سبق أن وُصل",
        ),
        undefinedness_conditions=(
            "صائتٌ بلا صامتٍ قبله: `J` غيرُ مُعرَّفة، ولا يُصطنَع لها صامتٌ صفريّ",
            "صامتان متواليان: غيرُ مُعرَّفة، ولا يُقرَّب الشكلُ إلى أقرب قالب",
            "كمّيّةٌ خارجَ `{1, 2}`: غيرُ مُعرَّفة، فيخرج `UNDEFINED` لا خطأٌ صامت",
        ),
        why_partiality_is_not_a_defect=(
            "دالّةٌ كلّيّةٌ على كلّ زوجٍ تُنتج مقطعًا من كلّ تجاور، فتصير "
            "`CLOSURE` لازمةً عن الكلّيّة لا نتيجةً عن البنية؛ فالجزئيّةُ هي ما "
            "يجعل الإغلاقَ قابلًا للفشل"
        ),
    )
)
"""الوصلُ مُعرَّفٌ بشروطه وموانعه معًا؛ وموانعُه هي ما يجعل نجاحَه ذا معنى."""


# --- قانونُ الإغلاق ---------------------------------------------------------


@dataclass(frozen=True, slots=True)
class BehaviouralClosureLaw:
    """الإغلاقُ خارجُ قسمةٍ يحفظ السلوكَ الخارجيّ، لا عضويّةٌ في جدول قوالب."""

    quotient_law: str
    observation_relation: str
    residual_condition: str
    underpowered_outcome: ExperimentOutcome
    what_does_not_substitute_for_it: str

    def __post_init__(self) -> None:
        for value, label in (
            (self.quotient_law, "قانونُ خارج القسمة"),
            (self.observation_relation, "علاقةُ المشاهدة"),
            (self.residual_condition, "شرطُ البقيّة"),
            (self.what_does_not_substitute_for_it, "ما لا ينوب عنه"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise VvBirthHypothesisError(f"{label} نصٌّ غير فارغ")
        if self.underpowered_outcome is not (
            ExperimentOutcome.BEHAVIOURAL_CLOSURE_UNDERPOWERED
        ):
            raise VvBirthHypothesisError(
                "تعذّرُ اختبارِ السياقات يخرج `BEHAVIOURAL_CLOSURE_UNDERPOWERED`"
            )

    def as_canonical_content(self) -> dict[str, str]:
        """محتوى القانون للبصمة."""

        return {
            "quotient_law": self.quotient_law,
            "observation_relation": self.observation_relation,
            "residual_condition": self.residual_condition,
            "underpowered_outcome": self.underpowered_outcome.value,
            "what_does_not_substitute_for_it": self.what_does_not_substitute_for_it,
        }


BEHAVIOURAL_CLOSURE_LAW: Final[BehaviouralClosureLaw] = BehaviouralClosureLaw(
    quotient_law=(
        "يوجد `π: g → s` بحيث لكلّ سياقٍ خارجيٍّ مرخَّصٍ `k ∈ K_allowed` يكون "
        "`Obs(k[g]) = Obs(k[π(g)])`؛ أي يُستبدَل التركيبُ الداخليُّ بالمركز "
        "في كلّ سياقٍ مرخَّصٍ بلا فقدِ سلوكٍ ذي صلة"
    ),
    observation_relation=(
        "`Obs` تُعرَّف قبل التشغيل على المشاهَد وحدَه، ولا تُوسَّع بعد رؤية " "أوّل سياقٍ يفرّق"
    ),
    residual_condition=(
        "`NoCrossBoundaryActiveResidual`: لا بقيّةَ فاعلةٌ تعبر حدَّ المركز؛ "
        "وبقيّةٌ عابرةٌ واحدةٌ تُسقط الإغلاق"
    ),
    underpowered_outcome=ExperimentOutcome.BEHAVIOURAL_CLOSURE_UNDERPOWERED,
    what_does_not_substitute_for_it=(
        "عضويّةُ الناتج في `SyllableTemplate` لا تنوب عن الإغلاق: الجدولُ "
        "يصف شكلًا، والإغلاقُ يصف سلوكًا في سياق"
    ),
)
"""قانونُ الإغلاق مكتوبًا قبل أن يُقاس، وبنصّ ما لا ينوب عنه."""


# --- أدنويّةُ الأثر ----------------------------------------------------------


@dataclass(frozen=True, slots=True)
class TraceMinimalityCriterion:
    """معيارُ أنّ الأثرَ معلومةٌ مختصرةٌ جديدة، لا نسخةٌ من المُدخَل المخفيّ."""

    audit_law: str
    minimality_law: str
    tautology_outcome: ExperimentOutcome
    why_a_copy_is_not_a_reconstruction: str

    def __post_init__(self) -> None:
        for value, label in (
            (self.audit_law, "قانونُ التدقيق"),
            (self.minimality_law, "قانونُ الأدنويّة"),
            (self.why_a_copy_is_not_a_reconstruction, "لماذا النسخُ ليس إعادةَ بناء"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise VvBirthHypothesisError(f"{label} نصٌّ غير فارغ")
        if self.tautology_outcome is not ExperimentOutcome.TRACE_TAUTOLOGY:
            raise VvBirthHypothesisError("أثرٌ يحمل الجوابَ يخرج `TRACE_TAUTOLOGY`")

    def as_canonical_content(self) -> dict[str, str]:
        """محتوى المعيار للبصمة."""

        return {
            "audit_law": self.audit_law,
            "minimality_law": self.minimality_law,
            "tautology_outcome": self.tautology_outcome.value,
            "why_a_copy_is_not_a_reconstruction": (
                self.why_a_copy_is_not_a_reconstruction
            ),
        }


TRACE_MINIMALITY_CRITERION: Final[TraceMinimalityCriterion] = TraceMinimalityCriterion(
    audit_law="`Audit(E(v), T) = (v, e)`: التدقيقُ يُعيد الأصلَ والامتداد",
    minimality_law=(
        "`∀ T' ⊊ T: Audit(E(v), T') ≠ (v, e)`؛ يُشغَّل على كلّ أجزاء `T` "
        "الحقيقيّة لا على جزءٍ مختارٍ منها"
    ),
    tautology_outcome=ExperimentOutcome.TRACE_TAUTOLOGY,
    why_a_copy_is_not_a_reconstruction=(
        "إن كان `T` تسلسلًا للمُدخَل الأصليّ فـ`ضغط + أثر` هو في الحقيقة "
        "`تخزينُ المُدخَل`؛ ونجاحُ التدقيق حينئذٍ نجاحُ القراءة من مخزن"
    ),
)
"""أدنويّةُ الأثر مُجمَّدةً قبل بناء أيّ أثر، فلا تُفصَّل على أثرٍ بعد كتابته."""


# --- النماذجُ الأضعف --------------------------------------------------------


class WeakerModelRole(Enum):
    """دورُ النموذج: أهو منافسٌ يُسقط الدعوى، أم مقياسُ تسريبٍ لا يُحتَجّ به؟"""

    RIVAL = "منافسٌ يُسقط دعوى الولادة إن بلغ الهدف"
    LEAKAGE_BASELINE = "مقياسُ تسريبٍ هوياتيّ، لا يُحتسَب دليلًا بحال"


@dataclass(frozen=True, slots=True)
class WeakerModel:
    """نموذجٌ أضعفُ واحد: ما يراه، وما يفتقده، وماذا يعني بلوغُه الهدف."""

    name: str
    what_it_sees: str
    what_it_lacks: str
    what_its_success_means: str
    role: WeakerModelRole

    def __post_init__(self) -> None:
        for value, label in (
            (self.name, "اسمُ النموذج"),
            (self.what_it_sees, "ما يراه"),
            (self.what_it_lacks, "ما يفتقده"),
            (self.what_its_success_means, "معنى بلوغِه الهدف"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise VvBirthHypothesisError(f"{label} نصٌّ غير فارغ")
        if not isinstance(self.role, WeakerModelRole):
            raise VvBirthHypothesisError("دورُ النموذج عضوٌ في مفردته المغلقة")

    @property
    def counts_as_evidence(self) -> bool:
        """أيُحتَجّ ببلوغه؟ مُشتقٌّ من دوره، ولا يُكتَب في حقلٍ على حدة."""

        return self.role is WeakerModelRole.RIVAL

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى النموذج للبصمة."""

        return {
            "name": self.name,
            "what_it_sees": self.what_it_sees,
            "what_it_lacks": self.what_it_lacks,
            "what_its_success_means": self.what_its_success_means,
            "role": self.role.value,
        }


WEAKER_MODELS: Final[tuple[WeakerModel, ...]] = (
    WeakerModel(
        name="M_drop",
        what_it_sees="الصوائتَ والصوامتَ بترتيبها",
        what_it_lacks="أثرَ الامتداد: يُسقطه فيعيد `VV → V`",
        what_its_success_means=(
            "بلوغُه الهدفَ يعني أنّ الامتدادَ لا يُضيف سلوكًا خارجيًّا، فدعوى "
            "`H_E` عن الكمّيّة بلا أثرٍ يُقاس"
        ),
        role=WeakerModelRole.RIVAL,
    ),
    WeakerModel(
        name="M_consonant",
        what_it_sees="التسلسلَ نفسَه",
        what_it_lacks="تمييزَ حاملِ المدّ: يعامله صامتًا مستقلًّا",
        what_its_success_means=(
            "بلوغُه يعني أنّ «حرفَ المدّ» لا يلزم أن يكون امتدادًا أصلًا، "
            "فتسقط الحاجةُ إلى `E`"
        ),
        role=WeakerModelRole.RIVAL,
    ),
    WeakerModel(
        name="M_second_vowel",
        what_it_sees="التسلسلَ نفسَه",
        what_it_lacks="وحدةَ الصائت: يعامل الامتدادَ صائتًا ثانيًا مستقلًّا",
        what_its_success_means=(
            "بلوغُه يعني أنّ `S(c, v, 2)` ليست حالةً ثانيةً لمركزٍ واحد بل "
            "تعاقبَ مركزين، فيرجّح `H_different_type`"
        ),
        role=WeakerModelRole.RIVAL,
    ),
    WeakerModel(
        name="M_no_join",
        what_it_sees="الصامتَ والصائتَ وترتيبَهما",
        what_it_lacks="عمليةَ `LicensedJoin`: لا يملك وصلًا مُعرَّفًا",
        what_its_success_means=(
            "بلوغُه يعني أنّ الوصلَ اسمٌ على تجاورٍ لا عمليةٌ تُضيف شيئًا، "
            "فتسقط دعوى الولادة بـ`WEAKER_MODEL_RECONSTRUCTS`"
        ),
        role=WeakerModelRole.RIVAL,
    ),
    WeakerModel(
        name="M_identity_lookup",
        what_it_sees="اسمَ الحرف ورمزَه المكتوب، بترخيصٍ صريح",
        what_it_lacks="أيَّ بنيةٍ سوى جدولِ بحثٍ على الهوية",
        what_its_success_means=(
            "بلوغُه **لا يُحتَجّ به دليلًا**: وظيفتُه قياسُ ما يُنال بالتسريب "
            "الهوياتيّ وحدَه؛ وما بلغه هو الحدُّ الذي يجب أن يتجاوزه المرشَّح"
        ),
        role=WeakerModelRole.LEAKAGE_BASELINE,
    ),
)
"""أربعةُ منافسين ومقياسُ تسريبٍ واحد، مُجمَّدةً قبل بناء النموذج المرشَّح."""


def weaker_model_named(name: str) -> WeakerModel:
    """النموذجُ الأضعفُ باسمه؛ ولا اسمَ خارجَ المُجمَّد."""

    for model in WEAKER_MODELS:
        if model.name == name:
            return model
    raise VvBirthHypothesisError(f"لا نموذجَ أضعفَ باسم {name!r}")


# --- الدعاوى المفصولة -------------------------------------------------------


@dataclass(frozen=True, slots=True)
class SeparatedClaim:
    """دعوى واحدةٌ مفصولة: ما تقوله، وما لا يُقرأ من نجاحها."""

    name: str
    statement: str
    what_its_success_does_not_prove: str

    def __post_init__(self) -> None:
        for value, label in (
            (self.name, "اسمُ الدعوى"),
            (self.statement, "نصُّ الدعوى"),
            (self.what_its_success_does_not_prove, "ما لا يُثبته نجاحُها"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise VvBirthHypothesisError(f"{label} نصٌّ غير فارغ")

    def as_canonical_content(self) -> dict[str, str]:
        """محتوى الدعوى للبصمة."""

        return {
            "name": self.name,
            "statement": self.statement,
            "what_its_success_does_not_prove": self.what_its_success_does_not_prove,
        }


SEPARATED_CLAIMS: Final[tuple[SeparatedClaim, ...]] = (
    SeparatedClaim(
        name="IDENTITY_PRESERVATION",
        statement="`π_I(E(v)) = π_I(v)` على كلّ موضعٍ مرخَّص",
        what_its_success_does_not_prove=(
            "لا يُثبت وجودَ عنصرٍ محايد: الحيادُ يلزمه `⊗` و`∼_I` معًا"
        ),
    ),
    SeparatedClaim(
        name="QUANTITY_TRANSFORMATION",
        statement="`π_Q(E(v)) > π_Q(v)` على كلّ موضعٍ مرخَّص",
        what_its_success_does_not_prove=(
            "لا يُثبت أنّ الفرقَ زمنٌ منطوق: `𝓠` عدّيٌّ لا زمنيّ في هذه الشجرة"
        ),
    ),
    SeparatedClaim(
        name="HISTORICAL_RECOVERABILITY",
        statement="`Audit(E(v), T) = (v, e)` بأثرٍ أدنى غيرِ حاملٍ للجواب",
        what_its_success_does_not_prove=(
            "لا يُثبته نجاحُ الدعوَيين قبله: حفظُ الهوية وتغيّرُ الكمّيّة لا "
            "يستلزمان استرجاعَ التاريخ، والعكسُ كذلك"
        ),
    ),
)
"""الدعاوى الثلاثُ مفصولةً، وكلٌّ بنصّ ما لا يُقرأ من نجاحها."""


# --- البواقي المُسمّاة -------------------------------------------------------


NO_JUDGEMENT_IS_FROZEN_ONLY_ITS_CONDITIONS: Final[str] = (
    "NoJudgementIsFrozenOnlyItsConditions: لا حكمَ في هذا التسجيل؛ المُجمَّدُ "
    "شرطُ الحكم ومُفنِّدُه، ومن جمّد المخرَجَ قبل التشغيل كتب النتيجةَ فرضيّة"
)

NO_NEUTRALITY_WITHOUT_AN_OPERATION_AND_AN_EQUIVALENCE: Final[str] = (
    "NoNeutralityWithoutAnOperationAndAnEquivalence: حفظُ الهوية مؤثّرٌ لا "
    "عنصرٌ محايد؛ و`NEUTRAL_ELEMENT_SUPPORTED` غيرُ متاحةٍ ما لم تُعرَّف `⊗` "
    "و`∼_I` تعريفًا مُشغَّلًا يُثبت `v ⊗ e ∼_I v` و`v ⊗ e = E(v)`"
)

A_PROGRAM_INDEX_IS_NOT_A_PHONETIC_IDENTITY: Final[str] = (
    "AProgramIndexIsNotAPhoneticIdentity: `letter_index` في "
    "`syllabifier.Slot` موضعٌ في مصفوفة، لا هويّةٌ صوتية؛ ومن حفِظه ادّعى حفظَ "
    "الترقيم وسمّاه حفظَ الصوت"
)

A_TARGET_MADE_BY_THE_MODEL_IS_NOT_A_TARGET: Final[str] = (
    "ATargetMadeByTheModelIsNotATarget: هدفٌ يُنتجه النموذجُ المرشَّحُ أو "
    "تُنتجه دالّةٌ بقواعده يجعل النتيجةَ واحدًا بالبناء؛ فيخرج `CIRCULAR_TARGET`"
)

MEMBERSHIP_IN_A_TEMPLATE_IS_NOT_BEHAVIOURAL_CLOSURE: Final[str] = (
    "MembershipInATemplateIsNotBehaviouralClosure: وقوعُ الناتج في `CV/CVV` "
    "وصفُ شكلٍ لا حفظُ سلوك؛ وتعذّرُ السياقات يخرج "
    "`BEHAVIOURAL_CLOSURE_UNDERPOWERED` ولا يُعوَّض بعضويّةٍ في جدول"
)

SUCCESS_IN_TWO_CLAIMS_IS_NOT_SUCCESS_IN_THE_THIRD: Final[str] = (
    "SuccessInTwoClaimsIsNotSuccessInTheThird: حفظُ الهوية وتغيّرُ الكمّيّة "
    "دعويان لا تستلزمان استرجاعَ التاريخ؛ وجمعُها في عبارةٍ واحدةٍ يُمرِّر "
    "الثالثةَ بنجاح الأولَيين"
)

AN_OBSERVED_LABEL_IS_NOT_A_PROVED_NEUTRALITY: Final[str] = (
    "AnObservedLabelIsNotAProvedNeutrality: `PhoneticRole.MADD_EXTENSION` وسمٌ "
    "يُعلَّق بقاعدةٍ على العلامات المكتوبة؛ ووجودُ الوسم مشاهدةٌ على الرسم لا "
    "برهانٌ على أنّ العملية محايدة"
)


_FORBIDDEN_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "outcome_value",
    "verdict",
    "birth",
    "born",
    "result",
    "score",
    "supported",
    "refuted",
    "measured",
    "e0",
)


def _refuse_a_judgement_written_as_a_condition() -> None:
    """حارسٌ عند الاستيراد: لا حقلَ يحمل حكمًا، ولا فرضيةَ بلا مُفنِّد."""

    for declaring_type in (
        TypedSpace,
        ProjectionSpecification,
        Hypothesis,
        LicensedJoinSpecification,
        BehaviouralClosureLaw,
        TraceMinimalityCriterion,
        WeakerModel,
        SeparatedClaim,
    ):
        declared = {item.name for item in fields(declaring_type)}
        for marker in _FORBIDDEN_FIELD_MARKERS:
            if any(marker in name for name in declared):
                raise VvBirthHypothesisError(
                    f"حقلُ {marker!r} حكمٌ لا شرط، فلا يكون في تسجيلٍ قبليّ"
                )
    if {space.identifier for space in TYPED_SPACES} != set(TypedSpaceIdentifier):
        raise VvBirthHypothesisError("الفضاءاتُ الثلاثةُ تُعرَّف كلُّها قبل التشغيل")
    if {hypothesis.identifier for hypothesis in HYPOTHESES} != set(
        HypothesisIdentifier
    ):
        raise VvBirthHypothesisError("كلُّ فرضيةٍ في المفردة تُجمَّد بمُفنِّدها")
    if any(
        outcome.value == "BORN" or outcome.name == "BORN"
        for outcome in ExperimentOutcome
    ):
        raise VvBirthHypothesisError("`BORN` ليست حالةً يُصدِرها نجاحُ قالب")
    names = [model.name for model in WEAKER_MODELS]
    if len(set(names)) != len(names):
        raise VvBirthHypothesisError("نموذجٌ أضعفُ تكرّر باسمه")
    rivals = [model for model in WEAKER_MODELS if model.counts_as_evidence]
    if len(rivals) < 4:
        raise VvBirthHypothesisError("المنافسون أربعةٌ فأكثرُ قبل أيّ دعوى ولادة")
    if not any(
        model.role is WeakerModelRole.LEAKAGE_BASELINE for model in WEAKER_MODELS
    ):
        raise VvBirthHypothesisError("مقياسُ التسريب الهوياتيّ لازمٌ في المُجمَّد")
    claim_names = [claim.name for claim in SEPARATED_CLAIMS]
    if claim_names != [
        "IDENTITY_PRESERVATION",
        "QUANTITY_TRANSFORMATION",
        "HISTORICAL_RECOVERABILITY",
    ]:
        raise VvBirthHypothesisError("الدعاوى الثلاثُ مفصولةٌ بأسمائها وترتيبها")


_refuse_a_judgement_written_as_a_condition()
