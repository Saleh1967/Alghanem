"""`Σ_L`: أوّليّاتُ النسبة — مرساةُ الطرف، والمحمولُ ذو الرتبة، والمُشغِّل، والقيد.

    Nisbah  =  Predicate_n(t_1,…,t_n | Θ)

**ومرساةُ الطرف أعمُّ من الجنس** (`TermAnchorIsWiderThanGenus`): «زيد» و«هذا»
و«أنا» و«خمسة رجال» أطرافٌ صالحةٌ محفوظةُ الهويّة، وليست أجناسًا بالمعنى
المنطقيّ الضيّق. فالفروعُ الخمسة المُسمّاة **مرشَّحةٌ مُعلَنةٌ لا مولودة**
(`CandidateBranchIsNotABornKind`): تسميتُها هنا تسجيلُ مرشَّحٍ يُختبَر، لا
ولادةُ نمطٍ سبقت تجربتَه.

**والرتبةُ تُرخَّص قبل استعمالها** (`ArityMustBeLicensedBeforeUse`): يجوز أن
تأتي من مواصفةٍ سابقة، أو مصدرٍ معجميّ، أو برهانٍ سابق، أو استدلالٍ مستقلٍّ
مُجمَّدٍ مسبقًا. والممنوعُ واحدٌ بعينه: انتزاعُها من **الحالة المستهدَفة** بعد
رؤيتها ثمّ استعمالُها في إثبات تلك الحالة؛ وهذا عضوٌ مُصرَّحٌ به في المفردة
يُرفَض عند الإنشاء، فلا يمرّ صامتًا تحت اسمٍ عامّ.

**وموضعُ الحجّة أوّليٌّ بلا تسميةٍ دلاليّة** (`ArgumentRolesAreDeferredToTheirOwnLayer`):
لا `Agent` ولا `Patient` ولا `Cause` ولا `Result` في هذه النواة، حفظًا لـ
`NoPatternNameBeforeIndependentBirth`؛ ومن سمّى موضعًا بأحدها سقط عند الإنشاء.

**والمُشغِّلُ بلا نطاقٍ ليس مُشغِّلًا** (`AnOperatorWithoutScopeIsNotScoped`):
النفيُ والشرطُ والاستفهامُ تعمل على موضعٍ مُسمًّى، ومُشغِّلٌ لا يقول على ماذا
يعمل يُقرَأ عامًّا بالسهو فيتغيّر معنى النسبة بلا ترخيص.

تسجيلٌ لا سلطة: لا حكمَ هنا، ولا استيرادَ من `kernel/` ولا من `arabic/`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest

__all__ = [
    "AN_OPERATOR_WITHOUT_SCOPE_IS_NOT_SCOPED",
    "ARGUMENT_ROLES_ARE_DEFERRED_TO_THEIR_OWN_LAYER",
    "ARITY_MUST_BE_LICENSED_BEFORE_USE",
    "CANDIDATE_BRANCH_IS_NOT_A_BORN_KIND",
    "DEFERRED_ARGUMENT_ROLE_NAMES",
    "NISBAH_COMPONENT_NAMES",
    "PREDICATE_COMPONENT_NAMES",
    "TERM_ANCHOR_IS_WIDER_THAN_GENUS",
    "ArgumentSlot",
    "ArityLicenseGenus",
    "ConstraintKind",
    "ConstraintSpecification",
    "NisbahError",
    "NisbahSignature",
    "OperatorSignature",
    "PredicateSignature",
    "TermAnchorKind",
    "TermAnchorSignature",
]


class NisbahError(ValueError):
    """رفضٌ عند الإنشاء في أوّليّات النسبة؛ لا حملَ على أقرب حالة."""


TERM_ANCHOR_IS_WIDER_THAN_GENUS: Final[str] = (
    "مرساةُ الطرف أعمُّ من الجنس: الجنسُ فرعٌ مرشَّحٌ منها، ومن جعل الطرفَ "
    "جنسًا بالمعنى المنطقيّ الضيّق أخرج المتعيَّنَ والإشاريَّ والكمّيَّ من النسبة"
)

CANDIDATE_BRANCH_IS_NOT_A_BORN_KIND: Final[str] = (
    "الفرعُ المرشَّحُ ليس نمطًا مولودًا: تسميةُ الفروع الخمسة تسجيلُ ما يُختبَر، "
    "ولا تُقرَأ ولادةً سبقت تجربتَها"
)

ARITY_MUST_BE_LICENSED_BEFORE_USE: Final[str] = (
    "رتبةُ المحمول تُرخَّص قبل استعمالها: تأتي من مواصفةٍ أو مصدرٍ أو برهانٍ "
    "أو استدلالٍ مستقلٍّ مُجمَّدٍ مسبقًا، ولا تُنتزَع من الحالة المستهدَفة بعد "
    "رؤيتها ثمّ تُستعمَل في إثباتها"
)

ARGUMENT_ROLES_ARE_DEFERRED_TO_THEIR_OWN_LAYER: Final[str] = (
    "الفاعليّةُ والمفعوليّةُ والسببيّةُ والنتيجةُ مؤجَّلةٌ لطبقتها: موضعُ الحجّة "
    "أوّليٌّ بلا تسميةٍ دلاليّة، وإدخالُ الأدوار في النواة تسميةُ نمطٍ قبل ولادته"
)

AN_OPERATOR_WITHOUT_SCOPE_IS_NOT_SCOPED: Final[str] = (
    "مُشغِّلٌ لا يقول على ماذا يعمل يُقرَأ عامًّا بالسهو: النطاقُ مكوّنٌ في "
    "المُشغِّل لا حاشيةٌ تُقدَّر عند القراءة"
)

DEFERRED_ARGUMENT_ROLE_NAMES: Final[tuple[str, ...]] = (
    "agent",
    "patient",
    "cause",
    "result",
    "فاعل",
    "مفعول",
    "سبب",
    "نتيجة",
)
"""الأسماءُ الدلاليّةُ المؤجَّلة؛ مذكورةٌ لتُمنَع لا لتُستعمَل."""


class TermAnchorKind(Enum):
    """فروعُ مرساة الطرف المرشَّحة؛ مُعلَنةٌ لا مولودة، وفيها عضوُ جهلٍ مُصرَّح."""

    GENUS = "genus"
    INDIVIDUAL = "individual"
    REFERENCE = "reference"
    EVENT_ANCHOR = "event_anchor"
    QUANTITY_ANCHOR = "quantity_anchor"
    UNREAD = "unread"


class ArityLicenseGenus(Enum):
    """جنسُ ترخيص الرتبة؛ أربعةٌ مقبولةٌ وواحدٌ مرفوضٌ بالبناء."""

    PRIOR_SPECIFICATION = "prior_specification"
    LEXICAL_SOURCE = "lexical_source"
    PRIOR_PROOF = "prior_proof"
    PREFROZEN_INDEPENDENT_INFERENCE = "prefrozen_independent_inference"
    DERIVED_FROM_THE_TARGET_STATE = "derived_from_the_target_state"

    @property
    def licenses_use(self) -> bool:
        """أيُرخِّص هذا الجنسُ استعمالَ الرتبة؟ الاستثناءُ مُسمًّى لا مُستنتَج."""

        return self is not ArityLicenseGenus.DERIVED_FROM_THE_TARGET_STATE


class ConstraintKind(Enum):
    """مفردةُ القيود `Θ`، مُجمَّدةٌ قبل نصِّ أيّ حالةٍ بعينها."""

    TIME = "time"
    QUANTITY = "quantity"
    DEFINITENESS = "definiteness"
    CONTEXT = "context"
    CONDITION = "condition"
    NEGATION = "negation"
    MODALITY = "modality"


PREDICATE_COMPONENT_NAMES: Final[tuple[str, ...]] = (
    "predicate_id",
    "arity",
    "arity_license",
    "slots",
)
"""مواضعُ المحمول الأربعة؛ مفردةٌ مغلقةٌ مصدرُها هذا الموضعُ وحدَه."""

NISBAH_COMPONENT_NAMES: Final[tuple[str, ...]] = (
    "nisbah_id",
    "predicate",
    "anchors",
    "operators",
    "constraints",
)
"""مواضعُ النسبة الخمسة؛ ومصدرُ أسمائها واحدٌ لا نسخةٌ ثانية."""


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise NisbahError(f"{label} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class TermAnchorSignature:
    """`TermAnchor`: ما يصحّ أن يكون طرفًا محفوظَ الهويّة في نسبة."""

    anchor_id: str
    candidate_kind: TermAnchorKind
    identity_condition: str

    def __post_init__(self) -> None:
        _require_text(self.anchor_id, "مُعرِّفُ المرساة")
        if not isinstance(self.candidate_kind, TermAnchorKind):
            raise NisbahError(
                "فرعُ المرساة عضوٌ في مفردته المغلقة؛ و" + CANDIDATE_BRANCH_IS_NOT_A_BORN_KIND
            )
        _require_text(self.identity_condition, "شرطُ حفظ هويّة الطرف")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المرساة للبصمة."""

        return {
            "anchor_id": self.anchor_id,
            "candidate_kind": self.candidate_kind.value,
            "identity_condition": self.identity_condition,
        }


