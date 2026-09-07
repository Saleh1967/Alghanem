import pytest

from alghanem.encyclopedia.frontier import GrowthFrontier
from alghanem.encyclopedia.inquiry import (
    EncyclopediaContractError,
    QuestionProposal,
    RootInquiry,
)
from alghanem.encyclopedia.snapshot import EncyclopediaNucleusSnapshot
from alghanem.kernel.birth import (
    BirthExperimentSpecification,
    BirthQuery,
    EvidenceMode,
    ProjectionPoset,
    StructureHypothesis,
)
from alghanem.kernel.fractal import FractalSnapshot


def birth_specification() -> BirthExperimentSpecification:
    return BirthExperimentSpecification(
        experiment_id="root-experiment",
        revision_id="r1",
        revision_sequence=1,
        evidence_mode=EvidenceMode.FORMAL,
        domain="discovery-jurisdiction",
        projection_poset=ProjectionPoset(("weaker", "test"), (("weaker", "test"),)),
        birth_query=BirthQuery(
            "root-question",
            StructureHypothesis("candidate", "a factor may be necessary"),
            "test",
        ),
        residual_definition_id="residual",
        residual_definition="unexplained observations",
        closure_criterion_id="closure",
        closure_criterion="all weaker models fail to close",
        evidence_requirements="finite formal observations",
    )


def root_inquiry() -> RootInquiry:
    return RootInquiry(
        inquiry_id="root-inquiry",
        jurisdiction_id="discovery-jurisdiction",
        experiment=birth_specification(),
    )


class TestInquiryContracts:
    def test_root_inquiry_requires_complete_g0_specification(self) -> None:
        with pytest.raises(EncyclopediaContractError):
            RootInquiry(
                inquiry_id="root-inquiry",
                jurisdiction_id="discovery-jurisdiction",
                experiment="proposal-only",  # type: ignore[arg-type]
            )

    def test_proposal_is_not_executable_inquiry(self) -> None:
        proposal = QuestionProposal(
            proposal_id="residual-proposal",
            jurisdiction_id="discovery-jurisdiction",
            basis_id="residual-1",
        )

        assert "experiment" not in QuestionProposal.__dataclass_fields__
        assert "execute" not in dir(proposal)
        assert "proposal" not in RootInquiry.__dataclass_fields__

    def test_contracts_do_not_introduce_domain_text_or_knowledge_fields(self) -> None:
        declared_fields = set(QuestionProposal.__dataclass_fields__)
        declared_fields.update(RootInquiry.__dataclass_fields__)

        assert declared_fields.isdisjoint(
            {"domain", "article", "text", "claim", "knowledge"}
        )


class TestGrowthFrontier:
    def test_deferred_root_inquiry_remains_in_immutable_frontier(self) -> None:
        frontier = GrowthFrontier((root_inquiry(),), ())

        assert frontier.root_inquiries == (root_inquiry(),)
        with pytest.raises(AttributeError):
            frontier.root_inquiries = ()  # type: ignore[misc]

    def test_rejects_duplicate_root_inquiry_ids(self) -> None:
        inquiry = root_inquiry()
        with pytest.raises(EncyclopediaContractError):
            GrowthFrontier((inquiry, inquiry), ())


class TestEncyclopediaNucleusSnapshot:
    def test_wraps_immutable_fractal_and_open_frontier(self) -> None:
        fractal = FractalSnapshot((), (), ())
        snapshot = EncyclopediaNucleusSnapshot(
            fractal=fractal,
            frontier=GrowthFrontier((root_inquiry(),), ()),
        )

        assert snapshot.fractal is fractal
        with pytest.raises(AttributeError):
            snapshot.fractal = FractalSnapshot((), (), ())  # type: ignore[misc]
