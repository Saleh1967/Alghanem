"""شواهدُ G0.FLT-1 قبل تشغيله: أمانةُ النقل مُشتقّة، والتسجيلُ مُودَعٌ بلا قراءة."""

from __future__ import annotations

import importlib.util

import pytest

from alghanem.arabic import flt1_hypothesis as hypothesis_module
from alghanem.arabic.flt1_hypothesis import (
    FLT1_HYPOTHESIS_TEXT,
    FLT1_TEXT_DIGEST,
    HIGHER_CENTER_CONDITIONS,
    REQUIRED_NOTATION_SITES,
    FidelityStanding,
    FLT1HypothesisError,
    NotationSite,
    derive_fidelity_report,
    flt1_text_digest,
)
from alghanem.arabic.flt1_preregistration import (
    DECLARED_HYPOTHESES,
    FLT1_FROZEN_SURFACES,
    FLT1_PREREGISTRATION_DIGEST,
    HIGHER_CENTER_CONDITION_DECLARATIONS,
    WEAKER_REPRESENTATIONS,
    FLT1PreregistrationError,
    flt1_preregistration_digest,
    hypothesis_named,
)
from alghanem.arabic.fractal_transition_preregistration import FROZEN_CASES


def test_every_decisive_notation_site_is_present_in_the_deposited_text() -> None:
    report = derive_fidelity_report()
    assert report.standing is FidelityStanding.ALL_REQUIRED_SITES_PRESENT
    assert report.absent_site_ids == ()
    assert report.is_fit_to_be_run is True
    assert len(report.sites) == len(REQUIRED_NOTATION_SITES)
    for reading in report.sites:
        assert reading.is_present is True
        assert reading.what_its_absence_invalidates.strip()


def test_an_absent_site_makes_the_registration_unfit_before_it_runs() -> None:
    report = derive_fidelity_report("نصٌّ فقد مواضعَه كلَّها")
    assert report.standing is FidelityStanding.A_REQUIRED_SITE_IS_ABSENT
    assert report.is_fit_to_be_run is False
    assert len(report.absent_site_ids) == len(REQUIRED_NOTATION_SITES)


def test_the_import_guard_refuses_a_text_that_lost_a_site(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(hypothesis_module, "FLT1_HYPOTHESIS_TEXT", "نصٌّ بلا موضعٍ واحد")
    with pytest.raises(FLT1HypothesisError):
        hypothesis_module._refuse_a_text_that_lost_a_required_site()


def test_the_text_digest_is_derived_from_the_text_not_written_beside_it() -> None:
    assert flt1_text_digest() == FLT1_TEXT_DIGEST
    assert flt1_text_digest(FLT1_HYPOTHESIS_TEXT + " ") != FLT1_TEXT_DIGEST


def test_the_count_is_a_prediction_and_never_enters_the_equivalence() -> None:
    h1 = hypothesis_named("H1-carrier-quotient")
    assert "28" in h1.predicted_result
    assert "28" not in h1.derivation_before_the_test
    assert h1.what_would_falsify_it.strip()


def test_every_hypothesis_names_what_would_falsify_it_and_what_lifts_it() -> None:
    assert len(DECLARED_HYPOTHESES) == 6
    ids = [item.hypothesis_id for item in DECLARED_HYPOTHESES]
    assert len(ids) == len(set(ids))
    for declaration in DECLARED_HYPOTHESES:
        assert declaration.what_would_falsify_it.strip()
        assert declaration.underpowered_condition.strip()
        assert declaration.what_would_lift_underpowered.strip()


def test_an_undeclared_hypothesis_is_refused_rather_than_created() -> None:
    with pytest.raises(FLT1PreregistrationError):
        hypothesis_named("H7-invented-after-the-result")


def test_the_three_weaker_representations_are_registered_before_the_run() -> None:
    assert len(WEAKER_REPRESENTATIONS) == 3
    assert {item.model_id for item in WEAKER_REPRESENTATIONS} == {
        "carrier-alone",
        "state-alone",
        "unordered-carrier-state-pair",
    }
    for item in WEAKER_REPRESENTATIONS:
        assert item.what_it_deliberately_ignores.strip()
        assert item.why_a_tie_defeats_the_claim.strip()


def test_the_four_conditions_match_the_frozen_text_in_name_and_order() -> None:
    declared = tuple(item.condition for item in HIGHER_CENTER_CONDITION_DECLARATIONS)
    assert declared == HIGHER_CENTER_CONDITIONS
    assert declared == ("Reconstruction", "Minimality", "NoBypass", "Closure")
    for item in HIGHER_CENTER_CONDITION_DECLARATIONS:
        assert item.what_would_fail_it.strip()


def test_no_frozen_surface_was_already_read_in_flt0() -> None:
    seen = {case.surface for case in FROZEN_CASES}
    chosen = {item.surface for item in FLT1_FROZEN_SURFACES}
    assert chosen.isdisjoint(seen)
    assert len(chosen) == len(FLT1_FROZEN_SURFACES)


def test_every_frozen_surface_states_why_it_was_included() -> None:
    for item in FLT1_FROZEN_SURFACES:
        assert item.why_it_is_included.strip()


def test_the_preregistration_digest_is_derived_not_transcribed() -> None:
    assert flt1_preregistration_digest() == FLT1_PREREGISTRATION_DIGEST


def test_a_site_without_a_literal_is_refused() -> None:
    with pytest.raises(FLT1HypothesisError):
        NotationSite(
            site_id="empty",
            literal="  ",
            what_it_decides="x",
            what_its_absence_invalidates="y",
        )


def test_no_readout_module_exists_for_flt1_in_this_deposit() -> None:
    assert importlib.util.find_spec("alghanem.arabic.flt1_readout") is None
    assert not hasattr(hypothesis_module, "read_flt1")


def test_the_registration_issues_no_verdict_vocabulary_of_its_own() -> None:
    from alghanem.arabic import flt1_preregistration as prereg_module

    assert not hasattr(prereg_module, "FLT1Verdict")
    assert not hasattr(prereg_module, "read_hypothesis")
