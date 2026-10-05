"""اختباراتُ سجلِّ ترخيصِ الجبر: التوقيع، والسُّلَّم، وفصلُ الدَّينَين."""

from __future__ import annotations

import pytest

from alghanem.arabic import algebra_licence_ledger as ledger
from alghanem.arabic import letter_haraka_partition as partition


def test_the_signature_reads_the_bytes_and_does_not_copy_the_prose() -> None:
    signatures = ledger.signed_references()
    assert len(signatures) == 2
    for signed in signatures:
        deposits = ledger._collation.THE_DEPOSITS
        declared_length, declared_seal = deposits[signed.reference]
        assert signed.byte_length == declared_length
        assert signed.sha256 == declared_seal


def test_a_third_copy_that_was_never_opened_is_outside_the_signature() -> None:
    assert ledger.covers_reference("quran-simple-enhanced.txt")
    assert not ledger.covers_reference("tanzil-uthmani.txt")
    with pytest.raises(ledger.AlgebraLicenceLedgerError):
        ledger.owner_signature("tanzil-uthmani.txt")


def test_a_licence_without_a_written_condition_is_refused() -> None:
    with pytest.raises(ledger.AlgebraLicenceLedgerError):
        ledger.OwnerSignature(
            reference="quran-simple-enhanced.txt",
            byte_length=1319901,
            sha256="3" * 64,
            condition="   ",
        )


def test_every_rung_names_what_it_withheld_and_not_only_what_it_licensed() -> None:
    rungs = ledger.licence_ladder()
    assert rungs
    for rung in rungs:
        assert rung.licensed.strip()
        assert rung.withheld.strip()


def test_a_rung_that_hides_its_withholding_is_refused() -> None:
    with pytest.raises(ledger.AlgebraLicenceLedgerError):
        ledger.LicenceRung(
            name="درجةٌ",
            material="مادّةٌ",
            licensed="رخَّصت كلَّ شيء",
            withheld="",
        )


def test_the_hundred_and_twelve_is_licensed_rung_by_rung_and_never_whole() -> None:
    rungs = [rung for rung in ledger.licence_ladder() if "الـ١١٢ عند" in rung.name]
    assert len(rungs) == len(partition.SourceRung)
    realized = [
        partition.table_census(source).realized_cells for source in partition.SourceRung
    ]
    assert realized == sorted(realized)
    assert realized[0] < realized[-1] < ledger.THE_HUNDRED_AND_TWELVE


def test_the_ladder_figures_are_rederived_and_not_transcribed() -> None:
    first = ledger.licence_ladder()
    second = ledger.licence_ladder()
    assert first == second
    taqalib = ledger._taqalib.taqalib_census()
    rung = next(r for r in first if r.name == "تقاليبُ المجرَّد")
    assert str(taqalib.orbits) in rung.licensed
    assert str(taqalib.unexamined) in rung.withheld


def test_the_counting_debt_is_zero_only_because_every_rung_actually_ran() -> None:
    assert ledger.counting_debts() == ()
    assert len(ledger._rung_builders()) == len(ledger.licence_ladder())


def test_a_rung_that_refuses_to_run_becomes_a_counting_debt_not_a_silence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def refuse() -> ledger.LicenceRung:
        raise RuntimeError("مادّتُها لم تُفتَح")

    monkeypatch.setattr(ledger, "_rung_of_the_collation", refuse)
    monkeypatch.setattr(
        ledger,
        "_rung_builders",
        lambda: (("مقابلةُ المرجعَين", "quran_mirror_collation", refuse),),
    )
    debts = ledger.counting_debts()
    assert len(debts) == 1
    assert debts[0].kind is ledger.DebtKind.COUNTING
    assert debts[0].standing is ledger.DebtStanding.UNSETTLED_FOR_A_RUNG_THAT_REFUSED
    assert "مادّتُها لم تُفتَح" in debts[0].resolver


def test_the_documentation_debt_is_not_zero_and_is_shown_by_its_names() -> None:
    debts = ledger.documentation_debts()
    assert debts
    for debt in debts:
        assert debt.kind is ledger.DebtKind.DOCUMENTATION
        assert debt.standing in {
            ledger.DebtStanding.SUSPENDED_FOR_ABSENT_BYTES,
            ledger.DebtStanding.SUSPENDED_FOR_ABSENT_TESTIMONY,
        }
        assert debt.material.strip()
        assert debt.resolver.strip()


def test_a_counting_debt_may_not_be_suspended_for_an_absent_material() -> None:
    with pytest.raises(ledger.AlgebraLicenceLedgerError):
        ledger.OutstandingDebt(
            subject="عددٌ",
            kind=ledger.DebtKind.COUNTING,
            standing=ledger.DebtStanding.SUSPENDED_FOR_ABSENT_BYTES,
            material="مادّةٌ غائبة",
            resolver="وحدةٌ",
        )


def test_a_debt_without_a_place_of_settlement_is_a_claim_not_a_debt() -> None:
    with pytest.raises(ledger.AlgebraLicenceLedgerError):
        ledger.OutstandingDebt(
            subject="بندٌ",
            kind=ledger.DebtKind.DOCUMENTATION,
            standing=ledger.DebtStanding.SUSPENDED_FOR_ABSENT_BYTES,
            material="مادّةٌ",
            resolver="",
        )


def test_the_two_debts_are_disjoint_in_kind() -> None:
    kinds = {debt.kind for debt in ledger.documentation_debts()}
    assert kinds == {ledger.DebtKind.DOCUMENTATION}
    counting = ledger.counting_debts()
    assert all(debt.kind is ledger.DebtKind.COUNTING for debt in counting)


def test_the_named_residuals_are_all_reachable_prose() -> None:
    assert len(ledger.ALGEBRA_LICENCE_LEDGER_NAMED_RESIDUALS) == 5
    for residual in ledger.ALGEBRA_LICENCE_LEDGER_NAMED_RESIDUALS:
        assert len(residual) > 40


def test_the_signature_lifts_no_block_and_thaws_no_freeze() -> None:
    before = ledger._taqalib.wazn_occupancy_is_suspended()
    ledger.signed_references()
    assert ledger._taqalib.wazn_occupancy_is_suspended() == before
    assert any(
        debt.resolver.startswith("mujarrad_taqalib_census")
        for debt in ledger.documentation_debts()
    )
