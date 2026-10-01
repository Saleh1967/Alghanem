"""اختباراتُ إحصاء الأوزان والتقاليب: كلُّ رقمٍ مُجمَّدٍ يُعاد اشتقاقُه هنا."""

from __future__ import annotations

import math
from itertools import permutations

import pytest

from alghanem.arabic.mujarrad_taqalib_census import (
    QUADRILATERAL_WAZN_LADDER,
    THE_CENSUS_AT_MEASUREMENT,
    THE_RULE_PRICES_AT_MEASUREMENT,
    TRILATERAL_WAZN_LADDER,
    CellStanding,
    ForbiddingRule,
    MujarradTaqalibError,
    RuleVerdict,
    RungWarrant,
    ShapeWitness,
    UsageWarrant,
    WaznRung,
    class_collisions,
    classify_cell,
    declared_fold,
    fold_root,
    forbidding_rules_against,
    multiset_permutation_count,
    orbit_readings,
    quadrilateral_formal_shapes,
    quadrilateral_readings,
    rule_prices,
    rule_verdict,
    rules_abstaining_on,
    taqalib_census,
    unranked_letters_of,
    wazn_occupancy_is_suspended,
)
from alghanem.arabic.tajsir_bridge import fold_map


def test_the_frozen_census_is_what_the_sealed_bytes_give() -> None:
    assert taqalib_census() == THE_CENSUS_AT_MEASUREMENT


def test_the_six_standings_exhaust_the_space_and_do_not_overlap() -> None:
    census = THE_CENSUS_AT_MEASUREMENT
    assert (
        census.used_unforbidden
        + census.used_though_forbidden
        + census.used_with_a_rule_abstaining
        + census.forbidden_and_unused
        + census.unused_with_a_rule_abstaining
        + census.muhmal
        == census.space
    )
    assert census.used == 4_559
    assert census.space - census.used == 6_656


def test_the_unexamined_cells_are_not_counted_as_muhmal() -> None:
    """ما امتنعت عنه القاعدةُ ليس مهملًا؛ وضمُّه إليه يدَّعي فحصًا لم يقع."""

    census = THE_CENSUS_AT_MEASUREMENT
    assert census.unexamined == 1_134
    assert census.muhmal == 5_244
    assert census.muhmal + census.unused_with_a_rule_abstaining == 6_006


def test_a_census_whose_parts_do_not_sum_is_refused() -> None:
    with pytest.raises(MujarradTaqalibError):
        type(THE_CENSUS_AT_MEASUREMENT)(
            orbits=1,
            space=10,
            used_unforbidden=1,
            used_though_forbidden=0,
            used_with_a_rule_abstaining=0,
            forbidden_and_unused=0,
            unused_with_a_rule_abstaining=0,
            muhmal=0,
        )


def test_the_multiset_count_is_not_the_permutation_count() -> None:
    assert multiset_permutation_count("جبذ") == 6
    assert multiset_permutation_count("ججب") == 3
    assert multiset_permutation_count("ددد") == 1
    assert multiset_permutation_count("جهجه") == 6
    assert multiset_permutation_count("جهزر") == math.factorial(4)
    with pytest.raises(MujarradTaqalibError):
        multiset_permutation_count("")


def test_every_orbit_space_equals_its_distinct_orderings() -> None:
    for reading in orbit_readings():
        assert reading.space == len({"".join(p) for p in permutations(reading.letters)})
        assert reading.space == len(reading.standings)
        assert reading.unused == reading.space - len(reading.used)


def test_both_declared_rules_are_refuted_as_impossibilities_by_attested_use() -> None:
    prices = {price.rule: price for price in rule_prices()}
    for rule, frozen in THE_RULE_PRICES_AT_MEASUREMENT.items():
        price = prices[rule]
        assert (price.cells, price.used_inside, price.cells_abstained) == frozen
        assert price.is_refuted_as_an_impossibility
        assert price.warrant_of_the_used is UsageWarrant.SAMA_IN_THE_SEALED_LEXICON


