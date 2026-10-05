"""`G0.METRIC-0`: المقامُ شجرةً مُجمَّدة، مُعلَنًا من خارج التنفيذ.

`CapabilityUniverse` لا تعرف `src/` ولا تقرأ ملفًّا واحدًا من الشجرة المبنيّة:
مقامٌ مُشتَقٌّ من التنفيذ يقيس التنفيذَ بنفسه
(`ADenominatorDerivedFromTheImplementationIsNotAMeasure`). وما لم يُبنَ يبقى
عقدةً في المقام، لا فراغًا خارج القسمة.

وتوسعةُ المقام تُصدِر مُلخَّصًا جديدًا: فشهادتان على مقامين ليستا مقارنةً، وإنقاصُ
الرقم بالتوسعة سلوكٌ صحيحٌ مُسمًّى (`TheMetricMustBeAllowedToGoDown`).
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass

from ..canonical_content import canonical_bytes, canonical_digest
from .node import CapabilityNode, NodeKind, Requirement

__all__ = [
    "CapabilityUniverse",
    "CapabilityUniverseError",
    "UniverseManifest",
]


class CapabilityUniverseError(ValueError):
    """رفضٌ بنيويٌّ مُسمًّى في بناء المقام؛ شجرةٌ معيبةٌ لا تُصحَّح صمتًا."""


@dataclass(frozen=True)
class UniverseManifest:
    """بيانُ المقام المُجمَّد: هويّتُه، وعددُ عقده وأوراقه، ومُلخَّصُ محتواه."""

    universe_id: str
    node_count: int
    leaf_count: int
    content_digest: str

    def as_canonical_content(self) -> dict[str, object]:
        """المحتوى القانونيّ للبيان."""

        return {
            "universe_id": self.universe_id,
            "node_count": self.node_count,
            "leaf_count": self.leaf_count,
            "content_digest": self.content_digest,
        }


class CapabilityUniverse:
    """شجرةُ المقام المُعلَن: أبٌ واحد، ولا دورة، ولا عقدةٌ بلا موضع."""

    __slots__ = ("_universe_id", "_nodes", "_children", "_root_id", "_manifest")

    def __init__(self, universe_id: str, nodes: Iterable[CapabilityNode]) -> None:
        if type(universe_id) is not str or not universe_id.strip():
            raise CapabilityUniverseError("a universe requires a universe_id")
        ordered = tuple(nodes)
        for node in ordered:
            if not isinstance(node, CapabilityNode):
                raise CapabilityUniverseError("a universe holds capability nodes only")
        by_id: dict[str, CapabilityNode] = {}
        for node in ordered:
            if node.node_id in by_id:
                raise CapabilityUniverseError(
                    f"«{node.node_id}» is declared twice in the denominator"
                )
            by_id[node.node_id] = node
        roots = tuple(node for node in ordered if node.is_root)
        if len(roots) != 1:
            raise CapabilityUniverseError(
                "a universe has exactly one total node, never zero and never two"
            )
        children: dict[str, list[str]] = {node.node_id: [] for node in ordered}
        for node in ordered:
            if node.parent_id is None:
                continue
            if node.parent_id not in by_id:
                raise CapabilityUniverseError(
                    f"«{node.node_id}» names an absent parent «{node.parent_id}»"
                )
            children[node.parent_id].append(node.node_id)
        self._universe_id = universe_id
        self._nodes: Mapping[str, CapabilityNode] = dict(by_id)
        self._children: Mapping[str, tuple[str, ...]] = {
            node_id: tuple(child_ids) for node_id, child_ids in children.items()
        }
        self._root_id = roots[0].node_id
        self._assert_every_node_reaches_the_root()
        self._manifest = self._derive_manifest()

    def _assert_every_node_reaches_the_root(self) -> None:
        reached: set[str] = set()
        frontier = [self._root_id]
        while frontier:
            node_id = frontier.pop()
            if node_id in reached:
                raise CapabilityUniverseError(
                    f"«{node_id}» is reached twice: the denominator is a tree"
                )
            reached.add(node_id)
            frontier.extend(self._children[node_id])
        if reached != set(self._nodes):
            orphans = sorted(set(self._nodes) - reached)
            raise CapabilityUniverseError(
                f"nodes outside the tree are outside the denominator: {orphans}"
            )

    def _derive_manifest(self) -> UniverseManifest:
        content = {
            "universe_id": self._universe_id,
            "nodes": [
                self._nodes[node_id].as_canonical_content()
                for node_id in sorted(self._nodes)
            ],
        }
        return UniverseManifest(
            universe_id=self._universe_id,
            node_count=len(self._nodes),
            leaf_count=len(self.leaf_ids()),
            content_digest=canonical_digest(canonical_bytes(content)),
        )

    @property
    def universe_id(self) -> str:
        """هويّةُ المقام المُعلَن."""

        return self._universe_id

    @property
    def root_id(self) -> str:
        """معرّفُ عقدة العربية الجامعة."""

        return self._root_id

    @property
    def manifest(self) -> UniverseManifest:
        """بيانُ المقام المُجمَّد، مُشتَقًّا لا مكتوبًا."""

        return self._manifest

    def node(self, node_id: str) -> CapabilityNode:
        """العقدةُ بمعرّفها؛ ومعرّفٌ غيرُ معلومٍ رفضٌ لا `None` صامت."""

        if node_id not in self._nodes:
            raise CapabilityUniverseError(f"«{node_id}» is not a declared capability")
        return self._nodes[node_id]

    def node_ids(self) -> tuple[str, ...]:
        """كلُّ معرّفات العقد مرتّبةً ترتيبًا مستقرًّا."""

        return tuple(sorted(self._nodes))

    def children(self, node_id: str) -> tuple[str, ...]:
        """أبناءُ العقدة مرتّبين ترتيبًا مستقرًّا."""

        self.node(node_id)
        return tuple(sorted(self._children[node_id]))

    def required_children(self, node_id: str) -> tuple[str, ...]:
        """الأبناءُ الذين يسقفون أباهم، دون المُسهِمين في تغطيته."""

        return tuple(
            child
            for child in self.children(node_id)
            if self._nodes[child].requirement is Requirement.REQUIRED
        )

    def is_leaf(self, node_id: str) -> bool:
        """هل العقدةُ ورقةٌ تُقاس بشواهدها مباشرةً؟"""

        return not self.children(node_id)

    def leaf_ids(self, node_id: str | None = None) -> tuple[str, ...]:
        """أوراقُ الشجرة تحت عقدةٍ ما، أو أوراقُ المقام كلِّه."""

        start = self._root_id if node_id is None else node_id
        self.node(start)
        leaves: list[str] = []
        frontier = [start]
        while frontier:
            current = frontier.pop()
            child_ids = self._children[current]
            if not child_ids:
                leaves.append(current)
            else:
                frontier.extend(child_ids)
        return tuple(sorted(leaves))

    def descendants(self, node_id: str) -> tuple[str, ...]:
        """العقدةُ وذريّتُها، ليُجمَّع عليها التغطيةُ والأهليّة."""

        self.node(node_id)
        collected: list[str] = []
        frontier = [node_id]
        while frontier:
            current = frontier.pop()
            collected.append(current)
            frontier.extend(self._children[current])
        return tuple(sorted(collected))

    def domain_ids(self) -> tuple[str, ...]:
        """معرّفاتُ المجالات العليا تحت العربية الجامعة."""

        return tuple(
            node_id
            for node_id in self.children(self._root_id)
            if self._nodes[node_id].kind is NodeKind.DOMAIN
        )
