import pytest

from alghanem.kernel.birth import (
    BirthAssessmentRequest,
    BirthExperimentSpecification,
    BirthExperimentSpecificationError,
    BirthFreeze,
    BirthQuery,
    BirthRevisionHistory,
    BirthVerdict,
    BirthVerdictStatus,
    CompetingExplanation,
    EvidenceMode,
    EvidenceSnapshot,
    ProjectionPoset,
)


def specification(revision_id: str = "r1") -> BirthExperimentSpecification:
    return BirthExperimentSpecification(
        experiment_id="experiment",
        revision_id=revision_id,
        evidence_mode=EvidenceMode.FORMAL,
        domain="finite-domain",
        projection_poset=ProjectionPoset(
            ("count", "set", "multiset", "sequence", "unicode"),
            (("count", "multiset"), ("set", "multiset"), ("multiset", "sequence")),
        ),
        birth_query=BirthQuery("query", "is sequence necessary?", "sequence"),
        frozen_weaker_models=("count", "set", "multiset"),
        residual_definition="unexplained distinction",
        closure_criterion="all prerequisite models fail to close the residual",
        evidence_requirements="exhaustive proof over the finite domain",
    )


def request(revision_id: str = "r1") -> BirthAssessmentRequest:
    return BirthAssessmentRequest(
        specification(revision_id), EvidenceSnapshot("snapshot", "enumeration")
    )


def verdict(status: BirthVerdictStatus, revision_id: str = "r1") -> BirthVerdict:
    return BirthVerdict(request(revision_id), status, "assessment complete")


def test_specification_derives_complete_prerequisite_cone() -> None:
    spec = specification()

    assert spec.prerequisite_cone == ("count", "set", "multiset")
    assert spec.competing_projections == ("unicode",)


def test_specification_rejects_caller_selected_incomplete_cone() -> None:
    with pytest.raises(
        BirthExperimentSpecificationError,
        match="exactly equal the derived prerequisite cone",
    ):
        BirthExperimentSpecification(
            experiment_id="experiment",
            revision_id="r1",
            evidence_mode=EvidenceMode.FORMAL,
            domain="finite-domain",
            projection_poset=ProjectionPoset(("low", "target"), (("low", "target"),)),
            birth_query=BirthQuery("query", "necessary?", "target"),
            frozen_weaker_models=(),
            residual_definition="residual",
            closure_criterion="criterion",
            evidence_requirements="requirements",
        )


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


def test_evidence_is_bound_after_the_frozen_specification() -> None:
    assessment = request()

    assert assessment.specification.birth_query.query_id == "query"
    assert assessment.evidence_snapshot.snapshot_id == "snapshot"


def test_birth_with_competing_explanation_requires_discriminating_evidence() -> None:
    with pytest.raises(ValueError, match="requires discriminating evidence"):
        BirthVerdict(
            request(),
            BirthVerdictStatus.BIRTH_IN_SCOPE,
            "would otherwise be born",
            (CompetingExplanation("unicode", "alternative closure"),),
        )


def test_only_birth_verdict_can_be_frozen() -> None:
    with pytest.raises(ValueError, match="only BIRTH_IN_SCOPE"):
        BirthFreeze(verdict(BirthVerdictStatus.DEFER_IN_SCOPE), "E0")

    frozen = BirthFreeze(verdict(BirthVerdictStatus.BIRTH_IN_SCOPE), "E0")

    assert frozen.e0_id == "E0"


def test_revision_history_preserves_old_verdict_and_activates_latest() -> None:
    old = verdict(BirthVerdictStatus.BIRTH_IN_SCOPE, "r1")
    current = verdict(BirthVerdictStatus.NO_BIRTH_IN_SCOPE, "r2")
    history = BirthRevisionHistory((old, current), "r2")

    assert history.verdicts == (old, current)
    assert history.active_revision_id == "r2"
