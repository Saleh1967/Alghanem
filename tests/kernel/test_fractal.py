import pytest

from alghanem.kernel.birth import BirthExperimentSpecificationError
from alghanem.kernel.fractal import (
    BornBridgeRef,
    DerivedRelationSpec,
    FractalContractError,
    FractalProvenancePath,
    FractalSnapshot,
    FrozenFactorRef,
    ReopenExperimentSpecification,
)


def factor_ref(factor_id: str = "f1") -> FrozenFactorRef:
    return FrozenFactorRef(
        factor_id=factor_id,
        factor_content_id="content-" + factor_id,
        freeze_certificate_id="cert-" + factor_id,
        domain="encoding",
        birth_experiment_id="experiment",
        birth_revision_id="r1",
    )


class TestFrozenFactorRef:
    def test_valid_construction(self) -> None:
        ref = factor_ref()
        assert ref.factor_id == "f1"
        assert ref.domain == "encoding"

    @pytest.mark.parametrize(
        "field_name",
        [
            "factor_id",
            "factor_content_id",
            "freeze_certificate_id",
            "domain",
            "birth_experiment_id",
            "birth_revision_id",
        ],
    )
    def test_rejects_blank_fields(self, field_name: str) -> None:
        kwargs = dict(
            factor_id="f1",
            factor_content_id="content",
            freeze_certificate_id="cert",
            domain="encoding",
            birth_experiment_id="experiment",
            birth_revision_id="r1",
        )
        kwargs[field_name] = ""
        with pytest.raises(BirthExperimentSpecificationError):
            FrozenFactorRef(**kwargs)

    def test_is_frozen(self) -> None:
        ref = factor_ref()
        with pytest.raises(AttributeError):
            ref.factor_id = "other"  # type: ignore[misc]


class TestBornBridgeRef:
    def test_valid_construction(self) -> None:
        bridge = BornBridgeRef(
            bridge_id="b1",
            bridge_content_id="content-b1",
            freeze_certificate_id="cert-b1",
            domain="encoding",
            endpoint_refs=(factor_ref("f1"), factor_ref("f2")),
            birth_experiment_id="experiment",
            birth_revision_id="r1",
        )
        assert len(bridge.endpoint_refs) == 2

    def test_requires_at_least_two_endpoints(self) -> None:
        with pytest.raises(FractalContractError):
            BornBridgeRef(
                bridge_id="b1",
                bridge_content_id="content-b1",
                freeze_certificate_id="cert-b1",
                domain="encoding",
                endpoint_refs=(factor_ref("f1"),),
                birth_experiment_id="experiment",
                birth_revision_id="r1",
            )

    def test_rejects_duplicate_endpoint_factors(self) -> None:
        with pytest.raises(FractalContractError):
            BornBridgeRef(
                bridge_id="b1",
                bridge_content_id="content-b1",
                freeze_certificate_id="cert-b1",
                domain="encoding",
                endpoint_refs=(factor_ref("f1"), factor_ref("f1")),
                birth_experiment_id="experiment",
                birth_revision_id="r1",
            )

    def test_rejects_non_factor_ref_endpoint(self) -> None:
        with pytest.raises(FractalContractError):
            BornBridgeRef(
                bridge_id="b1",
                bridge_content_id="content-b1",
                freeze_certificate_id="cert-b1",
                domain="encoding",
                endpoint_refs=(factor_ref("f1"), "not-a-ref"),  # type: ignore[arg-type]
                birth_experiment_id="experiment",
                birth_revision_id="r1",
            )


class TestDerivedRelationSpec:
    def test_valid_construction(self) -> None:
        relation = DerivedRelationSpec(
            relation_id="d1",
            source_factor_refs=(factor_ref("f1"), factor_ref("f2")),
            derivation_spec_id="spec",
            derivation_content_id="content",
            trace_id="trace",
        )
        assert relation.relation_id == "d1"

    def test_requires_at_least_one_source(self) -> None:
        with pytest.raises(FractalContractError):
            DerivedRelationSpec(
                relation_id="d1",
                source_factor_refs=(),
                derivation_spec_id="spec",
                derivation_content_id="content",
                trace_id="trace",
            )

    def test_rejects_duplicate_sources(self) -> None:
        with pytest.raises(FractalContractError):
            DerivedRelationSpec(
                relation_id="d1",
                source_factor_refs=(factor_ref("f1"), factor_ref("f1")),
                derivation_spec_id="spec",
                derivation_content_id="content",
                trace_id="trace",
            )


