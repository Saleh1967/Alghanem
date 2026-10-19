"""G0.VV-BIRTH-1 — التسجيلُ القبليّ، مختومًا قبل أن تُقرأ بايتةٌ واحدة.

هذه الوحدةُ **الالتزامُ الأوّل** من التزامين تاريخيين متمايزين. فيها التجميدُ
وحدَه، ولا قراءةَ فيها ولا تشغيل، ولا وجودَ لوحدةٍ باسم `vv_birth_readout` في
هذا الالتزام — وهو ما يفحصه اختبارٌ بالاسم لا بالوعد
(`THE_READOUT_DOES_NOT_EXIST_IN_THIS_COMMIT`).

**العيبُ الذي نبّه إليه النقدُ وأُغلق هنا:** فحصُ الأمانة كان **تحصيلَ حاصل**.
حين تُشتَقّ `REQUIRED_NOTATION_SITES` من نصّ المُجمَّد نفسِه، ثمّ يُفحَص أنّ كلّ
موقعٍ مطلوبٍ موجودٌ في النصّ، يكون المفحوصُ `x ∈ X ⇒ x ∈ X`؛ وبندٌ يُحذَف من
النصّ يُحذَف معه من قائمة المطلوب فلا يُكتشَف. فالقائمةُ هنا **مكتوبةٌ بيدٍ،
مستقلّةٌ عن النصّ**، وتُقابَل بالأسماء المُصدَّرة فعلًا من الوحدتين: من حذف بندًا
سقط اسمُه فسقط الاستيراد (`THE_SITE_LIST_IS_INDEPENDENT_NOT_DERIVED`).

**وحدُّ ما تبلغه هذه الوحدةُ من الختم مُصرَّحٌ به لا مُدَّعًى:** بصمةٌ تُعاد
اشتقاقُها من محتوى المُجمَّد تكشف تغيّرًا **بين التزامين**، ولا تكشف تحريرًا
يُغيّر النصَّ والبصمةَ في التزامٍ واحد. والختمُ التجريبيُّ الحقيقيُّ حدُّه
حدُّ التاريخ: `prereg_commit ≺ readout_commit`، والقراءةُ هي التي تحمل
`prereg_commit_sha` و`expected_digest` وتمتنع عن التشغيل عند عدم المطابقة
(`A_SELF_RECOMPUTED_DIGEST_IS_NOT_A_SEAL`). ولا تحمل هذه الوحدةُ بصمةَ التزامها
لأنّ ذلك مستحيلٌ بنيويًّا: المحتوى يدخل في البصمة قبل أن تُحسَب
(`A_COMMIT_CANNOT_CONTAIN_ITS_OWN_SHA`).

**وثلاثُ حقائقَ عن الشجرة مُودَعةٌ هنا لأنّها ضدّ التجربة لا معها** — وتجميدُ ما
يضرّ بالدعوى قبل التشغيل لا يُحابيها:

* **لا هدفَ مستقلٌّ في الشجرة اليوم.** `syllabifier` مُستبعَدٌ بالبناء لأنّه
  يستعمل قواعدَ النموذج المرشَّح نفسِها، و`p_extractor` كذلك. فسقفُ `H_S` اليوم
  `INDEPENDENT_TARGET_MISSING`، ولا يُستبدَل الهدفُ بمُخرَج الأداة.
* **لا شهادةَ ولادةٍ لـ`C` ولا لـ`V`.** فأعلى ما يُصدَر — لو نجحت كلُّ اختبارات
  المقطع — `CONDITIONAL_STRUCTURAL_BIRTH`، و`FULL_CONSTITUTIONAL_BIRTH` **غيرُ
  قابلةٍ للإصدار** من هذه التجربة بحال.
* **التحقّقُ الصوتيُّ الفيزيائيُّ محجوزٌ بحجزٍ قائم.** `UnicodeIsNotRecordedSound`
  في `epistemic_layers` نافذ: لا قطعةَ هنا صوتٌ مُسجَّل. فـ
  `PHYSICAL_PHONETIC_VERIFICATION = UNDERPOWERED` مكتوبةٌ قبل التشغيل، وسقفُ
  دعوى الاختبار الجبريّ `MODEL_THEORETIC_SUPPORT` لا تحقّقًا صوتيًّا.

**وملاحظةٌ لازمة:** النقدُ الذي وُلِّد عنه هذا التسجيل يُحيل إلى وحدةٍ باسم
`vv_neutral_birth_freeze.py`، **ولا وجودَ لها في هذه الشجرة ولا في تاريخها
المتاح**. فلم يُبنَ هنا شيءٌ على محتواها، ولم تُنسَخ منها عبارة؛ وما استُفيد هو
أجناسُ العيوب لا نصوصُها (`THE_CITED_FREEZE_IS_ABSENT_FROM_THIS_TREE`).

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولا تجميدَ `E0`، ولا استيرادَ من `kernel/`.
"""

