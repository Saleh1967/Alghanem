"""التحقّقُ المستقلُّ ثمّ القبولُ النهائيّ، مربوطَين بكلّ عنصرٍ مؤثِّر.

**والتحقّقُ ليس حالةَ نجاحٍ ولا بصماتٍ صحيحة**
(`A_PASS_FLAG_IS_NOT_A_VERIFICATION`): المتحقِّقُ يفحص خمسةَ مواضعَ بأعيانها،
ويُسمّي كلَّ إخفاقٍ منها على حدة:

1. **المقدّمات** — كلُّ مقدّمةٍ قائمةٌ غيرُ معلَّقةٍ وبصمةُ دليلها مطابقة.
2. **تطبيقُ القواعد** — القاعدةُ في الرصيد، وإصدارُها هو المذكور، ولا مانعَ قائم.
3. **الأطراف** — موضوعُ الجواب هو موضوعُ السؤال، ومحمولُه محمولُه.
4. **النطاق** — نطاقُ المقدّمات يشمل نطاقَ السؤال؛ وإثباتُ حالٍ في زمنٍ مشاهَدٍ
   لا يُقرَأ تعميمًا إلى فترةٍ لم تُشاهَد.
5. **الصلةُ بالسؤال** — نوعُ السؤال يطابق صورةَ القضيّة المُجاب بها.

**والقبولُ مربوطٌ بإصداراتٍ وبصمات** (`AcceptanceRecord`): بصمةُ الرصيد، وبصمةُ
السجلّ، وبصمةُ المضمون، وأدلّةٌ بإصداراتها، وقواعدُ بإصداراتها. فإن تغيّر عنصرٌ
مؤثِّرٌ صارت الشهادةُ **قديمةً** (`is_stale_against`) ووجب إعادةُ التحقّق؛ ولا
تُقرَأ سارية لأنّها نجحت مرّة.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from .content import DiscourseContent
from .facts import FactRegister, PropositionForm
from .inference import Derivation, SupportStatus
from .question import Question, QuestionKind
from .substance import SubstanceStore

__all__ = [
    "A_PASS_FLAG_IS_NOT_A_VERIFICATION",
    "A_VERIFICATION_IS_BOUND_TO_WHAT_IT_READ",
    "AcceptanceRecord",
    "Answer",
    "VerificationCheck",
    "VerificationError",
    "VerificationReport",
    "accept",
    "verify",
]


class VerificationError(ValueError):
    """رفضٌ بنيويٌّ في طبقة التحقّق؛ لا حملَ على أقرب حالة."""


A_PASS_FLAG_IS_NOT_A_VERIFICATION: Final[str] = (
    "حالةُ نجاحٍ ليست تحقّقًا: المتحقِّقُ يُسمّي المواضعَ التي فحصها وما وجده "
    "في كلٍّ منها؛ ومن اكتفى بـ«مرّ» سلّم للقارئ حكمًا لا يستطيع مراجعتَه"
)

A_VERIFICATION_IS_BOUND_TO_WHAT_IT_READ: Final[str] = (
    "التحقّقُ مربوطٌ بما قرأه: بصمةُ الرصيد والسجلّ والمضمون وإصداراتُ "
    "القواعد؛ فإن تغيّر واحدٌ منها فالشهادةُ قديمةٌ ويُعاد التحقّق، ولا تُقرَأ "
    "سارية لأنّها نجحت مرّة"
)


class VerificationCheck(Enum):
    """مواضعُ الفحص الخمسة؛ مفردةٌ مغلقةٌ تُقرَأ في التقرير موضعًا موضعًا."""

    PREMISES_STANDING = "premises_standing"
    RULE_APPLICATION = "rule_application"
    ARGUMENTS_MATCH = "arguments_match"
    SCOPE_COVERAGE = "scope_coverage"
    RELEVANCE_TO_QUESTION = "relevance_to_question"


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise VerificationError(f"{label} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class Answer:
    """جوابٌ عن سؤال: حالُه، وأثرُ استدلاله، ونصُّه، وما نقصه إن لم يُحسَم."""

    question_id: str
    status: SupportStatus
    derivation: Derivation
    statement: str

    def __post_init__(self) -> None:
        _require_text(self.question_id, "مُعرِّفُ السؤال في الجواب")
        if not isinstance(self.status, SupportStatus):
            raise VerificationError("حالُ الجواب عضوٌ في مفردته المغلقة")
        if not isinstance(self.derivation, Derivation):
            raise VerificationError("أثرُ الاستدلال أثرٌ قائم")
        if self.derivation.question_ref != self.question_id:
            raise VerificationError("أثرُ استدلالٍ عن سؤالٍ آخر: جوابٌ بلا صلة")
        if self.derivation.status is not self.status:
            raise VerificationError("حالُ الجواب تُخالف حالَ أثره: حقلٌ يُكتَب ولا يُشتَقّ")
        _require_text(self.statement, "نصُّ الجواب")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الجواب للبصمة."""

        return {
            "question_id": self.question_id,
            "status": self.status.value,
            "statement": self.statement,
            "derivation": self.derivation.as_canonical_content(),
        }


