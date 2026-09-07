import pytest

from alghanem.kernel.birth import (
    BirthExperimentSpecification,
    BirthExperimentSpecificationError,
    BirthQuery,
    EvidenceMode,
    ProjectionPoset,
    StructureHypothesis,
)
from alghanem.kernel.fractal import (
    BornBridgeRef,
    DerivedRelationRef,
    DerivedRelationSpec,
    FractalContractError,
    FractalProvenancePath,
    FractalSnapshot,
    FrozenFactorRef,
    ProofLineageEdge,
    ReopenExperimentSpecification,
)


def factor_ref(
    factor_id: str = "f1",
    *,
    content_id: str | None = None,
    domain: str = "encoding",
    birth_experiment_id: str = "experiment",
    birth_revision_id: str = "r1",
    freeze_certificate_id: str | None = None,
) -> FrozenFactorRef:
    return FrozenFactorRef(
        factor_id=factor_id,
        factor_content_id=content_id or ("content-" + factor_id),
        freeze_certificate_id=freeze_certificate_id or ("cert-" + factor_id),
        domain=domain,
        birth_experiment_id=birth_experiment_id,
        birth_revision_id=birth_revision_id,
    )


def birth_specification(
    experiment_id: str = "reopen-experiment",
    revision_id: str = "r1",
) -> BirthExperimentSpecification:
    return BirthExperimentSpecification(
        experiment_id=experiment_id,
        revision_id=revision_id,
        revision_sequence=1,
        evidence_mode=EvidenceMode.FORMAL,
        domain="encoding",
        projection_poset=ProjectionPoset(
            ("count", "set", "multiset", "sequence"),
            (("count", "multiset"), ("set", "multiset"), ("multiset", "sequence")),
        ),
        birth_query=BirthQuery(
            "query",
            StructureHypothesis("structure", "a coupling is necessary"),
            "sequence",
        ),
        residual_definition_id="residual",
        residual_definition="unexplained coupling distinction",
        closure_criterion_id="closure",
        closure_criterion="every weaker reconstruction fails to close",
        evidence_requirements="articulatory contrast evidence",
    )


def reopen_specification(
    parent: FrozenFactorRef | BornBridgeRef,
    *,
    experiment_id: str,
    revision_id: str = "r1",
) -> ReopenExperimentSpecification:
    return ReopenExperimentSpecification(
        reopen_id=f"reopen-{experiment_id}",
        parents=(parent,),
        experiment=birth_specification(experiment_id, revision_id),
        allowed_observables=("obs",),
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
            birth_experiment_id="bridge-experiment",
            birth_revision_id="r1",
        )
        kwargs[field_name] = ""
        with pytest.raises(BirthExperimentSpecificationError):
            FrozenFactorRef(**kwargs)

    def test_is_frozen(self) -> None:
        ref = factor_ref()
        with pytest.raises(AttributeError):
            ref.factor_id = "other"  # type: ignore[misc]

    def test_constructibility_confers_no_authority(self) -> None:
        """`ConstructibleContract != IssuedByAuthority`: no freeze/reopen
        authority exists yet, so hand-constructing a well-formed
        `FrozenFactorRef` must never be treated as proof a factor was
        actually born and frozen. There is no issuer, no registry, and no
        flag on the object distinguishing "issued" from "hand-built"."""
        hand_built = factor_ref("f1")
        also_hand_built = factor_ref("f1")
        # Nothing on the object records provenance of *how* it was built;
        # two independently hand-built refs with identical fields compare
        # equal, exactly as two authority-issued refs would.
        assert hand_built == also_hand_built
        assert not hasattr(hand_built, "issued_by")
        assert not hasattr(hand_built, "is_authority_issued")


