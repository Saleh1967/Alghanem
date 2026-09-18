"""المقياسُ عقدٌ لا لافتة: ما وحدتُه، وما هويّتُه، وما يجوز فيه، ومتى يُغلَق.

    FractalScaleContract  =  unit + identity + admissible operation + closure

**والمرجعُ لا يُقبَل إلّا بعقدٍ مُسجَّل** (`AScaleRefIsResolvedNotAsserted`):
`FractalScaleRef` يحمل مُعرِّفَ المقياس وبصمةَ عقده، ولا يصير مقياسًا إلّا إذا
قابل عقدًا في `ScaleSpace` ببصمته نفسِها؛ فاسمٌ بلا عقدٍ لافتةٌ لا مقياس.

**والعلاقاتُ بين المقاييس رأسيّةٌ وحدَها**: `REFINES` و`AGGREGATES`؛ ولا
`SIBLING` هنا، لأنّ الأخوّة أفقيّةٌ بين الفروع في مقياسٍ واحد لا بين المقاييس.

تسجيلٌ لا سلطة: لا ولادةَ، ولا حكمَ ولادةٍ، ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest, is_canonical_digest

__all__ = [
    "A_SCALE_REF_IS_RESOLVED_NOT_ASSERTED",
    "FractalScaleContract",
    "FractalScaleError",
    "FractalScaleRef",
    "ScaleRelation",
    "ScaleRelationEdge",
    "ScaleSpace",
]


A_SCALE_REF_IS_RESOLVED_NOT_ASSERTED: Final[str] = (
    "المرجعُ يُحَلّ ولا يُدّعى: مرجعُ المقياس يُقابَل بعقدٍ مُسجَّلٍ ببصمته، "
    "واسمٌ بلا عقدٍ مقابلٍ لافتةٌ لا مقياس"
)


class FractalScaleError(ValueError):
    """رفضٌ عند تكوين عقدِ مقياسٍ أو مرجعِه أو فضائه."""


def _named_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise FractalScaleError(f"{label} نصٌّ غير فارغ")
    return value


class ScaleRelation(Enum):
    """العلاقاتُ الرأسيّةُ بين المقاييس؛ مفردةٌ مغلقةٌ لا أخوّةَ فيها."""

    REFINES = "refines"
    AGGREGATES = "aggregates"


@dataclass(frozen=True, slots=True)
class FractalScaleContract:
    """عقدُ مقياس: وحدتُه، وهويّتُه، وعملياتُه الجائزة، وشرطُ إغلاقه."""

    scale_id: str
    domain_id: str
    unit_criterion: str
    identity_criterion: str
    admissible_operation_contract: str
    closure_contract: str

    def __post_init__(self) -> None:
        _named_text(self.scale_id, "مُعرِّفُ المقياس")
        _named_text(self.domain_id, "مجالُ المقياس")
        _named_text(self.unit_criterion, "معيارُ الوحدة")
        _named_text(self.identity_criterion, "معيارُ الهويّة")
        _named_text(self.admissible_operation_contract, "عقدُ العمليّات الجائزة")
        _named_text(self.closure_contract, "عقدُ الإغلاق")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى العقد للبصمة."""

        return {
            "scale_id": self.scale_id,
            "domain_id": self.domain_id,
            "unit_criterion": self.unit_criterion,
            "identity_criterion": self.identity_criterion,
            "admissible_operation_contract": self.admissible_operation_contract,
            "closure_contract": self.closure_contract,
        }

    @property
    def content_id(self) -> str:
        """بصمةُ العقد؛ مُشتَقّةٌ من محتواه لا مكتوبةٌ فيه."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))

    def as_ref(self) -> FractalScaleRef:
        """مرجعٌ إلى هذا العقد بعينه."""

        return FractalScaleRef(
            scale_id=self.scale_id, contract_content_id=self.content_id
        )


@dataclass(frozen=True, slots=True)
class FractalScaleRef:
    """مرجعُ مقياس: مُعرِّفُه وبصمةُ عقده؛ ولا يصير مقياسًا إلّا بحلٍّ في فضاء."""

    scale_id: str
    contract_content_id: str

    def __post_init__(self) -> None:
        _named_text(self.scale_id, "مُعرِّفُ المقياس المُشار إليه")
        if not is_canonical_digest(self.contract_content_id):
            raise FractalScaleError(
                "المرجعُ يحمل بصمةَ عقدٍ قانونيّةً؛ و" + A_SCALE_REF_IS_RESOLVED_NOT_ASSERTED
            )


@dataclass(frozen=True, slots=True)
class ScaleRelationEdge:
    """حافّةٌ رأسيّةٌ بين مقياسين: أدنى، وأعلى، وجنسُ العلاقة."""

    relation: ScaleRelation
    lower_scale_id: str
    higher_scale_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.relation, ScaleRelation):
            raise FractalScaleError("جنسُ العلاقة عضوٌ في مفردته الرأسيّة المغلقة")
        _named_text(self.lower_scale_id, "المقياسُ الأدنى")
        _named_text(self.higher_scale_id, "المقياسُ الأعلى")
        if self.lower_scale_id == self.higher_scale_id:
            raise FractalScaleError("لا علاقةَ رأسيّةَ لمقياسٍ مع نفسه")


class ScaleSpace:
    """فضاءُ المقاييس: سجلُّ العقود وحافّاتُها الرأسيّة، وسلطةُ حلِّ المراجع."""

    __slots__ = ("_contracts", "_edges")

    def __init__(
        self,
        *,
        contracts: tuple[FractalScaleContract, ...],
        relations: tuple[ScaleRelationEdge, ...] = (),
    ) -> None:
        if not isinstance(contracts, tuple) or not contracts:
            raise FractalScaleError("فضاءُ المقاييس يُسجَّل بعقدٍ واحدٍ فأكثر")
        registry: dict[str, FractalScaleContract] = {}
        for contract in contracts:
            if not isinstance(contract, FractalScaleContract):
                raise FractalScaleError("عضوٌ في سجلّ المقاييس خارج نوعه")
            if contract.scale_id in registry:
                raise FractalScaleError("مُعرِّفُ مقياسٍ مُكرَّرٌ في فضاءٍ واحد")
            registry[contract.scale_id] = contract
        if not isinstance(relations, tuple):
            raise FractalScaleError("حافّاتُ الفضاء مجموعةٌ مُصرَّحٌ بها")
        for edge in relations:
            if not isinstance(edge, ScaleRelationEdge):
                raise FractalScaleError("عضوٌ في حافّات الفضاء خارج نوعه")
            for scale_id in (edge.lower_scale_id, edge.higher_scale_id):
                if scale_id not in registry:
                    raise FractalScaleError(
                        "حافّةٌ تُشير إلى مقياسٍ غير مُسجَّل؛ و"
                        + A_SCALE_REF_IS_RESOLVED_NOT_ASSERTED
                    )
        self._contracts: dict[str, FractalScaleContract] = registry
        self._edges: tuple[ScaleRelationEdge, ...] = relations

    @property
    def contracts(self) -> tuple[FractalScaleContract, ...]:
        """العقودُ المُسجَّلة بترتيب تسجيلها؛ والترتيبُ عرضٌ لا حكم."""

        return tuple(self._contracts.values())

    @property
    def relations(self) -> tuple[ScaleRelationEdge, ...]:
        """الحافّاتُ الرأسيّةُ المُسجَّلة."""

        return self._edges

    def admits(self, ref: object) -> bool:
        """هل يُقابِل هذا المرجعُ عقدًا مُسجَّلًا ببصمته نفسِها؟"""

        if not isinstance(ref, FractalScaleRef):
            return False
        contract = self._contracts.get(ref.scale_id)
        return contract is not None and contract.content_id == ref.contract_content_id

    def resolve(self, ref: object) -> FractalScaleContract:
        """حُلَّ المرجعَ إلى عقده، أو ارفضه إن لم يُقابِل عقدًا مُسجَّلًا."""

        if not self.admits(ref):
            raise FractalScaleError(
                "مرجعُ مقياسٍ لا يُقابِل عقدًا مُسجَّلًا ببصمته؛ و"
                + A_SCALE_REF_IS_RESOLVED_NOT_ASSERTED
            )
        assert isinstance(ref, FractalScaleRef)
        return self._contracts[ref.scale_id]

    def ref_for(self, scale_id: str) -> FractalScaleRef:
        """مرجعٌ مُحَلٌّ إلى مقياسٍ مُسجَّلٍ باسمه."""

        contract = self._contracts.get(_named_text(scale_id, "مُعرِّفُ المقياس المطلوب"))
        if contract is None:
            raise FractalScaleError("لا عقدَ مُسجَّلًا بهذا المُعرِّف في هذا الفضاء")
        return contract.as_ref()

    def relation_between(
        self, *, lower_scale_id: str, higher_scale_id: str
    ) -> ScaleRelation | None:
        """جنسُ العلاقة الرأسيّة بين مقياسين إن سُجِّلت، وإلّا غيابٌ صريح."""

        for edge in self._edges:
            if (
                edge.lower_scale_id == lower_scale_id
                and edge.higher_scale_id == higher_scale_id
            ):
                return edge.relation
        return None
