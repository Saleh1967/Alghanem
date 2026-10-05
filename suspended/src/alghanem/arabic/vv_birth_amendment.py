"""G0.VV-BIRTH-1A — تجميدُ المؤثّرات تشغيليًّا، قبل أن تُكتَب قراءةٌ واحدة.

هذه الوحدةُ **الالتزامُ الوسيط**: بين تسجيلٍ قبليٍّ مختوم وقراءةٍ لم تُكتَب
بعد. ووظيفتُها واحدةٌ لا غير: **إغلاقُ الحرّيّة التنفيذيّة** التي بقيت بعد
الالتزام الأوّل. لا بيانات تُقرأ، ولا نتيجةَ تُصدَر، ولا وحدةَ باسم
`vv_birth_readout` تُنشأ هنا.

**وهي لا تمسّ الالتزامَ الأوّلَ بحرف.** `vv_birth_hypothesis` و
`vv_birth_preregistration` تبقيان كما خُتمتا، وبصمتُهما كما هي؛ فتحريرُهما
لإصلاح عيبٍ كان سيُبطل الختمَ الذي عليه تقوم القراءةُ القادمة
(`AN_AMENDMENT_THAT_EDITS_ITS_PARENT_BREAKS_THE_SEAL`). والسندُ التاريخيُّ
مكتوبٌ صراحةً في `SUPERSEDED_PREREGISTRATION_PARENT`، ومداه **تفاصيلُ التنفيذ
وحدَها**: لا فرضيةَ تُعدَّل، ولا مُفنِّدَ يُليَّن، ولا سقفَ يُرفَع
(`THE_AMENDMENT_SUPERSEDES_EXECUTION_NOT_HYPOTHESES`).

**خمسُ ثغراتٍ بقيت بعد التسجيل الأوّل، وأُغلقت هنا بالبناء:**

* **`E` كان وجوديًّا فقط.** `∃E: X_V ⇀ X_V` لا يمنع أن تُكتَب دالّتُه في
  الالتزام الثاني **على مقاس البيانات**، فيصير اختبارُ `H_E` لاحقًا لا سابقًا.
  فصار لـ`E` `ExtensionOperatorSpecification` يحمل مدخلاتِه المسموحةَ، ومصادرَه
  الممنوعة، وشرطَ مجاله، وقاعدةَ تحويله **حرفًا حرفًا**، وحالاتِ لا-تعريفه،
  ولوازمَ مخرَجه (`AN_EXISTENTIAL_OPERATOR_IS_A_BLANK_CHEQUE`).
* **`X_V` كان يناقض `𝓠`.** عضويّتُه كانت تُجيز «صفرًا أو أكثرَ من مواضع
  الامتداد» بينما `𝓠 = {1, 2}`؛ فامتدادان يُخرجان `π_Q` من مجاله أو يُضغَطان
  إليه قسرًا. فجُمِّد الحلُّ الأوّلُ من الحلّين: `#Extension ∈ {0, 1}`، ويبقى
  `𝓠 = {1, 2}` كما خُتم (`A_DOMAIN_THAT_CONTRADICTS_ITS_CODOMAIN_IS_NOT_FROZEN`).
* **النماذجُ الأضعفُ كانت نثرًا.** وصفُ ما يراه النموذجُ وما يفتقده لا يمنع أن
  تُكتَب دالّتُه في القراءة أضعفَ أو أقوى **بحسب النتيجة**. فصار لكلٍّ منها
  خوارزميّةٌ مُرقَّمةُ الخطوات بمدخلاتها ومخرَجها وحالات `UNDEFINED`
  (`A_RIVAL_WRITTEN_AFTER_THE_RESULT_IS_NOT_A_RIVAL`).
* **منعُ التسريب كان بالأسماء.** `carrier_codepoint` و`letter_index` ممنوعان
  بالاسم، فتُعاد المعلومةُ نفسُها باسم `unicode_scalar` فتعبر الحاجز. فصار
  المنعُ **بالمصدر**: لكلّ حقلٍ `ProvenanceClass`، و`π_I` ممنوعةٌ من
  `ORTHOGRAPHIC_IDENTITY ∪ PROGRAM_POSITION ∪ MODEL_OUTPUT` مهما سُمّي الحقل
  (`A_BAN_BY_NAME_IS_DEFEATED_BY_A_RENAME`).
* **`T' ⊊ T` لم تكن مُعرَّفةً على سجلٍّ مصنَّف.** الاحتواءُ الحقيقيُّ معرّفٌ على
  مجموعات، والأثرُ سجلٌّ بحقول؛ وحقلٌ واحدٌ قد يخزّن تسلسلَ المُدخَل كاملًا
  فينجح شرطُ حذف الحقول والأثرُ نسخة. فصار `T' ≺_T T` إسقاطًا مُعلَنًا على
  حقولٍ مُسمّاة، مع منعٍ بنيويٍّ أن يحمل أيُّ حقلٍ ترميزًا قابلًا لعكسِ المُدخَل
  كاملًا (`A_SINGLE_FIELD_CAN_HIDE_THE_WHOLE_INPUT`).

**وعدمُ تناظرٍ منطقيٌّ سادسٌ صُحِّح:** `H_same_type` يكفي لتفنيدها سياقٌ واحدٌ
يفرّق؛ أمّا `H_different_type` فـ**لا يفنّدها عدمُ العثور**، إذ قد يكون
السياقُ المميِّزُ هو الذي لم يُختبَر. فقُيّدت الدعوى بمجموعة سياقاتٍ مُجمَّدة
`K_0`، والمخرَجُ المتاحُ ثلاثةٌ لا غير: `DISTINGUISHED_ON_K0` و
`NOT_DISTINGUISHED_ON_K0` و`UNDERPOWERED`؛ ولا يُقرأ الثاني مساواةَ نوعٍ كونيّة
(`ABSENCE_ON_A_FINITE_CONTEXT_SET_IS_NOT_IDENTITY_OF_TYPE`).

**وثلاثةُ ضوابطَ مضادّةٍ لـ`H_E` مُجمَّدةٌ قبل القراءة:** `E_no_extension` و
`E_wrong_quality` و`E_wrong_partner`. فإن لم يستطع معيارُ `π_I`/`π_Q` أن
**يُفشِل** واحدًا منها، فالمعيارُ ينجح لكلّ تحويلٍ اعتباطيّ، والمخرَجُ
`REPRESENTATION_TAUTOLOGY` (`A_CRITERION_NOTHING_FAILS_MEASURES_NOTHING`).

**ومفرداتُ المخرَج المُضافةُ هنا لا تُحقَن في المختوم:** `ExperimentOutcome` في
الالتزام الأوّل تبقى كما هي — **بلا `BORN` كما خُتمت** — وما زاد فمفردةٌ ثانيةٌ
`AmendmentOutcome` مُعلَنةٌ هنا، لأنّ تعديلَ المفردة المختومة تحريرٌ لأبٍ مختوم
(`AN_AMENDMENT_THAT_EDITS_ITS_PARENT_BREAKS_THE_SEAL`).

تجميدٌ لا سلطة: لا ولادةَ ولا حكمَ ولا قراءة، ولا استيرادَ من `kernel/` حرفًا.
"""

from __future__ import annotations

import importlib
import importlib.util
from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from alghanem.canonical_content import canonical_bytes, canonical_digest

from .vv_birth_hypothesis import (
    BANNED_IDENTITY_PROXIES,
    HypothesisIdentifier,
    VvBirthHypothesisError,
    WeakerModelRole,
    weaker_model_named,
)
from .vv_birth_preregistration import (
    PREREGISTRATION_DIGEST,
    READOUT_MODULE_NAME,
)

