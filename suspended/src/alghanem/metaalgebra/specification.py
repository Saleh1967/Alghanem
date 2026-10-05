"""`Σ_A` — نظريّةٌ معيّنةٌ مكتوبةٌ بلغة `Σ_M`، مبصومةٌ بمحتواها.

    Σ_M  →  Σ_A  →  { R_Python(Σ_A), R_Arabic(Σ_A) }

فهذه الوحدةُ تحمل **طبقاتٍ وانتقالاتٍ بعينها**، بخلاف `schema` التي تحمل معنى
الطبقةِ والانتقال ولا تحمل واحدًا منهما. و`CompositionChain` عضوٌ **داخل**
المواصفة لا بديلٌ عنها (`A_CHAIN_IS_NOT_A_SPECIFICATION`): السلسلةُ مسارٌ في
النظريّة، والنظريّةُ قد تحمل طبقاتٍ لا تقع على مسارٍ واحد.

**والمواصفةُ مبنيّةٌ على بصمةِ لغتها:** نظريّةٌ تشير إلى بصمةِ `Σ_M` غيرِ
القائمة نظريّةٌ بلغةٍ أخرى، وتُرفَض عند الإنشاء لا تُقرَأ بالتسامح.

**وبصمةُ `Σ_A` لا تشمل تحقيقاتِها:** تغيّرُ تحقيقٍ لا يغيّر النظريّة، وهذا هو
الشاهدُ البنيويُّ على أنّ `Σ_A` أصلٌ لا مُشتَقّ من أحد تمثيليها
(`SIGMA_IS_THE_ORIGIN_NOT_ITS_REALIZATIONS` في `realization`).

تسجيلٌ لا سلطة: لا حكمَ في صنفٍ هنا، ولا استيرادَ من `kernel/` ولا من `arabic/`
ولا من حزمة التوليد.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from .composition import CompositionChain
from .layer import LayerSignature
from .schema import META_ALGEBRA_SCHEMA, MetaAlgebraSchema
from .standing import SpecificationSetRef
from .transition import TransitionSignature

__all__ = [
    "A_CHAIN_IS_NOT_A_SPECIFICATION",
    "A_SPECIFICATION_IS_WRITTEN_IN_A_NAMED_SCHEMA",
    "AbstractSystemSpecification",
    "AbstractSystemSpecificationError",
    "SchemaRef",
]


class AbstractSystemSpecificationError(ValueError):
    """رفضٌ عند الإنشاء: انتقالٌ يتيم، أو بصمةُ لغةٍ غيرُ مطابقة."""


A_CHAIN_IS_NOT_A_SPECIFICATION: Final[str] = (
    "السلسلةُ مسارٌ داخل النظريّة لا النظريّةُ نفسُها: مواصفةٌ تُختزَل في سلسلتها "
    "تفقد كلَّ طبقةٍ لا تقع على ذلك المسار"
)

A_SPECIFICATION_IS_WRITTEN_IN_A_NAMED_SCHEMA: Final[str] = (
    "كلُّ نظريّةٍ مكتوبةٌ بلغةٍ مُسمّاةٍ مبصومة؛ ونظريّةٌ تشير إلى بصمةِ لغةٍ غيرِ "
    "القائمة نظريّةٌ بلغةٍ أخرى، تُرفَض ولا تُقرَأ بالتسامح"
)


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise AbstractSystemSpecificationError(f"{label} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class SchemaRef:
    """إشارةٌ إلى `Σ_M`: إصدارُها وبصمةُ محتواها.

    والمطابقةُ تُفحَص عند الإنشاء مقابلَ اللغة المُجمَّدة في `schema`، فلا تُبنى
    نظريّةٌ على لغةٍ لم تَعُد قائمة.
    """

    schema_version: str
    content_id: str

    def __post_init__(self) -> None:
        _require_text(self.schema_version, "إصدارُ اللغة")
        _require_text(self.content_id, "بصمةُ اللغة")

    @classmethod
    def of(cls, schema: MetaAlgebraSchema = META_ALGEBRA_SCHEMA) -> SchemaRef:
        """إشارةٌ مُشتَقّةٌ من لغةٍ قائمة؛ ولا تُكتَب بصمتُها باليد."""

        return cls(schema_version=schema.schema_version, content_id=schema.content_id)

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الإشارة للبصمة."""

        return {
            "schema_version": self.schema_version,
            "content_id": self.content_id,
        }


