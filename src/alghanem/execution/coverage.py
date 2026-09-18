"""`G0.CASE-0.MATRIX`: دستورُ الحالات قبل الحالات؛ ما يجب بلوغُه وما يستحيل.

    CoverageRequirement  →  (case_id = None)  →  G0.CASE-0.DATA  →  READOUT

**والمطلوبُ يُجمَّد قبل اختيار الحالات** (`CoverageRequirementIsFrozenBeforeCaseSelection`):
لو كُتبت الحالاتُ أوّلًا لأثّر اختيارُها رجعيًّا في تعريف ما يجب تغطيتُه، فصار
الجدولُ وصفًا لما فُعِل لا مطلبًا يُحاسَب عليه. فتُجمَّد المصفوفةُ أوّلًا،
و`case_id` فيها `None` بلا استثناء.

**وتوقُّعُ الحالة يُجمَّد قبل أوّل قراءةٍ للمحرّك**
(`CaseExpectationIsFrozenBeforeFirstEngineReadout`): ثمّ تأتي `DATA` فتُجمِّد
المدخلاتِ والتوقّعاتِ من غير تشغيلٍ، ثمّ `READOUT` تُشغِّل المحرّكَ أوّلَ مرّةٍ
فيظهر الاتّفاقُ أو الفشل. فالترتيب:

    Specification  ≺  Cases  ≺  Readout

**والخليةُ غيرُ القابلة للوصول تُعلَّل ولا تُصطنَع**
(`AnUnreachableCellIsJustifiedNotInvented`): منزلةٌ يمنع الدستورُ بلوغَها
تُسجَّل `reachable=False` بتعليلٍ مُسمًّى، ولا تُخترَع لها حالةٌ مصطنعةٌ لملء جدول.

**وإثباتُ البلوغ لا يُغني عن إثبات المنع** (`forbidden_co_standings`): أن يبلغ
قانونٌ `VIOLATED` لا يكفي؛ يجب أن يثبت معه أنّه **على الموضوع نفسه** لا يكون في
الوقت نفسه `SATISFIED` أو `UNRESOLVED`. والمنعُ هنا لموضوعٍ واحدٍ لا للأثر
كلِّه؛ فقانونٌ ذو مواضعَ كثيرةٍ يصحّ أن يثبت في موضعٍ ويُخالَف في آخر.

**ولا تسمّي المصفوفةُ حالةً ولا بصمة** (`AMatrixNamesNoCaseAndNoDigest`): لا
`JSON` ولا `execution_digest` في هذه المرحلة ألبتّة.

**وهذه المصفوفةُ للمحرّك كما جُمِّد** (`AMatrixMeasuresTheEngineAsFrozen`): مدارُها
`PK₀ → O₀ → O_L² → Nisbah`. وأيُّ تأسيسٍ أنطولوجيٍّ أعمقَ لاحقٍ — كإعادة تعريف
`PK₀` شبكةَ عقدٍ ليفيّةٍ — طبقةٌ جديدةٌ فوق العقد الحاليّ، لها مصفوفتُها
وحالاتُها؛ ولا تُغيَّر بها هذه المصفوفةُ رجعيًّا.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from .lawset import LAW_SET, ExecutionLaw
from .outcome import CheckStanding

__all__ = [
    "AN_UNREACHABLE_CELL_IS_JUSTIFIED_NOT_INVENTED",
    "A_MATRIX_MEASURES_THE_ENGINE_AS_FROZEN",
    "A_MATRIX_NAMES_NO_CASE_AND_NO_DIGEST",
    "CASE_EXPECTATION_IS_FROZEN_BEFORE_FIRST_ENGINE_READOUT",
    "COVERAGE_MATRIX",
    "COVERAGE_MATRIX_DIGEST",
    "COVERAGE_MATRIX_ID",
    "COVERAGE_REQUIREMENT_IS_FROZEN_BEFORE_CASE_SELECTION",
    "CoverageAxis",
    "CoverageMatrix",
    "CoverageMatrixError",
    "CoverageRequirement",
    "ExpectedOutcome",
]


COVERAGE_REQUIREMENT_IS_FROZEN_BEFORE_CASE_SELECTION: Final[str] = (
    "مطلبُ التغطية يُجمَّد قبل اختيار الحالات: لو سبقت الحالاتُ لأثّر اختيارُها "
    "رجعيًّا في تعريف المطلوب، فصار الجدولُ وصفًا لما فُعِل لا مِعيارًا يُحاسَب به"
)

CASE_EXPECTATION_IS_FROZEN_BEFORE_FIRST_ENGINE_READOUT: Final[str] = (
    "توقُّعُ الحالة يُجمَّد قبل أوّل قراءةٍ للمحرّك: مواصفةٌ ثمّ حالاتٌ ثمّ قراءة؛ "
    "فالنجاحُ حينئذٍ دليلٌ لا توافقٌ صُنِع بعد رؤية النتيجة"
)

AN_UNREACHABLE_CELL_IS_JUSTIFIED_NOT_INVENTED: Final[str] = (
    "الخليةُ غيرُ القابلة للوصول تُعلَّل ولا تُصطنَع: منزلةٌ يمنع الدستورُ بلوغَها "
    "تُسجَّل ممنوعةً بتعليلها، ولا تُخترَع لها حالةٌ لملء جدول"
)

A_MATRIX_NAMES_NO_CASE_AND_NO_DIGEST: Final[str] = (
    "المصفوفةُ لا تسمّي حالةً ولا بصمةَ تنفيذ: `case_id` فيها معدومٌ بلا استثناء، "
    "وتسميةُ الحالات مرحلةٌ تالية"
)

A_MATRIX_MEASURES_THE_ENGINE_AS_FROZEN: Final[str] = (
    "المصفوفةُ تقيس المحرّكَ كما جُمِّد: مدارُها `PK₀ → O₀ → O_L² → Nisbah`؛ وأيُّ "
    "تأسيسٍ أنطولوجيٍّ أعمقَ لاحقٍ طبقةٌ جديدةٌ لها مصفوفتُها، ولا يُغيّر ما مضى"
)


class CoverageMatrixError(ValueError):
    """رفضٌ عند تكوين مطلبٍ أو مصفوفة؛ لا حملَ على أقرب حالةٍ مقبولة."""


class CoverageAxis(Enum):
    """محاورُ التغطية الثلاثة؛ مستقلّةٌ لا يُغني أحدُها عن الآخر."""

    LAW_STANDING = "law_standing"
    OUTCOME_REACHABILITY = "outcome_reachability"
    CROSS_STAGE_SEPARATION = "cross_stage_separation"


class ExpectedOutcome(Enum):
    """ما يجب أن تُنتِجه الحالةُ الشاهدة؛ وفيه ما ليس حكمًا أصلًا."""

    PASS = "pass"
    BLOCK = "block"
    DEFER = "defer"
    INHERITED = "inherited"
    NO_VERDICT_INVALID_INPUT = "no_verdict_invalid_input"
    NO_VERDICT_INVARIANT_ERROR = "no_verdict_invariant_error"
    NOT_CONSTRAINED = "not_constrained"


_OUTCOME_OF_STANDING: Final[dict[CheckStanding, ExpectedOutcome]] = {
    CheckStanding.SATISFIED: ExpectedOutcome.PASS,
    CheckStanding.VIOLATED: ExpectedOutcome.BLOCK,
    CheckStanding.UNRESOLVED: ExpectedOutcome.DEFER,
    CheckStanding.NOT_EVALUATED_BY_PREREQUISITE: ExpectedOutcome.INHERITED,
    CheckStanding.NOT_APPLICABLE_NO_CLAIM: ExpectedOutcome.PASS,
}
"""الحكمُ المتوقَّعُ من منزلةٍ مطلوبة؛ مُعلَنٌ لا مُستنتَجٌ عند القراءة."""


@dataclass(frozen=True, slots=True)
class CoverageRequirement:
    """خليّةُ تغطيةٍ واحدة: ما يجب أن يثبت، وما يمتنع معه، ولمَ إن امتنع."""

    requirement_id: str
    axis: CoverageAxis
    law: ExecutionLaw | None
    target_standing: CheckStanding | None
    claim: str | None
    required: bool
    reachable: bool
    prerequisite_laws: tuple[ExecutionLaw, ...]
    forbidden_co_standings: tuple[CheckStanding, ...]
    expected_outcome: ExpectedOutcome
    case_id: None
    justification_if_unreachable: str | None

    def __post_init__(self) -> None:
        if not isinstance(self.requirement_id, str) or not self.requirement_id.strip():
            raise CoverageMatrixError("مُعرِّفُ المطلب نصٌّ غير فارغ")
        if not isinstance(self.axis, CoverageAxis):
            raise CoverageMatrixError("محورُ التغطية عضوٌ في مفردته المغلقة")
        if not isinstance(self.expected_outcome, ExpectedOutcome):
            raise CoverageMatrixError("الحكمُ المتوقَّع عضوٌ في مفردته المغلقة")
        if self.case_id is not None:
            raise CoverageMatrixError(A_MATRIX_NAMES_NO_CASE_AND_NO_DIGEST)
        if self.axis is CoverageAxis.LAW_STANDING:
            if not isinstance(self.law, ExecutionLaw) or not isinstance(
                self.target_standing, CheckStanding
            ):
                raise CoverageMatrixError(
                    "خليّةُ المحور الأوّل قانونٌ ومنزلةٌ معًا لا أحدُهما"
                )
            if self.claim is not None:
                raise CoverageMatrixError(
                    "خليّةُ المحور الأوّل يُغني فيها القانونُ ومنزلتُه عن نثرٍ يعيدهما"
                )
        else:
            if self.law is not None or self.target_standing is not None:
                raise CoverageMatrixError(
                    "مطلبُ المحورين الثاني والثالث ليس خليّةَ قانونٍ في منزلة"
                )
            if not isinstance(self.claim, str) or not self.claim.strip():
                raise CoverageMatrixError("مطلبٌ خارج المحور الأوّل يُسمّي دعواه نصًّا")
        for value, label in (
            (self.prerequisite_laws, "القوانينُ السابقة"),
            (self.forbidden_co_standings, "المنازلُ الممنوعةُ معه"),
        ):
            if not isinstance(value, tuple):
                raise CoverageMatrixError(f"{label} مجموعةٌ مرتَّبةٌ مُصرَّحٌ بها")
        if self.law is not None and self.law in self.prerequisite_laws:
            raise CoverageMatrixError("القانونُ لا يكون شرطًا سابقًا لنفسه")
        if (
            self.target_standing is not None
            and self.target_standing in self.forbidden_co_standings
        ):
            raise CoverageMatrixError("المنزلةُ المطلوبةُ لا تُمنَع مع نفسها")
        if self.reachable:
            if self.justification_if_unreachable is not None:
                raise CoverageMatrixError(
                    "التعليلُ لِما امتنع؛ وخليّةٌ قابلةٌ للوصول لا تُعلَّل بامتناع"
                )
            if self.expected_outcome is ExpectedOutcome.NOT_CONSTRAINED:
                raise CoverageMatrixError(
                    "خليّةٌ مطلوبةٌ بلا حكمٍ متوقَّعٍ مطلبٌ لا يُحاسَب عليه"
                )
        else:
            if self.required:
                raise CoverageMatrixError(AN_UNREACHABLE_CELL_IS_JUSTIFIED_NOT_INVENTED)
            if (
                not isinstance(self.justification_if_unreachable, str)
                or not self.justification_if_unreachable.strip()
            ):
                raise CoverageMatrixError(AN_UNREACHABLE_CELL_IS_JUSTIFIED_NOT_INVENTED)
            if self.expected_outcome is not ExpectedOutcome.NOT_CONSTRAINED:
                raise CoverageMatrixError("ما لا يُبلَغ لا يُتوقَّع منه حكم؛ فحكمُه غيرُ مُقيَّد")
            if self.prerequisite_laws or self.forbidden_co_standings:
                raise CoverageMatrixError(
                    "ما لا يُبلَغ لا شرطَ سابقٌ له ولا منزلةَ تُمنَع معه"
                )
        if (
            self.target_standing is CheckStanding.NOT_EVALUATED_BY_PREREQUISITE
            and self.reachable
            and not self.prerequisite_laws
        ):
            raise CoverageMatrixError(
                "المحجوبُ يُسمّي القوانينَ التي قد تحجبه؛ وحجبٌ بلا حاجبٍ غيرُ مقروء"
            )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المطلب لبصمة المصفوفة."""

        return {
            "requirement_id": self.requirement_id,
            "axis": self.axis.value,
            "law": None if self.law is None else self.law.value,
            "target_standing": (
                None if self.target_standing is None else self.target_standing.value
            ),
            "claim": self.claim,
            "required": self.required,
            "reachable": self.reachable,
            "prerequisite_laws": [law.value for law in self.prerequisite_laws],
            "forbidden_co_standings": [
                standing.value for standing in self.forbidden_co_standings
            ],
            "expected_outcome": self.expected_outcome.value,
            "case_id": None,
            "justification_if_unreachable": self.justification_if_unreachable,
        }


