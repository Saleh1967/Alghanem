"""سلسلةُ الإنتاج: مراحلُ مفصولةٌ بالنوع، وإسقاطان أخوان لا سلسلةٌ واحدة.

    ProductionSpecification
      → LexicalSelectionCandidate
      → WordFormCandidate
      → RelationSlotAssignment
      → CompositionCandidate
      → CaseEffectCandidate
      →  { PhonologicalProjection : WITHHELD ,  OrthographicProjection }
      → GeneratedArabicUtterance

**والحجبُ نوعٌ لا قيمةُ حقل** (`AnUnrealizedLayerIsAWithheldStageNotANull`):
`StageReadout = GeneratedStage[T] | WithheldStage`، فلا يستوي «لم يُنتَج» و
«أُنتِج فكان لا شيء»، ولا يُقرأ حقلُ حالةٍ ليُعلَم أيُّهما وقع.

**والإسقاطان أخوان بعد التكوين** (`OrthographyNeedNotClaimPhonologicalDerivation`):
لو كان الرسمُ ابنًا للطبقة الصوتيّة، وهي محجوزةٌ لأنّ المقطعَ والوزنَ لم يُقاسا،
لامتنع الرسمُ كلُّه. فكلاهما يُبنى على `CaseEffectCandidate` مباشرةً، ويُبنى
الرسمُ من صورةٍ معجميّةٍ مُجمَّدةٍ لا من اشتقاقٍ صوتيٍّ يُدَّعى.

**ولا رمزَ سطحيٍّ بلا مرساة** (`NoSurfaceWithoutSourceAnchor`): كلُّ
`SurfaceToken` يحمل عنصرَ مصدره وموضعَه وأثرَه واختيارَه، فتكون العبارةُ شبكةً
يُردّ كلُّ رمزٍ فيها إلى سبب إنتاجه، لا نصًّا مسطورًا.

تسجيلٌ لا سلطة: لا ولادةَ، ولا حكمَ ولادةٍ، ولا تجميدَ `E0`.
"""

from __future__ import annotations

import unicodedata
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Final, Generic, TypeAlias, TypeVar

from ..canonical_content import canonical_bytes, canonical_digest
from .laws import (
    AN_UNREALIZED_LAYER_IS_A_WITHHELD_STAGE_NOT_A_NULL,
    NO_COMPOSITION_WITHOUT_RELATION,
    NO_INFLECTION_WITHOUT_LICENSED_SLOT,
    NO_SURFACE_WITHOUT_SOURCE_ANCHOR,
    NO_WORD_FORM_WITHOUT_MORPHOLOGICAL_TRACE,
    ORTHOGRAPHY_NEED_NOT_CLAIM_PHONOLOGICAL_DERIVATION,
)
from .specification import (
    CaseEffect,
    FormSelectionMode,
    LexicalChoiceRef,
    ProductionSpecification,
    SyntacticRealizationTarget,
)
from .trace import (
    A_CHAIN_IS_READ_FROM_ITS_DIGESTS_NOT_ITS_ORDER,
    GenerationResidual,
    GenerationResidualKind,
    GenerationStage,
    GenerationStep,
    GenerationTrace,
)

__all__ = [
    "CaseEffectCandidate",
    "CompositionCandidate",
    "GeneratedArabicUtterance",
    "GeneratedStage",
    "GenerationCandidateError",
    "LexicalSelectionCandidate",
    "MorphologicalOperation",
    "OrthographicProjection",
    "DO_NOT_STORE_DERIVABLE_IDENTITY_AS_A_SECOND_CLAIM",
    "PHONOLOGICAL_PROJECTION_IS_WITHHELD_IN_GEN0",
    "RelationSlotAssignment",
    "StageReadout",
    "SurfaceToken",
    "specification_content_id",
    "WithheldStage",
    "WordFormCandidate",
    "withheld_phonological_projection",
]


DO_NOT_STORE_DERIVABLE_IDENTITY_AS_A_SECOND_CLAIM: Final[str] = (
    "لا تُخزَّن هويّةٌ مُشتَقّةٌ دعوًى ثانية: ما يُحسَب من محتوًى محمولٍ في الكائن "
    "يُقرأ منه لا يُكتَب بجانبه، لأنّ حقلين لشيءٍ واحدٍ يفتحان انحرافًا بينهما "
    "لا يُغلِقه إلّا فحصٌ قد يُنسى"
)

