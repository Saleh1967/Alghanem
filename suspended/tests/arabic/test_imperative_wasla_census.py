"""اختباراتُ قياس همزة الوصل في الأمر المجرَّد على المدوَّنة المُبصَّمة.

والأسطرُ المكتوبة هنا **مُصطنَعةٌ مُصرَّحٌ بجنسها**، لا مقتطعةٌ من المدوَّنة:
رخصتُها تمنع نسخَ بايتاتها إلى هذه الشجرة. وبنيتُها وحدَها هي المُحاكاة.

وفيها الحالتان اللتان تكسران أقربَ قراءةٍ خاطئة: أمرٌ مجرَّدٌ بلا وَسْم `(I)`
(فمن اشترط حضورَه خرج بصفر)، وأمرٌ يبدأ بهمزة قطعٍ `>` لا وصلٍ `{` (فمن سوّى
بينهما عدَّ البابين بابًا).

وإعادةُ الاشتقاق من البايتات نفسِها اختبارٌ اختياريّ يُفعَّل بمتغيّر بيئةٍ
مُسمًّى، لأنّ البايتات ليست في الشجرة ولن تكون.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from alghanem.arabic.hollow_root_root_census import (
    SegmentRecord,
    corpus_lines,
    parse_segment_line,
)
from alghanem.arabic.imperative_wasla_census import (
    ARRIVING_IMPERATIVE_DIVERGENCES,
    BARE_IMPERATIVE_SEGMENTS,
    DOUBLED_ROOT_RESIDUAL,
    IMPERATIVE_WASLA_CENSUS_NAMED_RESIDUALS,
    NAQIS_RESIDUAL,
    REDERIVED_IDGHAM_AGREEMENT,
    REDERIVED_IMPERFECT_COEXISTENCE,
    REDERIVED_SALIM_AJWAF_TEST,
    REDERIVED_SHAPE_TABLES,
    SECOND_ARRIVING_SHAPE_FIGURES,
    ImperativeWaslaCensusError,
    classify_root,
    idgham_agreement,
    imperfect_coexistence,
    permutation_test,
    read_imperative,
    second_arriving_figures_that_matched,
    second_arriving_figures_without_a_rule,
    shape_table,
)
from alghanem.arabic.imperative_wasla_specification import (
    IMPERATIVE_WASL_SPECIFICATION_DIGEST,
    PERMUTATION_PROTOCOL,
    STANDING,
    WASL_CHARACTER,
    WEAKNESS_RULES,
    ImperativeWaslSpecificationError,
    RootShape,
    SpecificationStanding,
    WeaknessRule,
    specification_digest,
)

CORPUS_PATH_VARIABLE = "ALGHANEM_QAC_MORPHOLOGY_PATH"

RULES = {rule.name: rule for rule in WEAKNESS_RULES}

SYNTHETIC_LINES = (
    "(1:1:1:1)\t{Eobudu\tV\tSTEM|POS:V|IMPV|LEM:Eabada|ROOT:Ebd|2MP",
    "(1:1:2:1)\tqulo\tV\tSTEM|POS:V|IMPV|LEM:qaAla|ROOT:qwl|2MS",
    "(1:1:3:1)\t>otu\tV\tSTEM|POS:V|IMPV|LEM:>ataY|ROOT:Aty|2MP",
    "(1:1:4:1)\trud~u\tV\tSTEM|POS:V|IMPV|LEM:rad~a|ROOT:rdd|2MP",
    "(1:1:5:1)\t{$odudo\tV\tSTEM|POS:V|IMPV|LEM:$adado|ROOT:$dd|2MS",
    "(1:1:6:1)\t>aqiymu\tV\tSTEM|POS:V|IMPV|(IV)|LEM:>aqaAma|ROOT:qwm|2MP",
    "(1:1:7:1)\tyaEobudu\tV\tSTEM|POS:V|IMPF|LEM:Eabada|ROOT:Ebd|3MS",
)


def synthetic_records() -> list[SegmentRecord]:
    records = [parse_segment_line(line) for line in SYNTHETIC_LINES]
    return [record for record in records if record is not None]


def reading_for(root: str):
    for record in synthetic_records():
        reading = read_imperative(record)
        if reading is not None and reading.root == root:
            return reading
    raise AssertionError(f"no synthetic imperative for {root}")


def test_the_specification_standing_is_the_weaker_one_and_says_so() -> None:
    assert STANDING is SpecificationStanding.FORMULATED_AFTER_THE_NUMBER
    assert STANDING.value == "مُصاغة_بعد_الرقم"


def test_the_specification_is_frozen_under_its_own_digest() -> None:
    assert specification_digest() == IMPERATIVE_WASL_SPECIFICATION_DIGEST


def test_four_distinct_rules_are_declared_together() -> None:
    assert len(WEAKNESS_RULES) == 4
    signatures = {
        (tuple(sorted(rule.weak_letters)), rule.separates_the_doubled_root)
        for rule in WEAKNESS_RULES
    }
    assert len(signatures) == 4
    for rule in WEAKNESS_RULES:
        assert rule.what_it_assumes.strip()


def test_a_rule_without_a_declared_assumption_is_refused() -> None:
    with pytest.raises(ImperativeWaslSpecificationError):
        WeaknessRule(
            name="بلا_مُصادَرة",
            weak_letters=("w", "y"),
            separates_the_doubled_root=False,
            what_it_assumes="  ",
        )


def test_the_bare_imperative_is_read_from_the_absent_form_tag() -> None:
    assert reading_for("Ebd").is_bare is True
    augmented = [
        reading
        for reading in (read_imperative(record) for record in synthetic_records())
        if reading is not None and reading.root == "qwm"
    ]
    assert augmented and augmented[0].is_bare is False


def test_hamzat_qat_is_not_read_as_hamzat_wasl() -> None:
    assert WASL_CHARACTER == "{"
    assert reading_for("Ebd").has_wasla is True
    assert reading_for("Aty").has_wasla is False


def test_the_imperfect_is_not_read_as_an_imperative() -> None:
    imperfect = parse_segment_line(SYNTHETIC_LINES[-1])
    assert imperfect is not None
    assert read_imperative(imperfect) is None


def test_the_hollow_root_takes_no_wasla_in_the_synthetic_lines() -> None:
    assert reading_for("qwl").has_wasla is False


def test_the_same_root_is_classified_differently_by_different_rules() -> None:
    assert classify_root("Akl", RULES["علّة_فقط"]) is RootShape.SALIM
    assert classify_root("Akl", RULES["علّة_وهمزة"]) is RootShape.MITHAL
    assert classify_root("rdd", RULES["علّة_وهمزة"]) is RootShape.SALIM
    assert classify_root("rdd", RULES["علّة_وهمزة_والمضاعف_مُفرَد"]) is RootShape.MUDAAF


def test_a_root_is_not_classified_without_a_named_rule() -> None:
    with pytest.raises(ImperativeWaslaCensusError):
        classify_root("Ebd", "علّة_فقط")  # type: ignore[arg-type]


def test_only_trilateral_roots_are_classified() -> None:
    with pytest.raises(ImperativeWaslaCensusError):
        classify_root("dHrj", RULES["علّة_فقط"])


def test_the_shape_table_partitions_the_bare_segments() -> None:
    readings = tuple(
        reading
        for reading in (read_imperative(record) for record in synthetic_records())
        if reading is not None and reading.is_bare
    )
    for rule in WEAKNESS_RULES:
        table = shape_table(readings, rule)
        assert sum(count.segments for count in table) == len(readings)
        for count in table:
            assert count.with_wasla <= count.segments


def test_the_idgham_mechanism_splits_the_doubled_root_both_ways() -> None:
    readings = tuple(
        reading
        for reading in (read_imperative(record) for record in synthetic_records())
        if reading is not None and reading.is_bare
    )
    agreement = idgham_agreement(readings)
    assert agreement.assimilated_without_wasla == 1
    assert agreement.broken_with_wasla == 1
    assert agreement.disagreeing == 0


def test_the_hollow_zero_holds_under_every_declared_rule() -> None:
    for table in REDERIVED_SHAPE_TABLES.values():
        assert table["أجوف"][0] == 0


def test_every_rule_repartitions_the_same_total() -> None:
    assert set(REDERIVED_SHAPE_TABLES) == set(RULES)
    for table in REDERIVED_SHAPE_TABLES.values():
        assert (
            sum(segments for _, segments in table.values()) == BARE_IMPERATIVE_SEGMENTS
        )


def test_the_sound_rate_is_not_one_number_but_moves_with_the_rule() -> None:
    narrow = REDERIVED_SHAPE_TABLES["علّة_فقط"]["سالم"]
    wide = REDERIVED_SHAPE_TABLES["علّة_وهمزة_والمضاعف_مُفرَد"]["سالم"]
    assert narrow == (510, 604)
    assert wide == (493, 493)
    assert narrow[0] / narrow[1] < wide[0] / wide[1]


def test_the_fourteen_sound_exceptions_are_exactly_the_doubled_ones() -> None:
    with_hamza = REDERIVED_SHAPE_TABLES["علّة_وهمزة"]["سالم"]
    separated = REDERIVED_SHAPE_TABLES["علّة_وهمزة_والمضاعف_مُفرَد"]["سالم"]
    assert with_hamza[1] - with_hamza[0] == 14
    assert separated[1] - separated[0] == 0


def test_the_doubled_counts_agree_between_the_table_and_the_mechanism() -> None:
    doubled = REDERIVED_SHAPE_TABLES["علّة_فقط_والمضاعف_مُفرَد"]["مضاعف"]
    assert REDERIVED_IDGHAM_AGREEMENT.total == doubled[1] == 22
    assert REDERIVED_IDGHAM_AGREEMENT.broken_with_wasla == doubled[0] == 8
    assert REDERIVED_IDGHAM_AGREEMENT.agreeing == 21


def test_the_permutation_p_value_has_a_floor_and_never_reaches_zero() -> None:
    floor = 1 / (1 + PERMUTATION_PROTOCOL.permutations)
    for outcome in REDERIVED_SALIM_AJWAF_TEST.values():
        assert outcome.p_value >= floor
        assert outcome.p_value > 0.0


def test_the_permutation_is_deterministic_under_the_frozen_seed() -> None:
    first = [True] * 30 + [False] * 5
    second = [False] * 35
    assert permutation_test("اختبار", first, second) == permutation_test(
        "اختبار", first, second
    )


def test_an_empty_group_is_refused_rather_than_counted_as_zero() -> None:
    with pytest.raises(ImperativeWaslaCensusError):
        permutation_test("اختبار", [], [True, False])


def test_the_absent_imperfect_is_counted_not_turned_into_a_denial() -> None:
    coexistence = REDERIVED_IMPERFECT_COEXISTENCE
    assert coexistence.without_bare_imperfect == 33
    assert coexistence.without_any_imperfect == 25
    assert coexistence.with_bare_imperfect + coexistence.without_bare_imperfect == (
        coexistence.imperative_roots
    )


def test_the_two_residual_positions_are_named_and_kept() -> None:
    assert (DOUBLED_ROOT_RESIDUAL.sura, DOUBLED_ROOT_RESIDUAL.aya) == (33, 33)
    assert DOUBLED_ROOT_RESIDUAL.root == "qrr"
    assert (NAQIS_RESIDUAL.sura, NAQIS_RESIDUAL.aya) == (2, 186)
    assert NAQIS_RESIDUAL.root == "dEw"
    for residual in (DOUBLED_ROOT_RESIDUAL, NAQIS_RESIDUAL):
        assert residual.why_it_is_named.strip()


def test_the_arriving_figures_are_each_answered() -> None:
    assert len(ARRIVING_IMPERATIVE_DIVERGENCES) == 17
    matched = [item for item in ARRIVING_IMPERATIVE_DIVERGENCES if item.matched]
    assert len(matched) == 2
    labels = {item.figure.label for item in matched}
    assert labels == {"اللفيفُ بهمزة وصل", "استثناءاتُ الناقص"}
    for divergence in ARRIVING_IMPERATIVE_DIVERGENCES:
        assert divergence.rederived_value.strip()
        assert divergence.under_rule.strip()


def test_the_claimed_zero_p_value_is_recorded_as_not_rederived() -> None:
    claim = next(
        item
        for item in ARRIVING_IMPERATIVE_DIVERGENCES
        if item.figure.label == "احتمالُ الفارق"
    )
    assert claim.figure.claimed_value == "0.0000"
    assert claim.matched is False


def test_the_named_residuals_are_declared() -> None:
    assert set(IMPERATIVE_WASLA_CENSUS_NAMED_RESIDUALS) == {
        "TheSoundExceptionsWereAllOneThing",
        "TheMechanismWasTestedInsideOneClassNotBetweenTwo",
        "OneQacTagCarriesTheWholeNaqisException",
        "TheOneDoubledResidualIsTheContestedFormItself",
        "TheImperfectAsAPreconditionWasNotSettled",
        "Sha256OrdersNothing",
        "ASecondArrivingTableIsNotASecondMeasurement",
        "SplitLafifIsAFifthRuleNotAReading",
        "TheScopeOfTheArrivingRatioWasNotDeclared",
    }
    for name, note in IMPERATIVE_WASLA_CENSUS_NAMED_RESIDUALS.items():
        assert note.startswith(f"{name}:")


@pytest.mark.skipif(
    CORPUS_PATH_VARIABLE not in os.environ,
    reason=(
        f"يُفعَّل بوضع مسار المدوَّنة المُبصَّمة في {CORPUS_PATH_VARIABLE}؛ "
        "وبايتاتُها غيرُ منسوخةٍ إلى الشجرة."
    ),
)
def test_the_frozen_census_rederives_from_the_witness_bytes() -> None:
    path = Path(os.environ[CORPUS_PATH_VARIABLE])
    records = [
        record
        for record in (parse_segment_line(line) for line in corpus_lines(path))
        if record is not None
    ]
    readings = tuple(
        reading
        for reading in (read_imperative(record) for record in records)
        if reading is not None and reading.is_bare
    )

    assert len(readings) == BARE_IMPERATIVE_SEGMENTS
    for rule in WEAKNESS_RULES:
        measured = {
            count.shape.value: (count.with_wasla, count.segments)
            for count in shape_table(readings, rule)
        }
        assert measured == REDERIVED_SHAPE_TABLES[rule.name]
    for rule_name, frozen in REDERIVED_SALIM_AJWAF_TEST.items():
        rule = RULES[rule_name]
        sound = [
            reading.has_wasla
            for reading in readings
            if classify_root(reading.root, rule) is RootShape.SALIM
        ]
        hollow = [
            reading.has_wasla
            for reading in readings
            if classify_root(reading.root, rule) is RootShape.AJWAF
        ]
        assert permutation_test(frozen.label, sound, hollow) == frozen
    assert idgham_agreement(readings) == REDERIVED_IDGHAM_AGREEMENT
    assert imperfect_coexistence(records) == REDERIVED_IMPERFECT_COEXISTENCE


def test_the_second_arriving_table_is_recorded_as_divergence_not_as_a_rule() -> None:
    """الجدولُ الثاني الواردُ يُسجَّل فرقًا، ولا يُمَسُّ به رقمٌ مُعادُ الاشتقاق."""

    assert len(SECOND_ARRIVING_SHAPE_FIGURES) == 10
    matched = {figure.label for figure in second_arriving_figures_that_matched()}
    assert matched == {"الأجوفُ بألف وصل", "المثالُ بألف وصل"}
    without_a_rule = second_arriving_figures_without_a_rule()
    assert len(without_a_rule) == 2
    assert all("لفيف" in figure.label for figure in without_a_rule)
    assert all(figure.rederived_value is None for figure in without_a_rule)
    assert specification_digest() == IMPERATIVE_WASL_SPECIFICATION_DIGEST
    assert set(REDERIVED_SHAPE_TABLES) == {rule.name for rule in WEAKNESS_RULES}


def test_the_second_arriving_notes_are_named_residuals() -> None:
    for name in (
        "ASecondArrivingTableIsNotASecondMeasurement",
        "SplitLafifIsAFifthRuleNotAReading",
        "TheScopeOfTheArrivingRatioWasNotDeclared",
    ):
        assert name in IMPERATIVE_WASLA_CENSUS_NAMED_RESIDUALS
