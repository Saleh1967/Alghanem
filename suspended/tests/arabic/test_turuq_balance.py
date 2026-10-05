"""شهاداتُ موازن الطرق: الترتيبُ المسنون، والحارسُ المقدَّم، وعضُّ القواعد."""

from __future__ import annotations

import pytest

from alghanem.arabic.turuq_balance import (
    THE_FALSIFIERS,
    BalanceError,
    BalanceRule,
    Claim,
    Tariqa,
    rule_bites,
    strength_of,
    the_rules_in_order,
    weigh,
)


def _sound(name: str, tariqa: Tariqa) -> Claim:
    return Claim(
        name=name,
        tariqa=tariqa,
        counted_is_the_named=True,
        is_rederived=True,
    )


def test_the_guard_is_first_and_not_merely_present() -> None:
    assert the_rules_in_order()[0] is BalanceRule.D0_NAMED_IS_COUNTED
    assert the_rules_in_order().index(
        BalanceRule.D0_NAMED_IS_COUNTED
    ) < the_rules_in_order().index(BalanceRule.D1_ROAD_ORDER)


def test_counting_outranks_structure_outranks_reservation() -> None:
    assert strength_of(Tariqa.COUNTING) > strength_of(Tariqa.STRUCTURE)
    assert strength_of(Tariqa.STRUCTURE) > strength_of(Tariqa.RESERVATION)


def test_a_count_of_the_wrong_name_falls_before_it_is_weighed() -> None:
    misnamed = Claim(
        name="الشدّةُ مسمّاةً إدغامًا",
        tariqa=Tariqa.COUNTING,
        counted_is_the_named=False,
        is_rederived=True,
    )
    verdict = weigh(misnamed, _sound("بنيانٌ مرخَّص", Tariqa.STRUCTURE))
    assert verdict.deciding_rule is BalanceRule.D0_NAMED_IS_COUNTED
    assert verdict.upheld is None


def test_the_strongest_road_does_not_rescue_a_misnamed_count() -> None:
    misnamed = Claim(
        name="عدٌّ صحيحٌ لغير مسمّاه",
        tariqa=Tariqa.COUNTING,
        counted_is_the_named=False,
        is_rederived=True,
    )
    honest = _sound("عدٌّ آخر", Tariqa.COUNTING)
    assert weigh(misnamed, honest).deciding_rule is BalanceRule.D0_NAMED_IS_COUNTED


def test_structure_is_refused_when_it_opposes_a_count() -> None:
    verdict = weigh(
        _sound("بنيانٌ مرخَّص", Tariqa.STRUCTURE),
        _sound("عدٌّ مُعادُ الاشتقاق", Tariqa.COUNTING),
    )
    assert verdict.deciding_rule is BalanceRule.D1_ROAD_ORDER
    assert verdict.upheld == "عدٌّ مُعادُ الاشتقاق"


def test_a_claim_that_was_not_rederived_is_not_a_party_at_all() -> None:
    unmeasured = Claim(
        name="صوريٌّ لم تصل مادّتُه",
        tariqa=Tariqa.STRUCTURE,
        counted_is_the_named=True,
        is_rederived=False,
    )
    verdict = weigh(unmeasured, _sound("عدّ", Tariqa.COUNTING))
    assert verdict.deciding_rule is BalanceRule.D2_WHO_MAY_OPPOSE
    assert verdict.upheld is None


def test_a_reserved_claim_is_stopped_before_the_road_order_runs() -> None:
    reserved = Claim(
        name="محجوز",
        tariqa=Tariqa.RESERVATION,
        counted_is_the_named=True,
        is_reserved=True,
        is_rederived=True,
    )
    verdict = weigh(reserved, _sound("عدّ", Tariqa.COUNTING))
    assert verdict.deciding_rule is BalanceRule.D3_RESERVED_DOES_NOT_OPPOSE
    assert verdict.upheld is None


def test_a_reservation_cannot_wear_the_counting_road() -> None:
    with pytest.raises(BalanceError):
        Claim(
            name="محجوزٌ بثوب عدّ",
            tariqa=Tariqa.COUNTING,
            counted_is_the_named=True,
            is_reserved=True,
        )


def test_equal_roads_archive_both_sides_and_lift_neither() -> None:
    verdict = weigh(_sound("طرفٌ أوّل", Tariqa.COUNTING), _sound("ثانٍ", Tariqa.COUNTING))
    assert verdict.deciding_rule is BalanceRule.D4_REFUSAL_IS_ARCHIVED
    assert verdict.upheld is None
    assert "طرفٌ أوّل" in verdict.reason and "ثانٍ" in verdict.reason


def test_every_rule_carries_the_sentence_that_would_drop_it() -> None:
    assert set(THE_FALSIFIERS) == set(the_rules_in_order())
    for rule, sentence in THE_FALSIFIERS.items():
        assert sentence.startswith("تسقط "), rule


def test_no_rule_is_tenantless_on_the_deposited_ledger() -> None:
    bites = rule_bites()
    assert tuple(bite.rule for bite in bites) == the_rules_in_order()
    assert [bite for bite in bites if bite.is_tenantless] == []


def test_the_guard_bites_exactly_the_deposited_proxy_genus() -> None:
    from alghanem.arabic.tawlid_algebra_ledger import LinkGenus, standings

    deposited = sum(
        1 for link, _ in standings() if link.genus is LinkGenus.PROXY_NOT_THE_PHENOMENON
    )
    guard = next(
        bite for bite in rule_bites() if bite.rule is BalanceRule.D0_NAMED_IS_COUNTED
    )
    assert guard.bitten == deposited
    assert guard.bitten > 0


def test_a_claim_without_a_name_is_not_weighed() -> None:
    with pytest.raises(BalanceError):
        Claim(name="   ", tariqa=Tariqa.COUNTING, counted_is_the_named=True)
