"""رتبُ المنتَج وشهادتُه: ثلاثُ رتبٍ أنواعٌ لا قيمٌ، وشهادةٌ مُواصَفةٌ لا تُصدَر بعد.

    SurfaceCandidate → SpecificationConformantSurface → CertifiedGeneratedUtterance

**والرتبةُ الثانيةُ مطابقةٌ لا ترخيص** (`ConformanceIsNotLicensing`): البوّابةُ
تقيس المنتَجَ على **مواصفته** — ترتيبُ السطح، وموضعُ كلِّ رمزٍ كما أسنده صاحبُ
المواصفة، ومُعرِّفُ اختياره، وأثرُ إعراب عائلته، واتّصالُ سلسلته ببصماتها —
فتُثبِت أنّ دعوى صاحب المواصفة حُفِظت، لا أنّها مرخَّصةٌ من المصدر:

    CallerClaim → ConformsToCallerClaim  ⇏  Licensed

فلا يُفتَح اسمُ `StructurallyLicensedSurface` هنا؛ وهو محجوزٌ بالنصّ لا مُعرَّفٌ
بالنوع، ولا يُفتَح إلّا بعد `SyntacticBindingCertificate` التي تُثبِت
`Anchor →evidence→ LicensedSyntacticPosition`. وذلك مُسمًّى بمُعرِّفه:
`RES.GEN0.NoIndependentAnchorToSyntacticFunctionAuthority`.

**ولذلك يحمل كلُّ قرار مطابقةٍ بقاياه**: إسنادُ الفاعليّة والمفعوليّة غيرُ
مرخَّص، والمرجعُ المعجميُّ دعوى حتى `DATA` ثمّ `READOUT`. فلا يُقرأ نجاحُ
البوّابة أوسعَ من مداه.

**وما تُثبِته البوّابةُ من الأصل محدود** (`MetadataConformance ≠
GenerationProvenance`): تشدُّ العبارةَ إلى سلسلتها بالبصمات — مدخلُ الأثر بصمةُ
المواصفة، وآخرُ خطوةٍ إسقاطٌ كتابيٌّ مخرجُه بصمةُ الإسقاط، والبصمةُ تُعاد من
الرموز نفسِها، وأثرُ كلِّ رمزٍ يبدأ من بصمة المواصفة — ولا سلطةَ لها اليومَ
تُثبِت أنّ `surface` صورةُ مدخلةٍ معجميّةٍ مشهودةٍ لا نصًّا عربيًّا مُلفَّقًا.

**والرتبةُ ليست حقلًا يكتبه المستدعي** (`CallerDoesNotOwnGenerationRank`): لا
تُنشَأ الرتبتان العليا إلّا من بوّابةٍ تُصدِرهما، فلا يبلغ منتَجٌ رتبةً بأن
يُعلنها عن نفسه.

**وشهادةُ الذهاب والإياب**:

    GenerationCertificate
      = ForwardTrace + BackwardReconstruction + InvariantMatch + Residuals

بحيث إن كان `G(S)=U` فإنّ `A(U)=S'` و`S' ≃ S` **بحسب الثوابت المطلوبة** لا
بتطابق البايتات.

**وهي مُواصَفةٌ لا تُصدَر في `GEN-0`** (`RoundTripIsSpecifiedNotIssuable`):
طبقةُ التحليل القائمةُ تُرجِع **الحالةَ** الإعرابيّة لا **الوظيفة** — وهو نصُّ
`ACCUSATIVE_IS_NOT_OBJECTHOOD` في `arabic/irab_case_readout.py` — فلا سلطةَ هنا
تُثبِت أنّ الموقعَ استُرجِع. فمجالُ بوّابة الشهادة اليومَ عضوٌ واحدٌ: تأجيلٌ
مُسبَّب؛ ولا تُصدَر `CertifiedGeneratedUtterance` ألبتّة.

تسجيلٌ لا سلطة: لا ولادةَ، ولا حكمَ ولادةٍ، ولا تجميدَ `E0`.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Final

from .candidate import (
    GeneratedArabicUtterance,
    OrthographicProjection,
    specification_content_id,
)
from .laws import (
    CALLER_DOES_NOT_OWN_GENERATION_RANK,
    CONFORMANCE_IS_NOT_LICENSING,
    LEXICAL_CHOICE_REF_IS_A_CLAIM_UNTIL_THE_READOUT,
    NO_CERTIFIED_GENERATION_WITHOUT_ROUND_TRIP,
    NO_GENERATION_AUTHORITY_BEYOND_ITS_SOURCE,
    NO_INDEPENDENT_ANCHOR_TO_SYNTACTIC_FUNCTION_AUTHORITY,
    NO_INDEPENDENT_ANCHOR_TO_SYNTACTIC_FUNCTION_AUTHORITY_ID,
    NO_INFLECTION_WITHOUT_LICENSED_SLOT,
    NO_SURFACE_WITHOUT_SOURCE_ANCHOR,
)
from .specification import FormSelectionMode, ProductionSpecification
from .trace import (
    A_CHAIN_IS_READ_FROM_ITS_DIGESTS_NOT_ITS_ORDER,
    GenerationResidual,
    GenerationResidualKind,
    GenerationStage,
)

__all__ = [
    "CONFORMANCE_RESIDUALS",
    "CertifiedGeneratedUtterance",
    "GEN0_PRESERVED_INVARIANTS",
    "GenerationRankError",
    "PreservedGenerationInvariant",
    "PreservedInvariantSpec",
    "ROUND_TRIP_IS_SPECIFIED_NOT_ISSUABLE",
    "RoundTripCertificate",
    "RoundTripDecision",
    "RoundTripGate",
    "RoundTripStatus",
    "SpecificationConformanceDecision",
    "SpecificationConformanceGate",
    "SpecificationConformanceStatus",
    "SpecificationConformantSurface",
    "SurfaceCandidate",
]


ROUND_TRIP_IS_SPECIFIED_NOT_ISSUABLE: Final[str] = (
    "شهادةُ الذهاب والإياب مُواصَفةٌ لا تُصدَر: طبقةُ التحليل القائمةُ تُرجِع "
    "الحالةَ الإعرابيّةَ لا الوظيفةَ النحويّة، فلا سلطةَ هنا تُثبِت استرجاعَ "
    "الموقع؛ ومجالُ البوّابة اليومَ تأجيلٌ مُسبَّبٌ واحدٌ لا غير"
)


class GenerationRankError(ValueError):
    """رفضٌ عند تكوين رتبةٍ أو شهادةٍ أو قرارِ بوّابة."""


class _IssuanceToken:
    """رمزُ إصدارٍ داخليّ؛ وجودُه بيد البوّابة وحدَها لا بيد المستدعي."""

    __slots__ = ()


_CONFORMANCE_ISSUANCE: Final[_IssuanceToken] = _IssuanceToken()
_CERTIFICATE_ISSUANCE: Final[_IssuanceToken] = _IssuanceToken()


@dataclass(frozen=True, slots=True)
class SurfaceCandidate:
    """الرتبةُ الأولى: مرشَّحٌ سطحيٌّ أُنتِج؛ ولا دعوى ترخيصٍ فيه ولا شهادة."""

    utterance: GeneratedArabicUtterance
    specification_content_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.utterance, GeneratedArabicUtterance):
            raise GenerationRankError("المرشَّحُ السطحيُّ عبارةٌ منتَجةٌ من نوعها")
        if self.utterance.specification_content_id != self.specification_content_id:
            raise GenerationRankError(
                "المرشَّحُ مشدودٌ إلى بصمة مواصفته؛ و"
                + NO_GENERATION_AUTHORITY_BEYOND_ITS_SOURCE
            )

    @property
    def residuals(self) -> tuple[GenerationResidual, ...]:
        """بقايا المرشَّح مرصودةً من أثره."""

        return self.utterance.residuals


@dataclass(frozen=True, slots=True)
class SpecificationConformantSurface:
    """الرتبةُ الثانية: سطحٌ ثبت أنّه تابعٌ لمواصفته وعائلتها، لا أنّه مرخَّصٌ نحويًّا.

    ولا تُنشَأ إلّا ببوّابة؛ و`ConformanceIsNotLicensing` يمنع قراءةَ هذه الرتبة
    ترخيصًا لإسناد الفاعليّة والمفعوليّة.
    """

    candidate: SurfaceCandidate
    specification: ProductionSpecification
    issuance: _IssuanceToken

    def __post_init__(self) -> None:
        if self.issuance is not _CONFORMANCE_ISSUANCE:
            raise GenerationRankError(CALLER_DOES_NOT_OWN_GENERATION_RANK)
        if not isinstance(self.candidate, SurfaceCandidate):
            raise GenerationRankError("الرتبةُ الثانيةُ فوق مرشَّحٍ من نوعه")


@dataclass(frozen=True, slots=True)
class CertifiedGeneratedUtterance:
    """الرتبةُ الثالثة: منتَجٌ مُشهَدٌ بالذهاب والإياب؛ ولا تُصدَر في `GEN-0`."""

    conformant: SpecificationConformantSurface
    certificate: RoundTripCertificate
    issuance: _IssuanceToken

    def __post_init__(self) -> None:
        if self.issuance is not _CERTIFICATE_ISSUANCE:
            raise GenerationRankError(CALLER_DOES_NOT_OWN_GENERATION_RANK)
        if not isinstance(self.certificate, RoundTripCertificate):
            raise GenerationRankError(NO_CERTIFIED_GENERATION_WITHOUT_ROUND_TRIP)


class PreservedGenerationInvariant(Enum):
    """الثوابتُ التي يجب أن يحفظها الذهابُ والإياب؛ مفردةٌ مغلقةٌ مُجمَّدة."""

    RELATION = "relation"
    ANCHORS = "anchors"
    POSITIONS = "positions"
    TENSE = "tense"
    VOICE = "voice"
    CASE_RELATIONS = "case_relations"


@dataclass(frozen=True, slots=True)
class PreservedInvariantSpec:
    """مواصفةُ الثوابت المطلوبة؛ تُجمَّد قبل وجود محلِّلٍ يقيسها."""

    components: tuple[PreservedGenerationInvariant, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.components, tuple) or not self.components:
            raise GenerationRankError("مواصفةُ الثوابت مكوِّنٌ فأكثر")
        if len(set(self.components)) != len(self.components):
            raise GenerationRankError("مكوِّنُ ثابتٍ لا يتكرّر في مواصفةٍ واحدة")
        for component in self.components:
            if not isinstance(component, PreservedGenerationInvariant):
                raise GenerationRankError("مكوِّنُ الثابت عضوٌ في مفردته المغلقة")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المواصفة للبصمة."""

        return {"components": [component.value for component in self.components]}


