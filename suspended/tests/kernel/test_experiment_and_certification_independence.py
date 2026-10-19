"""G0.EX: permission to experiment and certification, read as two free axes.

`PermissionToExperimentAndCertificationAreIndependent` is a derivation of four
laws already enforced elsewhere, so nothing here introduces an authority or a
gate. What is asserted is the pair of directions that the four, read singly, do
not force a reader to notice::

    permitting a run      -/->  certifying what was run
    withholding a licence -/->  forbidding the run

The witness is the three authority signatures rather than prose. `run` takes no
certificate and no verdict and therefore cannot require one; `admit` takes a
`BirthCertificate` and therefore cannot waive one; `assess` takes no run record
and therefore is not reachable by a successful run.

One thing is deliberately **not** asserted: that a finished run leaves the
birth readings untouched forever. A run may become an `ExperimentalEvidenceOffer`
and travel the acquisition chain into a *new* licensed assessment, where the
readings are derived again. The claim here is only about what the run itself
confers, and about which arguments each authority accepts.
"""

import inspect

import pytest
from test_birth_certificate import (  # type: ignore[import-not-found]
    closure_decision,
    verdict_for,
)
from test_experimental import (  # type: ignore[import-not-found]
    bound,
    implementation_for,
)

from alghanem.kernel.birth_certificate import (
    BirthCertificate,
    BirthCertificateAuthorityError,
    ConstitutionalBirthAuthority,
    ExecutiveAdmissionGate,
    derive_preventer_findings,
)
from alghanem.kernel.experimental import (
    EXPERIMENTAL_NAMED_LAWS,
    ExperimentalAuthority,
    ExperimentalAuthorityError,
    ExperimentalOutcomeStatus,
    ExperimentalRunContext,
    ExperimentalRunRecord,
)
from alghanem.kernel.trace import Trace

JOINT_LAW = "PermissionToExperimentAndCertificationAreIndependent"
DERIVED_FROM = (
    "ExperimentalSuccessIsNotBirth",
    "ExperimentalFailureIsNotNoBirth",
    "NoBornEntityIsRequiredToRunAnExperiment",
    "ExperimentalRunIsNotExecutionOfABornEntity",
)


def parameter_names(function: object) -> set[str]:
    return set(inspect.signature(function).parameters) - {"self"}  # type: ignore[arg-type]


# --- direction one: not certified, still runnable ------------------------------


def test_running_an_experiment_accepts_no_certificate_and_no_verdict() -> None:
    """An argument that does not exist cannot be demanded."""

    assert parameter_names(ExperimentalAuthority.run) == {
        "run_id",
        "bound_request",
        "implementation",
    }
    annotations = {
        name: str(parameter.annotation)
        for name, parameter in inspect.signature(
            ExperimentalAuthority.run
        ).parameters.items()
    }
    joined = " ".join(annotations.values())
    for barred in ("BirthCertificate", "BirthVerdictDecision", "ExecutableEntity"):
        assert barred not in joined


def test_using_what_was_born_demands_the_certificate_that_running_does_not() -> None:
    """The two authorities read in one test, so the contrast is measured."""

    assert "certificate" in parameter_names(ExecutiveAdmissionGate.admit)
    assert "certificate" not in parameter_names(ExperimentalAuthority.run)

    record = ExperimentalAuthority(authority_id="lab").run(
        run_id="run-without-a-certificate",
        bound_request=bound(),
        implementation=implementation_for(frozenset()),
    )
    assert record.outcome_status is ExperimentalOutcomeStatus.COMPLETED

    with pytest.raises(BirthCertificateAuthorityError):
        ExecutiveAdmissionGate.admit(
            admission_id="admission",
            certificate=None,  # type: ignore[arg-type]
        )


def test_a_completed_run_and_an_uncertified_birth_stand_together() -> None:
    """One measured state holding both halves of the criterion at once."""

    record = ExperimentalAuthority(authority_id="lab").run(
        run_id="run-1",
        bound_request=bound(),
        implementation=implementation_for(frozenset({"c2"})),
    )
    closure = closure_decision()
    assessment = ConstitutionalBirthAuthority(authority_id="authority").assess(
        assessment_id="assessment", verdict=verdict_for(closure), closure=closure
    )

    assert record.outcome_status is ExperimentalOutcomeStatus.COMPLETED
    assert assessment.certificate is None
    assert {finding.preventer.name for finding in assessment.findings if finding.holds}


def test_a_failed_run_is_refused_certification_and_not_refused_running() -> None:
    def raising(
        context: ExperimentalRunContext, input_content: str
    ) -> tuple[str, Trace]:
        raise RuntimeError("the implementation gave up")

    record = ExperimentalAuthority(authority_id="lab").run(
        run_id="failed-run", bound_request=bound(), implementation=raising
    )

    assert record.records_failure is True
    assert record.confers_birth is False
    assert not isinstance(record, BirthCertificate)


# --- direction two: permitted to run, still not certified ----------------------


def test_a_run_record_is_not_an_admissible_argument_to_any_certifying_surface() -> None:
    record = ExperimentalAuthority(authority_id="lab").run(
        run_id="run-1",
        bound_request=bound(),
        implementation=implementation_for(frozenset()),
    )
    closure = closure_decision()
    authority = ConstitutionalBirthAuthority(authority_id="authority")

    with pytest.raises(BirthCertificateAuthorityError):
        authority.assess(
            assessment_id="assessment",
            verdict=record,  # type: ignore[arg-type]
            closure=closure,
        )
    with pytest.raises(BirthCertificateAuthorityError):
        ExecutiveAdmissionGate.admit(
            admission_id="admission",
            certificate=record,  # type: ignore[arg-type]
        )


def test_the_derivation_reads_five_declared_readings_and_no_run_record() -> None:
    """A run cannot clear a preventer *here*; a later licensed assessment may.

    The readings are re-derived from gate-issued decisions on every assessment,
    so this asserts which inputs the derivation accepts -- not that a run is
    without consequence once its offer has travelled the acquisition chain.
    """

    assert parameter_names(derive_preventer_findings) == {
        "verdict_status",
        "closure_status",
        "exhaustion_status",
        "survival_status",
        "evidence_mode",
    }


def test_an_experimental_refusal_is_not_a_certification_refusal() -> None:
    assert not issubclass(ExperimentalAuthorityError, BirthCertificateAuthorityError)
    assert not issubclass(BirthCertificateAuthorityError, ExperimentalAuthorityError)
    assert not issubclass(ExperimentalRunRecord, BirthCertificate)
    assert not issubclass(BirthCertificate, ExperimentalRunRecord)


# --- the joint law -------------------------------------------------------------


def test_the_joint_law_is_deposited_as_a_derivation_of_the_four() -> None:
    text = EXPERIMENTAL_NAMED_LAWS[JOINT_LAW]

    assert text.startswith(f"{JOINT_LAW}:")
    for source_law in DERIVED_FROM:
        assert source_law in text
        assert source_law in EXPERIMENTAL_NAMED_LAWS


def test_the_joint_law_added_no_authority_surface_and_no_new_argument() -> None:
    surface = {name for name in vars(ExperimentalAuthority) if not name.startswith("_")}

    assert surface == {"authority_id", "run"}
    assert parameter_names(ExperimentalAuthority.run) == {
        "run_id",
        "bound_request",
        "implementation",
    }
    assert {
        name for name in vars(ConstitutionalBirthAuthority) if not name.startswith("_")
    } == {"assess", "authority_id"}
