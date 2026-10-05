"""السؤالُ يُحدِّد الحدَّ الأدنى المكتمل، وفرقُ اللاتكرار عن الأصغريّة الشاملة.

**ولا تتساوى كفايةُ المقدّمات باختلاف السؤال**
(`A_SYNTACTIC_QUESTION_IS_NOT_A_FACTUAL_ONE`): «من الفاعلُ النحويّ؟» يكفيه
تحليلُ العبارة وحدَه، و«هل وقع الحدث؟» يحتاج دليلًا عن الواقع، و«ما حالُ الباب
الآن؟» يحتاج فوق ذلك دليلًا في زمنٍ يشمل زمنَ السؤال أو قاعدةَ استمرارٍ
مُصرَّحةً بموانعها. والمتطلّباتُ **تُشتَقّ من نوع السؤال والقواعد المتاحة** ولا
تُكتَب جدولًا ثابتًا.

**واللاتكرارُ غيرُ الأصغريّة الشاملة**
(`IRREDUNDANCY_IN_ONE_PROOF_IS_NOT_GLOBAL_MINIMALITY`):

* `is_irredundant_for_this_proof` — حُذِف كلُّ عنصرٍ على حدةٍ فسقط هذا البرهان.
  وهذا **مُثبَتٌ بالتشغيل**: الحذفُ يُجرَّب فعلًا ويُقاس أثرُه.
* `global_minimality` — لا تُقال إلّا إذا صُرِّح بفضاء البراهين البديلة
  وفُحِص؛ وإلّا فالقيمةُ `UNDECLARED` ولا تُقرَأ نفيًا. وقد يوجد أكثرُ من
  مسارٍ كافٍ للحكم نفسه، فتعدّدُ المسارات مُسجَّلٌ لا مطويّ.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Final

from .epistemics import Scope
from .inference import SupportStatus
from .substance import Declared, RuleKind, SubstanceStore

__all__ = [
    "A_SYNTACTIC_QUESTION_IS_NOT_A_FACTUAL_ONE",
    "IRREDUNDANCY_IN_ONE_PROOF_IS_NOT_GLOBAL_MINIMALITY",
    "MinimalityReading",
    "PremiseRequirement",
    "Question",
    "QuestionError",
    "QuestionKind",
    "RequirementGenus",
    "deletion_test",
    "requirements_for",
]


class QuestionError(ValueError):
    """رفضٌ بنيويٌّ في طبقة السؤال؛ لا حملَ على أقرب حالة."""


A_SYNTACTIC_QUESTION_IS_NOT_A_FACTUAL_ONE: Final[str] = (
    "كفايةُ مقدّمات «من الفاعلُ النحويّ؟» ليست كفايةَ «هل وقع الحدث؟»: الأوّلُ "
    "يُقطَع بتحليل العبارة، والثاني يحتاج دليلًا عن الواقع؛ ومن سوّى بينهما "
    "جعل الوسمَ النحويَّ خبرًا عن العالَم"
)

IRREDUNDANCY_IN_ONE_PROOF_IS_NOT_GLOBAL_MINIMALITY: Final[str] = (
    "لاتكرارُ مقدّماتِ برهانٍ ليس أصغريّةً بين كلّ البراهين: الأوّلُ يُثبَت "
    "بحذف كلّ عنصرٍ من هذا البرهان، والثاني يحتاج تحديدَ فضاء البدائل وفحصَه؛ "
    "وادّعاءُ الثاني بدليل الأوّل قفزٌ"
)


class QuestionKind(Enum):
    """أنواعُ الأسئلة المنفَّذة؛ مفردةٌ مغلقةٌ فيها عضوٌ لما خرج عن النطاق."""

    SYNTACTIC_FUNCTION = "syntactic_function"
    SEMANTIC_ROLE = "semantic_role"
    REFERENT_IDENTITY = "referent_identity"
    TYPE_MEMBERSHIP = "type_membership"
    EVENT_OCCURRENCE = "event_occurrence"
    CURRENT_STATE = "current_state"
    OUT_OF_SCOPE = "out_of_scope"


class RequirementGenus(Enum):
    """جنسُ المقدّمة المطلوبة؛ يُسمّي من أين تأتي لا أنّها مطلوبة فحسب."""

    SURFACE_ANALYSIS = "surface_analysis"
    LEXICAL_SENSE = "lexical_sense"
    SUBSTANCE_ENTRY = "substance_entry"
    DISCOURSE_CONTENT = "discourse_content"
    ACCEPTED_FACT = "accepted_fact"
    LICENSED_RULE = "licensed_rule"


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise QuestionError(f"{label} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class PremiseRequirement:
    """مقدّمةٌ مطلوبةٌ لحكمٍ بعينه: جنسُها، وبيانُها، وهل هي لازمةٌ أم مُعينة."""

    requirement_id: str
    genus: RequirementGenus
    statement: str
    obligatory: bool

    def __post_init__(self) -> None:
        _require_text(self.requirement_id, "مُعرِّفُ المقدّمة المطلوبة")
        if not isinstance(self.genus, RequirementGenus):
            raise QuestionError("جنسُ المقدّمة عضوٌ في مفردته المغلقة")
        _require_text(self.statement, "بيانُ المقدّمة المطلوبة")
        if not isinstance(self.obligatory, bool):
            raise QuestionError("لزومُ المقدّمة قيمةٌ ثنائيّةٌ مُصرَّح بها")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المقدّمة للبصمة."""

        return {
            "requirement_id": self.requirement_id,
            "genus": self.genus.value,
            "statement": self.statement,
            "obligatory": self.obligatory,
        }


