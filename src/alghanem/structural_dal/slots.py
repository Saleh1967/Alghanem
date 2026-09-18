"""`G0.SDAL-0.SLOTS`: الخانةُ والكلُّ البنيويّ؛ رموزٌ مُصطنَعةٌ لا لسانَ فيها.

الخانةُ هنا حاملٌ مُبهَم: لا حرفَ، ولا صوتَ، ولا مقطع. وإنّما تُثبَت صحّةُ
الجبر على `SlotA` ثمّ `SlotA + SlotB`، ويُؤجَّل كلُّ إسقاطٍ على لسانٍ بعينه.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from alghanem.fractal_generation import (
    FractalIdentity,
    FractalNode,
    FractalSeed,
    FractalTrace,
)

from .laws import (
    A_NEW_ANCHOR_REQUIRES_PROVENANCE,
    ZERO_ONE_BOUND,
    Scale,
    StructuralDalError,
)
from .space import SLOT_SCALE_REF

__all__ = [
    "DECLARED_ORIGIN",
    "StructuralSlot",
    "StructuralWhole",
    "origin_whole",
]

DECLARED_ORIGIN: str = "أصلٌ مُصرَّحٌ في هذا التشغيل لا مُرقًّى عن جزءٍ سابق"
"""نسبُ الكلِّ الابتدائيّ؛ يُصرَّح ولا يُترَك فراغًا."""

_IDENTITY_CRITERION: str = "criterion.structural_dal.whole_instance"


def _named_text(value: str, subject: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise StructuralDalError(f"{subject} نصٌّ غيرُ فارغ")
    return value


@dataclass(frozen=True, slots=True)
class StructuralSlot:
    """خانةٌ واحدةٌ في كلٍّ: موضعُها ورمزُها المُبهَم."""

    index: int
    token: str

    def __post_init__(self) -> None:
        if not isinstance(self.index, int) or isinstance(self.index, bool):
            raise StructuralDalError("موضعُ الخانة عددٌ صحيح")
        if self.index < 0:
            raise StructuralDalError("موضعُ الخانة لا يسبق الصفر")
        _named_text(self.token, "رمزُ الخانة")

    @property
    def slot_key(self) -> str:
        """مفتاحُ الخانة في محتوى العقدة؛ مُشتَقٌّ لا مكتوب."""

        return f"slot.{self.index}"


@dataclass(frozen=True, slots=True)
class StructuralWhole:
    """كلٌّ بنيويّ: مِرساةٌ، وخاناتٌ مرتّبة، ونسبٌ مُصرَّح، وأثرٌ إن وقع انتقال."""

    whole_id: str
    node: FractalNode
    provenance: str
    parent_anchor_id: str | None = None
    descent_depth: int = 0
    trace: FractalTrace | None = None

    def __post_init__(self) -> None:
        _named_text(self.whole_id, "مُعرِّفُ الكلّ")
        if not isinstance(self.node, FractalNode):
            raise StructuralDalError("الكلُّ يقوم على عقدةٍ من نوعها")
        _named_text(self.provenance, "نسبُ الكلّ")
        if not isinstance(self.descent_depth, int) or isinstance(
            self.descent_depth, bool
        ):
            raise StructuralDalError("عمقُ الانحدار عددٌ صحيح")
        if self.descent_depth < 0:
            raise StructuralDalError("عمقُ الانحدار لا يسبق الصفر")
        if (self.parent_anchor_id is None) != (self.descent_depth == 0):
            raise StructuralDalError(
                "كلٌّ بلا مِرساةِ أبٍ عمقُه صفرٌ، ومُرقًّى عمقُه فوق الصفر؛ و"
                + A_NEW_ANCHOR_REQUIRES_PROVENANCE
            )
        if self.parent_anchor_id is not None:
            _named_text(self.parent_anchor_id, "مِرساةُ الأب")
            if self.parent_anchor_id == self.anchor_id:
                raise StructuralDalError("مِرساةُ الأب لا تكون عينَ مِرساة الابن")
        if self.trace is not None and not isinstance(self.trace, FractalTrace):
            raise StructuralDalError("أثرُ الكلّ أثرٌ من نوعه أو لا أثرَ بعد")
        keys = tuple(key for key, _ in self.node.content)
        if not keys:
            raise StructuralDalError("الكلُّ خانةٌ واحدةٌ فأكثر")
        if keys != tuple(f"slot.{position}" for position in range(len(keys))):
            raise StructuralDalError("خاناتُ الكلّ متّصلةُ المواضع من الصفر بلا فجوة")

    @property
    def anchor_id(self) -> str:
        """مِرساةُ الكلّ؛ مقروءةٌ من هويّة العقدة لا مكتوبةٌ ثانية."""

        return self.node.identity.identity_id

    @property
    def slots(self) -> tuple[StructuralSlot, ...]:
        """خاناتُ الكلّ مرتّبةً؛ مُشتَقّةٌ من محتوى العقدة."""

        return tuple(
            StructuralSlot(index=position, token=token)
            for position, (_, token) in enumerate(self.node.content)
        )

    @property
    def slot_count(self) -> int:
        """عددُ الخانات؛ مُشتَقٌّ لا مُجمَّد."""

        return len(self.node.content)

    @property
    def tokens(self) -> tuple[str, ...]:
        """رموزُ الخانات مرتّبةً."""

        return tuple(token for _, token in self.node.content)

    @property
    def scale(self) -> Scale:
        """مقياسُ الكلّ في هذا الطور، أو رفضٌ فوق حدِّ `zero-one`."""

        for scale in Scale:
            if scale.slot_count == self.slot_count:
                return scale
        raise StructuralDalError(
            f"كلٌّ بـ{self.slot_count} خانةً فوق حدِّ هذا الطور {ZERO_ONE_BOUND}"
        )

    @property
    def content_id(self) -> str:
        """بصمةُ محتوى الكلّ؛ مُشتَقّةٌ من العقدة."""

        return self.node.content_id

    @property
    def trace_steps(self) -> int:
        """عددُ خطوات الأثر؛ صفرٌ قبل وقوع أيِّ انتقال."""

        return 0 if self.trace is None else len(self.trace.steps)

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الكلّ للعرض والمقارنة."""

        return {
            "whole_id": self.whole_id,
            "anchor_id": self.anchor_id,
            "parent_anchor_id": self.parent_anchor_id,
            "descent_depth": self.descent_depth,
            "provenance": self.provenance,
            "slots": [[slot.slot_key, slot.token] for slot in self.slots],
            "content_id": self.content_id,
            "trace_steps": self.trace_steps,
        }


def origin_whole(
    *,
    whole_id: str,
    anchor_id: str,
    carrier_id: str,
    tokens: Sequence[str],
) -> StructuralWhole:
    """ابنِ كلًّا ابتدائيًّا من رموزٍ مُصطنَعة؛ نسبُه مُصرَّحٌ وعمقُه صفر."""

    _named_text(anchor_id, "مِرساةُ الكلّ")
    _named_text(carrier_id, "حاملُ الكلّ")
    if not tokens:
        raise StructuralDalError("الكلُّ الابتدائيُّ خانةٌ واحدةٌ فأكثر")
    content = tuple(
        (f"slot.{position}", _named_text(token, "رمزُ الخانة"))
        for position, token in enumerate(tokens)
    )
    node = FractalNode.from_seed(
        FractalSeed(
            seed_id=f"seed.{whole_id}",
            identity=FractalIdentity(
                identity_id=anchor_id,
                scale_ref=SLOT_SCALE_REF,
                identity_criterion_id=_IDENTITY_CRITERION,
            ),
            carrier_id=carrier_id,
            content=content,
        ),
        node_id=f"node.{whole_id}",
    )
    return StructuralWhole(
        whole_id=whole_id,
        node=node,
        provenance=DECLARED_ORIGIN,
    )