__all__ = [
    "ABSENCE_ON_A_FINITE_CONTEXT_SET_IS_NOT_IDENTITY_OF_TYPE",
    "ADVERSARIAL_EXTENSION_OPERATORS",
    "AMENDMENT_DIGEST",
    "AMENDMENT_ID",
    "AN_AMENDMENT_THAT_EDITS_ITS_PARENT_BREAKS_THE_SEAL",
    "AN_EXISTENTIAL_OPERATOR_IS_A_BLANK_CHEQUE",
    "A_BAN_BY_NAME_IS_DEFEATED_BY_A_RENAME",
    "A_CRITERION_NOTHING_FAILS_MEASURES_NOTHING",
    "A_DOMAIN_THAT_CONTRADICTS_ITS_CODOMAIN_IS_NOT_FROZEN",
    "A_RIVAL_WRITTEN_AFTER_THE_RESULT_IS_NOT_A_RIVAL",
    "A_SINGLE_FIELD_CAN_HIDE_THE_WHOLE_INPUT",
    "CONTEXT_SET_K0",
    "EXTENSION_COUNT_AMENDMENT",
    "EXTENSION_OPERATOR_SPECIFICATION",
    "FORBIDDEN_TRACE_CONTENT",
    "IDENTITY_PROJECTION_FORBIDDEN_PROVENANCE",
    "REQUIRED_AMENDMENT_SITES",
    "SUPERSEDED_PREREGISTRATION_PARENT",
    "THE_AMENDMENT_SUPERSEDES_EXECUTION_NOT_HYPOTHESES",
    "TRACE_FIELD_SPECIFICATIONS",
    "TYPE_DISTINCTION_LAW",
    "VV_BIRTH_AMENDMENT_NAMED_RESIDUALS",
    "WEAKER_MODEL_IMPLEMENTATIONS",
    "AdversarialOperator",
    "AmendmentOutcome",
    "ContextK0",
    "ExtensionCountAmendment",
    "ExtensionOperatorSpecification",
    "InputField",
    "OperatorClass",
    "ProvenanceClass",
    "SupersededPreregistrationParent",
    "TraceFieldSpecification",
    "TypeDistinctionLaw",
    "VvBirthAmendmentError",
    "WeakerModelImplementation",
    "adversarial_operator_named",
    "amendment_digest",
    "identity_projection_refuses",
    "missing_amendment_sites",
    "readout_module_is_absent",
    "trace_projections_of",
    "weaker_model_implementation_named",
]


class VvBirthAmendmentError(ValueError):
    """رفضٌ عند الإنشاء أو الاستيراد: حرّيّةٌ تنفيذيّةٌ بقيت حيث يلزم إغلاقُها."""


AMENDMENT_ID: Final[str] = "G0.VV-BIRTH-1A"
"""مُعرِّفُ التعديل: تجميدُ المؤثّرات تشغيليًّا قبل القراءة."""


# --- الأبُ المختومُ الذي لا يُمَسّ -------------------------------------------