class TestReopenExperimentSpecification:
    def test_valid_construction(self) -> None:
        reopen = ReopenExperimentSpecification(
            reopen_id="reopen1",
            parents=(factor_ref("f1"),),
            new_question="does a coupling residual survive?",
            allowed_observables=("articulatory-evidence",),
            residual_definition_id="residual1",
            residual_definition="unexplained coupling distinction",
            closure_criterion_id="closure1",
            closure_criterion="every weaker reconstruction fails to close",
        )
        assert reopen.parents[0].factor_id == "f1"

    def test_requires_at_least_one_parent(self) -> None:
        with pytest.raises(FractalContractError):
            ReopenExperimentSpecification(
                reopen_id="reopen1",
                parents=(),
                new_question="q",
                allowed_observables=("obs",),
                residual_definition_id="residual1",
                residual_definition="text",
                closure_criterion_id="closure1",
                closure_criterion="text",
            )

    def test_rejects_duplicate_parents(self) -> None:
        with pytest.raises(FractalContractError):
            ReopenExperimentSpecification(
                reopen_id="reopen1",
                parents=(factor_ref("f1"), factor_ref("f1")),
                new_question="q",
                allowed_observables=("obs",),
                residual_definition_id="residual1",
                residual_definition="text",
                closure_criterion_id="closure1",
                closure_criterion="text",
            )


class TestFractalProvenancePath:
    def test_valid_construction_with_factor_ancestor(self) -> None:
        path = FractalProvenancePath(
            factor_id="f3",
            reopened_factor_refs=(factor_ref("f1"), factor_ref("f2")),
            reopened_bridge_refs=(),
            derived_relation_ids=("d1",),
            reopen_experiment_id="experiment2",
            reopen_revision_id="r1",
            residual_id="residual2",
            factorization_component_index=1,
        )
        assert path.factorization_component_index == 1

    def test_requires_at_least_one_ancestor(self) -> None:
        with pytest.raises(FractalContractError):
            FractalProvenancePath(
                factor_id="f3",
                reopened_factor_refs=(),
                reopened_bridge_refs=(),
                derived_relation_ids=(),
                reopen_experiment_id="experiment2",
                reopen_revision_id="r1",
                residual_id="residual2",
            )

    def test_rejects_negative_component_index(self) -> None:
        with pytest.raises(FractalContractError):
            FractalProvenancePath(
                factor_id="f3",
                reopened_factor_refs=(factor_ref("f1"),),
                reopened_bridge_refs=(),
                derived_relation_ids=(),
                reopen_experiment_id="experiment2",
                reopen_revision_id="r1",
                residual_id="residual2",
                factorization_component_index=-1,
            )


class TestFractalSnapshot:
    def test_valid_construction(self) -> None:
        f1 = factor_ref("f1")
        f2 = factor_ref("f2")
        snapshot = FractalSnapshot(
            frozen_factors=(f1, f2),
            derived_relations=(
                DerivedRelationSpec(
                    relation_id="d1",
                    source_factor_refs=(f1, f2),
                    derivation_spec_id="spec",
                    derivation_content_id="content",
                    trace_id="trace",
                ),
            ),
            born_bridges=(
                BornBridgeRef(
                    bridge_id="b1",
                    bridge_content_id="content-b1",
                    freeze_certificate_id="cert-b1",
                    domain="encoding",
                    endpoint_refs=(f1, f2),
                    birth_experiment_id="experiment",
                    birth_revision_id="r1",
                ),
            ),
        )
        assert len(snapshot.frozen_factors) == 2

    def test_rejects_duplicate_factors(self) -> None:
        f1 = factor_ref("f1")
        with pytest.raises(FractalContractError):
            FractalSnapshot(
                frozen_factors=(f1, f1),
                derived_relations=(),
                born_bridges=(),
            )

    def test_rejects_derived_relation_referencing_outside_factor(self) -> None:
        f1 = factor_ref("f1")
        outside = factor_ref("outside")
        with pytest.raises(FractalContractError):
            FractalSnapshot(
                frozen_factors=(f1,),
                derived_relations=(
                    DerivedRelationSpec(
                        relation_id="d1",
                        source_factor_refs=(f1, outside),
                        derivation_spec_id="spec",
                        derivation_content_id="content",
                        trace_id="trace",
                    ),
                ),
                born_bridges=(),
            )

    def test_rejects_bridge_referencing_outside_factor(self) -> None:
        f1 = factor_ref("f1")
        f2 = factor_ref("f2")
        outside = factor_ref("outside")
        with pytest.raises(FractalContractError):
            FractalSnapshot(
                frozen_factors=(f1, f2),
                derived_relations=(),
                born_bridges=(
                    BornBridgeRef(
                        bridge_id="b1",
                        bridge_content_id="content-b1",
                        freeze_certificate_id="cert-b1",
                        domain="encoding",
                        endpoint_refs=(f1, outside),
                        birth_experiment_id="experiment",
                        birth_revision_id="r1",
                    ),
                ),
            )

    def test_no_rule_table_field_exists(self) -> None:
        assert not hasattr(FractalSnapshot, "rule_table")
        assert "rule_table" not in FractalSnapshot.__dataclass_fields__