class TestBornBridgeRef:
    def test_valid_construction(self) -> None:
        bridge = BornBridgeRef(
            bridge_id="b1",
            bridge_content_id="content-b1",
            freeze_certificate_id="cert-b1",
            domain="encoding",
            endpoint_refs=(factor_ref("f1"), factor_ref("f2")),
            birth_experiment_id="bridge-experiment",
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
                birth_experiment_id="bridge-experiment",
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
                birth_experiment_id="bridge-experiment",
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
                birth_experiment_id="bridge-experiment",
                birth_revision_id="r1",
            )

    def test_requires_an_experiment_independent_of_its_endpoints(self) -> None:
        with pytest.raises(FractalContractError):
            BornBridgeRef(
                bridge_id="b1",
                bridge_content_id="content-b1",
                freeze_certificate_id="cert-b1",
                domain="encoding",
                endpoint_refs=(factor_ref("f1"), factor_ref("f2")),
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


class TestDerivedRelationRef:
    def test_valid_construction(self) -> None:
        ref = DerivedRelationRef(relation_id="d1", derivation_content_id="content-a")
        assert ref.relation_id == "d1"
        assert ref.derivation_content_id == "content-a"

    def test_rejects_blank_relation_id(self) -> None:
        with pytest.raises(BirthExperimentSpecificationError):
            DerivedRelationRef(relation_id="", derivation_content_id="content-a")

    def test_rejects_blank_content_id(self) -> None:
        with pytest.raises(BirthExperimentSpecificationError):
            DerivedRelationRef(relation_id="d1", derivation_content_id="")

    def test_same_relation_id_different_content_is_not_equal(self) -> None:
        """`SameRelationId != SameDerivationSemantics`: two refs sharing a
        `relation_id` but disagreeing on `derivation_content_id` must not
        compare equal, so provenance drift is detectable."""
        original = DerivedRelationRef(relation_id="d1", derivation_content_id="a")
        drifted = DerivedRelationRef(relation_id="d1", derivation_content_id="b")
        assert original != drifted


class TestReopenExperimentSpecification:
    def test_valid_construction(self) -> None:
        reopen = ReopenExperimentSpecification(
            reopen_id="reopen1",
            parents=(factor_ref("f1"),),
            experiment=birth_specification(),
            allowed_observables=("articulatory-evidence",),
        )
        assert reopen.parents[0].factor_id == "f1"
        assert reopen.experiment.experiment_id == "reopen-experiment"

    def test_requires_at_least_one_parent(self) -> None:
        with pytest.raises(FractalContractError):
            ReopenExperimentSpecification(
                reopen_id="reopen1",
                parents=(),
                experiment=birth_specification(),
                allowed_observables=("obs",),
            )

    def test_rejects_duplicate_parents(self) -> None:
        with pytest.raises(FractalContractError):
            ReopenExperimentSpecification(
                reopen_id="reopen1",
                parents=(factor_ref("f1"), factor_ref("f1")),
                experiment=birth_specification(),
                allowed_observables=("obs",),
            )

    def test_does_not_redeclare_question_residual_or_closure_fields(self) -> None:
        """`ReopenComposesG0DoesNotForkG0`: reopen must not have its own,
        independent question/residual/closure fields -- it must obtain them
        only through the embedded `BirthExperimentSpecification`."""
        declared_fields = set(ReopenExperimentSpecification.__dataclass_fields__)
        assert "new_question" not in declared_fields
        assert "residual_definition_id" not in declared_fields
        assert "residual_definition" not in declared_fields
        assert "closure_criterion_id" not in declared_fields
        assert "closure_criterion" not in declared_fields
        assert "experiment" in declared_fields

    def test_rejects_non_birth_experiment_specification(self) -> None:
        with pytest.raises(FractalContractError):
            ReopenExperimentSpecification(
                reopen_id="reopen1",
                parents=(factor_ref("f1"),),
                experiment="not-a-specification",  # type: ignore[arg-type]
                allowed_observables=("obs",),
            )

    def test_preserves_g0_revision_and_projection_poset(self) -> None:
        spec = birth_specification()
        reopen = ReopenExperimentSpecification(
            reopen_id="reopen1",
            parents=(factor_ref("f1"),),
            experiment=spec,
            allowed_observables=("obs",),
        )
        assert reopen.experiment.revision_id == spec.revision_id
        assert reopen.experiment.projection_poset is spec.projection_poset
        assert reopen.experiment.evidence_mode == spec.evidence_mode
        assert reopen.experiment.prerequisite_cone == spec.prerequisite_cone


class TestFractalProvenancePath:
    def test_valid_construction_with_factor_ancestor(self) -> None:
        path = FractalProvenancePath(
            factor_id="f3",
            reopened_factor_refs=(factor_ref("f1"), factor_ref("f2")),
            reopened_bridge_refs=(),
            derived_relation_refs=(
                DerivedRelationRef(relation_id="d1", derivation_content_id="content"),
            ),
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
                derived_relation_refs=(),
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
                derived_relation_refs=(),
                reopen_experiment_id="experiment2",
                reopen_revision_id="r1",
                residual_id="residual2",
                factorization_component_index=-1,
            )

    def test_rejects_bare_string_derived_relation_ids(self) -> None:
        """`derived_relation_refs` must be content-bound `DerivedRelationRef`
        values, not bare relation-id strings."""
        with pytest.raises(FractalContractError):
            FractalProvenancePath(
                factor_id="f3",
                reopened_factor_refs=(factor_ref("f1"),),
                reopened_bridge_refs=(),
                derived_relation_refs=("d1",),  # type: ignore[arg-type]
                reopen_experiment_id="experiment2",
                reopen_revision_id="r1",
                residual_id="residual2",
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
                    birth_experiment_id="bridge-experiment",
                    birth_revision_id="r1",
                ),
            ),
        )
        assert len(snapshot.frozen_factors) == 2

    def test_records_reopen_lineage_outside_other_graphs(self) -> None:
        parent = factor_ref("f1", birth_experiment_id="parent-experiment")
        child = factor_ref("f2", birth_experiment_id="reopen-experiment")
        lineage = ProofLineageEdge(
            parent_ref=parent,
            child_ref=child,
            reopen_specification=reopen_specification(
                parent, experiment_id="reopen-experiment"
            ),
        )
        snapshot = FractalSnapshot(
            frozen_factors=(parent, child),
            derived_relations=(),
            born_bridges=(),
            proof_lineage_edges=(lineage,),
        )
        assert snapshot.proof_lineage_edges == (lineage,)
        assert snapshot.born_bridges == ()
        assert snapshot.derived_relations == ()

    def test_rejects_lineage_with_an_endpoint_outside_the_snapshot(self) -> None:
        parent = factor_ref("f1", birth_experiment_id="parent-experiment")
        child = factor_ref("f2", birth_experiment_id="reopen-experiment")
        lineage = ProofLineageEdge(
            parent_ref=parent,
            child_ref=child,
            reopen_specification=reopen_specification(
                parent, experiment_id="reopen-experiment"
            ),
        )
        with pytest.raises(FractalContractError):
            FractalSnapshot(
                frozen_factors=(parent,),
                derived_relations=(),
                born_bridges=(),
                proof_lineage_edges=(lineage,),
            )

    def test_rejects_indirect_two_edge_cycle(self) -> None:
        f1 = factor_ref("f1", birth_experiment_id="e1")
        f2 = factor_ref("f2", birth_experiment_id="e2")
        edges = (
            ProofLineageEdge(
                parent_ref=f1,
                child_ref=f2,
                reopen_specification=reopen_specification(f1, experiment_id="e2"),
            ),
            ProofLineageEdge(
                parent_ref=f2,
                child_ref=f1,
                reopen_specification=reopen_specification(f2, experiment_id="e1"),
            ),
        )
        with pytest.raises(FractalContractError, match="acyclic"):
            FractalSnapshot(
                frozen_factors=(f1, f2),
                derived_relations=(),
                born_bridges=(),
                proof_lineage_edges=edges,
            )

    def test_rejects_indirect_three_edge_cycle(self) -> None:
        factors = tuple(
            factor_ref(f"f{i}", birth_experiment_id=f"e{i}") for i in range(1, 4)
        )
        edges = tuple(
            ProofLineageEdge(
                parent_ref=factors[index],
                child_ref=factors[(index + 1) % 3],
                reopen_specification=reopen_specification(
                    factors[index], experiment_id=f"e{(index + 1) % 3 + 1}"
                ),
            )
            for index in range(3)
        )
        with pytest.raises(FractalContractError, match="acyclic"):
            FractalSnapshot(
                frozen_factors=factors,
                derived_relations=(),
                born_bridges=(),
                proof_lineage_edges=edges,
            )

    def test_accepts_acyclic_lineage_chain(self) -> None:
        factors = tuple(
            factor_ref(f"f{i}", birth_experiment_id=f"e{i}") for i in range(1, 4)
        )
        edges = tuple(
            ProofLineageEdge(
                parent_ref=factors[index],
                child_ref=factors[index + 1],
                reopen_specification=reopen_specification(
                    factors[index], experiment_id=f"e{index + 2}"
                ),
            )
            for index in range(2)
        )
        snapshot = FractalSnapshot(
            frozen_factors=factors,
            derived_relations=(),
            born_bridges=(),
            proof_lineage_edges=edges,
        )
        assert snapshot.proof_lineage_edges == edges

    def test_accepts_born_bridge_as_lineage_parent(self) -> None:
        f1 = factor_ref("f1")
        f2 = factor_ref("f2")
        child = factor_ref("f3", birth_experiment_id="reopen-bridge")
        bridge = BornBridgeRef(
            bridge_id="b1",
            bridge_content_id="content-b1",
            freeze_certificate_id="cert-b1",
            domain="encoding",
            endpoint_refs=(f1, f2),
            birth_experiment_id="bridge-experiment",
            birth_revision_id="r1",
        )
        edge = ProofLineageEdge(
            parent_ref=bridge,
            child_ref=child,
            reopen_specification=reopen_specification(
                bridge, experiment_id="reopen-bridge"
            ),
        )
        snapshot = FractalSnapshot(
            frozen_factors=(f1, f2, child),
            derived_relations=(),
            born_bridges=(bridge,),
            proof_lineage_edges=(edge,),
        )
        assert snapshot.proof_lineage_edges == (edge,)

    def test_rejects_derived_relation_as_lineage_parent(self) -> None:
        relation = DerivedRelationRef(
            relation_id="d1", derivation_content_id="content"
        )
        with pytest.raises(FractalContractError):
            ProofLineageEdge(
                parent_ref=relation,  # type: ignore[arg-type]
                child_ref=factor_ref("f2", birth_experiment_id="e2"),
                reopen_specification=reopen_specification(
                    factor_ref("f1"), experiment_id="e2"
                ),
            )

    def test_rejects_parent_not_declared_by_reopen_specification(self) -> None:
        parent = factor_ref("f1")
        undeclared = factor_ref("f2")
        with pytest.raises(FractalContractError, match="declared"):
            ProofLineageEdge(
                parent_ref=parent,
                child_ref=factor_ref("f3", birth_experiment_id="e2"),
                reopen_specification=reopen_specification(
                    undeclared, experiment_id="e2"
                ),
            )

    def test_rejects_same_reopen_id_bound_to_different_specifications(self) -> None:
        parent_a = factor_ref("f1")
        parent_b = factor_ref("f2")
        child_a = factor_ref("f3", birth_experiment_id="e3")
        child_b = factor_ref("f4", birth_experiment_id="e4")
        spec_a = reopen_specification(parent_a, experiment_id="e3")
        spec_b = ReopenExperimentSpecification(
            reopen_id=spec_a.reopen_id,
            parents=(parent_b,),
            experiment=birth_specification("e4"),
            allowed_observables=("different-observation",),
        )
        edges = (
            ProofLineageEdge(parent_a, child_a, spec_a),
            ProofLineageEdge(parent_b, child_b, spec_b),
        )
        with pytest.raises(FractalContractError, match="one exact"):
            FractalSnapshot(
                frozen_factors=(parent_a, parent_b, child_a, child_b),
                derived_relations=(),
                born_bridges=(),
                proof_lineage_edges=edges,
            )

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
                        birth_experiment_id="bridge-experiment",
                        birth_revision_id="r1",
                    ),
                ),
            )

    def test_no_rule_table_field_exists(self) -> None:
        assert not hasattr(FractalSnapshot, "rule_table")
        assert "rule_table" not in FractalSnapshot.__dataclass_fields__

    def test_rejects_derived_relation_source_with_same_id_different_content(
        self,
    ) -> None:
        """`ExactFrozenReferencePreservation`: a relation source reference
        sharing `factor_id` with a snapshot member, but disagreeing on
        `factor_content_id`, must be rejected -- not silently accepted
        because the id string still matches."""
        f1_in_snapshot = factor_ref("f1", content_id="content-A")
        f1_drifted = factor_ref("f1", content_id="content-B")
        with pytest.raises(FractalContractError):
            FractalSnapshot(
                frozen_factors=(f1_in_snapshot,),
                derived_relations=(
                    DerivedRelationSpec(
                        relation_id="d1",
                        source_factor_refs=(f1_drifted,),
                        derivation_spec_id="spec",
                        derivation_content_id="content",
                        trace_id="trace",
                    ),
                ),
                born_bridges=(),
            )

    def test_rejects_derived_relation_source_with_same_id_different_scope(
        self,
    ) -> None:
        """Same `factor_id`, same `factor_content_id`, but a different
        `birth_experiment_id`/`domain`/`birth_revision_id`/
        `freeze_certificate_id` is still a distinct occurrence and must be
        rejected."""
        f1_in_snapshot = factor_ref("f1", birth_experiment_id="experiment-a")
        f1_other_scope = factor_ref("f1", birth_experiment_id="experiment-b")
        with pytest.raises(FractalContractError):
            FractalSnapshot(
                frozen_factors=(f1_in_snapshot,),
                derived_relations=(
                    DerivedRelationSpec(
                        relation_id="d1",
                        source_factor_refs=(f1_other_scope,),
                        derivation_spec_id="spec",
                        derivation_content_id="content",
                        trace_id="trace",
                    ),
                ),
                born_bridges=(),
            )

    def test_rejects_bridge_endpoint_with_same_id_different_content(self) -> None:
        f1_in_snapshot = factor_ref("f1", content_id="content-A")
        f2 = factor_ref("f2")
        f1_drifted = factor_ref("f1", content_id="content-B")
        with pytest.raises(FractalContractError):
            FractalSnapshot(
                frozen_factors=(f1_in_snapshot, f2),
                derived_relations=(),
                born_bridges=(
                    BornBridgeRef(
                        bridge_id="b1",
                        bridge_content_id="content-b1",
                        freeze_certificate_id="cert-b1",
                        domain="encoding",
                        endpoint_refs=(f1_drifted, f2),
                        birth_experiment_id="bridge-experiment",
                        birth_revision_id="r1",
                    ),
                ),
            )

    def test_rejects_bridge_endpoint_with_same_id_different_freeze_certificate(
        self,
    ) -> None:
        f1_in_snapshot = factor_ref("f1", freeze_certificate_id="cert-original")
        f2 = factor_ref("f2")
        f1_recertified = factor_ref("f1", freeze_certificate_id="cert-other")
        with pytest.raises(FractalContractError):
            FractalSnapshot(
                frozen_factors=(f1_in_snapshot, f2),
                derived_relations=(),
                born_bridges=(
                    BornBridgeRef(
                        bridge_id="b1",
                        bridge_content_id="content-b1",
                        freeze_certificate_id="cert-b1",
                        domain="encoding",
                        endpoint_refs=(f1_recertified, f2),
                        birth_experiment_id="bridge-experiment",
                        birth_revision_id="r1",
                    ),
                ),
            )

    def test_accepts_exact_matching_reference_by_value_not_identity(self) -> None:
        """A source/endpoint reference that is a *different Python object*
        but exactly equal in every field to the snapshot's frozen member
        must be accepted: membership is by value, not object identity."""
        f1_in_snapshot = factor_ref("f1")
        f1_equal_by_value = factor_ref("f1")
        assert f1_in_snapshot is not f1_equal_by_value
        assert f1_in_snapshot == f1_equal_by_value
        snapshot = FractalSnapshot(
            frozen_factors=(f1_in_snapshot,),
            derived_relations=(
                DerivedRelationSpec(
                    relation_id="d1",
                    source_factor_refs=(f1_equal_by_value,),
                    derivation_spec_id="spec",
                    derivation_content_id="content",
                    trace_id="trace",
                ),
            ),
            born_bridges=(),
        )
        assert len(snapshot.derived_relations) == 1