@dataclass(frozen=True, slots=True)
class ArgumentSlot:
    """موضعُ حجّةٍ داخلَ المحمول: رتبتُه وشرطُ ما يقع فيه، بلا تسميةٍ دلاليّة."""

    slot_id: str
    position: int
    admissibility_condition: str

    def __post_init__(self) -> None:
        _require_text(self.slot_id, "مُعرِّفُ الموضع")
        if type(self.position) is not int or self.position < 1:
            raise NisbahError("رتبةُ الموضع عددٌ صحيحٌ موجبٌ يبدأ من واحد")
        _require_text(self.admissibility_condition, "شرطُ ما يقع في الموضع")
        lowered = self.slot_id.casefold()
        for deferred in DEFERRED_ARGUMENT_ROLE_NAMES:
            if deferred in lowered:
                raise NisbahError(ARGUMENT_ROLES_ARE_DEFERRED_TO_THEIR_OWN_LAYER)

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الموضع للبصمة."""

        return {
            "slot_id": self.slot_id,
            "position": self.position,
            "admissibility_condition": self.admissibility_condition,
        }


@dataclass(frozen=True, slots=True)
class PredicateSignature:
    """`Predicate_n`: محمولٌ ذو رتبةٍ مُرخَّصةٍ ومواضعَ حججٍ مطابقةٍ لها."""

    predicate_id: str
    arity: int
    arity_license: ArityLicenseGenus
    slots: tuple[ArgumentSlot, ...]

    def __post_init__(self) -> None:
        _require_text(self.predicate_id, "مُعرِّفُ المحمول")
        if type(self.arity) is not int or self.arity < 1:
            raise NisbahError("رتبةُ المحمول عددٌ صحيحٌ موجب")
        if not isinstance(self.arity_license, ArityLicenseGenus):
            raise NisbahError("ترخيصُ الرتبة عضوٌ في مفردته المغلقة")
        if not self.arity_license.licenses_use:
            raise NisbahError(ARITY_MUST_BE_LICENSED_BEFORE_USE)
        if not isinstance(self.slots, tuple) or not self.slots:
            raise NisbahError("المحمولُ موضعُ حجّةٍ فأكثر")
        for slot in self.slots:
            if not isinstance(slot, ArgumentSlot):
                raise NisbahError("عضوٌ في مواضع الحجج خارج نوعه")
        if len(self.slots) != self.arity:
            raise NisbahError(
                "عددُ مواضع الحجج هو الرتبةُ نفسُها؛ ورتبةٌ تخالف مواضعَها "
                "رتبةٌ مكتوبةٌ لا مُشتَقّة"
            )
        positions = tuple(slot.position for slot in self.slots)
        if sorted(positions) != list(range(1, self.arity + 1)):
            raise NisbahError("مواضعُ الحجج متتابعةٌ من واحدٍ إلى الرتبة بلا ثغرة")
        slot_ids = tuple(slot.slot_id for slot in self.slots)
        if len(set(slot_ids)) != len(slot_ids):
            raise NisbahError("أسماءُ المواضع بلا تكرار؛ والمكرّرُ يُخفي موضعًا")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المحمول للبصمة."""

        return {
            "predicate_id": self.predicate_id,
            "arity": self.arity,
            "arity_license": self.arity_license.value,
            "slots": [slot.as_canonical_content() for slot in self.slots],
        }


