"""الرفعُ التجريبيُّ يختبر الضرورةَ ولا يشهد بها؛ وبذرتُه ليست البذرةَ الدائمة.

    ClosedFractalNode + ExperimentalLiftPermit → ExperimentalNextScaleSeed
    ExperimentalNextScaleSeed ≠ NextScaleSeed

و`ScaleNecessityCertificate` في النواة تبقى مغلقةً كما هي؛ ولا يفتحها نجاحُ
تشغيلٍ تجريبيٍّ ولا تراكمُ شواهده.

تسجيلٌ لا سلطة: لا ترخيصَ، ولا رتبةَ دائمة، ولا حكمَ كفاية.
"""

from __future__ import annotations

import pytest
from experiment_cases import (
    LOWER_REF,
    UPPER_REF,
    build_run,
    issue_permit,
)

from alghanem.fractal_experiment import (
    ExperimentalAuthorityError,
    ExperimentalFractalAuthority,
    ExperimentalLiftError,
    ExperimentalLiftStatus,
    ExperimentalNextScaleSeed,
    issue_experimental_lift_permit,
)
from alghanem.fractal_generation import (
    LiftError,
    LiftGate,
    LiftStatus,
    NextScaleSeed,
    ScaleNecessityCertificate,
)


def test_the_experimental_lift_issues_its_own_seed() -> None:
    run = build_run("run.lift")
    assert run.lift.status is ExperimentalLiftStatus.EXPERIMENTAL_SEED_ISSUED
    seed = run.lift.experimental_seed
    assert isinstance(seed, ExperimentalNextScaleSeed)
    assert seed.source_scale_ref == LOWER_REF
    assert seed.target_scale_ref == UPPER_REF


def test_the_experimental_seed_is_not_the_permanent_seed() -> None:
    run = build_run("run.lift")
    seed = run.lift.experimental_seed
    assert seed is not None
    assert not isinstance(seed, NextScaleSeed)
    assert ExperimentalNextScaleSeed is not NextScaleSeed
    assert not issubclass(ExperimentalNextScaleSeed, NextScaleSeed)


def test_the_experimental_seed_has_no_conversion_to_the_permanent_seed() -> None:
    run = build_run("run.lift")
    seed = run.lift.experimental_seed
    assert seed is not None
    for name in dir(seed):
        lowered = name.lower()
        assert "as_next_scale_seed" not in lowered
        assert "to_next_scale" not in lowered
        assert "promote" not in lowered
        assert "license" not in lowered
        assert "certify" not in lowered


def test_the_experimental_seed_carries_the_necessity_claim_as_under_test() -> None:
    run = build_run("run.lift")
    seed = run.lift.experimental_seed
    assert seed is not None
    assert "يُدَّعى" in seed.necessity_claim_under_test
    assert not hasattr(seed, "necessity_certificate")
    assert not hasattr(seed, "proved_necessity")


def test_the_sealed_certificate_of_the_core_is_still_unissuable() -> None:
    with pytest.raises((LiftError, TypeError)):
        ScaleNecessityCertificate(  # type: ignore[call-arg]
            requirement=None,
            exhaustion=None,
            issuance=None,
        )


def test_a_successful_experimental_run_does_not_open_the_permanent_seed() -> None:
    run = build_run("run.lift")
    assert run.lift.status is ExperimentalLiftStatus.EXPERIMENTAL_SEED_ISSUED
    assert LiftGate.assess.__doc__ is not None
    for status in LiftStatus:
        assert status is LiftStatus.DEFERRED_NO_SCALE_NECESSITY_AUTHORITY


def test_a_lift_permit_is_refused_outside_an_active_run() -> None:
    authority = ExperimentalFractalAuthority(authority_id="authority.synthetic")
    permit = issue_permit(authority, run_id="run.a")
    with pytest.raises(ExperimentalAuthorityError):
        issue_experimental_lift_permit(
            authority=authority,
            permit=permit,
            run_id="run.a",
            source_scale_ref=LOWER_REF,
            target_scale_ref=UPPER_REF,
            necessity_claim_under_test="دعوى تحت الاختبار",
        )


def test_a_lift_permit_is_refused_when_the_run_permit_forbids_lifting() -> None:
    authority = ExperimentalFractalAuthority(authority_id="authority.synthetic")
    permit = authority.activate(
        issue_permit(authority, run_id="run.b", permitted_experimental_lift=False)
    )
    with pytest.raises(ExperimentalLiftError):
        issue_experimental_lift_permit(
            authority=authority,
            permit=permit,
            run_id="run.b",
            source_scale_ref=LOWER_REF,
            target_scale_ref=UPPER_REF,
            necessity_claim_under_test="دعوى تحت الاختبار",
        )


def test_the_experimental_seed_is_not_written_by_a_caller() -> None:
    with pytest.raises(ExperimentalLiftError):
        ExperimentalNextScaleSeed(
            seed_id="seed.forged",
            experiment_id="experiment.synthetic",
            run_id="run.a",
            lift_permit_content_id="x" * 64,
            source_scale_ref=LOWER_REF,
            target_scale_ref=UPPER_REF,
            closed_node_content_id="y" * 64,
            necessity_claim_under_test="دعوى تحت الاختبار",
            carried_residuals=(),
            issuance=object(),  # type: ignore[arg-type]
        )
