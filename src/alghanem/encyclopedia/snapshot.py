"""The minimal immutable encyclopedia state: frozen discovery plus open inquiry."""

from __future__ import annotations

from dataclasses import dataclass

from alghanem.kernel.fractal import FractalSnapshot

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