@dataclass(frozen=True, slots=True)
class AbstractSystemSpecification:
    """`Σ_A`: طبقاتٌ وانتقالاتٌ بعينها، مكتوبةٌ بلغةٍ مُسمّاة، مبصومةٌ بمحتواها."""

    spec_id: str
    schema_ref: SchemaRef
    layers: tuple[LayerSignature, ...]
    transitions: tuple[TransitionSignature, ...]
    chains: tuple[CompositionChain, ...] = ()

    def __post_init__(self) -> None:
        _require_text(self.spec_id, "اسمُ المواصفة")
        if not isinstance(self.schema_ref, SchemaRef):
            raise AbstractSystemSpecificationError(
                A_SPECIFICATION_IS_WRITTEN_IN_A_NAMED_SCHEMA
            )
        if (
            self.schema_ref.schema_version != META_ALGEBRA_SCHEMA.schema_version
            or self.schema_ref.content_id != META_ALGEBRA_SCHEMA.content_id
        ):
            raise AbstractSystemSpecificationError(
                A_SPECIFICATION_IS_WRITTEN_IN_A_NAMED_SCHEMA
            )
        if not isinstance(self.layers, tuple) or not self.layers:
            raise AbstractSystemSpecificationError("المواصفةُ طبقةٌ فأكثر")
        if not isinstance(self.transitions, tuple):
            raise AbstractSystemSpecificationError("الانتقالاتُ مجموعةٌ مُصرَّحٌ بها")
        if not isinstance(self.chains, tuple):
            raise AbstractSystemSpecificationError("السلاسلُ مجموعةٌ مُصرَّحٌ بها")
        for layer in self.layers:
            if not isinstance(layer, LayerSignature):
                raise AbstractSystemSpecificationError("عضوٌ في الطبقات خارج نوعه")
        for transition in self.transitions:
            if not isinstance(transition, TransitionSignature):
                raise AbstractSystemSpecificationError("عضوٌ في الانتقالات خارج نوعه")
        for chain in self.chains:
            if not isinstance(chain, CompositionChain):
                raise AbstractSystemSpecificationError(
                    "عضوٌ في السلاسل خارج نوعه؛ و" + A_CHAIN_IS_NOT_A_SPECIFICATION
                )
        _require_unique(self.layer_ids, "أسماءُ الطبقات")
        _require_unique(self.transition_ids, "أسماءُ الانتقالات")
        _require_unique(tuple(chain.chain_id for chain in self.chains), "أسماءُ السلاسل")
        declared = set(self.layer_ids)
        for transition in self.transitions:
            for layer_id, side in (
                (transition.source_layer_id, "المصدر"),
                (transition.target_layer_id, "الهدف"),
            ):
                if layer_id not in declared:
                    raise AbstractSystemSpecificationError(
                        f"انتقالٌ `{transition.transition_id}` يشير إلى طبقةِ "
                        f"{side} `{layer_id}` غيرِ المُسجَّلة في المواصفة"
                    )
        for chain in self.chains:
            for layer in chain.layers:
                if layer.layer_id not in declared:
                    raise AbstractSystemSpecificationError(
                        f"سلسلةٌ `{chain.chain_id}` تضمّ طبقةً `{layer.layer_id}` "
                        "خارج المواصفة"
                    )
            for transition in chain.transitions:
                if transition.transition_id not in set(self.transition_ids):
                    raise AbstractSystemSpecificationError(
                        f"سلسلةٌ `{chain.chain_id}` تضمّ انتقالًا "
                        f"`{transition.transition_id}` خارج المواصفة"
                    )

    @property
    def layer_ids(self) -> tuple[str, ...]:
        """أسماءُ الطبقات؛ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب."""

        return tuple(layer.layer_id for layer in self.layers)

    @property
    def transition_ids(self) -> tuple[str, ...]:
        """أسماءُ الانتقالات؛ خاصّيّةٌ تُشتَقّ كذلك."""

        return tuple(transition.transition_id for transition in self.transitions)

    def layer(self, layer_id: str) -> LayerSignature:
        """الطبقةُ باسمها؛ والغيابُ رفضٌ لا `None` يُقرأ صمتًا."""

        for declared in self.layers:
            if declared.layer_id == layer_id:
                return declared
        raise AbstractSystemSpecificationError(
            f"لا طبقةَ في المواصفة اسمُها `{layer_id}`"
        )

    def transition(self, transition_id: str) -> TransitionSignature:
        """الانتقالُ باسمه؛ والغيابُ رفضٌ كذلك."""

        for declared in self.transitions:
            if declared.transition_id == transition_id:
                return declared
        raise AbstractSystemSpecificationError(
            f"لا انتقالَ في المواصفة اسمُه `{transition_id}`"
        )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المواصفة للبصمة؛ ولا تحقيقَ داخلَها بحال."""

        return {
            "spec_id": self.spec_id,
            "schema_ref": self.schema_ref.as_canonical_content(),
            "layers": [layer.as_canonical_content() for layer in self.layers],
            "transitions": [
                transition.as_canonical_content() for transition in self.transitions
            ],
            "chains": [chain.as_canonical_content() for chain in self.chains],
        }

    @property
    def content_id(self) -> str:
        """بصمةُ النظريّة؛ وهي `sigma_digest` الذي يُبنى عليه كلُّ توليد."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))

    def as_specification_ref(self, scope: str) -> SpecificationSetRef:
        """إشارةُ `Σ` لسجلّات المنزلة في `G0.ST`؛ ولا بصمةَ تُكتَب باليد."""

        return SpecificationSetRef(
            sigma_id=self.spec_id, content_id=self.content_id, scope=scope
        )


def _require_unique(names: tuple[str, ...], label: str) -> None:
    if len(set(names)) != len(names):
        raise AbstractSystemSpecificationError(
            f"{label} بلا تكرار؛ والمكرّرُ يُخفي واحدًا تحت هويّة آخر"
        )


_JUDGEMENT_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "outcome",
    "verdict",
    "status",
    "standing",
    "birth",
    "proved",
    "realization",
)

_SPECIFICATION_TYPES: Final[tuple[type, ...]] = (
    AbstractSystemSpecification,
    SchemaRef,
)

for _declaring_type in _SPECIFICATION_TYPES:  # pragma: no cover - import guard
    for _field in fields(_declaring_type):
        if any(marker in _field.name for marker in _JUDGEMENT_FIELD_MARKERS):
            raise RuntimeError(
                "المواصفةُ تحمل بنيتَها لا أحكامَها ولا تحقيقاتِها؛ ولا حقلَ من ذلك فيها"
            )
