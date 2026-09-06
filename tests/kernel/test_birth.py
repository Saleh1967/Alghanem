import pytest

import alghanem.kernel.birth as birth
from alghanem.kernel.birth import (
    BirthAssessmentRequest,
    BirthExperimentSpecification,
    BirthExperimentSpecificationError,
    BirthQuery,
    EvidenceMode,
    EvidenceSnapshot,
    ProjectionPoset,
    StructureHypothesis,
)


def specification() -> BirthExperimentSpecification:
    return BirthExperimentSpecification(
        experiment_id="experiment",
        revision_id="r1",
        revision_sequence=1,
        evidence_mode=EvidenceMode.FORMAL,
        domain="finite-domain",
        projection_poset=ProjectionPoset(
            ("count", "set", "multiset", "sequence", "unicode"),
            (("count", "multiset"), ("set", "multiset"), ("multiset", "sequence")),
        ),
        birth_query=BirthQuery(
            "query",
            StructureHypothesis("structure", "a structure is necessary"),
            "sequence",
        ),
        residual_definition="unexplained distinction",
        closure_criterion="all prerequisite models fail to close the residual",
        evidence_requirements="exhaustive proof over the finite domain",
    )


def test_specification_derives_models_without_treating_them_as_ontology() -> None:
    spec = specification()

    assert spec.birth_query.hypothesis.hypothesis_id == "structure"
    assert spec.birth_query.test_model == "sequence"
    assert spec.prerequisite_cone == ("count", "set", "multiset")
    assert spec.frozen_weaker_models == spec.prerequisite_cone
    assert spec.competing_projections == ("unicode",)


@pytest.mark.parametrize(
    ("projections", "relations", "message"),
    [
        (("one", "two"), (("one", "missing"),), "declared projections"),
        (("one", "two"), (("one", "two"), ("one", "two")), "duplicates"),
        (("one", "two"), (("one", "two"), ("two", "one")), "cycles"),
    ],
)
def test_projection_poset_rejects_malformed_relations(
    projections: tuple[str, ...],
    relations: tuple[tuple[str, str], ...],
    message: str,
) -> None:
    with pytest.raises(BirthExperimentSpecificationError, match=message):
        ProjectionPoset(projections, relations)


def test_g0_1_exports_no_birth_authority_or_freeze() -> None:
    assert not hasattr(birth, "BirthVerdict")
    assert not hasattr(birth, "BirthFreeze")
    assert not hasattr(birth, "BirthRevisionHistory")
    assert not hasattr(birth, "CompetingExplanation")


def test_assessment_request_binds_evidence_after_frozen_specification() -> None:
    request = BirthAssessmentRequest(
        specification(), EvidenceSnapshot("snapshot", "enumeration")
    )

    assert request.evidence_snapshot.snapshot_id == "snapshot"


@pytest.mark.parametrize("specification_value", (None, "not-a-specification"))
def test_malformed_assessment_request_cannot_enter_future_runtime(
    specification_value: object,
) -> None:
    with pytest.raises(BirthExperimentSpecificationError, match="specification"):
        BirthAssessmentRequest(
            specification_value,  # type: ignore[arg-type]
            EvidenceSnapshot("snapshot", "enumeration"),
        )


@pytest.mark.parametrize("evidence_value", (None, "not-an-evidence-snapshot"))
def test_request_requires_a_real_evidence_snapshot(evidence_value: object) -> None:
    with pytest.raises(BirthExperimentSpecificationError, match="evidence snapshot"):
        BirthAssessmentRequest(
            specification(),
            evidence_value,  # type: ignore[arg-type]
        )
