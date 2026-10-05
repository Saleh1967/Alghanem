"""شواهدُ معايرة G0.FLT-0: الانحرافُ مُشتَقٌّ، والحكمُ محجوبُ النسبة، والظرفُ مُعلَن."""

from __future__ import annotations

import pytest

from alghanem.arabic import fractal_transition_calibration as calibration_module
from alghanem.arabic.fractal_transition_calibration import (
    CALIBRATION_NAMED_RESIDUALS,
    FLT1_PREREQUISITES,
    REQUESTED_SUCCESS_CONDITION,
    CalibrationStanding,
    FractalCalibrationError,
    RequestedNotationSite,
    derive_capability_envelope,
    derive_verbatim_divergences,
    read_calibration,
)
from alghanem.arabic.fractal_transition_hypothesis import (
    HYPOTHESIS_DIGEST,
    FractalVerdict,
    hypothesis_digest,
)


def test_the_frozen_text_still_carries_the_digest_it_was_read_under() -> None:
    assert hypothesis_digest() == HYPOTHESIS_DIGEST


def test_the_divergence_is_derived_from_the_deposited_text_not_asserted() -> None:
    divergences = derive_verbatim_divergences()
    assert len(divergences) == 1
    divergence = divergences[0]
    assert divergence.site_id == REQUESTED_SUCCESS_CONDITION.site_id
    assert divergence.required_relation == ">"
    assert ">" not in divergence.what_the_frozen_text_carries
    assert "«»" in divergence.what_the_frozen_text_carries


def test_a_divergent_text_makes_the_run_an_invalid_preregistration() -> None:
    reading = read_calibration()
    assert reading.standing is CalibrationStanding.INVALID_PREREGISTRATION
    assert reading.observed_verdict_is_a_hypothesis_judgment is False
    assert reading.withheld_judgment_reason.strip()


def test_the_observed_reading_is_carried_whole_not_erased() -> None:
    reading = read_calibration()
    assert reading.observed_readout.verdict is FractalVerdict.WEAKER_MODEL_RECONSTRUCTS
    assert len(reading.observed_readout.pairs) == 3
    assert reading.degenerate_fields


def test_support_is_unreachable_by_construction_in_this_registration() -> None:
    envelope = derive_capability_envelope()
    assert envelope.unreachable_verdicts == (FractalVerdict.SUPPORTED,)
    assert set(envelope.reachable_verdicts) == {
        FractalVerdict.REFUTED,
        FractalVerdict.UNDERPOWERED,
        FractalVerdict.WEAKER_MODEL_RECONSTRUCTS,
    }
    assert envelope.holdout_pair_count == 0
    assert envelope.holdout_pairs_required_for_support == 3
    assert envelope.is_a_refutation_only_instrument is True


def test_every_named_limit_states_what_it_prevents_and_what_lifts_it() -> None:
    envelope = derive_capability_envelope()
    limit_ids = {limit.limit_id for limit in envelope.limits}
    assert limit_ids == {
        "no-holdout-pair-under-the-frozen-ladder",
        "boolean-agreement-is-not-scale-transport",
        "identity-is-declared-not-verified",
        "frozen-cases-and-pairs-are-now-seen",
    }
    for limit in envelope.limits:
        assert limit.holds is True
        assert limit.what_it_prevents.strip()
        assert limit.how_it_was_derived.strip()
        assert limit.what_would_lift_it.strip()


def test_an_absent_scale_transport_contract_is_derived_not_declared() -> None:
    assert calibration_module._an_independent_scale_transport_is_absent() is True


def test_identity_is_not_read_through_the_invariant_verification_gate() -> None:
    assert (
        calibration_module._identity_is_read_from_an_encoder_not_a_verification_gate()
        is True
    )


def test_the_next_experiment_is_declared_by_name_and_not_executed() -> None:
    assert len(FLT1_PREREQUISITES) == len(set(FLT1_PREREQUISITES))
    assert len(FLT1_PREREQUISITES) >= 6
    assert not hasattr(calibration_module, "read_flt1")
    assert not hasattr(calibration_module, "FLT1_FROZEN_CASES")


def test_a_site_without_a_named_operand_is_refused() -> None:
    with pytest.raises(FractalCalibrationError):
        RequestedNotationSite(
            site_id="empty",
            left_operand="   ",
            required_relation=">",
            right_operand="x",
            what_it_decides="y",
        )


def test_a_missing_operand_pair_is_refused_rather_than_read_as_fidelity(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(calibration_module, "HYPOTHESIS_TEXT", "نصٌّ بلا طرفين")
    with pytest.raises(FractalCalibrationError):
        derive_verbatim_divergences()


def test_a_faithful_text_would_not_be_reported_as_divergent(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    site = REQUESTED_SUCCESS_CONDITION
    monkeypatch.setattr(
        calibration_module,
        "HYPOTHESIS_TEXT",
        f"{site.left_operand}\n\n>\n\n{site.right_operand}",
    )
    assert derive_verbatim_divergences() == ()


def test_the_named_residuals_are_distinct_and_non_empty() -> None:
    assert len(CALIBRATION_NAMED_RESIDUALS) == len(set(CALIBRATION_NAMED_RESIDUALS))
    for note in CALIBRATION_NAMED_RESIDUALS:
        assert note.strip()


def test_the_calibration_refuses_to_run_on_a_repaired_frozen_text(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        calibration_module, "HYPOTHESIS_TEXT", "نصٌّ أُصلِح بعد قراءة نتيجته"
    )
    with pytest.raises(FractalCalibrationError):
        calibration_module._refuse_a_calibration_that_repairs_the_frozen_text()