@dataclass(frozen=True, slots=True)
class Question:
    """سؤالٌ واحد: نصُّه، ونوعُه، وموضوعُه، ومحموله، ونطاقُه الزمنيّ."""

    question_id: str
    text: str
    kind: QuestionKind
    subject_id: str
    predicate_id: str
    scope: Scope

    def __post_init__(self) -> None:
        _require_text(self.question_id, "مُعرِّفُ السؤال")
        _require_text(self.text, "نصُّ السؤال")
        if not isinstance(self.kind, QuestionKind):
            raise QuestionError("نوعُ السؤال عضوٌ في مفردته المغلقة")
        _require_text(self.subject_id, "موضوعُ السؤال")
        _require_text(self.predicate_id, "محمولُ السؤال")
        if not isinstance(self.scope, Scope):
            raise QuestionError("نطاقُ السؤال نطاقٌ قائم")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى السؤال للبصمة."""

        return {
            "question_id": self.question_id,
            "text": self.text,
            "kind": self.kind.value,
            "subject_id": self.subject_id,
            "predicate_id": self.predicate_id,
            "scope": self.scope.as_canonical_content(),
        }


def requirements_for(
    question: Question, store: SubstanceStore
) -> tuple[PremiseRequirement, ...]:
    """اشتقّ متطلّباتِ الحكم من **نوع السؤال والقواعد المتاحة** لا من جدولٍ ثابت.

    المدخل: سؤالٌ، ورصيدٌ فيه القواعد.
    الشرط: نوعُ السؤال منفَّذ؛ و`OUT_OF_SCOPE` يُخرِج صفرَ متطلّبات تصريحًا.
    المخرج: متطلّباتٌ مُسمّاةُ الجنس، وفيها اللازمُ والمُعين.
    حدُّها: لا تُخبِر أنّ المتطلّباتِ مستوفاة؛ تقول ما يلزم فحسب.
    """

    if not isinstance(question, Question):
        raise QuestionError("السؤالُ سؤالٌ قائم")
    if question.kind is QuestionKind.OUT_OF_SCOPE:
        return ()
    surface = PremiseRequirement(
        requirement_id="تحليل-سطحيّ",
        genus=RequirementGenus.SURFACE_ANALYSIS,
        statement="تحليلٌ مشتقٌّ من بايتات العبارة يُخرِج وظائفَها النحويّة",
        obligatory=True,
    )
    if question.kind is QuestionKind.SYNTACTIC_FUNCTION:
        return (surface,)
    sense = PremiseRequirement(
        requirement_id="معنًى-معتمَد",
        genus=RequirementGenus.LEXICAL_SENSE,
        statement="معنًى معجميٌّ معتمدٌ بمصدره، يُحدِّد نوعَ الحدث وأدوارَه",
        obligatory=True,
    )
    entry = PremiseRequirement(
        requirement_id="بندُ-رصيد",
        genus=RequirementGenus.SUBSTANCE_ENTRY,
        statement=f"بندٌ في الرصيد يُعرِّف `{question.predicate_id}` وشروطَه",
        obligatory=True,
    )
    content = PremiseRequirement(
        requirement_id="مضمونُ-خطاب",
        genus=RequirementGenus.DISCOURSE_CONTENT,
        statement="مضمونٌ منسوبٌ إلى العبارة، محفوظُ القطبيّة والجهة والنطاق",
        obligatory=True,
    )
    if question.kind in (QuestionKind.SEMANTIC_ROLE, QuestionKind.REFERENT_IDENTITY):
        return (surface, sense, entry, content)
    if question.kind is QuestionKind.TYPE_MEMBERSHIP:
        return (
            entry,
            PremiseRequirement(
                requirement_id="إسنادٌ-مقبول",
                genus=RequirementGenus.ACCEPTED_FACT,
                statement="إسنادُ صفةٍ أو جزءٍ أو قدرةٍ يُختبَر به شرطُ الانتماء",
                obligatory=True,
            ),
        )
    fact = PremiseRequirement(
        requirement_id="واقعةٌ-مقبولة",
        genus=RequirementGenus.ACCEPTED_FACT,
        statement=(
            "قضيّةٌ مقبولةٌ بدليلٍ يُثبِت، نطاقُها يشمل نطاقَ السؤال؛ "
            "ومضمونُ العبارة وحدَه لا يقوم مقامَها"
        ),
        obligatory=True,
    )
    if question.kind is QuestionKind.EVENT_OCCURRENCE:
        return (surface, sense, entry, content, fact)
    persistence_rules = tuple(
        rule
        for rule in store.rules
        if rule.kind is RuleKind.DEFEASIBLE and "استمرار" in rule.rule_id
    )
    requirements = [surface, sense, entry, content, fact]
    for rule in persistence_rules:
        requirements.append(
            PremiseRequirement(
                requirement_id=f"قاعدةُ-{rule.rule_id}",
                genus=RequirementGenus.LICENSED_RULE,
                statement=(
                    f"قاعدةٌ `{rule.versioned_id}` قابلةٌ للنقض، موانعُها: "
                    + "، ".join(rule.blocker_ids)
                ),
                obligatory=False,
            )
        )
    return tuple(requirements)


@dataclass(frozen=True, slots=True)
class MinimalityReading:
    """قراءةُ أصغريّةٍ: لاتكرارٌ **مُثبَتٌ بالحذف**، وأصغريّةٌ شاملةٌ لا تُدَّعى بلا فضاء."""

    proof_premise_ids: tuple[str, ...]
    removable_premise_ids: tuple[str, ...]
    global_minimality: Declared
    alternative_proof_count: int | None
    note: str

    def __post_init__(self) -> None:
        if not isinstance(self.global_minimality, Declared):
            raise QuestionError("الأصغريّةُ الشاملةُ ثلاثيّةُ الإعلان")
        if (
            self.global_minimality is not Declared.UNDECLARED
            and self.alternative_proof_count is None
        ):
            raise QuestionError(
                IRREDUNDANCY_IN_ONE_PROOF_IS_NOT_GLOBAL_MINIMALITY
                + "؛ ولا تُعلَن أصغريّةٌ شاملةٌ بلا عددٍ مفحوصٍ من البدائل"
            )
        _require_text(self.note, "بيانُ قراءة الأصغريّة")

    @property
    def is_irredundant_for_this_proof(self) -> bool:
        """أسقط البرهانُ بحذف كلّ عنصرٍ على حدة؟ خاصّيّةٌ تُشتَقّ من التشغيل."""

        return not self.removable_premise_ids

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى القراءة للبصمة."""

        return {
            "proof_premise_ids": list(self.proof_premise_ids),
            "removable_premise_ids": list(self.removable_premise_ids),
            "global_minimality": self.global_minimality.value,
            "alternative_proof_count": self.alternative_proof_count,
            "note": self.note,
        }