PHONOLOGICAL_PROJECTION_IS_WITHHELD_IN_GEN0: Final[str] = (
    "الإسقاطُ الصوتيُّ محجوزٌ في `GEN-0`: المقطعُ والوزنُ طبقتان غيرُ مقيستين، "
    "فلا تُخرَج صورةٌ صوتيّةٌ بحقلِ فراغ، بل مرحلةٌ محجوزةٌ باسمِ تعذّرها"
)


class GenerationCandidateError(ValueError):
    """رفضٌ عند تكوين مرحلةٍ من مراحل السلسلة."""


def _content_id(content: object) -> str:
    """بصمةٌ قانونيّةٌ لمحتوى مرحلة؛ مصدرُها واحدٌ لا يُكرَّر في هذه الطبقة."""

    return canonical_digest(canonical_bytes(content))


class MorphologicalOperation(Enum):
    """عمليّةٌ صرفيّةٌ مُسمّاة؛ والاختيارُ المشهودُ عمليّةٌ مُصرَّحٌ بها لا صمت."""

    LEXICALLY_ATTESTED_FORM_SELECTION = "lexically_attested_form_selection"


T = TypeVar("T")


@dataclass(frozen=True)
class GeneratedStage(Generic[T]):
    """مرحلةٌ أُنتِجت: حمولتُها، والخطوةُ التي أنتجتها، وبصمتُهما متطابقتان."""

    stage: GenerationStage
    payload: T
    step: GenerationStep

    def __post_init__(self) -> None:
        if not isinstance(self.stage, GenerationStage):
            raise GenerationCandidateError("مرحلةُ الإنتاج عضوٌ في مفردتها المغلقة")
        if not isinstance(self.step, GenerationStep):
            raise GenerationCandidateError("خطوةُ الإنتاج من نوعها لا وصفٌ حرّ")
        if self.step.stage is not self.stage:
            raise GenerationCandidateError("خطوةٌ تُنسَب إلى مرحلةٍ غير مرحلتها")
        content_id = getattr(self.payload, "content_id", None)
        if not isinstance(content_id, str):
            raise GenerationCandidateError("حمولةُ المرحلة تحمل بصمتَها المُشتَقّة")
        if self.step.output_content_id != content_id:
            raise GenerationCandidateError(
                "مخرجُ الخطوة هو بصمةُ حمولتها بعينها؛ ولا حمولةَ تُكتَب "
                "بجانب خطوةٍ لم تُخرِجها"
            )

    @property
    def content_id(self) -> str:
        """بصمةُ حمولة المرحلة."""

        produced: str = getattr(self.payload, "content_id")
        return produced


@dataclass(frozen=True, slots=True)
class WithheldStage:
    """مرحلةٌ محجوزة: لا حمولةَ لها، وبقيّتُها تُسمّي تعذّرَها ولا تُستنتَج."""

    stage: GenerationStage
    step: GenerationStep
    residual: GenerationResidual

    def __post_init__(self) -> None:
        if not isinstance(self.stage, GenerationStage):
            raise GenerationCandidateError("مرحلةُ الحجز عضوٌ في مفردتها المغلقة")
        if not isinstance(self.step, GenerationStep):
            raise GenerationCandidateError("خطوةُ الحجز من نوعها لا وصفٌ حرّ")
        if not isinstance(self.residual, GenerationResidual):
            raise GenerationCandidateError(
                "المرحلةُ المحجوزةُ بقيّةٌ مُسمّاةٌ لا فراغ؛ و"
                + AN_UNREALIZED_LAYER_IS_A_WITHHELD_STAGE_NOT_A_NULL
            )
        if self.step.stage is not self.stage or self.residual.stage is not self.stage:
            raise GenerationCandidateError("الخطوةُ والبقيّةُ من مرحلة الحجز نفسِها")
        if self.step.output_content_id is not None:
            raise GenerationCandidateError(
                "مرحلةٌ محجوزةٌ لا مخرجَ لها؛ و"
                + AN_UNREALIZED_LAYER_IS_A_WITHHELD_STAGE_NOT_A_NULL
            )
        if self.residual not in self.step.residuals:
            raise GenerationCandidateError(
                "بقيّةُ الحجز مرصودةٌ في خطوتها لا مكتوبةٌ بجانبها"
            )


StageReadout: TypeAlias = GeneratedStage[T] | WithheldStage


