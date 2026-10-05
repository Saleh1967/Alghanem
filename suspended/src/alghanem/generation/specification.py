"""مدخلُ الإنتاج: شهادةُ نجاحٍ سابقة، ثمّ مواصفةٌ رفيعةٌ لا تعيد كتابة النسبة.

    ExecutionPASS → PassedNisbahSourceRef → ProductionSpecification

**والمدخلُ ليس نصًّا، ولا بنيةً تُكتَب من جديد**: وجودُ `NisbahSignature` أو
`AnchoredNisbahSignatureV3` لا يثبت أنّه مرّ بالحكم التنفيذيّ المقصود، فلا
يُبنى الإنتاجُ إلّا على غلافِ نتيجةٍ ذي:

    Outcome = PASS  ∧  MaterializedIdentity ≠ ∅

وهذا لا يعني أنّ `generation` تُشغِّل المحرّك؛ بل تقرأ شهادةَ نجاحٍ سابقةً
وتُمسِك بها ببصماتها.

**ولا تكرارَ للبنية في المواصفة** (`NoGenerationAuthorityBeyondItsSource`): لا
`relation_kind` ولا `predicate_anchor` ولا `argument_anchors` تُكتَب هنا، لأنّها
في المصدر المرخَّص، وتكرارُها يفتح انحرافًا بين `SourceStructure` و
`ProductionSpecification` لا يُكشَف. وما في المواصفة إشاراتٌ إلى عناصر المصدر
بمُعرِّفاتها، تُتحقَّق عند التكوين من الغلاف نفسه.

**ولا رتبةَ ولا بقايا في المدخل** (`CallerDoesNotOwnGenerationRank`،
`ResidualsAreObservedNotAuthored`): الرتبةُ ناتجُ بوّابة، والبقايا رصدُ انتقالٍ
جرى؛ وكلاهما مُحرَّمٌ على صاحب المواصفة.

**وما لزم النوعَ لزمه في كلِّ طريقٍ إليه** (`ContractMustBindClassNotFactory`):
`PassedNisbahSourceRef` و`ProductionSpecification` كلتاهما مُغلَقةٌ برمز إصدارٍ
داخليّ، فلا تُبنى إحداهما بناءً مباشرًا يتجاوز فحصَ المصدر. وإشارةُ المصدر تحمل
**جردَ عناصره** — `SourceInventorySnapshot`: مُعرِّفُ المحمول ومُعرِّفاتُ المراسي
بأجناسها، ببصمةٍ مُشتَقّةٍ منها لا مكتوبةٍ بجانبها — فيُقاس عليه كلُّ مُعرِّفٍ في
المواصفة عند كلِّ بناءٍ لا عند المصنع وحدَه. والبصمةُ وحدَها لا تكفي: هي تُثبِت
هويّةَ الجرد ولا تُخبِر بما فيه، فيُحمَل الجردُ نفسُه إسقاطًا مشهودًا للمصدر.

**والموقعُ التركيبيُّ ليس دورًا دلاليًّا** (`APositionIsNotASemanticRole`): لا
يُفتَح هنا `Agent` ولا `Patient`، ولا تُعدَّل `linguistic/nisbah.py` لفتحهما.
وإنّما تقول المواصفة: هذه المرساةُ ستتحقّق في هذا **الموقع** ضمن عائلة
`GEN-0`، لا أنّ هذه المرساة **هي** فاعلٌ في الوجود.

**وموضعُ المحمول ثالثٌ لازم**: لو اقتصرت المواقعُ على الفاعل والمفعول لخرج
الفعلُ نفسُه رمزًا سطحيًّا بلا موقعٍ مرخَّص، وذلك نقضُ
`NoInflectionWithoutLicensedSlot` و`NoSurfaceWithoutSourceAnchor`. فـ
`PREDICATE_POSITION` موضعُ تحقّقِ محمولِ المصدر، وليس دورًا ولا حجّةً، ولا أثرَ
إعرابٍ له في هذه العائلة.

تسجيلٌ لا سلطة: لا ولادةَ، ولا حكمَ ولادةٍ، ولا تجميدَ `E0`.
"""

from __future__ import annotations

import unicodedata
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from ..execution.outcome import ExecutionOutcome
from ..execution.result import ExecutionResultEnvelope
from .laws import (
    A_POSITION_IS_NOT_A_SEMANTIC_ROLE,
    CONTRACT_MUST_BIND_CLASS_NOT_FACTORY,
    GENERATION_DOES_NOT_INVENT_INTENT,
    LEXICAL_CHOICE_REF_IS_A_CLAIM_UNTIL_THE_READOUT,
    NO_GENERATION_AUTHORITY_BEYOND_ITS_SOURCE,
    NO_LEXEME_OUTSIDE_A_FROZEN_LEXICAL_SOURCE,
    NO_WORD_FORM_WITHOUT_MORPHOLOGICAL_TRACE,
)

