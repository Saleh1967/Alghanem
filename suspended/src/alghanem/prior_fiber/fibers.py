"""`G0.FIBER-0.FIBERS`: ثلاثةُ ألياف متوازية من العقدة الواحدة.

    P  →  CarrierAlone  ‖  ContentAlone  ‖  CarrierAndContentTogether

والتوازي شرطٌ بنيويٌّ لا ترتيبُ عرض: كلُّ ليفٍ يُشتَقُّ من العقدة نفسِها ببصمتها،
ولا يُقبَل ليفٌ يُصرِّح بأنّه مبنيٌّ على مخرج ليفٍ آخر. فلو جاز ذلك لصار محورٌ
شرطًا لمحور، ولانتقلت أخطاءُ الأوّل إلى الثاني بلا موضعِ ردّ.

ولا يفرض هذا الطورُ على الليف دورًا إيجابيًّا: الليفُ يرث حيادَ عقدته، ويحمل
مرجعَ رتبته إحالةً، ولا يقرأ جوابًا.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from .laws import (
    THE_THREE_FIBERS_ARE_PARALLEL_NOT_SEQUENTIAL,
    PriorFiberError,
)
from .node import PriorFiberNode

__all__ = [
    "FIBER_AXIS_COUNT_IS_NOT_FROZEN_NOTE",
    "FiberAxis",
    "ParallelFiberBundle",
    "ProjectedFiber",
    "project_all_fibers",
    "project_fiber",
]

FIBER_AXIS_COUNT_IS_NOT_FROZEN_NOTE: Final[str] = (
    "عددُ المحاور يُشتَقُّ من المفردة المغلقة نفسِها، ولا يُثبَّت رقمًا في موضعٍ " "ثانٍ ينحرف عنها"
)


class FiberAxis(Enum):
    """محاورُ الاشتقاق الثلاثة؛ مفردةٌ مغلقةٌ محايدةٌ عن أيّ لسانٍ بعينه."""

    CARRIER_ALONE = "carrier_alone"
    CONTENT_ALONE = "content_alone"
    CARRIER_AND_CONTENT_TOGETHER = "carrier_and_content_together"

    @property
    def reads_the_carrier(self) -> bool:
        """أيقرأ هذا المحورُ الحاملَ؟"""

        return self is not FiberAxis.CONTENT_ALONE

    @property
    def reads_the_content(self) -> bool:
        """أيقرأ هذا المحورُ المحمولَ؟"""

        return self is not FiberAxis.CARRIER_ALONE


@dataclass(frozen=True, slots=True)
class ProjectedFiber:
    """ليفٌ واحدٌ مُشتَقٌّ من العقدة: محورُه، وبصمةُ عقدته، وما يقرأ."""

    axis: FiberAxis
    node_content_id: str
    origin_id: str
    instance_id: str
    slot_geometry: tuple[str, ...]
    admissible_distinction_ids: tuple[str, ...]
    derived_from_fiber: FiberAxis | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.axis, FiberAxis):
            raise PriorFiberError("محورُ الليف عضوٌ في مفردته المغلقة")
        if self.derived_from_fiber is not None:
            raise PriorFiberError(THE_THREE_FIBERS_ARE_PARALLEL_NOT_SEQUENTIAL)
        for label, value in (
            ("بصمةُ العقدة", self.node_content_id),
            ("مُعرِّفُ الأصل", self.origin_id),
            ("مُعرِّفُ النسخة", self.instance_id),
        ):
            if not isinstance(value, str) or not value.strip():
                raise PriorFiberError(f"{label} نصٌّ غير فارغ")
        if not self.slot_geometry:
            raise PriorFiberError("ليفٌ بلا هندسة خانات لا يقرأ شيئًا")

    @property
    def is_parallel_by_construction(self) -> bool:
        """أمُشتَقٌّ هذا الليفُ من العقدة مباشرةً لا من ليفٍ آخر؟"""

        return self.derived_from_fiber is None

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الليف للبصمة."""

        return {
            "axis": self.axis.value,
            "node_content_id": self.node_content_id,
            "origin_id": self.origin_id,
            "instance_id": self.instance_id,
            "slot_geometry": list(self.slot_geometry),
            "admissible_distinction_ids": list(self.admissible_distinction_ids),
            "reads_the_carrier": self.axis.reads_the_carrier,
            "reads_the_content": self.axis.reads_the_content,
        }

    @property
    def content_id(self) -> str:
        """بصمةُ الليف."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


@dataclass(frozen=True, slots=True)
class ParallelFiberBundle:
    """حزمةُ الألياف المتوازية: تغطيةٌ تامّةٌ للمحاور، وبصمةُ عقدةٍ واحدة."""

    node_content_id: str
    fibers: tuple[ProjectedFiber, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.fibers, tuple) or not self.fibers:
            raise PriorFiberError("حزمةٌ بلا ليفٍ لا تُشتَقّ")
        axes = tuple(fiber.axis for fiber in self.fibers)
        if len(set(axes)) != len(axes):
            raise PriorFiberError("محورٌ مُكرَّرٌ في الحزمة؛ والمكرّرُ يُرفَض لا يُطوى")
        missing = tuple(axis.value for axis in FiberAxis if axis not in set(axes))
        if missing:
            raise PriorFiberError(
                "تغطيةُ المحاور تامّةٌ لا أحسنَ جهد؛ والمحاورُ الغائبة: "
                + "، ".join(missing)
            )
        for fiber in self.fibers:
            if fiber.node_content_id != self.node_content_id:
                raise PriorFiberError("ليفٌ على بصمةِ عقدةٍ أخرى ليس عضوًا في هذه الحزمة")

    @property
    def is_parallel(self) -> bool:
        """أكلُّ ليفٍ في الحزمة مُشتَقٌّ من العقدة مباشرةً؟"""

        return all(fiber.is_parallel_by_construction for fiber in self.fibers)

    @property
    def parallelism_law(self) -> str:
        """قانونُ التوازي الذي تقوم عليه الحزمة."""

        return THE_THREE_FIBERS_ARE_PARALLEL_NOT_SEQUENTIAL

    def fiber(self, axis: FiberAxis) -> ProjectedFiber:
        """الليفُ بمحوره؛ والغيابُ رفضٌ لا `None` يُقرأ صمتًا."""

        for fiber in self.fibers:
            if fiber.axis is axis:
                return fiber
        raise PriorFiberError(f"لا ليفَ في الحزمة بمحور `{axis.value}`")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الحزمة للبصمة."""

        return {
            "node_content_id": self.node_content_id,
            "fibers": [
                fiber.as_canonical_content()
                for fiber in sorted(self.fibers, key=lambda item: item.axis.value)
            ],
            "is_parallel": self.is_parallel,
        }

    @property
    def content_id(self) -> str:
        """بصمةُ الحزمة."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


def project_fiber(node: PriorFiberNode, axis: FiberAxis) -> ProjectedFiber:
    """اشتقّ ليفًا واحدًا من العقدة مباشرةً."""

    if not isinstance(node, PriorFiberNode):
        raise PriorFiberError("الاشتقاقُ يقع على عقدةٍ ليفيّةٍ من نوعها")
    if not isinstance(axis, FiberAxis):
        raise PriorFiberError("محورُ الاشتقاق عضوٌ في مفردته المغلقة")
    return ProjectedFiber(
        axis=axis,
        node_content_id=node.content_id,
        origin_id=node.origin_id,
        instance_id=node.instance_id,
        slot_geometry=node.slot_geometry,
        admissible_distinction_ids=tuple(
            distinction.distinction_id for distinction in node.admissible_distinctions
        ),
    )


def project_all_fibers(node: PriorFiberNode) -> ParallelFiberBundle:
    """اشتقّ المحاورَ كلَّها من العقدة الواحدة معًا لا على التعاقب."""

    return ParallelFiberBundle(
        node_content_id=node.content_id,
        fibers=tuple(project_fiber(node, axis) for axis in FiberAxis),
    )


def _refuse_a_frozen_axis_count() -> None:
    """ارفض عند الاستيراد أيَّ عددٍ مُثبَّتٍ للمحاور خارج المفردة."""

    for name in globals():
        if name.startswith("EXPECTED") or name.endswith("_EXPECTED_COUNT"):
            raise PriorFiberError(FIBER_AXIS_COUNT_IS_NOT_FROZEN_NOTE)


_refuse_a_frozen_axis_count()