GEN0_PRESERVED_INVARIANTS: Final[PreservedInvariantSpec] = PreservedInvariantSpec(
    components=tuple(PreservedGenerationInvariant)
)


@dataclass(frozen=True, slots=True)
class RoundTripCertificate:
    """شهادةٌ: أثرُ الذهاب، وإعادةُ البناء، ومطابقةُ الثوابت، والبقايا."""

    forward_trace_content_id: str
    backward_structure_content_id: str
    invariant_spec: PreservedInvariantSpec
    invariant_match: Mapping[PreservedGenerationInvariant, bool]
    residuals: tuple[GenerationResidual, ...]
    issuance: _IssuanceToken

    def __post_init__(self) -> None:
        if self.issuance is not _CERTIFICATE_ISSUANCE:
            raise GenerationRankError(ROUND_TRIP_IS_SPECIFIED_NOT_ISSUABLE)
        if not isinstance(self.invariant_spec, PreservedInvariantSpec):
            raise GenerationRankError("مواصفةُ الثوابت من نوعها")
        covered = tuple(self.invariant_match)
        if set(covered) != set(self.invariant_spec.components):
            raise GenerationRankError(
                "المطابقةُ تُغطّي كلَّ مكوِّنٍ في المواصفة؛ ومكوِّنٌ لم يُقَس ليس موافقًا"
            )
        if not all(self.invariant_match.values()):
            raise GenerationRankError(NO_CERTIFIED_GENERATION_WITHOUT_ROUND_TRIP)
        object.__setattr__(
            self, "invariant_match", MappingProxyType(dict(self.invariant_match))
        )