__all__ = [
    "CaseEffect",
    "FormSelectionMode",
    "GenerationSpecificationError",
    "LexicalChoiceRef",
    "PAST_ACTIVE_TRANSITIVE_VSO",
    "PassedNisbahSourceRef",
    "ProductionFamily",
    "ProductionFamilySpec",
    "ProductionSpecification",
    "RealizationConstraint",
    "RealizationConstraintKind",
    "RealizationConstraintValue",
    "RealizationTargetAssignment",
    "RequestedSentenceForm",
    "RequestedTense",
    "RequestedVoice",
    "SourceElementKind",
    "SourceElementRef",
    "SourceInventorySnapshot",
    "SyntacticRealizationTarget",
]


class GenerationSpecificationError(ValueError):
    """رفضٌ عند تكوين مواصفةِ إنتاج؛ ولا حملَ على أقرب صورةٍ مقبولة."""


class _IssuanceToken:
    """رمزُ إصدارٍ داخليّ؛ وجودُه بيد هذه الوحدة لا بيد المستدعي."""

    __slots__ = ()


_SOURCE_REF_ISSUANCE: Final[_IssuanceToken] = _IssuanceToken()
_SPECIFICATION_ISSUANCE: Final[_IssuanceToken] = _IssuanceToken()


def _require_identifier(value: object, label: str) -> str:
    """مُعرِّفٌ نصّيٌّ غيرُ فارغٍ ولا يحمل حرفًا عربيًّا؛ فالمُعرِّف ليس لفظًا."""

    if not isinstance(value, str) or not value.strip():
        raise GenerationSpecificationError(f"{label} نصٌّ غير فارغ")
    for character in value:
        if "ARABIC" in unicodedata.name(character, ""):
            raise GenerationSpecificationError(
                f"{label} لا يحمل صورةً عربيّةً سطحيّة؛ و"
                + GENERATION_DOES_NOT_INVENT_INTENT
            )
    return value


class SourceElementKind(Enum):
    """جنسُ عنصرِ المصدر المُشار إليه؛ محمولٌ أو مرساةُ طرف، لا ثالثَ لهما هنا."""

    PREDICATE = "predicate"
    ANCHOR = "anchor"


class SyntacticRealizationTarget(Enum):
    """موضعُ التحقّق النحويّ؛ موضعٌ يُشغَل لا دورٌ يُنسَب."""

    PREDICATE_POSITION = "predicate_position"
    FAA_IL_POSITION = "faa_il_position"
    MAF_UL_BIH_POSITION = "maf_ul_bih_position"


class CaseEffect(Enum):
    """أثرُ الإعراب على الموضع؛ و«لا أثرَ في هذه العائلة» عضوٌ مُصرَّحٌ به لا صمت."""

    RAF = "raf"
    NASB = "nasb"
    NO_EFFECT_IN_THIS_FAMILY = "no_effect_in_this_family"


class RequestedTense(Enum):
    """الزمنُ المطلوب؛ ولا يُعلَن زمنٌ لم تُفتَح له عائلةٌ إنتاجيّة."""

    PAST = "past"
    UNDETERMINED = "undetermined"


class RequestedVoice(Enum):
    """البناءُ المطلوب؛ والمجهولُ غيرُ مفتوحٍ في `GEN-0` فلا يُسمّى عضوًا."""

    ACTIVE = "active"
    UNDETERMINED = "undetermined"


class RequestedSentenceForm(Enum):
    """صورةُ الجملة المطلوبة؛ فعليّةٌ بترتيب `VSO` وحدها في `GEN-0`."""

    VERBAL_VSO = "verbal_vso"
    UNDETERMINED = "undetermined"


class ProductionFamily(Enum):
    """العائلةُ الإنتاجيّة؛ واحدةٌ مفتوحةٌ في `GEN-0` لا غير."""

    PAST_ACTIVE_TRANSITIVE_VSO = "past_active_transitive_vso"


class FormSelectionMode(Enum):
    """جهةُ تحصيل صورة الكلمة؛ والاشتقاقُ مُسمًّى لأنّه مرفوضٌ لا لأنّه متاح."""

    LEXICALLY_ATTESTED_FORM_SELECTION = "lexically_attested_form_selection"
    DERIVED_FROM_ROOT = "derived_from_root"


