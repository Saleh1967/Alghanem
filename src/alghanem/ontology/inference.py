"""الاستدلال: خمسُ حالاتِ دعمٍ لا ثلاث، وشاهدا نموذجين لعدم اللزوم.

**«لازم/غير لازم/ممنوع» لا تكفي** (`THREE_OUTCOMES_HIDE_TWO_DIFFERENT_SILENCES`):
عدمُ الحسم بالمقدّمات المتاحة ليس إثباتًا لعدم اللزوم، وخروجُ السؤال عن النطاق
ليس عدمَ حسم. ولذلك المفردةُ خمسٌ:

* `SUPPORTS_PROPOSITION` — المقدّماتُ تدعم القضيّة.
* `SUPPORTS_NEGATION` — تدعم نقيضَها.
* `CONFLICTING_SUPPORT` — تدعمهما معًا، فيُسمَّى التعارضُ ولا يُرجَّح هنا.
* `UNDECIDED_BY_AVAILABLE_PREMISES` — لا حسمَ بالمتاح، وتُسمَّى المقدّمةُ الناقصة.
* `OUT_OF_SCOPE_OR_UNSUPPORTED` — السؤالُ أو العمليّةُ خارج ما نُفِّذ.

**وعدمُ اللزوم يُثبَت بشاهدين لا بسكوت** (`NON_ENTAILMENT_NEEDS_TWO_MODELS`):
`non_entailment_witness` تُخرِج **نموذجين** متوافقين مع المقدّمات المُعلَنة
يختلفان في القضيّة المسؤول عنها؛ ومن لم يُخرِجهما فقد قال «لا يلزم» ولم يُثبِته.
والنموذجُ ههنا إسنادُ قيمٍ للحالات داخل **النموذج المُعلَن** (مجالٌ مغلقٌ من
الأفراد والحالات والقيم)، فالدعوى محدودةٌ به ولا تتجاوزه.

**واستمرارُ الحال قاعدةٌ لها جنسُها وموانعُها** (`PERSISTENCE_IS_DEFEASIBLE`):
لا تُستعمَل حزمةً كافيةً بالسهو؛ تُصرَّح `RuleKind.DEFEASIBLE` بموانعَ مُسمّاة،
ويُفصَل إثباتُ الحال في زمنٍ مشاهَدٍ عن تعميمها إلى فترةٍ لم تُشاهَد.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from .facts import FactRegister, Proposition, PropositionForm
from .substance import SubstanceStore

__all__ = [
    "NON_ENTAILMENT_NEEDS_TWO_MODELS",
    "PERSISTENCE_IS_DEFEASIBLE",
    "THREE_OUTCOMES_HIDE_TWO_DIFFERENT_SILENCES",
    "Derivation",
    "InferenceError",
    "Model",
    "NonEntailmentWitness",
    "SupportStatus",
    "assess_support",
    "non_entailment_witness",
    "refuse_silence_as_negation",
]


class InferenceError(ValueError):
    """رفضٌ بنيويٌّ في طبقة الاستدلال؛ لا حملَ على أقرب حالة."""


THREE_OUTCOMES_HIDE_TWO_DIFFERENT_SILENCES: Final[str] = (
    "ثلاثُ حالاتٍ تُخفي سكوتين مختلفين: «لا أعرف بالمقدّمات المتاحة» غيرُ "
    "«هذا خارج ما نُفِّذ»، وجمعُهما في «غير لازم» يُخرِج نفيًا لم يُثبَت"
)

NON_ENTAILMENT_NEEDS_TWO_MODELS: Final[str] = (
    "عدمُ اللزوم يُثبَت بنموذجين: حالتانِ متوافقتانِ مع المقدّمات داخل النموذج "
    "المُعلَن تختلفان في القضيّة؛ ومن اكتفى بالسكوت لم يُثبِت إلّا عجزَه"
)

PERSISTENCE_IS_DEFEASIBLE: Final[str] = (
    "استمرارُ الحال افتراضٌ قابلٌ للنقض في نموذجٍ محدود، لا قاعدةٌ قطعيّة: "
    "يُصرَّح بجنسه وموانعه، ولا يُضَمّ إلى انحصار الفاعلين حزمةً كافيةً بالسهو"
)


class SupportStatus(Enum):
    """حالُ دعمِ المقدّمات لقضيّةٍ مسؤولٍ عنها؛ خمسٌ متمايزةٌ لا ثلاث."""

    SUPPORTS_PROPOSITION = "supports_proposition"
    SUPPORTS_NEGATION = "supports_negation"
    CONFLICTING_SUPPORT = "conflicting_support"
    UNDECIDED_BY_AVAILABLE_PREMISES = "undecided_by_available_premises"
    OUT_OF_SCOPE_OR_UNSUPPORTED = "out_of_scope_or_unsupported"

    @property
    def is_decided(self) -> bool:
        """أحُسِم الأمرُ في جهةٍ واحدة؟ والتعارضُ ليس حسمًا."""

        return self in (
            SupportStatus.SUPPORTS_PROPOSITION,
            SupportStatus.SUPPORTS_NEGATION,
        )

    @property
    def is_a_silence(self) -> bool:
        """أهذه حالُ سكوت؟ والسكوتانِ مُسمَّيانِ ولا يُقرآنِ نفيًا."""

        return self in (
            SupportStatus.UNDECIDED_BY_AVAILABLE_PREMISES,
            SupportStatus.OUT_OF_SCOPE_OR_UNSUPPORTED,
        )


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InferenceError(f"{label} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class Derivation:
    """أثرُ استدلالٍ واحد: حالُه، ومقدّماتُه، وقواعدُه بإصداراتها، وما نقصه."""

    question_ref: str
    status: SupportStatus
    premise_proposition_ids: tuple[str, ...]
    rule_versioned_ids: tuple[str, ...]
    missing_premise_note: str | None
    conclusion_proposition_id: str | None = None

    def __post_init__(self) -> None:
        _require_text(self.question_ref, "مُعرِّفُ السؤال")
        if not isinstance(self.status, SupportStatus):
            raise InferenceError("حالُ الدعم عضوٌ في مفردتها المغلقة")
        if self.status is SupportStatus.UNDECIDED_BY_AVAILABLE_PREMISES:
            _require_text(
                self.missing_premise_note,
                "المقدّمةُ الناقصةُ تُسمَّى عند عدم الحسم؛ وسكوتٌ بلا تسميةٍ " "يُقرَأ نفيًا",
            )
        if self.status.is_decided and self.conclusion_proposition_id is None:
            raise InferenceError("حكمٌ محسومٌ بلا قضيّةٍ يُشار إليها حكمٌ بلا محلّ")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الأثر للبصمة."""

        return {
            "question_ref": self.question_ref,
            "status": self.status.value,
            "premise_proposition_ids": list(self.premise_proposition_ids),
            "rule_versioned_ids": list(self.rule_versioned_ids),
            "missing_premise_note": self.missing_premise_note,
            "conclusion_proposition_id": self.conclusion_proposition_id,
        }

    @property
    def content_id(self) -> str:
        """بصمةُ الأثر؛ وتغييرُ مقدّمةٍ أو إصدارِ قاعدةٍ يُغيِّرها."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


@dataclass(frozen=True, slots=True)
class Model:
    """نموذجٌ مُعلَن: إسنادُ قيمةٍ لكلّ حالٍ من حالات أفرادِ مجالٍ مغلق.

    والنموذجُ **لا يدّعي الواقع**: هو حالةٌ ممكنةٌ داخل مجالٍ صُرِّح بأفراده
    وحالاته وقيمها؛ فما يُثبَت به محدودٌ بهذا المجال ولا يتجاوزه.
    """

    model_id: str
    state_values: Mapping[tuple[str, str], str]
    occurred_event_keys: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        _require_text(self.model_id, "مُعرِّفُ النموذج")
        for key in self.state_values:
            if not isinstance(key, tuple) or len(key) != 2:
                raise InferenceError("مفتاحُ الحال زوجٌ: فردٌ وحال")

    def state_of(self, individual_id: str, state_id: str) -> str | None:
        """قيمةُ حالٍ لفردٍ في هذا النموذج، أو `None` تصريحًا بأنّها غيرُ مُسنَدة."""

        return self.state_values.get((individual_id, state_id))

    def event_occurred(self, individual_id: str, event_type_id: str) -> bool:
        """أوقع حدثٌ من هذا النوع على هذا الفرد في هذا النموذج؟"""

        return (individual_id, event_type_id) in self.occurred_event_keys

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى النموذج للبصمة."""

        return {
            "model_id": self.model_id,
            "state_values": [
                {"individual_id": key[0], "state_id": key[1], "value": value}
                for key, value in sorted(self.state_values.items())
            ],
            "occurred_event_keys": [
                {"individual_id": key[0], "event_type_id": key[1]}
                for key in sorted(self.occurred_event_keys)
            ],
        }