class SpecificationConformanceStatus(Enum):
    """حكمُ المطابقة؛ ولا عضوَ فيه لترخيصٍ ولا لرتبةٍ أعلى."""

    CONFORMANT = "conformant"
    REFUSED = "refused"


CONFORMANCE_RESIDUALS: Final[tuple[GenerationResidual, ...]] = (
    GenerationResidual(
        kind=GenerationResidualKind.UNLICENSED_SYNTACTIC_FUNCTION_ASSIGNMENT,
        stage=GenerationStage.SPECIFICATION_CONFORMANCE,
        subject_id=NO_INDEPENDENT_ANCHOR_TO_SYNTACTIC_FUNCTION_AUTHORITY_ID,
        reason=NO_INDEPENDENT_ANCHOR_TO_SYNTACTIC_FUNCTION_AUTHORITY,
    ),
    GenerationResidual(
        kind=GenerationResidualKind.UNATTESTED_LEXICAL_REFERENCE,
        stage=GenerationStage.SPECIFICATION_CONFORMANCE,
        subject_id="lexical_choice_refs",
        reason=LEXICAL_CHOICE_REF_IS_A_CLAIM_UNTIL_THE_READOUT,
    ),
)


@dataclass(frozen=True, slots=True)
class SpecificationConformanceDecision:
    """قرارُ بوّابةِ المطابقة: حكمُه وسببُه وبقاياه، والرتبةُ عند المطابقة وحدَها."""

    status: SpecificationConformanceStatus
    reason: str
    conformant: SpecificationConformantSurface | None
    residuals: tuple[GenerationResidual, ...] = field(default=())

    def __post_init__(self) -> None:
        if not isinstance(self.status, SpecificationConformanceStatus):
            raise GenerationRankError("حكمُ المطابقة عضوٌ في مفردته المغلقة")
        if not isinstance(self.reason, str) or not self.reason.strip():
            raise GenerationRankError("سببُ القرار نصٌّ غير فارغ؛ ولا قرارَ صامت")
        if (self.status is SpecificationConformanceStatus.CONFORMANT) != (
            self.conformant is not None
        ):
            raise GenerationRankError(
                "المطابقةُ وحدَها تبلغ الرتبةَ الثانية، ولا مطابقةَ بلا رتبةٍ "
                "ولا رتبةَ بلا مطابقة"
            )
        if self.status is SpecificationConformanceStatus.CONFORMANT and (
            self.residuals != CONFORMANCE_RESIDUALS
        ):
            raise GenerationRankError(
                "قرارُ المطابقة يحمل بقاياه المُسمّاة كاملةً: إسنادُ الوظيفة "
                "النحويّة غيرُ مرخَّص، والمرجعُ المعجميُّ غيرُ مشهود؛ و"
                + CONFORMANCE_IS_NOT_LICENSING
            )