from __future__ import annotations

import importlib.util
from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from alghanem.canonical_content import canonical_bytes, canonical_digest

from .vv_birth_hypothesis import (
    BEHAVIOURAL_CLOSURE_LAW,
    HYPOTHESES,
    IDENTITY_PROJECTION,
    LICENSED_JOIN_SPECIFICATION,
    QUANTITY_PROJECTION,
    SEPARATED_CLAIMS,
    TRACE_MINIMALITY_CRITERION,
    TYPED_SPACES,
    WEAKER_MODELS,
    ExperimentOutcome,
    HypothesisIdentifier,
)

__all__ = [
    "A_COMMIT_CANNOT_CONTAIN_ITS_OWN_SHA",
    "A_SELF_RECOMPUTED_DIGEST_IS_NOT_A_SEAL",
    "ADVERSE_TREE_FACTS",
    "EXPERIMENT_ID",
    "NO_SOURCE_IS_IMPORTED_AFTER_THE_RESULT_IS_SEEN",
    "OUTCOME_CEILINGS",
    "PREREGISTRATION_DIGEST",
    "READOUT_MODULE_NAME",
    "READOUT_SEAL_CONTRACT",
    "RECONSTRUCTION_TARGET_ASSESSMENTS",
    "REQUIRED_NOTATION_SITES",
    "THE_CITED_FREEZE_IS_ABSENT_FROM_THIS_TREE",
    "THE_READOUT_DOES_NOT_EXIST_IN_THIS_COMMIT",
    "THE_SITE_LIST_IS_INDEPENDENT_NOT_DERIVED",
    "THIS_IS_REGISTRATION_NOT_AUTHORITY",
    "VV_BIRTH_PREREGISTRATION_NAMED_RESIDUALS",
    "AdverseTreeFact",
    "OutcomeCeiling",
    "ReadoutSealContract",
    "ReconstructionTargetAssessment",
    "TargetIndependence",
    "VvBirthPreregistrationError",
    "ceiling_for",
    "missing_notation_sites",
    "preregistration_digest",
    "readout_module_is_absent",
    "target_assessment_named",
]


class VvBirthPreregistrationError(ValueError):
    """رفضٌ عند الاستيراد أو الإنشاء: موقعُ دلالةٍ ساقط، أو ختمٌ يُدَّعى ولا يقوم."""


EXPERIMENT_ID: Final[str] = "G0.VV-BIRTH-1"
"""مُعرِّفُ التجربة: الامتدادُ الحافظُ للهوية وولادةُ المقطع."""

READOUT_MODULE_NAME: Final[str] = "alghanem.arabic.vv_birth_readout"
"""اسمُ وحدة القراءة، مُسمًّى هنا كي يُفحَص **انعدامُها** في هذا الالتزام."""


# --- مواقعُ الدلالة: قائمةٌ مستقلّةٌ مكتوبةٌ بيد ----------------------------