class RealizationConstraintKind(Enum):
    """جنسُ قيدِ التحقّق؛ مفردةٌ مغلقةٌ لا نصٌّ حرّ."""

    DEFINITENESS = "definiteness"
    NUMBER = "number"
    EXPRESSION = "expression"


class RealizationConstraintValue(Enum):
    """قيمةُ قيدِ التحقّق؛ مفردةٌ مغلقةٌ تُقابَل بجنسها."""

    DEFINITE = "definite"
    INDEFINITE = "indefinite"
    SINGULAR = "singular"
    EXPLICIT_NOT_PRONOMINAL = "explicit_not_pronominal"


_LICENSED_CONSTRAINT_PAIRS: Final[
    Mapping[RealizationConstraintKind, frozenset[str]]
] = MappingProxyType(
    {
        RealizationConstraintKind.DEFINITENESS: frozenset(
            {
                RealizationConstraintValue.DEFINITE.value,
                RealizationConstraintValue.INDEFINITE.value,
            }
        ),
        RealizationConstraintKind.NUMBER: frozenset(
            {RealizationConstraintValue.SINGULAR.value}
        ),
        RealizationConstraintKind.EXPRESSION: frozenset(
            {RealizationConstraintValue.EXPLICIT_NOT_PRONOMINAL.value}
        ),
    }
)