class SpecificationConformanceGate:
    """البوّابةُ الوحيدةُ التي تُصدِر الرتبةَ الثانية؛ ولا تقبل من المستدعي حكمًا."""

    @staticmethod
    def assess(
        *, candidate: SurfaceCandidate, specification: ProductionSpecification
    ) -> SpecificationConformanceDecision:
        """قِس المرشَّحَ على مواصفته وعائلتها؛ ولا تُصدِر رتبةً إلّا عن قياس."""

        if not isinstance(candidate, SurfaceCandidate):
            raise GenerationRankError("المُقاسُ مرشَّحٌ سطحيٌّ من نوعه")
        if not isinstance(specification, ProductionSpecification):
            raise GenerationRankError("المواصفةُ المقيسُ عليها من نوعها")
        if candidate.specification_content_id != specification_content_id(
            specification
        ):
            return SpecificationConformanceDecision(
                status=SpecificationConformanceStatus.REFUSED,
                reason=(
                    "المرشَّحُ ليس من هذه المواصفة: بصمتُها لا تُطابِق البصمةَ التي "
                    "بُني عليها؛ و" + NO_GENERATION_AUTHORITY_BEYOND_ITS_SOURCE
                ),
                conformant=None,
            )
        family = specification.production_family
        tokens = candidate.utterance.tokens
        if tuple(token.syntactic_target for token in tokens) != family.surface_order:
            return SpecificationConformanceDecision(
                status=SpecificationConformanceStatus.REFUSED,
                reason=(
                    "مواضعُ الرموز ليست مواضعَ العائلة بترتيب سطحها؛ و"
                    + NO_INFLECTION_WITHOUT_LICENSED_SLOT
                ),
                conformant=None,
            )
        assigned = {
            assignment.element_id: assignment.target
            for assignment in specification.realization_targets
        }
        choices = {
            choice.element_id: choice.choice_id
            for choice in specification.lexical_choice_refs
        }
        for token in tokens:
            target = assigned.get(token.source_element_id)
            if target is None:
                return SpecificationConformanceDecision(
                    status=SpecificationConformanceStatus.REFUSED,
                    reason=(
                        "رمزٌ يُنسَب إلى عنصرٍ لا موضعَ له في المواصفة؛ و"
                        + NO_SURFACE_WITHOUT_SOURCE_ANCHOR
                    ),
                    conformant=None,
                )
            if target is not token.syntactic_target:
                return SpecificationConformanceDecision(
                    status=SpecificationConformanceStatus.REFUSED,
                    reason="رمزٌ تحقّق في موضعٍ غير الموضع المُسنَد إلى عنصره",
                    conformant=None,
                )
            if choices.get(token.source_element_id) != token.lexical_choice_id:
                return SpecificationConformanceDecision(
                    status=SpecificationConformanceStatus.REFUSED,
                    reason="اختيارُ الرمز المعجميُّ ليس اختيارَ عنصره في المواصفة",
                    conformant=None,
                )
            if token.case_effect is not family.case_effect_for(token.syntactic_target):
                return SpecificationConformanceDecision(
                    status=SpecificationConformanceStatus.REFUSED,
                    reason=(
                        "أثرُ إعراب الرمز ليس أثرَ موضعه في العائلة؛ و"
                        + NO_INFLECTION_WITHOUT_LICENSED_SLOT
                    ),
                    conformant=None,
                )
        chain_refusal = SpecificationConformanceGate._refuse_a_broken_chain(
            candidate=candidate
        )
        if chain_refusal is not None:
            return chain_refusal
        return SpecificationConformanceDecision(
            status=SpecificationConformanceStatus.CONFORMANT,
            reason=(
                "كلُّ رمزٍ رُدَّ إلى عنصرٍ في المصدر، وتحقّق في موضعه المُسنَد، "
                "بأثرِ إعراب عائلته، وبترتيب سطحها، وسلسلتُه متّصلةٌ ببصماتها "
                "من المواصفة إلى الإسقاط الكتابيّ؛ ولا ترخيصَ نحويًّا في ذلك، و"
                + CONFORMANCE_IS_NOT_LICENSING
            ),
            conformant=SpecificationConformantSurface(
                candidate=candidate,
                specification=specification,
                issuance=_CONFORMANCE_ISSUANCE,
            ),
            residuals=CONFORMANCE_RESIDUALS,
        )

    @staticmethod
    def _refuse_a_broken_chain(
        *, candidate: SurfaceCandidate
    ) -> SpecificationConformanceDecision | None:
        """اقرأ اتّصالَ العبارة ببصماتها؛ فالوصفُ المطابقُ ليس أثرَ إنتاجٍ جرى."""

        utterance = candidate.utterance
        trace = utterance.trace
        if trace.input_content_id != candidate.specification_content_id:
            return SpecificationConformanceDecision(
                status=SpecificationConformanceStatus.REFUSED,
                reason=(
                    "أثرُ العبارة لا يبدأ من بصمة مواصفتها؛ و"
                    + A_CHAIN_IS_READ_FROM_ITS_DIGESTS_NOT_ITS_ORDER
                ),
                conformant=None,
            )
        last = trace.steps[-1]
        if last.stage is not GenerationStage.ORTHOGRAPHIC_PROJECTION:
            return SpecificationConformanceDecision(
                status=SpecificationConformanceStatus.REFUSED,
                reason=(
                    "آخرُ خطوةٍ في أثر العبارة إسقاطٌ كتابيّ؛ وعبارةٌ تنتهي بغيره "
                    "صورةٌ بلا مرحلةٍ أخرجتها"
                ),
                conformant=None,
            )
        if last.output_content_id != utterance.orthographic_content_id:
            return SpecificationConformanceDecision(
                status=SpecificationConformanceStatus.REFUSED,
                reason=(
                    "بصمةُ الإسقاط الكتابيِّ في العبارة ليست مخرجَ خطوته؛ و"
                    + A_CHAIN_IS_READ_FROM_ITS_DIGESTS_NOT_ITS_ORDER
                ),
                conformant=None,
            )
        recomputed = OrthographicProjection(
            case_effect_content_id=last.input_content_id,
            tokens=utterance.tokens,
            orthographic_source=FormSelectionMode.LEXICALLY_ATTESTED_FORM_SELECTION,
        )
        for token in utterance.tokens:
            if token.generation_trace.input_content_id != (
                candidate.specification_content_id
            ):
                return SpecificationConformanceDecision(
                    status=SpecificationConformanceStatus.REFUSED,
                    reason=(
                        "أثرُ رمزٍ لا يبدأ من بصمة المواصفة نفسِها؛ فهو أثرٌ مجاورٌ "
                        "لا سلسلةٌ واحدة؛ و"
                        + A_CHAIN_IS_READ_FROM_ITS_DIGESTS_NOT_ITS_ORDER
                    ),
                    conformant=None,
                )
        if recomputed.content_id != utterance.orthographic_content_id:
            return SpecificationConformanceDecision(
                status=SpecificationConformanceStatus.REFUSED,
                reason=(
                    "رموزُ العبارة ليست رموزَ الإسقاط الكتابيِّ الذي تحمل بصمتَه؛ "
                    "والبصمةُ تُعاد من الرموز لا تُؤخَذ دعوى"
                ),
                conformant=None,
            )
        return None