@dataclass(frozen=True, slots=True)
class CoverageMatrix:
    """المصفوفةُ المجمَّدةُ مرتَّبة؛ وهويّتُها بصمتُها لا عددُ خلاياها."""

    matrix_id: str
    requirements: tuple[CoverageRequirement, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.matrix_id, str) or not self.matrix_id.strip():
            raise CoverageMatrixError("اسمُ المصفوفة نصٌّ غير فارغ")
        if not isinstance(self.requirements, tuple) or not self.requirements:
            raise CoverageMatrixError("مصفوفةٌ بلا مطلبٍ واحدٍ ليست مِعيارًا")
        seen: set[str] = set()
        for requirement in self.requirements:
            if not isinstance(requirement, CoverageRequirement):
                raise CoverageMatrixError("عضوٌ في المصفوفة خارج نوعه")
            if requirement.requirement_id in seen:
                raise CoverageMatrixError(
                    f"مُعرِّفُ المطلب «{requirement.requirement_id}» مكرَّر؛ "
                    "والمُعرَّفُ المكرَّرُ يُخفي مطلبًا"
                )
            seen.add(requirement.requirement_id)

    def of_axis(self, axis: CoverageAxis) -> tuple[CoverageRequirement, ...]:
        """مطالبُ محورٍ واحدٍ على ترتيبها المجمَّد."""

        return tuple(item for item in self.requirements if item.axis is axis)

    def cell(
        self, law: ExecutionLaw, standing: CheckStanding
    ) -> CoverageRequirement | None:
        """خليّةُ قانونٍ في منزلة؛ والغيابُ `None` يُقرَأ غيابًا لا رخصة."""

        for item in self.requirements:
            if item.law is law and item.target_standing is standing:
                return item
        return None

    @property
    def required_cases(self) -> tuple[CoverageRequirement, ...]:
        """المطالبُ التي يجب أن تُقابِلها حالةٌ في `G0.CASE-0.DATA`."""

        return tuple(item for item in self.requirements if item.required)

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المصفوفة للبصمة؛ ورتبةُ المطالب فيه محتوًى لا عرض."""

        return {
            "matrix_id": self.matrix_id,
            "requirements": [item.as_canonical_content() for item in self.requirements],
        }


_NO_OPTIONAL_CLAIM: Final[str] = (
    "هذا القانونُ لا يقارن دعوى هويّةٍ اختياريّةً، فليس فيه موضعٌ لـ«لا دعوى»؛ "
    "ومادّتُه مُصرَّحٌ بها دائمًا أو غائبةٌ غيابَ نقصِ دليل"
)

_NOT_GATED_BY_A_PRIOR_LAW: Final[str] = (
    "مادّةُ هذا القانون تُقرَأ من التصريح ومن القاعدة السابقة مباشرةً، ولا يقف "
    "بينه وبينها فعلُ ترخيصٍ سابقٌ يحجبها؛ فغيابُها نقصُ دليلٍ لا حجب"
)

_SHAPE_IS_READ_FROM_THE_DECLARATION_ALONE: Final[str] = (
    "شكلُ المحمول يُقرَأ من التصريح وحدَه بلا مادّةٍ مُشتَقّة، وقيامُ الإدخال يمنع "
    "غيابَ حقوله؛ فلا نقصَ دليلٍ فيه ولا قانونَ سابقٌ يحجبه"
)

_AN_UNREAD_CONDITION_IS_NOT_A_PROVED_BREACH: Final[str] = (
    "الشرطُ غيرُ المقروء نقصُ دليلٍ لا مخالفةٌ ثابتة: ليس في الجنس المُصرَّح به قيمةٌ "
    "تجعل القراءةَ واقعةً وغيرَ واقعةٍ معًا، فيمتنع أن يثبت خرقُ هذا القانون"
)

_A_NISBAH_IDENTITY_IS_NOT_MISSING_EVIDENCE: Final[str] = (
    "هويّةُ النسبة ليست دليلًا ناقصًا في ذاتها: إمّا تُنشَأ النسبةُ فتُقارَن هويّتُها، "
    "أو يمنع قانونٌ سابقٌ إنشاءَها فيُسجَّل الحجبُ باسم حاجبه؛ ولا منزلةَ ثالثة"
)

_LINGUISTIC_BLOCKERS: Final[tuple[ExecutionLaw, ...]] = (
    ExecutionLaw.LINGUISTIC_LICENSES_SHARE_THE_FOUNDING_BASE,
    ExecutionLaw.LINGUISTIC_ONTOLOGY_FOUNDED_ON_THE_LINEAGE_GENERAL,
)
"""حاجبا الأنطولوجيا اللغويّة: اختلافُ قاعدة الرخصة، وردُّ التأسيس نفسِه."""

_ALL_PRIOR_LAWS: Final[tuple[ExecutionLaw, ...]] = tuple(
    law for law in LAW_SET if law is not ExecutionLaw.MATERIALIZED_IDENTITY_AGREES
)
"""القوانينُ السبعةَ عشرَ التي قد يحجب أوّلُ غيرِ ناجحٍ منها قانونَ التشييد."""


_REACHABLE: Final[dict[ExecutionLaw, dict[CheckStanding, tuple[ExecutionLaw, ...]]]] = {
    ExecutionLaw.NO_SELF_DERIVED_LICENSING_GENUS: {
        CheckStanding.SATISFIED: (),
        CheckStanding.VIOLATED: (),
        CheckStanding.UNRESOLVED: (),
    },
    ExecutionLaw.NO_UNREAD_CONDITION_IN_THE_FOUNDING_BASE: {
        CheckStanding.SATISFIED: (),
        CheckStanding.UNRESOLVED: (),
    },
    ExecutionLaw.GENERAL_ONTOLOGY_FOUNDED_ON_THE_LINEAGE_BASE: {
        CheckStanding.SATISFIED: (),
        CheckStanding.VIOLATED: (),
        CheckStanding.UNRESOLVED: (),
    },
    ExecutionLaw.LINGUISTIC_LICENSES_NAME_REGISTERED_CANDIDATES: {
        CheckStanding.SATISFIED: (),
        CheckStanding.VIOLATED: (),
        CheckStanding.UNRESOLVED: (),
    },
    ExecutionLaw.LINGUISTIC_LICENSES_SHARE_THE_FOUNDING_BASE: {
        CheckStanding.SATISFIED: (),
        CheckStanding.VIOLATED: (),
        CheckStanding.UNRESOLVED: (),
    },
    ExecutionLaw.LINGUISTIC_ONTOLOGY_FOUNDED_ON_THE_LINEAGE_GENERAL: {
        CheckStanding.SATISFIED: (),
        CheckStanding.VIOLATED: (),
        CheckStanding.UNRESOLVED: (),
        CheckStanding.NOT_EVALUATED_BY_PREREQUISITE: (
            ExecutionLaw.LINGUISTIC_LICENSES_SHARE_THE_FOUNDING_BASE,
        ),
    },
    ExecutionLaw.EXISTENCE_LINEAGE_REDERIVES: {
        CheckStanding.SATISFIED: (),
        CheckStanding.VIOLATED: (),
        CheckStanding.UNRESOLVED: (),
        CheckStanding.NOT_EVALUATED_BY_PREREQUISITE: _LINGUISTIC_BLOCKERS,
    },
    ExecutionLaw.CONDITION_SITES_SHARE_THE_LINEAGE_BASE: {
        CheckStanding.SATISFIED: (),
        CheckStanding.VIOLATED: (),
        CheckStanding.UNRESOLVED: (),
    },
    ExecutionLaw.CONDITION_SITES_ARE_LICENSED_FOR_USE: {
        CheckStanding.SATISFIED: (),
        CheckStanding.VIOLATED: (),
        CheckStanding.UNRESOLVED: (),
    },
    ExecutionLaw.ROLE_SITES_SHARE_THE_LINEAGE_ONTOLOGY: {
        CheckStanding.SATISFIED: (),
        CheckStanding.VIOLATED: (),
        CheckStanding.UNRESOLVED: (),
    },
    ExecutionLaw.ROLE_LICENSE_GRANTED_FOR_THE_FUNCTION_READ: {
        CheckStanding.SATISFIED: (),
        CheckStanding.VIOLATED: (),
        CheckStanding.UNRESOLVED: (),
        CheckStanding.NOT_EVALUATED_BY_PREREQUISITE: _LINGUISTIC_BLOCKERS,
    },
    ExecutionLaw.ROLE_LICENSE_IS_OPERATIVE: {
        CheckStanding.SATISFIED: (),
        CheckStanding.VIOLATED: (),
        CheckStanding.UNRESOLVED: (),
        CheckStanding.NOT_EVALUATED_BY_PREREQUISITE: _LINGUISTIC_BLOCKERS
        + (ExecutionLaw.ROLE_LICENSE_GRANTED_FOR_THE_FUNCTION_READ,),
    },
    ExecutionLaw.PREDICATE_ARITY_LICENSE_PERMITS_USE: {
        CheckStanding.SATISFIED: (),
        CheckStanding.VIOLATED: (),
    },
    ExecutionLaw.PREDICATE_ARITY_MATCHES_ITS_SLOTS: {
        CheckStanding.SATISFIED: (),
        CheckStanding.VIOLATED: (),
    },
    ExecutionLaw.ARGUMENT_SLOT_IDS_ARE_NOT_DEFERRED_ROLE_NAMES: {
        CheckStanding.SATISFIED: (),
        CheckStanding.VIOLATED: (),
    },
    ExecutionLaw.ANCHORS_DO_NOT_EXCEED_ARITY: {
        CheckStanding.SATISFIED: (),
        CheckStanding.VIOLATED: (),
    },
    ExecutionLaw.DECLARED_LINGUISTIC_IDENTITY_AGREES: {
        CheckStanding.SATISFIED: (),
        CheckStanding.VIOLATED: (),
        CheckStanding.UNRESOLVED: (),
        CheckStanding.NOT_EVALUATED_BY_PREREQUISITE: _LINGUISTIC_BLOCKERS,
        CheckStanding.NOT_APPLICABLE_NO_CLAIM: (),
    },
    ExecutionLaw.MATERIALIZED_IDENTITY_AGREES: {
        CheckStanding.SATISFIED: (),
        CheckStanding.VIOLATED: (),
        CheckStanding.NOT_EVALUATED_BY_PREREQUISITE: _ALL_PRIOR_LAWS,
        CheckStanding.NOT_APPLICABLE_NO_CLAIM: (),
    },
}
"""المنازلُ المطلوبُ بلوغُها لكلِّ قانون، ومعها القوانينُ التي قد تحجبها."""


_UNREACHABLE: Final[dict[ExecutionLaw, dict[CheckStanding, str]]] = {
    ExecutionLaw.NO_SELF_DERIVED_LICENSING_GENUS: {
        CheckStanding.NOT_EVALUATED_BY_PREREQUISITE: _NOT_GATED_BY_A_PRIOR_LAW,
        CheckStanding.NOT_APPLICABLE_NO_CLAIM: _NO_OPTIONAL_CLAIM,
    },
    ExecutionLaw.NO_UNREAD_CONDITION_IN_THE_FOUNDING_BASE: {
        CheckStanding.VIOLATED: _AN_UNREAD_CONDITION_IS_NOT_A_PROVED_BREACH,
        CheckStanding.NOT_EVALUATED_BY_PREREQUISITE: _NOT_GATED_BY_A_PRIOR_LAW,
        CheckStanding.NOT_APPLICABLE_NO_CLAIM: _NO_OPTIONAL_CLAIM,
    },
    ExecutionLaw.GENERAL_ONTOLOGY_FOUNDED_ON_THE_LINEAGE_BASE: {
        CheckStanding.NOT_EVALUATED_BY_PREREQUISITE: _NOT_GATED_BY_A_PRIOR_LAW,
        CheckStanding.NOT_APPLICABLE_NO_CLAIM: _NO_OPTIONAL_CLAIM,
    },
    ExecutionLaw.LINGUISTIC_LICENSES_NAME_REGISTERED_CANDIDATES: {
        CheckStanding.NOT_EVALUATED_BY_PREREQUISITE: _NOT_GATED_BY_A_PRIOR_LAW,
        CheckStanding.NOT_APPLICABLE_NO_CLAIM: _NO_OPTIONAL_CLAIM,
    },
    ExecutionLaw.LINGUISTIC_LICENSES_SHARE_THE_FOUNDING_BASE: {
        CheckStanding.NOT_EVALUATED_BY_PREREQUISITE: _NOT_GATED_BY_A_PRIOR_LAW,
        CheckStanding.NOT_APPLICABLE_NO_CLAIM: _NO_OPTIONAL_CLAIM,
    },
    ExecutionLaw.LINGUISTIC_ONTOLOGY_FOUNDED_ON_THE_LINEAGE_GENERAL: {
        CheckStanding.NOT_APPLICABLE_NO_CLAIM: _NO_OPTIONAL_CLAIM,
    },
    ExecutionLaw.EXISTENCE_LINEAGE_REDERIVES: {
        CheckStanding.NOT_APPLICABLE_NO_CLAIM: _NO_OPTIONAL_CLAIM,
    },
    ExecutionLaw.CONDITION_SITES_SHARE_THE_LINEAGE_BASE: {
        CheckStanding.NOT_EVALUATED_BY_PREREQUISITE: _NOT_GATED_BY_A_PRIOR_LAW,
        CheckStanding.NOT_APPLICABLE_NO_CLAIM: _NO_OPTIONAL_CLAIM,
    },
    ExecutionLaw.CONDITION_SITES_ARE_LICENSED_FOR_USE: {
        CheckStanding.NOT_EVALUATED_BY_PREREQUISITE: _NOT_GATED_BY_A_PRIOR_LAW,
        CheckStanding.NOT_APPLICABLE_NO_CLAIM: _NO_OPTIONAL_CLAIM,
    },
    ExecutionLaw.ROLE_SITES_SHARE_THE_LINEAGE_ONTOLOGY: {
        CheckStanding.NOT_EVALUATED_BY_PREREQUISITE: (
            "موضعُ الدور يُقارَن بأنطولوجيا السلسلة بالاسم المُصرَّح به وحدَه قبل أيّ "
            "اشتقاق؛ فلا تقف مادّتُه خلف فعلِ ترخيصٍ سابقٍ يحجبها"
        ),
        CheckStanding.NOT_APPLICABLE_NO_CLAIM: _NO_OPTIONAL_CLAIM,
    },
    ExecutionLaw.ROLE_LICENSE_GRANTED_FOR_THE_FUNCTION_READ: {
        CheckStanding.NOT_APPLICABLE_NO_CLAIM: _NO_OPTIONAL_CLAIM,
    },
    ExecutionLaw.ROLE_LICENSE_IS_OPERATIVE: {
        CheckStanding.NOT_APPLICABLE_NO_CLAIM: _NO_OPTIONAL_CLAIM,
    },
    ExecutionLaw.PREDICATE_ARITY_LICENSE_PERMITS_USE: {
        CheckStanding.UNRESOLVED: _SHAPE_IS_READ_FROM_THE_DECLARATION_ALONE,
        CheckStanding.NOT_EVALUATED_BY_PREREQUISITE: (
            _SHAPE_IS_READ_FROM_THE_DECLARATION_ALONE
        ),
        CheckStanding.NOT_APPLICABLE_NO_CLAIM: _NO_OPTIONAL_CLAIM,
    },
    ExecutionLaw.PREDICATE_ARITY_MATCHES_ITS_SLOTS: {
        CheckStanding.UNRESOLVED: _SHAPE_IS_READ_FROM_THE_DECLARATION_ALONE,
        CheckStanding.NOT_EVALUATED_BY_PREREQUISITE: (
            _SHAPE_IS_READ_FROM_THE_DECLARATION_ALONE
        ),
        CheckStanding.NOT_APPLICABLE_NO_CLAIM: _NO_OPTIONAL_CLAIM,
    },
    ExecutionLaw.ARGUMENT_SLOT_IDS_ARE_NOT_DEFERRED_ROLE_NAMES: {
        CheckStanding.UNRESOLVED: _SHAPE_IS_READ_FROM_THE_DECLARATION_ALONE,
        CheckStanding.NOT_EVALUATED_BY_PREREQUISITE: (
            _SHAPE_IS_READ_FROM_THE_DECLARATION_ALONE
        ),
        CheckStanding.NOT_APPLICABLE_NO_CLAIM: _NO_OPTIONAL_CLAIM,
    },
    ExecutionLaw.ANCHORS_DO_NOT_EXCEED_ARITY: {
        CheckStanding.UNRESOLVED: _SHAPE_IS_READ_FROM_THE_DECLARATION_ALONE,
        CheckStanding.NOT_EVALUATED_BY_PREREQUISITE: (
            _SHAPE_IS_READ_FROM_THE_DECLARATION_ALONE
        ),
        CheckStanding.NOT_APPLICABLE_NO_CLAIM: _NO_OPTIONAL_CLAIM,
    },
    ExecutionLaw.DECLARED_LINGUISTIC_IDENTITY_AGREES: {},
    ExecutionLaw.MATERIALIZED_IDENTITY_AGREES: {
        CheckStanding.UNRESOLVED: _A_NISBAH_IDENTITY_IS_NOT_MISSING_EVIDENCE,
    },
}
"""المنازلُ الممنوعةُ لكلِّ قانونٍ بتعليلها؛ ولا تُصطنَع لها حالة."""


def _law_standing_requirements() -> tuple[CoverageRequirement, ...]:
    """المحورُ الأوّل: كلُّ قانونٍ في كلِّ منزلة؛ لا خليّةَ تُطوى ولا تُكرَّر."""

    built: list[CoverageRequirement] = []
    for law in LAW_SET:
        reachable = _REACHABLE[law]
        refused = _UNREACHABLE[law]
        for standing in CheckStanding:
            identifier = f"LS.{law.value}.{standing.value}"
            if standing in reachable:
                built.append(
                    CoverageRequirement(
                        requirement_id=identifier,
                        axis=CoverageAxis.LAW_STANDING,
                        law=law,
                        target_standing=standing,
                        claim=None,
                        required=True,
                        reachable=True,
                        prerequisite_laws=reachable[standing],
                        forbidden_co_standings=tuple(
                            other for other in CheckStanding if other is not standing
                        ),
                        expected_outcome=_OUTCOME_OF_STANDING[standing],
                        case_id=None,
                        justification_if_unreachable=None,
                    )
                )
                continue
            built.append(
                CoverageRequirement(
                    requirement_id=identifier,
                    axis=CoverageAxis.LAW_STANDING,
                    law=law,
                    target_standing=standing,
                    claim=None,
                    required=False,
                    reachable=False,
                    prerequisite_laws=(),
                    forbidden_co_standings=(),
                    expected_outcome=ExpectedOutcome.NOT_CONSTRAINED,
                    case_id=None,
                    justification_if_unreachable=refused[standing],
                )
            )
    return tuple(built)


def _beyond_the_first_axis(
    requirement_id: str,
    axis: CoverageAxis,
    claim: str,
    expected_outcome: ExpectedOutcome,
    forbidden_co_standings: tuple[CheckStanding, ...] = (),
) -> CoverageRequirement:
    return CoverageRequirement(
        requirement_id=requirement_id,
        axis=axis,
        law=None,
        target_standing=None,
        claim=claim,
        required=True,
        reachable=True,
        prerequisite_laws=(),
        forbidden_co_standings=forbidden_co_standings,
        expected_outcome=expected_outcome,
        case_id=None,
        justification_if_unreachable=None,
    )


_OUTCOME_REACHABILITY: Final[tuple[CoverageRequirement, ...]] = (
    _beyond_the_first_axis(
        "OR.pass",
        CoverageAxis.OUTCOME_REACHABILITY,
        "حالةٌ واحدةُ الأصل كاملةُ العناصر تبلغ `PASS` وتُنشئ الهويّةَ السلطويّة",
        ExpectedOutcome.PASS,
        (CheckStanding.VIOLATED, CheckStanding.UNRESOLVED),
    ),
    _beyond_the_first_axis(
        "OR.block",
        CoverageAxis.OUTCOME_REACHABILITY,
        "حالةٌ يُخالَف فيها قانونٌ مُعلَنٌ فيثبت خرقُه، فتبلغ `BLOCK` بمخالفةٍ مُسمّاة",
        ExpectedOutcome.BLOCK,
    ),
    _beyond_the_first_axis(
        "OR.defer",
        CoverageAxis.OUTCOME_REACHABILITY,
        "حالةٌ ينقص فيها دليلٌ مُصرَّحٌ به بلا مخالفةٍ ثابتة، فتبلغ `DEFER` ببقيّةٍ مُسمّاة",
        ExpectedOutcome.DEFER,
        (CheckStanding.VIOLATED,),
    ),
    _beyond_the_first_axis(
        "OR.invalid_input",
        CoverageAxis.OUTCOME_REACHABILITY,
        "وثيقةٌ لا تقوم منها قضيّةٌ تُنتِج `InputValidation` فاسدةً ولا حكمَ معها؛ "
        "و`ExecutionOutcome` ليس فيها عضوٌ لفساد الإدخال",
        ExpectedOutcome.NO_VERDICT_INVALID_INPUT,
    ),
    _beyond_the_first_axis(
        "OR.invariant_error",
        CoverageAxis.OUTCOME_REACHABILITY,
        "شاهدُ وصولٍ لـ`ExecutionInvariantError`: ليس حكمًا ولا حالةَ مستخدم، بل عطبٌ "
        "داخليّ؛ فيُبلَغ عند وصل المحرّك بمادّةٍ مُشتَقّةٍ ناقصةٍ بعد نجاحٍ مبدئيّ، لا "
        "بوثيقةٍ يكتبها صاحبُ قضيّة",
        ExpectedOutcome.NO_VERDICT_INVARIANT_ERROR,
    ),
)


_CROSS_STAGE_SEPARATION: Final[tuple[CoverageRequirement, ...]] = (
    _beyond_the_first_axis(
        "XS.invalid_input_has_no_envelope",
        CoverageAxis.CROSS_STAGE_SEPARATION,
        "فسادُ الإدخال لا يُنتِج `ExecutionResultEnvelope` ألبتّة",
        ExpectedOutcome.NO_VERDICT_INVALID_INPUT,
    ),
    _beyond_the_first_axis(
        "XS.block_has_no_materialized_identity",
        CoverageAxis.CROSS_STAGE_SEPARATION,
        "`BLOCK` لا يُنتِج هويّةً سلطويّةً مُشيَّدة",
        ExpectedOutcome.BLOCK,
    ),
    _beyond_the_first_axis(
        "XS.defer_has_no_materialized_identity",
        CoverageAxis.CROSS_STAGE_SEPARATION,
        "`DEFER` لا يُنتِج هويّةً سلطويّةً مُشيَّدة",
        ExpectedOutcome.DEFER,
        (CheckStanding.VIOLATED,),
    ),
    _beyond_the_first_axis(
        "XS.pass_has_a_materialized_identity",
        CoverageAxis.CROSS_STAGE_SEPARATION,
        "`PASS` لا يخلو من هويّةٍ سلطويّةٍ مُشيَّدة؛ والعلاقةُ ثنائيّةُ الاتّجاه",
        ExpectedOutcome.PASS,
        (CheckStanding.VIOLATED, CheckStanding.UNRESOLVED),
    ),
    _beyond_the_first_axis(
        "XS.invariant_error_has_no_verdict_and_no_envelope",
        CoverageAxis.CROSS_STAGE_SEPARATION,
        "`ExecutionInvariantError` لا يُنتِج حكمًا ولا غلافًا مختومًا",
        ExpectedOutcome.NO_VERDICT_INVARIANT_ERROR,
    ),
    _beyond_the_first_axis(
        "XS.blocked_dependent_has_no_residual",
        CoverageAxis.CROSS_STAGE_SEPARATION,
        "`NOT_EVALUATED_BY_PREREQUISITE` لا يُنتِج بقيّةً؛ فالمحجوبُ ليس دليلًا ناقصًا",
        ExpectedOutcome.INHERITED,
    ),
    _beyond_the_first_axis(
        "XS.no_claim_is_not_read_as_satisfied",
        CoverageAxis.CROSS_STAGE_SEPARATION,
        "`NOT_APPLICABLE_NO_CLAIM` لا يُقرَأ `SATISFIED`؛ وغيابُ الدعوى ليس تصديقًا لها",
        ExpectedOutcome.PASS,
        (CheckStanding.SATISFIED,),
    ),
)


COVERAGE_MATRIX_ID: Final[str] = "alghanem.execution.coverage.G0.CASE-0.MATRIX"
"""اسمُ المصفوفة؛ وهويّتُها الحاكمةُ بصمتُها لا اسمُها."""

COVERAGE_MATRIX: Final[CoverageMatrix] = CoverageMatrix(
    matrix_id=COVERAGE_MATRIX_ID,
    requirements=(
        _law_standing_requirements() + _OUTCOME_REACHABILITY + _CROSS_STAGE_SEPARATION
    ),
)
"""المصفوفةُ المجمَّدة: ثلاثةُ محاورَ، ولا حالةَ مسمّاةٌ في واحدٍ منها."""

COVERAGE_MATRIX_DIGEST: Final[str] = canonical_digest(
    canonical_bytes(COVERAGE_MATRIX.as_canonical_content())
)
"""بصمةُ المصفوفة؛ تتغيّر بتغيّر مطلبٍ أو رتبته أو تعليله، وليست بصمةَ تنفيذ."""