def test_a_refuted_rule_still_carries_a_measured_depression() -> None:
    prices = {price.rule: price for price in rule_prices()}
    for price in prices.values():
        assert price.usage_rate_inside < price.usage_rate_outside
    adjacency = prices[ForbiddingRule.ADJACENT_SHARED_MAKHRAJ]
    assert adjacency.usage_rate_inside == pytest.approx(0.25, abs=1e-9)


def test_a_multiset_rule_cannot_separate_cells_inside_one_orbit() -> None:
    """قاعدةُ المجموعة ثابتةٌ على المدار، فلا تُفسِّر خلوًّا فيه؛ قضيّةٌ تُفحَص."""

    def multiset_rule(form: str) -> bool:
        return "ا" in form

    separating = 0
    for reading in orbit_readings():
        verdicts = {multiset_rule(cell) for cell in reading.standings}
        separating += len(verdicts) > 1
    assert separating == 0


def test_the_declared_order_sensitive_rules_do_separate_inside_orbits() -> None:
    separating = 0
    for reading in orbit_readings():
        for rule in ForbiddingRule:
            verdicts = {
                rule in forbidding_rules_against(cell) for cell in reading.standings
            }
            separating += len(verdicts) > 1
    assert separating > 0


def test_a_used_cell_that_a_rule_forbids_is_named_not_hidden() -> None:
    assert classify_cell("ددن", used=True) is CellStanding.USED_THOUGH_FORBIDDEN
    assert classify_cell("ددن", used=False) is CellStanding.FORBIDDEN_AND_UNUSED
    assert classify_cell("جبذ", used=True) is CellStanding.USED_UNFORBIDDEN
    assert classify_cell("جبذ", used=False) is CellStanding.MUHMAL


def test_a_rule_that_cannot_read_a_letter_abstains_instead_of_permitting() -> None:
    """الألفُ خارجُ ترتيب المخارج، فسكوتُ قاعدةِ الجوار امتناعٌ لا إباحة."""

    adjacency = ForbiddingRule.ADJACENT_SHARED_MAKHRAJ
    assert unranked_letters_of("حدا") == ("ا",)
    assert unranked_letters_of("جبذ") == ()
    assert (
        rule_verdict(adjacency, "حدا") is RuleVerdict.UNREADABLE_FOR_AN_UNRANKED_LETTER
    )
    assert rules_abstaining_on("حدا") == (adjacency,)
    assert adjacency not in forbidding_rules_against("حدا")
    assert classify_cell("حدا", used=True) is CellStanding.USED_WITH_A_RULE_ABSTAINING
    assert (
        classify_cell("حدا", used=False) is CellStanding.UNUSED_WITH_A_RULE_ABSTAINING
    )


def test_a_rule_that_does_fire_outranks_another_rule_abstaining() -> None:
    """حكمٌ واقعٌ أولى من سكوتٍ عن حكم؛ وبهذا خرج صفُّ الامتناع 1,134 لا 1,158."""

    assert rules_abstaining_on("ااد") == (ForbiddingRule.ADJACENT_SHARED_MAKHRAJ,)
    assert ForbiddingRule.FA_EQUALS_AYN in forbidding_rules_against("ااد")
    assert classify_cell("ااد", used=False) is CellStanding.FORBIDDEN_AND_UNUSED


def test_the_shared_makhraj_rule_reads_distinct_letters_only() -> None:
    assert ForbiddingRule.ADJACENT_SHARED_MAKHRAJ in forbidding_rules_against("مشج")
    assert ForbiddingRule.ADJACENT_SHARED_MAKHRAJ not in forbidding_rules_against("صرر")


def test_the_two_class_condition_is_measured_zero_on_a_counter_that_can_fire() -> None:
    collisions = class_collisions()
    assert [c for c in collisions if c.crosses_two_classes] == []
    assert len(collisions) == 3
    assert {c.folded_form for c in collisions} == {"حدا", "دفا", "لما"}
    assert {c.written_forms for c in collisions} == {
        ("حدأ", "حدا"),
        ("دفأ", "دفا"),
        ("لمأ", "لما"),
    }