REQUIRED_NOTATION_SITES: Final[tuple[tuple[str, str], ...]] = (
    ("vv_birth_hypothesis", "TYPED_SPACES"),
    ("vv_birth_hypothesis", "IDENTITY_PROJECTION"),
    ("vv_birth_hypothesis", "QUANTITY_PROJECTION"),
    ("vv_birth_hypothesis", "BANNED_IDENTITY_PROXIES"),
    ("vv_birth_hypothesis", "HYPOTHESES"),
    ("vv_birth_hypothesis", "COMPETING_TYPE_HYPOTHESES"),
    ("vv_birth_hypothesis", "LICENSED_JOIN_SPECIFICATION"),
    ("vv_birth_hypothesis", "BEHAVIOURAL_CLOSURE_LAW"),
    ("vv_birth_hypothesis", "TRACE_MINIMALITY_CRITERION"),
    ("vv_birth_hypothesis", "WEAKER_MODELS"),
    ("vv_birth_hypothesis", "SEPARATED_CLAIMS"),
    ("vv_birth_hypothesis", "ExperimentOutcome"),
    ("vv_birth_preregistration", "ADVERSE_TREE_FACTS"),
    ("vv_birth_preregistration", "OUTCOME_CEILINGS"),
    ("vv_birth_preregistration", "RECONSTRUCTION_TARGET_ASSESSMENTS"),
    ("vv_birth_preregistration", "READOUT_SEAL_CONTRACT"),
    ("vv_birth_preregistration", "PREREGISTRATION_DIGEST"),
)
"""المواقعُ التي **يجب** أن تبقى في المُجمَّد، مكتوبةً بيدٍ لا مشتقّةً من نصّه.

هذه هي النقطةُ التي كان فحصُ الأمانة يسقط عندها: لو اشتُقّت هذه القائمةُ من
النصّ لَحُذف البندُ منها كلّما حُذف من النصّ، فما كُشِف حذفٌ قطّ. وهي هنا ثابتةٌ
تُقابَل بما هو مُصدَّرٌ فعلًا، فحذفُ بندٍ يُسقِط الاستيراد.
"""


def missing_notation_sites() -> tuple[tuple[str, str], ...]:
    """المواقعُ المطلوبةُ الغائبةُ فعلًا، مُشتقّةً بالتشغيل لا بالادّعاء."""

    missing: list[tuple[str, str]] = []
    for module_name, site in REQUIRED_NOTATION_SITES:
        module = importlib.import_module(f".{module_name}", __package__)
        if not hasattr(module, site):
            missing.append((module_name, site))
        elif site not in getattr(module, "__all__", ()):
            missing.append((module_name, site))
    return tuple(missing)


# --- حقائقُ الشجرة الضارّةُ بالدعوى، مُودَعةً قبل التشغيل -------------------


