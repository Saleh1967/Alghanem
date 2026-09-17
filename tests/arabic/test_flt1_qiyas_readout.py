"""شواهدُ قراءة G0.FLT-1 على قانون القياس: الختمُ، والآلةُ، والنتيجةُ كما خرجت."""

from __future__ import annotations

import pytest

from alghanem.arabic.flt1_qiyas_preregistration import (
    HigherCenterStanding,
    QiyasOutcome,
)
from alghanem.arabic.flt1_qiyas_readout import (
    QIYAS_READOUT_NAMED_RESIDUALS,
    MinimalityStanding,
    QiyasReadoutError,
    SealedQiyasPreregistration,
    read_qiyas,
    seal_qiyas_preregistration,
)


@pytest.fixture(name="run")
def _run() -> object:
    return read_qiyas(seal_qiyas_preregistration())


def test_a_sealed_preregistration_is_not_built_by_hand() -> None:
    with pytest.raises(QiyasReadoutError):
        SealedQiyasPreregistration(
            law_text_digest="a" * 64,
            preregistration_digest="b" * 64,
            _token=object(),
        )


def test_a_drifted_seal_is_refused_not_repaired(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sealed = seal_qiyas_preregistration()
    monkeypatch.setattr(
        "alghanem.arabic.flt1_qiyas_readout.FLT1_QIYAS_TEXT_DIGEST", "c" * 64
    )

    with pytest.raises(QiyasReadoutError):
        read_qiyas(sealed)


def test_the_readout_refuses_anything_that_is_not_a_sealed_registration() -> None:
    with pytest.raises(QiyasReadoutError):
        read_qiyas(object())  # type: ignore[arg-type]


def test_every_frozen_surface_is_read_and_none_is_dropped(run) -> None:  # type: ignore[no-untyped-def]
    assert tuple(reading.surface for reading in run.surfaces) == (
        "فَتَحَ",
        "يَكْتُبُ",
        "مَسْجِدٌ",
        "بَابٌ",
        "شَدَّ",
        "اِسْتَغْفَرَ",
        "قِفْ",
    )


def test_an_open_center_reads_as_continuity_under_the_origin(run) -> None:  # type: ignore[no-untyped-def]
    reading = run.surface_named("فَتَحَ")

    assert (
        tuple(branch.outcome for branch in reading.branches)
        == (QiyasOutcome.CONTINUITY_UNDER_ORIGIN,) * 3
    )


def test_a_closed_center_reads_as_an_independent_branch_candidate(run) -> None:  # type: ignore[no-untyped-def]
    reading = run.surface_named("قِفْ")

    assert reading.branches[0].template == "CVC"
    assert reading.branches[0].outcome is QiyasOutcome.INDEPENDENT_BRANCH_CANDIDATE


def test_the_analytic_gates_are_marked_as_analytic_not_counted_as_evidence(run) -> None:  # type: ignore[no-untyped-def]
    branch = run.surface_named("قِفْ").branches[0]

    assert branch.gate(r"w^\*").is_analytic_in_this_deposit is True
    assert branch.gate(r"\mu").is_analytic_in_this_deposit is True
    assert branch.gate(r"\Delta_q").is_analytic_in_this_deposit is False
    assert run.analytic_gates == (r"w^\*", r"\mu")


def test_an_all_open_surface_is_reproduced_without_the_join_so_no_bypass_fails(  # noqa: E501
    run,  # type: ignore[no-untyped-def]
) -> None:
    reading = run.surface_named("فَتَحَ")

    assert reading.no_bypass.holds is False
    assert run.standing_for("فَتَحَ") is HigherCenterStanding.WITHHELD


def test_a_madd_surface_loses_reconstruction_and_closure_together(run) -> None:  # type: ignore[no-untyped-def]
    reading = run.surface_named("بَابٌ")

    assert reading.reconstruction.holds is False
    assert reading.closure.holds is False
    assert "(1,)" in reading.closure.named_reason
    assert run.standing_for("بَابٌ") is HigherCenterStanding.WITHHELD


def test_no_surface_earns_the_name_of_a_higher_center_in_this_run(run) -> None:  # type: ignore[no-untyped-def]
    standings = {
        reading.surface: run.standing_for(reading.surface) for reading in run.surfaces
    }

    assert HigherCenterStanding.BORN not in standings.values()
    assert standings["يَكْتُبُ"] is HigherCenterStanding.UNDERPOWERED
    assert standings["فَتَحَ"] is HigherCenterStanding.WITHHELD


def test_minimality_is_underpowered_because_the_target_is_not_independent(run) -> None:  # type: ignore[no-untyped-def]
    minimality = run.minimality

    assert minimality.licensed_hits == 18
    assert minimality.target_size == 18
    assert tuple(score.hits for score in minimality.weaker_scores) == (12, 12, 12)
    assert minimality.standing is MinimalityStanding.UNDERPOWERED_BY_TARGET_PROVENANCE


def test_a_weaker_model_that_ties_would_defeat_the_claim() -> None:
    from alghanem.arabic.flt1_qiyas_readout import (
        MinimalityReading,
        WeakerModelScore,
    )

    tied = MinimalityReading(
        licensed_hits=18,
        target_size=18,
        weaker_scores=(
            WeakerModelScore(
                model_id="carrier-alone",
                hits=18,
                attempts=18,
                what_generosity_it_was_given="سعةٌ مُعلَنة",
            ),
        ),
    )

    assert tied.standing is MinimalityStanding.DEFEATED_BY_A_TIE


def test_the_unfired_branches_of_the_decision_machine_are_named_not_hidden(run) -> None:  # type: ignore[no-untyped-def]
    assert run.unfired_outcomes == (
        "BLOCK",
        "DEFER/BLOCK",
        "FORMAL_DIFFERENCE_ONLY",
        "NO_EFFECTIVE_DESCRIPTION",
        "NO_QIYAS",
    )


def test_the_readout_names_its_own_limits_as_residuals() -> None:
    assert len(QIYAS_READOUT_NAMED_RESIDUALS) == 3
    assert any("مضمونٌ بالبناء" in note for note in QIYAS_READOUT_NAMED_RESIDUALS)


def test_an_unknown_surface_is_refused_not_invented(run) -> None:  # type: ignore[no-untyped-def]
    with pytest.raises(QiyasReadoutError):
        run.surface_named("كَتَبَ")


def test_an_unread_gate_is_refused_not_invented(run) -> None:  # type: ignore[no-untyped-def]
    with pytest.raises(QiyasReadoutError):
        run.surface_named("قِفْ").branches[0].gate("Zz")
