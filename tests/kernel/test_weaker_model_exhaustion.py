import pytest

from alghanem.kernel.birth import BirthEvaluatorRole, ClosureAssessmentStatus
from alghanem.kernel.weaker_model_closure import (
    WeakerModelClosureCertificate,
    WeakerModelClosureGate,
)
from alghanem.kernel.weaker_model_exhaustion import (
    WeakerModelExhaustionAssessment,
    WeakerModelExhaustionError,
    WeakerModelExhaustionGate,
    WeakerModelExhaustionStatus,
)
from tests.kernel.test_weaker_model_closure import (
    CLOSE_TOKEN,
    DEFER_TOKEN,
    FAIL_TOKEN,
    assessment_request,
    provenance_bound_record,
    sealed_vocabulary_registry,
    specification,
)

CONE = ("count", "multiset", "set")
_TOKENS = {
    ClosureAssessmentStatus.CLOSE: CLOSE_TOKEN,
    ClosureAssessmentStatus.FAIL_TO_CLOSE: FAIL_TOKEN,
    ClosureAssessmentStatus.DEFER: DEFER_TOKEN,
}


def certificate_for(
    request, model_id: str, status: ClosureAssessmentStatus
) -> WeakerModelClosureCertificate:
    return WeakerModelClosureGate.assess(
        registry=sealed_vocabulary_registry(),
        record=provenance_bound_record(
            output=_TOKENS[status], target_id=model_id, request=request
        ),
    )


def certificates_for(
    request, outcomes: dict[str, ClosureAssessmentStatus]
) -> tuple[WeakerModelClosureCertificate, ...]:
    return tuple(
        certificate_for(request, model_id, status)
        for model_id, status in outcomes.items()
    )


def all_failing(request) -> tuple[WeakerModelClosureCertificate, ...]:
    return certificates_for(
        request, dict.fromkeys(CONE, ClosureAssessmentStatus.FAIL_TO_CLOSE)
    )


def test_the_frozen_cone_is_derived_not_written() -> None:
    assert set(assessment_request().specification.frozen_weaker_models) == set(CONE)


def test_every_model_failing_to_close_is_exhaustion() -> None:
    request = assessment_request()

    assessment = WeakerModelExhaustionGate.assess(
        request=request, certificates=all_failing(request)
    )

    assert (
        assessment.status
        is WeakerModelExhaustionStatus.LICENSED_WEAKER_MODELS_EXHAUSTED
    )
    assert assessment.is_weaker_model_exhaustion is True


def test_one_closing_model_outranks_every_deferral() -> None:
    request = assessment_request()
    certificates = certificates_for(
        request,
        {
            "count": ClosureAssessmentStatus.DEFER,
            "multiset": ClosureAssessmentStatus.DEFER,
            "set": ClosureAssessmentStatus.CLOSE,
        },
    )

    assessment = WeakerModelExhaustionGate.assess(
        request=request, certificates=certificates
    )

    assert assessment.status is WeakerModelExhaustionStatus.WEAKER_MODEL_CLOSES_RESIDUAL
    assert assessment.closing_models == ("set",)
    assert assessment.is_weaker_model_exhaustion is False


def test_a_single_deferral_blocks_exhaustion() -> None:
    request = assessment_request()
    certificates = certificates_for(
        request,
        {
            "count": ClosureAssessmentStatus.FAIL_TO_CLOSE,
            "multiset": ClosureAssessmentStatus.FAIL_TO_CLOSE,
            "set": ClosureAssessmentStatus.DEFER,
        },
    )

    assessment = WeakerModelExhaustionGate.assess(
        request=request, certificates=certificates
    )

    assert assessment.status is WeakerModelExhaustionStatus.EXHAUSTION_UNDETERMINED
    assert assessment.deferred_models == ("set",)
    assert assessment.is_weaker_model_exhaustion is False


def test_the_aggregate_does_not_depend_on_certificate_order() -> None:
    request = assessment_request()
    certificates = certificates_for(
        request,
        {
            "count": ClosureAssessmentStatus.DEFER,
            "multiset": ClosureAssessmentStatus.CLOSE,
            "set": ClosureAssessmentStatus.FAIL_TO_CLOSE,
        },
    )

    forward = WeakerModelExhaustionGate.assess(
        request=request, certificates=certificates
    )
    reversed_order = WeakerModelExhaustionGate.assess(
        request=request, certificates=tuple(reversed(certificates))
    )

    assert forward.status is reversed_order.status
    assert forward.closing_models == reversed_order.closing_models
    assert forward.deferred_models == reversed_order.deferred_models


def test_every_exhaustion_status_is_reachable() -> None:
    request = assessment_request()
    reached = {
        WeakerModelExhaustionGate.assess(
            request=request, certificates=certificates_for(request, outcomes)
        ).status
        for outcomes in (
            dict.fromkeys(CONE, ClosureAssessmentStatus.FAIL_TO_CLOSE),
            {
                "count": ClosureAssessmentStatus.CLOSE,
                "multiset": ClosureAssessmentStatus.FAIL_TO_CLOSE,
                "set": ClosureAssessmentStatus.FAIL_TO_CLOSE,
            },
            {
                "count": ClosureAssessmentStatus.DEFER,
                "multiset": ClosureAssessmentStatus.FAIL_TO_CLOSE,
                "set": ClosureAssessmentStatus.FAIL_TO_CLOSE,
            },
        )
    }

    assert reached == set(WeakerModelExhaustionStatus)


