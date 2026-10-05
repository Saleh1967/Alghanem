"""شواهدُ `G0.PK-0`: النصُّ المُجمَّد، ومواضعُه الحاسمة، وبقاياه المُسمّاة."""

from __future__ import annotations

import pytest

from alghanem.prior.hypothesis import (
    A_LAYER_THAT_FOUND_A_LAYER_BENEATH_IT_IS_NOT_REFUTED_NOTE,
    NO_READOUT_EXISTS_FOR_PK0_YET_NOTE,
    ONTOLOGICAL_KIND_IS_NOT_LINGUISTIC_ROLE_NOTE,
    PRIOR_HYPOTHESIS_NAMED_RESIDUALS,
    PRIOR_HYPOTHESIS_TEXT,
    PRIOR_TEXT_DIGEST,
    REQUIRED_NOTATION_SITES,
    THE_ALGEBRA_DOES_NOT_CREATE_ITS_OBJECTS_NOTE,
    FidelityStanding,
    NotationSite,
    PriorHypothesisError,
    derive_fidelity_report,
    prior_text_digest,
)


def test_every_required_notation_site_is_present_in_the_deposited_text() -> None:
    report = derive_fidelity_report()
    assert report.standing is FidelityStanding.ALL_REQUIRED_SITES_PRESENT
    assert report.absent_site_ids == ()
    assert report.is_fit_to_be_run


def test_a_text_missing_a_decisive_site_is_unfit_to_be_run() -> None:
    mutilated = PRIOR_HYPOTHESIS_TEXT.replace("NoReadoutExistsForPK0Yet", "")
    report = derive_fidelity_report(mutilated)
    assert report.standing is FidelityStanding.A_REQUIRED_SITE_IS_ABSENT
    assert "no-readout-for-pk0" in report.absent_site_ids
    assert not report.is_fit_to_be_run


def test_the_digest_is_derived_from_the_text_and_not_written_beside_it() -> None:
    assert PRIOR_TEXT_DIGEST == prior_text_digest(PRIOR_HYPOTHESIS_TEXT)
    assert prior_text_digest(PRIOR_HYPOTHESIS_TEXT + " ") != PRIOR_TEXT_DIGEST


def test_an_empty_text_is_refused_rather_than_digested() -> None:
    with pytest.raises(PriorHypothesisError):
        prior_text_digest("   ")


def test_a_notation_site_without_a_literal_is_refused_at_construction() -> None:
    with pytest.raises(PriorHypothesisError):
        NotationSite(
            site_id="x",
            literal="",
            what_it_decides="شيء",
            what_its_absence_invalidates="شيء",
        )


def test_the_site_ids_are_unique() -> None:
    ids = [site.site_id for site in REQUIRED_NOTATION_SITES]
    assert len(set(ids)) == len(ids)


def test_the_named_residuals_carry_the_decisive_corrections() -> None:
    assert (
        THE_ALGEBRA_DOES_NOT_CREATE_ITS_OBJECTS_NOTE in PRIOR_HYPOTHESIS_NAMED_RESIDUALS
    )
    assert (
        ONTOLOGICAL_KIND_IS_NOT_LINGUISTIC_ROLE_NOTE in PRIOR_HYPOTHESIS_NAMED_RESIDUALS
    )
    assert (
        A_LAYER_THAT_FOUND_A_LAYER_BENEATH_IT_IS_NOT_REFUTED_NOTE
        in PRIOR_HYPOTHESIS_NAMED_RESIDUALS
    )
    assert NO_READOUT_EXISTS_FOR_PK0_YET_NOTE in PRIOR_HYPOTHESIS_NAMED_RESIDUALS


def test_the_deposit_names_no_arabic_entity() -> None:
    for forbidden in ("جذر", "وزن", "مصدر", "مشتقّ", "فاعل", "مفعول"):
        assert forbidden not in PRIOR_HYPOTHESIS_TEXT
