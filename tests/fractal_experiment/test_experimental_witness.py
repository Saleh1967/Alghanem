"""الشاهدُ يرصد ولا يحكم، والحزمةُ تجمع ولا تُرجِّح.

    ExperimentalPASS → Witness   (لا ترخيص)
    FAIL → Witness، UNDERPOWERED → Witness
    WitnessBundle ≠ EvidenceSufficiencyAssessment

تسجيلٌ لا سلطة: لا ترخيصَ، ولا رتبةَ دائمة، ولا حكمَ كفاية.
"""

from __future__ import annotations

import pytest
from experiment_cases import (
    FROZEN_ENTRY,
    LOWER_REF,
    PREREGISTRATION_CONTENT_ID,
    build_run,
)

from alghanem.fractal_experiment import (
    NO_SUFFICIENCY_ASSESSMENT_AUTHORITY,
    ExperimentalStanding,
    FractalExperimentalWitness,
    WitnessBundle,
    WitnessBundleError,
    WitnessError,
    WitnessSufficiencyContract,
)
from alghanem.fractal_generation import FractalResidual, FractalResidualKind


def _witness(
    standing: ExperimentalStanding, *, witness_id: str, permit_content_id: str
) -> FractalExperimentalWitness:
    return FractalExperimentalWitness(
        witness_id=witness_id,
        experiment_id="experiment.synthetic",
        run_id="run.other",
        permit_content_id=permit_content_id,
        frozen_input_content_id=FROZEN_ENTRY.content_id,
        preregistration_content_id=PREREGISTRATION_CONTENT_ID,
        standing=standing,
        source_scale=LOWER_REF,
        identity_before="a" * 64,
        identity_after="b" * 64,
        movement_kind="no_movement_observed",
        observed_difference="فرقٌ مرصودٌ بلا حكمٍ عليه",
        reconstruction_observation="إعادةُ البناء خالفت المرصود",
        closure_observation="لم تُغلَق العقدةُ عند مقياسها",
        residuals=(
            FractalResidual(
                kind=FractalResidualKind.UNRESOLVED_DIFFERENCE,
                subject_id=witness_id,
                reason="بقيّةٌ مرصودةٌ لا تُمحى",
            ),
        ),
    )


def test_a_successful_run_yields_a_witness_not_a_license() -> None:
    run = build_run("run.witness")
    assert run.witness.standing is ExperimentalStanding.OBSERVED_SUPPORT
    for name in dir(run.witness):
        lowered = name.lower()
        assert "license" not in lowered
        assert "licence" not in lowered
        assert "verdict" not in lowered
        assert "rank" not in lowered
        assert "score" not in lowered


def test_the_witness_keeps_its_residuals_and_its_frozen_identities() -> None:
    run = build_run("run.witness")
    assert run.witness.residuals
    assert run.witness.frozen_input_content_id == FROZEN_ENTRY.content_id
    assert run.witness.permit_content_id == run.permit.content_id
    assert run.witness.preregistration_content_id == PREREGISTRATION_CONTENT_ID
    assert run.witness.trace is not None


def test_a_witness_refuses_the_vocabulary_of_rank() -> None:
    for word in ("LICENSED", "TRUE", "NECESSARY", "PROVED"):
        with pytest.raises(WitnessError):
            FractalExperimentalWitness(
                witness_id="witness.rank",
                experiment_id="experiment.synthetic",
                run_id="run.rank",
                permit_content_id="c" * 64,
                frozen_input_content_id=FROZEN_ENTRY.content_id,
                preregistration_content_id=PREREGISTRATION_CONTENT_ID,
                standing=ExperimentalStanding.OBSERVED_SUPPORT,
                source_scale=LOWER_REF,
                identity_before="a" * 64,
                identity_after="b" * 64,
                movement_kind="identity_preserving_transformation",
                observed_difference=f"the claim is {word}",
                reconstruction_observation="إعادةُ البناء طابقت المرصود",
                closure_observation="أُغلقت العقدةُ عند مقياسها",
            )