@dataclass(frozen=True, slots=True)
class SourceElementRef:
    """عنصرٌ في المصدر المرخَّص: مُعرِّفُه وجنسُه، لا إعادةُ وصفٍ له."""

    element_id: str
    element_kind: SourceElementKind

    def __post_init__(self) -> None:
        _require_identifier(self.element_id, "مُعرِّفُ عنصر المصدر")
        if not isinstance(self.element_kind, SourceElementKind):
            raise GenerationSpecificationError("جنسُ عنصر المصدر عضوٌ في مفردته المغلقة")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى العنصر للبصمة."""

        return {
            "element_id": self.element_id,
            "element_kind": self.element_kind.value,
        }


@dataclass(frozen=True, slots=True)
class SourceInventorySnapshot:
    """إسقاطٌ مشهودٌ لجرد المصدر: عناصرُه بأجناسها، وبصمتُه مُشتَقّةٌ منها.

    وهو `CertifiedProjectionOfSource` لا إعادةَ كتابةٍ حرّةٍ للنسبة: لا يحمل
    نسبةً ولا محمولًا ولا حجّةً، وإنّما جردَ المُعرِّفات التي يُقاس عليها كلُّ
    مُعرِّفٍ في المواصفة. والبصمةُ وحدَها لا تكفي لإعادة الفحص لاحقًا — فهي
    تُثبِت هويّةَ الجرد ولا تُخبِر بما فيه — ولذلك يُحمَل الجردُ نفسُه.
    """

    elements: tuple[SourceElementRef, ...]
    issuance: _IssuanceToken

    def __post_init__(self) -> None:
        if self.issuance is not _SOURCE_REF_ISSUANCE:
            raise GenerationSpecificationError(
                "جردُ المصدر لا يُنشَأ إلّا من غلافِ نتيجةٍ ناجحة؛ و"
                + CONTRACT_MUST_BIND_CLASS_NOT_FACTORY
            )
        if not isinstance(self.elements, tuple) or not self.elements:
            raise GenerationSpecificationError(
                "جردُ عناصر المصدر عنصرٌ فأكثر؛ ومصدرٌ بلا جردٍ لا يُقاس عليه"
            )
        identifiers = []
        predicates = 0
        for element in self.elements:
            if not isinstance(element, SourceElementRef):
                raise GenerationSpecificationError("عنصرُ الجرد من نوعه لا وصفٌ حرّ")
            identifiers.append(element.element_id)
            if element.element_kind is SourceElementKind.PREDICATE:
                predicates += 1
        if len(set(identifiers)) != len(identifiers):
            raise GenerationSpecificationError("مُعرِّفُ عنصرٍ واحدٌ لا يتكرّر في جردٍ واحد")
        if predicates != 1:
            raise GenerationSpecificationError(
                "النسبةُ محمولٌ واحدٌ ومراسٍ؛ وجردٌ بمحمولين أو بلا محمولٍ ليس جردَها"
            )

    def kind_of(self, element_id: str) -> SourceElementKind | None:
        """جنسُ عنصرٍ في الجرد، أو غيابُه؛ ولا يُستنتَج جنسٌ لعنصرٍ لم يحمله."""

        for element in self.elements:
            if element.element_id == element_id:
                return element.element_kind
        return None

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الجرد للبصمة؛ ورمزُ الإصدار سلطةٌ لا محتوى."""

        return {
            "elements": [
                element.as_canonical_content()
                for element in sorted(self.elements, key=lambda ref: ref.element_id)
            ]
        }

    @property
    def content_id(self) -> str:
        """بصمةُ الجرد مُشتَقّةً من عناصره."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


@dataclass(frozen=True, slots=True)
class PassedNisbahSourceRef:
    """إشارةٌ رفيعةٌ إلى بنيةٍ نجحت: مُعرِّفُها وبصماتُها وجردُ عناصرها، لا نسخةٌ منها.

    ولا تُبنى إلّا من `from_envelope`؛ فرمزُ الإصدار بيد الوحدة لا بيد المستدعي،
    وقد كان الفحصُ في مصنعٍ وحدَه شرطًا اختياريًّا يُتجاوَز بالبناء المباشر —
    و`ContractMustBindClassNotFactory` يُبطِل ذلك.
    """

    nisbah_id: str
    materialized_content_id: str
    source_inventory: SourceInventorySnapshot
    input_digest: str
    execution_digest: str
    law_set_digest: str
    issuance: _IssuanceToken

    def __post_init__(self) -> None:
        if self.issuance is not _SOURCE_REF_ISSUANCE:
            raise GenerationSpecificationError(
                "إشارةُ المصدر لا تُنشَأ إلّا من غلافِ نتيجةٍ ناجحة؛ و"
                + CONTRACT_MUST_BIND_CLASS_NOT_FACTORY
            )
        for value, label in (
            (self.nisbah_id, "مُعرِّفُ النسبة المصدر"),
            (self.materialized_content_id, "بصمةُ المادّة السلطويّة"),
            (self.input_digest, "بصمةُ الإدخال"),
            (self.execution_digest, "بصمةُ التنفيذ"),
            (self.law_set_digest, "بصمةُ قائمة القوانين"),
        ):
            _require_identifier(value, label)
        if not isinstance(self.source_inventory, SourceInventorySnapshot):
            raise GenerationSpecificationError(
                "جردُ المصدر إسقاطٌ مشهودٌ من نوعه لا خريطةٌ تُكتَب بجانب الإشارة"
            )

    @classmethod
    def from_envelope(cls, envelope: ExecutionResultEnvelope) -> PassedNisbahSourceRef:
        """اقرأ شهادةَ نجاحٍ سابقةً؛ ولا تُنشَأ هذه الإشارةُ من غير غلافٍ ناجح."""

        if not isinstance(envelope, ExecutionResultEnvelope):
            raise GenerationSpecificationError(
                "مصدرُ الإنتاج غلافُ نتيجةٍ من نوعه لا وصفٌ حرّ؛ و"
                + NO_GENERATION_AUTHORITY_BEYOND_ITS_SOURCE
            )
        core = envelope.core
        if core.outcome is not ExecutionOutcome.PASS:
            raise GenerationSpecificationError(
                "لا إنتاجَ إلّا من نتيجةٍ حكمُها نجاح؛ و"
                + NO_GENERATION_AUTHORITY_BEYOND_ITS_SOURCE
            )
        materialized = core.materialized_identity
        if materialized is None:
            raise GenerationSpecificationError(
                "النجاحُ يبلغ المادّةَ السلطويّة؛ ونجاحٌ بلا هويّةٍ مُتحقِّقةٍ لا يُبنى عليه"
            )
        nisbah = envelope.declaration.nisbah
        elements = (
            SourceElementRef(
                element_id=nisbah.predicate.predicate_id,
                element_kind=SourceElementKind.PREDICATE,
            ),
            *(
                SourceElementRef(
                    element_id=anchor.anchor_id,
                    element_kind=SourceElementKind.ANCHOR,
                )
                for anchor in nisbah.anchors
            ),
        )
        return cls(
            nisbah_id=nisbah.nisbah_id,
            materialized_content_id=materialized.content_id,
            source_inventory=SourceInventorySnapshot(
                elements=elements, issuance=_SOURCE_REF_ISSUANCE
            ),
            input_digest=core.input_digest,
            execution_digest=envelope.execution_digest,
            law_set_digest=core.law_set_digest,
            issuance=_SOURCE_REF_ISSUANCE,
        )

    def kind_of(self, element_id: str) -> SourceElementKind | None:
        """جنسُ عنصرٍ في المصدر، أو غيابُه؛ ولا يُستنتَج جنسٌ لعنصرٍ لم يحمله."""

        return self.source_inventory.kind_of(element_id)

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الإشارة للبصمة؛ ورمزُ الإصدار سلطةٌ لا محتوى."""

        return {
            "nisbah_id": self.nisbah_id,
            "materialized_content_id": self.materialized_content_id,
            "input_digest": self.input_digest,
            "execution_digest": self.execution_digest,
            "law_set_digest": self.law_set_digest,
            "source_inventory": self.source_inventory.as_canonical_content(),
            "source_inventory_content_id": self.source_inventory.content_id,
        }


