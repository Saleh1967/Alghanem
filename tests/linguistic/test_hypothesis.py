"""نصُّ الفرضية مُجمَّدٌ، وأمانتُه مُشتَقّةٌ موضعًا بموضعٍ قبل أيّ قراءة."""

from __future__ import annotations

import pytest

from alghanem.linguistic.hypothesis import (
    NISBAH_HYPOTHESIS_NAMED_RESIDUALS,
    NISBAH_HYPOTHESIS_TEXT,
    NISBAH_TEXT_DIGEST,
    REQUIRED_NOTATION_SITES,
    FidelityStanding,
    NisbahHypothesisError,
    NotationSite,
    derive_fidelity_report,
    nisbah_text_digest,
)


def test_every_required_site_is_present_in_the_deposited_text() -> None:
    report = derive_fidelity_report()
    assert report.standing is FidelityStanding.ALL_REQUIRED_SITES_PRESENT
    assert report.absent_site_ids == ()
    assert report.is_fit_to_be_run


def test_a_text_that_lost_a_decisive_site_is_unfit_to_be_run() -> None:
    mutilated = NISBAH_HYPOTHESIS_TEXT.replace(r"\boxed{TermAnchor}", "")
    report = derive_fidelity_report(mutilated)
    assert report.standing is FidelityStanding.A_REQUIRED_SITE_IS_ABSENT
    assert "the-term-anchor" in report.absent_site_ids
    assert not report.is_fit_to_be_run


def test_the_three_level_correction_is_a_checked_site_not_a_promise() -> None:
    site_ids = tuple(site.site_id for site in REQUIRED_NOTATION_SITES)
    assert "the-three-levels" in site_ids
    without_levels = NISBAH_HYPOTHESIS_TEXT.replace(r"\Sigma_{AR}", "")
    assert "the-three-levels" in derive_fidelity_report(without_levels).absent_site_ids


def test_the_closure_and_ifadah_sites_are_separate_requirements() -> None:
    site_ids = tuple(site.site_id for site in REQUIRED_NOTATION_SITES)
    assert "closure-yields-pre-ifadah" in site_ids
    assert "ifadah-needs-force-and-context" in site_ids


def test_the_digest_is_derived_from_the_text_not_written_beside_it() -> None:
    assert NISBAH_TEXT_DIGEST == nisbah_text_digest(NISBAH_HYPOTHESIS_TEXT)
    assert nisbah_text_digest(NISBAH_HYPOTHESIS_TEXT + " ") != NISBAH_TEXT_DIGEST


def test_an_empty_text_has_no_digest() -> None:
    with pytest.raises(NisbahHypothesisError):
        nisbah_text_digest("   ")


def test_a_site_without_a_literal_is_refused() -> None:
    with pytest.raises(NisbahHypothesisError):
        NotationSite(
            site_id="empty",
            literal="  ",
            what_it_decides="لا شيء",
            what_its_absence_invalidates="لا شيء",
        )


def test_the_named_residuals_are_declared_not_folded() -> None:
    assert len(NISBAH_HYPOTHESIS_NAMED_RESIDUALS) == 4
    assert all(residual.strip() for residual in NISBAH_HYPOTHESIS_NAMED_RESIDUALS)