@dataclass(frozen=True, slots=True)
class SupersededPreregistrationParent:
    """الأبُ التاريخيُّ: بصمةُ التزامه، وبصمةُ محتواه، ومدى ما يُستبدَل منه."""

    commit_sha: str
    content_digest: str
    what_is_superseded: str
    what_is_preserved: str
    preserved_hypotheses: tuple[HypothesisIdentifier, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.commit_sha, str) or len(self.commit_sha) != 40:
            raise VvBirthAmendmentError("بصمةُ الالتزام الأبِ أربعون خانةً سُداسيّة")
        if any(letter not in "0123456789abcdef" for letter in self.commit_sha):
            raise VvBirthAmendmentError("بصمةُ الالتزام حروفٌ سُداسيّةٌ صغيرةٌ لا غير")
        if not isinstance(self.content_digest, str) or len(self.content_digest) != 64:
            raise VvBirthAmendmentError("بصمةُ المحتوى أربعٌ وستّون خانة")
        for value, label in (
            (self.what_is_superseded, "ما يُستبدَل"),
            (self.what_is_preserved, "ما يُحفَظ"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise VvBirthAmendmentError(f"{label} نصٌّ غير فارغ")
        if set(self.preserved_hypotheses) != set(HypothesisIdentifier):
            raise VvBirthAmendmentError(
                "تعديلُ التنفيذ يحفظ الفرضياتِ كلَّها؛ وإسقاطُ واحدةٍ تعديلٌ للدعوى"
            )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى السند الأبويّ للبصمة."""

        return {
            "commit_sha": self.commit_sha,
            "content_digest": self.content_digest,
            "what_is_superseded": self.what_is_superseded,
            "what_is_preserved": self.what_is_preserved,
            "preserved_hypotheses": [
                identifier.value for identifier in self.preserved_hypotheses
            ],
        }


SUPERSEDED_PREREGISTRATION_PARENT: Final[SupersededPreregistrationParent] = (
    SupersededPreregistrationParent(
        commit_sha="a2652ad5de68a69e77a99722e6715ab747468042",
        content_digest=PREREGISTRATION_DIGEST,
        what_is_superseded=(
            "تفاصيلُ التنفيذ وحدَها: دالّةُ `E`، وحدُّ عدد مواضع الامتداد في "
            "`X_V`، وخوارزمياتُ النماذج الأضعف، وصيغةُ منع التسريب، وترتيبُ "
            "الأثر، ومدى دعوى فرضيتَي النوع"
        ),
        what_is_preserved=(
            "الفرضياتُ الخمسُ بنصوصها ومُفنِّداتها، وسقوفُ المخرَج، والحقائقُ "
            "الضارّةُ المُودَعة، وعقدُ ختم القراءة؛ ولم يُحرَّر منها حرف"
        ),
        preserved_hypotheses=tuple(HypothesisIdentifier),
    )
)
"""سندُ الأبِ المختوم: بصمةُ التزامه وبصمةُ محتواه، ومدى الاستبدال مُقيَّدٌ به."""


# --- مفردةُ مخرَجٍ ثانيةٌ، لا حقنٌ في المختوم -------------------------------


class AmendmentOutcome(Enum):
    """حالاتُ مخرَجٍ زادها التعديل. ولا `BORN` هنا كما لا `BORN` هناك."""

    REPRESENTATION_TAUTOLOGY = "REPRESENTATION_TAUTOLOGY"
    DISTINGUISHED_ON_K0 = "DISTINGUISHED_ON_K0"
    NOT_DISTINGUISHED_ON_K0 = "NOT_DISTINGUISHED_ON_K0"
    UNDERPOWERED = "UNDERPOWERED"


# --- المصادر: منعٌ بالنسب لا بالاسم ----------------------------------------


class ProvenanceClass(Enum):
    """نسبُ الحقل: من أين جاءت معلومتُه، لا ماذا سُمّي."""

    ORTHOGRAPHIC_IDENTITY = "هويّةُ الرسم: نقطةُ ترميزٍ أو اسمُ حرفٍ مكتوب"
    PROGRAM_POSITION = "موضعٌ برمجيّ: فهرسٌ أو إزاحةٌ في بنيةِ تشغيل"
    MODEL_OUTPUT = "مخرَجُ نموذج: ناتجُ قاعدةٍ من قواعد المرشَّح أو ما يُشتقّ منه"
    PHYSICAL_OBSERVATION = "مشاهدةٌ فيزيائيّة: صوتٌ مُسجَّلٌ أو قياسُ نطق"
    STATE_OBSERVATION = "مشاهدةُ حالة: `CarrierState` مقروءةً من العلامة"


IDENTITY_PROJECTION_FORBIDDEN_PROVENANCE: Final[frozenset[ProvenanceClass]] = frozenset(
    {
        ProvenanceClass.ORTHOGRAPHIC_IDENTITY,
        ProvenanceClass.PROGRAM_POSITION,
        ProvenanceClass.MODEL_OUTPUT,
    }
)
"""ما لا يجوز أن تقرأ منه `π_I`؛ والمنعُ بالنسب فلا تُنقَض بإعادة تسمية."""


@dataclass(frozen=True, slots=True)
class InputField:
    """حقلُ مُدخَلٍ واحد: اسمُه، ونسبُه، وما يحمله بالضبط."""

    name: str
    provenance: ProvenanceClass
    what_it_carries: str

    def __post_init__(self) -> None:
        for value, label in (
            (self.name, "اسمُ الحقل"),
            (self.what_it_carries, "ما يحمله"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise VvBirthAmendmentError(f"{label} نصٌّ غير فارغ")
        if not isinstance(self.provenance, ProvenanceClass):
            raise VvBirthAmendmentError("نسبُ الحقل عضوٌ في مفردته المغلقة")

    def as_canonical_content(self) -> dict[str, str]:
        """محتوى الحقل للبصمة."""

        return {
            "name": self.name,
            "provenance": self.provenance.value,
            "what_it_carries": self.what_it_carries,
        }


def identity_projection_refuses(field: InputField) -> bool:
    """أتمتنع `π_I` عن هذا الحقل؟ الجوابُ من نسبه وحدَه لا من اسمه.

    ولهذا تُهزَم إعادةُ التسمية: `letter_index` باسم `unicode_scalar` يبقى
    `ORTHOGRAPHIC_IDENTITY` أو `PROGRAM_POSITION`، فيُرفَض كما رُفض أوّلَ مرّة.
    """

    return field.provenance in IDENTITY_PROJECTION_FORBIDDEN_PROVENANCE


# --- `E` مُجمَّدًا تشغيليًّا --------------------------------------------------


class OperatorClass(Enum):
    """طبقةُ المؤثّر: من أين يقرأ، وبأيّ سقفٍ يُنسَب إليه ما يقول."""

    ORTHOGRAPHIC_EXTENSION_OPERATOR = (
        "مؤثّرٌ يحتاج هويّةَ الرسم `ا/و/ي` ليحدّد الامتداد؛ فهو شاهدٌ على "
        "الكتابة لا على النطق، ولا يُسمّى شاهدًا صوتيًّا فيزيائيًّا"
    )
    STATE_ONLY_EXTENSION_OPERATOR = (
        "مؤثّرٌ لا يقرأ إلّا `CarrierState`؛ ولا يتحقّق في هذه الشجرة اليوم"
    )


@dataclass(frozen=True, slots=True)
class ExtensionOperatorSpecification:
    """`E: X_V ⇀ X_V` مُعرَّفًا بخطواته، لا موجودًا بكمٍّ وجوديّ."""

    operator_name: str
    operator_class: OperatorClass
    allowed_inputs: tuple[InputField, ...]
    forbidden_sources: tuple[str, ...]
    domain_predicate: str
    transformation_rule: tuple[str, ...]
    undefinedness_conditions: tuple[str, ...]
    output_invariants: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.operator_name, str) or not self.operator_name.strip():
            raise VvBirthAmendmentError("اسمُ المؤثّر نصٌّ غير فارغ")
        if not isinstance(self.operator_class, OperatorClass):
            raise VvBirthAmendmentError("طبقةُ المؤثّر عضوٌ في مفردتها المغلقة")
        if not self.allowed_inputs:
            raise VvBirthAmendmentError(
                "مؤثّرٌ بلا مدخلاتٍ مُعلَنةٍ يقرأ كلَّ شيء؛ وهذا هو الشيك المفتوح"
            )
        if not isinstance(self.domain_predicate, str) or not self.domain_predicate:
            raise VvBirthAmendmentError("شرطُ المجال نصٌّ غير فارغ")
        for sequence, label in (
            (self.forbidden_sources, "المصادرُ الممنوعة"),
            (self.transformation_rule, "قاعدةُ التحويل"),
            (self.undefinedness_conditions, "حالاتُ لا-التعريف"),
            (self.output_invariants, "لوازمُ المخرَج"),
        ):
            if not isinstance(sequence, tuple) or not sequence:
                raise VvBirthAmendmentError(f"{label} قائمةٌ مُسمّاةٌ غيرُ فارغة")
            for item in sequence:
                if not isinstance(item, str) or not item.strip():
                    raise VvBirthAmendmentError(f"بندٌ فارغٌ في {label}")
        reads_orthography = any(
            field.provenance is ProvenanceClass.ORTHOGRAPHIC_IDENTITY
            for field in self.allowed_inputs
        )
        if (
            reads_orthography
            and self.operator_class is not OperatorClass.ORTHOGRAPHIC_EXTENSION_OPERATOR
        ):
            raise VvBirthAmendmentError(
                "مؤثّرٌ يقرأ هويّةَ الرسم يُسمّى `ORTHOGRAPHIC_EXTENSION_OPERATOR`"
            )
        if any(
            field.provenance is ProvenanceClass.MODEL_OUTPUT
            for field in self.allowed_inputs
        ):
            raise VvBirthAmendmentError(
                "مخرَجُ نموذجٍ في مدخلات `E` يجعل اختبارَ `H_E` قراءةً لنفسه"
            )
        names = [field.name for field in self.allowed_inputs]
        if len(set(names)) != len(names):
            raise VvBirthAmendmentError("حقلُ مُدخَلٍ تكرّر باسمه")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المواصفة للبصمة."""

        return {
            "operator_name": self.operator_name,
            "operator_class": self.operator_class.value,
            "allowed_inputs": [
                field.as_canonical_content() for field in self.allowed_inputs
            ],
            "forbidden_sources": list(self.forbidden_sources),
            "domain_predicate": self.domain_predicate,
            "transformation_rule": list(self.transformation_rule),
            "undefinedness_conditions": list(self.undefinedness_conditions),
            "output_invariants": list(self.output_invariants),
        }


EXTENSION_OPERATOR_SPECIFICATION: Final[ExtensionOperatorSpecification] = (
    ExtensionOperatorSpecification(
        operator_name="E",
        operator_class=OperatorClass.ORTHOGRAPHIC_EXTENSION_OPERATOR,
        allowed_inputs=(
            InputField(
                name="vowel_state",
                provenance=ProvenanceClass.STATE_OBSERVATION,
                what_it_carries=(
                    "حالةَ الموضع الصائت مقروءةً من العلامة: فتحةٌ أو ضمّةٌ "
                    "أو كسرة، لا أكثر"
                ),
            ),
            InputField(
                name="following_carrier_identity",
                provenance=ProvenanceClass.ORTHOGRAPHIC_IDENTITY,
                what_it_carries=(
                    "هويّةَ الحامل التالي `ا/و/ي` رسمًا؛ وهي المُدخَل الذي "
                    "يجعل هذا المؤثّرَ شاهدًا على الكتابة لا على النطق"
                ),
            ),
            InputField(
                name="following_carrier_state",
                provenance=ProvenanceClass.STATE_OBSERVATION,
                what_it_carries=(
                    "حالةَ الحامل التالي؛ ويلزم أن تكون سكونًا ضمنيًّا فلا "
                    "يكون الحاملُ صامتًا متحرّكًا"
                ),
            ),
        ),
        forbidden_sources=(
            "`p_extractor.PhoneticRole.MADD_EXTENSION`: وسمٌ يُعلَّق بالقاعدة "
            "المراد اختبارُها، فقراءتُه قراءةُ الجواب",
            "أيُّ مخرَجٍ من `alghanem.arabic.syllabifier`، ومنه `Slot` و"
            "`letter_index` وجدولُ القوالب",
            "أيُّ هدفِ إعادةِ بناءٍ أو حكمٍ أو مخرَجٍ من هذه التجربة نفسِها",
            "أيُّ حقلٍ مُشتَقٍّ من النتيجة المراد اختبارُها، ولو بوسيط",
        ),
        domain_predicate=(
            "`v ∈ Dom(E)` متى كانت `vowel_state ∈ {FATHA, DAMMA, KASRA}`، "
            "وكان بعدها حاملٌ واحدٌ هويّتُه `ا` أو `و` أو `ي` حالتُه سكونٌ "
            "ضمنيّ، ولم يكن للموضع امتدادٌ مُحتسَبٌ سلفًا"
        ),
        transformation_rule=(
            "١. اقرأ `vowel_state` وسمِّه `q0`؛ و`π_Q(v) = 1` بحكم الشرط.",
            "٢. اقرأ `following_carrier_identity` وسمِّه `c₁`.",
            "٣. إن كان الزوجُ `(q0, c₁)` واحدًا من الثلاثة "
            "`(FATHA, ا)`، `(DAMMA, و)`، `(KASRA, ي)` فاعدُدْ موضعَ الامتداد "
            "واحدًا؛ وإلّا فـ`E` غيرُ مُعرَّفةٍ على `v`.",
            "٤. أخرِجْ `E(v)` بحالةٍ صائتةٍ هي `q0` نفسُها غيرَ مُبدَّلة، "
            "وبعدد مواضعَ يساوي اثنين.",
            "٥. لا تقرأ شيئًا غيرَ الحقول الثلاثة المُعلَنة، ولا تكتب في "
            "المخرَج حقلًا لم يُذكَر في لوازم المخرَج.",
        ),
        undefinedness_conditions=(
            "حالةُ الموضع سكونٌ أو `DAGGER` أو `PASSTHROUGH`: فليس في `X_V`",
            "الحاملُ التالي غيرُ `ا/و/ي`، أو حالتُه حركةٌ أو سكونٌ صريح",
            "الزوجُ `(q0, c₁)` غيرُ مطابق: كفتحةٍ يتلوها `ي`",
            "الموضعُ آخرُ الكلمة فلا حاملَ بعده",
            "الحاملُ التالي شقٌّ أوّلُ من شدّة: فالوصفُ تضعيفٌ لا امتداد",
        ),
        output_invariants=(
            "`π_I(E(v)) = π_I(v)` بالبناء: الخطوةُ الرابعةُ لا تبدّل الجودة",
            "`π_Q(E(v)) = 2` و`π_Q(v) = 1`، فـ`π_Q(E(v)) > π_Q(v)`",
            "لا حقلَ في المخرَج نسبُه `MODEL_OUTPUT`",
            "`E` لا تُعرَّف مرّتين على الموضع نفسِه، فلا يتراكم امتدادان",
        ),
    )
)
"""`E` بخطواته الخمس؛ ولوازمُ مخرَجه مكتوبةٌ لأنّها **تُقاس** لا لأنّها تُصدَّق.

وملاحظةٌ لازمة: كونُ `π_I(E(v)) = π_I(v)` لازمًا عن البناء يجعل `H_E` **صغيرةَ
المؤونة** على هذا المؤثّر بعينه؛ ولذلك وحدَه لا تُقرأ نتيجتُه دعوى إلّا مع
الضوابط المضادّة أدناه، فهي التي تُبيّن أنّ المعيارَ يُفشِل شيئًا أصلًا.
"""


@dataclass(frozen=True, slots=True)
class AdversarialOperator:
    """ضابطٌ مضادّ: تحويلٌ **يجب أن يفشل**، وإلّا فالمعيارُ لا يقيس شيئًا."""

    name: str
    transformation_rule: str
    which_invariant_it_must_break: str
    outcome_if_it_passes: AmendmentOutcome

    def __post_init__(self) -> None:
        for value, label in (
            (self.name, "اسمُ الضابط"),
            (self.transformation_rule, "قاعدةُ تحويله"),
            (self.which_invariant_it_must_break, "اللازمُ الذي يجب أن يكسره"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise VvBirthAmendmentError(f"{label} نصٌّ غير فارغ")
        if self.outcome_if_it_passes is not AmendmentOutcome.REPRESENTATION_TAUTOLOGY:
            raise VvBirthAmendmentError(
                "ضابطٌ مضادٌّ ينجح يعني أنّ المعيارَ ينجح لكلّ تحويل: "
                "`REPRESENTATION_TAUTOLOGY` لا غيرُها"
            )

    def as_canonical_content(self) -> dict[str, str]:
        """محتوى الضابط للبصمة."""

        return {
            "name": self.name,
            "transformation_rule": self.transformation_rule,
            "which_invariant_it_must_break": self.which_invariant_it_must_break,
            "outcome_if_it_passes": self.outcome_if_it_passes.value,
        }


ADVERSARIAL_EXTENSION_OPERATORS: Final[tuple[AdversarialOperator, ...]] = (
    AdversarialOperator(
        name="E_no_extension",
        transformation_rule=("يُعيد `v` كما هو بلا زيادةِ موضع: `π_Q(E(v)) = π_Q(v)`"),
        which_invariant_it_must_break="`π_Q(E(v)) > π_Q(v)`: يجب أن يسقط عليه",
        outcome_if_it_passes=AmendmentOutcome.REPRESENTATION_TAUTOLOGY,
    ),
    AdversarialOperator(
        name="E_wrong_quality",
        transformation_rule=(
            "يزيد موضعًا **ويبدّل** الجودةَ: فتحةً إلى ضمّة، مع بقاء العدد اثنين"
        ),
        which_invariant_it_must_break="`π_I(E(v)) = π_I(v)`: يجب أن يسقط عليه",
        outcome_if_it_passes=AmendmentOutcome.REPRESENTATION_TAUTOLOGY,
    ),
    AdversarialOperator(
        name="E_wrong_partner",
        transformation_rule=(
            "يمدّ الفتحةَ بـ`ي` والكسرةَ بـ`ا`: زوجٌ غيرُ مطابقٍ في الخطوة الثالثة"
        ),
        which_invariant_it_must_break=(
            "شرطَ المجال نفسَه: يجب أن يخرج `UNDEFINED` لا `PASS`"
        ),
        outcome_if_it_passes=AmendmentOutcome.REPRESENTATION_TAUTOLOGY,
    ),
)
"""ثلاثةُ ضوابطَ مضادّة؛ ومن لم يُفشِلها معيارُه فمعيارُه ينجح بلا مضمون."""


def adversarial_operator_named(name: str) -> AdversarialOperator:
    """الضابطُ المضادُّ باسمه؛ ولا اسمَ خارجَ المُجمَّد."""

    for operator in ADVERSARIAL_EXTENSION_OPERATORS:
        if operator.name == name:
            return operator
    raise VvBirthAmendmentError(f"لا ضابطَ مضادَّ باسم {name!r}")


# --- `X_V` مُوافِقًا لـ`𝓠` ----------------------------------------------------


@dataclass(frozen=True, slots=True)
class ExtensionCountAmendment:
    """حدُّ عدد مواضع الامتداد، مُجمَّدًا بحيث لا يناقض مجالَ `π_Q`."""

    superseded_clause: str
    chosen_bound: tuple[int, ...]
    quantity_codomain: tuple[int, ...]
    why_this_branch: str
    what_the_other_branch_would_have_required: str

    def __post_init__(self) -> None:
        for value, label in (
            (self.superseded_clause, "البندُ المُستبدَل"),
            (self.why_this_branch, "لماذا هذا الفرع"),
            (
                self.what_the_other_branch_would_have_required,
                "ما كان يلزم الفرعَ الآخر",
            ),
        ):
            if not isinstance(value, str) or not value.strip():
                raise VvBirthAmendmentError(f"{label} نصٌّ غير فارغ")
        if self.chosen_bound != (0, 1):
            raise VvBirthAmendmentError(
                "الفرعُ المُجمَّدُ `#Extension ∈ {0, 1}`؛ وتوسيعُ `𝓠` فرعٌ آخرُ لم يُختَر"
            )
        expected = tuple(count + 1 for count in self.chosen_bound)
        if self.quantity_codomain != expected:
            raise VvBirthAmendmentError(
                "مجالُ `π_Q` صورةُ الحدّ المختار؛ ومجالٌ يناقض مجاله ليس مُجمَّدًا"
            )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التعديل للبصمة."""

        return {
            "superseded_clause": self.superseded_clause,
            "chosen_bound": list(self.chosen_bound),
            "quantity_codomain": list(self.quantity_codomain),
            "why_this_branch": self.why_this_branch,
            "what_the_other_branch_would_have_required": (
                self.what_the_other_branch_would_have_required
            ),
        }


EXTENSION_COUNT_AMENDMENT: Final[ExtensionCountAmendment] = ExtensionCountAmendment(
    superseded_clause=(
        "«مع صفرٍ أو أكثرَ من مواضع الامتداد التالية لها» في شرط عضويّة `X_V` "
        "من `vv_birth_hypothesis`: يُقرأ من اليوم مُقيَّدًا بـ`#Extension ∈ {0, 1}`"
    ),
    chosen_bound=(0, 1),
    quantity_codomain=(1, 2),
    why_this_branch=(
        "`𝓠 = {1, 2}` مختومٌ في الالتزام الأوّل؛ فتقييدُ المجال يحفظ المختومَ "
        "كما هو، وتوسيعُ `𝓠` كان سيُغيّر إسقاطًا مُجمَّدًا — وهو تعديلُ دعوى "
        "لا تعديلُ تنفيذ"
    ),
    what_the_other_branch_would_have_required=(
        "قانونًا صريحًا لـ`π_Q` على ثلاثة مواضعَ فأكثر، وشاهدًا على أنّ "
        "الشجرة تُظهِر امتدادين متتاليين أصلًا؛ ولا واحدَ منهما قائمٌ اليوم"
    ),
)
"""الفرعُ المُجمَّد: مجالٌ ضيّقٌ يوافق مجالًا مختومًا، لا مجالٌ يُوسَّع بعد الختم."""


# --- النماذجُ الأضعفُ خوارزمياتٍ لا نثرًا ------------------------------------


@dataclass(frozen=True, slots=True)
class WeakerModelImplementation:
    """نموذجٌ أضعفُ مُجمَّدٌ بخطواته، فلا يُكتَب أوّلَ مرّةٍ داخل القراءة."""

    name: str
    input_fields: tuple[InputField, ...]
    algorithm: tuple[str, ...]
    output: str
    undefined_conditions: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise VvBirthAmendmentError("اسمُ النموذج نصٌّ غير فارغ")
        try:
            weaker_model_named(self.name)
        except VvBirthHypothesisError as error:
            raise VvBirthAmendmentError(
                f"نموذجٌ أضعفُ غيرُ مختومٍ في الالتزام الأوّل: {self.name!r}"
            ) from error
        if not self.input_fields:
            raise VvBirthAmendmentError("نموذجٌ بلا مدخلاتٍ مُعلَنةٍ يرى كلَّ شيء")
        if not isinstance(self.output, str) or not self.output.strip():
            raise VvBirthAmendmentError("مخرَجُ النموذج نصٌّ غير فارغ")
        for sequence, label in (
            (self.algorithm, "خطواتُ الخوارزميّة"),
            (self.undefined_conditions, "حالاتُ لا-التعريف"),
        ):
            if not isinstance(sequence, tuple) or not sequence:
                raise VvBirthAmendmentError(f"{label} قائمةٌ مُسمّاةٌ غيرُ فارغة")
            for item in sequence:
                if not isinstance(item, str) or not item.strip():
                    raise VvBirthAmendmentError(f"بندٌ فارغٌ في {label}")

    @property
    def counts_as_evidence(self) -> bool:
        """أيُحتَجّ ببلوغه؟ الجوابُ من دوره المختوم في الالتزام الأوّل."""

        return weaker_model_named(self.name).role is WeakerModelRole.RIVAL

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التنفيذ للبصمة."""

        return {
            "name": self.name,
            "input_fields": [
                field.as_canonical_content() for field in self.input_fields
            ],
            "algorithm": list(self.algorithm),
            "output": self.output,
            "undefined_conditions": list(self.undefined_conditions),
        }


_STATE_SEQUENCE: Final[InputField] = InputField(
    name="state_sequence",
    provenance=ProvenanceClass.STATE_OBSERVATION,
    what_it_carries="تسلسلَ `CarrierState` للوحدات بترتيبها، بلا وسمٍ ولا دور",
)

_CARRIER_SEQUENCE: Final[InputField] = InputField(
    name="carrier_sequence",
    provenance=ProvenanceClass.ORTHOGRAPHIC_IDENTITY,
    what_it_carries="تسلسلَ هويّات الحوامل رسمًا، بلا حالةٍ ولا دور",
)


WEAKER_MODEL_IMPLEMENTATIONS: Final[tuple[WeakerModelImplementation, ...]] = (
    WeakerModelImplementation(
        name="M_drop",
        input_fields=(_STATE_SEQUENCE, _CARRIER_SEQUENCE),
        algorithm=(
            "١. امسح التسلسلَ من يمينه إلى يساره موضعًا موضعًا.",
            "٢. متى صادفتَ حاملًا هويّتُه `ا/و/ي` حالتُه سكونٌ ضمنيّ، "
            "**احذفه من المخرَج جملةً** ولا تعدَّ له موضعًا.",
            "٣. أخرِجْ ما بقي بترتيبه، فيكون كلُّ صائتٍ بموضعٍ واحد.",
        ),
        output="تسلسلٌ لا يحمل امتدادًا البتّة: كلُّ `VV` صار `V`",
        undefined_conditions=(
            "لا حالةَ لا-تعريف: هذا النموذجُ كلّيٌّ على مدخلاته، وذاك جزءٌ " "من ضعفه المُعلَن",
        ),
    ),
    WeakerModelImplementation(
        name="M_consonant",
        input_fields=(_STATE_SEQUENCE, _CARRIER_SEQUENCE),
        algorithm=(
            "١. امسح التسلسلَ موضعًا موضعًا.",
            "٢. متى صادفتَ حاملًا هويّتُه `ا/و/ي` حالتُه سكونٌ ضمنيّ، "
            "**صنِّفه صامتًا ساكنًا مستقلًّا** ولا تربطه بما قبله.",
            "٣. أخرِجْ التصنيفَ صامتًا/صائتًا لكلّ موضعٍ على حدة.",
        ),
        output="تسلسلُ تصنيفٍ ثنائيٍّ لا امتدادَ فيه ولا وحدةَ صائتٍ ممدودة",
        undefined_conditions=(
            "حاملٌ خارجَ مجموعة الحوامل المُعلَنة: يخرج `UNDEFINED` ولا يُصنَّف",
        ),
    ),
    WeakerModelImplementation(
        name="M_second_vowel",
        input_fields=(_STATE_SEQUENCE, _CARRIER_SEQUENCE),
        algorithm=(
            "١. امسح التسلسلَ موضعًا موضعًا.",
            "٢. متى صادفتَ حاملًا هويّتُه `ا/و/ي` حالتُه سكونٌ ضمنيّ بعد "
            "صائت، **اجعله صائتًا ثانيًا مستقلًّا** بجودة الصائت السابق.",
            "٣. أخرِجْ تسلسلًا فيه صائتان متعاقبان حيث كان امتداد.",
        ),
        output="تسلسلٌ بمركزين متعاقبين حيث يدّعي المرشَّحُ مركزًا واحدًا بحالتين",
        undefined_conditions=(
            "حاملُ امتدادٍ لا صائتَ قبله: يخرج `UNDEFINED` ولا يُفترَض له جودة",
        ),
    ),
    WeakerModelImplementation(
        name="M_no_join",
        input_fields=(_STATE_SEQUENCE, _CARRIER_SEQUENCE),
        algorithm=(
            "١. صنِّف كلَّ موضعٍ صامتًا أو صائتًا كما يصنّفه المرشَّح.",
            "٢. احفظ الترتيبَ كما هو.",
            "٣. **لا تُطبِّق `J` ولا أيَّ عمليةِ وصل**: أخرِجْ قائمةً مسطَّحةً "
            "من المواضع المصنَّفة بلا أيّ تجميعٍ في مركز.",
        ),
        output="قائمةٌ مسطَّحةٌ مرتَّبة: تصنيفٌ وترتيبٌ بلا مركزٍ مقطعيّ",
        undefined_conditions=("لا حالةَ لا-تعريف: غيابُ الوصل ليس خطأً فيه بل هو تعريفُه",),
    ),
    WeakerModelImplementation(
        name="M_identity_lookup",
        input_fields=(_CARRIER_SEQUENCE,),
        algorithm=(
            "١. لكلّ موضعٍ خُذ هويّةَ حامله رسمًا، ولا تقرأ حالةً البتّة.",
            "٢. اقرأ المخرَجَ من جدولِ بحثٍ مفتاحُه الهويّةُ وحدَها.",
            "٣. أخرِجْ ما في الجدول بلا بنيةٍ ولا وصلٍ ولا كمّيّة.",
        ),
        output="ما يُنال بهويّة الرسم وحدَها؛ وهو **حدُّ التسريب** لا دليلًا",
        undefined_conditions=("هويّةٌ غيرُ مُقيَّدةٍ في الجدول: يخرج `UNDEFINED`",),
    ),
)
"""النماذجُ الخمسةُ بخطواتها؛ والخامسُ مقياسُ تسريبٍ لا يُحتَجّ به بحال."""


def weaker_model_implementation_named(name: str) -> WeakerModelImplementation:
    """تنفيذُ النموذج الأضعف باسمه؛ ولا اسمَ خارجَ المُجمَّد."""

    for implementation in WEAKER_MODEL_IMPLEMENTATIONS:
        if implementation.name == name:
            return implementation
    raise VvBirthAmendmentError(f"لا تنفيذَ لنموذجٍ أضعفَ باسم {name!r}")


# --- ترتيبُ الأثر ------------------------------------------------------------


FORBIDDEN_TRACE_CONTENT: Final[tuple[str, ...]] = (
    "raw_input",
    "raw_surface",
    "serialized_original_input",
    "reversible_whole_input_encoding",
)
"""ما لا يحمله حقلُ أثرٍ بحال؛ وحملُه إيّاه يجعل «الضغطَ» تخزينًا للمُدخَل."""


@dataclass(frozen=True, slots=True)
class TraceFieldSpecification:
    """حقلُ أثرٍ واحد: ما يحمله، وكم يُستعاد منه، وأيُّ إسقاطٍ يُسقِطه."""

    name: str
    what_it_carries: str
    what_is_recoverable_from_it_alone: str
    recovers_whole_input: bool
    is_droppable_in_a_projection: bool

    def __post_init__(self) -> None:
        for value, label in (
            (self.name, "اسمُ حقل الأثر"),
            (self.what_it_carries, "ما يحمله"),
            (self.what_is_recoverable_from_it_alone, "ما يُستعاد منه وحدَه"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise VvBirthAmendmentError(f"{label} نصٌّ غير فارغ")
        if not isinstance(self.recovers_whole_input, bool):
            raise VvBirthAmendmentError("استعادةُ المُدخَل كاملًا تصريحٌ منطقيّ")
        if self.recovers_whole_input:
            raise VvBirthAmendmentError(
                "حقلُ أثرٍ يُستعاد منه المُدخَلُ كاملًا نسخةٌ لا أثر: "
                "`TRACE_TAUTOLOGY` قبل أن يُشغَّل شيء"
            )
        if any(marker in self.name for marker in FORBIDDEN_TRACE_CONTENT):
            raise VvBirthAmendmentError(f"حقلُ الأثر {self.name!r} محتواه ممنوع")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى حقل الأثر للبصمة."""

        return {
            "name": self.name,
            "what_it_carries": self.what_it_carries,
            "what_is_recoverable_from_it_alone": (
                self.what_is_recoverable_from_it_alone
            ),
            "recovers_whole_input": self.recovers_whole_input,
            "is_droppable_in_a_projection": self.is_droppable_in_a_projection,
        }


TRACE_FIELD_SPECIFICATIONS: Final[tuple[TraceFieldSpecification, ...]] = (
    TraceFieldSpecification(
        name="source_vowel_quality",
        what_it_carries="جودةَ الصائت الأصليّ: قيمةٌ من ثلاثٍ لا أكثر",
        what_is_recoverable_from_it_alone=(
            "الجودةُ وحدَها؛ ولا يُستعاد منها موضعٌ ولا حاملٌ ولا كلمة"
        ),
        recovers_whole_input=False,
        is_droppable_in_a_projection=True,
    ),
    TraceFieldSpecification(
        name="extension_partner_identity",
        what_it_carries="هويّةَ الحامل الذي تحقّق به الامتداد: `ا` أو `و` أو `ي`",
        what_is_recoverable_from_it_alone=(
            "الحاملُ وحدَه؛ ولا يُستعاد منه ما قبله ولا ما بعده"
        ),
        recovers_whole_input=False,
        is_droppable_in_a_projection=True,
    ),
    TraceFieldSpecification(
        name="licence_reference",
        what_it_carries="إشارةً إلى بند الترخيص الذي أُجري تحته الامتداد",
        what_is_recoverable_from_it_alone="بندُ الترخيص؛ ولا مُدخَلَ فيه أصلًا",
        recovers_whole_input=False,
        is_droppable_in_a_projection=True,
    ),
)
"""حقولُ الأثر الثلاثةُ مُعلَنةً قبل بناء أثر؛ ولا رابعَ يُضاف في القراءة."""


def trace_projections_of(
    fields_in_trace: tuple[str, ...],
) -> tuple[tuple[str, ...], ...]:
    """`T' ≺_T T`: الإسقاطاتُ المسموحةُ، وهي حذفُ حقلٍ مُعلَنٍ واحدٍ فأكثر.

    والترتيبُ معلوماتيٌّ لا احتوائيّ: `T'` أدنى من `T` متى نتج عنه بإسقاط
    حقولٍ **مُسمّاةٍ سلفًا**؛ ولا يُقبَل حقلٌ خارجَ `TRACE_FIELD_SPECIFICATIONS`،
    لأنّ حقلًا غيرَ مُعلَنٍ قد يخبّئ المُدخَلَ كلَّه.
    """

    declared = {spec.name for spec in TRACE_FIELD_SPECIFICATIONS}
    for name in fields_in_trace:
        if name not in declared:
            raise VvBirthAmendmentError(
                f"حقلُ أثرٍ غيرُ مُعلَن: {name!r}؛ والأثرُ لا يُوسَّع في القراءة"
            )
    droppable = {
        spec.name
        for spec in TRACE_FIELD_SPECIFICATIONS
        if spec.is_droppable_in_a_projection
    }
    projections: list[tuple[str, ...]] = []
    for name in fields_in_trace:
        if name in droppable:
            projections.append(tuple(item for item in fields_in_trace if item != name))
    return tuple(projections)


# --- فرضيتا النوع: دعوى مقيَّدةٌ بمجموعة سياقاتٍ مُجمَّدة ----------------------


@dataclass(frozen=True, slots=True)
class ContextK0:
    """سياقٌ خارجيٌّ واحدٌ في `K_0`، مُسمًّى قبل أن يُشغَّل."""

    name: str
    what_it_places_the_centre_in: str
    what_it_observes: str

    def __post_init__(self) -> None:
        for value, label in (
            (self.name, "اسمُ السياق"),
            (self.what_it_places_the_centre_in, "موضعُ المركز فيه"),
            (self.what_it_observes, "ما يُشاهَد فيه"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise VvBirthAmendmentError(f"{label} نصٌّ غير فارغ")

    def as_canonical_content(self) -> dict[str, str]:
        """محتوى السياق للبصمة."""

        return {
            "name": self.name,
            "what_it_places_the_centre_in": self.what_it_places_the_centre_in,
            "what_it_observes": self.what_it_observes,
        }


CONTEXT_SET_K0: Final[tuple[ContextK0, ...]] = (
    ContextK0(
        name="k_word_final",
        what_it_places_the_centre_in="آخرَ الكلمة بلا ما بعده",
        what_it_observes="أيقبل المركزُ إغلاقًا بصامتٍ ساكنٍ بعده أم لا",
    ),
    ContextK0(
        name="k_before_cluster",
        what_it_places_the_centre_in="قبل صامتين ساكنين متتاليين",
        what_it_observes="أيلزم عن الموضع تغيّرٌ في الجوار أم لا شيء",
    ),
    ContextK0(
        name="k_before_shadda",
        what_it_places_the_centre_in="قبل شقٍّ أوّلَ من زوج تضعيف",
        what_it_observes="أيتغيّر تصنيفُ الشقّ باختلاف كمّيّة المركز أم لا",
    ),
    ContextK0(
        name="k_word_initial",
        what_it_places_the_centre_in="أوّلَ الكلمة بلا ما قبله",
        what_it_observes="أيقبل المركزُ الابتداءَ به على الكمّيّتين سواءً",
    ),
)
"""`K_0` مُجمَّدةً قبل التشغيل؛ وسياقٌ يُضاف بعد رؤية النتيجة سياقٌ مُنتقًى."""


@dataclass(frozen=True, slots=True)
class TypeDistinctionLaw:
    """قانونُ التمييز على `K_0`، ومخرَجاتُه الثلاثةُ وحدَها."""

    equivalence_law: str
    contexts: tuple[ContextK0, ...]
    admissible_outcomes: tuple[AmendmentOutcome, ...]
    what_not_distinguished_does_not_mean: str
    asymmetry_note: str

    def __post_init__(self) -> None:
        for value, label in (
            (self.equivalence_law, "قانونُ التكافؤ"),
            (self.what_not_distinguished_does_not_mean, "ما لا يعنيه عدمُ التمييز"),
            (self.asymmetry_note, "بيانُ عدم التناظر"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise VvBirthAmendmentError(f"{label} نصٌّ غير فارغ")
        if len(self.contexts) < 2:
            raise VvBirthAmendmentError(
                "مجموعةُ سياقاتٍ بسياقٍ واحدٍ لا تُقيِّد دعوى؛ فاثنان فأكثر"
            )
        if self.admissible_outcomes != (
            AmendmentOutcome.DISTINGUISHED_ON_K0,
            AmendmentOutcome.NOT_DISTINGUISHED_ON_K0,
            AmendmentOutcome.UNDERPOWERED,
        ):
            raise VvBirthAmendmentError(
                "المخرَجُ ثلاثةٌ بعينها وبترتيبها؛ ولا مساواةَ نوعٍ فيها"
            )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى القانون للبصمة."""

        return {
            "equivalence_law": self.equivalence_law,
            "contexts": [context.as_canonical_content() for context in self.contexts],
            "admissible_outcomes": [
                outcome.value for outcome in self.admissible_outcomes
            ],
            "what_not_distinguished_does_not_mean": (
                self.what_not_distinguished_does_not_mean
            ),
            "asymmetry_note": self.asymmetry_note,
        }


TYPE_DISTINCTION_LAW: Final[TypeDistinctionLaw] = TypeDistinctionLaw(
    equivalence_law=(
        "`CV ≡_{K_0} CVV ⟺ ∀ k ∈ K_0: Obs(k[CV]) = Obs(k[CVV])`؛ والدعوى "
        "مقيَّدةٌ بـ`K_0` نصًّا، لا مُطلَقةٌ على كلّ سياقٍ ممكن"
    ),
    contexts=CONTEXT_SET_K0,
    admissible_outcomes=(
        AmendmentOutcome.DISTINGUISHED_ON_K0,
        AmendmentOutcome.NOT_DISTINGUISHED_ON_K0,
        AmendmentOutcome.UNDERPOWERED,
    ),
    what_not_distinguished_does_not_mean=(
        "`NOT_DISTINGUISHED_ON_K0` **لا تعني** `Type(CV) = Type(CVV)`: هي "
        "قولٌ عن `K_0` وحدَها، وقد يكون المميِّزُ سياقًا لم يدخلها"
    ),
    asymmetry_note=(
        "الفرضيّتان غيرُ متناظرتين منطقيًّا: `H_same_type` يكفي لتفنيدها سياقٌ "
        "واحدٌ يفرّق؛ أمّا `H_different_type` فلا يفنّدها انعدامُ العثور، إذ "
        "انعدامُ الوجدان على مجموعةٍ منتهيةٍ ليس وجدانًا للعدم. فالمُسجَّلُ هنا "
        "أنّ عدمَ التمييز على `K_0` **لا يُفنِّد** `H_different_type`"
    ),
)
"""قانونُ التمييز مقيَّدًا بـ`K_0`؛ وهذا تصحيحُ عدمِ تناظرٍ منطقيٍّ لا تضييقُ نطاق."""


# --- مواقعُ الدلالة: قائمةٌ مستقلّةٌ ثانيةٌ مكتوبةٌ بيد ------------------------


REQUIRED_AMENDMENT_SITES: Final[tuple[tuple[str, str], ...]] = (
    ("vv_birth_amendment", "SUPERSEDED_PREREGISTRATION_PARENT"),
    ("vv_birth_amendment", "EXTENSION_OPERATOR_SPECIFICATION"),
    ("vv_birth_amendment", "ADVERSARIAL_EXTENSION_OPERATORS"),
    ("vv_birth_amendment", "EXTENSION_COUNT_AMENDMENT"),
    ("vv_birth_amendment", "WEAKER_MODEL_IMPLEMENTATIONS"),
    ("vv_birth_amendment", "IDENTITY_PROJECTION_FORBIDDEN_PROVENANCE"),
    ("vv_birth_amendment", "TRACE_FIELD_SPECIFICATIONS"),
    ("vv_birth_amendment", "FORBIDDEN_TRACE_CONTENT"),
    ("vv_birth_amendment", "CONTEXT_SET_K0"),
    ("vv_birth_amendment", "TYPE_DISTINCTION_LAW"),
    ("vv_birth_amendment", "AMENDMENT_DIGEST"),
)
"""المواقعُ التي يجب أن تبقى في هذا التعديل، مكتوبةً بيدٍ لا مشتقّةً من نصّه.

وهي قائمةٌ **ثانيةٌ مستقلّة**، لأنّ قائمةَ الأب مختومةٌ فلا تُوسَّع؛ وتوسيعُها
كان تحريرًا لأبٍ مختوم.
"""


def missing_amendment_sites() -> tuple[tuple[str, str], ...]:
    """المواقعُ المطلوبةُ الغائبةُ فعلًا من هذا التعديل، بالتشغيل لا بالادّعاء."""

    missing: list[tuple[str, str]] = []
    for module_name, site in REQUIRED_AMENDMENT_SITES:
        module = importlib.import_module(f".{module_name}", __package__)
        if not hasattr(module, site):
            missing.append((module_name, site))
        elif site not in getattr(module, "__all__", ()):
            missing.append((module_name, site))
    return tuple(missing)


# --- انعدامُ القراءة في هذا الالتزام ---------------------------------------


def readout_module_is_absent() -> bool:
    """أما زالت وحدةُ القراءة معدومةً؟ يُفحَص بالاسم لا بالوعد."""

    return importlib.util.find_spec(READOUT_MODULE_NAME) is None


# --- البواقي المُسمّاة --------------------------------------------------------


AN_EXISTENTIAL_OPERATOR_IS_A_BLANK_CHEQUE: Final[str] = (
    "AnExistentialOperatorIsABlankCheque: `∃E` لا تمنع أن تُكتَب دالّةُ `E` في "
    "الالتزام التالي على مقاس البيانات، فيصير اختبارُ `H_E` لاحقًا لا سابقًا؛ "
    "ولذلك جُمِّدت خطواتُه ومدخلاتُه قبل أن تُقرأ بايتة"
)

A_BAN_BY_NAME_IS_DEFEATED_BY_A_RENAME: Final[str] = (
    "ABanByNameIsDefeatedByARename: منعُ `carrier_codepoint` و`letter_index` "
    "بالاسم يُنقَض بإعادة التسمية إلى `unicode_scalar`؛ فالمنعُ هنا بالنسب "
    f"لا بالاسم، والأسماءُ المختومةُ {list(BANNED_IDENTITY_PROXIES)!r} تبقى "
    "قائمةً بوصفها أمثلةً لا بوصفها الحاجز"
)

A_CRITERION_NOTHING_FAILS_MEASURES_NOTHING: Final[str] = (
    "ACriterionNothingFailsMeasuresNothing: معيارٌ لا يُفشِل ضابطًا مضادًّا "
    "ينجح لكلّ تحويلٍ اعتباطيّ، فنجاحُه خاصّيّةُ الصياغة لا خاصّيّةُ المؤثّر؛ "
    "والمخرَجُ حينئذٍ `REPRESENTATION_TAUTOLOGY`"
)

A_DOMAIN_THAT_CONTRADICTS_ITS_CODOMAIN_IS_NOT_FROZEN: Final[str] = (
    "ADomainThatContradictsItsCodomainIsNotFrozen: مجالٌ يُجيز امتدادين "
    "ومجالُ إسقاطٍ `{1, 2}` متناقضان؛ وأحدُهما كان سيُضغَط قسرًا في القراءة، "
    "فالتقييدُ `#Extension ∈ {0, 1}` مُجمَّدٌ قبلها"
)

A_RIVAL_WRITTEN_AFTER_THE_RESULT_IS_NOT_A_RIVAL: Final[str] = (
    "ARivalWrittenAfterTheResultIsNotARival: نموذجٌ أضعفُ موصوفٌ بالنثر "
    "تُكتَب دالّتُه في القراءة أضعفَ أو أقوى بحسب ما خرج؛ فجُمِّدت خطواتُه "
    "مُرقَّمةً قبل التشغيل"
)

A_SINGLE_FIELD_CAN_HIDE_THE_WHOLE_INPUT: Final[str] = (
    "ASingleFieldCanHideTheWholeInput: `T' ⊊ T` مُعرَّفةٌ على مجموعاتٍ لا على "
    "سجلٍّ مصنَّف، وحقلٌ واحدٌ قد يخزّن تسلسلَ المُدخَل كاملًا فينجح شرطُ حذف "
    "الحقول والأثرُ نسخة؛ فصار الترتيبُ `T' ≺_T T` إسقاطًا مُعلَنًا، ومنعُ "
    "الاستعادة الكاملة بنيويًّا في `TraceFieldSpecification`"
)

ABSENCE_ON_A_FINITE_CONTEXT_SET_IS_NOT_IDENTITY_OF_TYPE: Final[str] = (
    "AbsenceOnAFiniteContextSetIsNotIdentityOfType: `NOT_DISTINGUISHED_ON_K0` "
    "قولٌ عن `K_0` المنتهية وحدَها؛ وقراءتُها `Type(CV) = Type(CVV)` استدلالٌ "
    "من عدم الوجدان على وجدان العدم"
)

AN_AMENDMENT_THAT_EDITS_ITS_PARENT_BREAKS_THE_SEAL: Final[str] = (
    "AnAmendmentThatEditsItsParentBreaksTheSeal: إصلاحُ عيبٍ بتحرير "
    "`vv_birth_hypothesis` أو `vv_birth_preregistration` كان سيُغيّر "
    "`PREREGISTRATION_DIGEST`، فيُبطل الختمَ الذي عليه تقوم القراءةُ القادمة؛ "
    "فلم يُمَسّ منهما حرف، وكلُّ تعديلٍ في هذه الوحدة وحدَها"
)

THE_AMENDMENT_SUPERSEDES_EXECUTION_NOT_HYPOTHESES: Final[str] = (
    "TheAmendmentSupersedesExecutionNotHypotheses: مدى هذا التعديل تفاصيلُ "
    "التنفيذ وحدَها؛ ولم تُعدَّل فرضيةٌ ولا مُفنِّدٌ ولا سقفُ مخرَج، و"
    "`SUPERSEDED_PREREGISTRATION_PARENT` يحمل بصمةَ الأب ومحتواه شاهدًا"
)


VV_BIRTH_AMENDMENT_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_BAN_BY_NAME_IS_DEFEATED_BY_A_RENAME,
    A_CRITERION_NOTHING_FAILS_MEASURES_NOTHING,
    A_DOMAIN_THAT_CONTRADICTS_ITS_CODOMAIN_IS_NOT_FROZEN,
    A_RIVAL_WRITTEN_AFTER_THE_RESULT_IS_NOT_A_RIVAL,
    A_SINGLE_FIELD_CAN_HIDE_THE_WHOLE_INPUT,
    ABSENCE_ON_A_FINITE_CONTEXT_SET_IS_NOT_IDENTITY_OF_TYPE,
    AN_AMENDMENT_THAT_EDITS_ITS_PARENT_BREAKS_THE_SEAL,
    AN_EXISTENTIAL_OPERATOR_IS_A_BLANK_CHEQUE,
    THE_AMENDMENT_SUPERSEDES_EXECUTION_NOT_HYPOTHESES,
)
"""البواقي المُسمّاةُ لهذه الوحدة، مرتّبةً كما تُرتَّب في بقيّة الطبقة."""


def amendment_digest() -> str:
    """بصمةُ التعديل، مُعادةَ الاشتقاق من محتواه لا مكتوبةً رقمًا في الشيفرة."""

    return canonical_digest(
        canonical_bytes(
            {
                "amendment_id": AMENDMENT_ID,
                "superseded_parent": (
                    SUPERSEDED_PREREGISTRATION_PARENT.as_canonical_content()
                ),
                "extension_operator": (
                    EXTENSION_OPERATOR_SPECIFICATION.as_canonical_content()
                ),
                "adversarial_operators": [
                    operator.as_canonical_content()
                    for operator in ADVERSARIAL_EXTENSION_OPERATORS
                ],
                "extension_count_amendment": (
                    EXTENSION_COUNT_AMENDMENT.as_canonical_content()
                ),
                "weaker_model_implementations": [
                    implementation.as_canonical_content()
                    for implementation in WEAKER_MODEL_IMPLEMENTATIONS
                ],
                "identity_projection_forbidden_provenance": sorted(
                    provenance.value
                    for provenance in IDENTITY_PROJECTION_FORBIDDEN_PROVENANCE
                ),
                "trace_fields": [
                    spec.as_canonical_content() for spec in TRACE_FIELD_SPECIFICATIONS
                ],
                "forbidden_trace_content": list(FORBIDDEN_TRACE_CONTENT),
                "required_amendment_sites": [
                    list(site) for site in REQUIRED_AMENDMENT_SITES
                ],
                "type_distinction_law": TYPE_DISTINCTION_LAW.as_canonical_content(),
                "named_residuals": list(VV_BIRTH_AMENDMENT_NAMED_RESIDUALS),
            }
        )
    )


AMENDMENT_DIGEST: Final[str] = amendment_digest()
"""بصمةُ التعديل؛ وحدُّ ما تكشفه حدُّ ما تكشفه بصمةُ الأب: تغيّرًا بين التزامين."""


_FORBIDDEN_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "observed_outcome",
    "verdict",
    "birth_decision",
    "born",
    "score",
    "measured",
    "e0",
)


def _refuse_an_execution_left_open() -> None:
    """حارسٌ عند الاستيراد: حرّيّةٌ تنفيذيّةٌ بقيت، أو قراءةٌ حضرت، أو أبٌ مُسّ."""

    for declaring_type in (
        SupersededPreregistrationParent,
        InputField,
        ExtensionOperatorSpecification,
        AdversarialOperator,
        ExtensionCountAmendment,
        WeakerModelImplementation,
        TraceFieldSpecification,
        ContextK0,
        TypeDistinctionLaw,
    ):
        declared = {item.name for item in fields(declaring_type)}
        for marker in _FORBIDDEN_FIELD_MARKERS:
            if any(marker in name for name in declared):
                raise VvBirthAmendmentError(
                    f"حقلُ {marker!r} حكمٌ لا شرط، فلا يكون في تجميدٍ قبليّ"
                )
    if any(
        outcome.value == "BORN" or outcome.name == "BORN"
        for outcome in AmendmentOutcome
    ):
        raise VvBirthAmendmentError("`BORN` ليست حالةً يزيدها تعديلُ تنفيذ")
    if SUPERSEDED_PREREGISTRATION_PARENT.content_digest != PREREGISTRATION_DIGEST:
        raise VvBirthAmendmentError(
            "بصمةُ الأب المُسجَّلةُ تخالف بصمةَ المُجمَّد القائم: الأبُ مُسّ"
        )
    implemented = {
        implementation.name for implementation in WEAKER_MODEL_IMPLEMENTATIONS
    }
    for name in ("M_drop", "M_consonant", "M_second_vowel", "M_no_join"):
        if name not in implemented:
            raise VvBirthAmendmentError(
                f"منافسٌ بلا خوارزميّةٍ مُجمَّدة: {name!r}؛ ولا تُكتَب في القراءة"
            )
    if weaker_model_implementation_named("M_identity_lookup").counts_as_evidence:
        raise VvBirthAmendmentError("مقياسُ التسريب لا يُحتَجّ به دليلًا بحال")
    for field in EXTENSION_OPERATOR_SPECIFICATION.allowed_inputs:
        if field.provenance is ProvenanceClass.MODEL_OUTPUT:
            raise VvBirthAmendmentError("مخرَجُ نموذجٍ في مدخلات `E` دائرةٌ مغلقة")
    if not any(
        "MADD_EXTENSION" in source
        for source in EXTENSION_OPERATOR_SPECIFICATION.forbidden_sources
    ):
        raise VvBirthAmendmentError(
            "منعُ `PhoneticRole.MADD_EXTENSION` لازمٌ صريحًا في مصادر `E`"
        )
    missing = missing_amendment_sites()
    if missing:
        raise VvBirthAmendmentError(f"مواقعُ دلالةٍ مطلوبةٌ ساقطةٌ من التعديل: {missing!r}")
    if len(set(REQUIRED_AMENDMENT_SITES)) != len(REQUIRED_AMENDMENT_SITES):
        raise VvBirthAmendmentError("موقعُ دلالةٍ تكرّر في القائمة المستقلّة")
    if len(ADVERSARIAL_EXTENSION_OPERATORS) < 3:
        raise VvBirthAmendmentError("الضوابطُ المضادّةُ ثلاثةٌ فأكثرُ قبل القراءة")
    if any(spec.recovers_whole_input for spec in TRACE_FIELD_SPECIFICATIONS):
        raise VvBirthAmendmentError("حقلُ أثرٍ يستعيد المُدخَلَ كاملًا نسخةٌ لا أثر")
    if not readout_module_is_absent():
        raise VvBirthAmendmentError(
            "التعديلُ التزامٌ بلا قراءة؛ ووجودُ وحدة القراءة يُبطل ترتيبَ التاريخ"
        )
    if list(VV_BIRTH_AMENDMENT_NAMED_RESIDUALS) != sorted(
        VV_BIRTH_AMENDMENT_NAMED_RESIDUALS
    ):
        raise VvBirthAmendmentError("البواقي المُسمّاةُ تُرتَّب ترتيبًا ثابتًا")


_refuse_an_execution_left_open()
