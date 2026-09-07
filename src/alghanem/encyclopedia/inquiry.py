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
)
from alghanem.kernel.experiment_spec_content_identity import (
    BirthExperimentSpecificationContentBinding,
)


class EncyclopediaContractError(BirthExperimentSpecificationError):
    """A malformed encyclopedia contract cannot enter the growth frontier."""


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise EncyclopediaContractError(f"{field_name} must be non-blank")


@dataclass(frozen=True, slots=True)
class QuestionProposal:
    """An unapproved question candidate, never an executable inquiry.

    Question generation is distinct from question authorization. This contract
    intentionally has no experiment or execution fields: a future authority
    must first translate an approved proposal into a complete G0 specification,
    freeze its canonical content, and bind it before a `RootInquiry` may be
    constructed.
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
    """A neutral root inquiry bound to authority-frozen pre-evidence content."""

    inquiry_id: str
    jurisdiction_id: str
    experiment_binding: BirthExperimentSpecificationContentBinding

    def __post_init__(self) -> None:
        _require_text(self.inquiry_id, "root inquiry id")
        _require_text(self.jurisdiction_id, "root inquiry jurisdiction id")
        if not isinstance(
            self.experiment_binding, BirthExperimentSpecificationContentBinding
        ):
            raise EncyclopediaContractError(
                "a root inquiry requires an authority-frozen pre-evidence "
                "experiment content binding"
            )

    @property
    def experiment(self) -> BirthExperimentSpecification:
        """Return the content-bound experiment specification."""

        return self.experiment_binding.specification