class RoundTripStatus(Enum):
    """حكمُ بوّابة الذهاب والإياب؛ ومجالُها اليومَ عضوٌ واحدٌ مُسبَّب."""

    DEFERRED_NO_FUNCTION_RECOVERING_ANALYSER = (
        "deferred_no_function_recovering_analyser"
    )


@dataclass(frozen=True, slots=True)
class RoundTripDecision:
    """قرارُ بوّابةِ الشهادة: حكمُه وسببُه وثوابتُه المطلوبة، وشهادةٌ عند صدورها."""

    status: RoundTripStatus
    reason: str
    invariant_spec: PreservedInvariantSpec
    certificate: RoundTripCertificate | None = field(default=None)

    def __post_init__(self) -> None:
        if not isinstance(self.status, RoundTripStatus):
            raise GenerationRankError("حكمُ الشهادة عضوٌ في مفردته المغلقة")
        if not isinstance(self.reason, str) or not self.reason.strip():
            raise GenerationRankError("سببُ التأجيل مُسمًّى لا صمت")
        if self.certificate is not None:
            raise GenerationRankError(ROUND_TRIP_IS_SPECIFIED_NOT_ISSUABLE)


class RoundTripGate:
    """البوّابةُ الوحيدةُ للشهادة؛ ولا تُصدِر اليومَ إلّا تأجيلًا مُسبَّبًا."""

    @staticmethod
    def assess(*, conformant: SpecificationConformantSurface) -> RoundTripDecision:
        """اقرأ سطحًا مطابقًا لمواصفته، وأجِّل الشهادةَ بسببها المُسمّى."""

        if not isinstance(conformant, SpecificationConformantSurface):
            raise GenerationRankError(
                "المُقاسُ في بوّابة الشهادة سطحٌ بلغ الرتبةَ الثانية؛ و"
                + NO_CERTIFIED_GENERATION_WITHOUT_ROUND_TRIP
            )
        return RoundTripDecision(
            status=RoundTripStatus.DEFERRED_NO_FUNCTION_RECOVERING_ANALYSER,
            reason=ROUND_TRIP_IS_SPECIFIED_NOT_ISSUABLE,
            invariant_spec=GEN0_PRESERVED_INVARIANTS,
        )
