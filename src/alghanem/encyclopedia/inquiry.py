"""Neutral inquiry contracts for the encyclopedia growth frontier.

These contracts deliberately issue neither evidence nor birth, freeze, or
knowledge decisions. A proposal is not an inquiry: only a complete G0
experiment specification can enter the frontier.
"""

from __future__ import annotations

from dataclasses import dataclass

from alghanem.kernel.birth import (
    BirthExperimentSpecification,
    BirthExperimentSpecificationError,
    _require_text,
)


class EncyclopediaContractError(BirthExperimentSpecificationError):
    """A malformed encyclopedia contract cannot enter the growth frontier."""


@dataclass(frozen=True, slots=True)
class QuestionProposal:
    """An unapproved question candidate, never an executable inquiry.

    Question generation is distinct from question authorization. This contract
    intentionally has no experiment or execution fields: a future authority
    must first translate an approved proposal into a separately frozen G0
    specification before a `RootInquiry` may be constructed.
    """

    proposal_id: str
    jurisdiction_id: str
    basis_id: str

    def __post_init__(self) -> None:
        _require_text(self.proposal_id, "question proposal id")
        _require_text(self.jurisdiction_id, "question proposal jurisdiction id")
        _require_text(self.basis_id, "question proposal basis id")


@dataclass(frozen=True, slots=True)
class RootInquiry:
    """A neutral root inquiry bound to one complete pre-evidence G0 contract."""

    inquiry_id: str
    jurisdiction_id: str
    experiment: BirthExperimentSpecification

    def __post_init__(self) -> None:
        _require_text(self.inquiry_id, "root inquiry id")
        _require_text(self.jurisdiction_id, "root inquiry jurisdiction id")
        if not isinstance(self.experiment, BirthExperimentSpecification):
            raise EncyclopediaContractError(
                "a root inquiry requires a complete BirthExperimentSpecification"
            )