def deletion_test(
    proof_premise_ids: Sequence[str],
    prove: Callable[[Sequence[str]], SupportStatus],
    alternative_proof_count: int | None = None,
) -> MinimalityReading:
    """احذف كلّ مقدّمةٍ على حدةٍ **وشغِّل البرهان**، ثمّ اقرأ اللاتكرار.

    المدخل: مقدّماتُ برهانٍ، ودالّةُ برهانٍ تُعاد تشغيلُها على ما بقي.
    الشرط: البرهانُ بكامل مقدّماته يحسم؛ وإلّا فالحذفُ لا يقيس شيئًا.
    المخرج: قراءةٌ تُسمّي ما أمكن حذفُه دون أن يسقط البرهان.
    حدُّها: لا تقول شيئًا عن براهينَ أخرى ما لم يُصرَّح بفضائها ويُفحَص.
    """

    premises = tuple(proof_premise_ids)
    if not premises:
        raise QuestionError("اختبارُ الحذف يحتاج مقدّمةً فأكثر")
    baseline = prove(premises)
    if not baseline.is_decided:
        raise QuestionError(
            "البرهانُ بكامل مقدّماته لم يحسم؛ وحذفُ مقدّمةٍ منه لا يقيس لزومَها"
        )
    removable: list[str] = []
    for premise_id in premises:
        remaining = tuple(item for item in premises if item != premise_id)
        if prove(remaining).is_decided:
            removable.append(premise_id)
    declared = (
        Declared.UNDECLARED
        if alternative_proof_count is None
        else (Declared.YES if alternative_proof_count == 1 else Declared.NO)
    )
    note = (
        IRREDUNDANCY_IN_ONE_PROOF_IS_NOT_GLOBAL_MINIMALITY
        if alternative_proof_count is None
        else f"فضاءُ البراهين المُصرَّحُ به مفحوصٌ، وعددُه {alternative_proof_count}"
    )
    return MinimalityReading(
        proof_premise_ids=premises,
        removable_premise_ids=tuple(removable),
        global_minimality=declared,
        alternative_proof_count=alternative_proof_count,
        note=note,
    )
