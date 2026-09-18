"""`G0.METRIC-0`: عقدةُ القدرة، بلا حقلِ حالةٍ يكتبه صاحبُها.

ليس في `CapabilityNode` حقلٌ اسمُه «مُنجَز» ولا «نسبة» ولا «درجة»: الحالةُ
تُشتَقّ من الشواهد في `measure.py`، فالادّعاءُ اليدويّ هنا **غيرُ قابلٍ للقول**
لا مرفوضٌ بعد وقوعه — وهو انضباطُ `arabic/epistemic_layers.py` نفسُه.

وكلُّ عقدةٍ تحمل استشهادَها: مصدرًا مُعلَنًا وموضعًا فيه
(`TheDenominatorIsCitedNotInvented`). والمصدرُ لا يُقرأ تصديقًا لعقدةٍ ولا
تكفيرًا لأخرى، وإنّما يُثبِت أنّ البابَ مُصطلَحٌ عليه في فنّه لا مُخترَعٌ هنا.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from .maturity import MaturityStage

__all__ = [
    "DECLARED_SOURCES",
    "CapabilityCitation",
    "CapabilityNode",
    "CapabilityNodeError",
    "DeclaredSource",
    "NodeKind",
    "Requirement",
]


class CapabilityNodeError(ValueError):
    """رفضٌ بنيويٌّ مُسمًّى في بناء العقدة؛ لا حملَ على أقرب حالة."""


class NodeKind(Enum):
    """جنسُ العقدة في الشجرة الفركتاليّة؛ مفردةٌ مغلقة."""

    TOTAL = "TOTAL"
    DOMAIN = "DOMAIN"
    CAPABILITY = "CAPABILITY"
    SUBCAPABILITY = "SUBCAPABILITY"


class Requirement(Enum):
    """علاقةُ الابن بأبيه: هل يسقف الأبَ أم يُسهِم في تغطيته فقط؟"""

    REQUIRED = "REQUIRED"
    CONTRIBUTING = "CONTRIBUTING"


@dataclass(frozen=True)
class DeclaredSource:
    """مصدرٌ مُعلَنٌ يُستشهَد به على وجود الباب في فنّه، لا على صحّة قولٍ فيه."""

    source_id: str
    title: str
    discipline: str

    def __post_init__(self) -> None:
        for name in ("source_id", "title", "discipline"):
            value = getattr(self, name)
            if type(value) is not str or not value.strip():
                raise CapabilityNodeError(
                    f"a declared source requires a non-empty «{name}»"
                )

    def as_canonical_content(self) -> dict[str, str]:
        """المحتوى القانونيّ للمصدر؛ لا بايتاتِ مصدرٍ ولا نقلَ نصّ."""

        return {
            "source_id": self.source_id,
            "title": self.title,
            "discipline": self.discipline,
        }


DECLARED_SOURCES: Final[tuple[DeclaredSource, ...]] = (
    DeclaredSource(
        source_id="sirr_sinaat_al_irab",
        title="سرُّ صناعة الإعراب — ابن جنّي",
        discipline="الأصوات والحروف",
    ),
    DeclaredSource(
        source_id="shafiya_ibn_al_hajib",
        title="الشافية في التصريف — ابن الحاجب",
        discipline="الصرف",
    ),
    DeclaredSource(
        source_id="sharh_ibn_aqil",
        title="شرح ابن عقيل على ألفيّة ابن مالك",
        discipline="النحو",
    ),
    DeclaredSource(
        source_id="mughni_al_labib",
        title="مغني اللبيب عن كتب الأعاريب — ابن هشام",
        discipline="الحروف والأدوات والإعراب",
    ),
    DeclaredSource(
        source_id="al_mustasfa",
        title="المستصفى من علم الأصول — الغزالي",
        discipline="أصول الفقه والدلالة",
    ),
    DeclaredSource(
        source_id="sharh_al_tahdhib",
        title="شرح تهذيب المنطق — التفتازاني وحواشيه",
        discipline="المنطق والدلالة الوضعيّة",
    ),
    DeclaredSource(
        source_id="miftah_al_ulum",
        title="مفتاح العلوم — السكّاكي",
        discipline="المعاني والبيان والخطاب",
    ),
)
"""المصادرُ المُعلَنةُ التي يُستشهَد بها على أبواب المقام؛ لا رابعَ لها يُضاف صمتًا."""

_SOURCE_IDS: Final[frozenset[str]] = frozenset(
    source.source_id for source in DECLARED_SOURCES
)


@dataclass(frozen=True)
class CapabilityCitation:
    """استشهادُ العقدة: مصدرٌ من المُعلَنين، وموضعٌ فيه باسم البابِ المصطلَح."""

    source_id: str
    locus: str

    def __post_init__(self) -> None:
        if type(self.source_id) is not str or self.source_id not in _SOURCE_IDS:
            raise CapabilityNodeError(
                "a citation names one of the declared sources and no other"
            )
        if type(self.locus) is not str or not self.locus.strip():
            raise CapabilityNodeError("a citation requires a non-empty locus")

    def as_canonical_content(self) -> dict[str, str]:
        """المحتوى القانونيّ للاستشهاد."""

        return {"source_id": self.source_id, "locus": self.locus}


@dataclass(frozen=True)
class CapabilityNode:
    """عقدةٌ في المقام المُعلَن؛ بلا حقلِ حالةٍ ولا نسبةٍ ولا درجةٍ مكتوبة."""

    node_id: str
    title: str
    kind: NodeKind
    parent_id: str | None
    requirement: Requirement
    citation: CapabilityCitation
    readiness_gate: MaturityStage

    def __post_init__(self) -> None:
        if type(self.node_id) is not str or not self.node_id.strip():
            raise CapabilityNodeError("a capability node requires a node_id")
        if type(self.title) is not str or not self.title.strip():
            raise CapabilityNodeError(f"«{self.node_id}» requires a title")
        if not isinstance(self.kind, NodeKind):
            raise CapabilityNodeError(f"«{self.node_id}» requires a NodeKind")
        if not isinstance(self.requirement, Requirement):
            raise CapabilityNodeError(f"«{self.node_id}» requires a Requirement")
        if not isinstance(self.citation, CapabilityCitation):
            raise CapabilityNodeError(
                f"«{self.node_id}» requires a citation: a denominator node is "
                "cited, never invented"
            )
        if not isinstance(self.readiness_gate, MaturityStage):
            raise CapabilityNodeError(
                f"«{self.node_id}» requires a declared readiness gate"
            )
        if not self.readiness_gate.is_an_attestable_gate:
            raise CapabilityNodeError(
                f"«{self.node_id}» cannot declare absence as its readiness gate"
            )
        if self.kind is NodeKind.TOTAL:
            if self.parent_id is not None:
                raise CapabilityNodeError("the total node has no parent")
        else:
            if type(self.parent_id) is not str or not self.parent_id.strip():
                raise CapabilityNodeError(f"«{self.node_id}» requires a parent_id")
            if self.parent_id == self.node_id:
                raise CapabilityNodeError(f"«{self.node_id}» cannot be its own parent")

    @property
    def is_root(self) -> bool:
        """هل هي عقدةُ العربيةِ الجامعة؟"""

        return self.kind is NodeKind.TOTAL

    def as_canonical_content(self) -> dict[str, object]:
        """المحتوى القانونيّ للعقدة، بلا حالةٍ ولا شاهدٍ ولا رقم."""

        return {
            "node_id": self.node_id,
            "title": self.title,
            "kind": self.kind.value,
            "parent_id": self.parent_id,
            "requirement": self.requirement.value,
            "citation": self.citation.as_canonical_content(),
            "readiness_gate": self.readiness_gate.value,
        }

    @property
    def node_digest(self) -> str:
        """مُلخَّصُ محتوى العقدة؛ يتغيّر بتغيّر إعلانها لا بتغيّر شواهدها."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))