@dataclass(frozen=True, slots=True)
class RealizationTargetAssignment:
    """عنصرُ مصدرٍ يتحقّق في موضع؛ إشارةٌ إلى المصدر لا إعادةُ وصفٍ له."""

    element_kind: SourceElementKind
    element_id: str
    target: SyntacticRealizationTarget

    def __post_init__(self) -> None:
        if not isinstance(self.element_kind, SourceElementKind):
            raise GenerationSpecificationError("جنسُ عنصر المصدر عضوٌ في مفردته المغلقة")
        if not isinstance(self.target, SyntacticRealizationTarget):
            raise GenerationSpecificationError("موضعُ التحقّق عضوٌ في مفردته المغلقة")
        _require_identifier(self.element_id, "مُعرِّفُ عنصر المصدر")
        predicate_site = self.target is SyntacticRealizationTarget.PREDICATE_POSITION
        if predicate_site != (self.element_kind is SourceElementKind.PREDICATE):
            raise GenerationSpecificationError(
                "موضعُ المحمول للمحمول وحدَه، وموضعا الحجّتين للمراسي وحدَها؛ و"
                + A_POSITION_IS_NOT_A_SEMANTIC_ROLE
            )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الإسناد للبصمة."""

        return {
            "element_kind": self.element_kind.value,
            "element_id": self.element_id,
            "target": self.target.value,
        }


@dataclass(frozen=True, slots=True)
class LexicalChoiceRef:
    """اختيارٌ معجميّ: مرجعٌ مُبصَّمٌ إلى مدخلةٍ مُجمَّدة، لا صورةٌ سطحيّةٌ تُكتَب.

    وهو **دعوى** في `SPEC` لا شهادة (`LexicalChoiceRefIsAClaimUntilTheReadout`):
    لا معجمَ مُجمَّدًا هنا يُطابَق به `entry_id` ولا `entry_content_id` ولا
    `lexical_source_digest`، ولا سلطةَ تُثبِت أنّ صورةَ الرمز هي صورةُ هذه
    المدخلة؛ وذلك مؤجَّلٌ إلى `GEN-0.DATA` ثمّ `GEN-0.READOUT`.
    """

    choice_id: str
    element_id: str
    entry_id: str
    entry_content_id: str
    lexical_source_id: str
    lexical_source_digest: str
    form_selection_mode: FormSelectionMode

    def __post_init__(self) -> None:
        for value, label in (
            (self.choice_id, "مُعرِّفُ الاختيار"),
            (self.element_id, "مُعرِّفُ عنصر المصدر"),
            (self.entry_id, "مُعرِّفُ المدخلة المعجميّة"),
            (self.entry_content_id, "بصمةُ المدخلة المعجميّة"),
            (self.lexical_source_id, "مُعرِّفُ المصدر المعجميّ"),
            (self.lexical_source_digest, "بصمةُ المصدر المعجميّ"),
        ):
            _require_identifier(value, label)
        if not isinstance(self.form_selection_mode, FormSelectionMode):
            raise GenerationSpecificationError(
                "جهةُ تحصيل الصيغة عضوٌ في مفردتها المغلقة؛ و"
                + NO_WORD_FORM_WITHOUT_MORPHOLOGICAL_TRACE
            )
        if self.form_selection_mode is FormSelectionMode.DERIVED_FROM_ROOT:
            raise GenerationSpecificationError(
                "الاشتقاقُ من الجذر مؤجَّلٌ إلى `GEN-MORPH-1`: صيغةُ `GEN-0` صورةٌ "
                "معجميّةٌ مشهودةٌ مختارة، وادّعاءُ الاشتقاق يزعم إغلاقَ الوزن قبل قياسه؛ و"
                + NO_LEXEME_OUTSIDE_A_FROZEN_LEXICAL_SOURCE
            )

    @property
    def is_a_claim_until_the_readout(self) -> str:
        """هذا المرجعُ دعوى لا شهادة؛ ونصُّ ذلك مقروءٌ من النوع نفسه."""

        return LEXICAL_CHOICE_REF_IS_A_CLAIM_UNTIL_THE_READOUT

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الاختيار للبصمة."""

        return {
            "choice_id": self.choice_id,
            "element_id": self.element_id,
            "entry_id": self.entry_id,
            "entry_content_id": self.entry_content_id,
            "lexical_source_id": self.lexical_source_id,
            "lexical_source_digest": self.lexical_source_digest,
            "form_selection_mode": self.form_selection_mode.value,
        }


