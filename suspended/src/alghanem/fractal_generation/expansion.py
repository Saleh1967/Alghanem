"""التوسّع: اقتراحٌ يُعرَض ويُقاس على عقد نمطه، ولا يحمل أثرَ حركةٍ لم تقع.

    ExpansionCandidate  =  proposal
    Candidate  ≠  Transition

**والمرشَّحُ اقتراحٌ لا حركة** (`CandidateIsNotTransition`): لا حقلَ فيه لأثرٍ
ولا لهويّةٍ «بعد»، لأنّ ما بعدُ لا يوجد قبل أن يقع انتقال.

**ومجموعةُ التوسّع بلا ترجيح** (`NoForcedChoiceAmongCoAdmissibleBranches`): لا
فائزَ فيها ولا أولويّةَ ولا درجة؛ وترتيبُ العرض عرضٌ لا حكم.

**والمطابقةُ ليست ترخيصًا** (`DeclaredDifference ≠ LicensedDifference`):
`PatternConformantDifference` تُثبِت أنّ الفرقَ المُصرَّحَ وافق عقدَ نمطه، ولا
تُثبِت أنّ النمطَ نفسَه مرخَّصٌ ولا أنّ الفرقَ مأذونٌ فيه من مصدرٍ أعلى؛
ولا تُنشَأ إلّا ببوّابتها برمزِ إصدارٍ داخليّ.

تسجيلٌ لا سلطة: لا ولادةَ، ولا حكمَ ولادةٍ، ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from .laws import (
    CANDIDATE_IS_NOT_TRANSITION,
    DECLARED_DIFFERENCE_IS_NOT_LICENSED_DIFFERENCE,
    NO_FORCED_CHOICE_AMONG_CO_ADMISSIBLE_BRANCHES,
    PATTERN_DECLARATION_IS_NOT_PATTERN_PROOF,
)
from .node import FractalNode, FractalNodeRef, FractalResidual
from .pattern import PatternContract, PatternRef
from .scale import ScaleSpace

__all__ = [
    "CONFORMANCE_IS_NOT_LICENSING",
    "DeclaredDifference",
    "ExpansionCandidate",
    "ExpansionError",
    "ExpansionSet",
    "PatternConformanceDecision",
    "PatternConformanceGate",
    "PatternConformanceStatus",
    "PatternConformantDifference",
    "ProposalProvenance",
]


CONFORMANCE_IS_NOT_LICENSING: Final[str] = (
    "المطابقةُ ليست ترخيصًا: بوّابةُ النمط تُثبِت أنّ الفرقَ المُصرَّحَ وافق عقدَ "
    "نمطه، ولا تُثبِت أنّ النمطَ مُبرهَنٌ ولا أنّ الفرقَ مأذونٌ فيه من مصدرٍ أعلى"
)


class ExpansionError(ValueError):
    """رفضٌ عند تكوين اقتراحٍ أو مجموعةِ توسّعٍ أو قرارِ مطابقة."""


class _IssuanceToken:
    """رمزُ إصدارٍ داخليّ؛ وجودُه بيد البوّابة وحدَها لا بيد المستدعي."""

    __slots__ = ()


_CONFORMANCE_ISSUANCE: Final[_IssuanceToken] = _IssuanceToken()


def _named_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ExpansionError(f"{label} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class DeclaredDifference:
    """فرقٌ مُصرَّحٌ به: بُعدُه، ووصفُه، والثوابتُ التي يدّعي حفظَها."""

    difference_id: str
    dimension: str
    description: str
    preserved_invariants: tuple[str, ...]

    def __post_init__(self) -> None:
        _named_text(self.difference_id, "مُعرِّفُ الفرق")
        _named_text(self.dimension, "بُعدُ الفرق")
        _named_text(self.description, "وصفُ الفرق")
        if not isinstance(self.preserved_invariants, tuple):
            raise ExpansionError("ثوابتُ الفرق مجموعةٌ مُصرَّحٌ بها")
        for invariant in self.preserved_invariants:
            _named_text(invariant, "عضوٌ في ثوابت الفرق")
        if len(set(self.preserved_invariants)) != len(self.preserved_invariants):
            raise ExpansionError("ثابتٌ مُكرَّرٌ في ثوابت الفرق")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الفرق للبصمة."""

        return {
            "difference_id": self.difference_id,
            "dimension": self.dimension,
            "description": self.description,
            "preserved_invariants": list(self.preserved_invariants),
        }


