"""شواهدُ العقد الليفيّ للحرف والحركة: عنصرٌ عنصرٌ بدليله ومانعه وبقاياه."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from alghanem.arabic import letter_haraka_fiber_contract
from alghanem.arabic.carrier_state_observed_fiber import (
    run_observed_fiber_on_the_deposited_fatiha,
)
from alghanem.arabic.fiber_transfer_contracts import CV_BIRTH_CERTIFICATE_STANDING
from alghanem.arabic.letter_haraka_fiber_contract import (
    LETTER_HARAKA_NAMED_RESIDUALS,
    ContractElement,
    ElementReading,
    ElementStanding,
    EvidenceGenus,
    LetterHarakaContractError,
    Subject,
    build_letter_haraka_contract,
    count_absent_diacritic_rows,
    count_written_sukun_rows,
    run_letter_haraka_contract,
)


@pytest.fixture(name="report")
def _report() -> object:
    return run_letter_haraka_contract()


@pytest.fixture(name="table")
def _table() -> object:
    return run_observed_fiber_on_the_deposited_fatiha()


def _element(**overrides: object) -> ContractElement:
    base = ContractElement(
        element_id="مثالُ شاهد",
        subject=Subject.WRITTEN_LETTER,
        what_is_claimed="دعوى",
        evidence_genus=EvidenceGenus.ORTHOGRAPHIC_OBSERVATION,
        what_the_evidence_counts="ما يُعَدّ",
        preventers=(),
        residuals=("بقيّةٌ مُسمّاة",),
    )
    return replace(base, **overrides)  # type: ignore[arg-type]


def test_every_element_names_its_claim_evidence_preventers_and_residuals() -> None:
    elements = build_letter_haraka_contract()

    assert len(elements) == 8
    for element in elements:
        assert element.what_is_claimed.strip()
        assert element.what_the_evidence_counts.strip()
        assert element.residuals
        if element.evidence_genus is EvidenceGenus.RECORDED_SOUND:
            assert element.preventers


def test_an_element_without_a_named_residual_is_refused() -> None:
    with pytest.raises(LetterHarakaContractError):
        _element(residuals=())


def test_a_recorded_sound_element_without_a_preventer_is_refused() -> None:
    with pytest.raises(LetterHarakaContractError):
        _element(evidence_genus=EvidenceGenus.RECORDED_SOUND, preventers=())


def test_a_duplicated_preventer_is_refused() -> None:
    with pytest.raises(LetterHarakaContractError):
        _element(
            evidence_genus=EvidenceGenus.RECORDED_SOUND,
            preventers=("مانعٌ واحد", "مانعٌ واحد"),
        )


def test_no_phonetic_element_can_be_reached_in_this_tree() -> None:
    phonetic = [
        element
        for element in build_letter_haraka_contract()
        if element.evidence_genus is EvidenceGenus.RECORDED_SOUND
    ]

    assert len(phonetic) == 3
    assert all(not element.is_reachable_in_this_tree for element in phonetic)


def test_the_written_letter_never_takes_the_standing_of_a_sound(report) -> None:  # type: ignore[no-untyped-def]
    written = report.reading_for("letter.written.is_an_observed_carrier")
    heard = report.reading_for("letter.phonetic.has_a_determinate_value")

    assert written.standing is ElementStanding.HELD_ON_THE_DEPOSIT
    assert heard.standing is ElementStanding.WITHHELD_BY_A_PREVENTER
    assert "UnicodeIsNotRecordedSound" in heard.withheld_because


def test_a_withheld_element_is_written_not_deleted(report) -> None:  # type: ignore[no-untyped-def]
    assert report.withheld == (
        "letter.phonetic.has_a_determinate_value",
        "haraka.phonetic.has_a_determinate_value",
        "sukun.phonetic.is_the_absence_of_a_vowel_sound",
    )
    for element_id in report.withheld:
        assert report.reading_for(element_id).observed_count == 0


def test_the_written_sukun_and_the_absent_diacritic_are_counted_apart(table) -> None:  # type: ignore[no-untyped-def]
    written_sukun = count_written_sukun_rows(table)
    absent = count_absent_diacritic_rows(table)

    assert written_sukun == 21
    assert absent == 40
    assert written_sukun != absent


def test_no_occurrence_carries_a_haraka_and_a_sukun_together(table) -> None:  # type: ignore[no-untyped-def]
    both = [
        row
        for row in table.rows
        if dict(row.state_vector)["vowel"] != "ABSENT"
        and dict(row.state_vector)["quiescence"] != "ABSENT"
    ]

    assert both == []


def test_the_haraka_is_shown_not_to_be_a_value_inside_the_letter(report) -> None:  # type: ignore[no-untyped-def]
    reading = report.reading_for("haraka.written.is_not_the_letter_itself")

    assert reading.standing is ElementStanding.HELD_ON_THE_DEPOSIT
    assert reading.observed_count == 14


def test_every_figure_comes_from_the_fingerprinted_deposit(report) -> None:  # type: ignore[no-untyped-def]
    assert report.deposit_sha256 == (
        "d435d63a4e49ea03a75344b050df01dd99d5bfb77335c807e2d6309f52174341"
    )
    assert (
        report.reading_for("letter.written.is_an_observed_carrier").observed_count
        == 143
    )
    assert report.reading_for("haraka.written.is_an_observed_mark").observed_count == 82
    assert report.reading_for("sukun.written.is_an_observed_mark").observed_count == 21
    assert report.reading_for("absence.is_not_the_written_sukun").observed_count == 40


def test_the_contract_covers_all_four_subjects(report) -> None:  # type: ignore[no-untyped-def]
    subjects = {reading.element.subject for reading in report.readings}

    assert subjects == set(Subject)


def test_a_held_reading_without_an_occurrence_is_refused() -> None:
    with pytest.raises(LetterHarakaContractError):
        ElementReading(
            element=_element(),
            standing=ElementStanding.HELD_ON_THE_DEPOSIT,
            observed_count=0,
            withheld_because="",
        )


def test_a_withheld_reading_without_a_reason_is_refused() -> None:
    with pytest.raises(LetterHarakaContractError):
        ElementReading(
            element=_element(),
            standing=ElementStanding.WITHHELD_BY_A_PREVENTER,
            observed_count=0,
            withheld_because="   ",
        )


def test_a_held_reading_that_also_writes_a_withholding_reason_is_refused() -> None:
    with pytest.raises(LetterHarakaContractError):
        ElementReading(
            element=_element(),
            standing=ElementStanding.HELD_ON_THE_DEPOSIT,
            observed_count=1,
            withheld_because="سببٌ لا موضعَ له",
        )


def test_an_unknown_element_is_refused_not_invented(report) -> None:  # type: ignore[no-untyped-def]
    with pytest.raises(LetterHarakaContractError):
        report.reading_for("letter.written.does_not_exist")


def test_a_contract_missing_a_subject_is_refused(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    without_haraka = tuple(
        element
        for element in build_letter_haraka_contract()
        if element.subject is not Subject.WRITTEN_HARAKA
    )
    monkeypatch.setattr(
        letter_haraka_fiber_contract,
        "build_letter_haraka_contract",
        lambda: without_haraka,
    )

    with pytest.raises(LetterHarakaContractError, match="الحركةُ المكتوبة"):
        run_letter_haraka_contract()


def test_one_element_carrying_both_separated_subjects_is_refused(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    conflated = tuple(
        replace(element, subject=Subject.ABSENT_DIACRITIC)
        if element.subject is Subject.WRITTEN_SUKUN
        else element
        for element in build_letter_haraka_contract()
    )
    monkeypatch.setattr(
        letter_haraka_fiber_contract,
        "build_letter_haraka_contract",
        lambda: conflated,
    )

    with pytest.raises(
        LetterHarakaContractError, match="AWrittenSukunIsNotAnAbsentDiacritic"
    ):
        run_letter_haraka_contract()


def test_the_run_refuses_a_deposit_where_the_two_classes_are_not_separable(  # type: ignore[no-untyped-def]
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        letter_haraka_fiber_contract, "count_absent_diacritic_rows", lambda table: 21
    )

    with pytest.raises(
        LetterHarakaContractError, match="AWrittenSukunIsNotAnAbsentDiacritic"
    ):
        run_letter_haraka_contract()


def test_the_contract_runs_while_the_cv_birth_certificate_is_unissued(report) -> None:  # type: ignore[no-untyped-def]
    assert CV_BIRTH_CERTIFICATE_STANDING.issued is False
    assert report.held
    assert report.withheld


def test_the_contract_names_its_own_limits_as_residuals() -> None:
    assert len(LETTER_HARAKA_NAMED_RESIDUALS) == 5
    assert any(
        "AWrittenLetterIsNotASound" in note for note in LETTER_HARAKA_NAMED_RESIDUALS
    )
    assert any(
        "AWrittenSukunIsNotAnAbsentDiacritic" in note
        for note in LETTER_HARAKA_NAMED_RESIDUALS
    )
    assert any(
        "RunningTheContractIsNotBlockedOnACertificate" in note
        for note in LETTER_HARAKA_NAMED_RESIDUALS
    )


def test_this_contract_reaches_no_kernel_module() -> None:
    from alghanem.import_boundary import ImportBoundaryPolicy, audit_import_boundary

    report = audit_import_boundary(
        (Path(letter_haraka_fiber_contract.__file__),),
        ImportBoundaryPolicy(
            policy_id="letter-haraka-contract-is-not-wired-to-the-kernel",
            permitted_modules=(),
            forbidden_packages=("alghanem.kernel",),
        ),
    )

    assert not any(
        reached == "alghanem.kernel" or reached.startswith("alghanem.kernel.")
        for reached in report.reached_modules
    ), report.reached_modules
