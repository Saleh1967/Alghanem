"""اختبارُ قانون الوديعة: أيمنع الشَّرِه، ويكشف الانحلال، ويأبى المجمَّد؟"""

from __future__ import annotations

import pytest

from alghanem.seals import (
    A_DEPOSIT_THAT_BRINGS_NO_LIVE_SEAL_IS_NOT_ADMITTED,
    A_GAIN_BOUGHT_BY_DROPPING_EVIDENCE_IS_DECAY_NOT_GAIN,
    AN_EXHIBIT_WITHOUT_A_PRICE_IS_NOT_EVIDENCE,
    DepositLawError,
    Invoice,
    rule_on_deposit,
)


def _invoice(
    *,
    cost_before: float = 100.0,
    cost_after: float = 90.0,
    covered_before: int = 50,
    covered_after: int = 50,
) -> Invoice:
    return Invoice(
        deposit="وديعةُ اختبار",
        scope="نطاقٌ واحدٌ مُسمّى",
        units="بتًّا",
        cost_before=cost_before,
        cost_after=cost_after,
        covered_before=covered_before,
        covered_after=covered_after,
    )


def test_a_deposit_that_pays_and_keeps_its_coverage_is_admitted() -> None:
    ruling = rule_on_deposit(_invoice(), brings_a_live_seal=True)
    assert ruling.is_admitted
    assert ruling.refusals == ()
    assert ruling.invoice.delta == -10.0


def test_a_deposit_that_does_not_pay_is_refused_by_name() -> None:
    ruling = rule_on_deposit(_invoice(cost_after=110.0), brings_a_live_seal=True)
    assert not ruling.is_admitted
    assert AN_EXHIBIT_WITHOUT_A_PRICE_IS_NOT_EVIDENCE in ruling.refusals


def test_a_zero_delta_is_not_a_payment() -> None:
    invoice = _invoice(cost_after=100.0)
    assert invoice.delta == 0.0
    assert not invoice.pays_for_itself
    assert not rule_on_deposit(invoice, brings_a_live_seal=True).is_admitted


def test_a_gain_bought_by_dropping_evidence_is_named_decay() -> None:
    invoice = _invoice(cost_after=10.0, covered_after=20)
    assert invoice.pays_for_itself
    assert invoice.decays
    ruling = rule_on_deposit(invoice, brings_a_live_seal=True)
    assert not ruling.is_admitted
    assert A_GAIN_BOUGHT_BY_DROPPING_EVIDENCE_IS_DECAY_NOT_GAIN in ruling.refusals


def test_widening_the_coverage_while_paying_is_still_admitted() -> None:
    invoice = _invoice(covered_after=80)
    assert invoice.coverage_delta == 30
    assert not invoice.decays
    assert rule_on_deposit(invoice, brings_a_live_seal=True).is_admitted


def test_a_deposit_without_a_live_seal_is_refused_even_when_it_pays() -> None:
    ruling = rule_on_deposit(_invoice(), brings_a_live_seal=False)
    assert not ruling.is_admitted
    assert A_DEPOSIT_THAT_BRINGS_NO_LIVE_SEAL_IS_NOT_ADMITTED in ruling.refusals


def test_every_failing_condition_is_named_and_none_is_swallowed() -> None:
    ruling = rule_on_deposit(
        _invoice(cost_after=100.0, covered_after=10), brings_a_live_seal=False
    )
    assert len(ruling.refusals) == 3


def test_the_admission_is_derived_from_the_refusals_and_not_a_written_field() -> None:
    assert not hasattr(Invoice, "is_admitted")
    ruling = rule_on_deposit(_invoice(), brings_a_live_seal=True)
    assert "admitted" not in {
        field
        for field in ruling.__dataclass_fields__  # type: ignore[attr-defined]
    }


def test_an_invoice_carries_exactly_one_scope() -> None:
    fields = set(Invoice.__dataclass_fields__)  # type: ignore[attr-defined]
    assert "scope" in fields
    assert "scope_before" not in fields
    assert "scope_after" not in fields


def test_a_negative_cost_is_refused() -> None:
    with pytest.raises(DepositLawError):
        _invoice(cost_after=-1.0)


def test_an_invoice_on_empty_coverage_is_refused() -> None:
    with pytest.raises(DepositLawError):
        _invoice(covered_before=0)


def test_an_invoice_without_a_named_scope_is_refused() -> None:
    with pytest.raises(DepositLawError):
        Invoice(
            deposit="وديعة",
            scope="   ",
            units="بتًّا",
            cost_before=2.0,
            cost_after=1.0,
            covered_before=1,
            covered_after=1,
        )
