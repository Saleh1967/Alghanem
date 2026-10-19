"""The immutable set of inquiries that remain open for encyclopedia growth."""

from __future__ import annotations

from dataclasses import dataclass

from alghanem.kernel.fractal import ReopenExperimentSpecification

from .inquiry import EncyclopediaContractError, RootInquiry


@dataclass(frozen=True, slots=True)
class GrowthFrontier:
    """Open root and reopened inquiries; it records no verdict or knowledge."""

    root_inquiries: tuple[RootInquiry, ...]
    reopen_inquiries: tuple[ReopenExperimentSpecification, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.root_inquiries, tuple) or any(
            not isinstance(inquiry, RootInquiry) for inquiry in self.root_inquiries
        ):
            raise EncyclopediaContractError(
                "growth frontier root inquiries must be RootInquiry values"
            )
        if not isinstance(self.reopen_inquiries, tuple) or any(
            not isinstance(inquiry, ReopenExperimentSpecification)
            for inquiry in self.reopen_inquiries
        ):
            raise EncyclopediaContractError(
                "growth frontier reopen inquiries must be reopen specifications"
            )
        root_ids = tuple(inquiry.inquiry_id for inquiry in self.root_inquiries)
        if len(set(root_ids)) != len(root_ids):
            raise EncyclopediaContractError(
                "growth frontier must not repeat root inquiry ids"
            )
        reopen_ids = tuple(inquiry.reopen_id for inquiry in self.reopen_inquiries)
        if len(set(reopen_ids)) != len(reopen_ids):
            raise EncyclopediaContractError(
                "growth frontier must not repeat reopen inquiry ids"
            )
