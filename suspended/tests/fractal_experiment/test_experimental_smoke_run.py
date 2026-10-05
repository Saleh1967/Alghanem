"""أوّلُ تشغيلٍ عامٍّ تحت سلطةٍ تجريبيّةٍ مؤقّتة؛ تخليقيٌّ محايدٌ لا لغةَ فيه.

    FrozenSyntheticInput
      → ExperimentalRunPermit → ACTIVE
      → FGEN transition
      → ExperimentalLiftPermit → ExperimentalNextScaleSeed
      → FractalExperimentalWitness
      → REVOKED

ثمّ يُقرأ الأثرُ فيُرى: `NextScaleSeed == unreachable` و`License == absent`.

تسجيلٌ لا سلطة: لا ترخيصَ، ولا رتبةَ دائمة، ولا حكمَ كفاية.
"""

from __future__ import annotations

import pytest
from experiment_cases import (
    BINDING,
    FROZEN_ENTRY,
    LOWER_REF,
    OPERATION,
    SEED_NODE,
    SyntheticExperimentalRun,
    build_run,
)

from alghanem.fractal_experiment import (
    ExperimentalFractalTransition,
    ExperimentalLiftStatus,
    ExperimentalPermitState,
    ExperimentalStanding,
)
from alghanem.fractal_generation import (
    ClosedFractalNode,
    FractalMovementKind,
    FractalTransition,
    NextScaleSeed,
)


@pytest.fixture(scope="module")
def run() -> SyntheticExperimentalRun:
    """الدورةُ التجريبيّةُ كاملةً، مُشغَّلةً مرّةً واحدةً ومقروءةً في الاختبارات."""

    return build_run("run.smoke")


def test_the_run_opens_upon_a_frozen_binding_not_upon_free_input(
    run: SyntheticExperimentalRun,
) -> None:
    assert run.permit.binding_content_id == BINDING.content_id
    assert BINDING.input_ids == {FROZEN_ENTRY.input_id}


def test_the_core_transition_is_wrapped_not_modified(
    run: SyntheticExperimentalRun,
) -> None:
    wrapper = run.experimental_transition
    assert isinstance(wrapper, ExperimentalFractalTransition)
    assert isinstance(wrapper.transition, FractalTransition)
    assert not isinstance(wrapper, FractalTransition)
    assert (
        wrapper.movement_kind is FractalMovementKind.IDENTITY_PRESERVING_TRANSFORMATION
    )
    assert wrapper.operation == OPERATION
    assert wrapper.scale_before == LOWER_REF
    assert wrapper.scale_after == LOWER_REF


def test_the_experimental_transition_names_its_permit_and_its_frozen_input(
    run: SyntheticExperimentalRun,
) -> None:
    wrapper = run.experimental_transition
    assert wrapper.permit_content_id == run.permit.content_id
    assert wrapper.frozen_input_id == FROZEN_ENTRY.input_id
    assert wrapper.frozen_input_content_id == FROZEN_ENTRY.content_id
    assert wrapper.residuals


def test_the_node_closes_and_the_experimental_seed_issues(
    run: SyntheticExperimentalRun,
) -> None:
    assert isinstance(run.closed, ClosedFractalNode)
    assert run.closed.trace.output_content_id == run.closed.node.content_id
    assert run.lift.status is ExperimentalLiftStatus.EXPERIMENTAL_SEED_ISSUED
    assert run.lift.experimental_seed is not None
    assert (
        run.lift.experimental_seed.closed_node_content_id == run.closed.node.content_id
    )


def test_the_run_ends_in_a_witness_and_the_permit_is_revoked(
    run: SyntheticExperimentalRun,
) -> None:
    assert run.witness.standing is ExperimentalStanding.OBSERVED_SUPPORT
    assert run.witness.identity_before == SEED_NODE.content_id
    assert run.final_state is ExperimentalPermitState.REVOKED


def test_no_permanent_seed_and_no_license_came_out_of_the_run(
    run: SyntheticExperimentalRun,
) -> None:
    seed = run.lift.experimental_seed
    assert seed is not None
    assert not isinstance(seed, NextScaleSeed)
    for produced in (run.witness, run.bundle, run.experimental_transition, seed):
        assert not isinstance(produced, NextScaleSeed)
        assert type(produced).__name__ not in (
            "License",
            "LicensedPattern",
            "LicensedTransition",
            "LicensedScaleLift",
            "ArabicRuleLicense",
        )


def test_the_run_is_reproducible_from_its_frozen_content() -> None:
    first = build_run("run.repeat")
    second = build_run("run.repeat")
    assert first.witness.content_id == second.witness.content_id
    assert first.bundle.content_id == second.bundle.content_id
    assert first.permit.content_id == second.permit.content_id