@dataclass(frozen=True, slots=True)
class LexicalSelectionCandidate:
    """اختيارٌ معجميٌّ لعنصرٍ في موضعه؛ مرجعٌ مُبصَّمٌ لا صورةٌ سطحيّة."""

    production_id: str
    specification_content_id: str
    element_id: str
    target: SyntacticRealizationTarget
    choice: LexicalChoiceRef

    def __post_init__(self) -> None:
        if not isinstance(self.choice, LexicalChoiceRef):
            raise GenerationCandidateError("الاختيارُ المعجميُّ مرجعٌ من نوعه")
        if not isinstance(self.target, SyntacticRealizationTarget):
            raise GenerationCandidateError("موضعُ التحقّق عضوٌ في مفردته المغلقة")
        if self.choice.element_id != self.element_id:
            raise GenerationCandidateError("اختيارُ عنصرٍ لا يُنسَب إلى عنصرٍ آخر")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المرحلة للبصمة."""

        return {
            "production_id": self.production_id,
            "specification_content_id": self.specification_content_id,
            "element_id": self.element_id,
            "target": self.target.value,
            "choice": self.choice.as_canonical_content(),
        }

    @property
    def content_id(self) -> str:
        """بصمةُ المرحلة."""

        return _content_id(self.as_canonical_content())


@dataclass(frozen=True, slots=True)
class WordFormCandidate:
    """صورةُ كلمةٍ مرشَّحة: جهةُ تحصيلها مُسمّاةٌ، ولا صورةَ بلا أثرٍ صرفيّ."""

    selection_content_id: str
    element_id: str
    target: SyntacticRealizationTarget
    lexical_form_ref: str
    morphological_operation_trace: tuple[MorphologicalOperation, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.morphological_operation_trace, tuple):
            raise GenerationCandidateError("الأثرُ الصرفيُّ مجموعةٌ مُصرَّحٌ بها")
        if not self.morphological_operation_trace:
            raise GenerationCandidateError(NO_WORD_FORM_WITHOUT_MORPHOLOGICAL_TRACE)
        for operation in self.morphological_operation_trace:
            if not isinstance(operation, MorphologicalOperation):
                raise GenerationCandidateError(
                    "عمليّةُ الأثر الصرفيّ عضوٌ في مفردتها المغلقة؛ و"
                    + NO_WORD_FORM_WITHOUT_MORPHOLOGICAL_TRACE
                )
        if (
            not isinstance(self.lexical_form_ref, str)
            or not self.lexical_form_ref.strip()
        ):
            raise GenerationCandidateError("مرجعُ الصورة المعجميّة نصٌّ غير فارغ")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المرحلة للبصمة."""

        return {
            "selection_content_id": self.selection_content_id,
            "element_id": self.element_id,
            "target": self.target.value,
            "lexical_form_ref": self.lexical_form_ref,
            "morphological_operation_trace": [
                operation.value for operation in self.morphological_operation_trace
            ],
        }

    @property
    def content_id(self) -> str:
        """بصمةُ المرحلة."""

        return _content_id(self.as_canonical_content())