@dataclass(frozen=True, slots=True)
class VerificationReport:
    """تقريرُ تحقّقٍ: موضعٌ موضعًا، بسببٍ مُسمًّى لكلّ إخفاق."""

    question_id: str
    findings: tuple[tuple[VerificationCheck, bool, str], ...]

    def __post_init__(self) -> None:
        _require_text(self.question_id, "مُعرِّفُ السؤال في التقرير")
        seen = tuple(check for check, _, _ in self.findings)
        if set(seen) != set(VerificationCheck):
            raise VerificationError(
                A_PASS_FLAG_IS_NOT_A_VERIFICATION
                + "؛ والمواضعُ الخمسةُ تُفحَص كلُّها ولا يُسكَت عن واحدٍ منها"
            )

    @property
    def passed(self) -> bool:
        """أمرّت المواضعُ كلُّها؟ خاصّيّةٌ تُشتَقّ من المواضع لا حقلٌ يُكتَب."""

        return all(ok for _, ok, _ in self.findings)

    @property
    def failed_checks(self) -> tuple[VerificationCheck, ...]:
        """المواضعُ المُخفِقة؛ تُسمَّى جميعًا ولا يُوقَف عند أوّلها."""

        return tuple(check for check, ok, _ in self.findings if not ok)

    def reason_for(self, check: VerificationCheck) -> str:
        """ما وجده المتحقِّقُ في موضعٍ بعينه."""

        for item, _, reason in self.findings:
            if item is check:
                return reason
        raise VerificationError(f"لا موضعَ `{check.value}` في هذا التقرير")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التقرير للبصمة."""

        return {
            "question_id": self.question_id,
            "findings": [
                {"check": check.value, "ok": ok, "reason": reason}
                for check, ok, reason in sorted(
                    self.findings, key=lambda item: item[0].value
                )
            ],
        }


_FORM_FOR_QUESTION: Final[dict[QuestionKind, PropositionForm]] = {
    QuestionKind.EVENT_OCCURRENCE: PropositionForm.EVENT_OCCURRED,
    QuestionKind.CURRENT_STATE: PropositionForm.STATE_HOLDS,
    QuestionKind.TYPE_MEMBERSHIP: PropositionForm.TYPE_MEMBERSHIP,
}
"""صورةُ القضيّة التي يطلبها كلُّ نوعِ سؤالٍ منفَّذ؛ وما ليس فيها خارجُ النطاق."""


def verify(
    question: Question,
    answer: Answer,
    register: FactRegister,
    store: SubstanceStore,
) -> VerificationReport:
    """افحص الجوابَ في المواضع الخمسة فحصًا **مستقلًّا** عن منتجه.

    المدخل: سؤالٌ، وجوابٌ بأثره، وسجلٌّ، ورصيد.
    الشرط: لا شيء؛ الفحصُ يُجرى دائمًا ويُخرِج موضعًا موضعًا.
    المخرج: تقريرٌ فيه المواضعُ الخمسةُ بأسبابها.
    حدُّها: لا يُصحِّح جوابًا ولا يُكمِل مقدّمةً؛ يفحص فحسب.
    """

    findings: list[tuple[VerificationCheck, bool, str]] = []

    premises_ok = True
    premise_reasons: list[str] = []
    for premise_id in answer.derivation.premise_proposition_ids:
        try:
            premise = register.proposition_of(premise_id)
        except Exception as absence:  # noqa: BLE001 - يُعاد بنصّه لا بصنفه
            premises_ok = False
            premise_reasons.append(str(absence))
            continue
        if premise.suspended:
            premises_ok = False
            premise_reasons.append(f"مقدّمةٌ معلَّقة: `{premise_id}`")
            continue
        try:
            evidence = register.evidence_of(premise.evidence_ref.evidence_id)
        except Exception as absence:  # noqa: BLE001
            premises_ok = False
            premise_reasons.append(str(absence))
            continue
        if not premise.evidence_ref.matches(evidence):
            premises_ok = False
            premise_reasons.append(
                f"بصمةُ دليل المقدّمة `{premise_id}` تغيّرت بعد الإشارة إليه"
            )
    if answer.status.is_decided and not answer.derivation.premise_proposition_ids:
        premises_ok = False
        premise_reasons.append("حكمٌ محسومٌ بلا مقدّمةٍ مُسمّاة")
    findings.append(
        (
            VerificationCheck.PREMISES_STANDING,
            premises_ok,
            "؛ ".join(premise_reasons)
            if premise_reasons
            else "كلُّ مقدّمةٍ قائمةٌ وبصمةُ دليلها مطابقة",
        )
    )

    rules_ok = True
    rule_reasons: list[str] = []
    for versioned in answer.derivation.rule_versioned_ids:
        rule_id, _, version = versioned.partition("@")
        try:
            rule = store.rule_of(rule_id)
        except Exception as absence:  # noqa: BLE001
            rules_ok = False
            rule_reasons.append(str(absence))
            continue
        if rule.version != version:
            rules_ok = False
            rule_reasons.append(
                f"إصدارُ القاعدة `{rule_id}` في الرصيد `{rule.version}` "
                f"لا `{version}`؛ والحكمُ مربوطٌ بإصداره"
            )
    findings.append(
        (
            VerificationCheck.RULE_APPLICATION,
            rules_ok,
            "؛ ".join(rule_reasons)
            if rule_reasons
            else "القواعدُ المذكورةُ قائمةٌ بإصداراتها",
        )
    )

    arguments_ok = True
    argument_reasons: list[str] = []
    conclusion_id = answer.derivation.conclusion_proposition_id
    if conclusion_id is not None:
        try:
            conclusion = register.proposition_of(conclusion_id)
        except Exception as absence:  # noqa: BLE001
            arguments_ok = False
            argument_reasons.append(str(absence))
        else:
            if conclusion.subject_id != question.subject_id:
                arguments_ok = False
                argument_reasons.append(
                    f"موضوعُ الجواب `{conclusion.subject_id}` غيرُ موضوع السؤال "
                    f"`{question.subject_id}`"
                )
            if conclusion.predicate_id != question.predicate_id:
                arguments_ok = False
                argument_reasons.append(
                    f"محمولُ الجواب `{conclusion.predicate_id}` غيرُ محمول السؤال "
                    f"`{question.predicate_id}`"
                )
    findings.append(
        (
            VerificationCheck.ARGUMENTS_MATCH,
            arguments_ok,
            "؛ ".join(argument_reasons)
            if argument_reasons
            else "الأطرافُ مطابقةٌ لأطراف السؤال",
        )
    )

    scope_ok = True
    scope_reasons: list[str] = []
    for premise_id in answer.derivation.premise_proposition_ids:
        try:
            premise = register.proposition_of(premise_id)
        except Exception:  # noqa: BLE001 - سُمّي في موضع المقدّمات
            continue
        if not premise.scope.covers(question.scope):
            scope_ok = False
            scope_reasons.append(
                f"نطاقُ المقدّمة `{premise_id}` لا يشمل نطاقَ السؤال؛ وإثباتُ "
                "الحال في زمنٍ مشاهَدٍ ليس تعميمًا لفترةٍ لم تُشاهَد"
            )
    findings.append(
        (
            VerificationCheck.SCOPE_COVERAGE,
            scope_ok,
            "؛ ".join(scope_reasons)
            if scope_reasons
            else "نطاقُ المقدّمات يشمل نطاقَ السؤال",
        )
    )

    expected = _FORM_FOR_QUESTION.get(question.kind)
    relevance_ok = True
    relevance_reason = "صورةُ القضيّة تطابق نوعَ السؤال"
    if expected is None:
        relevance_ok = answer.status is SupportStatus.OUT_OF_SCOPE_OR_UNSUPPORTED
        relevance_reason = (
            "سؤالٌ خارجَ الصورِ المنفَّذة، والجوابُ يُسمّي ذلك"
            if relevance_ok
            else "سؤالٌ خارجَ الصورِ المنفَّذة وجوابُه يدّعي حسمًا"
        )
    elif conclusion_id is not None:
        try:
            conclusion = register.proposition_of(conclusion_id)
        except Exception as absence:  # noqa: BLE001 - يُعاد بنصّه لا بصنفه
            relevance_ok = False
            relevance_reason = f"القضيّةُ المُشارُ إليها غائبةٌ عن السجلّ: {absence}"
        else:
            if conclusion.form is not expected:
                relevance_ok = False
                relevance_reason = (
                    f"صورةُ القضيّة `{conclusion.form.value}` لا تجيب عن سؤالٍ "
                    f"نوعُه `{question.kind.value}`"
                )
    findings.append(
        (VerificationCheck.RELEVANCE_TO_QUESTION, relevance_ok, relevance_reason)
    )

    return VerificationReport(
        question_id=question.question_id, findings=tuple(findings)
    )


@dataclass(frozen=True, slots=True)
class AcceptanceRecord:
    """شهادةُ قبولٍ مربوطةٌ بالسؤال والجواب والمضمون والأدلّة وإصدارات القواعد."""

    question: Question
    answer: Answer
    report: VerificationReport
    store_content_id: str
    register_content_id: str
    discourse_content_id: str
    evidence_content_ids: tuple[str, ...]
    rule_versioned_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.question.question_id != self.answer.question_id:
            raise VerificationError("شهادةٌ تجمع سؤالًا وجوابًا عن غيره")
        if self.report.question_id != self.question.question_id:
            raise VerificationError("تقريرُ تحقّقٍ عن سؤالٍ آخر")
        for value, label in (
            (self.store_content_id, "بصمةُ الرصيد"),
            (self.register_content_id, "بصمةُ السجلّ"),
            (self.discourse_content_id, "بصمةُ المضمون"),
        ):
            _require_text(value, label)

    @property
    def is_accepted(self) -> bool:
        """أقُبِل الجواب؟ لا يُقبَل إلّا بتقريرٍ مرّت مواضعُه الخمسة."""

        return self.report.passed

    def is_stale_against(
        self,
        store: SubstanceStore,
        register: FactRegister,
        content: DiscourseContent,
    ) -> bool:
        """أصارت الشهادةُ قديمةً؟ أيُّ عنصرٍ مؤثِّرٍ تغيّر يجعلها كذلك."""

        return (
            store.content_id != self.store_content_id
            or register.content_id != self.register_content_id
            or content.content_id != self.discourse_content_id
        )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الشهادة للبصمة."""

        return {
            "question": self.question.as_canonical_content(),
            "answer": self.answer.as_canonical_content(),
            "report": self.report.as_canonical_content(),
            "store_content_id": self.store_content_id,
            "register_content_id": self.register_content_id,
            "discourse_content_id": self.discourse_content_id,
            "evidence_content_ids": list(self.evidence_content_ids),
            "rule_versioned_ids": list(self.rule_versioned_ids),
        }

    @property
    def verification_id(self) -> str:
        """بصمةُ الشهادة؛ تُشتَقّ من كلّ ما رُبِطت به ولا تُكتَب."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


def accept(
    question: Question,
    answer: Answer,
    report: VerificationReport,
    store: SubstanceStore,
    register: FactRegister,
    content: DiscourseContent,
) -> AcceptanceRecord:
    """اربط القبولَ بكلّ ما قرأه التحقّق؛ ولا قبولَ بتقريرٍ مُخفِق.

    المدخل: سؤالٌ وجوابٌ وتقريرٌ، والرصيدُ والسجلُّ والمضمون.
    الشرط: التقريرُ مرّت مواضعُه الخمسة.
    المخرج: شهادةٌ مبصومةٌ تُكشَف قِدَمُها عند تغيّر أيّ عنصرٍ مؤثِّر.
    حدُّها: الشهادةُ لا تُثبِت الجوابَ صحيحًا في الواقع؛ تُثبِت أنّه مُستوفٍ
    للمقدّمات التي رُبِط بها.
    """

    if not report.passed:
        raise VerificationError(
            "لا قبولَ بتقريرٍ مُخفِق؛ والمواضعُ المُخفِقة: "
            + "، ".join(check.value for check in report.failed_checks)
        )
    evidence_ids: list[str] = []
    for premise_id in answer.derivation.premise_proposition_ids:
        premise = register.proposition_of(premise_id)
        evidence_ids.append(premise.evidence_ref.content_id)
    return AcceptanceRecord(
        question=question,
        answer=answer,
        report=report,
        store_content_id=store.content_id,
        register_content_id=register.content_id,
        discourse_content_id=content.content_id,
        evidence_content_ids=tuple(sorted(set(evidence_ids))),
        rule_versioned_ids=tuple(answer.derivation.rule_versioned_ids),
    )