@dataclass(frozen=True, slots=True)
class OperatorSignature:
    """`Operator`: مُشغِّلٌ يعمل على موضعٍ مُسمًّى من النسبة، لا على المجهول."""

    operator_id: str
    scope_target: str

    def __post_init__(self) -> None:
        _require_text(self.operator_id, "مُعرِّفُ المُشغِّل")
        if not isinstance(self.scope_target, str) or not self.scope_target.strip():
            raise NisbahError(AN_OPERATOR_WITHOUT_SCOPE_IS_NOT_SCOPED)

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المُشغِّل للبصمة."""

        return {
            "operator_id": self.operator_id,
            "scope_target": self.scope_target,
        }


@dataclass(frozen=True, slots=True)
class ConstraintSpecification:
    """قيدٌ من `Θ`: جنسُه ومصدرُ ترخيصه، بلا قيمةٍ تُقدَّر عند القراءة."""

    constraint_id: str
    kind: ConstraintKind
    licensed_by: str

    def __post_init__(self) -> None:
        _require_text(self.constraint_id, "مُعرِّفُ القيد")
        if not isinstance(self.kind, ConstraintKind):
            raise NisbahError("جنسُ القيد عضوٌ في مفردته المغلقة لا نصٌّ حرّ")
        _require_text(self.licensed_by, "مصدرُ ترخيص القيد")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى القيد للبصمة."""

        return {
            "constraint_id": self.constraint_id,
            "kind": self.kind.value,
            "licensed_by": self.licensed_by,
        }