@dataclass(frozen=True, slots=True)
class RelationSlotAssignment:
    """إسنادُ صورةٍ إلى موقعٍ في نسبةِ المصدر؛ ولا موقعَ بغير نسبةٍ تحمله."""

    word_form_content_id: str
    element_id: str
    target: SyntacticRealizationTarget
    source_nisbah_id: str
    source_execution_digest: str

    def __post_init__(self) -> None:
        for value, label in (
            (self.source_nisbah_id, "مُعرِّفُ نسبة المصدر"),
            (self.source_execution_digest, "بصمةُ تنفيذ المصدر"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise GenerationCandidateError(
                    f"{label} نصٌّ غير فارغ؛ و" + NO_COMPOSITION_WITHOUT_RELATION
                )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المرحلة للبصمة."""

        return {
            "word_form_content_id": self.word_form_content_id,
            "element_id": self.element_id,
            "target": self.target.value,
            "source_nisbah_id": self.source_nisbah_id,
            "source_execution_digest": self.source_execution_digest,
        }

    @property
    def content_id(self) -> str:
        """بصمةُ المرحلة."""

        return _content_id(self.as_canonical_content())


@dataclass(frozen=True, slots=True)
class CompositionCandidate:
    """تركيبٌ مرشَّح: مواقعُ العائلة بترتيب سطحها، مشدودةً إلى نسبةٍ واحدة."""

    specification_content_id: str
    source_nisbah_id: str
    assignments: tuple[RelationSlotAssignment, ...]
    surface_order: tuple[SyntacticRealizationTarget, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.assignments, tuple) or not self.assignments:
            raise GenerationCandidateError(NO_COMPOSITION_WITHOUT_RELATION)
        if tuple(item.target for item in self.assignments) != self.surface_order:
            raise GenerationCandidateError(
                "ترتيبُ التركيب ترتيبُ مواضع العائلة نفسُه لا ترتيبٌ يُختار"
            )
        for item in self.assignments:
            if item.source_nisbah_id != self.source_nisbah_id:
                raise GenerationCandidateError(
                    "مواقعُ تركيبٍ واحدٍ من نسبةٍ واحدة؛ و"
                    + NO_COMPOSITION_WITHOUT_RELATION
                )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المرحلة للبصمة."""

        return {
            "specification_content_id": self.specification_content_id,
            "source_nisbah_id": self.source_nisbah_id,
            "assignments": [item.as_canonical_content() for item in self.assignments],
            "surface_order": [target.value for target in self.surface_order],
        }

    @property
    def content_id(self) -> str:
        """بصمةُ المرحلة."""

        return _content_id(self.as_canonical_content())


@dataclass(frozen=True, slots=True)
class CaseEffectCandidate:
    """أثرُ الإعراب على مواقع التركيب؛ يتبع الموقعَ المرخَّص لا الصورةَ المختارة."""

    composition_content_id: str
    effects: Mapping[SyntacticRealizationTarget, CaseEffect]

    def __post_init__(self) -> None:
        if not isinstance(self.effects, Mapping) or not self.effects:
            raise GenerationCandidateError(NO_INFLECTION_WITHOUT_LICENSED_SLOT)
        for target, effect in self.effects.items():
            if not isinstance(target, SyntacticRealizationTarget):
                raise GenerationCandidateError(
                    "أثرُ الإعراب يتبع موضعًا مرخَّصًا؛ و"
                    + NO_INFLECTION_WITHOUT_LICENSED_SLOT
                )
            if not isinstance(effect, CaseEffect):
                raise GenerationCandidateError("أثرُ الإعراب عضوٌ في مفردته المغلقة")
        object.__setattr__(self, "effects", MappingProxyType(dict(self.effects)))

    def effect_for(self, target: SyntacticRealizationTarget) -> CaseEffect:
        """أثرُ موضعٍ واحد؛ ولا أثرَ يُستنتَج لموضعٍ لم يُسجَّل."""

        try:
            return self.effects[target]
        except KeyError as error:
            raise GenerationCandidateError(
                NO_INFLECTION_WITHOUT_LICENSED_SLOT
            ) from error

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المرحلة للبصمة."""

        return {
            "composition_content_id": self.composition_content_id,
            "effects": {
                target.value: effect.value for target, effect in self.effects.items()
            },
        }

    @property
    def content_id(self) -> str:
        """بصمةُ المرحلة."""

        return _content_id(self.as_canonical_content())


def _require_surface(value: object, label: str) -> str:
    """صورةٌ سطحيّةٌ فيها حرفٌ عربيٌّ واحدٌ على الأقلّ؛ فالسطحُ ليس مُعرِّفًا."""

    if not isinstance(value, str) or not value.strip():
        raise GenerationCandidateError(f"{label} نصٌّ غير فارغ")
    if not any("ARABIC" in unicodedata.name(character, "") for character in value):
        raise GenerationCandidateError(f"{label} صورةٌ عربيّةٌ لا مُعرِّفٌ لاتينيّ")
    return value


@dataclass(frozen=True, slots=True)
class SurfaceToken:
    """رمزٌ سطحيٌّ يُردّ إلى سبب إنتاجه: مصدرُه وموضعُه وأثرُه واختيارُه وحالتُه."""

    token_id: str
    surface: str
    source_element_id: str
    lexical_choice_id: str
    morphological_operation_trace: tuple[MorphologicalOperation, ...]
    syntactic_target: SyntacticRealizationTarget
    case_effect: CaseEffect
    generation_trace: GenerationTrace

    def __post_init__(self) -> None:
        for value, label in (
            (self.token_id, "مُعرِّفُ الرمز"),
            (self.source_element_id, "عنصرُ المصدر"),
            (self.lexical_choice_id, "مُعرِّفُ الاختيار المعجميّ"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise GenerationCandidateError(
                    f"{label} نصٌّ غير فارغ؛ و" + NO_SURFACE_WITHOUT_SOURCE_ANCHOR
                )
        _require_surface(self.surface, "صورةُ الرمز")
        if not isinstance(self.syntactic_target, SyntacticRealizationTarget):
            raise GenerationCandidateError(NO_INFLECTION_WITHOUT_LICENSED_SLOT)
        if not isinstance(self.case_effect, CaseEffect):
            raise GenerationCandidateError("أثرُ الإعراب عضوٌ في مفردته المغلقة")
        if not isinstance(self.generation_trace, GenerationTrace):
            raise GenerationCandidateError("أثرُ إنتاج الرمز من نوعه لا وصفٌ حرّ")
        if not isinstance(self.morphological_operation_trace, tuple) or not (
            self.morphological_operation_trace
        ):
            raise GenerationCandidateError(NO_WORD_FORM_WITHOUT_MORPHOLOGICAL_TRACE)
        for operation in self.morphological_operation_trace:
            if not isinstance(operation, MorphologicalOperation):
                raise GenerationCandidateError(NO_WORD_FORM_WITHOUT_MORPHOLOGICAL_TRACE)

    @property
    def residuals(self) -> tuple[GenerationResidual, ...]:
        """بقايا الرمز مرصودةً من أثره؛ ولا تُكتَب في حقلٍ بجانبه."""

        return self.generation_trace.residuals

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الرمز للبصمة."""

        return {
            "token_id": self.token_id,
            "surface": self.surface,
            "source_element_id": self.source_element_id,
            "lexical_choice_id": self.lexical_choice_id,
            "morphological_operation_trace": [
                operation.value for operation in self.morphological_operation_trace
            ],
            "syntactic_target": self.syntactic_target.value,
            "case_effect": self.case_effect.value,
            "generation_trace": self.generation_trace.as_canonical_content(),
        }

    @property
    def content_id(self) -> str:
        """بصمةُ الرمز."""

        return _content_id(self.as_canonical_content())


@dataclass(frozen=True, slots=True)
class OrthographicProjection:
    """إسقاطٌ كتابيّ: صورٌ مأخوذةٌ من مصدرٍ معجميٍّ مُجمَّد، لا مشتقّةٌ من صوتٍ لم يُقَس."""

    case_effect_content_id: str
    tokens: tuple[SurfaceToken, ...]
    orthographic_source: FormSelectionMode

    def __post_init__(self) -> None:
        if not isinstance(self.tokens, tuple) or not self.tokens:
            raise GenerationCandidateError("الإسقاطُ الكتابيُّ رمزٌ فأكثر")
        for token in self.tokens:
            if not isinstance(token, SurfaceToken):
                raise GenerationCandidateError(NO_SURFACE_WITHOUT_SOURCE_ANCHOR)
        if (
            self.orthographic_source
            is not FormSelectionMode.LEXICALLY_ATTESTED_FORM_SELECTION
        ):
            raise GenerationCandidateError(
                ORTHOGRAPHY_NEED_NOT_CLAIM_PHONOLOGICAL_DERIVATION
            )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المرحلة للبصمة."""

        return {
            "case_effect_content_id": self.case_effect_content_id,
            "tokens": [token.as_canonical_content() for token in self.tokens],
            "orthographic_source": self.orthographic_source.value,
        }

    @property
    def content_id(self) -> str:
        """بصمةُ المرحلة."""

        return _content_id(self.as_canonical_content())


def withheld_phonological_projection(
    *, case_effect_content_id: str, rule_id: str, subject_id: str
) -> WithheldStage:
    """الإسقاطُ الصوتيُّ محجوزٌ في `GEN-0`؛ وهذه هي صورتُه الوحيدةُ هنا."""

    residual = GenerationResidual(
        kind=GenerationResidualKind.UNMEASURED_PROSODIC_LAYER,
        stage=GenerationStage.PHONOLOGICAL_PROJECTION,
        subject_id=subject_id,
        reason=PHONOLOGICAL_PROJECTION_IS_WITHHELD_IN_GEN0,
    )
    step = GenerationStep(
        stage=GenerationStage.PHONOLOGICAL_PROJECTION,
        rule_id=rule_id,
        input_content_id=case_effect_content_id,
        output_content_id=None,
        residuals=(residual,),
    )
    return WithheldStage(
        stage=GenerationStage.PHONOLOGICAL_PROJECTION, step=step, residual=residual
    )


@dataclass(frozen=True, slots=True)
class GeneratedArabicUtterance:
    """عبارةٌ عربيّةٌ منتَجة: إسقاطُها الكتابيُّ نفسُه، ومواصفتُها، وأثرُها كاملًا.

    **ولا تُخزَّن هويّةٌ مُشتَقّةٌ دعوًى ثانية**
    (`DoNotStoreDerivableIdentityAsASecondClaim`): الرموزُ والبصمةُ الكتابيّةُ
    تُقرآن من `orthographic_projection` نفسِه، فلا يبقى موضعٌ لانحرافٍ بين
    `orthographic_content_id` و`Digest(tokens)` لأنّهما صارا شيئًا واحدًا.

    **واتّصالُ السلسلة شرطُ بناءٍ لا فحصُ بوّابة**: الأثرُ يبدأ من بصمة
    المواصفة، وينتهي بخطوةِ إسقاطٍ كتابيٍّ مخرجُها بصمةُ الإسقاط الذي تحمله
    العبارةُ بعينه. وما وراء ذلك — أنّ `surface` صورةُ مدخلةٍ معجميّةٍ مشهودة —
    فجوةُ سلطةٍ مُسمّاةٌ لا تُغلَق هنا.
    """

    production_id: str
    specification_content_id: str
    orthographic_projection: OrthographicProjection
    trace: GenerationTrace

    def __post_init__(self) -> None:
        if not isinstance(self.orthographic_projection, OrthographicProjection):
            raise GenerationCandidateError(
                "العبارةُ تحمل إسقاطَها الكتابيَّ نفسَه لا بصمتَه ورموزَه دعويين"
            )
        if not isinstance(self.trace, GenerationTrace):
            raise GenerationCandidateError("أثرُ العبارة من نوعه لا وصفٌ حرّ")
        elements = tuple(token.source_element_id for token in self.tokens)
        if len(set(elements)) != len(elements):
            raise GenerationCandidateError(
                "عنصرُ مصدرٍ واحدٌ لا يُخرِج رمزين في عبارةٍ واحدة"
            )
        if self.trace.input_content_id != self.specification_content_id:
            raise GenerationCandidateError(
                "أثرُ العبارة يبدأ من بصمة مواصفتها؛ و"
                + A_CHAIN_IS_READ_FROM_ITS_DIGESTS_NOT_ITS_ORDER
            )
        last = self.trace.steps[-1]
        if last.stage is not GenerationStage.ORTHOGRAPHIC_PROJECTION:
            raise GenerationCandidateError(
                "آخرُ خطوةٍ في أثر العبارة إسقاطٌ كتابيّ؛ وعبارةٌ تنتهي بغيره صورةٌ "
                "بلا مرحلةٍ أخرجتها"
            )
        if last.output_content_id != self.orthographic_projection.content_id:
            raise GenerationCandidateError(
                "مخرجُ آخرِ خطوةٍ هو بصمةُ إسقاط العبارة بعينها؛ و"
                + A_CHAIN_IS_READ_FROM_ITS_DIGESTS_NOT_ITS_ORDER
            )

    @property
    def tokens(self) -> tuple[SurfaceToken, ...]:
        """رموزُ العبارة مُشتَقّةً من إسقاطها الكتابيّ؛ ولا قائمةَ ثانيةً بجانبه."""

        return self.orthographic_projection.tokens

    @property
    def orthographic_content_id(self) -> str:
        """بصمةُ الإسقاط الكتابيِّ مُشتَقّةً منه؛ ولا تُكتَب دعوًى مستقلّة."""

        return self.orthographic_projection.content_id

    @property
    def surface(self) -> str:
        """الصورةُ السطحيّةُ مُشتَقّةً من رموزها؛ ولا نصَّ يُكتَب بجانبها."""

        return " ".join(token.surface for token in self.tokens)

    @property
    def residuals(self) -> tuple[GenerationResidual, ...]:
        """بقايا العبارة مرصودةً من أثرها."""

        return self.trace.residuals

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى العبارة للبصمة."""

        return {
            "production_id": self.production_id,
            "specification_content_id": self.specification_content_id,
            "orthographic_projection": (
                self.orthographic_projection.as_canonical_content()
            ),
            "trace": self.trace.as_canonical_content(),
        }

    @property
    def content_id(self) -> str:
        """بصمةُ العبارة."""

        return _content_id(self.as_canonical_content())


def specification_content_id(specification: ProductionSpecification) -> str:
    """بصمةُ مواصفةِ إنتاجٍ؛ مدخلُ أوّل خطوةٍ في السلسلة."""

    return _content_id(specification.as_canonical_content())