@dataclass(frozen=True, slots=True)
class AdverseTreeFact:
    """حقيقةٌ قائمةٌ في الشجرة تضيّق على التجربة، مُودَعةٌ قبل أن تُقاس."""

    name: str
    statement: str
    grounds: str
    what_it_forbids: str

    def __post_init__(self) -> None:
        for value, label in (
            (self.name, "اسمُ الحقيقة"),
            (self.statement, "نصُّها"),
            (self.grounds, "سندُها في الشجرة"),
            (self.what_it_forbids, "ما تمنعه"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise VvBirthPreregistrationError(f"{label} نصٌّ غير فارغ")

    def as_canonical_content(self) -> dict[str, str]:
        """محتوى الحقيقة للبصمة."""

        return {
            "name": self.name,
            "statement": self.statement,
            "grounds": self.grounds,
            "what_it_forbids": self.what_it_forbids,
        }


ADVERSE_TREE_FACTS: Final[tuple[AdverseTreeFact, ...]] = (
    AdverseTreeFact(
        name="NO_BIRTH_CERTIFICATE_FOR_C_OR_V",
        statement="لا شهادةَ ولادةٍ مستقلّةٍ لـ`C` ولا لـ`V` في هذه الشجرة",
        grounds=(
            "`kernel/birth.py` يقف عند `BirthAssessmentRequest` مُصادَقٍ عليه، "
            "و`BirthGate` مؤجَّلةٌ إلى G0.2؛ فلا جهةَ تُصدِر شهادةً أصلًا"
        ),
        what_it_forbids=(
            "إصدارَ `FULL_CONSTITUTIONAL_BIRTH` من هذه التجربة ولو نجحت كلُّ "
            "اختبارات المقطع"
        ),
    ),
    AdverseTreeFact(
        name="NO_RECORDED_SOUND_IN_THIS_TREE",
        statement="لا قطعةَ في هذا المستودع صوتٌ مُسجَّل؛ ما فيه نقاطُ ترميز",
        grounds=(
            "`epistemic_layers.UnicodeIsNotRecordedSound`: الطبقةُ الفيزيائيةُ "
            "مُعلَنةٌ وغيرُ قابلةٍ للبناء من أيّ قطعةٍ هنا"
        ),
        what_it_forbids=(
            "قراءةَ `𝓠` مدّةً زمنيةً منطوقة، ورفعَ أيّ نتيجةٍ بنيويةٍ إلى "
            "حقيقةٍ عن العربية المسموعة"
        ),
    ),
    AdverseTreeFact(
        name="NO_INDEPENDENT_RECONSTRUCTION_TARGET",
        statement="لا هدفَ إعادةِ بناءٍ مستقلٌّ عن قواعد النموذج المرشَّح اليوم",
        grounds=(
            "`syllabifier` يبني المقاطعَ بقواعد `syllable_preregistration` "
            "نفسِها، و`p_extractor` يُعلِّق `MADD_EXTENSION` بقاعدةٍ من جنس "
            "ما يُختبَر؛ فكلاهما مُخرَجُ النموذج لا شاهدٌ عليه"
        ),
        what_it_forbids=(
            "قياسَ `H_S` على مُخرَج الأداة؛ والمخرَجُ عند غياب الهدف "
            "`INDEPENDENT_TARGET_MISSING` لا `PASS`"
        ),
    ),
    AdverseTreeFact(
        name="THE_MADD_LABEL_IS_A_RULE_OUTPUT",
        statement="`PhoneticRole.MADD_EXTENSION` ناتجُ قاعدةٍ مكتوبة، لا مشاهدة",
        grounds=(
            "`p_extractor._apply_madd_extension` يُعلِّق الوسمَ عند مطابقة "
            "`_MADD_PARTNERS` لحالةِ ما قبلَه؛ فهو تطبيقُ قاعدةٍ على الرسم"
        ),
        what_it_forbids=(
            "أن يُحتَجّ بوجود الوسم على أنّ العملية محايدة؛ فُصِل "
            "`ObservedMaddRole` عن `NeutralExtensionHypothesis`"
        ),
    ),
)
"""أربعُ حقائقَ تضيّق على الدعوى، مُودَعةٌ قبل التشغيل لا مُكتشَفةٌ بعد فشلها."""


# --- سقوفُ المخرَج ----------------------------------------------------------


@dataclass(frozen=True, slots=True)
class OutcomeCeiling:
    """سقفُ ما تُصدِره فرضيةٌ اليوم، وسببُه، وما يرفعه غدًا."""

    hypothesis: HypothesisIdentifier
    ceiling: ExperimentOutcome
    grounds: str
    what_would_raise_it: str

    def __post_init__(self) -> None:
        if not isinstance(self.hypothesis, HypothesisIdentifier):
            raise VvBirthPreregistrationError("الفرضيةُ عضوٌ في مفردتها المغلقة")
        if not isinstance(self.ceiling, ExperimentOutcome):
            raise VvBirthPreregistrationError("السقفُ عضوٌ في مفردة المخرَج المغلقة")
        for value, label in (
            (self.grounds, "سببُ السقف"),
            (self.what_would_raise_it, "ما يرفع السقف"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise VvBirthPreregistrationError(f"{label} نصٌّ غير فارغ")
        for hypothesis in HYPOTHESES:
            if hypothesis.identifier is self.hypothesis:
                if self.ceiling not in hypothesis.admissible_outcomes:
                    raise VvBirthPreregistrationError(
                        "سقفُ الفرضية عضوٌ في مخرَجاتها المقبولة، وإلّا فهو حكمٌ دخيل"
                    )
                return
        raise VvBirthPreregistrationError("سقفٌ لفرضيةٍ غيرِ مُجمَّدة")

    def as_canonical_content(self) -> dict[str, str]:
        """محتوى السقف للبصمة."""

        return {
            "hypothesis": self.hypothesis.value,
            "ceiling": self.ceiling.value,
            "grounds": self.grounds,
            "what_would_raise_it": self.what_would_raise_it,
        }


OUTCOME_CEILINGS: Final[tuple[OutcomeCeiling, ...]] = (
    OutcomeCeiling(
        hypothesis=HypothesisIdentifier.H_S,
        ceiling=ExperimentOutcome.CONDITIONAL_STRUCTURAL_BIRTH,
        grounds=(
            "`NO_BIRTH_CERTIFICATE_FOR_C_OR_V`: ما لم يُولَد الطرفان لم يُولَد "
            "المركّبُ منهما إلّا شرطًا"
        ),
        what_would_raise_it=(
            "شهادتان مستقلّتان تُثبتان `Born(C)` و`Born(V)` من أثرٍ فيزيائيّ، "
            "وسلطةُ ولادةٍ قائمةٌ تُصدِرهما"
        ),
    ),
    OutcomeCeiling(
        hypothesis=HypothesisIdentifier.H_N,
        ceiling=ExperimentOutcome.UNDEFINED,
        grounds=(
            "`⊗` و`∼_I` غيرُ مُعرَّفتين في هذه الشجرة اليوم، و"
            "`NO_NEUTRALITY_WITHOUT_AN_OPERATION_AND_AN_EQUIVALENCE` يمنع "
            "الحكمَ قبل تعريفهما"
        ),
        what_would_raise_it=(
            "تعريفٌ مُشغَّلٌ لـ`⊗` و`∼_I` يُبرهَن عليه أنّ `∼_I` تكافؤٌ فعلًا "
            "(انعكاسٌ وتماثلٌ وتعدٍّ)، لا علاقةٌ تُسمّى تكافؤًا"
        ),
    ),
)
"""سقفان مكتوبان قبل التشغيل؛ وما لا سقفَ له يُقرأ من مخرَجات فرضيته وحدَها."""


def ceiling_for(hypothesis: HypothesisIdentifier) -> OutcomeCeiling | None:
    """سقفُ الفرضية إن كان لها سقفٌ مكتوب، وإلّا `None` صريحًا لا ضمنًا."""

    for ceiling in OUTCOME_CEILINGS:
        if ceiling.hypothesis is hypothesis:
            return ceiling
    return None


# --- أهدافُ إعادة البناء واستقلالُها ----------------------------------------


class TargetIndependence(Enum):
    """استقلالُ الهدف عن النموذج المرشَّح: مفردةٌ مغلقةٌ لا درجاتٌ بينها."""

    INDEPENDENT = "مستقلٌّ عن قواعد النموذج المرشَّح"
    DISQUALIFIED_SHARES_THE_MODEL_RULES = "مُستبعَدٌ: يستعمل قواعدَ النموذج نفسَها"
    DISQUALIFIED_NOT_PRESENT = "مُستبعَدٌ: غيرُ موجودٍ في الشجرة"


@dataclass(frozen=True, slots=True)
class ReconstructionTargetAssessment:
    """تقييمُ مرشَّحٍ للهدف: أمستقلٌّ هو، وبأيّ سندٍ حُكم عليه."""

    name: str
    independence: TargetIndependence
    grounds: str

    def __post_init__(self) -> None:
        for value, label in ((self.name, "اسمُ الهدف"), (self.grounds, "سندُ الحكم")):
            if not isinstance(value, str) or not value.strip():
                raise VvBirthPreregistrationError(f"{label} نصٌّ غير فارغ")
        if not isinstance(self.independence, TargetIndependence):
            raise VvBirthPreregistrationError("الاستقلالُ عضوٌ في مفردته المغلقة")

    @property
    def is_usable(self) -> bool:
        """أيصلح هدفًا؟ مُشتقٌّ من استقلاله، ولا يُكتَب في حقلٍ على حدة."""

        return self.independence is TargetIndependence.INDEPENDENT

    def as_canonical_content(self) -> dict[str, str]:
        """محتوى التقييم للبصمة."""

        return {
            "name": self.name,
            "independence": self.independence.value,
            "grounds": self.grounds,
        }


RECONSTRUCTION_TARGET_ASSESSMENTS: Final[tuple[ReconstructionTargetAssessment, ...]] = (
    ReconstructionTargetAssessment(
        name="alghanem.arabic.syllabifier",
        independence=TargetIndependence.DISQUALIFIED_SHARES_THE_MODEL_RULES,
        grounds=(
            "يُقطِّع بالقوالب الستّة المُجمَّدة في `syllable_preregistration`، "
            "وهي عينُ ما تدّعيه `H_S`؛ فقياسُ النموذج عليه "
            "`Target = ModelOutput` ودرجتُه واحدٌ بالبناء"
        ),
    ),
    ReconstructionTargetAssessment(
        name="alghanem.arabic.p_extractor",
        independence=TargetIndependence.DISQUALIFIED_SHARES_THE_MODEL_RULES,
        grounds=(
            "`_apply_madd_extension` يُعلِّق `MADD_EXTENSION` بقاعدةٍ من جنس "
            "القاعدة المُختبَرة، فوسمُه مُخرَجُ النموذج لا شاهدٌ عليه"
        ),
    ),
    ReconstructionTargetAssessment(
        name="مدوّنةٌ مقطّعةٌ بيدٍ بشريّةٍ قبل بناء النموذج",
        independence=TargetIndependence.DISQUALIFIED_NOT_PRESENT,
        grounds=(
            "لا مدوّنةَ من هذا الجنس في الشجرة؛ ولا تُستورَد بعد رؤية النتيجة "
            "(`NO_SOURCE_IS_IMPORTED_AFTER_THE_RESULT_IS_SEEN`)"
        ),
    ),
)
"""ثلاثةُ مرشَّحين، ولا مستقلَّ فيهم؛ فالسقفُ اليوم `INDEPENDENT_TARGET_MISSING`."""


def target_assessment_named(name: str) -> ReconstructionTargetAssessment:
    """تقييمُ الهدف باسمه؛ ولا اسمَ خارجَ المُجمَّد."""

    for assessment in RECONSTRUCTION_TARGET_ASSESSMENTS:
        if assessment.name == name:
            return assessment
    raise VvBirthPreregistrationError(f"لا هدفَ مُقيَّمٌ باسم {name!r}")


# --- عقدُ ختمِ القراءة ------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ReadoutSealContract:
    """ما يجب أن تحمله وحدةُ القراءة في الالتزام التالي، وما يمنعها من التشغيل."""

    required_readout_fields: tuple[str, ...]
    refusal_condition: str
    why_this_module_carries_no_commit_sha: str
    what_this_digest_does_not_detect: str

    def __post_init__(self) -> None:
        if (
            not isinstance(self.required_readout_fields, tuple)
            or len(self.required_readout_fields) < 2
        ):
            raise VvBirthPreregistrationError(
                "عقدُ الختم يُلزِم القراءةَ بحقلَين فأكثر: بصمةٌ والتزامٌ سابق"
            )
        for field_name in self.required_readout_fields:
            if not isinstance(field_name, str) or not field_name.strip():
                raise VvBirthPreregistrationError("اسمُ الحقل المُلزَم نصٌّ غير فارغ")
        for value, label in (
            (self.refusal_condition, "شرطُ الامتناع"),
            (
                self.why_this_module_carries_no_commit_sha,
                "لماذا لا تحمل هذه الوحدةُ بصمةَ التزامها",
            ),
            (self.what_this_digest_does_not_detect, "ما لا تكشفه البصمة"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise VvBirthPreregistrationError(f"{label} نصٌّ غير فارغ")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى العقد للبصمة."""

        return {
            "required_readout_fields": list(self.required_readout_fields),
            "refusal_condition": self.refusal_condition,
            "why_this_module_carries_no_commit_sha": (
                self.why_this_module_carries_no_commit_sha
            ),
            "what_this_digest_does_not_detect": self.what_this_digest_does_not_detect,
        }


READOUT_SEAL_CONTRACT: Final[ReadoutSealContract] = ReadoutSealContract(
    required_readout_fields=("prereg_commit_sha", "expected_preregistration_digest"),
    refusal_condition=(
        "تمتنع القراءةُ عن التشغيل إن لم يطابق `expected_preregistration_digest` "
        "البصمةَ المُعادَ اشتقاقُها من هذا المُجمَّد، أو إن لم يكن "
        "`prereg_commit_sha` سلفًا للالتزام الذي تقع فيه القراءة"
    ),
    why_this_module_carries_no_commit_sha=(
        "بصمةُ الالتزام تُحسَب على محتواه، والمحتوى يشمل هذا الملفّ؛ فكتابةُ "
        "بصمةِ الالتزام فيه دورٌ مستحيلٌ بنيويًّا لا اختيارٌ يُترَك"
    ),
    what_this_digest_does_not_detect=(
        "تحريرًا يُغيّر النصَّ والبصمةَ في التزامٍ واحد: هذه البصمةُ تكشف "
        "التغيّرَ بين التزامين لا داخلَ التزامٍ واحد، والفصلُ التاريخيُّ وحدَه "
        "هو ما يجعلها ختمًا"
    ),
)
"""عقدُ الختم: القراءةُ تحمل السلفَ وبصمتَه، وهذه الوحدةُ لا تدّعي ختمَ نفسها."""


def readout_module_is_absent() -> bool:
    """أغائبةٌ وحدةُ القراءةُ فعلًا؟ مُشتقٌّ بالبحث عنها لا بالتصريح."""

    return importlib.util.find_spec(READOUT_MODULE_NAME) is None


# --- البواقي المُسمّاة -------------------------------------------------------


THE_SITE_LIST_IS_INDEPENDENT_NOT_DERIVED: Final[str] = (
    "TheSiteListIsIndependentNotDerived: `REQUIRED_NOTATION_SITES` مكتوبةٌ "
    "بيدٍ ومستقلّةٌ عن نصّ المُجمَّد؛ ولو اشتُقّت منه لكان الفحصُ `x ∈ X ⇒ "
    "x ∈ X`، فما كشف حذفَ بندٍ قطّ"
)

A_SELF_RECOMPUTED_DIGEST_IS_NOT_A_SEAL: Final[str] = (
    "ASelfRecomputedDigestIsNotASeal: بصمةٌ تُعاد من النصّ الجاري تكشف "
    "التغيّرَ بين التزامين لا داخلَ التزام؛ والختمُ التجريبيُّ حدُّه "
    "`prereg_commit ≺ readout_commit` مع حملِ القراءة سلفَها وبصمتَه"
)

A_COMMIT_CANNOT_CONTAIN_ITS_OWN_SHA: Final[str] = (
    "ACommitCannotContainItsOwnSha: بصمةُ الالتزام تُحسَب على محتواه، فكتابتُها "
    "فيه دورٌ مستحيل؛ ومن كتب بصمةً في الملفّ المُبصَّم كتب رقمًا لا ختمًا"
)

THE_READOUT_DOES_NOT_EXIST_IN_THIS_COMMIT: Final[str] = (
    "TheReadoutDoesNotExistInThisCommit: الالتزامُ الأوّلُ تجميدٌ بلا قراءة؛ "
    "و`vv_birth_readout` معدومةٌ هنا، يفحص انعدامَها اختبارٌ بالاسم"
)

THE_CITED_FREEZE_IS_ABSENT_FROM_THIS_TREE: Final[str] = (
    "TheCitedFreezeIsAbsentFromThisTree: `vv_neutral_birth_freeze.py` المُحال "
    "إليها في النقد لا وجودَ لها في هذه الشجرة ولا في تاريخها المتاح؛ فلم "
    "يُبنَ على محتواها شيء، والمُستفادُ أجناسُ العيوب لا نصوصُها"
)

NO_SOURCE_IS_IMPORTED_AFTER_THE_RESULT_IS_SEEN: Final[str] = (
    "NoSourceIsImportedAfterTheResultIsSeen: عند غياب البيانات المستقلّة "
    "يُصرَّح بالغياب ولا يُستورَد مصدرٌ بعد رؤية النتيجة؛ فالاستيرادُ حينئذٍ "
    "اختيارٌ للشاهد على مقاس الجواب"
)

THIS_IS_REGISTRATION_NOT_AUTHORITY: Final[str] = (
    "ThisIsRegistrationNotAuthority: تجميدٌ قبل التشغيل بلا حكمٍ ولا ولادةٍ "
    "ولا `E0`، ولا تقرأ هذه الوحدةَ بوّابةٌ في `kernel/`"
)

VV_BIRTH_PREREGISTRATION_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_COMMIT_CANNOT_CONTAIN_ITS_OWN_SHA,
    A_SELF_RECOMPUTED_DIGEST_IS_NOT_A_SEAL,
    NO_SOURCE_IS_IMPORTED_AFTER_THE_RESULT_IS_SEEN,
    THE_CITED_FREEZE_IS_ABSENT_FROM_THIS_TREE,
    THE_READOUT_DOES_NOT_EXIST_IN_THIS_COMMIT,
    THE_SITE_LIST_IS_INDEPENDENT_NOT_DERIVED,
    THIS_IS_REGISTRATION_NOT_AUTHORITY,
)
"""البواقي المُسمّاةُ لهذه الوحدة، مرتّبةً كما تُرتَّب في بقيّة الطبقة."""


def preregistration_digest() -> str:
    """بصمةُ المُجمَّد، مُعادةَ الاشتقاق من محتواه لا مكتوبةً رقمًا في الشيفرة."""

    return canonical_digest(
        canonical_bytes(
            {
                "experiment_id": EXPERIMENT_ID,
                "typed_spaces": [
                    space.as_canonical_content() for space in TYPED_SPACES
                ],
                "identity_projection": IDENTITY_PROJECTION.as_canonical_content(),
                "quantity_projection": QUANTITY_PROJECTION.as_canonical_content(),
                "hypotheses": [
                    hypothesis.as_canonical_content() for hypothesis in HYPOTHESES
                ],
                "licensed_join": LICENSED_JOIN_SPECIFICATION.as_canonical_content(),
                "behavioural_closure": BEHAVIOURAL_CLOSURE_LAW.as_canonical_content(),
                "trace_minimality": (TRACE_MINIMALITY_CRITERION.as_canonical_content()),
                "weaker_models": [
                    model.as_canonical_content() for model in WEAKER_MODELS
                ],
                "separated_claims": [
                    claim.as_canonical_content() for claim in SEPARATED_CLAIMS
                ],
                "adverse_tree_facts": [
                    fact.as_canonical_content() for fact in ADVERSE_TREE_FACTS
                ],
                "outcome_ceilings": [
                    ceiling.as_canonical_content() for ceiling in OUTCOME_CEILINGS
                ],
                "reconstruction_targets": [
                    assessment.as_canonical_content()
                    for assessment in RECONSTRUCTION_TARGET_ASSESSMENTS
                ],
                "readout_seal_contract": READOUT_SEAL_CONTRACT.as_canonical_content(),
                "required_notation_sites": [
                    list(site) for site in REQUIRED_NOTATION_SITES
                ],
                "named_residuals": list(VV_BIRTH_PREREGISTRATION_NAMED_RESIDUALS),
            }
        )
    )


PREREGISTRATION_DIGEST: Final[str] = preregistration_digest()
"""البصمةُ المُجمَّدة، محسوبةً عند الاستيراد؛ وحدُّ ما تكشفه مكتوبٌ في العقد."""


_FORBIDDEN_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "observed_outcome",
    "verdict",
    "birth_decision",
    "born",
    "result",
    "score",
    "measured",
    "e0",
)


def _refuse_an_unsealed_preregistration() -> None:
    """حارسٌ عند الاستيراد: موقعٌ ساقط، أو قراءةٌ حاضرة، أو حكمٌ في حقل."""

    for declaring_type in (
        AdverseTreeFact,
        OutcomeCeiling,
        ReconstructionTargetAssessment,
        ReadoutSealContract,
    ):
        declared = {item.name for item in fields(declaring_type)}
        for marker in _FORBIDDEN_FIELD_MARKERS:
            if any(marker in name for name in declared):
                raise VvBirthPreregistrationError(
                    f"حقلُ {marker!r} حكمٌ لا شرط، فلا يكون في تسجيلٍ قبليّ"
                )
    missing = missing_notation_sites()
    if missing:
        raise VvBirthPreregistrationError(
            f"مواقعُ دلالةٍ مطلوبةٌ ساقطةٌ من المُجمَّد: {missing!r}"
        )
    if len(set(REQUIRED_NOTATION_SITES)) != len(REQUIRED_NOTATION_SITES):
        raise VvBirthPreregistrationError("موقعُ دلالةٍ تكرّر في القائمة المستقلّة")
    if not readout_module_is_absent():
        raise VvBirthPreregistrationError(
            "الالتزامُ الأوّلُ تجميدٌ بلا قراءة؛ ووجودُ وحدة القراءة يُبطله"
        )
    if any(assessment.is_usable for assessment in RECONSTRUCTION_TARGET_ASSESSMENTS):
        raise VvBirthPreregistrationError(
            "هدفٌ مستقلٌّ مُسجَّلٌ بلا سندٍ خارجيّ؛ فإن وُجد فليُودَع بمصدره"
        )
    if list(VV_BIRTH_PREREGISTRATION_NAMED_RESIDUALS) != sorted(
        VV_BIRTH_PREREGISTRATION_NAMED_RESIDUALS
    ):
        raise VvBirthPreregistrationError("البواقي المُسمّاةُ تُرتَّب ترتيبًا ثابتًا")


_refuse_an_unsealed_preregistration()
