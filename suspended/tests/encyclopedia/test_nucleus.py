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
from alghanem.kernel.experiment_spec_content_identity import (
    BirthExperimentSpecificationContentBinding,
    CanonicalBirthExperimentSpecificationEncoder,
    PreEvidenceSpecificationRegistry,
)
from alghanem.kernel.fractal import (
    BornBridgeRef,
    FractalSnapshot,
    FrozenFactorRef,
    ReopenExperimentSpecification,
)


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
    specification = birth_specification()
    return RootInquiry(
        inquiry_id="root-inquiry",
        jurisdiction_id="discovery-jurisdiction",
        experiment_binding=BirthExperimentSpecificationContentBinding(
            specification,
            PreEvidenceSpecificationRegistry().freeze(
                CanonicalBirthExperimentSpecificationEncoder.encode(specification)
            ),
        ),
    )


class TestInquiryContracts:
    @pytest.mark.parametrize(
        "field_name", ["proposal_id", "jurisdiction_id", "basis_id"]
    )
    def test_question_proposal_rejects_blank_fields(self, field_name: str) -> None:
        kwargs = {
            "proposal_id": "proposal",
            "jurisdiction_id": "discovery-jurisdiction",
            "basis_id": "residual",
        }
        kwargs[field_name] = ""

        with pytest.raises(EncyclopediaContractError):
            QuestionProposal(**kwargs)

    def test_root_inquiry_requires_frozen_pre_evidence_content_binding(self) -> None:
        with pytest.raises(EncyclopediaContractError):
            RootInquiry(
                inquiry_id="root-inquiry",
                jurisdiction_id="discovery-jurisdiction",
                experiment_binding="specification-only",  # type: ignore[arg-type]
            )

    def test_root_inquiry_exposes_the_bound_specification(self) -> None:
        inquiry = root_inquiry()

        assert inquiry.experiment is inquiry.experiment_binding.specification

    def test_root_inquiry_jurisdiction_must_match_bound_experiment_domain(self) -> None:
        inquiry = root_inquiry()
        with pytest.raises(EncyclopediaContractError, match="jurisdiction"):
            RootInquiry(
                inquiry_id=inquiry.inquiry_id,
                jurisdiction_id="different-jurisdiction",
                experiment_binding=inquiry.experiment_binding,
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
        assert "experiment" not in RootInquiry.__dataclass_fields__
        assert "experiment_binding" in RootInquiry.__dataclass_fields__

    def test_contracts_do_not_introduce_domain_text_or_knowledge_fields(self) -> None:
        declared_fields = set(QuestionProposal.__dataclass_fields__)
        declared_fields.update(RootInquiry.__dataclass_fields__)

        assert declared_fields.isdisjoint(
            {"domain", "article", "text", "claim", "knowledge"}
        )


class TestGrowthFrontier:
    def test_frontier_is_immutable(self) -> None:
        frontier = GrowthFrontier((root_inquiry(),), ())

        assert frontier.root_inquiries == (root_inquiry(),)
        with pytest.raises(AttributeError):
            frontier.root_inquiries = ()  # type: ignore[misc]

    def test_rejects_duplicate_root_inquiry_ids(self) -> None:
        inquiry = root_inquiry()
        with pytest.raises(EncyclopediaContractError):
            GrowthFrontier((inquiry, inquiry), ())

    def test_rejects_duplicate_reopen_inquiry_ids(self) -> None:
        parent = FrozenFactorRef(
            factor_id="factor",
            factor_content_id="content",
            freeze_certificate_id="certificate",
            domain="discovery-jurisdiction",
            birth_experiment_id="parent-experiment",
            birth_revision_id="r1",
        )
        inquiry = ReopenExperimentSpecification(
            reopen_id="reopen",
            parents=(parent,),
            experiment=birth_specification(),
            allowed_observables=("observation",),
        )

        with pytest.raises(EncyclopediaContractError):
            GrowthFrontier((), (inquiry, inquiry))

    @pytest.mark.parametrize(
        ("root_inquiries", "reopen_inquiries"),
        [
            ([], ()),
            (("not-an-inquiry",), ()),
            ((), []),
            ((), ("not-a-reopen",)),
        ],
    )
    def test_rejects_non_tuple_or_wrongly_typed_inquiries(
        self, root_inquiries: object, reopen_inquiries: object
    ) -> None:
        with pytest.raises(EncyclopediaContractError):
            GrowthFrontier(root_inquiries, reopen_inquiries)  # type: ignore[arg-type]


class TestEncyclopediaNucleusSnapshot:
    @pytest.mark.parametrize(
        ("fractal", "frontier"),
        [
            ("not-a-fractal", GrowthFrontier((), ())),
            (FractalSnapshot((), (), ()), "not-a-frontier"),
        ],
    )
    def test_rejects_wrongly_typed_state_parts(
        self, fractal: object, frontier: object
    ) -> None:
        with pytest.raises(EncyclopediaContractError):
            EncyclopediaNucleusSnapshot(  # type: ignore[arg-type]
                fractal=fractal,
                frontier=frontier,
            )

    def test_wraps_immutable_fractal_and_open_frontier(self) -> None:
        fractal = FractalSnapshot((), (), ())
        snapshot = EncyclopediaNucleusSnapshot(
            fractal=fractal,
            frontier=GrowthFrontier((root_inquiry(),), ()),
        )

        assert snapshot.fractal is fractal
        with pytest.raises(AttributeError):
            snapshot.fractal = FractalSnapshot((), (), ())  # type: ignore[misc]

    def test_reopen_parents_must_exist_as_exact_snapshot_references(self) -> None:
        parent = FrozenFactorRef(
            factor_id="factor",
            factor_content_id="content",
            freeze_certificate_id="certificate",
            domain="discovery-jurisdiction",
            birth_experiment_id="parent-experiment",
            birth_revision_id="r1",
        )
        reopen = ReopenExperimentSpecification(
            reopen_id="reopen",
            parents=(parent,),
            experiment=birth_specification(),
            allowed_observables=("observation",),
        )

        with pytest.raises(EncyclopediaContractError, match="reopen.*exact frozen"):
            EncyclopediaNucleusSnapshot(
                fractal=FractalSnapshot((), (), ()),
                frontier=GrowthFrontier((), (reopen,)),
            )

        snapshot = EncyclopediaNucleusSnapshot(
            fractal=FractalSnapshot((parent,), (), ()),
            frontier=GrowthFrontier((), (reopen,)),
        )

        assert snapshot.frontier.reopen_inquiries == (reopen,)

    def test_reopen_parent_must_not_only_share_a_factor_id(self) -> None:
        recorded = FrozenFactorRef(
            factor_id="factor",
            factor_content_id="original-content",
            freeze_certificate_id="certificate",
            domain="discovery-jurisdiction",
            birth_experiment_id="parent-experiment",
            birth_revision_id="r1",
        )
        drifted = FrozenFactorRef(
            factor_id="factor",
            factor_content_id="drifted-content",
            freeze_certificate_id="certificate",
            domain="discovery-jurisdiction",
            birth_experiment_id="parent-experiment",
            birth_revision_id="r1",
        )
        reopen = ReopenExperimentSpecification(
            reopen_id="reopen",
            parents=(drifted,),
            experiment=birth_specification(),
            allowed_observables=("observation",),
        )

        with pytest.raises(EncyclopediaContractError, match="exact frozen"):
            EncyclopediaNucleusSnapshot(
                fractal=FractalSnapshot((recorded,), (), ()),
                frontier=GrowthFrontier((), (reopen,)),
            )

    def test_reopen_parent_may_be_a_snapshot_born_bridge(self) -> None:
        first = FrozenFactorRef(
            factor_id="first",
            factor_content_id="first-content",
            freeze_certificate_id="first-certificate",
            domain="discovery-jurisdiction",
            birth_experiment_id="first-experiment",
            birth_revision_id="r1",
        )
        second = FrozenFactorRef(
            factor_id="second",
            factor_content_id="second-content",
            freeze_certificate_id="second-certificate",
            domain="discovery-jurisdiction",
            birth_experiment_id="second-experiment",
            birth_revision_id="r1",
        )
        bridge = BornBridgeRef(
            bridge_id="bridge",
            bridge_content_id="bridge-content",
            freeze_certificate_id="bridge-certificate",
            domain="discovery-jurisdiction",
            endpoint_refs=(first, second),
            birth_experiment_id="bridge-experiment",
            birth_revision_id="r1",
        )
        reopen = ReopenExperimentSpecification(
            reopen_id="bridge-reopen",
            parents=(bridge,),
            experiment=birth_specification(),
            allowed_observables=("observation",),
        )

        snapshot = EncyclopediaNucleusSnapshot(
            fractal=FractalSnapshot((first, second), (), (bridge,)),
            frontier=GrowthFrontier((), (reopen,)),
        )

        assert snapshot.frontier.reopen_inquiries == (reopen,)