@dataclass(frozen=True, slots=True)
class ProposalProvenance:
    """منشأُ الاقتراح: من اقترحه، وعلى أيِّ أساس، وبأيِّ سببٍ مُسمًّى."""

    proposer_id: str
    basis: str
    reason: str

    def __post_init__(self) -> None:
        _named_text(self.proposer_id, "مُعرِّفُ المقترِح")
        _named_text(self.basis, "أساسُ الاقتراح")
        _named_text(self.reason, "سببُ الاقتراح")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المنشأ للبصمة."""

        return {
            "proposer_id": self.proposer_id,
            "basis": self.basis,
            "reason": self.reason,
        }


@dataclass(frozen=True, slots=True)
class ExpansionCandidate:
    """اقتراحُ توسّعٍ من عقدةٍ بنمطٍ وفرقٍ مُصرَّح؛ ولا أثرَ حركةٍ فيه."""

    candidate_id: str
    source: FractalNodeRef
    pattern_ref: PatternRef
    declared_difference: DeclaredDifference
    proposal_provenance: ProposalProvenance

    def __post_init__(self) -> None:
        _named_text(self.candidate_id, "مُعرِّفُ المرشَّح")
        if not isinstance(self.source, FractalNodeRef):
            raise ExpansionError("مصدرُ المرشَّح مرجعُ عقدةٍ من نوعه")
        if not isinstance(self.pattern_ref, PatternRef):
            raise ExpansionError("نمطُ المرشَّح مرجعٌ من نوعه")
        if not isinstance(self.declared_difference, DeclaredDifference):
            raise ExpansionError("فرقُ المرشَّح مُصرَّحٌ من نوعه")
        if not isinstance(self.proposal_provenance, ProposalProvenance):
            raise ExpansionError(
                "منشأُ الاقتراح مُسمًّى من نوعه؛ و" + CANDIDATE_IS_NOT_TRANSITION
            )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المرشَّح للبصمة."""

        return {
            "candidate_id": self.candidate_id,
            "source": {
                "node_id": self.source.node_id,
                "content_id": self.source.content_id,
            },
            "pattern_ref": {
                "pattern_id": self.pattern_ref.pattern_id,
                "contract_content_id": self.pattern_ref.contract_content_id,
            },
            "declared_difference": self.declared_difference.as_canonical_content(),
            "proposal_provenance": self.proposal_provenance.as_canonical_content(),
        }

    @property
    def content_id(self) -> str:
        """بصمةُ المرشَّح؛ مُشتَقّةٌ لا مكتوبة."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


@dataclass(frozen=True, slots=True)
class ExpansionSet:
    """مجموعةُ اقتراحاتٍ من عقدةٍ واحدة؛ بلا فائزٍ ولا أولويّةٍ ولا درجة."""

    source: FractalNodeRef
    candidates: tuple[ExpansionCandidate, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.source, FractalNodeRef):
            raise ExpansionError("مصدرُ مجموعة التوسّع مرجعُ عقدةٍ من نوعه")
        if not isinstance(self.candidates, tuple) or not self.candidates:
            raise ExpansionError("مجموعةُ التوسّع اقتراحٌ واحدٌ فأكثر")
        seen: set[str] = set()
        for candidate in self.candidates:
            if not isinstance(candidate, ExpansionCandidate):
                raise ExpansionError("عضوٌ في مجموعة التوسّع خارج نوعه")
            if candidate.source != self.source:
                raise ExpansionError("اقتراحٌ يُنسَب إلى غير عقدة المجموعة")
            if candidate.candidate_id in seen:
                raise ExpansionError("مُعرِّفُ اقتراحٍ مُكرَّرٌ في مجموعةٍ واحدة")
            seen.add(candidate.candidate_id)

    @property
    def candidate_ids(self) -> frozenset[str]:
        """مُعرِّفاتُ الاقتراحات مجموعةً بلا ترتيبٍ ولا ترجيح."""

        return frozenset(candidate.candidate_id for candidate in self.candidates)

    def candidate_for(self, candidate_id: str) -> ExpansionCandidate:
        """اقتراحٌ باسمه، أو رفضٌ إن لم يكن في المجموعة."""

        for candidate in self.candidates:
            if candidate.candidate_id == candidate_id:
                return candidate
        raise ExpansionError(
            "لا اقتراحَ بهذا المُعرِّف في هذه المجموعة؛ و"
            + NO_FORCED_CHOICE_AMONG_CO_ADMISSIBLE_BRANCHES
        )


@dataclass(frozen=True, slots=True)
class PatternConformantDifference:
    """فرقٌ ثبتت مطابقتُه لعقد نمطه؛ مطابقةً لا ترخيصًا، ولا تُنشَأ إلّا ببوّابة."""

    candidate: ExpansionCandidate
    pattern_ref: PatternRef
    checked_invariants: tuple[str, ...]
    issuance: _IssuanceToken

    def __post_init__(self) -> None:
        if self.issuance is not _CONFORMANCE_ISSUANCE:
            raise ExpansionError(
                "رتبةُ المطابقة ناتجُ بوّابةٍ لا حقلٌ يكتبه المستدعي؛ و"
                + CONFORMANCE_IS_NOT_LICENSING
            )
        if not isinstance(self.candidate, ExpansionCandidate):
            raise ExpansionError("المطابقةُ فوق اقتراحٍ من نوعه")
        if self.candidate.pattern_ref != self.pattern_ref:
            raise ExpansionError("المطابقةُ تُنسَب إلى نمط الاقتراح بعينه")


class PatternConformanceStatus(Enum):
    """حالُ قياس الاقتراح على عقد نمطه؛ مفردةٌ مغلقة."""

    CONFORMANT = "conformant"
    NONCONFORMANT = "nonconformant"


@dataclass(frozen=True, slots=True)
class PatternConformanceDecision:
    """قرارُ بوّابة المطابقة: حالُه، وسببُه، ورتبتُه إن صدرت، وبقاياه."""

    status: PatternConformanceStatus
    reason: str
    conformant: PatternConformantDifference | None
    residuals: tuple[FractalResidual, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.status, PatternConformanceStatus):
            raise ExpansionError("حالُ القرار عضوٌ في مفردته المغلقة")
        _named_text(self.reason, "سببُ القرار")
        if not isinstance(self.residuals, tuple):
            raise ExpansionError("بقايا القرار مجموعةٌ مُصرَّحٌ بها")
        for residual in self.residuals:
            if not isinstance(residual, FractalResidual):
                raise ExpansionError("عضوٌ في بقايا القرار خارج نوعه")
        if self.status is PatternConformanceStatus.CONFORMANT:
            if not isinstance(self.conformant, PatternConformantDifference):
                raise ExpansionError("قرارُ المطابقة يحمل رتبتَه الصادرة")
        elif self.conformant is not None:
            raise ExpansionError("قرارُ عدم المطابقة لا يحمل رتبةً صادرة")


class PatternConformanceGate:
    """البوّابةُ الوحيدةُ التي تُصدِر `PatternConformantDifference`؛ مطابقةً لا ترخيصًا."""

    @staticmethod
    def assess(
        *,
        candidate: ExpansionCandidate,
        pattern: PatternContract,
        node: FractalNode,
        space: ScaleSpace,
    ) -> PatternConformanceDecision:
        """قِس الاقتراحَ على عقد نمطه عند مقياسٍ مُحَلّ؛ ولا تُصدِر رتبةً إلّا عن قياس."""

        if not isinstance(candidate, ExpansionCandidate):
            raise ExpansionError("المقيسُ اقتراحٌ من نوعه")
        if not isinstance(pattern, PatternContract):
            raise ExpansionError("المقيسُ عليه عقدُ نمطٍ من نوعه")
        if not isinstance(node, FractalNode):
            raise ExpansionError("العقدةُ المصدرُ من نوعها")
        if not isinstance(space, ScaleSpace):
            raise ExpansionError("فضاءُ المقاييس من نوعه")
        if candidate.pattern_ref != pattern.as_ref():
            return PatternConformanceDecision(
                status=PatternConformanceStatus.NONCONFORMANT,
                reason="الاقتراحُ يُشير إلى نمطٍ ببصمةٍ غير بصمة هذا العقد",
                conformant=None,
                residuals=(),
            )
        if candidate.source != node.as_ref():
            return PatternConformanceDecision(
                status=PatternConformanceStatus.NONCONFORMANT,
                reason="الاقتراحُ يُنسَب إلى عقدةٍ غير هذه العقدة ببصمتها",
                conformant=None,
                residuals=(),
            )
        scale_ref = node.identity.scale_ref
        if not space.admits(scale_ref) or not pattern.applies_at(scale_ref):
            return PatternConformanceDecision(
                status=PatternConformanceStatus.NONCONFORMANT,
                reason="النمطُ لا يجري عند مقياس هذه العقدة بمرجعه المُحَلّ",
                conformant=None,
                residuals=(),
            )
        difference = candidate.declared_difference
        if difference.dimension in pattern.blockers:
            return PatternConformanceDecision(
                status=PatternConformanceStatus.NONCONFORMANT,
                reason="بُعدُ الفرق مانعٌ مُسمًّى في عقد النمط",
                conformant=None,
                residuals=(),
            )
        missing = tuple(
            invariant
            for invariant in pattern.preserved_invariants
            if invariant not in difference.preserved_invariants
        )
        if missing:
            return PatternConformanceDecision(
                status=PatternConformanceStatus.NONCONFORMANT,
                reason=(
                    "الفرقُ المُصرَّحُ لا يُغطّي ثوابتَ النمط كلَّها؛ و"
                    + DECLARED_DIFFERENCE_IS_NOT_LICENSED_DIFFERENCE
                ),
                conformant=None,
                residuals=(),
            )
        return PatternConformanceDecision(
            status=PatternConformanceStatus.CONFORMANT,
            reason=(
                "الفرقُ المُصرَّحُ وافق عقدَ نمطه عند مقياسٍ مُحَلّ؛ و"
                + PATTERN_DECLARATION_IS_NOT_PATTERN_PROOF
            ),
            conformant=PatternConformantDifference(
                candidate=candidate,
                pattern_ref=candidate.pattern_ref,
                checked_invariants=pattern.preserved_invariants,
                issuance=_CONFORMANCE_ISSUANCE,
            ),
            residuals=(),
        )