def test_a_missing_model_is_refused_and_never_read_as_failure_to_close() -> None:
    request = assessment_request()
    certificates = certificates_for(
        request,
        {
            "count": ClosureAssessmentStatus.FAIL_TO_CLOSE,
            "multiset": ClosureAssessmentStatus.FAIL_TO_CLOSE,
        },
    )

    with pytest.raises(WeakerModelExhaustionError, match="never a failure to close"):
        WeakerModelExhaustionGate.assess(request=request, certificates=certificates)


def test_an_empty_certificate_set_is_refused() -> None:
    with pytest.raises(WeakerModelExhaustionError, match="exactly cover"):
        WeakerModelExhaustionGate.assess(request=assessment_request(), certificates=())


def test_a_duplicated_model_is_refused() -> None:
    request = assessment_request()
    certificates = all_failing(request) + (
        certificate_for(request, "count", ClosureAssessmentStatus.CLOSE),
    )

    with pytest.raises(WeakerModelExhaustionError, match="twice"):
        WeakerModelExhaustionGate.assess(request=request, certificates=certificates)


def test_a_certificate_from_another_request_is_refused() -> None:
    request = assessment_request()
    other = assessment_request()
    certificates = all_failing(request)[:-1] + (
        certificate_for(other, "set", ClosureAssessmentStatus.FAIL_TO_CLOSE),
    )

    with pytest.raises(WeakerModelExhaustionError, match="this exact"):
        WeakerModelExhaustionGate.assess(request=request, certificates=certificates)


def test_a_non_certificate_is_refused() -> None:
    with pytest.raises(WeakerModelExhaustionError, match="gate-issued"):
        WeakerModelExhaustionGate.assess(
            request=assessment_request(),
            certificates=(object(),),  # type: ignore[arg-type]
        )


def test_an_unauthorized_request_is_refused() -> None:
    with pytest.raises(WeakerModelExhaustionError, match="authorized assessment"):
        WeakerModelExhaustionGate.assess(
            request=object(),  # type: ignore[arg-type]
            certificates=(),
        )


def test_an_unissued_assessment_is_refused() -> None:
    request = assessment_request()

    with pytest.raises(WeakerModelExhaustionError, match="must be issued by"):
        WeakerModelExhaustionAssessment(
            request=request,
            certificates=all_failing(request),
            status=WeakerModelExhaustionStatus.LICENSED_WEAKER_MODELS_EXHAUSTED,
            reason="forged",
            closing_models=(),
            deferred_models=(),
        )


def test_outcome_counts_include_every_declared_outcome_at_zero() -> None:
    request = assessment_request()

    assessment = WeakerModelExhaustionGate.assess(
        request=request, certificates=all_failing(request)
    )

    assert set(assessment.outcome_counts) == set(ClosureAssessmentStatus)
    assert assessment.outcome_counts[ClosureAssessmentStatus.CLOSE] == 0
    assert assessment.outcome_counts[ClosureAssessmentStatus.FAIL_TO_CLOSE] == len(CONE)
    assert sum(assessment.outcome_counts.values()) == len(assessment.certificates)


def test_the_counts_are_properties_not_written_fields() -> None:
    assert isinstance(WeakerModelExhaustionAssessment.outcome_counts, property)
    assert isinstance(
        WeakerModelExhaustionAssessment.is_weaker_model_exhaustion, property
    )


def test_exhaustion_is_still_not_independent_closure() -> None:
    request = assessment_request()

    assessment = WeakerModelExhaustionGate.assess(
        request=request, certificates=all_failing(request)
    )

    assert assessment.is_independent_closure is False


def test_the_gate_accepts_no_status_or_reason_from_its_caller() -> None:
    import inspect

    parameters = inspect.signature(WeakerModelExhaustionGate.assess).parameters

    assert set(parameters) == {"request", "certificates"}


def test_this_gate_issues_no_verdict_candidate_or_freeze() -> None:
    request = assessment_request()
    assessment = WeakerModelExhaustionGate.assess(
        request=request, certificates=all_failing(request)
    )

    for forbidden in ("verdict", "birth_candidate", "freeze", "traditional_name", "e0"):
        assert not hasattr(assessment, forbidden)


def test_the_test_model_is_not_part_of_the_cone_to_be_exhausted() -> None:
    spec = specification()

    assert spec.birth_query.test_model not in spec.frozen_weaker_models


def test_a_record_under_the_weaker_model_role_is_what_feeds_this_gate() -> None:
    request = assessment_request()
    certificate = certificate_for(
        request, "count", ClosureAssessmentStatus.FAIL_TO_CLOSE
    )

    assert certificate.record.role is BirthEvaluatorRole.WEAKER_MODEL
