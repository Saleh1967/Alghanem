"""The minimal immutable encyclopedia state: frozen discovery plus open inquiry."""

from __future__ import annotations

from dataclasses import dataclass

from alghanem.kernel.fractal import FractalSnapshot, FrozenOntologyRef

from .frontier import GrowthFrontier
from .inquiry import EncyclopediaContractError


@dataclass(frozen=True, slots=True)
class EncyclopediaNucleusSnapshot:
    """An audit snapshot, not a knowledge graph, domain index, or article store."""

    fractal: FractalSnapshot
    frontier: GrowthFrontier

    def __post_init__(self) -> None:
        if not isinstance(self.fractal, FractalSnapshot):
            raise EncyclopediaContractError(
                "encyclopedia nucleus requires a FractalSnapshot"
            )
        if not isinstance(self.frontier, GrowthFrontier):
            raise EncyclopediaContractError(
                "encyclopedia nucleus requires a GrowthFrontier"
            )
        ontology_refs: frozenset[FrozenOntologyRef] = frozenset(
            self.fractal.frozen_factors + self.fractal.born_bridges
        )
        for inquiry in self.frontier.reopen_inquiries:
            if any(parent not in ontology_refs for parent in inquiry.parents):
                raise EncyclopediaContractError(
                    "frontier reopen parents for "
                    f"{inquiry.reopen_id!r} must be exact frozen ontology "
                    "references present in the fractal snapshot"
                )
