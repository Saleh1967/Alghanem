"""الفصلُ الأفقيُّ بين الفروع: ثلاثةُ أحكامٍ لا رابعَ لها، وسجلٌّ لا يُمحى.

    BranchStanding  =  ADMITTED | BLOCKED | DEFERRED

**والبقيّةُ ليست حكمًا** (`Residual ≠ Disposition`): لا حالةَ اسمُها
`RESIDUAL`؛ البقايا حقلٌ مستقلٌّ داخل القرار، ويُسمّى في كلِّ حكمٍ ما لم يُحسَم.

**ولا ترجيحَ بين المقبولين** (`NoForcedChoiceAmongCoAdmissibleBranches`): إن
قُبِل فرعان بقيا مقبولَين معًا، فلا فائزَ ولا رتبةَ ولا درجة.

**والحركتان المرشَّحتان اثنتان لا غير**:

    IdentityPreservingTransformation :  identity_before == identity_after
    BranchBirth                      :  parent_identity != child_identity

وحفظُ الهويّة حفظُ **عينِ النسخة** لا وحدةُ جنس الهويّة.

**والدفعُ الخارجيُّ توثيقٌ دستوريٌّ لا تنفيذ**: `X ↪ X ⊔_K Y` يُقرأ هنا شرحًا
لواجهةٍ مشتركةٍ مُصرَّحٍ بها (`shared_interface`)، ولا تدّعي هذه الطبقةُ حسابَ
دفعٍ ولا برهانَه.

تسجيلٌ لا سلطة: لا ولادةَ، ولا حكمَ ولادةٍ، ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from .expansion import (
    DeclaredDifference,
    ExpansionSet,
    PatternConformantDifference,
)
from .laws import (
    NO_FORCED_CHOICE_AMONG_CO_ADMISSIBLE_BRANCHES,
    NO_RESIDUAL_ERASURE,
    RESIDUAL_IS_NOT_DISPOSITION,
)
from .node import (
    INSTANCE_IDENTITY_IS_NOT_IDENTITY_TYPE,
    FractalContent,
    FractalIdentity,
    FractalNodeRef,
    FractalResidual,
)

__all__ = [
    "A_PUSHOUT_IS_DOCUMENTED_NOT_COMPUTED",
    "BranchAdjudicationDecision",
    "BranchAdjudicationGate",
    "BranchAssessment",
    "BranchBirthCandidate",
    "BranchError",
    "BranchRelation",
    "BranchStanding",
    "IdentityPreservingTransformationCandidate",
    "MovementCandidate",
]


A_PUSHOUT_IS_DOCUMENTED_NOT_COMPUTED: Final[str] = (
    "الدفعُ موثَّقٌ لا محسوب: `X ↪ X ⊔_K Y` شرحٌ دستوريٌّ لواجهةٍ مشتركةٍ "
    "مُصرَّحٍ بها، ولا تدّعي هذه الطبقةُ حسابَ دفعٍ ولا برهانَه"
)


class BranchError(ValueError):
    """رفضٌ عند تكوين مرشَّحِ حركةٍ أو حكمِ فرعٍ أو قرارِ فصل."""


class _IssuanceToken:
    """رمزُ إصدارٍ داخليّ؛ وجودُه بيد البوّابة وحدَها لا بيد المستدعي."""

    __slots__ = ()


_ADJUDICATION_ISSUANCE: Final[_IssuanceToken] = _IssuanceToken()


def _named_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise BranchError(f"{label} نصٌّ غير فارغ")
    return value


def _checked_residuals(residuals: object) -> tuple[FractalResidual, ...]:
    if not isinstance(residuals, tuple):
        raise BranchError("البقايا مجموعةٌ مُصرَّحٌ بها")
    for residual in residuals:
        if not isinstance(residual, FractalResidual):
            raise BranchError("عضوٌ في البقايا خارج نوعه")
    return residuals


def _checked_content(content: object) -> FractalContent:
    if not isinstance(content, tuple) or not content:
        raise BranchError("محتوى مخرج الحركة أزواجٌ مُصرَّحٌ بها غيرُ فارغة")
    for entry in content:
        if not isinstance(entry, tuple) or len(entry) != 2:
            raise BranchError("كلُّ مدخلةِ محتوًى زوجُ اسمٍ وقيمة")
        _named_text(entry[0], "اسمُ مدخلة المحتوى")
        _named_text(entry[1], "قيمةُ مدخلة المحتوى")
    return content


class BranchStanding(Enum):
    """أحكامُ الفروع؛ ثلاثةٌ لا رابعَ لها، وليس فيها حالٌ اسمُها بقيّة."""

    ADMITTED = "admitted"
    BLOCKED = "blocked"
    DEFERRED = "deferred"


class BranchRelation(Enum):
    """العلاقةُ الأفقيّةُ بين فرعٍ ووالده؛ أخوّةٌ في مقياسٍ واحدٍ لا علوٌّ عليه."""

    SIBLING_DIFFERENTIATION = "sibling_differentiation"
    SHARED_INTERFACE_EXTENSION = "shared_interface_extension"


@dataclass(frozen=True, slots=True)
class IdentityPreservingTransformationCandidate:
    """مرشَّحُ تحويلٍ حافظٍ للهويّة: الهويّةُ بعدُ عينُ الهويّة قبلُ لا جنسُها."""

    conformant: PatternConformantDifference
    carrier_id: str
    identity_before: FractalIdentity
    identity_after: FractalIdentity
    preserved_invariants: tuple[str, ...]
    output_content: FractalContent

    def __post_init__(self) -> None:
        if not isinstance(self.conformant, PatternConformantDifference):
            raise BranchError("مرشَّحُ الحركة فوق فرقٍ مُطابِقٍ صادرٍ عن بوّابته")
        _named_text(self.carrier_id, "حاملُ الحركة")
        for identity, label in (
            (self.identity_before, "الهويّةُ قبل"),
            (self.identity_after, "الهويّةُ بعد"),
        ):
            if not isinstance(identity, FractalIdentity):
                raise BranchError(f"{label} من نوعها")
        if not self.identity_before.is_same_instance_as(self.identity_after):
            raise BranchError(
                "التحويلُ الحافظُ يحفظ عينَ الهويّة؛ و"
                + INSTANCE_IDENTITY_IS_NOT_IDENTITY_TYPE
            )
        if not isinstance(self.preserved_invariants, tuple):
            raise BranchError("ثوابتُ الحركة مجموعةٌ مُصرَّحٌ بها")
        for invariant in self.preserved_invariants:
            _named_text(invariant, "عضوٌ في ثوابت الحركة")
        _checked_content(self.output_content)

    @property
    def candidate_id(self) -> str:
        """مُعرِّفُ الاقتراح الذي نشأ عنه هذا المرشَّح."""

        return self.conformant.candidate.candidate_id


@dataclass(frozen=True, slots=True)
class BranchBirthCandidate:
    """مرشَّحُ ولادةِ فرع: هويّةُ الابن غيرُ هويّة الوالد، بواجهةٍ مشتركةٍ مُصرَّحة."""

    conformant: PatternConformantDifference
    parent_ref: FractalNodeRef
    parent_identity: FractalIdentity
    child_identity: FractalIdentity
    branch_relation: BranchRelation
    shared_interface: tuple[str, ...]
    declared_difference: DeclaredDifference
    output_content: FractalContent

    def __post_init__(self) -> None:
        if not isinstance(self.conformant, PatternConformantDifference):
            raise BranchError("مرشَّحُ الولادة فوق فرقٍ مُطابِقٍ صادرٍ عن بوّابته")
        if not isinstance(self.parent_ref, FractalNodeRef):
            raise BranchError("الولادةُ تُسمّي مرجعَ والدها")
        for identity, label in (
            (self.parent_identity, "هويّةُ الوالد"),
            (self.child_identity, "هويّةُ الابن"),
        ):
            if not isinstance(identity, FractalIdentity):
                raise BranchError(f"{label} من نوعها")
        if self.parent_identity.is_same_instance_as(self.child_identity):
            raise BranchError(
                "ولادةُ فرعٍ تقتضي هويّةً غيرَ هويّة والدها؛ و"
                + INSTANCE_IDENTITY_IS_NOT_IDENTITY_TYPE
            )
        if not isinstance(self.branch_relation, BranchRelation):
            raise BranchError("علاقةُ الفرع عضوٌ في مفردتها الأفقيّة المغلقة")
        if not isinstance(self.shared_interface, tuple) or not self.shared_interface:
            raise BranchError(
                "الواجهةُ المشتركةُ مُصرَّحٌ بها غيرُ فارغة؛ و"
                + A_PUSHOUT_IS_DOCUMENTED_NOT_COMPUTED
            )
        for component in self.shared_interface:
            _named_text(component, "عضوٌ في الواجهة المشتركة")
        if not isinstance(self.declared_difference, DeclaredDifference):
            raise BranchError("فرقُ الولادة مُصرَّحٌ من نوعه")
        _checked_content(self.output_content)

    @property
    def candidate_id(self) -> str:
        """مُعرِّفُ الاقتراح الذي نشأ عنه هذا المرشَّح."""

        return self.conformant.candidate.candidate_id


MovementCandidate = IdentityPreservingTransformationCandidate | BranchBirthCandidate


@dataclass(frozen=True, slots=True)
class BranchAssessment:
    """حكمُ فرعٍ واحد: رتبتُه، وسببُه، وحركتُه إن قُبِل، وبقاياه مُسمّاة."""

    candidate_id: str
    standing: BranchStanding
    reason: str
    residuals: tuple[FractalResidual, ...]
    movement: MovementCandidate | None = None

    def __post_init__(self) -> None:
        _named_text(self.candidate_id, "مُعرِّفُ الفرع المحكوم فيه")
        if not isinstance(self.standing, BranchStanding):
            raise BranchError(
                "رتبةُ الفرع عضوٌ في مفردتها الثلاثيّة؛ و" + RESIDUAL_IS_NOT_DISPOSITION
            )
        _named_text(self.reason, "سببُ الحكم")
        _checked_residuals(self.residuals)
        if self.standing is BranchStanding.ADMITTED:
            if not isinstance(
                self.movement,
                IdentityPreservingTransformationCandidate | BranchBirthCandidate,
            ):
                raise BranchError("الفرعُ المقبولُ يحمل مرشَّحَ حركته")
            if self.movement.candidate_id != self.candidate_id:
                raise BranchError("مرشَّحُ الحركة يُنسَب إلى فرعٍ غير هذا الفرع")
        else:
            if self.movement is not None:
                raise BranchError("فرعٌ لم يُقبَل لا يحمل مرشَّحَ حركة")
            if not self.residuals:
                raise BranchError(
                    "المنعُ والتأجيلُ يُسمّيان ما لم يُحسَم؛ و" + NO_RESIDUAL_ERASURE
                )


@dataclass(frozen=True, slots=True)
class BranchAdjudicationDecision:
    """قرارُ الفصل الأفقيّ: سجلُّ الفروع كلِّها، مقبولِها وممنوعِها ومؤجَّلِها."""

    source: FractalNodeRef
    gate_id: str
    assessments: tuple[BranchAssessment, ...]
    issuance: _IssuanceToken

    def __post_init__(self) -> None:
        if self.issuance is not _ADJUDICATION_ISSUANCE:
            raise BranchError(
                "قرارُ الفصل ناتجُ بوّابةٍ لا حقلٌ يكتبه المستدعي؛ و"
                + NO_FORCED_CHOICE_AMONG_CO_ADMISSIBLE_BRANCHES
            )
        if not isinstance(self.source, FractalNodeRef):
            raise BranchError("قرارُ الفصل يُنسَب إلى عقدةٍ بمرجعها")
        _named_text(self.gate_id, "مُعرِّفُ بوّابة الفصل")

    def _of(self, standing: BranchStanding) -> tuple[BranchAssessment, ...]:
        return tuple(
            assessment
            for assessment in self.assessments
            if assessment.standing is standing
        )

    @property
    def admitted(self) -> tuple[BranchAssessment, ...]:
        """الفروعُ المقبولة؛ وترتيبُ عرضها ليس ترتيبَ أفضليّة."""

        return self._of(BranchStanding.ADMITTED)

    @property
    def blocked(self) -> tuple[BranchAssessment, ...]:
        """الفروعُ الممنوعة؛ وتبقى في السجلّ بلا محو."""

        return self._of(BranchStanding.BLOCKED)

    @property
    def deferred(self) -> tuple[BranchAssessment, ...]:
        """الفروعُ المؤجَّلة؛ وتبقى في السجلّ بلا محو."""

        return self._of(BranchStanding.DEFERRED)

    @property
    def residuals(self) -> tuple[FractalResidual, ...]:
        """بقايا القرار كلُّها مرصودةً من أحكام فروعه."""

        return tuple(
            residual
            for assessment in self.assessments
            for residual in assessment.residuals
        )

    @property
    def co_admissible_ids(self) -> frozenset[str]:
        """مُعرِّفاتُ المقبولين مجموعةً بلا ترتيب؛ فلا يُقرَأ منها فائز."""

        return frozenset(assessment.candidate_id for assessment in self.admitted)

    def assessment_for(self, candidate_id: str) -> BranchAssessment:
        """حكمُ فرعٍ باسمه، أو رفضٌ إن لم يكن في السجلّ."""

        for assessment in self.assessments:
            if assessment.candidate_id == candidate_id:
                return assessment
        raise BranchError("لا حكمَ بهذا المُعرِّف في هذا السجلّ")


class BranchAdjudicationGate:
    """بوّابةُ الفصل الأفقيّ: تحفظ كلَّ فرعٍ بحكمه، ولا تختار بين مقبولَين."""

    @staticmethod
    def adjudicate(
        *,
        expansion_set: ExpansionSet,
        assessments: tuple[BranchAssessment, ...],
        gate_id: str,
    ) -> BranchAdjudicationDecision:
        """افصِل في كلِّ فروع المجموعة فصلًا تامًّا؛ ولا تُسقِط فرعًا من السجلّ."""

        if not isinstance(expansion_set, ExpansionSet):
            raise BranchError("المفصولُ فيه مجموعةُ توسّعٍ من نوعها")
        if not isinstance(assessments, tuple) or not assessments:
            raise BranchError("الفصلُ حكمٌ واحدٌ فأكثر")
        judged: set[str] = set()
        for assessment in assessments:
            if not isinstance(assessment, BranchAssessment):
                raise BranchError("عضوٌ في أحكام الفصل خارج نوعه")
            if assessment.candidate_id in judged:
                raise BranchError("فرعٌ حُكِم فيه مرّتين في فصلٍ واحد")
            judged.add(assessment.candidate_id)
        if judged != set(expansion_set.candidate_ids):
            raise BranchError(
                "الفصلُ يستوعب فروعَ المجموعة كلَّها لا بعضَها؛ و" + NO_RESIDUAL_ERASURE
            )
        return BranchAdjudicationDecision(
            source=expansion_set.source,
            gate_id=_named_text(gate_id, "مُعرِّفُ بوّابة الفصل"),
            assessments=assessments,
            issuance=_ADJUDICATION_ISSUANCE,
        )