@dataclass(frozen=True, slots=True)
class NonEntailmentWitness:
    """شاهدُ عدم اللزوم: نموذجانِ متوافقانِ مع المقدّمات يختلفان في القضيّة."""

    question_ref: str
    queried_state_id: str
    queried_individual_id: str
    first: Model
    second: Model
    declared_model_note: str

    def __post_init__(self) -> None:
        _require_text(self.question_ref, "مُعرِّفُ السؤال")
        _require_text(self.queried_state_id, "الحالُ المسؤولُ عنها")
        _require_text(self.queried_individual_id, "الفردُ المسؤولُ عنه")
        _require_text(self.declared_model_note, "بيانُ حدود النموذج المُعلَن")
        for model in (self.first, self.second):
            if not isinstance(model, Model):
                raise InferenceError("الشاهدُ نموذجانِ قائمان")
        if self.first.model_id == self.second.model_id:
            raise InferenceError("النموذجانِ متمايزانِ بمُعرِّفيهما")
        key = (self.queried_individual_id, self.queried_state_id)
        first_value = self.first.state_values.get(key)
        second_value = self.second.state_values.get(key)
        if first_value is None or second_value is None:
            raise InferenceError(
                "شاهدُ عدم اللزوم يُسنِد القيمةَ في النموذجين معًا؛ وسكوتُ أحدهما "
                "ليس اختلافًا"
            )
        if first_value == second_value:
            raise InferenceError(
                NON_ENTAILMENT_NEEDS_TWO_MODELS
                + "؛ والنموذجانِ المُقدَّمانِ متّفقانِ في القضيّة فلا يشهدان"
            )

    @property
    def differing_values(self) -> tuple[str, str]:
        """القيمتانِ المختلفتانِ في النموذجين؛ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب."""

        key = (self.queried_individual_id, self.queried_state_id)
        first = self.first.state_values[key]
        second = self.second.state_values[key]
        return (first, second)

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الشاهد للبصمة."""

        return {
            "question_ref": self.question_ref,
            "queried_state_id": self.queried_state_id,
            "queried_individual_id": self.queried_individual_id,
            "first": self.first.as_canonical_content(),
            "second": self.second.as_canonical_content(),
            "declared_model_note": self.declared_model_note,
        }


def assess_support(
    question_ref: str,
    target: Proposition,
    register: FactRegister,
    store: SubstanceStore,
    missing_premise_note: str | None = None,
) -> Derivation:
    """قِس دعمَ المقدّمات القائمة لقضيّةٍ مسؤولٍ عنها، وسمِّ ما نقص.

    المدخل: قضيّةٌ مصوغة، وسجلٌّ، ورصيد.
    الشرط: صورةُ القضيّة منفَّذةٌ ههنا؛ وغيرُها يخرج `OUT_OF_SCOPE_OR_UNSUPPORTED`.
    المخرج: `Derivation` بحالٍ من خمسٍ، ومقدّماتٍ مُسمّاة.
    حدُّها: لا تُرجِّح عند التعارض، ولا تقرأ السكوتَ نفيًا.
    """

    if target.form not in (
        PropositionForm.STATE_HOLDS,
        PropositionForm.EVENT_OCCURRED,
    ):
        return Derivation(
            question_ref=question_ref,
            status=SupportStatus.OUT_OF_SCOPE_OR_UNSUPPORTED,
            premise_proposition_ids=(),
            rule_versioned_ids=(),
            missing_premise_note=(
                f"صورةُ القضيّة `{target.form.value}` غيرُ منفَّذةٍ في هذه الطبقة"
            ),
        )
    if target.form is PropositionForm.STATE_HOLDS:
        store.state_of(target.predicate_id)
    else:
        store.event_type_of(target.predicate_id)
    supporting: list[str] = []
    opposing: list[str] = []
    for item in register.active_propositions:
        if item.form is not target.form:
            continue
        if item.subject_id != target.subject_id:
            continue
        if item.predicate_id != target.predicate_id:
            continue
        if not item.scope.covers(target.scope):
            continue
        same_value = item.value == target.value
        same_polarity = item.polarity is target.polarity
        if same_value and same_polarity:
            supporting.append(item.proposition_id)
        elif same_polarity != same_value:
            opposing.append(item.proposition_id)
    if supporting and opposing:
        return Derivation(
            question_ref=question_ref,
            status=SupportStatus.CONFLICTING_SUPPORT,
            premise_proposition_ids=tuple(supporting + opposing),
            rule_versioned_ids=(),
            missing_premise_note=None,
            conclusion_proposition_id=None,
        )
    if supporting:
        return Derivation(
            question_ref=question_ref,
            status=SupportStatus.SUPPORTS_PROPOSITION,
            premise_proposition_ids=tuple(supporting),
            rule_versioned_ids=(),
            missing_premise_note=None,
            conclusion_proposition_id=supporting[0],
        )
    if opposing:
        return Derivation(
            question_ref=question_ref,
            status=SupportStatus.SUPPORTS_NEGATION,
            premise_proposition_ids=tuple(opposing),
            rule_versioned_ids=(),
            missing_premise_note=None,
            conclusion_proposition_id=opposing[0],
        )
    return Derivation(
        question_ref=question_ref,
        status=SupportStatus.UNDECIDED_BY_AVAILABLE_PREMISES,
        premise_proposition_ids=(),
        rule_versioned_ids=(),
        missing_premise_note=(
            missing_premise_note or "لا قضيّةَ قائمةٌ تشمل نطاقَ السؤال في هذا الموضع"
        ),
    )


def non_entailment_witness(
    question_ref: str,
    individual_id: str,
    state_id: str,
    values: Sequence[str],
    shared_occurred_event_keys: Sequence[tuple[str, str]],
    declared_model_note: str,
) -> NonEntailmentWitness:
    """ابنِ شاهدَ عدم لزومٍ: نموذجانِ يختلفان في قيمة الحال ويتّفقان فيما عداها.

    المدخل: فردٌ وحالٌ وقيمتانِ من قيمها، وما وقع من أحداثٍ في النموذجين معًا.
    الشرط: القيمتانِ مختلفتان؛ والمتّفقتانِ لا تشهدان.
    المخرج: شاهدٌ مبصومٌ يُقرَأ دليلًا على عدم اللزوم **داخل النموذج المُعلَن**.
    حدُّها: لا يُثبِت الشاهدُ شيئًا خارجَ المجال المُصرَّح به في بيانه.
    """

    if len(values) != 2:
        raise InferenceError(
            NON_ENTAILMENT_NEEDS_TWO_MODELS + "؛ والقيمُ المطلوبةُ قيمتانِ بالضبط"
        )
    first_value, second_value = values
    shared = tuple(shared_occurred_event_keys)
    return NonEntailmentWitness(
        question_ref=question_ref,
        queried_state_id=state_id,
        queried_individual_id=individual_id,
        first=Model(
            model_id=f"{question_ref}::نموذج-١",
            state_values={(individual_id, state_id): first_value},
            occurred_event_keys=shared,
        ),
        second=Model(
            model_id=f"{question_ref}::نموذج-٢",
            state_values={(individual_id, state_id): second_value},
            occurred_event_keys=shared,
        ),
        declared_model_note=declared_model_note,
    )


def refuse_silence_as_negation(status: SupportStatus) -> None:
    """ارفض قراءةَ السكوت نفيًا؛ `THREE_OUTCOMES_HIDE_TWO_DIFFERENT_SILENCES`."""

    if status.is_a_silence:
        raise InferenceError(THREE_OUTCOMES_HIDE_TWO_DIFFERENT_SILENCES)