def test_the_fold_is_read_from_the_agreed_bridge_and_not_rewritten_here() -> None:
    """طيٌّ ثانٍ يُشبه الأوّلَ ويُخالفه في بندٍ يَعُدّ شجرةً أخرى."""

    assert dict(declared_fold()) == dict(fold_map())
    assert declared_fold()["أ"] == "ا"
    assert declared_fold()["ء"] == "ا"


def test_the_fold_costs_and_the_cost_is_measured() -> None:
    assert fold_root("لمأ") == fold_root("لما") == "لما"
    assert fold_root("رمى") == "رمي"
    assert set(declared_fold().values()) == {"ا", "و", "ي"}
    with pytest.raises(MujarradTaqalibError):
        fold_root("")


def test_the_quadrilateral_row_is_emitted_empty_rather_than_dropped() -> None:
    readings = quadrilateral_readings()
    assert len(readings) == 3
    assert sum(len(reading.used) for reading in readings) == 3
    assert {reading.space for reading in readings} == {6}


def test_the_formal_space_stands_without_a_witness_and_is_not_deleted() -> None:
    """`ABCD` أربعةٌ وعشرون وإن خلا منه الجرد؛ والخلوُّ سكوتٌ لا نفي."""

    shapes = {shape.shape: shape for shape in quadrilateral_formal_shapes()}
    assert len(shapes) == 15
    assert shapes["ABCD"].space == 24
    assert shapes["ABCD"].attested_roots == 0
    assert shapes["ABCD"].witness is ShapeWitness.UNATTESTED_IN_THIS_DEPOSIT
    assert shapes["ABAB"].space == 6
    assert shapes["ABAB"].attested_roots == 3
    assert shapes["ABAB"].witness is ShapeWitness.ATTESTED_IN_THIS_DEPOSIT
    attested = [s for s in shapes.values() if s.attested_roots]
    assert [s.shape for s in attested] == ["ABAB"]


def test_the_formal_space_is_computed_from_the_shape_not_from_attestation() -> None:
    for shape in quadrilateral_formal_shapes():
        assert shape.space == multiset_permutation_count(shape.shape)


def test_the_trilateral_ladder_narrows_by_counting_and_names_its_warrant() -> None:
    cells = [rung.cells for rung in TRILATERAL_WAZN_LADDER]
    assert cells == [256, 81, 27, 9, 6]
    assert TRILATERAL_WAZN_LADDER[0].warrant is RungWarrant.DERIVED_BY_COUNTING
    assert all(
        rung.warrant is RungWarrant.TRANSCRIBED_NOT_MEASURED
        for rung in TRILATERAL_WAZN_LADDER[1:]
    )
    assert cells == sorted(cells, reverse=True)


def test_the_quadrilateral_ladder_ends_at_one_declared_cell() -> None:
    cells = [rung.cells for rung in QUADRILATERAL_WAZN_LADDER]
    assert cells == [1_024, 16, 1]
    assert QUADRILATERAL_WAZN_LADDER[-1].warrant is RungWarrant.TRANSCRIBED_NOT_MEASURED


def test_a_rung_without_a_written_constraint_is_refused() -> None:
    with pytest.raises(MujarradTaqalibError):
        WaznRung(
            name="درجة",
            cells=3,
            constraint="   ",
            warrant=RungWarrant.DERIVED_BY_COUNTING,
        )
    with pytest.raises(MujarradTaqalibError):
        WaznRung(
            name="درجة",
            cells=0,
            constraint="قيد",
            warrant=RungWarrant.DERIVED_BY_COUNTING,
        )


def test_the_wazn_occupancy_names_its_absent_material_instead_of_a_number() -> None:
    suspension = wazn_occupancy_is_suspended()
    assert "ALGHANEM_MASAQ_PATH" in suspension
    assert "معلَّق" in suspension


def test_qiyas_is_never_granted_here() -> None:
    refused = UsageWarrant.QIYAS_REFUSED_FOR_ABSENT_RULE_DEPOSIT
    assert refused.value.startswith("قياسٌ مرفوض")
    assert all(
        price.warrant_of_the_used is UsageWarrant.SAMA_IN_THE_SEALED_LEXICON
        for price in rule_prices()
    )