def test_refutation_and_underpoweredness_are_witnesses_too() -> None:
    run = build_run("run.witness")
    refutation = _witness(
        ExperimentalStanding.OBSERVED_REFUTATION,
        witness_id="witness.refutation",
        permit_content_id=run.permit.content_id,
    )
    underpowered = _witness(
        ExperimentalStanding.UNDERPOWERED,
        witness_id="witness.underpowered",
        permit_content_id=run.permit.content_id,
    )
    failure = _witness(
        ExperimentalStanding.RUN_FAILURE,
        witness_id="witness.failure",
        permit_content_id=run.permit.content_id,
    )
    bundle = WitnessBundle(
        bundle_id="bundle.mixed",
        target_claim_ref="دعوى تحت الاختبار",
        preregistration_ref=PREREGISTRATION_CONTENT_ID,
        witnesses=(run.witness, refutation, underpowered, failure),
        input_coverage=(FROZEN_ENTRY.input_id,),
    )
    assert len(bundle.positive_observations) == 1
    assert len(bundle.refuting_observations) == 1
    assert len(bundle.underpowered_observations) == 1
    assert len(bundle.run_failure_observations) == 1
    assert len(bundle.residual_union) == 4


def test_the_bundle_carries_no_verdict_and_no_rank() -> None:
    run = build_run("run.witness")
    for name in dir(run.bundle):
        lowered = name.lower()
        assert "verdict" not in lowered
        assert "license" not in lowered
        assert "licence" not in lowered
        assert "rank" not in lowered
        assert "score" not in lowered
        assert "sufficient" not in lowered
        assert "winner" not in lowered


def test_the_bundle_names_its_open_sufficiency_gap() -> None:
    run = build_run("run.witness")
    assert NO_SUFFICIENCY_ASSESSMENT_AUTHORITY in run.bundle.authority_gaps
    for gap in run.bundle.authority_gaps:
        assert gap.gap_id.startswith("RES.FGENEX0.")


def test_a_bundle_refuses_a_duplicated_witness_identifier() -> None:
    run = build_run("run.witness")
    with pytest.raises(WitnessBundleError):
        WitnessBundle(
            bundle_id="bundle.duplicate",
            target_claim_ref="دعوى تحت الاختبار",
            preregistration_ref=PREREGISTRATION_CONTENT_ID,
            witnesses=(run.witness, run.witness),
            input_coverage=(FROZEN_ENTRY.input_id,),
        )


def test_a_bundle_refuses_to_be_empty() -> None:
    with pytest.raises(WitnessBundleError):
        WitnessBundle(
            bundle_id="bundle.empty",
            target_claim_ref="دعوى تحت الاختبار",
            preregistration_ref=PREREGISTRATION_CONTENT_ID,
            witnesses=(),
            input_coverage=(),
        )


def test_the_sufficiency_contract_is_a_declaration_without_an_evaluator() -> None:
    contract = WitnessSufficiencyContract(
        contract_id="contract.synthetic",
        target_claim="دعوى تحت الاختبار",
        required_scope="مدًى مُعلَنٌ قبل العدّ",
        independence_criterion="تشغيلاتٌ بمُعرِّفاتٍ متمايزة",
        positive_witness_requirement="نصابٌ يُحدَّد قبل العدّ",
        negative_controls=("ضابطٌ سالبٌ مُعلَن",),
        weaker_model_requirement="بيانُ ما يعجز عنه الأضعف",
        counterexample_policy="النقضُ يُحفَظ ولا يُمحى",
        replication_requirement="إعادةُ التشغيل تُعطي الشواهدَ عينَها",
        reconstruction_requirement="الأثرُ يُعيد بناءَ المخرج",
        residual_tolerance="البقايا تُسمّى ولا تُمحى",
        blocking_residuals=("بقيّةٌ تمنع الإغلاق",),
    )
    assert len(contract.content_id) == 64
    for name in dir(contract):
        lowered = name.lower()
        assert "assess" not in lowered
        assert "evaluate" not in lowered
        assert "measure" not in lowered
        assert "verdict" not in lowered
        assert "license" not in lowered