@dataclass(frozen=True, slots=True)
class RealizationConstraint:
    """قيدُ تحقّقٍ على عنصرٍ واحد؛ جنسٌ وقيمةٌ من مفردتين متقابلتين."""

    element_id: str
    kind: RealizationConstraintKind
    value: RealizationConstraintValue

    def __post_init__(self) -> None:
        _require_identifier(self.element_id, "مُعرِّفُ عنصر المصدر")
        if not isinstance(self.kind, RealizationConstraintKind):
            raise GenerationSpecificationError("جنسُ القيد عضوٌ في مفردته المغلقة")
        if not isinstance(self.value, RealizationConstraintValue):
            raise GenerationSpecificationError("قيمةُ القيد عضوٌ في مفردتها المغلقة")
        if self.value.value not in _LICENSED_CONSTRAINT_PAIRS[self.kind]:
            raise GenerationSpecificationError(
                "قيمةُ القيد لا تقع تحت جنسه؛ والاقترانُ مُصرَّحٌ به لا مُستنتَج"
            )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى القيد للبصمة."""

        return {
            "element_id": self.element_id,
            "kind": self.kind.value,
            "value": self.value.value,
        }


@dataclass(frozen=True, slots=True)
class ProductionFamilySpec:
    """حدودُ العائلة الإنتاجيّة: ما يلزمها، وترتيبُ سطحها، وما خرج عنها بسببه."""

    family: ProductionFamily
    required_tense: RequestedTense
    required_voice: RequestedVoice
    required_sentence_form: RequestedSentenceForm
    surface_order: tuple[SyntacticRealizationTarget, ...]
    licensed_case_effect: Mapping[SyntacticRealizationTarget, CaseEffect]
    excluded_features: Mapping[str, str]

    def case_effect_for(self, target: SyntacticRealizationTarget) -> CaseEffect:
        """أثرُ الإعراب لموضعٍ في هذه العائلة؛ ولا موضعَ بلا أثرٍ مُسمًّى."""

        try:
            return self.licensed_case_effect[target]
        except KeyError as error:  # pragma: no cover - المواضعُ مُغلقةٌ بالعائلة
            raise GenerationSpecificationError(
                "موضعٌ خارج العائلة لا أثرَ إعرابٍ له"
            ) from error

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى العائلة للبصمة."""

        return {
            "family": self.family.value,
            "required_tense": self.required_tense.value,
            "required_voice": self.required_voice.value,
            "required_sentence_form": self.required_sentence_form.value,
            "surface_order": [target.value for target in self.surface_order],
            "licensed_case_effect": {
                target.value: effect.value
                for target, effect in self.licensed_case_effect.items()
            },
            "excluded_features": dict(self.excluded_features),
        }


PAST_ACTIVE_TRANSITIVE_VSO: Final[ProductionFamilySpec] = ProductionFamilySpec(
    family=ProductionFamily.PAST_ACTIVE_TRANSITIVE_VSO,
    required_tense=RequestedTense.PAST,
    required_voice=RequestedVoice.ACTIVE,
    required_sentence_form=RequestedSentenceForm.VERBAL_VSO,
    surface_order=(
        SyntacticRealizationTarget.PREDICATE_POSITION,
        SyntacticRealizationTarget.FAA_IL_POSITION,
        SyntacticRealizationTarget.MAF_UL_BIH_POSITION,
    ),
    licensed_case_effect=MappingProxyType(
        {
            SyntacticRealizationTarget.PREDICATE_POSITION: (
                CaseEffect.NO_EFFECT_IN_THIS_FAMILY
            ),
            SyntacticRealizationTarget.FAA_IL_POSITION: CaseEffect.RAF,
            SyntacticRealizationTarget.MAF_UL_BIH_POSITION: CaseEffect.NASB,
        }
    ),
    excluded_features=MappingProxyType(
        {
            "passive_voice": "المبنيُّ للمجهول يُغيِّر إسنادَ الموضعين، ولم تُفتَح عائلتُه",
            "augmented_verb": "المزيدُ يقتضي أثرًا صرفيًّا لم يُقَس في هذه المرحلة",
            "root_derivation": "الاشتقاقُ من الجذر مؤجَّلٌ إلى `GEN-MORPH-1` بنصّه",
            "pronominal_argument": (
                "الضميرُ المستترُ والمتّصلُ يحملان مسألةَ الحمل والحذف معًا"
            ),
            "ellipsis": "الحذفُ يُنتِج موضعًا بلا رمزٍ سطحيٍّ يُردّ إليه",
            "fronting": "التقديمُ والتأخيرُ ترتيبٌ ثانٍ يلزمه قيدُ إفادةٍ لم يُقرَّر",
            "dual_or_plural": "المثنّى والجمعُ صورتان معجميّتان زائدتان على المجمَّد",
            "nominal_sentence": "الجملةُ الاسميّةُ نسبةٌ بلا محمولٍ فعليٍّ في السطح",
            "prepositional_complement": "الجارُّ والمجرورُ موضعٌ رابعٌ خارج الثلاثة",
            "phonological_realization": (
                "الطبقةُ الصوتيّةُ محجوزةٌ لأنّ المقطعَ والوزنَ لم يُقاسا"
            ),
        }
    ),
)