@dataclass(frozen=True, slots=True)
class NisbahSignature:
    """`Nisbah`: محمولٌ ومراسي أطرافه ومُشغِّلاتُه وقيودُه، مبصومةً بمحتواها."""

    nisbah_id: str
    predicate: PredicateSignature
    anchors: tuple[TermAnchorSignature, ...]
    operators: tuple[OperatorSignature, ...] = ()
    constraints: tuple[ConstraintSpecification, ...] = ()

    def __post_init__(self) -> None:
        _require_text(self.nisbah_id, "مُعرِّفُ النسبة")
        if not isinstance(self.predicate, PredicateSignature):
            raise NisbahError("النسبةُ محمولٌ واحدٌ بنوعه لا نصٌّ يُسمّيه")
        if not isinstance(self.anchors, tuple):
            raise NisbahError("مراسي الأطراف مجموعةٌ مُصرَّحٌ بها")
        for anchor in self.anchors:
            if not isinstance(anchor, TermAnchorSignature):
                raise NisbahError("عضوٌ في مراسي الأطراف خارج نوعه")
        for operator in self.operators:
            if not isinstance(operator, OperatorSignature):
                raise NisbahError("عضوٌ في المُشغِّلات خارج نوعه")
        for constraint in self.constraints:
            if not isinstance(constraint, ConstraintSpecification):
                raise NisbahError("عضوٌ في القيود خارج نوعه")
        anchor_ids = tuple(anchor.anchor_id for anchor in self.anchors)
        if len(set(anchor_ids)) != len(anchor_ids):
            raise NisbahError("أسماءُ المراسي بلا تكرار في النسبة الواحدة")
        operator_ids = tuple(operator.operator_id for operator in self.operators)
        if len(set(operator_ids)) != len(operator_ids):
            raise NisbahError("أسماءُ المُشغِّلات بلا تكرار")
        constraint_ids = tuple(
            constraint.constraint_id for constraint in self.constraints
        )
        if len(set(constraint_ids)) != len(constraint_ids):
            raise NisbahError("أسماءُ القيود بلا تكرار")
        if len(self.anchors) > self.predicate.arity:
            raise NisbahError(
                "مراسي الأطراف لا تزيد على رتبة المحمول؛ وزيادتُها طرفٌ بلا موضع"
            )

    @property
    def unfilled_slot_count(self) -> int:
        """كم موضعَ حجّةٍ بقي بلا مرساة؟ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب."""

        return self.predicate.arity - len(self.anchors)

    @property
    def are_arguments_closed(self) -> bool:
        """أامتلأت مواضعُ الحجج؟ وهذا **مكوّنٌ واحدٌ** من الإغلاق لا الإغلاقُ كلُّه."""

        return self.unfilled_slot_count == 0

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى النسبة للبصمة."""

        return {
            "nisbah_id": self.nisbah_id,
            "predicate": self.predicate.as_canonical_content(),
            "anchors": [anchor.as_canonical_content() for anchor in self.anchors],
            "operators": [
                operator.as_canonical_content() for operator in self.operators
            ],
            "constraints": [
                constraint.as_canonical_content() for constraint in self.constraints
            ],
        }

    @property
    def content_id(self) -> str:
        """بصمةُ النسبة؛ ونسبتان بمحتوًى واحدٍ نسبةٌ واحدةٌ لا اثنتان."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))