@dataclass(frozen=True, slots=True)
class ProductionSpecification:
    """مواصفةُ إنتاج: إشارةٌ إلى مصدرٍ ناجح، ومواضعُ، واختياراتٌ، وقيود.

    ولا تحمل رتبةً ولا بقايا ولا نصًّا سطحيًّا، ولا تعيد كتابةَ نسبةِ المصدر.

    **وكلُّ فحصٍ يلزم النوعَ لا المصنع** (`ContractMustBindClassNotFactory`):
    وجودُ العنصر في جرد المصدر وجنسُه يُفحَصان في `__post_init__` نفسِه، لا في
    `for_passed_execution` وحدَه، فلا يبلغ البناءُ المباشرُ ولا `replace` ما
    يتجاوز المصدر. ورمزُ الإصدار يجعل المصنعَ الطريقَ الوحيد.
    """

    production_id: str
    source_ref: PassedNisbahSourceRef
    production_family: ProductionFamilySpec
    requested_tense: RequestedTense
    requested_voice: RequestedVoice
    requested_sentence_form: RequestedSentenceForm
    realization_targets: tuple[RealizationTargetAssignment, ...]
    lexical_choice_refs: tuple[LexicalChoiceRef, ...]
    realization_constraints: tuple[RealizationConstraint, ...]
    issuance: _IssuanceToken

    def __post_init__(self) -> None:
        if self.issuance is not _SPECIFICATION_ISSUANCE:
            raise GenerationSpecificationError(
                "المواصفةُ لا تُبنى إلّا من غلافٍ ناجحٍ عبر `for_passed_execution`؛ و"
                + CONTRACT_MUST_BIND_CLASS_NOT_FACTORY
            )
        _require_identifier(self.production_id, "مُعرِّفُ الإنتاج")
        if not isinstance(self.source_ref, PassedNisbahSourceRef):
            raise GenerationSpecificationError(
                "مصدرُ المواصفة إشارةٌ إلى نتيجةٍ ناجحةٍ من نوعها؛ و"
                + NO_GENERATION_AUTHORITY_BEYOND_ITS_SOURCE
            )
        if not isinstance(self.production_family, ProductionFamilySpec):
            raise GenerationSpecificationError("العائلةُ الإنتاجيّةُ حدٌّ مُجمَّدٌ من نوعه")
        family = self.production_family
        if (
            self.requested_tense is not family.required_tense
            or self.requested_voice is not family.required_voice
            or self.requested_sentence_form is not family.required_sentence_form
        ):
            raise GenerationSpecificationError(
                "المطلوبُ خارج حدود العائلة المفتوحة؛ وعضوُ الجهل مُصرَّحٌ به لا مقبول"
            )
        for value, label in (
            (self.realization_targets, "مواضعُ التحقّق"),
            (self.lexical_choice_refs, "الاختياراتُ المعجميّة"),
            (self.realization_constraints, "قيودُ التحقّق"),
        ):
            if not isinstance(value, tuple):
                raise GenerationSpecificationError(f"{label} مجموعةٌ مُصرَّحٌ بها")
        for assignment in self.realization_targets:
            if not isinstance(assignment, RealizationTargetAssignment):
                raise GenerationSpecificationError("موضعُ التحقّق إسنادٌ من نوعه")
        targets = tuple(assignment.target for assignment in self.realization_targets)
        if targets != family.surface_order:
            raise GenerationSpecificationError(
                "مواضعُ العائلةِ كلُّها مشغولةٌ مرّةً واحدةً وبترتيب سطحها؛ "
                "فلا موضعَ يتكرّر ولا موضعَ يغيب"
            )
        elements = tuple(
            assignment.element_id for assignment in self.realization_targets
        )
        if len(set(elements)) != len(elements):
            raise GenerationSpecificationError(
                "عنصرُ مصدرٍ واحدٌ لا يتحقّق في موضعين؛ والمواضعُ مُتباينةٌ بعناصرها"
            )
        self._refuse_every_element_outside_its_source()
        choices = tuple(choice.element_id for choice in self.lexical_choice_refs)
        if len(set(choices)) != len(choices) or set(choices) != set(elements):
            raise GenerationSpecificationError(
                "لكلّ عنصرٍ متحقّقٍ اختيارٌ معجميٌّ واحد؛ ولا اختيارَ لعنصرٍ بلا موضع؛ و"
                + NO_LEXEME_OUTSIDE_A_FROZEN_LEXICAL_SOURCE
            )
        for constraint in self.realization_constraints:
            if constraint.element_id not in set(elements):
                raise GenerationSpecificationError(
                    "قيدُ التحقّق على عنصرٍ من عناصر المصدر المتحقّقة لا على غيرها"
                )
        seen_constraints = tuple(
            (constraint.element_id, constraint.kind)
            for constraint in self.realization_constraints
        )
        if len(set(seen_constraints)) != len(seen_constraints):
            raise GenerationSpecificationError(
                "جنسُ قيدٍ واحدٍ لا يتكرّر على عنصرٍ واحدٍ بقيمتين"
            )

    def _refuse_every_element_outside_its_source(self) -> None:
        """كلُّ مُعرِّفِ عنصرٍ في المواصفة مقروءٌ من جرد المصدر لا مكتوبٌ فيها."""

        source = self.source_ref
        referenced: tuple[tuple[str, SourceElementKind | None], ...] = (
            tuple(
                (assignment.element_id, assignment.element_kind)
                for assignment in self.realization_targets
            )
            + tuple((choice.element_id, None) for choice in self.lexical_choice_refs)
            + tuple(
                (constraint.element_id, None)
                for constraint in self.realization_constraints
            )
        )
        for element_id, declared_kind in referenced:
            kind = source.kind_of(element_id)
            if kind is None:
                raise GenerationSpecificationError(
                    "لا يتحقّق عنصرٌ لا يحمله المصدرُ المرخَّص؛ و"
                    + NO_GENERATION_AUTHORITY_BEYOND_ITS_SOURCE
                )
            if declared_kind is not None and kind is not declared_kind:
                raise GenerationSpecificationError(
                    "جنسُ العنصر يُقرَأ من المصدر لا يُعلَن في المواصفة"
                )

    @classmethod
    def for_passed_execution(
        cls,
        *,
        envelope: ExecutionResultEnvelope,
        production_id: str,
        production_family: ProductionFamilySpec,
        requested_tense: RequestedTense,
        requested_voice: RequestedVoice,
        requested_sentence_form: RequestedSentenceForm,
        realization_targets: tuple[RealizationTargetAssignment, ...],
        lexical_choice_refs: tuple[LexicalChoiceRef, ...],
        realization_constraints: tuple[RealizationConstraint, ...],
    ) -> ProductionSpecification:
        """كوِّن مواصفةً من غلافٍ ناجح؛ والفحصُ في النوع نفسِه لا في هذا الطريق."""

        return cls(
            production_id=production_id,
            source_ref=PassedNisbahSourceRef.from_envelope(envelope),
            production_family=production_family,
            requested_tense=requested_tense,
            requested_voice=requested_voice,
            requested_sentence_form=requested_sentence_form,
            realization_targets=realization_targets,
            lexical_choice_refs=lexical_choice_refs,
            realization_constraints=realization_constraints,
            issuance=_SPECIFICATION_ISSUANCE,
        )

    def target_of(self, element_id: str) -> SyntacticRealizationTarget:
        """موضعُ عنصرٍ من عناصر المصدر؛ ولا موضعَ يُستنتَج لعنصرٍ لم يُسنَد."""

        for assignment in self.realization_targets:
            if assignment.element_id == element_id:
                return assignment.target
        raise GenerationSpecificationError("عنصرٌ بلا موضعِ تحقّقٍ مُسنَدٍ في هذه المواصفة")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المواصفة للبصمة؛ ولا رتبةَ فيها ولا بقايا."""

        return {
            "production_id": self.production_id,
            "source_ref": self.source_ref.as_canonical_content(),
            "production_family": self.production_family.as_canonical_content(),
            "requested_tense": self.requested_tense.value,
            "requested_voice": self.requested_voice.value,
            "requested_sentence_form": self.requested_sentence_form.value,
            "realization_targets": [
                assignment.as_canonical_content()
                for assignment in self.realization_targets
            ],
            "lexical_choice_refs": [
                choice.as_canonical_content() for choice in self.lexical_choice_refs
            ],
            "realization_constraints": [
                constraint.as_canonical_content()
                for constraint in self.realization_constraints
            ],
        }
